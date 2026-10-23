"use client"

type SkillMatch = {
  skill?: string
  found?: boolean
  match?: number
  source?: string
}

type Analysis = {
  overallScore?: number | null
  role?: string
  fileName?: string
  experience?: {
    years?: number | null
    known?: boolean
    relevance?: number | null
    relevanceLabel?: string
  }
  education?: { degree?: string | null; match?: number | null }
  keywords?: { found?: number | null; missing?: number | null }
  atsScore?: number | null
  atsBreakdown?: Record<string, { passed?: boolean; weight?: number }>
  skillMatches?: SkillMatch[]
}

function safeScore(value: unknown): number | null {
  if (typeof value !== "number" || !Number.isFinite(value)) return null
  return Math.max(0, Math.min(100, Math.round(value)))
}

function displayScore(value: unknown): string {
  const score = safeScore(value)
  return score === null ? "—" : `${score}%`
}

export function ScoreCard({ analysis }: { analysis: Analysis }) {
  const overall = safeScore(analysis?.overallScore)
  const ats = safeScore(analysis?.atsScore)
  const experienceYears = analysis?.experience?.years
  const yearsKnown =
    analysis?.experience?.known === true ||
    (typeof experienceYears === "number" && Number.isFinite(experienceYears))
  const experienceText = yearsKnown && typeof experienceYears === "number"
    ? `${experienceYears.toFixed(experienceYears % 1 === 0 ? 0 : 1)} ${experienceYears === 1 ? "year" : "years"}`
    : "Not detected"
  const roleCoverage = safeScore(analysis?.experience?.relevance)
  const educationMatch = safeScore(analysis?.education?.match)
  const skillMatches = Array.isArray(analysis?.skillMatches) ? analysis.skillMatches : []
  const matchedCount = skillMatches.filter((item) => item?.found === true).length
  const requiredCount = skillMatches.length
  const keywordsFound = typeof analysis?.keywords?.found === "number"
    ? analysis.keywords.found
    : matchedCount
  const keywordsMissing = typeof analysis?.keywords?.missing === "number"
    ? analysis.keywords.missing
    : Math.max(0, requiredCount - matchedCount)
  const atsChecks = Object.entries(analysis?.atsBreakdown ?? {})

  return (
    <section className="rounded-2xl border border-blue-100 bg-white p-5 shadow-sm sm:p-6">
      <div className="mb-5 flex items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="text-sm font-medium text-slate-500">Resume Score</p>
          <h2 className="mt-1 text-xl font-bold text-slate-900">{analysis?.role || "Resume analysis"}</h2>
          {analysis?.fileName && (
            <p className="mt-1 truncate text-xs text-slate-500" title={analysis.fileName}>
              {analysis.fileName}
            </p>
          )}
        </div>
        <div className="flex h-16 w-16 shrink-0 flex-col items-center justify-center rounded-full border-4 border-blue-100 bg-blue-50">
          <span className="text-xl font-bold text-blue-800">{overall ?? "—"}</span>
          <span className="text-[10px] text-slate-500">/ 100</span>
        </div>
      </div>

      <div className="mb-5">
        <div className="mb-1 flex items-center justify-between text-sm">
          <span className="font-medium text-slate-700">Required skill coverage</span>
          <span className="font-semibold text-slate-900">{displayScore(overall)}</span>
        </div>
        <div className="h-2.5 overflow-hidden rounded-full bg-slate-100">
          <div className="h-full rounded-full bg-gradient-to-r from-blue-500 to-cyan-500 transition-all" style={{ width: `${overall ?? 0}%` }} />
        </div>
        <p className="mt-1 text-xs text-slate-500">Based on required skills detected in the extracted resume text.</p>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <Metric label="Professional experience" value={experienceText} detail="Employment only; internships and projects excluded" />
        <Metric label="Role-skill coverage" value={displayScore(roleCoverage)} detail="Skill evidence, not years of experience" />
        <Metric label="Education match" value={displayScore(educationMatch)} detail={analysis?.education?.degree || "Education not detected"} />
        <Metric label="Required skills detected" value={`${keywordsFound} found`} detail={`${keywordsMissing} not detected`} />
      </div>

      <div className="mt-4 rounded-xl border border-slate-200 bg-slate-50 p-4">
        <div className="flex items-center justify-between gap-3">
          <div>
            <h3 className="text-sm font-semibold text-slate-800">ATS readability estimate</h3>
            <p className="mt-1 text-xs text-slate-500">Checks extracted text and common resume sections. This is not a score from a real ATS.</p>
          </div>
          <span className="shrink-0 text-lg font-bold text-slate-800">{displayScore(ats)}</span>
        </div>
        {atsChecks.length > 0 && (
          <details className="mt-3">
            <summary className="cursor-pointer text-xs font-medium text-blue-700">View readability checks ({atsChecks.filter(([, check]) => check?.passed).length}/{atsChecks.length} passed)</summary>
            <ul className="mt-2 space-y-1.5">
              {atsChecks.map(([name, check]) => (
                <li key={name} className="flex items-center justify-between gap-3 text-xs">
                  <span className="text-slate-600">{name.replaceAll("_", " ")}</span>
                  <span className={check?.passed ? "font-medium text-emerald-700" : "font-medium text-amber-700"}>
                    {check?.passed ? "Passed" : "Needs review"}
                  </span>
                </li>
              ))}
            </ul>
          </details>
        )}
      </div>
    </section>
  )
}

function Metric({ label, value, detail }: { label: string; value: string; detail: string }) {
  return (
    <div className="min-w-0 rounded-xl border border-slate-100 bg-slate-50 p-3">
      <p className="text-xs font-medium text-slate-500">{label}</p>
      <p className="mt-1 break-words text-base font-semibold text-slate-900">{value}</p>
      <p className="mt-1 line-clamp-2 text-xs text-slate-500" title={detail}>{detail}</p>
    </div>
  )
}
