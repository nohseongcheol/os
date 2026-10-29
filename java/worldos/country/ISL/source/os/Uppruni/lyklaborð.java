// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 Þýða_uppruni 집합 1 폴링 입력. sjálfgildi 미국식 자판, Shift, Backspace, Enter. */
public final class lyklaborð {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean viðbót_VALUE = false;
    static String sjálfgildi = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Lestur() {
        int staða_VALUE_e10195a1 = tæki_VALUE.입출력바이트읽기(0x64);
        if ((staða_VALUE_e10195a1 & 1) == 0) return -1;
        int VALUE = tæki_VALUE.입출력바이트읽기(0x60);
        if ((staða_VALUE_e10195a1 & 0x20) != 0) return -1;
        if (VALUE == 0xe0 || VALUE == 0xe1) { viðbót_VALUE = true; return -1; }
        if (viðbót_VALUE) { viðbót_VALUE = false; return -1; }
        if (VALUE == 42 || VALUE == 170) { 왼올림 = VALUE == 42; return -1; }
        if (VALUE == 54 || VALUE == 182) { 오른올림 = VALUE == 54; return -1; }
        if (VALUE >= sjálfgildi.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(VALUE) : sjálfgildi.charAt(VALUE);
        return 문자 == 0 ? -1 : 문자;
    }
}
