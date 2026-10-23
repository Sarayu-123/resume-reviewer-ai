
"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
} from "recharts"

type SkillMatch = {
  skill: string
  match: number
  found: boolean
  source?: string
}

type SkillChartProps = {
  skillMatches: SkillMatch[]
}

export function SkillChart({ skillMatches }: SkillChartProps) {
  const skills = Array.isArray(skillMatches) ? skillMatches : []

  // Keep the role's original skill order.
  const foundSkills = skills.filter((skill) => skill.found)
  const missingSkills = skills.filter((skill) => !skill.found)

  const barData = skills.map((skill) => ({
    name: skill.skill,
    match: skill.found ? skill.match : 0,
    found: skill.found,
  }))

  // Missing skills should have a score of zero, not an artificial 10.
  const radarData = skills.map((skill) => ({
    skill: skill.skill,
    score: skill.found ? skill.match : 0,
  }))

  // Average across ALL required skills, including missing ones.
  const averageMatch = skills.length
    ? Math.round(
        skills.reduce(
          (total, skill) =>
            total + (skill.found ? skill.match : 0),
          0
        ) / skills.length
      )
    : 0

  return (
    <Card>
      <CardHeader>
        <CardTitle>
          Skill Match ({foundSkills.length} / {skills.length})
        </CardTitle>
      </CardHeader>

      <CardContent className="space-y-6">
        {/* BAR CHART */}
        <div style={{ height: 300 }}>
          {skills.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={barData} layout="vertical">
                <XAxis type="number" domain={[0, 100]} />
                <YAxis
                  dataKey="name"
                  type="category"
                  width={120}
                />
                <Tooltip />
                <Bar dataKey="match" name="Skill coverage" fill="#2563eb" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p>No skill data available.</p>
          )}
        </div>

        {/* RADAR CHART */}
        <div style={{ height: 300 }}>
          {skills.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid />
                <PolarAngleAxis dataKey="skill" />
                <PolarRadiusAxis domain={[0, 100]} />
                <Radar
                  dataKey="score"
                  name="Skill coverage"
                  stroke="#2563eb"
                  fill="#3b82f6"
                  fillOpacity={0.5}
                />
                <Tooltip />
              </RadarChart>
            </ResponsiveContainer>
          ) : (
            <p>No skill data available.</p>
          )}
        </div>

        {/* MATCHED SKILLS */}
        <div>
          <h4 className="font-semibold">Matched Skills</h4>
          {foundSkills.length > 0 ? (
            <div className="mt-2 flex flex-wrap gap-2">
              {foundSkills.map((skill) => (
                <span
                  key={skill.skill}
                  className="text-sm"
                >
                  {skill.skill} ({skill.match}%)
                </span>
              ))}
            </div>
          ) : (
            <p className="mt-2 text-sm text-muted-foreground">
              No required skills detected.
            </p>
          )}
        </div>

        {/* MISSING SKILLS */}
        <div>
          <h4 className="font-semibold">Missing Skills</h4>
          {missingSkills.length > 0 ? (
            <div className="mt-2 flex flex-wrap gap-2">
              {missingSkills.map((skill) => (
                <span key={skill.skill} className="text-sm">
                  {skill.skill}
                </span>
              ))}
            </div>
          ) : (
            <p className="mt-2 text-sm text-muted-foreground">
              All listed role requirements were detected.
            </p>
          )}
        </div>

        <p className="font-semibold">
          Average Match: {averageMatch}%
        </p>
        <p className="text-xs text-muted-foreground">
          Calculated across all required skills, counting missing skills as zero.
          This measures skill coverage, not overall candidate quality.
        </p>
      </CardContent>
    </Card>
  )
}
