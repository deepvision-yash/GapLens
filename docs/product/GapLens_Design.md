# GapLens — Product UI & Design Implementation Specification

> **Purpose:** This is the single UI implementation brief for the coding agent. Build the GapLens frontend directly from this document. Do not use Stitch or wait for additional screen prompts.
>
> **Product:** GapLens — AI Research Intelligence & Information Gap Analysis  
> **Tagline:** *See what's missing. Verify what matters.*  
> **Primary experience:** A focused research workspace that turns a question and its sources into traceable claims, coverage gaps, conflicts, freshness signals, and a practical verification plan.

---

## 1. Instructions to the coding agent

You are acting as a senior product designer and senior frontend engineer. Implement a complete, cohesive, production-quality interface — not a wireframe, generic admin dashboard, or collection of disconnected cards.

### Mandatory working rules

1. **Inspect the existing repository before changing anything.** Identify the current framework, routes, components, installed UI libraries, linting rules, and existing design files.
2. **If `design.md` exists, it is the source of truth for design tokens.** Read it first. Preserve its exact colors, typography, spacing, radii, shadows, and other tokens. Do not replace or reinterpret them. If a token is missing, extend the system minimally and consistently.
3. Use the existing project stack and conventions. Do not migrate frameworks or replace working infrastructure just to match this brief.
4. Build the six-screen product flow in this document as one connected application with shared navigation, reusable components, and realistic interaction.
5. Do not stop after creating a landing page. Implement the research input, scope review, processing, intelligence dashboard, evidence explorer, and verification workspace.
6. Do not invent backend results and present them as real. Until API integration exists, use clearly labelled demo/sample data behind a typed mock-data layer. Keep the UI ready to swap to real API responses.
7. Avoid fake controls. Every visible button, tab, filter, menu, upload action, source link, checklist checkbox, and navigation item must work or be visibly disabled with a clear reason.
8. Do not add features outside the product scope just to fill space. Prioritize clarity, evidence traceability, and task completion.
9. Use semantic HTML, accessible labels, keyboard navigation, visible focus states, and responsive layouts.
10. After implementation, run the available checks (typecheck, lint, tests, build) and fix issues caused by your changes.

### Visual quality bar

The result should feel like a carefully art-directed research product: calm, confident, precise, editorial, and technically sophisticated. Use a **NotebookLM-inspired dark research workspace combined with the clarity and precision of Google AI Studio**. This is a direction, not permission to copy either product.

Avoid:
- Generic SaaS dashboard templates.
- Purple/blue AI gradients everywhere.
- Glassmorphism on every surface.
- Excessive rounded cards and pill badges.
- Huge hero typography that pushes the task below the fold.
- Decorative charts with no analytical meaning.
- Dense walls of metadata.
- Emoji as the primary icon system.
- Random stock photos or illustrations.
- Fake live metrics, fake citations, or fabricated source credibility.

The product should look excellent at desktop widths first, while remaining fully usable on tablet and mobile.

---

## 2. Product principles

Every screen must reinforce these principles:

### 2.1 Evidence before assertion
A finding should be traceable to one or more sources. A user must be able to move from a claim to the exact supporting excerpt and original source.

### 2.2 Separate facts from analysis
Do not visually blur:
- Extracted claims.
- Verified claims.
- Potential findings.
- Uncertain findings.
- AI-generated hypotheses or suggested research dimensions.

### 2.3 Make gaps actionable
A gap is not merely an alert. Show why it matters and what the user can do to resolve it.

### 2.4 Progressive disclosure
Show the most important information first. Put source metadata, long excerpts, technical details, and secondary controls behind drawers, expandable rows, or detail views.

### 2.5 One primary task per screen
- Home: start research.
- Scope: confirm what to investigate.
- Processing: understand progress.
- Intelligence: understand findings.
- Evidence: inspect provenance.
- Verification: complete next actions.

### 2.6 Trustworthy uncertainty
Never imply certainty where the evidence is incomplete. Do not turn an LLM confidence score into a verification badge.

---

## 3. Design system

### 3.1 Token authority

Before writing styles, inspect `design.md` and the current theme configuration.

- Reuse the existing CSS variables or Tailwind theme tokens.
- Do not hardcode a second palette in components.
- Do not create competing spacing or typography systems.
- If `design.md` is absent, derive a compact token set from the existing app styles and document the additions in one central theme file.
- All components must consume shared tokens.

