// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Fail/operand_Virn/viide/haru 경계를 Täida_käsk 중 검사한다. */
public final class 자바가상기계 {
    static int[] Fail = new int[16 * 16384], ajutine_fail = new int[16384], failinimi_SMS = new int[512];
    static int[] konstant_silt = new int[8192], 상가 = new int[8192], konstant_SECOND_VALUE = new int[8192], string_viide = new int[8192];
    static int[] meetod_nimetus_SMS = new int[512], meetod_TYPE = new int[512], meetod_pöördus = new int[512], meetod_omanik = new int[512];
    static int[] meetod_START = new int[512], meetod_lõpeta_kõne = new int[512], meetod_Virn = new int[512], 함수지역 = new int[512];
    static int[] meetod_argument_COUNT = new int[512], meetod_argument_TYPE = new int[8192], meetod_tagasi_saatma = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] kohalik_VALUE = new int[16384], kohalik_TYPE = new int[16384], operand_Virn_VALUE = new int[16384], operand_Virn_TYPE = new int[16384];
    static int[] raam_meetod = new int[128], raam_ametikoht = new int[128], raam_Virn = new int[128], 틀명령 = new int[128], 틀초기화 = new int[128];
    static int[] tund_Sõnaseletus_nimetus = new int[16], tund_Sõnaseletus_suurust_muutma = new int[16], tund_Sõnaseletus_ema = new int[16], tund_Sõnaseletus_Olek = new int[16], 종칸수 = new int[16], 종초기화 = new int[16];
    static int[] tund_liides = new int[16 * 16], tund_liides_COUNT = new int[16];
    static int[] 칸이름 = new int[512], 칸형 = new int[512], 칸주인 = new int[512], 칸권한 = new int[512], 칸위치 = new int[512], 칸값 = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], massiivi_element = new int[32768], salv_täisarv = new int[256];
    static int Suurus, 읽기위치, meetod_COUNT, klassinimi, raam_INDEX = -1, 힙끝 = 1, tagasi_saatma_TYPE;
    static int tund_Sõnaseletus_COUNT, 칸수, 잡기수, 현재읽는종, 던진객체, 잠시수, ekraan_COUNT, kogu_COUNT;
    static int tähtaja_piires_lõim, lõim_COUNT = 1, kirje_tund_Sõnaseletus;
    static int[] lõim_raam = new int[4], lõim_Olek = new int[4], lõim_objekt = new int[4], lõim_siht = new int[4], 가닥대기 = new int[4];
    static boolean VIGA, muutma_päring;
    static int[] lukk_omanik = new int[32768], 잠금깊이 = new int[32768], raam_lukk = new int[128], tund_lukk = new int[16], tund_lõim = new int[16];

    static void tõrge_VALUE(String Word_SMS) {
        if (VIGA) return;
        int ala_CODE = 0;
        if (자바도구.같음(Word_SMS, "ArithmeticException: / by zero")) ala_CODE = 4;
        if (자바도구.같음(Word_SMS, "NullPointerException") || 자바도구.같음(Word_SMS, "null or invalid array")) ala_CODE = 5;
        if (자바도구.같음(Word_SMS, "ArrayIndexOutOfBoundsException")) ala_CODE = 7;
        if (자바도구.같음(Word_SMS, "StringIndexOutOfBoundsException")) ala_CODE = 8;
        if (자바도구.같음(Word_SMS, "NumberFormatException")) ala_CODE = 10;
        if (자바도구.같음(Word_SMS, "FileNotFoundException: file open failed")) ala_CODE = 12;
        if (자바도구.같음(Word_SMS, "IOException: stream closed") || 자바도구.같음(Word_SMS, "IOException: read failed") || 자바도구.같음(Word_SMS, "IOException: write failed")) ala_CODE = 11;
        if (자바도구.같음(Word_SMS, "ClassCastException")) ala_CODE = 14;
        if (자바도구.같음(Word_SMS, "NegativeArraySizeException")) ala_CODE = 15;
        if (ala_CODE != 0 && raam_INDEX >= 0) { 예외던짐(ala_CODE, Word_SMS); return; }
        kasutaja.Kirjutamine("JVM error: "); kasutaja.Kirjutamine(Word_SMS); kasutaja.kirjutamine_märk_VALUE(10); VIGA = true;
    }
    static boolean klipp(int Käivita_2, int 길이) {
        if (Käivita_2 < 0 || Käivita_2 >= Fail.length || 길이 < 0) return false;
        int tund_Sõnaseletus = Käivita_2 / 16384;
        return Käivita_2 % 16384 <= tund_Sõnaseletus_suurust_muutma[tund_Sõnaseletus] && 길이 <= tund_Sõnaseletus_suurust_muutma[tund_Sõnaseletus] - Käivita_2 % 16384;
    }
    static int bait_VALUE() {
        if (!klipp(읽기위치, 1)) { tõrge_VALUE("truncated class file"); return 0; }
        return Fail[읽기위치++];
    }
    static int 짧은수() { return bait_VALUE() << 8 | bait_VALUE(); }
    static int täisarv() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int 길이) { if (!klipp(읽기위치, 길이)) tõrge_VALUE("invalid attribute size"); else 읽기위치 += 길이; }
    static boolean tšekk_konstant(int number, int 종류) {
        if (number <= 0 || number >= konstant_silt.length || konstant_silt[number] != 종류) { tõrge_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_vahemik(int Käivita_2, int 길이, String Word_SMS) {
        if (!klipp(Käivita_2, 길이)) return false;
        int 읽는자리 = Käivita_2, 끝 = Käivita_2 + 길이;
        for (int Loop_INDEX = 0; Loop_INDEX < Word_SMS.length(); Loop_INDEX++) {
            int koodipunkt = Word_SMS.charAt(Loop_INDEX);
            if (koodipunkt > 0 && koodipunkt < 128) { if (읽는자리 >= 끝 || Fail[읽는자리++] != koodipunkt) return false; }
            else if (koodipunkt < 2048) {
                if (읽는자리 + 2 > 끝 || Fail[읽는자리++] != (192 | (koodipunkt >> 6)) || Fail[읽는자리++] != (128 | (koodipunkt & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Fail[읽는자리++] != (224 | (koodipunkt >> 12)) || Fail[읽는자리++] != (128 | ((koodipunkt >> 6) & 63)) || Fail[읽는자리++] != (128 | (koodipunkt & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean Word_SMS(int konstant_VALUE, String Word_SMS) { return tšekk_konstant(konstant_VALUE, 1) && SMS_vahemik(상가[konstant_VALUE], konstant_SECOND_VALUE[konstant_VALUE], Word_SMS); }
    static boolean 같은말(int 가, int SECOND_operand) {
        if (!tšekk_konstant(가, 1) || !tšekk_konstant(SECOND_operand, 1) || konstant_SECOND_VALUE[가] != konstant_SECOND_VALUE[SECOND_operand]) return false;
        for (int number = 0; number < konstant_SECOND_VALUE[가]; number++) if (Fail[상가[가] + number] != Fail[상가[SECOND_operand] + number]) return false;
        return true;
    }
    static int klassinimi_SMS(int number) { return tšekk_konstant(number, 7) && tšekk_konstant(상가[number], 1) ? 상가[number] : 0; }
    static int viide_nimetus(int number) { return tšekk_konstant(number, 12) && tšekk_konstant(상가[number], 1) ? 상가[number] : 0; }
    static int viide_TYPE(int number) { return tšekk_konstant(number, 12) && tšekk_konstant(konstant_SECOND_VALUE[number], 1) ? konstant_SECOND_VALUE[number] : 0; }
    static int 서술형(int 끝, boolean 빈형) {
        if (읽기위치 >= 끝) { tõrge_VALUE("invalid descriptor"); return 0; }
        int VALUE = bait_VALUE();
        if (VALUE == 'V' && 빈형) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int Käivita_2 = 읽기위치;
            while (읽기위치 < 끝 && Fail[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Käivita_2) tõrge_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        tõrge_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int FUNCTION_VALUE) {
        int 이전 = 읽기위치, number = meetod_TYPE[FUNCTION_VALUE];
        if (!tšekk_konstant(number, 1)) return;
        읽기위치 = 상가[number]; int 끝 = 읽기위치 + konstant_SECOND_VALUE[number];
        if (bait_VALUE() != '(') tõrge_VALUE("invalid method descriptor");
        int kaup_COUNT = 0;
        while (!VIGA && 읽기위치 < 끝 && Fail[읽기위치] != ')') {
            if (kaup_COUNT == 16) { tõrge_VALUE("too many method arguments"); break; }
            meetod_argument_TYPE[FUNCTION_VALUE * 16 + kaup_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || bait_VALUE() != ')') tõrge_VALUE("invalid method descriptor");
        meetod_tagasi_saatma[FUNCTION_VALUE] = 서술형(끝, true); meetod_argument_COUNT[FUNCTION_VALUE] = kaup_COUNT;
        if (읽기위치 != 끝) tõrge_VALUE("invalid method descriptor");
        읽기위치 = 이전;
    }
    static int 상번호() { int VALUE = 짧은수(); return VALUE == 0 ? 0 : 현재읽는종 * 512 + VALUE; }
    static int 명상수() { return meetod_omanik[raam_meetod[raam_INDEX]] * 512 + 명짧(); }
    static void 속성건너() {
        int kaup_COUNT = 짧은수();
        for (int number = 0; number < kaup_COUNT && !VIGA; number++) { tšekk_konstant(상번호(), 1); 건너(täisarv()); }
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
    static int ametikoht_täisarv(int 읽는자리) {
        if (!klipp(읽는자리, 4)) { tõrge_VALUE("truncated bytecode operand"); return 0; }
        return Fail[읽는자리] << 24 | Fail[읽는자리 + 1] << 16 | Fail[읽는자리 + 2] << 8 | Fail[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Käivita_2, int 끝) {
        int VALUE = Fail[읽는자리], 길이 = 명령길이(VALUE);
        if (VALUE == 170 || VALUE == 171) {
            int BASE_ametikoht = 읽는자리 + 1;
            while ((BASE_ametikoht - Käivita_2) % 4 != 0) BASE_ametikoht++;
            if (끝 - BASE_ametikoht < (VALUE == 170 ? 12 : 8)) return 0;
            int kirje_COUNT = VALUE == 170 ? ametikoht_täisarv(BASE_ametikoht + 8) - ametikoht_täisarv(BASE_ametikoht + 4) + 1 : ametikoht_täisarv(BASE_ametikoht + 4);
            if (kirje_COUNT < 0 || kirje_COUNT > 2048) return 0;
            길이 = BASE_ametikoht - 읽는자리 + (VALUE == 170 ? 12 + 4 * kirje_COUNT : 8 + 8 * kirje_COUNT);
        }
        if (VALUE == 196 && 읽는자리 + 1 < 끝) {
            int Word_andmed = Fail[읽는자리 + 1]; 길이 = Word_andmed == 132 ? 6 : (Word_andmed == 21 || Word_andmed == 25 || Word_andmed == 54 || Word_andmed == 58) ? 4 : 0;
        }
        return 길이 > 0 && 길이 <= 끝 - 읽는자리 ? 길이 : 0;
    }
    static void tšekk_sihtkoht_VALUE(int sihtkoht_VALUE, int FUNCTION_VALUE) {
        if (sihtkoht_VALUE < meetod_START[FUNCTION_VALUE] || sihtkoht_VALUE >= meetod_lõpeta_kõne[FUNCTION_VALUE] || 경계[sihtkoht_VALUE] != FUNCTION_VALUE + 1) tõrge_VALUE("invalid branch target");
    }
    static void 클래스읽기(int tund_Sõnaseletus) {
        현재읽는종 = tund_Sõnaseletus; 읽기위치 = tund_Sõnaseletus * 16384; Suurus = 읽기위치 + tund_Sõnaseletus_suurust_muutma[tund_Sõnaseletus];
        if (täisarv() != 0xcafebabe) { tõrge_VALUE("not a class file"); return; }
        int 부판 = 짧은수(), versioon_VALUE = 짧은수();
        if (versioon_VALUE < 45 || versioon_VALUE > 52 || 부판 != 0) { tõrge_VALUE("supported class versions: 45..52, minor 0"); return; }
        int konstant_COUNT = 짧은수(), BASE_ametikoht = tund_Sõnaseletus * 512;
        if (konstant_COUNT < 1 || konstant_COUNT > 512) { tõrge_VALUE("constant pool limit (511)"); return; }
        for (int kirje_COUNT = 1; kirje_COUNT < konstant_COUNT && !VIGA; kirje_COUNT++) {
            int number = BASE_ametikoht + kirje_COUNT, 종류 = bait_VALUE(); konstant_silt[number] = 종류;
            if (종류 == 1) { konstant_SECOND_VALUE[number] = 짧은수(); 상가[number] = 읽기위치; 건너(konstant_SECOND_VALUE[number]); }
            else if (종류 == 3) 상가[number] = täisarv();
            else if (종류 == 7 || 종류 == 8) 상가[number] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[number] = 상번호(); konstant_SECOND_VALUE[number] = 상번호(); }
            else tõrge_VALUE("unsupported constant type");
        }
        int luba_VALUE = 짧은수();
        if ((luba_VALUE & (0x2000 | 0x4000)) != 0) tõrge_VALUE("annotation/enum class unsupported");
        tund_Sõnaseletus_nimetus[tund_Sõnaseletus] = klassinimi_SMS(상번호());
        tund_Sõnaseletus_ema[tund_Sõnaseletus] = klassinimi_SMS(상번호());
        int liides_COUNT = 짧은수(); if (liides_COUNT > 16) { tõrge_VALUE("interface count limit"); return; }
        tund_liides_COUNT[tund_Sõnaseletus] = liides_COUNT;
        for (int Loop_INDEX = 0; Loop_INDEX < liides_COUNT; Loop_INDEX++) tund_liides[tund_Sõnaseletus * 16 + Loop_INDEX] = klassinimi_SMS(상번호());
        int väli_COUNT = 짧은수();
        if (väli_COUNT > 512 - 칸수) { tõrge_VALUE("field count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < väli_COUNT && !VIGA; Loop_INDEX++) {
            int Fail_INDEX = 칸수++; 칸주인[Fail_INDEX] = tund_Sõnaseletus; 칸권한[Fail_INDEX] = 짧은수(); 칸이름[Fail_INDEX] = 상번호(); 칸형[Fail_INDEX] = 상번호();
            tšekk_konstant(칸이름[Fail_INDEX], 1); tšekk_konstant(칸형[Fail_INDEX], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[칸형[Fail_INDEX]]; int ala_CODE = 서술형(읽기위치 + konstant_SECOND_VALUE[칸형[Fail_INDEX]], false); 읽기위치 = 보존값;
            if ((칸권한[Fail_INDEX] & 8) == 0) 칸위치[Fail_INDEX] = 종칸수[tund_Sõnaseletus]++;
            int atribuut_andmed = 짧은수();
            for (int sisemine_ametikoht = 0; sisemine_ametikoht < atribuut_andmed && !VIGA; sisemine_ametikoht++) {
                int nimetus_konstant = 상번호(), 유효길이 = täisarv();
                if (Word_SMS(nimetus_konstant, "ConstantValue") && 유효길이 == 2) {
                    int andmed_VALUE = 상번호();
                    if (ala_CODE == 1 && tšekk_konstant(andmed_VALUE, 3)) 칸값[Fail_INDEX] = 상가[andmed_VALUE];
                    else if (ala_CODE == 2 && tšekk_konstant(andmed_VALUE, 8)) 칸값[Fail_INDEX] = konstant_SMS(상가[andmed_VALUE]);
                } else 건너(유효길이);
            }
        }
        int kaup_COUNT = 짧은수();
        if (kaup_COUNT > 512 - meetod_COUNT) { tõrge_VALUE("method count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < kaup_COUNT && !VIGA; Loop_INDEX++) {
            int number = meetod_COUNT++; meetod_omanik[number] = tund_Sõnaseletus;
            meetod_pöördus[number] = 짧은수(); meetod_nimetus_SMS[number] = 상번호(); meetod_TYPE[number] = 상번호();
            tšekk_konstant(meetod_nimetus_SMS[number], 1); 서술읽기(number);
            if ((meetod_pöördus[number] & 8) == 0) {
                if (meetod_argument_COUNT[number] == 16) { tõrge_VALUE("too many instance method arguments"); return; }
                for (int Võrdlus_ametikoht = meetod_argument_COUNT[number]; Võrdlus_ametikoht > 0; Võrdlus_ametikoht--) meetod_argument_TYPE[number * 16 + Võrdlus_ametikoht] = meetod_argument_TYPE[number * 16 + Võrdlus_ametikoht - 1];
                meetod_argument_TYPE[number * 16] = 2; meetod_argument_COUNT[number]++;
            }
            if ((meetod_pöördus[number] & 0x100) != 0) tõrge_VALUE("user native method unsupported");
            if (Word_SMS(meetod_nimetus_SMS[number], "<clinit>")) 종초기화[tund_Sõnaseletus] = number + 1;
            for (int esikaamera_VALUE = 0; esikaamera_VALUE < number; esikaamera_VALUE++) if (meetod_omanik[esikaamera_VALUE] == tund_Sõnaseletus && 같은말(meetod_nimetus_SMS[esikaamera_VALUE], meetod_nimetus_SMS[number]) && 같은말(meetod_TYPE[esikaamera_VALUE], meetod_TYPE[number])) tõrge_VALUE("duplicate method");
            int atribuut_COUNT = 짧은수();
            for (int atribuut_VALUE = 0; atribuut_VALUE < atribuut_COUNT && !VIGA; atribuut_VALUE++) {
                int Nimi_2 = 상번호(), 길이 = täisarv(), Käivita_2 = 읽기위치;
                if (!klipp(Käivita_2, 길이)) { tõrge_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Nimi_2, "Code")) {
                    if (meetod_START[number] != 0) tõrge_VALUE("duplicate Code attribute");
                    meetod_Virn[number] = 짧은수(); 함수지역[number] = 짧은수(); int 코드길이 = täisarv();
                    if (meetod_Virn[number] > 128 || 함수지역[number] > 128 || 함수지역[number] < meetod_argument_COUNT[number]
                        || 코드길이 < 1 || 코드길이 > 8192) tõrge_VALUE("method memory limits exceeded");
                    meetod_START[number] = 읽기위치; 건너(코드길이); meetod_lõpeta_kõne[number] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { tõrge_VALUE("exception table limit"); return; }
                    for (int sisemine_ametikoht = 0; sisemine_ametikoht < 잡는수; sisemine_ametikoht++) {
                        int tõrge_viide = 잡기수++; 잡기함수[tõrge_viide] = number;
                        잡기시작[tõrge_viide] = meetod_START[number] + 짧은수(); 잡기끝[tõrge_viide] = meetod_START[number] + 짧은수();
                        잡기위치[tõrge_viide] = meetod_START[number] + 짧은수(); int 부호값 = 상번호(); 잡기종[tõrge_viide] = 부호값 == 0 ? 0 : klassinimi_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != Käivita_2 + 길이) tõrge_VALUE("Code attribute size mismatch");
                } else 건너(길이);
            }
            if ((meetod_pöördus[number] & 0x400) != 0) continue;
            if (meetod_START[number] == 0) tõrge_VALUE("missing Code attribute");
            int 칸 = meetod_START[number];
            while (칸 < meetod_lõpeta_kõne[number] && !VIGA) {
                int 길이 = 길이읽기(칸, meetod_START[number], meetod_lõpeta_kõne[number]);
                if (길이 == 0) { tõrge_VALUE("unsupported or truncated bytecode"); break; }
                경계[칸] = number + 1; 칸 += 길이;
            }
            칸 = meetod_START[number];
            while (칸 < meetod_lõpeta_kõne[number] && !VIGA) {
                int VALUE = Fail[칸];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) tšekk_sihtkoht_VALUE(칸 + (short)(Fail[칸 + 1] << 8 | Fail[칸 + 2]), number);
                if (VALUE == 200) tšekk_sihtkoht_VALUE(칸 + ametikoht_täisarv(칸 + 1), number);
                if (VALUE == 170 || VALUE == 171) {
                    int 읽는자리 = 칸 + 1; while ((읽는자리 - meetod_START[number]) % 4 != 0) 읽는자리++;
                    tšekk_sihtkoht_VALUE(칸 + ametikoht_täisarv(읽는자리), number);
                    int kirje_COUNT = VALUE == 170 ? ametikoht_täisarv(읽는자리 + 8) - ametikoht_täisarv(읽는자리 + 4) + 1 : ametikoht_täisarv(읽는자리 + 4);
                    읽는자리 += VALUE == 170 ? 12 : 8;
                    for (int sisemine_ametikoht = 0; sisemine_ametikoht < kirje_COUNT; sisemine_ametikoht++) tšekk_sihtkoht_VALUE(칸 + ametikoht_täisarv(읽는자리 + sisemine_ametikoht * (VALUE == 170 ? 4 : 8) + (VALUE == 170 ? 0 : 4)), number);
                }
                칸 += 길이읽기(칸, meetod_START[number], meetod_lõpeta_kõne[number]);
            }
            for (int sisemine_ametikoht = 0; sisemine_ametikoht < 잡기수; sisemine_ametikoht++) if (잡기함수[sisemine_ametikoht] == number) {
                tšekk_sihtkoht_VALUE(잡기시작[sisemine_ametikoht], number); tšekk_sihtkoht_VALUE(잡기위치[sisemine_ametikoht], number);
                if (잡기끝[sisemine_ametikoht] != meetod_lõpeta_kõne[number]) tšekk_sihtkoht_VALUE(잡기끝[sisemine_ametikoht], number);
                if (잡기시작[sisemine_ametikoht] >= 잡기끝[sisemine_ametikoht]) tõrge_VALUE("invalid exception range");
            }
        }
        if (!VIGA) 속성건너();
        if (읽기위치 != Suurus) tõrge_VALUE("extra class file data");
    }
    static int lisama_salvesti(int 종류, int 길이) { return 새기억(종류, 길이); }
    static boolean objekt_VALUE(int viide, int 종류) {
        if (!객체유효(viide)) return false;
        if (힙[viide] != 종류) { tõrge_VALUE("object type mismatch"); return false; }
        return true;
    }
    static int konstant_SMS(int INDEX) {
        if (!tšekk_konstant(INDEX, 1)) return 0;
        if (string_viide[INDEX] != 0) return string_viide[INDEX];
        int viide = lisama_salvesti(1, konstant_SECOND_VALUE[INDEX]); if (VIGA) return 0;
        int 끝 = 상가[INDEX] + konstant_SECOND_VALUE[INDEX], number = 상가[INDEX], 길이 = 0;
        while (number < 끝 && !VIGA) {
            int VALUE = Fail[number++];
            if (VALUE == 0) tõrge_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && number < 끝) {
                int Edasi_kaup = Fail[number++];
                if ((Edasi_kaup & 192) != 128) tõrge_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | Edasi_kaup & 63;
                if (VALUE != 0 && VALUE < 128) tõrge_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && number + 1 < 끝) {
                int 가 = Fail[number++], SECOND_operand = Fail[number++];
                if ((가 & 192) != 128 || (SECOND_operand & 192) != 128) tõrge_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | SECOND_operand & 63;
                if (VALUE < 2048) tõrge_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) tõrge_VALUE("invalid modified UTF-8");
            힙[viide + 2 + 길이++] = VALUE;
        }
        힙[viide + 1] = 길이; string_viide[INDEX] = viide; return viide;
    }
    static int host_märk(String VALUE) {
        int viide = lisama_salvesti(1, VALUE.length()); if (VIGA) return 0;
        for (int number = 0; number < VALUE.length(); number++) 힙[viide + 2 + number] = VALUE.charAt(number);
        return viide;
    }
    static void kirjutamine_SMS(int viide) {
        if (viide == 0) { kasutaja.Kirjutamine("null"); return; }
        if (!objekt_VALUE(viide, 1)) return;
        for (int number = 0; number < 힙[viide + 1]; number++) kasutaja.kirjutamine_märk_VALUE(힙[viide + 2 + number]);
    }
    static int number_märk(int VALUE) {
        int viide = lisama_salvesti(1, 11); if (VIGA) return 0;
        int 길이 = 0;
        if (VALUE < 0) 힙[viide + 2 + 길이++] = '-'; else VALUE = -VALUE;
        int asukohaindeks = 1000000000; boolean Käivita_2 = false;
        while (asukohaindeks != 0) {
            int number = -(VALUE / asukohaindeks);
            if (number != 0 || Käivita_2 || asukohaindeks == 1) { 힙[viide + 2 + 길이++] = '0' + number; Käivita_2 = true; }
            VALUE %= asukohaindeks; asukohaindeks /= 10;
        }
        힙[viide + 1] = 길이; return viide;
    }
    static int 정수해독(int viide) {
        if (!objekt_VALUE(viide, 1)) return 0;
        int 길이 = 힙[viide + 1], number = 0, VALUE = 0; boolean 음수 = false;
        if (길이 > 0 && (힙[viide + 2] == '-' || 힙[viide + 2] == '+')) { 음수 = 힙[viide + 2] == '-'; number++; }
        if (number == 길이) tõrge_VALUE("NumberFormatException");
        for (; number < 길이 && !VIGA; number++) {
            int number_VALUE = 힙[viide + 2 + number] - '0';
            if (number_VALUE < 0 || number_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && number_VALUE > (음수 ? 8 : 7)) tõrge_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - number_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int TYPE_VALUE) {
        if (VIGA) return;
        if (raam_INDEX < 0 || raam_Virn[raam_INDEX] >= meetod_Virn[raam_meetod[raam_INDEX]]) { tõrge_VALUE("operand stack overflow"); return; }
        int 칸 = raam_INDEX * 128 + raam_Virn[raam_INDEX]++; operand_Virn_VALUE[칸] = VALUE; operand_Virn_TYPE[칸] = TYPE_VALUE;
    }
    static int 빼기(int TYPE_VALUE) {
        if (VIGA) return 0;
        if (raam_INDEX < 0 || raam_Virn[raam_INDEX] < 1) { tõrge_VALUE("operand stack underflow"); return 0; }
        int 칸 = raam_INDEX * 128 + --raam_Virn[raam_INDEX]; tagasi_saatma_TYPE = operand_Virn_TYPE[칸];
        if (TYPE_VALUE != 0 && tagasi_saatma_TYPE != TYPE_VALUE) tõrge_VALUE("operand type mismatch");
        if (tagasi_saatma_TYPE == 2) kaitsma_VALUE(operand_Virn_VALUE[칸]);
        return operand_Virn_VALUE[칸];
    }
    static void 지역읽기(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[raam_meetod[raam_INDEX]] || INDEX < 0 || kohalik_TYPE[raam_INDEX * 128 + INDEX] != TYPE_VALUE) { tõrge_VALUE("invalid or uninitialized local"); return; }
        넣기(kohalik_VALUE[raam_INDEX * 128 + INDEX], TYPE_VALUE);
    }
    static void kirjutamine_kohalik(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[raam_meetod[raam_INDEX]] || INDEX < 0) { tõrge_VALUE("local index out of range"); return; }
        int VALUE = 빼기(TYPE_VALUE); kohalik_VALUE[raam_INDEX * 128 + INDEX] = VALUE; kohalik_TYPE[raam_INDEX * 128 + INDEX] = TYPE_VALUE;
    }
    static int 명바() {
        int Asukoht = raam_ametikoht[raam_INDEX];
        if (Asukoht < meetod_START[raam_meetod[raam_INDEX]] || Asukoht >= meetod_lõpeta_kõne[raam_meetod[raam_INDEX]]) { tõrge_VALUE("instruction pointer out of range"); return 0; }
        raam_ametikoht[raam_INDEX]++; return Fail[Asukoht];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void liigutama_VALUE(int Asukoht) {
        int FUNCTION_VALUE = raam_meetod[raam_INDEX];
        if (Asukoht < meetod_START[FUNCTION_VALUE] || Asukoht >= meetod_lõpeta_kõne[FUNCTION_VALUE] || 경계[Asukoht] != FUNCTION_VALUE + 1) tõrge_VALUE("invalid branch target");
        else raam_ametikoht[raam_INDEX] = Asukoht;
    }
    static void 호출(int FUNCTION_VALUE) {
        if (raam_INDEX % 32 == 31) { tõrge_VALUE("call stack limit (32)"); return; }
        int Edasi_kaup = raam_INDEX + 1;
        for (int number = 0; number < 128; number++) kohalik_TYPE[Edasi_kaup * 128 + number] = 0;
        for (int number = meetod_argument_COUNT[FUNCTION_VALUE] - 1; number >= 0; number--) {
            kohalik_VALUE[Edasi_kaup * 128 + number] = 빼기(meetod_argument_TYPE[FUNCTION_VALUE * 16 + number]); kohalik_TYPE[Edasi_kaup * 128 + number] = meetod_argument_TYPE[FUNCTION_VALUE * 16 + number];
        }
        if (VIGA) return;
        raam_INDEX = Edasi_kaup; 틀초기화[raam_INDEX] = 0; raam_meetod[raam_INDEX] = FUNCTION_VALUE; raam_ametikoht[raam_INDEX] = meetod_START[FUNCTION_VALUE]; raam_Virn[raam_INDEX] = 0;
    }
    static void tagasi_saatma_näitaja(int TYPE_VALUE) {
        if (TYPE_VALUE != meetod_tagasi_saatma[raam_meetod[raam_INDEX]]) { tõrge_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        if (틀초기화[raam_INDEX] != 0) tund_Sõnaseletus_Olek[틀초기화[raam_INDEX] - 1] = 2;
        if (raam_lukk[raam_INDEX] != 0) { vabastama_lukk(raam_lukk[raam_INDEX]); raam_lukk[raam_INDEX] = 0; }
        raam_INDEX--; if (raam_INDEX >= tähtaja_piires_lõim * 32 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
    }
    static int[] voog_failinimi = new int[64];
    static void Fail_voog_CALL(int omanik_VALUE, int Nimi_2, int vorming_VALUE, int Käsk) {
        boolean Väljund = Word_SMS(omanik_VALUE, "java/io/FileOutputStream");
        int 종류 = Väljund ? 6 : 5;
        if (Käsk == 183 && Word_SMS(Nimi_2, "<init>")) {
            boolean 이어 = false;
            if (Väljund && Word_SMS(vorming_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(vorming_VALUE, "(Ljava/lang/String;)V")) { tõrge_VALUE("unsupported file stream constructor"); return; }
            int Fail_kirje_nimetus = 빼기(2), voog_VALUE = 빼기(2);
            if (!objekt_VALUE(Fail_kirje_nimetus, 1) || !objekt_VALUE(voog_VALUE, 종류) || VIGA) return;
            if (힙[voog_VALUE + 3] != 0) { tõrge_VALUE("file stream already initialized"); return; }
            int 길이 = 힙[Fail_kirje_nimetus + 1];
            if (길이 < 1 || 길이 > 63) { tõrge_VALUE("invalid file name length"); return; }
            for (int 칸 = 0; 칸 < 길이; 칸++) {
                int VALUE = 힙[Fail_kirje_nimetus + 2 + 칸];
                if (VALUE < 1) { tõrge_VALUE("invalid file stream path"); return; }
                voog_failinimi[칸] = VALUE;
            }
            voog_failinimi[길이] = 0;
            int 서술자 = kasutaja.파일서술자열기(voog_failinimi, Väljund ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { tõrge_VALUE("FileNotFoundException: file open failed"); return; }
            힙[voog_VALUE + 2] = 서술자; 힙[voog_VALUE + 3] = 1;
            return;
        }
        if (Käsk != 182) { tõrge_VALUE("invalid file stream invocation"); return; }
        if ((Väljund && Word_SMS(Nimi_2, "write") || !Väljund && Word_SMS(Nimi_2, "read"))
            && (Word_SMS(vorming_VALUE, Väljund ? "([B)V" : "([B)I") || Word_SMS(vorming_VALUE, Väljund ? "([BII)V" : "([BII)I"))) {
            boolean klipp_VALUE = Word_SMS(vorming_VALUE, Väljund ? "([BII)V" : "([BII)I");
            int kirje_COUNT = klipp_VALUE ? 빼기(1) : 0, 시작점 = klipp_VALUE ? 빼기(1) : 0, andmed_ARRAY = 빼기(2), objekt_viide = 빼기(2);
            if (!objekt_VALUE(andmed_ARRAY, 20) || !objekt_VALUE(objekt_viide, 종류)) return;
            if (!klipp_VALUE) kirje_COUNT = 힙[andmed_ARRAY + 1];
            if (시작점 < 0 || kirje_COUNT < 0 || 시작점 > 힙[andmed_ARRAY + 1] - kirje_COUNT) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[objekt_viide + 3] == 0 || 힙[objekt_viide + 2] < 0) { tõrge_VALUE("IOException: stream closed"); return; }
            int Lõpetatud_COUNT = 0;
            while (Lõpetatud_COUNT < kirje_COUNT && !VIGA) {
                int 반환값 = Väljund ? kasutaja.파일한바이트쓰기(힙[objekt_viide + 2], 힙[andmed_ARRAY + 2 + 시작점 + Lõpetatud_COUNT]) : kasutaja.파일한바이트읽기(힙[objekt_viide + 2]);
                if (반환값 < 0) { tõrge_VALUE(Väljund ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!Väljund && 반환값 == 256) break;
                if (!Väljund) 힙[andmed_ARRAY + 2 + 시작점 + Lõpetatud_COUNT] = (byte)반환값;
                Lõpetatud_COUNT++;
            }
            if (!Väljund) 넣기(kirje_COUNT != 0 && Lõpetatud_COUNT == 0 ? -1 : Lõpetatud_COUNT, 1);
            return;
        }
        if (Väljund && Word_SMS(Nimi_2, "flush") && Word_SMS(vorming_VALUE, "()V")) { int objekt_viide = 빼기(2); if (objekt_VALUE(objekt_viide, 종류) && 힙[objekt_viide + 2] < 0) tõrge_VALUE("IOException: stream closed"); return; }
        int Nimi = -1, VALUE = 0;
        if (Word_SMS(Nimi_2, "close") && Word_SMS(vorming_VALUE, "()V")) Nimi = 0;
        if (!Väljund && Word_SMS(Nimi_2, "read") && Word_SMS(vorming_VALUE, "()I")) Nimi = 1;
        if (Väljund && Word_SMS(Nimi_2, "write") && Word_SMS(vorming_VALUE, "(I)V")) { Nimi = 2; VALUE = 빼기(1); }
        if (Nimi < 0) { tõrge_VALUE("unsupported file stream method"); return; }
        int voog_VALUE = 빼기(2);
        if (!objekt_VALUE(voog_VALUE, 종류) || VIGA) return;
        if (힙[voog_VALUE + 3] == 0) { tõrge_VALUE("uninitialized file stream"); return; }
        int 서술자 = 힙[voog_VALUE + 2];
        if (Nimi == 0) {
            if (서술자 >= 0 && kasutaja.파일서술자닫기(서술자) < 0) tõrge_VALUE("IOException: close failed");
            힙[voog_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { tõrge_VALUE("IOException: stream closed"); return; }
        if (Nimi == 1) {
            int TULEMUS = kasutaja.파일한바이트읽기(서술자);
            if (TULEMUS < -1) tõrge_VALUE("IOException: read failed"); else 넣기(TULEMUS == 256 ? -1 : TULEMUS, 1);
        } else if (kasutaja.파일한바이트쓰기(서술자, VALUE) != 1) tõrge_VALUE("IOException: write failed");
    }
    static void CALL_meetod(int INDEX, int Käsk) {
        if (INDEX <= 0 || INDEX >= konstant_silt.length || (konstant_silt[INDEX] != 10 && konstant_silt[INDEX] != 11)) { tõrge_VALUE("invalid method reference"); return; }
        int omanik_VALUE = klassinimi_SMS(상가[INDEX]), Nimi_2 = viide_nimetus(konstant_SECOND_VALUE[INDEX]), vorming_VALUE = viide_TYPE(konstant_SECOND_VALUE[INDEX]);
        if (VIGA) return;
        if (기본호출(omanik_VALUE, Nimi_2, vorming_VALUE, Käsk)) return;
        if (Word_SMS(omanik_VALUE, "java/io/FileInputStream") || Word_SMS(omanik_VALUE, "java/io/FileOutputStream")) {
            Fail_voog_CALL(omanik_VALUE, Nimi_2, vorming_VALUE, Käsk); return;
        }
        if (Käsk == 184 && Word_SMS(omanik_VALUE, "java/lang/Integer") && Word_SMS(Nimi_2, "parseInt") && Word_SMS(vorming_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Käsk == 182 && Word_SMS(omanik_VALUE, "java/io/PrintStream") && (Word_SMS(Nimi_2, "println") || Word_SMS(Nimi_2, "print"))) {
            int TYPE_VALUE = 0, VALUE = 0;
            if (Word_SMS(vorming_VALUE, "(I)V")) { TYPE_VALUE = 1; VALUE = 빼기(1); }
            else if (Word_SMS(vorming_VALUE, "(Z)V")) { TYPE_VALUE = 2; VALUE = 빼기(1); }
            else if (Word_SMS(vorming_VALUE, "(C)V")) { TYPE_VALUE = 3; VALUE = 빼기(1); }
            else if (Word_SMS(vorming_VALUE, "(Ljava/lang/String;)V")) { TYPE_VALUE = 4; VALUE = 빼기(2); }
            else if (!Word_SMS(vorming_VALUE, "()V") || !Word_SMS(Nimi_2, "println")) tõrge_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) tõrge_VALUE("invalid PrintStream receiver");
            if (VIGA) return;
            if (TYPE_VALUE == 1) 자바도구.kirjutamine_number(VALUE);
            if (TYPE_VALUE == 2) kasutaja.Kirjutamine(VALUE == 0 ? "false" : "true");
            if (TYPE_VALUE == 3) kasutaja.kirjutamine_märk_VALUE(VALUE & 65535);
            if (TYPE_VALUE == 4) kirjutamine_SMS(VALUE);
            if (Word_SMS(Nimi_2, "println")) kasutaja.kirjutamine_märk_VALUE(10);
            return;
        }
        if (Käsk == 182 && Word_SMS(omanik_VALUE, "java/lang/String")) {
            if (Word_SMS(Nimi_2, "length") && Word_SMS(vorming_VALUE, "()I")) {
                int viide = 빼기(2); if (objekt_VALUE(viide, 1)) 넣기(힙[viide + 1], 1); return;
            }
            if (Word_SMS(Nimi_2, "charAt") && Word_SMS(vorming_VALUE, "(I)C")) {
                int allindeks_VALUE = 빼기(1), viide = 빼기(2);
                if (objekt_VALUE(viide, 1)) {
                    if (allindeks_VALUE < 0 || allindeks_VALUE >= 힙[viide + 1]) tõrge_VALUE("StringIndexOutOfBoundsException"); else 넣기(힙[viide + 2 + allindeks_VALUE], 1);
                }
                return;
            }
        }
        if (Word_SMS(omanik_VALUE, "java/lang/StringBuilder")) {
            if (Käsk == 183 && Word_SMS(Nimi_2, "<init>") && Word_SMS(vorming_VALUE, "()V")) { objekt_VALUE(빼기(2), 4); return; }
            if (Käsk == 182 && Word_SMS(Nimi_2, "toString") && Word_SMS(vorming_VALUE, "()Ljava/lang/String;")) {
                int viide = 빼기(2); if (objekt_VALUE(viide, 4)) 넣기(힙[viide + 2] == 0 ? host_märk("") : 힙[viide + 2], 2); return;
            }
            if (Käsk == 182 && Word_SMS(Nimi_2, "append")) {
                int Tekst = 0;
                if (Word_SMS(vorming_VALUE, "(I)Ljava/lang/StringBuilder;")) Tekst = number_märk(빼기(1));
                else if (Word_SMS(vorming_VALUE, "(Z)Ljava/lang/StringBuilder;")) Tekst = host_märk(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(vorming_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); Tekst = lisama_salvesti(1, 1); if (!VIGA) 힙[Tekst + 2] = VALUE & 65535;
                }
                else if (Word_SMS(vorming_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Tekst = 빼기(2); if (Tekst == 0) Tekst = host_märk("null"); }
                else { tõrge_VALUE("unsupported StringBuilder append"); return; }
                int viide = 빼기(2); if (!objekt_VALUE(viide, 4) || !objekt_VALUE(Tekst, 1)) return;
                int esikaamera_VALUE = 힙[viide + 2], 앞길이 = esikaamera_VALUE == 0 ? 0 : 힙[esikaamera_VALUE + 1], 뒤길이 = 힙[Tekst + 1];
                int 새글 = lisama_salvesti(1, 앞길이 + 뒤길이); if (VIGA) return;
                for (int number = 0; number < 앞길이; number++) 힙[새글 + 2 + number] = 힙[esikaamera_VALUE + 2 + number];
                for (int number = 0; number < 뒤길이; number++) 힙[새글 + 2 + 앞길이 + number] = 힙[Tekst + 2 + number];
                힙[viide + 2] = 새글; 넣기(viide, 2); return;
            }
        }
        int tund_Sõnaseletus = FIND_tund_Sõnaseletus(omanik_VALUE); if (tund_Sõnaseletus < 0 || VIGA) return;
        int Fail_INDEX = FIND_meetod(tund_Sõnaseletus, Nimi_2, vorming_VALUE);
        if (Fail_INDEX < 0) {
            for (int koodipunkt = tund_Sõnaseletus, kirje_COUNT = 0; koodipunkt >= 0 && kirje_COUNT < 16; kirje_COUNT++, koodipunkt = ema_tund(koodipunkt))
                if (Word_SMS(tund_Sõnaseletus_ema[koodipunkt], "java/lang/Thread")) { 가닥호출(Nimi_2, vorming_VALUE, Käsk); return; }
            tõrge_VALUE("NoSuchMethodError"); return;
        }
        if (((meetod_pöördus[Fail_INDEX] & 8) != 0) != (Käsk == 184)) { tõrge_VALUE("method static/instance mismatch"); return; }
        if (Käsk == 184) { if (!초기화(meetod_omanik[Fail_INDEX], 틀명령[raam_INDEX])) return; }
        else {
            int 읽는자리 = raam_Virn[raam_INDEX] - meetod_argument_COUNT[Fail_INDEX];
            if (읽는자리 < 0 || operand_Virn_TYPE[raam_INDEX * 128 + 읽는자리] != 2) { tõrge_VALUE("invalid method receiver"); return; }
            int objekt_viide = operand_Virn_VALUE[raam_INDEX * 128 + 읽는자리];
            if (!객체유효(objekt_viide)) return;
            if (힙[objekt_viide] < 32 || !종포함(힙[objekt_viide] - 32, omanik_VALUE)) { tõrge_VALUE("method receiver type mismatch"); return; }
            if (Käsk != 183) Fail_INDEX = FIND_meetod(힙[objekt_viide] - 32, Nimi_2, vorming_VALUE);
        }
        if (Fail_INDEX < 0 || (meetod_pöördus[Fail_INDEX] & 0x400) != 0) { tõrge_VALUE("AbstractMethodError"); return; }
        int lukk_viide = 0;
        if ((meetod_pöördus[Fail_INDEX] & 32) != 0) {
            if (Käsk == 184) { int koodipunkt = meetod_omanik[Fail_INDEX]; if (tund_lukk[koodipunkt] == 0) tund_lukk[koodipunkt] = lisama_salvesti(8, 0); lukk_viide = tund_lukk[koodipunkt]; }
            else lukk_viide = operand_Virn_VALUE[raam_INDEX * 128 + raam_Virn[raam_INDEX] - meetod_argument_COUNT[Fail_INDEX]];
            if (!잠금얻기(lukk_viide)) { if (!VIGA) raam_ametikoht[raam_INDEX] = 틀명령[raam_INDEX]; return; }
        }
        호출(Fail_INDEX); if (!VIGA) raam_lukk[raam_INDEX] = lukk_viide;
    }
    static boolean 배열저장가능(int ARRAY_viide, int andmed_VALUE) {
        if (andmed_VALUE == 0 || massiivi_element[ARRAY_viide] == 0) return true;
        boolean 성공여부 = massiivi_element[ARRAY_viide] == -1 ? (andmed_VALUE > 0 && andmed_VALUE < 힙끝 && 힙[andmed_VALUE] == 1) : 맞는객체(andmed_VALUE, massiivi_element[ARRAY_viide]);
        if (!성공여부 && !VIGA) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int 배열칸(int viide, int allindeks_VALUE, int TYPE_VALUE) {
        if (!objekt_VALUE(viide, TYPE_VALUE)) return 0;
        if (allindeks_VALUE < 0 || allindeks_VALUE >= 힙[viide + 1]) { tõrge_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return viide + 2 + allindeks_VALUE;
    }
    static void Täida_käsk() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (VIGA) { if (던진객체 != 0) pide_erand(); if (VIGA || raam_INDEX < tähtaja_piires_lõim * 32) break; }
            if (raam_INDEX < tähtaja_piires_lõim * 32 || muutma_päring || --조각 == 0) { if (!SWITCH_lõim()) break; 조각 = 100; }
            if (raam_INDEX == 0 && tund_Sõnaseletus_Olek[kirje_tund_Sõnaseletus] != 2 && !초기화(kirje_tund_Sõnaseletus, raam_ametikoht[raam_INDEX])) continue;
            if (raam_INDEX == tähtaja_piires_lõim * 32 && tähtaja_piires_lõim != 0 && (meetod_pöördus[raam_meetod[raam_INDEX]] & 32) != 0 && raam_lukk[raam_INDEX] == 0) {
                int objekt_viide = lõim_siht[tähtaja_piires_lõim]; if (!잠금얻기(objekt_viide)) { if (VIGA) break; continue; } raam_lukk[raam_INDEX] = objekt_viide;
            }
            잠시수 = 0;
            if (--남음 == 0) { tõrge_VALUE("instruction limit (500000)"); break; }
            int Käivita_2 = raam_ametikoht[raam_INDEX]; 틀명령[raam_INDEX] = Käivita_2; int VALUE = 명바();
            if (VIGA) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int number = meetod_omanik[raam_meetod[raam_INDEX]] * 512 + (VALUE == 18 ? 명바() : 명짧());
                if (number <= 0 || number >= konstant_silt.length) tõrge_VALUE("invalid ldc constant");
                else if (konstant_silt[number] == 3) 넣기(상가[number], 1);
                else if (konstant_silt[number] == 8) 넣기(konstant_SMS(상가[number]), 2);
                else tõrge_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { kirjutamine_kohalik(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { kirjutamine_kohalik(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { kirjutamine_kohalik(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE >= 50 && VALUE <= 53) {
                int kirje_ametikoht = 빼기(1), objekt_viide = 빼기(2), ala_CODE = VALUE == 46 ? 2 : VALUE == 50 ? 3 : VALUE == 51 ? 20 : VALUE == 52 ? 22 : 23;
                if (VALUE == 51 && objekt_viide > 0 && objekt_viide < 힙끝 && 힙[objekt_viide] == 21) ala_CODE = 21;
                int 읽는자리 = 배열칸(objekt_viide, kirje_ametikoht, ala_CODE); if (!VIGA) 넣기(힙[읽는자리], VALUE == 50 ? 2 : 1); continue;
            }
            if (VALUE == 79 || VALUE >= 83 && VALUE <= 86) {
                int kirje_viide = 빼기(VALUE == 83 ? 2 : 1), kirje_ametikoht = 빼기(1), objekt_viide = 빼기(2), ala_CODE = VALUE == 79 ? 2 : VALUE == 83 ? 3 : VALUE == 84 ? 20 : VALUE == 85 ? 22 : 23;
                if (VALUE == 84 && objekt_viide > 0 && objekt_viide < 힙끝 && 힙[objekt_viide] == 21) ala_CODE = 21;
                int 읽는자리 = 배열칸(objekt_viide, kirje_ametikoht, ala_CODE);
                if (!VIGA && ala_CODE == 3 && !배열저장가능(objekt_viide, kirje_viide)) continue;
                if (!VIGA) 힙[읽는자리] = ala_CODE == 20 ? (byte)kirje_viide : ala_CODE == 21 ? kirje_viide & 1 : ala_CODE == 22 ? (char)kirje_viide : ala_CODE == 23 ? (short)kirje_viide : kirje_viide;
                continue;
            }
            if (VALUE >= 87 && VALUE <= 95) { 스택명령(VALUE); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int SECOND_operand = 빼기(1), 가 = 빼기(1), TULEMUS = 0;
                if ((VALUE == 108 || VALUE == 112) && SECOND_operand == 0) { tõrge_VALUE("ArithmeticException: / by zero"); continue; }
                if (VALUE == 96) TULEMUS = 가 + SECOND_operand;
                if (VALUE == 100) TULEMUS = 가 - SECOND_operand;
                if (VALUE == 104) TULEMUS = 가 * SECOND_operand;
                if (VALUE == 108) TULEMUS = 가 / SECOND_operand;
                if (VALUE == 112) TULEMUS = 가 % SECOND_operand;
                if (VALUE == 120) TULEMUS = 가 << SECOND_operand;
                if (VALUE == 122) TULEMUS = 가 >> SECOND_operand;
                if (VALUE == 124) TULEMUS = 가 >>> SECOND_operand;
                if (VALUE == 126) TULEMUS = 가 & SECOND_operand;
                if (VALUE == 128) TULEMUS = 가 | SECOND_operand;
                if (VALUE == 130) TULEMUS = 가 ^ SECOND_operand;
                넣기(TULEMUS, 1); continue;
            }
            if (VALUE == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALUE == 132) {
                int kohalik_skoop = 명바(), samm_samm = (byte)명바(); 지역읽기(kohalik_skoop, 1); 넣기(빼기(1) + samm_samm, 1); kirjutamine_kohalik(kohalik_skoop, 1); continue;
            }
            if (VALUE >= 145 && VALUE <= 147) {
                int number = 빼기(1); 넣기(VALUE == 145 ? (byte)number : VALUE == 146 ? (char)number : (short)number, 1); continue;
            }
            if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                int sihtkoht_VALUE = Käivita_2 + (short)명짧(); boolean 갈까 = VALUE == 167;
                if (VALUE >= 153 && VALUE <= 158) {
                    int number = 빼기(1); 갈까 = VALUE == 153 ? number == 0 : VALUE == 154 ? number != 0 : VALUE == 155 ? number < 0 : VALUE == 156 ? number >= 0 : VALUE == 157 ? number > 0 : number <= 0;
                } else if (VALUE >= 159 && VALUE <= 166) {
                    int SECOND_operand = 빼기(VALUE >= 165 ? 2 : 1), 가 = 빼기(VALUE >= 165 ? 2 : 1);
                    갈까 = VALUE == 159 || VALUE == 165 ? 가 == SECOND_operand : VALUE == 160 || VALUE == 166 ? 가 != SECOND_operand : VALUE == 161 ? 가 < SECOND_operand : VALUE == 162 ? 가 >= SECOND_operand : VALUE == 163 ? 가 > SECOND_operand : 가 <= SECOND_operand;
                } else if (VALUE == 198 || VALUE == 199) { int number = 빼기(2); 갈까 = VALUE == 198 ? number == 0 : number != 0; }
                if (갈까) liigutama_VALUE(sihtkoht_VALUE); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { tagasi_saatma_näitaja(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE >= 178 && VALUE <= 181) { 필드호출(명상수(), VALUE, Käivita_2); continue; }
            if (VALUE >= 182 && VALUE <= 185) {
                int 부호값 = 명상수();
                if (VALUE == 185) { int kokku_COUNT = 명바(); if (kokku_COUNT == 0 || 명바() != 0) { tõrge_VALUE("invalid invokeinterface operands"); continue; } }
                CALL_meetod(부호값, VALUE); continue;
            }
            if (VALUE == 187) { 새객체(klassinimi_SMS(명상수()), Käivita_2); continue; }
            if (VALUE == 188 || VALUE == 189) {
                int ala_CODE = 3, komponent = 0;
                if (VALUE == 188) { int 임시값 = 명바(); ala_CODE = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else komponent = klassinimi_SMS(명상수());
                if (ala_CODE == 0) { tõrge_VALUE("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), objekt_viide = lisama_salvesti(ala_CODE, 유효길이); if (!VIGA) massiivi_element[objekt_viide] = komponent; 넣기(objekt_viide, 2); continue;
            }
            if (VALUE == 190) {
                int objekt_viide = 빼기(2);
                if (객체유효(objekt_viide)) { int Võrdlus_ametikoht = 힙[objekt_viide]; if (Võrdlus_ametikoht != 2 && Võrdlus_ametikoht != 3 && (Võrdlus_ametikoht < 20 || Võrdlus_ametikoht > 23)) tõrge_VALUE("not an array"); else 넣기(힙[objekt_viide + 1], 1); }
                continue;
            }
            if (VALUE == 191) {
                int objekt_viide = 빼기(2); if (객체유효(objekt_viide)) { if (힙[objekt_viide] != 9) tõrge_VALUE("athrow requires supported Throwable"); else { 던진객체 = objekt_viide; VIGA = true; } }
                continue;
            }
            if (VALUE == 192 || VALUE == 193) {
                int nimetus_konstant = klassinimi_SMS(명상수()), objekt_viide = 빼기(2); boolean MATCH = 맞는객체(objekt_viide, nimetus_konstant);
                if (VALUE == 193) 넣기(objekt_viide != 0 && MATCH ? 1 : 0, 1);
                else { if (!MATCH && !VIGA) tõrge_VALUE("ClassCastException"); 넣기(objekt_viide, 2); }
                continue;
            }
            if (VALUE == 170 || VALUE == 171) {
                int 읽는자리 = Käivita_2 + 1, Fail_INDEX = raam_meetod[raam_INDEX], Võti_viide = 빼기(1);
                while ((읽는자리 - meetod_START[Fail_INDEX]) % 4 != 0) 읽는자리++;
                int siht_ADDRESS = ametikoht_täisarv(읽는자리);
                if (VALUE == 170) { int 낮은값 = ametikoht_täisarv(읽는자리 + 4), 높은값 = ametikoht_täisarv(읽는자리 + 8); if (Võti_viide >= 낮은값 && Võti_viide <= 높은값) siht_ADDRESS = ametikoht_täisarv(읽는자리 + 12 + (Võti_viide - 낮은값) * 4); }
                else { int kokku_COUNT = ametikoht_täisarv(읽는자리 + 4); for (int Loop_INDEX = 0; Loop_INDEX < kokku_COUNT; Loop_INDEX++) if (ametikoht_täisarv(읽는자리 + 8 + Loop_INDEX * 8) == Võti_viide) siht_ADDRESS = ametikoht_täisarv(읽는자리 + 12 + Loop_INDEX * 8); }
                liigutama_VALUE(Käivita_2 + siht_ADDRESS); continue;
            }
            if (VALUE == 200) { liigutama_VALUE(Käivita_2 + ametikoht_täisarv(Käivita_2 + 1)); continue; }
            if (VALUE == 194 || VALUE == 195) {
                int objekt_viide = 빼기(2);
                if (VALUE == 195) vabastama_lukk(objekt_viide);
                else if (!잠금얻기(objekt_viide) && !VIGA) { 넣기(objekt_viide, 2); raam_ametikoht[raam_INDEX] = Käivita_2; }
                continue;
            }
            if (VALUE == 196) {
                int käsk_CODE = 명바(), kirje_ametikoht = 명짧();
                if (käsk_CODE == 21 || käsk_CODE == 25) 지역읽기(kirje_ametikoht, käsk_CODE == 21 ? 1 : 2);
                else if (käsk_CODE == 54 || käsk_CODE == 58) kirjutamine_kohalik(kirje_ametikoht, käsk_CODE == 54 ? 1 : 2);
                else if (käsk_CODE == 132) { int DELTA_VALUE = (short)명짧(); 지역읽기(kirje_ametikoht, 1); 넣기(빼기(1) + DELTA_VALUE, 1); kirjutamine_kohalik(kirje_ametikoht, 1); }
                else tõrge_VALUE("unsupported wide opcode");
                continue;
            }
            tõrge_VALUE("unsupported bytecode");
        }
    }
    static int FIND_tund_Sõnaseletus(int Nimi_2) {
        for (int Loop_INDEX = 0; Loop_INDEX < tund_Sõnaseletus_COUNT; Loop_INDEX++) if (tund_Sõnaseletus_nimetus[Loop_INDEX] != 0 && 같은말(tund_Sõnaseletus_nimetus[Loop_INDEX], Nimi_2)) return Loop_INDEX;
        return koormus_tund_Sõnaseletus(konstant_SMS(Nimi_2));
    }
    static int koormus_tund_Sõnaseletus(int nimetus_string) {
        if (!objekt_VALUE(nimetus_string, 1)) return -1;
        int 길이 = 힙[nimetus_string + 1];
        if (길이 < 1 || 길이 > 505 || tund_Sõnaseletus_COUNT == 16) { tõrge_VALUE("class name/count limit"); return -1; }
        for (int Loop_INDEX = 0; Loop_INDEX < 길이; Loop_INDEX++) { int koodipunkt = 힙[nimetus_string + 2 + Loop_INDEX]; failinimi_SMS[Loop_INDEX] = koodipunkt == '/' ? '.' : koodipunkt; }
        failinimi_SMS[길이] = '.'; failinimi_SMS[길이 + 1] = 'c'; failinimi_SMS[길이 + 2] = 'l'; failinimi_SMS[길이 + 3] = 'a'; failinimi_SMS[길이 + 4] = 's'; failinimi_SMS[길이 + 5] = 's'; failinimi_SMS[길이 + 6] = 0;
        int Suurus = kasutaja.파일읽기(failinimi_SMS, ajutine_fail);
        if (Suurus < 0) { tõrge_VALUE("ClassNotFoundException"); return -1; }
        int tund_Sõnaseletus = tund_Sõnaseletus_COUNT++; tund_Sõnaseletus_suurust_muutma[tund_Sõnaseletus] = Suurus;
        for (int Loop_INDEX = 0; Loop_INDEX < Suurus; Loop_INDEX++) Fail[tund_Sõnaseletus * 16384 + Loop_INDEX] = ajutine_fail[Loop_INDEX];
        클래스읽기(tund_Sõnaseletus); if (VIGA) return -1;
        int tegelik_andmed = konstant_SMS(tund_Sõnaseletus_nimetus[tund_Sõnaseletus]);
        if (!글같음(tegelik_andmed, nimetus_string, true)) { tõrge_VALUE("class name does not match file"); return -1; }
        int ema_VALUE = tund_Sõnaseletus_ema[tund_Sõnaseletus];
        if (ema_VALUE != 0 && !Word_SMS(ema_VALUE, "java/lang/Object") && !Word_SMS(ema_VALUE, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 uuesti_proovima_VALUE 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = FIND_tund_Sõnaseletus(ema_VALUE);
            if (VIGA || 위 < 0) return -1;
            int 읽는자리 = 위, etapp_COUNT = 0;
            while (읽는자리 >= 0 && etapp_COUNT++ < 16) {
                if (읽는자리 == tund_Sõnaseletus) { tõrge_VALUE("cyclic inheritance"); return -1; }
                읽는자리 = ema_tund(읽는자리);
            }
            int 시작변위 = 종칸수[위];
            for (int Fail_INDEX = 0; Fail_INDEX < 칸수; Fail_INDEX++) if (칸주인[Fail_INDEX] == tund_Sõnaseletus && (칸권한[Fail_INDEX] & 8) == 0) 칸위치[Fail_INDEX] += 시작변위;
            종칸수[tund_Sõnaseletus] += 시작변위;
        }
        return tund_Sõnaseletus;
    }
    static int ema_tund(int tund_Sõnaseletus) {
        int Nimi_2 = tund_Sõnaseletus_ema[tund_Sõnaseletus];
        for (int Loop_INDEX = 0; Loop_INDEX < tund_Sõnaseletus_COUNT; Loop_INDEX++) if (Nimi_2 != 0 && tund_Sõnaseletus_nimetus[Loop_INDEX] != 0 && 같은말(tund_Sõnaseletus_nimetus[Loop_INDEX], Nimi_2)) return Loop_INDEX;
        return -1;
    }
    static int FIND_meetod(int tund_Sõnaseletus, int Nimi_2, int vorming_VALUE) {
        for (int 깊이 = 0; tund_Sõnaseletus >= 0 && 깊이 < 16; 깊이++, tund_Sõnaseletus = ema_tund(tund_Sõnaseletus)) {
            for (int Loop_INDEX = 0; Loop_INDEX < meetod_COUNT; Loop_INDEX++) if (meetod_omanik[Loop_INDEX] == tund_Sõnaseletus && 같은말(meetod_nimetus_SMS[Loop_INDEX], Nimi_2) && 같은말(meetod_TYPE[Loop_INDEX], vorming_VALUE)) return Loop_INDEX;
        }
        return -1;
    }
    static int nimetus_meetod(int tund_Sõnaseletus, String Nimi_2, String vorming_VALUE) {
        for (int 깊이 = 0; tund_Sõnaseletus >= 0 && 깊이 < 16; 깊이++, tund_Sõnaseletus = ema_tund(tund_Sõnaseletus))
            for (int Loop_INDEX = 0; Loop_INDEX < meetod_COUNT; Loop_INDEX++) if (meetod_omanik[Loop_INDEX] == tund_Sõnaseletus && Word_SMS(meetod_nimetus_SMS[Loop_INDEX], Nimi_2) && Word_SMS(meetod_TYPE[Loop_INDEX], vorming_VALUE)) return Loop_INDEX;
        return -1;
    }
    static int 형종류(int Nimi_2) { return Fail[상가[Nimi_2]] == 'L' || Fail[상가[Nimi_2]] == '[' ? 2 : 1; }
    static boolean 초기화(int tund_Sõnaseletus, int käsk_START) {
        if (tund_Sõnaseletus < 0 || VIGA) return false;
        if (tund_Sõnaseletus_Olek[tund_Sõnaseletus] == 3) { tõrge_VALUE("NoClassDefFoundError: initialization failed"); return false; }
        if (tund_Sõnaseletus_Olek[tund_Sõnaseletus] == 1 && tund_lõim[tund_Sõnaseletus] != tähtaja_piires_lõim) { raam_ametikoht[raam_INDEX] = käsk_START; muutma_päring = true; return false; }
        if (tund_Sõnaseletus_Olek[tund_Sõnaseletus] != 0) return true;
        int 위 = ema_tund(tund_Sõnaseletus);
        if (위 >= 0 && !초기화(위, käsk_START)) return false;
        tund_Sõnaseletus_Olek[tund_Sõnaseletus] = 1; tund_lõim[tund_Sõnaseletus] = tähtaja_piires_lõim;
        if (종초기화[tund_Sõnaseletus] != 0) {
            raam_ametikoht[raam_INDEX] = käsk_START;
            호출(종초기화[tund_Sõnaseletus] - 1); if (!VIGA) 틀초기화[raam_INDEX] = tund_Sõnaseletus + 1;
            return false;
        }
        tund_Sõnaseletus_Olek[tund_Sõnaseletus] = 2; return true;
    }
    static void 필드호출(int INDEX, int Käsk, int Käivita_2) {
        if (!tšekk_konstant(INDEX, 9)) return;
        int omanik_VALUE = klassinimi_SMS(상가[INDEX]), Nimi_2 = viide_nimetus(konstant_SECOND_VALUE[INDEX]), vorming_VALUE = viide_TYPE(konstant_SECOND_VALUE[INDEX]);
        if (Word_SMS(omanik_VALUE, "java/lang/System") && (Word_SMS(Nimi_2, "out") || Word_SMS(Nimi_2, "err")) && Word_SMS(vorming_VALUE, "Ljava/io/PrintStream;") && Käsk == 178) { 넣기(-1, 2); return; }
        int tund_Sõnaseletus = FIND_tund_Sõnaseletus(omanik_VALUE); if (tund_Sõnaseletus < 0 || VIGA) return;
        int 찾음 = -1;
        for (int 읽는자리 = tund_Sõnaseletus, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = ema_tund(읽는자리))
            for (int Fail_INDEX = 0; Fail_INDEX < 칸수; Fail_INDEX++) if (칸주인[Fail_INDEX] == 읽는자리 && 같은말(칸이름[Fail_INDEX], Nimi_2) && 같은말(칸형[Fail_INDEX], vorming_VALUE)) 찾음 = Fail_INDEX;
        if (찾음 < 0) { tõrge_VALUE("NoSuchFieldError"); return; }
        boolean 정적 = Käsk == 178 || Käsk == 179;
        if (정적 != ((칸권한[찾음] & 8) != 0)) { tõrge_VALUE("field static/instance mismatch"); return; }
        if (정적 && !초기화(칸주인[찾음], Käivita_2)) return;
        int TYPE_VALUE = 형종류(vorming_VALUE), VALUE = 0;
        if (Käsk == 179 || Käsk == 181) VALUE = 빼기(TYPE_VALUE);
        if (정적) { if (Käsk == 178) 넣기(칸값[찾음], TYPE_VALUE); else if (!VIGA) 칸값[찾음] = VALUE; return; }
        int objekt_viide = 빼기(2);
        if (!객체유효(objekt_viide)) return;
        if (힙[objekt_viide] < 32 || !종포함(힙[objekt_viide] - 32, omanik_VALUE)) { tõrge_VALUE("field receiver type mismatch"); return; }
        int 보관칸 = objekt_viide + 2 + 칸위치[찾음];
        if (Käsk == 180) 넣기(힙[보관칸], TYPE_VALUE);
        else if (!VIGA) { 힙[보관칸] = VALUE; 힙참조[보관칸] = TYPE_VALUE == 2 ? 1 : 0; }
    }
    static boolean 종포함(int tund_Sõnaseletus, int Nimi_2) {
        for (int 중첩깊이 = 0; tund_Sõnaseletus >= 0 && 중첩깊이 < 16; 중첩깊이++, tund_Sõnaseletus = ema_tund(tund_Sõnaseletus)) {
            if (같은말(tund_Sõnaseletus_nimetus[tund_Sõnaseletus], Nimi_2) || (tund_Sõnaseletus_ema[tund_Sõnaseletus] != 0 && 같은말(tund_Sõnaseletus_ema[tund_Sõnaseletus], Nimi_2))) return true;
            for (int sisemine_ametikoht = 0; sisemine_ametikoht < tund_liides_COUNT[tund_Sõnaseletus]; sisemine_ametikoht++) if (같은말(tund_liides[tund_Sõnaseletus * 16 + sisemine_ametikoht], Nimi_2)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int bait_andmed, boolean RADA) {
        if (첫값 == bait_andmed) return true;
        if (첫값 <= 0 || bait_andmed <= 0 || 힙[첫값] != 1 || 힙[bait_andmed] != 1 || 힙[첫값 + 1] != 힙[bait_andmed + 1]) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) {
            int 가로좌표 = 힙[첫값 + 2 + Loop_INDEX], 세로좌표 = 힙[bait_andmed + 2 + Loop_INDEX];
            if (RADA) { if (가로좌표 == '.') 가로좌표 = '/'; if (세로좌표 == '.') 세로좌표 = '/'; }
            if (가로좌표 != 세로좌표) return false;
        }
        return true;
    }
    static boolean 객체유효(int objekt_viide) {
        if (objekt_viide == 0) { tõrge_VALUE("NullPointerException"); return false; }
        if (objekt_viide < 1 || objekt_viide >= 힙끝 || 힙폭[objekt_viide] < 2 || 힙[objekt_viide] == 0) { tõrge_VALUE("invalid object reference"); return false; }
        return true;
    }
    static void kaitsma_VALUE(int objekt_viide) {
        if (objekt_viide > 0 && objekt_viide < 힙끝 && 힙폭[objekt_viide] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = objekt_viide;
    }
    static void saade_VALUE(int objekt_viide) {
        if (objekt_viide > 0 && objekt_viide < 힙끝 && 힙폭[objekt_viide] >= 2 && 힙[objekt_viide] != 0 && 힙표시[objekt_viide] == 0) {
            힙표시[objekt_viide] = 1; 표시대기[ekraan_COUNT++] = objekt_viide;
        }
    }
    static void 수거() {
        ekraan_COUNT = 0; kogu_COUNT++;
        for (int tšekk_ametikoht = 1; tšekk_ametikoht < 힙끝; tšekk_ametikoht += 힙폭[tšekk_ametikoht]) 힙표시[tšekk_ametikoht] = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < string_viide.length; Loop_INDEX++) saade_VALUE(string_viide[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 칸수; Loop_INDEX++) if ((칸권한[Loop_INDEX] & 8) != 0 && 형종류(칸형[Loop_INDEX]) == 2) saade_VALUE(칸값[Loop_INDEX]);
        for (int 임시값 = 0; 임시값 < lõim_COUNT; 임시값++) {
            saade_VALUE(lõim_objekt[임시값]); saade_VALUE(lõim_siht[임시값]);
            int 꼭대기자리 = 임시값 == tähtaja_piires_lõim ? raam_INDEX : lõim_raam[임시값];
            for (int Fail_INDEX = 임시값 * 32; Fail_INDEX <= 꼭대기자리; Fail_INDEX++) {
                for (int sisemine_ametikoht = 0; sisemine_ametikoht < 함수지역[raam_meetod[Fail_INDEX]]; sisemine_ametikoht++) if (kohalik_TYPE[Fail_INDEX * 128 + sisemine_ametikoht] == 2) saade_VALUE(kohalik_VALUE[Fail_INDEX * 128 + sisemine_ametikoht]);
                for (int sisemine_ametikoht = 0; sisemine_ametikoht < raam_Virn[Fail_INDEX]; sisemine_ametikoht++) if (operand_Virn_TYPE[Fail_INDEX * 128 + sisemine_ametikoht] == 2) saade_VALUE(operand_Virn_VALUE[Fail_INDEX * 128 + sisemine_ametikoht]);
            }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 화면참조.length; Loop_INDEX++) saade_VALUE(화면참조[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 나중수; Loop_INDEX++) saade_VALUE(나중실행[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < salv_täisarv.length; Loop_INDEX++) saade_VALUE(salv_täisarv[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < tund_Sõnaseletus_COUNT; Loop_INDEX++) saade_VALUE(tund_lukk[Loop_INDEX]);
        for (int tšekk_ametikoht = 1; tšekk_ametikoht < 힙끝; tšekk_ametikoht += 힙폭[tšekk_ametikoht]) if (잠금깊이[tšekk_ametikoht] > 0) saade_VALUE(tšekk_ametikoht);
        saade_VALUE(던진객체);
        for (int Loop_INDEX = 0; Loop_INDEX < 잠시수; Loop_INDEX++) saade_VALUE(잠시참조[Loop_INDEX]);
        while (ekraan_COUNT > 0) {
            int objekt_viide = 표시대기[--ekraan_COUNT], ala_CODE = 힙[objekt_viide];
            for (int Loop_INDEX = objekt_viide + 2; Loop_INDEX < objekt_viide + 힙폭[objekt_viide]; Loop_INDEX++) if (ala_CODE == 3 || ala_CODE == 4 || 힙참조[Loop_INDEX] != 0) saade_VALUE(힙[Loop_INDEX]);
        }
        for (int tšekk_ametikoht = 1; tšekk_ametikoht < 힙끝; tšekk_ametikoht += 힙폭[tšekk_ametikoht]) if (힙표시[tšekk_ametikoht] == 0) 힙[tšekk_ametikoht] = 0;
        for (int tšekk_ametikoht = 1; tšekk_ametikoht < 힙끝; tšekk_ametikoht += 힙폭[tšekk_ametikoht]) if (힙[tšekk_ametikoht] == 0) {
            while (tšekk_ametikoht + 힙폭[tšekk_ametikoht] < 힙끝 && 힙[tšekk_ametikoht + 힙폭[tšekk_ametikoht]] == 0) { int Edasi_ametikoht = tšekk_ametikoht + 힙폭[tšekk_ametikoht]; 힙폭[tšekk_ametikoht] += 힙폭[Edasi_ametikoht]; 힙폭[Edasi_ametikoht] = 0; }
            if (tšekk_ametikoht + 힙폭[tšekk_ametikoht] == 힙끝) { 힙끝 = tšekk_ametikoht; break; }
        }
    }
    static int 새기억(int 종류, int 길이) {
        if (길이 < 0) { tõrge_VALUE("NegativeArraySizeException"); return 0; }
        if (길이 > 힙.length - 3) { tõrge_VALUE("object heap exhausted"); return 0; }
        int 필요수 = 길이 + 2, objekt_viide = 0;
        if (필요수 <= 힙.length - 힙끝) { objekt_viide = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { objekt_viide = 읽는자리; break; }
            if (objekt_viide != 0) {
                int 남은길이 = 힙폭[objekt_viide] - 필요수;
                if (남은길이 >= 2) { 힙폭[objekt_viide + 필요수] = 남은길이; 힙[objekt_viide + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { objekt_viide = 힙끝; 힙끝 += 필요수; }
        }
        if (objekt_viide == 0) { tõrge_VALUE("object heap exhausted"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < 필요수; Loop_INDEX++) { 힙[objekt_viide + Loop_INDEX] = 0; 힙참조[objekt_viide + Loop_INDEX] = 0; 힙폭[objekt_viide + Loop_INDEX] = 0; }
        massiivi_element[objekt_viide] = 0;
        힙폭[objekt_viide] = 필요수; 힙[objekt_viide] = 종류; 힙[objekt_viide + 1] = 길이; kaitsma_VALUE(objekt_viide); return objekt_viide;
    }
    static int erand_tund(String nimetus_konstant) {
        if (자바도구.같음(nimetus_konstant, "java/lang/Throwable")) return 1;
        if (자바도구.같음(nimetus_konstant, "java/lang/Exception")) return 2;
        if (자바도구.같음(nimetus_konstant, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(nimetus_konstant, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(nimetus_konstant, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(nimetus_konstant, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(nimetus_konstant, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(nimetus_konstant, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(nimetus_konstant, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(nimetus_konstant, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(nimetus_konstant, "java/io/IOException")) return 11;
        if (자바도구.같음(nimetus_konstant, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(nimetus_konstant, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(nimetus_konstant, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(nimetus_konstant, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int erand_konstant(int Nimi_2) {
        for (int Loop_INDEX = 1; Loop_INDEX <= 41; Loop_INDEX++) if (Word_SMS(Nimi_2, erand_nimetus(Loop_INDEX))) return Loop_INDEX;
        return 0;
    }
    static String erand_nimetus(int isik_VALUE) {
        if (isik_VALUE == 40) return "java/lang/InterruptedException";
        if (isik_VALUE == 41) return "Eesti/oma/대기중단예외";
        if (isik_VALUE == 39) return "java/net/SocketException";
        if (isik_VALUE == 20) return "Eesti/oma/erand";
        if (isik_VALUE == 21) return "Eesti/oma/실행예외";
        if (isik_VALUE == 22) return "Eesti/oma/I_O_erand";
        if (isik_VALUE == 23) return "Eesti/oma/Oota_TIMEOUT_erand";
        if (isik_VALUE == 24) return "Eesti/oma/ADDRESS_LOOKUP_erand";
        if (isik_VALUE == 25) return "Eesti/oma/파일없음예외";
        if (isik_VALUE == 26) return "Eesti/oma/통신예외";
        if (isik_VALUE == 27) return "Eesti/oma/kehtetu_argument_erand";
        if (isik_VALUE == 28) return "Eesti/oma/number_vorming_tõrge";
        if (isik_VALUE == 29) return "Eesti/oma/범위예외";
        if (isik_VALUE == 30) return "Eesti/oma/배열범위예외";
        if (isik_VALUE == 31) return "Eesti/oma/문자열범위예외";
        if (isik_VALUE == 32) return "Eesti/oma/NULL_viide_erand";
        if (isik_VALUE == 33) return "Eesti/oma/산술예외";
        if (isik_VALUE == 34) return "Eesti/oma/Olek_erand";
        if (isik_VALUE == 35) return "Eesti/oma/TYPE_esitama_erand";
        if (isik_VALUE == 36) return "Eesti/oma/음수배열크기예외";
        if (isik_VALUE == 37) return "Eesti/oma/ARRAY_salv_tõrge";
        if (isik_VALUE == 38) return "Eesti/oma/lõim_Olek_erand";
        if (isik_VALUE == 1) return "java/lang/Throwable"; if (isik_VALUE == 2) return "java/lang/Exception";
        if (isik_VALUE == 3) return "java/lang/RuntimeException"; if (isik_VALUE == 4) return "java/lang/ArithmeticException";
        if (isik_VALUE == 5) return "java/lang/NullPointerException"; if (isik_VALUE == 6) return "java/lang/IndexOutOfBoundsException";
        if (isik_VALUE == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (isik_VALUE == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (isik_VALUE == 9) return "java/lang/IllegalArgumentException"; if (isik_VALUE == 10) return "java/lang/NumberFormatException";
        if (isik_VALUE == 11) return "java/io/IOException"; if (isik_VALUE == 12) return "java/io/FileNotFoundException";
        if (isik_VALUE == 17) return "java/lang/ArrayStoreException";
        if (isik_VALUE == 18) return "java/net/UnknownHostException";
        if (isik_VALUE == 19) return "java/net/SocketTimeoutException";
        if (isik_VALUE == 16) return "java/lang/IllegalThreadStateException";
        if (isik_VALUE == 13) return "java/lang/IllegalStateException"; if (isik_VALUE == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int erand_ema(int isik_VALUE) {
        if (isik_VALUE == 40) return 2;
        if (isik_VALUE == 41) return 40;
        if (isik_VALUE == 39) return 11;
        if (isik_VALUE == 1) return 0;
        if (isik_VALUE == 2) return 1;
        if (isik_VALUE == 3) return 2;
        if (isik_VALUE == 4) return 3;
        if (isik_VALUE == 5) return 3;
        if (isik_VALUE == 6) return 3;
        if (isik_VALUE == 7) return 6;
        if (isik_VALUE == 8) return 6;
        if (isik_VALUE == 9) return 3;
        if (isik_VALUE == 10) return 9;
        if (isik_VALUE == 11) return 2;
        if (isik_VALUE == 12) return 11;
        if (isik_VALUE == 13) return 3;
        if (isik_VALUE == 14) return 3;
        if (isik_VALUE == 15) return 3;
        if (isik_VALUE == 16) return 9;
        if (isik_VALUE == 17) return 3;
        if (isik_VALUE == 18) return 11;
        if (isik_VALUE == 19) return 11;
        if (isik_VALUE == 20) return 2;
        if (isik_VALUE == 21) return 3;
        if (isik_VALUE == 22) return 11;
        if (isik_VALUE == 23) return 22;
        if (isik_VALUE == 24) return 22;
        if (isik_VALUE == 25) return 22;
        if (isik_VALUE == 26) return 22;
        if (isik_VALUE == 27) return 9;
        if (isik_VALUE == 28) return 27;
        if (isik_VALUE == 29) return 6;
        if (isik_VALUE == 30) return 29;
        if (isik_VALUE == 31) return 29;
        if (isik_VALUE == 32) return 5;
        if (isik_VALUE == 33) return 4;
        if (isik_VALUE == 34) return 13;
        if (isik_VALUE == 35) return 14;
        if (isik_VALUE == 36) return 15;
        if (isik_VALUE == 37) return 17;
        if (isik_VALUE == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int tegelik_väärtus, int 요구값) {
        for (int 깊이 = 0; tegelik_väärtus != 0 && 깊이 < 16; 깊이++, tegelik_väärtus = erand_ema(tegelik_väärtus))
            if (tegelik_väärtus == 요구값) return true;
        return false;
    }
    static void 예외던짐(int isik_VALUE, String 안내참조) {
        int objekt_viide = 새기억(9, 2); if (VIGA) return;
        힙[objekt_viide + 2] = isik_VALUE; 힙[objekt_viide + 3] = host_märk(안내참조); 힙참조[objekt_viide + 3] = 1;
        던진객체 = objekt_viide; VIGA = true;
    }
    static boolean 맞는객체(int objekt_viide, int Nimi_2) {
        if (objekt_viide == 0) return true;
        if (!객체유효(objekt_viide)) return false;
        int ala_CODE = 힙[objekt_viide];
        if (Word_SMS(Nimi_2, "java/lang/Object")) return true;
        if (ala_CODE >= 32) return 종포함(ala_CODE - 32, Nimi_2);
        if (ala_CODE == 9) { int siht_ADDRESS = erand_konstant(Nimi_2); return siht_ADDRESS != 0 && 예외포함(힙[objekt_viide + 2], siht_ADDRESS); }
        if (ala_CODE == 1) return Word_SMS(Nimi_2, "java/lang/String") || Word_SMS(Nimi_2, "java/lang/CharSequence");
        if (ala_CODE == 4) return Word_SMS(Nimi_2, "java/lang/StringBuilder") || Word_SMS(Nimi_2, "java/lang/CharSequence");
        if (ala_CODE == 10) return Word_SMS(Nimi_2, "java/util/ArrayList") || Word_SMS(Nimi_2, "java/util/List");
        if (ala_CODE == 11) return Word_SMS(Nimi_2, "java/util/HashMap") || Word_SMS(Nimi_2, "java/util/Map");
        if (ala_CODE == 12) return Word_SMS(Nimi_2, "java/lang/Integer") || Word_SMS(Nimi_2, "java/lang/Number");
        if (ala_CODE >= 24 && ala_CODE <= 28 && 힙[objekt_viide + 13] != 0) return 한국어화면종(Nimi_2) == ala_CODE || Word_SMS(Nimi_2, "Eesti/oma/화면구성요소");
        if (ala_CODE >= 24 && ala_CODE <= 28) return (한국어화면종(Nimi_2) == 0 && 화면종(Nimi_2) == ala_CODE) || Word_SMS(Nimi_2, "java/awt/Component") || Word_SMS(Nimi_2, "java/awt/Container") || Word_SMS(Nimi_2, "javax/swing/JComponent");
        if (ala_CODE == 29) return Word_SMS(Nimi_2, 힙[objekt_viide + 3] != 0 ? "Eesti/oma/Toiming_teatamine" : "java/awt/event/ActionEvent");
        if (ala_CODE == 30) return Word_SMS(Nimi_2, "java/awt/FlowLayout") || Word_SMS(Nimi_2, "java/awt/LayoutManager");
        if (ala_CODE == 17) return Word_SMS(Nimi_2, "java/net/Socket");
        if (ala_CODE == 18) return Word_SMS(Nimi_2, "java/net/ServerSocket");
        if (ala_CODE == 19) return Word_SMS(Nimi_2, 힙[objekt_viide + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (ala_CODE == 14) return Word_SMS(Nimi_2, "java/net/InetAddress");
        if (ala_CODE == 15) return Word_SMS(Nimi_2, "java/net/DatagramSocket");
        if (ala_CODE == 16) return Word_SMS(Nimi_2, "java/net/DatagramPacket");
        if (ala_CODE == 13) return Word_SMS(Nimi_2, 힙[objekt_viide + 3] != 0 ? "Eesti/oma/töötaja" : "java/lang/Thread");
        if (ala_CODE == 2) return Word_SMS(Nimi_2, "[I"); if (ala_CODE == 20) return Word_SMS(Nimi_2, "[B"); if (ala_CODE == 21) return Word_SMS(Nimi_2, "[Z");
        if (ala_CODE == 22) return Word_SMS(Nimi_2, "[C"); if (ala_CODE == 23) return Word_SMS(Nimi_2, "[S");
        if (ala_CODE != 3) return false;
        if (Word_SMS(Nimi_2, "[Ljava/lang/Object;")) return true;
        int komponent = massiivi_element[objekt_viide];
        if (komponent == -1) return Word_SMS(Nimi_2, "[Ljava/lang/String;") || Word_SMS(Nimi_2, "[Ljava/lang/CharSequence;");
        if (komponent == 0) return false;
        if (배열종비교(komponent, Nimi_2)) return true;
        if ((Word_SMS(komponent, "java/lang/String") || Word_SMS(komponent, "java/lang/StringBuilder")) && Word_SMS(Nimi_2, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDEX = 0; Loop_INDEX < tund_Sõnaseletus_COUNT; Loop_INDEX++) if (같은말(tund_Sõnaseletus_nimetus[Loop_INDEX], komponent)) {
            for (int koodipunkt = Loop_INDEX, 중첩깊이 = 0; koodipunkt >= 0 && 중첩깊이 < 16; 중첩깊이++, koodipunkt = ema_tund(koodipunkt)) {
                if (배열종비교(tund_Sõnaseletus_ema[koodipunkt], Nimi_2)) return true;
                for (int sisemine_ametikoht = 0; sisemine_ametikoht < tund_liides_COUNT[koodipunkt]; sisemine_ametikoht++) if (배열종비교(tund_liides[koodipunkt * 16 + sisemine_ametikoht], Nimi_2)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int nimetus_konstant, int 형식참조) {
        int tšekk_ametikoht = 상가[형식참조], kirje_COUNT = konstant_SECOND_VALUE[형식참조];
        if (nimetus_konstant == 0 || kirje_COUNT < 4 || Fail[tšekk_ametikoht] != '[' || Fail[tšekk_ametikoht + 1] != 'L' || Fail[tšekk_ametikoht + kirje_COUNT - 1] != ';' || konstant_SECOND_VALUE[nimetus_konstant] != kirje_COUNT - 3) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < kirje_COUNT - 3; Loop_INDEX++) if (Fail[상가[nimetus_konstant] + Loop_INDEX] != Fail[tšekk_ametikoht + 2 + Loop_INDEX]) return false;
        return true;
    }
    static void pide_erand() {
        if (던진객체 == 0) return;
        VIGA = false;
        while (raam_INDEX >= tähtaja_piires_lõim * 32) {
            int Fail_INDEX = raam_meetod[raam_INDEX], 읽는자리 = 틀명령[raam_INDEX];
            for (int Loop_INDEX = 0; Loop_INDEX < 잡기수; Loop_INDEX++) if (잡기함수[Loop_INDEX] == Fail_INDEX && 읽는자리 >= 잡기시작[Loop_INDEX] && 읽는자리 < 잡기끝[Loop_INDEX]
                && (잡기종[Loop_INDEX] == 0 || 맞는객체(던진객체, 잡기종[Loop_INDEX]))) {
                raam_ametikoht[raam_INDEX] = 잡기위치[Loop_INDEX]; raam_Virn[raam_INDEX] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (틀초기화[raam_INDEX] != 0) tund_Sõnaseletus_Olek[틀초기화[raam_INDEX] - 1] = 3;
            if (raam_lukk[raam_INDEX] != 0) { vabastama_lukk(raam_lukk[raam_INDEX]); raam_lukk[raam_INDEX] = 0; }
            raam_INDEX--;
        }
        kasutaja.Kirjutamine("Uncaught ");
        if (힙[던진객체] == 9) { kasutaja.Kirjutamine(erand_nimetus(힙[던진객체 + 2])); kasutaja.Kirjutamine(": "); kirjutamine_SMS(힙[던진객체 + 3]); }
        else kasutaja.Kirjutamine("user exception");
        kasutaja.kirjutamine_märk_VALUE(10); 던진객체 = 0; VIGA = true;
    }
    // 이 JVM의 operand_Virn 항목은 tähtaja_piires_kaup category-1(int/reference)만 허용한다.
    static void 스택명령(int käsk_CODE) {
        int 첫값 = 빼기(0), 첫형식 = tagasi_saatma_TYPE;
        if (käsk_CODE == 87) return;
        if (käsk_CODE == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int bait_andmed = 빼기(0), SECOND_vorming = tagasi_saatma_TYPE;
        if (käsk_CODE == 88) return;
        if (käsk_CODE == 90) { 넣기(첫값, 첫형식); 넣기(bait_andmed, SECOND_vorming); 넣기(첫값, 첫형식); return; }
        if (käsk_CODE == 92) { 넣기(bait_andmed, SECOND_vorming); 넣기(첫값, 첫형식); 넣기(bait_andmed, SECOND_vorming); 넣기(첫값, 첫형식); return; }
        if (käsk_CODE == 95) { 넣기(첫값, 첫형식); 넣기(bait_andmed, SECOND_vorming); return; }
        int koodipunkt = 빼기(0), 셋째형식 = tagasi_saatma_TYPE;
        if (käsk_CODE == 91) { 넣기(첫값, 첫형식); 넣기(koodipunkt, 셋째형식); 넣기(bait_andmed, SECOND_vorming); 넣기(첫값, 첫형식); return; }
        if (käsk_CODE == 93) { 넣기(bait_andmed, SECOND_vorming); 넣기(첫값, 첫형식); 넣기(koodipunkt, 셋째형식); 넣기(bait_andmed, SECOND_vorming); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = tagasi_saatma_TYPE;
        넣기(bait_andmed, SECOND_vorming); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(koodipunkt, 셋째형식); 넣기(bait_andmed, SECOND_vorming); 넣기(첫값, 첫형식);
    }
    static void 새객체(int nimetus_konstant, int 시작점) {
        int ala_CODE = 0, 유효길이 = 0, erand_viide = erand_konstant(nimetus_konstant);
        if (Word_SMS(nimetus_konstant, "java/lang/StringBuilder")) { ala_CODE = 4; 유효길이 = 1; }
        if (Word_SMS(nimetus_konstant, "java/io/FileInputStream")) { ala_CODE = 5; 유효길이 = 2; }
        if (Word_SMS(nimetus_konstant, "java/io/FileOutputStream")) { ala_CODE = 6; 유효길이 = 2; }
        if (erand_viide != 0) { ala_CODE = 9; 유효길이 = 2; }
        if (Word_SMS(nimetus_konstant, "java/util/ArrayList")) { ala_CODE = 10; 유효길이 = 2; }
        if (Word_SMS(nimetus_konstant, "java/util/HashMap")) { ala_CODE = 11; 유효길이 = 2; }
        if (Word_SMS(nimetus_konstant, "java/lang/Integer")) { ala_CODE = 12; 유효길이 = 1; }
        if (Word_SMS(nimetus_konstant, "java/net/Socket")) { ala_CODE = 17; 유효길이 = 5; }
        if (Word_SMS(nimetus_konstant, "java/net/ServerSocket")) { ala_CODE = 18; 유효길이 = 5; }
        if (Word_SMS(nimetus_konstant, "java/net/DatagramSocket")) { ala_CODE = 15; 유효길이 = 3; }
        if (Word_SMS(nimetus_konstant, "java/net/DatagramPacket")) { ala_CODE = 16; 유효길이 = 4; }
        if (Word_SMS(nimetus_konstant, "java/lang/Thread") || Word_SMS(nimetus_konstant, "Eesti/oma/töötaja")) { ala_CODE = 13; 유효길이 = 2; }
        if (Word_SMS(nimetus_konstant, "java/lang/Object")) { ala_CODE = 8; }
        if (ala_CODE == 0 && 화면종(nimetus_konstant) != 0) { ala_CODE = 화면종(nimetus_konstant); 유효길이 = 12; }
        if (ala_CODE == 0) {
            int koodipunkt = FIND_tund_Sõnaseletus(nimetus_konstant); if (koodipunkt < 0 || VIGA || !초기화(koodipunkt, 시작점)) return;
            ala_CODE = 32 + koodipunkt; 유효길이 = 종칸수[koodipunkt];
        }
        int objekt_viide = lisama_salvesti(ala_CODE, 유효길이); if (VIGA) return;
        if (ala_CODE == 13 && Word_SMS(nimetus_konstant, "Eesti/oma/töötaja")) 힙[objekt_viide + 3] = 1;
        if (ala_CODE >= 24 && ala_CODE <= 28 && 한국어화면종(nimetus_konstant) != 0) 힙[objekt_viide + 13] = 1;
        if (ala_CODE == 5 || ala_CODE == 6 || ala_CODE == 15 || ala_CODE == 17 || ala_CODE == 18) 힙[objekt_viide + 2] = -1;
        if (ala_CODE == 9) 힙[objekt_viide + 2] = erand_viide;
        넣기(objekt_viide, 2);
    }
    static boolean 값같음(int 첫값, int bait_andmed) {
        if (첫값 == bait_andmed) return true;
        if (첫값 == 0 || bait_andmed == 0 || 첫값 < 0 || bait_andmed < 0 || 첫값 >= 힙끝 || bait_andmed >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[bait_andmed] == 1) return 글같음(첫값, bait_andmed, false);
        return 힙[첫값] == 12 && 힙[bait_andmed] == 12 && 힙[첫값 + 2] == 힙[bait_andmed + 2];
    }
    static int 글조각(int objekt_viide, int START_ametikoht, int lõpeta_kõne_ametikoht) {
        if (!objekt_VALUE(objekt_viide, 1)) return 0;
        if (START_ametikoht < 0 || lõpeta_kõne_ametikoht < START_ametikoht || lõpeta_kõne_ametikoht > 힙[objekt_viide + 1]) { tõrge_VALUE("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = lisama_salvesti(1, lõpeta_kõne_ametikoht - START_ametikoht); if (VIGA) return 0;
        for (int Loop_INDEX = START_ametikoht; Loop_INDEX < lõpeta_kõne_ametikoht; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX - START_ametikoht] = 힙[objekt_viide + 2 + Loop_INDEX];
        return 반환값;
    }
    static int Ühine_SMS(int 첫값, int bait_andmed) {
        if (!objekt_VALUE(첫값, 1) || !objekt_VALUE(bait_andmed, 1)) return 0;
        int kirje_COUNT = 힙[첫값 + 1], meetod_INDEX = 힙[bait_andmed + 1], 반환값 = lisama_salvesti(1, kirje_COUNT + meetod_INDEX); if (VIGA) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < kirje_COUNT; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 힙[첫값 + 2 + Loop_INDEX];
        for (int Loop_INDEX = 0; Loop_INDEX < meetod_INDEX; Loop_INDEX++) 힙[반환값 + 2 + kirje_COUNT + Loop_INDEX] = 힙[bait_andmed + 2 + Loop_INDEX];
        return 반환값;
    }
    static boolean 기본호출(int omanik, int nimetus_konstant, int 서술상수, int käsk_CODE) {
        if (Word_SMS(omanik, "Eesti/oma/실행인수") && käsk_CODE == 184) {
            if (Word_SMS(nimetus_konstant, "kaup_COUNT") && Word_SMS(서술상수, "()I")) { 넣기(kasutaja.인수개수() - 1, 1); return true; }
            if (Word_SMS(nimetus_konstant, "Tekst") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= kasutaja.인수개수() - 1) 예외던짐(29, "Täida_käsk Argumendid 범위를 벗어났습니다");
                else 넣기(host_märk(kasutaja.Argumendid(순번 + 1)), 2);
                return true;
            }
            tõrge_VALUE("지원하지 않는 Eesti Täida_käsk Argumendid 호출"); return true;
        }
        if (Word_SMS(omanik, "Eesti/oma/töötaja")) { Joonis_lõim(nimetus_konstant, 서술상수, käsk_CODE, true); return true; }
        if (한국어화면소유(omanik)) { 한국어화면호출(omanik, nimetus_konstant, 서술상수, käsk_CODE); return true; }
        if (화면소유(omanik)) { 화면호출(omanik, nimetus_konstant, 서술상수, käsk_CODE); return true; }
        if (Word_SMS(omanik, "java/net/Socket") || Word_SMS(omanik, "java/net/ServerSocket") || Word_SMS(omanik, "java/io/InputStream") || Word_SMS(omanik, "java/io/OutputStream")) { 흐름호출(omanik, nimetus_konstant, 서술상수, käsk_CODE); return true; }
        if (Word_SMS(omanik, "Eesti/oma/tuum_VALUE") && käsk_CODE == 184) {
            if (Word_SMS(nimetus_konstant, "화면너비") && Word_SMS(서술상수, "()I")) { 넣기(kasutaja.화면너비(), 1); return true; }
            if (Word_SMS(nimetus_konstant, "화면높이") && Word_SMS(서술상수, "()I")) { 넣기(kasutaja.화면높이(), 1); return true; }
            if (Word_SMS(nimetus_konstant, "밀리초") && Word_SMS(서술상수, "()I")) { 넣기(kasutaja.밀리초(), 1); return true; }
            if (Word_SMS(nimetus_konstant, "그림대기") && Word_SMS(서술상수, "()I")) { 넣기(kasutaja.그림대기(), 1); return true; }
            if (Word_SMS(nimetus_konstant, "ristkülik") && Word_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), 가로좌표 = 빼기(1); 넣기(kasutaja.ristkülik(가로좌표, 세로좌표, 너비, 높이, 색상), 1); return true; }
        }
        if (Word_SMS(omanik, "java/net/InetAddress") || Word_SMS(omanik, "java/net/DatagramPacket") || Word_SMS(omanik, "java/net/DatagramSocket")) { 통신호출(omanik, nimetus_konstant, 서술상수, käsk_CODE); return true; }
        if (Word_SMS(omanik, "java/lang/Thread")) { 가닥호출(nimetus_konstant, 서술상수, käsk_CODE); return true; }
        if (Word_SMS(omanik, "java/lang/Object")) {
            if (Word_SMS(nimetus_konstant, "<init>") && Word_SMS(서술상수, "()V") && käsk_CODE == 183) { 객체유효(빼기(2)); return true; }
            if (Word_SMS(nimetus_konstant, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int bait_andmed = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == bait_andmed ? 1 : 0, 1); return true; }
        }
        if (erand_konstant(omanik) != 0) {
            if (Word_SMS(nimetus_konstant, "<init>") && käsk_CODE == 183 && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int viip = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), objekt_viide = 빼기(2);
                if (objekt_VALUE(objekt_viide, 9)) { 힙[objekt_viide + 3] = viip; 힙참조[objekt_viide + 3] = 1; } return true;
            }
            if ((Word_SMS(nimetus_konstant, "getMessage") || Word_SMS(nimetus_konstant, "설명")) && Word_SMS(서술상수, "()Ljava/lang/String;")) { int objekt_viide = 빼기(2); if (objekt_VALUE(objekt_viide, 9)) 넣기(힙[objekt_viide + 3], 2); return true; }
        }
        if (Word_SMS(omanik, "java/lang/String")) {
            if (käsk_CODE == 182 && Word_SMS(nimetus_konstant, "getBytes") && (Word_SMS(서술상수, "()[B") || Word_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int kodeerimine_nimetus = Word_SMS(서술상수, "()[B") ? 0 : 빼기(2), objekt_viide = 빼기(2);
                if (!objekt_VALUE(objekt_viide, 1)) return true;
                if (kodeerimine_nimetus != 0 && !글같음(kodeerimine_nimetus, host_märk("UTF-8"), false) && !글같음(kodeerimine_nimetus, host_märk("UTF8"), false) && !글같음(kodeerimine_nimetus, host_märk("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int kirje_COUNT = 힙[objekt_viide + 1], 반환값 = lisama_salvesti(20, kirje_COUNT * 3), 사용수 = 0; if (VIGA) return true;
                for (int sisemine_ametikoht = 0; sisemine_ametikoht < kirje_COUNT; sisemine_ametikoht++) {
                    int koodipunkt = 힙[objekt_viide + 2 + sisemine_ametikoht];
                    if (koodipunkt >= 0xd800 && koodipunkt <= 0xdbff && sisemine_ametikoht + 1 < kirje_COUNT && 힙[objekt_viide + 3 + sisemine_ametikoht] >= 0xdc00 && 힙[objekt_viide + 3 + sisemine_ametikoht] <= 0xdfff) koodipunkt = 0x10000 + ((koodipunkt - 0xd800) << 10) + 힙[objekt_viide + 2 + ++sisemine_ametikoht] - 0xdc00;
                    else if (koodipunkt >= 0xd800 && koodipunkt <= 0xdfff) koodipunkt = '?';
                    if (koodipunkt < 128) 힙[반환값 + 2 + 사용수++] = koodipunkt;
                    else { int bait_COUNT = koodipunkt < 2048 ? 2 : koodipunkt < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((bait_COUNT == 2 ? 192 : bait_COUNT == 3 ? 224 : 240) | koodipunkt >> (6 * (bait_COUNT - 1))); for (int Võrdlus_ametikoht = bait_COUNT - 1; Võrdlus_ametikoht > 0; Võrdlus_ametikoht--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | koodipunkt >> (6 * (Võrdlus_ametikoht - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (käsk_CODE == 184 && Word_SMS(nimetus_konstant, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(number_märk(빼기(1)), 2); return true; }
            if (käsk_CODE != 182) return false;
            if (Word_SMS(nimetus_konstant, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int bait_andmed = 빼기(2), 첫값 = 빼기(2); if (objekt_VALUE(첫값, 1)) 넣기(글같음(첫값, bait_andmed, false) ? 1 : 0, 1); return true; }
            if (Word_SMS(nimetus_konstant, "isEmpty") && Word_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (objekt_VALUE(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_SMS(nimetus_konstant, "substring") && (Word_SMS(서술상수, "(I)Ljava/lang/String;") || Word_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SECOND_VALUE = Word_SMS(서술상수, "(II)Ljava/lang/String;"); int lõpeta_kõne_ametikoht = SECOND_VALUE ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (objekt_VALUE(첫값, 1)) 넣기(글조각(첫값, 시작점, SECOND_VALUE ? lõpeta_kõne_ametikoht : 힙[첫값 + 1]), 2); return true;
            }
            if (Word_SMS(nimetus_konstant, "concat") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int bait_andmed = 빼기(2), 첫값 = 빼기(2); 넣기(Ühine_SMS(첫값, bait_andmed), 2); return true; }
            if (Word_SMS(nimetus_konstant, "hashCode") && Word_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), räsikood_VALUE = 0; if (objekt_VALUE(첫값, 1)) { for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) räsikood_VALUE = räsikood_VALUE * 31 + 힙[첫값 + 2 + Loop_INDEX]; 넣기(räsikood_VALUE, 1); } return true; }
            if (Word_SMS(nimetus_konstant, "toString") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (objekt_VALUE(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_SMS(omanik, "java/lang/Integer")) {
            if (käsk_CODE == 184 && Word_SMS(nimetus_konstant, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int andmed_VALUE = 빼기(1), objekt_viide = andmed_VALUE >= -128 && andmed_VALUE <= 127 ? salv_täisarv[andmed_VALUE + 128] : 0; if (objekt_viide == 0) { objekt_viide = lisama_salvesti(12, 1); if (!VIGA) { 힙[objekt_viide + 2] = andmed_VALUE; if (andmed_VALUE >= -128 && andmed_VALUE <= 127) salv_täisarv[andmed_VALUE + 128] = objekt_viide; } } 넣기(objekt_viide, 2); return true; }
            if (käsk_CODE == 183 && Word_SMS(nimetus_konstant, "<init>") && Word_SMS(서술상수, "(I)V")) { int andmed_VALUE = 빼기(1), objekt_viide = 빼기(2); if (objekt_VALUE(objekt_viide, 12)) 힙[objekt_viide + 2] = andmed_VALUE; return true; }
            if (käsk_CODE == 182 && Word_SMS(nimetus_konstant, "intValue") && Word_SMS(서술상수, "()I")) { int objekt_viide = 빼기(2); if (objekt_VALUE(objekt_viide, 12)) 넣기(힙[objekt_viide + 2], 1); return true; }
            if (käsk_CODE == 184 && Word_SMS(nimetus_konstant, "toString") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(number_märk(빼기(1)), 2); return true; }
        }
        if (Word_SMS(omanik, "java/lang/Math") && käsk_CODE == 184) {
            if (Word_SMS(nimetus_konstant, "abs") && Word_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_SMS(nimetus_konstant, "min") || Word_SMS(nimetus_konstant, "max")) && Word_SMS(서술상수, "(II)I")) { int bait_andmed = 빼기(1), 첫값 = 빼기(1); 넣기(Word_SMS(nimetus_konstant, "min") ? (첫값 < bait_andmed ? 첫값 : bait_andmed) : (첫값 > bait_andmed ? 첫값 : bait_andmed), 1); return true; }
        }
        if (Word_SMS(omanik, "java/lang/System") && käsk_CODE == 184) {
            if (Word_SMS(nimetus_konstant, "gc") && Word_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Word_SMS(nimetus_konstant, "arraycopy") && Word_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int kirje_COUNT = 빼기(1), sihtkoht_VALUE_INDEX = 빼기(1), bait_andmed = 빼기(2), START_ametikoht = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(bait_andmed)) {
                    int ala_CODE = 힙[첫값];
                    if (힙[bait_andmed] != ala_CODE || (ala_CODE != 2 && ala_CODE != 3 && (ala_CODE < 20 || ala_CODE > 23))) tõrge_VALUE("arraycopy type mismatch");
                    else if (kirje_COUNT < 0 || START_ametikoht < 0 || sihtkoht_VALUE_INDEX < 0 || START_ametikoht > 힙[첫값 + 1] - kirje_COUNT || sihtkoht_VALUE_INDEX > 힙[bait_andmed + 1] - kirje_COUNT) tõrge_VALUE("ArrayIndexOutOfBoundsException");
                    else if (첫값 == bait_andmed && sihtkoht_VALUE_INDEX > START_ametikoht) { for (int Loop_INDEX = kirje_COUNT - 1; Loop_INDEX >= 0; Loop_INDEX--) 힙[bait_andmed + 2 + sihtkoht_VALUE_INDEX + Loop_INDEX] = 힙[첫값 + 2 + START_ametikoht + Loop_INDEX]; }
                    else { for (int Loop_INDEX = 0; Loop_INDEX < kirje_COUNT && !VIGA; Loop_INDEX++) { int andmed_VALUE = 힙[첫값 + 2 + START_ametikoht + Loop_INDEX]; if (ala_CODE != 3 || 배열저장가능(bait_andmed, andmed_VALUE)) 힙[bait_andmed + 2 + sihtkoht_VALUE_INDEX + Loop_INDEX] = andmed_VALUE; } }
                }
                return true;
            }
        }
        if (Word_SMS(omanik, "java/util/ArrayList") || Word_SMS(omanik, "java/util/List") || Word_SMS(omanik, "java/util/HashMap") || Word_SMS(omanik, "java/util/Map")) {
            모음호출(omanik, nimetus_konstant, 서술상수, käsk_CODE); return true;
        }
        return false;
    }
    static void 모음늘리기(int objekt_viide, int 필요수) {
        int 이전값 = 힙[objekt_viide + 2], võimsus_andmed = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (võimsus_andmed >= 필요수) return;
        int Edasi_ametikoht = võimsus_andmed < 8 ? 8 : võimsus_andmed * 2; if (Edasi_ametikoht < 필요수) Edasi_ametikoht = 필요수;
        int andmed_ARRAY = lisama_salvesti(3, Edasi_ametikoht); if (VIGA) return;
        for (int Loop_INDEX = 0; Loop_INDEX < võimsus_andmed; Loop_INDEX++) 힙[andmed_ARRAY + 2 + Loop_INDEX] = 힙[이전값 + 2 + Loop_INDEX];
        힙[objekt_viide + 2] = andmed_ARRAY; 힙참조[objekt_viide + 2] = 1;
    }
    static void 모음호출(int omanik, int nimetus_konstant, int 서술상수, int käsk_CODE) {
        boolean 대응참조 = Word_SMS(omanik, "java/util/HashMap") || Word_SMS(omanik, "java/util/Map"); int ala_CODE = 대응참조 ? 11 : 10;
        if (Word_SMS(nimetus_konstant, "<init>") && käsk_CODE == 183 && Word_SMS(서술상수, "()V")) { int objekt_viide = 빼기(2); if (objekt_VALUE(objekt_viide, ala_CODE)) 모음늘리기(objekt_viide, 8); return; }
        if (käsk_CODE != 182 && käsk_CODE != 185) { tõrge_VALUE("invalid collection invocation"); return; }
        if (Word_SMS(nimetus_konstant, "size") && Word_SMS(서술상수, "()I") || Word_SMS(nimetus_konstant, "isEmpty") && Word_SMS(서술상수, "()Z")) {
            int objekt_viide = 빼기(2); if (objekt_VALUE(objekt_viide, ala_CODE)) 넣기(Word_SMS(nimetus_konstant, "size") ? 힙[objekt_viide + 3] : 힙[objekt_viide + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_SMS(nimetus_konstant, "clear") && Word_SMS(서술상수, "()V")) { int objekt_viide = 빼기(2); if (objekt_VALUE(objekt_viide, ala_CODE)) { int andmed_ARRAY = 힙[objekt_viide + 2]; for (int Loop_INDEX = 0; Loop_INDEX < 힙[andmed_ARRAY + 1]; Loop_INDEX++) 힙[andmed_ARRAY + 2 + Loop_INDEX] = 0; 힙[objekt_viide + 3] = 0; } return; }
        if (!대응참조 && Word_SMS(nimetus_konstant, "add") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int andmed_VALUE = 빼기(2), objekt_viide = 빼기(2); if (!objekt_VALUE(objekt_viide, 10)) return;
            int kirje_COUNT = 힙[objekt_viide + 3]; 모음늘리기(objekt_viide, kirje_COUNT + 1); if (!VIGA) { 힙[힙[objekt_viide + 2] + 2 + kirje_COUNT] = andmed_VALUE; 힙[objekt_viide + 3] = kirje_COUNT + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_SMS(nimetus_konstant, "get") || Word_SMS(nimetus_konstant, "remove")) && Word_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Word_SMS(nimetus_konstant, "set") && Word_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean infotehnoloogia_määratud = Word_SMS(nimetus_konstant, "set"); int andmed_VALUE = infotehnoloogia_määratud ? 빼기(2) : 0, kirje_ametikoht = 빼기(1), objekt_viide = 빼기(2);
            if (!objekt_VALUE(objekt_viide, 10)) return;
            int kirje_COUNT = 힙[objekt_viide + 3], andmed_ARRAY = 힙[objekt_viide + 2];
            if (kirje_ametikoht < 0 || kirje_ametikoht >= kirje_COUNT) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[andmed_ARRAY + 2 + kirje_ametikoht];
            if (infotehnoloogia_määratud) 힙[andmed_ARRAY + 2 + kirje_ametikoht] = andmed_VALUE;
            if (Word_SMS(nimetus_konstant, "remove")) { for (int Loop_INDEX = kirje_ametikoht + 1; Loop_INDEX < kirje_COUNT; Loop_INDEX++) 힙[andmed_ARRAY + 1 + Loop_INDEX] = 힙[andmed_ARRAY + 2 + Loop_INDEX]; 힙[andmed_ARRAY + 1 + kirje_COUNT] = 0; 힙[objekt_viide + 3] = kirje_COUNT - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Word_SMS(nimetus_konstant, "get") || Word_SMS(nimetus_konstant, "remove")) && Word_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(nimetus_konstant, "put") && Word_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(nimetus_konstant, "containsKey") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_SMS(nimetus_konstant, "put"), eemaldama = Word_SMS(nimetus_konstant, "remove");
            int andmed_VALUE = 넣기여부 ? 빼기(2) : 0, Võti_viide = 빼기(2), objekt_viide = 빼기(2); if (!objekt_VALUE(objekt_viide, 11)) return;
            int kirje_COUNT = 힙[objekt_viide + 3], andmed_ARRAY = 힙[objekt_viide + 2], 찾은여부 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < kirje_COUNT; Loop_INDEX++) if (값같음(Võti_viide, 힙[andmed_ARRAY + 2 + 2 * Loop_INDEX])) { 찾은여부 = Loop_INDEX; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[andmed_ARRAY + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(objekt_viide, (kirje_COUNT + 1) * 2); andmed_ARRAY = 힙[objekt_viide + 2]; 찾은여부 = kirje_COUNT; if (!VIGA) 힙[objekt_viide + 3] = kirje_COUNT + 1; }
                if (!VIGA) { 힙[andmed_ARRAY + 2 + 2 * 찾은여부] = Võti_viide; 힙[andmed_ARRAY + 3 + 2 * 찾은여부] = andmed_VALUE; }
            }
            if (eemaldama && 찾은여부 >= 0) { for (int Loop_INDEX = 찾은여부 + 1; Loop_INDEX < kirje_COUNT; Loop_INDEX++) { 힙[andmed_ARRAY + 2 * Loop_INDEX] = 힙[andmed_ARRAY + 2 + 2 * Loop_INDEX]; 힙[andmed_ARRAY + 1 + 2 * Loop_INDEX] = 힙[andmed_ARRAY + 3 + 2 * Loop_INDEX]; } 힙[andmed_ARRAY + 2 * kirje_COUNT] = 0; 힙[andmed_ARRAY + 1 + 2 * kirje_COUNT] = 0; 힙[objekt_viide + 3] = kirje_COUNT - 1; }
            if (Word_SMS(nimetus_konstant, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        tõrge_VALUE("unsupported collection method");
    }
    static boolean 잠금얻기(int objekt_viide) {
        if (!객체유효(objekt_viide)) return false;
        if (잠금깊이[objekt_viide] != 0 && lukk_omanik[objekt_viide] != tähtaja_piires_lõim + 1) { muutma_päring = true; return false; }
        lukk_omanik[objekt_viide] = tähtaja_piires_lõim + 1; 잠금깊이[objekt_viide]++; return true;
    }
    static void vabastama_lukk(int objekt_viide) {
        if (!객체유효(objekt_viide)) return;
        if (잠금깊이[objekt_viide] == 0 || lukk_omanik[objekt_viide] != tähtaja_piires_lõim + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[objekt_viide] == 0) lukk_omanik[objekt_viide] = 0;
    }
    static boolean SWITCH_lõim() {
        lõim_raam[tähtaja_piires_lõim] = raam_INDEX;
        if (raam_INDEX < tähtaja_piires_lõim * 32) lõim_Olek[tähtaja_piires_lõim] = 3;
        for (int Loop_INDEX = 0; Loop_INDEX < lõim_COUNT; Loop_INDEX++) if (lõim_Olek[Loop_INDEX] == 2 && lõim_Olek[가닥대기[Loop_INDEX]] == 3) lõim_Olek[Loop_INDEX] = 1;
        for (int Loop_INDEX = 1; Loop_INDEX <= lõim_COUNT; Loop_INDEX++) {
            int Edasi_ametikoht = (tähtaja_piires_lõim + Loop_INDEX) % lõim_COUNT;
            if (lõim_Olek[Edasi_ametikoht] == 1) { tähtaja_piires_lõim = Edasi_ametikoht; raam_INDEX = lõim_raam[Edasi_ametikoht]; muutma_päring = false; return true; }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < lõim_COUNT; Loop_INDEX++) if (lõim_Olek[Loop_INDEX] != 3) { tõrge_VALUE("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int nimetus_konstant, int 서술상수, int käsk_CODE) { Joonis_lõim(nimetus_konstant, 서술상수, käsk_CODE, false); }
    static void Joonis_lõim(int nimetus_konstant, int 서술상수, int käsk_CODE, boolean Eesti) {
        if (käsk_CODE == 184 && Word_SMS(nimetus_konstant, Eesti ? "YIELD_tööüksus" : "yield") && Word_SMS(서술상수, "()V")) { muutma_päring = true; return; }
        if (käsk_CODE == 184 && Word_SMS(nimetus_konstant, "currentThread") && Word_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(lõim_objekt[tähtaja_piires_lõim], 2); return; }
        if (käsk_CODE == 183 && Word_SMS(nimetus_konstant, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, Eesti ? "(LEesti/oma/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int siht_ADDRESS = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), objekt_viide = 빼기(2);
            if (!객체유효(objekt_viide)) return;
            if (힙[objekt_viide] == 13) { 힙[objekt_viide + 2] = siht_ADDRESS; 힙참조[objekt_viide + 2] = 1; }
            else if (siht_ADDRESS != 0) tõrge_VALUE("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (käsk_CODE == 182 && (Word_SMS(nimetus_konstant, Eesti ? "START_tööüksus" : "start") || Word_SMS(nimetus_konstant, Eesti ? "기다리기" : "join")) && Word_SMS(서술상수, "()V") || käsk_CODE == 182 && Word_SMS(nimetus_konstant, Eesti ? "살아있는가" : "isAlive") && Word_SMS(서술상수, "()Z")) {
            int objekt_viide = 빼기(2); if (!객체유효(objekt_viide)) return;
            int isik_VALUE = -1; for (int Loop_INDEX = 0; Loop_INDEX < lõim_COUNT; Loop_INDEX++) if (lõim_objekt[Loop_INDEX] == objekt_viide) isik_VALUE = Loop_INDEX;
            if (Word_SMS(nimetus_konstant, Eesti ? "살아있는가" : "isAlive")) { 넣기(isik_VALUE >= 0 && lõim_Olek[isik_VALUE] != 3 ? 1 : 0, 1); return; }
            if (Word_SMS(nimetus_konstant, Eesti ? "기다리기" : "join")) { if (isik_VALUE >= 0 && lõim_Olek[isik_VALUE] != 3) { 가닥대기[tähtaja_piires_lõim] = isik_VALUE; lõim_Olek[tähtaja_piires_lõim] = 2; muutma_päring = true; } return; }
            if (isik_VALUE >= 0) { 예외던짐(Eesti ? 38 : 16, "thread already started"); return; }
            if (lõim_COUNT == 4) { tõrge_VALUE("thread limit (4 including main)"); return; }
            int siht_ADDRESS = 힙[objekt_viide] == 13 ? 힙[objekt_viide + 2] : objekt_viide;
            int Fail_INDEX = siht_ADDRESS > 0 && 힙[siht_ADDRESS] >= 32 ? nimetus_meetod(힙[siht_ADDRESS] - 32, Eesti ? "Käivita" : "run", "()V") : -1;
            if (siht_ADDRESS != 0 && Fail_INDEX < 0) { tõrge_VALUE("Runnable.run required"); return; }
            isik_VALUE = lõim_COUNT++; lõim_objekt[isik_VALUE] = objekt_viide; lõim_siht[isik_VALUE] = siht_ADDRESS;
            int raam = isik_VALUE * 32; lõim_raam[isik_VALUE] = Fail_INDEX < 0 ? raam - 1 : raam; lõim_Olek[isik_VALUE] = Fail_INDEX < 0 ? 3 : 1;
            if (Fail_INDEX >= 0) { raam_meetod[raam] = Fail_INDEX; raam_ametikoht[raam] = meetod_START[Fail_INDEX]; kohalik_VALUE[raam * 128] = siht_ADDRESS; kohalik_TYPE[raam * 128] = 2; }
            return;
        }
        tõrge_VALUE("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], ADDRESS_SMS = new int[16];
    static int kohalik_ADDRESS() { return ADDRESS_objekt(0x7f000001); }
    static int ADDRESS_objekt(int VALUE) { int objekt_viide = lisama_salvesti(14, 1); if (!VIGA) 힙[objekt_viide + 2] = VALUE; return objekt_viide; }
    static int 주소해독(int objekt_viide) {
        if (objekt_viide == 0 || 글같음(objekt_viide, host_märk("localhost"), false)) return 0x7f000001;
        if (!objekt_VALUE(objekt_viide, 1)) return 0;
        int andmed_VALUE = 0, kokku_COUNT = 0, ADDRESS_bait = 0, 자릿수 = 0, kirje_COUNT = 힙[objekt_viide + 1];
        for (int Loop_INDEX = 0; Loop_INDEX <= kirje_COUNT; Loop_INDEX++) {
            int koodipunkt = Loop_INDEX == kirje_COUNT ? '.' : 힙[objekt_viide + 2 + Loop_INDEX];
            if (koodipunkt == '.') { if (자릿수 == 0 || kokku_COUNT == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } andmed_VALUE = andmed_VALUE << 8 | ADDRESS_bait; kokku_COUNT++; ADDRESS_bait = 자릿수 = 0; }
            else { if (koodipunkt < '0' || koodipunkt > '9' || ++자릿수 > 3 || (ADDRESS_bait = ADDRESS_bait * 10 + koodipunkt - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (kokku_COUNT != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return andmed_VALUE;
    }
    static int ADDRESS_märk(int andmed_VALUE) {
        int kirje_COUNT = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int ADDRESS_bait = andmed_VALUE >>> 이동비트 & 255;
            if (ADDRESS_bait >= 100) ADDRESS_SMS[kirje_COUNT++] = '0' + ADDRESS_bait / 100;
            if (ADDRESS_bait >= 10) ADDRESS_SMS[kirje_COUNT++] = '0' + ADDRESS_bait / 10 % 10;
            ADDRESS_SMS[kirje_COUNT++] = '0' + ADDRESS_bait % 10; if (이동비트 != 0) ADDRESS_SMS[kirje_COUNT++] = '.';
        }
        int objekt_viide = lisama_salvesti(1, kirje_COUNT); if (!VIGA) for (int Loop_INDEX = 0; Loop_INDEX < kirje_COUNT; Loop_INDEX++) 힙[objekt_viide + 2 + Loop_INDEX] = ADDRESS_SMS[Loop_INDEX]; return objekt_viide;
    }
    static void 통신호출(int omanik, int nimetus_konstant, int 서술상수, int käsk_CODE) {
        if (Word_SMS(omanik, "java/net/InetAddress")) {
            if (käsk_CODE == 184 && Word_SMS(nimetus_konstant, "getLoopbackAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(kohalik_ADDRESS(), 2); return; }
            if (käsk_CODE == 184 && Word_SMS(nimetus_konstant, "getByName") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int andmed_VALUE = 주소해독(빼기(2)); if (던진객체 == 0 && !VIGA) 넣기(ADDRESS_objekt(andmed_VALUE), 2); return;
            }
            if (käsk_CODE == 182 && Word_SMS(nimetus_konstant, "getHostAddress") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int objekt_viide = 빼기(2); if (objekt_VALUE(objekt_viide, 14)) 넣기(ADDRESS_märk(힙[objekt_viide + 2]), 2); return; }
        }
        if (Word_SMS(omanik, "java/net/DatagramPacket")) {
            if (käsk_CODE == 183 && Word_SMS(nimetus_konstant, "<init>") && (Word_SMS(서술상수, "([BI)V") || Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean sihtkoht_VALUE_viide = Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int pordinumber = sihtkoht_VALUE_viide ? 빼기(1) : 0, ADDRESS_viide = sihtkoht_VALUE_viide ? 빼기(2) : 0;
                int kirje_COUNT = 빼기(1), andmed_ARRAY = 빼기(2), objekt_viide = 빼기(2);
                if (!objekt_VALUE(objekt_viide, 16) || !objekt_VALUE(andmed_ARRAY, 20)) return;
                if (kirje_COUNT < 0 || kirje_COUNT > 힙[andmed_ARRAY + 1] || pordinumber < 0 || pordinumber > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (ADDRESS_viide != 0 && !objekt_VALUE(ADDRESS_viide, 14)) return;
                힙[objekt_viide + 2] = andmed_ARRAY; 힙참조[objekt_viide + 2] = 1; 힙[objekt_viide + 3] = kirje_COUNT;
                힙[objekt_viide + 4] = ADDRESS_viide; 힙참조[objekt_viide + 4] = 1; 힙[objekt_viide + 5] = pordinumber; return;
            }
            if (käsk_CODE == 182 && Word_SMS(nimetus_konstant, "setLength") && Word_SMS(서술상수, "(I)V")) {
                int kirje_COUNT = 빼기(1), objekt_viide = 빼기(2); if (!objekt_VALUE(objekt_viide, 16)) return;
                if (kirje_COUNT < 0 || kirje_COUNT > 힙[힙[objekt_viide + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[objekt_viide + 3] = kirje_COUNT; return;
            }
            if (käsk_CODE == 182 && (Word_SMS(nimetus_konstant, "getData") && Word_SMS(서술상수, "()[B") || Word_SMS(nimetus_konstant, "getLength") && Word_SMS(서술상수, "()I") || Word_SMS(nimetus_konstant, "getAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;") || Word_SMS(nimetus_konstant, "getPort") && Word_SMS(서술상수, "()I"))) {
                int objekt_viide = 빼기(2); if (!objekt_VALUE(objekt_viide, 16)) return;
                int kirje_ametikoht = Word_SMS(nimetus_konstant, "getData") ? 2 : Word_SMS(nimetus_konstant, "getLength") ? 3 : Word_SMS(nimetus_konstant, "getAddress") ? 4 : 5;
                넣기(힙[objekt_viide + kirje_ametikoht], kirje_ametikoht == 2 || kirje_ametikoht == 4 ? 2 : 1); return;
            }
        }
        if (Word_SMS(omanik, "java/net/DatagramSocket")) {
            if (käsk_CODE == 183 && Word_SMS(nimetus_konstant, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(I)V"))) {
                int pordinumber = Word_SMS(서술상수, "()V") ? 0 : 빼기(1), objekt_viide = 빼기(2); if (!objekt_VALUE(objekt_viide, 15)) return;
                if (pordinumber < 0 || pordinumber > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = kasutaja.avama_võrk(pordinumber); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[objekt_viide + 2] = 열린파일번호; return;
            }
            if (käsk_CODE == 182 && Word_SMS(nimetus_konstant, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), objekt_viide = 빼기(2); if (!objekt_VALUE(objekt_viide, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[objekt_viide + 3] = 밀리초값; return;
            }
            if (käsk_CODE == 182 && Word_SMS(nimetus_konstant, "getLocalPort") && Word_SMS(서술상수, "()I")) { int objekt_viide = 빼기(2); if (objekt_VALUE(objekt_viide, 15)) 넣기(힙[objekt_viide + 2] < 0 ? -1 : kasutaja.võrk_port(힙[objekt_viide + 2]), 1); return; }
            if (käsk_CODE == 182 && Word_SMS(nimetus_konstant, "isClosed") && Word_SMS(서술상수, "()Z")) { int objekt_viide = 빼기(2); if (objekt_VALUE(objekt_viide, 15)) 넣기(힙[objekt_viide + 2] < 0 ? 1 : 0, 1); return; }
            if (käsk_CODE == 182 && Word_SMS(nimetus_konstant, "close") && Word_SMS(서술상수, "()V")) { int objekt_viide = 빼기(2); if (objekt_VALUE(objekt_viide, 15) && 힙[objekt_viide + 2] >= 0) { kasutaja.파일서술자닫기(힙[objekt_viide + 2]); 힙[objekt_viide + 2] = -1; } return; }
            if (käsk_CODE == 182 && (Word_SMS(nimetus_konstant, "send") || Word_SMS(nimetus_konstant, "receive")) && Word_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int pakett = 빼기(2), objekt_viide = 빼기(2); if (!objekt_VALUE(pakett, 16) || !objekt_VALUE(objekt_viide, 15)) return;
                int andmed_ARRAY = 힙[pakett + 2], 유효길이 = 힙[pakett + 3], 열린파일번호 = 힙[objekt_viide + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_SMS(nimetus_konstant, "send")) {
                    if (!objekt_VALUE(힙[pakett + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < 유효길이; Loop_INDEX++) 통신임시[Loop_INDEX] = 힙[andmed_ARRAY + 2 + Loop_INDEX];
                    if (kasutaja.saatma_võrk(열린파일번호, 힙[힙[pakett + 4] + 2], 힙[pakett + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int kirje_COUNT = kasutaja.saama_võrk(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (kirje_COUNT == -11) {
                        int tähtaja_piires_Aeg = kasutaja.밀리초();
                        if (힙[objekt_viide + 4] == 0) 힙[objekt_viide + 4] = tähtaja_piires_Aeg + 1;
                        if (힙[objekt_viide + 3] > 0 && tähtaja_piires_Aeg - (힙[objekt_viide + 4] - 1) >= 힙[objekt_viide + 3]) { 힙[objekt_viide + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(objekt_viide, 2); 넣기(pakett, 2); raam_ametikoht[raam_INDEX] = 틀명령[raam_INDEX]; muutma_päring = true; return;
                    }
                    힙[objekt_viide + 4] = 0;
                    if (kirje_COUNT < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < kirje_COUNT; Loop_INDEX++) 힙[andmed_ARRAY + 2 + Loop_INDEX] = (byte)통신임시[Loop_INDEX];
                    힙[pakett + 3] = kirje_COUNT; 힙[pakett + 4] = ADDRESS_objekt(통신임시[513]); 힙참조[pakett + 4] = 1; 힙[pakett + 5] = 통신임시[512];
                }
                return;
            }
        }
        tõrge_VALUE("unsupported java.net method");
    }
    static boolean 흐름대기(int objekt_viide) {
        int tähtaja_piires_Aeg = kasutaja.밀리초();
        if (힙[objekt_viide + 5] == 0) 힙[objekt_viide + 5] = tähtaja_piires_Aeg + 1;
        if (힙[objekt_viide + 3] > 0 && tähtaja_piires_Aeg - (힙[objekt_viide + 5] - 1) >= 힙[objekt_viide + 3]) { 힙[objekt_viide + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        raam_ametikoht[raam_INDEX] = 틀명령[raam_INDEX]; muutma_päring = true; return true;
    }
    static void 흐름호출(int omanik, int nimetus_konstant, int 서술상수, int käsk_CODE) {
        boolean saama_leht = Word_SMS(omanik, "java/net/ServerSocket"), voog = Word_SMS(omanik, "java/io/InputStream") || Word_SMS(omanik, "java/io/OutputStream");
        if (!voog && käsk_CODE == 183 && Word_SMS(nimetus_konstant, "<init>")) {
            boolean 빈여부 = Word_SMS(서술상수, "()V"), 이름지정여부 = Word_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || saama_leht && Word_SMS(서술상수, "(I)V") || !saama_leht && (이름지정여부 || 주소지정여부))) { tõrge_VALUE("unsupported socket constructor"); return; }
            int pordinumber = 빈여부 ? 0 : 빼기(1), ADDRESS_viide = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, objekt_viide = 빼기(2);
            if (!objekt_VALUE(objekt_viide, saama_leht ? 18 : 17)) return;
            if (pordinumber < 0 || pordinumber > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !objekt_VALUE(ADDRESS_viide, 14)) return;
            int võrgu_ID = 이름지정여부 ? 주소해독(ADDRESS_viide) : 주소지정여부 ? 힙[ADDRESS_viide + 2] : 0x7f000001;
            if (VIGA || 던진객체 != 0) return;
            int 열린파일번호 = kasutaja.voog_meede(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : saama_leht ? kasutaja.voog_meede(1, 열린파일번호, pordinumber) : kasutaja.Ühenda_voog(열린파일번호, võrgu_ID, pordinumber);
            if (처리값 < 0) { kasutaja.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[objekt_viide + 2] = 열린파일번호; 힙[objekt_viide + 4] = pordinumber; 힙[objekt_viide + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!voog && Word_SMS(nimetus_konstant, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), objekt_viide = 빼기(2); if (!objekt_VALUE(objekt_viide, saama_leht ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[objekt_viide + 3] = 밀리초값; return; }
        if (!voog && Word_SMS(nimetus_konstant, "close") && Word_SMS(서술상수, "()V")) { int objekt_viide = 빼기(2); if (objekt_VALUE(objekt_viide, saama_leht ? 18 : 17) && 힙[objekt_viide + 2] >= 0) { kasutaja.파일서술자닫기(힙[objekt_viide + 2]); 힙[objekt_viide + 2] = -1; } return; }
        if (!voog && (Word_SMS(nimetus_konstant, "getLocalPort") || Word_SMS(nimetus_konstant, "getPort") || Word_SMS(nimetus_konstant, "isClosed") || Word_SMS(nimetus_konstant, "isConnected"))) {
            int objekt_viide = 빼기(2); if (!objekt_VALUE(objekt_viide, saama_leht ? 18 : 17)) return;
            넣기(Word_SMS(nimetus_konstant, "isClosed") ? 힙[objekt_viide + 2] < 0 ? 1 : 0 : Word_SMS(nimetus_konstant, "isConnected") ? 힙[objekt_viide + 6] : Word_SMS(nimetus_konstant, "getPort") ? 힙[objekt_viide + 4] : 힙[objekt_viide + 2] < 0 ? -1 : kasutaja.voog_meede(4, 힙[objekt_viide + 2], 0), 1); return;
        }
        if (saama_leht && Word_SMS(nimetus_konstant, "accept") && Word_SMS(서술상수, "()Ljava/net/Socket;")) {
            int objekt_viide = 빼기(2); if (!objekt_VALUE(objekt_viide, 18)) return; int 열린파일번호 = kasutaja.voog_meede(3, 힙[objekt_viide + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(objekt_viide)) 넣기(objekt_viide, 2); return; }
            힙[objekt_viide + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = lisama_salvesti(17, 5); if (VIGA) { kasutaja.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = kasutaja.voog_meede(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!saama_leht && !voog && ((Word_SMS(nimetus_konstant, "getInputStream") && Word_SMS(서술상수, "()Ljava/io/InputStream;")) || (Word_SMS(nimetus_konstant, "getOutputStream") && Word_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int objekt_viide = 빼기(2); if (!objekt_VALUE(objekt_viide, 17)) return; if (힙[objekt_viide + 2] < 0 || 힙[objekt_viide + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = lisama_salvesti(19, 4); if (VIGA) return; 힙[반환값 + 2] = objekt_viide; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Word_SMS(nimetus_konstant, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (voog) {
            boolean 읽기여부 = Word_SMS(nimetus_konstant, "read"), infotehnoloogia_kirjutamine_lõikus = Word_SMS(nimetus_konstant, "write"), plokk = Word_SMS(서술상수, "([B)I") || Word_SMS(서술상수, "([B)V"), infotehnoloogia_SUBARRAY = Word_SMS(서술상수, "([BII)I") || Word_SMS(서술상수, "([BII)V");
            int kirje_COUNT = infotehnoloogia_SUBARRAY ? 빼기(1) : 0, 시작변위 = infotehnoloogia_SUBARRAY ? 빼기(1) : 0, andmed_ARRAY = plokk || infotehnoloogia_SUBARRAY ? 빼기(2) : 0;
            int andmed_VALUE = infotehnoloogia_kirjutamine_lõikus && Word_SMS(서술상수, "(I)V") ? 빼기(1) : 0, objekt_viide = 빼기(2);
            if (!objekt_VALUE(objekt_viide, 19)) return; int ema_viide = 힙[objekt_viide + 2], 열린파일번호 = 힙[ema_viide + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_SMS(nimetus_konstant, "close") && Word_SMS(서술상수, "()V")) { kasutaja.파일서술자닫기(열린파일번호); 힙[ema_viide + 2] = -1; return; }
            if (Word_SMS(nimetus_konstant, "flush") && Word_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !infotehnoloogia_kirjutamine_lõikus) || 읽기여부 != (힙[objekt_viide + 3] == 0)) { tõrge_VALUE("unsupported stream operation"); return; }
            if (plokk || infotehnoloogia_SUBARRAY) { if (!objekt_VALUE(andmed_ARRAY, 20)) return; if (plokk) kirje_COUNT = 힙[andmed_ARRAY + 1]; if (시작변위 < 0 || kirje_COUNT < 0 || 시작변위 > 힙[andmed_ARRAY + 1] - kirje_COUNT) { 예외던짐(6, "stream array bounds"); return; } }
            else kirje_COUNT = 1;
            if (kirje_COUNT == 0) { if (읽기여부) 넣기(0, 1); return; }
            int Lõpetatud_COUNT = infotehnoloogia_kirjutamine_lõikus ? 힙[objekt_viide + 4] : 0, 처리값 = 0;
            while (Lõpetatud_COUNT < kirje_COUNT) {
                처리값 = 읽기여부 ? kasutaja.파일한바이트읽기(열린파일번호) : kasutaja.파일한바이트쓰기(열린파일번호, plokk || infotehnoloogia_SUBARRAY ? 힙[andmed_ARRAY + 2 + 시작변위 + Lõpetatud_COUNT] : andmed_VALUE);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (plokk || infotehnoloogia_SUBARRAY)) 힙[andmed_ARRAY + 2 + 시작변위 + Lõpetatud_COUNT] = (byte)처리값;
                Lõpetatud_COUNT++; if (읽기여부 && !(plokk || infotehnoloogia_SUBARRAY)) break;
            }
            if (처리값 == -11 && (infotehnoloogia_kirjutamine_lõikus || Lõpetatud_COUNT == 0)) {
                힙[objekt_viide + 4] = Lõpetatud_COUNT;
                if (흐름대기(ema_viide)) { 넣기(objekt_viide, 2); if (plokk || infotehnoloogia_SUBARRAY) 넣기(andmed_ARRAY, 2); if (infotehnoloogia_SUBARRAY) { 넣기(시작변위, 1); 넣기(kirje_COUNT, 1); } if (infotehnoloogia_kirjutamine_lõikus && !(plokk || infotehnoloogia_SUBARRAY)) 넣기(andmed_VALUE, 1); } return;
            }
            힙[objekt_viide + 4] = 0; 힙[ema_viide + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(Lõpetatud_COUNT == 0 && 처리값 == 256 ? -1 : plokk || infotehnoloogia_SUBARRAY ? Lõpetatud_COUNT : 처리값, 1); return;
        }
        tõrge_VALUE("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int nimetus_konstant) {
        if (Word_SMS(nimetus_konstant, "Eesti/oma/aken")) return 24;
        if (Word_SMS(nimetus_konstant, "Eesti/oma/Silt")) return 26;
        if (Word_SMS(nimetus_konstant, "Eesti/oma/nupp")) return 27;
        if (Word_SMS(nimetus_konstant, "Eesti/oma/tekstiväli")) return 28;
        if (Word_SMS(nimetus_konstant, "Eesti/oma/Toiming_teatamine")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int nimetus_konstant) {
        return 한국어화면종(nimetus_konstant) != 0 || Word_SMS(nimetus_konstant, "Eesti/oma/화면구성요소") || Word_SMS(nimetus_konstant, "Eesti/oma/sündmus_järjekord");
    }
    static int 화면종(int nimetus_konstant) {
        int 한국어종 = 한국어화면종(nimetus_konstant); if (한국어종 != 0) return 한국어종;
        if (Word_SMS(nimetus_konstant, "javax/swing/JFrame")) return 24;
        if (Word_SMS(nimetus_konstant, "javax/swing/JPanel")) return 25;
        if (Word_SMS(nimetus_konstant, "javax/swing/JLabel")) return 26;
        if (Word_SMS(nimetus_konstant, "javax/swing/JButton")) return 27;
        if (Word_SMS(nimetus_konstant, "javax/swing/JTextField")) return 28;
        if (Word_SMS(nimetus_konstant, "java/awt/event/ActionEvent")) return 29;
        if (Word_SMS(nimetus_konstant, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int nimetus_konstant) {
        return 화면종(nimetus_konstant) != 0 || Word_SMS(nimetus_konstant, "java/awt/Component") || Word_SMS(nimetus_konstant, "java/awt/Container") || Word_SMS(nimetus_konstant, "javax/swing/JComponent") || Word_SMS(nimetus_konstant, "javax/swing/AbstractButton") || Word_SMS(nimetus_konstant, "javax/swing/text/JTextComponent") || Word_SMS(nimetus_konstant, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int objekt_viide) { if (!객체유효(objekt_viide)) return false; if (힙[objekt_viide] < 24 || 힙[objekt_viide] > 28) { tõrge_VALUE("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int objekt_viide, int SMS_viide) {
        if (SMS_viide != 0 && !objekt_VALUE(SMS_viide, 1)) return;
        int kirje_COUNT = SMS_viide == 0 ? 0 : 힙[SMS_viide + 1]; if (kirje_COUNT > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < kirje_COUNT; Loop_INDEX++) 화면글임시[Loop_INDEX] = 힙[SMS_viide + 2 + Loop_INDEX];
        if (kasutaja.화면글(힙[objekt_viide + 2], 화면글임시, kirje_COUNT) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[objekt_viide + 3] = SMS_viide; 힙참조[objekt_viide + 3] = 1;
    }
    static int 화면문자읽기(int objekt_viide) {
        int isik_VALUE = 힙[objekt_viide + 2], kirje_COUNT = kasutaja.화면연결(8, isik_VALUE, 0, 0, 0, 0), 사용수 = 0;
        if (kirje_COUNT < 0) { tõrge_VALUE("GUI text read failed"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < kirje_COUNT; Loop_INDEX++) { int 부호값 = kasutaja.화면연결(9, isik_VALUE, Loop_INDEX, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = lisama_salvesti(1, 사용수); if (!VIGA) for (int Loop_INDEX = 0; Loop_INDEX < 사용수; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 화면글임시[Loop_INDEX]; return 반환값;
    }
    /* Eesti 객체를 직접 만들고 tuum_VALUE 화면 기능에 연결한다. Swing objekt_VALUE/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int omanik, int nimetus_konstant, int 서술상수, int käsk_CODE) {
        if (Word_SMS(omanik, "Eesti/oma/sündmus_järjekord")) {
            if (käsk_CODE == 184 && Word_SMS(nimetus_konstant, "나중에실행") && Word_SMS(서술상수, "(LEesti/oma/실행할일;)V")) {
                int tööüksus_Toiming = 빼기(2); if (!객체유효(tööüksus_Toiming)) return;
                if (나중수 == 8) { tõrge_VALUE("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = tööüksus_Toiming; return;
            }
            if (käsk_CODE == 184 && Word_SMS(nimetus_konstant, "사건처리중인가") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            tõrge_VALUE("지원하지 않는 Eesti 화면 일정 호출"); return;
        }
        if (Word_SMS(omanik, "Eesti/oma/Toiming_teatamine")) {
            int teatamine = 빼기(2); if (!objekt_VALUE(teatamine, 29) || 힙[teatamine + 3] == 0) return;
            if (Word_SMS(nimetus_konstant, "sündmuse_allikas") && Word_SMS(서술상수, "()LEesti/oma/화면구성요소;")) 넣기(힙[teatamine + 2], 2);
            else if (Word_SMS(nimetus_konstant, "käsk_SMS") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[teatamine + 2]), 2);
            else if (Word_SMS(nimetus_konstant, "INDEX") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else tõrge_VALUE("지원하지 않는 Eesti Nimi teatamine 호출"); return;
        }
        if (käsk_CODE == 183 && Word_SMS(nimetus_konstant, "<init>")) {
            int 종류 = 한국어화면종(omanik), 받이 = 0, 가로 = 0, vertikaal_ametikoht = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Word_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (kasutaja.화면너비() - 폭) / 2; vertikaal_ametikoht = (kasutaja.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Word_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Word_SMS(서술상수, "(Ljava/lang/String;IIIILEesti/oma/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); vertikaal_ametikoht = 빼기(1); 가로 = 빼기(1);
            } else { tõrge_VALUE("지원하지 않는 Eesti 화면 생성자"); return; }
            int Tekst = 빼기(2), element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || vertikaal_ametikoht < 0 || 폭 > kasutaja.화면너비() - 가로 || 높이 > kasutaja.화면높이() - vertikaal_ametikoht) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDEX = kasutaja.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (INDEX < 1 || INDEX > 32) { tõrge_VALUE("화면 element_VALUE 자리가 가득 찼습니다"); return; }
            힙[element_VALUE + 2] = INDEX; 화면참조[INDEX - 1] = element_VALUE;
            힙[element_VALUE + 5] = 가로; 힙[element_VALUE + 6] = vertikaal_ametikoht; 힙[element_VALUE + 7] = 폭; 힙[element_VALUE + 8] = 높이; 힙[element_VALUE + 10] = 2;
            힙[element_VALUE + 4] = 받이; 힙참조[element_VALUE + 4] = 1; 힙[element_VALUE + 12] = 1;
            kasutaja.화면연결(1, INDEX, 가로, vertikaal_ametikoht, 폭, 높이);
            if (종류 == 24) kasutaja.화면연결(7, INDEX, 2, 0, 0, 0);
            화면문자설정(element_VALUE, Tekst); return;
        }
        if (käsk_CODE != 182) { tõrge_VALUE("잘못된 Eesti 화면 호출 Käsk"); return; }
        if (Word_SMS(nimetus_konstant, "kirjutamine_SMS") && Word_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int Tekst = 빼기(2), element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 화면문자설정(element_VALUE, Tekst); return;
        }
        if (Word_SMS(nimetus_konstant, "글읽기") && Word_SMS(서술상수, "()Ljava/lang/String;")) {
            int element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 넣기(화면문자읽기(element_VALUE), 2); return;
        }
        if (Word_SMS(nimetus_konstant, "동작맡기기") && Word_SMS(서술상수, "(LEesti/oma/동작받이;)V")) {
            int 받이 = 빼기(2), element_VALUE = 빼기(2);
            if (화면객체(element_VALUE)) { 힙[element_VALUE + 4] = 받이; 힙참조[element_VALUE + 4] = 1; 힙[element_VALUE + 12] = 1; } return;
        }
        if (Word_SMS(nimetus_konstant, "Lisa_element") && Word_SMS(서술상수, "(LEesti/oma/화면구성요소;)V")) {
            int laps_VALUE = 빼기(2), ema_VALUE = 빼기(2); if (!화면객체(laps_VALUE) || !화면객체(ema_VALUE)) return;
            if (kasutaja.화면연결(2, 힙[ema_VALUE + 2], 힙[laps_VALUE + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[laps_VALUE + 11] = ema_VALUE; 힙참조[laps_VALUE + 11] = 1; return;
        }
        if (Word_SMS(nimetus_konstant, "자리정하기") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), vertikaal_ametikoht = 빼기(1), 가로 = 빼기(1), element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (kasutaja.화면연결(1, 힙[element_VALUE + 2], 가로, vertikaal_ametikoht, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[element_VALUE + 5] = 가로; 힙[element_VALUE + 6] = vertikaal_ametikoht; 힙[element_VALUE + 7] = 폭; 힙[element_VALUE + 8] = 높이; return;
        }
        if ((Word_SMS(nimetus_konstant, "saade_aken") || Word_SMS(nimetus_konstant, "Suletud")) && Word_SMS(서술상수, "()V")) {
            boolean nähtavus_VALUE = Word_SMS(nimetus_konstant, "saade_aken"); int element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (kasutaja.화면연결(nähtavus_VALUE ? 3 : 4, 힙[element_VALUE + 2], nähtavus_VALUE ? 1 : 0, 0, 0, 0) < 0) { tõrge_VALUE("화면은 대화형 명령에서 실행해야 합니다"); return; }
            힙[element_VALUE + 9] = nähtavus_VALUE ? 1 : 0; return;
        }
        if (Word_SMS(nimetus_konstant, "보이는가") && Word_SMS(서술상수, "()Z")) { int element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 넣기(힙[element_VALUE + 9], 1); return; }
        tõrge_VALUE("지원하지 않는 Eesti 화면 meetod_VALUE");
    }
    static void 화면호출(int omanik, int nimetus_konstant, int 서술상수, int käsk_CODE) {
        if (Word_SMS(omanik, "javax/swing/SwingUtilities")) {
            if (käsk_CODE == 184 && Word_SMS(nimetus_konstant, "invokeLater") && Word_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int objekt_viide = 빼기(2); if (!객체유효(objekt_viide)) return; if (나중수 == 8) { tõrge_VALUE("invokeLater queue full"); return; } 나중실행[나중수++] = objekt_viide; return; }
            if (käsk_CODE == 184 && Word_SMS(nimetus_konstant, "isEventDispatchThread") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            tõrge_VALUE("unsupported SwingUtilities method"); return;
        }
        if (Word_SMS(omanik, "java/awt/event/ActionEvent")) {
            int objekt_viide = 빼기(2); if (!objekt_VALUE(objekt_viide, 29)) return;
            if (Word_SMS(nimetus_konstant, "getSource") && Word_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[objekt_viide + 2], 2);
            else if (Word_SMS(nimetus_konstant, "getActionCommand") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[objekt_viide + 2]), 2);
            else if (Word_SMS(nimetus_konstant, "getID") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else tõrge_VALUE("unsupported ActionEvent method"); return;
        }
        if (käsk_CODE == 183 && Word_SMS(nimetus_konstant, "<init>")) {
            int COLUMNS = 0, SMS_viide = 0;
            if (Word_SMS(서술상수, "(I)V")) COLUMNS = 빼기(1);
            else if (Word_SMS(서술상수, "(Ljava/lang/String;I)V")) { COLUMNS = 빼기(1); SMS_viide = 빼기(2); }
            else if (Word_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_viide = 빼기(2);
            else if (Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_SMS(서술상수, "()V")) { tõrge_VALUE("unsupported Swing constructor"); return; }
            int objekt_viide = 빼기(2); if (!객체유효(objekt_viide)) return;
            if (힙[objekt_viide] == 30) { tõrge_VALUE("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(objekt_viide) || COLUMNS < 0) return;
            int isik_VALUE = kasutaja.화면연결(0, 힙[objekt_viide] - 23, 0, 0, 0, 0);
            if (isik_VALUE < 1 || isik_VALUE > 32) { tõrge_VALUE("GUI widget slots exhausted"); return; }
            힙[objekt_viide + 2] = isik_VALUE; 화면참조[isik_VALUE - 1] = objekt_viide; 힙[objekt_viide + 5] = 힙[objekt_viide] == 24 ? 130 : 16; 힙[objekt_viide + 6] = 힙[objekt_viide] == 24 ? 110 : 16;
            힙[objekt_viide + 7] = 힙[objekt_viide] == 24 ? 380 : 220; 힙[objekt_viide + 8] = 힙[objekt_viide] == 24 ? 240 : 28; 힙[objekt_viide + 10] = 1;
            화면문자설정(objekt_viide, SMS_viide); return;
        }
        if (Word_SMS(nimetus_konstant, "setText") || Word_SMS(nimetus_konstant, "setTitle")) { int SMS_viide = 빼기(2), objekt_viide = 빼기(2); if (화면객체(objekt_viide) && Word_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(objekt_viide, SMS_viide); return; }
        if (Word_SMS(nimetus_konstant, "getText") || Word_SMS(nimetus_konstant, "getTitle")) { int objekt_viide = 빼기(2); if (화면객체(objekt_viide) && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(objekt_viide), 2); return; }
        if (Word_SMS(nimetus_konstant, "addActionListener") && Word_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int saama_viide = 빼기(2), objekt_viide = 빼기(2); if (화면객체(objekt_viide)) { 힙[objekt_viide + 4] = saama_viide; 힙참조[objekt_viide + 4] = 1; } return; }
        if (Word_SMS(nimetus_konstant, "getContentPane") && Word_SMS(서술상수, "()Ljava/awt/Container;")) { int objekt_viide = 빼기(2); if (화면객체(objekt_viide)) 넣기(objekt_viide, 2); return; }
        if (Word_SMS(nimetus_konstant, "setLayout") && Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int küljend_viide = 빼기(2), objekt_viide = 빼기(2); if (화면객체(objekt_viide) && küljend_viide != 0) tõrge_VALUE("only absolute layout (null) is supported"); return; }
        if (Word_SMS(nimetus_konstant, "add") && (Word_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean küljend_tingimus = Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (küljend_tingimus) 빼기(2);
            int laps_viide = 빼기(2), objekt_viide = 빼기(2); if (!화면객체(laps_viide) || !화면객체(objekt_viide)) return;
            if (kasutaja.화면연결(2, 힙[objekt_viide + 2], 힙[laps_viide + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[laps_viide + 11] = objekt_viide; 힙참조[laps_viide + 11] = 1; if (!küljend_tingimus) 넣기(laps_viide, 2); return;
        }
        if (Word_SMS(nimetus_konstant, "setBounds") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), 가로좌표 = 빼기(1), objekt_viide = 빼기(2); if (!화면객체(objekt_viide)) return;
            if (kasutaja.화면연결(1, 힙[objekt_viide + 2], 가로좌표, 세로좌표, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[objekt_viide + 5] = 가로좌표; 힙[objekt_viide + 6] = 세로좌표; 힙[objekt_viide + 7] = 너비; 힙[objekt_viide + 8] = 높이; return;
        }
        if (Word_SMS(nimetus_konstant, "setSize") && Word_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), objekt_viide = 빼기(2); if (!화면객체(objekt_viide)) return;
            if (kasutaja.화면연결(1, 힙[objekt_viide + 2], 힙[objekt_viide + 5], 힙[objekt_viide + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[objekt_viide + 7] = 너비; 힙[objekt_viide + 8] = 높이; } return;
        }
        if (Word_SMS(nimetus_konstant, "setLocationRelativeTo") && Word_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), objekt_viide = 빼기(2); if (!화면객체(objekt_viide)) return; if (상대배치 != 0) { tõrge_VALUE("only screen centering supported"); return; } 힙[objekt_viide + 5] = (kasutaja.화면너비() - 힙[objekt_viide + 7]) / 2; 힙[objekt_viide + 6] = (kasutaja.화면높이() - 힙[objekt_viide + 8]) / 2; kasutaja.화면연결(1, 힙[objekt_viide + 2], 힙[objekt_viide + 5], 힙[objekt_viide + 6], 힙[objekt_viide + 7], 힙[objekt_viide + 8]); return; }
        if (Word_SMS(nimetus_konstant, "setDefaultCloseOperation") && Word_SMS(서술상수, "(I)V")) { int eeskirjad = 빼기(1), objekt_viide = 빼기(2); if (화면객체(objekt_viide)) { if (eeskirjad < 0 || eeskirjad > 3) 예외던짐(9, "close policy"); else { 힙[objekt_viide + 10] = eeskirjad; kasutaja.화면연결(7, 힙[objekt_viide + 2], eeskirjad, 0, 0, 0); } } return; }
        if (Word_SMS(nimetus_konstant, "setVisible") && Word_SMS(서술상수, "(Z)V")) { int andmed_VALUE = 빼기(1), objekt_viide = 빼기(2); if (화면객체(objekt_viide)) { int 처리값 = kasutaja.화면연결(3, 힙[objekt_viide + 2], andmed_VALUE, 0, 0, 0); if (처리값 < 0) tõrge_VALUE("Swing requires a standalone interactive command"); else 힙[objekt_viide + 9] = andmed_VALUE; } return; }
        if (Word_SMS(nimetus_konstant, "dispose") && Word_SMS(서술상수, "()V")) { int objekt_viide = 빼기(2); if (화면객체(objekt_viide)) { kasutaja.화면연결(4, 힙[objekt_viide + 2], 0, 0, 0, 0); 힙[objekt_viide + 9] = 0; } return; }
        if (Word_SMS(nimetus_konstant, "repaint") || Word_SMS(nimetus_konstant, "validate")) { int objekt_viide = 빼기(2); if (!화면객체(objekt_viide) || !Word_SMS(서술상수, "()V")) return; kasutaja.화면연결(1, 힙[objekt_viide + 2], 힙[objekt_viide + 5], 힙[objekt_viide + 6], 힙[objekt_viide + 7], 힙[objekt_viide + 8]); return; }
        if (Word_SMS(nimetus_konstant, "isVisible") && Word_SMS(서술상수, "()Z")) { int objekt_viide = 빼기(2); if (화면객체(objekt_viide)) 넣기(힙[objekt_viide + 9], 1); return; }
        tõrge_VALUE("unsupported Swing method (native subset)");
    }
    static void lähetus_sündmus(int siht_ADDRESS, int sündmus_number, boolean Eesti) {
        if (siht_ADDRESS < 1 || 힙[siht_ADDRESS] < 32) { tõrge_VALUE("Java event listener required"); return; }
        int Fail_INDEX = nimetus_meetod(힙[siht_ADDRESS] - 32, sündmus_number == 0 ? (Eesti ? "Käivita" : "run") : (Eesti ? "saama_Toiming" : "actionPerformed"), sündmus_number == 0 ? "()V" : (Eesti ? "(LEesti/oma/Toiming_teatamine;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (Fail_INDEX < 0) { tõrge_VALUE("event callback missing"); return; }
        tähtaja_piires_lõim = 0; lõim_COUNT = 1; raam_INDEX = 0; lõim_Olek[0] = 1; raam_Virn[0] = 0; raam_lukk[0] = 틀초기화[0] = 0; muutma_päring = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 128; Loop_INDEX++) { kohalik_VALUE[Loop_INDEX] = kohalik_TYPE[Loop_INDEX] = 0; }
        raam_meetod[0] = Fail_INDEX; raam_ametikoht[0] = meetod_START[Fail_INDEX]; kohalik_VALUE[0] = siht_ADDRESS; kohalik_TYPE[0] = 2;
        if (sündmus_number != 0) { kohalik_VALUE[1] = sündmus_number; kohalik_TYPE[1] = 2; }
        사건중 = true; Täida_käsk(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!VIGA) {
            if (나중수 > 0) { int siht_ADDRESS = 나중실행[0], Eesti = 나중한국어[0]; for (int Loop_INDEX = 1; Loop_INDEX < 나중수; Loop_INDEX++) { 나중실행[Loop_INDEX - 1] = 나중실행[Loop_INDEX]; 나중한국어[Loop_INDEX - 1] = 나중한국어[Loop_INDEX]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; lähetus_sündmus(siht_ADDRESS, 0, Eesti != 0); continue; }
            if (kasutaja.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int sündmus_number = kasutaja.화면연결(5, 0, 0, 0, 0, 0); if (sündmus_number == 0) continue;
            if (sündmus_number < 0) { tõrge_VALUE("GUI event I/O failed"); return; }
            int isik_VALUE = sündmus_number & 65535; if (isik_VALUE < 1 || isik_VALUE > 32) continue; int objekt_viide = 화면참조[isik_VALUE - 1]; if (objekt_viide == 0) continue;
            if ((sündmus_number & 65536) != 0) {
                if (힙[objekt_viide + 10] != 0) 힙[objekt_viide + 9] = 0;
                if (힙[objekt_viide + 10] == 3) for (int Loop_INDEX = 0; Loop_INDEX < 32; Loop_INDEX++) if (화면참조[Loop_INDEX] != 0 && 힙[화면참조[Loop_INDEX]] == 24) kasutaja.화면연결(4, Loop_INDEX + 1, 0, 0, 0, 0);
            } else if (힙[objekt_viide + 4] != 0) {
                int 안내참조 = lisama_salvesti(29, 2); if (VIGA) return; 힙[안내참조 + 2] = objekt_viide; 힙[안내참조 + 3] = 힙[objekt_viide + 12]; 힙참조[안내참조 + 2] = 1; lähetus_sündmus(힙[objekt_viide + 4], 안내참조, 힙[objekt_viide + 12] != 0);
            }
        }
    }
    public static int Käivita_2() {
        if (kasutaja.인수개수() == 1 && 자바도구.같음(kasutaja.Argumendid(0), "-version")) {
            kasutaja.Kirjutamine("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (kasutaja.인수개수() < 1) { kasutaja.Kirjutamine("Usage: java CLASS [ARGS]\n"); return 2; }
        kirje_tund_Sõnaseletus = koormus_tund_Sõnaseletus(host_märk(kasutaja.Argumendid(0))); if (VIGA || kirje_tund_Sõnaseletus < 0) return 1;
        int kirje_p_VALUE = nimetus_meetod(kirje_tund_Sõnaseletus, "Käivita_2", "()V");
        boolean 한국어진입 = kirje_p_VALUE >= 0 && (meetod_pöördus[kirje_p_VALUE] & 9) == 9;
        if (!한국어진입) kirje_p_VALUE = nimetus_meetod(kirje_tund_Sõnaseletus, "main", "([Ljava/lang/String;)V");
        if (kirje_p_VALUE < 0 || (meetod_pöördus[kirje_p_VALUE] & 9) != 9) tõrge_VALUE("public static void Käivita_2() or main(String[] args) required");
        if (VIGA) return 1;
        int Argumendid = lisama_salvesti(3, kasutaja.인수개수() - 1); massiivi_element[Argumendid] = -1;
        for (int number = 1; number < kasutaja.인수개수() && !VIGA; number++) 힙[Argumendid + 1 + number] = host_märk(kasutaja.Argumendid(number));
        raam_INDEX = 0; raam_meetod[0] = kirje_p_VALUE; raam_ametikoht[0] = meetod_START[kirje_p_VALUE]; kohalik_VALUE[0] = 한국어진입 ? 0 : Argumendid; kohalik_TYPE[0] = 한국어진입 ? 0 : 2;
        lõim_Olek[0] = 1; lõim_objekt[0] = lisama_salvesti(13, 2);
        Täida_käsk(); if (!VIGA) 화면사건들(); return VIGA ? 1 : 0;
    }
}
