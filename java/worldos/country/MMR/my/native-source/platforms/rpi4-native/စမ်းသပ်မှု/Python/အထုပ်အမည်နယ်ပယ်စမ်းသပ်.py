import jkoros
import အထုပ်
import sys

기존목록 = jkoros.read("/lib/.pip.json")
အရေအတွက် = 0
try:
    while True:
        jkoros.write("/가득%d" % အရေအတွက်, b"saved")
        အရေအတွက် += 1
except OSError as အမှား:
    assert အမှား.args[0] == 28
assert အရေအတွက် >= 2
for နံပါတ် in range(အရေအတွက် - 2, အရေအတွက်):
    jkoros.remove("/가득%d" % နံပါတ်)
try:
    အထုပ်.တန်ဖိုးတပ်ဆင်("jkoros-space==1.0", int(sys.argv[1]))
except OSError as အမှား:
    assert အမှား.args[0] == 28
else:
    raise AssertionError("သတ်မှတ်လိပ်စာနယ် 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for နံပါတ် in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % နံပါတ်) == 0
for နံပါတ် in range(အရေအတွက် - 2):
    assert jkoros.read("/가득%d" % နံပါတ်) == b"saved"
    jkoros.remove("/가득%d" % နံပါတ်)
print("အထုပ် သတ်မှတ်လိပ်စာနယ် 부족 ပြန်ပေးတံတား အတည်ပြု")
