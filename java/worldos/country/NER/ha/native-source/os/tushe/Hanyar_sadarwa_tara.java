// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Tsaye_cik_Daraja IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class Hanyar_sadarwa_tara {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int Hanyar_sadarwa_Burtu = 0xffffff00; /* ip.conf:NETMASK */
    static final int Mashiga_Daraja = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], 받은길이 = new int[4], 받은주소 = new int[4], 받은접속번호 = new int[4];
    static int[] 받은자료 = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, mai_ganewa_Daraja = 0, 폐기수 = 0;

    static int Lamba_mara_16(int[] allo_Indes, int 위치) { return (allo_Indes[위치] << 8) | allo_Indes[위치 + 1]; }
    static int Lamba_mara_32(int[] allo_Indes, int 위치) { return (Lamba_mara_16(allo_Indes, 위치) << 16) | Lamba_mara_16(allo_Indes, 위치 + 2); }
    static void 넣기16(int[] allo_Indes, int 위치, int Daraja) { allo_Indes[위치] = (Daraja >>> 8) & 255; allo_Indes[위치 + 1] = Daraja & 255; }
    static void 넣기32(int[] allo_Indes, int 위치, int Daraja) { 넣기16(allo_Indes, 위치, Daraja >>> 16); 넣기16(allo_Indes, 위치 + 2, Daraja); }
    static int 합(int[] allo_Indes, int Tafiyar_da, int Tsawo_Daraja, int Daraja) {
        for (int Indes = 0; Indes < Tsawo_Daraja; Indes += 2)
            Daraja += (allo_Indes[Tafiyar_da + Indes] << 8) | (Indes + 1 < Tsawo_Daraja ? allo_Indes[Tafiyar_da + Indes + 1] : 0);
        while ((Daraja >>> 16) != 0) Daraja = (Daraja & 65535) + (Daraja >>> 16);
        return Daraja;
    }
    static int 가상머리합(int 출발, int 도착, int Tsawo_Daraja) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + Tsawo_Daraja;
    }

    static void 과정정리() {
        for (int Indes = 0; Indes < 4; Indes++) {
            접속번호들[Indes] = 0; 받은길이[Indes] = -1; 받은주소[Indes] = 0; 받은접속번호[Indes] = 0;
        }
        for (int Indes = 0; Indes < 64; Indes++) if (Hanyar_sadarwa_diraiba.받기(입력틀) == 0) break;
    }
    static int Indes(int Mariki_Daraja) { return Mariki_Daraja >= 3 && Mariki_Daraja < 7 && 접속번호들[Mariki_Daraja - 3] != 0 ? Mariki_Daraja - 3 : -1; }
    static int Buɗe(int lambar_kafa) {
        if (Hanyar_sadarwa_diraiba.입출력기준주소 == 0) return -19;
        if (lambar_kafa < 0 || lambar_kafa > 65535) return -22;
        if (lambar_kafa != 0) for (int Indes = 0; Indes < 4; Indes++) if (접속번호들[Indes] == lambar_kafa) return -98;
        for (int Indes = 0; Indes < 4; Indes++) if (접속번호들[Indes] == 0) {
            if (lambar_kafa == 0) {
                lambar_kafa = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int kyamarar_gaba_Daraja = 0; kyamarar_gaba_Daraja < 4; kyamarar_gaba_Daraja++) if (접속번호들[kyamarar_gaba_Daraja] == lambar_kafa) 겹침 = true;
                    if (겹침) lambar_kafa++;
                }
            }
            접속번호들[Indes] = lambar_kafa; 받은길이[Indes] = -1;
            return Indes + 3;
        }
        return -24;
    }
    static int Rufe(int Mariki_Daraja) {
        int rami_Mashigar_bayanai = Indes(Mariki_Daraja);
        if (rami_Mashigar_bayanai < 0) return -9;
        접속번호들[rami_Mashigar_bayanai] = 0; 받은길이[rami_Mashigar_bayanai] = -1;
        return 0;
    }
    static int Fiya_imel(int Mariki_Daraja) { int rami_Mashigar_bayanai = Indes(Mariki_Daraja); return rami_Mashigar_bayanai < 0 ? -9 : 받은주소[rami_Mashigar_bayanai]; }
    static int Fiya_lambar_kafa(int Mariki_Daraja) { int rami_Mashigar_bayanai = Indes(Mariki_Daraja); return rami_Mashigar_bayanai < 0 ? -9 : 받은접속번호[rami_Mashigar_bayanai]; }

    static void 바깥머리(int 종류, boolean watsar_da_Daraja) {
        for (int Indes = 0; Indes < 6; Indes++) {
            출력틀[Indes] = watsar_da_Daraja ? 255 : 찾은장치[Indes];
            출력틀[6 + Indes] = Hanyar_sadarwa_diraiba.na_ura_imel[Indes];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void 주소요청(int Zangon_ƙarshe_Daraja) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int Indes = 0; Indes < 6; Indes++) {
            출력틀[22 + Indes] = Hanyar_sadarwa_diraiba.na_ura_imel[Indes]; 출력틀[32 + Indes] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, Zangon_ƙarshe_Daraja);
        Hanyar_sadarwa_diraiba.Aika(출력틀, 42);
    }
    static void haryar_aikin_na_ura_imel(int Tsawo_Daraja) {
        if (Tsawo_Daraja < 42 || Lamba_mara_16(입력틀, 14) != 1 || Lamba_mara_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || Lamba_mara_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = Lamba_mara_16(입력틀, 20), Fiya_Daraja = Lamba_mara_32(입력틀, 28);
        if (종류 == 2 && Fiya_Daraja == 찾을주소) {
            for (int Indes = 0; Indes < 6; Indes++) {
                if (입력틀[6 + Indes] != 입력틀[22 + Indes] || 입력틀[32 + Indes] != Hanyar_sadarwa_diraiba.na_ura_imel[Indes]) return;
            }
            for (int Indes = 0; Indes < 6; Indes++) 찾은장치[Indes] = 입력틀[22 + Indes];
            찾은주소 = Fiya_Daraja;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int Indes = 0; Indes < 6; Indes++) {
                출력틀[Indes] = 입력틀[22 + Indes]; 출력틀[32 + Indes] = 입력틀[22 + Indes];
                출력틀[22 + Indes] = Hanyar_sadarwa_diraiba.na_ura_imel[Indes];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, Fiya_Daraja);
            Hanyar_sadarwa_diraiba.Aika(출력틀, 42);
        }
    }

    static void haryar_aikin_na_ura_allo(int Tsawo_Daraja) {
        if (Tsawo_Daraja < 14 || Tsawo_Daraja > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, watsar_da_Daraja = true;
        for (int Indes = 0; Indes < 6; Indes++) {
            if (입력틀[Indes] != Hanyar_sadarwa_diraiba.na_ura_imel[Indes]) 자기 = false;
            if (입력틀[Indes] != 255) watsar_da_Daraja = false;
        }
        if (!자기 && !watsar_da_Daraja) return;
        if (Lamba_mara_16(입력틀, 12) == 0x0806) { haryar_aikin_na_ura_imel(Tsawo_Daraja); return; }
        if (Lamba_mara_16(입력틀, 12) != 0x0800) return;
        if (Tsawo_Daraja < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int Kai_Tsawo = (입력틀[14] & 15) * 4, 전체길이 = Lamba_mara_16(입력틀, 16);
        if (Kai_Tsawo < 20 || Kai_Tsawo > 60 || 전체길이 < Kai_Tsawo + 8 || 전체길이 > Tsawo_Daraja - 14
            || (Lamba_mara_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || Lamba_mara_32(입력틀, 30) != 내주소 || 합(입력틀, 14, Kai_Tsawo, 0) != 65535) { 폐기수++; return; }
        int Tafiyar_da = 14 + Kai_Tsawo, Tarin_bayani_Tsawo = Lamba_mara_16(입력틀, Tafiyar_da + 4);
        if (Tarin_bayani_Tsawo < 8 || Tarin_bayani_Tsawo != 전체길이 - Kai_Tsawo || Tarin_bayani_Tsawo > 1032) { 폐기수++; return; }
        int 출발 = Lamba_mara_32(입력틀, 26);
        if (Lamba_mara_16(입력틀, Tafiyar_da + 6) != 0 && 합(입력틀, Tafiyar_da, Tarin_bayani_Tsawo, 가상머리합(출발, 내주소, Tarin_bayani_Tsawo)) != 65535) {
            폐기수++; return;
        }
        int Zangon_ƙarshe_Daraja = Lamba_mara_16(입력틀, Tafiyar_da + 2);
        for (int rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < 4; rami_Mashigar_bayanai++) if (접속번호들[rami_Mashigar_bayanai] != 0 && 접속번호들[rami_Mashigar_bayanai] == Zangon_ƙarshe_Daraja) {
            if (받은길이[rami_Mashigar_bayanai] >= 0) { 폐기수++; return; }
            받은길이[rami_Mashigar_bayanai] = Tarin_bayani_Tsawo - 8; 받은주소[rami_Mashigar_bayanai] = 출발; 받은접속번호[rami_Mashigar_bayanai] = Lamba_mara_16(입력틀, Tafiyar_da);
            for (int Indes = 0; Indes < Tarin_bayani_Tsawo - 8; Indes++) 받은자료[rami_Mashigar_bayanai * 1024 + Indes] = 입력틀[Tafiyar_da + 8 + Indes];
            return;
        }
    }

    static void Tabbatar_da() {
        for (int Indes = 0; Indes < 16; Indes++) {
            int Tsawo_Daraja = Hanyar_sadarwa_diraiba.받기(입력틀);
            if (Tsawo_Daraja == 0) return;
            haryar_aikin_na_ura_allo(Tsawo_Daraja);
        }
    }
    static int nema_imel(int imel) {
        if (imel == 0 || imel == -1 || (imel >>> 28) >= 14 || (imel >>> 24) == 127 || imel == 내주소) return -101;
        int 다음 = (imel & Hanyar_sadarwa_Burtu) == (내주소 & Hanyar_sadarwa_Burtu) ? imel : Mashiga_Daraja;
        if (다음 == 찾은주소) return 0;
        찾을주소 = 다음;
        int Tafiyar_da = na_ura_Daraja.밀리초(), 다음요청 = Tafiyar_da;
        while (na_ura_Daraja.밀리초() - Tafiyar_da < 1000) {
            if (na_ura_Daraja.밀리초() - 다음요청 >= 0) { 주소요청(다음); 다음요청 += 300; }
            Tabbatar_da();
            if (찾은주소 == 다음) return 0;
            na_ura_Daraja.잠시양보();
        }
        return -110;
    }
    static int Aika(int Mariki_Daraja, int imel, int lambar_kafa, int[] Tarin_bayani, int Tsawo_Daraja) {
        int rami_Mashigar_bayanai = Indes(Mariki_Daraja);
        if (rami_Mashigar_bayanai < 0) return -9;
        if (Hanyar_sadarwa_diraiba.입출력기준주소 == 0) return -19;
        if (lambar_kafa < 1 || lambar_kafa > 65535 || Tsawo_Daraja < 0 || Tsawo_Daraja > 1024) return -22;
        int 결과 = nema_imel(imel);
        if (결과 < 0) return 결과;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + Tsawo_Daraja);
        넣기16(출력틀, 18, mai_ganewa_Daraja++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, imel);
        넣기16(출력틀, 24, ~합(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[rami_Mashigar_bayanai]); 넣기16(출력틀, 36, lambar_kafa);
        넣기16(출력틀, 38, Tsawo_Daraja + 8); 넣기16(출력틀, 40, 0);
        for (int Indes = 0; Indes < Tsawo_Daraja; Indes++) 출력틀[42 + Indes] = Tarin_bayani[Indes] & 255;
        int checksum = (~합(출력틀, 34, Tsawo_Daraja + 8, 가상머리합(내주소, imel, Tsawo_Daraja + 8))) & 65535;
        넣기16(출력틀, 40, checksum == 0 ? 65535 : checksum);
        결과 = Hanyar_sadarwa_diraiba.Aika(출력틀, Tsawo_Daraja + 42);
        return 결과 < 0 ? 결과 : Tsawo_Daraja;
    }
    static int 받기(int Mariki_Daraja, int[] Tarin_bayani, int 용량, int 제한) {
        int rami_Mashigar_bayanai = Indes(Mariki_Daraja);
        if (rami_Mashigar_bayanai < 0) return -9;
        int Tafiyar_da = na_ura_Daraja.밀리초();
        while (true) {
            Tabbatar_da();
            int Tsawo_Daraja = 받은길이[rami_Mashigar_bayanai];
            if (Tsawo_Daraja >= 0) {
                받은길이[rami_Mashigar_bayanai] = -1;
                if (Tsawo_Daraja > 용량) return -90;
                for (int Indes = 0; Indes < Tsawo_Daraja; Indes++) Tarin_bayani[Indes] = 받은자료[rami_Mashigar_bayanai * 1024 + Indes];
                return Tsawo_Daraja;
            }
            if (제한 == 0) return -11;
            if (na_ura_Daraja.밀리초() - Tafiyar_da >= 제한) return -110;
            na_ura_Daraja.잠시양보();
        }
    }
    static void Matsayi_Daraja() {
        문자단말.Yi_Rubutu(Hanyar_sadarwa_diraiba.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        문자단말.Yi_Rubutu("TX: "); 문자단말.수쓰기(Hanyar_sadarwa_diraiba.송신수);
        문자단말.Yi_Rubutu(" RX: "); 문자단말.수쓰기(Hanyar_sadarwa_diraiba.수신수);
        문자단말.Yi_Rubutu(" DROP: "); 문자단말.수쓰기(폐기수);
        문자단말.Yi_Rubutu("\n");
    }
}
