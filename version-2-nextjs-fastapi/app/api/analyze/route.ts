import { NextResponse } from "next/server"

export async function POST(request: Request) {
  try {
    const formData = await request.formData()
    const file = formData.get("resume") as File
    const role = formData.get("role") as string

    if (!file || !role) {
      return NextResponse.json(
        { error: "Resume and role are required" },
        { status: 400 }
      )
    }

    // Simulate AI analysis delay
    await new Promise((resolve) => setTimeout(resolve, 1500))

    // Generate mock analysis based on role
    const roleSkills: Record<string, string[]> = {
      "frontend-developer": ["React", "TypeScript", "CSS", "JavaScript", "HTML", "Tailwind", "Next.js", "Vue.js"],
      "backend-developer": ["Node.js", "Python", "SQL", "REST APIs", "GraphQL", "Docker", "AWS", "PostgreSQL"],
      "fullstack-developer": ["React", "Node.js", "TypeScript", "MongoDB", "Docker", "AWS", "REST APIs", "GraphQL"],
      "data-scientist": ["Python", "Machine Learning", "TensorFlow", "SQL", "Pandas", "Statistics", "R", "Deep Learning"],
      "product-manager": ["Agile", "Scrum", "JIRA", "Roadmapping", "User Research", "Analytics", "Strategy", "Communication"],
      "ux-designer": ["Figma", "User Research", "Prototyping", "Wireframing", "Design Systems", "Usability Testing", "Adobe XD", "Sketch"],
    }

    const requiredSkills = roleSkills[role] || roleSkills["frontend-developer"]
    
    // Generate random matches
    const skillMatches = requiredSkills.map((skill) => ({
      skill,
      match: Math.floor(Math.random() * 40) + 60,
      found: Math.random() > 0.3,
    }))

    const overallScore = Math.floor(
      skillMatches.reduce((acc, s) => acc + (s.found ? s.match : 0), 0) / skillMatches.length
    )

    const analysis = {
      overallScore,
      fileName: file.name,
      role: role.replace(/-/g, " ").replace(/\b\w/g, (l) => l.toUpperCase()),
      skillMatches,
      experience: {
        years: Math.floor(Math.random() * 8) + 1,
        relevance: Math.floor(Math.random() * 30) + 70,
      },
      education: {
        match: Math.floor(Math.random() * 30) + 70,
        degree: ["Bachelor's", "Master's", "PhD", "Bootcamp"][Math.floor(Math.random() * 4)],
      },
      keywords: {
        found: Math.floor(Math.random() * 15) + 10,
        missing: Math.floor(Math.random() * 8) + 2,
      },
      atsScore: Math.floor(Math.random() * 20) + 75,
    }

    return NextResponse.json(analysis)
  } catch {
    return NextResponse.json(
      { error: "Failed to analyze resume" },
      { status: 500 }
    )
  }
}
