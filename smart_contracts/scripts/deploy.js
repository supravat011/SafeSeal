const hre = require("hardhat");

async function main() {
    const CertificateRegistry = await hre.ethers.getContractFactory("CertificateRegistry");
    const registry = await CertificateRegistry.deploy();

    await registry.waitForDeployment();

    const address = await registry.getAddress();
    console.log(`CertificateRegistry deployed to ${address}`);

    // Save the address to a file for the frontend
    const fs = require("fs");
    const deploymentInfo = {
        address: address,
        chainId: hre.network.config.chainId || 1337
    };

    fs.writeFileSync(
        "../client/src/contract-address.json",
        JSON.stringify(deploymentInfo, null, 2)
    );
    console.log("Contract address saved to client/src/contract-address.json");
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
