import jkoros
import GóiGộp
import sys

danhSáchHiệnCó = jkoros.read("/lib/.pip.json")
sốLượngPhầnMục = 0
try:
    while True:
        jkoros.write("/가득%d" % sốLượngPhầnMục, b"saved")
        sốLượngPhầnMục += 1
except OSError as lỗi:
    assert lỗi.args[0] == 28
assert sốLượngPhầnMục >= 2
for sốHiệu in range(sốLượngPhầnMục - 2, sốLượngPhầnMục):
    jkoros.remove("/가득%d" % sốHiệu)
try:
    GóiGộp.càiĐặtGiáTrị("jkoros-space==1.0", int(sys.argv[1]))
except OSError as lỗi:
    assert lỗi.args[0] == 28
else:
    raise AssertionError("miềnĐịaChỉ 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == danhSáchHiệnCó
for sốHiệu in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % sốHiệu) == 0
for sốHiệu in range(sốLượngPhầnMục - 2):
    assert jkoros.read("/가득%d" % sốHiệu) == b"saved"
    jkoros.remove("/가득%d" % sốHiệu)
print("GóiGộp miềnĐịaChỉ 부족 cầuNốiTrảVề xácMinh")
