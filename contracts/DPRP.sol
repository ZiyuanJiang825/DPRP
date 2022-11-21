pragma solidity ^0.8.13;

contract DPRP {
    address payable public owner;

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

    function addReview(string memory message) external{
        emit Log(msg.sender, message);
    }
    
}