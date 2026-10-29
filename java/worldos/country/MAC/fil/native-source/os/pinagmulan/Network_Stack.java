// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** hindi_nababago_VALUE IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class Network_Stack {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int Network_mask = 0xffffff00; /* ip.conf:NETMASK */
    static final int entrada_VALUE = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], RECEIVED_haba = new int[4], RECEIVED_email = new int[4], RECEIVED_numero_ng_port = new int[4];
    static int[] RECEIVED_data = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, tagakilala_VALUE = 0, 폐기수 = 0;

    static int integer_buong_numero_16(int[] frame_INDEX, int posisyon) { return (frame_INDEX[posisyon] << 8) | frame_INDEX[posisyon + 1]; }
    static int integer_buong_numero_32(int[] frame_INDEX, int posisyon) { return (integer_buong_numero_16(frame_INDEX, posisyon) << 16) | integer_buong_numero_16(frame_INDEX, posisyon + 2); }
    static void 넣기16(int[] frame_INDEX, int posisyon, int VALUE) { frame_INDEX[posisyon] = (VALUE >>> 8) & 255; frame_INDEX[posisyon + 1] = VALUE & 255; }
    static void 넣기32(int[] frame_INDEX, int posisyon, int VALUE) { 넣기16(frame_INDEX, posisyon, VALUE >>> 16); 넣기16(frame_INDEX, posisyon + 2, VALUE); }
    static int SUM_VALUE(int[] frame_INDEX, int run, int haba_VALUE, int VALUE) {
        for (int INDEX = 0; INDEX < haba_VALUE; INDEX += 2)
            VALUE += (frame_INDEX[run + INDEX] << 8) | (INDEX + 1 < haba_VALUE ? frame_INDEX[run + INDEX + 1] : 0);
        while ((VALUE >>> 16) != 0) VALUE = (VALUE & 65535) + (VALUE >>> 16);
        return VALUE;
    }
    static int 가상머리합(int 출발, int 도착, int haba_VALUE) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + haba_VALUE;
    }

    static void CLEAN_Proseso() {
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            접속번호들[INDEX] = 0; RECEIVED_haba[INDEX] = -1; RECEIVED_email[INDEX] = 0; RECEIVED_numero_ng_port[INDEX] = 0;
        }
        for (int INDEX = 0; INDEX < 64; INDEX++) if (Network_driver.받기(입력틀) == 0) break;
    }
    static int INDEX(int hawakán_VALUE) { return hawakán_VALUE >= 3 && hawakán_VALUE < 7 && 접속번호들[hawakán_VALUE - 3] != 0 ? hawakán_VALUE - 3 : -1; }
    static int buksan(int numero_ng_port) {
        if (Network_driver.입출력기준주소 == 0) return -19;
        if (numero_ng_port < 0 || numero_ng_port > 65535) return -22;
        if (numero_ng_port != 0) for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == numero_ng_port) return -98;
        for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == 0) {
            if (numero_ng_port == 0) {
                numero_ng_port = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int nasa_harap_VALUE = 0; nasa_harap_VALUE < 4; nasa_harap_VALUE++) if (접속번호들[nasa_harap_VALUE] == numero_ng_port) 겹침 = true;
                    if (겹침) numero_ng_port++;
                }
            }
            접속번호들[INDEX] = numero_ng_port; RECEIVED_haba[INDEX] = -1;
            return INDEX + 3;
        }
        return -24;
    }
    static int isara(int hawakán_VALUE) {
        int espasyo_pagpasok = INDEX(hawakán_VALUE);
        if (espasyo_pagpasok < 0) return -9;
        접속번호들[espasyo_pagpasok] = 0; RECEIVED_haba[espasyo_pagpasok] = -1;
        return 0;
    }
    static int peer_email(int hawakán_VALUE) { int espasyo_pagpasok = INDEX(hawakán_VALUE); return espasyo_pagpasok < 0 ? -9 : RECEIVED_email[espasyo_pagpasok]; }
    static int peer_numero_ng_port(int hawakán_VALUE) { int espasyo_pagpasok = INDEX(hawakán_VALUE); return espasyo_pagpasok < 0 ? -9 : RECEIVED_numero_ng_port[espasyo_pagpasok]; }

    static void 바깥머리(int 종류, boolean broadcast_VALUE) {
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[INDEX] = broadcast_VALUE ? 255 : 찾은장치[INDEX];
            출력틀[6 + INDEX] = Network_driver.device_email[INDEX];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void 주소요청(int patutunguhan_VALUE) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[22 + INDEX] = Network_driver.device_email[INDEX]; 출력틀[32 + INDEX] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, patutunguhan_VALUE);
        Network_driver.i_email(출력틀, 42);
    }
    static void Proseso_email(int haba_VALUE) {
        if (haba_VALUE < 42 || integer_buong_numero_16(입력틀, 14) != 1 || integer_buong_numero_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || integer_buong_numero_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = integer_buong_numero_16(입력틀, 20), peer_VALUE = integer_buong_numero_32(입력틀, 28);
        if (종류 == 2 && peer_VALUE == 찾을주소) {
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                if (입력틀[6 + INDEX] != 입력틀[22 + INDEX] || 입력틀[32 + INDEX] != Network_driver.device_email[INDEX]) return;
            }
            for (int INDEX = 0; INDEX < 6; INDEX++) 찾은장치[INDEX] = 입력틀[22 + INDEX];
            찾은주소 = peer_VALUE;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                출력틀[INDEX] = 입력틀[22 + INDEX]; 출력틀[32 + INDEX] = 입력틀[22 + INDEX];
                출력틀[22 + INDEX] = Network_driver.device_email[INDEX];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, peer_VALUE);
            Network_driver.i_email(출력틀, 42);
        }
    }

    static void Proseso_frame(int haba_VALUE) {
        if (haba_VALUE < 14 || haba_VALUE > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, broadcast_VALUE = true;
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            if (입력틀[INDEX] != Network_driver.device_email[INDEX]) 자기 = false;
            if (입력틀[INDEX] != 255) broadcast_VALUE = false;
        }
        if (!자기 && !broadcast_VALUE) return;
        if (integer_buong_numero_16(입력틀, 12) == 0x0806) { Proseso_email(haba_VALUE); return; }
        if (integer_buong_numero_16(입력틀, 12) != 0x0800) return;
        if (haba_VALUE < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int Header_haba = (입력틀[14] & 15) * 4, 전체길이 = integer_buong_numero_16(입력틀, 16);
        if (Header_haba < 20 || Header_haba > 60 || 전체길이 < Header_haba + 8 || 전체길이 > haba_VALUE - 14
            || (integer_buong_numero_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || integer_buong_numero_32(입력틀, 30) != 내주소 || SUM_VALUE(입력틀, 14, Header_haba, 0) != 65535) { 폐기수++; return; }
        int run = 14 + Header_haba, data_haba = integer_buong_numero_16(입력틀, run + 4);
        if (data_haba < 8 || data_haba != 전체길이 - Header_haba || data_haba > 1032) { 폐기수++; return; }
        int 출발 = integer_buong_numero_32(입력틀, 26);
        if (integer_buong_numero_16(입력틀, run + 6) != 0 && SUM_VALUE(입력틀, run, data_haba, 가상머리합(출발, 내주소, data_haba)) != 65535) {
            폐기수++; return;
        }
        int patutunguhan_VALUE = integer_buong_numero_16(입력틀, run + 2);
        for (int espasyo_pagpasok = 0; espasyo_pagpasok < 4; espasyo_pagpasok++) if (접속번호들[espasyo_pagpasok] != 0 && 접속번호들[espasyo_pagpasok] == patutunguhan_VALUE) {
            if (RECEIVED_haba[espasyo_pagpasok] >= 0) { 폐기수++; return; }
            RECEIVED_haba[espasyo_pagpasok] = data_haba - 8; RECEIVED_email[espasyo_pagpasok] = 출발; RECEIVED_numero_ng_port[espasyo_pagpasok] = integer_buong_numero_16(입력틀, run);
            for (int INDEX = 0; INDEX < data_haba - 8; INDEX++) RECEIVED_data[espasyo_pagpasok * 1024 + INDEX] = 입력틀[run + 8 + INDEX];
            return;
        }
    }

    static void tiyakin_kumpirmahin() {
        for (int INDEX = 0; INDEX < 16; INDEX++) {
            int haba_VALUE = Network_driver.받기(입력틀);
            if (haba_VALUE == 0) return;
            Proseso_frame(haba_VALUE);
        }
    }
    static int FIND_email(int email) {
        if (email == 0 || email == -1 || (email >>> 28) >= 14 || (email >>> 24) == 127 || email == 내주소) return -101;
        int Susunod_item = (email & Network_mask) == (내주소 & Network_mask) ? email : entrada_VALUE;
        if (Susunod_item == 찾은주소) return 0;
        찾을주소 = Susunod_item;
        int run = device_VALUE.밀리초(), 다음요청 = run;
        while (device_VALUE.밀리초() - run < 1000) {
            if (device_VALUE.밀리초() - 다음요청 >= 0) { 주소요청(Susunod_item); 다음요청 += 300; }
            tiyakin_kumpirmahin();
            if (찾은주소 == Susunod_item) return 0;
            device_VALUE.잠시양보();
        }
        return -110;
    }
    static int i_email(int hawakán_VALUE, int email, int numero_ng_port, int[] data, int haba_VALUE) {
        int espasyo_pagpasok = INDEX(hawakán_VALUE);
        if (espasyo_pagpasok < 0) return -9;
        if (Network_driver.입출력기준주소 == 0) return -19;
        if (numero_ng_port < 1 || numero_ng_port > 65535 || haba_VALUE < 0 || haba_VALUE > 1024) return -22;
        int sukat = FIND_email(email);
        if (sukat < 0) return sukat;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + haba_VALUE);
        넣기16(출력틀, 18, tagakilala_VALUE++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, email);
        넣기16(출력틀, 24, ~SUM_VALUE(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[espasyo_pagpasok]); 넣기16(출력틀, 36, numero_ng_port);
        넣기16(출력틀, 38, haba_VALUE + 8); 넣기16(출력틀, 40, 0);
        for (int INDEX = 0; INDEX < haba_VALUE; INDEX++) 출력틀[42 + INDEX] = data[INDEX] & 255;
        int checksum = (~SUM_VALUE(출력틀, 34, haba_VALUE + 8, 가상머리합(내주소, email, haba_VALUE + 8))) & 65535;
        넣기16(출력틀, 40, checksum == 0 ? 65535 : checksum);
        sukat = Network_driver.i_email(출력틀, haba_VALUE + 42);
        return sukat < 0 ? sukat : haba_VALUE;
    }
    static int 받기(int hawakán_VALUE, int[] data, int 용량, int 제한) {
        int espasyo_pagpasok = INDEX(hawakán_VALUE);
        if (espasyo_pagpasok < 0) return -9;
        int run = device_VALUE.밀리초();
        while (true) {
            tiyakin_kumpirmahin();
            int haba_VALUE = RECEIVED_haba[espasyo_pagpasok];
            if (haba_VALUE >= 0) {
                RECEIVED_haba[espasyo_pagpasok] = -1;
                if (haba_VALUE > 용량) return -90;
                for (int INDEX = 0; INDEX < haba_VALUE; INDEX++) data[INDEX] = RECEIVED_data[espasyo_pagpasok * 1024 + INDEX];
                return haba_VALUE;
            }
            if (제한 == 0) return -11;
            if (device_VALUE.밀리초() - run >= 제한) return -110;
            device_VALUE.잠시양보();
        }
    }
    static void katayuan_VALUE() {
        SMS_Terminal.sumulat(Network_driver.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Terminal.sumulat("TX: "); SMS_Terminal.수쓰기(Network_driver.송신수);
        SMS_Terminal.sumulat(" RX: "); SMS_Terminal.수쓰기(Network_driver.수신수);
        SMS_Terminal.sumulat(" DROP: "); SMS_Terminal.수쓰기(폐기수);
        SMS_Terminal.sumulat("\n");
    }
}
