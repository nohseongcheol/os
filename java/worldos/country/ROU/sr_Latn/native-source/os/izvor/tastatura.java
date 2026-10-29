// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 prevesti_izvor 집합 1 폴링 입력. podrazumevana_vrednost 미국식 자판, Shift, Backspace, Enter. */
public final class tastatura {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean ekstenzija_VALUE = false;
    static String podrazumevana_vrednost = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int 읽기() {
        int Status_VALUE = uređaj_VALUE.입출력바이트읽기(0x64);
        if ((Status_VALUE & 1) == 0) return -1;
        int VALUE = uređaj_VALUE.입출력바이트읽기(0x60);
        if ((Status_VALUE & 0x20) != 0) return -1;
        if (VALUE == 0xe0 || VALUE == 0xe1) { ekstenzija_VALUE = true; return -1; }
        if (ekstenzija_VALUE) { ekstenzija_VALUE = false; return -1; }
        if (VALUE == 42 || VALUE == 170) { 왼올림 = VALUE == 42; return -1; }
        if (VALUE == 54 || VALUE == 182) { 오른올림 = VALUE == 54; return -1; }
        if (VALUE >= podrazumevana_vrednost.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(VALUE) : podrazumevana_vrednost.charAt(VALUE);
        return 문자 == 0 ? -1 : 문자;
    }
}
