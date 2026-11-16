# Nubmark — Design System & UI Specification

> **Every Kit Has a Story.**\
> **Status:** Approved visual direction / implementation reference\
> **Platform:** Android · Kotlin · Jetpack Compose · Material 3\
> **Application ID / Namespace:** `id.my.chromazone.nubmark`\
> **Last updated:** November 16, 2026

## 1. Design Direction

Nubmark is an Android application for managing a **Gunpla / plastic model kit collection**, tracking assembly progress, maintaining a wishlist, and documenting the story behind each build.

**Approved visual direction:** **Clean Minimal / Light** — the **white interface with subtle blue accents** from the first Nubmark concept mockup. The *dark futuristic hangar* concept is **not** the primary design reference.

![Approved Nubmark clean light UI concept](./nubmark_android_app_showcase.png)

> The image above is **concept art**, not a pixel-perfect design specification or a screenshot of an implemented application. Keep `nubmark_android_app_showcase.png` alongside this document as its supporting visual reference.

### Design principles

1. **Content first:** Gunpla and model kit photography is the main visual element; the interface should not compete with the photos.
2. **Clean and calm:** Use bright backgrounds, generous whitespace, simple cards, and restrained color accents.
3. **Track at a glance:** Collection status and build progress should be visible without excessive navigation.
4. **Builder identity:** Convey the Gunpla hobby through photography, terms such as *Backlog / Building / Completed*, and subtle nipper, runner, and box icons — **not** through an overly elaborate sci-fi HUD.
5. **Native-feeling:** Follow modern Android navigation, accessibility, and responsive-layout conventions.

### Initial scope

- **Light theme is the default** for the MVP; dark theme may be introduced later.
- The MVP is **offline-first**, without a mandatory account, backend, or cloud synchronization.
- Prioritize **Collection**, **Kit Detail**, **Build Progress**, and **Wishlist**.
- Advanced statistics can be deferred, but the layout may reserve space for them.

---

## 2. Brand Identity

| Element | Specification |
|---|---|
| App name | **Nubmark** |
| Tagline | **Every Kit Has a Story.** |
| Personality | Friendly, modern, organized, hobby-oriented, slightly technical |
| Primary logo | Simplified **runner/sprue + nipper** symbol |
| App icon | Rounded square, white or very light blue background, blue/navy mark |
| Brand accent | Blue, used sparingly for primary actions and active states |
| Avoid | Official Gundam/Bandai logos, franchise watermarks, aggressive sci-fi fonts, heavy neon styling |

**Interface labels** should initially use English to match the approved mockup: `Home`, `Collection`, `Wishlist`, `Builds`, and `Profile`. If Indonesian localization is added later, move user-facing text into Android string resources.

---

## 3. Color System

The following values are **initial design tokens** based on the approved mockup. Small adjustments are acceptable during implementation to preserve accessibility contrast and Material 3 consistency.

| Token | Hex | Usage |
|---|---|---|
| `brandBlue` | `#3B82F6` | Primary CTA, selected tabs, links, progress indicators |
| `brandBlueDark` | `#2563EB` | Pressed state, stronger emphasis |
| `brandBlueTint` | `#EAF2FF` | Selected chips, soft blue containers |
| `background` | `#FFFFFF` | Main screen background |
| `surface` | `#FFFFFF` | Cards, sheets, dialogs |
| `surfaceAlt` | `#F3F6FB` | Grouped sections, summary cards, secondary backgrounds |
| `surfaceSoftBlue` | `#EDF4FF` | Highlighted statistics and hero sections |
| `textPrimary` | `#172338` | Headlines, kit names, primary text |
| `textSecondary` | `#64748B` | Descriptions, captions, metadata |
| `outline` | `#E2E8F0` | Subtle borders and dividers |
| `success` | `#22C55E` | Completed state |
| `successTint` | `#DCFCE7` | Completed badge background |
| `warning` | `#D97706` | Noncritical warnings or optional wishlist priority |
| `backlogTint` | `#F1F5F9` | Backlog badge background |
| `danger` | `#DC2626` | Delete and destructive actions |

### Color usage rules

