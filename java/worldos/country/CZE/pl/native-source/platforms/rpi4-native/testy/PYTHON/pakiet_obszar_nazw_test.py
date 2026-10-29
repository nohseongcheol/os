import jkoros
import pakiet
import sys

기존목록 = jkoros.read("/lib/.pip.json")
towar_ILE_LICZB = 0
try:
    while True:
        jkoros.write("/가득%d" % towar_ILE_LICZB, b"saved")
        towar_ILE_LICZB += 1
except OSError as błąd:
    assert błąd.args[0] == 28
assert towar_ILE_LICZB >= 2
for INDEKS in range(towar_ILE_LICZB - 2, towar_ILE_LICZB):
    jkoros.remove("/가득%d" % INDEKS)
try:
    pakiet.instalować_WARTOŚĆ("jkoros-space==1.0", int(sys.argv[1]))
except OSError as błąd:
    assert błąd.args[0] == 28
else:
    raise AssertionError("ADRES_region 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for INDEKS in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % INDEKS) == 0
for INDEKS in range(towar_ILE_LICZB - 2):
    assert jkoros.read("/가득%d" % INDEKS) == b"saved"
    jkoros.remove("/가득%d" % INDEKS)
print("pakiet ADRES_region 부족 Zwrot_mostek 확인")
