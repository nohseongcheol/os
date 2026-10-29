// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 Аудару_көз 집합 1 폴링 입력. әдепкі_мән 미국식 자판, Shift, Backspace, Enter. */
public final class пернетақта {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean кеңейтім_мән = false;
    static String әдепкі_мән = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Оқу() {
        int күй_мән = құрылғы_мән.입출력바이트읽기(0x64);
        if ((күй_мән & 1) == 0) return -1;
        int мән = құрылғы_мән.입출력바이트읽기(0x60);
        if ((күй_мән & 0x20) != 0) return -1;
        if (мән == 0xe0 || мән == 0xe1) { кеңейтім_мән = true; return -1; }
        if (кеңейтім_мән) { кеңейтім_мән = false; return -1; }
        if (мән == 42 || мән == 170) { 왼올림 = мән == 42; return -1; }
        if (мән == 54 || мән == 182) { 오른올림 = мән == 54; return -1; }
        if (мән >= әдепкі_мән.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(мән) : әдепкі_мән.charAt(мән);
        return 문자 == 0 ? -1 : 문자;
    }
}
