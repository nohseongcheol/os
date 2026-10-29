import jkoros
import набір
import sys

기존목록 = jkoros.read("/lib/.pip.json")
개수 = 0
try:
    while True:
        jkoros.write("/가득%d" % 개수, b"saved")
        개수 += 1
except OSError as ПОМИЛКА:
    assert ПОМИЛКА.args[0] == 28
assert 개수 >= 2
for індекс in range(개수 - 2, 개수):
    jkoros.remove("/가득%d" % індекс)
try:
    набір.інсталювати_значення("jkoros-space==1.0", int(sys.argv[1]))
except OSError as ПОМИЛКА:
    assert ПОМИЛКА.args[0] == 28
else:
    raise AssertionError("адреса_область 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for індекс in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % індекс) == 0
for індекс in range(개수 - 2):
    assert jkoros.read("/가득%d" % індекс) == b"saved"
    jkoros.remove("/가득%d" % індекс)
print("набір адреса_область 부족 повернути_міст перевіряти")
