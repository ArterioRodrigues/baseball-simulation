# See what changed
git status

# Add all changes
git add .

# Commit with a message
git commit -m "Updated baseball simulation"

# Push to GitHub using your token
from google.colab import userdata
token = userdata.get('GITHUB_TOKEN')
git push https://{token}@github.com/ArterioRodrigues/baseball-simulation.git