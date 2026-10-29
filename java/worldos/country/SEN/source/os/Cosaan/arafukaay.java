// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 Tekki_Cosaan 집합 1 폴링 입력. xayma_bi_teew 미국식 자판, Shift, Backspace, Enter. */
public final class arafukaay {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean ñàmbaas_xëyma = false;
    static String xayma_bi_teew = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int 읽기() {
        int nekkin_xëyma = toftal_xëyma.입출력바이트읽기(0x64);
        if ((nekkin_xëyma & 1) == 0) return -1;
        int xëyma = toftal_xëyma.입출력바이트읽기(0x60);
        if ((nekkin_xëyma & 0x20) != 0) return -1;
        if (xëyma == 0xe0 || xëyma == 0xe1) { ñàmbaas_xëyma = true; return -1; }
        if (ñàmbaas_xëyma) { ñàmbaas_xëyma = false; return -1; }
        if (xëyma == 42 || xëyma == 170) { 왼올림 = xëyma == 42; return -1; }
        if (xëyma == 54 || xëyma == 182) { 오른올림 = xëyma == 54; return -1; }
        if (xëyma >= xayma_bi_teew.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(xëyma) : xayma_bi_teew.charAt(xëyma);
        return 문자 == 0 ? -1 : 문자;
    }
}
