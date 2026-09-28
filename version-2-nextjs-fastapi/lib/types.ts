export interface SkillMatch {
  skill: string
  match: number
  found: boolean
}

export interface ResumeAnalysis {
  overallScore: number
  fileName: string
  role: string
  skillMatches: SkillMatch[]
  experience: {
    years: number
    relevance: number
  }
  education: {
    match: number
    degree: string
  }
  keywords: {
    found: number
    missing: number
  }
  atsScore: number
}

export interface Suggestion {
  id: string
  type: "critical" | "improvement" | "skill" | "format" | "education" | "experience" | "ats" | "summary"
  icon: string
  title: string
  description: string
  impact: "high" | "medium" | "low"
}
