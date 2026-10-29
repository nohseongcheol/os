// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_VALUE snið_VALUE. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] skrá_tafla = new int[1024];
    static int 바이트해시(int VALUE, int gögn) { return (VALUE ^ gögn) * 16777619; }
    static void hreinsa_gögn() {
        for (int INDEX = 0; INDEX < 512; INDEX++) geymsla_tæki_tenging.hluti_gögn[INDEX] = 0;
    }
    static int tafla_heiltala(int Staðsetning) {
        return skrá_tafla[Staðsetning] | skrá_tafla[Staðsetning + 1] << 8 | skrá_tafla[Staðsetning + 2] << 16 | skrá_tafla[Staðsetning + 3] << 24;
    }
    static void skrifa_tafla_heiltala(int Staðsetning, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) skrá_tafla[Staðsetning + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
    static boolean athuga_tafla() {
        for (int Skrá = 0; Skrá < 8; Skrá++) {
            int lengd_VALUE = 0;
            for (int rauf_færsla = 0; rauf_færsla < 64; rauf_færsla++) Minni_skrárkerfi.Heiti[rauf_færsla] = skrá_tafla[Skrá * 72 + rauf_færsla];
            while (lengd_VALUE < 64 && Minni_skrárkerfi.Heiti[lengd_VALUE] != 0) lengd_VALUE++;
            if (lengd_VALUE == 0) continue;
            if (!Minni_skrárkerfi.athuga_heiti(Minni_skrárkerfi.Heiti, lengd_VALUE)
                || tafla_heiltala(Skrá * 72 + 64) < 0 || tafla_heiltala(Skrá * 72 + 64) > 16384) return false;
            for (int myndavél_að_framan_VALUE = 0; myndavél_að_framan_VALUE < Skrá; myndavél_að_framan_VALUE++) {
                boolean 같음 = skrá_tafla[myndavél_að_framan_VALUE * 72 + lengd_VALUE] == 0;
                for (int rauf_færsla = 0; rauf_færsla < lengd_VALUE; rauf_færsla++) if (skrá_tafla[myndavél_að_framan_VALUE * 72 + rauf_færsla] != Minni_skrárkerfi.Heiti[rauf_færsla]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int Opna_hluti = 1 + 보존본 * 259;
        if (geymsla_tæki_tenging.Lestur(Opna_hluti) < 0 || geymsla_tæki_tenging.þátta_heiltala(0) != 0x4a4b534e) return -1;
        int 세대 = geymsla_tæki_tenging.þátta_heiltala(4), prófsumma = geymsla_tæki_tenging.þátta_heiltala(8);
        if (세대 < 1 || geymsla_tæki_tenging.þátta_heiltala(12) != (세대 ^ prófsumma ^ 0x4a4b534e)) return -1;
        int tæting_skrá = 0x811c9dc5;
        for (int hluti_VALUE = 0; hluti_VALUE < 258; hluti_VALUE++) {
            if (geymsla_tæki_tenging.Lestur(Opna_hluti + 1 + hluti_VALUE) < 0) return -1;
            for (int rauf_færsla = 0; rauf_færsla < 512; rauf_færsla++) {
                int VALUE = geymsla_tæki_tenging.hluti_gögn[rauf_færsla];
                tæting_skrá = 바이트해시(tæting_skrá, VALUE);
                if (hluti_VALUE < 2) skrá_tafla[hluti_VALUE * 512 + rauf_færsla] = VALUE;
            }
        }
        return tæting_skrá == prófsumma && athuga_tafla() ? 세대 : -1;
    }
    static int Hlaða(int 보존본) {
        int Opna_hluti = 1 + 보존본 * 259;
        for (int hluti_VALUE = 0; hluti_VALUE < 2; hluti_VALUE++) {
            if (geymsla_tæki_tenging.Lestur(Opna_hluti + 1 + hluti_VALUE) < 0) return -5;
            for (int rauf_færsla = 0; rauf_færsla < 512; rauf_færsla++) skrá_tafla[hluti_VALUE * 512 + rauf_færsla] = geymsla_tæki_tenging.hluti_gögn[rauf_færsla];
        }
        for (int Skrá = 0; Skrá < 8; Skrá++) {
            for (int rauf_færsla = 0; rauf_færsla < 64; rauf_færsla++) Minni_skrárkerfi.이름들[Skrá * 64 + rauf_færsla] = skrá_tafla[Skrá * 72 + rauf_færsla];
            Minni_skrárkerfi.breyta_stærð_Listi[Skrá] = skrá_tafla[Skrá * 72] == 0 ? 0 : tafla_heiltala(Skrá * 72 + 64);
            Minni_skrárkerfi.허가들[Skrá] = tafla_heiltala(Skrá * 72 + 68) & 511;
            for (int hluti_VALUE = 0; hluti_VALUE < 32; hluti_VALUE++) {
                if (geymsla_tæki_tenging.Lestur(Opna_hluti + 3 + Skrá * 32 + hluti_VALUE) < 0) return -5;
                int slóð = tæki_VALUE.skrá_Minni() + Skrá * 16384 + hluti_VALUE * 512;
                for (int rauf_færsla = 0; rauf_færsla < 512; rauf_færsla++) tæki_VALUE.skrifa_Minni(slóð + rauf_færsla, geymsla_tæki_tenging.hluti_gögn[rauf_færsla]);
            }
        }
        return 0;
    }
    static void Undirbúa() {
        if (geymsla_tæki_tenging.Lestur(0) < 0 || geymsla_tæki_tenging.þátta_heiltala(0) != 0x54534b4a
            || geymsla_tæki_tenging.þátta_heiltala(4) != 0x3145524f || geymsla_tæki_tenging.þátta_heiltala(8) != 2048
            || geymsla_tæki_tenging.þátta_heiltala(12) != 0x3153464a) {
            SMS_Endastöð.Skrift("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        geymsla_tæki_tenging.upplýsingatækni_Laus_9e72441a = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Endastöð.Skrift("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (Hlaða(현재보존본) < 0) {
            SMS_Endastöð.Skrift("STORE read failed; halted to preserve files\n"); tæki_VALUE.정지();
        }
        SMS_Endastöð.Skrift("STORE restored generation "); SMS_Endastöð.skrifa_númer(세대번호); SMS_Endastöð.문자(10);
    }
    static int samstilla() {
        if (!geymsla_tæki_tenging.upplýsingatækni_Laus_9e72441a) return -19;
        if (세대번호 == 2147483647) return -75;
        int Áfram_vara = 현재보존본 == 0 ? 1 : 0, Opna_hluti = 1 + Áfram_vara * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 tæki_VALUE 캐시를 비운다.
        hreinsa_gögn();
        if (geymsla_tæki_tenging.Skrift(Opna_hluti) < 0 || geymsla_tæki_tenging.밀어쓰기() < 0) return -5;
        for (int rauf_færsla = 0; rauf_færsla < 1024; rauf_færsla++) skrá_tafla[rauf_færsla] = 0;
        for (int Skrá = 0; Skrá < 8; Skrá++) if (Minni_skrárkerfi.이름들[Skrá * 64] != 0) {
            for (int rauf_færsla = 0; rauf_færsla < 64; rauf_færsla++) skrá_tafla[Skrá * 72 + rauf_færsla] = Minni_skrárkerfi.이름들[Skrá * 64 + rauf_færsla];
            skrifa_tafla_heiltala(Skrá * 72 + 64, Minni_skrárkerfi.breyta_stærð_Listi[Skrá]);
            skrifa_tafla_heiltala(Skrá * 72 + 68, Minni_skrárkerfi.허가들[Skrá]);
        }
        int tæting_skrá = 0x811c9dc5;
        for (int hluti_VALUE = 0; hluti_VALUE < 258; hluti_VALUE++) {
            for (int rauf_færsla = 0; rauf_færsla < 512; rauf_færsla++) {
                int VALUE = 0;
                if (hluti_VALUE < 2) VALUE = skrá_tafla[hluti_VALUE * 512 + rauf_færsla];
                else {
                    int Skrá = (hluti_VALUE - 2) / 32, Staðsetning = (hluti_VALUE - 2) % 32 * 512 + rauf_færsla;
                    if (skrá_tafla[Skrá * 72] != 0 && Staðsetning < Minni_skrárkerfi.breyta_stærð_Listi[Skrá])
                        VALUE = tæki_VALUE.기억읽기(tæki_VALUE.skrá_Minni() + Skrá * 16384 + Staðsetning);
                }
                geymsla_tæki_tenging.hluti_gögn[rauf_færsla] = VALUE; tæting_skrá = 바이트해시(tæting_skrá, VALUE);
            }
            if (geymsla_tæki_tenging.Skrift(Opna_hluti + 1 + hluti_VALUE) < 0) return -5;
        }
        if (geymsla_tæki_tenging.밀어쓰기() < 0) return -5;
        hreinsa_gögn(); geymsla_tæki_tenging.skrifa_heiltala_VALUE(0, 0x4a4b534e);
        geymsla_tæki_tenging.skrifa_heiltala_VALUE(4, 세대번호 + 1); geymsla_tæki_tenging.skrifa_heiltala_VALUE(8, tæting_skrá);
        geymsla_tæki_tenging.skrifa_heiltala_VALUE(12, (세대번호 + 1) ^ tæting_skrá ^ 0x4a4b534e);
        if (geymsla_tæki_tenging.Skrift(Opna_hluti) < 0 || geymsla_tæki_tenging.밀어쓰기() < 0) return -5;
        현재보존본 = Áfram_vara; 세대번호++;
        return 0;
    }
}
