// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** adịmgbanwò_valuu IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class Netwọọkụ_ikpo {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int Netwọọkụ_mkpù = 0xffffff00; /* ip.conf:NETMASK */
    static final int ụzọmbànye_valuu = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], 받은길이 = new int[4], 받은주소 = new int[4], 받은접속번호 = new int[4];
    static int[] 받은자료 = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, ihe_nkọwapụta_valuu = 0, 폐기수 = 0;

    static int ọnụọgụ_nzùrùòkè_16(int[] okpokoro_indèks, int 위치) { return (okpokoro_indèks[위치] << 8) | okpokoro_indèks[위치 + 1]; }
    static int ọnụọgụ_nzùrùòkè_32(int[] okpokoro_indèks, int 위치) { return (ọnụọgụ_nzùrùòkè_16(okpokoro_indèks, 위치) << 16) | ọnụọgụ_nzùrùòkè_16(okpokoro_indèks, 위치 + 2); }
    static void 넣기16(int[] okpokoro_indèks, int 위치, int valuu) { okpokoro_indèks[위치] = (valuu >>> 8) & 255; okpokoro_indèks[위치 + 1] = valuu & 255; }
    static void 넣기32(int[] okpokoro_indèks, int 위치, int valuu) { 넣기16(okpokoro_indèks, 위치, valuu >>> 16); 넣기16(okpokoro_indèks, 위치 + 2, valuu); }
    static int 합(int[] okpokoro_indèks, int Bido, int ogologo_valuu, int valuu) {
        for (int indèks = 0; indèks < ogologo_valuu; indèks += 2)
            valuu += (okpokoro_indèks[Bido + indèks] << 8) | (indèks + 1 < ogologo_valuu ? okpokoro_indèks[Bido + indèks + 1] : 0);
        while ((valuu >>> 16) != 0) valuu = (valuu & 65535) + (valuu >>> 16);
        return valuu;
    }
    static int 가상머리합(int 출발, int 도착, int ogologo_valuu) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + ogologo_valuu;
    }

    static void 과정정리() {
        for (int indèks = 0; indèks < 4; indèks++) {
            접속번호들[indèks] = 0; 받은길이[indèks] = -1; 받은주소[indèks] = 0; 받은접속번호[indèks] = 0;
        }
        for (int indèks = 0; indèks < 64; indèks++) if (Netwọọkụ_ǹnyà.받기(입력틀) == 0) break;
    }
    static int indèks(int ebenjìaka_valuu) { return ebenjìaka_valuu >= 3 && ebenjìaka_valuu < 7 && 접속번호들[ebenjìaka_valuu - 3] != 0 ? ebenjìaka_valuu - 3 : -1; }
    static int Mepee(int 접속번호) {
        if (Netwọọkụ_ǹnyà.입출력기준주소 == 0) return -19;
        if (접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 != 0) for (int indèks = 0; indèks < 4; indèks++) if (접속번호들[indèks] == 접속번호) return -98;
        for (int indèks = 0; indèks < 4; indèks++) if (접속번호들[indèks] == 0) {
            if (접속번호 == 0) {
                접속번호 = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int 앞 = 0; 앞 < 4; 앞++) if (접속번호들[앞] == 접속번호) 겹침 = true;
                    if (겹침) 접속번호++;
                }
            }
            접속번호들[indèks] = 접속번호; 받은길이[indèks] = -1;
            return indèks + 3;
        }
        return -24;
    }
    static int Mechie(int ebenjìaka_valuu) {
        int oghere_ndebà = indèks(ebenjìaka_valuu);
        if (oghere_ndebà < 0) return -9;
        접속번호들[oghere_ndebà] = 0; 받은길이[oghere_ndebà] = -1;
        return 0;
    }
    static int ibè_àdreèsì(int ebenjìaka_valuu) { int oghere_ndebà = indèks(ebenjìaka_valuu); return oghere_ndebà < 0 ? -9 : 받은주소[oghere_ndebà]; }
    static int 상대접속번호(int ebenjìaka_valuu) { int oghere_ndebà = indèks(ebenjìaka_valuu); return oghere_ndebà < 0 ? -9 : 받은접속번호[oghere_ndebà]; }

    static void 바깥머리(int 종류, boolean 방송) {
        for (int indèks = 0; indèks < 6; indèks++) {
            출력틀[indèks] = 방송 ? 255 : 찾은장치[indèks];
            출력틀[6 + indèks] = Netwọọkụ_ǹnyà.njìarụ_àdreèsì[indèks];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void 주소요청(int ebemwèga_valuu) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int indèks = 0; indèks < 6; indèks++) {
            출력틀[22 + indèks] = Netwọọkụ_ǹnyà.njìarụ_àdreèsì[indèks]; 출력틀[32 + indèks] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, ebemwèga_valuu);
        Netwọọkụ_ǹnyà.zìga(출력틀, 42);
    }
    static void ùsòrò_àdreèsì(int ogologo_valuu) {
        if (ogologo_valuu < 42 || ọnụọgụ_nzùrùòkè_16(입력틀, 14) != 1 || ọnụọgụ_nzùrùòkè_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || ọnụọgụ_nzùrùòkè_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = ọnụọgụ_nzùrùòkè_16(입력틀, 20), ibè_valuu = ọnụọgụ_nzùrùòkè_32(입력틀, 28);
        if (종류 == 2 && ibè_valuu == 찾을주소) {
            for (int indèks = 0; indèks < 6; indèks++) {
                if (입력틀[6 + indèks] != 입력틀[22 + indèks] || 입력틀[32 + indèks] != Netwọọkụ_ǹnyà.njìarụ_àdreèsì[indèks]) return;
            }
            for (int indèks = 0; indèks < 6; indèks++) 찾은장치[indèks] = 입력틀[22 + indèks];
            찾은주소 = ibè_valuu;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int indèks = 0; indèks < 6; indèks++) {
                출력틀[indèks] = 입력틀[22 + indèks]; 출력틀[32 + indèks] = 입력틀[22 + indèks];
                출력틀[22 + indèks] = Netwọọkụ_ǹnyà.njìarụ_àdreèsì[indèks];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, ibè_valuu);
            Netwọọkụ_ǹnyà.zìga(출력틀, 42);
        }
    }

    static void ùsòrò_okpokoro(int ogologo_valuu) {
        if (ogologo_valuu < 14 || ogologo_valuu > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, 방송 = true;
        for (int indèks = 0; indèks < 6; indèks++) {
            if (입력틀[indèks] != Netwọọkụ_ǹnyà.njìarụ_àdreèsì[indèks]) 자기 = false;
            if (입력틀[indèks] != 255) 방송 = false;
        }
        if (!자기 && !방송) return;
        if (ọnụọgụ_nzùrùòkè_16(입력틀, 12) == 0x0806) { ùsòrò_àdreèsì(ogologo_valuu); return; }
        if (ọnụọgụ_nzùrùòkè_16(입력틀, 12) != 0x0800) return;
        if (ogologo_valuu < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int isi_ogologo = (입력틀[14] & 15) * 4, 전체길이 = ọnụọgụ_nzùrùòkè_16(입력틀, 16);
        if (isi_ogologo < 20 || isi_ogologo > 60 || 전체길이 < isi_ogologo + 8 || 전체길이 > ogologo_valuu - 14
            || (ọnụọgụ_nzùrùòkè_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || ọnụọgụ_nzùrùòkè_32(입력틀, 30) != 내주소 || 합(입력틀, 14, isi_ogologo, 0) != 65535) { 폐기수++; return; }
        int Bido = 14 + isi_ogologo, datà_ogologo = ọnụọgụ_nzùrùòkè_16(입력틀, Bido + 4);
        if (datà_ogologo < 8 || datà_ogologo != 전체길이 - isi_ogologo || datà_ogologo > 1032) { 폐기수++; return; }
        int 출발 = ọnụọgụ_nzùrùòkè_32(입력틀, 26);
        if (ọnụọgụ_nzùrùòkè_16(입력틀, Bido + 6) != 0 && 합(입력틀, Bido, datà_ogologo, 가상머리합(출발, 내주소, datà_ogologo)) != 65535) {
            폐기수++; return;
        }
        int ebemwèga_valuu = ọnụọgụ_nzùrùòkè_16(입력틀, Bido + 2);
        for (int oghere_ndebà = 0; oghere_ndebà < 4; oghere_ndebà++) if (접속번호들[oghere_ndebà] != 0 && 접속번호들[oghere_ndebà] == ebemwèga_valuu) {
            if (받은길이[oghere_ndebà] >= 0) { 폐기수++; return; }
            받은길이[oghere_ndebà] = datà_ogologo - 8; 받은주소[oghere_ndebà] = 출발; 받은접속번호[oghere_ndebà] = ọnụọgụ_nzùrùòkè_16(입력틀, Bido);
            for (int indèks = 0; indèks < datà_ogologo - 8; indèks++) 받은자료[oghere_ndebà * 1024 + indèks] = 입력틀[Bido + 8 + indèks];
            return;
        }
    }

    static void nkwàdo_eziokwū() {
        for (int indèks = 0; indèks < 16; indèks++) {
            int ogologo_valuu = Netwọọkụ_ǹnyà.받기(입력틀);
            if (ogologo_valuu == 0) return;
            ùsòrò_okpokoro(ogologo_valuu);
        }
    }
    static int chọta_àdreèsì(int àdreèsì) {
        if (àdreèsì == 0 || àdreèsì == -1 || (àdreèsì >>> 28) >= 14 || (àdreèsì >>> 24) == 127 || àdreèsì == 내주소) return -101;
        int 다음 = (àdreèsì & Netwọọkụ_mkpù) == (내주소 & Netwọọkụ_mkpù) ? àdreèsì : ụzọmbànye_valuu;
        if (다음 == 찾은주소) return 0;
        찾을주소 = 다음;
        int Bido = njìarụ_valuu.밀리초(), 다음요청 = Bido;
        while (njìarụ_valuu.밀리초() - Bido < 1000) {
            if (njìarụ_valuu.밀리초() - 다음요청 >= 0) { 주소요청(다음); 다음요청 += 300; }
            nkwàdo_eziokwū();
            if (찾은주소 == 다음) return 0;
            njìarụ_valuu.잠시양보();
        }
        return -110;
    }
    static int zìga(int ebenjìaka_valuu, int àdreèsì, int 접속번호, int[] datà, int ogologo_valuu) {
        int oghere_ndebà = indèks(ebenjìaka_valuu);
        if (oghere_ndebà < 0) return -9;
        if (Netwọọkụ_ǹnyà.입출력기준주소 == 0) return -19;
        if (접속번호 < 1 || 접속번호 > 65535 || ogologo_valuu < 0 || ogologo_valuu > 1024) return -22;
        int 결과 = chọta_àdreèsì(àdreèsì);
        if (결과 < 0) return 결과;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + ogologo_valuu);
        넣기16(출력틀, 18, ihe_nkọwapụta_valuu++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, àdreèsì);
        넣기16(출력틀, 24, ~합(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[oghere_ndebà]); 넣기16(출력틀, 36, 접속번호);
        넣기16(출력틀, 38, ogologo_valuu + 8); 넣기16(출력틀, 40, 0);
        for (int indèks = 0; indèks < ogologo_valuu; indèks++) 출력틀[42 + indèks] = datà[indèks] & 255;
        int 검사합 = (~합(출력틀, 34, ogologo_valuu + 8, 가상머리합(내주소, àdreèsì, ogologo_valuu + 8))) & 65535;
        넣기16(출력틀, 40, 검사합 == 0 ? 65535 : 검사합);
        결과 = Netwọọkụ_ǹnyà.zìga(출력틀, ogologo_valuu + 42);
        return 결과 < 0 ? 결과 : ogologo_valuu;
    }
    static int 받기(int ebenjìaka_valuu, int[] datà, int 용량, int 제한) {
        int oghere_ndebà = indèks(ebenjìaka_valuu);
        if (oghere_ndebà < 0) return -9;
        int Bido = njìarụ_valuu.밀리초();
        while (true) {
            nkwàdo_eziokwū();
            int ogologo_valuu = 받은길이[oghere_ndebà];
            if (ogologo_valuu >= 0) {
                받은길이[oghere_ndebà] = -1;
                if (ogologo_valuu > 용량) return -90;
                for (int indèks = 0; indèks < ogologo_valuu; indèks++) datà[indèks] = 받은자료[oghere_ndebà * 1024 + indèks];
                return ogologo_valuu;
            }
            if (제한 == 0) return -11;
            if (njìarụ_valuu.밀리초() - Bido >= 제한) return -110;
            njìarụ_valuu.잠시양보();
        }
    }
    static void ọnọdụ_valuu() {
        문자단말.Chekwaa_ozi(Netwọọkụ_ǹnyà.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        문자단말.Chekwaa_ozi("TX: "); 문자단말.수쓰기(Netwọọkụ_ǹnyà.송신수);
        문자단말.Chekwaa_ozi(" RX: "); 문자단말.수쓰기(Netwọọkụ_ǹnyà.수신수);
        문자단말.Chekwaa_ozi(" DROP: "); 문자단말.수쓰기(폐기수);
        문자단말.Chekwaa_ozi("\n");
    }
}
