// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Les 전용 Utfør_kommando 묶음의 ELF32 bekrefte, Argument Fram_VALUE, 한 번에 한 brukar Prosess_VALUE Utfør_kommando. */
public final class 실행관리 {
    static final int START_brukar_app = 0x04000000;
    static final int brukar_avslutte = 0x04400000;
    static final int IMAGE_avslutte_ADDRESS = 0x04200000;
    static final int argument_START = 0x04300000;
    static int argument_COUNT = 0;
    static int[] argument_ADDRESS = new int[16];

    static boolean klipp(int ADDRESS, int lengd_VALUE) {
        return ADDRESS >= START_brukar_app && ADDRESS < brukar_avslutte && lengd_VALUE >= 0 && lengd_VALUE <= brukar_avslutte - ADDRESS;
    }

    static int 수(int ADDRESS) { return 기억공간.dele_opp_heiltal(ADDRESS); }
    static int 짧은수(int ADDRESS) { return mobil_VALUE.기억읽기(ADDRESS) | mobil_VALUE.기억읽기(ADDRESS + 1) << 8; }
    static void 수쓰기(int ADDRESS, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) mobil_VALUE.skrive_Minne(ADDRESS + INDEX, VALUE >>> (INDEX * 8));
    }

    static int gruppe_COUNT() {
        int ADDRESS = mobil_VALUE.실행묶음();
        int Storleik = mobil_VALUE.실행묶음크기();
        if (Storleik < 8 || 수(ADDRESS) != 0x50414b4a) return 0;
        int vare_COUNT = 수(ADDRESS + 4);
        return vare_COUNT >= 0 && vare_COUNT <= 32 && vare_COUNT <= (Storleik - 8) / 24 ? vare_COUNT : 0;
    }

    static void oppføring_Liste() {
        for (int INDEX = 0; INDEX < gruppe_COUNT(); INDEX++) {
            int oppføring_VALUE = mobil_VALUE.실행묶음() + 8 + INDEX * 24;
            for (int teikn_VALUE = 0; teikn_VALUE < 16 && mobil_VALUE.기억읽기(oppføring_VALUE + teikn_VALUE) != 0; teikn_VALUE++)
                SMS_Terminal.문자(mobil_VALUE.기억읽기(oppføring_VALUE + teikn_VALUE));
            SMS_Terminal.Skriv("\n");
        }
    }

    static int Søk_oppføring(int[] 입력, int Køyr_2, int lengd_VALUE) {
        if (lengd_VALUE <= 0 || lengd_VALUE >= 16) return 0;
        for (int INDEX = 0; INDEX < gruppe_COUNT(); INDEX++) {
            int oppføring_VALUE = mobil_VALUE.실행묶음() + 8 + INDEX * 24;
            boolean 같음 = mobil_VALUE.기억읽기(oppføring_VALUE + lengd_VALUE) == 0;
            for (int teikn_VALUE = 0; teikn_VALUE < lengd_VALUE; teikn_VALUE++)
                if (입력[Køyr_2 + teikn_VALUE] != mobil_VALUE.기억읽기(oppføring_VALUE + teikn_VALUE)) 같음 = false;
            if (같음) return oppføring_VALUE;
        }
        return 0;
    }

    static int bekrefte(int Fil, int lengd_VALUE) {
        if (lengd_VALUE < 52 || 수(Fil) != 0x464c457f || mobil_VALUE.기억읽기(Fil + 4) != 1
            || mobil_VALUE.기억읽기(Fil + 5) != 1 || mobil_VALUE.기억읽기(Fil + 6) != 1
            || 짧은수(Fil + 16) != 2 || 짧은수(Fil + 18) != 3 || 수(Fil + 20) != 1
            || 짧은수(Fil + 40) != 52 || 짧은수(Fil + 42) != 32) return -8;
        int oppføring_p_VALUE = 수(Fil + 24);
        int tabell_plassere = 수(Fil + 28);
        int vare_COUNT = 짧은수(Fil + 44);
        if (vare_COUNT == 0 || vare_COUNT > 16 || tabell_plassere < 52 || tabell_plassere > lengd_VALUE - vare_COUNT * 32) return -8;
        boolean 실행가능 = false;
        for (int INDEX = 0; INDEX < vare_COUNT; INDEX++) {
            int LOOKUP_tabell = Fil + tabell_plassere + INDEX * 32;
            int 종류 = 수(LOOKUP_tabell);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Kopla_til/해석기 미지원
            if (종류 != 1) continue;
            int Posisjon = 수(LOOKUP_tabell + 4), ADDRESS = 수(LOOKUP_tabell + 8), fil_endre_storleik = 수(LOOKUP_tabell + 16), Minne_endre_storleik = 수(LOOKUP_tabell + 20);
            int justere_VALUE = 수(LOOKUP_tabell + 28);
            if (ADDRESS < START_brukar_app || ADDRESS >= IMAGE_avslutte_ADDRESS || Minne_endre_storleik < 0 || Minne_endre_storleik > IMAGE_avslutte_ADDRESS - ADDRESS
                || fil_endre_storleik < 0 || fil_endre_storleik > Minne_endre_storleik || Posisjon < 0 || (fil_endre_storleik > 0 && Posisjon > lengd_VALUE - fil_endre_storleik)
                || (justere_VALUE != 0 && (justere_VALUE < 0 || (justere_VALUE & (justere_VALUE - 1)) != 0
                    || ((ADDRESS - Posisjon) & (justere_VALUE - 1)) != 0))) return -8;
            for (int 앞 = 0; 앞 < INDEX; 앞++) {
                int 이전 = Fil + tabell_plassere + 앞 * 32;
                if (수(이전) == 1 && Minne_endre_storleik > 0 && 수(이전 + 20) > 0
                    && ADDRESS < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < ADDRESS + Minne_endre_storleik) return -8;
            }
            if ((수(LOOKUP_tabell + 24) & 1) != 0 && oppføring_p_VALUE >= ADDRESS && oppføring_p_VALUE - ADDRESS < fil_endre_storleik) 실행가능 = true;
        }
        return 실행가능 ? oppføring_p_VALUE : -8;
    }

    static int Utfør_kommando(int[] 입력, int Køyr_2, int lengd_VALUE) {
        while (Køyr_2 < lengd_VALUE && 입력[Køyr_2] == ' ') Køyr_2++;
        int 끝 = Køyr_2;
        while (끝 < lengd_VALUE && 입력[끝] != ' ') 끝++;
        int oppføring_VALUE = Søk_oppføring(입력, Køyr_2, 끝 - Køyr_2);
        if (oppføring_VALUE == 0) return -2;
        int Posisjon = 수(oppføring_VALUE + 16), Storleik = 수(oppføring_VALUE + 20);
        if (Posisjon < 8 + gruppe_COUNT() * 24 || Storleik < 52 || Posisjon > mobil_VALUE.실행묶음크기() - Storleik) return -8;
        int Fil = mobil_VALUE.실행묶음() + Posisjon;
        int oppføring_p_VALUE = bekrefte(Fil, Storleik);
        if (oppføring_p_VALUE < 0) return oppføring_p_VALUE;
        mobil_VALUE.brukar_fjerne_Innhald();
        int tabell_plassere = 수(Fil + 28), vare_COUNT = 짧은수(Fil + 44);
        for (int INDEX = 0; INDEX < vare_COUNT; INDEX++) {
            int LOOKUP_tabell = Fil + tabell_plassere + INDEX * 32;
            if (수(LOOKUP_tabell) != 1) continue;
            int 원본 = Fil + 수(LOOKUP_tabell + 4), mål_VALUE = 수(LOOKUP_tabell + 8), fil_endre_storleik = 수(LOOKUP_tabell + 16);
            for (int byte_VALUE = 0; byte_VALUE < fil_endre_storleik; byte_VALUE++) mobil_VALUE.skrive_Minne(mål_VALUE + byte_VALUE, mobil_VALUE.기억읽기(원본 + byte_VALUE));
        }
        argument_COUNT = 0;
        int Store_VALUE = argument_START;
        while (끝 < lengd_VALUE) {
            while (끝 < lengd_VALUE && 입력[끝] == ' ') 끝++;
            if (끝 == lengd_VALUE) break;
            if (argument_COUNT == argument_ADDRESS.length) return -22;
            Køyr_2 = 끝;
            while (끝 < lengd_VALUE && 입력[끝] != ' ') 끝++;
            argument_ADDRESS[argument_COUNT++] = Store_VALUE;
            수쓰기(Store_VALUE, 끝 - Køyr_2);
            for (int teikn_VALUE = Køyr_2; teikn_VALUE < 끝; teikn_VALUE++) 수쓰기(Store_VALUE + 4 + (teikn_VALUE - Køyr_2) * 4, 입력[teikn_VALUE]);
            Store_VALUE += 4 + (끝 - Køyr_2) * 4;
        }
        Nettverk_Stabel.CLEAN_Prosess();
        파일서술자관리.START_Prosess();
        int forretningsmål = mobil_VALUE.køyre_brukar_app(oppføring_p_VALUE, brukar_avslutte - 16);
        파일서술자관리.CLEAN_Prosess();
        Nettverk_Stabel.CLEAN_Prosess();
        return forretningsmål;
    }
}
