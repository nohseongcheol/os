// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_VALUE fformat_VALUE. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] ffeil_tabl = new int[1024];
    static int 바이트해시(int VALUE, int data) { return (VALUE ^ data) * 16777619; }
    static void clirio_data() {
        for (int INDEX = 0; INDEX < 512; INDEX++) Storio_dyfais_cyswllt.adran_data[INDEX] = 0;
    }
    static int tabl_cyfanrif(int safle) {
        return ffeil_tabl[safle] | ffeil_tabl[safle + 1] << 8 | ffeil_tabl[safle + 2] << 16 | ffeil_tabl[safle + 3] << 24;
    }
    static void ysgrifennu_tabl_cyfanrif(int safle, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) ffeil_tabl[safle + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
    static boolean gwirio_tabl() {
        for (int Ffeil = 0; Ffeil < 8; Ffeil++) {
            int hyd_VALUE = 0;
            for (int slot_cofnod = 0; slot_cofnod < 64; slot_cofnod++) Cof_system_ffeiliau.Enw[slot_cofnod] = ffeil_tabl[Ffeil * 72 + slot_cofnod];
            while (hyd_VALUE < 64 && Cof_system_ffeiliau.Enw[hyd_VALUE] != 0) hyd_VALUE++;
            if (hyd_VALUE == 0) continue;
            if (!Cof_system_ffeiliau.gwirio_enw(Cof_system_ffeiliau.Enw, hyd_VALUE)
                || tabl_cyfanrif(Ffeil * 72 + 64) < 0 || tabl_cyfanrif(Ffeil * 72 + 64) > 16384) return false;
            for (int 앞 = 0; 앞 < Ffeil; 앞++) {
                boolean 같음 = ffeil_tabl[앞 * 72 + hyd_VALUE] == 0;
                for (int slot_cofnod = 0; slot_cofnod < hyd_VALUE; slot_cofnod++) if (ffeil_tabl[앞 * 72 + slot_cofnod] != Cof_system_ffeiliau.Enw[slot_cofnod]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int START_adran = 1 + 보존본 * 259;
        if (Storio_dyfais_cyswllt.Darllen(START_adran) < 0 || Storio_dyfais_cyswllt.dosrannu_cyfanrif(0) != 0x4a4b534e) return -1;
        int 세대 = Storio_dyfais_cyswllt.dosrannu_cyfanrif(4), prawfswm = Storio_dyfais_cyswllt.dosrannu_cyfanrif(8);
        if (세대 < 1 || Storio_dyfais_cyswllt.dosrannu_cyfanrif(12) != (세대 ^ prawfswm ^ 0x4a4b534e)) return -1;
        int hash_ffeil = 0x811c9dc5;
        for (int adran_VALUE = 0; adran_VALUE < 258; adran_VALUE++) {
            if (Storio_dyfais_cyswllt.Darllen(START_adran + 1 + adran_VALUE) < 0) return -1;
            for (int slot_cofnod = 0; slot_cofnod < 512; slot_cofnod++) {
                int VALUE = Storio_dyfais_cyswllt.adran_data[slot_cofnod];
                hash_ffeil = 바이트해시(hash_ffeil, VALUE);
                if (adran_VALUE < 2) ffeil_tabl[adran_VALUE * 512 + slot_cofnod] = VALUE;
            }
        }
        return hash_ffeil == prawfswm && gwirio_tabl() ? 세대 : -1;
    }
    static int Llwyth(int 보존본) {
        int START_adran = 1 + 보존본 * 259;
        for (int adran_VALUE = 0; adran_VALUE < 2; adran_VALUE++) {
            if (Storio_dyfais_cyswllt.Darllen(START_adran + 1 + adran_VALUE) < 0) return -5;
            for (int slot_cofnod = 0; slot_cofnod < 512; slot_cofnod++) ffeil_tabl[adran_VALUE * 512 + slot_cofnod] = Storio_dyfais_cyswllt.adran_data[slot_cofnod];
        }
        for (int Ffeil = 0; Ffeil < 8; Ffeil++) {
            for (int slot_cofnod = 0; slot_cofnod < 64; slot_cofnod++) Cof_system_ffeiliau.이름들[Ffeil * 64 + slot_cofnod] = ffeil_tabl[Ffeil * 72 + slot_cofnod];
            Cof_system_ffeiliau.newid_maint_Rhestr[Ffeil] = ffeil_tabl[Ffeil * 72] == 0 ? 0 : tabl_cyfanrif(Ffeil * 72 + 64);
            Cof_system_ffeiliau.허가들[Ffeil] = tabl_cyfanrif(Ffeil * 72 + 68) & 511;
            for (int adran_VALUE = 0; adran_VALUE < 32; adran_VALUE++) {
                if (Storio_dyfais_cyswllt.Darllen(START_adran + 3 + Ffeil * 32 + adran_VALUE) < 0) return -5;
                int ADDRESS = dyfais_VALUE.ffeil_Cof() + Ffeil * 16384 + adran_VALUE * 512;
                for (int slot_cofnod = 0; slot_cofnod < 512; slot_cofnod++) dyfais_VALUE.ysgrifennu_Cof(ADDRESS + slot_cofnod, Storio_dyfais_cyswllt.adran_data[slot_cofnod]);
            }
        }
        return 0;
    }
    static void Paratoi() {
        if (Storio_dyfais_cyswllt.Darllen(0) < 0 || Storio_dyfais_cyswllt.dosrannu_cyfanrif(0) != 0x54534b4a
            || Storio_dyfais_cyswllt.dosrannu_cyfanrif(4) != 0x3145524f || Storio_dyfais_cyswllt.dosrannu_cyfanrif(8) != 2048
            || Storio_dyfais_cyswllt.dosrannu_cyfanrif(12) != 0x3153464a) {
            SMS_Terfynell.Ysgrifennu("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        Storio_dyfais_cyswllt.technoleg_gwybodaeth_Ar_gael_9e72441a = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Terfynell.Ysgrifennu("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (Llwyth(현재보존본) < 0) {
            SMS_Terfynell.Ysgrifennu("STORE read failed; halted to preserve files\n"); dyfais_VALUE.정지();
        }
        SMS_Terfynell.Ysgrifennu("STORE restored generation "); SMS_Terfynell.수쓰기(세대번호); SMS_Terfynell.문자(10);
    }
    static int cysoni() {
        if (!Storio_dyfais_cyswllt.technoleg_gwybodaeth_Ar_gael_9e72441a) return -19;
        if (세대번호 == 2147483647) return -75;
        int Nesaf_eitem = 현재보존본 == 0 ? 1 : 0, START_adran = 1 + Nesaf_eitem * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 dyfais_VALUE 캐시를 비운다.
        clirio_data();
        if (Storio_dyfais_cyswllt.Ysgrifennu(START_adran) < 0 || Storio_dyfais_cyswllt.밀어쓰기() < 0) return -5;
        for (int slot_cofnod = 0; slot_cofnod < 1024; slot_cofnod++) ffeil_tabl[slot_cofnod] = 0;
        for (int Ffeil = 0; Ffeil < 8; Ffeil++) if (Cof_system_ffeiliau.이름들[Ffeil * 64] != 0) {
            for (int slot_cofnod = 0; slot_cofnod < 64; slot_cofnod++) ffeil_tabl[Ffeil * 72 + slot_cofnod] = Cof_system_ffeiliau.이름들[Ffeil * 64 + slot_cofnod];
            ysgrifennu_tabl_cyfanrif(Ffeil * 72 + 64, Cof_system_ffeiliau.newid_maint_Rhestr[Ffeil]);
            ysgrifennu_tabl_cyfanrif(Ffeil * 72 + 68, Cof_system_ffeiliau.허가들[Ffeil]);
        }
        int hash_ffeil = 0x811c9dc5;
        for (int adran_VALUE = 0; adran_VALUE < 258; adran_VALUE++) {
            for (int slot_cofnod = 0; slot_cofnod < 512; slot_cofnod++) {
                int VALUE = 0;
                if (adran_VALUE < 2) VALUE = ffeil_tabl[adran_VALUE * 512 + slot_cofnod];
                else {
                    int Ffeil = (adran_VALUE - 2) / 32, safle = (adran_VALUE - 2) % 32 * 512 + slot_cofnod;
                    if (ffeil_tabl[Ffeil * 72] != 0 && safle < Cof_system_ffeiliau.newid_maint_Rhestr[Ffeil])
                        VALUE = dyfais_VALUE.기억읽기(dyfais_VALUE.ffeil_Cof() + Ffeil * 16384 + safle);
                }
                Storio_dyfais_cyswllt.adran_data[slot_cofnod] = VALUE; hash_ffeil = 바이트해시(hash_ffeil, VALUE);
            }
            if (Storio_dyfais_cyswllt.Ysgrifennu(START_adran + 1 + adran_VALUE) < 0) return -5;
        }
        if (Storio_dyfais_cyswllt.밀어쓰기() < 0) return -5;
        clirio_data(); Storio_dyfais_cyswllt.ysgrifennu_cyfanrif_VALUE(0, 0x4a4b534e);
        Storio_dyfais_cyswllt.ysgrifennu_cyfanrif_VALUE(4, 세대번호 + 1); Storio_dyfais_cyswllt.ysgrifennu_cyfanrif_VALUE(8, hash_ffeil);
        Storio_dyfais_cyswllt.ysgrifennu_cyfanrif_VALUE(12, (세대번호 + 1) ^ hash_ffeil ^ 0x4a4b534e);
        if (Storio_dyfais_cyswllt.Ysgrifennu(START_adran) < 0 || Storio_dyfais_cyswllt.밀어쓰기() < 0) return -5;
        현재보존본 = Nesaf_eitem; 세대번호++;
        return 0;
    }
}
