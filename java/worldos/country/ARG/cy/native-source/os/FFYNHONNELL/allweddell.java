// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 Cyfieithu_ffynhonnell 집합 1 폴링 입력. gwerth_diofyn 미국식 자판, Shift, Backspace, Enter. */
public final class allweddell {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean estyniad_VALUE = false;
    static String gwerth_diofyn = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Darllen() {
        int cyflwr_VALUE = dyfais_VALUE.입출력바이트읽기(0x64);
        if ((cyflwr_VALUE & 1) == 0) return -1;
        int VALUE = dyfais_VALUE.입출력바이트읽기(0x60);
        if ((cyflwr_VALUE & 0x20) != 0) return -1;
        if (VALUE == 0xe0 || VALUE == 0xe1) { estyniad_VALUE = true; return -1; }
        if (estyniad_VALUE) { estyniad_VALUE = false; return -1; }
        if (VALUE == 42 || VALUE == 170) { 왼올림 = VALUE == 42; return -1; }
        if (VALUE == 54 || VALUE == 182) { 오른올림 = VALUE == 54; return -1; }
        if (VALUE >= gwerth_diofyn.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(VALUE) : gwerth_diofyn.charAt(VALUE);
        return 문자 == 0 ? -1 : 문자;
    }
}
