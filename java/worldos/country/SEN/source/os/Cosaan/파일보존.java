// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_xëyma dayo_xëyma. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] bara_denc_àlluwa = new int[1024];
    static int 바이트해시(int xëyma, int mbir) { return (xëyma ^ mbir) * 16777619; }
    static void efaase_mbir() {
        for (int àlluwa_tur = 0; àlluwa_tur < 512; àlluwa_tur++) Dencukaay_toftal_jokkalóo.dog_mbir[àlluwa_tur] = 0;
    }
    static int àlluwa_lëmm(int 위치) {
        return bara_denc_àlluwa[위치] | bara_denc_àlluwa[위치 + 1] << 8 | bara_denc_àlluwa[위치 + 2] << 16 | bara_denc_àlluwa[위치 + 3] << 24;
    }
    static void biir_àlluwa_lëmm(int 위치, int xëyma) {
        for (int àlluwa_tur = 0; àlluwa_tur < 4; àlluwa_tur++) bara_denc_àlluwa[위치 + àlluwa_tur] = (xëyma >>> (àlluwa_tur * 8)) & 255;
    }
    static boolean sek_àlluwa() {
        for (int bara_denc = 0; bara_denc < 8; bara_denc++) {
            int diir_xëyma = 0;
            for (int xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < 64; xar_xar_dugal_xabaar++) fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.tur_253d1510[xar_xar_dugal_xabaar] = bara_denc_àlluwa[bara_denc * 72 + xar_xar_dugal_xabaar];
            while (diir_xëyma < 64 && fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.tur_253d1510[diir_xëyma] != 0) diir_xëyma++;
            if (diir_xëyma == 0) continue;
            if (!fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.sek_tur(fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.tur_253d1510, diir_xëyma)
                || àlluwa_lëmm(bara_denc * 72 + 64) < 0 || àlluwa_lëmm(bara_denc * 72 + 64) > 16384) return false;
            for (int 앞 = 0; 앞 < bara_denc; 앞++) {
                boolean 같음 = bara_denc_àlluwa[앞 * 72 + diir_xëyma] == 0;
                for (int xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < diir_xëyma; xar_xar_dugal_xabaar++) if (bara_denc_àlluwa[앞 * 72 + xar_xar_dugal_xabaar] != fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.tur_253d1510[xar_xar_dugal_xabaar]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int Door_dog = 1 + 보존본 * 259;
        if (Dencukaay_toftal_jokkalóo.읽기(Door_dog) < 0 || Dencukaay_toftal_jokkalóo.Segg_lëmm(0) != 0x4a4b534e) return -1;
        int 세대 = Dencukaay_toftal_jokkalóo.Segg_lëmm(4), 검사합 = Dencukaay_toftal_jokkalóo.Segg_lëmm(8);
        if (세대 < 1 || Dencukaay_toftal_jokkalóo.Segg_lëmm(12) != (세대 ^ 검사합 ^ 0x4a4b534e)) return -1;
        int caabiy_teqale_bi_bara_denc = 0x811c9dc5;
        for (int dog_xëyma = 0; dog_xëyma < 258; dog_xëyma++) {
            if (Dencukaay_toftal_jokkalóo.읽기(Door_dog + 1 + dog_xëyma) < 0) return -1;
            for (int xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < 512; xar_xar_dugal_xabaar++) {
                int xëyma = Dencukaay_toftal_jokkalóo.dog_mbir[xar_xar_dugal_xabaar];
                caabiy_teqale_bi_bara_denc = 바이트해시(caabiy_teqale_bi_bara_denc, xëyma);
                if (dog_xëyma < 2) bara_denc_àlluwa[dog_xëyma * 512 + xar_xar_dugal_xabaar] = xëyma;
            }
        }
        return caabiy_teqale_bi_bara_denc == 검사합 && sek_àlluwa() ? 세대 : -1;
    }
    static int Yab(int 보존본) {
        int Door_dog = 1 + 보존본 * 259;
        for (int dog_xëyma = 0; dog_xëyma < 2; dog_xëyma++) {
            if (Dencukaay_toftal_jokkalóo.읽기(Door_dog + 1 + dog_xëyma) < 0) return -5;
            for (int xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < 512; xar_xar_dugal_xabaar++) bara_denc_àlluwa[dog_xëyma * 512 + xar_xar_dugal_xabaar] = Dencukaay_toftal_jokkalóo.dog_mbir[xar_xar_dugal_xabaar];
        }
        for (int bara_denc = 0; bara_denc < 8; bara_denc++) {
            for (int xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < 64; xar_xar_dugal_xabaar++) fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.이름들[bara_denc * 64 + xar_xar_dugal_xabaar] = bara_denc_àlluwa[bara_denc * 72 + xar_xar_dugal_xabaar];
            fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.tolluwaay_lim[bara_denc] = bara_denc_àlluwa[bara_denc * 72] == 0 ? 0 : àlluwa_lëmm(bara_denc * 72 + 64);
            fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.허가들[bara_denc] = àlluwa_lëmm(bara_denc * 72 + 68) & 511;
            for (int dog_xëyma = 0; dog_xëyma < 32; dog_xëyma++) {
                if (Dencukaay_toftal_jokkalóo.읽기(Door_dog + 3 + bara_denc * 32 + dog_xëyma) < 0) return -5;
                int dëkkuwaay = toftal_xëyma.bara_denc_fatlekookaay() + bara_denc * 16384 + dog_xëyma * 512;
                for (int xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < 512; xar_xar_dugal_xabaar++) toftal_xëyma.biir_fatlekookaay(dëkkuwaay + xar_xar_dugal_xabaar, Dencukaay_toftal_jokkalóo.dog_mbir[xar_xar_dugal_xabaar]);
            }
        }
        return 0;
    }
    static void jël_matuwaay() {
        if (Dencukaay_toftal_jokkalóo.읽기(0) < 0 || Dencukaay_toftal_jokkalóo.Segg_lëmm(0) != 0x54534b4a
            || Dencukaay_toftal_jokkalóo.Segg_lëmm(4) != 0x3145524f || Dencukaay_toftal_jokkalóo.Segg_lëmm(8) != 2048
            || Dencukaay_toftal_jokkalóo.Segg_lëmm(12) != 0x3153464a) {
            문자단말.biir("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        Dencukaay_toftal_jokkalóo.사용가능 = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { 문자단말.biir("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (Yab(현재보존본) < 0) {
            문자단말.biir("STORE read failed; halted to preserve files\n"); toftal_xëyma.정지();
        }
        문자단말.biir("STORE restored generation "); 문자단말.수쓰기(세대번호); 문자단말.문자(10);
    }
    static int lëkkale() {
        if (!Dencukaay_toftal_jokkalóo.사용가능) return -19;
        if (세대번호 == 2147483647) return -75;
        int 다음 = 현재보존본 == 0 ? 1 : 0, Door_dog = 1 + 다음 * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 toftal_xëyma 캐시를 비운다.
        efaase_mbir();
        if (Dencukaay_toftal_jokkalóo.biir(Door_dog) < 0 || Dencukaay_toftal_jokkalóo.밀어쓰기() < 0) return -5;
        for (int xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < 1024; xar_xar_dugal_xabaar++) bara_denc_àlluwa[xar_xar_dugal_xabaar] = 0;
        for (int bara_denc = 0; bara_denc < 8; bara_denc++) if (fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.이름들[bara_denc * 64] != 0) {
            for (int xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < 64; xar_xar_dugal_xabaar++) bara_denc_àlluwa[bara_denc * 72 + xar_xar_dugal_xabaar] = fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.이름들[bara_denc * 64 + xar_xar_dugal_xabaar];
            biir_àlluwa_lëmm(bara_denc * 72 + 64, fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.tolluwaay_lim[bara_denc]);
            biir_àlluwa_lëmm(bara_denc * 72 + 68, fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.허가들[bara_denc]);
        }
        int caabiy_teqale_bi_bara_denc = 0x811c9dc5;
        for (int dog_xëyma = 0; dog_xëyma < 258; dog_xëyma++) {
            for (int xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < 512; xar_xar_dugal_xabaar++) {
                int xëyma = 0;
                if (dog_xëyma < 2) xëyma = bara_denc_àlluwa[dog_xëyma * 512 + xar_xar_dugal_xabaar];
                else {
                    int bara_denc = (dog_xëyma - 2) / 32, 위치 = (dog_xëyma - 2) % 32 * 512 + xar_xar_dugal_xabaar;
                    if (bara_denc_àlluwa[bara_denc * 72] != 0 && 위치 < fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.tolluwaay_lim[bara_denc])
                        xëyma = toftal_xëyma.기억읽기(toftal_xëyma.bara_denc_fatlekookaay() + bara_denc * 16384 + 위치);
                }
                Dencukaay_toftal_jokkalóo.dog_mbir[xar_xar_dugal_xabaar] = xëyma; caabiy_teqale_bi_bara_denc = 바이트해시(caabiy_teqale_bi_bara_denc, xëyma);
            }
            if (Dencukaay_toftal_jokkalóo.biir(Door_dog + 1 + dog_xëyma) < 0) return -5;
        }
        if (Dencukaay_toftal_jokkalóo.밀어쓰기() < 0) return -5;
        efaase_mbir(); Dencukaay_toftal_jokkalóo.biir_lëmm_xëyma(0, 0x4a4b534e);
        Dencukaay_toftal_jokkalóo.biir_lëmm_xëyma(4, 세대번호 + 1); Dencukaay_toftal_jokkalóo.biir_lëmm_xëyma(8, caabiy_teqale_bi_bara_denc);
        Dencukaay_toftal_jokkalóo.biir_lëmm_xëyma(12, (세대번호 + 1) ^ caabiy_teqale_bi_bara_denc ^ 0x4a4b534e);
        if (Dencukaay_toftal_jokkalóo.biir(Door_dog) < 0 || Dencukaay_toftal_jokkalóo.밀어쓰기() < 0) return -5;
        현재보존본 = 다음; 세대번호++;
        return 0;
    }
}
