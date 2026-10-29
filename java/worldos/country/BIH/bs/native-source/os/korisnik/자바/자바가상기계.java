// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Fajl/operand_snop/Reference/ogranak 경계를 Izvrši_komanda 중 검사한다. */
public final class 자바가상기계 {
    static int[] Fajl = new int[16384], fajl_naziv_SMS = new int[64];
    static int[] konstanta_oznaka = new int[512], 상가 = new int[512], konstanta_SECOND_VALUE = new int[512], string_Reference = new int[512];
    static int[] metoda_naziv_SMS = new int[32], metoda_TYPE = new int[32], metoda_pristup = new int[32];
    static int[] metoda_START = new int[32], metoda_završiti = new int[32], metoda_snop = new int[32], 함수지역 = new int[32];
    static int[] metoda_argument_COUNT = new int[32], metoda_argument_TYPE = new int[512], metoda_vratiti = new int[32];
    static int[] 경계 = new int[16384];
    static int[] lokalni_VALUE = new int[4096], lokalni_TYPE = new int[4096], operand_snop_VALUE = new int[4096], operand_snop_TYPE = new int[4096];
    static int[] kadar_metoda = new int[32], kadar_položaj = new int[32], kadar_snop = new int[32];
    static int[] 힙 = new int[8192];
    static int Veličina, 읽기위치, konstanta_COUNT, metoda_COUNT, naziv_klase, kadar_INDEX = -1, 힙끝 = 1, vratiti_TYPE;
    static boolean GRESKA;

