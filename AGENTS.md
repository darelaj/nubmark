# AGENTS.md — Nubmark

Instructions for AI coding agents and human contributors working on the **Nubmark** Android app and **Flask backend**.

> **Read `docs/PLAN.md` first** for release milestones, schema, flows, security and roadmap. Read **`docs/DESIGN.md` before UI changes**. This file governs implementation and verification. Do not assume files, modules, services, migrations, or tests exist until inspected.

---

## 1. Project Rules and Priorities

- **Product:** Nubmark — *Every build leaves a mark..*
- **Android application ID:** `id.my.chromazone.nubmark`.
- **Approved design:** clean **light/white UI** with subtle blue accents, Material 3, image-first kit cards. **Five tabs:** Home, Collection, Wishlist, Builds, Profile. Do not substitute the earlier dark hangar mockup or four-tab layout.
- **Milestone A:** Local MVP; Kotlin + Compose + Room. No mandatory account, no internet dependency.
- **Milestone B:** Optional cloud account/sync; Python + **Flask** + PostgreSQL. Flask is planned, but **do not add unused networking into Phase A**.
- **Local source of truth:** Room even when sync is enabled. API data is incorporated through repositories, never directly displayed from Retrofit.
- **User-facing language:** English default; Indonesian resources where feasible.
- **Scope control:** Work only on the active phase and the user's specific requested changes. No speculative features or unrelated refactors.

**Authority:** `docs/PLAN.md` defines behavior/data/release scope; `docs/DESIGN.md` defines approved visual appearance and screens; `AGENTS.md` defines coding/workflow rules. Surface any real contradiction instead of quietly picking a different design.

---

## 2. Project Layout

Preferred layout **for a new repository**:

```text
nubmark/
├── android/                    # Android Studio Gradle project
│   ├── app/
│   └── gradle/libs.versions.toml
├── backend/                    # Flask service, migrations, tests, Dockerfile
├── docs/                       # docs/openapi.yaml and architecture notes
├── DESIGN.md
├── PLAN.md
├── AGENTS.md
└── README.md
```

**Do not reorganize a repository that already exists merely to match this example.** Inspect its current structure and keep commands/paths accurate. Android Kotlin package path starts at `id/my/chromazone/nubmark`.

Suggested Android packages (single Gradle module initially):

```text
core/{design,navigation,ui,util}
data/{local,remote,repository,storage,sync}
domain/{model,usecase}
feature/{home,collection,kitdetail,kitform,wishlist,builds,profile}
timer/
di/
```

Suggested Flask packages:

```text
backend/app/{api,auth,models,schemas,services,storage,extensions}
backend/migrations/
backend/tests/
backend/wsgi.py
```

Create `data/remote` and `data/sync` only when starting the cloud milestone, or when explicitly authorized.

---

## 3. Technology Choices

### Android

- Kotlin, Coroutines, Flow; Jetpack Compose and Material 3.
- MVVM + UDF; Navigation Compose with type-safe routes.
- Hilt, Room/KSP, DataStore; Coil; Android Photo Picker; CameraX only if needed.
- JUnit, Turbine, Room instrumented tests, Compose UI tests.
- Cloud Beta: Retrofit/OkHttp, kotlinx.serialization, WorkManager, Android Keystore-backed secure token storage.
- Central Gradle version catalog. Add a library only for a documented feature, not by default.

### Flask backend (Cloud Beta)

- Python 3.12+ supported runtime, Flask application factory, modular Blueprints.
- SQLAlchemy 2.x, PostgreSQL, Alembic/Flask-Migrate migrations.
- Explicit request/response schemas (Marshmallow **or** Pydantic, choose one).
- pytest + Flask test client; PostgreSQL integration tests; Ruff.
- OpenAPI contract, versioned API prefix `/api/v1`.
- Docker + Gunicorn in production behind HTTPS reverse proxy.
- Managed/private object storage for uploaded photos in production.

Do not replace Flask with Django/FastAPI/Firebase/Supabase without explicit approval.

---

