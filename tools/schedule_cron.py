# schedule_cron.py — code-quality-auditor skill
# Sets up a weekly cron job to run knowledge_updater.py.
# Supports both Windows Task Scheduler and Unix crontab.
#
# Usage:
#   python tools/schedule_cron.py              # interactive: detect OS and set up
#   python tools/schedule_cron.py --dry-run    # preview what would be configured
#   python tools/schedule_cron.py --uninstall  # remove the scheduled task
#

from __future__ import annotations

import argparse
import os
import platform
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
UPDATER_SCRIPT = SKILL_DIR / "tools" / "knowledge_updater.py"
LOG_FILE = SKILL_DIR / "tools" / "crawl_log.txt"
BATCH_WRAPPER = SKILL_DIR / "tools" / "run_knowledge_update.bat"

CRON_DAY = "Monday"
CRON_DAY_ABBREV = "MON"  # Windows schtasks uses MON, TUE, etc.
CRON_TIME = "03:00"  # 3 AM UTC on Monday
TASK_NAME = "CodeQualityAuditor_KnowledgeUpdate"


def _is_windows() -> bool:
    return platform.system() == "Windows"


def _python_executable() -> str:
    return sys.executable


def _dry_run_message(msg: str) -> None:
    print(f"[DRY-RUN] {msg}")


def _ensure_batch_wrapper() -> None:
    """Create the batch wrapper script if it doesn't exist."""
    python = _python_executable()
    script = str(UPDATER_SCRIPT)
    log = str(LOG_FILE)

    batch_content = (
        '@echo off\r\n'
        'REM Wrapper script for code-quality-auditor knowledge_updater.py\r\n'
        'REM Created by schedule_cron.py for Windows Task Scheduler\r\n'
        'REM This wrapper handles output redirection since schtasks /TR does not support shell redirects.\r\n'
        '\r\n'
        f'echo [%DATE% %TIME%] Starting knowledge_updater.py >> "{log}"\r\n'
        f'"{python}" "{script}" >> "{log}" 2>&1\r\n'
        f'echo [%DATE% %TIME%] Completed knowledge_updater.py (exit code %%ERRORLEVEL%%) >> "{log}"\r\n'
    )
    BATCH_WRAPPER.write_text(batch_content, encoding="utf-8")
    print(f"  Batch wrapper created: {BATCH_WRAPPER}")


def _setup_windows_task(dry_run: bool = False) -> None:
    """Create a Windows Task Scheduler task that runs knowledge_updater.py weekly."""
    if not dry_run:
        _ensure_batch_wrapper()

    wrapper = str(BATCH_WRAPPER)

    # schtasks /create flags:
    #   /TN  - task name
    #   /TR  - task run command (use batch wrapper for redirect support)
    #   /SC  - schedule type (WEEKLY)
    #   /D   - day of week (abbreviated: MON, TUE, etc.)
    #   /ST  - start time (HH:MM, 24h)
    #   /F   - force overwrite if exists
    cmd = [
        "schtasks", "/create",
        "/tn", TASK_NAME,
        "/tr", f'"{wrapper}"',
        "/sc", "WEEKLY",
        "/d", CRON_DAY_ABBREV,
        "/st", CRON_TIME,
        "/f",
    ]

    if dry_run:
        _dry_run_message(f"Would create Windows scheduled task: {TASK_NAME}")
        _dry_run_message(f"  Command: {' '.join(cmd)}")
        _dry_run_message(f"  Schedule: Every {CRON_DAY} at {CRON_TIME}")
        _dry_run_message(f"  Batch wrapper: {wrapper}")
        _dry_run_message(f"  Script: {UPDATER_SCRIPT}")
        _dry_run_message(f"  Log: {LOG_FILE}")
        return

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"[OK] Windows Task Scheduler task created: {TASK_NAME}")
        print(f"  Schedule: Every {CRON_DAY} at {CRON_TIME}")
        print(f"  Batch wrapper: {wrapper}")
        print(f"  Script: {UPDATER_SCRIPT}")
        print(f"  Log: {LOG_FILE}")
        if result.stdout:
            print(f"  Output: {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to create scheduled task: {e}")
        if e.stderr:
            print(f"  stderr: {e.stderr.strip()}")
        print("  Try running as Administrator.")
        sys.exit(1)
    except FileNotFoundError:
        print("[ERROR] schtasks command not found. Are you on Windows?")
        sys.exit(1)


