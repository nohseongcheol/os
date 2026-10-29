// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Léigh 전용 Rith_ordú 묶음의 ELF32 bailíochtaigh, Argóintí Ar_aghaidh_VALUE, 한 번에 한 úsáideoir Próiseas_VALUE Rith_ordú. */
public final class 실행관리 {
    static final int Start_úsáideoir_clár = 0x04000000;
    static final int úsáideoir_cuir_deireadh_le = 0x04400000;
    static final int IMAGE_cuir_deireadh_le_ADDRESS = 0x04200000;
    static final int argóint_Start = 0x04300000;
    static int argóint_COUNT = 0;
    static int[] argóint_ADDRESS = new int[16];

    static boolean gearrthóg(int ADDRESS, int fad_VALUE) {
        return ADDRESS >= Start_úsáideoir_clár && ADDRESS < úsáideoir_cuir_deireadh_le && fad_VALUE >= 0 && fad_VALUE <= úsáideoir_cuir_deireadh_le - ADDRESS;
    }

    static int 수(int ADDRESS) { return 기억공간.parsáil_slánuimhir(ADDRESS); }
    static int 짧은수(int ADDRESS) { return gléas_VALUE.기억읽기(ADDRESS) | gléas_VALUE.기억읽기(ADDRESS + 1) << 8; }
    static void 수쓰기(int ADDRESS, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) gléas_VALUE.scríobh_Cuimhne(ADDRESS + INDEX, VALUE >>> (INDEX * 8));
    }

    static int Grúpa_COUNT() {
        int ADDRESS = gléas_VALUE.실행묶음();
        int Méid = gléas_VALUE.실행묶음크기();
        if (Méid < 8 || 수(ADDRESS) != 0x50414b4a) return 0;
        int mír_COUNT = 수(ADDRESS + 4);
        return mír_COUNT >= 0 && mír_COUNT <= 32 && mír_COUNT <= (Méid - 8) / 24 ? mír_COUNT : 0;
    }

    static void iontráil_Liosta() {
        for (int INDEX = 0; INDEX < Grúpa_COUNT(); INDEX++) {
            int iontráil_VALUE = gléas_VALUE.실행묶음() + 8 + INDEX * 24;
            for (int carachtar_VALUE = 0; carachtar_VALUE < 16 && gléas_VALUE.기억읽기(iontráil_VALUE + carachtar_VALUE) != 0; carachtar_VALUE++)
                SMS_Teirminéal.문자(gléas_VALUE.기억읽기(iontráil_VALUE + carachtar_VALUE));
            SMS_Teirminéal.Scríobh("\n");
        }
    }

    static int FIND_iontráil(int[] 입력, int Rith_2, int fad_VALUE) {
        if (fad_VALUE <= 0 || fad_VALUE >= 16) return 0;
        for (int INDEX = 0; INDEX < Grúpa_COUNT(); INDEX++) {
            int iontráil_VALUE = gléas_VALUE.실행묶음() + 8 + INDEX * 24;
            boolean 같음 = gléas_VALUE.기억읽기(iontráil_VALUE + fad_VALUE) == 0;
            for (int carachtar_VALUE = 0; carachtar_VALUE < fad_VALUE; carachtar_VALUE++)
                if (입력[Rith_2 + carachtar_VALUE] != gléas_VALUE.기억읽기(iontráil_VALUE + carachtar_VALUE)) 같음 = false;
            if (같음) return iontráil_VALUE;
        }
        return 0;
    }

    static int bailíochtaigh(int Comhad, int fad_VALUE) {
        if (fad_VALUE < 52 || 수(Comhad) != 0x464c457f || gléas_VALUE.기억읽기(Comhad + 4) != 1
            || gléas_VALUE.기억읽기(Comhad + 5) != 1 || gléas_VALUE.기억읽기(Comhad + 6) != 1
            || 짧은수(Comhad + 16) != 2 || 짧은수(Comhad + 18) != 3 || 수(Comhad + 20) != 1
            || 짧은수(Comhad + 40) != 52 || 짧은수(Comhad + 42) != 32) return -8;
        int iontráil_pointe_VALUE = 수(Comhad + 24);
        int tábla_suíomh = 수(Comhad + 28);
        int mír_COUNT = 짧은수(Comhad + 44);
        if (mír_COUNT == 0 || mír_COUNT > 16 || tábla_suíomh < 52 || tábla_suíomh > fad_VALUE - mír_COUNT * 32) return -8;
        boolean 실행가능 = false;
        for (int INDEX = 0; INDEX < mír_COUNT; INDEX++) {
            int LOOKUP_tábla = Comhad + tábla_suíomh + INDEX * 32;
            int 종류 = 수(LOOKUP_tábla);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Nasc/해석기 미지원
            if (종류 != 1) continue;
            int suíomh = 수(LOOKUP_tábla + 4), ADDRESS = 수(LOOKUP_tábla + 8), comhad_socraigh_méid = 수(LOOKUP_tábla + 16), Cuimhne_socraigh_méid = 수(LOOKUP_tábla + 20);
            int ailínigh_VALUE = 수(LOOKUP_tábla + 28);
            if (ADDRESS < Start_úsáideoir_clár || ADDRESS >= IMAGE_cuir_deireadh_le_ADDRESS || Cuimhne_socraigh_méid < 0 || Cuimhne_socraigh_méid > IMAGE_cuir_deireadh_le_ADDRESS - ADDRESS
                || comhad_socraigh_méid < 0 || comhad_socraigh_méid > Cuimhne_socraigh_méid || suíomh < 0 || (comhad_socraigh_méid > 0 && suíomh > fad_VALUE - comhad_socraigh_méid)
                || (ailínigh_VALUE != 0 && (ailínigh_VALUE < 0 || (ailínigh_VALUE & (ailínigh_VALUE - 1)) != 0
                    || ((ADDRESS - suíomh) & (ailínigh_VALUE - 1)) != 0))) return -8;
            for (int 앞 = 0; 앞 < INDEX; 앞++) {
                int 이전 = Comhad + tábla_suíomh + 앞 * 32;
                if (수(이전) == 1 && Cuimhne_socraigh_méid > 0 && 수(이전 + 20) > 0
                    && ADDRESS < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < ADDRESS + Cuimhne_socraigh_méid) return -8;
            }
            if ((수(LOOKUP_tábla + 24) & 1) != 0 && iontráil_pointe_VALUE >= ADDRESS && iontráil_pointe_VALUE - ADDRESS < comhad_socraigh_méid) 실행가능 = true;
        }
        return 실행가능 ? iontráil_pointe_VALUE : -8;
    }

    static int Rith_ordú(int[] 입력, int Rith_2, int fad_VALUE) {
        while (Rith_2 < fad_VALUE && 입력[Rith_2] == ' ') Rith_2++;
        int 끝 = Rith_2;
        while (끝 < fad_VALUE && 입력[끝] != ' ') 끝++;
        int iontráil_VALUE = FIND_iontráil(입력, Rith_2, 끝 - Rith_2);
        if (iontráil_VALUE == 0) return -2;
        int suíomh = 수(iontráil_VALUE + 16), Méid = 수(iontráil_VALUE + 20);
        if (suíomh < 8 + Grúpa_COUNT() * 24 || Méid < 52 || suíomh > gléas_VALUE.실행묶음크기() - Méid) return -8;
        int Comhad = gléas_VALUE.실행묶음() + suíomh;
        int iontráil_pointe_VALUE = bailíochtaigh(Comhad, Méid);
        if (iontráil_pointe_VALUE < 0) return iontráil_pointe_VALUE;
        gléas_VALUE.úsáideoir_glan_TOC();
        int tábla_suíomh = 수(Comhad + 28), mír_COUNT = 짧은수(Comhad + 44);
        for (int INDEX = 0; INDEX < mír_COUNT; INDEX++) {
            int LOOKUP_tábla = Comhad + tábla_suíomh + INDEX * 32;
            if (수(LOOKUP_tábla) != 1) continue;
            int 원본 = Comhad + 수(LOOKUP_tábla + 4), sprioc_VALUE = 수(LOOKUP_tábla + 8), comhad_socraigh_méid = 수(LOOKUP_tábla + 16);
            for (int beart_VALUE = 0; beart_VALUE < comhad_socraigh_méid; beart_VALUE++) gléas_VALUE.scríobh_Cuimhne(sprioc_VALUE + beart_VALUE, gléas_VALUE.기억읽기(원본 + beart_VALUE));
        }
        argóint_COUNT = 0;
        int Store_VALUE = argóint_Start;
        while (끝 < fad_VALUE) {
            while (끝 < fad_VALUE && 입력[끝] == ' ') 끝++;
            if (끝 == fad_VALUE) break;
            if (argóint_COUNT == argóint_ADDRESS.length) return -22;
            Rith_2 = 끝;
            while (끝 < fad_VALUE && 입력[끝] != ' ') 끝++;
            argóint_ADDRESS[argóint_COUNT++] = Store_VALUE;
            수쓰기(Store_VALUE, 끝 - Rith_2);
            for (int carachtar_VALUE = Rith_2; carachtar_VALUE < 끝; carachtar_VALUE++) 수쓰기(Store_VALUE + 4 + (carachtar_VALUE - Rith_2) * 4, 입력[carachtar_VALUE]);
            Store_VALUE += 4 + (끝 - Rith_2) * 4;
        }
        Líonra_Cruach.CLEAN_Próiseas();
        파일서술자관리.Start_Próiseas();
        int tomhas = gléas_VALUE.rith_úsáideoir_clár(iontráil_pointe_VALUE, úsáideoir_cuir_deireadh_le - 16);
        파일서술자관리.CLEAN_Próiseas();
        Líonra_Cruach.CLEAN_Próiseas();
        return tomhas;
    }
}
