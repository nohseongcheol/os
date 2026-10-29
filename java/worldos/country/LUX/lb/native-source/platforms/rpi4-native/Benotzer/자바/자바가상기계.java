// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Fichier/스택/Referenzen/Branche 경계를 ausféieren_Befeel 중 검사한다. */
public final class 자바가상기계 {
    static int[] Fichier = new int[16 * 16384], 임시파일 = new int[16384], Fichier_Numm_SMS = new int[512];
    static int[] Konstant_Tag = new int[8192], 상가 = new int[8192], Konstant_SECOND_VALUE = new int[8192], Zeechefolleg_Referenzen = new int[8192];
    static int[] Method_Numm_SMS = new int[512], Method_TYPE = new int[512], Method_Zougrëff = new int[512], Method_Besëtzer = new int[512];
    static int[] Method_Start = new int[512], Method_bëennegen = new int[512], Method_Stapel = new int[512], 함수지역 = new int[512];
    static int[] Method_Argument_COUNT = new int[512], Method_Argument_TYPE = new int[8192], 함수반환 = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] lokal_VALUE = new int[16384], lokal_TYPE = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] Rumm_Method = new int[128], Rumm_positionéieren = new int[128], Rumm_Stapel = new int[128], Rumm_Instruktioun = new int[128], initialiséieren_Rumm = new int[128];
    static int[] Klass_Definitioun_Numm = new int[16], Klass_Definitioun_d_Gréisst_veränneren = new int[16], 종부모 = new int[16], Klass_Definitioun_Status = new int[16], Klass_Slot_COUNT = new int[16], initialiséieren_Klass_Definitioun = new int[16];
    static int[] Klass_Interface = new int[16 * 16], Klass_Interface_COUNT = new int[16];
    static int[] Slot_Numm = new int[512], Slot_TYPE = new int[512], Slot_Besëtzer = new int[512], Slot_Autorisatiounen = new int[512], Slot_positionéieren = new int[512], Slot_Daten = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], ARRAY_Element = new int[32768], Store_Ganzzuel = new int[256];
    static int d_Gréisst_veränneren, 읽기위치, Method_COUNT, Klass_Numm, Rumm_INDEX = -1, 힙끝 = 1, 반환형;
    static int Klass_Definitioun_COUNT, Slot_COUNT, 잡기수, 현재읽는종, 던진객체, 잠시수, Bildschierm_COUNT, Sammlung_COUNT;
    static int 현재가닥, Thread_COUNT = 1, Agab_Klass_Definitioun;
    static int[] Thread_Rumm = new int[4], Thread_Status = new int[4], Thread_Objet = new int[4], Thread_Zil = new int[4], 가닥대기 = new int[4];
    static boolean Feeler, 바꿈요청;
    static int[] 잠금주인 = new int[32768], 잠금깊이 = new int[32768], 틀잠금 = new int[128], 종잠금 = new int[16], Klass_Thread = new int[16];

    static void Feeler_VALUE(String Word_SMS) {
        if (Feeler) return;
        int Kategorie_CODE = 0;
        if (자바도구.같음(Word_SMS, "ArithmeticException: / by zero")) Kategorie_CODE = 4;
        if (자바도구.같음(Word_SMS, "NullPointerException") || 자바도구.같음(Word_SMS, "null or invalid array")) Kategorie_CODE = 5;
        if (자바도구.같음(Word_SMS, "ArrayIndexOutOfBoundsException")) Kategorie_CODE = 7;
        if (자바도구.같음(Word_SMS, "StringIndexOutOfBoundsException")) Kategorie_CODE = 8;
        if (자바도구.같음(Word_SMS, "NumberFormatException")) Kategorie_CODE = 10;
        if (자바도구.같음(Word_SMS, "FileNotFoundException: file open failed")) Kategorie_CODE = 12;
        if (자바도구.같음(Word_SMS, "IOException: stream closed") || 자바도구.같음(Word_SMS, "IOException: read failed") || 자바도구.같음(Word_SMS, "IOException: write failed")) Kategorie_CODE = 11;
        if (자바도구.같음(Word_SMS, "ClassCastException")) Kategorie_CODE = 14;
        if (자바도구.같음(Word_SMS, "NegativeArraySizeException")) Kategorie_CODE = 15;
        if (Kategorie_CODE != 0 && Rumm_INDEX >= 0) { 예외던짐(Kategorie_CODE, Word_SMS); return; }
        Benotzer.schreiwen("JVM error: "); Benotzer.schreiwen(Word_SMS); Benotzer.schreiwen_Zeechen_VALUE(10); Feeler = true;
    }
    static boolean Clip(int Laf, int Längt_VALUE) {
        if (Laf < 0 || Laf >= Fichier.length || Längt_VALUE < 0) return false;
        int Klass_Definitioun = Laf / 16384;
        return Laf % 16384 <= Klass_Definitioun_d_Gréisst_veränneren[Klass_Definitioun] && Längt_VALUE <= Klass_Definitioun_d_Gréisst_veränneren[Klass_Definitioun] - Laf % 16384;
    }
    static int Byte_VALUE() {
        if (!Clip(읽기위치, 1)) { Feeler_VALUE("truncated class file"); return 0; }
        return Fichier[읽기위치++];
    }
    static int 짧은수() { return Byte_VALUE() << 8 | Byte_VALUE(); }
    static int Ganzzuel() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int Längt_VALUE) { if (!Clip(읽기위치, Längt_VALUE)) Feeler_VALUE("invalid attribute size"); else 읽기위치 += Längt_VALUE; }
    static boolean Scheck_Konstant(int 수, int 종류) {
        if (수 <= 0 || 수 >= Konstant_Tag.length || Konstant_Tag[수] != 종류) { Feeler_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Laf, int Längt_VALUE, String Word_SMS) {
        if (!Clip(Laf, Längt_VALUE)) return false;
        int 읽는자리 = Laf, 끝 = Laf + Längt_VALUE;
        for (int Loop_INDEX = 0; Loop_INDEX < Word_SMS.length(); Loop_INDEX++) {
            int Zeechecode = Word_SMS.charAt(Loop_INDEX);
            if (Zeechecode > 0 && Zeechecode < 128) { if (읽는자리 >= 끝 || Fichier[읽는자리++] != Zeechecode) return false; }
            else if (Zeechecode < 2048) {
                if (읽는자리 + 2 > 끝 || Fichier[읽는자리++] != (192 | (Zeechecode >> 6)) || Fichier[읽는자리++] != (128 | (Zeechecode & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Fichier[읽는자리++] != (224 | (Zeechecode >> 12)) || Fichier[읽는자리++] != (128 | ((Zeechecode >> 6) & 63)) || Fichier[읽는자리++] != (128 | (Zeechecode & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean Word_SMS(int Konstant_VALUE, String Word_SMS) { return Scheck_Konstant(Konstant_VALUE, 1) && 구간(상가[Konstant_VALUE], Konstant_SECOND_VALUE[Konstant_VALUE], Word_SMS); }
    static boolean 같은말(int 가, int 나) {
        if (!Scheck_Konstant(가, 1) || !Scheck_Konstant(나, 1) || Konstant_SECOND_VALUE[가] != Konstant_SECOND_VALUE[나]) return false;
        for (int 수 = 0; 수 < Konstant_SECOND_VALUE[가]; 수++) if (Fichier[상가[가] + 수] != Fichier[상가[나] + 수]) return false;
        return true;
    }
    static int Klass_Numm_SMS(int 수) { return Scheck_Konstant(수, 7) && Scheck_Konstant(상가[수], 1) ? 상가[수] : 0; }
    static int Referenzen_Numm(int 수) { return Scheck_Konstant(수, 12) && Scheck_Konstant(상가[수], 1) ? 상가[수] : 0; }
    static int Referenzen_TYPE(int 수) { return Scheck_Konstant(수, 12) && Scheck_Konstant(Konstant_SECOND_VALUE[수], 1) ? Konstant_SECOND_VALUE[수] : 0; }
    static int 서술형(int 끝, boolean eidel_TYPE) {
        if (읽기위치 >= 끝) { Feeler_VALUE("invalid descriptor"); return 0; }
        int VALUE = Byte_VALUE();
        if (VALUE == 'V' && eidel_TYPE) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int Laf = 읽기위치;
            while (읽기위치 < 끝 && Fichier[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Laf) Feeler_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        Feeler_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int FUNCTION_VALUE) {
        int 이전 = 읽기위치, 수 = Method_TYPE[FUNCTION_VALUE];
        if (!Scheck_Konstant(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + Konstant_SECOND_VALUE[수];
        if (Byte_VALUE() != '(') Feeler_VALUE("invalid method descriptor");
        int Element_COUNT = 0;
        while (!Feeler && 읽기위치 < 끝 && Fichier[읽기위치] != ')') {
            if (Element_COUNT == 16) { Feeler_VALUE("too many method arguments"); break; }
            Method_Argument_TYPE[FUNCTION_VALUE * 16 + Element_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || Byte_VALUE() != ')') Feeler_VALUE("invalid method descriptor");
        함수반환[FUNCTION_VALUE] = 서술형(끝, true); Method_Argument_COUNT[FUNCTION_VALUE] = Element_COUNT;
        if (읽기위치 != 끝) Feeler_VALUE("invalid method descriptor");
        읽기위치 = 이전;
    }
    static int 상번호() { int VALUE = 짧은수(); return VALUE == 0 ? 0 : 현재읽는종 * 512 + VALUE; }
    static int 명상수() { return Method_Besëtzer[Rumm_Method[Rumm_INDEX]] * 512 + 명짧(); }
    static void 속성건너() {
        int Element_COUNT = 짧은수();
        for (int 수 = 0; 수 < Element_COUNT && !Feeler; 수++) { Scheck_Konstant(상번호(), 1); 건너(Ganzzuel()); }
    }
    static int Befeel_Längt(int VALUE) {
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
    static int positionéieren_Ganzzuel(int 읽는자리) {
        if (!Clip(읽는자리, 4)) { Feeler_VALUE("truncated bytecode operand"); return 0; }
        return Fichier[읽는자리] << 24 | Fichier[읽는자리 + 1] << 16 | Fichier[읽는자리 + 2] << 8 | Fichier[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Laf, int 끝) {
        int VALUE = Fichier[읽는자리], Längt_VALUE = Befeel_Längt(VALUE);
        if (VALUE == 170 || VALUE == 171) {
            int BASE_positionéieren = 읽는자리 + 1;
            while ((BASE_positionéieren - Laf) % 4 != 0) BASE_positionéieren++;
            if (끝 - BASE_positionéieren < (VALUE == 170 ? 12 : 8)) return 0;
            int Agab_COUNT = VALUE == 170 ? positionéieren_Ganzzuel(BASE_positionéieren + 8) - positionéieren_Ganzzuel(BASE_positionéieren + 4) + 1 : positionéieren_Ganzzuel(BASE_positionéieren + 4);
            if (Agab_COUNT < 0 || Agab_COUNT > 2048) return 0;
            Längt_VALUE = BASE_positionéieren - 읽는자리 + (VALUE == 170 ? 12 + 4 * Agab_COUNT : 8 + 8 * Agab_COUNT);
        }
        if (VALUE == 196 && 읽는자리 + 1 < 끝) {
            int Word_Daten = Fichier[읽는자리 + 1]; Längt_VALUE = Word_Daten == 132 ? 6 : (Word_Daten == 21 || Word_Daten == 25 || Word_Daten == 54 || Word_Daten == 58) ? 4 : 0;
        }
        return Längt_VALUE > 0 && Längt_VALUE <= 끝 - 읽는자리 ? Längt_VALUE : 0;
    }
    static void Scheck_Zil_VALUE(int Zil_VALUE, int FUNCTION_VALUE) {
        if (Zil_VALUE < Method_Start[FUNCTION_VALUE] || Zil_VALUE >= Method_bëennegen[FUNCTION_VALUE] || 경계[Zil_VALUE] != FUNCTION_VALUE + 1) Feeler_VALUE("invalid branch target");
    }
    static void 클래스읽기(int Klass_Definitioun) {
        현재읽는종 = Klass_Definitioun; 읽기위치 = Klass_Definitioun * 16384; d_Gréisst_veränneren = 읽기위치 + Klass_Definitioun_d_Gréisst_veränneren[Klass_Definitioun];
        if (Ganzzuel() != 0xcafebabe) { Feeler_VALUE("not a class file"); return; }
        int 부판 = 짧은수(), Versioun_VALUE = 짧은수();
        if (Versioun_VALUE < 45 || Versioun_VALUE > 52 || 부판 != 0) { Feeler_VALUE("supported class versions: 45..52, minor 0"); return; }
        int Konstant_COUNT = 짧은수(), BASE_positionéieren = Klass_Definitioun * 512;
        if (Konstant_COUNT < 1 || Konstant_COUNT > 512) { Feeler_VALUE("constant pool limit (511)"); return; }
        for (int Agab_COUNT = 1; Agab_COUNT < Konstant_COUNT && !Feeler; Agab_COUNT++) {
            int 수 = BASE_positionéieren + Agab_COUNT, 종류 = Byte_VALUE(); Konstant_Tag[수] = 종류;
            if (종류 == 1) { Konstant_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(Konstant_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = Ganzzuel();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); Konstant_SECOND_VALUE[수] = 상번호(); }
            else Feeler_VALUE("unsupported constant type");
        }
        int Geneemegung_VALUE = 짧은수();
        if ((Geneemegung_VALUE & (0x2000 | 0x4000)) != 0) Feeler_VALUE("annotation/enum class unsupported");
        Klass_Definitioun_Numm[Klass_Definitioun] = Klass_Numm_SMS(상번호());
        종부모[Klass_Definitioun] = Klass_Numm_SMS(상번호());
        int Interface_COUNT = 짧은수(); if (Interface_COUNT > 16) { Feeler_VALUE("interface count limit"); return; }
        Klass_Interface_COUNT[Klass_Definitioun] = Interface_COUNT;
        for (int Loop_INDEX = 0; Loop_INDEX < Interface_COUNT; Loop_INDEX++) Klass_Interface[Klass_Definitioun * 16 + Loop_INDEX] = Klass_Numm_SMS(상번호());
        int Feld_COUNT = 짧은수();
        if (Feld_COUNT > 512 - Slot_COUNT) { Feeler_VALUE("field count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Feld_COUNT && !Feeler; Loop_INDEX++) {
            int Fichier_INDEX = Slot_COUNT++; Slot_Besëtzer[Fichier_INDEX] = Klass_Definitioun; Slot_Autorisatiounen[Fichier_INDEX] = 짧은수(); Slot_Numm[Fichier_INDEX] = 상번호(); Slot_TYPE[Fichier_INDEX] = 상번호();
            Scheck_Konstant(Slot_Numm[Fichier_INDEX], 1); Scheck_Konstant(Slot_TYPE[Fichier_INDEX], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[Slot_TYPE[Fichier_INDEX]]; int Kategorie_CODE = 서술형(읽기위치 + Konstant_SECOND_VALUE[Slot_TYPE[Fichier_INDEX]], false); 읽기위치 = 보존값;
            if ((Slot_Autorisatiounen[Fichier_INDEX] & 8) == 0) Slot_positionéieren[Fichier_INDEX] = Klass_Slot_COUNT[Klass_Definitioun]++;
            int Attribut_Daten = 짧은수();
            for (int intern_Verknëppung_positionéieren = 0; intern_Verknëppung_positionéieren < Attribut_Daten && !Feeler; intern_Verknëppung_positionéieren++) {
                int Numm_Konstant = 상번호(), 유효길이 = Ganzzuel();
                if (Word_SMS(Numm_Konstant, "ConstantValue") && 유효길이 == 2) {
                    int Daten_VALUE = 상번호();
                    if (Kategorie_CODE == 1 && Scheck_Konstant(Daten_VALUE, 3)) Slot_Daten[Fichier_INDEX] = 상가[Daten_VALUE];
                    else if (Kategorie_CODE == 2 && Scheck_Konstant(Daten_VALUE, 8)) Slot_Daten[Fichier_INDEX] = Konstant_SMS(상가[Daten_VALUE]);
                } else 건너(유효길이);
            }
        }
        int Element_COUNT = 짧은수();
        if (Element_COUNT > 512 - Method_COUNT) { Feeler_VALUE("method count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Element_COUNT && !Feeler; Loop_INDEX++) {
            int 수 = Method_COUNT++; Method_Besëtzer[수] = Klass_Definitioun;
            Method_Zougrëff[수] = 짧은수(); Method_Numm_SMS[수] = 상번호(); Method_TYPE[수] = 상번호();
            Scheck_Konstant(Method_Numm_SMS[수], 1); 서술읽기(수);
            if ((Method_Zougrëff[수] & 8) == 0) {
                if (Method_Argument_COUNT[수] == 16) { Feeler_VALUE("too many instance method arguments"); return; }
                for (int 비교자리 = Method_Argument_COUNT[수]; 비교자리 > 0; 비교자리--) Method_Argument_TYPE[수 * 16 + 비교자리] = Method_Argument_TYPE[수 * 16 + 비교자리 - 1];
                Method_Argument_TYPE[수 * 16] = 2; Method_Argument_COUNT[수]++;
            }
            if ((Method_Zougrëff[수] & 0x100) != 0) Feeler_VALUE("user native method unsupported");
            if (Word_SMS(Method_Numm_SMS[수], "<clinit>")) initialiséieren_Klass_Definitioun[Klass_Definitioun] = 수 + 1;
            for (int 앞 = 0; 앞 < 수; 앞++) if (Method_Besëtzer[앞] == Klass_Definitioun && 같은말(Method_Numm_SMS[앞], Method_Numm_SMS[수]) && 같은말(Method_TYPE[앞], Method_TYPE[수])) Feeler_VALUE("duplicate method");
            int Attribut_COUNT = 짧은수();
            for (int Attribut_VALUE = 0; Attribut_VALUE < Attribut_COUNT && !Feeler; Attribut_VALUE++) {
                int Numm = 상번호(), Längt_VALUE = Ganzzuel(), Laf = 읽기위치;
                if (!Clip(Laf, Längt_VALUE)) { Feeler_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Numm, "Code")) {
                    if (Method_Start[수] != 0) Feeler_VALUE("duplicate Code attribute");
                    Method_Stapel[수] = 짧은수(); 함수지역[수] = 짧은수(); int CODE_Längt = Ganzzuel();
                    if (Method_Stapel[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < Method_Argument_COUNT[수]
                        || CODE_Längt < 1 || CODE_Längt > 8192) Feeler_VALUE("method memory limits exceeded");
                    Method_Start[수] = 읽기위치; 건너(CODE_Längt); Method_bëennegen[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { Feeler_VALUE("exception table limit"); return; }
                    for (int intern_Verknëppung_positionéieren = 0; intern_Verknëppung_positionéieren < 잡는수; intern_Verknëppung_positionéieren++) {
                        int Feeler_Referenzen = 잡기수++; 잡기함수[Feeler_Referenzen] = 수;
                        잡기시작[Feeler_Referenzen] = Method_Start[수] + 짧은수(); 잡기끝[Feeler_Referenzen] = Method_Start[수] + 짧은수();
                        잡기위치[Feeler_Referenzen] = Method_Start[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[Feeler_Referenzen] = 부호값 == 0 ? 0 : Klass_Numm_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != Laf + Längt_VALUE) Feeler_VALUE("Code attribute size mismatch");
                } else 건너(Längt_VALUE);
            }
            if ((Method_Zougrëff[수] & 0x400) != 0) continue;
            if (Method_Start[수] == 0) Feeler_VALUE("missing Code attribute");
            int Slot_Agab = Method_Start[수];
            while (Slot_Agab < Method_bëennegen[수] && !Feeler) {
                int Längt_VALUE = 길이읽기(Slot_Agab, Method_Start[수], Method_bëennegen[수]);
                if (Längt_VALUE == 0) { Feeler_VALUE("unsupported or truncated bytecode"); break; }
                경계[Slot_Agab] = 수 + 1; Slot_Agab += Längt_VALUE;
            }
            Slot_Agab = Method_Start[수];
            while (Slot_Agab < Method_bëennegen[수] && !Feeler) {
                int VALUE = Fichier[Slot_Agab];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) Scheck_Zil_VALUE(Slot_Agab + (short)(Fichier[Slot_Agab + 1] << 8 | Fichier[Slot_Agab + 2]), 수);
                if (VALUE == 200) Scheck_Zil_VALUE(Slot_Agab + positionéieren_Ganzzuel(Slot_Agab + 1), 수);
                if (VALUE == 170 || VALUE == 171) {
                    int 읽는자리 = Slot_Agab + 1; while ((읽는자리 - Method_Start[수]) % 4 != 0) 읽는자리++;
                    Scheck_Zil_VALUE(Slot_Agab + positionéieren_Ganzzuel(읽는자리), 수);
                    int Agab_COUNT = VALUE == 170 ? positionéieren_Ganzzuel(읽는자리 + 8) - positionéieren_Ganzzuel(읽는자리 + 4) + 1 : positionéieren_Ganzzuel(읽는자리 + 4);
                    읽는자리 += VALUE == 170 ? 12 : 8;
                    for (int intern_Verknëppung_positionéieren = 0; intern_Verknëppung_positionéieren < Agab_COUNT; intern_Verknëppung_positionéieren++) Scheck_Zil_VALUE(Slot_Agab + positionéieren_Ganzzuel(읽는자리 + intern_Verknëppung_positionéieren * (VALUE == 170 ? 4 : 8) + (VALUE == 170 ? 0 : 4)), 수);
                }
                Slot_Agab += 길이읽기(Slot_Agab, Method_Start[수], Method_bëennegen[수]);
            }
            for (int intern_Verknëppung_positionéieren = 0; intern_Verknëppung_positionéieren < 잡기수; intern_Verknëppung_positionéieren++) if (잡기함수[intern_Verknëppung_positionéieren] == 수) {
                Scheck_Zil_VALUE(잡기시작[intern_Verknëppung_positionéieren], 수); Scheck_Zil_VALUE(잡기위치[intern_Verknëppung_positionéieren], 수);
                if (잡기끝[intern_Verknëppung_positionéieren] != Method_bëennegen[수]) Scheck_Zil_VALUE(잡기끝[intern_Verknëppung_positionéieren], 수);
                if (잡기시작[intern_Verknëppung_positionéieren] >= 잡기끝[intern_Verknëppung_positionéieren]) Feeler_VALUE("invalid exception range");
            }
        }
        if (!Feeler) 속성건너();
        if (읽기위치 != d_Gréisst_veränneren) Feeler_VALUE("extra class file data");
    }
    static int zouweisen_Späicher(int 종류, int Längt_VALUE) { return 새기억(종류, Längt_VALUE); }
    static boolean Objet_VALUE(int Referenzen, int 종류) {
        if (!객체유효(Referenzen)) return false;
        if (힙[Referenzen] != 종류) { Feeler_VALUE("object type mismatch"); return false; }
        return true;
    }
    static int Konstant_SMS(int INDEX) {
        if (!Scheck_Konstant(INDEX, 1)) return 0;
        if (Zeechefolleg_Referenzen[INDEX] != 0) return Zeechefolleg_Referenzen[INDEX];
        int Referenzen = zouweisen_Späicher(1, Konstant_SECOND_VALUE[INDEX]); if (Feeler) return 0;
        int 끝 = 상가[INDEX] + Konstant_SECOND_VALUE[INDEX], 수 = 상가[INDEX], Längt_VALUE = 0;
        while (수 < 끝 && !Feeler) {
            int VALUE = Fichier[수++];
            if (VALUE == 0) Feeler_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && 수 < 끝) {
                int Weider_Element = Fichier[수++];
                if ((Weider_Element & 192) != 128) Feeler_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | Weider_Element & 63;
                if (VALUE != 0 && VALUE < 128) Feeler_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && 수 + 1 < 끝) {
                int 가 = Fichier[수++], 나 = Fichier[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) Feeler_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (VALUE < 2048) Feeler_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) Feeler_VALUE("invalid modified UTF-8");
            힙[Referenzen + 2 + Längt_VALUE++] = VALUE;
        }
        힙[Referenzen + 1] = Längt_VALUE; Zeechefolleg_Referenzen[INDEX] = Referenzen; return Referenzen;
    }
    static int Host_Zeechen(String VALUE) {
        int Referenzen = zouweisen_Späicher(1, VALUE.length()); if (Feeler) return 0;
        for (int 수 = 0; 수 < VALUE.length(); 수++) 힙[Referenzen + 2 + 수] = VALUE.charAt(수);
        return Referenzen;
    }
    static void schreiwen_SMS(int Referenzen) {
        if (Referenzen == 0) { Benotzer.schreiwen("null"); return; }
        if (!Objet_VALUE(Referenzen, 1)) return;
        for (int 수 = 0; 수 < 힙[Referenzen + 1]; 수++) Benotzer.schreiwen_Zeechen_VALUE(힙[Referenzen + 2 + 수]);
    }
    static int Ziffer_Zeechen(int VALUE) {
        int Referenzen = zouweisen_Späicher(1, 11); if (Feeler) return 0;
        int Längt_VALUE = 0;
        if (VALUE < 0) 힙[Referenzen + 2 + Längt_VALUE++] = '-'; else VALUE = -VALUE;
        int positionéieren_INDEX = 1000000000; boolean Laf = false;
        while (positionéieren_INDEX != 0) {
            int 수 = -(VALUE / positionéieren_INDEX);
            if (수 != 0 || Laf || positionéieren_INDEX == 1) { 힙[Referenzen + 2 + Längt_VALUE++] = '0' + 수; Laf = true; }
            VALUE %= positionéieren_INDEX; positionéieren_INDEX /= 10;
        }
        힙[Referenzen + 1] = Längt_VALUE; return Referenzen;
    }
    static int 정수해독(int Referenzen) {
        if (!Objet_VALUE(Referenzen, 1)) return 0;
        int Längt_VALUE = 힙[Referenzen + 1], 수 = 0, VALUE = 0; boolean 음수 = false;
        if (Längt_VALUE > 0 && (힙[Referenzen + 2] == '-' || 힙[Referenzen + 2] == '+')) { 음수 = 힙[Referenzen + 2] == '-'; 수++; }
        if (수 == Längt_VALUE) Feeler_VALUE("NumberFormatException");
        for (; 수 < Längt_VALUE && !Feeler; 수++) {
            int Ziffer_VALUE = 힙[Referenzen + 2 + 수] - '0';
            if (Ziffer_VALUE < 0 || Ziffer_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && Ziffer_VALUE > (음수 ? 8 : 7)) Feeler_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - Ziffer_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int TYPE_VALUE) {
        if (Feeler) return;
        if (Rumm_INDEX < 0 || Rumm_Stapel[Rumm_INDEX] >= Method_Stapel[Rumm_Method[Rumm_INDEX]]) { Feeler_VALUE("operand stack overflow"); return; }
        int Slot_Agab = Rumm_INDEX * 128 + Rumm_Stapel[Rumm_INDEX]++; 스택값[Slot_Agab] = VALUE; 스택형[Slot_Agab] = TYPE_VALUE;
    }
    static int 빼기(int TYPE_VALUE) {
        if (Feeler) return 0;
        if (Rumm_INDEX < 0 || Rumm_Stapel[Rumm_INDEX] < 1) { Feeler_VALUE("operand stack underflow"); return 0; }
        int Slot_Agab = Rumm_INDEX * 128 + --Rumm_Stapel[Rumm_INDEX]; 반환형 = 스택형[Slot_Agab];
        if (TYPE_VALUE != 0 && 반환형 != TYPE_VALUE) Feeler_VALUE("operand type mismatch");
        if (반환형 == 2) schützen_VALUE(스택값[Slot_Agab]);
        return 스택값[Slot_Agab];
    }
    static void 지역읽기(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[Rumm_Method[Rumm_INDEX]] || INDEX < 0 || lokal_TYPE[Rumm_INDEX * 128 + INDEX] != TYPE_VALUE) { Feeler_VALUE("invalid or uninitialized local"); return; }
        넣기(lokal_VALUE[Rumm_INDEX * 128 + INDEX], TYPE_VALUE);
    }
    static void schreiwen_lokal(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[Rumm_Method[Rumm_INDEX]] || INDEX < 0) { Feeler_VALUE("local index out of range"); return; }
        int VALUE = 빼기(TYPE_VALUE); lokal_VALUE[Rumm_INDEX * 128 + INDEX] = VALUE; lokal_TYPE[Rumm_INDEX * 128 + INDEX] = TYPE_VALUE;
    }
    static int 명바() {
        int positionéieren = Rumm_positionéieren[Rumm_INDEX];
        if (positionéieren < Method_Start[Rumm_Method[Rumm_INDEX]] || positionéieren >= Method_bëennegen[Rumm_Method[Rumm_INDEX]]) { Feeler_VALUE("instruction pointer out of range"); return 0; }
        Rumm_positionéieren[Rumm_INDEX]++; return Fichier[positionéieren];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void verréckelen_VALUE(int positionéieren) {
        int FUNCTION_VALUE = Rumm_Method[Rumm_INDEX];
        if (positionéieren < Method_Start[FUNCTION_VALUE] || positionéieren >= Method_bëennegen[FUNCTION_VALUE] || 경계[positionéieren] != FUNCTION_VALUE + 1) Feeler_VALUE("invalid branch target");
        else Rumm_positionéieren[Rumm_INDEX] = positionéieren;
    }
    static void 호출(int FUNCTION_VALUE) {
        if (Rumm_INDEX % 32 == 31) { Feeler_VALUE("call stack limit (32)"); return; }
        int Weider_Element = Rumm_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) lokal_TYPE[Weider_Element * 128 + 수] = 0;
        for (int 수 = Method_Argument_COUNT[FUNCTION_VALUE] - 1; 수 >= 0; 수--) {
            lokal_VALUE[Weider_Element * 128 + 수] = 빼기(Method_Argument_TYPE[FUNCTION_VALUE * 16 + 수]); lokal_TYPE[Weider_Element * 128 + 수] = Method_Argument_TYPE[FUNCTION_VALUE * 16 + 수];
        }
        if (Feeler) return;
        Rumm_INDEX = Weider_Element; initialiséieren_Rumm[Rumm_INDEX] = 0; Rumm_Method[Rumm_INDEX] = FUNCTION_VALUE; Rumm_positionéieren[Rumm_INDEX] = Method_Start[FUNCTION_VALUE]; Rumm_Stapel[Rumm_INDEX] = 0;
    }
    static void 반환(int TYPE_VALUE) {
        if (TYPE_VALUE != 함수반환[Rumm_Method[Rumm_INDEX]]) { Feeler_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        if (initialiséieren_Rumm[Rumm_INDEX] != 0) Klass_Definitioun_Status[initialiséieren_Rumm[Rumm_INDEX] - 1] = 2;
        if (틀잠금[Rumm_INDEX] != 0) { 잠금풀기(틀잠금[Rumm_INDEX]); 틀잠금[Rumm_INDEX] = 0; }
        Rumm_INDEX--; if (Rumm_INDEX >= 현재가닥 * 32 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
    }
    static int[] Stream_Fichier_Numm = new int[64];
    static void Fichier_Stream_CALL(int Besëtzer_VALUE, int Numm, int Format_VALUE, int Befeel) {
        boolean 출력 = Word_SMS(Besëtzer_VALUE, "java/io/FileOutputStream");
        int 종류 = 출력 ? 6 : 5;
        if (Befeel == 183 && Word_SMS(Numm, "<init>")) {
            boolean 이어 = false;
            if (출력 && Word_SMS(Format_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(Format_VALUE, "(Ljava/lang/String;)V")) { Feeler_VALUE("unsupported file stream constructor"); return; }
            int Fichier_Agab_Numm = 빼기(2), Stream_VALUE = 빼기(2);
            if (!Objet_VALUE(Fichier_Agab_Numm, 1) || !Objet_VALUE(Stream_VALUE, 종류) || Feeler) return;
            if (힙[Stream_VALUE + 3] != 0) { Feeler_VALUE("file stream already initialized"); return; }
            int Längt_VALUE = 힙[Fichier_Agab_Numm + 1];
            if (Längt_VALUE < 1 || Längt_VALUE > 63) { Feeler_VALUE("invalid file name length"); return; }
            for (int Slot_Agab = 0; Slot_Agab < Längt_VALUE; Slot_Agab++) {
                int VALUE = 힙[Fichier_Agab_Numm + 2 + Slot_Agab];
                if (VALUE < 1) { Feeler_VALUE("invalid file stream path"); return; }
                Stream_Fichier_Numm[Slot_Agab] = VALUE;
            }
            Stream_Fichier_Numm[Längt_VALUE] = 0;
            int 서술자 = Benotzer.파일서술자열기(Stream_Fichier_Numm, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { Feeler_VALUE("FileNotFoundException: file open failed"); return; }
            힙[Stream_VALUE + 2] = 서술자; 힙[Stream_VALUE + 3] = 1;
            return;
        }
        if (Befeel != 182) { Feeler_VALUE("invalid file stream invocation"); return; }
        if ((출력 && Word_SMS(Numm, "write") || !출력 && Word_SMS(Numm, "read"))
            && (Word_SMS(Format_VALUE, 출력 ? "([B)V" : "([B)I") || Word_SMS(Format_VALUE, 출력 ? "([BII)V" : "([BII)I"))) {
            boolean Clip_VALUE = Word_SMS(Format_VALUE, 출력 ? "([BII)V" : "([BII)I");
            int Agab_COUNT = Clip_VALUE ? 빼기(1) : 0, 시작점 = Clip_VALUE ? 빼기(1) : 0, Daten_ARRAY = 빼기(2), Objet_Referenzen = 빼기(2);
            if (!Objet_VALUE(Daten_ARRAY, 20) || !Objet_VALUE(Objet_Referenzen, 종류)) return;
            if (!Clip_VALUE) Agab_COUNT = 힙[Daten_ARRAY + 1];
            if (시작점 < 0 || Agab_COUNT < 0 || 시작점 > 힙[Daten_ARRAY + 1] - Agab_COUNT) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[Objet_Referenzen + 3] == 0 || 힙[Objet_Referenzen + 2] < 0) { Feeler_VALUE("IOException: stream closed"); return; }
            int 완료수 = 0;
            while (완료수 < Agab_COUNT && !Feeler) {
                int 반환값 = 출력 ? Benotzer.파일한바이트쓰기(힙[Objet_Referenzen + 2], 힙[Daten_ARRAY + 2 + 시작점 + 완료수]) : Benotzer.파일한바이트읽기(힙[Objet_Referenzen + 2]);
                if (반환값 < 0) { Feeler_VALUE(출력 ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!출력 && 반환값 == 256) break;
                if (!출력) 힙[Daten_ARRAY + 2 + 시작점 + 완료수] = (byte)반환값;
                완료수++;
            }
            if (!출력) 넣기(Agab_COUNT != 0 && 완료수 == 0 ? -1 : 완료수, 1);
            return;
        }
        if (출력 && Word_SMS(Numm, "flush") && Word_SMS(Format_VALUE, "()V")) { int Objet_Referenzen = 빼기(2); if (Objet_VALUE(Objet_Referenzen, 종류) && 힙[Objet_Referenzen + 2] < 0) Feeler_VALUE("IOException: stream closed"); return; }
        int Aktioun = -1, VALUE = 0;
        if (Word_SMS(Numm, "close") && Word_SMS(Format_VALUE, "()V")) Aktioun = 0;
        if (!출력 && Word_SMS(Numm, "read") && Word_SMS(Format_VALUE, "()I")) Aktioun = 1;
        if (출력 && Word_SMS(Numm, "write") && Word_SMS(Format_VALUE, "(I)V")) { Aktioun = 2; VALUE = 빼기(1); }
        if (Aktioun < 0) { Feeler_VALUE("unsupported file stream method"); return; }
        int Stream_VALUE = 빼기(2);
        if (!Objet_VALUE(Stream_VALUE, 종류) || Feeler) return;
        if (힙[Stream_VALUE + 3] == 0) { Feeler_VALUE("uninitialized file stream"); return; }
        int 서술자 = 힙[Stream_VALUE + 2];
        if (Aktioun == 0) {
            if (서술자 >= 0 && Benotzer.파일서술자닫기(서술자) < 0) Feeler_VALUE("IOException: close failed");
            힙[Stream_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { Feeler_VALUE("IOException: stream closed"); return; }
        if (Aktioun == 1) {
            int Mooss = Benotzer.파일한바이트읽기(서술자);
            if (Mooss < -1) Feeler_VALUE("IOException: read failed"); else 넣기(Mooss == 256 ? -1 : Mooss, 1);
        } else if (Benotzer.파일한바이트쓰기(서술자, VALUE) != 1) Feeler_VALUE("IOException: write failed");
    }
    static void CALL_Method(int INDEX, int Befeel) {
        if (INDEX <= 0 || INDEX >= Konstant_Tag.length || (Konstant_Tag[INDEX] != 10 && Konstant_Tag[INDEX] != 11)) { Feeler_VALUE("invalid method reference"); return; }
        int Besëtzer_VALUE = Klass_Numm_SMS(상가[INDEX]), Numm = Referenzen_Numm(Konstant_SECOND_VALUE[INDEX]), Format_VALUE = Referenzen_TYPE(Konstant_SECOND_VALUE[INDEX]);
        if (Feeler) return;
        if (기본호출(Besëtzer_VALUE, Numm, Format_VALUE, Befeel)) return;
        if (Word_SMS(Besëtzer_VALUE, "java/io/FileInputStream") || Word_SMS(Besëtzer_VALUE, "java/io/FileOutputStream")) {
            Fichier_Stream_CALL(Besëtzer_VALUE, Numm, Format_VALUE, Befeel); return;
        }
        if (Befeel == 184 && Word_SMS(Besëtzer_VALUE, "java/lang/Integer") && Word_SMS(Numm, "parseInt") && Word_SMS(Format_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Befeel == 182 && Word_SMS(Besëtzer_VALUE, "java/io/PrintStream") && (Word_SMS(Numm, "println") || Word_SMS(Numm, "print"))) {
            int TYPE_VALUE = 0, VALUE = 0;
            if (Word_SMS(Format_VALUE, "(I)V")) { TYPE_VALUE = 1; VALUE = 빼기(1); }
            else if (Word_SMS(Format_VALUE, "(Z)V")) { TYPE_VALUE = 2; VALUE = 빼기(1); }
            else if (Word_SMS(Format_VALUE, "(C)V")) { TYPE_VALUE = 3; VALUE = 빼기(1); }
            else if (Word_SMS(Format_VALUE, "(Ljava/lang/String;)V")) { TYPE_VALUE = 4; VALUE = 빼기(2); }
            else if (!Word_SMS(Format_VALUE, "()V") || !Word_SMS(Numm, "println")) Feeler_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) Feeler_VALUE("invalid PrintStream receiver");
            if (Feeler) return;
            if (TYPE_VALUE == 1) 자바도구.수쓰기(VALUE);
            if (TYPE_VALUE == 2) Benotzer.schreiwen(VALUE == 0 ? "false" : "true");
            if (TYPE_VALUE == 3) Benotzer.schreiwen_Zeechen_VALUE(VALUE & 65535);
            if (TYPE_VALUE == 4) schreiwen_SMS(VALUE);
            if (Word_SMS(Numm, "println")) Benotzer.schreiwen_Zeechen_VALUE(10);
            return;
        }
        if (Befeel == 182 && Word_SMS(Besëtzer_VALUE, "java/lang/String")) {
            if (Word_SMS(Numm, "length") && Word_SMS(Format_VALUE, "()I")) {
                int Referenzen = 빼기(2); if (Objet_VALUE(Referenzen, 1)) 넣기(힙[Referenzen + 1], 1); return;
            }
            if (Word_SMS(Numm, "charAt") && Word_SMS(Format_VALUE, "(I)C")) {
                int déifstellen_VALUE = 빼기(1), Referenzen = 빼기(2);
                if (Objet_VALUE(Referenzen, 1)) {
                    if (déifstellen_VALUE < 0 || déifstellen_VALUE >= 힙[Referenzen + 1]) Feeler_VALUE("StringIndexOutOfBoundsException"); else 넣기(힙[Referenzen + 2 + déifstellen_VALUE], 1);
                }
                return;
            }
        }
        if (Word_SMS(Besëtzer_VALUE, "java/lang/StringBuilder")) {
            if (Befeel == 183 && Word_SMS(Numm, "<init>") && Word_SMS(Format_VALUE, "()V")) { Objet_VALUE(빼기(2), 4); return; }
            if (Befeel == 182 && Word_SMS(Numm, "toString") && Word_SMS(Format_VALUE, "()Ljava/lang/String;")) {
                int Referenzen = 빼기(2); if (Objet_VALUE(Referenzen, 4)) 넣기(힙[Referenzen + 2] == 0 ? Host_Zeechen("") : 힙[Referenzen + 2], 2); return;
            }
            if (Befeel == 182 && Word_SMS(Numm, "append")) {
                int SMS = 0;
                if (Word_SMS(Format_VALUE, "(I)Ljava/lang/StringBuilder;")) SMS = Ziffer_Zeechen(빼기(1));
                else if (Word_SMS(Format_VALUE, "(Z)Ljava/lang/StringBuilder;")) SMS = Host_Zeechen(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(Format_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); SMS = zouweisen_Späicher(1, 1); if (!Feeler) 힙[SMS + 2] = VALUE & 65535;
                }
                else if (Word_SMS(Format_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { SMS = 빼기(2); if (SMS == 0) SMS = Host_Zeechen("null"); }
                else { Feeler_VALUE("unsupported StringBuilder append"); return; }
                int Referenzen = 빼기(2); if (!Objet_VALUE(Referenzen, 4) || !Objet_VALUE(SMS, 1)) return;
                int 앞 = 힙[Referenzen + 2], 앞길이 = 앞 == 0 ? 0 : 힙[앞 + 1], Zeréck_VALUE_Längt = 힙[SMS + 1];
                int 새글 = zouweisen_Späicher(1, 앞길이 + Zeréck_VALUE_Längt); if (Feeler) return;
                for (int 수 = 0; 수 < 앞길이; 수++) 힙[새글 + 2 + 수] = 힙[앞 + 2 + 수];
                for (int 수 = 0; 수 < Zeréck_VALUE_Längt; 수++) 힙[새글 + 2 + 앞길이 + 수] = 힙[SMS + 2 + 수];
                힙[Referenzen + 2] = 새글; 넣기(Referenzen, 2); return;
            }
        }
        int Klass_Definitioun = FIND_Klass_Definitioun(Besëtzer_VALUE); if (Klass_Definitioun < 0 || Feeler) return;
        int Fichier_INDEX = FIND_Method(Klass_Definitioun, Numm, Format_VALUE);
        if (Fichier_INDEX < 0) {
            for (int Zeechecode = Klass_Definitioun, Agab_COUNT = 0; Zeechecode >= 0 && Agab_COUNT < 16; Agab_COUNT++, Zeechecode = 부모종(Zeechecode))
                if (Word_SMS(종부모[Zeechecode], "java/lang/Thread")) { 가닥호출(Numm, Format_VALUE, Befeel); return; }
            Feeler_VALUE("NoSuchMethodError"); return;
        }
        if (((Method_Zougrëff[Fichier_INDEX] & 8) != 0) != (Befeel == 184)) { Feeler_VALUE("method static/instance mismatch"); return; }
        if (Befeel == 184) { if (!initialiséieren(Method_Besëtzer[Fichier_INDEX], Rumm_Instruktioun[Rumm_INDEX])) return; }
        else {
            int 읽는자리 = Rumm_Stapel[Rumm_INDEX] - Method_Argument_COUNT[Fichier_INDEX];
            if (읽는자리 < 0 || 스택형[Rumm_INDEX * 128 + 읽는자리] != 2) { Feeler_VALUE("invalid method receiver"); return; }
            int Objet_Referenzen = 스택값[Rumm_INDEX * 128 + 읽는자리];
            if (!객체유효(Objet_Referenzen)) return;
            if (힙[Objet_Referenzen] < 32 || !종포함(힙[Objet_Referenzen] - 32, Besëtzer_VALUE)) { Feeler_VALUE("method receiver type mismatch"); return; }
            if (Befeel != 183) Fichier_INDEX = FIND_Method(힙[Objet_Referenzen] - 32, Numm, Format_VALUE);
        }
        if (Fichier_INDEX < 0 || (Method_Zougrëff[Fichier_INDEX] & 0x400) != 0) { Feeler_VALUE("AbstractMethodError"); return; }
        int 잠금참조 = 0;
        if ((Method_Zougrëff[Fichier_INDEX] & 32) != 0) {
            if (Befeel == 184) { int Zeechecode = Method_Besëtzer[Fichier_INDEX]; if (종잠금[Zeechecode] == 0) 종잠금[Zeechecode] = zouweisen_Späicher(8, 0); 잠금참조 = 종잠금[Zeechecode]; }
            else 잠금참조 = 스택값[Rumm_INDEX * 128 + Rumm_Stapel[Rumm_INDEX] - Method_Argument_COUNT[Fichier_INDEX]];
            if (!잠금얻기(잠금참조)) { if (!Feeler) Rumm_positionéieren[Rumm_INDEX] = Rumm_Instruktioun[Rumm_INDEX]; return; }
        }
        호출(Fichier_INDEX); if (!Feeler) 틀잠금[Rumm_INDEX] = 잠금참조;
    }
    static boolean 배열저장가능(int ARRAY_Referenzen, int Daten_VALUE) {
        if (Daten_VALUE == 0 || ARRAY_Element[ARRAY_Referenzen] == 0) return true;
        boolean 성공여부 = ARRAY_Element[ARRAY_Referenzen] == -1 ? (Daten_VALUE > 0 && Daten_VALUE < 힙끝 && 힙[Daten_VALUE] == 1) : 맞는객체(Daten_VALUE, ARRAY_Element[ARRAY_Referenzen]);
        if (!성공여부 && !Feeler) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int ARRAY_Slot(int Referenzen, int déifstellen_VALUE, int TYPE_VALUE) {
        if (!Objet_VALUE(Referenzen, TYPE_VALUE)) return 0;
        if (déifstellen_VALUE < 0 || déifstellen_VALUE >= 힙[Referenzen + 1]) { Feeler_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return Referenzen + 2 + déifstellen_VALUE;
    }
    static void ausféieren_Befeel() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (Feeler) { if (던진객체 != 0) 예외처리(); if (Feeler || Rumm_INDEX < 현재가닥 * 32) break; }
            if (Rumm_INDEX < 현재가닥 * 32 || 바꿈요청 || --조각 == 0) { if (!SWITCH_Thread()) break; 조각 = 100; }
            if (Rumm_INDEX == 0 && Klass_Definitioun_Status[Agab_Klass_Definitioun] != 2 && !initialiséieren(Agab_Klass_Definitioun, Rumm_positionéieren[Rumm_INDEX])) continue;
            if (Rumm_INDEX == 현재가닥 * 32 && 현재가닥 != 0 && (Method_Zougrëff[Rumm_Method[Rumm_INDEX]] & 32) != 0 && 틀잠금[Rumm_INDEX] == 0) {
                int Objet_Referenzen = Thread_Zil[현재가닥]; if (!잠금얻기(Objet_Referenzen)) { if (Feeler) break; continue; } 틀잠금[Rumm_INDEX] = Objet_Referenzen;
            }
            잠시수 = 0;
            if (--남음 == 0) { Feeler_VALUE("instruction limit (500000)"); break; }
            int Laf = Rumm_positionéieren[Rumm_INDEX]; Rumm_Instruktioun[Rumm_INDEX] = Laf; int VALUE = 명바();
            if (Feeler) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = Method_Besëtzer[Rumm_Method[Rumm_INDEX]] * 512 + (VALUE == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= Konstant_Tag.length) Feeler_VALUE("invalid ldc constant");
                else if (Konstant_Tag[수] == 3) 넣기(상가[수], 1);
                else if (Konstant_Tag[수] == 8) 넣기(Konstant_SMS(상가[수]), 2);
                else Feeler_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { schreiwen_lokal(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { schreiwen_lokal(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { schreiwen_lokal(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE >= 50 && VALUE <= 53) {
                int Agab_positionéieren = 빼기(1), Objet_Referenzen = 빼기(2), Kategorie_CODE = VALUE == 46 ? 2 : VALUE == 50 ? 3 : VALUE == 51 ? 20 : VALUE == 52 ? 22 : 23;
                if (VALUE == 51 && Objet_Referenzen > 0 && Objet_Referenzen < 힙끝 && 힙[Objet_Referenzen] == 21) Kategorie_CODE = 21;
                int 읽는자리 = ARRAY_Slot(Objet_Referenzen, Agab_positionéieren, Kategorie_CODE); if (!Feeler) 넣기(힙[읽는자리], VALUE == 50 ? 2 : 1); continue;
            }
            if (VALUE == 79 || VALUE >= 83 && VALUE <= 86) {
                int Agab_Referenzen = 빼기(VALUE == 83 ? 2 : 1), Agab_positionéieren = 빼기(1), Objet_Referenzen = 빼기(2), Kategorie_CODE = VALUE == 79 ? 2 : VALUE == 83 ? 3 : VALUE == 84 ? 20 : VALUE == 85 ? 22 : 23;
                if (VALUE == 84 && Objet_Referenzen > 0 && Objet_Referenzen < 힙끝 && 힙[Objet_Referenzen] == 21) Kategorie_CODE = 21;
                int 읽는자리 = ARRAY_Slot(Objet_Referenzen, Agab_positionéieren, Kategorie_CODE);
                if (!Feeler && Kategorie_CODE == 3 && !배열저장가능(Objet_Referenzen, Agab_Referenzen)) continue;
                if (!Feeler) 힙[읽는자리] = Kategorie_CODE == 20 ? (byte)Agab_Referenzen : Kategorie_CODE == 21 ? Agab_Referenzen & 1 : Kategorie_CODE == 22 ? (char)Agab_Referenzen : Kategorie_CODE == 23 ? (short)Agab_Referenzen : Agab_Referenzen;
                continue;
            }
            if (VALUE >= 87 && VALUE <= 95) { Stapel_Instruktioun(VALUE); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), Mooss = 0;
                if ((VALUE == 108 || VALUE == 112) && 나 == 0) { Feeler_VALUE("ArithmeticException: / by zero"); continue; }
                if (VALUE == 96) Mooss = 가 + 나;
                if (VALUE == 100) Mooss = 가 - 나;
                if (VALUE == 104) Mooss = 가 * 나;
                if (VALUE == 108) Mooss = 가 / 나;
                if (VALUE == 112) Mooss = 가 % 나;
                if (VALUE == 120) Mooss = 가 << 나;
                if (VALUE == 122) Mooss = 가 >> 나;
                if (VALUE == 124) Mooss = 가 >>> 나;
                if (VALUE == 126) Mooss = 가 & 나;
                if (VALUE == 128) Mooss = 가 | 나;
                if (VALUE == 130) Mooss = 가 ^ 나;
                넣기(Mooss, 1); continue;
            }
            if (VALUE == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALUE == 132) {
                int lokal_Beräich = 명바(), 증분 = (byte)명바(); 지역읽기(lokal_Beräich, 1); 넣기(빼기(1) + 증분, 1); schreiwen_lokal(lokal_Beräich, 1); continue;
            }
            if (VALUE >= 145 && VALUE <= 147) {
                int 수 = 빼기(1); 넣기(VALUE == 145 ? (byte)수 : VALUE == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                int Zil_VALUE = Laf + (short)명짧(); boolean 갈까 = VALUE == 167;
                if (VALUE >= 153 && VALUE <= 158) {
                    int 수 = 빼기(1); 갈까 = VALUE == 153 ? 수 == 0 : VALUE == 154 ? 수 != 0 : VALUE == 155 ? 수 < 0 : VALUE == 156 ? 수 >= 0 : VALUE == 157 ? 수 > 0 : 수 <= 0;
                } else if (VALUE >= 159 && VALUE <= 166) {
                    int 나 = 빼기(VALUE >= 165 ? 2 : 1), 가 = 빼기(VALUE >= 165 ? 2 : 1);
                    갈까 = VALUE == 159 || VALUE == 165 ? 가 == 나 : VALUE == 160 || VALUE == 166 ? 가 != 나 : VALUE == 161 ? 가 < 나 : VALUE == 162 ? 가 >= 나 : VALUE == 163 ? 가 > 나 : 가 <= 나;
                } else if (VALUE == 198 || VALUE == 199) { int 수 = 빼기(2); 갈까 = VALUE == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) verréckelen_VALUE(Zil_VALUE); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { 반환(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE >= 178 && VALUE <= 181) { 필드호출(명상수(), VALUE, Laf); continue; }
            if (VALUE >= 182 && VALUE <= 185) {
                int 부호값 = 명상수();
                if (VALUE == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { Feeler_VALUE("invalid invokeinterface operands"); continue; } }
                CALL_Method(부호값, VALUE); continue;
            }
            if (VALUE == 187) { 새객체(Klass_Numm_SMS(명상수()), Laf); continue; }
            if (VALUE == 188 || VALUE == 189) {
                int Kategorie_CODE = 3, Komponent = 0;
                if (VALUE == 188) { int 임시값 = 명바(); Kategorie_CODE = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else Komponent = Klass_Numm_SMS(명상수());
                if (Kategorie_CODE == 0) { Feeler_VALUE("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), Objet_Referenzen = zouweisen_Späicher(Kategorie_CODE, 유효길이); if (!Feeler) ARRAY_Element[Objet_Referenzen] = Komponent; 넣기(Objet_Referenzen, 2); continue;
            }
            if (VALUE == 190) {
                int Objet_Referenzen = 빼기(2);
                if (객체유효(Objet_Referenzen)) { int 비교자리 = 힙[Objet_Referenzen]; if (비교자리 != 2 && 비교자리 != 3 && (비교자리 < 20 || 비교자리 > 23)) Feeler_VALUE("not an array"); else 넣기(힙[Objet_Referenzen + 1], 1); }
                continue;
            }
            if (VALUE == 191) {
                int Objet_Referenzen = 빼기(2); if (객체유효(Objet_Referenzen)) { if (힙[Objet_Referenzen] != 9) Feeler_VALUE("athrow requires supported Throwable"); else { 던진객체 = Objet_Referenzen; Feeler = true; } }
                continue;
            }
            if (VALUE == 192 || VALUE == 193) {
                int Numm_Konstant = Klass_Numm_SMS(명상수()), Objet_Referenzen = 빼기(2); boolean MATCH = 맞는객체(Objet_Referenzen, Numm_Konstant);
                if (VALUE == 193) 넣기(Objet_Referenzen != 0 && MATCH ? 1 : 0, 1);
                else { if (!MATCH && !Feeler) Feeler_VALUE("ClassCastException"); 넣기(Objet_Referenzen, 2); }
                continue;
            }
            if (VALUE == 170 || VALUE == 171) {
                int 읽는자리 = Laf + 1, Fichier_INDEX = Rumm_Method[Rumm_INDEX], Tast_Referenzen = 빼기(1);
                while ((읽는자리 - Method_Start[Fichier_INDEX]) % 4 != 0) 읽는자리++;
                int Zil_Adress = positionéieren_Ganzzuel(읽는자리);
                if (VALUE == 170) { int 낮은값 = positionéieren_Ganzzuel(읽는자리 + 4), 높은값 = positionéieren_Ganzzuel(읽는자리 + 8); if (Tast_Referenzen >= 낮은값 && Tast_Referenzen <= 높은값) Zil_Adress = positionéieren_Ganzzuel(읽는자리 + 12 + (Tast_Referenzen - 낮은값) * 4); }
                else { int 총수 = positionéieren_Ganzzuel(읽는자리 + 4); for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) if (positionéieren_Ganzzuel(읽는자리 + 8 + Loop_INDEX * 8) == Tast_Referenzen) Zil_Adress = positionéieren_Ganzzuel(읽는자리 + 12 + Loop_INDEX * 8); }
                verréckelen_VALUE(Laf + Zil_Adress); continue;
            }
            if (VALUE == 200) { verréckelen_VALUE(Laf + positionéieren_Ganzzuel(Laf + 1)); continue; }
            if (VALUE == 194 || VALUE == 195) {
                int Objet_Referenzen = 빼기(2);
                if (VALUE == 195) 잠금풀기(Objet_Referenzen);
                else if (!잠금얻기(Objet_Referenzen) && !Feeler) { 넣기(Objet_Referenzen, 2); Rumm_positionéieren[Rumm_INDEX] = Laf; }
                continue;
            }
            if (VALUE == 196) {
                int Befeel_CODE = 명바(), Agab_positionéieren = 명짧();
                if (Befeel_CODE == 21 || Befeel_CODE == 25) 지역읽기(Agab_positionéieren, Befeel_CODE == 21 ? 1 : 2);
                else if (Befeel_CODE == 54 || Befeel_CODE == 58) schreiwen_lokal(Agab_positionéieren, Befeel_CODE == 54 ? 1 : 2);
                else if (Befeel_CODE == 132) { int DELTA_VALUE = (short)명짧(); 지역읽기(Agab_positionéieren, 1); 넣기(빼기(1) + DELTA_VALUE, 1); schreiwen_lokal(Agab_positionéieren, 1); }
                else Feeler_VALUE("unsupported wide opcode");
                continue;
            }
            Feeler_VALUE("unsupported bytecode");
        }
    }
    static int FIND_Klass_Definitioun(int Numm) {
        for (int Loop_INDEX = 0; Loop_INDEX < Klass_Definitioun_COUNT; Loop_INDEX++) if (Klass_Definitioun_Numm[Loop_INDEX] != 0 && 같은말(Klass_Definitioun_Numm[Loop_INDEX], Numm)) return Loop_INDEX;
        return Charge_Klass_Definitioun(Konstant_SMS(Numm));
    }
    static int Charge_Klass_Definitioun(int Numm_Zeechefolleg) {
        if (!Objet_VALUE(Numm_Zeechefolleg, 1)) return -1;
        int Längt_VALUE = 힙[Numm_Zeechefolleg + 1];
        if (Längt_VALUE < 1 || Längt_VALUE > 505 || Klass_Definitioun_COUNT == 16) { Feeler_VALUE("class name/count limit"); return -1; }
        for (int Loop_INDEX = 0; Loop_INDEX < Längt_VALUE; Loop_INDEX++) { int Zeechecode = 힙[Numm_Zeechefolleg + 2 + Loop_INDEX]; Fichier_Numm_SMS[Loop_INDEX] = Zeechecode == '/' ? '.' : Zeechecode; }
        Fichier_Numm_SMS[Längt_VALUE] = '.'; Fichier_Numm_SMS[Längt_VALUE + 1] = 'c'; Fichier_Numm_SMS[Längt_VALUE + 2] = 'l'; Fichier_Numm_SMS[Längt_VALUE + 3] = 'a'; Fichier_Numm_SMS[Längt_VALUE + 4] = 's'; Fichier_Numm_SMS[Längt_VALUE + 5] = 's'; Fichier_Numm_SMS[Längt_VALUE + 6] = 0;
        int d_Gréisst_veränneren = Benotzer.파일읽기(Fichier_Numm_SMS, 임시파일);
        if (d_Gréisst_veränneren < 0) { Feeler_VALUE("ClassNotFoundException"); return -1; }
        int Klass_Definitioun = Klass_Definitioun_COUNT++; Klass_Definitioun_d_Gréisst_veränneren[Klass_Definitioun] = d_Gréisst_veränneren;
        for (int Loop_INDEX = 0; Loop_INDEX < d_Gréisst_veränneren; Loop_INDEX++) Fichier[Klass_Definitioun * 16384 + Loop_INDEX] = 임시파일[Loop_INDEX];
        클래스읽기(Klass_Definitioun); if (Feeler) return -1;
        int aktuell_Daten = Konstant_SMS(Klass_Definitioun_Numm[Klass_Definitioun]);
        if (!글같음(aktuell_Daten, Numm_Zeechefolleg, true)) { Feeler_VALUE("class name does not match file"); return -1; }
        int 부모 = 종부모[Klass_Definitioun];
        if (부모 != 0 && !Word_SMS(부모, "java/lang/Object") && !Word_SMS(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = FIND_Klass_Definitioun(부모);
            if (Feeler || 위 < 0) return -1;
            int 읽는자리 = 위, Phas_COUNT = 0;
            while (읽는자리 >= 0 && Phas_COUNT++ < 16) {
                if (읽는자리 == Klass_Definitioun) { Feeler_VALUE("cyclic inheritance"); return -1; }
                읽는자리 = 부모종(읽는자리);
            }
            int 시작변위 = Klass_Slot_COUNT[위];
            for (int Fichier_INDEX = 0; Fichier_INDEX < Slot_COUNT; Fichier_INDEX++) if (Slot_Besëtzer[Fichier_INDEX] == Klass_Definitioun && (Slot_Autorisatiounen[Fichier_INDEX] & 8) == 0) Slot_positionéieren[Fichier_INDEX] += 시작변위;
            Klass_Slot_COUNT[Klass_Definitioun] += 시작변위;
        }
        return Klass_Definitioun;
    }
    static int 부모종(int Klass_Definitioun) {
        int Numm = 종부모[Klass_Definitioun];
        for (int Loop_INDEX = 0; Loop_INDEX < Klass_Definitioun_COUNT; Loop_INDEX++) if (Numm != 0 && Klass_Definitioun_Numm[Loop_INDEX] != 0 && 같은말(Klass_Definitioun_Numm[Loop_INDEX], Numm)) return Loop_INDEX;
        return -1;
    }
    static int FIND_Method(int Klass_Definitioun, int Numm, int Format_VALUE) {
        for (int 깊이 = 0; Klass_Definitioun >= 0 && 깊이 < 16; 깊이++, Klass_Definitioun = 부모종(Klass_Definitioun)) {
            for (int Loop_INDEX = 0; Loop_INDEX < Method_COUNT; Loop_INDEX++) if (Method_Besëtzer[Loop_INDEX] == Klass_Definitioun && 같은말(Method_Numm_SMS[Loop_INDEX], Numm) && 같은말(Method_TYPE[Loop_INDEX], Format_VALUE)) return Loop_INDEX;
        }
        return -1;
    }
    static int Numm_Method(int Klass_Definitioun, String Numm, String Format_VALUE) {
        for (int 깊이 = 0; Klass_Definitioun >= 0 && 깊이 < 16; 깊이++, Klass_Definitioun = 부모종(Klass_Definitioun))
            for (int Loop_INDEX = 0; Loop_INDEX < Method_COUNT; Loop_INDEX++) if (Method_Besëtzer[Loop_INDEX] == Klass_Definitioun && Word_SMS(Method_Numm_SMS[Loop_INDEX], Numm) && Word_SMS(Method_TYPE[Loop_INDEX], Format_VALUE)) return Loop_INDEX;
        return -1;
    }
    static int 형종류(int Numm) { return Fichier[상가[Numm]] == 'L' || Fichier[상가[Numm]] == '[' ? 2 : 1; }
    static boolean initialiséieren(int Klass_Definitioun, int Befeel_Start) {
        if (Klass_Definitioun < 0 || Feeler) return false;
        if (Klass_Definitioun_Status[Klass_Definitioun] == 3) { Feeler_VALUE("NoClassDefFoundError: initialization failed"); return false; }
        if (Klass_Definitioun_Status[Klass_Definitioun] == 1 && Klass_Thread[Klass_Definitioun] != 현재가닥) { Rumm_positionéieren[Rumm_INDEX] = Befeel_Start; 바꿈요청 = true; return false; }
        if (Klass_Definitioun_Status[Klass_Definitioun] != 0) return true;
        int 위 = 부모종(Klass_Definitioun);
        if (위 >= 0 && !initialiséieren(위, Befeel_Start)) return false;
        Klass_Definitioun_Status[Klass_Definitioun] = 1; Klass_Thread[Klass_Definitioun] = 현재가닥;
        if (initialiséieren_Klass_Definitioun[Klass_Definitioun] != 0) {
            Rumm_positionéieren[Rumm_INDEX] = Befeel_Start;
            호출(initialiséieren_Klass_Definitioun[Klass_Definitioun] - 1); if (!Feeler) initialiséieren_Rumm[Rumm_INDEX] = Klass_Definitioun + 1;
            return false;
        }
        Klass_Definitioun_Status[Klass_Definitioun] = 2; return true;
    }
    static void 필드호출(int INDEX, int Befeel, int Laf) {
        if (!Scheck_Konstant(INDEX, 9)) return;
        int Besëtzer_VALUE = Klass_Numm_SMS(상가[INDEX]), Numm = Referenzen_Numm(Konstant_SECOND_VALUE[INDEX]), Format_VALUE = Referenzen_TYPE(Konstant_SECOND_VALUE[INDEX]);
        if (Word_SMS(Besëtzer_VALUE, "java/lang/System") && (Word_SMS(Numm, "out") || Word_SMS(Numm, "err")) && Word_SMS(Format_VALUE, "Ljava/io/PrintStream;") && Befeel == 178) { 넣기(-1, 2); return; }
        int Klass_Definitioun = FIND_Klass_Definitioun(Besëtzer_VALUE); if (Klass_Definitioun < 0 || Feeler) return;
        int 찾음 = -1;
        for (int 읽는자리 = Klass_Definitioun, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = 부모종(읽는자리))
            for (int Fichier_INDEX = 0; Fichier_INDEX < Slot_COUNT; Fichier_INDEX++) if (Slot_Besëtzer[Fichier_INDEX] == 읽는자리 && 같은말(Slot_Numm[Fichier_INDEX], Numm) && 같은말(Slot_TYPE[Fichier_INDEX], Format_VALUE)) 찾음 = Fichier_INDEX;
        if (찾음 < 0) { Feeler_VALUE("NoSuchFieldError"); return; }
        boolean statesch_VALUE = Befeel == 178 || Befeel == 179;
        if (statesch_VALUE != ((Slot_Autorisatiounen[찾음] & 8) != 0)) { Feeler_VALUE("field static/instance mismatch"); return; }
        if (statesch_VALUE && !initialiséieren(Slot_Besëtzer[찾음], Laf)) return;
        int TYPE_VALUE = 형종류(Format_VALUE), VALUE = 0;
        if (Befeel == 179 || Befeel == 181) VALUE = 빼기(TYPE_VALUE);
        if (statesch_VALUE) { if (Befeel == 178) 넣기(Slot_Daten[찾음], TYPE_VALUE); else if (!Feeler) Slot_Daten[찾음] = VALUE; return; }
        int Objet_Referenzen = 빼기(2);
        if (!객체유효(Objet_Referenzen)) return;
        if (힙[Objet_Referenzen] < 32 || !종포함(힙[Objet_Referenzen] - 32, Besëtzer_VALUE)) { Feeler_VALUE("field receiver type mismatch"); return; }
        int 보관칸 = Objet_Referenzen + 2 + Slot_positionéieren[찾음];
        if (Befeel == 180) 넣기(힙[보관칸], TYPE_VALUE);
        else if (!Feeler) { 힙[보관칸] = VALUE; 힙참조[보관칸] = TYPE_VALUE == 2 ? 1 : 0; }
    }
    static boolean 종포함(int Klass_Definitioun, int Numm) {
        for (int 중첩깊이 = 0; Klass_Definitioun >= 0 && 중첩깊이 < 16; 중첩깊이++, Klass_Definitioun = 부모종(Klass_Definitioun)) {
            if (같은말(Klass_Definitioun_Numm[Klass_Definitioun], Numm) || (종부모[Klass_Definitioun] != 0 && 같은말(종부모[Klass_Definitioun], Numm))) return true;
            for (int intern_Verknëppung_positionéieren = 0; intern_Verknëppung_positionéieren < Klass_Interface_COUNT[Klass_Definitioun]; intern_Verknëppung_positionéieren++) if (같은말(Klass_Interface[Klass_Definitioun * 16 + intern_Verknëppung_positionéieren], Numm)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int Byte_Daten, boolean Wee) {
        if (첫값 == Byte_Daten) return true;
        if (첫값 <= 0 || Byte_Daten <= 0 || 힙[첫값] != 1 || 힙[Byte_Daten] != 1 || 힙[첫값 + 1] != 힙[Byte_Daten + 1]) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) {
            int X_Koordinat = 힙[첫값 + 2 + Loop_INDEX], 세로좌표 = 힙[Byte_Daten + 2 + Loop_INDEX];
            if (Wee) { if (X_Koordinat == '.') X_Koordinat = '/'; if (세로좌표 == '.') 세로좌표 = '/'; }
            if (X_Koordinat != 세로좌표) return false;
        }
        return true;
    }
    static boolean 객체유효(int Objet_Referenzen) {
        if (Objet_Referenzen == 0) { Feeler_VALUE("NullPointerException"); return false; }
        if (Objet_Referenzen < 1 || Objet_Referenzen >= 힙끝 || 힙폭[Objet_Referenzen] < 2 || 힙[Objet_Referenzen] == 0) { Feeler_VALUE("invalid object reference"); return false; }
        return true;
    }
    static void schützen_VALUE(int Objet_Referenzen) {
        if (Objet_Referenzen > 0 && Objet_Referenzen < 힙끝 && 힙폭[Objet_Referenzen] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = Objet_Referenzen;
    }
    static void Show_VALUE(int Objet_Referenzen) {
        if (Objet_Referenzen > 0 && Objet_Referenzen < 힙끝 && 힙폭[Objet_Referenzen] >= 2 && 힙[Objet_Referenzen] != 0 && 힙표시[Objet_Referenzen] == 0) {
            힙표시[Objet_Referenzen] = 1; 표시대기[Bildschierm_COUNT++] = Objet_Referenzen;
        }
    }
    static void 수거() {
        Bildschierm_COUNT = 0; Sammlung_COUNT++;
        for (int Scheck_positionéieren = 1; Scheck_positionéieren < 힙끝; Scheck_positionéieren += 힙폭[Scheck_positionéieren]) 힙표시[Scheck_positionéieren] = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Zeechefolleg_Referenzen.length; Loop_INDEX++) Show_VALUE(Zeechefolleg_Referenzen[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Slot_COUNT; Loop_INDEX++) if ((Slot_Autorisatiounen[Loop_INDEX] & 8) != 0 && 형종류(Slot_TYPE[Loop_INDEX]) == 2) Show_VALUE(Slot_Daten[Loop_INDEX]);
        for (int 임시값 = 0; 임시값 < Thread_COUNT; 임시값++) {
            Show_VALUE(Thread_Objet[임시값]); Show_VALUE(Thread_Zil[임시값]);
            int 꼭대기자리 = 임시값 == 현재가닥 ? Rumm_INDEX : Thread_Rumm[임시값];
            for (int Fichier_INDEX = 임시값 * 32; Fichier_INDEX <= 꼭대기자리; Fichier_INDEX++) {
                for (int intern_Verknëppung_positionéieren = 0; intern_Verknëppung_positionéieren < 함수지역[Rumm_Method[Fichier_INDEX]]; intern_Verknëppung_positionéieren++) if (lokal_TYPE[Fichier_INDEX * 128 + intern_Verknëppung_positionéieren] == 2) Show_VALUE(lokal_VALUE[Fichier_INDEX * 128 + intern_Verknëppung_positionéieren]);
                for (int intern_Verknëppung_positionéieren = 0; intern_Verknëppung_positionéieren < Rumm_Stapel[Fichier_INDEX]; intern_Verknëppung_positionéieren++) if (스택형[Fichier_INDEX * 128 + intern_Verknëppung_positionéieren] == 2) Show_VALUE(스택값[Fichier_INDEX * 128 + intern_Verknëppung_positionéieren]);
            }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 화면참조.length; Loop_INDEX++) Show_VALUE(화면참조[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 나중수; Loop_INDEX++) Show_VALUE(나중실행[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Store_Ganzzuel.length; Loop_INDEX++) Show_VALUE(Store_Ganzzuel[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Klass_Definitioun_COUNT; Loop_INDEX++) Show_VALUE(종잠금[Loop_INDEX]);
        for (int Scheck_positionéieren = 1; Scheck_positionéieren < 힙끝; Scheck_positionéieren += 힙폭[Scheck_positionéieren]) if (잠금깊이[Scheck_positionéieren] > 0) Show_VALUE(Scheck_positionéieren);
        Show_VALUE(던진객체);
        for (int Loop_INDEX = 0; Loop_INDEX < 잠시수; Loop_INDEX++) Show_VALUE(잠시참조[Loop_INDEX]);
        while (Bildschierm_COUNT > 0) {
            int Objet_Referenzen = 표시대기[--Bildschierm_COUNT], Kategorie_CODE = 힙[Objet_Referenzen];
            for (int Loop_INDEX = Objet_Referenzen + 2; Loop_INDEX < Objet_Referenzen + 힙폭[Objet_Referenzen]; Loop_INDEX++) if (Kategorie_CODE == 3 || Kategorie_CODE == 4 || 힙참조[Loop_INDEX] != 0) Show_VALUE(힙[Loop_INDEX]);
        }
        for (int Scheck_positionéieren = 1; Scheck_positionéieren < 힙끝; Scheck_positionéieren += 힙폭[Scheck_positionéieren]) if (힙표시[Scheck_positionéieren] == 0) 힙[Scheck_positionéieren] = 0;
        for (int Scheck_positionéieren = 1; Scheck_positionéieren < 힙끝; Scheck_positionéieren += 힙폭[Scheck_positionéieren]) if (힙[Scheck_positionéieren] == 0) {
            while (Scheck_positionéieren + 힙폭[Scheck_positionéieren] < 힙끝 && 힙[Scheck_positionéieren + 힙폭[Scheck_positionéieren]] == 0) { int Weider_positionéieren = Scheck_positionéieren + 힙폭[Scheck_positionéieren]; 힙폭[Scheck_positionéieren] += 힙폭[Weider_positionéieren]; 힙폭[Weider_positionéieren] = 0; }
            if (Scheck_positionéieren + 힙폭[Scheck_positionéieren] == 힙끝) { 힙끝 = Scheck_positionéieren; break; }
        }
    }
    static int 새기억(int 종류, int Längt_VALUE) {
        if (Längt_VALUE < 0) { Feeler_VALUE("NegativeArraySizeException"); return 0; }
        if (Längt_VALUE > 힙.length - 3) { Feeler_VALUE("object heap exhausted"); return 0; }
        int 필요수 = Längt_VALUE + 2, Objet_Referenzen = 0;
        if (필요수 <= 힙.length - 힙끝) { Objet_Referenzen = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { Objet_Referenzen = 읽는자리; break; }
            if (Objet_Referenzen != 0) {
                int 남은길이 = 힙폭[Objet_Referenzen] - 필요수;
                if (남은길이 >= 2) { 힙폭[Objet_Referenzen + 필요수] = 남은길이; 힙[Objet_Referenzen + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { Objet_Referenzen = 힙끝; 힙끝 += 필요수; }
        }
        if (Objet_Referenzen == 0) { Feeler_VALUE("object heap exhausted"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < 필요수; Loop_INDEX++) { 힙[Objet_Referenzen + Loop_INDEX] = 0; 힙참조[Objet_Referenzen + Loop_INDEX] = 0; 힙폭[Objet_Referenzen + Loop_INDEX] = 0; }
        ARRAY_Element[Objet_Referenzen] = 0;
        힙폭[Objet_Referenzen] = 필요수; 힙[Objet_Referenzen] = 종류; 힙[Objet_Referenzen + 1] = Längt_VALUE; schützen_VALUE(Objet_Referenzen); return Objet_Referenzen;
    }
    static int 예외종(String Numm_Konstant) {
        if (자바도구.같음(Numm_Konstant, "java/lang/Throwable")) return 1;
        if (자바도구.같음(Numm_Konstant, "java/lang/Exception")) return 2;
        if (자바도구.같음(Numm_Konstant, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(Numm_Konstant, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(Numm_Konstant, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(Numm_Konstant, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(Numm_Konstant, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(Numm_Konstant, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(Numm_Konstant, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(Numm_Konstant, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(Numm_Konstant, "java/io/IOException")) return 11;
        if (자바도구.같음(Numm_Konstant, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(Numm_Konstant, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(Numm_Konstant, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(Numm_Konstant, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int 예외상수(int Numm) {
        for (int Loop_INDEX = 1; Loop_INDEX <= 41; Loop_INDEX++) if (Word_SMS(Numm, 예외이름(Loop_INDEX))) return Loop_INDEX;
        return 0;
    }
    static String 예외이름(int Kont_VALUE) {
        if (Kont_VALUE == 40) return "java/lang/InterruptedException";
        if (Kont_VALUE == 41) return "한국어/자체/대기중단예외";
        if (Kont_VALUE == 39) return "java/net/SocketException";
        if (Kont_VALUE == 20) return "한국어/자체/예외";
        if (Kont_VALUE == 21) return "한국어/자체/실행예외";
        if (Kont_VALUE == 22) return "한국어/자체/입출력예외";
        if (Kont_VALUE == 23) return "한국어/자체/대기시간초과예외";
        if (Kont_VALUE == 24) return "한국어/자체/주소확인예외";
        if (Kont_VALUE == 25) return "한국어/자체/파일없음예외";
        if (Kont_VALUE == 26) return "한국어/자체/통신예외";
        if (Kont_VALUE == 27) return "한국어/자체/잘못된인수예외";
        if (Kont_VALUE == 28) return "한국어/자체/숫자형식예외";
        if (Kont_VALUE == 29) return "한국어/자체/범위예외";
        if (Kont_VALUE == 30) return "한국어/자체/배열범위예외";
        if (Kont_VALUE == 31) return "한국어/자체/문자열범위예외";
        if (Kont_VALUE == 32) return "한국어/자체/빈참조예외";
        if (Kont_VALUE == 33) return "한국어/자체/산술예외";
        if (Kont_VALUE == 34) return "한국어/자체/상태예외";
        if (Kont_VALUE == 35) return "한국어/자체/형변환예외";
        if (Kont_VALUE == 36) return "한국어/자체/음수배열크기예외";
        if (Kont_VALUE == 37) return "한국어/자체/ARRAY_Store_Feeler";
        if (Kont_VALUE == 38) return "한국어/자체/가닥상태예외";
        if (Kont_VALUE == 1) return "java/lang/Throwable"; if (Kont_VALUE == 2) return "java/lang/Exception";
        if (Kont_VALUE == 3) return "java/lang/RuntimeException"; if (Kont_VALUE == 4) return "java/lang/ArithmeticException";
        if (Kont_VALUE == 5) return "java/lang/NullPointerException"; if (Kont_VALUE == 6) return "java/lang/IndexOutOfBoundsException";
        if (Kont_VALUE == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (Kont_VALUE == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (Kont_VALUE == 9) return "java/lang/IllegalArgumentException"; if (Kont_VALUE == 10) return "java/lang/NumberFormatException";
        if (Kont_VALUE == 11) return "java/io/IOException"; if (Kont_VALUE == 12) return "java/io/FileNotFoundException";
        if (Kont_VALUE == 17) return "java/lang/ArrayStoreException";
        if (Kont_VALUE == 18) return "java/net/UnknownHostException";
        if (Kont_VALUE == 19) return "java/net/SocketTimeoutException";
        if (Kont_VALUE == 16) return "java/lang/IllegalThreadStateException";
        if (Kont_VALUE == 13) return "java/lang/IllegalStateException"; if (Kont_VALUE == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int Kont_VALUE) {
        if (Kont_VALUE == 40) return 2;
        if (Kont_VALUE == 41) return 40;
        if (Kont_VALUE == 39) return 11;
        if (Kont_VALUE == 1) return 0;
        if (Kont_VALUE == 2) return 1;
        if (Kont_VALUE == 3) return 2;
        if (Kont_VALUE == 4) return 3;
        if (Kont_VALUE == 5) return 3;
        if (Kont_VALUE == 6) return 3;
        if (Kont_VALUE == 7) return 6;
        if (Kont_VALUE == 8) return 6;
        if (Kont_VALUE == 9) return 3;
        if (Kont_VALUE == 10) return 9;
        if (Kont_VALUE == 11) return 2;
        if (Kont_VALUE == 12) return 11;
        if (Kont_VALUE == 13) return 3;
        if (Kont_VALUE == 14) return 3;
        if (Kont_VALUE == 15) return 3;
        if (Kont_VALUE == 16) return 9;
        if (Kont_VALUE == 17) return 3;
        if (Kont_VALUE == 18) return 11;
        if (Kont_VALUE == 19) return 11;
        if (Kont_VALUE == 20) return 2;
        if (Kont_VALUE == 21) return 3;
        if (Kont_VALUE == 22) return 11;
        if (Kont_VALUE == 23) return 22;
        if (Kont_VALUE == 24) return 22;
        if (Kont_VALUE == 25) return 22;
        if (Kont_VALUE == 26) return 22;
        if (Kont_VALUE == 27) return 9;
        if (Kont_VALUE == 28) return 27;
        if (Kont_VALUE == 29) return 6;
        if (Kont_VALUE == 30) return 29;
        if (Kont_VALUE == 31) return 29;
        if (Kont_VALUE == 32) return 5;
        if (Kont_VALUE == 33) return 4;
        if (Kont_VALUE == 34) return 13;
        if (Kont_VALUE == 35) return 14;
        if (Kont_VALUE == 36) return 15;
        if (Kont_VALUE == 37) return 17;
        if (Kont_VALUE == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int aktuell_VALUE, int 요구값) {
        for (int 깊이 = 0; aktuell_VALUE != 0 && 깊이 < 16; 깊이++, aktuell_VALUE = 예외부모(aktuell_VALUE))
            if (aktuell_VALUE == 요구값) return true;
        return false;
    }
    static void 예외던짐(int Kont_VALUE, String LIESMECH_Referenzen) {
        int Objet_Referenzen = 새기억(9, 2); if (Feeler) return;
        힙[Objet_Referenzen + 2] = Kont_VALUE; 힙[Objet_Referenzen + 3] = Host_Zeechen(LIESMECH_Referenzen); 힙참조[Objet_Referenzen + 3] = 1;
        던진객체 = Objet_Referenzen; Feeler = true;
    }
    static boolean 맞는객체(int Objet_Referenzen, int Numm) {
        if (Objet_Referenzen == 0) return true;
        if (!객체유효(Objet_Referenzen)) return false;
        int Kategorie_CODE = 힙[Objet_Referenzen];
        if (Word_SMS(Numm, "java/lang/Object")) return true;
        if (Kategorie_CODE >= 32) return 종포함(Kategorie_CODE - 32, Numm);
        if (Kategorie_CODE == 9) { int Zil_Adress = 예외상수(Numm); return Zil_Adress != 0 && 예외포함(힙[Objet_Referenzen + 2], Zil_Adress); }
        if (Kategorie_CODE == 1) return Word_SMS(Numm, "java/lang/String") || Word_SMS(Numm, "java/lang/CharSequence");
        if (Kategorie_CODE == 4) return Word_SMS(Numm, "java/lang/StringBuilder") || Word_SMS(Numm, "java/lang/CharSequence");
        if (Kategorie_CODE == 10) return Word_SMS(Numm, "java/util/ArrayList") || Word_SMS(Numm, "java/util/List");
        if (Kategorie_CODE == 11) return Word_SMS(Numm, "java/util/HashMap") || Word_SMS(Numm, "java/util/Map");
        if (Kategorie_CODE == 12) return Word_SMS(Numm, "java/lang/Integer") || Word_SMS(Numm, "java/lang/Number");
        if (Kategorie_CODE >= 24 && Kategorie_CODE <= 28 && 힙[Objet_Referenzen + 13] != 0) return 한국어화면종(Numm) == Kategorie_CODE || Word_SMS(Numm, "한국어/자체/화면구성요소");
        if (Kategorie_CODE >= 24 && Kategorie_CODE <= 28) return (한국어화면종(Numm) == 0 && 화면종(Numm) == Kategorie_CODE) || Word_SMS(Numm, "java/awt/Component") || Word_SMS(Numm, "java/awt/Container") || Word_SMS(Numm, "javax/swing/JComponent");
        if (Kategorie_CODE == 29) return Word_SMS(Numm, 힙[Objet_Referenzen + 3] != 0 ? "한국어/자체/동작알림" : "java/awt/event/ActionEvent");
        if (Kategorie_CODE == 30) return Word_SMS(Numm, "java/awt/FlowLayout") || Word_SMS(Numm, "java/awt/LayoutManager");
        if (Kategorie_CODE == 17) return Word_SMS(Numm, "java/net/Socket");
        if (Kategorie_CODE == 18) return Word_SMS(Numm, "java/net/ServerSocket");
        if (Kategorie_CODE == 19) return Word_SMS(Numm, 힙[Objet_Referenzen + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (Kategorie_CODE == 14) return Word_SMS(Numm, "java/net/InetAddress");
        if (Kategorie_CODE == 15) return Word_SMS(Numm, "java/net/DatagramSocket");
        if (Kategorie_CODE == 16) return Word_SMS(Numm, "java/net/DatagramPacket");
        if (Kategorie_CODE == 13) return Word_SMS(Numm, 힙[Objet_Referenzen + 3] != 0 ? "한국어/자체/작업가닥" : "java/lang/Thread");
        if (Kategorie_CODE == 2) return Word_SMS(Numm, "[I"); if (Kategorie_CODE == 20) return Word_SMS(Numm, "[B"); if (Kategorie_CODE == 21) return Word_SMS(Numm, "[Z");
        if (Kategorie_CODE == 22) return Word_SMS(Numm, "[C"); if (Kategorie_CODE == 23) return Word_SMS(Numm, "[S");
        if (Kategorie_CODE != 3) return false;
        if (Word_SMS(Numm, "[Ljava/lang/Object;")) return true;
        int Komponent = ARRAY_Element[Objet_Referenzen];
        if (Komponent == -1) return Word_SMS(Numm, "[Ljava/lang/String;") || Word_SMS(Numm, "[Ljava/lang/CharSequence;");
        if (Komponent == 0) return false;
        if (배열종비교(Komponent, Numm)) return true;
        if ((Word_SMS(Komponent, "java/lang/String") || Word_SMS(Komponent, "java/lang/StringBuilder")) && Word_SMS(Numm, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDEX = 0; Loop_INDEX < Klass_Definitioun_COUNT; Loop_INDEX++) if (같은말(Klass_Definitioun_Numm[Loop_INDEX], Komponent)) {
            for (int Zeechecode = Loop_INDEX, 중첩깊이 = 0; Zeechecode >= 0 && 중첩깊이 < 16; 중첩깊이++, Zeechecode = 부모종(Zeechecode)) {
                if (배열종비교(종부모[Zeechecode], Numm)) return true;
                for (int intern_Verknëppung_positionéieren = 0; intern_Verknëppung_positionéieren < Klass_Interface_COUNT[Zeechecode]; intern_Verknëppung_positionéieren++) if (배열종비교(Klass_Interface[Zeechecode * 16 + intern_Verknëppung_positionéieren], Numm)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int Numm_Konstant, int 형식참조) {
        int Scheck_positionéieren = 상가[형식참조], Agab_COUNT = Konstant_SECOND_VALUE[형식참조];
        if (Numm_Konstant == 0 || Agab_COUNT < 4 || Fichier[Scheck_positionéieren] != '[' || Fichier[Scheck_positionéieren + 1] != 'L' || Fichier[Scheck_positionéieren + Agab_COUNT - 1] != ';' || Konstant_SECOND_VALUE[Numm_Konstant] != Agab_COUNT - 3) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < Agab_COUNT - 3; Loop_INDEX++) if (Fichier[상가[Numm_Konstant] + Loop_INDEX] != Fichier[Scheck_positionéieren + 2 + Loop_INDEX]) return false;
        return true;
    }
    static void 예외처리() {
        if (던진객체 == 0) return;
        Feeler = false;
        while (Rumm_INDEX >= 현재가닥 * 32) {
            int Fichier_INDEX = Rumm_Method[Rumm_INDEX], 읽는자리 = Rumm_Instruktioun[Rumm_INDEX];
            for (int Loop_INDEX = 0; Loop_INDEX < 잡기수; Loop_INDEX++) if (잡기함수[Loop_INDEX] == Fichier_INDEX && 읽는자리 >= 잡기시작[Loop_INDEX] && 읽는자리 < 잡기끝[Loop_INDEX]
                && (잡기종[Loop_INDEX] == 0 || 맞는객체(던진객체, 잡기종[Loop_INDEX]))) {
                Rumm_positionéieren[Rumm_INDEX] = 잡기위치[Loop_INDEX]; Rumm_Stapel[Rumm_INDEX] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (initialiséieren_Rumm[Rumm_INDEX] != 0) Klass_Definitioun_Status[initialiséieren_Rumm[Rumm_INDEX] - 1] = 3;
            if (틀잠금[Rumm_INDEX] != 0) { 잠금풀기(틀잠금[Rumm_INDEX]); 틀잠금[Rumm_INDEX] = 0; }
            Rumm_INDEX--;
        }
        Benotzer.schreiwen("Uncaught ");
        if (힙[던진객체] == 9) { Benotzer.schreiwen(예외이름(힙[던진객체 + 2])); Benotzer.schreiwen(": "); schreiwen_SMS(힙[던진객체 + 3]); }
        else Benotzer.schreiwen("user exception");
        Benotzer.schreiwen_Zeechen_VALUE(10); 던진객체 = 0; Feeler = true;
    }
    // 이 JVM의 스택 항목은 현재 category-1(int/reference)만 허용한다.
    static void Stapel_Instruktioun(int Befeel_CODE) {
        int 첫값 = 빼기(0), 첫형식 = 반환형;
        if (Befeel_CODE == 87) return;
        if (Befeel_CODE == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int Byte_Daten = 빼기(0), SECOND_Format = 반환형;
        if (Befeel_CODE == 88) return;
        if (Befeel_CODE == 90) { 넣기(첫값, 첫형식); 넣기(Byte_Daten, SECOND_Format); 넣기(첫값, 첫형식); return; }
        if (Befeel_CODE == 92) { 넣기(Byte_Daten, SECOND_Format); 넣기(첫값, 첫형식); 넣기(Byte_Daten, SECOND_Format); 넣기(첫값, 첫형식); return; }
        if (Befeel_CODE == 95) { 넣기(첫값, 첫형식); 넣기(Byte_Daten, SECOND_Format); return; }
        int Zeechecode = 빼기(0), 셋째형식 = 반환형;
        if (Befeel_CODE == 91) { 넣기(첫값, 첫형식); 넣기(Zeechecode, 셋째형식); 넣기(Byte_Daten, SECOND_Format); 넣기(첫값, 첫형식); return; }
        if (Befeel_CODE == 93) { 넣기(Byte_Daten, SECOND_Format); 넣기(첫값, 첫형식); 넣기(Zeechecode, 셋째형식); 넣기(Byte_Daten, SECOND_Format); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = 반환형;
        넣기(Byte_Daten, SECOND_Format); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(Zeechecode, 셋째형식); 넣기(Byte_Daten, SECOND_Format); 넣기(첫값, 첫형식);
    }
    static void 새객체(int Numm_Konstant, int 시작점) {
        int Kategorie_CODE = 0, 유효길이 = 0, 예외참조 = 예외상수(Numm_Konstant);
        if (Word_SMS(Numm_Konstant, "java/lang/StringBuilder")) { Kategorie_CODE = 4; 유효길이 = 1; }
        if (Word_SMS(Numm_Konstant, "java/io/FileInputStream")) { Kategorie_CODE = 5; 유효길이 = 2; }
        if (Word_SMS(Numm_Konstant, "java/io/FileOutputStream")) { Kategorie_CODE = 6; 유효길이 = 2; }
        if (예외참조 != 0) { Kategorie_CODE = 9; 유효길이 = 2; }
        if (Word_SMS(Numm_Konstant, "java/util/ArrayList")) { Kategorie_CODE = 10; 유효길이 = 2; }
        if (Word_SMS(Numm_Konstant, "java/util/HashMap")) { Kategorie_CODE = 11; 유효길이 = 2; }
        if (Word_SMS(Numm_Konstant, "java/lang/Integer")) { Kategorie_CODE = 12; 유효길이 = 1; }
        if (Word_SMS(Numm_Konstant, "java/net/Socket")) { Kategorie_CODE = 17; 유효길이 = 5; }
        if (Word_SMS(Numm_Konstant, "java/net/ServerSocket")) { Kategorie_CODE = 18; 유효길이 = 5; }
        if (Word_SMS(Numm_Konstant, "java/net/DatagramSocket")) { Kategorie_CODE = 15; 유효길이 = 3; }
        if (Word_SMS(Numm_Konstant, "java/net/DatagramPacket")) { Kategorie_CODE = 16; 유효길이 = 4; }
        if (Word_SMS(Numm_Konstant, "java/lang/Thread") || Word_SMS(Numm_Konstant, "한국어/자체/작업가닥")) { Kategorie_CODE = 13; 유효길이 = 2; }
        if (Word_SMS(Numm_Konstant, "java/lang/Object")) { Kategorie_CODE = 8; }
        if (Kategorie_CODE == 0 && 화면종(Numm_Konstant) != 0) { Kategorie_CODE = 화면종(Numm_Konstant); 유효길이 = 12; }
        if (Kategorie_CODE == 0) {
            int Zeechecode = FIND_Klass_Definitioun(Numm_Konstant); if (Zeechecode < 0 || Feeler || !initialiséieren(Zeechecode, 시작점)) return;
            Kategorie_CODE = 32 + Zeechecode; 유효길이 = Klass_Slot_COUNT[Zeechecode];
        }
        int Objet_Referenzen = zouweisen_Späicher(Kategorie_CODE, 유효길이); if (Feeler) return;
        if (Kategorie_CODE == 13 && Word_SMS(Numm_Konstant, "한국어/자체/작업가닥")) 힙[Objet_Referenzen + 3] = 1;
        if (Kategorie_CODE >= 24 && Kategorie_CODE <= 28 && 한국어화면종(Numm_Konstant) != 0) 힙[Objet_Referenzen + 13] = 1;
        if (Kategorie_CODE == 5 || Kategorie_CODE == 6 || Kategorie_CODE == 15 || Kategorie_CODE == 17 || Kategorie_CODE == 18) 힙[Objet_Referenzen + 2] = -1;
        if (Kategorie_CODE == 9) 힙[Objet_Referenzen + 2] = 예외참조;
        넣기(Objet_Referenzen, 2);
    }
    static boolean 값같음(int 첫값, int Byte_Daten) {
        if (첫값 == Byte_Daten) return true;
        if (첫값 == 0 || Byte_Daten == 0 || 첫값 < 0 || Byte_Daten < 0 || 첫값 >= 힙끝 || Byte_Daten >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[Byte_Daten] == 1) return 글같음(첫값, Byte_Daten, false);
        return 힙[첫값] == 12 && 힙[Byte_Daten] == 12 && 힙[첫값 + 2] == 힙[Byte_Daten + 2];
    }
    static int 글조각(int Objet_Referenzen, int Start_positionéieren, int bëennegen_positionéieren) {
        if (!Objet_VALUE(Objet_Referenzen, 1)) return 0;
        if (Start_positionéieren < 0 || bëennegen_positionéieren < Start_positionéieren || bëennegen_positionéieren > 힙[Objet_Referenzen + 1]) { Feeler_VALUE("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = zouweisen_Späicher(1, bëennegen_positionéieren - Start_positionéieren); if (Feeler) return 0;
        for (int Loop_INDEX = Start_positionéieren; Loop_INDEX < bëennegen_positionéieren; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX - Start_positionéieren] = 힙[Objet_Referenzen + 2 + Loop_INDEX];
        return 반환값;
    }
    static int bäitrieden_SMS(int 첫값, int Byte_Daten) {
        if (!Objet_VALUE(첫값, 1) || !Objet_VALUE(Byte_Daten, 1)) return 0;
        int Agab_COUNT = 힙[첫값 + 1], Method_INDEX = 힙[Byte_Daten + 1], 반환값 = zouweisen_Späicher(1, Agab_COUNT + Method_INDEX); if (Feeler) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Agab_COUNT; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 힙[첫값 + 2 + Loop_INDEX];
        for (int Loop_INDEX = 0; Loop_INDEX < Method_INDEX; Loop_INDEX++) 힙[반환값 + 2 + Agab_COUNT + Loop_INDEX] = 힙[Byte_Daten + 2 + Loop_INDEX];
        return 반환값;
    }
    static boolean 기본호출(int Besëtzer, int Numm_Konstant, int 서술상수, int Befeel_CODE) {
        if (Word_SMS(Besëtzer, "한국어/자체/실행인수") && Befeel_CODE == 184) {
            if (Word_SMS(Numm_Konstant, "Element_COUNT") && Word_SMS(서술상수, "()I")) { 넣기(Benotzer.인수개수() - 1, 1); return true; }
            if (Word_SMS(Numm_Konstant, "SMS") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= Benotzer.인수개수() - 1) 예외던짐(29, "ausféieren_Befeel 인수 범위를 벗어났습니다");
                else 넣기(Host_Zeechen(Benotzer.인수(순번 + 1)), 2);
                return true;
            }
            Feeler_VALUE("지원하지 않는 한국어 ausféieren_Befeel 인수 호출"); return true;
        }
        if (Word_SMS(Besëtzer, "한국어/자체/작업가닥")) { Prozess_Thread(Numm_Konstant, 서술상수, Befeel_CODE, true); return true; }
        if (한국어화면소유(Besëtzer)) { 한국어화면호출(Besëtzer, Numm_Konstant, 서술상수, Befeel_CODE); return true; }
        if (화면소유(Besëtzer)) { 화면호출(Besëtzer, Numm_Konstant, 서술상수, Befeel_CODE); return true; }
        if (Word_SMS(Besëtzer, "java/net/Socket") || Word_SMS(Besëtzer, "java/net/ServerSocket") || Word_SMS(Besëtzer, "java/io/InputStream") || Word_SMS(Besëtzer, "java/io/OutputStream")) { 흐름호출(Besëtzer, Numm_Konstant, 서술상수, Befeel_CODE); return true; }
        if (Word_SMS(Besëtzer, "한국어/자체/Kernel_VALUE") && Befeel_CODE == 184) {
            if (Word_SMS(Numm_Konstant, "화면너비") && Word_SMS(서술상수, "()I")) { 넣기(Benotzer.화면너비(), 1); return true; }
            if (Word_SMS(Numm_Konstant, "화면높이") && Word_SMS(서술상수, "()I")) { 넣기(Benotzer.화면높이(), 1); return true; }
            if (Word_SMS(Numm_Konstant, "밀리초") && Word_SMS(서술상수, "()I")) { 넣기(Benotzer.밀리초(), 1); return true; }
            if (Word_SMS(Numm_Konstant, "그림대기") && Word_SMS(서술상수, "()I")) { 넣기(Benotzer.그림대기(), 1); return true; }
            if (Word_SMS(Numm_Konstant, "사각형") && Word_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), X_Koordinat = 빼기(1); 넣기(Benotzer.사각형(X_Koordinat, 세로좌표, 너비, 높이, 색상), 1); return true; }
        }
        if (Word_SMS(Besëtzer, "java/net/InetAddress") || Word_SMS(Besëtzer, "java/net/DatagramPacket") || Word_SMS(Besëtzer, "java/net/DatagramSocket")) { 통신호출(Besëtzer, Numm_Konstant, 서술상수, Befeel_CODE); return true; }
        if (Word_SMS(Besëtzer, "java/lang/Thread")) { 가닥호출(Numm_Konstant, 서술상수, Befeel_CODE); return true; }
        if (Word_SMS(Besëtzer, "java/lang/Object")) {
            if (Word_SMS(Numm_Konstant, "<init>") && Word_SMS(서술상수, "()V") && Befeel_CODE == 183) { 객체유효(빼기(2)); return true; }
            if (Word_SMS(Numm_Konstant, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int Byte_Daten = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == Byte_Daten ? 1 : 0, 1); return true; }
        }
        if (예외상수(Besëtzer) != 0) {
            if (Word_SMS(Numm_Konstant, "<init>") && Befeel_CODE == 183 && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int Prompt = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), Objet_Referenzen = 빼기(2);
                if (Objet_VALUE(Objet_Referenzen, 9)) { 힙[Objet_Referenzen + 3] = Prompt; 힙참조[Objet_Referenzen + 3] = 1; } return true;
            }
            if ((Word_SMS(Numm_Konstant, "getMessage") || Word_SMS(Numm_Konstant, "설명")) && Word_SMS(서술상수, "()Ljava/lang/String;")) { int Objet_Referenzen = 빼기(2); if (Objet_VALUE(Objet_Referenzen, 9)) 넣기(힙[Objet_Referenzen + 3], 2); return true; }
        }
        if (Word_SMS(Besëtzer, "java/lang/String")) {
            if (Befeel_CODE == 182 && Word_SMS(Numm_Konstant, "getBytes") && (Word_SMS(서술상수, "()[B") || Word_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int Codéierung_Numm = Word_SMS(서술상수, "()[B") ? 0 : 빼기(2), Objet_Referenzen = 빼기(2);
                if (!Objet_VALUE(Objet_Referenzen, 1)) return true;
                if (Codéierung_Numm != 0 && !글같음(Codéierung_Numm, Host_Zeechen("UTF-8"), false) && !글같음(Codéierung_Numm, Host_Zeechen("UTF8"), false) && !글같음(Codéierung_Numm, Host_Zeechen("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int Agab_COUNT = 힙[Objet_Referenzen + 1], 반환값 = zouweisen_Späicher(20, Agab_COUNT * 3), 사용수 = 0; if (Feeler) return true;
                for (int intern_Verknëppung_positionéieren = 0; intern_Verknëppung_positionéieren < Agab_COUNT; intern_Verknëppung_positionéieren++) {
                    int Zeechecode = 힙[Objet_Referenzen + 2 + intern_Verknëppung_positionéieren];
                    if (Zeechecode >= 0xd800 && Zeechecode <= 0xdbff && intern_Verknëppung_positionéieren + 1 < Agab_COUNT && 힙[Objet_Referenzen + 3 + intern_Verknëppung_positionéieren] >= 0xdc00 && 힙[Objet_Referenzen + 3 + intern_Verknëppung_positionéieren] <= 0xdfff) Zeechecode = 0x10000 + ((Zeechecode - 0xd800) << 10) + 힙[Objet_Referenzen + 2 + ++intern_Verknëppung_positionéieren] - 0xdc00;
                    else if (Zeechecode >= 0xd800 && Zeechecode <= 0xdfff) Zeechecode = '?';
                    if (Zeechecode < 128) 힙[반환값 + 2 + 사용수++] = Zeechecode;
                    else { int Byte_COUNT = Zeechecode < 2048 ? 2 : Zeechecode < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((Byte_COUNT == 2 ? 192 : Byte_COUNT == 3 ? 224 : 240) | Zeechecode >> (6 * (Byte_COUNT - 1))); for (int 비교자리 = Byte_COUNT - 1; 비교자리 > 0; 비교자리--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | Zeechecode >> (6 * (비교자리 - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (Befeel_CODE == 184 && Word_SMS(Numm_Konstant, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(Ziffer_Zeechen(빼기(1)), 2); return true; }
            if (Befeel_CODE != 182) return false;
            if (Word_SMS(Numm_Konstant, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int Byte_Daten = 빼기(2), 첫값 = 빼기(2); if (Objet_VALUE(첫값, 1)) 넣기(글같음(첫값, Byte_Daten, false) ? 1 : 0, 1); return true; }
            if (Word_SMS(Numm_Konstant, "isEmpty") && Word_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (Objet_VALUE(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_SMS(Numm_Konstant, "substring") && (Word_SMS(서술상수, "(I)Ljava/lang/String;") || Word_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SECOND_VALUE = Word_SMS(서술상수, "(II)Ljava/lang/String;"); int bëennegen_positionéieren = SECOND_VALUE ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (Objet_VALUE(첫값, 1)) 넣기(글조각(첫값, 시작점, SECOND_VALUE ? bëennegen_positionéieren : 힙[첫값 + 1]), 2); return true;
            }
            if (Word_SMS(Numm_Konstant, "concat") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int Byte_Daten = 빼기(2), 첫값 = 빼기(2); 넣기(bäitrieden_SMS(첫값, Byte_Daten), 2); return true; }
            if (Word_SMS(Numm_Konstant, "hashCode") && Word_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), Hash_VALUE = 0; if (Objet_VALUE(첫값, 1)) { for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) Hash_VALUE = Hash_VALUE * 31 + 힙[첫값 + 2 + Loop_INDEX]; 넣기(Hash_VALUE, 1); } return true; }
            if (Word_SMS(Numm_Konstant, "toString") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (Objet_VALUE(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_SMS(Besëtzer, "java/lang/Integer")) {
            if (Befeel_CODE == 184 && Word_SMS(Numm_Konstant, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int Daten_VALUE = 빼기(1), Objet_Referenzen = Daten_VALUE >= -128 && Daten_VALUE <= 127 ? Store_Ganzzuel[Daten_VALUE + 128] : 0; if (Objet_Referenzen == 0) { Objet_Referenzen = zouweisen_Späicher(12, 1); if (!Feeler) { 힙[Objet_Referenzen + 2] = Daten_VALUE; if (Daten_VALUE >= -128 && Daten_VALUE <= 127) Store_Ganzzuel[Daten_VALUE + 128] = Objet_Referenzen; } } 넣기(Objet_Referenzen, 2); return true; }
            if (Befeel_CODE == 183 && Word_SMS(Numm_Konstant, "<init>") && Word_SMS(서술상수, "(I)V")) { int Daten_VALUE = 빼기(1), Objet_Referenzen = 빼기(2); if (Objet_VALUE(Objet_Referenzen, 12)) 힙[Objet_Referenzen + 2] = Daten_VALUE; return true; }
            if (Befeel_CODE == 182 && Word_SMS(Numm_Konstant, "intValue") && Word_SMS(서술상수, "()I")) { int Objet_Referenzen = 빼기(2); if (Objet_VALUE(Objet_Referenzen, 12)) 넣기(힙[Objet_Referenzen + 2], 1); return true; }
            if (Befeel_CODE == 184 && Word_SMS(Numm_Konstant, "toString") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(Ziffer_Zeechen(빼기(1)), 2); return true; }
        }
        if (Word_SMS(Besëtzer, "java/lang/Math") && Befeel_CODE == 184) {
            if (Word_SMS(Numm_Konstant, "abs") && Word_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_SMS(Numm_Konstant, "min") || Word_SMS(Numm_Konstant, "max")) && Word_SMS(서술상수, "(II)I")) { int Byte_Daten = 빼기(1), 첫값 = 빼기(1); 넣기(Word_SMS(Numm_Konstant, "min") ? (첫값 < Byte_Daten ? 첫값 : Byte_Daten) : (첫값 > Byte_Daten ? 첫값 : Byte_Daten), 1); return true; }
        }
        if (Word_SMS(Besëtzer, "java/lang/System") && Befeel_CODE == 184) {
            if (Word_SMS(Numm_Konstant, "gc") && Word_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Word_SMS(Numm_Konstant, "arraycopy") && Word_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int Agab_COUNT = 빼기(1), Zil_VALUE_INDEX = 빼기(1), Byte_Daten = 빼기(2), Start_positionéieren = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(Byte_Daten)) {
                    int Kategorie_CODE = 힙[첫값];
                    if (힙[Byte_Daten] != Kategorie_CODE || (Kategorie_CODE != 2 && Kategorie_CODE != 3 && (Kategorie_CODE < 20 || Kategorie_CODE > 23))) Feeler_VALUE("arraycopy type mismatch");
                    else if (Agab_COUNT < 0 || Start_positionéieren < 0 || Zil_VALUE_INDEX < 0 || Start_positionéieren > 힙[첫값 + 1] - Agab_COUNT || Zil_VALUE_INDEX > 힙[Byte_Daten + 1] - Agab_COUNT) Feeler_VALUE("ArrayIndexOutOfBoundsException");
                    else if (첫값 == Byte_Daten && Zil_VALUE_INDEX > Start_positionéieren) { for (int Loop_INDEX = Agab_COUNT - 1; Loop_INDEX >= 0; Loop_INDEX--) 힙[Byte_Daten + 2 + Zil_VALUE_INDEX + Loop_INDEX] = 힙[첫값 + 2 + Start_positionéieren + Loop_INDEX]; }
                    else { for (int Loop_INDEX = 0; Loop_INDEX < Agab_COUNT && !Feeler; Loop_INDEX++) { int Daten_VALUE = 힙[첫값 + 2 + Start_positionéieren + Loop_INDEX]; if (Kategorie_CODE != 3 || 배열저장가능(Byte_Daten, Daten_VALUE)) 힙[Byte_Daten + 2 + Zil_VALUE_INDEX + Loop_INDEX] = Daten_VALUE; } }
                }
                return true;
            }
        }
        if (Word_SMS(Besëtzer, "java/util/ArrayList") || Word_SMS(Besëtzer, "java/util/List") || Word_SMS(Besëtzer, "java/util/HashMap") || Word_SMS(Besëtzer, "java/util/Map")) {
            모음호출(Besëtzer, Numm_Konstant, 서술상수, Befeel_CODE); return true;
        }
        return false;
    }
    static void 모음늘리기(int Objet_Referenzen, int 필요수) {
        int 이전값 = 힙[Objet_Referenzen + 2], 용량값 = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (용량값 >= 필요수) return;
        int Weider_positionéieren = 용량값 < 8 ? 8 : 용량값 * 2; if (Weider_positionéieren < 필요수) Weider_positionéieren = 필요수;
        int Daten_ARRAY = zouweisen_Späicher(3, Weider_positionéieren); if (Feeler) return;
        for (int Loop_INDEX = 0; Loop_INDEX < 용량값; Loop_INDEX++) 힙[Daten_ARRAY + 2 + Loop_INDEX] = 힙[이전값 + 2 + Loop_INDEX];
        힙[Objet_Referenzen + 2] = Daten_ARRAY; 힙참조[Objet_Referenzen + 2] = 1;
    }
    static void 모음호출(int Besëtzer, int Numm_Konstant, int 서술상수, int Befeel_CODE) {
        boolean 대응참조 = Word_SMS(Besëtzer, "java/util/HashMap") || Word_SMS(Besëtzer, "java/util/Map"); int Kategorie_CODE = 대응참조 ? 11 : 10;
        if (Word_SMS(Numm_Konstant, "<init>") && Befeel_CODE == 183 && Word_SMS(서술상수, "()V")) { int Objet_Referenzen = 빼기(2); if (Objet_VALUE(Objet_Referenzen, Kategorie_CODE)) 모음늘리기(Objet_Referenzen, 8); return; }
        if (Befeel_CODE != 182 && Befeel_CODE != 185) { Feeler_VALUE("invalid collection invocation"); return; }
        if (Word_SMS(Numm_Konstant, "size") && Word_SMS(서술상수, "()I") || Word_SMS(Numm_Konstant, "isEmpty") && Word_SMS(서술상수, "()Z")) {
            int Objet_Referenzen = 빼기(2); if (Objet_VALUE(Objet_Referenzen, Kategorie_CODE)) 넣기(Word_SMS(Numm_Konstant, "size") ? 힙[Objet_Referenzen + 3] : 힙[Objet_Referenzen + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_SMS(Numm_Konstant, "clear") && Word_SMS(서술상수, "()V")) { int Objet_Referenzen = 빼기(2); if (Objet_VALUE(Objet_Referenzen, Kategorie_CODE)) { int Daten_ARRAY = 힙[Objet_Referenzen + 2]; for (int Loop_INDEX = 0; Loop_INDEX < 힙[Daten_ARRAY + 1]; Loop_INDEX++) 힙[Daten_ARRAY + 2 + Loop_INDEX] = 0; 힙[Objet_Referenzen + 3] = 0; } return; }
        if (!대응참조 && Word_SMS(Numm_Konstant, "add") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int Daten_VALUE = 빼기(2), Objet_Referenzen = 빼기(2); if (!Objet_VALUE(Objet_Referenzen, 10)) return;
            int Agab_COUNT = 힙[Objet_Referenzen + 3]; 모음늘리기(Objet_Referenzen, Agab_COUNT + 1); if (!Feeler) { 힙[힙[Objet_Referenzen + 2] + 2 + Agab_COUNT] = Daten_VALUE; 힙[Objet_Referenzen + 3] = Agab_COUNT + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_SMS(Numm_Konstant, "get") || Word_SMS(Numm_Konstant, "remove")) && Word_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Word_SMS(Numm_Konstant, "set") && Word_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = Word_SMS(Numm_Konstant, "set"); int Daten_VALUE = 지정여부 ? 빼기(2) : 0, Agab_positionéieren = 빼기(1), Objet_Referenzen = 빼기(2);
            if (!Objet_VALUE(Objet_Referenzen, 10)) return;
            int Agab_COUNT = 힙[Objet_Referenzen + 3], Daten_ARRAY = 힙[Objet_Referenzen + 2];
            if (Agab_positionéieren < 0 || Agab_positionéieren >= Agab_COUNT) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[Daten_ARRAY + 2 + Agab_positionéieren];
            if (지정여부) 힙[Daten_ARRAY + 2 + Agab_positionéieren] = Daten_VALUE;
            if (Word_SMS(Numm_Konstant, "remove")) { for (int Loop_INDEX = Agab_positionéieren + 1; Loop_INDEX < Agab_COUNT; Loop_INDEX++) 힙[Daten_ARRAY + 1 + Loop_INDEX] = 힙[Daten_ARRAY + 2 + Loop_INDEX]; 힙[Daten_ARRAY + 1 + Agab_COUNT] = 0; 힙[Objet_Referenzen + 3] = Agab_COUNT - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Word_SMS(Numm_Konstant, "get") || Word_SMS(Numm_Konstant, "remove")) && Word_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(Numm_Konstant, "put") && Word_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(Numm_Konstant, "containsKey") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_SMS(Numm_Konstant, "put"), ewechhuelen = Word_SMS(Numm_Konstant, "remove");
            int Daten_VALUE = 넣기여부 ? 빼기(2) : 0, Tast_Referenzen = 빼기(2), Objet_Referenzen = 빼기(2); if (!Objet_VALUE(Objet_Referenzen, 11)) return;
            int Agab_COUNT = 힙[Objet_Referenzen + 3], Daten_ARRAY = 힙[Objet_Referenzen + 2], 찾은여부 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < Agab_COUNT; Loop_INDEX++) if (값같음(Tast_Referenzen, 힙[Daten_ARRAY + 2 + 2 * Loop_INDEX])) { 찾은여부 = Loop_INDEX; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[Daten_ARRAY + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(Objet_Referenzen, (Agab_COUNT + 1) * 2); Daten_ARRAY = 힙[Objet_Referenzen + 2]; 찾은여부 = Agab_COUNT; if (!Feeler) 힙[Objet_Referenzen + 3] = Agab_COUNT + 1; }
                if (!Feeler) { 힙[Daten_ARRAY + 2 + 2 * 찾은여부] = Tast_Referenzen; 힙[Daten_ARRAY + 3 + 2 * 찾은여부] = Daten_VALUE; }
            }
            if (ewechhuelen && 찾은여부 >= 0) { for (int Loop_INDEX = 찾은여부 + 1; Loop_INDEX < Agab_COUNT; Loop_INDEX++) { 힙[Daten_ARRAY + 2 * Loop_INDEX] = 힙[Daten_ARRAY + 2 + 2 * Loop_INDEX]; 힙[Daten_ARRAY + 1 + 2 * Loop_INDEX] = 힙[Daten_ARRAY + 3 + 2 * Loop_INDEX]; } 힙[Daten_ARRAY + 2 * Agab_COUNT] = 0; 힙[Daten_ARRAY + 1 + 2 * Agab_COUNT] = 0; 힙[Objet_Referenzen + 3] = Agab_COUNT - 1; }
            if (Word_SMS(Numm_Konstant, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        Feeler_VALUE("unsupported collection method");
    }
    static boolean 잠금얻기(int Objet_Referenzen) {
        if (!객체유효(Objet_Referenzen)) return false;
        if (잠금깊이[Objet_Referenzen] != 0 && 잠금주인[Objet_Referenzen] != 현재가닥 + 1) { 바꿈요청 = true; return false; }
        잠금주인[Objet_Referenzen] = 현재가닥 + 1; 잠금깊이[Objet_Referenzen]++; return true;
    }
    static void 잠금풀기(int Objet_Referenzen) {
        if (!객체유효(Objet_Referenzen)) return;
        if (잠금깊이[Objet_Referenzen] == 0 || 잠금주인[Objet_Referenzen] != 현재가닥 + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[Objet_Referenzen] == 0) 잠금주인[Objet_Referenzen] = 0;
    }
    static boolean SWITCH_Thread() {
        Thread_Rumm[현재가닥] = Rumm_INDEX;
        if (Rumm_INDEX < 현재가닥 * 32) Thread_Status[현재가닥] = 3;
        for (int Loop_INDEX = 0; Loop_INDEX < Thread_COUNT; Loop_INDEX++) if (Thread_Status[Loop_INDEX] == 2 && Thread_Status[가닥대기[Loop_INDEX]] == 3) Thread_Status[Loop_INDEX] = 1;
        for (int Loop_INDEX = 1; Loop_INDEX <= Thread_COUNT; Loop_INDEX++) {
            int Weider_positionéieren = (현재가닥 + Loop_INDEX) % Thread_COUNT;
            if (Thread_Status[Weider_positionéieren] == 1) { 현재가닥 = Weider_positionéieren; Rumm_INDEX = Thread_Rumm[Weider_positionéieren]; 바꿈요청 = false; return true; }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < Thread_COUNT; Loop_INDEX++) if (Thread_Status[Loop_INDEX] != 3) { Feeler_VALUE("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int Numm_Konstant, int 서술상수, int Befeel_CODE) { Prozess_Thread(Numm_Konstant, 서술상수, Befeel_CODE, false); }
    static void Prozess_Thread(int Numm_Konstant, int 서술상수, int Befeel_CODE, boolean 한국어) {
        if (Befeel_CODE == 184 && Word_SMS(Numm_Konstant, 한국어 ? "YIELD_To_do" : "yield") && Word_SMS(서술상수, "()V")) { 바꿈요청 = true; return; }
        if (Befeel_CODE == 184 && Word_SMS(Numm_Konstant, "currentThread") && Word_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(Thread_Objet[현재가닥], 2); return; }
        if (Befeel_CODE == 183 && Word_SMS(Numm_Konstant, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, 한국어 ? "(L한국어/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int Zil_Adress = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), Objet_Referenzen = 빼기(2);
            if (!객체유효(Objet_Referenzen)) return;
            if (힙[Objet_Referenzen] == 13) { 힙[Objet_Referenzen + 2] = Zil_Adress; 힙참조[Objet_Referenzen + 2] = 1; }
            else if (Zil_Adress != 0) Feeler_VALUE("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (Befeel_CODE == 182 && (Word_SMS(Numm_Konstant, 한국어 ? "Start_To_do" : "start") || Word_SMS(Numm_Konstant, 한국어 ? "기다리기" : "join")) && Word_SMS(서술상수, "()V") || Befeel_CODE == 182 && Word_SMS(Numm_Konstant, 한국어 ? "살아있는가" : "isAlive") && Word_SMS(서술상수, "()Z")) {
            int Objet_Referenzen = 빼기(2); if (!객체유효(Objet_Referenzen)) return;
            int Kont_VALUE = -1; for (int Loop_INDEX = 0; Loop_INDEX < Thread_COUNT; Loop_INDEX++) if (Thread_Objet[Loop_INDEX] == Objet_Referenzen) Kont_VALUE = Loop_INDEX;
            if (Word_SMS(Numm_Konstant, 한국어 ? "살아있는가" : "isAlive")) { 넣기(Kont_VALUE >= 0 && Thread_Status[Kont_VALUE] != 3 ? 1 : 0, 1); return; }
            if (Word_SMS(Numm_Konstant, 한국어 ? "기다리기" : "join")) { if (Kont_VALUE >= 0 && Thread_Status[Kont_VALUE] != 3) { 가닥대기[현재가닥] = Kont_VALUE; Thread_Status[현재가닥] = 2; 바꿈요청 = true; } return; }
            if (Kont_VALUE >= 0) { 예외던짐(한국어 ? 38 : 16, "thread already started"); return; }
            if (Thread_COUNT == 4) { Feeler_VALUE("thread limit (4 including main)"); return; }
            int Zil_Adress = 힙[Objet_Referenzen] == 13 ? 힙[Objet_Referenzen + 2] : Objet_Referenzen;
            int Fichier_INDEX = Zil_Adress > 0 && 힙[Zil_Adress] >= 32 ? Numm_Method(힙[Zil_Adress] - 32, 한국어 ? "Ausféieren" : "run", "()V") : -1;
            if (Zil_Adress != 0 && Fichier_INDEX < 0) { Feeler_VALUE("Runnable.run required"); return; }
            Kont_VALUE = Thread_COUNT++; Thread_Objet[Kont_VALUE] = Objet_Referenzen; Thread_Zil[Kont_VALUE] = Zil_Adress;
            int Rumm = Kont_VALUE * 32; Thread_Rumm[Kont_VALUE] = Fichier_INDEX < 0 ? Rumm - 1 : Rumm; Thread_Status[Kont_VALUE] = Fichier_INDEX < 0 ? 3 : 1;
            if (Fichier_INDEX >= 0) { Rumm_Method[Rumm] = Fichier_INDEX; Rumm_positionéieren[Rumm] = Method_Start[Fichier_INDEX]; lokal_VALUE[Rumm * 128] = Zil_Adress; lokal_TYPE[Rumm * 128] = 2; }
            return;
        }
        Feeler_VALUE("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], Adress_SMS = new int[16];
    static int lokal_Adress() { return Adress_Objet(0x7f000001); }
    static int Adress_Objet(int VALUE) { int Objet_Referenzen = zouweisen_Späicher(14, 1); if (!Feeler) 힙[Objet_Referenzen + 2] = VALUE; return Objet_Referenzen; }
    static int 주소해독(int Objet_Referenzen) {
        if (Objet_Referenzen == 0 || 글같음(Objet_Referenzen, Host_Zeechen("localhost"), false)) return 0x7f000001;
        if (!Objet_VALUE(Objet_Referenzen, 1)) return 0;
        int Daten_VALUE = 0, 총수 = 0, Adress_Byte = 0, 자릿수 = 0, Agab_COUNT = 힙[Objet_Referenzen + 1];
        for (int Loop_INDEX = 0; Loop_INDEX <= Agab_COUNT; Loop_INDEX++) {
            int Zeechecode = Loop_INDEX == Agab_COUNT ? '.' : 힙[Objet_Referenzen + 2 + Loop_INDEX];
            if (Zeechecode == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } Daten_VALUE = Daten_VALUE << 8 | Adress_Byte; 총수++; Adress_Byte = 자릿수 = 0; }
            else { if (Zeechecode < '0' || Zeechecode > '9' || ++자릿수 > 3 || (Adress_Byte = Adress_Byte * 10 + Zeechecode - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return Daten_VALUE;
    }
    static int Adress_Zeechen(int Daten_VALUE) {
        int Agab_COUNT = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int Adress_Byte = Daten_VALUE >>> 이동비트 & 255;
            if (Adress_Byte >= 100) Adress_SMS[Agab_COUNT++] = '0' + Adress_Byte / 100;
            if (Adress_Byte >= 10) Adress_SMS[Agab_COUNT++] = '0' + Adress_Byte / 10 % 10;
            Adress_SMS[Agab_COUNT++] = '0' + Adress_Byte % 10; if (이동비트 != 0) Adress_SMS[Agab_COUNT++] = '.';
        }
        int Objet_Referenzen = zouweisen_Späicher(1, Agab_COUNT); if (!Feeler) for (int Loop_INDEX = 0; Loop_INDEX < Agab_COUNT; Loop_INDEX++) 힙[Objet_Referenzen + 2 + Loop_INDEX] = Adress_SMS[Loop_INDEX]; return Objet_Referenzen;
    }
    static void 통신호출(int Besëtzer, int Numm_Konstant, int 서술상수, int Befeel_CODE) {
        if (Word_SMS(Besëtzer, "java/net/InetAddress")) {
            if (Befeel_CODE == 184 && Word_SMS(Numm_Konstant, "getLoopbackAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(lokal_Adress(), 2); return; }
            if (Befeel_CODE == 184 && Word_SMS(Numm_Konstant, "getByName") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int Daten_VALUE = 주소해독(빼기(2)); if (던진객체 == 0 && !Feeler) 넣기(Adress_Objet(Daten_VALUE), 2); return;
            }
            if (Befeel_CODE == 182 && Word_SMS(Numm_Konstant, "getHostAddress") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int Objet_Referenzen = 빼기(2); if (Objet_VALUE(Objet_Referenzen, 14)) 넣기(Adress_Zeechen(힙[Objet_Referenzen + 2]), 2); return; }
        }
        if (Word_SMS(Besëtzer, "java/net/DatagramPacket")) {
            if (Befeel_CODE == 183 && Word_SMS(Numm_Konstant, "<init>") && (Word_SMS(서술상수, "([BI)V") || Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean Zil_VALUE_Referenzen = Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int 접속번호 = Zil_VALUE_Referenzen ? 빼기(1) : 0, Adress_Referenzen = Zil_VALUE_Referenzen ? 빼기(2) : 0;
                int Agab_COUNT = 빼기(1), Daten_ARRAY = 빼기(2), Objet_Referenzen = 빼기(2);
                if (!Objet_VALUE(Objet_Referenzen, 16) || !Objet_VALUE(Daten_ARRAY, 20)) return;
                if (Agab_COUNT < 0 || Agab_COUNT > 힙[Daten_ARRAY + 1] || 접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (Adress_Referenzen != 0 && !Objet_VALUE(Adress_Referenzen, 14)) return;
                힙[Objet_Referenzen + 2] = Daten_ARRAY; 힙참조[Objet_Referenzen + 2] = 1; 힙[Objet_Referenzen + 3] = Agab_COUNT;
                힙[Objet_Referenzen + 4] = Adress_Referenzen; 힙참조[Objet_Referenzen + 4] = 1; 힙[Objet_Referenzen + 5] = 접속번호; return;
            }
            if (Befeel_CODE == 182 && Word_SMS(Numm_Konstant, "setLength") && Word_SMS(서술상수, "(I)V")) {
                int Agab_COUNT = 빼기(1), Objet_Referenzen = 빼기(2); if (!Objet_VALUE(Objet_Referenzen, 16)) return;
                if (Agab_COUNT < 0 || Agab_COUNT > 힙[힙[Objet_Referenzen + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[Objet_Referenzen + 3] = Agab_COUNT; return;
            }
            if (Befeel_CODE == 182 && (Word_SMS(Numm_Konstant, "getData") && Word_SMS(서술상수, "()[B") || Word_SMS(Numm_Konstant, "getLength") && Word_SMS(서술상수, "()I") || Word_SMS(Numm_Konstant, "getAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;") || Word_SMS(Numm_Konstant, "getPort") && Word_SMS(서술상수, "()I"))) {
                int Objet_Referenzen = 빼기(2); if (!Objet_VALUE(Objet_Referenzen, 16)) return;
                int Agab_positionéieren = Word_SMS(Numm_Konstant, "getData") ? 2 : Word_SMS(Numm_Konstant, "getLength") ? 3 : Word_SMS(Numm_Konstant, "getAddress") ? 4 : 5;
                넣기(힙[Objet_Referenzen + Agab_positionéieren], Agab_positionéieren == 2 || Agab_positionéieren == 4 ? 2 : 1); return;
            }
        }
        if (Word_SMS(Besëtzer, "java/net/DatagramSocket")) {
            if (Befeel_CODE == 183 && Word_SMS(Numm_Konstant, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(I)V"))) {
                int 접속번호 = Word_SMS(서술상수, "()V") ? 0 : 빼기(1), Objet_Referenzen = 빼기(2); if (!Objet_VALUE(Objet_Referenzen, 15)) return;
                if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = Benotzer.ariichten_Reseau(접속번호); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[Objet_Referenzen + 2] = 열린파일번호; return;
            }
            if (Befeel_CODE == 182 && Word_SMS(Numm_Konstant, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), Objet_Referenzen = 빼기(2); if (!Objet_VALUE(Objet_Referenzen, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[Objet_Referenzen + 3] = 밀리초값; return;
            }
            if (Befeel_CODE == 182 && Word_SMS(Numm_Konstant, "getLocalPort") && Word_SMS(서술상수, "()I")) { int Objet_Referenzen = 빼기(2); if (Objet_VALUE(Objet_Referenzen, 15)) 넣기(힙[Objet_Referenzen + 2] < 0 ? -1 : Benotzer.Reseau_Port(힙[Objet_Referenzen + 2]), 1); return; }
            if (Befeel_CODE == 182 && Word_SMS(Numm_Konstant, "isClosed") && Word_SMS(서술상수, "()Z")) { int Objet_Referenzen = 빼기(2); if (Objet_VALUE(Objet_Referenzen, 15)) 넣기(힙[Objet_Referenzen + 2] < 0 ? 1 : 0, 1); return; }
            if (Befeel_CODE == 182 && Word_SMS(Numm_Konstant, "close") && Word_SMS(서술상수, "()V")) { int Objet_Referenzen = 빼기(2); if (Objet_VALUE(Objet_Referenzen, 15) && 힙[Objet_Referenzen + 2] >= 0) { Benotzer.파일서술자닫기(힙[Objet_Referenzen + 2]); 힙[Objet_Referenzen + 2] = -1; } return; }
            if (Befeel_CODE == 182 && (Word_SMS(Numm_Konstant, "send") || Word_SMS(Numm_Konstant, "receive")) && Word_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int Pak = 빼기(2), Objet_Referenzen = 빼기(2); if (!Objet_VALUE(Pak, 16) || !Objet_VALUE(Objet_Referenzen, 15)) return;
                int Daten_ARRAY = 힙[Pak + 2], 유효길이 = 힙[Pak + 3], 열린파일번호 = 힙[Objet_Referenzen + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_SMS(Numm_Konstant, "send")) {
                    if (!Objet_VALUE(힙[Pak + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < 유효길이; Loop_INDEX++) 통신임시[Loop_INDEX] = 힙[Daten_ARRAY + 2 + Loop_INDEX];
                    if (Benotzer.mailen_Reseau(열린파일번호, 힙[힙[Pak + 4] + 2], 힙[Pak + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int Agab_COUNT = Benotzer.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (Agab_COUNT == -11) {
                        int 현재시각 = Benotzer.밀리초();
                        if (힙[Objet_Referenzen + 4] == 0) 힙[Objet_Referenzen + 4] = 현재시각 + 1;
                        if (힙[Objet_Referenzen + 3] > 0 && 현재시각 - (힙[Objet_Referenzen + 4] - 1) >= 힙[Objet_Referenzen + 3]) { 힙[Objet_Referenzen + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(Objet_Referenzen, 2); 넣기(Pak, 2); Rumm_positionéieren[Rumm_INDEX] = Rumm_Instruktioun[Rumm_INDEX]; 바꿈요청 = true; return;
                    }
                    힙[Objet_Referenzen + 4] = 0;
                    if (Agab_COUNT < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < Agab_COUNT; Loop_INDEX++) 힙[Daten_ARRAY + 2 + Loop_INDEX] = (byte)통신임시[Loop_INDEX];
                    힙[Pak + 3] = Agab_COUNT; 힙[Pak + 4] = Adress_Objet(통신임시[513]); 힙참조[Pak + 4] = 1; 힙[Pak + 5] = 통신임시[512];
                }
                return;
            }
        }
        Feeler_VALUE("unsupported java.net method");
    }
    static boolean 흐름대기(int Objet_Referenzen) {
        int 현재시각 = Benotzer.밀리초();
        if (힙[Objet_Referenzen + 5] == 0) 힙[Objet_Referenzen + 5] = 현재시각 + 1;
        if (힙[Objet_Referenzen + 3] > 0 && 현재시각 - (힙[Objet_Referenzen + 5] - 1) >= 힙[Objet_Referenzen + 3]) { 힙[Objet_Referenzen + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        Rumm_positionéieren[Rumm_INDEX] = Rumm_Instruktioun[Rumm_INDEX]; 바꿈요청 = true; return true;
    }
    static void 흐름호출(int Besëtzer, int Numm_Konstant, int 서술상수, int Befeel_CODE) {
        boolean 수신쪽 = Word_SMS(Besëtzer, "java/net/ServerSocket"), Stream = Word_SMS(Besëtzer, "java/io/InputStream") || Word_SMS(Besëtzer, "java/io/OutputStream");
        if (!Stream && Befeel_CODE == 183 && Word_SMS(Numm_Konstant, "<init>")) {
            boolean 빈여부 = Word_SMS(서술상수, "()V"), 이름지정여부 = Word_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || 수신쪽 && Word_SMS(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { Feeler_VALUE("unsupported socket constructor"); return; }
            int 접속번호 = 빈여부 ? 0 : 빼기(1), Adress_Referenzen = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, Objet_Referenzen = 빼기(2);
            if (!Objet_VALUE(Objet_Referenzen, 수신쪽 ? 18 : 17)) return;
            if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !Objet_VALUE(Adress_Referenzen, 14)) return;
            int Reseau_Adress = 이름지정여부 ? 주소해독(Adress_Referenzen) : 주소지정여부 ? 힙[Adress_Referenzen + 2] : 0x7f000001;
            if (Feeler || 던진객체 != 0) return;
            int 열린파일번호 = Benotzer.Stream_Kontroll(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : 수신쪽 ? Benotzer.Stream_Kontroll(1, 열린파일번호, 접속번호) : Benotzer.Verbannen_Stream(열린파일번호, Reseau_Adress, 접속번호);
            if (처리값 < 0) { Benotzer.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[Objet_Referenzen + 2] = 열린파일번호; 힙[Objet_Referenzen + 4] = 접속번호; 힙[Objet_Referenzen + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!Stream && Word_SMS(Numm_Konstant, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), Objet_Referenzen = 빼기(2); if (!Objet_VALUE(Objet_Referenzen, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[Objet_Referenzen + 3] = 밀리초값; return; }
        if (!Stream && Word_SMS(Numm_Konstant, "close") && Word_SMS(서술상수, "()V")) { int Objet_Referenzen = 빼기(2); if (Objet_VALUE(Objet_Referenzen, 수신쪽 ? 18 : 17) && 힙[Objet_Referenzen + 2] >= 0) { Benotzer.파일서술자닫기(힙[Objet_Referenzen + 2]); 힙[Objet_Referenzen + 2] = -1; } return; }
        if (!Stream && (Word_SMS(Numm_Konstant, "getLocalPort") || Word_SMS(Numm_Konstant, "getPort") || Word_SMS(Numm_Konstant, "isClosed") || Word_SMS(Numm_Konstant, "isConnected"))) {
            int Objet_Referenzen = 빼기(2); if (!Objet_VALUE(Objet_Referenzen, 수신쪽 ? 18 : 17)) return;
            넣기(Word_SMS(Numm_Konstant, "isClosed") ? 힙[Objet_Referenzen + 2] < 0 ? 1 : 0 : Word_SMS(Numm_Konstant, "isConnected") ? 힙[Objet_Referenzen + 6] : Word_SMS(Numm_Konstant, "getPort") ? 힙[Objet_Referenzen + 4] : 힙[Objet_Referenzen + 2] < 0 ? -1 : Benotzer.Stream_Kontroll(4, 힙[Objet_Referenzen + 2], 0), 1); return;
        }
        if (수신쪽 && Word_SMS(Numm_Konstant, "accept") && Word_SMS(서술상수, "()Ljava/net/Socket;")) {
            int Objet_Referenzen = 빼기(2); if (!Objet_VALUE(Objet_Referenzen, 18)) return; int 열린파일번호 = Benotzer.Stream_Kontroll(3, 힙[Objet_Referenzen + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(Objet_Referenzen)) 넣기(Objet_Referenzen, 2); return; }
            힙[Objet_Referenzen + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = zouweisen_Späicher(17, 5); if (Feeler) { Benotzer.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = Benotzer.Stream_Kontroll(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !Stream && ((Word_SMS(Numm_Konstant, "getInputStream") && Word_SMS(서술상수, "()Ljava/io/InputStream;")) || (Word_SMS(Numm_Konstant, "getOutputStream") && Word_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int Objet_Referenzen = 빼기(2); if (!Objet_VALUE(Objet_Referenzen, 17)) return; if (힙[Objet_Referenzen + 2] < 0 || 힙[Objet_Referenzen + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = zouweisen_Späicher(19, 4); if (Feeler) return; 힙[반환값 + 2] = Objet_Referenzen; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Word_SMS(Numm_Konstant, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (Stream) {
            boolean 읽기여부 = Word_SMS(Numm_Konstant, "read"), 쓰기여부 = Word_SMS(Numm_Konstant, "write"), blockéieren = Word_SMS(서술상수, "([B)I") || Word_SMS(서술상수, "([B)V"), 부분배열여부 = Word_SMS(서술상수, "([BII)I") || Word_SMS(서술상수, "([BII)V");
            int Agab_COUNT = 부분배열여부 ? 빼기(1) : 0, 시작변위 = 부분배열여부 ? 빼기(1) : 0, Daten_ARRAY = blockéieren || 부분배열여부 ? 빼기(2) : 0;
            int Daten_VALUE = 쓰기여부 && Word_SMS(서술상수, "(I)V") ? 빼기(1) : 0, Objet_Referenzen = 빼기(2);
            if (!Objet_VALUE(Objet_Referenzen, 19)) return; int 부모참조 = 힙[Objet_Referenzen + 2], 열린파일번호 = 힙[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_SMS(Numm_Konstant, "close") && Word_SMS(서술상수, "()V")) { Benotzer.파일서술자닫기(열린파일번호); 힙[부모참조 + 2] = -1; return; }
            if (Word_SMS(Numm_Konstant, "flush") && Word_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !쓰기여부) || 읽기여부 != (힙[Objet_Referenzen + 3] == 0)) { Feeler_VALUE("unsupported stream operation"); return; }
            if (blockéieren || 부분배열여부) { if (!Objet_VALUE(Daten_ARRAY, 20)) return; if (blockéieren) Agab_COUNT = 힙[Daten_ARRAY + 1]; if (시작변위 < 0 || Agab_COUNT < 0 || 시작변위 > 힙[Daten_ARRAY + 1] - Agab_COUNT) { 예외던짐(6, "stream array bounds"); return; } }
            else Agab_COUNT = 1;
            if (Agab_COUNT == 0) { if (읽기여부) 넣기(0, 1); return; }
            int 완료수 = 쓰기여부 ? 힙[Objet_Referenzen + 4] : 0, 처리값 = 0;
            while (완료수 < Agab_COUNT) {
                처리값 = 읽기여부 ? Benotzer.파일한바이트읽기(열린파일번호) : Benotzer.파일한바이트쓰기(열린파일번호, blockéieren || 부분배열여부 ? 힙[Daten_ARRAY + 2 + 시작변위 + 완료수] : Daten_VALUE);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (blockéieren || 부분배열여부)) 힙[Daten_ARRAY + 2 + 시작변위 + 완료수] = (byte)처리값;
                완료수++; if (읽기여부 && !(blockéieren || 부분배열여부)) break;
            }
            if (처리값 == -11 && (쓰기여부 || 완료수 == 0)) {
                힙[Objet_Referenzen + 4] = 완료수;
                if (흐름대기(부모참조)) { 넣기(Objet_Referenzen, 2); if (blockéieren || 부분배열여부) 넣기(Daten_ARRAY, 2); if (부분배열여부) { 넣기(시작변위, 1); 넣기(Agab_COUNT, 1); } if (쓰기여부 && !(blockéieren || 부분배열여부)) 넣기(Daten_VALUE, 1); } return;
            }
            힙[Objet_Referenzen + 4] = 0; 힙[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(완료수 == 0 && 처리값 == 256 ? -1 : blockéieren || 부분배열여부 ? 완료수 : 처리값, 1); return;
        }
        Feeler_VALUE("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int Numm_Konstant) {
        if (Word_SMS(Numm_Konstant, "한국어/자체/Fënster")) return 24;
        if (Word_SMS(Numm_Konstant, "한국어/자체/Numm_5ce2bd6f")) return 26;
        if (Word_SMS(Numm_Konstant, "한국어/자체/Tast")) return 27;
        if (Word_SMS(Numm_Konstant, "한국어/자체/Textfeld")) return 28;
        if (Word_SMS(Numm_Konstant, "한국어/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int Numm_Konstant) {
        return 한국어화면종(Numm_Konstant) != 0 || Word_SMS(Numm_Konstant, "한국어/자체/화면구성요소") || Word_SMS(Numm_Konstant, "한국어/자체/Evenement_Schlaang");
    }
    static int 화면종(int Numm_Konstant) {
        int 한국어종 = 한국어화면종(Numm_Konstant); if (한국어종 != 0) return 한국어종;
        if (Word_SMS(Numm_Konstant, "javax/swing/JFrame")) return 24;
        if (Word_SMS(Numm_Konstant, "javax/swing/JPanel")) return 25;
        if (Word_SMS(Numm_Konstant, "javax/swing/JLabel")) return 26;
        if (Word_SMS(Numm_Konstant, "javax/swing/JButton")) return 27;
        if (Word_SMS(Numm_Konstant, "javax/swing/JTextField")) return 28;
        if (Word_SMS(Numm_Konstant, "java/awt/event/ActionEvent")) return 29;
        if (Word_SMS(Numm_Konstant, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int Numm_Konstant) {
        return 화면종(Numm_Konstant) != 0 || Word_SMS(Numm_Konstant, "java/awt/Component") || Word_SMS(Numm_Konstant, "java/awt/Container") || Word_SMS(Numm_Konstant, "javax/swing/JComponent") || Word_SMS(Numm_Konstant, "javax/swing/AbstractButton") || Word_SMS(Numm_Konstant, "javax/swing/text/JTextComponent") || Word_SMS(Numm_Konstant, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int Objet_Referenzen) { if (!객체유효(Objet_Referenzen)) return false; if (힙[Objet_Referenzen] < 24 || 힙[Objet_Referenzen] > 28) { Feeler_VALUE("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int Objet_Referenzen, int SMS_Referenzen) {
        if (SMS_Referenzen != 0 && !Objet_VALUE(SMS_Referenzen, 1)) return;
        int Agab_COUNT = SMS_Referenzen == 0 ? 0 : 힙[SMS_Referenzen + 1]; if (Agab_COUNT > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Agab_COUNT; Loop_INDEX++) 화면글임시[Loop_INDEX] = 힙[SMS_Referenzen + 2 + Loop_INDEX];
        if (Benotzer.화면글(힙[Objet_Referenzen + 2], 화면글임시, Agab_COUNT) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[Objet_Referenzen + 3] = SMS_Referenzen; 힙참조[Objet_Referenzen + 3] = 1;
    }
    static int 화면문자읽기(int Objet_Referenzen) {
        int Kont_VALUE = 힙[Objet_Referenzen + 2], Agab_COUNT = Benotzer.화면연결(8, Kont_VALUE, 0, 0, 0, 0), 사용수 = 0;
        if (Agab_COUNT < 0) { Feeler_VALUE("GUI text read failed"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < Agab_COUNT; Loop_INDEX++) { int 부호값 = Benotzer.화면연결(9, Kont_VALUE, Loop_INDEX, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = zouweisen_Späicher(1, 사용수); if (!Feeler) for (int Loop_INDEX = 0; Loop_INDEX < 사용수; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 화면글임시[Loop_INDEX]; return 반환값;
    }
    /* 한국어 객체를 직접 만들고 Kernel_VALUE 화면 기능에 연결한다. Swing Objet_VALUE/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int Besëtzer, int Numm_Konstant, int 서술상수, int Befeel_CODE) {
        if (Word_SMS(Besëtzer, "한국어/자체/Evenement_Schlaang")) {
            if (Befeel_CODE == 184 && Word_SMS(Numm_Konstant, "나중에실행") && Word_SMS(서술상수, "(L한국어/자체/실행할일;)V")) {
                int To_do_Aktioun = 빼기(2); if (!객체유효(To_do_Aktioun)) return;
                if (나중수 == 8) { Feeler_VALUE("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = To_do_Aktioun; return;
            }
            if (Befeel_CODE == 184 && Word_SMS(Numm_Konstant, "사건처리중인가") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            Feeler_VALUE("지원하지 않는 한국어 화면 일정 호출"); return;
        }
        if (Word_SMS(Besëtzer, "한국어/자체/동작알림")) {
            int 알림 = 빼기(2); if (!Objet_VALUE(알림, 29) || 힙[알림 + 3] == 0) return;
            if (Word_SMS(Numm_Konstant, "Evenement_Quell") && Word_SMS(서술상수, "()L한국어/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (Word_SMS(Numm_Konstant, "Befeel_SMS") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (Word_SMS(Numm_Konstant, "INDEX") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else Feeler_VALUE("지원하지 않는 한국어 Aktioun 알림 호출"); return;
        }
        if (Befeel_CODE == 183 && Word_SMS(Numm_Konstant, "<init>")) {
            int 종류 = 한국어화면종(Besëtzer), 받이 = 0, 가로 = 0, Vertikal_positionéieren = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Word_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (Benotzer.화면너비() - 폭) / 2; Vertikal_positionéieren = (Benotzer.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Word_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Word_SMS(서술상수, "(Ljava/lang/String;IIIIL한국어/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); Vertikal_positionéieren = 빼기(1); 가로 = 빼기(1);
            } else { Feeler_VALUE("지원하지 않는 한국어 화면 생성자"); return; }
            int SMS = 빼기(2), Element_VALUE = 빼기(2); if (!화면객체(Element_VALUE)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || Vertikal_positionéieren < 0 || 폭 > Benotzer.화면너비() - 가로 || 높이 > Benotzer.화면높이() - Vertikal_positionéieren) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDEX = Benotzer.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (INDEX < 1 || INDEX > 32) { Feeler_VALUE("화면 Element_VALUE 자리가 가득 찼습니다"); return; }
            힙[Element_VALUE + 2] = INDEX; 화면참조[INDEX - 1] = Element_VALUE;
            힙[Element_VALUE + 5] = 가로; 힙[Element_VALUE + 6] = Vertikal_positionéieren; 힙[Element_VALUE + 7] = 폭; 힙[Element_VALUE + 8] = 높이; 힙[Element_VALUE + 10] = 2;
            힙[Element_VALUE + 4] = 받이; 힙참조[Element_VALUE + 4] = 1; 힙[Element_VALUE + 12] = 1;
            Benotzer.화면연결(1, INDEX, 가로, Vertikal_positionéieren, 폭, 높이);
            if (종류 == 24) Benotzer.화면연결(7, INDEX, 2, 0, 0, 0);
            화면문자설정(Element_VALUE, SMS); return;
        }
        if (Befeel_CODE != 182) { Feeler_VALUE("잘못된 한국어 화면 호출 Befeel"); return; }
        if (Word_SMS(Numm_Konstant, "schreiwen_SMS") && Word_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int SMS = 빼기(2), Element_VALUE = 빼기(2); if (화면객체(Element_VALUE)) 화면문자설정(Element_VALUE, SMS); return;
        }
        if (Word_SMS(Numm_Konstant, "글읽기") && Word_SMS(서술상수, "()Ljava/lang/String;")) {
            int Element_VALUE = 빼기(2); if (화면객체(Element_VALUE)) 넣기(화면문자읽기(Element_VALUE), 2); return;
        }
        if (Word_SMS(Numm_Konstant, "동작맡기기") && Word_SMS(서술상수, "(L한국어/자체/동작받이;)V")) {
            int 받이 = 빼기(2), Element_VALUE = 빼기(2);
            if (화면객체(Element_VALUE)) { 힙[Element_VALUE + 4] = 받이; 힙참조[Element_VALUE + 4] = 1; 힙[Element_VALUE + 12] = 1; } return;
        }
        if (Word_SMS(Numm_Konstant, "derbäisetzen_Element") && Word_SMS(서술상수, "(L한국어/자체/화면구성요소;)V")) {
            int Kand_VALUE = 빼기(2), 부모 = 빼기(2); if (!화면객체(Kand_VALUE) || !화면객체(부모)) return;
            if (Benotzer.화면연결(2, 힙[부모 + 2], 힙[Kand_VALUE + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[Kand_VALUE + 11] = 부모; 힙참조[Kand_VALUE + 11] = 1; return;
        }
        if (Word_SMS(Numm_Konstant, "자리정하기") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), Vertikal_positionéieren = 빼기(1), 가로 = 빼기(1), Element_VALUE = 빼기(2); if (!화면객체(Element_VALUE)) return;
            if (Benotzer.화면연결(1, 힙[Element_VALUE + 2], 가로, Vertikal_positionéieren, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[Element_VALUE + 5] = 가로; 힙[Element_VALUE + 6] = Vertikal_positionéieren; 힙[Element_VALUE + 7] = 폭; 힙[Element_VALUE + 8] = 높이; return;
        }
        if ((Word_SMS(Numm_Konstant, "Show_Fënster") || Word_SMS(Numm_Konstant, "Clôture")) && Word_SMS(서술상수, "()V")) {
            boolean Visibilitéit_VALUE = Word_SMS(Numm_Konstant, "Show_Fënster"); int Element_VALUE = 빼기(2); if (!화면객체(Element_VALUE)) return;
            if (Benotzer.화면연결(Visibilitéit_VALUE ? 3 : 4, 힙[Element_VALUE + 2], Visibilitéit_VALUE ? 1 : 0, 0, 0, 0) < 0) { Feeler_VALUE("화면은 interaktiv 명령에서 실행해야 합니다"); return; }
            힙[Element_VALUE + 9] = Visibilitéit_VALUE ? 1 : 0; return;
        }
        if (Word_SMS(Numm_Konstant, "보이는가") && Word_SMS(서술상수, "()Z")) { int Element_VALUE = 빼기(2); if (화면객체(Element_VALUE)) 넣기(힙[Element_VALUE + 9], 1); return; }
        Feeler_VALUE("지원하지 않는 한국어 화면 Method_VALUE");
    }
    static void 화면호출(int Besëtzer, int Numm_Konstant, int 서술상수, int Befeel_CODE) {
        if (Word_SMS(Besëtzer, "javax/swing/SwingUtilities")) {
            if (Befeel_CODE == 184 && Word_SMS(Numm_Konstant, "invokeLater") && Word_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int Objet_Referenzen = 빼기(2); if (!객체유효(Objet_Referenzen)) return; if (나중수 == 8) { Feeler_VALUE("invokeLater queue full"); return; } 나중실행[나중수++] = Objet_Referenzen; return; }
            if (Befeel_CODE == 184 && Word_SMS(Numm_Konstant, "isEventDispatchThread") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            Feeler_VALUE("unsupported SwingUtilities method"); return;
        }
        if (Word_SMS(Besëtzer, "java/awt/event/ActionEvent")) {
            int Objet_Referenzen = 빼기(2); if (!Objet_VALUE(Objet_Referenzen, 29)) return;
            if (Word_SMS(Numm_Konstant, "getSource") && Word_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[Objet_Referenzen + 2], 2);
            else if (Word_SMS(Numm_Konstant, "getActionCommand") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[Objet_Referenzen + 2]), 2);
            else if (Word_SMS(Numm_Konstant, "getID") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else Feeler_VALUE("unsupported ActionEvent method"); return;
        }
        if (Befeel_CODE == 183 && Word_SMS(Numm_Konstant, "<init>")) {
            int COLUMNS = 0, SMS_Referenzen = 0;
            if (Word_SMS(서술상수, "(I)V")) COLUMNS = 빼기(1);
            else if (Word_SMS(서술상수, "(Ljava/lang/String;I)V")) { COLUMNS = 빼기(1); SMS_Referenzen = 빼기(2); }
            else if (Word_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_Referenzen = 빼기(2);
            else if (Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_SMS(서술상수, "()V")) { Feeler_VALUE("unsupported Swing constructor"); return; }
            int Objet_Referenzen = 빼기(2); if (!객체유효(Objet_Referenzen)) return;
            if (힙[Objet_Referenzen] == 30) { Feeler_VALUE("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(Objet_Referenzen) || COLUMNS < 0) return;
            int Kont_VALUE = Benotzer.화면연결(0, 힙[Objet_Referenzen] - 23, 0, 0, 0, 0);
            if (Kont_VALUE < 1 || Kont_VALUE > 32) { Feeler_VALUE("GUI widget slots exhausted"); return; }
            힙[Objet_Referenzen + 2] = Kont_VALUE; 화면참조[Kont_VALUE - 1] = Objet_Referenzen; 힙[Objet_Referenzen + 5] = 힙[Objet_Referenzen] == 24 ? 130 : 16; 힙[Objet_Referenzen + 6] = 힙[Objet_Referenzen] == 24 ? 110 : 16;
            힙[Objet_Referenzen + 7] = 힙[Objet_Referenzen] == 24 ? 380 : 220; 힙[Objet_Referenzen + 8] = 힙[Objet_Referenzen] == 24 ? 240 : 28; 힙[Objet_Referenzen + 10] = 1;
            화면문자설정(Objet_Referenzen, SMS_Referenzen); return;
        }
        if (Word_SMS(Numm_Konstant, "setText") || Word_SMS(Numm_Konstant, "setTitle")) { int SMS_Referenzen = 빼기(2), Objet_Referenzen = 빼기(2); if (화면객체(Objet_Referenzen) && Word_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(Objet_Referenzen, SMS_Referenzen); return; }
        if (Word_SMS(Numm_Konstant, "getText") || Word_SMS(Numm_Konstant, "getTitle")) { int Objet_Referenzen = 빼기(2); if (화면객체(Objet_Referenzen) && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(Objet_Referenzen), 2); return; }
        if (Word_SMS(Numm_Konstant, "addActionListener") && Word_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), Objet_Referenzen = 빼기(2); if (화면객체(Objet_Referenzen)) { 힙[Objet_Referenzen + 4] = 수신참조; 힙참조[Objet_Referenzen + 4] = 1; } return; }
        if (Word_SMS(Numm_Konstant, "getContentPane") && Word_SMS(서술상수, "()Ljava/awt/Container;")) { int Objet_Referenzen = 빼기(2); if (화면객체(Objet_Referenzen)) 넣기(Objet_Referenzen, 2); return; }
        if (Word_SMS(Numm_Konstant, "setLayout") && Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Layout_Referenzen = 빼기(2), Objet_Referenzen = 빼기(2); if (화면객체(Objet_Referenzen) && Layout_Referenzen != 0) Feeler_VALUE("only absolute layout (null) is supported"); return; }
        if (Word_SMS(Numm_Konstant, "add") && (Word_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Layout_Bedéngung = Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Layout_Bedéngung) 빼기(2);
            int Kand_Referenzen = 빼기(2), Objet_Referenzen = 빼기(2); if (!화면객체(Kand_Referenzen) || !화면객체(Objet_Referenzen)) return;
            if (Benotzer.화면연결(2, 힙[Objet_Referenzen + 2], 힙[Kand_Referenzen + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[Kand_Referenzen + 11] = Objet_Referenzen; 힙참조[Kand_Referenzen + 11] = 1; if (!Layout_Bedéngung) 넣기(Kand_Referenzen, 2); return;
        }
        if (Word_SMS(Numm_Konstant, "setBounds") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), X_Koordinat = 빼기(1), Objet_Referenzen = 빼기(2); if (!화면객체(Objet_Referenzen)) return;
            if (Benotzer.화면연결(1, 힙[Objet_Referenzen + 2], X_Koordinat, 세로좌표, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[Objet_Referenzen + 5] = X_Koordinat; 힙[Objet_Referenzen + 6] = 세로좌표; 힙[Objet_Referenzen + 7] = 너비; 힙[Objet_Referenzen + 8] = 높이; return;
        }
        if (Word_SMS(Numm_Konstant, "setSize") && Word_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), Objet_Referenzen = 빼기(2); if (!화면객체(Objet_Referenzen)) return;
            if (Benotzer.화면연결(1, 힙[Objet_Referenzen + 2], 힙[Objet_Referenzen + 5], 힙[Objet_Referenzen + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[Objet_Referenzen + 7] = 너비; 힙[Objet_Referenzen + 8] = 높이; } return;
        }
        if (Word_SMS(Numm_Konstant, "setLocationRelativeTo") && Word_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), Objet_Referenzen = 빼기(2); if (!화면객체(Objet_Referenzen)) return; if (상대배치 != 0) { Feeler_VALUE("only screen centering supported"); return; } 힙[Objet_Referenzen + 5] = (Benotzer.화면너비() - 힙[Objet_Referenzen + 7]) / 2; 힙[Objet_Referenzen + 6] = (Benotzer.화면높이() - 힙[Objet_Referenzen + 8]) / 2; Benotzer.화면연결(1, 힙[Objet_Referenzen + 2], 힙[Objet_Referenzen + 5], 힙[Objet_Referenzen + 6], 힙[Objet_Referenzen + 7], 힙[Objet_Referenzen + 8]); return; }
        if (Word_SMS(Numm_Konstant, "setDefaultCloseOperation") && Word_SMS(서술상수, "(I)V")) { int Richtlinn = 빼기(1), Objet_Referenzen = 빼기(2); if (화면객체(Objet_Referenzen)) { if (Richtlinn < 0 || Richtlinn > 3) 예외던짐(9, "close policy"); else { 힙[Objet_Referenzen + 10] = Richtlinn; Benotzer.화면연결(7, 힙[Objet_Referenzen + 2], Richtlinn, 0, 0, 0); } } return; }
        if (Word_SMS(Numm_Konstant, "setVisible") && Word_SMS(서술상수, "(Z)V")) { int Daten_VALUE = 빼기(1), Objet_Referenzen = 빼기(2); if (화면객체(Objet_Referenzen)) { int 처리값 = Benotzer.화면연결(3, 힙[Objet_Referenzen + 2], Daten_VALUE, 0, 0, 0); if (처리값 < 0) Feeler_VALUE("Swing requires a standalone interactive command"); else 힙[Objet_Referenzen + 9] = Daten_VALUE; } return; }
        if (Word_SMS(Numm_Konstant, "dispose") && Word_SMS(서술상수, "()V")) { int Objet_Referenzen = 빼기(2); if (화면객체(Objet_Referenzen)) { Benotzer.화면연결(4, 힙[Objet_Referenzen + 2], 0, 0, 0, 0); 힙[Objet_Referenzen + 9] = 0; } return; }
        if (Word_SMS(Numm_Konstant, "repaint") || Word_SMS(Numm_Konstant, "validate")) { int Objet_Referenzen = 빼기(2); if (!화면객체(Objet_Referenzen) || !Word_SMS(서술상수, "()V")) return; Benotzer.화면연결(1, 힙[Objet_Referenzen + 2], 힙[Objet_Referenzen + 5], 힙[Objet_Referenzen + 6], 힙[Objet_Referenzen + 7], 힙[Objet_Referenzen + 8]); return; }
        if (Word_SMS(Numm_Konstant, "isVisible") && Word_SMS(서술상수, "()Z")) { int Objet_Referenzen = 빼기(2); if (화면객체(Objet_Referenzen)) 넣기(힙[Objet_Referenzen + 9], 1); return; }
        Feeler_VALUE("unsupported Swing method (native subset)");
    }
    static void 사건실행(int Zil_Adress, int 사건번호, boolean 한국어) {
        if (Zil_Adress < 1 || 힙[Zil_Adress] < 32) { Feeler_VALUE("Java event listener required"); return; }
        int Fichier_INDEX = Numm_Method(힙[Zil_Adress] - 32, 사건번호 == 0 ? (한국어 ? "Ausféieren" : "run") : (한국어 ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (한국어 ? "(L한국어/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (Fichier_INDEX < 0) { Feeler_VALUE("event callback missing"); return; }
        현재가닥 = 0; Thread_COUNT = 1; Rumm_INDEX = 0; Thread_Status[0] = 1; Rumm_Stapel[0] = 0; 틀잠금[0] = initialiséieren_Rumm[0] = 0; 바꿈요청 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 128; Loop_INDEX++) { lokal_VALUE[Loop_INDEX] = lokal_TYPE[Loop_INDEX] = 0; }
        Rumm_Method[0] = Fichier_INDEX; Rumm_positionéieren[0] = Method_Start[Fichier_INDEX]; lokal_VALUE[0] = Zil_Adress; lokal_TYPE[0] = 2;
        if (사건번호 != 0) { lokal_VALUE[1] = 사건번호; lokal_TYPE[1] = 2; }
        사건중 = true; ausféieren_Befeel(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!Feeler) {
            if (나중수 > 0) { int Zil_Adress = 나중실행[0], 한국어 = 나중한국어[0]; for (int Loop_INDEX = 1; Loop_INDEX < 나중수; Loop_INDEX++) { 나중실행[Loop_INDEX - 1] = 나중실행[Loop_INDEX]; 나중한국어[Loop_INDEX - 1] = 나중한국어[Loop_INDEX]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(Zil_Adress, 0, 한국어 != 0); continue; }
            if (Benotzer.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = Benotzer.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { Feeler_VALUE("GUI event I/O failed"); return; }
            int Kont_VALUE = 사건번호 & 65535; if (Kont_VALUE < 1 || Kont_VALUE > 32) continue; int Objet_Referenzen = 화면참조[Kont_VALUE - 1]; if (Objet_Referenzen == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[Objet_Referenzen + 10] != 0) 힙[Objet_Referenzen + 9] = 0;
                if (힙[Objet_Referenzen + 10] == 3) for (int Loop_INDEX = 0; Loop_INDEX < 32; Loop_INDEX++) if (화면참조[Loop_INDEX] != 0 && 힙[화면참조[Loop_INDEX]] == 24) Benotzer.화면연결(4, Loop_INDEX + 1, 0, 0, 0, 0);
            } else if (힙[Objet_Referenzen + 4] != 0) {
                int LIESMECH_Referenzen = zouweisen_Späicher(29, 2); if (Feeler) return; 힙[LIESMECH_Referenzen + 2] = Objet_Referenzen; 힙[LIESMECH_Referenzen + 3] = 힙[Objet_Referenzen + 12]; 힙참조[LIESMECH_Referenzen + 2] = 1; 사건실행(힙[Objet_Referenzen + 4], LIESMECH_Referenzen, 힙[Objet_Referenzen + 12] != 0);
            }
        }
    }
    public static int Laf() {
        if (Benotzer.인수개수() == 1 && 자바도구.같음(Benotzer.인수(0), "-version")) {
            Benotzer.schreiwen("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (Benotzer.인수개수() < 1) { Benotzer.schreiwen("Usage: java CLASS [ARGS]\n"); return 2; }
        Agab_Klass_Definitioun = Charge_Klass_Definitioun(Host_Zeechen(Benotzer.인수(0))); if (Feeler || Agab_Klass_Definitioun < 0) return 1;
        int Agab_Punkt_VALUE = Numm_Method(Agab_Klass_Definitioun, "Laf", "()V");
        boolean 한국어진입 = Agab_Punkt_VALUE >= 0 && (Method_Zougrëff[Agab_Punkt_VALUE] & 9) == 9;
        if (!한국어진입) Agab_Punkt_VALUE = Numm_Method(Agab_Klass_Definitioun, "main", "([Ljava/lang/String;)V");
        if (Agab_Punkt_VALUE < 0 || (Method_Zougrëff[Agab_Punkt_VALUE] & 9) != 9) Feeler_VALUE("public static void Laf() or main(String[] args) required");
        if (Feeler) return 1;
        int 인수 = zouweisen_Späicher(3, Benotzer.인수개수() - 1); ARRAY_Element[인수] = -1;
        for (int 수 = 1; 수 < Benotzer.인수개수() && !Feeler; 수++) 힙[인수 + 1 + 수] = Host_Zeechen(Benotzer.인수(수));
        Rumm_INDEX = 0; Rumm_Method[0] = Agab_Punkt_VALUE; Rumm_positionéieren[0] = Method_Start[Agab_Punkt_VALUE]; lokal_VALUE[0] = 한국어진입 ? 0 : 인수; lokal_TYPE[0] = 한국어진입 ? 0 : 2;
        Thread_Status[0] = 1; Thread_Objet[0] = zouweisen_Späicher(13, 2);
        ausféieren_Befeel(); if (!Feeler) 화면사건들(); return Feeler ? 1 : 0;
    }
}
