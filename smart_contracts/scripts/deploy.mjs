import hre from "hardhat";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function main() {
    const CertificateRegistry = await hre.ethers.getContractFactory("CertificateRegistry");
    const registry = await CertificateRegistry.deploy();

    await registry.waitForDeployment();

    const address = await registry.getAddress();
    console.log(`CertificateRegistry deployed to ${address}`);

    // Save the address to a file for the frontend
    const deploymentInfo = {
        address: address,
        chainId: hre.network.config.chainId || 1337
    };

    const outputPath = path.join(__dirname, "../../client/src/contract-address.json");
    fs.writeFileSync(
        outputPath,
        JSON.stringify(deploymentInfo, null, 2)
    );
    console.log("Contract address saved to client/src/contract-address.json");
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
