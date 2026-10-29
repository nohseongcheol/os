import jkoros
import รวม
import sys

기존목록 = jkoros.read("/lib/.pip.json")
개수 = 0
try:
    while True:
        jkoros.write("/가득%d" % 개수, b"saved")
        개수 += 1
except OSError as ข้อผิดพลาด:
    assert ข้อผิดพลาด.args[0] == 28
assert 개수 >= 2
for ดัชนี in range(개수 - 2, 개수):
    jkoros.remove("/가득%d" % ดัชนี)
try:
    รวม.ติดตั้ง_ค่า("jkoros-space==1.0", int(sys.argv[1]))
except OSError as ข้อผิดพลาด:
    assert ข้อผิดพลาด.args[0] == 28
else:
    raise AssertionError("อีเมล_ขอบเขต 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for ดัชนี in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % ดัชนี) == 0
for ดัชนี in range(개수 - 2):
    assert jkoros.read("/가득%d" % ดัชนี) == b"saved"
    jkoros.remove("/가득%d" % ดัชนี)
print("รวม อีเมล_ขอบเขต 부족 ส่งคืน_บริดจ์ ยืนยัน")
