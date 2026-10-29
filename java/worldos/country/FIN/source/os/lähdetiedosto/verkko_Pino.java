// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** staattinen_ARVO IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class verkko_Pino {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int verkko_peite = 0xffffff00; /* ip.conf:NETMASK */
    static final int yhdyskäytävä_ARVO = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] syöte_kuva = new int[1536], tulos_kuva = new int[1536];
    static int[] 접속번호들 = new int[4], SAATU_HINTA_kesto = new int[4], SAATU_HINTA_OSOITE = new int[4], SAATU_HINTA_portin_numero = new int[4];
    static int[] SAATU_HINTA_data = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, tunniste_ARVO = 0, 폐기수 = 0;

    static int kokonaisluku_16(int[] kuva_INDEKSI, int paikka) { return (kuva_INDEKSI[paikka] << 8) | kuva_INDEKSI[paikka + 1]; }
    static int kokonaisluku_32(int[] kuva_INDEKSI, int paikka) { return (kokonaisluku_16(kuva_INDEKSI, paikka) << 16) | kokonaisluku_16(kuva_INDEKSI, paikka + 2); }
    static void 넣기16(int[] kuva_INDEKSI, int paikka, int ARVO) { kuva_INDEKSI[paikka] = (ARVO >>> 8) & 255; kuva_INDEKSI[paikka + 1] = ARVO & 255; }
    static void 넣기32(int[] kuva_INDEKSI, int paikka, int ARVO) { 넣기16(kuva_INDEKSI, paikka, ARVO >>> 16); 넣기16(kuva_INDEKSI, paikka + 2, ARVO); }
    static int SUM_ARVO(int[] kuva_INDEKSI, int Suorita_2, int kesto_ARVO, int ARVO) {
        for (int INDEKSI = 0; INDEKSI < kesto_ARVO; INDEKSI += 2)
            ARVO += (kuva_INDEKSI[Suorita_2 + INDEKSI] << 8) | (INDEKSI + 1 < kesto_ARVO ? kuva_INDEKSI[Suorita_2 + INDEKSI + 1] : 0);
        while ((ARVO >>> 16) != 0) ARVO = (ARVO & 65535) + (ARVO >>> 16);
        return ARVO;
    }
    static int 가상머리합(int 출발, int 도착, int kesto_ARVO) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + kesto_ARVO;
    }

    static void SIIVOA_prosessi() {
        for (int INDEKSI = 0; INDEKSI < 4; INDEKSI++) {
            접속번호들[INDEKSI] = 0; SAATU_HINTA_kesto[INDEKSI] = -1; SAATU_HINTA_OSOITE[INDEKSI] = 0; SAATU_HINTA_portin_numero[INDEKSI] = 0;
        }
        for (int INDEKSI = 0; INDEKSI < 64; INDEKSI++) if (verkko_ohjain.saada(syöte_kuva) == 0) break;
    }
    static int INDEKSI(int kahva_ARVO) { return kahva_ARVO >= 3 && kahva_ARVO < 7 && 접속번호들[kahva_ARVO - 3] != 0 ? kahva_ARVO - 3 : -1; }
    static int Avaa(int portin_numero) {
        if (verkko_ohjain.입출력기준주소 == 0) return -19;
        if (portin_numero < 0 || portin_numero > 65535) return -22;
        if (portin_numero != 0) for (int INDEKSI = 0; INDEKSI < 4; INDEKSI++) if (접속번호들[INDEKSI] == portin_numero) return -98;
        for (int INDEKSI = 0; INDEKSI < 4; INDEKSI++) if (접속번호들[INDEKSI] == 0) {
            if (portin_numero == 0) {
                portin_numero = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int etukamera_ARVO = 0; etukamera_ARVO < 4; etukamera_ARVO++) if (접속번호들[etukamera_ARVO] == portin_numero) 겹침 = true;
                    if (겹침) portin_numero++;
                }
            }
            접속번호들[INDEKSI] = portin_numero; SAATU_HINTA_kesto[INDEKSI] = -1;
            return INDEKSI + 3;
        }
        return -24;
    }
    static int Sulje(int kahva_ARVO) {
        int paikka_merkintä = INDEKSI(kahva_ARVO);
        if (paikka_merkintä < 0) return -9;
        접속번호들[paikka_merkintä] = 0; SAATU_HINTA_kesto[paikka_merkintä] = -1;
        return 0;
    }
    static int vertaissolmu_OSOITE(int kahva_ARVO) { int paikka_merkintä = INDEKSI(kahva_ARVO); return paikka_merkintä < 0 ? -9 : SAATU_HINTA_OSOITE[paikka_merkintä]; }
    static int vertaissolmu_portin_numero(int kahva_ARVO) { int paikka_merkintä = INDEKSI(kahva_ARVO); return paikka_merkintä < 0 ? -9 : SAATU_HINTA_portin_numero[paikka_merkintä]; }

    static void 바깥머리(int 종류, boolean lähetä_ARVO) {
        for (int INDEKSI = 0; INDEKSI < 6; INDEKSI++) {
            tulos_kuva[INDEKSI] = lähetä_ARVO ? 255 : 찾은장치[INDEKSI];
            tulos_kuva[6 + INDEKSI] = verkko_ohjain.laite_OSOITE[INDEKSI];
        }
        넣기16(tulos_kuva, 12, 종류);
    }
    static void pyyntö_OSOITE(int kohde_ARVO) {
        바깥머리(0x0806, true);
        넣기16(tulos_kuva, 14, 1); 넣기16(tulos_kuva, 16, 0x0800);
        tulos_kuva[18] = 6; tulos_kuva[19] = 4; 넣기16(tulos_kuva, 20, 1);
        for (int INDEKSI = 0; INDEKSI < 6; INDEKSI++) {
            tulos_kuva[22 + INDEKSI] = verkko_ohjain.laite_OSOITE[INDEKSI]; tulos_kuva[32 + INDEKSI] = 0;
        }
        넣기32(tulos_kuva, 28, 내주소); 넣기32(tulos_kuva, 38, kohde_ARVO);
        verkko_ohjain.lähettää(tulos_kuva, 42);
    }
    static void prosessi_OSOITE(int kesto_ARVO) {
        if (kesto_ARVO < 42 || kokonaisluku_16(syöte_kuva, 14) != 1 || kokonaisluku_16(syöte_kuva, 16) != 0x0800
            || syöte_kuva[18] != 6 || syöte_kuva[19] != 4 || kokonaisluku_32(syöte_kuva, 38) != 내주소) { 폐기수++; return; }
        int 종류 = kokonaisluku_16(syöte_kuva, 20), vertaissolmu_ARVO = kokonaisluku_32(syöte_kuva, 28);
        if (종류 == 2 && vertaissolmu_ARVO == 찾을주소) {
            for (int INDEKSI = 0; INDEKSI < 6; INDEKSI++) {
                if (syöte_kuva[6 + INDEKSI] != syöte_kuva[22 + INDEKSI] || syöte_kuva[32 + INDEKSI] != verkko_ohjain.laite_OSOITE[INDEKSI]) return;
            }
            for (int INDEKSI = 0; INDEKSI < 6; INDEKSI++) 찾은장치[INDEKSI] = syöte_kuva[22 + INDEKSI];
            찾은주소 = vertaissolmu_ARVO;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(tulos_kuva, 14, 1); 넣기16(tulos_kuva, 16, 0x0800);
            tulos_kuva[18] = 6; tulos_kuva[19] = 4; 넣기16(tulos_kuva, 20, 2);
            for (int INDEKSI = 0; INDEKSI < 6; INDEKSI++) {
                tulos_kuva[INDEKSI] = syöte_kuva[22 + INDEKSI]; tulos_kuva[32 + INDEKSI] = syöte_kuva[22 + INDEKSI];
                tulos_kuva[22 + INDEKSI] = verkko_ohjain.laite_OSOITE[INDEKSI];
            }
            넣기32(tulos_kuva, 28, 내주소); 넣기32(tulos_kuva, 38, vertaissolmu_ARVO);
            verkko_ohjain.lähettää(tulos_kuva, 42);
        }
    }

    static void prosessi_kuva(int kesto_ARVO) {
        if (kesto_ARVO < 14 || kesto_ARVO > syöte_kuva.length) { 폐기수++; return; }
        boolean 자기 = true, lähetä_ARVO = true;
        for (int INDEKSI = 0; INDEKSI < 6; INDEKSI++) {
            if (syöte_kuva[INDEKSI] != verkko_ohjain.laite_OSOITE[INDEKSI]) 자기 = false;
            if (syöte_kuva[INDEKSI] != 255) lähetä_ARVO = false;
        }
        if (!자기 && !lähetä_ARVO) return;
        if (kokonaisluku_16(syöte_kuva, 12) == 0x0806) { prosessi_OSOITE(kesto_ARVO); return; }
        if (kokonaisluku_16(syöte_kuva, 12) != 0x0800) return;
        if (kesto_ARVO < 34 || (syöte_kuva[14] >>> 4) != 4) { 폐기수++; return; }
        int otsikko_kesto = (syöte_kuva[14] & 15) * 4, summa_kesto = kokonaisluku_16(syöte_kuva, 16);
        if (otsikko_kesto < 20 || otsikko_kesto > 60 || summa_kesto < otsikko_kesto + 8 || summa_kesto > kesto_ARVO - 14
            || (kokonaisluku_16(syöte_kuva, 20) & 0x3fff) != 0 || syöte_kuva[23] != 17
            || kokonaisluku_32(syöte_kuva, 30) != 내주소 || SUM_ARVO(syöte_kuva, 14, otsikko_kesto, 0) != 65535) { 폐기수++; return; }
        int Suorita_2 = 14 + otsikko_kesto, data_kesto = kokonaisluku_16(syöte_kuva, Suorita_2 + 4);
        if (data_kesto < 8 || data_kesto != summa_kesto - otsikko_kesto || data_kesto > 1032) { 폐기수++; return; }
        int 출발 = kokonaisluku_32(syöte_kuva, 26);
        if (kokonaisluku_16(syöte_kuva, Suorita_2 + 6) != 0 && SUM_ARVO(syöte_kuva, Suorita_2, data_kesto, 가상머리합(출발, 내주소, data_kesto)) != 65535) {
            폐기수++; return;
        }
        int kohde_ARVO = kokonaisluku_16(syöte_kuva, Suorita_2 + 2);
        for (int paikka_merkintä = 0; paikka_merkintä < 4; paikka_merkintä++) if (접속번호들[paikka_merkintä] != 0 && 접속번호들[paikka_merkintä] == kohde_ARVO) {
            if (SAATU_HINTA_kesto[paikka_merkintä] >= 0) { 폐기수++; return; }
            SAATU_HINTA_kesto[paikka_merkintä] = data_kesto - 8; SAATU_HINTA_OSOITE[paikka_merkintä] = 출발; SAATU_HINTA_portin_numero[paikka_merkintä] = kokonaisluku_16(syöte_kuva, Suorita_2);
            for (int INDEKSI = 0; INDEKSI < data_kesto - 8; INDEKSI++) SAATU_HINTA_data[paikka_merkintä * 1024 + INDEKSI] = syöte_kuva[Suorita_2 + 8 + INDEKSI];
            return;
        }
    }

    static void tarkistaa() {
        for (int INDEKSI = 0; INDEKSI < 16; INDEKSI++) {
            int kesto_ARVO = verkko_ohjain.saada(syöte_kuva);
            if (kesto_ARVO == 0) return;
            prosessi_kuva(kesto_ARVO);
        }
    }
    static int ETSI_OSOITE(int OSOITE) {
        if (OSOITE == 0 || OSOITE == -1 || (OSOITE >>> 28) >= 14 || (OSOITE >>> 24) == 127 || OSOITE == 내주소) return -101;
        int Seuraava_kohde = (OSOITE & verkko_peite) == (내주소 & verkko_peite) ? OSOITE : yhdyskäytävä_ARVO;
        if (Seuraava_kohde == 찾은주소) return 0;
        찾을주소 = Seuraava_kohde;
        int Suorita_2 = laite_ARVO.밀리초(), Seuraava_pyyntö = Suorita_2;
        while (laite_ARVO.밀리초() - Suorita_2 < 1000) {
            if (laite_ARVO.밀리초() - Seuraava_pyyntö >= 0) { pyyntö_OSOITE(Seuraava_kohde); Seuraava_pyyntö += 300; }
            tarkistaa();
            if (찾은주소 == Seuraava_kohde) return 0;
            laite_ARVO.잠시양보();
        }
        return -110;
    }
    static int lähettää(int kahva_ARVO, int OSOITE, int portin_numero, int[] data, int kesto_ARVO) {
        int paikka_merkintä = INDEKSI(kahva_ARVO);
        if (paikka_merkintä < 0) return -9;
        if (verkko_ohjain.입출력기준주소 == 0) return -19;
        if (portin_numero < 1 || portin_numero > 65535 || kesto_ARVO < 0 || kesto_ARVO > 1024) return -22;
        int TULOS = ETSI_OSOITE(OSOITE);
        if (TULOS < 0) return TULOS;
        바깥머리(0x0800, false);
        tulos_kuva[14] = 0x45; tulos_kuva[15] = 0; 넣기16(tulos_kuva, 16, 28 + kesto_ARVO);
        넣기16(tulos_kuva, 18, tunniste_ARVO++); 넣기16(tulos_kuva, 20, 0x4000);
        tulos_kuva[22] = 64; tulos_kuva[23] = 17; 넣기16(tulos_kuva, 24, 0);
        넣기32(tulos_kuva, 26, 내주소); 넣기32(tulos_kuva, 30, OSOITE);
        넣기16(tulos_kuva, 24, ~SUM_ARVO(tulos_kuva, 14, 20, 0));
        넣기16(tulos_kuva, 34, 접속번호들[paikka_merkintä]); 넣기16(tulos_kuva, 36, portin_numero);
        넣기16(tulos_kuva, 38, kesto_ARVO + 8); 넣기16(tulos_kuva, 40, 0);
        for (int INDEKSI = 0; INDEKSI < kesto_ARVO; INDEKSI++) tulos_kuva[42 + INDEKSI] = data[INDEKSI] & 255;
        int tarkistussumma = (~SUM_ARVO(tulos_kuva, 34, kesto_ARVO + 8, 가상머리합(내주소, OSOITE, kesto_ARVO + 8))) & 65535;
        넣기16(tulos_kuva, 40, tarkistussumma == 0 ? 65535 : tarkistussumma);
        TULOS = verkko_ohjain.lähettää(tulos_kuva, kesto_ARVO + 42);
        return TULOS < 0 ? TULOS : kesto_ARVO;
    }
    static int saada(int kahva_ARVO, int[] data, int kapasiteetti_ARVO, int 제한) {
        int paikka_merkintä = INDEKSI(kahva_ARVO);
        if (paikka_merkintä < 0) return -9;
        int Suorita_2 = laite_ARVO.밀리초();
        while (true) {
            tarkistaa();
            int kesto_ARVO = SAATU_HINTA_kesto[paikka_merkintä];
            if (kesto_ARVO >= 0) {
                SAATU_HINTA_kesto[paikka_merkintä] = -1;
                if (kesto_ARVO > kapasiteetti_ARVO) return -90;
                for (int INDEKSI = 0; INDEKSI < kesto_ARVO; INDEKSI++) data[INDEKSI] = SAATU_HINTA_data[paikka_merkintä * 1024 + INDEKSI];
                return kesto_ARVO;
            }
            if (제한 == 0) return -11;
            if (laite_ARVO.밀리초() - Suorita_2 >= 제한) return -110;
            laite_ARVO.잠시양보();
        }
    }
    static void Tila_ARVO() {
        SMS_Pääte.Kirjoitus(verkko_ohjain.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Pääte.Kirjoitus("TX: "); SMS_Pääte.kirjoitus_numero(verkko_ohjain.lähettää_LASKE);
        SMS_Pääte.Kirjoitus(" RX: "); SMS_Pääte.kirjoitus_numero(verkko_ohjain.saada_LASKE);
        SMS_Pääte.Kirjoitus(" DROP: "); SMS_Pääte.kirjoitus_numero(폐기수);
        SMS_Pääte.Kirjoitus("\n");
    }
}
