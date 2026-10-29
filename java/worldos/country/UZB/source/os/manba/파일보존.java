// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_VALUE format_VALUE. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] fayl_jadval = new int[1024];
    static int 바이트해시(int VALUE, int ma_lumotlar) { return (VALUE ^ ma_lumotlar) * 16777619; }
    static void tozalamoq_ma_lumotlar() {
        for (int INDEX = 0; INDEX < 512; INDEX++) Xotira_qurilma_aloqa.bo_lim_ma_lumotlar[INDEX] = 0;
    }
    static int jadval_butun_son(int Holati) {
        return fayl_jadval[Holati] | fayl_jadval[Holati + 1] << 8 | fayl_jadval[Holati + 2] << 16 | fayl_jadval[Holati + 3] << 24;
    }
    static void yozmoq_jadval_butun_son(int Holati, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) fayl_jadval[Holati + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
    static boolean chek_jadval() {
        for (int Fayl = 0; Fayl < 8; Fayl++) {
            int uzunlik_VALUE = 0;
            for (int in_kiritish = 0; in_kiritish < 64; in_kiritish++) Xotira_fayllar_tizimi.Nomi[in_kiritish] = fayl_jadval[Fayl * 72 + in_kiritish];
            while (uzunlik_VALUE < 64 && Xotira_fayllar_tizimi.Nomi[uzunlik_VALUE] != 0) uzunlik_VALUE++;
            if (uzunlik_VALUE == 0) continue;
            if (!Xotira_fayllar_tizimi.chek_nom(Xotira_fayllar_tizimi.Nomi, uzunlik_VALUE)
                || jadval_butun_son(Fayl * 72 + 64) < 0 || jadval_butun_son(Fayl * 72 + 64) > 16384) return false;
            for (int old_kamera_VALUE = 0; old_kamera_VALUE < Fayl; old_kamera_VALUE++) {
                boolean 같음 = fayl_jadval[old_kamera_VALUE * 72 + uzunlik_VALUE] == 0;
                for (int in_kiritish = 0; in_kiritish < uzunlik_VALUE; in_kiritish++) if (fayl_jadval[old_kamera_VALUE * 72 + in_kiritish] != Xotira_fayllar_tizimi.Nomi[in_kiritish]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int Start_bo_lim = 1 + 보존본 * 259;
        if (Xotira_qurilma_aloqa.Oʻqish(Start_bo_lim) < 0 || Xotira_qurilma_aloqa.tahlil_qilmoq_butun_son(0) != 0x4a4b534e) return -1;
        int 세대 = Xotira_qurilma_aloqa.tahlil_qilmoq_butun_son(4), 검사합 = Xotira_qurilma_aloqa.tahlil_qilmoq_butun_son(8);
        if (세대 < 1 || Xotira_qurilma_aloqa.tahlil_qilmoq_butun_son(12) != (세대 ^ 검사합 ^ 0x4a4b534e)) return -1;
        int tasodifiy_ma_lumot_fayl = 0x811c9dc5;
        for (int bo_lim_VALUE_366e0bfa = 0; bo_lim_VALUE_366e0bfa < 258; bo_lim_VALUE_366e0bfa++) {
            if (Xotira_qurilma_aloqa.Oʻqish(Start_bo_lim + 1 + bo_lim_VALUE_366e0bfa) < 0) return -1;
            for (int in_kiritish = 0; in_kiritish < 512; in_kiritish++) {
                int VALUE = Xotira_qurilma_aloqa.bo_lim_ma_lumotlar[in_kiritish];
                tasodifiy_ma_lumot_fayl = 바이트해시(tasodifiy_ma_lumot_fayl, VALUE);
                if (bo_lim_VALUE_366e0bfa < 2) fayl_jadval[bo_lim_VALUE_366e0bfa * 512 + in_kiritish] = VALUE;
            }
        }
        return tasodifiy_ma_lumot_fayl == 검사합 && chek_jadval() ? 세대 : -1;
    }
    static int Yuklash(int 보존본) {
        int Start_bo_lim = 1 + 보존본 * 259;
        for (int bo_lim_VALUE_366e0bfa = 0; bo_lim_VALUE_366e0bfa < 2; bo_lim_VALUE_366e0bfa++) {
            if (Xotira_qurilma_aloqa.Oʻqish(Start_bo_lim + 1 + bo_lim_VALUE_366e0bfa) < 0) return -5;
            for (int in_kiritish = 0; in_kiritish < 512; in_kiritish++) fayl_jadval[bo_lim_VALUE_366e0bfa * 512 + in_kiritish] = Xotira_qurilma_aloqa.bo_lim_ma_lumotlar[in_kiritish];
        }
        for (int Fayl = 0; Fayl < 8; Fayl++) {
            for (int in_kiritish = 0; in_kiritish < 64; in_kiritish++) Xotira_fayllar_tizimi.이름들[Fayl * 64 + in_kiritish] = fayl_jadval[Fayl * 72 + in_kiritish];
            Xotira_fayllar_tizimi.o_lcham_Ro_yxat[Fayl] = fayl_jadval[Fayl * 72] == 0 ? 0 : jadval_butun_son(Fayl * 72 + 64);
            Xotira_fayllar_tizimi.허가들[Fayl] = jadval_butun_son(Fayl * 72 + 68) & 511;
            for (int bo_lim_VALUE_366e0bfa = 0; bo_lim_VALUE_366e0bfa < 32; bo_lim_VALUE_366e0bfa++) {
                if (Xotira_qurilma_aloqa.Oʻqish(Start_bo_lim + 3 + Fayl * 32 + bo_lim_VALUE_366e0bfa) < 0) return -5;
                int manzil = qurilma_VALUE.fayl_Xotira() + Fayl * 16384 + bo_lim_VALUE_366e0bfa * 512;
                for (int in_kiritish = 0; in_kiritish < 512; in_kiritish++) qurilma_VALUE.yozmoq_Xotira(manzil + in_kiritish, Xotira_qurilma_aloqa.bo_lim_ma_lumotlar[in_kiritish]);
            }
        }
        return 0;
    }
    static void Tayyorlamoq() {
        if (Xotira_qurilma_aloqa.Oʻqish(0) < 0 || Xotira_qurilma_aloqa.tahlil_qilmoq_butun_son(0) != 0x54534b4a
            || Xotira_qurilma_aloqa.tahlil_qilmoq_butun_son(4) != 0x3145524f || Xotira_qurilma_aloqa.tahlil_qilmoq_butun_son(8) != 2048
            || Xotira_qurilma_aloqa.tahlil_qilmoq_butun_son(12) != 0x3153464a) {
            SMS_Terminal.Yozish("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        Xotira_qurilma_aloqa.사용가능 = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Terminal.Yozish("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (Yuklash(현재보존본) < 0) {
            SMS_Terminal.Yozish("STORE read failed; halted to preserve files\n"); qurilma_VALUE.정지();
        }
        SMS_Terminal.Yozish("STORE restored generation "); SMS_Terminal.수쓰기(세대번호); SMS_Terminal.문자(10);
    }
    static int sinxronlashtirish() {
        if (!Xotira_qurilma_aloqa.사용가능) return -19;
        if (세대번호 == 2147483647) return -75;
        int Keyingi_element = 현재보존본 == 0 ? 1 : 0, Start_bo_lim = 1 + Keyingi_element * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 qurilma_VALUE 캐시를 비운다.
        tozalamoq_ma_lumotlar();
        if (Xotira_qurilma_aloqa.Yozish(Start_bo_lim) < 0 || Xotira_qurilma_aloqa.밀어쓰기() < 0) return -5;
        for (int in_kiritish = 0; in_kiritish < 1024; in_kiritish++) fayl_jadval[in_kiritish] = 0;
        for (int Fayl = 0; Fayl < 8; Fayl++) if (Xotira_fayllar_tizimi.이름들[Fayl * 64] != 0) {
            for (int in_kiritish = 0; in_kiritish < 64; in_kiritish++) fayl_jadval[Fayl * 72 + in_kiritish] = Xotira_fayllar_tizimi.이름들[Fayl * 64 + in_kiritish];
            yozmoq_jadval_butun_son(Fayl * 72 + 64, Xotira_fayllar_tizimi.o_lcham_Ro_yxat[Fayl]);
            yozmoq_jadval_butun_son(Fayl * 72 + 68, Xotira_fayllar_tizimi.허가들[Fayl]);
        }
        int tasodifiy_ma_lumot_fayl = 0x811c9dc5;
        for (int bo_lim_VALUE_366e0bfa = 0; bo_lim_VALUE_366e0bfa < 258; bo_lim_VALUE_366e0bfa++) {
            for (int in_kiritish = 0; in_kiritish < 512; in_kiritish++) {
                int VALUE = 0;
                if (bo_lim_VALUE_366e0bfa < 2) VALUE = fayl_jadval[bo_lim_VALUE_366e0bfa * 512 + in_kiritish];
                else {
                    int Fayl = (bo_lim_VALUE_366e0bfa - 2) / 32, Holati = (bo_lim_VALUE_366e0bfa - 2) % 32 * 512 + in_kiritish;
                    if (fayl_jadval[Fayl * 72] != 0 && Holati < Xotira_fayllar_tizimi.o_lcham_Ro_yxat[Fayl])
                        VALUE = qurilma_VALUE.기억읽기(qurilma_VALUE.fayl_Xotira() + Fayl * 16384 + Holati);
                }
                Xotira_qurilma_aloqa.bo_lim_ma_lumotlar[in_kiritish] = VALUE; tasodifiy_ma_lumot_fayl = 바이트해시(tasodifiy_ma_lumot_fayl, VALUE);
            }
            if (Xotira_qurilma_aloqa.Yozish(Start_bo_lim + 1 + bo_lim_VALUE_366e0bfa) < 0) return -5;
        }
        if (Xotira_qurilma_aloqa.밀어쓰기() < 0) return -5;
        tozalamoq_ma_lumotlar(); Xotira_qurilma_aloqa.yozmoq_butun_son_VALUE(0, 0x4a4b534e);
        Xotira_qurilma_aloqa.yozmoq_butun_son_VALUE(4, 세대번호 + 1); Xotira_qurilma_aloqa.yozmoq_butun_son_VALUE(8, tasodifiy_ma_lumot_fayl);
        Xotira_qurilma_aloqa.yozmoq_butun_son_VALUE(12, (세대번호 + 1) ^ tasodifiy_ma_lumot_fayl ^ 0x4a4b534e);
        if (Xotira_qurilma_aloqa.Yozish(Start_bo_lim) < 0 || Xotira_qurilma_aloqa.밀어쓰기() < 0) return -5;
        현재보존본 = Keyingi_element; 세대번호++;
        return 0;
    }
}
