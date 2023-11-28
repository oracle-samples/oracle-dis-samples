--Copyright © 2023, Oracle and/or its affiliates. 
--The Universal Permissive License (UPL), Version 1.0 as shown at https://oss.oracle.com/licenses/upl.

create or replace procedure update_bip_jobrun (p_pipeline_name IN varchar2, p_from_date IN timestamp) is
begin
    update dis_bip_jobrun set is_locked = 'N', from_date = p_from_date where bip_report_pipeline_name = p_pipeline_name;
    commit;
end;
