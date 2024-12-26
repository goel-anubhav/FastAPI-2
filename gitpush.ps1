# Prompt the user for the commit message
$commitMessage = Read-Host "Enter your commit message"

# Stage all changes
git add .

# Commit with the provided message
git commit -m $commitMessage

# Push the changes
git push