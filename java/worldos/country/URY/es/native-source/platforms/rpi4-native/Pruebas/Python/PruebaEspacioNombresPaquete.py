import jkoros
import Paquete
import sys

listaExistente = jkoros.read("/lib/.pip.json")
númeroElementosElementoLista = 0
try:
    while True:
        jkoros.write("/가득%d" % númeroElementosElementoLista, b"saved")
        númeroElementosElementoLista += 1
except OSError as error:
    assert error.args[0] == 28
assert númeroElementosElementoLista >= 2
for número in range(númeroElementosElementoLista - 2, númeroElementosElementoLista):
    jkoros.remove("/가득%d" % número)
try:
    Paquete.instalarValor("jkoros-space==1.0", int(sys.argv[1]))
except OSError as error:
    assert error.args[0] == 28
else:
    raise AssertionError("regiónDirección 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == listaExistente
for número in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % número) == 0
for número in range(númeroElementosElementoLista - 2):
    assert jkoros.read("/가득%d" % número) == b"saved"
    jkoros.remove("/가득%d" % número)
print("Paquete regiónDirección 부족 puenteRetornar verificar")
