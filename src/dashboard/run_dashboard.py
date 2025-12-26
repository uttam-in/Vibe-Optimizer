"""
Quick start script for the dashboard
"""
import os
import sys
import subprocess

def main():
    """Run the Streamlit dashboard"""
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(script_dir, 'app.py')
    
    # Check if app.py exists
    if not os.path.exists(app_path):
        print(f"Error: app.py not found at {app_path}")
        sys.exit(1)
    
    # Check if data file exists
    data_path = os.path.join(script_dir, '..', '..', 'data', 'sentimentdataset.csv')
    if not os.path.exists(data_path):
        print(f"Warning: Data file not found at {data_path}")
        print("You may need to configure the data path in the dashboard.")
    
    # Check if model exists
    model_path = os.path.join(script_dir, '..', '..', 'models', 'sentiment_model.pkl')
    if not os.path.exists(model_path):
        print(f"Warning: Sentiment model not found at {model_path}")
        print("The dashboard will use VADER as fallback.")
        print("To train the model, run: python src/analysis/model_trainer.py")
    
    print("\n" + "="*60)
    print("Starting Vibe Optimizer Dashboard...")
    print("="*60 + "\n")
    
    # Run streamlit
    try:
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', app_path,
            '--server.headless', 'true'
        ])
    except KeyboardInterrupt:
        print("\n\nDashboard stopped.")
    except Exception as e:
        print(f"\nError running dashboard: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
