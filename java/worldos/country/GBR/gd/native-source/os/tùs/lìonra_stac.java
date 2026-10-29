// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** stadaigeach_VALUE IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class lìonra_stac {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int 망경계 = 0xffffff00; /* ip.conf:NETMASK */
    static final int 관문 = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], RECEIVED_faid = new int[4], RECEIVED_ADDRESS = new int[4], 받은접속번호 = new int[4];
    static int[] RECEIVED_dàta = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, aithnichear_VALUE = 0, 폐기수 = 0;

    static int àireamh_shlàn_16(int[] frèam_INDEX, int suidhich) { return (frèam_INDEX[suidhich] << 8) | frèam_INDEX[suidhich + 1]; }
    static int àireamh_shlàn_32(int[] frèam_INDEX, int suidhich) { return (àireamh_shlàn_16(frèam_INDEX, suidhich) << 16) | àireamh_shlàn_16(frèam_INDEX, suidhich + 2); }
    static void 넣기16(int[] frèam_INDEX, int suidhich, int VALUE) { frèam_INDEX[suidhich] = (VALUE >>> 8) & 255; frèam_INDEX[suidhich + 1] = VALUE & 255; }
    static void 넣기32(int[] frèam_INDEX, int suidhich, int VALUE) { 넣기16(frèam_INDEX, suidhich, VALUE >>> 16); 넣기16(frèam_INDEX, suidhich + 2, VALUE); }
    static int SUM_VALUE(int[] frèam_INDEX, int ruith, int faid_VALUE, int VALUE) {
        for (int INDEX = 0; INDEX < faid_VALUE; INDEX += 2)
            VALUE += (frèam_INDEX[ruith + INDEX] << 8) | (INDEX + 1 < faid_VALUE ? frèam_INDEX[ruith + INDEX + 1] : 0);
        while ((VALUE >>> 16) != 0) VALUE = (VALUE & 65535) + (VALUE >>> 16);
        return VALUE;
    }
    static int 가상머리합(int 출발, int 도착, int faid_VALUE) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + faid_VALUE;
    }

    static void CLEAN_Pròiseas() {
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            접속번호들[INDEX] = 0; RECEIVED_faid[INDEX] = -1; RECEIVED_ADDRESS[INDEX] = 0; 받은접속번호[INDEX] = 0;
        }
        for (int INDEX = 0; INDEX < 64; INDEX++) if (lìonra_dràibhear.받기(입력틀) == 0) break;
    }
    static int INDEX(int làmhrachan_VALUE) { return làmhrachan_VALUE >= 3 && làmhrachan_VALUE < 7 && 접속번호들[làmhrachan_VALUE - 3] != 0 ? làmhrachan_VALUE - 3 : -1; }
    static int fosgail(int 접속번호) {
        if (lìonra_dràibhear.입출력기준주소 == 0) return -19;
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
            접속번호들[INDEX] = 접속번호; RECEIVED_faid[INDEX] = -1;
            return INDEX + 3;
        }
        return -24;
    }
    static int dùin(int làmhrachan_VALUE) {
        int slot_cur_a_steach = INDEX(làmhrachan_VALUE);
        if (slot_cur_a_steach < 0) return -9;
        접속번호들[slot_cur_a_steach] = 0; RECEIVED_faid[slot_cur_a_steach] = -1;
        return 0;
    }
    static int seise_ADDRESS(int làmhrachan_VALUE) { int slot_cur_a_steach = INDEX(làmhrachan_VALUE); return slot_cur_a_steach < 0 ? -9 : RECEIVED_ADDRESS[slot_cur_a_steach]; }
    static int 상대접속번호(int làmhrachan_VALUE) { int slot_cur_a_steach = INDEX(làmhrachan_VALUE); return slot_cur_a_steach < 0 ? -9 : 받은접속번호[slot_cur_a_steach]; }

    static void 바깥머리(int 종류, boolean craoladh_VALUE) {
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[INDEX] = craoladh_VALUE ? 255 : 찾은장치[INDEX];
            출력틀[6 + INDEX] = lìonra_dràibhear.uidheam_ADDRESS[INDEX];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void 주소요청(int ceann_uidhe_VALUE) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[22 + INDEX] = lìonra_dràibhear.uidheam_ADDRESS[INDEX]; 출력틀[32 + INDEX] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, ceann_uidhe_VALUE);
        lìonra_dràibhear.cuir(출력틀, 42);
    }
    static void Pròiseas_ADDRESS(int faid_VALUE) {
        if (faid_VALUE < 42 || àireamh_shlàn_16(입력틀, 14) != 1 || àireamh_shlàn_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || àireamh_shlàn_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = àireamh_shlàn_16(입력틀, 20), seise_VALUE = àireamh_shlàn_32(입력틀, 28);
        if (종류 == 2 && seise_VALUE == 찾을주소) {
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                if (입력틀[6 + INDEX] != 입력틀[22 + INDEX] || 입력틀[32 + INDEX] != lìonra_dràibhear.uidheam_ADDRESS[INDEX]) return;
            }
            for (int INDEX = 0; INDEX < 6; INDEX++) 찾은장치[INDEX] = 입력틀[22 + INDEX];
            찾은주소 = seise_VALUE;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                출력틀[INDEX] = 입력틀[22 + INDEX]; 출력틀[32 + INDEX] = 입력틀[22 + INDEX];
                출력틀[22 + INDEX] = lìonra_dràibhear.uidheam_ADDRESS[INDEX];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, seise_VALUE);
            lìonra_dràibhear.cuir(출력틀, 42);
        }
    }

    static void Pròiseas_frèam(int faid_VALUE) {
        if (faid_VALUE < 14 || faid_VALUE > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, craoladh_VALUE = true;
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            if (입력틀[INDEX] != lìonra_dràibhear.uidheam_ADDRESS[INDEX]) 자기 = false;
            if (입력틀[INDEX] != 255) craoladh_VALUE = false;
        }
        if (!자기 && !craoladh_VALUE) return;
        if (àireamh_shlàn_16(입력틀, 12) == 0x0806) { Pròiseas_ADDRESS(faid_VALUE); return; }
        if (àireamh_shlàn_16(입력틀, 12) != 0x0800) return;
        if (faid_VALUE < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int bann_cinn_faid = (입력틀[14] & 15) * 4, 전체길이 = àireamh_shlàn_16(입력틀, 16);
        if (bann_cinn_faid < 20 || bann_cinn_faid > 60 || 전체길이 < bann_cinn_faid + 8 || 전체길이 > faid_VALUE - 14
            || (àireamh_shlàn_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || àireamh_shlàn_32(입력틀, 30) != 내주소 || SUM_VALUE(입력틀, 14, bann_cinn_faid, 0) != 65535) { 폐기수++; return; }
        int ruith = 14 + bann_cinn_faid, dàta_faid = àireamh_shlàn_16(입력틀, ruith + 4);
        if (dàta_faid < 8 || dàta_faid != 전체길이 - bann_cinn_faid || dàta_faid > 1032) { 폐기수++; return; }
        int 출발 = àireamh_shlàn_32(입력틀, 26);
        if (àireamh_shlàn_16(입력틀, ruith + 6) != 0 && SUM_VALUE(입력틀, ruith, dàta_faid, 가상머리합(출발, 내주소, dàta_faid)) != 65535) {
            폐기수++; return;
        }
        int ceann_uidhe_VALUE = àireamh_shlàn_16(입력틀, ruith + 2);
        for (int slot_cur_a_steach = 0; slot_cur_a_steach < 4; slot_cur_a_steach++) if (접속번호들[slot_cur_a_steach] != 0 && 접속번호들[slot_cur_a_steach] == ceann_uidhe_VALUE) {
            if (RECEIVED_faid[slot_cur_a_steach] >= 0) { 폐기수++; return; }
            RECEIVED_faid[slot_cur_a_steach] = dàta_faid - 8; RECEIVED_ADDRESS[slot_cur_a_steach] = 출발; 받은접속번호[slot_cur_a_steach] = àireamh_shlàn_16(입력틀, ruith);
            for (int INDEX = 0; INDEX < dàta_faid - 8; INDEX++) RECEIVED_dàta[slot_cur_a_steach * 1024 + INDEX] = 입력틀[ruith + 8 + INDEX];
            return;
        }
    }

    static void dearbh() {
        for (int INDEX = 0; INDEX < 16; INDEX++) {
            int faid_VALUE = lìonra_dràibhear.받기(입력틀);
            if (faid_VALUE == 0) return;
            Pròiseas_frèam(faid_VALUE);
        }
    }
    static int FIND_ADDRESS(int ADDRESS) {
        if (ADDRESS == 0 || ADDRESS == -1 || (ADDRESS >>> 28) >= 14 || (ADDRESS >>> 24) == 127 || ADDRESS == 내주소) return -101;
        int air_adhart_nì = (ADDRESS & 망경계) == (내주소 & 망경계) ? ADDRESS : 관문;
        if (air_adhart_nì == 찾은주소) return 0;
        찾을주소 = air_adhart_nì;
        int ruith = uidheam_VALUE.밀리초(), 다음요청 = ruith;
        while (uidheam_VALUE.밀리초() - ruith < 1000) {
            if (uidheam_VALUE.밀리초() - 다음요청 >= 0) { 주소요청(air_adhart_nì); 다음요청 += 300; }
            dearbh();
            if (찾은주소 == air_adhart_nì) return 0;
            uidheam_VALUE.잠시양보();
        }
        return -110;
    }
    static int cuir(int làmhrachan_VALUE, int ADDRESS, int 접속번호, int[] dàta, int faid_VALUE) {
        int slot_cur_a_steach = INDEX(làmhrachan_VALUE);
        if (slot_cur_a_steach < 0) return -9;
        if (lìonra_dràibhear.입출력기준주소 == 0) return -19;
        if (접속번호 < 1 || 접속번호 > 65535 || faid_VALUE < 0 || faid_VALUE > 1024) return -22;
        int tomhas = FIND_ADDRESS(ADDRESS);
        if (tomhas < 0) return tomhas;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + faid_VALUE);
        넣기16(출력틀, 18, aithnichear_VALUE++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, ADDRESS);
        넣기16(출력틀, 24, ~SUM_VALUE(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[slot_cur_a_steach]); 넣기16(출력틀, 36, 접속번호);
        넣기16(출력틀, 38, faid_VALUE + 8); 넣기16(출력틀, 40, 0);
        for (int INDEX = 0; INDEX < faid_VALUE; INDEX++) 출력틀[42 + INDEX] = dàta[INDEX] & 255;
        int 검사합 = (~SUM_VALUE(출력틀, 34, faid_VALUE + 8, 가상머리합(내주소, ADDRESS, faid_VALUE + 8))) & 65535;
        넣기16(출력틀, 40, 검사합 == 0 ? 65535 : 검사합);
        tomhas = lìonra_dràibhear.cuir(출력틀, faid_VALUE + 42);
        return tomhas < 0 ? tomhas : faid_VALUE;
    }
    static int 받기(int làmhrachan_VALUE, int[] dàta, int 용량, int 제한) {
        int slot_cur_a_steach = INDEX(làmhrachan_VALUE);
        if (slot_cur_a_steach < 0) return -9;
        int ruith = uidheam_VALUE.밀리초();
        while (true) {
            dearbh();
            int faid_VALUE = RECEIVED_faid[slot_cur_a_steach];
            if (faid_VALUE >= 0) {
                RECEIVED_faid[slot_cur_a_steach] = -1;
                if (faid_VALUE > 용량) return -90;
                for (int INDEX = 0; INDEX < faid_VALUE; INDEX++) dàta[INDEX] = RECEIVED_dàta[slot_cur_a_steach * 1024 + INDEX];
                return faid_VALUE;
            }
            if (제한 == 0) return -11;
            if (uidheam_VALUE.밀리초() - ruith >= 제한) return -110;
            uidheam_VALUE.잠시양보();
        }
    }
    static void cor_VALUE() {
        SMS_tèirmineal.sgrìobh(lìonra_dràibhear.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_tèirmineal.sgrìobh("TX: "); SMS_tèirmineal.수쓰기(lìonra_dràibhear.송신수);
        SMS_tèirmineal.sgrìobh(" RX: "); SMS_tèirmineal.수쓰기(lìonra_dràibhear.수신수);
        SMS_tèirmineal.sgrìobh(" DROP: "); SMS_tèirmineal.수쓰기(폐기수);
        SMS_tèirmineal.sgrìobh("\n");
    }
}
