// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import {Cont1} from "./Cont1.sol";

contract Cont2 {
	bool public freed = false;
	Cont1 public cont1;

	constructor( address _cont1) {
		cont1 = Cont1(_cont1);
	}

	function free() public{
		require(cont1.freed() == true, "Cont1 is not freed");
		freed = true;
	}
}
