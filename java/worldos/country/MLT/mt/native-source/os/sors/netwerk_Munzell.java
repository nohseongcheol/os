// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** statiku_VALUE IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class netwerk_Munzell {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int netwerk_maskra = 0xffffff00; /* ip.conf:NETMASK */
    static final int gateway_VALUE = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], RECEIVED_tul = new int[4], RECEIVED_ADDRESS = new int[4], 받은접속번호 = new int[4];
    static int[] RECEIVED_data = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, identifikatur_VALUE = 0, 폐기수 = 0;

    static int numru_sħiħ_16(int[] frejm_INDEX, int pożizzjoni) { return (frejm_INDEX[pożizzjoni] << 8) | frejm_INDEX[pożizzjoni + 1]; }
    static int numru_sħiħ_32(int[] frejm_INDEX, int pożizzjoni) { return (numru_sħiħ_16(frejm_INDEX, pożizzjoni) << 16) | numru_sħiħ_16(frejm_INDEX, pożizzjoni + 2); }
    static void 넣기16(int[] frejm_INDEX, int pożizzjoni, int VALUE) { frejm_INDEX[pożizzjoni] = (VALUE >>> 8) & 255; frejm_INDEX[pożizzjoni + 1] = VALUE & 255; }
    static void 넣기32(int[] frejm_INDEX, int pożizzjoni, int VALUE) { 넣기16(frejm_INDEX, pożizzjoni, VALUE >>> 16); 넣기16(frejm_INDEX, pożizzjoni + 2, VALUE); }
    static int SUM_VALUE(int[] frejm_INDEX, int serje, int tul_VALUE, int VALUE) {
        for (int INDEX = 0; INDEX < tul_VALUE; INDEX += 2)
            VALUE += (frejm_INDEX[serje + INDEX] << 8) | (INDEX + 1 < tul_VALUE ? frejm_INDEX[serje + INDEX + 1] : 0);
        while ((VALUE >>> 16) != 0) VALUE = (VALUE & 65535) + (VALUE >>> 16);
        return VALUE;
    }
    static int 가상머리합(int 출발, int 도착, int tul_VALUE) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + tul_VALUE;
    }

    static void CLEAN_Proċess() {
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            접속번호들[INDEX] = 0; RECEIVED_tul[INDEX] = -1; RECEIVED_ADDRESS[INDEX] = 0; 받은접속번호[INDEX] = 0;
        }
        for (int INDEX = 0; INDEX < 64; INDEX++) if (netwerk_drajver.받기(입력틀) == 0) break;
    }
    static int INDEX(int handle_VALUE) { return handle_VALUE >= 3 && handle_VALUE < 7 && 접속번호들[handle_VALUE - 3] != 0 ? handle_VALUE - 3 : -1; }
    static int fetaħ(int 접속번호) {
        if (netwerk_drajver.입출력기준주소 == 0) return -19;
        if (접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 != 0) for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == 접속번호) return -98;
        for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == 0) {
            if (접속번호 == 0) {
                접속번호 = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int 앞 = 0; 앞 < 4; 앞++) if (접속번호들[앞] == 접속번호) 겹침 = true;
                    if (겹침) 접속번호++;
                }
            }
            접속번호들[INDEX] = 접속번호; RECEIVED_tul[INDEX] = -1;
            return INDEX + 3;
        }
        return -24;
    }
    static int agħlaq(int handle_VALUE) {
        int slott_entrata = INDEX(handle_VALUE);
        if (slott_entrata < 0) return -9;
        접속번호들[slott_entrata] = 0; RECEIVED_tul[slott_entrata] = -1;
        return 0;
    }
    static int peer_ADDRESS(int handle_VALUE) { int slott_entrata = INDEX(handle_VALUE); return slott_entrata < 0 ? -9 : RECEIVED_ADDRESS[slott_entrata]; }
    static int 상대접속번호(int handle_VALUE) { int slott_entrata = INDEX(handle_VALUE); return slott_entrata < 0 ? -9 : 받은접속번호[slott_entrata]; }

    static void 바깥머리(int 종류, boolean xandira_VALUE) {
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[INDEX] = xandira_VALUE ? 255 : 찾은장치[INDEX];
            출력틀[6 + INDEX] = netwerk_drajver.mowbajl_ADDRESS[INDEX];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void 주소요청(int destinazzjoni_VALUE) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[22 + INDEX] = netwerk_drajver.mowbajl_ADDRESS[INDEX]; 출력틀[32 + INDEX] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, destinazzjoni_VALUE);
        netwerk_drajver.bagħat(출력틀, 42);
    }
    static void Proċess_ADDRESS(int tul_VALUE) {
        if (tul_VALUE < 42 || numru_sħiħ_16(입력틀, 14) != 1 || numru_sħiħ_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || numru_sħiħ_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = numru_sħiħ_16(입력틀, 20), peer_VALUE = numru_sħiħ_32(입력틀, 28);
        if (종류 == 2 && peer_VALUE == 찾을주소) {
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                if (입력틀[6 + INDEX] != 입력틀[22 + INDEX] || 입력틀[32 + INDEX] != netwerk_drajver.mowbajl_ADDRESS[INDEX]) return;
            }
            for (int INDEX = 0; INDEX < 6; INDEX++) 찾은장치[INDEX] = 입력틀[22 + INDEX];
            찾은주소 = peer_VALUE;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                출력틀[INDEX] = 입력틀[22 + INDEX]; 출력틀[32 + INDEX] = 입력틀[22 + INDEX];
                출력틀[22 + INDEX] = netwerk_drajver.mowbajl_ADDRESS[INDEX];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, peer_VALUE);
            netwerk_drajver.bagħat(출력틀, 42);
        }
    }

    static void Proċess_frejm(int tul_VALUE) {
        if (tul_VALUE < 14 || tul_VALUE > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, xandira_VALUE = true;
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            if (입력틀[INDEX] != netwerk_drajver.mowbajl_ADDRESS[INDEX]) 자기 = false;
            if (입력틀[INDEX] != 255) xandira_VALUE = false;
        }
        if (!자기 && !xandira_VALUE) return;
        if (numru_sħiħ_16(입력틀, 12) == 0x0806) { Proċess_ADDRESS(tul_VALUE); return; }
        if (numru_sħiħ_16(입력틀, 12) != 0x0800) return;
        if (tul_VALUE < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int Intestazzjoni_tul = (입력틀[14] & 15) * 4, 전체길이 = numru_sħiħ_16(입력틀, 16);
        if (Intestazzjoni_tul < 20 || Intestazzjoni_tul > 60 || 전체길이 < Intestazzjoni_tul + 8 || 전체길이 > tul_VALUE - 14
            || (numru_sħiħ_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || numru_sħiħ_32(입력틀, 30) != 내주소 || SUM_VALUE(입력틀, 14, Intestazzjoni_tul, 0) != 65535) { 폐기수++; return; }
        int serje = 14 + Intestazzjoni_tul, data_tul = numru_sħiħ_16(입력틀, serje + 4);
        if (data_tul < 8 || data_tul != 전체길이 - Intestazzjoni_tul || data_tul > 1032) { 폐기수++; return; }
        int 출발 = numru_sħiħ_32(입력틀, 26);
        if (numru_sħiħ_16(입력틀, serje + 6) != 0 && SUM_VALUE(입력틀, serje, data_tul, 가상머리합(출발, 내주소, data_tul)) != 65535) {
            폐기수++; return;
        }
        int destinazzjoni_VALUE = numru_sħiħ_16(입력틀, serje + 2);
        for (int slott_entrata = 0; slott_entrata < 4; slott_entrata++) if (접속번호들[slott_entrata] != 0 && 접속번호들[slott_entrata] == destinazzjoni_VALUE) {
            if (RECEIVED_tul[slott_entrata] >= 0) { 폐기수++; return; }
            RECEIVED_tul[slott_entrata] = data_tul - 8; RECEIVED_ADDRESS[slott_entrata] = 출발; 받은접속번호[slott_entrata] = numru_sħiħ_16(입력틀, serje);
            for (int INDEX = 0; INDEX < data_tul - 8; INDEX++) RECEIVED_data[slott_entrata * 1024 + INDEX] = 입력틀[serje + 8 + INDEX];
            return;
        }
    }

    static void vverifika() {
        for (int INDEX = 0; INDEX < 16; INDEX++) {
            int tul_VALUE = netwerk_drajver.받기(입력틀);
            if (tul_VALUE == 0) return;
            Proċess_frejm(tul_VALUE);
        }
    }
    static int sab_ADDRESS(int ADDRESS) {
        if (ADDRESS == 0 || ADDRESS == -1 || (ADDRESS >>> 28) >= 14 || (ADDRESS >>> 24) == 127 || ADDRESS == 내주소) return -101;
        int Li_Jmiss_element = (ADDRESS & netwerk_maskra) == (내주소 & netwerk_maskra) ? ADDRESS : gateway_VALUE;
        if (Li_Jmiss_element == 찾은주소) return 0;
        찾을주소 = Li_Jmiss_element;
        int serje = mowbajl_VALUE.밀리초(), 다음요청 = serje;
        while (mowbajl_VALUE.밀리초() - serje < 1000) {
            if (mowbajl_VALUE.밀리초() - 다음요청 >= 0) { 주소요청(Li_Jmiss_element); 다음요청 += 300; }
            vverifika();
            if (찾은주소 == Li_Jmiss_element) return 0;
            mowbajl_VALUE.잠시양보();
        }
        return -110;
    }
    static int bagħat(int handle_VALUE, int ADDRESS, int 접속번호, int[] data, int tul_VALUE) {
        int slott_entrata = INDEX(handle_VALUE);
        if (slott_entrata < 0) return -9;
        if (netwerk_drajver.입출력기준주소 == 0) return -19;
        if (접속번호 < 1 || 접속번호 > 65535 || tul_VALUE < 0 || tul_VALUE > 1024) return -22;
        int miżura = sab_ADDRESS(ADDRESS);
        if (miżura < 0) return miżura;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + tul_VALUE);
        넣기16(출력틀, 18, identifikatur_VALUE++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, ADDRESS);
        넣기16(출력틀, 24, ~SUM_VALUE(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[slott_entrata]); 넣기16(출력틀, 36, 접속번호);
        넣기16(출력틀, 38, tul_VALUE + 8); 넣기16(출력틀, 40, 0);
        for (int INDEX = 0; INDEX < tul_VALUE; INDEX++) 출력틀[42 + INDEX] = data[INDEX] & 255;
        int 검사합 = (~SUM_VALUE(출력틀, 34, tul_VALUE + 8, 가상머리합(내주소, ADDRESS, tul_VALUE + 8))) & 65535;
        넣기16(출력틀, 40, 검사합 == 0 ? 65535 : 검사합);
        miżura = netwerk_drajver.bagħat(출력틀, tul_VALUE + 42);
        return miżura < 0 ? miżura : tul_VALUE;
    }
    static int 받기(int handle_VALUE, int[] data, int 용량, int 제한) {
        int slott_entrata = INDEX(handle_VALUE);
        if (slott_entrata < 0) return -9;
        int serje = mowbajl_VALUE.밀리초();
        while (true) {
            vverifika();
            int tul_VALUE = RECEIVED_tul[slott_entrata];
            if (tul_VALUE >= 0) {
                RECEIVED_tul[slott_entrata] = -1;
                if (tul_VALUE > 용량) return -90;
                for (int INDEX = 0; INDEX < tul_VALUE; INDEX++) data[INDEX] = RECEIVED_data[slott_entrata * 1024 + INDEX];
                return tul_VALUE;
            }
            if (제한 == 0) return -11;
            if (mowbajl_VALUE.밀리초() - serje >= 제한) return -110;
            mowbajl_VALUE.잠시양보();
        }
    }
    static void stat_VALUE() {
        SMS_Terminal.kiteb(netwerk_drajver.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Terminal.kiteb("TX: "); SMS_Terminal.수쓰기(netwerk_drajver.송신수);
        SMS_Terminal.kiteb(" RX: "); SMS_Terminal.수쓰기(netwerk_drajver.수신수);
        SMS_Terminal.kiteb(" DROP: "); SMS_Terminal.수쓰기(폐기수);
        SMS_Terminal.kiteb("\n");
    }
}
