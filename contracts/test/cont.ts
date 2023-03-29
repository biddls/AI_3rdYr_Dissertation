import { loadFixture } from "@nomicfoundation/hardhat-network-helpers";
import { expect } from "chai";
import { ethers } from "hardhat";

describe("Lock", function () {
    async function deployConts() {

        const Cont1 = await ethers.getContractFactory("Cont1");
        const Cont2 = await ethers.getContractFactory("Cont2");
        const Cont3 = await ethers.getContractFactory("Cont3");
        const cont1 = await Cont1.deploy();
        const cont2 = await Cont2.deploy(cont1.address);
        const cont3 = await Cont3.deploy(cont2.address);

        return { cont1, cont2, cont3};
    }

    describe("Deployment", function () {
        it("It should unlock", async function () {
            const { cont1, cont2, cont3 } = await loadFixture(deployConts);

            await cont1.free();
            await cont2.free();
            await cont3.free();

            expect(await cont3.freed()).to.equal(true);
        });
        it("It shouldn't be unlocked", async function () {
            const { cont1, cont2, cont3 } = await loadFixture(deployConts);
            expect(await cont3.freed()).to.equal(false);

            await expect(cont3.free()).to.revertedWith("Cont2 is not freed");
            await expect(cont2.free()).to.revertedWith("Cont1 is not freed");
        });

    });
});
