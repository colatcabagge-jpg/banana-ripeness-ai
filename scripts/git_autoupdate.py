import subprocess
import sys

def run(cmd):
    return subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )

def main():
    print("🔍 Checking local Git status...")

    status = run("git status --porcelain")
    if status.stdout.strip():
        print("⚠️ Local changes detected.")
        print("Auto-update skipped to protect your work.")
        return

    print("📡 Fetching updates from GitHub...")
    run("git fetch")

    behind = run("git status -uno")

    if "behind" in behind.stdout:
        print("🔄 Updates found. Pulling latest changes...")
        pull = run("git pull --rebase")
        if pull.returncode != 0:
            print("❌ Git pull failed.")
            print(pull.stderr)
            sys.exit(1)
        print("✅ Repository updated successfully.")
    else:
        print("✅ Repository already up to date.")

if __name__ == "__main__":
    main()
