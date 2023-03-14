// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract Cont1 {
	bool public freed = false;
	constructor(){
	}

	function free() public{
		freed = true;
	}
}
