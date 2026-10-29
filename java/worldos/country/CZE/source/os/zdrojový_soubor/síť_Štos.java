// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** statický_HODNOTA IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class síť_Štos {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int síť_maska = 0xffffff00; /* ip.conf:NETMASK */
    static final int brána_HODNOTA = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] vstup_rámec = new int[1536], výstup_rámec = new int[1536];
    static int[] 접속번호들 = new int[4], RECEIVED_délka = new int[4], RECEIVED_ODKAZ = new int[4], RECEIVED_číslo_portu = new int[4];
    static int[] RECEIVED_data = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, identifikátor_HODNOTA = 0, 폐기수 = 0;

    static int integer_16(int[] rámec_INDEX, int pozice) { return (rámec_INDEX[pozice] << 8) | rámec_INDEX[pozice + 1]; }
    static int integer_32(int[] rámec_INDEX, int pozice) { return (integer_16(rámec_INDEX, pozice) << 16) | integer_16(rámec_INDEX, pozice + 2); }
    static void 넣기16(int[] rámec_INDEX, int pozice, int HODNOTA) { rámec_INDEX[pozice] = (HODNOTA >>> 8) & 255; rámec_INDEX[pozice + 1] = HODNOTA & 255; }
    static void 넣기32(int[] rámec_INDEX, int pozice, int HODNOTA) { 넣기16(rámec_INDEX, pozice, HODNOTA >>> 16); 넣기16(rámec_INDEX, pozice + 2, HODNOTA); }
    static int SUMA_HODNOTA(int[] rámec_INDEX, int Spustit_2, int délka_HODNOTA, int HODNOTA) {
        for (int INDEX = 0; INDEX < délka_HODNOTA; INDEX += 2)
            HODNOTA += (rámec_INDEX[Spustit_2 + INDEX] << 8) | (INDEX + 1 < délka_HODNOTA ? rámec_INDEX[Spustit_2 + INDEX + 1] : 0);
        while ((HODNOTA >>> 16) != 0) HODNOTA = (HODNOTA & 65535) + (HODNOTA >>> 16);
        return HODNOTA;
    }
    static int 가상머리합(int 출발, int 도착, int délka_HODNOTA) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + délka_HODNOTA;
    }

    static void Čisté_Proces() {
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            접속번호들[INDEX] = 0; RECEIVED_délka[INDEX] = -1; RECEIVED_ODKAZ[INDEX] = 0; RECEIVED_číslo_portu[INDEX] = 0;
        }
        for (int INDEX = 0; INDEX < 64; INDEX++) if (síť_ovladač.dostat(vstup_rámec) == 0) break;
    }
    static int INDEX(int úchyt_HODNOTA) { return úchyt_HODNOTA >= 3 && úchyt_HODNOTA < 7 && 접속번호들[úchyt_HODNOTA - 3] != 0 ? úchyt_HODNOTA - 3 : -1; }
    static int Otevřít(int číslo_portu) {
        if (síť_ovladač.입출력기준주소 == 0) return -19;
        if (číslo_portu < 0 || číslo_portu > 65535) return -22;
        if (číslo_portu != 0) for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == číslo_portu) return -98;
        for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == 0) {
            if (číslo_portu == 0) {
                číslo_portu = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int přední_fotoaparát_HODNOTA = 0; přední_fotoaparát_HODNOTA < 4; přední_fotoaparát_HODNOTA++) if (접속번호들[přední_fotoaparát_HODNOTA] == číslo_portu) 겹침 = true;
                    if (겹침) číslo_portu++;
                }
            }
            접속번호들[INDEX] = číslo_portu; RECEIVED_délka[INDEX] = -1;
            return INDEX + 3;
        }
        return -24;
    }
    static int Zavřené(int úchyt_HODNOTA) {
        int přihrádka_položka = INDEX(úchyt_HODNOTA);
        if (přihrádka_položka < 0) return -9;
        접속번호들[přihrádka_položka] = 0; RECEIVED_délka[přihrádka_položka] = -1;
        return 0;
    }
    static int partner_ODKAZ(int úchyt_HODNOTA) { int přihrádka_položka = INDEX(úchyt_HODNOTA); return přihrádka_položka < 0 ? -9 : RECEIVED_ODKAZ[přihrádka_položka]; }
    static int partner_číslo_portu(int úchyt_HODNOTA) { int přihrádka_položka = INDEX(úchyt_HODNOTA); return přihrádka_položka < 0 ? -9 : RECEIVED_číslo_portu[přihrádka_položka]; }

    static void 바깥머리(int Druh_HODNOTA, boolean vysílat_HODNOTA) {
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            výstup_rámec[INDEX] = vysílat_HODNOTA ? 255 : 찾은장치[INDEX];
            výstup_rámec[6 + INDEX] = síť_ovladač.mobilní_ODKAZ[INDEX];
        }
        넣기16(výstup_rámec, 12, Druh_HODNOTA);
    }
    static void žádost_ODKAZ(int cíl_HODNOTA) {
        바깥머리(0x0806, true);
        넣기16(výstup_rámec, 14, 1); 넣기16(výstup_rámec, 16, 0x0800);
        výstup_rámec[18] = 6; výstup_rámec[19] = 4; 넣기16(výstup_rámec, 20, 1);
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            výstup_rámec[22 + INDEX] = síť_ovladač.mobilní_ODKAZ[INDEX]; výstup_rámec[32 + INDEX] = 0;
        }
        넣기32(výstup_rámec, 28, 내주소); 넣기32(výstup_rámec, 38, cíl_HODNOTA);
        síť_ovladač.poslat(výstup_rámec, 42);
    }
    static void Proces_ODKAZ(int délka_HODNOTA) {
        if (délka_HODNOTA < 42 || integer_16(vstup_rámec, 14) != 1 || integer_16(vstup_rámec, 16) != 0x0800
            || vstup_rámec[18] != 6 || vstup_rámec[19] != 4 || integer_32(vstup_rámec, 38) != 내주소) { 폐기수++; return; }
        int Druh_HODNOTA = integer_16(vstup_rámec, 20), partner_HODNOTA = integer_32(vstup_rámec, 28);
        if (Druh_HODNOTA == 2 && partner_HODNOTA == 찾을주소) {
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                if (vstup_rámec[6 + INDEX] != vstup_rámec[22 + INDEX] || vstup_rámec[32 + INDEX] != síť_ovladač.mobilní_ODKAZ[INDEX]) return;
            }
            for (int INDEX = 0; INDEX < 6; INDEX++) 찾은장치[INDEX] = vstup_rámec[22 + INDEX];
            찾은주소 = partner_HODNOTA;
        } else if (Druh_HODNOTA == 1) {
            바깥머리(0x0806, false);
            넣기16(výstup_rámec, 14, 1); 넣기16(výstup_rámec, 16, 0x0800);
            výstup_rámec[18] = 6; výstup_rámec[19] = 4; 넣기16(výstup_rámec, 20, 2);
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                výstup_rámec[INDEX] = vstup_rámec[22 + INDEX]; výstup_rámec[32 + INDEX] = vstup_rámec[22 + INDEX];
                výstup_rámec[22 + INDEX] = síť_ovladač.mobilní_ODKAZ[INDEX];
            }
            넣기32(výstup_rámec, 28, 내주소); 넣기32(výstup_rámec, 38, partner_HODNOTA);
            síť_ovladač.poslat(výstup_rámec, 42);
        }
    }

    static void Proces_rámec(int délka_HODNOTA) {
        if (délka_HODNOTA < 14 || délka_HODNOTA > vstup_rámec.length) { 폐기수++; return; }
        boolean 자기 = true, vysílat_HODNOTA = true;
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            if (vstup_rámec[INDEX] != síť_ovladač.mobilní_ODKAZ[INDEX]) 자기 = false;
            if (vstup_rámec[INDEX] != 255) vysílat_HODNOTA = false;
        }
        if (!자기 && !vysílat_HODNOTA) return;
        if (integer_16(vstup_rámec, 12) == 0x0806) { Proces_ODKAZ(délka_HODNOTA); return; }
        if (integer_16(vstup_rámec, 12) != 0x0800) return;
        if (délka_HODNOTA < 34 || (vstup_rámec[14] >>> 4) != 4) { 폐기수++; return; }
        int Nadpis_délka = (vstup_rámec[14] & 15) * 4, celkem_délka = integer_16(vstup_rámec, 16);
        if (Nadpis_délka < 20 || Nadpis_délka > 60 || celkem_délka < Nadpis_délka + 8 || celkem_délka > délka_HODNOTA - 14
            || (integer_16(vstup_rámec, 20) & 0x3fff) != 0 || vstup_rámec[23] != 17
            || integer_32(vstup_rámec, 30) != 내주소 || SUMA_HODNOTA(vstup_rámec, 14, Nadpis_délka, 0) != 65535) { 폐기수++; return; }
        int Spustit_2 = 14 + Nadpis_délka, data_délka = integer_16(vstup_rámec, Spustit_2 + 4);
        if (data_délka < 8 || data_délka != celkem_délka - Nadpis_délka || data_délka > 1032) { 폐기수++; return; }
        int 출발 = integer_32(vstup_rámec, 26);
        if (integer_16(vstup_rámec, Spustit_2 + 6) != 0 && SUMA_HODNOTA(vstup_rámec, Spustit_2, data_délka, 가상머리합(출발, 내주소, data_délka)) != 65535) {
            폐기수++; return;
        }
        int cíl_HODNOTA = integer_16(vstup_rámec, Spustit_2 + 2);
        for (int přihrádka_položka = 0; přihrádka_položka < 4; přihrádka_položka++) if (접속번호들[přihrádka_položka] != 0 && 접속번호들[přihrádka_položka] == cíl_HODNOTA) {
            if (RECEIVED_délka[přihrádka_položka] >= 0) { 폐기수++; return; }
            RECEIVED_délka[přihrádka_položka] = data_délka - 8; RECEIVED_ODKAZ[přihrádka_položka] = 출발; RECEIVED_číslo_portu[přihrádka_položka] = integer_16(vstup_rámec, Spustit_2);
            for (int INDEX = 0; INDEX < data_délka - 8; INDEX++) RECEIVED_data[přihrádka_položka * 1024 + INDEX] = vstup_rámec[Spustit_2 + 8 + INDEX];
            return;
        }
    }

    static void ověřit() {
        for (int INDEX = 0; INDEX < 16; INDEX++) {
            int délka_HODNOTA = síť_ovladač.dostat(vstup_rámec);
            if (délka_HODNOTA == 0) return;
            Proces_rámec(délka_HODNOTA);
        }
    }
    static int NAJÍT_ODKAZ(int Adresa) {
        if (Adresa == 0 || Adresa == -1 || (Adresa >>> 28) >= 14 || (Adresa >>> 24) == 127 || Adresa == 내주소) return -101;
        int Další_zboží = (Adresa & síť_maska) == (내주소 & síť_maska) ? Adresa : brána_HODNOTA;
        if (Další_zboží == 찾은주소) return 0;
        찾을주소 = Další_zboží;
        int Spustit_2 = mobilní_HODNOTA.밀리초(), Další_žádost = Spustit_2;
        while (mobilní_HODNOTA.밀리초() - Spustit_2 < 1000) {
            if (mobilní_HODNOTA.밀리초() - Další_žádost >= 0) { žádost_ODKAZ(Další_zboží); Další_žádost += 300; }
            ověřit();
            if (찾은주소 == Další_zboží) return 0;
            mobilní_HODNOTA.잠시양보();
        }
        return -110;
    }
    static int poslat(int úchyt_HODNOTA, int Adresa, int číslo_portu, int[] data, int délka_HODNOTA) {
        int přihrádka_položka = INDEX(úchyt_HODNOTA);
        if (přihrádka_položka < 0) return -9;
        if (síť_ovladač.입출력기준주소 == 0) return -19;
        if (číslo_portu < 1 || číslo_portu > 65535 || délka_HODNOTA < 0 || délka_HODNOTA > 1024) return -22;
        int VÝSLEDEK = NAJÍT_ODKAZ(Adresa);
        if (VÝSLEDEK < 0) return VÝSLEDEK;
        바깥머리(0x0800, false);
        výstup_rámec[14] = 0x45; výstup_rámec[15] = 0; 넣기16(výstup_rámec, 16, 28 + délka_HODNOTA);
        넣기16(výstup_rámec, 18, identifikátor_HODNOTA++); 넣기16(výstup_rámec, 20, 0x4000);
        výstup_rámec[22] = 64; výstup_rámec[23] = 17; 넣기16(výstup_rámec, 24, 0);
        넣기32(výstup_rámec, 26, 내주소); 넣기32(výstup_rámec, 30, Adresa);
        넣기16(výstup_rámec, 24, ~SUMA_HODNOTA(výstup_rámec, 14, 20, 0));
        넣기16(výstup_rámec, 34, 접속번호들[přihrádka_položka]); 넣기16(výstup_rámec, 36, číslo_portu);
        넣기16(výstup_rámec, 38, délka_HODNOTA + 8); 넣기16(výstup_rámec, 40, 0);
        for (int INDEX = 0; INDEX < délka_HODNOTA; INDEX++) výstup_rámec[42 + INDEX] = data[INDEX] & 255;
        int kontrolní_součet = (~SUMA_HODNOTA(výstup_rámec, 34, délka_HODNOTA + 8, 가상머리합(내주소, Adresa, délka_HODNOTA + 8))) & 65535;
        넣기16(výstup_rámec, 40, kontrolní_součet == 0 ? 65535 : kontrolní_součet);
        VÝSLEDEK = síť_ovladač.poslat(výstup_rámec, délka_HODNOTA + 42);
        return VÝSLEDEK < 0 ? VÝSLEDEK : délka_HODNOTA;
    }
    static int dostat(int úchyt_HODNOTA, int[] data, int kapacita_HODNOTA, int 제한) {
        int přihrádka_položka = INDEX(úchyt_HODNOTA);
        if (přihrádka_položka < 0) return -9;
        int Spustit_2 = mobilní_HODNOTA.밀리초();
        while (true) {
            ověřit();
            int délka_HODNOTA = RECEIVED_délka[přihrádka_položka];
            if (délka_HODNOTA >= 0) {
                RECEIVED_délka[přihrádka_položka] = -1;
                if (délka_HODNOTA > kapacita_HODNOTA) return -90;
                for (int INDEX = 0; INDEX < délka_HODNOTA; INDEX++) data[INDEX] = RECEIVED_data[přihrádka_položka * 1024 + INDEX];
                return délka_HODNOTA;
            }
            if (제한 == 0) return -11;
            if (mobilní_HODNOTA.밀리초() - Spustit_2 >= 제한) return -110;
            mobilní_HODNOTA.잠시양보();
        }
    }
    static void Stav_HODNOTA() {
        SMS_Terminál.Zápis(síť_ovladač.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Terminál.Zápis("TX: "); SMS_Terminál.zápis_číslo(síť_ovladač.송신수);
        SMS_Terminál.Zápis(" RX: "); SMS_Terminál.zápis_číslo(síť_ovladač.dostat_POČET);
        SMS_Terminál.Zápis(" DROP: "); SMS_Terminál.zápis_číslo(폐기수);
        SMS_Terminál.Zápis("\n");
    }
}