### 3.2 Visual direction

**Primary mode:** dark interface.

**Character:** focused research desk, editorial information architecture, quiet technical precision.

**Surface hierarchy:**
1. App canvas — deepest background.
2. Navigation/sidebar — slightly differentiated from canvas.
3. Main working surface — clear content plane.
4. Raised surface — only for meaningful interactive groupings.
5. Overlay surface — dialogs, popovers, drawers.

Use subtle borders and tonal separation before using shadows. Reserve high-contrast accent color for primary actions, active navigation, selected states, and important analytical signals.

### 3.3 Color semantics

Use the existing design tokens where defined. Map semantic states consistently:

| Meaning | Visual treatment |
|---|---|
| Verified | Restrained green; never use it for an unverified AI claim |
| Potential | Amber / warm warning tone |
| Uncertain | Neutral or muted slate |
| Conflict | Red / coral warning tone |
| Missing | Neutral outline or muted warning tone |
| Outdated | Muted orange / amber |
| Primary action | Existing brand accent |
| Disabled | Low-contrast but still readable |

Color must never be the only way to communicate status. Pair color with a label and, where useful, an icon.

### 3.4 Typography

Use the typography already defined in `design.md`. Establish a clear hierarchy:
- Page title: strong, compact, readable.
- Section heading: clear but subordinate.
- Body: comfortable reading size and line-height.
- Metadata: smaller and muted, but accessible.
- Evidence excerpt: optimized for long-form reading.
- Numeric values: use tabular numerals when supported.

Avoid oversized headings and excessively tiny metadata.

### 3.5 Shape, borders, and elevation

Follow existing radius and border tokens. Prefer:
- Subtle 1px separators.
- Consistent control heights.
- Compact but breathable spacing.
- Small radii for controls and data surfaces.
- Larger radius only for major containers or overlays.

Do not wrap every section in a card. Use page background, whitespace, section headings, and dividers to create hierarchy.

### 3.6 Iconography

Use the icon library already installed in the repository. If none exists, use one consistent line-icon library such as Lucide. Do not mix icon families. Icons should clarify actions or categories, not decorate every label.

---

## 4. Application information architecture

### 4.1 Shared application shell

Create a persistent shell for all authenticated/research workspace routes.

**Left sidebar**
- GapLens mark + wordmark.
- Primary action: **New Research**.
- Navigation:
  - Home
  - Research history
  - Saved sources
  - Verification tasks
- Bottom area:
  - Settings
  - Help / documentation
  - User/profile area only if authentication already exists.

**Sidebar behavior**
- Desktop: fixed-width expanded sidebar; support collapse if straightforward.
- Tablet: collapsible sidebar.
- Mobile: off-canvas navigation opened by a menu button.
- Active route has a clear but restrained visual state.
- New Research remains visually prominent without overpowering navigation.

**Top workspace bar**
- Breadcrumb or current workspace title.
- Contextual actions only (for example, export or share if implemented).
- Do not fill the header with global search, notifications, profile controls, and filters unless those features exist.

**Main content**
- Use a consistent max-width and alignment system.
- Keep primary content centered in the available workspace.
- Dashboard may use wider content than input screens.
- Avoid horizontal overflow.

### 4.2 Routes

Use the routing conventions already present. Recommended logical routes:

```text
/
 /research/new
 /research/[id]/scope
 /research/[id]/processing
 /research/[id]
 /research/[id]/evidence/[claimId]   (drawer or nested detail)
 /tasks
 /history
 /sources
 /settings
```

If the existing repository uses different route conventions, preserve them while implementing the same experience.

---

## 5. Screen 01 — Research Home

**User question:** “What do I want to investigate?”

**Goal:** Let the user begin a research session immediately, without setup friction.

### Layout

- Shared app shell.
- A compact page introduction:
  - Title: **Start a research session**
  - Supporting sentence: “Bring a question. GapLens maps the evidence, finds what is missing, and shows what to verify next.”
- Main research composer as the dominant element.
- Optional source attachment area beneath or inside the composer.
- A small recent research section below the composer.

### Research composer

- Label: **What do you want to investigate?**
- Large multiline text area with a useful example placeholder, e.g.:
  “Compare the current eligibility rules, deadlines, and required documents for [programme] in India.”
