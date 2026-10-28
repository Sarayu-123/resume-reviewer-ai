"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { FileText, Sparkles, ChevronDown, ChevronUp } from "lucide-react"

interface JDInputCardProps {
  hasResume: boolean
  isLoading: boolean
  onAnalyzeJD: (jdText: string) => void
}

export function JDInputCard({
  hasResume,
  isLoading,
  onAnalyzeJD,
}: JDInputCardProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [jdText, setJdText] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!jdText.trim()) return
    onAnalyzeJD(jdText.trim())
  }

  return (
    <Card className="rounded-xl border border-sky-100 bg-white shadow-sm overflow-hidden transition-all">
      <CardHeader
        className="cursor-pointer py-3.5 px-4 flex flex-row items-center justify-between hover:bg-sky-50/50 transition-colors select-none"
        onClick={() => setIsOpen(!isOpen)}
      >
        <div className="flex items-center gap-2.5">
          <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-sky-100 text-sky-700">
            <FileText className="h-4 w-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <CardTitle className="text-sm font-semibold text-slate-800">
                Target Job Description
              </CardTitle>
              <span className="rounded-full bg-sky-100 px-2 py-0.5 text-[10px] font-semibold text-sky-700">
                Optional
              </span>
            </div>
            <p className="text-xs text-slate-500">
              Calculate match relevance & advice for a specific JD
            </p>
          </div>
        </div>

        <button
          type="button"
          aria-label={isOpen ? "Collapse section" : "Expand section"}
          className="text-slate-400 hover:text-slate-600"
        >
          {isOpen ? (
            <ChevronUp className="h-4 w-4" />
          ) : (
            <ChevronDown className="h-4 w-4" />
          )}
        </button>
      </CardHeader>

      {isOpen && (
        <CardContent className="pt-2 pb-4 px-4 border-t border-slate-100 space-y-3">
          <textarea
            value={jdText}
            onChange={(e) => setJdText(e.target.value)}
            rows={4}
            placeholder="Paste job description text here (e.g., responsibilities, qualifications, tech stack requirements)..."
            className="w-full rounded-lg border border-slate-200 p-2.5 text-xs text-slate-800 placeholder:text-slate-400 focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500 transition-all resize-y"
          />

          {!hasResume && (
            <p className="text-xs text-amber-600 flex items-center gap-1 font-medium">
              <span>⚠️</span> Upload and analyze your resume first to compare with this JD.
            </p>
          )}

          <div className="flex items-center justify-between gap-2">
            {jdText.trim() && (
              <button
                type="button"
                onClick={() => setJdText("")}
                className="text-xs text-slate-400 hover:text-slate-600"
              >
                Clear text
              </button>
            )}

            <Button
              type="button"
              onClick={handleSubmit}
              disabled={!hasResume || !jdText.trim() || isLoading}
              size="sm"
              className="ml-auto bg-sky-600 hover:bg-sky-700 text-white text-xs font-semibold px-4 shadow-sm"
            >
              {isLoading ? (
                <>
                  <span className="inline-block animate-spin mr-1.5">⏳</span>
                  Comparing JD...
                </>
              ) : (
                <>
                  <Sparkles className="h-3.5 w-3.5 mr-1" />
                  Analyze JD Match
                </>
              )}
            </Button>
          </div>
        </CardContent>
      )}
    </Card>
  )
}

