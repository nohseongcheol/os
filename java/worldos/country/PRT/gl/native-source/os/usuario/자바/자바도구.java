// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Ferramentas 공통 Saída 및 ASCII Ficheiro Nome Proceso_VALOR_introdución. */
public final class 자바도구 {
    /** UTF-8 byte_VALOR 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 rexeitar_VALOR_e3ecc00b. */
    static int 원문해독(int[] datos, int duración_VALOR) {
        int Lectura = 0, Escritura = 0;
        if (duración_VALOR >= 3 && datos[0] == 239 && datos[1] == 187 && datos[2] == 191) Lectura = 3;
        while (Lectura < duración_VALOR) {
            int VALOR = datos[Lectura++], 수 = 0, 최소 = 0;
            if (VALOR >= 194 && VALOR <= 223) { 수 = 1; 최소 = 128; VALOR &= 31; }
            else if (VALOR >= 224 && VALOR <= 239) { 수 = 2; 최소 = 2048; VALOR &= 15; }
            else if (VALOR >= 240 && VALOR <= 244) { 수 = 3; 최소 = 65536; VALOR &= 7; }
            else if (VALOR >= 128 || VALOR < 0) return -1;
            if (수 > duración_VALOR - Lectura) return -1;
            for (int i = 0; i < 수; i++) {
                int Seguinte_elemento = datos[Lectura++]; if ((Seguinte_elemento & 192) != 128) return -1;
                VALOR = (VALOR << 6) | (Seguinte_elemento & 63);
            }
            if (VALOR < 최소 || VALOR > 0x10ffff || (VALOR >= 0xd800 && VALOR <= 0xdfff)) return -1;
            if (VALOR >= 65536) { VALOR -= 65536; datos[Escritura++] = 0xd800 | (VALOR >> 10); datos[Escritura++] = 0xdc00 | (VALOR & 1023); }
            else datos[Escritura++] = VALOR;
        }
        return Escritura;
    }
    static void 수쓰기(int VALOR) {
        if (VALOR < 0) usuario.escribir_carácter_VALOR('-'); else VALOR = -VALOR;
        int cargo_ÍNDICE = 1000000000;
        boolean Executar_2 = false;
        while (cargo_ÍNDICE != 0) {
            int 수 = -(VALOR / cargo_ÍNDICE);
            if (수 != 0 || Executar_2 || cargo_ÍNDICE == 1) { usuario.escribir_carácter_VALOR('0' + 수); Executar_2 = true; }
            VALOR %= cargo_ÍNDICE; cargo_ÍNDICE /= 10;
        }
    }
    static int Nome(int[] destino_VALOR, String 원본) {
        if (원본.length() >= destino_VALOR.length) return -1;
        for (int 수 = 0; 수 < destino_VALOR.length; 수++) destino_VALOR[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String 나) {
        if (가.length() != 나.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != 나.charAt(수)) return false;
        return true;
    }
}
