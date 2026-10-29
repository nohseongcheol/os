// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 번역 집합 1 폴링 입력. ajutuu_aneekuushitüjülia 미국식 자판, Shift, Backspace, Enter. */
public final class ajüttiaapala {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean e_irukuu_ajutuu = false;
    static String ajutuu_aneekuushitüjülia = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int 읽기() {
        int jamakua_iparülein_ajutuu = serulaalü_ajutuu.입출력바이트읽기(0x64);
        if ((jamakua_iparülein_ajutuu & 1) == 0) return -1;
        int ajutuu = serulaalü_ajutuu.입출력바이트읽기(0x60);
        if ((jamakua_iparülein_ajutuu & 0x20) != 0) return -1;
        if (ajutuu == 0xe0 || ajutuu == 0xe1) { e_irukuu_ajutuu = true; return -1; }
        if (e_irukuu_ajutuu) { e_irukuu_ajutuu = false; return -1; }
        if (ajutuu == 42 || ajutuu == 170) { 왼올림 = ajutuu == 42; return -1; }
        if (ajutuu == 54 || ajutuu == 182) { 오른올림 = ajutuu == 54; return -1; }
        if (ajutuu >= ajutuu_aneekuushitüjülia.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(ajutuu) : ajutuu_aneekuushitüjülia.charAt(ajutuu);
        return 문자 == 0 ? -1 : 문자;
    }
}
