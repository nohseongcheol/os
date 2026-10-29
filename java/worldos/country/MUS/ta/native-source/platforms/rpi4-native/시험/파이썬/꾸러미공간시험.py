import jkoros
import மூட்டை
import sys

기존목록 = jkoros.read("/lib/.pip.json")
개수 = 0
try:
    while True:
        jkoros.write("/가득%d" % 개수, b"saved")
        개수 += 1
except OSError as பிழை:
    assert பிழை.args[0] == 28
assert 개수 >= 2
for அடைவு in range(개수 - 2, 개수):
    jkoros.remove("/가득%d" % அடைவு)
try:
    மூட்டை.நிறுவு_மதிப்பு("jkoros-space==1.0", int(sys.argv[1]))
except OSError as பிழை:
    assert பிழை.args[0] == 28
else:
    raise AssertionError("공간 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for அடைவு in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % அடைவு) == 0
for அடைவு in range(개수 - 2):
    assert jkoros.read("/가득%d" % அடைவு) == b"saved"
    jkoros.remove("/가득%d" % அடைவு)
print("மூட்டை 공간 부족 되돌림 சரிபார்")
