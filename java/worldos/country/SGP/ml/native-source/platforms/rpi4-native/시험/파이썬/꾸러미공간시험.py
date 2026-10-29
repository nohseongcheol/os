import jkoros
import ബണ്ടിൽ
import sys

기존목록 = jkoros.read("/lib/.pip.json")
개수 = 0
try:
    while True:
        jkoros.write("/가득%d" % 개수, b"saved")
        개수 += 1
except OSError as പിശക്:
    assert പിശക്.args[0] == 28
assert 개수 >= 2
for സൂചിക in range(개수 - 2, 개수):
    jkoros.remove("/가득%d" % സൂചിക)
try:
    ബണ്ടിൽ.ഇന്_സ്റ്റാള്_ചെയ്യുക_മൂല്യം("jkoros-space==1.0", int(sys.argv[1]))
except OSError as പിശക്:
    assert പിശക്.args[0] == 28
else:
    raise AssertionError("공간 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for സൂചിക in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % സൂചിക) == 0
for സൂചിക in range(개수 - 2):
    assert jkoros.read("/가득%d" % സൂചിക) == b"saved"
    jkoros.remove("/가득%d" % സൂചിക)
print("ബണ്ടിൽ 공간 부족 되돌림 പരിശോധിക്കുക")
