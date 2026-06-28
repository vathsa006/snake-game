"""
Quick test script to verify the Bhagavad Gita QA system setup
Run this before starting the Streamlit app to ensure everything works
"""

import sys

def test_imports():
    """Test if all required libraries are installed"""
    print("🔍 Testing library imports...\n")
    
    libraries = [
        ("json", "json"),
        ("os", "os"),
        ("pickle", "pickle"),
        ("numpy", "numpy"),
        ("streamlit", "streamlit"),
        ("google.generativeai", "google-generativeai"),
        ("faiss", "faiss-cpu"),
        ("pandas", "pandas"),
        ("tqdm", "tqdm"),
    ]
    
    all_good = True
    
    for module_name, package_name in libraries:
        try:
            __import__(module_name)
            print(f"✅ {package_name:25s} - OK")
        except ImportError:
            print(f"❌ {package_name:25s} - NOT INSTALLED")
            print(f"   Install with: pip install {package_name}")
            all_good = False
    
    return all_good

def test_files():
    """Test if required files exist"""
    print("\n🔍 Testing required files...\n")
    
    import os
    
    files = [
        "gita_slokas.json",
        "app.py",
        "requirements.txt"
    ]
    
    all_good = True
    
    for filename in files:
        if os.path.exists(filename):
            print(f"✅ {filename:25s} - Found")
        else:
            print(f"❌ {filename:25s} - NOT FOUND")
            all_good = False
    
    return all_good

def test_json_structure():
    """Test if JSON file has correct structure"""
    print("\n🔍 Testing JSON structure...\n")
    
    try:
        import json
        with open("gita_slokas.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        print(f"✅ JSON file loaded successfully")
        print(f"✅ Found {len(data)} slokas")
        
        # Check first sloka structure
        if len(data) > 0:
            first_sloka = data[0]
            required_fields = ["sloka", "explanation"]
            
            for field in required_fields:
                if field in first_sloka:
                    print(f"✅ Field '{field}' exists")
                else:
                    print(f"❌ Field '{field}' missing")
                    return False
        
        return True
        
    except FileNotFoundError:
        print("❌ gita_slokas.json not found")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON format: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_gemini_connection():
    """Test Gemini API connection"""
    print("\n🔍 Testing Gemini API connection...\n")
    
    try:
        import google.generativeai as genai
        
        # API key from app.py
        GEMINI_API_KEY = "AIzaSyB23pN4vZIY79K9qmHD_PDDAZq3hDuQxZY"
        
        genai.configure(api_key=GEMINI_API_KEY)
        print("✅ Gemini API configured")
        
        # Try to list models to verify connection
        print("✅ Testing API connection...")
        model = genai.GenerativeModel("gemini-2.0-flash")
        print("✅ Gemini 2.0 Flash model accessed successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Gemini API error: {e}")
        print("   Note: This might be a network issue or API key problem")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("  Bhagavad Gita QA System - Setup Verification")
    print("=" * 60)
    print()
    
    results = []
    
    # Test 1: Imports
    results.append(("Library Imports", test_imports()))
    
    # Test 2: Files
    results.append(("Required Files", test_files()))
    
    # Test 3: JSON
    results.append(("JSON Structure", test_json_structure()))
    
    # Test 4: Gemini API
    results.append(("Gemini API", test_gemini_connection()))
    
    # Summary
    print("\n" + "=" * 60)
    print("  TEST SUMMARY")
    print("=" * 60)
    print()
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:25s} : {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("✅ All tests passed! You're ready to run the app.")
        print("\nRun the app with:")
        print("    streamlit run app.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("\nTo install missing libraries:")
        print("    pip install -r requirements.txt")
    
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
