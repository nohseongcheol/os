// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** surravviqanngittuq_atuutilik IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class 통신망 {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int Kasuqatigiitsimajut_kiinappak = 0xffffff00; /* ip.conf:NETMASK */
    static final int aqqusiurut_atuutilik = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], 받은길이 = new int[4], 받은주소 = new int[4], 받은접속번호 = new int[4];
    static int[] 받은자료 = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, 식별자 = 0, 폐기수 = 0;

    static int naasaut_16(int[] avalu_nalunaiqsimavik, int 위치) { return (avalu_nalunaiqsimavik[위치] << 8) | avalu_nalunaiqsimavik[위치 + 1]; }
    static int naasaut_32(int[] avalu_nalunaiqsimavik, int 위치) { return (naasaut_16(avalu_nalunaiqsimavik, 위치) << 16) | naasaut_16(avalu_nalunaiqsimavik, 위치 + 2); }
    static void 넣기16(int[] avalu_nalunaiqsimavik, int 위치, int atuutilik) { avalu_nalunaiqsimavik[위치] = (atuutilik >>> 8) & 255; avalu_nalunaiqsimavik[위치 + 1] = atuutilik & 255; }
    static void 넣기32(int[] avalu_nalunaiqsimavik, int 위치, int atuutilik) { 넣기16(avalu_nalunaiqsimavik, 위치, atuutilik >>> 16); 넣기16(avalu_nalunaiqsimavik, 위치 + 2, atuutilik); }
    static int 합(int[] avalu_nalunaiqsimavik, int 시작, int takininga_atuutilik, int atuutilik) {
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < takininga_atuutilik; nalunaiqsimavik += 2)
            atuutilik += (avalu_nalunaiqsimavik[시작 + nalunaiqsimavik] << 8) | (nalunaiqsimavik + 1 < takininga_atuutilik ? avalu_nalunaiqsimavik[시작 + nalunaiqsimavik + 1] : 0);
        while ((atuutilik >>> 16) != 0) atuutilik = (atuutilik & 65535) + (atuutilik >>> 16);
        return atuutilik;
    }
    static int 가상머리합(int 출발, int 도착, int takininga_atuutilik) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + takininga_atuutilik;
    }

    static void 과정정리() {
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 4; nalunaiqsimavik++) {
            접속번호들[nalunaiqsimavik] = 0; 받은길이[nalunaiqsimavik] = -1; 받은주소[nalunaiqsimavik] = 0; 받은접속번호[nalunaiqsimavik] = 0;
        }
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 64; nalunaiqsimavik++) if (Kasuqatigiitsimajut_qarasaujalirijjut.받기(입력틀) == 0) break;
    }
    static int nalunaiqsimavik(int nuuttarut_atuutilik) { return nuuttarut_atuutilik >= 3 && nuuttarut_atuutilik < 7 && 접속번호들[nuuttarut_atuutilik - 3] != 0 ? nuuttarut_atuutilik - 3 : -1; }
    static int matuirli(int 접속번호) {
        if (Kasuqatigiitsimajut_qarasaujalirijjut.입출력기준주소 == 0) return -19;
        if (접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 != 0) for (int nalunaiqsimavik = 0; nalunaiqsimavik < 4; nalunaiqsimavik++) if (접속번호들[nalunaiqsimavik] == 접속번호) return -98;
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 4; nalunaiqsimavik++) if (접속번호들[nalunaiqsimavik] == 0) {
            if (접속번호 == 0) {
                접속번호 = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int 앞 = 0; 앞 < 4; 앞++) if (접속번호들[앞] == 접속번호) 겹침 = true;
                    if (겹침) 접속번호++;
                }
            }
            접속번호들[nalunaiqsimavik] = 접속번호; 받은길이[nalunaiqsimavik] = -1;
            return nalunaiqsimavik + 3;
        }
        return -24;
    }
    static int matuli(int nuuttarut_atuutilik) {
        int 칸 = nalunaiqsimavik(nuuttarut_atuutilik);
        if (칸 < 0) return -9;
        접속번호들[칸] = 0; 받은길이[칸] = -1;
        return 0;
    }
    static int ilagijaujuq_turaarut(int nuuttarut_atuutilik) { int 칸 = nalunaiqsimavik(nuuttarut_atuutilik); return 칸 < 0 ? -9 : 받은주소[칸]; }
    static int 상대접속번호(int nuuttarut_atuutilik) { int 칸 = nalunaiqsimavik(nuuttarut_atuutilik); return 칸 < 0 ? -9 : 받은접속번호[칸]; }

    static void 바깥머리(int 종류, boolean 방송) {
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 6; nalunaiqsimavik++) {
            출력틀[nalunaiqsimavik] = 방송 ? 255 : 찾은장치[nalunaiqsimavik];
            출력틀[6 + nalunaiqsimavik] = Kasuqatigiitsimajut_qarasaujalirijjut.sunakkutaaq_turaarut[nalunaiqsimavik];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void 주소요청(int namunngarvik_atuutilik) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 6; nalunaiqsimavik++) {
            출력틀[22 + nalunaiqsimavik] = Kasuqatigiitsimajut_qarasaujalirijjut.sunakkutaaq_turaarut[nalunaiqsimavik]; 출력틀[32 + nalunaiqsimavik] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, namunngarvik_atuutilik);
        Kasuqatigiitsimajut_qarasaujalirijjut.nassiutili(출력틀, 42);
    }
    static void Pivallianiq_turaarut(int takininga_atuutilik) {
        if (takininga_atuutilik < 42 || naasaut_16(입력틀, 14) != 1 || naasaut_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || naasaut_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = naasaut_16(입력틀, 20), ilagijaujuq_atuutilik = naasaut_32(입력틀, 28);
        if (종류 == 2 && ilagijaujuq_atuutilik == 찾을주소) {
            for (int nalunaiqsimavik = 0; nalunaiqsimavik < 6; nalunaiqsimavik++) {
                if (입력틀[6 + nalunaiqsimavik] != 입력틀[22 + nalunaiqsimavik] || 입력틀[32 + nalunaiqsimavik] != Kasuqatigiitsimajut_qarasaujalirijjut.sunakkutaaq_turaarut[nalunaiqsimavik]) return;
            }
            for (int nalunaiqsimavik = 0; nalunaiqsimavik < 6; nalunaiqsimavik++) 찾은장치[nalunaiqsimavik] = 입력틀[22 + nalunaiqsimavik];
            찾은주소 = ilagijaujuq_atuutilik;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int nalunaiqsimavik = 0; nalunaiqsimavik < 6; nalunaiqsimavik++) {
                출력틀[nalunaiqsimavik] = 입력틀[22 + nalunaiqsimavik]; 출력틀[32 + nalunaiqsimavik] = 입력틀[22 + nalunaiqsimavik];
                출력틀[22 + nalunaiqsimavik] = Kasuqatigiitsimajut_qarasaujalirijjut.sunakkutaaq_turaarut[nalunaiqsimavik];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, ilagijaujuq_atuutilik);
            Kasuqatigiitsimajut_qarasaujalirijjut.nassiutili(출력틀, 42);
        }
    }

    static void Pivallianiq_avalu(int takininga_atuutilik) {
        if (takininga_atuutilik < 14 || takininga_atuutilik > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, 방송 = true;
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 6; nalunaiqsimavik++) {
            if (입력틀[nalunaiqsimavik] != Kasuqatigiitsimajut_qarasaujalirijjut.sunakkutaaq_turaarut[nalunaiqsimavik]) 자기 = false;
            if (입력틀[nalunaiqsimavik] != 255) 방송 = false;
        }
        if (!자기 && !방송) return;
        if (naasaut_16(입력틀, 12) == 0x0806) { Pivallianiq_turaarut(takininga_atuutilik); return; }
        if (naasaut_16(입력틀, 12) != 0x0800) return;
        if (takininga_atuutilik < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int Taijaugusinga_takininga = (입력틀[14] & 15) * 4, 전체길이 = naasaut_16(입력틀, 16);
        if (Taijaugusinga_takininga < 20 || Taijaugusinga_takininga > 60 || 전체길이 < Taijaugusinga_takininga + 8 || 전체길이 > takininga_atuutilik - 14
            || (naasaut_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || naasaut_32(입력틀, 30) != 내주소 || 합(입력틀, 14, Taijaugusinga_takininga, 0) != 65535) { 폐기수++; return; }
        int 시작 = 14 + Taijaugusinga_takininga, titiqqat_takininga = naasaut_16(입력틀, 시작 + 4);
        if (titiqqat_takininga < 8 || titiqqat_takininga != 전체길이 - Taijaugusinga_takininga || titiqqat_takininga > 1032) { 폐기수++; return; }
        int 출발 = naasaut_32(입력틀, 26);
        if (naasaut_16(입력틀, 시작 + 6) != 0 && 합(입력틀, 시작, titiqqat_takininga, 가상머리합(출발, 내주소, titiqqat_takininga)) != 65535) {
            폐기수++; return;
        }
        int namunngarvik_atuutilik = naasaut_16(입력틀, 시작 + 2);
        for (int 칸 = 0; 칸 < 4; 칸++) if (접속번호들[칸] != 0 && 접속번호들[칸] == namunngarvik_atuutilik) {
            if (받은길이[칸] >= 0) { 폐기수++; return; }
            받은길이[칸] = titiqqat_takininga - 8; 받은주소[칸] = 출발; 받은접속번호[칸] = naasaut_16(입력틀, 시작);
            for (int nalunaiqsimavik = 0; nalunaiqsimavik < titiqqat_takininga - 8; nalunaiqsimavik++) 받은자료[칸 * 1024 + nalunaiqsimavik] = 입력틀[시작 + 8 + nalunaiqsimavik];
            return;
        }
    }

    static void nalunairli_1aacb54c() {
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 16; nalunaiqsimavik++) {
            int takininga_atuutilik = Kasuqatigiitsimajut_qarasaujalirijjut.받기(입력틀);
            if (takininga_atuutilik == 0) return;
            Pivallianiq_avalu(takininga_atuutilik);
        }
    }
    static int nanili_turaarut(int turaarut) {
        if (turaarut == 0 || turaarut == -1 || (turaarut >>> 28) >= 14 || (turaarut >>> 24) == 127 || turaarut == 내주소) return -101;
        int 다음 = (turaarut & Kasuqatigiitsimajut_kiinappak) == (내주소 & Kasuqatigiitsimajut_kiinappak) ? turaarut : aqqusiurut_atuutilik;
        if (다음 == 찾은주소) return 0;
        찾을주소 = 다음;
        int 시작 = sunakkutaaq_atuutilik.밀리초(), 다음요청 = 시작;
        while (sunakkutaaq_atuutilik.밀리초() - 시작 < 1000) {
            if (sunakkutaaq_atuutilik.밀리초() - 다음요청 >= 0) { 주소요청(다음); 다음요청 += 300; }
            nalunairli_1aacb54c();
            if (찾은주소 == 다음) return 0;
            sunakkutaaq_atuutilik.잠시양보();
        }
        return -110;
    }
    static int nassiutili(int nuuttarut_atuutilik, int turaarut, int 접속번호, int[] titiqqat, int takininga_atuutilik) {
        int 칸 = nalunaiqsimavik(nuuttarut_atuutilik);
        if (칸 < 0) return -9;
        if (Kasuqatigiitsimajut_qarasaujalirijjut.입출력기준주소 == 0) return -19;
        if (접속번호 < 1 || 접속번호 > 65535 || takininga_atuutilik < 0 || takininga_atuutilik > 1024) return -22;
        int 결과 = nanili_turaarut(turaarut);
        if (결과 < 0) return 결과;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + takininga_atuutilik);
        넣기16(출력틀, 18, 식별자++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, turaarut);
        넣기16(출력틀, 24, ~합(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[칸]); 넣기16(출력틀, 36, 접속번호);
        넣기16(출력틀, 38, takininga_atuutilik + 8); 넣기16(출력틀, 40, 0);
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < takininga_atuutilik; nalunaiqsimavik++) 출력틀[42 + nalunaiqsimavik] = titiqqat[nalunaiqsimavik] & 255;
        int 검사합 = (~합(출력틀, 34, takininga_atuutilik + 8, 가상머리합(내주소, turaarut, takininga_atuutilik + 8))) & 65535;
        넣기16(출력틀, 40, 검사합 == 0 ? 65535 : 검사합);
        결과 = Kasuqatigiitsimajut_qarasaujalirijjut.nassiutili(출력틀, takininga_atuutilik + 42);
        return 결과 < 0 ? 결과 : takininga_atuutilik;
    }
    static int 받기(int nuuttarut_atuutilik, int[] titiqqat, int 용량, int 제한) {
        int 칸 = nalunaiqsimavik(nuuttarut_atuutilik);
        if (칸 < 0) return -9;
        int 시작 = sunakkutaaq_atuutilik.밀리초();
        while (true) {
            nalunairli_1aacb54c();
            int takininga_atuutilik = 받은길이[칸];
            if (takininga_atuutilik >= 0) {
                받은길이[칸] = -1;
                if (takininga_atuutilik > 용량) return -90;
                for (int nalunaiqsimavik = 0; nalunaiqsimavik < takininga_atuutilik; nalunaiqsimavik++) titiqqat[nalunaiqsimavik] = 받은자료[칸 * 1024 + nalunaiqsimavik];
                return takininga_atuutilik;
            }
            if (제한 == 0) return -11;
            if (sunakkutaaq_atuutilik.밀리초() - 시작 >= 제한) return -110;
            sunakkutaaq_atuutilik.잠시양보();
        }
    }
    static void qanuilinganiq_atuutilik() {
        문자단말.titiraq(Kasuqatigiitsimajut_qarasaujalirijjut.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        문자단말.titiraq("TX: "); 문자단말.수쓰기(Kasuqatigiitsimajut_qarasaujalirijjut.송신수);
        문자단말.titiraq(" RX: "); 문자단말.수쓰기(Kasuqatigiitsimajut_qarasaujalirijjut.수신수);
        문자단말.titiraq(" DROP: "); 문자단말.수쓰기(폐기수);
        문자단말.titiraq("\n");
    }
}
