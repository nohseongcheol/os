// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Čítanie 전용 Vykonať_príkaz 묶음의 ELF32 overiť_5fb2b747, Argumenty Dopredu_VALUE, 한 번에 한 používateľ Proces_VALUE Vykonať_príkaz. */
public final class 실행관리 {
    static final int START_používateľ_program = 0x04000000;
    static final int používateľ_ukončiť_hovor = 0x04400000;
    static final int IMAGE_ukončiť_hovor_adresa = 0x04200000;
    static final int argument_START = 0x04300000;
    static int argument_COUNT = 0;
    static int[] argument_adresa = new int[16];

    static boolean klip(int adresa, int dĺžka_VALUE) {
        return adresa >= START_používateľ_program && adresa < používateľ_ukončiť_hovor && dĺžka_VALUE >= 0 && dĺžka_VALUE <= používateľ_ukončiť_hovor - adresa;
    }

    static int 수(int adresa) { return Pamäť_oblasť.analyzovať_celé_číslo(adresa); }
    static int 짧은수(int adresa) { return telefón_VALUE.기억읽기(adresa) | telefón_VALUE.기억읽기(adresa + 1) << 8; }
    static void 수쓰기(int adresa, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) telefón_VALUE.zapísať_Pamäť(adresa + INDEX, VALUE >>> (INDEX * 8));
    }

    static int Skupina_COUNT() {
        int adresa = telefón_VALUE.spustiteľný_súbor_zväzok();
        int Veľkosť = telefón_VALUE.spustiteľný_súbor_zväzok_zmeniť_veľkosť();
        if (Veľkosť < 8 || 수(adresa) != 0x50414b4a) return 0;
        int položka_COUNT = 수(adresa + 4);
        return položka_COUNT >= 0 && položka_COUNT <= 32 && položka_COUNT <= (Veľkosť - 8) / 24 ? položka_COUNT : 0;
    }

    static void položka_Zoznam() {
        for (int INDEX = 0; INDEX < Skupina_COUNT(); INDEX++) {
            int položka_VALUE = telefón_VALUE.spustiteľný_súbor_zväzok() + 8 + INDEX * 24;
            for (int znak_VALUE = 0; znak_VALUE < 16 && telefón_VALUE.기억읽기(položka_VALUE + znak_VALUE) != 0; znak_VALUE++)
                SMS_Terminál.문자(telefón_VALUE.기억읽기(položka_VALUE + znak_VALUE));
            SMS_Terminál.Zápis("\n");
        }
    }

    static int FIND_položka(int[] vstup_VALUE, int Spustiť_2, int dĺžka_VALUE) {
        if (dĺžka_VALUE <= 0 || dĺžka_VALUE >= 16) return 0;
        for (int INDEX = 0; INDEX < Skupina_COUNT(); INDEX++) {
            int položka_VALUE = telefón_VALUE.spustiteľný_súbor_zväzok() + 8 + INDEX * 24;
            boolean 같음 = telefón_VALUE.기억읽기(položka_VALUE + dĺžka_VALUE) == 0;
            for (int znak_VALUE = 0; znak_VALUE < dĺžka_VALUE; znak_VALUE++)
                if (vstup_VALUE[Spustiť_2 + znak_VALUE] != telefón_VALUE.기억읽기(položka_VALUE + znak_VALUE)) 같음 = false;
            if (같음) return položka_VALUE;
        }
        return 0;
    }

    static int overiť_5fb2b747(int Súbor, int dĺžka_VALUE) {
        if (dĺžka_VALUE < 52 || 수(Súbor) != 0x464c457f || telefón_VALUE.기억읽기(Súbor + 4) != 1
            || telefón_VALUE.기억읽기(Súbor + 5) != 1 || telefón_VALUE.기억읽기(Súbor + 6) != 1
            || 짧은수(Súbor + 16) != 2 || 짧은수(Súbor + 18) != 3 || 수(Súbor + 20) != 1
            || 짧은수(Súbor + 40) != 52 || 짧은수(Súbor + 42) != 32) return -8;
        int položka_bod_VALUE = 수(Súbor + 24);
        int tabuľka_pozícia = 수(Súbor + 28);
        int položka_COUNT = 짧은수(Súbor + 44);
        if (položka_COUNT == 0 || položka_COUNT > 16 || tabuľka_pozícia < 52 || tabuľka_pozícia > dĺžka_VALUE - položka_COUNT * 32) return -8;
        boolean Informačné_systémy_spustiteľný_súbor = false;
        for (int INDEX = 0; INDEX < položka_COUNT; INDEX++) {
            int vyhľadávacia_tabuľka = Súbor + tabuľka_pozícia + INDEX * 32;
            int 종류 = 수(vyhľadávacia_tabuľka);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Pripojiť/analyzátor_48ee4b1b 미지원
            if (종류 != 1) continue;
            int Pozícia = 수(vyhľadávacia_tabuľka + 4), adresa = 수(vyhľadávacia_tabuľka + 8), veľkosť_súboru = 수(vyhľadávacia_tabuľka + 16), Pamäť_zmeniť_veľkosť = 수(vyhľadávacia_tabuľka + 20);
            int zarovnať_VALUE = 수(vyhľadávacia_tabuľka + 28);
            if (adresa < START_používateľ_program || adresa >= IMAGE_ukončiť_hovor_adresa || Pamäť_zmeniť_veľkosť < 0 || Pamäť_zmeniť_veľkosť > IMAGE_ukončiť_hovor_adresa - adresa
                || veľkosť_súboru < 0 || veľkosť_súboru > Pamäť_zmeniť_veľkosť || Pozícia < 0 || (veľkosť_súboru > 0 && Pozícia > dĺžka_VALUE - veľkosť_súboru)
                || (zarovnať_VALUE != 0 && (zarovnať_VALUE < 0 || (zarovnať_VALUE & (zarovnať_VALUE - 1)) != 0
                    || ((adresa - Pozícia) & (zarovnať_VALUE - 1)) != 0))) return -8;
            for (int predný_VALUE = 0; predný_VALUE < INDEX; predný_VALUE++) {
                int 이전 = Súbor + tabuľka_pozícia + predný_VALUE * 32;
                if (수(이전) == 1 && Pamäť_zmeniť_veľkosť > 0 && 수(이전 + 20) > 0
                    && adresa < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < adresa + Pamäť_zmeniť_veľkosť) return -8;
            }
            if ((수(vyhľadávacia_tabuľka + 24) & 1) != 0 && položka_bod_VALUE >= adresa && položka_bod_VALUE - adresa < veľkosť_súboru) Informačné_systémy_spustiteľný_súbor = true;
        }
        return Informačné_systémy_spustiteľný_súbor ? položka_bod_VALUE : -8;
    }

    static int Vykonať_príkaz(int[] vstup_VALUE, int Spustiť_2, int dĺžka_VALUE) {
        while (Spustiť_2 < dĺžka_VALUE && vstup_VALUE[Spustiť_2] == ' ') Spustiť_2++;
        int 끝 = Spustiť_2;
        while (끝 < dĺžka_VALUE && vstup_VALUE[끝] != ' ') 끝++;
        int položka_VALUE = FIND_položka(vstup_VALUE, Spustiť_2, 끝 - Spustiť_2);
        if (položka_VALUE == 0) return -2;
        int Pozícia = 수(položka_VALUE + 16), Veľkosť = 수(položka_VALUE + 20);
        if (Pozícia < 8 + Skupina_COUNT() * 24 || Veľkosť < 52 || Pozícia > telefón_VALUE.spustiteľný_súbor_zväzok_zmeniť_veľkosť() - Veľkosť) return -8;
        int Súbor = telefón_VALUE.spustiteľný_súbor_zväzok() + Pozícia;
        int položka_bod_VALUE = overiť_5fb2b747(Súbor, Veľkosť);
        if (položka_bod_VALUE < 0) return položka_bod_VALUE;
        telefón_VALUE.používateľ_vymazať_Obsah();
        int tabuľka_pozícia = 수(Súbor + 28), položka_COUNT = 짧은수(Súbor + 44);
        for (int INDEX = 0; INDEX < položka_COUNT; INDEX++) {
            int vyhľadávacia_tabuľka = Súbor + tabuľka_pozícia + INDEX * 32;
            if (수(vyhľadávacia_tabuľka) != 1) continue;
            int 원본 = Súbor + 수(vyhľadávacia_tabuľka + 4), cieľ_VALUE = 수(vyhľadávacia_tabuľka + 8), veľkosť_súboru = 수(vyhľadávacia_tabuľka + 16);
            for (int Byte_VALUE = 0; Byte_VALUE < veľkosť_súboru; Byte_VALUE++) telefón_VALUE.zapísať_Pamäť(cieľ_VALUE + Byte_VALUE, telefón_VALUE.기억읽기(원본 + Byte_VALUE));
        }
        argument_COUNT = 0;
        int Store_VALUE = argument_START;
        while (끝 < dĺžka_VALUE) {
            while (끝 < dĺžka_VALUE && vstup_VALUE[끝] == ' ') 끝++;
            if (끝 == dĺžka_VALUE) break;
            if (argument_COUNT == argument_adresa.length) return -22;
            Spustiť_2 = 끝;
            while (끝 < dĺžka_VALUE && vstup_VALUE[끝] != ' ') 끝++;
            argument_adresa[argument_COUNT++] = Store_VALUE;
            수쓰기(Store_VALUE, 끝 - Spustiť_2);
            for (int znak_VALUE = Spustiť_2; znak_VALUE < 끝; znak_VALUE++) 수쓰기(Store_VALUE + 4 + (znak_VALUE - Spustiť_2) * 4, vstup_VALUE[znak_VALUE]);
            Store_VALUE += 4 + (끝 - Spustiť_2) * 4;
        }
        sieť_Vrstvy.CLEAN_Proces();
        파일서술자관리.START_Proces();
        int KR = telefón_VALUE.spustiť_používateľ_program(položka_bod_VALUE, používateľ_ukončiť_hovor - 16);
        파일서술자관리.CLEAN_Proces();
        sieť_Vrstvy.CLEAN_Proces();
        return KR;
    }
}
