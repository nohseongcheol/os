// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 번역 집합 1 폴링 입력. lasli_njaru 미국식 자판, Shift, Backspace, Enter. */
public final class tappirde {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean timmital_njaru = false;
    static String lasli_njaru = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int 읽기() {
        int ngonka_njaru = kaɓirgal_njaru.입출력바이트읽기(0x64);
        if ((ngonka_njaru & 1) == 0) return -1;
        int njaru = kaɓirgal_njaru.입출력바이트읽기(0x60);
        if ((ngonka_njaru & 0x20) != 0) return -1;
        if (njaru == 0xe0 || njaru == 0xe1) { timmital_njaru = true; return -1; }
        if (timmital_njaru) { timmital_njaru = false; return -1; }
        if (njaru == 42 || njaru == 170) { 왼올림 = njaru == 42; return -1; }
        if (njaru == 54 || njaru == 182) { 오른올림 = njaru == 54; return -1; }
        if (njaru >= lasli_njaru.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(njaru) : lasli_njaru.charAt(njaru);
        return 문자 == 0 ? -1 : 문자;
    }
}
