import jkoros
import paketas
import sys

기존목록 = jkoros.read("/lib/.pip.json")
prekė_COUNT = 0
try:
    while True:
        jkoros.write("/가득%d" % prekė_COUNT, b"saved")
        prekė_COUNT += 1
except OSError as KLAIDA:
    assert KLAIDA.args[0] == 28
assert prekė_COUNT >= 2
for INDEX in range(prekė_COUNT - 2, prekė_COUNT):
    jkoros.remove("/가득%d" % INDEX)
try:
    paketas.diegti_VALUE("jkoros-space==1.0", int(sys.argv[1]))
except OSError as KLAIDA:
    assert KLAIDA.args[0] == 28
else:
    raise AssertionError("ADDRESS_sritis 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for INDEX in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % INDEX) == 0
for INDEX in range(prekė_COUNT - 2):
    assert jkoros.read("/가득%d" % INDEX) == b"saved"
    jkoros.remove("/가득%d" % INDEX)
print("paketas ADDRESS_sritis 부족 grąžinti_tiltas patvirtinti")