- Do not use a chat-bubble visual treatment. This is a research brief, not a chatbot.
- Primary CTA: **Continue to scope**.
- Validate that the goal is not empty.
- Show a character count only if there is a real input limit.

### Optional source input

Support both automatic discovery and user-provided material:
- Add URL(s).
- Upload documents: PDF, DOCX, TXT.
- Allow multiple URLs/files.
- Show compact source chips/rows with filename or hostname, type, and remove action.
- Show upload progress, success, and error states.
- Do not show a large selected-sources panel on the right.
- Clearly communicate: adding sources is optional; web research is still part of the normal workflow.

### Recent research

- Show a short list of recent sessions if data exists.
- Each row: research title, last updated, concise status.
- Empty state should guide the user to start the first session.
- Do not invent historical sessions in production. Use labelled demo fixtures only in demo mode.

### Interactions

- Continue to scope creates or prepares the session and navigates to Screen 02.
- URL addition validates URL syntax and allows removal.
- File picker supports the accepted types and shows unsupported-file errors.
- Recent session row opens its session.

### Avoid

- Giant marketing hero.
- Decorative product screenshots that push the composer down.
- Multiple competing CTA buttons.
- Search mode selectors. Automatic web search is part of the research flow.

---

## 6. Screen 02 — Research Scope

**User question:** “Is GapLens investigating the right things?”

**Goal:** Let users review and adjust the AI-understood research objective and dimensions before expensive research begins.

### Layout

- Breadcrumb: Home / New Research / Review scope.
- Compact title: **Review your research scope**.
- One-sentence explanation that these dimensions guide the research.
- Main column contains objective and dimensions.
- Optional small context panel for attached sources / research settings only if it genuinely helps.

### Sections

**A. Interpreted objective**
- Display the normalized research objective.
- Allow inline edit.
- Preserve the user's original prompt for reference if useful.
- Make it clear that this is an interpretation, not a confirmed fact.

**B. Research dimensions**
- Display approximately 5–10 generated dimensions as an editable list.
- Each dimension has:
  - Name.
  - One-line description / question it will investigate.
  - Edit action.
  - Remove action.
- Add dimension action.
- Support reordering if practical.
- Avoid a grid of oversized cards. Use clean rows or compact grouped panels.

Example dimensions for a scholarship research goal:
- Eligibility and applicant categories.
- Application deadlines and cycle.
- Required documents.
- Financial benefits and coverage.
- Renewal conditions.
- Official application process.

**C. Scope controls**
- Optional geography, time period, language, or constraints only where supported by the product/API.
- Do not add fake controls that are not persisted or used.

### Footer actions

- Secondary: **Back**.
- Primary: **Start research**.
- If scope changes are pending, preserve them when starting.
- Show a concise confirmation/loading state to prevent duplicate submissions.

### States

- Loading while goal understanding runs.
- Error with retry if interpretation fails.
- Empty dimensions with add-dimension action.
- Validation if all dimensions are removed.
- Unsaved edits indicator if navigation can lose changes.

---

## 7. Screen 03 — Research in Progress

**User question:** “What is happening, and is the research making progress?”

**Goal:** Make the pipeline understandable and reassuring without pretending every stage is instantaneous or successful.

### Layout

- Compact research title and status.
- Main progress area with current stage and concise explanation.
- Vertical stage timeline.
- Live activity feed or source processing list below/alongside only when useful.

### Pipeline stages

Represent the actual backend stages. Suggested user-facing grouping:

1. Understanding research goal.
2. Building research dimensions.
3. Planning search queries.
4. Discovering sources.
5. Extracting source content.
6. Extracting claims.
7. Checking evidence and coverage.
8. Detecting gaps and conflicts.
9. Preparing verification checklist.

The backend may have more granular stages; map them into these understandable labels without falsifying progress.

### Stage item states

- Pending.
- Running.
- Completed.
- Partial.
- Failed / needs attention.

Each stage shows:
- Stage label.
- Short explanation.
- State indicator.
- Real counts only when supplied by backend.
- Error detail only when actionable.

### Progress behavior

- Connect to the real progress stream (SSE or existing transport).
- Reconnect safely after refresh.
- Fetch current session status after reconnect.
- Never fabricate a percentage if backend does not provide meaningful progress.
- If percentage is unavailable, use stage-based progress rather than a fake numeric meter.
- Source failures should be shown as source-level warnings where the overall session can continue.

