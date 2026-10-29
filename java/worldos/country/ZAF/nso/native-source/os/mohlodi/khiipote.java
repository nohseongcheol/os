// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 Fetolela_mohlodi 집합 1 폴링 입력. setsenywa_sa_tirelwa 미국식 자판, Shift, Backspace, Enter. */
public final class khiipote {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean koketšo_boleng = false;
    static String setsenywa_sa_tirelwa = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Bala() {
        int boemo_boleng = sedirišwa_boleng.입출력바이트읽기(0x64);
        if ((boemo_boleng & 1) == 0) return -1;
        int boleng = sedirišwa_boleng.입출력바이트읽기(0x60);
        if ((boemo_boleng & 0x20) != 0) return -1;
        if (boleng == 0xe0 || boleng == 0xe1) { koketšo_boleng = true; return -1; }
        if (koketšo_boleng) { koketšo_boleng = false; return -1; }
        if (boleng == 42 || boleng == 170) { 왼올림 = boleng == 42; return -1; }
        if (boleng == 54 || boleng == 182) { 오른올림 = boleng == 54; return -1; }
        if (boleng >= setsenywa_sa_tirelwa.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(boleng) : setsenywa_sa_tirelwa.charAt(boleng);
        return 문자 == 0 ? -1 : 문자;
    }
}
