import jkoros
import sada
import sys

기존목록 = jkoros.read("/lib/.pip.json")
zboží_POČET = 0
try:
    while True:
        jkoros.write("/가득%d" % zboží_POČET, b"saved")
        zboží_POČET += 1
except OSError as chyba:
    assert chyba.args[0] == 28
assert zboží_POČET >= 2
for INDEX in range(zboží_POČET - 2, zboží_POČET):
    jkoros.remove("/가득%d" % INDEX)
try:
    sada.instalovat_HODNOTA("jkoros-space==1.0", int(sys.argv[1]))
except OSError as chyba:
    assert chyba.args[0] == 28
else:
    raise AssertionError("ODKAZ_oblast 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for INDEX in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % INDEX) == 0
for INDEX in range(zboží_POČET - 2):
    assert jkoros.read("/가득%d" % INDEX) == b"saved"
    jkoros.remove("/가득%d" % INDEX)
print("sada ODKAZ_oblast 부족 Vratka_most ověřit")