## 4. Local Commands and Verification

Run Android commands from the Android Gradle root (often `android/`, but inspect before assuming):

```bash
./gradlew assembleDebug
./gradlew testDebugUnitTest
./gradlew lintDebug
./gradlew connectedDebugAndroidTest  # emulator or device required
./gradlew spotlessCheck             # only after configured
./gradlew spotlessApply             # only after configured
```

Run Flask commands from `backend/` after the project has been scaffolded:

```bash
python -m pip install -e '.[dev]'
python -m flask --app 'app:create_app' run --debug  # LOCAL DEV ONLY
python -m flask --app 'app:create_app' db upgrade  # after Flask-Migrate is configured
python -m pytest -q
python -m ruff check .
python -m ruff format --check .
```

Commands are **expected targets**, not evidence of existing configuration. If a command differs from the created project, update `AGENTS.md` accordingly. Never claim a test, migration or build passed without actually running it.

**Before completion:** run relevant tests, formatting, lint, and builds where available. If you cannot run a check (e.g., no emulator/database), report the precise limitation.

---

## 5. Architecture Boundaries

### Android

```text
Composable → ViewModel → Use case → Repository → Room/DataStore/internal storage
                                      └─ (Cloud Beta) Outbox → Sync Worker → Flask API
```

- Composables only render UI and send events; no database, filesystem or Retrofit calls.
- Screens expose a `StateFlow<UiState>` and accept typed `UiEvent`s; use one-off `UiEffect`s for navigation/snackbars.
- Split a stateful route from a stateless previewable screen. `modifier: Modifier = Modifier` for reusable composables.
- Domain logic is plain Kotlin where feasible; repositories map Room entities and API DTOs into domain models.
- Keep local writes and outbox enqueueing in one Room transaction when cloud sync is enabled.
- Even online, **read from Room**. WorkManager applies remote changes back into Room.

### Flask

```text
Blueprint / request validation → Auth + ownership → Service → SQLAlchemy → PostgreSQL
                                                     └─ Private photo store
```

- Blueprints handle parsing/HTTP responses; service layer owns business rules; persistence queries remain explicit.
- Keep authentication and object ownership checks server-side on **every** user-owned endpoint.
- Use DB transactions for multi-row mutations, not ad-hoc partial commits.
- Avoid hidden globals and circular imports; register extensions through the application factory.
- Keep API schemas and documented contracts consistent; version breaking changes.

---

## 6. Kotlin and Compose Standards

- Official Kotlin style; prefer immutable values and data classes; no `!!` in production.
- Inject `Clock` and dispatchers; don't use `GlobalScope` or arbitrary hardcoded `Dispatchers.IO` in testable code.
- Keep business logic out of composables and navigation destinations.
- Provide previewable stateless Composables for loaded, empty and important error states.
- Use centrally defined Material 3 theme tokens from `docs/DESIGN.md`; avoid hardcoded design colors in feature screens.
- Stable keys in lazy lists; no full-resolution photos in lists/grids.
- Text belongs in resources (`values/` English; `values-in/` Indonesian when feasible).
- Labels/content descriptions for meaningful icons, readable color contrast, ≥48dp touch targets, tested font scaling.
- Use five navigation destinations; **Wishlist is excluded from owned collection totals**.
- Never show mock counts as if they were real user content.

---

## 7. Critical Domain Invariants

### Identity / persistence

- All syncable entities use **client-generated UUIDs** (not auto-increment IDs tied to a device).
- Room schemas are exported and committed. Every breaking schema edit gets a migration and migration test; never use `fallbackToDestructiveMigration()` in release code.
- Use explicit relationships and indexes. Keep creation/update/deletion timestamps consistent.
- Deletions of synced entities use tombstones until propagated; do not accidentally resurrect deleted data.

### Kit lifecycle and progress

