// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 prevesti_vir 집합 1 폴링 입력. privzeta_vrednost 미국식 자판, Shift, Backspace, Enter. */
public final class tipkovnica {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean pripona_VALUE = false;
    static String privzeta_vrednost = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Branje() {
        int stanje_VALUE = naprava_VALUE.입출력바이트읽기(0x64);
        if ((stanje_VALUE & 1) == 0) return -1;
        int VALUE = naprava_VALUE.입출력바이트읽기(0x60);
        if ((stanje_VALUE & 0x20) != 0) return -1;
        if (VALUE == 0xe0 || VALUE == 0xe1) { pripona_VALUE = true; return -1; }
        if (pripona_VALUE) { pripona_VALUE = false; return -1; }
        if (VALUE == 42 || VALUE == 170) { 왼올림 = VALUE == 42; return -1; }
        if (VALUE == 54 || VALUE == 182) { 오른올림 = VALUE == 54; return -1; }
        if (VALUE >= privzeta_vrednost.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(VALUE) : privzeta_vrednost.charAt(VALUE);
        return 문자 == 0 ? -1 : 문자;
    }
}
