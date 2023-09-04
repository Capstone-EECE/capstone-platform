// 2023.08.30T23.42.50.140 test

module.exports = {
    DOWN: [
        `
            DROP SCHEMA capstone CASCADE;
        `
    ],
    UP: [
        `
            CREATE SCHEMA capstone;

            CREATE TABLE capstone.test (
	            name text NOT NULL,
	            text NOT NULL,
            );
        `
  ]
}
