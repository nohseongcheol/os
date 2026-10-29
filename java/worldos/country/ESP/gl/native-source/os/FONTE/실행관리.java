// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Lectura 전용 executar_comando 묶음의 ELF32 validar, Argumentos Adiante_VALOR, 한 번에 한 usuario Proceso_VALOR executar_comando. */
public final class 실행관리 {
    static final int START_usuario_apl = 0x04000000;
    static final int usuario_finalizar = 0x04400000;
    static final int IMAXE_finalizar_ENDEREZO = 0x04200000;
    static final int argumento_START = 0x04300000;
    static int argumento_CONTAR = 0;
    static int[] argumento_ENDEREZO = new int[16];

    static boolean clip(int ENDEREZO, int duración_VALOR) {
        return ENDEREZO >= START_usuario_apl && ENDEREZO < usuario_finalizar && duración_VALOR >= 0 && duración_VALOR <= usuario_finalizar - ENDEREZO;
    }

    static int 수(int ENDEREZO) { return 기억공간.analizar_número_enteiro(ENDEREZO); }
    static int 짧은수(int ENDEREZO) { return dispositivo_VALOR.기억읽기(ENDEREZO) | dispositivo_VALOR.기억읽기(ENDEREZO + 1) << 8; }
    static void 수쓰기(int ENDEREZO, int VALOR) {
        for (int ÍNDICE = 0; ÍNDICE < 4; ÍNDICE++) dispositivo_VALOR.escribir_Memoria(ENDEREZO + ÍNDICE, VALOR >>> (ÍNDICE * 8));
    }

    static int Grupo_CONTAR() {
        int ENDEREZO = dispositivo_VALOR.실행묶음();
        int Tamaño = dispositivo_VALOR.실행묶음크기();
        if (Tamaño < 8 || 수(ENDEREZO) != 0x50414b4a) return 0;
        int elemento_CONTAR = 수(ENDEREZO + 4);
        return elemento_CONTAR >= 0 && elemento_CONTAR <= 32 && elemento_CONTAR <= (Tamaño - 8) / 24 ? elemento_CONTAR : 0;
    }

    static void introdución_Lista() {
        for (int ÍNDICE = 0; ÍNDICE < Grupo_CONTAR(); ÍNDICE++) {
            int introdución_VALOR = dispositivo_VALOR.실행묶음() + 8 + ÍNDICE * 24;
            for (int carácter_VALOR = 0; carácter_VALOR < 16 && dispositivo_VALOR.기억읽기(introdución_VALOR + carácter_VALOR) != 0; carácter_VALOR++)
                SMS_Terminal.문자(dispositivo_VALOR.기억읽기(introdución_VALOR + carácter_VALOR));
            SMS_Terminal.Escritura("\n");
        }
    }

    static int Busca_introdución(int[] 입력, int Executar_2, int duración_VALOR) {
        if (duración_VALOR <= 0 || duración_VALOR >= 16) return 0;
        for (int ÍNDICE = 0; ÍNDICE < Grupo_CONTAR(); ÍNDICE++) {
            int introdución_VALOR = dispositivo_VALOR.실행묶음() + 8 + ÍNDICE * 24;
            boolean 같음 = dispositivo_VALOR.기억읽기(introdución_VALOR + duración_VALOR) == 0;
            for (int carácter_VALOR = 0; carácter_VALOR < duración_VALOR; carácter_VALOR++)
                if (입력[Executar_2 + carácter_VALOR] != dispositivo_VALOR.기억읽기(introdución_VALOR + carácter_VALOR)) 같음 = false;
            if (같음) return introdución_VALOR;
        }
        return 0;
    }

