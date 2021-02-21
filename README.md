# sraruninfo-sql

Take a large SraRunInfo.csv and upload to SQL using AWS Lambda.

## Database

Data is hosted on the Serratus PostgreSQL cluster, which is publicly accessible via any PostgreSQL client (e.g. pgAdmin)

- Endpoint: `serratus-aurora-20210220.cluster-ro-ccz9y6yshbls.us-east-1.rds.amazonaws.com`
- Database: `summary`
- Username: `public_reader`
- Password: `serratus`

Table: `srarun`

## optimizations

```sql
create index srarun_run_index on srarun (run);
create index srarun_bio_sample_index on srarun (bio_sample);
```
