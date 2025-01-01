import os
import re
import platform

# Get the current working directory
current_folder = os.getcwd()

# Check if any .class file exists in the current directory and join them into a single string
class_files = ', '.join(f[:-6] for f in os.listdir(current_folder) if f.endswith('.class'))

# Function to run commands based on the OS
def run_command(command):
    system_os = platform.system().lower()
    if system_os == 'windows':
        os.system(f'cmd /c "{command}"')
    else:
        os.system(command)

# Main logic
if class_files:
    print(f".class files found: {class_files}")
    testers_files = ', '.join(f for f in os.listdir(current_folder) if f.endswith('.txt'))
    
    if testers_files:
        print(f".txt files found: {testers_files}")
        # Assuming you want to run Java on the .txt files with the found .class file
        run_command(f"java {class_files} {testers_files}")
        
        while True:  # Loop for re-running the result
            repeat = input("Do you want to run the result again? (yes/no): ").strip().lower()
            if repeat == "yes":
                run_command(f"java {class_files} {testers_files}")
            elif repeat == "no":
                break
            else:
                print("Please enter 'yes' or 'no'.")
    else:
        print("No .txt files found in the current folder.")
else:
    while True:
        # Get input for the .lex file and the .txt test file
        lexer = input("Write your file.lex: ") + ".lex"
        tester = input("Write the file you are going to test with: ") + ".txt"
        
        if not os.path.exists(lexer):
            print(f"Error: The file {lexer} was not found. Please try again.")
            continue
        
        if not os.path.exists(tester):
            print(f"Error: The file {tester} was not found. Please try again.")
            continue

        # Extract the class name from the .lex file
        try:
            with open(lexer, 'r') as file:
                content = file.read()
                match = re.search(r'%class\s+(\w+)', content)  # Search for the %class directive
                if match:
                    class_name = match.group(1)
                else:
                    print("Error: Could not find a %class directive in the .lex file.")
                    continue
        except FileNotFoundError:
            print(f"Error: The file {lexer} was not found. Please try again.")
            continue
        
        # Run jflex to generate the .java file
        run_command(f"jflex {lexer}")

        # The generated .java file name is the class name + ".java"
        generated_java = f"{class_name}.java"

        # Compile the generated .java file
        run_command(f"javac {generated_java}")

        # Execute the compiled Java class with the test file
        run_command(f"java {class_name} {tester}")

        # Ask if the user wants to run the result again
        while True:  # Loop for re-running the result
            repeat = input("Do you want to run the result again? (yes/no): ").strip().lower()
            if repeat == "yes":
                run_command(f"java {class_name} {tester}")
            elif repeat == "no":
                break
            else:
                print("Please enter 'yes' or 'no'.")

        # Ask if the user wants to start a new process
        new_process = input("Do you want to run a new process? (yes/no): ").strip().lower()
        if new_process != "yes":
            break
