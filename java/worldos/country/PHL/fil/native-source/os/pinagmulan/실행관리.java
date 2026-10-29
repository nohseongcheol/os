// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 읽기 전용 Mag_execute_utos 묶음의 ELF32 patunayan, 인수 ipasa_VALUE_24592b8a, 한 번에 한 gumagamit Proseso_VALUE Mag_execute_utos. */
public final class 실행관리 {
    static final int Start_gumagamit_app = 0x04000000;
    static final int gumagamit_tapusin = 0x04400000;
    static final int IMAGE_tapusin_email = 0x04200000;
    static final int argumento_Start = 0x04300000;
    static int argumento_COUNT = 0;
    static int[] argumento_email = new int[16];

    static boolean clip(int email, int haba_VALUE) {
        return email >= Start_gumagamit_app && email < gumagamit_tapusin && haba_VALUE >= 0 && haba_VALUE <= gumagamit_tapusin - email;
    }

    static int 수(int email) { return 기억공간.mag_parse_integer_buong_numero(email); }
    static int 짧은수(int email) { return device_VALUE.기억읽기(email) | device_VALUE.기억읽기(email + 1) << 8; }
    static void 수쓰기(int email, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) device_VALUE.sumulat_Memory(email + INDEX, VALUE >>> (INDEX * 8));
    }

    static int Grupo_COUNT() {
        int email = device_VALUE.실행묶음();
        int sukat_82232621 = device_VALUE.실행묶음크기();
        if (sukat_82232621 < 8 || 수(email) != 0x50414b4a) return 0;
        int item_COUNT = 수(email + 4);
        return item_COUNT >= 0 && item_COUNT <= 32 && item_COUNT <= (sukat_82232621 - 8) / 24 ? item_COUNT : 0;
    }

    static void pagpasok_list() {
        for (int INDEX = 0; INDEX < Grupo_COUNT(); INDEX++) {
            int pagpasok_VALUE = device_VALUE.실행묶음() + 8 + INDEX * 24;
            for (int karakter_VALUE = 0; karakter_VALUE < 16 && device_VALUE.기억읽기(pagpasok_VALUE + karakter_VALUE) != 0; karakter_VALUE++)
                SMS_Terminal.문자(device_VALUE.기억읽기(pagpasok_VALUE + karakter_VALUE));
            SMS_Terminal.sumulat("\n");
        }
    }

    static int FIND_pagpasok(int[] 입력, int run, int haba_VALUE) {
        if (haba_VALUE <= 0 || haba_VALUE >= 16) return 0;
        for (int INDEX = 0; INDEX < Grupo_COUNT(); INDEX++) {
            int pagpasok_VALUE = device_VALUE.실행묶음() + 8 + INDEX * 24;
            boolean 같음 = device_VALUE.기억읽기(pagpasok_VALUE + haba_VALUE) == 0;
            for (int karakter_VALUE = 0; karakter_VALUE < haba_VALUE; karakter_VALUE++)
                if (입력[run + karakter_VALUE] != device_VALUE.기억읽기(pagpasok_VALUE + karakter_VALUE)) 같음 = false;
            if (같음) return pagpasok_VALUE;
        }
        return 0;
    }

    static int patunayan(int file, int haba_VALUE) {
        if (haba_VALUE < 52 || 수(file) != 0x464c457f || device_VALUE.기억읽기(file + 4) != 1
            || device_VALUE.기억읽기(file + 5) != 1 || device_VALUE.기억읽기(file + 6) != 1
            || 짧은수(file + 16) != 2 || 짧은수(file + 18) != 3 || 수(file + 20) != 1
            || 짧은수(file + 40) != 52 || 짧은수(file + 42) != 32) return -8;
        int pagpasok_point_VALUE = 수(file + 24);
        int talahanayan_posisyon = 수(file + 28);
        int item_COUNT = 짧은수(file + 44);
        if (item_COUNT == 0 || item_COUNT > 16 || talahanayan_posisyon < 52 || talahanayan_posisyon > haba_VALUE - item_COUNT * 32) return -8;
        boolean 실행가능 = false;
        for (int INDEX = 0; INDEX < item_COUNT; INDEX++) {
            int LOOKUP_talahanayan = file + talahanayan_posisyon + INDEX * 32;
            int 종류 = 수(LOOKUP_talahanayan);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 CONNECT/parser_48ee4b1b 미지원
            if (종류 != 1) continue;
            int posisyon = 수(LOOKUP_talahanayan + 4), email = 수(LOOKUP_talahanayan + 8), file_sukat = 수(LOOKUP_talahanayan + 16), Memory_sukat = 수(LOOKUP_talahanayan + 20);
            int maghanay_VALUE = 수(LOOKUP_talahanayan + 28);
            if (email < Start_gumagamit_app || email >= IMAGE_tapusin_email || Memory_sukat < 0 || Memory_sukat > IMAGE_tapusin_email - email
                || file_sukat < 0 || file_sukat > Memory_sukat || posisyon < 0 || (file_sukat > 0 && posisyon > haba_VALUE - file_sukat)
                || (maghanay_VALUE != 0 && (maghanay_VALUE < 0 || (maghanay_VALUE & (maghanay_VALUE - 1)) != 0
                    || ((email - posisyon) & (maghanay_VALUE - 1)) != 0))) return -8;
            for (int nasa_harap_VALUE = 0; nasa_harap_VALUE < INDEX; nasa_harap_VALUE++) {
                int 이전 = file + talahanayan_posisyon + nasa_harap_VALUE * 32;
                if (수(이전) == 1 && Memory_sukat > 0 && 수(이전 + 20) > 0
                    && email < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < email + Memory_sukat) return -8;
            }
            if ((수(LOOKUP_talahanayan + 24) & 1) != 0 && pagpasok_point_VALUE >= email && pagpasok_point_VALUE - email < file_sukat) 실행가능 = true;
        }
        return 실행가능 ? pagpasok_point_VALUE : -8;
    }

    static int Mag_execute_utos(int[] 입력, int run, int haba_VALUE) {
        while (run < haba_VALUE && 입력[run] == ' ') run++;
        int 끝 = run;
        while (끝 < haba_VALUE && 입력[끝] != ' ') 끝++;
        int pagpasok_VALUE = FIND_pagpasok(입력, run, 끝 - run);
        if (pagpasok_VALUE == 0) return -2;
        int posisyon = 수(pagpasok_VALUE + 16), sukat_82232621 = 수(pagpasok_VALUE + 20);
        if (posisyon < 8 + Grupo_COUNT() * 24 || sukat_82232621 < 52 || posisyon > device_VALUE.실행묶음크기() - sukat_82232621) return -8;
        int file = device_VALUE.실행묶음() + posisyon;
        int pagpasok_point_VALUE = patunayan(file, sukat_82232621);
        if (pagpasok_point_VALUE < 0) return pagpasok_point_VALUE;
        device_VALUE.gumagamit_i_clear_TOC();
        int talahanayan_posisyon = 수(file + 28), item_COUNT = 짧은수(file + 44);
        for (int INDEX = 0; INDEX < item_COUNT; INDEX++) {
            int LOOKUP_talahanayan = file + talahanayan_posisyon + INDEX * 32;
            if (수(LOOKUP_talahanayan) != 1) continue;
            int 원본 = file + 수(LOOKUP_talahanayan + 4), patutunguhan_VALUE = 수(LOOKUP_talahanayan + 8), file_sukat = 수(LOOKUP_talahanayan + 16);
            for (int byte_VALUE = 0; byte_VALUE < file_sukat; byte_VALUE++) device_VALUE.sumulat_Memory(patutunguhan_VALUE + byte_VALUE, device_VALUE.기억읽기(원본 + byte_VALUE));
        }
        argumento_COUNT = 0;
        int Store_VALUE = argumento_Start;
        while (끝 < haba_VALUE) {
            while (끝 < haba_VALUE && 입력[끝] == ' ') 끝++;
            if (끝 == haba_VALUE) break;
            if (argumento_COUNT == argumento_email.length) return -22;
            run = 끝;
            while (끝 < haba_VALUE && 입력[끝] != ' ') 끝++;
            argumento_email[argumento_COUNT++] = Store_VALUE;
            수쓰기(Store_VALUE, 끝 - run);
            for (int karakter_VALUE = run; karakter_VALUE < 끝; karakter_VALUE++) 수쓰기(Store_VALUE + 4 + (karakter_VALUE - run) * 4, 입력[karakter_VALUE]);
            Store_VALUE += 4 + (끝 - run) * 4;
        }
        Network_Stack.CLEAN_Proseso();
        파일서술자관리.Start_Proseso();
        int sukat = device_VALUE.run_gumagamit_app(pagpasok_point_VALUE, gumagamit_tapusin - 16);
        파일서술자관리.CLEAN_Proseso();
        Network_Stack.CLEAN_Proseso();
        return sukat;
    }
}
