// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** statig_VALUE IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class Rhwydwaith_pentwr {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int Rhwydwaith_masgio = 0xffffff00; /* ip.conf:NETMASK */
    static final int adwy_VALUE = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], RECEIVED_hyd = new int[4], RECEIVED_ADDRESS = new int[4], RECEIVED_rhif_porth = new int[4];
    static int[] RECEIVED_data = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, dynodwr_VALUE = 0, 폐기수 = 0;

    static int cyfanrif_16(int[] ffrâm_INDEX, int safle) { return (ffrâm_INDEX[safle] << 8) | ffrâm_INDEX[safle + 1]; }
    static int cyfanrif_32(int[] ffrâm_INDEX, int safle) { return (cyfanrif_16(ffrâm_INDEX, safle) << 16) | cyfanrif_16(ffrâm_INDEX, safle + 2); }
    static void 넣기16(int[] ffrâm_INDEX, int safle, int VALUE) { ffrâm_INDEX[safle] = (VALUE >>> 8) & 255; ffrâm_INDEX[safle + 1] = VALUE & 255; }
    static void 넣기32(int[] ffrâm_INDEX, int safle, int VALUE) { 넣기16(ffrâm_INDEX, safle, VALUE >>> 16); 넣기16(ffrâm_INDEX, safle + 2, VALUE); }
    static int SUM_VALUE(int[] ffrâm_INDEX, int Gweithredu_2, int hyd_VALUE, int VALUE) {
        for (int INDEX = 0; INDEX < hyd_VALUE; INDEX += 2)
            VALUE += (ffrâm_INDEX[Gweithredu_2 + INDEX] << 8) | (INDEX + 1 < hyd_VALUE ? ffrâm_INDEX[Gweithredu_2 + INDEX + 1] : 0);
        while ((VALUE >>> 16) != 0) VALUE = (VALUE & 65535) + (VALUE >>> 16);
        return VALUE;
    }
    static int 가상머리합(int 출발, int 도착, int hyd_VALUE) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + hyd_VALUE;
    }

    static void Glân_Proses() {
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            접속번호들[INDEX] = 0; RECEIVED_hyd[INDEX] = -1; RECEIVED_ADDRESS[INDEX] = 0; RECEIVED_rhif_porth[INDEX] = 0;
        }
        for (int INDEX = 0; INDEX < 64; INDEX++) if (Rhwydwaith_gyrrwr.받기(입력틀) == 0) break;
    }
    static int INDEX(int dolen_VALUE) { return dolen_VALUE >= 3 && dolen_VALUE < 7 && 접속번호들[dolen_VALUE - 3] != 0 ? dolen_VALUE - 3 : -1; }
    static int Agor(int rhif_porth) {
        if (Rhwydwaith_gyrrwr.입출력기준주소 == 0) return -19;
        if (rhif_porth < 0 || rhif_porth > 65535) return -22;
        if (rhif_porth != 0) for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == rhif_porth) return -98;
        for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == 0) {
            if (rhif_porth == 0) {
                rhif_porth = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int 앞 = 0; 앞 < 4; 앞++) if (접속번호들[앞] == rhif_porth) 겹침 = true;
                    if (겹침) rhif_porth++;
                }
            }
            접속번호들[INDEX] = rhif_porth; RECEIVED_hyd[INDEX] = -1;
            return INDEX + 3;
        }
        return -24;
    }
    static int Cau(int dolen_VALUE) {
        int slot_cofnod = INDEX(dolen_VALUE);
        if (slot_cofnod < 0) return -9;
        접속번호들[slot_cofnod] = 0; RECEIVED_hyd[slot_cofnod] = -1;
        return 0;
    }
    static int cymar_ADDRESS(int dolen_VALUE) { int slot_cofnod = INDEX(dolen_VALUE); return slot_cofnod < 0 ? -9 : RECEIVED_ADDRESS[slot_cofnod]; }
    static int cymar_rhif_porth(int dolen_VALUE) { int slot_cofnod = INDEX(dolen_VALUE); return slot_cofnod < 0 ? -9 : RECEIVED_rhif_porth[slot_cofnod]; }

    static void 바깥머리(int 종류, boolean darlledu_VALUE) {
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[INDEX] = darlledu_VALUE ? 255 : 찾은장치[INDEX];
            출력틀[6 + INDEX] = Rhwydwaith_gyrrwr.dyfais_ADDRESS[INDEX];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void cais_HTTP_ADDRESS(int cyrchfan_VALUE) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[22 + INDEX] = Rhwydwaith_gyrrwr.dyfais_ADDRESS[INDEX]; 출력틀[32 + INDEX] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, cyrchfan_VALUE);
        Rhwydwaith_gyrrwr.anfon(출력틀, 42);
    }
    static void Proses_ADDRESS(int hyd_VALUE) {
        if (hyd_VALUE < 42 || cyfanrif_16(입력틀, 14) != 1 || cyfanrif_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || cyfanrif_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = cyfanrif_16(입력틀, 20), cymar_VALUE = cyfanrif_32(입력틀, 28);
        if (종류 == 2 && cymar_VALUE == 찾을주소) {
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                if (입력틀[6 + INDEX] != 입력틀[22 + INDEX] || 입력틀[32 + INDEX] != Rhwydwaith_gyrrwr.dyfais_ADDRESS[INDEX]) return;
            }
            for (int INDEX = 0; INDEX < 6; INDEX++) 찾은장치[INDEX] = 입력틀[22 + INDEX];
            찾은주소 = cymar_VALUE;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                출력틀[INDEX] = 입력틀[22 + INDEX]; 출력틀[32 + INDEX] = 입력틀[22 + INDEX];
                출력틀[22 + INDEX] = Rhwydwaith_gyrrwr.dyfais_ADDRESS[INDEX];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, cymar_VALUE);
            Rhwydwaith_gyrrwr.anfon(출력틀, 42);
        }
    }

    static void Proses_ffrâm(int hyd_VALUE) {
        if (hyd_VALUE < 14 || hyd_VALUE > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, darlledu_VALUE = true;
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            if (입력틀[INDEX] != Rhwydwaith_gyrrwr.dyfais_ADDRESS[INDEX]) 자기 = false;
            if (입력틀[INDEX] != 255) darlledu_VALUE = false;
        }
        if (!자기 && !darlledu_VALUE) return;
        if (cyfanrif_16(입력틀, 12) == 0x0806) { Proses_ADDRESS(hyd_VALUE); return; }
        if (cyfanrif_16(입력틀, 12) != 0x0800) return;
        if (hyd_VALUE < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int Pennyn_hyd = (입력틀[14] & 15) * 4, 전체길이 = cyfanrif_16(입력틀, 16);
        if (Pennyn_hyd < 20 || Pennyn_hyd > 60 || 전체길이 < Pennyn_hyd + 8 || 전체길이 > hyd_VALUE - 14
            || (cyfanrif_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || cyfanrif_32(입력틀, 30) != 내주소 || SUM_VALUE(입력틀, 14, Pennyn_hyd, 0) != 65535) { 폐기수++; return; }
        int Gweithredu_2 = 14 + Pennyn_hyd, data_hyd = cyfanrif_16(입력틀, Gweithredu_2 + 4);
        if (data_hyd < 8 || data_hyd != 전체길이 - Pennyn_hyd || data_hyd > 1032) { 폐기수++; return; }
        int 출발 = cyfanrif_32(입력틀, 26);
        if (cyfanrif_16(입력틀, Gweithredu_2 + 6) != 0 && SUM_VALUE(입력틀, Gweithredu_2, data_hyd, 가상머리합(출발, 내주소, data_hyd)) != 65535) {
            폐기수++; return;
        }
        int cyrchfan_VALUE = cyfanrif_16(입력틀, Gweithredu_2 + 2);
        for (int slot_cofnod = 0; slot_cofnod < 4; slot_cofnod++) if (접속번호들[slot_cofnod] != 0 && 접속번호들[slot_cofnod] == cyrchfan_VALUE) {
            if (RECEIVED_hyd[slot_cofnod] >= 0) { 폐기수++; return; }
            RECEIVED_hyd[slot_cofnod] = data_hyd - 8; RECEIVED_ADDRESS[slot_cofnod] = 출발; RECEIVED_rhif_porth[slot_cofnod] = cyfanrif_16(입력틀, Gweithredu_2);
            for (int INDEX = 0; INDEX < data_hyd - 8; INDEX++) RECEIVED_data[slot_cofnod * 1024 + INDEX] = 입력틀[Gweithredu_2 + 8 + INDEX];
            return;
        }
    }

    static void dilysu() {
        for (int INDEX = 0; INDEX < 16; INDEX++) {
            int hyd_VALUE = Rhwydwaith_gyrrwr.받기(입력틀);
            if (hyd_VALUE == 0) return;
            Proses_ffrâm(hyd_VALUE);
        }
    }
    static int FIND_ADDRESS(int ADDRESS) {
        if (ADDRESS == 0 || ADDRESS == -1 || (ADDRESS >>> 28) >= 14 || (ADDRESS >>> 24) == 127 || ADDRESS == 내주소) return -101;
        int Nesaf_eitem = (ADDRESS & Rhwydwaith_masgio) == (내주소 & Rhwydwaith_masgio) ? ADDRESS : adwy_VALUE;
        if (Nesaf_eitem == 찾은주소) return 0;
        찾을주소 = Nesaf_eitem;
        int Gweithredu_2 = dyfais_VALUE.밀리초(), Nesaf_cais_HTTP = Gweithredu_2;
        while (dyfais_VALUE.밀리초() - Gweithredu_2 < 1000) {
            if (dyfais_VALUE.밀리초() - Nesaf_cais_HTTP >= 0) { cais_HTTP_ADDRESS(Nesaf_eitem); Nesaf_cais_HTTP += 300; }
            dilysu();
            if (찾은주소 == Nesaf_eitem) return 0;
            dyfais_VALUE.잠시양보();
        }
        return -110;
    }
    static int anfon(int dolen_VALUE, int ADDRESS, int rhif_porth, int[] data, int hyd_VALUE) {
        int slot_cofnod = INDEX(dolen_VALUE);
        if (slot_cofnod < 0) return -9;
        if (Rhwydwaith_gyrrwr.입출력기준주소 == 0) return -19;
        if (rhif_porth < 1 || rhif_porth > 65535 || hyd_VALUE < 0 || hyd_VALUE > 1024) return -22;
        int mesur = FIND_ADDRESS(ADDRESS);
        if (mesur < 0) return mesur;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + hyd_VALUE);
        넣기16(출력틀, 18, dynodwr_VALUE++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, ADDRESS);
        넣기16(출력틀, 24, ~SUM_VALUE(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[slot_cofnod]); 넣기16(출력틀, 36, rhif_porth);
        넣기16(출력틀, 38, hyd_VALUE + 8); 넣기16(출력틀, 40, 0);
        for (int INDEX = 0; INDEX < hyd_VALUE; INDEX++) 출력틀[42 + INDEX] = data[INDEX] & 255;
        int prawfswm = (~SUM_VALUE(출력틀, 34, hyd_VALUE + 8, 가상머리합(내주소, ADDRESS, hyd_VALUE + 8))) & 65535;
        넣기16(출력틀, 40, prawfswm == 0 ? 65535 : prawfswm);
        mesur = Rhwydwaith_gyrrwr.anfon(출력틀, hyd_VALUE + 42);
        return mesur < 0 ? mesur : hyd_VALUE;
    }
    static int 받기(int dolen_VALUE, int[] data, int 용량, int 제한) {
        int slot_cofnod = INDEX(dolen_VALUE);
        if (slot_cofnod < 0) return -9;
        int Gweithredu_2 = dyfais_VALUE.밀리초();
        while (true) {
            dilysu();
            int hyd_VALUE = RECEIVED_hyd[slot_cofnod];
            if (hyd_VALUE >= 0) {
                RECEIVED_hyd[slot_cofnod] = -1;
                if (hyd_VALUE > 용량) return -90;
                for (int INDEX = 0; INDEX < hyd_VALUE; INDEX++) data[INDEX] = RECEIVED_data[slot_cofnod * 1024 + INDEX];
                return hyd_VALUE;
            }
            if (제한 == 0) return -11;
            if (dyfais_VALUE.밀리초() - Gweithredu_2 >= 제한) return -110;
            dyfais_VALUE.잠시양보();
        }
    }
    static void cyflwr_VALUE() {
        SMS_Terfynell.Ysgrifennu(Rhwydwaith_gyrrwr.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Terfynell.Ysgrifennu("TX: "); SMS_Terfynell.수쓰기(Rhwydwaith_gyrrwr.송신수);
        SMS_Terfynell.Ysgrifennu(" RX: "); SMS_Terfynell.수쓰기(Rhwydwaith_gyrrwr.수신수);
        SMS_Terfynell.Ysgrifennu(" DROP: "); SMS_Terfynell.수쓰기(폐기수);
        SMS_Terfynell.Ysgrifennu("\n");
    }
}
