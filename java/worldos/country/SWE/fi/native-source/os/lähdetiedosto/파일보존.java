// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_ARVO muoto_ARVO. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] Tiedosto_taulukko = new int[1024];
    static int 바이트해시(int ARVO, int data) { return (ARVO ^ data) * 16777619; }
    static void selvittää_data() {
        for (int INDEKSI = 0; INDEKSI < 512; INDEKSI++) tallennuslaite_yhteys.osa_data[INDEKSI] = 0;
    }
    static int taulukko_kokonaisluku(int paikka) {
        return Tiedosto_taulukko[paikka] | Tiedosto_taulukko[paikka + 1] << 8 | Tiedosto_taulukko[paikka + 2] << 16 | Tiedosto_taulukko[paikka + 3] << 24;
    }
    static void kirjoitus_taulukko_kokonaisluku(int paikka, int ARVO) {
        for (int INDEKSI = 0; INDEKSI < 4; INDEKSI++) Tiedosto_taulukko[paikka + INDEKSI] = (ARVO >>> (INDEKSI * 8)) & 255;
    }
    static boolean sekki_taulukko() {
        for (int tiedoston_nimi = 0; tiedoston_nimi < 8; tiedoston_nimi++) {
            int kesto_ARVO = 0;
            for (int paikka_merkintä = 0; paikka_merkintä < 64; paikka_merkintä++) Muisti_tiedostojärjestelmä.Nimi[paikka_merkintä] = Tiedosto_taulukko[tiedoston_nimi * 72 + paikka_merkintä];
            while (kesto_ARVO < 64 && Muisti_tiedostojärjestelmä.Nimi[kesto_ARVO] != 0) kesto_ARVO++;
            if (kesto_ARVO == 0) continue;
            if (!Muisti_tiedostojärjestelmä.sekki_nimi(Muisti_tiedostojärjestelmä.Nimi, kesto_ARVO)
                || taulukko_kokonaisluku(tiedoston_nimi * 72 + 64) < 0 || taulukko_kokonaisluku(tiedoston_nimi * 72 + 64) > 16384) return false;
            for (int etukamera_ARVO = 0; etukamera_ARVO < tiedoston_nimi; etukamera_ARVO++) {
                boolean 같음 = Tiedosto_taulukko[etukamera_ARVO * 72 + kesto_ARVO] == 0;
                for (int paikka_merkintä = 0; paikka_merkintä < kesto_ARVO; paikka_merkintä++) if (Tiedosto_taulukko[etukamera_ARVO * 72 + paikka_merkintä] != Muisti_tiedostojärjestelmä.Nimi[paikka_merkintä]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int alku_osa = 1 + 보존본 * 259;
        if (tallennuslaite_yhteys.Luku(alku_osa) < 0 || tallennuslaite_yhteys.jäsentää_kokonaisluku(0) != 0x4a4b534e) return -1;
        int 세대 = tallennuslaite_yhteys.jäsentää_kokonaisluku(4), tarkistussumma = tallennuslaite_yhteys.jäsentää_kokonaisluku(8);
        if (세대 < 1 || tallennuslaite_yhteys.jäsentää_kokonaisluku(12) != (세대 ^ tarkistussumma ^ 0x4a4b534e)) return -1;
        int hajautusarvo_Tiedosto = 0x811c9dc5;
        for (int osa_ARVO = 0; osa_ARVO < 258; osa_ARVO++) {
            if (tallennuslaite_yhteys.Luku(alku_osa + 1 + osa_ARVO) < 0) return -1;
            for (int paikka_merkintä = 0; paikka_merkintä < 512; paikka_merkintä++) {
                int ARVO = tallennuslaite_yhteys.osa_data[paikka_merkintä];
                hajautusarvo_Tiedosto = 바이트해시(hajautusarvo_Tiedosto, ARVO);
                if (osa_ARVO < 2) Tiedosto_taulukko[osa_ARVO * 512 + paikka_merkintä] = ARVO;
            }
        }
        return hajautusarvo_Tiedosto == tarkistussumma && sekki_taulukko() ? 세대 : -1;
    }
    static int Verkkokuorma(int 보존본) {
        int alku_osa = 1 + 보존본 * 259;
        for (int osa_ARVO = 0; osa_ARVO < 2; osa_ARVO++) {
            if (tallennuslaite_yhteys.Luku(alku_osa + 1 + osa_ARVO) < 0) return -5;
            for (int paikka_merkintä = 0; paikka_merkintä < 512; paikka_merkintä++) Tiedosto_taulukko[osa_ARVO * 512 + paikka_merkintä] = tallennuslaite_yhteys.osa_data[paikka_merkintä];
        }
        for (int tiedoston_nimi = 0; tiedoston_nimi < 8; tiedoston_nimi++) {
            for (int paikka_merkintä = 0; paikka_merkintä < 64; paikka_merkintä++) Muisti_tiedostojärjestelmä.이름들[tiedoston_nimi * 64 + paikka_merkintä] = Tiedosto_taulukko[tiedoston_nimi * 72 + paikka_merkintä];
            Muisti_tiedostojärjestelmä.muuttaa_kokoa_luettelo[tiedoston_nimi] = Tiedosto_taulukko[tiedoston_nimi * 72] == 0 ? 0 : taulukko_kokonaisluku(tiedoston_nimi * 72 + 64);
            Muisti_tiedostojärjestelmä.허가들[tiedoston_nimi] = taulukko_kokonaisluku(tiedoston_nimi * 72 + 68) & 511;
            for (int osa_ARVO = 0; osa_ARVO < 32; osa_ARVO++) {
                if (tallennuslaite_yhteys.Luku(alku_osa + 3 + tiedoston_nimi * 32 + osa_ARVO) < 0) return -5;
                int OSOITE = laite_ARVO.Tiedosto_Muisti() + tiedoston_nimi * 16384 + osa_ARVO * 512;
                for (int paikka_merkintä = 0; paikka_merkintä < 512; paikka_merkintä++) laite_ARVO.kirjoitus_Muisti(OSOITE + paikka_merkintä, tallennuslaite_yhteys.osa_data[paikka_merkintä]);
            }
        }
        return 0;
    }
    static void Valmistele() {
        if (tallennuslaite_yhteys.Luku(0) < 0 || tallennuslaite_yhteys.jäsentää_kokonaisluku(0) != 0x54534b4a
            || tallennuslaite_yhteys.jäsentää_kokonaisluku(4) != 0x3145524f || tallennuslaite_yhteys.jäsentää_kokonaisluku(8) != 2048
            || tallennuslaite_yhteys.jäsentää_kokonaisluku(12) != 0x3153464a) {
            SMS_Pääte.Kirjoitus("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        tallennuslaite_yhteys.tietojärjestelmät_Aktiivinen_9e72441a = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Pääte.Kirjoitus("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (Verkkokuorma(현재보존본) < 0) {
            SMS_Pääte.Kirjoitus("STORE read failed; halted to preserve files\n"); laite_ARVO.정지();
        }
        SMS_Pääte.Kirjoitus("STORE restored generation "); SMS_Pääte.kirjoitus_numero(세대번호); SMS_Pääte.문자(10);
    }
    static int synkronoi() {
        if (!tallennuslaite_yhteys.tietojärjestelmät_Aktiivinen_9e72441a) return -19;
        if (세대번호 == 2147483647) return -75;
        int Seuraava_kohde = 현재보존본 == 0 ? 1 : 0, alku_osa = 1 + Seuraava_kohde * 259;
        // 새 본문보다 먼저 Edellinen_kohde commit을 무효화하고 laite_ARVO 캐시를 비운다.
        selvittää_data();
        if (tallennuslaite_yhteys.Kirjoitus(alku_osa) < 0 || tallennuslaite_yhteys.밀어쓰기() < 0) return -5;
        for (int paikka_merkintä = 0; paikka_merkintä < 1024; paikka_merkintä++) Tiedosto_taulukko[paikka_merkintä] = 0;
        for (int tiedoston_nimi = 0; tiedoston_nimi < 8; tiedoston_nimi++) if (Muisti_tiedostojärjestelmä.이름들[tiedoston_nimi * 64] != 0) {
            for (int paikka_merkintä = 0; paikka_merkintä < 64; paikka_merkintä++) Tiedosto_taulukko[tiedoston_nimi * 72 + paikka_merkintä] = Muisti_tiedostojärjestelmä.이름들[tiedoston_nimi * 64 + paikka_merkintä];
            kirjoitus_taulukko_kokonaisluku(tiedoston_nimi * 72 + 64, Muisti_tiedostojärjestelmä.muuttaa_kokoa_luettelo[tiedoston_nimi]);
            kirjoitus_taulukko_kokonaisluku(tiedoston_nimi * 72 + 68, Muisti_tiedostojärjestelmä.허가들[tiedoston_nimi]);
        }
        int hajautusarvo_Tiedosto = 0x811c9dc5;
        for (int osa_ARVO = 0; osa_ARVO < 258; osa_ARVO++) {
            for (int paikka_merkintä = 0; paikka_merkintä < 512; paikka_merkintä++) {
                int ARVO = 0;
                if (osa_ARVO < 2) ARVO = Tiedosto_taulukko[osa_ARVO * 512 + paikka_merkintä];
                else {
                    int tiedoston_nimi = (osa_ARVO - 2) / 32, paikka = (osa_ARVO - 2) % 32 * 512 + paikka_merkintä;
                    if (Tiedosto_taulukko[tiedoston_nimi * 72] != 0 && paikka < Muisti_tiedostojärjestelmä.muuttaa_kokoa_luettelo[tiedoston_nimi])
                        ARVO = laite_ARVO.lukea_Muisti(laite_ARVO.Tiedosto_Muisti() + tiedoston_nimi * 16384 + paikka);
                }
                tallennuslaite_yhteys.osa_data[paikka_merkintä] = ARVO; hajautusarvo_Tiedosto = 바이트해시(hajautusarvo_Tiedosto, ARVO);
            }
            if (tallennuslaite_yhteys.Kirjoitus(alku_osa + 1 + osa_ARVO) < 0) return -5;
        }
        if (tallennuslaite_yhteys.밀어쓰기() < 0) return -5;
        selvittää_data(); tallennuslaite_yhteys.kirjoitus_kokonaisluku_ARVO(0, 0x4a4b534e);
        tallennuslaite_yhteys.kirjoitus_kokonaisluku_ARVO(4, 세대번호 + 1); tallennuslaite_yhteys.kirjoitus_kokonaisluku_ARVO(8, hajautusarvo_Tiedosto);
        tallennuslaite_yhteys.kirjoitus_kokonaisluku_ARVO(12, (세대번호 + 1) ^ hajautusarvo_Tiedosto ^ 0x4a4b534e);
        if (tallennuslaite_yhteys.Kirjoitus(alku_osa) < 0 || tallennuslaite_yhteys.밀어쓰기() < 0) return -5;
        현재보존본 = Seuraava_kohde; 세대번호++;
        return 0;
    }
}
