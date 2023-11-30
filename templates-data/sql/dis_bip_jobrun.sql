--Copyright © 2023, Oracle and/or its affiliates. 
--The Universal Permissive License (UPL), Version 1.0 as shown at https://oss.oracle.com/licenses/upl.

  CREATE TABLE "METADATA_SCHEMA"."DIS_BIP_JOBRUN"
   (	"BIP_REPORT_PIPELINE_NAME" VARCHAR2(2000 BYTE) ,
	"FROM_DATE" TIMESTAMP (6),
	"IS_LOCKED" VARCHAR2(1 BYTE)
   );
