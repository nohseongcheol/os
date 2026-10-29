// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM tiedoston_nimi 64개, 파일당 16384바이트, 서술자 16개. 모든 data/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 VIRHE 번호다.
 */
public final class Muisti_Files {
    static final int Tiedosto_LASKE = 64;
    static int[] Nimi = new int[Tiedosto_LASKE * 64];
    static int[] 이름길이 = new int[Tiedosto_LASKE];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Sisältö_ARVO = new int[Tiedosto_LASKE * 4096];
    static int[] kesto_ARVO = new int[Tiedosto_LASKE];
    static int[] viite_LASKE = new int[Tiedosto_LASKE];
    static int[] käyttö_ARVO = new int[16];
    static int[] tavoite = new int[16];
    static int[] paikka = new int[16];
    static int[] menetelmä_tila = new int[16];
    static int[] polku_2 = new int[64];
    static int polku_kesto;

    public static int 파일한도() { return Tiedosto_LASKE; }
    static int lukea_data(int tiedoston_nimi, int sijainti) { return (Sisältö_ARVO[tiedoston_nimi * 4096 + sijainti / 4] >>> ((sijainti & 3) * 8)) & 255; }
    static void kirjoitus_data(int tiedoston_nimi, int sijainti, int ARVO) {
        int paikka_merkintä = tiedoston_nimi * 4096 + sijainti / 4, siirrä_ARVO_83b651b8 = (sijainti & 3) * 8;
        Sisältö_ARVO[paikka_merkintä] = (Sisältö_ARVO[paikka_merkintä] & ~(255 << siirrä_ARVO_83b651b8)) | ((ARVO & 255) << siirrä_ARVO_83b651b8);
    }

