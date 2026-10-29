// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** statik_VALUE IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class rrjet_Stivë {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int rrjet_maskë = 0xffffff00; /* ip.conf:NETMASK */
    static final int portëkalimi_VALUE = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], RECEIVED_gjatësi = new int[4], RECEIVED_email = new int[4], RECEIVED_numri_i_portës = new int[4];
    static int[] RECEIVED_të_dhëna = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, identifikues_VALUE = 0, 폐기수 = 0;

    static int numër_i_plotë_16(int[] kuadër_INDEX, int Pozicioni) { return (kuadër_INDEX[Pozicioni] << 8) | kuadër_INDEX[Pozicioni + 1]; }
    static int numër_i_plotë_32(int[] kuadër_INDEX, int Pozicioni) { return (numër_i_plotë_16(kuadër_INDEX, Pozicioni) << 16) | numër_i_plotë_16(kuadër_INDEX, Pozicioni + 2); }
    static void 넣기16(int[] kuadër_INDEX, int Pozicioni, int VALUE) { kuadër_INDEX[Pozicioni] = (VALUE >>> 8) & 255; kuadër_INDEX[Pozicioni + 1] = VALUE & 255; }
    static void 넣기32(int[] kuadër_INDEX, int Pozicioni, int VALUE) { 넣기16(kuadër_INDEX, Pozicioni, VALUE >>> 16); 넣기16(kuadër_INDEX, Pozicioni + 2, VALUE); }
    static int SUM_VALUE(int[] kuadër_INDEX, int Ekzekuto, int gjatësi_VALUE, int VALUE) {
        for (int INDEX = 0; INDEX < gjatësi_VALUE; INDEX += 2)
            VALUE += (kuadër_INDEX[Ekzekuto + INDEX] << 8) | (INDEX + 1 < gjatësi_VALUE ? kuadër_INDEX[Ekzekuto + INDEX + 1] : 0);
        while ((VALUE >>> 16) != 0) VALUE = (VALUE & 65535) + (VALUE >>> 16);
        return VALUE;
    }
    static int 가상머리합(int 출발, int 도착, int gjatësi_VALUE) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + gjatësi_VALUE;
    }

    static void CLEAN_Proces() {
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            접속번호들[INDEX] = 0; RECEIVED_gjatësi[INDEX] = -1; RECEIVED_email[INDEX] = 0; RECEIVED_numri_i_portës[INDEX] = 0;
        }
        for (int INDEX = 0; INDEX < 64; INDEX++) if (rrjet_drejtues.받기(입력틀) == 0) break;
    }
    static int INDEX(int dorezë_VALUE) { return dorezë_VALUE >= 3 && dorezë_VALUE < 7 && 접속번호들[dorezë_VALUE - 3] != 0 ? dorezë_VALUE - 3 : -1; }
    static int Hap(int numri_i_portës) {
        if (rrjet_drejtues.입출력기준주소 == 0) return -19;
        if (numri_i_portës < 0 || numri_i_portës > 65535) return -22;
        if (numri_i_portës != 0) for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == numri_i_portës) return -98;
        for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == 0) {
            if (numri_i_portës == 0) {
                numri_i_portës = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int e_përparme_VALUE = 0; e_përparme_VALUE < 4; e_përparme_VALUE++) if (접속번호들[e_përparme_VALUE] == numri_i_portës) 겹침 = true;
                    if (겹침) numri_i_portës++;
                }
            }
            접속번호들[INDEX] = numri_i_portës; RECEIVED_gjatësi[INDEX] = -1;
            return INDEX + 3;
        }
        return -24;
    }
    static int Mbyll(int dorezë_VALUE) {
        int hapësirë_për_tekst_futje = INDEX(dorezë_VALUE);
        if (hapësirë_për_tekst_futje < 0) return -9;
        접속번호들[hapësirë_për_tekst_futje] = 0; RECEIVED_gjatësi[hapësirë_për_tekst_futje] = -1;
        return 0;
    }
    static int homolog_email(int dorezë_VALUE) { int hapësirë_për_tekst_futje = INDEX(dorezë_VALUE); return hapësirë_për_tekst_futje < 0 ? -9 : RECEIVED_email[hapësirë_për_tekst_futje]; }
    static int homolog_numri_i_portës(int dorezë_VALUE) { int hapësirë_për_tekst_futje = INDEX(dorezë_VALUE); return hapësirë_për_tekst_futje < 0 ? -9 : RECEIVED_numri_i_portës[hapësirë_për_tekst_futje]; }

    static void 바깥머리(int 종류, boolean transmetoj_VALUE) {
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[INDEX] = transmetoj_VALUE ? 255 : 찾은장치[INDEX];
            출력틀[6 + INDEX] = rrjet_drejtues.pajisje_email[INDEX];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void 주소요청(int vendmbërritje_VALUE) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[22 + INDEX] = rrjet_drejtues.pajisje_email[INDEX]; 출력틀[32 + INDEX] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, vendmbërritje_VALUE);
        rrjet_drejtues.dërgoj(출력틀, 42);
    }
    static void Proces_email(int gjatësi_VALUE) {
        if (gjatësi_VALUE < 42 || numër_i_plotë_16(입력틀, 14) != 1 || numër_i_plotë_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || numër_i_plotë_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = numër_i_plotë_16(입력틀, 20), homolog_VALUE = numër_i_plotë_32(입력틀, 28);
        if (종류 == 2 && homolog_VALUE == 찾을주소) {
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                if (입력틀[6 + INDEX] != 입력틀[22 + INDEX] || 입력틀[32 + INDEX] != rrjet_drejtues.pajisje_email[INDEX]) return;
            }
            for (int INDEX = 0; INDEX < 6; INDEX++) 찾은장치[INDEX] = 입력틀[22 + INDEX];
            찾은주소 = homolog_VALUE;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                출력틀[INDEX] = 입력틀[22 + INDEX]; 출력틀[32 + INDEX] = 입력틀[22 + INDEX];
                출력틀[22 + INDEX] = rrjet_drejtues.pajisje_email[INDEX];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, homolog_VALUE);
            rrjet_drejtues.dërgoj(출력틀, 42);
        }
    }

    static void Proces_kuadër(int gjatësi_VALUE) {
        if (gjatësi_VALUE < 14 || gjatësi_VALUE > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, transmetoj_VALUE = true;
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            if (입력틀[INDEX] != rrjet_drejtues.pajisje_email[INDEX]) 자기 = false;
            if (입력틀[INDEX] != 255) transmetoj_VALUE = false;
        }
        if (!자기 && !transmetoj_VALUE) return;
        if (numër_i_plotë_16(입력틀, 12) == 0x0806) { Proces_email(gjatësi_VALUE); return; }
        if (numër_i_plotë_16(입력틀, 12) != 0x0800) return;
        if (gjatësi_VALUE < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int Kreu_gjatësi = (입력틀[14] & 15) * 4, 전체길이 = numër_i_plotë_16(입력틀, 16);
        if (Kreu_gjatësi < 20 || Kreu_gjatësi > 60 || 전체길이 < Kreu_gjatësi + 8 || 전체길이 > gjatësi_VALUE - 14
            || (numër_i_plotë_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || numër_i_plotë_32(입력틀, 30) != 내주소 || SUM_VALUE(입력틀, 14, Kreu_gjatësi, 0) != 65535) { 폐기수++; return; }
        int Ekzekuto = 14 + Kreu_gjatësi, të_dhëna_gjatësi = numër_i_plotë_16(입력틀, Ekzekuto + 4);
        if (të_dhëna_gjatësi < 8 || të_dhëna_gjatësi != 전체길이 - Kreu_gjatësi || të_dhëna_gjatësi > 1032) { 폐기수++; return; }
        int 출발 = numër_i_plotë_32(입력틀, 26);
        if (numër_i_plotë_16(입력틀, Ekzekuto + 6) != 0 && SUM_VALUE(입력틀, Ekzekuto, të_dhëna_gjatësi, 가상머리합(출발, 내주소, të_dhëna_gjatësi)) != 65535) {
            폐기수++; return;
        }
        int vendmbërritje_VALUE = numër_i_plotë_16(입력틀, Ekzekuto + 2);
        for (int hapësirë_për_tekst_futje = 0; hapësirë_për_tekst_futje < 4; hapësirë_për_tekst_futje++) if (접속번호들[hapësirë_për_tekst_futje] != 0 && 접속번호들[hapësirë_për_tekst_futje] == vendmbërritje_VALUE) {
            if (RECEIVED_gjatësi[hapësirë_për_tekst_futje] >= 0) { 폐기수++; return; }
            RECEIVED_gjatësi[hapësirë_për_tekst_futje] = të_dhëna_gjatësi - 8; RECEIVED_email[hapësirë_për_tekst_futje] = 출발; RECEIVED_numri_i_portës[hapësirë_për_tekst_futje] = numër_i_plotë_16(입력틀, Ekzekuto);
            for (int INDEX = 0; INDEX < të_dhëna_gjatësi - 8; INDEX++) RECEIVED_të_dhëna[hapësirë_për_tekst_futje * 1024 + INDEX] = 입력틀[Ekzekuto + 8 + INDEX];
            return;
        }
    }

    static void verifikoj() {
        for (int INDEX = 0; INDEX < 16; INDEX++) {
            int gjatësi_VALUE = rrjet_drejtues.받기(입력틀);
            if (gjatësi_VALUE == 0) return;
            Proces_kuadër(gjatësi_VALUE);
        }
    }
    static int FIND_email(int email) {
        if (email == 0 || email == -1 || (email >>> 28) >= 14 || (email >>> 24) == 127 || email == 내주소) return -101;
        int Tjetër_njësi = (email & rrjet_maskë) == (내주소 & rrjet_maskë) ? email : portëkalimi_VALUE;
        if (Tjetër_njësi == 찾은주소) return 0;
        찾을주소 = Tjetër_njësi;
        int Ekzekuto = pajisje_VALUE.밀리초(), 다음요청 = Ekzekuto;
        while (pajisje_VALUE.밀리초() - Ekzekuto < 1000) {
            if (pajisje_VALUE.밀리초() - 다음요청 >= 0) { 주소요청(Tjetër_njësi); 다음요청 += 300; }
            verifikoj();
            if (찾은주소 == Tjetër_njësi) return 0;
            pajisje_VALUE.잠시양보();
        }
        return -110;
    }
    static int dërgoj(int dorezë_VALUE, int email, int numri_i_portës, int[] të_dhëna, int gjatësi_VALUE) {
        int hapësirë_për_tekst_futje = INDEX(dorezë_VALUE);
        if (hapësirë_për_tekst_futje < 0) return -9;
        if (rrjet_drejtues.입출력기준주소 == 0) return -19;
        if (numri_i_portës < 1 || numri_i_portës > 65535 || gjatësi_VALUE < 0 || gjatësi_VALUE > 1024) return -22;
        int llogaritje = FIND_email(email);
        if (llogaritje < 0) return llogaritje;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + gjatësi_VALUE);
        넣기16(출력틀, 18, identifikues_VALUE++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, email);
        넣기16(출력틀, 24, ~SUM_VALUE(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[hapësirë_për_tekst_futje]); 넣기16(출력틀, 36, numri_i_portës);
        넣기16(출력틀, 38, gjatësi_VALUE + 8); 넣기16(출력틀, 40, 0);
        for (int INDEX = 0; INDEX < gjatësi_VALUE; INDEX++) 출력틀[42 + INDEX] = të_dhëna[INDEX] & 255;
        int kontrolli_i_shumës = (~SUM_VALUE(출력틀, 34, gjatësi_VALUE + 8, 가상머리합(내주소, email, gjatësi_VALUE + 8))) & 65535;
        넣기16(출력틀, 40, kontrolli_i_shumës == 0 ? 65535 : kontrolli_i_shumës);
        llogaritje = rrjet_drejtues.dërgoj(출력틀, gjatësi_VALUE + 42);
        return llogaritje < 0 ? llogaritje : gjatësi_VALUE;
    }
    static int 받기(int dorezë_VALUE, int[] të_dhëna, int 용량, int 제한) {
        int hapësirë_për_tekst_futje = INDEX(dorezë_VALUE);
        if (hapësirë_për_tekst_futje < 0) return -9;
        int Ekzekuto = pajisje_VALUE.밀리초();
        while (true) {
            verifikoj();
            int gjatësi_VALUE = RECEIVED_gjatësi[hapësirë_për_tekst_futje];
            if (gjatësi_VALUE >= 0) {
                RECEIVED_gjatësi[hapësirë_për_tekst_futje] = -1;
                if (gjatësi_VALUE > 용량) return -90;
                for (int INDEX = 0; INDEX < gjatësi_VALUE; INDEX++) të_dhëna[INDEX] = RECEIVED_të_dhëna[hapësirë_për_tekst_futje * 1024 + INDEX];
                return gjatësi_VALUE;
            }
            if (제한 == 0) return -11;
            if (pajisje_VALUE.밀리초() - Ekzekuto >= 제한) return -110;
            pajisje_VALUE.잠시양보();
        }
    }
    static void status_VALUE() {
        SMS_Terminali.Shkrimi(rrjet_drejtues.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Terminali.Shkrimi("TX: "); SMS_Terminali.수쓰기(rrjet_drejtues.송신수);
        SMS_Terminali.Shkrimi(" RX: "); SMS_Terminali.수쓰기(rrjet_drejtues.수신수);
        SMS_Terminali.Shkrimi(" DROP: "); SMS_Terminali.수쓰기(폐기수);
        SMS_Terminali.Shkrimi("\n");
    }
}
