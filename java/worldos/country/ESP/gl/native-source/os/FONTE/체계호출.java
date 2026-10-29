// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 usuario punteiro/길이는 acceso_introdución 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int MATRIZ_duración(int ENDEREZO) {
        if (!실행관리.clip(ENDEREZO, 4)) return -14;
        int duración_VALOR = 실행관리.수(ENDEREZO);
        if (duración_VALOR < 0 || duración_VALOR > (실행관리.usuario_finalizar - ENDEREZO - 4) / 4) return -14;
        return duración_VALOR;
    }

    public static int Proceso_VALOR_introdución(int ÍNDICE, int 가, int 나, int 다, int 라, int 마) {
        if (ÍNDICE == 30) return 파일서술자관리.abrir_Ficheiro(가, 나, 다);
        if (ÍNDICE == 31) return 파일서술자관리.파일읽기(가, 나, 다);
        if (ÍNDICE == 32) return 파일서술자관리.escribir_Ficheiro(가, 나, 다);
        if (ÍNDICE == 33) return 파일서술자관리.peche_Ficheiro(가);
        if (ÍNDICE == 34) return 파일서술자관리.buscar_Ficheiro(가, 나, 다);
        if (ÍNDICE == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (ÍNDICE == 36) return 파일서술자관리.서술자복제(가, 나, true, 0);
        if (ÍNDICE == 37) return 파일서술자관리.파일상태읽기(가, 나);
        if (ÍNDICE == 38) return 파일서술자관리.eliminar_Ficheiro_introdución_nome(가);
        if (ÍNDICE == 39) return 파일서술자관리.conxunto_Ficheiro_duración(가, 나);
        if (ÍNDICE == 40) return 파일서술자관리.서술자제어(가, 나, 다);
        if (ÍNDICE == 41) return 파일서술자관리.crear_extremo(가, 나, 다);
        if (ÍNDICE == 42) return 파일서술자관리.ligar_ENDEREZO(가, 나, 다);
        if (ÍNDICE == 43) return 파일서술자관리.자료전문보내기(가, 나, 다, 라, 마);
        if (ÍNDICE == 44) return 파일서술자관리.자료전문받기(가, 나, 다, 라, 마);
        if (ÍNDICE == 45) return 파일서술자관리.통신주소읽기(가, 나, 다);
        if (ÍNDICE == 46) return 파일서술자관리.수신대기정하기(가, 나);
        if (ÍNDICE == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.sinc();
        }
        if (ÍNDICE == 1) {
            int duración_VALOR = MATRIZ_duración(가);
            if (duración_VALOR < 0) return duración_VALOR;
            if (duración_VALOR > 4096) return -90;
            for (int carácter_VALOR = 0; carácter_VALOR < duración_VALOR; carácter_VALOR++) SMS_Terminal.문자(실행관리.수(가 + 4 + carácter_VALOR * 4) & 65535);
            return duración_VALOR;
        }
        if (ÍNDICE == 2) return 실행관리.argumento_CONTAR;
        if (ÍNDICE == 3) return 가 >= 0 && 가 < 실행관리.argumento_CONTAR ? 실행관리.argumento_ENDEREZO[가] : 0;
        if (ÍNDICE == 10) return Rede_Montón.Abrir(가);
        if (ÍNDICE == 11) {
            int duración_VALOR = MATRIZ_duración(라);
            if (duración_VALOR < 0) return duración_VALOR;
            if (마 < 0 || 마 > duración_VALOR || 마 > 1024) return -90;
            for (int Posición = 0; Posición < 마; Posición++) 임시자료[Posición] = 실행관리.수(라 + 4 + Posición * 4) & 255;
            return Rede_Montón.enviar(가, 나, 다, 임시자료, 마);
        }
        if (ÍNDICE == 12) {
            int duración_VALOR = MATRIZ_duración(나);
            if (duración_VALOR < 0) return duración_VALOR;
            if (다 < 0 || 다 > 2000) return -22;
            int RESULTANTE = Rede_Montón.받기(가, 임시자료, duración_VALOR < 1024 ? duración_VALOR : 1024, 다);
            if (RESULTANTE >= 0) for (int Posición = 0; Posición < RESULTANTE; Posición++) 실행관리.수쓰기(나 + 4 + Posición * 4, 임시자료[Posición]);
            return RESULTANTE;
        }
        if (ÍNDICE == 13) return Rede_Montón.Pechar(가);
        if (ÍNDICE == 14) return Rede_Montón.내주소;
        if (ÍNDICE == 15) return Rede_Montón.punto_ENDEREZO(가);
        if (ÍNDICE == 16) return Rede_Montón.punto_número_do_porto(가);
        if (ÍNDICE == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Terminal.문자(가); return 1;
        }
        if (ÍNDICE == 20 || ÍNDICE == 21) {
            int 이름크기 = MATRIZ_duración(가), 자료크기 = MATRIZ_duración(나);
            if (이름크기 < 0 || 자료크기 < 0) return -14;
            if (이름크기 < 1 || 이름크기 > 64) return -22;
            int duración_VALOR = 0;
            while (duración_VALOR < 이름크기 && 실행관리.수(가 + 4 + duración_VALOR * 4) != 0) {
                Memoria_sistema_de_ficheiros.Nome[duración_VALOR] = 실행관리.수(가 + 4 + duración_VALOR * 4);
                duración_VALOR++;
            }
            if (!Memoria_sistema_de_ficheiros.cheque_nome(Memoria_sistema_de_ficheiros.Nome, duración_VALOR)) return -22;
            if (ÍNDICE == 20) {
                int Ficheiro = Memoria_sistema_de_ficheiros.Busca_introdución(Memoria_sistema_de_ficheiros.Nome, duración_VALOR);
                if (Ficheiro < 0) return Ficheiro;
                int Tamaño = Memoria_sistema_de_ficheiros.크기들[Ficheiro];
                if (Tamaño > 자료크기) return -90;
                int ENDEREZO = dispositivo_VALOR.Ficheiro_Memoria() + Ficheiro * Memoria_sistema_de_ficheiros.최대크기;
                for (int 수 = 0; 수 < Tamaño; 수++) 실행관리.수쓰기(나 + 4 + 수 * 4, dispositivo_VALOR.기억읽기(ENDEREZO + 수));
                return Tamaño;
            }
            if (다 < 0 || 다 > 자료크기) return -22;
            if (다 > Memoria_sistema_de_ficheiros.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) Memoria_sistema_de_ficheiros.editar_VALOR[수] = 실행관리.수(나 + 4 + 수 * 4) & 255;
            return Memoria_sistema_de_ficheiros.Store_VALOR(Memoria_sistema_de_ficheiros.Nome, duración_VALOR, Memoria_sistema_de_ficheiros.editar_VALOR, 다);
        }
        return -38;
    }
}
