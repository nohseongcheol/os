// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ya_go_se_fetoge_boleng_f430d3f5 IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class Netweke_kgoboko {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int Netweke_maseke = 0xffffff00; /* ip.conf:NETMASK */
    static final int tsela_ya_netweke_boleng = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], 받은길이 = new int[4], 받은주소 = new int[4], 받은접속번호 = new int[4];
    static int[] 받은자료 = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, sešupi_boleng = 0, 폐기수 = 0;

    static int palotlalo_16(int[] freime_lokela, int 위치) { return (freime_lokela[위치] << 8) | freime_lokela[위치 + 1]; }
    static int palotlalo_32(int[] freime_lokela, int 위치) { return (palotlalo_16(freime_lokela, 위치) << 16) | palotlalo_16(freime_lokela, 위치 + 2); }
    static void 넣기16(int[] freime_lokela, int 위치, int boleng) { freime_lokela[위치] = (boleng >>> 8) & 255; freime_lokela[위치 + 1] = boleng & 255; }
    static void 넣기32(int[] freime_lokela, int 위치, int boleng) { 넣기16(freime_lokela, 위치, boleng >>> 16); 넣기16(freime_lokela, 위치 + 2, boleng); }
    static int 합(int[] freime_lokela, int Diriša, int botelele_boleng, int boleng) {
        for (int lokela = 0; lokela < botelele_boleng; lokela += 2)
            boleng += (freime_lokela[Diriša + lokela] << 8) | (lokela + 1 < botelele_boleng ? freime_lokela[Diriša + lokela + 1] : 0);
        while ((boleng >>> 16) != 0) boleng = (boleng & 65535) + (boleng >>> 16);
        return boleng;
    }
    static int 가상머리합(int 출발, int 도착, int botelele_boleng) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + botelele_boleng;
    }

    static void 과정정리() {
        for (int lokela = 0; lokela < 4; lokela++) {
            접속번호들[lokela] = 0; 받은길이[lokela] = -1; 받은주소[lokela] = 0; 받은접속번호[lokela] = 0;
        }
        for (int lokela = 0; lokela < 64; lokela++) if (Netweke_teraeba.받기(입력틀) == 0) break;
    }
    static int lokela(int tshwaro_boleng) { return tshwaro_boleng >= 3 && tshwaro_boleng < 7 && 접속번호들[tshwaro_boleng - 3] != 0 ? tshwaro_boleng - 3 : -1; }
    static int Bula(int 접속번호) {
        if (Netweke_teraeba.입출력기준주소 == 0) return -19;
        if (접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 != 0) for (int lokela = 0; lokela < 4; lokela++) if (접속번호들[lokela] == 접속번호) return -98;
        for (int lokela = 0; lokela < 4; lokela++) if (접속번호들[lokela] == 0) {
            if (접속번호 == 0) {
                접속번호 = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int 앞 = 0; 앞 < 4; 앞++) if (접속번호들[앞] == 접속번호) 겹침 = true;
                    if (겹침) 접속번호++;
                }
            }
            접속번호들[lokela] = 접속번호; 받은길이[lokela] = -1;
            return lokela + 3;
        }
        return -24;
    }
    static int Tswalela(int tshwaro_boleng) {
        int sekgobana_go_tsenya_tshedimošo = lokela(tshwaro_boleng);
        if (sekgobana_go_tsenya_tshedimošo < 0) return -9;
        접속번호들[sekgobana_go_tsenya_tshedimošo] = 0; 받은길이[sekgobana_go_tsenya_tshedimošo] = -1;
        return 0;
    }
    static int sedirišwa_sa_legoro_le_tee_atrese(int tshwaro_boleng) { int sekgobana_go_tsenya_tshedimošo = lokela(tshwaro_boleng); return sekgobana_go_tsenya_tshedimošo < 0 ? -9 : 받은주소[sekgobana_go_tsenya_tshedimošo]; }
    static int 상대접속번호(int tshwaro_boleng) { int sekgobana_go_tsenya_tshedimošo = lokela(tshwaro_boleng); return sekgobana_go_tsenya_tshedimošo < 0 ? -9 : 받은접속번호[sekgobana_go_tsenya_tshedimošo]; }

    static void 바깥머리(int 종류, boolean kgašo_boleng) {
        for (int lokela = 0; lokela < 6; lokela++) {
            출력틀[lokela] = kgašo_boleng ? 255 : 찾은장치[lokela];
            출력틀[6 + lokela] = Netweke_teraeba.sedirišwa_atrese[lokela];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void 주소요청(int boyo_boleng) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int lokela = 0; lokela < 6; lokela++) {
            출력틀[22 + lokela] = Netweke_teraeba.sedirišwa_atrese[lokela]; 출력틀[32 + lokela] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, boyo_boleng);
        Netweke_teraeba.Romela(출력틀, 42);
    }
    static void tiragalo_atrese(int botelele_boleng) {
        if (botelele_boleng < 42 || palotlalo_16(입력틀, 14) != 1 || palotlalo_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || palotlalo_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = palotlalo_16(입력틀, 20), sedirišwa_sa_legoro_le_tee_boleng = palotlalo_32(입력틀, 28);
        if (종류 == 2 && sedirišwa_sa_legoro_le_tee_boleng == 찾을주소) {
            for (int lokela = 0; lokela < 6; lokela++) {
                if (입력틀[6 + lokela] != 입력틀[22 + lokela] || 입력틀[32 + lokela] != Netweke_teraeba.sedirišwa_atrese[lokela]) return;
            }
            for (int lokela = 0; lokela < 6; lokela++) 찾은장치[lokela] = 입력틀[22 + lokela];
            찾은주소 = sedirišwa_sa_legoro_le_tee_boleng;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int lokela = 0; lokela < 6; lokela++) {
                출력틀[lokela] = 입력틀[22 + lokela]; 출력틀[32 + lokela] = 입력틀[22 + lokela];
                출력틀[22 + lokela] = Netweke_teraeba.sedirišwa_atrese[lokela];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, sedirišwa_sa_legoro_le_tee_boleng);
            Netweke_teraeba.Romela(출력틀, 42);
        }
    }

    static void tiragalo_freime(int botelele_boleng) {
        if (botelele_boleng < 14 || botelele_boleng > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, kgašo_boleng = true;
        for (int lokela = 0; lokela < 6; lokela++) {
            if (입력틀[lokela] != Netweke_teraeba.sedirišwa_atrese[lokela]) 자기 = false;
            if (입력틀[lokela] != 255) kgašo_boleng = false;
        }
        if (!자기 && !kgašo_boleng) return;
        if (palotlalo_16(입력틀, 12) == 0x0806) { tiragalo_atrese(botelele_boleng); return; }
        if (palotlalo_16(입력틀, 12) != 0x0800) return;
        if (botelele_boleng < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int Hlogo_botelele = (입력틀[14] & 15) * 4, 전체길이 = palotlalo_16(입력틀, 16);
        if (Hlogo_botelele < 20 || Hlogo_botelele > 60 || 전체길이 < Hlogo_botelele + 8 || 전체길이 > botelele_boleng - 14
            || (palotlalo_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || palotlalo_32(입력틀, 30) != 내주소 || 합(입력틀, 14, Hlogo_botelele, 0) != 65535) { 폐기수++; return; }
        int Diriša = 14 + Hlogo_botelele, data_botelele = palotlalo_16(입력틀, Diriša + 4);
        if (data_botelele < 8 || data_botelele != 전체길이 - Hlogo_botelele || data_botelele > 1032) { 폐기수++; return; }
        int 출발 = palotlalo_32(입력틀, 26);
        if (palotlalo_16(입력틀, Diriša + 6) != 0 && 합(입력틀, Diriša, data_botelele, 가상머리합(출발, 내주소, data_botelele)) != 65535) {
            폐기수++; return;
        }
        int boyo_boleng = palotlalo_16(입력틀, Diriša + 2);
        for (int sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < 4; sekgobana_go_tsenya_tshedimošo++) if (접속번호들[sekgobana_go_tsenya_tshedimošo] != 0 && 접속번호들[sekgobana_go_tsenya_tshedimošo] == boyo_boleng) {
            if (받은길이[sekgobana_go_tsenya_tshedimošo] >= 0) { 폐기수++; return; }
            받은길이[sekgobana_go_tsenya_tshedimošo] = data_botelele - 8; 받은주소[sekgobana_go_tsenya_tshedimošo] = 출발; 받은접속번호[sekgobana_go_tsenya_tshedimošo] = palotlalo_16(입력틀, Diriša);
            for (int lokela = 0; lokela < data_botelele - 8; lokela++) 받은자료[sekgobana_go_tsenya_tshedimošo * 1024 + lokela] = 입력틀[Diriša + 8 + lokela];
            return;
        }
    }

    static void kgonthiša() {
        for (int lokela = 0; lokela < 16; lokela++) {
            int botelele_boleng = Netweke_teraeba.받기(입력틀);
            if (botelele_boleng == 0) return;
            tiragalo_freime(botelele_boleng);
        }
    }
    static int hwetša_atrese(int atrese) {
        if (atrese == 0 || atrese == -1 || (atrese >>> 28) >= 14 || (atrese >>> 24) == 127 || atrese == 내주소) return -101;
        int 다음 = (atrese & Netweke_maseke) == (내주소 & Netweke_maseke) ? atrese : tsela_ya_netweke_boleng;
        if (다음 == 찾은주소) return 0;
        찾을주소 = 다음;
        int Diriša = sedirišwa_boleng.밀리초(), 다음요청 = Diriša;
        while (sedirišwa_boleng.밀리초() - Diriša < 1000) {
            if (sedirišwa_boleng.밀리초() - 다음요청 >= 0) { 주소요청(다음); 다음요청 += 300; }
            kgonthiša();
            if (찾은주소 == 다음) return 0;
            sedirišwa_boleng.잠시양보();
        }
        return -110;
    }
    static int Romela(int tshwaro_boleng, int atrese, int 접속번호, int[] data, int botelele_boleng) {
        int sekgobana_go_tsenya_tshedimošo = lokela(tshwaro_boleng);
        if (sekgobana_go_tsenya_tshedimošo < 0) return -9;
        if (Netweke_teraeba.입출력기준주소 == 0) return -19;
        if (접속번호 < 1 || 접속번호 > 65535 || botelele_boleng < 0 || botelele_boleng > 1024) return -22;
        int 결과 = hwetša_atrese(atrese);
        if (결과 < 0) return 결과;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + botelele_boleng);
        넣기16(출력틀, 18, sešupi_boleng++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, atrese);
        넣기16(출력틀, 24, ~합(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[sekgobana_go_tsenya_tshedimošo]); 넣기16(출력틀, 36, 접속번호);
        넣기16(출력틀, 38, botelele_boleng + 8); 넣기16(출력틀, 40, 0);
        for (int lokela = 0; lokela < botelele_boleng; lokela++) 출력틀[42 + lokela] = data[lokela] & 255;
        int 검사합 = (~합(출력틀, 34, botelele_boleng + 8, 가상머리합(내주소, atrese, botelele_boleng + 8))) & 65535;
        넣기16(출력틀, 40, 검사합 == 0 ? 65535 : 검사합);
        결과 = Netweke_teraeba.Romela(출력틀, botelele_boleng + 42);
        return 결과 < 0 ? 결과 : botelele_boleng;
    }
    static int 받기(int tshwaro_boleng, int[] data, int 용량, int 제한) {
        int sekgobana_go_tsenya_tshedimošo = lokela(tshwaro_boleng);
        if (sekgobana_go_tsenya_tshedimošo < 0) return -9;
        int Diriša = sedirišwa_boleng.밀리초();
        while (true) {
            kgonthiša();
            int botelele_boleng = 받은길이[sekgobana_go_tsenya_tshedimošo];
            if (botelele_boleng >= 0) {
                받은길이[sekgobana_go_tsenya_tshedimošo] = -1;
                if (botelele_boleng > 용량) return -90;
                for (int lokela = 0; lokela < botelele_boleng; lokela++) data[lokela] = 받은자료[sekgobana_go_tsenya_tshedimošo * 1024 + lokela];
                return botelele_boleng;
            }
            if (제한 == 0) return -11;
            if (sedirišwa_boleng.밀리초() - Diriša >= 제한) return -110;
            sedirišwa_boleng.잠시양보();
        }
    }
    static void boemo_boleng() {
        문자단말.Ngwala(Netweke_teraeba.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        문자단말.Ngwala("TX: "); 문자단말.수쓰기(Netweke_teraeba.송신수);
        문자단말.Ngwala(" RX: "); 문자단말.수쓰기(Netweke_teraeba.수신수);
        문자단말.Ngwala(" DROP: "); 문자단말.수쓰기(폐기수);
        문자단말.Ngwala("\n");
    }
}
