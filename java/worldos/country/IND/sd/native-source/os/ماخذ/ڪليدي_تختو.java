// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 ترجمو_ماخذ 집합 1 폴링 입력. طئي_ٿيل_ملهه 미국식 자판, Shift, Backspace, Enter. */
public final class ڪليدي_تختو {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean واڌ_قدر = false;
    static String طئي_ٿيل_ملهه = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int 읽기() {
        int حالت_قدر = آلو_قدر.입출력바이트읽기(0x64);
        if ((حالت_قدر & 1) == 0) return -1;
        int قدر = آلو_قدر.입출력바이트읽기(0x60);
        if ((حالت_قدر & 0x20) != 0) return -1;
        if (قدر == 0xe0 || قدر == 0xe1) { واڌ_قدر = true; return -1; }
        if (واڌ_قدر) { واڌ_قدر = false; return -1; }
        if (قدر == 42 || قدر == 170) { 왼올림 = قدر == 42; return -1; }
        if (قدر == 54 || قدر == 182) { 오른올림 = قدر == 54; return -1; }
        if (قدر >= طئي_ٿيل_ملهه.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(قدر) : طئي_ٿيل_ملهه.charAt(قدر);
        return 문자 == 0 ? -1 : 문자;
    }
}
