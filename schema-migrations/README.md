Performs database changes from CI/CD by making use of Sequlize CLI.


## Requirements
- NodeJS 15.x
- Docker
- postgresql-client

## Setup
```
npm install
```

### Running locally
You need to have docker cli installed and postgresql.
Next, make the `setup_local_db.sh` script executable,
```
.chmod +x setup_local_db.sh
```
and then:
```
./setup_local_db.sh -d
```
to run the DB server container in background and:
```
./setup_local_db.sh -s
```
to shutdown the server and clean up the container. `-h` flag will display these
usage instructions in your terminal.

## Generate Migration Scripts
```
node generate.js [name]
```

### Example
```
node generate.js client_history
```

## Run up migrations
```
node migrate.js up
```


## Run down migration
```
node migrate.js down
```


### View Pending Migrations
```
node migrate.js pending
```
