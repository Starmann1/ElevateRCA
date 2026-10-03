# ElevateRCA — REST API Specification

## Base URL: `/api/v1`

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/cases` | Create a new diagnostic case and trigger Iteration 1 RCA |
| `GET` | `/cases/{id}` | Inspect full case state, hypotheses, and iteration audit log |
| `POST` | `/cases/{id}/technician-feedback` | Ingest natural language technician feedback -> Iteration N+1 |
| `POST` | `/cases/{id}/diagnostic-test` | Record physical confirmation test outcome |
| `POST` | `/cases/{id}/post-repair-validation` | Submit post-repair test cycles to close or reopen case |
| `GET` | `/cases/{id}/report` | Export full 21-section Markdown audit report |
| `GET` | `/health` | Service healthcheck & safety boundary verification |
