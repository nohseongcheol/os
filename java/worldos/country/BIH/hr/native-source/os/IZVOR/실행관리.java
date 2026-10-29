// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Čitaj 전용 Izvrši_naredba 묶음의 ELF32 potvrditi, Argumenti Naprijed_VALUE, 한 번에 한 korisnik Proces_VALUE Izvrši_naredba. */
public final class 실행관리 {
    static final int START_korisnik_program = 0x04000000;
    static final int korisnik_završiti_razgovor = 0x04400000;
    static final int IMAGE_završiti_razgovor_adresa = 0x04200000;
    static final int argument_START = 0x04300000;
    static int argument_COUNT = 0;
    static int[] argument_adresa = new int[16];

    static boolean isječak(int adresa, int 길이) {
        return adresa >= START_korisnik_program && adresa < korisnik_završiti_razgovor && 길이 >= 0 && 길이 <= korisnik_završiti_razgovor - adresa;
    }

    static int 수(int adresa) { return Memorija_regije.rastavljati_cijeli_broj(adresa); }
    static int 짧은수(int adresa) { return uređaj_VALUE.기억읽기(adresa) | uređaj_VALUE.기억읽기(adresa + 1) << 8; }
    static void 수쓰기(int adresa, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) uređaj_VALUE.zapisivanje_Memorija(adresa + INDEX, VALUE >>> (INDEX * 8));
    }

    static int Grupa_COUNT() {
        int adresa = uređaj_VALUE.실행묶음();
        int Veličina = uređaj_VALUE.실행묶음크기();
        if (Veličina < 8 || 수(adresa) != 0x50414b4a) return 0;
        int artikl_COUNT = 수(adresa + 4);
        return artikl_COUNT >= 0 && artikl_COUNT <= 32 && artikl_COUNT <= (Veličina - 8) / 24 ? artikl_COUNT : 0;
    }

    static void unos_Popis() {
        for (int INDEX = 0; INDEX < Grupa_COUNT(); INDEX++) {
            int unos_VALUE = uređaj_VALUE.실행묶음() + 8 + INDEX * 24;
            for (int znak_VALUE = 0; znak_VALUE < 16 && uređaj_VALUE.기억읽기(unos_VALUE + znak_VALUE) != 0; znak_VALUE++)
                SMS_Terminal.문자(uređaj_VALUE.기억읽기(unos_VALUE + znak_VALUE));
            SMS_Terminal.Zapisuj("\n");
        }
    }

    static int FIND_unos(int[] 입력, int Pokreni, int 길이) {
        if (길이 <= 0 || 길이 >= 16) return 0;
        for (int INDEX = 0; INDEX < Grupa_COUNT(); INDEX++) {
            int unos_VALUE = uređaj_VALUE.실행묶음() + 8 + INDEX * 24;
            boolean 같음 = uređaj_VALUE.기억읽기(unos_VALUE + 길이) == 0;
            for (int znak_VALUE = 0; znak_VALUE < 길이; znak_VALUE++)
                if (입력[Pokreni + znak_VALUE] != uređaj_VALUE.기억읽기(unos_VALUE + znak_VALUE)) 같음 = false;
            if (같음) return unos_VALUE;
        }
        return 0;
    }

    static int potvrditi(int Datoteka, int 길이) {
        if (길이 < 52 || 수(Datoteka) != 0x464c457f || uređaj_VALUE.기억읽기(Datoteka + 4) != 1
            || uređaj_VALUE.기억읽기(Datoteka + 5) != 1 || uređaj_VALUE.기억읽기(Datoteka + 6) != 1
            || 짧은수(Datoteka + 16) != 2 || 짧은수(Datoteka + 18) != 3 || 수(Datoteka + 20) != 1
            || 짧은수(Datoteka + 40) != 52 || 짧은수(Datoteka + 42) != 32) return -8;
        int unos_p_VALUE = 수(Datoteka + 24);
        int tablica_položaj = 수(Datoteka + 28);
        int artikl_COUNT = 짧은수(Datoteka + 44);
        if (artikl_COUNT == 0 || artikl_COUNT > 16 || tablica_položaj < 52 || tablica_položaj > 길이 - artikl_COUNT * 32) return -8;
        boolean 실행가능 = false;
        for (int INDEX = 0; INDEX < artikl_COUNT; INDEX++) {
            int LOOKUP_tablica = Datoteka + tablica_položaj + INDEX * 32;
            int 종류 = 수(LOOKUP_tablica);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Spoji_se/analizator_48ee4b1b 미지원
            if (종류 != 1) continue;
            int Položaj = 수(LOOKUP_tablica + 4), adresa = 수(LOOKUP_tablica + 8), veličina_datoteke = 수(LOOKUP_tablica + 16), Memorija_promijeniti_veličinu = 수(LOOKUP_tablica + 20);
            int poravnati_VALUE = 수(LOOKUP_tablica + 28);
            if (adresa < START_korisnik_program || adresa >= IMAGE_završiti_razgovor_adresa || Memorija_promijeniti_veličinu < 0 || Memorija_promijeniti_veličinu > IMAGE_završiti_razgovor_adresa - adresa
                || veličina_datoteke < 0 || veličina_datoteke > Memorija_promijeniti_veličinu || Položaj < 0 || (veličina_datoteke > 0 && Položaj > 길이 - veličina_datoteke)
                || (poravnati_VALUE != 0 && (poravnati_VALUE < 0 || (poravnati_VALUE & (poravnati_VALUE - 1)) != 0
                    || ((adresa - Položaj) & (poravnati_VALUE - 1)) != 0))) return -8;
            for (int prednja_VALUE = 0; prednja_VALUE < INDEX; prednja_VALUE++) {
                int 이전 = Datoteka + tablica_položaj + prednja_VALUE * 32;
                if (수(이전) == 1 && Memorija_promijeniti_veličinu > 0 && 수(이전 + 20) > 0
                    && adresa < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < adresa + Memorija_promijeniti_veličinu) return -8;
            }
            if ((수(LOOKUP_tablica + 24) & 1) != 0 && unos_p_VALUE >= adresa && unos_p_VALUE - adresa < veličina_datoteke) 실행가능 = true;
        }
        return 실행가능 ? unos_p_VALUE : -8;
    }

    static int Izvrši_naredba(int[] 입력, int Pokreni, int 길이) {
        while (Pokreni < 길이 && 입력[Pokreni] == ' ') Pokreni++;
        int 끝 = Pokreni;
        while (끝 < 길이 && 입력[끝] != ' ') 끝++;
        int unos_VALUE = FIND_unos(입력, Pokreni, 끝 - Pokreni);
        if (unos_VALUE == 0) return -2;
        int Položaj = 수(unos_VALUE + 16), Veličina = 수(unos_VALUE + 20);
        if (Položaj < 8 + Grupa_COUNT() * 24 || Veličina < 52 || Položaj > uređaj_VALUE.실행묶음크기() - Veličina) return -8;
        int Datoteka = uređaj_VALUE.실행묶음() + Položaj;
        int unos_p_VALUE = potvrditi(Datoteka, Veličina);
        if (unos_p_VALUE < 0) return unos_p_VALUE;
        uređaj_VALUE.korisnik_očistiti_Sadržaj();
        int tablica_položaj = 수(Datoteka + 28), artikl_COUNT = 짧은수(Datoteka + 44);
        for (int INDEX = 0; INDEX < artikl_COUNT; INDEX++) {
            int LOOKUP_tablica = Datoteka + tablica_položaj + INDEX * 32;
            if (수(LOOKUP_tablica) != 1) continue;
            int 원본 = Datoteka + 수(LOOKUP_tablica + 4), odredište_VALUE = 수(LOOKUP_tablica + 8), veličina_datoteke = 수(LOOKUP_tablica + 16);
            for (int bajt_VALUE = 0; bajt_VALUE < veličina_datoteke; bajt_VALUE++) uređaj_VALUE.zapisivanje_Memorija(odredište_VALUE + bajt_VALUE, uređaj_VALUE.기억읽기(원본 + bajt_VALUE));
        }
        argument_COUNT = 0;
        int Store_VALUE = argument_START;
        while (끝 < 길이) {
            while (끝 < 길이 && 입력[끝] == ' ') 끝++;
            if (끝 == 길이) break;
            if (argument_COUNT == argument_adresa.length) return -22;
            Pokreni = 끝;
            while (끝 < 길이 && 입력[끝] != ' ') 끝++;
            argument_adresa[argument_COUNT++] = Store_VALUE;
            수쓰기(Store_VALUE, 끝 - Pokreni);
            for (int znak_VALUE = Pokreni; znak_VALUE < 끝; znak_VALUE++) 수쓰기(Store_VALUE + 4 + (znak_VALUE - Pokreni) * 4, 입력[znak_VALUE]);
            Store_VALUE += 4 + (끝 - Pokreni) * 4;
        }
        mreža_hrpa.CLEAN_Proces();
        파일서술자관리.START_Proces();
        int REZULTAT = uređaj_VALUE.izvršiti_korisnik_program(unos_p_VALUE, korisnik_završiti_razgovor - 16);
        파일서술자관리.CLEAN_Proces();
        mreža_hrpa.CLEAN_Proces();
        return REZULTAT;
    }
}
