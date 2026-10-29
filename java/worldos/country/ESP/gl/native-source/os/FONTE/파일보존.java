// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_VALOR formato_VALOR. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] Ficheiro_táboa = new int[1024];
    static int 바이트해시(int VALOR, int datos) { return (VALOR ^ datos) * 16777619; }
    static void desmarcar_datos() {
        for (int ÍNDICE = 0; ÍNDICE < 512; ÍNDICE++) Almacenamento_dispositivo_conexión.sección_datos[ÍNDICE] = 0;
    }
    static int táboa_número_enteiro(int Posición) {
        return Ficheiro_táboa[Posición] | Ficheiro_táboa[Posición + 1] << 8 | Ficheiro_táboa[Posición + 2] << 16 | Ficheiro_táboa[Posición + 3] << 24;
    }
    static void escribir_táboa_número_enteiro(int Posición, int VALOR) {
        for (int ÍNDICE = 0; ÍNDICE < 4; ÍNDICE++) Ficheiro_táboa[Posición + ÍNDICE] = (VALOR >>> (ÍNDICE * 8)) & 255;
    }
    static boolean cheque_táboa() {
        for (int Ficheiro = 0; Ficheiro < 8; Ficheiro++) {
            int duración_VALOR = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) Memoria_sistema_de_ficheiros.Nome[칸] = Ficheiro_táboa[Ficheiro * 72 + 칸];
            while (duración_VALOR < 64 && Memoria_sistema_de_ficheiros.Nome[duración_VALOR] != 0) duración_VALOR++;
            if (duración_VALOR == 0) continue;
            if (!Memoria_sistema_de_ficheiros.cheque_nome(Memoria_sistema_de_ficheiros.Nome, duración_VALOR)
                || táboa_número_enteiro(Ficheiro * 72 + 64) < 0 || táboa_número_enteiro(Ficheiro * 72 + 64) > 16384) return false;
            for (int frontal_VALOR = 0; frontal_VALOR < Ficheiro; frontal_VALOR++) {
                boolean 같음 = Ficheiro_táboa[frontal_VALOR * 72 + duración_VALOR] == 0;
                for (int 칸 = 0; 칸 < duración_VALOR; 칸++) if (Ficheiro_táboa[frontal_VALOR * 72 + 칸] != Memoria_sistema_de_ficheiros.Nome[칸]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int START_sección = 1 + 보존본 * 259;
        if (Almacenamento_dispositivo_conexión.Lectura(START_sección) < 0 || Almacenamento_dispositivo_conexión.analizar_número_enteiro(0) != 0x4a4b534e) return -1;
        int 세대 = Almacenamento_dispositivo_conexión.analizar_número_enteiro(4), suma_de_comprobación = Almacenamento_dispositivo_conexión.analizar_número_enteiro(8);
        if (세대 < 1 || Almacenamento_dispositivo_conexión.analizar_número_enteiro(12) != (세대 ^ suma_de_comprobación ^ 0x4a4b534e)) return -1;
        int hash_Ficheiro = 0x811c9dc5;
        for (int sección_VALOR = 0; sección_VALOR < 258; sección_VALOR++) {
            if (Almacenamento_dispositivo_conexión.Lectura(START_sección + 1 + sección_VALOR) < 0) return -1;
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int VALOR = Almacenamento_dispositivo_conexión.sección_datos[칸];
                hash_Ficheiro = 바이트해시(hash_Ficheiro, VALOR);
                if (sección_VALOR < 2) Ficheiro_táboa[sección_VALOR * 512 + 칸] = VALOR;
            }
        }
        return hash_Ficheiro == suma_de_comprobación && cheque_táboa() ? 세대 : -1;
    }
    static int Carga(int 보존본) {
        int START_sección = 1 + 보존본 * 259;
        for (int sección_VALOR = 0; sección_VALOR < 2; sección_VALOR++) {
            if (Almacenamento_dispositivo_conexión.Lectura(START_sección + 1 + sección_VALOR) < 0) return -5;
            for (int 칸 = 0; 칸 < 512; 칸++) Ficheiro_táboa[sección_VALOR * 512 + 칸] = Almacenamento_dispositivo_conexión.sección_datos[칸];
        }
        for (int Ficheiro = 0; Ficheiro < 8; Ficheiro++) {
            for (int 칸 = 0; 칸 < 64; 칸++) Memoria_sistema_de_ficheiros.이름들[Ficheiro * 64 + 칸] = Ficheiro_táboa[Ficheiro * 72 + 칸];
            Memoria_sistema_de_ficheiros.크기들[Ficheiro] = Ficheiro_táboa[Ficheiro * 72] == 0 ? 0 : táboa_número_enteiro(Ficheiro * 72 + 64);
            Memoria_sistema_de_ficheiros.허가들[Ficheiro] = táboa_número_enteiro(Ficheiro * 72 + 68) & 511;
            for (int sección_VALOR = 0; sección_VALOR < 32; sección_VALOR++) {
                if (Almacenamento_dispositivo_conexión.Lectura(START_sección + 3 + Ficheiro * 32 + sección_VALOR) < 0) return -5;
                int ENDEREZO = dispositivo_VALOR.Ficheiro_Memoria() + Ficheiro * 16384 + sección_VALOR * 512;
                for (int 칸 = 0; 칸 < 512; 칸++) dispositivo_VALOR.escribir_Memoria(ENDEREZO + 칸, Almacenamento_dispositivo_conexión.sección_datos[칸]);
            }
        }
        return 0;
    }
    static void 준비() {
        if (Almacenamento_dispositivo_conexión.Lectura(0) < 0 || Almacenamento_dispositivo_conexión.analizar_número_enteiro(0) != 0x54534b4a
            || Almacenamento_dispositivo_conexión.analizar_número_enteiro(4) != 0x3145524f || Almacenamento_dispositivo_conexión.analizar_número_enteiro(8) != 2048
            || Almacenamento_dispositivo_conexión.analizar_número_enteiro(12) != 0x3153464a) {
            SMS_Terminal.Escritura("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        Almacenamento_dispositivo_conexión.Tecnoloxía_da_información_TI_Activo_9e72441a = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Terminal.Escritura("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (Carga(현재보존본) < 0) {
            SMS_Terminal.Escritura("STORE read failed; halted to preserve files\n"); dispositivo_VALOR.정지();
        }
        SMS_Terminal.Escritura("STORE restored generation "); SMS_Terminal.수쓰기(세대번호); SMS_Terminal.문자(10);
    }
    static int sinc() {
        if (!Almacenamento_dispositivo_conexión.Tecnoloxía_da_información_TI_Activo_9e72441a) return -19;
        if (세대번호 == 2147483647) return -75;
        int Seguinte_elemento = 현재보존본 == 0 ? 1 : 0, START_sección = 1 + Seguinte_elemento * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 dispositivo_VALOR 캐시를 비운다.
        desmarcar_datos();
        if (Almacenamento_dispositivo_conexión.Escritura(START_sección) < 0 || Almacenamento_dispositivo_conexión.밀어쓰기() < 0) return -5;
        for (int 칸 = 0; 칸 < 1024; 칸++) Ficheiro_táboa[칸] = 0;
        for (int Ficheiro = 0; Ficheiro < 8; Ficheiro++) if (Memoria_sistema_de_ficheiros.이름들[Ficheiro * 64] != 0) {
            for (int 칸 = 0; 칸 < 64; 칸++) Ficheiro_táboa[Ficheiro * 72 + 칸] = Memoria_sistema_de_ficheiros.이름들[Ficheiro * 64 + 칸];
            escribir_táboa_número_enteiro(Ficheiro * 72 + 64, Memoria_sistema_de_ficheiros.크기들[Ficheiro]);
            escribir_táboa_número_enteiro(Ficheiro * 72 + 68, Memoria_sistema_de_ficheiros.허가들[Ficheiro]);
        }
        int hash_Ficheiro = 0x811c9dc5;
        for (int sección_VALOR = 0; sección_VALOR < 258; sección_VALOR++) {
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int VALOR = 0;
                if (sección_VALOR < 2) VALOR = Ficheiro_táboa[sección_VALOR * 512 + 칸];
                else {
                    int Ficheiro = (sección_VALOR - 2) / 32, Posición = (sección_VALOR - 2) % 32 * 512 + 칸;
                    if (Ficheiro_táboa[Ficheiro * 72] != 0 && Posición < Memoria_sistema_de_ficheiros.크기들[Ficheiro])
                        VALOR = dispositivo_VALOR.기억읽기(dispositivo_VALOR.Ficheiro_Memoria() + Ficheiro * 16384 + Posición);
                }
                Almacenamento_dispositivo_conexión.sección_datos[칸] = VALOR; hash_Ficheiro = 바이트해시(hash_Ficheiro, VALOR);
            }
            if (Almacenamento_dispositivo_conexión.Escritura(START_sección + 1 + sección_VALOR) < 0) return -5;
        }
        if (Almacenamento_dispositivo_conexión.밀어쓰기() < 0) return -5;
        desmarcar_datos(); Almacenamento_dispositivo_conexión.escribir_número_enteiro_VALOR(0, 0x4a4b534e);
        Almacenamento_dispositivo_conexión.escribir_número_enteiro_VALOR(4, 세대번호 + 1); Almacenamento_dispositivo_conexión.escribir_número_enteiro_VALOR(8, hash_Ficheiro);
        Almacenamento_dispositivo_conexión.escribir_número_enteiro_VALOR(12, (세대번호 + 1) ^ hash_Ficheiro ^ 0x4a4b534e);
        if (Almacenamento_dispositivo_conexión.Escritura(START_sección) < 0 || Almacenamento_dispositivo_conexión.밀어쓰기() < 0) return -5;
        현재보존본 = Seguinte_elemento; 세대번호++;
        return 0;
    }
}
