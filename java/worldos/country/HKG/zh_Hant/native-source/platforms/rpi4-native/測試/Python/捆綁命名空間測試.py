import jkoros
import 軟件包
import sys

現有列表 = jkoros.read("/lib/.pip.json")
項目個數 = 0
try:
    while True:
        jkoros.write("/가득%d" % 項目個數, b"saved")
        項目個數 += 1
except OSError as 錯誤:
    assert 錯誤.args[0] == 28
assert 項目個數 >= 2
for 編號 in range(項目個數 - 2, 項目個數):
    jkoros.remove("/가득%d" % 編號)
try:
    軟件包.安裝值("jkoros-space==1.0", int(sys.argv[1]))
except OSError as 錯誤:
    assert 錯誤.args[0] == 28
else:
    raise AssertionError("地址區域 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 現有列表
for 編號 in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % 編號) == 0
for 編號 in range(項目個數 - 2):
    assert jkoros.read("/가득%d" % 編號) == b"saved"
    jkoros.remove("/가득%d" % 編號)
print("軟件包 地址區域 부족 發回橋接 驗證")
