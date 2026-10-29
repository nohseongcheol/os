// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 정적 IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class võrk_Virn {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int võrk_mask = 0xffffff00; /* ip.conf:NETMASK */
    static final int lüüs_VALUE = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], toodang_raam = new int[1536];
    static int[] 접속번호들 = new int[4], 받은길이 = new int[4], RECEIVED_ADDRESS = new int[4], RECEIVED_pordinumber = new int[4];
    static int[] RECEIVED_andmed = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, identifikaator_VALUE = 0, 폐기수 = 0;

    static int täisarv_16(int[] raam_INDEX, int Asukoht) { return (raam_INDEX[Asukoht] << 8) | raam_INDEX[Asukoht + 1]; }
    static int täisarv_32(int[] raam_INDEX, int Asukoht) { return (täisarv_16(raam_INDEX, Asukoht) << 16) | täisarv_16(raam_INDEX, Asukoht + 2); }
    static void 넣기16(int[] raam_INDEX, int Asukoht, int VALUE) { raam_INDEX[Asukoht] = (VALUE >>> 8) & 255; raam_INDEX[Asukoht + 1] = VALUE & 255; }
    static void 넣기32(int[] raam_INDEX, int Asukoht, int VALUE) { 넣기16(raam_INDEX, Asukoht, VALUE >>> 16); 넣기16(raam_INDEX, Asukoht + 2, VALUE); }
    static int SUM_VALUE(int[] raam_INDEX, int Käivita_2, int 길이, int VALUE) {
        for (int INDEX = 0; INDEX < 길이; INDEX += 2)
            VALUE += (raam_INDEX[Käivita_2 + INDEX] << 8) | (INDEX + 1 < 길이 ? raam_INDEX[Käivita_2 + INDEX + 1] : 0);
        while ((VALUE >>> 16) != 0) VALUE = (VALUE & 65535) + (VALUE >>> 16);
        return VALUE;
    }
    static int 가상머리합(int 출발, int 도착, int 길이) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + 길이;
    }

    static void CLEAN_Joonis() {
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            접속번호들[INDEX] = 0; 받은길이[INDEX] = -1; RECEIVED_ADDRESS[INDEX] = 0; RECEIVED_pordinumber[INDEX] = 0;
        }
        for (int INDEX = 0; INDEX < 64; INDEX++) if (võrk_draiver.saama(입력틀) == 0) break;
    }
    static int INDEX(int pide_VALUE) { return pide_VALUE >= 3 && pide_VALUE < 7 && 접속번호들[pide_VALUE - 3] != 0 ? pide_VALUE - 3 : -1; }
    static int Ava(int pordinumber) {
        if (võrk_draiver.입출력기준주소 == 0) return -19;
        if (pordinumber < 0 || pordinumber > 65535) return -22;
        if (pordinumber != 0) for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == pordinumber) return -98;
        for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == 0) {
            if (pordinumber == 0) {
                pordinumber = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int esikaamera_VALUE = 0; esikaamera_VALUE < 4; esikaamera_VALUE++) if (접속번호들[esikaamera_VALUE] == pordinumber) 겹침 = true;
                    if (겹침) pordinumber++;
                }
            }
            접속번호들[INDEX] = pordinumber; 받은길이[INDEX] = -1;
            return INDEX + 3;
        }
        return -24;
    }
    static int Suletud(int pide_VALUE) {
        int 칸 = INDEX(pide_VALUE);
        if (칸 < 0) return -9;
        접속번호들[칸] = 0; 받은길이[칸] = -1;
        return 0;
    }
    static int partner_ADDRESS(int pide_VALUE) { int 칸 = INDEX(pide_VALUE); return 칸 < 0 ? -9 : RECEIVED_ADDRESS[칸]; }
    static int partner_pordinumber(int pide_VALUE) { int 칸 = INDEX(pide_VALUE); return 칸 < 0 ? -9 : RECEIVED_pordinumber[칸]; }

    static void 바깥머리(int 종류, boolean levi_VALUE) {
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            toodang_raam[INDEX] = levi_VALUE ? 255 : 찾은장치[INDEX];
            toodang_raam[6 + INDEX] = võrk_draiver.seade_ADDRESS[INDEX];
        }
        넣기16(toodang_raam, 12, 종류);
    }
    static void päring_ADDRESS(int sihtkoht_VALUE) {
        바깥머리(0x0806, true);
        넣기16(toodang_raam, 14, 1); 넣기16(toodang_raam, 16, 0x0800);
        toodang_raam[18] = 6; toodang_raam[19] = 4; 넣기16(toodang_raam, 20, 1);
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            toodang_raam[22 + INDEX] = võrk_draiver.seade_ADDRESS[INDEX]; toodang_raam[32 + INDEX] = 0;
        }
        넣기32(toodang_raam, 28, 내주소); 넣기32(toodang_raam, 38, sihtkoht_VALUE);
        võrk_draiver.saatma(toodang_raam, 42);
    }
    static void Joonis_ADDRESS(int 길이) {
        if (길이 < 42 || täisarv_16(입력틀, 14) != 1 || täisarv_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || täisarv_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = täisarv_16(입력틀, 20), partner_VALUE = täisarv_32(입력틀, 28);
        if (종류 == 2 && partner_VALUE == 찾을주소) {
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                if (입력틀[6 + INDEX] != 입력틀[22 + INDEX] || 입력틀[32 + INDEX] != võrk_draiver.seade_ADDRESS[INDEX]) return;
            }
            for (int INDEX = 0; INDEX < 6; INDEX++) 찾은장치[INDEX] = 입력틀[22 + INDEX];
            찾은주소 = partner_VALUE;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(toodang_raam, 14, 1); 넣기16(toodang_raam, 16, 0x0800);
            toodang_raam[18] = 6; toodang_raam[19] = 4; 넣기16(toodang_raam, 20, 2);
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                toodang_raam[INDEX] = 입력틀[22 + INDEX]; toodang_raam[32 + INDEX] = 입력틀[22 + INDEX];
                toodang_raam[22 + INDEX] = võrk_draiver.seade_ADDRESS[INDEX];
            }
            넣기32(toodang_raam, 28, 내주소); 넣기32(toodang_raam, 38, partner_VALUE);
            võrk_draiver.saatma(toodang_raam, 42);
        }
    }

    static void Joonis_raam(int 길이) {
        if (길이 < 14 || 길이 > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, levi_VALUE = true;
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            if (입력틀[INDEX] != võrk_draiver.seade_ADDRESS[INDEX]) 자기 = false;
            if (입력틀[INDEX] != 255) levi_VALUE = false;
        }
        if (!자기 && !levi_VALUE) return;
        if (täisarv_16(입력틀, 12) == 0x0806) { Joonis_ADDRESS(길이); return; }
        if (täisarv_16(입력틀, 12) != 0x0800) return;
        if (길이 < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int 머리길이 = (입력틀[14] & 15) * 4, 전체길이 = täisarv_16(입력틀, 16);
        if (머리길이 < 20 || 머리길이 > 60 || 전체길이 < 머리길이 + 8 || 전체길이 > 길이 - 14
            || (täisarv_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || täisarv_32(입력틀, 30) != 내주소 || SUM_VALUE(입력틀, 14, 머리길이, 0) != 65535) { 폐기수++; return; }
        int Käivita_2 = 14 + 머리길이, 자료길이 = täisarv_16(입력틀, Käivita_2 + 4);
        if (자료길이 < 8 || 자료길이 != 전체길이 - 머리길이 || 자료길이 > 1032) { 폐기수++; return; }
        int 출발 = täisarv_32(입력틀, 26);
        if (täisarv_16(입력틀, Käivita_2 + 6) != 0 && SUM_VALUE(입력틀, Käivita_2, 자료길이, 가상머리합(출발, 내주소, 자료길이)) != 65535) {
            폐기수++; return;
        }
        int sihtkoht_VALUE = täisarv_16(입력틀, Käivita_2 + 2);
        for (int 칸 = 0; 칸 < 4; 칸++) if (접속번호들[칸] != 0 && 접속번호들[칸] == sihtkoht_VALUE) {
            if (받은길이[칸] >= 0) { 폐기수++; return; }
            받은길이[칸] = 자료길이 - 8; RECEIVED_ADDRESS[칸] = 출발; RECEIVED_pordinumber[칸] = täisarv_16(입력틀, Käivita_2);
            for (int INDEX = 0; INDEX < 자료길이 - 8; INDEX++) RECEIVED_andmed[칸 * 1024 + INDEX] = 입력틀[Käivita_2 + 8 + INDEX];
            return;
        }
    }

    static void kinnitama() {
        for (int INDEX = 0; INDEX < 16; INDEX++) {
            int 길이 = võrk_draiver.saama(입력틀);
            if (길이 == 0) return;
            Joonis_raam(길이);
        }
    }
    static int FIND_ADDRESS(int ADDRESS) {
        if (ADDRESS == 0 || ADDRESS == -1 || (ADDRESS >>> 28) >= 14 || (ADDRESS >>> 24) == 127 || ADDRESS == 내주소) return -101;
        int Edasi_kaup = (ADDRESS & võrk_mask) == (내주소 & võrk_mask) ? ADDRESS : lüüs_VALUE;
        if (Edasi_kaup == 찾은주소) return 0;
        찾을주소 = Edasi_kaup;
        int Käivita_2 = seade_VALUE.밀리초(), Edasi_päring = Käivita_2;
        while (seade_VALUE.밀리초() - Käivita_2 < 1000) {
            if (seade_VALUE.밀리초() - Edasi_päring >= 0) { päring_ADDRESS(Edasi_kaup); Edasi_päring += 300; }
            kinnitama();
            if (찾은주소 == Edasi_kaup) return 0;
            seade_VALUE.잠시양보();
        }
        return -110;
    }
    static int saatma(int pide_VALUE, int ADDRESS, int pordinumber, int[] andmed, int 길이) {
        int 칸 = INDEX(pide_VALUE);
        if (칸 < 0) return -9;
        if (võrk_draiver.입출력기준주소 == 0) return -19;
        if (pordinumber < 1 || pordinumber > 65535 || 길이 < 0 || 길이 > 1024) return -22;
        int TULEMUS = FIND_ADDRESS(ADDRESS);
        if (TULEMUS < 0) return TULEMUS;
        바깥머리(0x0800, false);
        toodang_raam[14] = 0x45; toodang_raam[15] = 0; 넣기16(toodang_raam, 16, 28 + 길이);
        넣기16(toodang_raam, 18, identifikaator_VALUE++); 넣기16(toodang_raam, 20, 0x4000);
        toodang_raam[22] = 64; toodang_raam[23] = 17; 넣기16(toodang_raam, 24, 0);
        넣기32(toodang_raam, 26, 내주소); 넣기32(toodang_raam, 30, ADDRESS);
        넣기16(toodang_raam, 24, ~SUM_VALUE(toodang_raam, 14, 20, 0));
        넣기16(toodang_raam, 34, 접속번호들[칸]); 넣기16(toodang_raam, 36, pordinumber);
        넣기16(toodang_raam, 38, 길이 + 8); 넣기16(toodang_raam, 40, 0);
        for (int INDEX = 0; INDEX < 길이; INDEX++) toodang_raam[42 + INDEX] = andmed[INDEX] & 255;
        int kontrollsumma = (~SUM_VALUE(toodang_raam, 34, 길이 + 8, 가상머리합(내주소, ADDRESS, 길이 + 8))) & 65535;
        넣기16(toodang_raam, 40, kontrollsumma == 0 ? 65535 : kontrollsumma);
        TULEMUS = võrk_draiver.saatma(toodang_raam, 길이 + 42);
        return TULEMUS < 0 ? TULEMUS : 길이;
    }
    static int saama(int pide_VALUE, int[] andmed, int võimsus_VALUE, int 제한) {
        int 칸 = INDEX(pide_VALUE);
        if (칸 < 0) return -9;
        int Käivita_2 = seade_VALUE.밀리초();
        while (true) {
            kinnitama();
            int 길이 = 받은길이[칸];
            if (길이 >= 0) {
                받은길이[칸] = -1;
                if (길이 > võimsus_VALUE) return -90;
                for (int INDEX = 0; INDEX < 길이; INDEX++) andmed[INDEX] = RECEIVED_andmed[칸 * 1024 + INDEX];
                return 길이;
            }
            if (제한 == 0) return -11;
            if (seade_VALUE.밀리초() - Käivita_2 >= 제한) return -110;
            seade_VALUE.잠시양보();
        }
    }
    static void Olek_VALUE() {
        SMS_terminal.Kirjutamine(võrk_draiver.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_terminal.Kirjutamine("TX: "); SMS_terminal.kirjutamine_number(võrk_draiver.송신수);
        SMS_terminal.Kirjutamine(" RX: "); SMS_terminal.kirjutamine_number(võrk_draiver.saama_COUNT);
        SMS_terminal.Kirjutamine(" DROP: "); SMS_terminal.kirjutamine_number(폐기수);
        SMS_terminal.Kirjutamine("\n");
    }
}
