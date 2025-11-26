from google.colab import userdata
import subprocess

def sync_to_github(commit_message="Updated baseball simulation"):
    """Sync all changes to GitHub"""
    
    token = userdata.get('CLASSIC_GITHUB_TOKEN')
    

    print("=== Git Status ===")
    subprocess.run(['git', 'status'], check=False)
    
    print("\n=== Adding files ===")
    subprocess.run(['git', 'add', '.'], check=True)
    
    print(f"\n=== Committing: {commit_message} ===")
    result = subprocess.run(['git', 'commit', '-m', commit_message], 
                          capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        if "nothing to commit" in result.stderr:
            print("No changes to commit!")
            return
    
    print("\n=== Pushing to GitHub ===")
    repo_url = f"https://{token}@github.com/ArterioRodrigues/baseball-simulation.git"
    subprocess.run(['git', 'push', repo_url, 'main'], check=True)
    
    print("\n✅ Successfully synced to GitHub!")

sync_to_github("Updated baseball simulation")