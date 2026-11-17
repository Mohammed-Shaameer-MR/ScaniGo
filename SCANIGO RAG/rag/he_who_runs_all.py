import subprocess
import sys

python=sys.executable

files=[
    "rag/index_builder.py","rag/augmented_prompt_&_generator.py"
]

for file in files:
    print("\n")
    print(f"-----Currently Running {file}-----")
    result=subprocess.run([python,file])

    if result.returncode!=0:
        print(f"Error occured when handling {file}.")
        break
    else:
        print("\n")
        print(f"{file} got executed sucessfully")



        
        
    