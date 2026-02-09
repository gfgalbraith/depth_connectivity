# ARE + Git workflow

Key constraints:
- ARE runs in a container
- /home and /g/data are read-only
- work happens in /scratch
- persistence comes from git

Golden loop:

git status
git add -A
git commit -m "Describe what you did"
git push

# Then to edit git ignore
nano .gitignore
control + o to save
control + x to exit