### Completion

- Clear completion state.
- Primary CTA: **View research findings**.
- If results are partial, explicitly label them partial and show what could not be completed.
- Failed sessions offer retry where supported.

### Avoid

- Fake terminal logs.
- Rapidly cycling “AI thinking” animations.
- A spinner with no explanation.
- Pretending a failed source means the entire analysis failed.

---

## 8. Screen 04 — Research Intelligence Dashboard

**User question:** “What did we discover, what is missing, and what needs attention?”

This is the core product screen. It must be the most carefully designed and polished view.

### Header

- Research title.
- Status: Completed / Partial.
- Research date and concise scope summary.
- Actions: rerun or export only if implemented.
- Avoid a crowded action toolbar.

### Dashboard navigation

Use a compact tab row or section navigation:
- Overview
- Coverage
- Gaps
- Conflicts
- Sources & Evidence
- Verification

Keep navigation labels understandable. Tabs must change the displayed content or navigate to the relevant section.

### Overview section

At the top, show a concise **Research brief**:
- One or two sentence summary of the research result.
- Explicitly label it as AI-generated synthesis.
- Link to relevant evidence where possible.

Then show a restrained row of key counts:
- Sources reviewed.
- Claims extracted.
- Gaps identified.
- Conflicts detected.

Only render values returned by the API. Counts are secondary context, not the main experience.

### Coverage analysis

This is a key differentiator. Build a clear research-dimension coverage matrix/list.

Each dimension row should show:
- Dimension name.
- Status: Covered / Partial / Missing / Conflicting / Outdated / Weak evidence.
- Brief explanation.
- Evidence count if available.
- Action to inspect evidence or related gaps.

Use a table/list rather than a wall of cards. Make status scannable with text plus semantic color.

Provide filters only if the list is long enough to justify them. Keep the default view simple.

### Information gaps

Each gap item should answer:
1. What information is missing?
2. Which research dimension does it affect?
3. Why does it matter?
4. What evidence was searched or found?
5. What should the user check next?

Gap item anatomy:
- Short, specific title.
- Severity / priority label.
- Dimension.
- One-to-three sentence explanation.
- Evidence context or “no direct evidence found” statement.
- Suggested next action.
- Link to related sources/claims.

Do not label every absence as a proven gap. Use “potential gap” or “unresolved” where the search coverage is incomplete.

### Conflicts

Conflict items must show both sides, not just a warning headline.

For each conflict:
- Claim A.
- Claim B.
- Source for each claim.
- Publication/update dates where known.
- Context differences (time, geography, definition, population) if identified.
- Classification: genuine / temporal / contextual / definitional / jurisdictional / uncertain.
- Suggested resolution action.

Visually distinguish the two claims with a balanced comparison layout. Do not imply that one source is correct unless the evidence supports that conclusion.

### Freshness

Show freshness only where dates and context support it:
- Current.
- Aging.
- Outdated.
- Expired.
- Undated.
- Future-dated / suspicious.

Include date and reason. Do not treat a missing date as proof that information is outdated.

### Evidence quality and source reliability

Keep these concepts separate:
- Claim verification status.
- Evidence type / support strength.
- Source authority/reliability signal.
- Source freshness.
- Model confidence (if present).

Do not collapse these into one score or one “trust” badge.

### Dashboard hierarchy

Recommended order:
1. Research brief.
2. High-priority unresolved findings.
3. Coverage matrix.
4. Gaps and conflicts.
5. Freshness / evidence notes.
6. Source collection.

Avoid showing six metric cards, multiple charts, and several repeated summaries above the fold. The dashboard should feel like a research report, not a KPI dashboard.

---

## 9. Screen 05 — Evidence Explorer

**User question:** “Where did this claim come from, and can I inspect the evidence?”

**Goal:** Give claim-level traceability without losing the user's place in the dashboard.

### Presentation

Prefer a right-side drawer on desktop and a full-screen detail view on mobile. It may have a route for deep linking, but the normal interaction should preserve dashboard context.

### Evidence detail

Display:
- Claim text.
- Claim status: verified / potential / uncertain / unverified as supplied by the analysis rules.
- Related research dimension.
- Exact supporting excerpt.
- Source title.
- Source domain.
- Publication date / last updated date / retrieval date, where available.
- Source type.
- Original URL with open-in-new-tab behavior.
- Other supporting claims.
- Contradicting claims, if any.
- Extraction / analysis notes only when useful.

