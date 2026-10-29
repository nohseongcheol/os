// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Lasīt 전용 Izpildīt_komanda 묶음의 ELF32 validēt, Parametri pārsūtīt_VALUE, 한 번에 한 lietotājs Process_VALUE Izpildīt_komanda. */
public final class 실행관리 {
    static final int Sākt_lietotājs_programma = 0x04000000;
    static final int lietotājs_beigt_zvanu = 0x04400000;
    static final int IMAGE_beigt_zvanu_adrese = 0x04200000;
    static final int arg_Sākt = 0x04300000;
    static int arg_COUNT = 0;
    static int[] arg_adrese = new int[16];

    static boolean klips(int adrese, int 길이) {
        return adrese >= Sākt_lietotājs_programma && adrese < lietotājs_beigt_zvanu && 길이 >= 0 && 길이 <= lietotājs_beigt_zvanu - adrese;
    }

    static int numurs(int adrese) { return atmiņa_reģions.parsēt_vesels_skaitlis(adrese); }
    static int 짧은수(int adrese) { return ierīce_VALUE.기억읽기(adrese) | ierīce_VALUE.기억읽기(adrese + 1) << 8; }
    static void rakstīšana_numurs(int adrese, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) ierīce_VALUE.rakstīšana_atmiņa(adrese + INDEX, VALUE >>> (INDEX * 8));
    }

    static int Grupa_COUNT() {
        int adrese = ierīce_VALUE.izpildāms_fails_saistīt();
        int Izmērs = ierīce_VALUE.izpildāms_fails_saistīt_mainīt_izmērus();
        if (Izmērs < 8 || numurs(adrese) != 0x50414b4a) return 0;
        int krājums_COUNT = numurs(adrese + 4);
        return krājums_COUNT >= 0 && krājums_COUNT <= 32 && krājums_COUNT <= (Izmērs - 8) / 24 ? krājums_COUNT : 0;
    }

    static void ievade_Saraksts() {
        for (int INDEX = 0; INDEX < Grupa_COUNT(); INDEX++) {
            int ievade_VALUE = ierīce_VALUE.izpildāms_fails_saistīt() + 8 + INDEX * 24;
            for (int rakstzīme_VALUE = 0; rakstzīme_VALUE < 16 && ierīce_VALUE.기억읽기(ievade_VALUE + rakstzīme_VALUE) != 0; rakstzīme_VALUE++)
                SMS_Terminālis.문자(ierīce_VALUE.기억읽기(ievade_VALUE + rakstzīme_VALUE));
            SMS_Terminālis.Rakstīt("\n");
        }
    }

    static int FIND_ievade(int[] 입력, int Palaist, int 길이) {
        if (길이 <= 0 || 길이 >= 16) return 0;
        for (int INDEX = 0; INDEX < Grupa_COUNT(); INDEX++) {
            int ievade_VALUE = ierīce_VALUE.izpildāms_fails_saistīt() + 8 + INDEX * 24;
            boolean 같음 = ierīce_VALUE.기억읽기(ievade_VALUE + 길이) == 0;
            for (int rakstzīme_VALUE = 0; rakstzīme_VALUE < 길이; rakstzīme_VALUE++)
                if (입력[Palaist + rakstzīme_VALUE] != ierīce_VALUE.기억읽기(ievade_VALUE + rakstzīme_VALUE)) 같음 = false;
            if (같음) return ievade_VALUE;
        }
        return 0;
    }

    static int validēt(int Fails, int 길이) {
        if (길이 < 52 || numurs(Fails) != 0x464c457f || ierīce_VALUE.기억읽기(Fails + 4) != 1
            || ierīce_VALUE.기억읽기(Fails + 5) != 1 || ierīce_VALUE.기억읽기(Fails + 6) != 1
            || 짧은수(Fails + 16) != 2 || 짧은수(Fails + 18) != 3 || numurs(Fails + 20) != 1
            || 짧은수(Fails + 40) != 52 || 짧은수(Fails + 42) != 32) return -8;
        int ieejas_punkts_VALUE = numurs(Fails + 24);
        int tabula_amats = numurs(Fails + 28);
        int krājums_COUNT = 짧은수(Fails + 44);
        if (krājums_COUNT == 0 || krājums_COUNT > 16 || tabula_amats < 52 || tabula_amats > 길이 - krājums_COUNT * 32) return -8;
        boolean informācijas_tehnoloģija_izpildāms_fails = false;
        for (int INDEX = 0; INDEX < krājums_COUNT; INDEX++) {
            int LOOKUP_tabula = Fails + tabula_amats + INDEX * 32;
            int 종류 = numurs(LOOKUP_tabula);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Savienoties/parsētājs_48ee4b1b 미지원
            if (종류 != 1) continue;
            int Novietojums = numurs(LOOKUP_tabula + 4), adrese = numurs(LOOKUP_tabula + 8), faila_lielums = numurs(LOOKUP_tabula + 16), atmiņa_mainīt_izmērus = numurs(LOOKUP_tabula + 20);
            int līdzināt_VALUE = numurs(LOOKUP_tabula + 28);
            if (adrese < Sākt_lietotājs_programma || adrese >= IMAGE_beigt_zvanu_adrese || atmiņa_mainīt_izmērus < 0 || atmiņa_mainīt_izmērus > IMAGE_beigt_zvanu_adrese - adrese
                || faila_lielums < 0 || faila_lielums > atmiņa_mainīt_izmērus || Novietojums < 0 || (faila_lielums > 0 && Novietojums > 길이 - faila_lielums)
                || (līdzināt_VALUE != 0 && (līdzināt_VALUE < 0 || (līdzināt_VALUE & (līdzināt_VALUE - 1)) != 0
                    || ((adrese - Novietojums) & (līdzināt_VALUE - 1)) != 0))) return -8;
            for (int priekšējā_VALUE = 0; priekšējā_VALUE < INDEX; priekšējā_VALUE++) {
                int 이전 = Fails + tabula_amats + priekšējā_VALUE * 32;
                if (numurs(이전) == 1 && atmiņa_mainīt_izmērus > 0 && numurs(이전 + 20) > 0
                    && adrese < numurs(이전 + 8) + numurs(이전 + 20) && numurs(이전 + 8) < adrese + atmiņa_mainīt_izmērus) return -8;
            }
            if ((numurs(LOOKUP_tabula + 24) & 1) != 0 && ieejas_punkts_VALUE >= adrese && ieejas_punkts_VALUE - adrese < faila_lielums) informācijas_tehnoloģija_izpildāms_fails = true;
        }
        return informācijas_tehnoloģija_izpildāms_fails ? ieejas_punkts_VALUE : -8;
    }

    static int Izpildīt_komanda(int[] 입력, int Palaist, int 길이) {
        while (Palaist < 길이 && 입력[Palaist] == ' ') Palaist++;
        int 끝 = Palaist;
        while (끝 < 길이 && 입력[끝] != ' ') 끝++;
        int ievade_VALUE = FIND_ievade(입력, Palaist, 끝 - Palaist);
        if (ievade_VALUE == 0) return -2;
        int Novietojums = numurs(ievade_VALUE + 16), Izmērs = numurs(ievade_VALUE + 20);
        if (Novietojums < 8 + Grupa_COUNT() * 24 || Izmērs < 52 || Novietojums > ierīce_VALUE.izpildāms_fails_saistīt_mainīt_izmērus() - Izmērs) return -8;
        int Fails = ierīce_VALUE.izpildāms_fails_saistīt() + Novietojums;
        int ieejas_punkts_VALUE = validēt(Fails, Izmērs);
        if (ieejas_punkts_VALUE < 0) return ieejas_punkts_VALUE;
        ierīce_VALUE.lietotājs_nodzēst_Satura_rādītājs();
        int tabula_amats = numurs(Fails + 28), krājums_COUNT = 짧은수(Fails + 44);
        for (int INDEX = 0; INDEX < krājums_COUNT; INDEX++) {
            int LOOKUP_tabula = Fails + tabula_amats + INDEX * 32;
            if (numurs(LOOKUP_tabula) != 1) continue;
            int 원본 = Fails + numurs(LOOKUP_tabula + 4), mērķis_VALUE = numurs(LOOKUP_tabula + 8), faila_lielums = numurs(LOOKUP_tabula + 16);
            for (int byte_VALUE = 0; byte_VALUE < faila_lielums; byte_VALUE++) ierīce_VALUE.rakstīšana_atmiņa(mērķis_VALUE + byte_VALUE, ierīce_VALUE.기억읽기(원본 + byte_VALUE));
        }
        arg_COUNT = 0;
        int Store_VALUE = arg_Sākt;
        while (끝 < 길이) {
            while (끝 < 길이 && 입력[끝] == ' ') 끝++;
            if (끝 == 길이) break;
            if (arg_COUNT == arg_adrese.length) return -22;
            Palaist = 끝;
            while (끝 < 길이 && 입력[끝] != ' ') 끝++;
            arg_adrese[arg_COUNT++] = Store_VALUE;
            rakstīšana_numurs(Store_VALUE, 끝 - Palaist);
            for (int rakstzīme_VALUE = Palaist; rakstzīme_VALUE < 끝; rakstzīme_VALUE++) rakstīšana_numurs(Store_VALUE + 4 + (rakstzīme_VALUE - Palaist) * 4, 입력[rakstzīme_VALUE]);
            Store_VALUE += 4 + (끝 - Palaist) * 4;
        }
        tīkls_kopa.CLEAN_Process();
        파일서술자관리.Sākt_Process();
        int mērs = ierīce_VALUE.virkne_lietotājs_programma(ieejas_punkts_VALUE, lietotājs_beigt_zvanu - 16);
        파일서술자관리.CLEAN_Process();
        tīkls_kopa.CLEAN_Process();
        return mērs;
    }
}
