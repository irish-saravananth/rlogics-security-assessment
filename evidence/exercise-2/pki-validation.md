# Exercise 2 — OpenBao PKI Validation

## Environment
- OpenBao: 2.7.1
- Storage: Integrated Storage (Raft)
- Deployment: Single-node local lab
- API: HTTP, published on host loopback only
- CA: RLogics Assessment Lab Root CA (lab-only)

## Certificate role
- Role: assessment-local
- Allowed DNS domain: localhost
- Bare domain: enabled
- Localhost: enabled
- IP SANs: disabled
- Wildcard certificates: disabled
- Key type: EC
- Key size: 256 bits
- Requested certificate TTL: 1 hour
- Maximum role TTL: 1 hour

## Validation results
- Certificate issuance: PASS
- Subject: CN=localhost
- Issuer: CN=RLogics Assessment Lab Root CA
- Subject Alternative Name: DNS:localhost
- Expiry check for the next 3500 seconds: PASS
- Private-key integrity check: PASS

## Limitations
- This is a single-node lab, not a highly available deployment.
- The lab API uses HTTP; not recommended to this configuration for production.
- The root CA is for this exercise only.
- Production requires TLS, protected CA key custody, renewal automation,
  revocation procedures, monitoring, and tested recovery.
- The PKI issuance response and private key are stored outside Git.
