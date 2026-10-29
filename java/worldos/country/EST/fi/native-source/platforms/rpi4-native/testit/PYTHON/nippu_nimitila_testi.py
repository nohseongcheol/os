import jkoros
import nippu
import sys

기존목록 = jkoros.read("/lib/.pip.json")
kohde_LASKE = 0
try:
    while True:
        jkoros.write("/가득%d" % kohde_LASKE, b"saved")
        kohde_LASKE += 1
except OSError as VIRHE:
    assert VIRHE.args[0] == 28
assert kohde_LASKE >= 2
for INDEKSI in range(kohde_LASKE - 2, kohde_LASKE):
    jkoros.remove("/가득%d" % INDEKSI)
try:
    nippu.asentaa_ARVO("jkoros-space==1.0", int(sys.argv[1]))
except OSError as VIRHE:
    assert VIRHE.args[0] == 28
else:
    raise AssertionError("OSOITE_alue 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for INDEKSI in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % INDEKSI) == 0
for INDEKSI in range(kohde_LASKE - 2):
    assert jkoros.read("/가득%d" % INDEKSI) == b"saved"
    jkoros.remove("/가득%d" % INDEKSI)
print("nippu OSOITE_alue 부족 palauttaa_silta tarkistaa")
