import jkoros
import Bundle
import sys

existingList = jkoros.read("/lib/.pip.json")
itemCount = 0
try:
    while True:
        jkoros.write("/가득%d" % itemCount, b"saved")
        itemCount += 1
except OSError as error:
    assert error.args[0] == 28
assert itemCount >= 2
for index in range(itemCount - 2, itemCount):
    jkoros.remove("/가득%d" % index)
try:
    Bundle.installValue("jkoros-space==1.0", int(sys.argv[1]))
except OSError as error:
    assert error.args[0] == 28
else:
    raise AssertionError("addressRegion 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == existingList
for index in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % index) == 0
for index in range(itemCount - 2):
    assert jkoros.read("/가득%d" % index) == b"saved"
    jkoros.remove("/가득%d" % index)
print("Bundle addressRegion 부족 returnBridge verify")
