// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** statikus_ÉRTÉK IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class hálózat_Sor {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int hálózati_maszk = 0xffffff00; /* ip.conf:NETMASK */
    static final int átjáró_ÉRTÉK = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] bevitel_doboz = new int[1536], kimenet_doboz = new int[1536];
    static int[] 접속번호들 = new int[4], KAPOTT_hossz = new int[4], KAPOTT_CÍM = new int[4], KAPOTT_portszám = new int[4];
    static int[] KAPOTT_adat = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, azonosító_ÉRTÉK = 0, 폐기수 = 0;

    static int egész_szám_16(int[] doboz_INDEX, int Pozíció) { return (doboz_INDEX[Pozíció] << 8) | doboz_INDEX[Pozíció + 1]; }
    static int egész_szám_32(int[] doboz_INDEX, int Pozíció) { return (egész_szám_16(doboz_INDEX, Pozíció) << 16) | egész_szám_16(doboz_INDEX, Pozíció + 2); }
    static void 넣기16(int[] doboz_INDEX, int Pozíció, int ÉRTÉK) { doboz_INDEX[Pozíció] = (ÉRTÉK >>> 8) & 255; doboz_INDEX[Pozíció + 1] = ÉRTÉK & 255; }
    static void 넣기32(int[] doboz_INDEX, int Pozíció, int ÉRTÉK) { 넣기16(doboz_INDEX, Pozíció, ÉRTÉK >>> 16); 넣기16(doboz_INDEX, Pozíció + 2, ÉRTÉK); }
    static int SUM_ÉRTÉK(int[] doboz_INDEX, int Futtatás, int hossz_ÉRTÉK, int ÉRTÉK) {
        for (int INDEX = 0; INDEX < hossz_ÉRTÉK; INDEX += 2)
            ÉRTÉK += (doboz_INDEX[Futtatás + INDEX] << 8) | (INDEX + 1 < hossz_ÉRTÉK ? doboz_INDEX[Futtatás + INDEX + 1] : 0);
        while ((ÉRTÉK >>> 16) != 0) ÉRTÉK = (ÉRTÉK & 65535) + (ÉRTÉK >>> 16);
        return ÉRTÉK;
    }
    static int 가상머리합(int 출발, int 도착, int hossz_ÉRTÉK) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + hossz_ÉRTÉK;
    }

    static void TISZTÍT_folyamat() {
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            접속번호들[INDEX] = 0; KAPOTT_hossz[INDEX] = -1; KAPOTT_CÍM[INDEX] = 0; KAPOTT_portszám[INDEX] = 0;
        }
        for (int INDEX = 0; INDEX < 64; INDEX++) if (hálózat_eszközillesztő.fogad(bevitel_doboz) == 0) break;
    }
    static int INDEX(int leíró_ÉRTÉK) { return leíró_ÉRTÉK >= 3 && leíró_ÉRTÉK < 7 && 접속번호들[leíró_ÉRTÉK - 3] != 0 ? leíró_ÉRTÉK - 3 : -1; }
    static int Megnyitás(int portszám) {
        if (hálózat_eszközillesztő.입출력기준주소 == 0) return -19;
        if (portszám < 0 || portszám > 65535) return -22;
        if (portszám != 0) for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == portszám) return -98;
        for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == 0) {
            if (portszám == 0) {
                portszám = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int elülső_kamera_ÉRTÉK = 0; elülső_kamera_ÉRTÉK < 4; elülső_kamera_ÉRTÉK++) if (접속번호들[elülső_kamera_ÉRTÉK] == portszám) 겹침 = true;
                    if (겹침) portszám++;
                }
            }
            접속번호들[INDEX] = portszám; KAPOTT_hossz[INDEX] = -1;
            return INDEX + 3;
        }
        return -24;
    }
    static int Bezárás(int leíró_ÉRTÉK) {
        int tárolóhely_bejegyzés = INDEX(leíró_ÉRTÉK);
        if (tárolóhely_bejegyzés < 0) return -9;
        접속번호들[tárolóhely_bejegyzés] = 0; KAPOTT_hossz[tárolóhely_bejegyzés] = -1;
        return 0;
    }
    static int társ_CÍM(int leíró_ÉRTÉK) { int tárolóhely_bejegyzés = INDEX(leíró_ÉRTÉK); return tárolóhely_bejegyzés < 0 ? -9 : KAPOTT_CÍM[tárolóhely_bejegyzés]; }
    static int társ_portszám(int leíró_ÉRTÉK) { int tárolóhely_bejegyzés = INDEX(leíró_ÉRTÉK); return tárolóhely_bejegyzés < 0 ? -9 : KAPOTT_portszám[tárolóhely_bejegyzés]; }

    static void 바깥머리(int Altípus_ÉRTÉK, boolean adás_ÉRTÉK) {
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            kimenet_doboz[INDEX] = adás_ÉRTÉK ? 255 : 찾은장치[INDEX];
            kimenet_doboz[6 + INDEX] = hálózat_eszközillesztő.mobil_CÍM[INDEX];
        }
        넣기16(kimenet_doboz, 12, Altípus_ÉRTÉK);
    }
    static void kérés_CÍM(int cél_ÉRTÉK) {
        바깥머리(0x0806, true);
        넣기16(kimenet_doboz, 14, 1); 넣기16(kimenet_doboz, 16, 0x0800);
        kimenet_doboz[18] = 6; kimenet_doboz[19] = 4; 넣기16(kimenet_doboz, 20, 1);
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            kimenet_doboz[22 + INDEX] = hálózat_eszközillesztő.mobil_CÍM[INDEX]; kimenet_doboz[32 + INDEX] = 0;
        }
        넣기32(kimenet_doboz, 28, 내주소); 넣기32(kimenet_doboz, 38, cél_ÉRTÉK);
        hálózat_eszközillesztő.küld(kimenet_doboz, 42);
    }
    static void folyamat_CÍM(int hossz_ÉRTÉK) {
        if (hossz_ÉRTÉK < 42 || egész_szám_16(bevitel_doboz, 14) != 1 || egész_szám_16(bevitel_doboz, 16) != 0x0800
            || bevitel_doboz[18] != 6 || bevitel_doboz[19] != 4 || egész_szám_32(bevitel_doboz, 38) != 내주소) { 폐기수++; return; }
        int Altípus_ÉRTÉK = egész_szám_16(bevitel_doboz, 20), társ_ÉRTÉK = egész_szám_32(bevitel_doboz, 28);
        if (Altípus_ÉRTÉK == 2 && társ_ÉRTÉK == 찾을주소) {
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                if (bevitel_doboz[6 + INDEX] != bevitel_doboz[22 + INDEX] || bevitel_doboz[32 + INDEX] != hálózat_eszközillesztő.mobil_CÍM[INDEX]) return;
            }
            for (int INDEX = 0; INDEX < 6; INDEX++) 찾은장치[INDEX] = bevitel_doboz[22 + INDEX];
            찾은주소 = társ_ÉRTÉK;
        } else if (Altípus_ÉRTÉK == 1) {
            바깥머리(0x0806, false);
            넣기16(kimenet_doboz, 14, 1); 넣기16(kimenet_doboz, 16, 0x0800);
            kimenet_doboz[18] = 6; kimenet_doboz[19] = 4; 넣기16(kimenet_doboz, 20, 2);
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                kimenet_doboz[INDEX] = bevitel_doboz[22 + INDEX]; kimenet_doboz[32 + INDEX] = bevitel_doboz[22 + INDEX];
                kimenet_doboz[22 + INDEX] = hálózat_eszközillesztő.mobil_CÍM[INDEX];
            }
            넣기32(kimenet_doboz, 28, 내주소); 넣기32(kimenet_doboz, 38, társ_ÉRTÉK);
            hálózat_eszközillesztő.küld(kimenet_doboz, 42);
        }
    }

    static void folyamat_doboz(int hossz_ÉRTÉK) {
        if (hossz_ÉRTÉK < 14 || hossz_ÉRTÉK > bevitel_doboz.length) { 폐기수++; return; }
        boolean 자기 = true, adás_ÉRTÉK = true;
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            if (bevitel_doboz[INDEX] != hálózat_eszközillesztő.mobil_CÍM[INDEX]) 자기 = false;
            if (bevitel_doboz[INDEX] != 255) adás_ÉRTÉK = false;
        }
        if (!자기 && !adás_ÉRTÉK) return;
        if (egész_szám_16(bevitel_doboz, 12) == 0x0806) { folyamat_CÍM(hossz_ÉRTÉK); return; }
        if (egész_szám_16(bevitel_doboz, 12) != 0x0800) return;
        if (hossz_ÉRTÉK < 34 || (bevitel_doboz[14] >>> 4) != 4) { 폐기수++; return; }
        int fejléc_hossz = (bevitel_doboz[14] & 15) * 4, összesen_hossz = egész_szám_16(bevitel_doboz, 16);
        if (fejléc_hossz < 20 || fejléc_hossz > 60 || összesen_hossz < fejléc_hossz + 8 || összesen_hossz > hossz_ÉRTÉK - 14
            || (egész_szám_16(bevitel_doboz, 20) & 0x3fff) != 0 || bevitel_doboz[23] != 17
            || egész_szám_32(bevitel_doboz, 30) != 내주소 || SUM_ÉRTÉK(bevitel_doboz, 14, fejléc_hossz, 0) != 65535) { 폐기수++; return; }
        int Futtatás = 14 + fejléc_hossz, adat_hossz = egész_szám_16(bevitel_doboz, Futtatás + 4);
        if (adat_hossz < 8 || adat_hossz != összesen_hossz - fejléc_hossz || adat_hossz > 1032) { 폐기수++; return; }
        int 출발 = egész_szám_32(bevitel_doboz, 26);
        if (egész_szám_16(bevitel_doboz, Futtatás + 6) != 0 && SUM_ÉRTÉK(bevitel_doboz, Futtatás, adat_hossz, 가상머리합(출발, 내주소, adat_hossz)) != 65535) {
            폐기수++; return;
        }
        int cél_ÉRTÉK = egész_szám_16(bevitel_doboz, Futtatás + 2);
        for (int tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < 4; tárolóhely_bejegyzés++) if (접속번호들[tárolóhely_bejegyzés] != 0 && 접속번호들[tárolóhely_bejegyzés] == cél_ÉRTÉK) {
            if (KAPOTT_hossz[tárolóhely_bejegyzés] >= 0) { 폐기수++; return; }
            KAPOTT_hossz[tárolóhely_bejegyzés] = adat_hossz - 8; KAPOTT_CÍM[tárolóhely_bejegyzés] = 출발; KAPOTT_portszám[tárolóhely_bejegyzés] = egész_szám_16(bevitel_doboz, Futtatás);
            for (int INDEX = 0; INDEX < adat_hossz - 8; INDEX++) KAPOTT_adat[tárolóhely_bejegyzés * 1024 + INDEX] = bevitel_doboz[Futtatás + 8 + INDEX];
            return;
        }
    }

    static void igazol() {
        for (int INDEX = 0; INDEX < 16; INDEX++) {
            int hossz_ÉRTÉK = hálózat_eszközillesztő.fogad(bevitel_doboz);
            if (hossz_ÉRTÉK == 0) return;
            folyamat_doboz(hossz_ÉRTÉK);
        }
    }
    static int keres_CÍM(int CÍM) {
        if (CÍM == 0 || CÍM == -1 || (CÍM >>> 28) >= 14 || (CÍM >>> 24) == 127 || CÍM == 내주소) return -101;
        int Tovább_cikk = (CÍM & hálózati_maszk) == (내주소 & hálózati_maszk) ? CÍM : átjáró_ÉRTÉK;
        if (Tovább_cikk == 찾은주소) return 0;
        찾을주소 = Tovább_cikk;
        int Futtatás = mobil_ÉRTÉK.밀리초(), Tovább_kérés = Futtatás;
        while (mobil_ÉRTÉK.밀리초() - Futtatás < 1000) {
            if (mobil_ÉRTÉK.밀리초() - Tovább_kérés >= 0) { kérés_CÍM(Tovább_cikk); Tovább_kérés += 300; }
            igazol();
            if (찾은주소 == Tovább_cikk) return 0;
            mobil_ÉRTÉK.잠시양보();
        }
        return -110;
    }
    static int küld(int leíró_ÉRTÉK, int CÍM, int portszám, int[] adat, int hossz_ÉRTÉK) {
        int tárolóhely_bejegyzés = INDEX(leíró_ÉRTÉK);
        if (tárolóhely_bejegyzés < 0) return -9;
        if (hálózat_eszközillesztő.입출력기준주소 == 0) return -19;
        if (portszám < 1 || portszám > 65535 || hossz_ÉRTÉK < 0 || hossz_ÉRTÉK > 1024) return -22;
        int KR = keres_CÍM(CÍM);
        if (KR < 0) return KR;
        바깥머리(0x0800, false);
        kimenet_doboz[14] = 0x45; kimenet_doboz[15] = 0; 넣기16(kimenet_doboz, 16, 28 + hossz_ÉRTÉK);
        넣기16(kimenet_doboz, 18, azonosító_ÉRTÉK++); 넣기16(kimenet_doboz, 20, 0x4000);
        kimenet_doboz[22] = 64; kimenet_doboz[23] = 17; 넣기16(kimenet_doboz, 24, 0);
        넣기32(kimenet_doboz, 26, 내주소); 넣기32(kimenet_doboz, 30, CÍM);
        넣기16(kimenet_doboz, 24, ~SUM_ÉRTÉK(kimenet_doboz, 14, 20, 0));
        넣기16(kimenet_doboz, 34, 접속번호들[tárolóhely_bejegyzés]); 넣기16(kimenet_doboz, 36, portszám);
        넣기16(kimenet_doboz, 38, hossz_ÉRTÉK + 8); 넣기16(kimenet_doboz, 40, 0);
        for (int INDEX = 0; INDEX < hossz_ÉRTÉK; INDEX++) kimenet_doboz[42 + INDEX] = adat[INDEX] & 255;
        int ellenőrzőösszeg = (~SUM_ÉRTÉK(kimenet_doboz, 34, hossz_ÉRTÉK + 8, 가상머리합(내주소, CÍM, hossz_ÉRTÉK + 8))) & 65535;
        넣기16(kimenet_doboz, 40, ellenőrzőösszeg == 0 ? 65535 : ellenőrzőösszeg);
        KR = hálózat_eszközillesztő.küld(kimenet_doboz, hossz_ÉRTÉK + 42);
        return KR < 0 ? KR : hossz_ÉRTÉK;
    }
    static int fogad(int leíró_ÉRTÉK, int[] adat, int kapacitás_ÉRTÉK, int 제한) {
        int tárolóhely_bejegyzés = INDEX(leíró_ÉRTÉK);
        if (tárolóhely_bejegyzés < 0) return -9;
        int Futtatás = mobil_ÉRTÉK.밀리초();
        while (true) {
            igazol();
            int hossz_ÉRTÉK = KAPOTT_hossz[tárolóhely_bejegyzés];
            if (hossz_ÉRTÉK >= 0) {
                KAPOTT_hossz[tárolóhely_bejegyzés] = -1;
                if (hossz_ÉRTÉK > kapacitás_ÉRTÉK) return -90;
                for (int INDEX = 0; INDEX < hossz_ÉRTÉK; INDEX++) adat[INDEX] = KAPOTT_adat[tárolóhely_bejegyzés * 1024 + INDEX];
                return hossz_ÉRTÉK;
            }
            if (제한 == 0) return -11;
            if (mobil_ÉRTÉK.밀리초() - Futtatás >= 제한) return -110;
            mobil_ÉRTÉK.잠시양보();
        }
    }
    static void Állapot_ÉRTÉK() {
        SMS_Terminál.Írás(hálózat_eszközillesztő.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Terminál.Írás("TX: "); SMS_Terminál.ír_szám(hálózat_eszközillesztő.송신수);
        SMS_Terminál.Írás(" RX: "); SMS_Terminál.ír_szám(hálózat_eszközillesztő.fogad_DARAB);
        SMS_Terminál.Írás(" DROP: "); SMS_Terminál.ír_szám(폐기수);
        SMS_Terminál.Írás("\n");
    }
}
