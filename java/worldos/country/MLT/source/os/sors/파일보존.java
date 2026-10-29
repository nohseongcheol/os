// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_VALUE format_VALUE. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] fajl_tabella = new int[1024];
    static int 바이트해시(int VALUE, int data) { return (VALUE ^ data) * 16777619; }
    static void neħħa_data() {
        for (int INDEX = 0; INDEX < 512; INDEX++) Ħażna_mowbajl_konnessjoni.taqsima_data[INDEX] = 0;
    }
    static int tabella_numru_sħiħ(int pożizzjoni) {
        return fajl_tabella[pożizzjoni] | fajl_tabella[pożizzjoni + 1] << 8 | fajl_tabella[pożizzjoni + 2] << 16 | fajl_tabella[pożizzjoni + 3] << 24;
    }
    static void kiteb_tabella_numru_sħiħ(int pożizzjoni, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) fajl_tabella[pożizzjoni + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
    static boolean ċekk_tabella() {
        for (int fajl = 0; fajl < 8; fajl++) {
            int tul_VALUE = 0;
            for (int slott_entrata = 0; slott_entrata < 64; slott_entrata++) Memorja_sistema_tal_fajls.isem[slott_entrata] = fajl_tabella[fajl * 72 + slott_entrata];
            while (tul_VALUE < 64 && Memorja_sistema_tal_fajls.isem[tul_VALUE] != 0) tul_VALUE++;
            if (tul_VALUE == 0) continue;
            if (!Memorja_sistema_tal_fajls.ċekk_isem(Memorja_sistema_tal_fajls.isem, tul_VALUE)
                || tabella_numru_sħiħ(fajl * 72 + 64) < 0 || tabella_numru_sħiħ(fajl * 72 + 64) > 16384) return false;
            for (int 앞 = 0; 앞 < fajl; 앞++) {
                boolean 같음 = fajl_tabella[앞 * 72 + tul_VALUE] == 0;
                for (int slott_entrata = 0; slott_entrata < tul_VALUE; slott_entrata++) if (fajl_tabella[앞 * 72 + slott_entrata] != Memorja_sistema_tal_fajls.isem[slott_entrata]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int Bidu_taqsima = 1 + 보존본 * 259;
        if (Ħażna_mowbajl_konnessjoni.읽기(Bidu_taqsima) < 0 || Ħażna_mowbajl_konnessjoni.analizza_numru_sħiħ(0) != 0x4a4b534e) return -1;
        int 세대 = Ħażna_mowbajl_konnessjoni.analizza_numru_sħiħ(4), 검사합 = Ħażna_mowbajl_konnessjoni.analizza_numru_sħiħ(8);
        if (세대 < 1 || Ħażna_mowbajl_konnessjoni.analizza_numru_sħiħ(12) != (세대 ^ 검사합 ^ 0x4a4b534e)) return -1;
        int hash_fajl = 0x811c9dc5;
        for (int taqsima_VALUE_366e0bfa = 0; taqsima_VALUE_366e0bfa < 258; taqsima_VALUE_366e0bfa++) {
            if (Ħażna_mowbajl_konnessjoni.읽기(Bidu_taqsima + 1 + taqsima_VALUE_366e0bfa) < 0) return -1;
            for (int slott_entrata = 0; slott_entrata < 512; slott_entrata++) {
                int VALUE = Ħażna_mowbajl_konnessjoni.taqsima_data[slott_entrata];
                hash_fajl = 바이트해시(hash_fajl, VALUE);
                if (taqsima_VALUE_366e0bfa < 2) fajl_tabella[taqsima_VALUE_366e0bfa * 512 + slott_entrata] = VALUE;
            }
        }
        return hash_fajl == 검사합 && ċekk_tabella() ? 세대 : -1;
    }
    static int karga(int 보존본) {
        int Bidu_taqsima = 1 + 보존본 * 259;
        for (int taqsima_VALUE_366e0bfa = 0; taqsima_VALUE_366e0bfa < 2; taqsima_VALUE_366e0bfa++) {
            if (Ħażna_mowbajl_konnessjoni.읽기(Bidu_taqsima + 1 + taqsima_VALUE_366e0bfa) < 0) return -5;
            for (int slott_entrata = 0; slott_entrata < 512; slott_entrata++) fajl_tabella[taqsima_VALUE_366e0bfa * 512 + slott_entrata] = Ħażna_mowbajl_konnessjoni.taqsima_data[slott_entrata];
        }
        for (int fajl = 0; fajl < 8; fajl++) {
            for (int slott_entrata = 0; slott_entrata < 64; slott_entrata++) Memorja_sistema_tal_fajls.이름들[fajl * 64 + slott_entrata] = fajl_tabella[fajl * 72 + slott_entrata];
            Memorja_sistema_tal_fajls.daqqas_Lista[fajl] = fajl_tabella[fajl * 72] == 0 ? 0 : tabella_numru_sħiħ(fajl * 72 + 64);
            Memorja_sistema_tal_fajls.허가들[fajl] = tabella_numru_sħiħ(fajl * 72 + 68) & 511;
            for (int taqsima_VALUE_366e0bfa = 0; taqsima_VALUE_366e0bfa < 32; taqsima_VALUE_366e0bfa++) {
                if (Ħażna_mowbajl_konnessjoni.읽기(Bidu_taqsima + 3 + fajl * 32 + taqsima_VALUE_366e0bfa) < 0) return -5;
                int ADDRESS = mowbajl_VALUE.fajl_Memorja() + fajl * 16384 + taqsima_VALUE_366e0bfa * 512;
                for (int slott_entrata = 0; slott_entrata < 512; slott_entrata++) mowbajl_VALUE.kiteb_Memorja(ADDRESS + slott_entrata, Ħażna_mowbajl_konnessjoni.taqsima_data[slott_entrata]);
            }
        }
        return 0;
    }
    static void Ħejji() {
        if (Ħażna_mowbajl_konnessjoni.읽기(0) < 0 || Ħażna_mowbajl_konnessjoni.analizza_numru_sħiħ(0) != 0x54534b4a
            || Ħażna_mowbajl_konnessjoni.analizza_numru_sħiħ(4) != 0x3145524f || Ħażna_mowbajl_konnessjoni.analizza_numru_sħiħ(8) != 2048
            || Ħażna_mowbajl_konnessjoni.analizza_numru_sħiħ(12) != 0x3153464a) {
            SMS_Terminal.kiteb("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        Ħażna_mowbajl_konnessjoni.사용가능 = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Terminal.kiteb("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (karga(현재보존본) < 0) {
            SMS_Terminal.kiteb("STORE read failed; halted to preserve files\n"); mowbajl_VALUE.정지();
        }
        SMS_Terminal.kiteb("STORE restored generation "); SMS_Terminal.수쓰기(세대번호); SMS_Terminal.문자(10);
    }
    static int ssinkronizza() {
        if (!Ħażna_mowbajl_konnessjoni.사용가능) return -19;
        if (세대번호 == 2147483647) return -75;
        int Li_Jmiss_element = 현재보존본 == 0 ? 1 : 0, Bidu_taqsima = 1 + Li_Jmiss_element * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 mowbajl_VALUE 캐시를 비운다.
        neħħa_data();
        if (Ħażna_mowbajl_konnessjoni.kiteb(Bidu_taqsima) < 0 || Ħażna_mowbajl_konnessjoni.밀어쓰기() < 0) return -5;
        for (int slott_entrata = 0; slott_entrata < 1024; slott_entrata++) fajl_tabella[slott_entrata] = 0;
        for (int fajl = 0; fajl < 8; fajl++) if (Memorja_sistema_tal_fajls.이름들[fajl * 64] != 0) {
            for (int slott_entrata = 0; slott_entrata < 64; slott_entrata++) fajl_tabella[fajl * 72 + slott_entrata] = Memorja_sistema_tal_fajls.이름들[fajl * 64 + slott_entrata];
            kiteb_tabella_numru_sħiħ(fajl * 72 + 64, Memorja_sistema_tal_fajls.daqqas_Lista[fajl]);
            kiteb_tabella_numru_sħiħ(fajl * 72 + 68, Memorja_sistema_tal_fajls.허가들[fajl]);
        }
        int hash_fajl = 0x811c9dc5;
        for (int taqsima_VALUE_366e0bfa = 0; taqsima_VALUE_366e0bfa < 258; taqsima_VALUE_366e0bfa++) {
            for (int slott_entrata = 0; slott_entrata < 512; slott_entrata++) {
                int VALUE = 0;
                if (taqsima_VALUE_366e0bfa < 2) VALUE = fajl_tabella[taqsima_VALUE_366e0bfa * 512 + slott_entrata];
                else {
                    int fajl = (taqsima_VALUE_366e0bfa - 2) / 32, pożizzjoni = (taqsima_VALUE_366e0bfa - 2) % 32 * 512 + slott_entrata;
                    if (fajl_tabella[fajl * 72] != 0 && pożizzjoni < Memorja_sistema_tal_fajls.daqqas_Lista[fajl])
                        VALUE = mowbajl_VALUE.기억읽기(mowbajl_VALUE.fajl_Memorja() + fajl * 16384 + pożizzjoni);
                }
                Ħażna_mowbajl_konnessjoni.taqsima_data[slott_entrata] = VALUE; hash_fajl = 바이트해시(hash_fajl, VALUE);
            }
            if (Ħażna_mowbajl_konnessjoni.kiteb(Bidu_taqsima + 1 + taqsima_VALUE_366e0bfa) < 0) return -5;
        }
        if (Ħażna_mowbajl_konnessjoni.밀어쓰기() < 0) return -5;
        neħħa_data(); Ħażna_mowbajl_konnessjoni.kiteb_numru_sħiħ_VALUE(0, 0x4a4b534e);
        Ħażna_mowbajl_konnessjoni.kiteb_numru_sħiħ_VALUE(4, 세대번호 + 1); Ħażna_mowbajl_konnessjoni.kiteb_numru_sħiħ_VALUE(8, hash_fajl);
        Ħażna_mowbajl_konnessjoni.kiteb_numru_sħiħ_VALUE(12, (세대번호 + 1) ^ hash_fajl ^ 0x4a4b534e);
        if (Ħażna_mowbajl_konnessjoni.kiteb(Bidu_taqsima) < 0 || Ħażna_mowbajl_konnessjoni.밀어쓰기() < 0) return -5;
        현재보존본 = Li_Jmiss_element; 세대번호++;
        return 0;
    }
}
