"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { cn } from "@/lib/utils"
import type { ResumeAnalysis } from "@/lib/types"

interface ScoreCardProps {
  analysis: ResumeAnalysis
}

export function ScoreCard({ analysis }: ScoreCardProps) {
  const getScoreGradient = (score: number) => {
    if (score >= 80) return "from-cyan-500 to-blue-500"
    if (score >= 60) return "from-blue-400 to-sky-500"
    return "from-sky-400 to-blue-400"
  }

  const getScoreBg = (score: number) => {
    if (score >= 80) return "from-cyan-50 to-blue-50"
    if (score >= 60) return "from-blue-50 to-sky-50"
    return "from-sky-50 to-blue-50"
  }

  const getScoreLabel = (score: number) => {
    if (score >= 90) return { text: "Excellent", emoji: "\u{1F31F}" }
    if (score >= 80) return { text: "Great", emoji: "\u{1F389}" }
    if (score >= 70) return { text: "Good", emoji: "\u{1F44D}" }
    if (score >= 60) return { text: "Fair", emoji: "\u{1F4AA}" }
    return { text: "Needs Work", emoji: "\u{1F4DD}" }
  }

  const scoreInfo = getScoreLabel(analysis.overallScore)

  const stats = [
    {
      label: "Experience",
      value: `${analysis.experience.years} yrs`,
      subtext: `${analysis.experience.relevance}% relevant`,
      icon: "\u{1F4BC}",
      gradient: "from-blue-500 to-cyan-500",
      bg: "from-blue-50 to-cyan-50",
    },
    {
      label: "Education",
      value: analysis.education.degree,
      subtext: `${analysis.education.match}% match`,
      icon: "\u{1F393}",
      gradient: "from-sky-500 to-blue-500",
      bg: "from-sky-50 to-blue-50",
    },
    {
      label: "Keywords",
      value: analysis.keywords.found,
      subtext: `${analysis.keywords.missing} missing`,
      icon: "\u{1F511}",
      gradient: "from-cyan-500 to-sky-500",
      bg: "from-cyan-50 to-sky-50",
    },
    {
      label: "ATS Score",
      value: `${analysis.atsScore}%`,
      subtext: "Compatibility",
      icon: "\u{1F916}",
      gradient: "from-blue-600 to-cyan-500",
      bg: "from-blue-50 to-cyan-50",
    },
  ]

  return (
    <Card className="border-blue-100 bg-white/80 backdrop-blur-sm shadow-xl shadow-blue-500/5 overflow-hidden">
      <div className={cn("h-1 w-full bg-gradient-to-r", getScoreGradient(analysis.overallScore))} />
      <CardHeader className="pb-4">
        <div className="flex items-center gap-3">
          <div className="flex items-center justify-center w-12 h-12 rounded-2xl bg-gradient-to-br from-blue-500 to-cyan-500 shadow-lg shadow-blue-500/25">
            <span className="text-2xl">{"\u{1F4CA}"}</span>
          </div>
          <div>
            <CardTitle className="text-lg text-foreground">Resume Score</CardTitle>
            <CardDescription>
              Analysis for <span className="font-semibold text-blue-600">{analysis.role}</span>
            </CardDescription>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Main Score */}
        <div className={cn(
          "relative rounded-3xl p-6 bg-gradient-to-br",
          getScoreBg(analysis.overallScore)
        )}>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground font-medium mb-1">Overall Score</p>
              <div className="flex items-baseline gap-2">
                <span className={cn("text-5xl font-bold bg-gradient-to-r bg-clip-text text-transparent", getScoreGradient(analysis.overallScore))}>
                  {analysis.overallScore}
                </span>
                <span className="text-2xl text-muted-foreground font-medium">/100</span>
              </div>
              <div className="flex items-center gap-2 mt-2">
                <span className="text-xl">{scoreInfo.emoji}</span>
                <p className="text-sm font-medium text-foreground">
                  {scoreInfo.text} Match
                </p>
              </div>
            </div>
            <div className="relative w-24 h-24">
              <svg className="w-24 h-24 transform -rotate-90">
                <circle
                  cx="48"
                  cy="48"
                  r="40"
                  strokeWidth="10"
                  fill="none"
                  className="stroke-white/50"
                />
                <defs>
                  <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stopColor="#06b6d4" />
                    <stop offset="100%" stopColor="#3b82f6" />
                  </linearGradient>
                </defs>
                <circle
                  cx="48"
                  cy="48"
                  r="40"
                  strokeWidth="10"
                  fill="none"
                  strokeLinecap="round"
                  stroke="url(#scoreGradient)"
                  strokeDasharray={`${analysis.overallScore * 2.51} 251`}
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-3xl">{scoreInfo.emoji}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 gap-3">
          {stats.map((stat) => (
            <div
              key={stat.label}
              className={cn(
                "rounded-2xl p-4 bg-gradient-to-br border border-transparent transition-all duration-300 hover:scale-[1.02] hover:shadow-lg",
                stat.bg
              )}
            >
              <div className="flex items-center gap-2 mb-2">
                <span className="text-xl">{stat.icon}</span>
                <span className="text-xs text-muted-foreground font-medium">{stat.label}</span>
              </div>
              <p className={cn("text-xl font-bold bg-gradient-to-r bg-clip-text text-transparent", stat.gradient)}>{stat.value}</p>
              <p className="text-xs text-muted-foreground mt-0.5">{stat.subtext}</p>
            </div>
          ))}
        </div>

        {/* File Info */}
        <div className="flex items-center gap-3 px-4 py-3 rounded-xl bg-blue-50 border border-blue-100">
          <span className="text-lg">{"\u{1F4C4}"}</span>
          <span className="text-sm text-foreground font-medium truncate">{analysis.fileName}</span>
        </div>
      </CardContent>
    </Card>
  )
}