- **Primary CTA:** `brandBlue` background with white text; avoid dramatic gradients.
- **Secondary actions:** White/surface backgrounds with subtle outlines or `brandBlueTint`.
- **Headings:** Use navy (`textPrimary`) rather than absolute black.
- **Status colors:** `Backlog` = neutral, `Building` = blue, `Completed` = green. Never communicate status through color alone; include text and, where useful, an icon.
- Use `surfaceAlt` for larger grouping areas rather than stacking many strongly elevated cards.
- Ensure **WCAG AA contrast** for small text (at least 4.5:1 for normal-size text). Adjust status text or accent tones if a particular pairing does not meet the requirement.

---

## 4. Typography

**Recommended font:** `Roboto` (the Android default and a reliable choice for the MVP). `Inter` is an optional alternative if properly licensed and included in the project. Readability takes priority over decorative styling.

| Style | Size / Line height | Weight | Example |
|---|---|---|---|
| App title | 26sp / 32sp | Bold | `Nubmark` |
| Screen title | 22sp / 28sp | SemiBold | `My Collection` |
| Section title | 18sp / 24sp | SemiBold | `Recently Updated` |
| Kit name | 16sp / 22sp | SemiBold | `VX-03 Arden` |
| Body | 14sp / 20sp | Regular | Descriptions and details |
| Supporting text | 12sp / 16sp | Regular / Medium | Grade, scale, dates |
| Statistic | 28–32sp / 34–38sp | Bold | `42 Kits`, `72%` |
| Navigation label | 11–12sp / 16sp | Medium | `Home`, `Collection` |

- Use **sp** text sizes so content respects the user's Android font-size setting.
- Limit kit names in grid cards to one or two lines, using ellipsis for overflow.
- Maintain clear typographic hierarchy; not every label needs to be bold.

---

## 5. Layout & Components

### Spacing, shapes, and elevation

| Token | Recommended value |
|---|---|
| Base spacing | 4dp |
| Screen horizontal padding | 16dp |
| Section vertical spacing | 20–24dp |
| Card internal padding | 12–16dp |
| Spacing between grid cards | 12dp |
| Card corner radius | 16dp |
| Small chip/badge radius | Pill / fully rounded |
| Button corner radius | 12dp |
| Bottom sheet top corners | 24dp |
| Border | 1dp `outline`, when needed |
| Elevation | 0–2dp, subtle |
| Minimum touch target | 48 × 48dp |

### Reusable components

- **KitCard:** Image with `ContentScale.Crop`, kit name, grade/scale, status badge, and a progress bar when the kit is `Building`.
- **StatusBadge:** Pill with a label and optional icon; variants: `Backlog`, `Building`, `Completed`.
- **StatTile:** Large value and concise label; used for total kits, backlog, building, and completed counts.
- **ProgressBar:** Rounded blue bar, always accompanied by a numeric value.
- **ProgressRing:** Circular indicator for the build progress page, with a readable percentage in the center.
- **FilterChip:** `All`, `Backlog`, `Building`, `Completed`; selected state uses a soft blue tint.
- **QuickActionTile:** Outline icon with a short label such as `Collection`, `Wishlist`, `Progress`, or `Analytics`.
- **EmptyState:** Simple icon/illustration, concise headline, one line of guidance, and one clear CTA.
- **PhotoPlaceholder:** Graceful fallback for kits without photos; never show a broken image.
- **ConfirmationDialog:** Used for deleting kits, deleting data, or other irreversible actions.

### Images and photography

- Make photos prominent in cards and detail pages, with consistent cropping.
- Suggested aspect ratios: **4:3** for hero images and **1:1 or 4:5** for grid cards (choose one card ratio and apply it consistently).
- Apply a subtle scrim/overlay when placing text on top of photography.
- Do not bundle copyrighted official franchise imagery without permission. The primary flow should support **photos provided by users**.

---

## 6. Information Architecture

