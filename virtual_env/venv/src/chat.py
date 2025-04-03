import subprocess
import os

# Get absolute base directory (one level up from src/)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Paths to the model and binary
MODEL_PATH = os.path.join(BASE_DIR, "llama.cpp", "models", "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf")
LLAMA_BIN = os.path.join(BASE_DIR, "llama.cpp", "build", "bin", "llama-cli")

def get_grok_response(prompt):
    cmd = [LLAMA_BIN, "-m", MODEL_PATH, "-p", f"Grok: {prompt}", "--ctx-size", "512"]

    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=os.path.join(BASE_DIR, "llama.cpp"), bufsize=1)

        response = []
        for line in iter(process.stdout.readline, ''):  # Read line by line
            print(line, end="")  # Print for debugging
            response.append(line.strip())

        process.stdout.close()
        process.wait(timeout=10)  # Prevent indefinite hanging

        return "\n".join(response)

    except subprocess.TimeoutExpired:
        process.kill()
        return "Error: The model took too long to respond."

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print("Grok: Hello! I’m your local assistant. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Grok: Goodbye!")
            break
        response = get_grok_response(user_input)
        print(f"Grok: {response}")
