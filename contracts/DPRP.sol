pragma solidity ^0.8.13;

contract DPRP {
    address payable public owner;
    mapping(address => mapping(uint => bool)) public purchase;
    constructor() {
        owner = payable(msg.sender);
    }

    receive() external payable {}
    event Log(address indexed sender, string message);
    function getBalance() external view returns (uint) {
        return address(this).balance;
    }

    function withdraw(address payable _to, uint _amount) external {
        require(msg.sender == owner, "caller is not owner");
        payable(_to).transfer(_amount);
    }

    function addPurchase(address buyer, uint product_id) external {
        require(msg.sender == owner, "caller is not owner");
        purchase[buyer][product_id] = true;
    }
    function addReview(address user_address, uint product_id, string memory message) external{
        require(purchase[user_address][product_id] == true, "user has not purchased this product!");
        emit Log(msg.sender, message);
    }

}
