// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 읽기 전용 gnìomhaich_àithne 묶음의 ELF32 dearbh_5fb2b747, 인수 sìn_air_adhart_VALUE_24592b8a, 한 번에 한 cleachdaiche Pròiseas_VALUE gnìomhaich_àithne. */
public final class 실행관리 {
    static final int Start_cleachdaiche_ap = 0x04000000;
    static final int cleachdaiche_crìochnaich = 0x04400000;
    static final int IMAGE_crìochnaich_ADDRESS = 0x04200000;
    static final int argamaid_Start = 0x04300000;
    static int argamaid_COUNT = 0;
    static int[] argamaid_ADDRESS = new int[16];

    static boolean cliop(int ADDRESS, int faid_VALUE) {
        return ADDRESS >= Start_cleachdaiche_ap && ADDRESS < cleachdaiche_crìochnaich && faid_VALUE >= 0 && faid_VALUE <= cleachdaiche_crìochnaich - ADDRESS;
    }

    static int 수(int ADDRESS) { return 기억공간.정수읽기(ADDRESS); }
    static int 짧은수(int ADDRESS) { return uidheam_VALUE.기억읽기(ADDRESS) | uidheam_VALUE.기억읽기(ADDRESS + 1) << 8; }
    static void 수쓰기(int ADDRESS, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) uidheam_VALUE.sgrìobh_cuimhne(ADDRESS + INDEX, VALUE >>> (INDEX * 8));
    }

    static int buidheann_COUNT() {
        int ADDRESS = uidheam_VALUE.실행묶음();
        int atharraich_am_meud = uidheam_VALUE.실행묶음크기();
        if (atharraich_am_meud < 8 || 수(ADDRESS) != 0x50414b4a) return 0;
        int nì_COUNT = 수(ADDRESS + 4);
        return nì_COUNT >= 0 && nì_COUNT <= 32 && nì_COUNT <= (atharraich_am_meud - 8) / 24 ? nì_COUNT : 0;
    }

    static void cur_a_steach_Liosta() {
        for (int INDEX = 0; INDEX < buidheann_COUNT(); INDEX++) {
            int cur_a_steach_VALUE = uidheam_VALUE.실행묶음() + 8 + INDEX * 24;
            for (int caractar_VALUE = 0; caractar_VALUE < 16 && uidheam_VALUE.기억읽기(cur_a_steach_VALUE + caractar_VALUE) != 0; caractar_VALUE++)
                SMS_tèirmineal.문자(uidheam_VALUE.기억읽기(cur_a_steach_VALUE + caractar_VALUE));
            SMS_tèirmineal.sgrìobh("\n");
        }
    }

    static int FIND_cur_a_steach(int[] 입력, int ruith, int faid_VALUE) {
        if (faid_VALUE <= 0 || faid_VALUE >= 16) return 0;
        for (int INDEX = 0; INDEX < buidheann_COUNT(); INDEX++) {
            int cur_a_steach_VALUE = uidheam_VALUE.실행묶음() + 8 + INDEX * 24;
            boolean 같음 = uidheam_VALUE.기억읽기(cur_a_steach_VALUE + faid_VALUE) == 0;
            for (int caractar_VALUE = 0; caractar_VALUE < faid_VALUE; caractar_VALUE++)
                if (입력[ruith + caractar_VALUE] != uidheam_VALUE.기억읽기(cur_a_steach_VALUE + caractar_VALUE)) 같음 = false;
            if (같음) return cur_a_steach_VALUE;
        }
        return 0;
    }

    static int dearbh_5fb2b747(int faidhle, int faid_VALUE) {
        if (faid_VALUE < 52 || 수(faidhle) != 0x464c457f || uidheam_VALUE.기억읽기(faidhle + 4) != 1
            || uidheam_VALUE.기억읽기(faidhle + 5) != 1 || uidheam_VALUE.기억읽기(faidhle + 6) != 1
            || 짧은수(faidhle + 16) != 2 || 짧은수(faidhle + 18) != 3 || 수(faidhle + 20) != 1
            || 짧은수(faidhle + 40) != 52 || 짧은수(faidhle + 42) != 32) return -8;
        int cur_a_steach_puing_VALUE = 수(faidhle + 24);
        int clàr_suidhich = 수(faidhle + 28);
        int nì_COUNT = 짧은수(faidhle + 44);
        if (nì_COUNT == 0 || nì_COUNT > 16 || clàr_suidhich < 52 || clàr_suidhich > faid_VALUE - nì_COUNT * 32) return -8;
        boolean 실행가능 = false;
        for (int INDEX = 0; INDEX < nì_COUNT; INDEX++) {
            int LOOKUP_clàr = faidhle + clàr_suidhich + INDEX * 32;
            int 종류 = 수(LOOKUP_clàr);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 CONNECT/해석기 미지원
            if (종류 != 1) continue;
            int suidhich = 수(LOOKUP_clàr + 4), ADDRESS = 수(LOOKUP_clàr + 8), faidhle_atharraich_am_meud = 수(LOOKUP_clàr + 16), cuimhne_atharraich_am_meud = 수(LOOKUP_clàr + 20);
            int co_thaobhaich_VALUE = 수(LOOKUP_clàr + 28);
            if (ADDRESS < Start_cleachdaiche_ap || ADDRESS >= IMAGE_crìochnaich_ADDRESS || cuimhne_atharraich_am_meud < 0 || cuimhne_atharraich_am_meud > IMAGE_crìochnaich_ADDRESS - ADDRESS
                || faidhle_atharraich_am_meud < 0 || faidhle_atharraich_am_meud > cuimhne_atharraich_am_meud || suidhich < 0 || (faidhle_atharraich_am_meud > 0 && suidhich > faid_VALUE - faidhle_atharraich_am_meud)
                || (co_thaobhaich_VALUE != 0 && (co_thaobhaich_VALUE < 0 || (co_thaobhaich_VALUE & (co_thaobhaich_VALUE - 1)) != 0
                    || ((ADDRESS - suidhich) & (co_thaobhaich_VALUE - 1)) != 0))) return -8;
            for (int 앞 = 0; 앞 < INDEX; 앞++) {
                int 이전 = faidhle + clàr_suidhich + 앞 * 32;
                if (수(이전) == 1 && cuimhne_atharraich_am_meud > 0 && 수(이전 + 20) > 0
                    && ADDRESS < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < ADDRESS + cuimhne_atharraich_am_meud) return -8;
            }
            if ((수(LOOKUP_clàr + 24) & 1) != 0 && cur_a_steach_puing_VALUE >= ADDRESS && cur_a_steach_puing_VALUE - ADDRESS < faidhle_atharraich_am_meud) 실행가능 = true;
        }
        return 실행가능 ? cur_a_steach_puing_VALUE : -8;
    }

    static int gnìomhaich_àithne(int[] 입력, int ruith, int faid_VALUE) {
        while (ruith < faid_VALUE && 입력[ruith] == ' ') ruith++;
        int 끝 = ruith;
        while (끝 < faid_VALUE && 입력[끝] != ' ') 끝++;
        int cur_a_steach_VALUE = FIND_cur_a_steach(입력, ruith, 끝 - ruith);
        if (cur_a_steach_VALUE == 0) return -2;
        int suidhich = 수(cur_a_steach_VALUE + 16), atharraich_am_meud = 수(cur_a_steach_VALUE + 20);
        if (suidhich < 8 + buidheann_COUNT() * 24 || atharraich_am_meud < 52 || suidhich > uidheam_VALUE.실행묶음크기() - atharraich_am_meud) return -8;
        int faidhle = uidheam_VALUE.실행묶음() + suidhich;
        int cur_a_steach_puing_VALUE = dearbh_5fb2b747(faidhle, atharraich_am_meud);
        if (cur_a_steach_puing_VALUE < 0) return cur_a_steach_puing_VALUE;
        uidheam_VALUE.cleachdaiche_glan_susbaint();
        int clàr_suidhich = 수(faidhle + 28), nì_COUNT = 짧은수(faidhle + 44);
        for (int INDEX = 0; INDEX < nì_COUNT; INDEX++) {
            int LOOKUP_clàr = faidhle + clàr_suidhich + INDEX * 32;
            if (수(LOOKUP_clàr) != 1) continue;
            int 원본 = faidhle + 수(LOOKUP_clàr + 4), ceann_uidhe_VALUE = 수(LOOKUP_clàr + 8), faidhle_atharraich_am_meud = 수(LOOKUP_clàr + 16);
            for (int baidht_VALUE = 0; baidht_VALUE < faidhle_atharraich_am_meud; baidht_VALUE++) uidheam_VALUE.sgrìobh_cuimhne(ceann_uidhe_VALUE + baidht_VALUE, uidheam_VALUE.기억읽기(원본 + baidht_VALUE));
        }
        argamaid_COUNT = 0;
        int Store_VALUE = argamaid_Start;
        while (끝 < faid_VALUE) {
            while (끝 < faid_VALUE && 입력[끝] == ' ') 끝++;
            if (끝 == faid_VALUE) break;
            if (argamaid_COUNT == argamaid_ADDRESS.length) return -22;
            ruith = 끝;
            while (끝 < faid_VALUE && 입력[끝] != ' ') 끝++;
            argamaid_ADDRESS[argamaid_COUNT++] = Store_VALUE;
            수쓰기(Store_VALUE, 끝 - ruith);
            for (int caractar_VALUE = ruith; caractar_VALUE < 끝; caractar_VALUE++) 수쓰기(Store_VALUE + 4 + (caractar_VALUE - ruith) * 4, 입력[caractar_VALUE]);
            Store_VALUE += 4 + (끝 - ruith) * 4;
        }
        lìonra_stac.CLEAN_Pròiseas();
        파일서술자관리.Start_Pròiseas();
        int tomhas = uidheam_VALUE.ruith_cleachdaiche_ap(cur_a_steach_puing_VALUE, cleachdaiche_crìochnaich - 16);
        파일서술자관리.CLEAN_Pròiseas();
        lìonra_stac.CLEAN_Pròiseas();
        return tomhas;
    }
}
