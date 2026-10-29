// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** kitayega_agaciro IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class Urusobemiyoboro_Ikirundo {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int Urusobemiyoboro_masiki = 0xffffff00; /* ip.conf:NETMASK */
    static final int muhuzaporotokore_agaciro = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], 받은길이 = new int[4], 받은주소 = new int[4], 받은접속번호 = new int[4];
    static int[] 받은자료 = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, indanga_agaciro = 0, 폐기수 = 0;

    static int umubare_wuzuye_16(int[] ikadiri_umugerekashakiro, int 위치) { return (ikadiri_umugerekashakiro[위치] << 8) | ikadiri_umugerekashakiro[위치 + 1]; }
    static int umubare_wuzuye_32(int[] ikadiri_umugerekashakiro, int 위치) { return (umubare_wuzuye_16(ikadiri_umugerekashakiro, 위치) << 16) | umubare_wuzuye_16(ikadiri_umugerekashakiro, 위치 + 2); }
    static void 넣기16(int[] ikadiri_umugerekashakiro, int 위치, int agaciro) { ikadiri_umugerekashakiro[위치] = (agaciro >>> 8) & 255; ikadiri_umugerekashakiro[위치 + 1] = agaciro & 255; }
    static void 넣기32(int[] ikadiri_umugerekashakiro, int 위치, int agaciro) { 넣기16(ikadiri_umugerekashakiro, 위치, agaciro >>> 16); 넣기16(ikadiri_umugerekashakiro, 위치 + 2, agaciro); }
    static int 합(int[] ikadiri_umugerekashakiro, int ihuriro, int uburebure_agaciro, int agaciro) {
        for (int umugerekashakiro = 0; umugerekashakiro < uburebure_agaciro; umugerekashakiro += 2)
            agaciro += (ikadiri_umugerekashakiro[ihuriro + umugerekashakiro] << 8) | (umugerekashakiro + 1 < uburebure_agaciro ? ikadiri_umugerekashakiro[ihuriro + umugerekashakiro + 1] : 0);
        while ((agaciro >>> 16) != 0) agaciro = (agaciro & 65535) + (agaciro >>> 16);
        return agaciro;
    }
    static int 가상머리합(int 출발, int 도착, int uburebure_agaciro) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + uburebure_agaciro;
    }

    static void 과정정리() {
        for (int umugerekashakiro = 0; umugerekashakiro < 4; umugerekashakiro++) {
            접속번호들[umugerekashakiro] = 0; 받은길이[umugerekashakiro] = -1; 받은주소[umugerekashakiro] = 0; 받은접속번호[umugerekashakiro] = 0;
        }
        for (int umugerekashakiro = 0; umugerekashakiro < 64; umugerekashakiro++) if (Urusobemiyoboro_mukoresha.받기(입력틀) == 0) break;
    }
    static int umugerekashakiro(int umukondo_agaciro) { return umukondo_agaciro >= 3 && umukondo_agaciro < 7 && 접속번호들[umukondo_agaciro - 3] != 0 ? umukondo_agaciro - 3 : -1; }
    static int Gufungura(int 접속번호) {
        if (Urusobemiyoboro_mukoresha.입출력기준주소 == 0) return -19;
        if (접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 != 0) for (int umugerekashakiro = 0; umugerekashakiro < 4; umugerekashakiro++) if (접속번호들[umugerekashakiro] == 접속번호) return -98;
        for (int umugerekashakiro = 0; umugerekashakiro < 4; umugerekashakiro++) if (접속번호들[umugerekashakiro] == 0) {
            if (접속번호 == 0) {
                접속번호 = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int 앞 = 0; 앞 < 4; 앞++) if (접속번호들[앞] == 접속번호) 겹침 = true;
                    if (겹침) 접속번호++;
                }
            }
            접속번호들[umugerekashakiro] = 접속번호; 받은길이[umugerekashakiro] = -1;
            return umugerekashakiro + 3;
        }
        return -24;
    }
    static int Gufunga(int umukondo_agaciro) {
        int umwanya_icyinjizwa = umugerekashakiro(umukondo_agaciro);
        if (umwanya_icyinjizwa < 0) return -9;
        접속번호들[umwanya_icyinjizwa] = 0; 받은길이[umwanya_icyinjizwa] = -1;
        return 0;
    }
    static int Mugenzi_aderesi(int umukondo_agaciro) { int umwanya_icyinjizwa = umugerekashakiro(umukondo_agaciro); return umwanya_icyinjizwa < 0 ? -9 : 받은주소[umwanya_icyinjizwa]; }
    static int 상대접속번호(int umukondo_agaciro) { int umwanya_icyinjizwa = umugerekashakiro(umukondo_agaciro); return umwanya_icyinjizwa < 0 ? -9 : 받은접속번호[umwanya_icyinjizwa]; }

    static void 바깥머리(int 종류, boolean 방송) {
        for (int umugerekashakiro = 0; umugerekashakiro < 6; umugerekashakiro++) {
            출력틀[umugerekashakiro] = 방송 ? 255 : 찾은장치[umugerekashakiro];
            출력틀[6 + umugerekashakiro] = Urusobemiyoboro_mukoresha.igendanwa_aderesi[umugerekashakiro];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void 주소요청(int aho_ijya_agaciro) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int umugerekashakiro = 0; umugerekashakiro < 6; umugerekashakiro++) {
            출력틀[22 + umugerekashakiro] = Urusobemiyoboro_mukoresha.igendanwa_aderesi[umugerekashakiro]; 출력틀[32 + umugerekashakiro] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, aho_ijya_agaciro);
        Urusobemiyoboro_mukoresha.kohereza(출력틀, 42);
    }
    static void Inzira_aderesi(int uburebure_agaciro) {
        if (uburebure_agaciro < 42 || umubare_wuzuye_16(입력틀, 14) != 1 || umubare_wuzuye_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || umubare_wuzuye_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = umubare_wuzuye_16(입력틀, 20), Mugenzi_agaciro = umubare_wuzuye_32(입력틀, 28);
        if (종류 == 2 && Mugenzi_agaciro == 찾을주소) {
            for (int umugerekashakiro = 0; umugerekashakiro < 6; umugerekashakiro++) {
                if (입력틀[6 + umugerekashakiro] != 입력틀[22 + umugerekashakiro] || 입력틀[32 + umugerekashakiro] != Urusobemiyoboro_mukoresha.igendanwa_aderesi[umugerekashakiro]) return;
            }
            for (int umugerekashakiro = 0; umugerekashakiro < 6; umugerekashakiro++) 찾은장치[umugerekashakiro] = 입력틀[22 + umugerekashakiro];
            찾은주소 = Mugenzi_agaciro;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int umugerekashakiro = 0; umugerekashakiro < 6; umugerekashakiro++) {
                출력틀[umugerekashakiro] = 입력틀[22 + umugerekashakiro]; 출력틀[32 + umugerekashakiro] = 입력틀[22 + umugerekashakiro];
                출력틀[22 + umugerekashakiro] = Urusobemiyoboro_mukoresha.igendanwa_aderesi[umugerekashakiro];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, Mugenzi_agaciro);
            Urusobemiyoboro_mukoresha.kohereza(출력틀, 42);
        }
    }

    static void Inzira_ikadiri(int uburebure_agaciro) {
        if (uburebure_agaciro < 14 || uburebure_agaciro > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, 방송 = true;
        for (int umugerekashakiro = 0; umugerekashakiro < 6; umugerekashakiro++) {
            if (입력틀[umugerekashakiro] != Urusobemiyoboro_mukoresha.igendanwa_aderesi[umugerekashakiro]) 자기 = false;
            if (입력틀[umugerekashakiro] != 255) 방송 = false;
        }
        if (!자기 && !방송) return;
        if (umubare_wuzuye_16(입력틀, 12) == 0x0806) { Inzira_aderesi(uburebure_agaciro); return; }
        if (umubare_wuzuye_16(입력틀, 12) != 0x0800) return;
        if (uburebure_agaciro < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int Umutwengaruka_uburebure = (입력틀[14] & 15) * 4, 전체길이 = umubare_wuzuye_16(입력틀, 16);
        if (Umutwengaruka_uburebure < 20 || Umutwengaruka_uburebure > 60 || 전체길이 < Umutwengaruka_uburebure + 8 || 전체길이 > uburebure_agaciro - 14
            || (umubare_wuzuye_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || umubare_wuzuye_32(입력틀, 30) != 내주소 || 합(입력틀, 14, Umutwengaruka_uburebure, 0) != 65535) { 폐기수++; return; }
        int ihuriro = 14 + Umutwengaruka_uburebure, amakurushingiro_uburebure = umubare_wuzuye_16(입력틀, ihuriro + 4);
        if (amakurushingiro_uburebure < 8 || amakurushingiro_uburebure != 전체길이 - Umutwengaruka_uburebure || amakurushingiro_uburebure > 1032) { 폐기수++; return; }
        int 출발 = umubare_wuzuye_32(입력틀, 26);
        if (umubare_wuzuye_16(입력틀, ihuriro + 6) != 0 && 합(입력틀, ihuriro, amakurushingiro_uburebure, 가상머리합(출발, 내주소, amakurushingiro_uburebure)) != 65535) {
            폐기수++; return;
        }
        int aho_ijya_agaciro = umubare_wuzuye_16(입력틀, ihuriro + 2);
        for (int umwanya_icyinjizwa = 0; umwanya_icyinjizwa < 4; umwanya_icyinjizwa++) if (접속번호들[umwanya_icyinjizwa] != 0 && 접속번호들[umwanya_icyinjizwa] == aho_ijya_agaciro) {
            if (받은길이[umwanya_icyinjizwa] >= 0) { 폐기수++; return; }
            받은길이[umwanya_icyinjizwa] = amakurushingiro_uburebure - 8; 받은주소[umwanya_icyinjizwa] = 출발; 받은접속번호[umwanya_icyinjizwa] = umubare_wuzuye_16(입력틀, ihuriro);
            for (int umugerekashakiro = 0; umugerekashakiro < amakurushingiro_uburebure - 8; umugerekashakiro++) 받은자료[umwanya_icyinjizwa * 1024 + umugerekashakiro] = 입력틀[ihuriro + 8 + umugerekashakiro];
            return;
        }
    }

    static void gusuzuma() {
        for (int umugerekashakiro = 0; umugerekashakiro < 16; umugerekashakiro++) {
            int uburebure_agaciro = Urusobemiyoboro_mukoresha.받기(입력틀);
            if (uburebure_agaciro == 0) return;
            Inzira_ikadiri(uburebure_agaciro);
        }
    }
    static int gushaka_aderesi(int aderesi) {
        if (aderesi == 0 || aderesi == -1 || (aderesi >>> 28) >= 14 || (aderesi >>> 24) == 127 || aderesi == 내주소) return -101;
        int 다음 = (aderesi & Urusobemiyoboro_masiki) == (내주소 & Urusobemiyoboro_masiki) ? aderesi : muhuzaporotokore_agaciro;
        if (다음 == 찾은주소) return 0;
        찾을주소 = 다음;
        int ihuriro = igendanwa_agaciro.밀리초(), 다음요청 = ihuriro;
        while (igendanwa_agaciro.밀리초() - ihuriro < 1000) {
            if (igendanwa_agaciro.밀리초() - 다음요청 >= 0) { 주소요청(다음); 다음요청 += 300; }
            gusuzuma();
            if (찾은주소 == 다음) return 0;
            igendanwa_agaciro.잠시양보();
        }
        return -110;
    }
    static int kohereza(int umukondo_agaciro, int aderesi, int 접속번호, int[] amakurushingiro, int uburebure_agaciro) {
        int umwanya_icyinjizwa = umugerekashakiro(umukondo_agaciro);
        if (umwanya_icyinjizwa < 0) return -9;
        if (Urusobemiyoboro_mukoresha.입출력기준주소 == 0) return -19;
        if (접속번호 < 1 || 접속번호 > 65535 || uburebure_agaciro < 0 || uburebure_agaciro > 1024) return -22;
        int 결과 = gushaka_aderesi(aderesi);
        if (결과 < 0) return 결과;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + uburebure_agaciro);
        넣기16(출력틀, 18, indanga_agaciro++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, aderesi);
        넣기16(출력틀, 24, ~합(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[umwanya_icyinjizwa]); 넣기16(출력틀, 36, 접속번호);
        넣기16(출력틀, 38, uburebure_agaciro + 8); 넣기16(출력틀, 40, 0);
        for (int umugerekashakiro = 0; umugerekashakiro < uburebure_agaciro; umugerekashakiro++) 출력틀[42 + umugerekashakiro] = amakurushingiro[umugerekashakiro] & 255;
        int 검사합 = (~합(출력틀, 34, uburebure_agaciro + 8, 가상머리합(내주소, aderesi, uburebure_agaciro + 8))) & 65535;
        넣기16(출력틀, 40, 검사합 == 0 ? 65535 : 검사합);
        결과 = Urusobemiyoboro_mukoresha.kohereza(출력틀, uburebure_agaciro + 42);
        return 결과 < 0 ? 결과 : uburebure_agaciro;
    }
    static int 받기(int umukondo_agaciro, int[] amakurushingiro, int 용량, int 제한) {
        int umwanya_icyinjizwa = umugerekashakiro(umukondo_agaciro);
        if (umwanya_icyinjizwa < 0) return -9;
        int ihuriro = igendanwa_agaciro.밀리초();
        while (true) {
            gusuzuma();
            int uburebure_agaciro = 받은길이[umwanya_icyinjizwa];
            if (uburebure_agaciro >= 0) {
                받은길이[umwanya_icyinjizwa] = -1;
                if (uburebure_agaciro > 용량) return -90;
                for (int umugerekashakiro = 0; umugerekashakiro < uburebure_agaciro; umugerekashakiro++) amakurushingiro[umugerekashakiro] = 받은자료[umwanya_icyinjizwa * 1024 + umugerekashakiro];
                return uburebure_agaciro;
            }
            if (제한 == 0) return -11;
            if (igendanwa_agaciro.밀리초() - ihuriro >= 제한) return -110;
            igendanwa_agaciro.잠시양보();
        }
    }
    static void imimerere_agaciro() {
        문자단말.kwandika(Urusobemiyoboro_mukoresha.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        문자단말.kwandika("TX: "); 문자단말.수쓰기(Urusobemiyoboro_mukoresha.송신수);
        문자단말.kwandika(" RX: "); 문자단말.수쓰기(Urusobemiyoboro_mukoresha.수신수);
        문자단말.kwandika(" DROP: "); 문자단말.수쓰기(폐기수);
        문자단말.kwandika("\n");
    }
}
