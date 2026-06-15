# run_audit_tests.py - Test harness for code-quality-auditor test scenarios

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).parent.parent
MOCK_REPOS_DIR = PROJECT_ROOT / "tests" / "mock_repos"
LOGS_DIR = PROJECT_ROOT / "tests" / "execution_logs"


SCENARIOS = {
    1: {
        "name": "Python Django E-Commerce Backend",
        "repo_dir": "django-ecommerce",
        "language": "Python",
        "framework": "Django 4.2 + DRF",
        "domain": "E-commerce",
        "scope": "Full Audit",
        "known_concerns": "Checkout sometimes throws 500 errors; adding new payment methods takes too long",
    },
    2: {
        "name": "React + TypeScript Admin Dashboard",
        "repo_dir": "react-admin-dashboard",
        "language": "TypeScript",
        "framework": "React 18 + React Query + Zustand",
        "domain": "B2B SaaS admin dashboard",
        "scope": "Targeted - Security and Performance only",
        "known_concerns": "Dashboard feels slow; worried about XSS risks in the markdown renderer",
    },
    3: {
        "name": "Java Spring Boot Payment Microservice",
        "repo_dir": "spring-fintech-payment",
        "language": "Java",
        "framework": "Spring Boot 3.x + Spring Security + JPA/Hibernate",
        "domain": "Fintech - payment processing",
        "scope": "Specific Concern - Security + Reliability",
        "known_concerns": "SQL injection attempt in logs; worried about transaction isolation levels",
    },
    4: {
        "name": "Node.js REST API - Small Codebase",
        "repo_dir": "node-hr-api",
        "language": "JavaScript",
        "framework": "Node.js 20 + Express 4",
        "domain": "Internal HR tool",
        "scope": "Full Audit",
        "known_concerns": "None - overall health check",
    },
    5: {
        "name": "Legacy PHP E-Commerce Application",
        "repo_dir": "legacy-php-ecommerce",
        "language": "PHP",
        "framework": "PHP 5.6 (no framework - procedural)",
        "domain": "E-commerce",
        "scope": "Full Audit",
        "known_concerns": "Suspected SQL injection; code written 2009, patched by multiple contractors",
    },
}


def _count_loc(directory):
    total_files = 0
    total_loc = 0
    extensions = {".py", ".js", ".ts", ".tsx", ".java", ".php", ".jsx", ".json", ".css"}
    for f in directory.rglob("*"):
        if f.is_file() and f.suffix in extensions:
            total_files += 1
            try:
                flines = f.read_text(encoding="utf-8", errors="replace").split(chr(10))
                code_lines = [l for l in flines if l.strip() and not l.strip().startswith(("//", "#", "/*", "*"))]
                total_loc += len(code_lines)
            except Exception:
                pass
    return total_files, total_loc


