// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** tuli_thamani IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class Mtandao_Mpororo {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int Mtandao_barakoa = 0xffffff00; /* ip.conf:NETMASK */
    static final int kichanganishi_mtandao_thamani = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], 받은길이 = new int[4], 받은주소 = new int[4], 받은접속번호 = new int[4];
    static int[] 받은자료 = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, kitambulishi_thamani = 0, 폐기수 = 0;

    static int namba_kamili_16(int[] fremu_kielezo, int 위치) { return (fremu_kielezo[위치] << 8) | fremu_kielezo[위치 + 1]; }
    static int namba_kamili_32(int[] fremu_kielezo, int 위치) { return (namba_kamili_16(fremu_kielezo, 위치) << 16) | namba_kamili_16(fremu_kielezo, 위치 + 2); }
    static void 넣기16(int[] fremu_kielezo, int 위치, int thamani) { fremu_kielezo[위치] = (thamani >>> 8) & 255; fremu_kielezo[위치 + 1] = thamani & 255; }
    static void 넣기32(int[] fremu_kielezo, int 위치, int thamani) { 넣기16(fremu_kielezo, 위치, thamani >>> 16); 넣기16(fremu_kielezo, 위치 + 2, thamani); }
    static int 합(int[] fremu_kielezo, int endesha, int urefu_thamani, int thamani) {
        for (int kielezo = 0; kielezo < urefu_thamani; kielezo += 2)
            thamani += (fremu_kielezo[endesha + kielezo] << 8) | (kielezo + 1 < urefu_thamani ? fremu_kielezo[endesha + kielezo + 1] : 0);
        while ((thamani >>> 16) != 0) thamani = (thamani & 65535) + (thamani >>> 16);
        return thamani;
    }
    static int 가상머리합(int 출발, int 도착, int urefu_thamani) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + urefu_thamani;
    }

    static void Safi_Mchakato() {
        for (int kielezo = 0; kielezo < 4; kielezo++) {
            접속번호들[kielezo] = 0; 받은길이[kielezo] = -1; 받은주소[kielezo] = 0; 받은접속번호[kielezo] = 0;
        }
        for (int kielezo = 0; kielezo < 64; kielezo++) if (Mtandao_kiendeshaji.받기(입력틀) == 0) break;
    }
    static int kielezo(int kishiko_thamani) { return kishiko_thamani >= 3 && kishiko_thamani < 7 && 접속번호들[kishiko_thamani - 3] != 0 ? kishiko_thamani - 3 : -1; }
    static int unda(int namba_ya_kituo) {
        if (Mtandao_kiendeshaji.입출력기준주소 == 0) return -19;
        if (namba_ya_kituo < 0 || namba_ya_kituo > 65535) return -22;
        if (namba_ya_kituo != 0) for (int kielezo = 0; kielezo < 4; kielezo++) if (접속번호들[kielezo] == namba_ya_kituo) return -98;
        for (int kielezo = 0; kielezo < 4; kielezo++) if (접속번호들[kielezo] == 0) {
            if (namba_ya_kituo == 0) {
                namba_ya_kituo = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int mbele_thamani = 0; mbele_thamani < 4; mbele_thamani++) if (접속번호들[mbele_thamani] == namba_ya_kituo) 겹침 = true;
                    if (겹침) namba_ya_kituo++;
                }
            }
            접속번호들[kielezo] = namba_ya_kituo; 받은길이[kielezo] = -1;
            return kielezo + 3;
        }
        return -24;
    }
    static int funga(int kishiko_thamani) {
        int Sloti_ingizo = kielezo(kishiko_thamani);
        if (Sloti_ingizo < 0) return -9;
        접속번호들[Sloti_ingizo] = 0; 받은길이[Sloti_ingizo] = -1;
        return 0;
    }
    static int kompyuta_rika_anwani(int kishiko_thamani) { int Sloti_ingizo = kielezo(kishiko_thamani); return Sloti_ingizo < 0 ? -9 : 받은주소[Sloti_ingizo]; }
    static int kompyuta_rika_namba_ya_kituo(int kishiko_thamani) { int Sloti_ingizo = kielezo(kishiko_thamani); return Sloti_ingizo < 0 ? -9 : 받은접속번호[Sloti_ingizo]; }

    static void 바깥머리(int 종류, boolean kutangaza_thamani) {
        for (int kielezo = 0; kielezo < 6; kielezo++) {
            출력틀[kielezo] = kutangaza_thamani ? 255 : 찾은장치[kielezo];
            출력틀[6 + kielezo] = Mtandao_kiendeshaji.kifaa_anwani[kielezo];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void 주소요청(int fikio_thamani) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int kielezo = 0; kielezo < 6; kielezo++) {
            출력틀[22 + kielezo] = Mtandao_kiendeshaji.kifaa_anwani[kielezo]; 출력틀[32 + kielezo] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, fikio_thamani);
        Mtandao_kiendeshaji.tuma(출력틀, 42);
    }
    static void Mchakato_anwani(int urefu_thamani) {
        if (urefu_thamani < 42 || namba_kamili_16(입력틀, 14) != 1 || namba_kamili_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || namba_kamili_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = namba_kamili_16(입력틀, 20), kompyuta_rika_thamani = namba_kamili_32(입력틀, 28);
        if (종류 == 2 && kompyuta_rika_thamani == 찾을주소) {
            for (int kielezo = 0; kielezo < 6; kielezo++) {
                if (입력틀[6 + kielezo] != 입력틀[22 + kielezo] || 입력틀[32 + kielezo] != Mtandao_kiendeshaji.kifaa_anwani[kielezo]) return;
            }
            for (int kielezo = 0; kielezo < 6; kielezo++) 찾은장치[kielezo] = 입력틀[22 + kielezo];
            찾은주소 = kompyuta_rika_thamani;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int kielezo = 0; kielezo < 6; kielezo++) {
                출력틀[kielezo] = 입력틀[22 + kielezo]; 출력틀[32 + kielezo] = 입력틀[22 + kielezo];
                출력틀[22 + kielezo] = Mtandao_kiendeshaji.kifaa_anwani[kielezo];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, kompyuta_rika_thamani);
            Mtandao_kiendeshaji.tuma(출력틀, 42);
        }
    }

    static void Mchakato_fremu(int urefu_thamani) {
        if (urefu_thamani < 14 || urefu_thamani > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, kutangaza_thamani = true;
        for (int kielezo = 0; kielezo < 6; kielezo++) {
            if (입력틀[kielezo] != Mtandao_kiendeshaji.kifaa_anwani[kielezo]) 자기 = false;
            if (입력틀[kielezo] != 255) kutangaza_thamani = false;
        }
        if (!자기 && !kutangaza_thamani) return;
        if (namba_kamili_16(입력틀, 12) == 0x0806) { Mchakato_anwani(urefu_thamani); return; }
        if (namba_kamili_16(입력틀, 12) != 0x0800) return;
        if (urefu_thamani < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int kichwa_urefu = (입력틀[14] & 15) * 4, 전체길이 = namba_kamili_16(입력틀, 16);
        if (kichwa_urefu < 20 || kichwa_urefu > 60 || 전체길이 < kichwa_urefu + 8 || 전체길이 > urefu_thamani - 14
            || (namba_kamili_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || namba_kamili_32(입력틀, 30) != 내주소 || 합(입력틀, 14, kichwa_urefu, 0) != 65535) { 폐기수++; return; }
        int endesha = 14 + kichwa_urefu, data_urefu = namba_kamili_16(입력틀, endesha + 4);
        if (data_urefu < 8 || data_urefu != 전체길이 - kichwa_urefu || data_urefu > 1032) { 폐기수++; return; }
        int 출발 = namba_kamili_32(입력틀, 26);
        if (namba_kamili_16(입력틀, endesha + 6) != 0 && 합(입력틀, endesha, data_urefu, 가상머리합(출발, 내주소, data_urefu)) != 65535) {
            폐기수++; return;
        }
        int fikio_thamani = namba_kamili_16(입력틀, endesha + 2);
        for (int Sloti_ingizo = 0; Sloti_ingizo < 4; Sloti_ingizo++) if (접속번호들[Sloti_ingizo] != 0 && 접속번호들[Sloti_ingizo] == fikio_thamani) {
            if (받은길이[Sloti_ingizo] >= 0) { 폐기수++; return; }
            받은길이[Sloti_ingizo] = data_urefu - 8; 받은주소[Sloti_ingizo] = 출발; 받은접속번호[Sloti_ingizo] = namba_kamili_16(입력틀, endesha);
            for (int kielezo = 0; kielezo < data_urefu - 8; kielezo++) 받은자료[Sloti_ingizo * 1024 + kielezo] = 입력틀[endesha + 8 + kielezo];
            return;
        }
    }

    static void thibitisha() {
        for (int kielezo = 0; kielezo < 16; kielezo++) {
            int urefu_thamani = Mtandao_kiendeshaji.받기(입력틀);
            if (urefu_thamani == 0) return;
            Mchakato_fremu(urefu_thamani);
        }
    }
    static int gundua_anwani(int anwani) {
        if (anwani == 0 || anwani == -1 || (anwani >>> 28) >= 14 || (anwani >>> 24) == 127 || anwani == 내주소) return -101;
        int 다음 = (anwani & Mtandao_barakoa) == (내주소 & Mtandao_barakoa) ? anwani : kichanganishi_mtandao_thamani;
        if (다음 == 찾은주소) return 0;
        찾을주소 = 다음;
        int endesha = kifaa_thamani.밀리초(), 다음요청 = endesha;
        while (kifaa_thamani.밀리초() - endesha < 1000) {
            if (kifaa_thamani.밀리초() - 다음요청 >= 0) { 주소요청(다음); 다음요청 += 300; }
            thibitisha();
            if (찾은주소 == 다음) return 0;
            kifaa_thamani.잠시양보();
        }
        return -110;
    }
    static int tuma(int kishiko_thamani, int anwani, int namba_ya_kituo, int[] data, int urefu_thamani) {
        int Sloti_ingizo = kielezo(kishiko_thamani);
        if (Sloti_ingizo < 0) return -9;
        if (Mtandao_kiendeshaji.입출력기준주소 == 0) return -19;
        if (namba_ya_kituo < 1 || namba_ya_kituo > 65535 || urefu_thamani < 0 || urefu_thamani > 1024) return -22;
        int 결과 = gundua_anwani(anwani);
        if (결과 < 0) return 결과;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + urefu_thamani);
        넣기16(출력틀, 18, kitambulishi_thamani++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, anwani);
        넣기16(출력틀, 24, ~합(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[Sloti_ingizo]); 넣기16(출력틀, 36, namba_ya_kituo);
        넣기16(출력틀, 38, urefu_thamani + 8); 넣기16(출력틀, 40, 0);
        for (int kielezo = 0; kielezo < urefu_thamani; kielezo++) 출력틀[42 + kielezo] = data[kielezo] & 255;
        int jumla = (~합(출력틀, 34, urefu_thamani + 8, 가상머리합(내주소, anwani, urefu_thamani + 8))) & 65535;
        넣기16(출력틀, 40, jumla == 0 ? 65535 : jumla);
        결과 = Mtandao_kiendeshaji.tuma(출력틀, urefu_thamani + 42);
        return 결과 < 0 ? 결과 : urefu_thamani;
    }
    static int 받기(int kishiko_thamani, int[] data, int 용량, int 제한) {
        int Sloti_ingizo = kielezo(kishiko_thamani);
        if (Sloti_ingizo < 0) return -9;
        int endesha = kifaa_thamani.밀리초();
        while (true) {
            thibitisha();
            int urefu_thamani = 받은길이[Sloti_ingizo];
            if (urefu_thamani >= 0) {
                받은길이[Sloti_ingizo] = -1;
                if (urefu_thamani > 용량) return -90;
                for (int kielezo = 0; kielezo < urefu_thamani; kielezo++) data[kielezo] = 받은자료[Sloti_ingizo * 1024 + kielezo];
                return urefu_thamani;
            }
            if (제한 == 0) return -11;
            if (kifaa_thamani.밀리초() - endesha >= 제한) return -110;
            kifaa_thamani.잠시양보();
        }
    }
    static void hali_thamani() {
        문자단말.andika(Mtandao_kiendeshaji.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        문자단말.andika("TX: "); 문자단말.수쓰기(Mtandao_kiendeshaji.송신수);
        문자단말.andika(" RX: "); 문자단말.수쓰기(Mtandao_kiendeshaji.수신수);
        문자단말.andika(" DROP: "); 문자단말.수쓰기(폐기수);
        문자단말.andika("\n");
    }
}
