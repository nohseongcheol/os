// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 TRADUCI_fonte 집합 1 폴링 input_VALORE. valore_predefinito 미국식 자판, Shift, Backspace, Enter. */
public final class tastiera {
    static boolean scorrere_SINISTRA = false;
    static boolean scorrere_DESTRA = false;
    static boolean estensione_VALORE = false;
    static String valore_predefinito = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String scorrere_VALORE = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Lettura() {
        int Stato_VALORE = cellulare_VALORE.입출력바이트읽기(0x64);
        if ((Stato_VALORE & 1) == 0) return -1;
        int VALORE = cellulare_VALORE.입출력바이트읽기(0x60);
        if ((Stato_VALORE & 0x20) != 0) return -1;
        if (VALORE == 0xe0 || VALORE == 0xe1) { estensione_VALORE = true; return -1; }
        if (estensione_VALORE) { estensione_VALORE = false; return -1; }
        if (VALORE == 42 || VALORE == 170) { scorrere_SINISTRA = VALORE == 42; return -1; }
        if (VALORE == 54 || VALORE == 182) { scorrere_DESTRA = VALORE == 54; return -1; }
        if (VALORE >= valore_predefinito.length()) return -1;
        int 문자 = (scorrere_SINISTRA || scorrere_DESTRA) ? scorrere_VALORE.charAt(VALORE) : valore_predefinito.charAt(VALORE);
        return 문자 == 0 ? -1 : 문자;
    }
}
