// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Čtení 전용 Provést_příkaz 묶음의 ELF32 ověřit_5fb2b747, argumenty Vpřed_HODNOTA, 한 번에 한 uživatelský_prostor Proces_HODNOTA Provést_příkaz. */
public final class spuštění_Správce {
    static final int START_uživatel_program = 0x04000000;
    static final int uživatel_konec = 0x04400000;
    static final int image_konec_ODKAZ = 0x04200000;
    static final int argument_START = 0x04300000;
    static int argument_POČET = 0;
    static int[] argument_ODKAZ = new int[16];

    static boolean oříznout(int Adresa, int délka_HODNOTA) {
        return Adresa >= START_uživatel_program && Adresa < uživatel_konec && délka_HODNOTA >= 0 && délka_HODNOTA <= uživatel_konec - Adresa;
    }

    static int číslo(int Adresa) { return Paměť_oblast.parsovat_integer(Adresa); }
    static int 짧은수(int Adresa) { return mobilní_HODNOTA.기억읽기(Adresa) | mobilní_HODNOTA.기억읽기(Adresa + 1) << 8; }
    static void zápis_číslo(int Adresa, int HODNOTA) {
        for (int INDEX = 0; INDEX < 4; INDEX++) mobilní_HODNOTA.zápis_Paměť(Adresa + INDEX, HODNOTA >>> (INDEX * 8));
    }

    static int Skupina_POČET() {
        int Adresa = mobilní_HODNOTA.spustitelný_sada();
        int Velikost = mobilní_HODNOTA.spustitelný_sada_změnit_velikost();
        if (Velikost < 8 || číslo(Adresa) != 0x50414b4a) return 0;
        int zboží_POČET = číslo(Adresa + 4);
        return zboží_POČET >= 0 && zboží_POČET <= 32 && zboží_POČET <= (Velikost - 8) / 24 ? zboží_POČET : 0;
    }

    static void položka_Seznam() {
        for (int INDEX = 0; INDEX < Skupina_POČET(); INDEX++) {
            int položka_HODNOTA = mobilní_HODNOTA.spustitelný_sada() + 8 + INDEX * 24;
            for (int znak_HODNOTA = 0; znak_HODNOTA < 16 && mobilní_HODNOTA.기억읽기(položka_HODNOTA + znak_HODNOTA) != 0; znak_HODNOTA++)
                SMS_Terminál.문자(mobilní_HODNOTA.기억읽기(položka_HODNOTA + znak_HODNOTA));
            SMS_Terminál.Zápis("\n");
        }
    }

    static int NAJÍT_položka(int[] vstup_HODNOTA, int Spustit_2, int délka_HODNOTA) {
        if (délka_HODNOTA <= 0 || délka_HODNOTA >= 16) return 0;
        for (int INDEX = 0; INDEX < Skupina_POČET(); INDEX++) {
            int položka_HODNOTA = mobilní_HODNOTA.spustitelný_sada() + 8 + INDEX * 24;
            boolean 같음 = mobilní_HODNOTA.기억읽기(položka_HODNOTA + délka_HODNOTA) == 0;
            for (int znak_HODNOTA = 0; znak_HODNOTA < délka_HODNOTA; znak_HODNOTA++)
                if (vstup_HODNOTA[Spustit_2 + znak_HODNOTA] != mobilní_HODNOTA.기억읽기(položka_HODNOTA + znak_HODNOTA)) 같음 = false;
            if (같음) return položka_HODNOTA;
        }
        return 0;
    }

    static int ověřit_5fb2b747(int název_souboru, int délka_HODNOTA) {
        if (délka_HODNOTA < 52 || číslo(název_souboru) != 0x464c457f || mobilní_HODNOTA.기억읽기(název_souboru + 4) != 1
            || mobilní_HODNOTA.기억읽기(název_souboru + 5) != 1 || mobilní_HODNOTA.기억읽기(název_souboru + 6) != 1
            || 짧은수(název_souboru + 16) != 2 || 짧은수(název_souboru + 18) != 3 || číslo(název_souboru + 20) != 1
            || 짧은수(název_souboru + 40) != 52 || 짧은수(název_souboru + 42) != 32) return -8;
        int vstupní_bod_HODNOTA = číslo(název_souboru + 24);
        int tabulka_pozice = číslo(název_souboru + 28);
        int zboží_POČET = 짧은수(název_souboru + 44);
        if (zboží_POČET == 0 || zboží_POČET > 16 || tabulka_pozice < 52 || tabulka_pozice > délka_HODNOTA - zboží_POČET * 32) return -8;
        boolean informační_systémy_spustitelný = false;
        for (int INDEX = 0; INDEX < zboží_POČET; INDEX++) {
            int VYHLEDAT_tabulka = název_souboru + tabulka_pozice + INDEX * 32;
            int Druh_HODNOTA = číslo(VYHLEDAT_tabulka);
            if (Druh_HODNOTA == 2 || Druh_HODNOTA == 3) return -8; // 동적 Připojit/analyzátor_48ee4b1b 미지원
            if (Druh_HODNOTA != 1) continue;
            int pozice = číslo(VYHLEDAT_tabulka + 4), Adresa = číslo(VYHLEDAT_tabulka + 8), velikost_souboru = číslo(VYHLEDAT_tabulka + 16), Paměť_změnit_velikost = číslo(VYHLEDAT_tabulka + 20);
            int zarovnat_HODNOTA = číslo(VYHLEDAT_tabulka + 28);
            if (Adresa < START_uživatel_program || Adresa >= image_konec_ODKAZ || Paměť_změnit_velikost < 0 || Paměť_změnit_velikost > image_konec_ODKAZ - Adresa
                || velikost_souboru < 0 || velikost_souboru > Paměť_změnit_velikost || pozice < 0 || (velikost_souboru > 0 && pozice > délka_HODNOTA - velikost_souboru)
                || (zarovnat_HODNOTA != 0 && (zarovnat_HODNOTA < 0 || (zarovnat_HODNOTA & (zarovnat_HODNOTA - 1)) != 0
                    || ((Adresa - pozice) & (zarovnat_HODNOTA - 1)) != 0))) return -8;
            for (int přední_fotoaparát_HODNOTA = 0; přední_fotoaparát_HODNOTA < INDEX; přední_fotoaparát_HODNOTA++) {
                int Předchozí_zboží = název_souboru + tabulka_pozice + přední_fotoaparát_HODNOTA * 32;
                if (číslo(Předchozí_zboží) == 1 && Paměť_změnit_velikost > 0 && číslo(Předchozí_zboží + 20) > 0
                    && Adresa < číslo(Předchozí_zboží + 8) + číslo(Předchozí_zboží + 20) && číslo(Předchozí_zboží + 8) < Adresa + Paměť_změnit_velikost) return -8;
            }
            if ((číslo(VYHLEDAT_tabulka + 24) & 1) != 0 && vstupní_bod_HODNOTA >= Adresa && vstupní_bod_HODNOTA - Adresa < velikost_souboru) informační_systémy_spustitelný = true;
        }
        return informační_systémy_spustitelný ? vstupní_bod_HODNOTA : -8;
    }

