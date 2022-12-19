# Test
This is the test branch for our project. We test the user interaction with the website via Python unittest,
 and smart contract test using mocha.
## Python unittest
### Setup
Repeat web3 setup to create a new testnet for testing, then run `tests.py` for testing.

### Testing Coverage
- Exhaustively Testing the basic funcionalities:
  - Register, Login, Logout
  - Add a Review, Add a Product
  - Verify a Review, Edit a Review
- Testing the security:
  - Fake Reviews (Reviews of a product that has not been purchased by the user)

## Contract test
We use Truffle, Mocha to test the contract.
First you need to install Truffle using `npm install truffle`. You may also need to change the development network in `truffle-config.js`. And run
```shell
truffle migrate
truffle test ./test/contract_test.js
```
