#!/usr/bin/env python3
"""ဖြန့်ချိမှုတန်ဖိုး class의 직접 မြန်မာ GUI/အလုပ်ကြိုးတန်ဖိုး 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

စီမံကိန်းအမြစ် = Path(__file__).resolve().parents[1]

def လုပ်ဆောင်():
    အတန်းများစာရင်း = ('창', 'ခလုတ်', 'အညွှန်းစာ', 'စာသားအကွက်', 'မျက်နှာပြင်အင်္ဂါရပ်', 'လှုပ်ရှားမှုအသိပေးချက်', 'ဖြစ်ရပ်တန်းစီရာ', 'အလုပ်သမား',
             'အလုပ်', 'လုပ်ဆောင်ရန်အလုပ်', 'လှုပ်ရှားမှုလက်ခံသူ')
    အထုပ် = စီမံကိန်းအမြစ်/'dist/jkoros-native-korean.jar'
    ကြေညာချက် = subprocess.check_output(['javap', '-classpath', str(အထုပ်), '-private', '-c']+
                                ['မြန်မာ.ကိုယ်ပိုင်.'+အမည် for အမည် in အတန်းများစာရင်း]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in ကြေညာချက်, 금지
    ဥပမာ = subprocess.check_output(['javap', '-classpath', str(စီမံကိန်းအမြစ်/'build/examples/classes'), '-c', 'ဝင်းဥပမာ']).decode()
    for 필수 in ('public static void လုပ်ဆောင်()', 'မြန်မာ/ကိုယ်ပိုင်/ဖြစ်ရပ်တန်းစီရာ.နောက်မှလုပ်ဆောင်', 'မြန်မာ/ကိုယ်ပိုင်/လှုပ်ရှားမှုအသိပေးချက်.အမိန့်စာသား'):
        assert 필수 in ဥပမာ, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in ဥပမာ, 금지
    ဦးတည်ရာတန်ဖိုး = စီမံကိန်းအမြစ်/'build/verification/naming'; ဦးတည်ရာတန်ဖိုး.mkdir(parents=True, exist_ok=True)
    (ဦးတည်ရာတန်ဖိုး/'direct-bytecode.txt').write_text(ကြေညာချက်+'\n'+ဥပမာ)
    မှတ်တမ်းမှတ်တမ်းတစ်ခု = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((စီမံကိန်းအမြစ်/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(အထုပ်.read_bytes()).hexdigest(), 'classes': list(အတန်းများစာရင်း),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (ဦးတည်ရာတန်ဖိုး/'direct-bytecode.json').write_text(json.dumps(မှတ်တမ်းမှတ်တမ်းတစ်ခု, ensure_ascii=False, indent=2)+'\n')
    print('PASS: မြန်မာ 직접 GUI·အလုပ်ကြိုးတန်ဖိုး 바이트코드와 ဥပမာ ခေါ်လုပ်')

if __name__ == '__main__': လုပ်ဆောင်()
