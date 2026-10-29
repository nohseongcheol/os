// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 käyttäjätila 과정의 파일서술자와 열린 tiedoston_nimi 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int luku_ja_kirjoitus_merkitä = 2, Luo_merkintä = 64, 독점생성 = 128, selvittää_Sisällys = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] avata_kahva = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], tavoite = new int[서술자한도];
    static int[] Tiedosto_toimi = new int[서술자한도], avata_Asetukset = new int[서술자한도], viite_LASKE = new int[서술자한도];
    static int[] verkko_kahva = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] polku_nimi = new int[64], Siirrä_data = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return avata_kahva[파일서술자] - 1;
    }
    static int 빈서술자(int Suorita_2) {
        for (int INDEKSI = Suorita_2; INDEKSI < 서술자한도; INDEKSI++) if (avata_kahva[INDEKSI] == 0) return INDEKSI;
        return -24;
    }
    static int 빈기술() {
        for (int INDEKSI = 0; INDEKSI < 서술자한도; INDEKSI++) if (viite_LASKE[INDEKSI] == 0) return INDEKSI;
        return -24;
    }
    static int Yhdistä(int 서술자, int 기술, int 파일종류, int Tiedosto_tavoite, int Asetukset) {
        avata_kahva[서술자] = 기술 + 1; 서술자설정[서술자] = (Asetukset & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; tavoite[기술] = Tiedosto_tavoite; viite_LASKE[기술] = 1;
        avata_Asetukset[기술] = Asetukset & (3 | 이어쓰기 | 기다리지않기); Tiedosto_toimi[기술] = 0;
        verkko_kahva[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void alku_prosessi() {
        SIIVOA_prosessi();
        for (int INDEKSI = 0; INDEKSI < 3; INDEKSI++) Yhdistä(INDEKSI, INDEKSI, 1, INDEKSI, INDEKSI == 0 ? 0 : 1);
    }
    static void SIIVOA_prosessi() {
        for (int INDEKSI = 0; INDEKSI < 서술자한도; INDEKSI++) if (avata_kahva[INDEKSI] != 0) Sulje_Tiedosto(INDEKSI);
    }
    static int Sulje_Tiedosto(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        avata_kahva[서술자] = 0; 서술자설정[서술자] = 0;
        viite_LASKE[기술]--;
        if (viite_LASKE[기술] == 0) {
            if (종류[기술] == 2) Muisti_tiedostojärjestelmä.avata_LASKE[tavoite[기술]]--;
            if (종류[기술] == 3 && verkko_kahva[기술] != 0) verkko_Pino.Sulje(verkko_kahva[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 tavu_ARVO 문자열이다. 루트의 한 이름만 지원한다.
    static int lukea_polku(int OSOITE) {
        if (!suoritus_Valvoja.leikata(OSOITE, 1)) return -14;
        int paikka = laite_ARVO.lukea_Muisti(OSOITE) == '/' ? 1 : 0;
        for (int kesto_ARVO = 0; kesto_ARVO < 64; kesto_ARVO++) {
            if (!suoritus_Valvoja.leikata(OSOITE + paikka + kesto_ARVO, 1)) return -14;
            int ARVO = laite_ARVO.lukea_Muisti(OSOITE + paikka + kesto_ARVO);
            polku_nimi[kesto_ARVO] = ARVO;
            if (ARVO == 0) return kesto_ARVO == 0 ? -2 : (Muisti_tiedostojärjestelmä.sekki_nimi(polku_nimi, kesto_ARVO) ? kesto_ARVO : -22);
            if (ARVO == '/') return -20;
        }
        return -36;
    }
    static int avata_Tiedosto(int nimi_OSOITE, int Asetukset, int 허가) {
        int kesto_ARVO = lukea_polku(nimi_OSOITE);
        if (kesto_ARVO < 0) return kesto_ARVO;
        if ((Asetukset & ~(3 | Luo_merkintä | 독점생성 | selvittää_Sisällys | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Asetukset & 3) == 3 || ((Asetukset & selvittää_Sisällys) != 0 && (Asetukset & 3) == 0)) return -22;
        int tiedoston_nimi = Muisti_tiedostojärjestelmä.ETSI_merkintä(polku_nimi, kesto_ARVO);
        if (tiedoston_nimi >= 0 && (Asetukset & (Luo_merkintä | 독점생성)) == (Luo_merkintä | 독점생성)) return -17;
        if (tiedoston_nimi == -2 && (Asetukset & Luo_merkintä) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = 빈기술();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (tiedoston_nimi == -2) {
            int TULOS = Muisti_tiedostojärjestelmä.Store_ARVO(polku_nimi, kesto_ARVO, polku_nimi, 0);
            if (TULOS < 0) return TULOS;
            tiedoston_nimi = Muisti_tiedostojärjestelmä.ETSI_merkintä(polku_nimi, kesto_ARVO);
            Muisti_tiedostojärjestelmä.허가들[tiedoston_nimi] = 허가 & 511;
        }
        if (tiedoston_nimi < 0) return tiedoston_nimi;
        if ((Asetukset & selvittää_Sisällys) != 0) Muisti_tiedostojärjestelmä.muuttaa_kokoa_luettelo[tiedoston_nimi] = 0;
        Muisti_tiedostojärjestelmä.avata_LASKE[tiedoston_nimi]++;
        return Yhdistä(서술자, 기술, 2, tiedoston_nimi, Asetukset);
    }
    static int lukea_Tiedosto(int 서술자, int data_OSOITE, int kesto_ARVO) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (avata_Asetukset[기술] & 3) == 1) return -9;
        if (kesto_ARVO < 0) return -22;
        if (kesto_ARVO == 0) return 0;
        if (!suoritus_Valvoja.leikata(data_OSOITE, kesto_ARVO)) return -14;
        if (종류[기술] == 3) return saada_datagrammi_data(서술자, data_OSOITE, kesto_ARVO, 0, 0);
        if (종류[기술] == 1) {
            int SAATU_HINTA_LASKE = 0;
            while (SAATU_HINTA_LASKE < kesto_ARVO) {
                int ARVO = SMS_Pääte.직렬읽기();
                if (ARVO < 0) ARVO = näppäimistö.Luku();
                if (ARVO < 0) {
                    if (SAATU_HINTA_LASKE > 0) return SAATU_HINTA_LASKE;
                    if ((avata_Asetukset[기술] & 기다리지않기) != 0) return -11;
                    if (laite_ARVO.사용자남은밀리초() <= 10) return -11;
                    verkko_Pino.tarkistaa(); laite_ARVO.잠시양보();
                } else {
                    laite_ARVO.kirjoitus_Muisti(data_OSOITE + SAATU_HINTA_LASKE, ARVO); SAATU_HINTA_LASKE++;
                }
            }
            return SAATU_HINTA_LASKE;
        }
        int tiedoston_nimi = tavoite[기술], paikka = Tiedosto_toimi[기술];
        if (paikka >= Muisti_tiedostojärjestelmä.muuttaa_kokoa_luettelo[tiedoston_nimi]) return 0;
        if (kesto_ARVO > Muisti_tiedostojärjestelmä.muuttaa_kokoa_luettelo[tiedoston_nimi] - paikka) kesto_ARVO = Muisti_tiedostojärjestelmä.muuttaa_kokoa_luettelo[tiedoston_nimi] - paikka;
        int 원본주소 = laite_ARVO.Tiedosto_Muisti() + tiedoston_nimi * Muisti_tiedostojärjestelmä.최대크기 + paikka;
        for (int INDEKSI = 0; INDEKSI < kesto_ARVO; INDEKSI++) laite_ARVO.kirjoitus_Muisti(data_OSOITE + INDEKSI, laite_ARVO.lukea_Muisti(원본주소 + INDEKSI));
        Tiedosto_toimi[기술] += kesto_ARVO;
        return kesto_ARVO;
    }
    static int kirjoitus_Tiedosto(int 서술자, int data_OSOITE, int kesto_ARVO) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (avata_Asetukset[기술] & 3) == 0) return -9;
        if (kesto_ARVO < 0) return -22;
        if (kesto_ARVO == 0) return 0;
        if (!suoritus_Valvoja.leikata(data_OSOITE, kesto_ARVO)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 kohde_ARVO 주소가 필요하다.
        if (종류[기술] == 1) {
            if (kesto_ARVO > 16384) kesto_ARVO = 16384;
            for (int INDEKSI = 0; INDEKSI < kesto_ARVO; INDEKSI++) {
                int ARVO = laite_ARVO.lukea_Muisti(data_OSOITE + INDEKSI);
                SMS_Pääte.직렬바이트(ARVO); SMS_Pääte.화면문자(ARVO);
            }
            return kesto_ARVO;
        }
        int tiedoston_nimi = tavoite[기술], Koko = Muisti_tiedostojärjestelmä.muuttaa_kokoa_luettelo[tiedoston_nimi];
        int paikka = (avata_Asetukset[기술] & 이어쓰기) != 0 ? Koko : Tiedosto_toimi[기술];
        if (paikka >= Muisti_tiedostojärjestelmä.최대크기) return -27;
        if (kesto_ARVO > Muisti_tiedostojärjestelmä.최대크기 - paikka) kesto_ARVO = Muisti_tiedostojärjestelmä.최대크기 - paikka;
        int kohde_OSOITE_08bbd577 = laite_ARVO.Tiedosto_Muisti() + tiedoston_nimi * Muisti_tiedostojärjestelmä.최대크기;
        for (int INDEKSI = Koko; INDEKSI < paikka; INDEKSI++) laite_ARVO.kirjoitus_Muisti(kohde_OSOITE_08bbd577 + INDEKSI, 0);
        for (int INDEKSI = 0; INDEKSI < kesto_ARVO; INDEKSI++) laite_ARVO.kirjoitus_Muisti(kohde_OSOITE_08bbd577 + paikka + INDEKSI, laite_ARVO.lukea_Muisti(data_OSOITE + INDEKSI));
        Tiedosto_toimi[기술] = paikka + kesto_ARVO;
        if (paikka + kesto_ARVO > Koko) Muisti_tiedostojärjestelmä.muuttaa_kokoa_luettelo[tiedoston_nimi] = paikka + kesto_ARVO;
        return kesto_ARVO;
    }
    static int hae_Tiedosto(int 서술자, int SIIRTYMÄ_ARVO, int aloite_juuri) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (aloite_juuri < 0 || aloite_juuri > 2) return -22;
        int Tausta_ARVO = aloite_juuri == 0 ? 0 : (aloite_juuri == 1 ? Tiedosto_toimi[기술] : Muisti_tiedostojärjestelmä.muuttaa_kokoa_luettelo[tavoite[기술]]);
        if (SIIRTYMÄ_ARVO > 0 && Tausta_ARVO > 2147483647 - SIIRTYMÄ_ARVO) return -75;
        if (SIIRTYMÄ_ARVO < 0 && SIIRTYMÄ_ARVO < -Tausta_ARVO) return -22;
        Tiedosto_toimi[기술] = Tausta_ARVO + SIIRTYMÄ_ARVO;
        return Tiedosto_toimi[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean Määritä_ARVO, int Asetukset) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return Määritä_ARVO ? -9 : -22;
        if (Määritä_ARVO && 서술자 == 새서술자) return 새서술자;
        if (Määritä_ARVO) { if (avata_kahva[새서술자] != 0) Sulje_Tiedosto(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        avata_kahva[새서술자] = 기술 + 1; 서술자설정[새서술자] = Asetukset; viite_LASKE[기술]++;
        return 새서술자;
    }
    static int poistaa_Tiedosto_merkintä_nimi(int nimi_OSOITE) {
        int kesto_ARVO = lukea_polku(nimi_OSOITE);
        if (kesto_ARVO < 0) return kesto_ARVO;
        int tiedoston_nimi = Muisti_tiedostojärjestelmä.ETSI_merkintä(polku_nimi, kesto_ARVO);
        if (tiedoston_nimi < 0) return tiedoston_nimi;
        Muisti_tiedostojärjestelmä.이름들[tiedoston_nimi * 64] = 0;
        return 0;
    }
    static int ryhmä_Tiedosto_kesto(int 서술자, int kesto_ARVO) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (avata_Asetukset[기술] & 3) == 0 || kesto_ARVO < 0) return -22;
        if (kesto_ARVO > Muisti_tiedostojärjestelmä.최대크기) return -27;
        int tiedoston_nimi = tavoite[기술], OSOITE = laite_ARVO.Tiedosto_Muisti() + tiedoston_nimi * Muisti_tiedostojärjestelmä.최대크기;
        for (int INDEKSI = Muisti_tiedostojärjestelmä.muuttaa_kokoa_luettelo[tiedoston_nimi]; INDEKSI < kesto_ARVO; INDEKSI++) laite_ARVO.kirjoitus_Muisti(OSOITE + INDEKSI, 0);
        Muisti_tiedostojärjestelmä.muuttaa_kokoa_luettelo[tiedoston_nimi] = kesto_ARVO;
        return 0;
    }
    static int lukea_Tiedosto_tila(int 서술자, int OSOITE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!suoritus_Valvoja.leikata(OSOITE, 48)) return -14;
        for (int INDEKSI = 0; INDEKSI < 12; INDEKSI++) suoritus_Valvoja.kirjoitus_numero(OSOITE + INDEKSI * 4, 0);
        int tiedoston_nimi = tavoite[기술], Koko = 종류[기술] == 2 ? Muisti_tiedostojärjestelmä.muuttaa_kokoa_luettelo[tiedoston_nimi] : 0;
        int 허가 = 종류[기술] == 2 ? Muisti_tiedostojärjestelmä.허가들[tiedoston_nimi] : 438;
        suoritus_Valvoja.kirjoitus_numero(OSOITE, 1);
        suoritus_Valvoja.kirjoitus_numero(OSOITE + 4, 종류[기술] == 2 ? tiedoston_nimi + 1 : 100 + 기술);
        suoritus_Valvoja.kirjoitus_numero(OSOITE + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        suoritus_Valvoja.kirjoitus_numero(OSOITE + 12, 종류[기술] == 2 && Muisti_tiedostojärjestelmä.이름들[tiedoston_nimi * 64] == 0 ? 0 : 1);
        suoritus_Valvoja.kirjoitus_numero(OSOITE + 28, Koko); suoritus_Valvoja.kirjoitus_numero(OSOITE + 32, 512);
        suoritus_Valvoja.kirjoitus_numero(OSOITE + 36, (Koko + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int komento, int ARVO) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (komento == 0 || komento == 1030) return 서술자복제(서술자, ARVO, false, komento == 1030 ? 1 : 0);
        if (komento == 1) return 서술자설정[서술자];
        if (komento == 2) { if ((ARVO & ~1) != 0) return -22; 서술자설정[서술자] = ARVO; return 0; }
        if (komento == 3) return avata_Asetukset[기술];
        if (komento == 4) {
            if ((ARVO & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            avata_Asetukset[기술] = (avata_Asetukset[기술] & 3) | (ARVO & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int Luo_päätepiste(int 주소체계, int 통신종류, int työ_numero) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (työ_numero != 0 && työ_numero != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = 빈기술();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Yhdistä(서술자, 기술, 3, 0, luku_ja_kirjoitus_merkitä);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int OSOITE_32(int OSOITE) {
        return laite_ARVO.lukea_Muisti(OSOITE) << 24 | laite_ARVO.lukea_Muisti(OSOITE + 1) << 16
            | laite_ARVO.lukea_Muisti(OSOITE + 2) << 8 | laite_ARVO.lukea_Muisti(OSOITE + 3);
    }
    static int sekki_OSOITE(int OSOITE, int kesto_ARVO) {
        if (kesto_ARVO < 16) return -22;
        if (!suoritus_Valvoja.leikata(OSOITE, 16)) return -14;
        return suoritus_Valvoja.짧은수(OSOITE) == 2 ? 0 : -97;
    }
    static int BIND_OSOITE(int 서술자, int OSOITE, int kesto_ARVO) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int TULOS = sekki_OSOITE(OSOITE, kesto_ARVO);
        if (TULOS < 0) return TULOS;
        if (verkko_kahva[기술] != 0) return -22;
        int verkkotunnus = OSOITE_32(OSOITE + 4);
        if (verkkotunnus != 0 && verkkotunnus != verkko_Pino.내주소) return -99;
        int portin_numero = laite_ARVO.lukea_Muisti(OSOITE + 2) << 8 | laite_ARVO.lukea_Muisti(OSOITE + 3);
        TULOS = verkko_Pino.Avaa(portin_numero);
        if (TULOS < 0) return TULOS;
        verkko_kahva[기술] = TULOS; tavoite[기술] = verkkotunnus;
        return 0;
    }
    static int Automaattinen_BIND(int 기술) {
        if (verkko_kahva[기술] != 0) return 0;
        int TULOS = verkko_Pino.Avaa(0);
        if (TULOS < 0) return TULOS;
        verkko_kahva[기술] = TULOS;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 pyyntö 구조체로 전달한다.
    static int lähettää_datagrammi_data(int 서술자, int data_OSOITE, int kesto_ARVO, int Asetukset, int pyydetty_OSOITE) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Asetukset != 0) return -95;
        if (kesto_ARVO < 0 || kesto_ARVO > 1024) return -90;
        if (kesto_ARVO != 0 && !suoritus_Valvoja.leikata(data_OSOITE, kesto_ARVO)) return -14;
        if (!suoritus_Valvoja.leikata(pyydetty_OSOITE, 8)) return -14;
        int OSOITE = suoritus_Valvoja.numero(pyydetty_OSOITE);
        int TULOS = sekki_OSOITE(OSOITE, suoritus_Valvoja.numero(pyydetty_OSOITE + 4));
        if (TULOS < 0) return TULOS;
        int portin_numero = laite_ARVO.lukea_Muisti(OSOITE + 2) << 8 | laite_ARVO.lukea_Muisti(OSOITE + 3);
        if (portin_numero == 0) return -22;
        TULOS = Automaattinen_BIND(기술);
        if (TULOS < 0) return TULOS;
        for (int INDEKSI = 0; INDEKSI < kesto_ARVO; INDEKSI++) Siirrä_data[INDEKSI] = laite_ARVO.lukea_Muisti(data_OSOITE + INDEKSI);
        return verkko_Pino.lähettää(verkko_kahva[기술], OSOITE_32(OSOITE + 4), portin_numero, Siirrä_data, kesto_ARVO);
    }
    static void kirjoitus_OSOITE(int OSOITE, int kesto_ARVO, int verkkotunnus, int portin_numero) {
        for (int INDEKSI = 0; INDEKSI < kesto_ARVO && INDEKSI < 16; INDEKSI++) {
            int ARVO = 0;
            if (INDEKSI == 0) ARVO = 2;
            if (INDEKSI == 2) ARVO = portin_numero >>> 8;
            if (INDEKSI == 3) ARVO = portin_numero;
            if (INDEKSI >= 4 && INDEKSI < 8) ARVO = verkkotunnus >>> (56 - INDEKSI * 8);
            laite_ARVO.kirjoitus_Muisti(OSOITE + INDEKSI, ARVO & 255);
        }
    }
    static int saada_datagrammi_data(int 서술자, int data_OSOITE, int kesto_ARVO, int Asetukset, int pyydetty_OSOITE) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Asetukset & ~64) != 0) return -95;
        if (kesto_ARVO < 0) return -22;
        if (kesto_ARVO != 0 && !suoritus_Valvoja.leikata(data_OSOITE, kesto_ARVO)) return -14;
        int OSOITE = 0, OSOITE_kesto_OSOITE = 0, OSOITE_kesto = 0;
        if (pyydetty_OSOITE != 0) {
            if (!suoritus_Valvoja.leikata(pyydetty_OSOITE, 8)) return -14;
            OSOITE = suoritus_Valvoja.numero(pyydetty_OSOITE); OSOITE_kesto_OSOITE = suoritus_Valvoja.numero(pyydetty_OSOITE + 4);
            if (OSOITE != 0) {
                if (!suoritus_Valvoja.leikata(OSOITE_kesto_OSOITE, 4)) return -14;
                OSOITE_kesto = suoritus_Valvoja.numero(OSOITE_kesto_OSOITE);
                if (OSOITE_kesto < 0) return -22;
                if (!suoritus_Valvoja.leikata(OSOITE, OSOITE_kesto < 16 ? OSOITE_kesto : 16)) return -14;
            }
        }
        int TULOS = Automaattinen_BIND(기술);
        if (TULOS < 0) return TULOS;
        int Suorita_2 = laite_ARVO.밀리초();
        while (true) {
            TULOS = verkko_Pino.saada(verkko_kahva[기술], Siirrä_data, 1024, 0);
            if (TULOS != -11) break;
            if ((Asetukset & 64) != 0 || (avata_Asetukset[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && laite_ARVO.밀리초() - Suorita_2 >= 수신대기밀리초[기술]) return -11;
            if (laite_ARVO.사용자남은밀리초() <= 10) return -11;
            laite_ARVO.잠시양보();
        }
        if (TULOS < 0) return TULOS;
        if (TULOS > kesto_ARVO) TULOS = kesto_ARVO;
        for (int INDEKSI = 0; INDEKSI < TULOS; INDEKSI++) laite_ARVO.kirjoitus_Muisti(data_OSOITE + INDEKSI, Siirrä_data[INDEKSI]);
        if (OSOITE != 0) {
            kirjoitus_OSOITE(OSOITE, OSOITE_kesto, verkko_Pino.vertaissolmu_OSOITE(verkko_kahva[기술]), verkko_Pino.vertaissolmu_portin_numero(verkko_kahva[기술]));
            suoritus_Valvoja.kirjoitus_numero(OSOITE_kesto_OSOITE, 16);
        }
        return TULOS;
    }
    static int lukea_vastake_OSOITE(int 서술자, int OSOITE, int kesto_OSOITE) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!suoritus_Valvoja.leikata(kesto_OSOITE, 4)) return -14;
        int kesto_ARVO = suoritus_Valvoja.numero(kesto_OSOITE);
        if (kesto_ARVO < 0) return -22;
        if (!suoritus_Valvoja.leikata(OSOITE, kesto_ARVO < 16 ? kesto_ARVO : 16)) return -14;
        int paikka_merkintä = verkko_Pino.INDEKSI(verkko_kahva[기술]);
        kirjoitus_OSOITE(OSOITE, kesto_ARVO, tavoite[기술], paikka_merkintä < 0 ? 0 : verkko_Pino.접속번호들[paikka_merkintä]);
        suoritus_Valvoja.kirjoitus_numero(kesto_OSOITE, 16);
        return 0;
    }
    static int ryhmä_saada_AIKAKATKAISU(int 서술자, int 밀리초) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (밀리초 < 0 || 밀리초 > 2000) return -22;
        수신대기밀리초[기술] = 밀리초;
        return 0;
    }
}
