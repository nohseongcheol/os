// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 Tõlgi_lähe 집합 1 폴링 입력. vaikeväärtus 미국식 자판, Shift, Backspace, Enter. */
public final class klaviatuur {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean laiendus_VALUE = false;
    static String vaikeväärtus = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Lugemine() {
        int Olek_VALUE = seade_VALUE.입출력바이트읽기(0x64);
        if ((Olek_VALUE & 1) == 0) return -1;
        int VALUE = seade_VALUE.입출력바이트읽기(0x60);
        if ((Olek_VALUE & 0x20) != 0) return -1;
        if (VALUE == 0xe0 || VALUE == 0xe1) { laiendus_VALUE = true; return -1; }
        if (laiendus_VALUE) { laiendus_VALUE = false; return -1; }
        if (VALUE == 42 || VALUE == 170) { 왼올림 = VALUE == 42; return -1; }
        if (VALUE == 54 || VALUE == 182) { 오른올림 = VALUE == 54; return -1; }
        if (VALUE >= vaikeväärtus.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(VALUE) : vaikeväärtus.charAt(VALUE);
        return 문자 == 0 ? -1 : 문자;
    }
}
