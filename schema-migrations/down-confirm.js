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

async function run_down() {
    transactions = await umzug.executed();
    console.log(transactions.at(-1));

    await continue_prompt("Roll back this migration? y/[n]");
    console.log("running migrations");
    transactions = await umzug.down();
}

run_down();