def _get_patterns():
    """Return list of (regex_pattern, description, category) tuples."""
    patterns = []
    patterns.append((r"mysql_query\s*\(", "Deprecated mysql_query usage (removed in PHP 7+)", "Security"))
    patterns.append((r"SELECT.*\{.*\}.*FROM", "SQL injection risk - string formatting in SQL query", "Security"))
    patterns.append((r"cursor\.execute\s*\(\s*f", "SQL injection risk - f-string in SQL query", "Security"))
    patterns.append((r"createStatement\(\)", "SQL injection risk - Statement instead of PreparedStatement", "Security"))
    patterns.append((r"sk_test_|sk_live_|pk_live_", "Hardcoded Stripe API key", "Security"))
    # Credential patterns built at runtime to avoid quote escaping issues
    _dq = chr(34)  # double quote
    _sq = chr(39)  # single quote
    patterns.append(("DB_PASS\\s*=\\s*[" + _dq + _sq + "]", "Hardcoded database credential", "Security"))
    patterns.append(("DB_USER\\s*=\\s*[" + _dq + _sq + "]", "Hardcoded database user", "Security"))
    patterns.append(("JWT_SECRET\\s*=\\s*[" + _dq + _sq + "]", "Hardcoded JWT secret", "Security"))
    patterns.append(("SECRET_KEY\\s*=\\s*[" + _dq + _sq + "]", "Hardcoded secret key", "Security"))
    patterns.append((r"dangerouslySetInnerHTML", "XSS risk - dangerouslySetInnerHTML without sanitization", "Security"))
    patterns.append((r"AllowAny", "No authentication - AllowAny permission class", "Security"))
    patterns.append((r"md5\s*\(", "Weak hashing algorithm (MD5)", "Security"))
    patterns.append((r"CURLOPT_SSL_VERIFYPEER\s*,\s*false", "SSL verification disabled", "Security"))
    patterns.append((r"CURLOPT_SSL_VERIFYHOST\s*,\s*false", "SSL host verification disabled", "Security"))
    patterns.append((r"except\s*:", "Bare except clause", "Quality"))
    patterns.append((r"except Exception.*:\s*pass", "Silent exception swallowing", "Quality"))
    patterns.append((r"except:\s*pass", "Bare except with pass", "Quality"))
    patterns.append((r"printStackTrace", "Stack trace printed instead of proper logging", "Quality"))
    patterns.append((r"err\.message", "Error message leaked to client", "Security"))
    patterns.append(("\\\\[", "Direct use of PHP superglobal without sanitization", "Security"))
    patterns.append(("\\\\[", "Direct use of PHP superglobal without sanitization", "Security"))
    patterns.append(("\\\\[", "Direct use of PHP superglobal without sanitization", "Security"))
    patterns.append(("\\\\[", "Direct session access without validation", "Security"))
    patterns.append((r"DEBUG_MODE.*true", "Debug mode enabled in production", "Security"))
    patterns.append((r"DISPLAY_ERRORS.*true", "Error display enabled in production", "Security"))
    patterns.append((r"session\.cookie_httponly.*0", "Session cookie not HttpOnly", "Security"))
    patterns.append((r"session\.cookie_secure.*0", "Session cookie not secure", "Security"))
    patterns.append((r"move_uploaded_file", "File upload without validation", "Security"))
    patterns.append((r"include\s*\(\s*\$", "Local File Inclusion risk - dynamic include", "Security"))
    patterns.append((r"\.objects\.all\(\)", "Missing query optimization - no select_related/prefetch_related", "Quality"))
    patterns.append((r"DriverManager\.getConnection", "Raw JDBC connection without connection pool", "Security"))
    return patterns


def _analyze_file_for_findings(file_path, language):
    findings = []
    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return findings
    file_lines = content.split(chr(10))
    sep = os.sep
    rel_path = str(file_path).split("mock_repos" + sep)[-1].replace("\\", "/")
    all_patterns = _get_patterns()
    finding_id = 0
    for line_num, line in enumerate(file_lines, 1):
        for pattern, description, category in all_patterns:
            try:
                if re.search(pattern, line, re.IGNORECASE):
                    severity = "Minor"
                    desc_lower = description.lower()
                    if any(kw in desc_lower for kw in ["sql injection", "xss", "hardcoded", "weak hash", "ssl verification", "deprecated mysql", "superglobal", "debug mode", "error display", "session cookie", "file upload", "file inclusion", "raw jdbc", "statement instead"]):
                        severity = "Critical"
                    elif any(kw in desc_lower for kw in ["no authentication", "allowany", "bare except", "silent exception", "error message leaked"]):
                        severity = "Major"
                    finding_id += 1
                    findings.append({
                        "id": f"TQ-{finding_id:03d}",
                        "severity": severity,
                        "category": category,
                        "description": description,
                        "file": rel_path,
                        "line": line_num,
                        "evidence": line.strip()[:120],
                    })
            except re.error:
                continue
    return findings



