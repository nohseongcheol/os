// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 정적 IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class Mreža_stek {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int Mreža_maska = 0xffffff00; /* ip.conf:NETMASK */
    static final int mrežni_prolaz_VALUE = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], 받은길이 = new int[4], RECEIVED_adresa = new int[4], RECEIVED_broj_porta = new int[4];
    static int[] RECEIVED_podaci = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, identifikator_VALUE = 0, 폐기수 = 0;

    static int ceo_broj_16(int[] kadar_INDEX, int pozicija) { return (kadar_INDEX[pozicija] << 8) | kadar_INDEX[pozicija + 1]; }
    static int ceo_broj_32(int[] kadar_INDEX, int pozicija) { return (ceo_broj_16(kadar_INDEX, pozicija) << 16) | ceo_broj_16(kadar_INDEX, pozicija + 2); }
    static void 넣기16(int[] kadar_INDEX, int pozicija, int VALUE) { kadar_INDEX[pozicija] = (VALUE >>> 8) & 255; kadar_INDEX[pozicija + 1] = VALUE & 255; }
    static void 넣기32(int[] kadar_INDEX, int pozicija, int VALUE) { 넣기16(kadar_INDEX, pozicija, VALUE >>> 16); 넣기16(kadar_INDEX, pozicija + 2, VALUE); }
    static int SUM_VALUE(int[] kadar_INDEX, int koristiti, int 길이, int VALUE) {
        for (int INDEX = 0; INDEX < 길이; INDEX += 2)
            VALUE += (kadar_INDEX[koristiti + INDEX] << 8) | (INDEX + 1 < 길이 ? kadar_INDEX[koristiti + INDEX + 1] : 0);
        while ((VALUE >>> 16) != 0) VALUE = (VALUE & 65535) + (VALUE >>> 16);
        return VALUE;
    }
    static int 가상머리합(int 출발, int 도착, int 길이) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + 길이;
    }

    static void CLEAN_Proces() {
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            접속번호들[INDEX] = 0; 받은길이[INDEX] = -1; RECEIVED_adresa[INDEX] = 0; RECEIVED_broj_porta[INDEX] = 0;
        }
        for (int INDEX = 0; INDEX < 64; INDEX++) if (Mreža_Upravljački_program.primiti(입력틀) == 0) break;
    }
    static int INDEX(int pokazivač_VALUE) { return pokazivač_VALUE >= 3 && pokazivač_VALUE < 7 && 접속번호들[pokazivač_VALUE - 3] != 0 ? pokazivač_VALUE - 3 : -1; }
    static int otvoren(int broj_porta) {
        if (Mreža_Upravljački_program.입출력기준주소 == 0) return -19;
        if (broj_porta < 0 || broj_porta > 65535) return -22;
        if (broj_porta != 0) for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == broj_porta) return -98;
        for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == 0) {
            if (broj_porta == 0) {
                broj_porta = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int čeona_kamera_VALUE = 0; čeona_kamera_VALUE < 4; čeona_kamera_VALUE++) if (접속번호들[čeona_kamera_VALUE] == broj_porta) 겹침 = true;
                    if (겹침) broj_porta++;
                }
            }
            접속번호들[INDEX] = broj_porta; 받은길이[INDEX] = -1;
            return INDEX + 3;
        }
        return -24;
    }
    static int Zatvori(int pokazivač_VALUE) {
        int 칸 = INDEX(pokazivač_VALUE);
        if (칸 < 0) return -9;
        접속번호들[칸] = 0; 받은길이[칸] = -1;
        return 0;
    }
    static int ravnopravni_uređaj_adresa(int pokazivač_VALUE) { int 칸 = INDEX(pokazivač_VALUE); return 칸 < 0 ? -9 : RECEIVED_adresa[칸]; }
    static int ravnopravni_uređaj_broj_porta(int pokazivač_VALUE) { int 칸 = INDEX(pokazivač_VALUE); return 칸 < 0 ? -9 : RECEIVED_broj_porta[칸]; }

    static void 바깥머리(int 종류, boolean emitovati_VALUE) {
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[INDEX] = emitovati_VALUE ? 255 : 찾은장치[INDEX];
            출력틀[6 + INDEX] = Mreža_Upravljački_program.uređaj_adresa[INDEX];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void zahtev_adresa(int odredište_VALUE) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[22 + INDEX] = Mreža_Upravljački_program.uređaj_adresa[INDEX]; 출력틀[32 + INDEX] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, odredište_VALUE);
        Mreža_Upravljački_program.poslati(출력틀, 42);
    }
    static void Proces_adresa(int 길이) {
        if (길이 < 42 || ceo_broj_16(입력틀, 14) != 1 || ceo_broj_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || ceo_broj_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = ceo_broj_16(입력틀, 20), ravnopravni_uređaj_VALUE = ceo_broj_32(입력틀, 28);
        if (종류 == 2 && ravnopravni_uređaj_VALUE == 찾을주소) {
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                if (입력틀[6 + INDEX] != 입력틀[22 + INDEX] || 입력틀[32 + INDEX] != Mreža_Upravljački_program.uređaj_adresa[INDEX]) return;
            }
            for (int INDEX = 0; INDEX < 6; INDEX++) 찾은장치[INDEX] = 입력틀[22 + INDEX];
            찾은주소 = ravnopravni_uređaj_VALUE;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                출력틀[INDEX] = 입력틀[22 + INDEX]; 출력틀[32 + INDEX] = 입력틀[22 + INDEX];
                출력틀[22 + INDEX] = Mreža_Upravljački_program.uređaj_adresa[INDEX];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, ravnopravni_uređaj_VALUE);
            Mreža_Upravljački_program.poslati(출력틀, 42);
        }
    }

    static void Proces_kadar(int 길이) {
        if (길이 < 14 || 길이 > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, emitovati_VALUE = true;
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            if (입력틀[INDEX] != Mreža_Upravljački_program.uređaj_adresa[INDEX]) 자기 = false;
            if (입력틀[INDEX] != 255) emitovati_VALUE = false;
        }
        if (!자기 && !emitovati_VALUE) return;
        if (ceo_broj_16(입력틀, 12) == 0x0806) { Proces_adresa(길이); return; }
        if (ceo_broj_16(입력틀, 12) != 0x0800) return;
        if (길이 < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int 머리길이 = (입력틀[14] & 15) * 4, 전체길이 = ceo_broj_16(입력틀, 16);
        if (머리길이 < 20 || 머리길이 > 60 || 전체길이 < 머리길이 + 8 || 전체길이 > 길이 - 14
            || (ceo_broj_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || ceo_broj_32(입력틀, 30) != 내주소 || SUM_VALUE(입력틀, 14, 머리길이, 0) != 65535) { 폐기수++; return; }
        int koristiti = 14 + 머리길이, 자료길이 = ceo_broj_16(입력틀, koristiti + 4);
        if (자료길이 < 8 || 자료길이 != 전체길이 - 머리길이 || 자료길이 > 1032) { 폐기수++; return; }
        int 출발 = ceo_broj_32(입력틀, 26);
        if (ceo_broj_16(입력틀, koristiti + 6) != 0 && SUM_VALUE(입력틀, koristiti, 자료길이, 가상머리합(출발, 내주소, 자료길이)) != 65535) {
            폐기수++; return;
        }
        int odredište_VALUE = ceo_broj_16(입력틀, koristiti + 2);
        for (int 칸 = 0; 칸 < 4; 칸++) if (접속번호들[칸] != 0 && 접속번호들[칸] == odredište_VALUE) {
            if (받은길이[칸] >= 0) { 폐기수++; return; }
            받은길이[칸] = 자료길이 - 8; RECEIVED_adresa[칸] = 출발; RECEIVED_broj_porta[칸] = ceo_broj_16(입력틀, koristiti);
            for (int INDEX = 0; INDEX < 자료길이 - 8; INDEX++) RECEIVED_podaci[칸 * 1024 + INDEX] = 입력틀[koristiti + 8 + INDEX];
            return;
        }
    }

    static void verifikovati() {
        for (int INDEX = 0; INDEX < 16; INDEX++) {
            int 길이 = Mreža_Upravljački_program.primiti(입력틀);
            if (길이 == 0) return;
            Proces_kadar(길이);
        }
    }
    static int FIND_adresa(int adresa) {
        if (adresa == 0 || adresa == -1 || (adresa >>> 28) >= 14 || (adresa >>> 24) == 127 || adresa == 내주소) return -101;
        int Dalje_stavka = (adresa & Mreža_maska) == (내주소 & Mreža_maska) ? adresa : mrežni_prolaz_VALUE;
        if (Dalje_stavka == 찾은주소) return 0;
        찾을주소 = Dalje_stavka;
        int koristiti = uređaj_VALUE.밀리초(), Dalje_zahtev = koristiti;
        while (uređaj_VALUE.밀리초() - koristiti < 1000) {
            if (uređaj_VALUE.밀리초() - Dalje_zahtev >= 0) { zahtev_adresa(Dalje_stavka); Dalje_zahtev += 300; }
            verifikovati();
            if (찾은주소 == Dalje_stavka) return 0;
            uređaj_VALUE.잠시양보();
        }
        return -110;
    }
    static int poslati(int pokazivač_VALUE, int adresa, int broj_porta, int[] podaci, int 길이) {
        int 칸 = INDEX(pokazivač_VALUE);
        if (칸 < 0) return -9;
        if (Mreža_Upravljački_program.입출력기준주소 == 0) return -19;
        if (broj_porta < 1 || broj_porta > 65535 || 길이 < 0 || 길이 > 1024) return -22;
        int KR = FIND_adresa(adresa);
        if (KR < 0) return KR;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + 길이);
        넣기16(출력틀, 18, identifikator_VALUE++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, adresa);
        넣기16(출력틀, 24, ~SUM_VALUE(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[칸]); 넣기16(출력틀, 36, broj_porta);
        넣기16(출력틀, 38, 길이 + 8); 넣기16(출력틀, 40, 0);
        for (int INDEX = 0; INDEX < 길이; INDEX++) 출력틀[42 + INDEX] = podaci[INDEX] & 255;
        int kontrolni_zbir = (~SUM_VALUE(출력틀, 34, 길이 + 8, 가상머리합(내주소, adresa, 길이 + 8))) & 65535;
        넣기16(출력틀, 40, kontrolni_zbir == 0 ? 65535 : kontrolni_zbir);
        KR = Mreža_Upravljački_program.poslati(출력틀, 길이 + 42);
        return KR < 0 ? KR : 길이;
    }
    static int primiti(int pokazivač_VALUE, int[] podaci, int kapacitet_VALUE, int 제한) {
        int 칸 = INDEX(pokazivač_VALUE);
        if (칸 < 0) return -9;
        int koristiti = uređaj_VALUE.밀리초();
        while (true) {
            verifikovati();
            int 길이 = 받은길이[칸];
            if (길이 >= 0) {
                받은길이[칸] = -1;
                if (길이 > kapacitet_VALUE) return -90;
                for (int INDEX = 0; INDEX < 길이; INDEX++) podaci[INDEX] = RECEIVED_podaci[칸 * 1024 + INDEX];
                return 길이;
            }
            if (제한 == 0) return -11;
            if (uređaj_VALUE.밀리초() - koristiti >= 제한) return -110;
            uređaj_VALUE.잠시양보();
        }
    }
    static void Status_VALUE() {
        SMS_Terminal.쓰기(Mreža_Upravljački_program.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Terminal.쓰기("TX: "); SMS_Terminal.수쓰기(Mreža_Upravljački_program.송신수);
        SMS_Terminal.쓰기(" RX: "); SMS_Terminal.수쓰기(Mreža_Upravljački_program.primiti_COUNT);
        SMS_Terminal.쓰기(" DROP: "); SMS_Terminal.수쓰기(폐기수);
        SMS_Terminal.쓰기("\n");
    }
}
