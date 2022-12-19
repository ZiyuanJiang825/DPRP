const Web3 = require('web3');
const web3 = new Web3(new Web3(Web3.givenProvider || "ws://localhost:7545"));
const chai = require('chai');
const assert = chai.assert;
const DPRP = artifacts.require('DPRP');

contract('DPRP', (accounts) => {
  let dprp;

  before(async () => {
    dprp = await DPRP.deployed();
    dprp.send(web3.utils.toWei("10000", "wei")).then(function(result) {
      // Same result object as above.
    });
  });

  it('should set the correct owner in the constructor', async () => {
    const owner = await dprp.owner();
    assert.equal(owner, accounts[0]);
  });

  it('should allow the owner to add a purchase', async () => {
    const productId = 1;
    await dprp.addPurchase(accounts[1], productId, { from: accounts[0] });
    const hasPurchased = await dprp.purchase(accounts[1], productId);
    assert.isTrue(hasPurchased);
  });

  it('should not allow a non-owner to add a purchase', async () => {
    const productId = 2;
    try {
      await dprp.addPurchase(accounts[2], productId, { from: accounts[1] });
      assert.fail();
    } catch (error) {
      assert.include(error.message, 'caller is not owner');
    }
  });

  it('should allow a user to add a review if they have purchased the product', async () => {
    const productId = 1;
    const message = 'Great product!';
    await dprp.addPurchase(accounts[2], productId, { from: accounts[0] });
    const result = await dprp.addReview(accounts[2], productId, message, { from: accounts[2] });
    assert.equal(result.logs[0].args.sender, accounts[2]);
    assert.equal(result.logs[0].args.message, message);
  });

  it('should not allow a user to add a review if they have not purchased the product', async () => {
    const productId = 2;
    const message = 'Not so great...';
    try {
      await dprp.addReview(accounts[2], productId, message, { from: accounts[2] });
      assert.fail();
    } catch (error) {
      assert.include(error.message, 'user has not purchased this product!');
    }
  });

  it('should return the correct contract balance', async () => {
    const balance = await dprp.getBalance();
    assert.isAbove(balance.toNumber(), 0);
  });

  it('should allow the owner to withdraw funds', async () => {
    const balanceBefore = await web3.eth.getBalance(accounts[0]);
    const contractBalance = await dprp.getBalance();
    await dprp.withdraw(accounts[0], contractBalance / 2, { from: accounts[0] });
    const balanceAfter = await web3.eth.getBalance(accounts[0]);
    assert.isAbove(parseInt(balanceBefore.toString()), parseInt(balanceAfter.toString()));
  });

  it('should not allow a non-owner to withdraw funds', async () => {
    try {
      await dprp.withdraw(accounts[1], 10, { from: accounts[1] });
      assert.fail();
    } catch (error) {
      assert.include(error.message, 'caller is not owner');
    }
  });

});
