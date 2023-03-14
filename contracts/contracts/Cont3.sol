// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import Cont2 from "./Cont2.sol";

contract Cont3 {
    bool public freed = false;
	constructor() Cont2{

	}

    function free() public{
        require(Cont2.freed() == true, "Cont2 is not freed");
        freed = true;
    }
}
