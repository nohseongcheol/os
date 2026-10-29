// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Branje 전용 Izvedi_ukaz 묶음의 ELF32 preveriti_veljavnost, Argumenti Naprej_VALUE, 한 번에 한 uporabnik Proces_VALUE Izvedi_ukaz. */
public final class 실행관리 {
    static final int Start_uporabnik_aplikacija = 0x04000000;
    static final int uporabnik_končati_klic = 0x04400000;
    static final int IMAGE_končati_klic_naslov = 0x04200000;
    static final int argument_Start = 0x04300000;
    static int argument_COUNT = 0;
    static int[] argument_naslov = new int[16];

    static boolean izrezek(int naslov, int 길이) {
        return naslov >= Start_uporabnik_aplikacija && naslov < uporabnik_končati_klic && 길이 >= 0 && 길이 <= uporabnik_končati_klic - naslov;
    }

    static int 수(int naslov) { return pomnilnik_območje.razčlenjevati_celo_število(naslov); }
    static int 짧은수(int naslov) { return naprava_VALUE.기억읽기(naslov) | naprava_VALUE.기억읽기(naslov + 1) << 8; }
    static void 수쓰기(int naslov, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) naprava_VALUE.pisati_pomnilnik(naslov + INDEX, VALUE >>> (INDEX * 8));
    }

    static int Skupina_COUNT() {
        int naslov = naprava_VALUE.실행묶음();
        int Velikost = naprava_VALUE.실행묶음크기();
        if (Velikost < 8 || 수(naslov) != 0x50414b4a) return 0;
        int element_COUNT = 수(naslov + 4);
        return element_COUNT >= 0 && element_COUNT <= 32 && element_COUNT <= (Velikost - 8) / 24 ? element_COUNT : 0;
    }

    static void vnos_Seznam() {
        for (int INDEX = 0; INDEX < Skupina_COUNT(); INDEX++) {
            int vnos_VALUE = naprava_VALUE.실행묶음() + 8 + INDEX * 24;
            for (int znak_VALUE = 0; znak_VALUE < 16 && naprava_VALUE.기억읽기(vnos_VALUE + znak_VALUE) != 0; znak_VALUE++)
                SMS_Terminal.문자(naprava_VALUE.기억읽기(vnos_VALUE + znak_VALUE));
            SMS_Terminal.Pisanje("\n");
        }
    }

    static int FIND_vnos(int[] 입력, int Zaženi, int 길이) {
        if (길이 <= 0 || 길이 >= 16) return 0;
        for (int INDEX = 0; INDEX < Skupina_COUNT(); INDEX++) {
            int vnos_VALUE = naprava_VALUE.실행묶음() + 8 + INDEX * 24;
            boolean 같음 = naprava_VALUE.기억읽기(vnos_VALUE + 길이) == 0;
            for (int znak_VALUE = 0; znak_VALUE < 길이; znak_VALUE++)
                if (입력[Zaženi + znak_VALUE] != naprava_VALUE.기억읽기(vnos_VALUE + znak_VALUE)) 같음 = false;
            if (같음) return vnos_VALUE;
        }
        return 0;
    }

    static int preveriti_veljavnost(int Datoteka, int 길이) {
        if (길이 < 52 || 수(Datoteka) != 0x464c457f || naprava_VALUE.기억읽기(Datoteka + 4) != 1
            || naprava_VALUE.기억읽기(Datoteka + 5) != 1 || naprava_VALUE.기억읽기(Datoteka + 6) != 1
            || 짧은수(Datoteka + 16) != 2 || 짧은수(Datoteka + 18) != 3 || 수(Datoteka + 20) != 1
            || 짧은수(Datoteka + 40) != 52 || 짧은수(Datoteka + 42) != 32) return -8;
        int vnos_p_VALUE = 수(Datoteka + 24);
        int tabela_položaj = 수(Datoteka + 28);
        int element_COUNT = 짧은수(Datoteka + 44);
        if (element_COUNT == 0 || element_COUNT > 16 || tabela_položaj < 52 || tabela_položaj > 길이 - element_COUNT * 32) return -8;
        boolean 실행가능 = false;
        for (int INDEX = 0; INDEX < element_COUNT; INDEX++) {
            int iskalna_tabela = Datoteka + tabela_položaj + INDEX * 32;
            int 종류 = 수(iskalna_tabela);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Poveži/razčlenjevalnik_48ee4b1b 미지원
            if (종류 != 1) continue;
            int Položaj = 수(iskalna_tabela + 4), naslov = 수(iskalna_tabela + 8), velikost_datoteke = 수(iskalna_tabela + 16), pomnilnik_spremeniti_velikost = 수(iskalna_tabela + 20);
            int poravnati_VALUE = 수(iskalna_tabela + 28);
            if (naslov < Start_uporabnik_aplikacija || naslov >= IMAGE_končati_klic_naslov || pomnilnik_spremeniti_velikost < 0 || pomnilnik_spremeniti_velikost > IMAGE_končati_klic_naslov - naslov
                || velikost_datoteke < 0 || velikost_datoteke > pomnilnik_spremeniti_velikost || Položaj < 0 || (velikost_datoteke > 0 && Položaj > 길이 - velikost_datoteke)
                || (poravnati_VALUE != 0 && (poravnati_VALUE < 0 || (poravnati_VALUE & (poravnati_VALUE - 1)) != 0
                    || ((naslov - Položaj) & (poravnati_VALUE - 1)) != 0))) return -8;
            for (int sprednja_VALUE = 0; sprednja_VALUE < INDEX; sprednja_VALUE++) {
                int 이전 = Datoteka + tabela_položaj + sprednja_VALUE * 32;
                if (수(이전) == 1 && pomnilnik_spremeniti_velikost > 0 && 수(이전 + 20) > 0
                    && naslov < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < naslov + pomnilnik_spremeniti_velikost) return -8;
            }
            if ((수(iskalna_tabela + 24) & 1) != 0 && vnos_p_VALUE >= naslov && vnos_p_VALUE - naslov < velikost_datoteke) 실행가능 = true;
        }
        return 실행가능 ? vnos_p_VALUE : -8;
    }

    static int Izvedi_ukaz(int[] 입력, int Zaženi, int 길이) {
        while (Zaženi < 길이 && 입력[Zaženi] == ' ') Zaženi++;
        int 끝 = Zaženi;
        while (끝 < 길이 && 입력[끝] != ' ') 끝++;
        int vnos_VALUE = FIND_vnos(입력, Zaženi, 끝 - Zaženi);
        if (vnos_VALUE == 0) return -2;
        int Položaj = 수(vnos_VALUE + 16), Velikost = 수(vnos_VALUE + 20);
        if (Položaj < 8 + Skupina_COUNT() * 24 || Velikost < 52 || Položaj > naprava_VALUE.실행묶음크기() - Velikost) return -8;
        int Datoteka = naprava_VALUE.실행묶음() + Položaj;
        int vnos_p_VALUE = preveriti_veljavnost(Datoteka, Velikost);
        if (vnos_p_VALUE < 0) return vnos_p_VALUE;
        naprava_VALUE.uporabnik_počistiti_Vsebina();
        int tabela_položaj = 수(Datoteka + 28), element_COUNT = 짧은수(Datoteka + 44);
        for (int INDEX = 0; INDEX < element_COUNT; INDEX++) {
            int iskalna_tabela = Datoteka + tabela_položaj + INDEX * 32;
            if (수(iskalna_tabela) != 1) continue;
            int 원본 = Datoteka + 수(iskalna_tabela + 4), cilj_VALUE = 수(iskalna_tabela + 8), velikost_datoteke = 수(iskalna_tabela + 16);
            for (int bajt_VALUE = 0; bajt_VALUE < velikost_datoteke; bajt_VALUE++) naprava_VALUE.pisati_pomnilnik(cilj_VALUE + bajt_VALUE, naprava_VALUE.기억읽기(원본 + bajt_VALUE));
        }
        argument_COUNT = 0;
        int Store_VALUE = argument_Start;
        while (끝 < 길이) {
            while (끝 < 길이 && 입력[끝] == ' ') 끝++;
            if (끝 == 길이) break;
            if (argument_COUNT == argument_naslov.length) return -22;
            Zaženi = 끝;
            while (끝 < 길이 && 입력[끝] != ' ') 끝++;
            argument_naslov[argument_COUNT++] = Store_VALUE;
            수쓰기(Store_VALUE, 끝 - Zaženi);
            for (int znak_VALUE = Zaženi; znak_VALUE < 끝; znak_VALUE++) 수쓰기(Store_VALUE + 4 + (znak_VALUE - Zaženi) * 4, 입력[znak_VALUE]);
            Store_VALUE += 4 + (끝 - Zaženi) * 4;
        }
        mreža_Sklad.CLEAN_Proces();
        파일서술자관리.Start_Proces();
        int REZULTAT = naprava_VALUE.izvajati_uporabnik_aplikacija(vnos_p_VALUE, uporabnik_končati_klic - 16);
        파일서술자관리.CLEAN_Proces();
        mreža_Sklad.CLEAN_Proces();
        return REZULTAT;
    }
}
