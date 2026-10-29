// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 OVERSETT_kilde 집합 1 폴링 inndata_VERDI. standardverdi 미국식 자판, Shift, Backspace, Enter. */
public final class tastatur {
    static boolean flytte_VENSTRE = false;
    static boolean flytte_HØYRE = false;
    static boolean filtype_VERDI = false;
    static String standardverdi = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String flytte_VERDI = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Les() {
        int status_VERDI = enhet_VERDI.입출력바이트읽기(0x64);
        if ((status_VERDI & 1) == 0) return -1;
        int VERDI = enhet_VERDI.입출력바이트읽기(0x60);
        if ((status_VERDI & 0x20) != 0) return -1;
        if (VERDI == 0xe0 || VERDI == 0xe1) { filtype_VERDI = true; return -1; }
        if (filtype_VERDI) { filtype_VERDI = false; return -1; }
        if (VERDI == 42 || VERDI == 170) { flytte_VENSTRE = VERDI == 42; return -1; }
        if (VERDI == 54 || VERDI == 182) { flytte_HØYRE = VERDI == 54; return -1; }
        if (VERDI >= standardverdi.length()) return -1;
        int 문자 = (flytte_VENSTRE || flytte_HØYRE) ? flytte_VERDI.charAt(VERDI) : standardverdi.charAt(VERDI);
        return 문자 == 0 ? -1 : 문자;
    }
}
