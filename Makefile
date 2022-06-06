init:
	- docker-compose up -d --build
	- docker cp ./skel/user_profile.sql entity-slackui-db-1:/
	- docker cp ./skel/country.sql entity-slackui-db-1:/
	- docker cp ./skel/setup_auth_role.sql entity-slackui-db-1:/
	- sleep 3
	- docker exec -it entity-slackui-db-1 bash -c "export PGPASSWORD='nCCGkzg9qs3hPsy7'; psql -U admin -d demodb -q < user_profile.sql" 
	- docker exec -it entity-slackui-db-1 bash -c "export PGPASSWORD='nCCGkzg9qs3hPsy7'; psql -U admin -d demodb -q < country.sql" 
	- docker exec -it entity-slackui-db-1 bash -c "export PGPASSWORD='nCCGkzg9qs3hPsy7'; psql -U admin -d demodb -q < setup_auth_role.sql" 

start:
	- docker-compose up -d

stop:
	- docker-compose stop

destroy:
	- docker-compose down -v
