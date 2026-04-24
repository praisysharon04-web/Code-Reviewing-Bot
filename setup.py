"""
setup.py - Complete project initialization script

Run this AFTER you've copied all the downloaded files to this folder.
It will organize everything and create missing files.

Usage: python setup.py
"""

import os
import shutil
from pathlib import Path

def setup_project():
    """Setup project structure and organize files"""
    
    print("\n" + "="*50)
    print("  CODE REVIEWER BOT - PROJECT SETUP")
    print("="*50 + "\n")
    
    # Define base folder
    base_dir = Path(".")
    
    # Create folder structure
    folders = ["src", "api", "ui", "examples", "tests"]
    
    print("[1/5] Creating folder structure...")
    for folder in folders:
        folder_path = base_dir / folder
        folder_path.mkdir(exist_ok=True)
        print(f"      ✓ {folder}/")
    
    # Create __init__.py files
    print("\n[2/5] Creating __init__.py files...")
    init_files = [
        "src/__init__.py",
        "api/__init__.py",
        "ui/__init__.py",
        "examples/__init__.py",
        "tests/__init__.py"
    ]
    
    for init_file in init_files:
        init_path = base_dir / init_file
        if not init_path.exists():
            init_path.touch()
            print(f"      ✓ {init_file}")
    
    # Rename files if they exist
    print("\n[3/5] Organizing downloaded files...")
    
    file_mappings = {
        "src_reviewer.py": "src/reviewer.py",
        "src_llm_provider.py": "src/llm_provider.py",
        "api_main.py": "api/main.py",
        "ui_app.py": "ui/app.py",
        "examples_usage.py": "examples/usage_examples.py",
    }
    
    for source, dest in file_mappings.items():
        source_path = base_dir / source
        dest_path = base_dir / dest
        
        if source_path.exists():
            if not dest_path.exists():
                shutil.move(str(source_path), str(dest_path))
                print(f"      ✓ {source} → {dest}")
            else:
                print(f"      ~ {dest} already exists (skipped)")
        else:
            print(f"      ⚠ {source} not found (you'll need to copy it manually)")
    
    # Create .env file if it doesn't exist
    print("\n[4/5] Creating configuration files...")
    env_file = base_dir / ".env"
    if not env_file.exists():
        with open(env_file, "w") as f:
            f.write("""# LLM Provider Configuration
LLM_PROVIDER=mock

# Optional API Keys (uncomment and add your keys)
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
# HUGGINGFACE_API_KEY=hf_...

# Server Settings
PORT=8000
HOST=0.0.0.0
""")
        print("      ✓ .env configuration file created")
    else:
        print("      ~ .env already exists (skipped)")
    
    # Create .env.example
    env_example = base_dir / ".env.example"
    if not env_example.exists():
        with open(env_example, "w") as f:
            f.write("""# LLM Provider Configuration
LLM_PROVIDER=mock

# Optional API Keys (uncomment and add your keys)
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
# HUGGINGFACE_API_KEY=hf_...

# Server Settings
PORT=8000
HOST=0.0.0.0
""")
        print("      ✓ .env.example created")
    
    # Verify structure
    print("\n[5/5] Verifying project structure...")
    
    required_files = [
        "src/reviewer.py",
        "src/llm_provider.py",
        "api/main.py",
        "ui/app.py",
        "examples/usage_examples.py",
        "requirements.txt",
        "README.md",
    ]
    
    all_good = True
    for file_path in required_files:
        path = base_dir / file_path
        if path.exists():
            print(f"      ✓ {file_path}")
        else:
            print(f"      ✗ {file_path} (MISSING - copy it manually)")
            all_good = False
    
    # Print summary
    print("\n" + "="*50)
    if all_good:
        print("  ✓ PROJECT SETUP COMPLETE!")
    else:
        print("  ⚠ Setup partial - some files missing")
    print("="*50)
    
    print("\nNext steps:")
    print("  1. If any files are missing, copy them from Downloads")
    print("  2. Run: python -m venv venv")
    print("  3. Run: venv\\Scripts\\activate")
    print("  4. Run: pip install -r requirements.txt")
    print("  5. Run: streamlit run ui/app.py")
    print("\n")

if __name__ == "__main__":
    try:
        setup_project()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        input("Press Enter to exit...")
