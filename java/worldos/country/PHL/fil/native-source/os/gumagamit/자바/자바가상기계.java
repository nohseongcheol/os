// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. file/스택/Sanggunian/sanga 경계를 Mag_execute_utos 중 검사한다. */
public final class 자바가상기계 {
    static int[] file = new int[16384], file_pangalan_SMS = new int[64];
    static int[] constant_tag = new int[512], 상가 = new int[512], constant_SECOND_VALUE = new int[512], string_Sanggunian = new int[512];
    static int[] pamamaraan_pangalan_SMS = new int[32], pamamaraan_TYPE = new int[32], pamamaraan_access = new int[32];
    static int[] pamamaraan_Start = new int[32], pamamaraan_tapusin = new int[32], pamamaraan_Stack = new int[32], 함수지역 = new int[32];
    static int[] pamamaraan_argumento_COUNT = new int[32], pamamaraan_argumento_TYPE = new int[512], 함수반환 = new int[32];
    static int[] 경계 = new int[16384];
    static int[] lokal_VALUE = new int[4096], lokal_TYPE = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] frame_pamamaraan = new int[32], frame_posisyon = new int[32], frame_Stack = new int[32];
    static int[] 힙 = new int[8192];
    static int sukat_82232621, 읽기위치, constant_COUNT, pamamaraan_COUNT, kategorya_pangalan, frame_INDEX = -1, 힙끝 = 1, 반환형;
    static boolean error;

    static void pagpalya_VALUE(String Word_SMS) {
        if (!error) { gumagamit.sumulat("JVM error: "); gumagamit.sumulat(Word_SMS); gumagamit.sumulat_karakter_VALUE(10); }
        error = true;
    }
    static boolean clip(int run, int haba_VALUE) { return run >= 0 && haba_VALUE >= 0 && run <= sukat_82232621 - haba_VALUE; }
    static int byte_VALUE() {
        if (!clip(읽기위치, 1)) { pagpalya_VALUE("truncated class file"); return 0; }
        return file[읽기위치++];
    }
    static int 짧은수() { return byte_VALUE() << 8 | byte_VALUE(); }
    static int integer_buong_numero() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int haba_VALUE) { if (!clip(읽기위치, haba_VALUE)) pagpalya_VALUE("invalid attribute size"); else 읽기위치 += haba_VALUE; }
    static boolean tseke_constant(int 수, int 종류) {
        if (수 <= 0 || 수 >= constant_COUNT || constant_tag[수] != 종류) { pagpalya_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int run, int haba_VALUE, String Word_SMS) {
        if (!clip(run, haba_VALUE) || haba_VALUE != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < haba_VALUE; 수++) if (file[run + 수] != Word_SMS.charAt(수)) return false;
        return true;
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
    static void 속성건너() {
        int item_COUNT = 짧은수();
        for (int 수 = 0; 수 < item_COUNT && !error; 수++) { tseke_constant(짧은수(), 1); 건너(integer_buong_numero()); }
    }
    static int utos_haba(int VALUE) {
        if (VALUE == 16 || VALUE == 18 || VALUE == 21 || VALUE == 25 || VALUE == 54 || VALUE == 58 || VALUE == 188) return 2;
        if (VALUE == 17 || VALUE == 19 || VALUE == 132 || VALUE >= 153 && VALUE <= 167
            || VALUE >= 178 && VALUE <= 184 || VALUE == 187 || VALUE == 189 || VALUE == 192 || VALUE == 198 || VALUE == 199) return 3;
        if (VALUE >= 0 && VALUE <= 8 || VALUE >= 26 && VALUE <= 29 || VALUE >= 42 && VALUE <= 46 || VALUE == 50
            || VALUE >= 59 && VALUE <= 62 || VALUE >= 75 && VALUE <= 79 || VALUE == 83 || VALUE == 87 || VALUE == 89 || VALUE == 95
            || VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 116
            || VALUE == 120 || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130
            || VALUE >= 145 && VALUE <= 147 || VALUE == 172 || VALUE == 176 || VALUE == 177 || VALUE == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (integer_buong_numero() != 0xcafebabe) pagpalya_VALUE("not a class file");
        int 부판 = 짧은수(), bersyon_VALUE = 짧은수();
        if (bersyon_VALUE < 45 || bersyon_VALUE > 52 || 부판 != 0) pagpalya_VALUE("supported class versions: 45..52, minor 0");
        constant_COUNT = 짧은수();
        if (constant_COUNT < 1 || constant_COUNT > 512) { pagpalya_VALUE("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < constant_COUNT && !error; 수++) {
            int 종류 = byte_VALUE(); constant_tag[수] = 종류;
            if (종류 == 1) { constant_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(constant_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = integer_buong_numero();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); constant_SECOND_VALUE[수] = 짧은수(); }
            else pagpalya_VALUE("unsupported constant type");
        }
        int pahintulot_VALUE = 짧은수();
        if ((pahintulot_VALUE & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) pagpalya_VALUE("unsupported class flags");
        kategorya_pangalan = kategorya_pangalan_SMS(짧은수());
        if (!Word_SMS(kategorya_pangalan_SMS(짧은수()), "java/lang/Object")) pagpalya_VALUE("inheritance unsupported");
        if (짧은수() != 0) pagpalya_VALUE("interfaces unsupported");
        if (짧은수() != 0) pagpalya_VALUE("fields unsupported");
        pamamaraan_COUNT = 짧은수();
        if (pamamaraan_COUNT < 1 || pamamaraan_COUNT > 32) { pagpalya_VALUE("method count limit (32)"); return; }
        for (int 수 = 0; 수 < pamamaraan_COUNT && !error; 수++) {
            pamamaraan_access[수] = 짧은수(); pamamaraan_pangalan_SMS[수] = 짧은수(); pamamaraan_TYPE[수] = 짧은수();
            tseke_constant(pamamaraan_pangalan_SMS[수], 1); 서술읽기(수);
            if ((pamamaraan_access[수] & (0x100 | 0x400 | 0x20)) != 0) pagpalya_VALUE("native, abstract and synchronized methods unsupported");
            if ((pamamaraan_access[수] & 8) == 0 && !Word_SMS(pamamaraan_pangalan_SMS[수], "<init>")) pagpalya_VALUE("instance methods unsupported");
            if (Word_SMS(pamamaraan_pangalan_SMS[수], "<clinit>")) pagpalya_VALUE("class initializers unsupported");
            for (int nasa_harap_VALUE = 0; nasa_harap_VALUE < 수; nasa_harap_VALUE++) if (같은말(pamamaraan_pangalan_SMS[nasa_harap_VALUE], pamamaraan_pangalan_SMS[수]) && 같은말(pamamaraan_TYPE[nasa_harap_VALUE], pamamaraan_TYPE[수])) pagpalya_VALUE("duplicate method");
            int item_COUNT = 짧은수();
            for (int katangian_VALUE = 0; katangian_VALUE < item_COUNT && !error; katangian_VALUE++) {
                int pangalan = 짧은수(), haba_VALUE = integer_buong_numero(), run = 읽기위치;
                if (!clip(run, haba_VALUE)) { pagpalya_VALUE("truncated method attribute"); break; }
                if (Word_SMS(pangalan, "Code")) {
                    if (pamamaraan_Start[수] != 0) pagpalya_VALUE("duplicate Code attribute");
                    pamamaraan_Stack[수] = 짧은수(); 함수지역[수] = 짧은수(); int CODE_haba = integer_buong_numero();
                    if (pamamaraan_Stack[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < pamamaraan_argumento_COUNT[수]
                        || CODE_haba < 1 || CODE_haba > 8192) pagpalya_VALUE("method memory limits exceeded");
                    pamamaraan_Start[수] = 읽기위치; 건너(CODE_haba); pamamaraan_tapusin[수] = 읽기위치;
                    if (짧은수() != 0) pagpalya_VALUE("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != run + haba_VALUE) pagpalya_VALUE("Code attribute size mismatch");
                } else 건너(haba_VALUE);
            }
            if (pamamaraan_Start[수] == 0) pagpalya_VALUE("missing Code attribute");
            int espasyo_pagpasok = pamamaraan_Start[수];
            while (espasyo_pagpasok < pamamaraan_tapusin[수] && !error) {
                int haba_VALUE = utos_haba(file[espasyo_pagpasok]);
                if (haba_VALUE == 0 || haba_VALUE > pamamaraan_tapusin[수] - espasyo_pagpasok) { pagpalya_VALUE("unsupported or truncated bytecode"); break; }
                경계[espasyo_pagpasok] = 수 + 1; espasyo_pagpasok += haba_VALUE;
            }
            // 실행하지 않는 경로에도 잘못된 sanga 목적지를 허용하지 않는다.
            espasyo_pagpasok = pamamaraan_Start[수];
            while (espasyo_pagpasok < pamamaraan_tapusin[수] && !error) {
                int VALUE = file[espasyo_pagpasok];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                    int patutunguhan_VALUE = espasyo_pagpasok + (short)(file[espasyo_pagpasok + 1] << 8 | file[espasyo_pagpasok + 2]);
                    if (patutunguhan_VALUE < pamamaraan_Start[수] || patutunguhan_VALUE >= pamamaraan_tapusin[수] || 경계[patutunguhan_VALUE] != 수 + 1) pagpalya_VALUE("invalid branch target");
                }
                espasyo_pagpasok += utos_haba(VALUE);
            }
        }
        if (!error) 속성건너();
        if (읽기위치 != sukat_82232621) pagpalya_VALUE("extra class file data");
    }
    static int maglaan_Storage(int 종류, int haba_VALUE) {
        if (haba_VALUE < 0 || haba_VALUE > 힙.length - 힙끝 - 2) { pagpalya_VALUE("object heap exhausted or negative array size"); return 0; }
        int Sanggunian = 힙끝; 힙끝 += haba_VALUE + 2; 힙[Sanggunian] = 종류; 힙[Sanggunian + 1] = haba_VALUE;
        return Sanggunian;
    }
    static boolean bagay_VALUE(int Sanggunian, int 종류) {
        if (Sanggunian < 1 || Sanggunian >= 힙끝 - 1 || 힙[Sanggunian] != 종류) { pagpalya_VALUE("null or invalid object reference"); return false; }
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
        if (frame_INDEX == 31) { pagpalya_VALUE("call stack limit (32)"); return; }
        int Susunod_item = frame_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) lokal_TYPE[Susunod_item * 128 + 수] = 0;
        for (int 수 = pamamaraan_argumento_COUNT[pormula_VALUE] - 1; 수 >= 0; 수--) {
            lokal_VALUE[Susunod_item * 128 + 수] = 빼기(pamamaraan_argumento_TYPE[pormula_VALUE * 16 + 수]); lokal_TYPE[Susunod_item * 128 + 수] = pamamaraan_argumento_TYPE[pormula_VALUE * 16 + 수];
        }
        frame_INDEX = Susunod_item; frame_pamamaraan[frame_INDEX] = pormula_VALUE; frame_posisyon[frame_INDEX] = pamamaraan_Start[pormula_VALUE]; frame_Stack[frame_INDEX] = 0;
    }
    static void 반환(int TYPE_VALUE) {
        if (TYPE_VALUE != 함수반환[frame_pamamaraan[frame_INDEX]]) { pagpalya_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        frame_INDEX--; if (frame_INDEX >= 0 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
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
                if (VALUE < 1 || VALUE > 127) { pagpalya_VALUE("file stream paths currently require ASCII"); return; }
                Stream_file_pangalan[espasyo_pagpasok] = VALUE;
            }
            Stream_file_pangalan[haba_VALUE] = 0;
            int 서술자 = gumagamit.파일서술자열기(Stream_file_pangalan, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { pagpalya_VALUE("FileNotFoundException: file open failed"); return; }
            힙[Stream_VALUE + 2] = 서술자; 힙[Stream_VALUE + 3] = 1;
            return;
        }
        if (utos != 182) { pagpalya_VALUE("invalid file stream invocation"); return; }
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
            if (sukat < -1) pagpalya_VALUE("IOException: read failed"); else 넣기(sukat, 1);
        } else if (gumagamit.파일한바이트쓰기(서술자, VALUE) != 1) pagpalya_VALUE("IOException: write failed");
    }
    static void CALL_pamamaraan(int INDEX, int utos) {
        if (!tseke_constant(INDEX, 10)) return;
        int may_ari_VALUE = kategorya_pangalan_SMS(상가[INDEX]), pangalan = Sanggunian_pangalan(constant_SECOND_VALUE[INDEX]), format_VALUE = Sanggunian_TYPE(constant_SECOND_VALUE[INDEX]);
        if (error) return;
        if (같은말(may_ari_VALUE, kategorya_pangalan)) {
            if (utos != 184) { pagpalya_VALUE("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < pamamaraan_COUNT; 수++) if (같은말(pangalan, pamamaraan_pangalan_SMS[수]) && 같은말(format_VALUE, pamamaraan_TYPE[수])) {
                if ((pamamaraan_access[수] & 8) == 0) pagpalya_VALUE("method is not static"); else 호출(수);
                return;
            }
            pagpalya_VALUE("NoSuchMethodError"); return;
        }
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
        pagpalya_VALUE("unsupported library method");
    }
    static int ARRAY_espasyo(int Sanggunian, int subscript_VALUE, int TYPE_VALUE) {
        if (!bagay_VALUE(Sanggunian, TYPE_VALUE)) return 0;
        if (subscript_VALUE < 0 || subscript_VALUE >= 힙[Sanggunian + 1]) { pagpalya_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return Sanggunian + 2 + subscript_VALUE;
    }
    static void Mag_execute_utos() {
        int 남음 = 500000;
        while (frame_INDEX >= 0 && !error) {
            if (--남음 == 0) { pagpalya_VALUE("instruction limit (500000)"); break; }
            int run = frame_posisyon[frame_INDEX], VALUE = 명바();
            if (error) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = VALUE == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= constant_COUNT) pagpalya_VALUE("invalid ldc constant");
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
            if (VALUE == 46 || VALUE == 50) {
                int subscript_VALUE = 빼기(1), Sanggunian = 빼기(2), espasyo_pagpasok = ARRAY_espasyo(Sanggunian, subscript_VALUE, VALUE == 46 ? 2 : 3);
                if (!error) 넣기(힙[espasyo_pagpasok], VALUE == 46 ? 1 : 2); continue;
            }
            if (VALUE == 79 || VALUE == 83) {
                int item_elemento = 빼기(VALUE == 79 ? 1 : 2), subscript_VALUE = 빼기(1), Sanggunian = 빼기(2), espasyo_pagpasok = ARRAY_espasyo(Sanggunian, subscript_VALUE, VALUE == 79 ? 2 : 3);
                if (VALUE == 83 && item_elemento != 0) bagay_VALUE(item_elemento, 1);
                if (!error) 힙[espasyo_pagpasok] = item_elemento; continue;
            }
            if (VALUE == 87) { 빼기(0); continue; }
            if (VALUE == 89) { int 가 = 빼기(0), TYPE_VALUE = 반환형; 넣기(가, TYPE_VALUE); 넣기(가, TYPE_VALUE); continue; }
            if (VALUE == 95) { int 가 = 빼기(0), 가형 = 반환형, 나 = 빼기(0), 나형 = 반환형; 넣기(가, 가형); 넣기(나, 나형); continue; }
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
            if (VALUE == 178) {
                int 수 = 명짧(); if (!tseke_constant(수, 9)) continue;
                if (!Word_SMS(kategorya_pangalan_SMS(상가[수]), "java/lang/System") || !Word_SMS(Sanggunian_pangalan(constant_SECOND_VALUE[수]), "out")
                    || !Word_SMS(Sanggunian_TYPE(constant_SECOND_VALUE[수]), "Ljava/io/PrintStream;")) pagpalya_VALUE("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (VALUE == 182 || VALUE == 183 || VALUE == 184) { CALL_pamamaraan(명짧(), VALUE); continue; }
            if (VALUE == 187) {
                int pangalan = kategorya_pangalan_SMS(명짧());
                if (Word_SMS(pangalan, "java/lang/StringBuilder")) 넣기(maglaan_Storage(4, 1), 2);
                else if (Word_SMS(pangalan, "java/io/FileInputStream") || Word_SMS(pangalan, "java/io/FileOutputStream")) {
                    int Sanggunian = maglaan_Storage(Word_SMS(pangalan, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!error) { 힙[Sanggunian + 2] = -1; 넣기(Sanggunian, 2); }
                } else pagpalya_VALUE("unsupported object construction");
                continue;
            }
            if (VALUE == 188 || VALUE == 189) {
                if (VALUE == 188) { if (명바() != 10) pagpalya_VALUE("only int[] newarray is supported"); }
                else if (!Word_SMS(kategorya_pangalan_SMS(명짧()), "java/lang/String")) pagpalya_VALUE("only String[] anewarray is supported");
                int haba_VALUE = 빼기(1); 넣기(maglaan_Storage(VALUE == 188 ? 2 : 3, haba_VALUE), 2); continue;
            }
            if (VALUE == 190) {
                int Sanggunian = 빼기(2);
                if (Sanggunian < 1 || Sanggunian >= 힙끝 - 1 || (힙[Sanggunian] != 2 && 힙[Sanggunian] != 3)) pagpalya_VALUE("null or invalid array");
                else 넣기(힙[Sanggunian + 1], 1); continue;
            }
            if (VALUE == 192) {
                int pangalan = kategorya_pangalan_SMS(명짧()), Sanggunian = 빼기(2);
                if (!Word_SMS(pangalan, "java/lang/String")) pagpalya_VALUE("unsupported checkcast");
                else if (Sanggunian != 0) bagay_VALUE(Sanggunian, 1);
                넣기(Sanggunian, 2); continue;
            }
            pagpalya_VALUE("unsupported bytecode");
        }
    }
    public static int run() {
        if (gumagamit.인수개수() == 1 && 자바도구.같음(gumagamit.인수(0), "-version")) {
            gumagamit.sumulat("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (gumagamit.인수개수() < 1) { gumagamit.sumulat("Usage: java CLASS [ARGS]\n"); return 2; }
        int haba_VALUE = 자바도구.pangalan(file_pangalan_SMS, gumagamit.인수(0));
        if (haba_VALUE < 1 || haba_VALUE > 57) { gumagamit.sumulat("java: invalid class name\n"); return 2; }
        file_pangalan_SMS[haba_VALUE] = '.'; file_pangalan_SMS[haba_VALUE + 1] = 'c'; file_pangalan_SMS[haba_VALUE + 2] = 'l'; file_pangalan_SMS[haba_VALUE + 3] = 'a'; file_pangalan_SMS[haba_VALUE + 4] = 's'; file_pangalan_SMS[haba_VALUE + 5] = 's';
        sukat_82232621 = gumagamit.파일읽기(file_pangalan_SMS, file);
        if (sukat_82232621 < 0) { gumagamit.sumulat("java: cannot read class: "); 자바도구.수쓰기(sukat_82232621); gumagamit.sumulat_karakter_VALUE(10); return 1; }
        클래스읽기(); if (error) return 1;
        int karakter_pangalan = constant_SMS(kategorya_pangalan);
        if (!error && 힙[karakter_pangalan + 1] != haba_VALUE) pagpalya_VALUE("class name does not match file");
        for (int 수 = 0; 수 < haba_VALUE && !error; 수++) if (힙[karakter_pangalan + 2 + 수] != file_pangalan_SMS[수]) pagpalya_VALUE("class name does not match file");
        int pagpasok_point_VALUE = -1;
        for (int 수 = 0; 수 < pamamaraan_COUNT; 수++) if (Word_SMS(pamamaraan_pangalan_SMS[수], "main") && Word_SMS(pamamaraan_TYPE[수], "([Ljava/lang/String;)V") && (pamamaraan_access[수] & 9) == 9) pagpasok_point_VALUE = 수;
        if (pagpasok_point_VALUE < 0) pagpalya_VALUE("public static void main(String[] args) required");
        if (error) return 1;
        int 인수 = maglaan_Storage(3, gumagamit.인수개수() - 1);
        for (int 수 = 1; 수 < gumagamit.인수개수() && !error; 수++) 힙[인수 + 1 + 수] = host_karakter(gumagamit.인수(수));
        frame_INDEX = 0; frame_pamamaraan[0] = pagpasok_point_VALUE; frame_posisyon[0] = pamamaraan_Start[pagpasok_point_VALUE]; lokal_VALUE[0] = 인수; lokal_TYPE[0] = 2;
        Mag_execute_utos(); return error ? 1 : 0;
    }
}
