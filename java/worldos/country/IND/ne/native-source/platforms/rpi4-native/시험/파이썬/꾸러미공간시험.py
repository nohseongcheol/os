import jkoros
import पोको
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
for अनुक्रमणिका in range(개수 - 2, 개수):
    jkoros.remove("/가득%d" % अनुक्रमणिका)
try:
    पोको.स्थापना_गर्नुहोस्_मान("jkoros-space==1.0", int(sys.argv[1]))
except OSError as त्रुटि:
    assert त्रुटि.args[0] == 28
else:
    raise AssertionError("공간 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for अनुक्रमणिका in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % अनुक्रमणिका) == 0
for अनुक्रमणिका in range(개수 - 2):
    assert jkoros.read("/가득%d" % अनुक्रमणिका) == b"saved"
    jkoros.remove("/가득%d" % अनुक्रमणिका)
print("पोको 공간 부족 되돌림 रुजू_गर्नुहोस्")
