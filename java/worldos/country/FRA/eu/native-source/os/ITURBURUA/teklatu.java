// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 ITZULI_iturburu 집합 1 폴링 입력. balio_lehenetsi 미국식 자판, Shift, Backspace, Enter. */
public final class teklatu {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean luzapen_balio = false;
    static String balio_lehenetsi = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Irakurri() {
        int Egoera_balio = gailu_balio.입출력바이트읽기(0x64);
        if ((Egoera_balio & 1) == 0) return -1;
        int balio = gailu_balio.입출력바이트읽기(0x60);
        if ((Egoera_balio & 0x20) != 0) return -1;
        if (balio == 0xe0 || balio == 0xe1) { luzapen_balio = true; return -1; }
        if (luzapen_balio) { luzapen_balio = false; return -1; }
        if (balio == 42 || balio == 170) { 왼올림 = balio == 42; return -1; }
        if (balio == 54 || balio == 182) { 오른올림 = balio == 54; return -1; }
        if (balio >= balio_lehenetsi.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(balio) : balio_lehenetsi.charAt(balio);
        return 문자 == 0 ? -1 : 문자;
    }
}
