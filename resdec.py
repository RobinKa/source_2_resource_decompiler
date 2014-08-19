from particledecompiler import ParticleDecompiler
import os
import sys

def decompile_file(path):
    ext = os.path.splitext(path)[1]
    
    if not ext.endswith("_c"):
        print("Input file is not a _c compiled file.")
        return
    
    output_name = ""
    
    if len(sys.argv) == 3:
        output_name = sys.argv[2]
    else:
        output_name = os.path.basename(path) + "_decompiled" + ext[:-2]

    decompiler = None
    
    print("File " + path)
    
    if ext == ".vpcf_c":
        print("Decompiling with particle decompiler...")
        decompiler = ParticleDecompiler()
    else:
        print("Unknown extension " + ext)
        return
        
    decompiler.decompile(path, output_name)

def main():
    if len(sys.argv) < 2:
        print("Invalid arguments.")
        print("Usage: resdec <filename> <optional output_name>")
        return
        
    file_name = sys.argv[1]
    
    if file_name.endswith("*"):
        directory = file_name[:-1]
        for file in os.listdir(directory):
            if file.endswith("_c"):
                decompile_file(os.path.join(directory, file))
    else:
        decompile_file(file_name)
       
if __name__ == "__main__":
    main()
    