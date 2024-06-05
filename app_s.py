import os

file_path = "./static/upload/"+'ranjeev2210215@ssn.edu.innoc24-cs15.pdf'

if os.path.exists(file_path):
    os.remove(file_path)
    print(f"{file_path} has been deleted successfully.")
else:
    print(f"{file_path} does not exist.")