### Excerpt handling

- Preserve exact source excerpt text.
- Highlight the exact sentence or phrase supporting the claim where offsets are available.
- Do not rewrite an excerpt and present it as a quote.
- If the excerpt is unavailable, say so clearly and do not fabricate one.
- Long source content should be expandable.

### Source provenance

Make the source link obvious and trustworthy. The user should be able to open the original source directly.

Show metadata in a compact definition-list layout rather than a dense grid of tiny chips.

### Interactions

- Open source URL.
- Navigate to related claim.
- Navigate to related conflict or gap.
- Close drawer and return to the previous dashboard state.
- Keyboard Escape closes the drawer.

---

## 10. Screen 06 — Verification Workspace

**User question:** “What should I verify next?”

**Goal:** Convert findings into an ordered, actionable checklist.

### Layout

- Title: **Verification checklist**.
- Short explanation: “Resolve the highest-impact uncertainties first.”
- Compact progress summary (completed / remaining).
- Main checklist grouped by priority.

### Checklist item anatomy

- Checkbox / completion control.
- Action-oriented task title.
- Priority: Critical / High / Medium / Low.
- Related research dimension.
- Why this matters.
- Recommended source or authority to consult.
- Suggested verification method.
- Supporting evidence links.
- Effort estimate only if supplied or reliably inferred and labelled.

### Behavior

- Mark complete / reopen.
- Persist status through API when available.
- Optimistic updates must roll back if the server rejects the change.
- Allow filtering by status or priority only if useful.
- Group by priority by default.
- Completed items should remain accessible, visually subdued, and not disappear unexpectedly.

### Empty states

- No checklist items: explain that no verification tasks were generated and link back to findings.
- All complete: show a clear completion state and a way to revisit completed tasks.

---

## 11. Reusable component inventory

Build reusable, typed components rather than screen-specific one-offs.

### Shell
- `AppShell`
- `Sidebar`
- `MobileNavigation`
- `TopBar`
- `Breadcrumbs`
- `PageHeader`

### Research creation
- `ResearchGoalComposer`
- `UrlInput`
- `SourceUpload`
- `AttachedSourceList`
- `RecentResearchList`

### Scope
- `ResearchObjectiveEditor`
- `DimensionList`
- `DimensionRow`
- `AddDimensionControl`

### Processing
- `ResearchStageTimeline`
- `StageStatus`
- `ProcessingActivity`
- `SourceProcessingRow`
- `PartialFailureNotice`

### Intelligence
- `ResearchSummary`
- `FindingCountRow`
- `CoverageMatrix`
- `CoverageStatus`
- `GapList`
- `GapItem`
- `ConflictComparison`
- `FreshnessIndicator`
- `SourceList`

### Evidence
- `EvidenceDrawer`
- `ClaimHeader`
- `EvidenceExcerpt`
- `SourceMetadata`
- `RelatedClaims`

### Verification
- `VerificationProgress`
- `VerificationTaskList`
- `VerificationTask`
- `PriorityLabel`

### Shared primitives
- Button variants.
- Text input / textarea.
- Select / combobox only where required.
- Tabs.
- Tooltip.
- Dialog.
- Drawer.
- Dropdown menu.
- Toast.
- Skeleton.
- Empty state.
- Error state.
- Status label.
- Divider.

Do not build a large custom component framework. Reuse the installed component library where it fits the design system.

---

## 12. Data and API integration contract

The UI must be backend-ready. Keep API calls and mapping logic out of presentation components.

### Suggested frontend domain types

