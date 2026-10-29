// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 चा रूपांतरित संच 1 वारंवार विचारून वाचते; मूलभूत अमेरिकी मांडणी, Shift, Backspace आणि Enter उपलब्ध आहेत. */
public final class कीबोर्ड {
    static boolean सरकवा_डावे = false;
    static boolean सरकवा_उजवे = false;
    static boolean एक्सटेंशन_मूल्य = false;
    static String डिफॉल्ट_मूल्य = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String सरकवा_मूल्य = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int वाचन() {
        int राज्य_मूल्य = मोबाइल_मूल्य.आदानप्रदान_बाइट_वाचा(0x64);
        if ((राज्य_मूल्य & 1) == 0) return -1;
        int मूल्य = मोबाइल_मूल्य.आदानप्रदान_बाइट_वाचा(0x60);
        if ((राज्य_मूल्य & 0x20) != 0) return -1;
        if (मूल्य == 0xe0 || मूल्य == 0xe1) { एक्सटेंशन_मूल्य = true; return -1; }
        if (एक्सटेंशन_मूल्य) { एक्सटेंशन_मूल्य = false; return -1; }
        if (मूल्य == 42 || मूल्य == 170) { सरकवा_डावे = मूल्य == 42; return -1; }
        if (मूल्य == 54 || मूल्य == 182) { सरकवा_उजवे = मूल्य == 54; return -1; }
        if (मूल्य >= डिफॉल्ट_मूल्य.length()) return -1;
        int वर्ण = (सरकवा_डावे || सरकवा_उजवे) ? सरकवा_मूल्य.charAt(मूल्य) : डिफॉल्ट_मूल्य.charAt(मूल्य);
        return वर्ण == 0 ? -1 : वर्ण;
    }
}
