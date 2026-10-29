// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Lêer/스택/Naslaan/tak 경계를 uitvoer_bevel 중 검사한다. */
public final class 자바가상기계 {
    static int[] Lêer = new int[16384], lêer_naam_SMS = new int[64];
    static int[] konstante_merk = new int[512], 상가 = new int[512], konstante_SECOND_VALUE = new int[512], string_Naslaan = new int[512];
    static int[] metode_naam_SMS = new int[32], metode_TYPE = new int[32], metode_toegang = new int[32];
    static int[] metode_BEGIN = new int[32], metode_beëindig = new int[32], metode_Stapel = new int[32], 함수지역 = new int[32];
    static int[] metode_argument_COUNT = new int[32], metode_argument_TYPE = new int[512], metode_teruggee = new int[32];
    static int[] 경계 = new int[16384];
    static int[] lokaal_VALUE = new int[4096], lokaal_TYPE = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] raam_metode = new int[32], raam_plaas = new int[32], raam_Stapel = new int[32];
    static int[] 힙 = new int[8192];
    static int Grootte, 읽기위치, konstante_COUNT, metode_COUNT, Klas_naam, raam_INDEX = -1, 힙끝 = 1, teruggee_TYPE;
    static boolean Fout;

    static void faling_VALUE(String Word_SMS) {
        if (!Fout) { gebruiker.Skryf("JVM error: "); gebruiker.Skryf(Word_SMS); gebruiker.skryf_karakter_VALUE(10); }
        Fout = true;
    }
    static boolean snit(int Loop, int lengte_VALUE) { return Loop >= 0 && lengte_VALUE >= 0 && Loop <= Grootte - lengte_VALUE; }
    static int greep_VALUE() {
        if (!snit(읽기위치, 1)) { faling_VALUE("truncated class file"); return 0; }
        return Lêer[읽기위치++];
    }
    static int 짧은수() { return greep_VALUE() << 8 | greep_VALUE(); }
    static int heelgetal() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int lengte_VALUE) { if (!snit(읽기위치, lengte_VALUE)) faling_VALUE("invalid attribute size"); else 읽기위치 += lengte_VALUE; }
    static boolean tjek_konstante(int 수, int 종류) {
        if (수 <= 0 || 수 >= konstante_COUNT || konstante_merk[수] != 종류) { faling_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Loop, int lengte_VALUE, String Word_SMS) {
        if (!snit(Loop, lengte_VALUE) || lengte_VALUE != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < lengte_VALUE; 수++) if (Lêer[Loop + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static boolean Word_SMS(int konstante_VALUE, String Word_SMS) { return tjek_konstante(konstante_VALUE, 1) && 구간(상가[konstante_VALUE], konstante_SECOND_VALUE[konstante_VALUE], Word_SMS); }
    static boolean 같은말(int 가, int 나) {
        if (!tjek_konstante(가, 1) || !tjek_konstante(나, 1) || konstante_SECOND_VALUE[가] != konstante_SECOND_VALUE[나]) return false;
        for (int 수 = 0; 수 < konstante_SECOND_VALUE[가]; 수++) if (Lêer[상가[가] + 수] != Lêer[상가[나] + 수]) return false;
        return true;
    }
    static int Klas_naam_SMS(int 수) { return tjek_konstante(수, 7) && tjek_konstante(상가[수], 1) ? 상가[수] : 0; }
    static int Naslaan_naam(int 수) { return tjek_konstante(수, 12) && tjek_konstante(상가[수], 1) ? 상가[수] : 0; }
    static int Naslaan_TYPE(int 수) { return tjek_konstante(수, 12) && tjek_konstante(konstante_SECOND_VALUE[수], 1) ? konstante_SECOND_VALUE[수] : 0; }
    static int 서술형(int 끝, boolean leeg_TYPE) {
        if (읽기위치 >= 끝) { faling_VALUE("invalid descriptor"); return 0; }
        int VALUE = greep_VALUE();
        if (VALUE == 'V' && leeg_TYPE) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int Loop = 읽기위치;
            while (읽기위치 < 끝 && Lêer[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Loop) faling_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        faling_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int funksie_VALUE) {
        int 이전 = 읽기위치, 수 = metode_TYPE[funksie_VALUE];
        if (!tjek_konstante(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + konstante_SECOND_VALUE[수];
        if (greep_VALUE() != '(') faling_VALUE("invalid method descriptor");
        int item_COUNT = 0;
        while (!Fout && 읽기위치 < 끝 && Lêer[읽기위치] != ')') {
            if (item_COUNT == 16) { faling_VALUE("too many method arguments"); break; }
            metode_argument_TYPE[funksie_VALUE * 16 + item_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || greep_VALUE() != ')') faling_VALUE("invalid method descriptor");
        metode_teruggee[funksie_VALUE] = 서술형(끝, true); metode_argument_COUNT[funksie_VALUE] = item_COUNT;
        if (읽기위치 != 끝) faling_VALUE("invalid method descriptor");
        읽기위치 = 이전;
    }
    static void 속성건너() {
        int item_COUNT = 짧은수();
        for (int 수 = 0; 수 < item_COUNT && !Fout; 수++) { tjek_konstante(짧은수(), 1); 건너(heelgetal()); }
    }
    static int bevel_lengte(int VALUE) {
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
        if (heelgetal() != 0xcafebabe) faling_VALUE("not a class file");
        int 부판 = 짧은수(), weergawe_VALUE = 짧은수();
        if (weergawe_VALUE < 45 || weergawe_VALUE > 52 || 부판 != 0) faling_VALUE("supported class versions: 45..52, minor 0");
        konstante_COUNT = 짧은수();
        if (konstante_COUNT < 1 || konstante_COUNT > 512) { faling_VALUE("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < konstante_COUNT && !Fout; 수++) {
            int 종류 = greep_VALUE(); konstante_merk[수] = 종류;
            if (종류 == 1) { konstante_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(konstante_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = heelgetal();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); konstante_SECOND_VALUE[수] = 짧은수(); }
            else faling_VALUE("unsupported constant type");
        }
        int toestemming_VALUE = 짧은수();
        if ((toestemming_VALUE & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) faling_VALUE("unsupported class flags");
        Klas_naam = Klas_naam_SMS(짧은수());
        if (!Word_SMS(Klas_naam_SMS(짧은수()), "java/lang/Object")) faling_VALUE("inheritance unsupported");
        if (짧은수() != 0) faling_VALUE("interfaces unsupported");
        if (짧은수() != 0) faling_VALUE("fields unsupported");
        metode_COUNT = 짧은수();
        if (metode_COUNT < 1 || metode_COUNT > 32) { faling_VALUE("method count limit (32)"); return; }
        for (int 수 = 0; 수 < metode_COUNT && !Fout; 수++) {
            metode_toegang[수] = 짧은수(); metode_naam_SMS[수] = 짧은수(); metode_TYPE[수] = 짧은수();
            tjek_konstante(metode_naam_SMS[수], 1); 서술읽기(수);
            if ((metode_toegang[수] & (0x100 | 0x400 | 0x20)) != 0) faling_VALUE("native, abstract and synchronized methods unsupported");
            if ((metode_toegang[수] & 8) == 0 && !Word_SMS(metode_naam_SMS[수], "<init>")) faling_VALUE("instance methods unsupported");
            if (Word_SMS(metode_naam_SMS[수], "<clinit>")) faling_VALUE("class initializers unsupported");
            for (int voor_VALUE = 0; voor_VALUE < 수; voor_VALUE++) if (같은말(metode_naam_SMS[voor_VALUE], metode_naam_SMS[수]) && 같은말(metode_TYPE[voor_VALUE], metode_TYPE[수])) faling_VALUE("duplicate method");
            int item_COUNT = 짧은수();
            for (int kenmerk_VALUE = 0; kenmerk_VALUE < item_COUNT && !Fout; kenmerk_VALUE++) {
                int Naam = 짧은수(), lengte_VALUE = heelgetal(), Loop = 읽기위치;
                if (!snit(Loop, lengte_VALUE)) { faling_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Naam, "Code")) {
                    if (metode_BEGIN[수] != 0) faling_VALUE("duplicate Code attribute");
                    metode_Stapel[수] = 짧은수(); 함수지역[수] = 짧은수(); int CODE_lengte = heelgetal();
                    if (metode_Stapel[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < metode_argument_COUNT[수]
                        || CODE_lengte < 1 || CODE_lengte > 8192) faling_VALUE("method memory limits exceeded");
                    metode_BEGIN[수] = 읽기위치; 건너(CODE_lengte); metode_beëindig[수] = 읽기위치;
                    if (짧은수() != 0) faling_VALUE("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != Loop + lengte_VALUE) faling_VALUE("Code attribute size mismatch");
                } else 건너(lengte_VALUE);
            }
            if (metode_BEGIN[수] == 0) faling_VALUE("missing Code attribute");
            int gleuf_inskrywing = metode_BEGIN[수];
            while (gleuf_inskrywing < metode_beëindig[수] && !Fout) {
                int lengte_VALUE = bevel_lengte(Lêer[gleuf_inskrywing]);
                if (lengte_VALUE == 0 || lengte_VALUE > metode_beëindig[수] - gleuf_inskrywing) { faling_VALUE("unsupported or truncated bytecode"); break; }
                경계[gleuf_inskrywing] = 수 + 1; gleuf_inskrywing += lengte_VALUE;
            }
            // 실행하지 않는 경로에도 잘못된 tak 목적지를 허용하지 않는다.
            gleuf_inskrywing = metode_BEGIN[수];
            while (gleuf_inskrywing < metode_beëindig[수] && !Fout) {
                int VALUE = Lêer[gleuf_inskrywing];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                    int bestemming_VALUE = gleuf_inskrywing + (short)(Lêer[gleuf_inskrywing + 1] << 8 | Lêer[gleuf_inskrywing + 2]);
                    if (bestemming_VALUE < metode_BEGIN[수] || bestemming_VALUE >= metode_beëindig[수] || 경계[bestemming_VALUE] != 수 + 1) faling_VALUE("invalid branch target");
                }
                gleuf_inskrywing += bevel_lengte(VALUE);
            }
        }
        if (!Fout) 속성건너();
        if (읽기위치 != Grootte) faling_VALUE("extra class file data");
    }
    static int toewys_Berging(int 종류, int lengte_VALUE) {
        if (lengte_VALUE < 0 || lengte_VALUE > 힙.length - 힙끝 - 2) { faling_VALUE("object heap exhausted or negative array size"); return 0; }
        int Naslaan = 힙끝; 힙끝 += lengte_VALUE + 2; 힙[Naslaan] = 종류; 힙[Naslaan + 1] = lengte_VALUE;
        return Naslaan;
    }
    static boolean objek_VALUE(int Naslaan, int 종류) {
        if (Naslaan < 1 || Naslaan >= 힙끝 - 1 || 힙[Naslaan] != 종류) { faling_VALUE("null or invalid object reference"); return false; }
        return true;
    }
    static int konstante_SMS(int INDEX) {
        if (!tjek_konstante(INDEX, 1)) return 0;
        if (string_Naslaan[INDEX] != 0) return string_Naslaan[INDEX];
        int Naslaan = toewys_Berging(1, konstante_SECOND_VALUE[INDEX]); if (Fout) return 0;
        int 끝 = 상가[INDEX] + konstante_SECOND_VALUE[INDEX], 수 = 상가[INDEX], lengte_VALUE = 0;
        while (수 < 끝 && !Fout) {
            int VALUE = Lêer[수++];
            if (VALUE == 0) faling_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && 수 < 끝) {
                int Volgende_item = Lêer[수++];
                if ((Volgende_item & 192) != 128) faling_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | Volgende_item & 63;
                if (VALUE != 0 && VALUE < 128) faling_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && 수 + 1 < 끝) {
                int 가 = Lêer[수++], 나 = Lêer[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) faling_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (VALUE < 2048) faling_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) faling_VALUE("invalid modified UTF-8");
            힙[Naslaan + 2 + lengte_VALUE++] = VALUE;
        }
        힙[Naslaan + 1] = lengte_VALUE; string_Naslaan[INDEX] = Naslaan; return Naslaan;
    }
    static int hou_karakter(String VALUE) {
        int Naslaan = toewys_Berging(1, VALUE.length()); if (Fout) return 0;
        for (int 수 = 0; 수 < VALUE.length(); 수++) 힙[Naslaan + 2 + 수] = VALUE.charAt(수);
        return Naslaan;
    }
    static void skryf_SMS(int Naslaan) {
        if (Naslaan == 0) { gebruiker.Skryf("null"); return; }
        if (!objek_VALUE(Naslaan, 1)) return;
        for (int 수 = 0; 수 < 힙[Naslaan + 1]; 수++) gebruiker.skryf_karakter_VALUE(힙[Naslaan + 2 + 수]);
    }
    static int syfer_karakter(int VALUE) {
        int Naslaan = toewys_Berging(1, 11); if (Fout) return 0;
        int lengte_VALUE = 0;
        if (VALUE < 0) 힙[Naslaan + 2 + lengte_VALUE++] = '-'; else VALUE = -VALUE;
        int plaas_INDEX = 1000000000; boolean Loop = false;
        while (plaas_INDEX != 0) {
            int 수 = -(VALUE / plaas_INDEX);
            if (수 != 0 || Loop || plaas_INDEX == 1) { 힙[Naslaan + 2 + lengte_VALUE++] = '0' + 수; Loop = true; }
            VALUE %= plaas_INDEX; plaas_INDEX /= 10;
        }
        힙[Naslaan + 1] = lengte_VALUE; return Naslaan;
    }
    static int 정수해독(int Naslaan) {
        if (!objek_VALUE(Naslaan, 1)) return 0;
        int lengte_VALUE = 힙[Naslaan + 1], 수 = 0, VALUE = 0; boolean 음수 = false;
        if (lengte_VALUE > 0 && (힙[Naslaan + 2] == '-' || 힙[Naslaan + 2] == '+')) { 음수 = 힙[Naslaan + 2] == '-'; 수++; }
        if (수 == lengte_VALUE) faling_VALUE("NumberFormatException");
        for (; 수 < lengte_VALUE && !Fout; 수++) {
            int syfer_VALUE = 힙[Naslaan + 2 + 수] - '0';
            if (syfer_VALUE < 0 || syfer_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && syfer_VALUE > (음수 ? 8 : 7)) faling_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - syfer_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int TYPE_VALUE) {
        if (Fout) return;
        if (raam_INDEX < 0 || raam_Stapel[raam_INDEX] >= metode_Stapel[raam_metode[raam_INDEX]]) { faling_VALUE("operand stack overflow"); return; }
        int gleuf_inskrywing = raam_INDEX * 128 + raam_Stapel[raam_INDEX]++; 스택값[gleuf_inskrywing] = VALUE; 스택형[gleuf_inskrywing] = TYPE_VALUE;
    }
    static int 빼기(int TYPE_VALUE) {
        if (Fout) return 0;
        if (raam_INDEX < 0 || raam_Stapel[raam_INDEX] < 1) { faling_VALUE("operand stack underflow"); return 0; }
        int gleuf_inskrywing = raam_INDEX * 128 + --raam_Stapel[raam_INDEX]; teruggee_TYPE = 스택형[gleuf_inskrywing];
        if (TYPE_VALUE != 0 && teruggee_TYPE != TYPE_VALUE) faling_VALUE("operand type mismatch");
        return 스택값[gleuf_inskrywing];
    }
    static void 지역읽기(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[raam_metode[raam_INDEX]] || INDEX < 0 || lokaal_TYPE[raam_INDEX * 128 + INDEX] != TYPE_VALUE) { faling_VALUE("invalid or uninitialized local"); return; }
        넣기(lokaal_VALUE[raam_INDEX * 128 + INDEX], TYPE_VALUE);
    }
    static void skryf_lokaal(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[raam_metode[raam_INDEX]] || INDEX < 0) { faling_VALUE("local index out of range"); return; }
        int VALUE = 빼기(TYPE_VALUE); lokaal_VALUE[raam_INDEX * 128 + INDEX] = VALUE; lokaal_TYPE[raam_INDEX * 128 + INDEX] = TYPE_VALUE;
    }
    static int 명바() {
        int Posisie = raam_plaas[raam_INDEX];
        if (Posisie < metode_BEGIN[raam_metode[raam_INDEX]] || Posisie >= metode_beëindig[raam_metode[raam_INDEX]]) { faling_VALUE("instruction pointer out of range"); return 0; }
        raam_plaas[raam_INDEX]++; return Lêer[Posisie];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void skuif_VALUE(int Posisie) {
        int funksie_VALUE = raam_metode[raam_INDEX];
        if (Posisie < metode_BEGIN[funksie_VALUE] || Posisie >= metode_beëindig[funksie_VALUE] || 경계[Posisie] != funksie_VALUE + 1) faling_VALUE("invalid branch target");
        else raam_plaas[raam_INDEX] = Posisie;
    }
    static void 호출(int funksie_VALUE) {
        if (raam_INDEX == 31) { faling_VALUE("call stack limit (32)"); return; }
        int Volgende_item = raam_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) lokaal_TYPE[Volgende_item * 128 + 수] = 0;
        for (int 수 = metode_argument_COUNT[funksie_VALUE] - 1; 수 >= 0; 수--) {
            lokaal_VALUE[Volgende_item * 128 + 수] = 빼기(metode_argument_TYPE[funksie_VALUE * 16 + 수]); lokaal_TYPE[Volgende_item * 128 + 수] = metode_argument_TYPE[funksie_VALUE * 16 + 수];
        }
        raam_INDEX = Volgende_item; raam_metode[raam_INDEX] = funksie_VALUE; raam_plaas[raam_INDEX] = metode_BEGIN[funksie_VALUE]; raam_Stapel[raam_INDEX] = 0;
    }
    static void teruggee_maatreël(int TYPE_VALUE) {
        if (TYPE_VALUE != metode_teruggee[raam_metode[raam_INDEX]]) { faling_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        raam_INDEX--; if (raam_INDEX >= 0 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
    }
    static int[] Stream_lêer_naam = new int[64];
    static void lêer_Stream_Bel(int eienaar_VALUE, int Naam, int formaat_VALUE, int Opdrag) {
        boolean Afvoer = Word_SMS(eienaar_VALUE, "java/io/FileOutputStream");
        int 종류 = Afvoer ? 6 : 5;
        if (Opdrag == 183 && Word_SMS(Naam, "<init>")) {
            boolean 이어 = false;
            if (Afvoer && Word_SMS(formaat_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(formaat_VALUE, "(Ljava/lang/String;)V")) { faling_VALUE("unsupported file stream constructor"); return; }
            int lêer_inskrywing_naam = 빼기(2), Stream_VALUE = 빼기(2);
            if (!objek_VALUE(lêer_inskrywing_naam, 1) || !objek_VALUE(Stream_VALUE, 종류) || Fout) return;
            if (힙[Stream_VALUE + 3] != 0) { faling_VALUE("file stream already initialized"); return; }
            int lengte_VALUE = 힙[lêer_inskrywing_naam + 1];
            if (lengte_VALUE < 1 || lengte_VALUE > 63) { faling_VALUE("invalid file name length"); return; }
            for (int gleuf_inskrywing = 0; gleuf_inskrywing < lengte_VALUE; gleuf_inskrywing++) {
                int VALUE = 힙[lêer_inskrywing_naam + 2 + gleuf_inskrywing];
                if (VALUE < 1 || VALUE > 127) { faling_VALUE("file stream paths currently require ASCII"); return; }
                Stream_lêer_naam[gleuf_inskrywing] = VALUE;
            }
            Stream_lêer_naam[lengte_VALUE] = 0;
            int 서술자 = gebruiker.파일서술자열기(Stream_lêer_naam, Afvoer ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { faling_VALUE("FileNotFoundException: file open failed"); return; }
            힙[Stream_VALUE + 2] = 서술자; 힙[Stream_VALUE + 3] = 1;
            return;
        }
        if (Opdrag != 182) { faling_VALUE("invalid file stream invocation"); return; }
        int Aksie = -1, VALUE = 0;
        if (Word_SMS(Naam, "close") && Word_SMS(formaat_VALUE, "()V")) Aksie = 0;
        if (!Afvoer && Word_SMS(Naam, "read") && Word_SMS(formaat_VALUE, "()I")) Aksie = 1;
        if (Afvoer && Word_SMS(Naam, "write") && Word_SMS(formaat_VALUE, "(I)V")) { Aksie = 2; VALUE = 빼기(1); }
        if (Aksie < 0) { faling_VALUE("unsupported file stream method"); return; }
        int Stream_VALUE = 빼기(2);
        if (!objek_VALUE(Stream_VALUE, 종류) || Fout) return;
        if (힙[Stream_VALUE + 3] == 0) { faling_VALUE("uninitialized file stream"); return; }
        int 서술자 = 힙[Stream_VALUE + 2];
        if (Aksie == 0) {
            if (서술자 >= 0 && gebruiker.파일서술자닫기(서술자) < 0) faling_VALUE("IOException: close failed");
            힙[Stream_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { faling_VALUE("IOException: stream closed"); return; }
        if (Aksie == 1) {
            int maatreël = gebruiker.파일한바이트읽기(서술자);
            if (maatreël < -1) faling_VALUE("IOException: read failed"); else 넣기(maatreël, 1);
        } else if (gebruiker.파일한바이트쓰기(서술자, VALUE) != 1) faling_VALUE("IOException: write failed");
    }
    static void Bel_metode(int INDEX, int Opdrag) {
        if (!tjek_konstante(INDEX, 10)) return;
        int eienaar_VALUE = Klas_naam_SMS(상가[INDEX]), Naam = Naslaan_naam(konstante_SECOND_VALUE[INDEX]), formaat_VALUE = Naslaan_TYPE(konstante_SECOND_VALUE[INDEX]);
        if (Fout) return;
        if (같은말(eienaar_VALUE, Klas_naam)) {
            if (Opdrag != 184) { faling_VALUE("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < metode_COUNT; 수++) if (같은말(Naam, metode_naam_SMS[수]) && 같은말(formaat_VALUE, metode_TYPE[수])) {
                if ((metode_toegang[수] & 8) == 0) faling_VALUE("method is not static"); else 호출(수);
                return;
            }
            faling_VALUE("NoSuchMethodError"); return;
        }
        if (Word_SMS(eienaar_VALUE, "java/io/FileInputStream") || Word_SMS(eienaar_VALUE, "java/io/FileOutputStream")) {
            lêer_Stream_Bel(eienaar_VALUE, Naam, formaat_VALUE, Opdrag); return;
        }
        if (Opdrag == 184 && Word_SMS(eienaar_VALUE, "java/lang/Integer") && Word_SMS(Naam, "parseInt") && Word_SMS(formaat_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Opdrag == 182 && Word_SMS(eienaar_VALUE, "java/io/PrintStream") && (Word_SMS(Naam, "println") || Word_SMS(Naam, "print"))) {
            int TYPE_VALUE = 0, VALUE = 0;
            if (Word_SMS(formaat_VALUE, "(I)V")) { TYPE_VALUE = 1; VALUE = 빼기(1); }
            else if (Word_SMS(formaat_VALUE, "(Z)V")) { TYPE_VALUE = 2; VALUE = 빼기(1); }
            else if (Word_SMS(formaat_VALUE, "(C)V")) { TYPE_VALUE = 3; VALUE = 빼기(1); }
            else if (Word_SMS(formaat_VALUE, "(Ljava/lang/String;)V")) { TYPE_VALUE = 4; VALUE = 빼기(2); }
            else if (!Word_SMS(formaat_VALUE, "()V") || !Word_SMS(Naam, "println")) faling_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) faling_VALUE("invalid PrintStream receiver");
            if (Fout) return;
            if (TYPE_VALUE == 1) 자바도구.수쓰기(VALUE);
            if (TYPE_VALUE == 2) gebruiker.Skryf(VALUE == 0 ? "false" : "true");
            if (TYPE_VALUE == 3) gebruiker.skryf_karakter_VALUE(VALUE & 65535);
            if (TYPE_VALUE == 4) skryf_SMS(VALUE);
            if (Word_SMS(Naam, "println")) gebruiker.skryf_karakter_VALUE(10);
            return;
        }
        if (Opdrag == 182 && Word_SMS(eienaar_VALUE, "java/lang/String")) {
            if (Word_SMS(Naam, "length") && Word_SMS(formaat_VALUE, "()I")) {
                int Naslaan = 빼기(2); if (objek_VALUE(Naslaan, 1)) 넣기(힙[Naslaan + 1], 1); return;
            }
            if (Word_SMS(Naam, "charAt") && Word_SMS(formaat_VALUE, "(I)C")) {
                int voetskrif_VALUE = 빼기(1), Naslaan = 빼기(2);
                if (objek_VALUE(Naslaan, 1)) {
                    if (voetskrif_VALUE < 0 || voetskrif_VALUE >= 힙[Naslaan + 1]) faling_VALUE("StringIndexOutOfBoundsException"); else 넣기(힙[Naslaan + 2 + voetskrif_VALUE], 1);
                }
                return;
            }
        }
        if (Word_SMS(eienaar_VALUE, "java/lang/StringBuilder")) {
            if (Opdrag == 183 && Word_SMS(Naam, "<init>") && Word_SMS(formaat_VALUE, "()V")) { objek_VALUE(빼기(2), 4); return; }
            if (Opdrag == 182 && Word_SMS(Naam, "toString") && Word_SMS(formaat_VALUE, "()Ljava/lang/String;")) {
                int Naslaan = 빼기(2); if (objek_VALUE(Naslaan, 4)) 넣기(힙[Naslaan + 2] == 0 ? hou_karakter("") : 힙[Naslaan + 2], 2); return;
            }
            if (Opdrag == 182 && Word_SMS(Naam, "append")) {
                int Teks = 0;
                if (Word_SMS(formaat_VALUE, "(I)Ljava/lang/StringBuilder;")) Teks = syfer_karakter(빼기(1));
                else if (Word_SMS(formaat_VALUE, "(Z)Ljava/lang/StringBuilder;")) Teks = hou_karakter(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(formaat_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); Teks = toewys_Berging(1, 1); if (!Fout) 힙[Teks + 2] = VALUE & 65535;
                }
                else if (Word_SMS(formaat_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Teks = 빼기(2); if (Teks == 0) Teks = hou_karakter("null"); }
                else { faling_VALUE("unsupported StringBuilder append"); return; }
                int Naslaan = 빼기(2); if (!objek_VALUE(Naslaan, 4) || !objek_VALUE(Teks, 1)) return;
                int voor_VALUE = 힙[Naslaan + 2], voor_VALUE_lengte = voor_VALUE == 0 ? 0 : 힙[voor_VALUE + 1], TERUG_VALUE_lengte = 힙[Teks + 1];
                int 새글 = toewys_Berging(1, voor_VALUE_lengte + TERUG_VALUE_lengte); if (Fout) return;
                for (int 수 = 0; 수 < voor_VALUE_lengte; 수++) 힙[새글 + 2 + 수] = 힙[voor_VALUE + 2 + 수];
                for (int 수 = 0; 수 < TERUG_VALUE_lengte; 수++) 힙[새글 + 2 + voor_VALUE_lengte + 수] = 힙[Teks + 2 + 수];
                힙[Naslaan + 2] = 새글; 넣기(Naslaan, 2); return;
            }
        }
        faling_VALUE("unsupported library method");
    }
    static int ARRAY_gleuf(int Naslaan, int voetskrif_VALUE, int TYPE_VALUE) {
        if (!objek_VALUE(Naslaan, TYPE_VALUE)) return 0;
        if (voetskrif_VALUE < 0 || voetskrif_VALUE >= 힙[Naslaan + 1]) { faling_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return Naslaan + 2 + voetskrif_VALUE;
    }
    static void uitvoer_bevel() {
        int 남음 = 500000;
        while (raam_INDEX >= 0 && !Fout) {
            if (--남음 == 0) { faling_VALUE("instruction limit (500000)"); break; }
            int Loop = raam_plaas[raam_INDEX], VALUE = 명바();
            if (Fout) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = VALUE == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= konstante_COUNT) faling_VALUE("invalid ldc constant");
                else if (konstante_merk[수] == 3) 넣기(상가[수], 1);
                else if (konstante_merk[수] == 8) 넣기(konstante_SMS(상가[수]), 2);
                else faling_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { skryf_lokaal(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { skryf_lokaal(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { skryf_lokaal(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE == 50) {
                int voetskrif_VALUE = 빼기(1), Naslaan = 빼기(2), gleuf_inskrywing = ARRAY_gleuf(Naslaan, voetskrif_VALUE, VALUE == 46 ? 2 : 3);
                if (!Fout) 넣기(힙[gleuf_inskrywing], VALUE == 46 ? 1 : 2); continue;
            }
            if (VALUE == 79 || VALUE == 83) {
                int item_element = 빼기(VALUE == 79 ? 1 : 2), voetskrif_VALUE = 빼기(1), Naslaan = 빼기(2), gleuf_inskrywing = ARRAY_gleuf(Naslaan, voetskrif_VALUE, VALUE == 79 ? 2 : 3);
                if (VALUE == 83 && item_element != 0) objek_VALUE(item_element, 1);
                if (!Fout) 힙[gleuf_inskrywing] = item_element; continue;
            }
            if (VALUE == 87) { 빼기(0); continue; }
            if (VALUE == 89) { int 가 = 빼기(0), TYPE_VALUE = teruggee_TYPE; 넣기(가, TYPE_VALUE); 넣기(가, TYPE_VALUE); continue; }
            if (VALUE == 95) { int 가 = 빼기(0), 가형 = teruggee_TYPE, 나 = 빼기(0), 나형 = teruggee_TYPE; 넣기(가, 가형); 넣기(나, 나형); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), maatreël = 0;
                if ((VALUE == 108 || VALUE == 112) && 나 == 0) { faling_VALUE("ArithmeticException: / by zero"); continue; }
                if (VALUE == 96) maatreël = 가 + 나;
                if (VALUE == 100) maatreël = 가 - 나;
                if (VALUE == 104) maatreël = 가 * 나;
                if (VALUE == 108) maatreël = 가 / 나;
                if (VALUE == 112) maatreël = 가 % 나;
                if (VALUE == 120) maatreël = 가 << 나;
                if (VALUE == 122) maatreël = 가 >> 나;
                if (VALUE == 124) maatreël = 가 >>> 나;
                if (VALUE == 126) maatreël = 가 & 나;
                if (VALUE == 128) maatreël = 가 | 나;
                if (VALUE == 130) maatreël = 가 ^ 나;
                넣기(maatreël, 1); continue;
            }
            if (VALUE == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALUE == 132) {
                int lokaal_bestek = 명바(), 증분 = (byte)명바(); 지역읽기(lokaal_bestek, 1); 넣기(빼기(1) + 증분, 1); skryf_lokaal(lokaal_bestek, 1); continue;
            }
            if (VALUE >= 145 && VALUE <= 147) {
                int 수 = 빼기(1); 넣기(VALUE == 145 ? (byte)수 : VALUE == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                int bestemming_VALUE = Loop + (short)명짧(); boolean 갈까 = VALUE == 167;
                if (VALUE >= 153 && VALUE <= 158) {
                    int 수 = 빼기(1); 갈까 = VALUE == 153 ? 수 == 0 : VALUE == 154 ? 수 != 0 : VALUE == 155 ? 수 < 0 : VALUE == 156 ? 수 >= 0 : VALUE == 157 ? 수 > 0 : 수 <= 0;
                } else if (VALUE >= 159 && VALUE <= 166) {
                    int 나 = 빼기(VALUE >= 165 ? 2 : 1), 가 = 빼기(VALUE >= 165 ? 2 : 1);
                    갈까 = VALUE == 159 || VALUE == 165 ? 가 == 나 : VALUE == 160 || VALUE == 166 ? 가 != 나 : VALUE == 161 ? 가 < 나 : VALUE == 162 ? 가 >= 나 : VALUE == 163 ? 가 > 나 : 가 <= 나;
                } else if (VALUE == 198 || VALUE == 199) { int 수 = 빼기(2); 갈까 = VALUE == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) skuif_VALUE(bestemming_VALUE); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { teruggee_maatreël(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE == 178) {
                int 수 = 명짧(); if (!tjek_konstante(수, 9)) continue;
                if (!Word_SMS(Klas_naam_SMS(상가[수]), "java/lang/System") || !Word_SMS(Naslaan_naam(konstante_SECOND_VALUE[수]), "out")
                    || !Word_SMS(Naslaan_TYPE(konstante_SECOND_VALUE[수]), "Ljava/io/PrintStream;")) faling_VALUE("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (VALUE == 182 || VALUE == 183 || VALUE == 184) { Bel_metode(명짧(), VALUE); continue; }
            if (VALUE == 187) {
                int Naam = Klas_naam_SMS(명짧());
                if (Word_SMS(Naam, "java/lang/StringBuilder")) 넣기(toewys_Berging(4, 1), 2);
                else if (Word_SMS(Naam, "java/io/FileInputStream") || Word_SMS(Naam, "java/io/FileOutputStream")) {
                    int Naslaan = toewys_Berging(Word_SMS(Naam, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!Fout) { 힙[Naslaan + 2] = -1; 넣기(Naslaan, 2); }
                } else faling_VALUE("unsupported object construction");
                continue;
            }
            if (VALUE == 188 || VALUE == 189) {
                if (VALUE == 188) { if (명바() != 10) faling_VALUE("only int[] newarray is supported"); }
                else if (!Word_SMS(Klas_naam_SMS(명짧()), "java/lang/String")) faling_VALUE("only String[] anewarray is supported");
                int lengte_VALUE = 빼기(1); 넣기(toewys_Berging(VALUE == 188 ? 2 : 3, lengte_VALUE), 2); continue;
            }
            if (VALUE == 190) {
                int Naslaan = 빼기(2);
                if (Naslaan < 1 || Naslaan >= 힙끝 - 1 || (힙[Naslaan] != 2 && 힙[Naslaan] != 3)) faling_VALUE("null or invalid array");
                else 넣기(힙[Naslaan + 1], 1); continue;
            }
            if (VALUE == 192) {
                int Naam = Klas_naam_SMS(명짧()), Naslaan = 빼기(2);
                if (!Word_SMS(Naam, "java/lang/String")) faling_VALUE("unsupported checkcast");
                else if (Naslaan != 0) objek_VALUE(Naslaan, 1);
                넣기(Naslaan, 2); continue;
            }
            faling_VALUE("unsupported bytecode");
        }
    }
    public static int Loop() {
        if (gebruiker.인수개수() == 1 && 자바도구.같음(gebruiker.인수(0), "-version")) {
            gebruiker.Skryf("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (gebruiker.인수개수() < 1) { gebruiker.Skryf("Usage: java CLASS [ARGS]\n"); return 2; }
        int lengte_VALUE = 자바도구.Naam(lêer_naam_SMS, gebruiker.인수(0));
        if (lengte_VALUE < 1 || lengte_VALUE > 57) { gebruiker.Skryf("java: invalid class name\n"); return 2; }
        lêer_naam_SMS[lengte_VALUE] = '.'; lêer_naam_SMS[lengte_VALUE + 1] = 'c'; lêer_naam_SMS[lengte_VALUE + 2] = 'l'; lêer_naam_SMS[lengte_VALUE + 3] = 'a'; lêer_naam_SMS[lengte_VALUE + 4] = 's'; lêer_naam_SMS[lengte_VALUE + 5] = 's';
        Grootte = gebruiker.파일읽기(lêer_naam_SMS, Lêer);
        if (Grootte < 0) { gebruiker.Skryf("java: cannot read class: "); 자바도구.수쓰기(Grootte); gebruiker.skryf_karakter_VALUE(10); return 1; }
        클래스읽기(); if (Fout) return 1;
        int karakter_naam = konstante_SMS(Klas_naam);
        if (!Fout && 힙[karakter_naam + 1] != lengte_VALUE) faling_VALUE("class name does not match file");
        for (int 수 = 0; 수 < lengte_VALUE && !Fout; 수++) if (힙[karakter_naam + 2 + 수] != lêer_naam_SMS[수]) faling_VALUE("class name does not match file");
        int inskrywing_p_VALUE = -1;
        for (int 수 = 0; 수 < metode_COUNT; 수++) if (Word_SMS(metode_naam_SMS[수], "main") && Word_SMS(metode_TYPE[수], "([Ljava/lang/String;)V") && (metode_toegang[수] & 9) == 9) inskrywing_p_VALUE = 수;
        if (inskrywing_p_VALUE < 0) faling_VALUE("public static void main(String[] args) required");
        if (Fout) return 1;
        int 인수 = toewys_Berging(3, gebruiker.인수개수() - 1);
        for (int 수 = 1; 수 < gebruiker.인수개수() && !Fout; 수++) 힙[인수 + 1 + 수] = hou_karakter(gebruiker.인수(수));
        raam_INDEX = 0; raam_metode[0] = inskrywing_p_VALUE; raam_plaas[0] = metode_BEGIN[inskrywing_p_VALUE]; lokaal_VALUE[0] = 인수; lokaal_TYPE[0] = 2;
        uitvoer_bevel(); return Fout ? 1 : 0;
    }
}
