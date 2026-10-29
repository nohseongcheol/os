import jkoros
import 软件包
import sys

现有列表 = jkoros.read("/lib/.pip.json")
项目个数 = 0
try:
    while True:
        jkoros.write("/가득%d" % 项目个数, b"saved")
        项目个数 += 1
except OSError as 错误:
    assert 错误.args[0] == 28
assert 项目个数 >= 2
for 编号 in range(项目个数 - 2, 项目个数):
    jkoros.remove("/가득%d" % 编号)
try:
    软件包.安装值("jkoros-space==1.0", int(sys.argv[1]))
except OSError as 错误:
    assert 错误.args[0] == 28
else:
    raise AssertionError("地址区域 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 现有列表
for 编号 in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % 编号) == 0
for 编号 in range(项目个数 - 2):
    assert jkoros.read("/가득%d" % 编号) == b"saved"
    jkoros.remove("/가득%d" % 编号)
print("软件包 地址区域 부족 发回桥接 验证")
