// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_balio formatu_balio. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] fitxategi_taula = new int[1024];
    static int 바이트해시(int balio, int datuak) { return (balio ^ datuak) * 16777619; }
    static void garbitu_datuak() {
        for (int INDIZE = 0; INDIZE < 512; INDIZE++) biltegi_gailu_konexio.sekzio_datuak[INDIZE] = 0;
    }
    static int taula_osoko_zenbaki(int Posizioa) {
        return fitxategi_taula[Posizioa] | fitxategi_taula[Posizioa + 1] << 8 | fitxategi_taula[Posizioa + 2] << 16 | fitxategi_taula[Posizioa + 3] << 24;
    }
    static void idatzi_taula_osoko_zenbaki(int Posizioa, int balio) {
        for (int INDIZE = 0; INDIZE < 4; INDIZE++) fitxategi_taula[Posizioa + INDIZE] = (balio >>> (INDIZE * 8)) & 255;
    }
    static boolean txeke_taula() {
        for (int Fitxategia = 0; Fitxategia < 8; Fitxategia++) {
            int luzera_balio = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) Memoria_fitxategi_sistema.Izena[칸] = fitxategi_taula[Fitxategia * 72 + 칸];
            while (luzera_balio < 64 && Memoria_fitxategi_sistema.Izena[luzera_balio] != 0) luzera_balio++;
            if (luzera_balio == 0) continue;
            if (!Memoria_fitxategi_sistema.txeke_izen(Memoria_fitxategi_sistema.Izena, luzera_balio)
                || taula_osoko_zenbaki(Fitxategia * 72 + 64) < 0 || taula_osoko_zenbaki(Fitxategia * 72 + 64) > 16384) return false;
            for (int aurrekoa_balio = 0; aurrekoa_balio < Fitxategia; aurrekoa_balio++) {
                boolean 같음 = fitxategi_taula[aurrekoa_balio * 72 + luzera_balio] == 0;
                for (int 칸 = 0; 칸 < luzera_balio; 칸++) if (fitxategi_taula[aurrekoa_balio * 72 + 칸] != Memoria_fitxategi_sistema.Izena[칸]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int HASI_sekzio = 1 + 보존본 * 259;
        if (biltegi_gailu_konexio.Irakurri(HASI_sekzio) < 0 || biltegi_gailu_konexio.analizatu_osoko_zenbaki(0) != 0x4a4b534e) return -1;
        int 세대 = biltegi_gailu_konexio.analizatu_osoko_zenbaki(4), kontroleko_batura = biltegi_gailu_konexio.analizatu_osoko_zenbaki(8);
        if (세대 < 1 || biltegi_gailu_konexio.analizatu_osoko_zenbaki(12) != (세대 ^ kontroleko_batura ^ 0x4a4b534e)) return -1;
        int hash_fitxategi = 0x811c9dc5;
        for (int sekzio_balio = 0; sekzio_balio < 258; sekzio_balio++) {
            if (biltegi_gailu_konexio.Irakurri(HASI_sekzio + 1 + sekzio_balio) < 0) return -1;
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int balio = biltegi_gailu_konexio.sekzio_datuak[칸];
                hash_fitxategi = 바이트해시(hash_fitxategi, balio);
                if (sekzio_balio < 2) fitxategi_taula[sekzio_balio * 512 + 칸] = balio;
            }
        }
        return hash_fitxategi == kontroleko_batura && txeke_taula() ? 세대 : -1;
    }
    static int Karga(int 보존본) {
        int HASI_sekzio = 1 + 보존본 * 259;
        for (int sekzio_balio = 0; sekzio_balio < 2; sekzio_balio++) {
            if (biltegi_gailu_konexio.Irakurri(HASI_sekzio + 1 + sekzio_balio) < 0) return -5;
            for (int 칸 = 0; 칸 < 512; 칸++) fitxategi_taula[sekzio_balio * 512 + 칸] = biltegi_gailu_konexio.sekzio_datuak[칸];
        }
        for (int Fitxategia = 0; Fitxategia < 8; Fitxategia++) {
            for (int 칸 = 0; 칸 < 64; 칸++) Memoria_fitxategi_sistema.이름들[Fitxategia * 64 + 칸] = fitxategi_taula[Fitxategia * 72 + 칸];
            Memoria_fitxategi_sistema.크기들[Fitxategia] = fitxategi_taula[Fitxategia * 72] == 0 ? 0 : taula_osoko_zenbaki(Fitxategia * 72 + 64);
            Memoria_fitxategi_sistema.허가들[Fitxategia] = taula_osoko_zenbaki(Fitxategia * 72 + 68) & 511;
            for (int sekzio_balio = 0; sekzio_balio < 32; sekzio_balio++) {
                if (biltegi_gailu_konexio.Irakurri(HASI_sekzio + 3 + Fitxategia * 32 + sekzio_balio) < 0) return -5;
                int helbide = gailu_balio.fitxategi_Memoria() + Fitxategia * 16384 + sekzio_balio * 512;
                for (int 칸 = 0; 칸 < 512; 칸++) gailu_balio.idatzi_Memoria(helbide + 칸, biltegi_gailu_konexio.sekzio_datuak[칸]);
            }
        }
        return 0;
    }
    static void 준비() {
        if (biltegi_gailu_konexio.Irakurri(0) < 0 || biltegi_gailu_konexio.analizatu_osoko_zenbaki(0) != 0x54534b4a
            || biltegi_gailu_konexio.analizatu_osoko_zenbaki(4) != 0x3145524f || biltegi_gailu_konexio.analizatu_osoko_zenbaki(8) != 2048
            || biltegi_gailu_konexio.analizatu_osoko_zenbaki(12) != 0x3153464a) {
            SMS_Terminal.Idatzi("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        biltegi_gailu_konexio.informatika_libre = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Terminal.Idatzi("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (Karga(현재보존본) < 0) {
            SMS_Terminal.Idatzi("STORE read failed; halted to preserve files\n"); gailu_balio.정지();
        }
        SMS_Terminal.Idatzi("STORE restored generation "); SMS_Terminal.수쓰기(세대번호); SMS_Terminal.문자(10);
    }
    static int sinkronizatu() {
        if (!biltegi_gailu_konexio.informatika_libre) return -19;
        if (세대번호 == 2147483647) return -75;
        int Hurrengoa_elementu = 현재보존본 == 0 ? 1 : 0, HASI_sekzio = 1 + Hurrengoa_elementu * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 gailu_balio 캐시를 비운다.
        garbitu_datuak();
        if (biltegi_gailu_konexio.Idatzi(HASI_sekzio) < 0 || biltegi_gailu_konexio.밀어쓰기() < 0) return -5;
        for (int 칸 = 0; 칸 < 1024; 칸++) fitxategi_taula[칸] = 0;
        for (int Fitxategia = 0; Fitxategia < 8; Fitxategia++) if (Memoria_fitxategi_sistema.이름들[Fitxategia * 64] != 0) {
            for (int 칸 = 0; 칸 < 64; 칸++) fitxategi_taula[Fitxategia * 72 + 칸] = Memoria_fitxategi_sistema.이름들[Fitxategia * 64 + 칸];
            idatzi_taula_osoko_zenbaki(Fitxategia * 72 + 64, Memoria_fitxategi_sistema.크기들[Fitxategia]);
            idatzi_taula_osoko_zenbaki(Fitxategia * 72 + 68, Memoria_fitxategi_sistema.허가들[Fitxategia]);
        }
        int hash_fitxategi = 0x811c9dc5;
        for (int sekzio_balio = 0; sekzio_balio < 258; sekzio_balio++) {
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int balio = 0;
                if (sekzio_balio < 2) balio = fitxategi_taula[sekzio_balio * 512 + 칸];
                else {
                    int Fitxategia = (sekzio_balio - 2) / 32, Posizioa = (sekzio_balio - 2) % 32 * 512 + 칸;
                    if (fitxategi_taula[Fitxategia * 72] != 0 && Posizioa < Memoria_fitxategi_sistema.크기들[Fitxategia])
                        balio = gailu_balio.기억읽기(gailu_balio.fitxategi_Memoria() + Fitxategia * 16384 + Posizioa);
                }
                biltegi_gailu_konexio.sekzio_datuak[칸] = balio; hash_fitxategi = 바이트해시(hash_fitxategi, balio);
            }
            if (biltegi_gailu_konexio.Idatzi(HASI_sekzio + 1 + sekzio_balio) < 0) return -5;
        }
        if (biltegi_gailu_konexio.밀어쓰기() < 0) return -5;
        garbitu_datuak(); biltegi_gailu_konexio.idatzi_osoko_zenbaki_balio(0, 0x4a4b534e);
        biltegi_gailu_konexio.idatzi_osoko_zenbaki_balio(4, 세대번호 + 1); biltegi_gailu_konexio.idatzi_osoko_zenbaki_balio(8, hash_fitxategi);
        biltegi_gailu_konexio.idatzi_osoko_zenbaki_balio(12, (세대번호 + 1) ^ hash_fitxategi ^ 0x4a4b534e);
        if (biltegi_gailu_konexio.Idatzi(HASI_sekzio) < 0 || biltegi_gailu_konexio.밀어쓰기() < 0) return -5;
        현재보존본 = Hurrengoa_elementu; 세대번호++;
        return 0;
    }
}
