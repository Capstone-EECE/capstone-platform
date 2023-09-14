#!/bin/bash

readonly COLORS_CYAN='\e[36m'
readonly COLORS_NC='\e[0m' # No Color
readonly COLORS_GREEN='\e[32m'

# functions for the platform setup/teardown script
function step() {
    printf "\n${COLORS_CYAN}@ $1${COLORS_NC}\n"
}

function cleanup() {
    echo "Starting the cleanup..."
    docker stop capstone_db 2>/dev/null 1>&2 && docker rm capstone_db 2>/dev/null 1>&2
    printf "\n Done! \n"
}

function showHelp() {
    echo "USAGE: ${0} [ARGS]"
    echo ""
    echo " -h                                    Show this help message"
    echo " -d                                    Build Capstone container and run in background"
    echo " -f                                    Optionally copy the seed file to container and insert records"
    echo " -s                                    Clean up the Capstone container"
    echo ""
}

function checkContainerRunning() {
    res=$(docker ps -f name=capstone_db -q -a)
    if [[ -z "${res}" ]]; then
        return 0
    fi

    return 1
}

# start of the script

# Reset in case getopts has been used previously in the shell.
OPTIND=1
daemon=0
shutdown=0
seed_file=0

while getopts "h?dsf" opt; do
    case "$opt" in
    h|\?)
        showHelp
        exit 0
        ;;
    d)  daemon=1
        ;;
    s)  shutdown=1
        ;;
    f)  seed_file=1
        ;;
    esac
done

shift $((OPTIND-1))
[[ "${1:-}" = "--" ]] && shift


if [[ ${shutdown} -eq 1 ]]; then
    cleanup
    exit 0
fi

if [[ ${daemon} -eq 0 ]]; then
    showHelp
    exit 0
fi

step "Checking if Capstone database container is already running"
checkContainerRunning
if [[ $? -eq 1 ]]; then
    read -r -p "Container already running; do you wanna recreate it? [y/N] " res
    case "$res" in
        [yY][eE][sS]|[yY])
            step "Destroying previous environment"
            docker stop capstone_db && docker rm capstone_db
            ;;
        *)
            echo "Leaving it running. You can stop anytime using: $0 -s"
            echo
            exit 0
            ;;
    esac
fi

step "Creating Capstone DB server"
docker pull postgres:13.11
docker run --name=capstone_db -e POSTGRES_PASSWORD=postgres -p 8501:5432 -d postgres:13.11

step "Awaiting the DB server container to become available..."
until pg_isready -h localhost -p 8501 -q; do
    printf "."
    sleep 0.2;
done;
printf "\n Capstone DB server is up! \n"

step "Creating the capstone DB inside the server container..."
docker exec -i capstone_db psql -U postgres -h localhost -c "CREATE DATABASE capstone;"

step "Running the first migration"
# run all migrations and suppress the output
node migrate.js up 2>/dev/null 1>&2
printf "\n Done!"


if [[ ${seed_file} -eq 1 ]]; then
    step "Option -f specified, copying seed file to container and inserting records..."
    docker cp capstone_db.sql capstone_db:/capstone_db.sql
    docker exec -i capstone_db psql -U postgres -h localhost -d capstone -f capstone.sql
else
    step "No -f provided, so not seeding with dummy data..."
fi

printf "\n${COLORS_GREEN}Capstone DB & Schema Initialized\n"

# end of the script
