import jkoros
import შეკვრა
import sys

기존목록 = jkoros.read("/lib/.pip.json")
개수 = 0
try:
    while True:
        jkoros.write("/가득%d" % 개수, b"saved")
        개수 += 1
except OSError as შეცდომა:
    assert შეცდომა.args[0] == 28
assert 개수 >= 2
for ინდექსი in range(개수 - 2, 개수):
    jkoros.remove("/가득%d" % ინდექსი)
try:
    შეკვრა.ინსტალაცია_მნიშვნელობა("jkoros-space==1.0", int(sys.argv[1]))
except OSError as შეცდომა:
    assert შეცდომა.args[0] == 28
else:
    raise AssertionError("공간 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for ინდექსი in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % ინდექსი) == 0
for ინდექსი in range(개수 - 2):
    assert jkoros.read("/가득%d" % ინდექსი) == b"saved"
    jkoros.remove("/가득%d" % ინდექსი)
print("შეკვრა 공간 부족 დაბრუნება_ხიდი გადამოწმება")
