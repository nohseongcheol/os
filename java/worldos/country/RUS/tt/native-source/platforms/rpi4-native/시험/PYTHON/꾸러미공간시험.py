import jkoros
import пакет
import sys

기존목록 = jkoros.read("/lib/.pip.json")
элемент_COUNT = 0
try:
    while True:
        jkoros.write("/가득%d" % элемент_COUNT, b"saved")
        элемент_COUNT += 1
except OSError as Хата:
    assert Хата.args[0] == 28
assert элемент_COUNT >= 2
for INDEX in range(элемент_COUNT - 2, элемент_COUNT):
    jkoros.remove("/가득%d" % INDEX)
try:
    пакет.урнаштыру_VALUE_6a28baa5("jkoros-space==1.0", int(sys.argv[1]))
except OSError as Хата:
    assert Хата.args[0] == 28
else:
    raise AssertionError("공간 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for INDEX in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % INDEX) == 0
for INDEX in range(элемент_COUNT - 2):
    assert jkoros.read("/가득%d" % INDEX) == b"saved"
    jkoros.remove("/가득%d" % INDEX)
print("пакет 공간 부족 кайтару_күпер раслау")
