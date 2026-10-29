// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** estatiko_balio IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class sare_pila {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int sare_maskara = 0xffffff00; /* ip.conf:NETMASK */
    static final int atebide_balio = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], RECEIVED_luzera = new int[4], RECEIVED_helbide = new int[4], RECEIVED_ataka_zenbaki = new int[4];
    static int[] RECEIVED_datuak = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, identifikatzaile_balio = 0, 폐기수 = 0;

    static int osoko_zenbaki_16(int[] marko_INDIZE, int Posizioa) { return (marko_INDIZE[Posizioa] << 8) | marko_INDIZE[Posizioa + 1]; }
    static int osoko_zenbaki_32(int[] marko_INDIZE, int Posizioa) { return (osoko_zenbaki_16(marko_INDIZE, Posizioa) << 16) | osoko_zenbaki_16(marko_INDIZE, Posizioa + 2); }
    static void 넣기16(int[] marko_INDIZE, int Posizioa, int balio) { marko_INDIZE[Posizioa] = (balio >>> 8) & 255; marko_INDIZE[Posizioa + 1] = balio & 255; }
    static void 넣기32(int[] marko_INDIZE, int Posizioa, int balio) { 넣기16(marko_INDIZE, Posizioa, balio >>> 16); 넣기16(marko_INDIZE, Posizioa + 2, balio); }
    static int BATU_balio(int[] marko_INDIZE, int Exekutatu_2, int luzera_balio, int balio) {
        for (int INDIZE = 0; INDIZE < luzera_balio; INDIZE += 2)
            balio += (marko_INDIZE[Exekutatu_2 + INDIZE] << 8) | (INDIZE + 1 < luzera_balio ? marko_INDIZE[Exekutatu_2 + INDIZE + 1] : 0);
        while ((balio >>> 16) != 0) balio = (balio & 65535) + (balio >>> 16);
        return balio;
    }
    static int 가상머리합(int 출발, int 도착, int luzera_balio) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + luzera_balio;
    }

    static void GARBITU_prozesu() {
        for (int INDIZE = 0; INDIZE < 4; INDIZE++) {
            접속번호들[INDIZE] = 0; RECEIVED_luzera[INDIZE] = -1; RECEIVED_helbide[INDIZE] = 0; RECEIVED_ataka_zenbaki[INDIZE] = 0;
        }
        for (int INDIZE = 0; INDIZE < 64; INDIZE++) if (sare_kontrolatzaile.받기(입력틀) == 0) break;
    }
    static int INDIZE(int helduleku_balio) { return helduleku_balio >= 3 && helduleku_balio < 7 && 접속번호들[helduleku_balio - 3] != 0 ? helduleku_balio - 3 : -1; }
    static int Ireki(int ataka_zenbaki) {
        if (sare_kontrolatzaile.입출력기준주소 == 0) return -19;
        if (ataka_zenbaki < 0 || ataka_zenbaki > 65535) return -22;
        if (ataka_zenbaki != 0) for (int INDIZE = 0; INDIZE < 4; INDIZE++) if (접속번호들[INDIZE] == ataka_zenbaki) return -98;
        for (int INDIZE = 0; INDIZE < 4; INDIZE++) if (접속번호들[INDIZE] == 0) {
            if (ataka_zenbaki == 0) {
                ataka_zenbaki = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int aurrekoa_balio = 0; aurrekoa_balio < 4; aurrekoa_balio++) if (접속번호들[aurrekoa_balio] == ataka_zenbaki) 겹침 = true;
                    if (겹침) ataka_zenbaki++;
                }
            }
            접속번호들[INDIZE] = ataka_zenbaki; RECEIVED_luzera[INDIZE] = -1;
            return INDIZE + 3;
        }
        return -24;
    }
    static int Itxi(int helduleku_balio) {
        int 칸 = INDIZE(helduleku_balio);
        if (칸 < 0) return -9;
        접속번호들[칸] = 0; RECEIVED_luzera[칸] = -1;
        return 0;
    }
    static int pareko_helbide(int helduleku_balio) { int 칸 = INDIZE(helduleku_balio); return 칸 < 0 ? -9 : RECEIVED_helbide[칸]; }
    static int pareko_ataka_zenbaki(int helduleku_balio) { int 칸 = INDIZE(helduleku_balio); return 칸 < 0 ? -9 : RECEIVED_ataka_zenbaki[칸]; }

    static void 바깥머리(int 종류, boolean igorri_balio) {
        for (int INDIZE = 0; INDIZE < 6; INDIZE++) {
            출력틀[INDIZE] = igorri_balio ? 255 : 찾은장치[INDIZE];
            출력틀[6 + INDIZE] = sare_kontrolatzaile.gailu_helbide_856320c2[INDIZE];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void eskaera_helbide(int helburu_balio_a0fbc067) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int INDIZE = 0; INDIZE < 6; INDIZE++) {
            출력틀[22 + INDIZE] = sare_kontrolatzaile.gailu_helbide_856320c2[INDIZE]; 출력틀[32 + INDIZE] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, helburu_balio_a0fbc067);
        sare_kontrolatzaile.bidali(출력틀, 42);
    }
    static void prozesu_helbide(int luzera_balio) {
        if (luzera_balio < 42 || osoko_zenbaki_16(입력틀, 14) != 1 || osoko_zenbaki_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || osoko_zenbaki_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = osoko_zenbaki_16(입력틀, 20), pareko_balio = osoko_zenbaki_32(입력틀, 28);
        if (종류 == 2 && pareko_balio == 찾을주소) {
            for (int INDIZE = 0; INDIZE < 6; INDIZE++) {
                if (입력틀[6 + INDIZE] != 입력틀[22 + INDIZE] || 입력틀[32 + INDIZE] != sare_kontrolatzaile.gailu_helbide_856320c2[INDIZE]) return;
            }
            for (int INDIZE = 0; INDIZE < 6; INDIZE++) 찾은장치[INDIZE] = 입력틀[22 + INDIZE];
            찾은주소 = pareko_balio;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int INDIZE = 0; INDIZE < 6; INDIZE++) {
                출력틀[INDIZE] = 입력틀[22 + INDIZE]; 출력틀[32 + INDIZE] = 입력틀[22 + INDIZE];
                출력틀[22 + INDIZE] = sare_kontrolatzaile.gailu_helbide_856320c2[INDIZE];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, pareko_balio);
            sare_kontrolatzaile.bidali(출력틀, 42);
        }
    }

    static void prozesu_marko(int luzera_balio) {
        if (luzera_balio < 14 || luzera_balio > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, igorri_balio = true;
        for (int INDIZE = 0; INDIZE < 6; INDIZE++) {
            if (입력틀[INDIZE] != sare_kontrolatzaile.gailu_helbide_856320c2[INDIZE]) 자기 = false;
            if (입력틀[INDIZE] != 255) igorri_balio = false;
        }
        if (!자기 && !igorri_balio) return;
        if (osoko_zenbaki_16(입력틀, 12) == 0x0806) { prozesu_helbide(luzera_balio); return; }
        if (osoko_zenbaki_16(입력틀, 12) != 0x0800) return;
        if (luzera_balio < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int goiburu_luzera = (입력틀[14] & 15) * 4, 전체길이 = osoko_zenbaki_16(입력틀, 16);
        if (goiburu_luzera < 20 || goiburu_luzera > 60 || 전체길이 < goiburu_luzera + 8 || 전체길이 > luzera_balio - 14
            || (osoko_zenbaki_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || osoko_zenbaki_32(입력틀, 30) != 내주소 || BATU_balio(입력틀, 14, goiburu_luzera, 0) != 65535) { 폐기수++; return; }
        int Exekutatu_2 = 14 + goiburu_luzera, datuak_luzera = osoko_zenbaki_16(입력틀, Exekutatu_2 + 4);
        if (datuak_luzera < 8 || datuak_luzera != 전체길이 - goiburu_luzera || datuak_luzera > 1032) { 폐기수++; return; }
        int 출발 = osoko_zenbaki_32(입력틀, 26);
        if (osoko_zenbaki_16(입력틀, Exekutatu_2 + 6) != 0 && BATU_balio(입력틀, Exekutatu_2, datuak_luzera, 가상머리합(출발, 내주소, datuak_luzera)) != 65535) {
            폐기수++; return;
        }
        int helburu_balio_a0fbc067 = osoko_zenbaki_16(입력틀, Exekutatu_2 + 2);
        for (int 칸 = 0; 칸 < 4; 칸++) if (접속번호들[칸] != 0 && 접속번호들[칸] == helburu_balio_a0fbc067) {
            if (RECEIVED_luzera[칸] >= 0) { 폐기수++; return; }
            RECEIVED_luzera[칸] = datuak_luzera - 8; RECEIVED_helbide[칸] = 출발; RECEIVED_ataka_zenbaki[칸] = osoko_zenbaki_16(입력틀, Exekutatu_2);
            for (int INDIZE = 0; INDIZE < datuak_luzera - 8; INDIZE++) RECEIVED_datuak[칸 * 1024 + INDIZE] = 입력틀[Exekutatu_2 + 8 + INDIZE];
            return;
        }
    }

    static void egiaztatu() {
        for (int INDIZE = 0; INDIZE < 16; INDIZE++) {
            int luzera_balio = sare_kontrolatzaile.받기(입력틀);
            if (luzera_balio == 0) return;
            prozesu_marko(luzera_balio);
        }
    }
    static int Bilatu_helbide(int helbide) {
        if (helbide == 0 || helbide == -1 || (helbide >>> 28) >= 14 || (helbide >>> 24) == 127 || helbide == 내주소) return -101;
        int Hurrengoa_elementu = (helbide & sare_maskara) == (내주소 & sare_maskara) ? helbide : atebide_balio;
        if (Hurrengoa_elementu == 찾은주소) return 0;
        찾을주소 = Hurrengoa_elementu;
        int Exekutatu_2 = gailu_balio.밀리초(), Hurrengoa_eskaera = Exekutatu_2;
        while (gailu_balio.밀리초() - Exekutatu_2 < 1000) {
            if (gailu_balio.밀리초() - Hurrengoa_eskaera >= 0) { eskaera_helbide(Hurrengoa_elementu); Hurrengoa_eskaera += 300; }
            egiaztatu();
            if (찾은주소 == Hurrengoa_elementu) return 0;
            gailu_balio.잠시양보();
        }
        return -110;
    }
    static int bidali(int helduleku_balio, int helbide, int ataka_zenbaki, int[] datuak, int luzera_balio) {
        int 칸 = INDIZE(helduleku_balio);
        if (칸 < 0) return -9;
        if (sare_kontrolatzaile.입출력기준주소 == 0) return -19;
        if (ataka_zenbaki < 1 || ataka_zenbaki > 65535 || luzera_balio < 0 || luzera_balio > 1024) return -22;
        int EMAITZA = Bilatu_helbide(helbide);
        if (EMAITZA < 0) return EMAITZA;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + luzera_balio);
        넣기16(출력틀, 18, identifikatzaile_balio++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, helbide);
        넣기16(출력틀, 24, ~BATU_balio(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[칸]); 넣기16(출력틀, 36, ataka_zenbaki);
        넣기16(출력틀, 38, luzera_balio + 8); 넣기16(출력틀, 40, 0);
        for (int INDIZE = 0; INDIZE < luzera_balio; INDIZE++) 출력틀[42 + INDIZE] = datuak[INDIZE] & 255;
        int kontroleko_batura = (~BATU_balio(출력틀, 34, luzera_balio + 8, 가상머리합(내주소, helbide, luzera_balio + 8))) & 65535;
        넣기16(출력틀, 40, kontroleko_batura == 0 ? 65535 : kontroleko_batura);
        EMAITZA = sare_kontrolatzaile.bidali(출력틀, luzera_balio + 42);
        return EMAITZA < 0 ? EMAITZA : luzera_balio;
    }
    static int 받기(int helduleku_balio, int[] datuak, int ahalmen_balio, int 제한) {
        int 칸 = INDIZE(helduleku_balio);
        if (칸 < 0) return -9;
        int Exekutatu_2 = gailu_balio.밀리초();
        while (true) {
            egiaztatu();
            int luzera_balio = RECEIVED_luzera[칸];
            if (luzera_balio >= 0) {
                RECEIVED_luzera[칸] = -1;
                if (luzera_balio > ahalmen_balio) return -90;
                for (int INDIZE = 0; INDIZE < luzera_balio; INDIZE++) datuak[INDIZE] = RECEIVED_datuak[칸 * 1024 + INDIZE];
                return luzera_balio;
            }
            if (제한 == 0) return -11;
            if (gailu_balio.밀리초() - Exekutatu_2 >= 제한) return -110;
            gailu_balio.잠시양보();
        }
    }
    static void Egoera_balio() {
        SMS_Terminal.Idatzi(sare_kontrolatzaile.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Terminal.Idatzi("TX: "); SMS_Terminal.수쓰기(sare_kontrolatzaile.송신수);
        SMS_Terminal.Idatzi(" RX: "); SMS_Terminal.수쓰기(sare_kontrolatzaile.수신수);
        SMS_Terminal.Idatzi(" DROP: "); SMS_Terminal.수쓰기(폐기수);
        SMS_Terminal.Idatzi("\n");
    }
}
