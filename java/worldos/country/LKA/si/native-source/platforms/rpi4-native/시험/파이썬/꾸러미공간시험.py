import jkoros
import පොදිය
import sys

기존목록 = jkoros.read("/lib/.pip.json")
개수 = 0
try:
    while True:
        jkoros.write("/가득%d" % 개수, b"saved")
        개수 += 1
except OSError as දෝෂය:
    assert දෝෂය.args[0] == 28
assert 개수 >= 2
for සූචිය in range(개수 - 2, 개수):
    jkoros.remove("/가득%d" % සූචිය)
try:
    පොදිය.ස්ථාපනය_කරන්න_අගය("jkoros-space==1.0", int(sys.argv[1]))
except OSError as දෝෂය:
    assert දෝෂය.args[0] == 28
else:
    raise AssertionError("공간 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for සූචිය in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % සූචිය) == 0
for සූචිය in range(개수 - 2):
    assert jkoros.read("/가득%d" % සූචිය) == b"saved"
    jkoros.remove("/가득%d" % සූචිය)
print("පොදිය 공간 부족 되돌림 තහවුරු_කරන්න")
