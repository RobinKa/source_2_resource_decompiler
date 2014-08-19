Created by Toraxxx
==============

**Currently only supports decompiling .vpcf_c**

Requirements
--------------
- Windows
- Python 3 (https://www.python.org/download)
- Dota 2 Workshop Tools Alpha
- GCFScape or some other vpk extractor to extract what you want to decompile

How to use:
--------------
- Edit resourcedecompiler.py and set RESOURCE_INFO_PATH to the path of your resource info
- Extract the .vpcf_c that you want into the same corresponding path in dota_imported
  For example if a particle is in /particles/units/heroes/hero_axe/axe_culling_blade_kill.vpcf_c
  it will go into dota 2 beta/dota_ugc/game/dota_imported/particles/units/heroes/hero_axe/axe_culling_blade_kill.vpcf_c
- Now use the decompiler to decompile it by either drag-dropping the vpcf_c on resdec.py or using the console command

    python resdec.py inputfilepath optional outputfilepath
    
  Example: python resdec.py "D:\Program Files (x86)\Steam\SteamApps\common\dota 2 beta\dota_ugc\game\dota_imported\particles\units\heroes\hero_abaddon\abaddon_aphotic_shield_hit.vpcf_c"
  
  if you dont specify an output file path it will put it into your current work directory with the input file name + _decompiled.txt
- Now you can rename the decompiled file to somename.vpcf and put it into the content folder of your addon \o/

Useful:
--------------
- You can use python resdec.py Path/To/Directory/* to decompile all files that end with _c in that directory
- If you save the decompiled file with the editor it will indent it correctly


**You can contact me for any reasons at toraxxx@warlockbrawl.com**
