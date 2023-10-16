import os
import secrets
from dotenv import load_dotenv

print("-----------------------------------------------------------------------------------------")
print("Starting the script")

# Generating a random 16-digit string
secret_key = ''.join(secrets.choice('ABCdef*#0123') for i in range(16))

# Checking if .env file exists
if os.path.isfile('.env'):
    
    #Loading environment variables from .env file if it exists
    load_dotenv()

    # If .env already exists, updating SECRET_KEY
    with open('.env', 'r') as env_file:
        lines = env_file.readlines()
    
    with open('.env', 'w') as env_file:
        updated = False
        for line in lines:
            if line.startswith('SECRET_KEY='):
                env_file.write(f'SECRET_KEY={secret_key}\n')
                updated = True
            else:
                env_file.write(line)
        if not updated:
            env_file.write(f'SECRET_KEY={secret_key}\n')
        print(".env updated with a new secret_key")
else:
    # If .env doesn't exist, creating it with SECRET_KEY
    with open('.env', 'w') as env_file:
        env_file.write(f'SECRET_KEY={secret_key}\n')
        print(".env created with secret_key")


command = "python3 app.py"

print("Running the app")
print("-----------------------------------------------------------------------------------------")

os.system(command)

