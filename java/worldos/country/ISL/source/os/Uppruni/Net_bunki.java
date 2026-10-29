// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** fast_VALUE IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class Net_bunki {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int Net_sía = 0xffffff00; /* ip.conf:NETMASK */
    static final int gátt_VALUE_cfee51e8 = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], úttak_ramma = new int[1536];
    static int[] 접속번호들 = new int[4], RECEIVED_lengd = new int[4], RECEIVED_slóð = new int[4], RECEIVED_tengisnúmer = new int[4];
    static int[] RECEIVED_gögn = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, auðkenni_VALUE = 0, 폐기수 = 0;

    static int heiltala_16(int[] ramma_INDEX, int Staðsetning) { return (ramma_INDEX[Staðsetning] << 8) | ramma_INDEX[Staðsetning + 1]; }
    static int heiltala_32(int[] ramma_INDEX, int Staðsetning) { return (heiltala_16(ramma_INDEX, Staðsetning) << 16) | heiltala_16(ramma_INDEX, Staðsetning + 2); }
    static void 넣기16(int[] ramma_INDEX, int Staðsetning, int VALUE) { ramma_INDEX[Staðsetning] = (VALUE >>> 8) & 255; ramma_INDEX[Staðsetning + 1] = VALUE & 255; }
    static void 넣기32(int[] ramma_INDEX, int Staðsetning, int VALUE) { 넣기16(ramma_INDEX, Staðsetning, VALUE >>> 16); 넣기16(ramma_INDEX, Staðsetning + 2, VALUE); }
    static int SUM_VALUE(int[] ramma_INDEX, int Keyra_2, int lengd_VALUE, int VALUE) {
        for (int INDEX = 0; INDEX < lengd_VALUE; INDEX += 2)
            VALUE += (ramma_INDEX[Keyra_2 + INDEX] << 8) | (INDEX + 1 < lengd_VALUE ? ramma_INDEX[Keyra_2 + INDEX + 1] : 0);
        while ((VALUE >>> 16) != 0) VALUE = (VALUE & 65535) + (VALUE >>> 16);
        return VALUE;
    }
    static int 가상머리합(int 출발, int 도착, int lengd_VALUE) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + lengd_VALUE;
    }

    static void CLEAN_Ferli() {
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            접속번호들[INDEX] = 0; RECEIVED_lengd[INDEX] = -1; RECEIVED_slóð[INDEX] = 0; RECEIVED_tengisnúmer[INDEX] = 0;
        }
        for (int INDEX = 0; INDEX < 64; INDEX++) if (Net_rekill.받기(입력틀) == 0) break;
    }
    static int INDEX(int hald_VALUE) { return hald_VALUE >= 3 && hald_VALUE < 7 && 접속번호들[hald_VALUE - 3] != 0 ? hald_VALUE - 3 : -1; }
    static int Opna(int tengisnúmer) {
        if (Net_rekill.입출력기준주소 == 0) return -19;
        if (tengisnúmer < 0 || tengisnúmer > 65535) return -22;
        if (tengisnúmer != 0) for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == tengisnúmer) return -98;
        for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == 0) {
            if (tengisnúmer == 0) {
                tengisnúmer = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int myndavél_að_framan_VALUE = 0; myndavél_að_framan_VALUE < 4; myndavél_að_framan_VALUE++) if (접속번호들[myndavél_að_framan_VALUE] == tengisnúmer) 겹침 = true;
                    if (겹침) tengisnúmer++;
                }
            }
            접속번호들[INDEX] = tengisnúmer; RECEIVED_lengd[INDEX] = -1;
            return INDEX + 3;
        }
        return -24;
    }
    static int Loka(int hald_VALUE) {
        int rauf_færsla = INDEX(hald_VALUE);
        if (rauf_færsla < 0) return -9;
        접속번호들[rauf_færsla] = 0; RECEIVED_lengd[rauf_færsla] = -1;
        return 0;
    }
    static int jafningi_slóð(int hald_VALUE) { int rauf_færsla = INDEX(hald_VALUE); return rauf_færsla < 0 ? -9 : RECEIVED_slóð[rauf_færsla]; }
    static int jafningi_tengisnúmer(int hald_VALUE) { int rauf_færsla = INDEX(hald_VALUE); return rauf_færsla < 0 ? -9 : RECEIVED_tengisnúmer[rauf_færsla]; }

    static void 바깥머리(int 종류, boolean senda_út_VALUE) {
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            úttak_ramma[INDEX] = senda_út_VALUE ? 255 : 찾은장치[INDEX];
            úttak_ramma[6 + INDEX] = Net_rekill.tæki_slóð[INDEX];
        }
        넣기16(úttak_ramma, 12, 종류);
    }
    static void 주소요청(int endastaður_VALUE) {
        바깥머리(0x0806, true);
        넣기16(úttak_ramma, 14, 1); 넣기16(úttak_ramma, 16, 0x0800);
        úttak_ramma[18] = 6; úttak_ramma[19] = 4; 넣기16(úttak_ramma, 20, 1);
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            úttak_ramma[22 + INDEX] = Net_rekill.tæki_slóð[INDEX]; úttak_ramma[32 + INDEX] = 0;
        }
        넣기32(úttak_ramma, 28, 내주소); 넣기32(úttak_ramma, 38, endastaður_VALUE);
        Net_rekill.senda(úttak_ramma, 42);
    }
    static void Ferli_slóð(int lengd_VALUE) {
        if (lengd_VALUE < 42 || heiltala_16(입력틀, 14) != 1 || heiltala_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || heiltala_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = heiltala_16(입력틀, 20), jafningi_VALUE = heiltala_32(입력틀, 28);
        if (종류 == 2 && jafningi_VALUE == 찾을주소) {
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                if (입력틀[6 + INDEX] != 입력틀[22 + INDEX] || 입력틀[32 + INDEX] != Net_rekill.tæki_slóð[INDEX]) return;
            }
            for (int INDEX = 0; INDEX < 6; INDEX++) 찾은장치[INDEX] = 입력틀[22 + INDEX];
            찾은주소 = jafningi_VALUE;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(úttak_ramma, 14, 1); 넣기16(úttak_ramma, 16, 0x0800);
            úttak_ramma[18] = 6; úttak_ramma[19] = 4; 넣기16(úttak_ramma, 20, 2);
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                úttak_ramma[INDEX] = 입력틀[22 + INDEX]; úttak_ramma[32 + INDEX] = 입력틀[22 + INDEX];
                úttak_ramma[22 + INDEX] = Net_rekill.tæki_slóð[INDEX];
            }
            넣기32(úttak_ramma, 28, 내주소); 넣기32(úttak_ramma, 38, jafningi_VALUE);
            Net_rekill.senda(úttak_ramma, 42);
        }
    }

    static void Ferli_ramma(int lengd_VALUE) {
        if (lengd_VALUE < 14 || lengd_VALUE > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, senda_út_VALUE = true;
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            if (입력틀[INDEX] != Net_rekill.tæki_slóð[INDEX]) 자기 = false;
            if (입력틀[INDEX] != 255) senda_út_VALUE = false;
        }
        if (!자기 && !senda_út_VALUE) return;
        if (heiltala_16(입력틀, 12) == 0x0806) { Ferli_slóð(lengd_VALUE); return; }
        if (heiltala_16(입력틀, 12) != 0x0800) return;
        if (lengd_VALUE < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int Haus_lengd = (입력틀[14] & 15) * 4, samtala_lengd = heiltala_16(입력틀, 16);
        if (Haus_lengd < 20 || Haus_lengd > 60 || samtala_lengd < Haus_lengd + 8 || samtala_lengd > lengd_VALUE - 14
            || (heiltala_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || heiltala_32(입력틀, 30) != 내주소 || SUM_VALUE(입력틀, 14, Haus_lengd, 0) != 65535) { 폐기수++; return; }
        int Keyra_2 = 14 + Haus_lengd, gögn_lengd = heiltala_16(입력틀, Keyra_2 + 4);
        if (gögn_lengd < 8 || gögn_lengd != samtala_lengd - Haus_lengd || gögn_lengd > 1032) { 폐기수++; return; }
        int 출발 = heiltala_32(입력틀, 26);
        if (heiltala_16(입력틀, Keyra_2 + 6) != 0 && SUM_VALUE(입력틀, Keyra_2, gögn_lengd, 가상머리합(출발, 내주소, gögn_lengd)) != 65535) {
            폐기수++; return;
        }
        int endastaður_VALUE = heiltala_16(입력틀, Keyra_2 + 2);
        for (int rauf_færsla = 0; rauf_færsla < 4; rauf_færsla++) if (접속번호들[rauf_færsla] != 0 && 접속번호들[rauf_færsla] == endastaður_VALUE) {
            if (RECEIVED_lengd[rauf_færsla] >= 0) { 폐기수++; return; }
            RECEIVED_lengd[rauf_færsla] = gögn_lengd - 8; RECEIVED_slóð[rauf_færsla] = 출발; RECEIVED_tengisnúmer[rauf_færsla] = heiltala_16(입력틀, Keyra_2);
            for (int INDEX = 0; INDEX < gögn_lengd - 8; INDEX++) RECEIVED_gögn[rauf_færsla * 1024 + INDEX] = 입력틀[Keyra_2 + 8 + INDEX];
            return;
        }
    }

    static void sannprófa() {
        for (int INDEX = 0; INDEX < 16; INDEX++) {
            int lengd_VALUE = Net_rekill.받기(입력틀);
            if (lengd_VALUE == 0) return;
            Ferli_ramma(lengd_VALUE);
        }
    }
    static int FIND_slóð(int slóð) {
        if (slóð == 0 || slóð == -1 || (slóð >>> 28) >= 14 || (slóð >>> 24) == 127 || slóð == 내주소) return -101;
        int Áfram_vara = (slóð & Net_sía) == (내주소 & Net_sía) ? slóð : gátt_VALUE_cfee51e8;
        if (Áfram_vara == 찾은주소) return 0;
        찾을주소 = Áfram_vara;
        int Keyra_2 = tæki_VALUE.밀리초(), 다음요청 = Keyra_2;
        while (tæki_VALUE.밀리초() - Keyra_2 < 1000) {
            if (tæki_VALUE.밀리초() - 다음요청 >= 0) { 주소요청(Áfram_vara); 다음요청 += 300; }
            sannprófa();
            if (찾은주소 == Áfram_vara) return 0;
            tæki_VALUE.잠시양보();
        }
        return -110;
    }
    static int senda(int hald_VALUE, int slóð, int tengisnúmer, int[] gögn, int lengd_VALUE) {
        int rauf_færsla = INDEX(hald_VALUE);
        if (rauf_færsla < 0) return -9;
        if (Net_rekill.입출력기준주소 == 0) return -19;
        if (tengisnúmer < 1 || tengisnúmer > 65535 || lengd_VALUE < 0 || lengd_VALUE > 1024) return -22;
        int NIÐURSTAÐA = FIND_slóð(slóð);
        if (NIÐURSTAÐA < 0) return NIÐURSTAÐA;
        바깥머리(0x0800, false);
        úttak_ramma[14] = 0x45; úttak_ramma[15] = 0; 넣기16(úttak_ramma, 16, 28 + lengd_VALUE);
        넣기16(úttak_ramma, 18, auðkenni_VALUE++); 넣기16(úttak_ramma, 20, 0x4000);
        úttak_ramma[22] = 64; úttak_ramma[23] = 17; 넣기16(úttak_ramma, 24, 0);
        넣기32(úttak_ramma, 26, 내주소); 넣기32(úttak_ramma, 30, slóð);
        넣기16(úttak_ramma, 24, ~SUM_VALUE(úttak_ramma, 14, 20, 0));
        넣기16(úttak_ramma, 34, 접속번호들[rauf_færsla]); 넣기16(úttak_ramma, 36, tengisnúmer);
        넣기16(úttak_ramma, 38, lengd_VALUE + 8); 넣기16(úttak_ramma, 40, 0);
        for (int INDEX = 0; INDEX < lengd_VALUE; INDEX++) úttak_ramma[42 + INDEX] = gögn[INDEX] & 255;
        int prófsumma = (~SUM_VALUE(úttak_ramma, 34, lengd_VALUE + 8, 가상머리합(내주소, slóð, lengd_VALUE + 8))) & 65535;
        넣기16(úttak_ramma, 40, prófsumma == 0 ? 65535 : prófsumma);
        NIÐURSTAÐA = Net_rekill.senda(úttak_ramma, lengd_VALUE + 42);
        return NIÐURSTAÐA < 0 ? NIÐURSTAÐA : lengd_VALUE;
    }
    static int 받기(int hald_VALUE, int[] gögn, int afkastageta_VALUE, int 제한) {
        int rauf_færsla = INDEX(hald_VALUE);
        if (rauf_færsla < 0) return -9;
        int Keyra_2 = tæki_VALUE.밀리초();
        while (true) {
            sannprófa();
            int lengd_VALUE = RECEIVED_lengd[rauf_færsla];
            if (lengd_VALUE >= 0) {
                RECEIVED_lengd[rauf_færsla] = -1;
                if (lengd_VALUE > afkastageta_VALUE) return -90;
                for (int INDEX = 0; INDEX < lengd_VALUE; INDEX++) gögn[INDEX] = RECEIVED_gögn[rauf_færsla * 1024 + INDEX];
                return lengd_VALUE;
            }
            if (제한 == 0) return -11;
            if (tæki_VALUE.밀리초() - Keyra_2 >= 제한) return -110;
            tæki_VALUE.잠시양보();
        }
    }
    static void staða_VALUE_e10195a1() {
        SMS_Endastöð.Skrift(Net_rekill.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Endastöð.Skrift("TX: "); SMS_Endastöð.skrifa_númer(Net_rekill.송신수);
        SMS_Endastöð.Skrift(" RX: "); SMS_Endastöð.skrifa_númer(Net_rekill.수신수);
        SMS_Endastöð.Skrift(" DROP: "); SMS_Endastöð.skrifa_númer(폐기수);
        SMS_Endastöð.Skrift("\n");
    }
}
