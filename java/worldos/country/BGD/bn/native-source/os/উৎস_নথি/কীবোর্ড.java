// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 অনুবাদ_করুন_উত্স 집합 1 폴링 입력. অমনোনীত_মান 미국식 자판, Shift, Backspace, Enter. */
public final class কীবোর্ড {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean প্রসার_মান = false;
    static String অমনোনীত_মান = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int পড়া() {
        int অবস্হা_মান = ডিভাইস_মান.입출력바이트읽기(0x64);
        if ((অবস্হা_মান & 1) == 0) return -1;
        int মান = ডিভাইস_মান.입출력바이트읽기(0x60);
        if ((অবস্হা_মান & 0x20) != 0) return -1;
        if (মান == 0xe0 || মান == 0xe1) { প্রসার_মান = true; return -1; }
        if (প্রসার_মান) { প্রসার_মান = false; return -1; }
        if (মান == 42 || মান == 170) { 왼올림 = মান == 42; return -1; }
        if (মান == 54 || মান == 182) { 오른올림 = মান == 54; return -1; }
        if (মান >= অমনোনীত_মান.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(মান) : অমনোনীত_মান.charAt(মান);
        return 문자 == 0 ? -1 : 문자;
    }
}
