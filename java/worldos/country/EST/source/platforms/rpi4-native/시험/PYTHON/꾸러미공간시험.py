import jkoros
import kogum
import sys

기존목록 = jkoros.read("/lib/.pip.json")
kaup_COUNT = 0
try:
    while True:
        jkoros.write("/가득%d" % kaup_COUNT, b"saved")
        kaup_COUNT += 1
except OSError as VIGA:
    assert VIGA.args[0] == 28
assert kaup_COUNT >= 2
for INDEX in range(kaup_COUNT - 2, kaup_COUNT):
    jkoros.remove("/가득%d" % INDEX)
try:
    kogum.installima_VALUE("jkoros-space==1.0", int(sys.argv[1]))
except OSError as VIGA:
    assert VIGA.args[0] == 28
else:
    raise AssertionError("ADDRESS_regioon 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for INDEX in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % INDEX) == 0
for INDEX in range(kaup_COUNT - 2):
    assert jkoros.read("/가득%d" % INDEX) == b"saved"
    jkoros.remove("/가득%d" % INDEX)
print("kogum ADDRESS_regioon 부족 tagasi_saatma_sild kinnitama")
