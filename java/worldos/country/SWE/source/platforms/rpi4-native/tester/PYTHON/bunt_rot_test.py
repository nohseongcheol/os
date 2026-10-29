import jkoros
import bunt
import sys

기존목록 = jkoros.read("/lib/.pip.json")
objekt_ANTAL = 0
try:
    while True:
        jkoros.write("/가득%d" % objekt_ANTAL, b"saved")
        objekt_ANTAL += 1
except OSError as fel:
    assert fel.args[0] == 28
assert objekt_ANTAL >= 2
for INDEX in range(objekt_ANTAL - 2, objekt_ANTAL):
    jkoros.remove("/가득%d" % INDEX)
try:
    bunt.installera_värde("jkoros-space==1.0", int(sys.argv[1]))
except OSError as fel:
    assert fel.args[0] == 28
else:
    raise AssertionError("ADRESS_område 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for INDEX in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % INDEX) == 0
for INDEX in range(objekt_ANTAL - 2):
    assert jkoros.read("/가득%d" % INDEX) == b"saved"
    jkoros.remove("/가득%d" % INDEX)
print("bunt ADRESS_område 부족 Retur_brygga verifiera")
