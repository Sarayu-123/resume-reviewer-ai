import { NextResponse } from "next/server"

export async function POST(request: Request) {
  try {
    const body = await request.json()
    const { analysis } = body

    if (!analysis) {
      return NextResponse.json(
        { error: "Analysis data is required" },
        { status: 400 }
      )
    }

    // Simulate AI processing delay
    await new Promise((resolve) => setTimeout(resolve, 1000))

    const missingSkills = analysis.skillMatches
      .filter((s: { found: boolean }) => !s.found)
      .map((s: { skill: string }) => s.skill)

    const lowMatchSkills = analysis.skillMatches
      .filter((s: { found: boolean; match: number }) => s.found && s.match < 75)
      .map((s: { skill: string }) => s.skill)

    const suggestions = [
      {
        id: "1",
        type: "critical" as const,
        icon: "🎯",
        title: "Add Missing Keywords",
        description: `Your resume is missing ${analysis.keywords.missing} important keywords for the ${analysis.role} role. Include terms like "${missingSkills.slice(0, 2).join('", "')}" to improve ATS compatibility.`,
        impact: "high",
      },
      {
        id: "2",
        type: "improvement" as const,
        icon: "📈",
        title: "Quantify Your Achievements",
        description: "Add specific metrics and numbers to your experience section. For example: 'Increased conversion rate by 25%' or 'Managed a team of 8 engineers'.",
        impact: "high",
      },
      {
        id: "3",
        type: "skill" as const,
        icon: "🛠️",
        title: "Highlight Technical Skills",
        description: `Consider adding more details about your proficiency in ${lowMatchSkills.slice(0, 2).join(" and ")}. Include specific projects or certifications.`,
        impact: "medium",
      },
      {
        id: "4",
        type: "format" as const,
        icon: "📝",
        title: "Improve Resume Format",
        description: "Your resume could benefit from clearer section headers and consistent bullet point formatting. Use action verbs at the start of each bullet.",
        impact: "medium",
      },
      {
        id: "5",
        type: "education" as const,
        icon: "🎓",
        title: "Education Section Enhancement",
        description: `Your ${analysis.education.degree} degree is relevant. Consider adding relevant coursework, projects, or academic achievements that relate to ${analysis.role}.`,
        impact: "low",
      },
      {
        id: "6",
        type: "experience" as const,
        icon: "💼",
        title: "Experience Alignment",
        description: `With ${analysis.experience.years} years of experience, emphasize your most recent and relevant roles. Consider restructuring to highlight leadership and impact.`,
        impact: analysis.experience.years > 5 ? "high" : "medium",
      },
      {
        id: "7",
        type: "ats" as const,
        icon: "🤖",
        title: "ATS Optimization",
        description: `Your ATS score is ${analysis.atsScore}%. Remove graphics, tables, and fancy formatting. Use standard section headers like "Experience" and "Education".`,
        impact: analysis.atsScore < 80 ? "high" : "low",
      },
      {
        id: "8",
        type: "summary" as const,
        icon: "✨",
        title: "Professional Summary",
        description: `Add a compelling 2-3 sentence professional summary at the top highlighting your ${analysis.experience.years}+ years of experience and key strengths for the ${analysis.role} position.`,
        impact: "medium",
      },
    ]

    // Sort by impact
    const impactOrder = { high: 0, medium: 1, low: 2 }
    suggestions.sort((a, b) => impactOrder[a.impact as keyof typeof impactOrder] - impactOrder[b.impact as keyof typeof impactOrder])

    return NextResponse.json({ suggestions: suggestions.slice(0, 6) })
  } catch {
    return NextResponse.json(
      { error: "Failed to generate suggestions" },
      { status: 500 }
    )
  }
}