    static int Provést_příkaz(int[] vstup_HODNOTA, int Spustit_2, int délka_HODNOTA) {
        while (Spustit_2 < délka_HODNOTA && vstup_HODNOTA[Spustit_2] == ' ') Spustit_2++;
        int 끝 = Spustit_2;
        while (끝 < délka_HODNOTA && vstup_HODNOTA[끝] != ' ') 끝++;
        int položka_HODNOTA = NAJÍT_položka(vstup_HODNOTA, Spustit_2, 끝 - Spustit_2);
        if (položka_HODNOTA == 0) return -2;
        int pozice = číslo(položka_HODNOTA + 16), Velikost = číslo(položka_HODNOTA + 20);
        if (pozice < 8 + Skupina_POČET() * 24 || Velikost < 52 || pozice > mobilní_HODNOTA.spustitelný_sada_změnit_velikost() - Velikost) return -8;
        int název_souboru = mobilní_HODNOTA.spustitelný_sada() + pozice;
        int vstupní_bod_HODNOTA = ověřit_5fb2b747(název_souboru, Velikost);
        if (vstupní_bod_HODNOTA < 0) return vstupní_bod_HODNOTA;
        mobilní_HODNOTA.uživatel_vymazat_Obsah();
        int tabulka_pozice = číslo(název_souboru + 28), zboží_POČET = 짧은수(název_souboru + 44);
        for (int INDEX = 0; INDEX < zboží_POČET; INDEX++) {
            int VYHLEDAT_tabulka = název_souboru + tabulka_pozice + INDEX * 32;
            if (číslo(VYHLEDAT_tabulka) != 1) continue;
            int 원본 = název_souboru + číslo(VYHLEDAT_tabulka + 4), cíl_HODNOTA = číslo(VYHLEDAT_tabulka + 8), velikost_souboru = číslo(VYHLEDAT_tabulka + 16);
            for (int bajt_HODNOTA = 0; bajt_HODNOTA < velikost_souboru; bajt_HODNOTA++) mobilní_HODNOTA.zápis_Paměť(cíl_HODNOTA + bajt_HODNOTA, mobilní_HODNOTA.기억읽기(원본 + bajt_HODNOTA));
        }
        argument_POČET = 0;
        int Store_HODNOTA = argument_START;
        while (끝 < délka_HODNOTA) {
            while (끝 < délka_HODNOTA && vstup_HODNOTA[끝] == ' ') 끝++;
            if (끝 == délka_HODNOTA) break;
            if (argument_POČET == argument_ODKAZ.length) return -22;
            Spustit_2 = 끝;
            while (끝 < délka_HODNOTA && vstup_HODNOTA[끝] != ' ') 끝++;
            argument_ODKAZ[argument_POČET++] = Store_HODNOTA;
            zápis_číslo(Store_HODNOTA, 끝 - Spustit_2);
            for (int znak_HODNOTA = Spustit_2; znak_HODNOTA < 끝; znak_HODNOTA++) zápis_číslo(Store_HODNOTA + 4 + (znak_HODNOTA - Spustit_2) * 4, vstup_HODNOTA[znak_HODNOTA]);
            Store_HODNOTA += 4 + (끝 - Spustit_2) * 4;
        }
        síť_Štos.Čisté_Proces();
        Soubor_popisovač_Správce.START_Proces();
        int VÝSLEDEK = mobilní_HODNOTA.spustit_uživatel_program(vstupní_bod_HODNOTA, uživatel_konec - 16);
        Soubor_popisovač_Správce.Čisté_Proces();
        síť_Štos.Čisté_Proces();
        return VÝSLEDEK;
    }
}
