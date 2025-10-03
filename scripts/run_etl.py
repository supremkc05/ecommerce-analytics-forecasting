import sys
import os
from pathlib import Path

#parent directory
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

def main():
    """Main entry point for ETL pipeline"""
    print("Starting Ecommerce Analytics ETL Pipeline...")
    
    try:
        #import gareako robust_etl
        from etl.robust_etl import RobustETL
        
        # Initialize and run ETL
        etl = RobustETL()
        success = etl.run_etl()
        
        if success:
            print("ETL Pipeline completed successfully!")
            return 0
        else:
            print("ETL Pipeline failed!")
            return 1
            
    except ImportError as e:
        print(f"Error importing ETL module: {e}")
        print("Current working directory:", os.getcwd())
        print("Python path:", sys.path[:3])
        print("Make sure you're running from the project root directory")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)