# Exercise 2 — OpenBao PKI and Dynamic PostgreSQL Credentials

## 1. Objective

Design a secrets-management architecture using OpenBao to issue short-lived TLS certificates and generate temporary PostgreSQL credentials. The design should reduce long-lived secrets, enforce least privilege, support credential rotation and revocation, and provide auditable access.

## 2. Architecture

```text
Developer / CI Pipeline
        |
        | Authenticated identity
        v
  OpenBao API
        |
        +---------------------------+
        |                           |
        v                           v
   PKI Secrets Engine       Database Secrets Engine
        |                           |
        v                           v
 Short-lived TLS certs       PostgreSQL database
        |                           |
        v                           v
  Application workload      Temporary DB username
        |                    and generated password
        +-------------+-------------+
                      |
                      v
             Application services

OpenBao audit device ---> Protected audit destination
OpenBao metrics/logs ---> Monitoring and alerting
```

## 3. PKI design

- Configure an offline or separately protected root CA and use an intermediate CA for routine certificate issuance.
- Enable the OpenBao PKI secrets engine and configure an intermediate CA.
- Define certificate roles that restrict allowed DNS names, key types, key usages, and maximum TTL.
- Issue short-lived leaf certificates to authenticated workloads.
- Set certificate lifetimes according to workload needs; an initial lab target is 1 hour.
- Automate renewal before expiry and safely reload certificates in consuming applications.
- Restrict issuance and signing permissions through OpenBao policies.
- Protect CA private keys and plan for CA rotation, certificate revocation, and incident response.

A short-lived certificate is not automatically renewed or revoked merely because its TTL is short. Renewal automation, expiry handling, and revocation procedures must be designed and tested.

## 4. Dynamic PostgreSQL credentials

- Enable the OpenBao database secrets engine.
- Configure a PostgreSQL connection using a dedicated database administration identity with only the permissions needed to create and revoke temporary roles.
- Define a least-privilege database role for the application.
- Set a short default lease and maximum lease duration.
- Have an authenticated workload request credentials when needed.
- Renew a lease when supported and appropriate; otherwise request replacement credentials before expiry.
- Revoke leases when workloads terminate or access must be withdrawn.
- Test what happens when credentials expire while database connections are active.

Dynamic credentials should not use a PostgreSQL superuser as the routine application identity. The provisioning account itself must also be protected and restricted.

## 5. Authentication and authorization

- Prefer workload identity or a suitable authenticated machine identity over static tokens embedded in source code.
- Use separate OpenBao policies for PKI issuance, certificate administration, database credential requests, and system administration.
- Apply least privilege to each policy and role.
- Protect administrative access with strong authentication and restricted network access.
- Never store real tokens, passwords, private keys, or connection strings in Git.

## 6. Audit and monitoring

- Enable an OpenBao audit device and send audit records to a protected destination.
- Restrict access to audit records and monitor for repeated authentication failures, unusual issuance volume, privilege changes, and unexpected secret access.
- Protect audit integrity and availability.
- Monitor certificate expiry, lease issuance, lease renewal failures, revocation failures, and database authentication errors.
- Avoid logging secret values or private key material.

## 7. Failure scenarios

| Scenario | Expected response |
|---|---|
| OpenBao unavailable | Fail safely; do not silently fall back to hard-coded credentials |
| Certificate near expiry | Renew before expiry and alert on failure |
| Database lease expires | Reacquire credentials and reconnect safely where necessary |
| Workload is compromised | Revoke relevant leases, restrict identity, investigate audit records |
| CA key is compromised | Follow CA compromise and replacement procedures |
| Audit destination unavailable | Alert and follow the defined audit continuity policy |

Applications must define their own availability and recovery behavior. Caching credentials indefinitely defeats the purpose of short-lived leases.

## 8. Lab validation plan

1. Run OpenBao in an isolated local environment.
2. Enable a lab PKI engine and issue a short-lived certificate.
3. Verify the certificate subject, issuer, SANs, and expiration.
4. Configure a disposable PostgreSQL database and a restricted provisioning identity.
5. Request dynamic database credentials and test the granted database permissions.
6. Revoke the credential lease and verify that the generated database role is revoked.
7. Test expiry, renewal, authentication failures, and audit records.
8. Save sanitized configuration, command output, and test results under `evidence/exercise-2/`.

## 9. Production considerations and limitations

A local development setup does not establish production readiness. Production deployment requires a high-availability design, protected and backed-up storage, TLS, authenticated service identities, controlled CA key custody, recovery testing, monitoring, audit retention, and tested upgrade and rotation procedures.

Root and intermediate CA handling must be designed carefully. A lab-generated root key must never be represented as a production trust anchor.
