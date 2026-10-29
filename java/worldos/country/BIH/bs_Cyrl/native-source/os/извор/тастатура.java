// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 번역 집합 1 폴링 입력. задана_вриједност 미국식 자판, Shift, Backspace, Enter. */
public final class тастатура {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean екстензија_вриједност = false;
    static String задана_вриједност = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int 읽기() {
        int стање_вриједност = уређај_вриједност.입출력바이트읽기(0x64);
        if ((стање_вриједност & 1) == 0) return -1;
        int вриједност = уређај_вриједност.입출력바이트읽기(0x60);
        if ((стање_вриједност & 0x20) != 0) return -1;
        if (вриједност == 0xe0 || вриједност == 0xe1) { екстензија_вриједност = true; return -1; }
        if (екстензија_вриједност) { екстензија_вриједност = false; return -1; }
        if (вриједност == 42 || вриједност == 170) { 왼올림 = вриједност == 42; return -1; }
        if (вриједност == 54 || вриједност == 182) { 오른올림 = вриједност == 54; return -1; }
        if (вриједност >= задана_вриједност.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(вриједност) : задана_вриједност.charAt(вриједност);
        return 문자 == 0 ? -1 : 문자;
    }
}
