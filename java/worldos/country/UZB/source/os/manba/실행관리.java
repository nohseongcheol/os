// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Oʻqish 전용 bajarmoq_buyruq 묶음의 ELF32 tasdiqlash, 인수 Oldinga_VALUE, 한 번에 한 foydalanuvchi Jarayon_VALUE bajarmoq_buyruq. */
public final class 실행관리 {
    static final int Start_foydalanuvchi_ilova = 0x04000000;
    static final int foydalanuvchi_to_xtatmoq = 0x04400000;
    static final int rasm_to_xtatmoq_manzil = 0x04200000;
    static final int dalil_Start = 0x04300000;
    static int dalil_COUNT = 0;
    static int[] dalil_manzil = new int[16];

    static boolean klip(int manzil, int uzunlik_VALUE) {
        return manzil >= Start_foydalanuvchi_ilova && manzil < foydalanuvchi_to_xtatmoq && uzunlik_VALUE >= 0 && uzunlik_VALUE <= foydalanuvchi_to_xtatmoq - manzil;
    }

    static int 수(int manzil) { return 기억공간.tahlil_qilmoq_butun_son(manzil); }
    static int 짧은수(int manzil) { return qurilma_VALUE.기억읽기(manzil) | qurilma_VALUE.기억읽기(manzil + 1) << 8; }
    static void 수쓰기(int manzil, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) qurilma_VALUE.yozmoq_Xotira(manzil + INDEX, VALUE >>> (INDEX * 8));
    }

    static int Guruh_COUNT() {
        int manzil = qurilma_VALUE.실행묶음();
        int Hajmi = qurilma_VALUE.실행묶음크기();
        if (Hajmi < 8 || 수(manzil) != 0x50414b4a) return 0;
        int element_COUNT = 수(manzil + 4);
        return element_COUNT >= 0 && element_COUNT <= 32 && element_COUNT <= (Hajmi - 8) / 24 ? element_COUNT : 0;
    }

    static void kiritish_Ro_yxat() {
        for (int INDEX = 0; INDEX < Guruh_COUNT(); INDEX++) {
            int kiritish_VALUE = qurilma_VALUE.실행묶음() + 8 + INDEX * 24;
            for (int belgi_VALUE = 0; belgi_VALUE < 16 && qurilma_VALUE.기억읽기(kiritish_VALUE + belgi_VALUE) != 0; belgi_VALUE++)
                SMS_Terminal.문자(qurilma_VALUE.기억읽기(kiritish_VALUE + belgi_VALUE));
            SMS_Terminal.Yozish("\n");
        }
    }

    static int FIND_kiritish(int[] 입력, int Bajarish, int uzunlik_VALUE) {
        if (uzunlik_VALUE <= 0 || uzunlik_VALUE >= 16) return 0;
        for (int INDEX = 0; INDEX < Guruh_COUNT(); INDEX++) {
            int kiritish_VALUE = qurilma_VALUE.실행묶음() + 8 + INDEX * 24;
            boolean 같음 = qurilma_VALUE.기억읽기(kiritish_VALUE + uzunlik_VALUE) == 0;
            for (int belgi_VALUE = 0; belgi_VALUE < uzunlik_VALUE; belgi_VALUE++)
                if (입력[Bajarish + belgi_VALUE] != qurilma_VALUE.기억읽기(kiritish_VALUE + belgi_VALUE)) 같음 = false;
            if (같음) return kiritish_VALUE;
        }
        return 0;
    }

    static int tasdiqlash(int Fayl, int uzunlik_VALUE) {
        if (uzunlik_VALUE < 52 || 수(Fayl) != 0x464c457f || qurilma_VALUE.기억읽기(Fayl + 4) != 1
            || qurilma_VALUE.기억읽기(Fayl + 5) != 1 || qurilma_VALUE.기억읽기(Fayl + 6) != 1
            || 짧은수(Fayl + 16) != 2 || 짧은수(Fayl + 18) != 3 || 수(Fayl + 20) != 1
            || 짧은수(Fayl + 40) != 52 || 짧은수(Fayl + 42) != 32) return -8;
        int kiritish_nuqta_VALUE = 수(Fayl + 24);
        int jadval_holat = 수(Fayl + 28);
        int element_COUNT = 짧은수(Fayl + 44);
        if (element_COUNT == 0 || element_COUNT > 16 || jadval_holat < 52 || jadval_holat > uzunlik_VALUE - element_COUNT * 32) return -8;
        boolean 실행가능 = false;
        for (int INDEX = 0; INDEX < element_COUNT; INDEX++) {
            int LOOKUP_jadval = Fayl + jadval_holat + INDEX * 32;
            int 종류 = 수(LOOKUP_jadval);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Ulanish/parser_48ee4b1b 미지원
            if (종류 != 1) continue;
            int Holati = 수(LOOKUP_jadval + 4), manzil = 수(LOOKUP_jadval + 8), fayl_o_lcham = 수(LOOKUP_jadval + 16), Xotira_o_lcham = 수(LOOKUP_jadval + 20);
            int tenglashtirmoq_VALUE = 수(LOOKUP_jadval + 28);
            if (manzil < Start_foydalanuvchi_ilova || manzil >= rasm_to_xtatmoq_manzil || Xotira_o_lcham < 0 || Xotira_o_lcham > rasm_to_xtatmoq_manzil - manzil
                || fayl_o_lcham < 0 || fayl_o_lcham > Xotira_o_lcham || Holati < 0 || (fayl_o_lcham > 0 && Holati > uzunlik_VALUE - fayl_o_lcham)
                || (tenglashtirmoq_VALUE != 0 && (tenglashtirmoq_VALUE < 0 || (tenglashtirmoq_VALUE & (tenglashtirmoq_VALUE - 1)) != 0
                    || ((manzil - Holati) & (tenglashtirmoq_VALUE - 1)) != 0))) return -8;
            for (int old_kamera_VALUE = 0; old_kamera_VALUE < INDEX; old_kamera_VALUE++) {
                int 이전 = Fayl + jadval_holat + old_kamera_VALUE * 32;
                if (수(이전) == 1 && Xotira_o_lcham > 0 && 수(이전 + 20) > 0
                    && manzil < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < manzil + Xotira_o_lcham) return -8;
            }
            if ((수(LOOKUP_jadval + 24) & 1) != 0 && kiritish_nuqta_VALUE >= manzil && kiritish_nuqta_VALUE - manzil < fayl_o_lcham) 실행가능 = true;
        }
        return 실행가능 ? kiritish_nuqta_VALUE : -8;
    }

    static int bajarmoq_buyruq(int[] 입력, int Bajarish, int uzunlik_VALUE) {
        while (Bajarish < uzunlik_VALUE && 입력[Bajarish] == ' ') Bajarish++;
        int 끝 = Bajarish;
        while (끝 < uzunlik_VALUE && 입력[끝] != ' ') 끝++;
        int kiritish_VALUE = FIND_kiritish(입력, Bajarish, 끝 - Bajarish);
        if (kiritish_VALUE == 0) return -2;
        int Holati = 수(kiritish_VALUE + 16), Hajmi = 수(kiritish_VALUE + 20);
        if (Holati < 8 + Guruh_COUNT() * 24 || Hajmi < 52 || Holati > qurilma_VALUE.실행묶음크기() - Hajmi) return -8;
        int Fayl = qurilma_VALUE.실행묶음() + Holati;
        int kiritish_nuqta_VALUE = tasdiqlash(Fayl, Hajmi);
        if (kiritish_nuqta_VALUE < 0) return kiritish_nuqta_VALUE;
        qurilma_VALUE.foydalanuvchi_tozalamoq_TOC();
        int jadval_holat = 수(Fayl + 28), element_COUNT = 짧은수(Fayl + 44);
        for (int INDEX = 0; INDEX < element_COUNT; INDEX++) {
            int LOOKUP_jadval = Fayl + jadval_holat + INDEX * 32;
            if (수(LOOKUP_jadval) != 1) continue;
            int 원본 = Fayl + 수(LOOKUP_jadval + 4), ko_chirish_joyi_VALUE = 수(LOOKUP_jadval + 8), fayl_o_lcham = 수(LOOKUP_jadval + 16);
            for (int bayt_VALUE = 0; bayt_VALUE < fayl_o_lcham; bayt_VALUE++) qurilma_VALUE.yozmoq_Xotira(ko_chirish_joyi_VALUE + bayt_VALUE, qurilma_VALUE.기억읽기(원본 + bayt_VALUE));
        }
        dalil_COUNT = 0;
        int Store_VALUE = dalil_Start;
        while (끝 < uzunlik_VALUE) {
            while (끝 < uzunlik_VALUE && 입력[끝] == ' ') 끝++;
            if (끝 == uzunlik_VALUE) break;
            if (dalil_COUNT == dalil_manzil.length) return -22;
            Bajarish = 끝;
            while (끝 < uzunlik_VALUE && 입력[끝] != ' ') 끝++;
            dalil_manzil[dalil_COUNT++] = Store_VALUE;
            수쓰기(Store_VALUE, 끝 - Bajarish);
            for (int belgi_VALUE = Bajarish; belgi_VALUE < 끝; belgi_VALUE++) 수쓰기(Store_VALUE + 4 + (belgi_VALUE - Bajarish) * 4, 입력[belgi_VALUE]);
            Store_VALUE += 4 + (끝 - Bajarish) * 4;
        }
        Tarmoq_Stack.Toza_Jarayon();
        파일서술자관리.Start_Jarayon();
        int o_lchov = qurilma_VALUE.ishlash_foydalanuvchi_ilova(kiritish_nuqta_VALUE, foydalanuvchi_to_xtatmoq - 16);
        파일서술자관리.Toza_Jarayon();
        Tarmoq_Stack.Toza_Jarayon();
        return o_lchov;
    }
}
