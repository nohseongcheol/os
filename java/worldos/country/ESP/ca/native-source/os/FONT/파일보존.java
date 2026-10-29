// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_VALOR format_VALOR. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] arxiu_taula = new int[1024];
    static int 바이트해시(int VALOR, int dades) { return (VALOR ^ dades) * 16777619; }
    static void eliminar_dades() {
        for (int INDEX = 0; INDEX < 512; INDEX++) Emmagatzematge_dispositiu_connexió.secció_dades[INDEX] = 0;
    }
    static int 표정수(int Posició) {
        return arxiu_taula[Posició] | arxiu_taula[Posició + 1] << 8 | arxiu_taula[Posició + 2] << 16 | arxiu_taula[Posició + 3] << 24;
    }
    static void 표정수쓰기(int Posició, int VALOR) {
        for (int INDEX = 0; INDEX < 4; INDEX++) arxiu_taula[Posició + INDEX] = (VALOR >>> (INDEX * 8)) & 255;
    }
    static boolean xec_taula() {
        for (int Fitxer = 0; Fitxer < 8; Fitxer++) {
            int durada_VALOR = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) Memòria_sistema_d_arxius.Nom[칸] = arxiu_taula[Fitxer * 72 + 칸];
            while (durada_VALOR < 64 && Memòria_sistema_d_arxius.Nom[durada_VALOR] != 0) durada_VALOR++;
            if (durada_VALOR == 0) continue;
            if (!Memòria_sistema_d_arxius.xec_nom(Memòria_sistema_d_arxius.Nom, durada_VALOR)
                || 표정수(Fitxer * 72 + 64) < 0 || 표정수(Fitxer * 72 + 64) > 16384) return false;
            for (int frontal_VALOR = 0; frontal_VALOR < Fitxer; frontal_VALOR++) {
                boolean 같음 = arxiu_taula[frontal_VALOR * 72 + durada_VALOR] == 0;
                for (int 칸 = 0; 칸 < durada_VALOR; 칸++) if (arxiu_taula[frontal_VALOR * 72 + 칸] != Memòria_sistema_d_arxius.Nom[칸]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int Inici_secció = 1 + 보존본 * 259;
        if (Emmagatzematge_dispositiu_connexió.Lectura(Inici_secció) < 0 || Emmagatzematge_dispositiu_connexió.정수읽기(0) != 0x4a4b534e) return -1;
        int 세대 = Emmagatzematge_dispositiu_connexió.정수읽기(4), suma_de_comprovació = Emmagatzematge_dispositiu_connexió.정수읽기(8);
        if (세대 < 1 || Emmagatzematge_dispositiu_connexió.정수읽기(12) != (세대 ^ suma_de_comprovació ^ 0x4a4b534e)) return -1;
        int hash_arxiu = 0x811c9dc5;
        for (int secció_VALOR = 0; secció_VALOR < 258; secció_VALOR++) {
            if (Emmagatzematge_dispositiu_connexió.Lectura(Inici_secció + 1 + secció_VALOR) < 0) return -1;
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int VALOR = Emmagatzematge_dispositiu_connexió.secció_dades[칸];
                hash_arxiu = 바이트해시(hash_arxiu, VALOR);
                if (secció_VALOR < 2) arxiu_taula[secció_VALOR * 512 + 칸] = VALOR;
            }
        }
        return hash_arxiu == suma_de_comprovació && xec_taula() ? 세대 : -1;
    }
    static int Càrrega(int 보존본) {
        int Inici_secció = 1 + 보존본 * 259;
        for (int secció_VALOR = 0; secció_VALOR < 2; secció_VALOR++) {
            if (Emmagatzematge_dispositiu_connexió.Lectura(Inici_secció + 1 + secció_VALOR) < 0) return -5;
            for (int 칸 = 0; 칸 < 512; 칸++) arxiu_taula[secció_VALOR * 512 + 칸] = Emmagatzematge_dispositiu_connexió.secció_dades[칸];
        }
        for (int Fitxer = 0; Fitxer < 8; Fitxer++) {
            for (int 칸 = 0; 칸 < 64; 칸++) Memòria_sistema_d_arxius.이름들[Fitxer * 64 + 칸] = arxiu_taula[Fitxer * 72 + 칸];
            Memòria_sistema_d_arxius.canviar_la_mida_Llista[Fitxer] = arxiu_taula[Fitxer * 72] == 0 ? 0 : 표정수(Fitxer * 72 + 64);
            Memòria_sistema_d_arxius.허가들[Fitxer] = 표정수(Fitxer * 72 + 68) & 511;
            for (int secció_VALOR = 0; secció_VALOR < 32; secció_VALOR++) {
                if (Emmagatzematge_dispositiu_connexió.Lectura(Inici_secció + 3 + Fitxer * 32 + secció_VALOR) < 0) return -5;
                int Adreça = dispositiu_VALOR.arxiu_Memòria() + Fitxer * 16384 + secció_VALOR * 512;
                for (int 칸 = 0; 칸 < 512; 칸++) dispositiu_VALOR.escriure_Memòria(Adreça + 칸, Emmagatzematge_dispositiu_connexió.secció_dades[칸]);
            }
        }
        return 0;
    }
    static void Prepara() {
        if (Emmagatzematge_dispositiu_connexió.Lectura(0) < 0 || Emmagatzematge_dispositiu_connexió.정수읽기(0) != 0x54534b4a
            || Emmagatzematge_dispositiu_connexió.정수읽기(4) != 0x3145524f || Emmagatzematge_dispositiu_connexió.정수읽기(8) != 2048
            || Emmagatzematge_dispositiu_connexió.정수읽기(12) != 0x3153464a) {
            SMS_Terminal.Escriptura("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        Emmagatzematge_dispositiu_connexió.tecnologies_de_la_informació_Actiu_9e72441a = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Terminal.Escriptura("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (Càrrega(현재보존본) < 0) {
            SMS_Terminal.Escriptura("STORE read failed; halted to preserve files\n"); dispositiu_VALOR.정지();
        }
        SMS_Terminal.Escriptura("STORE restored generation "); SMS_Terminal.수쓰기(세대번호); SMS_Terminal.문자(10);
    }
    static int sincronitzar() {
        if (!Emmagatzematge_dispositiu_connexió.tecnologies_de_la_informació_Actiu_9e72441a) return -19;
        if (세대번호 == 2147483647) return -75;
        int Següent_element = 현재보존본 == 0 ? 1 : 0, Inici_secció = 1 + Següent_element * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 dispositiu_VALOR 캐시를 비운다.
        eliminar_dades();
        if (Emmagatzematge_dispositiu_connexió.Escriptura(Inici_secció) < 0 || Emmagatzematge_dispositiu_connexió.밀어쓰기() < 0) return -5;
        for (int 칸 = 0; 칸 < 1024; 칸++) arxiu_taula[칸] = 0;
        for (int Fitxer = 0; Fitxer < 8; Fitxer++) if (Memòria_sistema_d_arxius.이름들[Fitxer * 64] != 0) {
            for (int 칸 = 0; 칸 < 64; 칸++) arxiu_taula[Fitxer * 72 + 칸] = Memòria_sistema_d_arxius.이름들[Fitxer * 64 + 칸];
            표정수쓰기(Fitxer * 72 + 64, Memòria_sistema_d_arxius.canviar_la_mida_Llista[Fitxer]);
            표정수쓰기(Fitxer * 72 + 68, Memòria_sistema_d_arxius.허가들[Fitxer]);
        }
        int hash_arxiu = 0x811c9dc5;
        for (int secció_VALOR = 0; secció_VALOR < 258; secció_VALOR++) {
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int VALOR = 0;
                if (secció_VALOR < 2) VALOR = arxiu_taula[secció_VALOR * 512 + 칸];
                else {
                    int Fitxer = (secció_VALOR - 2) / 32, Posició = (secció_VALOR - 2) % 32 * 512 + 칸;
                    if (arxiu_taula[Fitxer * 72] != 0 && Posició < Memòria_sistema_d_arxius.canviar_la_mida_Llista[Fitxer])
                        VALOR = dispositiu_VALOR.tancar_Memòria(dispositiu_VALOR.arxiu_Memòria() + Fitxer * 16384 + Posició);
                }
                Emmagatzematge_dispositiu_connexió.secció_dades[칸] = VALOR; hash_arxiu = 바이트해시(hash_arxiu, VALOR);
            }
            if (Emmagatzematge_dispositiu_connexió.Escriptura(Inici_secció + 1 + secció_VALOR) < 0) return -5;
        }
        if (Emmagatzematge_dispositiu_connexió.밀어쓰기() < 0) return -5;
        eliminar_dades(); Emmagatzematge_dispositiu_connexió.정수쓰기(0, 0x4a4b534e);
        Emmagatzematge_dispositiu_connexió.정수쓰기(4, 세대번호 + 1); Emmagatzematge_dispositiu_connexió.정수쓰기(8, hash_arxiu);
        Emmagatzematge_dispositiu_connexió.정수쓰기(12, (세대번호 + 1) ^ hash_arxiu ^ 0x4a4b534e);
        if (Emmagatzematge_dispositiu_connexió.Escriptura(Inici_secció) < 0 || Emmagatzematge_dispositiu_connexió.밀어쓰기() < 0) return -5;
        현재보존본 = Següent_element; 세대번호++;
        return 0;
    }
}
