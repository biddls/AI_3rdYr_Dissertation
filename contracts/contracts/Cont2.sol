// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import Cont1 from "./Cont1.sol";

contract Cont2 {
	bool public freed = false;
	constructor() Cont1{
	}

	function free() public{
		require(Cont1.freed() == true, "Cont1 is not freed");
		freed = true;
	}
}
