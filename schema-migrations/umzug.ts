import { Umzug, SequelizeStorage, UmzugOptions } from "umzug";
import { Sequelize } from "sequelize";

const sequelize = new Sequelize({
    dialect: "postgres",
    ssl: true,
    pool: {
        max: 1,
        min: 0,
        acquire: 5000,
        idle: 200,
        evict: 200,
    },
});

let secret: any = null;

(sequelize as any).beforeConnect(async (options) => {
    try {
        if (false) {
            // Target DB hosted on AWS
            // Use Secrets
        } else {
            // Local DB
            (options as any).host = "localhost";
            (options as any).database = "calibration";
            (options as any).username = "postgres";
            (options as any).password = "postgres";
            (options as any).port = "8501";
        }
        console.log(
            `Connected to DB via provided credentials: ${options.username}@${options.host}`
        );
    } catch (err) {
        console.error(
            "Error with credentials. Check if all local credentials or secret path are defined.",
            err
        );
    }
});



const umzugOptions: UmzugOptions<Sequelize> = {
    migrations: {
      glob: ["migrations/*.js", { cwd: __dirname }],
      resolve: ({ name, path, context }) => {
        if (path) {
          const migration = require(path);

          return {
            name: name,
            up: async () => {
              await context.transaction(async (t: any) => {
                for (let i = 0; i < migration.UP.length; i++) {
                  const statement = migration.UP[i];
                  await context.query(statement, { transaction: t });
                }
              });
            },
            down: async () => {
              await context.transaction(async (t: any) => {
                for (let i = 0; i < migration.DOWN.length; i++) {
                  const statement = migration.DOWN[i];
                  await context.query(statement, { transaction: t });
                }
              });
            },
          } as any;
        }
      },
    },
    context: sequelize,
    storage: new SequelizeStorage({ sequelize }),
    logger: console,
    create: {
      folder: "migrations",
    },
  };

  export const migrator = new Umzug(umzugOptions);
  export type Migration = typeof migrator._types.migration;
