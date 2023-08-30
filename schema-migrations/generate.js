const fs = require("fs");

const NEW_FILE_CONTENTS = `
module.exports = {
    DOWN: [],
    UP: []
}
`;

/**
 * Get migration name from arguments
 *
 * @returns name of migration from command arguments
 */
function getMigrationNameParameter() {
    if (!(process.argv.length > 2)) {
        return null;
    }

    let args = process.argv.slice(2);
    let [name] = args;

    return name;
}

function getTimestampString() {
    let ts = new Date().toISOString();
    ts = ts.replace(/[-,:]/gi, ".");
    ts = ts.replace("Z", "");
    return ts;
}

function generateMigration() {
    let filename = getMigrationNameParameter();

    if (!filename || !(filename.length > 0)) {
        console.log("Usage:\nnode generate.ts {migration-name}\n\nExample: node generate.ts client-history-table");
        process.exit();
    }

    let dt = getTimestampString();
    console.log(dt);

    fs.writeFileSync(`./migrations/${dt}.${filename}.js`, `// ${dt} ${filename}\n${NEW_FILE_CONTENTS}`);
}

generateMigration();
