Map<Id,user> usermap= new Map<Id,user>([Select Id From User Where IsActive = true and LastModifiedDate = TODAY and Id <> '0058K000002okL7QAI']);

for(user u : usermap.values()){
    pse__Permission_Control__c  psa = new pse__Permission_Control__c ();
    psa.pse__User__c  = u.Id;
    psa.pse__Timecard_Entry__c  = True;
    psa.pse__Resource_Request_Entry__c  = true;
    
    psa.pse__Timecard_Ops_Edit__c   = true;
    
    psa.pse__Expense_Entry__c   = true;
    psa.pse__Create_Project_Version__c   = true;
    psa.pse__Compare_Project_Version__c	  = true;
    psa.pse__Skills_And_Certifications_View__c   = true;
    
    psa.pse__View_Task_Manager__c    = true;
    psa.pse__Edit_Task_Manager__c    = true;
    psa.pse__Forecast_View__c    = true;
    psa.pse__Forecast_Edit__c     = true;
    
    psa.pse__Region__c  = 'a9N8K000000KzPSUA0';
    insert psa;
}


delete [select Id from PermissionSetAssignment where  PermissionSetId ='0PS1T000000OGdn' and AssigneeId IN :usermap.keyset()];

for(user u : usermap.values()){
    System.setPassword(u.Id, 'FRR@salesforce23');
}

for(user u : usermap.values()){
    PermissionSetAssignment psa = new PermissionSetAssignment();
    psa.AssigneeId = u.Id;
    psa.PermissionSetGroupId = '0PG8K000000LBcyWAG';
    //psa.IsActive = true;
    insert psa;
}