// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_inani misa_inani. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] ifayela_ithebula = new int[1024];
    static int 바이트해시(int inani, int imininingwane) { return (inani ^ imininingwane) * 16777619; }
    static void sula_imininingwane() {
        for (int thola_inkomba = 0; thola_inkomba < 512; thola_inkomba++) Indawo_yokugcina_idivayisi_uxhumano.isigaba_imininingwane[thola_inkomba] = 0;
    }
    static int ithebula_inamba(int 위치) {
        return ifayela_ithebula[위치] | ifayela_ithebula[위치 + 1] << 8 | ifayela_ithebula[위치 + 2] << 16 | ifayela_ithebula[위치 + 3] << 24;
    }
    static void bhala_ithebula_inamba(int 위치, int inani) {
        for (int thola_inkomba = 0; thola_inkomba < 4; thola_inkomba++) ifayela_ithebula[위치 + thola_inkomba] = (inani >>> (thola_inkomba * 8)) & 255;
    }
    static boolean hlola_ithebula() {
        for (int Ihele = 0; Ihele < 8; Ihele++) {
            int ubude_inani = 0;
            for (int isikhala_okufakwayo = 0; isikhala_okufakwayo < 64; isikhala_okufakwayo++) inkumbulo_isistimu_yefayela.Igama[isikhala_okufakwayo] = ifayela_ithebula[Ihele * 72 + isikhala_okufakwayo];
            while (ubude_inani < 64 && inkumbulo_isistimu_yefayela.Igama[ubude_inani] != 0) ubude_inani++;
            if (ubude_inani == 0) continue;
            if (!inkumbulo_isistimu_yefayela.hlola_igama(inkumbulo_isistimu_yefayela.Igama, ubude_inani)
                || ithebula_inamba(Ihele * 72 + 64) < 0 || ithebula_inamba(Ihele * 72 + 64) > 16384) return false;
            for (int 앞 = 0; 앞 < Ihele; 앞++) {
                boolean 같음 = ifayela_ithebula[앞 * 72 + ubude_inani] == 0;
                for (int isikhala_okufakwayo = 0; isikhala_okufakwayo < ubude_inani; isikhala_okufakwayo++) if (ifayela_ithebula[앞 * 72 + isikhala_okufakwayo] != inkumbulo_isistimu_yefayela.Igama[isikhala_okufakwayo]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int qala_isigaba = 1 + 보존본 * 259;
        if (Indawo_yokugcina_idivayisi_uxhumano.Funda(qala_isigaba) < 0 || Indawo_yokugcina_idivayisi_uxhumano.zawula_inamba(0) != 0x4a4b534e) return -1;
        int 세대 = Indawo_yokugcina_idivayisi_uxhumano.zawula_inamba(4), 검사합 = Indawo_yokugcina_idivayisi_uxhumano.zawula_inamba(8);
        if (세대 < 1 || Indawo_yokugcina_idivayisi_uxhumano.zawula_inamba(12) != (세대 ^ 검사합 ^ 0x4a4b534e)) return -1;
        int i_hash_ifayela = 0x811c9dc5;
        for (int isigaba_inani = 0; isigaba_inani < 258; isigaba_inani++) {
            if (Indawo_yokugcina_idivayisi_uxhumano.Funda(qala_isigaba + 1 + isigaba_inani) < 0) return -1;
            for (int isikhala_okufakwayo = 0; isikhala_okufakwayo < 512; isikhala_okufakwayo++) {
                int inani = Indawo_yokugcina_idivayisi_uxhumano.isigaba_imininingwane[isikhala_okufakwayo];
                i_hash_ifayela = 바이트해시(i_hash_ifayela, inani);
                if (isigaba_inani < 2) ifayela_ithebula[isigaba_inani * 512 + isikhala_okufakwayo] = inani;
            }
        }
        return i_hash_ifayela == 검사합 && hlola_ithebula() ? 세대 : -1;
    }
    static int faka(int 보존본) {
        int qala_isigaba = 1 + 보존본 * 259;
        for (int isigaba_inani = 0; isigaba_inani < 2; isigaba_inani++) {
            if (Indawo_yokugcina_idivayisi_uxhumano.Funda(qala_isigaba + 1 + isigaba_inani) < 0) return -5;
            for (int isikhala_okufakwayo = 0; isikhala_okufakwayo < 512; isikhala_okufakwayo++) ifayela_ithebula[isigaba_inani * 512 + isikhala_okufakwayo] = Indawo_yokugcina_idivayisi_uxhumano.isigaba_imininingwane[isikhala_okufakwayo];
        }
        for (int Ihele = 0; Ihele < 8; Ihele++) {
            for (int isikhala_okufakwayo = 0; isikhala_okufakwayo < 64; isikhala_okufakwayo++) inkumbulo_isistimu_yefayela.이름들[Ihele * 64 + isikhala_okufakwayo] = ifayela_ithebula[Ihele * 72 + isikhala_okufakwayo];
            inkumbulo_isistimu_yefayela.linganisa_Uhlu[Ihele] = ifayela_ithebula[Ihele * 72] == 0 ? 0 : ithebula_inamba(Ihele * 72 + 64);
            inkumbulo_isistimu_yefayela.허가들[Ihele] = ithebula_inamba(Ihele * 72 + 68) & 511;
            for (int isigaba_inani = 0; isigaba_inani < 32; isigaba_inani++) {
                if (Indawo_yokugcina_idivayisi_uxhumano.Funda(qala_isigaba + 3 + Ihele * 32 + isigaba_inani) < 0) return -5;
                int ikheli = idivayisi_inani.ifayela_inkumbulo() + Ihele * 16384 + isigaba_inani * 512;
                for (int isikhala_okufakwayo = 0; isikhala_okufakwayo < 512; isikhala_okufakwayo++) idivayisi_inani.bhala_inkumbulo(ikheli + isikhala_okufakwayo, Indawo_yokugcina_idivayisi_uxhumano.isigaba_imininingwane[isikhala_okufakwayo]);
            }
        }
        return 0;
    }
    static void Hlela() {
        if (Indawo_yokugcina_idivayisi_uxhumano.Funda(0) < 0 || Indawo_yokugcina_idivayisi_uxhumano.zawula_inamba(0) != 0x54534b4a
            || Indawo_yokugcina_idivayisi_uxhumano.zawula_inamba(4) != 0x3145524f || Indawo_yokugcina_idivayisi_uxhumano.zawula_inamba(8) != 2048
            || Indawo_yokugcina_idivayisi_uxhumano.zawula_inamba(12) != 0x3153464a) {
            문자단말.Bhala("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        Indawo_yokugcina_idivayisi_uxhumano.사용가능 = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { 문자단말.Bhala("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (faka(현재보존본) < 0) {
            문자단말.Bhala("STORE read failed; halted to preserve files\n"); idivayisi_inani.정지();
        }
        문자단말.Bhala("STORE restored generation "); 문자단말.수쓰기(세대번호); 문자단말.문자(10);
    }
    static int i_sync() {
        if (!Indawo_yokugcina_idivayisi_uxhumano.사용가능) return -19;
        if (세대번호 == 2147483647) return -75;
        int 다음 = 현재보존본 == 0 ? 1 : 0, qala_isigaba = 1 + 다음 * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 idivayisi_inani 캐시를 비운다.
        sula_imininingwane();
        if (Indawo_yokugcina_idivayisi_uxhumano.Bhala(qala_isigaba) < 0 || Indawo_yokugcina_idivayisi_uxhumano.밀어쓰기() < 0) return -5;
        for (int isikhala_okufakwayo = 0; isikhala_okufakwayo < 1024; isikhala_okufakwayo++) ifayela_ithebula[isikhala_okufakwayo] = 0;
        for (int Ihele = 0; Ihele < 8; Ihele++) if (inkumbulo_isistimu_yefayela.이름들[Ihele * 64] != 0) {
            for (int isikhala_okufakwayo = 0; isikhala_okufakwayo < 64; isikhala_okufakwayo++) ifayela_ithebula[Ihele * 72 + isikhala_okufakwayo] = inkumbulo_isistimu_yefayela.이름들[Ihele * 64 + isikhala_okufakwayo];
            bhala_ithebula_inamba(Ihele * 72 + 64, inkumbulo_isistimu_yefayela.linganisa_Uhlu[Ihele]);
            bhala_ithebula_inamba(Ihele * 72 + 68, inkumbulo_isistimu_yefayela.허가들[Ihele]);
        }
        int i_hash_ifayela = 0x811c9dc5;
        for (int isigaba_inani = 0; isigaba_inani < 258; isigaba_inani++) {
            for (int isikhala_okufakwayo = 0; isikhala_okufakwayo < 512; isikhala_okufakwayo++) {
                int inani = 0;
                if (isigaba_inani < 2) inani = ifayela_ithebula[isigaba_inani * 512 + isikhala_okufakwayo];
                else {
                    int Ihele = (isigaba_inani - 2) / 32, 위치 = (isigaba_inani - 2) % 32 * 512 + isikhala_okufakwayo;
                    if (ifayela_ithebula[Ihele * 72] != 0 && 위치 < inkumbulo_isistimu_yefayela.linganisa_Uhlu[Ihele])
                        inani = idivayisi_inani.기억읽기(idivayisi_inani.ifayela_inkumbulo() + Ihele * 16384 + 위치);
                }
                Indawo_yokugcina_idivayisi_uxhumano.isigaba_imininingwane[isikhala_okufakwayo] = inani; i_hash_ifayela = 바이트해시(i_hash_ifayela, inani);
            }
            if (Indawo_yokugcina_idivayisi_uxhumano.Bhala(qala_isigaba + 1 + isigaba_inani) < 0) return -5;
        }
        if (Indawo_yokugcina_idivayisi_uxhumano.밀어쓰기() < 0) return -5;
        sula_imininingwane(); Indawo_yokugcina_idivayisi_uxhumano.bhala_inamba_inani(0, 0x4a4b534e);
        Indawo_yokugcina_idivayisi_uxhumano.bhala_inamba_inani(4, 세대번호 + 1); Indawo_yokugcina_idivayisi_uxhumano.bhala_inamba_inani(8, i_hash_ifayela);
        Indawo_yokugcina_idivayisi_uxhumano.bhala_inamba_inani(12, (세대번호 + 1) ^ i_hash_ifayela ^ 0x4a4b534e);
        if (Indawo_yokugcina_idivayisi_uxhumano.Bhala(qala_isigaba) < 0 || Indawo_yokugcina_idivayisi_uxhumano.밀어쓰기() < 0) return -5;
        현재보존본 = 다음; 세대번호++;
        return 0;
    }
}
