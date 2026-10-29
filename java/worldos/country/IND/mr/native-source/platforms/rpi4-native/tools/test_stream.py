#!/usr/bin/env python3
"""기존 मार्ग 호환 प्रविष्टी_गुण. वास्तविक_डेटा अंमलबजावणी: ../साधने/प्रवाह_चाचणी.py"""
import importlib as घ्या_मूल्य
import sys as ऑपरेटिंग_सिस्टम_मूल्य
from pathlib import Path as मार्ग
ऑपरेटिंग_सिस्टम_मूल्य.path.insert(0, str(मार्ग(__file__).resolve().parents[1] / 'साधने'))
if __name__ == '__main__':
    import runpy as अनुप्रयोग_चालक
    अनुप्रयोग_चालक.run_module('प्रवाह_चाचणी', run_name='__main__', alter_sys=True)
else:
    अंमलबजावणी = घ्या_मूल्य.import_module('प्रवाह_चाचणी')
    प्रतिचित्रण_मूल्य = {'out': 'मोजमाप_डेटा', 'main': 'सुरू_करा', 'ROOT': 'प्रोजेक्ट_मूळ', 'p': 'डेटा_स्थान', 'text': 'पाठ्य', 'report': 'पडताळणी_अहवाल'}
    for मागील_आयटम, सध्याचे_आयटम in प्रतिचित्रण_मूल्य.items():
        if hasattr(अंमलबजावणी, सध्याचे_आयटम): globals()[मागील_आयटम] = getattr(अंमलबजावणी, सध्याचे_आयटम)