```text
Nubmark
├── Home
│   ├── Collection summary
│   ├── At a Glance
│   ├── Quick Access
│   └── Recently Updated
├── Collection
│   ├── Filter: All / Backlog / Building / Completed
│   ├── Search & Sort
│   ├── Add / Edit Kit
│   └── Kit Detail
│       ├── Overview
│       ├── Build Log
│       ├── Photos
│       └── Notes
├── Wishlist
│   ├── Wishlist items
│   └── Add / Edit / Move to Collection
├── Builds
│   ├── Active Builds
│   └── Build Progress
│       ├── Stages
│       ├── Update status
│       └── Photos & notes
└── Profile
    ├── Collection statistics (MVP+)
    ├── Preferences
    └── About Nubmark
```

### Bottom navigation

Use the order shown in the approved mockup:

1. **Home** — `home` icon.
2. **Collection** — `inventory_2` / box icon.
3. **Wishlist** — `bookmark` icon.
4. **Builds** — `build` / wrench icon.
5. **Profile** — `person` icon.

Use Material 3 `NavigationBar`. Active items should use blue icon/label styling with a soft blue selection indicator; inactive items use secondary coloring. Never nest two bottom navigation bars on one screen.

---

## 7. Screen Specifications

### 7.1 Home — Dashboard

**Purpose:** Provide an immediate overview of the collection and shortcuts to current builds.

**Content order (top to bottom):**

1. App bar: `Nubmark` and an optional notification icon (may be omitted in the MVP).
2. Greeting: `Good morning!` or an appropriate time-based greeting, followed by `Ready to build something today?`.
3. **My Collection** summary hero: `Total Kits` and a featured kit photo when available.
4. Three **StatTiles**: `Backlog`, `Building`, `Completed`.
5. **At a Glance:** Completed-build summary; the monthly chart may be deferred for the MVP.
6. **Quick Access:** Collection, Wishlist, Progress, Analytics. Hide Analytics or show a clearly labeled placeholder until it is implemented.
7. **Recently Updated:** One to three recently changed kits, with progress for active builds.
8. Bottom navigation.

**Key interactions:** Tapping a status tile opens Collection with the relevant filter. Tapping a recently updated item opens Kit Detail. Quick actions navigate to the corresponding feature.

**Empty state:** `Your hangar is empty` with an **Add Your First Kit** CTA. Do not display fabricated counts or charts.

### 7.2 Collection — Grid & Filters

**Purpose:** Browse and manage all owned kits.

**Elements:**

- App bar with page heading, search, and sorting/filter actions.
- Horizontally scrollable filter chips: `All (n)`, `Backlog (n)`, `Building (n)`, `Completed (n)`.
- Two-column `LazyVerticalGrid` on standard phone widths, with consistent image-card proportions.
- Floating add button or prominent **Add Kit** action.

**KitCard content:** Photo, name, grade/scale (for example, `HG · 1/144`), status badge, and a progress bar for `Building` kits.

**Interactions:** Tap a card to open Kit Detail. Swipe actions are not required for the MVP. An optional `⋮` menu can expose Edit/Delete. Search and status filters must work together.

**Empty states:** `No kits yet` or `No kits match this filter`, with an option to clear filters where relevant.

### 7.3 Kit Detail — Overview, Build Log, Photos, Notes

**Purpose:** A single source of information for each owned kit.

**Layout:**

1. Hero photo gallery (swipeable if multiple images exist).
2. Kit name, grade, scale, series, and status badge.
3. Tabs: `Overview`, `Build Log`, `Photos`, `Notes`.
4. **Overview:** Metadata and a progress summary when the kit is being built.
5. Contextual actions: **Update Build** and **Add Photo**.

**Minimum metadata:** Kit name, grade, scale, optional series, optional acquisition date, and status. Optional purchase price should not dominate the page.

**Build Log:** Dated entries with notes and optional photos.\
**Photos:** Gallery of the kit and its assembly progress.\
**Notes:** Free-form notes about tools, paint colors, modifications, and building experience.

**Interactions:** Edit kit data, change status, and open photos in full screen. Prefer bottom sheets for lightweight actions instead of stacking dialogs.

### 7.4 Build Progress — Checklist

**Purpose:** Make assembly milestones clear and satisfying to track.

**Layout based on the approved mockup:**