    static int validar(int Ficheiro, int duración_VALOR) {
        if (duración_VALOR < 52 || 수(Ficheiro) != 0x464c457f || dispositivo_VALOR.기억읽기(Ficheiro + 4) != 1
            || dispositivo_VALOR.기억읽기(Ficheiro + 5) != 1 || dispositivo_VALOR.기억읽기(Ficheiro + 6) != 1
            || 짧은수(Ficheiro + 16) != 2 || 짧은수(Ficheiro + 18) != 3 || 수(Ficheiro + 20) != 1
            || 짧은수(Ficheiro + 40) != 52 || 짧은수(Ficheiro + 42) != 32) return -8;
        int introdución_p_VALOR = 수(Ficheiro + 24);
        int táboa_cargo = 수(Ficheiro + 28);
        int elemento_CONTAR = 짧은수(Ficheiro + 44);
        if (elemento_CONTAR == 0 || elemento_CONTAR > 16 || táboa_cargo < 52 || táboa_cargo > duración_VALOR - elemento_CONTAR * 32) return -8;
        boolean 실행가능 = false;
        for (int ÍNDICE = 0; ÍNDICE < elemento_CONTAR; ÍNDICE++) {
            int Busca_táboa = Ficheiro + táboa_cargo + ÍNDICE * 32;
            int 종류 = 수(Busca_táboa);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Conectar/analizador_48ee4b1b 미지원
            if (종류 != 1) continue;
            int Posición = 수(Busca_táboa + 4), ENDEREZO = 수(Busca_táboa + 8), 파일크기 = 수(Busca_táboa + 16), 기억크기 = 수(Busca_táboa + 20);
            int aliñar_VALOR = 수(Busca_táboa + 28);
            if (ENDEREZO < START_usuario_apl || ENDEREZO >= IMAXE_finalizar_ENDEREZO || 기억크기 < 0 || 기억크기 > IMAXE_finalizar_ENDEREZO - ENDEREZO
                || 파일크기 < 0 || 파일크기 > 기억크기 || Posición < 0 || (파일크기 > 0 && Posición > duración_VALOR - 파일크기)
                || (aliñar_VALOR != 0 && (aliñar_VALOR < 0 || (aliñar_VALOR & (aliñar_VALOR - 1)) != 0
                    || ((ENDEREZO - Posición) & (aliñar_VALOR - 1)) != 0))) return -8;
            for (int frontal_VALOR = 0; frontal_VALOR < ÍNDICE; frontal_VALOR++) {
                int 이전 = Ficheiro + táboa_cargo + frontal_VALOR * 32;
                if (수(이전) == 1 && 기억크기 > 0 && 수(이전 + 20) > 0
                    && ENDEREZO < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < ENDEREZO + 기억크기) return -8;
            }
            if ((수(Busca_táboa + 24) & 1) != 0 && introdución_p_VALOR >= ENDEREZO && introdución_p_VALOR - ENDEREZO < 파일크기) 실행가능 = true;
        }
        return 실행가능 ? introdución_p_VALOR : -8;
    }

    static int executar_comando(int[] 입력, int Executar_2, int duración_VALOR) {
        while (Executar_2 < duración_VALOR && 입력[Executar_2] == ' ') Executar_2++;
        int 끝 = Executar_2;
        while (끝 < duración_VALOR && 입력[끝] != ' ') 끝++;
        int introdución_VALOR = Busca_introdución(입력, Executar_2, 끝 - Executar_2);
        if (introdución_VALOR == 0) return -2;
        int Posición = 수(introdución_VALOR + 16), Tamaño = 수(introdución_VALOR + 20);
        if (Posición < 8 + Grupo_CONTAR() * 24 || Tamaño < 52 || Posición > dispositivo_VALOR.실행묶음크기() - Tamaño) return -8;
        int Ficheiro = dispositivo_VALOR.실행묶음() + Posición;
        int introdución_p_VALOR = validar(Ficheiro, Tamaño);
        if (introdución_p_VALOR < 0) return introdución_p_VALOR;
        dispositivo_VALOR.usuario_desmarcar_Contido();
        int táboa_cargo = 수(Ficheiro + 28), elemento_CONTAR = 짧은수(Ficheiro + 44);
        for (int ÍNDICE = 0; ÍNDICE < elemento_CONTAR; ÍNDICE++) {
            int Busca_táboa = Ficheiro + táboa_cargo + ÍNDICE * 32;
            if (수(Busca_táboa) != 1) continue;
            int 원본 = Ficheiro + 수(Busca_táboa + 4), destino_VALOR = 수(Busca_táboa + 8), 파일크기 = 수(Busca_táboa + 16);
            for (int byte_VALOR = 0; byte_VALOR < 파일크기; byte_VALOR++) dispositivo_VALOR.escribir_Memoria(destino_VALOR + byte_VALOR, dispositivo_VALOR.기억읽기(원본 + byte_VALOR));
        }
        argumento_CONTAR = 0;
        int Store_VALOR = argumento_START;
        while (끝 < duración_VALOR) {
            while (끝 < duración_VALOR && 입력[끝] == ' ') 끝++;
            if (끝 == duración_VALOR) break;
            if (argumento_CONTAR == argumento_ENDEREZO.length) return -22;
            Executar_2 = 끝;
            while (끝 < duración_VALOR && 입력[끝] != ' ') 끝++;
            argumento_ENDEREZO[argumento_CONTAR++] = Store_VALOR;
            수쓰기(Store_VALOR, 끝 - Executar_2);
            for (int carácter_VALOR = Executar_2; carácter_VALOR < 끝; carácter_VALOR++) 수쓰기(Store_VALOR + 4 + (carácter_VALOR - Executar_2) * 4, 입력[carácter_VALOR]);
            Store_VALOR += 4 + (끝 - Executar_2) * 4;
        }
        Rede_Montón.Limpo_Proceso();
        파일서술자관리.START_Proceso();
        int RESULTANTE = dispositivo_VALOR.executar_usuario_apl(introdución_p_VALOR, usuario_finalizar - 16);
        파일서술자관리.Limpo_Proceso();
        Rede_Montón.Limpo_Proceso();
        return RESULTANTE;
    }
}
