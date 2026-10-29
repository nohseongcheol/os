// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 Gusemura_inkomoko 집합 1 폴링 입력. agaciro_gasanzweho 미국식 자판, Shift, Backspace, Enter. */
public final class mwandikisho {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean umugereka_agaciro = false;
    static String agaciro_gasanzweho = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int 읽기() {
        int imimerere_agaciro = igendanwa_agaciro.입출력바이트읽기(0x64);
        if ((imimerere_agaciro & 1) == 0) return -1;
        int agaciro = igendanwa_agaciro.입출력바이트읽기(0x60);
        if ((imimerere_agaciro & 0x20) != 0) return -1;
        if (agaciro == 0xe0 || agaciro == 0xe1) { umugereka_agaciro = true; return -1; }
        if (umugereka_agaciro) { umugereka_agaciro = false; return -1; }
        if (agaciro == 42 || agaciro == 170) { 왼올림 = agaciro == 42; return -1; }
        if (agaciro == 54 || agaciro == 182) { 오른올림 = agaciro == 54; return -1; }
        if (agaciro >= agaciro_gasanzweho.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(agaciro) : agaciro_gasanzweho.charAt(agaciro);
        return 문자 == 0 ? -1 : 문자;
    }
}
