// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 ferramentas 공통 saídaTexto 및 ASCII ficheiro Nome Processo_VALOR_entrada. */
public final class FerramentasJava {
    /** UTF-8 byte_VALOR 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 rejeitar_VALOR. */
    static int 원문해독(int[] dados, int duração_VALOR) {
        int Leitura = 0, Escrita = 0;
        if (duração_VALOR >= 3 && dados[0] == 239 && dados[1] == 187 && dados[2] == 191) Leitura = 3;
        while (Leitura < duração_VALOR) {
            int VALOR = dados[Leitura++], número = 0, 최소 = 0;
            if (VALOR >= 194 && VALOR <= 223) { número = 1; 최소 = 128; VALOR &= 31; }
            else if (VALOR >= 224 && VALOR <= 239) { número = 2; 최소 = 2048; VALOR &= 15; }
            else if (VALOR >= 240 && VALOR <= 244) { número = 3; 최소 = 65536; VALOR &= 7; }
            else if (VALOR >= 128 || VALOR < 0) return -1;
            if (número > duração_VALOR - Leitura) return -1;
            for (int i = 0; i < número; i++) {
                int Avançar_item = dados[Leitura++]; if ((Avançar_item & 192) != 128) return -1;
                VALOR = (VALOR << 6) | (Avançar_item & 63);
            }
            if (VALOR < 최소 || VALOR > 0x10ffff || (VALOR >= 0xd800 && VALOR <= 0xdfff)) return -1;
            if (VALOR >= 65536) { VALOR -= 65536; dados[Escrita++] = 0xd800 | (VALOR >> 10); dados[Escrita++] = 0xdc00 | (VALOR & 1023); }
            else dados[Escrita++] = VALOR;
        }
        return Escrita;
    }
    static void gravar_número(int VALOR) {
        if (VALOR < 0) espaço_do_utilizador.gravar_caractere_VALOR('-'); else VALOR = -VALOR;
        int cargo_ÍNDICE = 1000000000;
        boolean iniciar = false;
        while (cargo_ÍNDICE != 0) {
            int número = -(VALOR / cargo_ÍNDICE);
            if (número != 0 || iniciar || cargo_ÍNDICE == 1) { espaço_do_utilizador.gravar_caractere_VALOR('0' + número); iniciar = true; }
            VALOR %= cargo_ÍNDICE; cargo_ÍNDICE /= 10;
        }
    }
    static int Nome(int[] destino_VALOR, String 원본) {
        if (원본.length() >= destino_VALOR.length) return -1;
        for (int número = 0; número < destino_VALOR.length; número++) destino_VALOR[número] = número < 원본.length() ? 원본.charAt(número) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String SEGUNDO_operando) {
        if (가.length() != SEGUNDO_operando.length()) return false;
        for (int número = 0; número < 가.length(); número++) if (가.charAt(número) != SEGUNDO_operando.charAt(número)) return false;
        return true;
    }
}