- Valid statuses: `WISHLIST`, `BACKLOG`, `BUILDING`, `COMPLETED`; enforce transitions in use cases.
- `completedAt` is set on completion and cleared on reopen, without deleting build history.
- Progress derives from `BuildStage`: `round(100 × done / applicable)`, excluding `SKIPPED` stages; 0 when none apply.
- A 100% checklist does **not** automatically mark a kit as Completed.

### Expenses

- Money is integer rupiah (`Long`/DB bigint). Never store money in `Double`/`Float`.
- **`Expense` is the single purchase/cost ledger**. A UI `pricePaid` input maps to one `KIT` expense; do not duplicate price in Kit and then add it again in totals.
- Per-kit cost sums expenses linked to that kit; total spend includes general expenses (`kitId = null`).

### Timer

- Active timer state is local and persisted in DataStore. UI ticks are **display only**.
- Use a monotonic clock for in-boot duration plus a separate wall time for display/recovery.
- Stop creates a finished `BuildSession`; reopening the app must not create duplicates.
- On reboot/clock anomaly, stop for review and support adjustment; do **not** promise exact duration through power-off.
- No foreground service for Local MVP unless explicitly re-scoped.
- The timer must remain usable when notification permission is denied.

### Photos and backups

- Copy photos from Photo Picker to internal storage; never persist external `content://` URI as the only source.
- Compress and strip unneeded location metadata, generate thumbnails, use relative local file paths.
- Deleting DB records and cleaning files requires recoverable cleanup; Room transactions do not atomically cover files.
- ZIP restore validates manifest, schema, checksums, archive paths and file sizes; stage files and use rollback/recovery strategy.
- No broad media-storage permissions without a documented requirement.

---

## 8. Flask API Rules (Cloud Beta)

**Versioned endpoints** under `/api/v1`; the exact REST contract and errors belong in `docs/openapi.yaml` before client implementation.

- Optional email/password account, strong password hash (Argon2id preferred), short-lived access tokens, rotating/revocable refresh tokens.
- Enforce authorization per record/user, not just authenticated status. Include tests for cross-account UUID access (IDOR).
- Validate and cap all payloads: enums, monetary values, text, pagination, photos, size, actual file type.
- Return predictable JSON errors, e.g. `{"code":"INVALID_INPUT","message":"...","requestId":"..."}`. Do not leak stack traces, password details or credentials.
- UUIDs created offline must be accepted idempotently; mutation requests carry an operation ID, and server deduplicates retries.
- Use server-managed revision/ETag; stale updates return `409`, not silent last-write-wins overwrites.
- Soft deletions/tombstones and cursor-based delta sync must cover every synchronized entity.
- Photos live in private storage, accessed through authorized handlers or short-lived signed URLs. The remote DB never stores Android local paths.
- Use Flask development server only locally. Production uses Gunicorn and HTTPS, with debug disabled.
- Use environment-based secrets and least-privileged database accounts; never expose a wildcard browser CORS policy by default.
- Keep DB migrations committed and tested; take and verify backups before destructive deploys.
- Provide rate limiting, safe logs, sensible quotas, health check, privacy and account deletion path before public Cloud Beta.

---

## 9. Offline Sync Rules (Cloud Beta)

- Never require network for normal kit viewing or editing.
- Changes are stored locally and queued to a **persistent transactional outbox**.
- WorkManager syncs on connectivity with retries/exponential backoff; `INTERNET` permission is introduced **only with Cloud Beta integration**.
- API operations are idempotent, identified by operation UUID.
- Pull by server-issued cursor, including tombstones; apply to Room in a transaction.
- Server versions detect stale edits. Preserve local content on conflict and provide an explicit resolution UX.
- First sign-in explains upload/merge. Never wipe a local guest collection during signup, login, logout, or initial sync without a separate explicit confirmation.
- Upload photo metadata and bytes separately; never mark complete if a photo has not been durably stored.
- Active timer stays local; only completed sessions are synchronized.
- Ensure two-device and offline tests before enabling automatic sync by default.

---

## 10. Python Style and Backend Tests

