name: Build and Deploy hrcp.com

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 7 * * *'
  workflow_dispatch:

permissions:
  contents: write
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Delete all old files (keep only build.py and workflow)
        run: |
          # Remove every tracked file except build.py and .github/
          FILES=$(git ls-files | grep -vE '^(build\.py|\.github/)' || true)
          if [ -n "$FILES" ]; then
            echo "$FILES" | xargs git rm -f --ignore-unmatch
          else
            echo "No files to remove"
          fi

          # Hard-delete anything untracked at root level
          find . -maxdepth 1 \
            ! -name '.' \
            ! -name 'build.py' \
            ! -name '.git' \
            ! -name '.github' \
            -exec rm -rf {} +

          # Clean any previous output folder
          rm -rf output/

          # Commit the purge
          git config user.name  "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add -A
          git commit -m "chore: purge all old files before rebuild [skip ci]" || echo "Nothing to commit"
          git push || echo "Nothing to push"

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Build site
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: python build.py

      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: output

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
