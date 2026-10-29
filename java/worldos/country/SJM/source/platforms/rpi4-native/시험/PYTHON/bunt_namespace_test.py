import jkoros
import bunt
import sys

기존목록 = jkoros.read("/lib/.pip.json")
vare_ANTALL = 0
try:
    while True:
        jkoros.write("/가득%d" % vare_ANTALL, b"saved")
        vare_ANTALL += 1
except OSError as feil:
    assert feil.args[0] == 28
assert vare_ANTALL >= 2
for INDEKS in range(vare_ANTALL - 2, vare_ANTALL):
    jkoros.remove("/가득%d" % INDEKS)
try:
    bunt.installer_VERDI("jkoros-space==1.0", int(sys.argv[1]))
except OSError as feil:
    assert feil.args[0] == 28
else:
    raise AssertionError("e_post_område 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for INDEKS in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % INDEKS) == 0
for INDEKS in range(vare_ANTALL - 2):
    assert jkoros.read("/가득%d" % INDEKS) == b"saved"
    jkoros.remove("/가득%d" % INDEKS)
print("bunt e_post_område 부족 return_bro bekrefte")