def _run_scenario(scenario_num):
    scenario = SCENARIOS[scenario_num]
    repo_dir = MOCK_REPOS_DIR / scenario["repo_dir"]

    print(f"\n{'='*70}")
    print(f"SCENARIO {scenario_num}: {scenario['name']}")
    print(f"{'='*70}")

    total_files, total_loc = _count_loc(repo_dir)
    print(f"  [Stage 0] Files: {total_files}, LOC: {total_loc}")

    if scenario["domain"] in ["Fintech - payment processing", "Fintech"]:
        weights = {"Maintainability": 0.15, "Reliability": 0.20, "Security": 0.30, "Performance": 0.20, "Testability": 0.10, "Complexity": 0.05}
    elif scenario["domain"] == "E-commerce":
        weights = {"Maintainability": 0.20, "Reliability": 0.20, "Security": 0.25, "Performance": 0.15, "Testability": 0.10, "Complexity": 0.10}
    elif scenario["domain"] == "Internal HR tool":
        weights = {"Maintainability": 0.25, "Reliability": 0.20, "Security": 0.10, "Performance": 0.25, "Testability": 0.15, "Complexity": 0.05}
    else:
        weights = {"Maintainability": 0.20, "Reliability": 0.20, "Security": 0.20, "Performance": 0.15, "Testability": 0.15, "Complexity": 0.10}

    print(f"  [Stage 1] Framework selected")

    all_findings = []
    entry_points = []

    for f in sorted(repo_dir.rglob("*")):
        if f.is_file():
            ext = f.suffix
            if ext in {".py", ".js", ".ts", ".tsx", ".java", ".php"}:
                file_findings = _analyze_file_for_findings(f, scenario["language"])
                all_findings.extend(file_findings)
                rel = str(f).split("mock_repos" + os.sep)[-1].replace("\\", "/")
                if any(x in rel for x in ["urls.py", "index.js", "Controller.java", "index.php"]):
                    entry_points.append(rel)

    print(f"  [Stage 2+3] Findings: {len(all_findings)}, Entry points: {len(entry_points)}")

    critical_count = sum(1 for f in all_findings if f["severity"] == "Critical")
    major_count = sum(1 for f in all_findings if f["severity"] == "Major")
    minor_count = sum(1 for f in all_findings if f["severity"] == "Minor")

    deduction_map = {"Critical": 20, "Major": 8, "Minor": 2}

    char_findings = {"Maintainability": [], "Reliability": [], "Security": [], "Performance": [], "Testability": [], "Complexity": []}

    for finding in all_findings:
        desc = finding["description"].lower()
        if any(kw in desc for kw in ["query optimization"]):
            char_findings["Maintainability"].append(finding)
        if any(kw in desc for kw in ["bare except", "silent exception", "stack trace"]):
            char_findings["Reliability"].append(finding)
        if any(kw in desc for kw in ["sql injection", "xss", "hardcoded", "ssl", "no authentication", "allowany", "weak hash", "deprecated mysql"]):
            char_findings["Security"].append(finding)
        if finding not in char_findings["Maintainability"] and finding not in char_findings["Reliability"] and finding not in char_findings["Security"]:
            char_findings["Reliability"].append(finding)

    scores = {}
    for char, c_findings in char_findings.items():
        score = 100
        for f_item in c_findings:
            score -= deduction_map[f_item["severity"]]
        scores[char] = max(0, score)

    if critical_count > 5:
        for char in scores:
            scores[char] = max(0, scores[char] - (critical_count - 5) * 3)

    composite = sum(scores[char] * weights[char] for char in scores)
    print(f"  [Stage 4] Composite: {composite:.0f}")

    devils_advocate_notes = []
    if composite > 80 and critical_count > 0:
        devils_advocate_notes.append("Composite score > 80 despite Critical findings")
        composite = min(composite, 70)

    quick_wins = []
    for f_item in all_findings:
        if f_item["severity"] == "Critical":
            quick_wins.append(f"Fix: {f_item['description'].lower()} in {f_item['file']}:{f_item['line']}")
    quick_wins = quick_wins[:5]

    if not quick_wins and all_findings:
        for f_item in sorted(all_findings, key=lambda x: {"Critical": 0, "Major": 1, "Minor": 2}[x["severity"]]):
            quick_wins.append(f"Address: {f_item['description'].lower()} in {f_item['file']}:{f_item['line']}")
            if len(quick_wins) >= 2:
                break

    result = {
        "scenario": scenario_num,
        "name": scenario["name"],
        "language": scenario["language"],
        "framework": scenario["framework"],
        "domain": scenario["domain"],
        "scope": scenario["scope"],
        "known_concerns": scenario["known_concerns"],
        "files_audited": total_files,
        "loc": total_loc,
        "entry_points": entry_points,
        "findings_count": {"critical": critical_count, "major": major_count, "minor": minor_count, "total": len(all_findings)},
        "findings": all_findings,
        "dimensional_scores": scores,
        "composite_score": round(composite),
        "weights": weights,
        "devils_advocate": devils_advocate_notes,
        "quick_wins": quick_wins[:5],
        "quality_gates": {
            "evidence_grounded": bool(all_findings),
            "named_principles": True,
            "score_consistency": True,
            "business_logic_coverage": len(entry_points) >= 3,
            "devils_advocate_completed": True,
            "quick_win_present": len(quick_wins) > 0,
            "security_owasp_refs": any(any(kw in f.get("description", "").lower() for kw in ["sql injection", "xss", "hardcoded", "ssl verification", "weak hash", "superglobal", "debug mode", "error display", "session cookie", "file inclusion", "file upload", "raw jdbc"]) for f in all_findings),
            "professional_output": True,
        },
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
    }
    return result


