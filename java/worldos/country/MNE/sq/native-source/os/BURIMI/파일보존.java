// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_VALUE format_VALUE. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] skedar_tabelë = new int[1024];
    static int 바이트해시(int VALUE, int të_dhëna) { return (VALUE ^ të_dhëna) * 16777619; }
    static void pastroj_të_dhëna() {
        for (int INDEX = 0; INDEX < 512; INDEX++) hapësira_ruajtëse_pajisje_lidhje.seksion_të_dhëna[INDEX] = 0;
    }
    static int tabelë_numër_i_plotë(int Pozicioni) {
        return skedar_tabelë[Pozicioni] | skedar_tabelë[Pozicioni + 1] << 8 | skedar_tabelë[Pozicioni + 2] << 16 | skedar_tabelë[Pozicioni + 3] << 24;
    }
    static void shkruaj_tabelë_numër_i_plotë(int Pozicioni, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) skedar_tabelë[Pozicioni + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
    static boolean çek_tabelë() {
        for (int Kartelë = 0; Kartelë < 8; Kartelë++) {
            int gjatësi_VALUE = 0;
            for (int hapësirë_për_tekst_futje = 0; hapësirë_për_tekst_futje < 64; hapësirë_për_tekst_futje++) Memorie_sistemi_i_skedarëve.Emër[hapësirë_për_tekst_futje] = skedar_tabelë[Kartelë * 72 + hapësirë_për_tekst_futje];
            while (gjatësi_VALUE < 64 && Memorie_sistemi_i_skedarëve.Emër[gjatësi_VALUE] != 0) gjatësi_VALUE++;
            if (gjatësi_VALUE == 0) continue;
            if (!Memorie_sistemi_i_skedarëve.çek_emër(Memorie_sistemi_i_skedarëve.Emër, gjatësi_VALUE)
                || tabelë_numër_i_plotë(Kartelë * 72 + 64) < 0 || tabelë_numër_i_plotë(Kartelë * 72 + 64) > 16384) return false;
            for (int e_përparme_VALUE = 0; e_përparme_VALUE < Kartelë; e_përparme_VALUE++) {
                boolean 같음 = skedar_tabelë[e_përparme_VALUE * 72 + gjatësi_VALUE] == 0;
                for (int hapësirë_për_tekst_futje = 0; hapësirë_për_tekst_futje < gjatësi_VALUE; hapësirë_për_tekst_futje++) if (skedar_tabelë[e_përparme_VALUE * 72 + hapësirë_për_tekst_futje] != Memorie_sistemi_i_skedarëve.Emër[hapësirë_për_tekst_futje]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int nis_seksion = 1 + 보존본 * 259;
        if (hapësira_ruajtëse_pajisje_lidhje.Leximi(nis_seksion) < 0 || hapësira_ruajtëse_pajisje_lidhje.analizoj_numër_i_plotë(0) != 0x4a4b534e) return -1;
        int 세대 = hapësira_ruajtëse_pajisje_lidhje.analizoj_numër_i_plotë(4), kontrolli_i_shumës = hapësira_ruajtëse_pajisje_lidhje.analizoj_numër_i_plotë(8);
        if (세대 < 1 || hapësira_ruajtëse_pajisje_lidhje.analizoj_numër_i_plotë(12) != (세대 ^ kontrolli_i_shumës ^ 0x4a4b534e)) return -1;
        int hash_skedar = 0x811c9dc5;
        for (int seksion_VALUE = 0; seksion_VALUE < 258; seksion_VALUE++) {
            if (hapësira_ruajtëse_pajisje_lidhje.Leximi(nis_seksion + 1 + seksion_VALUE) < 0) return -1;
            for (int hapësirë_për_tekst_futje = 0; hapësirë_për_tekst_futje < 512; hapësirë_për_tekst_futje++) {
                int VALUE = hapësira_ruajtëse_pajisje_lidhje.seksion_të_dhëna[hapësirë_për_tekst_futje];
                hash_skedar = 바이트해시(hash_skedar, VALUE);
                if (seksion_VALUE < 2) skedar_tabelë[seksion_VALUE * 512 + hapësirë_për_tekst_futje] = VALUE;
            }
        }
        return hash_skedar == kontrolli_i_shumës && çek_tabelë() ? 세대 : -1;
    }
    static int Ngarko(int 보존본) {
        int nis_seksion = 1 + 보존본 * 259;
        for (int seksion_VALUE = 0; seksion_VALUE < 2; seksion_VALUE++) {
            if (hapësira_ruajtëse_pajisje_lidhje.Leximi(nis_seksion + 1 + seksion_VALUE) < 0) return -5;
            for (int hapësirë_për_tekst_futje = 0; hapësirë_për_tekst_futje < 512; hapësirë_për_tekst_futje++) skedar_tabelë[seksion_VALUE * 512 + hapësirë_për_tekst_futje] = hapësira_ruajtëse_pajisje_lidhje.seksion_të_dhëna[hapësirë_për_tekst_futje];
        }
        for (int Kartelë = 0; Kartelë < 8; Kartelë++) {
            for (int hapësirë_për_tekst_futje = 0; hapësirë_për_tekst_futje < 64; hapësirë_për_tekst_futje++) Memorie_sistemi_i_skedarëve.이름들[Kartelë * 64 + hapësirë_për_tekst_futje] = skedar_tabelë[Kartelë * 72 + hapësirë_për_tekst_futje];
            Memorie_sistemi_i_skedarëve.ndryshoj_përmasat_Listë[Kartelë] = skedar_tabelë[Kartelë * 72] == 0 ? 0 : tabelë_numër_i_plotë(Kartelë * 72 + 64);
            Memorie_sistemi_i_skedarëve.허가들[Kartelë] = tabelë_numër_i_plotë(Kartelë * 72 + 68) & 511;
            for (int seksion_VALUE = 0; seksion_VALUE < 32; seksion_VALUE++) {
                if (hapësira_ruajtëse_pajisje_lidhje.Leximi(nis_seksion + 3 + Kartelë * 32 + seksion_VALUE) < 0) return -5;
                int email = pajisje_VALUE.skedar_Memorie() + Kartelë * 16384 + seksion_VALUE * 512;
                for (int hapësirë_për_tekst_futje = 0; hapësirë_për_tekst_futje < 512; hapësirë_për_tekst_futje++) pajisje_VALUE.shkruaj_Memorie(email + hapësirë_për_tekst_futje, hapësira_ruajtëse_pajisje_lidhje.seksion_të_dhëna[hapësirë_për_tekst_futje]);
            }
        }
        return 0;
    }
    static void Përgatit() {
        if (hapësira_ruajtëse_pajisje_lidhje.Leximi(0) < 0 || hapësira_ruajtëse_pajisje_lidhje.analizoj_numër_i_plotë(0) != 0x54534b4a
            || hapësira_ruajtëse_pajisje_lidhje.analizoj_numër_i_plotë(4) != 0x3145524f || hapësira_ruajtëse_pajisje_lidhje.analizoj_numër_i_plotë(8) != 2048
            || hapësira_ruajtëse_pajisje_lidhje.analizoj_numër_i_plotë(12) != 0x3153464a) {
            SMS_Terminali.Shkrimi("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        hapësira_ruajtëse_pajisje_lidhje.teknologjia_e_informacionit_Aktiv_9e72441a = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Terminali.Shkrimi("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (Ngarko(현재보존본) < 0) {
            SMS_Terminali.Shkrimi("STORE read failed; halted to preserve files\n"); pajisje_VALUE.정지();
        }
        SMS_Terminali.Shkrimi("STORE restored generation "); SMS_Terminali.수쓰기(세대번호); SMS_Terminali.문자(10);
    }
    static int sinkronizoj() {
        if (!hapësira_ruajtëse_pajisje_lidhje.teknologjia_e_informacionit_Aktiv_9e72441a) return -19;
        if (세대번호 == 2147483647) return -75;
        int Tjetër_njësi = 현재보존본 == 0 ? 1 : 0, nis_seksion = 1 + Tjetër_njësi * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 pajisje_VALUE 캐시를 비운다.
        pastroj_të_dhëna();
        if (hapësira_ruajtëse_pajisje_lidhje.Shkrimi(nis_seksion) < 0 || hapësira_ruajtëse_pajisje_lidhje.밀어쓰기() < 0) return -5;
        for (int hapësirë_për_tekst_futje = 0; hapësirë_për_tekst_futje < 1024; hapësirë_për_tekst_futje++) skedar_tabelë[hapësirë_për_tekst_futje] = 0;
        for (int Kartelë = 0; Kartelë < 8; Kartelë++) if (Memorie_sistemi_i_skedarëve.이름들[Kartelë * 64] != 0) {
            for (int hapësirë_për_tekst_futje = 0; hapësirë_për_tekst_futje < 64; hapësirë_për_tekst_futje++) skedar_tabelë[Kartelë * 72 + hapësirë_për_tekst_futje] = Memorie_sistemi_i_skedarëve.이름들[Kartelë * 64 + hapësirë_për_tekst_futje];
            shkruaj_tabelë_numër_i_plotë(Kartelë * 72 + 64, Memorie_sistemi_i_skedarëve.ndryshoj_përmasat_Listë[Kartelë]);
            shkruaj_tabelë_numër_i_plotë(Kartelë * 72 + 68, Memorie_sistemi_i_skedarëve.허가들[Kartelë]);
        }
        int hash_skedar = 0x811c9dc5;
        for (int seksion_VALUE = 0; seksion_VALUE < 258; seksion_VALUE++) {
            for (int hapësirë_për_tekst_futje = 0; hapësirë_për_tekst_futje < 512; hapësirë_për_tekst_futje++) {
                int VALUE = 0;
                if (seksion_VALUE < 2) VALUE = skedar_tabelë[seksion_VALUE * 512 + hapësirë_për_tekst_futje];
                else {
                    int Kartelë = (seksion_VALUE - 2) / 32, Pozicioni = (seksion_VALUE - 2) % 32 * 512 + hapësirë_për_tekst_futje;
                    if (skedar_tabelë[Kartelë * 72] != 0 && Pozicioni < Memorie_sistemi_i_skedarëve.ndryshoj_përmasat_Listë[Kartelë])
                        VALUE = pajisje_VALUE.기억읽기(pajisje_VALUE.skedar_Memorie() + Kartelë * 16384 + Pozicioni);
                }
                hapësira_ruajtëse_pajisje_lidhje.seksion_të_dhëna[hapësirë_për_tekst_futje] = VALUE; hash_skedar = 바이트해시(hash_skedar, VALUE);
            }
            if (hapësira_ruajtëse_pajisje_lidhje.Shkrimi(nis_seksion + 1 + seksion_VALUE) < 0) return -5;
        }
        if (hapësira_ruajtëse_pajisje_lidhje.밀어쓰기() < 0) return -5;
        pastroj_të_dhëna(); hapësira_ruajtëse_pajisje_lidhje.shkruaj_numër_i_plotë_VALUE(0, 0x4a4b534e);
        hapësira_ruajtëse_pajisje_lidhje.shkruaj_numër_i_plotë_VALUE(4, 세대번호 + 1); hapësira_ruajtëse_pajisje_lidhje.shkruaj_numër_i_plotë_VALUE(8, hash_skedar);
        hapësira_ruajtëse_pajisje_lidhje.shkruaj_numër_i_plotë_VALUE(12, (세대번호 + 1) ^ hash_skedar ^ 0x4a4b534e);
        if (hapësira_ruajtëse_pajisje_lidhje.Shkrimi(nis_seksion) < 0 || hapësira_ruajtëse_pajisje_lidhje.밀어쓰기() < 0) return -5;
        현재보존본 = Tjetër_njësi; 세대번호++;
        return 0;
    }
}
