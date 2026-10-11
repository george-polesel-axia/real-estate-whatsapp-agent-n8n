"""Scoped durable owner outbox. Uncertain transport is never blindly retried."""
import hashlib,json,re,threading,time,logging
from urllib.parse import quote
from behavior_state import norm
PREFIX='_professional_notice_'
def notice_key(mid):return PREFIX+hashlib.sha256(mid.encode()).hexdigest()[:24]
def notice_result(row):
 delivered=row.get('status')=='delivered'and(row.get('provider_receipt')or{}).get('provider_accepted')is True
 return {'ok':True,'status':'forwarded_to_owner'if delivered else 'recorded_for_test'if row.get('qa')is True else'recorded_pending_delivery','receipt':{'persistence_confirmed':True,'provider_confirmed':delivered},'user_message':'O aviso foi encaminhado ao responsável para verificação.'if delivered else'O aviso ficou registado para verificação. O encaminhamento ainda está pendente.'}
class SoldNoticeWorker:
 def __init__(self,service,owner_resolver,sender):self.service=service;self.rest=service.rest;self.owner_resolver=owner_resolver;self.sender=sender
 def process(self,co,cl,key,allow_qa=False):
  owner=self.owner_resolver(self.rest)
  if owner['company_id']!=co:raise ValueError('notice_company_forbidden')
  self.service.scope({'company_id':co,'client_id':cl})
  def run():
   q='company_id=eq.'+quote(co,safe='')+'&client_id=eq.'+quote(cl,safe='')+'&key=eq.'+quote(key,safe='')+'&select=key,value&limit=2'
   rows=self.rest.select('client_memory',q)or[]
   rows=[x for x in rows if x.get('key')==key]
   if len(rows)!=1:raise ValueError('notice_single_record_required')
   row=json.loads(rows[0]['value'])
   if row.get('kind')!='sold_notice'or row.get('source_client_id')!=cl or notice_key(str(row.get('message_id')or''))!=key:raise ValueError('notice_identity_forbidden')
   if row.get('status')!='pending':return notice_result(row)
   clients=self.rest.select('clients','company_id=eq.'+quote(co,safe='')+'&id=eq.'+quote(cl,safe='')+'&select=id,name&limit=2')
   if len(clients)!=1 or clients[0]['id']!=cl:raise ValueError('notice_client_forbidden')
   qa=row.get('qa')is True or bool(re.search(r'\b(?:qa|e2e|test|teste|fixture|synthetic)\b',norm(clients[0].get('name'))))
   if qa and not allow_qa:return notice_result(row)
   text=('TESTE AUTORIZADO — 'if qa else'')+'Patrícia v5 — Aviso de imóvel vendido recebido.\nInformação relatada; confirmar imóvel e venda antes de alterar o cadastro.\nReferência interna: '+hashlib.sha256((co+cl+key).encode()).hexdigest()[:12]+'\nRelato: '+str(row.get('text')or'')[:2000]
   delivery_key='SOLD_NOTICE_'+hashlib.sha256((co+':'+cl+':'+key).encode()).hexdigest()
   try:
    receipt=self.sender(delivery_key,text)
    if receipt.get('provider_accepted')is not True or receipt.get('owner_verified')is not True:raise ValueError('notice_provider_receipt_invalid')
   except Exception:
    row['status']='delivery_uncertain';row['provider_receipt']=None;row['last_error']='provider_outcome_uncertain_no_retry'
    self.service.write(co,cl,row,key=key)
    return notice_result(row)
   row.update(status='delivered',provider_receipt=receipt,forwarded_to_user_id=owner['owner_user_id'],delivered_at=time.time(),qa=qa)
   self.service.write(co,cl,row,key=key)
   return notice_result(row)
  return self.service.locked(co,cl,run)
 def tick(self):
  co=self.owner_resolver(self.rest)['company_id'];offset=0
  while True:
   rows=self.rest.select('client_memory','company_id=eq.'+quote(co,safe='')+'&key=like.'+PREFIX+'*&select=client_id,key,value&order=key.asc,client_id.asc&limit=100&offset='+str(offset))or[]
   for r in rows:
    try:
     if json.loads(r['value']).get('status')=='pending':self.process(co,r['client_id'],r['key'])
    except Exception as e:logging.warning('sold_notice_worker_record_failed:%s',type(e).__name__)
   if len(rows)<100:break
   offset+=len(rows)
 def start(self):
  def loop():
   while True:
    try:self.tick()
    except Exception as e:logging.warning('sold_notice_worker_poll_failed:%s',type(e).__name__)
    time.sleep(30)
  threading.Thread(target=loop,name='sold-notice-worker',daemon=True).start()
