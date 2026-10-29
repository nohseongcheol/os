// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Soppeekoodi_xëyma IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class mbaal_Tegalo {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int mbaal_muuraay = 0xffffff00; /* ip.conf:NETMASK */
    static final int bunt_xëyma = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], 받은길이 = new int[4], 받은주소 = new int[4], 받은접속번호 = new int[4];
    static int[] 받은자료 = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, raññeekaay_xëyma = 0, 폐기수 = 0;

    static int lëmm_16(int[] kadar_àlluwa_tur, int 위치) { return (kadar_àlluwa_tur[위치] << 8) | kadar_àlluwa_tur[위치 + 1]; }
    static int lëmm_32(int[] kadar_àlluwa_tur, int 위치) { return (lëmm_16(kadar_àlluwa_tur, 위치) << 16) | lëmm_16(kadar_àlluwa_tur, 위치 + 2); }
    static void 넣기16(int[] kadar_àlluwa_tur, int 위치, int xëyma) { kadar_àlluwa_tur[위치] = (xëyma >>> 8) & 255; kadar_àlluwa_tur[위치 + 1] = xëyma & 255; }
    static void 넣기32(int[] kadar_àlluwa_tur, int 위치, int xëyma) { 넣기16(kadar_àlluwa_tur, 위치, xëyma >>> 16); 넣기16(kadar_àlluwa_tur, 위치 + 2, xëyma); }
    static int 합(int[] kadar_àlluwa_tur, int daw, int diir_xëyma, int xëyma) {
        for (int àlluwa_tur = 0; àlluwa_tur < diir_xëyma; àlluwa_tur += 2)
            xëyma += (kadar_àlluwa_tur[daw + àlluwa_tur] << 8) | (àlluwa_tur + 1 < diir_xëyma ? kadar_àlluwa_tur[daw + àlluwa_tur + 1] : 0);
        while ((xëyma >>> 16) != 0) xëyma = (xëyma & 65535) + (xëyma >>> 16);
        return xëyma;
    }
    static int 가상머리합(int 출발, int 도착, int diir_xëyma) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + diir_xëyma;
    }

    static void 과정정리() {
        for (int àlluwa_tur = 0; àlluwa_tur < 4; àlluwa_tur++) {
            접속번호들[àlluwa_tur] = 0; 받은길이[àlluwa_tur] = -1; 받은주소[àlluwa_tur] = 0; 받은접속번호[àlluwa_tur] = 0;
        }
        for (int àlluwa_tur = 0; àlluwa_tur < 64; àlluwa_tur++) if (mbaal_daraayba.받기(입력틀) == 0) break;
    }
    static int àlluwa_tur(int yombal_xëyma) { return yombal_xëyma >= 3 && yombal_xëyma < 7 && 접속번호들[yombal_xëyma - 3] != 0 ? yombal_xëyma - 3 : -1; }
    static int sos(int 접속번호) {
        if (mbaal_daraayba.입출력기준주소 == 0) return -19;
        if (접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 != 0) for (int àlluwa_tur = 0; àlluwa_tur < 4; àlluwa_tur++) if (접속번호들[àlluwa_tur] == 접속번호) return -98;
        for (int àlluwa_tur = 0; àlluwa_tur < 4; àlluwa_tur++) if (접속번호들[àlluwa_tur] == 0) {
            if (접속번호 == 0) {
                접속번호 = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int 앞 = 0; 앞 < 4; 앞++) if (접속번호들[앞] == 접속번호) 겹침 = true;
                    if (겹침) 접속번호++;
                }
            }
            접속번호들[àlluwa_tur] = 접속번호; 받은길이[àlluwa_tur] = -1;
            return àlluwa_tur + 3;
        }
        return -24;
    }
    static int Tej(int yombal_xëyma) {
        int xar_xar_dugal_xabaar = àlluwa_tur(yombal_xëyma);
        if (xar_xar_dugal_xabaar < 0) return -9;
        접속번호들[xar_xar_dugal_xabaar] = 0; 받은길이[xar_xar_dugal_xabaar] = -1;
        return 0;
    }
    static int Nàttangoo_dëkkuwaay(int yombal_xëyma) { int xar_xar_dugal_xabaar = àlluwa_tur(yombal_xëyma); return xar_xar_dugal_xabaar < 0 ? -9 : 받은주소[xar_xar_dugal_xabaar]; }
    static int 상대접속번호(int yombal_xëyma) { int xar_xar_dugal_xabaar = àlluwa_tur(yombal_xëyma); return xar_xar_dugal_xabaar < 0 ? -9 : 받은접속번호[xar_xar_dugal_xabaar]; }

    static void 바깥머리(int 종류, boolean teg_xëyma) {
        for (int àlluwa_tur = 0; àlluwa_tur < 6; àlluwa_tur++) {
            출력틀[àlluwa_tur] = teg_xëyma ? 255 : 찾은장치[àlluwa_tur];
            출력틀[6 + àlluwa_tur] = mbaal_daraayba.toftal_dëkkuwaay[àlluwa_tur];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void 주소요청(int jëmmukaay_xëyma) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int àlluwa_tur = 0; àlluwa_tur < 6; àlluwa_tur++) {
            출력틀[22 + àlluwa_tur] = mbaal_daraayba.toftal_dëkkuwaay[àlluwa_tur]; 출력틀[32 + àlluwa_tur] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, jëmmukaay_xëyma);
        mbaal_daraayba.Yónnee(출력틀, 42);
    }
    static void yokkute_dëkkuwaay(int diir_xëyma) {
        if (diir_xëyma < 42 || lëmm_16(입력틀, 14) != 1 || lëmm_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || lëmm_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = lëmm_16(입력틀, 20), Nàttangoo_xëyma = lëmm_32(입력틀, 28);
        if (종류 == 2 && Nàttangoo_xëyma == 찾을주소) {
            for (int àlluwa_tur = 0; àlluwa_tur < 6; àlluwa_tur++) {
                if (입력틀[6 + àlluwa_tur] != 입력틀[22 + àlluwa_tur] || 입력틀[32 + àlluwa_tur] != mbaal_daraayba.toftal_dëkkuwaay[àlluwa_tur]) return;
            }
            for (int àlluwa_tur = 0; àlluwa_tur < 6; àlluwa_tur++) 찾은장치[àlluwa_tur] = 입력틀[22 + àlluwa_tur];
            찾은주소 = Nàttangoo_xëyma;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int àlluwa_tur = 0; àlluwa_tur < 6; àlluwa_tur++) {
                출력틀[àlluwa_tur] = 입력틀[22 + àlluwa_tur]; 출력틀[32 + àlluwa_tur] = 입력틀[22 + àlluwa_tur];
                출력틀[22 + àlluwa_tur] = mbaal_daraayba.toftal_dëkkuwaay[àlluwa_tur];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, Nàttangoo_xëyma);
            mbaal_daraayba.Yónnee(출력틀, 42);
        }
    }

    static void yokkute_kadar(int diir_xëyma) {
        if (diir_xëyma < 14 || diir_xëyma > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, teg_xëyma = true;
        for (int àlluwa_tur = 0; àlluwa_tur < 6; àlluwa_tur++) {
            if (입력틀[àlluwa_tur] != mbaal_daraayba.toftal_dëkkuwaay[àlluwa_tur]) 자기 = false;
            if (입력틀[àlluwa_tur] != 255) teg_xëyma = false;
        }
        if (!자기 && !teg_xëyma) return;
        if (lëmm_16(입력틀, 12) == 0x0806) { yokkute_dëkkuwaay(diir_xëyma); return; }
        if (lëmm_16(입력틀, 12) != 0x0800) return;
        if (diir_xëyma < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int Tur_diir = (입력틀[14] & 15) * 4, 전체길이 = lëmm_16(입력틀, 16);
        if (Tur_diir < 20 || Tur_diir > 60 || 전체길이 < Tur_diir + 8 || 전체길이 > diir_xëyma - 14
            || (lëmm_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || lëmm_32(입력틀, 30) != 내주소 || 합(입력틀, 14, Tur_diir, 0) != 65535) { 폐기수++; return; }
        int daw = 14 + Tur_diir, mbir_diir = lëmm_16(입력틀, daw + 4);
        if (mbir_diir < 8 || mbir_diir != 전체길이 - Tur_diir || mbir_diir > 1032) { 폐기수++; return; }
        int 출발 = lëmm_32(입력틀, 26);
        if (lëmm_16(입력틀, daw + 6) != 0 && 합(입력틀, daw, mbir_diir, 가상머리합(출발, 내주소, mbir_diir)) != 65535) {
            폐기수++; return;
        }
        int jëmmukaay_xëyma = lëmm_16(입력틀, daw + 2);
        for (int xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < 4; xar_xar_dugal_xabaar++) if (접속번호들[xar_xar_dugal_xabaar] != 0 && 접속번호들[xar_xar_dugal_xabaar] == jëmmukaay_xëyma) {
            if (받은길이[xar_xar_dugal_xabaar] >= 0) { 폐기수++; return; }
            받은길이[xar_xar_dugal_xabaar] = mbir_diir - 8; 받은주소[xar_xar_dugal_xabaar] = 출발; 받은접속번호[xar_xar_dugal_xabaar] = lëmm_16(입력틀, daw);
            for (int àlluwa_tur = 0; àlluwa_tur < mbir_diir - 8; àlluwa_tur++) 받은자료[xar_xar_dugal_xabaar * 1024 + àlluwa_tur] = 입력틀[daw + 8 + àlluwa_tur];
            return;
        }
    }

    static void luñutu() {
        for (int àlluwa_tur = 0; àlluwa_tur < 16; àlluwa_tur++) {
            int diir_xëyma = mbaal_daraayba.받기(입력틀);
            if (diir_xëyma == 0) return;
            yokkute_kadar(diir_xëyma);
        }
    }
    static int seet_dëkkuwaay(int dëkkuwaay) {
        if (dëkkuwaay == 0 || dëkkuwaay == -1 || (dëkkuwaay >>> 28) >= 14 || (dëkkuwaay >>> 24) == 127 || dëkkuwaay == 내주소) return -101;
        int 다음 = (dëkkuwaay & mbaal_muuraay) == (내주소 & mbaal_muuraay) ? dëkkuwaay : bunt_xëyma;
        if (다음 == 찾은주소) return 0;
        찾을주소 = 다음;
        int daw = toftal_xëyma.밀리초(), 다음요청 = daw;
        while (toftal_xëyma.밀리초() - daw < 1000) {
            if (toftal_xëyma.밀리초() - 다음요청 >= 0) { 주소요청(다음); 다음요청 += 300; }
            luñutu();
            if (찾은주소 == 다음) return 0;
            toftal_xëyma.잠시양보();
        }
        return -110;
    }
    static int Yónnee(int yombal_xëyma, int dëkkuwaay, int 접속번호, int[] mbir, int diir_xëyma) {
        int xar_xar_dugal_xabaar = àlluwa_tur(yombal_xëyma);
        if (xar_xar_dugal_xabaar < 0) return -9;
        if (mbaal_daraayba.입출력기준주소 == 0) return -19;
        if (접속번호 < 1 || 접속번호 > 65535 || diir_xëyma < 0 || diir_xëyma > 1024) return -22;
        int 결과 = seet_dëkkuwaay(dëkkuwaay);
        if (결과 < 0) return 결과;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + diir_xëyma);
        넣기16(출력틀, 18, raññeekaay_xëyma++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, dëkkuwaay);
        넣기16(출력틀, 24, ~합(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[xar_xar_dugal_xabaar]); 넣기16(출력틀, 36, 접속번호);
        넣기16(출력틀, 38, diir_xëyma + 8); 넣기16(출력틀, 40, 0);
        for (int àlluwa_tur = 0; àlluwa_tur < diir_xëyma; àlluwa_tur++) 출력틀[42 + àlluwa_tur] = mbir[àlluwa_tur] & 255;
        int 검사합 = (~합(출력틀, 34, diir_xëyma + 8, 가상머리합(내주소, dëkkuwaay, diir_xëyma + 8))) & 65535;
        넣기16(출력틀, 40, 검사합 == 0 ? 65535 : 검사합);
        결과 = mbaal_daraayba.Yónnee(출력틀, diir_xëyma + 42);
        return 결과 < 0 ? 결과 : diir_xëyma;
    }
    static int 받기(int yombal_xëyma, int[] mbir, int 용량, int 제한) {
        int xar_xar_dugal_xabaar = àlluwa_tur(yombal_xëyma);
        if (xar_xar_dugal_xabaar < 0) return -9;
        int daw = toftal_xëyma.밀리초();
        while (true) {
            luñutu();
            int diir_xëyma = 받은길이[xar_xar_dugal_xabaar];
            if (diir_xëyma >= 0) {
                받은길이[xar_xar_dugal_xabaar] = -1;
                if (diir_xëyma > 용량) return -90;
                for (int àlluwa_tur = 0; àlluwa_tur < diir_xëyma; àlluwa_tur++) mbir[àlluwa_tur] = 받은자료[xar_xar_dugal_xabaar * 1024 + àlluwa_tur];
                return diir_xëyma;
            }
            if (제한 == 0) return -11;
            if (toftal_xëyma.밀리초() - daw >= 제한) return -110;
            toftal_xëyma.잠시양보();
        }
    }
    static void nekkin_xëyma() {
        문자단말.biir(mbaal_daraayba.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        문자단말.biir("TX: "); 문자단말.수쓰기(mbaal_daraayba.송신수);
        문자단말.biir(" RX: "); 문자단말.수쓰기(mbaal_daraayba.수신수);
        문자단말.biir(" DROP: "); 문자단말.수쓰기(폐기수);
        문자단말.biir("\n");
    }
}
