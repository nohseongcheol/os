import jkoros
import bundt
import sys

기존목록 = jkoros.read("/lib/.pip.json")
vare_TÆL = 0
try:
    while True:
        jkoros.write("/가득%d" % vare_TÆL, b"saved")
        vare_TÆL += 1
except OSError as fejl:
    assert fejl.args[0] == 28
assert vare_TÆL >= 2
for INDEKS in range(vare_TÆL - 2, vare_TÆL):
    jkoros.remove("/가득%d" % INDEKS)
try:
    bundt.installér_VÆRDI("jkoros-space==1.0", int(sys.argv[1]))
except OSError as fejl:
    assert fejl.args[0] == 28
else:
    raise AssertionError("mail_område 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for INDEKS in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % INDEKS) == 0
for INDEKS in range(vare_TÆL - 2):
    assert jkoros.read("/가득%d" % INDEKS) == b"saved"
    jkoros.remove("/가득%d" % INDEKS)
print("bundt mail_område 부족 returnere_bro bekræfte")
