// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** statisk_VALUE IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class Nettverk_Stabel {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int Nettverk_maske = 0xffffff00; /* ip.conf:NETMASK */
    static final int gateway_VALUE = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], RECEIVED_lengd = new int[4], RECEIVED_ADDRESS = new int[4], RECEIVED_portnummer = new int[4];
    static int[] RECEIVED_data = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, identifikator_VALUE = 0, 폐기수 = 0;

    static int heiltal_16(int[] rute_INDEX, int Posisjon) { return (rute_INDEX[Posisjon] << 8) | rute_INDEX[Posisjon + 1]; }
    static int heiltal_32(int[] rute_INDEX, int Posisjon) { return (heiltal_16(rute_INDEX, Posisjon) << 16) | heiltal_16(rute_INDEX, Posisjon + 2); }
    static void 넣기16(int[] rute_INDEX, int Posisjon, int VALUE) { rute_INDEX[Posisjon] = (VALUE >>> 8) & 255; rute_INDEX[Posisjon + 1] = VALUE & 255; }
    static void 넣기32(int[] rute_INDEX, int Posisjon, int VALUE) { 넣기16(rute_INDEX, Posisjon, VALUE >>> 16); 넣기16(rute_INDEX, Posisjon + 2, VALUE); }
    static int SUM_VALUE(int[] rute_INDEX, int Køyr_2, int lengd_VALUE, int VALUE) {
        for (int INDEX = 0; INDEX < lengd_VALUE; INDEX += 2)
            VALUE += (rute_INDEX[Køyr_2 + INDEX] << 8) | (INDEX + 1 < lengd_VALUE ? rute_INDEX[Køyr_2 + INDEX + 1] : 0);
        while ((VALUE >>> 16) != 0) VALUE = (VALUE & 65535) + (VALUE >>> 16);
        return VALUE;
    }
    static int 가상머리합(int 출발, int 도착, int lengd_VALUE) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + lengd_VALUE;
    }

    static void CLEAN_Prosess() {
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            접속번호들[INDEX] = 0; RECEIVED_lengd[INDEX] = -1; RECEIVED_ADDRESS[INDEX] = 0; RECEIVED_portnummer[INDEX] = 0;
        }
        for (int INDEX = 0; INDEX < 64; INDEX++) if (Nettverk_drivar.받기(입력틀) == 0) break;
    }
    static int INDEX(int handtak_VALUE) { return handtak_VALUE >= 3 && handtak_VALUE < 7 && 접속번호들[handtak_VALUE - 3] != 0 ? handtak_VALUE - 3 : -1; }
    static int Opna(int portnummer) {
        if (Nettverk_drivar.입출력기준주소 == 0) return -19;
        if (portnummer < 0 || portnummer > 65535) return -22;
        if (portnummer != 0) for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == portnummer) return -98;
        for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == 0) {
            if (portnummer == 0) {
                portnummer = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int 앞 = 0; 앞 < 4; 앞++) if (접속번호들[앞] == portnummer) 겹침 = true;
                    if (겹침) portnummer++;
                }
            }
            접속번호들[INDEX] = portnummer; RECEIVED_lengd[INDEX] = -1;
            return INDEX + 3;
        }
        return -24;
    }
    static int Lukk(int handtak_VALUE) {
        int felt_oppføring = INDEX(handtak_VALUE);
        if (felt_oppføring < 0) return -9;
        접속번호들[felt_oppføring] = 0; RECEIVED_lengd[felt_oppføring] = -1;
        return 0;
    }
    static int node_ADDRESS(int handtak_VALUE) { int felt_oppføring = INDEX(handtak_VALUE); return felt_oppføring < 0 ? -9 : RECEIVED_ADDRESS[felt_oppføring]; }
    static int node_portnummer(int handtak_VALUE) { int felt_oppføring = INDEX(handtak_VALUE); return felt_oppføring < 0 ? -9 : RECEIVED_portnummer[felt_oppføring]; }

    static void 바깥머리(int 종류, boolean kringkasting_VALUE) {
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[INDEX] = kringkasting_VALUE ? 255 : 찾은장치[INDEX];
            출력틀[6 + INDEX] = Nettverk_drivar.mobil_ADDRESS[INDEX];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void 주소요청(int mål_VALUE) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[22 + INDEX] = Nettverk_drivar.mobil_ADDRESS[INDEX]; 출력틀[32 + INDEX] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, mål_VALUE);
        Nettverk_drivar.sende(출력틀, 42);
    }
    static void Prosess_ADDRESS(int lengd_VALUE) {
        if (lengd_VALUE < 42 || heiltal_16(입력틀, 14) != 1 || heiltal_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || heiltal_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = heiltal_16(입력틀, 20), node_VALUE_6a3b6fa7 = heiltal_32(입력틀, 28);
        if (종류 == 2 && node_VALUE_6a3b6fa7 == 찾을주소) {
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                if (입력틀[6 + INDEX] != 입력틀[22 + INDEX] || 입력틀[32 + INDEX] != Nettverk_drivar.mobil_ADDRESS[INDEX]) return;
            }
            for (int INDEX = 0; INDEX < 6; INDEX++) 찾은장치[INDEX] = 입력틀[22 + INDEX];
            찾은주소 = node_VALUE_6a3b6fa7;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                출력틀[INDEX] = 입력틀[22 + INDEX]; 출력틀[32 + INDEX] = 입력틀[22 + INDEX];
                출력틀[22 + INDEX] = Nettverk_drivar.mobil_ADDRESS[INDEX];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, node_VALUE_6a3b6fa7);
            Nettverk_drivar.sende(출력틀, 42);
        }
    }

    static void Prosess_rute(int lengd_VALUE) {
        if (lengd_VALUE < 14 || lengd_VALUE > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, kringkasting_VALUE = true;
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            if (입력틀[INDEX] != Nettverk_drivar.mobil_ADDRESS[INDEX]) 자기 = false;
            if (입력틀[INDEX] != 255) kringkasting_VALUE = false;
        }
        if (!자기 && !kringkasting_VALUE) return;
        if (heiltal_16(입력틀, 12) == 0x0806) { Prosess_ADDRESS(lengd_VALUE); return; }
        if (heiltal_16(입력틀, 12) != 0x0800) return;
        if (lengd_VALUE < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int hode_lengd = (입력틀[14] & 15) * 4, 전체길이 = heiltal_16(입력틀, 16);
        if (hode_lengd < 20 || hode_lengd > 60 || 전체길이 < hode_lengd + 8 || 전체길이 > lengd_VALUE - 14
            || (heiltal_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || heiltal_32(입력틀, 30) != 내주소 || SUM_VALUE(입력틀, 14, hode_lengd, 0) != 65535) { 폐기수++; return; }
        int Køyr_2 = 14 + hode_lengd, data_lengd = heiltal_16(입력틀, Køyr_2 + 4);
        if (data_lengd < 8 || data_lengd != 전체길이 - hode_lengd || data_lengd > 1032) { 폐기수++; return; }
        int 출발 = heiltal_32(입력틀, 26);
        if (heiltal_16(입력틀, Køyr_2 + 6) != 0 && SUM_VALUE(입력틀, Køyr_2, data_lengd, 가상머리합(출발, 내주소, data_lengd)) != 65535) {
            폐기수++; return;
        }
        int mål_VALUE = heiltal_16(입력틀, Køyr_2 + 2);
        for (int felt_oppføring = 0; felt_oppføring < 4; felt_oppføring++) if (접속번호들[felt_oppføring] != 0 && 접속번호들[felt_oppføring] == mål_VALUE) {
            if (RECEIVED_lengd[felt_oppføring] >= 0) { 폐기수++; return; }
            RECEIVED_lengd[felt_oppføring] = data_lengd - 8; RECEIVED_ADDRESS[felt_oppføring] = 출발; RECEIVED_portnummer[felt_oppføring] = heiltal_16(입력틀, Køyr_2);
            for (int INDEX = 0; INDEX < data_lengd - 8; INDEX++) RECEIVED_data[felt_oppføring * 1024 + INDEX] = 입력틀[Køyr_2 + 8 + INDEX];
            return;
        }
    }

    static void stadfeste() {
        for (int INDEX = 0; INDEX < 16; INDEX++) {
            int lengd_VALUE = Nettverk_drivar.받기(입력틀);
            if (lengd_VALUE == 0) return;
            Prosess_rute(lengd_VALUE);
        }
    }
    static int Søk_ADDRESS(int ADDRESS) {
        if (ADDRESS == 0 || ADDRESS == -1 || (ADDRESS >>> 28) >= 14 || (ADDRESS >>> 24) == 127 || ADDRESS == 내주소) return -101;
        int Neste_vare = (ADDRESS & Nettverk_maske) == (내주소 & Nettverk_maske) ? ADDRESS : gateway_VALUE;
        if (Neste_vare == 찾은주소) return 0;
        찾을주소 = Neste_vare;
        int Køyr_2 = mobil_VALUE.밀리초(), 다음요청 = Køyr_2;
        while (mobil_VALUE.밀리초() - Køyr_2 < 1000) {
            if (mobil_VALUE.밀리초() - 다음요청 >= 0) { 주소요청(Neste_vare); 다음요청 += 300; }
            stadfeste();
            if (찾은주소 == Neste_vare) return 0;
            mobil_VALUE.잠시양보();
        }
        return -110;
    }
    static int sende(int handtak_VALUE, int ADDRESS, int portnummer, int[] data, int lengd_VALUE) {
        int felt_oppføring = INDEX(handtak_VALUE);
        if (felt_oppføring < 0) return -9;
        if (Nettverk_drivar.입출력기준주소 == 0) return -19;
        if (portnummer < 1 || portnummer > 65535 || lengd_VALUE < 0 || lengd_VALUE > 1024) return -22;
        int forretningsmål = Søk_ADDRESS(ADDRESS);
        if (forretningsmål < 0) return forretningsmål;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + lengd_VALUE);
        넣기16(출력틀, 18, identifikator_VALUE++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, ADDRESS);
        넣기16(출력틀, 24, ~SUM_VALUE(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[felt_oppføring]); 넣기16(출력틀, 36, portnummer);
        넣기16(출력틀, 38, lengd_VALUE + 8); 넣기16(출력틀, 40, 0);
        for (int INDEX = 0; INDEX < lengd_VALUE; INDEX++) 출력틀[42 + INDEX] = data[INDEX] & 255;
        int kontrollsum = (~SUM_VALUE(출력틀, 34, lengd_VALUE + 8, 가상머리합(내주소, ADDRESS, lengd_VALUE + 8))) & 65535;
        넣기16(출력틀, 40, kontrollsum == 0 ? 65535 : kontrollsum);
        forretningsmål = Nettverk_drivar.sende(출력틀, lengd_VALUE + 42);
        return forretningsmål < 0 ? forretningsmål : lengd_VALUE;
    }
    static int 받기(int handtak_VALUE, int[] data, int 용량, int 제한) {
        int felt_oppføring = INDEX(handtak_VALUE);
        if (felt_oppføring < 0) return -9;
        int Køyr_2 = mobil_VALUE.밀리초();
        while (true) {
            stadfeste();
            int lengd_VALUE = RECEIVED_lengd[felt_oppføring];
            if (lengd_VALUE >= 0) {
                RECEIVED_lengd[felt_oppføring] = -1;
                if (lengd_VALUE > 용량) return -90;
                for (int INDEX = 0; INDEX < lengd_VALUE; INDEX++) data[INDEX] = RECEIVED_data[felt_oppføring * 1024 + INDEX];
                return lengd_VALUE;
            }
            if (제한 == 0) return -11;
            if (mobil_VALUE.밀리초() - Køyr_2 >= 제한) return -110;
            mobil_VALUE.잠시양보();
        }
    }
    static void status_VALUE() {
        SMS_Terminal.Skriv(Nettverk_drivar.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Terminal.Skriv("TX: "); SMS_Terminal.수쓰기(Nettverk_drivar.송신수);
        SMS_Terminal.Skriv(" RX: "); SMS_Terminal.수쓰기(Nettverk_drivar.수신수);
        SMS_Terminal.Skriv(" DROP: "); SMS_Terminal.수쓰기(폐기수);
        SMS_Terminal.Skriv("\n");
    }
}
