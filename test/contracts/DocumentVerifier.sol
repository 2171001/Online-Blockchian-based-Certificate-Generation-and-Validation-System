// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract DocumentVerifier {
    mapping(bytes32 => bool) private _documentHashes;

    event DocumentAdded(bytes32 indexed hash);
    event DocumentVerified(bytes32 indexed hash, bool isValid);

    function addDocumentHash(bytes32 hash) external {
        require(!_documentHashes[hash], "Document hash already exists");
        _documentHashes[hash] = true;
        emit DocumentAdded(hash);
    }

    function verifyDocumentHash(bytes32 hash) external view returns (bool) {
        return _documentHashes[hash];
    }

    function getStoredHash(bytes32 hash) external view returns (bool) {
        return _documentHashes[hash];
    }
}
