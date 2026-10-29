// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 정적 IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class sieť_Vrstvy {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int sieť_maska = 0xffffff00; /* ip.conf:NETMASK */
    static final int brána_VALUE = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] vstup_rám = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], RECEIVED_dĺžka = new int[4], RECEIVED_adresa = new int[4], RECEIVED_číslo_portu = new int[4];
    static int[] RECEIVED_údaje = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, identifikátor_VALUE = 0, 폐기수 = 0;

    static int celé_číslo_16(int[] rám_INDEX, int Pozícia) { return (rám_INDEX[Pozícia] << 8) | rám_INDEX[Pozícia + 1]; }
    static int celé_číslo_32(int[] rám_INDEX, int Pozícia) { return (celé_číslo_16(rám_INDEX, Pozícia) << 16) | celé_číslo_16(rám_INDEX, Pozícia + 2); }
    static void 넣기16(int[] rám_INDEX, int Pozícia, int VALUE) { rám_INDEX[Pozícia] = (VALUE >>> 8) & 255; rám_INDEX[Pozícia + 1] = VALUE & 255; }
    static void 넣기32(int[] rám_INDEX, int Pozícia, int VALUE) { 넣기16(rám_INDEX, Pozícia, VALUE >>> 16); 넣기16(rám_INDEX, Pozícia + 2, VALUE); }
    static int SUM_VALUE(int[] rám_INDEX, int Spustiť_2, int dĺžka_VALUE, int VALUE) {
        for (int INDEX = 0; INDEX < dĺžka_VALUE; INDEX += 2)
            VALUE += (rám_INDEX[Spustiť_2 + INDEX] << 8) | (INDEX + 1 < dĺžka_VALUE ? rám_INDEX[Spustiť_2 + INDEX + 1] : 0);
        while ((VALUE >>> 16) != 0) VALUE = (VALUE & 65535) + (VALUE >>> 16);
        return VALUE;
    }
    static int 가상머리합(int 출발, int 도착, int dĺžka_VALUE) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + dĺžka_VALUE;
    }

    static void CLEAN_Proces() {
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            접속번호들[INDEX] = 0; RECEIVED_dĺžka[INDEX] = -1; RECEIVED_adresa[INDEX] = 0; RECEIVED_číslo_portu[INDEX] = 0;
        }
        for (int INDEX = 0; INDEX < 64; INDEX++) if (sieť_ovládač.dostať(vstup_rám) == 0) break;
    }
    static int INDEX(int rukoväť_VALUE) { return rukoväť_VALUE >= 3 && rukoväť_VALUE < 7 && 접속번호들[rukoväť_VALUE - 3] != 0 ? rukoväť_VALUE - 3 : -1; }
    static int Otvoriť(int číslo_portu) {
        if (sieť_ovládač.입출력기준주소 == 0) return -19;
        if (číslo_portu < 0 || číslo_portu > 65535) return -22;
        if (číslo_portu != 0) for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == číslo_portu) return -98;
        for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == 0) {
            if (číslo_portu == 0) {
                číslo_portu = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int predný_VALUE = 0; predný_VALUE < 4; predný_VALUE++) if (접속번호들[predný_VALUE] == číslo_portu) 겹침 = true;
                    if (겹침) číslo_portu++;
                }
            }
            접속번호들[INDEX] = číslo_portu; RECEIVED_dĺžka[INDEX] = -1;
            return INDEX + 3;
        }
        return -24;
    }
    static int Zatvoriť(int rukoväť_VALUE) {
        int 칸 = INDEX(rukoväť_VALUE);
        if (칸 < 0) return -9;
        접속번호들[칸] = 0; RECEIVED_dĺžka[칸] = -1;
        return 0;
    }
    static int partnerský_uzol_adresa(int rukoväť_VALUE) { int 칸 = INDEX(rukoväť_VALUE); return 칸 < 0 ? -9 : RECEIVED_adresa[칸]; }
    static int partnerský_uzol_číslo_portu(int rukoväť_VALUE) { int 칸 = INDEX(rukoväť_VALUE); return 칸 < 0 ? -9 : RECEIVED_číslo_portu[칸]; }

    static void 바깥머리(int 종류, boolean vysielať_VALUE) {
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[INDEX] = vysielať_VALUE ? 255 : 찾은장치[INDEX];
            출력틀[6 + INDEX] = sieť_ovládač.telefón_adresa[INDEX];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void požiadavka_adresa(int cieľ_VALUE) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[22 + INDEX] = sieť_ovládač.telefón_adresa[INDEX]; 출력틀[32 + INDEX] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, cieľ_VALUE);
        sieť_ovládač.odoslať(출력틀, 42);
    }
    static void Proces_adresa(int dĺžka_VALUE) {
        if (dĺžka_VALUE < 42 || celé_číslo_16(vstup_rám, 14) != 1 || celé_číslo_16(vstup_rám, 16) != 0x0800
            || vstup_rám[18] != 6 || vstup_rám[19] != 4 || celé_číslo_32(vstup_rám, 38) != 내주소) { 폐기수++; return; }
        int 종류 = celé_číslo_16(vstup_rám, 20), partnerský_uzol_VALUE = celé_číslo_32(vstup_rám, 28);
        if (종류 == 2 && partnerský_uzol_VALUE == 찾을주소) {
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                if (vstup_rám[6 + INDEX] != vstup_rám[22 + INDEX] || vstup_rám[32 + INDEX] != sieť_ovládač.telefón_adresa[INDEX]) return;
            }
            for (int INDEX = 0; INDEX < 6; INDEX++) 찾은장치[INDEX] = vstup_rám[22 + INDEX];
            찾은주소 = partnerský_uzol_VALUE;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                출력틀[INDEX] = vstup_rám[22 + INDEX]; 출력틀[32 + INDEX] = vstup_rám[22 + INDEX];
                출력틀[22 + INDEX] = sieť_ovládač.telefón_adresa[INDEX];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, partnerský_uzol_VALUE);
            sieť_ovládač.odoslať(출력틀, 42);
        }
    }

    static void Proces_rám(int dĺžka_VALUE) {
        if (dĺžka_VALUE < 14 || dĺžka_VALUE > vstup_rám.length) { 폐기수++; return; }
        boolean 자기 = true, vysielať_VALUE = true;
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            if (vstup_rám[INDEX] != sieť_ovládač.telefón_adresa[INDEX]) 자기 = false;
            if (vstup_rám[INDEX] != 255) vysielať_VALUE = false;
        }
        if (!자기 && !vysielať_VALUE) return;
        if (celé_číslo_16(vstup_rám, 12) == 0x0806) { Proces_adresa(dĺžka_VALUE); return; }
        if (celé_číslo_16(vstup_rám, 12) != 0x0800) return;
        if (dĺžka_VALUE < 34 || (vstup_rám[14] >>> 4) != 4) { 폐기수++; return; }
        int Nadpis_dĺžka = (vstup_rám[14] & 15) * 4, celkovo_dĺžka = celé_číslo_16(vstup_rám, 16);
        if (Nadpis_dĺžka < 20 || Nadpis_dĺžka > 60 || celkovo_dĺžka < Nadpis_dĺžka + 8 || celkovo_dĺžka > dĺžka_VALUE - 14
            || (celé_číslo_16(vstup_rám, 20) & 0x3fff) != 0 || vstup_rám[23] != 17
            || celé_číslo_32(vstup_rám, 30) != 내주소 || SUM_VALUE(vstup_rám, 14, Nadpis_dĺžka, 0) != 65535) { 폐기수++; return; }
        int Spustiť_2 = 14 + Nadpis_dĺžka, údaje_dĺžka = celé_číslo_16(vstup_rám, Spustiť_2 + 4);
        if (údaje_dĺžka < 8 || údaje_dĺžka != celkovo_dĺžka - Nadpis_dĺžka || údaje_dĺžka > 1032) { 폐기수++; return; }
        int 출발 = celé_číslo_32(vstup_rám, 26);
        if (celé_číslo_16(vstup_rám, Spustiť_2 + 6) != 0 && SUM_VALUE(vstup_rám, Spustiť_2, údaje_dĺžka, 가상머리합(출발, 내주소, údaje_dĺžka)) != 65535) {
            폐기수++; return;
        }
        int cieľ_VALUE = celé_číslo_16(vstup_rám, Spustiť_2 + 2);
        for (int 칸 = 0; 칸 < 4; 칸++) if (접속번호들[칸] != 0 && 접속번호들[칸] == cieľ_VALUE) {
            if (RECEIVED_dĺžka[칸] >= 0) { 폐기수++; return; }
            RECEIVED_dĺžka[칸] = údaje_dĺžka - 8; RECEIVED_adresa[칸] = 출발; RECEIVED_číslo_portu[칸] = celé_číslo_16(vstup_rám, Spustiť_2);
            for (int INDEX = 0; INDEX < údaje_dĺžka - 8; INDEX++) RECEIVED_údaje[칸 * 1024 + INDEX] = vstup_rám[Spustiť_2 + 8 + INDEX];
            return;
        }
    }

    static void overiť() {
        for (int INDEX = 0; INDEX < 16; INDEX++) {
            int dĺžka_VALUE = sieť_ovládač.dostať(vstup_rám);
            if (dĺžka_VALUE == 0) return;
            Proces_rám(dĺžka_VALUE);
        }
    }
    static int FIND_adresa(int adresa) {
        if (adresa == 0 || adresa == -1 || (adresa >>> 28) >= 14 || (adresa >>> 24) == 127 || adresa == 내주소) return -101;
        int Ďalej_položka = (adresa & sieť_maska) == (내주소 & sieť_maska) ? adresa : brána_VALUE;
        if (Ďalej_položka == 찾은주소) return 0;
        찾을주소 = Ďalej_položka;
        int Spustiť_2 = telefón_VALUE.밀리초(), Ďalej_požiadavka = Spustiť_2;
        while (telefón_VALUE.밀리초() - Spustiť_2 < 1000) {
            if (telefón_VALUE.밀리초() - Ďalej_požiadavka >= 0) { požiadavka_adresa(Ďalej_položka); Ďalej_požiadavka += 300; }
            overiť();
            if (찾은주소 == Ďalej_položka) return 0;
            telefón_VALUE.잠시양보();
        }
        return -110;
    }
    static int odoslať(int rukoväť_VALUE, int adresa, int číslo_portu, int[] údaje, int dĺžka_VALUE) {
        int 칸 = INDEX(rukoväť_VALUE);
        if (칸 < 0) return -9;
        if (sieť_ovládač.입출력기준주소 == 0) return -19;
        if (číslo_portu < 1 || číslo_portu > 65535 || dĺžka_VALUE < 0 || dĺžka_VALUE > 1024) return -22;
        int KR = FIND_adresa(adresa);
        if (KR < 0) return KR;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + dĺžka_VALUE);
        넣기16(출력틀, 18, identifikátor_VALUE++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, adresa);
        넣기16(출력틀, 24, ~SUM_VALUE(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[칸]); 넣기16(출력틀, 36, číslo_portu);
        넣기16(출력틀, 38, dĺžka_VALUE + 8); 넣기16(출력틀, 40, 0);
        for (int INDEX = 0; INDEX < dĺžka_VALUE; INDEX++) 출력틀[42 + INDEX] = údaje[INDEX] & 255;
        int kontrolný_súčet = (~SUM_VALUE(출력틀, 34, dĺžka_VALUE + 8, 가상머리합(내주소, adresa, dĺžka_VALUE + 8))) & 65535;
        넣기16(출력틀, 40, kontrolný_súčet == 0 ? 65535 : kontrolný_súčet);
        KR = sieť_ovládač.odoslať(출력틀, dĺžka_VALUE + 42);
        return KR < 0 ? KR : dĺžka_VALUE;
    }
    static int dostať(int rukoväť_VALUE, int[] údaje, int kapacita_VALUE, int 제한) {
        int 칸 = INDEX(rukoväť_VALUE);
        if (칸 < 0) return -9;
        int Spustiť_2 = telefón_VALUE.밀리초();
        while (true) {
            overiť();
            int dĺžka_VALUE = RECEIVED_dĺžka[칸];
            if (dĺžka_VALUE >= 0) {
                RECEIVED_dĺžka[칸] = -1;
                if (dĺžka_VALUE > kapacita_VALUE) return -90;
                for (int INDEX = 0; INDEX < dĺžka_VALUE; INDEX++) údaje[INDEX] = RECEIVED_údaje[칸 * 1024 + INDEX];
                return dĺžka_VALUE;
            }
            if (제한 == 0) return -11;
            if (telefón_VALUE.밀리초() - Spustiť_2 >= 제한) return -110;
            telefón_VALUE.잠시양보();
        }
    }
    static void Stav_VALUE() {
        SMS_Terminál.Zápis(sieť_ovládač.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Terminál.Zápis("TX: "); SMS_Terminál.수쓰기(sieť_ovládač.송신수);
        SMS_Terminál.Zápis(" RX: "); SMS_Terminál.수쓰기(sieť_ovládač.dostať_COUNT);
        SMS_Terminál.Zápis(" DROP: "); SMS_Terminál.수쓰기(폐기수);
        SMS_Terminál.Zápis("\n");
    }
}
