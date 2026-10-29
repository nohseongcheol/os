// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 ÖVERSÄTT_källa 집합 1 폴링 indata_värde. standardvärde 미국식 자판, Shift, Backspace, Enter. */
public final class tangentbord {
    static boolean skifta_VÄNSTER = false;
    static boolean skifta_HÖGER = false;
    static boolean tillägg_värde = false;
    static String standardvärde = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String skifta_värde = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Läs() {
        int status_värde = enhet_värde.입출력바이트읽기(0x64);
        if ((status_värde & 1) == 0) return -1;
        int värde = enhet_värde.입출력바이트읽기(0x60);
        if ((status_värde & 0x20) != 0) return -1;
        if (värde == 0xe0 || värde == 0xe1) { tillägg_värde = true; return -1; }
        if (tillägg_värde) { tillägg_värde = false; return -1; }
        if (värde == 42 || värde == 170) { skifta_VÄNSTER = värde == 42; return -1; }
        if (värde == 54 || värde == 182) { skifta_HÖGER = värde == 54; return -1; }
        if (värde >= standardvärde.length()) return -1;
        int 문자 = (skifta_VÄNSTER || skifta_HÖGER) ? skifta_värde.charAt(värde) : standardvärde.charAt(värde);
        return 문자 == 0 ? -1 : 문자;
    }
}
