// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Luku 전용 Suorita_komento 묶음의 ELF32 vahvista, argumentit siirrä_ARVO_24592b8a, 한 번에 한 käyttäjätila prosessi_ARVO Suorita_komento. */
public final class suoritus_Valvoja {
    static final int alku_käyttäjä_ohjelma = 0x04000000;
    static final int käyttäjä_lopettaa_puhelu = 0x04400000;
    static final int KUVA_lopettaa_puhelu_OSOITE = 0x04200000;
    static final int argumentti_alku = 0x04300000;
    static int argumentti_LASKE = 0;
    static int[] argumentti_OSOITE = new int[16];

    static boolean leikata(int OSOITE, int kesto_ARVO) {
        return OSOITE >= alku_käyttäjä_ohjelma && OSOITE < käyttäjä_lopettaa_puhelu && kesto_ARVO >= 0 && kesto_ARVO <= käyttäjä_lopettaa_puhelu - OSOITE;
    }

    static int numero(int OSOITE) { return Muisti_alue.jäsentää_kokonaisluku(OSOITE); }
    static int 짧은수(int OSOITE) { return laite_ARVO.lukea_Muisti(OSOITE) | laite_ARVO.lukea_Muisti(OSOITE + 1) << 8; }
    static void kirjoitus_numero(int OSOITE, int ARVO) {
        for (int INDEKSI = 0; INDEKSI < 4; INDEKSI++) laite_ARVO.kirjoitus_Muisti(OSOITE + INDEKSI, ARVO >>> (INDEKSI * 8));
    }

    static int Ryhmä_LASKE() {
        int OSOITE = laite_ARVO.suoritettava_tiedosto_nippu();
        int Koko = laite_ARVO.suoritettava_tiedosto_nippu_muuttaa_kokoa();
        if (Koko < 8 || numero(OSOITE) != 0x50414b4a) return 0;
        int kohde_LASKE = numero(OSOITE + 4);
        return kohde_LASKE >= 0 && kohde_LASKE <= 32 && kohde_LASKE <= (Koko - 8) / 24 ? kohde_LASKE : 0;
    }

    static void merkintä_luettelo() {
        for (int INDEKSI = 0; INDEKSI < Ryhmä_LASKE(); INDEKSI++) {
            int merkintä_ARVO_962f286b = laite_ARVO.suoritettava_tiedosto_nippu() + 8 + INDEKSI * 24;
            for (int merkki_ARVO = 0; merkki_ARVO < 16 && laite_ARVO.lukea_Muisti(merkintä_ARVO_962f286b + merkki_ARVO) != 0; merkki_ARVO++)
                SMS_Pääte.문자(laite_ARVO.lukea_Muisti(merkintä_ARVO_962f286b + merkki_ARVO));
            SMS_Pääte.Kirjoitus("\n");
        }
    }

    static int ETSI_merkintä(int[] syöte_ARVO, int Suorita_2, int kesto_ARVO) {
        if (kesto_ARVO <= 0 || kesto_ARVO >= 16) return 0;
        for (int INDEKSI = 0; INDEKSI < Ryhmä_LASKE(); INDEKSI++) {
            int merkintä_ARVO_962f286b = laite_ARVO.suoritettava_tiedosto_nippu() + 8 + INDEKSI * 24;
            boolean 같음 = laite_ARVO.lukea_Muisti(merkintä_ARVO_962f286b + kesto_ARVO) == 0;
            for (int merkki_ARVO = 0; merkki_ARVO < kesto_ARVO; merkki_ARVO++)
                if (syöte_ARVO[Suorita_2 + merkki_ARVO] != laite_ARVO.lukea_Muisti(merkintä_ARVO_962f286b + merkki_ARVO)) 같음 = false;
            if (같음) return merkintä_ARVO_962f286b;
        }
        return 0;
    }

