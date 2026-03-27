from mcp.server.fastmcp import FastMCP
import urllib.request
import urllib.error
import json
import base64
import os

mcp = FastMCP("Jenkins")

# ── Jenkins connection config (override via environment variables) ──────────
JENKINS_URL  = os.getenv("JENKINS_URL",  "http://localhost:8080")
JENKINS_USER = os.getenv("JENKINS_USER", "admin")
JENKINS_TOKEN = os.getenv("JENKINS_TOKEN", "dedebc5474df47a0ad5cf88a60d0b54e")

def _auth_header() -> dict:
    """Build Basic-Auth header from credentials."""
    credentials = f"{JENKINS_USER}:{JENKINS_TOKEN}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json",
    }

def _get(path: str) -> dict:
    """Perform an authenticated GET request to the Jenkins REST API."""
    url = f"{JENKINS_URL}{path}"
    req = urllib.request.Request(url, headers=_auth_header())
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.reason}", "url": url}
    except Exception as e:
        return {"error": str(e), "url": url}


# ── Tools ────────────────────────────────────────────────────────────────────

@mcp.tool()
def get_all_builds(job_name: str) -> str:
    """
    Retrieve all builds for the specified Jenkins job.

    Args:
        job_name: The exact name of the Jenkins job (e.g. 'ci-pipeline').

    Returns:
        A JSON string with build numbers, results, timestamps, and durations.
    """
    print(f"Tool Called: get_all_builds(job_name={job_name!r})")
    data = _get(f"/job/{job_name}/api/json?tree=builds[number,result,timestamp,duration,url]")
    if "error" in data:
        return json.dumps(data)

    builds = data.get("builds", [])
    if not builds:
        return json.dumps({"message": f"No builds found for job '{job_name}'."})

    result = []
    for b in builds:
        result.append({
            "build_number": b.get("number"),
            "result":       b.get("result", "IN_PROGRESS"),
            "timestamp_ms": b.get("timestamp"),
            "duration_ms":  b.get("duration"),
            "url":          b.get("url"),
        })

    return json.dumps({"job": job_name, "total_builds": len(result), "builds": result}, indent=2)


@mcp.tool()
def get_build_details(job_name: str, build_number: int) -> str:
    """
    Retrieve detailed information about a specific build.

    Args:
        job_name:     The Jenkins job name.
        build_number: The build number to inspect.

    Returns:
        A JSON string with full build details including console output URL.
    """
    print(f"Tool Called: get_build_details(job_name={job_name!r}, build_number={build_number})")
    data = _get(
        f"/job/{job_name}/{build_number}/api/json"
        "?tree=number,result,timestamp,duration,url,description,builtOn,culprits[fullName]"
    )
    if "error" in data:
        return json.dumps(data)

    return json.dumps({
        "build_number": data.get("number"),
        "result":       data.get("result", "IN_PROGRESS"),
        "timestamp_ms": data.get("timestamp"),
        "duration_ms":  data.get("duration"),
        "description":  data.get("description"),
        "built_on":     data.get("builtOn"),
        "culprits":     [c["fullName"] for c in data.get("culprits", [])],
        "url":          data.get("url"),
        "console_url":  f"{data.get('url', '')}console",
    }, indent=2)


@mcp.tool()
def get_last_build_status(job_name: str) -> str:
    """
    Return the status of the most recent build for a Jenkins job.

    Args:
        job_name: The Jenkins job name.

    Returns:
        A JSON string with the latest build's number and result.
    """
    print(f"Tool Called: get_last_build_status(job_name={job_name!r})")
    data = _get(f"/job/{job_name}/api/json?tree=lastBuild[number,result,url]")
    if "error" in data:
        return json.dumps(data)

    last = data.get("lastBuild")
    if not last:
        return json.dumps({"message": f"No builds found for job '{job_name}'."})

    return json.dumps({
        "job":          job_name,
        "build_number": last.get("number"),
        "result":       last.get("result", "IN_PROGRESS"),
        "url":          last.get("url"),
    }, indent=2)


@mcp.tool()
def list_jobs() -> str:
    """
    List all jobs available on the Jenkins server.

    Returns:
        A JSON string with job names, URLs, and colours (status indicators).
    """
    print("Tool Called: list_jobs()")
    data = _get("/api/json?tree=jobs[name,url,color]")
    if "error" in data:
        return json.dumps(data)

    jobs = [
        {"name": j.get("name"), "url": j.get("url"), "status": j.get("color")}
        for j in data.get("jobs", [])
    ]
    return json.dumps({"total_jobs": len(jobs), "jobs": jobs}, indent=2)


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run(transport="stdio")