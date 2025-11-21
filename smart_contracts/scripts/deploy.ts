import { ethers } from "hardhat";

async function main() {
    const CertificateRegistry = await ethers.getContractFactory("CertificateRegistry");
    const registry = await CertificateRegistry.deploy();

    await registry.waitForDeployment();

    const address = await registry.getAddress();
    console.log(`CertificateRegistry deployed to ${address}`);

    // Update client config
    const fs = require("fs");
    const path = require("path");
    const configPath = path.join(__dirname, "../../client/src/contract-config.json");

    const config = {
        address: address,
        chainId: 1337, // Hardhat default chainId
        abi: JSON.parse(registry.interface.formatJson())
    };

    fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
    console.log(`Updated client config at ${configPath}`);
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
