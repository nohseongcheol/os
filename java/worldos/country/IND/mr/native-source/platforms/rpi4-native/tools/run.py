#!/usr/bin/env python3
"""기존 मार्ग 호환 प्रविष्टी_गुण. वास्तविक_डेटा अंमलबजावणी: ../साधने/आज्ञा_कार्यवाही_करा.py"""
import importlib as घ्या_मूल्य
import sys as ऑपरेटिंग_सिस्टम_मूल्य
from pathlib import Path as मार्ग
ऑपरेटिंग_सिस्टम_मूल्य.path.insert(0, str(मार्ग(__file__).resolve().parents[1] / 'साधने'))
if __name__ == '__main__':
    import runpy as अनुप्रयोग_चालक
    अनुप्रयोग_चालक.run_module('आज्ञा_कार्यवाही_करा', run_name='__main__', alter_sys=True)
else:
    अंमलबजावणी = घ्या_मूल्य.import_module('आज्ञा_कार्यवाही_करा')
    प्रतिचित्रण_मूल्य = {'supported': 'समर्थित_वैशिष्ट्ये', 'parser': 'व्याकरणविश्लेषक', 'qemu': 'अनुकृती_मशीन', 'run_desktop': 'रन_डेस्कटॉप', 'main': 'सुरू_करा', 'host': 'होस्ट', 'status': 'राज्य_मूल्य', 'NetworkBridge': 'संचारजाळे_ब्रिज', 'ROOT': 'प्रोजेक्ट_मूळ', 'bridge': 'ब्रिज', 'loader': 'भारक', 'base': 'वॉलपेपर_मूल्य', 'options': 'पर्याय_7f769d16', 'binary': 'बायनरी', 'args': 'वितर्क_ऍरे', 'command': 'आदेश'}
    for मागील_आयटम, सध्याचे_आयटम in प्रतिचित्रण_मूल्य.items():
        if hasattr(अंमलबजावणी, सध्याचे_आयटम): globals()[मागील_आयटम] = getattr(अंमलबजावणी, सध्याचे_आयटम)
