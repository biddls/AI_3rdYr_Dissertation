/* Autogenerated file. Do not edit manually. */
/* tslint:disable */
/* eslint-disable */

import { ethers } from "ethers";
import {
  FactoryOptions,
  HardhatEthersHelpers as HardhatEthersHelpersBase,
} from "@nomiclabs/hardhat-ethers/types";

import * as Contracts from ".";

declare module "hardhat/types/runtime" {
  interface HardhatEthersHelpers extends HardhatEthersHelpersBase {
    getContractFactory(
      name: "Cont1",
      signerOrOptions?: ethers.Signer | FactoryOptions
    ): Promise<Contracts.Cont1__factory>;
    getContractFactory(
      name: "Cont2",
      signerOrOptions?: ethers.Signer | FactoryOptions
    ): Promise<Contracts.Cont2__factory>;
    getContractFactory(
      name: "Cont3",
      signerOrOptions?: ethers.Signer | FactoryOptions
    ): Promise<Contracts.Cont3__factory>;

    getContractAt(
      name: "Cont1",
      address: string,
      signer?: ethers.Signer
    ): Promise<Contracts.Cont1>;
    getContractAt(
      name: "Cont2",
      address: string,
      signer?: ethers.Signer
    ): Promise<Contracts.Cont2>;
    getContractAt(
      name: "Cont3",
      address: string,
      signer?: ethers.Signer
    ): Promise<Contracts.Cont3>;

    // default types
    getContractFactory(
      name: string,
      signerOrOptions?: ethers.Signer | FactoryOptions
    ): Promise<ethers.ContractFactory>;
    getContractFactory(
      abi: any[],
      bytecode: ethers.utils.BytesLike,
      signer?: ethers.Signer
    ): Promise<ethers.ContractFactory>;
    getContractAt(
      nameOrAbi: string | any[],
      address: string,
      signer?: ethers.Signer
    ): Promise<ethers.Contract>;
  }
}
