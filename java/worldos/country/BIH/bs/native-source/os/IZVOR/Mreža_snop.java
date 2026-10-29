// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** statični_VALUE IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class Mreža_snop {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int Mreža_maska = 0xffffff00; /* ip.conf:NETMASK */
    static final int pristupni_uređaj_VALUE = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], RECEIVED_dužina = new int[4], RECEIVED_adresa = new int[4], RECEIVED_broj_priključka = new int[4];
    static int[] RECEIVED_podaci = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, identifikator_VALUE = 0, 폐기수 = 0;

    static int cijeli_broj_16(int[] kadar_INDEX, int Pozicija) { return (kadar_INDEX[Pozicija] << 8) | kadar_INDEX[Pozicija + 1]; }
    static int cijeli_broj_32(int[] kadar_INDEX, int Pozicija) { return (cijeli_broj_16(kadar_INDEX, Pozicija) << 16) | cijeli_broj_16(kadar_INDEX, Pozicija + 2); }
    static void 넣기16(int[] kadar_INDEX, int Pozicija, int VALUE) { kadar_INDEX[Pozicija] = (VALUE >>> 8) & 255; kadar_INDEX[Pozicija + 1] = VALUE & 255; }
    static void 넣기32(int[] kadar_INDEX, int Pozicija, int VALUE) { 넣기16(kadar_INDEX, Pozicija, VALUE >>> 16); 넣기16(kadar_INDEX, Pozicija + 2, VALUE); }
    static int SUM_VALUE(int[] kadar_INDEX, int Pokreni, int dužina_VALUE, int VALUE) {
        for (int INDEX = 0; INDEX < dužina_VALUE; INDEX += 2)
            VALUE += (kadar_INDEX[Pokreni + INDEX] << 8) | (INDEX + 1 < dužina_VALUE ? kadar_INDEX[Pokreni + INDEX + 1] : 0);
        while ((VALUE >>> 16) != 0) VALUE = (VALUE & 65535) + (VALUE >>> 16);
        return VALUE;
    }
    static int 가상머리합(int 출발, int 도착, int dužina_VALUE) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + dužina_VALUE;
    }

    static void CLEAN_proces() {
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            접속번호들[INDEX] = 0; RECEIVED_dužina[INDEX] = -1; RECEIVED_adresa[INDEX] = 0; RECEIVED_broj_priključka[INDEX] = 0;
        }
        for (int INDEX = 0; INDEX < 64; INDEX++) if (Mreža_drajver_uređaja.받기(입력틀) == 0) break;
    }
    static int INDEX(int hvatište_VALUE) { return hvatište_VALUE >= 3 && hvatište_VALUE < 7 && 접속번호들[hvatište_VALUE - 3] != 0 ? hvatište_VALUE - 3 : -1; }
    static int Otvori(int broj_priključka) {
        if (Mreža_drajver_uređaja.입출력기준주소 == 0) return -19;
        if (broj_priključka < 0 || broj_priključka > 65535) return -22;
        if (broj_priključka != 0) for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == broj_priključka) return -98;
        for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == 0) {
            if (broj_priključka == 0) {
                broj_priključka = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int 앞 = 0; 앞 < 4; 앞++) if (접속번호들[앞] == broj_priključka) 겹침 = true;
                    if (겹침) broj_priključka++;
                }
            }
            접속번호들[INDEX] = broj_priključka; RECEIVED_dužina[INDEX] = -1;
            return INDEX + 3;
        }
        return -24;
    }
    static int Zatvori(int hvatište_VALUE) {
        int prostor_za_unos_unos = INDEX(hvatište_VALUE);
        if (prostor_za_unos_unos < 0) return -9;
        접속번호들[prostor_za_unos_unos] = 0; RECEIVED_dužina[prostor_za_unos_unos] = -1;
        return 0;
    }
    static int peer_adresa(int hvatište_VALUE) { int prostor_za_unos_unos = INDEX(hvatište_VALUE); return prostor_za_unos_unos < 0 ? -9 : RECEIVED_adresa[prostor_za_unos_unos]; }
    static int peer_broj_priključka(int hvatište_VALUE) { int prostor_za_unos_unos = INDEX(hvatište_VALUE); return prostor_za_unos_unos < 0 ? -9 : RECEIVED_broj_priključka[prostor_za_unos_unos]; }

    static void 바깥머리(int 종류, boolean emitirati_VALUE) {
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[INDEX] = emitirati_VALUE ? 255 : 찾은장치[INDEX];
            출력틀[6 + INDEX] = Mreža_drajver_uređaja.uređaj_adresa[INDEX];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void HTTP_zahtjev_adresa(int odredište_VALUE) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[22 + INDEX] = Mreža_drajver_uređaja.uređaj_adresa[INDEX]; 출력틀[32 + INDEX] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, odredište_VALUE);
        Mreža_drajver_uređaja.poslati(출력틀, 42);
    }
    static void proces_adresa(int dužina_VALUE) {
        if (dužina_VALUE < 42 || cijeli_broj_16(입력틀, 14) != 1 || cijeli_broj_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || cijeli_broj_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = cijeli_broj_16(입력틀, 20), peer_VALUE = cijeli_broj_32(입력틀, 28);
        if (종류 == 2 && peer_VALUE == 찾을주소) {
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                if (입력틀[6 + INDEX] != 입력틀[22 + INDEX] || 입력틀[32 + INDEX] != Mreža_drajver_uređaja.uređaj_adresa[INDEX]) return;
            }
            for (int INDEX = 0; INDEX < 6; INDEX++) 찾은장치[INDEX] = 입력틀[22 + INDEX];
            찾은주소 = peer_VALUE;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                출력틀[INDEX] = 입력틀[22 + INDEX]; 출력틀[32 + INDEX] = 입력틀[22 + INDEX];
                출력틀[22 + INDEX] = Mreža_drajver_uređaja.uređaj_adresa[INDEX];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, peer_VALUE);
            Mreža_drajver_uređaja.poslati(출력틀, 42);
        }
    }

    static void proces_kadar(int dužina_VALUE) {
        if (dužina_VALUE < 14 || dužina_VALUE > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, emitirati_VALUE = true;
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            if (입력틀[INDEX] != Mreža_drajver_uređaja.uređaj_adresa[INDEX]) 자기 = false;
            if (입력틀[INDEX] != 255) emitirati_VALUE = false;
        }
        if (!자기 && !emitirati_VALUE) return;
        if (cijeli_broj_16(입력틀, 12) == 0x0806) { proces_adresa(dužina_VALUE); return; }
        if (cijeli_broj_16(입력틀, 12) != 0x0800) return;
        if (dužina_VALUE < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int Zaglavlje_dužina = (입력틀[14] & 15) * 4, 전체길이 = cijeli_broj_16(입력틀, 16);
        if (Zaglavlje_dužina < 20 || Zaglavlje_dužina > 60 || 전체길이 < Zaglavlje_dužina + 8 || 전체길이 > dužina_VALUE - 14
            || (cijeli_broj_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || cijeli_broj_32(입력틀, 30) != 내주소 || SUM_VALUE(입력틀, 14, Zaglavlje_dužina, 0) != 65535) { 폐기수++; return; }
        int Pokreni = 14 + Zaglavlje_dužina, podaci_dužina = cijeli_broj_16(입력틀, Pokreni + 4);
        if (podaci_dužina < 8 || podaci_dužina != 전체길이 - Zaglavlje_dužina || podaci_dužina > 1032) { 폐기수++; return; }
        int 출발 = cijeli_broj_32(입력틀, 26);
        if (cijeli_broj_16(입력틀, Pokreni + 6) != 0 && SUM_VALUE(입력틀, Pokreni, podaci_dužina, 가상머리합(출발, 내주소, podaci_dužina)) != 65535) {
            폐기수++; return;
        }
        int odredište_VALUE = cijeli_broj_16(입력틀, Pokreni + 2);
        for (int prostor_za_unos_unos = 0; prostor_za_unos_unos < 4; prostor_za_unos_unos++) if (접속번호들[prostor_za_unos_unos] != 0 && 접속번호들[prostor_za_unos_unos] == odredište_VALUE) {
            if (RECEIVED_dužina[prostor_za_unos_unos] >= 0) { 폐기수++; return; }
            RECEIVED_dužina[prostor_za_unos_unos] = podaci_dužina - 8; RECEIVED_adresa[prostor_za_unos_unos] = 출발; RECEIVED_broj_priključka[prostor_za_unos_unos] = cijeli_broj_16(입력틀, Pokreni);
            for (int INDEX = 0; INDEX < podaci_dužina - 8; INDEX++) RECEIVED_podaci[prostor_za_unos_unos * 1024 + INDEX] = 입력틀[Pokreni + 8 + INDEX];
            return;
        }
    }

    static void potvrditi() {
        for (int INDEX = 0; INDEX < 16; INDEX++) {
            int dužina_VALUE = Mreža_drajver_uređaja.받기(입력틀);
            if (dužina_VALUE == 0) return;
            proces_kadar(dužina_VALUE);
        }
    }
    static int FIND_adresa(int adresa) {
        if (adresa == 0 || adresa == -1 || (adresa >>> 28) >= 14 || (adresa >>> 24) == 127 || adresa == 내주소) return -101;
        int Dalje_stavka = (adresa & Mreža_maska) == (내주소 & Mreža_maska) ? adresa : pristupni_uređaj_VALUE;
        if (Dalje_stavka == 찾은주소) return 0;
        찾을주소 = Dalje_stavka;
        int Pokreni = uređaj_VALUE.밀리초(), Dalje_HTTP_zahtjev = Pokreni;
        while (uređaj_VALUE.밀리초() - Pokreni < 1000) {
            if (uređaj_VALUE.밀리초() - Dalje_HTTP_zahtjev >= 0) { HTTP_zahtjev_adresa(Dalje_stavka); Dalje_HTTP_zahtjev += 300; }
            potvrditi();
            if (찾은주소 == Dalje_stavka) return 0;
            uređaj_VALUE.잠시양보();
        }
        return -110;
    }
    static int poslati(int hvatište_VALUE, int adresa, int broj_priključka, int[] podaci, int dužina_VALUE) {
        int prostor_za_unos_unos = INDEX(hvatište_VALUE);
        if (prostor_za_unos_unos < 0) return -9;
        if (Mreža_drajver_uređaja.입출력기준주소 == 0) return -19;
        if (broj_priključka < 1 || broj_priključka > 65535 || dužina_VALUE < 0 || dužina_VALUE > 1024) return -22;
        int mjera = FIND_adresa(adresa);
        if (mjera < 0) return mjera;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + dužina_VALUE);
        넣기16(출력틀, 18, identifikator_VALUE++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, adresa);
        넣기16(출력틀, 24, ~SUM_VALUE(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[prostor_za_unos_unos]); 넣기16(출력틀, 36, broj_priključka);
        넣기16(출력틀, 38, dužina_VALUE + 8); 넣기16(출력틀, 40, 0);
        for (int INDEX = 0; INDEX < dužina_VALUE; INDEX++) 출력틀[42 + INDEX] = podaci[INDEX] & 255;
        int kontrolni_zbir = (~SUM_VALUE(출력틀, 34, dužina_VALUE + 8, 가상머리합(내주소, adresa, dužina_VALUE + 8))) & 65535;
        넣기16(출력틀, 40, kontrolni_zbir == 0 ? 65535 : kontrolni_zbir);
        mjera = Mreža_drajver_uređaja.poslati(출력틀, dužina_VALUE + 42);
        return mjera < 0 ? mjera : dužina_VALUE;
    }
    static int 받기(int hvatište_VALUE, int[] podaci, int 용량, int 제한) {
        int prostor_za_unos_unos = INDEX(hvatište_VALUE);
        if (prostor_za_unos_unos < 0) return -9;
        int Pokreni = uređaj_VALUE.밀리초();
        while (true) {
            potvrditi();
            int dužina_VALUE = RECEIVED_dužina[prostor_za_unos_unos];
            if (dužina_VALUE >= 0) {
                RECEIVED_dužina[prostor_za_unos_unos] = -1;
                if (dužina_VALUE > 용량) return -90;
                for (int INDEX = 0; INDEX < dužina_VALUE; INDEX++) podaci[INDEX] = RECEIVED_podaci[prostor_za_unos_unos * 1024 + INDEX];
                return dužina_VALUE;
            }
            if (제한 == 0) return -11;
            if (uređaj_VALUE.밀리초() - Pokreni >= 제한) return -110;
            uređaj_VALUE.잠시양보();
        }
    }
    static void stanje_VALUE() {
        SMS_Terminal.Piši(Mreža_drajver_uređaja.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Terminal.Piši("TX: "); SMS_Terminal.수쓰기(Mreža_drajver_uređaja.prenositi_COUNT);
        SMS_Terminal.Piši(" RX: "); SMS_Terminal.수쓰기(Mreža_drajver_uređaja.수신수);
        SMS_Terminal.Piši(" DROP: "); SMS_Terminal.수쓰기(폐기수);
        SMS_Terminal.Piši("\n");
    }
}
