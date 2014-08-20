from particledecompiler import ParticleDecompiler
import os
import sys
import multiprocessing

def decompile_file(args):
    path = args[0]
    out_path = args[1]

    ext = os.path.splitext(path)[1]
    
    if not ext.endswith("_c"):
        print("Input file is not a _c compiled file.")
        return
        
    #Check if the file already exists
    if os.path.exists(out_path):
        return
        
    #Create the output directory if it doesnt exist yet
    output_dir = os.path.dirname(out_path)
    if output_dir != "" and not os.path.isdir(output_dir):
        print("Directory didnt exist: " + output_dir)
        return

    decompiler = None
    
    if ext == ".vpcf_c":
        decompiler = ParticleDecompiler()
    else:
        print("Unknown extension " + ext)
        return
        
    decompiler.decompile(path, out_path)

def files_by_pattern(directory, match_func):
    out_files = []
    for path, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith(".vpcf_c"):
                out_files.append(os.path.join(path, f))
    return out_files
    
def main():
    if len(sys.argv) < 2:
        print("Invalid arguments.")
        print("Usage: resdec <filename> <optional output_name>")
        return
        
    file_name = sys.argv[1]
    
    if file_name.endswith("*"):
        directory = file_name[:-1]
        files = files_by_pattern(directory, lambda fn: fn.endswith(".vpcf_c"))
        print("File count: " + str(len(files)))
        
        output_dir = ""
        if len(sys.argv) == 3:
            output_dir = sys.argv[2]
        
        args = []
        for file in files:
            out_name = os.path.join(output_dir, os.path.relpath(file, directory)[:-2])
            args.append((file, out_name))
            
            #Create directories beforehand cause multithreaded i/o is annoying
            dir = os.path.dirname(out_name)
            if not os.path.isdir(dir):
                os.makedirs(dir)
            
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        
        num_tasks = len(files)

        for i, _ in enumerate(pool.imap_unordered(decompile_file, args)):
            print('\rProgress {0:%}'.format(i / num_tasks))
        
        pool.map(decompile_file, args)
        print("Done!")
    else:
        output_name = ""
        if len(sys.argv) == 3:
            output_name = sys.argv[2]
        else:
            output_name = os.path.basename(file_name)[:-2]
    
        decompile_file((file_name, output_name))
       
if __name__ == "__main__":
    main()
    