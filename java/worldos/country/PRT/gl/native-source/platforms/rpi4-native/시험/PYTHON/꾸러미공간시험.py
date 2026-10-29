import jkoros
import paquete
import sys

기존목록 = jkoros.read("/lib/.pip.json")
elemento_CONTAR = 0
try:
    while True:
        jkoros.write("/가득%d" % elemento_CONTAR, b"saved")
        elemento_CONTAR += 1
except OSError as ERRO:
    assert ERRO.args[0] == 28
assert elemento_CONTAR >= 2
for ÍNDICE in range(elemento_CONTAR - 2, elemento_CONTAR):
    jkoros.remove("/가득%d" % ÍNDICE)
try:
    paquete.instalar_VALOR("jkoros-space==1.0", int(sys.argv[1]))
except OSError as ERRO:
    assert ERRO.args[0] == 28
else:
    raise AssertionError("공간 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for ÍNDICE in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % ÍNDICE) == 0
for ÍNDICE in range(elemento_CONTAR - 2):
    assert jkoros.read("/가득%d" % ÍNDICE) == b"saved"
    jkoros.remove("/가득%d" % ÍNDICE)
print("paquete 공간 부족 devolver_ponte verificar")
