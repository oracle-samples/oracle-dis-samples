--Copyright © 2023, Oracle and/or its affiliates. 
--The Universal Permissive License (UPL), Version 1.0 as shown at https://oss.oracle.com/licenses/upl.

create or replace procedure check_bip_jobrun (p_bip_report_pipeline_name IN varchar2, p_wait_in_seconds IN integer, p_from_date IN OUT timestamp, p_first_time IN OUT varchar ) is
cursor get_pipeline is
select bip_report_pipeline_name, from_date, is_locked from dis_bip_jobrun
where bip_report_pipeline_name = p_bip_report_pipeline_name;

pipeline_rec get_pipeline%ROWTYPE;

begin
    open get_pipeline;
    fetch get_pipeline into pipeline_rec.bip_report_pipeline_name, pipeline_rec.from_date, pipeline_rec.is_locked;
    if get_pipeline%NOTFOUND then -- first time run
        insert into dis_bip_jobrun values (p_bip_report_pipeline_name, nvl(p_from_date, sysdate), 'Y');
        p_first_time := 'Y';
        commit;
    else
        if pipeline_rec.is_locked = 'Y' then -- check if pipeline is running
            close get_pipeline;
                while pipeline_rec.is_locked = 'Y'
                loop
                    dbms_session.sleep(p_wait_in_seconds); -- wait for until next check
                    open get_pipeline;
                    fetch get_pipeline into pipeline_rec.bip_report_pipeline_name, pipeline_rec.from_date, pipeline_rec.is_locked;
                    close get_pipeline;
                end loop;
        end if;
        update dis_bip_jobrun set is_locked = 'Y' where bip_report_pipeline_name = p_bip_report_pipeline_name;
        P_FROM_DATE := pipeline_rec.from_date;
        P_FIRST_TIME := 'N';
        commit;
    end if;
end;