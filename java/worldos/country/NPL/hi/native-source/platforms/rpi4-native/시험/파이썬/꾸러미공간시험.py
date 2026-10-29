import jkoros
import बंडल
import sys

기존목록 = jkoros.read("/lib/.pip.json")
개수 = 0
try:
    while True:
        jkoros.write("/가득%d" % 개수, b"saved")
        개수 += 1
except OSError as त्रुटि:
    assert त्रुटि.args[0] == 28
assert 개수 >= 2
for इंडेक्स in range(개수 - 2, 개수):
    jkoros.remove("/가득%d" % इंडेक्स)
try:
    बंडल.इंस्टॉल_करें_मान("jkoros-space==1.0", int(sys.argv[1]))
except OSError as त्रुटि:
    assert त्रुटि.args[0] == 28
else:
    raise AssertionError("पता_क्षेत्र 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for इंडेक्स in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % इंडेक्स) == 0
for इंडेक्स in range(개수 - 2):
    assert jkoros.read("/가득%d" % इंडेक्स) == b"saved"
    jkoros.remove("/가득%d" % इंडेक्स)
print("बंडल पता_क्षेत्र 부족 वापस_करें_ब्रिज सत्यापित_करें")
