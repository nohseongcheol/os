// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ìdágún_iye IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class Alásopọ̀_kójọ {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int Alásopọ̀_asẹ́_iye = 0xffffff00; /* ip.conf:NETMASK */
    static final int ẹnu_odi_iye = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], 받은길이 = new int[4], 받은주소 = new int[4], 받은접속번호 = new int[4];
    static int[] 받은자료 = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, Àfidámọ̀_iye = 0, 폐기수 = 0;

    static int nọ́ńbà_odindi_16(int[] férèmù_wá_atọ̀ka_àkóónú, int 위치) { return (férèmù_wá_atọ̀ka_àkóónú[위치] << 8) | férèmù_wá_atọ̀ka_àkóónú[위치 + 1]; }
    static int nọ́ńbà_odindi_32(int[] férèmù_wá_atọ̀ka_àkóónú, int 위치) { return (nọ́ńbà_odindi_16(férèmù_wá_atọ̀ka_àkóónú, 위치) << 16) | nọ́ńbà_odindi_16(férèmù_wá_atọ̀ka_àkóónú, 위치 + 2); }
    static void 넣기16(int[] férèmù_wá_atọ̀ka_àkóónú, int 위치, int iye) { férèmù_wá_atọ̀ka_àkóónú[위치] = (iye >>> 8) & 255; férèmù_wá_atọ̀ka_àkóónú[위치 + 1] = iye & 255; }
    static void 넣기32(int[] férèmù_wá_atọ̀ka_àkóónú, int 위치, int iye) { 넣기16(férèmù_wá_atọ̀ka_àkóónú, 위치, iye >>> 16); 넣기16(férèmù_wá_atọ̀ka_àkóónú, 위치 + 2, iye); }
    static int 합(int[] férèmù_wá_atọ̀ka_àkóónú, int Rọ́ọ̀nù, int gígùn_iye, int iye) {
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < gígùn_iye; wá_atọ̀ka_àkóónú += 2)
            iye += (férèmù_wá_atọ̀ka_àkóónú[Rọ́ọ̀nù + wá_atọ̀ka_àkóónú] << 8) | (wá_atọ̀ka_àkóónú + 1 < gígùn_iye ? férèmù_wá_atọ̀ka_àkóónú[Rọ́ọ̀nù + wá_atọ̀ka_àkóónú + 1] : 0);
        while ((iye >>> 16) != 0) iye = (iye & 65535) + (iye >>> 16);
        return iye;
    }
    static int 가상머리합(int 출발, int 도착, int gígùn_iye) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + gígùn_iye;
    }

    static void 과정정리() {
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 4; wá_atọ̀ka_àkóónú++) {
            접속번호들[wá_atọ̀ka_àkóónú] = 0; 받은길이[wá_atọ̀ka_àkóónú] = -1; 받은주소[wá_atọ̀ka_àkóónú] = 0; 받은접속번호[wá_atọ̀ka_àkóónú] = 0;
        }
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 64; wá_atọ̀ka_àkóónú++) if (Alásopọ̀_adarí_aláìrídìmú.받기(입력틀) == 0) break;
    }
    static int wá_atọ̀ka_àkóónú(int èkù_iye) { return èkù_iye >= 3 && èkù_iye < 7 && 접속번호들[èkù_iye - 3] != 0 ? èkù_iye - 3 : -1; }
    static int Ṣi(int 접속번호) {
        if (Alásopọ̀_adarí_aláìrídìmú.입출력기준주소 == 0) return -19;
        if (접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 != 0) for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 4; wá_atọ̀ka_àkóónú++) if (접속번호들[wá_atọ̀ka_àkóónú] == 접속번호) return -98;
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 4; wá_atọ̀ka_àkóónú++) if (접속번호들[wá_atọ̀ka_àkóónú] == 0) {
            if (접속번호 == 0) {
                접속번호 = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int 앞 = 0; 앞 < 4; 앞++) if (접속번호들[앞] == 접속번호) 겹침 = true;
                    if (겹침) 접속번호++;
                }
            }
            접속번호들[wá_atọ̀ka_àkóónú] = 접속번호; 받은길이[wá_atọ̀ka_àkóónú] = -1;
            return wá_atọ̀ka_àkóónú + 3;
        }
        return -24;
    }
    static int Ti(int èkù_iye) {
        int ààyè_ìfàyọkàsí_ìgbéwọlé = wá_atọ̀ka_àkóónú(èkù_iye);
        if (ààyè_ìfàyọkàsí_ìgbéwọlé < 0) return -9;
        접속번호들[ààyè_ìfàyọkàsí_ìgbéwọlé] = 0; 받은길이[ààyè_ìfàyọkàsí_ìgbéwọlé] = -1;
        return 0;
    }
    static int ọ̀gbà_àdírẹ́ẹ̀sì(int èkù_iye) { int ààyè_ìfàyọkàsí_ìgbéwọlé = wá_atọ̀ka_àkóónú(èkù_iye); return ààyè_ìfàyọkàsí_ìgbéwọlé < 0 ? -9 : 받은주소[ààyè_ìfàyọkàsí_ìgbéwọlé]; }
    static int 상대접속번호(int èkù_iye) { int ààyè_ìfàyọkàsí_ìgbéwọlé = wá_atọ̀ka_àkóónú(èkù_iye); return ààyè_ìfàyọkàsí_ìgbéwọlé < 0 ? -9 : 받은접속번호[ààyè_ìfàyọkàsí_ìgbéwọlé]; }

    static void 바깥머리(int 종류, boolean àtagbà_iye) {
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 6; wá_atọ̀ka_àkóónú++) {
            출력틀[wá_atọ̀ka_àkóónú] = àtagbà_iye ? 255 : 찾은장치[wá_atọ̀ka_àkóónú];
            출력틀[6 + wá_atọ̀ka_àkóónú] = Alásopọ̀_adarí_aláìrídìmú.ohun_èlò_àdírẹ́ẹ̀sì[wá_atọ̀ka_àkóónú];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void 주소요청(int èbúté_iye) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 6; wá_atọ̀ka_àkóónú++) {
            출력틀[22 + wá_atọ̀ka_àkóónú] = Alásopọ̀_adarí_aláìrídìmú.ohun_èlò_àdírẹ́ẹ̀sì[wá_atọ̀ka_àkóónú]; 출력틀[32 + wá_atọ̀ka_àkóónú] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, èbúté_iye);
        Alásopọ̀_adarí_aláìrídìmú.í_meèlì(출력틀, 42);
    }
    static void Ìlànà_àdírẹ́ẹ̀sì(int gígùn_iye) {
        if (gígùn_iye < 42 || nọ́ńbà_odindi_16(입력틀, 14) != 1 || nọ́ńbà_odindi_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || nọ́ńbà_odindi_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = nọ́ńbà_odindi_16(입력틀, 20), ọ̀gbà_iye = nọ́ńbà_odindi_32(입력틀, 28);
        if (종류 == 2 && ọ̀gbà_iye == 찾을주소) {
            for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 6; wá_atọ̀ka_àkóónú++) {
                if (입력틀[6 + wá_atọ̀ka_àkóónú] != 입력틀[22 + wá_atọ̀ka_àkóónú] || 입력틀[32 + wá_atọ̀ka_àkóónú] != Alásopọ̀_adarí_aláìrídìmú.ohun_èlò_àdírẹ́ẹ̀sì[wá_atọ̀ka_àkóónú]) return;
            }
            for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 6; wá_atọ̀ka_àkóónú++) 찾은장치[wá_atọ̀ka_àkóónú] = 입력틀[22 + wá_atọ̀ka_àkóónú];
            찾은주소 = ọ̀gbà_iye;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 6; wá_atọ̀ka_àkóónú++) {
                출력틀[wá_atọ̀ka_àkóónú] = 입력틀[22 + wá_atọ̀ka_àkóónú]; 출력틀[32 + wá_atọ̀ka_àkóónú] = 입력틀[22 + wá_atọ̀ka_àkóónú];
                출력틀[22 + wá_atọ̀ka_àkóónú] = Alásopọ̀_adarí_aláìrídìmú.ohun_èlò_àdírẹ́ẹ̀sì[wá_atọ̀ka_àkóónú];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, ọ̀gbà_iye);
            Alásopọ̀_adarí_aláìrídìmú.í_meèlì(출력틀, 42);
        }
    }

    static void Ìlànà_férèmù(int gígùn_iye) {
        if (gígùn_iye < 14 || gígùn_iye > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, àtagbà_iye = true;
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 6; wá_atọ̀ka_àkóónú++) {
            if (입력틀[wá_atọ̀ka_àkóónú] != Alásopọ̀_adarí_aláìrídìmú.ohun_èlò_àdírẹ́ẹ̀sì[wá_atọ̀ka_àkóónú]) 자기 = false;
            if (입력틀[wá_atọ̀ka_àkóónú] != 255) àtagbà_iye = false;
        }
        if (!자기 && !àtagbà_iye) return;
        if (nọ́ńbà_odindi_16(입력틀, 12) == 0x0806) { Ìlànà_àdírẹ́ẹ̀sì(gígùn_iye); return; }
        if (nọ́ńbà_odindi_16(입력틀, 12) != 0x0800) return;
        if (gígùn_iye < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int àkọlé_gígùn = (입력틀[14] & 15) * 4, 전체길이 = nọ́ńbà_odindi_16(입력틀, 16);
        if (àkọlé_gígùn < 20 || àkọlé_gígùn > 60 || 전체길이 < àkọlé_gígùn + 8 || 전체길이 > gígùn_iye - 14
            || (nọ́ńbà_odindi_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || nọ́ńbà_odindi_32(입력틀, 30) != 내주소 || 합(입력틀, 14, àkọlé_gígùn, 0) != 65535) { 폐기수++; return; }
        int Rọ́ọ̀nù = 14 + àkọlé_gígùn, détà_gígùn = nọ́ńbà_odindi_16(입력틀, Rọ́ọ̀nù + 4);
        if (détà_gígùn < 8 || détà_gígùn != 전체길이 - àkọlé_gígùn || détà_gígùn > 1032) { 폐기수++; return; }
        int 출발 = nọ́ńbà_odindi_32(입력틀, 26);
        if (nọ́ńbà_odindi_16(입력틀, Rọ́ọ̀nù + 6) != 0 && 합(입력틀, Rọ́ọ̀nù, détà_gígùn, 가상머리합(출발, 내주소, détà_gígùn)) != 65535) {
            폐기수++; return;
        }
        int èbúté_iye = nọ́ńbà_odindi_16(입력틀, Rọ́ọ̀nù + 2);
        for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < 4; ààyè_ìfàyọkàsí_ìgbéwọlé++) if (접속번호들[ààyè_ìfàyọkàsí_ìgbéwọlé] != 0 && 접속번호들[ààyè_ìfàyọkàsí_ìgbéwọlé] == èbúté_iye) {
            if (받은길이[ààyè_ìfàyọkàsí_ìgbéwọlé] >= 0) { 폐기수++; return; }
            받은길이[ààyè_ìfàyọkàsí_ìgbéwọlé] = détà_gígùn - 8; 받은주소[ààyè_ìfàyọkàsí_ìgbéwọlé] = 출발; 받은접속번호[ààyè_ìfàyọkàsí_ìgbéwọlé] = nọ́ńbà_odindi_16(입력틀, Rọ́ọ̀nù);
            for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < détà_gígùn - 8; wá_atọ̀ka_àkóónú++) 받은자료[ààyè_ìfàyọkàsí_ìgbéwọlé * 1024 + wá_atọ̀ka_àkóónú] = 입력틀[Rọ́ọ̀nù + 8 + wá_atọ̀ka_àkóónú];
            return;
        }
    }

    static void ridájú() {
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 16; wá_atọ̀ka_àkóónú++) {
            int gígùn_iye = Alásopọ̀_adarí_aláìrídìmú.받기(입력틀);
            if (gígùn_iye == 0) return;
            Ìlànà_férèmù(gígùn_iye);
        }
    }
    static int wá_àdírẹ́ẹ̀sì(int àdírẹ́ẹ̀sì) {
        if (àdírẹ́ẹ̀sì == 0 || àdírẹ́ẹ̀sì == -1 || (àdírẹ́ẹ̀sì >>> 28) >= 14 || (àdírẹ́ẹ̀sì >>> 24) == 127 || àdírẹ́ẹ̀sì == 내주소) return -101;
        int 다음 = (àdírẹ́ẹ̀sì & Alásopọ̀_asẹ́_iye) == (내주소 & Alásopọ̀_asẹ́_iye) ? àdírẹ́ẹ̀sì : ẹnu_odi_iye;
        if (다음 == 찾은주소) return 0;
        찾을주소 = 다음;
        int Rọ́ọ̀nù = ohun_èlò_iye.밀리초(), 다음요청 = Rọ́ọ̀nù;
        while (ohun_èlò_iye.밀리초() - Rọ́ọ̀nù < 1000) {
            if (ohun_èlò_iye.밀리초() - 다음요청 >= 0) { 주소요청(다음); 다음요청 += 300; }
            ridájú();
            if (찾은주소 == 다음) return 0;
            ohun_èlò_iye.잠시양보();
        }
        return -110;
    }
    static int í_meèlì(int èkù_iye, int àdírẹ́ẹ̀sì, int 접속번호, int[] détà, int gígùn_iye) {
        int ààyè_ìfàyọkàsí_ìgbéwọlé = wá_atọ̀ka_àkóónú(èkù_iye);
        if (ààyè_ìfàyọkàsí_ìgbéwọlé < 0) return -9;
        if (Alásopọ̀_adarí_aláìrídìmú.입출력기준주소 == 0) return -19;
        if (접속번호 < 1 || 접속번호 > 65535 || gígùn_iye < 0 || gígùn_iye > 1024) return -22;
        int 결과 = wá_àdírẹ́ẹ̀sì(àdírẹ́ẹ̀sì);
        if (결과 < 0) return 결과;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + gígùn_iye);
        넣기16(출력틀, 18, Àfidámọ̀_iye++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, àdírẹ́ẹ̀sì);
        넣기16(출력틀, 24, ~합(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[ààyè_ìfàyọkàsí_ìgbéwọlé]); 넣기16(출력틀, 36, 접속번호);
        넣기16(출력틀, 38, gígùn_iye + 8); 넣기16(출력틀, 40, 0);
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < gígùn_iye; wá_atọ̀ka_àkóónú++) 출력틀[42 + wá_atọ̀ka_àkóónú] = détà[wá_atọ̀ka_àkóónú] & 255;
        int 검사합 = (~합(출력틀, 34, gígùn_iye + 8, 가상머리합(내주소, àdírẹ́ẹ̀sì, gígùn_iye + 8))) & 65535;
        넣기16(출력틀, 40, 검사합 == 0 ? 65535 : 검사합);
        결과 = Alásopọ̀_adarí_aláìrídìmú.í_meèlì(출력틀, gígùn_iye + 42);
        return 결과 < 0 ? 결과 : gígùn_iye;
    }
    static int 받기(int èkù_iye, int[] détà, int 용량, int 제한) {
        int ààyè_ìfàyọkàsí_ìgbéwọlé = wá_atọ̀ka_àkóónú(èkù_iye);
        if (ààyè_ìfàyọkàsí_ìgbéwọlé < 0) return -9;
        int Rọ́ọ̀nù = ohun_èlò_iye.밀리초();
        while (true) {
            ridájú();
            int gígùn_iye = 받은길이[ààyè_ìfàyọkàsí_ìgbéwọlé];
            if (gígùn_iye >= 0) {
                받은길이[ààyè_ìfàyọkàsí_ìgbéwọlé] = -1;
                if (gígùn_iye > 용량) return -90;
                for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < gígùn_iye; wá_atọ̀ka_àkóónú++) détà[wá_atọ̀ka_àkóónú] = 받은자료[ààyè_ìfàyọkàsí_ìgbéwọlé * 1024 + wá_atọ̀ka_àkóónú];
                return gígùn_iye;
            }
            if (제한 == 0) return -11;
            if (ohun_èlò_iye.밀리초() - Rọ́ọ̀nù >= 제한) return -110;
            ohun_èlò_iye.잠시양보();
        }
    }
    static void ipò_iye() {
        문자단말.Kọ(Alásopọ̀_adarí_aláìrídìmú.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        문자단말.Kọ("TX: "); 문자단말.수쓰기(Alásopọ̀_adarí_aláìrídìmú.송신수);
        문자단말.Kọ(" RX: "); 문자단말.수쓰기(Alásopọ̀_adarí_aláìrídìmú.수신수);
        문자단말.Kọ(" DROP: "); 문자단말.수쓰기(폐기수);
        문자단말.Kọ("\n");
    }
}
