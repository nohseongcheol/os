// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_VALUE fòrmat_VALUE. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] faidhle_clàr = new int[1024];
    static int 바이트해시(int VALUE, int dàta) { return (VALUE ^ dàta) * 16777619; }
    static void glan_dàta() {
        for (int INDEX = 0; INDEX < 512; INDEX++) stòras_uidheam_ceangal.earrann_dàta[INDEX] = 0;
    }
    static int clàr_àireamh_shlàn(int suidhich) {
        return faidhle_clàr[suidhich] | faidhle_clàr[suidhich + 1] << 8 | faidhle_clàr[suidhich + 2] << 16 | faidhle_clàr[suidhich + 3] << 24;
    }
    static void sgrìobh_clàr_àireamh_shlàn(int suidhich, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) faidhle_clàr[suidhich + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
    static boolean seic_clàr() {
        for (int faidhle = 0; faidhle < 8; faidhle++) {
            int faid_VALUE = 0;
            for (int slot_cur_a_steach = 0; slot_cur_a_steach < 64; slot_cur_a_steach++) cuimhne_siostam_fhaidhlichean.Ainm[slot_cur_a_steach] = faidhle_clàr[faidhle * 72 + slot_cur_a_steach];
            while (faid_VALUE < 64 && cuimhne_siostam_fhaidhlichean.Ainm[faid_VALUE] != 0) faid_VALUE++;
            if (faid_VALUE == 0) continue;
            if (!cuimhne_siostam_fhaidhlichean.seic_ainm(cuimhne_siostam_fhaidhlichean.Ainm, faid_VALUE)
                || clàr_àireamh_shlàn(faidhle * 72 + 64) < 0 || clàr_àireamh_shlàn(faidhle * 72 + 64) > 16384) return false;
            for (int 앞 = 0; 앞 < faidhle; 앞++) {
                boolean 같음 = faidhle_clàr[앞 * 72 + faid_VALUE] == 0;
                for (int slot_cur_a_steach = 0; slot_cur_a_steach < faid_VALUE; slot_cur_a_steach++) if (faidhle_clàr[앞 * 72 + slot_cur_a_steach] != cuimhne_siostam_fhaidhlichean.Ainm[slot_cur_a_steach]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int Start_earrann = 1 + 보존본 * 259;
        if (stòras_uidheam_ceangal.읽기(Start_earrann) < 0 || stòras_uidheam_ceangal.정수읽기(0) != 0x4a4b534e) return -1;
        int 세대 = stòras_uidheam_ceangal.정수읽기(4), 검사합 = stòras_uidheam_ceangal.정수읽기(8);
        if (세대 < 1 || stòras_uidheam_ceangal.정수읽기(12) != (세대 ^ 검사합 ^ 0x4a4b534e)) return -1;
        int hais_faidhle = 0x811c9dc5;
        for (int earrann_VALUE = 0; earrann_VALUE < 258; earrann_VALUE++) {
            if (stòras_uidheam_ceangal.읽기(Start_earrann + 1 + earrann_VALUE) < 0) return -1;
            for (int slot_cur_a_steach = 0; slot_cur_a_steach < 512; slot_cur_a_steach++) {
                int VALUE = stòras_uidheam_ceangal.earrann_dàta[slot_cur_a_steach];
                hais_faidhle = 바이트해시(hais_faidhle, VALUE);
                if (earrann_VALUE < 2) faidhle_clàr[earrann_VALUE * 512 + slot_cur_a_steach] = VALUE;
            }
        }
        return hais_faidhle == 검사합 && seic_clàr() ? 세대 : -1;
    }
    static int luchd(int 보존본) {
        int Start_earrann = 1 + 보존본 * 259;
        for (int earrann_VALUE = 0; earrann_VALUE < 2; earrann_VALUE++) {
            if (stòras_uidheam_ceangal.읽기(Start_earrann + 1 + earrann_VALUE) < 0) return -5;
            for (int slot_cur_a_steach = 0; slot_cur_a_steach < 512; slot_cur_a_steach++) faidhle_clàr[earrann_VALUE * 512 + slot_cur_a_steach] = stòras_uidheam_ceangal.earrann_dàta[slot_cur_a_steach];
        }
        for (int faidhle = 0; faidhle < 8; faidhle++) {
            for (int slot_cur_a_steach = 0; slot_cur_a_steach < 64; slot_cur_a_steach++) cuimhne_siostam_fhaidhlichean.이름들[faidhle * 64 + slot_cur_a_steach] = faidhle_clàr[faidhle * 72 + slot_cur_a_steach];
            cuimhne_siostam_fhaidhlichean.atharraich_am_meud_Liosta[faidhle] = faidhle_clàr[faidhle * 72] == 0 ? 0 : clàr_àireamh_shlàn(faidhle * 72 + 64);
            cuimhne_siostam_fhaidhlichean.허가들[faidhle] = clàr_àireamh_shlàn(faidhle * 72 + 68) & 511;
            for (int earrann_VALUE = 0; earrann_VALUE < 32; earrann_VALUE++) {
                if (stòras_uidheam_ceangal.읽기(Start_earrann + 3 + faidhle * 32 + earrann_VALUE) < 0) return -5;
                int ADDRESS = uidheam_VALUE.faidhle_cuimhne() + faidhle * 16384 + earrann_VALUE * 512;
                for (int slot_cur_a_steach = 0; slot_cur_a_steach < 512; slot_cur_a_steach++) uidheam_VALUE.sgrìobh_cuimhne(ADDRESS + slot_cur_a_steach, stòras_uidheam_ceangal.earrann_dàta[slot_cur_a_steach]);
            }
        }
        return 0;
    }
    static void Ullaich() {
        if (stòras_uidheam_ceangal.읽기(0) < 0 || stòras_uidheam_ceangal.정수읽기(0) != 0x54534b4a
            || stòras_uidheam_ceangal.정수읽기(4) != 0x3145524f || stòras_uidheam_ceangal.정수읽기(8) != 2048
            || stòras_uidheam_ceangal.정수읽기(12) != 0x3153464a) {
            SMS_tèirmineal.sgrìobh("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        stòras_uidheam_ceangal.사용가능 = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_tèirmineal.sgrìobh("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (luchd(현재보존본) < 0) {
            SMS_tèirmineal.sgrìobh("STORE read failed; halted to preserve files\n"); uidheam_VALUE.정지();
        }
        SMS_tèirmineal.sgrìobh("STORE restored generation "); SMS_tèirmineal.수쓰기(세대번호); SMS_tèirmineal.문자(10);
    }
    static int sioncronaich() {
        if (!stòras_uidheam_ceangal.사용가능) return -19;
        if (세대번호 == 2147483647) return -75;
        int air_adhart_nì = 현재보존본 == 0 ? 1 : 0, Start_earrann = 1 + air_adhart_nì * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 uidheam_VALUE 캐시를 비운다.
        glan_dàta();
        if (stòras_uidheam_ceangal.sgrìobh(Start_earrann) < 0 || stòras_uidheam_ceangal.밀어쓰기() < 0) return -5;
        for (int slot_cur_a_steach = 0; slot_cur_a_steach < 1024; slot_cur_a_steach++) faidhle_clàr[slot_cur_a_steach] = 0;
        for (int faidhle = 0; faidhle < 8; faidhle++) if (cuimhne_siostam_fhaidhlichean.이름들[faidhle * 64] != 0) {
            for (int slot_cur_a_steach = 0; slot_cur_a_steach < 64; slot_cur_a_steach++) faidhle_clàr[faidhle * 72 + slot_cur_a_steach] = cuimhne_siostam_fhaidhlichean.이름들[faidhle * 64 + slot_cur_a_steach];
            sgrìobh_clàr_àireamh_shlàn(faidhle * 72 + 64, cuimhne_siostam_fhaidhlichean.atharraich_am_meud_Liosta[faidhle]);
            sgrìobh_clàr_àireamh_shlàn(faidhle * 72 + 68, cuimhne_siostam_fhaidhlichean.허가들[faidhle]);
        }
        int hais_faidhle = 0x811c9dc5;
        for (int earrann_VALUE = 0; earrann_VALUE < 258; earrann_VALUE++) {
            for (int slot_cur_a_steach = 0; slot_cur_a_steach < 512; slot_cur_a_steach++) {
                int VALUE = 0;
                if (earrann_VALUE < 2) VALUE = faidhle_clàr[earrann_VALUE * 512 + slot_cur_a_steach];
                else {
                    int faidhle = (earrann_VALUE - 2) / 32, suidhich = (earrann_VALUE - 2) % 32 * 512 + slot_cur_a_steach;
                    if (faidhle_clàr[faidhle * 72] != 0 && suidhich < cuimhne_siostam_fhaidhlichean.atharraich_am_meud_Liosta[faidhle])
                        VALUE = uidheam_VALUE.기억읽기(uidheam_VALUE.faidhle_cuimhne() + faidhle * 16384 + suidhich);
                }
                stòras_uidheam_ceangal.earrann_dàta[slot_cur_a_steach] = VALUE; hais_faidhle = 바이트해시(hais_faidhle, VALUE);
            }
            if (stòras_uidheam_ceangal.sgrìobh(Start_earrann + 1 + earrann_VALUE) < 0) return -5;
        }
        if (stòras_uidheam_ceangal.밀어쓰기() < 0) return -5;
        glan_dàta(); stòras_uidheam_ceangal.sgrìobh_àireamh_shlàn_VALUE(0, 0x4a4b534e);
        stòras_uidheam_ceangal.sgrìobh_àireamh_shlàn_VALUE(4, 세대번호 + 1); stòras_uidheam_ceangal.sgrìobh_àireamh_shlàn_VALUE(8, hais_faidhle);
        stòras_uidheam_ceangal.sgrìobh_àireamh_shlàn_VALUE(12, (세대번호 + 1) ^ hais_faidhle ^ 0x4a4b534e);
        if (stòras_uidheam_ceangal.sgrìobh(Start_earrann) < 0 || stòras_uidheam_ceangal.밀어쓰기() < 0) return -5;
        현재보존본 = air_adhart_nì; 세대번호++;
        return 0;
    }
}
