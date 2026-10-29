import jkoros
import пакет
import sys

기존목록 = jkoros.read("/lib/.pip.json")
ставка_COUNT = 0
try:
    while True:
        jkoros.write("/가득%d" % ставка_COUNT, b"saved")
        ставка_COUNT += 1
except OSError as ГРЕШКА:
    assert ГРЕШКА.args[0] == 28
assert ставка_COUNT >= 2
for INDEX in range(ставка_COUNT - 2, ставка_COUNT):
    jkoros.remove("/가득%d" % INDEX)
try:
    пакет.инсталирај_VALUE("jkoros-space==1.0", int(sys.argv[1]))
except OSError as ГРЕШКА:
    assert ГРЕШКА.args[0] == 28
else:
    raise AssertionError("공간 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for INDEX in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % INDEX) == 0
for INDEX in range(ставка_COUNT - 2):
    assert jkoros.read("/가득%d" % INDEX) == b"saved"
    jkoros.remove("/가득%d" % INDEX)
print("пакет 공간 부족 되돌림 провери")
