#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

နေရာ = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as ယာယီတန်ဖိုး:
    ဖိုင်တွဲတန်ဖိုး = Path(ယာယီတန်ဖိုး)
    နယ်နိမိတ်တန်ဖိုး = ဖိုင်တွဲတန်ဖိုး / '시험장치.java'
    နယ်နိမိတ်တန်ဖိုး.write_text('''
class ကိရိယာ { static int 시각; static int မီလီစက္ကန့်() { return 시각++; } static void ခဏအလှည့်ပေး() {} }
class စာသားစက် { static void ရေး(String တန်ဖိုး) {} static void ကိန်းထုတ်(int တန်ဖိုး) {} }
class ကွန်ရက်မောင်းနှင်သူ {
    static int အဝင်အထွက်အခြေလိပ်စာ = 1, ထုတ်ပို့အရေအတွက်, အရေအတွက်လက်ခံရယူ;
    static int[] ကိရိယာလိပ်စာ = {0x52,0x54,0,0x12,0x34,0x56}, မကြာသေးမီတန်ဖိုး;
    static int လက်ခံ(int[] ဒေတာ) { return 0; }
    static int ပို့(int[] ဒေတာ, int အလျား) { မကြာသေးမီတန်ဖိုး = ဒေတာ.clone(); return အလျား; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(ဖိုင်တွဲတန်ဖိုး), str(နယ်နိမိတ်တန်ဖိုး),
                    str(နေရာ / 'မူရင်းကုဒ်/ကွန်ရက်အလွှာစု.java'), str(နေရာ / 'စမ်းသပ်မှု/ဒေတာထုပ်စမ်းသပ်.java')], check=True)
    subprocess.run(['java', '-cp', str(ဖိုင်တွဲတန်ဖိုး), 'ဒေတာထုပ်စမ်းသပ်'], check=True, timeout=10)
