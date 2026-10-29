import jkoros
import bwndel
import sys

기존목록 = jkoros.read("/lib/.pip.json")
eitem_COUNT = 0
try:
    while True:
        jkoros.write("/가득%d" % eitem_COUNT, b"saved")
        eitem_COUNT += 1
except OSError as Gwall:
    assert Gwall.args[0] == 28
assert eitem_COUNT >= 2
for INDEX in range(eitem_COUNT - 2, eitem_COUNT):
    jkoros.remove("/가득%d" % INDEX)
try:
    bwndel.gosod_VALUE("jkoros-space==1.0", int(sys.argv[1]))
except OSError as Gwall:
    assert Gwall.args[0] == 28
else:
    raise AssertionError("공간 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for INDEX in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % INDEX) == 0
for INDEX in range(eitem_COUNT - 2):
    assert jkoros.read("/가득%d" % INDEX) == b"saved"
    jkoros.remove("/가득%d" % INDEX)
print("bwndel 공간 부족 return_pont dilysu")
