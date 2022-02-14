init:
	- docker-compose up -d --build
	- docker cp ./skel/user_profile.sql slack-query-db_db_1:/
	- docker cp ./skel/country.sql slack-query-db_db_1:/
	- docker cp ./skel/setup_auth_role.sql slack-query-db_db_1:/
	- sleep 3
	- docker exec -it slack-query-db_db_1 bash -c "export PGPASSWORD='nCCGkzg9qs3hPsy7'; psql -U admin -d demodb -q < user_profile.sql" 
	- docker exec -it slack-query-db_db_1 bash -c "export PGPASSWORD='nCCGkzg9qs3hPsy7'; psql -U admin -d demodb -q < country.sql" 
	- docker exec -it slack-query-db_db_1 bash -c "export PGPASSWORD='nCCGkzg9qs3hPsy7'; psql -U admin -d demodb -q < setup_auth_role.sql" 

start:
	- docker-compose up -d

stop:
	- docker-compose stop

destroy:
	- docker-compose down -v
