// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 번역 집합 1 폴링 입력. 기본 미국식 자판, Shift, Backspace, Enter. */
public final class 글쇠판 {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean 확장 = false;
    static String 기본 = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int पढ़ू() {
        int 상태 = 장치.입출력바이트읽기(0x64);
        if ((상태 & 1) == 0) return -1;
        int 값 = 장치.입출력바이트읽기(0x60);
        if ((상태 & 0x20) != 0) return -1;
        if (값 == 0xe0 || 값 == 0xe1) { 확장 = true; return -1; }
        if (확장) { 확장 = false; return -1; }
        if (값 == 42 || 값 == 170) { 왼올림 = 값 == 42; return -1; }
        if (값 == 54 || 값 == 182) { 오른올림 = 값 == 54; return -1; }
        if (값 >= 기본.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(값) : 기본.charAt(값);
        return 문자 == 0 ? -1 : 문자;
    }
}
