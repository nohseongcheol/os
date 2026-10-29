// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** statičen_VALUE IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class mreža_Sklad {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int mreža_maska = 0xffffff00; /* ip.conf:NETMASK */
    static final int prehod_VALUE = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], 받은길이 = new int[4], RECEIVED_naslov = new int[4], RECEIVED_številka_vrat = new int[4];
    static int[] RECEIVED_podatki = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, identifikator_VALUE = 0, 폐기수 = 0;

    static int celo_število_16(int[] okvir_INDEX, int Položaj) { return (okvir_INDEX[Položaj] << 8) | okvir_INDEX[Položaj + 1]; }
    static int celo_število_32(int[] okvir_INDEX, int Položaj) { return (celo_število_16(okvir_INDEX, Položaj) << 16) | celo_število_16(okvir_INDEX, Položaj + 2); }
    static void 넣기16(int[] okvir_INDEX, int Položaj, int VALUE) { okvir_INDEX[Položaj] = (VALUE >>> 8) & 255; okvir_INDEX[Položaj + 1] = VALUE & 255; }
    static void 넣기32(int[] okvir_INDEX, int Položaj, int VALUE) { 넣기16(okvir_INDEX, Položaj, VALUE >>> 16); 넣기16(okvir_INDEX, Položaj + 2, VALUE); }
    static int SUM_VALUE(int[] okvir_INDEX, int Zaženi, int 길이, int VALUE) {
        for (int INDEX = 0; INDEX < 길이; INDEX += 2)
            VALUE += (okvir_INDEX[Zaženi + INDEX] << 8) | (INDEX + 1 < 길이 ? okvir_INDEX[Zaženi + INDEX + 1] : 0);
        while ((VALUE >>> 16) != 0) VALUE = (VALUE & 65535) + (VALUE >>> 16);
        return VALUE;
    }
    static int 가상머리합(int 출발, int 도착, int 길이) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + 길이;
    }

    static void CLEAN_Proces() {
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            접속번호들[INDEX] = 0; 받은길이[INDEX] = -1; RECEIVED_naslov[INDEX] = 0; RECEIVED_številka_vrat[INDEX] = 0;
        }
        for (int INDEX = 0; INDEX < 64; INDEX++) if (mreža_gonilnik.sprejeti_sprejemati_prejeti_prejemati(입력틀) == 0) break;
    }
    static int INDEX(int ročica_VALUE) { return ročica_VALUE >= 3 && ročica_VALUE < 7 && 접속번호들[ročica_VALUE - 3] != 0 ? ročica_VALUE - 3 : -1; }
    static int Odpri(int številka_vrat) {
        if (mreža_gonilnik.입출력기준주소 == 0) return -19;
        if (številka_vrat < 0 || številka_vrat > 65535) return -22;
        if (številka_vrat != 0) for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == številka_vrat) return -98;
        for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == 0) {
            if (številka_vrat == 0) {
                številka_vrat = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int sprednja_VALUE = 0; sprednja_VALUE < 4; sprednja_VALUE++) if (접속번호들[sprednja_VALUE] == številka_vrat) 겹침 = true;
                    if (겹침) številka_vrat++;
                }
            }
            접속번호들[INDEX] = številka_vrat; 받은길이[INDEX] = -1;
            return INDEX + 3;
        }
        return -24;
    }
    static int Zapri(int ročica_VALUE) {
        int 칸 = INDEX(ročica_VALUE);
        if (칸 < 0) return -9;
        접속번호들[칸] = 0; 받은길이[칸] = -1;
        return 0;
    }
    static int enakovreden_naslov(int ročica_VALUE) { int 칸 = INDEX(ročica_VALUE); return 칸 < 0 ? -9 : RECEIVED_naslov[칸]; }
    static int enakovreden_številka_vrat(int ročica_VALUE) { int 칸 = INDEX(ročica_VALUE); return 칸 < 0 ? -9 : RECEIVED_številka_vrat[칸]; }

    static void 바깥머리(int 종류, boolean oddaja_VALUE) {
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[INDEX] = oddaja_VALUE ? 255 : 찾은장치[INDEX];
            출력틀[6 + INDEX] = mreža_gonilnik.naprava_naslov[INDEX];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void zahteva_naslov(int cilj_VALUE) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[22 + INDEX] = mreža_gonilnik.naprava_naslov[INDEX]; 출력틀[32 + INDEX] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, cilj_VALUE);
        mreža_gonilnik.poslati(출력틀, 42);
    }
    static void Proces_naslov(int 길이) {
        if (길이 < 42 || celo_število_16(입력틀, 14) != 1 || celo_število_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || celo_število_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = celo_število_16(입력틀, 20), enakovreden_VALUE = celo_število_32(입력틀, 28);
        if (종류 == 2 && enakovreden_VALUE == 찾을주소) {
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                if (입력틀[6 + INDEX] != 입력틀[22 + INDEX] || 입력틀[32 + INDEX] != mreža_gonilnik.naprava_naslov[INDEX]) return;
            }
            for (int INDEX = 0; INDEX < 6; INDEX++) 찾은장치[INDEX] = 입력틀[22 + INDEX];
            찾은주소 = enakovreden_VALUE;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                출력틀[INDEX] = 입력틀[22 + INDEX]; 출력틀[32 + INDEX] = 입력틀[22 + INDEX];
                출력틀[22 + INDEX] = mreža_gonilnik.naprava_naslov[INDEX];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, enakovreden_VALUE);
            mreža_gonilnik.poslati(출력틀, 42);
        }
    }

    static void Proces_okvir(int 길이) {
        if (길이 < 14 || 길이 > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, oddaja_VALUE = true;
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            if (입력틀[INDEX] != mreža_gonilnik.naprava_naslov[INDEX]) 자기 = false;
            if (입력틀[INDEX] != 255) oddaja_VALUE = false;
        }
        if (!자기 && !oddaja_VALUE) return;
        if (celo_število_16(입력틀, 12) == 0x0806) { Proces_naslov(길이); return; }
        if (celo_število_16(입력틀, 12) != 0x0800) return;
        if (길이 < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int 머리길이 = (입력틀[14] & 15) * 4, 전체길이 = celo_število_16(입력틀, 16);
        if (머리길이 < 20 || 머리길이 > 60 || 전체길이 < 머리길이 + 8 || 전체길이 > 길이 - 14
            || (celo_število_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || celo_število_32(입력틀, 30) != 내주소 || SUM_VALUE(입력틀, 14, 머리길이, 0) != 65535) { 폐기수++; return; }
        int Zaženi = 14 + 머리길이, 자료길이 = celo_število_16(입력틀, Zaženi + 4);
        if (자료길이 < 8 || 자료길이 != 전체길이 - 머리길이 || 자료길이 > 1032) { 폐기수++; return; }
        int 출발 = celo_število_32(입력틀, 26);
        if (celo_število_16(입력틀, Zaženi + 6) != 0 && SUM_VALUE(입력틀, Zaženi, 자료길이, 가상머리합(출발, 내주소, 자료길이)) != 65535) {
            폐기수++; return;
        }
        int cilj_VALUE = celo_število_16(입력틀, Zaženi + 2);
        for (int 칸 = 0; 칸 < 4; 칸++) if (접속번호들[칸] != 0 && 접속번호들[칸] == cilj_VALUE) {
            if (받은길이[칸] >= 0) { 폐기수++; return; }
            받은길이[칸] = 자료길이 - 8; RECEIVED_naslov[칸] = 출발; RECEIVED_številka_vrat[칸] = celo_število_16(입력틀, Zaženi);
            for (int INDEX = 0; INDEX < 자료길이 - 8; INDEX++) RECEIVED_podatki[칸 * 1024 + INDEX] = 입력틀[Zaženi + 8 + INDEX];
            return;
        }
    }

    static void 확인() {
        for (int INDEX = 0; INDEX < 16; INDEX++) {
            int 길이 = mreža_gonilnik.sprejeti_sprejemati_prejeti_prejemati(입력틀);
            if (길이 == 0) return;
            Proces_okvir(길이);
        }
    }
    static int FIND_naslov(int naslov) {
        if (naslov == 0 || naslov == -1 || (naslov >>> 28) >= 14 || (naslov >>> 24) == 127 || naslov == 내주소) return -101;
        int Naprej_element = (naslov & mreža_maska) == (내주소 & mreža_maska) ? naslov : prehod_VALUE;
        if (Naprej_element == 찾은주소) return 0;
        찾을주소 = Naprej_element;
        int Zaženi = naprava_VALUE.밀리초(), Naprej_zahteva = Zaženi;
        while (naprava_VALUE.밀리초() - Zaženi < 1000) {
            if (naprava_VALUE.밀리초() - Naprej_zahteva >= 0) { zahteva_naslov(Naprej_element); Naprej_zahteva += 300; }
            확인();
            if (찾은주소 == Naprej_element) return 0;
            naprava_VALUE.잠시양보();
        }
        return -110;
    }
    static int poslati(int ročica_VALUE, int naslov, int številka_vrat, int[] podatki, int 길이) {
        int 칸 = INDEX(ročica_VALUE);
        if (칸 < 0) return -9;
        if (mreža_gonilnik.입출력기준주소 == 0) return -19;
        if (številka_vrat < 1 || številka_vrat > 65535 || 길이 < 0 || 길이 > 1024) return -22;
        int REZULTAT = FIND_naslov(naslov);
        if (REZULTAT < 0) return REZULTAT;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + 길이);
        넣기16(출력틀, 18, identifikator_VALUE++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, naslov);
        넣기16(출력틀, 24, ~SUM_VALUE(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[칸]); 넣기16(출력틀, 36, številka_vrat);
        넣기16(출력틀, 38, 길이 + 8); 넣기16(출력틀, 40, 0);
        for (int INDEX = 0; INDEX < 길이; INDEX++) 출력틀[42 + INDEX] = podatki[INDEX] & 255;
        int kontrolna_vsota = (~SUM_VALUE(출력틀, 34, 길이 + 8, 가상머리합(내주소, naslov, 길이 + 8))) & 65535;
        넣기16(출력틀, 40, kontrolna_vsota == 0 ? 65535 : kontrolna_vsota);
        REZULTAT = mreža_gonilnik.poslati(출력틀, 길이 + 42);
        return REZULTAT < 0 ? REZULTAT : 길이;
    }
    static int sprejeti_sprejemati_prejeti_prejemati(int ročica_VALUE, int[] podatki, int zmogljivost_VALUE, int 제한) {
        int 칸 = INDEX(ročica_VALUE);
        if (칸 < 0) return -9;
        int Zaženi = naprava_VALUE.밀리초();
        while (true) {
            확인();
            int 길이 = 받은길이[칸];
            if (길이 >= 0) {
                받은길이[칸] = -1;
                if (길이 > zmogljivost_VALUE) return -90;
                for (int INDEX = 0; INDEX < 길이; INDEX++) podatki[INDEX] = RECEIVED_podatki[칸 * 1024 + INDEX];
                return 길이;
            }
            if (제한 == 0) return -11;
            if (naprava_VALUE.밀리초() - Zaženi >= 제한) return -110;
            naprava_VALUE.잠시양보();
        }
    }
    static void stanje_VALUE() {
        SMS_Terminal.Pisanje(mreža_gonilnik.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Terminal.Pisanje("TX: "); SMS_Terminal.수쓰기(mreža_gonilnik.송신수);
        SMS_Terminal.Pisanje(" RX: "); SMS_Terminal.수쓰기(mreža_gonilnik.sprejeti_sprejemati_prejeti_prejemati_COUNT);
        SMS_Terminal.Pisanje(" DROP: "); SMS_Terminal.수쓰기(폐기수);
        SMS_Terminal.Pisanje("\n");
    }
}
