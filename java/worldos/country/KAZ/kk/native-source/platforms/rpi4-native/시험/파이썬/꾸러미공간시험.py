import jkoros
import жинау
import sys

기존목록 = jkoros.read("/lib/.pip.json")
개수 = 0
try:
    while True:
        jkoros.write("/가득%d" % 개수, b"saved")
        개수 += 1
except OSError as Қате:
    assert Қате.args[0] == 28
assert 개수 >= 2
for индекс in range(개수 - 2, 개수):
    jkoros.remove("/가득%d" % индекс)
try:
    жинау.орнату_мән("jkoros-space==1.0", int(sys.argv[1]))
except OSError as Қате:
    assert Қате.args[0] == 28
else:
    raise AssertionError("мекенжай_аумақ 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for индекс in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % индекс) == 0
for индекс in range(개수 - 2):
    assert jkoros.read("/가득%d" % индекс) == b"saved"
    jkoros.remove("/가득%d" % индекс)
print("жинау мекенжай_аумақ 부족 қайтару_көпір тексеру")
