echo "Backing up portfolio database from 192.168.0.129"
pg_dump portfolio > ./dump/ats_dump-$(date -I) -h 192.168.0.129 -p 5432 -U postgres
