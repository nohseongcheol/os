// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Datoteka/operand_stek/referenca/grana 경계를 Izvrši_komanda 중 검사한다. */
public final class 자바가상기계 {
    static int[] Datoteka = new int[16384], ime_datoteke_SMS = new int[64];
    static int[] konstanta_oznaka = new int[512], 상가 = new int[512], konstanta_SECOND_VALUE = new int[512], niska_referenca = new int[512];
    static int[] metod_ime_SMS = new int[32], metod_tip = new int[32], metod_pristup = new int[32];
    static int[] metod_START = new int[32], metod_završiti_razgovor = new int[32], metod_stek = new int[32], 함수지역 = new int[32];
    static int[] metod_argument_COUNT = new int[32], metod_argument_tip = new int[512], metod_vratiti = new int[32];
    static int[] 경계 = new int[16384];
    static int[] lokalni_VALUE = new int[4096], lokalni_tip = new int[4096], operand_stek_VALUE = new int[4096], operand_stek_tip = new int[4096];
    static int[] kadar_metod = new int[32], kadar_pozicija = new int[32], kadar_stek = new int[32];
    static int[] 힙 = new int[8192];
    static int promeniti_veličinu, 읽기위치, konstanta_COUNT, metod_COUNT, ime_klase, kadar_INDEX = -1, 힙끝 = 1, vratiti_tip;
    static boolean greška;