1. Header featuring kit photo, name, grade/scale, and `Building` status.
2. **ProgressRing** and metadata: start date, optional target completion date, and elapsed time.
3. **Build Stages** heading with `x of y completed`.
4. Stage checklist, optionally expandable to show notes/photos (expansion can be deferred for MVP).

**Suggested default stages:**

1. Unboxing & Prep
2. Frame / Inner Build
3. Armor Assembly
4. Weapons & Equipment
5. Detailing (Panel Line / Decals)
6. Topcoat & Finish
7. Final Photos

These stages are a **template, not a mandatory workflow**: not all kits have an inner frame or require a topcoat. Future versions may allow users to reorder, customize, or skip stages.

**Progress calculation:** `completedStages / totalApplicableStages × 100`, rounded consistently. The percentage must match the checklist. If no applicable stages have been saved, show `0%` rather than a fabricated value.

**Completion behavior:** When all applicable stages are checked, offer **Mark as Completed**. Do not force an automatic status change; users should be able to review their work first.

### 7.5 Wishlist

**Purpose:** Save desired kits without counting them as owned items in `My Collection`.

**Elements:** Photo cards/grid (optional images), name, grade, scale, optional priority, optional estimated price, and an **Add to Collection** action.

**Interactions:** Add/edit/delete wishlist items. Once purchased, **Move to Collection** and default their status to `Backlog` (or let the user confirm a different status).

**Empty state:** `Your wishlist is empty` with **Add a Kit**.

### 7.6 Profile & Statistics (MVP+)

**Purpose:** Provide app preferences and personal collection insights.

**MVP:** A profile/settings area without requiring an account, basic preferences, and an About page.\
**Later:** Collection breakdown by grade, build completion charts, optional cost totals, and export/import backups.

---

## 8. Interaction & Motion

Animation should improve clarity and feedback rather than exist for decoration.

| Interaction | Recommendation |
|---|---|
| Tab/filter selection | Material 3 transitions, 150–250ms |
| Kit card → detail | Shared visual continuity if stable; otherwise standard navigation |
| Progress update | Animate progress bar/ring, 250–400ms |
| Checklist toggle | State change with subtle scale/color transition |
| Save operation | Brief snackbar: `Kit saved` / `Progress updated` |
| Destructive action | Confirmation dialog; Undo when feasible |
| Loading | Lightweight skeleton or progress indicator; avoid prolonged spinners |

Respect device motion preferences where available, and never block input solely to finish an animation.

---

## 9. UX States & Accessibility

Every screen that loads data should handle at least:

- **Loading:** An indicator that does not cause major layout shifts.
- **Success/content:** Real user data, not sample items or counts left over from the mockup.
- **Empty:** Brief explanation and a useful CTA.
- **Error:** Clear message and **Retry** action where appropriate.

### Accessibility checklist

- Minimum touch targets of **48dp**.
- Support font scaling; test layouts at approximately **1.3×–2.0×**.
- Provide accessible labels/content descriptions for icon-only actions.
- Communicate statuses through **text and color**, never color alone.
- Support TalkBack semantics for kit cards and progress stages.
- Verify text contrast, especially on blue/green badges and text over photos.
- Support narrow and large phone screens. Consider a single-column grid when large fonts leave insufficient width.

---

## 10. Implementation Mapping — Jetpack Compose

| Design element | Compose recommendation |
|---|---|
| App theme | `MaterialTheme(colorScheme, typography, shapes)` |
| Main scaffold | `Scaffold` + `NavigationBar` |
| Screen navigation | Navigation Compose |
| Content layout | `LazyColumn`, `LazyVerticalGrid`, `Row`, `Column` |
| Cards | `Card` / subtly styled `ElevatedCard` |
| Tabs & filters | `TabRow`, `FilterChip` |
| Progress | `LinearProgressIndicator`, `CircularProgressIndicator` |
| Add / Edit | Dedicated Compose form screen or modal bottom sheet |
| Images | Android Photo Picker + Coil `AsyncImage` |
| State management | `ViewModel` + `StateFlow` |
| Persistence | Room, offline-first |
| Preferences | DataStore (optional) |
| Icons | Material Symbols / Material icons with a consistent visual weight |

