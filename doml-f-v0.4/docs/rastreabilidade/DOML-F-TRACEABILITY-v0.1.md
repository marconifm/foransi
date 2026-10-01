# DOML-F Traceability Matrix v0.1

  -----------------------------------------------------------------------
  Requirement group       DOML-F component        Rule/test family
  ----------------------- ----------------------- -----------------------
  RF-MOD                  model, metadata, nodes, DOML-R001..R005
                          networks, services      

  RF-PROV                 providers, concrete     DOML-R050..R055
                          infrastructure          

  RF-SVC                  services                schema + semantic
                                                  service tests

  RF-LOG                  telemetry               telemetry validation

  SEG                     networks, nodes,        DOML-R020..R025
                          secret_ref, hardening,  
                          attacks                 

  FOR                     evidence, collection,   DOML-R030..R036
                          manifest, custody_event 

  EXP                     scenario, attack,       DOML-R040..R048
                          baseline, experiment,   
                          ground_truth            

  REP                     model, providers,       DOML-R050..R060
                          images, manifests,      
                          validations             

  DADO                    data-generation         semantic validator
                          metadata and            
                          synthetic-data policy   

  UC-01                   all model entities      syntax + semantic

  UC-02                   providers, nodes,       generator/integration
                          networks, storage       

  UC-03                   baseline, telemetry,    baseline tests
                          hardening               

  UC-04..09               scenario, attack,       controlled scenario
                          services, telemetry     tests

  UC-10..11               collection, evidence,   forensic tests
                          manifest, custody       

  UC-12                   baseline, restore state restore tests

  UC-13                   model, exports,         replication tests
                          manifests               

  UC-14                   validation, manifest,   audit tests
                          hashes                  
  -----------------------------------------------------------------------
