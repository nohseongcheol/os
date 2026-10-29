import jkoros
import रास
import sys

기존목록 = jkoros.read("/lib/.pip.json")
आयटम_COUNT = 0
try:
    while True:
        jkoros.write("/가득%d" % आयटम_COUNT, b"saved")
        आयटम_COUNT += 1
except OSError as चूक:
    assert चूक.args[0] == 28
assert आयटम_COUNT >= 2
for INDEX in range(आयटम_COUNT - 2, आयटम_COUNT):
    jkoros.remove("/가득%d" % INDEX)
try:
    रास.स्थापणूक_मोल("jkoros-space==1.0", int(sys.argv[1]))
except OSError as चूक:
    assert चूक.args[0] == 28
else:
    raise AssertionError("공간 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for INDEX in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % INDEX) == 0
for INDEX in range(आयटम_COUNT - 2):
    assert jkoros.read("/가득%d" % INDEX) == b"saved"
    jkoros.remove("/가득%d" % INDEX)
print("रास 공간 부족 return_ब्रिज पुनर्तपासणी_करची")
