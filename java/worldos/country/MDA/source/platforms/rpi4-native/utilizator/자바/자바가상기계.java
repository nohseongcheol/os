// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Fișier/operand_Teanc/referință/ramură 경계를 executa_comandă 중 검사한다. */
public final class 자바가상기계 {
    static int[] Fișier = new int[16 * 16384], fișier_temporar = new int[16384], nume_de_fișier_SMS = new int[512];
    static int[] constantă_eticheta = new int[8192], 상가 = new int[8192], constantă_SECOND_VALUE = new int[8192], șir_referință = new int[8192];
    static int[] metodă_nume_SMS = new int[512], metodă_Tip = new int[512], metodă_acces = new int[512], metodă_proprietar = new int[512];
    static int[] metodă_buta = new int[512], metodă_termina_un_apel = new int[512], metodă_Teanc = new int[512], 함수지역 = new int[512];
    static int[] metodă_argument_COUNT = new int[512], metodă_argument_Tip = new int[8192], metodă_restitui = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] local_VALUE = new int[16384], local_Tip = new int[16384], operand_Teanc_VALUE = new int[16384], operand_Teanc_Tip = new int[16384];
    static int[] cadru_metodă = new int[128], cadru_poziție = new int[128], cadru_Teanc = new int[128], 틀명령 = new int[128], 틀초기화 = new int[128];
    static int[] Clasă_Definiție_nume = new int[16], Clasă_Definiție_dimensiona = new int[16], Clasă_Definiție_părinte = new int[16], Clasă_Definiție_Stare = new int[16], 종칸수 = new int[16], 종초기화 = new int[16];
    static int[] Clasă_interfață = new int[16 * 16], Clasă_interfață_COUNT = new int[16];
    static int[] 칸이름 = new int[512], 칸형 = new int[512], 칸주인 = new int[512], 칸권한 = new int[512], 칸위치 = new int[512], 칸값 = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], element_vector = new int[32768], Store_întreg = new int[256];
    static int Mărime, 읽기위치, metodă_COUNT, nume_de_clasă, cadru_INDEX = -1, 힙끝 = 1, restitui_Tip;
    static int Clasă_Definiție_COUNT, 칸수, 잡기수, 현재읽는종, 던진객체, 잠시수, afișa_COUNT, Colecție_COUNT;
    static int curent_fir, fir_COUNT = 1, intrare_Clasă_Definiție;
    static int[] fir_cadru = new int[4], fir_Stare = new int[4], fir_obiect = new int[4], fir_țintă = new int[4], 가닥대기 = new int[4];
    static boolean eroare, schimba_cerere;
    static int[] blocare_proprietar = new int[32768], 잠금깊이 = new int[32768], cadru_blocare = new int[128], Clasă_blocare = new int[16], Clasă_fir = new int[16];

    static void eroare_VALUE(String Word_SMS) {
        if (eroare) return;
        int zonă_cod = 0;
        if (자바도구.같음(Word_SMS, "ArithmeticException: / by zero")) zonă_cod = 4;
        if (자바도구.같음(Word_SMS, "NullPointerException") || 자바도구.같음(Word_SMS, "null or invalid array")) zonă_cod = 5;
        if (자바도구.같음(Word_SMS, "ArrayIndexOutOfBoundsException")) zonă_cod = 7;
        if (자바도구.같음(Word_SMS, "StringIndexOutOfBoundsException")) zonă_cod = 8;
        if (자바도구.같음(Word_SMS, "NumberFormatException")) zonă_cod = 10;
        if (자바도구.같음(Word_SMS, "FileNotFoundException: file open failed")) zonă_cod = 12;
        if (자바도구.같음(Word_SMS, "IOException: stream closed") || 자바도구.같음(Word_SMS, "IOException: read failed") || 자바도구.같음(Word_SMS, "IOException: write failed")) zonă_cod = 11;
        if (자바도구.같음(Word_SMS, "ClassCastException")) zonă_cod = 14;
        if (자바도구.같음(Word_SMS, "NegativeArraySizeException")) zonă_cod = 15;
        if (zonă_cod != 0 && cadru_INDEX >= 0) { 예외던짐(zonă_cod, Word_SMS); return; }
        utilizator.Scriere("JVM error: "); utilizator.Scriere(Word_SMS); utilizator.scriere_caracter_VALUE(10); eroare = true;
    }
    static boolean clip(int Pornește, int lungime_VALUE) {
        if (Pornește < 0 || Pornește >= Fișier.length || lungime_VALUE < 0) return false;
        int Clasă_Definiție = Pornește / 16384;
        return Pornește % 16384 <= Clasă_Definiție_dimensiona[Clasă_Definiție] && lungime_VALUE <= Clasă_Definiție_dimensiona[Clasă_Definiție] - Pornește % 16384;
    }
    static int byte_VALUE() {
        if (!clip(읽기위치, 1)) { eroare_VALUE("truncated class file"); return 0; }
        return Fișier[읽기위치++];
    }
    static int 짧은수() { return byte_VALUE() << 8 | byte_VALUE(); }
    static int întreg() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int lungime_VALUE) { if (!clip(읽기위치, lungime_VALUE)) eroare_VALUE("invalid attribute size"); else 읽기위치 += lungime_VALUE; }
    static boolean verifica_constantă(int 수, int 종류) {
        if (수 <= 0 || 수 >= constantă_eticheta.length || constantă_eticheta[수] != 종류) { eroare_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_zonă(int Pornește, int lungime_VALUE, String Word_SMS) {
        if (!clip(Pornește, lungime_VALUE)) return false;
        int 읽는자리 = Pornește, 끝 = Pornește + lungime_VALUE;
        for (int Loop_INDEX = 0; Loop_INDEX < Word_SMS.length(); Loop_INDEX++) {
            int cod_caracter = Word_SMS.charAt(Loop_INDEX);
            if (cod_caracter > 0 && cod_caracter < 128) { if (읽는자리 >= 끝 || Fișier[읽는자리++] != cod_caracter) return false; }
            else if (cod_caracter < 2048) {
                if (읽는자리 + 2 > 끝 || Fișier[읽는자리++] != (192 | (cod_caracter >> 6)) || Fișier[읽는자리++] != (128 | (cod_caracter & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Fișier[읽는자리++] != (224 | (cod_caracter >> 12)) || Fișier[읽는자리++] != (128 | ((cod_caracter >> 6) & 63)) || Fișier[읽는자리++] != (128 | (cod_caracter & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean Word_SMS(int constantă_VALUE, String Word_SMS) { return verifica_constantă(constantă_VALUE, 1) && SMS_zonă(상가[constantă_VALUE], constantă_SECOND_VALUE[constantă_VALUE], Word_SMS); }
    static boolean 같은말(int 가, int SECOND_operand) {
        if (!verifica_constantă(가, 1) || !verifica_constantă(SECOND_operand, 1) || constantă_SECOND_VALUE[가] != constantă_SECOND_VALUE[SECOND_operand]) return false;
        for (int 수 = 0; 수 < constantă_SECOND_VALUE[가]; 수++) if (Fișier[상가[가] + 수] != Fișier[상가[SECOND_operand] + 수]) return false;
        return true;
    }
    static int nume_de_clasă_SMS(int 수) { return verifica_constantă(수, 7) && verifica_constantă(상가[수], 1) ? 상가[수] : 0; }
    static int referință_nume(int 수) { return verifica_constantă(수, 12) && verifica_constantă(상가[수], 1) ? 상가[수] : 0; }
    static int referință_Tip(int 수) { return verifica_constantă(수, 12) && verifica_constantă(constantă_SECOND_VALUE[수], 1) ? constantă_SECOND_VALUE[수] : 0; }
    static int 서술형(int 끝, boolean 빈형) {
        if (읽기위치 >= 끝) { eroare_VALUE("invalid descriptor"); return 0; }
        int VALUE = byte_VALUE();
        if (VALUE == 'V' && 빈형) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int Pornește = 읽기위치;
            while (읽기위치 < 끝 && Fișier[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Pornește) eroare_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        eroare_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int funcție_VALUE) {
        int Anteriorul_element = 읽기위치, 수 = metodă_Tip[funcție_VALUE];
        if (!verifica_constantă(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + constantă_SECOND_VALUE[수];
        if (byte_VALUE() != '(') eroare_VALUE("invalid method descriptor");
        int element_COUNT = 0;
        while (!eroare && 읽기위치 < 끝 && Fișier[읽기위치] != ')') {
            if (element_COUNT == 16) { eroare_VALUE("too many method arguments"); break; }
            metodă_argument_Tip[funcție_VALUE * 16 + element_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || byte_VALUE() != ')') eroare_VALUE("invalid method descriptor");
        metodă_restitui[funcție_VALUE] = 서술형(끝, true); metodă_argument_COUNT[funcție_VALUE] = element_COUNT;
        if (읽기위치 != 끝) eroare_VALUE("invalid method descriptor");
        읽기위치 = Anteriorul_element;
    }
    static int 상번호() { int VALUE = 짧은수(); return VALUE == 0 ? 0 : 현재읽는종 * 512 + VALUE; }
    static int 명상수() { return metodă_proprietar[cadru_metodă[cadru_INDEX]] * 512 + 명짧(); }
    static void 속성건너() {
        int element_COUNT = 짧은수();
        for (int 수 = 0; 수 < element_COUNT && !eroare; 수++) { verifica_constantă(상번호(), 1); 건너(întreg()); }
    }
    static int comandă_lungime(int VALUE) {
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
    static int poziție_întreg(int 읽는자리) {
        if (!clip(읽는자리, 4)) { eroare_VALUE("truncated bytecode operand"); return 0; }
        return Fișier[읽는자리] << 24 | Fișier[읽는자리 + 1] << 16 | Fișier[읽는자리 + 2] << 8 | Fișier[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Pornește, int 끝) {
        int VALUE = Fișier[읽는자리], lungime_VALUE = comandă_lungime(VALUE);
        if (VALUE == 170 || VALUE == 171) {
            int BASE_poziție = 읽는자리 + 1;
            while ((BASE_poziție - Pornește) % 4 != 0) BASE_poziție++;
            if (끝 - BASE_poziție < (VALUE == 170 ? 12 : 8)) return 0;
            int intrare_COUNT = VALUE == 170 ? poziție_întreg(BASE_poziție + 8) - poziție_întreg(BASE_poziție + 4) + 1 : poziție_întreg(BASE_poziție + 4);
            if (intrare_COUNT < 0 || intrare_COUNT > 2048) return 0;
            lungime_VALUE = BASE_poziție - 읽는자리 + (VALUE == 170 ? 12 + 4 * intrare_COUNT : 8 + 8 * intrare_COUNT);
        }
        if (VALUE == 196 && 읽는자리 + 1 < 끝) {
            int Word_date = Fișier[읽는자리 + 1]; lungime_VALUE = Word_date == 132 ? 6 : (Word_date == 21 || Word_date == 25 || Word_date == 54 || Word_date == 58) ? 4 : 0;
        }
        return lungime_VALUE > 0 && lungime_VALUE <= 끝 - 읽는자리 ? lungime_VALUE : 0;
    }
    static void verifica_destinație_VALUE(int destinație_VALUE, int funcție_VALUE) {
        if (destinație_VALUE < metodă_buta[funcție_VALUE] || destinație_VALUE >= metodă_termina_un_apel[funcție_VALUE] || 경계[destinație_VALUE] != funcție_VALUE + 1) eroare_VALUE("invalid branch target");
    }
    static void 클래스읽기(int Clasă_Definiție) {
        현재읽는종 = Clasă_Definiție; 읽기위치 = Clasă_Definiție * 16384; Mărime = 읽기위치 + Clasă_Definiție_dimensiona[Clasă_Definiție];
        if (întreg() != 0xcafebabe) { eroare_VALUE("not a class file"); return; }
        int 부판 = 짧은수(), versiune_VALUE = 짧은수();
        if (versiune_VALUE < 45 || versiune_VALUE > 52 || 부판 != 0) { eroare_VALUE("supported class versions: 45..52, minor 0"); return; }
        int constantă_COUNT = 짧은수(), BASE_poziție = Clasă_Definiție * 512;
        if (constantă_COUNT < 1 || constantă_COUNT > 512) { eroare_VALUE("constant pool limit (511)"); return; }
        for (int intrare_COUNT = 1; intrare_COUNT < constantă_COUNT && !eroare; intrare_COUNT++) {
            int 수 = BASE_poziție + intrare_COUNT, 종류 = byte_VALUE(); constantă_eticheta[수] = 종류;
            if (종류 == 1) { constantă_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(constantă_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = întreg();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); constantă_SECOND_VALUE[수] = 상번호(); }
            else eroare_VALUE("unsupported constant type");
        }
        int permisiune_VALUE = 짧은수();
        if ((permisiune_VALUE & (0x2000 | 0x4000)) != 0) eroare_VALUE("annotation/enum class unsupported");
        Clasă_Definiție_nume[Clasă_Definiție] = nume_de_clasă_SMS(상번호());
        Clasă_Definiție_părinte[Clasă_Definiție] = nume_de_clasă_SMS(상번호());
        int interfață_COUNT = 짧은수(); if (interfață_COUNT > 16) { eroare_VALUE("interface count limit"); return; }
        Clasă_interfață_COUNT[Clasă_Definiție] = interfață_COUNT;
        for (int Loop_INDEX = 0; Loop_INDEX < interfață_COUNT; Loop_INDEX++) Clasă_interfață[Clasă_Definiție * 16 + Loop_INDEX] = nume_de_clasă_SMS(상번호());
        int câmp_COUNT = 짧은수();
        if (câmp_COUNT > 512 - 칸수) { eroare_VALUE("field count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < câmp_COUNT && !eroare; Loop_INDEX++) {
            int Fișier_INDEX = 칸수++; 칸주인[Fișier_INDEX] = Clasă_Definiție; 칸권한[Fișier_INDEX] = 짧은수(); 칸이름[Fișier_INDEX] = 상번호(); 칸형[Fișier_INDEX] = 상번호();
            verifica_constantă(칸이름[Fișier_INDEX], 1); verifica_constantă(칸형[Fișier_INDEX], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[칸형[Fișier_INDEX]]; int zonă_cod = 서술형(읽기위치 + constantă_SECOND_VALUE[칸형[Fișier_INDEX]], false); 읽기위치 = 보존값;
            if ((칸권한[Fișier_INDEX] & 8) == 0) 칸위치[Fișier_INDEX] = 종칸수[Clasă_Definiție]++;
            int atribut_date = 짧은수();
            for (int internă_poziție = 0; internă_poziție < atribut_date && !eroare; internă_poziție++) {
                int nume_constantă = 상번호(), 유효길이 = întreg();
                if (Word_SMS(nume_constantă, "ConstantValue") && 유효길이 == 2) {
                    int date_VALUE = 상번호();
                    if (zonă_cod == 1 && verifica_constantă(date_VALUE, 3)) 칸값[Fișier_INDEX] = 상가[date_VALUE];
                    else if (zonă_cod == 2 && verifica_constantă(date_VALUE, 8)) 칸값[Fișier_INDEX] = constantă_SMS(상가[date_VALUE]);
                } else 건너(유효길이);
            }
        }
        int element_COUNT = 짧은수();
        if (element_COUNT > 512 - metodă_COUNT) { eroare_VALUE("method count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < element_COUNT && !eroare; Loop_INDEX++) {
            int 수 = metodă_COUNT++; metodă_proprietar[수] = Clasă_Definiție;
            metodă_acces[수] = 짧은수(); metodă_nume_SMS[수] = 상번호(); metodă_Tip[수] = 상번호();
            verifica_constantă(metodă_nume_SMS[수], 1); 서술읽기(수);
            if ((metodă_acces[수] & 8) == 0) {
                if (metodă_argument_COUNT[수] == 16) { eroare_VALUE("too many instance method arguments"); return; }
                for (int Comparație_poziție = metodă_argument_COUNT[수]; Comparație_poziție > 0; Comparație_poziție--) metodă_argument_Tip[수 * 16 + Comparație_poziție] = metodă_argument_Tip[수 * 16 + Comparație_poziție - 1];
                metodă_argument_Tip[수 * 16] = 2; metodă_argument_COUNT[수]++;
            }
            if ((metodă_acces[수] & 0x100) != 0) eroare_VALUE("user native method unsupported");
            if (Word_SMS(metodă_nume_SMS[수], "<clinit>")) 종초기화[Clasă_Definiție] = 수 + 1;
            for (int frontală_VALUE = 0; frontală_VALUE < 수; frontală_VALUE++) if (metodă_proprietar[frontală_VALUE] == Clasă_Definiție && 같은말(metodă_nume_SMS[frontală_VALUE], metodă_nume_SMS[수]) && 같은말(metodă_Tip[frontală_VALUE], metodă_Tip[수])) eroare_VALUE("duplicate method");
            int atribut_COUNT = 짧은수();
            for (int atribut_VALUE = 0; atribut_VALUE < atribut_COUNT && !eroare; atribut_VALUE++) {
                int Nume = 상번호(), lungime_VALUE = întreg(), Pornește = 읽기위치;
                if (!clip(Pornește, lungime_VALUE)) { eroare_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Nume, "Code")) {
                    if (metodă_buta[수] != 0) eroare_VALUE("duplicate Code attribute");
                    metodă_Teanc[수] = 짧은수(); 함수지역[수] = 짧은수(); int cod_lungime = întreg();
                    if (metodă_Teanc[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < metodă_argument_COUNT[수]
                        || cod_lungime < 1 || cod_lungime > 8192) eroare_VALUE("method memory limits exceeded");
                    metodă_buta[수] = 읽기위치; 건너(cod_lungime); metodă_termina_un_apel[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { eroare_VALUE("exception table limit"); return; }
                    for (int internă_poziție = 0; internă_poziție < 잡는수; internă_poziție++) {
                        int eroare_referință = 잡기수++; 잡기함수[eroare_referință] = 수;
                        잡기시작[eroare_referință] = metodă_buta[수] + 짧은수(); 잡기끝[eroare_referință] = metodă_buta[수] + 짧은수();
                        잡기위치[eroare_referință] = metodă_buta[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[eroare_referință] = 부호값 == 0 ? 0 : nume_de_clasă_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != Pornește + lungime_VALUE) eroare_VALUE("Code attribute size mismatch");
                } else 건너(lungime_VALUE);
            }
            if ((metodă_acces[수] & 0x400) != 0) continue;
            if (metodă_buta[수] == 0) eroare_VALUE("missing Code attribute");
            int 칸 = metodă_buta[수];
            while (칸 < metodă_termina_un_apel[수] && !eroare) {
                int lungime_VALUE = 길이읽기(칸, metodă_buta[수], metodă_termina_un_apel[수]);
                if (lungime_VALUE == 0) { eroare_VALUE("unsupported or truncated bytecode"); break; }
                경계[칸] = 수 + 1; 칸 += lungime_VALUE;
            }
            칸 = metodă_buta[수];
            while (칸 < metodă_termina_un_apel[수] && !eroare) {
                int VALUE = Fișier[칸];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) verifica_destinație_VALUE(칸 + (short)(Fișier[칸 + 1] << 8 | Fișier[칸 + 2]), 수);
                if (VALUE == 200) verifica_destinație_VALUE(칸 + poziție_întreg(칸 + 1), 수);
                if (VALUE == 170 || VALUE == 171) {
                    int 읽는자리 = 칸 + 1; while ((읽는자리 - metodă_buta[수]) % 4 != 0) 읽는자리++;
                    verifica_destinație_VALUE(칸 + poziție_întreg(읽는자리), 수);
                    int intrare_COUNT = VALUE == 170 ? poziție_întreg(읽는자리 + 8) - poziție_întreg(읽는자리 + 4) + 1 : poziție_întreg(읽는자리 + 4);
                    읽는자리 += VALUE == 170 ? 12 : 8;
                    for (int internă_poziție = 0; internă_poziție < intrare_COUNT; internă_poziție++) verifica_destinație_VALUE(칸 + poziție_întreg(읽는자리 + internă_poziție * (VALUE == 170 ? 4 : 8) + (VALUE == 170 ? 0 : 4)), 수);
                }
                칸 += 길이읽기(칸, metodă_buta[수], metodă_termina_un_apel[수]);
            }
            for (int internă_poziție = 0; internă_poziție < 잡기수; internă_poziție++) if (잡기함수[internă_poziție] == 수) {
                verifica_destinație_VALUE(잡기시작[internă_poziție], 수); verifica_destinație_VALUE(잡기위치[internă_poziție], 수);
                if (잡기끝[internă_poziție] != metodă_termina_un_apel[수]) verifica_destinație_VALUE(잡기끝[internă_poziție], 수);
                if (잡기시작[internă_poziție] >= 잡기끝[internă_poziție]) eroare_VALUE("invalid exception range");
            }
        }
        if (!eroare) 속성건너();
        if (읽기위치 != Mărime) eroare_VALUE("extra class file data");
    }
    static int aloca_Stocare(int 종류, int lungime_VALUE) { return 새기억(종류, lungime_VALUE); }
    static boolean obiect_VALUE(int referință, int 종류) {
        if (!객체유효(referință)) return false;
        if (힙[referință] != 종류) { eroare_VALUE("object type mismatch"); return false; }
        return true;
    }
    static int constantă_SMS(int INDEX) {
        if (!verifica_constantă(INDEX, 1)) return 0;
        if (șir_referință[INDEX] != 0) return șir_referință[INDEX];
        int referință = aloca_Stocare(1, constantă_SECOND_VALUE[INDEX]); if (eroare) return 0;
        int 끝 = 상가[INDEX] + constantă_SECOND_VALUE[INDEX], 수 = 상가[INDEX], lungime_VALUE = 0;
        while (수 < 끝 && !eroare) {
            int VALUE = Fișier[수++];
            if (VALUE == 0) eroare_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && 수 < 끝) {
                int Următorul_element = Fișier[수++];
                if ((Următorul_element & 192) != 128) eroare_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | Următorul_element & 63;
                if (VALUE != 0 && VALUE < 128) eroare_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && 수 + 1 < 끝) {
                int 가 = Fișier[수++], SECOND_operand = Fișier[수++];
                if ((가 & 192) != 128 || (SECOND_operand & 192) != 128) eroare_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | SECOND_operand & 63;
                if (VALUE < 2048) eroare_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) eroare_VALUE("invalid modified UTF-8");
            힙[referință + 2 + lungime_VALUE++] = VALUE;
        }
        힙[referință + 1] = lungime_VALUE; șir_referință[INDEX] = referință; return referință;
    }
    static int gazdă_caracter(String VALUE) {
        int referință = aloca_Stocare(1, VALUE.length()); if (eroare) return 0;
        for (int 수 = 0; 수 < VALUE.length(); 수++) 힙[referință + 2 + 수] = VALUE.charAt(수);
        return referință;
    }
    static void scriere_SMS(int referință) {
        if (referință == 0) { utilizator.Scriere("null"); return; }
        if (!obiect_VALUE(referință, 1)) return;
        for (int 수 = 0; 수 < 힙[referință + 1]; 수++) utilizator.scriere_caracter_VALUE(힙[referință + 2 + 수]);
    }
    static int cifră_caracter(int VALUE) {
        int referință = aloca_Stocare(1, 11); if (eroare) return 0;
        int lungime_VALUE = 0;
        if (VALUE < 0) 힙[referință + 2 + lungime_VALUE++] = '-'; else VALUE = -VALUE;
        int index_de_poziție = 1000000000; boolean Pornește = false;
        while (index_de_poziție != 0) {
            int 수 = -(VALUE / index_de_poziție);
            if (수 != 0 || Pornește || index_de_poziție == 1) { 힙[referință + 2 + lungime_VALUE++] = '0' + 수; Pornește = true; }
            VALUE %= index_de_poziție; index_de_poziție /= 10;
        }
        힙[referință + 1] = lungime_VALUE; return referință;
    }
    static int 정수해독(int referință) {
        if (!obiect_VALUE(referință, 1)) return 0;
        int lungime_VALUE = 힙[referință + 1], 수 = 0, VALUE = 0; boolean 음수 = false;
        if (lungime_VALUE > 0 && (힙[referință + 2] == '-' || 힙[referință + 2] == '+')) { 음수 = 힙[referință + 2] == '-'; 수++; }
        if (수 == lungime_VALUE) eroare_VALUE("NumberFormatException");
        for (; 수 < lungime_VALUE && !eroare; 수++) {
            int cifră_VALUE = 힙[referință + 2 + 수] - '0';
            if (cifră_VALUE < 0 || cifră_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && cifră_VALUE > (음수 ? 8 : 7)) eroare_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - cifră_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int Tip_VALUE) {
        if (eroare) return;
        if (cadru_INDEX < 0 || cadru_Teanc[cadru_INDEX] >= metodă_Teanc[cadru_metodă[cadru_INDEX]]) { eroare_VALUE("operand stack overflow"); return; }
        int 칸 = cadru_INDEX * 128 + cadru_Teanc[cadru_INDEX]++; operand_Teanc_VALUE[칸] = VALUE; operand_Teanc_Tip[칸] = Tip_VALUE;
    }
    static int 빼기(int Tip_VALUE) {
        if (eroare) return 0;
        if (cadru_INDEX < 0 || cadru_Teanc[cadru_INDEX] < 1) { eroare_VALUE("operand stack underflow"); return 0; }
        int 칸 = cadru_INDEX * 128 + --cadru_Teanc[cadru_INDEX]; restitui_Tip = operand_Teanc_Tip[칸];
        if (Tip_VALUE != 0 && restitui_Tip != Tip_VALUE) eroare_VALUE("operand type mismatch");
        if (restitui_Tip == 2) proteja_VALUE(operand_Teanc_VALUE[칸]);
        return operand_Teanc_VALUE[칸];
    }
    static void 지역읽기(int INDEX, int Tip_VALUE) {
        if (INDEX >= 함수지역[cadru_metodă[cadru_INDEX]] || INDEX < 0 || local_Tip[cadru_INDEX * 128 + INDEX] != Tip_VALUE) { eroare_VALUE("invalid or uninitialized local"); return; }
        넣기(local_VALUE[cadru_INDEX * 128 + INDEX], Tip_VALUE);
    }
    static void scriere_local(int INDEX, int Tip_VALUE) {
        if (INDEX >= 함수지역[cadru_metodă[cadru_INDEX]] || INDEX < 0) { eroare_VALUE("local index out of range"); return; }
        int VALUE = 빼기(Tip_VALUE); local_VALUE[cadru_INDEX * 128 + INDEX] = VALUE; local_Tip[cadru_INDEX * 128 + INDEX] = Tip_VALUE;
    }
    static int 명바() {
        int Poziție = cadru_poziție[cadru_INDEX];
        if (Poziție < metodă_buta[cadru_metodă[cadru_INDEX]] || Poziție >= metodă_termina_un_apel[cadru_metodă[cadru_INDEX]]) { eroare_VALUE("instruction pointer out of range"); return 0; }
        cadru_poziție[cadru_INDEX]++; return Fișier[Poziție];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void muta_VALUE_83b651b8(int Poziție) {
        int funcție_VALUE = cadru_metodă[cadru_INDEX];
        if (Poziție < metodă_buta[funcție_VALUE] || Poziție >= metodă_termina_un_apel[funcție_VALUE] || 경계[Poziție] != funcție_VALUE + 1) eroare_VALUE("invalid branch target");
        else cadru_poziție[cadru_INDEX] = Poziție;
    }
    static void 호출(int funcție_VALUE) {
        if (cadru_INDEX % 32 == 31) { eroare_VALUE("call stack limit (32)"); return; }
        int Următorul_element = cadru_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) local_Tip[Următorul_element * 128 + 수] = 0;
        for (int 수 = metodă_argument_COUNT[funcție_VALUE] - 1; 수 >= 0; 수--) {
            local_VALUE[Următorul_element * 128 + 수] = 빼기(metodă_argument_Tip[funcție_VALUE * 16 + 수]); local_Tip[Următorul_element * 128 + 수] = metodă_argument_Tip[funcție_VALUE * 16 + 수];
        }
        if (eroare) return;
        cadru_INDEX = Următorul_element; 틀초기화[cadru_INDEX] = 0; cadru_metodă[cadru_INDEX] = funcție_VALUE; cadru_poziție[cadru_INDEX] = metodă_buta[funcție_VALUE]; cadru_Teanc[cadru_INDEX] = 0;
    }
    static void restitui_KR(int Tip_VALUE) {
        if (Tip_VALUE != metodă_restitui[cadru_metodă[cadru_INDEX]]) { eroare_VALUE("return type mismatch"); return; }
        int VALUE = Tip_VALUE == 0 ? 0 : 빼기(Tip_VALUE);
        if (틀초기화[cadru_INDEX] != 0) Clasă_Definiție_Stare[틀초기화[cadru_INDEX] - 1] = 2;
        if (cadru_blocare[cadru_INDEX] != 0) { lansa_blocare(cadru_blocare[cadru_INDEX]); cadru_blocare[cadru_INDEX] = 0; }
        cadru_INDEX--; if (cadru_INDEX >= curent_fir * 32 && Tip_VALUE != 0) 넣기(VALUE, Tip_VALUE);
    }
    static int[] flux_nume_de_fișier = new int[64];
    static void Fișier_flux_Apel(int proprietar_VALUE, int Nume, int format_VALUE, int Comandă) {
        boolean Rezultat = Word_SMS(proprietar_VALUE, "java/io/FileOutputStream");
        int 종류 = Rezultat ? 6 : 5;
        if (Comandă == 183 && Word_SMS(Nume, "<init>")) {
            boolean 이어 = false;
            if (Rezultat && Word_SMS(format_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(format_VALUE, "(Ljava/lang/String;)V")) { eroare_VALUE("unsupported file stream constructor"); return; }
            int Fișier_intrare_nume = 빼기(2), flux_VALUE = 빼기(2);
            if (!obiect_VALUE(Fișier_intrare_nume, 1) || !obiect_VALUE(flux_VALUE, 종류) || eroare) return;
            if (힙[flux_VALUE + 3] != 0) { eroare_VALUE("file stream already initialized"); return; }
            int lungime_VALUE = 힙[Fișier_intrare_nume + 1];
            if (lungime_VALUE < 1 || lungime_VALUE > 63) { eroare_VALUE("invalid file name length"); return; }
            for (int 칸 = 0; 칸 < lungime_VALUE; 칸++) {
                int VALUE = 힙[Fișier_intrare_nume + 2 + 칸];
                if (VALUE < 1) { eroare_VALUE("invalid file stream path"); return; }
                flux_nume_de_fișier[칸] = VALUE;
            }
            flux_nume_de_fișier[lungime_VALUE] = 0;
            int 서술자 = utilizator.파일서술자열기(flux_nume_de_fișier, Rezultat ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { eroare_VALUE("FileNotFoundException: file open failed"); return; }
            힙[flux_VALUE + 2] = 서술자; 힙[flux_VALUE + 3] = 1;
            return;
        }
        if (Comandă != 182) { eroare_VALUE("invalid file stream invocation"); return; }
        if ((Rezultat && Word_SMS(Nume, "write") || !Rezultat && Word_SMS(Nume, "read"))
            && (Word_SMS(format_VALUE, Rezultat ? "([B)V" : "([B)I") || Word_SMS(format_VALUE, Rezultat ? "([BII)V" : "([BII)I"))) {
            boolean clip_VALUE = Word_SMS(format_VALUE, Rezultat ? "([BII)V" : "([BII)I");
            int intrare_COUNT = clip_VALUE ? 빼기(1) : 0, 시작점 = clip_VALUE ? 빼기(1) : 0, date_ARRAY = 빼기(2), obiect_referință = 빼기(2);
            if (!obiect_VALUE(date_ARRAY, 20) || !obiect_VALUE(obiect_referință, 종류)) return;
            if (!clip_VALUE) intrare_COUNT = 힙[date_ARRAY + 1];
            if (시작점 < 0 || intrare_COUNT < 0 || 시작점 > 힙[date_ARRAY + 1] - intrare_COUNT) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[obiect_referință + 3] == 0 || 힙[obiect_referință + 2] < 0) { eroare_VALUE("IOException: stream closed"); return; }
            int Finalizate_COUNT = 0;
            while (Finalizate_COUNT < intrare_COUNT && !eroare) {
                int 반환값 = Rezultat ? utilizator.파일한바이트쓰기(힙[obiect_referință + 2], 힙[date_ARRAY + 2 + 시작점 + Finalizate_COUNT]) : utilizator.파일한바이트읽기(힙[obiect_referință + 2]);
                if (반환값 < 0) { eroare_VALUE(Rezultat ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!Rezultat && 반환값 == 256) break;
                if (!Rezultat) 힙[date_ARRAY + 2 + 시작점 + Finalizate_COUNT] = (byte)반환값;
                Finalizate_COUNT++;
            }
            if (!Rezultat) 넣기(intrare_COUNT != 0 && Finalizate_COUNT == 0 ? -1 : Finalizate_COUNT, 1);
            return;
        }
        if (Rezultat && Word_SMS(Nume, "flush") && Word_SMS(format_VALUE, "()V")) { int obiect_referință = 빼기(2); if (obiect_VALUE(obiect_referință, 종류) && 힙[obiect_referință + 2] < 0) eroare_VALUE("IOException: stream closed"); return; }
        int Acțiuni = -1, VALUE = 0;
        if (Word_SMS(Nume, "close") && Word_SMS(format_VALUE, "()V")) Acțiuni = 0;
        if (!Rezultat && Word_SMS(Nume, "read") && Word_SMS(format_VALUE, "()I")) Acțiuni = 1;
        if (Rezultat && Word_SMS(Nume, "write") && Word_SMS(format_VALUE, "(I)V")) { Acțiuni = 2; VALUE = 빼기(1); }
        if (Acțiuni < 0) { eroare_VALUE("unsupported file stream method"); return; }
        int flux_VALUE = 빼기(2);
        if (!obiect_VALUE(flux_VALUE, 종류) || eroare) return;
        if (힙[flux_VALUE + 3] == 0) { eroare_VALUE("uninitialized file stream"); return; }
        int 서술자 = 힙[flux_VALUE + 2];
        if (Acțiuni == 0) {
            if (서술자 >= 0 && utilizator.파일서술자닫기(서술자) < 0) eroare_VALUE("IOException: close failed");
            힙[flux_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { eroare_VALUE("IOException: stream closed"); return; }
        if (Acțiuni == 1) {
            int KR = utilizator.파일한바이트읽기(서술자);
            if (KR < -1) eroare_VALUE("IOException: read failed"); else 넣기(KR == 256 ? -1 : KR, 1);
        } else if (utilizator.파일한바이트쓰기(서술자, VALUE) != 1) eroare_VALUE("IOException: write failed");
    }
    static void Apel_metodă(int INDEX, int Comandă) {
        if (INDEX <= 0 || INDEX >= constantă_eticheta.length || (constantă_eticheta[INDEX] != 10 && constantă_eticheta[INDEX] != 11)) { eroare_VALUE("invalid method reference"); return; }
        int proprietar_VALUE = nume_de_clasă_SMS(상가[INDEX]), Nume = referință_nume(constantă_SECOND_VALUE[INDEX]), format_VALUE = referință_Tip(constantă_SECOND_VALUE[INDEX]);
        if (eroare) return;
        if (기본호출(proprietar_VALUE, Nume, format_VALUE, Comandă)) return;
        if (Word_SMS(proprietar_VALUE, "java/io/FileInputStream") || Word_SMS(proprietar_VALUE, "java/io/FileOutputStream")) {
            Fișier_flux_Apel(proprietar_VALUE, Nume, format_VALUE, Comandă); return;
        }
        if (Comandă == 184 && Word_SMS(proprietar_VALUE, "java/lang/Integer") && Word_SMS(Nume, "parseInt") && Word_SMS(format_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Comandă == 182 && Word_SMS(proprietar_VALUE, "java/io/PrintStream") && (Word_SMS(Nume, "println") || Word_SMS(Nume, "print"))) {
            int Tip_VALUE = 0, VALUE = 0;
            if (Word_SMS(format_VALUE, "(I)V")) { Tip_VALUE = 1; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(Z)V")) { Tip_VALUE = 2; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(C)V")) { Tip_VALUE = 3; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(Ljava/lang/String;)V")) { Tip_VALUE = 4; VALUE = 빼기(2); }
            else if (!Word_SMS(format_VALUE, "()V") || !Word_SMS(Nume, "println")) eroare_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) eroare_VALUE("invalid PrintStream receiver");
            if (eroare) return;
            if (Tip_VALUE == 1) 자바도구.수쓰기(VALUE);
            if (Tip_VALUE == 2) utilizator.Scriere(VALUE == 0 ? "false" : "true");
            if (Tip_VALUE == 3) utilizator.scriere_caracter_VALUE(VALUE & 65535);
            if (Tip_VALUE == 4) scriere_SMS(VALUE);
            if (Word_SMS(Nume, "println")) utilizator.scriere_caracter_VALUE(10);
            return;
        }
        if (Comandă == 182 && Word_SMS(proprietar_VALUE, "java/lang/String")) {
            if (Word_SMS(Nume, "length") && Word_SMS(format_VALUE, "()I")) {
                int referință = 빼기(2); if (obiect_VALUE(referință, 1)) 넣기(힙[referință + 1], 1); return;
            }
            if (Word_SMS(Nume, "charAt") && Word_SMS(format_VALUE, "(I)C")) {
                int indice_VALUE = 빼기(1), referință = 빼기(2);
                if (obiect_VALUE(referință, 1)) {
                    if (indice_VALUE < 0 || indice_VALUE >= 힙[referință + 1]) eroare_VALUE("StringIndexOutOfBoundsException"); else 넣기(힙[referință + 2 + indice_VALUE], 1);
                }
                return;
            }
        }
        if (Word_SMS(proprietar_VALUE, "java/lang/StringBuilder")) {
            if (Comandă == 183 && Word_SMS(Nume, "<init>") && Word_SMS(format_VALUE, "()V")) { obiect_VALUE(빼기(2), 4); return; }
            if (Comandă == 182 && Word_SMS(Nume, "toString") && Word_SMS(format_VALUE, "()Ljava/lang/String;")) {
                int referință = 빼기(2); if (obiect_VALUE(referință, 4)) 넣기(힙[referință + 2] == 0 ? gazdă_caracter("") : 힙[referință + 2], 2); return;
            }
            if (Comandă == 182 && Word_SMS(Nume, "append")) {
                int SMS = 0;
                if (Word_SMS(format_VALUE, "(I)Ljava/lang/StringBuilder;")) SMS = cifră_caracter(빼기(1));
                else if (Word_SMS(format_VALUE, "(Z)Ljava/lang/StringBuilder;")) SMS = gazdă_caracter(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(format_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); SMS = aloca_Stocare(1, 1); if (!eroare) 힙[SMS + 2] = VALUE & 65535;
                }
                else if (Word_SMS(format_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { SMS = 빼기(2); if (SMS == 0) SMS = gazdă_caracter("null"); }
                else { eroare_VALUE("unsupported StringBuilder append"); return; }
                int referință = 빼기(2); if (!obiect_VALUE(referință, 4) || !obiect_VALUE(SMS, 1)) return;
                int frontală_VALUE = 힙[referință + 2], frontală_VALUE_lungime = frontală_VALUE == 0 ? 0 : 힙[frontală_VALUE + 1], ÎNAPOI_VALUE_lungime = 힙[SMS + 1];
                int 새글 = aloca_Stocare(1, frontală_VALUE_lungime + ÎNAPOI_VALUE_lungime); if (eroare) return;
                for (int 수 = 0; 수 < frontală_VALUE_lungime; 수++) 힙[새글 + 2 + 수] = 힙[frontală_VALUE + 2 + 수];
                for (int 수 = 0; 수 < ÎNAPOI_VALUE_lungime; 수++) 힙[새글 + 2 + frontală_VALUE_lungime + 수] = 힙[SMS + 2 + 수];
                힙[referință + 2] = 새글; 넣기(referință, 2); return;
            }
        }
        int Clasă_Definiție = FIND_Clasă_Definiție(proprietar_VALUE); if (Clasă_Definiție < 0 || eroare) return;
        int Fișier_INDEX = FIND_metodă(Clasă_Definiție, Nume, format_VALUE);
        if (Fișier_INDEX < 0) {
            for (int cod_caracter = Clasă_Definiție, intrare_COUNT = 0; cod_caracter >= 0 && intrare_COUNT < 16; intrare_COUNT++, cod_caracter = părinte_Clasă(cod_caracter))
                if (Word_SMS(Clasă_Definiție_părinte[cod_caracter], "java/lang/Thread")) { 가닥호출(Nume, format_VALUE, Comandă); return; }
            eroare_VALUE("NoSuchMethodError"); return;
        }
        if (((metodă_acces[Fișier_INDEX] & 8) != 0) != (Comandă == 184)) { eroare_VALUE("method static/instance mismatch"); return; }
        if (Comandă == 184) { if (!초기화(metodă_proprietar[Fișier_INDEX], 틀명령[cadru_INDEX])) return; }
        else {
            int 읽는자리 = cadru_Teanc[cadru_INDEX] - metodă_argument_COUNT[Fișier_INDEX];
            if (읽는자리 < 0 || operand_Teanc_Tip[cadru_INDEX * 128 + 읽는자리] != 2) { eroare_VALUE("invalid method receiver"); return; }
            int obiect_referință = operand_Teanc_VALUE[cadru_INDEX * 128 + 읽는자리];
            if (!객체유효(obiect_referință)) return;
            if (힙[obiect_referință] < 32 || !종포함(힙[obiect_referință] - 32, proprietar_VALUE)) { eroare_VALUE("method receiver type mismatch"); return; }
            if (Comandă != 183) Fișier_INDEX = FIND_metodă(힙[obiect_referință] - 32, Nume, format_VALUE);
        }
        if (Fișier_INDEX < 0 || (metodă_acces[Fișier_INDEX] & 0x400) != 0) { eroare_VALUE("AbstractMethodError"); return; }
        int blocare_referință = 0;
        if ((metodă_acces[Fișier_INDEX] & 32) != 0) {
            if (Comandă == 184) { int cod_caracter = metodă_proprietar[Fișier_INDEX]; if (Clasă_blocare[cod_caracter] == 0) Clasă_blocare[cod_caracter] = aloca_Stocare(8, 0); blocare_referință = Clasă_blocare[cod_caracter]; }
            else blocare_referință = operand_Teanc_VALUE[cadru_INDEX * 128 + cadru_Teanc[cadru_INDEX] - metodă_argument_COUNT[Fișier_INDEX]];
            if (!잠금얻기(blocare_referință)) { if (!eroare) cadru_poziție[cadru_INDEX] = 틀명령[cadru_INDEX]; return; }
        }
        호출(Fișier_INDEX); if (!eroare) cadru_blocare[cadru_INDEX] = blocare_referință;
    }
    static boolean 배열저장가능(int ARRAY_referință, int date_VALUE) {
        if (date_VALUE == 0 || element_vector[ARRAY_referință] == 0) return true;
        boolean 성공여부 = element_vector[ARRAY_referință] == -1 ? (date_VALUE > 0 && date_VALUE < 힙끝 && 힙[date_VALUE] == 1) : 맞는객체(date_VALUE, element_vector[ARRAY_referință]);
        if (!성공여부 && !eroare) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int 배열칸(int referință, int indice_VALUE, int Tip_VALUE) {
        if (!obiect_VALUE(referință, Tip_VALUE)) return 0;
        if (indice_VALUE < 0 || indice_VALUE >= 힙[referință + 1]) { eroare_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return referință + 2 + indice_VALUE;
    }
    static void executa_comandă() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (eroare) { if (던진객체 != 0) handle_excepție(); if (eroare || cadru_INDEX < curent_fir * 32) break; }
            if (cadru_INDEX < curent_fir * 32 || schimba_cerere || --조각 == 0) { if (!SWITCH_fir()) break; 조각 = 100; }
            if (cadru_INDEX == 0 && Clasă_Definiție_Stare[intrare_Clasă_Definiție] != 2 && !초기화(intrare_Clasă_Definiție, cadru_poziție[cadru_INDEX])) continue;
            if (cadru_INDEX == curent_fir * 32 && curent_fir != 0 && (metodă_acces[cadru_metodă[cadru_INDEX]] & 32) != 0 && cadru_blocare[cadru_INDEX] == 0) {
                int obiect_referință = fir_țintă[curent_fir]; if (!잠금얻기(obiect_referință)) { if (eroare) break; continue; } cadru_blocare[cadru_INDEX] = obiect_referință;
            }
            잠시수 = 0;
            if (--남음 == 0) { eroare_VALUE("instruction limit (500000)"); break; }
            int Pornește = cadru_poziție[cadru_INDEX]; 틀명령[cadru_INDEX] = Pornește; int VALUE = 명바();
            if (eroare) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = metodă_proprietar[cadru_metodă[cadru_INDEX]] * 512 + (VALUE == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= constantă_eticheta.length) eroare_VALUE("invalid ldc constant");
                else if (constantă_eticheta[수] == 3) 넣기(상가[수], 1);
                else if (constantă_eticheta[수] == 8) 넣기(constantă_SMS(상가[수]), 2);
                else eroare_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { scriere_local(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { scriere_local(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { scriere_local(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE >= 50 && VALUE <= 53) {
                int intrare_poziție = 빼기(1), obiect_referință = 빼기(2), zonă_cod = VALUE == 46 ? 2 : VALUE == 50 ? 3 : VALUE == 51 ? 20 : VALUE == 52 ? 22 : 23;
                if (VALUE == 51 && obiect_referință > 0 && obiect_referință < 힙끝 && 힙[obiect_referință] == 21) zonă_cod = 21;
                int 읽는자리 = 배열칸(obiect_referință, intrare_poziție, zonă_cod); if (!eroare) 넣기(힙[읽는자리], VALUE == 50 ? 2 : 1); continue;
            }
            if (VALUE == 79 || VALUE >= 83 && VALUE <= 86) {
                int intrare_referință = 빼기(VALUE == 83 ? 2 : 1), intrare_poziție = 빼기(1), obiect_referință = 빼기(2), zonă_cod = VALUE == 79 ? 2 : VALUE == 83 ? 3 : VALUE == 84 ? 20 : VALUE == 85 ? 22 : 23;
                if (VALUE == 84 && obiect_referință > 0 && obiect_referință < 힙끝 && 힙[obiect_referință] == 21) zonă_cod = 21;
                int 읽는자리 = 배열칸(obiect_referință, intrare_poziție, zonă_cod);
                if (!eroare && zonă_cod == 3 && !배열저장가능(obiect_referință, intrare_referință)) continue;
                if (!eroare) 힙[읽는자리] = zonă_cod == 20 ? (byte)intrare_referință : zonă_cod == 21 ? intrare_referință & 1 : zonă_cod == 22 ? (char)intrare_referință : zonă_cod == 23 ? (short)intrare_referință : intrare_referință;
                continue;
            }
            if (VALUE >= 87 && VALUE <= 95) { 스택명령(VALUE); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int SECOND_operand = 빼기(1), 가 = 빼기(1), KR = 0;
                if ((VALUE == 108 || VALUE == 112) && SECOND_operand == 0) { eroare_VALUE("ArithmeticException: / by zero"); continue; }
                if (VALUE == 96) KR = 가 + SECOND_operand;
                if (VALUE == 100) KR = 가 - SECOND_operand;
                if (VALUE == 104) KR = 가 * SECOND_operand;
                if (VALUE == 108) KR = 가 / SECOND_operand;
                if (VALUE == 112) KR = 가 % SECOND_operand;
                if (VALUE == 120) KR = 가 << SECOND_operand;
                if (VALUE == 122) KR = 가 >> SECOND_operand;
                if (VALUE == 124) KR = 가 >>> SECOND_operand;
                if (VALUE == 126) KR = 가 & SECOND_operand;
                if (VALUE == 128) KR = 가 | SECOND_operand;
                if (VALUE == 130) KR = 가 ^ SECOND_operand;
                넣기(KR, 1); continue;
            }
            if (VALUE == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALUE == 132) {
                int local_gamă = 명바(), increment_pas = (byte)명바(); 지역읽기(local_gamă, 1); 넣기(빼기(1) + increment_pas, 1); scriere_local(local_gamă, 1); continue;
            }
            if (VALUE >= 145 && VALUE <= 147) {
                int 수 = 빼기(1); 넣기(VALUE == 145 ? (byte)수 : VALUE == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                int destinație_VALUE = Pornește + (short)명짧(); boolean 갈까 = VALUE == 167;
                if (VALUE >= 153 && VALUE <= 158) {
                    int 수 = 빼기(1); 갈까 = VALUE == 153 ? 수 == 0 : VALUE == 154 ? 수 != 0 : VALUE == 155 ? 수 < 0 : VALUE == 156 ? 수 >= 0 : VALUE == 157 ? 수 > 0 : 수 <= 0;
                } else if (VALUE >= 159 && VALUE <= 166) {
                    int SECOND_operand = 빼기(VALUE >= 165 ? 2 : 1), 가 = 빼기(VALUE >= 165 ? 2 : 1);
                    갈까 = VALUE == 159 || VALUE == 165 ? 가 == SECOND_operand : VALUE == 160 || VALUE == 166 ? 가 != SECOND_operand : VALUE == 161 ? 가 < SECOND_operand : VALUE == 162 ? 가 >= SECOND_operand : VALUE == 163 ? 가 > SECOND_operand : 가 <= SECOND_operand;
                } else if (VALUE == 198 || VALUE == 199) { int 수 = 빼기(2); 갈까 = VALUE == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) muta_VALUE_83b651b8(destinație_VALUE); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { restitui_KR(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE >= 178 && VALUE <= 181) { 필드호출(명상수(), VALUE, Pornește); continue; }
            if (VALUE >= 182 && VALUE <= 185) {
                int 부호값 = 명상수();
                if (VALUE == 185) { int total_COUNT = 명바(); if (total_COUNT == 0 || 명바() != 0) { eroare_VALUE("invalid invokeinterface operands"); continue; } }
                Apel_metodă(부호값, VALUE); continue;
            }
            if (VALUE == 187) { 새객체(nume_de_clasă_SMS(명상수()), Pornește); continue; }
            if (VALUE == 188 || VALUE == 189) {
                int zonă_cod = 3, componentă = 0;
                if (VALUE == 188) { int 임시값 = 명바(); zonă_cod = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else componentă = nume_de_clasă_SMS(명상수());
                if (zonă_cod == 0) { eroare_VALUE("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), obiect_referință = aloca_Stocare(zonă_cod, 유효길이); if (!eroare) element_vector[obiect_referință] = componentă; 넣기(obiect_referință, 2); continue;
            }
            if (VALUE == 190) {
                int obiect_referință = 빼기(2);
                if (객체유효(obiect_referință)) { int Comparație_poziție = 힙[obiect_referință]; if (Comparație_poziție != 2 && Comparație_poziție != 3 && (Comparație_poziție < 20 || Comparație_poziție > 23)) eroare_VALUE("not an array"); else 넣기(힙[obiect_referință + 1], 1); }
                continue;
            }
            if (VALUE == 191) {
                int obiect_referință = 빼기(2); if (객체유효(obiect_referință)) { if (힙[obiect_referință] != 9) eroare_VALUE("athrow requires supported Throwable"); else { 던진객체 = obiect_referință; eroare = true; } }
                continue;
            }
            if (VALUE == 192 || VALUE == 193) {
                int nume_constantă = nume_de_clasă_SMS(명상수()), obiect_referință = 빼기(2); boolean MATCH = 맞는객체(obiect_referință, nume_constantă);
                if (VALUE == 193) 넣기(obiect_referință != 0 && MATCH ? 1 : 0, 1);
                else { if (!MATCH && !eroare) eroare_VALUE("ClassCastException"); 넣기(obiect_referință, 2); }
                continue;
            }
            if (VALUE == 170 || VALUE == 171) {
                int 읽는자리 = Pornește + 1, Fișier_INDEX = cadru_metodă[cadru_INDEX], Cheie_referință = 빼기(1);
                while ((읽는자리 - metodă_buta[Fișier_INDEX]) % 4 != 0) 읽는자리++;
                int țintă_adresa = poziție_întreg(읽는자리);
                if (VALUE == 170) { int 낮은값 = poziție_întreg(읽는자리 + 4), 높은값 = poziție_întreg(읽는자리 + 8); if (Cheie_referință >= 낮은값 && Cheie_referință <= 높은값) țintă_adresa = poziție_întreg(읽는자리 + 12 + (Cheie_referință - 낮은값) * 4); }
                else { int total_COUNT = poziție_întreg(읽는자리 + 4); for (int Loop_INDEX = 0; Loop_INDEX < total_COUNT; Loop_INDEX++) if (poziție_întreg(읽는자리 + 8 + Loop_INDEX * 8) == Cheie_referință) țintă_adresa = poziție_întreg(읽는자리 + 12 + Loop_INDEX * 8); }
                muta_VALUE_83b651b8(Pornește + țintă_adresa); continue;
            }
            if (VALUE == 200) { muta_VALUE_83b651b8(Pornește + poziție_întreg(Pornește + 1)); continue; }
            if (VALUE == 194 || VALUE == 195) {
                int obiect_referință = 빼기(2);
                if (VALUE == 195) lansa_blocare(obiect_referință);
                else if (!잠금얻기(obiect_referință) && !eroare) { 넣기(obiect_referință, 2); cadru_poziție[cadru_INDEX] = Pornește; }
                continue;
            }
            if (VALUE == 196) {
                int comandă_cod = 명바(), intrare_poziție = 명짧();
                if (comandă_cod == 21 || comandă_cod == 25) 지역읽기(intrare_poziție, comandă_cod == 21 ? 1 : 2);
                else if (comandă_cod == 54 || comandă_cod == 58) scriere_local(intrare_poziție, comandă_cod == 54 ? 1 : 2);
                else if (comandă_cod == 132) { int DELTA_VALUE = (short)명짧(); 지역읽기(intrare_poziție, 1); 넣기(빼기(1) + DELTA_VALUE, 1); scriere_local(intrare_poziție, 1); }
                else eroare_VALUE("unsupported wide opcode");
                continue;
            }
            eroare_VALUE("unsupported bytecode");
        }
    }
    static int FIND_Clasă_Definiție(int Nume) {
        for (int Loop_INDEX = 0; Loop_INDEX < Clasă_Definiție_COUNT; Loop_INDEX++) if (Clasă_Definiție_nume[Loop_INDEX] != 0 && 같은말(Clasă_Definiție_nume[Loop_INDEX], Nume)) return Loop_INDEX;
        return încărca_Clasă_Definiție(constantă_SMS(Nume));
    }
    static int încărca_Clasă_Definiție(int nume_șir) {
        if (!obiect_VALUE(nume_șir, 1)) return -1;
        int lungime_VALUE = 힙[nume_șir + 1];
        if (lungime_VALUE < 1 || lungime_VALUE > 505 || Clasă_Definiție_COUNT == 16) { eroare_VALUE("class name/count limit"); return -1; }
        for (int Loop_INDEX = 0; Loop_INDEX < lungime_VALUE; Loop_INDEX++) { int cod_caracter = 힙[nume_șir + 2 + Loop_INDEX]; nume_de_fișier_SMS[Loop_INDEX] = cod_caracter == '/' ? '.' : cod_caracter; }
        nume_de_fișier_SMS[lungime_VALUE] = '.'; nume_de_fișier_SMS[lungime_VALUE + 1] = 'c'; nume_de_fișier_SMS[lungime_VALUE + 2] = 'l'; nume_de_fișier_SMS[lungime_VALUE + 3] = 'a'; nume_de_fișier_SMS[lungime_VALUE + 4] = 's'; nume_de_fișier_SMS[lungime_VALUE + 5] = 's'; nume_de_fișier_SMS[lungime_VALUE + 6] = 0;
        int Mărime = utilizator.파일읽기(nume_de_fișier_SMS, fișier_temporar);
        if (Mărime < 0) { eroare_VALUE("ClassNotFoundException"); return -1; }
        int Clasă_Definiție = Clasă_Definiție_COUNT++; Clasă_Definiție_dimensiona[Clasă_Definiție] = Mărime;
        for (int Loop_INDEX = 0; Loop_INDEX < Mărime; Loop_INDEX++) Fișier[Clasă_Definiție * 16384 + Loop_INDEX] = fișier_temporar[Loop_INDEX];
        클래스읽기(Clasă_Definiție); if (eroare) return -1;
        int real_date = constantă_SMS(Clasă_Definiție_nume[Clasă_Definiție]);
        if (!글같음(real_date, nume_șir, true)) { eroare_VALUE("class name does not match file"); return -1; }
        int părinte_VALUE = Clasă_Definiție_părinte[Clasă_Definiție];
        if (părinte_VALUE != 0 && !Word_SMS(părinte_VALUE, "java/lang/Object") && !Word_SMS(părinte_VALUE, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 reîncerca_VALUE 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = FIND_Clasă_Definiție(părinte_VALUE);
            if (eroare || 위 < 0) return -1;
            int 읽는자리 = 위, fază_COUNT = 0;
            while (읽는자리 >= 0 && fază_COUNT++ < 16) {
                if (읽는자리 == Clasă_Definiție) { eroare_VALUE("cyclic inheritance"); return -1; }
                읽는자리 = părinte_Clasă(읽는자리);
            }
            int 시작변위 = 종칸수[위];
            for (int Fișier_INDEX = 0; Fișier_INDEX < 칸수; Fișier_INDEX++) if (칸주인[Fișier_INDEX] == Clasă_Definiție && (칸권한[Fișier_INDEX] & 8) == 0) 칸위치[Fișier_INDEX] += 시작변위;
            종칸수[Clasă_Definiție] += 시작변위;
        }
        return Clasă_Definiție;
    }
    static int părinte_Clasă(int Clasă_Definiție) {
        int Nume = Clasă_Definiție_părinte[Clasă_Definiție];
        for (int Loop_INDEX = 0; Loop_INDEX < Clasă_Definiție_COUNT; Loop_INDEX++) if (Nume != 0 && Clasă_Definiție_nume[Loop_INDEX] != 0 && 같은말(Clasă_Definiție_nume[Loop_INDEX], Nume)) return Loop_INDEX;
        return -1;
    }
    static int FIND_metodă(int Clasă_Definiție, int Nume, int format_VALUE) {
        for (int 깊이 = 0; Clasă_Definiție >= 0 && 깊이 < 16; 깊이++, Clasă_Definiție = părinte_Clasă(Clasă_Definiție)) {
            for (int Loop_INDEX = 0; Loop_INDEX < metodă_COUNT; Loop_INDEX++) if (metodă_proprietar[Loop_INDEX] == Clasă_Definiție && 같은말(metodă_nume_SMS[Loop_INDEX], Nume) && 같은말(metodă_Tip[Loop_INDEX], format_VALUE)) return Loop_INDEX;
        }
        return -1;
    }
    static int nume_metodă(int Clasă_Definiție, String Nume, String format_VALUE) {
        for (int 깊이 = 0; Clasă_Definiție >= 0 && 깊이 < 16; 깊이++, Clasă_Definiție = părinte_Clasă(Clasă_Definiție))
            for (int Loop_INDEX = 0; Loop_INDEX < metodă_COUNT; Loop_INDEX++) if (metodă_proprietar[Loop_INDEX] == Clasă_Definiție && Word_SMS(metodă_nume_SMS[Loop_INDEX], Nume) && Word_SMS(metodă_Tip[Loop_INDEX], format_VALUE)) return Loop_INDEX;
        return -1;
    }
    static int 형종류(int Nume) { return Fișier[상가[Nume]] == 'L' || Fișier[상가[Nume]] == '[' ? 2 : 1; }
    static boolean 초기화(int Clasă_Definiție, int comandă_buta) {
        if (Clasă_Definiție < 0 || eroare) return false;
        if (Clasă_Definiție_Stare[Clasă_Definiție] == 3) { eroare_VALUE("NoClassDefFoundError: initialization failed"); return false; }
        if (Clasă_Definiție_Stare[Clasă_Definiție] == 1 && Clasă_fir[Clasă_Definiție] != curent_fir) { cadru_poziție[cadru_INDEX] = comandă_buta; schimba_cerere = true; return false; }
        if (Clasă_Definiție_Stare[Clasă_Definiție] != 0) return true;
        int 위 = părinte_Clasă(Clasă_Definiție);
        if (위 >= 0 && !초기화(위, comandă_buta)) return false;
        Clasă_Definiție_Stare[Clasă_Definiție] = 1; Clasă_fir[Clasă_Definiție] = curent_fir;
        if (종초기화[Clasă_Definiție] != 0) {
            cadru_poziție[cadru_INDEX] = comandă_buta;
            호출(종초기화[Clasă_Definiție] - 1); if (!eroare) 틀초기화[cadru_INDEX] = Clasă_Definiție + 1;
            return false;
        }
        Clasă_Definiție_Stare[Clasă_Definiție] = 2; return true;
    }
    static void 필드호출(int INDEX, int Comandă, int Pornește) {
        if (!verifica_constantă(INDEX, 9)) return;
        int proprietar_VALUE = nume_de_clasă_SMS(상가[INDEX]), Nume = referință_nume(constantă_SECOND_VALUE[INDEX]), format_VALUE = referință_Tip(constantă_SECOND_VALUE[INDEX]);
        if (Word_SMS(proprietar_VALUE, "java/lang/System") && (Word_SMS(Nume, "out") || Word_SMS(Nume, "err")) && Word_SMS(format_VALUE, "Ljava/io/PrintStream;") && Comandă == 178) { 넣기(-1, 2); return; }
        int Clasă_Definiție = FIND_Clasă_Definiție(proprietar_VALUE); if (Clasă_Definiție < 0 || eroare) return;
        int 찾음 = -1;
        for (int 읽는자리 = Clasă_Definiție, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = părinte_Clasă(읽는자리))
            for (int Fișier_INDEX = 0; Fișier_INDEX < 칸수; Fișier_INDEX++) if (칸주인[Fișier_INDEX] == 읽는자리 && 같은말(칸이름[Fișier_INDEX], Nume) && 같은말(칸형[Fișier_INDEX], format_VALUE)) 찾음 = Fișier_INDEX;
        if (찾음 < 0) { eroare_VALUE("NoSuchFieldError"); return; }
        boolean 정적 = Comandă == 178 || Comandă == 179;
        if (정적 != ((칸권한[찾음] & 8) != 0)) { eroare_VALUE("field static/instance mismatch"); return; }
        if (정적 && !초기화(칸주인[찾음], Pornește)) return;
        int Tip_VALUE = 형종류(format_VALUE), VALUE = 0;
        if (Comandă == 179 || Comandă == 181) VALUE = 빼기(Tip_VALUE);
        if (정적) { if (Comandă == 178) 넣기(칸값[찾음], Tip_VALUE); else if (!eroare) 칸값[찾음] = VALUE; return; }
        int obiect_referință = 빼기(2);
        if (!객체유효(obiect_referință)) return;
        if (힙[obiect_referință] < 32 || !종포함(힙[obiect_referință] - 32, proprietar_VALUE)) { eroare_VALUE("field receiver type mismatch"); return; }
        int 보관칸 = obiect_referință + 2 + 칸위치[찾음];
        if (Comandă == 180) 넣기(힙[보관칸], Tip_VALUE);
        else if (!eroare) { 힙[보관칸] = VALUE; 힙참조[보관칸] = Tip_VALUE == 2 ? 1 : 0; }
    }
    static boolean 종포함(int Clasă_Definiție, int Nume) {
        for (int 중첩깊이 = 0; Clasă_Definiție >= 0 && 중첩깊이 < 16; 중첩깊이++, Clasă_Definiție = părinte_Clasă(Clasă_Definiție)) {
            if (같은말(Clasă_Definiție_nume[Clasă_Definiție], Nume) || (Clasă_Definiție_părinte[Clasă_Definiție] != 0 && 같은말(Clasă_Definiție_părinte[Clasă_Definiție], Nume))) return true;
            for (int internă_poziție = 0; internă_poziție < Clasă_interfață_COUNT[Clasă_Definiție]; internă_poziție++) if (같은말(Clasă_interfață[Clasă_Definiție * 16 + internă_poziție], Nume)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int byte_date, boolean Cale) {
        if (첫값 == byte_date) return true;
        if (첫값 <= 0 || byte_date <= 0 || 힙[첫값] != 1 || 힙[byte_date] != 1 || 힙[첫값 + 1] != 힙[byte_date + 1]) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) {
            int coordonata_X = 힙[첫값 + 2 + Loop_INDEX], 세로좌표 = 힙[byte_date + 2 + Loop_INDEX];
            if (Cale) { if (coordonata_X == '.') coordonata_X = '/'; if (세로좌표 == '.') 세로좌표 = '/'; }
            if (coordonata_X != 세로좌표) return false;
        }
        return true;
    }
    static boolean 객체유효(int obiect_referință) {
        if (obiect_referință == 0) { eroare_VALUE("NullPointerException"); return false; }
        if (obiect_referință < 1 || obiect_referință >= 힙끝 || 힙폭[obiect_referință] < 2 || 힙[obiect_referință] == 0) { eroare_VALUE("invalid object reference"); return false; }
        return true;
    }
    static void proteja_VALUE(int obiect_referință) {
        if (obiect_referință > 0 && obiect_referință < 힙끝 && 힙폭[obiect_referință] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = obiect_referință;
    }
    static void afișa_VALUE(int obiect_referință) {
        if (obiect_referință > 0 && obiect_referință < 힙끝 && 힙폭[obiect_referință] >= 2 && 힙[obiect_referință] != 0 && 힙표시[obiect_referință] == 0) {
            힙표시[obiect_referință] = 1; 표시대기[afișa_COUNT++] = obiect_referință;
        }
    }
    static void 수거() {
        afișa_COUNT = 0; Colecție_COUNT++;
        for (int verifica_poziție_9b8e3629 = 1; verifica_poziție_9b8e3629 < 힙끝; verifica_poziție_9b8e3629 += 힙폭[verifica_poziție_9b8e3629]) 힙표시[verifica_poziție_9b8e3629] = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < șir_referință.length; Loop_INDEX++) afișa_VALUE(șir_referință[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 칸수; Loop_INDEX++) if ((칸권한[Loop_INDEX] & 8) != 0 && 형종류(칸형[Loop_INDEX]) == 2) afișa_VALUE(칸값[Loop_INDEX]);
        for (int 임시값 = 0; 임시값 < fir_COUNT; 임시값++) {
            afișa_VALUE(fir_obiect[임시값]); afișa_VALUE(fir_țintă[임시값]);
            int 꼭대기자리 = 임시값 == curent_fir ? cadru_INDEX : fir_cadru[임시값];
            for (int Fișier_INDEX = 임시값 * 32; Fișier_INDEX <= 꼭대기자리; Fișier_INDEX++) {
                for (int internă_poziție = 0; internă_poziție < 함수지역[cadru_metodă[Fișier_INDEX]]; internă_poziție++) if (local_Tip[Fișier_INDEX * 128 + internă_poziție] == 2) afișa_VALUE(local_VALUE[Fișier_INDEX * 128 + internă_poziție]);
                for (int internă_poziție = 0; internă_poziție < cadru_Teanc[Fișier_INDEX]; internă_poziție++) if (operand_Teanc_Tip[Fișier_INDEX * 128 + internă_poziție] == 2) afișa_VALUE(operand_Teanc_VALUE[Fișier_INDEX * 128 + internă_poziție]);
            }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 화면참조.length; Loop_INDEX++) afișa_VALUE(화면참조[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 나중수; Loop_INDEX++) afișa_VALUE(나중실행[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Store_întreg.length; Loop_INDEX++) afișa_VALUE(Store_întreg[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Clasă_Definiție_COUNT; Loop_INDEX++) afișa_VALUE(Clasă_blocare[Loop_INDEX]);
        for (int verifica_poziție_9b8e3629 = 1; verifica_poziție_9b8e3629 < 힙끝; verifica_poziție_9b8e3629 += 힙폭[verifica_poziție_9b8e3629]) if (잠금깊이[verifica_poziție_9b8e3629] > 0) afișa_VALUE(verifica_poziție_9b8e3629);
        afișa_VALUE(던진객체);
        for (int Loop_INDEX = 0; Loop_INDEX < 잠시수; Loop_INDEX++) afișa_VALUE(잠시참조[Loop_INDEX]);
        while (afișa_COUNT > 0) {
            int obiect_referință = 표시대기[--afișa_COUNT], zonă_cod = 힙[obiect_referință];
            for (int Loop_INDEX = obiect_referință + 2; Loop_INDEX < obiect_referință + 힙폭[obiect_referință]; Loop_INDEX++) if (zonă_cod == 3 || zonă_cod == 4 || 힙참조[Loop_INDEX] != 0) afișa_VALUE(힙[Loop_INDEX]);
        }
        for (int verifica_poziție_9b8e3629 = 1; verifica_poziție_9b8e3629 < 힙끝; verifica_poziție_9b8e3629 += 힙폭[verifica_poziție_9b8e3629]) if (힙표시[verifica_poziție_9b8e3629] == 0) 힙[verifica_poziție_9b8e3629] = 0;
        for (int verifica_poziție_9b8e3629 = 1; verifica_poziție_9b8e3629 < 힙끝; verifica_poziție_9b8e3629 += 힙폭[verifica_poziție_9b8e3629]) if (힙[verifica_poziție_9b8e3629] == 0) {
            while (verifica_poziție_9b8e3629 + 힙폭[verifica_poziție_9b8e3629] < 힙끝 && 힙[verifica_poziție_9b8e3629 + 힙폭[verifica_poziție_9b8e3629]] == 0) { int Următorul_poziție = verifica_poziție_9b8e3629 + 힙폭[verifica_poziție_9b8e3629]; 힙폭[verifica_poziție_9b8e3629] += 힙폭[Următorul_poziție]; 힙폭[Următorul_poziție] = 0; }
            if (verifica_poziție_9b8e3629 + 힙폭[verifica_poziție_9b8e3629] == 힙끝) { 힙끝 = verifica_poziție_9b8e3629; break; }
        }
    }
    static int 새기억(int 종류, int lungime_VALUE) {
        if (lungime_VALUE < 0) { eroare_VALUE("NegativeArraySizeException"); return 0; }
        if (lungime_VALUE > 힙.length - 3) { eroare_VALUE("object heap exhausted"); return 0; }
        int 필요수 = lungime_VALUE + 2, obiect_referință = 0;
        if (필요수 <= 힙.length - 힙끝) { obiect_referință = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { obiect_referință = 읽는자리; break; }
            if (obiect_referință != 0) {
                int 남은길이 = 힙폭[obiect_referință] - 필요수;
                if (남은길이 >= 2) { 힙폭[obiect_referință + 필요수] = 남은길이; 힙[obiect_referință + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { obiect_referință = 힙끝; 힙끝 += 필요수; }
        }
        if (obiect_referință == 0) { eroare_VALUE("object heap exhausted"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < 필요수; Loop_INDEX++) { 힙[obiect_referință + Loop_INDEX] = 0; 힙참조[obiect_referință + Loop_INDEX] = 0; 힙폭[obiect_referință + Loop_INDEX] = 0; }
        element_vector[obiect_referință] = 0;
        힙폭[obiect_referință] = 필요수; 힙[obiect_referință] = 종류; 힙[obiect_referință + 1] = lungime_VALUE; proteja_VALUE(obiect_referință); return obiect_referință;
    }
    static int excepție_Clasă(String nume_constantă) {
        if (자바도구.같음(nume_constantă, "java/lang/Throwable")) return 1;
        if (자바도구.같음(nume_constantă, "java/lang/Exception")) return 2;
        if (자바도구.같음(nume_constantă, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(nume_constantă, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(nume_constantă, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(nume_constantă, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(nume_constantă, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(nume_constantă, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(nume_constantă, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(nume_constantă, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(nume_constantă, "java/io/IOException")) return 11;
        if (자바도구.같음(nume_constantă, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(nume_constantă, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(nume_constantă, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(nume_constantă, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int excepție_constantă(int Nume) {
        for (int Loop_INDEX = 1; Loop_INDEX <= 41; Loop_INDEX++) if (Word_SMS(Nume, excepție_nume(Loop_INDEX))) return Loop_INDEX;
        return 0;
    }
    static String excepție_nume(int cont_VALUE) {
        if (cont_VALUE == 40) return "java/lang/InterruptedException";
        if (cont_VALUE == 41) return "Română/propriu/대기중단예외";
        if (cont_VALUE == 39) return "java/net/SocketException";
        if (cont_VALUE == 20) return "Română/propriu/excepție";
        if (cont_VALUE == 21) return "Română/propriu/executare_excepție";
        if (cont_VALUE == 22) return "Română/propriu/I_O_excepție";
        if (cont_VALUE == 23) return "Română/propriu/대기시간초과예외";
        if (cont_VALUE == 24) return "Română/propriu/adresa_LOOKUP_excepție";
        if (cont_VALUE == 25) return "Română/propriu/파일없음예외";
        if (cont_VALUE == 26) return "Română/propriu/통신예외";
        if (cont_VALUE == 27) return "Română/propriu/nul_argument_excepție";
        if (cont_VALUE == 28) return "Română/propriu/숫자형식예외";
        if (cont_VALUE == 29) return "Română/propriu/범위예외";
        if (cont_VALUE == 30) return "Română/propriu/배열범위예외";
        if (cont_VALUE == 31) return "Română/propriu/문자열범위예외";
        if (cont_VALUE == 32) return "Română/propriu/NUL_referință_excepție";
        if (cont_VALUE == 33) return "Română/propriu/산술예외";
        if (cont_VALUE == 34) return "Română/propriu/Stare_excepție";
        if (cont_VALUE == 35) return "Română/propriu/Tip_cast_excepție";
        if (cont_VALUE == 36) return "Română/propriu/음수배열크기예외";
        if (cont_VALUE == 37) return "Română/propriu/ARRAY_Store_eroare";
        if (cont_VALUE == 38) return "Română/propriu/fir_Stare_excepție";
        if (cont_VALUE == 1) return "java/lang/Throwable"; if (cont_VALUE == 2) return "java/lang/Exception";
        if (cont_VALUE == 3) return "java/lang/RuntimeException"; if (cont_VALUE == 4) return "java/lang/ArithmeticException";
        if (cont_VALUE == 5) return "java/lang/NullPointerException"; if (cont_VALUE == 6) return "java/lang/IndexOutOfBoundsException";
        if (cont_VALUE == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (cont_VALUE == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (cont_VALUE == 9) return "java/lang/IllegalArgumentException"; if (cont_VALUE == 10) return "java/lang/NumberFormatException";
        if (cont_VALUE == 11) return "java/io/IOException"; if (cont_VALUE == 12) return "java/io/FileNotFoundException";
        if (cont_VALUE == 17) return "java/lang/ArrayStoreException";
        if (cont_VALUE == 18) return "java/net/UnknownHostException";
        if (cont_VALUE == 19) return "java/net/SocketTimeoutException";
        if (cont_VALUE == 16) return "java/lang/IllegalThreadStateException";
        if (cont_VALUE == 13) return "java/lang/IllegalStateException"; if (cont_VALUE == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int excepție_părinte(int cont_VALUE) {
        if (cont_VALUE == 40) return 2;
        if (cont_VALUE == 41) return 40;
        if (cont_VALUE == 39) return 11;
        if (cont_VALUE == 1) return 0;
        if (cont_VALUE == 2) return 1;
        if (cont_VALUE == 3) return 2;
        if (cont_VALUE == 4) return 3;
        if (cont_VALUE == 5) return 3;
        if (cont_VALUE == 6) return 3;
        if (cont_VALUE == 7) return 6;
        if (cont_VALUE == 8) return 6;
        if (cont_VALUE == 9) return 3;
        if (cont_VALUE == 10) return 9;
        if (cont_VALUE == 11) return 2;
        if (cont_VALUE == 12) return 11;
        if (cont_VALUE == 13) return 3;
        if (cont_VALUE == 14) return 3;
        if (cont_VALUE == 15) return 3;
        if (cont_VALUE == 16) return 9;
        if (cont_VALUE == 17) return 3;
        if (cont_VALUE == 18) return 11;
        if (cont_VALUE == 19) return 11;
        if (cont_VALUE == 20) return 2;
        if (cont_VALUE == 21) return 3;
        if (cont_VALUE == 22) return 11;
        if (cont_VALUE == 23) return 22;
        if (cont_VALUE == 24) return 22;
        if (cont_VALUE == 25) return 22;
        if (cont_VALUE == 26) return 22;
        if (cont_VALUE == 27) return 9;
        if (cont_VALUE == 28) return 27;
        if (cont_VALUE == 29) return 6;
        if (cont_VALUE == 30) return 29;
        if (cont_VALUE == 31) return 29;
        if (cont_VALUE == 32) return 5;
        if (cont_VALUE == 33) return 4;
        if (cont_VALUE == 34) return 13;
        if (cont_VALUE == 35) return 14;
        if (cont_VALUE == 36) return 15;
        if (cont_VALUE == 37) return 17;
        if (cont_VALUE == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int valoare_reală, int 요구값) {
        for (int 깊이 = 0; valoare_reală != 0 && 깊이 < 16; 깊이++, valoare_reală = excepție_părinte(valoare_reală))
            if (valoare_reală == 요구값) return true;
        return false;
    }
    static void 예외던짐(int cont_VALUE, String 안내참조) {
        int obiect_referință = 새기억(9, 2); if (eroare) return;
        힙[obiect_referință + 2] = cont_VALUE; 힙[obiect_referință + 3] = gazdă_caracter(안내참조); 힙참조[obiect_referință + 3] = 1;
        던진객체 = obiect_referință; eroare = true;
    }
    static boolean 맞는객체(int obiect_referință, int Nume) {
        if (obiect_referință == 0) return true;
        if (!객체유효(obiect_referință)) return false;
        int zonă_cod = 힙[obiect_referință];
        if (Word_SMS(Nume, "java/lang/Object")) return true;
        if (zonă_cod >= 32) return 종포함(zonă_cod - 32, Nume);
        if (zonă_cod == 9) { int țintă_adresa = excepție_constantă(Nume); return țintă_adresa != 0 && 예외포함(힙[obiect_referință + 2], țintă_adresa); }
        if (zonă_cod == 1) return Word_SMS(Nume, "java/lang/String") || Word_SMS(Nume, "java/lang/CharSequence");
        if (zonă_cod == 4) return Word_SMS(Nume, "java/lang/StringBuilder") || Word_SMS(Nume, "java/lang/CharSequence");
        if (zonă_cod == 10) return Word_SMS(Nume, "java/util/ArrayList") || Word_SMS(Nume, "java/util/List");
        if (zonă_cod == 11) return Word_SMS(Nume, "java/util/HashMap") || Word_SMS(Nume, "java/util/Map");
        if (zonă_cod == 12) return Word_SMS(Nume, "java/lang/Integer") || Word_SMS(Nume, "java/lang/Number");
        if (zonă_cod >= 24 && zonă_cod <= 28 && 힙[obiect_referință + 13] != 0) return 한국어화면종(Nume) == zonă_cod || Word_SMS(Nume, "Română/propriu/화면구성요소");
        if (zonă_cod >= 24 && zonă_cod <= 28) return (한국어화면종(Nume) == 0 && 화면종(Nume) == zonă_cod) || Word_SMS(Nume, "java/awt/Component") || Word_SMS(Nume, "java/awt/Container") || Word_SMS(Nume, "javax/swing/JComponent");
        if (zonă_cod == 29) return Word_SMS(Nume, 힙[obiect_referință + 3] != 0 ? "Română/propriu/Acțiune_înștiințare" : "java/awt/event/ActionEvent");
        if (zonă_cod == 30) return Word_SMS(Nume, "java/awt/FlowLayout") || Word_SMS(Nume, "java/awt/LayoutManager");
        if (zonă_cod == 17) return Word_SMS(Nume, "java/net/Socket");
        if (zonă_cod == 18) return Word_SMS(Nume, "java/net/ServerSocket");
        if (zonă_cod == 19) return Word_SMS(Nume, 힙[obiect_referință + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (zonă_cod == 14) return Word_SMS(Nume, "java/net/InetAddress");
        if (zonă_cod == 15) return Word_SMS(Nume, "java/net/DatagramSocket");
        if (zonă_cod == 16) return Word_SMS(Nume, "java/net/DatagramPacket");
        if (zonă_cod == 13) return Word_SMS(Nume, 힙[obiect_referință + 3] != 0 ? "Română/propriu/작업가닥" : "java/lang/Thread");
        if (zonă_cod == 2) return Word_SMS(Nume, "[I"); if (zonă_cod == 20) return Word_SMS(Nume, "[B"); if (zonă_cod == 21) return Word_SMS(Nume, "[Z");
        if (zonă_cod == 22) return Word_SMS(Nume, "[C"); if (zonă_cod == 23) return Word_SMS(Nume, "[S");
        if (zonă_cod != 3) return false;
        if (Word_SMS(Nume, "[Ljava/lang/Object;")) return true;
        int componentă = element_vector[obiect_referință];
        if (componentă == -1) return Word_SMS(Nume, "[Ljava/lang/String;") || Word_SMS(Nume, "[Ljava/lang/CharSequence;");
        if (componentă == 0) return false;
        if (배열종비교(componentă, Nume)) return true;
        if ((Word_SMS(componentă, "java/lang/String") || Word_SMS(componentă, "java/lang/StringBuilder")) && Word_SMS(Nume, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDEX = 0; Loop_INDEX < Clasă_Definiție_COUNT; Loop_INDEX++) if (같은말(Clasă_Definiție_nume[Loop_INDEX], componentă)) {
            for (int cod_caracter = Loop_INDEX, 중첩깊이 = 0; cod_caracter >= 0 && 중첩깊이 < 16; 중첩깊이++, cod_caracter = părinte_Clasă(cod_caracter)) {
                if (배열종비교(Clasă_Definiție_părinte[cod_caracter], Nume)) return true;
                for (int internă_poziție = 0; internă_poziție < Clasă_interfață_COUNT[cod_caracter]; internă_poziție++) if (배열종비교(Clasă_interfață[cod_caracter * 16 + internă_poziție], Nume)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int nume_constantă, int 형식참조) {
        int verifica_poziție_9b8e3629 = 상가[형식참조], intrare_COUNT = constantă_SECOND_VALUE[형식참조];
        if (nume_constantă == 0 || intrare_COUNT < 4 || Fișier[verifica_poziție_9b8e3629] != '[' || Fișier[verifica_poziție_9b8e3629 + 1] != 'L' || Fișier[verifica_poziție_9b8e3629 + intrare_COUNT - 1] != ';' || constantă_SECOND_VALUE[nume_constantă] != intrare_COUNT - 3) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < intrare_COUNT - 3; Loop_INDEX++) if (Fișier[상가[nume_constantă] + Loop_INDEX] != Fișier[verifica_poziție_9b8e3629 + 2 + Loop_INDEX]) return false;
        return true;
    }
    static void handle_excepție() {
        if (던진객체 == 0) return;
        eroare = false;
        while (cadru_INDEX >= curent_fir * 32) {
            int Fișier_INDEX = cadru_metodă[cadru_INDEX], 읽는자리 = 틀명령[cadru_INDEX];
            for (int Loop_INDEX = 0; Loop_INDEX < 잡기수; Loop_INDEX++) if (잡기함수[Loop_INDEX] == Fișier_INDEX && 읽는자리 >= 잡기시작[Loop_INDEX] && 읽는자리 < 잡기끝[Loop_INDEX]
                && (잡기종[Loop_INDEX] == 0 || 맞는객체(던진객체, 잡기종[Loop_INDEX]))) {
                cadru_poziție[cadru_INDEX] = 잡기위치[Loop_INDEX]; cadru_Teanc[cadru_INDEX] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (틀초기화[cadru_INDEX] != 0) Clasă_Definiție_Stare[틀초기화[cadru_INDEX] - 1] = 3;
            if (cadru_blocare[cadru_INDEX] != 0) { lansa_blocare(cadru_blocare[cadru_INDEX]); cadru_blocare[cadru_INDEX] = 0; }
            cadru_INDEX--;
        }
        utilizator.Scriere("Uncaught ");
        if (힙[던진객체] == 9) { utilizator.Scriere(excepție_nume(힙[던진객체 + 2])); utilizator.Scriere(": "); scriere_SMS(힙[던진객체 + 3]); }
        else utilizator.Scriere("user exception");
        utilizator.scriere_caracter_VALUE(10); 던진객체 = 0; eroare = true;
    }
    // 이 JVM의 operand_Teanc 항목은 curent_element category-1(int/reference)만 허용한다.
    static void 스택명령(int comandă_cod) {
        int 첫값 = 빼기(0), 첫형식 = restitui_Tip;
        if (comandă_cod == 87) return;
        if (comandă_cod == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int byte_date = 빼기(0), SECOND_format = restitui_Tip;
        if (comandă_cod == 88) return;
        if (comandă_cod == 90) { 넣기(첫값, 첫형식); 넣기(byte_date, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (comandă_cod == 92) { 넣기(byte_date, SECOND_format); 넣기(첫값, 첫형식); 넣기(byte_date, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (comandă_cod == 95) { 넣기(첫값, 첫형식); 넣기(byte_date, SECOND_format); return; }
        int cod_caracter = 빼기(0), 셋째형식 = restitui_Tip;
        if (comandă_cod == 91) { 넣기(첫값, 첫형식); 넣기(cod_caracter, 셋째형식); 넣기(byte_date, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (comandă_cod == 93) { 넣기(byte_date, SECOND_format); 넣기(첫값, 첫형식); 넣기(cod_caracter, 셋째형식); 넣기(byte_date, SECOND_format); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = restitui_Tip;
        넣기(byte_date, SECOND_format); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(cod_caracter, 셋째형식); 넣기(byte_date, SECOND_format); 넣기(첫값, 첫형식);
    }
    static void 새객체(int nume_constantă, int 시작점) {
        int zonă_cod = 0, 유효길이 = 0, excepție_referință = excepție_constantă(nume_constantă);
        if (Word_SMS(nume_constantă, "java/lang/StringBuilder")) { zonă_cod = 4; 유효길이 = 1; }
        if (Word_SMS(nume_constantă, "java/io/FileInputStream")) { zonă_cod = 5; 유효길이 = 2; }
        if (Word_SMS(nume_constantă, "java/io/FileOutputStream")) { zonă_cod = 6; 유효길이 = 2; }
        if (excepție_referință != 0) { zonă_cod = 9; 유효길이 = 2; }
        if (Word_SMS(nume_constantă, "java/util/ArrayList")) { zonă_cod = 10; 유효길이 = 2; }
        if (Word_SMS(nume_constantă, "java/util/HashMap")) { zonă_cod = 11; 유효길이 = 2; }
        if (Word_SMS(nume_constantă, "java/lang/Integer")) { zonă_cod = 12; 유효길이 = 1; }
        if (Word_SMS(nume_constantă, "java/net/Socket")) { zonă_cod = 17; 유효길이 = 5; }
        if (Word_SMS(nume_constantă, "java/net/ServerSocket")) { zonă_cod = 18; 유효길이 = 5; }
        if (Word_SMS(nume_constantă, "java/net/DatagramSocket")) { zonă_cod = 15; 유효길이 = 3; }
        if (Word_SMS(nume_constantă, "java/net/DatagramPacket")) { zonă_cod = 16; 유효길이 = 4; }
        if (Word_SMS(nume_constantă, "java/lang/Thread") || Word_SMS(nume_constantă, "Română/propriu/작업가닥")) { zonă_cod = 13; 유효길이 = 2; }
        if (Word_SMS(nume_constantă, "java/lang/Object")) { zonă_cod = 8; }
        if (zonă_cod == 0 && 화면종(nume_constantă) != 0) { zonă_cod = 화면종(nume_constantă); 유효길이 = 12; }
        if (zonă_cod == 0) {
            int cod_caracter = FIND_Clasă_Definiție(nume_constantă); if (cod_caracter < 0 || eroare || !초기화(cod_caracter, 시작점)) return;
            zonă_cod = 32 + cod_caracter; 유효길이 = 종칸수[cod_caracter];
        }
        int obiect_referință = aloca_Stocare(zonă_cod, 유효길이); if (eroare) return;
        if (zonă_cod == 13 && Word_SMS(nume_constantă, "Română/propriu/작업가닥")) 힙[obiect_referință + 3] = 1;
        if (zonă_cod >= 24 && zonă_cod <= 28 && 한국어화면종(nume_constantă) != 0) 힙[obiect_referință + 13] = 1;
        if (zonă_cod == 5 || zonă_cod == 6 || zonă_cod == 15 || zonă_cod == 17 || zonă_cod == 18) 힙[obiect_referință + 2] = -1;
        if (zonă_cod == 9) 힙[obiect_referință + 2] = excepție_referință;
        넣기(obiect_referință, 2);
    }
    static boolean 값같음(int 첫값, int byte_date) {
        if (첫값 == byte_date) return true;
        if (첫값 == 0 || byte_date == 0 || 첫값 < 0 || byte_date < 0 || 첫값 >= 힙끝 || byte_date >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[byte_date] == 1) return 글같음(첫값, byte_date, false);
        return 힙[첫값] == 12 && 힙[byte_date] == 12 && 힙[첫값 + 2] == 힙[byte_date + 2];
    }
    static int 글조각(int obiect_referință, int buta_poziție, int termina_un_apel_poziție) {
        if (!obiect_VALUE(obiect_referință, 1)) return 0;
        if (buta_poziție < 0 || termina_un_apel_poziție < buta_poziție || termina_un_apel_poziție > 힙[obiect_referință + 1]) { eroare_VALUE("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = aloca_Stocare(1, termina_un_apel_poziție - buta_poziție); if (eroare) return 0;
        for (int Loop_INDEX = buta_poziție; Loop_INDEX < termina_un_apel_poziție; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX - buta_poziție] = 힙[obiect_referință + 2 + Loop_INDEX];
        return 반환값;
    }
    static int asocia_SMS(int 첫값, int byte_date) {
        if (!obiect_VALUE(첫값, 1) || !obiect_VALUE(byte_date, 1)) return 0;
        int intrare_COUNT = 힙[첫값 + 1], metodă_INDEX = 힙[byte_date + 1], 반환값 = aloca_Stocare(1, intrare_COUNT + metodă_INDEX); if (eroare) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < intrare_COUNT; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 힙[첫값 + 2 + Loop_INDEX];
        for (int Loop_INDEX = 0; Loop_INDEX < metodă_INDEX; Loop_INDEX++) 힙[반환값 + 2 + intrare_COUNT + Loop_INDEX] = 힙[byte_date + 2 + Loop_INDEX];
        return 반환값;
    }
    static boolean 기본호출(int proprietar, int nume_constantă, int 서술상수, int comandă_cod) {
        if (Word_SMS(proprietar, "Română/propriu/실행인수") && comandă_cod == 184) {
            if (Word_SMS(nume_constantă, "element_COUNT") && Word_SMS(서술상수, "()I")) { 넣기(utilizator.인수개수() - 1, 1); return true; }
            if (Word_SMS(nume_constantă, "SMS") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= utilizator.인수개수() - 1) 예외던짐(29, "executa_comandă Argumente 범위를 벗어났습니다");
                else 넣기(gazdă_caracter(utilizator.Argumente(순번 + 1)), 2);
                return true;
            }
            eroare_VALUE("지원하지 않는 Română executa_comandă Argumente 호출"); return true;
        }
        if (Word_SMS(proprietar, "Română/propriu/작업가닥")) { Proces_fir(nume_constantă, 서술상수, comandă_cod, true); return true; }
        if (한국어화면소유(proprietar)) { 한국어화면호출(proprietar, nume_constantă, 서술상수, comandă_cod); return true; }
        if (화면소유(proprietar)) { 화면호출(proprietar, nume_constantă, 서술상수, comandă_cod); return true; }
        if (Word_SMS(proprietar, "java/net/Socket") || Word_SMS(proprietar, "java/net/ServerSocket") || Word_SMS(proprietar, "java/io/InputStream") || Word_SMS(proprietar, "java/io/OutputStream")) { 흐름호출(proprietar, nume_constantă, 서술상수, comandă_cod); return true; }
        if (Word_SMS(proprietar, "Română/propriu/nucleu_VALUE") && comandă_cod == 184) {
            if (Word_SMS(nume_constantă, "화면너비") && Word_SMS(서술상수, "()I")) { 넣기(utilizator.화면너비(), 1); return true; }
            if (Word_SMS(nume_constantă, "화면높이") && Word_SMS(서술상수, "()I")) { 넣기(utilizator.화면높이(), 1); return true; }
            if (Word_SMS(nume_constantă, "밀리초") && Word_SMS(서술상수, "()I")) { 넣기(utilizator.밀리초(), 1); return true; }
            if (Word_SMS(nume_constantă, "그림대기") && Word_SMS(서술상수, "()I")) { 넣기(utilizator.그림대기(), 1); return true; }
            if (Word_SMS(nume_constantă, "dreptunghi") && Word_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), coordonata_X = 빼기(1); 넣기(utilizator.dreptunghi(coordonata_X, 세로좌표, 너비, 높이, 색상), 1); return true; }
        }
        if (Word_SMS(proprietar, "java/net/InetAddress") || Word_SMS(proprietar, "java/net/DatagramPacket") || Word_SMS(proprietar, "java/net/DatagramSocket")) { 통신호출(proprietar, nume_constantă, 서술상수, comandă_cod); return true; }
        if (Word_SMS(proprietar, "java/lang/Thread")) { 가닥호출(nume_constantă, 서술상수, comandă_cod); return true; }
        if (Word_SMS(proprietar, "java/lang/Object")) {
            if (Word_SMS(nume_constantă, "<init>") && Word_SMS(서술상수, "()V") && comandă_cod == 183) { 객체유효(빼기(2)); return true; }
            if (Word_SMS(nume_constantă, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int byte_date = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == byte_date ? 1 : 0, 1); return true; }
        }
        if (excepție_constantă(proprietar) != 0) {
            if (Word_SMS(nume_constantă, "<init>") && comandă_cod == 183 && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int solicita = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), obiect_referință = 빼기(2);
                if (obiect_VALUE(obiect_referință, 9)) { 힙[obiect_referință + 3] = solicita; 힙참조[obiect_referință + 3] = 1; } return true;
            }
            if ((Word_SMS(nume_constantă, "getMessage") || Word_SMS(nume_constantă, "설명")) && Word_SMS(서술상수, "()Ljava/lang/String;")) { int obiect_referință = 빼기(2); if (obiect_VALUE(obiect_referință, 9)) 넣기(힙[obiect_referință + 3], 2); return true; }
        }
        if (Word_SMS(proprietar, "java/lang/String")) {
            if (comandă_cod == 182 && Word_SMS(nume_constantă, "getBytes") && (Word_SMS(서술상수, "()[B") || Word_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int codificare_nume = Word_SMS(서술상수, "()[B") ? 0 : 빼기(2), obiect_referință = 빼기(2);
                if (!obiect_VALUE(obiect_referință, 1)) return true;
                if (codificare_nume != 0 && !글같음(codificare_nume, gazdă_caracter("UTF-8"), false) && !글같음(codificare_nume, gazdă_caracter("UTF8"), false) && !글같음(codificare_nume, gazdă_caracter("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int intrare_COUNT = 힙[obiect_referință + 1], 반환값 = aloca_Stocare(20, intrare_COUNT * 3), 사용수 = 0; if (eroare) return true;
                for (int internă_poziție = 0; internă_poziție < intrare_COUNT; internă_poziție++) {
                    int cod_caracter = 힙[obiect_referință + 2 + internă_poziție];
                    if (cod_caracter >= 0xd800 && cod_caracter <= 0xdbff && internă_poziție + 1 < intrare_COUNT && 힙[obiect_referință + 3 + internă_poziție] >= 0xdc00 && 힙[obiect_referință + 3 + internă_poziție] <= 0xdfff) cod_caracter = 0x10000 + ((cod_caracter - 0xd800) << 10) + 힙[obiect_referință + 2 + ++internă_poziție] - 0xdc00;
                    else if (cod_caracter >= 0xd800 && cod_caracter <= 0xdfff) cod_caracter = '?';
                    if (cod_caracter < 128) 힙[반환값 + 2 + 사용수++] = cod_caracter;
                    else { int byte_COUNT = cod_caracter < 2048 ? 2 : cod_caracter < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((byte_COUNT == 2 ? 192 : byte_COUNT == 3 ? 224 : 240) | cod_caracter >> (6 * (byte_COUNT - 1))); for (int Comparație_poziție = byte_COUNT - 1; Comparație_poziție > 0; Comparație_poziție--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | cod_caracter >> (6 * (Comparație_poziție - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (comandă_cod == 184 && Word_SMS(nume_constantă, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(cifră_caracter(빼기(1)), 2); return true; }
            if (comandă_cod != 182) return false;
            if (Word_SMS(nume_constantă, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int byte_date = 빼기(2), 첫값 = 빼기(2); if (obiect_VALUE(첫값, 1)) 넣기(글같음(첫값, byte_date, false) ? 1 : 0, 1); return true; }
            if (Word_SMS(nume_constantă, "isEmpty") && Word_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (obiect_VALUE(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_SMS(nume_constantă, "substring") && (Word_SMS(서술상수, "(I)Ljava/lang/String;") || Word_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SECOND_VALUE = Word_SMS(서술상수, "(II)Ljava/lang/String;"); int termina_un_apel_poziție = SECOND_VALUE ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (obiect_VALUE(첫값, 1)) 넣기(글조각(첫값, 시작점, SECOND_VALUE ? termina_un_apel_poziție : 힙[첫값 + 1]), 2); return true;
            }
            if (Word_SMS(nume_constantă, "concat") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int byte_date = 빼기(2), 첫값 = 빼기(2); 넣기(asocia_SMS(첫값, byte_date), 2); return true; }
            if (Word_SMS(nume_constantă, "hashCode") && Word_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), cod_hash_VALUE = 0; if (obiect_VALUE(첫값, 1)) { for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) cod_hash_VALUE = cod_hash_VALUE * 31 + 힙[첫값 + 2 + Loop_INDEX]; 넣기(cod_hash_VALUE, 1); } return true; }
            if (Word_SMS(nume_constantă, "toString") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (obiect_VALUE(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_SMS(proprietar, "java/lang/Integer")) {
            if (comandă_cod == 184 && Word_SMS(nume_constantă, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int date_VALUE = 빼기(1), obiect_referință = date_VALUE >= -128 && date_VALUE <= 127 ? Store_întreg[date_VALUE + 128] : 0; if (obiect_referință == 0) { obiect_referință = aloca_Stocare(12, 1); if (!eroare) { 힙[obiect_referință + 2] = date_VALUE; if (date_VALUE >= -128 && date_VALUE <= 127) Store_întreg[date_VALUE + 128] = obiect_referință; } } 넣기(obiect_referință, 2); return true; }
            if (comandă_cod == 183 && Word_SMS(nume_constantă, "<init>") && Word_SMS(서술상수, "(I)V")) { int date_VALUE = 빼기(1), obiect_referință = 빼기(2); if (obiect_VALUE(obiect_referință, 12)) 힙[obiect_referință + 2] = date_VALUE; return true; }
            if (comandă_cod == 182 && Word_SMS(nume_constantă, "intValue") && Word_SMS(서술상수, "()I")) { int obiect_referință = 빼기(2); if (obiect_VALUE(obiect_referință, 12)) 넣기(힙[obiect_referință + 2], 1); return true; }
            if (comandă_cod == 184 && Word_SMS(nume_constantă, "toString") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(cifră_caracter(빼기(1)), 2); return true; }
        }
        if (Word_SMS(proprietar, "java/lang/Math") && comandă_cod == 184) {
            if (Word_SMS(nume_constantă, "abs") && Word_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_SMS(nume_constantă, "min") || Word_SMS(nume_constantă, "max")) && Word_SMS(서술상수, "(II)I")) { int byte_date = 빼기(1), 첫값 = 빼기(1); 넣기(Word_SMS(nume_constantă, "min") ? (첫값 < byte_date ? 첫값 : byte_date) : (첫값 > byte_date ? 첫값 : byte_date), 1); return true; }
        }
        if (Word_SMS(proprietar, "java/lang/System") && comandă_cod == 184) {
            if (Word_SMS(nume_constantă, "gc") && Word_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Word_SMS(nume_constantă, "arraycopy") && Word_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int intrare_COUNT = 빼기(1), destinație_VALUE_INDEX = 빼기(1), byte_date = 빼기(2), buta_poziție = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(byte_date)) {
                    int zonă_cod = 힙[첫값];
                    if (힙[byte_date] != zonă_cod || (zonă_cod != 2 && zonă_cod != 3 && (zonă_cod < 20 || zonă_cod > 23))) eroare_VALUE("arraycopy type mismatch");
                    else if (intrare_COUNT < 0 || buta_poziție < 0 || destinație_VALUE_INDEX < 0 || buta_poziție > 힙[첫값 + 1] - intrare_COUNT || destinație_VALUE_INDEX > 힙[byte_date + 1] - intrare_COUNT) eroare_VALUE("ArrayIndexOutOfBoundsException");
                    else if (첫값 == byte_date && destinație_VALUE_INDEX > buta_poziție) { for (int Loop_INDEX = intrare_COUNT - 1; Loop_INDEX >= 0; Loop_INDEX--) 힙[byte_date + 2 + destinație_VALUE_INDEX + Loop_INDEX] = 힙[첫값 + 2 + buta_poziție + Loop_INDEX]; }
                    else { for (int Loop_INDEX = 0; Loop_INDEX < intrare_COUNT && !eroare; Loop_INDEX++) { int date_VALUE = 힙[첫값 + 2 + buta_poziție + Loop_INDEX]; if (zonă_cod != 3 || 배열저장가능(byte_date, date_VALUE)) 힙[byte_date + 2 + destinație_VALUE_INDEX + Loop_INDEX] = date_VALUE; } }
                }
                return true;
            }
        }
        if (Word_SMS(proprietar, "java/util/ArrayList") || Word_SMS(proprietar, "java/util/List") || Word_SMS(proprietar, "java/util/HashMap") || Word_SMS(proprietar, "java/util/Map")) {
            모음호출(proprietar, nume_constantă, 서술상수, comandă_cod); return true;
        }
        return false;
    }
    static void 모음늘리기(int obiect_referință, int 필요수) {
        int Anteriorul_VALUE = 힙[obiect_referință + 2], capacitate_date = Anteriorul_VALUE == 0 ? 0 : 힙[Anteriorul_VALUE + 1];
        if (capacitate_date >= 필요수) return;
        int Următorul_poziție = capacitate_date < 8 ? 8 : capacitate_date * 2; if (Următorul_poziție < 필요수) Următorul_poziție = 필요수;
        int date_ARRAY = aloca_Stocare(3, Următorul_poziție); if (eroare) return;
        for (int Loop_INDEX = 0; Loop_INDEX < capacitate_date; Loop_INDEX++) 힙[date_ARRAY + 2 + Loop_INDEX] = 힙[Anteriorul_VALUE + 2 + Loop_INDEX];
        힙[obiect_referință + 2] = date_ARRAY; 힙참조[obiect_referință + 2] = 1;
    }
    static void 모음호출(int proprietar, int nume_constantă, int 서술상수, int comandă_cod) {
        boolean 대응참조 = Word_SMS(proprietar, "java/util/HashMap") || Word_SMS(proprietar, "java/util/Map"); int zonă_cod = 대응참조 ? 11 : 10;
        if (Word_SMS(nume_constantă, "<init>") && comandă_cod == 183 && Word_SMS(서술상수, "()V")) { int obiect_referință = 빼기(2); if (obiect_VALUE(obiect_referință, zonă_cod)) 모음늘리기(obiect_referință, 8); return; }
        if (comandă_cod != 182 && comandă_cod != 185) { eroare_VALUE("invalid collection invocation"); return; }
        if (Word_SMS(nume_constantă, "size") && Word_SMS(서술상수, "()I") || Word_SMS(nume_constantă, "isEmpty") && Word_SMS(서술상수, "()Z")) {
            int obiect_referință = 빼기(2); if (obiect_VALUE(obiect_referință, zonă_cod)) 넣기(Word_SMS(nume_constantă, "size") ? 힙[obiect_referință + 3] : 힙[obiect_referință + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_SMS(nume_constantă, "clear") && Word_SMS(서술상수, "()V")) { int obiect_referință = 빼기(2); if (obiect_VALUE(obiect_referință, zonă_cod)) { int date_ARRAY = 힙[obiect_referință + 2]; for (int Loop_INDEX = 0; Loop_INDEX < 힙[date_ARRAY + 1]; Loop_INDEX++) 힙[date_ARRAY + 2 + Loop_INDEX] = 0; 힙[obiect_referință + 3] = 0; } return; }
        if (!대응참조 && Word_SMS(nume_constantă, "add") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int date_VALUE = 빼기(2), obiect_referință = 빼기(2); if (!obiect_VALUE(obiect_referință, 10)) return;
            int intrare_COUNT = 힙[obiect_referință + 3]; 모음늘리기(obiect_referință, intrare_COUNT + 1); if (!eroare) { 힙[힙[obiect_referință + 2] + 2 + intrare_COUNT] = date_VALUE; 힙[obiect_referință + 3] = intrare_COUNT + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_SMS(nume_constantă, "get") || Word_SMS(nume_constantă, "remove")) && Word_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Word_SMS(nume_constantă, "set") && Word_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean sisteme_de_informații_atribuit = Word_SMS(nume_constantă, "set"); int date_VALUE = sisteme_de_informații_atribuit ? 빼기(2) : 0, intrare_poziție = 빼기(1), obiect_referință = 빼기(2);
            if (!obiect_VALUE(obiect_referință, 10)) return;
            int intrare_COUNT = 힙[obiect_referință + 3], date_ARRAY = 힙[obiect_referință + 2];
            if (intrare_poziție < 0 || intrare_poziție >= intrare_COUNT) { 예외던짐(6, "list index"); return; }
            int Anteriorul_VALUE = 힙[date_ARRAY + 2 + intrare_poziție];
            if (sisteme_de_informații_atribuit) 힙[date_ARRAY + 2 + intrare_poziție] = date_VALUE;
            if (Word_SMS(nume_constantă, "remove")) { for (int Loop_INDEX = intrare_poziție + 1; Loop_INDEX < intrare_COUNT; Loop_INDEX++) 힙[date_ARRAY + 1 + Loop_INDEX] = 힙[date_ARRAY + 2 + Loop_INDEX]; 힙[date_ARRAY + 1 + intrare_COUNT] = 0; 힙[obiect_referință + 3] = intrare_COUNT - 1; }
            넣기(Anteriorul_VALUE, 2); return;
        }
        if (대응참조 && (Word_SMS(nume_constantă, "get") || Word_SMS(nume_constantă, "remove")) && Word_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(nume_constantă, "put") && Word_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(nume_constantă, "containsKey") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_SMS(nume_constantă, "put"), elimina = Word_SMS(nume_constantă, "remove");
            int date_VALUE = 넣기여부 ? 빼기(2) : 0, Cheie_referință = 빼기(2), obiect_referință = 빼기(2); if (!obiect_VALUE(obiect_referință, 11)) return;
            int intrare_COUNT = 힙[obiect_referință + 3], date_ARRAY = 힙[obiect_referință + 2], 찾은여부 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < intrare_COUNT; Loop_INDEX++) if (값같음(Cheie_referință, 힙[date_ARRAY + 2 + 2 * Loop_INDEX])) { 찾은여부 = Loop_INDEX; break; }
            int Anteriorul_VALUE = 찾은여부 < 0 ? 0 : 힙[date_ARRAY + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(obiect_referință, (intrare_COUNT + 1) * 2); date_ARRAY = 힙[obiect_referință + 2]; 찾은여부 = intrare_COUNT; if (!eroare) 힙[obiect_referință + 3] = intrare_COUNT + 1; }
                if (!eroare) { 힙[date_ARRAY + 2 + 2 * 찾은여부] = Cheie_referință; 힙[date_ARRAY + 3 + 2 * 찾은여부] = date_VALUE; }
            }
            if (elimina && 찾은여부 >= 0) { for (int Loop_INDEX = 찾은여부 + 1; Loop_INDEX < intrare_COUNT; Loop_INDEX++) { 힙[date_ARRAY + 2 * Loop_INDEX] = 힙[date_ARRAY + 2 + 2 * Loop_INDEX]; 힙[date_ARRAY + 1 + 2 * Loop_INDEX] = 힙[date_ARRAY + 3 + 2 * Loop_INDEX]; } 힙[date_ARRAY + 2 * intrare_COUNT] = 0; 힙[date_ARRAY + 1 + 2 * intrare_COUNT] = 0; 힙[obiect_referință + 3] = intrare_COUNT - 1; }
            if (Word_SMS(nume_constantă, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(Anteriorul_VALUE, 2);
            return;
        }
        eroare_VALUE("unsupported collection method");
    }
    static boolean 잠금얻기(int obiect_referință) {
        if (!객체유효(obiect_referință)) return false;
        if (잠금깊이[obiect_referință] != 0 && blocare_proprietar[obiect_referință] != curent_fir + 1) { schimba_cerere = true; return false; }
        blocare_proprietar[obiect_referință] = curent_fir + 1; 잠금깊이[obiect_referință]++; return true;
    }
    static void lansa_blocare(int obiect_referință) {
        if (!객체유효(obiect_referință)) return;
        if (잠금깊이[obiect_referință] == 0 || blocare_proprietar[obiect_referință] != curent_fir + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[obiect_referință] == 0) blocare_proprietar[obiect_referință] = 0;
    }
    static boolean SWITCH_fir() {
        fir_cadru[curent_fir] = cadru_INDEX;
        if (cadru_INDEX < curent_fir * 32) fir_Stare[curent_fir] = 3;
        for (int Loop_INDEX = 0; Loop_INDEX < fir_COUNT; Loop_INDEX++) if (fir_Stare[Loop_INDEX] == 2 && fir_Stare[가닥대기[Loop_INDEX]] == 3) fir_Stare[Loop_INDEX] = 1;
        for (int Loop_INDEX = 1; Loop_INDEX <= fir_COUNT; Loop_INDEX++) {
            int Următorul_poziție = (curent_fir + Loop_INDEX) % fir_COUNT;
            if (fir_Stare[Următorul_poziție] == 1) { curent_fir = Următorul_poziție; cadru_INDEX = fir_cadru[Următorul_poziție]; schimba_cerere = false; return true; }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < fir_COUNT; Loop_INDEX++) if (fir_Stare[Loop_INDEX] != 3) { eroare_VALUE("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int nume_constantă, int 서술상수, int comandă_cod) { Proces_fir(nume_constantă, 서술상수, comandă_cod, false); }
    static void Proces_fir(int nume_constantă, int 서술상수, int comandă_cod, boolean Română) {
        if (comandă_cod == 184 && Word_SMS(nume_constantă, Română ? "YIELD_sarcină" : "yield") && Word_SMS(서술상수, "()V")) { schimba_cerere = true; return; }
        if (comandă_cod == 184 && Word_SMS(nume_constantă, "currentThread") && Word_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(fir_obiect[curent_fir], 2); return; }
        if (comandă_cod == 183 && Word_SMS(nume_constantă, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, Română ? "(LRomână/propriu/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int țintă_adresa = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), obiect_referință = 빼기(2);
            if (!객체유효(obiect_referință)) return;
            if (힙[obiect_referință] == 13) { 힙[obiect_referință + 2] = țintă_adresa; 힙참조[obiect_referință + 2] = 1; }
            else if (țintă_adresa != 0) eroare_VALUE("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (comandă_cod == 182 && (Word_SMS(nume_constantă, Română ? "buta_sarcină" : "start") || Word_SMS(nume_constantă, Română ? "기다리기" : "join")) && Word_SMS(서술상수, "()V") || comandă_cod == 182 && Word_SMS(nume_constantă, Română ? "살아있는가" : "isAlive") && Word_SMS(서술상수, "()Z")) {
            int obiect_referință = 빼기(2); if (!객체유효(obiect_referință)) return;
            int cont_VALUE = -1; for (int Loop_INDEX = 0; Loop_INDEX < fir_COUNT; Loop_INDEX++) if (fir_obiect[Loop_INDEX] == obiect_referință) cont_VALUE = Loop_INDEX;
            if (Word_SMS(nume_constantă, Română ? "살아있는가" : "isAlive")) { 넣기(cont_VALUE >= 0 && fir_Stare[cont_VALUE] != 3 ? 1 : 0, 1); return; }
            if (Word_SMS(nume_constantă, Română ? "기다리기" : "join")) { if (cont_VALUE >= 0 && fir_Stare[cont_VALUE] != 3) { 가닥대기[curent_fir] = cont_VALUE; fir_Stare[curent_fir] = 2; schimba_cerere = true; } return; }
            if (cont_VALUE >= 0) { 예외던짐(Română ? 38 : 16, "thread already started"); return; }
            if (fir_COUNT == 4) { eroare_VALUE("thread limit (4 including main)"); return; }
            int țintă_adresa = 힙[obiect_referință] == 13 ? 힙[obiect_referință + 2] : obiect_referință;
            int Fișier_INDEX = țintă_adresa > 0 && 힙[țintă_adresa] >= 32 ? nume_metodă(힙[țintă_adresa] - 32, Română ? "Execută" : "run", "()V") : -1;
            if (țintă_adresa != 0 && Fișier_INDEX < 0) { eroare_VALUE("Runnable.run required"); return; }
            cont_VALUE = fir_COUNT++; fir_obiect[cont_VALUE] = obiect_referință; fir_țintă[cont_VALUE] = țintă_adresa;
            int cadru = cont_VALUE * 32; fir_cadru[cont_VALUE] = Fișier_INDEX < 0 ? cadru - 1 : cadru; fir_Stare[cont_VALUE] = Fișier_INDEX < 0 ? 3 : 1;
            if (Fișier_INDEX >= 0) { cadru_metodă[cadru] = Fișier_INDEX; cadru_poziție[cadru] = metodă_buta[Fișier_INDEX]; local_VALUE[cadru * 128] = țintă_adresa; local_Tip[cadru * 128] = 2; }
            return;
        }
        eroare_VALUE("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], adresa_SMS = new int[16];
    static int local_adresa() { return adresa_obiect(0x7f000001); }
    static int adresa_obiect(int VALUE) { int obiect_referință = aloca_Stocare(14, 1); if (!eroare) 힙[obiect_referință + 2] = VALUE; return obiect_referință; }
    static int 주소해독(int obiect_referință) {
        if (obiect_referință == 0 || 글같음(obiect_referință, gazdă_caracter("localhost"), false)) return 0x7f000001;
        if (!obiect_VALUE(obiect_referință, 1)) return 0;
        int date_VALUE = 0, total_COUNT = 0, adresa_byte = 0, 자릿수 = 0, intrare_COUNT = 힙[obiect_referință + 1];
        for (int Loop_INDEX = 0; Loop_INDEX <= intrare_COUNT; Loop_INDEX++) {
            int cod_caracter = Loop_INDEX == intrare_COUNT ? '.' : 힙[obiect_referință + 2 + Loop_INDEX];
            if (cod_caracter == '.') { if (자릿수 == 0 || total_COUNT == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } date_VALUE = date_VALUE << 8 | adresa_byte; total_COUNT++; adresa_byte = 자릿수 = 0; }
            else { if (cod_caracter < '0' || cod_caracter > '9' || ++자릿수 > 3 || (adresa_byte = adresa_byte * 10 + cod_caracter - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (total_COUNT != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return date_VALUE;
    }
    static int adresa_caracter(int date_VALUE) {
        int intrare_COUNT = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int adresa_byte = date_VALUE >>> 이동비트 & 255;
            if (adresa_byte >= 100) adresa_SMS[intrare_COUNT++] = '0' + adresa_byte / 100;
            if (adresa_byte >= 10) adresa_SMS[intrare_COUNT++] = '0' + adresa_byte / 10 % 10;
            adresa_SMS[intrare_COUNT++] = '0' + adresa_byte % 10; if (이동비트 != 0) adresa_SMS[intrare_COUNT++] = '.';
        }
        int obiect_referință = aloca_Stocare(1, intrare_COUNT); if (!eroare) for (int Loop_INDEX = 0; Loop_INDEX < intrare_COUNT; Loop_INDEX++) 힙[obiect_referință + 2 + Loop_INDEX] = adresa_SMS[Loop_INDEX]; return obiect_referință;
    }
    static void 통신호출(int proprietar, int nume_constantă, int 서술상수, int comandă_cod) {
        if (Word_SMS(proprietar, "java/net/InetAddress")) {
            if (comandă_cod == 184 && Word_SMS(nume_constantă, "getLoopbackAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(local_adresa(), 2); return; }
            if (comandă_cod == 184 && Word_SMS(nume_constantă, "getByName") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int date_VALUE = 주소해독(빼기(2)); if (던진객체 == 0 && !eroare) 넣기(adresa_obiect(date_VALUE), 2); return;
            }
            if (comandă_cod == 182 && Word_SMS(nume_constantă, "getHostAddress") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int obiect_referință = 빼기(2); if (obiect_VALUE(obiect_referință, 14)) 넣기(adresa_caracter(힙[obiect_referință + 2]), 2); return; }
        }
        if (Word_SMS(proprietar, "java/net/DatagramPacket")) {
            if (comandă_cod == 183 && Word_SMS(nume_constantă, "<init>") && (Word_SMS(서술상수, "([BI)V") || Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean destinație_VALUE_referință = Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int număr_port = destinație_VALUE_referință ? 빼기(1) : 0, adresa_referință = destinație_VALUE_referință ? 빼기(2) : 0;
                int intrare_COUNT = 빼기(1), date_ARRAY = 빼기(2), obiect_referință = 빼기(2);
                if (!obiect_VALUE(obiect_referință, 16) || !obiect_VALUE(date_ARRAY, 20)) return;
                if (intrare_COUNT < 0 || intrare_COUNT > 힙[date_ARRAY + 1] || număr_port < 0 || număr_port > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (adresa_referință != 0 && !obiect_VALUE(adresa_referință, 14)) return;
                힙[obiect_referință + 2] = date_ARRAY; 힙참조[obiect_referință + 2] = 1; 힙[obiect_referință + 3] = intrare_COUNT;
                힙[obiect_referință + 4] = adresa_referință; 힙참조[obiect_referință + 4] = 1; 힙[obiect_referință + 5] = număr_port; return;
            }
            if (comandă_cod == 182 && Word_SMS(nume_constantă, "setLength") && Word_SMS(서술상수, "(I)V")) {
                int intrare_COUNT = 빼기(1), obiect_referință = 빼기(2); if (!obiect_VALUE(obiect_referință, 16)) return;
                if (intrare_COUNT < 0 || intrare_COUNT > 힙[힙[obiect_referință + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[obiect_referință + 3] = intrare_COUNT; return;
            }
            if (comandă_cod == 182 && (Word_SMS(nume_constantă, "getData") && Word_SMS(서술상수, "()[B") || Word_SMS(nume_constantă, "getLength") && Word_SMS(서술상수, "()I") || Word_SMS(nume_constantă, "getAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;") || Word_SMS(nume_constantă, "getPort") && Word_SMS(서술상수, "()I"))) {
                int obiect_referință = 빼기(2); if (!obiect_VALUE(obiect_referință, 16)) return;
                int intrare_poziție = Word_SMS(nume_constantă, "getData") ? 2 : Word_SMS(nume_constantă, "getLength") ? 3 : Word_SMS(nume_constantă, "getAddress") ? 4 : 5;
                넣기(힙[obiect_referință + intrare_poziție], intrare_poziție == 2 || intrare_poziție == 4 ? 2 : 1); return;
            }
        }
        if (Word_SMS(proprietar, "java/net/DatagramSocket")) {
            if (comandă_cod == 183 && Word_SMS(nume_constantă, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(I)V"))) {
                int număr_port = Word_SMS(서술상수, "()V") ? 0 : 빼기(1), obiect_referință = 빼기(2); if (!obiect_VALUE(obiect_referință, 15)) return;
                if (număr_port < 0 || număr_port > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = utilizator.crea_rețea(număr_port); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[obiect_referință + 2] = 열린파일번호; return;
            }
            if (comandă_cod == 182 && Word_SMS(nume_constantă, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), obiect_referință = 빼기(2); if (!obiect_VALUE(obiect_referință, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[obiect_referință + 3] = 밀리초값; return;
            }
            if (comandă_cod == 182 && Word_SMS(nume_constantă, "getLocalPort") && Word_SMS(서술상수, "()I")) { int obiect_referință = 빼기(2); if (obiect_VALUE(obiect_referință, 15)) 넣기(힙[obiect_referință + 2] < 0 ? -1 : utilizator.rețea_muta(힙[obiect_referință + 2]), 1); return; }
            if (comandă_cod == 182 && Word_SMS(nume_constantă, "isClosed") && Word_SMS(서술상수, "()Z")) { int obiect_referință = 빼기(2); if (obiect_VALUE(obiect_referință, 15)) 넣기(힙[obiect_referință + 2] < 0 ? 1 : 0, 1); return; }
            if (comandă_cod == 182 && Word_SMS(nume_constantă, "close") && Word_SMS(서술상수, "()V")) { int obiect_referință = 빼기(2); if (obiect_VALUE(obiect_referință, 15) && 힙[obiect_referință + 2] >= 0) { utilizator.파일서술자닫기(힙[obiect_referință + 2]); 힙[obiect_referință + 2] = -1; } return; }
            if (comandă_cod == 182 && (Word_SMS(nume_constantă, "send") || Word_SMS(nume_constantă, "receive")) && Word_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int pachet = 빼기(2), obiect_referință = 빼기(2); if (!obiect_VALUE(pachet, 16) || !obiect_VALUE(obiect_referință, 15)) return;
                int date_ARRAY = 힙[pachet + 2], 유효길이 = 힙[pachet + 3], 열린파일번호 = 힙[obiect_referință + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_SMS(nume_constantă, "send")) {
                    if (!obiect_VALUE(힙[pachet + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < 유효길이; Loop_INDEX++) 통신임시[Loop_INDEX] = 힙[date_ARRAY + 2 + Loop_INDEX];
                    if (utilizator.trimite_rețea(열린파일번호, 힙[힙[pachet + 4] + 2], 힙[pachet + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int intrare_COUNT = utilizator.primi_rețea(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (intrare_COUNT == -11) {
                        int curent_oră = utilizator.밀리초();
                        if (힙[obiect_referință + 4] == 0) 힙[obiect_referință + 4] = curent_oră + 1;
                        if (힙[obiect_referință + 3] > 0 && curent_oră - (힙[obiect_referință + 4] - 1) >= 힙[obiect_referință + 3]) { 힙[obiect_referință + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(obiect_referință, 2); 넣기(pachet, 2); cadru_poziție[cadru_INDEX] = 틀명령[cadru_INDEX]; schimba_cerere = true; return;
                    }
                    힙[obiect_referință + 4] = 0;
                    if (intrare_COUNT < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < intrare_COUNT; Loop_INDEX++) 힙[date_ARRAY + 2 + Loop_INDEX] = (byte)통신임시[Loop_INDEX];
                    힙[pachet + 3] = intrare_COUNT; 힙[pachet + 4] = adresa_obiect(통신임시[513]); 힙참조[pachet + 4] = 1; 힙[pachet + 5] = 통신임시[512];
                }
                return;
            }
        }
        eroare_VALUE("unsupported java.net method");
    }
    static boolean 흐름대기(int obiect_referință) {
        int curent_oră = utilizator.밀리초();
        if (힙[obiect_referință + 5] == 0) 힙[obiect_referință + 5] = curent_oră + 1;
        if (힙[obiect_referință + 3] > 0 && curent_oră - (힙[obiect_referință + 5] - 1) >= 힙[obiect_referință + 3]) { 힙[obiect_referință + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        cadru_poziție[cadru_INDEX] = 틀명령[cadru_INDEX]; schimba_cerere = true; return true;
    }
    static void 흐름호출(int proprietar, int nume_constantă, int 서술상수, int comandă_cod) {
        boolean primi_pagina = Word_SMS(proprietar, "java/net/ServerSocket"), flux = Word_SMS(proprietar, "java/io/InputStream") || Word_SMS(proprietar, "java/io/OutputStream");
        if (!flux && comandă_cod == 183 && Word_SMS(nume_constantă, "<init>")) {
            boolean 빈여부 = Word_SMS(서술상수, "()V"), 이름지정여부 = Word_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || primi_pagina && Word_SMS(서술상수, "(I)V") || !primi_pagina && (이름지정여부 || 주소지정여부))) { eroare_VALUE("unsupported socket constructor"); return; }
            int număr_port = 빈여부 ? 0 : 빼기(1), adresa_referință = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, obiect_referință = 빼기(2);
            if (!obiect_VALUE(obiect_referință, primi_pagina ? 18 : 17)) return;
            if (număr_port < 0 || număr_port > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !obiect_VALUE(adresa_referință, 14)) return;
            int ID_rețea = 이름지정여부 ? 주소해독(adresa_referință) : 주소지정여부 ? 힙[adresa_referință + 2] : 0x7f000001;
            if (eroare || 던진객체 != 0) return;
            int 열린파일번호 = utilizator.flux_control(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : primi_pagina ? utilizator.flux_control(1, 열린파일번호, număr_port) : utilizator.conecta_flux(열린파일번호, ID_rețea, număr_port);
            if (처리값 < 0) { utilizator.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[obiect_referință + 2] = 열린파일번호; 힙[obiect_referință + 4] = număr_port; 힙[obiect_referință + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!flux && Word_SMS(nume_constantă, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), obiect_referință = 빼기(2); if (!obiect_VALUE(obiect_referință, primi_pagina ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[obiect_referință + 3] = 밀리초값; return; }
        if (!flux && Word_SMS(nume_constantă, "close") && Word_SMS(서술상수, "()V")) { int obiect_referință = 빼기(2); if (obiect_VALUE(obiect_referință, primi_pagina ? 18 : 17) && 힙[obiect_referință + 2] >= 0) { utilizator.파일서술자닫기(힙[obiect_referință + 2]); 힙[obiect_referință + 2] = -1; } return; }
        if (!flux && (Word_SMS(nume_constantă, "getLocalPort") || Word_SMS(nume_constantă, "getPort") || Word_SMS(nume_constantă, "isClosed") || Word_SMS(nume_constantă, "isConnected"))) {
            int obiect_referință = 빼기(2); if (!obiect_VALUE(obiect_referință, primi_pagina ? 18 : 17)) return;
            넣기(Word_SMS(nume_constantă, "isClosed") ? 힙[obiect_referință + 2] < 0 ? 1 : 0 : Word_SMS(nume_constantă, "isConnected") ? 힙[obiect_referință + 6] : Word_SMS(nume_constantă, "getPort") ? 힙[obiect_referință + 4] : 힙[obiect_referință + 2] < 0 ? -1 : utilizator.flux_control(4, 힙[obiect_referință + 2], 0), 1); return;
        }
        if (primi_pagina && Word_SMS(nume_constantă, "accept") && Word_SMS(서술상수, "()Ljava/net/Socket;")) {
            int obiect_referință = 빼기(2); if (!obiect_VALUE(obiect_referință, 18)) return; int 열린파일번호 = utilizator.flux_control(3, 힙[obiect_referință + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(obiect_referință)) 넣기(obiect_referință, 2); return; }
            힙[obiect_referință + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = aloca_Stocare(17, 5); if (eroare) { utilizator.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = utilizator.flux_control(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!primi_pagina && !flux && ((Word_SMS(nume_constantă, "getInputStream") && Word_SMS(서술상수, "()Ljava/io/InputStream;")) || (Word_SMS(nume_constantă, "getOutputStream") && Word_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int obiect_referință = 빼기(2); if (!obiect_VALUE(obiect_referință, 17)) return; if (힙[obiect_referință + 2] < 0 || 힙[obiect_referință + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = aloca_Stocare(19, 4); if (eroare) return; 힙[반환값 + 2] = obiect_referință; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Word_SMS(nume_constantă, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (flux) {
            boolean 읽기여부 = Word_SMS(nume_constantă, "read"), sisteme_de_informații_scriere_operație = Word_SMS(nume_constantă, "write"), bloc = Word_SMS(서술상수, "([B)I") || Word_SMS(서술상수, "([B)V"), sisteme_de_informații_SUBARRAY = Word_SMS(서술상수, "([BII)I") || Word_SMS(서술상수, "([BII)V");
            int intrare_COUNT = sisteme_de_informații_SUBARRAY ? 빼기(1) : 0, 시작변위 = sisteme_de_informații_SUBARRAY ? 빼기(1) : 0, date_ARRAY = bloc || sisteme_de_informații_SUBARRAY ? 빼기(2) : 0;
            int date_VALUE = sisteme_de_informații_scriere_operație && Word_SMS(서술상수, "(I)V") ? 빼기(1) : 0, obiect_referință = 빼기(2);
            if (!obiect_VALUE(obiect_referință, 19)) return; int părinte_referință = 힙[obiect_referință + 2], 열린파일번호 = 힙[părinte_referință + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_SMS(nume_constantă, "close") && Word_SMS(서술상수, "()V")) { utilizator.파일서술자닫기(열린파일번호); 힙[părinte_referință + 2] = -1; return; }
            if (Word_SMS(nume_constantă, "flush") && Word_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !sisteme_de_informații_scriere_operație) || 읽기여부 != (힙[obiect_referință + 3] == 0)) { eroare_VALUE("unsupported stream operation"); return; }
            if (bloc || sisteme_de_informații_SUBARRAY) { if (!obiect_VALUE(date_ARRAY, 20)) return; if (bloc) intrare_COUNT = 힙[date_ARRAY + 1]; if (시작변위 < 0 || intrare_COUNT < 0 || 시작변위 > 힙[date_ARRAY + 1] - intrare_COUNT) { 예외던짐(6, "stream array bounds"); return; } }
            else intrare_COUNT = 1;
            if (intrare_COUNT == 0) { if (읽기여부) 넣기(0, 1); return; }
            int Finalizate_COUNT = sisteme_de_informații_scriere_operație ? 힙[obiect_referință + 4] : 0, 처리값 = 0;
            while (Finalizate_COUNT < intrare_COUNT) {
                처리값 = 읽기여부 ? utilizator.파일한바이트읽기(열린파일번호) : utilizator.파일한바이트쓰기(열린파일번호, bloc || sisteme_de_informații_SUBARRAY ? 힙[date_ARRAY + 2 + 시작변위 + Finalizate_COUNT] : date_VALUE);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (bloc || sisteme_de_informații_SUBARRAY)) 힙[date_ARRAY + 2 + 시작변위 + Finalizate_COUNT] = (byte)처리값;
                Finalizate_COUNT++; if (읽기여부 && !(bloc || sisteme_de_informații_SUBARRAY)) break;
            }
            if (처리값 == -11 && (sisteme_de_informații_scriere_operație || Finalizate_COUNT == 0)) {
                힙[obiect_referință + 4] = Finalizate_COUNT;
                if (흐름대기(părinte_referință)) { 넣기(obiect_referință, 2); if (bloc || sisteme_de_informații_SUBARRAY) 넣기(date_ARRAY, 2); if (sisteme_de_informații_SUBARRAY) { 넣기(시작변위, 1); 넣기(intrare_COUNT, 1); } if (sisteme_de_informații_scriere_operație && !(bloc || sisteme_de_informații_SUBARRAY)) 넣기(date_VALUE, 1); } return;
            }
            힙[obiect_referință + 4] = 0; 힙[părinte_referință + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(Finalizate_COUNT == 0 && 처리값 == 256 ? -1 : bloc || sisteme_de_informații_SUBARRAY ? Finalizate_COUNT : 처리값, 1); return;
        }
        eroare_VALUE("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int nume_constantă) {
        if (Word_SMS(nume_constantă, "Română/propriu/Fereastră")) return 24;
        if (Word_SMS(nume_constantă, "Română/propriu/Etichetă")) return 26;
        if (Word_SMS(nume_constantă, "Română/propriu/buton")) return 27;
        if (Word_SMS(nume_constantă, "Română/propriu/câmp_text")) return 28;
        if (Word_SMS(nume_constantă, "Română/propriu/Acțiune_înștiințare")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int nume_constantă) {
        return 한국어화면종(nume_constantă) != 0 || Word_SMS(nume_constantă, "Română/propriu/화면구성요소") || Word_SMS(nume_constantă, "Română/propriu/eveniment_coadă");
    }
    static int 화면종(int nume_constantă) {
        int 한국어종 = 한국어화면종(nume_constantă); if (한국어종 != 0) return 한국어종;
        if (Word_SMS(nume_constantă, "javax/swing/JFrame")) return 24;
        if (Word_SMS(nume_constantă, "javax/swing/JPanel")) return 25;
        if (Word_SMS(nume_constantă, "javax/swing/JLabel")) return 26;
        if (Word_SMS(nume_constantă, "javax/swing/JButton")) return 27;
        if (Word_SMS(nume_constantă, "javax/swing/JTextField")) return 28;
        if (Word_SMS(nume_constantă, "java/awt/event/ActionEvent")) return 29;
        if (Word_SMS(nume_constantă, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int nume_constantă) {
        return 화면종(nume_constantă) != 0 || Word_SMS(nume_constantă, "java/awt/Component") || Word_SMS(nume_constantă, "java/awt/Container") || Word_SMS(nume_constantă, "javax/swing/JComponent") || Word_SMS(nume_constantă, "javax/swing/AbstractButton") || Word_SMS(nume_constantă, "javax/swing/text/JTextComponent") || Word_SMS(nume_constantă, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int obiect_referință) { if (!객체유효(obiect_referință)) return false; if (힙[obiect_referință] < 24 || 힙[obiect_referință] > 28) { eroare_VALUE("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int obiect_referință, int SMS_referință) {
        if (SMS_referință != 0 && !obiect_VALUE(SMS_referință, 1)) return;
        int intrare_COUNT = SMS_referință == 0 ? 0 : 힙[SMS_referință + 1]; if (intrare_COUNT > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < intrare_COUNT; Loop_INDEX++) 화면글임시[Loop_INDEX] = 힙[SMS_referință + 2 + Loop_INDEX];
        if (utilizator.화면글(힙[obiect_referință + 2], 화면글임시, intrare_COUNT) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[obiect_referință + 3] = SMS_referință; 힙참조[obiect_referință + 3] = 1;
    }
    static int 화면문자읽기(int obiect_referință) {
        int cont_VALUE = 힙[obiect_referință + 2], intrare_COUNT = utilizator.화면연결(8, cont_VALUE, 0, 0, 0, 0), 사용수 = 0;
        if (intrare_COUNT < 0) { eroare_VALUE("GUI text read failed"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < intrare_COUNT; Loop_INDEX++) { int 부호값 = utilizator.화면연결(9, cont_VALUE, Loop_INDEX, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = aloca_Stocare(1, 사용수); if (!eroare) for (int Loop_INDEX = 0; Loop_INDEX < 사용수; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 화면글임시[Loop_INDEX]; return 반환값;
    }
    /* Română 객체를 직접 만들고 nucleu_VALUE 화면 기능에 연결한다. Swing obiect_VALUE/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int proprietar, int nume_constantă, int 서술상수, int comandă_cod) {
        if (Word_SMS(proprietar, "Română/propriu/eveniment_coadă")) {
            if (comandă_cod == 184 && Word_SMS(nume_constantă, "나중에실행") && Word_SMS(서술상수, "(LRomână/propriu/실행할일;)V")) {
                int sarcină_Acțiune = 빼기(2); if (!객체유효(sarcină_Acțiune)) return;
                if (나중수 == 8) { eroare_VALUE("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = sarcină_Acțiune; return;
            }
            if (comandă_cod == 184 && Word_SMS(nume_constantă, "사건처리중인가") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            eroare_VALUE("지원하지 않는 Română 화면 일정 호출"); return;
        }
        if (Word_SMS(proprietar, "Română/propriu/Acțiune_înștiințare")) {
            int înștiințare = 빼기(2); if (!obiect_VALUE(înștiințare, 29) || 힙[înștiințare + 3] == 0) return;
            if (Word_SMS(nume_constantă, "sursă_eveniment") && Word_SMS(서술상수, "()LRomână/propriu/화면구성요소;")) 넣기(힙[înștiințare + 2], 2);
            else if (Word_SMS(nume_constantă, "comandă_SMS") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[înștiințare + 2]), 2);
            else if (Word_SMS(nume_constantă, "INDEX") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else eroare_VALUE("지원하지 않는 Română Acțiuni înștiințare 호출"); return;
        }
        if (comandă_cod == 183 && Word_SMS(nume_constantă, "<init>")) {
            int 종류 = 한국어화면종(proprietar), 받이 = 0, 가로 = 0, Verticală_poziție = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Word_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (utilizator.화면너비() - 폭) / 2; Verticală_poziție = (utilizator.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Word_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Word_SMS(서술상수, "(Ljava/lang/String;IIIILRomână/propriu/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); Verticală_poziție = 빼기(1); 가로 = 빼기(1);
            } else { eroare_VALUE("지원하지 않는 Română 화면 생성자"); return; }
            int SMS = 빼기(2), element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || Verticală_poziție < 0 || 폭 > utilizator.화면너비() - 가로 || 높이 > utilizator.화면높이() - Verticală_poziție) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDEX = utilizator.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (INDEX < 1 || INDEX > 32) { eroare_VALUE("화면 element_VALUE 자리가 가득 찼습니다"); return; }
            힙[element_VALUE + 2] = INDEX; 화면참조[INDEX - 1] = element_VALUE;
            힙[element_VALUE + 5] = 가로; 힙[element_VALUE + 6] = Verticală_poziție; 힙[element_VALUE + 7] = 폭; 힙[element_VALUE + 8] = 높이; 힙[element_VALUE + 10] = 2;
            힙[element_VALUE + 4] = 받이; 힙참조[element_VALUE + 4] = 1; 힙[element_VALUE + 12] = 1;
            utilizator.화면연결(1, INDEX, 가로, Verticală_poziție, 폭, 높이);
            if (종류 == 24) utilizator.화면연결(7, INDEX, 2, 0, 0, 0);
            화면문자설정(element_VALUE, SMS); return;
        }
        if (comandă_cod != 182) { eroare_VALUE("잘못된 Română 화면 호출 Comandă"); return; }
        if (Word_SMS(nume_constantă, "scriere_SMS") && Word_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int SMS = 빼기(2), element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 화면문자설정(element_VALUE, SMS); return;
        }
        if (Word_SMS(nume_constantă, "글읽기") && Word_SMS(서술상수, "()Ljava/lang/String;")) {
            int element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 넣기(화면문자읽기(element_VALUE), 2); return;
        }
        if (Word_SMS(nume_constantă, "동작맡기기") && Word_SMS(서술상수, "(LRomână/propriu/동작받이;)V")) {
            int 받이 = 빼기(2), element_VALUE = 빼기(2);
            if (화면객체(element_VALUE)) { 힙[element_VALUE + 4] = 받이; 힙참조[element_VALUE + 4] = 1; 힙[element_VALUE + 12] = 1; } return;
        }
        if (Word_SMS(nume_constantă, "adăuga_element") && Word_SMS(서술상수, "(LRomână/propriu/화면구성요소;)V")) {
            int copil_VALUE = 빼기(2), părinte_VALUE = 빼기(2); if (!화면객체(copil_VALUE) || !화면객체(părinte_VALUE)) return;
            if (utilizator.화면연결(2, 힙[părinte_VALUE + 2], 힙[copil_VALUE + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[copil_VALUE + 11] = părinte_VALUE; 힙참조[copil_VALUE + 11] = 1; return;
        }
        if (Word_SMS(nume_constantă, "자리정하기") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), Verticală_poziție = 빼기(1), 가로 = 빼기(1), element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (utilizator.화면연결(1, 힙[element_VALUE + 2], 가로, Verticală_poziție, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[element_VALUE + 5] = 가로; 힙[element_VALUE + 6] = Verticală_poziție; 힙[element_VALUE + 7] = 폭; 힙[element_VALUE + 8] = 높이; return;
        }
        if ((Word_SMS(nume_constantă, "afișa_fereastră") || Word_SMS(nume_constantă, "Închide")) && Word_SMS(서술상수, "()V")) {
            boolean vizibilitate_VALUE = Word_SMS(nume_constantă, "afișa_fereastră"); int element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (utilizator.화면연결(vizibilitate_VALUE ? 3 : 4, 힙[element_VALUE + 2], vizibilitate_VALUE ? 1 : 0, 0, 0, 0) < 0) { eroare_VALUE("화면은 대화형 명령에서 실행해야 합니다"); return; }
            힙[element_VALUE + 9] = vizibilitate_VALUE ? 1 : 0; return;
        }
        if (Word_SMS(nume_constantă, "보이는가") && Word_SMS(서술상수, "()Z")) { int element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 넣기(힙[element_VALUE + 9], 1); return; }
        eroare_VALUE("지원하지 않는 Română 화면 metodă_VALUE");
    }
    static void 화면호출(int proprietar, int nume_constantă, int 서술상수, int comandă_cod) {
        if (Word_SMS(proprietar, "javax/swing/SwingUtilities")) {
            if (comandă_cod == 184 && Word_SMS(nume_constantă, "invokeLater") && Word_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int obiect_referință = 빼기(2); if (!객체유효(obiect_referință)) return; if (나중수 == 8) { eroare_VALUE("invokeLater queue full"); return; } 나중실행[나중수++] = obiect_referință; return; }
            if (comandă_cod == 184 && Word_SMS(nume_constantă, "isEventDispatchThread") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            eroare_VALUE("unsupported SwingUtilities method"); return;
        }
        if (Word_SMS(proprietar, "java/awt/event/ActionEvent")) {
            int obiect_referință = 빼기(2); if (!obiect_VALUE(obiect_referință, 29)) return;
            if (Word_SMS(nume_constantă, "getSource") && Word_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[obiect_referință + 2], 2);
            else if (Word_SMS(nume_constantă, "getActionCommand") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[obiect_referință + 2]), 2);
            else if (Word_SMS(nume_constantă, "getID") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else eroare_VALUE("unsupported ActionEvent method"); return;
        }
        if (comandă_cod == 183 && Word_SMS(nume_constantă, "<init>")) {
            int COLUMNS = 0, SMS_referință = 0;
            if (Word_SMS(서술상수, "(I)V")) COLUMNS = 빼기(1);
            else if (Word_SMS(서술상수, "(Ljava/lang/String;I)V")) { COLUMNS = 빼기(1); SMS_referință = 빼기(2); }
            else if (Word_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_referință = 빼기(2);
            else if (Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_SMS(서술상수, "()V")) { eroare_VALUE("unsupported Swing constructor"); return; }
            int obiect_referință = 빼기(2); if (!객체유효(obiect_referință)) return;
            if (힙[obiect_referință] == 30) { eroare_VALUE("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(obiect_referință) || COLUMNS < 0) return;
            int cont_VALUE = utilizator.화면연결(0, 힙[obiect_referință] - 23, 0, 0, 0, 0);
            if (cont_VALUE < 1 || cont_VALUE > 32) { eroare_VALUE("GUI widget slots exhausted"); return; }
            힙[obiect_referință + 2] = cont_VALUE; 화면참조[cont_VALUE - 1] = obiect_referință; 힙[obiect_referință + 5] = 힙[obiect_referință] == 24 ? 130 : 16; 힙[obiect_referință + 6] = 힙[obiect_referință] == 24 ? 110 : 16;
            힙[obiect_referință + 7] = 힙[obiect_referință] == 24 ? 380 : 220; 힙[obiect_referință + 8] = 힙[obiect_referință] == 24 ? 240 : 28; 힙[obiect_referință + 10] = 1;
            화면문자설정(obiect_referință, SMS_referință); return;
        }
        if (Word_SMS(nume_constantă, "setText") || Word_SMS(nume_constantă, "setTitle")) { int SMS_referință = 빼기(2), obiect_referință = 빼기(2); if (화면객체(obiect_referință) && Word_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(obiect_referință, SMS_referință); return; }
        if (Word_SMS(nume_constantă, "getText") || Word_SMS(nume_constantă, "getTitle")) { int obiect_referință = 빼기(2); if (화면객체(obiect_referință) && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(obiect_referință), 2); return; }
        if (Word_SMS(nume_constantă, "addActionListener") && Word_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int primi_referință = 빼기(2), obiect_referință = 빼기(2); if (화면객체(obiect_referință)) { 힙[obiect_referință + 4] = primi_referință; 힙참조[obiect_referință + 4] = 1; } return; }
        if (Word_SMS(nume_constantă, "getContentPane") && Word_SMS(서술상수, "()Ljava/awt/Container;")) { int obiect_referință = 빼기(2); if (화면객체(obiect_referință)) 넣기(obiect_referință, 2); return; }
        if (Word_SMS(nume_constantă, "setLayout") && Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Aspect_referință = 빼기(2), obiect_referință = 빼기(2); if (화면객체(obiect_referință) && Aspect_referință != 0) eroare_VALUE("only absolute layout (null) is supported"); return; }
        if (Word_SMS(nume_constantă, "add") && (Word_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Aspect_condiție = Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Aspect_condiție) 빼기(2);
            int copil_referință = 빼기(2), obiect_referință = 빼기(2); if (!화면객체(copil_referință) || !화면객체(obiect_referință)) return;
            if (utilizator.화면연결(2, 힙[obiect_referință + 2], 힙[copil_referință + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[copil_referință + 11] = obiect_referință; 힙참조[copil_referință + 11] = 1; if (!Aspect_condiție) 넣기(copil_referință, 2); return;
        }
        if (Word_SMS(nume_constantă, "setBounds") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), coordonata_X = 빼기(1), obiect_referință = 빼기(2); if (!화면객체(obiect_referință)) return;
            if (utilizator.화면연결(1, 힙[obiect_referință + 2], coordonata_X, 세로좌표, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[obiect_referință + 5] = coordonata_X; 힙[obiect_referință + 6] = 세로좌표; 힙[obiect_referință + 7] = 너비; 힙[obiect_referință + 8] = 높이; return;
        }
        if (Word_SMS(nume_constantă, "setSize") && Word_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), obiect_referință = 빼기(2); if (!화면객체(obiect_referință)) return;
            if (utilizator.화면연결(1, 힙[obiect_referință + 2], 힙[obiect_referință + 5], 힙[obiect_referință + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[obiect_referință + 7] = 너비; 힙[obiect_referință + 8] = 높이; } return;
        }
        if (Word_SMS(nume_constantă, "setLocationRelativeTo") && Word_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), obiect_referință = 빼기(2); if (!화면객체(obiect_referință)) return; if (상대배치 != 0) { eroare_VALUE("only screen centering supported"); return; } 힙[obiect_referință + 5] = (utilizator.화면너비() - 힙[obiect_referință + 7]) / 2; 힙[obiect_referință + 6] = (utilizator.화면높이() - 힙[obiect_referință + 8]) / 2; utilizator.화면연결(1, 힙[obiect_referință + 2], 힙[obiect_referință + 5], 힙[obiect_referință + 6], 힙[obiect_referință + 7], 힙[obiect_referință + 8]); return; }
        if (Word_SMS(nume_constantă, "setDefaultCloseOperation") && Word_SMS(서술상수, "(I)V")) { int Policy = 빼기(1), obiect_referință = 빼기(2); if (화면객체(obiect_referință)) { if (Policy < 0 || Policy > 3) 예외던짐(9, "close policy"); else { 힙[obiect_referință + 10] = Policy; utilizator.화면연결(7, 힙[obiect_referință + 2], Policy, 0, 0, 0); } } return; }
        if (Word_SMS(nume_constantă, "setVisible") && Word_SMS(서술상수, "(Z)V")) { int date_VALUE = 빼기(1), obiect_referință = 빼기(2); if (화면객체(obiect_referință)) { int 처리값 = utilizator.화면연결(3, 힙[obiect_referință + 2], date_VALUE, 0, 0, 0); if (처리값 < 0) eroare_VALUE("Swing requires a standalone interactive command"); else 힙[obiect_referință + 9] = date_VALUE; } return; }
        if (Word_SMS(nume_constantă, "dispose") && Word_SMS(서술상수, "()V")) { int obiect_referință = 빼기(2); if (화면객체(obiect_referință)) { utilizator.화면연결(4, 힙[obiect_referință + 2], 0, 0, 0, 0); 힙[obiect_referință + 9] = 0; } return; }
        if (Word_SMS(nume_constantă, "repaint") || Word_SMS(nume_constantă, "validate")) { int obiect_referință = 빼기(2); if (!화면객체(obiect_referință) || !Word_SMS(서술상수, "()V")) return; utilizator.화면연결(1, 힙[obiect_referință + 2], 힙[obiect_referință + 5], 힙[obiect_referință + 6], 힙[obiect_referință + 7], 힙[obiect_referință + 8]); return; }
        if (Word_SMS(nume_constantă, "isVisible") && Word_SMS(서술상수, "()Z")) { int obiect_referință = 빼기(2); if (화면객체(obiect_referință)) 넣기(힙[obiect_referință + 9], 1); return; }
        eroare_VALUE("unsupported Swing method (native subset)");
    }
    static void 사건실행(int țintă_adresa, int 사건번호, boolean Română) {
        if (țintă_adresa < 1 || 힙[țintă_adresa] < 32) { eroare_VALUE("Java event listener required"); return; }
        int Fișier_INDEX = nume_metodă(힙[țintă_adresa] - 32, 사건번호 == 0 ? (Română ? "Execută" : "run") : (Română ? "primi_Acțiune" : "actionPerformed"), 사건번호 == 0 ? "()V" : (Română ? "(LRomână/propriu/Acțiune_înștiințare;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (Fișier_INDEX < 0) { eroare_VALUE("event callback missing"); return; }
        curent_fir = 0; fir_COUNT = 1; cadru_INDEX = 0; fir_Stare[0] = 1; cadru_Teanc[0] = 0; cadru_blocare[0] = 틀초기화[0] = 0; schimba_cerere = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 128; Loop_INDEX++) { local_VALUE[Loop_INDEX] = local_Tip[Loop_INDEX] = 0; }
        cadru_metodă[0] = Fișier_INDEX; cadru_poziție[0] = metodă_buta[Fișier_INDEX]; local_VALUE[0] = țintă_adresa; local_Tip[0] = 2;
        if (사건번호 != 0) { local_VALUE[1] = 사건번호; local_Tip[1] = 2; }
        사건중 = true; executa_comandă(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!eroare) {
            if (나중수 > 0) { int țintă_adresa = 나중실행[0], Română = 나중한국어[0]; for (int Loop_INDEX = 1; Loop_INDEX < 나중수; Loop_INDEX++) { 나중실행[Loop_INDEX - 1] = 나중실행[Loop_INDEX]; 나중한국어[Loop_INDEX - 1] = 나중한국어[Loop_INDEX]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(țintă_adresa, 0, Română != 0); continue; }
            if (utilizator.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = utilizator.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { eroare_VALUE("GUI event I/O failed"); return; }
            int cont_VALUE = 사건번호 & 65535; if (cont_VALUE < 1 || cont_VALUE > 32) continue; int obiect_referință = 화면참조[cont_VALUE - 1]; if (obiect_referință == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[obiect_referință + 10] != 0) 힙[obiect_referință + 9] = 0;
                if (힙[obiect_referință + 10] == 3) for (int Loop_INDEX = 0; Loop_INDEX < 32; Loop_INDEX++) if (화면참조[Loop_INDEX] != 0 && 힙[화면참조[Loop_INDEX]] == 24) utilizator.화면연결(4, Loop_INDEX + 1, 0, 0, 0, 0);
            } else if (힙[obiect_referință + 4] != 0) {
                int 안내참조 = aloca_Stocare(29, 2); if (eroare) return; 힙[안내참조 + 2] = obiect_referință; 힙[안내참조 + 3] = 힙[obiect_referință + 12]; 힙참조[안내참조 + 2] = 1; 사건실행(힙[obiect_referință + 4], 안내참조, 힙[obiect_referință + 12] != 0);
            }
        }
    }
    public static int Pornește() {
        if (utilizator.인수개수() == 1 && 자바도구.같음(utilizator.Argumente(0), "-version")) {
            utilizator.Scriere("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (utilizator.인수개수() < 1) { utilizator.Scriere("Usage: java CLASS [ARGS]\n"); return 2; }
        intrare_Clasă_Definiție = încărca_Clasă_Definiție(gazdă_caracter(utilizator.Argumente(0))); if (eroare || intrare_Clasă_Definiție < 0) return 1;
        int intrare_p_VALUE = nume_metodă(intrare_Clasă_Definiție, "Pornește", "()V");
        boolean 한국어진입 = intrare_p_VALUE >= 0 && (metodă_acces[intrare_p_VALUE] & 9) == 9;
        if (!한국어진입) intrare_p_VALUE = nume_metodă(intrare_Clasă_Definiție, "main", "([Ljava/lang/String;)V");
        if (intrare_p_VALUE < 0 || (metodă_acces[intrare_p_VALUE] & 9) != 9) eroare_VALUE("public static void Pornește() or main(String[] args) required");
        if (eroare) return 1;
        int Argumente = aloca_Stocare(3, utilizator.인수개수() - 1); element_vector[Argumente] = -1;
        for (int 수 = 1; 수 < utilizator.인수개수() && !eroare; 수++) 힙[Argumente + 1 + 수] = gazdă_caracter(utilizator.Argumente(수));
        cadru_INDEX = 0; cadru_metodă[0] = intrare_p_VALUE; cadru_poziție[0] = metodă_buta[intrare_p_VALUE]; local_VALUE[0] = 한국어진입 ? 0 : Argumente; local_Tip[0] = 한국어진입 ? 0 : 2;
        fir_Stare[0] = 1; fir_obiect[0] = aloca_Stocare(13, 2);
        executa_comandă(); if (!eroare) 화면사건들(); return eroare ? 1 : 0;
    }
}