    static int vahvista(int tiedoston_nimi, int kesto_ARVO) {
        if (kesto_ARVO < 52 || numero(tiedoston_nimi) != 0x464c457f || laite_ARVO.lukea_Muisti(tiedoston_nimi + 4) != 1
            || laite_ARVO.lukea_Muisti(tiedoston_nimi + 5) != 1 || laite_ARVO.lukea_Muisti(tiedoston_nimi + 6) != 1
            || 짧은수(tiedoston_nimi + 16) != 2 || 짧은수(tiedoston_nimi + 18) != 3 || numero(tiedoston_nimi + 20) != 1
            || 짧은수(tiedoston_nimi + 40) != 52 || 짧은수(tiedoston_nimi + 42) != 32) return -8;
        int aloituskohta_ARVO = numero(tiedoston_nimi + 24);
        int taulukko_toimi = numero(tiedoston_nimi + 28);
        int kohde_LASKE = 짧은수(tiedoston_nimi + 44);
        if (kohde_LASKE == 0 || kohde_LASKE > 16 || taulukko_toimi < 52 || taulukko_toimi > kesto_ARVO - kohde_LASKE * 32) return -8;
        boolean tietojärjestelmät_suoritettava_tiedosto = false;
        for (int INDEKSI = 0; INDEKSI < kohde_LASKE; INDEKSI++) {
            int HAKU_taulukko = tiedoston_nimi + taulukko_toimi + INDEKSI * 32;
            int 종류 = numero(HAKU_taulukko);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Yhdistä/jäsennin_48ee4b1b 미지원
            if (종류 != 1) continue;
            int paikka = numero(HAKU_taulukko + 4), OSOITE = numero(HAKU_taulukko + 8), tiedostokoko = numero(HAKU_taulukko + 16), Muisti_muuttaa_kokoa = numero(HAKU_taulukko + 20);
            int tasaa_ARVO = numero(HAKU_taulukko + 28);
            if (OSOITE < alku_käyttäjä_ohjelma || OSOITE >= KUVA_lopettaa_puhelu_OSOITE || Muisti_muuttaa_kokoa < 0 || Muisti_muuttaa_kokoa > KUVA_lopettaa_puhelu_OSOITE - OSOITE
                || tiedostokoko < 0 || tiedostokoko > Muisti_muuttaa_kokoa || paikka < 0 || (tiedostokoko > 0 && paikka > kesto_ARVO - tiedostokoko)
                || (tasaa_ARVO != 0 && (tasaa_ARVO < 0 || (tasaa_ARVO & (tasaa_ARVO - 1)) != 0
                    || ((OSOITE - paikka) & (tasaa_ARVO - 1)) != 0))) return -8;
            for (int etukamera_ARVO = 0; etukamera_ARVO < INDEKSI; etukamera_ARVO++) {
                int Edellinen_kohde = tiedoston_nimi + taulukko_toimi + etukamera_ARVO * 32;
                if (numero(Edellinen_kohde) == 1 && Muisti_muuttaa_kokoa > 0 && numero(Edellinen_kohde + 20) > 0
                    && OSOITE < numero(Edellinen_kohde + 8) + numero(Edellinen_kohde + 20) && numero(Edellinen_kohde + 8) < OSOITE + Muisti_muuttaa_kokoa) return -8;
            }
            if ((numero(HAKU_taulukko + 24) & 1) != 0 && aloituskohta_ARVO >= OSOITE && aloituskohta_ARVO - OSOITE < tiedostokoko) tietojärjestelmät_suoritettava_tiedosto = true;
        }
        return tietojärjestelmät_suoritettava_tiedosto ? aloituskohta_ARVO : -8;
    }

    static int Suorita_komento(int[] syöte_ARVO, int Suorita_2, int kesto_ARVO) {
        while (Suorita_2 < kesto_ARVO && syöte_ARVO[Suorita_2] == ' ') Suorita_2++;
        int 끝 = Suorita_2;
        while (끝 < kesto_ARVO && syöte_ARVO[끝] != ' ') 끝++;
        int merkintä_ARVO_962f286b = ETSI_merkintä(syöte_ARVO, Suorita_2, 끝 - Suorita_2);
        if (merkintä_ARVO_962f286b == 0) return -2;
        int paikka = numero(merkintä_ARVO_962f286b + 16), Koko = numero(merkintä_ARVO_962f286b + 20);
        if (paikka < 8 + Ryhmä_LASKE() * 24 || Koko < 52 || paikka > laite_ARVO.suoritettava_tiedosto_nippu_muuttaa_kokoa() - Koko) return -8;
        int tiedoston_nimi = laite_ARVO.suoritettava_tiedosto_nippu() + paikka;
        int aloituskohta_ARVO = vahvista(tiedoston_nimi, Koko);
        if (aloituskohta_ARVO < 0) return aloituskohta_ARVO;
        laite_ARVO.käyttäjä_selvittää_Sisällys();
        int taulukko_toimi = numero(tiedoston_nimi + 28), kohde_LASKE = 짧은수(tiedoston_nimi + 44);
        for (int INDEKSI = 0; INDEKSI < kohde_LASKE; INDEKSI++) {
            int HAKU_taulukko = tiedoston_nimi + taulukko_toimi + INDEKSI * 32;
            if (numero(HAKU_taulukko) != 1) continue;
            int 원본 = tiedoston_nimi + numero(HAKU_taulukko + 4), kohde_ARVO = numero(HAKU_taulukko + 8), tiedostokoko = numero(HAKU_taulukko + 16);
            for (int tavu_ARVO = 0; tavu_ARVO < tiedostokoko; tavu_ARVO++) laite_ARVO.kirjoitus_Muisti(kohde_ARVO + tavu_ARVO, laite_ARVO.lukea_Muisti(원본 + tavu_ARVO));
        }
        argumentti_LASKE = 0;
        int Store_ARVO = argumentti_alku;
        while (끝 < kesto_ARVO) {
            while (끝 < kesto_ARVO && syöte_ARVO[끝] == ' ') 끝++;
            if (끝 == kesto_ARVO) break;
            if (argumentti_LASKE == argumentti_OSOITE.length) return -22;
            Suorita_2 = 끝;
            while (끝 < kesto_ARVO && syöte_ARVO[끝] != ' ') 끝++;
            argumentti_OSOITE[argumentti_LASKE++] = Store_ARVO;
            kirjoitus_numero(Store_ARVO, 끝 - Suorita_2);
            for (int merkki_ARVO = Suorita_2; merkki_ARVO < 끝; merkki_ARVO++) kirjoitus_numero(Store_ARVO + 4 + (merkki_ARVO - Suorita_2) * 4, syöte_ARVO[merkki_ARVO]);
            Store_ARVO += 4 + (끝 - Suorita_2) * 4;
        }
        verkko_Pino.SIIVOA_prosessi();
        파일서술자관리.alku_prosessi();
        int TULOS = laite_ARVO.suorittaa_käyttäjä_ohjelma(aloituskohta_ARVO, käyttäjä_lopettaa_puhelu - 16);
        파일서술자관리.SIIVOA_prosessi();
        verkko_Pino.SIIVOA_prosessi();
        return TULOS;
    }
}
