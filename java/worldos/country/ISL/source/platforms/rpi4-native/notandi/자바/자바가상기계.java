// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Skrá/스택/tilvísun/grein 경계를 keyra_skipun 중 검사한다. */
public final class 자바가상기계 {
    static int[] Skrá = new int[16 * 16384], 임시파일 = new int[16384], skrá_heiti_SMS = new int[512];
    static int[] fasti_merki = new int[8192], 상가 = new int[8192], fasti_SECOND_VALUE = new int[8192], strengur_tilvísun = new int[8192];
    static int[] aðferð_heiti_SMS = new int[512], aðferð_TYPE = new int[512], aðferð_aðgangur = new int[512], aðferð_eigandi = new int[512];
    static int[] aðferð_Opna = new int[512], aðferð_ljúka = new int[512], aðferð_bunki = new int[512], 함수지역 = new int[512];
    static int[] aðferð_frumbreyta_COUNT = new int[512], aðferð_frumbreyta_TYPE = new int[8192], aðferð_skila = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] staðbundið_VALUE = new int[16384], staðbundið_TYPE = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] ramma_aðferð = new int[128], ramma_staða = new int[128], ramma_bunki = new int[128], ramma_skipun = new int[128], frumstilla_ramma = new int[128];
    static int[] klasi_Skilgreining_heiti = new int[16], klasi_Skilgreining_breyta_stærð = new int[16], klasi_Skilgreining_yfireining = new int[16], klasi_Skilgreining_staða = new int[16], klasi_rauf_COUNT = new int[16], frumstilla_klasi_Skilgreining = new int[16];
    static int[] klasi_viðmót = new int[16 * 16], klasi_viðmót_COUNT = new int[16];
    static int[] rauf_heiti = new int[512], rauf_TYPE = new int[512], rauf_eigandi = new int[512], rauf_Heimildir = new int[512], rauf_staða = new int[512], rauf_gögn = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], ARRAY_eining = new int[32768], Store_heiltala = new int[256];
    static int Stærð, 읽기위치, aðferð_COUNT, klasi_heiti, ramma_INDEX = -1, 힙끝 = 1, skila_TYPE;
    static int klasi_Skilgreining_COUNT, rauf_COUNT, 잡기수, 현재읽는종, 던진객체, 잠시수, birta_COUNT, Safn_COUNT;
    static int 현재가닥, þráður_COUNT = 1, færsla_klasi_Skilgreining;
    static int[] þráður_ramma = new int[4], þráður_staða = new int[4], þráður_hlutur = new int[4], þráður_markmið = new int[4], 가닥대기 = new int[4];
    static boolean Villa, 바꿈요청;
    static int[] Loka_eigandi = new int[32768], 잠금깊이 = new int[32768], ramma_Loka = new int[128], klasi_Loka = new int[16], klasi_þráður = new int[16];

    static void bilun_VALUE(String Word_SMS) {
        if (Villa) return;
        int tegund_CODE = 0;
        if (자바도구.같음(Word_SMS, "ArithmeticException: / by zero")) tegund_CODE = 4;
        if (자바도구.같음(Word_SMS, "NullPointerException") || 자바도구.같음(Word_SMS, "null or invalid array")) tegund_CODE = 5;
        if (자바도구.같음(Word_SMS, "ArrayIndexOutOfBoundsException")) tegund_CODE = 7;
        if (자바도구.같음(Word_SMS, "StringIndexOutOfBoundsException")) tegund_CODE = 8;
        if (자바도구.같음(Word_SMS, "NumberFormatException")) tegund_CODE = 10;
        if (자바도구.같음(Word_SMS, "FileNotFoundException: file open failed")) tegund_CODE = 12;
        if (자바도구.같음(Word_SMS, "IOException: stream closed") || 자바도구.같음(Word_SMS, "IOException: read failed") || 자바도구.같음(Word_SMS, "IOException: write failed")) tegund_CODE = 11;
        if (자바도구.같음(Word_SMS, "ClassCastException")) tegund_CODE = 14;
        if (자바도구.같음(Word_SMS, "NegativeArraySizeException")) tegund_CODE = 15;
        if (tegund_CODE != 0 && ramma_INDEX >= 0) { 예외던짐(tegund_CODE, Word_SMS); return; }
        notandi.Skrift("JVM error: "); notandi.Skrift(Word_SMS); notandi.skrifa_stafur_VALUE(10); Villa = true;
    }
    static boolean miðlaskrá(int Keyra_2, int lengd_VALUE) {
        if (Keyra_2 < 0 || Keyra_2 >= Skrá.length || lengd_VALUE < 0) return false;
        int klasi_Skilgreining = Keyra_2 / 16384;
        return Keyra_2 % 16384 <= klasi_Skilgreining_breyta_stærð[klasi_Skilgreining] && lengd_VALUE <= klasi_Skilgreining_breyta_stærð[klasi_Skilgreining] - Keyra_2 % 16384;
    }
    static int bæti_VALUE() {
        if (!miðlaskrá(읽기위치, 1)) { bilun_VALUE("truncated class file"); return 0; }
        return Skrá[읽기위치++];
    }
    static int 짧은수() { return bæti_VALUE() << 8 | bæti_VALUE(); }
    static int heiltala() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int lengd_VALUE) { if (!miðlaskrá(읽기위치, lengd_VALUE)) bilun_VALUE("invalid attribute size"); else 읽기위치 += lengd_VALUE; }
    static boolean athuga_fasti(int númer, int 종류) {
        if (númer <= 0 || númer >= fasti_merki.length || fasti_merki[númer] != 종류) { bilun_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Keyra_2, int lengd_VALUE, String Word_SMS) {
        if (!miðlaskrá(Keyra_2, lengd_VALUE)) return false;
        int 읽는자리 = Keyra_2, 끝 = Keyra_2 + lengd_VALUE;
        for (int Loop_INDEX = 0; Loop_INDEX < Word_SMS.length(); Loop_INDEX++) {
            int stafkóði = Word_SMS.charAt(Loop_INDEX);
            if (stafkóði > 0 && stafkóði < 128) { if (읽는자리 >= 끝 || Skrá[읽는자리++] != stafkóði) return false; }
            else if (stafkóði < 2048) {
                if (읽는자리 + 2 > 끝 || Skrá[읽는자리++] != (192 | (stafkóði >> 6)) || Skrá[읽는자리++] != (128 | (stafkóði & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Skrá[읽는자리++] != (224 | (stafkóði >> 12)) || Skrá[읽는자리++] != (128 | ((stafkóði >> 6) & 63)) || Skrá[읽는자리++] != (128 | (stafkóði & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean Word_SMS(int fasti_VALUE, String Word_SMS) { return athuga_fasti(fasti_VALUE, 1) && 구간(상가[fasti_VALUE], fasti_SECOND_VALUE[fasti_VALUE], Word_SMS); }
    static boolean samsvörun_Word(int 가, int 나) {
        if (!athuga_fasti(가, 1) || !athuga_fasti(나, 1) || fasti_SECOND_VALUE[가] != fasti_SECOND_VALUE[나]) return false;
        for (int númer = 0; númer < fasti_SECOND_VALUE[가]; númer++) if (Skrá[상가[가] + númer] != Skrá[상가[나] + númer]) return false;
        return true;
    }
    static int klasi_heiti_SMS(int númer) { return athuga_fasti(númer, 7) && athuga_fasti(상가[númer], 1) ? 상가[númer] : 0; }
    static int tilvísun_heiti(int númer) { return athuga_fasti(númer, 12) && athuga_fasti(상가[númer], 1) ? 상가[númer] : 0; }
    static int tilvísun_TYPE(int númer) { return athuga_fasti(númer, 12) && athuga_fasti(fasti_SECOND_VALUE[númer], 1) ? fasti_SECOND_VALUE[númer] : 0; }
    static int 서술형(int 끝, boolean autt_TYPE) {
        if (읽기위치 >= 끝) { bilun_VALUE("invalid descriptor"); return 0; }
        int VALUE = bæti_VALUE();
        if (VALUE == 'V' && autt_TYPE) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int Keyra_2 = 읽기위치;
            while (읽기위치 < 끝 && Skrá[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Keyra_2) bilun_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        bilun_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int fall_VALUE) {
        int 이전 = 읽기위치, númer = aðferð_TYPE[fall_VALUE];
        if (!athuga_fasti(númer, 1)) return;
        읽기위치 = 상가[númer]; int 끝 = 읽기위치 + fasti_SECOND_VALUE[númer];
        if (bæti_VALUE() != '(') bilun_VALUE("invalid method descriptor");
        int vara_COUNT = 0;
        while (!Villa && 읽기위치 < 끝 && Skrá[읽기위치] != ')') {
            if (vara_COUNT == 16) { bilun_VALUE("too many method arguments"); break; }
            aðferð_frumbreyta_TYPE[fall_VALUE * 16 + vara_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || bæti_VALUE() != ')') bilun_VALUE("invalid method descriptor");
        aðferð_skila[fall_VALUE] = 서술형(끝, true); aðferð_frumbreyta_COUNT[fall_VALUE] = vara_COUNT;
        if (읽기위치 != 끝) bilun_VALUE("invalid method descriptor");
        읽기위치 = 이전;
    }
    static int 상번호() { int VALUE = 짧은수(); return VALUE == 0 ? 0 : 현재읽는종 * 512 + VALUE; }
    static int 명상수() { return aðferð_eigandi[ramma_aðferð[ramma_INDEX]] * 512 + 명짧(); }
    static void 속성건너() {
        int vara_COUNT = 짧은수();
        for (int númer = 0; númer < vara_COUNT && !Villa; númer++) { athuga_fasti(상번호(), 1); 건너(heiltala()); }
    }
    static int skipun_lengd(int VALUE) {
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
    static int staða_heiltala(int 읽는자리) {
        if (!miðlaskrá(읽는자리, 4)) { bilun_VALUE("truncated bytecode operand"); return 0; }
        return Skrá[읽는자리] << 24 | Skrá[읽는자리 + 1] << 16 | Skrá[읽는자리 + 2] << 8 | Skrá[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Keyra_2, int 끝) {
        int VALUE = Skrá[읽는자리], lengd_VALUE = skipun_lengd(VALUE);
        if (VALUE == 170 || VALUE == 171) {
            int BASE_staða = 읽는자리 + 1;
            while ((BASE_staða - Keyra_2) % 4 != 0) BASE_staða++;
            if (끝 - BASE_staða < (VALUE == 170 ? 12 : 8)) return 0;
            int færsla_COUNT = VALUE == 170 ? staða_heiltala(BASE_staða + 8) - staða_heiltala(BASE_staða + 4) + 1 : staða_heiltala(BASE_staða + 4);
            if (færsla_COUNT < 0 || færsla_COUNT > 2048) return 0;
            lengd_VALUE = BASE_staða - 읽는자리 + (VALUE == 170 ? 12 + 4 * færsla_COUNT : 8 + 8 * færsla_COUNT);
        }
        if (VALUE == 196 && 읽는자리 + 1 < 끝) {
            int Word_gögn = Skrá[읽는자리 + 1]; lengd_VALUE = Word_gögn == 132 ? 6 : (Word_gögn == 21 || Word_gögn == 25 || Word_gögn == 54 || Word_gögn == 58) ? 4 : 0;
        }
        return lengd_VALUE > 0 && lengd_VALUE <= 끝 - 읽는자리 ? lengd_VALUE : 0;
    }
    static void athuga_endastaður_VALUE(int endastaður_VALUE, int fall_VALUE) {
        if (endastaður_VALUE < aðferð_Opna[fall_VALUE] || endastaður_VALUE >= aðferð_ljúka[fall_VALUE] || 경계[endastaður_VALUE] != fall_VALUE + 1) bilun_VALUE("invalid branch target");
    }
    static void 클래스읽기(int klasi_Skilgreining) {
        현재읽는종 = klasi_Skilgreining; 읽기위치 = klasi_Skilgreining * 16384; Stærð = 읽기위치 + klasi_Skilgreining_breyta_stærð[klasi_Skilgreining];
        if (heiltala() != 0xcafebabe) { bilun_VALUE("not a class file"); return; }
        int 부판 = 짧은수(), útgáfa_VALUE = 짧은수();
        if (útgáfa_VALUE < 45 || útgáfa_VALUE > 52 || 부판 != 0) { bilun_VALUE("supported class versions: 45..52, minor 0"); return; }
        int fasti_COUNT = 짧은수(), BASE_staða = klasi_Skilgreining * 512;
        if (fasti_COUNT < 1 || fasti_COUNT > 512) { bilun_VALUE("constant pool limit (511)"); return; }
        for (int færsla_COUNT = 1; færsla_COUNT < fasti_COUNT && !Villa; færsla_COUNT++) {
            int númer = BASE_staða + færsla_COUNT, 종류 = bæti_VALUE(); fasti_merki[númer] = 종류;
            if (종류 == 1) { fasti_SECOND_VALUE[númer] = 짧은수(); 상가[númer] = 읽기위치; 건너(fasti_SECOND_VALUE[númer]); }
            else if (종류 == 3) 상가[númer] = heiltala();
            else if (종류 == 7 || 종류 == 8) 상가[númer] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[númer] = 상번호(); fasti_SECOND_VALUE[númer] = 상번호(); }
            else bilun_VALUE("unsupported constant type");
        }
        int leyfi_VALUE = 짧은수();
        if ((leyfi_VALUE & (0x2000 | 0x4000)) != 0) bilun_VALUE("annotation/enum class unsupported");
        klasi_Skilgreining_heiti[klasi_Skilgreining] = klasi_heiti_SMS(상번호());
        klasi_Skilgreining_yfireining[klasi_Skilgreining] = klasi_heiti_SMS(상번호());
        int viðmót_COUNT = 짧은수(); if (viðmót_COUNT > 16) { bilun_VALUE("interface count limit"); return; }
        klasi_viðmót_COUNT[klasi_Skilgreining] = viðmót_COUNT;
        for (int Loop_INDEX = 0; Loop_INDEX < viðmót_COUNT; Loop_INDEX++) klasi_viðmót[klasi_Skilgreining * 16 + Loop_INDEX] = klasi_heiti_SMS(상번호());
        int reitur_COUNT = 짧은수();
        if (reitur_COUNT > 512 - rauf_COUNT) { bilun_VALUE("field count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < reitur_COUNT && !Villa; Loop_INDEX++) {
            int skrá_INDEX = rauf_COUNT++; rauf_eigandi[skrá_INDEX] = klasi_Skilgreining; rauf_Heimildir[skrá_INDEX] = 짧은수(); rauf_heiti[skrá_INDEX] = 상번호(); rauf_TYPE[skrá_INDEX] = 상번호();
            athuga_fasti(rauf_heiti[skrá_INDEX], 1); athuga_fasti(rauf_TYPE[skrá_INDEX], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[rauf_TYPE[skrá_INDEX]]; int tegund_CODE = 서술형(읽기위치 + fasti_SECOND_VALUE[rauf_TYPE[skrá_INDEX]], false); 읽기위치 = 보존값;
            if ((rauf_Heimildir[skrá_INDEX] & 8) == 0) rauf_staða[skrá_INDEX] = klasi_rauf_COUNT[klasi_Skilgreining]++;
            int eigind_gögn = 짧은수();
            for (int innri_samtenging_staða = 0; innri_samtenging_staða < eigind_gögn && !Villa; innri_samtenging_staða++) {
                int heiti_fasti = 상번호(), 유효길이 = heiltala();
                if (Word_SMS(heiti_fasti, "ConstantValue") && 유효길이 == 2) {
                    int gögn_VALUE = 상번호();
                    if (tegund_CODE == 1 && athuga_fasti(gögn_VALUE, 3)) rauf_gögn[skrá_INDEX] = 상가[gögn_VALUE];
                    else if (tegund_CODE == 2 && athuga_fasti(gögn_VALUE, 8)) rauf_gögn[skrá_INDEX] = fasti_SMS(상가[gögn_VALUE]);
                } else 건너(유효길이);
            }
        }
        int vara_COUNT = 짧은수();
        if (vara_COUNT > 512 - aðferð_COUNT) { bilun_VALUE("method count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < vara_COUNT && !Villa; Loop_INDEX++) {
            int númer = aðferð_COUNT++; aðferð_eigandi[númer] = klasi_Skilgreining;
            aðferð_aðgangur[númer] = 짧은수(); aðferð_heiti_SMS[númer] = 상번호(); aðferð_TYPE[númer] = 상번호();
            athuga_fasti(aðferð_heiti_SMS[númer], 1); 서술읽기(númer);
            if ((aðferð_aðgangur[númer] & 8) == 0) {
                if (aðferð_frumbreyta_COUNT[númer] == 16) { bilun_VALUE("too many instance method arguments"); return; }
                for (int Samanburður_staða = aðferð_frumbreyta_COUNT[númer]; Samanburður_staða > 0; Samanburður_staða--) aðferð_frumbreyta_TYPE[númer * 16 + Samanburður_staða] = aðferð_frumbreyta_TYPE[númer * 16 + Samanburður_staða - 1];
                aðferð_frumbreyta_TYPE[númer * 16] = 2; aðferð_frumbreyta_COUNT[númer]++;
            }
            if ((aðferð_aðgangur[númer] & 0x100) != 0) bilun_VALUE("user native method unsupported");
            if (Word_SMS(aðferð_heiti_SMS[númer], "<clinit>")) frumstilla_klasi_Skilgreining[klasi_Skilgreining] = númer + 1;
            for (int myndavél_að_framan_VALUE = 0; myndavél_að_framan_VALUE < númer; myndavél_að_framan_VALUE++) if (aðferð_eigandi[myndavél_að_framan_VALUE] == klasi_Skilgreining && samsvörun_Word(aðferð_heiti_SMS[myndavél_að_framan_VALUE], aðferð_heiti_SMS[númer]) && samsvörun_Word(aðferð_TYPE[myndavél_að_framan_VALUE], aðferð_TYPE[númer])) bilun_VALUE("duplicate method");
            int eigind_COUNT = 짧은수();
            for (int eigind_VALUE = 0; eigind_VALUE < eigind_COUNT && !Villa; eigind_VALUE++) {
                int Heiti = 상번호(), lengd_VALUE = heiltala(), Keyra_2 = 읽기위치;
                if (!miðlaskrá(Keyra_2, lengd_VALUE)) { bilun_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Heiti, "Code")) {
                    if (aðferð_Opna[númer] != 0) bilun_VALUE("duplicate Code attribute");
                    aðferð_bunki[númer] = 짧은수(); 함수지역[númer] = 짧은수(); int CODE_lengd = heiltala();
                    if (aðferð_bunki[númer] > 128 || 함수지역[númer] > 128 || 함수지역[númer] < aðferð_frumbreyta_COUNT[númer]
                        || CODE_lengd < 1 || CODE_lengd > 8192) bilun_VALUE("method memory limits exceeded");
                    aðferð_Opna[númer] = 읽기위치; 건너(CODE_lengd); aðferð_ljúka[númer] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { bilun_VALUE("exception table limit"); return; }
                    for (int innri_samtenging_staða = 0; innri_samtenging_staða < 잡는수; innri_samtenging_staða++) {
                        int villa_tilvísun = 잡기수++; 잡기함수[villa_tilvísun] = númer;
                        잡기시작[villa_tilvísun] = aðferð_Opna[númer] + 짧은수(); 잡기끝[villa_tilvísun] = aðferð_Opna[númer] + 짧은수();
                        잡기위치[villa_tilvísun] = aðferð_Opna[númer] + 짧은수(); int 부호값 = 상번호(); 잡기종[villa_tilvísun] = 부호값 == 0 ? 0 : klasi_heiti_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != Keyra_2 + lengd_VALUE) bilun_VALUE("Code attribute size mismatch");
                } else 건너(lengd_VALUE);
            }
            if ((aðferð_aðgangur[númer] & 0x400) != 0) continue;
            if (aðferð_Opna[númer] == 0) bilun_VALUE("missing Code attribute");
            int rauf_færsla = aðferð_Opna[númer];
            while (rauf_færsla < aðferð_ljúka[númer] && !Villa) {
                int lengd_VALUE = 길이읽기(rauf_færsla, aðferð_Opna[númer], aðferð_ljúka[númer]);
                if (lengd_VALUE == 0) { bilun_VALUE("unsupported or truncated bytecode"); break; }
                경계[rauf_færsla] = númer + 1; rauf_færsla += lengd_VALUE;
            }
            rauf_færsla = aðferð_Opna[númer];
            while (rauf_færsla < aðferð_ljúka[númer] && !Villa) {
                int VALUE = Skrá[rauf_færsla];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) athuga_endastaður_VALUE(rauf_færsla + (short)(Skrá[rauf_færsla + 1] << 8 | Skrá[rauf_færsla + 2]), númer);
                if (VALUE == 200) athuga_endastaður_VALUE(rauf_færsla + staða_heiltala(rauf_færsla + 1), númer);
                if (VALUE == 170 || VALUE == 171) {
                    int 읽는자리 = rauf_færsla + 1; while ((읽는자리 - aðferð_Opna[númer]) % 4 != 0) 읽는자리++;
                    athuga_endastaður_VALUE(rauf_færsla + staða_heiltala(읽는자리), númer);
                    int færsla_COUNT = VALUE == 170 ? staða_heiltala(읽는자리 + 8) - staða_heiltala(읽는자리 + 4) + 1 : staða_heiltala(읽는자리 + 4);
                    읽는자리 += VALUE == 170 ? 12 : 8;
                    for (int innri_samtenging_staða = 0; innri_samtenging_staða < færsla_COUNT; innri_samtenging_staða++) athuga_endastaður_VALUE(rauf_færsla + staða_heiltala(읽는자리 + innri_samtenging_staða * (VALUE == 170 ? 4 : 8) + (VALUE == 170 ? 0 : 4)), númer);
                }
                rauf_færsla += 길이읽기(rauf_færsla, aðferð_Opna[númer], aðferð_ljúka[númer]);
            }
            for (int innri_samtenging_staða = 0; innri_samtenging_staða < 잡기수; innri_samtenging_staða++) if (잡기함수[innri_samtenging_staða] == númer) {
                athuga_endastaður_VALUE(잡기시작[innri_samtenging_staða], númer); athuga_endastaður_VALUE(잡기위치[innri_samtenging_staða], númer);
                if (잡기끝[innri_samtenging_staða] != aðferð_ljúka[númer]) athuga_endastaður_VALUE(잡기끝[innri_samtenging_staða], númer);
                if (잡기시작[innri_samtenging_staða] >= 잡기끝[innri_samtenging_staða]) bilun_VALUE("invalid exception range");
            }
        }
        if (!Villa) 속성건너();
        if (읽기위치 != Stærð) bilun_VALUE("extra class file data");
    }
    static int úthluta_geymsla(int 종류, int lengd_VALUE) { return 새기억(종류, lengd_VALUE); }
    static boolean hlutur_VALUE(int tilvísun, int 종류) {
        if (!객체유효(tilvísun)) return false;
        if (힙[tilvísun] != 종류) { bilun_VALUE("object type mismatch"); return false; }
        return true;
    }
    static int fasti_SMS(int INDEX) {
        if (!athuga_fasti(INDEX, 1)) return 0;
        if (strengur_tilvísun[INDEX] != 0) return strengur_tilvísun[INDEX];
        int tilvísun = úthluta_geymsla(1, fasti_SECOND_VALUE[INDEX]); if (Villa) return 0;
        int 끝 = 상가[INDEX] + fasti_SECOND_VALUE[INDEX], númer = 상가[INDEX], lengd_VALUE = 0;
        while (númer < 끝 && !Villa) {
            int VALUE = Skrá[númer++];
            if (VALUE == 0) bilun_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && númer < 끝) {
                int Áfram_vara = Skrá[númer++];
                if ((Áfram_vara & 192) != 128) bilun_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | Áfram_vara & 63;
                if (VALUE != 0 && VALUE < 128) bilun_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && númer + 1 < 끝) {
                int 가 = Skrá[númer++], 나 = Skrá[númer++];
                if ((가 & 192) != 128 || (나 & 192) != 128) bilun_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (VALUE < 2048) bilun_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) bilun_VALUE("invalid modified UTF-8");
            힙[tilvísun + 2 + lengd_VALUE++] = VALUE;
        }
        힙[tilvísun + 1] = lengd_VALUE; strengur_tilvísun[INDEX] = tilvísun; return tilvísun;
    }
    static int hýsa_stafur(String VALUE) {
        int tilvísun = úthluta_geymsla(1, VALUE.length()); if (Villa) return 0;
        for (int númer = 0; númer < VALUE.length(); númer++) 힙[tilvísun + 2 + númer] = VALUE.charAt(númer);
        return tilvísun;
    }
    static void skrifa_SMS(int tilvísun) {
        if (tilvísun == 0) { notandi.Skrift("null"); return; }
        if (!hlutur_VALUE(tilvísun, 1)) return;
        for (int númer = 0; númer < 힙[tilvísun + 1]; númer++) notandi.skrifa_stafur_VALUE(힙[tilvísun + 2 + númer]);
    }
    static int tölustafur_stafur(int VALUE) {
        int tilvísun = úthluta_geymsla(1, 11); if (Villa) return 0;
        int lengd_VALUE = 0;
        if (VALUE < 0) 힙[tilvísun + 2 + lengd_VALUE++] = '-'; else VALUE = -VALUE;
        int staða_INDEX = 1000000000; boolean Keyra_2 = false;
        while (staða_INDEX != 0) {
            int númer = -(VALUE / staða_INDEX);
            if (númer != 0 || Keyra_2 || staða_INDEX == 1) { 힙[tilvísun + 2 + lengd_VALUE++] = '0' + númer; Keyra_2 = true; }
            VALUE %= staða_INDEX; staða_INDEX /= 10;
        }
        힙[tilvísun + 1] = lengd_VALUE; return tilvísun;
    }
    static int 정수해독(int tilvísun) {
        if (!hlutur_VALUE(tilvísun, 1)) return 0;
        int lengd_VALUE = 힙[tilvísun + 1], númer = 0, VALUE = 0; boolean 음수 = false;
        if (lengd_VALUE > 0 && (힙[tilvísun + 2] == '-' || 힙[tilvísun + 2] == '+')) { 음수 = 힙[tilvísun + 2] == '-'; númer++; }
        if (númer == lengd_VALUE) bilun_VALUE("NumberFormatException");
        for (; númer < lengd_VALUE && !Villa; númer++) {
            int tölustafur_VALUE = 힙[tilvísun + 2 + númer] - '0';
            if (tölustafur_VALUE < 0 || tölustafur_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && tölustafur_VALUE > (음수 ? 8 : 7)) bilun_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - tölustafur_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int TYPE_VALUE) {
        if (Villa) return;
        if (ramma_INDEX < 0 || ramma_bunki[ramma_INDEX] >= aðferð_bunki[ramma_aðferð[ramma_INDEX]]) { bilun_VALUE("operand stack overflow"); return; }
        int rauf_færsla = ramma_INDEX * 128 + ramma_bunki[ramma_INDEX]++; 스택값[rauf_færsla] = VALUE; 스택형[rauf_færsla] = TYPE_VALUE;
    }
    static int 빼기(int TYPE_VALUE) {
        if (Villa) return 0;
        if (ramma_INDEX < 0 || ramma_bunki[ramma_INDEX] < 1) { bilun_VALUE("operand stack underflow"); return 0; }
        int rauf_færsla = ramma_INDEX * 128 + --ramma_bunki[ramma_INDEX]; skila_TYPE = 스택형[rauf_færsla];
        if (TYPE_VALUE != 0 && skila_TYPE != TYPE_VALUE) bilun_VALUE("operand type mismatch");
        if (skila_TYPE == 2) verja_VALUE(스택값[rauf_færsla]);
        return 스택값[rauf_færsla];
    }
    static void 지역읽기(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[ramma_aðferð[ramma_INDEX]] || INDEX < 0 || staðbundið_TYPE[ramma_INDEX * 128 + INDEX] != TYPE_VALUE) { bilun_VALUE("invalid or uninitialized local"); return; }
        넣기(staðbundið_VALUE[ramma_INDEX * 128 + INDEX], TYPE_VALUE);
    }
    static void skrifa_staðbundið(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[ramma_aðferð[ramma_INDEX]] || INDEX < 0) { bilun_VALUE("local index out of range"); return; }
        int VALUE = 빼기(TYPE_VALUE); staðbundið_VALUE[ramma_INDEX * 128 + INDEX] = VALUE; staðbundið_TYPE[ramma_INDEX * 128 + INDEX] = TYPE_VALUE;
    }
    static int 명바() {
        int Staðsetning = ramma_staða[ramma_INDEX];
        if (Staðsetning < aðferð_Opna[ramma_aðferð[ramma_INDEX]] || Staðsetning >= aðferð_ljúka[ramma_aðferð[ramma_INDEX]]) { bilun_VALUE("instruction pointer out of range"); return 0; }
        ramma_staða[ramma_INDEX]++; return Skrá[Staðsetning];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void færa_VALUE(int Staðsetning) {
        int fall_VALUE = ramma_aðferð[ramma_INDEX];
        if (Staðsetning < aðferð_Opna[fall_VALUE] || Staðsetning >= aðferð_ljúka[fall_VALUE] || 경계[Staðsetning] != fall_VALUE + 1) bilun_VALUE("invalid branch target");
        else ramma_staða[ramma_INDEX] = Staðsetning;
    }
    static void 호출(int fall_VALUE) {
        if (ramma_INDEX % 32 == 31) { bilun_VALUE("call stack limit (32)"); return; }
        int Áfram_vara = ramma_INDEX + 1;
        for (int númer = 0; númer < 128; númer++) staðbundið_TYPE[Áfram_vara * 128 + númer] = 0;
        for (int númer = aðferð_frumbreyta_COUNT[fall_VALUE] - 1; númer >= 0; númer--) {
            staðbundið_VALUE[Áfram_vara * 128 + númer] = 빼기(aðferð_frumbreyta_TYPE[fall_VALUE * 16 + númer]); staðbundið_TYPE[Áfram_vara * 128 + númer] = aðferð_frumbreyta_TYPE[fall_VALUE * 16 + númer];
        }
        if (Villa) return;
        ramma_INDEX = Áfram_vara; frumstilla_ramma[ramma_INDEX] = 0; ramma_aðferð[ramma_INDEX] = fall_VALUE; ramma_staða[ramma_INDEX] = aðferð_Opna[fall_VALUE]; ramma_bunki[ramma_INDEX] = 0;
    }
    static void skila_mæld_stærð(int TYPE_VALUE) {
        if (TYPE_VALUE != aðferð_skila[ramma_aðferð[ramma_INDEX]]) { bilun_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        if (frumstilla_ramma[ramma_INDEX] != 0) klasi_Skilgreining_staða[frumstilla_ramma[ramma_INDEX] - 1] = 2;
        if (ramma_Loka[ramma_INDEX] != 0) { losa_Loka(ramma_Loka[ramma_INDEX]); ramma_Loka[ramma_INDEX] = 0; }
        ramma_INDEX--; if (ramma_INDEX >= 현재가닥 * 32 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
    }
    static int[] Stream_skrá_heiti = new int[64];
    static void skrá_Stream_CALL(int eigandi_VALUE, int Heiti, int snið_VALUE, int Skipun) {
        boolean úttak = Word_SMS(eigandi_VALUE, "java/io/FileOutputStream");
        int 종류 = úttak ? 6 : 5;
        if (Skipun == 183 && Word_SMS(Heiti, "<init>")) {
            boolean 이어 = false;
            if (úttak && Word_SMS(snið_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(snið_VALUE, "(Ljava/lang/String;)V")) { bilun_VALUE("unsupported file stream constructor"); return; }
            int skrá_færsla_heiti = 빼기(2), Stream_VALUE = 빼기(2);
            if (!hlutur_VALUE(skrá_færsla_heiti, 1) || !hlutur_VALUE(Stream_VALUE, 종류) || Villa) return;
            if (힙[Stream_VALUE + 3] != 0) { bilun_VALUE("file stream already initialized"); return; }
            int lengd_VALUE = 힙[skrá_færsla_heiti + 1];
            if (lengd_VALUE < 1 || lengd_VALUE > 63) { bilun_VALUE("invalid file name length"); return; }
            for (int rauf_færsla = 0; rauf_færsla < lengd_VALUE; rauf_færsla++) {
                int VALUE = 힙[skrá_færsla_heiti + 2 + rauf_færsla];
                if (VALUE < 1) { bilun_VALUE("invalid file stream path"); return; }
                Stream_skrá_heiti[rauf_færsla] = VALUE;
            }
            Stream_skrá_heiti[lengd_VALUE] = 0;
            int 서술자 = notandi.파일서술자열기(Stream_skrá_heiti, úttak ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { bilun_VALUE("FileNotFoundException: file open failed"); return; }
            힙[Stream_VALUE + 2] = 서술자; 힙[Stream_VALUE + 3] = 1;
            return;
        }
        if (Skipun != 182) { bilun_VALUE("invalid file stream invocation"); return; }
        if ((úttak && Word_SMS(Heiti, "write") || !úttak && Word_SMS(Heiti, "read"))
            && (Word_SMS(snið_VALUE, úttak ? "([B)V" : "([B)I") || Word_SMS(snið_VALUE, úttak ? "([BII)V" : "([BII)I"))) {
            boolean miðlaskrá_VALUE = Word_SMS(snið_VALUE, úttak ? "([BII)V" : "([BII)I");
            int færsla_COUNT = miðlaskrá_VALUE ? 빼기(1) : 0, 시작점 = miðlaskrá_VALUE ? 빼기(1) : 0, gögn_ARRAY = 빼기(2), hlutur_tilvísun = 빼기(2);
            if (!hlutur_VALUE(gögn_ARRAY, 20) || !hlutur_VALUE(hlutur_tilvísun, 종류)) return;
            if (!miðlaskrá_VALUE) færsla_COUNT = 힙[gögn_ARRAY + 1];
            if (시작점 < 0 || færsla_COUNT < 0 || 시작점 > 힙[gögn_ARRAY + 1] - færsla_COUNT) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[hlutur_tilvísun + 3] == 0 || 힙[hlutur_tilvísun + 2] < 0) { bilun_VALUE("IOException: stream closed"); return; }
            int lokið_COUNT = 0;
            while (lokið_COUNT < færsla_COUNT && !Villa) {
                int 반환값 = úttak ? notandi.파일한바이트쓰기(힙[hlutur_tilvísun + 2], 힙[gögn_ARRAY + 2 + 시작점 + lokið_COUNT]) : notandi.파일한바이트읽기(힙[hlutur_tilvísun + 2]);
                if (반환값 < 0) { bilun_VALUE(úttak ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!úttak && 반환값 == 256) break;
                if (!úttak) 힙[gögn_ARRAY + 2 + 시작점 + lokið_COUNT] = (byte)반환값;
                lokið_COUNT++;
            }
            if (!úttak) 넣기(færsla_COUNT != 0 && lokið_COUNT == 0 ? -1 : lokið_COUNT, 1);
            return;
        }
        if (úttak && Word_SMS(Heiti, "flush") && Word_SMS(snið_VALUE, "()V")) { int hlutur_tilvísun = 빼기(2); if (hlutur_VALUE(hlutur_tilvísun, 종류) && 힙[hlutur_tilvísun + 2] < 0) bilun_VALUE("IOException: stream closed"); return; }
        int Aðgerð = -1, VALUE = 0;
        if (Word_SMS(Heiti, "close") && Word_SMS(snið_VALUE, "()V")) Aðgerð = 0;
        if (!úttak && Word_SMS(Heiti, "read") && Word_SMS(snið_VALUE, "()I")) Aðgerð = 1;
        if (úttak && Word_SMS(Heiti, "write") && Word_SMS(snið_VALUE, "(I)V")) { Aðgerð = 2; VALUE = 빼기(1); }
        if (Aðgerð < 0) { bilun_VALUE("unsupported file stream method"); return; }
        int Stream_VALUE = 빼기(2);
        if (!hlutur_VALUE(Stream_VALUE, 종류) || Villa) return;
        if (힙[Stream_VALUE + 3] == 0) { bilun_VALUE("uninitialized file stream"); return; }
        int 서술자 = 힙[Stream_VALUE + 2];
        if (Aðgerð == 0) {
            if (서술자 >= 0 && notandi.파일서술자닫기(서술자) < 0) bilun_VALUE("IOException: close failed");
            힙[Stream_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { bilun_VALUE("IOException: stream closed"); return; }
        if (Aðgerð == 1) {
            int NIÐURSTAÐA = notandi.파일한바이트읽기(서술자);
            if (NIÐURSTAÐA < -1) bilun_VALUE("IOException: read failed"); else 넣기(NIÐURSTAÐA == 256 ? -1 : NIÐURSTAÐA, 1);
        } else if (notandi.파일한바이트쓰기(서술자, VALUE) != 1) bilun_VALUE("IOException: write failed");
    }
    static void CALL_aðferð(int INDEX, int Skipun) {
        if (INDEX <= 0 || INDEX >= fasti_merki.length || (fasti_merki[INDEX] != 10 && fasti_merki[INDEX] != 11)) { bilun_VALUE("invalid method reference"); return; }
        int eigandi_VALUE = klasi_heiti_SMS(상가[INDEX]), Heiti = tilvísun_heiti(fasti_SECOND_VALUE[INDEX]), snið_VALUE = tilvísun_TYPE(fasti_SECOND_VALUE[INDEX]);
        if (Villa) return;
        if (기본호출(eigandi_VALUE, Heiti, snið_VALUE, Skipun)) return;
        if (Word_SMS(eigandi_VALUE, "java/io/FileInputStream") || Word_SMS(eigandi_VALUE, "java/io/FileOutputStream")) {
            skrá_Stream_CALL(eigandi_VALUE, Heiti, snið_VALUE, Skipun); return;
        }
        if (Skipun == 184 && Word_SMS(eigandi_VALUE, "java/lang/Integer") && Word_SMS(Heiti, "parseInt") && Word_SMS(snið_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Skipun == 182 && Word_SMS(eigandi_VALUE, "java/io/PrintStream") && (Word_SMS(Heiti, "println") || Word_SMS(Heiti, "print"))) {
            int TYPE_VALUE = 0, VALUE = 0;
            if (Word_SMS(snið_VALUE, "(I)V")) { TYPE_VALUE = 1; VALUE = 빼기(1); }
            else if (Word_SMS(snið_VALUE, "(Z)V")) { TYPE_VALUE = 2; VALUE = 빼기(1); }
            else if (Word_SMS(snið_VALUE, "(C)V")) { TYPE_VALUE = 3; VALUE = 빼기(1); }
            else if (Word_SMS(snið_VALUE, "(Ljava/lang/String;)V")) { TYPE_VALUE = 4; VALUE = 빼기(2); }
            else if (!Word_SMS(snið_VALUE, "()V") || !Word_SMS(Heiti, "println")) bilun_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) bilun_VALUE("invalid PrintStream receiver");
            if (Villa) return;
            if (TYPE_VALUE == 1) 자바도구.skrifa_númer(VALUE);
            if (TYPE_VALUE == 2) notandi.Skrift(VALUE == 0 ? "false" : "true");
            if (TYPE_VALUE == 3) notandi.skrifa_stafur_VALUE(VALUE & 65535);
            if (TYPE_VALUE == 4) skrifa_SMS(VALUE);
            if (Word_SMS(Heiti, "println")) notandi.skrifa_stafur_VALUE(10);
            return;
        }
        if (Skipun == 182 && Word_SMS(eigandi_VALUE, "java/lang/String")) {
            if (Word_SMS(Heiti, "length") && Word_SMS(snið_VALUE, "()I")) {
                int tilvísun = 빼기(2); if (hlutur_VALUE(tilvísun, 1)) 넣기(힙[tilvísun + 1], 1); return;
            }
            if (Word_SMS(Heiti, "charAt") && Word_SMS(snið_VALUE, "(I)C")) {
                int hnéletur_VALUE = 빼기(1), tilvísun = 빼기(2);
                if (hlutur_VALUE(tilvísun, 1)) {
                    if (hnéletur_VALUE < 0 || hnéletur_VALUE >= 힙[tilvísun + 1]) bilun_VALUE("StringIndexOutOfBoundsException"); else 넣기(힙[tilvísun + 2 + hnéletur_VALUE], 1);
                }
                return;
            }
        }
        if (Word_SMS(eigandi_VALUE, "java/lang/StringBuilder")) {
            if (Skipun == 183 && Word_SMS(Heiti, "<init>") && Word_SMS(snið_VALUE, "()V")) { hlutur_VALUE(빼기(2), 4); return; }
            if (Skipun == 182 && Word_SMS(Heiti, "toString") && Word_SMS(snið_VALUE, "()Ljava/lang/String;")) {
                int tilvísun = 빼기(2); if (hlutur_VALUE(tilvísun, 4)) 넣기(힙[tilvísun + 2] == 0 ? hýsa_stafur("") : 힙[tilvísun + 2], 2); return;
            }
            if (Skipun == 182 && Word_SMS(Heiti, "append")) {
                int Texti = 0;
                if (Word_SMS(snið_VALUE, "(I)Ljava/lang/StringBuilder;")) Texti = tölustafur_stafur(빼기(1));
                else if (Word_SMS(snið_VALUE, "(Z)Ljava/lang/StringBuilder;")) Texti = hýsa_stafur(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(snið_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); Texti = úthluta_geymsla(1, 1); if (!Villa) 힙[Texti + 2] = VALUE & 65535;
                }
                else if (Word_SMS(snið_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Texti = 빼기(2); if (Texti == 0) Texti = hýsa_stafur("null"); }
                else { bilun_VALUE("unsupported StringBuilder append"); return; }
                int tilvísun = 빼기(2); if (!hlutur_VALUE(tilvísun, 4) || !hlutur_VALUE(Texti, 1)) return;
                int myndavél_að_framan_VALUE = 힙[tilvísun + 2], myndavél_að_framan_VALUE_lengd = myndavél_að_framan_VALUE == 0 ? 0 : 힙[myndavél_að_framan_VALUE + 1], TIL_BAKA_VALUE_lengd = 힙[Texti + 1];
                int 새글 = úthluta_geymsla(1, myndavél_að_framan_VALUE_lengd + TIL_BAKA_VALUE_lengd); if (Villa) return;
                for (int númer = 0; númer < myndavél_að_framan_VALUE_lengd; númer++) 힙[새글 + 2 + númer] = 힙[myndavél_að_framan_VALUE + 2 + númer];
                for (int númer = 0; númer < TIL_BAKA_VALUE_lengd; númer++) 힙[새글 + 2 + myndavél_að_framan_VALUE_lengd + númer] = 힙[Texti + 2 + númer];
                힙[tilvísun + 2] = 새글; 넣기(tilvísun, 2); return;
            }
        }
        int klasi_Skilgreining = FIND_klasi_Skilgreining(eigandi_VALUE); if (klasi_Skilgreining < 0 || Villa) return;
        int skrá_INDEX = FIND_aðferð(klasi_Skilgreining, Heiti, snið_VALUE);
        if (skrá_INDEX < 0) {
            for (int stafkóði = klasi_Skilgreining, færsla_COUNT = 0; stafkóði >= 0 && færsla_COUNT < 16; færsla_COUNT++, stafkóði = yfireining_klasi(stafkóði))
                if (Word_SMS(klasi_Skilgreining_yfireining[stafkóði], "java/lang/Thread")) { 가닥호출(Heiti, snið_VALUE, Skipun); return; }
            bilun_VALUE("NoSuchMethodError"); return;
        }
        if (((aðferð_aðgangur[skrá_INDEX] & 8) != 0) != (Skipun == 184)) { bilun_VALUE("method static/instance mismatch"); return; }
        if (Skipun == 184) { if (!frumstilla(aðferð_eigandi[skrá_INDEX], ramma_skipun[ramma_INDEX])) return; }
        else {
            int 읽는자리 = ramma_bunki[ramma_INDEX] - aðferð_frumbreyta_COUNT[skrá_INDEX];
            if (읽는자리 < 0 || 스택형[ramma_INDEX * 128 + 읽는자리] != 2) { bilun_VALUE("invalid method receiver"); return; }
            int hlutur_tilvísun = 스택값[ramma_INDEX * 128 + 읽는자리];
            if (!객체유효(hlutur_tilvísun)) return;
            if (힙[hlutur_tilvísun] < 32 || !종포함(힙[hlutur_tilvísun] - 32, eigandi_VALUE)) { bilun_VALUE("method receiver type mismatch"); return; }
            if (Skipun != 183) skrá_INDEX = FIND_aðferð(힙[hlutur_tilvísun] - 32, Heiti, snið_VALUE);
        }
        if (skrá_INDEX < 0 || (aðferð_aðgangur[skrá_INDEX] & 0x400) != 0) { bilun_VALUE("AbstractMethodError"); return; }
        int Loka_tilvísun = 0;
        if ((aðferð_aðgangur[skrá_INDEX] & 32) != 0) {
            if (Skipun == 184) { int stafkóði = aðferð_eigandi[skrá_INDEX]; if (klasi_Loka[stafkóði] == 0) klasi_Loka[stafkóði] = úthluta_geymsla(8, 0); Loka_tilvísun = klasi_Loka[stafkóði]; }
            else Loka_tilvísun = 스택값[ramma_INDEX * 128 + ramma_bunki[ramma_INDEX] - aðferð_frumbreyta_COUNT[skrá_INDEX]];
            if (!잠금얻기(Loka_tilvísun)) { if (!Villa) ramma_staða[ramma_INDEX] = ramma_skipun[ramma_INDEX]; return; }
        }
        호출(skrá_INDEX); if (!Villa) ramma_Loka[ramma_INDEX] = Loka_tilvísun;
    }
    static boolean 배열저장가능(int ARRAY_tilvísun, int gögn_VALUE) {
        if (gögn_VALUE == 0 || ARRAY_eining[ARRAY_tilvísun] == 0) return true;
        boolean 성공여부 = ARRAY_eining[ARRAY_tilvísun] == -1 ? (gögn_VALUE > 0 && gögn_VALUE < 힙끝 && 힙[gögn_VALUE] == 1) : samsvörun_hlutur(gögn_VALUE, ARRAY_eining[ARRAY_tilvísun]);
        if (!성공여부 && !Villa) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int ARRAY_rauf(int tilvísun, int hnéletur_VALUE, int TYPE_VALUE) {
        if (!hlutur_VALUE(tilvísun, TYPE_VALUE)) return 0;
        if (hnéletur_VALUE < 0 || hnéletur_VALUE >= 힙[tilvísun + 1]) { bilun_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return tilvísun + 2 + hnéletur_VALUE;
    }
    static void keyra_skipun() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (Villa) { if (던진객체 != 0) hald_undantekning(); if (Villa || ramma_INDEX < 현재가닥 * 32) break; }
            if (ramma_INDEX < 현재가닥 * 32 || 바꿈요청 || --조각 == 0) { if (!SWITCH_þráður()) break; 조각 = 100; }
            if (ramma_INDEX == 0 && klasi_Skilgreining_staða[færsla_klasi_Skilgreining] != 2 && !frumstilla(færsla_klasi_Skilgreining, ramma_staða[ramma_INDEX])) continue;
            if (ramma_INDEX == 현재가닥 * 32 && 현재가닥 != 0 && (aðferð_aðgangur[ramma_aðferð[ramma_INDEX]] & 32) != 0 && ramma_Loka[ramma_INDEX] == 0) {
                int hlutur_tilvísun = þráður_markmið[현재가닥]; if (!잠금얻기(hlutur_tilvísun)) { if (Villa) break; continue; } ramma_Loka[ramma_INDEX] = hlutur_tilvísun;
            }
            잠시수 = 0;
            if (--남음 == 0) { bilun_VALUE("instruction limit (500000)"); break; }
            int Keyra_2 = ramma_staða[ramma_INDEX]; ramma_skipun[ramma_INDEX] = Keyra_2; int VALUE = 명바();
            if (Villa) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int númer = aðferð_eigandi[ramma_aðferð[ramma_INDEX]] * 512 + (VALUE == 18 ? 명바() : 명짧());
                if (númer <= 0 || númer >= fasti_merki.length) bilun_VALUE("invalid ldc constant");
                else if (fasti_merki[númer] == 3) 넣기(상가[númer], 1);
                else if (fasti_merki[númer] == 8) 넣기(fasti_SMS(상가[númer]), 2);
                else bilun_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { skrifa_staðbundið(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { skrifa_staðbundið(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { skrifa_staðbundið(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE >= 50 && VALUE <= 53) {
                int færsla_staða = 빼기(1), hlutur_tilvísun = 빼기(2), tegund_CODE = VALUE == 46 ? 2 : VALUE == 50 ? 3 : VALUE == 51 ? 20 : VALUE == 52 ? 22 : 23;
                if (VALUE == 51 && hlutur_tilvísun > 0 && hlutur_tilvísun < 힙끝 && 힙[hlutur_tilvísun] == 21) tegund_CODE = 21;
                int 읽는자리 = ARRAY_rauf(hlutur_tilvísun, færsla_staða, tegund_CODE); if (!Villa) 넣기(힙[읽는자리], VALUE == 50 ? 2 : 1); continue;
            }
            if (VALUE == 79 || VALUE >= 83 && VALUE <= 86) {
                int færsla_tilvísun = 빼기(VALUE == 83 ? 2 : 1), færsla_staða = 빼기(1), hlutur_tilvísun = 빼기(2), tegund_CODE = VALUE == 79 ? 2 : VALUE == 83 ? 3 : VALUE == 84 ? 20 : VALUE == 85 ? 22 : 23;
                if (VALUE == 84 && hlutur_tilvísun > 0 && hlutur_tilvísun < 힙끝 && 힙[hlutur_tilvísun] == 21) tegund_CODE = 21;
                int 읽는자리 = ARRAY_rauf(hlutur_tilvísun, færsla_staða, tegund_CODE);
                if (!Villa && tegund_CODE == 3 && !배열저장가능(hlutur_tilvísun, færsla_tilvísun)) continue;
                if (!Villa) 힙[읽는자리] = tegund_CODE == 20 ? (byte)færsla_tilvísun : tegund_CODE == 21 ? færsla_tilvísun & 1 : tegund_CODE == 22 ? (char)færsla_tilvísun : tegund_CODE == 23 ? (short)færsla_tilvísun : færsla_tilvísun;
                continue;
            }
            if (VALUE >= 87 && VALUE <= 95) { bunki_skipun(VALUE); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), NIÐURSTAÐA = 0;
                if ((VALUE == 108 || VALUE == 112) && 나 == 0) { bilun_VALUE("ArithmeticException: / by zero"); continue; }
                if (VALUE == 96) NIÐURSTAÐA = 가 + 나;
                if (VALUE == 100) NIÐURSTAÐA = 가 - 나;
                if (VALUE == 104) NIÐURSTAÐA = 가 * 나;
                if (VALUE == 108) NIÐURSTAÐA = 가 / 나;
                if (VALUE == 112) NIÐURSTAÐA = 가 % 나;
                if (VALUE == 120) NIÐURSTAÐA = 가 << 나;
                if (VALUE == 122) NIÐURSTAÐA = 가 >> 나;
                if (VALUE == 124) NIÐURSTAÐA = 가 >>> 나;
                if (VALUE == 126) NIÐURSTAÐA = 가 & 나;
                if (VALUE == 128) NIÐURSTAÐA = 가 | 나;
                if (VALUE == 130) NIÐURSTAÐA = 가 ^ 나;
                넣기(NIÐURSTAÐA, 1); continue;
            }
            if (VALUE == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALUE == 132) {
                int staðbundið_umfang = 명바(), 증분 = (byte)명바(); 지역읽기(staðbundið_umfang, 1); 넣기(빼기(1) + 증분, 1); skrifa_staðbundið(staðbundið_umfang, 1); continue;
            }
            if (VALUE >= 145 && VALUE <= 147) {
                int númer = 빼기(1); 넣기(VALUE == 145 ? (byte)númer : VALUE == 146 ? (char)númer : (short)númer, 1); continue;
            }
            if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                int endastaður_VALUE = Keyra_2 + (short)명짧(); boolean 갈까 = VALUE == 167;
                if (VALUE >= 153 && VALUE <= 158) {
                    int númer = 빼기(1); 갈까 = VALUE == 153 ? númer == 0 : VALUE == 154 ? númer != 0 : VALUE == 155 ? númer < 0 : VALUE == 156 ? númer >= 0 : VALUE == 157 ? númer > 0 : númer <= 0;
                } else if (VALUE >= 159 && VALUE <= 166) {
                    int 나 = 빼기(VALUE >= 165 ? 2 : 1), 가 = 빼기(VALUE >= 165 ? 2 : 1);
                    갈까 = VALUE == 159 || VALUE == 165 ? 가 == 나 : VALUE == 160 || VALUE == 166 ? 가 != 나 : VALUE == 161 ? 가 < 나 : VALUE == 162 ? 가 >= 나 : VALUE == 163 ? 가 > 나 : 가 <= 나;
                } else if (VALUE == 198 || VALUE == 199) { int númer = 빼기(2); 갈까 = VALUE == 198 ? númer == 0 : númer != 0; }
                if (갈까) færa_VALUE(endastaður_VALUE); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { skila_mæld_stærð(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE >= 178 && VALUE <= 181) { 필드호출(명상수(), VALUE, Keyra_2); continue; }
            if (VALUE >= 182 && VALUE <= 185) {
                int 부호값 = 명상수();
                if (VALUE == 185) { int samtala_COUNT = 명바(); if (samtala_COUNT == 0 || 명바() != 0) { bilun_VALUE("invalid invokeinterface operands"); continue; } }
                CALL_aðferð(부호값, VALUE); continue;
            }
            if (VALUE == 187) { 새객체(klasi_heiti_SMS(명상수()), Keyra_2); continue; }
            if (VALUE == 188 || VALUE == 189) {
                int tegund_CODE = 3, þáttur = 0;
                if (VALUE == 188) { int 임시값 = 명바(); tegund_CODE = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else þáttur = klasi_heiti_SMS(명상수());
                if (tegund_CODE == 0) { bilun_VALUE("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), hlutur_tilvísun = úthluta_geymsla(tegund_CODE, 유효길이); if (!Villa) ARRAY_eining[hlutur_tilvísun] = þáttur; 넣기(hlutur_tilvísun, 2); continue;
            }
            if (VALUE == 190) {
                int hlutur_tilvísun = 빼기(2);
                if (객체유효(hlutur_tilvísun)) { int Samanburður_staða = 힙[hlutur_tilvísun]; if (Samanburður_staða != 2 && Samanburður_staða != 3 && (Samanburður_staða < 20 || Samanburður_staða > 23)) bilun_VALUE("not an array"); else 넣기(힙[hlutur_tilvísun + 1], 1); }
                continue;
            }
            if (VALUE == 191) {
                int hlutur_tilvísun = 빼기(2); if (객체유효(hlutur_tilvísun)) { if (힙[hlutur_tilvísun] != 9) bilun_VALUE("athrow requires supported Throwable"); else { 던진객체 = hlutur_tilvísun; Villa = true; } }
                continue;
            }
            if (VALUE == 192 || VALUE == 193) {
                int heiti_fasti = klasi_heiti_SMS(명상수()), hlutur_tilvísun = 빼기(2); boolean MATCH = samsvörun_hlutur(hlutur_tilvísun, heiti_fasti);
                if (VALUE == 193) 넣기(hlutur_tilvísun != 0 && MATCH ? 1 : 0, 1);
                else { if (!MATCH && !Villa) bilun_VALUE("ClassCastException"); 넣기(hlutur_tilvísun, 2); }
                continue;
            }
            if (VALUE == 170 || VALUE == 171) {
                int 읽는자리 = Keyra_2 + 1, skrá_INDEX = ramma_aðferð[ramma_INDEX], Lykill_tilvísun = 빼기(1);
                while ((읽는자리 - aðferð_Opna[skrá_INDEX]) % 4 != 0) 읽는자리++;
                int markmið_slóð = staða_heiltala(읽는자리);
                if (VALUE == 170) { int 낮은값 = staða_heiltala(읽는자리 + 4), 높은값 = staða_heiltala(읽는자리 + 8); if (Lykill_tilvísun >= 낮은값 && Lykill_tilvísun <= 높은값) markmið_slóð = staða_heiltala(읽는자리 + 12 + (Lykill_tilvísun - 낮은값) * 4); }
                else { int samtala_COUNT = staða_heiltala(읽는자리 + 4); for (int Loop_INDEX = 0; Loop_INDEX < samtala_COUNT; Loop_INDEX++) if (staða_heiltala(읽는자리 + 8 + Loop_INDEX * 8) == Lykill_tilvísun) markmið_slóð = staða_heiltala(읽는자리 + 12 + Loop_INDEX * 8); }
                færa_VALUE(Keyra_2 + markmið_slóð); continue;
            }
            if (VALUE == 200) { færa_VALUE(Keyra_2 + staða_heiltala(Keyra_2 + 1)); continue; }
            if (VALUE == 194 || VALUE == 195) {
                int hlutur_tilvísun = 빼기(2);
                if (VALUE == 195) losa_Loka(hlutur_tilvísun);
                else if (!잠금얻기(hlutur_tilvísun) && !Villa) { 넣기(hlutur_tilvísun, 2); ramma_staða[ramma_INDEX] = Keyra_2; }
                continue;
            }
            if (VALUE == 196) {
                int skipun_CODE = 명바(), færsla_staða = 명짧();
                if (skipun_CODE == 21 || skipun_CODE == 25) 지역읽기(færsla_staða, skipun_CODE == 21 ? 1 : 2);
                else if (skipun_CODE == 54 || skipun_CODE == 58) skrifa_staðbundið(færsla_staða, skipun_CODE == 54 ? 1 : 2);
                else if (skipun_CODE == 132) { int DELTA_VALUE = (short)명짧(); 지역읽기(færsla_staða, 1); 넣기(빼기(1) + DELTA_VALUE, 1); skrifa_staðbundið(færsla_staða, 1); }
                else bilun_VALUE("unsupported wide opcode");
                continue;
            }
            bilun_VALUE("unsupported bytecode");
        }
    }
    static int FIND_klasi_Skilgreining(int Heiti) {
        for (int Loop_INDEX = 0; Loop_INDEX < klasi_Skilgreining_COUNT; Loop_INDEX++) if (klasi_Skilgreining_heiti[Loop_INDEX] != 0 && samsvörun_Word(klasi_Skilgreining_heiti[Loop_INDEX], Heiti)) return Loop_INDEX;
        return álag_klasi_Skilgreining(fasti_SMS(Heiti));
    }
    static int álag_klasi_Skilgreining(int heiti_strengur) {
        if (!hlutur_VALUE(heiti_strengur, 1)) return -1;
        int lengd_VALUE = 힙[heiti_strengur + 1];
        if (lengd_VALUE < 1 || lengd_VALUE > 505 || klasi_Skilgreining_COUNT == 16) { bilun_VALUE("class name/count limit"); return -1; }
        for (int Loop_INDEX = 0; Loop_INDEX < lengd_VALUE; Loop_INDEX++) { int stafkóði = 힙[heiti_strengur + 2 + Loop_INDEX]; skrá_heiti_SMS[Loop_INDEX] = stafkóði == '/' ? '.' : stafkóði; }
        skrá_heiti_SMS[lengd_VALUE] = '.'; skrá_heiti_SMS[lengd_VALUE + 1] = 'c'; skrá_heiti_SMS[lengd_VALUE + 2] = 'l'; skrá_heiti_SMS[lengd_VALUE + 3] = 'a'; skrá_heiti_SMS[lengd_VALUE + 4] = 's'; skrá_heiti_SMS[lengd_VALUE + 5] = 's'; skrá_heiti_SMS[lengd_VALUE + 6] = 0;
        int Stærð = notandi.파일읽기(skrá_heiti_SMS, 임시파일);
        if (Stærð < 0) { bilun_VALUE("ClassNotFoundException"); return -1; }
        int klasi_Skilgreining = klasi_Skilgreining_COUNT++; klasi_Skilgreining_breyta_stærð[klasi_Skilgreining] = Stærð;
        for (int Loop_INDEX = 0; Loop_INDEX < Stærð; Loop_INDEX++) Skrá[klasi_Skilgreining * 16384 + Loop_INDEX] = 임시파일[Loop_INDEX];
        클래스읽기(klasi_Skilgreining); if (Villa) return -1;
        int raun_gögn = fasti_SMS(klasi_Skilgreining_heiti[klasi_Skilgreining]);
        if (!글같음(raun_gögn, heiti_strengur, true)) { bilun_VALUE("class name does not match file"); return -1; }
        int yfireining_VALUE = klasi_Skilgreining_yfireining[klasi_Skilgreining];
        if (yfireining_VALUE != 0 && !Word_SMS(yfireining_VALUE, "java/lang/Object") && !Word_SMS(yfireining_VALUE, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = FIND_klasi_Skilgreining(yfireining_VALUE);
            if (Villa || 위 < 0) return -1;
            int 읽는자리 = 위, stig_COUNT = 0;
            while (읽는자리 >= 0 && stig_COUNT++ < 16) {
                if (읽는자리 == klasi_Skilgreining) { bilun_VALUE("cyclic inheritance"); return -1; }
                읽는자리 = yfireining_klasi(읽는자리);
            }
            int 시작변위 = klasi_rauf_COUNT[위];
            for (int skrá_INDEX = 0; skrá_INDEX < rauf_COUNT; skrá_INDEX++) if (rauf_eigandi[skrá_INDEX] == klasi_Skilgreining && (rauf_Heimildir[skrá_INDEX] & 8) == 0) rauf_staða[skrá_INDEX] += 시작변위;
            klasi_rauf_COUNT[klasi_Skilgreining] += 시작변위;
        }
        return klasi_Skilgreining;
    }
    static int yfireining_klasi(int klasi_Skilgreining) {
        int Heiti = klasi_Skilgreining_yfireining[klasi_Skilgreining];
        for (int Loop_INDEX = 0; Loop_INDEX < klasi_Skilgreining_COUNT; Loop_INDEX++) if (Heiti != 0 && klasi_Skilgreining_heiti[Loop_INDEX] != 0 && samsvörun_Word(klasi_Skilgreining_heiti[Loop_INDEX], Heiti)) return Loop_INDEX;
        return -1;
    }
    static int FIND_aðferð(int klasi_Skilgreining, int Heiti, int snið_VALUE) {
        for (int 깊이 = 0; klasi_Skilgreining >= 0 && 깊이 < 16; 깊이++, klasi_Skilgreining = yfireining_klasi(klasi_Skilgreining)) {
            for (int Loop_INDEX = 0; Loop_INDEX < aðferð_COUNT; Loop_INDEX++) if (aðferð_eigandi[Loop_INDEX] == klasi_Skilgreining && samsvörun_Word(aðferð_heiti_SMS[Loop_INDEX], Heiti) && samsvörun_Word(aðferð_TYPE[Loop_INDEX], snið_VALUE)) return Loop_INDEX;
        }
        return -1;
    }
    static int heiti_aðferð(int klasi_Skilgreining, String Heiti, String snið_VALUE) {
        for (int 깊이 = 0; klasi_Skilgreining >= 0 && 깊이 < 16; 깊이++, klasi_Skilgreining = yfireining_klasi(klasi_Skilgreining))
            for (int Loop_INDEX = 0; Loop_INDEX < aðferð_COUNT; Loop_INDEX++) if (aðferð_eigandi[Loop_INDEX] == klasi_Skilgreining && Word_SMS(aðferð_heiti_SMS[Loop_INDEX], Heiti) && Word_SMS(aðferð_TYPE[Loop_INDEX], snið_VALUE)) return Loop_INDEX;
        return -1;
    }
    static int 형종류(int Heiti) { return Skrá[상가[Heiti]] == 'L' || Skrá[상가[Heiti]] == '[' ? 2 : 1; }
    static boolean frumstilla(int klasi_Skilgreining, int skipun_Opna) {
        if (klasi_Skilgreining < 0 || Villa) return false;
        if (klasi_Skilgreining_staða[klasi_Skilgreining] == 3) { bilun_VALUE("NoClassDefFoundError: initialization failed"); return false; }
        if (klasi_Skilgreining_staða[klasi_Skilgreining] == 1 && klasi_þráður[klasi_Skilgreining] != 현재가닥) { ramma_staða[ramma_INDEX] = skipun_Opna; 바꿈요청 = true; return false; }
        if (klasi_Skilgreining_staða[klasi_Skilgreining] != 0) return true;
        int 위 = yfireining_klasi(klasi_Skilgreining);
        if (위 >= 0 && !frumstilla(위, skipun_Opna)) return false;
        klasi_Skilgreining_staða[klasi_Skilgreining] = 1; klasi_þráður[klasi_Skilgreining] = 현재가닥;
        if (frumstilla_klasi_Skilgreining[klasi_Skilgreining] != 0) {
            ramma_staða[ramma_INDEX] = skipun_Opna;
            호출(frumstilla_klasi_Skilgreining[klasi_Skilgreining] - 1); if (!Villa) frumstilla_ramma[ramma_INDEX] = klasi_Skilgreining + 1;
            return false;
        }
        klasi_Skilgreining_staða[klasi_Skilgreining] = 2; return true;
    }
    static void 필드호출(int INDEX, int Skipun, int Keyra_2) {
        if (!athuga_fasti(INDEX, 9)) return;
        int eigandi_VALUE = klasi_heiti_SMS(상가[INDEX]), Heiti = tilvísun_heiti(fasti_SECOND_VALUE[INDEX]), snið_VALUE = tilvísun_TYPE(fasti_SECOND_VALUE[INDEX]);
        if (Word_SMS(eigandi_VALUE, "java/lang/System") && (Word_SMS(Heiti, "out") || Word_SMS(Heiti, "err")) && Word_SMS(snið_VALUE, "Ljava/io/PrintStream;") && Skipun == 178) { 넣기(-1, 2); return; }
        int klasi_Skilgreining = FIND_klasi_Skilgreining(eigandi_VALUE); if (klasi_Skilgreining < 0 || Villa) return;
        int 찾음 = -1;
        for (int 읽는자리 = klasi_Skilgreining, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = yfireining_klasi(읽는자리))
            for (int skrá_INDEX = 0; skrá_INDEX < rauf_COUNT; skrá_INDEX++) if (rauf_eigandi[skrá_INDEX] == 읽는자리 && samsvörun_Word(rauf_heiti[skrá_INDEX], Heiti) && samsvörun_Word(rauf_TYPE[skrá_INDEX], snið_VALUE)) 찾음 = skrá_INDEX;
        if (찾음 < 0) { bilun_VALUE("NoSuchFieldError"); return; }
        boolean fast_VALUE = Skipun == 178 || Skipun == 179;
        if (fast_VALUE != ((rauf_Heimildir[찾음] & 8) != 0)) { bilun_VALUE("field static/instance mismatch"); return; }
        if (fast_VALUE && !frumstilla(rauf_eigandi[찾음], Keyra_2)) return;
        int TYPE_VALUE = 형종류(snið_VALUE), VALUE = 0;
        if (Skipun == 179 || Skipun == 181) VALUE = 빼기(TYPE_VALUE);
        if (fast_VALUE) { if (Skipun == 178) 넣기(rauf_gögn[찾음], TYPE_VALUE); else if (!Villa) rauf_gögn[찾음] = VALUE; return; }
        int hlutur_tilvísun = 빼기(2);
        if (!객체유효(hlutur_tilvísun)) return;
        if (힙[hlutur_tilvísun] < 32 || !종포함(힙[hlutur_tilvísun] - 32, eigandi_VALUE)) { bilun_VALUE("field receiver type mismatch"); return; }
        int 보관칸 = hlutur_tilvísun + 2 + rauf_staða[찾음];
        if (Skipun == 180) 넣기(힙[보관칸], TYPE_VALUE);
        else if (!Villa) { 힙[보관칸] = VALUE; 힙참조[보관칸] = TYPE_VALUE == 2 ? 1 : 0; }
    }
    static boolean 종포함(int klasi_Skilgreining, int Heiti) {
        for (int 중첩깊이 = 0; klasi_Skilgreining >= 0 && 중첩깊이 < 16; 중첩깊이++, klasi_Skilgreining = yfireining_klasi(klasi_Skilgreining)) {
            if (samsvörun_Word(klasi_Skilgreining_heiti[klasi_Skilgreining], Heiti) || (klasi_Skilgreining_yfireining[klasi_Skilgreining] != 0 && samsvörun_Word(klasi_Skilgreining_yfireining[klasi_Skilgreining], Heiti))) return true;
            for (int innri_samtenging_staða = 0; innri_samtenging_staða < klasi_viðmót_COUNT[klasi_Skilgreining]; innri_samtenging_staða++) if (samsvörun_Word(klasi_viðmót[klasi_Skilgreining * 16 + innri_samtenging_staða], Heiti)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int bæti_gögn, boolean SLÓÐ) {
        if (첫값 == bæti_gögn) return true;
        if (첫값 <= 0 || bæti_gögn <= 0 || 힙[첫값] != 1 || 힙[bæti_gögn] != 1 || 힙[첫값 + 1] != 힙[bæti_gögn + 1]) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) {
            int x_hnit = 힙[첫값 + 2 + Loop_INDEX], Y_hnit = 힙[bæti_gögn + 2 + Loop_INDEX];
            if (SLÓÐ) { if (x_hnit == '.') x_hnit = '/'; if (Y_hnit == '.') Y_hnit = '/'; }
            if (x_hnit != Y_hnit) return false;
        }
        return true;
    }
    static boolean 객체유효(int hlutur_tilvísun) {
        if (hlutur_tilvísun == 0) { bilun_VALUE("NullPointerException"); return false; }
        if (hlutur_tilvísun < 1 || hlutur_tilvísun >= 힙끝 || 힙폭[hlutur_tilvísun] < 2 || 힙[hlutur_tilvísun] == 0) { bilun_VALUE("invalid object reference"); return false; }
        return true;
    }
    static void verja_VALUE(int hlutur_tilvísun) {
        if (hlutur_tilvísun > 0 && hlutur_tilvísun < 힙끝 && 힙폭[hlutur_tilvísun] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = hlutur_tilvísun;
    }
    static void sýna_VALUE(int hlutur_tilvísun) {
        if (hlutur_tilvísun > 0 && hlutur_tilvísun < 힙끝 && 힙폭[hlutur_tilvísun] >= 2 && 힙[hlutur_tilvísun] != 0 && 힙표시[hlutur_tilvísun] == 0) {
            힙표시[hlutur_tilvísun] = 1; 표시대기[birta_COUNT++] = hlutur_tilvísun;
        }
    }
    static void 수거() {
        birta_COUNT = 0; Safn_COUNT++;
        for (int athuga_staða = 1; athuga_staða < 힙끝; athuga_staða += 힙폭[athuga_staða]) 힙표시[athuga_staða] = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < strengur_tilvísun.length; Loop_INDEX++) sýna_VALUE(strengur_tilvísun[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < rauf_COUNT; Loop_INDEX++) if ((rauf_Heimildir[Loop_INDEX] & 8) != 0 && 형종류(rauf_TYPE[Loop_INDEX]) == 2) sýna_VALUE(rauf_gögn[Loop_INDEX]);
        for (int 임시값 = 0; 임시값 < þráður_COUNT; 임시값++) {
            sýna_VALUE(þráður_hlutur[임시값]); sýna_VALUE(þráður_markmið[임시값]);
            int 꼭대기자리 = 임시값 == 현재가닥 ? ramma_INDEX : þráður_ramma[임시값];
            for (int skrá_INDEX = 임시값 * 32; skrá_INDEX <= 꼭대기자리; skrá_INDEX++) {
                for (int innri_samtenging_staða = 0; innri_samtenging_staða < 함수지역[ramma_aðferð[skrá_INDEX]]; innri_samtenging_staða++) if (staðbundið_TYPE[skrá_INDEX * 128 + innri_samtenging_staða] == 2) sýna_VALUE(staðbundið_VALUE[skrá_INDEX * 128 + innri_samtenging_staða]);
                for (int innri_samtenging_staða = 0; innri_samtenging_staða < ramma_bunki[skrá_INDEX]; innri_samtenging_staða++) if (스택형[skrá_INDEX * 128 + innri_samtenging_staða] == 2) sýna_VALUE(스택값[skrá_INDEX * 128 + innri_samtenging_staða]);
            }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 화면참조.length; Loop_INDEX++) sýna_VALUE(화면참조[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 나중수; Loop_INDEX++) sýna_VALUE(나중실행[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Store_heiltala.length; Loop_INDEX++) sýna_VALUE(Store_heiltala[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < klasi_Skilgreining_COUNT; Loop_INDEX++) sýna_VALUE(klasi_Loka[Loop_INDEX]);
        for (int athuga_staða = 1; athuga_staða < 힙끝; athuga_staða += 힙폭[athuga_staða]) if (잠금깊이[athuga_staða] > 0) sýna_VALUE(athuga_staða);
        sýna_VALUE(던진객체);
        for (int Loop_INDEX = 0; Loop_INDEX < 잠시수; Loop_INDEX++) sýna_VALUE(잠시참조[Loop_INDEX]);
        while (birta_COUNT > 0) {
            int hlutur_tilvísun = 표시대기[--birta_COUNT], tegund_CODE = 힙[hlutur_tilvísun];
            for (int Loop_INDEX = hlutur_tilvísun + 2; Loop_INDEX < hlutur_tilvísun + 힙폭[hlutur_tilvísun]; Loop_INDEX++) if (tegund_CODE == 3 || tegund_CODE == 4 || 힙참조[Loop_INDEX] != 0) sýna_VALUE(힙[Loop_INDEX]);
        }
        for (int athuga_staða = 1; athuga_staða < 힙끝; athuga_staða += 힙폭[athuga_staða]) if (힙표시[athuga_staða] == 0) 힙[athuga_staða] = 0;
        for (int athuga_staða = 1; athuga_staða < 힙끝; athuga_staða += 힙폭[athuga_staða]) if (힙[athuga_staða] == 0) {
            while (athuga_staða + 힙폭[athuga_staða] < 힙끝 && 힙[athuga_staða + 힙폭[athuga_staða]] == 0) { int Áfram_staða = athuga_staða + 힙폭[athuga_staða]; 힙폭[athuga_staða] += 힙폭[Áfram_staða]; 힙폭[Áfram_staða] = 0; }
            if (athuga_staða + 힙폭[athuga_staða] == 힙끝) { 힙끝 = athuga_staða; break; }
        }
    }
    static int 새기억(int 종류, int lengd_VALUE) {
        if (lengd_VALUE < 0) { bilun_VALUE("NegativeArraySizeException"); return 0; }
        if (lengd_VALUE > 힙.length - 3) { bilun_VALUE("object heap exhausted"); return 0; }
        int 필요수 = lengd_VALUE + 2, hlutur_tilvísun = 0;
        if (필요수 <= 힙.length - 힙끝) { hlutur_tilvísun = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { hlutur_tilvísun = 읽는자리; break; }
            if (hlutur_tilvísun != 0) {
                int 남은길이 = 힙폭[hlutur_tilvísun] - 필요수;
                if (남은길이 >= 2) { 힙폭[hlutur_tilvísun + 필요수] = 남은길이; 힙[hlutur_tilvísun + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { hlutur_tilvísun = 힙끝; 힙끝 += 필요수; }
        }
        if (hlutur_tilvísun == 0) { bilun_VALUE("object heap exhausted"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < 필요수; Loop_INDEX++) { 힙[hlutur_tilvísun + Loop_INDEX] = 0; 힙참조[hlutur_tilvísun + Loop_INDEX] = 0; 힙폭[hlutur_tilvísun + Loop_INDEX] = 0; }
        ARRAY_eining[hlutur_tilvísun] = 0;
        힙폭[hlutur_tilvísun] = 필요수; 힙[hlutur_tilvísun] = 종류; 힙[hlutur_tilvísun + 1] = lengd_VALUE; verja_VALUE(hlutur_tilvísun); return hlutur_tilvísun;
    }
    static int undantekning_klasi(String heiti_fasti) {
        if (자바도구.같음(heiti_fasti, "java/lang/Throwable")) return 1;
        if (자바도구.같음(heiti_fasti, "java/lang/Exception")) return 2;
        if (자바도구.같음(heiti_fasti, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(heiti_fasti, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(heiti_fasti, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(heiti_fasti, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(heiti_fasti, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(heiti_fasti, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(heiti_fasti, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(heiti_fasti, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(heiti_fasti, "java/io/IOException")) return 11;
        if (자바도구.같음(heiti_fasti, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(heiti_fasti, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(heiti_fasti, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(heiti_fasti, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int undantekning_fasti(int Heiti) {
        for (int Loop_INDEX = 1; Loop_INDEX <= 41; Loop_INDEX++) if (Word_SMS(Heiti, undantekning_heiti(Loop_INDEX))) return Loop_INDEX;
        return 0;
    }
    static String undantekning_heiti(int Auðkenni_VALUE) {
        if (Auðkenni_VALUE == 40) return "java/lang/InterruptedException";
        if (Auðkenni_VALUE == 41) return "Íslenska/eigin/대기중단예외";
        if (Auðkenni_VALUE == 39) return "java/net/SocketException";
        if (Auðkenni_VALUE == 20) return "Íslenska/eigin/undantekning";
        if (Auðkenni_VALUE == 21) return "Íslenska/eigin/실행예외";
        if (Auðkenni_VALUE == 22) return "Íslenska/eigin/I_Ú_undantekning";
        if (Auðkenni_VALUE == 23) return "Íslenska/eigin/Bíddu_TIMEOUT_undantekning";
        if (Auðkenni_VALUE == 24) return "Íslenska/eigin/slóð_LOOKUP_undantekning";
        if (Auðkenni_VALUE == 25) return "Íslenska/eigin/파일없음예외";
        if (Auðkenni_VALUE == 26) return "Íslenska/eigin/통신예외";
        if (Auðkenni_VALUE == 27) return "Íslenska/eigin/ógilt_frumbreyta_undantekning";
        if (Auðkenni_VALUE == 28) return "Íslenska/eigin/númer_snið_bilun";
        if (Auðkenni_VALUE == 29) return "Íslenska/eigin/범위예외";
        if (Auðkenni_VALUE == 30) return "Íslenska/eigin/배열범위예외";
        if (Auðkenni_VALUE == 31) return "Íslenska/eigin/문자열범위예외";
        if (Auðkenni_VALUE == 32) return "Íslenska/eigin/NULL_tilvísun_undantekning";
        if (Auðkenni_VALUE == 33) return "Íslenska/eigin/산술예외";
        if (Auðkenni_VALUE == 34) return "Íslenska/eigin/staða_undantekning";
        if (Auðkenni_VALUE == 35) return "Íslenska/eigin/TYPE_senda_út_undantekning";
        if (Auðkenni_VALUE == 36) return "Íslenska/eigin/음수배열크기예외";
        if (Auðkenni_VALUE == 37) return "Íslenska/eigin/ARRAY_Store_bilun";
        if (Auðkenni_VALUE == 38) return "Íslenska/eigin/þráður_staða_undantekning";
        if (Auðkenni_VALUE == 1) return "java/lang/Throwable"; if (Auðkenni_VALUE == 2) return "java/lang/Exception";
        if (Auðkenni_VALUE == 3) return "java/lang/RuntimeException"; if (Auðkenni_VALUE == 4) return "java/lang/ArithmeticException";
        if (Auðkenni_VALUE == 5) return "java/lang/NullPointerException"; if (Auðkenni_VALUE == 6) return "java/lang/IndexOutOfBoundsException";
        if (Auðkenni_VALUE == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (Auðkenni_VALUE == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (Auðkenni_VALUE == 9) return "java/lang/IllegalArgumentException"; if (Auðkenni_VALUE == 10) return "java/lang/NumberFormatException";
        if (Auðkenni_VALUE == 11) return "java/io/IOException"; if (Auðkenni_VALUE == 12) return "java/io/FileNotFoundException";
        if (Auðkenni_VALUE == 17) return "java/lang/ArrayStoreException";
        if (Auðkenni_VALUE == 18) return "java/net/UnknownHostException";
        if (Auðkenni_VALUE == 19) return "java/net/SocketTimeoutException";
        if (Auðkenni_VALUE == 16) return "java/lang/IllegalThreadStateException";
        if (Auðkenni_VALUE == 13) return "java/lang/IllegalStateException"; if (Auðkenni_VALUE == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int undantekning_yfireining(int Auðkenni_VALUE) {
        if (Auðkenni_VALUE == 40) return 2;
        if (Auðkenni_VALUE == 41) return 40;
        if (Auðkenni_VALUE == 39) return 11;
        if (Auðkenni_VALUE == 1) return 0;
        if (Auðkenni_VALUE == 2) return 1;
        if (Auðkenni_VALUE == 3) return 2;
        if (Auðkenni_VALUE == 4) return 3;
        if (Auðkenni_VALUE == 5) return 3;
        if (Auðkenni_VALUE == 6) return 3;
        if (Auðkenni_VALUE == 7) return 6;
        if (Auðkenni_VALUE == 8) return 6;
        if (Auðkenni_VALUE == 9) return 3;
        if (Auðkenni_VALUE == 10) return 9;
        if (Auðkenni_VALUE == 11) return 2;
        if (Auðkenni_VALUE == 12) return 11;
        if (Auðkenni_VALUE == 13) return 3;
        if (Auðkenni_VALUE == 14) return 3;
        if (Auðkenni_VALUE == 15) return 3;
        if (Auðkenni_VALUE == 16) return 9;
        if (Auðkenni_VALUE == 17) return 3;
        if (Auðkenni_VALUE == 18) return 11;
        if (Auðkenni_VALUE == 19) return 11;
        if (Auðkenni_VALUE == 20) return 2;
        if (Auðkenni_VALUE == 21) return 3;
        if (Auðkenni_VALUE == 22) return 11;
        if (Auðkenni_VALUE == 23) return 22;
        if (Auðkenni_VALUE == 24) return 22;
        if (Auðkenni_VALUE == 25) return 22;
        if (Auðkenni_VALUE == 26) return 22;
        if (Auðkenni_VALUE == 27) return 9;
        if (Auðkenni_VALUE == 28) return 27;
        if (Auðkenni_VALUE == 29) return 6;
        if (Auðkenni_VALUE == 30) return 29;
        if (Auðkenni_VALUE == 31) return 29;
        if (Auðkenni_VALUE == 32) return 5;
        if (Auðkenni_VALUE == 33) return 4;
        if (Auðkenni_VALUE == 34) return 13;
        if (Auðkenni_VALUE == 35) return 14;
        if (Auðkenni_VALUE == 36) return 15;
        if (Auðkenni_VALUE == 37) return 17;
        if (Auðkenni_VALUE == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int raun_VALUE, int 요구값) {
        for (int 깊이 = 0; raun_VALUE != 0 && 깊이 < 16; 깊이++, raun_VALUE = undantekning_yfireining(raun_VALUE))
            if (raun_VALUE == 요구값) return true;
        return false;
    }
    static void 예외던짐(int Auðkenni_VALUE, String LESTUMIG_tilvísun) {
        int hlutur_tilvísun = 새기억(9, 2); if (Villa) return;
        힙[hlutur_tilvísun + 2] = Auðkenni_VALUE; 힙[hlutur_tilvísun + 3] = hýsa_stafur(LESTUMIG_tilvísun); 힙참조[hlutur_tilvísun + 3] = 1;
        던진객체 = hlutur_tilvísun; Villa = true;
    }
    static boolean samsvörun_hlutur(int hlutur_tilvísun, int Heiti) {
        if (hlutur_tilvísun == 0) return true;
        if (!객체유효(hlutur_tilvísun)) return false;
        int tegund_CODE = 힙[hlutur_tilvísun];
        if (Word_SMS(Heiti, "java/lang/Object")) return true;
        if (tegund_CODE >= 32) return 종포함(tegund_CODE - 32, Heiti);
        if (tegund_CODE == 9) { int markmið_slóð = undantekning_fasti(Heiti); return markmið_slóð != 0 && 예외포함(힙[hlutur_tilvísun + 2], markmið_slóð); }
        if (tegund_CODE == 1) return Word_SMS(Heiti, "java/lang/String") || Word_SMS(Heiti, "java/lang/CharSequence");
        if (tegund_CODE == 4) return Word_SMS(Heiti, "java/lang/StringBuilder") || Word_SMS(Heiti, "java/lang/CharSequence");
        if (tegund_CODE == 10) return Word_SMS(Heiti, "java/util/ArrayList") || Word_SMS(Heiti, "java/util/List");
        if (tegund_CODE == 11) return Word_SMS(Heiti, "java/util/HashMap") || Word_SMS(Heiti, "java/util/Map");
        if (tegund_CODE == 12) return Word_SMS(Heiti, "java/lang/Integer") || Word_SMS(Heiti, "java/lang/Number");
        if (tegund_CODE >= 24 && tegund_CODE <= 28 && 힙[hlutur_tilvísun + 13] != 0) return 한국어화면종(Heiti) == tegund_CODE || Word_SMS(Heiti, "Íslenska/eigin/화면구성요소");
        if (tegund_CODE >= 24 && tegund_CODE <= 28) return (한국어화면종(Heiti) == 0 && 화면종(Heiti) == tegund_CODE) || Word_SMS(Heiti, "java/awt/Component") || Word_SMS(Heiti, "java/awt/Container") || Word_SMS(Heiti, "javax/swing/JComponent");
        if (tegund_CODE == 29) return Word_SMS(Heiti, 힙[hlutur_tilvísun + 3] != 0 ? "Íslenska/eigin/동작알림" : "java/awt/event/ActionEvent");
        if (tegund_CODE == 30) return Word_SMS(Heiti, "java/awt/FlowLayout") || Word_SMS(Heiti, "java/awt/LayoutManager");
        if (tegund_CODE == 17) return Word_SMS(Heiti, "java/net/Socket");
        if (tegund_CODE == 18) return Word_SMS(Heiti, "java/net/ServerSocket");
        if (tegund_CODE == 19) return Word_SMS(Heiti, 힙[hlutur_tilvísun + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (tegund_CODE == 14) return Word_SMS(Heiti, "java/net/InetAddress");
        if (tegund_CODE == 15) return Word_SMS(Heiti, "java/net/DatagramSocket");
        if (tegund_CODE == 16) return Word_SMS(Heiti, "java/net/DatagramPacket");
        if (tegund_CODE == 13) return Word_SMS(Heiti, 힙[hlutur_tilvísun + 3] != 0 ? "Íslenska/eigin/starfskraftur" : "java/lang/Thread");
        if (tegund_CODE == 2) return Word_SMS(Heiti, "[I"); if (tegund_CODE == 20) return Word_SMS(Heiti, "[B"); if (tegund_CODE == 21) return Word_SMS(Heiti, "[Z");
        if (tegund_CODE == 22) return Word_SMS(Heiti, "[C"); if (tegund_CODE == 23) return Word_SMS(Heiti, "[S");
        if (tegund_CODE != 3) return false;
        if (Word_SMS(Heiti, "[Ljava/lang/Object;")) return true;
        int þáttur = ARRAY_eining[hlutur_tilvísun];
        if (þáttur == -1) return Word_SMS(Heiti, "[Ljava/lang/String;") || Word_SMS(Heiti, "[Ljava/lang/CharSequence;");
        if (þáttur == 0) return false;
        if (배열종비교(þáttur, Heiti)) return true;
        if ((Word_SMS(þáttur, "java/lang/String") || Word_SMS(þáttur, "java/lang/StringBuilder")) && Word_SMS(Heiti, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDEX = 0; Loop_INDEX < klasi_Skilgreining_COUNT; Loop_INDEX++) if (samsvörun_Word(klasi_Skilgreining_heiti[Loop_INDEX], þáttur)) {
            for (int stafkóði = Loop_INDEX, 중첩깊이 = 0; stafkóði >= 0 && 중첩깊이 < 16; 중첩깊이++, stafkóði = yfireining_klasi(stafkóði)) {
                if (배열종비교(klasi_Skilgreining_yfireining[stafkóði], Heiti)) return true;
                for (int innri_samtenging_staða = 0; innri_samtenging_staða < klasi_viðmót_COUNT[stafkóði]; innri_samtenging_staða++) if (배열종비교(klasi_viðmót[stafkóði * 16 + innri_samtenging_staða], Heiti)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int heiti_fasti, int 형식참조) {
        int athuga_staða = 상가[형식참조], færsla_COUNT = fasti_SECOND_VALUE[형식참조];
        if (heiti_fasti == 0 || færsla_COUNT < 4 || Skrá[athuga_staða] != '[' || Skrá[athuga_staða + 1] != 'L' || Skrá[athuga_staða + færsla_COUNT - 1] != ';' || fasti_SECOND_VALUE[heiti_fasti] != færsla_COUNT - 3) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < færsla_COUNT - 3; Loop_INDEX++) if (Skrá[상가[heiti_fasti] + Loop_INDEX] != Skrá[athuga_staða + 2 + Loop_INDEX]) return false;
        return true;
    }
    static void hald_undantekning() {
        if (던진객체 == 0) return;
        Villa = false;
        while (ramma_INDEX >= 현재가닥 * 32) {
            int skrá_INDEX = ramma_aðferð[ramma_INDEX], 읽는자리 = ramma_skipun[ramma_INDEX];
            for (int Loop_INDEX = 0; Loop_INDEX < 잡기수; Loop_INDEX++) if (잡기함수[Loop_INDEX] == skrá_INDEX && 읽는자리 >= 잡기시작[Loop_INDEX] && 읽는자리 < 잡기끝[Loop_INDEX]
                && (잡기종[Loop_INDEX] == 0 || samsvörun_hlutur(던진객체, 잡기종[Loop_INDEX]))) {
                ramma_staða[ramma_INDEX] = 잡기위치[Loop_INDEX]; ramma_bunki[ramma_INDEX] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (frumstilla_ramma[ramma_INDEX] != 0) klasi_Skilgreining_staða[frumstilla_ramma[ramma_INDEX] - 1] = 3;
            if (ramma_Loka[ramma_INDEX] != 0) { losa_Loka(ramma_Loka[ramma_INDEX]); ramma_Loka[ramma_INDEX] = 0; }
            ramma_INDEX--;
        }
        notandi.Skrift("Uncaught ");
        if (힙[던진객체] == 9) { notandi.Skrift(undantekning_heiti(힙[던진객체 + 2])); notandi.Skrift(": "); skrifa_SMS(힙[던진객체 + 3]); }
        else notandi.Skrift("user exception");
        notandi.skrifa_stafur_VALUE(10); 던진객체 = 0; Villa = true;
    }
    // 이 JVM의 스택 항목은 현재 category-1(int/reference)만 허용한다.
    static void bunki_skipun(int skipun_CODE) {
        int 첫값 = 빼기(0), 첫형식 = skila_TYPE;
        if (skipun_CODE == 87) return;
        if (skipun_CODE == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int bæti_gögn = 빼기(0), SECOND_snið = skila_TYPE;
        if (skipun_CODE == 88) return;
        if (skipun_CODE == 90) { 넣기(첫값, 첫형식); 넣기(bæti_gögn, SECOND_snið); 넣기(첫값, 첫형식); return; }
        if (skipun_CODE == 92) { 넣기(bæti_gögn, SECOND_snið); 넣기(첫값, 첫형식); 넣기(bæti_gögn, SECOND_snið); 넣기(첫값, 첫형식); return; }
        if (skipun_CODE == 95) { 넣기(첫값, 첫형식); 넣기(bæti_gögn, SECOND_snið); return; }
        int stafkóði = 빼기(0), 셋째형식 = skila_TYPE;
        if (skipun_CODE == 91) { 넣기(첫값, 첫형식); 넣기(stafkóði, 셋째형식); 넣기(bæti_gögn, SECOND_snið); 넣기(첫값, 첫형식); return; }
        if (skipun_CODE == 93) { 넣기(bæti_gögn, SECOND_snið); 넣기(첫값, 첫형식); 넣기(stafkóði, 셋째형식); 넣기(bæti_gögn, SECOND_snið); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = skila_TYPE;
        넣기(bæti_gögn, SECOND_snið); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(stafkóði, 셋째형식); 넣기(bæti_gögn, SECOND_snið); 넣기(첫값, 첫형식);
    }
    static void 새객체(int heiti_fasti, int 시작점) {
        int tegund_CODE = 0, 유효길이 = 0, undantekning_tilvísun = undantekning_fasti(heiti_fasti);
        if (Word_SMS(heiti_fasti, "java/lang/StringBuilder")) { tegund_CODE = 4; 유효길이 = 1; }
        if (Word_SMS(heiti_fasti, "java/io/FileInputStream")) { tegund_CODE = 5; 유효길이 = 2; }
        if (Word_SMS(heiti_fasti, "java/io/FileOutputStream")) { tegund_CODE = 6; 유효길이 = 2; }
        if (undantekning_tilvísun != 0) { tegund_CODE = 9; 유효길이 = 2; }
        if (Word_SMS(heiti_fasti, "java/util/ArrayList")) { tegund_CODE = 10; 유효길이 = 2; }
        if (Word_SMS(heiti_fasti, "java/util/HashMap")) { tegund_CODE = 11; 유효길이 = 2; }
        if (Word_SMS(heiti_fasti, "java/lang/Integer")) { tegund_CODE = 12; 유효길이 = 1; }
        if (Word_SMS(heiti_fasti, "java/net/Socket")) { tegund_CODE = 17; 유효길이 = 5; }
        if (Word_SMS(heiti_fasti, "java/net/ServerSocket")) { tegund_CODE = 18; 유효길이 = 5; }
        if (Word_SMS(heiti_fasti, "java/net/DatagramSocket")) { tegund_CODE = 15; 유효길이 = 3; }
        if (Word_SMS(heiti_fasti, "java/net/DatagramPacket")) { tegund_CODE = 16; 유효길이 = 4; }
        if (Word_SMS(heiti_fasti, "java/lang/Thread") || Word_SMS(heiti_fasti, "Íslenska/eigin/starfskraftur")) { tegund_CODE = 13; 유효길이 = 2; }
        if (Word_SMS(heiti_fasti, "java/lang/Object")) { tegund_CODE = 8; }
        if (tegund_CODE == 0 && 화면종(heiti_fasti) != 0) { tegund_CODE = 화면종(heiti_fasti); 유효길이 = 12; }
        if (tegund_CODE == 0) {
            int stafkóði = FIND_klasi_Skilgreining(heiti_fasti); if (stafkóði < 0 || Villa || !frumstilla(stafkóði, 시작점)) return;
            tegund_CODE = 32 + stafkóði; 유효길이 = klasi_rauf_COUNT[stafkóði];
        }
        int hlutur_tilvísun = úthluta_geymsla(tegund_CODE, 유효길이); if (Villa) return;
        if (tegund_CODE == 13 && Word_SMS(heiti_fasti, "Íslenska/eigin/starfskraftur")) 힙[hlutur_tilvísun + 3] = 1;
        if (tegund_CODE >= 24 && tegund_CODE <= 28 && 한국어화면종(heiti_fasti) != 0) 힙[hlutur_tilvísun + 13] = 1;
        if (tegund_CODE == 5 || tegund_CODE == 6 || tegund_CODE == 15 || tegund_CODE == 17 || tegund_CODE == 18) 힙[hlutur_tilvísun + 2] = -1;
        if (tegund_CODE == 9) 힙[hlutur_tilvísun + 2] = undantekning_tilvísun;
        넣기(hlutur_tilvísun, 2);
    }
    static boolean 값같음(int 첫값, int bæti_gögn) {
        if (첫값 == bæti_gögn) return true;
        if (첫값 == 0 || bæti_gögn == 0 || 첫값 < 0 || bæti_gögn < 0 || 첫값 >= 힙끝 || bæti_gögn >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[bæti_gögn] == 1) return 글같음(첫값, bæti_gögn, false);
        return 힙[첫값] == 12 && 힙[bæti_gögn] == 12 && 힙[첫값 + 2] == 힙[bæti_gögn + 2];
    }
    static int 글조각(int hlutur_tilvísun, int Opna_staða, int ljúka_staða) {
        if (!hlutur_VALUE(hlutur_tilvísun, 1)) return 0;
        if (Opna_staða < 0 || ljúka_staða < Opna_staða || ljúka_staða > 힙[hlutur_tilvísun + 1]) { bilun_VALUE("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = úthluta_geymsla(1, ljúka_staða - Opna_staða); if (Villa) return 0;
        for (int Loop_INDEX = Opna_staða; Loop_INDEX < ljúka_staða; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX - Opna_staða] = 힙[hlutur_tilvísun + 2 + Loop_INDEX];
        return 반환값;
    }
    static int Tengja_SMS(int 첫값, int bæti_gögn) {
        if (!hlutur_VALUE(첫값, 1) || !hlutur_VALUE(bæti_gögn, 1)) return 0;
        int færsla_COUNT = 힙[첫값 + 1], aðferð_INDEX = 힙[bæti_gögn + 1], 반환값 = úthluta_geymsla(1, færsla_COUNT + aðferð_INDEX); if (Villa) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < færsla_COUNT; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 힙[첫값 + 2 + Loop_INDEX];
        for (int Loop_INDEX = 0; Loop_INDEX < aðferð_INDEX; Loop_INDEX++) 힙[반환값 + 2 + færsla_COUNT + Loop_INDEX] = 힙[bæti_gögn + 2 + Loop_INDEX];
        return 반환값;
    }
    static boolean 기본호출(int eigandi, int heiti_fasti, int 서술상수, int skipun_CODE) {
        if (Word_SMS(eigandi, "Íslenska/eigin/실행인수") && skipun_CODE == 184) {
            if (Word_SMS(heiti_fasti, "vara_COUNT") && Word_SMS(서술상수, "()I")) { 넣기(notandi.인수개수() - 1, 1); return true; }
            if (Word_SMS(heiti_fasti, "Texti") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= notandi.인수개수() - 1) 예외던짐(29, "keyra_skipun Viðföng 범위를 벗어났습니다");
                else 넣기(hýsa_stafur(notandi.Viðföng(순번 + 1)), 2);
                return true;
            }
            bilun_VALUE("지원하지 않는 Íslenska keyra_skipun Viðföng 호출"); return true;
        }
        if (Word_SMS(eigandi, "Íslenska/eigin/starfskraftur")) { Ferli_þráður(heiti_fasti, 서술상수, skipun_CODE, true); return true; }
        if (한국어화면소유(eigandi)) { 한국어화면호출(eigandi, heiti_fasti, 서술상수, skipun_CODE); return true; }
        if (화면소유(eigandi)) { 화면호출(eigandi, heiti_fasti, 서술상수, skipun_CODE); return true; }
        if (Word_SMS(eigandi, "java/net/Socket") || Word_SMS(eigandi, "java/net/ServerSocket") || Word_SMS(eigandi, "java/io/InputStream") || Word_SMS(eigandi, "java/io/OutputStream")) { 흐름호출(eigandi, heiti_fasti, 서술상수, skipun_CODE); return true; }
        if (Word_SMS(eigandi, "Íslenska/eigin/kjarni_VALUE") && skipun_CODE == 184) {
            if (Word_SMS(heiti_fasti, "화면너비") && Word_SMS(서술상수, "()I")) { 넣기(notandi.화면너비(), 1); return true; }
            if (Word_SMS(heiti_fasti, "화면높이") && Word_SMS(서술상수, "()I")) { 넣기(notandi.화면높이(), 1); return true; }
            if (Word_SMS(heiti_fasti, "밀리초") && Word_SMS(서술상수, "()I")) { 넣기(notandi.밀리초(), 1); return true; }
            if (Word_SMS(heiti_fasti, "그림대기") && Word_SMS(서술상수, "()I")) { 넣기(notandi.그림대기(), 1); return true; }
            if (Word_SMS(heiti_fasti, "사각형") && Word_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), Y_hnit = 빼기(1), x_hnit = 빼기(1); 넣기(notandi.사각형(x_hnit, Y_hnit, 너비, 높이, 색상), 1); return true; }
        }
        if (Word_SMS(eigandi, "java/net/InetAddress") || Word_SMS(eigandi, "java/net/DatagramPacket") || Word_SMS(eigandi, "java/net/DatagramSocket")) { 통신호출(eigandi, heiti_fasti, 서술상수, skipun_CODE); return true; }
        if (Word_SMS(eigandi, "java/lang/Thread")) { 가닥호출(heiti_fasti, 서술상수, skipun_CODE); return true; }
        if (Word_SMS(eigandi, "java/lang/Object")) {
            if (Word_SMS(heiti_fasti, "<init>") && Word_SMS(서술상수, "()V") && skipun_CODE == 183) { 객체유효(빼기(2)); return true; }
            if (Word_SMS(heiti_fasti, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int bæti_gögn = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == bæti_gögn ? 1 : 0, 1); return true; }
        }
        if (undantekning_fasti(eigandi) != 0) {
            if (Word_SMS(heiti_fasti, "<init>") && skipun_CODE == 183 && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int biðja = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), hlutur_tilvísun = 빼기(2);
                if (hlutur_VALUE(hlutur_tilvísun, 9)) { 힙[hlutur_tilvísun + 3] = biðja; 힙참조[hlutur_tilvísun + 3] = 1; } return true;
            }
            if ((Word_SMS(heiti_fasti, "getMessage") || Word_SMS(heiti_fasti, "설명")) && Word_SMS(서술상수, "()Ljava/lang/String;")) { int hlutur_tilvísun = 빼기(2); if (hlutur_VALUE(hlutur_tilvísun, 9)) 넣기(힙[hlutur_tilvísun + 3], 2); return true; }
        }
        if (Word_SMS(eigandi, "java/lang/String")) {
            if (skipun_CODE == 182 && Word_SMS(heiti_fasti, "getBytes") && (Word_SMS(서술상수, "()[B") || Word_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int kóðun_heiti = Word_SMS(서술상수, "()[B") ? 0 : 빼기(2), hlutur_tilvísun = 빼기(2);
                if (!hlutur_VALUE(hlutur_tilvísun, 1)) return true;
                if (kóðun_heiti != 0 && !글같음(kóðun_heiti, hýsa_stafur("UTF-8"), false) && !글같음(kóðun_heiti, hýsa_stafur("UTF8"), false) && !글같음(kóðun_heiti, hýsa_stafur("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int færsla_COUNT = 힙[hlutur_tilvísun + 1], 반환값 = úthluta_geymsla(20, færsla_COUNT * 3), 사용수 = 0; if (Villa) return true;
                for (int innri_samtenging_staða = 0; innri_samtenging_staða < færsla_COUNT; innri_samtenging_staða++) {
                    int stafkóði = 힙[hlutur_tilvísun + 2 + innri_samtenging_staða];
                    if (stafkóði >= 0xd800 && stafkóði <= 0xdbff && innri_samtenging_staða + 1 < færsla_COUNT && 힙[hlutur_tilvísun + 3 + innri_samtenging_staða] >= 0xdc00 && 힙[hlutur_tilvísun + 3 + innri_samtenging_staða] <= 0xdfff) stafkóði = 0x10000 + ((stafkóði - 0xd800) << 10) + 힙[hlutur_tilvísun + 2 + ++innri_samtenging_staða] - 0xdc00;
                    else if (stafkóði >= 0xd800 && stafkóði <= 0xdfff) stafkóði = '?';
                    if (stafkóði < 128) 힙[반환값 + 2 + 사용수++] = stafkóði;
                    else { int bæti_COUNT = stafkóði < 2048 ? 2 : stafkóði < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((bæti_COUNT == 2 ? 192 : bæti_COUNT == 3 ? 224 : 240) | stafkóði >> (6 * (bæti_COUNT - 1))); for (int Samanburður_staða = bæti_COUNT - 1; Samanburður_staða > 0; Samanburður_staða--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | stafkóði >> (6 * (Samanburður_staða - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (skipun_CODE == 184 && Word_SMS(heiti_fasti, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(tölustafur_stafur(빼기(1)), 2); return true; }
            if (skipun_CODE != 182) return false;
            if (Word_SMS(heiti_fasti, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int bæti_gögn = 빼기(2), 첫값 = 빼기(2); if (hlutur_VALUE(첫값, 1)) 넣기(글같음(첫값, bæti_gögn, false) ? 1 : 0, 1); return true; }
            if (Word_SMS(heiti_fasti, "isEmpty") && Word_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (hlutur_VALUE(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_SMS(heiti_fasti, "substring") && (Word_SMS(서술상수, "(I)Ljava/lang/String;") || Word_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SECOND_VALUE = Word_SMS(서술상수, "(II)Ljava/lang/String;"); int ljúka_staða = SECOND_VALUE ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (hlutur_VALUE(첫값, 1)) 넣기(글조각(첫값, 시작점, SECOND_VALUE ? ljúka_staða : 힙[첫값 + 1]), 2); return true;
            }
            if (Word_SMS(heiti_fasti, "concat") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int bæti_gögn = 빼기(2), 첫값 = 빼기(2); 넣기(Tengja_SMS(첫값, bæti_gögn), 2); return true; }
            if (Word_SMS(heiti_fasti, "hashCode") && Word_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), tæting_VALUE = 0; if (hlutur_VALUE(첫값, 1)) { for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) tæting_VALUE = tæting_VALUE * 31 + 힙[첫값 + 2 + Loop_INDEX]; 넣기(tæting_VALUE, 1); } return true; }
            if (Word_SMS(heiti_fasti, "toString") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (hlutur_VALUE(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_SMS(eigandi, "java/lang/Integer")) {
            if (skipun_CODE == 184 && Word_SMS(heiti_fasti, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int gögn_VALUE = 빼기(1), hlutur_tilvísun = gögn_VALUE >= -128 && gögn_VALUE <= 127 ? Store_heiltala[gögn_VALUE + 128] : 0; if (hlutur_tilvísun == 0) { hlutur_tilvísun = úthluta_geymsla(12, 1); if (!Villa) { 힙[hlutur_tilvísun + 2] = gögn_VALUE; if (gögn_VALUE >= -128 && gögn_VALUE <= 127) Store_heiltala[gögn_VALUE + 128] = hlutur_tilvísun; } } 넣기(hlutur_tilvísun, 2); return true; }
            if (skipun_CODE == 183 && Word_SMS(heiti_fasti, "<init>") && Word_SMS(서술상수, "(I)V")) { int gögn_VALUE = 빼기(1), hlutur_tilvísun = 빼기(2); if (hlutur_VALUE(hlutur_tilvísun, 12)) 힙[hlutur_tilvísun + 2] = gögn_VALUE; return true; }
            if (skipun_CODE == 182 && Word_SMS(heiti_fasti, "intValue") && Word_SMS(서술상수, "()I")) { int hlutur_tilvísun = 빼기(2); if (hlutur_VALUE(hlutur_tilvísun, 12)) 넣기(힙[hlutur_tilvísun + 2], 1); return true; }
            if (skipun_CODE == 184 && Word_SMS(heiti_fasti, "toString") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(tölustafur_stafur(빼기(1)), 2); return true; }
        }
        if (Word_SMS(eigandi, "java/lang/Math") && skipun_CODE == 184) {
            if (Word_SMS(heiti_fasti, "abs") && Word_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_SMS(heiti_fasti, "min") || Word_SMS(heiti_fasti, "max")) && Word_SMS(서술상수, "(II)I")) { int bæti_gögn = 빼기(1), 첫값 = 빼기(1); 넣기(Word_SMS(heiti_fasti, "min") ? (첫값 < bæti_gögn ? 첫값 : bæti_gögn) : (첫값 > bæti_gögn ? 첫값 : bæti_gögn), 1); return true; }
        }
        if (Word_SMS(eigandi, "java/lang/System") && skipun_CODE == 184) {
            if (Word_SMS(heiti_fasti, "gc") && Word_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Word_SMS(heiti_fasti, "arraycopy") && Word_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int færsla_COUNT = 빼기(1), endastaður_VALUE_INDEX = 빼기(1), bæti_gögn = 빼기(2), Opna_staða = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(bæti_gögn)) {
                    int tegund_CODE = 힙[첫값];
                    if (힙[bæti_gögn] != tegund_CODE || (tegund_CODE != 2 && tegund_CODE != 3 && (tegund_CODE < 20 || tegund_CODE > 23))) bilun_VALUE("arraycopy type mismatch");
                    else if (færsla_COUNT < 0 || Opna_staða < 0 || endastaður_VALUE_INDEX < 0 || Opna_staða > 힙[첫값 + 1] - færsla_COUNT || endastaður_VALUE_INDEX > 힙[bæti_gögn + 1] - færsla_COUNT) bilun_VALUE("ArrayIndexOutOfBoundsException");
                    else if (첫값 == bæti_gögn && endastaður_VALUE_INDEX > Opna_staða) { for (int Loop_INDEX = færsla_COUNT - 1; Loop_INDEX >= 0; Loop_INDEX--) 힙[bæti_gögn + 2 + endastaður_VALUE_INDEX + Loop_INDEX] = 힙[첫값 + 2 + Opna_staða + Loop_INDEX]; }
                    else { for (int Loop_INDEX = 0; Loop_INDEX < færsla_COUNT && !Villa; Loop_INDEX++) { int gögn_VALUE = 힙[첫값 + 2 + Opna_staða + Loop_INDEX]; if (tegund_CODE != 3 || 배열저장가능(bæti_gögn, gögn_VALUE)) 힙[bæti_gögn + 2 + endastaður_VALUE_INDEX + Loop_INDEX] = gögn_VALUE; } }
                }
                return true;
            }
        }
        if (Word_SMS(eigandi, "java/util/ArrayList") || Word_SMS(eigandi, "java/util/List") || Word_SMS(eigandi, "java/util/HashMap") || Word_SMS(eigandi, "java/util/Map")) {
            모음호출(eigandi, heiti_fasti, 서술상수, skipun_CODE); return true;
        }
        return false;
    }
    static void 모음늘리기(int hlutur_tilvísun, int 필요수) {
        int 이전값 = 힙[hlutur_tilvísun + 2], afkastageta_gögn = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (afkastageta_gögn >= 필요수) return;
        int Áfram_staða = afkastageta_gögn < 8 ? 8 : afkastageta_gögn * 2; if (Áfram_staða < 필요수) Áfram_staða = 필요수;
        int gögn_ARRAY = úthluta_geymsla(3, Áfram_staða); if (Villa) return;
        for (int Loop_INDEX = 0; Loop_INDEX < afkastageta_gögn; Loop_INDEX++) 힙[gögn_ARRAY + 2 + Loop_INDEX] = 힙[이전값 + 2 + Loop_INDEX];
        힙[hlutur_tilvísun + 2] = gögn_ARRAY; 힙참조[hlutur_tilvísun + 2] = 1;
    }
    static void 모음호출(int eigandi, int heiti_fasti, int 서술상수, int skipun_CODE) {
        boolean 대응참조 = Word_SMS(eigandi, "java/util/HashMap") || Word_SMS(eigandi, "java/util/Map"); int tegund_CODE = 대응참조 ? 11 : 10;
        if (Word_SMS(heiti_fasti, "<init>") && skipun_CODE == 183 && Word_SMS(서술상수, "()V")) { int hlutur_tilvísun = 빼기(2); if (hlutur_VALUE(hlutur_tilvísun, tegund_CODE)) 모음늘리기(hlutur_tilvísun, 8); return; }
        if (skipun_CODE != 182 && skipun_CODE != 185) { bilun_VALUE("invalid collection invocation"); return; }
        if (Word_SMS(heiti_fasti, "size") && Word_SMS(서술상수, "()I") || Word_SMS(heiti_fasti, "isEmpty") && Word_SMS(서술상수, "()Z")) {
            int hlutur_tilvísun = 빼기(2); if (hlutur_VALUE(hlutur_tilvísun, tegund_CODE)) 넣기(Word_SMS(heiti_fasti, "size") ? 힙[hlutur_tilvísun + 3] : 힙[hlutur_tilvísun + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_SMS(heiti_fasti, "clear") && Word_SMS(서술상수, "()V")) { int hlutur_tilvísun = 빼기(2); if (hlutur_VALUE(hlutur_tilvísun, tegund_CODE)) { int gögn_ARRAY = 힙[hlutur_tilvísun + 2]; for (int Loop_INDEX = 0; Loop_INDEX < 힙[gögn_ARRAY + 1]; Loop_INDEX++) 힙[gögn_ARRAY + 2 + Loop_INDEX] = 0; 힙[hlutur_tilvísun + 3] = 0; } return; }
        if (!대응참조 && Word_SMS(heiti_fasti, "add") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int gögn_VALUE = 빼기(2), hlutur_tilvísun = 빼기(2); if (!hlutur_VALUE(hlutur_tilvísun, 10)) return;
            int færsla_COUNT = 힙[hlutur_tilvísun + 3]; 모음늘리기(hlutur_tilvísun, færsla_COUNT + 1); if (!Villa) { 힙[힙[hlutur_tilvísun + 2] + 2 + færsla_COUNT] = gögn_VALUE; 힙[hlutur_tilvísun + 3] = færsla_COUNT + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_SMS(heiti_fasti, "get") || Word_SMS(heiti_fasti, "remove")) && Word_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Word_SMS(heiti_fasti, "set") && Word_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = Word_SMS(heiti_fasti, "set"); int gögn_VALUE = 지정여부 ? 빼기(2) : 0, færsla_staða = 빼기(1), hlutur_tilvísun = 빼기(2);
            if (!hlutur_VALUE(hlutur_tilvísun, 10)) return;
            int færsla_COUNT = 힙[hlutur_tilvísun + 3], gögn_ARRAY = 힙[hlutur_tilvísun + 2];
            if (færsla_staða < 0 || færsla_staða >= færsla_COUNT) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[gögn_ARRAY + 2 + færsla_staða];
            if (지정여부) 힙[gögn_ARRAY + 2 + færsla_staða] = gögn_VALUE;
            if (Word_SMS(heiti_fasti, "remove")) { for (int Loop_INDEX = færsla_staða + 1; Loop_INDEX < færsla_COUNT; Loop_INDEX++) 힙[gögn_ARRAY + 1 + Loop_INDEX] = 힙[gögn_ARRAY + 2 + Loop_INDEX]; 힙[gögn_ARRAY + 1 + færsla_COUNT] = 0; 힙[hlutur_tilvísun + 3] = færsla_COUNT - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Word_SMS(heiti_fasti, "get") || Word_SMS(heiti_fasti, "remove")) && Word_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(heiti_fasti, "put") && Word_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(heiti_fasti, "containsKey") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_SMS(heiti_fasti, "put"), fjarlægja = Word_SMS(heiti_fasti, "remove");
            int gögn_VALUE = 넣기여부 ? 빼기(2) : 0, Lykill_tilvísun = 빼기(2), hlutur_tilvísun = 빼기(2); if (!hlutur_VALUE(hlutur_tilvísun, 11)) return;
            int færsla_COUNT = 힙[hlutur_tilvísun + 3], gögn_ARRAY = 힙[hlutur_tilvísun + 2], 찾은여부 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < færsla_COUNT; Loop_INDEX++) if (값같음(Lykill_tilvísun, 힙[gögn_ARRAY + 2 + 2 * Loop_INDEX])) { 찾은여부 = Loop_INDEX; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[gögn_ARRAY + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(hlutur_tilvísun, (færsla_COUNT + 1) * 2); gögn_ARRAY = 힙[hlutur_tilvísun + 2]; 찾은여부 = færsla_COUNT; if (!Villa) 힙[hlutur_tilvísun + 3] = færsla_COUNT + 1; }
                if (!Villa) { 힙[gögn_ARRAY + 2 + 2 * 찾은여부] = Lykill_tilvísun; 힙[gögn_ARRAY + 3 + 2 * 찾은여부] = gögn_VALUE; }
            }
            if (fjarlægja && 찾은여부 >= 0) { for (int Loop_INDEX = 찾은여부 + 1; Loop_INDEX < færsla_COUNT; Loop_INDEX++) { 힙[gögn_ARRAY + 2 * Loop_INDEX] = 힙[gögn_ARRAY + 2 + 2 * Loop_INDEX]; 힙[gögn_ARRAY + 1 + 2 * Loop_INDEX] = 힙[gögn_ARRAY + 3 + 2 * Loop_INDEX]; } 힙[gögn_ARRAY + 2 * færsla_COUNT] = 0; 힙[gögn_ARRAY + 1 + 2 * færsla_COUNT] = 0; 힙[hlutur_tilvísun + 3] = færsla_COUNT - 1; }
            if (Word_SMS(heiti_fasti, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        bilun_VALUE("unsupported collection method");
    }
    static boolean 잠금얻기(int hlutur_tilvísun) {
        if (!객체유효(hlutur_tilvísun)) return false;
        if (잠금깊이[hlutur_tilvísun] != 0 && Loka_eigandi[hlutur_tilvísun] != 현재가닥 + 1) { 바꿈요청 = true; return false; }
        Loka_eigandi[hlutur_tilvísun] = 현재가닥 + 1; 잠금깊이[hlutur_tilvísun]++; return true;
    }
    static void losa_Loka(int hlutur_tilvísun) {
        if (!객체유효(hlutur_tilvísun)) return;
        if (잠금깊이[hlutur_tilvísun] == 0 || Loka_eigandi[hlutur_tilvísun] != 현재가닥 + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[hlutur_tilvísun] == 0) Loka_eigandi[hlutur_tilvísun] = 0;
    }
    static boolean SWITCH_þráður() {
        þráður_ramma[현재가닥] = ramma_INDEX;
        if (ramma_INDEX < 현재가닥 * 32) þráður_staða[현재가닥] = 3;
        for (int Loop_INDEX = 0; Loop_INDEX < þráður_COUNT; Loop_INDEX++) if (þráður_staða[Loop_INDEX] == 2 && þráður_staða[가닥대기[Loop_INDEX]] == 3) þráður_staða[Loop_INDEX] = 1;
        for (int Loop_INDEX = 1; Loop_INDEX <= þráður_COUNT; Loop_INDEX++) {
            int Áfram_staða = (현재가닥 + Loop_INDEX) % þráður_COUNT;
            if (þráður_staða[Áfram_staða] == 1) { 현재가닥 = Áfram_staða; ramma_INDEX = þráður_ramma[Áfram_staða]; 바꿈요청 = false; return true; }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < þráður_COUNT; Loop_INDEX++) if (þráður_staða[Loop_INDEX] != 3) { bilun_VALUE("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int heiti_fasti, int 서술상수, int skipun_CODE) { Ferli_þráður(heiti_fasti, 서술상수, skipun_CODE, false); }
    static void Ferli_þráður(int heiti_fasti, int 서술상수, int skipun_CODE, boolean Íslenska) {
        if (skipun_CODE == 184 && Word_SMS(heiti_fasti, Íslenska ? "YIELD_verk" : "yield") && Word_SMS(서술상수, "()V")) { 바꿈요청 = true; return; }
        if (skipun_CODE == 184 && Word_SMS(heiti_fasti, "currentThread") && Word_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(þráður_hlutur[현재가닥], 2); return; }
        if (skipun_CODE == 183 && Word_SMS(heiti_fasti, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, Íslenska ? "(LÍslenska/eigin/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int markmið_slóð = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), hlutur_tilvísun = 빼기(2);
            if (!객체유효(hlutur_tilvísun)) return;
            if (힙[hlutur_tilvísun] == 13) { 힙[hlutur_tilvísun + 2] = markmið_slóð; 힙참조[hlutur_tilvísun + 2] = 1; }
            else if (markmið_slóð != 0) bilun_VALUE("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (skipun_CODE == 182 && (Word_SMS(heiti_fasti, Íslenska ? "Opna_verk" : "start") || Word_SMS(heiti_fasti, Íslenska ? "기다리기" : "join")) && Word_SMS(서술상수, "()V") || skipun_CODE == 182 && Word_SMS(heiti_fasti, Íslenska ? "살아있는가" : "isAlive") && Word_SMS(서술상수, "()Z")) {
            int hlutur_tilvísun = 빼기(2); if (!객체유효(hlutur_tilvísun)) return;
            int Auðkenni_VALUE = -1; for (int Loop_INDEX = 0; Loop_INDEX < þráður_COUNT; Loop_INDEX++) if (þráður_hlutur[Loop_INDEX] == hlutur_tilvísun) Auðkenni_VALUE = Loop_INDEX;
            if (Word_SMS(heiti_fasti, Íslenska ? "살아있는가" : "isAlive")) { 넣기(Auðkenni_VALUE >= 0 && þráður_staða[Auðkenni_VALUE] != 3 ? 1 : 0, 1); return; }
            if (Word_SMS(heiti_fasti, Íslenska ? "기다리기" : "join")) { if (Auðkenni_VALUE >= 0 && þráður_staða[Auðkenni_VALUE] != 3) { 가닥대기[현재가닥] = Auðkenni_VALUE; þráður_staða[현재가닥] = 2; 바꿈요청 = true; } return; }
            if (Auðkenni_VALUE >= 0) { 예외던짐(Íslenska ? 38 : 16, "thread already started"); return; }
            if (þráður_COUNT == 4) { bilun_VALUE("thread limit (4 including main)"); return; }
            int markmið_slóð = 힙[hlutur_tilvísun] == 13 ? 힙[hlutur_tilvísun + 2] : hlutur_tilvísun;
            int skrá_INDEX = markmið_slóð > 0 && 힙[markmið_slóð] >= 32 ? heiti_aðferð(힙[markmið_slóð] - 32, Íslenska ? "Keyra" : "run", "()V") : -1;
            if (markmið_slóð != 0 && skrá_INDEX < 0) { bilun_VALUE("Runnable.run required"); return; }
            Auðkenni_VALUE = þráður_COUNT++; þráður_hlutur[Auðkenni_VALUE] = hlutur_tilvísun; þráður_markmið[Auðkenni_VALUE] = markmið_slóð;
            int ramma = Auðkenni_VALUE * 32; þráður_ramma[Auðkenni_VALUE] = skrá_INDEX < 0 ? ramma - 1 : ramma; þráður_staða[Auðkenni_VALUE] = skrá_INDEX < 0 ? 3 : 1;
            if (skrá_INDEX >= 0) { ramma_aðferð[ramma] = skrá_INDEX; ramma_staða[ramma] = aðferð_Opna[skrá_INDEX]; staðbundið_VALUE[ramma * 128] = markmið_slóð; staðbundið_TYPE[ramma * 128] = 2; }
            return;
        }
        bilun_VALUE("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], slóð_SMS = new int[16];
    static int staðbundið_slóð() { return slóð_hlutur(0x7f000001); }
    static int slóð_hlutur(int VALUE) { int hlutur_tilvísun = úthluta_geymsla(14, 1); if (!Villa) 힙[hlutur_tilvísun + 2] = VALUE; return hlutur_tilvísun; }
    static int 주소해독(int hlutur_tilvísun) {
        if (hlutur_tilvísun == 0 || 글같음(hlutur_tilvísun, hýsa_stafur("localhost"), false)) return 0x7f000001;
        if (!hlutur_VALUE(hlutur_tilvísun, 1)) return 0;
        int gögn_VALUE = 0, samtala_COUNT = 0, slóð_bæti_63221787 = 0, 자릿수 = 0, færsla_COUNT = 힙[hlutur_tilvísun + 1];
        for (int Loop_INDEX = 0; Loop_INDEX <= færsla_COUNT; Loop_INDEX++) {
            int stafkóði = Loop_INDEX == færsla_COUNT ? '.' : 힙[hlutur_tilvísun + 2 + Loop_INDEX];
            if (stafkóði == '.') { if (자릿수 == 0 || samtala_COUNT == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } gögn_VALUE = gögn_VALUE << 8 | slóð_bæti_63221787; samtala_COUNT++; slóð_bæti_63221787 = 자릿수 = 0; }
            else { if (stafkóði < '0' || stafkóði > '9' || ++자릿수 > 3 || (slóð_bæti_63221787 = slóð_bæti_63221787 * 10 + stafkóði - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (samtala_COUNT != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return gögn_VALUE;
    }
    static int slóð_stafur(int gögn_VALUE) {
        int færsla_COUNT = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int slóð_bæti_63221787 = gögn_VALUE >>> 이동비트 & 255;
            if (slóð_bæti_63221787 >= 100) slóð_SMS[færsla_COUNT++] = '0' + slóð_bæti_63221787 / 100;
            if (slóð_bæti_63221787 >= 10) slóð_SMS[færsla_COUNT++] = '0' + slóð_bæti_63221787 / 10 % 10;
            slóð_SMS[færsla_COUNT++] = '0' + slóð_bæti_63221787 % 10; if (이동비트 != 0) slóð_SMS[færsla_COUNT++] = '.';
        }
        int hlutur_tilvísun = úthluta_geymsla(1, færsla_COUNT); if (!Villa) for (int Loop_INDEX = 0; Loop_INDEX < færsla_COUNT; Loop_INDEX++) 힙[hlutur_tilvísun + 2 + Loop_INDEX] = slóð_SMS[Loop_INDEX]; return hlutur_tilvísun;
    }
    static void 통신호출(int eigandi, int heiti_fasti, int 서술상수, int skipun_CODE) {
        if (Word_SMS(eigandi, "java/net/InetAddress")) {
            if (skipun_CODE == 184 && Word_SMS(heiti_fasti, "getLoopbackAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(staðbundið_slóð(), 2); return; }
            if (skipun_CODE == 184 && Word_SMS(heiti_fasti, "getByName") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int gögn_VALUE = 주소해독(빼기(2)); if (던진객체 == 0 && !Villa) 넣기(slóð_hlutur(gögn_VALUE), 2); return;
            }
            if (skipun_CODE == 182 && Word_SMS(heiti_fasti, "getHostAddress") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int hlutur_tilvísun = 빼기(2); if (hlutur_VALUE(hlutur_tilvísun, 14)) 넣기(slóð_stafur(힙[hlutur_tilvísun + 2]), 2); return; }
        }
        if (Word_SMS(eigandi, "java/net/DatagramPacket")) {
            if (skipun_CODE == 183 && Word_SMS(heiti_fasti, "<init>") && (Word_SMS(서술상수, "([BI)V") || Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean endastaður_VALUE_tilvísun = Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int tengisnúmer = endastaður_VALUE_tilvísun ? 빼기(1) : 0, slóð_tilvísun = endastaður_VALUE_tilvísun ? 빼기(2) : 0;
                int færsla_COUNT = 빼기(1), gögn_ARRAY = 빼기(2), hlutur_tilvísun = 빼기(2);
                if (!hlutur_VALUE(hlutur_tilvísun, 16) || !hlutur_VALUE(gögn_ARRAY, 20)) return;
                if (færsla_COUNT < 0 || færsla_COUNT > 힙[gögn_ARRAY + 1] || tengisnúmer < 0 || tengisnúmer > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (slóð_tilvísun != 0 && !hlutur_VALUE(slóð_tilvísun, 14)) return;
                힙[hlutur_tilvísun + 2] = gögn_ARRAY; 힙참조[hlutur_tilvísun + 2] = 1; 힙[hlutur_tilvísun + 3] = færsla_COUNT;
                힙[hlutur_tilvísun + 4] = slóð_tilvísun; 힙참조[hlutur_tilvísun + 4] = 1; 힙[hlutur_tilvísun + 5] = tengisnúmer; return;
            }
            if (skipun_CODE == 182 && Word_SMS(heiti_fasti, "setLength") && Word_SMS(서술상수, "(I)V")) {
                int færsla_COUNT = 빼기(1), hlutur_tilvísun = 빼기(2); if (!hlutur_VALUE(hlutur_tilvísun, 16)) return;
                if (færsla_COUNT < 0 || færsla_COUNT > 힙[힙[hlutur_tilvísun + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[hlutur_tilvísun + 3] = færsla_COUNT; return;
            }
            if (skipun_CODE == 182 && (Word_SMS(heiti_fasti, "getData") && Word_SMS(서술상수, "()[B") || Word_SMS(heiti_fasti, "getLength") && Word_SMS(서술상수, "()I") || Word_SMS(heiti_fasti, "getAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;") || Word_SMS(heiti_fasti, "getPort") && Word_SMS(서술상수, "()I"))) {
                int hlutur_tilvísun = 빼기(2); if (!hlutur_VALUE(hlutur_tilvísun, 16)) return;
                int færsla_staða = Word_SMS(heiti_fasti, "getData") ? 2 : Word_SMS(heiti_fasti, "getLength") ? 3 : Word_SMS(heiti_fasti, "getAddress") ? 4 : 5;
                넣기(힙[hlutur_tilvísun + færsla_staða], færsla_staða == 2 || færsla_staða == 4 ? 2 : 1); return;
            }
        }
        if (Word_SMS(eigandi, "java/net/DatagramSocket")) {
            if (skipun_CODE == 183 && Word_SMS(heiti_fasti, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(I)V"))) {
                int tengisnúmer = Word_SMS(서술상수, "()V") ? 0 : 빼기(1), hlutur_tilvísun = 빼기(2); if (!hlutur_VALUE(hlutur_tilvísun, 15)) return;
                if (tengisnúmer < 0 || tengisnúmer > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = notandi.opið_Net(tengisnúmer); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[hlutur_tilvísun + 2] = 열린파일번호; return;
            }
            if (skipun_CODE == 182 && Word_SMS(heiti_fasti, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), hlutur_tilvísun = 빼기(2); if (!hlutur_VALUE(hlutur_tilvísun, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[hlutur_tilvísun + 3] = 밀리초값; return;
            }
            if (skipun_CODE == 182 && Word_SMS(heiti_fasti, "getLocalPort") && Word_SMS(서술상수, "()I")) { int hlutur_tilvísun = 빼기(2); if (hlutur_VALUE(hlutur_tilvísun, 15)) 넣기(힙[hlutur_tilvísun + 2] < 0 ? -1 : notandi.Net_gátt(힙[hlutur_tilvísun + 2]), 1); return; }
            if (skipun_CODE == 182 && Word_SMS(heiti_fasti, "isClosed") && Word_SMS(서술상수, "()Z")) { int hlutur_tilvísun = 빼기(2); if (hlutur_VALUE(hlutur_tilvísun, 15)) 넣기(힙[hlutur_tilvísun + 2] < 0 ? 1 : 0, 1); return; }
            if (skipun_CODE == 182 && Word_SMS(heiti_fasti, "close") && Word_SMS(서술상수, "()V")) { int hlutur_tilvísun = 빼기(2); if (hlutur_VALUE(hlutur_tilvísun, 15) && 힙[hlutur_tilvísun + 2] >= 0) { notandi.파일서술자닫기(힙[hlutur_tilvísun + 2]); 힙[hlutur_tilvísun + 2] = -1; } return; }
            if (skipun_CODE == 182 && (Word_SMS(heiti_fasti, "send") || Word_SMS(heiti_fasti, "receive")) && Word_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int pakki = 빼기(2), hlutur_tilvísun = 빼기(2); if (!hlutur_VALUE(pakki, 16) || !hlutur_VALUE(hlutur_tilvísun, 15)) return;
                int gögn_ARRAY = 힙[pakki + 2], 유효길이 = 힙[pakki + 3], 열린파일번호 = 힙[hlutur_tilvísun + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_SMS(heiti_fasti, "send")) {
                    if (!hlutur_VALUE(힙[pakki + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < 유효길이; Loop_INDEX++) 통신임시[Loop_INDEX] = 힙[gögn_ARRAY + 2 + Loop_INDEX];
                    if (notandi.senda_Net(열린파일번호, 힙[힙[pakki + 4] + 2], 힙[pakki + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int færsla_COUNT = notandi.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (færsla_COUNT == -11) {
                        int 현재시각 = notandi.밀리초();
                        if (힙[hlutur_tilvísun + 4] == 0) 힙[hlutur_tilvísun + 4] = 현재시각 + 1;
                        if (힙[hlutur_tilvísun + 3] > 0 && 현재시각 - (힙[hlutur_tilvísun + 4] - 1) >= 힙[hlutur_tilvísun + 3]) { 힙[hlutur_tilvísun + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(hlutur_tilvísun, 2); 넣기(pakki, 2); ramma_staða[ramma_INDEX] = ramma_skipun[ramma_INDEX]; 바꿈요청 = true; return;
                    }
                    힙[hlutur_tilvísun + 4] = 0;
                    if (færsla_COUNT < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < færsla_COUNT; Loop_INDEX++) 힙[gögn_ARRAY + 2 + Loop_INDEX] = (byte)통신임시[Loop_INDEX];
                    힙[pakki + 3] = færsla_COUNT; 힙[pakki + 4] = slóð_hlutur(통신임시[513]); 힙참조[pakki + 4] = 1; 힙[pakki + 5] = 통신임시[512];
                }
                return;
            }
        }
        bilun_VALUE("unsupported java.net method");
    }
    static boolean 흐름대기(int hlutur_tilvísun) {
        int 현재시각 = notandi.밀리초();
        if (힙[hlutur_tilvísun + 5] == 0) 힙[hlutur_tilvísun + 5] = 현재시각 + 1;
        if (힙[hlutur_tilvísun + 3] > 0 && 현재시각 - (힙[hlutur_tilvísun + 5] - 1) >= 힙[hlutur_tilvísun + 3]) { 힙[hlutur_tilvísun + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        ramma_staða[ramma_INDEX] = ramma_skipun[ramma_INDEX]; 바꿈요청 = true; return true;
    }
    static void 흐름호출(int eigandi, int heiti_fasti, int 서술상수, int skipun_CODE) {
        boolean 수신쪽 = Word_SMS(eigandi, "java/net/ServerSocket"), Stream = Word_SMS(eigandi, "java/io/InputStream") || Word_SMS(eigandi, "java/io/OutputStream");
        if (!Stream && skipun_CODE == 183 && Word_SMS(heiti_fasti, "<init>")) {
            boolean upplýsingatækni_autt_staða = Word_SMS(서술상수, "()V"), 이름지정여부 = Word_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(upplýsingatækni_autt_staða || 수신쪽 && Word_SMS(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { bilun_VALUE("unsupported socket constructor"); return; }
            int tengisnúmer = upplýsingatækni_autt_staða ? 0 : 빼기(1), slóð_tilvísun = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, hlutur_tilvísun = 빼기(2);
            if (!hlutur_VALUE(hlutur_tilvísun, 수신쪽 ? 18 : 17)) return;
            if (tengisnúmer < 0 || tengisnúmer > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !hlutur_VALUE(slóð_tilvísun, 14)) return;
            int Net_slóð = 이름지정여부 ? 주소해독(slóð_tilvísun) : 주소지정여부 ? 힙[slóð_tilvísun + 2] : 0x7f000001;
            if (Villa || 던진객체 != 0) return;
            int 열린파일번호 = notandi.Stream_stýring(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = upplýsingatækni_autt_staða ? 0 : 수신쪽 ? notandi.Stream_stýring(1, 열린파일번호, tengisnúmer) : notandi.TENGJA_Stream(열린파일번호, Net_slóð, tengisnúmer);
            if (처리값 < 0) { notandi.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[hlutur_tilvísun + 2] = 열린파일번호; 힙[hlutur_tilvísun + 4] = tengisnúmer; 힙[hlutur_tilvísun + 6] = upplýsingatækni_autt_staða ? 0 : 1; return;
        }
        if (!Stream && Word_SMS(heiti_fasti, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), hlutur_tilvísun = 빼기(2); if (!hlutur_VALUE(hlutur_tilvísun, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[hlutur_tilvísun + 3] = 밀리초값; return; }
        if (!Stream && Word_SMS(heiti_fasti, "close") && Word_SMS(서술상수, "()V")) { int hlutur_tilvísun = 빼기(2); if (hlutur_VALUE(hlutur_tilvísun, 수신쪽 ? 18 : 17) && 힙[hlutur_tilvísun + 2] >= 0) { notandi.파일서술자닫기(힙[hlutur_tilvísun + 2]); 힙[hlutur_tilvísun + 2] = -1; } return; }
        if (!Stream && (Word_SMS(heiti_fasti, "getLocalPort") || Word_SMS(heiti_fasti, "getPort") || Word_SMS(heiti_fasti, "isClosed") || Word_SMS(heiti_fasti, "isConnected"))) {
            int hlutur_tilvísun = 빼기(2); if (!hlutur_VALUE(hlutur_tilvísun, 수신쪽 ? 18 : 17)) return;
            넣기(Word_SMS(heiti_fasti, "isClosed") ? 힙[hlutur_tilvísun + 2] < 0 ? 1 : 0 : Word_SMS(heiti_fasti, "isConnected") ? 힙[hlutur_tilvísun + 6] : Word_SMS(heiti_fasti, "getPort") ? 힙[hlutur_tilvísun + 4] : 힙[hlutur_tilvísun + 2] < 0 ? -1 : notandi.Stream_stýring(4, 힙[hlutur_tilvísun + 2], 0), 1); return;
        }
        if (수신쪽 && Word_SMS(heiti_fasti, "accept") && Word_SMS(서술상수, "()Ljava/net/Socket;")) {
            int hlutur_tilvísun = 빼기(2); if (!hlutur_VALUE(hlutur_tilvísun, 18)) return; int 열린파일번호 = notandi.Stream_stýring(3, 힙[hlutur_tilvísun + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(hlutur_tilvísun)) 넣기(hlutur_tilvísun, 2); return; }
            힙[hlutur_tilvísun + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = úthluta_geymsla(17, 5); if (Villa) { notandi.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = notandi.Stream_stýring(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !Stream && ((Word_SMS(heiti_fasti, "getInputStream") && Word_SMS(서술상수, "()Ljava/io/InputStream;")) || (Word_SMS(heiti_fasti, "getOutputStream") && Word_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int hlutur_tilvísun = 빼기(2); if (!hlutur_VALUE(hlutur_tilvísun, 17)) return; if (힙[hlutur_tilvísun + 2] < 0 || 힙[hlutur_tilvísun + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = úthluta_geymsla(19, 4); if (Villa) return; 힙[반환값 + 2] = hlutur_tilvísun; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Word_SMS(heiti_fasti, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (Stream) {
            boolean 읽기여부 = Word_SMS(heiti_fasti, "read"), upplýsingatækni_skrifa_aðgerð = Word_SMS(heiti_fasti, "write"), útiloka = Word_SMS(서술상수, "([B)I") || Word_SMS(서술상수, "([B)V"), upplýsingatækni_SUBARRAY = Word_SMS(서술상수, "([BII)I") || Word_SMS(서술상수, "([BII)V");
            int færsla_COUNT = upplýsingatækni_SUBARRAY ? 빼기(1) : 0, 시작변위 = upplýsingatækni_SUBARRAY ? 빼기(1) : 0, gögn_ARRAY = útiloka || upplýsingatækni_SUBARRAY ? 빼기(2) : 0;
            int gögn_VALUE = upplýsingatækni_skrifa_aðgerð && Word_SMS(서술상수, "(I)V") ? 빼기(1) : 0, hlutur_tilvísun = 빼기(2);
            if (!hlutur_VALUE(hlutur_tilvísun, 19)) return; int yfireining_tilvísun = 힙[hlutur_tilvísun + 2], 열린파일번호 = 힙[yfireining_tilvísun + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_SMS(heiti_fasti, "close") && Word_SMS(서술상수, "()V")) { notandi.파일서술자닫기(열린파일번호); 힙[yfireining_tilvísun + 2] = -1; return; }
            if (Word_SMS(heiti_fasti, "flush") && Word_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !upplýsingatækni_skrifa_aðgerð) || 읽기여부 != (힙[hlutur_tilvísun + 3] == 0)) { bilun_VALUE("unsupported stream operation"); return; }
            if (útiloka || upplýsingatækni_SUBARRAY) { if (!hlutur_VALUE(gögn_ARRAY, 20)) return; if (útiloka) færsla_COUNT = 힙[gögn_ARRAY + 1]; if (시작변위 < 0 || færsla_COUNT < 0 || 시작변위 > 힙[gögn_ARRAY + 1] - færsla_COUNT) { 예외던짐(6, "stream array bounds"); return; } }
            else færsla_COUNT = 1;
            if (færsla_COUNT == 0) { if (읽기여부) 넣기(0, 1); return; }
            int lokið_COUNT = upplýsingatækni_skrifa_aðgerð ? 힙[hlutur_tilvísun + 4] : 0, 처리값 = 0;
            while (lokið_COUNT < færsla_COUNT) {
                처리값 = 읽기여부 ? notandi.파일한바이트읽기(열린파일번호) : notandi.파일한바이트쓰기(열린파일번호, útiloka || upplýsingatækni_SUBARRAY ? 힙[gögn_ARRAY + 2 + 시작변위 + lokið_COUNT] : gögn_VALUE);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (útiloka || upplýsingatækni_SUBARRAY)) 힙[gögn_ARRAY + 2 + 시작변위 + lokið_COUNT] = (byte)처리값;
                lokið_COUNT++; if (읽기여부 && !(útiloka || upplýsingatækni_SUBARRAY)) break;
            }
            if (처리값 == -11 && (upplýsingatækni_skrifa_aðgerð || lokið_COUNT == 0)) {
                힙[hlutur_tilvísun + 4] = lokið_COUNT;
                if (흐름대기(yfireining_tilvísun)) { 넣기(hlutur_tilvísun, 2); if (útiloka || upplýsingatækni_SUBARRAY) 넣기(gögn_ARRAY, 2); if (upplýsingatækni_SUBARRAY) { 넣기(시작변위, 1); 넣기(færsla_COUNT, 1); } if (upplýsingatækni_skrifa_aðgerð && !(útiloka || upplýsingatækni_SUBARRAY)) 넣기(gögn_VALUE, 1); } return;
            }
            힙[hlutur_tilvísun + 4] = 0; 힙[yfireining_tilvísun + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(lokið_COUNT == 0 && 처리값 == 256 ? -1 : útiloka || upplýsingatækni_SUBARRAY ? lokið_COUNT : 처리값, 1); return;
        }
        bilun_VALUE("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int heiti_fasti) {
        if (Word_SMS(heiti_fasti, "Íslenska/eigin/Gluggi")) return 24;
        if (Word_SMS(heiti_fasti, "Íslenska/eigin/Skýring")) return 26;
        if (Word_SMS(heiti_fasti, "Íslenska/eigin/hnappur")) return 27;
        if (Word_SMS(heiti_fasti, "Íslenska/eigin/SMS_reitur")) return 28;
        if (Word_SMS(heiti_fasti, "Íslenska/eigin/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int heiti_fasti) {
        return 한국어화면종(heiti_fasti) != 0 || Word_SMS(heiti_fasti, "Íslenska/eigin/화면구성요소") || Word_SMS(heiti_fasti, "Íslenska/eigin/atvik_biðröð");
    }
    static int 화면종(int heiti_fasti) {
        int 한국어종 = 한국어화면종(heiti_fasti); if (한국어종 != 0) return 한국어종;
        if (Word_SMS(heiti_fasti, "javax/swing/JFrame")) return 24;
        if (Word_SMS(heiti_fasti, "javax/swing/JPanel")) return 25;
        if (Word_SMS(heiti_fasti, "javax/swing/JLabel")) return 26;
        if (Word_SMS(heiti_fasti, "javax/swing/JButton")) return 27;
        if (Word_SMS(heiti_fasti, "javax/swing/JTextField")) return 28;
        if (Word_SMS(heiti_fasti, "java/awt/event/ActionEvent")) return 29;
        if (Word_SMS(heiti_fasti, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int heiti_fasti) {
        return 화면종(heiti_fasti) != 0 || Word_SMS(heiti_fasti, "java/awt/Component") || Word_SMS(heiti_fasti, "java/awt/Container") || Word_SMS(heiti_fasti, "javax/swing/JComponent") || Word_SMS(heiti_fasti, "javax/swing/AbstractButton") || Word_SMS(heiti_fasti, "javax/swing/text/JTextComponent") || Word_SMS(heiti_fasti, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int hlutur_tilvísun) { if (!객체유효(hlutur_tilvísun)) return false; if (힙[hlutur_tilvísun] < 24 || 힙[hlutur_tilvísun] > 28) { bilun_VALUE("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int hlutur_tilvísun, int SMS_tilvísun) {
        if (SMS_tilvísun != 0 && !hlutur_VALUE(SMS_tilvísun, 1)) return;
        int færsla_COUNT = SMS_tilvísun == 0 ? 0 : 힙[SMS_tilvísun + 1]; if (færsla_COUNT > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < færsla_COUNT; Loop_INDEX++) 화면글임시[Loop_INDEX] = 힙[SMS_tilvísun + 2 + Loop_INDEX];
        if (notandi.화면글(힙[hlutur_tilvísun + 2], 화면글임시, færsla_COUNT) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[hlutur_tilvísun + 3] = SMS_tilvísun; 힙참조[hlutur_tilvísun + 3] = 1;
    }
    static int 화면문자읽기(int hlutur_tilvísun) {
        int Auðkenni_VALUE = 힙[hlutur_tilvísun + 2], færsla_COUNT = notandi.화면연결(8, Auðkenni_VALUE, 0, 0, 0, 0), 사용수 = 0;
        if (færsla_COUNT < 0) { bilun_VALUE("GUI text read failed"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < færsla_COUNT; Loop_INDEX++) { int 부호값 = notandi.화면연결(9, Auðkenni_VALUE, Loop_INDEX, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = úthluta_geymsla(1, 사용수); if (!Villa) for (int Loop_INDEX = 0; Loop_INDEX < 사용수; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 화면글임시[Loop_INDEX]; return 반환값;
    }
    /* Íslenska 객체를 직접 만들고 kjarni_VALUE 화면 기능에 연결한다. Swing hlutur_VALUE/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int eigandi, int heiti_fasti, int 서술상수, int skipun_CODE) {
        if (Word_SMS(eigandi, "Íslenska/eigin/atvik_biðröð")) {
            if (skipun_CODE == 184 && Word_SMS(heiti_fasti, "나중에실행") && Word_SMS(서술상수, "(LÍslenska/eigin/실행할일;)V")) {
                int verk_aðgerð = 빼기(2); if (!객체유효(verk_aðgerð)) return;
                if (나중수 == 8) { bilun_VALUE("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = verk_aðgerð; return;
            }
            if (skipun_CODE == 184 && Word_SMS(heiti_fasti, "사건처리중인가") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            bilun_VALUE("지원하지 않는 Íslenska 화면 일정 호출"); return;
        }
        if (Word_SMS(eigandi, "Íslenska/eigin/동작알림")) {
            int 알림 = 빼기(2); if (!hlutur_VALUE(알림, 29) || 힙[알림 + 3] == 0) return;
            if (Word_SMS(heiti_fasti, "atvik_uppruni") && Word_SMS(서술상수, "()LÍslenska/eigin/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (Word_SMS(heiti_fasti, "skipun_SMS") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (Word_SMS(heiti_fasti, "INDEX") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else bilun_VALUE("지원하지 않는 Íslenska Aðgerð 알림 호출"); return;
        }
        if (skipun_CODE == 183 && Word_SMS(heiti_fasti, "<init>")) {
            int 종류 = 한국어화면종(eigandi), 받이 = 0, 가로 = 0, Lóðrétt_staða = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Word_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (notandi.화면너비() - 폭) / 2; Lóðrétt_staða = (notandi.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Word_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Word_SMS(서술상수, "(Ljava/lang/String;IIIILÍslenska/eigin/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); Lóðrétt_staða = 빼기(1); 가로 = 빼기(1);
            } else { bilun_VALUE("지원하지 않는 Íslenska 화면 생성자"); return; }
            int Texti = 빼기(2), eining_VALUE = 빼기(2); if (!화면객체(eining_VALUE)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || Lóðrétt_staða < 0 || 폭 > notandi.화면너비() - 가로 || 높이 > notandi.화면높이() - Lóðrétt_staða) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDEX = notandi.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (INDEX < 1 || INDEX > 32) { bilun_VALUE("화면 eining_VALUE 자리가 가득 찼습니다"); return; }
            힙[eining_VALUE + 2] = INDEX; 화면참조[INDEX - 1] = eining_VALUE;
            힙[eining_VALUE + 5] = 가로; 힙[eining_VALUE + 6] = Lóðrétt_staða; 힙[eining_VALUE + 7] = 폭; 힙[eining_VALUE + 8] = 높이; 힙[eining_VALUE + 10] = 2;
            힙[eining_VALUE + 4] = 받이; 힙참조[eining_VALUE + 4] = 1; 힙[eining_VALUE + 12] = 1;
            notandi.화면연결(1, INDEX, 가로, Lóðrétt_staða, 폭, 높이);
            if (종류 == 24) notandi.화면연결(7, INDEX, 2, 0, 0, 0);
            화면문자설정(eining_VALUE, Texti); return;
        }
        if (skipun_CODE != 182) { bilun_VALUE("잘못된 Íslenska 화면 호출 Skipun"); return; }
        if (Word_SMS(heiti_fasti, "skrifa_SMS") && Word_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int Texti = 빼기(2), eining_VALUE = 빼기(2); if (화면객체(eining_VALUE)) 화면문자설정(eining_VALUE, Texti); return;
        }
        if (Word_SMS(heiti_fasti, "글읽기") && Word_SMS(서술상수, "()Ljava/lang/String;")) {
            int eining_VALUE = 빼기(2); if (화면객체(eining_VALUE)) 넣기(화면문자읽기(eining_VALUE), 2); return;
        }
        if (Word_SMS(heiti_fasti, "동작맡기기") && Word_SMS(서술상수, "(LÍslenska/eigin/동작받이;)V")) {
            int 받이 = 빼기(2), eining_VALUE = 빼기(2);
            if (화면객체(eining_VALUE)) { 힙[eining_VALUE + 4] = 받이; 힙참조[eining_VALUE + 4] = 1; 힙[eining_VALUE + 12] = 1; } return;
        }
        if (Word_SMS(heiti_fasti, "bæta_við_eining") && Word_SMS(서술상수, "(LÍslenska/eigin/화면구성요소;)V")) {
            int barn_VALUE = 빼기(2), yfireining_VALUE = 빼기(2); if (!화면객체(barn_VALUE) || !화면객체(yfireining_VALUE)) return;
            if (notandi.화면연결(2, 힙[yfireining_VALUE + 2], 힙[barn_VALUE + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[barn_VALUE + 11] = yfireining_VALUE; 힙참조[barn_VALUE + 11] = 1; return;
        }
        if (Word_SMS(heiti_fasti, "자리정하기") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), Lóðrétt_staða = 빼기(1), 가로 = 빼기(1), eining_VALUE = 빼기(2); if (!화면객체(eining_VALUE)) return;
            if (notandi.화면연결(1, 힙[eining_VALUE + 2], 가로, Lóðrétt_staða, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[eining_VALUE + 5] = 가로; 힙[eining_VALUE + 6] = Lóðrétt_staða; 힙[eining_VALUE + 7] = 폭; 힙[eining_VALUE + 8] = 높이; return;
        }
        if ((Word_SMS(heiti_fasti, "sýna_gluggi") || Word_SMS(heiti_fasti, "Loka")) && Word_SMS(서술상수, "()V")) {
            boolean sýnileiki_VALUE = Word_SMS(heiti_fasti, "sýna_gluggi"); int eining_VALUE = 빼기(2); if (!화면객체(eining_VALUE)) return;
            if (notandi.화면연결(sýnileiki_VALUE ? 3 : 4, 힙[eining_VALUE + 2], sýnileiki_VALUE ? 1 : 0, 0, 0, 0) < 0) { bilun_VALUE("화면은 gagnvirkur 명령에서 실행해야 합니다"); return; }
            힙[eining_VALUE + 9] = sýnileiki_VALUE ? 1 : 0; return;
        }
        if (Word_SMS(heiti_fasti, "보이는가") && Word_SMS(서술상수, "()Z")) { int eining_VALUE = 빼기(2); if (화면객체(eining_VALUE)) 넣기(힙[eining_VALUE + 9], 1); return; }
        bilun_VALUE("지원하지 않는 Íslenska 화면 aðferð_VALUE");
    }
    static void 화면호출(int eigandi, int heiti_fasti, int 서술상수, int skipun_CODE) {
        if (Word_SMS(eigandi, "javax/swing/SwingUtilities")) {
            if (skipun_CODE == 184 && Word_SMS(heiti_fasti, "invokeLater") && Word_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int hlutur_tilvísun = 빼기(2); if (!객체유효(hlutur_tilvísun)) return; if (나중수 == 8) { bilun_VALUE("invokeLater queue full"); return; } 나중실행[나중수++] = hlutur_tilvísun; return; }
            if (skipun_CODE == 184 && Word_SMS(heiti_fasti, "isEventDispatchThread") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            bilun_VALUE("unsupported SwingUtilities method"); return;
        }
        if (Word_SMS(eigandi, "java/awt/event/ActionEvent")) {
            int hlutur_tilvísun = 빼기(2); if (!hlutur_VALUE(hlutur_tilvísun, 29)) return;
            if (Word_SMS(heiti_fasti, "getSource") && Word_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[hlutur_tilvísun + 2], 2);
            else if (Word_SMS(heiti_fasti, "getActionCommand") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[hlutur_tilvísun + 2]), 2);
            else if (Word_SMS(heiti_fasti, "getID") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else bilun_VALUE("unsupported ActionEvent method"); return;
        }
        if (skipun_CODE == 183 && Word_SMS(heiti_fasti, "<init>")) {
            int COLUMNS = 0, SMS_tilvísun = 0;
            if (Word_SMS(서술상수, "(I)V")) COLUMNS = 빼기(1);
            else if (Word_SMS(서술상수, "(Ljava/lang/String;I)V")) { COLUMNS = 빼기(1); SMS_tilvísun = 빼기(2); }
            else if (Word_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_tilvísun = 빼기(2);
            else if (Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_SMS(서술상수, "()V")) { bilun_VALUE("unsupported Swing constructor"); return; }
            int hlutur_tilvísun = 빼기(2); if (!객체유효(hlutur_tilvísun)) return;
            if (힙[hlutur_tilvísun] == 30) { bilun_VALUE("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(hlutur_tilvísun) || COLUMNS < 0) return;
            int Auðkenni_VALUE = notandi.화면연결(0, 힙[hlutur_tilvísun] - 23, 0, 0, 0, 0);
            if (Auðkenni_VALUE < 1 || Auðkenni_VALUE > 32) { bilun_VALUE("GUI widget slots exhausted"); return; }
            힙[hlutur_tilvísun + 2] = Auðkenni_VALUE; 화면참조[Auðkenni_VALUE - 1] = hlutur_tilvísun; 힙[hlutur_tilvísun + 5] = 힙[hlutur_tilvísun] == 24 ? 130 : 16; 힙[hlutur_tilvísun + 6] = 힙[hlutur_tilvísun] == 24 ? 110 : 16;
            힙[hlutur_tilvísun + 7] = 힙[hlutur_tilvísun] == 24 ? 380 : 220; 힙[hlutur_tilvísun + 8] = 힙[hlutur_tilvísun] == 24 ? 240 : 28; 힙[hlutur_tilvísun + 10] = 1;
            화면문자설정(hlutur_tilvísun, SMS_tilvísun); return;
        }
        if (Word_SMS(heiti_fasti, "setText") || Word_SMS(heiti_fasti, "setTitle")) { int SMS_tilvísun = 빼기(2), hlutur_tilvísun = 빼기(2); if (화면객체(hlutur_tilvísun) && Word_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(hlutur_tilvísun, SMS_tilvísun); return; }
        if (Word_SMS(heiti_fasti, "getText") || Word_SMS(heiti_fasti, "getTitle")) { int hlutur_tilvísun = 빼기(2); if (화면객체(hlutur_tilvísun) && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(hlutur_tilvísun), 2); return; }
        if (Word_SMS(heiti_fasti, "addActionListener") && Word_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), hlutur_tilvísun = 빼기(2); if (화면객체(hlutur_tilvísun)) { 힙[hlutur_tilvísun + 4] = 수신참조; 힙참조[hlutur_tilvísun + 4] = 1; } return; }
        if (Word_SMS(heiti_fasti, "getContentPane") && Word_SMS(서술상수, "()Ljava/awt/Container;")) { int hlutur_tilvísun = 빼기(2); if (화면객체(hlutur_tilvísun)) 넣기(hlutur_tilvísun, 2); return; }
        if (Word_SMS(heiti_fasti, "setLayout") && Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int útlit_tilvísun = 빼기(2), hlutur_tilvísun = 빼기(2); if (화면객체(hlutur_tilvísun) && útlit_tilvísun != 0) bilun_VALUE("only absolute layout (null) is supported"); return; }
        if (Word_SMS(heiti_fasti, "add") && (Word_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean útlit_skilyrði = Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (útlit_skilyrði) 빼기(2);
            int barn_tilvísun = 빼기(2), hlutur_tilvísun = 빼기(2); if (!화면객체(barn_tilvísun) || !화면객체(hlutur_tilvísun)) return;
            if (notandi.화면연결(2, 힙[hlutur_tilvísun + 2], 힙[barn_tilvísun + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[barn_tilvísun + 11] = hlutur_tilvísun; 힙참조[barn_tilvísun + 11] = 1; if (!útlit_skilyrði) 넣기(barn_tilvísun, 2); return;
        }
        if (Word_SMS(heiti_fasti, "setBounds") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), Y_hnit = 빼기(1), x_hnit = 빼기(1), hlutur_tilvísun = 빼기(2); if (!화면객체(hlutur_tilvísun)) return;
            if (notandi.화면연결(1, 힙[hlutur_tilvísun + 2], x_hnit, Y_hnit, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[hlutur_tilvísun + 5] = x_hnit; 힙[hlutur_tilvísun + 6] = Y_hnit; 힙[hlutur_tilvísun + 7] = 너비; 힙[hlutur_tilvísun + 8] = 높이; return;
        }
        if (Word_SMS(heiti_fasti, "setSize") && Word_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), hlutur_tilvísun = 빼기(2); if (!화면객체(hlutur_tilvísun)) return;
            if (notandi.화면연결(1, 힙[hlutur_tilvísun + 2], 힙[hlutur_tilvísun + 5], 힙[hlutur_tilvísun + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[hlutur_tilvísun + 7] = 너비; 힙[hlutur_tilvísun + 8] = 높이; } return;
        }
        if (Word_SMS(heiti_fasti, "setLocationRelativeTo") && Word_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), hlutur_tilvísun = 빼기(2); if (!화면객체(hlutur_tilvísun)) return; if (상대배치 != 0) { bilun_VALUE("only screen centering supported"); return; } 힙[hlutur_tilvísun + 5] = (notandi.화면너비() - 힙[hlutur_tilvísun + 7]) / 2; 힙[hlutur_tilvísun + 6] = (notandi.화면높이() - 힙[hlutur_tilvísun + 8]) / 2; notandi.화면연결(1, 힙[hlutur_tilvísun + 2], 힙[hlutur_tilvísun + 5], 힙[hlutur_tilvísun + 6], 힙[hlutur_tilvísun + 7], 힙[hlutur_tilvísun + 8]); return; }
        if (Word_SMS(heiti_fasti, "setDefaultCloseOperation") && Word_SMS(서술상수, "(I)V")) { int regla = 빼기(1), hlutur_tilvísun = 빼기(2); if (화면객체(hlutur_tilvísun)) { if (regla < 0 || regla > 3) 예외던짐(9, "close policy"); else { 힙[hlutur_tilvísun + 10] = regla; notandi.화면연결(7, 힙[hlutur_tilvísun + 2], regla, 0, 0, 0); } } return; }
        if (Word_SMS(heiti_fasti, "setVisible") && Word_SMS(서술상수, "(Z)V")) { int gögn_VALUE = 빼기(1), hlutur_tilvísun = 빼기(2); if (화면객체(hlutur_tilvísun)) { int 처리값 = notandi.화면연결(3, 힙[hlutur_tilvísun + 2], gögn_VALUE, 0, 0, 0); if (처리값 < 0) bilun_VALUE("Swing requires a standalone interactive command"); else 힙[hlutur_tilvísun + 9] = gögn_VALUE; } return; }
        if (Word_SMS(heiti_fasti, "dispose") && Word_SMS(서술상수, "()V")) { int hlutur_tilvísun = 빼기(2); if (화면객체(hlutur_tilvísun)) { notandi.화면연결(4, 힙[hlutur_tilvísun + 2], 0, 0, 0, 0); 힙[hlutur_tilvísun + 9] = 0; } return; }
        if (Word_SMS(heiti_fasti, "repaint") || Word_SMS(heiti_fasti, "validate")) { int hlutur_tilvísun = 빼기(2); if (!화면객체(hlutur_tilvísun) || !Word_SMS(서술상수, "()V")) return; notandi.화면연결(1, 힙[hlutur_tilvísun + 2], 힙[hlutur_tilvísun + 5], 힙[hlutur_tilvísun + 6], 힙[hlutur_tilvísun + 7], 힙[hlutur_tilvísun + 8]); return; }
        if (Word_SMS(heiti_fasti, "isVisible") && Word_SMS(서술상수, "()Z")) { int hlutur_tilvísun = 빼기(2); if (화면객체(hlutur_tilvísun)) 넣기(힙[hlutur_tilvísun + 9], 1); return; }
        bilun_VALUE("unsupported Swing method (native subset)");
    }
    static void senda_atvik(int markmið_slóð, int atvik_númer, boolean Íslenska) {
        if (markmið_slóð < 1 || 힙[markmið_slóð] < 32) { bilun_VALUE("Java event listener required"); return; }
        int skrá_INDEX = heiti_aðferð(힙[markmið_slóð] - 32, atvik_númer == 0 ? (Íslenska ? "Keyra" : "run") : (Íslenska ? "동작받기" : "actionPerformed"), atvik_númer == 0 ? "()V" : (Íslenska ? "(LÍslenska/eigin/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (skrá_INDEX < 0) { bilun_VALUE("event callback missing"); return; }
        현재가닥 = 0; þráður_COUNT = 1; ramma_INDEX = 0; þráður_staða[0] = 1; ramma_bunki[0] = 0; ramma_Loka[0] = frumstilla_ramma[0] = 0; 바꿈요청 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 128; Loop_INDEX++) { staðbundið_VALUE[Loop_INDEX] = staðbundið_TYPE[Loop_INDEX] = 0; }
        ramma_aðferð[0] = skrá_INDEX; ramma_staða[0] = aðferð_Opna[skrá_INDEX]; staðbundið_VALUE[0] = markmið_slóð; staðbundið_TYPE[0] = 2;
        if (atvik_númer != 0) { staðbundið_VALUE[1] = atvik_númer; staðbundið_TYPE[1] = 2; }
        사건중 = true; keyra_skipun(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!Villa) {
            if (나중수 > 0) { int markmið_slóð = 나중실행[0], Íslenska = 나중한국어[0]; for (int Loop_INDEX = 1; Loop_INDEX < 나중수; Loop_INDEX++) { 나중실행[Loop_INDEX - 1] = 나중실행[Loop_INDEX]; 나중한국어[Loop_INDEX - 1] = 나중한국어[Loop_INDEX]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; senda_atvik(markmið_slóð, 0, Íslenska != 0); continue; }
            if (notandi.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int atvik_númer = notandi.화면연결(5, 0, 0, 0, 0, 0); if (atvik_númer == 0) continue;
            if (atvik_númer < 0) { bilun_VALUE("GUI event I/O failed"); return; }
            int Auðkenni_VALUE = atvik_númer & 65535; if (Auðkenni_VALUE < 1 || Auðkenni_VALUE > 32) continue; int hlutur_tilvísun = 화면참조[Auðkenni_VALUE - 1]; if (hlutur_tilvísun == 0) continue;
            if ((atvik_númer & 65536) != 0) {
                if (힙[hlutur_tilvísun + 10] != 0) 힙[hlutur_tilvísun + 9] = 0;
                if (힙[hlutur_tilvísun + 10] == 3) for (int Loop_INDEX = 0; Loop_INDEX < 32; Loop_INDEX++) if (화면참조[Loop_INDEX] != 0 && 힙[화면참조[Loop_INDEX]] == 24) notandi.화면연결(4, Loop_INDEX + 1, 0, 0, 0, 0);
            } else if (힙[hlutur_tilvísun + 4] != 0) {
                int LESTUMIG_tilvísun = úthluta_geymsla(29, 2); if (Villa) return; 힙[LESTUMIG_tilvísun + 2] = hlutur_tilvísun; 힙[LESTUMIG_tilvísun + 3] = 힙[hlutur_tilvísun + 12]; 힙참조[LESTUMIG_tilvísun + 2] = 1; senda_atvik(힙[hlutur_tilvísun + 4], LESTUMIG_tilvísun, 힙[hlutur_tilvísun + 12] != 0);
            }
        }
    }
    public static int Keyra_2() {
        if (notandi.인수개수() == 1 && 자바도구.같음(notandi.Viðföng(0), "-version")) {
            notandi.Skrift("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (notandi.인수개수() < 1) { notandi.Skrift("Usage: java CLASS [ARGS]\n"); return 2; }
        færsla_klasi_Skilgreining = álag_klasi_Skilgreining(hýsa_stafur(notandi.Viðföng(0))); if (Villa || færsla_klasi_Skilgreining < 0) return 1;
        int færsla_P_VALUE = heiti_aðferð(færsla_klasi_Skilgreining, "Keyra_2", "()V");
        boolean 한국어진입 = færsla_P_VALUE >= 0 && (aðferð_aðgangur[færsla_P_VALUE] & 9) == 9;
        if (!한국어진입) færsla_P_VALUE = heiti_aðferð(færsla_klasi_Skilgreining, "main", "([Ljava/lang/String;)V");
        if (færsla_P_VALUE < 0 || (aðferð_aðgangur[færsla_P_VALUE] & 9) != 9) bilun_VALUE("public static void Keyra_2() or main(String[] args) required");
        if (Villa) return 1;
        int Viðföng = úthluta_geymsla(3, notandi.인수개수() - 1); ARRAY_eining[Viðföng] = -1;
        for (int númer = 1; númer < notandi.인수개수() && !Villa; númer++) 힙[Viðföng + 1 + númer] = hýsa_stafur(notandi.Viðföng(númer));
        ramma_INDEX = 0; ramma_aðferð[0] = færsla_P_VALUE; ramma_staða[0] = aðferð_Opna[færsla_P_VALUE]; staðbundið_VALUE[0] = 한국어진입 ? 0 : Viðföng; staðbundið_TYPE[0] = 한국어진입 ? 0 : 2;
        þráður_staða[0] = 1; þráður_hlutur[0] = úthluta_geymsla(13, 2);
        keyra_skipun(); if (!Villa) 화면사건들(); return Villa ? 1 : 0;
    }
}
