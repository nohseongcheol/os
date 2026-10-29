// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** pateko_uara IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class whatunga_Huinga {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int whatunga_hīpoki = 0xffffff00; /* ip.conf:NETMASK */
    static final int waharoa_uara = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], RECEIVED_roa = new int[4], RECEIVED_ADDRESS = new int[4], 받은접속번호 = new int[4];
    static int[] RECEIVED_raraunga = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, pūtāutu_uara = 0, 폐기수 = 0;

    static int tau_tōpū_16(int[] tāpare_INDEX, int tūranga) { return (tāpare_INDEX[tūranga] << 8) | tāpare_INDEX[tūranga + 1]; }
    static int tau_tōpū_32(int[] tāpare_INDEX, int tūranga) { return (tau_tōpū_16(tāpare_INDEX, tūranga) << 16) | tau_tōpū_16(tāpare_INDEX, tūranga + 2); }
    static void 넣기16(int[] tāpare_INDEX, int tūranga, int uara) { tāpare_INDEX[tūranga] = (uara >>> 8) & 255; tāpare_INDEX[tūranga + 1] = uara & 255; }
    static void 넣기32(int[] tāpare_INDEX, int tūranga, int uara) { 넣기16(tāpare_INDEX, tūranga, uara >>> 16); 넣기16(tāpare_INDEX, tūranga + 2, uara); }
    static int SUM_uara(int[] tāpare_INDEX, int whakahaere, int roa_uara, int uara) {
        for (int INDEX = 0; INDEX < roa_uara; INDEX += 2)
            uara += (tāpare_INDEX[whakahaere + INDEX] << 8) | (INDEX + 1 < roa_uara ? tāpare_INDEX[whakahaere + INDEX + 1] : 0);
        while ((uara >>> 16) != 0) uara = (uara & 65535) + (uara >>> 16);
        return uara;
    }
    static int 가상머리합(int 출발, int 도착, int roa_uara) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + roa_uara;
    }

    static void CLEAN_Hātepe() {
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            접속번호들[INDEX] = 0; RECEIVED_roa[INDEX] = -1; RECEIVED_ADDRESS[INDEX] = 0; 받은접속번호[INDEX] = 0;
        }
        for (int INDEX = 0; INDEX < 64; INDEX++) if (whatunga_atekōkiri.받기(입력틀) == 0) break;
    }
    static int INDEX(int raweke_uara) { return raweke_uara >= 3 && raweke_uara < 7 && 접속번호들[raweke_uara - 3] != 0 ? raweke_uara - 3 : -1; }
    static int Huaki(int 접속번호) {
        if (whatunga_atekōkiri.입출력기준주소 == 0) return -19;
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
            접속번호들[INDEX] = 접속번호; RECEIVED_roa[INDEX] = -1;
            return INDEX + 3;
        }
        return -24;
    }
    static int Kati(int raweke_uara) {
        int kāniwha_tāurunga = INDEX(raweke_uara);
        if (kāniwha_tāurunga < 0) return -9;
        접속번호들[kāniwha_tāurunga] = 0; RECEIVED_roa[kāniwha_tāurunga] = -1;
        return 0;
    }
    static int hoa_ADDRESS(int raweke_uara) { int kāniwha_tāurunga = INDEX(raweke_uara); return kāniwha_tāurunga < 0 ? -9 : RECEIVED_ADDRESS[kāniwha_tāurunga]; }
    static int 상대접속번호(int raweke_uara) { int kāniwha_tāurunga = INDEX(raweke_uara); return kāniwha_tāurunga < 0 ? -9 : 받은접속번호[kāniwha_tāurunga]; }

    static void 바깥머리(int 종류, boolean pāohotanga_uara) {
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[INDEX] = pāohotanga_uara ? 255 : 찾은장치[INDEX];
            출력틀[6 + INDEX] = whatunga_atekōkiri.pūkoro_ADDRESS[INDEX];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void 주소요청(int ūnga_uara) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[22 + INDEX] = whatunga_atekōkiri.pūkoro_ADDRESS[INDEX]; 출력틀[32 + INDEX] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, ūnga_uara);
        whatunga_atekōkiri.tuku(출력틀, 42);
    }
    static void Hātepe_ADDRESS(int roa_uara) {
        if (roa_uara < 42 || tau_tōpū_16(입력틀, 14) != 1 || tau_tōpū_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || tau_tōpū_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = tau_tōpū_16(입력틀, 20), hoa_uara = tau_tōpū_32(입력틀, 28);
        if (종류 == 2 && hoa_uara == 찾을주소) {
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                if (입력틀[6 + INDEX] != 입력틀[22 + INDEX] || 입력틀[32 + INDEX] != whatunga_atekōkiri.pūkoro_ADDRESS[INDEX]) return;
            }
            for (int INDEX = 0; INDEX < 6; INDEX++) 찾은장치[INDEX] = 입력틀[22 + INDEX];
            찾은주소 = hoa_uara;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                출력틀[INDEX] = 입력틀[22 + INDEX]; 출력틀[32 + INDEX] = 입력틀[22 + INDEX];
                출력틀[22 + INDEX] = whatunga_atekōkiri.pūkoro_ADDRESS[INDEX];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, hoa_uara);
            whatunga_atekōkiri.tuku(출력틀, 42);
        }
    }

    static void Hātepe_tāpare(int roa_uara) {
        if (roa_uara < 14 || roa_uara > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, pāohotanga_uara = true;
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            if (입력틀[INDEX] != whatunga_atekōkiri.pūkoro_ADDRESS[INDEX]) 자기 = false;
            if (입력틀[INDEX] != 255) pāohotanga_uara = false;
        }
        if (!자기 && !pāohotanga_uara) return;
        if (tau_tōpū_16(입력틀, 12) == 0x0806) { Hātepe_ADDRESS(roa_uara); return; }
        if (tau_tōpū_16(입력틀, 12) != 0x0800) return;
        if (roa_uara < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int Pane_roa = (입력틀[14] & 15) * 4, 전체길이 = tau_tōpū_16(입력틀, 16);
        if (Pane_roa < 20 || Pane_roa > 60 || 전체길이 < Pane_roa + 8 || 전체길이 > roa_uara - 14
            || (tau_tōpū_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || tau_tōpū_32(입력틀, 30) != 내주소 || SUM_uara(입력틀, 14, Pane_roa, 0) != 65535) { 폐기수++; return; }
        int whakahaere = 14 + Pane_roa, raraunga_roa = tau_tōpū_16(입력틀, whakahaere + 4);
        if (raraunga_roa < 8 || raraunga_roa != 전체길이 - Pane_roa || raraunga_roa > 1032) { 폐기수++; return; }
        int 출발 = tau_tōpū_32(입력틀, 26);
        if (tau_tōpū_16(입력틀, whakahaere + 6) != 0 && SUM_uara(입력틀, whakahaere, raraunga_roa, 가상머리합(출발, 내주소, raraunga_roa)) != 65535) {
            폐기수++; return;
        }
        int ūnga_uara = tau_tōpū_16(입력틀, whakahaere + 2);
        for (int kāniwha_tāurunga = 0; kāniwha_tāurunga < 4; kāniwha_tāurunga++) if (접속번호들[kāniwha_tāurunga] != 0 && 접속번호들[kāniwha_tāurunga] == ūnga_uara) {
            if (RECEIVED_roa[kāniwha_tāurunga] >= 0) { 폐기수++; return; }
            RECEIVED_roa[kāniwha_tāurunga] = raraunga_roa - 8; RECEIVED_ADDRESS[kāniwha_tāurunga] = 출발; 받은접속번호[kāniwha_tāurunga] = tau_tōpū_16(입력틀, whakahaere);
            for (int INDEX = 0; INDEX < raraunga_roa - 8; INDEX++) RECEIVED_raraunga[kāniwha_tāurunga * 1024 + INDEX] = 입력틀[whakahaere + 8 + INDEX];
            return;
        }
    }

    static void manatoko() {
        for (int INDEX = 0; INDEX < 16; INDEX++) {
            int roa_uara = whatunga_atekōkiri.받기(입력틀);
            if (roa_uara == 0) return;
            Hātepe_tāpare(roa_uara);
        }
    }
    static int FIND_ADDRESS(int ADDRESS) {
        if (ADDRESS == 0 || ADDRESS == -1 || (ADDRESS >>> 28) >= 14 || (ADDRESS >>> 24) == 127 || ADDRESS == 내주소) return -101;
        int Panuku_tuemi = (ADDRESS & whatunga_hīpoki) == (내주소 & whatunga_hīpoki) ? ADDRESS : waharoa_uara;
        if (Panuku_tuemi == 찾은주소) return 0;
        찾을주소 = Panuku_tuemi;
        int whakahaere = pūkoro_uara.밀리초(), 다음요청 = whakahaere;
        while (pūkoro_uara.밀리초() - whakahaere < 1000) {
            if (pūkoro_uara.밀리초() - 다음요청 >= 0) { 주소요청(Panuku_tuemi); 다음요청 += 300; }
            manatoko();
            if (찾은주소 == Panuku_tuemi) return 0;
            pūkoro_uara.잠시양보();
        }
        return -110;
    }
    static int tuku(int raweke_uara, int ADDRESS, int 접속번호, int[] raraunga, int roa_uara) {
        int kāniwha_tāurunga = INDEX(raweke_uara);
        if (kāniwha_tāurunga < 0) return -9;
        if (whatunga_atekōkiri.입출력기준주소 == 0) return -19;
        if (접속번호 < 1 || 접속번호 > 65535 || roa_uara < 0 || roa_uara > 1024) return -22;
        int mēhua = FIND_ADDRESS(ADDRESS);
        if (mēhua < 0) return mēhua;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + roa_uara);
        넣기16(출력틀, 18, pūtāutu_uara++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, ADDRESS);
        넣기16(출력틀, 24, ~SUM_uara(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[kāniwha_tāurunga]); 넣기16(출력틀, 36, 접속번호);
        넣기16(출력틀, 38, roa_uara + 8); 넣기16(출력틀, 40, 0);
        for (int INDEX = 0; INDEX < roa_uara; INDEX++) 출력틀[42 + INDEX] = raraunga[INDEX] & 255;
        int 검사합 = (~SUM_uara(출력틀, 34, roa_uara + 8, 가상머리합(내주소, ADDRESS, roa_uara + 8))) & 65535;
        넣기16(출력틀, 40, 검사합 == 0 ? 65535 : 검사합);
        mēhua = whatunga_atekōkiri.tuku(출력틀, roa_uara + 42);
        return mēhua < 0 ? mēhua : roa_uara;
    }
    static int 받기(int raweke_uara, int[] raraunga, int 용량, int 제한) {
        int kāniwha_tāurunga = INDEX(raweke_uara);
        if (kāniwha_tāurunga < 0) return -9;
        int whakahaere = pūkoro_uara.밀리초();
        while (true) {
            manatoko();
            int roa_uara = RECEIVED_roa[kāniwha_tāurunga];
            if (roa_uara >= 0) {
                RECEIVED_roa[kāniwha_tāurunga] = -1;
                if (roa_uara > 용량) return -90;
                for (int INDEX = 0; INDEX < roa_uara; INDEX++) raraunga[INDEX] = RECEIVED_raraunga[kāniwha_tāurunga * 1024 + INDEX];
                return roa_uara;
            }
            if (제한 == 0) return -11;
            if (pūkoro_uara.밀리초() - whakahaere >= 제한) return -110;
            pūkoro_uara.잠시양보();
        }
    }
    static void tūnga_uara() {
        TEXT_Tauranga.Tuhia(whatunga_atekōkiri.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        TEXT_Tauranga.Tuhia("TX: "); TEXT_Tauranga.수쓰기(whatunga_atekōkiri.송신수);
        TEXT_Tauranga.Tuhia(" RX: "); TEXT_Tauranga.수쓰기(whatunga_atekōkiri.수신수);
        TEXT_Tauranga.Tuhia(" DROP: "); TEXT_Tauranga.수쓰기(폐기수);
        TEXT_Tauranga.Tuhia("\n");
    }
}
