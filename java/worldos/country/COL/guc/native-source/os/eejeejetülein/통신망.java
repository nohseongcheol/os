// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jimatüsü_ajutuu IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class 통신망 {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int kusu_o_upünaa_utajana = 0xffffff00; /* ip.conf:NETMASK */
    static final int miicho_u_a_ttaalee_ajutuu = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], 받은길이 = new int[4], 받은주소 = new int[4], 받은접속번호 = new int[4];
    static int[] 받은자료 = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, 식별자 = 0, 폐기수 = 0;

    static int waneepiasü_16(int[] otpünaa_ee_iyatialujuna, int 위치) { return (otpünaa_ee_iyatialujuna[위치] << 8) | otpünaa_ee_iyatialujuna[위치 + 1]; }
    static int waneepiasü_32(int[] otpünaa_ee_iyatialujuna, int 위치) { return (waneepiasü_16(otpünaa_ee_iyatialujuna, 위치) << 16) | waneepiasü_16(otpünaa_ee_iyatialujuna, 위치 + 2); }
    static void 넣기16(int[] otpünaa_ee_iyatialujuna, int 위치, int ajutuu) { otpünaa_ee_iyatialujuna[위치] = (ajutuu >>> 8) & 255; otpünaa_ee_iyatialujuna[위치 + 1] = ajutuu & 255; }
    static void 넣기32(int[] otpünaa_ee_iyatialujuna, int 위치, int ajutuu) { 넣기16(otpünaa_ee_iyatialujuna, 위치, ajutuu >>> 16); 넣기16(otpünaa_ee_iyatialujuna, 위치 + 2, ajutuu); }
    static int 합(int[] otpünaa_ee_iyatialujuna, int 시작, int akaliaa_ajutuu, int ajutuu) {
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < akaliaa_ajutuu; ee_iyatialujuna += 2)
            ajutuu += (otpünaa_ee_iyatialujuna[시작 + ee_iyatialujuna] << 8) | (ee_iyatialujuna + 1 < akaliaa_ajutuu ? otpünaa_ee_iyatialujuna[시작 + ee_iyatialujuna + 1] : 0);
        while ((ajutuu >>> 16) != 0) ajutuu = (ajutuu & 65535) + (ajutuu >>> 16);
        return ajutuu;
    }
    static int 가상머리합(int 출발, int 도착, int akaliaa_ajutuu) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + akaliaa_ajutuu;
    }

    static void 과정정리() {
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 4; ee_iyatialujuna++) {
            접속번호들[ee_iyatialujuna] = 0; 받은길이[ee_iyatialujuna] = -1; 받은주소[ee_iyatialujuna] = 0; 받은접속번호[ee_iyatialujuna] = 0;
        }
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 64; ee_iyatialujuna++) if (kusu_aa_inmajülü.받기(입력틀) == 0) break;
    }
    static int ee_iyatialujuna(int aapaaya_ajutuu) { return aapaaya_ajutuu >= 3 && aapaaya_ajutuu < 7 && 접속번호들[aapaaya_ajutuu - 3] != 0 ? aapaaya_ajutuu - 3 : -1; }
    static int 열기(int 접속번호) {
        if (kusu_aa_inmajülü.입출력기준주소 == 0) return -19;
        if (접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 != 0) for (int ee_iyatialujuna = 0; ee_iyatialujuna < 4; ee_iyatialujuna++) if (접속번호들[ee_iyatialujuna] == 접속번호) return -98;
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 4; ee_iyatialujuna++) if (접속번호들[ee_iyatialujuna] == 0) {
            if (접속번호 == 0) {
                접속번호 = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int 앞 = 0; 앞 < 4; 앞++) if (접속번호들[앞] == 접속번호) 겹침 = true;
                    if (겹침) 접속번호++;
                }
            }
            접속번호들[ee_iyatialujuna] = 접속번호; 받은길이[ee_iyatialujuna] = -1;
            return ee_iyatialujuna + 3;
        }
        return -24;
    }
    static int asürülaa(int aapaaya_ajutuu) {
        int 칸 = ee_iyatialujuna(aapaaya_ajutuu);
        if (칸 < 0) return -9;
        접속번호들[칸] = 0; 받은길이[칸] = -1;
        return 0;
    }
    static int wanaawasü_ejepüsee(int aapaaya_ajutuu) { int 칸 = ee_iyatialujuna(aapaaya_ajutuu); return 칸 < 0 ? -9 : 받은주소[칸]; }
    static int 상대접속번호(int aapaaya_ajutuu) { int 칸 = ee_iyatialujuna(aapaaya_ajutuu); return 칸 < 0 ? -9 : 받은접속번호[칸]; }

    static void 바깥머리(int 종류, boolean 방송) {
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 6; ee_iyatialujuna++) {
            출력틀[ee_iyatialujuna] = 방송 ? 255 : 찾은장치[ee_iyatialujuna];
            출력틀[6 + ee_iyatialujuna] = kusu_aa_inmajülü.serulaalü_ejepüsee[ee_iyatialujuna];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void 주소요청(int jalamüinjatü_ajutuu) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 6; ee_iyatialujuna++) {
            출력틀[22 + ee_iyatialujuna] = kusu_aa_inmajülü.serulaalü_ejepüsee[ee_iyatialujuna]; 출력틀[32 + ee_iyatialujuna] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, jalamüinjatü_ajutuu);
        kusu_aa_inmajülü.ajütaa(출력틀, 42);
    }
    static void 주소처리(int akaliaa_ajutuu) {
        if (akaliaa_ajutuu < 42 || waneepiasü_16(입력틀, 14) != 1 || waneepiasü_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || waneepiasü_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = waneepiasü_16(입력틀, 20), wanaawasü_ajutuu = waneepiasü_32(입력틀, 28);
        if (종류 == 2 && wanaawasü_ajutuu == 찾을주소) {
            for (int ee_iyatialujuna = 0; ee_iyatialujuna < 6; ee_iyatialujuna++) {
                if (입력틀[6 + ee_iyatialujuna] != 입력틀[22 + ee_iyatialujuna] || 입력틀[32 + ee_iyatialujuna] != kusu_aa_inmajülü.serulaalü_ejepüsee[ee_iyatialujuna]) return;
            }
            for (int ee_iyatialujuna = 0; ee_iyatialujuna < 6; ee_iyatialujuna++) 찾은장치[ee_iyatialujuna] = 입력틀[22 + ee_iyatialujuna];
            찾은주소 = wanaawasü_ajutuu;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int ee_iyatialujuna = 0; ee_iyatialujuna < 6; ee_iyatialujuna++) {
                출력틀[ee_iyatialujuna] = 입력틀[22 + ee_iyatialujuna]; 출력틀[32 + ee_iyatialujuna] = 입력틀[22 + ee_iyatialujuna];
                출력틀[22 + ee_iyatialujuna] = kusu_aa_inmajülü.serulaalü_ejepüsee[ee_iyatialujuna];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, wanaawasü_ajutuu);
            kusu_aa_inmajülü.ajütaa(출력틀, 42);
        }
    }

    static void 틀처리(int akaliaa_ajutuu) {
        if (akaliaa_ajutuu < 14 || akaliaa_ajutuu > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, 방송 = true;
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 6; ee_iyatialujuna++) {
            if (입력틀[ee_iyatialujuna] != kusu_aa_inmajülü.serulaalü_ejepüsee[ee_iyatialujuna]) 자기 = false;
            if (입력틀[ee_iyatialujuna] != 255) 방송 = false;
        }
        if (!자기 && !방송) return;
        if (waneepiasü_16(입력틀, 12) == 0x0806) { 주소처리(akaliaa_ajutuu); return; }
        if (waneepiasü_16(입력틀, 12) != 0x0800) return;
        if (akaliaa_ajutuu < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int o_ttiakii_akaliaa = (입력틀[14] & 15) * 4, 전체길이 = waneepiasü_16(입력틀, 16);
        if (o_ttiakii_akaliaa < 20 || o_ttiakii_akaliaa > 60 || 전체길이 < o_ttiakii_akaliaa + 8 || 전체길이 > akaliaa_ajutuu - 14
            || (waneepiasü_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || waneepiasü_32(입력틀, 30) != 내주소 || 합(입력틀, 14, o_ttiakii_akaliaa, 0) != 65535) { 폐기수++; return; }
        int 시작 = 14 + o_ttiakii_akaliaa, atijaaya_akaliaa = waneepiasü_16(입력틀, 시작 + 4);
        if (atijaaya_akaliaa < 8 || atijaaya_akaliaa != 전체길이 - o_ttiakii_akaliaa || atijaaya_akaliaa > 1032) { 폐기수++; return; }
        int 출발 = waneepiasü_32(입력틀, 26);
        if (waneepiasü_16(입력틀, 시작 + 6) != 0 && 합(입력틀, 시작, atijaaya_akaliaa, 가상머리합(출발, 내주소, atijaaya_akaliaa)) != 65535) {
            폐기수++; return;
        }
        int jalamüinjatü_ajutuu = waneepiasü_16(입력틀, 시작 + 2);
        for (int 칸 = 0; 칸 < 4; 칸++) if (접속번호들[칸] != 0 && 접속번호들[칸] == jalamüinjatü_ajutuu) {
            if (받은길이[칸] >= 0) { 폐기수++; return; }
            받은길이[칸] = atijaaya_akaliaa - 8; 받은주소[칸] = 출발; 받은접속번호[칸] = waneepiasü_16(입력틀, 시작);
            for (int ee_iyatialujuna = 0; ee_iyatialujuna < atijaaya_akaliaa - 8; ee_iyatialujuna++) 받은자료[칸 * 1024 + ee_iyatialujuna] = 입력틀[시작 + 8 + ee_iyatialujuna];
            return;
        }
    }

    static void 확인() {
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 16; ee_iyatialujuna++) {
            int akaliaa_ajutuu = kusu_aa_inmajülü.받기(입력틀);
            if (akaliaa_ajutuu == 0) return;
            틀처리(akaliaa_ajutuu);
        }
    }
    static int 주소찾기(int ejepüsee) {
        if (ejepüsee == 0 || ejepüsee == -1 || (ejepüsee >>> 28) >= 14 || (ejepüsee >>> 24) == 127 || ejepüsee == 내주소) return -101;
        int 다음 = (ejepüsee & kusu_o_upünaa_utajana) == (내주소 & kusu_o_upünaa_utajana) ? ejepüsee : miicho_u_a_ttaalee_ajutuu;
        if (다음 == 찾은주소) return 0;
        찾을주소 = 다음;
        int 시작 = serulaalü_ajutuu.밀리초(), 다음요청 = 시작;
        while (serulaalü_ajutuu.밀리초() - 시작 < 1000) {
            if (serulaalü_ajutuu.밀리초() - 다음요청 >= 0) { 주소요청(다음); 다음요청 += 300; }
            확인();
            if (찾은주소 == 다음) return 0;
            serulaalü_ajutuu.잠시양보();
        }
        return -110;
    }
    static int ajütaa(int aapaaya_ajutuu, int ejepüsee, int 접속번호, int[] atijaaya, int akaliaa_ajutuu) {
        int 칸 = ee_iyatialujuna(aapaaya_ajutuu);
        if (칸 < 0) return -9;
        if (kusu_aa_inmajülü.입출력기준주소 == 0) return -19;
        if (접속번호 < 1 || 접속번호 > 65535 || akaliaa_ajutuu < 0 || akaliaa_ajutuu > 1024) return -22;
        int 결과 = 주소찾기(ejepüsee);
        if (결과 < 0) return 결과;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + akaliaa_ajutuu);
        넣기16(출력틀, 18, 식별자++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, ejepüsee);
        넣기16(출력틀, 24, ~합(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[칸]); 넣기16(출력틀, 36, 접속번호);
        넣기16(출력틀, 38, akaliaa_ajutuu + 8); 넣기16(출력틀, 40, 0);
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < akaliaa_ajutuu; ee_iyatialujuna++) 출력틀[42 + ee_iyatialujuna] = atijaaya[ee_iyatialujuna] & 255;
        int 검사합 = (~합(출력틀, 34, akaliaa_ajutuu + 8, 가상머리합(내주소, ejepüsee, akaliaa_ajutuu + 8))) & 65535;
        넣기16(출력틀, 40, 검사합 == 0 ? 65535 : 검사합);
        결과 = kusu_aa_inmajülü.ajütaa(출력틀, akaliaa_ajutuu + 42);
        return 결과 < 0 ? 결과 : akaliaa_ajutuu;
    }
    static int 받기(int aapaaya_ajutuu, int[] atijaaya, int 용량, int 제한) {
        int 칸 = ee_iyatialujuna(aapaaya_ajutuu);
        if (칸 < 0) return -9;
        int 시작 = serulaalü_ajutuu.밀리초();
        while (true) {
            확인();
            int akaliaa_ajutuu = 받은길이[칸];
            if (akaliaa_ajutuu >= 0) {
                받은길이[칸] = -1;
                if (akaliaa_ajutuu > 용량) return -90;
                for (int ee_iyatialujuna = 0; ee_iyatialujuna < akaliaa_ajutuu; ee_iyatialujuna++) atijaaya[ee_iyatialujuna] = 받은자료[칸 * 1024 + ee_iyatialujuna];
                return akaliaa_ajutuu;
            }
            if (제한 == 0) return -11;
            if (serulaalü_ajutuu.밀리초() - 시작 >= 제한) return -110;
            serulaalü_ajutuu.잠시양보();
        }
    }
    static void jamakua_iparülein_ajutuu() {
        문자단말.ashajaa(kusu_aa_inmajülü.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        문자단말.ashajaa("TX: "); 문자단말.수쓰기(kusu_aa_inmajülü.송신수);
        문자단말.ashajaa(" RX: "); 문자단말.수쓰기(kusu_aa_inmajülü.수신수);
        문자단말.ashajaa(" DROP: "); 문자단말.수쓰기(폐기수);
        문자단말.ashajaa("\n");
    }
}
