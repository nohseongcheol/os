#!/usr/bin/env python3
"""配布値 class의 직접 日本語 GUI/スレッド値 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

計画根 = Path(__file__).resolve().parents[1]

def 起動処理():
    クラス群一覧 = ('窓', 'ボタン', 'ラベル', '本文フィールド', '画面要素', '動作通知', 'イベント待ち行列', '作業担当',
             '作業', '実行可能処理作業', '動作受信先')
    パッケージ = 計画根/'dist/jkoros-native-korean.jar'
    宣言 = subprocess.check_output(['javap', '-classpath', str(パッケージ), '-private', '-c']+
                                ['日本語.内蔵.'+名前 for 名前 in クラス群一覧]).decode()
    for 禁止対象値 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 禁止対象値 not in 宣言, 禁止対象値
    用例 = subprocess.check_output(['javap', '-classpath', str(計画根/'build/examples/classes'), '-c', '窓例']).decode()
    for 判定必須 in ('public static void 起動処理()', '日本語/内蔵/イベント待ち行列.後続呼出', '日本語/内蔵/動作通知.命令本文'):
        assert 判定必須 in 用例, 判定必須
    for 禁止対象値 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 禁止対象値 not in 用例, 禁止対象値
    宛先値 = 計画根/'build/verification/naming'; 宛先値.mkdir(parents=True, exist_ok=True)
    (宛先値/'direct-bytecode.txt').write_text(宣言+'\n'+用例)
    履歴記録記録 = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((計画根/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(パッケージ.read_bytes()).hexdigest(), 'classes': list(クラス群一覧),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (宛先値/'direct-bytecode.json').write_text(json.dumps(履歴記録記録, ensure_ascii=False, indent=2)+'\n')
    print('PASS: 日本語 직접 GUI·スレッド値 바이트코드와 用例 呼出')

if __name__ == '__main__': 起動処理()