- Follow PEP 8, use type hints in nontrivial service functions, and run Ruff on changed files.
- No credentials, tokens or personal records in logs or test fixtures committed to Git.
- Keep request validation separate from persistence; avoid giant route functions and SQL in Blueprints.
- DB changes are Alembic revisions with upgrade/downgrade considerations; never silently recreate production tables.
- Prefer deterministic tests with a temporary PostgreSQL DB/container and seeded fixtures. Mock external storage and email as appropriate.
- Required tests: registration/auth/token rotation, ownership access, CRUD, validation errors, pagination, idempotency, conflict 409, tombstones, upload restrictions, migrations and a sync contract smoke test.
- Do not weaken authentication/ownership tests to make the suite green.

---

## 11. Agent Workflow, Git and Review

1. **Read before editing:** `docs/PLAN.md`, `docs/DESIGN.md` for visual work, `AGENTS.md`, plus the relevant existing code.
2. **Identify active milestone/phase:** do not implement cloud dependencies or endpoints during local-only tasks without request.
3. **State assumptions:** especially around data migrations, authentication, sync ownership or destructive behaviors.
4. **Make focused changes:** small, reviewable patches and commits; preserve working functionality.
5. **Add tests:** new behavior + relevant regression checks; maintain schema/migration tests.
6. **Verify honestly:** run accessible commands; record exact success, failure, or environment limitations.
7. **Keep docs updated:** reflect completed roadmap items in `docs/PLAN.md` and evolving conventions/contracts in the appropriate doc.
8. **Commit each completed task:** after verification, create a separate Conventional Commit for each task, including its related code, tests, and documentation changes (including `docs/PLAN.md` and `docs/DESIGN.md` when changed). Do not accumulate unrelated completed tasks into one commit. This is standing authorization to commit completed tasks unless the user instructs otherwise; push only when requested.

Conventional commits:

```text
feat(android): add build-stage checklist
feat(backend): add authenticated kit endpoints
feat(sync): implement durable outbox worker
fix(expenses): avoid duplicated kit purchase cost
test(backend): reject cross-account kit access
docs: align PLAN and AGENTS with Flask roadmap
```

- `main` must remain buildable. Create a new, short-lived branch before starting each feature or any major change; never implement major changes directly on `main`. Use `codex/feat/<topic>` for features and `codex/fix/<topic>` for fixes.
- Minor changes, such as small documentation updates or localized fixes without architectural, schema, or broad behavior changes, may be made directly on `main`. Every new feature still requires its own branch regardless of size. If scope grows into a major change, create a branch before continuing.
- No unrelated refactors, surprise deployments, destructive operations, secret commits, release keystores, or `local.properties`.
- Do not bypass failing checks using unjustified suppression or disabled tests.
- Use explicit approval before external deployments, account migrations, data deletion or infrastructure spending.

---

## 12. Definition of Done per Task

- [ ] Request implemented without unrelated behavior changes.
- [ ] `docs/PLAN.md` release scope and `docs/DESIGN.md` UI contract still satisfied.
- [ ] Correct domain invariants (UUID, money, status, stages, timer, data ownership).
- [ ] Tests written/updated and relevant build/lint/format/migration checks run where possible.
- [ ] Loading/empty/error and accessibility states covered for UI changes.
- [ ] Docs/contracts and checklist updated where needed.
- [ ] Each completed task has its own commit with related documentation; feature and major changes use a dedicated branch.
- [ ] No secrets, private user data, destructive migrations or insecure public endpoints introduced.
- [ ] Final report includes files changed, checks actually run and any limitations.

---

## 13. Glossary

- **Gunpla:** Gundam plastic model kits.
- **Backlog:** owned kit not yet being built.
- **WIP:** work-in-progress photo.
- **Build stage:** per-kit checklist item; completed/skipped status drives progress.
- **Build session:** completed time interval spent working on one kit.
- **Local MVP:** Android app that requires no backend or account.
- **Cloud Beta:** optional Flask-backed account, private storage and synchronization.
- **Outbox:** local queue of changes pending upload.
- **Tombstone:** deletion marker retained to synchronize a deletion across devices.
