// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** statiki_baha IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class Tor_Desse {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int Tor_örtük = 0xffffff00; /* ip.conf:NETMASK */
    static final int şlýuz_baha = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], 받은길이 = new int[4], 받은주소 = new int[4], 받은접속번호 = new int[4];
    static int[] 받은자료 = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, tanaýjy_baha = 0, 폐기수 = 0;

    static int bitin_16(int[] kadr_indeks, int 위치) { return (kadr_indeks[위치] << 8) | kadr_indeks[위치 + 1]; }
    static int bitin_32(int[] kadr_indeks, int 위치) { return (bitin_16(kadr_indeks, 위치) << 16) | bitin_16(kadr_indeks, 위치 + 2); }
    static void 넣기16(int[] kadr_indeks, int 위치, int baha) { kadr_indeks[위치] = (baha >>> 8) & 255; kadr_indeks[위치 + 1] = baha & 255; }
    static void 넣기32(int[] kadr_indeks, int 위치, int baha) { 넣기16(kadr_indeks, 위치, baha >>> 16); 넣기16(kadr_indeks, 위치 + 2, baha); }
    static int 합(int[] kadr_indeks, int Bitir, int dowamlylyk_baha, int baha) {
        for (int indeks = 0; indeks < dowamlylyk_baha; indeks += 2)
            baha += (kadr_indeks[Bitir + indeks] << 8) | (indeks + 1 < dowamlylyk_baha ? kadr_indeks[Bitir + indeks + 1] : 0);
        while ((baha >>> 16) != 0) baha = (baha & 65535) + (baha >>> 16);
        return baha;
    }
    static int 가상머리합(int 출발, int 도착, int dowamlylyk_baha) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + dowamlylyk_baha;
    }

    static void Päkize_Proses() {
        for (int indeks = 0; indeks < 4; indeks++) {
            접속번호들[indeks] = 0; 받은길이[indeks] = -1; 받은주소[indeks] = 0; 받은접속번호[indeks] = 0;
        }
        for (int indeks = 0; indeks < 64; indeks++) if (Tor_draýwer.받기(입력틀) == 0) break;
    }
    static int indeks(int ryçag_baha) { return ryçag_baha >= 3 && ryçag_baha < 7 && 접속번호들[ryçag_baha - 3] != 0 ? ryçag_baha - 3 : -1; }
    static int Aç(int 접속번호) {
        if (Tor_draýwer.입출력기준주소 == 0) return -19;
        if (접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 != 0) for (int indeks = 0; indeks < 4; indeks++) if (접속번호들[indeks] == 접속번호) return -98;
        for (int indeks = 0; indeks < 4; indeks++) if (접속번호들[indeks] == 0) {
            if (접속번호 == 0) {
                접속번호 = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int 앞 = 0; 앞 < 4; 앞++) if (접속번호들[앞] == 접속번호) 겹침 = true;
                    if (겹침) 접속번호++;
                }
            }
            접속번호들[indeks] = 접속번호; 받은길이[indeks] = -1;
            return indeks + 3;
        }
        return -24;
    }
    static int Ýap(int ryçag_baha) {
        int ýer_girizmeklik = indeks(ryçag_baha);
        if (ýer_girizmeklik < 0) return -9;
        접속번호들[ýer_girizmeklik] = 0; 받은길이[ýer_girizmeklik] = -1;
        return 0;
    }
    static int deň_derejeli_düwün_salgy(int ryçag_baha) { int ýer_girizmeklik = indeks(ryçag_baha); return ýer_girizmeklik < 0 ? -9 : 받은주소[ýer_girizmeklik]; }
    static int 상대접속번호(int ryçag_baha) { int ýer_girizmeklik = indeks(ryçag_baha); return ýer_girizmeklik < 0 ? -9 : 받은접속번호[ýer_girizmeklik]; }

    static void 바깥머리(int 종류, boolean 방송) {
        for (int indeks = 0; indeks < 6; indeks++) {
            출력틀[indeks] = 방송 ? 255 : 찾은장치[indeks];
            출력틀[6 + indeks] = Tor_draýwer.enjam_salgy[indeks];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void 주소요청(int barylmaly_ýer_baha) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int indeks = 0; indeks < 6; indeks++) {
            출력틀[22 + indeks] = Tor_draýwer.enjam_salgy[indeks]; 출력틀[32 + indeks] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, barylmaly_ýer_baha);
        Tor_draýwer.iber(출력틀, 42);
    }
    static void Proses_salgy(int dowamlylyk_baha) {
        if (dowamlylyk_baha < 42 || bitin_16(입력틀, 14) != 1 || bitin_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || bitin_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = bitin_16(입력틀, 20), deň_derejeli_düwün_baha = bitin_32(입력틀, 28);
        if (종류 == 2 && deň_derejeli_düwün_baha == 찾을주소) {
            for (int indeks = 0; indeks < 6; indeks++) {
                if (입력틀[6 + indeks] != 입력틀[22 + indeks] || 입력틀[32 + indeks] != Tor_draýwer.enjam_salgy[indeks]) return;
            }
            for (int indeks = 0; indeks < 6; indeks++) 찾은장치[indeks] = 입력틀[22 + indeks];
            찾은주소 = deň_derejeli_düwün_baha;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int indeks = 0; indeks < 6; indeks++) {
                출력틀[indeks] = 입력틀[22 + indeks]; 출력틀[32 + indeks] = 입력틀[22 + indeks];
                출력틀[22 + indeks] = Tor_draýwer.enjam_salgy[indeks];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, deň_derejeli_düwün_baha);
            Tor_draýwer.iber(출력틀, 42);
        }
    }

    static void Proses_kadr(int dowamlylyk_baha) {
        if (dowamlylyk_baha < 14 || dowamlylyk_baha > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, 방송 = true;
        for (int indeks = 0; indeks < 6; indeks++) {
            if (입력틀[indeks] != Tor_draýwer.enjam_salgy[indeks]) 자기 = false;
            if (입력틀[indeks] != 255) 방송 = false;
        }
        if (!자기 && !방송) return;
        if (bitin_16(입력틀, 12) == 0x0806) { Proses_salgy(dowamlylyk_baha); return; }
        if (bitin_16(입력틀, 12) != 0x0800) return;
        if (dowamlylyk_baha < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int At_dowamlylyk = (입력틀[14] & 15) * 4, 전체길이 = bitin_16(입력틀, 16);
        if (At_dowamlylyk < 20 || At_dowamlylyk > 60 || 전체길이 < At_dowamlylyk + 8 || 전체길이 > dowamlylyk_baha - 14
            || (bitin_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || bitin_32(입력틀, 30) != 내주소 || 합(입력틀, 14, At_dowamlylyk, 0) != 65535) { 폐기수++; return; }
        int Bitir = 14 + At_dowamlylyk, maglumat_dowamlylyk = bitin_16(입력틀, Bitir + 4);
        if (maglumat_dowamlylyk < 8 || maglumat_dowamlylyk != 전체길이 - At_dowamlylyk || maglumat_dowamlylyk > 1032) { 폐기수++; return; }
        int 출발 = bitin_32(입력틀, 26);
        if (bitin_16(입력틀, Bitir + 6) != 0 && 합(입력틀, Bitir, maglumat_dowamlylyk, 가상머리합(출발, 내주소, maglumat_dowamlylyk)) != 65535) {
            폐기수++; return;
        }
        int barylmaly_ýer_baha = bitin_16(입력틀, Bitir + 2);
        for (int ýer_girizmeklik = 0; ýer_girizmeklik < 4; ýer_girizmeklik++) if (접속번호들[ýer_girizmeklik] != 0 && 접속번호들[ýer_girizmeklik] == barylmaly_ýer_baha) {
            if (받은길이[ýer_girizmeklik] >= 0) { 폐기수++; return; }
            받은길이[ýer_girizmeklik] = maglumat_dowamlylyk - 8; 받은주소[ýer_girizmeklik] = 출발; 받은접속번호[ýer_girizmeklik] = bitin_16(입력틀, Bitir);
            for (int indeks = 0; indeks < maglumat_dowamlylyk - 8; indeks++) 받은자료[ýer_girizmeklik * 1024 + indeks] = 입력틀[Bitir + 8 + indeks];
            return;
        }
    }

    static void barla() {
        for (int indeks = 0; indeks < 16; indeks++) {
            int dowamlylyk_baha = Tor_draýwer.받기(입력틀);
            if (dowamlylyk_baha == 0) return;
            Proses_kadr(dowamlylyk_baha);
        }
    }
    static int tap_salgy(int salgy) {
        if (salgy == 0 || salgy == -1 || (salgy >>> 28) >= 14 || (salgy >>> 24) == 127 || salgy == 내주소) return -101;
        int 다음 = (salgy & Tor_örtük) == (내주소 & Tor_örtük) ? salgy : şlýuz_baha;
        if (다음 == 찾은주소) return 0;
        찾을주소 = 다음;
        int Bitir = enjam_baha.밀리초(), 다음요청 = Bitir;
        while (enjam_baha.밀리초() - Bitir < 1000) {
            if (enjam_baha.밀리초() - 다음요청 >= 0) { 주소요청(다음); 다음요청 += 300; }
            barla();
            if (찾은주소 == 다음) return 0;
            enjam_baha.잠시양보();
        }
        return -110;
    }
    static int iber(int ryçag_baha, int salgy, int 접속번호, int[] maglumat, int dowamlylyk_baha) {
        int ýer_girizmeklik = indeks(ryçag_baha);
        if (ýer_girizmeklik < 0) return -9;
        if (Tor_draýwer.입출력기준주소 == 0) return -19;
        if (접속번호 < 1 || 접속번호 > 65535 || dowamlylyk_baha < 0 || dowamlylyk_baha > 1024) return -22;
        int 결과 = tap_salgy(salgy);
        if (결과 < 0) return 결과;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + dowamlylyk_baha);
        넣기16(출력틀, 18, tanaýjy_baha++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, salgy);
        넣기16(출력틀, 24, ~합(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[ýer_girizmeklik]); 넣기16(출력틀, 36, 접속번호);
        넣기16(출력틀, 38, dowamlylyk_baha + 8); 넣기16(출력틀, 40, 0);
        for (int indeks = 0; indeks < dowamlylyk_baha; indeks++) 출력틀[42 + indeks] = maglumat[indeks] & 255;
        int 검사합 = (~합(출력틀, 34, dowamlylyk_baha + 8, 가상머리합(내주소, salgy, dowamlylyk_baha + 8))) & 65535;
        넣기16(출력틀, 40, 검사합 == 0 ? 65535 : 검사합);
        결과 = Tor_draýwer.iber(출력틀, dowamlylyk_baha + 42);
        return 결과 < 0 ? 결과 : dowamlylyk_baha;
    }
    static int 받기(int ryçag_baha, int[] maglumat, int 용량, int 제한) {
        int ýer_girizmeklik = indeks(ryçag_baha);
        if (ýer_girizmeklik < 0) return -9;
        int Bitir = enjam_baha.밀리초();
        while (true) {
            barla();
            int dowamlylyk_baha = 받은길이[ýer_girizmeklik];
            if (dowamlylyk_baha >= 0) {
                받은길이[ýer_girizmeklik] = -1;
                if (dowamlylyk_baha > 용량) return -90;
                for (int indeks = 0; indeks < dowamlylyk_baha; indeks++) maglumat[indeks] = 받은자료[ýer_girizmeklik * 1024 + indeks];
                return dowamlylyk_baha;
            }
            if (제한 == 0) return -11;
            if (enjam_baha.밀리초() - Bitir >= 제한) return -110;
            enjam_baha.잠시양보();
        }
    }
    static void ýagdaý_baha() {
        문자단말.Ýaz(Tor_draýwer.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        문자단말.Ýaz("TX: "); 문자단말.수쓰기(Tor_draýwer.송신수);
        문자단말.Ýaz(" RX: "); 문자단말.수쓰기(Tor_draýwer.수신수);
        문자단말.Ýaz(" DROP: "); 문자단말.수쓰기(폐기수);
        문자단말.Ýaz("\n");
    }
}
