// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 OVERSÆT_kilde 집합 1 폴링 input_VÆRDI. standardværdi 미국식 자판, Shift, Backspace, Enter. */
public final class tastatur {
    static boolean flytte_VENSTRE = false;
    static boolean flytte_HØJRE = false;
    static boolean udvidelse_VÆRDI = false;
    static String standardværdi = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String flytte_VÆRDI = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Læse() {
        int status_VÆRDI = enhed_VÆRDI.입출력바이트읽기(0x64);
        if ((status_VÆRDI & 1) == 0) return -1;
        int VÆRDI = enhed_VÆRDI.입출력바이트읽기(0x60);
        if ((status_VÆRDI & 0x20) != 0) return -1;
        if (VÆRDI == 0xe0 || VÆRDI == 0xe1) { udvidelse_VÆRDI = true; return -1; }
        if (udvidelse_VÆRDI) { udvidelse_VÆRDI = false; return -1; }
        if (VÆRDI == 42 || VÆRDI == 170) { flytte_VENSTRE = VÆRDI == 42; return -1; }
        if (VÆRDI == 54 || VÆRDI == 182) { flytte_HØJRE = VÆRDI == 54; return -1; }
        if (VÆRDI >= standardværdi.length()) return -1;
        int 문자 = (flytte_VENSTRE || flytte_HØJRE) ? flytte_VÆRDI.charAt(VÆRDI) : standardværdi.charAt(VÆRDI);
        return 문자 == 0 ? -1 : 문자;
    }
}
