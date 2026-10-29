// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 sección_VALOR. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class Almacenamento_dispositivo_conexión {
    static boolean Tecnoloxía_da_información_TI_Activo_9e72441a = false;
    static int[] sección_datos = new int[512];
    static void 잠깐기다리기() {
        for (int ÍNDICE = 0; ÍNDICE < 4; ÍNDICE++) dispositivo_VALOR.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Executar_2 = dispositivo_VALOR.밀리초();
        while (dispositivo_VALOR.밀리초() - Executar_2 < 500) {
            int Estado_VALOR = dispositivo_VALOR.입출력바이트읽기(0x1f7);
            if (Estado_VALOR == 0 || Estado_VALOR == 255) return -19;
            if ((Estado_VALOR & 128) == 0) {
                if ((Estado_VALOR & 33) != 0) return -5;
                if (!자료필요 || (Estado_VALOR & 8) != 0) return 0;
            }
            dispositivo_VALOR.잠시양보();
        }
        return -110;
    }
    static int solicitude(int sección_VALOR, int Orde) {
        if (sección_VALOR < 0 || sección_VALOR >= 2048) return -22;
        dispositivo_VALOR.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        dispositivo_VALOR.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int RESULTANTE = 준비기다리기(false);
        if (RESULTANTE < 0) return RESULTANTE;
        dispositivo_VALOR.입출력바이트쓰기(0x1f2, 1);
        dispositivo_VALOR.입출력바이트쓰기(0x1f3, sección_VALOR & 255);
        dispositivo_VALOR.입출력바이트쓰기(0x1f4, (sección_VALOR >>> 8) & 255);
        dispositivo_VALOR.입출력바이트쓰기(0x1f5, 0);
        dispositivo_VALOR.입출력바이트쓰기(0x1f7, Orde); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Lectura(int sección_VALOR) {
        int RESULTANTE = solicitude(sección_VALOR, 0x20);
        if (RESULTANTE < 0) return RESULTANTE;
        for (int ÍNDICE = 0; ÍNDICE < 256; ÍNDICE++) {
            int VALOR = dispositivo_VALOR.입출력짧은수읽기(0x1f0);
            sección_datos[ÍNDICE * 2] = VALOR & 255; sección_datos[ÍNDICE * 2 + 1] = VALOR >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Escritura(int sección_VALOR) {
        if (!Tecnoloxía_da_información_TI_Activo_9e72441a || sección_VALOR < 1 || sección_VALOR > 518) return -19;
        int RESULTANTE = solicitude(sección_VALOR, 0x30);
        if (RESULTANTE < 0) return RESULTANTE;
        for (int ÍNDICE = 0; ÍNDICE < 256; ÍNDICE++)
            dispositivo_VALOR.입출력짧은수쓰기(0x1f0, sección_datos[ÍNDICE * 2] | sección_datos[ÍNDICE * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!Tecnoloxía_da_información_TI_Activo_9e72441a) return -19;
        dispositivo_VALOR.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int analizar_número_enteiro(int Posición) {
        return sección_datos[Posición] | sección_datos[Posición + 1] << 8 | sección_datos[Posición + 2] << 16 | sección_datos[Posición + 3] << 24;
    }
    static void escribir_número_enteiro_VALOR(int Posición, int VALOR) {
        for (int ÍNDICE = 0; ÍNDICE < 4; ÍNDICE++) sección_datos[Posición + ÍNDICE] = (VALOR >>> (ÍNDICE * 8)) & 255;
    }
}