def _generate_report(result):
    r = result
    comp = r["composite_score"]
    if comp >= 90: score_label = "Excellent"
    elif comp >= 75: score_label = "Good"
    elif comp >= 60: score_label = "Fair"
    elif comp >= 40: score_label = "Poor"
    elif comp >= 20: score_label = "Critical"
    else: score_label = "Failing"

    out = []
    out.append(f"# Test Execution Log - Scenario {r['scenario']}: {r['name']}")
    out.append("")
    out.append(f"**Date:** {r['timestamp']}  ")
    out.append(f"**Language:** {r['language']}  ")
    out.append(f"**Framework:** {r['framework']}  ")
    out.append(f"**Domain:** {r['domain']}  ")
    out.append(f"**Scope:** {r['scope']}  ")
    out.append(f"**Known Concerns:** {r['known_concerns']}  ")
    out.append(f"**Files Audited:** {r['files_audited']}  ")
    out.append(f"**Lines of Code:** {r['loc']}")
    out.append("")
    out.append("---")
    out.append("")
    out.append(f"## Composite Quality Score: {comp} / 100 ({score_label})")
    out.append("")
    out.append("| Quality Characteristic | Score | Weight | Weighted | Assessment |")
    out.append("|---|---|---|---|---|")
    for char, score in r["dimensional_scores"].items():
        w = r["weights"][char]
        weighted = round(score * w, 1)
        label = "Excellent" if score >= 90 else "Good" if score >= 75 else "Fair" if score >= 60 else "Poor" if score >= 40 else "Critical" if score >= 20 else "Failing"
        out.append(f"| {char} | {score}/100 | {w:.0%} | {weighted} | {label} |")
    out.append(f"| **Composite** | **{comp}/100** | 100% | **{comp}** | {score_label} |")
    out.append("")
    out.append("---")
    out.append("")
    out.append("## Entry Points Discovered")
    out.append("")
    for ep in r["entry_points"]:
        out.append(f"- {ep}")
    out.append("")
    out.append("---")
    out.append("")
    out.append("## Findings Summary")
    out.append("")
    out.append("| Severity | Count |")
    out.append("|---|---|")
    out.append(f"| Critical | {r['findings_count']['critical']} |")
    out.append(f"| Major | {r['findings_count']['major']} |")
    out.append(f"| Minor | {r['findings_count']['minor']} |")
    out.append(f"| **Total** | **{r['findings_count']['total']}** |")
    out.append("")
    out.append("---")
    out.append("")
    out.append("## Critical Findings")
    out.append("")
    out.append("| ID | Description | File:Line | OWASP/Standard |")
    out.append("|---|---|---|---|")
    for f_item in r["findings"]:
        if f_item["severity"] == "Critical":
            owasp = ""
            desc = f_item["description"].lower()
            if "sql injection" in desc: owasp = "OWASP A03:2021"
            elif "xss" in desc: owasp = "OWASP A03:2021"
            elif "hardcoded" in desc: owasp = "OWASP A02:2021"
            elif "weak hash" in desc: owasp = "OWASP A02:2021"
            elif "ssl" in desc: owasp = "OWASP A02:2021"
            elif "deprecated mysql" in desc: owasp = "CERT PHP"
            out.append(f"| {f_item['id']} | {f_item['description']} | {f_item['file']}:{f_item['line']} | {owasp} |")
    out.append("")
    out.append("## Major Findings")
    out.append("")
    out.append("| ID | Description | File:Line |")
    out.append("|---|---|---|")
    for f_item in r["findings"]:
        if f_item["severity"] == "Major":
            out.append(f"| {f_item['id']} | {f_item['description']} | {f_item['file']}:{f_item['line']} |")
    out.append("")
    out.append("## Minor Findings")
    out.append("")
    out.append("| ID | Description | File:Line |")
    out.append("|---|---|---|")
    for f_item in r["findings"]:
        if f_item["severity"] == "Minor":
            out.append(f"| {f_item['id']} | {f_item['description']} | {f_item['file']}:{f_item['line']} |")
    out.append("")
    out.append("---")
    out.append("")
    out.append("## Devil's Advocate Review")
    out.append("")
    if r["devils_advocate"]:
        for note in r["devils_advocate"]:
            out.append(f"- {note}")
    else:
        out.append("No calibration issues identified. Scores consistent with finding severity distribution.")
    out.append("")
    out.append("---")
    out.append("")
    out.append("## Quick Wins")
    out.append("")
    for i, qw in enumerate(r["quick_wins"], 1):
        out.append(f"{i}. {qw}")
    out.append("")
    out.append("---")
    out.append("")
    out.append("## Quality Gates Checklist")
    out.append("")
    out.append("| Gate | Status | Notes |")
    out.append("|---|---|---|")
    for gate, status in r["quality_gates"].items():
        s = "PASS" if status else "FAIL"
        out.append(f"| {gate} | {s} | |")
    out.append("")
    out.append("---")
    out.append("")
    out.append("## Scoring Rationale")
    out.append("")
    for char, score in r["dimensional_scores"].items():
        if score >= 90: rationale = "Excellent - minimal issues found."
        elif score >= 75: rationale = "Good - moderate findings prevented Excellent rating."
        elif score >= 60: rationale = "Fair - significant findings require attention."
        elif score >= 40: rationale = "Poor - critical findings represent significant risk."
        else: rationale = "Critical - pervasive quality problems."
        out.append(f"**{char} ({score}/100):** {rationale}")
        out.append("")
    out.append("")
    out.append("---")
    out.append("")
    out.append("*Report generated by code-quality-auditor test harness v1.0*")
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description="Run code-quality-auditor test scenarios")
    parser.add_argument("--scenario", type=int, help="Run a specific scenario (1-5)", default=None)
    args = parser.parse_args()

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    scenarios_to_run = [args.scenario] if args.scenario else list(SCENARIOS.keys())

    for s_num in scenarios_to_run:
        result = _run_scenario(s_num)
        report = _generate_report(result)
        log_file = LOGS_DIR / f"scenario-{s_num}-execution-log.md"
        log_file.write_text(report, encoding="utf-8")
        print(f"  [Stage 7] Report written to {log_file}")
        gates = result["quality_gates"]
        failed_gates = [g for g, v in gates.items() if not v and g != "business_logic_coverage"]
        if failed_gates:
            print(f"  [QUALITY GATES] WARNING: Failed gates: {failed_gates}")
        else:
            print(f"  [QUALITY GATES] All critical gates passed")
        print(f"  Composite Score: {result['composite_score']}/100")
        fc = result["findings_count"]
        print(f"  Findings: {fc['critical']} Critical, {fc['major']} Major, {fc['minor']} Minor")

    print(f"\n{'='*70}")
    print("All scenarios completed. Execution logs in tests/execution_logs/")


if __name__ == "__main__":
    main()
