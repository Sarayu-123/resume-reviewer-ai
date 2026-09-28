"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar
} from "recharts"

export function SkillChart({ skillMatches }: any) {

  // SORT skills so different roles LOOK different
  const sortedSkills = [...skillMatches].sort((a, b) => b.match - a.match)

  const foundSkills = sortedSkills.filter((s) => s.found)
  const missingSkills = sortedSkills.filter((s) => !s.found)

  const barData = sortedSkills.map((s) => ({
    name: s.skill,
    match: s.match,
    found: s.found
  }))

  // ❗ IMPORTANT: DO NOT slice → shows all skills
  const radarData = sortedSkills.map((s) => ({
    skill: s.skill,
    score: s.found ? s.match : 10
  }))

  const avg =
    foundSkills.length > 0
      ? Math.round(foundSkills.reduce((a, b) => a + b.match, 0) / foundSkills.length)
      : 0

  return (
    <Card>
      <CardHeader>
        <CardTitle>
          Skill Match ({foundSkills.length} / {sortedSkills.length})
        </CardTitle>
      </CardHeader>

      <CardContent>

        {/* BAR CHART */}
        <div style={{ height: 300 }}>
          <ResponsiveContainer>
            <BarChart data={barData} layout="vertical">
              <XAxis type="number" domain={[0, 100]} />
              <YAxis dataKey="name" type="category" width={120} />
              <Tooltip />
              <Bar dataKey="match" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* RADAR CHART */}
        <div style={{ height: 300 }}>
          <ResponsiveContainer>
            <RadarChart data={radarData}>
              <PolarGrid />
              <PolarAngleAxis dataKey="skill" />
              <PolarRadiusAxis domain={[0, 100]} />
              <Radar dataKey="score" stroke="#2563eb" fill="#3b82f6" fillOpacity={0.5} />
            </RadarChart>
          </ResponsiveContainer>
        </div>

        {/* MATCHED */}
        <div>
          <h4>Matched Skills</h4>
          {foundSkills.map((s, i) => (
            <span key={i} style={{ marginRight: 8 }}>
              {s.skill} ({s.match}%)
            </span>
          ))}
        </div>

        {/* MISSING */}
        <div>
          <h4>Missing Skills</h4>
          {missingSkills.map((s, i) => (
            <span key={i} style={{ marginRight: 8 }}>
              {s.skill}
            </span>
          ))}
        </div>

        <p>Average Match: {avg}%</p>

      </CardContent>
    </Card>
  )
}
