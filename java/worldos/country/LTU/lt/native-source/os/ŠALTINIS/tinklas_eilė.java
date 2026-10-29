// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 정적 IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class tinklas_eilė {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int tinklas_šablonas = 0xffffff00; /* ip.conf:NETMASK */
    static final int šliuzas_VALUE = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], išeiga_kadras = new int[1536];
    static int[] 접속번호들 = new int[4], 받은길이 = new int[4], RECEIVED_ADDRESS = new int[4], RECEIVED_prievado_numeris = new int[4];
    static int[] RECEIVED_duomenys = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, identifikatorius_VALUE = 0, 폐기수 = 0;

    static int sveikasis_skaičius_16(int[] kadras_INDEX, int Pozicija) { return (kadras_INDEX[Pozicija] << 8) | kadras_INDEX[Pozicija + 1]; }
    static int sveikasis_skaičius_32(int[] kadras_INDEX, int Pozicija) { return (sveikasis_skaičius_16(kadras_INDEX, Pozicija) << 16) | sveikasis_skaičius_16(kadras_INDEX, Pozicija + 2); }
    static void 넣기16(int[] kadras_INDEX, int Pozicija, int VALUE) { kadras_INDEX[Pozicija] = (VALUE >>> 8) & 255; kadras_INDEX[Pozicija + 1] = VALUE & 255; }
    static void 넣기32(int[] kadras_INDEX, int Pozicija, int VALUE) { 넣기16(kadras_INDEX, Pozicija, VALUE >>> 16); 넣기16(kadras_INDEX, Pozicija + 2, VALUE); }
    static int SUM_VALUE(int[] kadras_INDEX, int Paleisti, int 길이, int VALUE) {
        for (int INDEX = 0; INDEX < 길이; INDEX += 2)
            VALUE += (kadras_INDEX[Paleisti + INDEX] << 8) | (INDEX + 1 < 길이 ? kadras_INDEX[Paleisti + INDEX + 1] : 0);
        while ((VALUE >>> 16) != 0) VALUE = (VALUE & 65535) + (VALUE >>> 16);
        return VALUE;
    }
    static int 가상머리합(int 출발, int 도착, int 길이) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + 길이;
    }

    static void CLEAN_Procesas() {
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            접속번호들[INDEX] = 0; 받은길이[INDEX] = -1; RECEIVED_ADDRESS[INDEX] = 0; RECEIVED_prievado_numeris[INDEX] = 0;
        }
        for (int INDEX = 0; INDEX < 64; INDEX++) if (tinklas_tvarkyklė.gauti(입력틀) == 0) break;
    }
    static int INDEX(int rodyklė_VALUE) { return rodyklė_VALUE >= 3 && rodyklė_VALUE < 7 && 접속번호들[rodyklė_VALUE - 3] != 0 ? rodyklė_VALUE - 3 : -1; }
    static int Atverti(int prievado_numeris) {
        if (tinklas_tvarkyklė.입출력기준주소 == 0) return -19;
        if (prievado_numeris < 0 || prievado_numeris > 65535) return -22;
        if (prievado_numeris != 0) for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == prievado_numeris) return -98;
        for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == 0) {
            if (prievado_numeris == 0) {
                prievado_numeris = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int priekinis_VALUE = 0; priekinis_VALUE < 4; priekinis_VALUE++) if (접속번호들[priekinis_VALUE] == prievado_numeris) 겹침 = true;
                    if (겹침) prievado_numeris++;
                }
            }
            접속번호들[INDEX] = prievado_numeris; 받은길이[INDEX] = -1;
            return INDEX + 3;
        }
        return -24;
    }
    static int Užverti(int rodyklė_VALUE) {
        int 칸 = INDEX(rodyklė_VALUE);
        if (칸 < 0) return -9;
        접속번호들[칸] = 0; 받은길이[칸] = -1;
        return 0;
    }
    static int lygiavertis_mazgas_ADDRESS(int rodyklė_VALUE) { int 칸 = INDEX(rodyklė_VALUE); return 칸 < 0 ? -9 : RECEIVED_ADDRESS[칸]; }
    static int lygiavertis_mazgas_prievado_numeris(int rodyklė_VALUE) { int 칸 = INDEX(rodyklė_VALUE); return 칸 < 0 ? -9 : RECEIVED_prievado_numeris[칸]; }

    static void 바깥머리(int 종류, boolean transliuoti_VALUE) {
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            išeiga_kadras[INDEX] = transliuoti_VALUE ? 255 : 찾은장치[INDEX];
            išeiga_kadras[6 + INDEX] = tinklas_tvarkyklė.įrenginys_ADDRESS[INDEX];
        }
        넣기16(išeiga_kadras, 12, 종류);
    }
    static void užklausa_ADDRESS(int vieta_VALUE) {
        바깥머리(0x0806, true);
        넣기16(išeiga_kadras, 14, 1); 넣기16(išeiga_kadras, 16, 0x0800);
        išeiga_kadras[18] = 6; išeiga_kadras[19] = 4; 넣기16(išeiga_kadras, 20, 1);
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            išeiga_kadras[22 + INDEX] = tinklas_tvarkyklė.įrenginys_ADDRESS[INDEX]; išeiga_kadras[32 + INDEX] = 0;
        }
        넣기32(išeiga_kadras, 28, 내주소); 넣기32(išeiga_kadras, 38, vieta_VALUE);
        tinklas_tvarkyklė.siųsti(išeiga_kadras, 42);
    }
    static void Procesas_ADDRESS(int 길이) {
        if (길이 < 42 || sveikasis_skaičius_16(입력틀, 14) != 1 || sveikasis_skaičius_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || sveikasis_skaičius_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = sveikasis_skaičius_16(입력틀, 20), lygiavertis_mazgas_VALUE = sveikasis_skaičius_32(입력틀, 28);
        if (종류 == 2 && lygiavertis_mazgas_VALUE == 찾을주소) {
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                if (입력틀[6 + INDEX] != 입력틀[22 + INDEX] || 입력틀[32 + INDEX] != tinklas_tvarkyklė.įrenginys_ADDRESS[INDEX]) return;
            }
            for (int INDEX = 0; INDEX < 6; INDEX++) 찾은장치[INDEX] = 입력틀[22 + INDEX];
            찾은주소 = lygiavertis_mazgas_VALUE;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(išeiga_kadras, 14, 1); 넣기16(išeiga_kadras, 16, 0x0800);
            išeiga_kadras[18] = 6; išeiga_kadras[19] = 4; 넣기16(išeiga_kadras, 20, 2);
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                išeiga_kadras[INDEX] = 입력틀[22 + INDEX]; išeiga_kadras[32 + INDEX] = 입력틀[22 + INDEX];
                išeiga_kadras[22 + INDEX] = tinklas_tvarkyklė.įrenginys_ADDRESS[INDEX];
            }
            넣기32(išeiga_kadras, 28, 내주소); 넣기32(išeiga_kadras, 38, lygiavertis_mazgas_VALUE);
            tinklas_tvarkyklė.siųsti(išeiga_kadras, 42);
        }
    }

    static void Procesas_kadras(int 길이) {
        if (길이 < 14 || 길이 > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, transliuoti_VALUE = true;
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            if (입력틀[INDEX] != tinklas_tvarkyklė.įrenginys_ADDRESS[INDEX]) 자기 = false;
            if (입력틀[INDEX] != 255) transliuoti_VALUE = false;
        }
        if (!자기 && !transliuoti_VALUE) return;
        if (sveikasis_skaičius_16(입력틀, 12) == 0x0806) { Procesas_ADDRESS(길이); return; }
        if (sveikasis_skaičius_16(입력틀, 12) != 0x0800) return;
        if (길이 < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int 머리길이 = (입력틀[14] & 15) * 4, 전체길이 = sveikasis_skaičius_16(입력틀, 16);
        if (머리길이 < 20 || 머리길이 > 60 || 전체길이 < 머리길이 + 8 || 전체길이 > 길이 - 14
            || (sveikasis_skaičius_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || sveikasis_skaičius_32(입력틀, 30) != 내주소 || SUM_VALUE(입력틀, 14, 머리길이, 0) != 65535) { 폐기수++; return; }
        int Paleisti = 14 + 머리길이, 자료길이 = sveikasis_skaičius_16(입력틀, Paleisti + 4);
        if (자료길이 < 8 || 자료길이 != 전체길이 - 머리길이 || 자료길이 > 1032) { 폐기수++; return; }
        int 출발 = sveikasis_skaičius_32(입력틀, 26);
        if (sveikasis_skaičius_16(입력틀, Paleisti + 6) != 0 && SUM_VALUE(입력틀, Paleisti, 자료길이, 가상머리합(출발, 내주소, 자료길이)) != 65535) {
            폐기수++; return;
        }
        int vieta_VALUE = sveikasis_skaičius_16(입력틀, Paleisti + 2);
        for (int 칸 = 0; 칸 < 4; 칸++) if (접속번호들[칸] != 0 && 접속번호들[칸] == vieta_VALUE) {
            if (받은길이[칸] >= 0) { 폐기수++; return; }
            받은길이[칸] = 자료길이 - 8; RECEIVED_ADDRESS[칸] = 출발; RECEIVED_prievado_numeris[칸] = sveikasis_skaičius_16(입력틀, Paleisti);
            for (int INDEX = 0; INDEX < 자료길이 - 8; INDEX++) RECEIVED_duomenys[칸 * 1024 + INDEX] = 입력틀[Paleisti + 8 + INDEX];
            return;
        }
    }

    static void patvirtinti() {
        for (int INDEX = 0; INDEX < 16; INDEX++) {
            int 길이 = tinklas_tvarkyklė.gauti(입력틀);
            if (길이 == 0) return;
            Procesas_kadras(길이);
        }
    }
    static int FIND_ADDRESS(int ADDRESS) {
        if (ADDRESS == 0 || ADDRESS == -1 || (ADDRESS >>> 28) >= 14 || (ADDRESS >>> 24) == 127 || ADDRESS == 내주소) return -101;
        int toliau_prekė = (ADDRESS & tinklas_šablonas) == (내주소 & tinklas_šablonas) ? ADDRESS : šliuzas_VALUE;
        if (toliau_prekė == 찾은주소) return 0;
        찾을주소 = toliau_prekė;
        int Paleisti = įrenginys_VALUE.밀리초(), toliau_užklausa = Paleisti;
        while (įrenginys_VALUE.밀리초() - Paleisti < 1000) {
            if (įrenginys_VALUE.밀리초() - toliau_užklausa >= 0) { užklausa_ADDRESS(toliau_prekė); toliau_užklausa += 300; }
            patvirtinti();
            if (찾은주소 == toliau_prekė) return 0;
            įrenginys_VALUE.잠시양보();
        }
        return -110;
    }
    static int siųsti(int rodyklė_VALUE, int ADDRESS, int prievado_numeris, int[] duomenys, int 길이) {
        int 칸 = INDEX(rodyklė_VALUE);
        if (칸 < 0) return -9;
        if (tinklas_tvarkyklė.입출력기준주소 == 0) return -19;
        if (prievado_numeris < 1 || prievado_numeris > 65535 || 길이 < 0 || 길이 > 1024) return -22;
        int REZULTATAS = FIND_ADDRESS(ADDRESS);
        if (REZULTATAS < 0) return REZULTATAS;
        바깥머리(0x0800, false);
        išeiga_kadras[14] = 0x45; išeiga_kadras[15] = 0; 넣기16(išeiga_kadras, 16, 28 + 길이);
        넣기16(išeiga_kadras, 18, identifikatorius_VALUE++); 넣기16(išeiga_kadras, 20, 0x4000);
        išeiga_kadras[22] = 64; išeiga_kadras[23] = 17; 넣기16(išeiga_kadras, 24, 0);
        넣기32(išeiga_kadras, 26, 내주소); 넣기32(išeiga_kadras, 30, ADDRESS);
        넣기16(išeiga_kadras, 24, ~SUM_VALUE(išeiga_kadras, 14, 20, 0));
        넣기16(išeiga_kadras, 34, 접속번호들[칸]); 넣기16(išeiga_kadras, 36, prievado_numeris);
        넣기16(išeiga_kadras, 38, 길이 + 8); 넣기16(išeiga_kadras, 40, 0);
        for (int INDEX = 0; INDEX < 길이; INDEX++) išeiga_kadras[42 + INDEX] = duomenys[INDEX] & 255;
        int kontrolinė_suma = (~SUM_VALUE(išeiga_kadras, 34, 길이 + 8, 가상머리합(내주소, ADDRESS, 길이 + 8))) & 65535;
        넣기16(išeiga_kadras, 40, kontrolinė_suma == 0 ? 65535 : kontrolinė_suma);
        REZULTATAS = tinklas_tvarkyklė.siųsti(išeiga_kadras, 길이 + 42);
        return REZULTATAS < 0 ? REZULTATAS : 길이;
    }
    static int gauti(int rodyklė_VALUE, int[] duomenys, int pajėgumas_VALUE, int 제한) {
        int 칸 = INDEX(rodyklė_VALUE);
        if (칸 < 0) return -9;
        int Paleisti = įrenginys_VALUE.밀리초();
        while (true) {
            patvirtinti();
            int 길이 = 받은길이[칸];
            if (길이 >= 0) {
                받은길이[칸] = -1;
                if (길이 > pajėgumas_VALUE) return -90;
                for (int INDEX = 0; INDEX < 길이; INDEX++) duomenys[INDEX] = RECEIVED_duomenys[칸 * 1024 + INDEX];
                return 길이;
            }
            if (제한 == 0) return -11;
            if (įrenginys_VALUE.밀리초() - Paleisti >= 제한) return -110;
            įrenginys_VALUE.잠시양보();
        }
    }
    static void Būsena_VALUE() {
        SMS_Terminalas.Rašymas(tinklas_tvarkyklė.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Terminalas.Rašymas("TX: "); SMS_Terminalas.rašymas_numeris(tinklas_tvarkyklė.송신수);
        SMS_Terminalas.Rašymas(" RX: "); SMS_Terminalas.rašymas_numeris(tinklas_tvarkyklė.gauti_COUNT);
        SMS_Terminalas.Rašymas(" DROP: "); SMS_Terminalas.rašymas_numeris(폐기수);
        SMS_Terminalas.Rašymas("\n");
    }
}
