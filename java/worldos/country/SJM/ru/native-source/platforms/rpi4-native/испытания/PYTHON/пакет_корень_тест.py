import jkoros
import пакет
import sys

기존목록 = jkoros.read("/lib/.pip.json")
товар_СЧЁТ = 0
try:
    while True:
        jkoros.write("/가득%d" % товар_СЧЁТ, b"saved")
        товар_СЧЁТ += 1
except OSError as ошибка:
    assert ошибка.args[0] == 28
assert товар_СЧЁТ >= 2
for ИНДЕКС in range(товар_СЧЁТ - 2, товар_СЧЁТ):
    jkoros.remove("/가득%d" % ИНДЕКС)
try:
    пакет.установить_ЗНАЧЕН("jkoros-space==1.0", int(sys.argv[1]))
except OSError as ошибка:
    assert ошибка.args[0] == 28
else:
    raise AssertionError("АДРЕС_регион 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for ИНДЕКС in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % ИНДЕКС) == 0
for ИНДЕКС in range(товар_СЧЁТ - 2):
    assert jkoros.read("/가득%d" % ИНДЕКС) == b"saved"
    jkoros.remove("/가득%d" % ИНДЕКС)
print("пакет АДРЕС_регион 부족 Возврат_мост проверять")
