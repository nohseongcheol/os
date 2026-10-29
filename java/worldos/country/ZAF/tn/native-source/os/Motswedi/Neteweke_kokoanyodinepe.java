// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** e_e_emeng_Boleng IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class Neteweke_kokoanyodinepe {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int Neteweke_mmaseke = 0xffffff00; /* ip.conf:NETMASK */
    static final int kgorotsamaiso_Boleng = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], 받은길이 = new int[4], 받은주소 = new int[4], 받은접속번호 = new int[4];
    static int[] 받은자료 = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, setlhaodi_Boleng = 0, 폐기수 = 0;

    static int Palotlalo_16(int[] Foreimi_tshupane, int 위치) { return (Foreimi_tshupane[위치] << 8) | Foreimi_tshupane[위치 + 1]; }
    static int Palotlalo_32(int[] Foreimi_tshupane, int 위치) { return (Palotlalo_16(Foreimi_tshupane, 위치) << 16) | Palotlalo_16(Foreimi_tshupane, 위치 + 2); }
    static void 넣기16(int[] Foreimi_tshupane, int 위치, int Boleng) { Foreimi_tshupane[위치] = (Boleng >>> 8) & 255; Foreimi_tshupane[위치 + 1] = Boleng & 255; }
    static void 넣기32(int[] Foreimi_tshupane, int 위치, int Boleng) { 넣기16(Foreimi_tshupane, 위치, Boleng >>> 16); 넣기16(Foreimi_tshupane, 위치 + 2, Boleng); }
    static int 합(int[] Foreimi_tshupane, int dirisa, int boleele_Boleng, int Boleng) {
        for (int tshupane = 0; tshupane < boleele_Boleng; tshupane += 2)
            Boleng += (Foreimi_tshupane[dirisa + tshupane] << 8) | (tshupane + 1 < boleele_Boleng ? Foreimi_tshupane[dirisa + tshupane + 1] : 0);
        while ((Boleng >>> 16) != 0) Boleng = (Boleng & 65535) + (Boleng >>> 16);
        return Boleng;
    }
    static int 가상머리합(int 출발, int 도착, int boleele_Boleng) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + boleele_Boleng;
    }

    static void 과정정리() {
        for (int tshupane = 0; tshupane < 4; tshupane++) {
            접속번호들[tshupane] = 0; 받은길이[tshupane] = -1; 받은주소[tshupane] = 0; 받은접속번호[tshupane] = 0;
        }
        for (int tshupane = 0; tshupane < 64; tshupane++) if (Neteweke_selaodi.받기(입력틀) == 0) break;
    }
    static int tshupane(int mokgwakamogelo_Boleng) { return mokgwakamogelo_Boleng >= 3 && mokgwakamogelo_Boleng < 7 && 접속번호들[mokgwakamogelo_Boleng - 3] != 0 ? mokgwakamogelo_Boleng - 3 : -1; }
    static int bula(int 접속번호) {
        if (Neteweke_selaodi.입출력기준주소 == 0) return -19;
        if (접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 != 0) for (int tshupane = 0; tshupane < 4; tshupane++) if (접속번호들[tshupane] == 접속번호) return -98;
        for (int tshupane = 0; tshupane < 4; tshupane++) if (접속번호들[tshupane] == 0) {
            if (접속번호 == 0) {
                접속번호 = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int 앞 = 0; 앞 < 4; 앞++) if (접속번호들[앞] == 접속번호) 겹침 = true;
                    if (겹침) 접속번호++;
                }
            }
            접속번호들[tshupane] = 접속번호; 받은길이[tshupane] = -1;
            return tshupane + 3;
        }
        return -24;
    }
    static int tswala(int mokgwakamogelo_Boleng) {
        int sebaka_tsenyo = tshupane(mokgwakamogelo_Boleng);
        if (sebaka_tsenyo < 0) return -9;
        접속번호들[sebaka_tsenyo] = 0; 받은길이[sebaka_tsenyo] = -1;
        return 0;
    }
    static int semphato_aterese(int mokgwakamogelo_Boleng) { int sebaka_tsenyo = tshupane(mokgwakamogelo_Boleng); return sebaka_tsenyo < 0 ? -9 : 받은주소[sebaka_tsenyo]; }
    static int 상대접속번호(int mokgwakamogelo_Boleng) { int sebaka_tsenyo = tshupane(mokgwakamogelo_Boleng); return sebaka_tsenyo < 0 ? -9 : 받은접속번호[sebaka_tsenyo]; }

    static void 바깥머리(int 종류, boolean kgaso_Boleng) {
        for (int tshupane = 0; tshupane < 6; tshupane++) {
            출력틀[tshupane] = kgaso_Boleng ? 255 : 찾은장치[tshupane];
            출력틀[6 + tshupane] = Neteweke_selaodi.mobaele_aterese[tshupane];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void 주소요청(int bogorogelo_Boleng) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int tshupane = 0; tshupane < 6; tshupane++) {
            출력틀[22 + tshupane] = Neteweke_selaodi.mobaele_aterese[tshupane]; 출력틀[32 + tshupane] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, bogorogelo_Boleng);
        Neteweke_selaodi.romela(출력틀, 42);
    }
    static void Thulaganyo_aterese(int boleele_Boleng) {
        if (boleele_Boleng < 42 || Palotlalo_16(입력틀, 14) != 1 || Palotlalo_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || Palotlalo_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = Palotlalo_16(입력틀, 20), semphato_Boleng = Palotlalo_32(입력틀, 28);
        if (종류 == 2 && semphato_Boleng == 찾을주소) {
            for (int tshupane = 0; tshupane < 6; tshupane++) {
                if (입력틀[6 + tshupane] != 입력틀[22 + tshupane] || 입력틀[32 + tshupane] != Neteweke_selaodi.mobaele_aterese[tshupane]) return;
            }
            for (int tshupane = 0; tshupane < 6; tshupane++) 찾은장치[tshupane] = 입력틀[22 + tshupane];
            찾은주소 = semphato_Boleng;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int tshupane = 0; tshupane < 6; tshupane++) {
                출력틀[tshupane] = 입력틀[22 + tshupane]; 출력틀[32 + tshupane] = 입력틀[22 + tshupane];
                출력틀[22 + tshupane] = Neteweke_selaodi.mobaele_aterese[tshupane];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, semphato_Boleng);
            Neteweke_selaodi.romela(출력틀, 42);
        }
    }

    static void Thulaganyo_Foreimi(int boleele_Boleng) {
        if (boleele_Boleng < 14 || boleele_Boleng > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, kgaso_Boleng = true;
        for (int tshupane = 0; tshupane < 6; tshupane++) {
            if (입력틀[tshupane] != Neteweke_selaodi.mobaele_aterese[tshupane]) 자기 = false;
            if (입력틀[tshupane] != 255) kgaso_Boleng = false;
        }
        if (!자기 && !kgaso_Boleng) return;
        if (Palotlalo_16(입력틀, 12) == 0x0806) { Thulaganyo_aterese(boleele_Boleng); return; }
        if (Palotlalo_16(입력틀, 12) != 0x0800) return;
        if (boleele_Boleng < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int setlhogo_boleele = (입력틀[14] & 15) * 4, 전체길이 = Palotlalo_16(입력틀, 16);
        if (setlhogo_boleele < 20 || setlhogo_boleele > 60 || 전체길이 < setlhogo_boleele + 8 || 전체길이 > boleele_Boleng - 14
            || (Palotlalo_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || Palotlalo_32(입력틀, 30) != 내주소 || 합(입력틀, 14, setlhogo_boleele, 0) != 65535) { 폐기수++; return; }
        int dirisa = 14 + setlhogo_boleele, tshedimosetso_boleele = Palotlalo_16(입력틀, dirisa + 4);
        if (tshedimosetso_boleele < 8 || tshedimosetso_boleele != 전체길이 - setlhogo_boleele || tshedimosetso_boleele > 1032) { 폐기수++; return; }
        int 출발 = Palotlalo_32(입력틀, 26);
        if (Palotlalo_16(입력틀, dirisa + 6) != 0 && 합(입력틀, dirisa, tshedimosetso_boleele, 가상머리합(출발, 내주소, tshedimosetso_boleele)) != 65535) {
            폐기수++; return;
        }
        int bogorogelo_Boleng = Palotlalo_16(입력틀, dirisa + 2);
        for (int sebaka_tsenyo = 0; sebaka_tsenyo < 4; sebaka_tsenyo++) if (접속번호들[sebaka_tsenyo] != 0 && 접속번호들[sebaka_tsenyo] == bogorogelo_Boleng) {
            if (받은길이[sebaka_tsenyo] >= 0) { 폐기수++; return; }
            받은길이[sebaka_tsenyo] = tshedimosetso_boleele - 8; 받은주소[sebaka_tsenyo] = 출발; 받은접속번호[sebaka_tsenyo] = Palotlalo_16(입력틀, dirisa);
            for (int tshupane = 0; tshupane < tshedimosetso_boleele - 8; tshupane++) 받은자료[sebaka_tsenyo * 1024 + tshupane] = 입력틀[dirisa + 8 + tshupane];
            return;
        }
    }

    static void netefatsa() {
        for (int tshupane = 0; tshupane < 16; tshupane++) {
            int boleele_Boleng = Neteweke_selaodi.받기(입력틀);
            if (boleele_Boleng == 0) return;
            Thulaganyo_Foreimi(boleele_Boleng);
        }
    }
    static int batla_aterese(int aterese) {
        if (aterese == 0 || aterese == -1 || (aterese >>> 28) >= 14 || (aterese >>> 24) == 127 || aterese == 내주소) return -101;
        int 다음 = (aterese & Neteweke_mmaseke) == (내주소 & Neteweke_mmaseke) ? aterese : kgorotsamaiso_Boleng;
        if (다음 == 찾은주소) return 0;
        찾을주소 = 다음;
        int dirisa = mobaele_Boleng.밀리초(), 다음요청 = dirisa;
        while (mobaele_Boleng.밀리초() - dirisa < 1000) {
            if (mobaele_Boleng.밀리초() - 다음요청 >= 0) { 주소요청(다음); 다음요청 += 300; }
            netefatsa();
            if (찾은주소 == 다음) return 0;
            mobaele_Boleng.잠시양보();
        }
        return -110;
    }
    static int romela(int mokgwakamogelo_Boleng, int aterese, int 접속번호, int[] tshedimosetso, int boleele_Boleng) {
        int sebaka_tsenyo = tshupane(mokgwakamogelo_Boleng);
        if (sebaka_tsenyo < 0) return -9;
        if (Neteweke_selaodi.입출력기준주소 == 0) return -19;
        if (접속번호 < 1 || 접속번호 > 65535 || boleele_Boleng < 0 || boleele_Boleng > 1024) return -22;
        int 결과 = batla_aterese(aterese);
        if (결과 < 0) return 결과;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + boleele_Boleng);
        넣기16(출력틀, 18, setlhaodi_Boleng++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, aterese);
        넣기16(출력틀, 24, ~합(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[sebaka_tsenyo]); 넣기16(출력틀, 36, 접속번호);
        넣기16(출력틀, 38, boleele_Boleng + 8); 넣기16(출력틀, 40, 0);
        for (int tshupane = 0; tshupane < boleele_Boleng; tshupane++) 출력틀[42 + tshupane] = tshedimosetso[tshupane] & 255;
        int 검사합 = (~합(출력틀, 34, boleele_Boleng + 8, 가상머리합(내주소, aterese, boleele_Boleng + 8))) & 65535;
        넣기16(출력틀, 40, 검사합 == 0 ? 65535 : 검사합);
        결과 = Neteweke_selaodi.romela(출력틀, boleele_Boleng + 42);
        return 결과 < 0 ? 결과 : boleele_Boleng;
    }
    static int 받기(int mokgwakamogelo_Boleng, int[] tshedimosetso, int 용량, int 제한) {
        int sebaka_tsenyo = tshupane(mokgwakamogelo_Boleng);
        if (sebaka_tsenyo < 0) return -9;
        int dirisa = mobaele_Boleng.밀리초();
        while (true) {
            netefatsa();
            int boleele_Boleng = 받은길이[sebaka_tsenyo];
            if (boleele_Boleng >= 0) {
                받은길이[sebaka_tsenyo] = -1;
                if (boleele_Boleng > 용량) return -90;
                for (int tshupane = 0; tshupane < boleele_Boleng; tshupane++) tshedimosetso[tshupane] = 받은자료[sebaka_tsenyo * 1024 + tshupane];
                return boleele_Boleng;
            }
            if (제한 == 0) return -11;
            if (mobaele_Boleng.밀리초() - dirisa >= 제한) return -110;
            mobaele_Boleng.잠시양보();
        }
    }
    static void kemo_Boleng() {
        문자단말.kwala(Neteweke_selaodi.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        문자단말.kwala("TX: "); 문자단말.수쓰기(Neteweke_selaodi.송신수);
        문자단말.kwala(" RX: "); 문자단말.수쓰기(Neteweke_selaodi.수신수);
        문자단말.kwala(" DROP: "); 문자단말.수쓰기(폐기수);
        문자단말.kwala("\n");
    }
}
