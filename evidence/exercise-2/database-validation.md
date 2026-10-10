# Exercise 2 — Dynamic Database Credentials

## Environment
- Secrets manager: OpenBao 2.7.1
- Database: PostgreSQL 16
- Deployment: Isolated local Docker network
- Database engine: OpenBao database secrets engine

## Configuration
- Connection: `assessment-postgres`
- Dynamic role: `assessment-app`
- Default lease: 15 minutes
- Maximum lease: 1 hour
- Granted database role: `app_readwrite`
- Database privileges: CONNECT, schema USAGE, table SELECT/INSERT,
  and sequence USAGE/SELECT as configured for the demo table

## Validation results
- Database connection configuration: PASS
- Dynamic credential issuance: PASS
- Insert and read using generated credentials: PASS
- Lease revocation: PASS
- Authentication after revocation: PASS

## Security notes
- PostgreSQL administrator credentials and generated credentials are stored
  outside Git in files with restrictive permissions.
- The database is not published on a host port.
- The lab connection uses `sslmode=disable` on an isolated Docker network.
  Production deployments must use appropriate TLS and credential protections.
- This is a local single-node lab, not a production high-availability setup.