    public static int polku_alku(int Koko) {
        polku_kesto = 0;
        if (Koko < 1 || Koko > 63) return -36;
        polku_kesto = Koko;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < Koko; Loop_INDEKSI++) polku_2[Loop_INDEKSI] = 0;
        return 0;
    }
    public static int polku_tavu(int INDEKSI, int ARVO) {
        if (INDEKSI < 0 || INDEKSI >= polku_kesto || ARVO < 1 || ARVO > 255) return -22;
        polku_2[INDEKSI] = ARVO; return 0;
    }
    static int ETSI_merkintä() {
        for (int Tiedosto_INDEKSI = 0; Tiedosto_INDEKSI < Tiedosto_LASKE; Tiedosto_INDEKSI++) if (이름길이[Tiedosto_INDEKSI] > 0 && 이름길이[Tiedosto_INDEKSI] == Canonical_kesto && 접두(Nimi, Tiedosto_INDEKSI * 64, 이름길이[Tiedosto_INDEKSI], Canonical_ARVO, Canonical_kesto)) return Tiedosto_INDEKSI;
        return -1;
    }
    public static int Avaa(int 플래그) {
        if (polku_kesto == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < polku_kesto; Loop_INDEKSI++) if (polku_2[Loop_INDEKSI] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int TULOS = normalisoida_ARVO(); if (TULOS < 0) return TULOS;
        if (ETSI_Directory(Canonical_kesto) >= 0) return -21;
        TULOS = sekki_pää(); if (TULOS < 0) return TULOS;
        int tiedoston_nimi = ETSI_merkintä();
        if (tiedoston_nimi >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (tiedoston_nimi < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < 16; Loop_INDEKSI++) if (käyttö_ARVO[Loop_INDEKSI] == 0) { 서술자 = Loop_INDEKSI; break; }
        if (서술자 < 0) return -24;
        if (tiedoston_nimi < 0) {
            for (int Loop_INDEKSI = 0; Loop_INDEKSI < Tiedosto_LASKE; Loop_INDEKSI++) if (이름길이[Loop_INDEKSI] == 0 && viite_LASKE[Loop_INDEKSI] == 0) { tiedoston_nimi = Loop_INDEKSI; break; }
            if (tiedoston_nimi < 0) return -28;
            이름길이[tiedoston_nimi] = Canonical_kesto;
            for (int Loop_INDEKSI = 0; Loop_INDEKSI < Canonical_kesto; Loop_INDEKSI++) Nimi[tiedoston_nimi * 64 + Loop_INDEKSI] = Canonical_ARVO[Loop_INDEKSI];
            kesto_ARVO[tiedoston_nimi] = 0;
        }
        if ((플래그 & 0x200) != 0) kesto_ARVO[tiedoston_nimi] = 0;
        käyttö_ARVO[서술자] = 1; tavoite[서술자] = tiedoston_nimi; paikka[서술자] = 0; menetelmä_tila[서술자] = 플래그;
        viite_LASKE[tiedoston_nimi]++;
        return 서술자 + 3;
    }
    static int tarkistaa(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && käyttö_ARVO[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Luku(int 서술자) {
        int paikka_merkintä = tarkistaa(서술자);
        if (paikka_merkintä < 0 || (menetelmä_tila[paikka_merkintä] & 3) == 1) return -9;
        int tiedoston_nimi = tavoite[paikka_merkintä];
        if (paikka[paikka_merkintä] >= kesto_ARVO[tiedoston_nimi]) return 256; // EOF와 todellinen_data 0x00..0xff 구별
        return lukea_data(tiedoston_nimi, paikka[paikka_merkintä]++);
    }
    public static int Kirjoitus(int 서술자, int ARVO) {
        int paikka_merkintä = tarkistaa(서술자);
        if (paikka_merkintä < 0 || (menetelmä_tila[paikka_merkintä] & 3) == 0) return -9;
        int tiedoston_nimi = tavoite[paikka_merkintä];
        if ((menetelmä_tila[paikka_merkintä] & 0x400) != 0) paikka[paikka_merkintä] = kesto_ARVO[tiedoston_nimi];
        if (paikka[paikka_merkintä] >= 16384) return -28;
        while (kesto_ARVO[tiedoston_nimi] < paikka[paikka_merkintä]) kirjoitus_data(tiedoston_nimi, kesto_ARVO[tiedoston_nimi]++, 0);
        kirjoitus_data(tiedoston_nimi, paikka[paikka_merkintä]++, ARVO);
        if (kesto_ARVO[tiedoston_nimi] < paikka[paikka_merkintä]) kesto_ARVO[tiedoston_nimi] = paikka[paikka_merkintä];
        return 1;
    }
    public static int hae_toimi(int 서술자, int 거리, int aloite_juuri) {
        int paikka_merkintä = tarkistaa(서술자);
        if (paikka_merkintä < 0) return -9;
        if (aloite_juuri < 0 || aloite_juuri > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (aloite_juuri == 0 ? 0 : aloite_juuri == 1 ? paikka[paikka_merkintä] : kesto_ARVO[tavoite[paikka_merkintä]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        paikka[paikka_merkintä] = 새위치; return 새위치;
    }
    public static int Sulje(int 서술자) {
        int paikka_merkintä = tarkistaa(서술자);
        if (paikka_merkintä < 0) return -9;
        viite_LASKE[tavoite[paikka_merkintä]]--; käyttö_ARVO[paikka_merkintä] = 0; return 0;
    }
    public static int Koko(int 서술자) {
        int paikka_merkintä = tarkistaa(서술자); return paikka_merkintä < 0 ? -9 : kesto_ARVO[tavoite[paikka_merkintä]];
    }
    public static int ryhmä_kesto(int 서술자, int Koko) {
        int paikka_merkintä = tarkistaa(서술자);
        if (paikka_merkintä < 0 || (menetelmä_tila[paikka_merkintä] & 3) == 0) return -9;
        if (Koko < 0 || Koko > 16384) return -22;
        int tiedoston_nimi = tavoite[paikka_merkintä];
        while (kesto_ARVO[tiedoston_nimi] < Koko) kirjoitus_data(tiedoston_nimi, kesto_ARVO[tiedoston_nimi]++, 0);
        kesto_ARVO[tiedoston_nimi] = Koko; return 0;
    }
    public static int poistaa_merkintä_c8dbc399() {
        if (polku_kesto == 0) return -22;
        int TULOS = normalisoida_ARVO(); if (TULOS < 0) return TULOS;
        if (ETSI_Directory(Canonical_kesto) >= 0) return -21;
        TULOS = sekki_pää(); if (TULOS < 0) return TULOS;
        int tiedoston_nimi = ETSI_merkintä();
        if (tiedoston_nimi < 0) return -2;
        이름길이[tiedoston_nimi] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void merkintä_luettelo() {
        polku_alku(1); polku_tavu(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEKSI) {
        if (INDEKSI < 0 || INDEKSI >= Tiedosto_LASKE || 이름길이[INDEKSI] == 0) return 0;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < 이름길이[INDEKSI]; Loop_INDEKSI++) if (Nimi[INDEKSI * 64 + Loop_INDEKSI] == '/') return 0;
        return 이름길이[INDEKSI];
    }
    public static int 공개이름바이트(int INDEKSI, int sijainti) {
        return INDEKSI >= 0 && INDEKSI < Tiedosto_LASKE && sijainti >= 0 && sijainti < 이름길이[INDEKSI] ? Nimi[INDEKSI * 64 + sijainti] : -22;
    }
    public static int 공개파일크기(int INDEKSI) { return INDEKSI >= 0 && INDEKSI < Tiedosto_LASKE ? kesto_ARVO[INDEKSI] : -22; }
    static int[] Canonical_ARVO = new int[64], nykyinen_kohde = new int[64], Directory_nimi = new int[16 * 64], Directory_kesto = new int[16];
    static int Canonical_kesto, nykyinen_kesto;
    static boolean 접두(int[] 이름들, int Suorita_2, int polku_ARVO, int[] etukamera_ARVO, int riviväli_polku) {
        if (polku_ARVO < riviväli_polku) return false;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < riviväli_polku; Loop_INDEKSI++) if (이름들[Suorita_2 + Loop_INDEKSI] != etukamera_ARVO[Loop_INDEKSI]) return false;
        return true;
    }
    static int normalisoida_ARVO() {
        if (polku_kesto == 0) return -22;
        Canonical_kesto = polku_2[0] == '/' ? 0 : nykyinen_kesto;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < Canonical_kesto; Loop_INDEKSI++) Canonical_ARVO[Loop_INDEKSI] = nykyinen_kohde[Loop_INDEKSI];
        int lukea_kohdistin = 0;
        while (lukea_kohdistin < polku_kesto) {
            while (lukea_kohdistin < polku_kesto && polku_2[lukea_kohdistin] == '/') lukea_kohdistin++;
            int alku_toimi = lukea_kohdistin; while (lukea_kohdistin < polku_kesto && polku_2[lukea_kohdistin] != '/') { if (polku_2[lukea_kohdistin] == 0) return -22; lukea_kohdistin++; }
            int merkintä_LASKE = lukea_kohdistin - alku_toimi; if (merkintä_LASKE == 0 || merkintä_LASKE == 1 && polku_2[alku_toimi] == '.') continue;
            if (merkintä_LASKE == 2 && polku_2[alku_toimi] == '.' && polku_2[alku_toimi + 1] == '.') {
                while (Canonical_kesto > 0 && Canonical_ARVO[Canonical_kesto - 1] != '/') Canonical_kesto--;
                if (Canonical_kesto > 0) Canonical_kesto--;
                continue;
            }
            if (Canonical_kesto + merkintä_LASKE + (Canonical_kesto == 0 ? 0 : 1) > 63) return -36;
            if (Canonical_kesto > 0) Canonical_ARVO[Canonical_kesto++] = '/';
            for (int Loop_INDEKSI = alku_toimi; Loop_INDEKSI < lukea_kohdistin; Loop_INDEKSI++) Canonical_ARVO[Canonical_kesto++] = polku_2[Loop_INDEKSI];
        }
        return 0;
    }
    static int ETSI_Directory(int merkintä_LASKE) {
        if (merkintä_LASKE == 0) return 0;
        for (int Loop_INDEKSI = 1; Loop_INDEKSI < 16; Loop_INDEKSI++) if (Directory_kesto[Loop_INDEKSI] == merkintä_LASKE && 접두(Directory_nimi, Loop_INDEKSI * 64, merkintä_LASKE, Canonical_ARVO, merkintä_LASKE)) return Loop_INDEKSI;
        return -1;
    }
    static int sekki_pää() {
        int merkintä_LASKE = Canonical_kesto; while (merkintä_LASKE > 0 && Canonical_ARVO[merkintä_LASKE - 1] != '/') merkintä_LASKE--;
        return ETSI_Directory(merkintä_LASKE == 0 ? 0 : merkintä_LASKE - 1) < 0 ? -2 : 0;
    }
    public static int Luo_Directory() {
        int 처리값 = normalisoida_ARVO(); if (처리값 < 0) return 처리값;
        if (ETSI_Directory(Canonical_kesto) >= 0 || ETSI_merkintä() >= 0) return -17;
        처리값 = sekki_pää(); if (처리값 < 0) return 처리값;
        for (int Loop_INDEKSI = 1; Loop_INDEKSI < 16; Loop_INDEKSI++) if (Directory_kesto[Loop_INDEKSI] == 0) {
            Directory_kesto[Loop_INDEKSI] = Canonical_kesto; for (int sisäliitos_toimi = 0; sisäliitos_toimi < Canonical_kesto; sisäliitos_toimi++) Directory_nimi[Loop_INDEKSI * 64 + sisäliitos_toimi] = Canonical_ARVO[sisäliitos_toimi]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = normalisoida_ARVO(); if (처리값 < 0) return 처리값;
        if (ETSI_Directory(Canonical_kesto) >= 0) return 2;
        return ETSI_merkintä() >= 0 ? 1 : 0;
    }
    public static int muuttaa_Directory() {
        int 처리값 = normalisoida_ARVO(); if (처리값 < 0) return 처리값;
        if (ETSI_Directory(Canonical_kesto) < 0) return -2;
        nykyinen_kesto = Canonical_kesto; for (int Loop_INDEKSI = 0; Loop_INDEKSI < nykyinen_kesto; Loop_INDEKSI++) nykyinen_kohde[Loop_INDEKSI] = Canonical_ARVO[Loop_INDEKSI]; return 0;
    }
    public static int poistaa_Directory() {
        int 처리값 = normalisoida_ARVO(); if (처리값 < 0) return 처리값;
        int Directory_numero = ETSI_Directory(Canonical_kesto); if (Directory_numero < 0) return -2; if (Directory_numero == 0) return -16;
        if (nykyinen_kesto == Canonical_kesto && 접두(nykyinen_kohde, 0, nykyinen_kesto, Canonical_ARVO, Canonical_kesto)) return -16;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < Tiedosto_LASKE; Loop_INDEKSI++) {
            if (이름길이[Loop_INDEKSI] > Canonical_kesto && 접두(Nimi, Loop_INDEKSI * 64, 이름길이[Loop_INDEKSI], Canonical_ARVO, Canonical_kesto) && Nimi[Loop_INDEKSI * 64 + Canonical_kesto] == '/') return -39;
        }
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < 16; Loop_INDEKSI++) {
            if (Directory_kesto[Loop_INDEKSI] > Canonical_kesto && 접두(Directory_nimi, Loop_INDEKSI * 64, Directory_kesto[Loop_INDEKSI], Canonical_ARVO, Canonical_kesto) && Directory_nimi[Loop_INDEKSI * 64 + Canonical_kesto] == '/') return -39;
        }
        Directory_kesto[Directory_numero] = 0; return 0;
    }
    public static int Nimeä_uudelleen_merkintä(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= Tiedosto_LASKE || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normalisoida_ARVO(); if (처리값 < 0) return 처리값;
        if (ETSI_Directory(Canonical_kesto) >= 0) return -21;
        처리값 = sekki_pää(); if (처리값 < 0) return 처리값;
        int Edellinen_ARVO = ETSI_merkintä(); if (Edellinen_ARVO == 원본번호) return 0;
        if (Edellinen_ARVO >= 0) 이름길이[Edellinen_ARVO] = 0;
        이름길이[원본번호] = Canonical_kesto; for (int Loop_INDEKSI = 0; Loop_INDEKSI < Canonical_kesto; Loop_INDEKSI++) Nimi[원본번호 * 64 + Loop_INDEKSI] = Canonical_ARVO[Loop_INDEKSI]; return 0;
    }
    static int merkintä_alku(int[] data_MATRIISI, int 시작점, int merkintä_LASKE) {
        if (!접두(data_MATRIISI, 시작점, merkintä_LASKE, Canonical_ARVO, Canonical_kesto)) return -1;
        int alku_toimi = Canonical_kesto;
        if (alku_toimi > 0) { if (merkintä_LASKE <= alku_toimi || data_MATRIISI[시작점 + alku_toimi] != '/') return -1; alku_toimi++; }
        if (merkintä_LASKE <= alku_toimi) return -1;
        for (int Loop_INDEKSI = alku_toimi; Loop_INDEKSI < merkintä_LASKE; Loop_INDEKSI++) if (data_MATRIISI[시작점 + Loop_INDEKSI] == '/') return -1;
        return alku_toimi;
    }
    static void nykyinen_kirjoitus() { 단말.문자('/'); for (int Loop_INDEKSI = 0; Loop_INDEKSI < nykyinen_kesto; Loop_INDEKSI++) Taulu.직렬쓰기(nykyinen_kohde[Loop_INDEKSI]); }
    static int 경로목록() {
        int 처리값 = normalisoida_ARVO(); if (처리값 < 0) return 처리값;
        int Tiedosto_tavoite = ETSI_merkintä();
        if (Tiedosto_tavoite >= 0) { for (int Loop_INDEKSI = 0; Loop_INDEKSI < Canonical_kesto; Loop_INDEKSI++) Taulu.직렬쓰기(Canonical_ARVO[Loop_INDEKSI]); 단말.Kirjoitus("  "); 단말.numero(kesto_ARVO[Tiedosto_tavoite]); 단말.Kirjoitus("tavu_ARVO(주기억 tiedoston_nimi)\n"); return 0; }
        if (ETSI_Directory(Canonical_kesto) < 0) return -2;
        for (int seuraava_ARVO = 1; seuraava_ARVO < 16; seuraava_ARVO++) if (Directory_kesto[seuraava_ARVO] > 0) {
            int alku_toimi = merkintä_alku(Directory_nimi, seuraava_ARVO * 64, Directory_kesto[seuraava_ARVO]); if (alku_toimi < 0) continue;
            for (int Loop_INDEKSI = alku_toimi; Loop_INDEKSI < Directory_kesto[seuraava_ARVO]; Loop_INDEKSI++) Taulu.직렬쓰기(Directory_nimi[seuraava_ARVO * 64 + Loop_INDEKSI]); 단말.Kirjoitus("/\n");
        }
        for (int Tiedosto_INDEKSI = 0; Tiedosto_INDEKSI < Tiedosto_LASKE; Tiedosto_INDEKSI++) if (이름길이[Tiedosto_INDEKSI] > 0) {
            int alku_toimi = merkintä_alku(Nimi, Tiedosto_INDEKSI * 64, 이름길이[Tiedosto_INDEKSI]); if (alku_toimi < 0) continue;
            for (int Loop_INDEKSI = alku_toimi; Loop_INDEKSI < 이름길이[Tiedosto_INDEKSI]; Loop_INDEKSI++) Taulu.직렬쓰기(Nimi[Tiedosto_INDEKSI * 64 + Loop_INDEKSI]);
            단말.Kirjoitus("  "); 단말.numero(kesto_ARVO[Tiedosto_INDEKSI]); 단말.Kirjoitus("tavu_ARVO(주기억 tiedoston_nimi)\n");
        }
        return 0;
    }
}
