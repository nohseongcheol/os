// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ngaguquki_inani IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class iNethiwekhi_Isitaki {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int iNethiwekhi_insitha = 0xffffff00; /* ip.conf:NETMASK */
    static final int isango_inani = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], 받은길이 = new int[4], 받은주소 = new int[4], 받은접속번호 = new int[4];
    static int[] 받은자료 = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, isivezi_inani = 0, 폐기수 = 0;

    static int inamba_16(int[] uhlaka_thola_inkomba, int 위치) { return (uhlaka_thola_inkomba[위치] << 8) | uhlaka_thola_inkomba[위치 + 1]; }
    static int inamba_32(int[] uhlaka_thola_inkomba, int 위치) { return (inamba_16(uhlaka_thola_inkomba, 위치) << 16) | inamba_16(uhlaka_thola_inkomba, 위치 + 2); }
    static void 넣기16(int[] uhlaka_thola_inkomba, int 위치, int inani) { uhlaka_thola_inkomba[위치] = (inani >>> 8) & 255; uhlaka_thola_inkomba[위치 + 1] = inani & 255; }
    static void 넣기32(int[] uhlaka_thola_inkomba, int 위치, int inani) { 넣기16(uhlaka_thola_inkomba, 위치, inani >>> 16); 넣기16(uhlaka_thola_inkomba, 위치 + 2, inani); }
    static int 합(int[] uhlaka_thola_inkomba, int Sebenzisa, int ubude_inani, int inani) {
        for (int thola_inkomba = 0; thola_inkomba < ubude_inani; thola_inkomba += 2)
            inani += (uhlaka_thola_inkomba[Sebenzisa + thola_inkomba] << 8) | (thola_inkomba + 1 < ubude_inani ? uhlaka_thola_inkomba[Sebenzisa + thola_inkomba + 1] : 0);
        while ((inani >>> 16) != 0) inani = (inani & 65535) + (inani >>> 16);
        return inani;
    }
    static int 가상머리합(int 출발, int 도착, int ubude_inani) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + ubude_inani;
    }

    static void 과정정리() {
        for (int thola_inkomba = 0; thola_inkomba < 4; thola_inkomba++) {
            접속번호들[thola_inkomba] = 0; 받은길이[thola_inkomba] = -1; 받은주소[thola_inkomba] = 0; 받은접속번호[thola_inkomba] = 0;
        }
        for (int thola_inkomba = 0; thola_inkomba < 64; thola_inkomba++) if (iNethiwekhi_idrayiva.받기(입력틀) == 0) break;
    }
    static int thola_inkomba(int isibambo_inani) { return isibambo_inani >= 3 && isibambo_inani < 7 && 접속번호들[isibambo_inani - 3] != 0 ? isibambo_inani - 3 : -1; }
    static int Vula(int 접속번호) {
        if (iNethiwekhi_idrayiva.입출력기준주소 == 0) return -19;
        if (접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 != 0) for (int thola_inkomba = 0; thola_inkomba < 4; thola_inkomba++) if (접속번호들[thola_inkomba] == 접속번호) return -98;
        for (int thola_inkomba = 0; thola_inkomba < 4; thola_inkomba++) if (접속번호들[thola_inkomba] == 0) {
            if (접속번호 == 0) {
                접속번호 = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int 앞 = 0; 앞 < 4; 앞++) if (접속번호들[앞] == 접속번호) 겹침 = true;
                    if (겹침) 접속번호++;
                }
            }
            접속번호들[thola_inkomba] = 접속번호; 받은길이[thola_inkomba] = -1;
            return thola_inkomba + 3;
        }
        return -24;
    }
    static int Vala(int isibambo_inani) {
        int isikhala_okufakwayo = thola_inkomba(isibambo_inani);
        if (isikhala_okufakwayo < 0) return -9;
        접속번호들[isikhala_okufakwayo] = 0; 받은길이[isikhala_okufakwayo] = -1;
        return 0;
    }
    static int untanga_ikheli(int isibambo_inani) { int isikhala_okufakwayo = thola_inkomba(isibambo_inani); return isikhala_okufakwayo < 0 ? -9 : 받은주소[isikhala_okufakwayo]; }
    static int 상대접속번호(int isibambo_inani) { int isikhala_okufakwayo = thola_inkomba(isibambo_inani); return isikhala_okufakwayo < 0 ? -9 : 받은접속번호[isikhala_okufakwayo]; }

    static void 바깥머리(int 종류, boolean ukusakaza_inani) {
        for (int thola_inkomba = 0; thola_inkomba < 6; thola_inkomba++) {
            출력틀[thola_inkomba] = ukusakaza_inani ? 255 : 찾은장치[thola_inkomba];
            출력틀[6 + thola_inkomba] = iNethiwekhi_idrayiva.idivayisi_ikheli[thola_inkomba];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void 주소요청(int isikhumulo_inani) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int thola_inkomba = 0; thola_inkomba < 6; thola_inkomba++) {
            출력틀[22 + thola_inkomba] = iNethiwekhi_idrayiva.idivayisi_ikheli[thola_inkomba]; 출력틀[32 + thola_inkomba] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, isikhumulo_inani);
        iNethiwekhi_idrayiva.Thumela(출력틀, 42);
    }
    static void Inqubo_ikheli(int ubude_inani) {
        if (ubude_inani < 42 || inamba_16(입력틀, 14) != 1 || inamba_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || inamba_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = inamba_16(입력틀, 20), untanga_inani = inamba_32(입력틀, 28);
        if (종류 == 2 && untanga_inani == 찾을주소) {
            for (int thola_inkomba = 0; thola_inkomba < 6; thola_inkomba++) {
                if (입력틀[6 + thola_inkomba] != 입력틀[22 + thola_inkomba] || 입력틀[32 + thola_inkomba] != iNethiwekhi_idrayiva.idivayisi_ikheli[thola_inkomba]) return;
            }
            for (int thola_inkomba = 0; thola_inkomba < 6; thola_inkomba++) 찾은장치[thola_inkomba] = 입력틀[22 + thola_inkomba];
            찾은주소 = untanga_inani;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int thola_inkomba = 0; thola_inkomba < 6; thola_inkomba++) {
                출력틀[thola_inkomba] = 입력틀[22 + thola_inkomba]; 출력틀[32 + thola_inkomba] = 입력틀[22 + thola_inkomba];
                출력틀[22 + thola_inkomba] = iNethiwekhi_idrayiva.idivayisi_ikheli[thola_inkomba];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, untanga_inani);
            iNethiwekhi_idrayiva.Thumela(출력틀, 42);
        }
    }

    static void Inqubo_uhlaka(int ubude_inani) {
        if (ubude_inani < 14 || ubude_inani > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, ukusakaza_inani = true;
        for (int thola_inkomba = 0; thola_inkomba < 6; thola_inkomba++) {
            if (입력틀[thola_inkomba] != iNethiwekhi_idrayiva.idivayisi_ikheli[thola_inkomba]) 자기 = false;
            if (입력틀[thola_inkomba] != 255) ukusakaza_inani = false;
        }
        if (!자기 && !ukusakaza_inani) return;
        if (inamba_16(입력틀, 12) == 0x0806) { Inqubo_ikheli(ubude_inani); return; }
        if (inamba_16(입력틀, 12) != 0x0800) return;
        if (ubude_inani < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int Unhlokweni_ubude = (입력틀[14] & 15) * 4, 전체길이 = inamba_16(입력틀, 16);
        if (Unhlokweni_ubude < 20 || Unhlokweni_ubude > 60 || 전체길이 < Unhlokweni_ubude + 8 || 전체길이 > ubude_inani - 14
            || (inamba_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || inamba_32(입력틀, 30) != 내주소 || 합(입력틀, 14, Unhlokweni_ubude, 0) != 65535) { 폐기수++; return; }
        int Sebenzisa = 14 + Unhlokweni_ubude, imininingwane_ubude = inamba_16(입력틀, Sebenzisa + 4);
        if (imininingwane_ubude < 8 || imininingwane_ubude != 전체길이 - Unhlokweni_ubude || imininingwane_ubude > 1032) { 폐기수++; return; }
        int 출발 = inamba_32(입력틀, 26);
        if (inamba_16(입력틀, Sebenzisa + 6) != 0 && 합(입력틀, Sebenzisa, imininingwane_ubude, 가상머리합(출발, 내주소, imininingwane_ubude)) != 65535) {
            폐기수++; return;
        }
        int isikhumulo_inani = inamba_16(입력틀, Sebenzisa + 2);
        for (int isikhala_okufakwayo = 0; isikhala_okufakwayo < 4; isikhala_okufakwayo++) if (접속번호들[isikhala_okufakwayo] != 0 && 접속번호들[isikhala_okufakwayo] == isikhumulo_inani) {
            if (받은길이[isikhala_okufakwayo] >= 0) { 폐기수++; return; }
            받은길이[isikhala_okufakwayo] = imininingwane_ubude - 8; 받은주소[isikhala_okufakwayo] = 출발; 받은접속번호[isikhala_okufakwayo] = inamba_16(입력틀, Sebenzisa);
            for (int thola_inkomba = 0; thola_inkomba < imininingwane_ubude - 8; thola_inkomba++) 받은자료[isikhala_okufakwayo * 1024 + thola_inkomba] = 입력틀[Sebenzisa + 8 + thola_inkomba];
            return;
        }
    }

    static void qiniseka() {
        for (int thola_inkomba = 0; thola_inkomba < 16; thola_inkomba++) {
            int ubude_inani = iNethiwekhi_idrayiva.받기(입력틀);
            if (ubude_inani == 0) return;
            Inqubo_uhlaka(ubude_inani);
        }
    }
    static int thola_ikheli(int ikheli) {
        if (ikheli == 0 || ikheli == -1 || (ikheli >>> 28) >= 14 || (ikheli >>> 24) == 127 || ikheli == 내주소) return -101;
        int 다음 = (ikheli & iNethiwekhi_insitha) == (내주소 & iNethiwekhi_insitha) ? ikheli : isango_inani;
        if (다음 == 찾은주소) return 0;
        찾을주소 = 다음;
        int Sebenzisa = idivayisi_inani.밀리초(), 다음요청 = Sebenzisa;
        while (idivayisi_inani.밀리초() - Sebenzisa < 1000) {
            if (idivayisi_inani.밀리초() - 다음요청 >= 0) { 주소요청(다음); 다음요청 += 300; }
            qiniseka();
            if (찾은주소 == 다음) return 0;
            idivayisi_inani.잠시양보();
        }
        return -110;
    }
    static int Thumela(int isibambo_inani, int ikheli, int 접속번호, int[] imininingwane, int ubude_inani) {
        int isikhala_okufakwayo = thola_inkomba(isibambo_inani);
        if (isikhala_okufakwayo < 0) return -9;
        if (iNethiwekhi_idrayiva.입출력기준주소 == 0) return -19;
        if (접속번호 < 1 || 접속번호 > 65535 || ubude_inani < 0 || ubude_inani > 1024) return -22;
        int 결과 = thola_ikheli(ikheli);
        if (결과 < 0) return 결과;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + ubude_inani);
        넣기16(출력틀, 18, isivezi_inani++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, ikheli);
        넣기16(출력틀, 24, ~합(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[isikhala_okufakwayo]); 넣기16(출력틀, 36, 접속번호);
        넣기16(출력틀, 38, ubude_inani + 8); 넣기16(출력틀, 40, 0);
        for (int thola_inkomba = 0; thola_inkomba < ubude_inani; thola_inkomba++) 출력틀[42 + thola_inkomba] = imininingwane[thola_inkomba] & 255;
        int 검사합 = (~합(출력틀, 34, ubude_inani + 8, 가상머리합(내주소, ikheli, ubude_inani + 8))) & 65535;
        넣기16(출력틀, 40, 검사합 == 0 ? 65535 : 검사합);
        결과 = iNethiwekhi_idrayiva.Thumela(출력틀, ubude_inani + 42);
        return 결과 < 0 ? 결과 : ubude_inani;
    }
    static int 받기(int isibambo_inani, int[] imininingwane, int 용량, int 제한) {
        int isikhala_okufakwayo = thola_inkomba(isibambo_inani);
        if (isikhala_okufakwayo < 0) return -9;
        int Sebenzisa = idivayisi_inani.밀리초();
        while (true) {
            qiniseka();
            int ubude_inani = 받은길이[isikhala_okufakwayo];
            if (ubude_inani >= 0) {
                받은길이[isikhala_okufakwayo] = -1;
                if (ubude_inani > 용량) return -90;
                for (int thola_inkomba = 0; thola_inkomba < ubude_inani; thola_inkomba++) imininingwane[thola_inkomba] = 받은자료[isikhala_okufakwayo * 1024 + thola_inkomba];
                return ubude_inani;
            }
            if (제한 == 0) return -11;
            if (idivayisi_inani.밀리초() - Sebenzisa >= 제한) return -110;
            idivayisi_inani.잠시양보();
        }
    }
    static void isimo_inani() {
        문자단말.Bhala(iNethiwekhi_idrayiva.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        문자단말.Bhala("TX: "); 문자단말.수쓰기(iNethiwekhi_idrayiva.송신수);
        문자단말.Bhala(" RX: "); 문자단말.수쓰기(iNethiwekhi_idrayiva.수신수);
        문자단말.Bhala(" DROP: "); 문자단말.수쓰기(폐기수);
        문자단말.Bhala("\n");
    }
}
