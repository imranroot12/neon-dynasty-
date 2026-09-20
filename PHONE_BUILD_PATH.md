# Neon Dynasty — no-PC production path

A PC is not required if the project is placed in a GitHub repository. The included workflow is designed for GitHub Actions and performs the official Engine Math SDK optimization, Web SDK build, and release gate in a cloud runner.

## Phone workflow
1. Put the Build 60 repository contents into a GitHub repository.
2. Open the repository on a phone browser.
3. Open **Actions** → **Neon Dynasty production gate**.
4. Choose **Run workflow**.
5. Wait for the workflow to finish.
6. If successful, download the `neon-dynasty-production` artifact.

The workflow performs the Rust/Python/Node production build in GitHub's cloud runner; the phone does not need the development tools installed.
