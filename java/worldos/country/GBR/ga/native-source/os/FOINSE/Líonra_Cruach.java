// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** statach_VALUE IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class Líonra_Cruach {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int Líonra_masc = 0xffffff00; /* ip.conf:NETMASK */
    static final int geata_VALUE = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], RECEIVED_fad = new int[4], RECEIVED_ADDRESS = new int[4], RECEIVED_uimhir_phoirt = new int[4];
    static int[] RECEIVED_sonraí = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, aitheantóir_VALUE = 0, 폐기수 = 0;

    static int slánuimhir_16(int[] fráma_INDEX, int suíomh) { return (fráma_INDEX[suíomh] << 8) | fráma_INDEX[suíomh + 1]; }
    static int slánuimhir_32(int[] fráma_INDEX, int suíomh) { return (slánuimhir_16(fráma_INDEX, suíomh) << 16) | slánuimhir_16(fráma_INDEX, suíomh + 2); }
    static void 넣기16(int[] fráma_INDEX, int suíomh, int VALUE) { fráma_INDEX[suíomh] = (VALUE >>> 8) & 255; fráma_INDEX[suíomh + 1] = VALUE & 255; }
    static void 넣기32(int[] fráma_INDEX, int suíomh, int VALUE) { 넣기16(fráma_INDEX, suíomh, VALUE >>> 16); 넣기16(fráma_INDEX, suíomh + 2, VALUE); }
    static int SUM_VALUE(int[] fráma_INDEX, int Rith_2, int fad_VALUE, int VALUE) {
        for (int INDEX = 0; INDEX < fad_VALUE; INDEX += 2)
            VALUE += (fráma_INDEX[Rith_2 + INDEX] << 8) | (INDEX + 1 < fad_VALUE ? fráma_INDEX[Rith_2 + INDEX + 1] : 0);
        while ((VALUE >>> 16) != 0) VALUE = (VALUE & 65535) + (VALUE >>> 16);
        return VALUE;
    }
    static int 가상머리합(int 출발, int 도착, int fad_VALUE) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + fad_VALUE;
    }

    static void CLEAN_Próiseas() {
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            접속번호들[INDEX] = 0; RECEIVED_fad[INDEX] = -1; RECEIVED_ADDRESS[INDEX] = 0; RECEIVED_uimhir_phoirt[INDEX] = 0;
        }
        for (int INDEX = 0; INDEX < 64; INDEX++) if (Líonra_tiománaí.받기(입력틀) == 0) break;
    }
    static int INDEX(int hanla_VALUE) { return hanla_VALUE >= 3 && hanla_VALUE < 7 && 접속번호들[hanla_VALUE - 3] != 0 ? hanla_VALUE - 3 : -1; }
    static int Oscail(int uimhir_phoirt) {
        if (Líonra_tiománaí.입출력기준주소 == 0) return -19;
        if (uimhir_phoirt < 0 || uimhir_phoirt > 65535) return -22;
        if (uimhir_phoirt != 0) for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == uimhir_phoirt) return -98;
        for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == 0) {
            if (uimhir_phoirt == 0) {
                uimhir_phoirt = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int 앞 = 0; 앞 < 4; 앞++) if (접속번호들[앞] == uimhir_phoirt) 겹침 = true;
                    if (겹침) uimhir_phoirt++;
                }
            }
            접속번호들[INDEX] = uimhir_phoirt; RECEIVED_fad[INDEX] = -1;
            return INDEX + 3;
        }
        return -24;
    }
    static int Dún(int hanla_VALUE) {
        int spás_iontráil = INDEX(hanla_VALUE);
        if (spás_iontráil < 0) return -9;
        접속번호들[spás_iontráil] = 0; RECEIVED_fad[spás_iontráil] = -1;
        return 0;
    }
    static int piara_ADDRESS(int hanla_VALUE) { int spás_iontráil = INDEX(hanla_VALUE); return spás_iontráil < 0 ? -9 : RECEIVED_ADDRESS[spás_iontráil]; }
    static int piara_uimhir_phoirt(int hanla_VALUE) { int spás_iontráil = INDEX(hanla_VALUE); return spás_iontráil < 0 ? -9 : RECEIVED_uimhir_phoirt[spás_iontráil]; }

    static void 바깥머리(int 종류, boolean craolachán_VALUE) {
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[INDEX] = craolachán_VALUE ? 255 : 찾은장치[INDEX];
            출력틀[6 + INDEX] = Líonra_tiománaí.gléas_ADDRESS[INDEX];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void iarratas_HTTP_ADDRESS(int sprioc_VALUE) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[22 + INDEX] = Líonra_tiománaí.gléas_ADDRESS[INDEX]; 출력틀[32 + INDEX] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, sprioc_VALUE);
        Líonra_tiománaí.seol(출력틀, 42);
    }
    static void Próiseas_ADDRESS(int fad_VALUE) {
        if (fad_VALUE < 42 || slánuimhir_16(입력틀, 14) != 1 || slánuimhir_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || slánuimhir_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = slánuimhir_16(입력틀, 20), piara_VALUE = slánuimhir_32(입력틀, 28);
        if (종류 == 2 && piara_VALUE == 찾을주소) {
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                if (입력틀[6 + INDEX] != 입력틀[22 + INDEX] || 입력틀[32 + INDEX] != Líonra_tiománaí.gléas_ADDRESS[INDEX]) return;
            }
            for (int INDEX = 0; INDEX < 6; INDEX++) 찾은장치[INDEX] = 입력틀[22 + INDEX];
            찾은주소 = piara_VALUE;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                출력틀[INDEX] = 입력틀[22 + INDEX]; 출력틀[32 + INDEX] = 입력틀[22 + INDEX];
                출력틀[22 + INDEX] = Líonra_tiománaí.gléas_ADDRESS[INDEX];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, piara_VALUE);
            Líonra_tiománaí.seol(출력틀, 42);
        }
    }

    static void Próiseas_fráma(int fad_VALUE) {
        if (fad_VALUE < 14 || fad_VALUE > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, craolachán_VALUE = true;
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            if (입력틀[INDEX] != Líonra_tiománaí.gléas_ADDRESS[INDEX]) 자기 = false;
            if (입력틀[INDEX] != 255) craolachán_VALUE = false;
        }
        if (!자기 && !craolachán_VALUE) return;
        if (slánuimhir_16(입력틀, 12) == 0x0806) { Próiseas_ADDRESS(fad_VALUE); return; }
        if (slánuimhir_16(입력틀, 12) != 0x0800) return;
        if (fad_VALUE < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int Ceanntásc_fad = (입력틀[14] & 15) * 4, 전체길이 = slánuimhir_16(입력틀, 16);
        if (Ceanntásc_fad < 20 || Ceanntásc_fad > 60 || 전체길이 < Ceanntásc_fad + 8 || 전체길이 > fad_VALUE - 14
            || (slánuimhir_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || slánuimhir_32(입력틀, 30) != 내주소 || SUM_VALUE(입력틀, 14, Ceanntásc_fad, 0) != 65535) { 폐기수++; return; }
        int Rith_2 = 14 + Ceanntásc_fad, sonraí_fad = slánuimhir_16(입력틀, Rith_2 + 4);
        if (sonraí_fad < 8 || sonraí_fad != 전체길이 - Ceanntásc_fad || sonraí_fad > 1032) { 폐기수++; return; }
        int 출발 = slánuimhir_32(입력틀, 26);
        if (slánuimhir_16(입력틀, Rith_2 + 6) != 0 && SUM_VALUE(입력틀, Rith_2, sonraí_fad, 가상머리합(출발, 내주소, sonraí_fad)) != 65535) {
            폐기수++; return;
        }
        int sprioc_VALUE = slánuimhir_16(입력틀, Rith_2 + 2);
        for (int spás_iontráil = 0; spás_iontráil < 4; spás_iontráil++) if (접속번호들[spás_iontráil] != 0 && 접속번호들[spás_iontráil] == sprioc_VALUE) {
            if (RECEIVED_fad[spás_iontráil] >= 0) { 폐기수++; return; }
            RECEIVED_fad[spás_iontráil] = sonraí_fad - 8; RECEIVED_ADDRESS[spás_iontráil] = 출발; RECEIVED_uimhir_phoirt[spás_iontráil] = slánuimhir_16(입력틀, Rith_2);
            for (int INDEX = 0; INDEX < sonraí_fad - 8; INDEX++) RECEIVED_sonraí[spás_iontráil * 1024 + INDEX] = 입력틀[Rith_2 + 8 + INDEX];
            return;
        }
    }

    static void fíoraigh() {
        for (int INDEX = 0; INDEX < 16; INDEX++) {
            int fad_VALUE = Líonra_tiománaí.받기(입력틀);
            if (fad_VALUE == 0) return;
            Próiseas_fráma(fad_VALUE);
        }
    }
    static int FIND_ADDRESS(int ADDRESS) {
        if (ADDRESS == 0 || ADDRESS == -1 || (ADDRESS >>> 28) >= 14 || (ADDRESS >>> 24) == 127 || ADDRESS == 내주소) return -101;
        int Ar_aghaidh_mír = (ADDRESS & Líonra_masc) == (내주소 & Líonra_masc) ? ADDRESS : geata_VALUE;
        if (Ar_aghaidh_mír == 찾은주소) return 0;
        찾을주소 = Ar_aghaidh_mír;
        int Rith_2 = gléas_VALUE.밀리초(), Ar_aghaidh_iarratas_HTTP = Rith_2;
        while (gléas_VALUE.밀리초() - Rith_2 < 1000) {
            if (gléas_VALUE.밀리초() - Ar_aghaidh_iarratas_HTTP >= 0) { iarratas_HTTP_ADDRESS(Ar_aghaidh_mír); Ar_aghaidh_iarratas_HTTP += 300; }
            fíoraigh();
            if (찾은주소 == Ar_aghaidh_mír) return 0;
            gléas_VALUE.잠시양보();
        }
        return -110;
    }
    static int seol(int hanla_VALUE, int ADDRESS, int uimhir_phoirt, int[] sonraí, int fad_VALUE) {
        int spás_iontráil = INDEX(hanla_VALUE);
        if (spás_iontráil < 0) return -9;
        if (Líonra_tiománaí.입출력기준주소 == 0) return -19;
        if (uimhir_phoirt < 1 || uimhir_phoirt > 65535 || fad_VALUE < 0 || fad_VALUE > 1024) return -22;
        int tomhas = FIND_ADDRESS(ADDRESS);
        if (tomhas < 0) return tomhas;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + fad_VALUE);
        넣기16(출력틀, 18, aitheantóir_VALUE++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, ADDRESS);
        넣기16(출력틀, 24, ~SUM_VALUE(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[spás_iontráil]); 넣기16(출력틀, 36, uimhir_phoirt);
        넣기16(출력틀, 38, fad_VALUE + 8); 넣기16(출력틀, 40, 0);
        for (int INDEX = 0; INDEX < fad_VALUE; INDEX++) 출력틀[42 + INDEX] = sonraí[INDEX] & 255;
        int suim_seiceála = (~SUM_VALUE(출력틀, 34, fad_VALUE + 8, 가상머리합(내주소, ADDRESS, fad_VALUE + 8))) & 65535;
        넣기16(출력틀, 40, suim_seiceála == 0 ? 65535 : suim_seiceála);
        tomhas = Líonra_tiománaí.seol(출력틀, fad_VALUE + 42);
        return tomhas < 0 ? tomhas : fad_VALUE;
    }
    static int 받기(int hanla_VALUE, int[] sonraí, int 용량, int 제한) {
        int spás_iontráil = INDEX(hanla_VALUE);
        if (spás_iontráil < 0) return -9;
        int Rith_2 = gléas_VALUE.밀리초();
        while (true) {
            fíoraigh();
            int fad_VALUE = RECEIVED_fad[spás_iontráil];
            if (fad_VALUE >= 0) {
                RECEIVED_fad[spás_iontráil] = -1;
                if (fad_VALUE > 용량) return -90;
                for (int INDEX = 0; INDEX < fad_VALUE; INDEX++) sonraí[INDEX] = RECEIVED_sonraí[spás_iontráil * 1024 + INDEX];
                return fad_VALUE;
            }
            if (제한 == 0) return -11;
            if (gléas_VALUE.밀리초() - Rith_2 >= 제한) return -110;
            gléas_VALUE.잠시양보();
        }
    }
    static void staid_VALUE() {
        SMS_Teirminéal.Scríobh(Líonra_tiománaí.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Teirminéal.Scríobh("TX: "); SMS_Teirminéal.수쓰기(Líonra_tiománaí.송신수);
        SMS_Teirminéal.Scríobh(" RX: "); SMS_Teirminéal.수쓰기(Líonra_tiománaí.수신수);
        SMS_Teirminéal.Scríobh(" DROP: "); SMS_Teirminéal.수쓰기(폐기수);
        SMS_Teirminéal.Scríobh("\n");
    }
}
