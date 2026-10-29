// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Darllen 전용 Gweithredu_gorchymyn 묶음의 ELF32 dilysu_5fb2b747, 인수 Ymlaen_VALUE, 한 번에 한 defnyddiwr Proses_VALUE Gweithredu_gorchymyn. */
public final class 실행관리 {
    static final int START_defnyddiwr_Rhaglen = 0x04000000;
    static final int defnyddiwr_gorffen = 0x04400000;
    static final int llun_gorffen_ADDRESS = 0x04200000;
    static final int arg_START = 0x04300000;
    static int arg_COUNT = 0;
    static int[] arg_ADDRESS = new int[16];

    static boolean clip(int ADDRESS, int hyd_VALUE) {
        return ADDRESS >= START_defnyddiwr_Rhaglen && ADDRESS < defnyddiwr_gorffen && hyd_VALUE >= 0 && hyd_VALUE <= defnyddiwr_gorffen - ADDRESS;
    }

    static int 수(int ADDRESS) { return 기억공간.dosrannu_cyfanrif(ADDRESS); }
    static int 짧은수(int ADDRESS) { return dyfais_VALUE.기억읽기(ADDRESS) | dyfais_VALUE.기억읽기(ADDRESS + 1) << 8; }
    static void 수쓰기(int ADDRESS, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) dyfais_VALUE.ysgrifennu_Cof(ADDRESS + INDEX, VALUE >>> (INDEX * 8));
    }

    static int Grŵp_COUNT() {
        int ADDRESS = dyfais_VALUE.실행묶음();
        int Maint = dyfais_VALUE.실행묶음크기();
        if (Maint < 8 || 수(ADDRESS) != 0x50414b4a) return 0;
        int eitem_COUNT = 수(ADDRESS + 4);
        return eitem_COUNT >= 0 && eitem_COUNT <= 32 && eitem_COUNT <= (Maint - 8) / 24 ? eitem_COUNT : 0;
    }

    static void cofnod_Rhestr() {
        for (int INDEX = 0; INDEX < Grŵp_COUNT(); INDEX++) {
            int cofnod_VALUE = dyfais_VALUE.실행묶음() + 8 + INDEX * 24;
            for (int nod_VALUE = 0; nod_VALUE < 16 && dyfais_VALUE.기억읽기(cofnod_VALUE + nod_VALUE) != 0; nod_VALUE++)
                SMS_Terfynell.문자(dyfais_VALUE.기억읽기(cofnod_VALUE + nod_VALUE));
            SMS_Terfynell.Ysgrifennu("\n");
        }
    }

    static int FIND_cofnod(int[] 입력, int Gweithredu_2, int hyd_VALUE) {
        if (hyd_VALUE <= 0 || hyd_VALUE >= 16) return 0;
        for (int INDEX = 0; INDEX < Grŵp_COUNT(); INDEX++) {
            int cofnod_VALUE = dyfais_VALUE.실행묶음() + 8 + INDEX * 24;
            boolean 같음 = dyfais_VALUE.기억읽기(cofnod_VALUE + hyd_VALUE) == 0;
            for (int nod_VALUE = 0; nod_VALUE < hyd_VALUE; nod_VALUE++)
                if (입력[Gweithredu_2 + nod_VALUE] != dyfais_VALUE.기억읽기(cofnod_VALUE + nod_VALUE)) 같음 = false;
            if (같음) return cofnod_VALUE;
        }
        return 0;
    }

    static int dilysu_5fb2b747(int Ffeil, int hyd_VALUE) {
        if (hyd_VALUE < 52 || 수(Ffeil) != 0x464c457f || dyfais_VALUE.기억읽기(Ffeil + 4) != 1
            || dyfais_VALUE.기억읽기(Ffeil + 5) != 1 || dyfais_VALUE.기억읽기(Ffeil + 6) != 1
            || 짧은수(Ffeil + 16) != 2 || 짧은수(Ffeil + 18) != 3 || 수(Ffeil + 20) != 1
            || 짧은수(Ffeil + 40) != 52 || 짧은수(Ffeil + 42) != 32) return -8;
        int cofnod_p_VALUE = 수(Ffeil + 24);
        int tabl_safle = 수(Ffeil + 28);
        int eitem_COUNT = 짧은수(Ffeil + 44);
        if (eitem_COUNT == 0 || eitem_COUNT > 16 || tabl_safle < 52 || tabl_safle > hyd_VALUE - eitem_COUNT * 32) return -8;
        boolean 실행가능 = false;
        for (int INDEX = 0; INDEX < eitem_COUNT; INDEX++) {
            int LOOKUP_tabl = Ffeil + tabl_safle + INDEX * 32;
            int 종류 = 수(LOOKUP_tabl);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Cysylltu/해석기 미지원
            if (종류 != 1) continue;
            int safle = 수(LOOKUP_tabl + 4), ADDRESS = 수(LOOKUP_tabl + 8), ffeil_newid_maint = 수(LOOKUP_tabl + 16), Cof_newid_maint = 수(LOOKUP_tabl + 20);
            int alinio_VALUE = 수(LOOKUP_tabl + 28);
            if (ADDRESS < START_defnyddiwr_Rhaglen || ADDRESS >= llun_gorffen_ADDRESS || Cof_newid_maint < 0 || Cof_newid_maint > llun_gorffen_ADDRESS - ADDRESS
                || ffeil_newid_maint < 0 || ffeil_newid_maint > Cof_newid_maint || safle < 0 || (ffeil_newid_maint > 0 && safle > hyd_VALUE - ffeil_newid_maint)
                || (alinio_VALUE != 0 && (alinio_VALUE < 0 || (alinio_VALUE & (alinio_VALUE - 1)) != 0
                    || ((ADDRESS - safle) & (alinio_VALUE - 1)) != 0))) return -8;
            for (int 앞 = 0; 앞 < INDEX; 앞++) {
                int 이전 = Ffeil + tabl_safle + 앞 * 32;
                if (수(이전) == 1 && Cof_newid_maint > 0 && 수(이전 + 20) > 0
                    && ADDRESS < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < ADDRESS + Cof_newid_maint) return -8;
            }
            if ((수(LOOKUP_tabl + 24) & 1) != 0 && cofnod_p_VALUE >= ADDRESS && cofnod_p_VALUE - ADDRESS < ffeil_newid_maint) 실행가능 = true;
        }
        return 실행가능 ? cofnod_p_VALUE : -8;
    }

    static int Gweithredu_gorchymyn(int[] 입력, int Gweithredu_2, int hyd_VALUE) {
        while (Gweithredu_2 < hyd_VALUE && 입력[Gweithredu_2] == ' ') Gweithredu_2++;
        int 끝 = Gweithredu_2;
        while (끝 < hyd_VALUE && 입력[끝] != ' ') 끝++;
        int cofnod_VALUE = FIND_cofnod(입력, Gweithredu_2, 끝 - Gweithredu_2);
        if (cofnod_VALUE == 0) return -2;
        int safle = 수(cofnod_VALUE + 16), Maint = 수(cofnod_VALUE + 20);
        if (safle < 8 + Grŵp_COUNT() * 24 || Maint < 52 || safle > dyfais_VALUE.실행묶음크기() - Maint) return -8;
        int Ffeil = dyfais_VALUE.실행묶음() + safle;
        int cofnod_p_VALUE = dilysu_5fb2b747(Ffeil, Maint);
        if (cofnod_p_VALUE < 0) return cofnod_p_VALUE;
        dyfais_VALUE.defnyddiwr_clirio_Cynnwys();
        int tabl_safle = 수(Ffeil + 28), eitem_COUNT = 짧은수(Ffeil + 44);
        for (int INDEX = 0; INDEX < eitem_COUNT; INDEX++) {
            int LOOKUP_tabl = Ffeil + tabl_safle + INDEX * 32;
            if (수(LOOKUP_tabl) != 1) continue;
            int 원본 = Ffeil + 수(LOOKUP_tabl + 4), cyrchfan_VALUE = 수(LOOKUP_tabl + 8), ffeil_newid_maint = 수(LOOKUP_tabl + 16);
            for (int beit_VALUE = 0; beit_VALUE < ffeil_newid_maint; beit_VALUE++) dyfais_VALUE.ysgrifennu_Cof(cyrchfan_VALUE + beit_VALUE, dyfais_VALUE.기억읽기(원본 + beit_VALUE));
        }
        arg_COUNT = 0;
        int Store_VALUE = arg_START;
        while (끝 < hyd_VALUE) {
            while (끝 < hyd_VALUE && 입력[끝] == ' ') 끝++;
            if (끝 == hyd_VALUE) break;
            if (arg_COUNT == arg_ADDRESS.length) return -22;
            Gweithredu_2 = 끝;
            while (끝 < hyd_VALUE && 입력[끝] != ' ') 끝++;
            arg_ADDRESS[arg_COUNT++] = Store_VALUE;
            수쓰기(Store_VALUE, 끝 - Gweithredu_2);
            for (int nod_VALUE = Gweithredu_2; nod_VALUE < 끝; nod_VALUE++) 수쓰기(Store_VALUE + 4 + (nod_VALUE - Gweithredu_2) * 4, 입력[nod_VALUE]);
            Store_VALUE += 4 + (끝 - Gweithredu_2) * 4;
        }
        Rhwydwaith_pentwr.Glân_Proses();
        파일서술자관리.START_Proses();
        int mesur = dyfais_VALUE.rhedeg_defnyddiwr_Rhaglen(cofnod_p_VALUE, defnyddiwr_gorffen - 16);
        파일서술자관리.Glân_Proses();
        Rhwydwaith_pentwr.Glân_Proses();
        return mesur;
    }
}