```ts
type SessionStatus =
  | "created"
  | "understanding"
  | "scope_review"
  | "ready"
  | "searching"
  | "extracting"
  | "claim_extraction"
  | "analyzing"
  | "generating_checklist"
  | "completed"
  | "partial"
  | "failed";

type FindingStatus =
  | "verified"
  | "potential"
  | "uncertain"
  | "unverified";

type CoverageStatus =
  | "covered"
  | "partial"
  | "missing"
  | "conflicting"
  | "outdated"
  | "weak_evidence";

type FreshnessStatus =
  | "current"
  | "aging"
  | "outdated"
  | "expired"
  | "undated"
  | "future";

type SourceInput =
  | { kind: "url"; url: string }
  | { kind: "file"; file: File };

interface ResearchSession {
  id: string;
  title: string;
  goal: string;
  status: SessionStatus;
  createdAt: string;
  updatedAt: string;
  isPartial?: boolean;
}

interface ResearchDimension {
  id: string;
  name: string;
  description: string;
  coverageStatus?: CoverageStatus;
  claimCount?: number;
}

interface ResearchSource {
  id: string;
  title: string;
  url?: string;
  domain?: string;
  sourceType: string;
  publicationDate?: string;
  lastModified?: string;
  retrievalDate?: string;
  extractionStatus?: "pending" | "success" | "partial" | "failed";
}

interface EvidenceClaim {
  id: string;
  text: string;
  status: FindingStatus;
  dimensionId?: string;
  sourceId?: string;
  exactExcerpt?: string;
  confidence?: number;
  freshness?: FreshnessStatus;
}

interface ResearchGap {
  id: string;
  title: string;
  explanation: string;
  priority: "critical" | "high" | "medium" | "low";
  dimensionId?: string;
  relatedClaimIds: string[];
  nextAction?: string;
}

interface ResearchConflict {
  id: string;
  title: string;
  claimA: EvidenceClaim;
  claimB: EvidenceClaim;
  conflictType:
    | "genuine"
    | "temporal"
    | "contextual"
    | "definitional"
    | "jurisdictional"
    | "uncertain";
  resolutionAction?: string;
}

interface VerificationTask {
  id: string;
  title: string;
  priority: "critical" | "high" | "medium" | "low";
  explanation: string;
  completed: boolean;
  dimensionId?: string;
  sourceIds: string[];
  recommendedAuthority?: string;
  verificationMethod?: string;
}
```

Adapt names to the actual FastAPI response models. Do not force the backend to adopt frontend naming if an existing API contract is already defined; map API DTOs to UI domain types in one adapter layer.

### API endpoints to support

Use the actual backend routes if they already exist. The following are the intended product capabilities:

```text
POST   /api/research
POST   /api/research/{id}/sources
POST   /api/research/{id}/understand
GET    /api/research/{id}/scope
PATCH  /api/research/{id}/scope
POST   /api/research/{id}/start
GET    /api/research/{id}/events       # SSE
GET    /api/research/{id}/status
GET    /api/research/{id}/results
GET    /api/research/{id}/sources
GET    /api/research/{id}/claims
GET    /api/research/{id}/gaps
GET    /api/research/{id}/conflicts
GET    /api/research/{id}/checklist
PATCH  /api/research/{id}/checklist/{task_id}
```

### Data integrity rules

- Do not fabricate evidence excerpts, dates, source titles, URLs, source counts, or verification labels.
- Missing fields should render as “Not provided” or be omitted, depending on importance.
- A source extraction failure must not automatically mark every claim or session as failed.
- Partial results must be visibly labelled partial.
- A claim is not verified merely because an LLM extracted it.
- Keep source reliability, evidence support, freshness, and claim status independent.
- Use stable IDs from the backend; do not use array indexes as entity identity.

### Mock data

If the backend is not ready:
- Put mock records in a dedicated `mocks/` or `fixtures/` directory.
- Add an obvious development/demo mode switch or environment flag.
- Use a coherent single sample research session across every screen.
- Label sample data as **Demo data** in the UI.
- Never mix mock and live records in the same session.
- Keep all screen components compatible with the real domain types.

---

## 13. Interaction and motion

Motion should make state changes easier to understand, not make the product feel animated for its own sake.

Use restrained transitions for:
- Sidebar collapse/expand.
- Drawer open/close.
- Tab changes.
- Checklist completion.
- Upload progress.
- Loading skeleton transitions.
- Stage status changes.

Guidelines:
- Prefer short, subtle transitions.
- Respect `prefers-reduced-motion`.
- Avoid looping background animations.
- Avoid fake AI typing effects.
- Avoid animated charts unless the animation communicates a real change.

---

## 14. Responsive behavior

### Desktop
- Persistent sidebar.
- Main workspace uses available width.
- Evidence drawer overlays from the right.
- Coverage and conflict comparisons can use multiple columns where space supports them.

### Tablet
- Sidebar can collapse.
- Dashboard columns stack when needed.
- Keep tables readable; allow controlled horizontal scrolling only for genuinely tabular data.

