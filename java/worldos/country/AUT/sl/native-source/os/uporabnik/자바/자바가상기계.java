// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Datoteka/operand_Sklad/Gradiva/veja 경계를 Izvedi_ukaz 중 검사한다. */
public final class 자바가상기계 {
    static int[] Datoteka = new int[16384], ime_datoteke_SMS = new int[64];
    static int[] konstanta_oznaka = new int[512], 상가 = new int[512], konstanta_SECOND_VALUE = new int[512], niz_Gradiva = new int[512];
    static int[] metoda_ime_SMS = new int[32], metoda_Tip = new int[32], metoda_dostop = new int[32];
    static int[] metoda_Start = new int[32], metoda_končati_klic = new int[32], metoda_Sklad = new int[32], 함수지역 = new int[32];
    static int[] metoda_argument_COUNT = new int[32], metoda_argument_Tip = new int[512], metoda_vrni = new int[32];
    static int[] 경계 = new int[16384];
    static int[] lokalen_krajeven_VALUE = new int[4096], lokalen_krajeven_Tip = new int[4096], operand_Sklad_VALUE = new int[4096], operand_Sklad_Tip = new int[4096];
    static int[] okvir_metoda = new int[32], okvir_položaj = new int[32], okvir_Sklad = new int[32];
    static int[] kopica_VALUE = new int[8192];
    static int Velikost, 읽기위치, konstanta_COUNT, metoda_COUNT, ime_razreda, okvir_INDEX = -1, kopica_končati_klic_položaj = 1, vrni_Tip;
    static boolean NAPAKA;

