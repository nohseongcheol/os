// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 mover_fonte 집합 1 폴링 entrada_VALOR. valor_padrão 미국식 자판, Shift, Backspace, Enter. */
public final class teclado {
    static boolean deslocar_ESQUERDA = false;
    static boolean deslocar_DIREITA = false;
    static boolean extensão_VALOR = false;
    static String valor_padrão = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String deslocar_VALOR = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Leitura() {
        int Estado_VALOR = celular_VALOR.입출력바이트읽기(0x64);
        if ((Estado_VALOR & 1) == 0) return -1;
        int VALOR = celular_VALOR.입출력바이트읽기(0x60);
        if ((Estado_VALOR & 0x20) != 0) return -1;
        if (VALOR == 0xe0 || VALOR == 0xe1) { extensão_VALOR = true; return -1; }
        if (extensão_VALOR) { extensão_VALOR = false; return -1; }
        if (VALOR == 42 || VALOR == 170) { deslocar_ESQUERDA = VALOR == 42; return -1; }
        if (VALOR == 54 || VALOR == 182) { deslocar_DIREITA = VALOR == 54; return -1; }
        if (VALOR >= valor_padrão.length()) return -1;
        int 문자 = (deslocar_ESQUERDA || deslocar_DIREITA) ? deslocar_VALOR.charAt(VALOR) : valor_padrão.charAt(VALOR);
        return 문자 == 0 ? -1 : 문자;
    }
}