### Mobile
- Off-canvas navigation.
- Single-column content.
- Research composer fills available width.
- Scope dimensions become compact list rows.
- Processing timeline remains vertical.
- Evidence drawer becomes a full-screen detail view.
- Conflict comparison stacks claim A and claim B.
- Checklist actions remain easy to tap.
- No hover-only interactions.
- Avoid horizontal page scrolling.

---

## 15. Accessibility and quality requirements

- Meet WCAG AA contrast where practical.
- All inputs have visible labels.
- All icon-only buttons have accessible names.
- All interactive controls are keyboard accessible.
- Focus indicators are visible and consistent.
- Use proper heading order.
- Use `aria-live` for meaningful processing status updates, not for every tiny counter change.
- Do not communicate state using color alone.
- Dialogs/drawers manage focus and return focus to the trigger.
- Respect reduced-motion preferences.
- Make error messages actionable and associated with the relevant field.

---

## 16. Loading, empty, error, and partial states

Every major screen must have designed states, not just a happy path.

### Loading
- Use skeletons that resemble the final layout.
- Avoid blank screens and indefinite spinners.
- Keep layout stable to prevent content jumps.

### Empty
- Explain why the section is empty.
- Provide one relevant next action.
- Avoid decorative empty-state illustrations that distract from the task.

### Error
- Explain what failed in plain language.
- Offer retry if safe.
- Preserve user input and completed work.
- Do not expose raw stack traces or API secrets.

### Partial
- Label the session or section as partial.
- Identify the affected stage/source.
- Preserve successful results.
- Explain what remains unresolved.

---

## 17. Suggested implementation sequence

Build in this order, but keep the shared design system coherent from the beginning.

1. Inspect repo and current `design.md`; establish token usage.
2. Implement app shell, sidebar, responsive navigation, and base primitives.
3. Implement Research Home and source attachment interactions.
4. Implement Scope Review and dimension editing.
5. Implement Processing screen and progress event adapter.
6. Implement Intelligence dashboard and coverage matrix.
7. Implement gaps and conflict views.
8. Implement Evidence Explorer drawer and source provenance.
9. Implement Verification Workspace and persisted task state.
10. Connect actual API endpoints or isolate demo fixtures.
11. Add loading, empty, error, partial, and responsive states.
12. Run lint, typecheck, tests, and production build.

Do not spend the entire implementation budget polishing the landing screen while the core research workflow remains unbuilt.

---

## 18. Acceptance criteria

The implementation is complete only when all of the following are true:

### Product flow
- [ ] A user can enter a research goal.
- [ ] A user can optionally add URLs and supported documents.
- [ ] The user can review and edit the interpreted objective and research dimensions.
- [ ] The user can start research and see meaningful progress states.
- [ ] The user can open the completed or partial research dashboard.
- [ ] The user can inspect a claim's exact excerpt and source provenance.
- [ ] The user can inspect coverage, gaps, conflicts, and freshness.
- [ ] The user can complete and reopen verification tasks.

### Visual quality
- [ ] All screens share one consistent design system.
- [ ] Existing `design.md` tokens are respected.
- [ ] Desktop layout feels intentional and polished.
- [ ] Mobile layout is usable without horizontal page overflow.
- [ ] The UI is not a generic card-based admin template.
- [ ] Typography, spacing, alignment, and component states are consistent.
- [ ] No decorative charts or fake metrics are present.

### Engineering quality
- [ ] Components are reusable and typed.
- [ ] API and mock-data layers are separated from presentation.
- [ ] No fake buttons or dead navigation items.
- [ ] Loading, empty, error, and partial states exist.
- [ ] Accessibility basics are implemented.
- [ ] Lint/typecheck/build pass, or pre-existing failures are documented separately.

---

## 19. Final direction

Build GapLens as a **serious evidence-research workspace**, not an AI chatbot with a dashboard attached.

The signature experience is the chain:

**Research question → scope → sources → claims → evidence → coverage → gaps/conflicts → verification actions.**

Every design decision should make that chain easier to understand and act on.

The most important screens are the Research Intelligence dashboard, Evidence Explorer, and Verification Workspace. Give those the same design attention as the first screen.

**Do not ask for another Stitch prompt. Use this document, inspect the existing repository, preserve the existing design tokens, and implement the complete connected UI.**