    static void neuspjeh_VALUE(String Word_SMS) {
        if (!GRESKA) { korisnik.Piši("JVM error: "); korisnik.Piši(Word_SMS); korisnik.pisati_znak_VALUE(10); }
        GRESKA = true;
    }
    static boolean isječak(int Pokreni, int dužina_VALUE) { return Pokreni >= 0 && dužina_VALUE >= 0 && Pokreni <= Veličina - dužina_VALUE; }
    static int bajt_VALUE() {
        if (!isječak(읽기위치, 1)) { neuspjeh_VALUE("truncated class file"); return 0; }
        return Fajl[읽기위치++];
    }
    static int 짧은수() { return bajt_VALUE() << 8 | bajt_VALUE(); }
    static int cijeli_broj() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int dužina_VALUE) { if (!isječak(읽기위치, dužina_VALUE)) neuspjeh_VALUE("invalid attribute size"); else 읽기위치 += dužina_VALUE; }
    static boolean ček_konstanta(int 수, int 종류) {
        if (수 <= 0 || 수 >= konstanta_COUNT || konstanta_oznaka[수] != 종류) { neuspjeh_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Pokreni, int dužina_VALUE, String Word_SMS) {
        if (!isječak(Pokreni, dužina_VALUE) || dužina_VALUE != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < dužina_VALUE; 수++) if (Fajl[Pokreni + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static boolean Word_SMS(int konstanta_VALUE, String Word_SMS) { return ček_konstanta(konstanta_VALUE, 1) && 구간(상가[konstanta_VALUE], konstanta_SECOND_VALUE[konstanta_VALUE], Word_SMS); }
    static boolean 같은말(int 가, int SECOND_operand) {
        if (!ček_konstanta(가, 1) || !ček_konstanta(SECOND_operand, 1) || konstanta_SECOND_VALUE[가] != konstanta_SECOND_VALUE[SECOND_operand]) return false;
        for (int 수 = 0; 수 < konstanta_SECOND_VALUE[가]; 수++) if (Fajl[상가[가] + 수] != Fajl[상가[SECOND_operand] + 수]) return false;
        return true;
    }
    static int naziv_klase_SMS(int 수) { return ček_konstanta(수, 7) && ček_konstanta(상가[수], 1) ? 상가[수] : 0; }
    static int Reference_naziv(int 수) { return ček_konstanta(수, 12) && ček_konstanta(상가[수], 1) ? 상가[수] : 0; }
    static int Reference_TYPE(int 수) { return ček_konstanta(수, 12) && ček_konstanta(konstanta_SECOND_VALUE[수], 1) ? konstanta_SECOND_VALUE[수] : 0; }
    static int 서술형(int 끝, boolean prazno_TYPE) {
        if (읽기위치 >= 끝) { neuspjeh_VALUE("invalid descriptor"); return 0; }
        int VALUE = bajt_VALUE();
        if (VALUE == 'V' && prazno_TYPE) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int Pokreni = 읽기위치;
            while (읽기위치 < 끝 && Fajl[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Pokreni) neuspjeh_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        neuspjeh_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int FUNCTION_VALUE) {
        int 이전 = 읽기위치, 수 = metoda_TYPE[FUNCTION_VALUE];
        if (!ček_konstanta(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + konstanta_SECOND_VALUE[수];
        if (bajt_VALUE() != '(') neuspjeh_VALUE("invalid method descriptor");
        int stavka_COUNT = 0;
        while (!GRESKA && 읽기위치 < 끝 && Fajl[읽기위치] != ')') {
            if (stavka_COUNT == 16) { neuspjeh_VALUE("too many method arguments"); break; }
            metoda_argument_TYPE[FUNCTION_VALUE * 16 + stavka_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || bajt_VALUE() != ')') neuspjeh_VALUE("invalid method descriptor");
        metoda_vratiti[FUNCTION_VALUE] = 서술형(끝, true); metoda_argument_COUNT[FUNCTION_VALUE] = stavka_COUNT;
        if (읽기위치 != 끝) neuspjeh_VALUE("invalid method descriptor");
        읽기위치 = 이전;
    }
    static void 속성건너() {
        int stavka_COUNT = 짧은수();
        for (int 수 = 0; 수 < stavka_COUNT && !GRESKA; 수++) { ček_konstanta(짧은수(), 1); 건너(cijeli_broj()); }
    }
    static int komanda_dužina(int VALUE) {
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
        if (cijeli_broj() != 0xcafebabe) neuspjeh_VALUE("not a class file");
        int 부판 = 짧은수(), verzija_VALUE = 짧은수();
        if (verzija_VALUE < 45 || verzija_VALUE > 52 || 부판 != 0) neuspjeh_VALUE("supported class versions: 45..52, minor 0");
        konstanta_COUNT = 짧은수();
        if (konstanta_COUNT < 1 || konstanta_COUNT > 512) { neuspjeh_VALUE("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < konstanta_COUNT && !GRESKA; 수++) {
            int 종류 = bajt_VALUE(); konstanta_oznaka[수] = 종류;
            if (종류 == 1) { konstanta_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(konstanta_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = cijeli_broj();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); konstanta_SECOND_VALUE[수] = 짧은수(); }
            else neuspjeh_VALUE("unsupported constant type");
        }
        int dozvola_VALUE = 짧은수();
        if ((dozvola_VALUE & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) neuspjeh_VALUE("unsupported class flags");
        naziv_klase = naziv_klase_SMS(짧은수());
        if (!Word_SMS(naziv_klase_SMS(짧은수()), "java/lang/Object")) neuspjeh_VALUE("inheritance unsupported");
        if (짧은수() != 0) neuspjeh_VALUE("interfaces unsupported");
        if (짧은수() != 0) neuspjeh_VALUE("fields unsupported");
        metoda_COUNT = 짧은수();
        if (metoda_COUNT < 1 || metoda_COUNT > 32) { neuspjeh_VALUE("method count limit (32)"); return; }
        for (int 수 = 0; 수 < metoda_COUNT && !GRESKA; 수++) {
            metoda_pristup[수] = 짧은수(); metoda_naziv_SMS[수] = 짧은수(); metoda_TYPE[수] = 짧은수();
            ček_konstanta(metoda_naziv_SMS[수], 1); 서술읽기(수);
            if ((metoda_pristup[수] & (0x100 | 0x400 | 0x20)) != 0) neuspjeh_VALUE("native, abstract and synchronized methods unsupported");
            if ((metoda_pristup[수] & 8) == 0 && !Word_SMS(metoda_naziv_SMS[수], "<init>")) neuspjeh_VALUE("instance methods unsupported");
            if (Word_SMS(metoda_naziv_SMS[수], "<clinit>")) neuspjeh_VALUE("class initializers unsupported");
            for (int 앞 = 0; 앞 < 수; 앞++) if (같은말(metoda_naziv_SMS[앞], metoda_naziv_SMS[수]) && 같은말(metoda_TYPE[앞], metoda_TYPE[수])) neuspjeh_VALUE("duplicate method");
            int stavka_COUNT = 짧은수();
            for (int atribut_VALUE = 0; atribut_VALUE < stavka_COUNT && !GRESKA; atribut_VALUE++) {
                int Naziv = 짧은수(), dužina_VALUE = cijeli_broj(), Pokreni = 읽기위치;
                if (!isječak(Pokreni, dužina_VALUE)) { neuspjeh_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Naziv, "Code")) {
                    if (metoda_START[수] != 0) neuspjeh_VALUE("duplicate Code attribute");
                    metoda_snop[수] = 짧은수(); 함수지역[수] = 짧은수(); int kod_dužina = cijeli_broj();
                    if (metoda_snop[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < metoda_argument_COUNT[수]
                        || kod_dužina < 1 || kod_dužina > 8192) neuspjeh_VALUE("method memory limits exceeded");
                    metoda_START[수] = 읽기위치; 건너(kod_dužina); metoda_završiti[수] = 읽기위치;
                    if (짧은수() != 0) neuspjeh_VALUE("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != Pokreni + dužina_VALUE) neuspjeh_VALUE("Code attribute size mismatch");
                } else 건너(dužina_VALUE);
            }
            if (metoda_START[수] == 0) neuspjeh_VALUE("missing Code attribute");
            int prostor_za_unos_unos = metoda_START[수];
            while (prostor_za_unos_unos < metoda_završiti[수] && !GRESKA) {
                int dužina_VALUE = komanda_dužina(Fajl[prostor_za_unos_unos]);
                if (dužina_VALUE == 0 || dužina_VALUE > metoda_završiti[수] - prostor_za_unos_unos) { neuspjeh_VALUE("unsupported or truncated bytecode"); break; }
                경계[prostor_za_unos_unos] = 수 + 1; prostor_za_unos_unos += dužina_VALUE;
            }
            // 실행하지 않는 경로에도 잘못된 ogranak 목적지를 허용하지 않는다.
            prostor_za_unos_unos = metoda_START[수];
            while (prostor_za_unos_unos < metoda_završiti[수] && !GRESKA) {
                int VALUE = Fajl[prostor_za_unos_unos];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                    int odredište_VALUE = prostor_za_unos_unos + (short)(Fajl[prostor_za_unos_unos + 1] << 8 | Fajl[prostor_za_unos_unos + 2]);
                    if (odredište_VALUE < metoda_START[수] || odredište_VALUE >= metoda_završiti[수] || 경계[odredište_VALUE] != 수 + 1) neuspjeh_VALUE("invalid branch target");
                }
                prostor_za_unos_unos += komanda_dužina(VALUE);
            }
        }
        if (!GRESKA) 속성건너();
        if (읽기위치 != Veličina) neuspjeh_VALUE("extra class file data");
    }
    static int dodijeliti_Pohrana(int 종류, int dužina_VALUE) {
        if (dužina_VALUE < 0 || dužina_VALUE > 힙.length - 힙끝 - 2) { neuspjeh_VALUE("object heap exhausted or negative array size"); return 0; }
        int Reference = 힙끝; 힙끝 += dužina_VALUE + 2; 힙[Reference] = 종류; 힙[Reference + 1] = dužina_VALUE;
        return Reference;
    }
    static boolean objekt_VALUE(int Reference, int 종류) {
        if (Reference < 1 || Reference >= 힙끝 - 1 || 힙[Reference] != 종류) { neuspjeh_VALUE("null or invalid object reference"); return false; }
        return true;
    }
    static int konstanta_SMS(int INDEX) {
        if (!ček_konstanta(INDEX, 1)) return 0;
        if (string_Reference[INDEX] != 0) return string_Reference[INDEX];
        int Reference = dodijeliti_Pohrana(1, konstanta_SECOND_VALUE[INDEX]); if (GRESKA) return 0;
        int 끝 = 상가[INDEX] + konstanta_SECOND_VALUE[INDEX], 수 = 상가[INDEX], dužina_VALUE = 0;
        while (수 < 끝 && !GRESKA) {
            int VALUE = Fajl[수++];
            if (VALUE == 0) neuspjeh_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && 수 < 끝) {
                int Dalje_stavka = Fajl[수++];
                if ((Dalje_stavka & 192) != 128) neuspjeh_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | Dalje_stavka & 63;
                if (VALUE != 0 && VALUE < 128) neuspjeh_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && 수 + 1 < 끝) {
                int 가 = Fajl[수++], SECOND_operand = Fajl[수++];
                if ((가 & 192) != 128 || (SECOND_operand & 192) != 128) neuspjeh_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | SECOND_operand & 63;
                if (VALUE < 2048) neuspjeh_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) neuspjeh_VALUE("invalid modified UTF-8");
            힙[Reference + 2 + dužina_VALUE++] = VALUE;
        }
        힙[Reference + 1] = dužina_VALUE; string_Reference[INDEX] = Reference; return Reference;
    }
    static int organizator_znak(String VALUE) {
        int Reference = dodijeliti_Pohrana(1, VALUE.length()); if (GRESKA) return 0;
        for (int 수 = 0; 수 < VALUE.length(); 수++) 힙[Reference + 2 + 수] = VALUE.charAt(수);
        return Reference;
    }
    static void pisati_SMS(int Reference) {
        if (Reference == 0) { korisnik.Piši("null"); return; }
        if (!objekt_VALUE(Reference, 1)) return;
        for (int 수 = 0; 수 < 힙[Reference + 1]; 수++) korisnik.pisati_znak_VALUE(힙[Reference + 2 + 수]);
    }
    static int cifra_znak(int VALUE) {
        int Reference = dodijeliti_Pohrana(1, 11); if (GRESKA) return 0;
        int dužina_VALUE = 0;
        if (VALUE < 0) 힙[Reference + 2 + dužina_VALUE++] = '-'; else VALUE = -VALUE;
        int položaj_INDEX = 1000000000; boolean Pokreni = false;
        while (položaj_INDEX != 0) {
            int 수 = -(VALUE / položaj_INDEX);
            if (수 != 0 || Pokreni || položaj_INDEX == 1) { 힙[Reference + 2 + dužina_VALUE++] = '0' + 수; Pokreni = true; }
            VALUE %= položaj_INDEX; položaj_INDEX /= 10;
        }
        힙[Reference + 1] = dužina_VALUE; return Reference;
    }
    static int 정수해독(int Reference) {
        if (!objekt_VALUE(Reference, 1)) return 0;
        int dužina_VALUE = 힙[Reference + 1], 수 = 0, VALUE = 0; boolean 음수 = false;
        if (dužina_VALUE > 0 && (힙[Reference + 2] == '-' || 힙[Reference + 2] == '+')) { 음수 = 힙[Reference + 2] == '-'; 수++; }
        if (수 == dužina_VALUE) neuspjeh_VALUE("NumberFormatException");
        for (; 수 < dužina_VALUE && !GRESKA; 수++) {
            int cifra_VALUE = 힙[Reference + 2 + 수] - '0';
            if (cifra_VALUE < 0 || cifra_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && cifra_VALUE > (음수 ? 8 : 7)) neuspjeh_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - cifra_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int TYPE_VALUE) {
        if (GRESKA) return;
        if (kadar_INDEX < 0 || kadar_snop[kadar_INDEX] >= metoda_snop[kadar_metoda[kadar_INDEX]]) { neuspjeh_VALUE("operand stack overflow"); return; }
        int prostor_za_unos_unos = kadar_INDEX * 128 + kadar_snop[kadar_INDEX]++; operand_snop_VALUE[prostor_za_unos_unos] = VALUE; operand_snop_TYPE[prostor_za_unos_unos] = TYPE_VALUE;
    }
    static int 빼기(int TYPE_VALUE) {
        if (GRESKA) return 0;
        if (kadar_INDEX < 0 || kadar_snop[kadar_INDEX] < 1) { neuspjeh_VALUE("operand stack underflow"); return 0; }
        int prostor_za_unos_unos = kadar_INDEX * 128 + --kadar_snop[kadar_INDEX]; vratiti_TYPE = operand_snop_TYPE[prostor_za_unos_unos];
        if (TYPE_VALUE != 0 && vratiti_TYPE != TYPE_VALUE) neuspjeh_VALUE("operand type mismatch");
        return operand_snop_VALUE[prostor_za_unos_unos];
    }
    static void 지역읽기(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[kadar_metoda[kadar_INDEX]] || INDEX < 0 || lokalni_TYPE[kadar_INDEX * 128 + INDEX] != TYPE_VALUE) { neuspjeh_VALUE("invalid or uninitialized local"); return; }
        넣기(lokalni_VALUE[kadar_INDEX * 128 + INDEX], TYPE_VALUE);
    }
    static void pisati_lokalni(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[kadar_metoda[kadar_INDEX]] || INDEX < 0) { neuspjeh_VALUE("local index out of range"); return; }
        int VALUE = 빼기(TYPE_VALUE); lokalni_VALUE[kadar_INDEX * 128 + INDEX] = VALUE; lokalni_TYPE[kadar_INDEX * 128 + INDEX] = TYPE_VALUE;
    }
    static int 명바() {
        int Pozicija = kadar_položaj[kadar_INDEX];
        if (Pozicija < metoda_START[kadar_metoda[kadar_INDEX]] || Pozicija >= metoda_završiti[kadar_metoda[kadar_INDEX]]) { neuspjeh_VALUE("instruction pointer out of range"); return 0; }
        kadar_položaj[kadar_INDEX]++; return Fajl[Pozicija];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void pomaći_VALUE(int Pozicija) {
        int FUNCTION_VALUE = kadar_metoda[kadar_INDEX];
        if (Pozicija < metoda_START[FUNCTION_VALUE] || Pozicija >= metoda_završiti[FUNCTION_VALUE] || 경계[Pozicija] != FUNCTION_VALUE + 1) neuspjeh_VALUE("invalid branch target");
        else kadar_položaj[kadar_INDEX] = Pozicija;
    }
    static void 호출(int FUNCTION_VALUE) {
        if (kadar_INDEX == 31) { neuspjeh_VALUE("call stack limit (32)"); return; }
        int Dalje_stavka = kadar_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) lokalni_TYPE[Dalje_stavka * 128 + 수] = 0;
        for (int 수 = metoda_argument_COUNT[FUNCTION_VALUE] - 1; 수 >= 0; 수--) {
            lokalni_VALUE[Dalje_stavka * 128 + 수] = 빼기(metoda_argument_TYPE[FUNCTION_VALUE * 16 + 수]); lokalni_TYPE[Dalje_stavka * 128 + 수] = metoda_argument_TYPE[FUNCTION_VALUE * 16 + 수];
        }
        kadar_INDEX = Dalje_stavka; kadar_metoda[kadar_INDEX] = FUNCTION_VALUE; kadar_položaj[kadar_INDEX] = metoda_START[FUNCTION_VALUE]; kadar_snop[kadar_INDEX] = 0;
    }
    static void vratiti_mjera(int TYPE_VALUE) {
        if (TYPE_VALUE != metoda_vratiti[kadar_metoda[kadar_INDEX]]) { neuspjeh_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        kadar_INDEX--; if (kadar_INDEX >= 0 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
    }
    static int[] tok_fajl_naziv = new int[64];
    static void fajl_tok_CALL(int vlasnik_VALUE, int Naziv, int format_VALUE, int Naredba) {
        boolean Ispis = Word_SMS(vlasnik_VALUE, "java/io/FileOutputStream");
        int 종류 = Ispis ? 6 : 5;
        if (Naredba == 183 && Word_SMS(Naziv, "<init>")) {
            boolean 이어 = false;
            if (Ispis && Word_SMS(format_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(format_VALUE, "(Ljava/lang/String;)V")) { neuspjeh_VALUE("unsupported file stream constructor"); return; }
            int fajl_unos_naziv = 빼기(2), tok_VALUE = 빼기(2);
            if (!objekt_VALUE(fajl_unos_naziv, 1) || !objekt_VALUE(tok_VALUE, 종류) || GRESKA) return;
            if (힙[tok_VALUE + 3] != 0) { neuspjeh_VALUE("file stream already initialized"); return; }
            int dužina_VALUE = 힙[fajl_unos_naziv + 1];
            if (dužina_VALUE < 1 || dužina_VALUE > 63) { neuspjeh_VALUE("invalid file name length"); return; }
            for (int prostor_za_unos_unos = 0; prostor_za_unos_unos < dužina_VALUE; prostor_za_unos_unos++) {
                int VALUE = 힙[fajl_unos_naziv + 2 + prostor_za_unos_unos];
                if (VALUE < 1 || VALUE > 127) { neuspjeh_VALUE("file stream paths currently require ASCII"); return; }
                tok_fajl_naziv[prostor_za_unos_unos] = VALUE;
            }
            tok_fajl_naziv[dužina_VALUE] = 0;
            int 서술자 = korisnik.파일서술자열기(tok_fajl_naziv, Ispis ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { neuspjeh_VALUE("FileNotFoundException: file open failed"); return; }
            힙[tok_VALUE + 2] = 서술자; 힙[tok_VALUE + 3] = 1;
            return;
        }
        if (Naredba != 182) { neuspjeh_VALUE("invalid file stream invocation"); return; }
        int radnja = -1, VALUE = 0;
        if (Word_SMS(Naziv, "close") && Word_SMS(format_VALUE, "()V")) radnja = 0;
        if (!Ispis && Word_SMS(Naziv, "read") && Word_SMS(format_VALUE, "()I")) radnja = 1;
        if (Ispis && Word_SMS(Naziv, "write") && Word_SMS(format_VALUE, "(I)V")) { radnja = 2; VALUE = 빼기(1); }
        if (radnja < 0) { neuspjeh_VALUE("unsupported file stream method"); return; }
        int tok_VALUE = 빼기(2);
        if (!objekt_VALUE(tok_VALUE, 종류) || GRESKA) return;
        if (힙[tok_VALUE + 3] == 0) { neuspjeh_VALUE("uninitialized file stream"); return; }
        int 서술자 = 힙[tok_VALUE + 2];
        if (radnja == 0) {
            if (서술자 >= 0 && korisnik.파일서술자닫기(서술자) < 0) neuspjeh_VALUE("IOException: close failed");
            힙[tok_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { neuspjeh_VALUE("IOException: stream closed"); return; }
        if (radnja == 1) {
            int mjera = korisnik.파일한바이트읽기(서술자);
            if (mjera < -1) neuspjeh_VALUE("IOException: read failed"); else 넣기(mjera, 1);
        } else if (korisnik.파일한바이트쓰기(서술자, VALUE) != 1) neuspjeh_VALUE("IOException: write failed");
    }
    static void CALL_metoda(int INDEX, int Naredba) {
        if (!ček_konstanta(INDEX, 10)) return;
        int vlasnik_VALUE = naziv_klase_SMS(상가[INDEX]), Naziv = Reference_naziv(konstanta_SECOND_VALUE[INDEX]), format_VALUE = Reference_TYPE(konstanta_SECOND_VALUE[INDEX]);
        if (GRESKA) return;
        if (같은말(vlasnik_VALUE, naziv_klase)) {
            if (Naredba != 184) { neuspjeh_VALUE("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < metoda_COUNT; 수++) if (같은말(Naziv, metoda_naziv_SMS[수]) && 같은말(format_VALUE, metoda_TYPE[수])) {
                if ((metoda_pristup[수] & 8) == 0) neuspjeh_VALUE("method is not static"); else 호출(수);
                return;
            }
            neuspjeh_VALUE("NoSuchMethodError"); return;
        }
        if (Word_SMS(vlasnik_VALUE, "java/io/FileInputStream") || Word_SMS(vlasnik_VALUE, "java/io/FileOutputStream")) {
            fajl_tok_CALL(vlasnik_VALUE, Naziv, format_VALUE, Naredba); return;
        }
        if (Naredba == 184 && Word_SMS(vlasnik_VALUE, "java/lang/Integer") && Word_SMS(Naziv, "parseInt") && Word_SMS(format_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Naredba == 182 && Word_SMS(vlasnik_VALUE, "java/io/PrintStream") && (Word_SMS(Naziv, "println") || Word_SMS(Naziv, "print"))) {
            int TYPE_VALUE = 0, VALUE = 0;
            if (Word_SMS(format_VALUE, "(I)V")) { TYPE_VALUE = 1; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(Z)V")) { TYPE_VALUE = 2; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(C)V")) { TYPE_VALUE = 3; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(Ljava/lang/String;)V")) { TYPE_VALUE = 4; VALUE = 빼기(2); }
            else if (!Word_SMS(format_VALUE, "()V") || !Word_SMS(Naziv, "println")) neuspjeh_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) neuspjeh_VALUE("invalid PrintStream receiver");
            if (GRESKA) return;
            if (TYPE_VALUE == 1) 자바도구.수쓰기(VALUE);
            if (TYPE_VALUE == 2) korisnik.Piši(VALUE == 0 ? "false" : "true");
            if (TYPE_VALUE == 3) korisnik.pisati_znak_VALUE(VALUE & 65535);
            if (TYPE_VALUE == 4) pisati_SMS(VALUE);
            if (Word_SMS(Naziv, "println")) korisnik.pisati_znak_VALUE(10);
            return;
        }
        if (Naredba == 182 && Word_SMS(vlasnik_VALUE, "java/lang/String")) {
            if (Word_SMS(Naziv, "length") && Word_SMS(format_VALUE, "()I")) {
                int Reference = 빼기(2); if (objekt_VALUE(Reference, 1)) 넣기(힙[Reference + 1], 1); return;
            }
            if (Word_SMS(Naziv, "charAt") && Word_SMS(format_VALUE, "(I)C")) {
                int indeks_VALUE = 빼기(1), Reference = 빼기(2);
                if (objekt_VALUE(Reference, 1)) {
                    if (indeks_VALUE < 0 || indeks_VALUE >= 힙[Reference + 1]) neuspjeh_VALUE("StringIndexOutOfBoundsException"); else 넣기(힙[Reference + 2 + indeks_VALUE], 1);
                }
                return;
            }
        }
        if (Word_SMS(vlasnik_VALUE, "java/lang/StringBuilder")) {
            if (Naredba == 183 && Word_SMS(Naziv, "<init>") && Word_SMS(format_VALUE, "()V")) { objekt_VALUE(빼기(2), 4); return; }
            if (Naredba == 182 && Word_SMS(Naziv, "toString") && Word_SMS(format_VALUE, "()Ljava/lang/String;")) {
                int Reference = 빼기(2); if (objekt_VALUE(Reference, 4)) 넣기(힙[Reference + 2] == 0 ? organizator_znak("") : 힙[Reference + 2], 2); return;
            }
            if (Naredba == 182 && Word_SMS(Naziv, "append")) {
                int Tekst = 0;
                if (Word_SMS(format_VALUE, "(I)Ljava/lang/StringBuilder;")) Tekst = cifra_znak(빼기(1));
                else if (Word_SMS(format_VALUE, "(Z)Ljava/lang/StringBuilder;")) Tekst = organizator_znak(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(format_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); Tekst = dodijeliti_Pohrana(1, 1); if (!GRESKA) 힙[Tekst + 2] = VALUE & 65535;
                }
                else if (Word_SMS(format_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Tekst = 빼기(2); if (Tekst == 0) Tekst = organizator_znak("null"); }
                else { neuspjeh_VALUE("unsupported StringBuilder append"); return; }
                int Reference = 빼기(2); if (!objekt_VALUE(Reference, 4) || !objekt_VALUE(Tekst, 1)) return;
                int 앞 = 힙[Reference + 2], 앞길이 = 앞 == 0 ? 0 : 힙[앞 + 1], ZAD_VALUE_dužina = 힙[Tekst + 1];
                int 새글 = dodijeliti_Pohrana(1, 앞길이 + ZAD_VALUE_dužina); if (GRESKA) return;
                for (int 수 = 0; 수 < 앞길이; 수++) 힙[새글 + 2 + 수] = 힙[앞 + 2 + 수];
                for (int 수 = 0; 수 < ZAD_VALUE_dužina; 수++) 힙[새글 + 2 + 앞길이 + 수] = 힙[Tekst + 2 + 수];
                힙[Reference + 2] = 새글; 넣기(Reference, 2); return;
            }
        }
        neuspjeh_VALUE("unsupported library method");
    }
    static int niz_prostor_za_unos(int Reference, int indeks_VALUE, int TYPE_VALUE) {
        if (!objekt_VALUE(Reference, TYPE_VALUE)) return 0;
        if (indeks_VALUE < 0 || indeks_VALUE >= 힙[Reference + 1]) { neuspjeh_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return Reference + 2 + indeks_VALUE;
    }
    static void Izvrši_komanda() {
        int 남음 = 500000;
        while (kadar_INDEX >= 0 && !GRESKA) {
            if (--남음 == 0) { neuspjeh_VALUE("instruction limit (500000)"); break; }
            int Pokreni = kadar_položaj[kadar_INDEX], VALUE = 명바();
            if (GRESKA) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = VALUE == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= konstanta_COUNT) neuspjeh_VALUE("invalid ldc constant");
                else if (konstanta_oznaka[수] == 3) 넣기(상가[수], 1);
                else if (konstanta_oznaka[수] == 8) 넣기(konstanta_SMS(상가[수]), 2);
                else neuspjeh_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { pisati_lokalni(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { pisati_lokalni(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { pisati_lokalni(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE == 50) {
                int indeks_VALUE = 빼기(1), Reference = 빼기(2), prostor_za_unos_unos = niz_prostor_za_unos(Reference, indeks_VALUE, VALUE == 46 ? 2 : 3);
                if (!GRESKA) 넣기(힙[prostor_za_unos_unos], VALUE == 46 ? 1 : 2); continue;
            }
            if (VALUE == 79 || VALUE == 83) {
                int stavka_element = 빼기(VALUE == 79 ? 1 : 2), indeks_VALUE = 빼기(1), Reference = 빼기(2), prostor_za_unos_unos = niz_prostor_za_unos(Reference, indeks_VALUE, VALUE == 79 ? 2 : 3);
                if (VALUE == 83 && stavka_element != 0) objekt_VALUE(stavka_element, 1);
                if (!GRESKA) 힙[prostor_za_unos_unos] = stavka_element; continue;
            }
            if (VALUE == 87) { 빼기(0); continue; }
            if (VALUE == 89) { int 가 = 빼기(0), TYPE_VALUE = vratiti_TYPE; 넣기(가, TYPE_VALUE); 넣기(가, TYPE_VALUE); continue; }
            if (VALUE == 95) { int 가 = 빼기(0), 가형 = vratiti_TYPE, SECOND_operand = 빼기(0), SECOND_operand_TYPE = vratiti_TYPE; 넣기(가, 가형); 넣기(SECOND_operand, SECOND_operand_TYPE); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int SECOND_operand = 빼기(1), 가 = 빼기(1), mjera = 0;
                if ((VALUE == 108 || VALUE == 112) && SECOND_operand == 0) { neuspjeh_VALUE("ArithmeticException: / by zero"); continue; }
                if (VALUE == 96) mjera = 가 + SECOND_operand;
                if (VALUE == 100) mjera = 가 - SECOND_operand;
                if (VALUE == 104) mjera = 가 * SECOND_operand;
                if (VALUE == 108) mjera = 가 / SECOND_operand;
                if (VALUE == 112) mjera = 가 % SECOND_operand;
                if (VALUE == 120) mjera = 가 << SECOND_operand;
                if (VALUE == 122) mjera = 가 >> SECOND_operand;
                if (VALUE == 124) mjera = 가 >>> SECOND_operand;
                if (VALUE == 126) mjera = 가 & SECOND_operand;
                if (VALUE == 128) mjera = 가 | SECOND_operand;
                if (VALUE == 130) mjera = 가 ^ SECOND_operand;
                넣기(mjera, 1); continue;
            }
            if (VALUE == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALUE == 132) {
                int lokalni_opseg = 명바(), 증분 = (byte)명바(); 지역읽기(lokalni_opseg, 1); 넣기(빼기(1) + 증분, 1); pisati_lokalni(lokalni_opseg, 1); continue;
            }
            if (VALUE >= 145 && VALUE <= 147) {
                int 수 = 빼기(1); 넣기(VALUE == 145 ? (byte)수 : VALUE == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                int odredište_VALUE = Pokreni + (short)명짧(); boolean 갈까 = VALUE == 167;
                if (VALUE >= 153 && VALUE <= 158) {
                    int 수 = 빼기(1); 갈까 = VALUE == 153 ? 수 == 0 : VALUE == 154 ? 수 != 0 : VALUE == 155 ? 수 < 0 : VALUE == 156 ? 수 >= 0 : VALUE == 157 ? 수 > 0 : 수 <= 0;
                } else if (VALUE >= 159 && VALUE <= 166) {
                    int SECOND_operand = 빼기(VALUE >= 165 ? 2 : 1), 가 = 빼기(VALUE >= 165 ? 2 : 1);
                    갈까 = VALUE == 159 || VALUE == 165 ? 가 == SECOND_operand : VALUE == 160 || VALUE == 166 ? 가 != SECOND_operand : VALUE == 161 ? 가 < SECOND_operand : VALUE == 162 ? 가 >= SECOND_operand : VALUE == 163 ? 가 > SECOND_operand : 가 <= SECOND_operand;
                } else if (VALUE == 198 || VALUE == 199) { int 수 = 빼기(2); 갈까 = VALUE == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) pomaći_VALUE(odredište_VALUE); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { vratiti_mjera(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE == 178) {
                int 수 = 명짧(); if (!ček_konstanta(수, 9)) continue;
                if (!Word_SMS(naziv_klase_SMS(상가[수]), "java/lang/System") || !Word_SMS(Reference_naziv(konstanta_SECOND_VALUE[수]), "out")
                    || !Word_SMS(Reference_TYPE(konstanta_SECOND_VALUE[수]), "Ljava/io/PrintStream;")) neuspjeh_VALUE("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (VALUE == 182 || VALUE == 183 || VALUE == 184) { CALL_metoda(명짧(), VALUE); continue; }
            if (VALUE == 187) {
                int Naziv = naziv_klase_SMS(명짧());
                if (Word_SMS(Naziv, "java/lang/StringBuilder")) 넣기(dodijeliti_Pohrana(4, 1), 2);
                else if (Word_SMS(Naziv, "java/io/FileInputStream") || Word_SMS(Naziv, "java/io/FileOutputStream")) {
                    int Reference = dodijeliti_Pohrana(Word_SMS(Naziv, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!GRESKA) { 힙[Reference + 2] = -1; 넣기(Reference, 2); }
                } else neuspjeh_VALUE("unsupported object construction");
                continue;
            }
            if (VALUE == 188 || VALUE == 189) {
                if (VALUE == 188) { if (명바() != 10) neuspjeh_VALUE("only int[] newarray is supported"); }
                else if (!Word_SMS(naziv_klase_SMS(명짧()), "java/lang/String")) neuspjeh_VALUE("only String[] anewarray is supported");
                int dužina_VALUE = 빼기(1); 넣기(dodijeliti_Pohrana(VALUE == 188 ? 2 : 3, dužina_VALUE), 2); continue;
            }
            if (VALUE == 190) {
                int Reference = 빼기(2);
                if (Reference < 1 || Reference >= 힙끝 - 1 || (힙[Reference] != 2 && 힙[Reference] != 3)) neuspjeh_VALUE("null or invalid array");
                else 넣기(힙[Reference + 1], 1); continue;
            }
            if (VALUE == 192) {
                int Naziv = naziv_klase_SMS(명짧()), Reference = 빼기(2);
                if (!Word_SMS(Naziv, "java/lang/String")) neuspjeh_VALUE("unsupported checkcast");
                else if (Reference != 0) objekt_VALUE(Reference, 1);
                넣기(Reference, 2); continue;
            }
            neuspjeh_VALUE("unsupported bytecode");
        }
    }
    public static int Pokreni() {
        if (korisnik.인수개수() == 1 && 자바도구.같음(korisnik.Argumenti(0), "-version")) {
            korisnik.Piši("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (korisnik.인수개수() < 1) { korisnik.Piši("Usage: java CLASS [ARGS]\n"); return 2; }
        int dužina_VALUE = 자바도구.Naziv(fajl_naziv_SMS, korisnik.Argumenti(0));
        if (dužina_VALUE < 1 || dužina_VALUE > 57) { korisnik.Piši("java: invalid class name\n"); return 2; }
        fajl_naziv_SMS[dužina_VALUE] = '.'; fajl_naziv_SMS[dužina_VALUE + 1] = 'c'; fajl_naziv_SMS[dužina_VALUE + 2] = 'l'; fajl_naziv_SMS[dužina_VALUE + 3] = 'a'; fajl_naziv_SMS[dužina_VALUE + 4] = 's'; fajl_naziv_SMS[dužina_VALUE + 5] = 's';
        Veličina = korisnik.파일읽기(fajl_naziv_SMS, Fajl);
        if (Veličina < 0) { korisnik.Piši("java: cannot read class: "); 자바도구.수쓰기(Veličina); korisnik.pisati_znak_VALUE(10); return 1; }
        클래스읽기(); if (GRESKA) return 1;
        int znak_naziv = konstanta_SMS(naziv_klase);
        if (!GRESKA && 힙[znak_naziv + 1] != dužina_VALUE) neuspjeh_VALUE("class name does not match file");
        for (int 수 = 0; 수 < dužina_VALUE && !GRESKA; 수++) if (힙[znak_naziv + 2 + 수] != fajl_naziv_SMS[수]) neuspjeh_VALUE("class name does not match file");
        int unos_p_VALUE = -1;
        for (int 수 = 0; 수 < metoda_COUNT; 수++) if (Word_SMS(metoda_naziv_SMS[수], "main") && Word_SMS(metoda_TYPE[수], "([Ljava/lang/String;)V") && (metoda_pristup[수] & 9) == 9) unos_p_VALUE = 수;
        if (unos_p_VALUE < 0) neuspjeh_VALUE("public static void main(String[] args) required");
        if (GRESKA) return 1;
        int Argumenti = dodijeliti_Pohrana(3, korisnik.인수개수() - 1);
        for (int 수 = 1; 수 < korisnik.인수개수() && !GRESKA; 수++) 힙[Argumenti + 1 + 수] = organizator_znak(korisnik.Argumenti(수));
        kadar_INDEX = 0; kadar_metoda[0] = unos_p_VALUE; kadar_položaj[0] = metoda_START[unos_p_VALUE]; lokalni_VALUE[0] = Argumenti; lokalni_TYPE[0] = 2;
        Izvrši_komanda(); return GRESKA ? 1 : 0;
    }
}
