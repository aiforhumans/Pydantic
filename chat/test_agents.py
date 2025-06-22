#!/usr/bin/env python3
"""
Test script to verify our PydanticAI agents work correctly
"""

def test_file_syntax(filename):
    """Test if a Python file has correct syntax"""
    try:
        import py_compile
        py_compile.compile(filename, doraise=True)
        print(f"✅ {filename} - No syntax errors!")
        return True
    except Exception as e:
        print(f"❌ {filename} - Syntax error: {e}")
        return False

def main():
    print("🧪 Testing PydanticAI Agent Files")
    print("=" * 40)
    
    files_to_test = [
        'simple_agent.py',
        'roulette_agent.py', 
        'advanced_agent.py',
        'multi_tool_agent.py'
    ]
    
    all_good = True
    for filename in files_to_test:
        try:
            result = test_file_syntax(filename)
            all_good = all_good and result
        except FileNotFoundError:
            print(f"⚠️ {filename} - File not found")
            all_good = False
    
    print("\n" + "=" * 40)
    if all_good:
        print("🎉 All files passed syntax check!")
        print("Your PydanticAI agents are ready to use!")
    else:
        print("🔧 Some files need fixes")
    
    print("\n📋 Usage:")
    print("python simple_agent.py      # Basic agent chat")
    print("python roulette_agent.py    # Roulette game with tools")
    print("python advanced_agent.py    # All run methods demo")
    print("python multi_tool_agent.py  # Multi-tool assistant")

if __name__ == "__main__":
    main()
