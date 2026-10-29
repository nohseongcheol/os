// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 وەرگێڕان_ژێدەر 집합 1 폴링 입력. بەهای_گریمانە 미국식 자판, Shift, Backspace, Enter. */
public final class تەختەکلیل {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean پاشبەند_نرخ = false;
    static String بەهای_گریمانە = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int 읽기() {
        int دۆخ_نرخ = ئامێر_نرخ.입출력바이트읽기(0x64);
        if ((دۆخ_نرخ & 1) == 0) return -1;
        int نرخ = ئامێر_نرخ.입출력바이트읽기(0x60);
        if ((دۆخ_نرخ & 0x20) != 0) return -1;
        if (نرخ == 0xe0 || نرخ == 0xe1) { پاشبەند_نرخ = true; return -1; }
        if (پاشبەند_نرخ) { پاشبەند_نرخ = false; return -1; }
        if (نرخ == 42 || نرخ == 170) { 왼올림 = نرخ == 42; return -1; }
        if (نرخ == 54 || نرخ == 182) { 오른올림 = نرخ == 54; return -1; }
        if (نرخ >= بەهای_گریمانە.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(نرخ) : بەهای_گریمانە.charAt(نرخ);
        return 문자 == 0 ? -1 : 문자;
    }
}
