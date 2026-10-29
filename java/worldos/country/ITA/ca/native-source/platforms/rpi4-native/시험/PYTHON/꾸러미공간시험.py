import jkoros
import paquet
import sys

기존목록 = jkoros.read("/lib/.pip.json")
element_COMPT = 0
try:
    while True:
        jkoros.write("/가득%d" % element_COMPT, b"saved")
        element_COMPT += 1
except OSError as s_ha_produït_un_error:
    assert s_ha_produït_un_error.args[0] == 28
assert element_COMPT >= 2
for INDEX in range(element_COMPT - 2, element_COMPT):
    jkoros.remove("/가득%d" % INDEX)
try:
    paquet.instal_lar_VALOR("jkoros-space==1.0", int(sys.argv[1]))
except OSError as s_ha_produït_un_error:
    assert s_ha_produït_un_error.args[0] == 28
else:
    raise AssertionError("공간 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for INDEX in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % INDEX) == 0
for INDEX in range(element_COMPT - 2):
    assert jkoros.read("/가득%d" % INDEX) == b"saved"
    jkoros.remove("/가득%d" % INDEX)
print("paquet 공간 부족 tornar_les_tasques_pont verificar")
