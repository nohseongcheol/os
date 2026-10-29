// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Lestur 전용 keyra_skipun 묶음의 ELF32 staðfesta, Viðföng Áfram_VALUE, 한 번에 한 notandi Ferli_VALUE keyra_skipun. */
public final class 실행관리 {
    static final int Opna_notandi_forrit = 0x04000000;
    static final int notandi_ljúka = 0x04400000;
    static final int mynd_ljúka_slóð = 0x04200000;
    static final int frumbreyta_Opna = 0x04300000;
    static int frumbreyta_COUNT = 0;
    static int[] frumbreyta_slóð = new int[16];

    static boolean miðlaskrá(int slóð, int lengd_VALUE) {
        return slóð >= Opna_notandi_forrit && slóð < notandi_ljúka && lengd_VALUE >= 0 && lengd_VALUE <= notandi_ljúka - slóð;
    }

    static int númer(int slóð) { return 기억공간.þátta_heiltala(slóð); }
    static int 짧은수(int slóð) { return tæki_VALUE.기억읽기(slóð) | tæki_VALUE.기억읽기(slóð + 1) << 8; }
    static void skrifa_númer(int slóð, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) tæki_VALUE.skrifa_Minni(slóð + INDEX, VALUE >>> (INDEX * 8));
    }

    static int Hópur_COUNT() {
        int slóð = tæki_VALUE.실행묶음();
        int Stærð = tæki_VALUE.실행묶음크기();
        if (Stærð < 8 || númer(slóð) != 0x50414b4a) return 0;
        int vara_COUNT = númer(slóð + 4);
        return vara_COUNT >= 0 && vara_COUNT <= 32 && vara_COUNT <= (Stærð - 8) / 24 ? vara_COUNT : 0;
    }

    static void færsla_Listi() {
        for (int INDEX = 0; INDEX < Hópur_COUNT(); INDEX++) {
            int færsla_VALUE = tæki_VALUE.실행묶음() + 8 + INDEX * 24;
            for (int stafur_VALUE = 0; stafur_VALUE < 16 && tæki_VALUE.기억읽기(færsla_VALUE + stafur_VALUE) != 0; stafur_VALUE++)
                SMS_Endastöð.문자(tæki_VALUE.기억읽기(færsla_VALUE + stafur_VALUE));
            SMS_Endastöð.Skrift("\n");
        }
    }

    static int FIND_færsla(int[] 입력, int Keyra_2, int lengd_VALUE) {
        if (lengd_VALUE <= 0 || lengd_VALUE >= 16) return 0;
        for (int INDEX = 0; INDEX < Hópur_COUNT(); INDEX++) {
            int færsla_VALUE = tæki_VALUE.실행묶음() + 8 + INDEX * 24;
            boolean 같음 = tæki_VALUE.기억읽기(færsla_VALUE + lengd_VALUE) == 0;
            for (int stafur_VALUE = 0; stafur_VALUE < lengd_VALUE; stafur_VALUE++)
                if (입력[Keyra_2 + stafur_VALUE] != tæki_VALUE.기억읽기(færsla_VALUE + stafur_VALUE)) 같음 = false;
            if (같음) return færsla_VALUE;
        }
        return 0;
    }

    static int staðfesta(int Skrá, int lengd_VALUE) {
        if (lengd_VALUE < 52 || númer(Skrá) != 0x464c457f || tæki_VALUE.기억읽기(Skrá + 4) != 1
            || tæki_VALUE.기억읽기(Skrá + 5) != 1 || tæki_VALUE.기억읽기(Skrá + 6) != 1
            || 짧은수(Skrá + 16) != 2 || 짧은수(Skrá + 18) != 3 || númer(Skrá + 20) != 1
            || 짧은수(Skrá + 40) != 52 || 짧은수(Skrá + 42) != 32) return -8;
        int færsla_P_VALUE = númer(Skrá + 24);
        int tafla_staða = númer(Skrá + 28);
        int vara_COUNT = 짧은수(Skrá + 44);
        if (vara_COUNT == 0 || vara_COUNT > 16 || tafla_staða < 52 || tafla_staða > lengd_VALUE - vara_COUNT * 32) return -8;
        boolean 실행가능 = false;
        for (int INDEX = 0; INDEX < vara_COUNT; INDEX++) {
            int LOOKUP_tafla = Skrá + tafla_staða + INDEX * 32;
            int 종류 = númer(LOOKUP_tafla);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Tengjast/þáttari_48ee4b1b 미지원
            if (종류 != 1) continue;
            int Staðsetning = númer(LOOKUP_tafla + 4), slóð = númer(LOOKUP_tafla + 8), skrá_breyta_stærð = númer(LOOKUP_tafla + 16), Minni_breyta_stærð = númer(LOOKUP_tafla + 20);
            int stilla_VALUE = númer(LOOKUP_tafla + 28);
            if (slóð < Opna_notandi_forrit || slóð >= mynd_ljúka_slóð || Minni_breyta_stærð < 0 || Minni_breyta_stærð > mynd_ljúka_slóð - slóð
                || skrá_breyta_stærð < 0 || skrá_breyta_stærð > Minni_breyta_stærð || Staðsetning < 0 || (skrá_breyta_stærð > 0 && Staðsetning > lengd_VALUE - skrá_breyta_stærð)
                || (stilla_VALUE != 0 && (stilla_VALUE < 0 || (stilla_VALUE & (stilla_VALUE - 1)) != 0
                    || ((slóð - Staðsetning) & (stilla_VALUE - 1)) != 0))) return -8;
            for (int myndavél_að_framan_VALUE = 0; myndavél_að_framan_VALUE < INDEX; myndavél_að_framan_VALUE++) {
                int 이전 = Skrá + tafla_staða + myndavél_að_framan_VALUE * 32;
                if (númer(이전) == 1 && Minni_breyta_stærð > 0 && númer(이전 + 20) > 0
                    && slóð < númer(이전 + 8) + númer(이전 + 20) && númer(이전 + 8) < slóð + Minni_breyta_stærð) return -8;
            }
            if ((númer(LOOKUP_tafla + 24) & 1) != 0 && færsla_P_VALUE >= slóð && færsla_P_VALUE - slóð < skrá_breyta_stærð) 실행가능 = true;
        }
        return 실행가능 ? færsla_P_VALUE : -8;
    }

    static int keyra_skipun(int[] 입력, int Keyra_2, int lengd_VALUE) {
        while (Keyra_2 < lengd_VALUE && 입력[Keyra_2] == ' ') Keyra_2++;
        int 끝 = Keyra_2;
        while (끝 < lengd_VALUE && 입력[끝] != ' ') 끝++;
        int færsla_VALUE = FIND_færsla(입력, Keyra_2, 끝 - Keyra_2);
        if (færsla_VALUE == 0) return -2;
        int Staðsetning = númer(færsla_VALUE + 16), Stærð = númer(færsla_VALUE + 20);
        if (Staðsetning < 8 + Hópur_COUNT() * 24 || Stærð < 52 || Staðsetning > tæki_VALUE.실행묶음크기() - Stærð) return -8;
        int Skrá = tæki_VALUE.실행묶음() + Staðsetning;
        int færsla_P_VALUE = staðfesta(Skrá, Stærð);
        if (færsla_P_VALUE < 0) return færsla_P_VALUE;
        tæki_VALUE.notandi_hreinsa_Innihald();
        int tafla_staða = númer(Skrá + 28), vara_COUNT = 짧은수(Skrá + 44);
        for (int INDEX = 0; INDEX < vara_COUNT; INDEX++) {
            int LOOKUP_tafla = Skrá + tafla_staða + INDEX * 32;
            if (númer(LOOKUP_tafla) != 1) continue;
            int 원본 = Skrá + númer(LOOKUP_tafla + 4), endastaður_VALUE = númer(LOOKUP_tafla + 8), skrá_breyta_stærð = númer(LOOKUP_tafla + 16);
            for (int bæti_VALUE = 0; bæti_VALUE < skrá_breyta_stærð; bæti_VALUE++) tæki_VALUE.skrifa_Minni(endastaður_VALUE + bæti_VALUE, tæki_VALUE.기억읽기(원본 + bæti_VALUE));
        }
        frumbreyta_COUNT = 0;
        int Store_VALUE = frumbreyta_Opna;
        while (끝 < lengd_VALUE) {
            while (끝 < lengd_VALUE && 입력[끝] == ' ') 끝++;
            if (끝 == lengd_VALUE) break;
            if (frumbreyta_COUNT == frumbreyta_slóð.length) return -22;
            Keyra_2 = 끝;
            while (끝 < lengd_VALUE && 입력[끝] != ' ') 끝++;
            frumbreyta_slóð[frumbreyta_COUNT++] = Store_VALUE;
            skrifa_númer(Store_VALUE, 끝 - Keyra_2);
            for (int stafur_VALUE = Keyra_2; stafur_VALUE < 끝; stafur_VALUE++) skrifa_númer(Store_VALUE + 4 + (stafur_VALUE - Keyra_2) * 4, 입력[stafur_VALUE]);
            Store_VALUE += 4 + (끝 - Keyra_2) * 4;
        }
        Net_bunki.CLEAN_Ferli();
        파일서술자관리.Opna_Ferli();
        int NIÐURSTAÐA = tæki_VALUE.runa_notandi_forrit(færsla_P_VALUE, notandi_ljúka - 16);
        파일서술자관리.CLEAN_Ferli();
        Net_bunki.CLEAN_Ferli();
        return NIÐURSTAÐA;
    }
}
