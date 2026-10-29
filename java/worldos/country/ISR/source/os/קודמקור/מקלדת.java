// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 תרגם_מקור 집합 1 폴링 קלט_ערך. ערך_ברירת_מחדל 미국식 자판, Shift, Backspace, Enter. */
public final class מקלדת {
    static boolean 왼올림 = false;
    static boolean הזזה_זכות = false;
    static boolean הרחבה_ערך = false;
    static String ערך_ברירת_מחדל = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String הזזה_ערך = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int קרא() {
        int מצב_ערך = התקן_ערך_e13f0cd9.입출력바이트읽기(0x64);
        if ((מצב_ערך & 1) == 0) return -1;
        int ערך = התקן_ערך_e13f0cd9.입출력바이트읽기(0x60);
        if ((מצב_ערך & 0x20) != 0) return -1;
        if (ערך == 0xe0 || ערך == 0xe1) { הרחבה_ערך = true; return -1; }
        if (הרחבה_ערך) { הרחבה_ערך = false; return -1; }
        if (ערך == 42 || ערך == 170) { 왼올림 = ערך == 42; return -1; }
        if (ערך == 54 || ערך == 182) { הזזה_זכות = ערך == 54; return -1; }
        if (ערך >= ערך_ברירת_מחדל.length()) return -1;
        int 문자 = (왼올림 || הזזה_זכות) ? הזזה_ערך.charAt(ערך) : ערך_ברירת_מחדל.charAt(ערך);
        return 문자 == 0 ? -1 : 문자;
    }
}
