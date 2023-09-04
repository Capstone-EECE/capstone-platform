require("ts-node/register/transpile-only");

umzug = require("./umzug").migrator;
const stdin = process.openStdin();

async function continue_prompt(prompt) {
    console.log(prompt);

    return new Promise((resolve) => {
        stdin.on("data", function (chunk) {
            if (chunk.toString()[0] != "y") {
                console.log("good choice");
                process.exit(1);
            } else {
                resolve();
            }
        });
    });
}

async function run_up() {
    transactions = await umzug.pending();
    console.log(transactions);

    await continue_prompt("Run all migrations above? y/[n]");
    console.log("running migrations");
    transactions = await umzug.up();
}

run_up();
