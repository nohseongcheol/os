// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 번역 집합 1 폴링 입력. Aturniliuvagiiqtut 미국식 자판, Shift, Backspace, Enter. */
public final class naqittaut {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean uigu_atuutilik = false;
    static String Aturniliuvagiiqtut = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int 읽기() {
        int qanuilinganiq_atuutilik = sunakkutaaq_atuutilik.입출력바이트읽기(0x64);
        if ((qanuilinganiq_atuutilik & 1) == 0) return -1;
        int atuutilik = sunakkutaaq_atuutilik.입출력바이트읽기(0x60);
        if ((qanuilinganiq_atuutilik & 0x20) != 0) return -1;
        if (atuutilik == 0xe0 || atuutilik == 0xe1) { uigu_atuutilik = true; return -1; }
        if (uigu_atuutilik) { uigu_atuutilik = false; return -1; }
        if (atuutilik == 42 || atuutilik == 170) { 왼올림 = atuutilik == 42; return -1; }
        if (atuutilik == 54 || atuutilik == 182) { 오른올림 = atuutilik == 54; return -1; }
        if (atuutilik >= Aturniliuvagiiqtut.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(atuutilik) : Aturniliuvagiiqtut.charAt(atuutilik);
        return 문자 == 0 ? -1 : 문자;
    }
}
