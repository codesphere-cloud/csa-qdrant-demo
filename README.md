# csa-qdrant-demo

This demo provides a simple Python/Flask application that injects and fetches data from/to a Qdrant database. 

The application is a modified version of the [Local Quickstart](https://qdrant.tech/documentation/quickstart/). 

The database needs to be provisioned through Codesphere Markplace by deploying the 
* Name: <choose any>
* Image: `qdrant/qdrant"
* Datacenter: <choose any>
* Public port: `6333`
* Run command: <none>
* No env var needed
* Smallest plan will do

When the docker image is up, paste the URL into the `.env` file as `QDRANDT_HOST=<DOCKER_URL>:443`. 
The port is needed since the Docker deployment will have the port 443 mapped to the specific public port and without a port set Qdrant would default to 6333. 

