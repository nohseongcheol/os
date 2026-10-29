// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. file/스택/Sanggunian/sanga 경계를 Mag_execute_utos 중 검사한다. */
public final class 자바가상기계 {
    static int[] file = new int[16 * 16384], 임시파일 = new int[16384], file_pangalan_SMS = new int[512];
    static int[] constant_tag = new int[8192], 상가 = new int[8192], constant_SECOND_VALUE = new int[8192], string_Sanggunian = new int[8192];
    static int[] pamamaraan_pangalan_SMS = new int[512], pamamaraan_TYPE = new int[512], pamamaraan_access = new int[512], pamamaraan_may_ari = new int[512];
    static int[] pamamaraan_Start = new int[512], pamamaraan_tapusin = new int[512], pamamaraan_Stack = new int[512], 함수지역 = new int[512];
    static int[] pamamaraan_argumento_COUNT = new int[512], pamamaraan_argumento_TYPE = new int[8192], 함수반환 = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] lokal_VALUE = new int[16384], lokal_TYPE = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] frame_pamamaraan = new int[128], frame_posisyon = new int[128], frame_Stack = new int[128], frame_instruksiyon = new int[128], magsimula_frame = new int[128];
    static int[] kategorya_Kahulugan_pangalan = new int[16], kategorya_Kahulugan_sukat = new int[16], 종부모 = new int[16], kategorya_Kahulugan_katayuan = new int[16], kategorya_espasyo_COUNT = new int[16], magsimula_kategorya_Kahulugan = new int[16];
    static int[] kategorya_interface = new int[16 * 16], kategorya_interface_COUNT = new int[16];
    static int[] espasyo_pangalan = new int[512], espasyo_TYPE = new int[512], espasyo_may_ari = new int[512], espasyo_Mga_Pahintulot = new int[512], espasyo_posisyon = new int[512], espasyo_data = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], ARRAY_elemento = new int[32768], Store_integer_buong_numero = new int[256];
    static int sukat_82232621, 읽기위치, pamamaraan_COUNT, kategorya_pangalan, frame_INDEX = -1, 힙끝 = 1, 반환형;
    static int kategorya_Kahulugan_COUNT, espasyo_COUNT, 잡기수, 현재읽는종, 던진객체, 잠시수, display_COUNT, Koleksyon_COUNT;
    static int 현재가닥, thread_COUNT = 1, pagpasok_kategorya_Kahulugan;
    static int[] thread_frame = new int[4], thread_katayuan = new int[4], thread_bagay = new int[4], thread_target = new int[4], 가닥대기 = new int[4];
    static boolean error, 바꿈요청;
    static int[] 잠금주인 = new int[32768], 잠금깊이 = new int[32768], 틀잠금 = new int[128], 종잠금 = new int[16], kategorya_thread = new int[16];

    static void pagpalya_VALUE(String Word_SMS) {
        if (error) return;
        int kategorya_CODE = 0;
        if (자바도구.같음(Word_SMS, "ArithmeticException: / by zero")) kategorya_CODE = 4;
        if (자바도구.같음(Word_SMS, "NullPointerException") || 자바도구.같음(Word_SMS, "null or invalid array")) kategorya_CODE = 5;
        if (자바도구.같음(Word_SMS, "ArrayIndexOutOfBoundsException")) kategorya_CODE = 7;
        if (자바도구.같음(Word_SMS, "StringIndexOutOfBoundsException")) kategorya_CODE = 8;
        if (자바도구.같음(Word_SMS, "NumberFormatException")) kategorya_CODE = 10;
        if (자바도구.같음(Word_SMS, "FileNotFoundException: file open failed")) kategorya_CODE = 12;
        if (자바도구.같음(Word_SMS, "IOException: stream closed") || 자바도구.같음(Word_SMS, "IOException: read failed") || 자바도구.같음(Word_SMS, "IOException: write failed")) kategorya_CODE = 11;
        if (자바도구.같음(Word_SMS, "ClassCastException")) kategorya_CODE = 14;
        if (자바도구.같음(Word_SMS, "NegativeArraySizeException")) kategorya_CODE = 15;
        if (kategorya_CODE != 0 && frame_INDEX >= 0) { 예외던짐(kategorya_CODE, Word_SMS); return; }
        gumagamit.sumulat("JVM error: "); gumagamit.sumulat(Word_SMS); gumagamit.sumulat_karakter_VALUE(10); error = true;
    }
    static boolean clip(int run, int haba_VALUE) {
        if (run < 0 || run >= file.length || haba_VALUE < 0) return false;
        int kategorya_Kahulugan = run / 16384;
        return run % 16384 <= kategorya_Kahulugan_sukat[kategorya_Kahulugan] && haba_VALUE <= kategorya_Kahulugan_sukat[kategorya_Kahulugan] - run % 16384;
    }
    static int byte_VALUE() {
        if (!clip(읽기위치, 1)) { pagpalya_VALUE("truncated class file"); return 0; }
        return file[읽기위치++];
    }
    static int 짧은수() { return byte_VALUE() << 8 | byte_VALUE(); }
    static int integer_buong_numero() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int haba_VALUE) { if (!clip(읽기위치, haba_VALUE)) pagpalya_VALUE("invalid attribute size"); else 읽기위치 += haba_VALUE; }
    static boolean tseke_constant(int 수, int 종류) {
        if (수 <= 0 || 수 >= constant_tag.length || constant_tag[수] != 종류) { pagpalya_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int run, int haba_VALUE, String Word_SMS) {
        if (!clip(run, haba_VALUE)) return false;
        int 읽는자리 = run, 끝 = run + haba_VALUE;
        for (int Loop_INDEX = 0; Loop_INDEX < Word_SMS.length(); Loop_INDEX++) {
            int character_code = Word_SMS.charAt(Loop_INDEX);
            if (character_code > 0 && character_code < 128) { if (읽는자리 >= 끝 || file[읽는자리++] != character_code) return false; }
            else if (character_code < 2048) {
                if (읽는자리 + 2 > 끝 || file[읽는자리++] != (192 | (character_code >> 6)) || file[읽는자리++] != (128 | (character_code & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || file[읽는자리++] != (224 | (character_code >> 12)) || file[읽는자리++] != (128 | ((character_code >> 6) & 63)) || file[읽는자리++] != (128 | (character_code & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean Word_SMS(int constant_VALUE, String Word_SMS) { return tseke_constant(constant_VALUE, 1) && 구간(상가[constant_VALUE], constant_SECOND_VALUE[constant_VALUE], Word_SMS); }
    static boolean 같은말(int 가, int 나) {
        if (!tseke_constant(가, 1) || !tseke_constant(나, 1) || constant_SECOND_VALUE[가] != constant_SECOND_VALUE[나]) return false;
        for (int 수 = 0; 수 < constant_SECOND_VALUE[가]; 수++) if (file[상가[가] + 수] != file[상가[나] + 수]) return false;
        return true;
    }
    static int kategorya_pangalan_SMS(int 수) { return tseke_constant(수, 7) && tseke_constant(상가[수], 1) ? 상가[수] : 0; }
    static int Sanggunian_pangalan(int 수) { return tseke_constant(수, 12) && tseke_constant(상가[수], 1) ? 상가[수] : 0; }
    static int Sanggunian_TYPE(int 수) { return tseke_constant(수, 12) && tseke_constant(constant_SECOND_VALUE[수], 1) ? constant_SECOND_VALUE[수] : 0; }
    static int 서술형(int 끝, boolean walang_laman_TYPE) {
        if (읽기위치 >= 끝) { pagpalya_VALUE("invalid descriptor"); return 0; }
        int VALUE = byte_VALUE();
        if (VALUE == 'V' && walang_laman_TYPE) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int run = 읽기위치;
            while (읽기위치 < 끝 && file[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == run) pagpalya_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        pagpalya_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int pormula_VALUE) {
        int 이전 = 읽기위치, 수 = pamamaraan_TYPE[pormula_VALUE];
        if (!tseke_constant(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + constant_SECOND_VALUE[수];
        if (byte_VALUE() != '(') pagpalya_VALUE("invalid method descriptor");
        int item_COUNT = 0;
        while (!error && 읽기위치 < 끝 && file[읽기위치] != ')') {
            if (item_COUNT == 16) { pagpalya_VALUE("too many method arguments"); break; }
            pamamaraan_argumento_TYPE[pormula_VALUE * 16 + item_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || byte_VALUE() != ')') pagpalya_VALUE("invalid method descriptor");
        함수반환[pormula_VALUE] = 서술형(끝, true); pamamaraan_argumento_COUNT[pormula_VALUE] = item_COUNT;
        if (읽기위치 != 끝) pagpalya_VALUE("invalid method descriptor");
        읽기위치 = 이전;
    }
    static int 상번호() { int VALUE = 짧은수(); return VALUE == 0 ? 0 : 현재읽는종 * 512 + VALUE; }
    static int 명상수() { return pamamaraan_may_ari[frame_pamamaraan[frame_INDEX]] * 512 + 명짧(); }
    static void 속성건너() {
        int item_COUNT = 짧은수();
        for (int 수 = 0; 수 < item_COUNT && !error; 수++) { tseke_constant(상번호(), 1); 건너(integer_buong_numero()); }
    }
    static int utos_haba(int VALUE) {
        if (VALUE == 16 || VALUE == 18 || VALUE == 21 || VALUE == 25 || VALUE == 54 || VALUE == 58 || VALUE == 188) return 2;
        if (VALUE == 17 || VALUE == 19 || VALUE == 132 || VALUE >= 153 && VALUE <= 167
            || VALUE >= 178 && VALUE <= 184 || VALUE == 187 || VALUE == 189 || VALUE == 192 || VALUE == 193 || VALUE == 198 || VALUE == 199) return 3;
        if (VALUE == 185 || VALUE == 200) return 5;
        if (VALUE >= 0 && VALUE <= 8 || VALUE >= 26 && VALUE <= 29 || VALUE >= 42 && VALUE <= 46 || VALUE >= 50 && VALUE <= 53
            || VALUE >= 59 && VALUE <= 62 || VALUE >= 75 && VALUE <= 79 || VALUE >= 83 && VALUE <= 95
            || VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 116
            || VALUE == 120 || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130
            || VALUE >= 145 && VALUE <= 147 || VALUE == 172 || VALUE == 176 || VALUE == 177 || VALUE == 190 || VALUE == 191
            || VALUE == 194 || VALUE == 195) return 1;
        return 0;
    }
    static int posisyon_integer_buong_numero(int 읽는자리) {
        if (!clip(읽는자리, 4)) { pagpalya_VALUE("truncated bytecode operand"); return 0; }
        return file[읽는자리] << 24 | file[읽는자리 + 1] << 16 | file[읽는자리 + 2] << 8 | file[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int run, int 끝) {
        int VALUE = file[읽는자리], haba_VALUE = utos_haba(VALUE);
        if (VALUE == 170 || VALUE == 171) {
            int BASE_posisyon = 읽는자리 + 1;
            while ((BASE_posisyon - run) % 4 != 0) BASE_posisyon++;
            if (끝 - BASE_posisyon < (VALUE == 170 ? 12 : 8)) return 0;
            int pagpasok_COUNT = VALUE == 170 ? posisyon_integer_buong_numero(BASE_posisyon + 8) - posisyon_integer_buong_numero(BASE_posisyon + 4) + 1 : posisyon_integer_buong_numero(BASE_posisyon + 4);
            if (pagpasok_COUNT < 0 || pagpasok_COUNT > 2048) return 0;
            haba_VALUE = BASE_posisyon - 읽는자리 + (VALUE == 170 ? 12 + 4 * pagpasok_COUNT : 8 + 8 * pagpasok_COUNT);
        }
        if (VALUE == 196 && 읽는자리 + 1 < 끝) {
            int Word_data = file[읽는자리 + 1]; haba_VALUE = Word_data == 132 ? 6 : (Word_data == 21 || Word_data == 25 || Word_data == 54 || Word_data == 58) ? 4 : 0;
        }
        return haba_VALUE > 0 && haba_VALUE <= 끝 - 읽는자리 ? haba_VALUE : 0;
    }
    static void tseke_patutunguhan_VALUE(int patutunguhan_VALUE, int pormula_VALUE) {
        if (patutunguhan_VALUE < pamamaraan_Start[pormula_VALUE] || patutunguhan_VALUE >= pamamaraan_tapusin[pormula_VALUE] || 경계[patutunguhan_VALUE] != pormula_VALUE + 1) pagpalya_VALUE("invalid branch target");
    }
    static void 클래스읽기(int kategorya_Kahulugan) {
        현재읽는종 = kategorya_Kahulugan; 읽기위치 = kategorya_Kahulugan * 16384; sukat_82232621 = 읽기위치 + kategorya_Kahulugan_sukat[kategorya_Kahulugan];
        if (integer_buong_numero() != 0xcafebabe) { pagpalya_VALUE("not a class file"); return; }
        int 부판 = 짧은수(), bersyon_VALUE = 짧은수();
        if (bersyon_VALUE < 45 || bersyon_VALUE > 52 || 부판 != 0) { pagpalya_VALUE("supported class versions: 45..52, minor 0"); return; }
        int constant_COUNT = 짧은수(), BASE_posisyon = kategorya_Kahulugan * 512;
        if (constant_COUNT < 1 || constant_COUNT > 512) { pagpalya_VALUE("constant pool limit (511)"); return; }
        for (int pagpasok_COUNT = 1; pagpasok_COUNT < constant_COUNT && !error; pagpasok_COUNT++) {
            int 수 = BASE_posisyon + pagpasok_COUNT, 종류 = byte_VALUE(); constant_tag[수] = 종류;
            if (종류 == 1) { constant_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(constant_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = integer_buong_numero();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); constant_SECOND_VALUE[수] = 상번호(); }
            else pagpalya_VALUE("unsupported constant type");
        }
        int pahintulot_VALUE = 짧은수();
        if ((pahintulot_VALUE & (0x2000 | 0x4000)) != 0) pagpalya_VALUE("annotation/enum class unsupported");
        kategorya_Kahulugan_pangalan[kategorya_Kahulugan] = kategorya_pangalan_SMS(상번호());
        종부모[kategorya_Kahulugan] = kategorya_pangalan_SMS(상번호());
        int interface_COUNT = 짧은수(); if (interface_COUNT > 16) { pagpalya_VALUE("interface count limit"); return; }
        kategorya_interface_COUNT[kategorya_Kahulugan] = interface_COUNT;
        for (int Loop_INDEX = 0; Loop_INDEX < interface_COUNT; Loop_INDEX++) kategorya_interface[kategorya_Kahulugan * 16 + Loop_INDEX] = kategorya_pangalan_SMS(상번호());
        int field_COUNT = 짧은수();
        if (field_COUNT > 512 - espasyo_COUNT) { pagpalya_VALUE("field count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < field_COUNT && !error; Loop_INDEX++) {
            int file_INDEX = espasyo_COUNT++; espasyo_may_ari[file_INDEX] = kategorya_Kahulugan; espasyo_Mga_Pahintulot[file_INDEX] = 짧은수(); espasyo_pangalan[file_INDEX] = 상번호(); espasyo_TYPE[file_INDEX] = 상번호();
            tseke_constant(espasyo_pangalan[file_INDEX], 1); tseke_constant(espasyo_TYPE[file_INDEX], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[espasyo_TYPE[file_INDEX]]; int kategorya_CODE = 서술형(읽기위치 + constant_SECOND_VALUE[espasyo_TYPE[file_INDEX]], false); 읽기위치 = 보존값;
            if ((espasyo_Mga_Pahintulot[file_INDEX] & 8) == 0) espasyo_posisyon[file_INDEX] = kategorya_espasyo_COUNT[kategorya_Kahulugan]++;
            int katangian_data = 짧은수();
            for (int inner_join_posisyon = 0; inner_join_posisyon < katangian_data && !error; inner_join_posisyon++) {
                int pangalan_constant = 상번호(), 유효길이 = integer_buong_numero();
                if (Word_SMS(pangalan_constant, "ConstantValue") && 유효길이 == 2) {
                    int data_VALUE = 상번호();
                    if (kategorya_CODE == 1 && tseke_constant(data_VALUE, 3)) espasyo_data[file_INDEX] = 상가[data_VALUE];
                    else if (kategorya_CODE == 2 && tseke_constant(data_VALUE, 8)) espasyo_data[file_INDEX] = constant_SMS(상가[data_VALUE]);
                } else 건너(유효길이);
            }
        }
        int item_COUNT = 짧은수();
        if (item_COUNT > 512 - pamamaraan_COUNT) { pagpalya_VALUE("method count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < item_COUNT && !error; Loop_INDEX++) {
            int 수 = pamamaraan_COUNT++; pamamaraan_may_ari[수] = kategorya_Kahulugan;
            pamamaraan_access[수] = 짧은수(); pamamaraan_pangalan_SMS[수] = 상번호(); pamamaraan_TYPE[수] = 상번호();
            tseke_constant(pamamaraan_pangalan_SMS[수], 1); 서술읽기(수);
            if ((pamamaraan_access[수] & 8) == 0) {
                if (pamamaraan_argumento_COUNT[수] == 16) { pagpalya_VALUE("too many instance method arguments"); return; }
                for (int Paghahambing_posisyon = pamamaraan_argumento_COUNT[수]; Paghahambing_posisyon > 0; Paghahambing_posisyon--) pamamaraan_argumento_TYPE[수 * 16 + Paghahambing_posisyon] = pamamaraan_argumento_TYPE[수 * 16 + Paghahambing_posisyon - 1];
                pamamaraan_argumento_TYPE[수 * 16] = 2; pamamaraan_argumento_COUNT[수]++;
            }
            if ((pamamaraan_access[수] & 0x100) != 0) pagpalya_VALUE("user native method unsupported");
            if (Word_SMS(pamamaraan_pangalan_SMS[수], "<clinit>")) magsimula_kategorya_Kahulugan[kategorya_Kahulugan] = 수 + 1;
            for (int nasa_harap_VALUE = 0; nasa_harap_VALUE < 수; nasa_harap_VALUE++) if (pamamaraan_may_ari[nasa_harap_VALUE] == kategorya_Kahulugan && 같은말(pamamaraan_pangalan_SMS[nasa_harap_VALUE], pamamaraan_pangalan_SMS[수]) && 같은말(pamamaraan_TYPE[nasa_harap_VALUE], pamamaraan_TYPE[수])) pagpalya_VALUE("duplicate method");
            int katangian_COUNT = 짧은수();
            for (int katangian_VALUE = 0; katangian_VALUE < katangian_COUNT && !error; katangian_VALUE++) {
                int pangalan = 상번호(), haba_VALUE = integer_buong_numero(), run = 읽기위치;
                if (!clip(run, haba_VALUE)) { pagpalya_VALUE("truncated method attribute"); break; }
                if (Word_SMS(pangalan, "Code")) {
                    if (pamamaraan_Start[수] != 0) pagpalya_VALUE("duplicate Code attribute");
                    pamamaraan_Stack[수] = 짧은수(); 함수지역[수] = 짧은수(); int CODE_haba = integer_buong_numero();
                    if (pamamaraan_Stack[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < pamamaraan_argumento_COUNT[수]
                        || CODE_haba < 1 || CODE_haba > 8192) pagpalya_VALUE("method memory limits exceeded");
                    pamamaraan_Start[수] = 읽기위치; 건너(CODE_haba); pamamaraan_tapusin[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { pagpalya_VALUE("exception table limit"); return; }
                    for (int inner_join_posisyon = 0; inner_join_posisyon < 잡는수; inner_join_posisyon++) {
                        int error_Sanggunian = 잡기수++; 잡기함수[error_Sanggunian] = 수;
                        잡기시작[error_Sanggunian] = pamamaraan_Start[수] + 짧은수(); 잡기끝[error_Sanggunian] = pamamaraan_Start[수] + 짧은수();
                        잡기위치[error_Sanggunian] = pamamaraan_Start[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[error_Sanggunian] = 부호값 == 0 ? 0 : kategorya_pangalan_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != run + haba_VALUE) pagpalya_VALUE("Code attribute size mismatch");
                } else 건너(haba_VALUE);
            }
            if ((pamamaraan_access[수] & 0x400) != 0) continue;
            if (pamamaraan_Start[수] == 0) pagpalya_VALUE("missing Code attribute");
            int espasyo_pagpasok = pamamaraan_Start[수];
            while (espasyo_pagpasok < pamamaraan_tapusin[수] && !error) {
                int haba_VALUE = 길이읽기(espasyo_pagpasok, pamamaraan_Start[수], pamamaraan_tapusin[수]);
                if (haba_VALUE == 0) { pagpalya_VALUE("unsupported or truncated bytecode"); break; }
                경계[espasyo_pagpasok] = 수 + 1; espasyo_pagpasok += haba_VALUE;
            }
            espasyo_pagpasok = pamamaraan_Start[수];
            while (espasyo_pagpasok < pamamaraan_tapusin[수] && !error) {
                int VALUE = file[espasyo_pagpasok];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) tseke_patutunguhan_VALUE(espasyo_pagpasok + (short)(file[espasyo_pagpasok + 1] << 8 | file[espasyo_pagpasok + 2]), 수);
                if (VALUE == 200) tseke_patutunguhan_VALUE(espasyo_pagpasok + posisyon_integer_buong_numero(espasyo_pagpasok + 1), 수);
                if (VALUE == 170 || VALUE == 171) {
                    int 읽는자리 = espasyo_pagpasok + 1; while ((읽는자리 - pamamaraan_Start[수]) % 4 != 0) 읽는자리++;
                    tseke_patutunguhan_VALUE(espasyo_pagpasok + posisyon_integer_buong_numero(읽는자리), 수);
                    int pagpasok_COUNT = VALUE == 170 ? posisyon_integer_buong_numero(읽는자리 + 8) - posisyon_integer_buong_numero(읽는자리 + 4) + 1 : posisyon_integer_buong_numero(읽는자리 + 4);
                    읽는자리 += VALUE == 170 ? 12 : 8;
                    for (int inner_join_posisyon = 0; inner_join_posisyon < pagpasok_COUNT; inner_join_posisyon++) tseke_patutunguhan_VALUE(espasyo_pagpasok + posisyon_integer_buong_numero(읽는자리 + inner_join_posisyon * (VALUE == 170 ? 4 : 8) + (VALUE == 170 ? 0 : 4)), 수);
                }
                espasyo_pagpasok += 길이읽기(espasyo_pagpasok, pamamaraan_Start[수], pamamaraan_tapusin[수]);
            }
            for (int inner_join_posisyon = 0; inner_join_posisyon < 잡기수; inner_join_posisyon++) if (잡기함수[inner_join_posisyon] == 수) {
                tseke_patutunguhan_VALUE(잡기시작[inner_join_posisyon], 수); tseke_patutunguhan_VALUE(잡기위치[inner_join_posisyon], 수);
                if (잡기끝[inner_join_posisyon] != pamamaraan_tapusin[수]) tseke_patutunguhan_VALUE(잡기끝[inner_join_posisyon], 수);
                if (잡기시작[inner_join_posisyon] >= 잡기끝[inner_join_posisyon]) pagpalya_VALUE("invalid exception range");
            }
        }
        if (!error) 속성건너();
        if (읽기위치 != sukat_82232621) pagpalya_VALUE("extra class file data");
    }
    static int maglaan_Storage(int 종류, int haba_VALUE) { return 새기억(종류, haba_VALUE); }
    static boolean bagay_VALUE(int Sanggunian, int 종류) {
        if (!객체유효(Sanggunian)) return false;
        if (힙[Sanggunian] != 종류) { pagpalya_VALUE("object type mismatch"); return false; }
        return true;
    }
    static int constant_SMS(int INDEX) {
        if (!tseke_constant(INDEX, 1)) return 0;
        if (string_Sanggunian[INDEX] != 0) return string_Sanggunian[INDEX];
        int Sanggunian = maglaan_Storage(1, constant_SECOND_VALUE[INDEX]); if (error) return 0;
        int 끝 = 상가[INDEX] + constant_SECOND_VALUE[INDEX], 수 = 상가[INDEX], haba_VALUE = 0;
        while (수 < 끝 && !error) {
            int VALUE = file[수++];
            if (VALUE == 0) pagpalya_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && 수 < 끝) {
                int Susunod_item = file[수++];
                if ((Susunod_item & 192) != 128) pagpalya_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | Susunod_item & 63;
                if (VALUE != 0 && VALUE < 128) pagpalya_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && 수 + 1 < 끝) {
                int 가 = file[수++], 나 = file[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) pagpalya_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (VALUE < 2048) pagpalya_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) pagpalya_VALUE("invalid modified UTF-8");
            힙[Sanggunian + 2 + haba_VALUE++] = VALUE;
        }
        힙[Sanggunian + 1] = haba_VALUE; string_Sanggunian[INDEX] = Sanggunian; return Sanggunian;
    }
    static int host_karakter(String VALUE) {
        int Sanggunian = maglaan_Storage(1, VALUE.length()); if (error) return 0;
        for (int 수 = 0; 수 < VALUE.length(); 수++) 힙[Sanggunian + 2 + 수] = VALUE.charAt(수);
        return Sanggunian;
    }
    static void sumulat_SMS(int Sanggunian) {
        if (Sanggunian == 0) { gumagamit.sumulat("null"); return; }
        if (!bagay_VALUE(Sanggunian, 1)) return;
        for (int 수 = 0; 수 < 힙[Sanggunian + 1]; 수++) gumagamit.sumulat_karakter_VALUE(힙[Sanggunian + 2 + 수]);
    }
    static int digit_karakter(int VALUE) {
        int Sanggunian = maglaan_Storage(1, 11); if (error) return 0;
        int haba_VALUE = 0;
        if (VALUE < 0) 힙[Sanggunian + 2 + haba_VALUE++] = '-'; else VALUE = -VALUE;
        int posisyon_INDEX = 1000000000; boolean run = false;
        while (posisyon_INDEX != 0) {
            int 수 = -(VALUE / posisyon_INDEX);
            if (수 != 0 || run || posisyon_INDEX == 1) { 힙[Sanggunian + 2 + haba_VALUE++] = '0' + 수; run = true; }
            VALUE %= posisyon_INDEX; posisyon_INDEX /= 10;
        }
        힙[Sanggunian + 1] = haba_VALUE; return Sanggunian;
    }
    static int 정수해독(int Sanggunian) {
        if (!bagay_VALUE(Sanggunian, 1)) return 0;
        int haba_VALUE = 힙[Sanggunian + 1], 수 = 0, VALUE = 0; boolean 음수 = false;
        if (haba_VALUE > 0 && (힙[Sanggunian + 2] == '-' || 힙[Sanggunian + 2] == '+')) { 음수 = 힙[Sanggunian + 2] == '-'; 수++; }
        if (수 == haba_VALUE) pagpalya_VALUE("NumberFormatException");
        for (; 수 < haba_VALUE && !error; 수++) {
            int digit_VALUE = 힙[Sanggunian + 2 + 수] - '0';
            if (digit_VALUE < 0 || digit_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && digit_VALUE > (음수 ? 8 : 7)) pagpalya_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - digit_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int TYPE_VALUE) {
        if (error) return;
        if (frame_INDEX < 0 || frame_Stack[frame_INDEX] >= pamamaraan_Stack[frame_pamamaraan[frame_INDEX]]) { pagpalya_VALUE("operand stack overflow"); return; }
        int espasyo_pagpasok = frame_INDEX * 128 + frame_Stack[frame_INDEX]++; 스택값[espasyo_pagpasok] = VALUE; 스택형[espasyo_pagpasok] = TYPE_VALUE;
    }
    static int 빼기(int TYPE_VALUE) {
        if (error) return 0;
        if (frame_INDEX < 0 || frame_Stack[frame_INDEX] < 1) { pagpalya_VALUE("operand stack underflow"); return 0; }
        int espasyo_pagpasok = frame_INDEX * 128 + --frame_Stack[frame_INDEX]; 반환형 = 스택형[espasyo_pagpasok];
        if (TYPE_VALUE != 0 && 반환형 != TYPE_VALUE) pagpalya_VALUE("operand type mismatch");
        if (반환형 == 2) magprotekta_VALUE(스택값[espasyo_pagpasok]);
        return 스택값[espasyo_pagpasok];
    }
    static void 지역읽기(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[frame_pamamaraan[frame_INDEX]] || INDEX < 0 || lokal_TYPE[frame_INDEX * 128 + INDEX] != TYPE_VALUE) { pagpalya_VALUE("invalid or uninitialized local"); return; }
        넣기(lokal_VALUE[frame_INDEX * 128 + INDEX], TYPE_VALUE);
    }
    static void sumulat_lokal(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[frame_pamamaraan[frame_INDEX]] || INDEX < 0) { pagpalya_VALUE("local index out of range"); return; }
        int VALUE = 빼기(TYPE_VALUE); lokal_VALUE[frame_INDEX * 128 + INDEX] = VALUE; lokal_TYPE[frame_INDEX * 128 + INDEX] = TYPE_VALUE;
    }
    static int 명바() {
        int posisyon = frame_posisyon[frame_INDEX];
        if (posisyon < pamamaraan_Start[frame_pamamaraan[frame_INDEX]] || posisyon >= pamamaraan_tapusin[frame_pamamaraan[frame_INDEX]]) { pagpalya_VALUE("instruction pointer out of range"); return 0; }
        frame_posisyon[frame_INDEX]++; return file[posisyon];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void ilipat_VALUE(int posisyon) {
        int pormula_VALUE = frame_pamamaraan[frame_INDEX];
        if (posisyon < pamamaraan_Start[pormula_VALUE] || posisyon >= pamamaraan_tapusin[pormula_VALUE] || 경계[posisyon] != pormula_VALUE + 1) pagpalya_VALUE("invalid branch target");
        else frame_posisyon[frame_INDEX] = posisyon;
    }
    static void 호출(int pormula_VALUE) {
        if (frame_INDEX % 32 == 31) { pagpalya_VALUE("call stack limit (32)"); return; }
        int Susunod_item = frame_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) lokal_TYPE[Susunod_item * 128 + 수] = 0;
        for (int 수 = pamamaraan_argumento_COUNT[pormula_VALUE] - 1; 수 >= 0; 수--) {
            lokal_VALUE[Susunod_item * 128 + 수] = 빼기(pamamaraan_argumento_TYPE[pormula_VALUE * 16 + 수]); lokal_TYPE[Susunod_item * 128 + 수] = pamamaraan_argumento_TYPE[pormula_VALUE * 16 + 수];
        }
        if (error) return;
        frame_INDEX = Susunod_item; magsimula_frame[frame_INDEX] = 0; frame_pamamaraan[frame_INDEX] = pormula_VALUE; frame_posisyon[frame_INDEX] = pamamaraan_Start[pormula_VALUE]; frame_Stack[frame_INDEX] = 0;
    }
    static void 반환(int TYPE_VALUE) {
        if (TYPE_VALUE != 함수반환[frame_pamamaraan[frame_INDEX]]) { pagpalya_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        if (magsimula_frame[frame_INDEX] != 0) kategorya_Kahulugan_katayuan[magsimula_frame[frame_INDEX] - 1] = 2;
        if (틀잠금[frame_INDEX] != 0) { 잠금풀기(틀잠금[frame_INDEX]); 틀잠금[frame_INDEX] = 0; }
        frame_INDEX--; if (frame_INDEX >= 현재가닥 * 32 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
    }
    static int[] Stream_file_pangalan = new int[64];
    static void file_Stream_CALL(int may_ari_VALUE, int pangalan, int format_VALUE, int utos) {
        boolean 출력 = Word_SMS(may_ari_VALUE, "java/io/FileOutputStream");
        int 종류 = 출력 ? 6 : 5;
        if (utos == 183 && Word_SMS(pangalan, "<init>")) {
            boolean 이어 = false;
            if (출력 && Word_SMS(format_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(format_VALUE, "(Ljava/lang/String;)V")) { pagpalya_VALUE("unsupported file stream constructor"); return; }
            int file_pagpasok_pangalan = 빼기(2), Stream_VALUE = 빼기(2);
            if (!bagay_VALUE(file_pagpasok_pangalan, 1) || !bagay_VALUE(Stream_VALUE, 종류) || error) return;
            if (힙[Stream_VALUE + 3] != 0) { pagpalya_VALUE("file stream already initialized"); return; }
            int haba_VALUE = 힙[file_pagpasok_pangalan + 1];
            if (haba_VALUE < 1 || haba_VALUE > 63) { pagpalya_VALUE("invalid file name length"); return; }
            for (int espasyo_pagpasok = 0; espasyo_pagpasok < haba_VALUE; espasyo_pagpasok++) {
                int VALUE = 힙[file_pagpasok_pangalan + 2 + espasyo_pagpasok];
                if (VALUE < 1) { pagpalya_VALUE("invalid file stream path"); return; }
                Stream_file_pangalan[espasyo_pagpasok] = VALUE;
            }
            Stream_file_pangalan[haba_VALUE] = 0;
            int 서술자 = gumagamit.파일서술자열기(Stream_file_pangalan, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { pagpalya_VALUE("FileNotFoundException: file open failed"); return; }
            힙[Stream_VALUE + 2] = 서술자; 힙[Stream_VALUE + 3] = 1;
            return;
        }
        if (utos != 182) { pagpalya_VALUE("invalid file stream invocation"); return; }
        if ((출력 && Word_SMS(pangalan, "write") || !출력 && Word_SMS(pangalan, "read"))
            && (Word_SMS(format_VALUE, 출력 ? "([B)V" : "([B)I") || Word_SMS(format_VALUE, 출력 ? "([BII)V" : "([BII)I"))) {
            boolean clip_VALUE = Word_SMS(format_VALUE, 출력 ? "([BII)V" : "([BII)I");
            int pagpasok_COUNT = clip_VALUE ? 빼기(1) : 0, 시작점 = clip_VALUE ? 빼기(1) : 0, data_ARRAY = 빼기(2), bagay_Sanggunian = 빼기(2);
            if (!bagay_VALUE(data_ARRAY, 20) || !bagay_VALUE(bagay_Sanggunian, 종류)) return;
            if (!clip_VALUE) pagpasok_COUNT = 힙[data_ARRAY + 1];
            if (시작점 < 0 || pagpasok_COUNT < 0 || 시작점 > 힙[data_ARRAY + 1] - pagpasok_COUNT) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[bagay_Sanggunian + 3] == 0 || 힙[bagay_Sanggunian + 2] < 0) { pagpalya_VALUE("IOException: stream closed"); return; }
            int 완료수 = 0;
            while (완료수 < pagpasok_COUNT && !error) {
                int 반환값 = 출력 ? gumagamit.파일한바이트쓰기(힙[bagay_Sanggunian + 2], 힙[data_ARRAY + 2 + 시작점 + 완료수]) : gumagamit.파일한바이트읽기(힙[bagay_Sanggunian + 2]);
                if (반환값 < 0) { pagpalya_VALUE(출력 ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!출력 && 반환값 == 256) break;
                if (!출력) 힙[data_ARRAY + 2 + 시작점 + 완료수] = (byte)반환값;
                완료수++;
            }
            if (!출력) 넣기(pagpasok_COUNT != 0 && 완료수 == 0 ? -1 : 완료수, 1);
            return;
        }
        if (출력 && Word_SMS(pangalan, "flush") && Word_SMS(format_VALUE, "()V")) { int bagay_Sanggunian = 빼기(2); if (bagay_VALUE(bagay_Sanggunian, 종류) && 힙[bagay_Sanggunian + 2] < 0) pagpalya_VALUE("IOException: stream closed"); return; }
        int aksyon = -1, VALUE = 0;
        if (Word_SMS(pangalan, "close") && Word_SMS(format_VALUE, "()V")) aksyon = 0;
        if (!출력 && Word_SMS(pangalan, "read") && Word_SMS(format_VALUE, "()I")) aksyon = 1;
        if (출력 && Word_SMS(pangalan, "write") && Word_SMS(format_VALUE, "(I)V")) { aksyon = 2; VALUE = 빼기(1); }
        if (aksyon < 0) { pagpalya_VALUE("unsupported file stream method"); return; }
        int Stream_VALUE = 빼기(2);
        if (!bagay_VALUE(Stream_VALUE, 종류) || error) return;
        if (힙[Stream_VALUE + 3] == 0) { pagpalya_VALUE("uninitialized file stream"); return; }
        int 서술자 = 힙[Stream_VALUE + 2];
        if (aksyon == 0) {
            if (서술자 >= 0 && gumagamit.파일서술자닫기(서술자) < 0) pagpalya_VALUE("IOException: close failed");
            힙[Stream_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { pagpalya_VALUE("IOException: stream closed"); return; }
        if (aksyon == 1) {
            int sukat = gumagamit.파일한바이트읽기(서술자);
            if (sukat < -1) pagpalya_VALUE("IOException: read failed"); else 넣기(sukat == 256 ? -1 : sukat, 1);
        } else if (gumagamit.파일한바이트쓰기(서술자, VALUE) != 1) pagpalya_VALUE("IOException: write failed");
    }
    static void CALL_pamamaraan(int INDEX, int utos) {
        if (INDEX <= 0 || INDEX >= constant_tag.length || (constant_tag[INDEX] != 10 && constant_tag[INDEX] != 11)) { pagpalya_VALUE("invalid method reference"); return; }
        int may_ari_VALUE = kategorya_pangalan_SMS(상가[INDEX]), pangalan = Sanggunian_pangalan(constant_SECOND_VALUE[INDEX]), format_VALUE = Sanggunian_TYPE(constant_SECOND_VALUE[INDEX]);
        if (error) return;
        if (기본호출(may_ari_VALUE, pangalan, format_VALUE, utos)) return;
        if (Word_SMS(may_ari_VALUE, "java/io/FileInputStream") || Word_SMS(may_ari_VALUE, "java/io/FileOutputStream")) {
            file_Stream_CALL(may_ari_VALUE, pangalan, format_VALUE, utos); return;
        }
        if (utos == 184 && Word_SMS(may_ari_VALUE, "java/lang/Integer") && Word_SMS(pangalan, "parseInt") && Word_SMS(format_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (utos == 182 && Word_SMS(may_ari_VALUE, "java/io/PrintStream") && (Word_SMS(pangalan, "println") || Word_SMS(pangalan, "print"))) {
            int TYPE_VALUE = 0, VALUE = 0;
            if (Word_SMS(format_VALUE, "(I)V")) { TYPE_VALUE = 1; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(Z)V")) { TYPE_VALUE = 2; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(C)V")) { TYPE_VALUE = 3; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(Ljava/lang/String;)V")) { TYPE_VALUE = 4; VALUE = 빼기(2); }
            else if (!Word_SMS(format_VALUE, "()V") || !Word_SMS(pangalan, "println")) pagpalya_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) pagpalya_VALUE("invalid PrintStream receiver");
            if (error) return;
            if (TYPE_VALUE == 1) 자바도구.수쓰기(VALUE);
            if (TYPE_VALUE == 2) gumagamit.sumulat(VALUE == 0 ? "false" : "true");
            if (TYPE_VALUE == 3) gumagamit.sumulat_karakter_VALUE(VALUE & 65535);
            if (TYPE_VALUE == 4) sumulat_SMS(VALUE);
            if (Word_SMS(pangalan, "println")) gumagamit.sumulat_karakter_VALUE(10);
            return;
        }
        if (utos == 182 && Word_SMS(may_ari_VALUE, "java/lang/String")) {
            if (Word_SMS(pangalan, "length") && Word_SMS(format_VALUE, "()I")) {
                int Sanggunian = 빼기(2); if (bagay_VALUE(Sanggunian, 1)) 넣기(힙[Sanggunian + 1], 1); return;
            }
            if (Word_SMS(pangalan, "charAt") && Word_SMS(format_VALUE, "(I)C")) {
                int subscript_VALUE = 빼기(1), Sanggunian = 빼기(2);
                if (bagay_VALUE(Sanggunian, 1)) {
                    if (subscript_VALUE < 0 || subscript_VALUE >= 힙[Sanggunian + 1]) pagpalya_VALUE("StringIndexOutOfBoundsException"); else 넣기(힙[Sanggunian + 2 + subscript_VALUE], 1);
                }
                return;
            }
        }
        if (Word_SMS(may_ari_VALUE, "java/lang/StringBuilder")) {
            if (utos == 183 && Word_SMS(pangalan, "<init>") && Word_SMS(format_VALUE, "()V")) { bagay_VALUE(빼기(2), 4); return; }
            if (utos == 182 && Word_SMS(pangalan, "toString") && Word_SMS(format_VALUE, "()Ljava/lang/String;")) {
                int Sanggunian = 빼기(2); if (bagay_VALUE(Sanggunian, 4)) 넣기(힙[Sanggunian + 2] == 0 ? host_karakter("") : 힙[Sanggunian + 2], 2); return;
            }
            if (utos == 182 && Word_SMS(pangalan, "append")) {
                int SMS = 0;
                if (Word_SMS(format_VALUE, "(I)Ljava/lang/StringBuilder;")) SMS = digit_karakter(빼기(1));
                else if (Word_SMS(format_VALUE, "(Z)Ljava/lang/StringBuilder;")) SMS = host_karakter(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(format_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); SMS = maglaan_Storage(1, 1); if (!error) 힙[SMS + 2] = VALUE & 65535;
                }
                else if (Word_SMS(format_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { SMS = 빼기(2); if (SMS == 0) SMS = host_karakter("null"); }
                else { pagpalya_VALUE("unsupported StringBuilder append"); return; }
                int Sanggunian = 빼기(2); if (!bagay_VALUE(Sanggunian, 4) || !bagay_VALUE(SMS, 1)) return;
                int nasa_harap_VALUE = 힙[Sanggunian + 2], nasa_harap_VALUE_haba = nasa_harap_VALUE == 0 ? 0 : 힙[nasa_harap_VALUE + 1], Bumalik_VALUE_haba = 힙[SMS + 1];
                int 새글 = maglaan_Storage(1, nasa_harap_VALUE_haba + Bumalik_VALUE_haba); if (error) return;
                for (int 수 = 0; 수 < nasa_harap_VALUE_haba; 수++) 힙[새글 + 2 + 수] = 힙[nasa_harap_VALUE + 2 + 수];
                for (int 수 = 0; 수 < Bumalik_VALUE_haba; 수++) 힙[새글 + 2 + nasa_harap_VALUE_haba + 수] = 힙[SMS + 2 + 수];
                힙[Sanggunian + 2] = 새글; 넣기(Sanggunian, 2); return;
            }
        }
        int kategorya_Kahulugan = FIND_kategorya_Kahulugan(may_ari_VALUE); if (kategorya_Kahulugan < 0 || error) return;
        int file_INDEX = FIND_pamamaraan(kategorya_Kahulugan, pangalan, format_VALUE);
        if (file_INDEX < 0) {
            for (int character_code = kategorya_Kahulugan, pagpasok_COUNT = 0; character_code >= 0 && pagpasok_COUNT < 16; pagpasok_COUNT++, character_code = 부모종(character_code))
                if (Word_SMS(종부모[character_code], "java/lang/Thread")) { 가닥호출(pangalan, format_VALUE, utos); return; }
            pagpalya_VALUE("NoSuchMethodError"); return;
        }
        if (((pamamaraan_access[file_INDEX] & 8) != 0) != (utos == 184)) { pagpalya_VALUE("method static/instance mismatch"); return; }
        if (utos == 184) { if (!magsimula(pamamaraan_may_ari[file_INDEX], frame_instruksiyon[frame_INDEX])) return; }
        else {
            int 읽는자리 = frame_Stack[frame_INDEX] - pamamaraan_argumento_COUNT[file_INDEX];
            if (읽는자리 < 0 || 스택형[frame_INDEX * 128 + 읽는자리] != 2) { pagpalya_VALUE("invalid method receiver"); return; }
            int bagay_Sanggunian = 스택값[frame_INDEX * 128 + 읽는자리];
            if (!객체유효(bagay_Sanggunian)) return;
            if (힙[bagay_Sanggunian] < 32 || !종포함(힙[bagay_Sanggunian] - 32, may_ari_VALUE)) { pagpalya_VALUE("method receiver type mismatch"); return; }
            if (utos != 183) file_INDEX = FIND_pamamaraan(힙[bagay_Sanggunian] - 32, pangalan, format_VALUE);
        }
        if (file_INDEX < 0 || (pamamaraan_access[file_INDEX] & 0x400) != 0) { pagpalya_VALUE("AbstractMethodError"); return; }
        int 잠금참조 = 0;
        if ((pamamaraan_access[file_INDEX] & 32) != 0) {
            if (utos == 184) { int character_code = pamamaraan_may_ari[file_INDEX]; if (종잠금[character_code] == 0) 종잠금[character_code] = maglaan_Storage(8, 0); 잠금참조 = 종잠금[character_code]; }
            else 잠금참조 = 스택값[frame_INDEX * 128 + frame_Stack[frame_INDEX] - pamamaraan_argumento_COUNT[file_INDEX]];
            if (!잠금얻기(잠금참조)) { if (!error) frame_posisyon[frame_INDEX] = frame_instruksiyon[frame_INDEX]; return; }
        }
        호출(file_INDEX); if (!error) 틀잠금[frame_INDEX] = 잠금참조;
    }
    static boolean 배열저장가능(int ARRAY_Sanggunian, int data_VALUE) {
        if (data_VALUE == 0 || ARRAY_elemento[ARRAY_Sanggunian] == 0) return true;
        boolean 성공여부 = ARRAY_elemento[ARRAY_Sanggunian] == -1 ? (data_VALUE > 0 && data_VALUE < 힙끝 && 힙[data_VALUE] == 1) : 맞는객체(data_VALUE, ARRAY_elemento[ARRAY_Sanggunian]);
        if (!성공여부 && !error) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int ARRAY_espasyo(int Sanggunian, int subscript_VALUE, int TYPE_VALUE) {
        if (!bagay_VALUE(Sanggunian, TYPE_VALUE)) return 0;
        if (subscript_VALUE < 0 || subscript_VALUE >= 힙[Sanggunian + 1]) { pagpalya_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return Sanggunian + 2 + subscript_VALUE;
    }
    static void Mag_execute_utos() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (error) { if (던진객체 != 0) hawakán_pagbubukod(); if (error || frame_INDEX < 현재가닥 * 32) break; }
            if (frame_INDEX < 현재가닥 * 32 || 바꿈요청 || --조각 == 0) { if (!SWITCH_thread()) break; 조각 = 100; }
            if (frame_INDEX == 0 && kategorya_Kahulugan_katayuan[pagpasok_kategorya_Kahulugan] != 2 && !magsimula(pagpasok_kategorya_Kahulugan, frame_posisyon[frame_INDEX])) continue;
            if (frame_INDEX == 현재가닥 * 32 && 현재가닥 != 0 && (pamamaraan_access[frame_pamamaraan[frame_INDEX]] & 32) != 0 && 틀잠금[frame_INDEX] == 0) {
                int bagay_Sanggunian = thread_target[현재가닥]; if (!잠금얻기(bagay_Sanggunian)) { if (error) break; continue; } 틀잠금[frame_INDEX] = bagay_Sanggunian;
            }
            잠시수 = 0;
            if (--남음 == 0) { pagpalya_VALUE("instruction limit (500000)"); break; }
            int run = frame_posisyon[frame_INDEX]; frame_instruksiyon[frame_INDEX] = run; int VALUE = 명바();
            if (error) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = pamamaraan_may_ari[frame_pamamaraan[frame_INDEX]] * 512 + (VALUE == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= constant_tag.length) pagpalya_VALUE("invalid ldc constant");
                else if (constant_tag[수] == 3) 넣기(상가[수], 1);
                else if (constant_tag[수] == 8) 넣기(constant_SMS(상가[수]), 2);
                else pagpalya_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { sumulat_lokal(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { sumulat_lokal(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { sumulat_lokal(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE >= 50 && VALUE <= 53) {
                int pagpasok_posisyon = 빼기(1), bagay_Sanggunian = 빼기(2), kategorya_CODE = VALUE == 46 ? 2 : VALUE == 50 ? 3 : VALUE == 51 ? 20 : VALUE == 52 ? 22 : 23;
                if (VALUE == 51 && bagay_Sanggunian > 0 && bagay_Sanggunian < 힙끝 && 힙[bagay_Sanggunian] == 21) kategorya_CODE = 21;
                int 읽는자리 = ARRAY_espasyo(bagay_Sanggunian, pagpasok_posisyon, kategorya_CODE); if (!error) 넣기(힙[읽는자리], VALUE == 50 ? 2 : 1); continue;
            }
            if (VALUE == 79 || VALUE >= 83 && VALUE <= 86) {
                int pagpasok_Sanggunian = 빼기(VALUE == 83 ? 2 : 1), pagpasok_posisyon = 빼기(1), bagay_Sanggunian = 빼기(2), kategorya_CODE = VALUE == 79 ? 2 : VALUE == 83 ? 3 : VALUE == 84 ? 20 : VALUE == 85 ? 22 : 23;
                if (VALUE == 84 && bagay_Sanggunian > 0 && bagay_Sanggunian < 힙끝 && 힙[bagay_Sanggunian] == 21) kategorya_CODE = 21;
                int 읽는자리 = ARRAY_espasyo(bagay_Sanggunian, pagpasok_posisyon, kategorya_CODE);
                if (!error && kategorya_CODE == 3 && !배열저장가능(bagay_Sanggunian, pagpasok_Sanggunian)) continue;
                if (!error) 힙[읽는자리] = kategorya_CODE == 20 ? (byte)pagpasok_Sanggunian : kategorya_CODE == 21 ? pagpasok_Sanggunian & 1 : kategorya_CODE == 22 ? (char)pagpasok_Sanggunian : kategorya_CODE == 23 ? (short)pagpasok_Sanggunian : pagpasok_Sanggunian;
                continue;
            }
            if (VALUE >= 87 && VALUE <= 95) { Stack_instruksiyon(VALUE); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), sukat = 0;
                if ((VALUE == 108 || VALUE == 112) && 나 == 0) { pagpalya_VALUE("ArithmeticException: / by zero"); continue; }
                if (VALUE == 96) sukat = 가 + 나;
                if (VALUE == 100) sukat = 가 - 나;
                if (VALUE == 104) sukat = 가 * 나;
                if (VALUE == 108) sukat = 가 / 나;
                if (VALUE == 112) sukat = 가 % 나;
                if (VALUE == 120) sukat = 가 << 나;
                if (VALUE == 122) sukat = 가 >> 나;
                if (VALUE == 124) sukat = 가 >>> 나;
                if (VALUE == 126) sukat = 가 & 나;
                if (VALUE == 128) sukat = 가 | 나;
                if (VALUE == 130) sukat = 가 ^ 나;
                넣기(sukat, 1); continue;
            }
            if (VALUE == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALUE == 132) {
                int lokal_lawak = 명바(), 증분 = (byte)명바(); 지역읽기(lokal_lawak, 1); 넣기(빼기(1) + 증분, 1); sumulat_lokal(lokal_lawak, 1); continue;
            }
            if (VALUE >= 145 && VALUE <= 147) {
                int 수 = 빼기(1); 넣기(VALUE == 145 ? (byte)수 : VALUE == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                int patutunguhan_VALUE = run + (short)명짧(); boolean 갈까 = VALUE == 167;
                if (VALUE >= 153 && VALUE <= 158) {
                    int 수 = 빼기(1); 갈까 = VALUE == 153 ? 수 == 0 : VALUE == 154 ? 수 != 0 : VALUE == 155 ? 수 < 0 : VALUE == 156 ? 수 >= 0 : VALUE == 157 ? 수 > 0 : 수 <= 0;
                } else if (VALUE >= 159 && VALUE <= 166) {
                    int 나 = 빼기(VALUE >= 165 ? 2 : 1), 가 = 빼기(VALUE >= 165 ? 2 : 1);
                    갈까 = VALUE == 159 || VALUE == 165 ? 가 == 나 : VALUE == 160 || VALUE == 166 ? 가 != 나 : VALUE == 161 ? 가 < 나 : VALUE == 162 ? 가 >= 나 : VALUE == 163 ? 가 > 나 : 가 <= 나;
                } else if (VALUE == 198 || VALUE == 199) { int 수 = 빼기(2); 갈까 = VALUE == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) ilipat_VALUE(patutunguhan_VALUE); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { 반환(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE >= 178 && VALUE <= 181) { 필드호출(명상수(), VALUE, run); continue; }
            if (VALUE >= 182 && VALUE <= 185) {
                int 부호값 = 명상수();
                if (VALUE == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { pagpalya_VALUE("invalid invokeinterface operands"); continue; } }
                CALL_pamamaraan(부호값, VALUE); continue;
            }
            if (VALUE == 187) { 새객체(kategorya_pangalan_SMS(명상수()), run); continue; }
            if (VALUE == 188 || VALUE == 189) {
                int kategorya_CODE = 3, component = 0;
                if (VALUE == 188) { int 임시값 = 명바(); kategorya_CODE = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else component = kategorya_pangalan_SMS(명상수());
                if (kategorya_CODE == 0) { pagpalya_VALUE("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), bagay_Sanggunian = maglaan_Storage(kategorya_CODE, 유효길이); if (!error) ARRAY_elemento[bagay_Sanggunian] = component; 넣기(bagay_Sanggunian, 2); continue;
            }
            if (VALUE == 190) {
                int bagay_Sanggunian = 빼기(2);
                if (객체유효(bagay_Sanggunian)) { int Paghahambing_posisyon = 힙[bagay_Sanggunian]; if (Paghahambing_posisyon != 2 && Paghahambing_posisyon != 3 && (Paghahambing_posisyon < 20 || Paghahambing_posisyon > 23)) pagpalya_VALUE("not an array"); else 넣기(힙[bagay_Sanggunian + 1], 1); }
                continue;
            }
            if (VALUE == 191) {
                int bagay_Sanggunian = 빼기(2); if (객체유효(bagay_Sanggunian)) { if (힙[bagay_Sanggunian] != 9) pagpalya_VALUE("athrow requires supported Throwable"); else { 던진객체 = bagay_Sanggunian; error = true; } }
                continue;
            }
            if (VALUE == 192 || VALUE == 193) {
                int pangalan_constant = kategorya_pangalan_SMS(명상수()), bagay_Sanggunian = 빼기(2); boolean MATCH = 맞는객체(bagay_Sanggunian, pangalan_constant);
                if (VALUE == 193) 넣기(bagay_Sanggunian != 0 && MATCH ? 1 : 0, 1);
                else { if (!MATCH && !error) pagpalya_VALUE("ClassCastException"); 넣기(bagay_Sanggunian, 2); }
                continue;
            }
            if (VALUE == 170 || VALUE == 171) {
                int 읽는자리 = run + 1, file_INDEX = frame_pamamaraan[frame_INDEX], key_Sanggunian = 빼기(1);
                while ((읽는자리 - pamamaraan_Start[file_INDEX]) % 4 != 0) 읽는자리++;
                int target_email = posisyon_integer_buong_numero(읽는자리);
                if (VALUE == 170) { int 낮은값 = posisyon_integer_buong_numero(읽는자리 + 4), 높은값 = posisyon_integer_buong_numero(읽는자리 + 8); if (key_Sanggunian >= 낮은값 && key_Sanggunian <= 높은값) target_email = posisyon_integer_buong_numero(읽는자리 + 12 + (key_Sanggunian - 낮은값) * 4); }
                else { int 총수 = posisyon_integer_buong_numero(읽는자리 + 4); for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) if (posisyon_integer_buong_numero(읽는자리 + 8 + Loop_INDEX * 8) == key_Sanggunian) target_email = posisyon_integer_buong_numero(읽는자리 + 12 + Loop_INDEX * 8); }
                ilipat_VALUE(run + target_email); continue;
            }
            if (VALUE == 200) { ilipat_VALUE(run + posisyon_integer_buong_numero(run + 1)); continue; }
            if (VALUE == 194 || VALUE == 195) {
                int bagay_Sanggunian = 빼기(2);
                if (VALUE == 195) 잠금풀기(bagay_Sanggunian);
                else if (!잠금얻기(bagay_Sanggunian) && !error) { 넣기(bagay_Sanggunian, 2); frame_posisyon[frame_INDEX] = run; }
                continue;
            }
            if (VALUE == 196) {
                int utos_CODE = 명바(), pagpasok_posisyon = 명짧();
                if (utos_CODE == 21 || utos_CODE == 25) 지역읽기(pagpasok_posisyon, utos_CODE == 21 ? 1 : 2);
                else if (utos_CODE == 54 || utos_CODE == 58) sumulat_lokal(pagpasok_posisyon, utos_CODE == 54 ? 1 : 2);
                else if (utos_CODE == 132) { int DELTA_VALUE = (short)명짧(); 지역읽기(pagpasok_posisyon, 1); 넣기(빼기(1) + DELTA_VALUE, 1); sumulat_lokal(pagpasok_posisyon, 1); }
                else pagpalya_VALUE("unsupported wide opcode");
                continue;
            }
            pagpalya_VALUE("unsupported bytecode");
        }
    }
    static int FIND_kategorya_Kahulugan(int pangalan) {
        for (int Loop_INDEX = 0; Loop_INDEX < kategorya_Kahulugan_COUNT; Loop_INDEX++) if (kategorya_Kahulugan_pangalan[Loop_INDEX] != 0 && 같은말(kategorya_Kahulugan_pangalan[Loop_INDEX], pangalan)) return Loop_INDEX;
        return load_kategorya_Kahulugan(constant_SMS(pangalan));
    }
    static int load_kategorya_Kahulugan(int pangalan_string) {
        if (!bagay_VALUE(pangalan_string, 1)) return -1;
        int haba_VALUE = 힙[pangalan_string + 1];
        if (haba_VALUE < 1 || haba_VALUE > 505 || kategorya_Kahulugan_COUNT == 16) { pagpalya_VALUE("class name/count limit"); return -1; }
        for (int Loop_INDEX = 0; Loop_INDEX < haba_VALUE; Loop_INDEX++) { int character_code = 힙[pangalan_string + 2 + Loop_INDEX]; file_pangalan_SMS[Loop_INDEX] = character_code == '/' ? '.' : character_code; }
        file_pangalan_SMS[haba_VALUE] = '.'; file_pangalan_SMS[haba_VALUE + 1] = 'c'; file_pangalan_SMS[haba_VALUE + 2] = 'l'; file_pangalan_SMS[haba_VALUE + 3] = 'a'; file_pangalan_SMS[haba_VALUE + 4] = 's'; file_pangalan_SMS[haba_VALUE + 5] = 's'; file_pangalan_SMS[haba_VALUE + 6] = 0;
        int sukat_82232621 = gumagamit.파일읽기(file_pangalan_SMS, 임시파일);
        if (sukat_82232621 < 0) { pagpalya_VALUE("ClassNotFoundException"); return -1; }
        int kategorya_Kahulugan = kategorya_Kahulugan_COUNT++; kategorya_Kahulugan_sukat[kategorya_Kahulugan] = sukat_82232621;
        for (int Loop_INDEX = 0; Loop_INDEX < sukat_82232621; Loop_INDEX++) file[kategorya_Kahulugan * 16384 + Loop_INDEX] = 임시파일[Loop_INDEX];
        클래스읽기(kategorya_Kahulugan); if (error) return -1;
        int totoo_data = constant_SMS(kategorya_Kahulugan_pangalan[kategorya_Kahulugan]);
        if (!글같음(totoo_data, pangalan_string, true)) { pagpalya_VALUE("class name does not match file"); return -1; }
        int 부모 = 종부모[kategorya_Kahulugan];
        if (부모 != 0 && !Word_SMS(부모, "java/lang/Object") && !Word_SMS(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = FIND_kategorya_Kahulugan(부모);
            if (error || 위 < 0) return -1;
            int 읽는자리 = 위, stage_COUNT = 0;
            while (읽는자리 >= 0 && stage_COUNT++ < 16) {
                if (읽는자리 == kategorya_Kahulugan) { pagpalya_VALUE("cyclic inheritance"); return -1; }
                읽는자리 = 부모종(읽는자리);
            }
            int 시작변위 = kategorya_espasyo_COUNT[위];
            for (int file_INDEX = 0; file_INDEX < espasyo_COUNT; file_INDEX++) if (espasyo_may_ari[file_INDEX] == kategorya_Kahulugan && (espasyo_Mga_Pahintulot[file_INDEX] & 8) == 0) espasyo_posisyon[file_INDEX] += 시작변위;
            kategorya_espasyo_COUNT[kategorya_Kahulugan] += 시작변위;
        }
        return kategorya_Kahulugan;
    }
    static int 부모종(int kategorya_Kahulugan) {
        int pangalan = 종부모[kategorya_Kahulugan];
        for (int Loop_INDEX = 0; Loop_INDEX < kategorya_Kahulugan_COUNT; Loop_INDEX++) if (pangalan != 0 && kategorya_Kahulugan_pangalan[Loop_INDEX] != 0 && 같은말(kategorya_Kahulugan_pangalan[Loop_INDEX], pangalan)) return Loop_INDEX;
        return -1;
    }
    static int FIND_pamamaraan(int kategorya_Kahulugan, int pangalan, int format_VALUE) {
        for (int 깊이 = 0; kategorya_Kahulugan >= 0 && 깊이 < 16; 깊이++, kategorya_Kahulugan = 부모종(kategorya_Kahulugan)) {
            for (int Loop_INDEX = 0; Loop_INDEX < pamamaraan_COUNT; Loop_INDEX++) if (pamamaraan_may_ari[Loop_INDEX] == kategorya_Kahulugan && 같은말(pamamaraan_pangalan_SMS[Loop_INDEX], pangalan) && 같은말(pamamaraan_TYPE[Loop_INDEX], format_VALUE)) return Loop_INDEX;
        }
        return -1;
    }
    static int pangalan_pamamaraan(int kategorya_Kahulugan, String pangalan, String format_VALUE) {
        for (int 깊이 = 0; kategorya_Kahulugan >= 0 && 깊이 < 16; 깊이++, kategorya_Kahulugan = 부모종(kategorya_Kahulugan))
            for (int Loop_INDEX = 0; Loop_INDEX < pamamaraan_COUNT; Loop_INDEX++) if (pamamaraan_may_ari[Loop_INDEX] == kategorya_Kahulugan && Word_SMS(pamamaraan_pangalan_SMS[Loop_INDEX], pangalan) && Word_SMS(pamamaraan_TYPE[Loop_INDEX], format_VALUE)) return Loop_INDEX;
        return -1;
    }
    static int 형종류(int pangalan) { return file[상가[pangalan]] == 'L' || file[상가[pangalan]] == '[' ? 2 : 1; }
    static boolean magsimula(int kategorya_Kahulugan, int utos_Start) {
        if (kategorya_Kahulugan < 0 || error) return false;
        if (kategorya_Kahulugan_katayuan[kategorya_Kahulugan] == 3) { pagpalya_VALUE("NoClassDefFoundError: initialization failed"); return false; }
        if (kategorya_Kahulugan_katayuan[kategorya_Kahulugan] == 1 && kategorya_thread[kategorya_Kahulugan] != 현재가닥) { frame_posisyon[frame_INDEX] = utos_Start; 바꿈요청 = true; return false; }
        if (kategorya_Kahulugan_katayuan[kategorya_Kahulugan] != 0) return true;
        int 위 = 부모종(kategorya_Kahulugan);
        if (위 >= 0 && !magsimula(위, utos_Start)) return false;
        kategorya_Kahulugan_katayuan[kategorya_Kahulugan] = 1; kategorya_thread[kategorya_Kahulugan] = 현재가닥;
        if (magsimula_kategorya_Kahulugan[kategorya_Kahulugan] != 0) {
            frame_posisyon[frame_INDEX] = utos_Start;
            호출(magsimula_kategorya_Kahulugan[kategorya_Kahulugan] - 1); if (!error) magsimula_frame[frame_INDEX] = kategorya_Kahulugan + 1;
            return false;
        }
        kategorya_Kahulugan_katayuan[kategorya_Kahulugan] = 2; return true;
    }
    static void 필드호출(int INDEX, int utos, int run) {
        if (!tseke_constant(INDEX, 9)) return;
        int may_ari_VALUE = kategorya_pangalan_SMS(상가[INDEX]), pangalan = Sanggunian_pangalan(constant_SECOND_VALUE[INDEX]), format_VALUE = Sanggunian_TYPE(constant_SECOND_VALUE[INDEX]);
        if (Word_SMS(may_ari_VALUE, "java/lang/System") && (Word_SMS(pangalan, "out") || Word_SMS(pangalan, "err")) && Word_SMS(format_VALUE, "Ljava/io/PrintStream;") && utos == 178) { 넣기(-1, 2); return; }
        int kategorya_Kahulugan = FIND_kategorya_Kahulugan(may_ari_VALUE); if (kategorya_Kahulugan < 0 || error) return;
        int 찾음 = -1;
        for (int 읽는자리 = kategorya_Kahulugan, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = 부모종(읽는자리))
            for (int file_INDEX = 0; file_INDEX < espasyo_COUNT; file_INDEX++) if (espasyo_may_ari[file_INDEX] == 읽는자리 && 같은말(espasyo_pangalan[file_INDEX], pangalan) && 같은말(espasyo_TYPE[file_INDEX], format_VALUE)) 찾음 = file_INDEX;
        if (찾음 < 0) { pagpalya_VALUE("NoSuchFieldError"); return; }
        boolean hindi_nababago_VALUE = utos == 178 || utos == 179;
        if (hindi_nababago_VALUE != ((espasyo_Mga_Pahintulot[찾음] & 8) != 0)) { pagpalya_VALUE("field static/instance mismatch"); return; }
        if (hindi_nababago_VALUE && !magsimula(espasyo_may_ari[찾음], run)) return;
        int TYPE_VALUE = 형종류(format_VALUE), VALUE = 0;
        if (utos == 179 || utos == 181) VALUE = 빼기(TYPE_VALUE);
        if (hindi_nababago_VALUE) { if (utos == 178) 넣기(espasyo_data[찾음], TYPE_VALUE); else if (!error) espasyo_data[찾음] = VALUE; return; }
        int bagay_Sanggunian = 빼기(2);
        if (!객체유효(bagay_Sanggunian)) return;
        if (힙[bagay_Sanggunian] < 32 || !종포함(힙[bagay_Sanggunian] - 32, may_ari_VALUE)) { pagpalya_VALUE("field receiver type mismatch"); return; }
        int 보관칸 = bagay_Sanggunian + 2 + espasyo_posisyon[찾음];
        if (utos == 180) 넣기(힙[보관칸], TYPE_VALUE);
        else if (!error) { 힙[보관칸] = VALUE; 힙참조[보관칸] = TYPE_VALUE == 2 ? 1 : 0; }
    }
    static boolean 종포함(int kategorya_Kahulugan, int pangalan) {
        for (int 중첩깊이 = 0; kategorya_Kahulugan >= 0 && 중첩깊이 < 16; 중첩깊이++, kategorya_Kahulugan = 부모종(kategorya_Kahulugan)) {
            if (같은말(kategorya_Kahulugan_pangalan[kategorya_Kahulugan], pangalan) || (종부모[kategorya_Kahulugan] != 0 && 같은말(종부모[kategorya_Kahulugan], pangalan))) return true;
            for (int inner_join_posisyon = 0; inner_join_posisyon < kategorya_interface_COUNT[kategorya_Kahulugan]; inner_join_posisyon++) if (같은말(kategorya_interface[kategorya_Kahulugan * 16 + inner_join_posisyon], pangalan)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int byte_data, boolean path) {
        if (첫값 == byte_data) return true;
        if (첫값 <= 0 || byte_data <= 0 || 힙[첫값] != 1 || 힙[byte_data] != 1 || 힙[첫값 + 1] != 힙[byte_data + 1]) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) {
            int x_coordinate = 힙[첫값 + 2 + Loop_INDEX], Y_button_coordinate = 힙[byte_data + 2 + Loop_INDEX];
            if (path) { if (x_coordinate == '.') x_coordinate = '/'; if (Y_button_coordinate == '.') Y_button_coordinate = '/'; }
            if (x_coordinate != Y_button_coordinate) return false;
        }
        return true;
    }
    static boolean 객체유효(int bagay_Sanggunian) {
        if (bagay_Sanggunian == 0) { pagpalya_VALUE("NullPointerException"); return false; }
        if (bagay_Sanggunian < 1 || bagay_Sanggunian >= 힙끝 || 힙폭[bagay_Sanggunian] < 2 || 힙[bagay_Sanggunian] == 0) { pagpalya_VALUE("invalid object reference"); return false; }
        return true;
    }
    static void magprotekta_VALUE(int bagay_Sanggunian) {
        if (bagay_Sanggunian > 0 && bagay_Sanggunian < 힙끝 && 힙폭[bagay_Sanggunian] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = bagay_Sanggunian;
    }
    static void ipakita_VALUE(int bagay_Sanggunian) {
        if (bagay_Sanggunian > 0 && bagay_Sanggunian < 힙끝 && 힙폭[bagay_Sanggunian] >= 2 && 힙[bagay_Sanggunian] != 0 && 힙표시[bagay_Sanggunian] == 0) {
            힙표시[bagay_Sanggunian] = 1; 표시대기[display_COUNT++] = bagay_Sanggunian;
        }
    }
    static void 수거() {
        display_COUNT = 0; Koleksyon_COUNT++;
        for (int tseke_posisyon = 1; tseke_posisyon < 힙끝; tseke_posisyon += 힙폭[tseke_posisyon]) 힙표시[tseke_posisyon] = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < string_Sanggunian.length; Loop_INDEX++) ipakita_VALUE(string_Sanggunian[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < espasyo_COUNT; Loop_INDEX++) if ((espasyo_Mga_Pahintulot[Loop_INDEX] & 8) != 0 && 형종류(espasyo_TYPE[Loop_INDEX]) == 2) ipakita_VALUE(espasyo_data[Loop_INDEX]);
        for (int 임시값 = 0; 임시값 < thread_COUNT; 임시값++) {
            ipakita_VALUE(thread_bagay[임시값]); ipakita_VALUE(thread_target[임시값]);
            int 꼭대기자리 = 임시값 == 현재가닥 ? frame_INDEX : thread_frame[임시값];
            for (int file_INDEX = 임시값 * 32; file_INDEX <= 꼭대기자리; file_INDEX++) {
                for (int inner_join_posisyon = 0; inner_join_posisyon < 함수지역[frame_pamamaraan[file_INDEX]]; inner_join_posisyon++) if (lokal_TYPE[file_INDEX * 128 + inner_join_posisyon] == 2) ipakita_VALUE(lokal_VALUE[file_INDEX * 128 + inner_join_posisyon]);
                for (int inner_join_posisyon = 0; inner_join_posisyon < frame_Stack[file_INDEX]; inner_join_posisyon++) if (스택형[file_INDEX * 128 + inner_join_posisyon] == 2) ipakita_VALUE(스택값[file_INDEX * 128 + inner_join_posisyon]);
            }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 화면참조.length; Loop_INDEX++) ipakita_VALUE(화면참조[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 나중수; Loop_INDEX++) ipakita_VALUE(나중실행[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Store_integer_buong_numero.length; Loop_INDEX++) ipakita_VALUE(Store_integer_buong_numero[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < kategorya_Kahulugan_COUNT; Loop_INDEX++) ipakita_VALUE(종잠금[Loop_INDEX]);
        for (int tseke_posisyon = 1; tseke_posisyon < 힙끝; tseke_posisyon += 힙폭[tseke_posisyon]) if (잠금깊이[tseke_posisyon] > 0) ipakita_VALUE(tseke_posisyon);
        ipakita_VALUE(던진객체);
        for (int Loop_INDEX = 0; Loop_INDEX < 잠시수; Loop_INDEX++) ipakita_VALUE(잠시참조[Loop_INDEX]);
        while (display_COUNT > 0) {
            int bagay_Sanggunian = 표시대기[--display_COUNT], kategorya_CODE = 힙[bagay_Sanggunian];
            for (int Loop_INDEX = bagay_Sanggunian + 2; Loop_INDEX < bagay_Sanggunian + 힙폭[bagay_Sanggunian]; Loop_INDEX++) if (kategorya_CODE == 3 || kategorya_CODE == 4 || 힙참조[Loop_INDEX] != 0) ipakita_VALUE(힙[Loop_INDEX]);
        }
        for (int tseke_posisyon = 1; tseke_posisyon < 힙끝; tseke_posisyon += 힙폭[tseke_posisyon]) if (힙표시[tseke_posisyon] == 0) 힙[tseke_posisyon] = 0;
        for (int tseke_posisyon = 1; tseke_posisyon < 힙끝; tseke_posisyon += 힙폭[tseke_posisyon]) if (힙[tseke_posisyon] == 0) {
            while (tseke_posisyon + 힙폭[tseke_posisyon] < 힙끝 && 힙[tseke_posisyon + 힙폭[tseke_posisyon]] == 0) { int Susunod_posisyon = tseke_posisyon + 힙폭[tseke_posisyon]; 힙폭[tseke_posisyon] += 힙폭[Susunod_posisyon]; 힙폭[Susunod_posisyon] = 0; }
            if (tseke_posisyon + 힙폭[tseke_posisyon] == 힙끝) { 힙끝 = tseke_posisyon; break; }
        }
    }
    static int 새기억(int 종류, int haba_VALUE) {
        if (haba_VALUE < 0) { pagpalya_VALUE("NegativeArraySizeException"); return 0; }
        if (haba_VALUE > 힙.length - 3) { pagpalya_VALUE("object heap exhausted"); return 0; }
        int 필요수 = haba_VALUE + 2, bagay_Sanggunian = 0;
        if (필요수 <= 힙.length - 힙끝) { bagay_Sanggunian = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { bagay_Sanggunian = 읽는자리; break; }
            if (bagay_Sanggunian != 0) {
                int 남은길이 = 힙폭[bagay_Sanggunian] - 필요수;
                if (남은길이 >= 2) { 힙폭[bagay_Sanggunian + 필요수] = 남은길이; 힙[bagay_Sanggunian + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { bagay_Sanggunian = 힙끝; 힙끝 += 필요수; }
        }
        if (bagay_Sanggunian == 0) { pagpalya_VALUE("object heap exhausted"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < 필요수; Loop_INDEX++) { 힙[bagay_Sanggunian + Loop_INDEX] = 0; 힙참조[bagay_Sanggunian + Loop_INDEX] = 0; 힙폭[bagay_Sanggunian + Loop_INDEX] = 0; }
        ARRAY_elemento[bagay_Sanggunian] = 0;
        힙폭[bagay_Sanggunian] = 필요수; 힙[bagay_Sanggunian] = 종류; 힙[bagay_Sanggunian + 1] = haba_VALUE; magprotekta_VALUE(bagay_Sanggunian); return bagay_Sanggunian;
    }
    static int pagbubukod_kategorya_6be6071e(String pangalan_constant) {
        if (자바도구.같음(pangalan_constant, "java/lang/Throwable")) return 1;
        if (자바도구.같음(pangalan_constant, "java/lang/Exception")) return 2;
        if (자바도구.같음(pangalan_constant, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(pangalan_constant, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(pangalan_constant, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(pangalan_constant, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(pangalan_constant, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(pangalan_constant, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(pangalan_constant, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(pangalan_constant, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(pangalan_constant, "java/io/IOException")) return 11;
        if (자바도구.같음(pangalan_constant, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(pangalan_constant, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(pangalan_constant, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(pangalan_constant, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int pagbubukod_constant(int pangalan) {
        for (int Loop_INDEX = 1; Loop_INDEX <= 41; Loop_INDEX++) if (Word_SMS(pangalan, pagbubukod_pangalan(Loop_INDEX))) return Loop_INDEX;
        return 0;
    }
    static String pagbubukod_pangalan(int account_VALUE) {
        if (account_VALUE == 40) return "java/lang/InterruptedException";
        if (account_VALUE == 41) return "한국어/자체/대기중단예외";
        if (account_VALUE == 39) return "java/net/SocketException";
        if (account_VALUE == 20) return "한국어/자체/pagbubukod";
        if (account_VALUE == 21) return "한국어/자체/실행예외";
        if (account_VALUE == 22) return "한국어/자체/I_O_pagbubukod";
        if (account_VALUE == 23) return "한국어/자체/maghintay_TIMEOUT_pagbubukod";
        if (account_VALUE == 24) return "한국어/자체/email_LOOKUP_pagbubukod";
        if (account_VALUE == 25) return "한국어/자체/파일없음예외";
        if (account_VALUE == 26) return "한국어/자체/통신예외";
        if (account_VALUE == 27) return "한국어/자체/hindi_tama_argumento_pagbubukod";
        if (account_VALUE == 28) return "한국어/자체/숫자형식예외";
        if (account_VALUE == 29) return "한국어/자체/범위예외";
        if (account_VALUE == 30) return "한국어/자체/배열범위예외";
        if (account_VALUE == 31) return "한국어/자체/문자열범위예외";
        if (account_VALUE == 32) return "한국어/자체/NULL_Sanggunian_pagbubukod";
        if (account_VALUE == 33) return "한국어/자체/산술예외";
        if (account_VALUE == 34) return "한국어/자체/katayuan_pagbubukod";
        if (account_VALUE == 35) return "한국어/자체/TYPE_Cast_pagbubukod";
        if (account_VALUE == 36) return "한국어/자체/음수배열크기예외";
        if (account_VALUE == 37) return "한국어/자체/ARRAY_Store_pagpalya";
        if (account_VALUE == 38) return "한국어/자체/thread_katayuan_pagbubukod";
        if (account_VALUE == 1) return "java/lang/Throwable"; if (account_VALUE == 2) return "java/lang/Exception";
        if (account_VALUE == 3) return "java/lang/RuntimeException"; if (account_VALUE == 4) return "java/lang/ArithmeticException";
        if (account_VALUE == 5) return "java/lang/NullPointerException"; if (account_VALUE == 6) return "java/lang/IndexOutOfBoundsException";
        if (account_VALUE == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (account_VALUE == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (account_VALUE == 9) return "java/lang/IllegalArgumentException"; if (account_VALUE == 10) return "java/lang/NumberFormatException";
        if (account_VALUE == 11) return "java/io/IOException"; if (account_VALUE == 12) return "java/io/FileNotFoundException";
        if (account_VALUE == 17) return "java/lang/ArrayStoreException";
        if (account_VALUE == 18) return "java/net/UnknownHostException";
        if (account_VALUE == 19) return "java/net/SocketTimeoutException";
        if (account_VALUE == 16) return "java/lang/IllegalThreadStateException";
        if (account_VALUE == 13) return "java/lang/IllegalStateException"; if (account_VALUE == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int account_VALUE) {
        if (account_VALUE == 40) return 2;
        if (account_VALUE == 41) return 40;
        if (account_VALUE == 39) return 11;
        if (account_VALUE == 1) return 0;
        if (account_VALUE == 2) return 1;
        if (account_VALUE == 3) return 2;
        if (account_VALUE == 4) return 3;
        if (account_VALUE == 5) return 3;
        if (account_VALUE == 6) return 3;
        if (account_VALUE == 7) return 6;
        if (account_VALUE == 8) return 6;
        if (account_VALUE == 9) return 3;
        if (account_VALUE == 10) return 9;
        if (account_VALUE == 11) return 2;
        if (account_VALUE == 12) return 11;
        if (account_VALUE == 13) return 3;
        if (account_VALUE == 14) return 3;
        if (account_VALUE == 15) return 3;
        if (account_VALUE == 16) return 9;
        if (account_VALUE == 17) return 3;
        if (account_VALUE == 18) return 11;
        if (account_VALUE == 19) return 11;
        if (account_VALUE == 20) return 2;
        if (account_VALUE == 21) return 3;
        if (account_VALUE == 22) return 11;
        if (account_VALUE == 23) return 22;
        if (account_VALUE == 24) return 22;
        if (account_VALUE == 25) return 22;
        if (account_VALUE == 26) return 22;
        if (account_VALUE == 27) return 9;
        if (account_VALUE == 28) return 27;
        if (account_VALUE == 29) return 6;
        if (account_VALUE == 30) return 29;
        if (account_VALUE == 31) return 29;
        if (account_VALUE == 32) return 5;
        if (account_VALUE == 33) return 4;
        if (account_VALUE == 34) return 13;
        if (account_VALUE == 35) return 14;
        if (account_VALUE == 36) return 15;
        if (account_VALUE == 37) return 17;
        if (account_VALUE == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int totoo_VALUE, int 요구값) {
        for (int 깊이 = 0; totoo_VALUE != 0 && 깊이 < 16; 깊이++, totoo_VALUE = 예외부모(totoo_VALUE))
            if (totoo_VALUE == 요구값) return true;
        return false;
    }
    static void 예외던짐(int account_VALUE, String BASAHINAKO_Sanggunian) {
        int bagay_Sanggunian = 새기억(9, 2); if (error) return;
        힙[bagay_Sanggunian + 2] = account_VALUE; 힙[bagay_Sanggunian + 3] = host_karakter(BASAHINAKO_Sanggunian); 힙참조[bagay_Sanggunian + 3] = 1;
        던진객체 = bagay_Sanggunian; error = true;
    }
    static boolean 맞는객체(int bagay_Sanggunian, int pangalan) {
        if (bagay_Sanggunian == 0) return true;
        if (!객체유효(bagay_Sanggunian)) return false;
        int kategorya_CODE = 힙[bagay_Sanggunian];
        if (Word_SMS(pangalan, "java/lang/Object")) return true;
        if (kategorya_CODE >= 32) return 종포함(kategorya_CODE - 32, pangalan);
        if (kategorya_CODE == 9) { int target_email = pagbubukod_constant(pangalan); return target_email != 0 && 예외포함(힙[bagay_Sanggunian + 2], target_email); }
        if (kategorya_CODE == 1) return Word_SMS(pangalan, "java/lang/String") || Word_SMS(pangalan, "java/lang/CharSequence");
        if (kategorya_CODE == 4) return Word_SMS(pangalan, "java/lang/StringBuilder") || Word_SMS(pangalan, "java/lang/CharSequence");
        if (kategorya_CODE == 10) return Word_SMS(pangalan, "java/util/ArrayList") || Word_SMS(pangalan, "java/util/List");
        if (kategorya_CODE == 11) return Word_SMS(pangalan, "java/util/HashMap") || Word_SMS(pangalan, "java/util/Map");
        if (kategorya_CODE == 12) return Word_SMS(pangalan, "java/lang/Integer") || Word_SMS(pangalan, "java/lang/Number");
        if (kategorya_CODE >= 24 && kategorya_CODE <= 28 && 힙[bagay_Sanggunian + 13] != 0) return 한국어화면종(pangalan) == kategorya_CODE || Word_SMS(pangalan, "한국어/자체/화면구성요소");
        if (kategorya_CODE >= 24 && kategorya_CODE <= 28) return (한국어화면종(pangalan) == 0 && 화면종(pangalan) == kategorya_CODE) || Word_SMS(pangalan, "java/awt/Component") || Word_SMS(pangalan, "java/awt/Container") || Word_SMS(pangalan, "javax/swing/JComponent");
        if (kategorya_CODE == 29) return Word_SMS(pangalan, 힙[bagay_Sanggunian + 3] != 0 ? "한국어/자체/동작알림" : "java/awt/event/ActionEvent");
        if (kategorya_CODE == 30) return Word_SMS(pangalan, "java/awt/FlowLayout") || Word_SMS(pangalan, "java/awt/LayoutManager");
        if (kategorya_CODE == 17) return Word_SMS(pangalan, "java/net/Socket");
        if (kategorya_CODE == 18) return Word_SMS(pangalan, "java/net/ServerSocket");
        if (kategorya_CODE == 19) return Word_SMS(pangalan, 힙[bagay_Sanggunian + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (kategorya_CODE == 14) return Word_SMS(pangalan, "java/net/InetAddress");
        if (kategorya_CODE == 15) return Word_SMS(pangalan, "java/net/DatagramSocket");
        if (kategorya_CODE == 16) return Word_SMS(pangalan, "java/net/DatagramPacket");
        if (kategorya_CODE == 13) return Word_SMS(pangalan, 힙[bagay_Sanggunian + 3] != 0 ? "한국어/자체/작업가닥" : "java/lang/Thread");
        if (kategorya_CODE == 2) return Word_SMS(pangalan, "[I"); if (kategorya_CODE == 20) return Word_SMS(pangalan, "[B"); if (kategorya_CODE == 21) return Word_SMS(pangalan, "[Z");
        if (kategorya_CODE == 22) return Word_SMS(pangalan, "[C"); if (kategorya_CODE == 23) return Word_SMS(pangalan, "[S");
        if (kategorya_CODE != 3) return false;
        if (Word_SMS(pangalan, "[Ljava/lang/Object;")) return true;
        int component = ARRAY_elemento[bagay_Sanggunian];
        if (component == -1) return Word_SMS(pangalan, "[Ljava/lang/String;") || Word_SMS(pangalan, "[Ljava/lang/CharSequence;");
        if (component == 0) return false;
        if (배열종비교(component, pangalan)) return true;
        if ((Word_SMS(component, "java/lang/String") || Word_SMS(component, "java/lang/StringBuilder")) && Word_SMS(pangalan, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDEX = 0; Loop_INDEX < kategorya_Kahulugan_COUNT; Loop_INDEX++) if (같은말(kategorya_Kahulugan_pangalan[Loop_INDEX], component)) {
            for (int character_code = Loop_INDEX, 중첩깊이 = 0; character_code >= 0 && 중첩깊이 < 16; 중첩깊이++, character_code = 부모종(character_code)) {
                if (배열종비교(종부모[character_code], pangalan)) return true;
                for (int inner_join_posisyon = 0; inner_join_posisyon < kategorya_interface_COUNT[character_code]; inner_join_posisyon++) if (배열종비교(kategorya_interface[character_code * 16 + inner_join_posisyon], pangalan)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int pangalan_constant, int 형식참조) {
        int tseke_posisyon = 상가[형식참조], pagpasok_COUNT = constant_SECOND_VALUE[형식참조];
        if (pangalan_constant == 0 || pagpasok_COUNT < 4 || file[tseke_posisyon] != '[' || file[tseke_posisyon + 1] != 'L' || file[tseke_posisyon + pagpasok_COUNT - 1] != ';' || constant_SECOND_VALUE[pangalan_constant] != pagpasok_COUNT - 3) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < pagpasok_COUNT - 3; Loop_INDEX++) if (file[상가[pangalan_constant] + Loop_INDEX] != file[tseke_posisyon + 2 + Loop_INDEX]) return false;
        return true;
    }
    static void hawakán_pagbubukod() {
        if (던진객체 == 0) return;
        error = false;
        while (frame_INDEX >= 현재가닥 * 32) {
            int file_INDEX = frame_pamamaraan[frame_INDEX], 읽는자리 = frame_instruksiyon[frame_INDEX];
            for (int Loop_INDEX = 0; Loop_INDEX < 잡기수; Loop_INDEX++) if (잡기함수[Loop_INDEX] == file_INDEX && 읽는자리 >= 잡기시작[Loop_INDEX] && 읽는자리 < 잡기끝[Loop_INDEX]
                && (잡기종[Loop_INDEX] == 0 || 맞는객체(던진객체, 잡기종[Loop_INDEX]))) {
                frame_posisyon[frame_INDEX] = 잡기위치[Loop_INDEX]; frame_Stack[frame_INDEX] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (magsimula_frame[frame_INDEX] != 0) kategorya_Kahulugan_katayuan[magsimula_frame[frame_INDEX] - 1] = 3;
            if (틀잠금[frame_INDEX] != 0) { 잠금풀기(틀잠금[frame_INDEX]); 틀잠금[frame_INDEX] = 0; }
            frame_INDEX--;
        }
        gumagamit.sumulat("Uncaught ");
        if (힙[던진객체] == 9) { gumagamit.sumulat(pagbubukod_pangalan(힙[던진객체 + 2])); gumagamit.sumulat(": "); sumulat_SMS(힙[던진객체 + 3]); }
        else gumagamit.sumulat("user exception");
        gumagamit.sumulat_karakter_VALUE(10); 던진객체 = 0; error = true;
    }
    // 이 JVM의 스택 항목은 현재 category-1(int/reference)만 허용한다.
    static void Stack_instruksiyon(int utos_CODE) {
        int 첫값 = 빼기(0), 첫형식 = 반환형;
        if (utos_CODE == 87) return;
        if (utos_CODE == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int byte_data = 빼기(0), SECOND_format = 반환형;
        if (utos_CODE == 88) return;
        if (utos_CODE == 90) { 넣기(첫값, 첫형식); 넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (utos_CODE == 92) { 넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식); 넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (utos_CODE == 95) { 넣기(첫값, 첫형식); 넣기(byte_data, SECOND_format); return; }
        int character_code = 빼기(0), 셋째형식 = 반환형;
        if (utos_CODE == 91) { 넣기(첫값, 첫형식); 넣기(character_code, 셋째형식); 넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (utos_CODE == 93) { 넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식); 넣기(character_code, 셋째형식); 넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = 반환형;
        넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(character_code, 셋째형식); 넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식);
    }
    static void 새객체(int pangalan_constant, int 시작점) {
        int kategorya_CODE = 0, 유효길이 = 0, pagbubukod_Sanggunian = pagbubukod_constant(pangalan_constant);
        if (Word_SMS(pangalan_constant, "java/lang/StringBuilder")) { kategorya_CODE = 4; 유효길이 = 1; }
        if (Word_SMS(pangalan_constant, "java/io/FileInputStream")) { kategorya_CODE = 5; 유효길이 = 2; }
        if (Word_SMS(pangalan_constant, "java/io/FileOutputStream")) { kategorya_CODE = 6; 유효길이 = 2; }
        if (pagbubukod_Sanggunian != 0) { kategorya_CODE = 9; 유효길이 = 2; }
        if (Word_SMS(pangalan_constant, "java/util/ArrayList")) { kategorya_CODE = 10; 유효길이 = 2; }
        if (Word_SMS(pangalan_constant, "java/util/HashMap")) { kategorya_CODE = 11; 유효길이 = 2; }
        if (Word_SMS(pangalan_constant, "java/lang/Integer")) { kategorya_CODE = 12; 유효길이 = 1; }
        if (Word_SMS(pangalan_constant, "java/net/Socket")) { kategorya_CODE = 17; 유효길이 = 5; }
        if (Word_SMS(pangalan_constant, "java/net/ServerSocket")) { kategorya_CODE = 18; 유효길이 = 5; }
        if (Word_SMS(pangalan_constant, "java/net/DatagramSocket")) { kategorya_CODE = 15; 유효길이 = 3; }
        if (Word_SMS(pangalan_constant, "java/net/DatagramPacket")) { kategorya_CODE = 16; 유효길이 = 4; }
        if (Word_SMS(pangalan_constant, "java/lang/Thread") || Word_SMS(pangalan_constant, "한국어/자체/작업가닥")) { kategorya_CODE = 13; 유효길이 = 2; }
        if (Word_SMS(pangalan_constant, "java/lang/Object")) { kategorya_CODE = 8; }
        if (kategorya_CODE == 0 && 화면종(pangalan_constant) != 0) { kategorya_CODE = 화면종(pangalan_constant); 유효길이 = 12; }
        if (kategorya_CODE == 0) {
            int character_code = FIND_kategorya_Kahulugan(pangalan_constant); if (character_code < 0 || error || !magsimula(character_code, 시작점)) return;
            kategorya_CODE = 32 + character_code; 유효길이 = kategorya_espasyo_COUNT[character_code];
        }
        int bagay_Sanggunian = maglaan_Storage(kategorya_CODE, 유효길이); if (error) return;
        if (kategorya_CODE == 13 && Word_SMS(pangalan_constant, "한국어/자체/작업가닥")) 힙[bagay_Sanggunian + 3] = 1;
        if (kategorya_CODE >= 24 && kategorya_CODE <= 28 && 한국어화면종(pangalan_constant) != 0) 힙[bagay_Sanggunian + 13] = 1;
        if (kategorya_CODE == 5 || kategorya_CODE == 6 || kategorya_CODE == 15 || kategorya_CODE == 17 || kategorya_CODE == 18) 힙[bagay_Sanggunian + 2] = -1;
        if (kategorya_CODE == 9) 힙[bagay_Sanggunian + 2] = pagbubukod_Sanggunian;
        넣기(bagay_Sanggunian, 2);
    }
    static boolean 값같음(int 첫값, int byte_data) {
        if (첫값 == byte_data) return true;
        if (첫값 == 0 || byte_data == 0 || 첫값 < 0 || byte_data < 0 || 첫값 >= 힙끝 || byte_data >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[byte_data] == 1) return 글같음(첫값, byte_data, false);
        return 힙[첫값] == 12 && 힙[byte_data] == 12 && 힙[첫값 + 2] == 힙[byte_data + 2];
    }
    static int 글조각(int bagay_Sanggunian, int Start_posisyon, int tapusin_posisyon) {
        if (!bagay_VALUE(bagay_Sanggunian, 1)) return 0;
        if (Start_posisyon < 0 || tapusin_posisyon < Start_posisyon || tapusin_posisyon > 힙[bagay_Sanggunian + 1]) { pagpalya_VALUE("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = maglaan_Storage(1, tapusin_posisyon - Start_posisyon); if (error) return 0;
        for (int Loop_INDEX = Start_posisyon; Loop_INDEX < tapusin_posisyon; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX - Start_posisyon] = 힙[bagay_Sanggunian + 2 + Loop_INDEX];
        return 반환값;
    }
    static int sumali_SMS(int 첫값, int byte_data) {
        if (!bagay_VALUE(첫값, 1) || !bagay_VALUE(byte_data, 1)) return 0;
        int pagpasok_COUNT = 힙[첫값 + 1], pamamaraan_INDEX = 힙[byte_data + 1], 반환값 = maglaan_Storage(1, pagpasok_COUNT + pamamaraan_INDEX); if (error) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < pagpasok_COUNT; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 힙[첫값 + 2 + Loop_INDEX];
        for (int Loop_INDEX = 0; Loop_INDEX < pamamaraan_INDEX; Loop_INDEX++) 힙[반환값 + 2 + pagpasok_COUNT + Loop_INDEX] = 힙[byte_data + 2 + Loop_INDEX];
        return 반환값;
    }
    static boolean 기본호출(int may_ari, int pangalan_constant, int 서술상수, int utos_CODE) {
        if (Word_SMS(may_ari, "한국어/자체/실행인수") && utos_CODE == 184) {
            if (Word_SMS(pangalan_constant, "item_COUNT") && Word_SMS(서술상수, "()I")) { 넣기(gumagamit.인수개수() - 1, 1); return true; }
            if (Word_SMS(pangalan_constant, "SMS") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= gumagamit.인수개수() - 1) 예외던짐(29, "Mag_execute_utos 인수 범위를 벗어났습니다");
                else 넣기(host_karakter(gumagamit.인수(순번 + 1)), 2);
                return true;
            }
            pagpalya_VALUE("지원하지 않는 한국어 Mag_execute_utos 인수 호출"); return true;
        }
        if (Word_SMS(may_ari, "한국어/자체/작업가닥")) { Proseso_thread(pangalan_constant, 서술상수, utos_CODE, true); return true; }
        if (한국어화면소유(may_ari)) { 한국어화면호출(may_ari, pangalan_constant, 서술상수, utos_CODE); return true; }
        if (화면소유(may_ari)) { 화면호출(may_ari, pangalan_constant, 서술상수, utos_CODE); return true; }
        if (Word_SMS(may_ari, "java/net/Socket") || Word_SMS(may_ari, "java/net/ServerSocket") || Word_SMS(may_ari, "java/io/InputStream") || Word_SMS(may_ari, "java/io/OutputStream")) { 흐름호출(may_ari, pangalan_constant, 서술상수, utos_CODE); return true; }
        if (Word_SMS(may_ari, "한국어/자체/kernel_VALUE") && utos_CODE == 184) {
            if (Word_SMS(pangalan_constant, "화면너비") && Word_SMS(서술상수, "()I")) { 넣기(gumagamit.화면너비(), 1); return true; }
            if (Word_SMS(pangalan_constant, "화면높이") && Word_SMS(서술상수, "()I")) { 넣기(gumagamit.화면높이(), 1); return true; }
            if (Word_SMS(pangalan_constant, "밀리초") && Word_SMS(서술상수, "()I")) { 넣기(gumagamit.밀리초(), 1); return true; }
            if (Word_SMS(pangalan_constant, "그림대기") && Word_SMS(서술상수, "()I")) { 넣기(gumagamit.그림대기(), 1); return true; }
            if (Word_SMS(pangalan_constant, "사각형") && Word_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), Y_button_coordinate = 빼기(1), x_coordinate = 빼기(1); 넣기(gumagamit.사각형(x_coordinate, Y_button_coordinate, 너비, 높이, 색상), 1); return true; }
        }
        if (Word_SMS(may_ari, "java/net/InetAddress") || Word_SMS(may_ari, "java/net/DatagramPacket") || Word_SMS(may_ari, "java/net/DatagramSocket")) { 통신호출(may_ari, pangalan_constant, 서술상수, utos_CODE); return true; }
        if (Word_SMS(may_ari, "java/lang/Thread")) { 가닥호출(pangalan_constant, 서술상수, utos_CODE); return true; }
        if (Word_SMS(may_ari, "java/lang/Object")) {
            if (Word_SMS(pangalan_constant, "<init>") && Word_SMS(서술상수, "()V") && utos_CODE == 183) { 객체유효(빼기(2)); return true; }
            if (Word_SMS(pangalan_constant, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int byte_data = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == byte_data ? 1 : 0, 1); return true; }
        }
        if (pagbubukod_constant(may_ari) != 0) {
            if (Word_SMS(pangalan_constant, "<init>") && utos_CODE == 183 && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int prompt = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), bagay_Sanggunian = 빼기(2);
                if (bagay_VALUE(bagay_Sanggunian, 9)) { 힙[bagay_Sanggunian + 3] = prompt; 힙참조[bagay_Sanggunian + 3] = 1; } return true;
            }
            if ((Word_SMS(pangalan_constant, "getMessage") || Word_SMS(pangalan_constant, "설명")) && Word_SMS(서술상수, "()Ljava/lang/String;")) { int bagay_Sanggunian = 빼기(2); if (bagay_VALUE(bagay_Sanggunian, 9)) 넣기(힙[bagay_Sanggunian + 3], 2); return true; }
        }
        if (Word_SMS(may_ari, "java/lang/String")) {
            if (utos_CODE == 182 && Word_SMS(pangalan_constant, "getBytes") && (Word_SMS(서술상수, "()[B") || Word_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int pag_encode_pangalan = Word_SMS(서술상수, "()[B") ? 0 : 빼기(2), bagay_Sanggunian = 빼기(2);
                if (!bagay_VALUE(bagay_Sanggunian, 1)) return true;
                if (pag_encode_pangalan != 0 && !글같음(pag_encode_pangalan, host_karakter("UTF-8"), false) && !글같음(pag_encode_pangalan, host_karakter("UTF8"), false) && !글같음(pag_encode_pangalan, host_karakter("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int pagpasok_COUNT = 힙[bagay_Sanggunian + 1], 반환값 = maglaan_Storage(20, pagpasok_COUNT * 3), 사용수 = 0; if (error) return true;
                for (int inner_join_posisyon = 0; inner_join_posisyon < pagpasok_COUNT; inner_join_posisyon++) {
                    int character_code = 힙[bagay_Sanggunian + 2 + inner_join_posisyon];
                    if (character_code >= 0xd800 && character_code <= 0xdbff && inner_join_posisyon + 1 < pagpasok_COUNT && 힙[bagay_Sanggunian + 3 + inner_join_posisyon] >= 0xdc00 && 힙[bagay_Sanggunian + 3 + inner_join_posisyon] <= 0xdfff) character_code = 0x10000 + ((character_code - 0xd800) << 10) + 힙[bagay_Sanggunian + 2 + ++inner_join_posisyon] - 0xdc00;
                    else if (character_code >= 0xd800 && character_code <= 0xdfff) character_code = '?';
                    if (character_code < 128) 힙[반환값 + 2 + 사용수++] = character_code;
                    else { int byte_COUNT = character_code < 2048 ? 2 : character_code < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((byte_COUNT == 2 ? 192 : byte_COUNT == 3 ? 224 : 240) | character_code >> (6 * (byte_COUNT - 1))); for (int Paghahambing_posisyon = byte_COUNT - 1; Paghahambing_posisyon > 0; Paghahambing_posisyon--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | character_code >> (6 * (Paghahambing_posisyon - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (utos_CODE == 184 && Word_SMS(pangalan_constant, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(digit_karakter(빼기(1)), 2); return true; }
            if (utos_CODE != 182) return false;
            if (Word_SMS(pangalan_constant, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int byte_data = 빼기(2), 첫값 = 빼기(2); if (bagay_VALUE(첫값, 1)) 넣기(글같음(첫값, byte_data, false) ? 1 : 0, 1); return true; }
            if (Word_SMS(pangalan_constant, "isEmpty") && Word_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (bagay_VALUE(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_SMS(pangalan_constant, "substring") && (Word_SMS(서술상수, "(I)Ljava/lang/String;") || Word_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SECOND_VALUE = Word_SMS(서술상수, "(II)Ljava/lang/String;"); int tapusin_posisyon = SECOND_VALUE ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (bagay_VALUE(첫값, 1)) 넣기(글조각(첫값, 시작점, SECOND_VALUE ? tapusin_posisyon : 힙[첫값 + 1]), 2); return true;
            }
            if (Word_SMS(pangalan_constant, "concat") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int byte_data = 빼기(2), 첫값 = 빼기(2); 넣기(sumali_SMS(첫값, byte_data), 2); return true; }
            if (Word_SMS(pangalan_constant, "hashCode") && Word_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), hash_VALUE = 0; if (bagay_VALUE(첫값, 1)) { for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) hash_VALUE = hash_VALUE * 31 + 힙[첫값 + 2 + Loop_INDEX]; 넣기(hash_VALUE, 1); } return true; }
            if (Word_SMS(pangalan_constant, "toString") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (bagay_VALUE(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_SMS(may_ari, "java/lang/Integer")) {
            if (utos_CODE == 184 && Word_SMS(pangalan_constant, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int data_VALUE = 빼기(1), bagay_Sanggunian = data_VALUE >= -128 && data_VALUE <= 127 ? Store_integer_buong_numero[data_VALUE + 128] : 0; if (bagay_Sanggunian == 0) { bagay_Sanggunian = maglaan_Storage(12, 1); if (!error) { 힙[bagay_Sanggunian + 2] = data_VALUE; if (data_VALUE >= -128 && data_VALUE <= 127) Store_integer_buong_numero[data_VALUE + 128] = bagay_Sanggunian; } } 넣기(bagay_Sanggunian, 2); return true; }
            if (utos_CODE == 183 && Word_SMS(pangalan_constant, "<init>") && Word_SMS(서술상수, "(I)V")) { int data_VALUE = 빼기(1), bagay_Sanggunian = 빼기(2); if (bagay_VALUE(bagay_Sanggunian, 12)) 힙[bagay_Sanggunian + 2] = data_VALUE; return true; }
            if (utos_CODE == 182 && Word_SMS(pangalan_constant, "intValue") && Word_SMS(서술상수, "()I")) { int bagay_Sanggunian = 빼기(2); if (bagay_VALUE(bagay_Sanggunian, 12)) 넣기(힙[bagay_Sanggunian + 2], 1); return true; }
            if (utos_CODE == 184 && Word_SMS(pangalan_constant, "toString") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(digit_karakter(빼기(1)), 2); return true; }
        }
        if (Word_SMS(may_ari, "java/lang/Math") && utos_CODE == 184) {
            if (Word_SMS(pangalan_constant, "abs") && Word_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_SMS(pangalan_constant, "min") || Word_SMS(pangalan_constant, "max")) && Word_SMS(서술상수, "(II)I")) { int byte_data = 빼기(1), 첫값 = 빼기(1); 넣기(Word_SMS(pangalan_constant, "min") ? (첫값 < byte_data ? 첫값 : byte_data) : (첫값 > byte_data ? 첫값 : byte_data), 1); return true; }
        }
        if (Word_SMS(may_ari, "java/lang/System") && utos_CODE == 184) {
            if (Word_SMS(pangalan_constant, "gc") && Word_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Word_SMS(pangalan_constant, "arraycopy") && Word_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int pagpasok_COUNT = 빼기(1), patutunguhan_VALUE_INDEX = 빼기(1), byte_data = 빼기(2), Start_posisyon = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(byte_data)) {
                    int kategorya_CODE = 힙[첫값];
                    if (힙[byte_data] != kategorya_CODE || (kategorya_CODE != 2 && kategorya_CODE != 3 && (kategorya_CODE < 20 || kategorya_CODE > 23))) pagpalya_VALUE("arraycopy type mismatch");
                    else if (pagpasok_COUNT < 0 || Start_posisyon < 0 || patutunguhan_VALUE_INDEX < 0 || Start_posisyon > 힙[첫값 + 1] - pagpasok_COUNT || patutunguhan_VALUE_INDEX > 힙[byte_data + 1] - pagpasok_COUNT) pagpalya_VALUE("ArrayIndexOutOfBoundsException");
                    else if (첫값 == byte_data && patutunguhan_VALUE_INDEX > Start_posisyon) { for (int Loop_INDEX = pagpasok_COUNT - 1; Loop_INDEX >= 0; Loop_INDEX--) 힙[byte_data + 2 + patutunguhan_VALUE_INDEX + Loop_INDEX] = 힙[첫값 + 2 + Start_posisyon + Loop_INDEX]; }
                    else { for (int Loop_INDEX = 0; Loop_INDEX < pagpasok_COUNT && !error; Loop_INDEX++) { int data_VALUE = 힙[첫값 + 2 + Start_posisyon + Loop_INDEX]; if (kategorya_CODE != 3 || 배열저장가능(byte_data, data_VALUE)) 힙[byte_data + 2 + patutunguhan_VALUE_INDEX + Loop_INDEX] = data_VALUE; } }
                }
                return true;
            }
        }
        if (Word_SMS(may_ari, "java/util/ArrayList") || Word_SMS(may_ari, "java/util/List") || Word_SMS(may_ari, "java/util/HashMap") || Word_SMS(may_ari, "java/util/Map")) {
            모음호출(may_ari, pangalan_constant, 서술상수, utos_CODE); return true;
        }
        return false;
    }
    static void 모음늘리기(int bagay_Sanggunian, int 필요수) {
        int 이전값 = 힙[bagay_Sanggunian + 2], 용량값 = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (용량값 >= 필요수) return;
        int Susunod_posisyon = 용량값 < 8 ? 8 : 용량값 * 2; if (Susunod_posisyon < 필요수) Susunod_posisyon = 필요수;
        int data_ARRAY = maglaan_Storage(3, Susunod_posisyon); if (error) return;
        for (int Loop_INDEX = 0; Loop_INDEX < 용량값; Loop_INDEX++) 힙[data_ARRAY + 2 + Loop_INDEX] = 힙[이전값 + 2 + Loop_INDEX];
        힙[bagay_Sanggunian + 2] = data_ARRAY; 힙참조[bagay_Sanggunian + 2] = 1;
    }
    static void 모음호출(int may_ari, int pangalan_constant, int 서술상수, int utos_CODE) {
        boolean 대응참조 = Word_SMS(may_ari, "java/util/HashMap") || Word_SMS(may_ari, "java/util/Map"); int kategorya_CODE = 대응참조 ? 11 : 10;
        if (Word_SMS(pangalan_constant, "<init>") && utos_CODE == 183 && Word_SMS(서술상수, "()V")) { int bagay_Sanggunian = 빼기(2); if (bagay_VALUE(bagay_Sanggunian, kategorya_CODE)) 모음늘리기(bagay_Sanggunian, 8); return; }
        if (utos_CODE != 182 && utos_CODE != 185) { pagpalya_VALUE("invalid collection invocation"); return; }
        if (Word_SMS(pangalan_constant, "size") && Word_SMS(서술상수, "()I") || Word_SMS(pangalan_constant, "isEmpty") && Word_SMS(서술상수, "()Z")) {
            int bagay_Sanggunian = 빼기(2); if (bagay_VALUE(bagay_Sanggunian, kategorya_CODE)) 넣기(Word_SMS(pangalan_constant, "size") ? 힙[bagay_Sanggunian + 3] : 힙[bagay_Sanggunian + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_SMS(pangalan_constant, "clear") && Word_SMS(서술상수, "()V")) { int bagay_Sanggunian = 빼기(2); if (bagay_VALUE(bagay_Sanggunian, kategorya_CODE)) { int data_ARRAY = 힙[bagay_Sanggunian + 2]; for (int Loop_INDEX = 0; Loop_INDEX < 힙[data_ARRAY + 1]; Loop_INDEX++) 힙[data_ARRAY + 2 + Loop_INDEX] = 0; 힙[bagay_Sanggunian + 3] = 0; } return; }
        if (!대응참조 && Word_SMS(pangalan_constant, "add") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int data_VALUE = 빼기(2), bagay_Sanggunian = 빼기(2); if (!bagay_VALUE(bagay_Sanggunian, 10)) return;
            int pagpasok_COUNT = 힙[bagay_Sanggunian + 3]; 모음늘리기(bagay_Sanggunian, pagpasok_COUNT + 1); if (!error) { 힙[힙[bagay_Sanggunian + 2] + 2 + pagpasok_COUNT] = data_VALUE; 힙[bagay_Sanggunian + 3] = pagpasok_COUNT + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_SMS(pangalan_constant, "get") || Word_SMS(pangalan_constant, "remove")) && Word_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Word_SMS(pangalan_constant, "set") && Word_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = Word_SMS(pangalan_constant, "set"); int data_VALUE = 지정여부 ? 빼기(2) : 0, pagpasok_posisyon = 빼기(1), bagay_Sanggunian = 빼기(2);
            if (!bagay_VALUE(bagay_Sanggunian, 10)) return;
            int pagpasok_COUNT = 힙[bagay_Sanggunian + 3], data_ARRAY = 힙[bagay_Sanggunian + 2];
            if (pagpasok_posisyon < 0 || pagpasok_posisyon >= pagpasok_COUNT) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[data_ARRAY + 2 + pagpasok_posisyon];
            if (지정여부) 힙[data_ARRAY + 2 + pagpasok_posisyon] = data_VALUE;
            if (Word_SMS(pangalan_constant, "remove")) { for (int Loop_INDEX = pagpasok_posisyon + 1; Loop_INDEX < pagpasok_COUNT; Loop_INDEX++) 힙[data_ARRAY + 1 + Loop_INDEX] = 힙[data_ARRAY + 2 + Loop_INDEX]; 힙[data_ARRAY + 1 + pagpasok_COUNT] = 0; 힙[bagay_Sanggunian + 3] = pagpasok_COUNT - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Word_SMS(pangalan_constant, "get") || Word_SMS(pangalan_constant, "remove")) && Word_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(pangalan_constant, "put") && Word_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(pangalan_constant, "containsKey") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_SMS(pangalan_constant, "put"), tanggalin = Word_SMS(pangalan_constant, "remove");
            int data_VALUE = 넣기여부 ? 빼기(2) : 0, key_Sanggunian = 빼기(2), bagay_Sanggunian = 빼기(2); if (!bagay_VALUE(bagay_Sanggunian, 11)) return;
            int pagpasok_COUNT = 힙[bagay_Sanggunian + 3], data_ARRAY = 힙[bagay_Sanggunian + 2], 찾은여부 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < pagpasok_COUNT; Loop_INDEX++) if (값같음(key_Sanggunian, 힙[data_ARRAY + 2 + 2 * Loop_INDEX])) { 찾은여부 = Loop_INDEX; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[data_ARRAY + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(bagay_Sanggunian, (pagpasok_COUNT + 1) * 2); data_ARRAY = 힙[bagay_Sanggunian + 2]; 찾은여부 = pagpasok_COUNT; if (!error) 힙[bagay_Sanggunian + 3] = pagpasok_COUNT + 1; }
                if (!error) { 힙[data_ARRAY + 2 + 2 * 찾은여부] = key_Sanggunian; 힙[data_ARRAY + 3 + 2 * 찾은여부] = data_VALUE; }
            }
            if (tanggalin && 찾은여부 >= 0) { for (int Loop_INDEX = 찾은여부 + 1; Loop_INDEX < pagpasok_COUNT; Loop_INDEX++) { 힙[data_ARRAY + 2 * Loop_INDEX] = 힙[data_ARRAY + 2 + 2 * Loop_INDEX]; 힙[data_ARRAY + 1 + 2 * Loop_INDEX] = 힙[data_ARRAY + 3 + 2 * Loop_INDEX]; } 힙[data_ARRAY + 2 * pagpasok_COUNT] = 0; 힙[data_ARRAY + 1 + 2 * pagpasok_COUNT] = 0; 힙[bagay_Sanggunian + 3] = pagpasok_COUNT - 1; }
            if (Word_SMS(pangalan_constant, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        pagpalya_VALUE("unsupported collection method");
    }
    static boolean 잠금얻기(int bagay_Sanggunian) {
        if (!객체유효(bagay_Sanggunian)) return false;
        if (잠금깊이[bagay_Sanggunian] != 0 && 잠금주인[bagay_Sanggunian] != 현재가닥 + 1) { 바꿈요청 = true; return false; }
        잠금주인[bagay_Sanggunian] = 현재가닥 + 1; 잠금깊이[bagay_Sanggunian]++; return true;
    }
    static void 잠금풀기(int bagay_Sanggunian) {
        if (!객체유효(bagay_Sanggunian)) return;
        if (잠금깊이[bagay_Sanggunian] == 0 || 잠금주인[bagay_Sanggunian] != 현재가닥 + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[bagay_Sanggunian] == 0) 잠금주인[bagay_Sanggunian] = 0;
    }
    static boolean SWITCH_thread() {
        thread_frame[현재가닥] = frame_INDEX;
        if (frame_INDEX < 현재가닥 * 32) thread_katayuan[현재가닥] = 3;
        for (int Loop_INDEX = 0; Loop_INDEX < thread_COUNT; Loop_INDEX++) if (thread_katayuan[Loop_INDEX] == 2 && thread_katayuan[가닥대기[Loop_INDEX]] == 3) thread_katayuan[Loop_INDEX] = 1;
        for (int Loop_INDEX = 1; Loop_INDEX <= thread_COUNT; Loop_INDEX++) {
            int Susunod_posisyon = (현재가닥 + Loop_INDEX) % thread_COUNT;
            if (thread_katayuan[Susunod_posisyon] == 1) { 현재가닥 = Susunod_posisyon; frame_INDEX = thread_frame[Susunod_posisyon]; 바꿈요청 = false; return true; }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < thread_COUNT; Loop_INDEX++) if (thread_katayuan[Loop_INDEX] != 3) { pagpalya_VALUE("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int pangalan_constant, int 서술상수, int utos_CODE) { Proseso_thread(pangalan_constant, 서술상수, utos_CODE, false); }
    static void Proseso_thread(int pangalan_constant, int 서술상수, int utos_CODE, boolean 한국어) {
        if (utos_CODE == 184 && Word_SMS(pangalan_constant, 한국어 ? "YIELD_gawain" : "yield") && Word_SMS(서술상수, "()V")) { 바꿈요청 = true; return; }
        if (utos_CODE == 184 && Word_SMS(pangalan_constant, "currentThread") && Word_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(thread_bagay[현재가닥], 2); return; }
        if (utos_CODE == 183 && Word_SMS(pangalan_constant, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, 한국어 ? "(L한국어/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int target_email = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), bagay_Sanggunian = 빼기(2);
            if (!객체유효(bagay_Sanggunian)) return;
            if (힙[bagay_Sanggunian] == 13) { 힙[bagay_Sanggunian + 2] = target_email; 힙참조[bagay_Sanggunian + 2] = 1; }
            else if (target_email != 0) pagpalya_VALUE("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (utos_CODE == 182 && (Word_SMS(pangalan_constant, 한국어 ? "Start_gawain" : "start") || Word_SMS(pangalan_constant, 한국어 ? "기다리기" : "join")) && Word_SMS(서술상수, "()V") || utos_CODE == 182 && Word_SMS(pangalan_constant, 한국어 ? "살아있는가" : "isAlive") && Word_SMS(서술상수, "()Z")) {
            int bagay_Sanggunian = 빼기(2); if (!객체유효(bagay_Sanggunian)) return;
            int account_VALUE = -1; for (int Loop_INDEX = 0; Loop_INDEX < thread_COUNT; Loop_INDEX++) if (thread_bagay[Loop_INDEX] == bagay_Sanggunian) account_VALUE = Loop_INDEX;
            if (Word_SMS(pangalan_constant, 한국어 ? "살아있는가" : "isAlive")) { 넣기(account_VALUE >= 0 && thread_katayuan[account_VALUE] != 3 ? 1 : 0, 1); return; }
            if (Word_SMS(pangalan_constant, 한국어 ? "기다리기" : "join")) { if (account_VALUE >= 0 && thread_katayuan[account_VALUE] != 3) { 가닥대기[현재가닥] = account_VALUE; thread_katayuan[현재가닥] = 2; 바꿈요청 = true; } return; }
            if (account_VALUE >= 0) { 예외던짐(한국어 ? 38 : 16, "thread already started"); return; }
            if (thread_COUNT == 4) { pagpalya_VALUE("thread limit (4 including main)"); return; }
            int target_email = 힙[bagay_Sanggunian] == 13 ? 힙[bagay_Sanggunian + 2] : bagay_Sanggunian;
            int file_INDEX = target_email > 0 && 힙[target_email] >= 32 ? pangalan_pamamaraan(힙[target_email] - 32, 한국어 ? "Mag_execute_gawain" : "run", "()V") : -1;
            if (target_email != 0 && file_INDEX < 0) { pagpalya_VALUE("Runnable.run required"); return; }
            account_VALUE = thread_COUNT++; thread_bagay[account_VALUE] = bagay_Sanggunian; thread_target[account_VALUE] = target_email;
            int frame = account_VALUE * 32; thread_frame[account_VALUE] = file_INDEX < 0 ? frame - 1 : frame; thread_katayuan[account_VALUE] = file_INDEX < 0 ? 3 : 1;
            if (file_INDEX >= 0) { frame_pamamaraan[frame] = file_INDEX; frame_posisyon[frame] = pamamaraan_Start[file_INDEX]; lokal_VALUE[frame * 128] = target_email; lokal_TYPE[frame * 128] = 2; }
            return;
        }
        pagpalya_VALUE("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], email_SMS = new int[16];
    static int lokal_email() { return email_bagay(0x7f000001); }
    static int email_bagay(int VALUE) { int bagay_Sanggunian = maglaan_Storage(14, 1); if (!error) 힙[bagay_Sanggunian + 2] = VALUE; return bagay_Sanggunian; }
    static int 주소해독(int bagay_Sanggunian) {
        if (bagay_Sanggunian == 0 || 글같음(bagay_Sanggunian, host_karakter("localhost"), false)) return 0x7f000001;
        if (!bagay_VALUE(bagay_Sanggunian, 1)) return 0;
        int data_VALUE = 0, 총수 = 0, email_byte = 0, 자릿수 = 0, pagpasok_COUNT = 힙[bagay_Sanggunian + 1];
        for (int Loop_INDEX = 0; Loop_INDEX <= pagpasok_COUNT; Loop_INDEX++) {
            int character_code = Loop_INDEX == pagpasok_COUNT ? '.' : 힙[bagay_Sanggunian + 2 + Loop_INDEX];
            if (character_code == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } data_VALUE = data_VALUE << 8 | email_byte; 총수++; email_byte = 자릿수 = 0; }
            else { if (character_code < '0' || character_code > '9' || ++자릿수 > 3 || (email_byte = email_byte * 10 + character_code - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return data_VALUE;
    }
    static int email_karakter(int data_VALUE) {
        int pagpasok_COUNT = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int email_byte = data_VALUE >>> 이동비트 & 255;
            if (email_byte >= 100) email_SMS[pagpasok_COUNT++] = '0' + email_byte / 100;
            if (email_byte >= 10) email_SMS[pagpasok_COUNT++] = '0' + email_byte / 10 % 10;
            email_SMS[pagpasok_COUNT++] = '0' + email_byte % 10; if (이동비트 != 0) email_SMS[pagpasok_COUNT++] = '.';
        }
        int bagay_Sanggunian = maglaan_Storage(1, pagpasok_COUNT); if (!error) for (int Loop_INDEX = 0; Loop_INDEX < pagpasok_COUNT; Loop_INDEX++) 힙[bagay_Sanggunian + 2 + Loop_INDEX] = email_SMS[Loop_INDEX]; return bagay_Sanggunian;
    }
    static void 통신호출(int may_ari, int pangalan_constant, int 서술상수, int utos_CODE) {
        if (Word_SMS(may_ari, "java/net/InetAddress")) {
            if (utos_CODE == 184 && Word_SMS(pangalan_constant, "getLoopbackAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(lokal_email(), 2); return; }
            if (utos_CODE == 184 && Word_SMS(pangalan_constant, "getByName") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int data_VALUE = 주소해독(빼기(2)); if (던진객체 == 0 && !error) 넣기(email_bagay(data_VALUE), 2); return;
            }
            if (utos_CODE == 182 && Word_SMS(pangalan_constant, "getHostAddress") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int bagay_Sanggunian = 빼기(2); if (bagay_VALUE(bagay_Sanggunian, 14)) 넣기(email_karakter(힙[bagay_Sanggunian + 2]), 2); return; }
        }
        if (Word_SMS(may_ari, "java/net/DatagramPacket")) {
            if (utos_CODE == 183 && Word_SMS(pangalan_constant, "<init>") && (Word_SMS(서술상수, "([BI)V") || Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean patutunguhan_VALUE_Sanggunian = Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int numero_ng_port = patutunguhan_VALUE_Sanggunian ? 빼기(1) : 0, email_Sanggunian = patutunguhan_VALUE_Sanggunian ? 빼기(2) : 0;
                int pagpasok_COUNT = 빼기(1), data_ARRAY = 빼기(2), bagay_Sanggunian = 빼기(2);
                if (!bagay_VALUE(bagay_Sanggunian, 16) || !bagay_VALUE(data_ARRAY, 20)) return;
                if (pagpasok_COUNT < 0 || pagpasok_COUNT > 힙[data_ARRAY + 1] || numero_ng_port < 0 || numero_ng_port > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (email_Sanggunian != 0 && !bagay_VALUE(email_Sanggunian, 14)) return;
                힙[bagay_Sanggunian + 2] = data_ARRAY; 힙참조[bagay_Sanggunian + 2] = 1; 힙[bagay_Sanggunian + 3] = pagpasok_COUNT;
                힙[bagay_Sanggunian + 4] = email_Sanggunian; 힙참조[bagay_Sanggunian + 4] = 1; 힙[bagay_Sanggunian + 5] = numero_ng_port; return;
            }
            if (utos_CODE == 182 && Word_SMS(pangalan_constant, "setLength") && Word_SMS(서술상수, "(I)V")) {
                int pagpasok_COUNT = 빼기(1), bagay_Sanggunian = 빼기(2); if (!bagay_VALUE(bagay_Sanggunian, 16)) return;
                if (pagpasok_COUNT < 0 || pagpasok_COUNT > 힙[힙[bagay_Sanggunian + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[bagay_Sanggunian + 3] = pagpasok_COUNT; return;
            }
            if (utos_CODE == 182 && (Word_SMS(pangalan_constant, "getData") && Word_SMS(서술상수, "()[B") || Word_SMS(pangalan_constant, "getLength") && Word_SMS(서술상수, "()I") || Word_SMS(pangalan_constant, "getAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;") || Word_SMS(pangalan_constant, "getPort") && Word_SMS(서술상수, "()I"))) {
                int bagay_Sanggunian = 빼기(2); if (!bagay_VALUE(bagay_Sanggunian, 16)) return;
                int pagpasok_posisyon = Word_SMS(pangalan_constant, "getData") ? 2 : Word_SMS(pangalan_constant, "getLength") ? 3 : Word_SMS(pangalan_constant, "getAddress") ? 4 : 5;
                넣기(힙[bagay_Sanggunian + pagpasok_posisyon], pagpasok_posisyon == 2 || pagpasok_posisyon == 4 ? 2 : 1); return;
            }
        }
        if (Word_SMS(may_ari, "java/net/DatagramSocket")) {
            if (utos_CODE == 183 && Word_SMS(pangalan_constant, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(I)V"))) {
                int numero_ng_port = Word_SMS(서술상수, "()V") ? 0 : 빼기(1), bagay_Sanggunian = 빼기(2); if (!bagay_VALUE(bagay_Sanggunian, 15)) return;
                if (numero_ng_port < 0 || numero_ng_port > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = gumagamit.buksan_Network(numero_ng_port); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[bagay_Sanggunian + 2] = 열린파일번호; return;
            }
            if (utos_CODE == 182 && Word_SMS(pangalan_constant, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), bagay_Sanggunian = 빼기(2); if (!bagay_VALUE(bagay_Sanggunian, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[bagay_Sanggunian + 3] = 밀리초값; return;
            }
            if (utos_CODE == 182 && Word_SMS(pangalan_constant, "getLocalPort") && Word_SMS(서술상수, "()I")) { int bagay_Sanggunian = 빼기(2); if (bagay_VALUE(bagay_Sanggunian, 15)) 넣기(힙[bagay_Sanggunian + 2] < 0 ? -1 : gumagamit.Network_port(힙[bagay_Sanggunian + 2]), 1); return; }
            if (utos_CODE == 182 && Word_SMS(pangalan_constant, "isClosed") && Word_SMS(서술상수, "()Z")) { int bagay_Sanggunian = 빼기(2); if (bagay_VALUE(bagay_Sanggunian, 15)) 넣기(힙[bagay_Sanggunian + 2] < 0 ? 1 : 0, 1); return; }
            if (utos_CODE == 182 && Word_SMS(pangalan_constant, "close") && Word_SMS(서술상수, "()V")) { int bagay_Sanggunian = 빼기(2); if (bagay_VALUE(bagay_Sanggunian, 15) && 힙[bagay_Sanggunian + 2] >= 0) { gumagamit.파일서술자닫기(힙[bagay_Sanggunian + 2]); 힙[bagay_Sanggunian + 2] = -1; } return; }
            if (utos_CODE == 182 && (Word_SMS(pangalan_constant, "send") || Word_SMS(pangalan_constant, "receive")) && Word_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int packet = 빼기(2), bagay_Sanggunian = 빼기(2); if (!bagay_VALUE(packet, 16) || !bagay_VALUE(bagay_Sanggunian, 15)) return;
                int data_ARRAY = 힙[packet + 2], 유효길이 = 힙[packet + 3], 열린파일번호 = 힙[bagay_Sanggunian + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_SMS(pangalan_constant, "send")) {
                    if (!bagay_VALUE(힙[packet + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < 유효길이; Loop_INDEX++) 통신임시[Loop_INDEX] = 힙[data_ARRAY + 2 + Loop_INDEX];
                    if (gumagamit.i_email_Network(열린파일번호, 힙[힙[packet + 4] + 2], 힙[packet + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int pagpasok_COUNT = gumagamit.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (pagpasok_COUNT == -11) {
                        int 현재시각 = gumagamit.밀리초();
                        if (힙[bagay_Sanggunian + 4] == 0) 힙[bagay_Sanggunian + 4] = 현재시각 + 1;
                        if (힙[bagay_Sanggunian + 3] > 0 && 현재시각 - (힙[bagay_Sanggunian + 4] - 1) >= 힙[bagay_Sanggunian + 3]) { 힙[bagay_Sanggunian + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(bagay_Sanggunian, 2); 넣기(packet, 2); frame_posisyon[frame_INDEX] = frame_instruksiyon[frame_INDEX]; 바꿈요청 = true; return;
                    }
                    힙[bagay_Sanggunian + 4] = 0;
                    if (pagpasok_COUNT < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < pagpasok_COUNT; Loop_INDEX++) 힙[data_ARRAY + 2 + Loop_INDEX] = (byte)통신임시[Loop_INDEX];
                    힙[packet + 3] = pagpasok_COUNT; 힙[packet + 4] = email_bagay(통신임시[513]); 힙참조[packet + 4] = 1; 힙[packet + 5] = 통신임시[512];
                }
                return;
            }
        }
        pagpalya_VALUE("unsupported java.net method");
    }
    static boolean 흐름대기(int bagay_Sanggunian) {
        int 현재시각 = gumagamit.밀리초();
        if (힙[bagay_Sanggunian + 5] == 0) 힙[bagay_Sanggunian + 5] = 현재시각 + 1;
        if (힙[bagay_Sanggunian + 3] > 0 && 현재시각 - (힙[bagay_Sanggunian + 5] - 1) >= 힙[bagay_Sanggunian + 3]) { 힙[bagay_Sanggunian + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        frame_posisyon[frame_INDEX] = frame_instruksiyon[frame_INDEX]; 바꿈요청 = true; return true;
    }
    static void 흐름호출(int may_ari, int pangalan_constant, int 서술상수, int utos_CODE) {
        boolean 수신쪽 = Word_SMS(may_ari, "java/net/ServerSocket"), Stream = Word_SMS(may_ari, "java/io/InputStream") || Word_SMS(may_ari, "java/io/OutputStream");
        if (!Stream && utos_CODE == 183 && Word_SMS(pangalan_constant, "<init>")) {
            boolean information_technology_walang_laman_katayuan = Word_SMS(서술상수, "()V"), 이름지정여부 = Word_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(information_technology_walang_laman_katayuan || 수신쪽 && Word_SMS(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { pagpalya_VALUE("unsupported socket constructor"); return; }
            int numero_ng_port = information_technology_walang_laman_katayuan ? 0 : 빼기(1), email_Sanggunian = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, bagay_Sanggunian = 빼기(2);
            if (!bagay_VALUE(bagay_Sanggunian, 수신쪽 ? 18 : 17)) return;
            if (numero_ng_port < 0 || numero_ng_port > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !bagay_VALUE(email_Sanggunian, 14)) return;
            int Network_email_df3458bb = 이름지정여부 ? 주소해독(email_Sanggunian) : 주소지정여부 ? 힙[email_Sanggunian + 2] : 0x7f000001;
            if (error || 던진객체 != 0) return;
            int 열린파일번호 = gumagamit.Stream_control(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = information_technology_walang_laman_katayuan ? 0 : 수신쪽 ? gumagamit.Stream_control(1, 열린파일번호, numero_ng_port) : gumagamit.CONNECT_Stream(열린파일번호, Network_email_df3458bb, numero_ng_port);
            if (처리값 < 0) { gumagamit.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[bagay_Sanggunian + 2] = 열린파일번호; 힙[bagay_Sanggunian + 4] = numero_ng_port; 힙[bagay_Sanggunian + 6] = information_technology_walang_laman_katayuan ? 0 : 1; return;
        }
        if (!Stream && Word_SMS(pangalan_constant, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), bagay_Sanggunian = 빼기(2); if (!bagay_VALUE(bagay_Sanggunian, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[bagay_Sanggunian + 3] = 밀리초값; return; }
        if (!Stream && Word_SMS(pangalan_constant, "close") && Word_SMS(서술상수, "()V")) { int bagay_Sanggunian = 빼기(2); if (bagay_VALUE(bagay_Sanggunian, 수신쪽 ? 18 : 17) && 힙[bagay_Sanggunian + 2] >= 0) { gumagamit.파일서술자닫기(힙[bagay_Sanggunian + 2]); 힙[bagay_Sanggunian + 2] = -1; } return; }
        if (!Stream && (Word_SMS(pangalan_constant, "getLocalPort") || Word_SMS(pangalan_constant, "getPort") || Word_SMS(pangalan_constant, "isClosed") || Word_SMS(pangalan_constant, "isConnected"))) {
            int bagay_Sanggunian = 빼기(2); if (!bagay_VALUE(bagay_Sanggunian, 수신쪽 ? 18 : 17)) return;
            넣기(Word_SMS(pangalan_constant, "isClosed") ? 힙[bagay_Sanggunian + 2] < 0 ? 1 : 0 : Word_SMS(pangalan_constant, "isConnected") ? 힙[bagay_Sanggunian + 6] : Word_SMS(pangalan_constant, "getPort") ? 힙[bagay_Sanggunian + 4] : 힙[bagay_Sanggunian + 2] < 0 ? -1 : gumagamit.Stream_control(4, 힙[bagay_Sanggunian + 2], 0), 1); return;
        }
        if (수신쪽 && Word_SMS(pangalan_constant, "accept") && Word_SMS(서술상수, "()Ljava/net/Socket;")) {
            int bagay_Sanggunian = 빼기(2); if (!bagay_VALUE(bagay_Sanggunian, 18)) return; int 열린파일번호 = gumagamit.Stream_control(3, 힙[bagay_Sanggunian + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(bagay_Sanggunian)) 넣기(bagay_Sanggunian, 2); return; }
            힙[bagay_Sanggunian + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = maglaan_Storage(17, 5); if (error) { gumagamit.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = gumagamit.Stream_control(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !Stream && ((Word_SMS(pangalan_constant, "getInputStream") && Word_SMS(서술상수, "()Ljava/io/InputStream;")) || (Word_SMS(pangalan_constant, "getOutputStream") && Word_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int bagay_Sanggunian = 빼기(2); if (!bagay_VALUE(bagay_Sanggunian, 17)) return; if (힙[bagay_Sanggunian + 2] < 0 || 힙[bagay_Sanggunian + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = maglaan_Storage(19, 4); if (error) return; 힙[반환값 + 2] = bagay_Sanggunian; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Word_SMS(pangalan_constant, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (Stream) {
            boolean 읽기여부 = Word_SMS(pangalan_constant, "read"), information_technology_sumulat_operasyon = Word_SMS(pangalan_constant, "write"), i_block = Word_SMS(서술상수, "([B)I") || Word_SMS(서술상수, "([B)V"), information_technology_SUBARRAY = Word_SMS(서술상수, "([BII)I") || Word_SMS(서술상수, "([BII)V");
            int pagpasok_COUNT = information_technology_SUBARRAY ? 빼기(1) : 0, 시작변위 = information_technology_SUBARRAY ? 빼기(1) : 0, data_ARRAY = i_block || information_technology_SUBARRAY ? 빼기(2) : 0;
            int data_VALUE = information_technology_sumulat_operasyon && Word_SMS(서술상수, "(I)V") ? 빼기(1) : 0, bagay_Sanggunian = 빼기(2);
            if (!bagay_VALUE(bagay_Sanggunian, 19)) return; int 부모참조 = 힙[bagay_Sanggunian + 2], 열린파일번호 = 힙[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_SMS(pangalan_constant, "close") && Word_SMS(서술상수, "()V")) { gumagamit.파일서술자닫기(열린파일번호); 힙[부모참조 + 2] = -1; return; }
            if (Word_SMS(pangalan_constant, "flush") && Word_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !information_technology_sumulat_operasyon) || 읽기여부 != (힙[bagay_Sanggunian + 3] == 0)) { pagpalya_VALUE("unsupported stream operation"); return; }
            if (i_block || information_technology_SUBARRAY) { if (!bagay_VALUE(data_ARRAY, 20)) return; if (i_block) pagpasok_COUNT = 힙[data_ARRAY + 1]; if (시작변위 < 0 || pagpasok_COUNT < 0 || 시작변위 > 힙[data_ARRAY + 1] - pagpasok_COUNT) { 예외던짐(6, "stream array bounds"); return; } }
            else pagpasok_COUNT = 1;
            if (pagpasok_COUNT == 0) { if (읽기여부) 넣기(0, 1); return; }
            int 완료수 = information_technology_sumulat_operasyon ? 힙[bagay_Sanggunian + 4] : 0, 처리값 = 0;
            while (완료수 < pagpasok_COUNT) {
                처리값 = 읽기여부 ? gumagamit.파일한바이트읽기(열린파일번호) : gumagamit.파일한바이트쓰기(열린파일번호, i_block || information_technology_SUBARRAY ? 힙[data_ARRAY + 2 + 시작변위 + 완료수] : data_VALUE);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (i_block || information_technology_SUBARRAY)) 힙[data_ARRAY + 2 + 시작변위 + 완료수] = (byte)처리값;
                완료수++; if (읽기여부 && !(i_block || information_technology_SUBARRAY)) break;
            }
            if (처리값 == -11 && (information_technology_sumulat_operasyon || 완료수 == 0)) {
                힙[bagay_Sanggunian + 4] = 완료수;
                if (흐름대기(부모참조)) { 넣기(bagay_Sanggunian, 2); if (i_block || information_technology_SUBARRAY) 넣기(data_ARRAY, 2); if (information_technology_SUBARRAY) { 넣기(시작변위, 1); 넣기(pagpasok_COUNT, 1); } if (information_technology_sumulat_operasyon && !(i_block || information_technology_SUBARRAY)) 넣기(data_VALUE, 1); } return;
            }
            힙[bagay_Sanggunian + 4] = 0; 힙[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(완료수 == 0 && 처리값 == 256 ? -1 : i_block || information_technology_SUBARRAY ? 완료수 : 처리값, 1); return;
        }
        pagpalya_VALUE("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int pangalan_constant) {
        if (Word_SMS(pangalan_constant, "한국어/자체/window")) return 24;
        if (Word_SMS(pangalan_constant, "한국어/자체/label")) return 26;
        if (Word_SMS(pangalan_constant, "한국어/자체/button")) return 27;
        if (Word_SMS(pangalan_constant, "한국어/자체/SMS_field")) return 28;
        if (Word_SMS(pangalan_constant, "한국어/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int pangalan_constant) {
        return 한국어화면종(pangalan_constant) != 0 || Word_SMS(pangalan_constant, "한국어/자체/화면구성요소") || Word_SMS(pangalan_constant, "한국어/자체/kaganapan_pila");
    }
    static int 화면종(int pangalan_constant) {
        int 한국어종 = 한국어화면종(pangalan_constant); if (한국어종 != 0) return 한국어종;
        if (Word_SMS(pangalan_constant, "javax/swing/JFrame")) return 24;
        if (Word_SMS(pangalan_constant, "javax/swing/JPanel")) return 25;
        if (Word_SMS(pangalan_constant, "javax/swing/JLabel")) return 26;
        if (Word_SMS(pangalan_constant, "javax/swing/JButton")) return 27;
        if (Word_SMS(pangalan_constant, "javax/swing/JTextField")) return 28;
        if (Word_SMS(pangalan_constant, "java/awt/event/ActionEvent")) return 29;
        if (Word_SMS(pangalan_constant, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int pangalan_constant) {
        return 화면종(pangalan_constant) != 0 || Word_SMS(pangalan_constant, "java/awt/Component") || Word_SMS(pangalan_constant, "java/awt/Container") || Word_SMS(pangalan_constant, "javax/swing/JComponent") || Word_SMS(pangalan_constant, "javax/swing/AbstractButton") || Word_SMS(pangalan_constant, "javax/swing/text/JTextComponent") || Word_SMS(pangalan_constant, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int bagay_Sanggunian) { if (!객체유효(bagay_Sanggunian)) return false; if (힙[bagay_Sanggunian] < 24 || 힙[bagay_Sanggunian] > 28) { pagpalya_VALUE("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int bagay_Sanggunian, int SMS_Sanggunian) {
        if (SMS_Sanggunian != 0 && !bagay_VALUE(SMS_Sanggunian, 1)) return;
        int pagpasok_COUNT = SMS_Sanggunian == 0 ? 0 : 힙[SMS_Sanggunian + 1]; if (pagpasok_COUNT > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < pagpasok_COUNT; Loop_INDEX++) 화면글임시[Loop_INDEX] = 힙[SMS_Sanggunian + 2 + Loop_INDEX];
        if (gumagamit.화면글(힙[bagay_Sanggunian + 2], 화면글임시, pagpasok_COUNT) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[bagay_Sanggunian + 3] = SMS_Sanggunian; 힙참조[bagay_Sanggunian + 3] = 1;
    }
    static int 화면문자읽기(int bagay_Sanggunian) {
        int account_VALUE = 힙[bagay_Sanggunian + 2], pagpasok_COUNT = gumagamit.화면연결(8, account_VALUE, 0, 0, 0, 0), 사용수 = 0;
        if (pagpasok_COUNT < 0) { pagpalya_VALUE("GUI text read failed"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < pagpasok_COUNT; Loop_INDEX++) { int 부호값 = gumagamit.화면연결(9, account_VALUE, Loop_INDEX, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = maglaan_Storage(1, 사용수); if (!error) for (int Loop_INDEX = 0; Loop_INDEX < 사용수; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 화면글임시[Loop_INDEX]; return 반환값;
    }
    /* 한국어 객체를 직접 만들고 kernel_VALUE 화면 기능에 연결한다. Swing bagay_VALUE/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int may_ari, int pangalan_constant, int 서술상수, int utos_CODE) {
        if (Word_SMS(may_ari, "한국어/자체/kaganapan_pila")) {
            if (utos_CODE == 184 && Word_SMS(pangalan_constant, "나중에실행") && Word_SMS(서술상수, "(L한국어/자체/실행할일;)V")) {
                int gawain_aksyon = 빼기(2); if (!객체유효(gawain_aksyon)) return;
                if (나중수 == 8) { pagpalya_VALUE("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = gawain_aksyon; return;
            }
            if (utos_CODE == 184 && Word_SMS(pangalan_constant, "사건처리중인가") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            pagpalya_VALUE("지원하지 않는 한국어 화면 일정 호출"); return;
        }
        if (Word_SMS(may_ari, "한국어/자체/동작알림")) {
            int 알림 = 빼기(2); if (!bagay_VALUE(알림, 29) || 힙[알림 + 3] == 0) return;
            if (Word_SMS(pangalan_constant, "kaganapan_pinagmulan") && Word_SMS(서술상수, "()L한국어/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (Word_SMS(pangalan_constant, "utos_SMS") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (Word_SMS(pangalan_constant, "INDEX") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else pagpalya_VALUE("지원하지 않는 한국어 aksyon 알림 호출"); return;
        }
        if (utos_CODE == 183 && Word_SMS(pangalan_constant, "<init>")) {
            int 종류 = 한국어화면종(may_ari), 받이 = 0, 가로 = 0, archive_posisyon = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Word_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (gumagamit.화면너비() - 폭) / 2; archive_posisyon = (gumagamit.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Word_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Word_SMS(서술상수, "(Ljava/lang/String;IIIIL한국어/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); archive_posisyon = 빼기(1); 가로 = 빼기(1);
            } else { pagpalya_VALUE("지원하지 않는 한국어 화면 생성자"); return; }
            int SMS = 빼기(2), elemento_VALUE = 빼기(2); if (!화면객체(elemento_VALUE)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || archive_posisyon < 0 || 폭 > gumagamit.화면너비() - 가로 || 높이 > gumagamit.화면높이() - archive_posisyon) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDEX = gumagamit.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (INDEX < 1 || INDEX > 32) { pagpalya_VALUE("화면 elemento_VALUE 자리가 가득 찼습니다"); return; }
            힙[elemento_VALUE + 2] = INDEX; 화면참조[INDEX - 1] = elemento_VALUE;
            힙[elemento_VALUE + 5] = 가로; 힙[elemento_VALUE + 6] = archive_posisyon; 힙[elemento_VALUE + 7] = 폭; 힙[elemento_VALUE + 8] = 높이; 힙[elemento_VALUE + 10] = 2;
            힙[elemento_VALUE + 4] = 받이; 힙참조[elemento_VALUE + 4] = 1; 힙[elemento_VALUE + 12] = 1;
            gumagamit.화면연결(1, INDEX, 가로, archive_posisyon, 폭, 높이);
            if (종류 == 24) gumagamit.화면연결(7, INDEX, 2, 0, 0, 0);
            화면문자설정(elemento_VALUE, SMS); return;
        }
        if (utos_CODE != 182) { pagpalya_VALUE("잘못된 한국어 화면 호출 utos"); return; }
        if (Word_SMS(pangalan_constant, "sumulat_SMS") && Word_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int SMS = 빼기(2), elemento_VALUE = 빼기(2); if (화면객체(elemento_VALUE)) 화면문자설정(elemento_VALUE, SMS); return;
        }
        if (Word_SMS(pangalan_constant, "글읽기") && Word_SMS(서술상수, "()Ljava/lang/String;")) {
            int elemento_VALUE = 빼기(2); if (화면객체(elemento_VALUE)) 넣기(화면문자읽기(elemento_VALUE), 2); return;
        }
        if (Word_SMS(pangalan_constant, "동작맡기기") && Word_SMS(서술상수, "(L한국어/자체/동작받이;)V")) {
            int 받이 = 빼기(2), elemento_VALUE = 빼기(2);
            if (화면객체(elemento_VALUE)) { 힙[elemento_VALUE + 4] = 받이; 힙참조[elemento_VALUE + 4] = 1; 힙[elemento_VALUE + 12] = 1; } return;
        }
        if (Word_SMS(pangalan_constant, "idagdag_elemento") && Word_SMS(서술상수, "(L한국어/자체/화면구성요소;)V")) {
            int anak_VALUE = 빼기(2), 부모 = 빼기(2); if (!화면객체(anak_VALUE) || !화면객체(부모)) return;
            if (gumagamit.화면연결(2, 힙[부모 + 2], 힙[anak_VALUE + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[anak_VALUE + 11] = 부모; 힙참조[anak_VALUE + 11] = 1; return;
        }
        if (Word_SMS(pangalan_constant, "자리정하기") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), archive_posisyon = 빼기(1), 가로 = 빼기(1), elemento_VALUE = 빼기(2); if (!화면객체(elemento_VALUE)) return;
            if (gumagamit.화면연결(1, 힙[elemento_VALUE + 2], 가로, archive_posisyon, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[elemento_VALUE + 5] = 가로; 힙[elemento_VALUE + 6] = archive_posisyon; 힙[elemento_VALUE + 7] = 폭; 힙[elemento_VALUE + 8] = 높이; return;
        }
        if ((Word_SMS(pangalan_constant, "ipakita_window") || Word_SMS(pangalan_constant, "isara")) && Word_SMS(서술상수, "()V")) {
            boolean pagiging_madaling_makita_VALUE = Word_SMS(pangalan_constant, "ipakita_window"); int elemento_VALUE = 빼기(2); if (!화면객체(elemento_VALUE)) return;
            if (gumagamit.화면연결(pagiging_madaling_makita_VALUE ? 3 : 4, 힙[elemento_VALUE + 2], pagiging_madaling_makita_VALUE ? 1 : 0, 0, 0, 0) < 0) { pagpalya_VALUE("화면은 tumutugon_interactive 명령에서 실행해야 합니다"); return; }
            힙[elemento_VALUE + 9] = pagiging_madaling_makita_VALUE ? 1 : 0; return;
        }
        if (Word_SMS(pangalan_constant, "보이는가") && Word_SMS(서술상수, "()Z")) { int elemento_VALUE = 빼기(2); if (화면객체(elemento_VALUE)) 넣기(힙[elemento_VALUE + 9], 1); return; }
        pagpalya_VALUE("지원하지 않는 한국어 화면 pamamaraan_VALUE");
    }
    static void 화면호출(int may_ari, int pangalan_constant, int 서술상수, int utos_CODE) {
        if (Word_SMS(may_ari, "javax/swing/SwingUtilities")) {
            if (utos_CODE == 184 && Word_SMS(pangalan_constant, "invokeLater") && Word_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int bagay_Sanggunian = 빼기(2); if (!객체유효(bagay_Sanggunian)) return; if (나중수 == 8) { pagpalya_VALUE("invokeLater queue full"); return; } 나중실행[나중수++] = bagay_Sanggunian; return; }
            if (utos_CODE == 184 && Word_SMS(pangalan_constant, "isEventDispatchThread") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            pagpalya_VALUE("unsupported SwingUtilities method"); return;
        }
        if (Word_SMS(may_ari, "java/awt/event/ActionEvent")) {
            int bagay_Sanggunian = 빼기(2); if (!bagay_VALUE(bagay_Sanggunian, 29)) return;
            if (Word_SMS(pangalan_constant, "getSource") && Word_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[bagay_Sanggunian + 2], 2);
            else if (Word_SMS(pangalan_constant, "getActionCommand") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[bagay_Sanggunian + 2]), 2);
            else if (Word_SMS(pangalan_constant, "getID") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else pagpalya_VALUE("unsupported ActionEvent method"); return;
        }
        if (utos_CODE == 183 && Word_SMS(pangalan_constant, "<init>")) {
            int COLUMNS = 0, SMS_Sanggunian = 0;
            if (Word_SMS(서술상수, "(I)V")) COLUMNS = 빼기(1);
            else if (Word_SMS(서술상수, "(Ljava/lang/String;I)V")) { COLUMNS = 빼기(1); SMS_Sanggunian = 빼기(2); }
            else if (Word_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_Sanggunian = 빼기(2);
            else if (Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_SMS(서술상수, "()V")) { pagpalya_VALUE("unsupported Swing constructor"); return; }
            int bagay_Sanggunian = 빼기(2); if (!객체유효(bagay_Sanggunian)) return;
            if (힙[bagay_Sanggunian] == 30) { pagpalya_VALUE("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(bagay_Sanggunian) || COLUMNS < 0) return;
            int account_VALUE = gumagamit.화면연결(0, 힙[bagay_Sanggunian] - 23, 0, 0, 0, 0);
            if (account_VALUE < 1 || account_VALUE > 32) { pagpalya_VALUE("GUI widget slots exhausted"); return; }
            힙[bagay_Sanggunian + 2] = account_VALUE; 화면참조[account_VALUE - 1] = bagay_Sanggunian; 힙[bagay_Sanggunian + 5] = 힙[bagay_Sanggunian] == 24 ? 130 : 16; 힙[bagay_Sanggunian + 6] = 힙[bagay_Sanggunian] == 24 ? 110 : 16;
            힙[bagay_Sanggunian + 7] = 힙[bagay_Sanggunian] == 24 ? 380 : 220; 힙[bagay_Sanggunian + 8] = 힙[bagay_Sanggunian] == 24 ? 240 : 28; 힙[bagay_Sanggunian + 10] = 1;
            화면문자설정(bagay_Sanggunian, SMS_Sanggunian); return;
        }
        if (Word_SMS(pangalan_constant, "setText") || Word_SMS(pangalan_constant, "setTitle")) { int SMS_Sanggunian = 빼기(2), bagay_Sanggunian = 빼기(2); if (화면객체(bagay_Sanggunian) && Word_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(bagay_Sanggunian, SMS_Sanggunian); return; }
        if (Word_SMS(pangalan_constant, "getText") || Word_SMS(pangalan_constant, "getTitle")) { int bagay_Sanggunian = 빼기(2); if (화면객체(bagay_Sanggunian) && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(bagay_Sanggunian), 2); return; }
        if (Word_SMS(pangalan_constant, "addActionListener") && Word_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), bagay_Sanggunian = 빼기(2); if (화면객체(bagay_Sanggunian)) { 힙[bagay_Sanggunian + 4] = 수신참조; 힙참조[bagay_Sanggunian + 4] = 1; } return; }
        if (Word_SMS(pangalan_constant, "getContentPane") && Word_SMS(서술상수, "()Ljava/awt/Container;")) { int bagay_Sanggunian = 빼기(2); if (화면객체(bagay_Sanggunian)) 넣기(bagay_Sanggunian, 2); return; }
        if (Word_SMS(pangalan_constant, "setLayout") && Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Layout_Sanggunian = 빼기(2), bagay_Sanggunian = 빼기(2); if (화면객체(bagay_Sanggunian) && Layout_Sanggunian != 0) pagpalya_VALUE("only absolute layout (null) is supported"); return; }
        if (Word_SMS(pangalan_constant, "add") && (Word_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Layout_kondisyon = Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Layout_kondisyon) 빼기(2);
            int anak_Sanggunian = 빼기(2), bagay_Sanggunian = 빼기(2); if (!화면객체(anak_Sanggunian) || !화면객체(bagay_Sanggunian)) return;
            if (gumagamit.화면연결(2, 힙[bagay_Sanggunian + 2], 힙[anak_Sanggunian + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[anak_Sanggunian + 11] = bagay_Sanggunian; 힙참조[anak_Sanggunian + 11] = 1; if (!Layout_kondisyon) 넣기(anak_Sanggunian, 2); return;
        }
        if (Word_SMS(pangalan_constant, "setBounds") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), Y_button_coordinate = 빼기(1), x_coordinate = 빼기(1), bagay_Sanggunian = 빼기(2); if (!화면객체(bagay_Sanggunian)) return;
            if (gumagamit.화면연결(1, 힙[bagay_Sanggunian + 2], x_coordinate, Y_button_coordinate, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[bagay_Sanggunian + 5] = x_coordinate; 힙[bagay_Sanggunian + 6] = Y_button_coordinate; 힙[bagay_Sanggunian + 7] = 너비; 힙[bagay_Sanggunian + 8] = 높이; return;
        }
        if (Word_SMS(pangalan_constant, "setSize") && Word_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), bagay_Sanggunian = 빼기(2); if (!화면객체(bagay_Sanggunian)) return;
            if (gumagamit.화면연결(1, 힙[bagay_Sanggunian + 2], 힙[bagay_Sanggunian + 5], 힙[bagay_Sanggunian + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[bagay_Sanggunian + 7] = 너비; 힙[bagay_Sanggunian + 8] = 높이; } return;
        }
        if (Word_SMS(pangalan_constant, "setLocationRelativeTo") && Word_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), bagay_Sanggunian = 빼기(2); if (!화면객체(bagay_Sanggunian)) return; if (상대배치 != 0) { pagpalya_VALUE("only screen centering supported"); return; } 힙[bagay_Sanggunian + 5] = (gumagamit.화면너비() - 힙[bagay_Sanggunian + 7]) / 2; 힙[bagay_Sanggunian + 6] = (gumagamit.화면높이() - 힙[bagay_Sanggunian + 8]) / 2; gumagamit.화면연결(1, 힙[bagay_Sanggunian + 2], 힙[bagay_Sanggunian + 5], 힙[bagay_Sanggunian + 6], 힙[bagay_Sanggunian + 7], 힙[bagay_Sanggunian + 8]); return; }
        if (Word_SMS(pangalan_constant, "setDefaultCloseOperation") && Word_SMS(서술상수, "(I)V")) { int patakaran = 빼기(1), bagay_Sanggunian = 빼기(2); if (화면객체(bagay_Sanggunian)) { if (patakaran < 0 || patakaran > 3) 예외던짐(9, "close policy"); else { 힙[bagay_Sanggunian + 10] = patakaran; gumagamit.화면연결(7, 힙[bagay_Sanggunian + 2], patakaran, 0, 0, 0); } } return; }
        if (Word_SMS(pangalan_constant, "setVisible") && Word_SMS(서술상수, "(Z)V")) { int data_VALUE = 빼기(1), bagay_Sanggunian = 빼기(2); if (화면객체(bagay_Sanggunian)) { int 처리값 = gumagamit.화면연결(3, 힙[bagay_Sanggunian + 2], data_VALUE, 0, 0, 0); if (처리값 < 0) pagpalya_VALUE("Swing requires a standalone interactive command"); else 힙[bagay_Sanggunian + 9] = data_VALUE; } return; }
        if (Word_SMS(pangalan_constant, "dispose") && Word_SMS(서술상수, "()V")) { int bagay_Sanggunian = 빼기(2); if (화면객체(bagay_Sanggunian)) { gumagamit.화면연결(4, 힙[bagay_Sanggunian + 2], 0, 0, 0, 0); 힙[bagay_Sanggunian + 9] = 0; } return; }
        if (Word_SMS(pangalan_constant, "repaint") || Word_SMS(pangalan_constant, "validate")) { int bagay_Sanggunian = 빼기(2); if (!화면객체(bagay_Sanggunian) || !Word_SMS(서술상수, "()V")) return; gumagamit.화면연결(1, 힙[bagay_Sanggunian + 2], 힙[bagay_Sanggunian + 5], 힙[bagay_Sanggunian + 6], 힙[bagay_Sanggunian + 7], 힙[bagay_Sanggunian + 8]); return; }
        if (Word_SMS(pangalan_constant, "isVisible") && Word_SMS(서술상수, "()Z")) { int bagay_Sanggunian = 빼기(2); if (화면객체(bagay_Sanggunian)) 넣기(힙[bagay_Sanggunian + 9], 1); return; }
        pagpalya_VALUE("unsupported Swing method (native subset)");
    }
    static void 사건실행(int target_email, int 사건번호, boolean 한국어) {
        if (target_email < 1 || 힙[target_email] < 32) { pagpalya_VALUE("Java event listener required"); return; }
        int file_INDEX = pangalan_pamamaraan(힙[target_email] - 32, 사건번호 == 0 ? (한국어 ? "Mag_execute_gawain" : "run") : (한국어 ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (한국어 ? "(L한국어/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (file_INDEX < 0) { pagpalya_VALUE("event callback missing"); return; }
        현재가닥 = 0; thread_COUNT = 1; frame_INDEX = 0; thread_katayuan[0] = 1; frame_Stack[0] = 0; 틀잠금[0] = magsimula_frame[0] = 0; 바꿈요청 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 128; Loop_INDEX++) { lokal_VALUE[Loop_INDEX] = lokal_TYPE[Loop_INDEX] = 0; }
        frame_pamamaraan[0] = file_INDEX; frame_posisyon[0] = pamamaraan_Start[file_INDEX]; lokal_VALUE[0] = target_email; lokal_TYPE[0] = 2;
        if (사건번호 != 0) { lokal_VALUE[1] = 사건번호; lokal_TYPE[1] = 2; }
        사건중 = true; Mag_execute_utos(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!error) {
            if (나중수 > 0) { int target_email = 나중실행[0], 한국어 = 나중한국어[0]; for (int Loop_INDEX = 1; Loop_INDEX < 나중수; Loop_INDEX++) { 나중실행[Loop_INDEX - 1] = 나중실행[Loop_INDEX]; 나중한국어[Loop_INDEX - 1] = 나중한국어[Loop_INDEX]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(target_email, 0, 한국어 != 0); continue; }
            if (gumagamit.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = gumagamit.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { pagpalya_VALUE("GUI event I/O failed"); return; }
            int account_VALUE = 사건번호 & 65535; if (account_VALUE < 1 || account_VALUE > 32) continue; int bagay_Sanggunian = 화면참조[account_VALUE - 1]; if (bagay_Sanggunian == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[bagay_Sanggunian + 10] != 0) 힙[bagay_Sanggunian + 9] = 0;
                if (힙[bagay_Sanggunian + 10] == 3) for (int Loop_INDEX = 0; Loop_INDEX < 32; Loop_INDEX++) if (화면참조[Loop_INDEX] != 0 && 힙[화면참조[Loop_INDEX]] == 24) gumagamit.화면연결(4, Loop_INDEX + 1, 0, 0, 0, 0);
            } else if (힙[bagay_Sanggunian + 4] != 0) {
                int BASAHINAKO_Sanggunian = maglaan_Storage(29, 2); if (error) return; 힙[BASAHINAKO_Sanggunian + 2] = bagay_Sanggunian; 힙[BASAHINAKO_Sanggunian + 3] = 힙[bagay_Sanggunian + 12]; 힙참조[BASAHINAKO_Sanggunian + 2] = 1; 사건실행(힙[bagay_Sanggunian + 4], BASAHINAKO_Sanggunian, 힙[bagay_Sanggunian + 12] != 0);
            }
        }
    }
    public static int run() {
        if (gumagamit.인수개수() == 1 && 자바도구.같음(gumagamit.인수(0), "-version")) {
            gumagamit.sumulat("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (gumagamit.인수개수() < 1) { gumagamit.sumulat("Usage: java CLASS [ARGS]\n"); return 2; }
        pagpasok_kategorya_Kahulugan = load_kategorya_Kahulugan(host_karakter(gumagamit.인수(0))); if (error || pagpasok_kategorya_Kahulugan < 0) return 1;
        int pagpasok_point_VALUE = pangalan_pamamaraan(pagpasok_kategorya_Kahulugan, "run", "()V");
        boolean 한국어진입 = pagpasok_point_VALUE >= 0 && (pamamaraan_access[pagpasok_point_VALUE] & 9) == 9;
        if (!한국어진입) pagpasok_point_VALUE = pangalan_pamamaraan(pagpasok_kategorya_Kahulugan, "main", "([Ljava/lang/String;)V");
        if (pagpasok_point_VALUE < 0 || (pamamaraan_access[pagpasok_point_VALUE] & 9) != 9) pagpalya_VALUE("public static void run() or main(String[] args) required");
        if (error) return 1;
        int 인수 = maglaan_Storage(3, gumagamit.인수개수() - 1); ARRAY_elemento[인수] = -1;
        for (int 수 = 1; 수 < gumagamit.인수개수() && !error; 수++) 힙[인수 + 1 + 수] = host_karakter(gumagamit.인수(수));
        frame_INDEX = 0; frame_pamamaraan[0] = pagpasok_point_VALUE; frame_posisyon[0] = pamamaraan_Start[pagpasok_point_VALUE]; lokal_VALUE[0] = 한국어진입 ? 0 : 인수; lokal_TYPE[0] = 한국어진입 ? 0 : 2;
        thread_katayuan[0] = 1; thread_bagay[0] = maglaan_Storage(13, 2);
        Mag_execute_utos(); if (!error) 화면사건들(); return error ? 1 : 0;
    }
}