### Suggested package organization

```text
id.my.chromazone.nubmark
├── core
│   ├── design
│   │   ├── Color.kt
│   │   ├── Type.kt
│   │   ├── Shape.kt
│   │   └── Theme.kt
│   ├── navigation
│   └── ui
│       ├── components
│       └── states
├── feature
│   ├── home
│   ├── collection
│   ├── kitdetail
│   ├── builds
│   ├── wishlist
│   └── profile
└── data
    ├── local
    ├── model
    └── repository
```

This is a **suggested code organization**, not a requirement for multiple Gradle modules. A single `:app` module is sufficient for the MVP.

### Suggested Compose design tokens

```kotlin
val NubmarkBlue = Color(0xFF3B82F6)
val NubmarkNavy = Color(0xFF172338)
val NubmarkBackground = Color(0xFFFFFFFF)
val NubmarkSurfaceAlt = Color(0xFFF3F6FB)
val NubmarkOutline = Color(0xFFE2E8F0)
val NubmarkSuccess = Color(0xFF22C55E)

val NubmarkCardShape = RoundedCornerShape(16.dp)
val NubmarkButtonShape = RoundedCornerShape(12.dp)
```

Define colors and shapes centrally in theme/token files. **Avoid hardcoding colors in individual Composables.**

---

## 11. MVP Screen Priority

| Priority | Screen / Feature | Expected result |
|---|---|---|
| P0 | Theme & reusable components | Consistent light UI matching the approved concept |
| P0 | Collection + Add/Edit Kit | CRUD operations with locally stored kit photos |
| P0 | Kit Detail | Metadata, status, and photos |
| P0 | Build Progress | Stage checklist with accurate progress calculation |
| P0 | Home summary | Status counts and recently updated kits |
| P1 | Wishlist | Wishlist management and move-to-collection workflow |
| P1 | Build Log & Notes | Per-kit progress notes |
| P2 | Analytics / charts | Build activity and collection statistics visualizations |
| P2 | Export/import, backup, dark theme | Post-MVP enhancements |

### Definition of done — MVP UI

- [ ] The application follows the **white/light theme with subtle blue accents** shown in the approved mockup.
- [ ] Typography, spacing, corner radii, icon style, and labels are consistent across screens.
- [ ] Bottom navigation opens the correct five sections; unfinished features use honest empty/coming-soon states.
- [ ] Every collection card opens a detail view, photos are not distorted, and status labels are clear.
- [ ] `Backlog`, `Building`, and `Completed` accurately reflect persisted user data.
- [ ] Progress percentages match the applicable stage checklist.
- [ ] Home does not show misleading mock counts or sample photos for an empty collection.
- [ ] Layout handles status bars, navigation bars, the keyboard, and font scaling.
- [ ] Loading, empty, and error states are implemented for essential flows.

---

## 12. Do / Don't

**Do**

- Use whitespace, kit photography, rounded cards, blue accents, and a clear text hierarchy.
- Make browsing the collection feel like exploring a personal gallery.
- Give immediate feedback when a kit, status, or progress change is saved.
- Add subtle hobby references, such as nipper/runner icons and builder terminology.

**Don't**

- Do not switch the default visual direction to dark cyberpunk or a neon hangar theme.
- Do not overuse glassmorphism, gradients, or heavy visual effects.
- Do not present invented charts or sample counts as real user data.
- Do not include wishlist items in owned-collection totals.
- Do not require login before accessing the application's core features.

---

## 13. Source of Truth & Future Changes

1. **User-approved decision:** The **first, white/clean design** is the primary visual reference.
2. **Reference image:** `nubmark_android_app_showcase.png` communicates the visual direction, not immutable pixel-level measurements.
3. **This document (`DESIGN.md`):** The implementation-oriented design specification for consistent UI/UX development.
4. Any substantial changes to the theme, navigation, or core product features should be reflected in this document before implementation.

**Note:** The numbers, kit names, dates, and mecha designs in the concept mockup are illustrative. Production content must come from the user's own collection.
