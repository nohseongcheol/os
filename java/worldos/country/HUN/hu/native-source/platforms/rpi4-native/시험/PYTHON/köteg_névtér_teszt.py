import jkoros
import köteg
import sys

기존목록 = jkoros.read("/lib/.pip.json")
cikk_DARAB = 0
try:
    while True:
        jkoros.write("/가득%d" % cikk_DARAB, b"saved")
        cikk_DARAB += 1
except OSError as HIBA:
    assert HIBA.args[0] == 28
assert cikk_DARAB >= 2
for INDEX in range(cikk_DARAB - 2, cikk_DARAB):
    jkoros.remove("/가득%d" % INDEX)
try:
    köteg.telepít_ÉRTÉK("jkoros-space==1.0", int(sys.argv[1]))
except OSError as HIBA:
    assert HIBA.args[0] == 28
else:
    raise AssertionError("CÍM_régió 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for INDEX in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % INDEX) == 0
for INDEX in range(cikk_DARAB - 2):
    assert jkoros.read("/가득%d" % INDEX) == b"saved"
    jkoros.remove("/가득%d" % INDEX)
print("köteg CÍM_régió 부족 visszaküld_híd igazol")
