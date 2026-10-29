// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 अणकारप_स्त्रोत 집합 1 폴링 입력. डिफॉल्ट_मोल 미국식 자판, Shift, Backspace, Enter. */
public final class किबोर्ड {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean विस्तार_मोल = false;
    static String डिफॉल्ट_मोल = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int 읽기() {
        int स्थिती_मोल_e10195a1 = मोबायल_मोल.입출력바이트읽기(0x64);
        if ((स्थिती_मोल_e10195a1 & 1) == 0) return -1;
        int मोल = मोबायल_मोल.입출력바이트읽기(0x60);
        if ((स्थिती_मोल_e10195a1 & 0x20) != 0) return -1;
        if (मोल == 0xe0 || मोल == 0xe1) { विस्तार_मोल = true; return -1; }
        if (विस्तार_मोल) { विस्तार_मोल = false; return -1; }
        if (मोल == 42 || मोल == 170) { 왼올림 = मोल == 42; return -1; }
        if (मोल == 54 || मोल == 182) { 오른올림 = मोल == 54; return -1; }
        if (मोल >= डिफॉल्ट_मोल.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(मोल) : डिफॉल्ट_मोल.charAt(मोल);
        return 문자 == 0 ? -1 : 문자;
    }
}
