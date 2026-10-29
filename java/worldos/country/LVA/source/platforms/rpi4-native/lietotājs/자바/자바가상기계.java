// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Fails/operands_kopa/Uzziņas/zars 경계를 Izpildīt_komanda 중 검사한다. */
public final class 자바가상기계 {
    static int[] Fails = new int[16 * 16384], pagaidu_fails = new int[16384], faila_nosaukums_SMS = new int[512];
    static int[] konstante_tags = new int[8192], 상가 = new int[8192], konstante_SECOND_VALUE = new int[8192], virkne_Uzziņas = new int[8192];
    static int[] metode_nosaukums_SMS = new int[512], metode_TYPE = new int[512], metode_piekļūt = new int[512], metode_īpašnieks = new int[512];
    static int[] metode_Sākt = new int[512], metode_beigt_zvanu = new int[512], metode_kopa = new int[512], 함수지역 = new int[512];
    static int[] metode_arg_COUNT = new int[512], metode_arg_TYPE = new int[8192], metode_atdot = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] vietējs_VALUE = new int[16384], vietējs_TYPE = new int[16384], operands_kopa_VALUE = new int[16384], operands_kopa_TYPE = new int[16384];
    static int[] kadrs_metode = new int[128], kadrs_amats = new int[128], kadrs_kopa = new int[128], 틀명령 = new int[128], 틀초기화 = new int[128];
    static int[] klase_definīcija_nosaukums = new int[16], klase_definīcija_mainīt_izmērus = new int[16], klase_definīcija_vecākobjekts = new int[16], klase_definīcija_Statuss = new int[16], 종칸수 = new int[16], 종초기화 = new int[16];
    static int[] klase_interfeiss = new int[16 * 16], klase_interfeiss_COUNT = new int[16];
    static int[] 칸이름 = new int[512], 칸형 = new int[512], 칸주인 = new int[512], 칸권한 = new int[512], 칸위치 = new int[512], 칸값 = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] kaudze_VALUE = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], kaudze_Uzziņas = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], masīva_elements = new int[32768], Store_vesels_skaitlis = new int[256];
    static int Izmērs, 읽기위치, metode_COUNT, klases_nosaukums, kadrs_INDEX = -1, kaudze_beigt_zvanu_amats = 1, atdot_TYPE;
    static int klase_definīcija_COUNT, 칸수, 잡기수, 현재읽는종, 던진객체, 잠시수, rādīt_COUNT, kopums_COUNT;
    static int pašreizējais_saruna, saruna_COUNT = 1, ievade_klase_definīcija;
    static int[] saruna_kadrs = new int[4], saruna_Statuss = new int[4], saruna_objekts = new int[4], saruna_mērķis = new int[4], 가닥대기 = new int[4];
    static boolean Kļūda, mainīt_pieprasījums;
    static int[] bloķēt_īpašnieks = new int[32768], 잠금깊이 = new int[32768], kadrs_bloķēt = new int[128], klase_bloķēt = new int[16], klase_saruna = new int[16];

    static void kļūme_VALUE(String Word_SMS) {
        if (Kļūda) return;
        int joma_CODE = 0;
        if (자바도구.같음(Word_SMS, "ArithmeticException: / by zero")) joma_CODE = 4;
        if (자바도구.같음(Word_SMS, "NullPointerException") || 자바도구.같음(Word_SMS, "null or invalid array")) joma_CODE = 5;
        if (자바도구.같음(Word_SMS, "ArrayIndexOutOfBoundsException")) joma_CODE = 7;
        if (자바도구.같음(Word_SMS, "StringIndexOutOfBoundsException")) joma_CODE = 8;
        if (자바도구.같음(Word_SMS, "NumberFormatException")) joma_CODE = 10;
        if (자바도구.같음(Word_SMS, "FileNotFoundException: file open failed")) joma_CODE = 12;
        if (자바도구.같음(Word_SMS, "IOException: stream closed") || 자바도구.같음(Word_SMS, "IOException: read failed") || 자바도구.같음(Word_SMS, "IOException: write failed")) joma_CODE = 11;
        if (자바도구.같음(Word_SMS, "ClassCastException")) joma_CODE = 14;
        if (자바도구.같음(Word_SMS, "NegativeArraySizeException")) joma_CODE = 15;
        if (joma_CODE != 0 && kadrs_INDEX >= 0) { 예외던짐(joma_CODE, Word_SMS); return; }
        lietotājs.Rakstīt("JVM error: "); lietotājs.Rakstīt(Word_SMS); lietotājs.rakstīšana_rakstzīme_VALUE(10); Kļūda = true;
    }
    static boolean klips(int Palaist, int 길이) {
        if (Palaist < 0 || Palaist >= Fails.length || 길이 < 0) return false;
        int klase_definīcija = Palaist / 16384;
        return Palaist % 16384 <= klase_definīcija_mainīt_izmērus[klase_definīcija] && 길이 <= klase_definīcija_mainīt_izmērus[klase_definīcija] - Palaist % 16384;
    }
    static int byte_VALUE() {
        if (!klips(읽기위치, 1)) { kļūme_VALUE("truncated class file"); return 0; }
        return Fails[읽기위치++];
    }
    static int 짧은수() { return byte_VALUE() << 8 | byte_VALUE(); }
    static int vesels_skaitlis() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int 길이) { if (!klips(읽기위치, 길이)) kļūme_VALUE("invalid attribute size"); else 읽기위치 += 길이; }
    static boolean čeks_konstante(int numurs, int 종류) {
        if (numurs <= 0 || numurs >= konstante_tags.length || konstante_tags[numurs] != 종류) { kļūme_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_diapazons(int Palaist, int 길이, String Word_SMS) {
        if (!klips(Palaist, 길이)) return false;
        int 읽는자리 = Palaist, 끝 = Palaist + 길이;
        for (int Loop_INDEX = 0; Loop_INDEX < Word_SMS.length(); Loop_INDEX++) {
            int koda_punkts = Word_SMS.charAt(Loop_INDEX);
            if (koda_punkts > 0 && koda_punkts < 128) { if (읽는자리 >= 끝 || Fails[읽는자리++] != koda_punkts) return false; }
            else if (koda_punkts < 2048) {
                if (읽는자리 + 2 > 끝 || Fails[읽는자리++] != (192 | (koda_punkts >> 6)) || Fails[읽는자리++] != (128 | (koda_punkts & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Fails[읽는자리++] != (224 | (koda_punkts >> 12)) || Fails[읽는자리++] != (128 | ((koda_punkts >> 6) & 63)) || Fails[읽는자리++] != (128 | (koda_punkts & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean Word_SMS(int konstante_VALUE, String Word_SMS) { return čeks_konstante(konstante_VALUE, 1) && SMS_diapazons(상가[konstante_VALUE], konstante_SECOND_VALUE[konstante_VALUE], Word_SMS); }
    static boolean 같은말(int 가, int SECOND_operands) {
        if (!čeks_konstante(가, 1) || !čeks_konstante(SECOND_operands, 1) || konstante_SECOND_VALUE[가] != konstante_SECOND_VALUE[SECOND_operands]) return false;
        for (int numurs = 0; numurs < konstante_SECOND_VALUE[가]; numurs++) if (Fails[상가[가] + numurs] != Fails[상가[SECOND_operands] + numurs]) return false;
        return true;
    }
    static int klases_nosaukums_SMS(int numurs) { return čeks_konstante(numurs, 7) && čeks_konstante(상가[numurs], 1) ? 상가[numurs] : 0; }
    static int Uzziņas_nosaukums(int numurs) { return čeks_konstante(numurs, 12) && čeks_konstante(상가[numurs], 1) ? 상가[numurs] : 0; }
    static int Uzziņas_TYPE(int numurs) { return čeks_konstante(numurs, 12) && čeks_konstante(konstante_SECOND_VALUE[numurs], 1) ? konstante_SECOND_VALUE[numurs] : 0; }
    static int 서술형(int 끝, boolean 빈형) {
        if (읽기위치 >= 끝) { kļūme_VALUE("invalid descriptor"); return 0; }
        int VALUE = byte_VALUE();
        if (VALUE == 'V' && 빈형) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int Palaist = 읽기위치;
            while (읽기위치 < 끝 && Fails[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Palaist) kļūme_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        kļūme_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int FUNCTION_VALUE) {
        int 이전 = 읽기위치, numurs = metode_TYPE[FUNCTION_VALUE];
        if (!čeks_konstante(numurs, 1)) return;
        읽기위치 = 상가[numurs]; int 끝 = 읽기위치 + konstante_SECOND_VALUE[numurs];
        if (byte_VALUE() != '(') kļūme_VALUE("invalid method descriptor");
        int krājums_COUNT = 0;
        while (!Kļūda && 읽기위치 < 끝 && Fails[읽기위치] != ')') {
            if (krājums_COUNT == 16) { kļūme_VALUE("too many method arguments"); break; }
            metode_arg_TYPE[FUNCTION_VALUE * 16 + krājums_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || byte_VALUE() != ')') kļūme_VALUE("invalid method descriptor");
        metode_atdot[FUNCTION_VALUE] = 서술형(끝, true); metode_arg_COUNT[FUNCTION_VALUE] = krājums_COUNT;
        if (읽기위치 != 끝) kļūme_VALUE("invalid method descriptor");
        읽기위치 = 이전;
    }
    static int 상번호() { int VALUE = 짧은수(); return VALUE == 0 ? 0 : 현재읽는종 * 512 + VALUE; }
    static int 명상수() { return metode_īpašnieks[kadrs_metode[kadrs_INDEX]] * 512 + 명짧(); }
    static void 속성건너() {
        int krājums_COUNT = 짧은수();
        for (int numurs = 0; numurs < krājums_COUNT && !Kļūda; numurs++) { čeks_konstante(상번호(), 1); 건너(vesels_skaitlis()); }
    }
    static int 명령길이(int VALUE) {
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
    static int amats_vesels_skaitlis(int 읽는자리) {
        if (!klips(읽는자리, 4)) { kļūme_VALUE("truncated bytecode operand"); return 0; }
        return Fails[읽는자리] << 24 | Fails[읽는자리 + 1] << 16 | Fails[읽는자리 + 2] << 8 | Fails[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Palaist, int 끝) {
        int VALUE = Fails[읽는자리], 길이 = 명령길이(VALUE);
        if (VALUE == 170 || VALUE == 171) {
            int BASE_amats = 읽는자리 + 1;
            while ((BASE_amats - Palaist) % 4 != 0) BASE_amats++;
            if (끝 - BASE_amats < (VALUE == 170 ? 12 : 8)) return 0;
            int ievade_COUNT = VALUE == 170 ? amats_vesels_skaitlis(BASE_amats + 8) - amats_vesels_skaitlis(BASE_amats + 4) + 1 : amats_vesels_skaitlis(BASE_amats + 4);
            if (ievade_COUNT < 0 || ievade_COUNT > 2048) return 0;
            길이 = BASE_amats - 읽는자리 + (VALUE == 170 ? 12 + 4 * ievade_COUNT : 8 + 8 * ievade_COUNT);
        }
        if (VALUE == 196 && 읽는자리 + 1 < 끝) {
            int Word_dati = Fails[읽는자리 + 1]; 길이 = Word_dati == 132 ? 6 : (Word_dati == 21 || Word_dati == 25 || Word_dati == 54 || Word_dati == 58) ? 4 : 0;
        }
        return 길이 > 0 && 길이 <= 끝 - 읽는자리 ? 길이 : 0;
    }
    static void čeks_mērķis_VALUE(int mērķis_VALUE, int FUNCTION_VALUE) {
        if (mērķis_VALUE < metode_Sākt[FUNCTION_VALUE] || mērķis_VALUE >= metode_beigt_zvanu[FUNCTION_VALUE] || 경계[mērķis_VALUE] != FUNCTION_VALUE + 1) kļūme_VALUE("invalid branch target");
    }
    static void 클래스읽기(int klase_definīcija) {
        현재읽는종 = klase_definīcija; 읽기위치 = klase_definīcija * 16384; Izmērs = 읽기위치 + klase_definīcija_mainīt_izmērus[klase_definīcija];
        if (vesels_skaitlis() != 0xcafebabe) { kļūme_VALUE("not a class file"); return; }
        int 부판 = 짧은수(), versija_VALUE = 짧은수();
        if (versija_VALUE < 45 || versija_VALUE > 52 || 부판 != 0) { kļūme_VALUE("supported class versions: 45..52, minor 0"); return; }
        int konstante_COUNT = 짧은수(), BASE_amats = klase_definīcija * 512;
        if (konstante_COUNT < 1 || konstante_COUNT > 512) { kļūme_VALUE("constant pool limit (511)"); return; }
        for (int ievade_COUNT = 1; ievade_COUNT < konstante_COUNT && !Kļūda; ievade_COUNT++) {
            int numurs = BASE_amats + ievade_COUNT, 종류 = byte_VALUE(); konstante_tags[numurs] = 종류;
            if (종류 == 1) { konstante_SECOND_VALUE[numurs] = 짧은수(); 상가[numurs] = 읽기위치; 건너(konstante_SECOND_VALUE[numurs]); }
            else if (종류 == 3) 상가[numurs] = vesels_skaitlis();
            else if (종류 == 7 || 종류 == 8) 상가[numurs] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[numurs] = 상번호(); konstante_SECOND_VALUE[numurs] = 상번호(); }
            else kļūme_VALUE("unsupported constant type");
        }
        int atļauja_VALUE = 짧은수();
        if ((atļauja_VALUE & (0x2000 | 0x4000)) != 0) kļūme_VALUE("annotation/enum class unsupported");
        klase_definīcija_nosaukums[klase_definīcija] = klases_nosaukums_SMS(상번호());
        klase_definīcija_vecākobjekts[klase_definīcija] = klases_nosaukums_SMS(상번호());
        int interfeiss_COUNT = 짧은수(); if (interfeiss_COUNT > 16) { kļūme_VALUE("interface count limit"); return; }
        klase_interfeiss_COUNT[klase_definīcija] = interfeiss_COUNT;
        for (int Loop_INDEX = 0; Loop_INDEX < interfeiss_COUNT; Loop_INDEX++) klase_interfeiss[klase_definīcija * 16 + Loop_INDEX] = klases_nosaukums_SMS(상번호());
        int lauks_COUNT = 짧은수();
        if (lauks_COUNT > 512 - 칸수) { kļūme_VALUE("field count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < lauks_COUNT && !Kļūda; Loop_INDEX++) {
            int Fails_INDEX = 칸수++; 칸주인[Fails_INDEX] = klase_definīcija; 칸권한[Fails_INDEX] = 짧은수(); 칸이름[Fails_INDEX] = 상번호(); 칸형[Fails_INDEX] = 상번호();
            čeks_konstante(칸이름[Fails_INDEX], 1); čeks_konstante(칸형[Fails_INDEX], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[칸형[Fails_INDEX]]; int joma_CODE = 서술형(읽기위치 + konstante_SECOND_VALUE[칸형[Fails_INDEX]], false); 읽기위치 = 보존값;
            if ((칸권한[Fails_INDEX] & 8) == 0) 칸위치[Fails_INDEX] = 종칸수[klase_definīcija]++;
            int atribūts_dati = 짧은수();
            for (int iekšējais_amats = 0; iekšējais_amats < atribūts_dati && !Kļūda; iekšējais_amats++) {
                int nosaukums_konstante = 상번호(), 유효길이 = vesels_skaitlis();
                if (Word_SMS(nosaukums_konstante, "ConstantValue") && 유효길이 == 2) {
                    int dati_VALUE = 상번호();
                    if (joma_CODE == 1 && čeks_konstante(dati_VALUE, 3)) 칸값[Fails_INDEX] = 상가[dati_VALUE];
                    else if (joma_CODE == 2 && čeks_konstante(dati_VALUE, 8)) 칸값[Fails_INDEX] = konstante_SMS(상가[dati_VALUE]);
                } else 건너(유효길이);
            }
        }
        int krājums_COUNT = 짧은수();
        if (krājums_COUNT > 512 - metode_COUNT) { kļūme_VALUE("method count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < krājums_COUNT && !Kļūda; Loop_INDEX++) {
            int numurs = metode_COUNT++; metode_īpašnieks[numurs] = klase_definīcija;
            metode_piekļūt[numurs] = 짧은수(); metode_nosaukums_SMS[numurs] = 상번호(); metode_TYPE[numurs] = 상번호();
            čeks_konstante(metode_nosaukums_SMS[numurs], 1); 서술읽기(numurs);
            if ((metode_piekļūt[numurs] & 8) == 0) {
                if (metode_arg_COUNT[numurs] == 16) { kļūme_VALUE("too many instance method arguments"); return; }
                for (int Salīdzinājums_amats = metode_arg_COUNT[numurs]; Salīdzinājums_amats > 0; Salīdzinājums_amats--) metode_arg_TYPE[numurs * 16 + Salīdzinājums_amats] = metode_arg_TYPE[numurs * 16 + Salīdzinājums_amats - 1];
                metode_arg_TYPE[numurs * 16] = 2; metode_arg_COUNT[numurs]++;
            }
            if ((metode_piekļūt[numurs] & 0x100) != 0) kļūme_VALUE("user native method unsupported");
            if (Word_SMS(metode_nosaukums_SMS[numurs], "<clinit>")) 종초기화[klase_definīcija] = numurs + 1;
            for (int priekšējā_VALUE = 0; priekšējā_VALUE < numurs; priekšējā_VALUE++) if (metode_īpašnieks[priekšējā_VALUE] == klase_definīcija && 같은말(metode_nosaukums_SMS[priekšējā_VALUE], metode_nosaukums_SMS[numurs]) && 같은말(metode_TYPE[priekšējā_VALUE], metode_TYPE[numurs])) kļūme_VALUE("duplicate method");
            int atribūts_COUNT = 짧은수();
            for (int atribūts_VALUE = 0; atribūts_VALUE < atribūts_COUNT && !Kļūda; atribūts_VALUE++) {
                int Nosaukums = 상번호(), 길이 = vesels_skaitlis(), Palaist = 읽기위치;
                if (!klips(Palaist, 길이)) { kļūme_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Nosaukums, "Code")) {
                    if (metode_Sākt[numurs] != 0) kļūme_VALUE("duplicate Code attribute");
                    metode_kopa[numurs] = 짧은수(); 함수지역[numurs] = 짧은수(); int 코드길이 = vesels_skaitlis();
                    if (metode_kopa[numurs] > 128 || 함수지역[numurs] > 128 || 함수지역[numurs] < metode_arg_COUNT[numurs]
                        || 코드길이 < 1 || 코드길이 > 8192) kļūme_VALUE("method memory limits exceeded");
                    metode_Sākt[numurs] = 읽기위치; 건너(코드길이); metode_beigt_zvanu[numurs] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { kļūme_VALUE("exception table limit"); return; }
                    for (int iekšējais_amats = 0; iekšējais_amats < 잡는수; iekšējais_amats++) {
                        int kļūda_Uzziņas = 잡기수++; 잡기함수[kļūda_Uzziņas] = numurs;
                        잡기시작[kļūda_Uzziņas] = metode_Sākt[numurs] + 짧은수(); 잡기끝[kļūda_Uzziņas] = metode_Sākt[numurs] + 짧은수();
                        잡기위치[kļūda_Uzziņas] = metode_Sākt[numurs] + 짧은수(); int 부호값 = 상번호(); 잡기종[kļūda_Uzziņas] = 부호값 == 0 ? 0 : klases_nosaukums_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != Palaist + 길이) kļūme_VALUE("Code attribute size mismatch");
                } else 건너(길이);
            }
            if ((metode_piekļūt[numurs] & 0x400) != 0) continue;
            if (metode_Sākt[numurs] == 0) kļūme_VALUE("missing Code attribute");
            int 칸 = metode_Sākt[numurs];
            while (칸 < metode_beigt_zvanu[numurs] && !Kļūda) {
                int 길이 = 길이읽기(칸, metode_Sākt[numurs], metode_beigt_zvanu[numurs]);
                if (길이 == 0) { kļūme_VALUE("unsupported or truncated bytecode"); break; }
                경계[칸] = numurs + 1; 칸 += 길이;
            }
            칸 = metode_Sākt[numurs];
            while (칸 < metode_beigt_zvanu[numurs] && !Kļūda) {
                int VALUE = Fails[칸];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) čeks_mērķis_VALUE(칸 + (short)(Fails[칸 + 1] << 8 | Fails[칸 + 2]), numurs);
                if (VALUE == 200) čeks_mērķis_VALUE(칸 + amats_vesels_skaitlis(칸 + 1), numurs);
                if (VALUE == 170 || VALUE == 171) {
                    int 읽는자리 = 칸 + 1; while ((읽는자리 - metode_Sākt[numurs]) % 4 != 0) 읽는자리++;
                    čeks_mērķis_VALUE(칸 + amats_vesels_skaitlis(읽는자리), numurs);
                    int ievade_COUNT = VALUE == 170 ? amats_vesels_skaitlis(읽는자리 + 8) - amats_vesels_skaitlis(읽는자리 + 4) + 1 : amats_vesels_skaitlis(읽는자리 + 4);
                    읽는자리 += VALUE == 170 ? 12 : 8;
                    for (int iekšējais_amats = 0; iekšējais_amats < ievade_COUNT; iekšējais_amats++) čeks_mērķis_VALUE(칸 + amats_vesels_skaitlis(읽는자리 + iekšējais_amats * (VALUE == 170 ? 4 : 8) + (VALUE == 170 ? 0 : 4)), numurs);
                }
                칸 += 길이읽기(칸, metode_Sākt[numurs], metode_beigt_zvanu[numurs]);
            }
            for (int iekšējais_amats = 0; iekšējais_amats < 잡기수; iekšējais_amats++) if (잡기함수[iekšējais_amats] == numurs) {
                čeks_mērķis_VALUE(잡기시작[iekšējais_amats], numurs); čeks_mērķis_VALUE(잡기위치[iekšējais_amats], numurs);
                if (잡기끝[iekšējais_amats] != metode_beigt_zvanu[numurs]) čeks_mērķis_VALUE(잡기끝[iekšējais_amats], numurs);
                if (잡기시작[iekšējais_amats] >= 잡기끝[iekšējais_amats]) kļūme_VALUE("invalid exception range");
            }
        }
        if (!Kļūda) 속성건너();
        if (읽기위치 != Izmērs) kļūme_VALUE("extra class file data");
    }
    static int piešķirt_Krātuve(int 종류, int 길이) { return 새기억(종류, 길이); }
    static boolean objekts_VALUE(int Uzziņas, int 종류) {
        if (!객체유효(Uzziņas)) return false;
        if (kaudze_VALUE[Uzziņas] != 종류) { kļūme_VALUE("object type mismatch"); return false; }
        return true;
    }
    static int konstante_SMS(int INDEX) {
        if (!čeks_konstante(INDEX, 1)) return 0;
        if (virkne_Uzziņas[INDEX] != 0) return virkne_Uzziņas[INDEX];
        int Uzziņas = piešķirt_Krātuve(1, konstante_SECOND_VALUE[INDEX]); if (Kļūda) return 0;
        int 끝 = 상가[INDEX] + konstante_SECOND_VALUE[INDEX], numurs = 상가[INDEX], 길이 = 0;
        while (numurs < 끝 && !Kļūda) {
            int VALUE = Fails[numurs++];
            if (VALUE == 0) kļūme_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && numurs < 끝) {
                int Tālāk_krājums = Fails[numurs++];
                if ((Tālāk_krājums & 192) != 128) kļūme_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | Tālāk_krājums & 63;
                if (VALUE != 0 && VALUE < 128) kļūme_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && numurs + 1 < 끝) {
                int 가 = Fails[numurs++], SECOND_operands = Fails[numurs++];
                if ((가 & 192) != 128 || (SECOND_operands & 192) != 128) kļūme_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | SECOND_operands & 63;
                if (VALUE < 2048) kļūme_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) kļūme_VALUE("invalid modified UTF-8");
            kaudze_VALUE[Uzziņas + 2 + 길이++] = VALUE;
        }
        kaudze_VALUE[Uzziņas + 1] = 길이; virkne_Uzziņas[INDEX] = Uzziņas; return Uzziņas;
    }
    static int viesot_rakstzīme(String VALUE) {
        int Uzziņas = piešķirt_Krātuve(1, VALUE.length()); if (Kļūda) return 0;
        for (int numurs = 0; numurs < VALUE.length(); numurs++) kaudze_VALUE[Uzziņas + 2 + numurs] = VALUE.charAt(numurs);
        return Uzziņas;
    }
    static void rakstīšana_SMS(int Uzziņas) {
        if (Uzziņas == 0) { lietotājs.Rakstīt("null"); return; }
        if (!objekts_VALUE(Uzziņas, 1)) return;
        for (int numurs = 0; numurs < kaudze_VALUE[Uzziņas + 1]; numurs++) lietotājs.rakstīšana_rakstzīme_VALUE(kaudze_VALUE[Uzziņas + 2 + numurs]);
    }
    static int cipars_rakstzīme(int VALUE) {
        int Uzziņas = piešķirt_Krātuve(1, 11); if (Kļūda) return 0;
        int 길이 = 0;
        if (VALUE < 0) kaudze_VALUE[Uzziņas + 2 + 길이++] = '-'; else VALUE = -VALUE;
        int pozīcijas_indekss = 1000000000; boolean Palaist = false;
        while (pozīcijas_indekss != 0) {
            int numurs = -(VALUE / pozīcijas_indekss);
            if (numurs != 0 || Palaist || pozīcijas_indekss == 1) { kaudze_VALUE[Uzziņas + 2 + 길이++] = '0' + numurs; Palaist = true; }
            VALUE %= pozīcijas_indekss; pozīcijas_indekss /= 10;
        }
        kaudze_VALUE[Uzziņas + 1] = 길이; return Uzziņas;
    }
    static int 정수해독(int Uzziņas) {
        if (!objekts_VALUE(Uzziņas, 1)) return 0;
        int 길이 = kaudze_VALUE[Uzziņas + 1], numurs = 0, VALUE = 0; boolean 음수 = false;
        if (길이 > 0 && (kaudze_VALUE[Uzziņas + 2] == '-' || kaudze_VALUE[Uzziņas + 2] == '+')) { 음수 = kaudze_VALUE[Uzziņas + 2] == '-'; numurs++; }
        if (numurs == 길이) kļūme_VALUE("NumberFormatException");
        for (; numurs < 길이 && !Kļūda; numurs++) {
            int cipars_VALUE = kaudze_VALUE[Uzziņas + 2 + numurs] - '0';
            if (cipars_VALUE < 0 || cipars_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && cipars_VALUE > (음수 ? 8 : 7)) kļūme_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - cipars_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int TYPE_VALUE) {
        if (Kļūda) return;
        if (kadrs_INDEX < 0 || kadrs_kopa[kadrs_INDEX] >= metode_kopa[kadrs_metode[kadrs_INDEX]]) { kļūme_VALUE("operand stack overflow"); return; }
        int 칸 = kadrs_INDEX * 128 + kadrs_kopa[kadrs_INDEX]++; operands_kopa_VALUE[칸] = VALUE; operands_kopa_TYPE[칸] = TYPE_VALUE;
    }
    static int 빼기(int TYPE_VALUE) {
        if (Kļūda) return 0;
        if (kadrs_INDEX < 0 || kadrs_kopa[kadrs_INDEX] < 1) { kļūme_VALUE("operand stack underflow"); return 0; }
        int 칸 = kadrs_INDEX * 128 + --kadrs_kopa[kadrs_INDEX]; atdot_TYPE = operands_kopa_TYPE[칸];
        if (TYPE_VALUE != 0 && atdot_TYPE != TYPE_VALUE) kļūme_VALUE("operand type mismatch");
        if (atdot_TYPE == 2) aizsargāt_VALUE(operands_kopa_VALUE[칸]);
        return operands_kopa_VALUE[칸];
    }
    static void 지역읽기(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[kadrs_metode[kadrs_INDEX]] || INDEX < 0 || vietējs_TYPE[kadrs_INDEX * 128 + INDEX] != TYPE_VALUE) { kļūme_VALUE("invalid or uninitialized local"); return; }
        넣기(vietējs_VALUE[kadrs_INDEX * 128 + INDEX], TYPE_VALUE);
    }
    static void rakstīšana_vietējs(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[kadrs_metode[kadrs_INDEX]] || INDEX < 0) { kļūme_VALUE("local index out of range"); return; }
        int VALUE = 빼기(TYPE_VALUE); vietējs_VALUE[kadrs_INDEX * 128 + INDEX] = VALUE; vietējs_TYPE[kadrs_INDEX * 128 + INDEX] = TYPE_VALUE;
    }
    static int 명바() {
        int Novietojums = kadrs_amats[kadrs_INDEX];
        if (Novietojums < metode_Sākt[kadrs_metode[kadrs_INDEX]] || Novietojums >= metode_beigt_zvanu[kadrs_metode[kadrs_INDEX]]) { kļūme_VALUE("instruction pointer out of range"); return 0; }
        kadrs_amats[kadrs_INDEX]++; return Fails[Novietojums];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void pārvietot_VALUE(int Novietojums) {
        int FUNCTION_VALUE = kadrs_metode[kadrs_INDEX];
        if (Novietojums < metode_Sākt[FUNCTION_VALUE] || Novietojums >= metode_beigt_zvanu[FUNCTION_VALUE] || 경계[Novietojums] != FUNCTION_VALUE + 1) kļūme_VALUE("invalid branch target");
        else kadrs_amats[kadrs_INDEX] = Novietojums;
    }
    static void 호출(int FUNCTION_VALUE) {
        if (kadrs_INDEX % 32 == 31) { kļūme_VALUE("call stack limit (32)"); return; }
        int Tālāk_krājums = kadrs_INDEX + 1;
        for (int numurs = 0; numurs < 128; numurs++) vietējs_TYPE[Tālāk_krājums * 128 + numurs] = 0;
        for (int numurs = metode_arg_COUNT[FUNCTION_VALUE] - 1; numurs >= 0; numurs--) {
            vietējs_VALUE[Tālāk_krājums * 128 + numurs] = 빼기(metode_arg_TYPE[FUNCTION_VALUE * 16 + numurs]); vietējs_TYPE[Tālāk_krājums * 128 + numurs] = metode_arg_TYPE[FUNCTION_VALUE * 16 + numurs];
        }
        if (Kļūda) return;
        kadrs_INDEX = Tālāk_krājums; 틀초기화[kadrs_INDEX] = 0; kadrs_metode[kadrs_INDEX] = FUNCTION_VALUE; kadrs_amats[kadrs_INDEX] = metode_Sākt[FUNCTION_VALUE]; kadrs_kopa[kadrs_INDEX] = 0;
    }
    static void atdot_mērs(int TYPE_VALUE) {
        if (TYPE_VALUE != metode_atdot[kadrs_metode[kadrs_INDEX]]) { kļūme_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        if (틀초기화[kadrs_INDEX] != 0) klase_definīcija_Statuss[틀초기화[kadrs_INDEX] - 1] = 2;
        if (kadrs_bloķēt[kadrs_INDEX] != 0) { izlaist_bloķēt(kadrs_bloķēt[kadrs_INDEX]); kadrs_bloķēt[kadrs_INDEX] = 0; }
        kadrs_INDEX--; if (kadrs_INDEX >= pašreizējais_saruna * 32 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
    }
    static int[] Stream_faila_nosaukums = new int[64];
    static void Fails_Stream_CALL(int īpašnieks_VALUE, int Nosaukums, int formāts_VALUE, int Komanda) {
        boolean Izvade = Word_SMS(īpašnieks_VALUE, "java/io/FileOutputStream");
        int 종류 = Izvade ? 6 : 5;
        if (Komanda == 183 && Word_SMS(Nosaukums, "<init>")) {
            boolean 이어 = false;
            if (Izvade && Word_SMS(formāts_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(formāts_VALUE, "(Ljava/lang/String;)V")) { kļūme_VALUE("unsupported file stream constructor"); return; }
            int Fails_ievade_nosaukums = 빼기(2), Stream_VALUE = 빼기(2);
            if (!objekts_VALUE(Fails_ievade_nosaukums, 1) || !objekts_VALUE(Stream_VALUE, 종류) || Kļūda) return;
            if (kaudze_VALUE[Stream_VALUE + 3] != 0) { kļūme_VALUE("file stream already initialized"); return; }
            int 길이 = kaudze_VALUE[Fails_ievade_nosaukums + 1];
            if (길이 < 1 || 길이 > 63) { kļūme_VALUE("invalid file name length"); return; }
            for (int 칸 = 0; 칸 < 길이; 칸++) {
                int VALUE = kaudze_VALUE[Fails_ievade_nosaukums + 2 + 칸];
                if (VALUE < 1) { kļūme_VALUE("invalid file stream path"); return; }
                Stream_faila_nosaukums[칸] = VALUE;
            }
            Stream_faila_nosaukums[길이] = 0;
            int 서술자 = lietotājs.파일서술자열기(Stream_faila_nosaukums, Izvade ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { kļūme_VALUE("FileNotFoundException: file open failed"); return; }
            kaudze_VALUE[Stream_VALUE + 2] = 서술자; kaudze_VALUE[Stream_VALUE + 3] = 1;
            return;
        }
        if (Komanda != 182) { kļūme_VALUE("invalid file stream invocation"); return; }
        if ((Izvade && Word_SMS(Nosaukums, "write") || !Izvade && Word_SMS(Nosaukums, "read"))
            && (Word_SMS(formāts_VALUE, Izvade ? "([B)V" : "([B)I") || Word_SMS(formāts_VALUE, Izvade ? "([BII)V" : "([BII)I"))) {
            boolean klips_VALUE = Word_SMS(formāts_VALUE, Izvade ? "([BII)V" : "([BII)I");
            int ievade_COUNT = klips_VALUE ? 빼기(1) : 0, 시작점 = klips_VALUE ? 빼기(1) : 0, dati_ARRAY = 빼기(2), objekts_Uzziņas = 빼기(2);
            if (!objekts_VALUE(dati_ARRAY, 20) || !objekts_VALUE(objekts_Uzziņas, 종류)) return;
            if (!klips_VALUE) ievade_COUNT = kaudze_VALUE[dati_ARRAY + 1];
            if (시작점 < 0 || ievade_COUNT < 0 || 시작점 > kaudze_VALUE[dati_ARRAY + 1] - ievade_COUNT) { 예외던짐(6, "file buffer bounds"); return; }
            if (kaudze_VALUE[objekts_Uzziņas + 3] == 0 || kaudze_VALUE[objekts_Uzziņas + 2] < 0) { kļūme_VALUE("IOException: stream closed"); return; }
            int Pabeigti_COUNT = 0;
            while (Pabeigti_COUNT < ievade_COUNT && !Kļūda) {
                int 반환값 = Izvade ? lietotājs.파일한바이트쓰기(kaudze_VALUE[objekts_Uzziņas + 2], kaudze_VALUE[dati_ARRAY + 2 + 시작점 + Pabeigti_COUNT]) : lietotājs.파일한바이트읽기(kaudze_VALUE[objekts_Uzziņas + 2]);
                if (반환값 < 0) { kļūme_VALUE(Izvade ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!Izvade && 반환값 == 256) break;
                if (!Izvade) kaudze_VALUE[dati_ARRAY + 2 + 시작점 + Pabeigti_COUNT] = (byte)반환값;
                Pabeigti_COUNT++;
            }
            if (!Izvade) 넣기(ievade_COUNT != 0 && Pabeigti_COUNT == 0 ? -1 : Pabeigti_COUNT, 1);
            return;
        }
        if (Izvade && Word_SMS(Nosaukums, "flush") && Word_SMS(formāts_VALUE, "()V")) { int objekts_Uzziņas = 빼기(2); if (objekts_VALUE(objekts_Uzziņas, 종류) && kaudze_VALUE[objekts_Uzziņas + 2] < 0) kļūme_VALUE("IOException: stream closed"); return; }
        int Darbība = -1, VALUE = 0;
        if (Word_SMS(Nosaukums, "close") && Word_SMS(formāts_VALUE, "()V")) Darbība = 0;
        if (!Izvade && Word_SMS(Nosaukums, "read") && Word_SMS(formāts_VALUE, "()I")) Darbība = 1;
        if (Izvade && Word_SMS(Nosaukums, "write") && Word_SMS(formāts_VALUE, "(I)V")) { Darbība = 2; VALUE = 빼기(1); }
        if (Darbība < 0) { kļūme_VALUE("unsupported file stream method"); return; }
        int Stream_VALUE = 빼기(2);
        if (!objekts_VALUE(Stream_VALUE, 종류) || Kļūda) return;
        if (kaudze_VALUE[Stream_VALUE + 3] == 0) { kļūme_VALUE("uninitialized file stream"); return; }
        int 서술자 = kaudze_VALUE[Stream_VALUE + 2];
        if (Darbība == 0) {
            if (서술자 >= 0 && lietotājs.파일서술자닫기(서술자) < 0) kļūme_VALUE("IOException: close failed");
            kaudze_VALUE[Stream_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { kļūme_VALUE("IOException: stream closed"); return; }
        if (Darbība == 1) {
            int mērs = lietotājs.파일한바이트읽기(서술자);
            if (mērs < -1) kļūme_VALUE("IOException: read failed"); else 넣기(mērs == 256 ? -1 : mērs, 1);
        } else if (lietotājs.파일한바이트쓰기(서술자, VALUE) != 1) kļūme_VALUE("IOException: write failed");
    }
    static void CALL_metode(int INDEX, int Komanda) {
        if (INDEX <= 0 || INDEX >= konstante_tags.length || (konstante_tags[INDEX] != 10 && konstante_tags[INDEX] != 11)) { kļūme_VALUE("invalid method reference"); return; }
        int īpašnieks_VALUE = klases_nosaukums_SMS(상가[INDEX]), Nosaukums = Uzziņas_nosaukums(konstante_SECOND_VALUE[INDEX]), formāts_VALUE = Uzziņas_TYPE(konstante_SECOND_VALUE[INDEX]);
        if (Kļūda) return;
        if (기본호출(īpašnieks_VALUE, Nosaukums, formāts_VALUE, Komanda)) return;
        if (Word_SMS(īpašnieks_VALUE, "java/io/FileInputStream") || Word_SMS(īpašnieks_VALUE, "java/io/FileOutputStream")) {
            Fails_Stream_CALL(īpašnieks_VALUE, Nosaukums, formāts_VALUE, Komanda); return;
        }
        if (Komanda == 184 && Word_SMS(īpašnieks_VALUE, "java/lang/Integer") && Word_SMS(Nosaukums, "parseInt") && Word_SMS(formāts_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Komanda == 182 && Word_SMS(īpašnieks_VALUE, "java/io/PrintStream") && (Word_SMS(Nosaukums, "println") || Word_SMS(Nosaukums, "print"))) {
            int TYPE_VALUE = 0, VALUE = 0;
            if (Word_SMS(formāts_VALUE, "(I)V")) { TYPE_VALUE = 1; VALUE = 빼기(1); }
            else if (Word_SMS(formāts_VALUE, "(Z)V")) { TYPE_VALUE = 2; VALUE = 빼기(1); }
            else if (Word_SMS(formāts_VALUE, "(C)V")) { TYPE_VALUE = 3; VALUE = 빼기(1); }
            else if (Word_SMS(formāts_VALUE, "(Ljava/lang/String;)V")) { TYPE_VALUE = 4; VALUE = 빼기(2); }
            else if (!Word_SMS(formāts_VALUE, "()V") || !Word_SMS(Nosaukums, "println")) kļūme_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) kļūme_VALUE("invalid PrintStream receiver");
            if (Kļūda) return;
            if (TYPE_VALUE == 1) 자바도구.rakstīšana_numurs(VALUE);
            if (TYPE_VALUE == 2) lietotājs.Rakstīt(VALUE == 0 ? "false" : "true");
            if (TYPE_VALUE == 3) lietotājs.rakstīšana_rakstzīme_VALUE(VALUE & 65535);
            if (TYPE_VALUE == 4) rakstīšana_SMS(VALUE);
            if (Word_SMS(Nosaukums, "println")) lietotājs.rakstīšana_rakstzīme_VALUE(10);
            return;
        }
        if (Komanda == 182 && Word_SMS(īpašnieks_VALUE, "java/lang/String")) {
            if (Word_SMS(Nosaukums, "length") && Word_SMS(formāts_VALUE, "()I")) {
                int Uzziņas = 빼기(2); if (objekts_VALUE(Uzziņas, 1)) 넣기(kaudze_VALUE[Uzziņas + 1], 1); return;
            }
            if (Word_SMS(Nosaukums, "charAt") && Word_SMS(formāts_VALUE, "(I)C")) {
                int apakšraksts_VALUE = 빼기(1), Uzziņas = 빼기(2);
                if (objekts_VALUE(Uzziņas, 1)) {
                    if (apakšraksts_VALUE < 0 || apakšraksts_VALUE >= kaudze_VALUE[Uzziņas + 1]) kļūme_VALUE("StringIndexOutOfBoundsException"); else 넣기(kaudze_VALUE[Uzziņas + 2 + apakšraksts_VALUE], 1);
                }
                return;
            }
        }
        if (Word_SMS(īpašnieks_VALUE, "java/lang/StringBuilder")) {
            if (Komanda == 183 && Word_SMS(Nosaukums, "<init>") && Word_SMS(formāts_VALUE, "()V")) { objekts_VALUE(빼기(2), 4); return; }
            if (Komanda == 182 && Word_SMS(Nosaukums, "toString") && Word_SMS(formāts_VALUE, "()Ljava/lang/String;")) {
                int Uzziņas = 빼기(2); if (objekts_VALUE(Uzziņas, 4)) 넣기(kaudze_VALUE[Uzziņas + 2] == 0 ? viesot_rakstzīme("") : kaudze_VALUE[Uzziņas + 2], 2); return;
            }
            if (Komanda == 182 && Word_SMS(Nosaukums, "append")) {
                int Teksts = 0;
                if (Word_SMS(formāts_VALUE, "(I)Ljava/lang/StringBuilder;")) Teksts = cipars_rakstzīme(빼기(1));
                else if (Word_SMS(formāts_VALUE, "(Z)Ljava/lang/StringBuilder;")) Teksts = viesot_rakstzīme(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(formāts_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); Teksts = piešķirt_Krātuve(1, 1); if (!Kļūda) kaudze_VALUE[Teksts + 2] = VALUE & 65535;
                }
                else if (Word_SMS(formāts_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Teksts = 빼기(2); if (Teksts == 0) Teksts = viesot_rakstzīme("null"); }
                else { kļūme_VALUE("unsupported StringBuilder append"); return; }
                int Uzziņas = 빼기(2); if (!objekts_VALUE(Uzziņas, 4) || !objekts_VALUE(Teksts, 1)) return;
                int priekšējā_VALUE = kaudze_VALUE[Uzziņas + 2], 앞길이 = priekšējā_VALUE == 0 ? 0 : kaudze_VALUE[priekšējā_VALUE + 1], 뒤길이 = kaudze_VALUE[Teksts + 1];
                int 새글 = piešķirt_Krātuve(1, 앞길이 + 뒤길이); if (Kļūda) return;
                for (int numurs = 0; numurs < 앞길이; numurs++) kaudze_VALUE[새글 + 2 + numurs] = kaudze_VALUE[priekšējā_VALUE + 2 + numurs];
                for (int numurs = 0; numurs < 뒤길이; numurs++) kaudze_VALUE[새글 + 2 + 앞길이 + numurs] = kaudze_VALUE[Teksts + 2 + numurs];
                kaudze_VALUE[Uzziņas + 2] = 새글; 넣기(Uzziņas, 2); return;
            }
        }
        int klase_definīcija = FIND_klase_definīcija(īpašnieks_VALUE); if (klase_definīcija < 0 || Kļūda) return;
        int Fails_INDEX = FIND_metode(klase_definīcija, Nosaukums, formāts_VALUE);
        if (Fails_INDEX < 0) {
            for (int koda_punkts = klase_definīcija, ievade_COUNT = 0; koda_punkts >= 0 && ievade_COUNT < 16; ievade_COUNT++, koda_punkts = vecākobjekts_klase(koda_punkts))
                if (Word_SMS(klase_definīcija_vecākobjekts[koda_punkts], "java/lang/Thread")) { 가닥호출(Nosaukums, formāts_VALUE, Komanda); return; }
            kļūme_VALUE("NoSuchMethodError"); return;
        }
        if (((metode_piekļūt[Fails_INDEX] & 8) != 0) != (Komanda == 184)) { kļūme_VALUE("method static/instance mismatch"); return; }
        if (Komanda == 184) { if (!초기화(metode_īpašnieks[Fails_INDEX], 틀명령[kadrs_INDEX])) return; }
        else {
            int 읽는자리 = kadrs_kopa[kadrs_INDEX] - metode_arg_COUNT[Fails_INDEX];
            if (읽는자리 < 0 || operands_kopa_TYPE[kadrs_INDEX * 128 + 읽는자리] != 2) { kļūme_VALUE("invalid method receiver"); return; }
            int objekts_Uzziņas = operands_kopa_VALUE[kadrs_INDEX * 128 + 읽는자리];
            if (!객체유효(objekts_Uzziņas)) return;
            if (kaudze_VALUE[objekts_Uzziņas] < 32 || !종포함(kaudze_VALUE[objekts_Uzziņas] - 32, īpašnieks_VALUE)) { kļūme_VALUE("method receiver type mismatch"); return; }
            if (Komanda != 183) Fails_INDEX = FIND_metode(kaudze_VALUE[objekts_Uzziņas] - 32, Nosaukums, formāts_VALUE);
        }
        if (Fails_INDEX < 0 || (metode_piekļūt[Fails_INDEX] & 0x400) != 0) { kļūme_VALUE("AbstractMethodError"); return; }
        int bloķēt_Uzziņas = 0;
        if ((metode_piekļūt[Fails_INDEX] & 32) != 0) {
            if (Komanda == 184) { int koda_punkts = metode_īpašnieks[Fails_INDEX]; if (klase_bloķēt[koda_punkts] == 0) klase_bloķēt[koda_punkts] = piešķirt_Krātuve(8, 0); bloķēt_Uzziņas = klase_bloķēt[koda_punkts]; }
            else bloķēt_Uzziņas = operands_kopa_VALUE[kadrs_INDEX * 128 + kadrs_kopa[kadrs_INDEX] - metode_arg_COUNT[Fails_INDEX]];
            if (!잠금얻기(bloķēt_Uzziņas)) { if (!Kļūda) kadrs_amats[kadrs_INDEX] = 틀명령[kadrs_INDEX]; return; }
        }
        호출(Fails_INDEX); if (!Kļūda) kadrs_bloķēt[kadrs_INDEX] = bloķēt_Uzziņas;
    }
    static boolean 배열저장가능(int ARRAY_Uzziņas, int dati_VALUE) {
        if (dati_VALUE == 0 || masīva_elements[ARRAY_Uzziņas] == 0) return true;
        boolean 성공여부 = masīva_elements[ARRAY_Uzziņas] == -1 ? (dati_VALUE > 0 && dati_VALUE < kaudze_beigt_zvanu_amats && kaudze_VALUE[dati_VALUE] == 1) : 맞는객체(dati_VALUE, masīva_elements[ARRAY_Uzziņas]);
        if (!성공여부 && !Kļūda) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int 배열칸(int Uzziņas, int apakšraksts_VALUE, int TYPE_VALUE) {
        if (!objekts_VALUE(Uzziņas, TYPE_VALUE)) return 0;
        if (apakšraksts_VALUE < 0 || apakšraksts_VALUE >= kaudze_VALUE[Uzziņas + 1]) { kļūme_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return Uzziņas + 2 + apakšraksts_VALUE;
    }
    static void Izpildīt_komanda() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (Kļūda) { if (던진객체 != 0) turis_izņēmums(); if (Kļūda || kadrs_INDEX < pašreizējais_saruna * 32) break; }
            if (kadrs_INDEX < pašreizējais_saruna * 32 || mainīt_pieprasījums || --조각 == 0) { if (!SWITCH_saruna()) break; 조각 = 100; }
            if (kadrs_INDEX == 0 && klase_definīcija_Statuss[ievade_klase_definīcija] != 2 && !초기화(ievade_klase_definīcija, kadrs_amats[kadrs_INDEX])) continue;
            if (kadrs_INDEX == pašreizējais_saruna * 32 && pašreizējais_saruna != 0 && (metode_piekļūt[kadrs_metode[kadrs_INDEX]] & 32) != 0 && kadrs_bloķēt[kadrs_INDEX] == 0) {
                int objekts_Uzziņas = saruna_mērķis[pašreizējais_saruna]; if (!잠금얻기(objekts_Uzziņas)) { if (Kļūda) break; continue; } kadrs_bloķēt[kadrs_INDEX] = objekts_Uzziņas;
            }
            잠시수 = 0;
            if (--남음 == 0) { kļūme_VALUE("instruction limit (500000)"); break; }
            int Palaist = kadrs_amats[kadrs_INDEX]; 틀명령[kadrs_INDEX] = Palaist; int VALUE = 명바();
            if (Kļūda) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int numurs = metode_īpašnieks[kadrs_metode[kadrs_INDEX]] * 512 + (VALUE == 18 ? 명바() : 명짧());
                if (numurs <= 0 || numurs >= konstante_tags.length) kļūme_VALUE("invalid ldc constant");
                else if (konstante_tags[numurs] == 3) 넣기(상가[numurs], 1);
                else if (konstante_tags[numurs] == 8) 넣기(konstante_SMS(상가[numurs]), 2);
                else kļūme_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { rakstīšana_vietējs(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { rakstīšana_vietējs(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { rakstīšana_vietējs(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE >= 50 && VALUE <= 53) {
                int ievade_amats = 빼기(1), objekts_Uzziņas = 빼기(2), joma_CODE = VALUE == 46 ? 2 : VALUE == 50 ? 3 : VALUE == 51 ? 20 : VALUE == 52 ? 22 : 23;
                if (VALUE == 51 && objekts_Uzziņas > 0 && objekts_Uzziņas < kaudze_beigt_zvanu_amats && kaudze_VALUE[objekts_Uzziņas] == 21) joma_CODE = 21;
                int 읽는자리 = 배열칸(objekts_Uzziņas, ievade_amats, joma_CODE); if (!Kļūda) 넣기(kaudze_VALUE[읽는자리], VALUE == 50 ? 2 : 1); continue;
            }
            if (VALUE == 79 || VALUE >= 83 && VALUE <= 86) {
                int ievade_Uzziņas = 빼기(VALUE == 83 ? 2 : 1), ievade_amats = 빼기(1), objekts_Uzziņas = 빼기(2), joma_CODE = VALUE == 79 ? 2 : VALUE == 83 ? 3 : VALUE == 84 ? 20 : VALUE == 85 ? 22 : 23;
                if (VALUE == 84 && objekts_Uzziņas > 0 && objekts_Uzziņas < kaudze_beigt_zvanu_amats && kaudze_VALUE[objekts_Uzziņas] == 21) joma_CODE = 21;
                int 읽는자리 = 배열칸(objekts_Uzziņas, ievade_amats, joma_CODE);
                if (!Kļūda && joma_CODE == 3 && !배열저장가능(objekts_Uzziņas, ievade_Uzziņas)) continue;
                if (!Kļūda) kaudze_VALUE[읽는자리] = joma_CODE == 20 ? (byte)ievade_Uzziņas : joma_CODE == 21 ? ievade_Uzziņas & 1 : joma_CODE == 22 ? (char)ievade_Uzziņas : joma_CODE == 23 ? (short)ievade_Uzziņas : ievade_Uzziņas;
                continue;
            }
            if (VALUE >= 87 && VALUE <= 95) { 스택명령(VALUE); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int SECOND_operands = 빼기(1), 가 = 빼기(1), mērs = 0;
                if ((VALUE == 108 || VALUE == 112) && SECOND_operands == 0) { kļūme_VALUE("ArithmeticException: / by zero"); continue; }
                if (VALUE == 96) mērs = 가 + SECOND_operands;
                if (VALUE == 100) mērs = 가 - SECOND_operands;
                if (VALUE == 104) mērs = 가 * SECOND_operands;
                if (VALUE == 108) mērs = 가 / SECOND_operands;
                if (VALUE == 112) mērs = 가 % SECOND_operands;
                if (VALUE == 120) mērs = 가 << SECOND_operands;
                if (VALUE == 122) mērs = 가 >> SECOND_operands;
                if (VALUE == 124) mērs = 가 >>> SECOND_operands;
                if (VALUE == 126) mērs = 가 & SECOND_operands;
                if (VALUE == 128) mērs = 가 | SECOND_operands;
                if (VALUE == 130) mērs = 가 ^ SECOND_operands;
                넣기(mērs, 1); continue;
            }
            if (VALUE == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALUE == 132) {
                int vietējs_Tvērums = 명바(), palielinājums_solis = (byte)명바(); 지역읽기(vietējs_Tvērums, 1); 넣기(빼기(1) + palielinājums_solis, 1); rakstīšana_vietējs(vietējs_Tvērums, 1); continue;
            }
            if (VALUE >= 145 && VALUE <= 147) {
                int numurs = 빼기(1); 넣기(VALUE == 145 ? (byte)numurs : VALUE == 146 ? (char)numurs : (short)numurs, 1); continue;
            }
            if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                int mērķis_VALUE = Palaist + (short)명짧(); boolean 갈까 = VALUE == 167;
                if (VALUE >= 153 && VALUE <= 158) {
                    int numurs = 빼기(1); 갈까 = VALUE == 153 ? numurs == 0 : VALUE == 154 ? numurs != 0 : VALUE == 155 ? numurs < 0 : VALUE == 156 ? numurs >= 0 : VALUE == 157 ? numurs > 0 : numurs <= 0;
                } else if (VALUE >= 159 && VALUE <= 166) {
                    int SECOND_operands = 빼기(VALUE >= 165 ? 2 : 1), 가 = 빼기(VALUE >= 165 ? 2 : 1);
                    갈까 = VALUE == 159 || VALUE == 165 ? 가 == SECOND_operands : VALUE == 160 || VALUE == 166 ? 가 != SECOND_operands : VALUE == 161 ? 가 < SECOND_operands : VALUE == 162 ? 가 >= SECOND_operands : VALUE == 163 ? 가 > SECOND_operands : 가 <= SECOND_operands;
                } else if (VALUE == 198 || VALUE == 199) { int numurs = 빼기(2); 갈까 = VALUE == 198 ? numurs == 0 : numurs != 0; }
                if (갈까) pārvietot_VALUE(mērķis_VALUE); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { atdot_mērs(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE >= 178 && VALUE <= 181) { 필드호출(명상수(), VALUE, Palaist); continue; }
            if (VALUE >= 182 && VALUE <= 185) {
                int 부호값 = 명상수();
                if (VALUE == 185) { int kopsumma_COUNT = 명바(); if (kopsumma_COUNT == 0 || 명바() != 0) { kļūme_VALUE("invalid invokeinterface operands"); continue; } }
                CALL_metode(부호값, VALUE); continue;
            }
            if (VALUE == 187) { 새객체(klases_nosaukums_SMS(명상수()), Palaist); continue; }
            if (VALUE == 188 || VALUE == 189) {
                int joma_CODE = 3, komponents = 0;
                if (VALUE == 188) { int 임시값 = 명바(); joma_CODE = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else komponents = klases_nosaukums_SMS(명상수());
                if (joma_CODE == 0) { kļūme_VALUE("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), objekts_Uzziņas = piešķirt_Krātuve(joma_CODE, 유효길이); if (!Kļūda) masīva_elements[objekts_Uzziņas] = komponents; 넣기(objekts_Uzziņas, 2); continue;
            }
            if (VALUE == 190) {
                int objekts_Uzziņas = 빼기(2);
                if (객체유효(objekts_Uzziņas)) { int Salīdzinājums_amats = kaudze_VALUE[objekts_Uzziņas]; if (Salīdzinājums_amats != 2 && Salīdzinājums_amats != 3 && (Salīdzinājums_amats < 20 || Salīdzinājums_amats > 23)) kļūme_VALUE("not an array"); else 넣기(kaudze_VALUE[objekts_Uzziņas + 1], 1); }
                continue;
            }
            if (VALUE == 191) {
                int objekts_Uzziņas = 빼기(2); if (객체유효(objekts_Uzziņas)) { if (kaudze_VALUE[objekts_Uzziņas] != 9) kļūme_VALUE("athrow requires supported Throwable"); else { 던진객체 = objekts_Uzziņas; Kļūda = true; } }
                continue;
            }
            if (VALUE == 192 || VALUE == 193) {
                int nosaukums_konstante = klases_nosaukums_SMS(명상수()), objekts_Uzziņas = 빼기(2); boolean MATCH = 맞는객체(objekts_Uzziņas, nosaukums_konstante);
                if (VALUE == 193) 넣기(objekts_Uzziņas != 0 && MATCH ? 1 : 0, 1);
                else { if (!MATCH && !Kļūda) kļūme_VALUE("ClassCastException"); 넣기(objekts_Uzziņas, 2); }
                continue;
            }
            if (VALUE == 170 || VALUE == 171) {
                int 읽는자리 = Palaist + 1, Fails_INDEX = kadrs_metode[kadrs_INDEX], Atslēga_Uzziņas = 빼기(1);
                while ((읽는자리 - metode_Sākt[Fails_INDEX]) % 4 != 0) 읽는자리++;
                int mērķis_adrese = amats_vesels_skaitlis(읽는자리);
                if (VALUE == 170) { int 낮은값 = amats_vesels_skaitlis(읽는자리 + 4), 높은값 = amats_vesels_skaitlis(읽는자리 + 8); if (Atslēga_Uzziņas >= 낮은값 && Atslēga_Uzziņas <= 높은값) mērķis_adrese = amats_vesels_skaitlis(읽는자리 + 12 + (Atslēga_Uzziņas - 낮은값) * 4); }
                else { int kopsumma_COUNT = amats_vesels_skaitlis(읽는자리 + 4); for (int Loop_INDEX = 0; Loop_INDEX < kopsumma_COUNT; Loop_INDEX++) if (amats_vesels_skaitlis(읽는자리 + 8 + Loop_INDEX * 8) == Atslēga_Uzziņas) mērķis_adrese = amats_vesels_skaitlis(읽는자리 + 12 + Loop_INDEX * 8); }
                pārvietot_VALUE(Palaist + mērķis_adrese); continue;
            }
            if (VALUE == 200) { pārvietot_VALUE(Palaist + amats_vesels_skaitlis(Palaist + 1)); continue; }
            if (VALUE == 194 || VALUE == 195) {
                int objekts_Uzziņas = 빼기(2);
                if (VALUE == 195) izlaist_bloķēt(objekts_Uzziņas);
                else if (!잠금얻기(objekts_Uzziņas) && !Kļūda) { 넣기(objekts_Uzziņas, 2); kadrs_amats[kadrs_INDEX] = Palaist; }
                continue;
            }
            if (VALUE == 196) {
                int komanda_CODE = 명바(), ievade_amats = 명짧();
                if (komanda_CODE == 21 || komanda_CODE == 25) 지역읽기(ievade_amats, komanda_CODE == 21 ? 1 : 2);
                else if (komanda_CODE == 54 || komanda_CODE == 58) rakstīšana_vietējs(ievade_amats, komanda_CODE == 54 ? 1 : 2);
                else if (komanda_CODE == 132) { int DELTA_VALUE = (short)명짧(); 지역읽기(ievade_amats, 1); 넣기(빼기(1) + DELTA_VALUE, 1); rakstīšana_vietējs(ievade_amats, 1); }
                else kļūme_VALUE("unsupported wide opcode");
                continue;
            }
            kļūme_VALUE("unsupported bytecode");
        }
    }
    static int FIND_klase_definīcija(int Nosaukums) {
        for (int Loop_INDEX = 0; Loop_INDEX < klase_definīcija_COUNT; Loop_INDEX++) if (klase_definīcija_nosaukums[Loop_INDEX] != 0 && 같은말(klase_definīcija_nosaukums[Loop_INDEX], Nosaukums)) return Loop_INDEX;
        return ielāde_klase_definīcija(konstante_SMS(Nosaukums));
    }
    static int ielāde_klase_definīcija(int nosaukums_virkne) {
        if (!objekts_VALUE(nosaukums_virkne, 1)) return -1;
        int 길이 = kaudze_VALUE[nosaukums_virkne + 1];
        if (길이 < 1 || 길이 > 505 || klase_definīcija_COUNT == 16) { kļūme_VALUE("class name/count limit"); return -1; }
        for (int Loop_INDEX = 0; Loop_INDEX < 길이; Loop_INDEX++) { int koda_punkts = kaudze_VALUE[nosaukums_virkne + 2 + Loop_INDEX]; faila_nosaukums_SMS[Loop_INDEX] = koda_punkts == '/' ? '.' : koda_punkts; }
        faila_nosaukums_SMS[길이] = '.'; faila_nosaukums_SMS[길이 + 1] = 'c'; faila_nosaukums_SMS[길이 + 2] = 'l'; faila_nosaukums_SMS[길이 + 3] = 'a'; faila_nosaukums_SMS[길이 + 4] = 's'; faila_nosaukums_SMS[길이 + 5] = 's'; faila_nosaukums_SMS[길이 + 6] = 0;
        int Izmērs = lietotājs.파일읽기(faila_nosaukums_SMS, pagaidu_fails);
        if (Izmērs < 0) { kļūme_VALUE("ClassNotFoundException"); return -1; }
        int klase_definīcija = klase_definīcija_COUNT++; klase_definīcija_mainīt_izmērus[klase_definīcija] = Izmērs;
        for (int Loop_INDEX = 0; Loop_INDEX < Izmērs; Loop_INDEX++) Fails[klase_definīcija * 16384 + Loop_INDEX] = pagaidu_fails[Loop_INDEX];
        클래스읽기(klase_definīcija); if (Kļūda) return -1;
        int faktisks_dati = konstante_SMS(klase_definīcija_nosaukums[klase_definīcija]);
        if (!글같음(faktisks_dati, nosaukums_virkne, true)) { kļūme_VALUE("class name does not match file"); return -1; }
        int vecākobjekts_VALUE = klase_definīcija_vecākobjekts[klase_definīcija];
        if (vecākobjekts_VALUE != 0 && !Word_SMS(vecākobjekts_VALUE, "java/lang/Object") && !Word_SMS(vecākobjekts_VALUE, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 mēģināt_vēlreiz_VALUE 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = FIND_klase_definīcija(vecākobjekts_VALUE);
            if (Kļūda || 위 < 0) return -1;
            int 읽는자리 = 위, posms_COUNT = 0;
            while (읽는자리 >= 0 && posms_COUNT++ < 16) {
                if (읽는자리 == klase_definīcija) { kļūme_VALUE("cyclic inheritance"); return -1; }
                읽는자리 = vecākobjekts_klase(읽는자리);
            }
            int 시작변위 = 종칸수[위];
            for (int Fails_INDEX = 0; Fails_INDEX < 칸수; Fails_INDEX++) if (칸주인[Fails_INDEX] == klase_definīcija && (칸권한[Fails_INDEX] & 8) == 0) 칸위치[Fails_INDEX] += 시작변위;
            종칸수[klase_definīcija] += 시작변위;
        }
        return klase_definīcija;
    }
    static int vecākobjekts_klase(int klase_definīcija) {
        int Nosaukums = klase_definīcija_vecākobjekts[klase_definīcija];
        for (int Loop_INDEX = 0; Loop_INDEX < klase_definīcija_COUNT; Loop_INDEX++) if (Nosaukums != 0 && klase_definīcija_nosaukums[Loop_INDEX] != 0 && 같은말(klase_definīcija_nosaukums[Loop_INDEX], Nosaukums)) return Loop_INDEX;
        return -1;
    }
    static int FIND_metode(int klase_definīcija, int Nosaukums, int formāts_VALUE) {
        for (int 깊이 = 0; klase_definīcija >= 0 && 깊이 < 16; 깊이++, klase_definīcija = vecākobjekts_klase(klase_definīcija)) {
            for (int Loop_INDEX = 0; Loop_INDEX < metode_COUNT; Loop_INDEX++) if (metode_īpašnieks[Loop_INDEX] == klase_definīcija && 같은말(metode_nosaukums_SMS[Loop_INDEX], Nosaukums) && 같은말(metode_TYPE[Loop_INDEX], formāts_VALUE)) return Loop_INDEX;
        }
        return -1;
    }
    static int nosaukums_metode(int klase_definīcija, String Nosaukums, String formāts_VALUE) {
        for (int 깊이 = 0; klase_definīcija >= 0 && 깊이 < 16; 깊이++, klase_definīcija = vecākobjekts_klase(klase_definīcija))
            for (int Loop_INDEX = 0; Loop_INDEX < metode_COUNT; Loop_INDEX++) if (metode_īpašnieks[Loop_INDEX] == klase_definīcija && Word_SMS(metode_nosaukums_SMS[Loop_INDEX], Nosaukums) && Word_SMS(metode_TYPE[Loop_INDEX], formāts_VALUE)) return Loop_INDEX;
        return -1;
    }
    static int 형종류(int Nosaukums) { return Fails[상가[Nosaukums]] == 'L' || Fails[상가[Nosaukums]] == '[' ? 2 : 1; }
    static boolean 초기화(int klase_definīcija, int komanda_Sākt) {
        if (klase_definīcija < 0 || Kļūda) return false;
        if (klase_definīcija_Statuss[klase_definīcija] == 3) { kļūme_VALUE("NoClassDefFoundError: initialization failed"); return false; }
        if (klase_definīcija_Statuss[klase_definīcija] == 1 && klase_saruna[klase_definīcija] != pašreizējais_saruna) { kadrs_amats[kadrs_INDEX] = komanda_Sākt; mainīt_pieprasījums = true; return false; }
        if (klase_definīcija_Statuss[klase_definīcija] != 0) return true;
        int 위 = vecākobjekts_klase(klase_definīcija);
        if (위 >= 0 && !초기화(위, komanda_Sākt)) return false;
        klase_definīcija_Statuss[klase_definīcija] = 1; klase_saruna[klase_definīcija] = pašreizējais_saruna;
        if (종초기화[klase_definīcija] != 0) {
            kadrs_amats[kadrs_INDEX] = komanda_Sākt;
            호출(종초기화[klase_definīcija] - 1); if (!Kļūda) 틀초기화[kadrs_INDEX] = klase_definīcija + 1;
            return false;
        }
        klase_definīcija_Statuss[klase_definīcija] = 2; return true;
    }
    static void 필드호출(int INDEX, int Komanda, int Palaist) {
        if (!čeks_konstante(INDEX, 9)) return;
        int īpašnieks_VALUE = klases_nosaukums_SMS(상가[INDEX]), Nosaukums = Uzziņas_nosaukums(konstante_SECOND_VALUE[INDEX]), formāts_VALUE = Uzziņas_TYPE(konstante_SECOND_VALUE[INDEX]);
        if (Word_SMS(īpašnieks_VALUE, "java/lang/System") && (Word_SMS(Nosaukums, "out") || Word_SMS(Nosaukums, "err")) && Word_SMS(formāts_VALUE, "Ljava/io/PrintStream;") && Komanda == 178) { 넣기(-1, 2); return; }
        int klase_definīcija = FIND_klase_definīcija(īpašnieks_VALUE); if (klase_definīcija < 0 || Kļūda) return;
        int 찾음 = -1;
        for (int 읽는자리 = klase_definīcija, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = vecākobjekts_klase(읽는자리))
            for (int Fails_INDEX = 0; Fails_INDEX < 칸수; Fails_INDEX++) if (칸주인[Fails_INDEX] == 읽는자리 && 같은말(칸이름[Fails_INDEX], Nosaukums) && 같은말(칸형[Fails_INDEX], formāts_VALUE)) 찾음 = Fails_INDEX;
        if (찾음 < 0) { kļūme_VALUE("NoSuchFieldError"); return; }
        boolean 정적 = Komanda == 178 || Komanda == 179;
        if (정적 != ((칸권한[찾음] & 8) != 0)) { kļūme_VALUE("field static/instance mismatch"); return; }
        if (정적 && !초기화(칸주인[찾음], Palaist)) return;
        int TYPE_VALUE = 형종류(formāts_VALUE), VALUE = 0;
        if (Komanda == 179 || Komanda == 181) VALUE = 빼기(TYPE_VALUE);
        if (정적) { if (Komanda == 178) 넣기(칸값[찾음], TYPE_VALUE); else if (!Kļūda) 칸값[찾음] = VALUE; return; }
        int objekts_Uzziņas = 빼기(2);
        if (!객체유효(objekts_Uzziņas)) return;
        if (kaudze_VALUE[objekts_Uzziņas] < 32 || !종포함(kaudze_VALUE[objekts_Uzziņas] - 32, īpašnieks_VALUE)) { kļūme_VALUE("field receiver type mismatch"); return; }
        int 보관칸 = objekts_Uzziņas + 2 + 칸위치[찾음];
        if (Komanda == 180) 넣기(kaudze_VALUE[보관칸], TYPE_VALUE);
        else if (!Kļūda) { kaudze_VALUE[보관칸] = VALUE; kaudze_Uzziņas[보관칸] = TYPE_VALUE == 2 ? 1 : 0; }
    }
    static boolean 종포함(int klase_definīcija, int Nosaukums) {
        for (int 중첩깊이 = 0; klase_definīcija >= 0 && 중첩깊이 < 16; 중첩깊이++, klase_definīcija = vecākobjekts_klase(klase_definīcija)) {
            if (같은말(klase_definīcija_nosaukums[klase_definīcija], Nosaukums) || (klase_definīcija_vecākobjekts[klase_definīcija] != 0 && 같은말(klase_definīcija_vecākobjekts[klase_definīcija], Nosaukums))) return true;
            for (int iekšējais_amats = 0; iekšējais_amats < klase_interfeiss_COUNT[klase_definīcija]; iekšējais_amats++) if (같은말(klase_interfeiss[klase_definīcija * 16 + iekšējais_amats], Nosaukums)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int byte_dati, boolean CEĻŠ) {
        if (첫값 == byte_dati) return true;
        if (첫값 <= 0 || byte_dati <= 0 || kaudze_VALUE[첫값] != 1 || kaudze_VALUE[byte_dati] != 1 || kaudze_VALUE[첫값 + 1] != kaudze_VALUE[byte_dati + 1]) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < kaudze_VALUE[첫값 + 1]; Loop_INDEX++) {
            int x_koordināta = kaudze_VALUE[첫값 + 2 + Loop_INDEX], 세로좌표 = kaudze_VALUE[byte_dati + 2 + Loop_INDEX];
            if (CEĻŠ) { if (x_koordināta == '.') x_koordināta = '/'; if (세로좌표 == '.') 세로좌표 = '/'; }
            if (x_koordināta != 세로좌표) return false;
        }
        return true;
    }
    static boolean 객체유효(int objekts_Uzziņas) {
        if (objekts_Uzziņas == 0) { kļūme_VALUE("NullPointerException"); return false; }
        if (objekts_Uzziņas < 1 || objekts_Uzziņas >= kaudze_beigt_zvanu_amats || 힙폭[objekts_Uzziņas] < 2 || kaudze_VALUE[objekts_Uzziņas] == 0) { kļūme_VALUE("invalid object reference"); return false; }
        return true;
    }
    static void aizsargāt_VALUE(int objekts_Uzziņas) {
        if (objekts_Uzziņas > 0 && objekts_Uzziņas < kaudze_beigt_zvanu_amats && 힙폭[objekts_Uzziņas] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = objekts_Uzziņas;
    }
    static void rādīt_VALUE(int objekts_Uzziņas) {
        if (objekts_Uzziņas > 0 && objekts_Uzziņas < kaudze_beigt_zvanu_amats && 힙폭[objekts_Uzziņas] >= 2 && kaudze_VALUE[objekts_Uzziņas] != 0 && 힙표시[objekts_Uzziņas] == 0) {
            힙표시[objekts_Uzziņas] = 1; 표시대기[rādīt_COUNT++] = objekts_Uzziņas;
        }
    }
    static void 수거() {
        rādīt_COUNT = 0; kopums_COUNT++;
        for (int čeks_amats = 1; čeks_amats < kaudze_beigt_zvanu_amats; čeks_amats += 힙폭[čeks_amats]) 힙표시[čeks_amats] = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < virkne_Uzziņas.length; Loop_INDEX++) rādīt_VALUE(virkne_Uzziņas[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 칸수; Loop_INDEX++) if ((칸권한[Loop_INDEX] & 8) != 0 && 형종류(칸형[Loop_INDEX]) == 2) rādīt_VALUE(칸값[Loop_INDEX]);
        for (int 임시값 = 0; 임시값 < saruna_COUNT; 임시값++) {
            rādīt_VALUE(saruna_objekts[임시값]); rādīt_VALUE(saruna_mērķis[임시값]);
            int 꼭대기자리 = 임시값 == pašreizējais_saruna ? kadrs_INDEX : saruna_kadrs[임시값];
            for (int Fails_INDEX = 임시값 * 32; Fails_INDEX <= 꼭대기자리; Fails_INDEX++) {
                for (int iekšējais_amats = 0; iekšējais_amats < 함수지역[kadrs_metode[Fails_INDEX]]; iekšējais_amats++) if (vietējs_TYPE[Fails_INDEX * 128 + iekšējais_amats] == 2) rādīt_VALUE(vietējs_VALUE[Fails_INDEX * 128 + iekšējais_amats]);
                for (int iekšējais_amats = 0; iekšējais_amats < kadrs_kopa[Fails_INDEX]; iekšējais_amats++) if (operands_kopa_TYPE[Fails_INDEX * 128 + iekšējais_amats] == 2) rādīt_VALUE(operands_kopa_VALUE[Fails_INDEX * 128 + iekšējais_amats]);
            }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 화면참조.length; Loop_INDEX++) rādīt_VALUE(화면참조[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 나중수; Loop_INDEX++) rādīt_VALUE(나중실행[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Store_vesels_skaitlis.length; Loop_INDEX++) rādīt_VALUE(Store_vesels_skaitlis[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < klase_definīcija_COUNT; Loop_INDEX++) rādīt_VALUE(klase_bloķēt[Loop_INDEX]);
        for (int čeks_amats = 1; čeks_amats < kaudze_beigt_zvanu_amats; čeks_amats += 힙폭[čeks_amats]) if (잠금깊이[čeks_amats] > 0) rādīt_VALUE(čeks_amats);
        rādīt_VALUE(던진객체);
        for (int Loop_INDEX = 0; Loop_INDEX < 잠시수; Loop_INDEX++) rādīt_VALUE(잠시참조[Loop_INDEX]);
        while (rādīt_COUNT > 0) {
            int objekts_Uzziņas = 표시대기[--rādīt_COUNT], joma_CODE = kaudze_VALUE[objekts_Uzziņas];
            for (int Loop_INDEX = objekts_Uzziņas + 2; Loop_INDEX < objekts_Uzziņas + 힙폭[objekts_Uzziņas]; Loop_INDEX++) if (joma_CODE == 3 || joma_CODE == 4 || kaudze_Uzziņas[Loop_INDEX] != 0) rādīt_VALUE(kaudze_VALUE[Loop_INDEX]);
        }
        for (int čeks_amats = 1; čeks_amats < kaudze_beigt_zvanu_amats; čeks_amats += 힙폭[čeks_amats]) if (힙표시[čeks_amats] == 0) kaudze_VALUE[čeks_amats] = 0;
        for (int čeks_amats = 1; čeks_amats < kaudze_beigt_zvanu_amats; čeks_amats += 힙폭[čeks_amats]) if (kaudze_VALUE[čeks_amats] == 0) {
            while (čeks_amats + 힙폭[čeks_amats] < kaudze_beigt_zvanu_amats && kaudze_VALUE[čeks_amats + 힙폭[čeks_amats]] == 0) { int Tālāk_amats = čeks_amats + 힙폭[čeks_amats]; 힙폭[čeks_amats] += 힙폭[Tālāk_amats]; 힙폭[Tālāk_amats] = 0; }
            if (čeks_amats + 힙폭[čeks_amats] == kaudze_beigt_zvanu_amats) { kaudze_beigt_zvanu_amats = čeks_amats; break; }
        }
    }
    static int 새기억(int 종류, int 길이) {
        if (길이 < 0) { kļūme_VALUE("NegativeArraySizeException"); return 0; }
        if (길이 > kaudze_VALUE.length - 3) { kļūme_VALUE("object heap exhausted"); return 0; }
        int 필요수 = 길이 + 2, objekts_Uzziņas = 0;
        if (필요수 <= kaudze_VALUE.length - kaudze_beigt_zvanu_amats) { objekts_Uzziņas = kaudze_beigt_zvanu_amats; kaudze_beigt_zvanu_amats += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < kaudze_beigt_zvanu_amats; 읽는자리 += 힙폭[읽는자리]) if (kaudze_VALUE[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { objekts_Uzziņas = 읽는자리; break; }
            if (objekts_Uzziņas != 0) {
                int 남은길이 = 힙폭[objekts_Uzziņas] - 필요수;
                if (남은길이 >= 2) { 힙폭[objekts_Uzziņas + 필요수] = 남은길이; kaudze_VALUE[objekts_Uzziņas + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= kaudze_VALUE.length - kaudze_beigt_zvanu_amats) { objekts_Uzziņas = kaudze_beigt_zvanu_amats; kaudze_beigt_zvanu_amats += 필요수; }
        }
        if (objekts_Uzziņas == 0) { kļūme_VALUE("object heap exhausted"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < 필요수; Loop_INDEX++) { kaudze_VALUE[objekts_Uzziņas + Loop_INDEX] = 0; kaudze_Uzziņas[objekts_Uzziņas + Loop_INDEX] = 0; 힙폭[objekts_Uzziņas + Loop_INDEX] = 0; }
        masīva_elements[objekts_Uzziņas] = 0;
        힙폭[objekts_Uzziņas] = 필요수; kaudze_VALUE[objekts_Uzziņas] = 종류; kaudze_VALUE[objekts_Uzziņas + 1] = 길이; aizsargāt_VALUE(objekts_Uzziņas); return objekts_Uzziņas;
    }
    static int izņēmums_klase(String nosaukums_konstante) {
        if (자바도구.같음(nosaukums_konstante, "java/lang/Throwable")) return 1;
        if (자바도구.같음(nosaukums_konstante, "java/lang/Exception")) return 2;
        if (자바도구.같음(nosaukums_konstante, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(nosaukums_konstante, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(nosaukums_konstante, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(nosaukums_konstante, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(nosaukums_konstante, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(nosaukums_konstante, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(nosaukums_konstante, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(nosaukums_konstante, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(nosaukums_konstante, "java/io/IOException")) return 11;
        if (자바도구.같음(nosaukums_konstante, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(nosaukums_konstante, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(nosaukums_konstante, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(nosaukums_konstante, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int izņēmums_konstante(int Nosaukums) {
        for (int Loop_INDEX = 1; Loop_INDEX <= 41; Loop_INDEX++) if (Word_SMS(Nosaukums, izņēmums_nosaukums(Loop_INDEX))) return Loop_INDEX;
        return 0;
    }
    static String izņēmums_nosaukums(int konts_VALUE) {
        if (konts_VALUE == 40) return "java/lang/InterruptedException";
        if (konts_VALUE == 41) return "Latviešu/savs/대기중단예외";
        if (konts_VALUE == 39) return "java/net/SocketException";
        if (konts_VALUE == 20) return "Latviešu/savs/izņēmums";
        if (konts_VALUE == 21) return "Latviešu/savs/실행예외";
        if (konts_VALUE == 22) return "Latviešu/savs/ievadizvade_izņēmums";
        if (konts_VALUE == 23) return "Latviešu/savs/pagaidi_NOILGUMS_izņēmums";
        if (konts_VALUE == 24) return "Latviešu/savs/adrese_LOOKUP_izņēmums";
        if (konts_VALUE == 25) return "Latviešu/savs/파일없음예외";
        if (konts_VALUE == 26) return "Latviešu/savs/통신예외";
        if (konts_VALUE == 27) return "Latviešu/savs/nederīgs_arg_izņēmums";
        if (konts_VALUE == 28) return "Latviešu/savs/numurs_formāts_kļūme";
        if (konts_VALUE == 29) return "Latviešu/savs/범위예외";
        if (konts_VALUE == 30) return "Latviešu/savs/배열범위예외";
        if (konts_VALUE == 31) return "Latviešu/savs/문자열범위예외";
        if (konts_VALUE == 32) return "Latviešu/savs/NULL_Uzziņas_izņēmums";
        if (konts_VALUE == 33) return "Latviešu/savs/산술예외";
        if (konts_VALUE == 34) return "Latviešu/savs/Statuss_izņēmums";
        if (konts_VALUE == 35) return "Latviešu/savs/TYPE_atskaņot_izņēmums";
        if (konts_VALUE == 36) return "Latviešu/savs/음수배열크기예외";
        if (konts_VALUE == 37) return "Latviešu/savs/ARRAY_Store_kļūme";
        if (konts_VALUE == 38) return "Latviešu/savs/saruna_Statuss_izņēmums";
        if (konts_VALUE == 1) return "java/lang/Throwable"; if (konts_VALUE == 2) return "java/lang/Exception";
        if (konts_VALUE == 3) return "java/lang/RuntimeException"; if (konts_VALUE == 4) return "java/lang/ArithmeticException";
        if (konts_VALUE == 5) return "java/lang/NullPointerException"; if (konts_VALUE == 6) return "java/lang/IndexOutOfBoundsException";
        if (konts_VALUE == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (konts_VALUE == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (konts_VALUE == 9) return "java/lang/IllegalArgumentException"; if (konts_VALUE == 10) return "java/lang/NumberFormatException";
        if (konts_VALUE == 11) return "java/io/IOException"; if (konts_VALUE == 12) return "java/io/FileNotFoundException";
        if (konts_VALUE == 17) return "java/lang/ArrayStoreException";
        if (konts_VALUE == 18) return "java/net/UnknownHostException";
        if (konts_VALUE == 19) return "java/net/SocketTimeoutException";
        if (konts_VALUE == 16) return "java/lang/IllegalThreadStateException";
        if (konts_VALUE == 13) return "java/lang/IllegalStateException"; if (konts_VALUE == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int izņēmums_vecākobjekts(int konts_VALUE) {
        if (konts_VALUE == 40) return 2;
        if (konts_VALUE == 41) return 40;
        if (konts_VALUE == 39) return 11;
        if (konts_VALUE == 1) return 0;
        if (konts_VALUE == 2) return 1;
        if (konts_VALUE == 3) return 2;
        if (konts_VALUE == 4) return 3;
        if (konts_VALUE == 5) return 3;
        if (konts_VALUE == 6) return 3;
        if (konts_VALUE == 7) return 6;
        if (konts_VALUE == 8) return 6;
        if (konts_VALUE == 9) return 3;
        if (konts_VALUE == 10) return 9;
        if (konts_VALUE == 11) return 2;
        if (konts_VALUE == 12) return 11;
        if (konts_VALUE == 13) return 3;
        if (konts_VALUE == 14) return 3;
        if (konts_VALUE == 15) return 3;
        if (konts_VALUE == 16) return 9;
        if (konts_VALUE == 17) return 3;
        if (konts_VALUE == 18) return 11;
        if (konts_VALUE == 19) return 11;
        if (konts_VALUE == 20) return 2;
        if (konts_VALUE == 21) return 3;
        if (konts_VALUE == 22) return 11;
        if (konts_VALUE == 23) return 22;
        if (konts_VALUE == 24) return 22;
        if (konts_VALUE == 25) return 22;
        if (konts_VALUE == 26) return 22;
        if (konts_VALUE == 27) return 9;
        if (konts_VALUE == 28) return 27;
        if (konts_VALUE == 29) return 6;
        if (konts_VALUE == 30) return 29;
        if (konts_VALUE == 31) return 29;
        if (konts_VALUE == 32) return 5;
        if (konts_VALUE == 33) return 4;
        if (konts_VALUE == 34) return 13;
        if (konts_VALUE == 35) return 14;
        if (konts_VALUE == 36) return 15;
        if (konts_VALUE == 37) return 17;
        if (konts_VALUE == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int faktiskā_vērtība, int 요구값) {
        for (int 깊이 = 0; faktiskā_vērtība != 0 && 깊이 < 16; 깊이++, faktiskā_vērtība = izņēmums_vecākobjekts(faktiskā_vērtība))
            if (faktiskā_vērtība == 요구값) return true;
        return false;
    }
    static void 예외던짐(int konts_VALUE, String fails_Lasi_mani_Uzziņas) {
        int objekts_Uzziņas = 새기억(9, 2); if (Kļūda) return;
        kaudze_VALUE[objekts_Uzziņas + 2] = konts_VALUE; kaudze_VALUE[objekts_Uzziņas + 3] = viesot_rakstzīme(fails_Lasi_mani_Uzziņas); kaudze_Uzziņas[objekts_Uzziņas + 3] = 1;
        던진객체 = objekts_Uzziņas; Kļūda = true;
    }
    static boolean 맞는객체(int objekts_Uzziņas, int Nosaukums) {
        if (objekts_Uzziņas == 0) return true;
        if (!객체유효(objekts_Uzziņas)) return false;
        int joma_CODE = kaudze_VALUE[objekts_Uzziņas];
        if (Word_SMS(Nosaukums, "java/lang/Object")) return true;
        if (joma_CODE >= 32) return 종포함(joma_CODE - 32, Nosaukums);
        if (joma_CODE == 9) { int mērķis_adrese = izņēmums_konstante(Nosaukums); return mērķis_adrese != 0 && 예외포함(kaudze_VALUE[objekts_Uzziņas + 2], mērķis_adrese); }
        if (joma_CODE == 1) return Word_SMS(Nosaukums, "java/lang/String") || Word_SMS(Nosaukums, "java/lang/CharSequence");
        if (joma_CODE == 4) return Word_SMS(Nosaukums, "java/lang/StringBuilder") || Word_SMS(Nosaukums, "java/lang/CharSequence");
        if (joma_CODE == 10) return Word_SMS(Nosaukums, "java/util/ArrayList") || Word_SMS(Nosaukums, "java/util/List");
        if (joma_CODE == 11) return Word_SMS(Nosaukums, "java/util/HashMap") || Word_SMS(Nosaukums, "java/util/Map");
        if (joma_CODE == 12) return Word_SMS(Nosaukums, "java/lang/Integer") || Word_SMS(Nosaukums, "java/lang/Number");
        if (joma_CODE >= 24 && joma_CODE <= 28 && kaudze_VALUE[objekts_Uzziņas + 13] != 0) return 한국어화면종(Nosaukums) == joma_CODE || Word_SMS(Nosaukums, "Latviešu/savs/화면구성요소");
        if (joma_CODE >= 24 && joma_CODE <= 28) return (한국어화면종(Nosaukums) == 0 && 화면종(Nosaukums) == joma_CODE) || Word_SMS(Nosaukums, "java/awt/Component") || Word_SMS(Nosaukums, "java/awt/Container") || Word_SMS(Nosaukums, "javax/swing/JComponent");
        if (joma_CODE == 29) return Word_SMS(Nosaukums, kaudze_VALUE[objekts_Uzziņas + 3] != 0 ? "Latviešu/savs/darbība_informēšana" : "java/awt/event/ActionEvent");
        if (joma_CODE == 30) return Word_SMS(Nosaukums, "java/awt/FlowLayout") || Word_SMS(Nosaukums, "java/awt/LayoutManager");
        if (joma_CODE == 17) return Word_SMS(Nosaukums, "java/net/Socket");
        if (joma_CODE == 18) return Word_SMS(Nosaukums, "java/net/ServerSocket");
        if (joma_CODE == 19) return Word_SMS(Nosaukums, kaudze_VALUE[objekts_Uzziņas + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (joma_CODE == 14) return Word_SMS(Nosaukums, "java/net/InetAddress");
        if (joma_CODE == 15) return Word_SMS(Nosaukums, "java/net/DatagramSocket");
        if (joma_CODE == 16) return Word_SMS(Nosaukums, "java/net/DatagramPacket");
        if (joma_CODE == 13) return Word_SMS(Nosaukums, kaudze_VALUE[objekts_Uzziņas + 3] != 0 ? "Latviešu/savs/nodarbinātais" : "java/lang/Thread");
        if (joma_CODE == 2) return Word_SMS(Nosaukums, "[I"); if (joma_CODE == 20) return Word_SMS(Nosaukums, "[B"); if (joma_CODE == 21) return Word_SMS(Nosaukums, "[Z");
        if (joma_CODE == 22) return Word_SMS(Nosaukums, "[C"); if (joma_CODE == 23) return Word_SMS(Nosaukums, "[S");
        if (joma_CODE != 3) return false;
        if (Word_SMS(Nosaukums, "[Ljava/lang/Object;")) return true;
        int komponents = masīva_elements[objekts_Uzziņas];
        if (komponents == -1) return Word_SMS(Nosaukums, "[Ljava/lang/String;") || Word_SMS(Nosaukums, "[Ljava/lang/CharSequence;");
        if (komponents == 0) return false;
        if (배열종비교(komponents, Nosaukums)) return true;
        if ((Word_SMS(komponents, "java/lang/String") || Word_SMS(komponents, "java/lang/StringBuilder")) && Word_SMS(Nosaukums, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDEX = 0; Loop_INDEX < klase_definīcija_COUNT; Loop_INDEX++) if (같은말(klase_definīcija_nosaukums[Loop_INDEX], komponents)) {
            for (int koda_punkts = Loop_INDEX, 중첩깊이 = 0; koda_punkts >= 0 && 중첩깊이 < 16; 중첩깊이++, koda_punkts = vecākobjekts_klase(koda_punkts)) {
                if (배열종비교(klase_definīcija_vecākobjekts[koda_punkts], Nosaukums)) return true;
                for (int iekšējais_amats = 0; iekšējais_amats < klase_interfeiss_COUNT[koda_punkts]; iekšējais_amats++) if (배열종비교(klase_interfeiss[koda_punkts * 16 + iekšējais_amats], Nosaukums)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int nosaukums_konstante, int 형식참조) {
        int čeks_amats = 상가[형식참조], ievade_COUNT = konstante_SECOND_VALUE[형식참조];
        if (nosaukums_konstante == 0 || ievade_COUNT < 4 || Fails[čeks_amats] != '[' || Fails[čeks_amats + 1] != 'L' || Fails[čeks_amats + ievade_COUNT - 1] != ';' || konstante_SECOND_VALUE[nosaukums_konstante] != ievade_COUNT - 3) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < ievade_COUNT - 3; Loop_INDEX++) if (Fails[상가[nosaukums_konstante] + Loop_INDEX] != Fails[čeks_amats + 2 + Loop_INDEX]) return false;
        return true;
    }
    static void turis_izņēmums() {
        if (던진객체 == 0) return;
        Kļūda = false;
        while (kadrs_INDEX >= pašreizējais_saruna * 32) {
            int Fails_INDEX = kadrs_metode[kadrs_INDEX], 읽는자리 = 틀명령[kadrs_INDEX];
            for (int Loop_INDEX = 0; Loop_INDEX < 잡기수; Loop_INDEX++) if (잡기함수[Loop_INDEX] == Fails_INDEX && 읽는자리 >= 잡기시작[Loop_INDEX] && 읽는자리 < 잡기끝[Loop_INDEX]
                && (잡기종[Loop_INDEX] == 0 || 맞는객체(던진객체, 잡기종[Loop_INDEX]))) {
                kadrs_amats[kadrs_INDEX] = 잡기위치[Loop_INDEX]; kadrs_kopa[kadrs_INDEX] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (틀초기화[kadrs_INDEX] != 0) klase_definīcija_Statuss[틀초기화[kadrs_INDEX] - 1] = 3;
            if (kadrs_bloķēt[kadrs_INDEX] != 0) { izlaist_bloķēt(kadrs_bloķēt[kadrs_INDEX]); kadrs_bloķēt[kadrs_INDEX] = 0; }
            kadrs_INDEX--;
        }
        lietotājs.Rakstīt("Uncaught ");
        if (kaudze_VALUE[던진객체] == 9) { lietotājs.Rakstīt(izņēmums_nosaukums(kaudze_VALUE[던진객체 + 2])); lietotājs.Rakstīt(": "); rakstīšana_SMS(kaudze_VALUE[던진객체 + 3]); }
        else lietotājs.Rakstīt("user exception");
        lietotājs.rakstīšana_rakstzīme_VALUE(10); 던진객체 = 0; Kļūda = true;
    }
    // 이 JVM의 operands_kopa 항목은 pašreizējais_krājums category-1(int/reference)만 허용한다.
    static void 스택명령(int komanda_CODE) {
        int 첫값 = 빼기(0), 첫형식 = atdot_TYPE;
        if (komanda_CODE == 87) return;
        if (komanda_CODE == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int byte_dati = 빼기(0), SECOND_formāts = atdot_TYPE;
        if (komanda_CODE == 88) return;
        if (komanda_CODE == 90) { 넣기(첫값, 첫형식); 넣기(byte_dati, SECOND_formāts); 넣기(첫값, 첫형식); return; }
        if (komanda_CODE == 92) { 넣기(byte_dati, SECOND_formāts); 넣기(첫값, 첫형식); 넣기(byte_dati, SECOND_formāts); 넣기(첫값, 첫형식); return; }
        if (komanda_CODE == 95) { 넣기(첫값, 첫형식); 넣기(byte_dati, SECOND_formāts); return; }
        int koda_punkts = 빼기(0), 셋째형식 = atdot_TYPE;
        if (komanda_CODE == 91) { 넣기(첫값, 첫형식); 넣기(koda_punkts, 셋째형식); 넣기(byte_dati, SECOND_formāts); 넣기(첫값, 첫형식); return; }
        if (komanda_CODE == 93) { 넣기(byte_dati, SECOND_formāts); 넣기(첫값, 첫형식); 넣기(koda_punkts, 셋째형식); 넣기(byte_dati, SECOND_formāts); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = atdot_TYPE;
        넣기(byte_dati, SECOND_formāts); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(koda_punkts, 셋째형식); 넣기(byte_dati, SECOND_formāts); 넣기(첫값, 첫형식);
    }
    static void 새객체(int nosaukums_konstante, int 시작점) {
        int joma_CODE = 0, 유효길이 = 0, izņēmums_Uzziņas = izņēmums_konstante(nosaukums_konstante);
        if (Word_SMS(nosaukums_konstante, "java/lang/StringBuilder")) { joma_CODE = 4; 유효길이 = 1; }
        if (Word_SMS(nosaukums_konstante, "java/io/FileInputStream")) { joma_CODE = 5; 유효길이 = 2; }
        if (Word_SMS(nosaukums_konstante, "java/io/FileOutputStream")) { joma_CODE = 6; 유효길이 = 2; }
        if (izņēmums_Uzziņas != 0) { joma_CODE = 9; 유효길이 = 2; }
        if (Word_SMS(nosaukums_konstante, "java/util/ArrayList")) { joma_CODE = 10; 유효길이 = 2; }
        if (Word_SMS(nosaukums_konstante, "java/util/HashMap")) { joma_CODE = 11; 유효길이 = 2; }
        if (Word_SMS(nosaukums_konstante, "java/lang/Integer")) { joma_CODE = 12; 유효길이 = 1; }
        if (Word_SMS(nosaukums_konstante, "java/net/Socket")) { joma_CODE = 17; 유효길이 = 5; }
        if (Word_SMS(nosaukums_konstante, "java/net/ServerSocket")) { joma_CODE = 18; 유효길이 = 5; }
        if (Word_SMS(nosaukums_konstante, "java/net/DatagramSocket")) { joma_CODE = 15; 유효길이 = 3; }
        if (Word_SMS(nosaukums_konstante, "java/net/DatagramPacket")) { joma_CODE = 16; 유효길이 = 4; }
        if (Word_SMS(nosaukums_konstante, "java/lang/Thread") || Word_SMS(nosaukums_konstante, "Latviešu/savs/nodarbinātais")) { joma_CODE = 13; 유효길이 = 2; }
        if (Word_SMS(nosaukums_konstante, "java/lang/Object")) { joma_CODE = 8; }
        if (joma_CODE == 0 && 화면종(nosaukums_konstante) != 0) { joma_CODE = 화면종(nosaukums_konstante); 유효길이 = 12; }
        if (joma_CODE == 0) {
            int koda_punkts = FIND_klase_definīcija(nosaukums_konstante); if (koda_punkts < 0 || Kļūda || !초기화(koda_punkts, 시작점)) return;
            joma_CODE = 32 + koda_punkts; 유효길이 = 종칸수[koda_punkts];
        }
        int objekts_Uzziņas = piešķirt_Krātuve(joma_CODE, 유효길이); if (Kļūda) return;
        if (joma_CODE == 13 && Word_SMS(nosaukums_konstante, "Latviešu/savs/nodarbinātais")) kaudze_VALUE[objekts_Uzziņas + 3] = 1;
        if (joma_CODE >= 24 && joma_CODE <= 28 && 한국어화면종(nosaukums_konstante) != 0) kaudze_VALUE[objekts_Uzziņas + 13] = 1;
        if (joma_CODE == 5 || joma_CODE == 6 || joma_CODE == 15 || joma_CODE == 17 || joma_CODE == 18) kaudze_VALUE[objekts_Uzziņas + 2] = -1;
        if (joma_CODE == 9) kaudze_VALUE[objekts_Uzziņas + 2] = izņēmums_Uzziņas;
        넣기(objekts_Uzziņas, 2);
    }
    static boolean 값같음(int 첫값, int byte_dati) {
        if (첫값 == byte_dati) return true;
        if (첫값 == 0 || byte_dati == 0 || 첫값 < 0 || byte_dati < 0 || 첫값 >= kaudze_beigt_zvanu_amats || byte_dati >= kaudze_beigt_zvanu_amats) return false;
        if (kaudze_VALUE[첫값] == 1 && kaudze_VALUE[byte_dati] == 1) return 글같음(첫값, byte_dati, false);
        return kaudze_VALUE[첫값] == 12 && kaudze_VALUE[byte_dati] == 12 && kaudze_VALUE[첫값 + 2] == kaudze_VALUE[byte_dati + 2];
    }
    static int 글조각(int objekts_Uzziņas, int Sākt_amats, int beigt_zvanu_amats) {
        if (!objekts_VALUE(objekts_Uzziņas, 1)) return 0;
        if (Sākt_amats < 0 || beigt_zvanu_amats < Sākt_amats || beigt_zvanu_amats > kaudze_VALUE[objekts_Uzziņas + 1]) { kļūme_VALUE("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = piešķirt_Krātuve(1, beigt_zvanu_amats - Sākt_amats); if (Kļūda) return 0;
        for (int Loop_INDEX = Sākt_amats; Loop_INDEX < beigt_zvanu_amats; Loop_INDEX++) kaudze_VALUE[반환값 + 2 + Loop_INDEX - Sākt_amats] = kaudze_VALUE[objekts_Uzziņas + 2 + Loop_INDEX];
        return 반환값;
    }
    static int savienot_SMS(int 첫값, int byte_dati) {
        if (!objekts_VALUE(첫값, 1) || !objekts_VALUE(byte_dati, 1)) return 0;
        int ievade_COUNT = kaudze_VALUE[첫값 + 1], metode_INDEX = kaudze_VALUE[byte_dati + 1], 반환값 = piešķirt_Krātuve(1, ievade_COUNT + metode_INDEX); if (Kļūda) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < ievade_COUNT; Loop_INDEX++) kaudze_VALUE[반환값 + 2 + Loop_INDEX] = kaudze_VALUE[첫값 + 2 + Loop_INDEX];
        for (int Loop_INDEX = 0; Loop_INDEX < metode_INDEX; Loop_INDEX++) kaudze_VALUE[반환값 + 2 + ievade_COUNT + Loop_INDEX] = kaudze_VALUE[byte_dati + 2 + Loop_INDEX];
        return 반환값;
    }
    static boolean 기본호출(int īpašnieks, int nosaukums_konstante, int 서술상수, int komanda_CODE) {
        if (Word_SMS(īpašnieks, "Latviešu/savs/실행인수") && komanda_CODE == 184) {
            if (Word_SMS(nosaukums_konstante, "krājums_COUNT") && Word_SMS(서술상수, "()I")) { 넣기(lietotājs.인수개수() - 1, 1); return true; }
            if (Word_SMS(nosaukums_konstante, "Teksts") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= lietotājs.인수개수() - 1) 예외던짐(29, "Izpildīt_komanda Parametri 범위를 벗어났습니다");
                else 넣기(viesot_rakstzīme(lietotājs.Parametri(순번 + 1)), 2);
                return true;
            }
            kļūme_VALUE("지원하지 않는 Latviešu Izpildīt_komanda Parametri 호출"); return true;
        }
        if (Word_SMS(īpašnieks, "Latviešu/savs/nodarbinātais")) { Process_saruna(nosaukums_konstante, 서술상수, komanda_CODE, true); return true; }
        if (한국어화면소유(īpašnieks)) { 한국어화면호출(īpašnieks, nosaukums_konstante, 서술상수, komanda_CODE); return true; }
        if (화면소유(īpašnieks)) { 화면호출(īpašnieks, nosaukums_konstante, 서술상수, komanda_CODE); return true; }
        if (Word_SMS(īpašnieks, "java/net/Socket") || Word_SMS(īpašnieks, "java/net/ServerSocket") || Word_SMS(īpašnieks, "java/io/InputStream") || Word_SMS(īpašnieks, "java/io/OutputStream")) { 흐름호출(īpašnieks, nosaukums_konstante, 서술상수, komanda_CODE); return true; }
        if (Word_SMS(īpašnieks, "Latviešu/savs/kodols_VALUE") && komanda_CODE == 184) {
            if (Word_SMS(nosaukums_konstante, "화면너비") && Word_SMS(서술상수, "()I")) { 넣기(lietotājs.화면너비(), 1); return true; }
            if (Word_SMS(nosaukums_konstante, "화면높이") && Word_SMS(서술상수, "()I")) { 넣기(lietotājs.화면높이(), 1); return true; }
            if (Word_SMS(nosaukums_konstante, "밀리초") && Word_SMS(서술상수, "()I")) { 넣기(lietotājs.밀리초(), 1); return true; }
            if (Word_SMS(nosaukums_konstante, "그림대기") && Word_SMS(서술상수, "()I")) { 넣기(lietotājs.그림대기(), 1); return true; }
            if (Word_SMS(nosaukums_konstante, "taisnstūris") && Word_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), x_koordināta = 빼기(1); 넣기(lietotājs.taisnstūris(x_koordināta, 세로좌표, 너비, 높이, 색상), 1); return true; }
        }
        if (Word_SMS(īpašnieks, "java/net/InetAddress") || Word_SMS(īpašnieks, "java/net/DatagramPacket") || Word_SMS(īpašnieks, "java/net/DatagramSocket")) { 통신호출(īpašnieks, nosaukums_konstante, 서술상수, komanda_CODE); return true; }
        if (Word_SMS(īpašnieks, "java/lang/Thread")) { 가닥호출(nosaukums_konstante, 서술상수, komanda_CODE); return true; }
        if (Word_SMS(īpašnieks, "java/lang/Object")) {
            if (Word_SMS(nosaukums_konstante, "<init>") && Word_SMS(서술상수, "()V") && komanda_CODE == 183) { 객체유효(빼기(2)); return true; }
            if (Word_SMS(nosaukums_konstante, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int byte_dati = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == byte_dati ? 1 : 0, 1); return true; }
        }
        if (izņēmums_konstante(īpašnieks) != 0) {
            if (Word_SMS(nosaukums_konstante, "<init>") && komanda_CODE == 183 && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int uzvedne = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), objekts_Uzziņas = 빼기(2);
                if (objekts_VALUE(objekts_Uzziņas, 9)) { kaudze_VALUE[objekts_Uzziņas + 3] = uzvedne; kaudze_Uzziņas[objekts_Uzziņas + 3] = 1; } return true;
            }
            if ((Word_SMS(nosaukums_konstante, "getMessage") || Word_SMS(nosaukums_konstante, "설명")) && Word_SMS(서술상수, "()Ljava/lang/String;")) { int objekts_Uzziņas = 빼기(2); if (objekts_VALUE(objekts_Uzziņas, 9)) 넣기(kaudze_VALUE[objekts_Uzziņas + 3], 2); return true; }
        }
        if (Word_SMS(īpašnieks, "java/lang/String")) {
            if (komanda_CODE == 182 && Word_SMS(nosaukums_konstante, "getBytes") && (Word_SMS(서술상수, "()[B") || Word_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int kodēšana_nosaukums = Word_SMS(서술상수, "()[B") ? 0 : 빼기(2), objekts_Uzziņas = 빼기(2);
                if (!objekts_VALUE(objekts_Uzziņas, 1)) return true;
                if (kodēšana_nosaukums != 0 && !글같음(kodēšana_nosaukums, viesot_rakstzīme("UTF-8"), false) && !글같음(kodēšana_nosaukums, viesot_rakstzīme("UTF8"), false) && !글같음(kodēšana_nosaukums, viesot_rakstzīme("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int ievade_COUNT = kaudze_VALUE[objekts_Uzziņas + 1], 반환값 = piešķirt_Krātuve(20, ievade_COUNT * 3), 사용수 = 0; if (Kļūda) return true;
                for (int iekšējais_amats = 0; iekšējais_amats < ievade_COUNT; iekšējais_amats++) {
                    int koda_punkts = kaudze_VALUE[objekts_Uzziņas + 2 + iekšējais_amats];
                    if (koda_punkts >= 0xd800 && koda_punkts <= 0xdbff && iekšējais_amats + 1 < ievade_COUNT && kaudze_VALUE[objekts_Uzziņas + 3 + iekšējais_amats] >= 0xdc00 && kaudze_VALUE[objekts_Uzziņas + 3 + iekšējais_amats] <= 0xdfff) koda_punkts = 0x10000 + ((koda_punkts - 0xd800) << 10) + kaudze_VALUE[objekts_Uzziņas + 2 + ++iekšējais_amats] - 0xdc00;
                    else if (koda_punkts >= 0xd800 && koda_punkts <= 0xdfff) koda_punkts = '?';
                    if (koda_punkts < 128) kaudze_VALUE[반환값 + 2 + 사용수++] = koda_punkts;
                    else { int byte_COUNT = koda_punkts < 2048 ? 2 : koda_punkts < 65536 ? 3 : 4; kaudze_VALUE[반환값 + 2 + 사용수++] = (byte)((byte_COUNT == 2 ? 192 : byte_COUNT == 3 ? 224 : 240) | koda_punkts >> (6 * (byte_COUNT - 1))); for (int Salīdzinājums_amats = byte_COUNT - 1; Salīdzinājums_amats > 0; Salīdzinājums_amats--) kaudze_VALUE[반환값 + 2 + 사용수++] = (byte)(128 | koda_punkts >> (6 * (Salīdzinājums_amats - 1)) & 63); }
                }
                kaudze_VALUE[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (komanda_CODE == 184 && Word_SMS(nosaukums_konstante, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(cipars_rakstzīme(빼기(1)), 2); return true; }
            if (komanda_CODE != 182) return false;
            if (Word_SMS(nosaukums_konstante, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int byte_dati = 빼기(2), 첫값 = 빼기(2); if (objekts_VALUE(첫값, 1)) 넣기(글같음(첫값, byte_dati, false) ? 1 : 0, 1); return true; }
            if (Word_SMS(nosaukums_konstante, "isEmpty") && Word_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (objekts_VALUE(첫값, 1)) 넣기(kaudze_VALUE[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_SMS(nosaukums_konstante, "substring") && (Word_SMS(서술상수, "(I)Ljava/lang/String;") || Word_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SECOND_VALUE = Word_SMS(서술상수, "(II)Ljava/lang/String;"); int beigt_zvanu_amats = SECOND_VALUE ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (objekts_VALUE(첫값, 1)) 넣기(글조각(첫값, 시작점, SECOND_VALUE ? beigt_zvanu_amats : kaudze_VALUE[첫값 + 1]), 2); return true;
            }
            if (Word_SMS(nosaukums_konstante, "concat") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int byte_dati = 빼기(2), 첫값 = 빼기(2); 넣기(savienot_SMS(첫값, byte_dati), 2); return true; }
            if (Word_SMS(nosaukums_konstante, "hashCode") && Word_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), jaukšana_VALUE = 0; if (objekts_VALUE(첫값, 1)) { for (int Loop_INDEX = 0; Loop_INDEX < kaudze_VALUE[첫값 + 1]; Loop_INDEX++) jaukšana_VALUE = jaukšana_VALUE * 31 + kaudze_VALUE[첫값 + 2 + Loop_INDEX]; 넣기(jaukšana_VALUE, 1); } return true; }
            if (Word_SMS(nosaukums_konstante, "toString") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (objekts_VALUE(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_SMS(īpašnieks, "java/lang/Integer")) {
            if (komanda_CODE == 184 && Word_SMS(nosaukums_konstante, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int dati_VALUE = 빼기(1), objekts_Uzziņas = dati_VALUE >= -128 && dati_VALUE <= 127 ? Store_vesels_skaitlis[dati_VALUE + 128] : 0; if (objekts_Uzziņas == 0) { objekts_Uzziņas = piešķirt_Krātuve(12, 1); if (!Kļūda) { kaudze_VALUE[objekts_Uzziņas + 2] = dati_VALUE; if (dati_VALUE >= -128 && dati_VALUE <= 127) Store_vesels_skaitlis[dati_VALUE + 128] = objekts_Uzziņas; } } 넣기(objekts_Uzziņas, 2); return true; }
            if (komanda_CODE == 183 && Word_SMS(nosaukums_konstante, "<init>") && Word_SMS(서술상수, "(I)V")) { int dati_VALUE = 빼기(1), objekts_Uzziņas = 빼기(2); if (objekts_VALUE(objekts_Uzziņas, 12)) kaudze_VALUE[objekts_Uzziņas + 2] = dati_VALUE; return true; }
            if (komanda_CODE == 182 && Word_SMS(nosaukums_konstante, "intValue") && Word_SMS(서술상수, "()I")) { int objekts_Uzziņas = 빼기(2); if (objekts_VALUE(objekts_Uzziņas, 12)) 넣기(kaudze_VALUE[objekts_Uzziņas + 2], 1); return true; }
            if (komanda_CODE == 184 && Word_SMS(nosaukums_konstante, "toString") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(cipars_rakstzīme(빼기(1)), 2); return true; }
        }
        if (Word_SMS(īpašnieks, "java/lang/Math") && komanda_CODE == 184) {
            if (Word_SMS(nosaukums_konstante, "abs") && Word_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_SMS(nosaukums_konstante, "min") || Word_SMS(nosaukums_konstante, "max")) && Word_SMS(서술상수, "(II)I")) { int byte_dati = 빼기(1), 첫값 = 빼기(1); 넣기(Word_SMS(nosaukums_konstante, "min") ? (첫값 < byte_dati ? 첫값 : byte_dati) : (첫값 > byte_dati ? 첫값 : byte_dati), 1); return true; }
        }
        if (Word_SMS(īpašnieks, "java/lang/System") && komanda_CODE == 184) {
            if (Word_SMS(nosaukums_konstante, "gc") && Word_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Word_SMS(nosaukums_konstante, "arraycopy") && Word_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int ievade_COUNT = 빼기(1), mērķis_VALUE_INDEX = 빼기(1), byte_dati = 빼기(2), Sākt_amats = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(byte_dati)) {
                    int joma_CODE = kaudze_VALUE[첫값];
                    if (kaudze_VALUE[byte_dati] != joma_CODE || (joma_CODE != 2 && joma_CODE != 3 && (joma_CODE < 20 || joma_CODE > 23))) kļūme_VALUE("arraycopy type mismatch");
                    else if (ievade_COUNT < 0 || Sākt_amats < 0 || mērķis_VALUE_INDEX < 0 || Sākt_amats > kaudze_VALUE[첫값 + 1] - ievade_COUNT || mērķis_VALUE_INDEX > kaudze_VALUE[byte_dati + 1] - ievade_COUNT) kļūme_VALUE("ArrayIndexOutOfBoundsException");
                    else if (첫값 == byte_dati && mērķis_VALUE_INDEX > Sākt_amats) { for (int Loop_INDEX = ievade_COUNT - 1; Loop_INDEX >= 0; Loop_INDEX--) kaudze_VALUE[byte_dati + 2 + mērķis_VALUE_INDEX + Loop_INDEX] = kaudze_VALUE[첫값 + 2 + Sākt_amats + Loop_INDEX]; }
                    else { for (int Loop_INDEX = 0; Loop_INDEX < ievade_COUNT && !Kļūda; Loop_INDEX++) { int dati_VALUE = kaudze_VALUE[첫값 + 2 + Sākt_amats + Loop_INDEX]; if (joma_CODE != 3 || 배열저장가능(byte_dati, dati_VALUE)) kaudze_VALUE[byte_dati + 2 + mērķis_VALUE_INDEX + Loop_INDEX] = dati_VALUE; } }
                }
                return true;
            }
        }
        if (Word_SMS(īpašnieks, "java/util/ArrayList") || Word_SMS(īpašnieks, "java/util/List") || Word_SMS(īpašnieks, "java/util/HashMap") || Word_SMS(īpašnieks, "java/util/Map")) {
            모음호출(īpašnieks, nosaukums_konstante, 서술상수, komanda_CODE); return true;
        }
        return false;
    }
    static void 모음늘리기(int objekts_Uzziņas, int 필요수) {
        int 이전값 = kaudze_VALUE[objekts_Uzziņas + 2], noslodze_dati = 이전값 == 0 ? 0 : kaudze_VALUE[이전값 + 1];
        if (noslodze_dati >= 필요수) return;
        int Tālāk_amats = noslodze_dati < 8 ? 8 : noslodze_dati * 2; if (Tālāk_amats < 필요수) Tālāk_amats = 필요수;
        int dati_ARRAY = piešķirt_Krātuve(3, Tālāk_amats); if (Kļūda) return;
        for (int Loop_INDEX = 0; Loop_INDEX < noslodze_dati; Loop_INDEX++) kaudze_VALUE[dati_ARRAY + 2 + Loop_INDEX] = kaudze_VALUE[이전값 + 2 + Loop_INDEX];
        kaudze_VALUE[objekts_Uzziņas + 2] = dati_ARRAY; kaudze_Uzziņas[objekts_Uzziņas + 2] = 1;
    }
    static void 모음호출(int īpašnieks, int nosaukums_konstante, int 서술상수, int komanda_CODE) {
        boolean 대응참조 = Word_SMS(īpašnieks, "java/util/HashMap") || Word_SMS(īpašnieks, "java/util/Map"); int joma_CODE = 대응참조 ? 11 : 10;
        if (Word_SMS(nosaukums_konstante, "<init>") && komanda_CODE == 183 && Word_SMS(서술상수, "()V")) { int objekts_Uzziņas = 빼기(2); if (objekts_VALUE(objekts_Uzziņas, joma_CODE)) 모음늘리기(objekts_Uzziņas, 8); return; }
        if (komanda_CODE != 182 && komanda_CODE != 185) { kļūme_VALUE("invalid collection invocation"); return; }
        if (Word_SMS(nosaukums_konstante, "size") && Word_SMS(서술상수, "()I") || Word_SMS(nosaukums_konstante, "isEmpty") && Word_SMS(서술상수, "()Z")) {
            int objekts_Uzziņas = 빼기(2); if (objekts_VALUE(objekts_Uzziņas, joma_CODE)) 넣기(Word_SMS(nosaukums_konstante, "size") ? kaudze_VALUE[objekts_Uzziņas + 3] : kaudze_VALUE[objekts_Uzziņas + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_SMS(nosaukums_konstante, "clear") && Word_SMS(서술상수, "()V")) { int objekts_Uzziņas = 빼기(2); if (objekts_VALUE(objekts_Uzziņas, joma_CODE)) { int dati_ARRAY = kaudze_VALUE[objekts_Uzziņas + 2]; for (int Loop_INDEX = 0; Loop_INDEX < kaudze_VALUE[dati_ARRAY + 1]; Loop_INDEX++) kaudze_VALUE[dati_ARRAY + 2 + Loop_INDEX] = 0; kaudze_VALUE[objekts_Uzziņas + 3] = 0; } return; }
        if (!대응참조 && Word_SMS(nosaukums_konstante, "add") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int dati_VALUE = 빼기(2), objekts_Uzziņas = 빼기(2); if (!objekts_VALUE(objekts_Uzziņas, 10)) return;
            int ievade_COUNT = kaudze_VALUE[objekts_Uzziņas + 3]; 모음늘리기(objekts_Uzziņas, ievade_COUNT + 1); if (!Kļūda) { kaudze_VALUE[kaudze_VALUE[objekts_Uzziņas + 2] + 2 + ievade_COUNT] = dati_VALUE; kaudze_VALUE[objekts_Uzziņas + 3] = ievade_COUNT + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_SMS(nosaukums_konstante, "get") || Word_SMS(nosaukums_konstante, "remove")) && Word_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Word_SMS(nosaukums_konstante, "set") && Word_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean informācijas_tehnoloģija_piešķīra = Word_SMS(nosaukums_konstante, "set"); int dati_VALUE = informācijas_tehnoloģija_piešķīra ? 빼기(2) : 0, ievade_amats = 빼기(1), objekts_Uzziņas = 빼기(2);
            if (!objekts_VALUE(objekts_Uzziņas, 10)) return;
            int ievade_COUNT = kaudze_VALUE[objekts_Uzziņas + 3], dati_ARRAY = kaudze_VALUE[objekts_Uzziņas + 2];
            if (ievade_amats < 0 || ievade_amats >= ievade_COUNT) { 예외던짐(6, "list index"); return; }
            int 이전값 = kaudze_VALUE[dati_ARRAY + 2 + ievade_amats];
            if (informācijas_tehnoloģija_piešķīra) kaudze_VALUE[dati_ARRAY + 2 + ievade_amats] = dati_VALUE;
            if (Word_SMS(nosaukums_konstante, "remove")) { for (int Loop_INDEX = ievade_amats + 1; Loop_INDEX < ievade_COUNT; Loop_INDEX++) kaudze_VALUE[dati_ARRAY + 1 + Loop_INDEX] = kaudze_VALUE[dati_ARRAY + 2 + Loop_INDEX]; kaudze_VALUE[dati_ARRAY + 1 + ievade_COUNT] = 0; kaudze_VALUE[objekts_Uzziņas + 3] = ievade_COUNT - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Word_SMS(nosaukums_konstante, "get") || Word_SMS(nosaukums_konstante, "remove")) && Word_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(nosaukums_konstante, "put") && Word_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(nosaukums_konstante, "containsKey") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_SMS(nosaukums_konstante, "put"), noņemt = Word_SMS(nosaukums_konstante, "remove");
            int dati_VALUE = 넣기여부 ? 빼기(2) : 0, Atslēga_Uzziņas = 빼기(2), objekts_Uzziņas = 빼기(2); if (!objekts_VALUE(objekts_Uzziņas, 11)) return;
            int ievade_COUNT = kaudze_VALUE[objekts_Uzziņas + 3], dati_ARRAY = kaudze_VALUE[objekts_Uzziņas + 2], 찾은여부 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < ievade_COUNT; Loop_INDEX++) if (값같음(Atslēga_Uzziņas, kaudze_VALUE[dati_ARRAY + 2 + 2 * Loop_INDEX])) { 찾은여부 = Loop_INDEX; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : kaudze_VALUE[dati_ARRAY + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(objekts_Uzziņas, (ievade_COUNT + 1) * 2); dati_ARRAY = kaudze_VALUE[objekts_Uzziņas + 2]; 찾은여부 = ievade_COUNT; if (!Kļūda) kaudze_VALUE[objekts_Uzziņas + 3] = ievade_COUNT + 1; }
                if (!Kļūda) { kaudze_VALUE[dati_ARRAY + 2 + 2 * 찾은여부] = Atslēga_Uzziņas; kaudze_VALUE[dati_ARRAY + 3 + 2 * 찾은여부] = dati_VALUE; }
            }
            if (noņemt && 찾은여부 >= 0) { for (int Loop_INDEX = 찾은여부 + 1; Loop_INDEX < ievade_COUNT; Loop_INDEX++) { kaudze_VALUE[dati_ARRAY + 2 * Loop_INDEX] = kaudze_VALUE[dati_ARRAY + 2 + 2 * Loop_INDEX]; kaudze_VALUE[dati_ARRAY + 1 + 2 * Loop_INDEX] = kaudze_VALUE[dati_ARRAY + 3 + 2 * Loop_INDEX]; } kaudze_VALUE[dati_ARRAY + 2 * ievade_COUNT] = 0; kaudze_VALUE[dati_ARRAY + 1 + 2 * ievade_COUNT] = 0; kaudze_VALUE[objekts_Uzziņas + 3] = ievade_COUNT - 1; }
            if (Word_SMS(nosaukums_konstante, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        kļūme_VALUE("unsupported collection method");
    }
    static boolean 잠금얻기(int objekts_Uzziņas) {
        if (!객체유효(objekts_Uzziņas)) return false;
        if (잠금깊이[objekts_Uzziņas] != 0 && bloķēt_īpašnieks[objekts_Uzziņas] != pašreizējais_saruna + 1) { mainīt_pieprasījums = true; return false; }
        bloķēt_īpašnieks[objekts_Uzziņas] = pašreizējais_saruna + 1; 잠금깊이[objekts_Uzziņas]++; return true;
    }
    static void izlaist_bloķēt(int objekts_Uzziņas) {
        if (!객체유효(objekts_Uzziņas)) return;
        if (잠금깊이[objekts_Uzziņas] == 0 || bloķēt_īpašnieks[objekts_Uzziņas] != pašreizējais_saruna + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[objekts_Uzziņas] == 0) bloķēt_īpašnieks[objekts_Uzziņas] = 0;
    }
    static boolean SWITCH_saruna() {
        saruna_kadrs[pašreizējais_saruna] = kadrs_INDEX;
        if (kadrs_INDEX < pašreizējais_saruna * 32) saruna_Statuss[pašreizējais_saruna] = 3;
        for (int Loop_INDEX = 0; Loop_INDEX < saruna_COUNT; Loop_INDEX++) if (saruna_Statuss[Loop_INDEX] == 2 && saruna_Statuss[가닥대기[Loop_INDEX]] == 3) saruna_Statuss[Loop_INDEX] = 1;
        for (int Loop_INDEX = 1; Loop_INDEX <= saruna_COUNT; Loop_INDEX++) {
            int Tālāk_amats = (pašreizējais_saruna + Loop_INDEX) % saruna_COUNT;
            if (saruna_Statuss[Tālāk_amats] == 1) { pašreizējais_saruna = Tālāk_amats; kadrs_INDEX = saruna_kadrs[Tālāk_amats]; mainīt_pieprasījums = false; return true; }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < saruna_COUNT; Loop_INDEX++) if (saruna_Statuss[Loop_INDEX] != 3) { kļūme_VALUE("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int nosaukums_konstante, int 서술상수, int komanda_CODE) { Process_saruna(nosaukums_konstante, 서술상수, komanda_CODE, false); }
    static void Process_saruna(int nosaukums_konstante, int 서술상수, int komanda_CODE, boolean Latviešu) {
        if (komanda_CODE == 184 && Word_SMS(nosaukums_konstante, Latviešu ? "YIELD_uzdevums" : "yield") && Word_SMS(서술상수, "()V")) { mainīt_pieprasījums = true; return; }
        if (komanda_CODE == 184 && Word_SMS(nosaukums_konstante, "currentThread") && Word_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(saruna_objekts[pašreizējais_saruna], 2); return; }
        if (komanda_CODE == 183 && Word_SMS(nosaukums_konstante, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, Latviešu ? "(LLatviešu/savs/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int mērķis_adrese = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), objekts_Uzziņas = 빼기(2);
            if (!객체유효(objekts_Uzziņas)) return;
            if (kaudze_VALUE[objekts_Uzziņas] == 13) { kaudze_VALUE[objekts_Uzziņas + 2] = mērķis_adrese; kaudze_Uzziņas[objekts_Uzziņas + 2] = 1; }
            else if (mērķis_adrese != 0) kļūme_VALUE("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (komanda_CODE == 182 && (Word_SMS(nosaukums_konstante, Latviešu ? "Sākt_uzdevums" : "start") || Word_SMS(nosaukums_konstante, Latviešu ? "기다리기" : "join")) && Word_SMS(서술상수, "()V") || komanda_CODE == 182 && Word_SMS(nosaukums_konstante, Latviešu ? "살아있는가" : "isAlive") && Word_SMS(서술상수, "()Z")) {
            int objekts_Uzziņas = 빼기(2); if (!객체유효(objekts_Uzziņas)) return;
            int konts_VALUE = -1; for (int Loop_INDEX = 0; Loop_INDEX < saruna_COUNT; Loop_INDEX++) if (saruna_objekts[Loop_INDEX] == objekts_Uzziņas) konts_VALUE = Loop_INDEX;
            if (Word_SMS(nosaukums_konstante, Latviešu ? "살아있는가" : "isAlive")) { 넣기(konts_VALUE >= 0 && saruna_Statuss[konts_VALUE] != 3 ? 1 : 0, 1); return; }
            if (Word_SMS(nosaukums_konstante, Latviešu ? "기다리기" : "join")) { if (konts_VALUE >= 0 && saruna_Statuss[konts_VALUE] != 3) { 가닥대기[pašreizējais_saruna] = konts_VALUE; saruna_Statuss[pašreizējais_saruna] = 2; mainīt_pieprasījums = true; } return; }
            if (konts_VALUE >= 0) { 예외던짐(Latviešu ? 38 : 16, "thread already started"); return; }
            if (saruna_COUNT == 4) { kļūme_VALUE("thread limit (4 including main)"); return; }
            int mērķis_adrese = kaudze_VALUE[objekts_Uzziņas] == 13 ? kaudze_VALUE[objekts_Uzziņas + 2] : objekts_Uzziņas;
            int Fails_INDEX = mērķis_adrese > 0 && kaudze_VALUE[mērķis_adrese] >= 32 ? nosaukums_metode(kaudze_VALUE[mērķis_adrese] - 32, Latviešu ? "Izpildīt" : "run", "()V") : -1;
            if (mērķis_adrese != 0 && Fails_INDEX < 0) { kļūme_VALUE("Runnable.run required"); return; }
            konts_VALUE = saruna_COUNT++; saruna_objekts[konts_VALUE] = objekts_Uzziņas; saruna_mērķis[konts_VALUE] = mērķis_adrese;
            int kadrs = konts_VALUE * 32; saruna_kadrs[konts_VALUE] = Fails_INDEX < 0 ? kadrs - 1 : kadrs; saruna_Statuss[konts_VALUE] = Fails_INDEX < 0 ? 3 : 1;
            if (Fails_INDEX >= 0) { kadrs_metode[kadrs] = Fails_INDEX; kadrs_amats[kadrs] = metode_Sākt[Fails_INDEX]; vietējs_VALUE[kadrs * 128] = mērķis_adrese; vietējs_TYPE[kadrs * 128] = 2; }
            return;
        }
        kļūme_VALUE("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], adrese_SMS = new int[16];
    static int vietējs_adrese() { return adrese_objekts(0x7f000001); }
    static int adrese_objekts(int VALUE) { int objekts_Uzziņas = piešķirt_Krātuve(14, 1); if (!Kļūda) kaudze_VALUE[objekts_Uzziņas + 2] = VALUE; return objekts_Uzziņas; }
    static int 주소해독(int objekts_Uzziņas) {
        if (objekts_Uzziņas == 0 || 글같음(objekts_Uzziņas, viesot_rakstzīme("localhost"), false)) return 0x7f000001;
        if (!objekts_VALUE(objekts_Uzziņas, 1)) return 0;
        int dati_VALUE = 0, kopsumma_COUNT = 0, adrese_byte = 0, 자릿수 = 0, ievade_COUNT = kaudze_VALUE[objekts_Uzziņas + 1];
        for (int Loop_INDEX = 0; Loop_INDEX <= ievade_COUNT; Loop_INDEX++) {
            int koda_punkts = Loop_INDEX == ievade_COUNT ? '.' : kaudze_VALUE[objekts_Uzziņas + 2 + Loop_INDEX];
            if (koda_punkts == '.') { if (자릿수 == 0 || kopsumma_COUNT == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } dati_VALUE = dati_VALUE << 8 | adrese_byte; kopsumma_COUNT++; adrese_byte = 자릿수 = 0; }
            else { if (koda_punkts < '0' || koda_punkts > '9' || ++자릿수 > 3 || (adrese_byte = adrese_byte * 10 + koda_punkts - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (kopsumma_COUNT != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return dati_VALUE;
    }
    static int adrese_rakstzīme(int dati_VALUE) {
        int ievade_COUNT = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int adrese_byte = dati_VALUE >>> 이동비트 & 255;
            if (adrese_byte >= 100) adrese_SMS[ievade_COUNT++] = '0' + adrese_byte / 100;
            if (adrese_byte >= 10) adrese_SMS[ievade_COUNT++] = '0' + adrese_byte / 10 % 10;
            adrese_SMS[ievade_COUNT++] = '0' + adrese_byte % 10; if (이동비트 != 0) adrese_SMS[ievade_COUNT++] = '.';
        }
        int objekts_Uzziņas = piešķirt_Krātuve(1, ievade_COUNT); if (!Kļūda) for (int Loop_INDEX = 0; Loop_INDEX < ievade_COUNT; Loop_INDEX++) kaudze_VALUE[objekts_Uzziņas + 2 + Loop_INDEX] = adrese_SMS[Loop_INDEX]; return objekts_Uzziņas;
    }
    static void 통신호출(int īpašnieks, int nosaukums_konstante, int 서술상수, int komanda_CODE) {
        if (Word_SMS(īpašnieks, "java/net/InetAddress")) {
            if (komanda_CODE == 184 && Word_SMS(nosaukums_konstante, "getLoopbackAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(vietējs_adrese(), 2); return; }
            if (komanda_CODE == 184 && Word_SMS(nosaukums_konstante, "getByName") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int dati_VALUE = 주소해독(빼기(2)); if (던진객체 == 0 && !Kļūda) 넣기(adrese_objekts(dati_VALUE), 2); return;
            }
            if (komanda_CODE == 182 && Word_SMS(nosaukums_konstante, "getHostAddress") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int objekts_Uzziņas = 빼기(2); if (objekts_VALUE(objekts_Uzziņas, 14)) 넣기(adrese_rakstzīme(kaudze_VALUE[objekts_Uzziņas + 2]), 2); return; }
        }
        if (Word_SMS(īpašnieks, "java/net/DatagramPacket")) {
            if (komanda_CODE == 183 && Word_SMS(nosaukums_konstante, "<init>") && (Word_SMS(서술상수, "([BI)V") || Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean mērķis_VALUE_Uzziņas = Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int porta_numurs = mērķis_VALUE_Uzziņas ? 빼기(1) : 0, adrese_Uzziņas = mērķis_VALUE_Uzziņas ? 빼기(2) : 0;
                int ievade_COUNT = 빼기(1), dati_ARRAY = 빼기(2), objekts_Uzziņas = 빼기(2);
                if (!objekts_VALUE(objekts_Uzziņas, 16) || !objekts_VALUE(dati_ARRAY, 20)) return;
                if (ievade_COUNT < 0 || ievade_COUNT > kaudze_VALUE[dati_ARRAY + 1] || porta_numurs < 0 || porta_numurs > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (adrese_Uzziņas != 0 && !objekts_VALUE(adrese_Uzziņas, 14)) return;
                kaudze_VALUE[objekts_Uzziņas + 2] = dati_ARRAY; kaudze_Uzziņas[objekts_Uzziņas + 2] = 1; kaudze_VALUE[objekts_Uzziņas + 3] = ievade_COUNT;
                kaudze_VALUE[objekts_Uzziņas + 4] = adrese_Uzziņas; kaudze_Uzziņas[objekts_Uzziņas + 4] = 1; kaudze_VALUE[objekts_Uzziņas + 5] = porta_numurs; return;
            }
            if (komanda_CODE == 182 && Word_SMS(nosaukums_konstante, "setLength") && Word_SMS(서술상수, "(I)V")) {
                int ievade_COUNT = 빼기(1), objekts_Uzziņas = 빼기(2); if (!objekts_VALUE(objekts_Uzziņas, 16)) return;
                if (ievade_COUNT < 0 || ievade_COUNT > kaudze_VALUE[kaudze_VALUE[objekts_Uzziņas + 2] + 1]) 예외던짐(9, "invalid datagram length"); else kaudze_VALUE[objekts_Uzziņas + 3] = ievade_COUNT; return;
            }
            if (komanda_CODE == 182 && (Word_SMS(nosaukums_konstante, "getData") && Word_SMS(서술상수, "()[B") || Word_SMS(nosaukums_konstante, "getLength") && Word_SMS(서술상수, "()I") || Word_SMS(nosaukums_konstante, "getAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;") || Word_SMS(nosaukums_konstante, "getPort") && Word_SMS(서술상수, "()I"))) {
                int objekts_Uzziņas = 빼기(2); if (!objekts_VALUE(objekts_Uzziņas, 16)) return;
                int ievade_amats = Word_SMS(nosaukums_konstante, "getData") ? 2 : Word_SMS(nosaukums_konstante, "getLength") ? 3 : Word_SMS(nosaukums_konstante, "getAddress") ? 4 : 5;
                넣기(kaudze_VALUE[objekts_Uzziņas + ievade_amats], ievade_amats == 2 || ievade_amats == 4 ? 2 : 1); return;
            }
        }
        if (Word_SMS(īpašnieks, "java/net/DatagramSocket")) {
            if (komanda_CODE == 183 && Word_SMS(nosaukums_konstante, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(I)V"))) {
                int porta_numurs = Word_SMS(서술상수, "()V") ? 0 : 빼기(1), objekts_Uzziņas = 빼기(2); if (!objekts_VALUE(objekts_Uzziņas, 15)) return;
                if (porta_numurs < 0 || porta_numurs > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = lietotājs.atvērt_tīkls(porta_numurs); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else kaudze_VALUE[objekts_Uzziņas + 2] = 열린파일번호; return;
            }
            if (komanda_CODE == 182 && Word_SMS(nosaukums_konstante, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), objekts_Uzziņas = 빼기(2); if (!objekts_VALUE(objekts_Uzziņas, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else kaudze_VALUE[objekts_Uzziņas + 3] = 밀리초값; return;
            }
            if (komanda_CODE == 182 && Word_SMS(nosaukums_konstante, "getLocalPort") && Word_SMS(서술상수, "()I")) { int objekts_Uzziņas = 빼기(2); if (objekts_VALUE(objekts_Uzziņas, 15)) 넣기(kaudze_VALUE[objekts_Uzziņas + 2] < 0 ? -1 : lietotājs.tīkls_ports(kaudze_VALUE[objekts_Uzziņas + 2]), 1); return; }
            if (komanda_CODE == 182 && Word_SMS(nosaukums_konstante, "isClosed") && Word_SMS(서술상수, "()Z")) { int objekts_Uzziņas = 빼기(2); if (objekts_VALUE(objekts_Uzziņas, 15)) 넣기(kaudze_VALUE[objekts_Uzziņas + 2] < 0 ? 1 : 0, 1); return; }
            if (komanda_CODE == 182 && Word_SMS(nosaukums_konstante, "close") && Word_SMS(서술상수, "()V")) { int objekts_Uzziņas = 빼기(2); if (objekts_VALUE(objekts_Uzziņas, 15) && kaudze_VALUE[objekts_Uzziņas + 2] >= 0) { lietotājs.파일서술자닫기(kaudze_VALUE[objekts_Uzziņas + 2]); kaudze_VALUE[objekts_Uzziņas + 2] = -1; } return; }
            if (komanda_CODE == 182 && (Word_SMS(nosaukums_konstante, "send") || Word_SMS(nosaukums_konstante, "receive")) && Word_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int pakete = 빼기(2), objekts_Uzziņas = 빼기(2); if (!objekts_VALUE(pakete, 16) || !objekts_VALUE(objekts_Uzziņas, 15)) return;
                int dati_ARRAY = kaudze_VALUE[pakete + 2], 유효길이 = kaudze_VALUE[pakete + 3], 열린파일번호 = kaudze_VALUE[objekts_Uzziņas + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_SMS(nosaukums_konstante, "send")) {
                    if (!objekts_VALUE(kaudze_VALUE[pakete + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < 유효길이; Loop_INDEX++) 통신임시[Loop_INDEX] = kaudze_VALUE[dati_ARRAY + 2 + Loop_INDEX];
                    if (lietotājs.sūtīt_tīkls(열린파일번호, kaudze_VALUE[kaudze_VALUE[pakete + 4] + 2], kaudze_VALUE[pakete + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int ievade_COUNT = lietotājs.saņemt_tīkls(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (ievade_COUNT == -11) {
                        int pašreizējais_TIME = lietotājs.밀리초();
                        if (kaudze_VALUE[objekts_Uzziņas + 4] == 0) kaudze_VALUE[objekts_Uzziņas + 4] = pašreizējais_TIME + 1;
                        if (kaudze_VALUE[objekts_Uzziņas + 3] > 0 && pašreizējais_TIME - (kaudze_VALUE[objekts_Uzziņas + 4] - 1) >= kaudze_VALUE[objekts_Uzziņas + 3]) { kaudze_VALUE[objekts_Uzziņas + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(objekts_Uzziņas, 2); 넣기(pakete, 2); kadrs_amats[kadrs_INDEX] = 틀명령[kadrs_INDEX]; mainīt_pieprasījums = true; return;
                    }
                    kaudze_VALUE[objekts_Uzziņas + 4] = 0;
                    if (ievade_COUNT < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < ievade_COUNT; Loop_INDEX++) kaudze_VALUE[dati_ARRAY + 2 + Loop_INDEX] = (byte)통신임시[Loop_INDEX];
                    kaudze_VALUE[pakete + 3] = ievade_COUNT; kaudze_VALUE[pakete + 4] = adrese_objekts(통신임시[513]); kaudze_Uzziņas[pakete + 4] = 1; kaudze_VALUE[pakete + 5] = 통신임시[512];
                }
                return;
            }
        }
        kļūme_VALUE("unsupported java.net method");
    }
    static boolean 흐름대기(int objekts_Uzziņas) {
        int pašreizējais_TIME = lietotājs.밀리초();
        if (kaudze_VALUE[objekts_Uzziņas + 5] == 0) kaudze_VALUE[objekts_Uzziņas + 5] = pašreizējais_TIME + 1;
        if (kaudze_VALUE[objekts_Uzziņas + 3] > 0 && pašreizējais_TIME - (kaudze_VALUE[objekts_Uzziņas + 5] - 1) >= kaudze_VALUE[objekts_Uzziņas + 3]) { kaudze_VALUE[objekts_Uzziņas + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        kadrs_amats[kadrs_INDEX] = 틀명령[kadrs_INDEX]; mainīt_pieprasījums = true; return true;
    }
    static void 흐름호출(int īpašnieks, int nosaukums_konstante, int 서술상수, int komanda_CODE) {
        boolean saņemt_lapa = Word_SMS(īpašnieks, "java/net/ServerSocket"), Stream = Word_SMS(īpašnieks, "java/io/InputStream") || Word_SMS(īpašnieks, "java/io/OutputStream");
        if (!Stream && komanda_CODE == 183 && Word_SMS(nosaukums_konstante, "<init>")) {
            boolean 빈여부 = Word_SMS(서술상수, "()V"), 이름지정여부 = Word_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || saņemt_lapa && Word_SMS(서술상수, "(I)V") || !saņemt_lapa && (이름지정여부 || 주소지정여부))) { kļūme_VALUE("unsupported socket constructor"); return; }
            int porta_numurs = 빈여부 ? 0 : 빼기(1), adrese_Uzziņas = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, objekts_Uzziņas = 빼기(2);
            if (!objekts_VALUE(objekts_Uzziņas, saņemt_lapa ? 18 : 17)) return;
            if (porta_numurs < 0 || porta_numurs > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !objekts_VALUE(adrese_Uzziņas, 14)) return;
            int tīkla_ID = 이름지정여부 ? 주소해독(adrese_Uzziņas) : 주소지정여부 ? kaudze_VALUE[adrese_Uzziņas + 2] : 0x7f000001;
            if (Kļūda || 던진객체 != 0) return;
            int 열린파일번호 = lietotājs.Stream_vadība(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : saņemt_lapa ? lietotājs.Stream_vadība(1, 열린파일번호, porta_numurs) : lietotājs.saziņa_Stream(열린파일번호, tīkla_ID, porta_numurs);
            if (처리값 < 0) { lietotājs.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            kaudze_VALUE[objekts_Uzziņas + 2] = 열린파일번호; kaudze_VALUE[objekts_Uzziņas + 4] = porta_numurs; kaudze_VALUE[objekts_Uzziņas + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!Stream && Word_SMS(nosaukums_konstante, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), objekts_Uzziņas = 빼기(2); if (!objekts_VALUE(objekts_Uzziņas, saņemt_lapa ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else kaudze_VALUE[objekts_Uzziņas + 3] = 밀리초값; return; }
        if (!Stream && Word_SMS(nosaukums_konstante, "close") && Word_SMS(서술상수, "()V")) { int objekts_Uzziņas = 빼기(2); if (objekts_VALUE(objekts_Uzziņas, saņemt_lapa ? 18 : 17) && kaudze_VALUE[objekts_Uzziņas + 2] >= 0) { lietotājs.파일서술자닫기(kaudze_VALUE[objekts_Uzziņas + 2]); kaudze_VALUE[objekts_Uzziņas + 2] = -1; } return; }
        if (!Stream && (Word_SMS(nosaukums_konstante, "getLocalPort") || Word_SMS(nosaukums_konstante, "getPort") || Word_SMS(nosaukums_konstante, "isClosed") || Word_SMS(nosaukums_konstante, "isConnected"))) {
            int objekts_Uzziņas = 빼기(2); if (!objekts_VALUE(objekts_Uzziņas, saņemt_lapa ? 18 : 17)) return;
            넣기(Word_SMS(nosaukums_konstante, "isClosed") ? kaudze_VALUE[objekts_Uzziņas + 2] < 0 ? 1 : 0 : Word_SMS(nosaukums_konstante, "isConnected") ? kaudze_VALUE[objekts_Uzziņas + 6] : Word_SMS(nosaukums_konstante, "getPort") ? kaudze_VALUE[objekts_Uzziņas + 4] : kaudze_VALUE[objekts_Uzziņas + 2] < 0 ? -1 : lietotājs.Stream_vadība(4, kaudze_VALUE[objekts_Uzziņas + 2], 0), 1); return;
        }
        if (saņemt_lapa && Word_SMS(nosaukums_konstante, "accept") && Word_SMS(서술상수, "()Ljava/net/Socket;")) {
            int objekts_Uzziņas = 빼기(2); if (!objekts_VALUE(objekts_Uzziņas, 18)) return; int 열린파일번호 = lietotājs.Stream_vadība(3, kaudze_VALUE[objekts_Uzziņas + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(objekts_Uzziņas)) 넣기(objekts_Uzziņas, 2); return; }
            kaudze_VALUE[objekts_Uzziņas + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = piešķirt_Krātuve(17, 5); if (Kļūda) { lietotājs.파일서술자닫기(열린파일번호); return; } kaudze_VALUE[반환값 + 2] = 열린파일번호; kaudze_VALUE[반환값 + 4] = lietotājs.Stream_vadība(5, 열린파일번호, 0); kaudze_VALUE[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!saņemt_lapa && !Stream && ((Word_SMS(nosaukums_konstante, "getInputStream") && Word_SMS(서술상수, "()Ljava/io/InputStream;")) || (Word_SMS(nosaukums_konstante, "getOutputStream") && Word_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int objekts_Uzziņas = 빼기(2); if (!objekts_VALUE(objekts_Uzziņas, 17)) return; if (kaudze_VALUE[objekts_Uzziņas + 2] < 0 || kaudze_VALUE[objekts_Uzziņas + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = piešķirt_Krātuve(19, 4); if (Kļūda) return; kaudze_VALUE[반환값 + 2] = objekts_Uzziņas; kaudze_Uzziņas[반환값 + 2] = 1; kaudze_VALUE[반환값 + 3] = Word_SMS(nosaukums_konstante, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (Stream) {
            boolean 읽기여부 = Word_SMS(nosaukums_konstante, "read"), informācijas_tehnoloģija_rakstīšana_operācija = Word_SMS(nosaukums_konstante, "write"), bloks = Word_SMS(서술상수, "([B)I") || Word_SMS(서술상수, "([B)V"), informācijas_tehnoloģija_SUBARRAY = Word_SMS(서술상수, "([BII)I") || Word_SMS(서술상수, "([BII)V");
            int ievade_COUNT = informācijas_tehnoloģija_SUBARRAY ? 빼기(1) : 0, 시작변위 = informācijas_tehnoloģija_SUBARRAY ? 빼기(1) : 0, dati_ARRAY = bloks || informācijas_tehnoloģija_SUBARRAY ? 빼기(2) : 0;
            int dati_VALUE = informācijas_tehnoloģija_rakstīšana_operācija && Word_SMS(서술상수, "(I)V") ? 빼기(1) : 0, objekts_Uzziņas = 빼기(2);
            if (!objekts_VALUE(objekts_Uzziņas, 19)) return; int vecākobjekts_Uzziņas = kaudze_VALUE[objekts_Uzziņas + 2], 열린파일번호 = kaudze_VALUE[vecākobjekts_Uzziņas + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_SMS(nosaukums_konstante, "close") && Word_SMS(서술상수, "()V")) { lietotājs.파일서술자닫기(열린파일번호); kaudze_VALUE[vecākobjekts_Uzziņas + 2] = -1; return; }
            if (Word_SMS(nosaukums_konstante, "flush") && Word_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !informācijas_tehnoloģija_rakstīšana_operācija) || 읽기여부 != (kaudze_VALUE[objekts_Uzziņas + 3] == 0)) { kļūme_VALUE("unsupported stream operation"); return; }
            if (bloks || informācijas_tehnoloģija_SUBARRAY) { if (!objekts_VALUE(dati_ARRAY, 20)) return; if (bloks) ievade_COUNT = kaudze_VALUE[dati_ARRAY + 1]; if (시작변위 < 0 || ievade_COUNT < 0 || 시작변위 > kaudze_VALUE[dati_ARRAY + 1] - ievade_COUNT) { 예외던짐(6, "stream array bounds"); return; } }
            else ievade_COUNT = 1;
            if (ievade_COUNT == 0) { if (읽기여부) 넣기(0, 1); return; }
            int Pabeigti_COUNT = informācijas_tehnoloģija_rakstīšana_operācija ? kaudze_VALUE[objekts_Uzziņas + 4] : 0, 처리값 = 0;
            while (Pabeigti_COUNT < ievade_COUNT) {
                처리값 = 읽기여부 ? lietotājs.파일한바이트읽기(열린파일번호) : lietotājs.파일한바이트쓰기(열린파일번호, bloks || informācijas_tehnoloģija_SUBARRAY ? kaudze_VALUE[dati_ARRAY + 2 + 시작변위 + Pabeigti_COUNT] : dati_VALUE);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (bloks || informācijas_tehnoloģija_SUBARRAY)) kaudze_VALUE[dati_ARRAY + 2 + 시작변위 + Pabeigti_COUNT] = (byte)처리값;
                Pabeigti_COUNT++; if (읽기여부 && !(bloks || informācijas_tehnoloģija_SUBARRAY)) break;
            }
            if (처리값 == -11 && (informācijas_tehnoloģija_rakstīšana_operācija || Pabeigti_COUNT == 0)) {
                kaudze_VALUE[objekts_Uzziņas + 4] = Pabeigti_COUNT;
                if (흐름대기(vecākobjekts_Uzziņas)) { 넣기(objekts_Uzziņas, 2); if (bloks || informācijas_tehnoloģija_SUBARRAY) 넣기(dati_ARRAY, 2); if (informācijas_tehnoloģija_SUBARRAY) { 넣기(시작변위, 1); 넣기(ievade_COUNT, 1); } if (informācijas_tehnoloģija_rakstīšana_operācija && !(bloks || informācijas_tehnoloģija_SUBARRAY)) 넣기(dati_VALUE, 1); } return;
            }
            kaudze_VALUE[objekts_Uzziņas + 4] = 0; kaudze_VALUE[vecākobjekts_Uzziņas + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(Pabeigti_COUNT == 0 && 처리값 == 256 ? -1 : bloks || informācijas_tehnoloģija_SUBARRAY ? Pabeigti_COUNT : 처리값, 1); return;
        }
        kļūme_VALUE("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int nosaukums_konstante) {
        if (Word_SMS(nosaukums_konstante, "Latviešu/savs/Logs")) return 24;
        if (Word_SMS(nosaukums_konstante, "Latviešu/savs/Etiķete")) return 26;
        if (Word_SMS(nosaukums_konstante, "Latviešu/savs/Pogas")) return 27;
        if (Word_SMS(nosaukums_konstante, "Latviešu/savs/teksta_lauks")) return 28;
        if (Word_SMS(nosaukums_konstante, "Latviešu/savs/darbība_informēšana")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int nosaukums_konstante) {
        return 한국어화면종(nosaukums_konstante) != 0 || Word_SMS(nosaukums_konstante, "Latviešu/savs/화면구성요소") || Word_SMS(nosaukums_konstante, "Latviešu/savs/notikums_rinda");
    }
    static int 화면종(int nosaukums_konstante) {
        int 한국어종 = 한국어화면종(nosaukums_konstante); if (한국어종 != 0) return 한국어종;
        if (Word_SMS(nosaukums_konstante, "javax/swing/JFrame")) return 24;
        if (Word_SMS(nosaukums_konstante, "javax/swing/JPanel")) return 25;
        if (Word_SMS(nosaukums_konstante, "javax/swing/JLabel")) return 26;
        if (Word_SMS(nosaukums_konstante, "javax/swing/JButton")) return 27;
        if (Word_SMS(nosaukums_konstante, "javax/swing/JTextField")) return 28;
        if (Word_SMS(nosaukums_konstante, "java/awt/event/ActionEvent")) return 29;
        if (Word_SMS(nosaukums_konstante, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int nosaukums_konstante) {
        return 화면종(nosaukums_konstante) != 0 || Word_SMS(nosaukums_konstante, "java/awt/Component") || Word_SMS(nosaukums_konstante, "java/awt/Container") || Word_SMS(nosaukums_konstante, "javax/swing/JComponent") || Word_SMS(nosaukums_konstante, "javax/swing/AbstractButton") || Word_SMS(nosaukums_konstante, "javax/swing/text/JTextComponent") || Word_SMS(nosaukums_konstante, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int objekts_Uzziņas) { if (!객체유효(objekts_Uzziņas)) return false; if (kaudze_VALUE[objekts_Uzziņas] < 24 || kaudze_VALUE[objekts_Uzziņas] > 28) { kļūme_VALUE("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int objekts_Uzziņas, int SMS_Uzziņas) {
        if (SMS_Uzziņas != 0 && !objekts_VALUE(SMS_Uzziņas, 1)) return;
        int ievade_COUNT = SMS_Uzziņas == 0 ? 0 : kaudze_VALUE[SMS_Uzziņas + 1]; if (ievade_COUNT > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < ievade_COUNT; Loop_INDEX++) 화면글임시[Loop_INDEX] = kaudze_VALUE[SMS_Uzziņas + 2 + Loop_INDEX];
        if (lietotājs.화면글(kaudze_VALUE[objekts_Uzziņas + 2], 화면글임시, ievade_COUNT) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        kaudze_VALUE[objekts_Uzziņas + 3] = SMS_Uzziņas; kaudze_Uzziņas[objekts_Uzziņas + 3] = 1;
    }
    static int 화면문자읽기(int objekts_Uzziņas) {
        int konts_VALUE = kaudze_VALUE[objekts_Uzziņas + 2], ievade_COUNT = lietotājs.화면연결(8, konts_VALUE, 0, 0, 0, 0), 사용수 = 0;
        if (ievade_COUNT < 0) { kļūme_VALUE("GUI text read failed"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < ievade_COUNT; Loop_INDEX++) { int 부호값 = lietotājs.화면연결(9, konts_VALUE, Loop_INDEX, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = piešķirt_Krātuve(1, 사용수); if (!Kļūda) for (int Loop_INDEX = 0; Loop_INDEX < 사용수; Loop_INDEX++) kaudze_VALUE[반환값 + 2 + Loop_INDEX] = 화면글임시[Loop_INDEX]; return 반환값;
    }
    /* Latviešu 객체를 직접 만들고 kodols_VALUE 화면 기능에 연결한다. Swing objekts_VALUE/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int īpašnieks, int nosaukums_konstante, int 서술상수, int komanda_CODE) {
        if (Word_SMS(īpašnieks, "Latviešu/savs/notikums_rinda")) {
            if (komanda_CODE == 184 && Word_SMS(nosaukums_konstante, "나중에실행") && Word_SMS(서술상수, "(LLatviešu/savs/실행할일;)V")) {
                int uzdevums_darbība = 빼기(2); if (!객체유효(uzdevums_darbība)) return;
                if (나중수 == 8) { kļūme_VALUE("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = uzdevums_darbība; return;
            }
            if (komanda_CODE == 184 && Word_SMS(nosaukums_konstante, "사건처리중인가") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            kļūme_VALUE("지원하지 않는 Latviešu 화면 일정 호출"); return;
        }
        if (Word_SMS(īpašnieks, "Latviešu/savs/darbība_informēšana")) {
            int informēšana = 빼기(2); if (!objekts_VALUE(informēšana, 29) || kaudze_VALUE[informēšana + 3] == 0) return;
            if (Word_SMS(nosaukums_konstante, "notikuma_avots") && Word_SMS(서술상수, "()LLatviešu/savs/화면구성요소;")) 넣기(kaudze_VALUE[informēšana + 2], 2);
            else if (Word_SMS(nosaukums_konstante, "komanda_SMS") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(kaudze_VALUE[informēšana + 2]), 2);
            else if (Word_SMS(nosaukums_konstante, "INDEX") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else kļūme_VALUE("지원하지 않는 Latviešu Darbība informēšana 호출"); return;
        }
        if (komanda_CODE == 183 && Word_SMS(nosaukums_konstante, "<init>")) {
            int 종류 = 한국어화면종(īpašnieks), 받이 = 0, 가로 = 0, vertikāle_amats = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Word_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (lietotājs.화면너비() - 폭) / 2; vertikāle_amats = (lietotājs.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Word_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Word_SMS(서술상수, "(Ljava/lang/String;IIIILLatviešu/savs/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); vertikāle_amats = 빼기(1); 가로 = 빼기(1);
            } else { kļūme_VALUE("지원하지 않는 Latviešu 화면 생성자"); return; }
            int Teksts = 빼기(2), elements_VALUE = 빼기(2); if (!화면객체(elements_VALUE)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || vertikāle_amats < 0 || 폭 > lietotājs.화면너비() - 가로 || 높이 > lietotājs.화면높이() - vertikāle_amats) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDEX = lietotājs.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (INDEX < 1 || INDEX > 32) { kļūme_VALUE("화면 elements_VALUE 자리가 가득 찼습니다"); return; }
            kaudze_VALUE[elements_VALUE + 2] = INDEX; 화면참조[INDEX - 1] = elements_VALUE;
            kaudze_VALUE[elements_VALUE + 5] = 가로; kaudze_VALUE[elements_VALUE + 6] = vertikāle_amats; kaudze_VALUE[elements_VALUE + 7] = 폭; kaudze_VALUE[elements_VALUE + 8] = 높이; kaudze_VALUE[elements_VALUE + 10] = 2;
            kaudze_VALUE[elements_VALUE + 4] = 받이; kaudze_Uzziņas[elements_VALUE + 4] = 1; kaudze_VALUE[elements_VALUE + 12] = 1;
            lietotājs.화면연결(1, INDEX, 가로, vertikāle_amats, 폭, 높이);
            if (종류 == 24) lietotājs.화면연결(7, INDEX, 2, 0, 0, 0);
            화면문자설정(elements_VALUE, Teksts); return;
        }
        if (komanda_CODE != 182) { kļūme_VALUE("잘못된 Latviešu 화면 호출 Komanda"); return; }
        if (Word_SMS(nosaukums_konstante, "rakstīšana_SMS") && Word_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int Teksts = 빼기(2), elements_VALUE = 빼기(2); if (화면객체(elements_VALUE)) 화면문자설정(elements_VALUE, Teksts); return;
        }
        if (Word_SMS(nosaukums_konstante, "글읽기") && Word_SMS(서술상수, "()Ljava/lang/String;")) {
            int elements_VALUE = 빼기(2); if (화면객체(elements_VALUE)) 넣기(화면문자읽기(elements_VALUE), 2); return;
        }
        if (Word_SMS(nosaukums_konstante, "동작맡기기") && Word_SMS(서술상수, "(LLatviešu/savs/동작받이;)V")) {
            int 받이 = 빼기(2), elements_VALUE = 빼기(2);
            if (화면객체(elements_VALUE)) { kaudze_VALUE[elements_VALUE + 4] = 받이; kaudze_Uzziņas[elements_VALUE + 4] = 1; kaudze_VALUE[elements_VALUE + 12] = 1; } return;
        }
        if (Word_SMS(nosaukums_konstante, "Pievienot_elements") && Word_SMS(서술상수, "(LLatviešu/savs/화면구성요소;)V")) {
            int bērns_VALUE = 빼기(2), vecākobjekts_VALUE = 빼기(2); if (!화면객체(bērns_VALUE) || !화면객체(vecākobjekts_VALUE)) return;
            if (lietotājs.화면연결(2, kaudze_VALUE[vecākobjekts_VALUE + 2], kaudze_VALUE[bērns_VALUE + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            kaudze_VALUE[bērns_VALUE + 11] = vecākobjekts_VALUE; kaudze_Uzziņas[bērns_VALUE + 11] = 1; return;
        }
        if (Word_SMS(nosaukums_konstante, "자리정하기") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), vertikāle_amats = 빼기(1), 가로 = 빼기(1), elements_VALUE = 빼기(2); if (!화면객체(elements_VALUE)) return;
            if (lietotājs.화면연결(1, kaudze_VALUE[elements_VALUE + 2], 가로, vertikāle_amats, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            kaudze_VALUE[elements_VALUE + 5] = 가로; kaudze_VALUE[elements_VALUE + 6] = vertikāle_amats; kaudze_VALUE[elements_VALUE + 7] = 폭; kaudze_VALUE[elements_VALUE + 8] = 높이; return;
        }
        if ((Word_SMS(nosaukums_konstante, "rādīt_logs") || Word_SMS(nosaukums_konstante, "Aizvērt")) && Word_SMS(서술상수, "()V")) {
            boolean redzamība_VALUE = Word_SMS(nosaukums_konstante, "rādīt_logs"); int elements_VALUE = 빼기(2); if (!화면객체(elements_VALUE)) return;
            if (lietotājs.화면연결(redzamība_VALUE ? 3 : 4, kaudze_VALUE[elements_VALUE + 2], redzamība_VALUE ? 1 : 0, 0, 0, 0) < 0) { kļūme_VALUE("화면은 대화형 명령에서 실행해야 합니다"); return; }
            kaudze_VALUE[elements_VALUE + 9] = redzamība_VALUE ? 1 : 0; return;
        }
        if (Word_SMS(nosaukums_konstante, "보이는가") && Word_SMS(서술상수, "()Z")) { int elements_VALUE = 빼기(2); if (화면객체(elements_VALUE)) 넣기(kaudze_VALUE[elements_VALUE + 9], 1); return; }
        kļūme_VALUE("지원하지 않는 Latviešu 화면 metode_VALUE");
    }
    static void 화면호출(int īpašnieks, int nosaukums_konstante, int 서술상수, int komanda_CODE) {
        if (Word_SMS(īpašnieks, "javax/swing/SwingUtilities")) {
            if (komanda_CODE == 184 && Word_SMS(nosaukums_konstante, "invokeLater") && Word_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int objekts_Uzziņas = 빼기(2); if (!객체유효(objekts_Uzziņas)) return; if (나중수 == 8) { kļūme_VALUE("invokeLater queue full"); return; } 나중실행[나중수++] = objekts_Uzziņas; return; }
            if (komanda_CODE == 184 && Word_SMS(nosaukums_konstante, "isEventDispatchThread") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            kļūme_VALUE("unsupported SwingUtilities method"); return;
        }
        if (Word_SMS(īpašnieks, "java/awt/event/ActionEvent")) {
            int objekts_Uzziņas = 빼기(2); if (!objekts_VALUE(objekts_Uzziņas, 29)) return;
            if (Word_SMS(nosaukums_konstante, "getSource") && Word_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(kaudze_VALUE[objekts_Uzziņas + 2], 2);
            else if (Word_SMS(nosaukums_konstante, "getActionCommand") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(kaudze_VALUE[objekts_Uzziņas + 2]), 2);
            else if (Word_SMS(nosaukums_konstante, "getID") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else kļūme_VALUE("unsupported ActionEvent method"); return;
        }
        if (komanda_CODE == 183 && Word_SMS(nosaukums_konstante, "<init>")) {
            int COLUMNS = 0, SMS_Uzziņas = 0;
            if (Word_SMS(서술상수, "(I)V")) COLUMNS = 빼기(1);
            else if (Word_SMS(서술상수, "(Ljava/lang/String;I)V")) { COLUMNS = 빼기(1); SMS_Uzziņas = 빼기(2); }
            else if (Word_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_Uzziņas = 빼기(2);
            else if (Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_SMS(서술상수, "()V")) { kļūme_VALUE("unsupported Swing constructor"); return; }
            int objekts_Uzziņas = 빼기(2); if (!객체유효(objekts_Uzziņas)) return;
            if (kaudze_VALUE[objekts_Uzziņas] == 30) { kļūme_VALUE("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(objekts_Uzziņas) || COLUMNS < 0) return;
            int konts_VALUE = lietotājs.화면연결(0, kaudze_VALUE[objekts_Uzziņas] - 23, 0, 0, 0, 0);
            if (konts_VALUE < 1 || konts_VALUE > 32) { kļūme_VALUE("GUI widget slots exhausted"); return; }
            kaudze_VALUE[objekts_Uzziņas + 2] = konts_VALUE; 화면참조[konts_VALUE - 1] = objekts_Uzziņas; kaudze_VALUE[objekts_Uzziņas + 5] = kaudze_VALUE[objekts_Uzziņas] == 24 ? 130 : 16; kaudze_VALUE[objekts_Uzziņas + 6] = kaudze_VALUE[objekts_Uzziņas] == 24 ? 110 : 16;
            kaudze_VALUE[objekts_Uzziņas + 7] = kaudze_VALUE[objekts_Uzziņas] == 24 ? 380 : 220; kaudze_VALUE[objekts_Uzziņas + 8] = kaudze_VALUE[objekts_Uzziņas] == 24 ? 240 : 28; kaudze_VALUE[objekts_Uzziņas + 10] = 1;
            화면문자설정(objekts_Uzziņas, SMS_Uzziņas); return;
        }
        if (Word_SMS(nosaukums_konstante, "setText") || Word_SMS(nosaukums_konstante, "setTitle")) { int SMS_Uzziņas = 빼기(2), objekts_Uzziņas = 빼기(2); if (화면객체(objekts_Uzziņas) && Word_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(objekts_Uzziņas, SMS_Uzziņas); return; }
        if (Word_SMS(nosaukums_konstante, "getText") || Word_SMS(nosaukums_konstante, "getTitle")) { int objekts_Uzziņas = 빼기(2); if (화면객체(objekts_Uzziņas) && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(objekts_Uzziņas), 2); return; }
        if (Word_SMS(nosaukums_konstante, "addActionListener") && Word_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int saņemt_Uzziņas = 빼기(2), objekts_Uzziņas = 빼기(2); if (화면객체(objekts_Uzziņas)) { kaudze_VALUE[objekts_Uzziņas + 4] = saņemt_Uzziņas; kaudze_Uzziņas[objekts_Uzziņas + 4] = 1; } return; }
        if (Word_SMS(nosaukums_konstante, "getContentPane") && Word_SMS(서술상수, "()Ljava/awt/Container;")) { int objekts_Uzziņas = 빼기(2); if (화면객체(objekts_Uzziņas)) 넣기(objekts_Uzziņas, 2); return; }
        if (Word_SMS(nosaukums_konstante, "setLayout") && Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int shēma_Uzziņas = 빼기(2), objekts_Uzziņas = 빼기(2); if (화면객체(objekts_Uzziņas) && shēma_Uzziņas != 0) kļūme_VALUE("only absolute layout (null) is supported"); return; }
        if (Word_SMS(nosaukums_konstante, "add") && (Word_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean shēma_nosacījums = Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (shēma_nosacījums) 빼기(2);
            int bērns_Uzziņas = 빼기(2), objekts_Uzziņas = 빼기(2); if (!화면객체(bērns_Uzziņas) || !화면객체(objekts_Uzziņas)) return;
            if (lietotājs.화면연결(2, kaudze_VALUE[objekts_Uzziņas + 2], kaudze_VALUE[bērns_Uzziņas + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            kaudze_VALUE[bērns_Uzziņas + 11] = objekts_Uzziņas; kaudze_Uzziņas[bērns_Uzziņas + 11] = 1; if (!shēma_nosacījums) 넣기(bērns_Uzziņas, 2); return;
        }
        if (Word_SMS(nosaukums_konstante, "setBounds") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), x_koordināta = 빼기(1), objekts_Uzziņas = 빼기(2); if (!화면객체(objekts_Uzziņas)) return;
            if (lietotājs.화면연결(1, kaudze_VALUE[objekts_Uzziņas + 2], x_koordināta, 세로좌표, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            kaudze_VALUE[objekts_Uzziņas + 5] = x_koordināta; kaudze_VALUE[objekts_Uzziņas + 6] = 세로좌표; kaudze_VALUE[objekts_Uzziņas + 7] = 너비; kaudze_VALUE[objekts_Uzziņas + 8] = 높이; return;
        }
        if (Word_SMS(nosaukums_konstante, "setSize") && Word_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), objekts_Uzziņas = 빼기(2); if (!화면객체(objekts_Uzziņas)) return;
            if (lietotājs.화면연결(1, kaudze_VALUE[objekts_Uzziņas + 2], kaudze_VALUE[objekts_Uzziņas + 5], kaudze_VALUE[objekts_Uzziņas + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { kaudze_VALUE[objekts_Uzziņas + 7] = 너비; kaudze_VALUE[objekts_Uzziņas + 8] = 높이; } return;
        }
        if (Word_SMS(nosaukums_konstante, "setLocationRelativeTo") && Word_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), objekts_Uzziņas = 빼기(2); if (!화면객체(objekts_Uzziņas)) return; if (상대배치 != 0) { kļūme_VALUE("only screen centering supported"); return; } kaudze_VALUE[objekts_Uzziņas + 5] = (lietotājs.화면너비() - kaudze_VALUE[objekts_Uzziņas + 7]) / 2; kaudze_VALUE[objekts_Uzziņas + 6] = (lietotājs.화면높이() - kaudze_VALUE[objekts_Uzziņas + 8]) / 2; lietotājs.화면연결(1, kaudze_VALUE[objekts_Uzziņas + 2], kaudze_VALUE[objekts_Uzziņas + 5], kaudze_VALUE[objekts_Uzziņas + 6], kaudze_VALUE[objekts_Uzziņas + 7], kaudze_VALUE[objekts_Uzziņas + 8]); return; }
        if (Word_SMS(nosaukums_konstante, "setDefaultCloseOperation") && Word_SMS(서술상수, "(I)V")) { int politika = 빼기(1), objekts_Uzziņas = 빼기(2); if (화면객체(objekts_Uzziņas)) { if (politika < 0 || politika > 3) 예외던짐(9, "close policy"); else { kaudze_VALUE[objekts_Uzziņas + 10] = politika; lietotājs.화면연결(7, kaudze_VALUE[objekts_Uzziņas + 2], politika, 0, 0, 0); } } return; }
        if (Word_SMS(nosaukums_konstante, "setVisible") && Word_SMS(서술상수, "(Z)V")) { int dati_VALUE = 빼기(1), objekts_Uzziņas = 빼기(2); if (화면객체(objekts_Uzziņas)) { int 처리값 = lietotājs.화면연결(3, kaudze_VALUE[objekts_Uzziņas + 2], dati_VALUE, 0, 0, 0); if (처리값 < 0) kļūme_VALUE("Swing requires a standalone interactive command"); else kaudze_VALUE[objekts_Uzziņas + 9] = dati_VALUE; } return; }
        if (Word_SMS(nosaukums_konstante, "dispose") && Word_SMS(서술상수, "()V")) { int objekts_Uzziņas = 빼기(2); if (화면객체(objekts_Uzziņas)) { lietotājs.화면연결(4, kaudze_VALUE[objekts_Uzziņas + 2], 0, 0, 0, 0); kaudze_VALUE[objekts_Uzziņas + 9] = 0; } return; }
        if (Word_SMS(nosaukums_konstante, "repaint") || Word_SMS(nosaukums_konstante, "validate")) { int objekts_Uzziņas = 빼기(2); if (!화면객체(objekts_Uzziņas) || !Word_SMS(서술상수, "()V")) return; lietotājs.화면연결(1, kaudze_VALUE[objekts_Uzziņas + 2], kaudze_VALUE[objekts_Uzziņas + 5], kaudze_VALUE[objekts_Uzziņas + 6], kaudze_VALUE[objekts_Uzziņas + 7], kaudze_VALUE[objekts_Uzziņas + 8]); return; }
        if (Word_SMS(nosaukums_konstante, "isVisible") && Word_SMS(서술상수, "()Z")) { int objekts_Uzziņas = 빼기(2); if (화면객체(objekts_Uzziņas)) 넣기(kaudze_VALUE[objekts_Uzziņas + 9], 1); return; }
        kļūme_VALUE("unsupported Swing method (native subset)");
    }
    static void nosūtīt_notikums(int mērķis_adrese, int notikums_numurs, boolean Latviešu) {
        if (mērķis_adrese < 1 || kaudze_VALUE[mērķis_adrese] < 32) { kļūme_VALUE("Java event listener required"); return; }
        int Fails_INDEX = nosaukums_metode(kaudze_VALUE[mērķis_adrese] - 32, notikums_numurs == 0 ? (Latviešu ? "Izpildīt" : "run") : (Latviešu ? "saņemt_darbība" : "actionPerformed"), notikums_numurs == 0 ? "()V" : (Latviešu ? "(LLatviešu/savs/darbība_informēšana;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (Fails_INDEX < 0) { kļūme_VALUE("event callback missing"); return; }
        pašreizējais_saruna = 0; saruna_COUNT = 1; kadrs_INDEX = 0; saruna_Statuss[0] = 1; kadrs_kopa[0] = 0; kadrs_bloķēt[0] = 틀초기화[0] = 0; mainīt_pieprasījums = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 128; Loop_INDEX++) { vietējs_VALUE[Loop_INDEX] = vietējs_TYPE[Loop_INDEX] = 0; }
        kadrs_metode[0] = Fails_INDEX; kadrs_amats[0] = metode_Sākt[Fails_INDEX]; vietējs_VALUE[0] = mērķis_adrese; vietējs_TYPE[0] = 2;
        if (notikums_numurs != 0) { vietējs_VALUE[1] = notikums_numurs; vietējs_TYPE[1] = 2; }
        사건중 = true; Izpildīt_komanda(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!Kļūda) {
            if (나중수 > 0) { int mērķis_adrese = 나중실행[0], Latviešu = 나중한국어[0]; for (int Loop_INDEX = 1; Loop_INDEX < 나중수; Loop_INDEX++) { 나중실행[Loop_INDEX - 1] = 나중실행[Loop_INDEX]; 나중한국어[Loop_INDEX - 1] = 나중한국어[Loop_INDEX]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; nosūtīt_notikums(mērķis_adrese, 0, Latviešu != 0); continue; }
            if (lietotājs.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int notikums_numurs = lietotājs.화면연결(5, 0, 0, 0, 0, 0); if (notikums_numurs == 0) continue;
            if (notikums_numurs < 0) { kļūme_VALUE("GUI event I/O failed"); return; }
            int konts_VALUE = notikums_numurs & 65535; if (konts_VALUE < 1 || konts_VALUE > 32) continue; int objekts_Uzziņas = 화면참조[konts_VALUE - 1]; if (objekts_Uzziņas == 0) continue;
            if ((notikums_numurs & 65536) != 0) {
                if (kaudze_VALUE[objekts_Uzziņas + 10] != 0) kaudze_VALUE[objekts_Uzziņas + 9] = 0;
                if (kaudze_VALUE[objekts_Uzziņas + 10] == 3) for (int Loop_INDEX = 0; Loop_INDEX < 32; Loop_INDEX++) if (화면참조[Loop_INDEX] != 0 && kaudze_VALUE[화면참조[Loop_INDEX]] == 24) lietotājs.화면연결(4, Loop_INDEX + 1, 0, 0, 0, 0);
            } else if (kaudze_VALUE[objekts_Uzziņas + 4] != 0) {
                int fails_Lasi_mani_Uzziņas = piešķirt_Krātuve(29, 2); if (Kļūda) return; kaudze_VALUE[fails_Lasi_mani_Uzziņas + 2] = objekts_Uzziņas; kaudze_VALUE[fails_Lasi_mani_Uzziņas + 3] = kaudze_VALUE[objekts_Uzziņas + 12]; kaudze_Uzziņas[fails_Lasi_mani_Uzziņas + 2] = 1; nosūtīt_notikums(kaudze_VALUE[objekts_Uzziņas + 4], fails_Lasi_mani_Uzziņas, kaudze_VALUE[objekts_Uzziņas + 12] != 0);
            }
        }
    }
    public static int Palaist() {
        if (lietotājs.인수개수() == 1 && 자바도구.같음(lietotājs.Parametri(0), "-version")) {
            lietotājs.Rakstīt("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (lietotājs.인수개수() < 1) { lietotājs.Rakstīt("Usage: java CLASS [ARGS]\n"); return 2; }
        ievade_klase_definīcija = ielāde_klase_definīcija(viesot_rakstzīme(lietotājs.Parametri(0))); if (Kļūda || ievade_klase_definīcija < 0) return 1;
        int ieejas_punkts_VALUE = nosaukums_metode(ievade_klase_definīcija, "Palaist", "()V");
        boolean 한국어진입 = ieejas_punkts_VALUE >= 0 && (metode_piekļūt[ieejas_punkts_VALUE] & 9) == 9;
        if (!한국어진입) ieejas_punkts_VALUE = nosaukums_metode(ievade_klase_definīcija, "main", "([Ljava/lang/String;)V");
        if (ieejas_punkts_VALUE < 0 || (metode_piekļūt[ieejas_punkts_VALUE] & 9) != 9) kļūme_VALUE("public static void Palaist() or main(String[] args) required");
        if (Kļūda) return 1;
        int Parametri = piešķirt_Krātuve(3, lietotājs.인수개수() - 1); masīva_elements[Parametri] = -1;
        for (int numurs = 1; numurs < lietotājs.인수개수() && !Kļūda; numurs++) kaudze_VALUE[Parametri + 1 + numurs] = viesot_rakstzīme(lietotājs.Parametri(numurs));
        kadrs_INDEX = 0; kadrs_metode[0] = ieejas_punkts_VALUE; kadrs_amats[0] = metode_Sākt[ieejas_punkts_VALUE]; vietējs_VALUE[0] = 한국어진입 ? 0 : Parametri; vietējs_TYPE[0] = 한국어진입 ? 0 : 2;
        saruna_Statuss[0] = 1; saruna_objekts[0] = piešķirt_Krātuve(13, 2);
        Izpildīt_komanda(); if (!Kļūda) 화면사건들(); return Kļūda ? 1 : 0;
    }
}
