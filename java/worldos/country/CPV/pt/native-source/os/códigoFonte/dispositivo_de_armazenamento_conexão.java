// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 seção_VALOR. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class dispositivo_de_armazenamento_conexão {
    static boolean TI_Ativo_9e72441a = false;
    static int[] seção_dados = new int[512];
    static void 잠깐기다리기() {
        for (int ÍNDICE = 0; ÍNDICE < 4; ÍNDICE++) celular_VALOR.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int iniciar = celular_VALOR.밀리초();
        while (celular_VALOR.밀리초() - iniciar < 500) {
            int Estado_VALOR = celular_VALOR.입출력바이트읽기(0x1f7);
            if (Estado_VALOR == 0 || Estado_VALOR == 255) return -19;
            if ((Estado_VALOR & 128) == 0) {
                if ((Estado_VALOR & 33) != 0) return -5;
                if (!자료필요 || (Estado_VALOR & 8) != 0) return 0;
            }
            celular_VALOR.잠시양보();
        }
        return -110;
    }
    static int solicitação(int seção_VALOR, int comando) {
        if (seção_VALOR < 0 || seção_VALOR >= 2048) return -22;
        celular_VALOR.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ uso_VALOR 안 함
        celular_VALOR.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int resultado = 준비기다리기(false);
        if (resultado < 0) return resultado;
        celular_VALOR.입출력바이트쓰기(0x1f2, 1);
        celular_VALOR.입출력바이트쓰기(0x1f3, seção_VALOR & 255);
        celular_VALOR.입출력바이트쓰기(0x1f4, (seção_VALOR >>> 8) & 255);
        celular_VALOR.입출력바이트쓰기(0x1f5, 0);
        celular_VALOR.입출력바이트쓰기(0x1f7, comando); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Leitura(int seção_VALOR) {
        int resultado = solicitação(seção_VALOR, 0x20);
        if (resultado < 0) return resultado;
        for (int ÍNDICE = 0; ÍNDICE < 256; ÍNDICE++) {
            int VALOR = celular_VALOR.입출력짧은수읽기(0x1f0);
            seção_dados[ÍNDICE * 2] = VALOR & 255; seção_dados[ÍNDICE * 2 + 1] = VALOR >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Escrita(int seção_VALOR) {
        if (!TI_Ativo_9e72441a || seção_VALOR < 1 || seção_VALOR > 518) return -19;
        int resultado = solicitação(seção_VALOR, 0x30);
        if (resultado < 0) return resultado;
        for (int ÍNDICE = 0; ÍNDICE < 256; ÍNDICE++)
            celular_VALOR.입출력짧은수쓰기(0x1f0, seção_dados[ÍNDICE * 2] | seção_dados[ÍNDICE * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int liberar_saída() {
        if (!TI_Ativo_9e72441a) return -19;
        celular_VALOR.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int analisar_inteiro(int posição) {
        return seção_dados[posição] | seção_dados[posição + 1] << 8 | seção_dados[posição + 2] << 16 | seção_dados[posição + 3] << 24;
    }
    static void gravar_inteiro_VALOR(int posição, int VALOR) {
        for (int ÍNDICE = 0; ÍNDICE < 4; ÍNDICE++) seção_dados[posição + ÍNDICE] = (VALOR >>> (ÍNDICE * 8)) & 255;
    }
}
