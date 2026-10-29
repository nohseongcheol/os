// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 FORDÍTÁS_forrás 집합 1 폴링 bevitel_ÉRTÉK. alapértelmezett_érték 미국식 자판, Shift, Backspace, Enter. */
public final class billentyűzet {
    static boolean eltol_BAL = false;
    static boolean eltol_jog = false;
    static boolean bővítmény_ÉRTÉK = false;
    static String alapértelmezett_érték = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String eltol_ÉRTÉK = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Olvasás() {
        int Állapot_ÉRTÉK = mobil_ÉRTÉK.입출력바이트읽기(0x64);
        if ((Állapot_ÉRTÉK & 1) == 0) return -1;
        int ÉRTÉK = mobil_ÉRTÉK.입출력바이트읽기(0x60);
        if ((Állapot_ÉRTÉK & 0x20) != 0) return -1;
        if (ÉRTÉK == 0xe0 || ÉRTÉK == 0xe1) { bővítmény_ÉRTÉK = true; return -1; }
        if (bővítmény_ÉRTÉK) { bővítmény_ÉRTÉK = false; return -1; }
        if (ÉRTÉK == 42 || ÉRTÉK == 170) { eltol_BAL = ÉRTÉK == 42; return -1; }
        if (ÉRTÉK == 54 || ÉRTÉK == 182) { eltol_jog = ÉRTÉK == 54; return -1; }
        if (ÉRTÉK >= alapértelmezett_érték.length()) return -1;
        int 문자 = (eltol_BAL || eltol_jog) ? eltol_ÉRTÉK.charAt(ÉRTÉK) : alapértelmezett_érték.charAt(ÉRTÉK);
        return 문자 == 0 ? -1 : 문자;
    }
}
