import jkoros
import Paket
import sys

bestehendListe = jkoros.read("/lib/.pip.json")
elementeintragAnzahl = 0
try:
    while True:
        jkoros.write("/가득%d" % elementeintragAnzahl, b"saved")
        elementeintragAnzahl += 1
except OSError as fehler:
    assert fehler.args[0] == 28
assert elementeintragAnzahl >= 2
for Nummer in range(elementeintragAnzahl - 2, elementeintragAnzahl):
    jkoros.remove("/가득%d" % Nummer)
try:
    Paket.wertEinrichten("jkoros-space==1.0", int(sys.argv[1]))
except OSError as fehler:
    assert fehler.args[0] == 28
else:
    raise AssertionError("adresseGebiet 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == bestehendListe
for Nummer in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % Nummer) == 0
for Nummer in range(elementeintragAnzahl - 2):
    assert jkoros.read("/가득%d" % Nummer) == b"saved"
    jkoros.remove("/가득%d" % Nummer)
print("Paket adresseGebiet 부족 zurückkehrenBrücke überprüfen")
