# SBOM Generation and Signing

## Artifact details

- Container image: `rlogics-sample:1.0.0`
- SBOM formats: CycloneDX JSON and SPDX JSON
- Generation tool: Syft 1.54.1
- Packages cataloged: 95
- Executables cataloged: 752
- File locations cataloged: 2,652

## Signing and verification

- Signing tool: Cosign 3.1.3
- Signed artifact: `image-sbom-cyclonedx.json`
- Signature bundle: `image-sbom.sigstore.json`
- Signing method: Local key-based signing
- Transparency log: Disabled for this local exercise
- Verification command: `cosign verify-blob`
- Verification result: Verified OK

## Limitations

- The signing private key must never be committed to Git.
- Local key-based signing does not independently establish the identity of the key owner.
- Skipping transparency-log verification reduces the assurance provided by the verification process.
- The SBOM describes the cataloged artifact; it does not prove that every component is safe or free of vulnerabilities.
- This exercise demonstrates a local workflow, not a complete production software-supply-chain trust system.
