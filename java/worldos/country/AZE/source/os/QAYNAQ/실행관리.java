// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Oxuma 전용 icra_etmək_əmr 묶음의 ELF32 təsdiqlə, 인수 irəli_VALUE, 한 번에 한 istifadəçi Proses_VALUE icra_etmək_əmr. */
public final class 실행관리 {
    static final int Başla_istifadəçi_proqram = 0x04000000;
    static final int istifadəçi_bitirmək = 0x04400000;
    static final int IMAGE_bitirmək_ünvan = 0x04200000;
    static final int arqument_Başla = 0x04300000;
    static int arqument_COUNT = 0;
    static int[] arqument_ünvan = new int[16];

    static boolean klip(int ünvan, int uzunluq_VALUE) {
        return ünvan >= Başla_istifadəçi_proqram && ünvan < istifadəçi_bitirmək && uzunluq_VALUE >= 0 && uzunluq_VALUE <= istifadəçi_bitirmək - ünvan;
    }

    static int 수(int ünvan) { return 기억공간.parselləmək_tam_ədəd(ünvan); }
    static int 짧은수(int ünvan) { return cihaz_VALUE.기억읽기(ünvan) | cihaz_VALUE.기억읽기(ünvan + 1) << 8; }
    static void 수쓰기(int ünvan, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) cihaz_VALUE.yazmaq_Yaddaş(ünvan + INDEX, VALUE >>> (INDEX * 8));
    }

    static int Qrup_COUNT() {
        int ünvan = cihaz_VALUE.실행묶음();
        int Böyüklük = cihaz_VALUE.실행묶음크기();
        if (Böyüklük < 8 || 수(ünvan) != 0x50414b4a) return 0;
        int element_COUNT = 수(ünvan + 4);
        return element_COUNT >= 0 && element_COUNT <= 32 && element_COUNT <= (Böyüklük - 8) / 24 ? element_COUNT : 0;
    }

    static void daxiletmə_Siyahı() {
        for (int INDEX = 0; INDEX < Qrup_COUNT(); INDEX++) {
            int daxiletmə_VALUE = cihaz_VALUE.실행묶음() + 8 + INDEX * 24;
            for (int simvol_VALUE_068c2631 = 0; simvol_VALUE_068c2631 < 16 && cihaz_VALUE.기억읽기(daxiletmə_VALUE + simvol_VALUE_068c2631) != 0; simvol_VALUE_068c2631++)
                SMS_Terminal.문자(cihaz_VALUE.기억읽기(daxiletmə_VALUE + simvol_VALUE_068c2631));
            SMS_Terminal.Yazma("\n");
        }
    }

    static int FIND_daxiletmə(int[] 입력, int İcra_Et, int uzunluq_VALUE) {
        if (uzunluq_VALUE <= 0 || uzunluq_VALUE >= 16) return 0;
        for (int INDEX = 0; INDEX < Qrup_COUNT(); INDEX++) {
            int daxiletmə_VALUE = cihaz_VALUE.실행묶음() + 8 + INDEX * 24;
            boolean 같음 = cihaz_VALUE.기억읽기(daxiletmə_VALUE + uzunluq_VALUE) == 0;
            for (int simvol_VALUE_068c2631 = 0; simvol_VALUE_068c2631 < uzunluq_VALUE; simvol_VALUE_068c2631++)
                if (입력[İcra_Et + simvol_VALUE_068c2631] != cihaz_VALUE.기억읽기(daxiletmə_VALUE + simvol_VALUE_068c2631)) 같음 = false;
            if (같음) return daxiletmə_VALUE;
        }
        return 0;
    }

    static int təsdiqlə(int FAYL, int uzunluq_VALUE) {
        if (uzunluq_VALUE < 52 || 수(FAYL) != 0x464c457f || cihaz_VALUE.기억읽기(FAYL + 4) != 1
            || cihaz_VALUE.기억읽기(FAYL + 5) != 1 || cihaz_VALUE.기억읽기(FAYL + 6) != 1
            || 짧은수(FAYL + 16) != 2 || 짧은수(FAYL + 18) != 3 || 수(FAYL + 20) != 1
            || 짧은수(FAYL + 40) != 52 || 짧은수(FAYL + 42) != 32) return -8;
        int daxiletmə_p_VALUE = 수(FAYL + 24);
        int cədvəl_yerinə_qoymaq = 수(FAYL + 28);
        int element_COUNT = 짧은수(FAYL + 44);
        if (element_COUNT == 0 || element_COUNT > 16 || cədvəl_yerinə_qoymaq < 52 || cədvəl_yerinə_qoymaq > uzunluq_VALUE - element_COUNT * 32) return -8;
        boolean 실행가능 = false;
        for (int INDEX = 0; INDEX < element_COUNT; INDEX++) {
            int LOOKUP_cədvəl = FAYL + cədvəl_yerinə_qoymaq + INDEX * 32;
            int 종류 = 수(LOOKUP_cədvəl);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Bağlan/parser_48ee4b1b 미지원
            if (종류 != 1) continue;
            int yerinə_qoymaq = 수(LOOKUP_cədvəl + 4), ünvan = 수(LOOKUP_cədvəl + 8), fayl_ölçünü_dəyişmək = 수(LOOKUP_cədvəl + 16), Yaddaş_ölçünü_dəyişmək = 수(LOOKUP_cədvəl + 20);
            int düzləndirmək_VALUE = 수(LOOKUP_cədvəl + 28);
            if (ünvan < Başla_istifadəçi_proqram || ünvan >= IMAGE_bitirmək_ünvan || Yaddaş_ölçünü_dəyişmək < 0 || Yaddaş_ölçünü_dəyişmək > IMAGE_bitirmək_ünvan - ünvan
                || fayl_ölçünü_dəyişmək < 0 || fayl_ölçünü_dəyişmək > Yaddaş_ölçünü_dəyişmək || yerinə_qoymaq < 0 || (fayl_ölçünü_dəyişmək > 0 && yerinə_qoymaq > uzunluq_VALUE - fayl_ölçünü_dəyişmək)
                || (düzləndirmək_VALUE != 0 && (düzləndirmək_VALUE < 0 || (düzləndirmək_VALUE & (düzləndirmək_VALUE - 1)) != 0
                    || ((ünvan - yerinə_qoymaq) & (düzləndirmək_VALUE - 1)) != 0))) return -8;
            for (int ön_VALUE = 0; ön_VALUE < INDEX; ön_VALUE++) {
                int 이전 = FAYL + cədvəl_yerinə_qoymaq + ön_VALUE * 32;
                if (수(이전) == 1 && Yaddaş_ölçünü_dəyişmək > 0 && 수(이전 + 20) > 0
                    && ünvan < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < ünvan + Yaddaş_ölçünü_dəyişmək) return -8;
            }
            if ((수(LOOKUP_cədvəl + 24) & 1) != 0 && daxiletmə_p_VALUE >= ünvan && daxiletmə_p_VALUE - ünvan < fayl_ölçünü_dəyişmək) 실행가능 = true;
        }
        return 실행가능 ? daxiletmə_p_VALUE : -8;
    }

    static int icra_etmək_əmr(int[] 입력, int İcra_Et, int uzunluq_VALUE) {
        while (İcra_Et < uzunluq_VALUE && 입력[İcra_Et] == ' ') İcra_Et++;
        int 끝 = İcra_Et;
        while (끝 < uzunluq_VALUE && 입력[끝] != ' ') 끝++;
        int daxiletmə_VALUE = FIND_daxiletmə(입력, İcra_Et, 끝 - İcra_Et);
        if (daxiletmə_VALUE == 0) return -2;
        int yerinə_qoymaq = 수(daxiletmə_VALUE + 16), Böyüklük = 수(daxiletmə_VALUE + 20);
        if (yerinə_qoymaq < 8 + Qrup_COUNT() * 24 || Böyüklük < 52 || yerinə_qoymaq > cihaz_VALUE.실행묶음크기() - Böyüklük) return -8;
        int FAYL = cihaz_VALUE.실행묶음() + yerinə_qoymaq;
        int daxiletmə_p_VALUE = təsdiqlə(FAYL, Böyüklük);
        if (daxiletmə_p_VALUE < 0) return daxiletmə_p_VALUE;
        cihaz_VALUE.istifadəçi_təmizləmək_TOC();
        int cədvəl_yerinə_qoymaq = 수(FAYL + 28), element_COUNT = 짧은수(FAYL + 44);
        for (int INDEX = 0; INDEX < element_COUNT; INDEX++) {
            int LOOKUP_cədvəl = FAYL + cədvəl_yerinə_qoymaq + INDEX * 32;
            if (수(LOOKUP_cədvəl) != 1) continue;
            int 원본 = FAYL + 수(LOOKUP_cədvəl + 4), təyinat_VALUE_a0fbc067 = 수(LOOKUP_cədvəl + 8), fayl_ölçünü_dəyişmək = 수(LOOKUP_cədvəl + 16);
            for (int bayt_VALUE = 0; bayt_VALUE < fayl_ölçünü_dəyişmək; bayt_VALUE++) cihaz_VALUE.yazmaq_Yaddaş(təyinat_VALUE_a0fbc067 + bayt_VALUE, cihaz_VALUE.기억읽기(원본 + bayt_VALUE));
        }
        arqument_COUNT = 0;
        int Store_VALUE = arqument_Başla;
        while (끝 < uzunluq_VALUE) {
            while (끝 < uzunluq_VALUE && 입력[끝] == ' ') 끝++;
            if (끝 == uzunluq_VALUE) break;
            if (arqument_COUNT == arqument_ünvan.length) return -22;
            İcra_Et = 끝;
            while (끝 < uzunluq_VALUE && 입력[끝] != ' ') 끝++;
            arqument_ünvan[arqument_COUNT++] = Store_VALUE;
            수쓰기(Store_VALUE, 끝 - İcra_Et);
            for (int simvol_VALUE_068c2631 = İcra_Et; simvol_VALUE_068c2631 < 끝; simvol_VALUE_068c2631++) 수쓰기(Store_VALUE + 4 + (simvol_VALUE_068c2631 - İcra_Et) * 4, 입력[simvol_VALUE_068c2631]);
            Store_VALUE += 4 + (끝 - İcra_Et) * 4;
        }
        Şəbəkə_Yığın.CLEAN_Proses();
        파일서술자관리.Başla_Proses();
        int ölçü = cihaz_VALUE.icra_istifadəçi_proqram(daxiletmə_p_VALUE, istifadəçi_bitirmək - 16);
        파일서술자관리.CLEAN_Proses();
        Şəbəkə_Yığın.CLEAN_Proses();
        return ölçü;
    }
}
