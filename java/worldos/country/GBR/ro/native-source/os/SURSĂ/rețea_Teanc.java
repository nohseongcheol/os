// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 정적 IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class rețea_Teanc {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int rețea_mască = 0xffffff00; /* ip.conf:NETMASK */
    static final int gateway_VALUE = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], RECEIVED_lungime = new int[4], RECEIVED_adresa = new int[4], RECEIVED_număr_port = new int[4];
    static int[] RECEIVED_date = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, identificator_VALUE = 0, 폐기수 = 0;

    static int întreg_16(int[] cadru_INDEX, int Poziție) { return (cadru_INDEX[Poziție] << 8) | cadru_INDEX[Poziție + 1]; }
    static int întreg_32(int[] cadru_INDEX, int Poziție) { return (întreg_16(cadru_INDEX, Poziție) << 16) | întreg_16(cadru_INDEX, Poziție + 2); }
    static void 넣기16(int[] cadru_INDEX, int Poziție, int VALUE) { cadru_INDEX[Poziție] = (VALUE >>> 8) & 255; cadru_INDEX[Poziție + 1] = VALUE & 255; }
    static void 넣기32(int[] cadru_INDEX, int Poziție, int VALUE) { 넣기16(cadru_INDEX, Poziție, VALUE >>> 16); 넣기16(cadru_INDEX, Poziție + 2, VALUE); }
    static int SUM_VALUE(int[] cadru_INDEX, int Pornește, int lungime_VALUE, int VALUE) {
        for (int INDEX = 0; INDEX < lungime_VALUE; INDEX += 2)
            VALUE += (cadru_INDEX[Pornește + INDEX] << 8) | (INDEX + 1 < lungime_VALUE ? cadru_INDEX[Pornește + INDEX + 1] : 0);
        while ((VALUE >>> 16) != 0) VALUE = (VALUE & 65535) + (VALUE >>> 16);
        return VALUE;
    }
    static int 가상머리합(int 출발, int 도착, int lungime_VALUE) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + lungime_VALUE;
    }

    static void CLEAN_Proces() {
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            접속번호들[INDEX] = 0; RECEIVED_lungime[INDEX] = -1; RECEIVED_adresa[INDEX] = 0; RECEIVED_număr_port[INDEX] = 0;
        }
        for (int INDEX = 0; INDEX < 64; INDEX++) if (rețea_driver.primi(입력틀) == 0) break;
    }
    static int INDEX(int handle_VALUE) { return handle_VALUE >= 3 && handle_VALUE < 7 && 접속번호들[handle_VALUE - 3] != 0 ? handle_VALUE - 3 : -1; }
    static int Deschide(int număr_port) {
        if (rețea_driver.입출력기준주소 == 0) return -19;
        if (număr_port < 0 || număr_port > 65535) return -22;
        if (număr_port != 0) for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == număr_port) return -98;
        for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == 0) {
            if (număr_port == 0) {
                număr_port = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int frontală_VALUE = 0; frontală_VALUE < 4; frontală_VALUE++) if (접속번호들[frontală_VALUE] == număr_port) 겹침 = true;
                    if (겹침) număr_port++;
                }
            }
            접속번호들[INDEX] = număr_port; RECEIVED_lungime[INDEX] = -1;
            return INDEX + 3;
        }
        return -24;
    }
    static int Închide(int handle_VALUE) {
        int 칸 = INDEX(handle_VALUE);
        if (칸 < 0) return -9;
        접속번호들[칸] = 0; RECEIVED_lungime[칸] = -1;
        return 0;
    }
    static int pereche_adresa(int handle_VALUE) { int 칸 = INDEX(handle_VALUE); return 칸 < 0 ? -9 : RECEIVED_adresa[칸]; }
    static int pereche_număr_port(int handle_VALUE) { int 칸 = INDEX(handle_VALUE); return 칸 < 0 ? -9 : RECEIVED_număr_port[칸]; }

    static void 바깥머리(int 종류, boolean difuza_VALUE) {
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[INDEX] = difuza_VALUE ? 255 : 찾은장치[INDEX];
            출력틀[6 + INDEX] = rețea_driver.mobil_adresa[INDEX];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void cerere_adresa(int destinație_VALUE) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[22 + INDEX] = rețea_driver.mobil_adresa[INDEX]; 출력틀[32 + INDEX] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, destinație_VALUE);
        rețea_driver.trimite(출력틀, 42);
    }
    static void Proces_adresa(int lungime_VALUE) {
        if (lungime_VALUE < 42 || întreg_16(입력틀, 14) != 1 || întreg_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || întreg_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = întreg_16(입력틀, 20), pereche_VALUE = întreg_32(입력틀, 28);
        if (종류 == 2 && pereche_VALUE == 찾을주소) {
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                if (입력틀[6 + INDEX] != 입력틀[22 + INDEX] || 입력틀[32 + INDEX] != rețea_driver.mobil_adresa[INDEX]) return;
            }
            for (int INDEX = 0; INDEX < 6; INDEX++) 찾은장치[INDEX] = 입력틀[22 + INDEX];
            찾은주소 = pereche_VALUE;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                출력틀[INDEX] = 입력틀[22 + INDEX]; 출력틀[32 + INDEX] = 입력틀[22 + INDEX];
                출력틀[22 + INDEX] = rețea_driver.mobil_adresa[INDEX];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, pereche_VALUE);
            rețea_driver.trimite(출력틀, 42);
        }
    }

    static void Proces_cadru(int lungime_VALUE) {
        if (lungime_VALUE < 14 || lungime_VALUE > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, difuza_VALUE = true;
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            if (입력틀[INDEX] != rețea_driver.mobil_adresa[INDEX]) 자기 = false;
            if (입력틀[INDEX] != 255) difuza_VALUE = false;
        }
        if (!자기 && !difuza_VALUE) return;
        if (întreg_16(입력틀, 12) == 0x0806) { Proces_adresa(lungime_VALUE); return; }
        if (întreg_16(입력틀, 12) != 0x0800) return;
        if (lungime_VALUE < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int Antet_lungime = (입력틀[14] & 15) * 4, total_lungime = întreg_16(입력틀, 16);
        if (Antet_lungime < 20 || Antet_lungime > 60 || total_lungime < Antet_lungime + 8 || total_lungime > lungime_VALUE - 14
            || (întreg_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || întreg_32(입력틀, 30) != 내주소 || SUM_VALUE(입력틀, 14, Antet_lungime, 0) != 65535) { 폐기수++; return; }
        int Pornește = 14 + Antet_lungime, date_lungime = întreg_16(입력틀, Pornește + 4);
        if (date_lungime < 8 || date_lungime != total_lungime - Antet_lungime || date_lungime > 1032) { 폐기수++; return; }
        int 출발 = întreg_32(입력틀, 26);
        if (întreg_16(입력틀, Pornește + 6) != 0 && SUM_VALUE(입력틀, Pornește, date_lungime, 가상머리합(출발, 내주소, date_lungime)) != 65535) {
            폐기수++; return;
        }
        int destinație_VALUE = întreg_16(입력틀, Pornește + 2);
        for (int 칸 = 0; 칸 < 4; 칸++) if (접속번호들[칸] != 0 && 접속번호들[칸] == destinație_VALUE) {
            if (RECEIVED_lungime[칸] >= 0) { 폐기수++; return; }
            RECEIVED_lungime[칸] = date_lungime - 8; RECEIVED_adresa[칸] = 출발; RECEIVED_număr_port[칸] = întreg_16(입력틀, Pornește);
            for (int INDEX = 0; INDEX < date_lungime - 8; INDEX++) RECEIVED_date[칸 * 1024 + INDEX] = 입력틀[Pornește + 8 + INDEX];
            return;
        }
    }

    static void verifica() {
        for (int INDEX = 0; INDEX < 16; INDEX++) {
            int lungime_VALUE = rețea_driver.primi(입력틀);
            if (lungime_VALUE == 0) return;
            Proces_cadru(lungime_VALUE);
        }
    }
    static int FIND_adresa(int adresa) {
        if (adresa == 0 || adresa == -1 || (adresa >>> 28) >= 14 || (adresa >>> 24) == 127 || adresa == 내주소) return -101;
        int Următorul_element = (adresa & rețea_mască) == (내주소 & rețea_mască) ? adresa : gateway_VALUE;
        if (Următorul_element == 찾은주소) return 0;
        찾을주소 = Următorul_element;
        int Pornește = mobil_VALUE.밀리초(), Următorul_cerere = Pornește;
        while (mobil_VALUE.밀리초() - Pornește < 1000) {
            if (mobil_VALUE.밀리초() - Următorul_cerere >= 0) { cerere_adresa(Următorul_element); Următorul_cerere += 300; }
            verifica();
            if (찾은주소 == Următorul_element) return 0;
            mobil_VALUE.잠시양보();
        }
        return -110;
    }
    static int trimite(int handle_VALUE, int adresa, int număr_port, int[] date, int lungime_VALUE) {
        int 칸 = INDEX(handle_VALUE);
        if (칸 < 0) return -9;
        if (rețea_driver.입출력기준주소 == 0) return -19;
        if (număr_port < 1 || număr_port > 65535 || lungime_VALUE < 0 || lungime_VALUE > 1024) return -22;
        int KR = FIND_adresa(adresa);
        if (KR < 0) return KR;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + lungime_VALUE);
        넣기16(출력틀, 18, identificator_VALUE++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, adresa);
        넣기16(출력틀, 24, ~SUM_VALUE(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[칸]); 넣기16(출력틀, 36, număr_port);
        넣기16(출력틀, 38, lungime_VALUE + 8); 넣기16(출력틀, 40, 0);
        for (int INDEX = 0; INDEX < lungime_VALUE; INDEX++) 출력틀[42 + INDEX] = date[INDEX] & 255;
        int sumă_de_verificare = (~SUM_VALUE(출력틀, 34, lungime_VALUE + 8, 가상머리합(내주소, adresa, lungime_VALUE + 8))) & 65535;
        넣기16(출력틀, 40, sumă_de_verificare == 0 ? 65535 : sumă_de_verificare);
        KR = rețea_driver.trimite(출력틀, lungime_VALUE + 42);
        return KR < 0 ? KR : lungime_VALUE;
    }
    static int primi(int handle_VALUE, int[] date, int capacitate_VALUE, int 제한) {
        int 칸 = INDEX(handle_VALUE);
        if (칸 < 0) return -9;
        int Pornește = mobil_VALUE.밀리초();
        while (true) {
            verifica();
            int lungime_VALUE = RECEIVED_lungime[칸];
            if (lungime_VALUE >= 0) {
                RECEIVED_lungime[칸] = -1;
                if (lungime_VALUE > capacitate_VALUE) return -90;
                for (int INDEX = 0; INDEX < lungime_VALUE; INDEX++) date[INDEX] = RECEIVED_date[칸 * 1024 + INDEX];
                return lungime_VALUE;
            }
            if (제한 == 0) return -11;
            if (mobil_VALUE.밀리초() - Pornește >= 제한) return -110;
            mobil_VALUE.잠시양보();
        }
    }
    static void Stare_VALUE() {
        SMS_Terminal.Scriere(rețea_driver.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Terminal.Scriere("TX: "); SMS_Terminal.수쓰기(rețea_driver.송신수);
        SMS_Terminal.Scriere(" RX: "); SMS_Terminal.수쓰기(rețea_driver.primi_COUNT);
        SMS_Terminal.Scriere(" DROP: "); SMS_Terminal.수쓰기(폐기수);
        SMS_Terminal.Scriere("\n");
    }
}
