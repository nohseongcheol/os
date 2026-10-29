// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 읽기 전용 Izvrši_komanda 묶음의 ELF32 potvrditi, 인수 Napred_VALUE, 한 번에 한 korisnik Proces_VALUE Izvrši_komanda. */
public final class 실행관리 {
    static final int START_korisnik_program = 0x04000000;
    static final int korisnik_završiti_razgovor = 0x04400000;
    static final int IMAGE_završiti_razgovor_adresa = 0x04200000;
    static final int argument_START = 0x04300000;
    static int argument_COUNT = 0;
    static int[] argument_adresa = new int[16];

    static boolean klip(int adresa, int 길이) {
        return adresa >= START_korisnik_program && adresa < korisnik_završiti_razgovor && 길이 >= 0 && 길이 <= korisnik_završiti_razgovor - adresa;
    }

    static int 수(int adresa) { return Memorija_oblast.raščlaniti_ceo_broj(adresa); }
    static int 짧은수(int adresa) { return uređaj_VALUE.기억읽기(adresa) | uređaj_VALUE.기억읽기(adresa + 1) << 8; }
    static void 수쓰기(int adresa, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) uređaj_VALUE.기억쓰기(adresa + INDEX, VALUE >>> (INDEX * 8));
    }

    static int Grupa_COUNT() {
        int adresa = uređaj_VALUE.실행묶음();
        int promeniti_veličinu = uređaj_VALUE.실행묶음크기();
        if (promeniti_veličinu < 8 || 수(adresa) != 0x50414b4a) return 0;
        int stavka_COUNT = 수(adresa + 4);
        return stavka_COUNT >= 0 && stavka_COUNT <= 32 && stavka_COUNT <= (promeniti_veličinu - 8) / 24 ? stavka_COUNT : 0;
    }

    static void stavka_Lista() {
        for (int INDEX = 0; INDEX < Grupa_COUNT(); INDEX++) {
            int stavka_VALUE = uređaj_VALUE.실행묶음() + 8 + INDEX * 24;
            for (int znak_VALUE = 0; znak_VALUE < 16 && uređaj_VALUE.기억읽기(stavka_VALUE + znak_VALUE) != 0; znak_VALUE++)
                SMS_Terminal.문자(uređaj_VALUE.기억읽기(stavka_VALUE + znak_VALUE));
            SMS_Terminal.쓰기("\n");
        }
    }

    static int FIND_stavka(int[] 입력, int koristiti, int 길이) {
        if (길이 <= 0 || 길이 >= 16) return 0;
        for (int INDEX = 0; INDEX < Grupa_COUNT(); INDEX++) {
            int stavka_VALUE = uređaj_VALUE.실행묶음() + 8 + INDEX * 24;
            boolean 같음 = uređaj_VALUE.기억읽기(stavka_VALUE + 길이) == 0;
            for (int znak_VALUE = 0; znak_VALUE < 길이; znak_VALUE++)
                if (입력[koristiti + znak_VALUE] != uređaj_VALUE.기억읽기(stavka_VALUE + znak_VALUE)) 같음 = false;
            if (같음) return stavka_VALUE;
        }
        return 0;
    }

    static int potvrditi(int Datoteka, int 길이) {
        if (길이 < 52 || 수(Datoteka) != 0x464c457f || uređaj_VALUE.기억읽기(Datoteka + 4) != 1
            || uređaj_VALUE.기억읽기(Datoteka + 5) != 1 || uređaj_VALUE.기억읽기(Datoteka + 6) != 1
            || 짧은수(Datoteka + 16) != 2 || 짧은수(Datoteka + 18) != 3 || 수(Datoteka + 20) != 1
            || 짧은수(Datoteka + 40) != 52 || 짧은수(Datoteka + 42) != 32) return -8;
        int stavka_p_VALUE = 수(Datoteka + 24);
        int tabela_pozicija = 수(Datoteka + 28);
        int stavka_COUNT = 짧은수(Datoteka + 44);
        if (stavka_COUNT == 0 || stavka_COUNT > 16 || tabela_pozicija < 52 || tabela_pozicija > 길이 - stavka_COUNT * 32) return -8;
        boolean 실행가능 = false;
        for (int INDEX = 0; INDEX < stavka_COUNT; INDEX++) {
            int LOOKUP_tabela = Datoteka + tabela_pozicija + INDEX * 32;
            int 종류 = 수(LOOKUP_tabela);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 veze/analizator_48ee4b1b 미지원
            if (종류 != 1) continue;
            int pozicija = 수(LOOKUP_tabela + 4), adresa = 수(LOOKUP_tabela + 8), veličina_datoteke = 수(LOOKUP_tabela + 16), Memorija_promeniti_veličinu = 수(LOOKUP_tabela + 20);
            int poravnati_VALUE = 수(LOOKUP_tabela + 28);
            if (adresa < START_korisnik_program || adresa >= IMAGE_završiti_razgovor_adresa || Memorija_promeniti_veličinu < 0 || Memorija_promeniti_veličinu > IMAGE_završiti_razgovor_adresa - adresa
                || veličina_datoteke < 0 || veličina_datoteke > Memorija_promeniti_veličinu || pozicija < 0 || (veličina_datoteke > 0 && pozicija > 길이 - veličina_datoteke)
                || (poravnati_VALUE != 0 && (poravnati_VALUE < 0 || (poravnati_VALUE & (poravnati_VALUE - 1)) != 0
                    || ((adresa - pozicija) & (poravnati_VALUE - 1)) != 0))) return -8;
            for (int čeona_kamera_VALUE = 0; čeona_kamera_VALUE < INDEX; čeona_kamera_VALUE++) {
                int 이전 = Datoteka + tabela_pozicija + čeona_kamera_VALUE * 32;
                if (수(이전) == 1 && Memorija_promeniti_veličinu > 0 && 수(이전 + 20) > 0
                    && adresa < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < adresa + Memorija_promeniti_veličinu) return -8;
            }
            if ((수(LOOKUP_tabela + 24) & 1) != 0 && stavka_p_VALUE >= adresa && stavka_p_VALUE - adresa < veličina_datoteke) 실행가능 = true;
        }
        return 실행가능 ? stavka_p_VALUE : -8;
    }

    static int Izvrši_komanda(int[] 입력, int koristiti, int 길이) {
        while (koristiti < 길이 && 입력[koristiti] == ' ') koristiti++;
        int 끝 = koristiti;
        while (끝 < 길이 && 입력[끝] != ' ') 끝++;
        int stavka_VALUE = FIND_stavka(입력, koristiti, 끝 - koristiti);
        if (stavka_VALUE == 0) return -2;
        int pozicija = 수(stavka_VALUE + 16), promeniti_veličinu = 수(stavka_VALUE + 20);
        if (pozicija < 8 + Grupa_COUNT() * 24 || promeniti_veličinu < 52 || pozicija > uređaj_VALUE.실행묶음크기() - promeniti_veličinu) return -8;
        int Datoteka = uređaj_VALUE.실행묶음() + pozicija;
        int stavka_p_VALUE = potvrditi(Datoteka, promeniti_veličinu);
        if (stavka_p_VALUE < 0) return stavka_p_VALUE;
        uređaj_VALUE.korisnik_obrisati_Sadržaj();
        int tabela_pozicija = 수(Datoteka + 28), stavka_COUNT = 짧은수(Datoteka + 44);
        for (int INDEX = 0; INDEX < stavka_COUNT; INDEX++) {
            int LOOKUP_tabela = Datoteka + tabela_pozicija + INDEX * 32;
            if (수(LOOKUP_tabela) != 1) continue;
            int 원본 = Datoteka + 수(LOOKUP_tabela + 4), odredište_VALUE = 수(LOOKUP_tabela + 8), veličina_datoteke = 수(LOOKUP_tabela + 16);
            for (int bajt_VALUE = 0; bajt_VALUE < veličina_datoteke; bajt_VALUE++) uređaj_VALUE.기억쓰기(odredište_VALUE + bajt_VALUE, uređaj_VALUE.기억읽기(원본 + bajt_VALUE));
        }
        argument_COUNT = 0;
        int Store_VALUE = argument_START;
        while (끝 < 길이) {
            while (끝 < 길이 && 입력[끝] == ' ') 끝++;
            if (끝 == 길이) break;
            if (argument_COUNT == argument_adresa.length) return -22;
            koristiti = 끝;
            while (끝 < 길이 && 입력[끝] != ' ') 끝++;
            argument_adresa[argument_COUNT++] = Store_VALUE;
            수쓰기(Store_VALUE, 끝 - koristiti);
            for (int znak_VALUE = koristiti; znak_VALUE < 끝; znak_VALUE++) 수쓰기(Store_VALUE + 4 + (znak_VALUE - koristiti) * 4, 입력[znak_VALUE]);
            Store_VALUE += 4 + (끝 - koristiti) * 4;
        }
        Mreža_stek.CLEAN_Proces();
        파일서술자관리.START_Proces();
        int KR = uređaj_VALUE.koristiti_korisnik_program(stavka_p_VALUE, korisnik_završiti_razgovor - 16);
        파일서술자관리.CLEAN_Proces();
        Mreža_stek.CLEAN_Proces();
        return KR;
    }
}
