#!/bin/bash
# Robot Otomatis Zerix PR
if [ -z "$1" ]; then
  echo "Error: Masukkan pesan commit! Contoh: bash pr.sh 'feat: tambah fitur'"
  exit 1
fi

MSG="$1"
BRANCH="auto/$(date +%s)"

echo "🤖 Membuat branch: $BRANCH"
git checkout -b "$BRANCH"

echo "🤖 Menyimpan perubahan..."
git add .
git commit -m "$MSG"

echo "🤖 Mengirim ke GitHub..."
git push -u origin "$BRANCH"

echo "🤖 Membuat Pull Request..."
gh pr create --title "$MSG" --body "Automated PR generated via Termux." --base main --head "$BRANCH"

echo "🤖 Melakukan Merge..."
gh pr merge "$BRANCH" --merge --delete-branch

echo "🤖 Berpindah kembali ke main..."
git checkout main
git pull origin main

echo "✅ Selesai! Fitur sudah masuk ke main dengan aman."
