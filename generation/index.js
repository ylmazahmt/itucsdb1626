const faker = require('faker');

function generate() {

  return {
    username: faker.name.firstName() + ' ' + faker.name.lastName(),
    inserted_at: new Date(),
    post_title: faker.lorem.sentence(),
    post_body: faker.lorem.paragraph(),
    cost_of_meal: faker.finance.currencySymbol() + ' ' + faker.finance.amount(),
    place_name: faker.company.companyName()
  }
};

for (var i = 0; i < 100; ++i) {
  console.log(generate());
}
