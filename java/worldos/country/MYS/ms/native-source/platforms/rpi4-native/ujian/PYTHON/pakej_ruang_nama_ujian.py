import jkoros
import pakej
import sys

기존목록 = jkoros.read("/lib/.pip.json")
item_COUNT = 0
try:
    while True:
        jkoros.write("/가득%d" % item_COUNT, b"saved")
        item_COUNT += 1
except OSError as RALAT:
    assert RALAT.args[0] == 28
assert item_COUNT >= 2
for INDEX in range(item_COUNT - 2, item_COUNT):
    jkoros.remove("/가득%d" % INDEX)
try:
    pakej.pasang_VALUE("jkoros-space==1.0", int(sys.argv[1]))
except OSError as RALAT:
    assert RALAT.args[0] == 28
else:
    raise AssertionError("e_mel_rantau 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for INDEX in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % INDEX) == 0
for INDEX in range(item_COUNT - 2):
    assert jkoros.read("/가득%d" % INDEX) == b"saved"
    jkoros.remove("/가득%d" % INDEX)
print("pakej e_mel_rantau 부족 kembalikan_penghubung tentu_sahkan")
