import jkoros
import takku_xéewël
import sys

기존목록 = jkoros.read("/lib/.pip.json")
개수 = 0
try:
    while True:
        jkoros.write("/가득%d" % 개수, b"saved")
        개수 += 1
except OSError as njumte:
    assert njumte.args[0] == 28
assert 개수 >= 2
for àlluwa_tur in range(개수 - 2, 개수):
    jkoros.remove("/가득%d" % àlluwa_tur)
try:
    takku_xéewël.samp_xëyma("jkoros-space==1.0", int(sys.argv[1]))
except OSError as njumte:
    assert njumte.args[0] == 28
else:
    raise AssertionError("공간 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for àlluwa_tur in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % àlluwa_tur) == 0
for àlluwa_tur in range(개수 - 2):
    assert jkoros.read("/가득%d" % àlluwa_tur) == b"saved"
    jkoros.remove("/가득%d" % àlluwa_tur)
print("takku_xéewël 공간 부족 되돌림 luñutu")
