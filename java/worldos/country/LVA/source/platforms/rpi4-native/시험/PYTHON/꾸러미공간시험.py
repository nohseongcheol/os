import jkoros
import saistīt
import sys

기존목록 = jkoros.read("/lib/.pip.json")
krājums_COUNT = 0
try:
    while True:
        jkoros.write("/가득%d" % krājums_COUNT, b"saved")
        krājums_COUNT += 1
except OSError as Kļūda:
    assert Kļūda.args[0] == 28
assert krājums_COUNT >= 2
for INDEX in range(krājums_COUNT - 2, krājums_COUNT):
    jkoros.remove("/가득%d" % INDEX)
try:
    saistīt.instalēt_VALUE("jkoros-space==1.0", int(sys.argv[1]))
except OSError as Kļūda:
    assert Kļūda.args[0] == 28
else:
    raise AssertionError("adrese_reģions 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for INDEX in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % INDEX) == 0
for INDEX in range(krājums_COUNT - 2):
    assert jkoros.read("/가득%d" % INDEX) == b"saved"
    jkoros.remove("/가득%d" % INDEX)
print("saistīt adrese_reģions 부족 atdot_tilts verificēt")
