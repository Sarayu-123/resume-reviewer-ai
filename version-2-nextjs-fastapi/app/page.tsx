
"use client"

import { useState } from "react"
import { DashboardHeader } from "@/components/dashboard/header"
import { ResumeUpload } from "@/components/dashboard/resume-upload"
import { ScoreCard } from "@/components/dashboard/score-card"
import { SkillChart } from "@/components/dashboard/skill-chart"
import { SuggestionsPanel } from "@/components/dashboard/suggestions-panel"
import { EmptyState } from "@/components/dashboard/empty-state"

const API_BASE_URL = "http://127.0.0.1:8000"

async function readResponse(res: Response) {
  const text = await res.text()

  let data: any

  try {
    data = text ? JSON.parse(text) : {}
  } catch {
    throw new Error(
      `Backend returned an invalid response (HTTP ${res.status}). Check the FastAPI terminal.`
    )
  }

  if (!res.ok) {
    const detail =
      typeof data.detail === "string"
        ? data.detail
        : `Request failed with HTTP ${res.status}`

    throw new Error(detail)
  }

  return data
}

export default function Dashboard() {
  const [analysis, setAnalysis] = useState<any>(null)
  const [suggestions, setSuggestions] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [suggestLoading, setSuggestLoading] = useState(false)
  const [error, setError] = useState("")

  const handleAnalyze = async (file: File, role: string) => {
    const formData = new FormData()
    formData.append("file", file)
    formData.append("role", role)

    setLoading(true)
    setError("")
    setAnalysis(null)
    setSuggestions([])

    try {
      let res: Response

      try {
        res = await fetch(`${API_BASE_URL}/analyze`, {
          method: "POST",
          body: formData,
        })
      } catch (err) {
        throw new Error(
          "Cannot connect to FastAPI. Start the backend and check that http://127.0.0.1:8000/docs opens."
        )
      }

      const data = await readResponse(res)

      console.log("BACKEND ANALYSIS RESPONSE:", data)
      setAnalysis(data)

      // Generate suggestions separately so a suggestion failure
      // does not erase a successful resume analysis.
      void fetchSuggestions(data)
    } catch (err) {
      console.error("Resume analysis error:", err)

      setError(
        err instanceof Error
          ? err.message
          : "An unexpected error occurred during resume analysis."
      )
    } finally {
      setLoading(false)
    }
  }

  const fetchSuggestions = async (analysisData: any) => {
    setSuggestLoading(true)

    try {
      let res: Response

      try {
        res = await fetch(`${API_BASE_URL}/ai-suggestions`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            role: analysisData.role,
            skillMatches: analysisData.skillMatches,
            resumeText: analysisData.resumeText,
          }),
        })
      } catch {
        throw new Error(
          "Cannot connect to the suggestions endpoint. Check that FastAPI is running."
        )
      }

      const data = await readResponse(res)

      setSuggestions(
        Array.isArray(data.suggestions) ? data.suggestions : []
      )
    } catch (err) {
      console.error("AI suggestions error:", err)

      setSuggestions([
        err instanceof Error
          ? err.message
          : "Could not generate AI suggestions. Try refreshing suggestions.",
      ])
    } finally {
      setSuggestLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-sky-50 to-cyan-50">
      <DashboardHeader />

      <main className="max-w-7xl mx-auto px-4 py-8">
        {error && (
          <div
            role="alert"
            className="mb-6 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700"
          >
            <p className="font-semibold">Resume analysis failed</p>
            <p className="mt-1">{error}</p>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="space-y-6">
            <ResumeUpload
              onAnalyze={handleAnalyze}
              isAnalyzing={loading}
            />

            {analysis && (
              <SuggestionsPanel
                suggestions={suggestions}
                isLoading={suggestLoading}
                onRefresh={() => fetchSuggestions(analysis)}
              />
            )}
          </div>

          <div className="lg:col-span-2">
            {analysis ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <ScoreCard analysis={analysis} />
                <SkillChart skillMatches={analysis.skillMatches} />
              </div>
            ) : (
              <EmptyState />
            )}
          </div>
        </div>
      </main>
    </div>
  )
}
