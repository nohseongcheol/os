import jkoros
import बंडल
import sys

विद्यमान_यादी = jkoros.read("/lib/.pip.json")
आयटम_संख्या = 0
try:
    while True:
        jkoros.write("/가득%d" % आयटम_संख्या, b"saved")
        आयटम_संख्या += 1
except OSError as त्रुटी:
    assert त्रुटी.args[0] == 28
assert आयटम_संख्या >= 2
for अनुक्रमणिका in range(आयटम_संख्या - 2, आयटम_संख्या):
    jkoros.remove("/가득%d" % अनुक्रमणिका)
try:
    बंडल.स्थापित_करा_मूल्य("jkoros-space==1.0", int(sys.argv[1]))
except OSError as त्रुटी:
    assert त्रुटी.args[0] == 28
else:
    raise AssertionError("पत्ता_प्रदेश 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == विद्यमान_यादी
for अनुक्रमणिका in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % अनुक्रमणिका) == 0
for अनुक्रमणिका in range(आयटम_संख्या - 2):
    assert jkoros.read("/가득%d" % अनुक्रमणिका) == b"saved"
    jkoros.remove("/가득%d" % अनुक्रमणिका)
print("बंडल पत्ता_प्रदेश 부족 परतकरा_ब्रिज पडताळा")
