// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** staties_VALUE IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class Netwerk_Stapel {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int Netwerk_masker = 0xffffff00; /* ip.conf:NETMASK */
    static final int deurgang_VALUE = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], RECEIVED_lengte = new int[4], RECEIVED_adres = new int[4], 받은접속번호 = new int[4];
    static int[] RECEIVED_data = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, waarde_VALUE = 0, 폐기수 = 0;

    static int heelgetal_16(int[] raam_INDEX, int Posisie) { return (raam_INDEX[Posisie] << 8) | raam_INDEX[Posisie + 1]; }
    static int heelgetal_32(int[] raam_INDEX, int Posisie) { return (heelgetal_16(raam_INDEX, Posisie) << 16) | heelgetal_16(raam_INDEX, Posisie + 2); }
    static void 넣기16(int[] raam_INDEX, int Posisie, int VALUE) { raam_INDEX[Posisie] = (VALUE >>> 8) & 255; raam_INDEX[Posisie + 1] = VALUE & 255; }
    static void 넣기32(int[] raam_INDEX, int Posisie, int VALUE) { 넣기16(raam_INDEX, Posisie, VALUE >>> 16); 넣기16(raam_INDEX, Posisie + 2, VALUE); }
    static int SUM_VALUE(int[] raam_INDEX, int Loop, int lengte_VALUE, int VALUE) {
        for (int INDEX = 0; INDEX < lengte_VALUE; INDEX += 2)
            VALUE += (raam_INDEX[Loop + INDEX] << 8) | (INDEX + 1 < lengte_VALUE ? raam_INDEX[Loop + INDEX + 1] : 0);
        while ((VALUE >>> 16) != 0) VALUE = (VALUE & 65535) + (VALUE >>> 16);
        return VALUE;
    }
    static int 가상머리합(int 출발, int 도착, int lengte_VALUE) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + lengte_VALUE;
    }

    static void CLEAN_Proses() {
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            접속번호들[INDEX] = 0; RECEIVED_lengte[INDEX] = -1; RECEIVED_adres[INDEX] = 0; 받은접속번호[INDEX] = 0;
        }
        for (int INDEX = 0; INDEX < 64; INDEX++) if (Netwerk_drywer.받기(입력틀) == 0) break;
    }
    static int INDEX(int handvatsel_VALUE) { return handvatsel_VALUE >= 3 && handvatsel_VALUE < 7 && 접속번호들[handvatsel_VALUE - 3] != 0 ? handvatsel_VALUE - 3 : -1; }
    static int skep(int 접속번호) {
        if (Netwerk_drywer.입출력기준주소 == 0) return -19;
        if (접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 != 0) for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == 접속번호) return -98;
        for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == 0) {
            if (접속번호 == 0) {
                접속번호 = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int voor_VALUE = 0; voor_VALUE < 4; voor_VALUE++) if (접속번호들[voor_VALUE] == 접속번호) 겹침 = true;
                    if (겹침) 접속번호++;
                }
            }
            접속번호들[INDEX] = 접속번호; RECEIVED_lengte[INDEX] = -1;
            return INDEX + 3;
        }
        return -24;
    }
    static int Sluit(int handvatsel_VALUE) {
        int gleuf_inskrywing = INDEX(handvatsel_VALUE);
        if (gleuf_inskrywing < 0) return -9;
        접속번호들[gleuf_inskrywing] = 0; RECEIVED_lengte[gleuf_inskrywing] = -1;
        return 0;
    }
    static int portuur_adres(int handvatsel_VALUE) { int gleuf_inskrywing = INDEX(handvatsel_VALUE); return gleuf_inskrywing < 0 ? -9 : RECEIVED_adres[gleuf_inskrywing]; }
    static int 상대접속번호(int handvatsel_VALUE) { int gleuf_inskrywing = INDEX(handvatsel_VALUE); return gleuf_inskrywing < 0 ? -9 : 받은접속번호[gleuf_inskrywing]; }

    static void 바깥머리(int 종류, boolean uitsaai_VALUE) {
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[INDEX] = uitsaai_VALUE ? 255 : 찾은장치[INDEX];
            출력틀[6 + INDEX] = Netwerk_drywer.mobiel_adres[INDEX];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void 주소요청(int bestemming_VALUE) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[22 + INDEX] = Netwerk_drywer.mobiel_adres[INDEX]; 출력틀[32 + INDEX] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, bestemming_VALUE);
        Netwerk_drywer.e_pos(출력틀, 42);
    }
    static void Proses_adres(int lengte_VALUE) {
        if (lengte_VALUE < 42 || heelgetal_16(입력틀, 14) != 1 || heelgetal_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || heelgetal_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = heelgetal_16(입력틀, 20), portuur_VALUE = heelgetal_32(입력틀, 28);
        if (종류 == 2 && portuur_VALUE == 찾을주소) {
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                if (입력틀[6 + INDEX] != 입력틀[22 + INDEX] || 입력틀[32 + INDEX] != Netwerk_drywer.mobiel_adres[INDEX]) return;
            }
            for (int INDEX = 0; INDEX < 6; INDEX++) 찾은장치[INDEX] = 입력틀[22 + INDEX];
            찾은주소 = portuur_VALUE;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                출력틀[INDEX] = 입력틀[22 + INDEX]; 출력틀[32 + INDEX] = 입력틀[22 + INDEX];
                출력틀[22 + INDEX] = Netwerk_drywer.mobiel_adres[INDEX];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, portuur_VALUE);
            Netwerk_drywer.e_pos(출력틀, 42);
        }
    }

    static void Proses_raam(int lengte_VALUE) {
        if (lengte_VALUE < 14 || lengte_VALUE > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, uitsaai_VALUE = true;
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            if (입력틀[INDEX] != Netwerk_drywer.mobiel_adres[INDEX]) 자기 = false;
            if (입력틀[INDEX] != 255) uitsaai_VALUE = false;
        }
        if (!자기 && !uitsaai_VALUE) return;
        if (heelgetal_16(입력틀, 12) == 0x0806) { Proses_adres(lengte_VALUE); return; }
        if (heelgetal_16(입력틀, 12) != 0x0800) return;
        if (lengte_VALUE < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int Loopkop_lengte = (입력틀[14] & 15) * 4, 전체길이 = heelgetal_16(입력틀, 16);
        if (Loopkop_lengte < 20 || Loopkop_lengte > 60 || 전체길이 < Loopkop_lengte + 8 || 전체길이 > lengte_VALUE - 14
            || (heelgetal_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || heelgetal_32(입력틀, 30) != 내주소 || SUM_VALUE(입력틀, 14, Loopkop_lengte, 0) != 65535) { 폐기수++; return; }
        int Loop = 14 + Loopkop_lengte, data_lengte = heelgetal_16(입력틀, Loop + 4);
        if (data_lengte < 8 || data_lengte != 전체길이 - Loopkop_lengte || data_lengte > 1032) { 폐기수++; return; }
        int 출발 = heelgetal_32(입력틀, 26);
        if (heelgetal_16(입력틀, Loop + 6) != 0 && SUM_VALUE(입력틀, Loop, data_lengte, 가상머리합(출발, 내주소, data_lengte)) != 65535) {
            폐기수++; return;
        }
        int bestemming_VALUE = heelgetal_16(입력틀, Loop + 2);
        for (int gleuf_inskrywing = 0; gleuf_inskrywing < 4; gleuf_inskrywing++) if (접속번호들[gleuf_inskrywing] != 0 && 접속번호들[gleuf_inskrywing] == bestemming_VALUE) {
            if (RECEIVED_lengte[gleuf_inskrywing] >= 0) { 폐기수++; return; }
            RECEIVED_lengte[gleuf_inskrywing] = data_lengte - 8; RECEIVED_adres[gleuf_inskrywing] = 출발; 받은접속번호[gleuf_inskrywing] = heelgetal_16(입력틀, Loop);
            for (int INDEX = 0; INDEX < data_lengte - 8; INDEX++) RECEIVED_data[gleuf_inskrywing * 1024 + INDEX] = 입력틀[Loop + 8 + INDEX];
            return;
        }
    }

    static void verifieer() {
        for (int INDEX = 0; INDEX < 16; INDEX++) {
            int lengte_VALUE = Netwerk_drywer.받기(입력틀);
            if (lengte_VALUE == 0) return;
            Proses_raam(lengte_VALUE);
        }
    }
    static int FIND_adres(int adres) {
        if (adres == 0 || adres == -1 || (adres >>> 28) >= 14 || (adres >>> 24) == 127 || adres == 내주소) return -101;
        int Volgende_item = (adres & Netwerk_masker) == (내주소 & Netwerk_masker) ? adres : deurgang_VALUE;
        if (Volgende_item == 찾은주소) return 0;
        찾을주소 = Volgende_item;
        int Loop = mobiel_VALUE.밀리초(), 다음요청 = Loop;
        while (mobiel_VALUE.밀리초() - Loop < 1000) {
            if (mobiel_VALUE.밀리초() - 다음요청 >= 0) { 주소요청(Volgende_item); 다음요청 += 300; }
            verifieer();
            if (찾은주소 == Volgende_item) return 0;
            mobiel_VALUE.잠시양보();
        }
        return -110;
    }
    static int e_pos(int handvatsel_VALUE, int adres, int 접속번호, int[] data, int lengte_VALUE) {
        int gleuf_inskrywing = INDEX(handvatsel_VALUE);
        if (gleuf_inskrywing < 0) return -9;
        if (Netwerk_drywer.입출력기준주소 == 0) return -19;
        if (접속번호 < 1 || 접속번호 > 65535 || lengte_VALUE < 0 || lengte_VALUE > 1024) return -22;
        int maatreël = FIND_adres(adres);
        if (maatreël < 0) return maatreël;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + lengte_VALUE);
        넣기16(출력틀, 18, waarde_VALUE++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, adres);
        넣기16(출력틀, 24, ~SUM_VALUE(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[gleuf_inskrywing]); 넣기16(출력틀, 36, 접속번호);
        넣기16(출력틀, 38, lengte_VALUE + 8); 넣기16(출력틀, 40, 0);
        for (int INDEX = 0; INDEX < lengte_VALUE; INDEX++) 출력틀[42 + INDEX] = data[INDEX] & 255;
        int 검사합 = (~SUM_VALUE(출력틀, 34, lengte_VALUE + 8, 가상머리합(내주소, adres, lengte_VALUE + 8))) & 65535;
        넣기16(출력틀, 40, 검사합 == 0 ? 65535 : 검사합);
        maatreël = Netwerk_drywer.e_pos(출력틀, lengte_VALUE + 42);
        return maatreël < 0 ? maatreël : lengte_VALUE;
    }
    static int 받기(int handvatsel_VALUE, int[] data, int 용량, int 제한) {
        int gleuf_inskrywing = INDEX(handvatsel_VALUE);
        if (gleuf_inskrywing < 0) return -9;
        int Loop = mobiel_VALUE.밀리초();
        while (true) {
            verifieer();
            int lengte_VALUE = RECEIVED_lengte[gleuf_inskrywing];
            if (lengte_VALUE >= 0) {
                RECEIVED_lengte[gleuf_inskrywing] = -1;
                if (lengte_VALUE > 용량) return -90;
                for (int INDEX = 0; INDEX < lengte_VALUE; INDEX++) data[INDEX] = RECEIVED_data[gleuf_inskrywing * 1024 + INDEX];
                return lengte_VALUE;
            }
            if (제한 == 0) return -11;
            if (mobiel_VALUE.밀리초() - Loop >= 제한) return -110;
            mobiel_VALUE.잠시양보();
        }
    }
    static void stand_VALUE() {
        SMS_Terminaal.Skryf(Netwerk_drywer.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Terminaal.Skryf("TX: "); SMS_Terminaal.수쓰기(Netwerk_drywer.송신수);
        SMS_Terminaal.Skryf(" RX: "); SMS_Terminaal.수쓰기(Netwerk_drywer.수신수);
        SMS_Terminaal.Skryf(" DROP: "); SMS_Terminaal.수쓰기(폐기수);
        SMS_Terminaal.Skryf("\n");
    }
}