def _uninstall_windows_task(dry_run: bool = False) -> None:
    """Remove the Windows Task Scheduler task."""
    cmd = ["schtasks", "/delete", "/tn", TASK_NAME, "/f"]

    if dry_run:
        _dry_run_message(f"Would delete Windows scheduled task: {TASK_NAME}")
        _dry_run_message(f"  Command: {' '.join(cmd)}")
        return

    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"[OK] Windows scheduled task deleted: {TASK_NAME}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to delete scheduled task: {e}")
        if e.stderr:
            print(f"  stderr: {e.stderr.strip()}")
        sys.exit(1)
    except FileNotFoundError:
        print("[ERROR] schtasks command not found.")
        sys.exit(1)


def _setup_unix_cron(dry_run: bool = False) -> None:
    """Create a Unix crontab entry for weekly knowledge_updater.py execution."""
    python = _python_executable()
    script = str(UPDATER_SCRIPT)
    log = str(LOG_FILE)

    # Cron format: minute hour day-of-month month day-of-week command
    # Monday = 1 in crontab (0=Sunday)
    # 3 AM UTC on Monday: 0 3 * * 1
    cron_entry = f"0 3 * * 1 {python} {script} >> {log} 2>&1  # {TASK_NAME}"

    if dry_run:
        _dry_run_message("Would add crontab entry:")
        _dry_run_message(f"  {cron_entry}")
        return

    try:
        # Read existing crontab
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        existing = result.stdout if result.returncode == 0 else ""

        # Check if entry already exists
        if TASK_NAME in existing:
            print(f"[OK] Crontab entry already exists: {TASK_NAME}")
            return

        # Add new entry
        new_crontab = existing.rstrip("\n") + "\n" + cron_entry + "\n"
        process = subprocess.run(
            ["crontab", "-"],
            input=new_crontab,
            capture_output=True,
            text=True,
        )
        if process.returncode == 0:
            print(f"[OK] Crontab entry created: {TASK_NAME}")
            print(f"  Schedule: Every Monday at 03:00 UTC")
            print(f"  Script: {script}")
            print(f"  Log: {log}")
        else:
            print(f"[ERROR] Failed to update crontab: {process.stderr.strip()}")
            sys.exit(1)
    except FileNotFoundError:
        print("[ERROR] crontab command not found. Is cron installed?")
        sys.exit(1)


def _uninstall_unix_cron(dry_run: bool = False) -> None:
    """Remove the crontab entry."""
    if dry_run:
        _dry_run_message(f"Would remove crontab entry: {TASK_NAME}")
        return

    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        if result.returncode != 0:
            print("[OK] No crontab to modify.")
            return

        existing = result.stdout
        lines = [
            line for line in existing.split("\n")
            if TASK_NAME not in line
        ]
        new_crontab = "\n".join(lines).strip() + "\n"
        process = subprocess.run(
            ["crontab", "-"],
            input=new_crontab,
            capture_output=True,
            text=True,
        )
        if process.returncode == 0:
            print(f"[OK] Crontab entry removed: {TASK_NAME}")
        else:
            print(f"[ERROR] Failed to update crontab: {process.stderr.strip()}")
            sys.exit(1)
    except FileNotFoundError:
        print("[ERROR] crontab command not found.")
        sys.exit(1)


def _setup(dry_run: bool = False) -> None:
    """Detect OS and set up the appropriate scheduler."""
    print(f"=== code-quality-auditor Cron Setup ===")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Python: {_python_executable()}")
    print(f"Script: {UPDATER_SCRIPT}")
    print(f"Schedule: Every {CRON_DAY} at {CRON_TIME}")
    print()

    if not UPDATER_SCRIPT.exists():
        print(f"[ERROR] knowledge_updater.py not found at {UPDATER_SCRIPT}")
        sys.exit(1)

    if _is_windows():
        _setup_windows_task(dry_run)
    else:
        _setup_unix_cron(dry_run)

    if not dry_run:
        print()
        print("Next steps:")
        print(f"  - Verify the task is scheduled: schtasks /query /tn \"{TASK_NAME}\"")
        print("  - Check logs after first run: tools/crawl_log.txt")
        print("  - To uninstall: python tools/schedule_cron.py --uninstall")


def _uninstall(dry_run: bool = False) -> None:
    """Remove the scheduled task."""
    print(f"=== Uninstalling {TASK_NAME} ===")

    if _is_windows():
        _uninstall_windows_task(dry_run)
    else:
        _uninstall_unix_cron(dry_run)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Set up weekly cron job for code-quality-auditor knowledge_updater.py"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be configured without making changes",
    )
    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="Remove the scheduled task",
    )
    args = parser.parse_args()

    if args.uninstall:
        _uninstall(dry_run=args.dry_run)
    else:
        _setup(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
