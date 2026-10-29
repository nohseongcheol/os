// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 읽기 전용 def_ndigel 묶음의 ELF32 wéral, 인수 jëmal_kanam_xëyma, 한 번에 한 kiy_jariñoo_internet yokkute_xëyma def_ndigel. */
public final class 실행관리 {
    static final int Door_kiy_jariñoo_internet_jëfekaay = 0x04000000;
    static final int kiy_jariñoo_internet_jeexal = 0x04400000;
    static final int nataal_jeexal_dëkkuwaay = 0x04200000;
    static final int Tegtal_Door = 0x04300000;
    static int 인수수 = 0;
    static int[] Tegtal_dëkkuwaay = new int[16];

    static boolean kilip(int dëkkuwaay, int diir_xëyma) {
        return dëkkuwaay >= Door_kiy_jariñoo_internet_jëfekaay && dëkkuwaay < kiy_jariñoo_internet_jeexal && diir_xëyma >= 0 && diir_xëyma <= kiy_jariñoo_internet_jeexal - dëkkuwaay;
    }

    static int 수(int dëkkuwaay) { return 기억공간.Segg_lëmm(dëkkuwaay); }
    static int 짧은수(int dëkkuwaay) { return toftal_xëyma.기억읽기(dëkkuwaay) | toftal_xëyma.기억읽기(dëkkuwaay + 1) << 8; }
    static void 수쓰기(int dëkkuwaay, int xëyma) {
        for (int àlluwa_tur = 0; àlluwa_tur < 4; àlluwa_tur++) toftal_xëyma.biir_fatlekookaay(dëkkuwaay + àlluwa_tur, xëyma >>> (àlluwa_tur * 8));
    }

    static int 묶음개수() {
        int dëkkuwaay = toftal_xëyma.실행묶음();
        int tolluwaay = toftal_xëyma.실행묶음크기();
        if (tolluwaay < 8 || 수(dëkkuwaay) != 0x50414b4a) return 0;
        int 개수 = 수(dëkkuwaay + 4);
        return 개수 >= 0 && 개수 <= 32 && 개수 <= (tolluwaay - 8) / 24 ? 개수 : 0;
    }

    static void dugal_xabaar_lim() {
        for (int àlluwa_tur = 0; àlluwa_tur < 묶음개수(); àlluwa_tur++) {
            int dugal_xabaar_xëyma = toftal_xëyma.실행묶음() + 8 + àlluwa_tur * 24;
            for (int Araf_xëyma = 0; Araf_xëyma < 16 && toftal_xëyma.기억읽기(dugal_xabaar_xëyma + Araf_xëyma) != 0; Araf_xëyma++)
                문자단말.문자(toftal_xëyma.기억읽기(dugal_xabaar_xëyma + Araf_xëyma));
            문자단말.biir("\n");
        }
    }

    static int seet_dugal_xabaar(int[] 입력, int daw, int diir_xëyma) {
        if (diir_xëyma <= 0 || diir_xëyma >= 16) return 0;
        for (int àlluwa_tur = 0; àlluwa_tur < 묶음개수(); àlluwa_tur++) {
            int dugal_xabaar_xëyma = toftal_xëyma.실행묶음() + 8 + àlluwa_tur * 24;
            boolean 같음 = toftal_xëyma.기억읽기(dugal_xabaar_xëyma + diir_xëyma) == 0;
            for (int Araf_xëyma = 0; Araf_xëyma < diir_xëyma; Araf_xëyma++)
                if (입력[daw + Araf_xëyma] != toftal_xëyma.기억읽기(dugal_xabaar_xëyma + Araf_xëyma)) 같음 = false;
            if (같음) return dugal_xabaar_xëyma;
        }
        return 0;
    }

