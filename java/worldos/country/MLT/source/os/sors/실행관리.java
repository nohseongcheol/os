// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 읽기 전용 eżegwixxa_kmand 묶음의 ELF32 vvalida, 인수 għadda_VALUE_24592b8a, 한 번에 한 utent Proċess_VALUE eżegwixxa_kmand. */
public final class 실행관리 {
    static final int Bidu_utent_programm = 0x04000000;
    static final int utent_ttermina = 0x04400000;
    static final int IMAGE_ttermina_ADDRESS = 0x04200000;
    static final int argument_Bidu = 0x04300000;
    static int argument_COUNT = 0;
    static int[] argument_ADDRESS = new int[16];

    static boolean klipp(int ADDRESS, int tul_VALUE) {
        return ADDRESS >= Bidu_utent_programm && ADDRESS < utent_ttermina && tul_VALUE >= 0 && tul_VALUE <= utent_ttermina - ADDRESS;
    }

    static int 수(int ADDRESS) { return 기억공간.analizza_numru_sħiħ(ADDRESS); }
    static int 짧은수(int ADDRESS) { return mowbajl_VALUE.기억읽기(ADDRESS) | mowbajl_VALUE.기억읽기(ADDRESS + 1) << 8; }
    static void 수쓰기(int ADDRESS, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) mowbajl_VALUE.kiteb_Memorja(ADDRESS + INDEX, VALUE >>> (INDEX * 8));
    }

    static int grupp_COUNT() {
        int ADDRESS = mowbajl_VALUE.실행묶음();
        int daqqas = mowbajl_VALUE.실행묶음크기();
        if (daqqas < 8 || 수(ADDRESS) != 0x50414b4a) return 0;
        int element_COUNT = 수(ADDRESS + 4);
        return element_COUNT >= 0 && element_COUNT <= 32 && element_COUNT <= (daqqas - 8) / 24 ? element_COUNT : 0;
    }

    static void entrata_Lista() {
        for (int INDEX = 0; INDEX < grupp_COUNT(); INDEX++) {
            int entrata_VALUE = mowbajl_VALUE.실행묶음() + 8 + INDEX * 24;
            for (int karattru_VALUE = 0; karattru_VALUE < 16 && mowbajl_VALUE.기억읽기(entrata_VALUE + karattru_VALUE) != 0; karattru_VALUE++)
                SMS_Terminal.문자(mowbajl_VALUE.기억읽기(entrata_VALUE + karattru_VALUE));
            SMS_Terminal.kiteb("\n");
        }
    }

    static int sab_entrata(int[] 입력, int serje, int tul_VALUE) {
        if (tul_VALUE <= 0 || tul_VALUE >= 16) return 0;
        for (int INDEX = 0; INDEX < grupp_COUNT(); INDEX++) {
            int entrata_VALUE = mowbajl_VALUE.실행묶음() + 8 + INDEX * 24;
            boolean 같음 = mowbajl_VALUE.기억읽기(entrata_VALUE + tul_VALUE) == 0;
            for (int karattru_VALUE = 0; karattru_VALUE < tul_VALUE; karattru_VALUE++)
                if (입력[serje + karattru_VALUE] != mowbajl_VALUE.기억읽기(entrata_VALUE + karattru_VALUE)) 같음 = false;
            if (같음) return entrata_VALUE;
        }
        return 0;
    }

    static int vvalida(int fajl, int tul_VALUE) {
        if (tul_VALUE < 52 || 수(fajl) != 0x464c457f || mowbajl_VALUE.기억읽기(fajl + 4) != 1
            || mowbajl_VALUE.기억읽기(fajl + 5) != 1 || mowbajl_VALUE.기억읽기(fajl + 6) != 1
            || 짧은수(fajl + 16) != 2 || 짧은수(fajl + 18) != 3 || 수(fajl + 20) != 1
            || 짧은수(fajl + 40) != 52 || 짧은수(fajl + 42) != 32) return -8;
        int entrata_punt_VALUE = 수(fajl + 24);
        int tabella_pożizzjoni = 수(fajl + 28);
        int element_COUNT = 짧은수(fajl + 44);
        if (element_COUNT == 0 || element_COUNT > 16 || tabella_pożizzjoni < 52 || tabella_pożizzjoni > tul_VALUE - element_COUNT * 32) return -8;
        boolean 실행가능 = false;
        for (int INDEX = 0; INDEX < element_COUNT; INDEX++) {
            int LOOKUP_tabella = fajl + tabella_pożizzjoni + INDEX * 32;
            int 종류 = 수(LOOKUP_tabella);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 AQBAD/해석기 미지원
            if (종류 != 1) continue;
            int pożizzjoni = 수(LOOKUP_tabella + 4), ADDRESS = 수(LOOKUP_tabella + 8), fajl_daqqas = 수(LOOKUP_tabella + 16), Memorja_daqqas = 수(LOOKUP_tabella + 20);
            int allinja_VALUE = 수(LOOKUP_tabella + 28);
            if (ADDRESS < Bidu_utent_programm || ADDRESS >= IMAGE_ttermina_ADDRESS || Memorja_daqqas < 0 || Memorja_daqqas > IMAGE_ttermina_ADDRESS - ADDRESS
                || fajl_daqqas < 0 || fajl_daqqas > Memorja_daqqas || pożizzjoni < 0 || (fajl_daqqas > 0 && pożizzjoni > tul_VALUE - fajl_daqqas)
                || (allinja_VALUE != 0 && (allinja_VALUE < 0 || (allinja_VALUE & (allinja_VALUE - 1)) != 0
                    || ((ADDRESS - pożizzjoni) & (allinja_VALUE - 1)) != 0))) return -8;
            for (int 앞 = 0; 앞 < INDEX; 앞++) {
                int 이전 = fajl + tabella_pożizzjoni + 앞 * 32;
                if (수(이전) == 1 && Memorja_daqqas > 0 && 수(이전 + 20) > 0
                    && ADDRESS < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < ADDRESS + Memorja_daqqas) return -8;
            }
            if ((수(LOOKUP_tabella + 24) & 1) != 0 && entrata_punt_VALUE >= ADDRESS && entrata_punt_VALUE - ADDRESS < fajl_daqqas) 실행가능 = true;
        }
        return 실행가능 ? entrata_punt_VALUE : -8;
    }

    static int eżegwixxa_kmand(int[] 입력, int serje, int tul_VALUE) {
        while (serje < tul_VALUE && 입력[serje] == ' ') serje++;
        int 끝 = serje;
        while (끝 < tul_VALUE && 입력[끝] != ' ') 끝++;
        int entrata_VALUE = sab_entrata(입력, serje, 끝 - serje);
        if (entrata_VALUE == 0) return -2;
        int pożizzjoni = 수(entrata_VALUE + 16), daqqas = 수(entrata_VALUE + 20);
        if (pożizzjoni < 8 + grupp_COUNT() * 24 || daqqas < 52 || pożizzjoni > mowbajl_VALUE.실행묶음크기() - daqqas) return -8;
        int fajl = mowbajl_VALUE.실행묶음() + pożizzjoni;
        int entrata_punt_VALUE = vvalida(fajl, daqqas);
        if (entrata_punt_VALUE < 0) return entrata_punt_VALUE;
        mowbajl_VALUE.utent_neħħa_TOC();
        int tabella_pożizzjoni = 수(fajl + 28), element_COUNT = 짧은수(fajl + 44);
        for (int INDEX = 0; INDEX < element_COUNT; INDEX++) {
            int LOOKUP_tabella = fajl + tabella_pożizzjoni + INDEX * 32;
            if (수(LOOKUP_tabella) != 1) continue;
            int 원본 = fajl + 수(LOOKUP_tabella + 4), destinazzjoni_VALUE = 수(LOOKUP_tabella + 8), fajl_daqqas = 수(LOOKUP_tabella + 16);
            for (int byte_VALUE = 0; byte_VALUE < fajl_daqqas; byte_VALUE++) mowbajl_VALUE.kiteb_Memorja(destinazzjoni_VALUE + byte_VALUE, mowbajl_VALUE.기억읽기(원본 + byte_VALUE));
        }
        argument_COUNT = 0;
        int Store_VALUE = argument_Bidu;
        while (끝 < tul_VALUE) {
            while (끝 < tul_VALUE && 입력[끝] == ' ') 끝++;
            if (끝 == tul_VALUE) break;
            if (argument_COUNT == argument_ADDRESS.length) return -22;
            serje = 끝;
            while (끝 < tul_VALUE && 입력[끝] != ' ') 끝++;
            argument_ADDRESS[argument_COUNT++] = Store_VALUE;
            수쓰기(Store_VALUE, 끝 - serje);
            for (int karattru_VALUE = serje; karattru_VALUE < 끝; karattru_VALUE++) 수쓰기(Store_VALUE + 4 + (karattru_VALUE - serje) * 4, 입력[karattru_VALUE]);
            Store_VALUE += 4 + (끝 - serje) * 4;
        }
        netwerk_Munzell.CLEAN_Proċess();
        파일서술자관리.Bidu_Proċess();
        int miżura = mowbajl_VALUE.serje_utent_programm(entrata_punt_VALUE, utent_ttermina - 16);
        파일서술자관리.CLEAN_Proċess();
        netwerk_Munzell.CLEAN_Proċess();
        return miżura;
    }
}
