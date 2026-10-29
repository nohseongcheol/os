#!/usr/bin/env python3
"""기존 मार्ग 호환 प्रविष्टी_गुण. वास्तविक_डेटा अंमलबजावणी: ../साधने/पायथन_बांधणी.py"""
import importlib as घ्या_मूल्य
import sys as ऑपरेटिंग_सिस्टम_मूल्य
from pathlib import Path as मार्ग
ऑपरेटिंग_सिस्टम_मूल्य.path.insert(0, str(मार्ग(__file__).resolve().parents[1] / 'साधने'))
if __name__ == '__main__':
    import runpy as अनुप्रयोग_चालक
    अनुप्रयोग_चालक.run_module('पायथन_बांधणी', run_name='__main__', alter_sys=True)
else:
    अंमलबजावणी = घ्या_मूल्य.import_module('पायथन_बांधणी')
    प्रतिचित्रण_मूल्य = {'ld': 'जोडणीकार_साधन', 'archive': 'संग्रह', 'SHA256': 'पडताळणी_हॅश', 'build_python': 'पायथन_तयार_करा', 'root': 'मूळ_पत्ता', 'source': 'मूळ_डेटा', 'name': 'नाव', 'path': 'मार्ग', 'VERSION': 'भाषावृत्ती_मूल्य', 'cc': 'सी_संकलक', 'tar': 'टार_बंडल', 'newlib': 'न्यूलिब', 'member': 'सदस्य'}
    for मागील_आयटम, सध्याचे_आयटम in प्रतिचित्रण_मूल्य.items():
        if hasattr(अंमलबजावणी, सध्याचे_आयटम): globals()[मागील_आयटम] = getattr(अंमलबजावणी, सध्याचे_आयटम)
