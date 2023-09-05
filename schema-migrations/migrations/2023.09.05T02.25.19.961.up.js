// 2023.09.05T02.25.19.961 up

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
	            name text
            );
        `
  ]
}
