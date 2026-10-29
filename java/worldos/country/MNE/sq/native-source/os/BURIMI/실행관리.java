// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Leximi 전용 zbatoj_komandë 묶음의 ELF32 vlerësoj, Argumente paso_VALUE, 한 번에 한 përdorues Proces_VALUE zbatoj_komandë. */
public final class 실행관리 {
    static final int nis_përdorues_program = 0x04000000;
    static final int përdorues_mbaroj = 0x04400000;
    static final int IMAGE_mbaroj_email = 0x04200000;
    static final int argument_nis = 0x04300000;
    static int argument_COUNT = 0;
    static int[] argument_email = new int[16];

    static boolean fragment(int email, int gjatësi_VALUE) {
        return email >= nis_përdorues_program && email < përdorues_mbaroj && gjatësi_VALUE >= 0 && gjatësi_VALUE <= përdorues_mbaroj - email;
    }

    static int 수(int email) { return 기억공간.analizoj_numër_i_plotë(email); }
    static int 짧은수(int email) { return pajisje_VALUE.기억읽기(email) | pajisje_VALUE.기억읽기(email + 1) << 8; }
    static void 수쓰기(int email, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) pajisje_VALUE.shkruaj_Memorie(email + INDEX, VALUE >>> (INDEX * 8));
    }

    static int grup_COUNT() {
        int email = pajisje_VALUE.실행묶음();
        int Madhësi = pajisje_VALUE.실행묶음크기();
        if (Madhësi < 8 || 수(email) != 0x50414b4a) return 0;
        int njësi_COUNT = 수(email + 4);
        return njësi_COUNT >= 0 && njësi_COUNT <= 32 && njësi_COUNT <= (Madhësi - 8) / 24 ? njësi_COUNT : 0;
    }

    static void futje_Listë() {
        for (int INDEX = 0; INDEX < grup_COUNT(); INDEX++) {
            int futje_VALUE = pajisje_VALUE.실행묶음() + 8 + INDEX * 24;
            for (int karakter_VALUE = 0; karakter_VALUE < 16 && pajisje_VALUE.기억읽기(futje_VALUE + karakter_VALUE) != 0; karakter_VALUE++)
                SMS_Terminali.문자(pajisje_VALUE.기억읽기(futje_VALUE + karakter_VALUE));
            SMS_Terminali.Shkrimi("\n");
        }
    }

    static int FIND_futje(int[] 입력, int Ekzekuto, int gjatësi_VALUE) {
        if (gjatësi_VALUE <= 0 || gjatësi_VALUE >= 16) return 0;
        for (int INDEX = 0; INDEX < grup_COUNT(); INDEX++) {
            int futje_VALUE = pajisje_VALUE.실행묶음() + 8 + INDEX * 24;
            boolean 같음 = pajisje_VALUE.기억읽기(futje_VALUE + gjatësi_VALUE) == 0;
            for (int karakter_VALUE = 0; karakter_VALUE < gjatësi_VALUE; karakter_VALUE++)
                if (입력[Ekzekuto + karakter_VALUE] != pajisje_VALUE.기억읽기(futje_VALUE + karakter_VALUE)) 같음 = false;
            if (같음) return futje_VALUE;
        }
        return 0;
    }

    static int vlerësoj(int Kartelë, int gjatësi_VALUE) {
        if (gjatësi_VALUE < 52 || 수(Kartelë) != 0x464c457f || pajisje_VALUE.기억읽기(Kartelë + 4) != 1
            || pajisje_VALUE.기억읽기(Kartelë + 5) != 1 || pajisje_VALUE.기억읽기(Kartelë + 6) != 1
            || 짧은수(Kartelë + 16) != 2 || 짧은수(Kartelë + 18) != 3 || 수(Kartelë + 20) != 1
            || 짧은수(Kartelë + 40) != 52 || 짧은수(Kartelë + 42) != 32) return -8;
        int futje_p_VALUE = 수(Kartelë + 24);
        int tabelë_pozicioni = 수(Kartelë + 28);
        int njësi_COUNT = 짧은수(Kartelë + 44);
        if (njësi_COUNT == 0 || njësi_COUNT > 16 || tabelë_pozicioni < 52 || tabelë_pozicioni > gjatësi_VALUE - njësi_COUNT * 32) return -8;
        boolean 실행가능 = false;
        for (int INDEX = 0; INDEX < njësi_COUNT; INDEX++) {
            int LOOKUP_tabelë = Kartelë + tabelë_pozicioni + INDEX * 32;
            int 종류 = 수(LOOKUP_tabelë);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Lidhu/analizues_48ee4b1b 미지원
            if (종류 != 1) continue;
            int Pozicioni = 수(LOOKUP_tabelë + 4), email = 수(LOOKUP_tabelë + 8), skedar_ndryshoj_përmasat = 수(LOOKUP_tabelë + 16), Memorie_ndryshoj_përmasat = 수(LOOKUP_tabelë + 20);
            int drejtvendos_VALUE = 수(LOOKUP_tabelë + 28);
            if (email < nis_përdorues_program || email >= IMAGE_mbaroj_email || Memorie_ndryshoj_përmasat < 0 || Memorie_ndryshoj_përmasat > IMAGE_mbaroj_email - email
                || skedar_ndryshoj_përmasat < 0 || skedar_ndryshoj_përmasat > Memorie_ndryshoj_përmasat || Pozicioni < 0 || (skedar_ndryshoj_përmasat > 0 && Pozicioni > gjatësi_VALUE - skedar_ndryshoj_përmasat)
                || (drejtvendos_VALUE != 0 && (drejtvendos_VALUE < 0 || (drejtvendos_VALUE & (drejtvendos_VALUE - 1)) != 0
                    || ((email - Pozicioni) & (drejtvendos_VALUE - 1)) != 0))) return -8;
            for (int e_përparme_VALUE = 0; e_përparme_VALUE < INDEX; e_përparme_VALUE++) {
                int 이전 = Kartelë + tabelë_pozicioni + e_përparme_VALUE * 32;
                if (수(이전) == 1 && Memorie_ndryshoj_përmasat > 0 && 수(이전 + 20) > 0
                    && email < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < email + Memorie_ndryshoj_përmasat) return -8;
            }
            if ((수(LOOKUP_tabelë + 24) & 1) != 0 && futje_p_VALUE >= email && futje_p_VALUE - email < skedar_ndryshoj_përmasat) 실행가능 = true;
        }
        return 실행가능 ? futje_p_VALUE : -8;
    }

    static int zbatoj_komandë(int[] 입력, int Ekzekuto, int gjatësi_VALUE) {
        while (Ekzekuto < gjatësi_VALUE && 입력[Ekzekuto] == ' ') Ekzekuto++;
        int 끝 = Ekzekuto;
        while (끝 < gjatësi_VALUE && 입력[끝] != ' ') 끝++;
        int futje_VALUE = FIND_futje(입력, Ekzekuto, 끝 - Ekzekuto);
        if (futje_VALUE == 0) return -2;
        int Pozicioni = 수(futje_VALUE + 16), Madhësi = 수(futje_VALUE + 20);
        if (Pozicioni < 8 + grup_COUNT() * 24 || Madhësi < 52 || Pozicioni > pajisje_VALUE.실행묶음크기() - Madhësi) return -8;
        int Kartelë = pajisje_VALUE.실행묶음() + Pozicioni;
        int futje_p_VALUE = vlerësoj(Kartelë, Madhësi);
        if (futje_p_VALUE < 0) return futje_p_VALUE;
        pajisje_VALUE.përdorues_pastroj_TOC();
        int tabelë_pozicioni = 수(Kartelë + 28), njësi_COUNT = 짧은수(Kartelë + 44);
        for (int INDEX = 0; INDEX < njësi_COUNT; INDEX++) {
            int LOOKUP_tabelë = Kartelë + tabelë_pozicioni + INDEX * 32;
            if (수(LOOKUP_tabelë) != 1) continue;
            int 원본 = Kartelë + 수(LOOKUP_tabelë + 4), vendmbërritje_VALUE = 수(LOOKUP_tabelë + 8), skedar_ndryshoj_përmasat = 수(LOOKUP_tabelë + 16);
            for (int bajt_VALUE = 0; bajt_VALUE < skedar_ndryshoj_përmasat; bajt_VALUE++) pajisje_VALUE.shkruaj_Memorie(vendmbërritje_VALUE + bajt_VALUE, pajisje_VALUE.기억읽기(원본 + bajt_VALUE));
        }
        argument_COUNT = 0;
        int Store_VALUE = argument_nis;
        while (끝 < gjatësi_VALUE) {
            while (끝 < gjatësi_VALUE && 입력[끝] == ' ') 끝++;
            if (끝 == gjatësi_VALUE) break;
            if (argument_COUNT == argument_email.length) return -22;
            Ekzekuto = 끝;
            while (끝 < gjatësi_VALUE && 입력[끝] != ' ') 끝++;
            argument_email[argument_COUNT++] = Store_VALUE;
            수쓰기(Store_VALUE, 끝 - Ekzekuto);
            for (int karakter_VALUE = Ekzekuto; karakter_VALUE < 끝; karakter_VALUE++) 수쓰기(Store_VALUE + 4 + (karakter_VALUE - Ekzekuto) * 4, 입력[karakter_VALUE]);
            Store_VALUE += 4 + (끝 - Ekzekuto) * 4;
        }
        rrjet_Stivë.CLEAN_Proces();
        파일서술자관리.nis_Proces();
        int llogaritje = pajisje_VALUE.varg_përdorues_program(futje_p_VALUE, përdorues_mbaroj - 16);
        파일서술자관리.CLEAN_Proces();
        rrjet_Stivë.CLEAN_Proces();
        return llogaritje;
    }
}
