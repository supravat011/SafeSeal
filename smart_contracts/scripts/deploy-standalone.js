const { ethers } = require("ethers");
const fs = require("fs");
const path = require("path");

async function main() {
    // Connect to the local Hardhat node
    const provider = new ethers.JsonRpcProvider("http://127.0.0.1:8545");

    // Use one of the Hardhat default accounts
    const privateKey = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80";
    const wallet = new ethers.Wallet(privateKey, provider);

    console.log("Deploying from:", wallet.address);

    // Load the contract artifact
    const artifactPath = path.join(__dirname, "../artifacts/contracts/CertificateRegistry.sol/CertificateRegistry.json");
    const artifact = JSON.parse(fs.readFileSync(artifactPath, "utf8"));

    // Create contract factory and deploy
    const factory = new ethers.ContractFactory(artifact.abi, artifact.bytecode, wallet);
    const contract = await factory.deploy();

    await contract.waitForDeployment();

    const address = await contract.getAddress();
    console.log(`CertificateRegistry deployed to: ${address}`);

    // Save deployment info
    const deploymentInfo = {
        address: address,
        chainId: 1337,
        abi: artifact.abi
    };

    const outputPath = path.join(__dirname, "../../client/src/contract-config.json");
    fs.writeFileSync(outputPath, JSON.stringify(deploymentInfo, null, 2));
    console.log("Contract config saved to client/src/contract-config.json");
}

main().catch((error) => {
    console.error(error);
    process.exit(1);
});
