"""Scoped conversation state. Existing client_memory JSON, no schema migration or deletion."""
from __future__ import annotations
import copy,datetime,fcntl,hashlib,json,re,unicodedata,uuid
from pathlib import Path
from urllib.parse import quote
KEY='_behavior_state_v1'
FILTERS={'city','neighborhood','property_type','price_min','price_max','bedrooms_min','bathrooms_min','parking_min','area_min','pet_friendly','zone'}
def norm(v):
 return ''.join(c for c in unicodedata.normalize('NFD',str(v or '').lower())if not unicodedata.combining(c))
def transition(previous,text,message_id):
 s=copy.deepcopy(previous or {});s.setdefault('query_id',uuid.uuid4().hex);s.setdefault('filters',{});s.setdefault('cleared',[]);s.setdefault('purpose','');s.setdefault('beneficiary','self');s.setdefault('agent_ia',False);s.setdefault('closed',False)
 if s.get('last_message_id')==message_id:return s
 t=norm(text)
 # Only explicit first-person identity; professional role, questions and mentions are not bot evidence.
 if '?'not in str(text)and re.search(r'^(?:ola[,.! ]+)?(?:eu )?sou (?:uma? )?(?:agente (?:de )?ia|assistente virtual(?: de ia)?|(?:robo|bot)(?: de atendimento)?)\b',t.strip()):
  s['agent_ia']=True;s['agent_ia_evidence']='explicit_self_identification'
 beneficiary='sogra'if re.search(r'\b(?:para|pra|da) (?:a )?(?:minha )?sogra\b',t)else 'self'if re.search(r'\b(?:para|pra) mim\b|\bminha propria procura\b',t)else None
 purpose='rent'if re.search(r'\b(?:arrendar|arrendamento|alugar|aluguel|locacao)\b',t)else 'sale'if re.search(r'\b(?:comprar|compra)\b',t)else None
 reset=bool(re.search(r'\b(?:esquece|esqueca|retire|remova|sem) (?:qualquer |todos os |os )?filtros?\b|\bnova procura (?:ampla|sem filtros)\b',t))
 switched=bool((purpose and purpose!=s['purpose'])or(beneficiary and beneficiary!=s['beneficiary']))
 if reset or switched:
  s['query_id']=uuid.uuid4().hex;s['filters']={};s['cleared']=sorted(FILTERS)
 if purpose:s['purpose']=purpose
 if beneficiary:s['beneficiary']=beneficiary
 if re.search(r'\b(?:sem (?:limite(?: de)?|restricao(?: de)?|filtro(?: de)?) (?:preco|orcamento)|nao (?:restringi|limitei|defini|estipulei) (?:o )?(?:preco|orcamento)|(?:esquece|esqueca|retire|remova) (?:o )?(?:limite|orcamento))\b|\bsem limite\b',t):
  for k in ['price_min','price_max']:s['filters'].pop(k,None)
  s['cleared']=sorted(set(s['cleared'])|{'price_min','price_max'})
 # Explicit fresh criteria replace only their own fields.
 type_map={'apartamento':'apartment','studio':'studio','estudio':'studio','casa':'house','moradia':'house'}
 if not re.search(r'\b(?:qualquer tipo|todos os tipos)\b',t):
  for token,value in type_map.items():
   if re.search(r'\b'+token+r's?\b',t):s['filters']['property_type']=value;s['cleared']=[k for k in s['cleared']if k!='property_type'];break
 else:s['filters'].pop('property_type',None);s['cleared']=sorted(set(s['cleared'])|{'property_type'})
 city=re.search(r'\b(?:na cidade de|cidade[: ]+|agora em)\s+([A-Za-zÀ-ÿ ]{3,50})(?:[,;.!?]|$)',str(text),re.I)
 if city:s['filters']['city']=city[1].strip();s['filters'].pop('neighborhood',None);s['cleared']=[k for k in s['cleared']if k!='city']
 budget=re.search(r'\b(?:ate|orcamento (?:de|e)|limite (?:de|e))\s*(?:r\$\s*)?(\d+(?:[.,]\d+)?)\s*(mil|milhao|milhoes)?\b',t)
 if budget:
  value=float(budget[1].replace(',','.'));value*=1000 if budget[2]=='mil'else 1000000 if budget[2]else 1
  s['filters']['price_max']=value;s['cleared']=[k for k in s['cleared']if k not in {'price_min','price_max'}]
 wants_text=bool(re.search(r'\b(?:por escrito|sem audio|(?:responda|responde|envie|mande|prefiro|quero)(?: so| somente)? (?:em |por )?texto)\b',t))
 wants_audio=bool(re.search(r'\b(?:responda|responde|envie|mande|manda|prefiro|quero|pode responder)(?: (?:a resposta|isso|isto))? (?:em |por )?(?:audio|voz)\b',t))
 s['response_mode']='text'if wants_text else 'audio'if wants_audio else None
 # End only a closure/explicit refusal, not an unrelated negative answer to qualification.
 closure=bool(re.search(r'\b(?:ate logo|ate mais|tchau|adeus|nao preciso de mais nada|nao quero mais(?: nada| atendimento)?|nao me (?:responda|envie)|pode encerrar)\b',t))
 if closure:s['closed']=True
 elif s['closed']and re.search(r'\b(?:quero|procuro|gostaria|preciso|mostre|mande|marcar|comprar|arrendar|imovel|apartamento)\b',t):s['closed']=False
 if re.search(r'\b(?:fotos?|fotografias?|imagens?)\b',t)and re.search(r'\b(?:errad[ao]s?|nao (?:sao|e|correspondem)|diverg|outro imovel|nao parecem)\b',t):
  selected=s.get('selected_property',{});pid=selected.get('id')
  if pid:s.setdefault('photo_disputes',{})[pid]={'status':'pending_review','message_id':message_id}
 rows=s.get('last_shortlist',[])
 selected=[r for r in rows if r.get('property_code')and re.search(r'(?<![\w-])'+re.escape(norm(r['property_code']))+r'(?![\w-])',t)]
 ordinal=re.search(r'\b(?:opcao|imovel)\s*([1-3])\b',t)
 if ordinal and int(ordinal[1])<=len(rows):selected=[rows[int(ordinal[1])-1]]
 if len(selected)==1:s['selected_property']=copy.deepcopy(selected[0])
 s['last_message_id']=message_id;s['updated_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
 return s
def apply_criteria(criteria,state,text):
 c=copy.deepcopy(criteria);state=state or {};t=norm(text)
 if c.get('search_mode') in {'property_code','property_url'}or c.get('property_code')or c.get('property_url'):return c
 if state.get('purpose'):c['purpose']=state['purpose']
 for k in FILTERS:
  candidate=c.get(k);fresh=isinstance(candidate,str)and norm(candidate).strip()and norm(candidate).strip()in t
  if k in state.get('cleared',[])and not fresh:c[k]=None if k in {'price_min','price_max','bedrooms_min','bathrooms_min','parking_min','area_min','pet_friendly'}else ''
  if k in state.get('filters',{}):c[k]=state['filters'][k]
 return c
class BehaviorService:
 def __init__(self,rest,state_dir):
  self.rest=rest;self.root=Path(state_dir);self.root.mkdir(exist_ok=True,parents=True,mode=0o700)
 def scope(self,b):
  co=str(b.get('company_id')or'').strip();cl=str(b.get('client_id')or'').strip()
  if not co or not cl:raise ValueError('behavior_context_required')
  q='company_id=eq.'+quote(co,safe='')+'&id=eq.'+quote(cl,safe='')
  rows=self.rest.select('clients',q+'&select=id,company_id&limit=2')or[]
  if len(rows)!=1 or rows[0]['id']!=cl or rows[0]['company_id']!=co:raise ValueError('behavior_client_scope_forbidden')
  return co,cl
 def read(self,co,cl):
  q='company_id=eq.'+quote(co,safe='')+'&client_id=eq.'+quote(cl,safe='')+'&key=eq.'+KEY+'&select=value&limit=2'
  rows=self.rest.select('client_memory',q)or[]
  rows=[r for r in rows if r.get('key',KEY)==KEY]
  if len(rows)>1:raise ValueError('behavior_state_duplicate')
  if not rows:return {}
  value=rows[0].get('value');s=json.loads(value)if isinstance(value,str)else value
  if not isinstance(s,dict):raise ValueError('behavior_state_invalid')
  return s
 def write(self,co,cl,s,key=KEY):
  row={'company_id':co,'client_id':cl,'key':key,'value':json.dumps(s,ensure_ascii=False,separators=(',',':'))}
  result=self.rest._json_request('POST','/rest/v1/client_memory?on_conflict=company_id,client_id,key',row,{'Prefer':'resolution=merge-duplicates,return=representation'})
  if not isinstance(result,list)or len(result)!=1 or result[0].get('value')!=row['value']:raise ValueError('behavior_persistence_unconfirmed')
 def locked(self,co,cl,callback):
  file=self.root/(hashlib.sha256((co+':'+cl).encode()).hexdigest()+'.lock')
  with file.open('a')as lock:
   fcntl.flock(lock,fcntl.LOCK_EX)
   try:return callback()
   finally:fcntl.flock(lock,fcntl.LOCK_UN)
 def context(self,b):
  co,cl=self.scope(b)
  def run():
   prior=self.read(co,cl);s=transition(prior,str(b.get('input_text')or''),str(b.get('message_id')or''))
   if s!=prior:self.write(co,cl,s)
   if re.search(r'\b(?:imovel|apartamento|casa|anuncio)\b',norm(b.get('input_text')) )and re.search(r'\bvendid[ao]\b',norm(b.get('input_text'))):
    s['professional_notice']=self._notice(b);self.write(co,cl,s)
   memory=[{'key':k,'value':v,'scope':{'query_id':s['query_id'],'purpose':s['purpose'],'beneficiary':s['beneficiary']},'updated_at':s['updated_at']}for k,v in s['filters'].items()]
   if s['purpose']:memory.append({'key':'purpose','value':s['purpose']})
   if s.get('last_shortlist'):memory.append({'key':'last_shortlist','value':json.dumps(s['last_shortlist'],ensure_ascii=False)})
   if s.get('selected_property'):memory.append({'key':'selected_property','value':json.dumps(s['selected_property'],ensure_ascii=False)})
   return {'ok':True,'state':s,'memory':memory,'suppress_response':s['agent_ia']or(s['closed']and prior.get('closed',False))}
  return self.locked(co,cl,run)
 def policy(self,b):
  co,cl=self.scope(b);s=self.read(co,cl)
  return {'ok':True,'criteria':apply_criteria(b.get('criteria')or{},s,str(b.get('input_text')or'')),'state':s}
 def save_shortlist(self,b):
  co,cl=self.scope(b)
  def run():
   s=self.read(co,cl);rows=b.get('results')or[]
   criteria=b.get('criteria')or{}
   for k in FILTERS:
    value=criteria.get(k)
    if value is not None and value!='' and value!=0:s.setdefault('filters',{})[k]=value;s['cleared']=[x for x in s.get('cleared',[])if x!=k]
   if criteria:self.write(co,cl,s)
   if not isinstance(rows,list):raise ValueError('shortlist_array_required')
   if rows:
    s['last_shortlist']=[{k:r.get(k)for k in ['id','property_code','title','address','city','neighborhood','price']}for r in rows]
    if len(rows)==1:s['selected_property']=s['last_shortlist'][0]
    self.write(co,cl,s)
   return {'ok':True,'state':s}
  return self.locked(co,cl,run)
 def preference(self,b):
  co,cl=self.scope(b);key=str(b.get('key')or'')
  if key not in FILTERS|{'purpose'}:raise ValueError('preference_key_not_allowed')
  def run():
   s=self.read(co,cl);value=b.get('value')
   if key=='purpose':
    value={'compra':'sale','aluguel':'rent','arrendamento':'rent','venda':'sale'}.get(norm(value),value)
    s=transition(s,'quero comprar'if value=='sale'else'quero arrendar'if value=='rent'else'',str(b.get('message_id')or uuid.uuid4().hex))
   elif key in {'price_min','price_max'}:
    if not s.get('purpose'):return {'ok':False,'status':'needs_purpose','user_message':'Este orçamento é para compra ou arrendamento?'}
    if norm(value)in {'sem limite','null','nenhum','sem restricao'}:s.setdefault('filters',{}).pop(key,None);s['cleared']=sorted(set(s.get('cleared',[]))|{key})
    else:s.setdefault('filters',{})[key]=float(str(value).replace(',','.'));s['cleared']=[x for x in s.get('cleared',[])if x!=key]
   else:s.setdefault('filters',{})[key]=value;s['cleared']=[x for x in s.get('cleared',[])if x!=key]
   s.setdefault('durable_preferences',{})[s.get('purpose','')+':'+s.get('beneficiary','self')]=copy.deepcopy(s.get('filters',{}))
   self.write(co,cl,s);return {'ok':True,'status':'saved','key':key,'value':value,'query_id':s.get('query_id'),'evidence':{'persistence_confirmed':True}}
  return self.locked(co,cl,run)
 def catalog(self,b):
  co,cl=self.scope(b);rows=[];offset=0
  while True:
   page=self.rest.select('products','company_id=eq.'+quote(co,safe='')+'&status=eq.active&product_type=eq.real_estate&select=id,company_id,property_code,title,description,price,data,responsible_user_id,latitude,longitude,geocoded_address,google_place_id&order=id.asc&limit=500&offset='+str(offset))or[]
   rows.extend(page)
   if len(page)<500:break
   offset+=len(page)
   if offset>=100000:raise ValueError('catalog_pagination_incomplete')
  return {'ok':True,'rows':rows,'complete_pagination':True}
 def ingress(self,body):
  p=body.get('payload')or{};sender=str(p.get('from')or'')
  if not re.fullmatch(r'\d{8,15}@(c\.us|s\.whatsapp\.net)',sender):return {'blocked':False}
  from visit_owner_contact import resolve_owner_contact
  owner=resolve_owner_contact(self.rest);co=owner['company_id'];phone=sender.split('@')[0]
  rows=self.rest.select('clients','company_id=eq.'+quote(co,safe='')+'&phone=eq.'+quote(phone,safe='')+'&select=id,company_id&limit=2')or[]
  if len(rows)!=1:return {'blocked':False}
  cl=rows[0]['id'];s=self.read(co,cl)
  if s.get('agent_ia'):return {'blocked':True,'reason':'agent_ia'}
  text=str(p.get('body')or'');candidate=transition(s,text,str(p.get('id')or''))
  if candidate.get('agent_ia'):
   self.locked(co,cl,lambda:self.write(co,cl,candidate))
   return {'blocked':True,'reason':'explicit_agent_ia'}
  return {'blocked':False}
 def photo_allowed(self,b):
  co,cl=self.scope(b);s=self.read(co,cl);pid=b.get('product_id')
  allowed=pid not in s.get('photo_disputes',{})
  return {'ok':allowed,'allowed':allowed,'status':'allowed'if allowed else'pending_photo_review','user_message':''if allowed else'As fotografias contestadas estão suspensas até ser verificada a associação ao imóvel.'}
 def _notice(self,b):
  from sold_notice_worker import notice_key,notice_result
  co,cl=self.scope(b);mid=str(b.get('message_id')or'')
  if not mid:raise ValueError('message_id_required')
  key=notice_key(mid)
  q='company_id=eq.'+quote(co,safe='')+'&client_id=eq.'+quote(cl,safe='')+'&key=eq.'+key+'&select=key,value&limit=2'
  rows=[r for r in(self.rest.select('client_memory',q)or[])if r.get('key')==key]
  if len(rows)>1:raise ValueError('notice_duplicate')
  text=str(b.get('input_text')or'')[:2000]
  if rows:
   row=json.loads(rows[0]['value'])
   if row.get('text')!=text or row.get('source_client_id')!=cl or row.get('message_id')!=mid:raise ValueError('notice_message_collision')
  else:
   row={'status':'pending','kind':'sold_notice','message_id':mid,'text':text,'source_client_id':cl,'provider_receipt':None,'qa':b.get('qa')is True}
   self.write(co,cl,row,key=key)
  return notice_result(row)
 def notice(self,b):
  co,cl=self.scope(b)
  return self.locked(co,cl,lambda:self._notice(b))