    static void otkazivanje_VALUE(String Word_SMS) {
        if (!greška) { korisnik.쓰기("JVM error: "); korisnik.쓰기(Word_SMS); korisnik.문자쓰기(10); }
        greška = true;
    }
    static boolean klip(int koristiti, int 길이) { return koristiti >= 0 && 길이 >= 0 && koristiti <= promeniti_veličinu - 길이; }
    static int bajt_VALUE() {
        if (!klip(읽기위치, 1)) { otkazivanje_VALUE("truncated class file"); return 0; }
        return Datoteka[읽기위치++];
    }
    static int 짧은수() { return bajt_VALUE() << 8 | bajt_VALUE(); }
    static int ceo_broj() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int 길이) { if (!klip(읽기위치, 길이)) otkazivanje_VALUE("invalid attribute size"); else 읽기위치 += 길이; }
    static boolean proveriti_konstanta(int 수, int 종류) {
        if (수 <= 0 || 수 >= konstanta_COUNT || konstanta_oznaka[수] != 종류) { otkazivanje_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_opseg(int koristiti, int 길이, String Word_SMS) {
        if (!klip(koristiti, 길이) || 길이 != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < 길이; 수++) if (Datoteka[koristiti + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static boolean Word_SMS(int konstanta_VALUE, String Word_SMS) { return proveriti_konstanta(konstanta_VALUE, 1) && SMS_opseg(상가[konstanta_VALUE], konstanta_SECOND_VALUE[konstanta_VALUE], Word_SMS); }
    static boolean 같은말(int 가, int SECOND_operand) {
        if (!proveriti_konstanta(가, 1) || !proveriti_konstanta(SECOND_operand, 1) || konstanta_SECOND_VALUE[가] != konstanta_SECOND_VALUE[SECOND_operand]) return false;
        for (int 수 = 0; 수 < konstanta_SECOND_VALUE[가]; 수++) if (Datoteka[상가[가] + 수] != Datoteka[상가[SECOND_operand] + 수]) return false;
        return true;
    }
    static int ime_klase_SMS(int 수) { return proveriti_konstanta(수, 7) && proveriti_konstanta(상가[수], 1) ? 상가[수] : 0; }
    static int referenca_ime(int 수) { return proveriti_konstanta(수, 12) && proveriti_konstanta(상가[수], 1) ? 상가[수] : 0; }
    static int referenca_tip(int 수) { return proveriti_konstanta(수, 12) && proveriti_konstanta(konstanta_SECOND_VALUE[수], 1) ? konstanta_SECOND_VALUE[수] : 0; }
    static int 서술형(int 끝, boolean 빈형) {
        if (읽기위치 >= 끝) { otkazivanje_VALUE("invalid descriptor"); return 0; }
        int VALUE = bajt_VALUE();
        if (VALUE == 'V' && 빈형) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int koristiti = 읽기위치;
            while (읽기위치 < 끝 && Datoteka[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == koristiti) otkazivanje_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        otkazivanje_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int FUNCTION_VALUE) {
        int 이전 = 읽기위치, 수 = metod_tip[FUNCTION_VALUE];
        if (!proveriti_konstanta(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + konstanta_SECOND_VALUE[수];
        if (bajt_VALUE() != '(') otkazivanje_VALUE("invalid method descriptor");
        int stavka_COUNT = 0;
        while (!greška && 읽기위치 < 끝 && Datoteka[읽기위치] != ')') {
            if (stavka_COUNT == 16) { otkazivanje_VALUE("too many method arguments"); break; }
            metod_argument_tip[FUNCTION_VALUE * 16 + stavka_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || bajt_VALUE() != ')') otkazivanje_VALUE("invalid method descriptor");
        metod_vratiti[FUNCTION_VALUE] = 서술형(끝, true); metod_argument_COUNT[FUNCTION_VALUE] = stavka_COUNT;
        if (읽기위치 != 끝) otkazivanje_VALUE("invalid method descriptor");
        읽기위치 = 이전;
    }
    static void 속성건너() {
        int stavka_COUNT = 짧은수();
        for (int 수 = 0; 수 < stavka_COUNT && !greška; 수++) { proveriti_konstanta(짧은수(), 1); 건너(ceo_broj()); }
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
        if (ceo_broj() != 0xcafebabe) otkazivanje_VALUE("not a class file");
        int 부판 = 짧은수(), verzija_VALUE = 짧은수();
        if (verzija_VALUE < 45 || verzija_VALUE > 52 || 부판 != 0) otkazivanje_VALUE("supported class versions: 45..52, minor 0");
        konstanta_COUNT = 짧은수();
        if (konstanta_COUNT < 1 || konstanta_COUNT > 512) { otkazivanje_VALUE("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < konstanta_COUNT && !greška; 수++) {
            int 종류 = bajt_VALUE(); konstanta_oznaka[수] = 종류;
            if (종류 == 1) { konstanta_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(konstanta_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = ceo_broj();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); konstanta_SECOND_VALUE[수] = 짧은수(); }
            else otkazivanje_VALUE("unsupported constant type");
        }
        int dozvola_VALUE = 짧은수();
        if ((dozvola_VALUE & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) otkazivanje_VALUE("unsupported class flags");
        ime_klase = ime_klase_SMS(짧은수());
        if (!Word_SMS(ime_klase_SMS(짧은수()), "java/lang/Object")) otkazivanje_VALUE("inheritance unsupported");
        if (짧은수() != 0) otkazivanje_VALUE("interfaces unsupported");
        if (짧은수() != 0) otkazivanje_VALUE("fields unsupported");
        metod_COUNT = 짧은수();
        if (metod_COUNT < 1 || metod_COUNT > 32) { otkazivanje_VALUE("method count limit (32)"); return; }
        for (int 수 = 0; 수 < metod_COUNT && !greška; 수++) {
            metod_pristup[수] = 짧은수(); metod_ime_SMS[수] = 짧은수(); metod_tip[수] = 짧은수();
            proveriti_konstanta(metod_ime_SMS[수], 1); 서술읽기(수);
            if ((metod_pristup[수] & (0x100 | 0x400 | 0x20)) != 0) otkazivanje_VALUE("native, abstract and synchronized methods unsupported");
            if ((metod_pristup[수] & 8) == 0 && !Word_SMS(metod_ime_SMS[수], "<init>")) otkazivanje_VALUE("instance methods unsupported");
            if (Word_SMS(metod_ime_SMS[수], "<clinit>")) otkazivanje_VALUE("class initializers unsupported");
            for (int čeona_kamera_VALUE = 0; čeona_kamera_VALUE < 수; čeona_kamera_VALUE++) if (같은말(metod_ime_SMS[čeona_kamera_VALUE], metod_ime_SMS[수]) && 같은말(metod_tip[čeona_kamera_VALUE], metod_tip[수])) otkazivanje_VALUE("duplicate method");
            int stavka_COUNT = 짧은수();
            for (int atribut_VALUE = 0; atribut_VALUE < stavka_COUNT && !greška; atribut_VALUE++) {
                int ime = 짧은수(), 길이 = ceo_broj(), koristiti = 읽기위치;
                if (!klip(koristiti, 길이)) { otkazivanje_VALUE("truncated method attribute"); break; }
                if (Word_SMS(ime, "Code")) {
                    if (metod_START[수] != 0) otkazivanje_VALUE("duplicate Code attribute");
                    metod_stek[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = ceo_broj();
                    if (metod_stek[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < metod_argument_COUNT[수]
                        || 코드길이 < 1 || 코드길이 > 8192) otkazivanje_VALUE("method memory limits exceeded");
                    metod_START[수] = 읽기위치; 건너(코드길이); metod_završiti_razgovor[수] = 읽기위치;
                    if (짧은수() != 0) otkazivanje_VALUE("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != koristiti + 길이) otkazivanje_VALUE("Code attribute size mismatch");
                } else 건너(길이);
            }
            if (metod_START[수] == 0) otkazivanje_VALUE("missing Code attribute");
            int 칸 = metod_START[수];
            while (칸 < metod_završiti_razgovor[수] && !greška) {
                int 길이 = 명령길이(Datoteka[칸]);
                if (길이 == 0 || 길이 > metod_završiti_razgovor[수] - 칸) { otkazivanje_VALUE("unsupported or truncated bytecode"); break; }
                경계[칸] = 수 + 1; 칸 += 길이;
            }
            // 실행하지 않는 경로에도 잘못된 grana 목적지를 허용하지 않는다.
            칸 = metod_START[수];
            while (칸 < metod_završiti_razgovor[수] && !greška) {
                int VALUE = Datoteka[칸];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                    int odredište_VALUE = 칸 + (short)(Datoteka[칸 + 1] << 8 | Datoteka[칸 + 2]);
                    if (odredište_VALUE < metod_START[수] || odredište_VALUE >= metod_završiti_razgovor[수] || 경계[odredište_VALUE] != 수 + 1) otkazivanje_VALUE("invalid branch target");
                }
                칸 += 명령길이(VALUE);
            }
        }
        if (!greška) 속성건너();
        if (읽기위치 != promeniti_veličinu) otkazivanje_VALUE("extra class file data");
    }
    static int dodeliti_Skladište(int 종류, int 길이) {
        if (길이 < 0 || 길이 > 힙.length - 힙끝 - 2) { otkazivanje_VALUE("object heap exhausted or negative array size"); return 0; }
        int referenca = 힙끝; 힙끝 += 길이 + 2; 힙[referenca] = 종류; 힙[referenca + 1] = 길이;
        return referenca;
    }
    static boolean objekat_VALUE(int referenca, int 종류) {
        if (referenca < 1 || referenca >= 힙끝 - 1 || 힙[referenca] != 종류) { otkazivanje_VALUE("null or invalid object reference"); return false; }
        return true;
    }
    static int konstanta_SMS(int INDEX) {
        if (!proveriti_konstanta(INDEX, 1)) return 0;
        if (niska_referenca[INDEX] != 0) return niska_referenca[INDEX];
        int referenca = dodeliti_Skladište(1, konstanta_SECOND_VALUE[INDEX]); if (greška) return 0;
        int 끝 = 상가[INDEX] + konstanta_SECOND_VALUE[INDEX], 수 = 상가[INDEX], 길이 = 0;
        while (수 < 끝 && !greška) {
            int VALUE = Datoteka[수++];
            if (VALUE == 0) otkazivanje_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && 수 < 끝) {
                int Dalje_stavka = Datoteka[수++];
                if ((Dalje_stavka & 192) != 128) otkazivanje_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | Dalje_stavka & 63;
                if (VALUE != 0 && VALUE < 128) otkazivanje_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && 수 + 1 < 끝) {
                int 가 = Datoteka[수++], SECOND_operand = Datoteka[수++];
                if ((가 & 192) != 128 || (SECOND_operand & 192) != 128) otkazivanje_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | SECOND_operand & 63;
                if (VALUE < 2048) otkazivanje_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) otkazivanje_VALUE("invalid modified UTF-8");
            힙[referenca + 2 + 길이++] = VALUE;
        }
        힙[referenca + 1] = 길이; niska_referenca[INDEX] = referenca; return referenca;
    }
    static int host_znak(String VALUE) {
        int referenca = dodeliti_Skladište(1, VALUE.length()); if (greška) return 0;
        for (int 수 = 0; 수 < VALUE.length(); 수++) 힙[referenca + 2 + 수] = VALUE.charAt(수);
        return referenca;
    }
    static void 글쓰기(int referenca) {
        if (referenca == 0) { korisnik.쓰기("null"); return; }
        if (!objekat_VALUE(referenca, 1)) return;
        for (int 수 = 0; 수 < 힙[referenca + 1]; 수++) korisnik.문자쓰기(힙[referenca + 2 + 수]);
    }
    static int cifra_znak(int VALUE) {
        int referenca = dodeliti_Skladište(1, 11); if (greška) return 0;
        int 길이 = 0;
        if (VALUE < 0) 힙[referenca + 2 + 길이++] = '-'; else VALUE = -VALUE;
        int indeks_pozicije = 1000000000; boolean koristiti = false;
        while (indeks_pozicije != 0) {
            int 수 = -(VALUE / indeks_pozicije);
            if (수 != 0 || koristiti || indeks_pozicije == 1) { 힙[referenca + 2 + 길이++] = '0' + 수; koristiti = true; }
            VALUE %= indeks_pozicije; indeks_pozicije /= 10;
        }
        힙[referenca + 1] = 길이; return referenca;
    }
    static int 정수해독(int referenca) {
        if (!objekat_VALUE(referenca, 1)) return 0;
        int 길이 = 힙[referenca + 1], 수 = 0, VALUE = 0; boolean 음수 = false;
        if (길이 > 0 && (힙[referenca + 2] == '-' || 힙[referenca + 2] == '+')) { 음수 = 힙[referenca + 2] == '-'; 수++; }
        if (수 == 길이) otkazivanje_VALUE("NumberFormatException");
        for (; 수 < 길이 && !greška; 수++) {
            int cifra_VALUE = 힙[referenca + 2 + 수] - '0';
            if (cifra_VALUE < 0 || cifra_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && cifra_VALUE > (음수 ? 8 : 7)) otkazivanje_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - cifra_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int tip_VALUE) {
        if (greška) return;
        if (kadar_INDEX < 0 || kadar_stek[kadar_INDEX] >= metod_stek[kadar_metod[kadar_INDEX]]) { otkazivanje_VALUE("operand stack overflow"); return; }
        int 칸 = kadar_INDEX * 128 + kadar_stek[kadar_INDEX]++; operand_stek_VALUE[칸] = VALUE; operand_stek_tip[칸] = tip_VALUE;
    }
    static int 빼기(int tip_VALUE) {
        if (greška) return 0;
        if (kadar_INDEX < 0 || kadar_stek[kadar_INDEX] < 1) { otkazivanje_VALUE("operand stack underflow"); return 0; }
        int 칸 = kadar_INDEX * 128 + --kadar_stek[kadar_INDEX]; vratiti_tip = operand_stek_tip[칸];
        if (tip_VALUE != 0 && vratiti_tip != tip_VALUE) otkazivanje_VALUE("operand type mismatch");
        return operand_stek_VALUE[칸];
    }
    static void 지역읽기(int INDEX, int tip_VALUE) {
        if (INDEX >= 함수지역[kadar_metod[kadar_INDEX]] || INDEX < 0 || lokalni_tip[kadar_INDEX * 128 + INDEX] != tip_VALUE) { otkazivanje_VALUE("invalid or uninitialized local"); return; }
        넣기(lokalni_VALUE[kadar_INDEX * 128 + INDEX], tip_VALUE);
    }
    static void 지역쓰기(int INDEX, int tip_VALUE) {
        if (INDEX >= 함수지역[kadar_metod[kadar_INDEX]] || INDEX < 0) { otkazivanje_VALUE("local index out of range"); return; }
        int VALUE = 빼기(tip_VALUE); lokalni_VALUE[kadar_INDEX * 128 + INDEX] = VALUE; lokalni_tip[kadar_INDEX * 128 + INDEX] = tip_VALUE;
    }
    static int 명바() {
        int pozicija = kadar_pozicija[kadar_INDEX];
        if (pozicija < metod_START[kadar_metod[kadar_INDEX]] || pozicija >= metod_završiti_razgovor[kadar_metod[kadar_INDEX]]) { otkazivanje_VALUE("instruction pointer out of range"); return 0; }
        kadar_pozicija[kadar_INDEX]++; return Datoteka[pozicija];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void premestiti_VALUE(int pozicija) {
        int FUNCTION_VALUE = kadar_metod[kadar_INDEX];
        if (pozicija < metod_START[FUNCTION_VALUE] || pozicija >= metod_završiti_razgovor[FUNCTION_VALUE] || 경계[pozicija] != FUNCTION_VALUE + 1) otkazivanje_VALUE("invalid branch target");
        else kadar_pozicija[kadar_INDEX] = pozicija;
    }
    static void 호출(int FUNCTION_VALUE) {
        if (kadar_INDEX == 31) { otkazivanje_VALUE("call stack limit (32)"); return; }
        int Dalje_stavka = kadar_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) lokalni_tip[Dalje_stavka * 128 + 수] = 0;
        for (int 수 = metod_argument_COUNT[FUNCTION_VALUE] - 1; 수 >= 0; 수--) {
            lokalni_VALUE[Dalje_stavka * 128 + 수] = 빼기(metod_argument_tip[FUNCTION_VALUE * 16 + 수]); lokalni_tip[Dalje_stavka * 128 + 수] = metod_argument_tip[FUNCTION_VALUE * 16 + 수];
        }
        kadar_INDEX = Dalje_stavka; kadar_metod[kadar_INDEX] = FUNCTION_VALUE; kadar_pozicija[kadar_INDEX] = metod_START[FUNCTION_VALUE]; kadar_stek[kadar_INDEX] = 0;
    }
    static void vratiti_KR(int tip_VALUE) {
        if (tip_VALUE != metod_vratiti[kadar_metod[kadar_INDEX]]) { otkazivanje_VALUE("return type mismatch"); return; }
        int VALUE = tip_VALUE == 0 ? 0 : 빼기(tip_VALUE);
        kadar_INDEX--; if (kadar_INDEX >= 0 && tip_VALUE != 0) 넣기(VALUE, tip_VALUE);
    }
    static int[] tok_ime_datoteke = new int[64];
    static void Datoteka_tok_CALL(int vlasnik_VALUE, int ime, int format_VALUE, int komanda) {
        boolean 출력 = Word_SMS(vlasnik_VALUE, "java/io/FileOutputStream");
        int 종류 = 출력 ? 6 : 5;
        if (komanda == 183 && Word_SMS(ime, "<init>")) {
            boolean 이어 = false;
            if (출력 && Word_SMS(format_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(format_VALUE, "(Ljava/lang/String;)V")) { otkazivanje_VALUE("unsupported file stream constructor"); return; }
            int Datoteka_stavka_ime = 빼기(2), tok_VALUE = 빼기(2);
            if (!objekat_VALUE(Datoteka_stavka_ime, 1) || !objekat_VALUE(tok_VALUE, 종류) || greška) return;
            if (힙[tok_VALUE + 3] != 0) { otkazivanje_VALUE("file stream already initialized"); return; }
            int 길이 = 힙[Datoteka_stavka_ime + 1];
            if (길이 < 1 || 길이 > 63) { otkazivanje_VALUE("invalid file name length"); return; }
            for (int 칸 = 0; 칸 < 길이; 칸++) {
                int VALUE = 힙[Datoteka_stavka_ime + 2 + 칸];
                if (VALUE < 1 || VALUE > 127) { otkazivanje_VALUE("file stream paths currently require ASCII"); return; }
                tok_ime_datoteke[칸] = VALUE;
            }
            tok_ime_datoteke[길이] = 0;
            int 서술자 = korisnik.파일서술자열기(tok_ime_datoteke, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { otkazivanje_VALUE("FileNotFoundException: file open failed"); return; }
            힙[tok_VALUE + 2] = 서술자; 힙[tok_VALUE + 3] = 1;
            return;
        }
        if (komanda != 182) { otkazivanje_VALUE("invalid file stream invocation"); return; }
        int radnja = -1, VALUE = 0;
        if (Word_SMS(ime, "close") && Word_SMS(format_VALUE, "()V")) radnja = 0;
        if (!출력 && Word_SMS(ime, "read") && Word_SMS(format_VALUE, "()I")) radnja = 1;
        if (출력 && Word_SMS(ime, "write") && Word_SMS(format_VALUE, "(I)V")) { radnja = 2; VALUE = 빼기(1); }
        if (radnja < 0) { otkazivanje_VALUE("unsupported file stream method"); return; }
        int tok_VALUE = 빼기(2);
        if (!objekat_VALUE(tok_VALUE, 종류) || greška) return;
        if (힙[tok_VALUE + 3] == 0) { otkazivanje_VALUE("uninitialized file stream"); return; }
        int 서술자 = 힙[tok_VALUE + 2];
        if (radnja == 0) {
            if (서술자 >= 0 && korisnik.파일서술자닫기(서술자) < 0) otkazivanje_VALUE("IOException: close failed");
            힙[tok_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { otkazivanje_VALUE("IOException: stream closed"); return; }
        if (radnja == 1) {
            int KR = korisnik.파일한바이트읽기(서술자);
            if (KR < -1) otkazivanje_VALUE("IOException: read failed"); else 넣기(KR, 1);
        } else if (korisnik.파일한바이트쓰기(서술자, VALUE) != 1) otkazivanje_VALUE("IOException: write failed");
    }
    static void CALL_metod(int INDEX, int komanda) {
        if (!proveriti_konstanta(INDEX, 10)) return;
        int vlasnik_VALUE = ime_klase_SMS(상가[INDEX]), ime = referenca_ime(konstanta_SECOND_VALUE[INDEX]), format_VALUE = referenca_tip(konstanta_SECOND_VALUE[INDEX]);
        if (greška) return;
        if (같은말(vlasnik_VALUE, ime_klase)) {
            if (komanda != 184) { otkazivanje_VALUE("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < metod_COUNT; 수++) if (같은말(ime, metod_ime_SMS[수]) && 같은말(format_VALUE, metod_tip[수])) {
                if ((metod_pristup[수] & 8) == 0) otkazivanje_VALUE("method is not static"); else 호출(수);
                return;
            }
            otkazivanje_VALUE("NoSuchMethodError"); return;
        }
        if (Word_SMS(vlasnik_VALUE, "java/io/FileInputStream") || Word_SMS(vlasnik_VALUE, "java/io/FileOutputStream")) {
            Datoteka_tok_CALL(vlasnik_VALUE, ime, format_VALUE, komanda); return;
        }
        if (komanda == 184 && Word_SMS(vlasnik_VALUE, "java/lang/Integer") && Word_SMS(ime, "parseInt") && Word_SMS(format_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (komanda == 182 && Word_SMS(vlasnik_VALUE, "java/io/PrintStream") && (Word_SMS(ime, "println") || Word_SMS(ime, "print"))) {
            int tip_VALUE = 0, VALUE = 0;
            if (Word_SMS(format_VALUE, "(I)V")) { tip_VALUE = 1; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(Z)V")) { tip_VALUE = 2; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(C)V")) { tip_VALUE = 3; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(Ljava/lang/String;)V")) { tip_VALUE = 4; VALUE = 빼기(2); }
            else if (!Word_SMS(format_VALUE, "()V") || !Word_SMS(ime, "println")) otkazivanje_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) otkazivanje_VALUE("invalid PrintStream receiver");
            if (greška) return;
            if (tip_VALUE == 1) 자바도구.수쓰기(VALUE);
            if (tip_VALUE == 2) korisnik.쓰기(VALUE == 0 ? "false" : "true");
            if (tip_VALUE == 3) korisnik.문자쓰기(VALUE & 65535);
            if (tip_VALUE == 4) 글쓰기(VALUE);
            if (Word_SMS(ime, "println")) korisnik.문자쓰기(10);
            return;
        }
        if (komanda == 182 && Word_SMS(vlasnik_VALUE, "java/lang/String")) {
            if (Word_SMS(ime, "length") && Word_SMS(format_VALUE, "()I")) {
                int referenca = 빼기(2); if (objekat_VALUE(referenca, 1)) 넣기(힙[referenca + 1], 1); return;
            }
            if (Word_SMS(ime, "charAt") && Word_SMS(format_VALUE, "(I)C")) {
                int indeksni_tekst_VALUE = 빼기(1), referenca = 빼기(2);
                if (objekat_VALUE(referenca, 1)) {
                    if (indeksni_tekst_VALUE < 0 || indeksni_tekst_VALUE >= 힙[referenca + 1]) otkazivanje_VALUE("StringIndexOutOfBoundsException"); else 넣기(힙[referenca + 2 + indeksni_tekst_VALUE], 1);
                }
                return;
            }
        }
        if (Word_SMS(vlasnik_VALUE, "java/lang/StringBuilder")) {
            if (komanda == 183 && Word_SMS(ime, "<init>") && Word_SMS(format_VALUE, "()V")) { objekat_VALUE(빼기(2), 4); return; }
            if (komanda == 182 && Word_SMS(ime, "toString") && Word_SMS(format_VALUE, "()Ljava/lang/String;")) {
                int referenca = 빼기(2); if (objekat_VALUE(referenca, 4)) 넣기(힙[referenca + 2] == 0 ? host_znak("") : 힙[referenca + 2], 2); return;
            }
            if (komanda == 182 && Word_SMS(ime, "append")) {
                int SMS = 0;
                if (Word_SMS(format_VALUE, "(I)Ljava/lang/StringBuilder;")) SMS = cifra_znak(빼기(1));
                else if (Word_SMS(format_VALUE, "(Z)Ljava/lang/StringBuilder;")) SMS = host_znak(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(format_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); SMS = dodeliti_Skladište(1, 1); if (!greška) 힙[SMS + 2] = VALUE & 65535;
                }
                else if (Word_SMS(format_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { SMS = 빼기(2); if (SMS == 0) SMS = host_znak("null"); }
                else { otkazivanje_VALUE("unsupported StringBuilder append"); return; }
                int referenca = 빼기(2); if (!objekat_VALUE(referenca, 4) || !objekat_VALUE(SMS, 1)) return;
                int čeona_kamera_VALUE = 힙[referenca + 2], 앞길이 = čeona_kamera_VALUE == 0 ? 0 : 힙[čeona_kamera_VALUE + 1], 뒤길이 = 힙[SMS + 1];
                int 새글 = dodeliti_Skladište(1, 앞길이 + 뒤길이); if (greška) return;
                for (int 수 = 0; 수 < 앞길이; 수++) 힙[새글 + 2 + 수] = 힙[čeona_kamera_VALUE + 2 + 수];
                for (int 수 = 0; 수 < 뒤길이; 수++) 힙[새글 + 2 + 앞길이 + 수] = 힙[SMS + 2 + 수];
                힙[referenca + 2] = 새글; 넣기(referenca, 2); return;
            }
        }
        otkazivanje_VALUE("unsupported library method");
    }
    static int 배열칸(int referenca, int indeksni_tekst_VALUE, int tip_VALUE) {
        if (!objekat_VALUE(referenca, tip_VALUE)) return 0;
        if (indeksni_tekst_VALUE < 0 || indeksni_tekst_VALUE >= 힙[referenca + 1]) { otkazivanje_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return referenca + 2 + indeksni_tekst_VALUE;
    }
    static void Izvrši_komanda() {
        int 남음 = 500000;
        while (kadar_INDEX >= 0 && !greška) {
            if (--남음 == 0) { otkazivanje_VALUE("instruction limit (500000)"); break; }
            int koristiti = kadar_pozicija[kadar_INDEX], VALUE = 명바();
            if (greška) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = VALUE == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= konstanta_COUNT) otkazivanje_VALUE("invalid ldc constant");
                else if (konstanta_oznaka[수] == 3) 넣기(상가[수], 1);
                else if (konstanta_oznaka[수] == 8) 넣기(konstanta_SMS(상가[수]), 2);
                else otkazivanje_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { 지역쓰기(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { 지역쓰기(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { 지역쓰기(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE == 50) {
                int indeksni_tekst_VALUE = 빼기(1), referenca = 빼기(2), 칸 = 배열칸(referenca, indeksni_tekst_VALUE, VALUE == 46 ? 2 : 3);
                if (!greška) 넣기(힙[칸], VALUE == 46 ? 1 : 2); continue;
            }
            if (VALUE == 79 || VALUE == 83) {
                int stavka_element = 빼기(VALUE == 79 ? 1 : 2), indeksni_tekst_VALUE = 빼기(1), referenca = 빼기(2), 칸 = 배열칸(referenca, indeksni_tekst_VALUE, VALUE == 79 ? 2 : 3);
                if (VALUE == 83 && stavka_element != 0) objekat_VALUE(stavka_element, 1);
                if (!greška) 힙[칸] = stavka_element; continue;
            }
            if (VALUE == 87) { 빼기(0); continue; }
            if (VALUE == 89) { int 가 = 빼기(0), tip_VALUE = vratiti_tip; 넣기(가, tip_VALUE); 넣기(가, tip_VALUE); continue; }
            if (VALUE == 95) { int 가 = 빼기(0), 가형 = vratiti_tip, SECOND_operand = 빼기(0), SECOND_operand_tip = vratiti_tip; 넣기(가, 가형); 넣기(SECOND_operand, SECOND_operand_tip); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int SECOND_operand = 빼기(1), 가 = 빼기(1), KR = 0;
                if ((VALUE == 108 || VALUE == 112) && SECOND_operand == 0) { otkazivanje_VALUE("ArithmeticException: / by zero"); continue; }
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
                int lokalni_skup = 명바(), 증분 = (byte)명바(); 지역읽기(lokalni_skup, 1); 넣기(빼기(1) + 증분, 1); 지역쓰기(lokalni_skup, 1); continue;
            }
            if (VALUE >= 145 && VALUE <= 147) {
                int 수 = 빼기(1); 넣기(VALUE == 145 ? (byte)수 : VALUE == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                int odredište_VALUE = koristiti + (short)명짧(); boolean 갈까 = VALUE == 167;
                if (VALUE >= 153 && VALUE <= 158) {
                    int 수 = 빼기(1); 갈까 = VALUE == 153 ? 수 == 0 : VALUE == 154 ? 수 != 0 : VALUE == 155 ? 수 < 0 : VALUE == 156 ? 수 >= 0 : VALUE == 157 ? 수 > 0 : 수 <= 0;
                } else if (VALUE >= 159 && VALUE <= 166) {
                    int SECOND_operand = 빼기(VALUE >= 165 ? 2 : 1), 가 = 빼기(VALUE >= 165 ? 2 : 1);
                    갈까 = VALUE == 159 || VALUE == 165 ? 가 == SECOND_operand : VALUE == 160 || VALUE == 166 ? 가 != SECOND_operand : VALUE == 161 ? 가 < SECOND_operand : VALUE == 162 ? 가 >= SECOND_operand : VALUE == 163 ? 가 > SECOND_operand : 가 <= SECOND_operand;
                } else if (VALUE == 198 || VALUE == 199) { int 수 = 빼기(2); 갈까 = VALUE == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) premestiti_VALUE(odredište_VALUE); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { vratiti_KR(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE == 178) {
                int 수 = 명짧(); if (!proveriti_konstanta(수, 9)) continue;
                if (!Word_SMS(ime_klase_SMS(상가[수]), "java/lang/System") || !Word_SMS(referenca_ime(konstanta_SECOND_VALUE[수]), "out")
                    || !Word_SMS(referenca_tip(konstanta_SECOND_VALUE[수]), "Ljava/io/PrintStream;")) otkazivanje_VALUE("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (VALUE == 182 || VALUE == 183 || VALUE == 184) { CALL_metod(명짧(), VALUE); continue; }
            if (VALUE == 187) {
                int ime = ime_klase_SMS(명짧());
                if (Word_SMS(ime, "java/lang/StringBuilder")) 넣기(dodeliti_Skladište(4, 1), 2);
                else if (Word_SMS(ime, "java/io/FileInputStream") || Word_SMS(ime, "java/io/FileOutputStream")) {
                    int referenca = dodeliti_Skladište(Word_SMS(ime, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!greška) { 힙[referenca + 2] = -1; 넣기(referenca, 2); }
                } else otkazivanje_VALUE("unsupported object construction");
                continue;
            }
            if (VALUE == 188 || VALUE == 189) {
                if (VALUE == 188) { if (명바() != 10) otkazivanje_VALUE("only int[] newarray is supported"); }
                else if (!Word_SMS(ime_klase_SMS(명짧()), "java/lang/String")) otkazivanje_VALUE("only String[] anewarray is supported");
                int 길이 = 빼기(1); 넣기(dodeliti_Skladište(VALUE == 188 ? 2 : 3, 길이), 2); continue;
            }
            if (VALUE == 190) {
                int referenca = 빼기(2);
                if (referenca < 1 || referenca >= 힙끝 - 1 || (힙[referenca] != 2 && 힙[referenca] != 3)) otkazivanje_VALUE("null or invalid array");
                else 넣기(힙[referenca + 1], 1); continue;
            }
            if (VALUE == 192) {
                int ime = ime_klase_SMS(명짧()), referenca = 빼기(2);
                if (!Word_SMS(ime, "java/lang/String")) otkazivanje_VALUE("unsupported checkcast");
                else if (referenca != 0) objekat_VALUE(referenca, 1);
                넣기(referenca, 2); continue;
            }
            otkazivanje_VALUE("unsupported bytecode");
        }
    }
    public static int koristiti() {
        if (korisnik.인수개수() == 1 && 자바도구.같음(korisnik.인수(0), "-version")) {
            korisnik.쓰기("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (korisnik.인수개수() < 1) { korisnik.쓰기("Usage: java CLASS [ARGS]\n"); return 2; }
        int 길이 = 자바도구.ime(ime_datoteke_SMS, korisnik.인수(0));
        if (길이 < 1 || 길이 > 57) { korisnik.쓰기("java: invalid class name\n"); return 2; }
        ime_datoteke_SMS[길이] = '.'; ime_datoteke_SMS[길이 + 1] = 'c'; ime_datoteke_SMS[길이 + 2] = 'l'; ime_datoteke_SMS[길이 + 3] = 'a'; ime_datoteke_SMS[길이 + 4] = 's'; ime_datoteke_SMS[길이 + 5] = 's';
        promeniti_veličinu = korisnik.파일읽기(ime_datoteke_SMS, Datoteka);
        if (promeniti_veličinu < 0) { korisnik.쓰기("java: cannot read class: "); 자바도구.수쓰기(promeniti_veličinu); korisnik.문자쓰기(10); return 1; }
        클래스읽기(); if (greška) return 1;
        int znak_ime = konstanta_SMS(ime_klase);
        if (!greška && 힙[znak_ime + 1] != 길이) otkazivanje_VALUE("class name does not match file");
        for (int 수 = 0; 수 < 길이 && !greška; 수++) if (힙[znak_ime + 2 + 수] != ime_datoteke_SMS[수]) otkazivanje_VALUE("class name does not match file");
        int stavka_p_VALUE = -1;
        for (int 수 = 0; 수 < metod_COUNT; 수++) if (Word_SMS(metod_ime_SMS[수], "main") && Word_SMS(metod_tip[수], "([Ljava/lang/String;)V") && (metod_pristup[수] & 9) == 9) stavka_p_VALUE = 수;
        if (stavka_p_VALUE < 0) otkazivanje_VALUE("public static void main(String[] args) required");
        if (greška) return 1;
        int 인수 = dodeliti_Skladište(3, korisnik.인수개수() - 1);
        for (int 수 = 1; 수 < korisnik.인수개수() && !greška; 수++) 힙[인수 + 1 + 수] = host_znak(korisnik.인수(수));
        kadar_INDEX = 0; kadar_metod[0] = stavka_p_VALUE; kadar_pozicija[0] = metod_START[stavka_p_VALUE]; lokalni_VALUE[0] = 인수; lokalni_tip[0] = 2;
        Izvrši_komanda(); return greška ? 1 : 0;
    }
}
