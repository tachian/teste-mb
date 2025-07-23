# teste-mb

## Desafio Ethereum MB

## RoadMap to UP:+ Install Sqlite in your local machine or use a docker image
    + In Sqlite execute:
        + `Create databases "teste-mb";`
        + `Create databases "teste-mb_test";`

 + Dependencies
   `sudo apt install libcurl4-openssl-dev libssl-dev`

 + Verify if SSH is configured:
    + `your local machine`
    + `your BitBucket count`

 + Clone repository
    + `git clone git@github.com:tachian/teste-mb.git`

 + Create and activate "virtualenv"

 + Install "requirements":
    + `(pip install -r src/requirements-dev.txt)`

 + Set environment variable:
    + DEPLOY_ENV=<environment where App will run>
    + LOGS_LEVEL=<Level of logs - Used on production environment>+ DATABASE_URI=Sqlite://<user>:<password>@localhost:5432/<database>
    + DATABASE_URI_TEST=Sqlite://<user>:<password>@localhost:5432/<database>_test+ Execute (inside src dir)
    + `flask db migrate` To generate database revision files
    + `flask db upgrade` To apply revision files

 + Start server (inside src dir)
    + `flask run`

 + HEALTH endpoints
    + /api/healthz: If API is working, must show {"service": "teste-mb API HealthCheck", "version": "9.9.9"}
    + /api/docs/swagger: IF API is working, must show SWAGGER page

## Commands
 + Reset Database (inside src dir)
	+ `flask drop-create-tables`

## Generate the Docker image

Inside src execute `docker build . -t teste-mb:<tag>`

A merge to dev or qa branchs will also build an image automatically on Jenkins and push it to AWS ECR

### Managing the image tag

The tag must be changed manually on .env.yaml file before opening a PR to dev or qa branches.

The version should be managed using the [SEMVER](https://semver.org/) scheme
