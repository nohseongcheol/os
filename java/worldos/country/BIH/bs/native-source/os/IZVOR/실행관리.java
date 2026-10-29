// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Čitaj 전용 Izvrši_komanda 묶음의 ELF32 ovjeriti, Argumenti Naprijed_VALUE, 한 번에 한 korisnik proces_VALUE Izvrši_komanda. */
public final class 실행관리 {
    static final int START_korisnik_program = 0x04000000;
    static final int korisnik_završiti = 0x04400000;
    static final int IMAGE_završiti_adresa = 0x04200000;
    static final int argument_START = 0x04300000;
    static int argument_COUNT = 0;
    static int[] argument_adresa = new int[16];

    static boolean isječak(int adresa, int dužina_VALUE) {
        return adresa >= START_korisnik_program && adresa < korisnik_završiti && dužina_VALUE >= 0 && dužina_VALUE <= korisnik_završiti - adresa;
    }

    static int 수(int adresa) { return 기억공간.raščlanjivati_cijeli_broj(adresa); }
    static int 짧은수(int adresa) { return uređaj_VALUE.기억읽기(adresa) | uređaj_VALUE.기억읽기(adresa + 1) << 8; }
    static void 수쓰기(int adresa, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) uređaj_VALUE.pisati_Memorija(adresa + INDEX, VALUE >>> (INDEX * 8));
    }

    static int Grupa_COUNT() {
        int adresa = uređaj_VALUE.실행묶음();
        int Veličina = uređaj_VALUE.실행묶음크기();
        if (Veličina < 8 || 수(adresa) != 0x50414b4a) return 0;
        int stavka_COUNT = 수(adresa + 4);
        return stavka_COUNT >= 0 && stavka_COUNT <= 32 && stavka_COUNT <= (Veličina - 8) / 24 ? stavka_COUNT : 0;
    }

    static void unos_spisak() {
        for (int INDEX = 0; INDEX < Grupa_COUNT(); INDEX++) {
            int unos_VALUE = uređaj_VALUE.실행묶음() + 8 + INDEX * 24;
            for (int znak_VALUE = 0; znak_VALUE < 16 && uređaj_VALUE.기억읽기(unos_VALUE + znak_VALUE) != 0; znak_VALUE++)
                SMS_Terminal.문자(uređaj_VALUE.기억읽기(unos_VALUE + znak_VALUE));
            SMS_Terminal.Piši("\n");
        }
    }

    static int FIND_unos(int[] 입력, int Pokreni, int dužina_VALUE) {
        if (dužina_VALUE <= 0 || dužina_VALUE >= 16) return 0;
        for (int INDEX = 0; INDEX < Grupa_COUNT(); INDEX++) {
            int unos_VALUE = uređaj_VALUE.실행묶음() + 8 + INDEX * 24;
            boolean 같음 = uređaj_VALUE.기억읽기(unos_VALUE + dužina_VALUE) == 0;
            for (int znak_VALUE = 0; znak_VALUE < dužina_VALUE; znak_VALUE++)
                if (입력[Pokreni + znak_VALUE] != uređaj_VALUE.기억읽기(unos_VALUE + znak_VALUE)) 같음 = false;
            if (같음) return unos_VALUE;
        }
        return 0;
    }

    static int ovjeriti(int Fajl, int dužina_VALUE) {
        if (dužina_VALUE < 52 || 수(Fajl) != 0x464c457f || uređaj_VALUE.기억읽기(Fajl + 4) != 1
            || uređaj_VALUE.기억읽기(Fajl + 5) != 1 || uređaj_VALUE.기억읽기(Fajl + 6) != 1
            || 짧은수(Fajl + 16) != 2 || 짧은수(Fajl + 18) != 3 || 수(Fajl + 20) != 1
            || 짧은수(Fajl + 40) != 52 || 짧은수(Fajl + 42) != 32) return -8;
        int unos_p_VALUE = 수(Fajl + 24);
        int tabela_položaj = 수(Fajl + 28);
        int stavka_COUNT = 짧은수(Fajl + 44);
        if (stavka_COUNT == 0 || stavka_COUNT > 16 || tabela_položaj < 52 || tabela_položaj > dužina_VALUE - stavka_COUNT * 32) return -8;
        boolean 실행가능 = false;
        for (int INDEX = 0; INDEX < stavka_COUNT; INDEX++) {
            int LOOKUP_tabela = Fajl + tabela_položaj + INDEX * 32;
            int 종류 = 수(LOOKUP_tabela);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Spoji_se/해석기 미지원
            if (종류 != 1) continue;
            int Pozicija = 수(LOOKUP_tabela + 4), adresa = 수(LOOKUP_tabela + 8), fajl_podesiti_veličinu = 수(LOOKUP_tabela + 16), Memorija_podesiti_veličinu = 수(LOOKUP_tabela + 20);
            int poravnati_VALUE = 수(LOOKUP_tabela + 28);
            if (adresa < START_korisnik_program || adresa >= IMAGE_završiti_adresa || Memorija_podesiti_veličinu < 0 || Memorija_podesiti_veličinu > IMAGE_završiti_adresa - adresa
                || fajl_podesiti_veličinu < 0 || fajl_podesiti_veličinu > Memorija_podesiti_veličinu || Pozicija < 0 || (fajl_podesiti_veličinu > 0 && Pozicija > dužina_VALUE - fajl_podesiti_veličinu)
                || (poravnati_VALUE != 0 && (poravnati_VALUE < 0 || (poravnati_VALUE & (poravnati_VALUE - 1)) != 0
                    || ((adresa - Pozicija) & (poravnati_VALUE - 1)) != 0))) return -8;
            for (int 앞 = 0; 앞 < INDEX; 앞++) {
                int 이전 = Fajl + tabela_položaj + 앞 * 32;
                if (수(이전) == 1 && Memorija_podesiti_veličinu > 0 && 수(이전 + 20) > 0
                    && adresa < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < adresa + Memorija_podesiti_veličinu) return -8;
            }
            if ((수(LOOKUP_tabela + 24) & 1) != 0 && unos_p_VALUE >= adresa && unos_p_VALUE - adresa < fajl_podesiti_veličinu) 실행가능 = true;
        }
        return 실행가능 ? unos_p_VALUE : -8;
    }

    static int Izvrši_komanda(int[] 입력, int Pokreni, int dužina_VALUE) {
        while (Pokreni < dužina_VALUE && 입력[Pokreni] == ' ') Pokreni++;
        int 끝 = Pokreni;
        while (끝 < dužina_VALUE && 입력[끝] != ' ') 끝++;
        int unos_VALUE = FIND_unos(입력, Pokreni, 끝 - Pokreni);
        if (unos_VALUE == 0) return -2;
        int Pozicija = 수(unos_VALUE + 16), Veličina = 수(unos_VALUE + 20);
        if (Pozicija < 8 + Grupa_COUNT() * 24 || Veličina < 52 || Pozicija > uređaj_VALUE.실행묶음크기() - Veličina) return -8;
        int Fajl = uređaj_VALUE.실행묶음() + Pozicija;
        int unos_p_VALUE = ovjeriti(Fajl, Veličina);
        if (unos_p_VALUE < 0) return unos_p_VALUE;
        uređaj_VALUE.korisnik_obrisati_TOC();
        int tabela_položaj = 수(Fajl + 28), stavka_COUNT = 짧은수(Fajl + 44);
        for (int INDEX = 0; INDEX < stavka_COUNT; INDEX++) {
            int LOOKUP_tabela = Fajl + tabela_položaj + INDEX * 32;
            if (수(LOOKUP_tabela) != 1) continue;
            int 원본 = Fajl + 수(LOOKUP_tabela + 4), odredište_VALUE = 수(LOOKUP_tabela + 8), fajl_podesiti_veličinu = 수(LOOKUP_tabela + 16);
            for (int bajt_VALUE = 0; bajt_VALUE < fajl_podesiti_veličinu; bajt_VALUE++) uređaj_VALUE.pisati_Memorija(odredište_VALUE + bajt_VALUE, uređaj_VALUE.기억읽기(원본 + bajt_VALUE));
        }
        argument_COUNT = 0;
        int Store_VALUE = argument_START;
        while (끝 < dužina_VALUE) {
            while (끝 < dužina_VALUE && 입력[끝] == ' ') 끝++;
            if (끝 == dužina_VALUE) break;
            if (argument_COUNT == argument_adresa.length) return -22;
            Pokreni = 끝;
            while (끝 < dužina_VALUE && 입력[끝] != ' ') 끝++;
            argument_adresa[argument_COUNT++] = Store_VALUE;
            수쓰기(Store_VALUE, 끝 - Pokreni);
            for (int znak_VALUE = Pokreni; znak_VALUE < 끝; znak_VALUE++) 수쓰기(Store_VALUE + 4 + (znak_VALUE - Pokreni) * 4, 입력[znak_VALUE]);
            Store_VALUE += 4 + (끝 - Pokreni) * 4;
        }
        Mreža_snop.CLEAN_proces();
        파일서술자관리.START_proces();
        int mjera = uređaj_VALUE.niz_korisnik_program(unos_p_VALUE, korisnik_završiti - 16);
        파일서술자관리.CLEAN_proces();
        Mreža_snop.CLEAN_proces();
        return mjera;
    }
}
