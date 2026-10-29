// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 TRADUEIX_font 집합 1 폴링 입력. valor_per_defecte 미국식 자판, Shift, Backspace, Enter. */
public final class teclat {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean extensió_VALOR = false;
    static String valor_per_defecte = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Lectura() {
        int Estat_VALOR = dispositiu_VALOR.입출력바이트읽기(0x64);
        if ((Estat_VALOR & 1) == 0) return -1;
        int VALOR = dispositiu_VALOR.입출력바이트읽기(0x60);
        if ((Estat_VALOR & 0x20) != 0) return -1;
        if (VALOR == 0xe0 || VALOR == 0xe1) { extensió_VALOR = true; return -1; }
        if (extensió_VALOR) { extensió_VALOR = false; return -1; }
        if (VALOR == 42 || VALOR == 170) { 왼올림 = VALOR == 42; return -1; }
        if (VALOR == 54 || VALOR == 182) { 오른올림 = VALOR == 54; return -1; }
        if (VALOR >= valor_per_defecte.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(VALOR) : valor_per_defecte.charAt(VALOR);
        return 문자 == 0 ? -1 : 문자;
    }
}
