// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Datoteka/operand_hrpa/Reference/grana 경계를 Izvrši_naredba 중 검사한다. */
public final class 자바가상기계 {
    static int[] Datoteka = new int[16384], naziv_datoteke_SMS = new int[64];
    static int[] konstanta_oznaka = new int[512], 상가 = new int[512], konstanta_SECOND_VALUE = new int[512], niz_Reference = new int[512];
    static int[] postupak_naziv_SMS = new int[32], postupak_TYPE = new int[32], postupak_pristup = new int[32];
    static int[] postupak_START = new int[32], postupak_završiti_razgovor = new int[32], postupak_hrpa = new int[32], 함수지역 = new int[32];
    static int[] postupak_argument_COUNT = new int[32], postupak_argument_TYPE = new int[512], postupak_vratiti = new int[32];
    static int[] 경계 = new int[16384];
    static int[] lokalno_VALUE = new int[4096], lokalno_TYPE = new int[4096], operand_hrpa_VALUE = new int[4096], operand_hrpa_TYPE = new int[4096];
    static int[] kadar_postupak = new int[32], kadar_položaj = new int[32], kadar_hrpa = new int[32];
    static int[] 힙 = new int[8192];
    static int Veličina, 읽기위치, konstanta_COUNT, postupak_COUNT, naziv_klase, kadar_INDEX = -1, 힙끝 = 1, vratiti_TYPE;
    static boolean GREŠKA;

