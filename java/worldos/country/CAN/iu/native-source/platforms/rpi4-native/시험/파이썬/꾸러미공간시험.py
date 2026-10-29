import jkoros
import 꾸러미
import sys

기존목록 = jkoros.read("/lib/.pip.json")
개수 = 0
try:
    while True:
        jkoros.write("/가득%d" % 개수, b"saved")
        개수 += 1
except OSError as tammarniq:
    assert tammarniq.args[0] == 28
assert 개수 >= 2
for nalunaiqsimavik in range(개수 - 2, 개수):
    jkoros.remove("/가득%d" % nalunaiqsimavik)
try:
    꾸러미.ilili_atuutilik("jkoros-space==1.0", int(sys.argv[1]))
except OSError as tammarniq:
    assert tammarniq.args[0] == 28
else:
    raise AssertionError("공간 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for nalunaiqsimavik in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % nalunaiqsimavik) == 0
for nalunaiqsimavik in range(개수 - 2):
    assert jkoros.read("/가득%d" % nalunaiqsimavik) == b"saved"
    jkoros.remove("/가득%d" % nalunaiqsimavik)
print("꾸러미 공간 부족 되돌림 nalunairli_1aacb54c")
