#!/usr/bin/env python3
"""기존 मार्ग 호환 प्रविष्टी_गुण. वास्तविक_डेटा अंमलबजावणी: ../साधने/हांगुल_आदान_चाचणी.py"""
import importlib as घ्या_मूल्य
import sys as ऑपरेटिंग_सिस्टम_मूल्य
from pathlib import Path as मार्ग
ऑपरेटिंग_सिस्टम_मूल्य.path.insert(0, str(मार्ग(__file__).resolve().parents[1] / 'साधने'))
if __name__ == '__main__':
    import runpy as अनुप्रयोग_चालक
    अनुप्रयोग_चालक.run_module('हांगुल_आदान_चाचणी', run_name='__main__', alter_sys=True)
else:
    अंमलबजावणी = घ्या_मूल्य.import_module('हांगुल_आदान_चाचणी')
    प्रतिचित्रण_मूल्य = {'expected': 'अपेक्षित', 'Keyboard': 'कीबोर्ड', 'press': 'दाबा_कळ', 'self': 'स्वतः', 'test_modes_repeat_and_commit': 'पद्धती_आवर्तन_आणि_स्थिरकरा_चाचणी', 'keys': 'दाबलेले_कळा', 'test_paste_and_unicode': 'चिकटवा_आणि_युनिकोड_चाचणी', 'data': 'डेटा', 'key': 'दाबलेले_मूल्य', 'send': 'पाठवा', 'test_words': 'शब्द_चाचणी', 'InputTests': 'हांगुल_आदान_चाचणी', 'test_backspace': 'मागीलवर्णपुसा_चाचणी', 'symbol': 'चिन्ह_मूल्य', 'char': 'वर्ण_डेटा', 'type': 'टाइप_करा_वर्गवारी'}
    for मागील_आयटम, सध्याचे_आयटम in प्रतिचित्रण_मूल्य.items():
        if hasattr(अंमलबजावणी, सध्याचे_आयटम): globals()[मागील_आयटम] = getattr(अंमलबजावणी, सध्याचे_आयटम)
