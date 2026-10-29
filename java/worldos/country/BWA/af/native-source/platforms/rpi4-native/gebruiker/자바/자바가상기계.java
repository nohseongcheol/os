// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Lêer/스택/Naslaan/tak 경계를 uitvoer_bevel 중 검사한다. */
public final class 자바가상기계 {
    static int[] Lêer = new int[16 * 16384], 임시파일 = new int[16384], lêer_naam_SMS = new int[512];
    static int[] konstante_merk = new int[8192], 상가 = new int[8192], konstante_SECOND_VALUE = new int[8192], string_Naslaan = new int[8192];
    static int[] metode_naam_SMS = new int[512], metode_TYPE = new int[512], metode_toegang = new int[512], metode_eienaar = new int[512];
    static int[] metode_BEGIN = new int[512], metode_beëindig = new int[512], metode_Stapel = new int[512], 함수지역 = new int[512];
    static int[] metode_argument_COUNT = new int[512], metode_argument_TYPE = new int[8192], metode_teruggee = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] lokaal_VALUE = new int[16384], lokaal_TYPE = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] raam_metode = new int[128], raam_plaas = new int[128], raam_Stapel = new int[128], raam_instruksie = new int[128], inisialiseer_raam = new int[128];
    static int[] Klas_Definisie_naam = new int[16], Klas_Definisie_verstel = new int[16], 종부모 = new int[16], Klas_Definisie_stand = new int[16], Klas_gleuf_COUNT = new int[16], inisialiseer_Klas_Definisie = new int[16];
    static int[] Klas_koppelvlak = new int[16 * 16], Klas_koppelvlak_COUNT = new int[16];
    static int[] gleuf_naam = new int[512], gleuf_TYPE = new int[512], gleuf_eienaar = new int[512], gleuf_Toestemmings = new int[512], gleuf_plaas = new int[512], gleuf_data = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], ARRAY_element = new int[32768], bêre_heelgetal = new int[256];
    static int Grootte, 읽기위치, metode_COUNT, Klas_naam, raam_INDEX = -1, 힙끝 = 1, teruggee_TYPE;
    static int Klas_Definisie_COUNT, gleuf_COUNT, 잡기수, 현재읽는종, 던진객체, 잠시수, wys_COUNT, Versameling_COUNT;
    static int 현재가닥, draad_COUNT = 1, inskrywing_Klas_Definisie;
    static int[] draad_raam = new int[4], draad_stand = new int[4], draad_objek = new int[4], draad_teiken = new int[4], 가닥대기 = new int[4];
    static boolean Fout, 바꿈요청;
    static int[] 잠금주인 = new int[32768], 잠금깊이 = new int[32768], 틀잠금 = new int[128], 종잠금 = new int[16], Klas_draad = new int[16];

    static void faling_VALUE(String Word_SMS) {
        if (Fout) return;
        int kategorie_CODE = 0;
        if (자바도구.같음(Word_SMS, "ArithmeticException: / by zero")) kategorie_CODE = 4;
        if (자바도구.같음(Word_SMS, "NullPointerException") || 자바도구.같음(Word_SMS, "null or invalid array")) kategorie_CODE = 5;
        if (자바도구.같음(Word_SMS, "ArrayIndexOutOfBoundsException")) kategorie_CODE = 7;
        if (자바도구.같음(Word_SMS, "StringIndexOutOfBoundsException")) kategorie_CODE = 8;
        if (자바도구.같음(Word_SMS, "NumberFormatException")) kategorie_CODE = 10;
        if (자바도구.같음(Word_SMS, "FileNotFoundException: file open failed")) kategorie_CODE = 12;
        if (자바도구.같음(Word_SMS, "IOException: stream closed") || 자바도구.같음(Word_SMS, "IOException: read failed") || 자바도구.같음(Word_SMS, "IOException: write failed")) kategorie_CODE = 11;
        if (자바도구.같음(Word_SMS, "ClassCastException")) kategorie_CODE = 14;
        if (자바도구.같음(Word_SMS, "NegativeArraySizeException")) kategorie_CODE = 15;
        if (kategorie_CODE != 0 && raam_INDEX >= 0) { 예외던짐(kategorie_CODE, Word_SMS); return; }
        gebruiker.Skryf("JVM error: "); gebruiker.Skryf(Word_SMS); gebruiker.skryf_karakter_VALUE(10); Fout = true;
    }
    static boolean snit(int Loop, int lengte_VALUE) {
        if (Loop < 0 || Loop >= Lêer.length || lengte_VALUE < 0) return false;
        int Klas_Definisie = Loop / 16384;
        return Loop % 16384 <= Klas_Definisie_verstel[Klas_Definisie] && lengte_VALUE <= Klas_Definisie_verstel[Klas_Definisie] - Loop % 16384;
    }
    static int greep_VALUE() {
        if (!snit(읽기위치, 1)) { faling_VALUE("truncated class file"); return 0; }
        return Lêer[읽기위치++];
    }
    static int 짧은수() { return greep_VALUE() << 8 | greep_VALUE(); }
    static int heelgetal() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int lengte_VALUE) { if (!snit(읽기위치, lengte_VALUE)) faling_VALUE("invalid attribute size"); else 읽기위치 += lengte_VALUE; }
    static boolean tjek_konstante(int 수, int 종류) {
        if (수 <= 0 || 수 >= konstante_merk.length || konstante_merk[수] != 종류) { faling_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Loop, int lengte_VALUE, String Word_SMS) {
        if (!snit(Loop, lengte_VALUE)) return false;
        int 읽는자리 = Loop, 끝 = Loop + lengte_VALUE;
        for (int lus_INDEX = 0; lus_INDEX < Word_SMS.length(); lus_INDEX++) {
            int karakterkode = Word_SMS.charAt(lus_INDEX);
            if (karakterkode > 0 && karakterkode < 128) { if (읽는자리 >= 끝 || Lêer[읽는자리++] != karakterkode) return false; }
            else if (karakterkode < 2048) {
                if (읽는자리 + 2 > 끝 || Lêer[읽는자리++] != (192 | (karakterkode >> 6)) || Lêer[읽는자리++] != (128 | (karakterkode & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Lêer[읽는자리++] != (224 | (karakterkode >> 12)) || Lêer[읽는자리++] != (128 | ((karakterkode >> 6) & 63)) || Lêer[읽는자리++] != (128 | (karakterkode & 63))) return false;
        }
        return 읽는자리 == 끝;
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
    static int 상번호() { int VALUE = 짧은수(); return VALUE == 0 ? 0 : 현재읽는종 * 512 + VALUE; }
    static int 명상수() { return metode_eienaar[raam_metode[raam_INDEX]] * 512 + 명짧(); }
    static void 속성건너() {
        int item_COUNT = 짧은수();
        for (int 수 = 0; 수 < item_COUNT && !Fout; 수++) { tjek_konstante(상번호(), 1); 건너(heelgetal()); }
    }
    static int bevel_lengte(int VALUE) {
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
    static int plaas_heelgetal(int 읽는자리) {
        if (!snit(읽는자리, 4)) { faling_VALUE("truncated bytecode operand"); return 0; }
        return Lêer[읽는자리] << 24 | Lêer[읽는자리 + 1] << 16 | Lêer[읽는자리 + 2] << 8 | Lêer[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Loop, int 끝) {
        int VALUE = Lêer[읽는자리], lengte_VALUE = bevel_lengte(VALUE);
        if (VALUE == 170 || VALUE == 171) {
            int BASE_plaas = 읽는자리 + 1;
            while ((BASE_plaas - Loop) % 4 != 0) BASE_plaas++;
            if (끝 - BASE_plaas < (VALUE == 170 ? 12 : 8)) return 0;
            int inskrywing_COUNT = VALUE == 170 ? plaas_heelgetal(BASE_plaas + 8) - plaas_heelgetal(BASE_plaas + 4) + 1 : plaas_heelgetal(BASE_plaas + 4);
            if (inskrywing_COUNT < 0 || inskrywing_COUNT > 2048) return 0;
            lengte_VALUE = BASE_plaas - 읽는자리 + (VALUE == 170 ? 12 + 4 * inskrywing_COUNT : 8 + 8 * inskrywing_COUNT);
        }
        if (VALUE == 196 && 읽는자리 + 1 < 끝) {
            int Word_data = Lêer[읽는자리 + 1]; lengte_VALUE = Word_data == 132 ? 6 : (Word_data == 21 || Word_data == 25 || Word_data == 54 || Word_data == 58) ? 4 : 0;
        }
        return lengte_VALUE > 0 && lengte_VALUE <= 끝 - 읽는자리 ? lengte_VALUE : 0;
    }
    static void tjek_bestemming_VALUE(int bestemming_VALUE, int funksie_VALUE) {
        if (bestemming_VALUE < metode_BEGIN[funksie_VALUE] || bestemming_VALUE >= metode_beëindig[funksie_VALUE] || 경계[bestemming_VALUE] != funksie_VALUE + 1) faling_VALUE("invalid branch target");
    }
    static void 클래스읽기(int Klas_Definisie) {
        현재읽는종 = Klas_Definisie; 읽기위치 = Klas_Definisie * 16384; Grootte = 읽기위치 + Klas_Definisie_verstel[Klas_Definisie];
        if (heelgetal() != 0xcafebabe) { faling_VALUE("not a class file"); return; }
        int 부판 = 짧은수(), weergawe_VALUE = 짧은수();
        if (weergawe_VALUE < 45 || weergawe_VALUE > 52 || 부판 != 0) { faling_VALUE("supported class versions: 45..52, minor 0"); return; }
        int konstante_COUNT = 짧은수(), BASE_plaas = Klas_Definisie * 512;
        if (konstante_COUNT < 1 || konstante_COUNT > 512) { faling_VALUE("constant pool limit (511)"); return; }
        for (int inskrywing_COUNT = 1; inskrywing_COUNT < konstante_COUNT && !Fout; inskrywing_COUNT++) {
            int 수 = BASE_plaas + inskrywing_COUNT, 종류 = greep_VALUE(); konstante_merk[수] = 종류;
            if (종류 == 1) { konstante_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(konstante_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = heelgetal();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); konstante_SECOND_VALUE[수] = 상번호(); }
            else faling_VALUE("unsupported constant type");
        }
        int toestemming_VALUE = 짧은수();
        if ((toestemming_VALUE & (0x2000 | 0x4000)) != 0) faling_VALUE("annotation/enum class unsupported");
        Klas_Definisie_naam[Klas_Definisie] = Klas_naam_SMS(상번호());
        종부모[Klas_Definisie] = Klas_naam_SMS(상번호());
        int koppelvlak_COUNT = 짧은수(); if (koppelvlak_COUNT > 16) { faling_VALUE("interface count limit"); return; }
        Klas_koppelvlak_COUNT[Klas_Definisie] = koppelvlak_COUNT;
        for (int lus_INDEX = 0; lus_INDEX < koppelvlak_COUNT; lus_INDEX++) Klas_koppelvlak[Klas_Definisie * 16 + lus_INDEX] = Klas_naam_SMS(상번호());
        int veld_COUNT = 짧은수();
        if (veld_COUNT > 512 - gleuf_COUNT) { faling_VALUE("field count limit (512)"); return; }
        for (int lus_INDEX = 0; lus_INDEX < veld_COUNT && !Fout; lus_INDEX++) {
            int lêer_INDEX = gleuf_COUNT++; gleuf_eienaar[lêer_INDEX] = Klas_Definisie; gleuf_Toestemmings[lêer_INDEX] = 짧은수(); gleuf_naam[lêer_INDEX] = 상번호(); gleuf_TYPE[lêer_INDEX] = 상번호();
            tjek_konstante(gleuf_naam[lêer_INDEX], 1); tjek_konstante(gleuf_TYPE[lêer_INDEX], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[gleuf_TYPE[lêer_INDEX]]; int kategorie_CODE = 서술형(읽기위치 + konstante_SECOND_VALUE[gleuf_TYPE[lêer_INDEX]], false); 읽기위치 = 보존값;
            if ((gleuf_Toestemmings[lêer_INDEX] & 8) == 0) gleuf_plaas[lêer_INDEX] = Klas_gleuf_COUNT[Klas_Definisie]++;
            int kenmerk_data = 짧은수();
            for (int binnebind_plaas = 0; binnebind_plaas < kenmerk_data && !Fout; binnebind_plaas++) {
                int naam_konstante = 상번호(), 유효길이 = heelgetal();
                if (Word_SMS(naam_konstante, "ConstantValue") && 유효길이 == 2) {
                    int data_VALUE = 상번호();
                    if (kategorie_CODE == 1 && tjek_konstante(data_VALUE, 3)) gleuf_data[lêer_INDEX] = 상가[data_VALUE];
                    else if (kategorie_CODE == 2 && tjek_konstante(data_VALUE, 8)) gleuf_data[lêer_INDEX] = konstante_SMS(상가[data_VALUE]);
                } else 건너(유효길이);
            }
        }
        int item_COUNT = 짧은수();
        if (item_COUNT > 512 - metode_COUNT) { faling_VALUE("method count limit (512)"); return; }
        for (int lus_INDEX = 0; lus_INDEX < item_COUNT && !Fout; lus_INDEX++) {
            int 수 = metode_COUNT++; metode_eienaar[수] = Klas_Definisie;
            metode_toegang[수] = 짧은수(); metode_naam_SMS[수] = 상번호(); metode_TYPE[수] = 상번호();
            tjek_konstante(metode_naam_SMS[수], 1); 서술읽기(수);
            if ((metode_toegang[수] & 8) == 0) {
                if (metode_argument_COUNT[수] == 16) { faling_VALUE("too many instance method arguments"); return; }
                for (int Vergelyking_plaas = metode_argument_COUNT[수]; Vergelyking_plaas > 0; Vergelyking_plaas--) metode_argument_TYPE[수 * 16 + Vergelyking_plaas] = metode_argument_TYPE[수 * 16 + Vergelyking_plaas - 1];
                metode_argument_TYPE[수 * 16] = 2; metode_argument_COUNT[수]++;
            }
            if ((metode_toegang[수] & 0x100) != 0) faling_VALUE("user native method unsupported");
            if (Word_SMS(metode_naam_SMS[수], "<clinit>")) inisialiseer_Klas_Definisie[Klas_Definisie] = 수 + 1;
            for (int voor_VALUE = 0; voor_VALUE < 수; voor_VALUE++) if (metode_eienaar[voor_VALUE] == Klas_Definisie && 같은말(metode_naam_SMS[voor_VALUE], metode_naam_SMS[수]) && 같은말(metode_TYPE[voor_VALUE], metode_TYPE[수])) faling_VALUE("duplicate method");
            int kenmerk_COUNT = 짧은수();
            for (int kenmerk_VALUE = 0; kenmerk_VALUE < kenmerk_COUNT && !Fout; kenmerk_VALUE++) {
                int Naam = 상번호(), lengte_VALUE = heelgetal(), Loop = 읽기위치;
                if (!snit(Loop, lengte_VALUE)) { faling_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Naam, "Code")) {
                    if (metode_BEGIN[수] != 0) faling_VALUE("duplicate Code attribute");
                    metode_Stapel[수] = 짧은수(); 함수지역[수] = 짧은수(); int CODE_lengte = heelgetal();
                    if (metode_Stapel[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < metode_argument_COUNT[수]
                        || CODE_lengte < 1 || CODE_lengte > 8192) faling_VALUE("method memory limits exceeded");
                    metode_BEGIN[수] = 읽기위치; 건너(CODE_lengte); metode_beëindig[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { faling_VALUE("exception table limit"); return; }
                    for (int binnebind_plaas = 0; binnebind_plaas < 잡는수; binnebind_plaas++) {
                        int fout_Naslaan = 잡기수++; 잡기함수[fout_Naslaan] = 수;
                        잡기시작[fout_Naslaan] = metode_BEGIN[수] + 짧은수(); 잡기끝[fout_Naslaan] = metode_BEGIN[수] + 짧은수();
                        잡기위치[fout_Naslaan] = metode_BEGIN[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[fout_Naslaan] = 부호값 == 0 ? 0 : Klas_naam_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != Loop + lengte_VALUE) faling_VALUE("Code attribute size mismatch");
                } else 건너(lengte_VALUE);
            }
            if ((metode_toegang[수] & 0x400) != 0) continue;
            if (metode_BEGIN[수] == 0) faling_VALUE("missing Code attribute");
            int gleuf_inskrywing = metode_BEGIN[수];
            while (gleuf_inskrywing < metode_beëindig[수] && !Fout) {
                int lengte_VALUE = 길이읽기(gleuf_inskrywing, metode_BEGIN[수], metode_beëindig[수]);
                if (lengte_VALUE == 0) { faling_VALUE("unsupported or truncated bytecode"); break; }
                경계[gleuf_inskrywing] = 수 + 1; gleuf_inskrywing += lengte_VALUE;
            }
            gleuf_inskrywing = metode_BEGIN[수];
            while (gleuf_inskrywing < metode_beëindig[수] && !Fout) {
                int VALUE = Lêer[gleuf_inskrywing];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) tjek_bestemming_VALUE(gleuf_inskrywing + (short)(Lêer[gleuf_inskrywing + 1] << 8 | Lêer[gleuf_inskrywing + 2]), 수);
                if (VALUE == 200) tjek_bestemming_VALUE(gleuf_inskrywing + plaas_heelgetal(gleuf_inskrywing + 1), 수);
                if (VALUE == 170 || VALUE == 171) {
                    int 읽는자리 = gleuf_inskrywing + 1; while ((읽는자리 - metode_BEGIN[수]) % 4 != 0) 읽는자리++;
                    tjek_bestemming_VALUE(gleuf_inskrywing + plaas_heelgetal(읽는자리), 수);
                    int inskrywing_COUNT = VALUE == 170 ? plaas_heelgetal(읽는자리 + 8) - plaas_heelgetal(읽는자리 + 4) + 1 : plaas_heelgetal(읽는자리 + 4);
                    읽는자리 += VALUE == 170 ? 12 : 8;
                    for (int binnebind_plaas = 0; binnebind_plaas < inskrywing_COUNT; binnebind_plaas++) tjek_bestemming_VALUE(gleuf_inskrywing + plaas_heelgetal(읽는자리 + binnebind_plaas * (VALUE == 170 ? 4 : 8) + (VALUE == 170 ? 0 : 4)), 수);
                }
                gleuf_inskrywing += 길이읽기(gleuf_inskrywing, metode_BEGIN[수], metode_beëindig[수]);
            }
            for (int binnebind_plaas = 0; binnebind_plaas < 잡기수; binnebind_plaas++) if (잡기함수[binnebind_plaas] == 수) {
                tjek_bestemming_VALUE(잡기시작[binnebind_plaas], 수); tjek_bestemming_VALUE(잡기위치[binnebind_plaas], 수);
                if (잡기끝[binnebind_plaas] != metode_beëindig[수]) tjek_bestemming_VALUE(잡기끝[binnebind_plaas], 수);
                if (잡기시작[binnebind_plaas] >= 잡기끝[binnebind_plaas]) faling_VALUE("invalid exception range");
            }
        }
        if (!Fout) 속성건너();
        if (읽기위치 != Grootte) faling_VALUE("extra class file data");
    }
    static int toewys_Berging(int 종류, int lengte_VALUE) { return 새기억(종류, lengte_VALUE); }
    static boolean objek_VALUE(int Naslaan, int 종류) {
        if (!객체유효(Naslaan)) return false;
        if (힙[Naslaan] != 종류) { faling_VALUE("object type mismatch"); return false; }
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
        if (teruggee_TYPE == 2) beskerm_VALUE(스택값[gleuf_inskrywing]);
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
        if (raam_INDEX % 32 == 31) { faling_VALUE("call stack limit (32)"); return; }
        int Volgende_item = raam_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) lokaal_TYPE[Volgende_item * 128 + 수] = 0;
        for (int 수 = metode_argument_COUNT[funksie_VALUE] - 1; 수 >= 0; 수--) {
            lokaal_VALUE[Volgende_item * 128 + 수] = 빼기(metode_argument_TYPE[funksie_VALUE * 16 + 수]); lokaal_TYPE[Volgende_item * 128 + 수] = metode_argument_TYPE[funksie_VALUE * 16 + 수];
        }
        if (Fout) return;
        raam_INDEX = Volgende_item; inisialiseer_raam[raam_INDEX] = 0; raam_metode[raam_INDEX] = funksie_VALUE; raam_plaas[raam_INDEX] = metode_BEGIN[funksie_VALUE]; raam_Stapel[raam_INDEX] = 0;
    }
    static void teruggee_maatreël(int TYPE_VALUE) {
        if (TYPE_VALUE != metode_teruggee[raam_metode[raam_INDEX]]) { faling_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        if (inisialiseer_raam[raam_INDEX] != 0) Klas_Definisie_stand[inisialiseer_raam[raam_INDEX] - 1] = 2;
        if (틀잠금[raam_INDEX] != 0) { 잠금풀기(틀잠금[raam_INDEX]); 틀잠금[raam_INDEX] = 0; }
        raam_INDEX--; if (raam_INDEX >= 현재가닥 * 32 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
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
                if (VALUE < 1) { faling_VALUE("invalid file stream path"); return; }
                Stream_lêer_naam[gleuf_inskrywing] = VALUE;
            }
            Stream_lêer_naam[lengte_VALUE] = 0;
            int 서술자 = gebruiker.파일서술자열기(Stream_lêer_naam, Afvoer ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { faling_VALUE("FileNotFoundException: file open failed"); return; }
            힙[Stream_VALUE + 2] = 서술자; 힙[Stream_VALUE + 3] = 1;
            return;
        }
        if (Opdrag != 182) { faling_VALUE("invalid file stream invocation"); return; }
        if ((Afvoer && Word_SMS(Naam, "write") || !Afvoer && Word_SMS(Naam, "read"))
            && (Word_SMS(formaat_VALUE, Afvoer ? "([B)V" : "([B)I") || Word_SMS(formaat_VALUE, Afvoer ? "([BII)V" : "([BII)I"))) {
            boolean snit_VALUE = Word_SMS(formaat_VALUE, Afvoer ? "([BII)V" : "([BII)I");
            int inskrywing_COUNT = snit_VALUE ? 빼기(1) : 0, 시작점 = snit_VALUE ? 빼기(1) : 0, data_ARRAY = 빼기(2), objek_Naslaan = 빼기(2);
            if (!objek_VALUE(data_ARRAY, 20) || !objek_VALUE(objek_Naslaan, 종류)) return;
            if (!snit_VALUE) inskrywing_COUNT = 힙[data_ARRAY + 1];
            if (시작점 < 0 || inskrywing_COUNT < 0 || 시작점 > 힙[data_ARRAY + 1] - inskrywing_COUNT) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[objek_Naslaan + 3] == 0 || 힙[objek_Naslaan + 2] < 0) { faling_VALUE("IOException: stream closed"); return; }
            int 완료수 = 0;
            while (완료수 < inskrywing_COUNT && !Fout) {
                int 반환값 = Afvoer ? gebruiker.파일한바이트쓰기(힙[objek_Naslaan + 2], 힙[data_ARRAY + 2 + 시작점 + 완료수]) : gebruiker.파일한바이트읽기(힙[objek_Naslaan + 2]);
                if (반환값 < 0) { faling_VALUE(Afvoer ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!Afvoer && 반환값 == 256) break;
                if (!Afvoer) 힙[data_ARRAY + 2 + 시작점 + 완료수] = (byte)반환값;
                완료수++;
            }
            if (!Afvoer) 넣기(inskrywing_COUNT != 0 && 완료수 == 0 ? -1 : 완료수, 1);
            return;
        }
        if (Afvoer && Word_SMS(Naam, "flush") && Word_SMS(formaat_VALUE, "()V")) { int objek_Naslaan = 빼기(2); if (objek_VALUE(objek_Naslaan, 종류) && 힙[objek_Naslaan + 2] < 0) faling_VALUE("IOException: stream closed"); return; }
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
            if (maatreël < -1) faling_VALUE("IOException: read failed"); else 넣기(maatreël == 256 ? -1 : maatreël, 1);
        } else if (gebruiker.파일한바이트쓰기(서술자, VALUE) != 1) faling_VALUE("IOException: write failed");
    }
    static void Bel_metode(int INDEX, int Opdrag) {
        if (INDEX <= 0 || INDEX >= konstante_merk.length || (konstante_merk[INDEX] != 10 && konstante_merk[INDEX] != 11)) { faling_VALUE("invalid method reference"); return; }
        int eienaar_VALUE = Klas_naam_SMS(상가[INDEX]), Naam = Naslaan_naam(konstante_SECOND_VALUE[INDEX]), formaat_VALUE = Naslaan_TYPE(konstante_SECOND_VALUE[INDEX]);
        if (Fout) return;
        if (기본호출(eienaar_VALUE, Naam, formaat_VALUE, Opdrag)) return;
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
        int Klas_Definisie = FIND_Klas_Definisie(eienaar_VALUE); if (Klas_Definisie < 0 || Fout) return;
        int lêer_INDEX = FIND_metode(Klas_Definisie, Naam, formaat_VALUE);
        if (lêer_INDEX < 0) {
            for (int karakterkode = Klas_Definisie, inskrywing_COUNT = 0; karakterkode >= 0 && inskrywing_COUNT < 16; inskrywing_COUNT++, karakterkode = 부모종(karakterkode))
                if (Word_SMS(종부모[karakterkode], "java/lang/Thread")) { 가닥호출(Naam, formaat_VALUE, Opdrag); return; }
            faling_VALUE("NoSuchMethodError"); return;
        }
        if (((metode_toegang[lêer_INDEX] & 8) != 0) != (Opdrag == 184)) { faling_VALUE("method static/instance mismatch"); return; }
        if (Opdrag == 184) { if (!inisialiseer(metode_eienaar[lêer_INDEX], raam_instruksie[raam_INDEX])) return; }
        else {
            int 읽는자리 = raam_Stapel[raam_INDEX] - metode_argument_COUNT[lêer_INDEX];
            if (읽는자리 < 0 || 스택형[raam_INDEX * 128 + 읽는자리] != 2) { faling_VALUE("invalid method receiver"); return; }
            int objek_Naslaan = 스택값[raam_INDEX * 128 + 읽는자리];
            if (!객체유효(objek_Naslaan)) return;
            if (힙[objek_Naslaan] < 32 || !종포함(힙[objek_Naslaan] - 32, eienaar_VALUE)) { faling_VALUE("method receiver type mismatch"); return; }
            if (Opdrag != 183) lêer_INDEX = FIND_metode(힙[objek_Naslaan] - 32, Naam, formaat_VALUE);
        }
        if (lêer_INDEX < 0 || (metode_toegang[lêer_INDEX] & 0x400) != 0) { faling_VALUE("AbstractMethodError"); return; }
        int 잠금참조 = 0;
        if ((metode_toegang[lêer_INDEX] & 32) != 0) {
            if (Opdrag == 184) { int karakterkode = metode_eienaar[lêer_INDEX]; if (종잠금[karakterkode] == 0) 종잠금[karakterkode] = toewys_Berging(8, 0); 잠금참조 = 종잠금[karakterkode]; }
            else 잠금참조 = 스택값[raam_INDEX * 128 + raam_Stapel[raam_INDEX] - metode_argument_COUNT[lêer_INDEX]];
            if (!잠금얻기(잠금참조)) { if (!Fout) raam_plaas[raam_INDEX] = raam_instruksie[raam_INDEX]; return; }
        }
        호출(lêer_INDEX); if (!Fout) 틀잠금[raam_INDEX] = 잠금참조;
    }
    static boolean 배열저장가능(int ARRAY_Naslaan, int data_VALUE) {
        if (data_VALUE == 0 || ARRAY_element[ARRAY_Naslaan] == 0) return true;
        boolean 성공여부 = ARRAY_element[ARRAY_Naslaan] == -1 ? (data_VALUE > 0 && data_VALUE < 힙끝 && 힙[data_VALUE] == 1) : 맞는객체(data_VALUE, ARRAY_element[ARRAY_Naslaan]);
        if (!성공여부 && !Fout) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int ARRAY_gleuf(int Naslaan, int voetskrif_VALUE, int TYPE_VALUE) {
        if (!objek_VALUE(Naslaan, TYPE_VALUE)) return 0;
        if (voetskrif_VALUE < 0 || voetskrif_VALUE >= 힙[Naslaan + 1]) { faling_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return Naslaan + 2 + voetskrif_VALUE;
    }
    static void uitvoer_bevel() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (Fout) { if (던진객체 != 0) handvatsel_uitsondering(); if (Fout || raam_INDEX < 현재가닥 * 32) break; }
            if (raam_INDEX < 현재가닥 * 32 || 바꿈요청 || --조각 == 0) { if (!SWITCH_draad()) break; 조각 = 100; }
            if (raam_INDEX == 0 && Klas_Definisie_stand[inskrywing_Klas_Definisie] != 2 && !inisialiseer(inskrywing_Klas_Definisie, raam_plaas[raam_INDEX])) continue;
            if (raam_INDEX == 현재가닥 * 32 && 현재가닥 != 0 && (metode_toegang[raam_metode[raam_INDEX]] & 32) != 0 && 틀잠금[raam_INDEX] == 0) {
                int objek_Naslaan = draad_teiken[현재가닥]; if (!잠금얻기(objek_Naslaan)) { if (Fout) break; continue; } 틀잠금[raam_INDEX] = objek_Naslaan;
            }
            잠시수 = 0;
            if (--남음 == 0) { faling_VALUE("instruction limit (500000)"); break; }
            int Loop = raam_plaas[raam_INDEX]; raam_instruksie[raam_INDEX] = Loop; int VALUE = 명바();
            if (Fout) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = metode_eienaar[raam_metode[raam_INDEX]] * 512 + (VALUE == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= konstante_merk.length) faling_VALUE("invalid ldc constant");
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
            if (VALUE == 46 || VALUE >= 50 && VALUE <= 53) {
                int inskrywing_plaas = 빼기(1), objek_Naslaan = 빼기(2), kategorie_CODE = VALUE == 46 ? 2 : VALUE == 50 ? 3 : VALUE == 51 ? 20 : VALUE == 52 ? 22 : 23;
                if (VALUE == 51 && objek_Naslaan > 0 && objek_Naslaan < 힙끝 && 힙[objek_Naslaan] == 21) kategorie_CODE = 21;
                int 읽는자리 = ARRAY_gleuf(objek_Naslaan, inskrywing_plaas, kategorie_CODE); if (!Fout) 넣기(힙[읽는자리], VALUE == 50 ? 2 : 1); continue;
            }
            if (VALUE == 79 || VALUE >= 83 && VALUE <= 86) {
                int inskrywing_Naslaan = 빼기(VALUE == 83 ? 2 : 1), inskrywing_plaas = 빼기(1), objek_Naslaan = 빼기(2), kategorie_CODE = VALUE == 79 ? 2 : VALUE == 83 ? 3 : VALUE == 84 ? 20 : VALUE == 85 ? 22 : 23;
                if (VALUE == 84 && objek_Naslaan > 0 && objek_Naslaan < 힙끝 && 힙[objek_Naslaan] == 21) kategorie_CODE = 21;
                int 읽는자리 = ARRAY_gleuf(objek_Naslaan, inskrywing_plaas, kategorie_CODE);
                if (!Fout && kategorie_CODE == 3 && !배열저장가능(objek_Naslaan, inskrywing_Naslaan)) continue;
                if (!Fout) 힙[읽는자리] = kategorie_CODE == 20 ? (byte)inskrywing_Naslaan : kategorie_CODE == 21 ? inskrywing_Naslaan & 1 : kategorie_CODE == 22 ? (char)inskrywing_Naslaan : kategorie_CODE == 23 ? (short)inskrywing_Naslaan : inskrywing_Naslaan;
                continue;
            }
            if (VALUE >= 87 && VALUE <= 95) { Stapel_instruksie(VALUE); continue; }
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
            if (VALUE >= 178 && VALUE <= 181) { 필드호출(명상수(), VALUE, Loop); continue; }
            if (VALUE >= 182 && VALUE <= 185) {
                int 부호값 = 명상수();
                if (VALUE == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { faling_VALUE("invalid invokeinterface operands"); continue; } }
                Bel_metode(부호값, VALUE); continue;
            }
            if (VALUE == 187) { 새객체(Klas_naam_SMS(명상수()), Loop); continue; }
            if (VALUE == 188 || VALUE == 189) {
                int kategorie_CODE = 3, komponent = 0;
                if (VALUE == 188) { int 임시값 = 명바(); kategorie_CODE = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else komponent = Klas_naam_SMS(명상수());
                if (kategorie_CODE == 0) { faling_VALUE("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), objek_Naslaan = toewys_Berging(kategorie_CODE, 유효길이); if (!Fout) ARRAY_element[objek_Naslaan] = komponent; 넣기(objek_Naslaan, 2); continue;
            }
            if (VALUE == 190) {
                int objek_Naslaan = 빼기(2);
                if (객체유효(objek_Naslaan)) { int Vergelyking_plaas = 힙[objek_Naslaan]; if (Vergelyking_plaas != 2 && Vergelyking_plaas != 3 && (Vergelyking_plaas < 20 || Vergelyking_plaas > 23)) faling_VALUE("not an array"); else 넣기(힙[objek_Naslaan + 1], 1); }
                continue;
            }
            if (VALUE == 191) {
                int objek_Naslaan = 빼기(2); if (객체유효(objek_Naslaan)) { if (힙[objek_Naslaan] != 9) faling_VALUE("athrow requires supported Throwable"); else { 던진객체 = objek_Naslaan; Fout = true; } }
                continue;
            }
            if (VALUE == 192 || VALUE == 193) {
                int naam_konstante = Klas_naam_SMS(명상수()), objek_Naslaan = 빼기(2); boolean MATCH = 맞는객체(objek_Naslaan, naam_konstante);
                if (VALUE == 193) 넣기(objek_Naslaan != 0 && MATCH ? 1 : 0, 1);
                else { if (!MATCH && !Fout) faling_VALUE("ClassCastException"); 넣기(objek_Naslaan, 2); }
                continue;
            }
            if (VALUE == 170 || VALUE == 171) {
                int 읽는자리 = Loop + 1, lêer_INDEX = raam_metode[raam_INDEX], Sleutel_Naslaan = 빼기(1);
                while ((읽는자리 - metode_BEGIN[lêer_INDEX]) % 4 != 0) 읽는자리++;
                int teiken_adres = plaas_heelgetal(읽는자리);
                if (VALUE == 170) { int 낮은값 = plaas_heelgetal(읽는자리 + 4), 높은값 = plaas_heelgetal(읽는자리 + 8); if (Sleutel_Naslaan >= 낮은값 && Sleutel_Naslaan <= 높은값) teiken_adres = plaas_heelgetal(읽는자리 + 12 + (Sleutel_Naslaan - 낮은값) * 4); }
                else { int 총수 = plaas_heelgetal(읽는자리 + 4); for (int lus_INDEX = 0; lus_INDEX < 총수; lus_INDEX++) if (plaas_heelgetal(읽는자리 + 8 + lus_INDEX * 8) == Sleutel_Naslaan) teiken_adres = plaas_heelgetal(읽는자리 + 12 + lus_INDEX * 8); }
                skuif_VALUE(Loop + teiken_adres); continue;
            }
            if (VALUE == 200) { skuif_VALUE(Loop + plaas_heelgetal(Loop + 1)); continue; }
            if (VALUE == 194 || VALUE == 195) {
                int objek_Naslaan = 빼기(2);
                if (VALUE == 195) 잠금풀기(objek_Naslaan);
                else if (!잠금얻기(objek_Naslaan) && !Fout) { 넣기(objek_Naslaan, 2); raam_plaas[raam_INDEX] = Loop; }
                continue;
            }
            if (VALUE == 196) {
                int bevel_CODE = 명바(), inskrywing_plaas = 명짧();
                if (bevel_CODE == 21 || bevel_CODE == 25) 지역읽기(inskrywing_plaas, bevel_CODE == 21 ? 1 : 2);
                else if (bevel_CODE == 54 || bevel_CODE == 58) skryf_lokaal(inskrywing_plaas, bevel_CODE == 54 ? 1 : 2);
                else if (bevel_CODE == 132) { int DELTA_VALUE = (short)명짧(); 지역읽기(inskrywing_plaas, 1); 넣기(빼기(1) + DELTA_VALUE, 1); skryf_lokaal(inskrywing_plaas, 1); }
                else faling_VALUE("unsupported wide opcode");
                continue;
            }
            faling_VALUE("unsupported bytecode");
        }
    }
    static int FIND_Klas_Definisie(int Naam) {
        for (int lus_INDEX = 0; lus_INDEX < Klas_Definisie_COUNT; lus_INDEX++) if (Klas_Definisie_naam[lus_INDEX] != 0 && 같은말(Klas_Definisie_naam[lus_INDEX], Naam)) return lus_INDEX;
        return laai_Klas_Definisie(konstante_SMS(Naam));
    }
    static int laai_Klas_Definisie(int naam_string) {
        if (!objek_VALUE(naam_string, 1)) return -1;
        int lengte_VALUE = 힙[naam_string + 1];
        if (lengte_VALUE < 1 || lengte_VALUE > 505 || Klas_Definisie_COUNT == 16) { faling_VALUE("class name/count limit"); return -1; }
        for (int lus_INDEX = 0; lus_INDEX < lengte_VALUE; lus_INDEX++) { int karakterkode = 힙[naam_string + 2 + lus_INDEX]; lêer_naam_SMS[lus_INDEX] = karakterkode == '/' ? '.' : karakterkode; }
        lêer_naam_SMS[lengte_VALUE] = '.'; lêer_naam_SMS[lengte_VALUE + 1] = 'c'; lêer_naam_SMS[lengte_VALUE + 2] = 'l'; lêer_naam_SMS[lengte_VALUE + 3] = 'a'; lêer_naam_SMS[lengte_VALUE + 4] = 's'; lêer_naam_SMS[lengte_VALUE + 5] = 's'; lêer_naam_SMS[lengte_VALUE + 6] = 0;
        int Grootte = gebruiker.파일읽기(lêer_naam_SMS, 임시파일);
        if (Grootte < 0) { faling_VALUE("ClassNotFoundException"); return -1; }
        int Klas_Definisie = Klas_Definisie_COUNT++; Klas_Definisie_verstel[Klas_Definisie] = Grootte;
        for (int lus_INDEX = 0; lus_INDEX < Grootte; lus_INDEX++) Lêer[Klas_Definisie * 16384 + lus_INDEX] = 임시파일[lus_INDEX];
        클래스읽기(Klas_Definisie); if (Fout) return -1;
        int werklik_data = konstante_SMS(Klas_Definisie_naam[Klas_Definisie]);
        if (!글같음(werklik_data, naam_string, true)) { faling_VALUE("class name does not match file"); return -1; }
        int 부모 = 종부모[Klas_Definisie];
        if (부모 != 0 && !Word_SMS(부모, "java/lang/Object") && !Word_SMS(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = FIND_Klas_Definisie(부모);
            if (Fout || 위 < 0) return -1;
            int 읽는자리 = 위, toneel_COUNT = 0;
            while (읽는자리 >= 0 && toneel_COUNT++ < 16) {
                if (읽는자리 == Klas_Definisie) { faling_VALUE("cyclic inheritance"); return -1; }
                읽는자리 = 부모종(읽는자리);
            }
            int 시작변위 = Klas_gleuf_COUNT[위];
            for (int lêer_INDEX = 0; lêer_INDEX < gleuf_COUNT; lêer_INDEX++) if (gleuf_eienaar[lêer_INDEX] == Klas_Definisie && (gleuf_Toestemmings[lêer_INDEX] & 8) == 0) gleuf_plaas[lêer_INDEX] += 시작변위;
            Klas_gleuf_COUNT[Klas_Definisie] += 시작변위;
        }
        return Klas_Definisie;
    }
    static int 부모종(int Klas_Definisie) {
        int Naam = 종부모[Klas_Definisie];
        for (int lus_INDEX = 0; lus_INDEX < Klas_Definisie_COUNT; lus_INDEX++) if (Naam != 0 && Klas_Definisie_naam[lus_INDEX] != 0 && 같은말(Klas_Definisie_naam[lus_INDEX], Naam)) return lus_INDEX;
        return -1;
    }
    static int FIND_metode(int Klas_Definisie, int Naam, int formaat_VALUE) {
        for (int 깊이 = 0; Klas_Definisie >= 0 && 깊이 < 16; 깊이++, Klas_Definisie = 부모종(Klas_Definisie)) {
            for (int lus_INDEX = 0; lus_INDEX < metode_COUNT; lus_INDEX++) if (metode_eienaar[lus_INDEX] == Klas_Definisie && 같은말(metode_naam_SMS[lus_INDEX], Naam) && 같은말(metode_TYPE[lus_INDEX], formaat_VALUE)) return lus_INDEX;
        }
        return -1;
    }
    static int naam_metode(int Klas_Definisie, String Naam, String formaat_VALUE) {
        for (int 깊이 = 0; Klas_Definisie >= 0 && 깊이 < 16; 깊이++, Klas_Definisie = 부모종(Klas_Definisie))
            for (int lus_INDEX = 0; lus_INDEX < metode_COUNT; lus_INDEX++) if (metode_eienaar[lus_INDEX] == Klas_Definisie && Word_SMS(metode_naam_SMS[lus_INDEX], Naam) && Word_SMS(metode_TYPE[lus_INDEX], formaat_VALUE)) return lus_INDEX;
        return -1;
    }
    static int 형종류(int Naam) { return Lêer[상가[Naam]] == 'L' || Lêer[상가[Naam]] == '[' ? 2 : 1; }
    static boolean inisialiseer(int Klas_Definisie, int bevel_BEGIN) {
        if (Klas_Definisie < 0 || Fout) return false;
        if (Klas_Definisie_stand[Klas_Definisie] == 3) { faling_VALUE("NoClassDefFoundError: initialization failed"); return false; }
        if (Klas_Definisie_stand[Klas_Definisie] == 1 && Klas_draad[Klas_Definisie] != 현재가닥) { raam_plaas[raam_INDEX] = bevel_BEGIN; 바꿈요청 = true; return false; }
        if (Klas_Definisie_stand[Klas_Definisie] != 0) return true;
        int 위 = 부모종(Klas_Definisie);
        if (위 >= 0 && !inisialiseer(위, bevel_BEGIN)) return false;
        Klas_Definisie_stand[Klas_Definisie] = 1; Klas_draad[Klas_Definisie] = 현재가닥;
        if (inisialiseer_Klas_Definisie[Klas_Definisie] != 0) {
            raam_plaas[raam_INDEX] = bevel_BEGIN;
            호출(inisialiseer_Klas_Definisie[Klas_Definisie] - 1); if (!Fout) inisialiseer_raam[raam_INDEX] = Klas_Definisie + 1;
            return false;
        }
        Klas_Definisie_stand[Klas_Definisie] = 2; return true;
    }
    static void 필드호출(int INDEX, int Opdrag, int Loop) {
        if (!tjek_konstante(INDEX, 9)) return;
        int eienaar_VALUE = Klas_naam_SMS(상가[INDEX]), Naam = Naslaan_naam(konstante_SECOND_VALUE[INDEX]), formaat_VALUE = Naslaan_TYPE(konstante_SECOND_VALUE[INDEX]);
        if (Word_SMS(eienaar_VALUE, "java/lang/System") && (Word_SMS(Naam, "out") || Word_SMS(Naam, "err")) && Word_SMS(formaat_VALUE, "Ljava/io/PrintStream;") && Opdrag == 178) { 넣기(-1, 2); return; }
        int Klas_Definisie = FIND_Klas_Definisie(eienaar_VALUE); if (Klas_Definisie < 0 || Fout) return;
        int 찾음 = -1;
        for (int 읽는자리 = Klas_Definisie, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = 부모종(읽는자리))
            for (int lêer_INDEX = 0; lêer_INDEX < gleuf_COUNT; lêer_INDEX++) if (gleuf_eienaar[lêer_INDEX] == 읽는자리 && 같은말(gleuf_naam[lêer_INDEX], Naam) && 같은말(gleuf_TYPE[lêer_INDEX], formaat_VALUE)) 찾음 = lêer_INDEX;
        if (찾음 < 0) { faling_VALUE("NoSuchFieldError"); return; }
        boolean staties_VALUE = Opdrag == 178 || Opdrag == 179;
        if (staties_VALUE != ((gleuf_Toestemmings[찾음] & 8) != 0)) { faling_VALUE("field static/instance mismatch"); return; }
        if (staties_VALUE && !inisialiseer(gleuf_eienaar[찾음], Loop)) return;
        int TYPE_VALUE = 형종류(formaat_VALUE), VALUE = 0;
        if (Opdrag == 179 || Opdrag == 181) VALUE = 빼기(TYPE_VALUE);
        if (staties_VALUE) { if (Opdrag == 178) 넣기(gleuf_data[찾음], TYPE_VALUE); else if (!Fout) gleuf_data[찾음] = VALUE; return; }
        int objek_Naslaan = 빼기(2);
        if (!객체유효(objek_Naslaan)) return;
        if (힙[objek_Naslaan] < 32 || !종포함(힙[objek_Naslaan] - 32, eienaar_VALUE)) { faling_VALUE("field receiver type mismatch"); return; }
        int 보관칸 = objek_Naslaan + 2 + gleuf_plaas[찾음];
        if (Opdrag == 180) 넣기(힙[보관칸], TYPE_VALUE);
        else if (!Fout) { 힙[보관칸] = VALUE; 힙참조[보관칸] = TYPE_VALUE == 2 ? 1 : 0; }
    }
    static boolean 종포함(int Klas_Definisie, int Naam) {
        for (int 중첩깊이 = 0; Klas_Definisie >= 0 && 중첩깊이 < 16; 중첩깊이++, Klas_Definisie = 부모종(Klas_Definisie)) {
            if (같은말(Klas_Definisie_naam[Klas_Definisie], Naam) || (종부모[Klas_Definisie] != 0 && 같은말(종부모[Klas_Definisie], Naam))) return true;
            for (int binnebind_plaas = 0; binnebind_plaas < Klas_koppelvlak_COUNT[Klas_Definisie]; binnebind_plaas++) if (같은말(Klas_koppelvlak[Klas_Definisie * 16 + binnebind_plaas], Naam)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int greep_data, boolean Pad) {
        if (첫값 == greep_data) return true;
        if (첫값 <= 0 || greep_data <= 0 || 힙[첫값] != 1 || 힙[greep_data] != 1 || 힙[첫값 + 1] != 힙[greep_data + 1]) return false;
        for (int lus_INDEX = 0; lus_INDEX < 힙[첫값 + 1]; lus_INDEX++) {
            int x_koördinaat = 힙[첫값 + 2 + lus_INDEX], Y_koördinaat = 힙[greep_data + 2 + lus_INDEX];
            if (Pad) { if (x_koördinaat == '.') x_koördinaat = '/'; if (Y_koördinaat == '.') Y_koördinaat = '/'; }
            if (x_koördinaat != Y_koördinaat) return false;
        }
        return true;
    }
    static boolean 객체유효(int objek_Naslaan) {
        if (objek_Naslaan == 0) { faling_VALUE("NullPointerException"); return false; }
        if (objek_Naslaan < 1 || objek_Naslaan >= 힙끝 || 힙폭[objek_Naslaan] < 2 || 힙[objek_Naslaan] == 0) { faling_VALUE("invalid object reference"); return false; }
        return true;
    }
    static void beskerm_VALUE(int objek_Naslaan) {
        if (objek_Naslaan > 0 && objek_Naslaan < 힙끝 && 힙폭[objek_Naslaan] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = objek_Naslaan;
    }
    static void wys_VALUE(int objek_Naslaan) {
        if (objek_Naslaan > 0 && objek_Naslaan < 힙끝 && 힙폭[objek_Naslaan] >= 2 && 힙[objek_Naslaan] != 0 && 힙표시[objek_Naslaan] == 0) {
            힙표시[objek_Naslaan] = 1; 표시대기[wys_COUNT++] = objek_Naslaan;
        }
    }
    static void 수거() {
        wys_COUNT = 0; Versameling_COUNT++;
        for (int tjek_plaas = 1; tjek_plaas < 힙끝; tjek_plaas += 힙폭[tjek_plaas]) 힙표시[tjek_plaas] = 0;
        for (int lus_INDEX = 0; lus_INDEX < string_Naslaan.length; lus_INDEX++) wys_VALUE(string_Naslaan[lus_INDEX]);
        for (int lus_INDEX = 0; lus_INDEX < gleuf_COUNT; lus_INDEX++) if ((gleuf_Toestemmings[lus_INDEX] & 8) != 0 && 형종류(gleuf_TYPE[lus_INDEX]) == 2) wys_VALUE(gleuf_data[lus_INDEX]);
        for (int 임시값 = 0; 임시값 < draad_COUNT; 임시값++) {
            wys_VALUE(draad_objek[임시값]); wys_VALUE(draad_teiken[임시값]);
            int 꼭대기자리 = 임시값 == 현재가닥 ? raam_INDEX : draad_raam[임시값];
            for (int lêer_INDEX = 임시값 * 32; lêer_INDEX <= 꼭대기자리; lêer_INDEX++) {
                for (int binnebind_plaas = 0; binnebind_plaas < 함수지역[raam_metode[lêer_INDEX]]; binnebind_plaas++) if (lokaal_TYPE[lêer_INDEX * 128 + binnebind_plaas] == 2) wys_VALUE(lokaal_VALUE[lêer_INDEX * 128 + binnebind_plaas]);
                for (int binnebind_plaas = 0; binnebind_plaas < raam_Stapel[lêer_INDEX]; binnebind_plaas++) if (스택형[lêer_INDEX * 128 + binnebind_plaas] == 2) wys_VALUE(스택값[lêer_INDEX * 128 + binnebind_plaas]);
            }
        }
        for (int lus_INDEX = 0; lus_INDEX < 화면참조.length; lus_INDEX++) wys_VALUE(화면참조[lus_INDEX]);
        for (int lus_INDEX = 0; lus_INDEX < 나중수; lus_INDEX++) wys_VALUE(나중실행[lus_INDEX]);
        for (int lus_INDEX = 0; lus_INDEX < bêre_heelgetal.length; lus_INDEX++) wys_VALUE(bêre_heelgetal[lus_INDEX]);
        for (int lus_INDEX = 0; lus_INDEX < Klas_Definisie_COUNT; lus_INDEX++) wys_VALUE(종잠금[lus_INDEX]);
        for (int tjek_plaas = 1; tjek_plaas < 힙끝; tjek_plaas += 힙폭[tjek_plaas]) if (잠금깊이[tjek_plaas] > 0) wys_VALUE(tjek_plaas);
        wys_VALUE(던진객체);
        for (int lus_INDEX = 0; lus_INDEX < 잠시수; lus_INDEX++) wys_VALUE(잠시참조[lus_INDEX]);
        while (wys_COUNT > 0) {
            int objek_Naslaan = 표시대기[--wys_COUNT], kategorie_CODE = 힙[objek_Naslaan];
            for (int lus_INDEX = objek_Naslaan + 2; lus_INDEX < objek_Naslaan + 힙폭[objek_Naslaan]; lus_INDEX++) if (kategorie_CODE == 3 || kategorie_CODE == 4 || 힙참조[lus_INDEX] != 0) wys_VALUE(힙[lus_INDEX]);
        }
        for (int tjek_plaas = 1; tjek_plaas < 힙끝; tjek_plaas += 힙폭[tjek_plaas]) if (힙표시[tjek_plaas] == 0) 힙[tjek_plaas] = 0;
        for (int tjek_plaas = 1; tjek_plaas < 힙끝; tjek_plaas += 힙폭[tjek_plaas]) if (힙[tjek_plaas] == 0) {
            while (tjek_plaas + 힙폭[tjek_plaas] < 힙끝 && 힙[tjek_plaas + 힙폭[tjek_plaas]] == 0) { int Volgende_plaas = tjek_plaas + 힙폭[tjek_plaas]; 힙폭[tjek_plaas] += 힙폭[Volgende_plaas]; 힙폭[Volgende_plaas] = 0; }
            if (tjek_plaas + 힙폭[tjek_plaas] == 힙끝) { 힙끝 = tjek_plaas; break; }
        }
    }
    static int 새기억(int 종류, int lengte_VALUE) {
        if (lengte_VALUE < 0) { faling_VALUE("NegativeArraySizeException"); return 0; }
        if (lengte_VALUE > 힙.length - 3) { faling_VALUE("object heap exhausted"); return 0; }
        int 필요수 = lengte_VALUE + 2, objek_Naslaan = 0;
        if (필요수 <= 힙.length - 힙끝) { objek_Naslaan = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { objek_Naslaan = 읽는자리; break; }
            if (objek_Naslaan != 0) {
                int 남은길이 = 힙폭[objek_Naslaan] - 필요수;
                if (남은길이 >= 2) { 힙폭[objek_Naslaan + 필요수] = 남은길이; 힙[objek_Naslaan + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { objek_Naslaan = 힙끝; 힙끝 += 필요수; }
        }
        if (objek_Naslaan == 0) { faling_VALUE("object heap exhausted"); return 0; }
        for (int lus_INDEX = 0; lus_INDEX < 필요수; lus_INDEX++) { 힙[objek_Naslaan + lus_INDEX] = 0; 힙참조[objek_Naslaan + lus_INDEX] = 0; 힙폭[objek_Naslaan + lus_INDEX] = 0; }
        ARRAY_element[objek_Naslaan] = 0;
        힙폭[objek_Naslaan] = 필요수; 힙[objek_Naslaan] = 종류; 힙[objek_Naslaan + 1] = lengte_VALUE; beskerm_VALUE(objek_Naslaan); return objek_Naslaan;
    }
    static int uitsondering_Klas(String naam_konstante) {
        if (자바도구.같음(naam_konstante, "java/lang/Throwable")) return 1;
        if (자바도구.같음(naam_konstante, "java/lang/Exception")) return 2;
        if (자바도구.같음(naam_konstante, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(naam_konstante, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(naam_konstante, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(naam_konstante, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(naam_konstante, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(naam_konstante, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(naam_konstante, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(naam_konstante, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(naam_konstante, "java/io/IOException")) return 11;
        if (자바도구.같음(naam_konstante, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(naam_konstante, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(naam_konstante, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(naam_konstante, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int uitsondering_konstante(int Naam) {
        for (int lus_INDEX = 1; lus_INDEX <= 41; lus_INDEX++) if (Word_SMS(Naam, uitsondering_naam(lus_INDEX))) return lus_INDEX;
        return 0;
    }
    static String uitsondering_naam(int rekening_VALUE) {
        if (rekening_VALUE == 40) return "java/lang/InterruptedException";
        if (rekening_VALUE == 41) return "한국어/자체/대기중단예외";
        if (rekening_VALUE == 39) return "java/net/SocketException";
        if (rekening_VALUE == 20) return "한국어/자체/uitsondering";
        if (rekening_VALUE == 21) return "한국어/자체/실행예외";
        if (rekening_VALUE == 22) return "한국어/자체/I_O_uitsondering";
        if (rekening_VALUE == 23) return "한국어/자체/wag_UITTELLING_uitsondering";
        if (rekening_VALUE == 24) return "한국어/자체/adres_LOOKUP_uitsondering";
        if (rekening_VALUE == 25) return "한국어/자체/파일없음예외";
        if (rekening_VALUE == 26) return "한국어/자체/통신예외";
        if (rekening_VALUE == 27) return "한국어/자체/ongeldig_argument_uitsondering";
        if (rekening_VALUE == 28) return "한국어/자체/숫자형식예외";
        if (rekening_VALUE == 29) return "한국어/자체/범위예외";
        if (rekening_VALUE == 30) return "한국어/자체/배열범위예외";
        if (rekening_VALUE == 31) return "한국어/자체/문자열범위예외";
        if (rekening_VALUE == 32) return "한국어/자체/nul_Naslaan_uitsondering";
        if (rekening_VALUE == 33) return "한국어/자체/산술예외";
        if (rekening_VALUE == 34) return "한국어/자체/stand_uitsondering";
        if (rekening_VALUE == 35) return "한국어/자체/TYPE_Uitsaai_uitsondering";
        if (rekening_VALUE == 36) return "한국어/자체/음수배열크기예외";
        if (rekening_VALUE == 37) return "한국어/자체/ARRAY_bêre_faling";
        if (rekening_VALUE == 38) return "한국어/자체/draad_stand_uitsondering";
        if (rekening_VALUE == 1) return "java/lang/Throwable"; if (rekening_VALUE == 2) return "java/lang/Exception";
        if (rekening_VALUE == 3) return "java/lang/RuntimeException"; if (rekening_VALUE == 4) return "java/lang/ArithmeticException";
        if (rekening_VALUE == 5) return "java/lang/NullPointerException"; if (rekening_VALUE == 6) return "java/lang/IndexOutOfBoundsException";
        if (rekening_VALUE == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (rekening_VALUE == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (rekening_VALUE == 9) return "java/lang/IllegalArgumentException"; if (rekening_VALUE == 10) return "java/lang/NumberFormatException";
        if (rekening_VALUE == 11) return "java/io/IOException"; if (rekening_VALUE == 12) return "java/io/FileNotFoundException";
        if (rekening_VALUE == 17) return "java/lang/ArrayStoreException";
        if (rekening_VALUE == 18) return "java/net/UnknownHostException";
        if (rekening_VALUE == 19) return "java/net/SocketTimeoutException";
        if (rekening_VALUE == 16) return "java/lang/IllegalThreadStateException";
        if (rekening_VALUE == 13) return "java/lang/IllegalStateException"; if (rekening_VALUE == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int rekening_VALUE) {
        if (rekening_VALUE == 40) return 2;
        if (rekening_VALUE == 41) return 40;
        if (rekening_VALUE == 39) return 11;
        if (rekening_VALUE == 1) return 0;
        if (rekening_VALUE == 2) return 1;
        if (rekening_VALUE == 3) return 2;
        if (rekening_VALUE == 4) return 3;
        if (rekening_VALUE == 5) return 3;
        if (rekening_VALUE == 6) return 3;
        if (rekening_VALUE == 7) return 6;
        if (rekening_VALUE == 8) return 6;
        if (rekening_VALUE == 9) return 3;
        if (rekening_VALUE == 10) return 9;
        if (rekening_VALUE == 11) return 2;
        if (rekening_VALUE == 12) return 11;
        if (rekening_VALUE == 13) return 3;
        if (rekening_VALUE == 14) return 3;
        if (rekening_VALUE == 15) return 3;
        if (rekening_VALUE == 16) return 9;
        if (rekening_VALUE == 17) return 3;
        if (rekening_VALUE == 18) return 11;
        if (rekening_VALUE == 19) return 11;
        if (rekening_VALUE == 20) return 2;
        if (rekening_VALUE == 21) return 3;
        if (rekening_VALUE == 22) return 11;
        if (rekening_VALUE == 23) return 22;
        if (rekening_VALUE == 24) return 22;
        if (rekening_VALUE == 25) return 22;
        if (rekening_VALUE == 26) return 22;
        if (rekening_VALUE == 27) return 9;
        if (rekening_VALUE == 28) return 27;
        if (rekening_VALUE == 29) return 6;
        if (rekening_VALUE == 30) return 29;
        if (rekening_VALUE == 31) return 29;
        if (rekening_VALUE == 32) return 5;
        if (rekening_VALUE == 33) return 4;
        if (rekening_VALUE == 34) return 13;
        if (rekening_VALUE == 35) return 14;
        if (rekening_VALUE == 36) return 15;
        if (rekening_VALUE == 37) return 17;
        if (rekening_VALUE == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int werklik_VALUE, int 요구값) {
        for (int 깊이 = 0; werklik_VALUE != 0 && 깊이 < 16; 깊이++, werklik_VALUE = 예외부모(werklik_VALUE))
            if (werklik_VALUE == 요구값) return true;
        return false;
    }
    static void 예외던짐(int rekening_VALUE, String README_Naslaan) {
        int objek_Naslaan = 새기억(9, 2); if (Fout) return;
        힙[objek_Naslaan + 2] = rekening_VALUE; 힙[objek_Naslaan + 3] = hou_karakter(README_Naslaan); 힙참조[objek_Naslaan + 3] = 1;
        던진객체 = objek_Naslaan; Fout = true;
    }
    static boolean 맞는객체(int objek_Naslaan, int Naam) {
        if (objek_Naslaan == 0) return true;
        if (!객체유효(objek_Naslaan)) return false;
        int kategorie_CODE = 힙[objek_Naslaan];
        if (Word_SMS(Naam, "java/lang/Object")) return true;
        if (kategorie_CODE >= 32) return 종포함(kategorie_CODE - 32, Naam);
        if (kategorie_CODE == 9) { int teiken_adres = uitsondering_konstante(Naam); return teiken_adres != 0 && 예외포함(힙[objek_Naslaan + 2], teiken_adres); }
        if (kategorie_CODE == 1) return Word_SMS(Naam, "java/lang/String") || Word_SMS(Naam, "java/lang/CharSequence");
        if (kategorie_CODE == 4) return Word_SMS(Naam, "java/lang/StringBuilder") || Word_SMS(Naam, "java/lang/CharSequence");
        if (kategorie_CODE == 10) return Word_SMS(Naam, "java/util/ArrayList") || Word_SMS(Naam, "java/util/List");
        if (kategorie_CODE == 11) return Word_SMS(Naam, "java/util/HashMap") || Word_SMS(Naam, "java/util/Map");
        if (kategorie_CODE == 12) return Word_SMS(Naam, "java/lang/Integer") || Word_SMS(Naam, "java/lang/Number");
        if (kategorie_CODE >= 24 && kategorie_CODE <= 28 && 힙[objek_Naslaan + 13] != 0) return 한국어화면종(Naam) == kategorie_CODE || Word_SMS(Naam, "한국어/자체/화면구성요소");
        if (kategorie_CODE >= 24 && kategorie_CODE <= 28) return (한국어화면종(Naam) == 0 && 화면종(Naam) == kategorie_CODE) || Word_SMS(Naam, "java/awt/Component") || Word_SMS(Naam, "java/awt/Container") || Word_SMS(Naam, "javax/swing/JComponent");
        if (kategorie_CODE == 29) return Word_SMS(Naam, 힙[objek_Naslaan + 3] != 0 ? "한국어/자체/동작알림" : "java/awt/event/ActionEvent");
        if (kategorie_CODE == 30) return Word_SMS(Naam, "java/awt/FlowLayout") || Word_SMS(Naam, "java/awt/LayoutManager");
        if (kategorie_CODE == 17) return Word_SMS(Naam, "java/net/Socket");
        if (kategorie_CODE == 18) return Word_SMS(Naam, "java/net/ServerSocket");
        if (kategorie_CODE == 19) return Word_SMS(Naam, 힙[objek_Naslaan + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (kategorie_CODE == 14) return Word_SMS(Naam, "java/net/InetAddress");
        if (kategorie_CODE == 15) return Word_SMS(Naam, "java/net/DatagramSocket");
        if (kategorie_CODE == 16) return Word_SMS(Naam, "java/net/DatagramPacket");
        if (kategorie_CODE == 13) return Word_SMS(Naam, 힙[objek_Naslaan + 3] != 0 ? "한국어/자체/작업가닥" : "java/lang/Thread");
        if (kategorie_CODE == 2) return Word_SMS(Naam, "[I"); if (kategorie_CODE == 20) return Word_SMS(Naam, "[B"); if (kategorie_CODE == 21) return Word_SMS(Naam, "[Z");
        if (kategorie_CODE == 22) return Word_SMS(Naam, "[C"); if (kategorie_CODE == 23) return Word_SMS(Naam, "[S");
        if (kategorie_CODE != 3) return false;
        if (Word_SMS(Naam, "[Ljava/lang/Object;")) return true;
        int komponent = ARRAY_element[objek_Naslaan];
        if (komponent == -1) return Word_SMS(Naam, "[Ljava/lang/String;") || Word_SMS(Naam, "[Ljava/lang/CharSequence;");
        if (komponent == 0) return false;
        if (배열종비교(komponent, Naam)) return true;
        if ((Word_SMS(komponent, "java/lang/String") || Word_SMS(komponent, "java/lang/StringBuilder")) && Word_SMS(Naam, "[Ljava/lang/CharSequence;")) return true;
        for (int lus_INDEX = 0; lus_INDEX < Klas_Definisie_COUNT; lus_INDEX++) if (같은말(Klas_Definisie_naam[lus_INDEX], komponent)) {
            for (int karakterkode = lus_INDEX, 중첩깊이 = 0; karakterkode >= 0 && 중첩깊이 < 16; 중첩깊이++, karakterkode = 부모종(karakterkode)) {
                if (배열종비교(종부모[karakterkode], Naam)) return true;
                for (int binnebind_plaas = 0; binnebind_plaas < Klas_koppelvlak_COUNT[karakterkode]; binnebind_plaas++) if (배열종비교(Klas_koppelvlak[karakterkode * 16 + binnebind_plaas], Naam)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int naam_konstante, int 형식참조) {
        int tjek_plaas = 상가[형식참조], inskrywing_COUNT = konstante_SECOND_VALUE[형식참조];
        if (naam_konstante == 0 || inskrywing_COUNT < 4 || Lêer[tjek_plaas] != '[' || Lêer[tjek_plaas + 1] != 'L' || Lêer[tjek_plaas + inskrywing_COUNT - 1] != ';' || konstante_SECOND_VALUE[naam_konstante] != inskrywing_COUNT - 3) return false;
        for (int lus_INDEX = 0; lus_INDEX < inskrywing_COUNT - 3; lus_INDEX++) if (Lêer[상가[naam_konstante] + lus_INDEX] != Lêer[tjek_plaas + 2 + lus_INDEX]) return false;
        return true;
    }
    static void handvatsel_uitsondering() {
        if (던진객체 == 0) return;
        Fout = false;
        while (raam_INDEX >= 현재가닥 * 32) {
            int lêer_INDEX = raam_metode[raam_INDEX], 읽는자리 = raam_instruksie[raam_INDEX];
            for (int lus_INDEX = 0; lus_INDEX < 잡기수; lus_INDEX++) if (잡기함수[lus_INDEX] == lêer_INDEX && 읽는자리 >= 잡기시작[lus_INDEX] && 읽는자리 < 잡기끝[lus_INDEX]
                && (잡기종[lus_INDEX] == 0 || 맞는객체(던진객체, 잡기종[lus_INDEX]))) {
                raam_plaas[raam_INDEX] = 잡기위치[lus_INDEX]; raam_Stapel[raam_INDEX] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (inisialiseer_raam[raam_INDEX] != 0) Klas_Definisie_stand[inisialiseer_raam[raam_INDEX] - 1] = 3;
            if (틀잠금[raam_INDEX] != 0) { 잠금풀기(틀잠금[raam_INDEX]); 틀잠금[raam_INDEX] = 0; }
            raam_INDEX--;
        }
        gebruiker.Skryf("Uncaught ");
        if (힙[던진객체] == 9) { gebruiker.Skryf(uitsondering_naam(힙[던진객체 + 2])); gebruiker.Skryf(": "); skryf_SMS(힙[던진객체 + 3]); }
        else gebruiker.Skryf("user exception");
        gebruiker.skryf_karakter_VALUE(10); 던진객체 = 0; Fout = true;
    }
    // 이 JVM의 스택 항목은 현재 category-1(int/reference)만 허용한다.
    static void Stapel_instruksie(int bevel_CODE) {
        int 첫값 = 빼기(0), 첫형식 = teruggee_TYPE;
        if (bevel_CODE == 87) return;
        if (bevel_CODE == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int greep_data = 빼기(0), SECOND_formaat = teruggee_TYPE;
        if (bevel_CODE == 88) return;
        if (bevel_CODE == 90) { 넣기(첫값, 첫형식); 넣기(greep_data, SECOND_formaat); 넣기(첫값, 첫형식); return; }
        if (bevel_CODE == 92) { 넣기(greep_data, SECOND_formaat); 넣기(첫값, 첫형식); 넣기(greep_data, SECOND_formaat); 넣기(첫값, 첫형식); return; }
        if (bevel_CODE == 95) { 넣기(첫값, 첫형식); 넣기(greep_data, SECOND_formaat); return; }
        int karakterkode = 빼기(0), 셋째형식 = teruggee_TYPE;
        if (bevel_CODE == 91) { 넣기(첫값, 첫형식); 넣기(karakterkode, 셋째형식); 넣기(greep_data, SECOND_formaat); 넣기(첫값, 첫형식); return; }
        if (bevel_CODE == 93) { 넣기(greep_data, SECOND_formaat); 넣기(첫값, 첫형식); 넣기(karakterkode, 셋째형식); 넣기(greep_data, SECOND_formaat); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = teruggee_TYPE;
        넣기(greep_data, SECOND_formaat); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(karakterkode, 셋째형식); 넣기(greep_data, SECOND_formaat); 넣기(첫값, 첫형식);
    }
    static void 새객체(int naam_konstante, int 시작점) {
        int kategorie_CODE = 0, 유효길이 = 0, uitsondering_Naslaan = uitsondering_konstante(naam_konstante);
        if (Word_SMS(naam_konstante, "java/lang/StringBuilder")) { kategorie_CODE = 4; 유효길이 = 1; }
        if (Word_SMS(naam_konstante, "java/io/FileInputStream")) { kategorie_CODE = 5; 유효길이 = 2; }
        if (Word_SMS(naam_konstante, "java/io/FileOutputStream")) { kategorie_CODE = 6; 유효길이 = 2; }
        if (uitsondering_Naslaan != 0) { kategorie_CODE = 9; 유효길이 = 2; }
        if (Word_SMS(naam_konstante, "java/util/ArrayList")) { kategorie_CODE = 10; 유효길이 = 2; }
        if (Word_SMS(naam_konstante, "java/util/HashMap")) { kategorie_CODE = 11; 유효길이 = 2; }
        if (Word_SMS(naam_konstante, "java/lang/Integer")) { kategorie_CODE = 12; 유효길이 = 1; }
        if (Word_SMS(naam_konstante, "java/net/Socket")) { kategorie_CODE = 17; 유효길이 = 5; }
        if (Word_SMS(naam_konstante, "java/net/ServerSocket")) { kategorie_CODE = 18; 유효길이 = 5; }
        if (Word_SMS(naam_konstante, "java/net/DatagramSocket")) { kategorie_CODE = 15; 유효길이 = 3; }
        if (Word_SMS(naam_konstante, "java/net/DatagramPacket")) { kategorie_CODE = 16; 유효길이 = 4; }
        if (Word_SMS(naam_konstante, "java/lang/Thread") || Word_SMS(naam_konstante, "한국어/자체/작업가닥")) { kategorie_CODE = 13; 유효길이 = 2; }
        if (Word_SMS(naam_konstante, "java/lang/Object")) { kategorie_CODE = 8; }
        if (kategorie_CODE == 0 && 화면종(naam_konstante) != 0) { kategorie_CODE = 화면종(naam_konstante); 유효길이 = 12; }
        if (kategorie_CODE == 0) {
            int karakterkode = FIND_Klas_Definisie(naam_konstante); if (karakterkode < 0 || Fout || !inisialiseer(karakterkode, 시작점)) return;
            kategorie_CODE = 32 + karakterkode; 유효길이 = Klas_gleuf_COUNT[karakterkode];
        }
        int objek_Naslaan = toewys_Berging(kategorie_CODE, 유효길이); if (Fout) return;
        if (kategorie_CODE == 13 && Word_SMS(naam_konstante, "한국어/자체/작업가닥")) 힙[objek_Naslaan + 3] = 1;
        if (kategorie_CODE >= 24 && kategorie_CODE <= 28 && 한국어화면종(naam_konstante) != 0) 힙[objek_Naslaan + 13] = 1;
        if (kategorie_CODE == 5 || kategorie_CODE == 6 || kategorie_CODE == 15 || kategorie_CODE == 17 || kategorie_CODE == 18) 힙[objek_Naslaan + 2] = -1;
        if (kategorie_CODE == 9) 힙[objek_Naslaan + 2] = uitsondering_Naslaan;
        넣기(objek_Naslaan, 2);
    }
    static boolean 값같음(int 첫값, int greep_data) {
        if (첫값 == greep_data) return true;
        if (첫값 == 0 || greep_data == 0 || 첫값 < 0 || greep_data < 0 || 첫값 >= 힙끝 || greep_data >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[greep_data] == 1) return 글같음(첫값, greep_data, false);
        return 힙[첫값] == 12 && 힙[greep_data] == 12 && 힙[첫값 + 2] == 힙[greep_data + 2];
    }
    static int 글조각(int objek_Naslaan, int BEGIN_plaas, int beëindig_plaas) {
        if (!objek_VALUE(objek_Naslaan, 1)) return 0;
        if (BEGIN_plaas < 0 || beëindig_plaas < BEGIN_plaas || beëindig_plaas > 힙[objek_Naslaan + 1]) { faling_VALUE("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = toewys_Berging(1, beëindig_plaas - BEGIN_plaas); if (Fout) return 0;
        for (int lus_INDEX = BEGIN_plaas; lus_INDEX < beëindig_plaas; lus_INDEX++) 힙[반환값 + 2 + lus_INDEX - BEGIN_plaas] = 힙[objek_Naslaan + 2 + lus_INDEX];
        return 반환값;
    }
    static int las_SMS(int 첫값, int greep_data) {
        if (!objek_VALUE(첫값, 1) || !objek_VALUE(greep_data, 1)) return 0;
        int inskrywing_COUNT = 힙[첫값 + 1], metode_INDEX = 힙[greep_data + 1], 반환값 = toewys_Berging(1, inskrywing_COUNT + metode_INDEX); if (Fout) return 0;
        for (int lus_INDEX = 0; lus_INDEX < inskrywing_COUNT; lus_INDEX++) 힙[반환값 + 2 + lus_INDEX] = 힙[첫값 + 2 + lus_INDEX];
        for (int lus_INDEX = 0; lus_INDEX < metode_INDEX; lus_INDEX++) 힙[반환값 + 2 + inskrywing_COUNT + lus_INDEX] = 힙[greep_data + 2 + lus_INDEX];
        return 반환값;
    }
    static boolean 기본호출(int eienaar, int naam_konstante, int 서술상수, int bevel_CODE) {
        if (Word_SMS(eienaar, "한국어/자체/실행인수") && bevel_CODE == 184) {
            if (Word_SMS(naam_konstante, "item_COUNT") && Word_SMS(서술상수, "()I")) { 넣기(gebruiker.인수개수() - 1, 1); return true; }
            if (Word_SMS(naam_konstante, "Teks") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= gebruiker.인수개수() - 1) 예외던짐(29, "uitvoer_bevel 인수 범위를 벗어났습니다");
                else 넣기(hou_karakter(gebruiker.인수(순번 + 1)), 2);
                return true;
            }
            faling_VALUE("지원하지 않는 한국어 uitvoer_bevel 인수 호출"); return true;
        }
        if (Word_SMS(eienaar, "한국어/자체/작업가닥")) { Proses_draad(naam_konstante, 서술상수, bevel_CODE, true); return true; }
        if (한국어화면소유(eienaar)) { 한국어화면호출(eienaar, naam_konstante, 서술상수, bevel_CODE); return true; }
        if (화면소유(eienaar)) { 화면호출(eienaar, naam_konstante, 서술상수, bevel_CODE); return true; }
        if (Word_SMS(eienaar, "java/net/Socket") || Word_SMS(eienaar, "java/net/ServerSocket") || Word_SMS(eienaar, "java/io/InputStream") || Word_SMS(eienaar, "java/io/OutputStream")) { 흐름호출(eienaar, naam_konstante, 서술상수, bevel_CODE); return true; }
        if (Word_SMS(eienaar, "한국어/자체/kern_VALUE") && bevel_CODE == 184) {
            if (Word_SMS(naam_konstante, "화면너비") && Word_SMS(서술상수, "()I")) { 넣기(gebruiker.화면너비(), 1); return true; }
            if (Word_SMS(naam_konstante, "화면높이") && Word_SMS(서술상수, "()I")) { 넣기(gebruiker.화면높이(), 1); return true; }
            if (Word_SMS(naam_konstante, "밀리초") && Word_SMS(서술상수, "()I")) { 넣기(gebruiker.밀리초(), 1); return true; }
            if (Word_SMS(naam_konstante, "그림대기") && Word_SMS(서술상수, "()I")) { 넣기(gebruiker.그림대기(), 1); return true; }
            if (Word_SMS(naam_konstante, "사각형") && Word_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), Y_koördinaat = 빼기(1), x_koördinaat = 빼기(1); 넣기(gebruiker.사각형(x_koördinaat, Y_koördinaat, 너비, 높이, 색상), 1); return true; }
        }
        if (Word_SMS(eienaar, "java/net/InetAddress") || Word_SMS(eienaar, "java/net/DatagramPacket") || Word_SMS(eienaar, "java/net/DatagramSocket")) { 통신호출(eienaar, naam_konstante, 서술상수, bevel_CODE); return true; }
        if (Word_SMS(eienaar, "java/lang/Thread")) { 가닥호출(naam_konstante, 서술상수, bevel_CODE); return true; }
        if (Word_SMS(eienaar, "java/lang/Object")) {
            if (Word_SMS(naam_konstante, "<init>") && Word_SMS(서술상수, "()V") && bevel_CODE == 183) { 객체유효(빼기(2)); return true; }
            if (Word_SMS(naam_konstante, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int greep_data = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == greep_data ? 1 : 0, 1); return true; }
        }
        if (uitsondering_konstante(eienaar) != 0) {
            if (Word_SMS(naam_konstante, "<init>") && bevel_CODE == 183 && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int por = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), objek_Naslaan = 빼기(2);
                if (objek_VALUE(objek_Naslaan, 9)) { 힙[objek_Naslaan + 3] = por; 힙참조[objek_Naslaan + 3] = 1; } return true;
            }
            if ((Word_SMS(naam_konstante, "getMessage") || Word_SMS(naam_konstante, "설명")) && Word_SMS(서술상수, "()Ljava/lang/String;")) { int objek_Naslaan = 빼기(2); if (objek_VALUE(objek_Naslaan, 9)) 넣기(힙[objek_Naslaan + 3], 2); return true; }
        }
        if (Word_SMS(eienaar, "java/lang/String")) {
            if (bevel_CODE == 182 && Word_SMS(naam_konstante, "getBytes") && (Word_SMS(서술상수, "()[B") || Word_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int enkodering_naam = Word_SMS(서술상수, "()[B") ? 0 : 빼기(2), objek_Naslaan = 빼기(2);
                if (!objek_VALUE(objek_Naslaan, 1)) return true;
                if (enkodering_naam != 0 && !글같음(enkodering_naam, hou_karakter("UTF-8"), false) && !글같음(enkodering_naam, hou_karakter("UTF8"), false) && !글같음(enkodering_naam, hou_karakter("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int inskrywing_COUNT = 힙[objek_Naslaan + 1], 반환값 = toewys_Berging(20, inskrywing_COUNT * 3), 사용수 = 0; if (Fout) return true;
                for (int binnebind_plaas = 0; binnebind_plaas < inskrywing_COUNT; binnebind_plaas++) {
                    int karakterkode = 힙[objek_Naslaan + 2 + binnebind_plaas];
                    if (karakterkode >= 0xd800 && karakterkode <= 0xdbff && binnebind_plaas + 1 < inskrywing_COUNT && 힙[objek_Naslaan + 3 + binnebind_plaas] >= 0xdc00 && 힙[objek_Naslaan + 3 + binnebind_plaas] <= 0xdfff) karakterkode = 0x10000 + ((karakterkode - 0xd800) << 10) + 힙[objek_Naslaan + 2 + ++binnebind_plaas] - 0xdc00;
                    else if (karakterkode >= 0xd800 && karakterkode <= 0xdfff) karakterkode = '?';
                    if (karakterkode < 128) 힙[반환값 + 2 + 사용수++] = karakterkode;
                    else { int greep_COUNT = karakterkode < 2048 ? 2 : karakterkode < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((greep_COUNT == 2 ? 192 : greep_COUNT == 3 ? 224 : 240) | karakterkode >> (6 * (greep_COUNT - 1))); for (int Vergelyking_plaas = greep_COUNT - 1; Vergelyking_plaas > 0; Vergelyking_plaas--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | karakterkode >> (6 * (Vergelyking_plaas - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (bevel_CODE == 184 && Word_SMS(naam_konstante, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(syfer_karakter(빼기(1)), 2); return true; }
            if (bevel_CODE != 182) return false;
            if (Word_SMS(naam_konstante, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int greep_data = 빼기(2), 첫값 = 빼기(2); if (objek_VALUE(첫값, 1)) 넣기(글같음(첫값, greep_data, false) ? 1 : 0, 1); return true; }
            if (Word_SMS(naam_konstante, "isEmpty") && Word_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (objek_VALUE(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_SMS(naam_konstante, "substring") && (Word_SMS(서술상수, "(I)Ljava/lang/String;") || Word_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SECOND_VALUE = Word_SMS(서술상수, "(II)Ljava/lang/String;"); int beëindig_plaas = SECOND_VALUE ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (objek_VALUE(첫값, 1)) 넣기(글조각(첫값, 시작점, SECOND_VALUE ? beëindig_plaas : 힙[첫값 + 1]), 2); return true;
            }
            if (Word_SMS(naam_konstante, "concat") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int greep_data = 빼기(2), 첫값 = 빼기(2); 넣기(las_SMS(첫값, greep_data), 2); return true; }
            if (Word_SMS(naam_konstante, "hashCode") && Word_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), huts_VALUE = 0; if (objek_VALUE(첫값, 1)) { for (int lus_INDEX = 0; lus_INDEX < 힙[첫값 + 1]; lus_INDEX++) huts_VALUE = huts_VALUE * 31 + 힙[첫값 + 2 + lus_INDEX]; 넣기(huts_VALUE, 1); } return true; }
            if (Word_SMS(naam_konstante, "toString") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (objek_VALUE(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_SMS(eienaar, "java/lang/Integer")) {
            if (bevel_CODE == 184 && Word_SMS(naam_konstante, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int data_VALUE = 빼기(1), objek_Naslaan = data_VALUE >= -128 && data_VALUE <= 127 ? bêre_heelgetal[data_VALUE + 128] : 0; if (objek_Naslaan == 0) { objek_Naslaan = toewys_Berging(12, 1); if (!Fout) { 힙[objek_Naslaan + 2] = data_VALUE; if (data_VALUE >= -128 && data_VALUE <= 127) bêre_heelgetal[data_VALUE + 128] = objek_Naslaan; } } 넣기(objek_Naslaan, 2); return true; }
            if (bevel_CODE == 183 && Word_SMS(naam_konstante, "<init>") && Word_SMS(서술상수, "(I)V")) { int data_VALUE = 빼기(1), objek_Naslaan = 빼기(2); if (objek_VALUE(objek_Naslaan, 12)) 힙[objek_Naslaan + 2] = data_VALUE; return true; }
            if (bevel_CODE == 182 && Word_SMS(naam_konstante, "intValue") && Word_SMS(서술상수, "()I")) { int objek_Naslaan = 빼기(2); if (objek_VALUE(objek_Naslaan, 12)) 넣기(힙[objek_Naslaan + 2], 1); return true; }
            if (bevel_CODE == 184 && Word_SMS(naam_konstante, "toString") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(syfer_karakter(빼기(1)), 2); return true; }
        }
        if (Word_SMS(eienaar, "java/lang/Math") && bevel_CODE == 184) {
            if (Word_SMS(naam_konstante, "abs") && Word_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_SMS(naam_konstante, "min") || Word_SMS(naam_konstante, "max")) && Word_SMS(서술상수, "(II)I")) { int greep_data = 빼기(1), 첫값 = 빼기(1); 넣기(Word_SMS(naam_konstante, "min") ? (첫값 < greep_data ? 첫값 : greep_data) : (첫값 > greep_data ? 첫값 : greep_data), 1); return true; }
        }
        if (Word_SMS(eienaar, "java/lang/System") && bevel_CODE == 184) {
            if (Word_SMS(naam_konstante, "gc") && Word_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Word_SMS(naam_konstante, "arraycopy") && Word_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int inskrywing_COUNT = 빼기(1), bestemming_VALUE_INDEX = 빼기(1), greep_data = 빼기(2), BEGIN_plaas = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(greep_data)) {
                    int kategorie_CODE = 힙[첫값];
                    if (힙[greep_data] != kategorie_CODE || (kategorie_CODE != 2 && kategorie_CODE != 3 && (kategorie_CODE < 20 || kategorie_CODE > 23))) faling_VALUE("arraycopy type mismatch");
                    else if (inskrywing_COUNT < 0 || BEGIN_plaas < 0 || bestemming_VALUE_INDEX < 0 || BEGIN_plaas > 힙[첫값 + 1] - inskrywing_COUNT || bestemming_VALUE_INDEX > 힙[greep_data + 1] - inskrywing_COUNT) faling_VALUE("ArrayIndexOutOfBoundsException");
                    else if (첫값 == greep_data && bestemming_VALUE_INDEX > BEGIN_plaas) { for (int lus_INDEX = inskrywing_COUNT - 1; lus_INDEX >= 0; lus_INDEX--) 힙[greep_data + 2 + bestemming_VALUE_INDEX + lus_INDEX] = 힙[첫값 + 2 + BEGIN_plaas + lus_INDEX]; }
                    else { for (int lus_INDEX = 0; lus_INDEX < inskrywing_COUNT && !Fout; lus_INDEX++) { int data_VALUE = 힙[첫값 + 2 + BEGIN_plaas + lus_INDEX]; if (kategorie_CODE != 3 || 배열저장가능(greep_data, data_VALUE)) 힙[greep_data + 2 + bestemming_VALUE_INDEX + lus_INDEX] = data_VALUE; } }
                }
                return true;
            }
        }
        if (Word_SMS(eienaar, "java/util/ArrayList") || Word_SMS(eienaar, "java/util/List") || Word_SMS(eienaar, "java/util/HashMap") || Word_SMS(eienaar, "java/util/Map")) {
            모음호출(eienaar, naam_konstante, 서술상수, bevel_CODE); return true;
        }
        return false;
    }
    static void 모음늘리기(int objek_Naslaan, int 필요수) {
        int 이전값 = 힙[objek_Naslaan + 2], 용량값 = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (용량값 >= 필요수) return;
        int Volgende_plaas = 용량값 < 8 ? 8 : 용량값 * 2; if (Volgende_plaas < 필요수) Volgende_plaas = 필요수;
        int data_ARRAY = toewys_Berging(3, Volgende_plaas); if (Fout) return;
        for (int lus_INDEX = 0; lus_INDEX < 용량값; lus_INDEX++) 힙[data_ARRAY + 2 + lus_INDEX] = 힙[이전값 + 2 + lus_INDEX];
        힙[objek_Naslaan + 2] = data_ARRAY; 힙참조[objek_Naslaan + 2] = 1;
    }
    static void 모음호출(int eienaar, int naam_konstante, int 서술상수, int bevel_CODE) {
        boolean 대응참조 = Word_SMS(eienaar, "java/util/HashMap") || Word_SMS(eienaar, "java/util/Map"); int kategorie_CODE = 대응참조 ? 11 : 10;
        if (Word_SMS(naam_konstante, "<init>") && bevel_CODE == 183 && Word_SMS(서술상수, "()V")) { int objek_Naslaan = 빼기(2); if (objek_VALUE(objek_Naslaan, kategorie_CODE)) 모음늘리기(objek_Naslaan, 8); return; }
        if (bevel_CODE != 182 && bevel_CODE != 185) { faling_VALUE("invalid collection invocation"); return; }
        if (Word_SMS(naam_konstante, "size") && Word_SMS(서술상수, "()I") || Word_SMS(naam_konstante, "isEmpty") && Word_SMS(서술상수, "()Z")) {
            int objek_Naslaan = 빼기(2); if (objek_VALUE(objek_Naslaan, kategorie_CODE)) 넣기(Word_SMS(naam_konstante, "size") ? 힙[objek_Naslaan + 3] : 힙[objek_Naslaan + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_SMS(naam_konstante, "clear") && Word_SMS(서술상수, "()V")) { int objek_Naslaan = 빼기(2); if (objek_VALUE(objek_Naslaan, kategorie_CODE)) { int data_ARRAY = 힙[objek_Naslaan + 2]; for (int lus_INDEX = 0; lus_INDEX < 힙[data_ARRAY + 1]; lus_INDEX++) 힙[data_ARRAY + 2 + lus_INDEX] = 0; 힙[objek_Naslaan + 3] = 0; } return; }
        if (!대응참조 && Word_SMS(naam_konstante, "add") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int data_VALUE = 빼기(2), objek_Naslaan = 빼기(2); if (!objek_VALUE(objek_Naslaan, 10)) return;
            int inskrywing_COUNT = 힙[objek_Naslaan + 3]; 모음늘리기(objek_Naslaan, inskrywing_COUNT + 1); if (!Fout) { 힙[힙[objek_Naslaan + 2] + 2 + inskrywing_COUNT] = data_VALUE; 힙[objek_Naslaan + 3] = inskrywing_COUNT + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_SMS(naam_konstante, "get") || Word_SMS(naam_konstante, "remove")) && Word_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Word_SMS(naam_konstante, "set") && Word_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = Word_SMS(naam_konstante, "set"); int data_VALUE = 지정여부 ? 빼기(2) : 0, inskrywing_plaas = 빼기(1), objek_Naslaan = 빼기(2);
            if (!objek_VALUE(objek_Naslaan, 10)) return;
            int inskrywing_COUNT = 힙[objek_Naslaan + 3], data_ARRAY = 힙[objek_Naslaan + 2];
            if (inskrywing_plaas < 0 || inskrywing_plaas >= inskrywing_COUNT) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[data_ARRAY + 2 + inskrywing_plaas];
            if (지정여부) 힙[data_ARRAY + 2 + inskrywing_plaas] = data_VALUE;
            if (Word_SMS(naam_konstante, "remove")) { for (int lus_INDEX = inskrywing_plaas + 1; lus_INDEX < inskrywing_COUNT; lus_INDEX++) 힙[data_ARRAY + 1 + lus_INDEX] = 힙[data_ARRAY + 2 + lus_INDEX]; 힙[data_ARRAY + 1 + inskrywing_COUNT] = 0; 힙[objek_Naslaan + 3] = inskrywing_COUNT - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Word_SMS(naam_konstante, "get") || Word_SMS(naam_konstante, "remove")) && Word_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(naam_konstante, "put") && Word_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(naam_konstante, "containsKey") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_SMS(naam_konstante, "put"), verwyder = Word_SMS(naam_konstante, "remove");
            int data_VALUE = 넣기여부 ? 빼기(2) : 0, Sleutel_Naslaan = 빼기(2), objek_Naslaan = 빼기(2); if (!objek_VALUE(objek_Naslaan, 11)) return;
            int inskrywing_COUNT = 힙[objek_Naslaan + 3], data_ARRAY = 힙[objek_Naslaan + 2], 찾은여부 = -1;
            for (int lus_INDEX = 0; lus_INDEX < inskrywing_COUNT; lus_INDEX++) if (값같음(Sleutel_Naslaan, 힙[data_ARRAY + 2 + 2 * lus_INDEX])) { 찾은여부 = lus_INDEX; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[data_ARRAY + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(objek_Naslaan, (inskrywing_COUNT + 1) * 2); data_ARRAY = 힙[objek_Naslaan + 2]; 찾은여부 = inskrywing_COUNT; if (!Fout) 힙[objek_Naslaan + 3] = inskrywing_COUNT + 1; }
                if (!Fout) { 힙[data_ARRAY + 2 + 2 * 찾은여부] = Sleutel_Naslaan; 힙[data_ARRAY + 3 + 2 * 찾은여부] = data_VALUE; }
            }
            if (verwyder && 찾은여부 >= 0) { for (int lus_INDEX = 찾은여부 + 1; lus_INDEX < inskrywing_COUNT; lus_INDEX++) { 힙[data_ARRAY + 2 * lus_INDEX] = 힙[data_ARRAY + 2 + 2 * lus_INDEX]; 힙[data_ARRAY + 1 + 2 * lus_INDEX] = 힙[data_ARRAY + 3 + 2 * lus_INDEX]; } 힙[data_ARRAY + 2 * inskrywing_COUNT] = 0; 힙[data_ARRAY + 1 + 2 * inskrywing_COUNT] = 0; 힙[objek_Naslaan + 3] = inskrywing_COUNT - 1; }
            if (Word_SMS(naam_konstante, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        faling_VALUE("unsupported collection method");
    }
    static boolean 잠금얻기(int objek_Naslaan) {
        if (!객체유효(objek_Naslaan)) return false;
        if (잠금깊이[objek_Naslaan] != 0 && 잠금주인[objek_Naslaan] != 현재가닥 + 1) { 바꿈요청 = true; return false; }
        잠금주인[objek_Naslaan] = 현재가닥 + 1; 잠금깊이[objek_Naslaan]++; return true;
    }
    static void 잠금풀기(int objek_Naslaan) {
        if (!객체유효(objek_Naslaan)) return;
        if (잠금깊이[objek_Naslaan] == 0 || 잠금주인[objek_Naslaan] != 현재가닥 + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[objek_Naslaan] == 0) 잠금주인[objek_Naslaan] = 0;
    }
    static boolean SWITCH_draad() {
        draad_raam[현재가닥] = raam_INDEX;
        if (raam_INDEX < 현재가닥 * 32) draad_stand[현재가닥] = 3;
        for (int lus_INDEX = 0; lus_INDEX < draad_COUNT; lus_INDEX++) if (draad_stand[lus_INDEX] == 2 && draad_stand[가닥대기[lus_INDEX]] == 3) draad_stand[lus_INDEX] = 1;
        for (int lus_INDEX = 1; lus_INDEX <= draad_COUNT; lus_INDEX++) {
            int Volgende_plaas = (현재가닥 + lus_INDEX) % draad_COUNT;
            if (draad_stand[Volgende_plaas] == 1) { 현재가닥 = Volgende_plaas; raam_INDEX = draad_raam[Volgende_plaas]; 바꿈요청 = false; return true; }
        }
        for (int lus_INDEX = 0; lus_INDEX < draad_COUNT; lus_INDEX++) if (draad_stand[lus_INDEX] != 3) { faling_VALUE("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int naam_konstante, int 서술상수, int bevel_CODE) { Proses_draad(naam_konstante, 서술상수, bevel_CODE, false); }
    static void Proses_draad(int naam_konstante, int 서술상수, int bevel_CODE, boolean 한국어) {
        if (bevel_CODE == 184 && Word_SMS(naam_konstante, 한국어 ? "YIELD_taak" : "yield") && Word_SMS(서술상수, "()V")) { 바꿈요청 = true; return; }
        if (bevel_CODE == 184 && Word_SMS(naam_konstante, "currentThread") && Word_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(draad_objek[현재가닥], 2); return; }
        if (bevel_CODE == 183 && Word_SMS(naam_konstante, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, 한국어 ? "(L한국어/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int teiken_adres = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), objek_Naslaan = 빼기(2);
            if (!객체유효(objek_Naslaan)) return;
            if (힙[objek_Naslaan] == 13) { 힙[objek_Naslaan + 2] = teiken_adres; 힙참조[objek_Naslaan + 2] = 1; }
            else if (teiken_adres != 0) faling_VALUE("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (bevel_CODE == 182 && (Word_SMS(naam_konstante, 한국어 ? "BEGIN_taak" : "start") || Word_SMS(naam_konstante, 한국어 ? "기다리기" : "join")) && Word_SMS(서술상수, "()V") || bevel_CODE == 182 && Word_SMS(naam_konstante, 한국어 ? "살아있는가" : "isAlive") && Word_SMS(서술상수, "()Z")) {
            int objek_Naslaan = 빼기(2); if (!객체유효(objek_Naslaan)) return;
            int rekening_VALUE = -1; for (int lus_INDEX = 0; lus_INDEX < draad_COUNT; lus_INDEX++) if (draad_objek[lus_INDEX] == objek_Naslaan) rekening_VALUE = lus_INDEX;
            if (Word_SMS(naam_konstante, 한국어 ? "살아있는가" : "isAlive")) { 넣기(rekening_VALUE >= 0 && draad_stand[rekening_VALUE] != 3 ? 1 : 0, 1); return; }
            if (Word_SMS(naam_konstante, 한국어 ? "기다리기" : "join")) { if (rekening_VALUE >= 0 && draad_stand[rekening_VALUE] != 3) { 가닥대기[현재가닥] = rekening_VALUE; draad_stand[현재가닥] = 2; 바꿈요청 = true; } return; }
            if (rekening_VALUE >= 0) { 예외던짐(한국어 ? 38 : 16, "thread already started"); return; }
            if (draad_COUNT == 4) { faling_VALUE("thread limit (4 including main)"); return; }
            int teiken_adres = 힙[objek_Naslaan] == 13 ? 힙[objek_Naslaan + 2] : objek_Naslaan;
            int lêer_INDEX = teiken_adres > 0 && 힙[teiken_adres] >= 32 ? naam_metode(힙[teiken_adres] - 32, 한국어 ? "Voer_uit" : "run", "()V") : -1;
            if (teiken_adres != 0 && lêer_INDEX < 0) { faling_VALUE("Runnable.run required"); return; }
            rekening_VALUE = draad_COUNT++; draad_objek[rekening_VALUE] = objek_Naslaan; draad_teiken[rekening_VALUE] = teiken_adres;
            int raam = rekening_VALUE * 32; draad_raam[rekening_VALUE] = lêer_INDEX < 0 ? raam - 1 : raam; draad_stand[rekening_VALUE] = lêer_INDEX < 0 ? 3 : 1;
            if (lêer_INDEX >= 0) { raam_metode[raam] = lêer_INDEX; raam_plaas[raam] = metode_BEGIN[lêer_INDEX]; lokaal_VALUE[raam * 128] = teiken_adres; lokaal_TYPE[raam * 128] = 2; }
            return;
        }
        faling_VALUE("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], adres_SMS = new int[16];
    static int lokaal_adres() { return adres_objek(0x7f000001); }
    static int adres_objek(int VALUE) { int objek_Naslaan = toewys_Berging(14, 1); if (!Fout) 힙[objek_Naslaan + 2] = VALUE; return objek_Naslaan; }
    static int 주소해독(int objek_Naslaan) {
        if (objek_Naslaan == 0 || 글같음(objek_Naslaan, hou_karakter("localhost"), false)) return 0x7f000001;
        if (!objek_VALUE(objek_Naslaan, 1)) return 0;
        int data_VALUE = 0, 총수 = 0, adres_greep = 0, 자릿수 = 0, inskrywing_COUNT = 힙[objek_Naslaan + 1];
        for (int lus_INDEX = 0; lus_INDEX <= inskrywing_COUNT; lus_INDEX++) {
            int karakterkode = lus_INDEX == inskrywing_COUNT ? '.' : 힙[objek_Naslaan + 2 + lus_INDEX];
            if (karakterkode == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } data_VALUE = data_VALUE << 8 | adres_greep; 총수++; adres_greep = 자릿수 = 0; }
            else { if (karakterkode < '0' || karakterkode > '9' || ++자릿수 > 3 || (adres_greep = adres_greep * 10 + karakterkode - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return data_VALUE;
    }
    static int adres_karakter(int data_VALUE) {
        int inskrywing_COUNT = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int adres_greep = data_VALUE >>> 이동비트 & 255;
            if (adres_greep >= 100) adres_SMS[inskrywing_COUNT++] = '0' + adres_greep / 100;
            if (adres_greep >= 10) adres_SMS[inskrywing_COUNT++] = '0' + adres_greep / 10 % 10;
            adres_SMS[inskrywing_COUNT++] = '0' + adres_greep % 10; if (이동비트 != 0) adres_SMS[inskrywing_COUNT++] = '.';
        }
        int objek_Naslaan = toewys_Berging(1, inskrywing_COUNT); if (!Fout) for (int lus_INDEX = 0; lus_INDEX < inskrywing_COUNT; lus_INDEX++) 힙[objek_Naslaan + 2 + lus_INDEX] = adres_SMS[lus_INDEX]; return objek_Naslaan;
    }
    static void 통신호출(int eienaar, int naam_konstante, int 서술상수, int bevel_CODE) {
        if (Word_SMS(eienaar, "java/net/InetAddress")) {
            if (bevel_CODE == 184 && Word_SMS(naam_konstante, "getLoopbackAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(lokaal_adres(), 2); return; }
            if (bevel_CODE == 184 && Word_SMS(naam_konstante, "getByName") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int data_VALUE = 주소해독(빼기(2)); if (던진객체 == 0 && !Fout) 넣기(adres_objek(data_VALUE), 2); return;
            }
            if (bevel_CODE == 182 && Word_SMS(naam_konstante, "getHostAddress") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int objek_Naslaan = 빼기(2); if (objek_VALUE(objek_Naslaan, 14)) 넣기(adres_karakter(힙[objek_Naslaan + 2]), 2); return; }
        }
        if (Word_SMS(eienaar, "java/net/DatagramPacket")) {
            if (bevel_CODE == 183 && Word_SMS(naam_konstante, "<init>") && (Word_SMS(서술상수, "([BI)V") || Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean bestemming_VALUE_Naslaan = Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int 접속번호 = bestemming_VALUE_Naslaan ? 빼기(1) : 0, adres_Naslaan = bestemming_VALUE_Naslaan ? 빼기(2) : 0;
                int inskrywing_COUNT = 빼기(1), data_ARRAY = 빼기(2), objek_Naslaan = 빼기(2);
                if (!objek_VALUE(objek_Naslaan, 16) || !objek_VALUE(data_ARRAY, 20)) return;
                if (inskrywing_COUNT < 0 || inskrywing_COUNT > 힙[data_ARRAY + 1] || 접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (adres_Naslaan != 0 && !objek_VALUE(adres_Naslaan, 14)) return;
                힙[objek_Naslaan + 2] = data_ARRAY; 힙참조[objek_Naslaan + 2] = 1; 힙[objek_Naslaan + 3] = inskrywing_COUNT;
                힙[objek_Naslaan + 4] = adres_Naslaan; 힙참조[objek_Naslaan + 4] = 1; 힙[objek_Naslaan + 5] = 접속번호; return;
            }
            if (bevel_CODE == 182 && Word_SMS(naam_konstante, "setLength") && Word_SMS(서술상수, "(I)V")) {
                int inskrywing_COUNT = 빼기(1), objek_Naslaan = 빼기(2); if (!objek_VALUE(objek_Naslaan, 16)) return;
                if (inskrywing_COUNT < 0 || inskrywing_COUNT > 힙[힙[objek_Naslaan + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[objek_Naslaan + 3] = inskrywing_COUNT; return;
            }
            if (bevel_CODE == 182 && (Word_SMS(naam_konstante, "getData") && Word_SMS(서술상수, "()[B") || Word_SMS(naam_konstante, "getLength") && Word_SMS(서술상수, "()I") || Word_SMS(naam_konstante, "getAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;") || Word_SMS(naam_konstante, "getPort") && Word_SMS(서술상수, "()I"))) {
                int objek_Naslaan = 빼기(2); if (!objek_VALUE(objek_Naslaan, 16)) return;
                int inskrywing_plaas = Word_SMS(naam_konstante, "getData") ? 2 : Word_SMS(naam_konstante, "getLength") ? 3 : Word_SMS(naam_konstante, "getAddress") ? 4 : 5;
                넣기(힙[objek_Naslaan + inskrywing_plaas], inskrywing_plaas == 2 || inskrywing_plaas == 4 ? 2 : 1); return;
            }
        }
        if (Word_SMS(eienaar, "java/net/DatagramSocket")) {
            if (bevel_CODE == 183 && Word_SMS(naam_konstante, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(I)V"))) {
                int 접속번호 = Word_SMS(서술상수, "()V") ? 0 : 빼기(1), objek_Naslaan = 빼기(2); if (!objek_VALUE(objek_Naslaan, 15)) return;
                if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = gebruiker.skep_Netwerk(접속번호); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[objek_Naslaan + 2] = 열린파일번호; return;
            }
            if (bevel_CODE == 182 && Word_SMS(naam_konstante, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), objek_Naslaan = 빼기(2); if (!objek_VALUE(objek_Naslaan, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[objek_Naslaan + 3] = 밀리초값; return;
            }
            if (bevel_CODE == 182 && Word_SMS(naam_konstante, "getLocalPort") && Word_SMS(서술상수, "()I")) { int objek_Naslaan = 빼기(2); if (objek_VALUE(objek_Naslaan, 15)) 넣기(힙[objek_Naslaan + 2] < 0 ? -1 : gebruiker.Netwerk_ombou(힙[objek_Naslaan + 2]), 1); return; }
            if (bevel_CODE == 182 && Word_SMS(naam_konstante, "isClosed") && Word_SMS(서술상수, "()Z")) { int objek_Naslaan = 빼기(2); if (objek_VALUE(objek_Naslaan, 15)) 넣기(힙[objek_Naslaan + 2] < 0 ? 1 : 0, 1); return; }
            if (bevel_CODE == 182 && Word_SMS(naam_konstante, "close") && Word_SMS(서술상수, "()V")) { int objek_Naslaan = 빼기(2); if (objek_VALUE(objek_Naslaan, 15) && 힙[objek_Naslaan + 2] >= 0) { gebruiker.파일서술자닫기(힙[objek_Naslaan + 2]); 힙[objek_Naslaan + 2] = -1; } return; }
            if (bevel_CODE == 182 && (Word_SMS(naam_konstante, "send") || Word_SMS(naam_konstante, "receive")) && Word_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int pakket = 빼기(2), objek_Naslaan = 빼기(2); if (!objek_VALUE(pakket, 16) || !objek_VALUE(objek_Naslaan, 15)) return;
                int data_ARRAY = 힙[pakket + 2], 유효길이 = 힙[pakket + 3], 열린파일번호 = 힙[objek_Naslaan + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_SMS(naam_konstante, "send")) {
                    if (!objek_VALUE(힙[pakket + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int lus_INDEX = 0; lus_INDEX < 유효길이; lus_INDEX++) 통신임시[lus_INDEX] = 힙[data_ARRAY + 2 + lus_INDEX];
                    if (gebruiker.e_pos_Netwerk(열린파일번호, 힙[힙[pakket + 4] + 2], 힙[pakket + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int inskrywing_COUNT = gebruiker.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (inskrywing_COUNT == -11) {
                        int 현재시각 = gebruiker.밀리초();
                        if (힙[objek_Naslaan + 4] == 0) 힙[objek_Naslaan + 4] = 현재시각 + 1;
                        if (힙[objek_Naslaan + 3] > 0 && 현재시각 - (힙[objek_Naslaan + 4] - 1) >= 힙[objek_Naslaan + 3]) { 힙[objek_Naslaan + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(objek_Naslaan, 2); 넣기(pakket, 2); raam_plaas[raam_INDEX] = raam_instruksie[raam_INDEX]; 바꿈요청 = true; return;
                    }
                    힙[objek_Naslaan + 4] = 0;
                    if (inskrywing_COUNT < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int lus_INDEX = 0; lus_INDEX < inskrywing_COUNT; lus_INDEX++) 힙[data_ARRAY + 2 + lus_INDEX] = (byte)통신임시[lus_INDEX];
                    힙[pakket + 3] = inskrywing_COUNT; 힙[pakket + 4] = adres_objek(통신임시[513]); 힙참조[pakket + 4] = 1; 힙[pakket + 5] = 통신임시[512];
                }
                return;
            }
        }
        faling_VALUE("unsupported java.net method");
    }
    static boolean 흐름대기(int objek_Naslaan) {
        int 현재시각 = gebruiker.밀리초();
        if (힙[objek_Naslaan + 5] == 0) 힙[objek_Naslaan + 5] = 현재시각 + 1;
        if (힙[objek_Naslaan + 3] > 0 && 현재시각 - (힙[objek_Naslaan + 5] - 1) >= 힙[objek_Naslaan + 3]) { 힙[objek_Naslaan + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        raam_plaas[raam_INDEX] = raam_instruksie[raam_INDEX]; 바꿈요청 = true; return true;
    }
    static void 흐름호출(int eienaar, int naam_konstante, int 서술상수, int bevel_CODE) {
        boolean 수신쪽 = Word_SMS(eienaar, "java/net/ServerSocket"), Stream = Word_SMS(eienaar, "java/io/InputStream") || Word_SMS(eienaar, "java/io/OutputStream");
        if (!Stream && bevel_CODE == 183 && Word_SMS(naam_konstante, "<init>")) {
            boolean 빈여부 = Word_SMS(서술상수, "()V"), 이름지정여부 = Word_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || 수신쪽 && Word_SMS(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { faling_VALUE("unsupported socket constructor"); return; }
            int 접속번호 = 빈여부 ? 0 : 빼기(1), adres_Naslaan = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, objek_Naslaan = 빼기(2);
            if (!objek_VALUE(objek_Naslaan, 수신쪽 ? 18 : 17)) return;
            if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !objek_VALUE(adres_Naslaan, 14)) return;
            int Netwerk_adres = 이름지정여부 ? 주소해독(adres_Naslaan) : 주소지정여부 ? 힙[adres_Naslaan + 2] : 0x7f000001;
            if (Fout || 던진객체 != 0) return;
            int 열린파일번호 = gebruiker.Stream_kontrole(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : 수신쪽 ? gebruiker.Stream_kontrole(1, 열린파일번호, 접속번호) : gebruiker.KOPPEL_Stream(열린파일번호, Netwerk_adres, 접속번호);
            if (처리값 < 0) { gebruiker.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[objek_Naslaan + 2] = 열린파일번호; 힙[objek_Naslaan + 4] = 접속번호; 힙[objek_Naslaan + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!Stream && Word_SMS(naam_konstante, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), objek_Naslaan = 빼기(2); if (!objek_VALUE(objek_Naslaan, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[objek_Naslaan + 3] = 밀리초값; return; }
        if (!Stream && Word_SMS(naam_konstante, "close") && Word_SMS(서술상수, "()V")) { int objek_Naslaan = 빼기(2); if (objek_VALUE(objek_Naslaan, 수신쪽 ? 18 : 17) && 힙[objek_Naslaan + 2] >= 0) { gebruiker.파일서술자닫기(힙[objek_Naslaan + 2]); 힙[objek_Naslaan + 2] = -1; } return; }
        if (!Stream && (Word_SMS(naam_konstante, "getLocalPort") || Word_SMS(naam_konstante, "getPort") || Word_SMS(naam_konstante, "isClosed") || Word_SMS(naam_konstante, "isConnected"))) {
            int objek_Naslaan = 빼기(2); if (!objek_VALUE(objek_Naslaan, 수신쪽 ? 18 : 17)) return;
            넣기(Word_SMS(naam_konstante, "isClosed") ? 힙[objek_Naslaan + 2] < 0 ? 1 : 0 : Word_SMS(naam_konstante, "isConnected") ? 힙[objek_Naslaan + 6] : Word_SMS(naam_konstante, "getPort") ? 힙[objek_Naslaan + 4] : 힙[objek_Naslaan + 2] < 0 ? -1 : gebruiker.Stream_kontrole(4, 힙[objek_Naslaan + 2], 0), 1); return;
        }
        if (수신쪽 && Word_SMS(naam_konstante, "accept") && Word_SMS(서술상수, "()Ljava/net/Socket;")) {
            int objek_Naslaan = 빼기(2); if (!objek_VALUE(objek_Naslaan, 18)) return; int 열린파일번호 = gebruiker.Stream_kontrole(3, 힙[objek_Naslaan + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(objek_Naslaan)) 넣기(objek_Naslaan, 2); return; }
            힙[objek_Naslaan + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = toewys_Berging(17, 5); if (Fout) { gebruiker.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = gebruiker.Stream_kontrole(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !Stream && ((Word_SMS(naam_konstante, "getInputStream") && Word_SMS(서술상수, "()Ljava/io/InputStream;")) || (Word_SMS(naam_konstante, "getOutputStream") && Word_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int objek_Naslaan = 빼기(2); if (!objek_VALUE(objek_Naslaan, 17)) return; if (힙[objek_Naslaan + 2] < 0 || 힙[objek_Naslaan + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = toewys_Berging(19, 4); if (Fout) return; 힙[반환값 + 2] = objek_Naslaan; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Word_SMS(naam_konstante, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (Stream) {
            boolean 읽기여부 = Word_SMS(naam_konstante, "read"), 쓰기여부 = Word_SMS(naam_konstante, "write"), blokkeer = Word_SMS(서술상수, "([B)I") || Word_SMS(서술상수, "([B)V"), 부분배열여부 = Word_SMS(서술상수, "([BII)I") || Word_SMS(서술상수, "([BII)V");
            int inskrywing_COUNT = 부분배열여부 ? 빼기(1) : 0, 시작변위 = 부분배열여부 ? 빼기(1) : 0, data_ARRAY = blokkeer || 부분배열여부 ? 빼기(2) : 0;
            int data_VALUE = 쓰기여부 && Word_SMS(서술상수, "(I)V") ? 빼기(1) : 0, objek_Naslaan = 빼기(2);
            if (!objek_VALUE(objek_Naslaan, 19)) return; int 부모참조 = 힙[objek_Naslaan + 2], 열린파일번호 = 힙[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_SMS(naam_konstante, "close") && Word_SMS(서술상수, "()V")) { gebruiker.파일서술자닫기(열린파일번호); 힙[부모참조 + 2] = -1; return; }
            if (Word_SMS(naam_konstante, "flush") && Word_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !쓰기여부) || 읽기여부 != (힙[objek_Naslaan + 3] == 0)) { faling_VALUE("unsupported stream operation"); return; }
            if (blokkeer || 부분배열여부) { if (!objek_VALUE(data_ARRAY, 20)) return; if (blokkeer) inskrywing_COUNT = 힙[data_ARRAY + 1]; if (시작변위 < 0 || inskrywing_COUNT < 0 || 시작변위 > 힙[data_ARRAY + 1] - inskrywing_COUNT) { 예외던짐(6, "stream array bounds"); return; } }
            else inskrywing_COUNT = 1;
            if (inskrywing_COUNT == 0) { if (읽기여부) 넣기(0, 1); return; }
            int 완료수 = 쓰기여부 ? 힙[objek_Naslaan + 4] : 0, 처리값 = 0;
            while (완료수 < inskrywing_COUNT) {
                처리값 = 읽기여부 ? gebruiker.파일한바이트읽기(열린파일번호) : gebruiker.파일한바이트쓰기(열린파일번호, blokkeer || 부분배열여부 ? 힙[data_ARRAY + 2 + 시작변위 + 완료수] : data_VALUE);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (blokkeer || 부분배열여부)) 힙[data_ARRAY + 2 + 시작변위 + 완료수] = (byte)처리값;
                완료수++; if (읽기여부 && !(blokkeer || 부분배열여부)) break;
            }
            if (처리값 == -11 && (쓰기여부 || 완료수 == 0)) {
                힙[objek_Naslaan + 4] = 완료수;
                if (흐름대기(부모참조)) { 넣기(objek_Naslaan, 2); if (blokkeer || 부분배열여부) 넣기(data_ARRAY, 2); if (부분배열여부) { 넣기(시작변위, 1); 넣기(inskrywing_COUNT, 1); } if (쓰기여부 && !(blokkeer || 부분배열여부)) 넣기(data_VALUE, 1); } return;
            }
            힙[objek_Naslaan + 4] = 0; 힙[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(완료수 == 0 && 처리값 == 256 ? -1 : blokkeer || 부분배열여부 ? 완료수 : 처리값, 1); return;
        }
        faling_VALUE("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int naam_konstante) {
        if (Word_SMS(naam_konstante, "한국어/자체/venster")) return 24;
        if (Word_SMS(naam_konstante, "한국어/자체/etiket")) return 26;
        if (Word_SMS(naam_konstante, "한국어/자체/knoppie")) return 27;
        if (Word_SMS(naam_konstante, "한국어/자체/SMS_veld")) return 28;
        if (Word_SMS(naam_konstante, "한국어/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int naam_konstante) {
        return 한국어화면종(naam_konstante) != 0 || Word_SMS(naam_konstante, "한국어/자체/화면구성요소") || Word_SMS(naam_konstante, "한국어/자체/gebeurtenis_tou");
    }
    static int 화면종(int naam_konstante) {
        int 한국어종 = 한국어화면종(naam_konstante); if (한국어종 != 0) return 한국어종;
        if (Word_SMS(naam_konstante, "javax/swing/JFrame")) return 24;
        if (Word_SMS(naam_konstante, "javax/swing/JPanel")) return 25;
        if (Word_SMS(naam_konstante, "javax/swing/JLabel")) return 26;
        if (Word_SMS(naam_konstante, "javax/swing/JButton")) return 27;
        if (Word_SMS(naam_konstante, "javax/swing/JTextField")) return 28;
        if (Word_SMS(naam_konstante, "java/awt/event/ActionEvent")) return 29;
        if (Word_SMS(naam_konstante, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int naam_konstante) {
        return 화면종(naam_konstante) != 0 || Word_SMS(naam_konstante, "java/awt/Component") || Word_SMS(naam_konstante, "java/awt/Container") || Word_SMS(naam_konstante, "javax/swing/JComponent") || Word_SMS(naam_konstante, "javax/swing/AbstractButton") || Word_SMS(naam_konstante, "javax/swing/text/JTextComponent") || Word_SMS(naam_konstante, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int objek_Naslaan) { if (!객체유효(objek_Naslaan)) return false; if (힙[objek_Naslaan] < 24 || 힙[objek_Naslaan] > 28) { faling_VALUE("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int objek_Naslaan, int SMS_Naslaan) {
        if (SMS_Naslaan != 0 && !objek_VALUE(SMS_Naslaan, 1)) return;
        int inskrywing_COUNT = SMS_Naslaan == 0 ? 0 : 힙[SMS_Naslaan + 1]; if (inskrywing_COUNT > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int lus_INDEX = 0; lus_INDEX < inskrywing_COUNT; lus_INDEX++) 화면글임시[lus_INDEX] = 힙[SMS_Naslaan + 2 + lus_INDEX];
        if (gebruiker.화면글(힙[objek_Naslaan + 2], 화면글임시, inskrywing_COUNT) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[objek_Naslaan + 3] = SMS_Naslaan; 힙참조[objek_Naslaan + 3] = 1;
    }
    static int 화면문자읽기(int objek_Naslaan) {
        int rekening_VALUE = 힙[objek_Naslaan + 2], inskrywing_COUNT = gebruiker.화면연결(8, rekening_VALUE, 0, 0, 0, 0), 사용수 = 0;
        if (inskrywing_COUNT < 0) { faling_VALUE("GUI text read failed"); return 0; }
        for (int lus_INDEX = 0; lus_INDEX < inskrywing_COUNT; lus_INDEX++) { int 부호값 = gebruiker.화면연결(9, rekening_VALUE, lus_INDEX, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = toewys_Berging(1, 사용수); if (!Fout) for (int lus_INDEX = 0; lus_INDEX < 사용수; lus_INDEX++) 힙[반환값 + 2 + lus_INDEX] = 화면글임시[lus_INDEX]; return 반환값;
    }
    /* 한국어 객체를 직접 만들고 kern_VALUE 화면 기능에 연결한다. Swing objek_VALUE/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int eienaar, int naam_konstante, int 서술상수, int bevel_CODE) {
        if (Word_SMS(eienaar, "한국어/자체/gebeurtenis_tou")) {
            if (bevel_CODE == 184 && Word_SMS(naam_konstante, "나중에실행") && Word_SMS(서술상수, "(L한국어/자체/실행할일;)V")) {
                int taak_aksie = 빼기(2); if (!객체유효(taak_aksie)) return;
                if (나중수 == 8) { faling_VALUE("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = taak_aksie; return;
            }
            if (bevel_CODE == 184 && Word_SMS(naam_konstante, "사건처리중인가") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            faling_VALUE("지원하지 않는 한국어 화면 일정 호출"); return;
        }
        if (Word_SMS(eienaar, "한국어/자체/동작알림")) {
            int 알림 = 빼기(2); if (!objek_VALUE(알림, 29) || 힙[알림 + 3] == 0) return;
            if (Word_SMS(naam_konstante, "gebeurtenis_bron") && Word_SMS(서술상수, "()L한국어/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (Word_SMS(naam_konstante, "bevel_SMS") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (Word_SMS(naam_konstante, "INDEX") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else faling_VALUE("지원하지 않는 한국어 Aksie 알림 호출"); return;
        }
        if (bevel_CODE == 183 && Word_SMS(naam_konstante, "<init>")) {
            int 종류 = 한국어화면종(eienaar), 받이 = 0, 가로 = 0, Vertikaal_plaas = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Word_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (gebruiker.화면너비() - 폭) / 2; Vertikaal_plaas = (gebruiker.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Word_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Word_SMS(서술상수, "(Ljava/lang/String;IIIIL한국어/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); Vertikaal_plaas = 빼기(1); 가로 = 빼기(1);
            } else { faling_VALUE("지원하지 않는 한국어 화면 생성자"); return; }
            int Teks = 빼기(2), element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || Vertikaal_plaas < 0 || 폭 > gebruiker.화면너비() - 가로 || 높이 > gebruiker.화면높이() - Vertikaal_plaas) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDEX = gebruiker.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (INDEX < 1 || INDEX > 32) { faling_VALUE("화면 element_VALUE 자리가 가득 찼습니다"); return; }
            힙[element_VALUE + 2] = INDEX; 화면참조[INDEX - 1] = element_VALUE;
            힙[element_VALUE + 5] = 가로; 힙[element_VALUE + 6] = Vertikaal_plaas; 힙[element_VALUE + 7] = 폭; 힙[element_VALUE + 8] = 높이; 힙[element_VALUE + 10] = 2;
            힙[element_VALUE + 4] = 받이; 힙참조[element_VALUE + 4] = 1; 힙[element_VALUE + 12] = 1;
            gebruiker.화면연결(1, INDEX, 가로, Vertikaal_plaas, 폭, 높이);
            if (종류 == 24) gebruiker.화면연결(7, INDEX, 2, 0, 0, 0);
            화면문자설정(element_VALUE, Teks); return;
        }
        if (bevel_CODE != 182) { faling_VALUE("잘못된 한국어 화면 호출 Opdrag"); return; }
        if (Word_SMS(naam_konstante, "skryf_SMS") && Word_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int Teks = 빼기(2), element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 화면문자설정(element_VALUE, Teks); return;
        }
        if (Word_SMS(naam_konstante, "글읽기") && Word_SMS(서술상수, "()Ljava/lang/String;")) {
            int element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 넣기(화면문자읽기(element_VALUE), 2); return;
        }
        if (Word_SMS(naam_konstante, "동작맡기기") && Word_SMS(서술상수, "(L한국어/자체/동작받이;)V")) {
            int 받이 = 빼기(2), element_VALUE = 빼기(2);
            if (화면객체(element_VALUE)) { 힙[element_VALUE + 4] = 받이; 힙참조[element_VALUE + 4] = 1; 힙[element_VALUE + 12] = 1; } return;
        }
        if (Word_SMS(naam_konstante, "byvoeg_element") && Word_SMS(서술상수, "(L한국어/자체/화면구성요소;)V")) {
            int kind_VALUE = 빼기(2), 부모 = 빼기(2); if (!화면객체(kind_VALUE) || !화면객체(부모)) return;
            if (gebruiker.화면연결(2, 힙[부모 + 2], 힙[kind_VALUE + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[kind_VALUE + 11] = 부모; 힙참조[kind_VALUE + 11] = 1; return;
        }
        if (Word_SMS(naam_konstante, "자리정하기") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), Vertikaal_plaas = 빼기(1), 가로 = 빼기(1), element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (gebruiker.화면연결(1, 힙[element_VALUE + 2], 가로, Vertikaal_plaas, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[element_VALUE + 5] = 가로; 힙[element_VALUE + 6] = Vertikaal_plaas; 힙[element_VALUE + 7] = 폭; 힙[element_VALUE + 8] = 높이; return;
        }
        if ((Word_SMS(naam_konstante, "wys_venster") || Word_SMS(naam_konstante, "Sluit")) && Word_SMS(서술상수, "()V")) {
            boolean sigbaarheid_VALUE = Word_SMS(naam_konstante, "wys_venster"); int element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (gebruiker.화면연결(sigbaarheid_VALUE ? 3 : 4, 힙[element_VALUE + 2], sigbaarheid_VALUE ? 1 : 0, 0, 0, 0) < 0) { faling_VALUE("화면은 interaktief 명령에서 실행해야 합니다"); return; }
            힙[element_VALUE + 9] = sigbaarheid_VALUE ? 1 : 0; return;
        }
        if (Word_SMS(naam_konstante, "보이는가") && Word_SMS(서술상수, "()Z")) { int element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 넣기(힙[element_VALUE + 9], 1); return; }
        faling_VALUE("지원하지 않는 한국어 화면 metode_VALUE");
    }
    static void 화면호출(int eienaar, int naam_konstante, int 서술상수, int bevel_CODE) {
        if (Word_SMS(eienaar, "javax/swing/SwingUtilities")) {
            if (bevel_CODE == 184 && Word_SMS(naam_konstante, "invokeLater") && Word_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int objek_Naslaan = 빼기(2); if (!객체유효(objek_Naslaan)) return; if (나중수 == 8) { faling_VALUE("invokeLater queue full"); return; } 나중실행[나중수++] = objek_Naslaan; return; }
            if (bevel_CODE == 184 && Word_SMS(naam_konstante, "isEventDispatchThread") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            faling_VALUE("unsupported SwingUtilities method"); return;
        }
        if (Word_SMS(eienaar, "java/awt/event/ActionEvent")) {
            int objek_Naslaan = 빼기(2); if (!objek_VALUE(objek_Naslaan, 29)) return;
            if (Word_SMS(naam_konstante, "getSource") && Word_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[objek_Naslaan + 2], 2);
            else if (Word_SMS(naam_konstante, "getActionCommand") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[objek_Naslaan + 2]), 2);
            else if (Word_SMS(naam_konstante, "getID") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else faling_VALUE("unsupported ActionEvent method"); return;
        }
        if (bevel_CODE == 183 && Word_SMS(naam_konstante, "<init>")) {
            int COLUMNS = 0, SMS_Naslaan = 0;
            if (Word_SMS(서술상수, "(I)V")) COLUMNS = 빼기(1);
            else if (Word_SMS(서술상수, "(Ljava/lang/String;I)V")) { COLUMNS = 빼기(1); SMS_Naslaan = 빼기(2); }
            else if (Word_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_Naslaan = 빼기(2);
            else if (Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_SMS(서술상수, "()V")) { faling_VALUE("unsupported Swing constructor"); return; }
            int objek_Naslaan = 빼기(2); if (!객체유효(objek_Naslaan)) return;
            if (힙[objek_Naslaan] == 30) { faling_VALUE("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(objek_Naslaan) || COLUMNS < 0) return;
            int rekening_VALUE = gebruiker.화면연결(0, 힙[objek_Naslaan] - 23, 0, 0, 0, 0);
            if (rekening_VALUE < 1 || rekening_VALUE > 32) { faling_VALUE("GUI widget slots exhausted"); return; }
            힙[objek_Naslaan + 2] = rekening_VALUE; 화면참조[rekening_VALUE - 1] = objek_Naslaan; 힙[objek_Naslaan + 5] = 힙[objek_Naslaan] == 24 ? 130 : 16; 힙[objek_Naslaan + 6] = 힙[objek_Naslaan] == 24 ? 110 : 16;
            힙[objek_Naslaan + 7] = 힙[objek_Naslaan] == 24 ? 380 : 220; 힙[objek_Naslaan + 8] = 힙[objek_Naslaan] == 24 ? 240 : 28; 힙[objek_Naslaan + 10] = 1;
            화면문자설정(objek_Naslaan, SMS_Naslaan); return;
        }
        if (Word_SMS(naam_konstante, "setText") || Word_SMS(naam_konstante, "setTitle")) { int SMS_Naslaan = 빼기(2), objek_Naslaan = 빼기(2); if (화면객체(objek_Naslaan) && Word_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(objek_Naslaan, SMS_Naslaan); return; }
        if (Word_SMS(naam_konstante, "getText") || Word_SMS(naam_konstante, "getTitle")) { int objek_Naslaan = 빼기(2); if (화면객체(objek_Naslaan) && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(objek_Naslaan), 2); return; }
        if (Word_SMS(naam_konstante, "addActionListener") && Word_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), objek_Naslaan = 빼기(2); if (화면객체(objek_Naslaan)) { 힙[objek_Naslaan + 4] = 수신참조; 힙참조[objek_Naslaan + 4] = 1; } return; }
        if (Word_SMS(naam_konstante, "getContentPane") && Word_SMS(서술상수, "()Ljava/awt/Container;")) { int objek_Naslaan = 빼기(2); if (화면객체(objek_Naslaan)) 넣기(objek_Naslaan, 2); return; }
        if (Word_SMS(naam_konstante, "setLayout") && Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Uitleg_Naslaan = 빼기(2), objek_Naslaan = 빼기(2); if (화면객체(objek_Naslaan) && Uitleg_Naslaan != 0) faling_VALUE("only absolute layout (null) is supported"); return; }
        if (Word_SMS(naam_konstante, "add") && (Word_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Uitleg_toestand = Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Uitleg_toestand) 빼기(2);
            int kind_Naslaan = 빼기(2), objek_Naslaan = 빼기(2); if (!화면객체(kind_Naslaan) || !화면객체(objek_Naslaan)) return;
            if (gebruiker.화면연결(2, 힙[objek_Naslaan + 2], 힙[kind_Naslaan + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[kind_Naslaan + 11] = objek_Naslaan; 힙참조[kind_Naslaan + 11] = 1; if (!Uitleg_toestand) 넣기(kind_Naslaan, 2); return;
        }
        if (Word_SMS(naam_konstante, "setBounds") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), Y_koördinaat = 빼기(1), x_koördinaat = 빼기(1), objek_Naslaan = 빼기(2); if (!화면객체(objek_Naslaan)) return;
            if (gebruiker.화면연결(1, 힙[objek_Naslaan + 2], x_koördinaat, Y_koördinaat, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[objek_Naslaan + 5] = x_koördinaat; 힙[objek_Naslaan + 6] = Y_koördinaat; 힙[objek_Naslaan + 7] = 너비; 힙[objek_Naslaan + 8] = 높이; return;
        }
        if (Word_SMS(naam_konstante, "setSize") && Word_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), objek_Naslaan = 빼기(2); if (!화면객체(objek_Naslaan)) return;
            if (gebruiker.화면연결(1, 힙[objek_Naslaan + 2], 힙[objek_Naslaan + 5], 힙[objek_Naslaan + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[objek_Naslaan + 7] = 너비; 힙[objek_Naslaan + 8] = 높이; } return;
        }
        if (Word_SMS(naam_konstante, "setLocationRelativeTo") && Word_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), objek_Naslaan = 빼기(2); if (!화면객체(objek_Naslaan)) return; if (상대배치 != 0) { faling_VALUE("only screen centering supported"); return; } 힙[objek_Naslaan + 5] = (gebruiker.화면너비() - 힙[objek_Naslaan + 7]) / 2; 힙[objek_Naslaan + 6] = (gebruiker.화면높이() - 힙[objek_Naslaan + 8]) / 2; gebruiker.화면연결(1, 힙[objek_Naslaan + 2], 힙[objek_Naslaan + 5], 힙[objek_Naslaan + 6], 힙[objek_Naslaan + 7], 힙[objek_Naslaan + 8]); return; }
        if (Word_SMS(naam_konstante, "setDefaultCloseOperation") && Word_SMS(서술상수, "(I)V")) { int beleid = 빼기(1), objek_Naslaan = 빼기(2); if (화면객체(objek_Naslaan)) { if (beleid < 0 || beleid > 3) 예외던짐(9, "close policy"); else { 힙[objek_Naslaan + 10] = beleid; gebruiker.화면연결(7, 힙[objek_Naslaan + 2], beleid, 0, 0, 0); } } return; }
        if (Word_SMS(naam_konstante, "setVisible") && Word_SMS(서술상수, "(Z)V")) { int data_VALUE = 빼기(1), objek_Naslaan = 빼기(2); if (화면객체(objek_Naslaan)) { int 처리값 = gebruiker.화면연결(3, 힙[objek_Naslaan + 2], data_VALUE, 0, 0, 0); if (처리값 < 0) faling_VALUE("Swing requires a standalone interactive command"); else 힙[objek_Naslaan + 9] = data_VALUE; } return; }
        if (Word_SMS(naam_konstante, "dispose") && Word_SMS(서술상수, "()V")) { int objek_Naslaan = 빼기(2); if (화면객체(objek_Naslaan)) { gebruiker.화면연결(4, 힙[objek_Naslaan + 2], 0, 0, 0, 0); 힙[objek_Naslaan + 9] = 0; } return; }
        if (Word_SMS(naam_konstante, "repaint") || Word_SMS(naam_konstante, "validate")) { int objek_Naslaan = 빼기(2); if (!화면객체(objek_Naslaan) || !Word_SMS(서술상수, "()V")) return; gebruiker.화면연결(1, 힙[objek_Naslaan + 2], 힙[objek_Naslaan + 5], 힙[objek_Naslaan + 6], 힙[objek_Naslaan + 7], 힙[objek_Naslaan + 8]); return; }
        if (Word_SMS(naam_konstante, "isVisible") && Word_SMS(서술상수, "()Z")) { int objek_Naslaan = 빼기(2); if (화면객체(objek_Naslaan)) 넣기(힙[objek_Naslaan + 9], 1); return; }
        faling_VALUE("unsupported Swing method (native subset)");
    }
    static void 사건실행(int teiken_adres, int 사건번호, boolean 한국어) {
        if (teiken_adres < 1 || 힙[teiken_adres] < 32) { faling_VALUE("Java event listener required"); return; }
        int lêer_INDEX = naam_metode(힙[teiken_adres] - 32, 사건번호 == 0 ? (한국어 ? "Voer_uit" : "run") : (한국어 ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (한국어 ? "(L한국어/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (lêer_INDEX < 0) { faling_VALUE("event callback missing"); return; }
        현재가닥 = 0; draad_COUNT = 1; raam_INDEX = 0; draad_stand[0] = 1; raam_Stapel[0] = 0; 틀잠금[0] = inisialiseer_raam[0] = 0; 바꿈요청 = false;
        for (int lus_INDEX = 0; lus_INDEX < 128; lus_INDEX++) { lokaal_VALUE[lus_INDEX] = lokaal_TYPE[lus_INDEX] = 0; }
        raam_metode[0] = lêer_INDEX; raam_plaas[0] = metode_BEGIN[lêer_INDEX]; lokaal_VALUE[0] = teiken_adres; lokaal_TYPE[0] = 2;
        if (사건번호 != 0) { lokaal_VALUE[1] = 사건번호; lokaal_TYPE[1] = 2; }
        사건중 = true; uitvoer_bevel(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!Fout) {
            if (나중수 > 0) { int teiken_adres = 나중실행[0], 한국어 = 나중한국어[0]; for (int lus_INDEX = 1; lus_INDEX < 나중수; lus_INDEX++) { 나중실행[lus_INDEX - 1] = 나중실행[lus_INDEX]; 나중한국어[lus_INDEX - 1] = 나중한국어[lus_INDEX]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(teiken_adres, 0, 한국어 != 0); continue; }
            if (gebruiker.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = gebruiker.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { faling_VALUE("GUI event I/O failed"); return; }
            int rekening_VALUE = 사건번호 & 65535; if (rekening_VALUE < 1 || rekening_VALUE > 32) continue; int objek_Naslaan = 화면참조[rekening_VALUE - 1]; if (objek_Naslaan == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[objek_Naslaan + 10] != 0) 힙[objek_Naslaan + 9] = 0;
                if (힙[objek_Naslaan + 10] == 3) for (int lus_INDEX = 0; lus_INDEX < 32; lus_INDEX++) if (화면참조[lus_INDEX] != 0 && 힙[화면참조[lus_INDEX]] == 24) gebruiker.화면연결(4, lus_INDEX + 1, 0, 0, 0, 0);
            } else if (힙[objek_Naslaan + 4] != 0) {
                int README_Naslaan = toewys_Berging(29, 2); if (Fout) return; 힙[README_Naslaan + 2] = objek_Naslaan; 힙[README_Naslaan + 3] = 힙[objek_Naslaan + 12]; 힙참조[README_Naslaan + 2] = 1; 사건실행(힙[objek_Naslaan + 4], README_Naslaan, 힙[objek_Naslaan + 12] != 0);
            }
        }
    }
    public static int Loop() {
        if (gebruiker.인수개수() == 1 && 자바도구.같음(gebruiker.인수(0), "-version")) {
            gebruiker.Skryf("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (gebruiker.인수개수() < 1) { gebruiker.Skryf("Usage: java CLASS [ARGS]\n"); return 2; }
        inskrywing_Klas_Definisie = laai_Klas_Definisie(hou_karakter(gebruiker.인수(0))); if (Fout || inskrywing_Klas_Definisie < 0) return 1;
        int inskrywing_p_VALUE = naam_metode(inskrywing_Klas_Definisie, "Loop", "()V");
        boolean 한국어진입 = inskrywing_p_VALUE >= 0 && (metode_toegang[inskrywing_p_VALUE] & 9) == 9;
        if (!한국어진입) inskrywing_p_VALUE = naam_metode(inskrywing_Klas_Definisie, "main", "([Ljava/lang/String;)V");
        if (inskrywing_p_VALUE < 0 || (metode_toegang[inskrywing_p_VALUE] & 9) != 9) faling_VALUE("public static void Loop() or main(String[] args) required");
        if (Fout) return 1;
        int 인수 = toewys_Berging(3, gebruiker.인수개수() - 1); ARRAY_element[인수] = -1;
        for (int 수 = 1; 수 < gebruiker.인수개수() && !Fout; 수++) 힙[인수 + 1 + 수] = hou_karakter(gebruiker.인수(수));
        raam_INDEX = 0; raam_metode[0] = inskrywing_p_VALUE; raam_plaas[0] = metode_BEGIN[inskrywing_p_VALUE]; lokaal_VALUE[0] = 한국어진입 ? 0 : 인수; lokaal_TYPE[0] = 한국어진입 ? 0 : 2;
        draad_stand[0] = 1; draad_objek[0] = toewys_Berging(13, 2);
        uitvoer_bevel(); if (!Fout) 화면사건들(); return Fout ? 1 : 0;
    }
}
