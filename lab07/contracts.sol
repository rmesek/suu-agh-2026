// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.8.2 <0.9.0;

// smart contract declaration

contract SuuPlayground {

	// this will get initialize to 0 
    uint256 favoriteNumber;
	bool  favoriteBool = true;
	address favoriteAddress; 

    // This is a comment!
    struct People {
        uint256 favoriteNumber;
        string name;
    }

    People[] public people;
	// dictinary to values
    mapping(string => uint256) public nameToFavoriteNumber;

    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    // does not change the state of transactions (e.g. compute)
    function retrieve() public view returns (uint256){
        return favoriteNumber;
    }

	// there are to options to store in memory (data will be stored in function execution) 
	// storage will persist after function is executed
    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_favoriteNumber, _name));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }

    function fundMe() payable public returns (uint256){
        return  msg.value;
        //  require( condition, "message);          
        // for transfering msg.sender.transfer()
    }

    function overflow() public pure returns (uint8) {
        uint8 big = 0;
        unchecked { 
            big = 255 + uint8(10);
        }
        return big;
    }
}
