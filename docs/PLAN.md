# PLAN.md — Nubmark

> **Nubmark — Every Kit Has a Story.**\
> Android app for collecting, documenting, and building Gunpla / plastic model kits.\
> **Application ID:** `id.my.chromazone.nubmark`\
> **Product approach:** local-first Android application, followed by an **optional Flask-powered cloud account, backup, and synchronization service**.\
> **Team:** one developer, part-time. **Document status:** planning; checkboxes are not implementation claims.

Status: `[ ]` todo · `[~]` in progress · `[x]` done

**Related references:** `DESIGN.md` (approved UI design) and `AGENTS.md` (contributor and coding rules). The approved design is **light, clean, white with restrained blue accents**, not the dark sci-fi concept. Figma: [Nubmark](https://www.figma.com/design/bFClgupa4BKpWsVHin7Yj5/Nubmark?node-id=0-1).

---

## 1. Product Vision and Problems

Nubmark helps Gunpla hobbyists answer: *What do I own, what should I build next, how far along is this build, and how much have I spent?*

Problems:
- **Backlog / pile of shame:** owned-but-unbuilt kits are hard to track.
- **Duplicate purchases:** it is easy to forget what is already owned or wishlisted.
- **Lost build history:** progress notes and photos are scattered across the gallery.
- **Unknown cost:** kit purchases, paint, tools, and finishing supplies add up.
- **Unknown effort:** builders cannot easily see how long their kits took to assemble.
- **Device loss (cloud phase):** a single-device collection can be lost without backups.

Differentiators:
1. Gunpla-aware lifecycle: **Wishlist → Backlog → Building → Completed**.
2. Per-kit stage checklist, build journal, photo gallery, and session timer.
3. **Useful without an account or connection**; local Room data remains the Android source of truth.
4. Clean, image-first library and meaningful statistics.
5. **Optional cloud sync** through a self-hosted Flask REST API, without making login a prerequisite for core features.

---

## 2. Delivery Strategy and Scope

### 2.1 Two delivery milestones

| Milestone | What ships | Backend needed? |
|---|---|---|
| **A — Local MVP** | Full Android collection tracker, status workflow, photos, checklist, journal, timer, costs, basic stats, local ZIP backup | **No**. All core features work completely offline. |
| **B — Cloud Beta** | Flask API + PostgreSQL, optional account, authenticated cloud backup/sync, multi-device recovery, photo upload/download | **Yes**. Account and internet required **only** for these optional cloud features. |

Both milestones are part of this plan. Milestone B is a **planned implementation phase**, not a hypothetical future idea. Do not couple Milestone A UI/domain behavior to server availability.

### 2.2 Feature priorities

| Priority | Scope |
|---|---|
| **P0 / Local MVP** | Kit CRUD; Wishlist/Backlog/Building/Completed; collection grid, search and filters; Home; Kit Detail; editable build stages and progress; dated build log/notes; kit photos; build timer/sessions; expense ledger; basic stats; local ZIP backup/restore; Profile/Settings; accessibility/empty states |
| **P1 / Cloud Beta** | Flask REST API; PostgreSQL; user authentication; per-user authorization; cloud persistence for kits/stages/logs/sessions/expenses; photo storage; offline write queue; sync and conflict handling; account connection and sign out; deployment and monitoring |
| **P2 / Enhancements** | Advanced statistics, widget, CSV export, dark mode, dynamic color, barcode prefill, paint/tool inventory, shareable build cards |
| **Later** | Community features, licensed online kit catalog, social sharing, cross-platform clients |

### 2.3 Explicit non-goals

- No **mandatory** login, network dependency, or paywall for collection tracking.
- No official Bandai/Gundam branding, unauthorized copyrighted photo bundles, or scraping without rights.
- No community feeds, marketplace, or third-party kit catalog for the two milestones.
- No tablet-specific or foldable-optimized UX in the first release (layouts must remain usable).
- No Android foreground service merely to keep a ticking timer in memory.

### 2.4 Product decisions already made

| Topic | Decision |
|---|---|
| Name | **Nubmark**; tagline **Every Kit Has a Story.** |
| Package | `id.my.chromazone.nubmark` |
| UI | `DESIGN.md`: Material 3, light background, muted blue accents, kit photography first |
| Navigation | **Home · Collection · Wishlist · Builds · Profile** (five bottom tabs) |
| Default locale | English UI; Indonesian translation in resources where feasible |
| `minSdk` | API 26; `targetSdk` latest stable compatible with dependencies at implementation time |
| Local data | Room, DataStore, app-internal photo files; **no network required** |
| Server | Python + Flask; PostgreSQL; isolated `backend/` service |
| Cloud opt-in | Local data can exist indefinitely without an account; first upload requires explicit consent |
| Cost | Store money as integer **IDR rupiah** (`Long` on Android, integer/bigint on server), never floating point |
| Record IDs | Generate stable **UUIDs on-device** to support offline creation and eventual sync |
| Kit entry | Manual entry with local autocomplete. No dependency on an unverified official kit API |

---

## 3. User Journeys and Status Rules

```text
First launch ──> Home (empty state) ──> Add kit ──> Wishlist / Backlog
                                                           │
Wishlist ── purchase ──> Backlog ── start build ──> Building ── finish ──> Completed
                                           │                   │
                                      pause/reopen         Photos, stages,
                                           │               journal, sessions
                                           └──── Backlog ◀───────┘

Optional after local use:
Profile ──> Cloud Sync ──> Sign up / Sign in ──> Confirm upload/merge
                                              ──> background synchronization
```

| Transition | Required behavior |
|---|---|
| Wishlist → Backlog | Offer optional purchase amount, store and purchase date; add one `KIT` expense **if a purchase amount is entered**. Do not count wishlisted items as owned. |
| Backlog → Building | Set `startedAt` if not already set, initialize default applicable stage checklist if needed, optionally start timer. |
| Building → Backlog | Pause any active timer; preserve history and checklist. |
| Building → Completed | Stop/finalize active timer, set `completedAt`, offer final photo/rating; no photo/rating required. |
| Completed → Building | Reopen the build and clear `completedAt`; preserve sessions and photos. |

- Status mutations happen in use cases and are covered by tests.
- A user may edit/skips stages; **marking all stages complete suggests, but does not automatically perform, status completion**.
- If a wishlist item is bought, it moves to `Backlog` and its purchase expense is recorded once.

---

## 4. UI and Information Architecture

`DESIGN.md` is authoritative for colors, fonts, spacing, component styling, and UX states. Build the following navigation **instead of** the older four-tab Collection/Wishlist/Statistics/Settings layout.

```text
Nubmark
├── Home
│   ├── Collection totals (owned only)
│   ├── At a Glance / basic statistics
│   ├── Quick Access
│   └── Recently Updated
├── Collection
│   ├── Search / status chips / grade filters / sort
│   ├── Add / Edit Kit
│   └── Kit Detail
│       ├── Overview
│       ├── Build Log / Sessions
│       ├── Photos
│       └── Notes / Costs
├── Wishlist
│   └── Add / Edit / Purchase (move to Backlog)
├── Builds
│   ├── Active builds
│   ├── Build Progress / Stage Checklist
│   └── Timer / Session history
└── Profile
    ├── Statistics
    ├── Settings / Local Backup & Restore
    ├── Cloud Sync (only after backend phase)
    └── About
```

### Primary screen acceptance criteria

- **Home:** accurate owned-kit counts and recent activity; no fake sample values when data is empty.
- **Collection:** image-first two-column grid where width permits; grade/status/search filters combine correctly.
- **Kit Detail:** image gallery, metadata, progress, tabs for log/photos/notes, and appropriate status actions.
- **Builds:** active build list, progress ring based on real stage completion, editable checklist, and timer entry.
- **Wishlist:** separate from owned kit totals, with a clear **Move to Collection** action.
- **Profile:** statistics, preferences, backup/restore, then optional account/sync settings in Cloud Beta.
- **Shared:** loading/empty/error states, image fallbacks, 48dp touch targets, font scaling, accessibility labels, and responsive safe areas.

---

## 5. Android Architecture and Stack

| Layer | Choice |
|---|---|
| UI | Kotlin + Jetpack Compose + Material 3 |
| State | MVVM, UDF (`UiState`, `UiEvent`, `UiEffect`) |
| Navigation | Navigation Compose with type-safe destinations |
| Injection | Hilt |
| Local DB | Room + KSP + Flow; exported migrations |
| Settings / active timer | DataStore |
| Media | Android Photo Picker; Coil; CameraX optional |
| Async | Kotlin Coroutines + Flow |
| Time | Injected Clock; timestamps are the truth |
| Graphs | Custom Compose Canvas initially; evaluate Vico only if needed |
| Local backup | ZIP with JSON manifest and photo files; Storage Access Framework |
| **Cloud Beta only** | Retrofit/OkHttp, kotlinx.serialization, WorkManager, secure token storage backed by Android Keystore |
| Tests | JUnit, Turbine, Room in-memory, Compose UI tests, integration tests |
| Build | Gradle Kotlin DSL + `libs.versions.toml` |

**Android read/write path (Cloud Beta):**

```text
Compose UI → ViewModel → Use Case → Repository → Room / internal photos
                                       │
                                       └─ persistent outbox + WorkManager
                                                ↓ (when online)
                                         Flask REST API → PostgreSQL / object storage
                                                ↓
                                          merge changes → Room → UI
```

- UI reads from Room **even while online**; no direct API calls from composables.
- Local writes succeed immediately and enqueue a durable outbox operation when an account is connected.
- Background sync is best-effort and retryable; no screen should be blocked on network availability.

### Repository layout (one repo, two runnable projects)

```text
nubmark/
├── android/                     # Android Studio / Gradle project
│   ├── app/src/main/java/id/my/chromazone/nubmark/
│   │   ├── core/{design,navigation,ui,util}/
│   │   ├── data/{local,remote,repository,storage,sync}/
│   │   ├── domain/{model,usecase}/
│   │   ├── feature/{home,collection,kitdetail,kitform,wishlist,builds,profile}/
│   │   ├── timer/
│   │   └── di/
│   └── gradle/libs.versions.toml
├── backend/                     # Flask / Python service
│   ├── app/{api,auth,models,schemas,services,storage,extensions}/
│   ├── migrations/
│   ├── tests/
│   ├── pyproject.toml
│   ├── wsgi.py
│   └── Dockerfile
├── docs/                        # API specification, architectural notes
├── PLAN.md
├── AGENTS.md
├── DESIGN.md
└── README.md
```

If the Android app already exists at repository root, **do not move it solely to match this proposed tree**. Adopt the structure incrementally, document actual command locations, and avoid unrelated changes.

---

## 6. Local Domain and Data Model

### 6.1 Entities

Use immutable domain models and explicit Room entities. The following is a **logical schema**, not a paste-ready Room class. UUID strings are generated on the client at creation.

| Entity | Core fields / notes |
|---|---|
| `Kit` | `id UUID`, name, grade, series?, scale?, status, targetPrice?, rating?, notes?, startedAt?, completedAt?, coverPhotoId?, `createdAt`, `updatedAt`, `deletedAt?` |
| `BuildStage` | `id UUID`, kitId FK, name, order, `state` (`TODO`, `DONE`, `SKIPPED`), completedAt?, timestamps |
| `BuildLogEntry` | `id UUID`, kitId FK, loggedAt, title?, body, timestamps |
| `BuildSession` | `id UUID`, kitId FK, startedAt, endedAt, durationMs, note?, timestamps |
| `KitPhoto` | `id UUID`, kitId FK, type (`BOX`, `WIP`, `FINAL`), relativeLocalPath, thumbnailRelativePath, captureDate?, timestamps; remote object info kept in separate sync metadata |
| `Expense` | `id UUID`, kitId? FK, category (`KIT`, `PAINT`, `TOOL`, `OTHER`), amount IDR integer, date, shop?, note?, timestamps |
| `OutboxOperation` | Cloud Beta only: unique operation UUID, entity type, record UUID, operation, payload/version, queuedAt, attempt state |
| `SyncMetadata` | Cloud Beta only: record UUID, last known server version, upload/download state, last cursor |

**Grade values:** `SD`, `EG`, `HG`, `RG`, `MG`, `PG`, `MGSD`, `OTHER` (support free-text model line if needed). **IDs and references use UUIDs** from the start to avoid a later local-ID/server-ID migration.

### 6.2 Critical consistency rules

- **Money has one source of truth: `Expense`.** Kit purchase prices are `Expense(category = KIT, kitId = ...)`. The form may show “Price paid” but must create/update the corresponding purchase expense, not a duplicate `Kit.pricePaid` field.
- `kitCost = SUM(Expense.amount WHERE kitId = kit.id)`; `overallSpend = SUM(Expense.amount)` including general tools. Shared supplies without a specific kit keep `kitId = null`.
- `totalBuildMs = SUM(BuildSession.durationMs)`. **An active, unfinished timer is not counted as a finished session** until stopped (optional live UI preview is separate).
- `applicableStages = stages where state != SKIPPED`; `progressPercent = round(100 * done / applicableCount)` when count > 0, otherwise `0`. A skipped stage is excluded from numerator and denominator.
- Wishlist records are excluded from owned collection totals and owned-kit grade distribution.
- Status transitions and timestamp changes must be atomic with corresponding local writes.
- Room foreign keys: stage/log/session/photo → kit `CASCADE`; expenses linked to a deleted kit may be retained as general expenses (`SET NULL`) with an explicit user-facing delete option.
- Index foreign keys plus frequent filter columns (`Kit.status`, `Kit.grade`, `updatedAt`). Export schemas and test migrations; never use destructive release migrations.
- Use `deletedAt` tombstones for **synced records** so deletion can propagate; permanent cleanup only after synchronization and retention policies.

### 6.3 Default build stages

1. Unboxing & Prep
2. Frame / Inner Build
3. Armor Assembly
4. Weapons & Equipment
5. Detailing (Panel Line / Decals)
6. Topcoat & Finish
7. Final Photos

Template stages may be renamed, reordered, marked skipped, or removed where they do not apply. Preserve meaningful progress after edits; do not assume every kit has an inner frame or topcoat.

---

## 7. Timer, Photos, and Backup

### 7.1 Timer

Persist local timer state (`kitId`, accumulated duration, resume timestamps, running flag) in DataStore. A monotonic clock (`SystemClock.elapsedRealtime`) is preferred for active measurement within a boot; keep wall-clock timestamps for display and recovery. The UI refresh interval is **display-only**.

- Start, pause, resume, stop; only one active timer in the Local MVP.
- Finishing a session saves a `BuildSession` and clears persisted active state.
- After process death, recover from persisted timestamps; an OS notification is **not** the timer engine.
- After reboot or a significant clock change, recover conservatively: **pause for review and allow the user to adjust duration**. Do not promise uninterrupted precise timing across power-off.
- A persistent/ongoing notification and actions are best-effort subject to Android restrictions and permission; timer must work if `POST_NOTIFICATIONS` is denied.
- Do not add a foreground service for the Local MVP unless a newly established product requirement warrants it and platform rules are reviewed.

### 7.2 Photos

- Use Android Photo Picker (no broad library permission). Optional camera capture through CameraX.
- Copy into app-internal storage, normalize orientation, strip unwanted location EXIF metadata, compress to ~1600px long edge, and generate ~400px thumbnails.
- Store **relative paths** locally. Render thumbnails in lists/grids; never decode full-sized files there.
- When a kit/photo is deleted, coordinate DB and file cleanup with a recoverable/idempotent strategy; a database transaction does **not** make filesystem deletion atomic.
- In Cloud Beta, upload photo bytes separately from metadata and keep local thumbnails working while uploads are pending.

### 7.3 Local ZIP backup / restore

- ZIP manifest (`schemaVersion`, `exportedAt`, checksums), JSON records and `photos/`.
- Validate schema, sizes, IDs, references, and checksums before applying a restore; prevent ZIP path traversal and oversized entries.
- Stage files in a temporary directory, restore data transactionally, and finalize file swap with a recovery journal/rollback. **A Room transaction alone cannot guarantee atomic file+database restoration.**
- Local backup is available without an account, even once Cloud Beta exists.
- First release supports **Replace all** after explicit confirmation; merge restore can be deferred.

---

## 8. Flask Backend — Architecture and Responsibilities

### 8.1 Why Flask exists

The backend enables **optional cloud backup and synchronization**, not local CRUD. Its responsibilities are authentication, per-account authorization, durable storage, sync APIs, safe photo uploads/downloads, and recovery on a second device. It is **not** a source of UI state during normal offline use.

### 8.2 Server tech stack

| Concern | Selection |
|---|---|
| Language / framework | Python 3.12+ (choose a supported version) + Flask, **application factory** and versioned Blueprints |
| REST validation | Marshmallow or Pydantic (pick one; validate request and response contracts) |
| Persistence | PostgreSQL + SQLAlchemy 2.x |
| Schema migrations | Alembic / Flask-Migrate; checked-in migrations |
| Authentication | Email/password with strong password hashing (Argon2id where available), short-lived access token, rotating refresh token with revocation |
| API docs | OpenAPI document stored in repo (`docs/openapi.yaml`) |
| Photo storage | Private object storage in production; local isolated storage volume for dev only |
| Tests | pytest, Flask test client, PostgreSQL integration tests |
| Formatting/lint | Ruff; typing (mypy or pyright if adopted) |
| Deployment | Docker, Gunicorn, TLS reverse proxy, environment-based secrets, structured logs |
| Operations | Health checks, DB backups, error monitoring, retention and restore drills |

- Use Flask's built-in server **only for development**; deploy with a production WSGI server. See [Flask deployment guidance](https://flask.palletsprojects.com/en/stable/deploying/).
- No public user collection endpoint may be served without authentication and object ownership checks.
- Deployment target (VPS, PaaS, or managed service), storage provider and hostname are **configuration choices**, not assumptions about existing infrastructure.

### 8.3 Backend logical entities

`User`, `RefreshToken` (hashed/revocable), `Kit`, `BuildStage`, `BuildLogEntry`, `BuildSession`, `Expense`, `KitPhoto`, `PhotoObject`, `SyncChange`/change cursor, and a processed-operation/idempotency table.

- User-owned tables have `user_id` and owner-scoped queries/constraints.
- Client-generated UUIDs remain stable across Android and server. IDs do **not** depend on PostgreSQL auto-increment.
- Each record has server-managed version/revision, UTC timestamps, and a deletion tombstone where relevant.
- Never persist Android device-local photo file paths in the remote database. Store private object keys and metadata.

### 8.4 Minimal REST contract (versioned)

All paths below begin with `/api/v1`. Exact JSON schemas must be specified in OpenAPI **before implementing the Android remote client**.

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Liveness (no sensitive server metadata) |
| `POST` | `/auth/register` | Create optional cloud account |
| `POST` | `/auth/login` | Issue access and refresh tokens |
| `POST` | `/auth/refresh` | Rotate refresh token and renew access |
| `POST` | `/auth/logout` | Revoke refresh session |
| `GET` | `/auth/me` | Current authenticated account |
| `GET` | `/kits` | Paginated user-owned kits (diagnostics/recovery) |
| `POST` | `/kits` | Create user-owned kit with client UUID, idempotently |
| `GET` | `/kits/{id}` | Read user-owned kit |
| `PATCH` | `/kits/{id}` | Update kit with expected revision / ETag |
| `DELETE` | `/kits/{id}` | Soft delete, retaining tombstone for sync |
| `POST` | `/kits/{id}/photos` | Validate/authenticate and upload photo |
| `GET` | `/kits/{id}/photos/{photo_id}` | Authorized photo retrieval / short-lived URL |
| `DELETE` | `/kits/{id}/photos/{photo_id}` | Delete metadata and schedule object cleanup |
| `POST` | `/sync/push` | Idempotent batch of local changes with revision checks |
| `GET` | `/sync/changes?cursor=...` | Paginated changes (including deletions) since cursor |

Additional stage, log, session and expense data may be handled via documented batch sync or resource endpoints; no hidden API contracts. Use standard errors (`400`, `401`, `403`, `404`, `409`, `413`, `422`, `429`, `500`) with a consistent `{code, message, details?, requestId}` shape and no secrets.

### 8.5 Authentication, security and privacy

- Cloud accounts are optional. Provide **Guest / Continue offline** on Android.
- Hash passwords with a modern adaptive algorithm, never plaintext or reversible encryption.
- Protect authentication endpoints with rate limiting and generic error messages; require HTTPS; securely rotate/revoke refresh credentials.
- Android uses Android Keystore-backed token protection. Never log passwords, tokens, private photo URLs, or sensitive user data.
- Authorize each object against `user_id`. A valid token alone does not authorize access to another user's UUID.
- Validate types, enumerations, money ranges, stage order, mime/file signature and maximum upload size. Strip sensitive photo metadata.
- Define CORS only if a trusted browser client is later introduced; Android native clients do not need an open CORS policy.
- Maintain account deletion/data export workflows and a privacy policy before public cloud release.
- Use HTTPS, secret management, least-privilege DB credentials, DB backup encryption and recovery testing.

---

## 9. Offline-to-Cloud Sync Design

This is a **nontrivial feature**, with its own planned milestone and tests. Do not assume Retrofit calls alone provide synchronization.

### 9.1 Core rules

1. **Room remains the Android source of truth.** All user actions mutate local records first.
2. On write, atomically save the domain change and a persistent outbox item in the same Room transaction (when signed in).
3. Use WorkManager with connectivity constraint, retry and exponential backoff; expose sync status without blocking normal use. [Android offline-first guidance](https://developer.android.com/topic/architecture/data-layer/offline-first).
4. The server deduplicates client operations by operation UUID and returns authoritative record revisions.
5. Pull changes using server-generated cursors (do not rely solely on device wall-clock timestamps). Apply batch updates to Room transactionally.
6. Delete propagation uses tombstones rather than immediate hard deletion. Server garbage-collects tombstones only after a documented safe retention window.
7. **Conflicts:** send expected revision; server returns `409` on a stale version. Preserve local unsynced data and surface a conflict resolution choice (e.g., **Keep local** / **Use cloud**), never silently discard a build or photo.
8. **First sign-in:** explain what will upload; explicitly ask whether to merge local data with the account or keep collections separate. Never silently replace one with the other.
9. **Sign out:** revoke remote session and stop sync; ask whether to retain the device's local collection. Logging out must not erase offline data by surprise.
10. **Photos:** metadata and media are distinct sync steps; retry uploads/downloads safely with size limits and checksums. Do not mark a photo synced before its content is durable.

### 9.2 Sync edge cases to test

- Create/edit/delete while offline, reconnect and upload exactly once.
- App killed between local commit and upload; retry succeeds without duplicates.
- Two devices edit the same kit; stale revision produces visible conflict resolution.
- Deleted kit and late changes from second device; no unwanted resurrection.
- Partial media upload, timeout, quota/error, and safe retry.
- Existing local collection attached to a new/old account without silent data loss.
- Clock skew; empty changes; expired cursor/token; server outage.

---

## 10. Roadmap and Checklists

Estimates are **rough solo-developer planning effort**, not promises. Implement in small verifiable increments; update dates only after measuring actual progress.

### Milestone A — Local MVP (approximately 9–12 part-time weeks)

#### Phase 0 — Repository and UI foundation
- [ ] Set project name and package ID to `id.my.chromazone.nubmark`.
- [ ] Confirm Android project layout and tooling; configure Compose, Hilt, Room, DataStore, version catalog.
- [ ] Apply `DESIGN.md` light theme, reusable cards, status badges, progress indicators, accessible labels.
- [ ] Implement five-tab NavigationBar and empty/loaded/loading/error screen skeletons.
- [ ] Set up Gradle lint, JVM tests, formatting, CI; ensure `AGENTS.md` is current.
- [ ] Establish UUID-based schema and Room migrations/schema export from the start.

**Exit:** App builds; five destinations navigate; theme and CI work; no backend required.

#### Phase 1 — Collection + Wishlist
- [ ] Kit/expense entities, DAO, repositories, use cases and tests.
- [ ] Create/edit/delete kit, image placeholder, manual grade/scale/series input.
- [ ] Collection grid with combined search, status filters, grade sorting.
- [ ] Wishlist screen and purchase → Backlog flow; price creates **one** expense.
- [ ] Home summary with real counts and recently updated items.
- [ ] Status transitions, confirmations, snackbar/undo where safe.

**Exit:** Collection and wishlist work fully offline with accurate owned totals.

#### Phase 2 — Kit Detail, checklist and journal
- [ ] Kit Detail Overview / Build Log / Photos / Notes UI.
- [ ] Stage model and default template; done/skip/edit/reorder; progress calculation tests.
- [ ] Build log entries and notes; optional linkage to photos.
- [ ] Build list with progress ring and contextual actions.
- [ ] Gallery import, compression, thumbnails, cover photo and safe cleanup.

**Exit:** A real kit can be built and documented end-to-end using the approved UI.

#### Phase 3 — Build timer and sessions
- [ ] Timestamp/monotonic-based local timer state and fake clock tests.
- [ ] Start/pause/resume/stop, one active session; persist completed sessions in Room.
- [ ] Timer UI + mini player + optional notification action handling.
- [ ] Test process death, app relaunch, clock changes, reboot recovery UX.

**Exit:** Sessions and accumulated time are correct; reboot anomalies can be reviewed and corrected.

#### Phase 4 — Costs, statistics and local recovery
- [ ] Per-kit and overall expense ledger with no double counting.
- [ ] Basic statistics in Home/Profile and grade/status counts.
- [ ] ZIP export/restore with validation, image recovery, failure tests.
- [ ] Consistent currency formatting, accessibility, empty/loading/error states.

**Exit:** Expense totals reconcile and full local data/photos can be restored.

#### Phase 5 — Android local release hardening
- [ ] Instrumented Room/migration tests, Compose flow tests, performance with 500+ kits.
- [ ] App icon, splash, language resources, privacy copy, no misleading demo content.
- [ ] Android permission audit, QA on supported API levels, release signing hygiene.
- [ ] Internal/closed Android testing build.

**Exit:** Milestone A definition of done is met without a server.

### Milestone B — Flask Cloud Beta (approximately 6–9 additional part-time weeks)

#### Phase 6 — Flask backend foundation
- [ ] Create `backend/` Python project with app factory, Blueprints, env-based config, Ruff and pytest.
- [ ] Set up PostgreSQL, SQLAlchemy, Alembic/Flask-Migrate and reproducible migrations.
- [ ] Set up Docker dev environment, DB health check and production WSGI entrypoint.
- [ ] Define OpenAPI schemas, canonical UUIDs, ownership, revisioning and error format.
- [ ] Add API CI using an ephemeral PostgreSQL test DB.

**Exit:** Backend boots reproducibly; `/api/v1/health` and migration/test checks pass.

#### Phase 7 — Auth and cloud data APIs
- [ ] Implement register/login/refresh/logout/me and secure password/token handling.
- [ ] Add owner-scoped CRUD/storage for Kit, BuildStage, BuildLogEntry, BuildSession and Expense.
- [ ] Implement photo upload/retrieve/delete with validation and private storage.
- [ ] Add consistent validation, pagination, idempotency, rate limiting, structured errors.
- [ ] Write tests for unauthorized access, cross-account isolation, duplicates and limits.

**Exit:** Authenticated API can safely persist an account's full collection without cross-user leaks.

#### Phase 8 — Android/cloud integration
- [ ] Add Retrofit client and typed API DTOs **without exposing them to Compose UI**.
- [ ] Add optional sign-in/profile sync settings and clear local-to-cloud consent flow.
- [ ] Implement durable outbox and WorkManager push/pull with server cursors.
- [ ] Implement conflict UI, tombstones, signed-in/signed-out transitions.
- [ ] Implement resumable/retryable photo sync and sync status indications.
- [ ] Test with two devices, offline edits, token expiry and backend outage.

**Exit:** Second-device restoration works; offline edits later sync without silent data loss.

#### Phase 9 — Cloud deployment and beta QA
- [ ] Configure deployment target, domain, TLS, Gunicorn/reverse proxy, environment secrets.
- [ ] Run migrations, private photo storage, automated PostgreSQL/storage backups.
- [ ] Add monitoring, quotas, audit-safe logging, restore drill and incident plan.
- [ ] Review privacy policy, account/data deletion, rate limits and cost ceilings.
- [ ] Run end-to-end Cloud Beta regression tests and monitored small beta rollout.

**Exit:** Production-like environment recovers from failures and enforces authentication/ownership.

### Explicitly deferred features

- [ ] Advanced charting and shareable build cards.
- [ ] Barcode scan and licensed catalog enrichment.
- [ ] Paint/tool inventory and supply consumption.
- [ ] Widgets, dark theme, community features.

---

## 11. Testing and Release Gates

| Layer | Required verification |
|---|---|
| Domain | Status transitions, skipped-stage progress, ledger arithmetic, owned vs wishlist counts |
| Timer | Fake-clock start/pause/resume/stop, app-process recovery, clock anomalies |
| Android persistence | DAO foreign keys, cascades/SET NULL, migrations, UUIDs, outbox atomicity |
| Media/backup | Photo compression and deletion, ZIP tampering/path traversal, failed restore rollback |
| Compose UI | Add-kit, wishlist purchase, stage completion, timer and empty-state flows |
| Flask API | pytest unit/integration, schema validation, migrations, ownership, unauthorized requests |
| Auth/security | Wrong credentials, rate limits, refresh rotation, revoked tokens, upload limits, IDOR tests |
| Synchronization | Lost connection, duplicated request, edit conflicts, tombstones, two devices, first upload |
| CI | Android lint/test/assemble; backend Ruff/pytest/migration smoke tests |
| Deployment | HTTPS, no development server/debug, backup restoration, log/secret scan |

### Definition of Done — Local MVP

- [ ] P0 features work on supported Android versions without requiring internet/login.
- [ ] The approved `DESIGN.md` navigation and clean light visual language are implemented.
- [ ] Counts, progress, build times and spending reconcile with persisted data.
- [ ] Photos and JSON records survive an export/restore; malformed input fails safely.
- [ ] App relaunch/process death does not lose an active session; reboot uncertainty is handled honestly.
- [ ] Required Android tests/lint/build pass in CI.

### Definition of Done — Cloud Beta

- [ ] Optional cloud account can be created, signed in, refreshed and revoked securely.
- [ ] Flask/PostgreSQL APIs store all synchronizable records and private photos per user.
- [ ] Android app remains usable offline; queued changes sync later, with conflict protection.
- [ ] Second device can restore all cloud-synced data and photos.
- [ ] Ownership, idempotency, tombstones, auth, migration, upload and recovery tests pass.
- [ ] HTTPS deployment and tested backups are in place; core features remain guest-accessible.

---

## 12. Risks, Mitigations and Open Decisions

| Risk | Mitigation |
|---|---|
| Backend introduces unnecessary work for single-device use | Separate milestones; local-first works before and after Cloud Beta. |
| Sync conflicts or accidental data loss | Stable UUIDs, versions, tombstones, outbox, first-upload consent, conflict UI and tests. |
| Price counted twice | Canonical `Expense` ledger, not `Kit.pricePaid` + expense. |
| Stage progress mismatches UI | Store stage states; derive percentage from applicable stages. |
| Timer drift/reboot uncertainty | Monotonic timing within boot; recover for review, fake clock tests. |
| Photos/storage become expensive | Compression, storage limits, quotas, cleanup, optional cloud uploads. |
| Backup file/DB partial failure | Staging, checksums, recovery journal, transactional DB changes, tests. |
| Public API leaks account data | Central auth and per-object owner verification, integration tests. |
| Evolving schemas break clients | Versioned `/api/v1`, Alembic/Room migrations, contract tests. |
| Scope creep | Freeze P0/P1, track P2 ideas separately. |

**Open decisions (do not block Android local MVP):**
- [ ] Flask production hosting provider, hostname and photo object store.
- [ ] Email verification/recovery solution and sending provider for Cloud Beta.
- [ ] Cloud limits and retention policy (storage per account, backups, deleted records).
- [ ] Exact conflict-resolution UI copy, based on user testing.
- [ ] Whether dark theme and CSV export enter P2 or a later release.

**Next actionable step:** align existing repository naming and navigation to Nubmark / `DESIGN.md`; begin Phase 0. Backend foundation and API contract are explicitly scheduled for Phase 6, with schema compatibility (UUIDs, timestamps, outbox-ready models) considered from Phase 0 onward.
