"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Target, CheckCircle2, AlertCircle, Lightbulb, Briefcase } from "lucide-react"
import type { JDAnalysisResult } from "@/lib/types"

interface JDMatchCardProps {
  result: JDAnalysisResult
  onClear?: () => void
}

export function JDMatchCard({ result, onClear }: JDMatchCardProps) {
  const score = Math.max(0, Math.min(100, Math.round(result.jdScore ?? 0)))
  const matchedCount = result.matchedSkills?.length ?? 0
  const missingCount = result.missingSkills?.length ?? 0
  const totalCount = result.totalJdSkills || (matchedCount + missingCount)

  // Color theme based on relevance score
  const getScoreColor = (val: number) => {
    if (val >= 75) return "text-emerald-700 bg-emerald-50 border-emerald-200"
    if (val >= 40) return "text-amber-700 bg-amber-50 border-amber-200"
    return "text-rose-700 bg-rose-50 border-rose-200"
  }

  const getProgressColor = (val: number) => {
    if (val >= 75) return "from-emerald-500 to-teal-500"
    if (val >= 40) return "from-amber-500 to-orange-500"
    return "from-rose-500 to-red-500"
  }

  return (
    <Card className="rounded-2xl border border-sky-100 bg-white/95 backdrop-blur-sm shadow-md transition-all">
      <CardHeader className="flex flex-row items-start justify-between pb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-sky-100 text-sky-700">
              <Briefcase className="h-4 w-4" />
            </span>
            <div>
              <CardTitle className="text-lg font-bold text-slate-900">
                Job Description Relevance
              </CardTitle>
              <p className="text-xs text-slate-500">
                Direct comparison against your custom Job Description
              </p>
            </div>
          </div>
        </div>

        <div
          className={`flex h-14 w-14 shrink-0 flex-col items-center justify-center rounded-2xl border-2 ${getScoreColor(
            score
          )} shadow-xs`}
        >
          <span className="text-lg font-extrabold leading-none">{score}%</span>
          <span className="text-[9px] uppercase tracking-wider font-semibold opacity-80 mt-0.5">
            Match
          </span>
        </div>
      </CardHeader>

      <CardContent className="space-y-5">
        {/* PROGRESS BAR */}
        <div>
          <div className="mb-1 flex items-center justify-between text-xs">
            <span className="font-medium text-slate-600">JD Coverage Rate</span>
            <span className="font-semibold text-slate-800">
              {matchedCount} of {totalCount} requirements detected
            </span>
          </div>
          <div className="h-2 w-full overflow-hidden rounded-full bg-slate-100">
            <div
              className={`h-full rounded-full bg-gradient-to-r ${getProgressColor(
                score
              )} transition-all duration-500`}
              style={{ width: `${score}%` }}
            />
          </div>
        </div>

        {/* SUMMARY METRICS */}
        <div className="grid grid-cols-2 gap-3">
          <div className="rounded-xl border border-emerald-100 bg-emerald-50/60 p-3">
            <div className="flex items-center gap-1.5 text-xs font-semibold text-emerald-800">
              <CheckCircle2 className="h-3.5 w-3.5" />
              <span>Matched Skills ({matchedCount})</span>
            </div>
            <div className="mt-2 flex flex-wrap gap-1.5">
              {matchedCount > 0 ? (
                result.matchedSkills.map((skill, idx) => (
                  <span
                    key={idx}
                    className="inline-flex items-center rounded-md bg-white px-2 py-0.5 text-xs font-medium text-emerald-800 border border-emerald-200 shadow-2xs"
                  >
                    {skill}
                  </span>
                ))
              ) : (
                <span className="text-xs text-slate-500 italic">None detected</span>
              )}
            </div>
          </div>

          <div className="rounded-xl border border-amber-100 bg-amber-50/60 p-3">
            <div className="flex items-center gap-1.5 text-xs font-semibold text-amber-800">
              <AlertCircle className="h-3.5 w-3.5" />
              <span>Missing from Resume ({missingCount})</span>
            </div>
            <div className="mt-2 flex flex-wrap gap-1.5">
              {missingCount > 0 ? (
                result.missingSkills.map((skill, idx) => (
                  <span
                    key={idx}
                    className="inline-flex items-center rounded-md bg-white px-2 py-0.5 text-xs font-medium text-amber-800 border border-amber-200 shadow-2xs"
                  >
                    {skill}
                  </span>
                ))
              ) : (
                <span className="text-xs text-slate-500 italic">All requirements covered</span>
              )}
            </div>
          </div>
        </div>

        {/* TAILORED JD SUGGESTIONS */}
        {result.suggestions && result.suggestions.length > 0 && (
          <div className="space-y-2 pt-2 border-t border-slate-100">
            <h4 className="flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wider text-slate-600">
              <Lightbulb className="h-3.5 w-3.5 text-amber-500" />
              Targeted Recommendations for this Job
            </h4>

            <div className="space-y-2.5">
              {result.suggestions.map((sug, i) => (
                <div
                  key={i}
                  className="rounded-xl border border-sky-100 bg-sky-50/50 p-3 text-xs"
                >
                  <p className="font-semibold text-sky-900">{sug.title}</p>
                  <p className="mt-1 text-slate-600 leading-relaxed">
                    {sug.description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}

        {onClear && (
          <div className="flex justify-end pt-1">
            <button
              type="button"
              onClick={onClear}
              className="text-xs text-slate-400 hover:text-slate-600 transition-colors"
            >
              Clear JD Analysis
            </button>
          </div>
        )}
      </CardContent>
    </Card>
  )
}

