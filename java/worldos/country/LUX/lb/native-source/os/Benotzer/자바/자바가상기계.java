// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Fichier/스택/Referenzen/Branche 경계를 ausféieren_Befeel 중 검사한다. */
public final class 자바가상기계 {
    static int[] Fichier = new int[16384], Fichier_Numm_SMS = new int[64];
    static int[] Konstant_Tag = new int[512], 상가 = new int[512], Konstant_SECOND_VALUE = new int[512], Zeechefolleg_Referenzen = new int[512];
    static int[] Method_Numm_SMS = new int[32], Method_TYPE = new int[32], Method_Zougrëff = new int[32];
    static int[] Method_Start = new int[32], Method_bëennegen = new int[32], Method_Stapel = new int[32], 함수지역 = new int[32];
    static int[] Method_Argument_COUNT = new int[32], Method_Argument_TYPE = new int[512], 함수반환 = new int[32];
    static int[] 경계 = new int[16384];
    static int[] lokal_VALUE = new int[4096], lokal_TYPE = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] Rumm_Method = new int[32], Rumm_positionéieren = new int[32], Rumm_Stapel = new int[32];
    static int[] 힙 = new int[8192];
    static int d_Gréisst_veränneren, 읽기위치, Konstant_COUNT, Method_COUNT, Klass_Numm, Rumm_INDEX = -1, 힙끝 = 1, 반환형;
    static boolean Feeler;

    static void Feeler_VALUE(String Word_SMS) {
        if (!Feeler) { Benotzer.schreiwen("JVM error: "); Benotzer.schreiwen(Word_SMS); Benotzer.schreiwen_Zeechen_VALUE(10); }
        Feeler = true;
    }
    static boolean Clip(int Laf, int Längt_VALUE) { return Laf >= 0 && Längt_VALUE >= 0 && Laf <= d_Gréisst_veränneren - Längt_VALUE; }
    static int Byte_VALUE() {
        if (!Clip(읽기위치, 1)) { Feeler_VALUE("truncated class file"); return 0; }
        return Fichier[읽기위치++];
    }
    static int 짧은수() { return Byte_VALUE() << 8 | Byte_VALUE(); }
    static int Ganzzuel() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int Längt_VALUE) { if (!Clip(읽기위치, Längt_VALUE)) Feeler_VALUE("invalid attribute size"); else 읽기위치 += Längt_VALUE; }
    static boolean Scheck_Konstant(int 수, int 종류) {
        if (수 <= 0 || 수 >= Konstant_COUNT || Konstant_Tag[수] != 종류) { Feeler_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Laf, int Längt_VALUE, String Word_SMS) {
        if (!Clip(Laf, Längt_VALUE) || Längt_VALUE != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < Längt_VALUE; 수++) if (Fichier[Laf + 수] != Word_SMS.charAt(수)) return false;
        return true;
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
    static void 속성건너() {
        int Element_COUNT = 짧은수();
        for (int 수 = 0; 수 < Element_COUNT && !Feeler; 수++) { Scheck_Konstant(짧은수(), 1); 건너(Ganzzuel()); }
    }
    static int Befeel_Längt(int VALUE) {
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
        if (Ganzzuel() != 0xcafebabe) Feeler_VALUE("not a class file");
        int 부판 = 짧은수(), Versioun_VALUE = 짧은수();
        if (Versioun_VALUE < 45 || Versioun_VALUE > 52 || 부판 != 0) Feeler_VALUE("supported class versions: 45..52, minor 0");
        Konstant_COUNT = 짧은수();
        if (Konstant_COUNT < 1 || Konstant_COUNT > 512) { Feeler_VALUE("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < Konstant_COUNT && !Feeler; 수++) {
            int 종류 = Byte_VALUE(); Konstant_Tag[수] = 종류;
            if (종류 == 1) { Konstant_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(Konstant_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = Ganzzuel();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); Konstant_SECOND_VALUE[수] = 짧은수(); }
            else Feeler_VALUE("unsupported constant type");
        }
        int Geneemegung_VALUE = 짧은수();
        if ((Geneemegung_VALUE & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) Feeler_VALUE("unsupported class flags");
        Klass_Numm = Klass_Numm_SMS(짧은수());
        if (!Word_SMS(Klass_Numm_SMS(짧은수()), "java/lang/Object")) Feeler_VALUE("inheritance unsupported");
        if (짧은수() != 0) Feeler_VALUE("interfaces unsupported");
        if (짧은수() != 0) Feeler_VALUE("fields unsupported");
        Method_COUNT = 짧은수();
        if (Method_COUNT < 1 || Method_COUNT > 32) { Feeler_VALUE("method count limit (32)"); return; }
        for (int 수 = 0; 수 < Method_COUNT && !Feeler; 수++) {
            Method_Zougrëff[수] = 짧은수(); Method_Numm_SMS[수] = 짧은수(); Method_TYPE[수] = 짧은수();
            Scheck_Konstant(Method_Numm_SMS[수], 1); 서술읽기(수);
            if ((Method_Zougrëff[수] & (0x100 | 0x400 | 0x20)) != 0) Feeler_VALUE("native, abstract and synchronized methods unsupported");
            if ((Method_Zougrëff[수] & 8) == 0 && !Word_SMS(Method_Numm_SMS[수], "<init>")) Feeler_VALUE("instance methods unsupported");
            if (Word_SMS(Method_Numm_SMS[수], "<clinit>")) Feeler_VALUE("class initializers unsupported");
            for (int 앞 = 0; 앞 < 수; 앞++) if (같은말(Method_Numm_SMS[앞], Method_Numm_SMS[수]) && 같은말(Method_TYPE[앞], Method_TYPE[수])) Feeler_VALUE("duplicate method");
            int Element_COUNT = 짧은수();
            for (int Attribut_VALUE = 0; Attribut_VALUE < Element_COUNT && !Feeler; Attribut_VALUE++) {
                int Numm = 짧은수(), Längt_VALUE = Ganzzuel(), Laf = 읽기위치;
                if (!Clip(Laf, Längt_VALUE)) { Feeler_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Numm, "Code")) {
                    if (Method_Start[수] != 0) Feeler_VALUE("duplicate Code attribute");
                    Method_Stapel[수] = 짧은수(); 함수지역[수] = 짧은수(); int CODE_Längt = Ganzzuel();
                    if (Method_Stapel[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < Method_Argument_COUNT[수]
                        || CODE_Längt < 1 || CODE_Längt > 8192) Feeler_VALUE("method memory limits exceeded");
                    Method_Start[수] = 읽기위치; 건너(CODE_Längt); Method_bëennegen[수] = 읽기위치;
                    if (짧은수() != 0) Feeler_VALUE("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != Laf + Längt_VALUE) Feeler_VALUE("Code attribute size mismatch");
                } else 건너(Längt_VALUE);
            }
            if (Method_Start[수] == 0) Feeler_VALUE("missing Code attribute");
            int Slot_Agab = Method_Start[수];
            while (Slot_Agab < Method_bëennegen[수] && !Feeler) {
                int Längt_VALUE = Befeel_Längt(Fichier[Slot_Agab]);
                if (Längt_VALUE == 0 || Längt_VALUE > Method_bëennegen[수] - Slot_Agab) { Feeler_VALUE("unsupported or truncated bytecode"); break; }
                경계[Slot_Agab] = 수 + 1; Slot_Agab += Längt_VALUE;
            }
            // 실행하지 않는 경로에도 잘못된 Branche 목적지를 허용하지 않는다.
            Slot_Agab = Method_Start[수];
            while (Slot_Agab < Method_bëennegen[수] && !Feeler) {
                int VALUE = Fichier[Slot_Agab];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                    int Zil_VALUE = Slot_Agab + (short)(Fichier[Slot_Agab + 1] << 8 | Fichier[Slot_Agab + 2]);
                    if (Zil_VALUE < Method_Start[수] || Zil_VALUE >= Method_bëennegen[수] || 경계[Zil_VALUE] != 수 + 1) Feeler_VALUE("invalid branch target");
                }
                Slot_Agab += Befeel_Längt(VALUE);
            }
        }
        if (!Feeler) 속성건너();
        if (읽기위치 != d_Gréisst_veränneren) Feeler_VALUE("extra class file data");
    }
    static int zouweisen_Späicher(int 종류, int Längt_VALUE) {
        if (Längt_VALUE < 0 || Längt_VALUE > 힙.length - 힙끝 - 2) { Feeler_VALUE("object heap exhausted or negative array size"); return 0; }
        int Referenzen = 힙끝; 힙끝 += Längt_VALUE + 2; 힙[Referenzen] = 종류; 힙[Referenzen + 1] = Längt_VALUE;
        return Referenzen;
    }
    static boolean Objet_VALUE(int Referenzen, int 종류) {
        if (Referenzen < 1 || Referenzen >= 힙끝 - 1 || 힙[Referenzen] != 종류) { Feeler_VALUE("null or invalid object reference"); return false; }
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
        if (Rumm_INDEX == 31) { Feeler_VALUE("call stack limit (32)"); return; }
        int Weider_Element = Rumm_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) lokal_TYPE[Weider_Element * 128 + 수] = 0;
        for (int 수 = Method_Argument_COUNT[FUNCTION_VALUE] - 1; 수 >= 0; 수--) {
            lokal_VALUE[Weider_Element * 128 + 수] = 빼기(Method_Argument_TYPE[FUNCTION_VALUE * 16 + 수]); lokal_TYPE[Weider_Element * 128 + 수] = Method_Argument_TYPE[FUNCTION_VALUE * 16 + 수];
        }
        Rumm_INDEX = Weider_Element; Rumm_Method[Rumm_INDEX] = FUNCTION_VALUE; Rumm_positionéieren[Rumm_INDEX] = Method_Start[FUNCTION_VALUE]; Rumm_Stapel[Rumm_INDEX] = 0;
    }
    static void 반환(int TYPE_VALUE) {
        if (TYPE_VALUE != 함수반환[Rumm_Method[Rumm_INDEX]]) { Feeler_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        Rumm_INDEX--; if (Rumm_INDEX >= 0 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
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
                if (VALUE < 1 || VALUE > 127) { Feeler_VALUE("file stream paths currently require ASCII"); return; }
                Stream_Fichier_Numm[Slot_Agab] = VALUE;
            }
            Stream_Fichier_Numm[Längt_VALUE] = 0;
            int 서술자 = Benotzer.파일서술자열기(Stream_Fichier_Numm, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { Feeler_VALUE("FileNotFoundException: file open failed"); return; }
            힙[Stream_VALUE + 2] = 서술자; 힙[Stream_VALUE + 3] = 1;
            return;
        }
        if (Befeel != 182) { Feeler_VALUE("invalid file stream invocation"); return; }
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
            if (Mooss < -1) Feeler_VALUE("IOException: read failed"); else 넣기(Mooss, 1);
        } else if (Benotzer.파일한바이트쓰기(서술자, VALUE) != 1) Feeler_VALUE("IOException: write failed");
    }
    static void CALL_Method(int INDEX, int Befeel) {
        if (!Scheck_Konstant(INDEX, 10)) return;
        int Besëtzer_VALUE = Klass_Numm_SMS(상가[INDEX]), Numm = Referenzen_Numm(Konstant_SECOND_VALUE[INDEX]), Format_VALUE = Referenzen_TYPE(Konstant_SECOND_VALUE[INDEX]);
        if (Feeler) return;
        if (같은말(Besëtzer_VALUE, Klass_Numm)) {
            if (Befeel != 184) { Feeler_VALUE("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < Method_COUNT; 수++) if (같은말(Numm, Method_Numm_SMS[수]) && 같은말(Format_VALUE, Method_TYPE[수])) {
                if ((Method_Zougrëff[수] & 8) == 0) Feeler_VALUE("method is not static"); else 호출(수);
                return;
            }
            Feeler_VALUE("NoSuchMethodError"); return;
        }
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
        Feeler_VALUE("unsupported library method");
    }
    static int ARRAY_Slot(int Referenzen, int déifstellen_VALUE, int TYPE_VALUE) {
        if (!Objet_VALUE(Referenzen, TYPE_VALUE)) return 0;
        if (déifstellen_VALUE < 0 || déifstellen_VALUE >= 힙[Referenzen + 1]) { Feeler_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return Referenzen + 2 + déifstellen_VALUE;
    }
    static void ausféieren_Befeel() {
        int 남음 = 500000;
        while (Rumm_INDEX >= 0 && !Feeler) {
            if (--남음 == 0) { Feeler_VALUE("instruction limit (500000)"); break; }
            int Laf = Rumm_positionéieren[Rumm_INDEX], VALUE = 명바();
            if (Feeler) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = VALUE == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= Konstant_COUNT) Feeler_VALUE("invalid ldc constant");
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
            if (VALUE == 46 || VALUE == 50) {
                int déifstellen_VALUE = 빼기(1), Referenzen = 빼기(2), Slot_Agab = ARRAY_Slot(Referenzen, déifstellen_VALUE, VALUE == 46 ? 2 : 3);
                if (!Feeler) 넣기(힙[Slot_Agab], VALUE == 46 ? 1 : 2); continue;
            }
            if (VALUE == 79 || VALUE == 83) {
                int Element_Element = 빼기(VALUE == 79 ? 1 : 2), déifstellen_VALUE = 빼기(1), Referenzen = 빼기(2), Slot_Agab = ARRAY_Slot(Referenzen, déifstellen_VALUE, VALUE == 79 ? 2 : 3);
                if (VALUE == 83 && Element_Element != 0) Objet_VALUE(Element_Element, 1);
                if (!Feeler) 힙[Slot_Agab] = Element_Element; continue;
            }
            if (VALUE == 87) { 빼기(0); continue; }
            if (VALUE == 89) { int 가 = 빼기(0), TYPE_VALUE = 반환형; 넣기(가, TYPE_VALUE); 넣기(가, TYPE_VALUE); continue; }
            if (VALUE == 95) { int 가 = 빼기(0), 가형 = 반환형, 나 = 빼기(0), 나형 = 반환형; 넣기(가, 가형); 넣기(나, 나형); continue; }
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
            if (VALUE == 178) {
                int 수 = 명짧(); if (!Scheck_Konstant(수, 9)) continue;
                if (!Word_SMS(Klass_Numm_SMS(상가[수]), "java/lang/System") || !Word_SMS(Referenzen_Numm(Konstant_SECOND_VALUE[수]), "out")
                    || !Word_SMS(Referenzen_TYPE(Konstant_SECOND_VALUE[수]), "Ljava/io/PrintStream;")) Feeler_VALUE("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (VALUE == 182 || VALUE == 183 || VALUE == 184) { CALL_Method(명짧(), VALUE); continue; }
            if (VALUE == 187) {
                int Numm = Klass_Numm_SMS(명짧());
                if (Word_SMS(Numm, "java/lang/StringBuilder")) 넣기(zouweisen_Späicher(4, 1), 2);
                else if (Word_SMS(Numm, "java/io/FileInputStream") || Word_SMS(Numm, "java/io/FileOutputStream")) {
                    int Referenzen = zouweisen_Späicher(Word_SMS(Numm, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!Feeler) { 힙[Referenzen + 2] = -1; 넣기(Referenzen, 2); }
                } else Feeler_VALUE("unsupported object construction");
                continue;
            }
            if (VALUE == 188 || VALUE == 189) {
                if (VALUE == 188) { if (명바() != 10) Feeler_VALUE("only int[] newarray is supported"); }
                else if (!Word_SMS(Klass_Numm_SMS(명짧()), "java/lang/String")) Feeler_VALUE("only String[] anewarray is supported");
                int Längt_VALUE = 빼기(1); 넣기(zouweisen_Späicher(VALUE == 188 ? 2 : 3, Längt_VALUE), 2); continue;
            }
            if (VALUE == 190) {
                int Referenzen = 빼기(2);
                if (Referenzen < 1 || Referenzen >= 힙끝 - 1 || (힙[Referenzen] != 2 && 힙[Referenzen] != 3)) Feeler_VALUE("null or invalid array");
                else 넣기(힙[Referenzen + 1], 1); continue;
            }
            if (VALUE == 192) {
                int Numm = Klass_Numm_SMS(명짧()), Referenzen = 빼기(2);
                if (!Word_SMS(Numm, "java/lang/String")) Feeler_VALUE("unsupported checkcast");
                else if (Referenzen != 0) Objet_VALUE(Referenzen, 1);
                넣기(Referenzen, 2); continue;
            }
            Feeler_VALUE("unsupported bytecode");
        }
    }
    public static int Laf() {
        if (Benotzer.인수개수() == 1 && 자바도구.같음(Benotzer.인수(0), "-version")) {
            Benotzer.schreiwen("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (Benotzer.인수개수() < 1) { Benotzer.schreiwen("Usage: java CLASS [ARGS]\n"); return 2; }
        int Längt_VALUE = 자바도구.Numm(Fichier_Numm_SMS, Benotzer.인수(0));
        if (Längt_VALUE < 1 || Längt_VALUE > 57) { Benotzer.schreiwen("java: invalid class name\n"); return 2; }
        Fichier_Numm_SMS[Längt_VALUE] = '.'; Fichier_Numm_SMS[Längt_VALUE + 1] = 'c'; Fichier_Numm_SMS[Längt_VALUE + 2] = 'l'; Fichier_Numm_SMS[Längt_VALUE + 3] = 'a'; Fichier_Numm_SMS[Längt_VALUE + 4] = 's'; Fichier_Numm_SMS[Längt_VALUE + 5] = 's';
        d_Gréisst_veränneren = Benotzer.파일읽기(Fichier_Numm_SMS, Fichier);
        if (d_Gréisst_veränneren < 0) { Benotzer.schreiwen("java: cannot read class: "); 자바도구.수쓰기(d_Gréisst_veränneren); Benotzer.schreiwen_Zeechen_VALUE(10); return 1; }
        클래스읽기(); if (Feeler) return 1;
        int Zeechen_Numm = Konstant_SMS(Klass_Numm);
        if (!Feeler && 힙[Zeechen_Numm + 1] != Längt_VALUE) Feeler_VALUE("class name does not match file");
        for (int 수 = 0; 수 < Längt_VALUE && !Feeler; 수++) if (힙[Zeechen_Numm + 2 + 수] != Fichier_Numm_SMS[수]) Feeler_VALUE("class name does not match file");
        int Agab_Punkt_VALUE = -1;
        for (int 수 = 0; 수 < Method_COUNT; 수++) if (Word_SMS(Method_Numm_SMS[수], "main") && Word_SMS(Method_TYPE[수], "([Ljava/lang/String;)V") && (Method_Zougrëff[수] & 9) == 9) Agab_Punkt_VALUE = 수;
        if (Agab_Punkt_VALUE < 0) Feeler_VALUE("public static void main(String[] args) required");
        if (Feeler) return 1;
        int 인수 = zouweisen_Späicher(3, Benotzer.인수개수() - 1);
        for (int 수 = 1; 수 < Benotzer.인수개수() && !Feeler; 수++) 힙[인수 + 1 + 수] = Host_Zeechen(Benotzer.인수(수));
        Rumm_INDEX = 0; Rumm_Method[0] = Agab_Punkt_VALUE; Rumm_positionéieren[0] = Method_Start[Agab_Punkt_VALUE]; lokal_VALUE[0] = 인수; lokal_TYPE[0] = 2;
        ausféieren_Befeel(); return Feeler ? 1 : 0;
    }
}
