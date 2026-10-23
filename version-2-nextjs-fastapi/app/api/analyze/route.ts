
import { NextResponse } from "next/server"

export async function POST(request: Request) {
  try {
    const body = await request.json()

    if (
      !body.role ||
      !Array.isArray(body.skillMatches) ||
      !body.resumeText
    ) {
      return NextResponse.json(
        {
          error: "Role, skill matches, and resume text are required",
        },
        { status: 400 }
      )
    }

    const backendUrl =
      process.env.BACKEND_API_URL || "http://127.0.0.1:8000"

    const response = await fetch(
      `${backendUrl}/ai-suggestions`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
        cache: "no-store",
        signal: AbortSignal.timeout(150000),
      }
    )

    const result = await response.json()

    if (!response.ok) {
      return NextResponse.json(
        {
          error:
            result.detail ||
            result.error ||
            "AI suggestion generation failed",
        },
        { status: response.status }
      )
    }

    return NextResponse.json(result)
  } catch (error) {
    console.error("AI suggestions request failed:", error)

    return NextResponse.json(
      {
        error: "Could not connect to the AI suggestions backend",
      },
      { status: 502 }
    )
  }
}
