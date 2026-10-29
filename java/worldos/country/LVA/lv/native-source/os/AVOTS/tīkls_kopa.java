// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 정적 IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class tīkls_kopa {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int tīkls_maska = 0xffffff00; /* ip.conf:NETMASK */
    static final int vārteja_VALUE = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], ražojums_kadrs = new int[1536];
    static int[] 접속번호들 = new int[4], 받은길이 = new int[4], RECEIVED_adrese = new int[4], RECEIVED_porta_numurs = new int[4];
    static int[] RECEIVED_dati = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, identifikators_VALUE = 0, 폐기수 = 0;

    static int vesels_skaitlis_16(int[] kadrs_INDEX, int Novietojums) { return (kadrs_INDEX[Novietojums] << 8) | kadrs_INDEX[Novietojums + 1]; }
    static int vesels_skaitlis_32(int[] kadrs_INDEX, int Novietojums) { return (vesels_skaitlis_16(kadrs_INDEX, Novietojums) << 16) | vesels_skaitlis_16(kadrs_INDEX, Novietojums + 2); }
    static void 넣기16(int[] kadrs_INDEX, int Novietojums, int VALUE) { kadrs_INDEX[Novietojums] = (VALUE >>> 8) & 255; kadrs_INDEX[Novietojums + 1] = VALUE & 255; }
    static void 넣기32(int[] kadrs_INDEX, int Novietojums, int VALUE) { 넣기16(kadrs_INDEX, Novietojums, VALUE >>> 16); 넣기16(kadrs_INDEX, Novietojums + 2, VALUE); }
    static int SUM_VALUE(int[] kadrs_INDEX, int Palaist, int 길이, int VALUE) {
        for (int INDEX = 0; INDEX < 길이; INDEX += 2)
            VALUE += (kadrs_INDEX[Palaist + INDEX] << 8) | (INDEX + 1 < 길이 ? kadrs_INDEX[Palaist + INDEX + 1] : 0);
        while ((VALUE >>> 16) != 0) VALUE = (VALUE & 65535) + (VALUE >>> 16);
        return VALUE;
    }
    static int 가상머리합(int 출발, int 도착, int 길이) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + 길이;
    }

    static void CLEAN_Process() {
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            접속번호들[INDEX] = 0; 받은길이[INDEX] = -1; RECEIVED_adrese[INDEX] = 0; RECEIVED_porta_numurs[INDEX] = 0;
        }
        for (int INDEX = 0; INDEX < 64; INDEX++) if (tīkls_draiveris.saņemt(입력틀) == 0) break;
    }
    static int INDEX(int turis_VALUE) { return turis_VALUE >= 3 && turis_VALUE < 7 && 접속번호들[turis_VALUE - 3] != 0 ? turis_VALUE - 3 : -1; }
    static int Atvērt(int porta_numurs) {
        if (tīkls_draiveris.입출력기준주소 == 0) return -19;
        if (porta_numurs < 0 || porta_numurs > 65535) return -22;
        if (porta_numurs != 0) for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == porta_numurs) return -98;
        for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == 0) {
            if (porta_numurs == 0) {
                porta_numurs = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int priekšējā_VALUE = 0; priekšējā_VALUE < 4; priekšējā_VALUE++) if (접속번호들[priekšējā_VALUE] == porta_numurs) 겹침 = true;
                    if (겹침) porta_numurs++;
                }
            }
            접속번호들[INDEX] = porta_numurs; 받은길이[INDEX] = -1;
            return INDEX + 3;
        }
        return -24;
    }
    static int Aizvērt(int turis_VALUE) {
        int 칸 = INDEX(turis_VALUE);
        if (칸 < 0) return -9;
        접속번호들[칸] = 0; 받은길이[칸] = -1;
        return 0;
    }
    static int vienranga_adrese(int turis_VALUE) { int 칸 = INDEX(turis_VALUE); return 칸 < 0 ? -9 : RECEIVED_adrese[칸]; }
    static int vienranga_porta_numurs(int turis_VALUE) { int 칸 = INDEX(turis_VALUE); return 칸 < 0 ? -9 : RECEIVED_porta_numurs[칸]; }

    static void 바깥머리(int 종류, boolean apraide_VALUE) {
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            ražojums_kadrs[INDEX] = apraide_VALUE ? 255 : 찾은장치[INDEX];
            ražojums_kadrs[6 + INDEX] = tīkls_draiveris.ierīce_adrese[INDEX];
        }
        넣기16(ražojums_kadrs, 12, 종류);
    }
    static void pieprasījums_adrese(int mērķis_VALUE) {
        바깥머리(0x0806, true);
        넣기16(ražojums_kadrs, 14, 1); 넣기16(ražojums_kadrs, 16, 0x0800);
        ražojums_kadrs[18] = 6; ražojums_kadrs[19] = 4; 넣기16(ražojums_kadrs, 20, 1);
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            ražojums_kadrs[22 + INDEX] = tīkls_draiveris.ierīce_adrese[INDEX]; ražojums_kadrs[32 + INDEX] = 0;
        }
        넣기32(ražojums_kadrs, 28, 내주소); 넣기32(ražojums_kadrs, 38, mērķis_VALUE);
        tīkls_draiveris.sūtīt(ražojums_kadrs, 42);
    }
    static void Process_adrese(int 길이) {
        if (길이 < 42 || vesels_skaitlis_16(입력틀, 14) != 1 || vesels_skaitlis_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || vesels_skaitlis_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = vesels_skaitlis_16(입력틀, 20), vienranga_VALUE = vesels_skaitlis_32(입력틀, 28);
        if (종류 == 2 && vienranga_VALUE == 찾을주소) {
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                if (입력틀[6 + INDEX] != 입력틀[22 + INDEX] || 입력틀[32 + INDEX] != tīkls_draiveris.ierīce_adrese[INDEX]) return;
            }
            for (int INDEX = 0; INDEX < 6; INDEX++) 찾은장치[INDEX] = 입력틀[22 + INDEX];
            찾은주소 = vienranga_VALUE;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(ražojums_kadrs, 14, 1); 넣기16(ražojums_kadrs, 16, 0x0800);
            ražojums_kadrs[18] = 6; ražojums_kadrs[19] = 4; 넣기16(ražojums_kadrs, 20, 2);
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                ražojums_kadrs[INDEX] = 입력틀[22 + INDEX]; ražojums_kadrs[32 + INDEX] = 입력틀[22 + INDEX];
                ražojums_kadrs[22 + INDEX] = tīkls_draiveris.ierīce_adrese[INDEX];
            }
            넣기32(ražojums_kadrs, 28, 내주소); 넣기32(ražojums_kadrs, 38, vienranga_VALUE);
            tīkls_draiveris.sūtīt(ražojums_kadrs, 42);
        }
    }

    static void Process_kadrs(int 길이) {
        if (길이 < 14 || 길이 > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, apraide_VALUE = true;
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            if (입력틀[INDEX] != tīkls_draiveris.ierīce_adrese[INDEX]) 자기 = false;
            if (입력틀[INDEX] != 255) apraide_VALUE = false;
        }
        if (!자기 && !apraide_VALUE) return;
        if (vesels_skaitlis_16(입력틀, 12) == 0x0806) { Process_adrese(길이); return; }
        if (vesels_skaitlis_16(입력틀, 12) != 0x0800) return;
        if (길이 < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int 머리길이 = (입력틀[14] & 15) * 4, 전체길이 = vesels_skaitlis_16(입력틀, 16);
        if (머리길이 < 20 || 머리길이 > 60 || 전체길이 < 머리길이 + 8 || 전체길이 > 길이 - 14
            || (vesels_skaitlis_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || vesels_skaitlis_32(입력틀, 30) != 내주소 || SUM_VALUE(입력틀, 14, 머리길이, 0) != 65535) { 폐기수++; return; }
        int Palaist = 14 + 머리길이, 자료길이 = vesels_skaitlis_16(입력틀, Palaist + 4);
        if (자료길이 < 8 || 자료길이 != 전체길이 - 머리길이 || 자료길이 > 1032) { 폐기수++; return; }
        int 출발 = vesels_skaitlis_32(입력틀, 26);
        if (vesels_skaitlis_16(입력틀, Palaist + 6) != 0 && SUM_VALUE(입력틀, Palaist, 자료길이, 가상머리합(출발, 내주소, 자료길이)) != 65535) {
            폐기수++; return;
        }
        int mērķis_VALUE = vesels_skaitlis_16(입력틀, Palaist + 2);
        for (int 칸 = 0; 칸 < 4; 칸++) if (접속번호들[칸] != 0 && 접속번호들[칸] == mērķis_VALUE) {
            if (받은길이[칸] >= 0) { 폐기수++; return; }
            받은길이[칸] = 자료길이 - 8; RECEIVED_adrese[칸] = 출발; RECEIVED_porta_numurs[칸] = vesels_skaitlis_16(입력틀, Palaist);
            for (int INDEX = 0; INDEX < 자료길이 - 8; INDEX++) RECEIVED_dati[칸 * 1024 + INDEX] = 입력틀[Palaist + 8 + INDEX];
            return;
        }
    }

    static void verificēt() {
        for (int INDEX = 0; INDEX < 16; INDEX++) {
            int 길이 = tīkls_draiveris.saņemt(입력틀);
            if (길이 == 0) return;
            Process_kadrs(길이);
        }
    }
    static int FIND_adrese(int adrese) {
        if (adrese == 0 || adrese == -1 || (adrese >>> 28) >= 14 || (adrese >>> 24) == 127 || adrese == 내주소) return -101;
        int Tālāk_krājums = (adrese & tīkls_maska) == (내주소 & tīkls_maska) ? adrese : vārteja_VALUE;
        if (Tālāk_krājums == 찾은주소) return 0;
        찾을주소 = Tālāk_krājums;
        int Palaist = ierīce_VALUE.밀리초(), Tālāk_pieprasījums = Palaist;
        while (ierīce_VALUE.밀리초() - Palaist < 1000) {
            if (ierīce_VALUE.밀리초() - Tālāk_pieprasījums >= 0) { pieprasījums_adrese(Tālāk_krājums); Tālāk_pieprasījums += 300; }
            verificēt();
            if (찾은주소 == Tālāk_krājums) return 0;
            ierīce_VALUE.잠시양보();
        }
        return -110;
    }
    static int sūtīt(int turis_VALUE, int adrese, int porta_numurs, int[] dati, int 길이) {
        int 칸 = INDEX(turis_VALUE);
        if (칸 < 0) return -9;
        if (tīkls_draiveris.입출력기준주소 == 0) return -19;
        if (porta_numurs < 1 || porta_numurs > 65535 || 길이 < 0 || 길이 > 1024) return -22;
        int mērs = FIND_adrese(adrese);
        if (mērs < 0) return mērs;
        바깥머리(0x0800, false);
        ražojums_kadrs[14] = 0x45; ražojums_kadrs[15] = 0; 넣기16(ražojums_kadrs, 16, 28 + 길이);
        넣기16(ražojums_kadrs, 18, identifikators_VALUE++); 넣기16(ražojums_kadrs, 20, 0x4000);
        ražojums_kadrs[22] = 64; ražojums_kadrs[23] = 17; 넣기16(ražojums_kadrs, 24, 0);
        넣기32(ražojums_kadrs, 26, 내주소); 넣기32(ražojums_kadrs, 30, adrese);
        넣기16(ražojums_kadrs, 24, ~SUM_VALUE(ražojums_kadrs, 14, 20, 0));
        넣기16(ražojums_kadrs, 34, 접속번호들[칸]); 넣기16(ražojums_kadrs, 36, porta_numurs);
        넣기16(ražojums_kadrs, 38, 길이 + 8); 넣기16(ražojums_kadrs, 40, 0);
        for (int INDEX = 0; INDEX < 길이; INDEX++) ražojums_kadrs[42 + INDEX] = dati[INDEX] & 255;
        int kontrolsumma = (~SUM_VALUE(ražojums_kadrs, 34, 길이 + 8, 가상머리합(내주소, adrese, 길이 + 8))) & 65535;
        넣기16(ražojums_kadrs, 40, kontrolsumma == 0 ? 65535 : kontrolsumma);
        mērs = tīkls_draiveris.sūtīt(ražojums_kadrs, 길이 + 42);
        return mērs < 0 ? mērs : 길이;
    }
    static int saņemt(int turis_VALUE, int[] dati, int noslodze_VALUE, int 제한) {
        int 칸 = INDEX(turis_VALUE);
        if (칸 < 0) return -9;
        int Palaist = ierīce_VALUE.밀리초();
        while (true) {
            verificēt();
            int 길이 = 받은길이[칸];
            if (길이 >= 0) {
                받은길이[칸] = -1;
                if (길이 > noslodze_VALUE) return -90;
                for (int INDEX = 0; INDEX < 길이; INDEX++) dati[INDEX] = RECEIVED_dati[칸 * 1024 + INDEX];
                return 길이;
            }
            if (제한 == 0) return -11;
            if (ierīce_VALUE.밀리초() - Palaist >= 제한) return -110;
            ierīce_VALUE.잠시양보();
        }
    }
    static void Statuss_VALUE() {
        SMS_Terminālis.Rakstīt(tīkls_draiveris.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Terminālis.Rakstīt("TX: "); SMS_Terminālis.rakstīšana_numurs(tīkls_draiveris.송신수);
        SMS_Terminālis.Rakstīt(" RX: "); SMS_Terminālis.rakstīšana_numurs(tīkls_draiveris.saņemt_COUNT);
        SMS_Terminālis.Rakstīt(" DROP: "); SMS_Terminālis.rakstīšana_numurs(폐기수);
        SMS_Terminālis.Rakstīt("\n");
    }
}
