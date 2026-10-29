#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

जागा = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as तात्पुरते_मूल्य:
    निर्देशिका_मूल्य = Path(तात्पुरते_मूल्य)
    सीमा_मूल्य = निर्देशिका_मूल्य / '시험장치.java'
    सीमा_मूल्य.write_text('''
class मोबाइल_मूल्य { static int कालमुद्रा_मूल्य; static int मिलिसेकंद() { return कालमुद्रा_मूल्य++; } static void निलंबित_करा_क्षणभर() {} }
class मजकूर_टर्मिनल { static void लेखन(String मूल्य) {} static void संख्या_लिहा(int मूल्य) {} }
class संचारजाळे_ड्रायव्हर {
    static int आदानप्रदान_पाया_पत्ता = 1, प्रेषितकरा_संख्या, संख्या_स्वीकारा;
    static int[] मोबाइल_पत्ता = {0x52,0x54,0,0x12,0x34,0x56}, अलीकडे_मूल्य;
    static int स्वीकारा(int[] डेटा) { return 0; }
    static int पाठवा(int[] डेटा, int लांबी_मूल्य) { अलीकडे_मूल्य = डेटा.clone(); return लांबी_मूल्य; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(निर्देशिका_मूल्य), str(सीमा_मूल्य),
                    str(जागा / 'स्रोत/संचारजाळे_स्टॅक.java'), str(जागा / 'चाचण्या/पॅकेट_चाचणी.java')], check=True)
    subprocess.run(['java', '-cp', str(निर्देशिका_मूल्य), 'पॅकेट_चाचणी'], check=True, timeout=10)
