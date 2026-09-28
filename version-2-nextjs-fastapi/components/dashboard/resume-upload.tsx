"use client"

import { useState } from "react"

interface Props {
  onAnalyze: (file: File, role: string) => void
  isAnalyzing: boolean
}

export function ResumeUpload({ onAnalyze, isAnalyzing }: Props) {

  const [file, setFile] = useState<File | null>(null)
  const [role, setRole] = useState("Software Engineer")

  const roles = [
    "Frontend Developer",
    "Backend Developer",
    "Fullstack Developer",
    "Data Scientist",
    "Machine Learning Engineer",
    "Data Engineer",
    "Data Analyst",
    "DevOps Engineer",
    "Cloud Engineer",
    "Mobile Developer",
    "AI Engineer",
    "Software Engineer",
    "Product Manager",
    "UX Designer",
    "Security Engineer",
    "QA Engineer"
  ]

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0]
    if (selected) {
      setFile(selected)
    }
  }

  const handleSubmit = () => {
    if (!file) {
      alert("Please upload a resume first")
      return
    }

    console.log("Selected Role:", role)
    console.log("Selected File:", file.name)

    onAnalyze(file, role)
  }

  return (
    <div className="p-6 bg-white rounded-xl shadow-md space-y-4">

      <h2 className="text-lg font-semibold">Upload Resume</h2>

      {/* FILE INPUT */}
      <input
        type="file"
        accept=".pdf,.docx"
        onChange={handleFileChange}
        className="w-full border p-2 rounded"
      />

      {/* ROLE DROPDOWN */}
      <select
        value={role}
        onChange={(e) => setRole(e.target.value)}
        className="w-full border p-2 rounded"
      >
        {roles.map((r, i) => (
          <option key={i} value={r}>
            {r}
          </option>
        ))}
      </select>

      {/* BUTTON */}
      <button
        onClick={handleSubmit}
        disabled={isAnalyzing}
        className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
      >
        {isAnalyzing ? "Analyzing..." : "Analyze Resume"}
      </button>

      {/* FILE NAME DISPLAY */}
      {file && (
        <p className="text-sm text-gray-500">
          Selected: {file.name}
        </p>
      )}

    </div>
  )
}