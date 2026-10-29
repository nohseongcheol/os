// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** imi_ndawonye_ixabiso IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class Inethiwekhi_fumba {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int Inethiwekhi_imaskhi = 0xffffff00; /* ip.conf:NETMASK */
    static final int isango_lekhompyutha_ixabiso = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], 받은길이 = new int[4], 받은주소 = new int[4], 받은접속번호 = new int[4];
    static int[] 받은자료 = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, isalathisi_ixabiso = 0, 폐기수 = 0;

    static int inani_elipheleleyo_16(int[] ifreyim_indeksa, int 위치) { return (ifreyim_indeksa[위치] << 8) | ifreyim_indeksa[위치 + 1]; }
    static int inani_elipheleleyo_32(int[] ifreyim_indeksa, int 위치) { return (inani_elipheleleyo_16(ifreyim_indeksa, 위치) << 16) | inani_elipheleleyo_16(ifreyim_indeksa, 위치 + 2); }
    static void 넣기16(int[] ifreyim_indeksa, int 위치, int ixabiso) { ifreyim_indeksa[위치] = (ixabiso >>> 8) & 255; ifreyim_indeksa[위치 + 1] = ixabiso & 255; }
    static void 넣기32(int[] ifreyim_indeksa, int 위치, int ixabiso) { 넣기16(ifreyim_indeksa, 위치, ixabiso >>> 16); 넣기16(ifreyim_indeksa, 위치 + 2, ixabiso); }
    static int 합(int[] ifreyim_indeksa, int Phumeza, int ubude_ixabiso, int ixabiso) {
        for (int indeksa = 0; indeksa < ubude_ixabiso; indeksa += 2)
            ixabiso += (ifreyim_indeksa[Phumeza + indeksa] << 8) | (indeksa + 1 < ubude_ixabiso ? ifreyim_indeksa[Phumeza + indeksa + 1] : 0);
        while ((ixabiso >>> 16) != 0) ixabiso = (ixabiso & 65535) + (ixabiso >>> 16);
        return ixabiso;
    }
    static int 가상머리합(int 출발, int 도착, int ubude_ixabiso) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + ubude_ixabiso;
    }

    static void 과정정리() {
        for (int indeksa = 0; indeksa < 4; indeksa++) {
            접속번호들[indeksa] = 0; 받은길이[indeksa] = -1; 받은주소[indeksa] = 0; 받은접속번호[indeksa] = 0;
        }
        for (int indeksa = 0; indeksa < 64; indeksa++) if (Inethiwekhi_idrayiva.받기(입력틀) == 0) break;
    }
    static int indeksa(int isibambi_ixabiso) { return isibambi_ixabiso >= 3 && isibambi_ixabiso < 7 && 접속번호들[isibambi_ixabiso - 3] != 0 ? isibambi_ixabiso - 3 : -1; }
    static int Vula(int 접속번호) {
        if (Inethiwekhi_idrayiva.입출력기준주소 == 0) return -19;
        if (접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 != 0) for (int indeksa = 0; indeksa < 4; indeksa++) if (접속번호들[indeksa] == 접속번호) return -98;
        for (int indeksa = 0; indeksa < 4; indeksa++) if (접속번호들[indeksa] == 0) {
            if (접속번호 == 0) {
                접속번호 = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int 앞 = 0; 앞 < 4; 앞++) if (접속번호들[앞] == 접속번호) 겹침 = true;
                    if (겹침) 접속번호++;
                }
            }
            접속번호들[indeksa] = 접속번호; 받은길이[indeksa] = -1;
            return indeksa + 3;
        }
        return -24;
    }
    static int Vala(int isibambi_ixabiso) {
        int isithuba_ufako_nkcukacha = indeksa(isibambi_ixabiso);
        if (isithuba_ufako_nkcukacha < 0) return -9;
        접속번호들[isithuba_ufako_nkcukacha] = 0; 받은길이[isithuba_ufako_nkcukacha] = -1;
        return 0;
    }
    static int untanga_idilesi(int isibambi_ixabiso) { int isithuba_ufako_nkcukacha = indeksa(isibambi_ixabiso); return isithuba_ufako_nkcukacha < 0 ? -9 : 받은주소[isithuba_ufako_nkcukacha]; }
    static int 상대접속번호(int isibambi_ixabiso) { int isithuba_ufako_nkcukacha = indeksa(isibambi_ixabiso); return isithuba_ufako_nkcukacha < 0 ? -9 : 받은접속번호[isithuba_ufako_nkcukacha]; }

    static void 바깥머리(int 종류, boolean usasazo_ixabiso) {
        for (int indeksa = 0; indeksa < 6; indeksa++) {
            출력틀[indeksa] = usasazo_ixabiso ? 255 : 찾은장치[indeksa];
            출력틀[6 + indeksa] = Inethiwekhi_idrayiva.isixhobo_idilesi[indeksa];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void 주소요청(int indawo_ekuyiwa_kuyo_ixabiso) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int indeksa = 0; indeksa < 6; indeksa++) {
            출력틀[22 + indeksa] = Inethiwekhi_idrayiva.isixhobo_idilesi[indeksa]; 출력틀[32 + indeksa] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, indawo_ekuyiwa_kuyo_ixabiso);
        Inethiwekhi_idrayiva.thumela(출력틀, 42);
    }
    static void Inkqubo_idilesi(int ubude_ixabiso) {
        if (ubude_ixabiso < 42 || inani_elipheleleyo_16(입력틀, 14) != 1 || inani_elipheleleyo_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || inani_elipheleleyo_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = inani_elipheleleyo_16(입력틀, 20), untanga_ixabiso = inani_elipheleleyo_32(입력틀, 28);
        if (종류 == 2 && untanga_ixabiso == 찾을주소) {
            for (int indeksa = 0; indeksa < 6; indeksa++) {
                if (입력틀[6 + indeksa] != 입력틀[22 + indeksa] || 입력틀[32 + indeksa] != Inethiwekhi_idrayiva.isixhobo_idilesi[indeksa]) return;
            }
            for (int indeksa = 0; indeksa < 6; indeksa++) 찾은장치[indeksa] = 입력틀[22 + indeksa];
            찾은주소 = untanga_ixabiso;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int indeksa = 0; indeksa < 6; indeksa++) {
                출력틀[indeksa] = 입력틀[22 + indeksa]; 출력틀[32 + indeksa] = 입력틀[22 + indeksa];
                출력틀[22 + indeksa] = Inethiwekhi_idrayiva.isixhobo_idilesi[indeksa];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, untanga_ixabiso);
            Inethiwekhi_idrayiva.thumela(출력틀, 42);
        }
    }

    static void Inkqubo_ifreyim(int ubude_ixabiso) {
        if (ubude_ixabiso < 14 || ubude_ixabiso > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, usasazo_ixabiso = true;
        for (int indeksa = 0; indeksa < 6; indeksa++) {
            if (입력틀[indeksa] != Inethiwekhi_idrayiva.isixhobo_idilesi[indeksa]) 자기 = false;
            if (입력틀[indeksa] != 255) usasazo_ixabiso = false;
        }
        if (!자기 && !usasazo_ixabiso) return;
        if (inani_elipheleleyo_16(입력틀, 12) == 0x0806) { Inkqubo_idilesi(ubude_ixabiso); return; }
        if (inani_elipheleleyo_16(입력틀, 12) != 0x0800) return;
        if (ubude_ixabiso < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int Iheda_ubude = (입력틀[14] & 15) * 4, 전체길이 = inani_elipheleleyo_16(입력틀, 16);
        if (Iheda_ubude < 20 || Iheda_ubude > 60 || 전체길이 < Iheda_ubude + 8 || 전체길이 > ubude_ixabiso - 14
            || (inani_elipheleleyo_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || inani_elipheleleyo_32(입력틀, 30) != 내주소 || 합(입력틀, 14, Iheda_ubude, 0) != 65535) { 폐기수++; return; }
        int Phumeza = 14 + Iheda_ubude, iingcombolo_ubude = inani_elipheleleyo_16(입력틀, Phumeza + 4);
        if (iingcombolo_ubude < 8 || iingcombolo_ubude != 전체길이 - Iheda_ubude || iingcombolo_ubude > 1032) { 폐기수++; return; }
        int 출발 = inani_elipheleleyo_32(입력틀, 26);
        if (inani_elipheleleyo_16(입력틀, Phumeza + 6) != 0 && 합(입력틀, Phumeza, iingcombolo_ubude, 가상머리합(출발, 내주소, iingcombolo_ubude)) != 65535) {
            폐기수++; return;
        }
        int indawo_ekuyiwa_kuyo_ixabiso = inani_elipheleleyo_16(입력틀, Phumeza + 2);
        for (int isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < 4; isithuba_ufako_nkcukacha++) if (접속번호들[isithuba_ufako_nkcukacha] != 0 && 접속번호들[isithuba_ufako_nkcukacha] == indawo_ekuyiwa_kuyo_ixabiso) {
            if (받은길이[isithuba_ufako_nkcukacha] >= 0) { 폐기수++; return; }
            받은길이[isithuba_ufako_nkcukacha] = iingcombolo_ubude - 8; 받은주소[isithuba_ufako_nkcukacha] = 출발; 받은접속번호[isithuba_ufako_nkcukacha] = inani_elipheleleyo_16(입력틀, Phumeza);
            for (int indeksa = 0; indeksa < iingcombolo_ubude - 8; indeksa++) 받은자료[isithuba_ufako_nkcukacha * 1024 + indeksa] = 입력틀[Phumeza + 8 + indeksa];
            return;
        }
    }

    static void ngqinisisa() {
        for (int indeksa = 0; indeksa < 16; indeksa++) {
            int ubude_ixabiso = Inethiwekhi_idrayiva.받기(입력틀);
            if (ubude_ixabiso == 0) return;
            Inkqubo_ifreyim(ubude_ixabiso);
        }
    }
    static int fumana_idilesi(int idilesi) {
        if (idilesi == 0 || idilesi == -1 || (idilesi >>> 28) >= 14 || (idilesi >>> 24) == 127 || idilesi == 내주소) return -101;
        int 다음 = (idilesi & Inethiwekhi_imaskhi) == (내주소 & Inethiwekhi_imaskhi) ? idilesi : isango_lekhompyutha_ixabiso;
        if (다음 == 찾은주소) return 0;
        찾을주소 = 다음;
        int Phumeza = isixhobo_ixabiso.밀리초(), 다음요청 = Phumeza;
        while (isixhobo_ixabiso.밀리초() - Phumeza < 1000) {
            if (isixhobo_ixabiso.밀리초() - 다음요청 >= 0) { 주소요청(다음); 다음요청 += 300; }
            ngqinisisa();
            if (찾은주소 == 다음) return 0;
            isixhobo_ixabiso.잠시양보();
        }
        return -110;
    }
    static int thumela(int isibambi_ixabiso, int idilesi, int 접속번호, int[] iingcombolo, int ubude_ixabiso) {
        int isithuba_ufako_nkcukacha = indeksa(isibambi_ixabiso);
        if (isithuba_ufako_nkcukacha < 0) return -9;
        if (Inethiwekhi_idrayiva.입출력기준주소 == 0) return -19;
        if (접속번호 < 1 || 접속번호 > 65535 || ubude_ixabiso < 0 || ubude_ixabiso > 1024) return -22;
        int 결과 = fumana_idilesi(idilesi);
        if (결과 < 0) return 결과;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + ubude_ixabiso);
        넣기16(출력틀, 18, isalathisi_ixabiso++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, idilesi);
        넣기16(출력틀, 24, ~합(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[isithuba_ufako_nkcukacha]); 넣기16(출력틀, 36, 접속번호);
        넣기16(출력틀, 38, ubude_ixabiso + 8); 넣기16(출력틀, 40, 0);
        for (int indeksa = 0; indeksa < ubude_ixabiso; indeksa++) 출력틀[42 + indeksa] = iingcombolo[indeksa] & 255;
        int 검사합 = (~합(출력틀, 34, ubude_ixabiso + 8, 가상머리합(내주소, idilesi, ubude_ixabiso + 8))) & 65535;
        넣기16(출력틀, 40, 검사합 == 0 ? 65535 : 검사합);
        결과 = Inethiwekhi_idrayiva.thumela(출력틀, ubude_ixabiso + 42);
        return 결과 < 0 ? 결과 : ubude_ixabiso;
    }
    static int 받기(int isibambi_ixabiso, int[] iingcombolo, int 용량, int 제한) {
        int isithuba_ufako_nkcukacha = indeksa(isibambi_ixabiso);
        if (isithuba_ufako_nkcukacha < 0) return -9;
        int Phumeza = isixhobo_ixabiso.밀리초();
        while (true) {
            ngqinisisa();
            int ubude_ixabiso = 받은길이[isithuba_ufako_nkcukacha];
            if (ubude_ixabiso >= 0) {
                받은길이[isithuba_ufako_nkcukacha] = -1;
                if (ubude_ixabiso > 용량) return -90;
                for (int indeksa = 0; indeksa < ubude_ixabiso; indeksa++) iingcombolo[indeksa] = 받은자료[isithuba_ufako_nkcukacha * 1024 + indeksa];
                return ubude_ixabiso;
            }
            if (제한 == 0) return -11;
            if (isixhobo_ixabiso.밀리초() - Phumeza >= 제한) return -110;
            isixhobo_ixabiso.잠시양보();
        }
    }
    static void imo_ixabiso() {
        문자단말.Bhala(Inethiwekhi_idrayiva.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        문자단말.Bhala("TX: "); 문자단말.수쓰기(Inethiwekhi_idrayiva.송신수);
        문자단말.Bhala(" RX: "); 문자단말.수쓰기(Inethiwekhi_idrayiva.수신수);
        문자단말.Bhala(" DROP: "); 문자단말.수쓰기(폐기수);
        문자단말.Bhala("\n");
    }
}
