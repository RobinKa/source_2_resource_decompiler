from particledecompiler import ParticleDecompiler
import os
import sys

def main():
    if len(sys.argv) < 2:
        print("Invalid arguments.")
        print("Usage: resdec <filename> <optional output_name>")
        return
        
    file_name = sys.argv[1]
    ext = os.path.splitext(file_name)[1]
    
    if not ext.endswith("_c"):
        print("Input file is not a _c compiled file.")
        return
    
    output_name = ""
    
    if len(sys.argv) == 3:
        output_name = sys.argv[2]
    else:
        output_name = os.path.basename(file_name) + "_decompiled" + ext[:-2]

    decompiler = None
    
    if ext == ".vpcf_c":
        print("Decompiling with particle decompiler...")
        decompiler = ParticleDecompiler()
    else:
        print("Unknown extension " + ext)
        return
        
    decompiler.decompile(file_name, output_name)
       
if __name__ == "__main__":
    main()
    