    static int wéral(int bara_denc, int diir_xëyma) {
        if (diir_xëyma < 52 || 수(bara_denc) != 0x464c457f || toftal_xëyma.기억읽기(bara_denc + 4) != 1
            || toftal_xëyma.기억읽기(bara_denc + 5) != 1 || toftal_xëyma.기억읽기(bara_denc + 6) != 1
            || 짧은수(bara_denc + 16) != 2 || 짧은수(bara_denc + 18) != 3 || 수(bara_denc + 20) != 1
            || 짧은수(bara_denc + 40) != 52 || 짧은수(bara_denc + 42) != 32) return -8;
        int dugal_xabaar_Tomb_xëyma = 수(bara_denc + 24);
        int 표위치 = 수(bara_denc + 28);
        int 개수 = 짧은수(bara_denc + 44);
        if (개수 == 0 || 개수 > 16 || 표위치 < 52 || 표위치 > diir_xëyma - 개수 * 32) return -8;
        boolean 실행가능 = false;
        for (int àlluwa_tur = 0; àlluwa_tur < 개수; àlluwa_tur++) {
            int 표 = bara_denc + 표위치 + àlluwa_tur * 32;
            int 종류 = 수(표);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 JOKKOO/해석기 미지원
            if (종류 != 1) continue;
            int 위치 = 수(표 + 4), dëkkuwaay = 수(표 + 8), bara_denc_tolluwaay = 수(표 + 16), fatlekookaay_tolluwaay = 수(표 + 20);
            int Féeteel_xëyma = 수(표 + 28);
            if (dëkkuwaay < Door_kiy_jariñoo_internet_jëfekaay || dëkkuwaay >= nataal_jeexal_dëkkuwaay || fatlekookaay_tolluwaay < 0 || fatlekookaay_tolluwaay > nataal_jeexal_dëkkuwaay - dëkkuwaay
                || bara_denc_tolluwaay < 0 || bara_denc_tolluwaay > fatlekookaay_tolluwaay || 위치 < 0 || (bara_denc_tolluwaay > 0 && 위치 > diir_xëyma - bara_denc_tolluwaay)
                || (Féeteel_xëyma != 0 && (Féeteel_xëyma < 0 || (Féeteel_xëyma & (Féeteel_xëyma - 1)) != 0
                    || ((dëkkuwaay - 위치) & (Féeteel_xëyma - 1)) != 0))) return -8;
            for (int 앞 = 0; 앞 < àlluwa_tur; 앞++) {
                int 이전 = bara_denc + 표위치 + 앞 * 32;
                if (수(이전) == 1 && fatlekookaay_tolluwaay > 0 && 수(이전 + 20) > 0
                    && dëkkuwaay < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < dëkkuwaay + fatlekookaay_tolluwaay) return -8;
            }
            if ((수(표 + 24) & 1) != 0 && dugal_xabaar_Tomb_xëyma >= dëkkuwaay && dugal_xabaar_Tomb_xëyma - dëkkuwaay < bara_denc_tolluwaay) 실행가능 = true;
        }
        return 실행가능 ? dugal_xabaar_Tomb_xëyma : -8;
    }

    static int def_ndigel(int[] 입력, int daw, int diir_xëyma) {
        while (daw < diir_xëyma && 입력[daw] == ' ') daw++;
        int 끝 = daw;
        while (끝 < diir_xëyma && 입력[끝] != ' ') 끝++;
        int dugal_xabaar_xëyma = seet_dugal_xabaar(입력, daw, 끝 - daw);
        if (dugal_xabaar_xëyma == 0) return -2;
        int 위치 = 수(dugal_xabaar_xëyma + 16), tolluwaay = 수(dugal_xabaar_xëyma + 20);
        if (위치 < 8 + 묶음개수() * 24 || tolluwaay < 52 || 위치 > toftal_xëyma.실행묶음크기() - tolluwaay) return -8;
        int bara_denc = toftal_xëyma.실행묶음() + 위치;
        int dugal_xabaar_Tomb_xëyma = wéral(bara_denc, tolluwaay);
        if (dugal_xabaar_Tomb_xëyma < 0) return dugal_xabaar_Tomb_xëyma;
        toftal_xëyma.kiy_jariñoo_internet_efaase_TOC();
        int 표위치 = 수(bara_denc + 28), 개수 = 짧은수(bara_denc + 44);
        for (int àlluwa_tur = 0; àlluwa_tur < 개수; àlluwa_tur++) {
            int 표 = bara_denc + 표위치 + àlluwa_tur * 32;
            if (수(표) != 1) continue;
            int 원본 = bara_denc + 수(표 + 4), jëmmukaay_xëyma = 수(표 + 8), bara_denc_tolluwaay = 수(표 + 16);
            for (int okte_xëyma = 0; okte_xëyma < bara_denc_tolluwaay; okte_xëyma++) toftal_xëyma.biir_fatlekookaay(jëmmukaay_xëyma + okte_xëyma, toftal_xëyma.기억읽기(원본 + okte_xëyma));
        }
        인수수 = 0;
        int Store_xëyma = Tegtal_Door;
        while (끝 < diir_xëyma) {
            while (끝 < diir_xëyma && 입력[끝] == ' ') 끝++;
            if (끝 == diir_xëyma) break;
            if (인수수 == Tegtal_dëkkuwaay.length) return -22;
            daw = 끝;
            while (끝 < diir_xëyma && 입력[끝] != ' ') 끝++;
            Tegtal_dëkkuwaay[인수수++] = Store_xëyma;
            수쓰기(Store_xëyma, 끝 - daw);
            for (int Araf_xëyma = daw; Araf_xëyma < 끝; Araf_xëyma++) 수쓰기(Store_xëyma + 4 + (Araf_xëyma - daw) * 4, 입력[Araf_xëyma]);
            Store_xëyma += 4 + (끝 - daw) * 4;
        }
        mbaal_Tegalo.과정정리();
        파일서술자관리.Door_yokkute();
        int 결과 = toftal_xëyma.daw_kiy_jariñoo_internet_jëfekaay(dugal_xabaar_Tomb_xëyma, kiy_jariñoo_internet_jeexal - 16);
        파일서술자관리.과정정리();
        mbaal_Tegalo.과정정리();
        return 결과;
    }
}
