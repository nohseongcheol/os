import jkoros
import grupo
import sys

기존목록 = jkoros.read("/lib/.pip.json")
item_CONT_NÚM = 0
try:
    while True:
        jkoros.write("/가득%d" % item_CONT_NÚM, b"saved")
        item_CONT_NÚM += 1
except OSError as erro:
    assert erro.args[0] == 28
assert item_CONT_NÚM >= 2
for ÍNDICE in range(item_CONT_NÚM - 2, item_CONT_NÚM):
    jkoros.remove("/가득%d" % ÍNDICE)
try:
    grupo.instalar_VALOR("jkoros-space==1.0", int(sys.argv[1]))
except OSError as erro:
    assert erro.args[0] == 28
else:
    raise AssertionError("email_região 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for ÍNDICE in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % ÍNDICE) == 0
for ÍNDICE in range(item_CONT_NÚM - 2):
    assert jkoros.read("/가득%d" % ÍNDICE) == b"saved"
    jkoros.remove("/가득%d" % ÍNDICE)
print("grupo email_região 부족 devolver_ponte verificar")
