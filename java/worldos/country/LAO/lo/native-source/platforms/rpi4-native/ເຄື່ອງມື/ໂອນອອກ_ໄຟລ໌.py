#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ=argparse.ArgumentParser(description=__doc__);ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.add_argument('file',type=Path);ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.add_argument('--name',help='guest file name (e.g. package.Class.class)');ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ=ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.parse_args()
ຂໍ້ມູນ=ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.file.read_bytes();ຊື່=ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.name or ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.file.name
if len(ຂໍ້ມູນ)>16384 or not 1<=len(ຊື່.encode('utf-8'))<=63 or any(ord(ຈຸດ_ລະ_ຫັດ)<32 for ຈຸດ_ລະ_ຫັດ in ຊື່):ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(ຊື່))
for 순번 in range(0,len(ຂໍ້ມູນ),64):print(ຂໍ້ມູນ[순번:순번+64].hex())
print('.')
