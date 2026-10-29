import jkoros
import zväzok
import sys

기존목록 = jkoros.read("/lib/.pip.json")
položka_COUNT = 0
try:
    while True:
        jkoros.write("/가득%d" % položka_COUNT, b"saved")
        položka_COUNT += 1
except OSError as chyba:
    assert chyba.args[0] == 28
assert položka_COUNT >= 2
for INDEX in range(položka_COUNT - 2, položka_COUNT):
    jkoros.remove("/가득%d" % INDEX)
try:
    zväzok.inštalovať_VALUE("jkoros-space==1.0", int(sys.argv[1]))
except OSError as chyba:
    assert chyba.args[0] == 28
else:
    raise AssertionError("adresa_oblasť 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for INDEX in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % INDEX) == 0
for INDEX in range(položka_COUNT - 2):
    assert jkoros.read("/가득%d" % INDEX) == b"saved"
    jkoros.remove("/가득%d" % INDEX)
print("zväzok adresa_oblasť 부족 vrátiť_most overiť")
