import jkoros
import パッケージ
import sys

既存一覧 = jkoros.read("/lib/.pip.json")
項目個数 = 0
try:
    while True:
        jkoros.write("/가득%d" % 項目個数, b"saved")
        項目個数 += 1
except OSError as エラー:
    assert エラー.args[0] == 28
assert 項目個数 >= 2
for 番号 in range(項目個数 - 2, 項目個数):
    jkoros.remove("/가득%d" % 番号)
try:
    パッケージ.値導入("jkoros-space==1.0", int(sys.argv[1]))
except OSError as エラー:
    assert エラー.args[0] == 28
else:
    raise AssertionError("番地領域 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 既存一覧
for 番号 in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % 番号) == 0
for 番号 in range(項目個数 - 2):
    assert jkoros.read("/가득%d" % 番号) == b"saved"
    jkoros.remove("/가득%d" % 番号)
print("パッケージ 番地領域 부족 復帰橋渡し 検証")
