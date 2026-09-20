from conftest import CONTRACT
PLEDGES=[{'member':'upper field','work':'Clear the north irrigation gate.','points':10},{'member':'lower field','work':'Repair the shared stone channel.','points':8}]
URLS=['https://journal.example/round','https://witness.example/round']
def setup(vm,deploy,a,b):
 vm.warp('2035-01-01T00:00:00+00:00');vm.sender=a;c=deploy(CONTRACT);c.convene('spring-5','0x'+b.hex(),'Spring channel work',PLEDGES,600);return c
def mocks(vm,done='[0,1]',partial='[]',missing='[]',earned='[10,8]'):
 vm.mock_web(r'journal\.example',{'status':200,'body':'north gate cleared; stone channel repaired'});vm.mock_web(r'witness\.example',{'status':200,'body':'independent village work log'});vm.mock_llm(r'.*CommonsCarry work audit.*','{"completed_indexes":'+done+',"partial_indexes":'+partial+',"missing_indexes":'+missing+',"earned_points":'+earned+',"note":"Shared work was reconciled without erasing partial effort."}')
def test_balanced_round_settles(direct_vm,direct_deploy,direct_alice,direct_bob):
 c=setup(direct_vm,direct_deploy,direct_alice,direct_bob);direct_vm.sender=direct_bob;mocks(direct_vm);c.audit('spring-5',URLS);assert c.get_round('spring-5')['carry_points']==[0,0];direct_vm.warp('2035-01-01T00:10:01+00:00');direct_vm.sender=direct_alice;c.settle('spring-5');assert c.get_round('spring-5')['state']=='SETTLED'
def test_partial_work_preserves_credit_and_carry(direct_vm,direct_deploy,direct_alice,direct_bob):
 c=setup(direct_vm,direct_deploy,direct_alice,direct_bob);direct_vm.sender=direct_bob;mocks(direct_vm,'[0]','[1]','[]','[10,3]');c.audit('spring-5',URLS);r=c.get_round('spring-5');assert r['state']=='CARRY_OPEN' and r['carry_points']==[0,5]
def test_keeper_only_audit(direct_vm,direct_deploy,direct_alice,direct_bob):
 c=setup(direct_vm,direct_deploy,direct_alice,direct_bob);mocks(direct_vm)
 with direct_vm.expect_revert('keeper audit'):c.audit('spring-5',URLS)
def test_validator_rejects_inflated_partial_credit(direct_vm,direct_deploy,direct_alice,direct_bob):
 c=setup(direct_vm,direct_deploy,direct_alice,direct_bob);mocks(direct_vm,'[0]','[1]','[]','[10,3]');x=c.rounds['SPRING-5'];r=c._audit(x,URLS);assert direct_vm.run_validator(leader_result=r) is True;f=dict(r);f['earned_points']=[10,8];assert direct_vm.run_validator(leader_result=f) is False
def test_logs_require_distinct_origins(direct_vm,direct_deploy,direct_alice,direct_bob):
 c=setup(direct_vm,direct_deploy,direct_alice,direct_bob);direct_vm.sender=direct_bob
 with direct_vm.expect_revert('independent logs'):c.audit('spring-5',['https://journal.example/a','https://journal.example/b'])
