import jkoros
import 꾸러미
import sys

기존목록 = jkoros.read("/lib/.pip.json")
개수 = 0
try:
    while True:
        jkoros.write("/가득%d" % 개수, b"saved")
        개수 += 1
except OSError as 오류:
    assert 오류.args[0] == 28
assert 개수 >= 2
for 번호 in range(개수 - 2, 개수):
    jkoros.remove("/가득%d" % 번호)
try:
    꾸러미.설치("jkoros-space==1.0", int(sys.argv[1]))
except OSError as 오류:
    assert 오류.args[0] == 28
else:
    raise AssertionError("공간 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for 번호 in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % 번호) == 0
for 번호 in range(개수 - 2):
    assert jkoros.read("/가득%d" % 번호) == b"saved"
    jkoros.remove("/가득%d" % 번호)
print("꾸러미 공간 부족 되돌림 확인")
