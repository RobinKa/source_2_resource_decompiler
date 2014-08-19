from resourcedecompiler import ResourceDecompiler

class Section:
    name = ""
    type = ""
    data = ""

class ParticleDecompiler(ResourceDecompiler):
    var_types = {
        "float32": "float",
        "bool": "bool",
        "int32": "int",
        "Vector": "float(3)",
        "Color": "uint(4)",
        "Vector4D": "float(4)",
        "QAngle": "float(3)",
        "fltx4": "float(4)"
    }

    def write_output(self, s):
        if self.write_to_section:
            self.current_section.data += s
        else:
            super(ParticleDecompiler, self).write_output(s)
        
    def write_sections(self):
        for section in self.sections:
            self.write_output_line(section.type + " " + section.name)
            self.write_output_line("{")
            self.write_output(section.data)
            self.write_output_line("}")

    def handle_variable(self, tokens):
        tokens[0] = self.var_types[tokens[0]]
        self.write_output_list(tokens)
        
    def handle_char_array(self, tokens):
        tokens[0] = "string"
        self.write_output_list(tokens)
        
    def handle_resource_string(self, tokens):
        self.write_output_line("string " + tokens[1] + " " + tokens[2] + " \"\"")
        
    def handle_external_ref(self, tokens):
        self.write_output("string " + tokens[1] + " = \"")

        if tokens[4] in self.external_refs:
            self.write_output(self.external_refs[tokens[4]])
        elif tokens[4] != "0000000000000000":
            print("Unknown reference " + tokens[4] + ", writing blank string")
            
        self.write_output_line("\"")
        
    def handle_struct(self, tokens):
        if len(tokens) == 4 and tokens[3] == "CParticleVisibilityInputs":
            self.write_output_line("CParticleVisibilityInputs " + tokens[1] + " = CParticleVisibilityInputs")
            self.visibility_inputs = True
        else:
            #Names are like m_Children[0] so split before the [
            a = tokens[1].split("[")
            name = a[0]
            type = ""

            #Get the number inside the brackets
            
            if len(a) > 1:
                self.struct_count = int(a[1].split("]")[0])
            else:
                self.struct_count = 0
            
            #Determine struct type
            if name == "m_Children":
                type = "ParticleChildrenInfo_t[] "
            else:
                type = "CParticleOperatorInstance*[] "

            #Write Type Name =
            self.write_output_line(type + " " + name + " =")
        
    def handle_pointer(self, tokens):
        section = Section()
        section.type = tokens[2]
        section.name = section.type + "_" + str(len(self.sections))
        
        #Write the reference to the section
        self.struct_count -= 1
        
        if self.struct_count > 0:
            self.write_output_line("&" + section.name + ",")
        else:
            self.write_output_line("&" + section.name)
        
        self.current_section = section
        self.write_to_section = True
        
    def handle_open_bracket(self, tokens):
        self.write_output_line("[")
        
    def handle_close_bracket(self, tokens):
        self.write_output_line("]")
        
    def handle_open_curly(self, tokens):
        if self.visibility_inputs or self.model_ref:
            self.write_output_line("{")
        else:
            #Ignores curlies when writing to sections
            if not self.write_to_section:
                self.write_output_line("{")
            
    def handle_close_curly(self, tokens):
        if self.visibility_inputs:
            self.write_output_line("}")
            self.visibility_inputs = False
        elif self.model_ref:
            self.write_output_line("}")
            self.model_ref = False
        else:
            if not self.write_to_section:
                #Write a comma after if its set
                if self.next_close_curly_comma:
                    self.write_output_line("},")
                    self.next_close_curly_comma = False
                else:
                    self.write_output_line("}")
            else:
                #Closed curly ends sections
                self.write_to_section = False
                self.sections.append(self.current_section)
                self.current_section = None
            
    def handle_particle_system_def(self, tokens):
        self.write_output_line(tokens[0] + " " + tokens[0] + "_" + str(self.particle_def_count))
        self.particle_def_count += 1
        
    def handle_particle_children_info(self, tokens):
        self.write_output_line(tokens[0])
        self.struct_count -= 1
        if self.struct_count > 0:
            self.next_close_curly_comma = True
            
    def handle_enum(self, tokens):
        enum_int = int(tokens[6].replace("}", ""))
        self.write_output_line("symbol " + tokens[1] + " = " + str(enum_int))
        
    def handle_model_reference(self, tokens):
        self.write_output_line(tokens[0]) #ModelReference_t
        self.model_ref = True
        self.struct_count -= 1
        if self.struct_count > 0:
            self.next_close_curly_comma = True
        
    def read_external_ref(self, tokens):
        self.external_refs[tokens[0]] = tokens[1]
        
    def start(self):
        self.sections = []
        self.external_refs = {}
        
        self.write_to_section = False
        self.current_section = None
        self.particle_def_count = 0
        self.visibility_inputs = False
        self.model_ref = True
        self.next_close_curly_comma = False
 
        start_found = False
        read_refs = False
        section_data_count = 0
        
        self.write_output_line("<!-- schema text {7e125a45-3d83-4043-b292-9e24f8ef27b4} generic {198980d8-3a93-4919-b4c6-dd1fb07a3a4b} -->\n")
        
        for line in self.data_lines:
            if not start_found:
                #Read external references if read_refs is set
                if read_refs:
                    tokens = line.split(" ")
                    
                    if(tokens[0] == "Id:" and tokens[1] == "Resource" and tokens[2] == "Name:"):
                        print("Resource reference table head")
                    elif len(tokens) != 2:
                        read_refs = False
                    else:
                        self.read_external_ref(line.split(" "))
            
                if line.startswith("--- Resource External Refs: ---"):
                    read_refs = True

                elif line.startswith("--- vpcf Resource Data"):
                    start_found = True
                continue
        
            tokens = line.split(" ")

            #Handle all the different stuff just by looking at the first word of each line
            if tokens[0] == "CParticleSystemDefinition":
                self.handle_particle_system_def(tokens)
            elif tokens[0] == "{":
                self.handle_open_curly(tokens)
            elif tokens[0] == "}":
                self.handle_close_curly(tokens)
            elif tokens[0] in self.var_types:
                self.handle_variable(tokens)
            elif tokens[0].startswith("char["):
                self.handle_char_array(tokens)
            elif tokens[0] == "CResourceString":
                self.handle_resource_string(tokens)
            elif tokens[0] == "Struct":
                self.handle_struct(tokens)
            elif tokens[0] == "(ptr)":
                self.handle_pointer(tokens)
            elif tokens[0] == "[":
                self.handle_open_bracket(tokens)
            elif tokens[0] == "]":
                self.handle_close_bracket(tokens)
            elif tokens[0] == "ExternalReference":
                self.handle_external_ref(tokens)
            elif tokens[0] == "ParticleChildrenInfo_t":
                self.handle_particle_children_info(tokens)
            elif tokens[0] == "Enum":
                self.handle_enum(tokens)
            elif tokens[0] == "ModelReference_t":
                self.handle_model_reference(tokens)
            else:
                print("WARNING: Unprocessed line: " + line)
                
        self.write_sections()
