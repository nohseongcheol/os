// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ñiiɓ_njaru IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class 통신망 {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int 망경계 = 0xffffff00; /* ip.conf:NETMASK */
    static final int 관문 = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], 받은길이 = new int[4], 받은주소 = new int[4], 받은접속번호 = new int[4];
    static int[] 받은자료 = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, 식별자 = 0, 폐기수 = 0;

    static int 수16(int[] taƴtinnde_joopirdu, int 위치) { return (taƴtinnde_joopirdu[위치] << 8) | taƴtinnde_joopirdu[위치 + 1]; }
    static int 수32(int[] taƴtinnde_joopirdu, int 위치) { return (수16(taƴtinnde_joopirdu, 위치) << 16) | 수16(taƴtinnde_joopirdu, 위치 + 2); }
    static void 넣기16(int[] taƴtinnde_joopirdu, int 위치, int njaru) { taƴtinnde_joopirdu[위치] = (njaru >>> 8) & 255; taƴtinnde_joopirdu[위치 + 1] = njaru & 255; }
    static void 넣기32(int[] taƴtinnde_joopirdu, int 위치, int njaru) { 넣기16(taƴtinnde_joopirdu, 위치, njaru >>> 16); 넣기16(taƴtinnde_joopirdu, 위치 + 2, njaru); }
    static int 합(int[] taƴtinnde_joopirdu, int huutoraade, int njuuteendi_njaru, int njaru) {
        for (int joopirdu = 0; joopirdu < njuuteendi_njaru; joopirdu += 2)
            njaru += (taƴtinnde_joopirdu[huutoraade + joopirdu] << 8) | (joopirdu + 1 < njuuteendi_njaru ? taƴtinnde_joopirdu[huutoraade + joopirdu + 1] : 0);
        while ((njaru >>> 16) != 0) njaru = (njaru & 65535) + (njaru >>> 16);
        return njaru;
    }
    static int 가상머리합(int 출발, int 도착, int njuuteendi_njaru) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + njuuteendi_njaru;
    }

    static void 과정정리() {
        for (int joopirdu = 0; joopirdu < 4; joopirdu++) {
            접속번호들[joopirdu] = 0; 받은길이[joopirdu] = -1; 받은주소[joopirdu] = 0; 받은접속번호[joopirdu] = 0;
        }
        for (int joopirdu = 0; joopirdu < 64; joopirdu++) if (laylaytol_pilot.받기(입력틀) == 0) break;
    }
    static int joopirdu(int jaggoode_njaru) { return jaggoode_njaru >= 3 && jaggoode_njaru < 7 && 접속번호들[jaggoode_njaru - 3] != 0 ? jaggoode_njaru - 3 : -1; }
    static int udditde(int 접속번호) {
        if (laylaytol_pilot.입출력기준주소 == 0) return -19;
        if (접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 != 0) for (int joopirdu = 0; joopirdu < 4; joopirdu++) if (접속번호들[joopirdu] == 접속번호) return -98;
        for (int joopirdu = 0; joopirdu < 4; joopirdu++) if (접속번호들[joopirdu] == 0) {
            if (접속번호 == 0) {
                접속번호 = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int 앞 = 0; 앞 < 4; 앞++) if (접속번호들[앞] == 접속번호) 겹침 = true;
                    if (겹침) 접속번호++;
                }
            }
            접속번호들[joopirdu] = 접속번호; 받은길이[joopirdu] = -1;
            return joopirdu + 3;
        }
        return -24;
    }
    static int uddude(int jaggoode_njaru) {
        int 칸 = joopirdu(jaggoode_njaru);
        if (칸 < 0) return -9;
        접속번호들[칸] = 0; 받은길이[칸] = -1;
        return 0;
    }
    static int giƴiraaɗo_ñiiɓirde(int jaggoode_njaru) { int 칸 = joopirdu(jaggoode_njaru); return 칸 < 0 ? -9 : 받은주소[칸]; }
    static int 상대접속번호(int jaggoode_njaru) { int 칸 = joopirdu(jaggoode_njaru); return 칸 < 0 ? -9 : 받은접속번호[칸]; }

    static void 바깥머리(int 종류, boolean 방송) {
        for (int joopirdu = 0; joopirdu < 6; joopirdu++) {
            출력틀[joopirdu] = 방송 ? 255 : 찾은장치[joopirdu];
            출력틀[6 + joopirdu] = laylaytol_pilot.kaɓirgal_ñiiɓirde[joopirdu];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void 주소요청(int tiindaare_njaru) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int joopirdu = 0; joopirdu < 6; joopirdu++) {
            출력틀[22 + joopirdu] = laylaytol_pilot.kaɓirgal_ñiiɓirde[joopirdu]; 출력틀[32 + joopirdu] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, tiindaare_njaru);
        laylaytol_pilot.neldude(출력틀, 42);
    }
    static void Yuɓɓo_golle_ñiiɓirde(int njuuteendi_njaru) {
        if (njuuteendi_njaru < 42 || 수16(입력틀, 14) != 1 || 수16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || 수32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = 수16(입력틀, 20), giƴiraaɗo_njaru = 수32(입력틀, 28);
        if (종류 == 2 && giƴiraaɗo_njaru == 찾을주소) {
            for (int joopirdu = 0; joopirdu < 6; joopirdu++) {
                if (입력틀[6 + joopirdu] != 입력틀[22 + joopirdu] || 입력틀[32 + joopirdu] != laylaytol_pilot.kaɓirgal_ñiiɓirde[joopirdu]) return;
            }
            for (int joopirdu = 0; joopirdu < 6; joopirdu++) 찾은장치[joopirdu] = 입력틀[22 + joopirdu];
            찾은주소 = giƴiraaɗo_njaru;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int joopirdu = 0; joopirdu < 6; joopirdu++) {
                출력틀[joopirdu] = 입력틀[22 + joopirdu]; 출력틀[32 + joopirdu] = 입력틀[22 + joopirdu];
                출력틀[22 + joopirdu] = laylaytol_pilot.kaɓirgal_ñiiɓirde[joopirdu];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, giƴiraaɗo_njaru);
            laylaytol_pilot.neldude(출력틀, 42);
        }
    }

    static void Yuɓɓo_golle_taƴtinnde(int njuuteendi_njaru) {
        if (njuuteendi_njaru < 14 || njuuteendi_njaru > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, 방송 = true;
        for (int joopirdu = 0; joopirdu < 6; joopirdu++) {
            if (입력틀[joopirdu] != laylaytol_pilot.kaɓirgal_ñiiɓirde[joopirdu]) 자기 = false;
            if (입력틀[joopirdu] != 255) 방송 = false;
        }
        if (!자기 && !방송) return;
        if (수16(입력틀, 12) == 0x0806) { Yuɓɓo_golle_ñiiɓirde(njuuteendi_njaru); return; }
        if (수16(입력틀, 12) != 0x0800) return;
        if (njuuteendi_njaru < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int meetalol_hello_njuuteendi = (입력틀[14] & 15) * 4, 전체길이 = 수16(입력틀, 16);
        if (meetalol_hello_njuuteendi < 20 || meetalol_hello_njuuteendi > 60 || 전체길이 < meetalol_hello_njuuteendi + 8 || 전체길이 > njuuteendi_njaru - 14
            || (수16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || 수32(입력틀, 30) != 내주소 || 합(입력틀, 14, meetalol_hello_njuuteendi, 0) != 65535) { 폐기수++; return; }
        int huutoraade = 14 + meetalol_hello_njuuteendi, keɓe_njuuteendi = 수16(입력틀, huutoraade + 4);
        if (keɓe_njuuteendi < 8 || keɓe_njuuteendi != 전체길이 - meetalol_hello_njuuteendi || keɓe_njuuteendi > 1032) { 폐기수++; return; }
        int 출발 = 수32(입력틀, 26);
        if (수16(입력틀, huutoraade + 6) != 0 && 합(입력틀, huutoraade, keɓe_njuuteendi, 가상머리합(출발, 내주소, keɓe_njuuteendi)) != 65535) {
            폐기수++; return;
        }
        int tiindaare_njaru = 수16(입력틀, huutoraade + 2);
        for (int 칸 = 0; 칸 < 4; 칸++) if (접속번호들[칸] != 0 && 접속번호들[칸] == tiindaare_njaru) {
            if (받은길이[칸] >= 0) { 폐기수++; return; }
            받은길이[칸] = keɓe_njuuteendi - 8; 받은주소[칸] = 출발; 받은접속번호[칸] = 수16(입력틀, huutoraade);
            for (int joopirdu = 0; joopirdu < keɓe_njuuteendi - 8; joopirdu++) 받은자료[칸 * 1024 + joopirdu] = 입력틀[huutoraade + 8 + joopirdu];
            return;
        }
    }

    static void ƴeewtaade() {
        for (int joopirdu = 0; joopirdu < 16; joopirdu++) {
            int njuuteendi_njaru = laylaytol_pilot.받기(입력틀);
            if (njuuteendi_njaru == 0) return;
            Yuɓɓo_golle_taƴtinnde(njuuteendi_njaru);
        }
    }
    static int yiylaade_ñiiɓirde(int ñiiɓirde) {
        if (ñiiɓirde == 0 || ñiiɓirde == -1 || (ñiiɓirde >>> 28) >= 14 || (ñiiɓirde >>> 24) == 127 || ñiiɓirde == 내주소) return -101;
        int 다음 = (ñiiɓirde & 망경계) == (내주소 & 망경계) ? ñiiɓirde : 관문;
        if (다음 == 찾은주소) return 0;
        찾을주소 = 다음;
        int huutoraade = kaɓirgal_njaru.밀리초(), 다음요청 = huutoraade;
        while (kaɓirgal_njaru.밀리초() - huutoraade < 1000) {
            if (kaɓirgal_njaru.밀리초() - 다음요청 >= 0) { 주소요청(다음); 다음요청 += 300; }
            ƴeewtaade();
            if (찾은주소 == 다음) return 0;
            kaɓirgal_njaru.잠시양보();
        }
        return -110;
    }
    static int neldude(int jaggoode_njaru, int ñiiɓirde, int 접속번호, int[] keɓe, int njuuteendi_njaru) {
        int 칸 = joopirdu(jaggoode_njaru);
        if (칸 < 0) return -9;
        if (laylaytol_pilot.입출력기준주소 == 0) return -19;
        if (접속번호 < 1 || 접속번호 > 65535 || njuuteendi_njaru < 0 || njuuteendi_njaru > 1024) return -22;
        int 결과 = yiylaade_ñiiɓirde(ñiiɓirde);
        if (결과 < 0) return 결과;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + njuuteendi_njaru);
        넣기16(출력틀, 18, 식별자++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, ñiiɓirde);
        넣기16(출력틀, 24, ~합(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[칸]); 넣기16(출력틀, 36, 접속번호);
        넣기16(출력틀, 38, njuuteendi_njaru + 8); 넣기16(출력틀, 40, 0);
        for (int joopirdu = 0; joopirdu < njuuteendi_njaru; joopirdu++) 출력틀[42 + joopirdu] = keɓe[joopirdu] & 255;
        int 검사합 = (~합(출력틀, 34, njuuteendi_njaru + 8, 가상머리합(내주소, ñiiɓirde, njuuteendi_njaru + 8))) & 65535;
        넣기16(출력틀, 40, 검사합 == 0 ? 65535 : 검사합);
        결과 = laylaytol_pilot.neldude(출력틀, njuuteendi_njaru + 42);
        return 결과 < 0 ? 결과 : njuuteendi_njaru;
    }
    static int 받기(int jaggoode_njaru, int[] keɓe, int 용량, int 제한) {
        int 칸 = joopirdu(jaggoode_njaru);
        if (칸 < 0) return -9;
        int huutoraade = kaɓirgal_njaru.밀리초();
        while (true) {
            ƴeewtaade();
            int njuuteendi_njaru = 받은길이[칸];
            if (njuuteendi_njaru >= 0) {
                받은길이[칸] = -1;
                if (njuuteendi_njaru > 용량) return -90;
                for (int joopirdu = 0; joopirdu < njuuteendi_njaru; joopirdu++) keɓe[joopirdu] = 받은자료[칸 * 1024 + joopirdu];
                return njuuteendi_njaru;
            }
            if (제한 == 0) return -11;
            if (kaɓirgal_njaru.밀리초() - huutoraade >= 제한) return -110;
            kaɓirgal_njaru.잠시양보();
        }
    }
    static void ngonka_njaru() {
        문자단말.winndude(laylaytol_pilot.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        문자단말.winndude("TX: "); 문자단말.수쓰기(laylaytol_pilot.송신수);
        문자단말.winndude(" RX: "); 문자단말.수쓰기(laylaytol_pilot.수신수);
        문자단말.winndude(" DROP: "); 문자단말.수쓰기(폐기수);
        문자단말.winndude("\n");
    }
}