    static void kvar_VALUE(String Word_SMS) {
        if (!GREŠKA) { korisnik.Zapisuj("JVM error: "); korisnik.Zapisuj(Word_SMS); korisnik.zapisivanje_znak_VALUE(10); }
        GREŠKA = true;
    }
    static boolean isječak(int Pokreni, int 길이) { return Pokreni >= 0 && 길이 >= 0 && Pokreni <= Veličina - 길이; }
    static int bajt_VALUE() {
        if (!isječak(읽기위치, 1)) { kvar_VALUE("truncated class file"); return 0; }
        return Datoteka[읽기위치++];
    }
    static int 짧은수() { return bajt_VALUE() << 8 | bajt_VALUE(); }
    static int cijeli_broj() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int 길이) { if (!isječak(읽기위치, 길이)) kvar_VALUE("invalid attribute size"); else 읽기위치 += 길이; }
    static boolean 상검사(int 수, int 종류) {
        if (수 <= 0 || 수 >= konstanta_COUNT || konstanta_oznaka[수] != 종류) { kvar_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_raspon(int Pokreni, int 길이, String Word_SMS) {
        if (!isječak(Pokreni, 길이) || 길이 != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < 길이; 수++) if (Datoteka[Pokreni + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static boolean Word_SMS(int konstanta_VALUE, String Word_SMS) { return 상검사(konstanta_VALUE, 1) && SMS_raspon(상가[konstanta_VALUE], konstanta_SECOND_VALUE[konstanta_VALUE], Word_SMS); }
    static boolean 같은말(int 가, int SECOND_operand) {
        if (!상검사(가, 1) || !상검사(SECOND_operand, 1) || konstanta_SECOND_VALUE[가] != konstanta_SECOND_VALUE[SECOND_operand]) return false;
        for (int 수 = 0; 수 < konstanta_SECOND_VALUE[가]; 수++) if (Datoteka[상가[가] + 수] != Datoteka[상가[SECOND_operand] + 수]) return false;
        return true;
    }
    static int naziv_klase_SMS(int 수) { return 상검사(수, 7) && 상검사(상가[수], 1) ? 상가[수] : 0; }
    static int Reference_naziv(int 수) { return 상검사(수, 12) && 상검사(상가[수], 1) ? 상가[수] : 0; }
    static int Reference_TYPE(int 수) { return 상검사(수, 12) && 상검사(konstanta_SECOND_VALUE[수], 1) ? konstanta_SECOND_VALUE[수] : 0; }
    static int 서술형(int 끝, boolean 빈형) {
        if (읽기위치 >= 끝) { kvar_VALUE("invalid descriptor"); return 0; }
        int VALUE = bajt_VALUE();
        if (VALUE == 'V' && 빈형) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int Pokreni = 읽기위치;
            while (읽기위치 < 끝 && Datoteka[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Pokreni) kvar_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        kvar_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int FUNCTION_VALUE) {
        int 이전 = 읽기위치, 수 = postupak_TYPE[FUNCTION_VALUE];
        if (!상검사(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + konstanta_SECOND_VALUE[수];
        if (bajt_VALUE() != '(') kvar_VALUE("invalid method descriptor");
        int artikl_COUNT = 0;
        while (!GREŠKA && 읽기위치 < 끝 && Datoteka[읽기위치] != ')') {
            if (artikl_COUNT == 16) { kvar_VALUE("too many method arguments"); break; }
            postupak_argument_TYPE[FUNCTION_VALUE * 16 + artikl_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || bajt_VALUE() != ')') kvar_VALUE("invalid method descriptor");
        postupak_vratiti[FUNCTION_VALUE] = 서술형(끝, true); postupak_argument_COUNT[FUNCTION_VALUE] = artikl_COUNT;
        if (읽기위치 != 끝) kvar_VALUE("invalid method descriptor");
        읽기위치 = 이전;
    }
    static void 속성건너() {
        int artikl_COUNT = 짧은수();
        for (int 수 = 0; 수 < artikl_COUNT && !GREŠKA; 수++) { 상검사(짧은수(), 1); 건너(cijeli_broj()); }
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
        if (cijeli_broj() != 0xcafebabe) kvar_VALUE("not a class file");
        int 부판 = 짧은수(), verzija_VALUE = 짧은수();
        if (verzija_VALUE < 45 || verzija_VALUE > 52 || 부판 != 0) kvar_VALUE("supported class versions: 45..52, minor 0");
        konstanta_COUNT = 짧은수();
        if (konstanta_COUNT < 1 || konstanta_COUNT > 512) { kvar_VALUE("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < konstanta_COUNT && !GREŠKA; 수++) {
            int 종류 = bajt_VALUE(); konstanta_oznaka[수] = 종류;
            if (종류 == 1) { konstanta_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(konstanta_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = cijeli_broj();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); konstanta_SECOND_VALUE[수] = 짧은수(); }
            else kvar_VALUE("unsupported constant type");
        }
        int dozvola_VALUE = 짧은수();
        if ((dozvola_VALUE & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) kvar_VALUE("unsupported class flags");
        naziv_klase = naziv_klase_SMS(짧은수());
        if (!Word_SMS(naziv_klase_SMS(짧은수()), "java/lang/Object")) kvar_VALUE("inheritance unsupported");
        if (짧은수() != 0) kvar_VALUE("interfaces unsupported");
        if (짧은수() != 0) kvar_VALUE("fields unsupported");
        postupak_COUNT = 짧은수();
        if (postupak_COUNT < 1 || postupak_COUNT > 32) { kvar_VALUE("method count limit (32)"); return; }
        for (int 수 = 0; 수 < postupak_COUNT && !GREŠKA; 수++) {
            postupak_pristup[수] = 짧은수(); postupak_naziv_SMS[수] = 짧은수(); postupak_TYPE[수] = 짧은수();
            상검사(postupak_naziv_SMS[수], 1); 서술읽기(수);
            if ((postupak_pristup[수] & (0x100 | 0x400 | 0x20)) != 0) kvar_VALUE("native, abstract and synchronized methods unsupported");
            if ((postupak_pristup[수] & 8) == 0 && !Word_SMS(postupak_naziv_SMS[수], "<init>")) kvar_VALUE("instance methods unsupported");
            if (Word_SMS(postupak_naziv_SMS[수], "<clinit>")) kvar_VALUE("class initializers unsupported");
            for (int prednja_VALUE = 0; prednja_VALUE < 수; prednja_VALUE++) if (같은말(postupak_naziv_SMS[prednja_VALUE], postupak_naziv_SMS[수]) && 같은말(postupak_TYPE[prednja_VALUE], postupak_TYPE[수])) kvar_VALUE("duplicate method");
            int artikl_COUNT = 짧은수();
            for (int atribut_VALUE = 0; atribut_VALUE < artikl_COUNT && !GREŠKA; atribut_VALUE++) {
                int Ime = 짧은수(), 길이 = cijeli_broj(), Pokreni = 읽기위치;
                if (!isječak(Pokreni, 길이)) { kvar_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Ime, "Code")) {
                    if (postupak_START[수] != 0) kvar_VALUE("duplicate Code attribute");
                    postupak_hrpa[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = cijeli_broj();
                    if (postupak_hrpa[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < postupak_argument_COUNT[수]
                        || 코드길이 < 1 || 코드길이 > 8192) kvar_VALUE("method memory limits exceeded");
                    postupak_START[수] = 읽기위치; 건너(코드길이); postupak_završiti_razgovor[수] = 읽기위치;
                    if (짧은수() != 0) kvar_VALUE("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != Pokreni + 길이) kvar_VALUE("Code attribute size mismatch");
                } else 건너(길이);
            }
            if (postupak_START[수] == 0) kvar_VALUE("missing Code attribute");
            int 칸 = postupak_START[수];
            while (칸 < postupak_završiti_razgovor[수] && !GREŠKA) {
                int 길이 = 명령길이(Datoteka[칸]);
                if (길이 == 0 || 길이 > postupak_završiti_razgovor[수] - 칸) { kvar_VALUE("unsupported or truncated bytecode"); break; }
                경계[칸] = 수 + 1; 칸 += 길이;
            }
            // 실행하지 않는 경로에도 잘못된 grana 목적지를 허용하지 않는다.
            칸 = postupak_START[수];
            while (칸 < postupak_završiti_razgovor[수] && !GREŠKA) {
                int VALUE = Datoteka[칸];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                    int odredište_VALUE = 칸 + (short)(Datoteka[칸 + 1] << 8 | Datoteka[칸 + 2]);
                    if (odredište_VALUE < postupak_START[수] || odredište_VALUE >= postupak_završiti_razgovor[수] || 경계[odredište_VALUE] != 수 + 1) kvar_VALUE("invalid branch target");
                }
                칸 += 명령길이(VALUE);
            }
        }
        if (!GREŠKA) 속성건너();
        if (읽기위치 != Veličina) kvar_VALUE("extra class file data");
    }
    static int dodijeli_Pohrana(int 종류, int 길이) {
        if (길이 < 0 || 길이 > 힙.length - 힙끝 - 2) { kvar_VALUE("object heap exhausted or negative array size"); return 0; }
        int Reference = 힙끝; 힙끝 += 길이 + 2; 힙[Reference] = 종류; 힙[Reference + 1] = 길이;
        return Reference;
    }
    static boolean objekt_VALUE(int Reference, int 종류) {
        if (Reference < 1 || Reference >= 힙끝 - 1 || 힙[Reference] != 종류) { kvar_VALUE("null or invalid object reference"); return false; }
        return true;
    }
    static int konstanta_SMS(int INDEX) {
        if (!상검사(INDEX, 1)) return 0;
        if (niz_Reference[INDEX] != 0) return niz_Reference[INDEX];
        int Reference = dodijeli_Pohrana(1, konstanta_SECOND_VALUE[INDEX]); if (GREŠKA) return 0;
        int 끝 = 상가[INDEX] + konstanta_SECOND_VALUE[INDEX], 수 = 상가[INDEX], 길이 = 0;
        while (수 < 끝 && !GREŠKA) {
            int VALUE = Datoteka[수++];
            if (VALUE == 0) kvar_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && 수 < 끝) {
                int Dalje_artikl = Datoteka[수++];
                if ((Dalje_artikl & 192) != 128) kvar_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | Dalje_artikl & 63;
                if (VALUE != 0 && VALUE < 128) kvar_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && 수 + 1 < 끝) {
                int 가 = Datoteka[수++], SECOND_operand = Datoteka[수++];
                if ((가 & 192) != 128 || (SECOND_operand & 192) != 128) kvar_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | SECOND_operand & 63;
                if (VALUE < 2048) kvar_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) kvar_VALUE("invalid modified UTF-8");
            힙[Reference + 2 + 길이++] = VALUE;
        }
        힙[Reference + 1] = 길이; niz_Reference[INDEX] = Reference; return Reference;
    }
    static int domaćin_znak(String VALUE) {
        int Reference = dodijeli_Pohrana(1, VALUE.length()); if (GREŠKA) return 0;
        for (int 수 = 0; 수 < VALUE.length(); 수++) 힙[Reference + 2 + 수] = VALUE.charAt(수);
        return Reference;
    }
    static void zapisivanje_SMS(int Reference) {
        if (Reference == 0) { korisnik.Zapisuj("null"); return; }
        if (!objekt_VALUE(Reference, 1)) return;
        for (int 수 = 0; 수 < 힙[Reference + 1]; 수++) korisnik.zapisivanje_znak_VALUE(힙[Reference + 2 + 수]);
    }
    static int znamenka_znak(int VALUE) {
        int Reference = dodijeli_Pohrana(1, 11); if (GREŠKA) return 0;
        int 길이 = 0;
        if (VALUE < 0) 힙[Reference + 2 + 길이++] = '-'; else VALUE = -VALUE;
        int indeks_položaja = 1000000000; boolean Pokreni = false;
        while (indeks_položaja != 0) {
            int 수 = -(VALUE / indeks_položaja);
            if (수 != 0 || Pokreni || indeks_položaja == 1) { 힙[Reference + 2 + 길이++] = '0' + 수; Pokreni = true; }
            VALUE %= indeks_položaja; indeks_položaja /= 10;
        }
        힙[Reference + 1] = 길이; return Reference;
    }
    static int 정수해독(int Reference) {
        if (!objekt_VALUE(Reference, 1)) return 0;
        int 길이 = 힙[Reference + 1], 수 = 0, VALUE = 0; boolean 음수 = false;
        if (길이 > 0 && (힙[Reference + 2] == '-' || 힙[Reference + 2] == '+')) { 음수 = 힙[Reference + 2] == '-'; 수++; }
        if (수 == 길이) kvar_VALUE("NumberFormatException");
        for (; 수 < 길이 && !GREŠKA; 수++) {
            int znamenka_VALUE = 힙[Reference + 2 + 수] - '0';
            if (znamenka_VALUE < 0 || znamenka_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && znamenka_VALUE > (음수 ? 8 : 7)) kvar_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - znamenka_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int TYPE_VALUE) {
        if (GREŠKA) return;
        if (kadar_INDEX < 0 || kadar_hrpa[kadar_INDEX] >= postupak_hrpa[kadar_postupak[kadar_INDEX]]) { kvar_VALUE("operand stack overflow"); return; }
        int 칸 = kadar_INDEX * 128 + kadar_hrpa[kadar_INDEX]++; operand_hrpa_VALUE[칸] = VALUE; operand_hrpa_TYPE[칸] = TYPE_VALUE;
    }
    static int 빼기(int TYPE_VALUE) {
        if (GREŠKA) return 0;
        if (kadar_INDEX < 0 || kadar_hrpa[kadar_INDEX] < 1) { kvar_VALUE("operand stack underflow"); return 0; }
        int 칸 = kadar_INDEX * 128 + --kadar_hrpa[kadar_INDEX]; vratiti_TYPE = operand_hrpa_TYPE[칸];
        if (TYPE_VALUE != 0 && vratiti_TYPE != TYPE_VALUE) kvar_VALUE("operand type mismatch");
        return operand_hrpa_VALUE[칸];
    }
    static void 지역읽기(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[kadar_postupak[kadar_INDEX]] || INDEX < 0 || lokalno_TYPE[kadar_INDEX * 128 + INDEX] != TYPE_VALUE) { kvar_VALUE("invalid or uninitialized local"); return; }
        넣기(lokalno_VALUE[kadar_INDEX * 128 + INDEX], TYPE_VALUE);
    }
    static void zapisivanje_lokalno(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[kadar_postupak[kadar_INDEX]] || INDEX < 0) { kvar_VALUE("local index out of range"); return; }
        int VALUE = 빼기(TYPE_VALUE); lokalno_VALUE[kadar_INDEX * 128 + INDEX] = VALUE; lokalno_TYPE[kadar_INDEX * 128 + INDEX] = TYPE_VALUE;
    }
    static int 명바() {
        int Položaj = kadar_položaj[kadar_INDEX];
        if (Položaj < postupak_START[kadar_postupak[kadar_INDEX]] || Položaj >= postupak_završiti_razgovor[kadar_postupak[kadar_INDEX]]) { kvar_VALUE("instruction pointer out of range"); return 0; }
        kadar_položaj[kadar_INDEX]++; return Datoteka[Položaj];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void pomicati_se_VALUE(int Položaj) {
        int FUNCTION_VALUE = kadar_postupak[kadar_INDEX];
        if (Položaj < postupak_START[FUNCTION_VALUE] || Položaj >= postupak_završiti_razgovor[FUNCTION_VALUE] || 경계[Položaj] != FUNCTION_VALUE + 1) kvar_VALUE("invalid branch target");
        else kadar_položaj[kadar_INDEX] = Položaj;
    }
    static void 호출(int FUNCTION_VALUE) {
        if (kadar_INDEX == 31) { kvar_VALUE("call stack limit (32)"); return; }
        int Dalje_artikl = kadar_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) lokalno_TYPE[Dalje_artikl * 128 + 수] = 0;
        for (int 수 = postupak_argument_COUNT[FUNCTION_VALUE] - 1; 수 >= 0; 수--) {
            lokalno_VALUE[Dalje_artikl * 128 + 수] = 빼기(postupak_argument_TYPE[FUNCTION_VALUE * 16 + 수]); lokalno_TYPE[Dalje_artikl * 128 + 수] = postupak_argument_TYPE[FUNCTION_VALUE * 16 + 수];
        }
        kadar_INDEX = Dalje_artikl; kadar_postupak[kadar_INDEX] = FUNCTION_VALUE; kadar_položaj[kadar_INDEX] = postupak_START[FUNCTION_VALUE]; kadar_hrpa[kadar_INDEX] = 0;
    }
    static void vratiti_KR(int TYPE_VALUE) {
        if (TYPE_VALUE != postupak_vratiti[kadar_postupak[kadar_INDEX]]) { kvar_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        kadar_INDEX--; if (kadar_INDEX >= 0 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
    }
    static int[] tok_naziv_datoteke = new int[64];
    static void Datoteka_tok_CALL(int vlasnik_VALUE, int Ime, int oblik_VALUE, int Naredba) {
        boolean Izlaz = Word_SMS(vlasnik_VALUE, "java/io/FileOutputStream");
        int 종류 = Izlaz ? 6 : 5;
        if (Naredba == 183 && Word_SMS(Ime, "<init>")) {
            boolean 이어 = false;
            if (Izlaz && Word_SMS(oblik_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(oblik_VALUE, "(Ljava/lang/String;)V")) { kvar_VALUE("unsupported file stream constructor"); return; }
            int Datoteka_unos_naziv = 빼기(2), tok_VALUE = 빼기(2);
            if (!objekt_VALUE(Datoteka_unos_naziv, 1) || !objekt_VALUE(tok_VALUE, 종류) || GREŠKA) return;
            if (힙[tok_VALUE + 3] != 0) { kvar_VALUE("file stream already initialized"); return; }
            int 길이 = 힙[Datoteka_unos_naziv + 1];
            if (길이 < 1 || 길이 > 63) { kvar_VALUE("invalid file name length"); return; }
            for (int 칸 = 0; 칸 < 길이; 칸++) {
                int VALUE = 힙[Datoteka_unos_naziv + 2 + 칸];
                if (VALUE < 1 || VALUE > 127) { kvar_VALUE("file stream paths currently require ASCII"); return; }
                tok_naziv_datoteke[칸] = VALUE;
            }
            tok_naziv_datoteke[길이] = 0;
            int 서술자 = korisnik.파일서술자열기(tok_naziv_datoteke, Izlaz ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { kvar_VALUE("FileNotFoundException: file open failed"); return; }
            힙[tok_VALUE + 2] = 서술자; 힙[tok_VALUE + 3] = 1;
            return;
        }
        if (Naredba != 182) { kvar_VALUE("invalid file stream invocation"); return; }
        int Aktivnost = -1, VALUE = 0;
        if (Word_SMS(Ime, "close") && Word_SMS(oblik_VALUE, "()V")) Aktivnost = 0;
        if (!Izlaz && Word_SMS(Ime, "read") && Word_SMS(oblik_VALUE, "()I")) Aktivnost = 1;
        if (Izlaz && Word_SMS(Ime, "write") && Word_SMS(oblik_VALUE, "(I)V")) { Aktivnost = 2; VALUE = 빼기(1); }
        if (Aktivnost < 0) { kvar_VALUE("unsupported file stream method"); return; }
        int tok_VALUE = 빼기(2);
        if (!objekt_VALUE(tok_VALUE, 종류) || GREŠKA) return;
        if (힙[tok_VALUE + 3] == 0) { kvar_VALUE("uninitialized file stream"); return; }
        int 서술자 = 힙[tok_VALUE + 2];
        if (Aktivnost == 0) {
            if (서술자 >= 0 && korisnik.파일서술자닫기(서술자) < 0) kvar_VALUE("IOException: close failed");
            힙[tok_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { kvar_VALUE("IOException: stream closed"); return; }
        if (Aktivnost == 1) {
            int REZULTAT = korisnik.파일한바이트읽기(서술자);
            if (REZULTAT < -1) kvar_VALUE("IOException: read failed"); else 넣기(REZULTAT, 1);
        } else if (korisnik.파일한바이트쓰기(서술자, VALUE) != 1) kvar_VALUE("IOException: write failed");
    }
    static void CALL_postupak(int INDEX, int Naredba) {
        if (!상검사(INDEX, 10)) return;
        int vlasnik_VALUE = naziv_klase_SMS(상가[INDEX]), Ime = Reference_naziv(konstanta_SECOND_VALUE[INDEX]), oblik_VALUE = Reference_TYPE(konstanta_SECOND_VALUE[INDEX]);
        if (GREŠKA) return;
        if (같은말(vlasnik_VALUE, naziv_klase)) {
            if (Naredba != 184) { kvar_VALUE("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < postupak_COUNT; 수++) if (같은말(Ime, postupak_naziv_SMS[수]) && 같은말(oblik_VALUE, postupak_TYPE[수])) {
                if ((postupak_pristup[수] & 8) == 0) kvar_VALUE("method is not static"); else 호출(수);
                return;
            }
            kvar_VALUE("NoSuchMethodError"); return;
        }
        if (Word_SMS(vlasnik_VALUE, "java/io/FileInputStream") || Word_SMS(vlasnik_VALUE, "java/io/FileOutputStream")) {
            Datoteka_tok_CALL(vlasnik_VALUE, Ime, oblik_VALUE, Naredba); return;
        }
        if (Naredba == 184 && Word_SMS(vlasnik_VALUE, "java/lang/Integer") && Word_SMS(Ime, "parseInt") && Word_SMS(oblik_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Naredba == 182 && Word_SMS(vlasnik_VALUE, "java/io/PrintStream") && (Word_SMS(Ime, "println") || Word_SMS(Ime, "print"))) {
            int TYPE_VALUE = 0, VALUE = 0;
            if (Word_SMS(oblik_VALUE, "(I)V")) { TYPE_VALUE = 1; VALUE = 빼기(1); }
            else if (Word_SMS(oblik_VALUE, "(Z)V")) { TYPE_VALUE = 2; VALUE = 빼기(1); }
            else if (Word_SMS(oblik_VALUE, "(C)V")) { TYPE_VALUE = 3; VALUE = 빼기(1); }
            else if (Word_SMS(oblik_VALUE, "(Ljava/lang/String;)V")) { TYPE_VALUE = 4; VALUE = 빼기(2); }
            else if (!Word_SMS(oblik_VALUE, "()V") || !Word_SMS(Ime, "println")) kvar_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) kvar_VALUE("invalid PrintStream receiver");
            if (GREŠKA) return;
            if (TYPE_VALUE == 1) 자바도구.수쓰기(VALUE);
            if (TYPE_VALUE == 2) korisnik.Zapisuj(VALUE == 0 ? "false" : "true");
            if (TYPE_VALUE == 3) korisnik.zapisivanje_znak_VALUE(VALUE & 65535);
            if (TYPE_VALUE == 4) zapisivanje_SMS(VALUE);
            if (Word_SMS(Ime, "println")) korisnik.zapisivanje_znak_VALUE(10);
            return;
        }
        if (Naredba == 182 && Word_SMS(vlasnik_VALUE, "java/lang/String")) {
            if (Word_SMS(Ime, "length") && Word_SMS(oblik_VALUE, "()I")) {
                int Reference = 빼기(2); if (objekt_VALUE(Reference, 1)) 넣기(힙[Reference + 1], 1); return;
            }
            if (Word_SMS(Ime, "charAt") && Word_SMS(oblik_VALUE, "(I)C")) {
                int indeks_VALUE = 빼기(1), Reference = 빼기(2);
                if (objekt_VALUE(Reference, 1)) {
                    if (indeks_VALUE < 0 || indeks_VALUE >= 힙[Reference + 1]) kvar_VALUE("StringIndexOutOfBoundsException"); else 넣기(힙[Reference + 2 + indeks_VALUE], 1);
                }
                return;
            }
        }
        if (Word_SMS(vlasnik_VALUE, "java/lang/StringBuilder")) {
            if (Naredba == 183 && Word_SMS(Ime, "<init>") && Word_SMS(oblik_VALUE, "()V")) { objekt_VALUE(빼기(2), 4); return; }
            if (Naredba == 182 && Word_SMS(Ime, "toString") && Word_SMS(oblik_VALUE, "()Ljava/lang/String;")) {
                int Reference = 빼기(2); if (objekt_VALUE(Reference, 4)) 넣기(힙[Reference + 2] == 0 ? domaćin_znak("") : 힙[Reference + 2], 2); return;
            }
            if (Naredba == 182 && Word_SMS(Ime, "append")) {
                int Tekst = 0;
                if (Word_SMS(oblik_VALUE, "(I)Ljava/lang/StringBuilder;")) Tekst = znamenka_znak(빼기(1));
                else if (Word_SMS(oblik_VALUE, "(Z)Ljava/lang/StringBuilder;")) Tekst = domaćin_znak(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(oblik_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); Tekst = dodijeli_Pohrana(1, 1); if (!GREŠKA) 힙[Tekst + 2] = VALUE & 65535;
                }
                else if (Word_SMS(oblik_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Tekst = 빼기(2); if (Tekst == 0) Tekst = domaćin_znak("null"); }
                else { kvar_VALUE("unsupported StringBuilder append"); return; }
                int Reference = 빼기(2); if (!objekt_VALUE(Reference, 4) || !objekt_VALUE(Tekst, 1)) return;
                int prednja_VALUE = 힙[Reference + 2], 앞길이 = prednja_VALUE == 0 ? 0 : 힙[prednja_VALUE + 1], 뒤길이 = 힙[Tekst + 1];
                int 새글 = dodijeli_Pohrana(1, 앞길이 + 뒤길이); if (GREŠKA) return;
                for (int 수 = 0; 수 < 앞길이; 수++) 힙[새글 + 2 + 수] = 힙[prednja_VALUE + 2 + 수];
                for (int 수 = 0; 수 < 뒤길이; 수++) 힙[새글 + 2 + 앞길이 + 수] = 힙[Tekst + 2 + 수];
                힙[Reference + 2] = 새글; 넣기(Reference, 2); return;
            }
        }
        kvar_VALUE("unsupported library method");
    }
    static int 배열칸(int Reference, int indeks_VALUE, int TYPE_VALUE) {
        if (!objekt_VALUE(Reference, TYPE_VALUE)) return 0;
        if (indeks_VALUE < 0 || indeks_VALUE >= 힙[Reference + 1]) { kvar_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return Reference + 2 + indeks_VALUE;
    }
    static void Izvrši_naredba() {
        int 남음 = 500000;
        while (kadar_INDEX >= 0 && !GREŠKA) {
            if (--남음 == 0) { kvar_VALUE("instruction limit (500000)"); break; }
            int Pokreni = kadar_položaj[kadar_INDEX], VALUE = 명바();
            if (GREŠKA) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = VALUE == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= konstanta_COUNT) kvar_VALUE("invalid ldc constant");
                else if (konstanta_oznaka[수] == 3) 넣기(상가[수], 1);
                else if (konstanta_oznaka[수] == 8) 넣기(konstanta_SMS(상가[수]), 2);
                else kvar_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { zapisivanje_lokalno(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { zapisivanje_lokalno(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { zapisivanje_lokalno(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE == 50) {
                int indeks_VALUE = 빼기(1), Reference = 빼기(2), 칸 = 배열칸(Reference, indeks_VALUE, VALUE == 46 ? 2 : 3);
                if (!GREŠKA) 넣기(힙[칸], VALUE == 46 ? 1 : 2); continue;
            }
            if (VALUE == 79 || VALUE == 83) {
                int artikl_element = 빼기(VALUE == 79 ? 1 : 2), indeks_VALUE = 빼기(1), Reference = 빼기(2), 칸 = 배열칸(Reference, indeks_VALUE, VALUE == 79 ? 2 : 3);
                if (VALUE == 83 && artikl_element != 0) objekt_VALUE(artikl_element, 1);
                if (!GREŠKA) 힙[칸] = artikl_element; continue;
            }
            if (VALUE == 87) { 빼기(0); continue; }
            if (VALUE == 89) { int 가 = 빼기(0), TYPE_VALUE = vratiti_TYPE; 넣기(가, TYPE_VALUE); 넣기(가, TYPE_VALUE); continue; }
            if (VALUE == 95) { int 가 = 빼기(0), 가형 = vratiti_TYPE, SECOND_operand = 빼기(0), SECOND_operand_TYPE = vratiti_TYPE; 넣기(가, 가형); 넣기(SECOND_operand, SECOND_operand_TYPE); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int SECOND_operand = 빼기(1), 가 = 빼기(1), REZULTAT = 0;
                if ((VALUE == 108 || VALUE == 112) && SECOND_operand == 0) { kvar_VALUE("ArithmeticException: / by zero"); continue; }
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
                int lokalno_doseg = 명바(), inkrement_korak = (byte)명바(); 지역읽기(lokalno_doseg, 1); 넣기(빼기(1) + inkrement_korak, 1); zapisivanje_lokalno(lokalno_doseg, 1); continue;
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
                if (갈까) pomicati_se_VALUE(odredište_VALUE); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { vratiti_KR(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE == 178) {
                int 수 = 명짧(); if (!상검사(수, 9)) continue;
                if (!Word_SMS(naziv_klase_SMS(상가[수]), "java/lang/System") || !Word_SMS(Reference_naziv(konstanta_SECOND_VALUE[수]), "out")
                    || !Word_SMS(Reference_TYPE(konstanta_SECOND_VALUE[수]), "Ljava/io/PrintStream;")) kvar_VALUE("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (VALUE == 182 || VALUE == 183 || VALUE == 184) { CALL_postupak(명짧(), VALUE); continue; }
            if (VALUE == 187) {
                int Ime = naziv_klase_SMS(명짧());
                if (Word_SMS(Ime, "java/lang/StringBuilder")) 넣기(dodijeli_Pohrana(4, 1), 2);
                else if (Word_SMS(Ime, "java/io/FileInputStream") || Word_SMS(Ime, "java/io/FileOutputStream")) {
                    int Reference = dodijeli_Pohrana(Word_SMS(Ime, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!GREŠKA) { 힙[Reference + 2] = -1; 넣기(Reference, 2); }
                } else kvar_VALUE("unsupported object construction");
                continue;
            }
            if (VALUE == 188 || VALUE == 189) {
                if (VALUE == 188) { if (명바() != 10) kvar_VALUE("only int[] newarray is supported"); }
                else if (!Word_SMS(naziv_klase_SMS(명짧()), "java/lang/String")) kvar_VALUE("only String[] anewarray is supported");
                int 길이 = 빼기(1); 넣기(dodijeli_Pohrana(VALUE == 188 ? 2 : 3, 길이), 2); continue;
            }
            if (VALUE == 190) {
                int Reference = 빼기(2);
                if (Reference < 1 || Reference >= 힙끝 - 1 || (힙[Reference] != 2 && 힙[Reference] != 3)) kvar_VALUE("null or invalid array");
                else 넣기(힙[Reference + 1], 1); continue;
            }
            if (VALUE == 192) {
                int Ime = naziv_klase_SMS(명짧()), Reference = 빼기(2);
                if (!Word_SMS(Ime, "java/lang/String")) kvar_VALUE("unsupported checkcast");
                else if (Reference != 0) objekt_VALUE(Reference, 1);
                넣기(Reference, 2); continue;
            }
            kvar_VALUE("unsupported bytecode");
        }
    }
    public static int Pokreni() {
        if (korisnik.인수개수() == 1 && 자바도구.같음(korisnik.Argumenti(0), "-version")) {
            korisnik.Zapisuj("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (korisnik.인수개수() < 1) { korisnik.Zapisuj("Usage: java CLASS [ARGS]\n"); return 2; }
        int 길이 = 자바도구.Ime(naziv_datoteke_SMS, korisnik.Argumenti(0));
        if (길이 < 1 || 길이 > 57) { korisnik.Zapisuj("java: invalid class name\n"); return 2; }
        naziv_datoteke_SMS[길이] = '.'; naziv_datoteke_SMS[길이 + 1] = 'c'; naziv_datoteke_SMS[길이 + 2] = 'l'; naziv_datoteke_SMS[길이 + 3] = 'a'; naziv_datoteke_SMS[길이 + 4] = 's'; naziv_datoteke_SMS[길이 + 5] = 's';
        Veličina = korisnik.파일읽기(naziv_datoteke_SMS, Datoteka);
        if (Veličina < 0) { korisnik.Zapisuj("java: cannot read class: "); 자바도구.수쓰기(Veličina); korisnik.zapisivanje_znak_VALUE(10); return 1; }
        클래스읽기(); if (GREŠKA) return 1;
        int znak_naziv = konstanta_SMS(naziv_klase);
        if (!GREŠKA && 힙[znak_naziv + 1] != 길이) kvar_VALUE("class name does not match file");
        for (int 수 = 0; 수 < 길이 && !GREŠKA; 수++) if (힙[znak_naziv + 2 + 수] != naziv_datoteke_SMS[수]) kvar_VALUE("class name does not match file");
        int unos_p_VALUE = -1;
        for (int 수 = 0; 수 < postupak_COUNT; 수++) if (Word_SMS(postupak_naziv_SMS[수], "main") && Word_SMS(postupak_TYPE[수], "([Ljava/lang/String;)V") && (postupak_pristup[수] & 9) == 9) unos_p_VALUE = 수;
        if (unos_p_VALUE < 0) kvar_VALUE("public static void main(String[] args) required");
        if (GREŠKA) return 1;
        int Argumenti = dodijeli_Pohrana(3, korisnik.인수개수() - 1);
        for (int 수 = 1; 수 < korisnik.인수개수() && !GREŠKA; 수++) 힙[Argumenti + 1 + 수] = domaćin_znak(korisnik.Argumenti(수));
        kadar_INDEX = 0; kadar_postupak[0] = unos_p_VALUE; kadar_položaj[0] = postupak_START[unos_p_VALUE]; lokalno_VALUE[0] = Argumenti; lokalno_TYPE[0] = 2;
        Izvrši_naredba(); return GREŠKA ? 1 : 0;
    }
}
