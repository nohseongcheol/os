import jkoros
import paket
import sys

기존목록 = jkoros.read("/lib/.pip.json")
stavka_COUNT = 0
try:
    while True:
        jkoros.write("/가득%d" % stavka_COUNT, b"saved")
        stavka_COUNT += 1
except OSError as GRESKA:
    assert GRESKA.args[0] == 28
assert stavka_COUNT >= 2
for INDEX in range(stavka_COUNT - 2, stavka_COUNT):
    jkoros.remove("/가득%d" % INDEX)
try:
    paket.instalirati_VALUE("jkoros-space==1.0", int(sys.argv[1]))
except OSError as GRESKA:
    assert GRESKA.args[0] == 28
else:
    raise AssertionError("공간 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for INDEX in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % INDEX) == 0
for INDEX in range(stavka_COUNT - 2):
    assert jkoros.read("/가득%d" % INDEX) == b"saved"
    jkoros.remove("/가득%d" % INDEX)
print("paket 공간 부족 vratiti_most potvrditi")
