import jkoros
import បាច់
import sys

기존목록 = jkoros.read("/lib/.pip.json")
개수 = 0
try:
    while True:
        jkoros.write("/가득%d" % 개수, b"saved")
        개수 += 1
except OSError as កំហុស:
    assert កំហុស.args[0] == 28
assert 개수 >= 2
for សន្ទស្សន៏ in range(개수 - 2, 개수):
    jkoros.remove("/가득%d" % សន្ទស្សន៏)
try:
    បាច់.ដំឡើង_តំលៃ("jkoros-space==1.0", int(sys.argv[1]))
except OSError as កំហុស:
    assert កំហុស.args[0] == 28
else:
    raise AssertionError("공간 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for សន្ទស្សន៏ in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % សន្ទស្សន៏) == 0
for សន្ទស្សន៏ in range(개수 - 2):
    assert jkoros.read("/가득%d" % សន្ទស្សន៏) == b"saved"
    jkoros.remove("/가득%d" % សន្ទស្សន៏)
print("បាច់ 공간 부족 되돌림 ផ្ទៀងផ្ទាត់")
