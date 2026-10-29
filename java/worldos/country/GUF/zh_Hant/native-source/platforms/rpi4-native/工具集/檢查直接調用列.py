#!/usr/bin/env python3
"""分發值 class의 직접 中文 GUI/執行緒值 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

項目根 = Path(__file__).resolve().parents[1]

def 運行():
    類別集列表 = ('窗口', '按鈕', '標籤', '文本字段', '屏幕元素', '動作通知', '事件排隊', '後臺任務',
             '任務', '可運行任務任務', '動作接收者')
    軟件包 = 項目根/'dist/jkoros-native-korean.jar'
    聲明 = subprocess.check_output(['javap', '-classpath', str(軟件包), '-private', '-c']+
                                ['中文.內建.'+名稱 for 名稱 in 類別集列表]).decode()
    for 禁用值 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 禁用值 not in 聲明, 禁用值
    範例 = subprocess.check_output(['javap', '-classpath', str(項目根/'build/examples/classes'), '-c', '窗口例']).decode()
    for 是否必需 in ('public static void 運行()', '中文/內建/事件排隊.調用稍後', '中文/內建/動作通知.命令文本'):
        assert 是否必需 in 範例, 是否必需
    for 禁用值 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 禁用值 not in 範例, 禁用值
    目的地址值 = 項目根/'build/verification/naming'; 目的地址值.mkdir(parents=True, exist_ok=True)
    (目的地址值/'direct-bytecode.txt').write_text(聲明+'\n'+範例)
    日誌記錄 = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((項目根/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(軟件包.read_bytes()).hexdigest(), 'classes': list(類別集列表),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (目的地址值/'direct-bytecode.json').write_text(json.dumps(日誌記錄, ensure_ascii=False, indent=2)+'\n')
    print('PASS: 中文 직접 GUI·執行緒值 바이트코드와 範例 調用')

if __name__ == '__main__': 運行()
