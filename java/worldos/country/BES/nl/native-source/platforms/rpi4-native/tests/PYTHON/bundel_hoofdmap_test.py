import jkoros
import bundel
import sys

기존목록 = jkoros.read("/lib/.pip.json")
item_AANTAL = 0
try:
    while True:
        jkoros.write("/가득%d" % item_AANTAL, b"saved")
        item_AANTAL += 1
except OSError as fout:
    assert fout.args[0] == 28
assert item_AANTAL >= 2
for INDEX in range(item_AANTAL - 2, item_AANTAL):
    jkoros.remove("/가득%d" % INDEX)
try:
    bundel.installeren_WAARDE("jkoros-space==1.0", int(sys.argv[1]))
except OSError as fout:
    assert fout.args[0] == 28
else:
    raise AssertionError("ADRES_regio 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for INDEX in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % INDEX) == 0
for INDEX in range(item_AANTAL - 2):
    assert jkoros.read("/가득%d" % INDEX) == b"saved"
    jkoros.remove("/가득%d" % INDEX)
print("bundel ADRES_regio 부족 Retour_brug bevestigen")
