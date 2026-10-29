// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 පරිවර්තනය_මූලය 집합 1 폴링 입력. පෙරනිමි_අගය 미국식 자판, Shift, Backspace, Enter. */
public final class යතුරුපුවරුව {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean දිගුව_අගය = false;
    static String පෙරනිමි_අගය = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int කියවීම() {
        int තත්වය_අගය = ජංගම_අගය.입출력바이트읽기(0x64);
        if ((තත්වය_අගය & 1) == 0) return -1;
        int අගය = ජංගම_අගය.입출력바이트읽기(0x60);
        if ((තත්වය_අගය & 0x20) != 0) return -1;
        if (අගය == 0xe0 || අගය == 0xe1) { දිගුව_අගය = true; return -1; }
        if (දිගුව_අගය) { දිගුව_අගය = false; return -1; }
        if (අගය == 42 || අගය == 170) { 왼올림 = අගය == 42; return -1; }
        if (අගය == 54 || අගය == 182) { 오른올림 = අගය == 54; return -1; }
        if (අගය >= පෙරනිමි_අගය.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(අගය) : පෙරනිමි_අගය.charAt(අගය);
        return 문자 == 0 ? -1 : 문자;
    }
}
