docker build -t myimage .
docker tag myimage [REDACTED]/arbeitsagentur2mongo
docker push [REDACTED]/arbeitsagentur2mongo
ssh admin@pertschy.cloud 'sudo /usr/local/bin/docker pull registry.pertschy.cloud/arbeitsagentur2mongo'
#Cronjob:
#docker run --rm REDACTED]/indeed2mongo



