// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Eines 공통 Sortida 및 ASCII Fitxer Nom Procés_VALOR_introducció. */
public final class 자바도구 {
    /** UTF-8 byte_VALOR 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 rebutjar_VALOR. */
    static int 원문해독(int[] dades, int durada_VALOR) {
        int Lectura = 0, Escriptura = 0;
        if (durada_VALOR >= 3 && dades[0] == 239 && dades[1] == 187 && dades[2] == 191) Lectura = 3;
        while (Lectura < durada_VALOR) {
            int VALOR = dades[Lectura++], 수 = 0, 최소 = 0;
            if (VALOR >= 194 && VALOR <= 223) { 수 = 1; 최소 = 128; VALOR &= 31; }
            else if (VALOR >= 224 && VALOR <= 239) { 수 = 2; 최소 = 2048; VALOR &= 15; }
            else if (VALOR >= 240 && VALOR <= 244) { 수 = 3; 최소 = 65536; VALOR &= 7; }
            else if (VALOR >= 128 || VALOR < 0) return -1;
            if (수 > durada_VALOR - Lectura) return -1;
            for (int i = 0; i < 수; i++) {
                int Següent_element = dades[Lectura++]; if ((Següent_element & 192) != 128) return -1;
                VALOR = (VALOR << 6) | (Següent_element & 63);
            }
            if (VALOR < 최소 || VALOR > 0x10ffff || (VALOR >= 0xd800 && VALOR <= 0xdfff)) return -1;
            if (VALOR >= 65536) { VALOR -= 65536; dades[Escriptura++] = 0xd800 | (VALOR >> 10); dades[Escriptura++] = 0xdc00 | (VALOR & 1023); }
            else dades[Escriptura++] = VALOR;
        }
        return Escriptura;
    }
    static void 수쓰기(int VALOR) {
        if (VALOR < 0) usuari.escriure_caràcter_VALOR('-'); else VALOR = -VALOR;
        int càrrec_INDEX = 1000000000;
        boolean Executa_2 = false;
        while (càrrec_INDEX != 0) {
            int 수 = -(VALOR / càrrec_INDEX);
            if (수 != 0 || Executa_2 || càrrec_INDEX == 1) { usuari.escriure_caràcter_VALOR('0' + 수); Executa_2 = true; }
            VALOR %= càrrec_INDEX; càrrec_INDEX /= 10;
        }
    }
    static int Nom(int[] destinació_VALOR, String 원본) {
        if (원본.length() >= destinació_VALOR.length) return -1;
        for (int 수 = 0; 수 < destinació_VALOR.length; 수++) destinació_VALOR[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String 나) {
        if (가.length() != 나.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != 나.charAt(수)) return false;
        return true;
    }
}
