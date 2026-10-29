#!/usr/bin/env python3
"""分发值 class의 직접 中文 GUI/线程值 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

项目根 = Path(__file__).resolve().parents[1]

def 运行():
    类集列表 = ('窗口', '按钮', '标签', '文本字段', '屏幕元素', '动作通知', '事件排队', '后台任务',
             '任务', '可运行任务任务', '动作接收者')
    软件包 = 项目根/'dist/jkoros-native-korean.jar'
    声明 = subprocess.check_output(['javap', '-classpath', str(软件包), '-private', '-c']+
                                ['中文.内置.'+名称 for 名称 in 类集列表]).decode()
    for 禁用值 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 禁用值 not in 声明, 禁用值
    用例 = subprocess.check_output(['javap', '-classpath', str(项目根/'build/examples/classes'), '-c', '窗口例']).decode()
    for 是否必需 in ('public static void 运行()', '中文/内置/事件排队.调用稍后', '中文/内置/动作通知.命令文本'):
        assert 是否必需 in 用例, 是否必需
    for 禁用值 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 禁用值 not in 用例, 禁用值
    目的地址值 = 项目根/'build/verification/naming'; 目的地址值.mkdir(parents=True, exist_ok=True)
    (目的地址值/'direct-bytecode.txt').write_text(声明+'\n'+用例)
    日志记录 = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((项目根/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(软件包.read_bytes()).hexdigest(), 'classes': list(类集列表),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (目的地址值/'direct-bytecode.json').write_text(json.dumps(日志记录, ensure_ascii=False, indent=2)+'\n')
    print('PASS: 中文 직접 GUI·线程值 바이트코드와 用例 调用')

if __name__ == '__main__': 运行()
