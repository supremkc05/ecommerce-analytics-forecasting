
import sys
import os
from pathlib import Path

#path setup
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

def main():
    """Run analysis scripts"""
    print("📊 Starting Ecommerce Data Analysis...")
    
    try:
        # Import and run final_status
        print("🔍 Running database status check...")
        sys.path.append(str(src_path / "analysis"))
        
        # Import final_status function and run it
        import final_status
        final_status.final_status()
        
        print("\n📈 Running data analysis...")
        # Import and run analyze_data
        import analyze_data
        analyze_data.main()
        
        print("✅ Analysis completed successfully!")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        print(f"📁 Current working directory: {os.getcwd()}")
        print(f"🔍 Python path: {sys.path[:3]}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)