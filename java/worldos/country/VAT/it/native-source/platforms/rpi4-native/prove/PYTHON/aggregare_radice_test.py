import jkoros
import aggregare
import sys

기존목록 = jkoros.read("/lib/.pip.json")
articolo_CONTA_NUMERI = 0
try:
    while True:
        jkoros.write("/가득%d" % articolo_CONTA_NUMERI, b"saved")
        articolo_CONTA_NUMERI += 1
except OSError as errore:
    assert errore.args[0] == 28
assert articolo_CONTA_NUMERI >= 2
for INDICE in range(articolo_CONTA_NUMERI - 2, articolo_CONTA_NUMERI):
    jkoros.remove("/가득%d" % INDICE)
try:
    aggregare.installare_VALORE("jkoros-space==1.0", int(sys.argv[1]))
except OSError as errore:
    assert errore.args[0] == 28
else:
    raise AssertionError("e_mail_area 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for INDICE in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % INDICE) == 0
for INDICE in range(articolo_CONTA_NUMERI - 2):
    assert jkoros.read("/가득%d" % INDICE) == b"saved"
    jkoros.remove("/가득%d" % INDICE)
print("aggregare e_mail_area 부족 Reso_bridge verificare")
