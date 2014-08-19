import subprocess

RESOURCE_INFO_PATH = "D:/Program Files (x86)/Steam/SteamApps/common/dota 2 beta/dota_ugc/game/bin/win64/resourceinfo.exe"

class ResourceDecompiler:
    def decompile(self, file_path, output_path):
        cmd = [RESOURCE_INFO_PATH, "-i", file_path, "-b", "DATA"]
        
        p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        out, err = p.communicate()
        
        self.data_str = out.decode("utf-8")
        
        self.data_lines = [" ".join(line.replace("\t", " ").split()) for line in self.data_str.splitlines()]
        self.output_data = ""
        
        self.start()
        
        #Write file output
        f = open(output_path, "w")
        f.write(self.output_data)
        f.close()
        
    def write_output(self, s):
        self.output_data += s
        
    def write_output_line(self, line):
        self.write_output(line + "\n")
        
    def write_output_list(self, list):
        self.write_output_line(" ".join(list))
        
    #Override this in subclasses
    def start(self):
        print("Started parsing")
        
