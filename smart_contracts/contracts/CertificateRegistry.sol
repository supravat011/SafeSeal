// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

contract CertificateRegistry {
    struct Certificate {
        string studentId;
        string data; // JSON string or metadata
        address issuer;
        uint256 timestamp;
        bool isValid;
    }

    mapping(bytes32 => Certificate) public certificates;
    mapping(address => bool) public authorizedIssuers;
    address public owner;

    event CertificateIssued(bytes32 indexed hash, string studentId, address indexed issuer);
    event CertificateRevoked(bytes32 indexed hash, address indexed issuer);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    modifier onlyIssuer() {
        require(authorizedIssuers[msg.sender], "Not authorized issuer");
        _;
    }

    constructor() {
        owner = msg.sender;
        authorizedIssuers[msg.sender] = true; // Owner is also an issuer for simplicity
    }

    function addIssuer(address _issuer) external onlyOwner {
        authorizedIssuers[_issuer] = true;
    }

    function removeIssuer(address _issuer) external onlyOwner {
        authorizedIssuers[_issuer] = false;
    }

    function issueCertificate(bytes32 _hash, string memory _studentId, string memory _data) external onlyIssuer {
        require(certificates[_hash].timestamp == 0, "Certificate already exists");
        
        certificates[_hash] = Certificate({
            studentId: _studentId,
            data: _data,
            issuer: msg.sender,
            timestamp: block.timestamp,
            isValid: true
        });

        emit CertificateIssued(_hash, _studentId, msg.sender);
    }

    function verifyCertificate(bytes32 _hash) external view returns (bool, string memory, string memory, uint256, address) {
        Certificate memory cert = certificates[_hash];
        return (cert.isValid, cert.studentId, cert.data, cert.timestamp, cert.issuer);
    }

    function revokeCertificate(bytes32 _hash) external onlyIssuer {
        require(certificates[_hash].timestamp != 0, "Certificate does not exist");
        // Ideally only the issuer or owner can revoke. 
        // For now, any authorized issuer can revoke (or restrict to original issuer).
        require(certificates[_hash].issuer == msg.sender || msg.sender == owner, "Not authorized to revoke");
        
        certificates[_hash].isValid = false;
        emit CertificateRevoked(_hash, msg.sender);
    }
}
