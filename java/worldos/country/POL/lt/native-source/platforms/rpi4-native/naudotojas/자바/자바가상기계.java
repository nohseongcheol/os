// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Failas/operandas_eilė/nuoroda/šaka 경계를 Vykdyti_komanda 중 검사한다. */
public final class 자바가상기계 {
    static int[] Failas = new int[16 * 16384], laikinasis_failas = new int[16384], failo_vardas_SMS = new int[512];
    static int[] konstanta_žyma = new int[8192], 상가 = new int[8192], konstanta_SECOND_VALUE = new int[8192], eilutė_nuoroda = new int[8192];
    static int[] metodas_pavadinimas_SMS = new int[512], metodas_TYPE = new int[512], metodas_prieiga = new int[512], metodas_savininkas = new int[512];
    static int[] metodas_Start = new int[512], metodas_baigti_pokalbį = new int[512], metodas_eilė = new int[512], 함수지역 = new int[512];
    static int[] metodas_argumentas_COUNT = new int[512], metodas_argumentas_TYPE = new int[8192], metodas_grąžinti = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] vietinis_VALUE = new int[16384], vietinis_TYPE = new int[16384], operandas_eilė_VALUE = new int[16384], operandas_eilė_TYPE = new int[16384];
    static int[] kadras_metodas = new int[128], kadras_padėtis = new int[128], kadras_eilė = new int[128], 틀명령 = new int[128], 틀초기화 = new int[128];
    static int[] klasė_Apibrėžtis_pavadinimas = new int[16], klasė_Apibrėžtis_dydis = new int[16], klasė_Apibrėžtis_pirminis = new int[16], klasė_Apibrėžtis_Būsena = new int[16], 종칸수 = new int[16], 종초기화 = new int[16];
    static int[] klasė_sąsaja = new int[16 * 16], klasė_sąsaja_COUNT = new int[16];
    static int[] 칸이름 = new int[512], 칸형 = new int[512], 칸주인 = new int[512], 칸권한 = new int[512], 칸위치 = new int[512], 칸값 = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], masyvo_elementas = new int[32768], Store_sveikasis_skaičius = new int[256];
    static int Dydis, 읽기위치, metodas_COUNT, klasės_pavadinimas, kadras_INDEX = -1, 힙끝 = 1, grąžinti_TYPE;
    static int klasė_Apibrėžtis_COUNT, 칸수, 잡기수, 현재읽는종, 던진객체, 잠시수, rodyti_COUNT, aibė_COUNT;
    static int dabartinis_gija, gija_COUNT = 1, įrašas_klasė_Apibrėžtis;
    static int[] gija_kadras = new int[4], gija_Būsena = new int[4], gija_objektas = new int[4], gija_tikslas = new int[4], 가닥대기 = new int[4];
    static boolean KLAIDA, keisti_užklausa;
    static int[] užraktas_savininkas = new int[32768], 잠금깊이 = new int[32768], kadras_užraktas = new int[128], klasė_užraktas = new int[16], klasė_gija = new int[16];

    static void triktis_VALUE(String Word_SMS) {
        if (KLAIDA) return;
        int sritis_CODE = 0;
        if (자바도구.같음(Word_SMS, "ArithmeticException: / by zero")) sritis_CODE = 4;
        if (자바도구.같음(Word_SMS, "NullPointerException") || 자바도구.같음(Word_SMS, "null or invalid array")) sritis_CODE = 5;
        if (자바도구.같음(Word_SMS, "ArrayIndexOutOfBoundsException")) sritis_CODE = 7;
        if (자바도구.같음(Word_SMS, "StringIndexOutOfBoundsException")) sritis_CODE = 8;
        if (자바도구.같음(Word_SMS, "NumberFormatException")) sritis_CODE = 10;
        if (자바도구.같음(Word_SMS, "FileNotFoundException: file open failed")) sritis_CODE = 12;
        if (자바도구.같음(Word_SMS, "IOException: stream closed") || 자바도구.같음(Word_SMS, "IOException: read failed") || 자바도구.같음(Word_SMS, "IOException: write failed")) sritis_CODE = 11;
        if (자바도구.같음(Word_SMS, "ClassCastException")) sritis_CODE = 14;
        if (자바도구.같음(Word_SMS, "NegativeArraySizeException")) sritis_CODE = 15;
        if (sritis_CODE != 0 && kadras_INDEX >= 0) { 예외던짐(sritis_CODE, Word_SMS); return; }
        naudotojas.Rašymas("JVM error: "); naudotojas.Rašymas(Word_SMS); naudotojas.rašymas_simbolis_VALUE(10); KLAIDA = true;
    }
    static boolean klipas(int Paleisti, int 길이) {
        if (Paleisti < 0 || Paleisti >= Failas.length || 길이 < 0) return false;
        int klasė_Apibrėžtis = Paleisti / 16384;
        return Paleisti % 16384 <= klasė_Apibrėžtis_dydis[klasė_Apibrėžtis] && 길이 <= klasė_Apibrėžtis_dydis[klasė_Apibrėžtis] - Paleisti % 16384;
    }
    static int baitas_VALUE() {
        if (!klipas(읽기위치, 1)) { triktis_VALUE("truncated class file"); return 0; }
        return Failas[읽기위치++];
    }
    static int 짧은수() { return baitas_VALUE() << 8 | baitas_VALUE(); }
    static int sveikasis_skaičius() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int 길이) { if (!klipas(읽기위치, 길이)) triktis_VALUE("invalid attribute size"); else 읽기위치 += 길이; }
    static boolean čekis_konstanta(int numeris, int 종류) {
        if (numeris <= 0 || numeris >= konstanta_žyma.length || konstanta_žyma[numeris] != 종류) { triktis_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_diapazonas(int Paleisti, int 길이, String Word_SMS) {
        if (!klipas(Paleisti, 길이)) return false;
        int 읽는자리 = Paleisti, 끝 = Paleisti + 길이;
        for (int Loop_INDEX = 0; Loop_INDEX < Word_SMS.length(); Loop_INDEX++) {
            int simbolio_kodas = Word_SMS.charAt(Loop_INDEX);
            if (simbolio_kodas > 0 && simbolio_kodas < 128) { if (읽는자리 >= 끝 || Failas[읽는자리++] != simbolio_kodas) return false; }
            else if (simbolio_kodas < 2048) {
                if (읽는자리 + 2 > 끝 || Failas[읽는자리++] != (192 | (simbolio_kodas >> 6)) || Failas[읽는자리++] != (128 | (simbolio_kodas & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Failas[읽는자리++] != (224 | (simbolio_kodas >> 12)) || Failas[읽는자리++] != (128 | ((simbolio_kodas >> 6) & 63)) || Failas[읽는자리++] != (128 | (simbolio_kodas & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean Word_SMS(int konstanta_VALUE, String Word_SMS) { return čekis_konstanta(konstanta_VALUE, 1) && SMS_diapazonas(상가[konstanta_VALUE], konstanta_SECOND_VALUE[konstanta_VALUE], Word_SMS); }
    static boolean 같은말(int 가, int SECOND_operandas) {
        if (!čekis_konstanta(가, 1) || !čekis_konstanta(SECOND_operandas, 1) || konstanta_SECOND_VALUE[가] != konstanta_SECOND_VALUE[SECOND_operandas]) return false;
        for (int numeris = 0; numeris < konstanta_SECOND_VALUE[가]; numeris++) if (Failas[상가[가] + numeris] != Failas[상가[SECOND_operandas] + numeris]) return false;
        return true;
    }
    static int klasės_pavadinimas_SMS(int numeris) { return čekis_konstanta(numeris, 7) && čekis_konstanta(상가[numeris], 1) ? 상가[numeris] : 0; }
    static int nuoroda_pavadinimas(int numeris) { return čekis_konstanta(numeris, 12) && čekis_konstanta(상가[numeris], 1) ? 상가[numeris] : 0; }
    static int nuoroda_TYPE(int numeris) { return čekis_konstanta(numeris, 12) && čekis_konstanta(konstanta_SECOND_VALUE[numeris], 1) ? konstanta_SECOND_VALUE[numeris] : 0; }
    static int 서술형(int 끝, boolean 빈형) {
        if (읽기위치 >= 끝) { triktis_VALUE("invalid descriptor"); return 0; }
        int VALUE = baitas_VALUE();
        if (VALUE == 'V' && 빈형) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int Paleisti = 읽기위치;
            while (읽기위치 < 끝 && Failas[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Paleisti) triktis_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        triktis_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int FUNCTION_VALUE) {
        int 이전 = 읽기위치, numeris = metodas_TYPE[FUNCTION_VALUE];
        if (!čekis_konstanta(numeris, 1)) return;
        읽기위치 = 상가[numeris]; int 끝 = 읽기위치 + konstanta_SECOND_VALUE[numeris];
        if (baitas_VALUE() != '(') triktis_VALUE("invalid method descriptor");
        int prekė_COUNT = 0;
        while (!KLAIDA && 읽기위치 < 끝 && Failas[읽기위치] != ')') {
            if (prekė_COUNT == 16) { triktis_VALUE("too many method arguments"); break; }
            metodas_argumentas_TYPE[FUNCTION_VALUE * 16 + prekė_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || baitas_VALUE() != ')') triktis_VALUE("invalid method descriptor");
        metodas_grąžinti[FUNCTION_VALUE] = 서술형(끝, true); metodas_argumentas_COUNT[FUNCTION_VALUE] = prekė_COUNT;
        if (읽기위치 != 끝) triktis_VALUE("invalid method descriptor");
        읽기위치 = 이전;
    }
    static int 상번호() { int VALUE = 짧은수(); return VALUE == 0 ? 0 : 현재읽는종 * 512 + VALUE; }
    static int 명상수() { return metodas_savininkas[kadras_metodas[kadras_INDEX]] * 512 + 명짧(); }
    static void 속성건너() {
        int prekė_COUNT = 짧은수();
        for (int numeris = 0; numeris < prekė_COUNT && !KLAIDA; numeris++) { čekis_konstanta(상번호(), 1); 건너(sveikasis_skaičius()); }
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
    static int padėtis_sveikasis_skaičius(int 읽는자리) {
        if (!klipas(읽는자리, 4)) { triktis_VALUE("truncated bytecode operand"); return 0; }
        return Failas[읽는자리] << 24 | Failas[읽는자리 + 1] << 16 | Failas[읽는자리 + 2] << 8 | Failas[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Paleisti, int 끝) {
        int VALUE = Failas[읽는자리], 길이 = 명령길이(VALUE);
        if (VALUE == 170 || VALUE == 171) {
            int BASE_padėtis = 읽는자리 + 1;
            while ((BASE_padėtis - Paleisti) % 4 != 0) BASE_padėtis++;
            if (끝 - BASE_padėtis < (VALUE == 170 ? 12 : 8)) return 0;
            int įrašas_COUNT = VALUE == 170 ? padėtis_sveikasis_skaičius(BASE_padėtis + 8) - padėtis_sveikasis_skaičius(BASE_padėtis + 4) + 1 : padėtis_sveikasis_skaičius(BASE_padėtis + 4);
            if (įrašas_COUNT < 0 || įrašas_COUNT > 2048) return 0;
            길이 = BASE_padėtis - 읽는자리 + (VALUE == 170 ? 12 + 4 * įrašas_COUNT : 8 + 8 * įrašas_COUNT);
        }
        if (VALUE == 196 && 읽는자리 + 1 < 끝) {
            int Word_duomenys = Failas[읽는자리 + 1]; 길이 = Word_duomenys == 132 ? 6 : (Word_duomenys == 21 || Word_duomenys == 25 || Word_duomenys == 54 || Word_duomenys == 58) ? 4 : 0;
        }
        return 길이 > 0 && 길이 <= 끝 - 읽는자리 ? 길이 : 0;
    }
    static void čekis_vieta_VALUE(int vieta_VALUE, int FUNCTION_VALUE) {
        if (vieta_VALUE < metodas_Start[FUNCTION_VALUE] || vieta_VALUE >= metodas_baigti_pokalbį[FUNCTION_VALUE] || 경계[vieta_VALUE] != FUNCTION_VALUE + 1) triktis_VALUE("invalid branch target");
    }
    static void 클래스읽기(int klasė_Apibrėžtis) {
        현재읽는종 = klasė_Apibrėžtis; 읽기위치 = klasė_Apibrėžtis * 16384; Dydis = 읽기위치 + klasė_Apibrėžtis_dydis[klasė_Apibrėžtis];
        if (sveikasis_skaičius() != 0xcafebabe) { triktis_VALUE("not a class file"); return; }
        int 부판 = 짧은수(), versija_VALUE = 짧은수();
        if (versija_VALUE < 45 || versija_VALUE > 52 || 부판 != 0) { triktis_VALUE("supported class versions: 45..52, minor 0"); return; }
        int konstanta_COUNT = 짧은수(), BASE_padėtis = klasė_Apibrėžtis * 512;
        if (konstanta_COUNT < 1 || konstanta_COUNT > 512) { triktis_VALUE("constant pool limit (511)"); return; }
        for (int įrašas_COUNT = 1; įrašas_COUNT < konstanta_COUNT && !KLAIDA; įrašas_COUNT++) {
            int numeris = BASE_padėtis + įrašas_COUNT, 종류 = baitas_VALUE(); konstanta_žyma[numeris] = 종류;
            if (종류 == 1) { konstanta_SECOND_VALUE[numeris] = 짧은수(); 상가[numeris] = 읽기위치; 건너(konstanta_SECOND_VALUE[numeris]); }
            else if (종류 == 3) 상가[numeris] = sveikasis_skaičius();
            else if (종류 == 7 || 종류 == 8) 상가[numeris] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[numeris] = 상번호(); konstanta_SECOND_VALUE[numeris] = 상번호(); }
            else triktis_VALUE("unsupported constant type");
        }
        int teisė_VALUE = 짧은수();
        if ((teisė_VALUE & (0x2000 | 0x4000)) != 0) triktis_VALUE("annotation/enum class unsupported");
        klasė_Apibrėžtis_pavadinimas[klasė_Apibrėžtis] = klasės_pavadinimas_SMS(상번호());
        klasė_Apibrėžtis_pirminis[klasė_Apibrėžtis] = klasės_pavadinimas_SMS(상번호());
        int sąsaja_COUNT = 짧은수(); if (sąsaja_COUNT > 16) { triktis_VALUE("interface count limit"); return; }
        klasė_sąsaja_COUNT[klasė_Apibrėžtis] = sąsaja_COUNT;
        for (int Loop_INDEX = 0; Loop_INDEX < sąsaja_COUNT; Loop_INDEX++) klasė_sąsaja[klasė_Apibrėžtis * 16 + Loop_INDEX] = klasės_pavadinimas_SMS(상번호());
        int laukas_COUNT = 짧은수();
        if (laukas_COUNT > 512 - 칸수) { triktis_VALUE("field count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < laukas_COUNT && !KLAIDA; Loop_INDEX++) {
            int Failas_INDEX = 칸수++; 칸주인[Failas_INDEX] = klasė_Apibrėžtis; 칸권한[Failas_INDEX] = 짧은수(); 칸이름[Failas_INDEX] = 상번호(); 칸형[Failas_INDEX] = 상번호();
            čekis_konstanta(칸이름[Failas_INDEX], 1); čekis_konstanta(칸형[Failas_INDEX], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[칸형[Failas_INDEX]]; int sritis_CODE = 서술형(읽기위치 + konstanta_SECOND_VALUE[칸형[Failas_INDEX]], false); 읽기위치 = 보존값;
            if ((칸권한[Failas_INDEX] & 8) == 0) 칸위치[Failas_INDEX] = 종칸수[klasė_Apibrėžtis]++;
            int atributas_duomenys = 짧은수();
            for (int vidinis_padėtis = 0; vidinis_padėtis < atributas_duomenys && !KLAIDA; vidinis_padėtis++) {
                int pavadinimas_konstanta = 상번호(), 유효길이 = sveikasis_skaičius();
                if (Word_SMS(pavadinimas_konstanta, "ConstantValue") && 유효길이 == 2) {
                    int duomenys_VALUE = 상번호();
                    if (sritis_CODE == 1 && čekis_konstanta(duomenys_VALUE, 3)) 칸값[Failas_INDEX] = 상가[duomenys_VALUE];
                    else if (sritis_CODE == 2 && čekis_konstanta(duomenys_VALUE, 8)) 칸값[Failas_INDEX] = konstanta_SMS(상가[duomenys_VALUE]);
                } else 건너(유효길이);
            }
        }
        int prekė_COUNT = 짧은수();
        if (prekė_COUNT > 512 - metodas_COUNT) { triktis_VALUE("method count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < prekė_COUNT && !KLAIDA; Loop_INDEX++) {
            int numeris = metodas_COUNT++; metodas_savininkas[numeris] = klasė_Apibrėžtis;
            metodas_prieiga[numeris] = 짧은수(); metodas_pavadinimas_SMS[numeris] = 상번호(); metodas_TYPE[numeris] = 상번호();
            čekis_konstanta(metodas_pavadinimas_SMS[numeris], 1); 서술읽기(numeris);
            if ((metodas_prieiga[numeris] & 8) == 0) {
                if (metodas_argumentas_COUNT[numeris] == 16) { triktis_VALUE("too many instance method arguments"); return; }
                for (int Palyginimas_padėtis = metodas_argumentas_COUNT[numeris]; Palyginimas_padėtis > 0; Palyginimas_padėtis--) metodas_argumentas_TYPE[numeris * 16 + Palyginimas_padėtis] = metodas_argumentas_TYPE[numeris * 16 + Palyginimas_padėtis - 1];
                metodas_argumentas_TYPE[numeris * 16] = 2; metodas_argumentas_COUNT[numeris]++;
            }
            if ((metodas_prieiga[numeris] & 0x100) != 0) triktis_VALUE("user native method unsupported");
            if (Word_SMS(metodas_pavadinimas_SMS[numeris], "<clinit>")) 종초기화[klasė_Apibrėžtis] = numeris + 1;
            for (int priekinis_VALUE = 0; priekinis_VALUE < numeris; priekinis_VALUE++) if (metodas_savininkas[priekinis_VALUE] == klasė_Apibrėžtis && 같은말(metodas_pavadinimas_SMS[priekinis_VALUE], metodas_pavadinimas_SMS[numeris]) && 같은말(metodas_TYPE[priekinis_VALUE], metodas_TYPE[numeris])) triktis_VALUE("duplicate method");
            int atributas_COUNT = 짧은수();
            for (int atributas_VALUE = 0; atributas_VALUE < atributas_COUNT && !KLAIDA; atributas_VALUE++) {
                int Pavadinimas_2 = 상번호(), 길이 = sveikasis_skaičius(), Paleisti = 읽기위치;
                if (!klipas(Paleisti, 길이)) { triktis_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Pavadinimas_2, "Code")) {
                    if (metodas_Start[numeris] != 0) triktis_VALUE("duplicate Code attribute");
                    metodas_eilė[numeris] = 짧은수(); 함수지역[numeris] = 짧은수(); int 코드길이 = sveikasis_skaičius();
                    if (metodas_eilė[numeris] > 128 || 함수지역[numeris] > 128 || 함수지역[numeris] < metodas_argumentas_COUNT[numeris]
                        || 코드길이 < 1 || 코드길이 > 8192) triktis_VALUE("method memory limits exceeded");
                    metodas_Start[numeris] = 읽기위치; 건너(코드길이); metodas_baigti_pokalbį[numeris] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { triktis_VALUE("exception table limit"); return; }
                    for (int vidinis_padėtis = 0; vidinis_padėtis < 잡는수; vidinis_padėtis++) {
                        int 오류참조 = 잡기수++; 잡기함수[오류참조] = numeris;
                        잡기시작[오류참조] = metodas_Start[numeris] + 짧은수(); 잡기끝[오류참조] = metodas_Start[numeris] + 짧은수();
                        잡기위치[오류참조] = metodas_Start[numeris] + 짧은수(); int 부호값 = 상번호(); 잡기종[오류참조] = 부호값 == 0 ? 0 : klasės_pavadinimas_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != Paleisti + 길이) triktis_VALUE("Code attribute size mismatch");
                } else 건너(길이);
            }
            if ((metodas_prieiga[numeris] & 0x400) != 0) continue;
            if (metodas_Start[numeris] == 0) triktis_VALUE("missing Code attribute");
            int 칸 = metodas_Start[numeris];
            while (칸 < metodas_baigti_pokalbį[numeris] && !KLAIDA) {
                int 길이 = 길이읽기(칸, metodas_Start[numeris], metodas_baigti_pokalbį[numeris]);
                if (길이 == 0) { triktis_VALUE("unsupported or truncated bytecode"); break; }
                경계[칸] = numeris + 1; 칸 += 길이;
            }
            칸 = metodas_Start[numeris];
            while (칸 < metodas_baigti_pokalbį[numeris] && !KLAIDA) {
                int VALUE = Failas[칸];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) čekis_vieta_VALUE(칸 + (short)(Failas[칸 + 1] << 8 | Failas[칸 + 2]), numeris);
                if (VALUE == 200) čekis_vieta_VALUE(칸 + padėtis_sveikasis_skaičius(칸 + 1), numeris);
                if (VALUE == 170 || VALUE == 171) {
                    int 읽는자리 = 칸 + 1; while ((읽는자리 - metodas_Start[numeris]) % 4 != 0) 읽는자리++;
                    čekis_vieta_VALUE(칸 + padėtis_sveikasis_skaičius(읽는자리), numeris);
                    int įrašas_COUNT = VALUE == 170 ? padėtis_sveikasis_skaičius(읽는자리 + 8) - padėtis_sveikasis_skaičius(읽는자리 + 4) + 1 : padėtis_sveikasis_skaičius(읽는자리 + 4);
                    읽는자리 += VALUE == 170 ? 12 : 8;
                    for (int vidinis_padėtis = 0; vidinis_padėtis < įrašas_COUNT; vidinis_padėtis++) čekis_vieta_VALUE(칸 + padėtis_sveikasis_skaičius(읽는자리 + vidinis_padėtis * (VALUE == 170 ? 4 : 8) + (VALUE == 170 ? 0 : 4)), numeris);
                }
                칸 += 길이읽기(칸, metodas_Start[numeris], metodas_baigti_pokalbį[numeris]);
            }
            for (int vidinis_padėtis = 0; vidinis_padėtis < 잡기수; vidinis_padėtis++) if (잡기함수[vidinis_padėtis] == numeris) {
                čekis_vieta_VALUE(잡기시작[vidinis_padėtis], numeris); čekis_vieta_VALUE(잡기위치[vidinis_padėtis], numeris);
                if (잡기끝[vidinis_padėtis] != metodas_baigti_pokalbį[numeris]) čekis_vieta_VALUE(잡기끝[vidinis_padėtis], numeris);
                if (잡기시작[vidinis_padėtis] >= 잡기끝[vidinis_padėtis]) triktis_VALUE("invalid exception range");
            }
        }
        if (!KLAIDA) 속성건너();
        if (읽기위치 != Dydis) triktis_VALUE("extra class file data");
    }
    static int priskirti_Saugykla(int 종류, int 길이) { return 새기억(종류, 길이); }
    static boolean objektas_VALUE(int nuoroda, int 종류) {
        if (!객체유효(nuoroda)) return false;
        if (힙[nuoroda] != 종류) { triktis_VALUE("object type mismatch"); return false; }
        return true;
    }
    static int konstanta_SMS(int INDEX) {
        if (!čekis_konstanta(INDEX, 1)) return 0;
        if (eilutė_nuoroda[INDEX] != 0) return eilutė_nuoroda[INDEX];
        int nuoroda = priskirti_Saugykla(1, konstanta_SECOND_VALUE[INDEX]); if (KLAIDA) return 0;
        int 끝 = 상가[INDEX] + konstanta_SECOND_VALUE[INDEX], numeris = 상가[INDEX], 길이 = 0;
        while (numeris < 끝 && !KLAIDA) {
            int VALUE = Failas[numeris++];
            if (VALUE == 0) triktis_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && numeris < 끝) {
                int toliau_prekė = Failas[numeris++];
                if ((toliau_prekė & 192) != 128) triktis_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | toliau_prekė & 63;
                if (VALUE != 0 && VALUE < 128) triktis_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && numeris + 1 < 끝) {
                int 가 = Failas[numeris++], SECOND_operandas = Failas[numeris++];
                if ((가 & 192) != 128 || (SECOND_operandas & 192) != 128) triktis_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | SECOND_operandas & 63;
                if (VALUE < 2048) triktis_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) triktis_VALUE("invalid modified UTF-8");
            힙[nuoroda + 2 + 길이++] = VALUE;
        }
        힙[nuoroda + 1] = 길이; eilutė_nuoroda[INDEX] = nuoroda; return nuoroda;
    }
    static int organizuoti_simbolis(String VALUE) {
        int nuoroda = priskirti_Saugykla(1, VALUE.length()); if (KLAIDA) return 0;
        for (int numeris = 0; numeris < VALUE.length(); numeris++) 힙[nuoroda + 2 + numeris] = VALUE.charAt(numeris);
        return nuoroda;
    }
    static void rašymas_SMS(int nuoroda) {
        if (nuoroda == 0) { naudotojas.Rašymas("null"); return; }
        if (!objektas_VALUE(nuoroda, 1)) return;
        for (int numeris = 0; numeris < 힙[nuoroda + 1]; numeris++) naudotojas.rašymas_simbolis_VALUE(힙[nuoroda + 2 + numeris]);
    }
    static int skaitmuo_simbolis(int VALUE) {
        int nuoroda = priskirti_Saugykla(1, 11); if (KLAIDA) return 0;
        int 길이 = 0;
        if (VALUE < 0) 힙[nuoroda + 2 + 길이++] = '-'; else VALUE = -VALUE;
        int vietos_rodyklė = 1000000000; boolean Paleisti = false;
        while (vietos_rodyklė != 0) {
            int numeris = -(VALUE / vietos_rodyklė);
            if (numeris != 0 || Paleisti || vietos_rodyklė == 1) { 힙[nuoroda + 2 + 길이++] = '0' + numeris; Paleisti = true; }
            VALUE %= vietos_rodyklė; vietos_rodyklė /= 10;
        }
        힙[nuoroda + 1] = 길이; return nuoroda;
    }
    static int 정수해독(int nuoroda) {
        if (!objektas_VALUE(nuoroda, 1)) return 0;
        int 길이 = 힙[nuoroda + 1], numeris = 0, VALUE = 0; boolean 음수 = false;
        if (길이 > 0 && (힙[nuoroda + 2] == '-' || 힙[nuoroda + 2] == '+')) { 음수 = 힙[nuoroda + 2] == '-'; numeris++; }
        if (numeris == 길이) triktis_VALUE("NumberFormatException");
        for (; numeris < 길이 && !KLAIDA; numeris++) {
            int skaitmuo_VALUE = 힙[nuoroda + 2 + numeris] - '0';
            if (skaitmuo_VALUE < 0 || skaitmuo_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && skaitmuo_VALUE > (음수 ? 8 : 7)) triktis_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - skaitmuo_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int TYPE_VALUE) {
        if (KLAIDA) return;
        if (kadras_INDEX < 0 || kadras_eilė[kadras_INDEX] >= metodas_eilė[kadras_metodas[kadras_INDEX]]) { triktis_VALUE("operand stack overflow"); return; }
        int 칸 = kadras_INDEX * 128 + kadras_eilė[kadras_INDEX]++; operandas_eilė_VALUE[칸] = VALUE; operandas_eilė_TYPE[칸] = TYPE_VALUE;
    }
    static int 빼기(int TYPE_VALUE) {
        if (KLAIDA) return 0;
        if (kadras_INDEX < 0 || kadras_eilė[kadras_INDEX] < 1) { triktis_VALUE("operand stack underflow"); return 0; }
        int 칸 = kadras_INDEX * 128 + --kadras_eilė[kadras_INDEX]; grąžinti_TYPE = operandas_eilė_TYPE[칸];
        if (TYPE_VALUE != 0 && grąžinti_TYPE != TYPE_VALUE) triktis_VALUE("operand type mismatch");
        if (grąžinti_TYPE == 2) apsaugoti_VALUE(operandas_eilė_VALUE[칸]);
        return operandas_eilė_VALUE[칸];
    }
    static void 지역읽기(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[kadras_metodas[kadras_INDEX]] || INDEX < 0 || vietinis_TYPE[kadras_INDEX * 128 + INDEX] != TYPE_VALUE) { triktis_VALUE("invalid or uninitialized local"); return; }
        넣기(vietinis_VALUE[kadras_INDEX * 128 + INDEX], TYPE_VALUE);
    }
    static void rašymas_vietinis(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[kadras_metodas[kadras_INDEX]] || INDEX < 0) { triktis_VALUE("local index out of range"); return; }
        int VALUE = 빼기(TYPE_VALUE); vietinis_VALUE[kadras_INDEX * 128 + INDEX] = VALUE; vietinis_TYPE[kadras_INDEX * 128 + INDEX] = TYPE_VALUE;
    }
    static int 명바() {
        int Pozicija = kadras_padėtis[kadras_INDEX];
        if (Pozicija < metodas_Start[kadras_metodas[kadras_INDEX]] || Pozicija >= metodas_baigti_pokalbį[kadras_metodas[kadras_INDEX]]) { triktis_VALUE("instruction pointer out of range"); return 0; }
        kadras_padėtis[kadras_INDEX]++; return Failas[Pozicija];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void judėti_VALUE(int Pozicija) {
        int FUNCTION_VALUE = kadras_metodas[kadras_INDEX];
        if (Pozicija < metodas_Start[FUNCTION_VALUE] || Pozicija >= metodas_baigti_pokalbį[FUNCTION_VALUE] || 경계[Pozicija] != FUNCTION_VALUE + 1) triktis_VALUE("invalid branch target");
        else kadras_padėtis[kadras_INDEX] = Pozicija;
    }
    static void 호출(int FUNCTION_VALUE) {
        if (kadras_INDEX % 32 == 31) { triktis_VALUE("call stack limit (32)"); return; }
        int toliau_prekė = kadras_INDEX + 1;
        for (int numeris = 0; numeris < 128; numeris++) vietinis_TYPE[toliau_prekė * 128 + numeris] = 0;
        for (int numeris = metodas_argumentas_COUNT[FUNCTION_VALUE] - 1; numeris >= 0; numeris--) {
            vietinis_VALUE[toliau_prekė * 128 + numeris] = 빼기(metodas_argumentas_TYPE[FUNCTION_VALUE * 16 + numeris]); vietinis_TYPE[toliau_prekė * 128 + numeris] = metodas_argumentas_TYPE[FUNCTION_VALUE * 16 + numeris];
        }
        if (KLAIDA) return;
        kadras_INDEX = toliau_prekė; 틀초기화[kadras_INDEX] = 0; kadras_metodas[kadras_INDEX] = FUNCTION_VALUE; kadras_padėtis[kadras_INDEX] = metodas_Start[FUNCTION_VALUE]; kadras_eilė[kadras_INDEX] = 0;
    }
    static void grąžinti_KR(int TYPE_VALUE) {
        if (TYPE_VALUE != metodas_grąžinti[kadras_metodas[kadras_INDEX]]) { triktis_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        if (틀초기화[kadras_INDEX] != 0) klasė_Apibrėžtis_Būsena[틀초기화[kadras_INDEX] - 1] = 2;
        if (kadras_užraktas[kadras_INDEX] != 0) { išleisti_užraktas(kadras_užraktas[kadras_INDEX]); kadras_užraktas[kadras_INDEX] = 0; }
        kadras_INDEX--; if (kadras_INDEX >= dabartinis_gija * 32 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
    }
    static int[] Stream_failo_vardas = new int[64];
    static void Failas_Stream_CALL(int savininkas_VALUE, int Pavadinimas_2, int formatas_VALUE, int Komanda) {
        boolean Išvestis = Word_SMS(savininkas_VALUE, "java/io/FileOutputStream");
        int 종류 = Išvestis ? 6 : 5;
        if (Komanda == 183 && Word_SMS(Pavadinimas_2, "<init>")) {
            boolean 이어 = false;
            if (Išvestis && Word_SMS(formatas_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(formatas_VALUE, "(Ljava/lang/String;)V")) { triktis_VALUE("unsupported file stream constructor"); return; }
            int Failas_įrašas_pavadinimas = 빼기(2), Stream_VALUE = 빼기(2);
            if (!objektas_VALUE(Failas_įrašas_pavadinimas, 1) || !objektas_VALUE(Stream_VALUE, 종류) || KLAIDA) return;
            if (힙[Stream_VALUE + 3] != 0) { triktis_VALUE("file stream already initialized"); return; }
            int 길이 = 힙[Failas_įrašas_pavadinimas + 1];
            if (길이 < 1 || 길이 > 63) { triktis_VALUE("invalid file name length"); return; }
            for (int 칸 = 0; 칸 < 길이; 칸++) {
                int VALUE = 힙[Failas_įrašas_pavadinimas + 2 + 칸];
                if (VALUE < 1) { triktis_VALUE("invalid file stream path"); return; }
                Stream_failo_vardas[칸] = VALUE;
            }
            Stream_failo_vardas[길이] = 0;
            int 서술자 = naudotojas.파일서술자열기(Stream_failo_vardas, Išvestis ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { triktis_VALUE("FileNotFoundException: file open failed"); return; }
            힙[Stream_VALUE + 2] = 서술자; 힙[Stream_VALUE + 3] = 1;
            return;
        }
        if (Komanda != 182) { triktis_VALUE("invalid file stream invocation"); return; }
        if ((Išvestis && Word_SMS(Pavadinimas_2, "write") || !Išvestis && Word_SMS(Pavadinimas_2, "read"))
            && (Word_SMS(formatas_VALUE, Išvestis ? "([B)V" : "([B)I") || Word_SMS(formatas_VALUE, Išvestis ? "([BII)V" : "([BII)I"))) {
            boolean klipas_VALUE = Word_SMS(formatas_VALUE, Išvestis ? "([BII)V" : "([BII)I");
            int įrašas_COUNT = klipas_VALUE ? 빼기(1) : 0, 시작점 = klipas_VALUE ? 빼기(1) : 0, duomenys_ARRAY = 빼기(2), objektas_nuoroda = 빼기(2);
            if (!objektas_VALUE(duomenys_ARRAY, 20) || !objektas_VALUE(objektas_nuoroda, 종류)) return;
            if (!klipas_VALUE) įrašas_COUNT = 힙[duomenys_ARRAY + 1];
            if (시작점 < 0 || įrašas_COUNT < 0 || 시작점 > 힙[duomenys_ARRAY + 1] - įrašas_COUNT) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[objektas_nuoroda + 3] == 0 || 힙[objektas_nuoroda + 2] < 0) { triktis_VALUE("IOException: stream closed"); return; }
            int baigta_COUNT = 0;
            while (baigta_COUNT < įrašas_COUNT && !KLAIDA) {
                int 반환값 = Išvestis ? naudotojas.파일한바이트쓰기(힙[objektas_nuoroda + 2], 힙[duomenys_ARRAY + 2 + 시작점 + baigta_COUNT]) : naudotojas.파일한바이트읽기(힙[objektas_nuoroda + 2]);
                if (반환값 < 0) { triktis_VALUE(Išvestis ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!Išvestis && 반환값 == 256) break;
                if (!Išvestis) 힙[duomenys_ARRAY + 2 + 시작점 + baigta_COUNT] = (byte)반환값;
                baigta_COUNT++;
            }
            if (!Išvestis) 넣기(įrašas_COUNT != 0 && baigta_COUNT == 0 ? -1 : baigta_COUNT, 1);
            return;
        }
        if (Išvestis && Word_SMS(Pavadinimas_2, "flush") && Word_SMS(formatas_VALUE, "()V")) { int objektas_nuoroda = 빼기(2); if (objektas_VALUE(objektas_nuoroda, 종류) && 힙[objektas_nuoroda + 2] < 0) triktis_VALUE("IOException: stream closed"); return; }
        int Veiksmas = -1, VALUE = 0;
        if (Word_SMS(Pavadinimas_2, "close") && Word_SMS(formatas_VALUE, "()V")) Veiksmas = 0;
        if (!Išvestis && Word_SMS(Pavadinimas_2, "read") && Word_SMS(formatas_VALUE, "()I")) Veiksmas = 1;
        if (Išvestis && Word_SMS(Pavadinimas_2, "write") && Word_SMS(formatas_VALUE, "(I)V")) { Veiksmas = 2; VALUE = 빼기(1); }
        if (Veiksmas < 0) { triktis_VALUE("unsupported file stream method"); return; }
        int Stream_VALUE = 빼기(2);
        if (!objektas_VALUE(Stream_VALUE, 종류) || KLAIDA) return;
        if (힙[Stream_VALUE + 3] == 0) { triktis_VALUE("uninitialized file stream"); return; }
        int 서술자 = 힙[Stream_VALUE + 2];
        if (Veiksmas == 0) {
            if (서술자 >= 0 && naudotojas.파일서술자닫기(서술자) < 0) triktis_VALUE("IOException: close failed");
            힙[Stream_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { triktis_VALUE("IOException: stream closed"); return; }
        if (Veiksmas == 1) {
            int REZULTATAS = naudotojas.파일한바이트읽기(서술자);
            if (REZULTATAS < -1) triktis_VALUE("IOException: read failed"); else 넣기(REZULTATAS == 256 ? -1 : REZULTATAS, 1);
        } else if (naudotojas.파일한바이트쓰기(서술자, VALUE) != 1) triktis_VALUE("IOException: write failed");
    }
    static void CALL_metodas(int INDEX, int Komanda) {
        if (INDEX <= 0 || INDEX >= konstanta_žyma.length || (konstanta_žyma[INDEX] != 10 && konstanta_žyma[INDEX] != 11)) { triktis_VALUE("invalid method reference"); return; }
        int savininkas_VALUE = klasės_pavadinimas_SMS(상가[INDEX]), Pavadinimas_2 = nuoroda_pavadinimas(konstanta_SECOND_VALUE[INDEX]), formatas_VALUE = nuoroda_TYPE(konstanta_SECOND_VALUE[INDEX]);
        if (KLAIDA) return;
        if (기본호출(savininkas_VALUE, Pavadinimas_2, formatas_VALUE, Komanda)) return;
        if (Word_SMS(savininkas_VALUE, "java/io/FileInputStream") || Word_SMS(savininkas_VALUE, "java/io/FileOutputStream")) {
            Failas_Stream_CALL(savininkas_VALUE, Pavadinimas_2, formatas_VALUE, Komanda); return;
        }
        if (Komanda == 184 && Word_SMS(savininkas_VALUE, "java/lang/Integer") && Word_SMS(Pavadinimas_2, "parseInt") && Word_SMS(formatas_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Komanda == 182 && Word_SMS(savininkas_VALUE, "java/io/PrintStream") && (Word_SMS(Pavadinimas_2, "println") || Word_SMS(Pavadinimas_2, "print"))) {
            int TYPE_VALUE = 0, VALUE = 0;
            if (Word_SMS(formatas_VALUE, "(I)V")) { TYPE_VALUE = 1; VALUE = 빼기(1); }
            else if (Word_SMS(formatas_VALUE, "(Z)V")) { TYPE_VALUE = 2; VALUE = 빼기(1); }
            else if (Word_SMS(formatas_VALUE, "(C)V")) { TYPE_VALUE = 3; VALUE = 빼기(1); }
            else if (Word_SMS(formatas_VALUE, "(Ljava/lang/String;)V")) { TYPE_VALUE = 4; VALUE = 빼기(2); }
            else if (!Word_SMS(formatas_VALUE, "()V") || !Word_SMS(Pavadinimas_2, "println")) triktis_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) triktis_VALUE("invalid PrintStream receiver");
            if (KLAIDA) return;
            if (TYPE_VALUE == 1) 자바도구.rašymas_numeris(VALUE);
            if (TYPE_VALUE == 2) naudotojas.Rašymas(VALUE == 0 ? "false" : "true");
            if (TYPE_VALUE == 3) naudotojas.rašymas_simbolis_VALUE(VALUE & 65535);
            if (TYPE_VALUE == 4) rašymas_SMS(VALUE);
            if (Word_SMS(Pavadinimas_2, "println")) naudotojas.rašymas_simbolis_VALUE(10);
            return;
        }
        if (Komanda == 182 && Word_SMS(savininkas_VALUE, "java/lang/String")) {
            if (Word_SMS(Pavadinimas_2, "length") && Word_SMS(formatas_VALUE, "()I")) {
                int nuoroda = 빼기(2); if (objektas_VALUE(nuoroda, 1)) 넣기(힙[nuoroda + 1], 1); return;
            }
            if (Word_SMS(Pavadinimas_2, "charAt") && Word_SMS(formatas_VALUE, "(I)C")) {
                int apatinis_indeksas_VALUE = 빼기(1), nuoroda = 빼기(2);
                if (objektas_VALUE(nuoroda, 1)) {
                    if (apatinis_indeksas_VALUE < 0 || apatinis_indeksas_VALUE >= 힙[nuoroda + 1]) triktis_VALUE("StringIndexOutOfBoundsException"); else 넣기(힙[nuoroda + 2 + apatinis_indeksas_VALUE], 1);
                }
                return;
            }
        }
        if (Word_SMS(savininkas_VALUE, "java/lang/StringBuilder")) {
            if (Komanda == 183 && Word_SMS(Pavadinimas_2, "<init>") && Word_SMS(formatas_VALUE, "()V")) { objektas_VALUE(빼기(2), 4); return; }
            if (Komanda == 182 && Word_SMS(Pavadinimas_2, "toString") && Word_SMS(formatas_VALUE, "()Ljava/lang/String;")) {
                int nuoroda = 빼기(2); if (objektas_VALUE(nuoroda, 4)) 넣기(힙[nuoroda + 2] == 0 ? organizuoti_simbolis("") : 힙[nuoroda + 2], 2); return;
            }
            if (Komanda == 182 && Word_SMS(Pavadinimas_2, "append")) {
                int Tekstas = 0;
                if (Word_SMS(formatas_VALUE, "(I)Ljava/lang/StringBuilder;")) Tekstas = skaitmuo_simbolis(빼기(1));
                else if (Word_SMS(formatas_VALUE, "(Z)Ljava/lang/StringBuilder;")) Tekstas = organizuoti_simbolis(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(formatas_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); Tekstas = priskirti_Saugykla(1, 1); if (!KLAIDA) 힙[Tekstas + 2] = VALUE & 65535;
                }
                else if (Word_SMS(formatas_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Tekstas = 빼기(2); if (Tekstas == 0) Tekstas = organizuoti_simbolis("null"); }
                else { triktis_VALUE("unsupported StringBuilder append"); return; }
                int nuoroda = 빼기(2); if (!objektas_VALUE(nuoroda, 4) || !objektas_VALUE(Tekstas, 1)) return;
                int priekinis_VALUE = 힙[nuoroda + 2], 앞길이 = priekinis_VALUE == 0 ? 0 : 힙[priekinis_VALUE + 1], 뒤길이 = 힙[Tekstas + 1];
                int 새글 = priskirti_Saugykla(1, 앞길이 + 뒤길이); if (KLAIDA) return;
                for (int numeris = 0; numeris < 앞길이; numeris++) 힙[새글 + 2 + numeris] = 힙[priekinis_VALUE + 2 + numeris];
                for (int numeris = 0; numeris < 뒤길이; numeris++) 힙[새글 + 2 + 앞길이 + numeris] = 힙[Tekstas + 2 + numeris];
                힙[nuoroda + 2] = 새글; 넣기(nuoroda, 2); return;
            }
        }
        int klasė_Apibrėžtis = FIND_klasė_Apibrėžtis(savininkas_VALUE); if (klasė_Apibrėžtis < 0 || KLAIDA) return;
        int Failas_INDEX = FIND_metodas(klasė_Apibrėžtis, Pavadinimas_2, formatas_VALUE);
        if (Failas_INDEX < 0) {
            for (int simbolio_kodas = klasė_Apibrėžtis, įrašas_COUNT = 0; simbolio_kodas >= 0 && įrašas_COUNT < 16; įrašas_COUNT++, simbolio_kodas = pirminis_klasė(simbolio_kodas))
                if (Word_SMS(klasė_Apibrėžtis_pirminis[simbolio_kodas], "java/lang/Thread")) { 가닥호출(Pavadinimas_2, formatas_VALUE, Komanda); return; }
            triktis_VALUE("NoSuchMethodError"); return;
        }
        if (((metodas_prieiga[Failas_INDEX] & 8) != 0) != (Komanda == 184)) { triktis_VALUE("method static/instance mismatch"); return; }
        if (Komanda == 184) { if (!초기화(metodas_savininkas[Failas_INDEX], 틀명령[kadras_INDEX])) return; }
        else {
            int 읽는자리 = kadras_eilė[kadras_INDEX] - metodas_argumentas_COUNT[Failas_INDEX];
            if (읽는자리 < 0 || operandas_eilė_TYPE[kadras_INDEX * 128 + 읽는자리] != 2) { triktis_VALUE("invalid method receiver"); return; }
            int objektas_nuoroda = operandas_eilė_VALUE[kadras_INDEX * 128 + 읽는자리];
            if (!객체유효(objektas_nuoroda)) return;
            if (힙[objektas_nuoroda] < 32 || !종포함(힙[objektas_nuoroda] - 32, savininkas_VALUE)) { triktis_VALUE("method receiver type mismatch"); return; }
            if (Komanda != 183) Failas_INDEX = FIND_metodas(힙[objektas_nuoroda] - 32, Pavadinimas_2, formatas_VALUE);
        }
        if (Failas_INDEX < 0 || (metodas_prieiga[Failas_INDEX] & 0x400) != 0) { triktis_VALUE("AbstractMethodError"); return; }
        int užraktas_nuoroda = 0;
        if ((metodas_prieiga[Failas_INDEX] & 32) != 0) {
            if (Komanda == 184) { int simbolio_kodas = metodas_savininkas[Failas_INDEX]; if (klasė_užraktas[simbolio_kodas] == 0) klasė_užraktas[simbolio_kodas] = priskirti_Saugykla(8, 0); užraktas_nuoroda = klasė_užraktas[simbolio_kodas]; }
            else užraktas_nuoroda = operandas_eilė_VALUE[kadras_INDEX * 128 + kadras_eilė[kadras_INDEX] - metodas_argumentas_COUNT[Failas_INDEX]];
            if (!잠금얻기(užraktas_nuoroda)) { if (!KLAIDA) kadras_padėtis[kadras_INDEX] = 틀명령[kadras_INDEX]; return; }
        }
        호출(Failas_INDEX); if (!KLAIDA) kadras_užraktas[kadras_INDEX] = užraktas_nuoroda;
    }
    static boolean 배열저장가능(int ARRAY_nuoroda, int duomenys_VALUE) {
        if (duomenys_VALUE == 0 || masyvo_elementas[ARRAY_nuoroda] == 0) return true;
        boolean 성공여부 = masyvo_elementas[ARRAY_nuoroda] == -1 ? (duomenys_VALUE > 0 && duomenys_VALUE < 힙끝 && 힙[duomenys_VALUE] == 1) : 맞는객체(duomenys_VALUE, masyvo_elementas[ARRAY_nuoroda]);
        if (!성공여부 && !KLAIDA) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int 배열칸(int nuoroda, int apatinis_indeksas_VALUE, int TYPE_VALUE) {
        if (!objektas_VALUE(nuoroda, TYPE_VALUE)) return 0;
        if (apatinis_indeksas_VALUE < 0 || apatinis_indeksas_VALUE >= 힙[nuoroda + 1]) { triktis_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return nuoroda + 2 + apatinis_indeksas_VALUE;
    }
    static void Vykdyti_komanda() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (KLAIDA) { if (던진객체 != 0) rodyklė_išimtis(); if (KLAIDA || kadras_INDEX < dabartinis_gija * 32) break; }
            if (kadras_INDEX < dabartinis_gija * 32 || keisti_užklausa || --조각 == 0) { if (!SWITCH_gija()) break; 조각 = 100; }
            if (kadras_INDEX == 0 && klasė_Apibrėžtis_Būsena[įrašas_klasė_Apibrėžtis] != 2 && !초기화(įrašas_klasė_Apibrėžtis, kadras_padėtis[kadras_INDEX])) continue;
            if (kadras_INDEX == dabartinis_gija * 32 && dabartinis_gija != 0 && (metodas_prieiga[kadras_metodas[kadras_INDEX]] & 32) != 0 && kadras_užraktas[kadras_INDEX] == 0) {
                int objektas_nuoroda = gija_tikslas[dabartinis_gija]; if (!잠금얻기(objektas_nuoroda)) { if (KLAIDA) break; continue; } kadras_užraktas[kadras_INDEX] = objektas_nuoroda;
            }
            잠시수 = 0;
            if (--남음 == 0) { triktis_VALUE("instruction limit (500000)"); break; }
            int Paleisti = kadras_padėtis[kadras_INDEX]; 틀명령[kadras_INDEX] = Paleisti; int VALUE = 명바();
            if (KLAIDA) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int numeris = metodas_savininkas[kadras_metodas[kadras_INDEX]] * 512 + (VALUE == 18 ? 명바() : 명짧());
                if (numeris <= 0 || numeris >= konstanta_žyma.length) triktis_VALUE("invalid ldc constant");
                else if (konstanta_žyma[numeris] == 3) 넣기(상가[numeris], 1);
                else if (konstanta_žyma[numeris] == 8) 넣기(konstanta_SMS(상가[numeris]), 2);
                else triktis_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { rašymas_vietinis(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { rašymas_vietinis(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { rašymas_vietinis(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE >= 50 && VALUE <= 53) {
                int įrašas_padėtis = 빼기(1), objektas_nuoroda = 빼기(2), sritis_CODE = VALUE == 46 ? 2 : VALUE == 50 ? 3 : VALUE == 51 ? 20 : VALUE == 52 ? 22 : 23;
                if (VALUE == 51 && objektas_nuoroda > 0 && objektas_nuoroda < 힙끝 && 힙[objektas_nuoroda] == 21) sritis_CODE = 21;
                int 읽는자리 = 배열칸(objektas_nuoroda, įrašas_padėtis, sritis_CODE); if (!KLAIDA) 넣기(힙[읽는자리], VALUE == 50 ? 2 : 1); continue;
            }
            if (VALUE == 79 || VALUE >= 83 && VALUE <= 86) {
                int įrašas_nuoroda = 빼기(VALUE == 83 ? 2 : 1), įrašas_padėtis = 빼기(1), objektas_nuoroda = 빼기(2), sritis_CODE = VALUE == 79 ? 2 : VALUE == 83 ? 3 : VALUE == 84 ? 20 : VALUE == 85 ? 22 : 23;
                if (VALUE == 84 && objektas_nuoroda > 0 && objektas_nuoroda < 힙끝 && 힙[objektas_nuoroda] == 21) sritis_CODE = 21;
                int 읽는자리 = 배열칸(objektas_nuoroda, įrašas_padėtis, sritis_CODE);
                if (!KLAIDA && sritis_CODE == 3 && !배열저장가능(objektas_nuoroda, įrašas_nuoroda)) continue;
                if (!KLAIDA) 힙[읽는자리] = sritis_CODE == 20 ? (byte)įrašas_nuoroda : sritis_CODE == 21 ? įrašas_nuoroda & 1 : sritis_CODE == 22 ? (char)įrašas_nuoroda : sritis_CODE == 23 ? (short)įrašas_nuoroda : įrašas_nuoroda;
                continue;
            }
            if (VALUE >= 87 && VALUE <= 95) { 스택명령(VALUE); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int SECOND_operandas = 빼기(1), 가 = 빼기(1), REZULTATAS = 0;
                if ((VALUE == 108 || VALUE == 112) && SECOND_operandas == 0) { triktis_VALUE("ArithmeticException: / by zero"); continue; }
                if (VALUE == 96) REZULTATAS = 가 + SECOND_operandas;
                if (VALUE == 100) REZULTATAS = 가 - SECOND_operandas;
                if (VALUE == 104) REZULTATAS = 가 * SECOND_operandas;
                if (VALUE == 108) REZULTATAS = 가 / SECOND_operandas;
                if (VALUE == 112) REZULTATAS = 가 % SECOND_operandas;
                if (VALUE == 120) REZULTATAS = 가 << SECOND_operandas;
                if (VALUE == 122) REZULTATAS = 가 >> SECOND_operandas;
                if (VALUE == 124) REZULTATAS = 가 >>> SECOND_operandas;
                if (VALUE == 126) REZULTATAS = 가 & SECOND_operandas;
                if (VALUE == 128) REZULTATAS = 가 | SECOND_operandas;
                if (VALUE == 130) REZULTATAS = 가 ^ SECOND_operandas;
                넣기(REZULTATAS, 1); continue;
            }
            if (VALUE == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALUE == 132) {
                int vietinis_Aprėptis = 명바(), padidinimas_veiksmas = (byte)명바(); 지역읽기(vietinis_Aprėptis, 1); 넣기(빼기(1) + padidinimas_veiksmas, 1); rašymas_vietinis(vietinis_Aprėptis, 1); continue;
            }
            if (VALUE >= 145 && VALUE <= 147) {
                int numeris = 빼기(1); 넣기(VALUE == 145 ? (byte)numeris : VALUE == 146 ? (char)numeris : (short)numeris, 1); continue;
            }
            if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                int vieta_VALUE = Paleisti + (short)명짧(); boolean 갈까 = VALUE == 167;
                if (VALUE >= 153 && VALUE <= 158) {
                    int numeris = 빼기(1); 갈까 = VALUE == 153 ? numeris == 0 : VALUE == 154 ? numeris != 0 : VALUE == 155 ? numeris < 0 : VALUE == 156 ? numeris >= 0 : VALUE == 157 ? numeris > 0 : numeris <= 0;
                } else if (VALUE >= 159 && VALUE <= 166) {
                    int SECOND_operandas = 빼기(VALUE >= 165 ? 2 : 1), 가 = 빼기(VALUE >= 165 ? 2 : 1);
                    갈까 = VALUE == 159 || VALUE == 165 ? 가 == SECOND_operandas : VALUE == 160 || VALUE == 166 ? 가 != SECOND_operandas : VALUE == 161 ? 가 < SECOND_operandas : VALUE == 162 ? 가 >= SECOND_operandas : VALUE == 163 ? 가 > SECOND_operandas : 가 <= SECOND_operandas;
                } else if (VALUE == 198 || VALUE == 199) { int numeris = 빼기(2); 갈까 = VALUE == 198 ? numeris == 0 : numeris != 0; }
                if (갈까) judėti_VALUE(vieta_VALUE); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { grąžinti_KR(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE >= 178 && VALUE <= 181) { 필드호출(명상수(), VALUE, Paleisti); continue; }
            if (VALUE >= 182 && VALUE <= 185) {
                int 부호값 = 명상수();
                if (VALUE == 185) { int bendras_COUNT = 명바(); if (bendras_COUNT == 0 || 명바() != 0) { triktis_VALUE("invalid invokeinterface operands"); continue; } }
                CALL_metodas(부호값, VALUE); continue;
            }
            if (VALUE == 187) { 새객체(klasės_pavadinimas_SMS(명상수()), Paleisti); continue; }
            if (VALUE == 188 || VALUE == 189) {
                int sritis_CODE = 3, komponentas = 0;
                if (VALUE == 188) { int 임시값 = 명바(); sritis_CODE = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else komponentas = klasės_pavadinimas_SMS(명상수());
                if (sritis_CODE == 0) { triktis_VALUE("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), objektas_nuoroda = priskirti_Saugykla(sritis_CODE, 유효길이); if (!KLAIDA) masyvo_elementas[objektas_nuoroda] = komponentas; 넣기(objektas_nuoroda, 2); continue;
            }
            if (VALUE == 190) {
                int objektas_nuoroda = 빼기(2);
                if (객체유효(objektas_nuoroda)) { int Palyginimas_padėtis = 힙[objektas_nuoroda]; if (Palyginimas_padėtis != 2 && Palyginimas_padėtis != 3 && (Palyginimas_padėtis < 20 || Palyginimas_padėtis > 23)) triktis_VALUE("not an array"); else 넣기(힙[objektas_nuoroda + 1], 1); }
                continue;
            }
            if (VALUE == 191) {
                int objektas_nuoroda = 빼기(2); if (객체유효(objektas_nuoroda)) { if (힙[objektas_nuoroda] != 9) triktis_VALUE("athrow requires supported Throwable"); else { 던진객체 = objektas_nuoroda; KLAIDA = true; } }
                continue;
            }
            if (VALUE == 192 || VALUE == 193) {
                int pavadinimas_konstanta = klasės_pavadinimas_SMS(명상수()), objektas_nuoroda = 빼기(2); boolean MATCH = 맞는객체(objektas_nuoroda, pavadinimas_konstanta);
                if (VALUE == 193) 넣기(objektas_nuoroda != 0 && MATCH ? 1 : 0, 1);
                else { if (!MATCH && !KLAIDA) triktis_VALUE("ClassCastException"); 넣기(objektas_nuoroda, 2); }
                continue;
            }
            if (VALUE == 170 || VALUE == 171) {
                int 읽는자리 = Paleisti + 1, Failas_INDEX = kadras_metodas[kadras_INDEX], Raktas_nuoroda = 빼기(1);
                while ((읽는자리 - metodas_Start[Failas_INDEX]) % 4 != 0) 읽는자리++;
                int tikslas_ADDRESS = padėtis_sveikasis_skaičius(읽는자리);
                if (VALUE == 170) { int 낮은값 = padėtis_sveikasis_skaičius(읽는자리 + 4), 높은값 = padėtis_sveikasis_skaičius(읽는자리 + 8); if (Raktas_nuoroda >= 낮은값 && Raktas_nuoroda <= 높은값) tikslas_ADDRESS = padėtis_sveikasis_skaičius(읽는자리 + 12 + (Raktas_nuoroda - 낮은값) * 4); }
                else { int bendras_COUNT = padėtis_sveikasis_skaičius(읽는자리 + 4); for (int Loop_INDEX = 0; Loop_INDEX < bendras_COUNT; Loop_INDEX++) if (padėtis_sveikasis_skaičius(읽는자리 + 8 + Loop_INDEX * 8) == Raktas_nuoroda) tikslas_ADDRESS = padėtis_sveikasis_skaičius(읽는자리 + 12 + Loop_INDEX * 8); }
                judėti_VALUE(Paleisti + tikslas_ADDRESS); continue;
            }
            if (VALUE == 200) { judėti_VALUE(Paleisti + padėtis_sveikasis_skaičius(Paleisti + 1)); continue; }
            if (VALUE == 194 || VALUE == 195) {
                int objektas_nuoroda = 빼기(2);
                if (VALUE == 195) išleisti_užraktas(objektas_nuoroda);
                else if (!잠금얻기(objektas_nuoroda) && !KLAIDA) { 넣기(objektas_nuoroda, 2); kadras_padėtis[kadras_INDEX] = Paleisti; }
                continue;
            }
            if (VALUE == 196) {
                int komanda_CODE = 명바(), įrašas_padėtis = 명짧();
                if (komanda_CODE == 21 || komanda_CODE == 25) 지역읽기(įrašas_padėtis, komanda_CODE == 21 ? 1 : 2);
                else if (komanda_CODE == 54 || komanda_CODE == 58) rašymas_vietinis(įrašas_padėtis, komanda_CODE == 54 ? 1 : 2);
                else if (komanda_CODE == 132) { int DELTA_VALUE = (short)명짧(); 지역읽기(įrašas_padėtis, 1); 넣기(빼기(1) + DELTA_VALUE, 1); rašymas_vietinis(įrašas_padėtis, 1); }
                else triktis_VALUE("unsupported wide opcode");
                continue;
            }
            triktis_VALUE("unsupported bytecode");
        }
    }
    static int FIND_klasė_Apibrėžtis(int Pavadinimas_2) {
        for (int Loop_INDEX = 0; Loop_INDEX < klasė_Apibrėžtis_COUNT; Loop_INDEX++) if (klasė_Apibrėžtis_pavadinimas[Loop_INDEX] != 0 && 같은말(klasė_Apibrėžtis_pavadinimas[Loop_INDEX], Pavadinimas_2)) return Loop_INDEX;
        return įkelti_klasė_Apibrėžtis(konstanta_SMS(Pavadinimas_2));
    }
    static int įkelti_klasė_Apibrėžtis(int pavadinimas_eilutė) {
        if (!objektas_VALUE(pavadinimas_eilutė, 1)) return -1;
        int 길이 = 힙[pavadinimas_eilutė + 1];
        if (길이 < 1 || 길이 > 505 || klasė_Apibrėžtis_COUNT == 16) { triktis_VALUE("class name/count limit"); return -1; }
        for (int Loop_INDEX = 0; Loop_INDEX < 길이; Loop_INDEX++) { int simbolio_kodas = 힙[pavadinimas_eilutė + 2 + Loop_INDEX]; failo_vardas_SMS[Loop_INDEX] = simbolio_kodas == '/' ? '.' : simbolio_kodas; }
        failo_vardas_SMS[길이] = '.'; failo_vardas_SMS[길이 + 1] = 'c'; failo_vardas_SMS[길이 + 2] = 'l'; failo_vardas_SMS[길이 + 3] = 'a'; failo_vardas_SMS[길이 + 4] = 's'; failo_vardas_SMS[길이 + 5] = 's'; failo_vardas_SMS[길이 + 6] = 0;
        int Dydis = naudotojas.파일읽기(failo_vardas_SMS, laikinasis_failas);
        if (Dydis < 0) { triktis_VALUE("ClassNotFoundException"); return -1; }
        int klasė_Apibrėžtis = klasė_Apibrėžtis_COUNT++; klasė_Apibrėžtis_dydis[klasė_Apibrėžtis] = Dydis;
        for (int Loop_INDEX = 0; Loop_INDEX < Dydis; Loop_INDEX++) Failas[klasė_Apibrėžtis * 16384 + Loop_INDEX] = laikinasis_failas[Loop_INDEX];
        클래스읽기(klasė_Apibrėžtis); if (KLAIDA) return -1;
        int faktinis_duomenys = konstanta_SMS(klasė_Apibrėžtis_pavadinimas[klasė_Apibrėžtis]);
        if (!글같음(faktinis_duomenys, pavadinimas_eilutė, true)) { triktis_VALUE("class name does not match file"); return -1; }
        int pirminis_VALUE = klasė_Apibrėžtis_pirminis[klasė_Apibrėžtis];
        if (pirminis_VALUE != 0 && !Word_SMS(pirminis_VALUE, "java/lang/Object") && !Word_SMS(pirminis_VALUE, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 kartoti_VALUE 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = FIND_klasė_Apibrėžtis(pirminis_VALUE);
            if (KLAIDA || 위 < 0) return -1;
            int 읽는자리 = 위, etapas_COUNT = 0;
            while (읽는자리 >= 0 && etapas_COUNT++ < 16) {
                if (읽는자리 == klasė_Apibrėžtis) { triktis_VALUE("cyclic inheritance"); return -1; }
                읽는자리 = pirminis_klasė(읽는자리);
            }
            int 시작변위 = 종칸수[위];
            for (int Failas_INDEX = 0; Failas_INDEX < 칸수; Failas_INDEX++) if (칸주인[Failas_INDEX] == klasė_Apibrėžtis && (칸권한[Failas_INDEX] & 8) == 0) 칸위치[Failas_INDEX] += 시작변위;
            종칸수[klasė_Apibrėžtis] += 시작변위;
        }
        return klasė_Apibrėžtis;
    }
    static int pirminis_klasė(int klasė_Apibrėžtis) {
        int Pavadinimas_2 = klasė_Apibrėžtis_pirminis[klasė_Apibrėžtis];
        for (int Loop_INDEX = 0; Loop_INDEX < klasė_Apibrėžtis_COUNT; Loop_INDEX++) if (Pavadinimas_2 != 0 && klasė_Apibrėžtis_pavadinimas[Loop_INDEX] != 0 && 같은말(klasė_Apibrėžtis_pavadinimas[Loop_INDEX], Pavadinimas_2)) return Loop_INDEX;
        return -1;
    }
    static int FIND_metodas(int klasė_Apibrėžtis, int Pavadinimas_2, int formatas_VALUE) {
        for (int 깊이 = 0; klasė_Apibrėžtis >= 0 && 깊이 < 16; 깊이++, klasė_Apibrėžtis = pirminis_klasė(klasė_Apibrėžtis)) {
            for (int Loop_INDEX = 0; Loop_INDEX < metodas_COUNT; Loop_INDEX++) if (metodas_savininkas[Loop_INDEX] == klasė_Apibrėžtis && 같은말(metodas_pavadinimas_SMS[Loop_INDEX], Pavadinimas_2) && 같은말(metodas_TYPE[Loop_INDEX], formatas_VALUE)) return Loop_INDEX;
        }
        return -1;
    }
    static int pavadinimas_metodas(int klasė_Apibrėžtis, String Pavadinimas_2, String formatas_VALUE) {
        for (int 깊이 = 0; klasė_Apibrėžtis >= 0 && 깊이 < 16; 깊이++, klasė_Apibrėžtis = pirminis_klasė(klasė_Apibrėžtis))
            for (int Loop_INDEX = 0; Loop_INDEX < metodas_COUNT; Loop_INDEX++) if (metodas_savininkas[Loop_INDEX] == klasė_Apibrėžtis && Word_SMS(metodas_pavadinimas_SMS[Loop_INDEX], Pavadinimas_2) && Word_SMS(metodas_TYPE[Loop_INDEX], formatas_VALUE)) return Loop_INDEX;
        return -1;
    }
    static int 형종류(int Pavadinimas_2) { return Failas[상가[Pavadinimas_2]] == 'L' || Failas[상가[Pavadinimas_2]] == '[' ? 2 : 1; }
    static boolean 초기화(int klasė_Apibrėžtis, int komanda_Start) {
        if (klasė_Apibrėžtis < 0 || KLAIDA) return false;
        if (klasė_Apibrėžtis_Būsena[klasė_Apibrėžtis] == 3) { triktis_VALUE("NoClassDefFoundError: initialization failed"); return false; }
        if (klasė_Apibrėžtis_Būsena[klasė_Apibrėžtis] == 1 && klasė_gija[klasė_Apibrėžtis] != dabartinis_gija) { kadras_padėtis[kadras_INDEX] = komanda_Start; keisti_užklausa = true; return false; }
        if (klasė_Apibrėžtis_Būsena[klasė_Apibrėžtis] != 0) return true;
        int 위 = pirminis_klasė(klasė_Apibrėžtis);
        if (위 >= 0 && !초기화(위, komanda_Start)) return false;
        klasė_Apibrėžtis_Būsena[klasė_Apibrėžtis] = 1; klasė_gija[klasė_Apibrėžtis] = dabartinis_gija;
        if (종초기화[klasė_Apibrėžtis] != 0) {
            kadras_padėtis[kadras_INDEX] = komanda_Start;
            호출(종초기화[klasė_Apibrėžtis] - 1); if (!KLAIDA) 틀초기화[kadras_INDEX] = klasė_Apibrėžtis + 1;
            return false;
        }
        klasė_Apibrėžtis_Būsena[klasė_Apibrėžtis] = 2; return true;
    }
    static void 필드호출(int INDEX, int Komanda, int Paleisti) {
        if (!čekis_konstanta(INDEX, 9)) return;
        int savininkas_VALUE = klasės_pavadinimas_SMS(상가[INDEX]), Pavadinimas_2 = nuoroda_pavadinimas(konstanta_SECOND_VALUE[INDEX]), formatas_VALUE = nuoroda_TYPE(konstanta_SECOND_VALUE[INDEX]);
        if (Word_SMS(savininkas_VALUE, "java/lang/System") && (Word_SMS(Pavadinimas_2, "out") || Word_SMS(Pavadinimas_2, "err")) && Word_SMS(formatas_VALUE, "Ljava/io/PrintStream;") && Komanda == 178) { 넣기(-1, 2); return; }
        int klasė_Apibrėžtis = FIND_klasė_Apibrėžtis(savininkas_VALUE); if (klasė_Apibrėžtis < 0 || KLAIDA) return;
        int 찾음 = -1;
        for (int 읽는자리 = klasė_Apibrėžtis, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = pirminis_klasė(읽는자리))
            for (int Failas_INDEX = 0; Failas_INDEX < 칸수; Failas_INDEX++) if (칸주인[Failas_INDEX] == 읽는자리 && 같은말(칸이름[Failas_INDEX], Pavadinimas_2) && 같은말(칸형[Failas_INDEX], formatas_VALUE)) 찾음 = Failas_INDEX;
        if (찾음 < 0) { triktis_VALUE("NoSuchFieldError"); return; }
        boolean 정적 = Komanda == 178 || Komanda == 179;
        if (정적 != ((칸권한[찾음] & 8) != 0)) { triktis_VALUE("field static/instance mismatch"); return; }
        if (정적 && !초기화(칸주인[찾음], Paleisti)) return;
        int TYPE_VALUE = 형종류(formatas_VALUE), VALUE = 0;
        if (Komanda == 179 || Komanda == 181) VALUE = 빼기(TYPE_VALUE);
        if (정적) { if (Komanda == 178) 넣기(칸값[찾음], TYPE_VALUE); else if (!KLAIDA) 칸값[찾음] = VALUE; return; }
        int objektas_nuoroda = 빼기(2);
        if (!객체유효(objektas_nuoroda)) return;
        if (힙[objektas_nuoroda] < 32 || !종포함(힙[objektas_nuoroda] - 32, savininkas_VALUE)) { triktis_VALUE("field receiver type mismatch"); return; }
        int 보관칸 = objektas_nuoroda + 2 + 칸위치[찾음];
        if (Komanda == 180) 넣기(힙[보관칸], TYPE_VALUE);
        else if (!KLAIDA) { 힙[보관칸] = VALUE; 힙참조[보관칸] = TYPE_VALUE == 2 ? 1 : 0; }
    }
    static boolean 종포함(int klasė_Apibrėžtis, int Pavadinimas_2) {
        for (int 중첩깊이 = 0; klasė_Apibrėžtis >= 0 && 중첩깊이 < 16; 중첩깊이++, klasė_Apibrėžtis = pirminis_klasė(klasė_Apibrėžtis)) {
            if (같은말(klasė_Apibrėžtis_pavadinimas[klasė_Apibrėžtis], Pavadinimas_2) || (klasė_Apibrėžtis_pirminis[klasė_Apibrėžtis] != 0 && 같은말(klasė_Apibrėžtis_pirminis[klasė_Apibrėžtis], Pavadinimas_2))) return true;
            for (int vidinis_padėtis = 0; vidinis_padėtis < klasė_sąsaja_COUNT[klasė_Apibrėžtis]; vidinis_padėtis++) if (같은말(klasė_sąsaja[klasė_Apibrėžtis * 16 + vidinis_padėtis], Pavadinimas_2)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int baitas_duomenys, boolean KELIAS) {
        if (첫값 == baitas_duomenys) return true;
        if (첫값 <= 0 || baitas_duomenys <= 0 || 힙[첫값] != 1 || 힙[baitas_duomenys] != 1 || 힙[첫값 + 1] != 힙[baitas_duomenys + 1]) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) {
            int x_koordinatė = 힙[첫값 + 2 + Loop_INDEX], 세로좌표 = 힙[baitas_duomenys + 2 + Loop_INDEX];
            if (KELIAS) { if (x_koordinatė == '.') x_koordinatė = '/'; if (세로좌표 == '.') 세로좌표 = '/'; }
            if (x_koordinatė != 세로좌표) return false;
        }
        return true;
    }
    static boolean 객체유효(int objektas_nuoroda) {
        if (objektas_nuoroda == 0) { triktis_VALUE("NullPointerException"); return false; }
        if (objektas_nuoroda < 1 || objektas_nuoroda >= 힙끝 || 힙폭[objektas_nuoroda] < 2 || 힙[objektas_nuoroda] == 0) { triktis_VALUE("invalid object reference"); return false; }
        return true;
    }
    static void apsaugoti_VALUE(int objektas_nuoroda) {
        if (objektas_nuoroda > 0 && objektas_nuoroda < 힙끝 && 힙폭[objektas_nuoroda] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = objektas_nuoroda;
    }
    static void laida_VALUE(int objektas_nuoroda) {
        if (objektas_nuoroda > 0 && objektas_nuoroda < 힙끝 && 힙폭[objektas_nuoroda] >= 2 && 힙[objektas_nuoroda] != 0 && 힙표시[objektas_nuoroda] == 0) {
            힙표시[objektas_nuoroda] = 1; 표시대기[rodyti_COUNT++] = objektas_nuoroda;
        }
    }
    static void 수거() {
        rodyti_COUNT = 0; aibė_COUNT++;
        for (int čekis_padėtis = 1; čekis_padėtis < 힙끝; čekis_padėtis += 힙폭[čekis_padėtis]) 힙표시[čekis_padėtis] = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < eilutė_nuoroda.length; Loop_INDEX++) laida_VALUE(eilutė_nuoroda[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 칸수; Loop_INDEX++) if ((칸권한[Loop_INDEX] & 8) != 0 && 형종류(칸형[Loop_INDEX]) == 2) laida_VALUE(칸값[Loop_INDEX]);
        for (int 임시값 = 0; 임시값 < gija_COUNT; 임시값++) {
            laida_VALUE(gija_objektas[임시값]); laida_VALUE(gija_tikslas[임시값]);
            int 꼭대기자리 = 임시값 == dabartinis_gija ? kadras_INDEX : gija_kadras[임시값];
            for (int Failas_INDEX = 임시값 * 32; Failas_INDEX <= 꼭대기자리; Failas_INDEX++) {
                for (int vidinis_padėtis = 0; vidinis_padėtis < 함수지역[kadras_metodas[Failas_INDEX]]; vidinis_padėtis++) if (vietinis_TYPE[Failas_INDEX * 128 + vidinis_padėtis] == 2) laida_VALUE(vietinis_VALUE[Failas_INDEX * 128 + vidinis_padėtis]);
                for (int vidinis_padėtis = 0; vidinis_padėtis < kadras_eilė[Failas_INDEX]; vidinis_padėtis++) if (operandas_eilė_TYPE[Failas_INDEX * 128 + vidinis_padėtis] == 2) laida_VALUE(operandas_eilė_VALUE[Failas_INDEX * 128 + vidinis_padėtis]);
            }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 화면참조.length; Loop_INDEX++) laida_VALUE(화면참조[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 나중수; Loop_INDEX++) laida_VALUE(나중실행[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Store_sveikasis_skaičius.length; Loop_INDEX++) laida_VALUE(Store_sveikasis_skaičius[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < klasė_Apibrėžtis_COUNT; Loop_INDEX++) laida_VALUE(klasė_užraktas[Loop_INDEX]);
        for (int čekis_padėtis = 1; čekis_padėtis < 힙끝; čekis_padėtis += 힙폭[čekis_padėtis]) if (잠금깊이[čekis_padėtis] > 0) laida_VALUE(čekis_padėtis);
        laida_VALUE(던진객체);
        for (int Loop_INDEX = 0; Loop_INDEX < 잠시수; Loop_INDEX++) laida_VALUE(잠시참조[Loop_INDEX]);
        while (rodyti_COUNT > 0) {
            int objektas_nuoroda = 표시대기[--rodyti_COUNT], sritis_CODE = 힙[objektas_nuoroda];
            for (int Loop_INDEX = objektas_nuoroda + 2; Loop_INDEX < objektas_nuoroda + 힙폭[objektas_nuoroda]; Loop_INDEX++) if (sritis_CODE == 3 || sritis_CODE == 4 || 힙참조[Loop_INDEX] != 0) laida_VALUE(힙[Loop_INDEX]);
        }
        for (int čekis_padėtis = 1; čekis_padėtis < 힙끝; čekis_padėtis += 힙폭[čekis_padėtis]) if (힙표시[čekis_padėtis] == 0) 힙[čekis_padėtis] = 0;
        for (int čekis_padėtis = 1; čekis_padėtis < 힙끝; čekis_padėtis += 힙폭[čekis_padėtis]) if (힙[čekis_padėtis] == 0) {
            while (čekis_padėtis + 힙폭[čekis_padėtis] < 힙끝 && 힙[čekis_padėtis + 힙폭[čekis_padėtis]] == 0) { int toliau_padėtis = čekis_padėtis + 힙폭[čekis_padėtis]; 힙폭[čekis_padėtis] += 힙폭[toliau_padėtis]; 힙폭[toliau_padėtis] = 0; }
            if (čekis_padėtis + 힙폭[čekis_padėtis] == 힙끝) { 힙끝 = čekis_padėtis; break; }
        }
    }
    static int 새기억(int 종류, int 길이) {
        if (길이 < 0) { triktis_VALUE("NegativeArraySizeException"); return 0; }
        if (길이 > 힙.length - 3) { triktis_VALUE("object heap exhausted"); return 0; }
        int 필요수 = 길이 + 2, objektas_nuoroda = 0;
        if (필요수 <= 힙.length - 힙끝) { objektas_nuoroda = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { objektas_nuoroda = 읽는자리; break; }
            if (objektas_nuoroda != 0) {
                int 남은길이 = 힙폭[objektas_nuoroda] - 필요수;
                if (남은길이 >= 2) { 힙폭[objektas_nuoroda + 필요수] = 남은길이; 힙[objektas_nuoroda + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { objektas_nuoroda = 힙끝; 힙끝 += 필요수; }
        }
        if (objektas_nuoroda == 0) { triktis_VALUE("object heap exhausted"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < 필요수; Loop_INDEX++) { 힙[objektas_nuoroda + Loop_INDEX] = 0; 힙참조[objektas_nuoroda + Loop_INDEX] = 0; 힙폭[objektas_nuoroda + Loop_INDEX] = 0; }
        masyvo_elementas[objektas_nuoroda] = 0;
        힙폭[objektas_nuoroda] = 필요수; 힙[objektas_nuoroda] = 종류; 힙[objektas_nuoroda + 1] = 길이; apsaugoti_VALUE(objektas_nuoroda); return objektas_nuoroda;
    }
    static int išimtis_klasė(String pavadinimas_konstanta) {
        if (자바도구.같음(pavadinimas_konstanta, "java/lang/Throwable")) return 1;
        if (자바도구.같음(pavadinimas_konstanta, "java/lang/Exception")) return 2;
        if (자바도구.같음(pavadinimas_konstanta, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(pavadinimas_konstanta, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(pavadinimas_konstanta, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(pavadinimas_konstanta, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(pavadinimas_konstanta, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(pavadinimas_konstanta, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(pavadinimas_konstanta, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(pavadinimas_konstanta, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(pavadinimas_konstanta, "java/io/IOException")) return 11;
        if (자바도구.같음(pavadinimas_konstanta, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(pavadinimas_konstanta, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(pavadinimas_konstanta, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(pavadinimas_konstanta, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int išimtis_konstanta(int Pavadinimas_2) {
        for (int Loop_INDEX = 1; Loop_INDEX <= 41; Loop_INDEX++) if (Word_SMS(Pavadinimas_2, išimtis_pavadinimas(Loop_INDEX))) return Loop_INDEX;
        return 0;
    }
    static String išimtis_pavadinimas(int paskyra_VALUE) {
        if (paskyra_VALUE == 40) return "java/lang/InterruptedException";
        if (paskyra_VALUE == 41) return "Lietuvių/savas/대기중단예외";
        if (paskyra_VALUE == 39) return "java/net/SocketException";
        if (paskyra_VALUE == 20) return "Lietuvių/savas/išimtis";
        if (paskyra_VALUE == 21) return "Lietuvių/savas/실행예외";
        if (paskyra_VALUE == 22) return "Lietuvių/savas/Į_I_išimtis";
        if (paskyra_VALUE == 23) return "Lietuvių/savas/Palauk_SKIRTASIS_LAIKAS_išimtis";
        if (paskyra_VALUE == 24) return "Lietuvių/savas/ADDRESS_LOOKUP_išimtis";
        if (paskyra_VALUE == 25) return "Lietuvių/savas/파일없음예외";
        if (paskyra_VALUE == 26) return "Lietuvių/savas/통신예외";
        if (paskyra_VALUE == 27) return "Lietuvių/savas/neleistinas_argumentas_išimtis";
        if (paskyra_VALUE == 28) return "Lietuvių/savas/numeris_formatas_triktis";
        if (paskyra_VALUE == 29) return "Lietuvių/savas/범위예외";
        if (paskyra_VALUE == 30) return "Lietuvių/savas/배열범위예외";
        if (paskyra_VALUE == 31) return "Lietuvių/savas/문자열범위예외";
        if (paskyra_VALUE == 32) return "Lietuvių/savas/NULL_nuoroda_išimtis";
        if (paskyra_VALUE == 33) return "Lietuvių/savas/산술예외";
        if (paskyra_VALUE == 34) return "Lietuvių/savas/Būsena_išimtis";
        if (paskyra_VALUE == 35) return "Lietuvių/savas/TYPE_perduoti_išimtis";
        if (paskyra_VALUE == 36) return "Lietuvių/savas/음수배열크기예외";
        if (paskyra_VALUE == 37) return "Lietuvių/savas/ARRAY_Store_triktis";
        if (paskyra_VALUE == 38) return "Lietuvių/savas/gija_Būsena_išimtis";
        if (paskyra_VALUE == 1) return "java/lang/Throwable"; if (paskyra_VALUE == 2) return "java/lang/Exception";
        if (paskyra_VALUE == 3) return "java/lang/RuntimeException"; if (paskyra_VALUE == 4) return "java/lang/ArithmeticException";
        if (paskyra_VALUE == 5) return "java/lang/NullPointerException"; if (paskyra_VALUE == 6) return "java/lang/IndexOutOfBoundsException";
        if (paskyra_VALUE == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (paskyra_VALUE == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (paskyra_VALUE == 9) return "java/lang/IllegalArgumentException"; if (paskyra_VALUE == 10) return "java/lang/NumberFormatException";
        if (paskyra_VALUE == 11) return "java/io/IOException"; if (paskyra_VALUE == 12) return "java/io/FileNotFoundException";
        if (paskyra_VALUE == 17) return "java/lang/ArrayStoreException";
        if (paskyra_VALUE == 18) return "java/net/UnknownHostException";
        if (paskyra_VALUE == 19) return "java/net/SocketTimeoutException";
        if (paskyra_VALUE == 16) return "java/lang/IllegalThreadStateException";
        if (paskyra_VALUE == 13) return "java/lang/IllegalStateException"; if (paskyra_VALUE == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int išimtis_pirminis(int paskyra_VALUE) {
        if (paskyra_VALUE == 40) return 2;
        if (paskyra_VALUE == 41) return 40;
        if (paskyra_VALUE == 39) return 11;
        if (paskyra_VALUE == 1) return 0;
        if (paskyra_VALUE == 2) return 1;
        if (paskyra_VALUE == 3) return 2;
        if (paskyra_VALUE == 4) return 3;
        if (paskyra_VALUE == 5) return 3;
        if (paskyra_VALUE == 6) return 3;
        if (paskyra_VALUE == 7) return 6;
        if (paskyra_VALUE == 8) return 6;
        if (paskyra_VALUE == 9) return 3;
        if (paskyra_VALUE == 10) return 9;
        if (paskyra_VALUE == 11) return 2;
        if (paskyra_VALUE == 12) return 11;
        if (paskyra_VALUE == 13) return 3;
        if (paskyra_VALUE == 14) return 3;
        if (paskyra_VALUE == 15) return 3;
        if (paskyra_VALUE == 16) return 9;
        if (paskyra_VALUE == 17) return 3;
        if (paskyra_VALUE == 18) return 11;
        if (paskyra_VALUE == 19) return 11;
        if (paskyra_VALUE == 20) return 2;
        if (paskyra_VALUE == 21) return 3;
        if (paskyra_VALUE == 22) return 11;
        if (paskyra_VALUE == 23) return 22;
        if (paskyra_VALUE == 24) return 22;
        if (paskyra_VALUE == 25) return 22;
        if (paskyra_VALUE == 26) return 22;
        if (paskyra_VALUE == 27) return 9;
        if (paskyra_VALUE == 28) return 27;
        if (paskyra_VALUE == 29) return 6;
        if (paskyra_VALUE == 30) return 29;
        if (paskyra_VALUE == 31) return 29;
        if (paskyra_VALUE == 32) return 5;
        if (paskyra_VALUE == 33) return 4;
        if (paskyra_VALUE == 34) return 13;
        if (paskyra_VALUE == 35) return 14;
        if (paskyra_VALUE == 36) return 15;
        if (paskyra_VALUE == 37) return 17;
        if (paskyra_VALUE == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int faktinė_reikšmė, int 요구값) {
        for (int 깊이 = 0; faktinė_reikšmė != 0 && 깊이 < 16; 깊이++, faktinė_reikšmė = išimtis_pirminis(faktinė_reikšmė))
            if (faktinė_reikšmė == 요구값) return true;
        return false;
    }
    static void 예외던짐(int paskyra_VALUE, String 안내참조) {
        int objektas_nuoroda = 새기억(9, 2); if (KLAIDA) return;
        힙[objektas_nuoroda + 2] = paskyra_VALUE; 힙[objektas_nuoroda + 3] = organizuoti_simbolis(안내참조); 힙참조[objektas_nuoroda + 3] = 1;
        던진객체 = objektas_nuoroda; KLAIDA = true;
    }
    static boolean 맞는객체(int objektas_nuoroda, int Pavadinimas_2) {
        if (objektas_nuoroda == 0) return true;
        if (!객체유효(objektas_nuoroda)) return false;
        int sritis_CODE = 힙[objektas_nuoroda];
        if (Word_SMS(Pavadinimas_2, "java/lang/Object")) return true;
        if (sritis_CODE >= 32) return 종포함(sritis_CODE - 32, Pavadinimas_2);
        if (sritis_CODE == 9) { int tikslas_ADDRESS = išimtis_konstanta(Pavadinimas_2); return tikslas_ADDRESS != 0 && 예외포함(힙[objektas_nuoroda + 2], tikslas_ADDRESS); }
        if (sritis_CODE == 1) return Word_SMS(Pavadinimas_2, "java/lang/String") || Word_SMS(Pavadinimas_2, "java/lang/CharSequence");
        if (sritis_CODE == 4) return Word_SMS(Pavadinimas_2, "java/lang/StringBuilder") || Word_SMS(Pavadinimas_2, "java/lang/CharSequence");
        if (sritis_CODE == 10) return Word_SMS(Pavadinimas_2, "java/util/ArrayList") || Word_SMS(Pavadinimas_2, "java/util/List");
        if (sritis_CODE == 11) return Word_SMS(Pavadinimas_2, "java/util/HashMap") || Word_SMS(Pavadinimas_2, "java/util/Map");
        if (sritis_CODE == 12) return Word_SMS(Pavadinimas_2, "java/lang/Integer") || Word_SMS(Pavadinimas_2, "java/lang/Number");
        if (sritis_CODE >= 24 && sritis_CODE <= 28 && 힙[objektas_nuoroda + 13] != 0) return 한국어화면종(Pavadinimas_2) == sritis_CODE || Word_SMS(Pavadinimas_2, "Lietuvių/savas/화면구성요소");
        if (sritis_CODE >= 24 && sritis_CODE <= 28) return (한국어화면종(Pavadinimas_2) == 0 && 화면종(Pavadinimas_2) == sritis_CODE) || Word_SMS(Pavadinimas_2, "java/awt/Component") || Word_SMS(Pavadinimas_2, "java/awt/Container") || Word_SMS(Pavadinimas_2, "javax/swing/JComponent");
        if (sritis_CODE == 29) return Word_SMS(Pavadinimas_2, 힙[objektas_nuoroda + 3] != 0 ? "Lietuvių/savas/gavinys_pranešimas" : "java/awt/event/ActionEvent");
        if (sritis_CODE == 30) return Word_SMS(Pavadinimas_2, "java/awt/FlowLayout") || Word_SMS(Pavadinimas_2, "java/awt/LayoutManager");
        if (sritis_CODE == 17) return Word_SMS(Pavadinimas_2, "java/net/Socket");
        if (sritis_CODE == 18) return Word_SMS(Pavadinimas_2, "java/net/ServerSocket");
        if (sritis_CODE == 19) return Word_SMS(Pavadinimas_2, 힙[objektas_nuoroda + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (sritis_CODE == 14) return Word_SMS(Pavadinimas_2, "java/net/InetAddress");
        if (sritis_CODE == 15) return Word_SMS(Pavadinimas_2, "java/net/DatagramSocket");
        if (sritis_CODE == 16) return Word_SMS(Pavadinimas_2, "java/net/DatagramPacket");
        if (sritis_CODE == 13) return Word_SMS(Pavadinimas_2, 힙[objektas_nuoroda + 3] != 0 ? "Lietuvių/savas/darbininkas" : "java/lang/Thread");
        if (sritis_CODE == 2) return Word_SMS(Pavadinimas_2, "[I"); if (sritis_CODE == 20) return Word_SMS(Pavadinimas_2, "[B"); if (sritis_CODE == 21) return Word_SMS(Pavadinimas_2, "[Z");
        if (sritis_CODE == 22) return Word_SMS(Pavadinimas_2, "[C"); if (sritis_CODE == 23) return Word_SMS(Pavadinimas_2, "[S");
        if (sritis_CODE != 3) return false;
        if (Word_SMS(Pavadinimas_2, "[Ljava/lang/Object;")) return true;
        int komponentas = masyvo_elementas[objektas_nuoroda];
        if (komponentas == -1) return Word_SMS(Pavadinimas_2, "[Ljava/lang/String;") || Word_SMS(Pavadinimas_2, "[Ljava/lang/CharSequence;");
        if (komponentas == 0) return false;
        if (배열종비교(komponentas, Pavadinimas_2)) return true;
        if ((Word_SMS(komponentas, "java/lang/String") || Word_SMS(komponentas, "java/lang/StringBuilder")) && Word_SMS(Pavadinimas_2, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDEX = 0; Loop_INDEX < klasė_Apibrėžtis_COUNT; Loop_INDEX++) if (같은말(klasė_Apibrėžtis_pavadinimas[Loop_INDEX], komponentas)) {
            for (int simbolio_kodas = Loop_INDEX, 중첩깊이 = 0; simbolio_kodas >= 0 && 중첩깊이 < 16; 중첩깊이++, simbolio_kodas = pirminis_klasė(simbolio_kodas)) {
                if (배열종비교(klasė_Apibrėžtis_pirminis[simbolio_kodas], Pavadinimas_2)) return true;
                for (int vidinis_padėtis = 0; vidinis_padėtis < klasė_sąsaja_COUNT[simbolio_kodas]; vidinis_padėtis++) if (배열종비교(klasė_sąsaja[simbolio_kodas * 16 + vidinis_padėtis], Pavadinimas_2)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int pavadinimas_konstanta, int 형식참조) {
        int čekis_padėtis = 상가[형식참조], įrašas_COUNT = konstanta_SECOND_VALUE[형식참조];
        if (pavadinimas_konstanta == 0 || įrašas_COUNT < 4 || Failas[čekis_padėtis] != '[' || Failas[čekis_padėtis + 1] != 'L' || Failas[čekis_padėtis + įrašas_COUNT - 1] != ';' || konstanta_SECOND_VALUE[pavadinimas_konstanta] != įrašas_COUNT - 3) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < įrašas_COUNT - 3; Loop_INDEX++) if (Failas[상가[pavadinimas_konstanta] + Loop_INDEX] != Failas[čekis_padėtis + 2 + Loop_INDEX]) return false;
        return true;
    }
    static void rodyklė_išimtis() {
        if (던진객체 == 0) return;
        KLAIDA = false;
        while (kadras_INDEX >= dabartinis_gija * 32) {
            int Failas_INDEX = kadras_metodas[kadras_INDEX], 읽는자리 = 틀명령[kadras_INDEX];
            for (int Loop_INDEX = 0; Loop_INDEX < 잡기수; Loop_INDEX++) if (잡기함수[Loop_INDEX] == Failas_INDEX && 읽는자리 >= 잡기시작[Loop_INDEX] && 읽는자리 < 잡기끝[Loop_INDEX]
                && (잡기종[Loop_INDEX] == 0 || 맞는객체(던진객체, 잡기종[Loop_INDEX]))) {
                kadras_padėtis[kadras_INDEX] = 잡기위치[Loop_INDEX]; kadras_eilė[kadras_INDEX] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (틀초기화[kadras_INDEX] != 0) klasė_Apibrėžtis_Būsena[틀초기화[kadras_INDEX] - 1] = 3;
            if (kadras_užraktas[kadras_INDEX] != 0) { išleisti_užraktas(kadras_užraktas[kadras_INDEX]); kadras_užraktas[kadras_INDEX] = 0; }
            kadras_INDEX--;
        }
        naudotojas.Rašymas("Uncaught ");
        if (힙[던진객체] == 9) { naudotojas.Rašymas(išimtis_pavadinimas(힙[던진객체 + 2])); naudotojas.Rašymas(": "); rašymas_SMS(힙[던진객체 + 3]); }
        else naudotojas.Rašymas("user exception");
        naudotojas.rašymas_simbolis_VALUE(10); 던진객체 = 0; KLAIDA = true;
    }
    // 이 JVM의 operandas_eilė 항목은 dabartinis_prekė category-1(int/reference)만 허용한다.
    static void 스택명령(int komanda_CODE) {
        int 첫값 = 빼기(0), 첫형식 = grąžinti_TYPE;
        if (komanda_CODE == 87) return;
        if (komanda_CODE == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int baitas_duomenys = 빼기(0), SECOND_formatas = grąžinti_TYPE;
        if (komanda_CODE == 88) return;
        if (komanda_CODE == 90) { 넣기(첫값, 첫형식); 넣기(baitas_duomenys, SECOND_formatas); 넣기(첫값, 첫형식); return; }
        if (komanda_CODE == 92) { 넣기(baitas_duomenys, SECOND_formatas); 넣기(첫값, 첫형식); 넣기(baitas_duomenys, SECOND_formatas); 넣기(첫값, 첫형식); return; }
        if (komanda_CODE == 95) { 넣기(첫값, 첫형식); 넣기(baitas_duomenys, SECOND_formatas); return; }
        int simbolio_kodas = 빼기(0), 셋째형식 = grąžinti_TYPE;
        if (komanda_CODE == 91) { 넣기(첫값, 첫형식); 넣기(simbolio_kodas, 셋째형식); 넣기(baitas_duomenys, SECOND_formatas); 넣기(첫값, 첫형식); return; }
        if (komanda_CODE == 93) { 넣기(baitas_duomenys, SECOND_formatas); 넣기(첫값, 첫형식); 넣기(simbolio_kodas, 셋째형식); 넣기(baitas_duomenys, SECOND_formatas); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = grąžinti_TYPE;
        넣기(baitas_duomenys, SECOND_formatas); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(simbolio_kodas, 셋째형식); 넣기(baitas_duomenys, SECOND_formatas); 넣기(첫값, 첫형식);
    }
    static void 새객체(int pavadinimas_konstanta, int 시작점) {
        int sritis_CODE = 0, 유효길이 = 0, išimtis_nuoroda = išimtis_konstanta(pavadinimas_konstanta);
        if (Word_SMS(pavadinimas_konstanta, "java/lang/StringBuilder")) { sritis_CODE = 4; 유효길이 = 1; }
        if (Word_SMS(pavadinimas_konstanta, "java/io/FileInputStream")) { sritis_CODE = 5; 유효길이 = 2; }
        if (Word_SMS(pavadinimas_konstanta, "java/io/FileOutputStream")) { sritis_CODE = 6; 유효길이 = 2; }
        if (išimtis_nuoroda != 0) { sritis_CODE = 9; 유효길이 = 2; }
        if (Word_SMS(pavadinimas_konstanta, "java/util/ArrayList")) { sritis_CODE = 10; 유효길이 = 2; }
        if (Word_SMS(pavadinimas_konstanta, "java/util/HashMap")) { sritis_CODE = 11; 유효길이 = 2; }
        if (Word_SMS(pavadinimas_konstanta, "java/lang/Integer")) { sritis_CODE = 12; 유효길이 = 1; }
        if (Word_SMS(pavadinimas_konstanta, "java/net/Socket")) { sritis_CODE = 17; 유효길이 = 5; }
        if (Word_SMS(pavadinimas_konstanta, "java/net/ServerSocket")) { sritis_CODE = 18; 유효길이 = 5; }
        if (Word_SMS(pavadinimas_konstanta, "java/net/DatagramSocket")) { sritis_CODE = 15; 유효길이 = 3; }
        if (Word_SMS(pavadinimas_konstanta, "java/net/DatagramPacket")) { sritis_CODE = 16; 유효길이 = 4; }
        if (Word_SMS(pavadinimas_konstanta, "java/lang/Thread") || Word_SMS(pavadinimas_konstanta, "Lietuvių/savas/darbininkas")) { sritis_CODE = 13; 유효길이 = 2; }
        if (Word_SMS(pavadinimas_konstanta, "java/lang/Object")) { sritis_CODE = 8; }
        if (sritis_CODE == 0 && 화면종(pavadinimas_konstanta) != 0) { sritis_CODE = 화면종(pavadinimas_konstanta); 유효길이 = 12; }
        if (sritis_CODE == 0) {
            int simbolio_kodas = FIND_klasė_Apibrėžtis(pavadinimas_konstanta); if (simbolio_kodas < 0 || KLAIDA || !초기화(simbolio_kodas, 시작점)) return;
            sritis_CODE = 32 + simbolio_kodas; 유효길이 = 종칸수[simbolio_kodas];
        }
        int objektas_nuoroda = priskirti_Saugykla(sritis_CODE, 유효길이); if (KLAIDA) return;
        if (sritis_CODE == 13 && Word_SMS(pavadinimas_konstanta, "Lietuvių/savas/darbininkas")) 힙[objektas_nuoroda + 3] = 1;
        if (sritis_CODE >= 24 && sritis_CODE <= 28 && 한국어화면종(pavadinimas_konstanta) != 0) 힙[objektas_nuoroda + 13] = 1;
        if (sritis_CODE == 5 || sritis_CODE == 6 || sritis_CODE == 15 || sritis_CODE == 17 || sritis_CODE == 18) 힙[objektas_nuoroda + 2] = -1;
        if (sritis_CODE == 9) 힙[objektas_nuoroda + 2] = išimtis_nuoroda;
        넣기(objektas_nuoroda, 2);
    }
    static boolean 값같음(int 첫값, int baitas_duomenys) {
        if (첫값 == baitas_duomenys) return true;
        if (첫값 == 0 || baitas_duomenys == 0 || 첫값 < 0 || baitas_duomenys < 0 || 첫값 >= 힙끝 || baitas_duomenys >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[baitas_duomenys] == 1) return 글같음(첫값, baitas_duomenys, false);
        return 힙[첫값] == 12 && 힙[baitas_duomenys] == 12 && 힙[첫값 + 2] == 힙[baitas_duomenys + 2];
    }
    static int 글조각(int objektas_nuoroda, int Start_padėtis, int baigti_pokalbį_padėtis) {
        if (!objektas_VALUE(objektas_nuoroda, 1)) return 0;
        if (Start_padėtis < 0 || baigti_pokalbį_padėtis < Start_padėtis || baigti_pokalbį_padėtis > 힙[objektas_nuoroda + 1]) { triktis_VALUE("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = priskirti_Saugykla(1, baigti_pokalbį_padėtis - Start_padėtis); if (KLAIDA) return 0;
        for (int Loop_INDEX = Start_padėtis; Loop_INDEX < baigti_pokalbį_padėtis; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX - Start_padėtis] = 힙[objektas_nuoroda + 2 + Loop_INDEX];
        return 반환값;
    }
    static int sujungti_SMS_967a7f2f(int 첫값, int baitas_duomenys) {
        if (!objektas_VALUE(첫값, 1) || !objektas_VALUE(baitas_duomenys, 1)) return 0;
        int įrašas_COUNT = 힙[첫값 + 1], metodas_INDEX = 힙[baitas_duomenys + 1], 반환값 = priskirti_Saugykla(1, įrašas_COUNT + metodas_INDEX); if (KLAIDA) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < įrašas_COUNT; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 힙[첫값 + 2 + Loop_INDEX];
        for (int Loop_INDEX = 0; Loop_INDEX < metodas_INDEX; Loop_INDEX++) 힙[반환값 + 2 + įrašas_COUNT + Loop_INDEX] = 힙[baitas_duomenys + 2 + Loop_INDEX];
        return 반환값;
    }
    static boolean 기본호출(int savininkas, int pavadinimas_konstanta, int 서술상수, int komanda_CODE) {
        if (Word_SMS(savininkas, "Lietuvių/savas/실행인수") && komanda_CODE == 184) {
            if (Word_SMS(pavadinimas_konstanta, "prekė_COUNT") && Word_SMS(서술상수, "()I")) { 넣기(naudotojas.인수개수() - 1, 1); return true; }
            if (Word_SMS(pavadinimas_konstanta, "Tekstas") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= naudotojas.인수개수() - 1) 예외던짐(29, "Vykdyti_komanda Argumentai 범위를 벗어났습니다");
                else 넣기(organizuoti_simbolis(naudotojas.Argumentai(순번 + 1)), 2);
                return true;
            }
            triktis_VALUE("지원하지 않는 Lietuvių Vykdyti_komanda Argumentai 호출"); return true;
        }
        if (Word_SMS(savininkas, "Lietuvių/savas/darbininkas")) { Procesas_gija(pavadinimas_konstanta, 서술상수, komanda_CODE, true); return true; }
        if (한국어화면소유(savininkas)) { 한국어화면호출(savininkas, pavadinimas_konstanta, 서술상수, komanda_CODE); return true; }
        if (화면소유(savininkas)) { 화면호출(savininkas, pavadinimas_konstanta, 서술상수, komanda_CODE); return true; }
        if (Word_SMS(savininkas, "java/net/Socket") || Word_SMS(savininkas, "java/net/ServerSocket") || Word_SMS(savininkas, "java/io/InputStream") || Word_SMS(savininkas, "java/io/OutputStream")) { 흐름호출(savininkas, pavadinimas_konstanta, 서술상수, komanda_CODE); return true; }
        if (Word_SMS(savininkas, "Lietuvių/savas/branduolys_VALUE") && komanda_CODE == 184) {
            if (Word_SMS(pavadinimas_konstanta, "화면너비") && Word_SMS(서술상수, "()I")) { 넣기(naudotojas.화면너비(), 1); return true; }
            if (Word_SMS(pavadinimas_konstanta, "화면높이") && Word_SMS(서술상수, "()I")) { 넣기(naudotojas.화면높이(), 1); return true; }
            if (Word_SMS(pavadinimas_konstanta, "밀리초") && Word_SMS(서술상수, "()I")) { 넣기(naudotojas.밀리초(), 1); return true; }
            if (Word_SMS(pavadinimas_konstanta, "그림대기") && Word_SMS(서술상수, "()I")) { 넣기(naudotojas.그림대기(), 1); return true; }
            if (Word_SMS(pavadinimas_konstanta, "stačiakampis") && Word_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), x_koordinatė = 빼기(1); 넣기(naudotojas.stačiakampis(x_koordinatė, 세로좌표, 너비, 높이, 색상), 1); return true; }
        }
        if (Word_SMS(savininkas, "java/net/InetAddress") || Word_SMS(savininkas, "java/net/DatagramPacket") || Word_SMS(savininkas, "java/net/DatagramSocket")) { 통신호출(savininkas, pavadinimas_konstanta, 서술상수, komanda_CODE); return true; }
        if (Word_SMS(savininkas, "java/lang/Thread")) { 가닥호출(pavadinimas_konstanta, 서술상수, komanda_CODE); return true; }
        if (Word_SMS(savininkas, "java/lang/Object")) {
            if (Word_SMS(pavadinimas_konstanta, "<init>") && Word_SMS(서술상수, "()V") && komanda_CODE == 183) { 객체유효(빼기(2)); return true; }
            if (Word_SMS(pavadinimas_konstanta, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int baitas_duomenys = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == baitas_duomenys ? 1 : 0, 1); return true; }
        }
        if (išimtis_konstanta(savininkas) != 0) {
            if (Word_SMS(pavadinimas_konstanta, "<init>") && komanda_CODE == 183 && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int raginimas = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), objektas_nuoroda = 빼기(2);
                if (objektas_VALUE(objektas_nuoroda, 9)) { 힙[objektas_nuoroda + 3] = raginimas; 힙참조[objektas_nuoroda + 3] = 1; } return true;
            }
            if ((Word_SMS(pavadinimas_konstanta, "getMessage") || Word_SMS(pavadinimas_konstanta, "aprašas")) && Word_SMS(서술상수, "()Ljava/lang/String;")) { int objektas_nuoroda = 빼기(2); if (objektas_VALUE(objektas_nuoroda, 9)) 넣기(힙[objektas_nuoroda + 3], 2); return true; }
        }
        if (Word_SMS(savininkas, "java/lang/String")) {
            if (komanda_CODE == 182 && Word_SMS(pavadinimas_konstanta, "getBytes") && (Word_SMS(서술상수, "()[B") || Word_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int kodavimas_pavadinimas = Word_SMS(서술상수, "()[B") ? 0 : 빼기(2), objektas_nuoroda = 빼기(2);
                if (!objektas_VALUE(objektas_nuoroda, 1)) return true;
                if (kodavimas_pavadinimas != 0 && !글같음(kodavimas_pavadinimas, organizuoti_simbolis("UTF-8"), false) && !글같음(kodavimas_pavadinimas, organizuoti_simbolis("UTF8"), false) && !글같음(kodavimas_pavadinimas, organizuoti_simbolis("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int įrašas_COUNT = 힙[objektas_nuoroda + 1], 반환값 = priskirti_Saugykla(20, įrašas_COUNT * 3), 사용수 = 0; if (KLAIDA) return true;
                for (int vidinis_padėtis = 0; vidinis_padėtis < įrašas_COUNT; vidinis_padėtis++) {
                    int simbolio_kodas = 힙[objektas_nuoroda + 2 + vidinis_padėtis];
                    if (simbolio_kodas >= 0xd800 && simbolio_kodas <= 0xdbff && vidinis_padėtis + 1 < įrašas_COUNT && 힙[objektas_nuoroda + 3 + vidinis_padėtis] >= 0xdc00 && 힙[objektas_nuoroda + 3 + vidinis_padėtis] <= 0xdfff) simbolio_kodas = 0x10000 + ((simbolio_kodas - 0xd800) << 10) + 힙[objektas_nuoroda + 2 + ++vidinis_padėtis] - 0xdc00;
                    else if (simbolio_kodas >= 0xd800 && simbolio_kodas <= 0xdfff) simbolio_kodas = '?';
                    if (simbolio_kodas < 128) 힙[반환값 + 2 + 사용수++] = simbolio_kodas;
                    else { int baitas_COUNT = simbolio_kodas < 2048 ? 2 : simbolio_kodas < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((baitas_COUNT == 2 ? 192 : baitas_COUNT == 3 ? 224 : 240) | simbolio_kodas >> (6 * (baitas_COUNT - 1))); for (int Palyginimas_padėtis = baitas_COUNT - 1; Palyginimas_padėtis > 0; Palyginimas_padėtis--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | simbolio_kodas >> (6 * (Palyginimas_padėtis - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (komanda_CODE == 184 && Word_SMS(pavadinimas_konstanta, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(skaitmuo_simbolis(빼기(1)), 2); return true; }
            if (komanda_CODE != 182) return false;
            if (Word_SMS(pavadinimas_konstanta, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int baitas_duomenys = 빼기(2), 첫값 = 빼기(2); if (objektas_VALUE(첫값, 1)) 넣기(글같음(첫값, baitas_duomenys, false) ? 1 : 0, 1); return true; }
            if (Word_SMS(pavadinimas_konstanta, "isEmpty") && Word_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (objektas_VALUE(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_SMS(pavadinimas_konstanta, "substring") && (Word_SMS(서술상수, "(I)Ljava/lang/String;") || Word_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SECOND_VALUE = Word_SMS(서술상수, "(II)Ljava/lang/String;"); int baigti_pokalbį_padėtis = SECOND_VALUE ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (objektas_VALUE(첫값, 1)) 넣기(글조각(첫값, 시작점, SECOND_VALUE ? baigti_pokalbį_padėtis : 힙[첫값 + 1]), 2); return true;
            }
            if (Word_SMS(pavadinimas_konstanta, "concat") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int baitas_duomenys = 빼기(2), 첫값 = 빼기(2); 넣기(sujungti_SMS_967a7f2f(첫값, baitas_duomenys), 2); return true; }
            if (Word_SMS(pavadinimas_konstanta, "hashCode") && Word_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), maiša_VALUE = 0; if (objektas_VALUE(첫값, 1)) { for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) maiša_VALUE = maiša_VALUE * 31 + 힙[첫값 + 2 + Loop_INDEX]; 넣기(maiša_VALUE, 1); } return true; }
            if (Word_SMS(pavadinimas_konstanta, "toString") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (objektas_VALUE(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_SMS(savininkas, "java/lang/Integer")) {
            if (komanda_CODE == 184 && Word_SMS(pavadinimas_konstanta, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int duomenys_VALUE = 빼기(1), objektas_nuoroda = duomenys_VALUE >= -128 && duomenys_VALUE <= 127 ? Store_sveikasis_skaičius[duomenys_VALUE + 128] : 0; if (objektas_nuoroda == 0) { objektas_nuoroda = priskirti_Saugykla(12, 1); if (!KLAIDA) { 힙[objektas_nuoroda + 2] = duomenys_VALUE; if (duomenys_VALUE >= -128 && duomenys_VALUE <= 127) Store_sveikasis_skaičius[duomenys_VALUE + 128] = objektas_nuoroda; } } 넣기(objektas_nuoroda, 2); return true; }
            if (komanda_CODE == 183 && Word_SMS(pavadinimas_konstanta, "<init>") && Word_SMS(서술상수, "(I)V")) { int duomenys_VALUE = 빼기(1), objektas_nuoroda = 빼기(2); if (objektas_VALUE(objektas_nuoroda, 12)) 힙[objektas_nuoroda + 2] = duomenys_VALUE; return true; }
            if (komanda_CODE == 182 && Word_SMS(pavadinimas_konstanta, "intValue") && Word_SMS(서술상수, "()I")) { int objektas_nuoroda = 빼기(2); if (objektas_VALUE(objektas_nuoroda, 12)) 넣기(힙[objektas_nuoroda + 2], 1); return true; }
            if (komanda_CODE == 184 && Word_SMS(pavadinimas_konstanta, "toString") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(skaitmuo_simbolis(빼기(1)), 2); return true; }
        }
        if (Word_SMS(savininkas, "java/lang/Math") && komanda_CODE == 184) {
            if (Word_SMS(pavadinimas_konstanta, "abs") && Word_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_SMS(pavadinimas_konstanta, "min") || Word_SMS(pavadinimas_konstanta, "max")) && Word_SMS(서술상수, "(II)I")) { int baitas_duomenys = 빼기(1), 첫값 = 빼기(1); 넣기(Word_SMS(pavadinimas_konstanta, "min") ? (첫값 < baitas_duomenys ? 첫값 : baitas_duomenys) : (첫값 > baitas_duomenys ? 첫값 : baitas_duomenys), 1); return true; }
        }
        if (Word_SMS(savininkas, "java/lang/System") && komanda_CODE == 184) {
            if (Word_SMS(pavadinimas_konstanta, "gc") && Word_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Word_SMS(pavadinimas_konstanta, "arraycopy") && Word_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int įrašas_COUNT = 빼기(1), vieta_VALUE_INDEX = 빼기(1), baitas_duomenys = 빼기(2), Start_padėtis = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(baitas_duomenys)) {
                    int sritis_CODE = 힙[첫값];
                    if (힙[baitas_duomenys] != sritis_CODE || (sritis_CODE != 2 && sritis_CODE != 3 && (sritis_CODE < 20 || sritis_CODE > 23))) triktis_VALUE("arraycopy type mismatch");
                    else if (įrašas_COUNT < 0 || Start_padėtis < 0 || vieta_VALUE_INDEX < 0 || Start_padėtis > 힙[첫값 + 1] - įrašas_COUNT || vieta_VALUE_INDEX > 힙[baitas_duomenys + 1] - įrašas_COUNT) triktis_VALUE("ArrayIndexOutOfBoundsException");
                    else if (첫값 == baitas_duomenys && vieta_VALUE_INDEX > Start_padėtis) { for (int Loop_INDEX = įrašas_COUNT - 1; Loop_INDEX >= 0; Loop_INDEX--) 힙[baitas_duomenys + 2 + vieta_VALUE_INDEX + Loop_INDEX] = 힙[첫값 + 2 + Start_padėtis + Loop_INDEX]; }
                    else { for (int Loop_INDEX = 0; Loop_INDEX < įrašas_COUNT && !KLAIDA; Loop_INDEX++) { int duomenys_VALUE = 힙[첫값 + 2 + Start_padėtis + Loop_INDEX]; if (sritis_CODE != 3 || 배열저장가능(baitas_duomenys, duomenys_VALUE)) 힙[baitas_duomenys + 2 + vieta_VALUE_INDEX + Loop_INDEX] = duomenys_VALUE; } }
                }
                return true;
            }
        }
        if (Word_SMS(savininkas, "java/util/ArrayList") || Word_SMS(savininkas, "java/util/List") || Word_SMS(savininkas, "java/util/HashMap") || Word_SMS(savininkas, "java/util/Map")) {
            모음호출(savininkas, pavadinimas_konstanta, 서술상수, komanda_CODE); return true;
        }
        return false;
    }
    static void 모음늘리기(int objektas_nuoroda, int 필요수) {
        int 이전값 = 힙[objektas_nuoroda + 2], pajėgumas_duomenys = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (pajėgumas_duomenys >= 필요수) return;
        int toliau_padėtis = pajėgumas_duomenys < 8 ? 8 : pajėgumas_duomenys * 2; if (toliau_padėtis < 필요수) toliau_padėtis = 필요수;
        int duomenys_ARRAY = priskirti_Saugykla(3, toliau_padėtis); if (KLAIDA) return;
        for (int Loop_INDEX = 0; Loop_INDEX < pajėgumas_duomenys; Loop_INDEX++) 힙[duomenys_ARRAY + 2 + Loop_INDEX] = 힙[이전값 + 2 + Loop_INDEX];
        힙[objektas_nuoroda + 2] = duomenys_ARRAY; 힙참조[objektas_nuoroda + 2] = 1;
    }
    static void 모음호출(int savininkas, int pavadinimas_konstanta, int 서술상수, int komanda_CODE) {
        boolean 대응참조 = Word_SMS(savininkas, "java/util/HashMap") || Word_SMS(savininkas, "java/util/Map"); int sritis_CODE = 대응참조 ? 11 : 10;
        if (Word_SMS(pavadinimas_konstanta, "<init>") && komanda_CODE == 183 && Word_SMS(서술상수, "()V")) { int objektas_nuoroda = 빼기(2); if (objektas_VALUE(objektas_nuoroda, sritis_CODE)) 모음늘리기(objektas_nuoroda, 8); return; }
        if (komanda_CODE != 182 && komanda_CODE != 185) { triktis_VALUE("invalid collection invocation"); return; }
        if (Word_SMS(pavadinimas_konstanta, "size") && Word_SMS(서술상수, "()I") || Word_SMS(pavadinimas_konstanta, "isEmpty") && Word_SMS(서술상수, "()Z")) {
            int objektas_nuoroda = 빼기(2); if (objektas_VALUE(objektas_nuoroda, sritis_CODE)) 넣기(Word_SMS(pavadinimas_konstanta, "size") ? 힙[objektas_nuoroda + 3] : 힙[objektas_nuoroda + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_SMS(pavadinimas_konstanta, "clear") && Word_SMS(서술상수, "()V")) { int objektas_nuoroda = 빼기(2); if (objektas_VALUE(objektas_nuoroda, sritis_CODE)) { int duomenys_ARRAY = 힙[objektas_nuoroda + 2]; for (int Loop_INDEX = 0; Loop_INDEX < 힙[duomenys_ARRAY + 1]; Loop_INDEX++) 힙[duomenys_ARRAY + 2 + Loop_INDEX] = 0; 힙[objektas_nuoroda + 3] = 0; } return; }
        if (!대응참조 && Word_SMS(pavadinimas_konstanta, "add") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int duomenys_VALUE = 빼기(2), objektas_nuoroda = 빼기(2); if (!objektas_VALUE(objektas_nuoroda, 10)) return;
            int įrašas_COUNT = 힙[objektas_nuoroda + 3]; 모음늘리기(objektas_nuoroda, įrašas_COUNT + 1); if (!KLAIDA) { 힙[힙[objektas_nuoroda + 2] + 2 + įrašas_COUNT] = duomenys_VALUE; 힙[objektas_nuoroda + 3] = įrašas_COUNT + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_SMS(pavadinimas_konstanta, "get") || Word_SMS(pavadinimas_konstanta, "remove")) && Word_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Word_SMS(pavadinimas_konstanta, "set") && Word_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean informacinės_technologijos_priskirta = Word_SMS(pavadinimas_konstanta, "set"); int duomenys_VALUE = informacinės_technologijos_priskirta ? 빼기(2) : 0, įrašas_padėtis = 빼기(1), objektas_nuoroda = 빼기(2);
            if (!objektas_VALUE(objektas_nuoroda, 10)) return;
            int įrašas_COUNT = 힙[objektas_nuoroda + 3], duomenys_ARRAY = 힙[objektas_nuoroda + 2];
            if (įrašas_padėtis < 0 || įrašas_padėtis >= įrašas_COUNT) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[duomenys_ARRAY + 2 + įrašas_padėtis];
            if (informacinės_technologijos_priskirta) 힙[duomenys_ARRAY + 2 + įrašas_padėtis] = duomenys_VALUE;
            if (Word_SMS(pavadinimas_konstanta, "remove")) { for (int Loop_INDEX = įrašas_padėtis + 1; Loop_INDEX < įrašas_COUNT; Loop_INDEX++) 힙[duomenys_ARRAY + 1 + Loop_INDEX] = 힙[duomenys_ARRAY + 2 + Loop_INDEX]; 힙[duomenys_ARRAY + 1 + įrašas_COUNT] = 0; 힙[objektas_nuoroda + 3] = įrašas_COUNT - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Word_SMS(pavadinimas_konstanta, "get") || Word_SMS(pavadinimas_konstanta, "remove")) && Word_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(pavadinimas_konstanta, "put") && Word_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(pavadinimas_konstanta, "containsKey") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_SMS(pavadinimas_konstanta, "put"), pašalinti = Word_SMS(pavadinimas_konstanta, "remove");
            int duomenys_VALUE = 넣기여부 ? 빼기(2) : 0, Raktas_nuoroda = 빼기(2), objektas_nuoroda = 빼기(2); if (!objektas_VALUE(objektas_nuoroda, 11)) return;
            int įrašas_COUNT = 힙[objektas_nuoroda + 3], duomenys_ARRAY = 힙[objektas_nuoroda + 2], 찾은여부 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < įrašas_COUNT; Loop_INDEX++) if (값같음(Raktas_nuoroda, 힙[duomenys_ARRAY + 2 + 2 * Loop_INDEX])) { 찾은여부 = Loop_INDEX; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[duomenys_ARRAY + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(objektas_nuoroda, (įrašas_COUNT + 1) * 2); duomenys_ARRAY = 힙[objektas_nuoroda + 2]; 찾은여부 = įrašas_COUNT; if (!KLAIDA) 힙[objektas_nuoroda + 3] = įrašas_COUNT + 1; }
                if (!KLAIDA) { 힙[duomenys_ARRAY + 2 + 2 * 찾은여부] = Raktas_nuoroda; 힙[duomenys_ARRAY + 3 + 2 * 찾은여부] = duomenys_VALUE; }
            }
            if (pašalinti && 찾은여부 >= 0) { for (int Loop_INDEX = 찾은여부 + 1; Loop_INDEX < įrašas_COUNT; Loop_INDEX++) { 힙[duomenys_ARRAY + 2 * Loop_INDEX] = 힙[duomenys_ARRAY + 2 + 2 * Loop_INDEX]; 힙[duomenys_ARRAY + 1 + 2 * Loop_INDEX] = 힙[duomenys_ARRAY + 3 + 2 * Loop_INDEX]; } 힙[duomenys_ARRAY + 2 * įrašas_COUNT] = 0; 힙[duomenys_ARRAY + 1 + 2 * įrašas_COUNT] = 0; 힙[objektas_nuoroda + 3] = įrašas_COUNT - 1; }
            if (Word_SMS(pavadinimas_konstanta, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        triktis_VALUE("unsupported collection method");
    }
    static boolean 잠금얻기(int objektas_nuoroda) {
        if (!객체유효(objektas_nuoroda)) return false;
        if (잠금깊이[objektas_nuoroda] != 0 && užraktas_savininkas[objektas_nuoroda] != dabartinis_gija + 1) { keisti_užklausa = true; return false; }
        užraktas_savininkas[objektas_nuoroda] = dabartinis_gija + 1; 잠금깊이[objektas_nuoroda]++; return true;
    }
    static void išleisti_užraktas(int objektas_nuoroda) {
        if (!객체유효(objektas_nuoroda)) return;
        if (잠금깊이[objektas_nuoroda] == 0 || užraktas_savininkas[objektas_nuoroda] != dabartinis_gija + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[objektas_nuoroda] == 0) užraktas_savininkas[objektas_nuoroda] = 0;
    }
    static boolean SWITCH_gija() {
        gija_kadras[dabartinis_gija] = kadras_INDEX;
        if (kadras_INDEX < dabartinis_gija * 32) gija_Būsena[dabartinis_gija] = 3;
        for (int Loop_INDEX = 0; Loop_INDEX < gija_COUNT; Loop_INDEX++) if (gija_Būsena[Loop_INDEX] == 2 && gija_Būsena[가닥대기[Loop_INDEX]] == 3) gija_Būsena[Loop_INDEX] = 1;
        for (int Loop_INDEX = 1; Loop_INDEX <= gija_COUNT; Loop_INDEX++) {
            int toliau_padėtis = (dabartinis_gija + Loop_INDEX) % gija_COUNT;
            if (gija_Būsena[toliau_padėtis] == 1) { dabartinis_gija = toliau_padėtis; kadras_INDEX = gija_kadras[toliau_padėtis]; keisti_užklausa = false; return true; }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < gija_COUNT; Loop_INDEX++) if (gija_Būsena[Loop_INDEX] != 3) { triktis_VALUE("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int pavadinimas_konstanta, int 서술상수, int komanda_CODE) { Procesas_gija(pavadinimas_konstanta, 서술상수, komanda_CODE, false); }
    static void Procesas_gija(int pavadinimas_konstanta, int 서술상수, int komanda_CODE, boolean Lietuvių) {
        if (komanda_CODE == 184 && Word_SMS(pavadinimas_konstanta, Lietuvių ? "YIELD_užduotis" : "yield") && Word_SMS(서술상수, "()V")) { keisti_užklausa = true; return; }
        if (komanda_CODE == 184 && Word_SMS(pavadinimas_konstanta, "currentThread") && Word_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(gija_objektas[dabartinis_gija], 2); return; }
        if (komanda_CODE == 183 && Word_SMS(pavadinimas_konstanta, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, Lietuvių ? "(LLietuvių/savas/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int tikslas_ADDRESS = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), objektas_nuoroda = 빼기(2);
            if (!객체유효(objektas_nuoroda)) return;
            if (힙[objektas_nuoroda] == 13) { 힙[objektas_nuoroda + 2] = tikslas_ADDRESS; 힙참조[objektas_nuoroda + 2] = 1; }
            else if (tikslas_ADDRESS != 0) triktis_VALUE("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (komanda_CODE == 182 && (Word_SMS(pavadinimas_konstanta, Lietuvių ? "Start_užduotis" : "start") || Word_SMS(pavadinimas_konstanta, Lietuvių ? "기다리기" : "join")) && Word_SMS(서술상수, "()V") || komanda_CODE == 182 && Word_SMS(pavadinimas_konstanta, Lietuvių ? "살아있는가" : "isAlive") && Word_SMS(서술상수, "()Z")) {
            int objektas_nuoroda = 빼기(2); if (!객체유효(objektas_nuoroda)) return;
            int paskyra_VALUE = -1; for (int Loop_INDEX = 0; Loop_INDEX < gija_COUNT; Loop_INDEX++) if (gija_objektas[Loop_INDEX] == objektas_nuoroda) paskyra_VALUE = Loop_INDEX;
            if (Word_SMS(pavadinimas_konstanta, Lietuvių ? "살아있는가" : "isAlive")) { 넣기(paskyra_VALUE >= 0 && gija_Būsena[paskyra_VALUE] != 3 ? 1 : 0, 1); return; }
            if (Word_SMS(pavadinimas_konstanta, Lietuvių ? "기다리기" : "join")) { if (paskyra_VALUE >= 0 && gija_Būsena[paskyra_VALUE] != 3) { 가닥대기[dabartinis_gija] = paskyra_VALUE; gija_Būsena[dabartinis_gija] = 2; keisti_užklausa = true; } return; }
            if (paskyra_VALUE >= 0) { 예외던짐(Lietuvių ? 38 : 16, "thread already started"); return; }
            if (gija_COUNT == 4) { triktis_VALUE("thread limit (4 including main)"); return; }
            int tikslas_ADDRESS = 힙[objektas_nuoroda] == 13 ? 힙[objektas_nuoroda + 2] : objektas_nuoroda;
            int Failas_INDEX = tikslas_ADDRESS > 0 && 힙[tikslas_ADDRESS] >= 32 ? pavadinimas_metodas(힙[tikslas_ADDRESS] - 32, Lietuvių ? "Vykdyti" : "run", "()V") : -1;
            if (tikslas_ADDRESS != 0 && Failas_INDEX < 0) { triktis_VALUE("Runnable.run required"); return; }
            paskyra_VALUE = gija_COUNT++; gija_objektas[paskyra_VALUE] = objektas_nuoroda; gija_tikslas[paskyra_VALUE] = tikslas_ADDRESS;
            int kadras = paskyra_VALUE * 32; gija_kadras[paskyra_VALUE] = Failas_INDEX < 0 ? kadras - 1 : kadras; gija_Būsena[paskyra_VALUE] = Failas_INDEX < 0 ? 3 : 1;
            if (Failas_INDEX >= 0) { kadras_metodas[kadras] = Failas_INDEX; kadras_padėtis[kadras] = metodas_Start[Failas_INDEX]; vietinis_VALUE[kadras * 128] = tikslas_ADDRESS; vietinis_TYPE[kadras * 128] = 2; }
            return;
        }
        triktis_VALUE("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], ADDRESS_SMS = new int[16];
    static int vietinis_ADDRESS() { return ADDRESS_objektas(0x7f000001); }
    static int ADDRESS_objektas(int VALUE) { int objektas_nuoroda = priskirti_Saugykla(14, 1); if (!KLAIDA) 힙[objektas_nuoroda + 2] = VALUE; return objektas_nuoroda; }
    static int 주소해독(int objektas_nuoroda) {
        if (objektas_nuoroda == 0 || 글같음(objektas_nuoroda, organizuoti_simbolis("localhost"), false)) return 0x7f000001;
        if (!objektas_VALUE(objektas_nuoroda, 1)) return 0;
        int duomenys_VALUE = 0, bendras_COUNT = 0, ADDRESS_baitas = 0, 자릿수 = 0, įrašas_COUNT = 힙[objektas_nuoroda + 1];
        for (int Loop_INDEX = 0; Loop_INDEX <= įrašas_COUNT; Loop_INDEX++) {
            int simbolio_kodas = Loop_INDEX == įrašas_COUNT ? '.' : 힙[objektas_nuoroda + 2 + Loop_INDEX];
            if (simbolio_kodas == '.') { if (자릿수 == 0 || bendras_COUNT == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } duomenys_VALUE = duomenys_VALUE << 8 | ADDRESS_baitas; bendras_COUNT++; ADDRESS_baitas = 자릿수 = 0; }
            else { if (simbolio_kodas < '0' || simbolio_kodas > '9' || ++자릿수 > 3 || (ADDRESS_baitas = ADDRESS_baitas * 10 + simbolio_kodas - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (bendras_COUNT != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return duomenys_VALUE;
    }
    static int ADDRESS_simbolis(int duomenys_VALUE) {
        int įrašas_COUNT = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int ADDRESS_baitas = duomenys_VALUE >>> 이동비트 & 255;
            if (ADDRESS_baitas >= 100) ADDRESS_SMS[įrašas_COUNT++] = '0' + ADDRESS_baitas / 100;
            if (ADDRESS_baitas >= 10) ADDRESS_SMS[įrašas_COUNT++] = '0' + ADDRESS_baitas / 10 % 10;
            ADDRESS_SMS[įrašas_COUNT++] = '0' + ADDRESS_baitas % 10; if (이동비트 != 0) ADDRESS_SMS[įrašas_COUNT++] = '.';
        }
        int objektas_nuoroda = priskirti_Saugykla(1, įrašas_COUNT); if (!KLAIDA) for (int Loop_INDEX = 0; Loop_INDEX < įrašas_COUNT; Loop_INDEX++) 힙[objektas_nuoroda + 2 + Loop_INDEX] = ADDRESS_SMS[Loop_INDEX]; return objektas_nuoroda;
    }
    static void 통신호출(int savininkas, int pavadinimas_konstanta, int 서술상수, int komanda_CODE) {
        if (Word_SMS(savininkas, "java/net/InetAddress")) {
            if (komanda_CODE == 184 && Word_SMS(pavadinimas_konstanta, "getLoopbackAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(vietinis_ADDRESS(), 2); return; }
            if (komanda_CODE == 184 && Word_SMS(pavadinimas_konstanta, "getByName") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int duomenys_VALUE = 주소해독(빼기(2)); if (던진객체 == 0 && !KLAIDA) 넣기(ADDRESS_objektas(duomenys_VALUE), 2); return;
            }
            if (komanda_CODE == 182 && Word_SMS(pavadinimas_konstanta, "getHostAddress") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int objektas_nuoroda = 빼기(2); if (objektas_VALUE(objektas_nuoroda, 14)) 넣기(ADDRESS_simbolis(힙[objektas_nuoroda + 2]), 2); return; }
        }
        if (Word_SMS(savininkas, "java/net/DatagramPacket")) {
            if (komanda_CODE == 183 && Word_SMS(pavadinimas_konstanta, "<init>") && (Word_SMS(서술상수, "([BI)V") || Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean vieta_VALUE_nuoroda = Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int prievado_numeris = vieta_VALUE_nuoroda ? 빼기(1) : 0, ADDRESS_nuoroda = vieta_VALUE_nuoroda ? 빼기(2) : 0;
                int įrašas_COUNT = 빼기(1), duomenys_ARRAY = 빼기(2), objektas_nuoroda = 빼기(2);
                if (!objektas_VALUE(objektas_nuoroda, 16) || !objektas_VALUE(duomenys_ARRAY, 20)) return;
                if (įrašas_COUNT < 0 || įrašas_COUNT > 힙[duomenys_ARRAY + 1] || prievado_numeris < 0 || prievado_numeris > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (ADDRESS_nuoroda != 0 && !objektas_VALUE(ADDRESS_nuoroda, 14)) return;
                힙[objektas_nuoroda + 2] = duomenys_ARRAY; 힙참조[objektas_nuoroda + 2] = 1; 힙[objektas_nuoroda + 3] = įrašas_COUNT;
                힙[objektas_nuoroda + 4] = ADDRESS_nuoroda; 힙참조[objektas_nuoroda + 4] = 1; 힙[objektas_nuoroda + 5] = prievado_numeris; return;
            }
            if (komanda_CODE == 182 && Word_SMS(pavadinimas_konstanta, "setLength") && Word_SMS(서술상수, "(I)V")) {
                int įrašas_COUNT = 빼기(1), objektas_nuoroda = 빼기(2); if (!objektas_VALUE(objektas_nuoroda, 16)) return;
                if (įrašas_COUNT < 0 || įrašas_COUNT > 힙[힙[objektas_nuoroda + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[objektas_nuoroda + 3] = įrašas_COUNT; return;
            }
            if (komanda_CODE == 182 && (Word_SMS(pavadinimas_konstanta, "getData") && Word_SMS(서술상수, "()[B") || Word_SMS(pavadinimas_konstanta, "getLength") && Word_SMS(서술상수, "()I") || Word_SMS(pavadinimas_konstanta, "getAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;") || Word_SMS(pavadinimas_konstanta, "getPort") && Word_SMS(서술상수, "()I"))) {
                int objektas_nuoroda = 빼기(2); if (!objektas_VALUE(objektas_nuoroda, 16)) return;
                int įrašas_padėtis = Word_SMS(pavadinimas_konstanta, "getData") ? 2 : Word_SMS(pavadinimas_konstanta, "getLength") ? 3 : Word_SMS(pavadinimas_konstanta, "getAddress") ? 4 : 5;
                넣기(힙[objektas_nuoroda + įrašas_padėtis], įrašas_padėtis == 2 || įrašas_padėtis == 4 ? 2 : 1); return;
            }
        }
        if (Word_SMS(savininkas, "java/net/DatagramSocket")) {
            if (komanda_CODE == 183 && Word_SMS(pavadinimas_konstanta, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(I)V"))) {
                int prievado_numeris = Word_SMS(서술상수, "()V") ? 0 : 빼기(1), objektas_nuoroda = 빼기(2); if (!objektas_VALUE(objektas_nuoroda, 15)) return;
                if (prievado_numeris < 0 || prievado_numeris > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = naudotojas.kurti_tinklas(prievado_numeris); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[objektas_nuoroda + 2] = 열린파일번호; return;
            }
            if (komanda_CODE == 182 && Word_SMS(pavadinimas_konstanta, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), objektas_nuoroda = 빼기(2); if (!objektas_VALUE(objektas_nuoroda, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[objektas_nuoroda + 3] = 밀리초값; return;
            }
            if (komanda_CODE == 182 && Word_SMS(pavadinimas_konstanta, "getLocalPort") && Word_SMS(서술상수, "()I")) { int objektas_nuoroda = 빼기(2); if (objektas_VALUE(objektas_nuoroda, 15)) 넣기(힙[objektas_nuoroda + 2] < 0 ? -1 : naudotojas.tinklas_jungtis(힙[objektas_nuoroda + 2]), 1); return; }
            if (komanda_CODE == 182 && Word_SMS(pavadinimas_konstanta, "isClosed") && Word_SMS(서술상수, "()Z")) { int objektas_nuoroda = 빼기(2); if (objektas_VALUE(objektas_nuoroda, 15)) 넣기(힙[objektas_nuoroda + 2] < 0 ? 1 : 0, 1); return; }
            if (komanda_CODE == 182 && Word_SMS(pavadinimas_konstanta, "close") && Word_SMS(서술상수, "()V")) { int objektas_nuoroda = 빼기(2); if (objektas_VALUE(objektas_nuoroda, 15) && 힙[objektas_nuoroda + 2] >= 0) { naudotojas.파일서술자닫기(힙[objektas_nuoroda + 2]); 힙[objektas_nuoroda + 2] = -1; } return; }
            if (komanda_CODE == 182 && (Word_SMS(pavadinimas_konstanta, "send") || Word_SMS(pavadinimas_konstanta, "receive")) && Word_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int paketas_5cd5338b = 빼기(2), objektas_nuoroda = 빼기(2); if (!objektas_VALUE(paketas_5cd5338b, 16) || !objektas_VALUE(objektas_nuoroda, 15)) return;
                int duomenys_ARRAY = 힙[paketas_5cd5338b + 2], 유효길이 = 힙[paketas_5cd5338b + 3], 열린파일번호 = 힙[objektas_nuoroda + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_SMS(pavadinimas_konstanta, "send")) {
                    if (!objektas_VALUE(힙[paketas_5cd5338b + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < 유효길이; Loop_INDEX++) 통신임시[Loop_INDEX] = 힙[duomenys_ARRAY + 2 + Loop_INDEX];
                    if (naudotojas.siųsti_tinklas(열린파일번호, 힙[힙[paketas_5cd5338b + 4] + 2], 힙[paketas_5cd5338b + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int įrašas_COUNT = naudotojas.gauti_tinklas(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (įrašas_COUNT == -11) {
                        int dabartinis_TIME = naudotojas.밀리초();
                        if (힙[objektas_nuoroda + 4] == 0) 힙[objektas_nuoroda + 4] = dabartinis_TIME + 1;
                        if (힙[objektas_nuoroda + 3] > 0 && dabartinis_TIME - (힙[objektas_nuoroda + 4] - 1) >= 힙[objektas_nuoroda + 3]) { 힙[objektas_nuoroda + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(objektas_nuoroda, 2); 넣기(paketas_5cd5338b, 2); kadras_padėtis[kadras_INDEX] = 틀명령[kadras_INDEX]; keisti_užklausa = true; return;
                    }
                    힙[objektas_nuoroda + 4] = 0;
                    if (įrašas_COUNT < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < įrašas_COUNT; Loop_INDEX++) 힙[duomenys_ARRAY + 2 + Loop_INDEX] = (byte)통신임시[Loop_INDEX];
                    힙[paketas_5cd5338b + 3] = įrašas_COUNT; 힙[paketas_5cd5338b + 4] = ADDRESS_objektas(통신임시[513]); 힙참조[paketas_5cd5338b + 4] = 1; 힙[paketas_5cd5338b + 5] = 통신임시[512];
                }
                return;
            }
        }
        triktis_VALUE("unsupported java.net method");
    }
    static boolean 흐름대기(int objektas_nuoroda) {
        int dabartinis_TIME = naudotojas.밀리초();
        if (힙[objektas_nuoroda + 5] == 0) 힙[objektas_nuoroda + 5] = dabartinis_TIME + 1;
        if (힙[objektas_nuoroda + 3] > 0 && dabartinis_TIME - (힙[objektas_nuoroda + 5] - 1) >= 힙[objektas_nuoroda + 3]) { 힙[objektas_nuoroda + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        kadras_padėtis[kadras_INDEX] = 틀명령[kadras_INDEX]; keisti_užklausa = true; return true;
    }
    static void 흐름호출(int savininkas, int pavadinimas_konstanta, int 서술상수, int komanda_CODE) {
        boolean gauti_puslapis = Word_SMS(savininkas, "java/net/ServerSocket"), Stream = Word_SMS(savininkas, "java/io/InputStream") || Word_SMS(savininkas, "java/io/OutputStream");
        if (!Stream && komanda_CODE == 183 && Word_SMS(pavadinimas_konstanta, "<init>")) {
            boolean 빈여부 = Word_SMS(서술상수, "()V"), 이름지정여부 = Word_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || gauti_puslapis && Word_SMS(서술상수, "(I)V") || !gauti_puslapis && (이름지정여부 || 주소지정여부))) { triktis_VALUE("unsupported socket constructor"); return; }
            int prievado_numeris = 빈여부 ? 0 : 빼기(1), ADDRESS_nuoroda = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, objektas_nuoroda = 빼기(2);
            if (!objektas_VALUE(objektas_nuoroda, gauti_puslapis ? 18 : 17)) return;
            if (prievado_numeris < 0 || prievado_numeris > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !objektas_VALUE(ADDRESS_nuoroda, 14)) return;
            int tinklo_identifikatorius = 이름지정여부 ? 주소해독(ADDRESS_nuoroda) : 주소지정여부 ? 힙[ADDRESS_nuoroda + 2] : 0x7f000001;
            if (KLAIDA || 던진객체 != 0) return;
            int 열린파일번호 = naudotojas.Stream_valdymas(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : gauti_puslapis ? naudotojas.Stream_valdymas(1, 열린파일번호, prievado_numeris) : naudotojas.ryšys_Stream(열린파일번호, tinklo_identifikatorius, prievado_numeris);
            if (처리값 < 0) { naudotojas.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[objektas_nuoroda + 2] = 열린파일번호; 힙[objektas_nuoroda + 4] = prievado_numeris; 힙[objektas_nuoroda + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!Stream && Word_SMS(pavadinimas_konstanta, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), objektas_nuoroda = 빼기(2); if (!objektas_VALUE(objektas_nuoroda, gauti_puslapis ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[objektas_nuoroda + 3] = 밀리초값; return; }
        if (!Stream && Word_SMS(pavadinimas_konstanta, "close") && Word_SMS(서술상수, "()V")) { int objektas_nuoroda = 빼기(2); if (objektas_VALUE(objektas_nuoroda, gauti_puslapis ? 18 : 17) && 힙[objektas_nuoroda + 2] >= 0) { naudotojas.파일서술자닫기(힙[objektas_nuoroda + 2]); 힙[objektas_nuoroda + 2] = -1; } return; }
        if (!Stream && (Word_SMS(pavadinimas_konstanta, "getLocalPort") || Word_SMS(pavadinimas_konstanta, "getPort") || Word_SMS(pavadinimas_konstanta, "isClosed") || Word_SMS(pavadinimas_konstanta, "isConnected"))) {
            int objektas_nuoroda = 빼기(2); if (!objektas_VALUE(objektas_nuoroda, gauti_puslapis ? 18 : 17)) return;
            넣기(Word_SMS(pavadinimas_konstanta, "isClosed") ? 힙[objektas_nuoroda + 2] < 0 ? 1 : 0 : Word_SMS(pavadinimas_konstanta, "isConnected") ? 힙[objektas_nuoroda + 6] : Word_SMS(pavadinimas_konstanta, "getPort") ? 힙[objektas_nuoroda + 4] : 힙[objektas_nuoroda + 2] < 0 ? -1 : naudotojas.Stream_valdymas(4, 힙[objektas_nuoroda + 2], 0), 1); return;
        }
        if (gauti_puslapis && Word_SMS(pavadinimas_konstanta, "accept") && Word_SMS(서술상수, "()Ljava/net/Socket;")) {
            int objektas_nuoroda = 빼기(2); if (!objektas_VALUE(objektas_nuoroda, 18)) return; int 열린파일번호 = naudotojas.Stream_valdymas(3, 힙[objektas_nuoroda + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(objektas_nuoroda)) 넣기(objektas_nuoroda, 2); return; }
            힙[objektas_nuoroda + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = priskirti_Saugykla(17, 5); if (KLAIDA) { naudotojas.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = naudotojas.Stream_valdymas(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!gauti_puslapis && !Stream && ((Word_SMS(pavadinimas_konstanta, "getInputStream") && Word_SMS(서술상수, "()Ljava/io/InputStream;")) || (Word_SMS(pavadinimas_konstanta, "getOutputStream") && Word_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int objektas_nuoroda = 빼기(2); if (!objektas_VALUE(objektas_nuoroda, 17)) return; if (힙[objektas_nuoroda + 2] < 0 || 힙[objektas_nuoroda + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = priskirti_Saugykla(19, 4); if (KLAIDA) return; 힙[반환값 + 2] = objektas_nuoroda; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Word_SMS(pavadinimas_konstanta, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (Stream) {
            boolean 읽기여부 = Word_SMS(pavadinimas_konstanta, "read"), informacinės_technologijos_rašymas_operacija = Word_SMS(pavadinimas_konstanta, "write"), blokas = Word_SMS(서술상수, "([B)I") || Word_SMS(서술상수, "([B)V"), informacinės_technologijos_SUBARRAY = Word_SMS(서술상수, "([BII)I") || Word_SMS(서술상수, "([BII)V");
            int įrašas_COUNT = informacinės_technologijos_SUBARRAY ? 빼기(1) : 0, 시작변위 = informacinės_technologijos_SUBARRAY ? 빼기(1) : 0, duomenys_ARRAY = blokas || informacinės_technologijos_SUBARRAY ? 빼기(2) : 0;
            int duomenys_VALUE = informacinės_technologijos_rašymas_operacija && Word_SMS(서술상수, "(I)V") ? 빼기(1) : 0, objektas_nuoroda = 빼기(2);
            if (!objektas_VALUE(objektas_nuoroda, 19)) return; int pirminis_nuoroda = 힙[objektas_nuoroda + 2], 열린파일번호 = 힙[pirminis_nuoroda + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_SMS(pavadinimas_konstanta, "close") && Word_SMS(서술상수, "()V")) { naudotojas.파일서술자닫기(열린파일번호); 힙[pirminis_nuoroda + 2] = -1; return; }
            if (Word_SMS(pavadinimas_konstanta, "flush") && Word_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !informacinės_technologijos_rašymas_operacija) || 읽기여부 != (힙[objektas_nuoroda + 3] == 0)) { triktis_VALUE("unsupported stream operation"); return; }
            if (blokas || informacinės_technologijos_SUBARRAY) { if (!objektas_VALUE(duomenys_ARRAY, 20)) return; if (blokas) įrašas_COUNT = 힙[duomenys_ARRAY + 1]; if (시작변위 < 0 || įrašas_COUNT < 0 || 시작변위 > 힙[duomenys_ARRAY + 1] - įrašas_COUNT) { 예외던짐(6, "stream array bounds"); return; } }
            else įrašas_COUNT = 1;
            if (įrašas_COUNT == 0) { if (읽기여부) 넣기(0, 1); return; }
            int baigta_COUNT = informacinės_technologijos_rašymas_operacija ? 힙[objektas_nuoroda + 4] : 0, 처리값 = 0;
            while (baigta_COUNT < įrašas_COUNT) {
                처리값 = 읽기여부 ? naudotojas.파일한바이트읽기(열린파일번호) : naudotojas.파일한바이트쓰기(열린파일번호, blokas || informacinės_technologijos_SUBARRAY ? 힙[duomenys_ARRAY + 2 + 시작변위 + baigta_COUNT] : duomenys_VALUE);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (blokas || informacinės_technologijos_SUBARRAY)) 힙[duomenys_ARRAY + 2 + 시작변위 + baigta_COUNT] = (byte)처리값;
                baigta_COUNT++; if (읽기여부 && !(blokas || informacinės_technologijos_SUBARRAY)) break;
            }
            if (처리값 == -11 && (informacinės_technologijos_rašymas_operacija || baigta_COUNT == 0)) {
                힙[objektas_nuoroda + 4] = baigta_COUNT;
                if (흐름대기(pirminis_nuoroda)) { 넣기(objektas_nuoroda, 2); if (blokas || informacinės_technologijos_SUBARRAY) 넣기(duomenys_ARRAY, 2); if (informacinės_technologijos_SUBARRAY) { 넣기(시작변위, 1); 넣기(įrašas_COUNT, 1); } if (informacinės_technologijos_rašymas_operacija && !(blokas || informacinės_technologijos_SUBARRAY)) 넣기(duomenys_VALUE, 1); } return;
            }
            힙[objektas_nuoroda + 4] = 0; 힙[pirminis_nuoroda + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(baigta_COUNT == 0 && 처리값 == 256 ? -1 : blokas || informacinės_technologijos_SUBARRAY ? baigta_COUNT : 처리값, 1); return;
        }
        triktis_VALUE("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int pavadinimas_konstanta) {
        if (Word_SMS(pavadinimas_konstanta, "Lietuvių/savas/Langas")) return 24;
        if (Word_SMS(pavadinimas_konstanta, "Lietuvių/savas/Pavadinimas")) return 26;
        if (Word_SMS(pavadinimas_konstanta, "Lietuvių/savas/mygtukas")) return 27;
        if (Word_SMS(pavadinimas_konstanta, "Lietuvių/savas/teksto_laukas")) return 28;
        if (Word_SMS(pavadinimas_konstanta, "Lietuvių/savas/gavinys_pranešimas")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int pavadinimas_konstanta) {
        return 한국어화면종(pavadinimas_konstanta) != 0 || Word_SMS(pavadinimas_konstanta, "Lietuvių/savas/화면구성요소") || Word_SMS(pavadinimas_konstanta, "Lietuvių/savas/įvykis_eilė");
    }
    static int 화면종(int pavadinimas_konstanta) {
        int 한국어종 = 한국어화면종(pavadinimas_konstanta); if (한국어종 != 0) return 한국어종;
        if (Word_SMS(pavadinimas_konstanta, "javax/swing/JFrame")) return 24;
        if (Word_SMS(pavadinimas_konstanta, "javax/swing/JPanel")) return 25;
        if (Word_SMS(pavadinimas_konstanta, "javax/swing/JLabel")) return 26;
        if (Word_SMS(pavadinimas_konstanta, "javax/swing/JButton")) return 27;
        if (Word_SMS(pavadinimas_konstanta, "javax/swing/JTextField")) return 28;
        if (Word_SMS(pavadinimas_konstanta, "java/awt/event/ActionEvent")) return 29;
        if (Word_SMS(pavadinimas_konstanta, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int pavadinimas_konstanta) {
        return 화면종(pavadinimas_konstanta) != 0 || Word_SMS(pavadinimas_konstanta, "java/awt/Component") || Word_SMS(pavadinimas_konstanta, "java/awt/Container") || Word_SMS(pavadinimas_konstanta, "javax/swing/JComponent") || Word_SMS(pavadinimas_konstanta, "javax/swing/AbstractButton") || Word_SMS(pavadinimas_konstanta, "javax/swing/text/JTextComponent") || Word_SMS(pavadinimas_konstanta, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int objektas_nuoroda) { if (!객체유효(objektas_nuoroda)) return false; if (힙[objektas_nuoroda] < 24 || 힙[objektas_nuoroda] > 28) { triktis_VALUE("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int objektas_nuoroda, int SMS_nuoroda) {
        if (SMS_nuoroda != 0 && !objektas_VALUE(SMS_nuoroda, 1)) return;
        int įrašas_COUNT = SMS_nuoroda == 0 ? 0 : 힙[SMS_nuoroda + 1]; if (įrašas_COUNT > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < įrašas_COUNT; Loop_INDEX++) 화면글임시[Loop_INDEX] = 힙[SMS_nuoroda + 2 + Loop_INDEX];
        if (naudotojas.화면글(힙[objektas_nuoroda + 2], 화면글임시, įrašas_COUNT) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[objektas_nuoroda + 3] = SMS_nuoroda; 힙참조[objektas_nuoroda + 3] = 1;
    }
    static int 화면문자읽기(int objektas_nuoroda) {
        int paskyra_VALUE = 힙[objektas_nuoroda + 2], įrašas_COUNT = naudotojas.화면연결(8, paskyra_VALUE, 0, 0, 0, 0), 사용수 = 0;
        if (įrašas_COUNT < 0) { triktis_VALUE("GUI text read failed"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < įrašas_COUNT; Loop_INDEX++) { int 부호값 = naudotojas.화면연결(9, paskyra_VALUE, Loop_INDEX, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = priskirti_Saugykla(1, 사용수); if (!KLAIDA) for (int Loop_INDEX = 0; Loop_INDEX < 사용수; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 화면글임시[Loop_INDEX]; return 반환값;
    }
    /* Lietuvių 객체를 직접 만들고 branduolys_VALUE 화면 기능에 연결한다. Swing objektas_VALUE/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int savininkas, int pavadinimas_konstanta, int 서술상수, int komanda_CODE) {
        if (Word_SMS(savininkas, "Lietuvių/savas/įvykis_eilė")) {
            if (komanda_CODE == 184 && Word_SMS(pavadinimas_konstanta, "나중에실행") && Word_SMS(서술상수, "(LLietuvių/savas/실행할일;)V")) {
                int užduotis_gavinys = 빼기(2); if (!객체유효(užduotis_gavinys)) return;
                if (나중수 == 8) { triktis_VALUE("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = užduotis_gavinys; return;
            }
            if (komanda_CODE == 184 && Word_SMS(pavadinimas_konstanta, "사건처리중인가") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            triktis_VALUE("지원하지 않는 Lietuvių 화면 일정 호출"); return;
        }
        if (Word_SMS(savininkas, "Lietuvių/savas/gavinys_pranešimas")) {
            int pranešimas = 빼기(2); if (!objektas_VALUE(pranešimas, 29) || 힙[pranešimas + 3] == 0) return;
            if (Word_SMS(pavadinimas_konstanta, "įvykio_šaltinis") && Word_SMS(서술상수, "()LLietuvių/savas/화면구성요소;")) 넣기(힙[pranešimas + 2], 2);
            else if (Word_SMS(pavadinimas_konstanta, "komanda_SMS") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[pranešimas + 2]), 2);
            else if (Word_SMS(pavadinimas_konstanta, "INDEX") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else triktis_VALUE("지원하지 않는 Lietuvių Veiksmas pranešimas 호출"); return;
        }
        if (komanda_CODE == 183 && Word_SMS(pavadinimas_konstanta, "<init>")) {
            int 종류 = 한국어화면종(savininkas), 받이 = 0, 가로 = 0, segmentas_padėtis = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Word_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (naudotojas.화면너비() - 폭) / 2; segmentas_padėtis = (naudotojas.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Word_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Word_SMS(서술상수, "(Ljava/lang/String;IIIILLietuvių/savas/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); segmentas_padėtis = 빼기(1); 가로 = 빼기(1);
            } else { triktis_VALUE("지원하지 않는 Lietuvių 화면 생성자"); return; }
            int Tekstas = 빼기(2), elementas_VALUE = 빼기(2); if (!화면객체(elementas_VALUE)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || segmentas_padėtis < 0 || 폭 > naudotojas.화면너비() - 가로 || 높이 > naudotojas.화면높이() - segmentas_padėtis) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDEX = naudotojas.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (INDEX < 1 || INDEX > 32) { triktis_VALUE("화면 elementas_VALUE 자리가 가득 찼습니다"); return; }
            힙[elementas_VALUE + 2] = INDEX; 화면참조[INDEX - 1] = elementas_VALUE;
            힙[elementas_VALUE + 5] = 가로; 힙[elementas_VALUE + 6] = segmentas_padėtis; 힙[elementas_VALUE + 7] = 폭; 힙[elementas_VALUE + 8] = 높이; 힙[elementas_VALUE + 10] = 2;
            힙[elementas_VALUE + 4] = 받이; 힙참조[elementas_VALUE + 4] = 1; 힙[elementas_VALUE + 12] = 1;
            naudotojas.화면연결(1, INDEX, 가로, segmentas_padėtis, 폭, 높이);
            if (종류 == 24) naudotojas.화면연결(7, INDEX, 2, 0, 0, 0);
            화면문자설정(elementas_VALUE, Tekstas); return;
        }
        if (komanda_CODE != 182) { triktis_VALUE("잘못된 Lietuvių 화면 호출 Komanda"); return; }
        if (Word_SMS(pavadinimas_konstanta, "rašymas_SMS") && Word_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int Tekstas = 빼기(2), elementas_VALUE = 빼기(2); if (화면객체(elementas_VALUE)) 화면문자설정(elementas_VALUE, Tekstas); return;
        }
        if (Word_SMS(pavadinimas_konstanta, "글읽기") && Word_SMS(서술상수, "()Ljava/lang/String;")) {
            int elementas_VALUE = 빼기(2); if (화면객체(elementas_VALUE)) 넣기(화면문자읽기(elementas_VALUE), 2); return;
        }
        if (Word_SMS(pavadinimas_konstanta, "동작맡기기") && Word_SMS(서술상수, "(LLietuvių/savas/동작받이;)V")) {
            int 받이 = 빼기(2), elementas_VALUE = 빼기(2);
            if (화면객체(elementas_VALUE)) { 힙[elementas_VALUE + 4] = 받이; 힙참조[elementas_VALUE + 4] = 1; 힙[elementas_VALUE + 12] = 1; } return;
        }
        if (Word_SMS(pavadinimas_konstanta, "Įtraukti_elementas") && Word_SMS(서술상수, "(LLietuvių/savas/화면구성요소;)V")) {
            int vaikas_VALUE = 빼기(2), pirminis_VALUE = 빼기(2); if (!화면객체(vaikas_VALUE) || !화면객체(pirminis_VALUE)) return;
            if (naudotojas.화면연결(2, 힙[pirminis_VALUE + 2], 힙[vaikas_VALUE + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[vaikas_VALUE + 11] = pirminis_VALUE; 힙참조[vaikas_VALUE + 11] = 1; return;
        }
        if (Word_SMS(pavadinimas_konstanta, "자리정하기") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), segmentas_padėtis = 빼기(1), 가로 = 빼기(1), elementas_VALUE = 빼기(2); if (!화면객체(elementas_VALUE)) return;
            if (naudotojas.화면연결(1, 힙[elementas_VALUE + 2], 가로, segmentas_padėtis, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[elementas_VALUE + 5] = 가로; 힙[elementas_VALUE + 6] = segmentas_padėtis; 힙[elementas_VALUE + 7] = 폭; 힙[elementas_VALUE + 8] = 높이; return;
        }
        if ((Word_SMS(pavadinimas_konstanta, "laida_langas") || Word_SMS(pavadinimas_konstanta, "Užverti")) && Word_SMS(서술상수, "()V")) {
            boolean matomumas_VALUE = Word_SMS(pavadinimas_konstanta, "laida_langas"); int elementas_VALUE = 빼기(2); if (!화면객체(elementas_VALUE)) return;
            if (naudotojas.화면연결(matomumas_VALUE ? 3 : 4, 힙[elementas_VALUE + 2], matomumas_VALUE ? 1 : 0, 0, 0, 0) < 0) { triktis_VALUE("화면은 대화형 명령에서 실행해야 합니다"); return; }
            힙[elementas_VALUE + 9] = matomumas_VALUE ? 1 : 0; return;
        }
        if (Word_SMS(pavadinimas_konstanta, "보이는가") && Word_SMS(서술상수, "()Z")) { int elementas_VALUE = 빼기(2); if (화면객체(elementas_VALUE)) 넣기(힙[elementas_VALUE + 9], 1); return; }
        triktis_VALUE("지원하지 않는 Lietuvių 화면 metodas_VALUE");
    }
    static void 화면호출(int savininkas, int pavadinimas_konstanta, int 서술상수, int komanda_CODE) {
        if (Word_SMS(savininkas, "javax/swing/SwingUtilities")) {
            if (komanda_CODE == 184 && Word_SMS(pavadinimas_konstanta, "invokeLater") && Word_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int objektas_nuoroda = 빼기(2); if (!객체유효(objektas_nuoroda)) return; if (나중수 == 8) { triktis_VALUE("invokeLater queue full"); return; } 나중실행[나중수++] = objektas_nuoroda; return; }
            if (komanda_CODE == 184 && Word_SMS(pavadinimas_konstanta, "isEventDispatchThread") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            triktis_VALUE("unsupported SwingUtilities method"); return;
        }
        if (Word_SMS(savininkas, "java/awt/event/ActionEvent")) {
            int objektas_nuoroda = 빼기(2); if (!objektas_VALUE(objektas_nuoroda, 29)) return;
            if (Word_SMS(pavadinimas_konstanta, "getSource") && Word_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[objektas_nuoroda + 2], 2);
            else if (Word_SMS(pavadinimas_konstanta, "getActionCommand") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[objektas_nuoroda + 2]), 2);
            else if (Word_SMS(pavadinimas_konstanta, "getID") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else triktis_VALUE("unsupported ActionEvent method"); return;
        }
        if (komanda_CODE == 183 && Word_SMS(pavadinimas_konstanta, "<init>")) {
            int COLUMNS = 0, SMS_nuoroda = 0;
            if (Word_SMS(서술상수, "(I)V")) COLUMNS = 빼기(1);
            else if (Word_SMS(서술상수, "(Ljava/lang/String;I)V")) { COLUMNS = 빼기(1); SMS_nuoroda = 빼기(2); }
            else if (Word_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_nuoroda = 빼기(2);
            else if (Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_SMS(서술상수, "()V")) { triktis_VALUE("unsupported Swing constructor"); return; }
            int objektas_nuoroda = 빼기(2); if (!객체유효(objektas_nuoroda)) return;
            if (힙[objektas_nuoroda] == 30) { triktis_VALUE("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(objektas_nuoroda) || COLUMNS < 0) return;
            int paskyra_VALUE = naudotojas.화면연결(0, 힙[objektas_nuoroda] - 23, 0, 0, 0, 0);
            if (paskyra_VALUE < 1 || paskyra_VALUE > 32) { triktis_VALUE("GUI widget slots exhausted"); return; }
            힙[objektas_nuoroda + 2] = paskyra_VALUE; 화면참조[paskyra_VALUE - 1] = objektas_nuoroda; 힙[objektas_nuoroda + 5] = 힙[objektas_nuoroda] == 24 ? 130 : 16; 힙[objektas_nuoroda + 6] = 힙[objektas_nuoroda] == 24 ? 110 : 16;
            힙[objektas_nuoroda + 7] = 힙[objektas_nuoroda] == 24 ? 380 : 220; 힙[objektas_nuoroda + 8] = 힙[objektas_nuoroda] == 24 ? 240 : 28; 힙[objektas_nuoroda + 10] = 1;
            화면문자설정(objektas_nuoroda, SMS_nuoroda); return;
        }
        if (Word_SMS(pavadinimas_konstanta, "setText") || Word_SMS(pavadinimas_konstanta, "setTitle")) { int SMS_nuoroda = 빼기(2), objektas_nuoroda = 빼기(2); if (화면객체(objektas_nuoroda) && Word_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(objektas_nuoroda, SMS_nuoroda); return; }
        if (Word_SMS(pavadinimas_konstanta, "getText") || Word_SMS(pavadinimas_konstanta, "getTitle")) { int objektas_nuoroda = 빼기(2); if (화면객체(objektas_nuoroda) && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(objektas_nuoroda), 2); return; }
        if (Word_SMS(pavadinimas_konstanta, "addActionListener") && Word_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int gauti_nuoroda = 빼기(2), objektas_nuoroda = 빼기(2); if (화면객체(objektas_nuoroda)) { 힙[objektas_nuoroda + 4] = gauti_nuoroda; 힙참조[objektas_nuoroda + 4] = 1; } return; }
        if (Word_SMS(pavadinimas_konstanta, "getContentPane") && Word_SMS(서술상수, "()Ljava/awt/Container;")) { int objektas_nuoroda = 빼기(2); if (화면객체(objektas_nuoroda)) 넣기(objektas_nuoroda, 2); return; }
        if (Word_SMS(pavadinimas_konstanta, "setLayout") && Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int schema_nuoroda = 빼기(2), objektas_nuoroda = 빼기(2); if (화면객체(objektas_nuoroda) && schema_nuoroda != 0) triktis_VALUE("only absolute layout (null) is supported"); return; }
        if (Word_SMS(pavadinimas_konstanta, "add") && (Word_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean schema_sąlyga = Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (schema_sąlyga) 빼기(2);
            int vaikas_nuoroda = 빼기(2), objektas_nuoroda = 빼기(2); if (!화면객체(vaikas_nuoroda) || !화면객체(objektas_nuoroda)) return;
            if (naudotojas.화면연결(2, 힙[objektas_nuoroda + 2], 힙[vaikas_nuoroda + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[vaikas_nuoroda + 11] = objektas_nuoroda; 힙참조[vaikas_nuoroda + 11] = 1; if (!schema_sąlyga) 넣기(vaikas_nuoroda, 2); return;
        }
        if (Word_SMS(pavadinimas_konstanta, "setBounds") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), x_koordinatė = 빼기(1), objektas_nuoroda = 빼기(2); if (!화면객체(objektas_nuoroda)) return;
            if (naudotojas.화면연결(1, 힙[objektas_nuoroda + 2], x_koordinatė, 세로좌표, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[objektas_nuoroda + 5] = x_koordinatė; 힙[objektas_nuoroda + 6] = 세로좌표; 힙[objektas_nuoroda + 7] = 너비; 힙[objektas_nuoroda + 8] = 높이; return;
        }
        if (Word_SMS(pavadinimas_konstanta, "setSize") && Word_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), objektas_nuoroda = 빼기(2); if (!화면객체(objektas_nuoroda)) return;
            if (naudotojas.화면연결(1, 힙[objektas_nuoroda + 2], 힙[objektas_nuoroda + 5], 힙[objektas_nuoroda + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[objektas_nuoroda + 7] = 너비; 힙[objektas_nuoroda + 8] = 높이; } return;
        }
        if (Word_SMS(pavadinimas_konstanta, "setLocationRelativeTo") && Word_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), objektas_nuoroda = 빼기(2); if (!화면객체(objektas_nuoroda)) return; if (상대배치 != 0) { triktis_VALUE("only screen centering supported"); return; } 힙[objektas_nuoroda + 5] = (naudotojas.화면너비() - 힙[objektas_nuoroda + 7]) / 2; 힙[objektas_nuoroda + 6] = (naudotojas.화면높이() - 힙[objektas_nuoroda + 8]) / 2; naudotojas.화면연결(1, 힙[objektas_nuoroda + 2], 힙[objektas_nuoroda + 5], 힙[objektas_nuoroda + 6], 힙[objektas_nuoroda + 7], 힙[objektas_nuoroda + 8]); return; }
        if (Word_SMS(pavadinimas_konstanta, "setDefaultCloseOperation") && Word_SMS(서술상수, "(I)V")) { int strategija = 빼기(1), objektas_nuoroda = 빼기(2); if (화면객체(objektas_nuoroda)) { if (strategija < 0 || strategija > 3) 예외던짐(9, "close policy"); else { 힙[objektas_nuoroda + 10] = strategija; naudotojas.화면연결(7, 힙[objektas_nuoroda + 2], strategija, 0, 0, 0); } } return; }
        if (Word_SMS(pavadinimas_konstanta, "setVisible") && Word_SMS(서술상수, "(Z)V")) { int duomenys_VALUE = 빼기(1), objektas_nuoroda = 빼기(2); if (화면객체(objektas_nuoroda)) { int 처리값 = naudotojas.화면연결(3, 힙[objektas_nuoroda + 2], duomenys_VALUE, 0, 0, 0); if (처리값 < 0) triktis_VALUE("Swing requires a standalone interactive command"); else 힙[objektas_nuoroda + 9] = duomenys_VALUE; } return; }
        if (Word_SMS(pavadinimas_konstanta, "dispose") && Word_SMS(서술상수, "()V")) { int objektas_nuoroda = 빼기(2); if (화면객체(objektas_nuoroda)) { naudotojas.화면연결(4, 힙[objektas_nuoroda + 2], 0, 0, 0, 0); 힙[objektas_nuoroda + 9] = 0; } return; }
        if (Word_SMS(pavadinimas_konstanta, "repaint") || Word_SMS(pavadinimas_konstanta, "validate")) { int objektas_nuoroda = 빼기(2); if (!화면객체(objektas_nuoroda) || !Word_SMS(서술상수, "()V")) return; naudotojas.화면연결(1, 힙[objektas_nuoroda + 2], 힙[objektas_nuoroda + 5], 힙[objektas_nuoroda + 6], 힙[objektas_nuoroda + 7], 힙[objektas_nuoroda + 8]); return; }
        if (Word_SMS(pavadinimas_konstanta, "isVisible") && Word_SMS(서술상수, "()Z")) { int objektas_nuoroda = 빼기(2); if (화면객체(objektas_nuoroda)) 넣기(힙[objektas_nuoroda + 9], 1); return; }
        triktis_VALUE("unsupported Swing method (native subset)");
    }
    static void išsiųsti_įvykis(int tikslas_ADDRESS, int įvykis_numeris, boolean Lietuvių) {
        if (tikslas_ADDRESS < 1 || 힙[tikslas_ADDRESS] < 32) { triktis_VALUE("Java event listener required"); return; }
        int Failas_INDEX = pavadinimas_metodas(힙[tikslas_ADDRESS] - 32, įvykis_numeris == 0 ? (Lietuvių ? "Vykdyti" : "run") : (Lietuvių ? "gauti_gavinys" : "actionPerformed"), įvykis_numeris == 0 ? "()V" : (Lietuvių ? "(LLietuvių/savas/gavinys_pranešimas;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (Failas_INDEX < 0) { triktis_VALUE("event callback missing"); return; }
        dabartinis_gija = 0; gija_COUNT = 1; kadras_INDEX = 0; gija_Būsena[0] = 1; kadras_eilė[0] = 0; kadras_užraktas[0] = 틀초기화[0] = 0; keisti_užklausa = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 128; Loop_INDEX++) { vietinis_VALUE[Loop_INDEX] = vietinis_TYPE[Loop_INDEX] = 0; }
        kadras_metodas[0] = Failas_INDEX; kadras_padėtis[0] = metodas_Start[Failas_INDEX]; vietinis_VALUE[0] = tikslas_ADDRESS; vietinis_TYPE[0] = 2;
        if (įvykis_numeris != 0) { vietinis_VALUE[1] = įvykis_numeris; vietinis_TYPE[1] = 2; }
        사건중 = true; Vykdyti_komanda(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!KLAIDA) {
            if (나중수 > 0) { int tikslas_ADDRESS = 나중실행[0], Lietuvių = 나중한국어[0]; for (int Loop_INDEX = 1; Loop_INDEX < 나중수; Loop_INDEX++) { 나중실행[Loop_INDEX - 1] = 나중실행[Loop_INDEX]; 나중한국어[Loop_INDEX - 1] = 나중한국어[Loop_INDEX]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; išsiųsti_įvykis(tikslas_ADDRESS, 0, Lietuvių != 0); continue; }
            if (naudotojas.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int įvykis_numeris = naudotojas.화면연결(5, 0, 0, 0, 0, 0); if (įvykis_numeris == 0) continue;
            if (įvykis_numeris < 0) { triktis_VALUE("GUI event I/O failed"); return; }
            int paskyra_VALUE = įvykis_numeris & 65535; if (paskyra_VALUE < 1 || paskyra_VALUE > 32) continue; int objektas_nuoroda = 화면참조[paskyra_VALUE - 1]; if (objektas_nuoroda == 0) continue;
            if ((įvykis_numeris & 65536) != 0) {
                if (힙[objektas_nuoroda + 10] != 0) 힙[objektas_nuoroda + 9] = 0;
                if (힙[objektas_nuoroda + 10] == 3) for (int Loop_INDEX = 0; Loop_INDEX < 32; Loop_INDEX++) if (화면참조[Loop_INDEX] != 0 && 힙[화면참조[Loop_INDEX]] == 24) naudotojas.화면연결(4, Loop_INDEX + 1, 0, 0, 0, 0);
            } else if (힙[objektas_nuoroda + 4] != 0) {
                int 안내참조 = priskirti_Saugykla(29, 2); if (KLAIDA) return; 힙[안내참조 + 2] = objektas_nuoroda; 힙[안내참조 + 3] = 힙[objektas_nuoroda + 12]; 힙참조[안내참조 + 2] = 1; išsiųsti_įvykis(힙[objektas_nuoroda + 4], 안내참조, 힙[objektas_nuoroda + 12] != 0);
            }
        }
    }
    public static int Paleisti() {
        if (naudotojas.인수개수() == 1 && 자바도구.같음(naudotojas.Argumentai(0), "-version")) {
            naudotojas.Rašymas("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (naudotojas.인수개수() < 1) { naudotojas.Rašymas("Usage: java CLASS [ARGS]\n"); return 2; }
        įrašas_klasė_Apibrėžtis = įkelti_klasė_Apibrėžtis(organizuoti_simbolis(naudotojas.Argumentai(0))); if (KLAIDA || įrašas_klasė_Apibrėžtis < 0) return 1;
        int įrašas_p_VALUE = pavadinimas_metodas(įrašas_klasė_Apibrėžtis, "Paleisti", "()V");
        boolean 한국어진입 = įrašas_p_VALUE >= 0 && (metodas_prieiga[įrašas_p_VALUE] & 9) == 9;
        if (!한국어진입) įrašas_p_VALUE = pavadinimas_metodas(įrašas_klasė_Apibrėžtis, "main", "([Ljava/lang/String;)V");
        if (įrašas_p_VALUE < 0 || (metodas_prieiga[įrašas_p_VALUE] & 9) != 9) triktis_VALUE("public static void Paleisti() or main(String[] args) required");
        if (KLAIDA) return 1;
        int Argumentai = priskirti_Saugykla(3, naudotojas.인수개수() - 1); masyvo_elementas[Argumentai] = -1;
        for (int numeris = 1; numeris < naudotojas.인수개수() && !KLAIDA; numeris++) 힙[Argumentai + 1 + numeris] = organizuoti_simbolis(naudotojas.Argumentai(numeris));
        kadras_INDEX = 0; kadras_metodas[0] = įrašas_p_VALUE; kadras_padėtis[0] = metodas_Start[įrašas_p_VALUE]; vietinis_VALUE[0] = 한국어진입 ? 0 : Argumentai; vietinis_TYPE[0] = 한국어진입 ? 0 : 2;
        gija_Būsena[0] = 1; gija_objektas[0] = priskirti_Saugykla(13, 2);
        Vykdyti_komanda(); if (!KLAIDA) 화면사건들(); return KLAIDA ? 1 : 0;
    }
}
