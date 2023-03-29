// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import {Cont2} from "./Cont2.sol";

contract Cont3 {
    bool public freed = false;
	Cont2 public cont2;

	constructor( address _cont2){
		cont2 = Cont2(_cont2);
	}

    function free() public{
        require(cont2.freed() == true, "Cont2 is not freed");
        freed = true;
    }
}
