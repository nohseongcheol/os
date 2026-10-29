import jkoros
import àkópọ̀
import sys

기존목록 = jkoros.read("/lib/.pip.json")
개수 = 0
try:
    while True:
        jkoros.write("/가득%d" % 개수, b"saved")
        개수 += 1
except OSError as àṣìṣe:
    assert àṣìṣe.args[0] == 28
assert 개수 >= 2
for wá_atọ̀ka_àkóónú in range(개수 - 2, 개수):
    jkoros.remove("/가득%d" % wá_atọ̀ka_àkóónú)
try:
    àkópọ̀.ṣàgbékalẹ̀_iye("jkoros-space==1.0", int(sys.argv[1]))
except OSError as àṣìṣe:
    assert àṣìṣe.args[0] == 28
else:
    raise AssertionError("공간 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for wá_atọ̀ka_àkóónú in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % wá_atọ̀ka_àkóónú) == 0
for wá_atọ̀ka_àkóónú in range(개수 - 2):
    assert jkoros.read("/가득%d" % wá_atọ̀ka_àkóónú) == b"saved"
    jkoros.remove("/가득%d" % wá_atọ̀ka_àkóónú)
print("àkópọ̀ 공간 부족 되돌림 ridájú")
