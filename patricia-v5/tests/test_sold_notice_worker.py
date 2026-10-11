import sys,unittest,tempfile,json
from pathlib import Path
sys.path[:0]=[str(Path(__file__).resolve().parents[1]/'backend')]
from behavior_state import BehaviorService
from sold_notice_worker import SoldNoticeWorker,notice_key
class Rest:
 def __init__(self):self.mem={};self.clients=[{'id':'client','company_id':'co','name':'Cliente real'}]
 def select(self,table,q):
  if table=='clients':return self.clients
  if table=='client_memory':return list(self.mem.values())
  return []
 def _json_request(self,method,path,payload,headers):self.mem[payload['key']]=dict(payload);return [payload]
class Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.rest=Rest();self.service=BehaviorService(self.rest,self.tmp.name);self.sent=[]
  self.owner=lambda rest:{'company_id':'co','owner_user_id':'owner'}
  def sender(key,text):self.sent.append((key,text));return {'provider_accepted':True,'owner_verified':True,'message_id_sha256':'receipt'}
  self.worker=SoldNoticeWorker(self.service,self.owner,sender)
  self.body={'company_id':'co','client_id':'client','message_id':'message','input_text':'O imóvel ABC901 já foi vendido'}
  self.key=notice_key('message')
 def saved(self):return json.loads(self.rest.mem[self.key]['value'])
 def test_delivery_and_three_replays_send_once(self):
  self.service.context(self.body);self.worker.process('co','client',self.key)
  for i in range(3):
   self.assertTrue(self.service.context(self.body)['state']['professional_notice']['receipt']['provider_confirmed'])
   self.assertTrue(self.worker.process('co','client',self.key)['receipt']['provider_confirmed'])
  self.assertEqual(len(self.sent),1);self.assertEqual(self.saved()['status'],'delivered')
 def test_pending_replay_is_not_rewritten(self):
  self.service.notice(self.body);before=dict(self.rest.mem[self.key]);self.service.notice(self.body);self.assertEqual(before,self.rest.mem[self.key])
 def test_message_collision_refused(self):
  self.service.notice(self.body)
  with self.assertRaisesRegex(ValueError,'collision'):self.service.notice(dict(self.body,input_text='Outro relato'))
 def test_foreign_company_refused(self):
  self.service.notice(self.body)
  with self.assertRaisesRegex(ValueError,'company_forbidden'):self.worker.process('foreign','client',self.key)
  self.assertEqual(len(self.sent),0)
 def test_wrong_record_source_refused(self):
  self.service.notice(self.body);row=self.saved();row['source_client_id']='other';self.service.write('co','client',row,self.key)
  with self.assertRaisesRegex(ValueError,'identity_forbidden'):self.worker.process('co','client',self.key)
  self.assertEqual(len(self.sent),0)
 def test_explicit_qa_never_auto_sends(self):
  self.service.notice(dict(self.body,qa=True));self.worker.process('co','client',self.key);self.assertEqual(len(self.sent),0)
 def test_qa_client_never_auto_sends(self):
  self.rest.clients[0]['name']='Patricia QA fixture';self.service.notice(self.body);self.worker.process('co','client',self.key);self.assertEqual(len(self.sent),0)
 def test_uncertain_outcome_never_retried(self):
  self.service.notice(self.body)
  def fail(key,text):self.sent.append((key,text));raise RuntimeError('timeout')
  self.worker.sender=fail;self.worker.process('co','client',self.key)
  for i in range(3):self.service.notice(self.body);self.worker.process('co','client',self.key)
  self.assertEqual(len(self.sent),1);self.assertEqual(self.saved()['status'],'delivery_uncertain')
 def test_transport_receipt_without_owner_confirmation_rejected(self):
  self.service.notice(self.body);self.worker.sender=lambda key,text:{'provider_accepted':True}
  self.worker.process('co','client',self.key);self.assertEqual(self.saved()['status'],'delivery_uncertain')
 def test_explicit_controlled_qa_delivers_to_owner(self):
  self.service.notice(dict(self.body,qa=True));self.worker.process('co','client',self.key,allow_qa=True)
  self.assertTrue(self.saved()['qa']);self.assertEqual(len(self.sent),1);self.assertIn('TESTE AUTORIZADO',self.sent[0][1])
if __name__=='__main__':unittest.main()
