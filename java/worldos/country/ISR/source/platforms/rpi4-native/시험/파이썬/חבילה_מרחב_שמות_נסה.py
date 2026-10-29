import jkoros
import חבילה
import sys

기존목록 = jkoros.read("/lib/.pip.json")
개수 = 0
try:
    while True:
        jkoros.write("/가득%d" % 개수, b"saved")
        개수 += 1
except OSError as שגיאה:
    assert שגיאה.args[0] == 28
assert 개수 >= 2
for מדד in range(개수 - 2, 개수):
    jkoros.remove("/가득%d" % מדד)
try:
    חבילה.התקן_ערך("jkoros-space==1.0", int(sys.argv[1]))
except OSError as שגיאה:
    assert שגיאה.args[0] == 28
else:
    raise AssertionError("למען_אזור 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for מדד in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % מדד) == 0
for מדד in range(개수 - 2):
    assert jkoros.read("/가득%d" % מדד) == b"saved"
    jkoros.remove("/가득%d" % מדד)
print("חבילה למען_אזור 부족 החזר_גשר ודא_אמת")
