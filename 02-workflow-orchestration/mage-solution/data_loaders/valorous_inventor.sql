-- Docs: https://docs.mage.ai/guides/sql-blocks
SELECT distinct(lpep_pickup_date) from mage.green_taxi order by lpep_pickup_date desc;