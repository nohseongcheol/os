// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Skaitymas 전용 Vykdyti_komanda 묶음의 ELF32 tikrinti, Argumentai Pirmyn_VALUE, 한 번에 한 naudotojas Procesas_VALUE Vykdyti_komanda. */
public final class 실행관리 {
    static final int Start_naudotojas_programa = 0x04000000;
    static final int naudotojas_baigti_pokalbį = 0x04400000;
    static final int IMAGE_baigti_pokalbį_ADDRESS = 0x04200000;
    static final int argumentas_Start = 0x04300000;
    static int argumentas_COUNT = 0;
    static int[] argumentas_ADDRESS = new int[16];

    static boolean klipas(int ADDRESS, int 길이) {
        return ADDRESS >= Start_naudotojas_programa && ADDRESS < naudotojas_baigti_pokalbį && 길이 >= 0 && 길이 <= naudotojas_baigti_pokalbį - ADDRESS;
    }

    static int numeris(int ADDRESS) { return atmintis_sritis.analizuoti_sintaksę_sveikasis_skaičius(ADDRESS); }
    static int 짧은수(int ADDRESS) { return įrenginys_VALUE.기억읽기(ADDRESS) | įrenginys_VALUE.기억읽기(ADDRESS + 1) << 8; }
    static void rašymas_numeris(int ADDRESS, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) įrenginys_VALUE.rašymas_atmintis(ADDRESS + INDEX, VALUE >>> (INDEX * 8));
    }

    static int Grupė_COUNT() {
        int ADDRESS = įrenginys_VALUE.실행묶음();
        int Dydis = įrenginys_VALUE.실행묶음크기();
        if (Dydis < 8 || numeris(ADDRESS) != 0x50414b4a) return 0;
        int prekė_COUNT = numeris(ADDRESS + 4);
        return prekė_COUNT >= 0 && prekė_COUNT <= 32 && prekė_COUNT <= (Dydis - 8) / 24 ? prekė_COUNT : 0;
    }

    static void įrašas_Sąrašas() {
        for (int INDEX = 0; INDEX < Grupė_COUNT(); INDEX++) {
            int įrašas_VALUE = įrenginys_VALUE.실행묶음() + 8 + INDEX * 24;
            for (int simbolis_VALUE_068c2631 = 0; simbolis_VALUE_068c2631 < 16 && įrenginys_VALUE.기억읽기(įrašas_VALUE + simbolis_VALUE_068c2631) != 0; simbolis_VALUE_068c2631++)
                SMS_Terminalas.문자(įrenginys_VALUE.기억읽기(įrašas_VALUE + simbolis_VALUE_068c2631));
            SMS_Terminalas.Rašymas("\n");
        }
    }

    static int FIND_įrašas(int[] 입력, int Paleisti, int 길이) {
        if (길이 <= 0 || 길이 >= 16) return 0;
        for (int INDEX = 0; INDEX < Grupė_COUNT(); INDEX++) {
            int įrašas_VALUE = įrenginys_VALUE.실행묶음() + 8 + INDEX * 24;
            boolean 같음 = įrenginys_VALUE.기억읽기(įrašas_VALUE + 길이) == 0;
            for (int simbolis_VALUE_068c2631 = 0; simbolis_VALUE_068c2631 < 길이; simbolis_VALUE_068c2631++)
                if (입력[Paleisti + simbolis_VALUE_068c2631] != įrenginys_VALUE.기억읽기(įrašas_VALUE + simbolis_VALUE_068c2631)) 같음 = false;
            if (같음) return įrašas_VALUE;
        }
        return 0;
    }

    static int tikrinti(int Failas, int 길이) {
        if (길이 < 52 || numeris(Failas) != 0x464c457f || įrenginys_VALUE.기억읽기(Failas + 4) != 1
            || įrenginys_VALUE.기억읽기(Failas + 5) != 1 || įrenginys_VALUE.기억읽기(Failas + 6) != 1
            || 짧은수(Failas + 16) != 2 || 짧은수(Failas + 18) != 3 || numeris(Failas + 20) != 1
            || 짧은수(Failas + 40) != 52 || 짧은수(Failas + 42) != 32) return -8;
        int įrašas_p_VALUE = numeris(Failas + 24);
        int lentelė_padėtis = numeris(Failas + 28);
        int prekė_COUNT = 짧은수(Failas + 44);
        if (prekė_COUNT == 0 || prekė_COUNT > 16 || lentelė_padėtis < 52 || lentelė_padėtis > 길이 - prekė_COUNT * 32) return -8;
        boolean 실행가능 = false;
        for (int INDEX = 0; INDEX < prekė_COUNT; INDEX++) {
            int LOOKUP_lentelė = Failas + lentelė_padėtis + INDEX * 32;
            int 종류 = numeris(LOOKUP_lentelė);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Prisijungti/analizatorius_48ee4b1b 미지원
            if (종류 != 1) continue;
            int Pozicija = numeris(LOOKUP_lentelė + 4), ADDRESS = numeris(LOOKUP_lentelė + 8), failo_dydis = numeris(LOOKUP_lentelė + 16), atmintis_dydis = numeris(LOOKUP_lentelė + 20);
            int lygiuoti_VALUE = numeris(LOOKUP_lentelė + 28);
            if (ADDRESS < Start_naudotojas_programa || ADDRESS >= IMAGE_baigti_pokalbį_ADDRESS || atmintis_dydis < 0 || atmintis_dydis > IMAGE_baigti_pokalbį_ADDRESS - ADDRESS
                || failo_dydis < 0 || failo_dydis > atmintis_dydis || Pozicija < 0 || (failo_dydis > 0 && Pozicija > 길이 - failo_dydis)
                || (lygiuoti_VALUE != 0 && (lygiuoti_VALUE < 0 || (lygiuoti_VALUE & (lygiuoti_VALUE - 1)) != 0
                    || ((ADDRESS - Pozicija) & (lygiuoti_VALUE - 1)) != 0))) return -8;
            for (int priekinis_VALUE = 0; priekinis_VALUE < INDEX; priekinis_VALUE++) {
                int 이전 = Failas + lentelė_padėtis + priekinis_VALUE * 32;
                if (numeris(이전) == 1 && atmintis_dydis > 0 && numeris(이전 + 20) > 0
                    && ADDRESS < numeris(이전 + 8) + numeris(이전 + 20) && numeris(이전 + 8) < ADDRESS + atmintis_dydis) return -8;
            }
            if ((numeris(LOOKUP_lentelė + 24) & 1) != 0 && įrašas_p_VALUE >= ADDRESS && įrašas_p_VALUE - ADDRESS < failo_dydis) 실행가능 = true;
        }
        return 실행가능 ? įrašas_p_VALUE : -8;
    }

    static int Vykdyti_komanda(int[] 입력, int Paleisti, int 길이) {
        while (Paleisti < 길이 && 입력[Paleisti] == ' ') Paleisti++;
        int 끝 = Paleisti;
        while (끝 < 길이 && 입력[끝] != ' ') 끝++;
        int įrašas_VALUE = FIND_įrašas(입력, Paleisti, 끝 - Paleisti);
        if (įrašas_VALUE == 0) return -2;
        int Pozicija = numeris(įrašas_VALUE + 16), Dydis = numeris(įrašas_VALUE + 20);
        if (Pozicija < 8 + Grupė_COUNT() * 24 || Dydis < 52 || Pozicija > įrenginys_VALUE.실행묶음크기() - Dydis) return -8;
        int Failas = įrenginys_VALUE.실행묶음() + Pozicija;
        int įrašas_p_VALUE = tikrinti(Failas, Dydis);
        if (įrašas_p_VALUE < 0) return įrašas_p_VALUE;
        įrenginys_VALUE.naudotojas_apmokėti_Turinys();
        int lentelė_padėtis = numeris(Failas + 28), prekė_COUNT = 짧은수(Failas + 44);
        for (int INDEX = 0; INDEX < prekė_COUNT; INDEX++) {
            int LOOKUP_lentelė = Failas + lentelė_padėtis + INDEX * 32;
            if (numeris(LOOKUP_lentelė) != 1) continue;
            int 원본 = Failas + numeris(LOOKUP_lentelė + 4), vieta_VALUE = numeris(LOOKUP_lentelė + 8), failo_dydis = numeris(LOOKUP_lentelė + 16);
            for (int baitas_VALUE = 0; baitas_VALUE < failo_dydis; baitas_VALUE++) įrenginys_VALUE.rašymas_atmintis(vieta_VALUE + baitas_VALUE, įrenginys_VALUE.기억읽기(원본 + baitas_VALUE));
        }
        argumentas_COUNT = 0;
        int Store_VALUE = argumentas_Start;
        while (끝 < 길이) {
            while (끝 < 길이 && 입력[끝] == ' ') 끝++;
            if (끝 == 길이) break;
            if (argumentas_COUNT == argumentas_ADDRESS.length) return -22;
            Paleisti = 끝;
            while (끝 < 길이 && 입력[끝] != ' ') 끝++;
            argumentas_ADDRESS[argumentas_COUNT++] = Store_VALUE;
            rašymas_numeris(Store_VALUE, 끝 - Paleisti);
            for (int simbolis_VALUE_068c2631 = Paleisti; simbolis_VALUE_068c2631 < 끝; simbolis_VALUE_068c2631++) rašymas_numeris(Store_VALUE + 4 + (simbolis_VALUE_068c2631 - Paleisti) * 4, 입력[simbolis_VALUE_068c2631]);
            Store_VALUE += 4 + (끝 - Paleisti) * 4;
        }
        tinklas_eilė.CLEAN_Procesas();
        파일서술자관리.Start_Procesas();
        int REZULTATAS = įrenginys_VALUE.vykdyti_naudotojas_programa(įrašas_p_VALUE, naudotojas_baigti_pokalbį - 16);
        파일서술자관리.CLEAN_Procesas();
        tinklas_eilė.CLEAN_Procesas();
        return REZULTATAS;
    }
}
