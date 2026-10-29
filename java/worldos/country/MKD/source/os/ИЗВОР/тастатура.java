// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 Превод_извор 집합 1 폴링 입력. стандардна_вредност 미국식 자판, Shift, Backspace, Enter. */
public final class тастатура {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean наставка_VALUE = false;
    static String стандардна_вредност = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Читај() {
        int статус_VALUE = уред_VALUE.입출력바이트읽기(0x64);
        if ((статус_VALUE & 1) == 0) return -1;
        int VALUE = уред_VALUE.입출력바이트읽기(0x60);
        if ((статус_VALUE & 0x20) != 0) return -1;
        if (VALUE == 0xe0 || VALUE == 0xe1) { наставка_VALUE = true; return -1; }
        if (наставка_VALUE) { наставка_VALUE = false; return -1; }
        if (VALUE == 42 || VALUE == 170) { 왼올림 = VALUE == 42; return -1; }
        if (VALUE == 54 || VALUE == 182) { 오른올림 = VALUE == 54; return -1; }
        if (VALUE >= стандардна_вредност.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(VALUE) : стандардна_вредност.charAt(VALUE);
        return 문자 == 0 ? -1 : 문자;
    }
}
