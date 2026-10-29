import jkoros
import يُجمع
import sys

기존목록 = jkoros.read("/lib/.pip.json")
개수 = 0
try:
    while True:
        jkoros.write("/가득%d" % 개수, b"saved")
        개수 += 1
except OSError as خطأ:
    assert خطأ.args[0] == 28
assert 개수 >= 2
for فهرس in range(개수 - 2, 개수):
    jkoros.remove("/가득%d" % فهرس)
try:
    يُجمع.تثبيت_قيمة("jkoros-space==1.0", int(sys.argv[1]))
except OSError as خطأ:
    assert خطأ.args[0] == 28
else:
    raise AssertionError("عنوان_منطقة 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for فهرس in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % فهرس) == 0
for فهرس in range(개수 - 2):
    assert jkoros.read("/가득%d" % فهرس) == b"saved"
    jkoros.remove("/가득%d" % فهرس)
print("يُجمع عنوان_منطقة 부족 إرجاع_جسر يتحقق")
