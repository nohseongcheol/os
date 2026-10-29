import jkoros
import multzo
import sys

기존목록 = jkoros.read("/lib/.pip.json")
elementu_ZENBATU = 0
try:
    while True:
        jkoros.write("/가득%d" % elementu_ZENBATU, b"saved")
        elementu_ZENBATU += 1
except OSError as errorea:
    assert errorea.args[0] == 28
assert elementu_ZENBATU >= 2
for INDIZE in range(elementu_ZENBATU - 2, elementu_ZENBATU):
    jkoros.remove("/가득%d" % INDIZE)
try:
    multzo.instalatu_balio("jkoros-space==1.0", int(sys.argv[1]))
except OSError as errorea:
    assert errorea.args[0] == 28
else:
    raise AssertionError("공간 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for INDIZE in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % INDIZE) == 0
for INDIZE in range(elementu_ZENBATU - 2):
    assert jkoros.read("/가득%d" % INDIZE) == b"saved"
    jkoros.remove("/가득%d" % INDIZE)
print("multzo 공간 부족 itzuli_zubi egiaztatu")
