"use client"

import { useState } from "react"
import { DashboardHeader } from "@/components/dashboard/header"
import { ResumeUpload } from "@/components/dashboard/resume-upload"
import { ScoreCard } from "@/components/dashboard/score-card"
import { SkillChart } from "@/components/dashboard/skill-chart"
import { SuggestionsPanel } from "@/components/dashboard/suggestions-panel"
import { EmptyState } from "@/components/dashboard/empty-state"

export default function Dashboard() {

  const [analysis, setAnalysis] = useState<any>(null)
  const [suggestions, setSuggestions] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [suggestLoading, setSuggestLoading] = useState(false)

  // 🔥 THIS IS WHERE formData IS CREATED
  const handleAnalyze = async (file: File, role: string) => {

    console.log("ROLE SENT:", role)

    const formData = new FormData()
    formData.append("file", file)   // IMPORTANT
    formData.append("role", role)

    try {
      setLoading(true)

      const res = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        body: formData,
      })

      const data = await res.json()

      console.log("BACKEND RESPONSE:", data)

      setAnalysis(data)

      fetchSuggestions(data)

    } catch (err) {
      console.error("ERROR:", err)
      alert("Backend connection failed")
    } finally {
      setLoading(false)
    }
  }

  const fetchSuggestions = async (analysisData: any) => {
    try {
      setSuggestLoading(true)

      const res = await fetch("http://127.0.0.1:8000/ai-suggestions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(analysisData)
      })

      const data = await res.json()

      setSuggestions(data.suggestions || [])

    } catch (err) {
      console.error("Suggestions error:", err)
    } finally {
      setSuggestLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-sky-50 to-cyan-50">

      <DashboardHeader />

      <main className="max-w-7xl mx-auto px-4 py-8">

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

          {/* LEFT SIDE */}
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

          {/* RIGHT SIDE */}
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