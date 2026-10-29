// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_baha format_baha. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] faýl_tablisa = new int[1024];
    static int 바이트해시(int baha, int maglumat) { return (baha ^ maglumat) * 16777619; }
    static void arassala_maglumat() {
        for (int indeks = 0; indeks < 512; indeks++) Ammar_enjam_birikme.bölüm_maglumat[indeks] = 0;
    }
    static int tablisa_bitin(int 위치) {
        return faýl_tablisa[위치] | faýl_tablisa[위치 + 1] << 8 | faýl_tablisa[위치 + 2] << 16 | faýl_tablisa[위치 + 3] << 24;
    }
    static void ýaz_tablisa_bitin(int 위치, int baha) {
        for (int indeks = 0; indeks < 4; indeks++) faýl_tablisa[위치 + indeks] = (baha >>> (indeks * 8)) & 255;
    }
    static boolean derňe_tablisa() {
        for (int Faýl = 0; Faýl < 8; Faýl++) {
            int dowamlylyk_baha = 0;
            for (int ýer_girizmeklik = 0; ýer_girizmeklik < 64; ýer_girizmeklik++) ýat_faýl_ulgamy.Ad[ýer_girizmeklik] = faýl_tablisa[Faýl * 72 + ýer_girizmeklik];
            while (dowamlylyk_baha < 64 && ýat_faýl_ulgamy.Ad[dowamlylyk_baha] != 0) dowamlylyk_baha++;
            if (dowamlylyk_baha == 0) continue;
            if (!ýat_faýl_ulgamy.derňe_at(ýat_faýl_ulgamy.Ad, dowamlylyk_baha)
                || tablisa_bitin(Faýl * 72 + 64) < 0 || tablisa_bitin(Faýl * 72 + 64) > 16384) return false;
            for (int 앞 = 0; 앞 < Faýl; 앞++) {
                boolean 같음 = faýl_tablisa[앞 * 72 + dowamlylyk_baha] == 0;
                for (int ýer_girizmeklik = 0; ýer_girizmeklik < dowamlylyk_baha; ýer_girizmeklik++) if (faýl_tablisa[앞 * 72 + ýer_girizmeklik] != ýat_faýl_ulgamy.Ad[ýer_girizmeklik]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int başlat_bölüm = 1 + 보존본 * 259;
        if (Ammar_enjam_birikme.Oka(başlat_bölüm) < 0 || Ammar_enjam_birikme.seljer_bitin(0) != 0x4a4b534e) return -1;
        int 세대 = Ammar_enjam_birikme.seljer_bitin(4), 검사합 = Ammar_enjam_birikme.seljer_bitin(8);
        if (세대 < 1 || Ammar_enjam_birikme.seljer_bitin(12) != (세대 ^ 검사합 ^ 0x4a4b534e)) return -1;
        int heş_kody_faýl = 0x811c9dc5;
        for (int bölüm_baha_366e0bfa = 0; bölüm_baha_366e0bfa < 258; bölüm_baha_366e0bfa++) {
            if (Ammar_enjam_birikme.Oka(başlat_bölüm + 1 + bölüm_baha_366e0bfa) < 0) return -1;
            for (int ýer_girizmeklik = 0; ýer_girizmeklik < 512; ýer_girizmeklik++) {
                int baha = Ammar_enjam_birikme.bölüm_maglumat[ýer_girizmeklik];
                heş_kody_faýl = 바이트해시(heş_kody_faýl, baha);
                if (bölüm_baha_366e0bfa < 2) faýl_tablisa[bölüm_baha_366e0bfa * 512 + ýer_girizmeklik] = baha;
            }
        }
        return heş_kody_faýl == 검사합 && derňe_tablisa() ? 세대 : -1;
    }
    static int ýük(int 보존본) {
        int başlat_bölüm = 1 + 보존본 * 259;
        for (int bölüm_baha_366e0bfa = 0; bölüm_baha_366e0bfa < 2; bölüm_baha_366e0bfa++) {
            if (Ammar_enjam_birikme.Oka(başlat_bölüm + 1 + bölüm_baha_366e0bfa) < 0) return -5;
            for (int ýer_girizmeklik = 0; ýer_girizmeklik < 512; ýer_girizmeklik++) faýl_tablisa[bölüm_baha_366e0bfa * 512 + ýer_girizmeklik] = Ammar_enjam_birikme.bölüm_maglumat[ýer_girizmeklik];
        }
        for (int Faýl = 0; Faýl < 8; Faýl++) {
            for (int ýer_girizmeklik = 0; ýer_girizmeklik < 64; ýer_girizmeklik++) ýat_faýl_ulgamy.이름들[Faýl * 64 + ýer_girizmeklik] = faýl_tablisa[Faýl * 72 + ýer_girizmeklik];
            ýat_faýl_ulgamy.ölçegi_üýtget_Sanaw[Faýl] = faýl_tablisa[Faýl * 72] == 0 ? 0 : tablisa_bitin(Faýl * 72 + 64);
            ýat_faýl_ulgamy.허가들[Faýl] = tablisa_bitin(Faýl * 72 + 68) & 511;
            for (int bölüm_baha_366e0bfa = 0; bölüm_baha_366e0bfa < 32; bölüm_baha_366e0bfa++) {
                if (Ammar_enjam_birikme.Oka(başlat_bölüm + 3 + Faýl * 32 + bölüm_baha_366e0bfa) < 0) return -5;
                int salgy = enjam_baha.faýl_ýat() + Faýl * 16384 + bölüm_baha_366e0bfa * 512;
                for (int ýer_girizmeklik = 0; ýer_girizmeklik < 512; ýer_girizmeklik++) enjam_baha.ýaz_ýat(salgy + ýer_girizmeklik, Ammar_enjam_birikme.bölüm_maglumat[ýer_girizmeklik]);
            }
        }
        return 0;
    }
    static void Taýýarla() {
        if (Ammar_enjam_birikme.Oka(0) < 0 || Ammar_enjam_birikme.seljer_bitin(0) != 0x54534b4a
            || Ammar_enjam_birikme.seljer_bitin(4) != 0x3145524f || Ammar_enjam_birikme.seljer_bitin(8) != 2048
            || Ammar_enjam_birikme.seljer_bitin(12) != 0x3153464a) {
            문자단말.Ýaz("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        Ammar_enjam_birikme.사용가능 = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { 문자단말.Ýaz("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (ýük(현재보존본) < 0) {
            문자단말.Ýaz("STORE read failed; halted to preserve files\n"); enjam_baha.정지();
        }
        문자단말.Ýaz("STORE restored generation "); 문자단말.수쓰기(세대번호); 문자단말.문자(10);
    }
    static int sinhronlaşdyr() {
        if (!Ammar_enjam_birikme.사용가능) return -19;
        if (세대번호 == 2147483647) return -75;
        int 다음 = 현재보존본 == 0 ? 1 : 0, başlat_bölüm = 1 + 다음 * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 enjam_baha 캐시를 비운다.
        arassala_maglumat();
        if (Ammar_enjam_birikme.Ýaz(başlat_bölüm) < 0 || Ammar_enjam_birikme.밀어쓰기() < 0) return -5;
        for (int ýer_girizmeklik = 0; ýer_girizmeklik < 1024; ýer_girizmeklik++) faýl_tablisa[ýer_girizmeklik] = 0;
        for (int Faýl = 0; Faýl < 8; Faýl++) if (ýat_faýl_ulgamy.이름들[Faýl * 64] != 0) {
            for (int ýer_girizmeklik = 0; ýer_girizmeklik < 64; ýer_girizmeklik++) faýl_tablisa[Faýl * 72 + ýer_girizmeklik] = ýat_faýl_ulgamy.이름들[Faýl * 64 + ýer_girizmeklik];
            ýaz_tablisa_bitin(Faýl * 72 + 64, ýat_faýl_ulgamy.ölçegi_üýtget_Sanaw[Faýl]);
            ýaz_tablisa_bitin(Faýl * 72 + 68, ýat_faýl_ulgamy.허가들[Faýl]);
        }
        int heş_kody_faýl = 0x811c9dc5;
        for (int bölüm_baha_366e0bfa = 0; bölüm_baha_366e0bfa < 258; bölüm_baha_366e0bfa++) {
            for (int ýer_girizmeklik = 0; ýer_girizmeklik < 512; ýer_girizmeklik++) {
                int baha = 0;
                if (bölüm_baha_366e0bfa < 2) baha = faýl_tablisa[bölüm_baha_366e0bfa * 512 + ýer_girizmeklik];
                else {
                    int Faýl = (bölüm_baha_366e0bfa - 2) / 32, 위치 = (bölüm_baha_366e0bfa - 2) % 32 * 512 + ýer_girizmeklik;
                    if (faýl_tablisa[Faýl * 72] != 0 && 위치 < ýat_faýl_ulgamy.ölçegi_üýtget_Sanaw[Faýl])
                        baha = enjam_baha.기억읽기(enjam_baha.faýl_ýat() + Faýl * 16384 + 위치);
                }
                Ammar_enjam_birikme.bölüm_maglumat[ýer_girizmeklik] = baha; heş_kody_faýl = 바이트해시(heş_kody_faýl, baha);
            }
            if (Ammar_enjam_birikme.Ýaz(başlat_bölüm + 1 + bölüm_baha_366e0bfa) < 0) return -5;
        }
        if (Ammar_enjam_birikme.밀어쓰기() < 0) return -5;
        arassala_maglumat(); Ammar_enjam_birikme.ýaz_bitin_baha(0, 0x4a4b534e);
        Ammar_enjam_birikme.ýaz_bitin_baha(4, 세대번호 + 1); Ammar_enjam_birikme.ýaz_bitin_baha(8, heş_kody_faýl);
        Ammar_enjam_birikme.ýaz_bitin_baha(12, (세대번호 + 1) ^ heş_kody_faýl ^ 0x4a4b534e);
        if (Ammar_enjam_birikme.Ýaz(başlat_bölüm) < 0 || Ammar_enjam_birikme.밀어쓰기() < 0) return -5;
        현재보존본 = 다음; 세대번호++;
        return 0;
    }
}