    static void napaka_VALUE(String Word_SMS) {
        if (!NAPAKA) { uporabnik.Pisanje("JVM error: "); uporabnik.Pisanje(Word_SMS); uporabnik.pisati_znak_VALUE(10); }
        NAPAKA = true;
    }
    static boolean izrezek(int Zaženi, int 길이) { return Zaženi >= 0 && 길이 >= 0 && Zaženi <= Velikost - 길이; }
    static int bajt_VALUE() {
        if (!izrezek(읽기위치, 1)) { napaka_VALUE("truncated class file"); return 0; }
        return Datoteka[읽기위치++];
    }
    static int 짧은수() { return bajt_VALUE() << 8 | bajt_VALUE(); }
    static int celo_število() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int 길이) { if (!izrezek(읽기위치, 길이)) napaka_VALUE("invalid attribute size"); else 읽기위치 += 길이; }
    static boolean preveriti_konstanta(int 수, int 종류) {
        if (수 <= 0 || 수 >= konstanta_COUNT || konstanta_oznaka[수] != 종류) { napaka_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_obseg(int Zaženi, int 길이, String Word_SMS) {
        if (!izrezek(Zaženi, 길이) || 길이 != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < 길이; 수++) if (Datoteka[Zaženi + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static boolean Word_SMS(int konstanta_VALUE, String Word_SMS) { return preveriti_konstanta(konstanta_VALUE, 1) && SMS_obseg(상가[konstanta_VALUE], konstanta_SECOND_VALUE[konstanta_VALUE], Word_SMS); }
    static boolean 같은말(int 가, int SECOND_operand) {
        if (!preveriti_konstanta(가, 1) || !preveriti_konstanta(SECOND_operand, 1) || konstanta_SECOND_VALUE[가] != konstanta_SECOND_VALUE[SECOND_operand]) return false;
        for (int 수 = 0; 수 < konstanta_SECOND_VALUE[가]; 수++) if (Datoteka[상가[가] + 수] != Datoteka[상가[SECOND_operand] + 수]) return false;
        return true;
    }
    static int ime_razreda_SMS(int 수) { return preveriti_konstanta(수, 7) && preveriti_konstanta(상가[수], 1) ? 상가[수] : 0; }
    static int Gradiva_ime(int 수) { return preveriti_konstanta(수, 12) && preveriti_konstanta(상가[수], 1) ? 상가[수] : 0; }
    static int Gradiva_Tip(int 수) { return preveriti_konstanta(수, 12) && preveriti_konstanta(konstanta_SECOND_VALUE[수], 1) ? konstanta_SECOND_VALUE[수] : 0; }
    static int 서술형(int 끝, boolean prazen_Tip) {
        if (읽기위치 >= 끝) { napaka_VALUE("invalid descriptor"); return 0; }
        int VALUE = bajt_VALUE();
        if (VALUE == 'V' && prazen_Tip) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int Zaženi = 읽기위치;
            while (읽기위치 < 끝 && Datoteka[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Zaženi) napaka_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        napaka_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int FUNCTION_VALUE) {
        int 이전 = 읽기위치, 수 = metoda_Tip[FUNCTION_VALUE];
        if (!preveriti_konstanta(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + konstanta_SECOND_VALUE[수];
        if (bajt_VALUE() != '(') napaka_VALUE("invalid method descriptor");
        int element_COUNT = 0;
        while (!NAPAKA && 읽기위치 < 끝 && Datoteka[읽기위치] != ')') {
            if (element_COUNT == 16) { napaka_VALUE("too many method arguments"); break; }
            metoda_argument_Tip[FUNCTION_VALUE * 16 + element_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || bajt_VALUE() != ')') napaka_VALUE("invalid method descriptor");
        metoda_vrni[FUNCTION_VALUE] = 서술형(끝, true); metoda_argument_COUNT[FUNCTION_VALUE] = element_COUNT;
        if (읽기위치 != 끝) napaka_VALUE("invalid method descriptor");
        읽기위치 = 이전;
    }
    static void 속성건너() {
        int element_COUNT = 짧은수();
        for (int 수 = 0; 수 < element_COUNT && !NAPAKA; 수++) { preveriti_konstanta(짧은수(), 1); 건너(celo_število()); }
    }
    static int 명령길이(int VALUE) {
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
        if (celo_število() != 0xcafebabe) napaka_VALUE("not a class file");
        int 부판 = 짧은수(), različica_VALUE = 짧은수();
        if (različica_VALUE < 45 || različica_VALUE > 52 || 부판 != 0) napaka_VALUE("supported class versions: 45..52, minor 0");
        konstanta_COUNT = 짧은수();
        if (konstanta_COUNT < 1 || konstanta_COUNT > 512) { napaka_VALUE("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < konstanta_COUNT && !NAPAKA; 수++) {
            int 종류 = bajt_VALUE(); konstanta_oznaka[수] = 종류;
            if (종류 == 1) { konstanta_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(konstanta_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = celo_število();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); konstanta_SECOND_VALUE[수] = 짧은수(); }
            else napaka_VALUE("unsupported constant type");
        }
        int dovoljenje_VALUE = 짧은수();
        if ((dovoljenje_VALUE & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) napaka_VALUE("unsupported class flags");
        ime_razreda = ime_razreda_SMS(짧은수());
        if (!Word_SMS(ime_razreda_SMS(짧은수()), "java/lang/Object")) napaka_VALUE("inheritance unsupported");
        if (짧은수() != 0) napaka_VALUE("interfaces unsupported");
        if (짧은수() != 0) napaka_VALUE("fields unsupported");
        metoda_COUNT = 짧은수();
        if (metoda_COUNT < 1 || metoda_COUNT > 32) { napaka_VALUE("method count limit (32)"); return; }
        for (int 수 = 0; 수 < metoda_COUNT && !NAPAKA; 수++) {
            metoda_dostop[수] = 짧은수(); metoda_ime_SMS[수] = 짧은수(); metoda_Tip[수] = 짧은수();
            preveriti_konstanta(metoda_ime_SMS[수], 1); 서술읽기(수);
            if ((metoda_dostop[수] & (0x100 | 0x400 | 0x20)) != 0) napaka_VALUE("native, abstract and synchronized methods unsupported");
            if ((metoda_dostop[수] & 8) == 0 && !Word_SMS(metoda_ime_SMS[수], "<init>")) napaka_VALUE("instance methods unsupported");
            if (Word_SMS(metoda_ime_SMS[수], "<clinit>")) napaka_VALUE("class initializers unsupported");
            for (int sprednja_VALUE = 0; sprednja_VALUE < 수; sprednja_VALUE++) if (같은말(metoda_ime_SMS[sprednja_VALUE], metoda_ime_SMS[수]) && 같은말(metoda_Tip[sprednja_VALUE], metoda_Tip[수])) napaka_VALUE("duplicate method");
            int element_COUNT = 짧은수();
            for (int atribut_VALUE = 0; atribut_VALUE < element_COUNT && !NAPAKA; atribut_VALUE++) {
                int Ime = 짧은수(), 길이 = celo_število(), Zaženi = 읽기위치;
                if (!izrezek(Zaženi, 길이)) { napaka_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Ime, "Code")) {
                    if (metoda_Start[수] != 0) napaka_VALUE("duplicate Code attribute");
                    metoda_Sklad[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = celo_število();
                    if (metoda_Sklad[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < metoda_argument_COUNT[수]
                        || 코드길이 < 1 || 코드길이 > 8192) napaka_VALUE("method memory limits exceeded");
                    metoda_Start[수] = 읽기위치; 건너(코드길이); metoda_končati_klic[수] = 읽기위치;
                    if (짧은수() != 0) napaka_VALUE("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != Zaženi + 길이) napaka_VALUE("Code attribute size mismatch");
                } else 건너(길이);
            }
            if (metoda_Start[수] == 0) napaka_VALUE("missing Code attribute");
            int 칸 = metoda_Start[수];
            while (칸 < metoda_končati_klic[수] && !NAPAKA) {
                int 길이 = 명령길이(Datoteka[칸]);
                if (길이 == 0 || 길이 > metoda_končati_klic[수] - 칸) { napaka_VALUE("unsupported or truncated bytecode"); break; }
                경계[칸] = 수 + 1; 칸 += 길이;
            }
            // 실행하지 않는 경로에도 잘못된 veja 목적지를 허용하지 않는다.
            칸 = metoda_Start[수];
            while (칸 < metoda_končati_klic[수] && !NAPAKA) {
                int VALUE = Datoteka[칸];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                    int cilj_VALUE = 칸 + (short)(Datoteka[칸 + 1] << 8 | Datoteka[칸 + 2]);
                    if (cilj_VALUE < metoda_Start[수] || cilj_VALUE >= metoda_končati_klic[수] || 경계[cilj_VALUE] != 수 + 1) napaka_VALUE("invalid branch target");
                }
                칸 += 명령길이(VALUE);
            }
        }
        if (!NAPAKA) 속성건너();
        if (읽기위치 != Velikost) napaka_VALUE("extra class file data");
    }
    static int dodeliti_Senzor_prostora(int 종류, int 길이) {
        if (길이 < 0 || 길이 > kopica_VALUE.length - kopica_končati_klic_položaj - 2) { napaka_VALUE("object heap exhausted or negative array size"); return 0; }
        int Gradiva = kopica_končati_klic_položaj; kopica_končati_klic_položaj += 길이 + 2; kopica_VALUE[Gradiva] = 종류; kopica_VALUE[Gradiva + 1] = 길이;
        return Gradiva;
    }
    static boolean predmet_VALUE(int Gradiva, int 종류) {
        if (Gradiva < 1 || Gradiva >= kopica_končati_klic_položaj - 1 || kopica_VALUE[Gradiva] != 종류) { napaka_VALUE("null or invalid object reference"); return false; }
        return true;
    }
    static int konstanta_SMS(int INDEX) {
        if (!preveriti_konstanta(INDEX, 1)) return 0;
        if (niz_Gradiva[INDEX] != 0) return niz_Gradiva[INDEX];
        int Gradiva = dodeliti_Senzor_prostora(1, konstanta_SECOND_VALUE[INDEX]); if (NAPAKA) return 0;
        int 끝 = 상가[INDEX] + konstanta_SECOND_VALUE[INDEX], 수 = 상가[INDEX], 길이 = 0;
        while (수 < 끝 && !NAPAKA) {
            int VALUE = Datoteka[수++];
            if (VALUE == 0) napaka_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && 수 < 끝) {
                int Naprej_element = Datoteka[수++];
                if ((Naprej_element & 192) != 128) napaka_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | Naprej_element & 63;
                if (VALUE != 0 && VALUE < 128) napaka_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && 수 + 1 < 끝) {
                int 가 = Datoteka[수++], SECOND_operand = Datoteka[수++];
                if ((가 & 192) != 128 || (SECOND_operand & 192) != 128) napaka_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | SECOND_operand & 63;
                if (VALUE < 2048) napaka_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) napaka_VALUE("invalid modified UTF-8");
            kopica_VALUE[Gradiva + 2 + 길이++] = VALUE;
        }
        kopica_VALUE[Gradiva + 1] = 길이; niz_Gradiva[INDEX] = Gradiva; return Gradiva;
    }
    static int gostiti_znak(String VALUE) {
        int Gradiva = dodeliti_Senzor_prostora(1, VALUE.length()); if (NAPAKA) return 0;
        for (int 수 = 0; 수 < VALUE.length(); 수++) kopica_VALUE[Gradiva + 2 + 수] = VALUE.charAt(수);
        return Gradiva;
    }
    static void pisati_SMS(int Gradiva) {
        if (Gradiva == 0) { uporabnik.Pisanje("null"); return; }
        if (!predmet_VALUE(Gradiva, 1)) return;
        for (int 수 = 0; 수 < kopica_VALUE[Gradiva + 1]; 수++) uporabnik.pisati_znak_VALUE(kopica_VALUE[Gradiva + 2 + 수]);
    }
    static int številka_znak(int VALUE) {
        int Gradiva = dodeliti_Senzor_prostora(1, 11); if (NAPAKA) return 0;
        int 길이 = 0;
        if (VALUE < 0) kopica_VALUE[Gradiva + 2 + 길이++] = '-'; else VALUE = -VALUE;
        int kazalec_mesta = 1000000000; boolean Zaženi = false;
        while (kazalec_mesta != 0) {
            int 수 = -(VALUE / kazalec_mesta);
            if (수 != 0 || Zaženi || kazalec_mesta == 1) { kopica_VALUE[Gradiva + 2 + 길이++] = '0' + 수; Zaženi = true; }
            VALUE %= kazalec_mesta; kazalec_mesta /= 10;
        }
        kopica_VALUE[Gradiva + 1] = 길이; return Gradiva;
    }
    static int 정수해독(int Gradiva) {
        if (!predmet_VALUE(Gradiva, 1)) return 0;
        int 길이 = kopica_VALUE[Gradiva + 1], 수 = 0, VALUE = 0; boolean 음수 = false;
        if (길이 > 0 && (kopica_VALUE[Gradiva + 2] == '-' || kopica_VALUE[Gradiva + 2] == '+')) { 음수 = kopica_VALUE[Gradiva + 2] == '-'; 수++; }
        if (수 == 길이) napaka_VALUE("NumberFormatException");
        for (; 수 < 길이 && !NAPAKA; 수++) {
            int številka_VALUE = kopica_VALUE[Gradiva + 2 + 수] - '0';
            if (številka_VALUE < 0 || številka_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && številka_VALUE > (음수 ? 8 : 7)) napaka_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - številka_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int Tip_VALUE) {
        if (NAPAKA) return;
        if (okvir_INDEX < 0 || okvir_Sklad[okvir_INDEX] >= metoda_Sklad[okvir_metoda[okvir_INDEX]]) { napaka_VALUE("operand stack overflow"); return; }
        int 칸 = okvir_INDEX * 128 + okvir_Sklad[okvir_INDEX]++; operand_Sklad_VALUE[칸] = VALUE; operand_Sklad_Tip[칸] = Tip_VALUE;
    }
    static int 빼기(int Tip_VALUE) {
        if (NAPAKA) return 0;
        if (okvir_INDEX < 0 || okvir_Sklad[okvir_INDEX] < 1) { napaka_VALUE("operand stack underflow"); return 0; }
        int 칸 = okvir_INDEX * 128 + --okvir_Sklad[okvir_INDEX]; vrni_Tip = operand_Sklad_Tip[칸];
        if (Tip_VALUE != 0 && vrni_Tip != Tip_VALUE) napaka_VALUE("operand type mismatch");
        return operand_Sklad_VALUE[칸];
    }
    static void 지역읽기(int INDEX, int Tip_VALUE) {
        if (INDEX >= 함수지역[okvir_metoda[okvir_INDEX]] || INDEX < 0 || lokalen_krajeven_Tip[okvir_INDEX * 128 + INDEX] != Tip_VALUE) { napaka_VALUE("invalid or uninitialized local"); return; }
        넣기(lokalen_krajeven_VALUE[okvir_INDEX * 128 + INDEX], Tip_VALUE);
    }
    static void pisati_lokalen_krajeven(int INDEX, int Tip_VALUE) {
        if (INDEX >= 함수지역[okvir_metoda[okvir_INDEX]] || INDEX < 0) { napaka_VALUE("local index out of range"); return; }
        int VALUE = 빼기(Tip_VALUE); lokalen_krajeven_VALUE[okvir_INDEX * 128 + INDEX] = VALUE; lokalen_krajeven_Tip[okvir_INDEX * 128 + INDEX] = Tip_VALUE;
    }
    static int 명바() {
        int Položaj = okvir_položaj[okvir_INDEX];
        if (Položaj < metoda_Start[okvir_metoda[okvir_INDEX]] || Položaj >= metoda_končati_klic[okvir_metoda[okvir_INDEX]]) { napaka_VALUE("instruction pointer out of range"); return 0; }
        okvir_položaj[okvir_INDEX]++; return Datoteka[Položaj];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void premikati_VALUE(int Položaj) {
        int FUNCTION_VALUE = okvir_metoda[okvir_INDEX];
        if (Položaj < metoda_Start[FUNCTION_VALUE] || Položaj >= metoda_končati_klic[FUNCTION_VALUE] || 경계[Položaj] != FUNCTION_VALUE + 1) napaka_VALUE("invalid branch target");
        else okvir_položaj[okvir_INDEX] = Položaj;
    }
    static void 호출(int FUNCTION_VALUE) {
        if (okvir_INDEX == 31) { napaka_VALUE("call stack limit (32)"); return; }
        int Naprej_element = okvir_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) lokalen_krajeven_Tip[Naprej_element * 128 + 수] = 0;
        for (int 수 = metoda_argument_COUNT[FUNCTION_VALUE] - 1; 수 >= 0; 수--) {
            lokalen_krajeven_VALUE[Naprej_element * 128 + 수] = 빼기(metoda_argument_Tip[FUNCTION_VALUE * 16 + 수]); lokalen_krajeven_Tip[Naprej_element * 128 + 수] = metoda_argument_Tip[FUNCTION_VALUE * 16 + 수];
        }
        okvir_INDEX = Naprej_element; okvir_metoda[okvir_INDEX] = FUNCTION_VALUE; okvir_položaj[okvir_INDEX] = metoda_Start[FUNCTION_VALUE]; okvir_Sklad[okvir_INDEX] = 0;
    }
    static void vrni_KR(int Tip_VALUE) {
        if (Tip_VALUE != metoda_vrni[okvir_metoda[okvir_INDEX]]) { napaka_VALUE("return type mismatch"); return; }
        int VALUE = Tip_VALUE == 0 ? 0 : 빼기(Tip_VALUE);
        okvir_INDEX--; if (okvir_INDEX >= 0 && Tip_VALUE != 0) 넣기(VALUE, Tip_VALUE);
    }
    static int[] tok_ime_datoteke = new int[64];
    static void Datoteka_tok_CALL(int lastnik_VALUE, int Ime, int oblika_VALUE, int Ukaz) {
        boolean Izpis = Word_SMS(lastnik_VALUE, "java/io/FileOutputStream");
        int 종류 = Izpis ? 6 : 5;
        if (Ukaz == 183 && Word_SMS(Ime, "<init>")) {
            boolean 이어 = false;
            if (Izpis && Word_SMS(oblika_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(oblika_VALUE, "(Ljava/lang/String;)V")) { napaka_VALUE("unsupported file stream constructor"); return; }
            int Datoteka_vnos_ime = 빼기(2), tok_VALUE = 빼기(2);
            if (!predmet_VALUE(Datoteka_vnos_ime, 1) || !predmet_VALUE(tok_VALUE, 종류) || NAPAKA) return;
            if (kopica_VALUE[tok_VALUE + 3] != 0) { napaka_VALUE("file stream already initialized"); return; }
            int 길이 = kopica_VALUE[Datoteka_vnos_ime + 1];
            if (길이 < 1 || 길이 > 63) { napaka_VALUE("invalid file name length"); return; }
            for (int 칸 = 0; 칸 < 길이; 칸++) {
                int VALUE = kopica_VALUE[Datoteka_vnos_ime + 2 + 칸];
                if (VALUE < 1 || VALUE > 127) { napaka_VALUE("file stream paths currently require ASCII"); return; }
                tok_ime_datoteke[칸] = VALUE;
            }
            tok_ime_datoteke[길이] = 0;
            int 서술자 = uporabnik.파일서술자열기(tok_ime_datoteke, Izpis ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { napaka_VALUE("FileNotFoundException: file open failed"); return; }
            kopica_VALUE[tok_VALUE + 2] = 서술자; kopica_VALUE[tok_VALUE + 3] = 1;
            return;
        }
        if (Ukaz != 182) { napaka_VALUE("invalid file stream invocation"); return; }
        int Dejanje = -1, VALUE = 0;
        if (Word_SMS(Ime, "close") && Word_SMS(oblika_VALUE, "()V")) Dejanje = 0;
        if (!Izpis && Word_SMS(Ime, "read") && Word_SMS(oblika_VALUE, "()I")) Dejanje = 1;
        if (Izpis && Word_SMS(Ime, "write") && Word_SMS(oblika_VALUE, "(I)V")) { Dejanje = 2; VALUE = 빼기(1); }
        if (Dejanje < 0) { napaka_VALUE("unsupported file stream method"); return; }
        int tok_VALUE = 빼기(2);
        if (!predmet_VALUE(tok_VALUE, 종류) || NAPAKA) return;
        if (kopica_VALUE[tok_VALUE + 3] == 0) { napaka_VALUE("uninitialized file stream"); return; }
        int 서술자 = kopica_VALUE[tok_VALUE + 2];
        if (Dejanje == 0) {
            if (서술자 >= 0 && uporabnik.파일서술자닫기(서술자) < 0) napaka_VALUE("IOException: close failed");
            kopica_VALUE[tok_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { napaka_VALUE("IOException: stream closed"); return; }
        if (Dejanje == 1) {
            int REZULTAT = uporabnik.파일한바이트읽기(서술자);
            if (REZULTAT < -1) napaka_VALUE("IOException: read failed"); else 넣기(REZULTAT, 1);
        } else if (uporabnik.파일한바이트쓰기(서술자, VALUE) != 1) napaka_VALUE("IOException: write failed");
    }
    static void CALL_metoda(int INDEX, int Ukaz) {
        if (!preveriti_konstanta(INDEX, 10)) return;
        int lastnik_VALUE = ime_razreda_SMS(상가[INDEX]), Ime = Gradiva_ime(konstanta_SECOND_VALUE[INDEX]), oblika_VALUE = Gradiva_Tip(konstanta_SECOND_VALUE[INDEX]);
        if (NAPAKA) return;
        if (같은말(lastnik_VALUE, ime_razreda)) {
            if (Ukaz != 184) { napaka_VALUE("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < metoda_COUNT; 수++) if (같은말(Ime, metoda_ime_SMS[수]) && 같은말(oblika_VALUE, metoda_Tip[수])) {
                if ((metoda_dostop[수] & 8) == 0) napaka_VALUE("method is not static"); else 호출(수);
                return;
            }
            napaka_VALUE("NoSuchMethodError"); return;
        }
        if (Word_SMS(lastnik_VALUE, "java/io/FileInputStream") || Word_SMS(lastnik_VALUE, "java/io/FileOutputStream")) {
            Datoteka_tok_CALL(lastnik_VALUE, Ime, oblika_VALUE, Ukaz); return;
        }
        if (Ukaz == 184 && Word_SMS(lastnik_VALUE, "java/lang/Integer") && Word_SMS(Ime, "parseInt") && Word_SMS(oblika_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Ukaz == 182 && Word_SMS(lastnik_VALUE, "java/io/PrintStream") && (Word_SMS(Ime, "println") || Word_SMS(Ime, "print"))) {
            int Tip_VALUE = 0, VALUE = 0;
            if (Word_SMS(oblika_VALUE, "(I)V")) { Tip_VALUE = 1; VALUE = 빼기(1); }
            else if (Word_SMS(oblika_VALUE, "(Z)V")) { Tip_VALUE = 2; VALUE = 빼기(1); }
            else if (Word_SMS(oblika_VALUE, "(C)V")) { Tip_VALUE = 3; VALUE = 빼기(1); }
            else if (Word_SMS(oblika_VALUE, "(Ljava/lang/String;)V")) { Tip_VALUE = 4; VALUE = 빼기(2); }
            else if (!Word_SMS(oblika_VALUE, "()V") || !Word_SMS(Ime, "println")) napaka_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) napaka_VALUE("invalid PrintStream receiver");
            if (NAPAKA) return;
            if (Tip_VALUE == 1) 자바도구.수쓰기(VALUE);
            if (Tip_VALUE == 2) uporabnik.Pisanje(VALUE == 0 ? "false" : "true");
            if (Tip_VALUE == 3) uporabnik.pisati_znak_VALUE(VALUE & 65535);
            if (Tip_VALUE == 4) pisati_SMS(VALUE);
            if (Word_SMS(Ime, "println")) uporabnik.pisati_znak_VALUE(10);
            return;
        }
        if (Ukaz == 182 && Word_SMS(lastnik_VALUE, "java/lang/String")) {
            if (Word_SMS(Ime, "length") && Word_SMS(oblika_VALUE, "()I")) {
                int Gradiva = 빼기(2); if (predmet_VALUE(Gradiva, 1)) 넣기(kopica_VALUE[Gradiva + 1], 1); return;
            }
            if (Word_SMS(Ime, "charAt") && Word_SMS(oblika_VALUE, "(I)C")) {
                int podpisano_VALUE = 빼기(1), Gradiva = 빼기(2);
                if (predmet_VALUE(Gradiva, 1)) {
                    if (podpisano_VALUE < 0 || podpisano_VALUE >= kopica_VALUE[Gradiva + 1]) napaka_VALUE("StringIndexOutOfBoundsException"); else 넣기(kopica_VALUE[Gradiva + 2 + podpisano_VALUE], 1);
                }
                return;
            }
        }
        if (Word_SMS(lastnik_VALUE, "java/lang/StringBuilder")) {
            if (Ukaz == 183 && Word_SMS(Ime, "<init>") && Word_SMS(oblika_VALUE, "()V")) { predmet_VALUE(빼기(2), 4); return; }
            if (Ukaz == 182 && Word_SMS(Ime, "toString") && Word_SMS(oblika_VALUE, "()Ljava/lang/String;")) {
                int Gradiva = 빼기(2); if (predmet_VALUE(Gradiva, 4)) 넣기(kopica_VALUE[Gradiva + 2] == 0 ? gostiti_znak("") : kopica_VALUE[Gradiva + 2], 2); return;
            }
            if (Ukaz == 182 && Word_SMS(Ime, "append")) {
                int Besedilo = 0;
                if (Word_SMS(oblika_VALUE, "(I)Ljava/lang/StringBuilder;")) Besedilo = številka_znak(빼기(1));
                else if (Word_SMS(oblika_VALUE, "(Z)Ljava/lang/StringBuilder;")) Besedilo = gostiti_znak(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(oblika_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); Besedilo = dodeliti_Senzor_prostora(1, 1); if (!NAPAKA) kopica_VALUE[Besedilo + 2] = VALUE & 65535;
                }
                else if (Word_SMS(oblika_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Besedilo = 빼기(2); if (Besedilo == 0) Besedilo = gostiti_znak("null"); }
                else { napaka_VALUE("unsupported StringBuilder append"); return; }
                int Gradiva = 빼기(2); if (!predmet_VALUE(Gradiva, 4) || !predmet_VALUE(Besedilo, 1)) return;
                int sprednja_VALUE = kopica_VALUE[Gradiva + 2], 앞길이 = sprednja_VALUE == 0 ? 0 : kopica_VALUE[sprednja_VALUE + 1], 뒤길이 = kopica_VALUE[Besedilo + 1];
                int 새글 = dodeliti_Senzor_prostora(1, 앞길이 + 뒤길이); if (NAPAKA) return;
                for (int 수 = 0; 수 < 앞길이; 수++) kopica_VALUE[새글 + 2 + 수] = kopica_VALUE[sprednja_VALUE + 2 + 수];
                for (int 수 = 0; 수 < 뒤길이; 수++) kopica_VALUE[새글 + 2 + 앞길이 + 수] = kopica_VALUE[Besedilo + 2 + 수];
                kopica_VALUE[Gradiva + 2] = 새글; 넣기(Gradiva, 2); return;
            }
        }
        napaka_VALUE("unsupported library method");
    }
    static int 배열칸(int Gradiva, int podpisano_VALUE, int Tip_VALUE) {
        if (!predmet_VALUE(Gradiva, Tip_VALUE)) return 0;
        if (podpisano_VALUE < 0 || podpisano_VALUE >= kopica_VALUE[Gradiva + 1]) { napaka_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return Gradiva + 2 + podpisano_VALUE;
    }
    static void Izvedi_ukaz() {
        int 남음 = 500000;
        while (okvir_INDEX >= 0 && !NAPAKA) {
            if (--남음 == 0) { napaka_VALUE("instruction limit (500000)"); break; }
            int Zaženi = okvir_položaj[okvir_INDEX], VALUE = 명바();
            if (NAPAKA) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = VALUE == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= konstanta_COUNT) napaka_VALUE("invalid ldc constant");
                else if (konstanta_oznaka[수] == 3) 넣기(상가[수], 1);
                else if (konstanta_oznaka[수] == 8) 넣기(konstanta_SMS(상가[수]), 2);
                else napaka_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { pisati_lokalen_krajeven(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { pisati_lokalen_krajeven(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { pisati_lokalen_krajeven(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE == 50) {
                int podpisano_VALUE = 빼기(1), Gradiva = 빼기(2), 칸 = 배열칸(Gradiva, podpisano_VALUE, VALUE == 46 ? 2 : 3);
                if (!NAPAKA) 넣기(kopica_VALUE[칸], VALUE == 46 ? 1 : 2); continue;
            }
            if (VALUE == 79 || VALUE == 83) {
                int element_element = 빼기(VALUE == 79 ? 1 : 2), podpisano_VALUE = 빼기(1), Gradiva = 빼기(2), 칸 = 배열칸(Gradiva, podpisano_VALUE, VALUE == 79 ? 2 : 3);
                if (VALUE == 83 && element_element != 0) predmet_VALUE(element_element, 1);
                if (!NAPAKA) kopica_VALUE[칸] = element_element; continue;
            }
            if (VALUE == 87) { 빼기(0); continue; }
            if (VALUE == 89) { int 가 = 빼기(0), Tip_VALUE = vrni_Tip; 넣기(가, Tip_VALUE); 넣기(가, Tip_VALUE); continue; }
            if (VALUE == 95) { int 가 = 빼기(0), 가형 = vrni_Tip, SECOND_operand = 빼기(0), SECOND_operand_Tip = vrni_Tip; 넣기(가, 가형); 넣기(SECOND_operand, SECOND_operand_Tip); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int SECOND_operand = 빼기(1), 가 = 빼기(1), REZULTAT = 0;
                if ((VALUE == 108 || VALUE == 112) && SECOND_operand == 0) { napaka_VALUE("ArithmeticException: / by zero"); continue; }
                if (VALUE == 96) REZULTAT = 가 + SECOND_operand;
                if (VALUE == 100) REZULTAT = 가 - SECOND_operand;
                if (VALUE == 104) REZULTAT = 가 * SECOND_operand;
                if (VALUE == 108) REZULTAT = 가 / SECOND_operand;
                if (VALUE == 112) REZULTAT = 가 % SECOND_operand;
                if (VALUE == 120) REZULTAT = 가 << SECOND_operand;
                if (VALUE == 122) REZULTAT = 가 >> SECOND_operand;
                if (VALUE == 124) REZULTAT = 가 >>> SECOND_operand;
                if (VALUE == 126) REZULTAT = 가 & SECOND_operand;
                if (VALUE == 128) REZULTAT = 가 | SECOND_operand;
                if (VALUE == 130) REZULTAT = 가 ^ SECOND_operand;
                넣기(REZULTAT, 1); continue;
            }
            if (VALUE == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALUE == 132) {
                int lokalen_krajeven_obseg = 명바(), 증분 = (byte)명바(); 지역읽기(lokalen_krajeven_obseg, 1); 넣기(빼기(1) + 증분, 1); pisati_lokalen_krajeven(lokalen_krajeven_obseg, 1); continue;
            }
            if (VALUE >= 145 && VALUE <= 147) {
                int 수 = 빼기(1); 넣기(VALUE == 145 ? (byte)수 : VALUE == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                int cilj_VALUE = Zaženi + (short)명짧(); boolean 갈까 = VALUE == 167;
                if (VALUE >= 153 && VALUE <= 158) {
                    int 수 = 빼기(1); 갈까 = VALUE == 153 ? 수 == 0 : VALUE == 154 ? 수 != 0 : VALUE == 155 ? 수 < 0 : VALUE == 156 ? 수 >= 0 : VALUE == 157 ? 수 > 0 : 수 <= 0;
                } else if (VALUE >= 159 && VALUE <= 166) {
                    int SECOND_operand = 빼기(VALUE >= 165 ? 2 : 1), 가 = 빼기(VALUE >= 165 ? 2 : 1);
                    갈까 = VALUE == 159 || VALUE == 165 ? 가 == SECOND_operand : VALUE == 160 || VALUE == 166 ? 가 != SECOND_operand : VALUE == 161 ? 가 < SECOND_operand : VALUE == 162 ? 가 >= SECOND_operand : VALUE == 163 ? 가 > SECOND_operand : 가 <= SECOND_operand;
                } else if (VALUE == 198 || VALUE == 199) { int 수 = 빼기(2); 갈까 = VALUE == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) premikati_VALUE(cilj_VALUE); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { vrni_KR(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE == 178) {
                int 수 = 명짧(); if (!preveriti_konstanta(수, 9)) continue;
                if (!Word_SMS(ime_razreda_SMS(상가[수]), "java/lang/System") || !Word_SMS(Gradiva_ime(konstanta_SECOND_VALUE[수]), "out")
                    || !Word_SMS(Gradiva_Tip(konstanta_SECOND_VALUE[수]), "Ljava/io/PrintStream;")) napaka_VALUE("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (VALUE == 182 || VALUE == 183 || VALUE == 184) { CALL_metoda(명짧(), VALUE); continue; }
            if (VALUE == 187) {
                int Ime = ime_razreda_SMS(명짧());
                if (Word_SMS(Ime, "java/lang/StringBuilder")) 넣기(dodeliti_Senzor_prostora(4, 1), 2);
                else if (Word_SMS(Ime, "java/io/FileInputStream") || Word_SMS(Ime, "java/io/FileOutputStream")) {
                    int Gradiva = dodeliti_Senzor_prostora(Word_SMS(Ime, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!NAPAKA) { kopica_VALUE[Gradiva + 2] = -1; 넣기(Gradiva, 2); }
                } else napaka_VALUE("unsupported object construction");
                continue;
            }
            if (VALUE == 188 || VALUE == 189) {
                if (VALUE == 188) { if (명바() != 10) napaka_VALUE("only int[] newarray is supported"); }
                else if (!Word_SMS(ime_razreda_SMS(명짧()), "java/lang/String")) napaka_VALUE("only String[] anewarray is supported");
                int 길이 = 빼기(1); 넣기(dodeliti_Senzor_prostora(VALUE == 188 ? 2 : 3, 길이), 2); continue;
            }
            if (VALUE == 190) {
                int Gradiva = 빼기(2);
                if (Gradiva < 1 || Gradiva >= kopica_končati_klic_položaj - 1 || (kopica_VALUE[Gradiva] != 2 && kopica_VALUE[Gradiva] != 3)) napaka_VALUE("null or invalid array");
                else 넣기(kopica_VALUE[Gradiva + 1], 1); continue;
            }
            if (VALUE == 192) {
                int Ime = ime_razreda_SMS(명짧()), Gradiva = 빼기(2);
                if (!Word_SMS(Ime, "java/lang/String")) napaka_VALUE("unsupported checkcast");
                else if (Gradiva != 0) predmet_VALUE(Gradiva, 1);
                넣기(Gradiva, 2); continue;
            }
            napaka_VALUE("unsupported bytecode");
        }
    }
    public static int Zaženi() {
        if (uporabnik.인수개수() == 1 && 자바도구.같음(uporabnik.Argumenti(0), "-version")) {
            uporabnik.Pisanje("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (uporabnik.인수개수() < 1) { uporabnik.Pisanje("Usage: java CLASS [ARGS]\n"); return 2; }
        int 길이 = 자바도구.Ime(ime_datoteke_SMS, uporabnik.Argumenti(0));
        if (길이 < 1 || 길이 > 57) { uporabnik.Pisanje("java: invalid class name\n"); return 2; }
        ime_datoteke_SMS[길이] = '.'; ime_datoteke_SMS[길이 + 1] = 'c'; ime_datoteke_SMS[길이 + 2] = 'l'; ime_datoteke_SMS[길이 + 3] = 'a'; ime_datoteke_SMS[길이 + 4] = 's'; ime_datoteke_SMS[길이 + 5] = 's';
        Velikost = uporabnik.파일읽기(ime_datoteke_SMS, Datoteka);
        if (Velikost < 0) { uporabnik.Pisanje("java: cannot read class: "); 자바도구.수쓰기(Velikost); uporabnik.pisati_znak_VALUE(10); return 1; }
        클래스읽기(); if (NAPAKA) return 1;
        int znak_ime = konstanta_SMS(ime_razreda);
        if (!NAPAKA && kopica_VALUE[znak_ime + 1] != 길이) napaka_VALUE("class name does not match file");
        for (int 수 = 0; 수 < 길이 && !NAPAKA; 수++) if (kopica_VALUE[znak_ime + 2 + 수] != ime_datoteke_SMS[수]) napaka_VALUE("class name does not match file");
        int vnos_p_VALUE = -1;
        for (int 수 = 0; 수 < metoda_COUNT; 수++) if (Word_SMS(metoda_ime_SMS[수], "main") && Word_SMS(metoda_Tip[수], "([Ljava/lang/String;)V") && (metoda_dostop[수] & 9) == 9) vnos_p_VALUE = 수;
        if (vnos_p_VALUE < 0) napaka_VALUE("public static void main(String[] args) required");
        if (NAPAKA) return 1;
        int Argumenti = dodeliti_Senzor_prostora(3, uporabnik.인수개수() - 1);
        for (int 수 = 1; 수 < uporabnik.인수개수() && !NAPAKA; 수++) kopica_VALUE[Argumenti + 1 + 수] = gostiti_znak(uporabnik.Argumenti(수));
        okvir_INDEX = 0; okvir_metoda[0] = vnos_p_VALUE; okvir_položaj[0] = metoda_Start[vnos_p_VALUE]; lokalen_krajeven_VALUE[0] = Argumenti; lokalen_krajeven_Tip[0] = 2;
        Izvedi_ukaz(); return NAPAKA ? 1 : 0;
    }
}
