// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Datoteka/operand_hrpa/Reference/grana 경계를 Izvrši_naredba 중 검사한다. */
public final class 자바가상기계 {
    static int[] Datoteka = new int[16 * 16384], privremena_datoteka = new int[16384], naziv_datoteke_SMS = new int[512];
    static int[] konstanta_oznaka = new int[8192], 상가 = new int[8192], konstanta_SECOND_VALUE = new int[8192], niz_Reference = new int[8192];
    static int[] postupak_naziv_SMS = new int[512], postupak_TYPE = new int[512], postupak_pristup = new int[512], postupak_vlasnik = new int[512];
    static int[] postupak_START = new int[512], postupak_završiti_razgovor = new int[512], postupak_hrpa = new int[512], 함수지역 = new int[512];
    static int[] postupak_argument_COUNT = new int[512], postupak_argument_TYPE = new int[8192], postupak_vratiti = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] lokalno_VALUE = new int[16384], lokalno_TYPE = new int[16384], operand_hrpa_VALUE = new int[16384], operand_hrpa_TYPE = new int[16384];
    static int[] kadar_postupak = new int[128], kadar_položaj = new int[128], kadar_hrpa = new int[128], 틀명령 = new int[128], 틀초기화 = new int[128];
    static int[] poduka_definicija_naziv = new int[16], poduka_definicija_promijeniti_veličinu = new int[16], poduka_definicija_roditeljski = new int[16], poduka_definicija_Stanje = new int[16], 종칸수 = new int[16], 종초기화 = new int[16];
    static int[] poduka_sučelje = new int[16 * 16], poduka_sučelje_COUNT = new int[16];
    static int[] 칸이름 = new int[512], 칸형 = new int[512], 칸주인 = new int[512], 칸권한 = new int[512], 칸위치 = new int[512], 칸값 = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], element_polja = new int[32768], Store_cijeli_broj = new int[256];
    static int Veličina, 읽기위치, postupak_COUNT, naziv_klase, kadar_INDEX = -1, 힙끝 = 1, vratiti_TYPE;
    static int poduka_definicija_COUNT, 칸수, 잡기수, 현재읽는종, 던진객체, 잠시수, zaslon_COUNT, Zbirka_COUNT;
    static int redovno_nit, nit_COUNT = 1, unos_poduka_definicija;
    static int[] nit_kadar = new int[4], nit_Stanje = new int[4], nit_objekt = new int[4], nit_cilj = new int[4], 가닥대기 = new int[4];
    static boolean GREŠKA, promijeniti_zahtjev;
    static int[] zaključati_vlasnik = new int[32768], 잠금깊이 = new int[32768], kadar_zaključati = new int[128], poduka_zaključati = new int[16], poduka_nit = new int[16];

    static void kvar_VALUE(String Word_SMS) {
        if (GREŠKA) return;
        int područje_kod = 0;
        if (자바도구.같음(Word_SMS, "ArithmeticException: / by zero")) područje_kod = 4;
        if (자바도구.같음(Word_SMS, "NullPointerException") || 자바도구.같음(Word_SMS, "null or invalid array")) područje_kod = 5;
        if (자바도구.같음(Word_SMS, "ArrayIndexOutOfBoundsException")) područje_kod = 7;
        if (자바도구.같음(Word_SMS, "StringIndexOutOfBoundsException")) područje_kod = 8;
        if (자바도구.같음(Word_SMS, "NumberFormatException")) područje_kod = 10;
        if (자바도구.같음(Word_SMS, "FileNotFoundException: file open failed")) područje_kod = 12;
        if (자바도구.같음(Word_SMS, "IOException: stream closed") || 자바도구.같음(Word_SMS, "IOException: read failed") || 자바도구.같음(Word_SMS, "IOException: write failed")) područje_kod = 11;
        if (자바도구.같음(Word_SMS, "ClassCastException")) područje_kod = 14;
        if (자바도구.같음(Word_SMS, "NegativeArraySizeException")) područje_kod = 15;
        if (područje_kod != 0 && kadar_INDEX >= 0) { 예외던짐(područje_kod, Word_SMS); return; }
        korisnik.Zapisuj("JVM error: "); korisnik.Zapisuj(Word_SMS); korisnik.zapisivanje_znak_VALUE(10); GREŠKA = true;
    }
    static boolean isječak(int Pokreni, int 길이) {
        if (Pokreni < 0 || Pokreni >= Datoteka.length || 길이 < 0) return false;
        int poduka_definicija = Pokreni / 16384;
        return Pokreni % 16384 <= poduka_definicija_promijeniti_veličinu[poduka_definicija] && 길이 <= poduka_definicija_promijeniti_veličinu[poduka_definicija] - Pokreni % 16384;
    }
    static int bajt_VALUE() {
        if (!isječak(읽기위치, 1)) { kvar_VALUE("truncated class file"); return 0; }
        return Datoteka[읽기위치++];
    }
    static int 짧은수() { return bajt_VALUE() << 8 | bajt_VALUE(); }
    static int cijeli_broj() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int 길이) { if (!isječak(읽기위치, 길이)) kvar_VALUE("invalid attribute size"); else 읽기위치 += 길이; }
    static boolean 상검사(int 수, int 종류) {
        if (수 <= 0 || 수 >= konstanta_oznaka.length || konstanta_oznaka[수] != 종류) { kvar_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_raspon(int Pokreni, int 길이, String Word_SMS) {
        if (!isječak(Pokreni, 길이)) return false;
        int 읽는자리 = Pokreni, 끝 = Pokreni + 길이;
        for (int Loop_INDEX = 0; Loop_INDEX < Word_SMS.length(); Loop_INDEX++) {
            int kodna_točka = Word_SMS.charAt(Loop_INDEX);
            if (kodna_točka > 0 && kodna_točka < 128) { if (읽는자리 >= 끝 || Datoteka[읽는자리++] != kodna_točka) return false; }
            else if (kodna_točka < 2048) {
                if (읽는자리 + 2 > 끝 || Datoteka[읽는자리++] != (192 | (kodna_točka >> 6)) || Datoteka[읽는자리++] != (128 | (kodna_točka & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Datoteka[읽는자리++] != (224 | (kodna_točka >> 12)) || Datoteka[읽는자리++] != (128 | ((kodna_točka >> 6) & 63)) || Datoteka[읽는자리++] != (128 | (kodna_točka & 63))) return false;
        }
        return 읽는자리 == 끝;
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
    static int 상번호() { int VALUE = 짧은수(); return VALUE == 0 ? 0 : 현재읽는종 * 512 + VALUE; }
    static int 명상수() { return postupak_vlasnik[kadar_postupak[kadar_INDEX]] * 512 + 명짧(); }
    static void 속성건너() {
        int artikl_COUNT = 짧은수();
        for (int 수 = 0; 수 < artikl_COUNT && !GREŠKA; 수++) { 상검사(상번호(), 1); 건너(cijeli_broj()); }
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
    static int položaj_cijeli_broj(int 읽는자리) {
        if (!isječak(읽는자리, 4)) { kvar_VALUE("truncated bytecode operand"); return 0; }
        return Datoteka[읽는자리] << 24 | Datoteka[읽는자리 + 1] << 16 | Datoteka[읽는자리 + 2] << 8 | Datoteka[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Pokreni, int 끝) {
        int VALUE = Datoteka[읽는자리], 길이 = 명령길이(VALUE);
        if (VALUE == 170 || VALUE == 171) {
            int BASE_položaj = 읽는자리 + 1;
            while ((BASE_položaj - Pokreni) % 4 != 0) BASE_položaj++;
            if (끝 - BASE_položaj < (VALUE == 170 ? 12 : 8)) return 0;
            int unos_COUNT = VALUE == 170 ? položaj_cijeli_broj(BASE_položaj + 8) - položaj_cijeli_broj(BASE_položaj + 4) + 1 : položaj_cijeli_broj(BASE_položaj + 4);
            if (unos_COUNT < 0 || unos_COUNT > 2048) return 0;
            길이 = BASE_položaj - 읽는자리 + (VALUE == 170 ? 12 + 4 * unos_COUNT : 8 + 8 * unos_COUNT);
        }
        if (VALUE == 196 && 읽는자리 + 1 < 끝) {
            int Word_podaci = Datoteka[읽는자리 + 1]; 길이 = Word_podaci == 132 ? 6 : (Word_podaci == 21 || Word_podaci == 25 || Word_podaci == 54 || Word_podaci == 58) ? 4 : 0;
        }
        return 길이 > 0 && 길이 <= 끝 - 읽는자리 ? 길이 : 0;
    }
    static void 목적검사(int odredište_VALUE, int FUNCTION_VALUE) {
        if (odredište_VALUE < postupak_START[FUNCTION_VALUE] || odredište_VALUE >= postupak_završiti_razgovor[FUNCTION_VALUE] || 경계[odredište_VALUE] != FUNCTION_VALUE + 1) kvar_VALUE("invalid branch target");
    }
    static void 클래스읽기(int poduka_definicija) {
        현재읽는종 = poduka_definicija; 읽기위치 = poduka_definicija * 16384; Veličina = 읽기위치 + poduka_definicija_promijeniti_veličinu[poduka_definicija];
        if (cijeli_broj() != 0xcafebabe) { kvar_VALUE("not a class file"); return; }
        int 부판 = 짧은수(), verzija_VALUE = 짧은수();
        if (verzija_VALUE < 45 || verzija_VALUE > 52 || 부판 != 0) { kvar_VALUE("supported class versions: 45..52, minor 0"); return; }
        int konstanta_COUNT = 짧은수(), BASE_položaj = poduka_definicija * 512;
        if (konstanta_COUNT < 1 || konstanta_COUNT > 512) { kvar_VALUE("constant pool limit (511)"); return; }
        for (int unos_COUNT = 1; unos_COUNT < konstanta_COUNT && !GREŠKA; unos_COUNT++) {
            int 수 = BASE_položaj + unos_COUNT, 종류 = bajt_VALUE(); konstanta_oznaka[수] = 종류;
            if (종류 == 1) { konstanta_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(konstanta_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = cijeli_broj();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); konstanta_SECOND_VALUE[수] = 상번호(); }
            else kvar_VALUE("unsupported constant type");
        }
        int dozvola_VALUE = 짧은수();
        if ((dozvola_VALUE & (0x2000 | 0x4000)) != 0) kvar_VALUE("annotation/enum class unsupported");
        poduka_definicija_naziv[poduka_definicija] = naziv_klase_SMS(상번호());
        poduka_definicija_roditeljski[poduka_definicija] = naziv_klase_SMS(상번호());
        int sučelje_COUNT = 짧은수(); if (sučelje_COUNT > 16) { kvar_VALUE("interface count limit"); return; }
        poduka_sučelje_COUNT[poduka_definicija] = sučelje_COUNT;
        for (int Loop_INDEX = 0; Loop_INDEX < sučelje_COUNT; Loop_INDEX++) poduka_sučelje[poduka_definicija * 16 + Loop_INDEX] = naziv_klase_SMS(상번호());
        int polje_COUNT = 짧은수();
        if (polje_COUNT > 512 - 칸수) { kvar_VALUE("field count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < polje_COUNT && !GREŠKA; Loop_INDEX++) {
            int Datoteka_INDEX = 칸수++; 칸주인[Datoteka_INDEX] = poduka_definicija; 칸권한[Datoteka_INDEX] = 짧은수(); 칸이름[Datoteka_INDEX] = 상번호(); 칸형[Datoteka_INDEX] = 상번호();
            상검사(칸이름[Datoteka_INDEX], 1); 상검사(칸형[Datoteka_INDEX], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[칸형[Datoteka_INDEX]]; int područje_kod = 서술형(읽기위치 + konstanta_SECOND_VALUE[칸형[Datoteka_INDEX]], false); 읽기위치 = 보존값;
            if ((칸권한[Datoteka_INDEX] & 8) == 0) 칸위치[Datoteka_INDEX] = 종칸수[poduka_definicija]++;
            int atribut_podaci = 짧은수();
            for (int unutarnji_položaj = 0; unutarnji_položaj < atribut_podaci && !GREŠKA; unutarnji_položaj++) {
                int naziv_konstanta = 상번호(), 유효길이 = cijeli_broj();
                if (Word_SMS(naziv_konstanta, "ConstantValue") && 유효길이 == 2) {
                    int podaci_VALUE = 상번호();
                    if (područje_kod == 1 && 상검사(podaci_VALUE, 3)) 칸값[Datoteka_INDEX] = 상가[podaci_VALUE];
                    else if (područje_kod == 2 && 상검사(podaci_VALUE, 8)) 칸값[Datoteka_INDEX] = konstanta_SMS(상가[podaci_VALUE]);
                } else 건너(유효길이);
            }
        }
        int artikl_COUNT = 짧은수();
        if (artikl_COUNT > 512 - postupak_COUNT) { kvar_VALUE("method count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < artikl_COUNT && !GREŠKA; Loop_INDEX++) {
            int 수 = postupak_COUNT++; postupak_vlasnik[수] = poduka_definicija;
            postupak_pristup[수] = 짧은수(); postupak_naziv_SMS[수] = 상번호(); postupak_TYPE[수] = 상번호();
            상검사(postupak_naziv_SMS[수], 1); 서술읽기(수);
            if ((postupak_pristup[수] & 8) == 0) {
                if (postupak_argument_COUNT[수] == 16) { kvar_VALUE("too many instance method arguments"); return; }
                for (int Usporedba_položaj = postupak_argument_COUNT[수]; Usporedba_položaj > 0; Usporedba_položaj--) postupak_argument_TYPE[수 * 16 + Usporedba_položaj] = postupak_argument_TYPE[수 * 16 + Usporedba_položaj - 1];
                postupak_argument_TYPE[수 * 16] = 2; postupak_argument_COUNT[수]++;
            }
            if ((postupak_pristup[수] & 0x100) != 0) kvar_VALUE("user native method unsupported");
            if (Word_SMS(postupak_naziv_SMS[수], "<clinit>")) 종초기화[poduka_definicija] = 수 + 1;
            for (int prednja_VALUE = 0; prednja_VALUE < 수; prednja_VALUE++) if (postupak_vlasnik[prednja_VALUE] == poduka_definicija && 같은말(postupak_naziv_SMS[prednja_VALUE], postupak_naziv_SMS[수]) && 같은말(postupak_TYPE[prednja_VALUE], postupak_TYPE[수])) kvar_VALUE("duplicate method");
            int atribut_COUNT = 짧은수();
            for (int atribut_VALUE = 0; atribut_VALUE < atribut_COUNT && !GREŠKA; atribut_VALUE++) {
                int Ime = 상번호(), 길이 = cijeli_broj(), Pokreni = 읽기위치;
                if (!isječak(Pokreni, 길이)) { kvar_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Ime, "Code")) {
                    if (postupak_START[수] != 0) kvar_VALUE("duplicate Code attribute");
                    postupak_hrpa[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = cijeli_broj();
                    if (postupak_hrpa[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < postupak_argument_COUNT[수]
                        || 코드길이 < 1 || 코드길이 > 8192) kvar_VALUE("method memory limits exceeded");
                    postupak_START[수] = 읽기위치; 건너(코드길이); postupak_završiti_razgovor[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { kvar_VALUE("exception table limit"); return; }
                    for (int unutarnji_položaj = 0; unutarnji_položaj < 잡는수; unutarnji_položaj++) {
                        int pogreška_Reference = 잡기수++; 잡기함수[pogreška_Reference] = 수;
                        잡기시작[pogreška_Reference] = postupak_START[수] + 짧은수(); 잡기끝[pogreška_Reference] = postupak_START[수] + 짧은수();
                        잡기위치[pogreška_Reference] = postupak_START[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[pogreška_Reference] = 부호값 == 0 ? 0 : naziv_klase_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != Pokreni + 길이) kvar_VALUE("Code attribute size mismatch");
                } else 건너(길이);
            }
            if ((postupak_pristup[수] & 0x400) != 0) continue;
            if (postupak_START[수] == 0) kvar_VALUE("missing Code attribute");
            int 칸 = postupak_START[수];
            while (칸 < postupak_završiti_razgovor[수] && !GREŠKA) {
                int 길이 = 길이읽기(칸, postupak_START[수], postupak_završiti_razgovor[수]);
                if (길이 == 0) { kvar_VALUE("unsupported or truncated bytecode"); break; }
                경계[칸] = 수 + 1; 칸 += 길이;
            }
            칸 = postupak_START[수];
            while (칸 < postupak_završiti_razgovor[수] && !GREŠKA) {
                int VALUE = Datoteka[칸];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) 목적검사(칸 + (short)(Datoteka[칸 + 1] << 8 | Datoteka[칸 + 2]), 수);
                if (VALUE == 200) 목적검사(칸 + položaj_cijeli_broj(칸 + 1), 수);
                if (VALUE == 170 || VALUE == 171) {
                    int 읽는자리 = 칸 + 1; while ((읽는자리 - postupak_START[수]) % 4 != 0) 읽는자리++;
                    목적검사(칸 + položaj_cijeli_broj(읽는자리), 수);
                    int unos_COUNT = VALUE == 170 ? položaj_cijeli_broj(읽는자리 + 8) - položaj_cijeli_broj(읽는자리 + 4) + 1 : položaj_cijeli_broj(읽는자리 + 4);
                    읽는자리 += VALUE == 170 ? 12 : 8;
                    for (int unutarnji_položaj = 0; unutarnji_položaj < unos_COUNT; unutarnji_položaj++) 목적검사(칸 + položaj_cijeli_broj(읽는자리 + unutarnji_položaj * (VALUE == 170 ? 4 : 8) + (VALUE == 170 ? 0 : 4)), 수);
                }
                칸 += 길이읽기(칸, postupak_START[수], postupak_završiti_razgovor[수]);
            }
            for (int unutarnji_položaj = 0; unutarnji_položaj < 잡기수; unutarnji_položaj++) if (잡기함수[unutarnji_položaj] == 수) {
                목적검사(잡기시작[unutarnji_položaj], 수); 목적검사(잡기위치[unutarnji_položaj], 수);
                if (잡기끝[unutarnji_položaj] != postupak_završiti_razgovor[수]) 목적검사(잡기끝[unutarnji_položaj], 수);
                if (잡기시작[unutarnji_položaj] >= 잡기끝[unutarnji_položaj]) kvar_VALUE("invalid exception range");
            }
        }
        if (!GREŠKA) 속성건너();
        if (읽기위치 != Veličina) kvar_VALUE("extra class file data");
    }
    static int dodijeli_Pohrana(int 종류, int 길이) { return 새기억(종류, 길이); }
    static boolean objekt_VALUE(int Reference, int 종류) {
        if (!객체유효(Reference)) return false;
        if (힙[Reference] != 종류) { kvar_VALUE("object type mismatch"); return false; }
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
        if (vratiti_TYPE == 2) zaštititi_VALUE(operand_hrpa_VALUE[칸]);
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
        if (kadar_INDEX % 32 == 31) { kvar_VALUE("call stack limit (32)"); return; }
        int Dalje_artikl = kadar_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) lokalno_TYPE[Dalje_artikl * 128 + 수] = 0;
        for (int 수 = postupak_argument_COUNT[FUNCTION_VALUE] - 1; 수 >= 0; 수--) {
            lokalno_VALUE[Dalje_artikl * 128 + 수] = 빼기(postupak_argument_TYPE[FUNCTION_VALUE * 16 + 수]); lokalno_TYPE[Dalje_artikl * 128 + 수] = postupak_argument_TYPE[FUNCTION_VALUE * 16 + 수];
        }
        if (GREŠKA) return;
        kadar_INDEX = Dalje_artikl; 틀초기화[kadar_INDEX] = 0; kadar_postupak[kadar_INDEX] = FUNCTION_VALUE; kadar_položaj[kadar_INDEX] = postupak_START[FUNCTION_VALUE]; kadar_hrpa[kadar_INDEX] = 0;
    }
    static void vratiti_KR(int TYPE_VALUE) {
        if (TYPE_VALUE != postupak_vratiti[kadar_postupak[kadar_INDEX]]) { kvar_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        if (틀초기화[kadar_INDEX] != 0) poduka_definicija_Stanje[틀초기화[kadar_INDEX] - 1] = 2;
        if (kadar_zaključati[kadar_INDEX] != 0) { izdati_zaključati(kadar_zaključati[kadar_INDEX]); kadar_zaključati[kadar_INDEX] = 0; }
        kadar_INDEX--; if (kadar_INDEX >= redovno_nit * 32 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
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
                if (VALUE < 1) { kvar_VALUE("invalid file stream path"); return; }
                tok_naziv_datoteke[칸] = VALUE;
            }
            tok_naziv_datoteke[길이] = 0;
            int 서술자 = korisnik.파일서술자열기(tok_naziv_datoteke, Izlaz ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { kvar_VALUE("FileNotFoundException: file open failed"); return; }
            힙[tok_VALUE + 2] = 서술자; 힙[tok_VALUE + 3] = 1;
            return;
        }
        if (Naredba != 182) { kvar_VALUE("invalid file stream invocation"); return; }
        if ((Izlaz && Word_SMS(Ime, "write") || !Izlaz && Word_SMS(Ime, "read"))
            && (Word_SMS(oblik_VALUE, Izlaz ? "([B)V" : "([B)I") || Word_SMS(oblik_VALUE, Izlaz ? "([BII)V" : "([BII)I"))) {
            boolean isječak_VALUE = Word_SMS(oblik_VALUE, Izlaz ? "([BII)V" : "([BII)I");
            int unos_COUNT = isječak_VALUE ? 빼기(1) : 0, 시작점 = isječak_VALUE ? 빼기(1) : 0, podaci_ARRAY = 빼기(2), objekt_Reference = 빼기(2);
            if (!objekt_VALUE(podaci_ARRAY, 20) || !objekt_VALUE(objekt_Reference, 종류)) return;
            if (!isječak_VALUE) unos_COUNT = 힙[podaci_ARRAY + 1];
            if (시작점 < 0 || unos_COUNT < 0 || 시작점 > 힙[podaci_ARRAY + 1] - unos_COUNT) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[objekt_Reference + 3] == 0 || 힙[objekt_Reference + 2] < 0) { kvar_VALUE("IOException: stream closed"); return; }
            int Dovršeno_COUNT = 0;
            while (Dovršeno_COUNT < unos_COUNT && !GREŠKA) {
                int 반환값 = Izlaz ? korisnik.파일한바이트쓰기(힙[objekt_Reference + 2], 힙[podaci_ARRAY + 2 + 시작점 + Dovršeno_COUNT]) : korisnik.파일한바이트읽기(힙[objekt_Reference + 2]);
                if (반환값 < 0) { kvar_VALUE(Izlaz ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!Izlaz && 반환값 == 256) break;
                if (!Izlaz) 힙[podaci_ARRAY + 2 + 시작점 + Dovršeno_COUNT] = (byte)반환값;
                Dovršeno_COUNT++;
            }
            if (!Izlaz) 넣기(unos_COUNT != 0 && Dovršeno_COUNT == 0 ? -1 : Dovršeno_COUNT, 1);
            return;
        }
        if (Izlaz && Word_SMS(Ime, "flush") && Word_SMS(oblik_VALUE, "()V")) { int objekt_Reference = 빼기(2); if (objekt_VALUE(objekt_Reference, 종류) && 힙[objekt_Reference + 2] < 0) kvar_VALUE("IOException: stream closed"); return; }
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
            if (REZULTAT < -1) kvar_VALUE("IOException: read failed"); else 넣기(REZULTAT == 256 ? -1 : REZULTAT, 1);
        } else if (korisnik.파일한바이트쓰기(서술자, VALUE) != 1) kvar_VALUE("IOException: write failed");
    }
    static void CALL_postupak(int INDEX, int Naredba) {
        if (INDEX <= 0 || INDEX >= konstanta_oznaka.length || (konstanta_oznaka[INDEX] != 10 && konstanta_oznaka[INDEX] != 11)) { kvar_VALUE("invalid method reference"); return; }
        int vlasnik_VALUE = naziv_klase_SMS(상가[INDEX]), Ime = Reference_naziv(konstanta_SECOND_VALUE[INDEX]), oblik_VALUE = Reference_TYPE(konstanta_SECOND_VALUE[INDEX]);
        if (GREŠKA) return;
        if (기본호출(vlasnik_VALUE, Ime, oblik_VALUE, Naredba)) return;
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
        int poduka_definicija = FIND_poduka_definicija(vlasnik_VALUE); if (poduka_definicija < 0 || GREŠKA) return;
        int Datoteka_INDEX = FIND_postupak(poduka_definicija, Ime, oblik_VALUE);
        if (Datoteka_INDEX < 0) {
            for (int kodna_točka = poduka_definicija, unos_COUNT = 0; kodna_točka >= 0 && unos_COUNT < 16; unos_COUNT++, kodna_točka = roditeljski_poduka(kodna_točka))
                if (Word_SMS(poduka_definicija_roditeljski[kodna_točka], "java/lang/Thread")) { 가닥호출(Ime, oblik_VALUE, Naredba); return; }
            kvar_VALUE("NoSuchMethodError"); return;
        }
        if (((postupak_pristup[Datoteka_INDEX] & 8) != 0) != (Naredba == 184)) { kvar_VALUE("method static/instance mismatch"); return; }
        if (Naredba == 184) { if (!초기화(postupak_vlasnik[Datoteka_INDEX], 틀명령[kadar_INDEX])) return; }
        else {
            int 읽는자리 = kadar_hrpa[kadar_INDEX] - postupak_argument_COUNT[Datoteka_INDEX];
            if (읽는자리 < 0 || operand_hrpa_TYPE[kadar_INDEX * 128 + 읽는자리] != 2) { kvar_VALUE("invalid method receiver"); return; }
            int objekt_Reference = operand_hrpa_VALUE[kadar_INDEX * 128 + 읽는자리];
            if (!객체유효(objekt_Reference)) return;
            if (힙[objekt_Reference] < 32 || !종포함(힙[objekt_Reference] - 32, vlasnik_VALUE)) { kvar_VALUE("method receiver type mismatch"); return; }
            if (Naredba != 183) Datoteka_INDEX = FIND_postupak(힙[objekt_Reference] - 32, Ime, oblik_VALUE);
        }
        if (Datoteka_INDEX < 0 || (postupak_pristup[Datoteka_INDEX] & 0x400) != 0) { kvar_VALUE("AbstractMethodError"); return; }
        int zaključati_Reference = 0;
        if ((postupak_pristup[Datoteka_INDEX] & 32) != 0) {
            if (Naredba == 184) { int kodna_točka = postupak_vlasnik[Datoteka_INDEX]; if (poduka_zaključati[kodna_točka] == 0) poduka_zaključati[kodna_točka] = dodijeli_Pohrana(8, 0); zaključati_Reference = poduka_zaključati[kodna_točka]; }
            else zaključati_Reference = operand_hrpa_VALUE[kadar_INDEX * 128 + kadar_hrpa[kadar_INDEX] - postupak_argument_COUNT[Datoteka_INDEX]];
            if (!잠금얻기(zaključati_Reference)) { if (!GREŠKA) kadar_položaj[kadar_INDEX] = 틀명령[kadar_INDEX]; return; }
        }
        호출(Datoteka_INDEX); if (!GREŠKA) kadar_zaključati[kadar_INDEX] = zaključati_Reference;
    }
    static boolean 배열저장가능(int ARRAY_Reference, int podaci_VALUE) {
        if (podaci_VALUE == 0 || element_polja[ARRAY_Reference] == 0) return true;
        boolean 성공여부 = element_polja[ARRAY_Reference] == -1 ? (podaci_VALUE > 0 && podaci_VALUE < 힙끝 && 힙[podaci_VALUE] == 1) : 맞는객체(podaci_VALUE, element_polja[ARRAY_Reference]);
        if (!성공여부 && !GREŠKA) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int 배열칸(int Reference, int indeks_VALUE, int TYPE_VALUE) {
        if (!objekt_VALUE(Reference, TYPE_VALUE)) return 0;
        if (indeks_VALUE < 0 || indeks_VALUE >= 힙[Reference + 1]) { kvar_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return Reference + 2 + indeks_VALUE;
    }
    static void Izvrši_naredba() {
        int 남음 = 500000, fragment_VALUE = 100;
        while (true) {
            if (GREŠKA) { if (던진객체 != 0) ustroj_iznimka(); if (GREŠKA || kadar_INDEX < redovno_nit * 32) break; }
            if (kadar_INDEX < redovno_nit * 32 || promijeniti_zahtjev || --fragment_VALUE == 0) { if (!SWITCH_nit()) break; fragment_VALUE = 100; }
            if (kadar_INDEX == 0 && poduka_definicija_Stanje[unos_poduka_definicija] != 2 && !초기화(unos_poduka_definicija, kadar_položaj[kadar_INDEX])) continue;
            if (kadar_INDEX == redovno_nit * 32 && redovno_nit != 0 && (postupak_pristup[kadar_postupak[kadar_INDEX]] & 32) != 0 && kadar_zaključati[kadar_INDEX] == 0) {
                int objekt_Reference = nit_cilj[redovno_nit]; if (!잠금얻기(objekt_Reference)) { if (GREŠKA) break; continue; } kadar_zaključati[kadar_INDEX] = objekt_Reference;
            }
            잠시수 = 0;
            if (--남음 == 0) { kvar_VALUE("instruction limit (500000)"); break; }
            int Pokreni = kadar_položaj[kadar_INDEX]; 틀명령[kadar_INDEX] = Pokreni; int VALUE = 명바();
            if (GREŠKA) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = postupak_vlasnik[kadar_postupak[kadar_INDEX]] * 512 + (VALUE == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= konstanta_oznaka.length) kvar_VALUE("invalid ldc constant");
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
            if (VALUE == 46 || VALUE >= 50 && VALUE <= 53) {
                int unos_položaj = 빼기(1), objekt_Reference = 빼기(2), područje_kod = VALUE == 46 ? 2 : VALUE == 50 ? 3 : VALUE == 51 ? 20 : VALUE == 52 ? 22 : 23;
                if (VALUE == 51 && objekt_Reference > 0 && objekt_Reference < 힙끝 && 힙[objekt_Reference] == 21) područje_kod = 21;
                int 읽는자리 = 배열칸(objekt_Reference, unos_položaj, područje_kod); if (!GREŠKA) 넣기(힙[읽는자리], VALUE == 50 ? 2 : 1); continue;
            }
            if (VALUE == 79 || VALUE >= 83 && VALUE <= 86) {
                int unos_Reference = 빼기(VALUE == 83 ? 2 : 1), unos_položaj = 빼기(1), objekt_Reference = 빼기(2), područje_kod = VALUE == 79 ? 2 : VALUE == 83 ? 3 : VALUE == 84 ? 20 : VALUE == 85 ? 22 : 23;
                if (VALUE == 84 && objekt_Reference > 0 && objekt_Reference < 힙끝 && 힙[objekt_Reference] == 21) područje_kod = 21;
                int 읽는자리 = 배열칸(objekt_Reference, unos_položaj, područje_kod);
                if (!GREŠKA && područje_kod == 3 && !배열저장가능(objekt_Reference, unos_Reference)) continue;
                if (!GREŠKA) 힙[읽는자리] = područje_kod == 20 ? (byte)unos_Reference : područje_kod == 21 ? unos_Reference & 1 : područje_kod == 22 ? (char)unos_Reference : područje_kod == 23 ? (short)unos_Reference : unos_Reference;
                continue;
            }
            if (VALUE >= 87 && VALUE <= 95) { 스택명령(VALUE); continue; }
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
            if (VALUE >= 178 && VALUE <= 181) { 필드호출(명상수(), VALUE, Pokreni); continue; }
            if (VALUE >= 182 && VALUE <= 185) {
                int 부호값 = 명상수();
                if (VALUE == 185) { int ukupni_zbroj_COUNT = 명바(); if (ukupni_zbroj_COUNT == 0 || 명바() != 0) { kvar_VALUE("invalid invokeinterface operands"); continue; } }
                CALL_postupak(부호값, VALUE); continue;
            }
            if (VALUE == 187) { 새객체(naziv_klase_SMS(명상수()), Pokreni); continue; }
            if (VALUE == 188 || VALUE == 189) {
                int područje_kod = 3, komponenta = 0;
                if (VALUE == 188) { int 임시값 = 명바(); područje_kod = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else komponenta = naziv_klase_SMS(명상수());
                if (područje_kod == 0) { kvar_VALUE("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), objekt_Reference = dodijeli_Pohrana(područje_kod, 유효길이); if (!GREŠKA) element_polja[objekt_Reference] = komponenta; 넣기(objekt_Reference, 2); continue;
            }
            if (VALUE == 190) {
                int objekt_Reference = 빼기(2);
                if (객체유효(objekt_Reference)) { int Usporedba_položaj = 힙[objekt_Reference]; if (Usporedba_položaj != 2 && Usporedba_položaj != 3 && (Usporedba_položaj < 20 || Usporedba_položaj > 23)) kvar_VALUE("not an array"); else 넣기(힙[objekt_Reference + 1], 1); }
                continue;
            }
            if (VALUE == 191) {
                int objekt_Reference = 빼기(2); if (객체유효(objekt_Reference)) { if (힙[objekt_Reference] != 9) kvar_VALUE("athrow requires supported Throwable"); else { 던진객체 = objekt_Reference; GREŠKA = true; } }
                continue;
            }
            if (VALUE == 192 || VALUE == 193) {
                int naziv_konstanta = naziv_klase_SMS(명상수()), objekt_Reference = 빼기(2); boolean MATCH = 맞는객체(objekt_Reference, naziv_konstanta);
                if (VALUE == 193) 넣기(objekt_Reference != 0 && MATCH ? 1 : 0, 1);
                else { if (!MATCH && !GREŠKA) kvar_VALUE("ClassCastException"); 넣기(objekt_Reference, 2); }
                continue;
            }
            if (VALUE == 170 || VALUE == 171) {
                int 읽는자리 = Pokreni + 1, Datoteka_INDEX = kadar_postupak[kadar_INDEX], Ključ_Reference = 빼기(1);
                while ((읽는자리 - postupak_START[Datoteka_INDEX]) % 4 != 0) 읽는자리++;
                int cilj_adresa = položaj_cijeli_broj(읽는자리);
                if (VALUE == 170) { int 낮은값 = položaj_cijeli_broj(읽는자리 + 4), 높은값 = položaj_cijeli_broj(읽는자리 + 8); if (Ključ_Reference >= 낮은값 && Ključ_Reference <= 높은값) cilj_adresa = položaj_cijeli_broj(읽는자리 + 12 + (Ključ_Reference - 낮은값) * 4); }
                else { int ukupni_zbroj_COUNT = položaj_cijeli_broj(읽는자리 + 4); for (int Loop_INDEX = 0; Loop_INDEX < ukupni_zbroj_COUNT; Loop_INDEX++) if (položaj_cijeli_broj(읽는자리 + 8 + Loop_INDEX * 8) == Ključ_Reference) cilj_adresa = položaj_cijeli_broj(읽는자리 + 12 + Loop_INDEX * 8); }
                pomicati_se_VALUE(Pokreni + cilj_adresa); continue;
            }
            if (VALUE == 200) { pomicati_se_VALUE(Pokreni + položaj_cijeli_broj(Pokreni + 1)); continue; }
            if (VALUE == 194 || VALUE == 195) {
                int objekt_Reference = 빼기(2);
                if (VALUE == 195) izdati_zaključati(objekt_Reference);
                else if (!잠금얻기(objekt_Reference) && !GREŠKA) { 넣기(objekt_Reference, 2); kadar_položaj[kadar_INDEX] = Pokreni; }
                continue;
            }
            if (VALUE == 196) {
                int naredba_kod = 명바(), unos_položaj = 명짧();
                if (naredba_kod == 21 || naredba_kod == 25) 지역읽기(unos_položaj, naredba_kod == 21 ? 1 : 2);
                else if (naredba_kod == 54 || naredba_kod == 58) zapisivanje_lokalno(unos_položaj, naredba_kod == 54 ? 1 : 2);
                else if (naredba_kod == 132) { int DELTA_VALUE = (short)명짧(); 지역읽기(unos_položaj, 1); 넣기(빼기(1) + DELTA_VALUE, 1); zapisivanje_lokalno(unos_položaj, 1); }
                else kvar_VALUE("unsupported wide opcode");
                continue;
            }
            kvar_VALUE("unsupported bytecode");
        }
    }
    static int FIND_poduka_definicija(int Ime) {
        for (int Loop_INDEX = 0; Loop_INDEX < poduka_definicija_COUNT; Loop_INDEX++) if (poduka_definicija_naziv[Loop_INDEX] != 0 && 같은말(poduka_definicija_naziv[Loop_INDEX], Ime)) return Loop_INDEX;
        return dosje_poduka_definicija(konstanta_SMS(Ime));
    }
    static int dosje_poduka_definicija(int naziv_niz) {
        if (!objekt_VALUE(naziv_niz, 1)) return -1;
        int 길이 = 힙[naziv_niz + 1];
        if (길이 < 1 || 길이 > 505 || poduka_definicija_COUNT == 16) { kvar_VALUE("class name/count limit"); return -1; }
        for (int Loop_INDEX = 0; Loop_INDEX < 길이; Loop_INDEX++) { int kodna_točka = 힙[naziv_niz + 2 + Loop_INDEX]; naziv_datoteke_SMS[Loop_INDEX] = kodna_točka == '/' ? '.' : kodna_točka; }
        naziv_datoteke_SMS[길이] = '.'; naziv_datoteke_SMS[길이 + 1] = 'c'; naziv_datoteke_SMS[길이 + 2] = 'l'; naziv_datoteke_SMS[길이 + 3] = 'a'; naziv_datoteke_SMS[길이 + 4] = 's'; naziv_datoteke_SMS[길이 + 5] = 's'; naziv_datoteke_SMS[길이 + 6] = 0;
        int Veličina = korisnik.파일읽기(naziv_datoteke_SMS, privremena_datoteka);
        if (Veličina < 0) { kvar_VALUE("ClassNotFoundException"); return -1; }
        int poduka_definicija = poduka_definicija_COUNT++; poduka_definicija_promijeniti_veličinu[poduka_definicija] = Veličina;
        for (int Loop_INDEX = 0; Loop_INDEX < Veličina; Loop_INDEX++) Datoteka[poduka_definicija * 16384 + Loop_INDEX] = privremena_datoteka[Loop_INDEX];
        클래스읽기(poduka_definicija); if (GREŠKA) return -1;
        int stvaran_podaci = konstanta_SMS(poduka_definicija_naziv[poduka_definicija]);
        if (!글같음(stvaran_podaci, naziv_niz, true)) { kvar_VALUE("class name does not match file"); return -1; }
        int roditeljski_VALUE = poduka_definicija_roditeljski[poduka_definicija];
        if (roditeljski_VALUE != 0 && !Word_SMS(roditeljski_VALUE, "java/lang/Object") && !Word_SMS(roditeljski_VALUE, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 pokušati_ponovno_VALUE 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = FIND_poduka_definicija(roditeljski_VALUE);
            if (GREŠKA || 위 < 0) return -1;
            int 읽는자리 = 위, faza_COUNT = 0;
            while (읽는자리 >= 0 && faza_COUNT++ < 16) {
                if (읽는자리 == poduka_definicija) { kvar_VALUE("cyclic inheritance"); return -1; }
                읽는자리 = roditeljski_poduka(읽는자리);
            }
            int 시작변위 = 종칸수[위];
            for (int Datoteka_INDEX = 0; Datoteka_INDEX < 칸수; Datoteka_INDEX++) if (칸주인[Datoteka_INDEX] == poduka_definicija && (칸권한[Datoteka_INDEX] & 8) == 0) 칸위치[Datoteka_INDEX] += 시작변위;
            종칸수[poduka_definicija] += 시작변위;
        }
        return poduka_definicija;
    }
    static int roditeljski_poduka(int poduka_definicija) {
        int Ime = poduka_definicija_roditeljski[poduka_definicija];
        for (int Loop_INDEX = 0; Loop_INDEX < poduka_definicija_COUNT; Loop_INDEX++) if (Ime != 0 && poduka_definicija_naziv[Loop_INDEX] != 0 && 같은말(poduka_definicija_naziv[Loop_INDEX], Ime)) return Loop_INDEX;
        return -1;
    }
    static int FIND_postupak(int poduka_definicija, int Ime, int oblik_VALUE) {
        for (int 깊이 = 0; poduka_definicija >= 0 && 깊이 < 16; 깊이++, poduka_definicija = roditeljski_poduka(poduka_definicija)) {
            for (int Loop_INDEX = 0; Loop_INDEX < postupak_COUNT; Loop_INDEX++) if (postupak_vlasnik[Loop_INDEX] == poduka_definicija && 같은말(postupak_naziv_SMS[Loop_INDEX], Ime) && 같은말(postupak_TYPE[Loop_INDEX], oblik_VALUE)) return Loop_INDEX;
        }
        return -1;
    }
    static int naziv_postupak(int poduka_definicija, String Ime, String oblik_VALUE) {
        for (int 깊이 = 0; poduka_definicija >= 0 && 깊이 < 16; 깊이++, poduka_definicija = roditeljski_poduka(poduka_definicija))
            for (int Loop_INDEX = 0; Loop_INDEX < postupak_COUNT; Loop_INDEX++) if (postupak_vlasnik[Loop_INDEX] == poduka_definicija && Word_SMS(postupak_naziv_SMS[Loop_INDEX], Ime) && Word_SMS(postupak_TYPE[Loop_INDEX], oblik_VALUE)) return Loop_INDEX;
        return -1;
    }
    static int 형종류(int Ime) { return Datoteka[상가[Ime]] == 'L' || Datoteka[상가[Ime]] == '[' ? 2 : 1; }
    static boolean 초기화(int poduka_definicija, int naredba_START) {
        if (poduka_definicija < 0 || GREŠKA) return false;
        if (poduka_definicija_Stanje[poduka_definicija] == 3) { kvar_VALUE("NoClassDefFoundError: initialization failed"); return false; }
        if (poduka_definicija_Stanje[poduka_definicija] == 1 && poduka_nit[poduka_definicija] != redovno_nit) { kadar_položaj[kadar_INDEX] = naredba_START; promijeniti_zahtjev = true; return false; }
        if (poduka_definicija_Stanje[poduka_definicija] != 0) return true;
        int 위 = roditeljski_poduka(poduka_definicija);
        if (위 >= 0 && !초기화(위, naredba_START)) return false;
        poduka_definicija_Stanje[poduka_definicija] = 1; poduka_nit[poduka_definicija] = redovno_nit;
        if (종초기화[poduka_definicija] != 0) {
            kadar_položaj[kadar_INDEX] = naredba_START;
            호출(종초기화[poduka_definicija] - 1); if (!GREŠKA) 틀초기화[kadar_INDEX] = poduka_definicija + 1;
            return false;
        }
        poduka_definicija_Stanje[poduka_definicija] = 2; return true;
    }
    static void 필드호출(int INDEX, int Naredba, int Pokreni) {
        if (!상검사(INDEX, 9)) return;
        int vlasnik_VALUE = naziv_klase_SMS(상가[INDEX]), Ime = Reference_naziv(konstanta_SECOND_VALUE[INDEX]), oblik_VALUE = Reference_TYPE(konstanta_SECOND_VALUE[INDEX]);
        if (Word_SMS(vlasnik_VALUE, "java/lang/System") && (Word_SMS(Ime, "out") || Word_SMS(Ime, "err")) && Word_SMS(oblik_VALUE, "Ljava/io/PrintStream;") && Naredba == 178) { 넣기(-1, 2); return; }
        int poduka_definicija = FIND_poduka_definicija(vlasnik_VALUE); if (poduka_definicija < 0 || GREŠKA) return;
        int 찾음 = -1;
        for (int 읽는자리 = poduka_definicija, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = roditeljski_poduka(읽는자리))
            for (int Datoteka_INDEX = 0; Datoteka_INDEX < 칸수; Datoteka_INDEX++) if (칸주인[Datoteka_INDEX] == 읽는자리 && 같은말(칸이름[Datoteka_INDEX], Ime) && 같은말(칸형[Datoteka_INDEX], oblik_VALUE)) 찾음 = Datoteka_INDEX;
        if (찾음 < 0) { kvar_VALUE("NoSuchFieldError"); return; }
        boolean 정적 = Naredba == 178 || Naredba == 179;
        if (정적 != ((칸권한[찾음] & 8) != 0)) { kvar_VALUE("field static/instance mismatch"); return; }
        if (정적 && !초기화(칸주인[찾음], Pokreni)) return;
        int TYPE_VALUE = 형종류(oblik_VALUE), VALUE = 0;
        if (Naredba == 179 || Naredba == 181) VALUE = 빼기(TYPE_VALUE);
        if (정적) { if (Naredba == 178) 넣기(칸값[찾음], TYPE_VALUE); else if (!GREŠKA) 칸값[찾음] = VALUE; return; }
        int objekt_Reference = 빼기(2);
        if (!객체유효(objekt_Reference)) return;
        if (힙[objekt_Reference] < 32 || !종포함(힙[objekt_Reference] - 32, vlasnik_VALUE)) { kvar_VALUE("field receiver type mismatch"); return; }
        int 보관칸 = objekt_Reference + 2 + 칸위치[찾음];
        if (Naredba == 180) 넣기(힙[보관칸], TYPE_VALUE);
        else if (!GREŠKA) { 힙[보관칸] = VALUE; 힙참조[보관칸] = TYPE_VALUE == 2 ? 1 : 0; }
    }
    static boolean 종포함(int poduka_definicija, int Ime) {
        for (int 중첩깊이 = 0; poduka_definicija >= 0 && 중첩깊이 < 16; 중첩깊이++, poduka_definicija = roditeljski_poduka(poduka_definicija)) {
            if (같은말(poduka_definicija_naziv[poduka_definicija], Ime) || (poduka_definicija_roditeljski[poduka_definicija] != 0 && 같은말(poduka_definicija_roditeljski[poduka_definicija], Ime))) return true;
            for (int unutarnji_položaj = 0; unutarnji_položaj < poduka_sučelje_COUNT[poduka_definicija]; unutarnji_položaj++) if (같은말(poduka_sučelje[poduka_definicija * 16 + unutarnji_položaj], Ime)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int bajt_podaci, boolean PUTANJA) {
        if (첫값 == bajt_podaci) return true;
        if (첫값 <= 0 || bajt_podaci <= 0 || 힙[첫값] != 1 || 힙[bajt_podaci] != 1 || 힙[첫값 + 1] != 힙[bajt_podaci + 1]) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) {
            int koordinata_x = 힙[첫값 + 2 + Loop_INDEX], 세로좌표 = 힙[bajt_podaci + 2 + Loop_INDEX];
            if (PUTANJA) { if (koordinata_x == '.') koordinata_x = '/'; if (세로좌표 == '.') 세로좌표 = '/'; }
            if (koordinata_x != 세로좌표) return false;
        }
        return true;
    }
    static boolean 객체유효(int objekt_Reference) {
        if (objekt_Reference == 0) { kvar_VALUE("NullPointerException"); return false; }
        if (objekt_Reference < 1 || objekt_Reference >= 힙끝 || 힙폭[objekt_Reference] < 2 || 힙[objekt_Reference] == 0) { kvar_VALUE("invalid object reference"); return false; }
        return true;
    }
    static void zaštititi_VALUE(int objekt_Reference) {
        if (objekt_Reference > 0 && objekt_Reference < 힙끝 && 힙폭[objekt_Reference] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = objekt_Reference;
    }
    static void emisija_VALUE(int objekt_Reference) {
        if (objekt_Reference > 0 && objekt_Reference < 힙끝 && 힙폭[objekt_Reference] >= 2 && 힙[objekt_Reference] != 0 && 힙표시[objekt_Reference] == 0) {
            힙표시[objekt_Reference] = 1; 표시대기[zaslon_COUNT++] = objekt_Reference;
        }
    }
    static void 수거() {
        zaslon_COUNT = 0; Zbirka_COUNT++;
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) 힙표시[검사자리] = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < niz_Reference.length; Loop_INDEX++) emisija_VALUE(niz_Reference[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 칸수; Loop_INDEX++) if ((칸권한[Loop_INDEX] & 8) != 0 && 형종류(칸형[Loop_INDEX]) == 2) emisija_VALUE(칸값[Loop_INDEX]);
        for (int 임시값 = 0; 임시값 < nit_COUNT; 임시값++) {
            emisija_VALUE(nit_objekt[임시값]); emisija_VALUE(nit_cilj[임시값]);
            int 꼭대기자리 = 임시값 == redovno_nit ? kadar_INDEX : nit_kadar[임시값];
            for (int Datoteka_INDEX = 임시값 * 32; Datoteka_INDEX <= 꼭대기자리; Datoteka_INDEX++) {
                for (int unutarnji_položaj = 0; unutarnji_položaj < 함수지역[kadar_postupak[Datoteka_INDEX]]; unutarnji_položaj++) if (lokalno_TYPE[Datoteka_INDEX * 128 + unutarnji_položaj] == 2) emisija_VALUE(lokalno_VALUE[Datoteka_INDEX * 128 + unutarnji_položaj]);
                for (int unutarnji_položaj = 0; unutarnji_položaj < kadar_hrpa[Datoteka_INDEX]; unutarnji_položaj++) if (operand_hrpa_TYPE[Datoteka_INDEX * 128 + unutarnji_položaj] == 2) emisija_VALUE(operand_hrpa_VALUE[Datoteka_INDEX * 128 + unutarnji_položaj]);
            }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 화면참조.length; Loop_INDEX++) emisija_VALUE(화면참조[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 나중수; Loop_INDEX++) emisija_VALUE(나중실행[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Store_cijeli_broj.length; Loop_INDEX++) emisija_VALUE(Store_cijeli_broj[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < poduka_definicija_COUNT; Loop_INDEX++) emisija_VALUE(poduka_zaključati[Loop_INDEX]);
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (잠금깊이[검사자리] > 0) emisija_VALUE(검사자리);
        emisija_VALUE(던진객체);
        for (int Loop_INDEX = 0; Loop_INDEX < 잠시수; Loop_INDEX++) emisija_VALUE(잠시참조[Loop_INDEX]);
        while (zaslon_COUNT > 0) {
            int objekt_Reference = 표시대기[--zaslon_COUNT], područje_kod = 힙[objekt_Reference];
            for (int Loop_INDEX = objekt_Reference + 2; Loop_INDEX < objekt_Reference + 힙폭[objekt_Reference]; Loop_INDEX++) if (područje_kod == 3 || područje_kod == 4 || 힙참조[Loop_INDEX] != 0) emisija_VALUE(힙[Loop_INDEX]);
        }
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙표시[검사자리] == 0) 힙[검사자리] = 0;
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙[검사자리] == 0) {
            while (검사자리 + 힙폭[검사자리] < 힙끝 && 힙[검사자리 + 힙폭[검사자리]] == 0) { int Dalje_položaj = 검사자리 + 힙폭[검사자리]; 힙폭[검사자리] += 힙폭[Dalje_položaj]; 힙폭[Dalje_položaj] = 0; }
            if (검사자리 + 힙폭[검사자리] == 힙끝) { 힙끝 = 검사자리; break; }
        }
    }
    static int 새기억(int 종류, int 길이) {
        if (길이 < 0) { kvar_VALUE("NegativeArraySizeException"); return 0; }
        if (길이 > 힙.length - 3) { kvar_VALUE("object heap exhausted"); return 0; }
        int 필요수 = 길이 + 2, objekt_Reference = 0;
        if (필요수 <= 힙.length - 힙끝) { objekt_Reference = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { objekt_Reference = 읽는자리; break; }
            if (objekt_Reference != 0) {
                int 남은길이 = 힙폭[objekt_Reference] - 필요수;
                if (남은길이 >= 2) { 힙폭[objekt_Reference + 필요수] = 남은길이; 힙[objekt_Reference + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { objekt_Reference = 힙끝; 힙끝 += 필요수; }
        }
        if (objekt_Reference == 0) { kvar_VALUE("object heap exhausted"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < 필요수; Loop_INDEX++) { 힙[objekt_Reference + Loop_INDEX] = 0; 힙참조[objekt_Reference + Loop_INDEX] = 0; 힙폭[objekt_Reference + Loop_INDEX] = 0; }
        element_polja[objekt_Reference] = 0;
        힙폭[objekt_Reference] = 필요수; 힙[objekt_Reference] = 종류; 힙[objekt_Reference + 1] = 길이; zaštititi_VALUE(objekt_Reference); return objekt_Reference;
    }
    static int iznimka_poduka(String naziv_konstanta) {
        if (자바도구.같음(naziv_konstanta, "java/lang/Throwable")) return 1;
        if (자바도구.같음(naziv_konstanta, "java/lang/Exception")) return 2;
        if (자바도구.같음(naziv_konstanta, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(naziv_konstanta, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(naziv_konstanta, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(naziv_konstanta, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(naziv_konstanta, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(naziv_konstanta, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(naziv_konstanta, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(naziv_konstanta, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(naziv_konstanta, "java/io/IOException")) return 11;
        if (자바도구.같음(naziv_konstanta, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(naziv_konstanta, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(naziv_konstanta, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(naziv_konstanta, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int iznimka_konstanta(int Ime) {
        for (int Loop_INDEX = 1; Loop_INDEX <= 41; Loop_INDEX++) if (Word_SMS(Ime, iznimka_naziv(Loop_INDEX))) return Loop_INDEX;
        return 0;
    }
    static String iznimka_naziv(int račun_VALUE) {
        if (račun_VALUE == 40) return "java/lang/InterruptedException";
        if (račun_VALUE == 41) return "hrvatski/vlastiti/대기중단예외";
        if (račun_VALUE == 39) return "java/net/SocketException";
        if (račun_VALUE == 20) return "hrvatski/vlastiti/iznimka";
        if (račun_VALUE == 21) return "hrvatski/vlastiti/실행예외";
        if (račun_VALUE == 22) return "hrvatski/vlastiti/U_I_iznimka";
        if (račun_VALUE == 23) return "hrvatski/vlastiti/čekaj_TIMEOUT_iznimka";
        if (račun_VALUE == 24) return "hrvatski/vlastiti/adresa_LOOKUP_iznimka";
        if (račun_VALUE == 25) return "hrvatski/vlastiti/파일없음예외";
        if (račun_VALUE == 26) return "hrvatski/vlastiti/통신예외";
        if (račun_VALUE == 27) return "hrvatski/vlastiti/nevaljan_argument_iznimka";
        if (račun_VALUE == 28) return "hrvatski/vlastiti/숫자형식예외";
        if (račun_VALUE == 29) return "hrvatski/vlastiti/범위예외";
        if (račun_VALUE == 30) return "hrvatski/vlastiti/배열범위예외";
        if (račun_VALUE == 31) return "hrvatski/vlastiti/문자열범위예외";
        if (račun_VALUE == 32) return "hrvatski/vlastiti/NULL_Reference_iznimka";
        if (račun_VALUE == 33) return "hrvatski/vlastiti/산술예외";
        if (račun_VALUE == 34) return "hrvatski/vlastiti/Stanje_iznimka";
        if (račun_VALUE == 35) return "hrvatski/vlastiti/TYPE_emitirati_iznimka";
        if (račun_VALUE == 36) return "hrvatski/vlastiti/음수배열크기예외";
        if (račun_VALUE == 37) return "hrvatski/vlastiti/ARRAY_Store_kvar";
        if (račun_VALUE == 38) return "hrvatski/vlastiti/nit_Stanje_iznimka";
        if (račun_VALUE == 1) return "java/lang/Throwable"; if (račun_VALUE == 2) return "java/lang/Exception";
        if (račun_VALUE == 3) return "java/lang/RuntimeException"; if (račun_VALUE == 4) return "java/lang/ArithmeticException";
        if (račun_VALUE == 5) return "java/lang/NullPointerException"; if (račun_VALUE == 6) return "java/lang/IndexOutOfBoundsException";
        if (račun_VALUE == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (račun_VALUE == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (račun_VALUE == 9) return "java/lang/IllegalArgumentException"; if (račun_VALUE == 10) return "java/lang/NumberFormatException";
        if (račun_VALUE == 11) return "java/io/IOException"; if (račun_VALUE == 12) return "java/io/FileNotFoundException";
        if (račun_VALUE == 17) return "java/lang/ArrayStoreException";
        if (račun_VALUE == 18) return "java/net/UnknownHostException";
        if (račun_VALUE == 19) return "java/net/SocketTimeoutException";
        if (račun_VALUE == 16) return "java/lang/IllegalThreadStateException";
        if (račun_VALUE == 13) return "java/lang/IllegalStateException"; if (račun_VALUE == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int iznimka_roditeljski(int račun_VALUE) {
        if (račun_VALUE == 40) return 2;
        if (račun_VALUE == 41) return 40;
        if (račun_VALUE == 39) return 11;
        if (račun_VALUE == 1) return 0;
        if (račun_VALUE == 2) return 1;
        if (račun_VALUE == 3) return 2;
        if (račun_VALUE == 4) return 3;
        if (račun_VALUE == 5) return 3;
        if (račun_VALUE == 6) return 3;
        if (račun_VALUE == 7) return 6;
        if (račun_VALUE == 8) return 6;
        if (račun_VALUE == 9) return 3;
        if (račun_VALUE == 10) return 9;
        if (račun_VALUE == 11) return 2;
        if (račun_VALUE == 12) return 11;
        if (račun_VALUE == 13) return 3;
        if (račun_VALUE == 14) return 3;
        if (račun_VALUE == 15) return 3;
        if (račun_VALUE == 16) return 9;
        if (račun_VALUE == 17) return 3;
        if (račun_VALUE == 18) return 11;
        if (račun_VALUE == 19) return 11;
        if (račun_VALUE == 20) return 2;
        if (račun_VALUE == 21) return 3;
        if (račun_VALUE == 22) return 11;
        if (račun_VALUE == 23) return 22;
        if (račun_VALUE == 24) return 22;
        if (račun_VALUE == 25) return 22;
        if (račun_VALUE == 26) return 22;
        if (račun_VALUE == 27) return 9;
        if (račun_VALUE == 28) return 27;
        if (račun_VALUE == 29) return 6;
        if (račun_VALUE == 30) return 29;
        if (račun_VALUE == 31) return 29;
        if (račun_VALUE == 32) return 5;
        if (račun_VALUE == 33) return 4;
        if (račun_VALUE == 34) return 13;
        if (račun_VALUE == 35) return 14;
        if (račun_VALUE == 36) return 15;
        if (račun_VALUE == 37) return 17;
        if (račun_VALUE == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int stvarna_vrijednost, int 요구값) {
        for (int 깊이 = 0; stvarna_vrijednost != 0 && 깊이 < 16; 깊이++, stvarna_vrijednost = iznimka_roditeljski(stvarna_vrijednost))
            if (stvarna_vrijednost == 요구값) return true;
        return false;
    }
    static void 예외던짐(int račun_VALUE, String 안내참조) {
        int objekt_Reference = 새기억(9, 2); if (GREŠKA) return;
        힙[objekt_Reference + 2] = račun_VALUE; 힙[objekt_Reference + 3] = domaćin_znak(안내참조); 힙참조[objekt_Reference + 3] = 1;
        던진객체 = objekt_Reference; GREŠKA = true;
    }
    static boolean 맞는객체(int objekt_Reference, int Ime) {
        if (objekt_Reference == 0) return true;
        if (!객체유효(objekt_Reference)) return false;
        int područje_kod = 힙[objekt_Reference];
        if (Word_SMS(Ime, "java/lang/Object")) return true;
        if (područje_kod >= 32) return 종포함(područje_kod - 32, Ime);
        if (područje_kod == 9) { int cilj_adresa = iznimka_konstanta(Ime); return cilj_adresa != 0 && 예외포함(힙[objekt_Reference + 2], cilj_adresa); }
        if (područje_kod == 1) return Word_SMS(Ime, "java/lang/String") || Word_SMS(Ime, "java/lang/CharSequence");
        if (područje_kod == 4) return Word_SMS(Ime, "java/lang/StringBuilder") || Word_SMS(Ime, "java/lang/CharSequence");
        if (područje_kod == 10) return Word_SMS(Ime, "java/util/ArrayList") || Word_SMS(Ime, "java/util/List");
        if (područje_kod == 11) return Word_SMS(Ime, "java/util/HashMap") || Word_SMS(Ime, "java/util/Map");
        if (područje_kod == 12) return Word_SMS(Ime, "java/lang/Integer") || Word_SMS(Ime, "java/lang/Number");
        if (područje_kod >= 24 && područje_kod <= 28 && 힙[objekt_Reference + 13] != 0) return 한국어화면종(Ime) == područje_kod || Word_SMS(Ime, "hrvatski/vlastiti/화면구성요소");
        if (područje_kod >= 24 && područje_kod <= 28) return (한국어화면종(Ime) == 0 && 화면종(Ime) == područje_kod) || Word_SMS(Ime, "java/awt/Component") || Word_SMS(Ime, "java/awt/Container") || Word_SMS(Ime, "javax/swing/JComponent");
        if (područje_kod == 29) return Word_SMS(Ime, 힙[objekt_Reference + 3] != 0 ? "hrvatski/vlastiti/akcija_obavijest" : "java/awt/event/ActionEvent");
        if (područje_kod == 30) return Word_SMS(Ime, "java/awt/FlowLayout") || Word_SMS(Ime, "java/awt/LayoutManager");
        if (područje_kod == 17) return Word_SMS(Ime, "java/net/Socket");
        if (područje_kod == 18) return Word_SMS(Ime, "java/net/ServerSocket");
        if (područje_kod == 19) return Word_SMS(Ime, 힙[objekt_Reference + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (područje_kod == 14) return Word_SMS(Ime, "java/net/InetAddress");
        if (područje_kod == 15) return Word_SMS(Ime, "java/net/DatagramSocket");
        if (područje_kod == 16) return Word_SMS(Ime, "java/net/DatagramPacket");
        if (područje_kod == 13) return Word_SMS(Ime, 힙[objekt_Reference + 3] != 0 ? "hrvatski/vlastiti/작업가닥" : "java/lang/Thread");
        if (područje_kod == 2) return Word_SMS(Ime, "[I"); if (područje_kod == 20) return Word_SMS(Ime, "[B"); if (područje_kod == 21) return Word_SMS(Ime, "[Z");
        if (područje_kod == 22) return Word_SMS(Ime, "[C"); if (područje_kod == 23) return Word_SMS(Ime, "[S");
        if (područje_kod != 3) return false;
        if (Word_SMS(Ime, "[Ljava/lang/Object;")) return true;
        int komponenta = element_polja[objekt_Reference];
        if (komponenta == -1) return Word_SMS(Ime, "[Ljava/lang/String;") || Word_SMS(Ime, "[Ljava/lang/CharSequence;");
        if (komponenta == 0) return false;
        if (배열종비교(komponenta, Ime)) return true;
        if ((Word_SMS(komponenta, "java/lang/String") || Word_SMS(komponenta, "java/lang/StringBuilder")) && Word_SMS(Ime, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDEX = 0; Loop_INDEX < poduka_definicija_COUNT; Loop_INDEX++) if (같은말(poduka_definicija_naziv[Loop_INDEX], komponenta)) {
            for (int kodna_točka = Loop_INDEX, 중첩깊이 = 0; kodna_točka >= 0 && 중첩깊이 < 16; 중첩깊이++, kodna_točka = roditeljski_poduka(kodna_točka)) {
                if (배열종비교(poduka_definicija_roditeljski[kodna_točka], Ime)) return true;
                for (int unutarnji_položaj = 0; unutarnji_položaj < poduka_sučelje_COUNT[kodna_točka]; unutarnji_položaj++) if (배열종비교(poduka_sučelje[kodna_točka * 16 + unutarnji_položaj], Ime)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int naziv_konstanta, int 형식참조) {
        int 검사자리 = 상가[형식참조], unos_COUNT = konstanta_SECOND_VALUE[형식참조];
        if (naziv_konstanta == 0 || unos_COUNT < 4 || Datoteka[검사자리] != '[' || Datoteka[검사자리 + 1] != 'L' || Datoteka[검사자리 + unos_COUNT - 1] != ';' || konstanta_SECOND_VALUE[naziv_konstanta] != unos_COUNT - 3) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < unos_COUNT - 3; Loop_INDEX++) if (Datoteka[상가[naziv_konstanta] + Loop_INDEX] != Datoteka[검사자리 + 2 + Loop_INDEX]) return false;
        return true;
    }
    static void ustroj_iznimka() {
        if (던진객체 == 0) return;
        GREŠKA = false;
        while (kadar_INDEX >= redovno_nit * 32) {
            int Datoteka_INDEX = kadar_postupak[kadar_INDEX], 읽는자리 = 틀명령[kadar_INDEX];
            for (int Loop_INDEX = 0; Loop_INDEX < 잡기수; Loop_INDEX++) if (잡기함수[Loop_INDEX] == Datoteka_INDEX && 읽는자리 >= 잡기시작[Loop_INDEX] && 읽는자리 < 잡기끝[Loop_INDEX]
                && (잡기종[Loop_INDEX] == 0 || 맞는객체(던진객체, 잡기종[Loop_INDEX]))) {
                kadar_položaj[kadar_INDEX] = 잡기위치[Loop_INDEX]; kadar_hrpa[kadar_INDEX] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (틀초기화[kadar_INDEX] != 0) poduka_definicija_Stanje[틀초기화[kadar_INDEX] - 1] = 3;
            if (kadar_zaključati[kadar_INDEX] != 0) { izdati_zaključati(kadar_zaključati[kadar_INDEX]); kadar_zaključati[kadar_INDEX] = 0; }
            kadar_INDEX--;
        }
        korisnik.Zapisuj("Uncaught ");
        if (힙[던진객체] == 9) { korisnik.Zapisuj(iznimka_naziv(힙[던진객체 + 2])); korisnik.Zapisuj(": "); zapisivanje_SMS(힙[던진객체 + 3]); }
        else korisnik.Zapisuj("user exception");
        korisnik.zapisivanje_znak_VALUE(10); 던진객체 = 0; GREŠKA = true;
    }
    // 이 JVM의 operand_hrpa 항목은 redovno_artikl category-1(int/reference)만 허용한다.
    static void 스택명령(int naredba_kod) {
        int 첫값 = 빼기(0), 첫형식 = vratiti_TYPE;
        if (naredba_kod == 87) return;
        if (naredba_kod == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int bajt_podaci = 빼기(0), SECOND_oblik = vratiti_TYPE;
        if (naredba_kod == 88) return;
        if (naredba_kod == 90) { 넣기(첫값, 첫형식); 넣기(bajt_podaci, SECOND_oblik); 넣기(첫값, 첫형식); return; }
        if (naredba_kod == 92) { 넣기(bajt_podaci, SECOND_oblik); 넣기(첫값, 첫형식); 넣기(bajt_podaci, SECOND_oblik); 넣기(첫값, 첫형식); return; }
        if (naredba_kod == 95) { 넣기(첫값, 첫형식); 넣기(bajt_podaci, SECOND_oblik); return; }
        int kodna_točka = 빼기(0), 셋째형식 = vratiti_TYPE;
        if (naredba_kod == 91) { 넣기(첫값, 첫형식); 넣기(kodna_točka, 셋째형식); 넣기(bajt_podaci, SECOND_oblik); 넣기(첫값, 첫형식); return; }
        if (naredba_kod == 93) { 넣기(bajt_podaci, SECOND_oblik); 넣기(첫값, 첫형식); 넣기(kodna_točka, 셋째형식); 넣기(bajt_podaci, SECOND_oblik); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = vratiti_TYPE;
        넣기(bajt_podaci, SECOND_oblik); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(kodna_točka, 셋째형식); 넣기(bajt_podaci, SECOND_oblik); 넣기(첫값, 첫형식);
    }
    static void 새객체(int naziv_konstanta, int 시작점) {
        int područje_kod = 0, 유효길이 = 0, iznimka_Reference = iznimka_konstanta(naziv_konstanta);
        if (Word_SMS(naziv_konstanta, "java/lang/StringBuilder")) { područje_kod = 4; 유효길이 = 1; }
        if (Word_SMS(naziv_konstanta, "java/io/FileInputStream")) { područje_kod = 5; 유효길이 = 2; }
        if (Word_SMS(naziv_konstanta, "java/io/FileOutputStream")) { područje_kod = 6; 유효길이 = 2; }
        if (iznimka_Reference != 0) { područje_kod = 9; 유효길이 = 2; }
        if (Word_SMS(naziv_konstanta, "java/util/ArrayList")) { područje_kod = 10; 유효길이 = 2; }
        if (Word_SMS(naziv_konstanta, "java/util/HashMap")) { područje_kod = 11; 유효길이 = 2; }
        if (Word_SMS(naziv_konstanta, "java/lang/Integer")) { područje_kod = 12; 유효길이 = 1; }
        if (Word_SMS(naziv_konstanta, "java/net/Socket")) { područje_kod = 17; 유효길이 = 5; }
        if (Word_SMS(naziv_konstanta, "java/net/ServerSocket")) { područje_kod = 18; 유효길이 = 5; }
        if (Word_SMS(naziv_konstanta, "java/net/DatagramSocket")) { područje_kod = 15; 유효길이 = 3; }
        if (Word_SMS(naziv_konstanta, "java/net/DatagramPacket")) { područje_kod = 16; 유효길이 = 4; }
        if (Word_SMS(naziv_konstanta, "java/lang/Thread") || Word_SMS(naziv_konstanta, "hrvatski/vlastiti/작업가닥")) { područje_kod = 13; 유효길이 = 2; }
        if (Word_SMS(naziv_konstanta, "java/lang/Object")) { područje_kod = 8; }
        if (područje_kod == 0 && 화면종(naziv_konstanta) != 0) { područje_kod = 화면종(naziv_konstanta); 유효길이 = 12; }
        if (područje_kod == 0) {
            int kodna_točka = FIND_poduka_definicija(naziv_konstanta); if (kodna_točka < 0 || GREŠKA || !초기화(kodna_točka, 시작점)) return;
            područje_kod = 32 + kodna_točka; 유효길이 = 종칸수[kodna_točka];
        }
        int objekt_Reference = dodijeli_Pohrana(područje_kod, 유효길이); if (GREŠKA) return;
        if (područje_kod == 13 && Word_SMS(naziv_konstanta, "hrvatski/vlastiti/작업가닥")) 힙[objekt_Reference + 3] = 1;
        if (područje_kod >= 24 && područje_kod <= 28 && 한국어화면종(naziv_konstanta) != 0) 힙[objekt_Reference + 13] = 1;
        if (područje_kod == 5 || područje_kod == 6 || područje_kod == 15 || područje_kod == 17 || područje_kod == 18) 힙[objekt_Reference + 2] = -1;
        if (područje_kod == 9) 힙[objekt_Reference + 2] = iznimka_Reference;
        넣기(objekt_Reference, 2);
    }
    static boolean 값같음(int 첫값, int bajt_podaci) {
        if (첫값 == bajt_podaci) return true;
        if (첫값 == 0 || bajt_podaci == 0 || 첫값 < 0 || bajt_podaci < 0 || 첫값 >= 힙끝 || bajt_podaci >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[bajt_podaci] == 1) return 글같음(첫값, bajt_podaci, false);
        return 힙[첫값] == 12 && 힙[bajt_podaci] == 12 && 힙[첫값 + 2] == 힙[bajt_podaci + 2];
    }
    static int SMS_fragment(int objekt_Reference, int START_položaj, int završiti_razgovor_položaj) {
        if (!objekt_VALUE(objekt_Reference, 1)) return 0;
        if (START_položaj < 0 || završiti_razgovor_položaj < START_položaj || završiti_razgovor_položaj > 힙[objekt_Reference + 1]) { kvar_VALUE("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = dodijeli_Pohrana(1, završiti_razgovor_položaj - START_položaj); if (GREŠKA) return 0;
        for (int Loop_INDEX = START_položaj; Loop_INDEX < završiti_razgovor_položaj; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX - START_položaj] = 힙[objekt_Reference + 2 + Loop_INDEX];
        return 반환값;
    }
    static int spojiti_SMS(int 첫값, int bajt_podaci) {
        if (!objekt_VALUE(첫값, 1) || !objekt_VALUE(bajt_podaci, 1)) return 0;
        int unos_COUNT = 힙[첫값 + 1], postupak_INDEX = 힙[bajt_podaci + 1], 반환값 = dodijeli_Pohrana(1, unos_COUNT + postupak_INDEX); if (GREŠKA) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < unos_COUNT; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 힙[첫값 + 2 + Loop_INDEX];
        for (int Loop_INDEX = 0; Loop_INDEX < postupak_INDEX; Loop_INDEX++) 힙[반환값 + 2 + unos_COUNT + Loop_INDEX] = 힙[bajt_podaci + 2 + Loop_INDEX];
        return 반환값;
    }
    static boolean 기본호출(int vlasnik, int naziv_konstanta, int 서술상수, int naredba_kod) {
        if (Word_SMS(vlasnik, "hrvatski/vlastiti/실행인수") && naredba_kod == 184) {
            if (Word_SMS(naziv_konstanta, "artikl_COUNT") && Word_SMS(서술상수, "()I")) { 넣기(korisnik.인수개수() - 1, 1); return true; }
            if (Word_SMS(naziv_konstanta, "Tekst") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= korisnik.인수개수() - 1) 예외던짐(29, "Izvrši_naredba Argumenti 범위를 벗어났습니다");
                else 넣기(domaćin_znak(korisnik.Argumenti(순번 + 1)), 2);
                return true;
            }
            kvar_VALUE("지원하지 않는 hrvatski Izvrši_naredba Argumenti 호출"); return true;
        }
        if (Word_SMS(vlasnik, "hrvatski/vlastiti/작업가닥")) { Proces_nit(naziv_konstanta, 서술상수, naredba_kod, true); return true; }
        if (한국어화면소유(vlasnik)) { 한국어화면호출(vlasnik, naziv_konstanta, 서술상수, naredba_kod); return true; }
        if (화면소유(vlasnik)) { 화면호출(vlasnik, naziv_konstanta, 서술상수, naredba_kod); return true; }
        if (Word_SMS(vlasnik, "java/net/Socket") || Word_SMS(vlasnik, "java/net/ServerSocket") || Word_SMS(vlasnik, "java/io/InputStream") || Word_SMS(vlasnik, "java/io/OutputStream")) { 흐름호출(vlasnik, naziv_konstanta, 서술상수, naredba_kod); return true; }
        if (Word_SMS(vlasnik, "hrvatski/vlastiti/jezgra_sustava_VALUE") && naredba_kod == 184) {
            if (Word_SMS(naziv_konstanta, "화면너비") && Word_SMS(서술상수, "()I")) { 넣기(korisnik.화면너비(), 1); return true; }
            if (Word_SMS(naziv_konstanta, "화면높이") && Word_SMS(서술상수, "()I")) { 넣기(korisnik.화면높이(), 1); return true; }
            if (Word_SMS(naziv_konstanta, "밀리초") && Word_SMS(서술상수, "()I")) { 넣기(korisnik.밀리초(), 1); return true; }
            if (Word_SMS(naziv_konstanta, "그림대기") && Word_SMS(서술상수, "()I")) { 넣기(korisnik.그림대기(), 1); return true; }
            if (Word_SMS(naziv_konstanta, "pravokutnik") && Word_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), koordinata_x = 빼기(1); 넣기(korisnik.pravokutnik(koordinata_x, 세로좌표, 너비, 높이, 색상), 1); return true; }
        }
        if (Word_SMS(vlasnik, "java/net/InetAddress") || Word_SMS(vlasnik, "java/net/DatagramPacket") || Word_SMS(vlasnik, "java/net/DatagramSocket")) { 통신호출(vlasnik, naziv_konstanta, 서술상수, naredba_kod); return true; }
        if (Word_SMS(vlasnik, "java/lang/Thread")) { 가닥호출(naziv_konstanta, 서술상수, naredba_kod); return true; }
        if (Word_SMS(vlasnik, "java/lang/Object")) {
            if (Word_SMS(naziv_konstanta, "<init>") && Word_SMS(서술상수, "()V") && naredba_kod == 183) { 객체유효(빼기(2)); return true; }
            if (Word_SMS(naziv_konstanta, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int bajt_podaci = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == bajt_podaci ? 1 : 0, 1); return true; }
        }
        if (iznimka_konstanta(vlasnik) != 0) {
            if (Word_SMS(naziv_konstanta, "<init>") && naredba_kod == 183 && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int upit = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), objekt_Reference = 빼기(2);
                if (objekt_VALUE(objekt_Reference, 9)) { 힙[objekt_Reference + 3] = upit; 힙참조[objekt_Reference + 3] = 1; } return true;
            }
            if ((Word_SMS(naziv_konstanta, "getMessage") || Word_SMS(naziv_konstanta, "설명")) && Word_SMS(서술상수, "()Ljava/lang/String;")) { int objekt_Reference = 빼기(2); if (objekt_VALUE(objekt_Reference, 9)) 넣기(힙[objekt_Reference + 3], 2); return true; }
        }
        if (Word_SMS(vlasnik, "java/lang/String")) {
            if (naredba_kod == 182 && Word_SMS(naziv_konstanta, "getBytes") && (Word_SMS(서술상수, "()[B") || Word_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int šifriranje_naziv = Word_SMS(서술상수, "()[B") ? 0 : 빼기(2), objekt_Reference = 빼기(2);
                if (!objekt_VALUE(objekt_Reference, 1)) return true;
                if (šifriranje_naziv != 0 && !글같음(šifriranje_naziv, domaćin_znak("UTF-8"), false) && !글같음(šifriranje_naziv, domaćin_znak("UTF8"), false) && !글같음(šifriranje_naziv, domaćin_znak("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int unos_COUNT = 힙[objekt_Reference + 1], 반환값 = dodijeli_Pohrana(20, unos_COUNT * 3), 사용수 = 0; if (GREŠKA) return true;
                for (int unutarnji_položaj = 0; unutarnji_položaj < unos_COUNT; unutarnji_položaj++) {
                    int kodna_točka = 힙[objekt_Reference + 2 + unutarnji_položaj];
                    if (kodna_točka >= 0xd800 && kodna_točka <= 0xdbff && unutarnji_položaj + 1 < unos_COUNT && 힙[objekt_Reference + 3 + unutarnji_položaj] >= 0xdc00 && 힙[objekt_Reference + 3 + unutarnji_položaj] <= 0xdfff) kodna_točka = 0x10000 + ((kodna_točka - 0xd800) << 10) + 힙[objekt_Reference + 2 + ++unutarnji_položaj] - 0xdc00;
                    else if (kodna_točka >= 0xd800 && kodna_točka <= 0xdfff) kodna_točka = '?';
                    if (kodna_točka < 128) 힙[반환값 + 2 + 사용수++] = kodna_točka;
                    else { int bajt_COUNT = kodna_točka < 2048 ? 2 : kodna_točka < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((bajt_COUNT == 2 ? 192 : bajt_COUNT == 3 ? 224 : 240) | kodna_točka >> (6 * (bajt_COUNT - 1))); for (int Usporedba_položaj = bajt_COUNT - 1; Usporedba_položaj > 0; Usporedba_položaj--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | kodna_točka >> (6 * (Usporedba_položaj - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (naredba_kod == 184 && Word_SMS(naziv_konstanta, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(znamenka_znak(빼기(1)), 2); return true; }
            if (naredba_kod != 182) return false;
            if (Word_SMS(naziv_konstanta, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int bajt_podaci = 빼기(2), 첫값 = 빼기(2); if (objekt_VALUE(첫값, 1)) 넣기(글같음(첫값, bajt_podaci, false) ? 1 : 0, 1); return true; }
            if (Word_SMS(naziv_konstanta, "isEmpty") && Word_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (objekt_VALUE(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_SMS(naziv_konstanta, "substring") && (Word_SMS(서술상수, "(I)Ljava/lang/String;") || Word_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SECOND_VALUE = Word_SMS(서술상수, "(II)Ljava/lang/String;"); int završiti_razgovor_položaj = SECOND_VALUE ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (objekt_VALUE(첫값, 1)) 넣기(SMS_fragment(첫값, 시작점, SECOND_VALUE ? završiti_razgovor_položaj : 힙[첫값 + 1]), 2); return true;
            }
            if (Word_SMS(naziv_konstanta, "concat") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int bajt_podaci = 빼기(2), 첫값 = 빼기(2); 넣기(spojiti_SMS(첫값, bajt_podaci), 2); return true; }
            if (Word_SMS(naziv_konstanta, "hashCode") && Word_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), raspršivanje_VALUE = 0; if (objekt_VALUE(첫값, 1)) { for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) raspršivanje_VALUE = raspršivanje_VALUE * 31 + 힙[첫값 + 2 + Loop_INDEX]; 넣기(raspršivanje_VALUE, 1); } return true; }
            if (Word_SMS(naziv_konstanta, "toString") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (objekt_VALUE(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_SMS(vlasnik, "java/lang/Integer")) {
            if (naredba_kod == 184 && Word_SMS(naziv_konstanta, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int podaci_VALUE = 빼기(1), objekt_Reference = podaci_VALUE >= -128 && podaci_VALUE <= 127 ? Store_cijeli_broj[podaci_VALUE + 128] : 0; if (objekt_Reference == 0) { objekt_Reference = dodijeli_Pohrana(12, 1); if (!GREŠKA) { 힙[objekt_Reference + 2] = podaci_VALUE; if (podaci_VALUE >= -128 && podaci_VALUE <= 127) Store_cijeli_broj[podaci_VALUE + 128] = objekt_Reference; } } 넣기(objekt_Reference, 2); return true; }
            if (naredba_kod == 183 && Word_SMS(naziv_konstanta, "<init>") && Word_SMS(서술상수, "(I)V")) { int podaci_VALUE = 빼기(1), objekt_Reference = 빼기(2); if (objekt_VALUE(objekt_Reference, 12)) 힙[objekt_Reference + 2] = podaci_VALUE; return true; }
            if (naredba_kod == 182 && Word_SMS(naziv_konstanta, "intValue") && Word_SMS(서술상수, "()I")) { int objekt_Reference = 빼기(2); if (objekt_VALUE(objekt_Reference, 12)) 넣기(힙[objekt_Reference + 2], 1); return true; }
            if (naredba_kod == 184 && Word_SMS(naziv_konstanta, "toString") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(znamenka_znak(빼기(1)), 2); return true; }
        }
        if (Word_SMS(vlasnik, "java/lang/Math") && naredba_kod == 184) {
            if (Word_SMS(naziv_konstanta, "abs") && Word_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_SMS(naziv_konstanta, "min") || Word_SMS(naziv_konstanta, "max")) && Word_SMS(서술상수, "(II)I")) { int bajt_podaci = 빼기(1), 첫값 = 빼기(1); 넣기(Word_SMS(naziv_konstanta, "min") ? (첫값 < bajt_podaci ? 첫값 : bajt_podaci) : (첫값 > bajt_podaci ? 첫값 : bajt_podaci), 1); return true; }
        }
        if (Word_SMS(vlasnik, "java/lang/System") && naredba_kod == 184) {
            if (Word_SMS(naziv_konstanta, "gc") && Word_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Word_SMS(naziv_konstanta, "arraycopy") && Word_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int unos_COUNT = 빼기(1), odredište_VALUE_INDEX = 빼기(1), bajt_podaci = 빼기(2), START_položaj = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(bajt_podaci)) {
                    int područje_kod = 힙[첫값];
                    if (힙[bajt_podaci] != područje_kod || (područje_kod != 2 && područje_kod != 3 && (područje_kod < 20 || područje_kod > 23))) kvar_VALUE("arraycopy type mismatch");
                    else if (unos_COUNT < 0 || START_položaj < 0 || odredište_VALUE_INDEX < 0 || START_položaj > 힙[첫값 + 1] - unos_COUNT || odredište_VALUE_INDEX > 힙[bajt_podaci + 1] - unos_COUNT) kvar_VALUE("ArrayIndexOutOfBoundsException");
                    else if (첫값 == bajt_podaci && odredište_VALUE_INDEX > START_položaj) { for (int Loop_INDEX = unos_COUNT - 1; Loop_INDEX >= 0; Loop_INDEX--) 힙[bajt_podaci + 2 + odredište_VALUE_INDEX + Loop_INDEX] = 힙[첫값 + 2 + START_položaj + Loop_INDEX]; }
                    else { for (int Loop_INDEX = 0; Loop_INDEX < unos_COUNT && !GREŠKA; Loop_INDEX++) { int podaci_VALUE = 힙[첫값 + 2 + START_položaj + Loop_INDEX]; if (područje_kod != 3 || 배열저장가능(bajt_podaci, podaci_VALUE)) 힙[bajt_podaci + 2 + odredište_VALUE_INDEX + Loop_INDEX] = podaci_VALUE; } }
                }
                return true;
            }
        }
        if (Word_SMS(vlasnik, "java/util/ArrayList") || Word_SMS(vlasnik, "java/util/List") || Word_SMS(vlasnik, "java/util/HashMap") || Word_SMS(vlasnik, "java/util/Map")) {
            모음호출(vlasnik, naziv_konstanta, 서술상수, naredba_kod); return true;
        }
        return false;
    }
    static void 모음늘리기(int objekt_Reference, int 필요수) {
        int 이전값 = 힙[objekt_Reference + 2], kapacitet_podaci = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (kapacitet_podaci >= 필요수) return;
        int Dalje_položaj = kapacitet_podaci < 8 ? 8 : kapacitet_podaci * 2; if (Dalje_položaj < 필요수) Dalje_položaj = 필요수;
        int podaci_ARRAY = dodijeli_Pohrana(3, Dalje_položaj); if (GREŠKA) return;
        for (int Loop_INDEX = 0; Loop_INDEX < kapacitet_podaci; Loop_INDEX++) 힙[podaci_ARRAY + 2 + Loop_INDEX] = 힙[이전값 + 2 + Loop_INDEX];
        힙[objekt_Reference + 2] = podaci_ARRAY; 힙참조[objekt_Reference + 2] = 1;
    }
    static void 모음호출(int vlasnik, int naziv_konstanta, int 서술상수, int naredba_kod) {
        boolean 대응참조 = Word_SMS(vlasnik, "java/util/HashMap") || Word_SMS(vlasnik, "java/util/Map"); int područje_kod = 대응참조 ? 11 : 10;
        if (Word_SMS(naziv_konstanta, "<init>") && naredba_kod == 183 && Word_SMS(서술상수, "()V")) { int objekt_Reference = 빼기(2); if (objekt_VALUE(objekt_Reference, područje_kod)) 모음늘리기(objekt_Reference, 8); return; }
        if (naredba_kod != 182 && naredba_kod != 185) { kvar_VALUE("invalid collection invocation"); return; }
        if (Word_SMS(naziv_konstanta, "size") && Word_SMS(서술상수, "()I") || Word_SMS(naziv_konstanta, "isEmpty") && Word_SMS(서술상수, "()Z")) {
            int objekt_Reference = 빼기(2); if (objekt_VALUE(objekt_Reference, područje_kod)) 넣기(Word_SMS(naziv_konstanta, "size") ? 힙[objekt_Reference + 3] : 힙[objekt_Reference + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_SMS(naziv_konstanta, "clear") && Word_SMS(서술상수, "()V")) { int objekt_Reference = 빼기(2); if (objekt_VALUE(objekt_Reference, područje_kod)) { int podaci_ARRAY = 힙[objekt_Reference + 2]; for (int Loop_INDEX = 0; Loop_INDEX < 힙[podaci_ARRAY + 1]; Loop_INDEX++) 힙[podaci_ARRAY + 2 + Loop_INDEX] = 0; 힙[objekt_Reference + 3] = 0; } return; }
        if (!대응참조 && Word_SMS(naziv_konstanta, "add") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int podaci_VALUE = 빼기(2), objekt_Reference = 빼기(2); if (!objekt_VALUE(objekt_Reference, 10)) return;
            int unos_COUNT = 힙[objekt_Reference + 3]; 모음늘리기(objekt_Reference, unos_COUNT + 1); if (!GREŠKA) { 힙[힙[objekt_Reference + 2] + 2 + unos_COUNT] = podaci_VALUE; 힙[objekt_Reference + 3] = unos_COUNT + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_SMS(naziv_konstanta, "get") || Word_SMS(naziv_konstanta, "remove")) && Word_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Word_SMS(naziv_konstanta, "set") && Word_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean odjel_informacijske_tehnologije_dodijeljeno = Word_SMS(naziv_konstanta, "set"); int podaci_VALUE = odjel_informacijske_tehnologije_dodijeljeno ? 빼기(2) : 0, unos_položaj = 빼기(1), objekt_Reference = 빼기(2);
            if (!objekt_VALUE(objekt_Reference, 10)) return;
            int unos_COUNT = 힙[objekt_Reference + 3], podaci_ARRAY = 힙[objekt_Reference + 2];
            if (unos_položaj < 0 || unos_položaj >= unos_COUNT) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[podaci_ARRAY + 2 + unos_položaj];
            if (odjel_informacijske_tehnologije_dodijeljeno) 힙[podaci_ARRAY + 2 + unos_položaj] = podaci_VALUE;
            if (Word_SMS(naziv_konstanta, "remove")) { for (int Loop_INDEX = unos_položaj + 1; Loop_INDEX < unos_COUNT; Loop_INDEX++) 힙[podaci_ARRAY + 1 + Loop_INDEX] = 힙[podaci_ARRAY + 2 + Loop_INDEX]; 힙[podaci_ARRAY + 1 + unos_COUNT] = 0; 힙[objekt_Reference + 3] = unos_COUNT - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Word_SMS(naziv_konstanta, "get") || Word_SMS(naziv_konstanta, "remove")) && Word_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(naziv_konstanta, "put") && Word_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(naziv_konstanta, "containsKey") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_SMS(naziv_konstanta, "put"), ukloniti = Word_SMS(naziv_konstanta, "remove");
            int podaci_VALUE = 넣기여부 ? 빼기(2) : 0, Ključ_Reference = 빼기(2), objekt_Reference = 빼기(2); if (!objekt_VALUE(objekt_Reference, 11)) return;
            int unos_COUNT = 힙[objekt_Reference + 3], podaci_ARRAY = 힙[objekt_Reference + 2], 찾은여부 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < unos_COUNT; Loop_INDEX++) if (값같음(Ključ_Reference, 힙[podaci_ARRAY + 2 + 2 * Loop_INDEX])) { 찾은여부 = Loop_INDEX; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[podaci_ARRAY + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(objekt_Reference, (unos_COUNT + 1) * 2); podaci_ARRAY = 힙[objekt_Reference + 2]; 찾은여부 = unos_COUNT; if (!GREŠKA) 힙[objekt_Reference + 3] = unos_COUNT + 1; }
                if (!GREŠKA) { 힙[podaci_ARRAY + 2 + 2 * 찾은여부] = Ključ_Reference; 힙[podaci_ARRAY + 3 + 2 * 찾은여부] = podaci_VALUE; }
            }
            if (ukloniti && 찾은여부 >= 0) { for (int Loop_INDEX = 찾은여부 + 1; Loop_INDEX < unos_COUNT; Loop_INDEX++) { 힙[podaci_ARRAY + 2 * Loop_INDEX] = 힙[podaci_ARRAY + 2 + 2 * Loop_INDEX]; 힙[podaci_ARRAY + 1 + 2 * Loop_INDEX] = 힙[podaci_ARRAY + 3 + 2 * Loop_INDEX]; } 힙[podaci_ARRAY + 2 * unos_COUNT] = 0; 힙[podaci_ARRAY + 1 + 2 * unos_COUNT] = 0; 힙[objekt_Reference + 3] = unos_COUNT - 1; }
            if (Word_SMS(naziv_konstanta, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        kvar_VALUE("unsupported collection method");
    }
    static boolean 잠금얻기(int objekt_Reference) {
        if (!객체유효(objekt_Reference)) return false;
        if (잠금깊이[objekt_Reference] != 0 && zaključati_vlasnik[objekt_Reference] != redovno_nit + 1) { promijeniti_zahtjev = true; return false; }
        zaključati_vlasnik[objekt_Reference] = redovno_nit + 1; 잠금깊이[objekt_Reference]++; return true;
    }
    static void izdati_zaključati(int objekt_Reference) {
        if (!객체유효(objekt_Reference)) return;
        if (잠금깊이[objekt_Reference] == 0 || zaključati_vlasnik[objekt_Reference] != redovno_nit + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[objekt_Reference] == 0) zaključati_vlasnik[objekt_Reference] = 0;
    }
    static boolean SWITCH_nit() {
        nit_kadar[redovno_nit] = kadar_INDEX;
        if (kadar_INDEX < redovno_nit * 32) nit_Stanje[redovno_nit] = 3;
        for (int Loop_INDEX = 0; Loop_INDEX < nit_COUNT; Loop_INDEX++) if (nit_Stanje[Loop_INDEX] == 2 && nit_Stanje[가닥대기[Loop_INDEX]] == 3) nit_Stanje[Loop_INDEX] = 1;
        for (int Loop_INDEX = 1; Loop_INDEX <= nit_COUNT; Loop_INDEX++) {
            int Dalje_položaj = (redovno_nit + Loop_INDEX) % nit_COUNT;
            if (nit_Stanje[Dalje_položaj] == 1) { redovno_nit = Dalje_položaj; kadar_INDEX = nit_kadar[Dalje_položaj]; promijeniti_zahtjev = false; return true; }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < nit_COUNT; Loop_INDEX++) if (nit_Stanje[Loop_INDEX] != 3) { kvar_VALUE("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int naziv_konstanta, int 서술상수, int naredba_kod) { Proces_nit(naziv_konstanta, 서술상수, naredba_kod, false); }
    static void Proces_nit(int naziv_konstanta, int 서술상수, int naredba_kod, boolean hrvatski) {
        if (naredba_kod == 184 && Word_SMS(naziv_konstanta, hrvatski ? "YIELD_obaveza" : "yield") && Word_SMS(서술상수, "()V")) { promijeniti_zahtjev = true; return; }
        if (naredba_kod == 184 && Word_SMS(naziv_konstanta, "currentThread") && Word_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(nit_objekt[redovno_nit], 2); return; }
        if (naredba_kod == 183 && Word_SMS(naziv_konstanta, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, hrvatski ? "(Lhrvatski/vlastiti/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int cilj_adresa = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), objekt_Reference = 빼기(2);
            if (!객체유효(objekt_Reference)) return;
            if (힙[objekt_Reference] == 13) { 힙[objekt_Reference + 2] = cilj_adresa; 힙참조[objekt_Reference + 2] = 1; }
            else if (cilj_adresa != 0) kvar_VALUE("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (naredba_kod == 182 && (Word_SMS(naziv_konstanta, hrvatski ? "START_obaveza" : "start") || Word_SMS(naziv_konstanta, hrvatski ? "기다리기" : "join")) && Word_SMS(서술상수, "()V") || naredba_kod == 182 && Word_SMS(naziv_konstanta, hrvatski ? "살아있는가" : "isAlive") && Word_SMS(서술상수, "()Z")) {
            int objekt_Reference = 빼기(2); if (!객체유효(objekt_Reference)) return;
            int račun_VALUE = -1; for (int Loop_INDEX = 0; Loop_INDEX < nit_COUNT; Loop_INDEX++) if (nit_objekt[Loop_INDEX] == objekt_Reference) račun_VALUE = Loop_INDEX;
            if (Word_SMS(naziv_konstanta, hrvatski ? "살아있는가" : "isAlive")) { 넣기(račun_VALUE >= 0 && nit_Stanje[račun_VALUE] != 3 ? 1 : 0, 1); return; }
            if (Word_SMS(naziv_konstanta, hrvatski ? "기다리기" : "join")) { if (račun_VALUE >= 0 && nit_Stanje[račun_VALUE] != 3) { 가닥대기[redovno_nit] = račun_VALUE; nit_Stanje[redovno_nit] = 2; promijeniti_zahtjev = true; } return; }
            if (račun_VALUE >= 0) { 예외던짐(hrvatski ? 38 : 16, "thread already started"); return; }
            if (nit_COUNT == 4) { kvar_VALUE("thread limit (4 including main)"); return; }
            int cilj_adresa = 힙[objekt_Reference] == 13 ? 힙[objekt_Reference + 2] : objekt_Reference;
            int Datoteka_INDEX = cilj_adresa > 0 && 힙[cilj_adresa] >= 32 ? naziv_postupak(힙[cilj_adresa] - 32, hrvatski ? "Izvrši" : "run", "()V") : -1;
            if (cilj_adresa != 0 && Datoteka_INDEX < 0) { kvar_VALUE("Runnable.run required"); return; }
            račun_VALUE = nit_COUNT++; nit_objekt[račun_VALUE] = objekt_Reference; nit_cilj[račun_VALUE] = cilj_adresa;
            int kadar = račun_VALUE * 32; nit_kadar[račun_VALUE] = Datoteka_INDEX < 0 ? kadar - 1 : kadar; nit_Stanje[račun_VALUE] = Datoteka_INDEX < 0 ? 3 : 1;
            if (Datoteka_INDEX >= 0) { kadar_postupak[kadar] = Datoteka_INDEX; kadar_položaj[kadar] = postupak_START[Datoteka_INDEX]; lokalno_VALUE[kadar * 128] = cilj_adresa; lokalno_TYPE[kadar * 128] = 2; }
            return;
        }
        kvar_VALUE("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], adresa_SMS = new int[16];
    static int lokalno_adresa() { return adresa_objekt(0x7f000001); }
    static int adresa_objekt(int VALUE) { int objekt_Reference = dodijeli_Pohrana(14, 1); if (!GREŠKA) 힙[objekt_Reference + 2] = VALUE; return objekt_Reference; }
    static int 주소해독(int objekt_Reference) {
        if (objekt_Reference == 0 || 글같음(objekt_Reference, domaćin_znak("localhost"), false)) return 0x7f000001;
        if (!objekt_VALUE(objekt_Reference, 1)) return 0;
        int podaci_VALUE = 0, ukupni_zbroj_COUNT = 0, adresa_bajt = 0, 자릿수 = 0, unos_COUNT = 힙[objekt_Reference + 1];
        for (int Loop_INDEX = 0; Loop_INDEX <= unos_COUNT; Loop_INDEX++) {
            int kodna_točka = Loop_INDEX == unos_COUNT ? '.' : 힙[objekt_Reference + 2 + Loop_INDEX];
            if (kodna_točka == '.') { if (자릿수 == 0 || ukupni_zbroj_COUNT == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } podaci_VALUE = podaci_VALUE << 8 | adresa_bajt; ukupni_zbroj_COUNT++; adresa_bajt = 자릿수 = 0; }
            else { if (kodna_točka < '0' || kodna_točka > '9' || ++자릿수 > 3 || (adresa_bajt = adresa_bajt * 10 + kodna_točka - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (ukupni_zbroj_COUNT != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return podaci_VALUE;
    }
    static int adresa_znak(int podaci_VALUE) {
        int unos_COUNT = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int adresa_bajt = podaci_VALUE >>> 이동비트 & 255;
            if (adresa_bajt >= 100) adresa_SMS[unos_COUNT++] = '0' + adresa_bajt / 100;
            if (adresa_bajt >= 10) adresa_SMS[unos_COUNT++] = '0' + adresa_bajt / 10 % 10;
            adresa_SMS[unos_COUNT++] = '0' + adresa_bajt % 10; if (이동비트 != 0) adresa_SMS[unos_COUNT++] = '.';
        }
        int objekt_Reference = dodijeli_Pohrana(1, unos_COUNT); if (!GREŠKA) for (int Loop_INDEX = 0; Loop_INDEX < unos_COUNT; Loop_INDEX++) 힙[objekt_Reference + 2 + Loop_INDEX] = adresa_SMS[Loop_INDEX]; return objekt_Reference;
    }
    static void 통신호출(int vlasnik, int naziv_konstanta, int 서술상수, int naredba_kod) {
        if (Word_SMS(vlasnik, "java/net/InetAddress")) {
            if (naredba_kod == 184 && Word_SMS(naziv_konstanta, "getLoopbackAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(lokalno_adresa(), 2); return; }
            if (naredba_kod == 184 && Word_SMS(naziv_konstanta, "getByName") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int podaci_VALUE = 주소해독(빼기(2)); if (던진객체 == 0 && !GREŠKA) 넣기(adresa_objekt(podaci_VALUE), 2); return;
            }
            if (naredba_kod == 182 && Word_SMS(naziv_konstanta, "getHostAddress") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int objekt_Reference = 빼기(2); if (objekt_VALUE(objekt_Reference, 14)) 넣기(adresa_znak(힙[objekt_Reference + 2]), 2); return; }
        }
        if (Word_SMS(vlasnik, "java/net/DatagramPacket")) {
            if (naredba_kod == 183 && Word_SMS(naziv_konstanta, "<init>") && (Word_SMS(서술상수, "([BI)V") || Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean odredište_VALUE_Reference = Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int broj_priključka = odredište_VALUE_Reference ? 빼기(1) : 0, adresa_Reference = odredište_VALUE_Reference ? 빼기(2) : 0;
                int unos_COUNT = 빼기(1), podaci_ARRAY = 빼기(2), objekt_Reference = 빼기(2);
                if (!objekt_VALUE(objekt_Reference, 16) || !objekt_VALUE(podaci_ARRAY, 20)) return;
                if (unos_COUNT < 0 || unos_COUNT > 힙[podaci_ARRAY + 1] || broj_priključka < 0 || broj_priključka > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (adresa_Reference != 0 && !objekt_VALUE(adresa_Reference, 14)) return;
                힙[objekt_Reference + 2] = podaci_ARRAY; 힙참조[objekt_Reference + 2] = 1; 힙[objekt_Reference + 3] = unos_COUNT;
                힙[objekt_Reference + 4] = adresa_Reference; 힙참조[objekt_Reference + 4] = 1; 힙[objekt_Reference + 5] = broj_priključka; return;
            }
            if (naredba_kod == 182 && Word_SMS(naziv_konstanta, "setLength") && Word_SMS(서술상수, "(I)V")) {
                int unos_COUNT = 빼기(1), objekt_Reference = 빼기(2); if (!objekt_VALUE(objekt_Reference, 16)) return;
                if (unos_COUNT < 0 || unos_COUNT > 힙[힙[objekt_Reference + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[objekt_Reference + 3] = unos_COUNT; return;
            }
            if (naredba_kod == 182 && (Word_SMS(naziv_konstanta, "getData") && Word_SMS(서술상수, "()[B") || Word_SMS(naziv_konstanta, "getLength") && Word_SMS(서술상수, "()I") || Word_SMS(naziv_konstanta, "getAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;") || Word_SMS(naziv_konstanta, "getPort") && Word_SMS(서술상수, "()I"))) {
                int objekt_Reference = 빼기(2); if (!objekt_VALUE(objekt_Reference, 16)) return;
                int unos_položaj = Word_SMS(naziv_konstanta, "getData") ? 2 : Word_SMS(naziv_konstanta, "getLength") ? 3 : Word_SMS(naziv_konstanta, "getAddress") ? 4 : 5;
                넣기(힙[objekt_Reference + unos_položaj], unos_položaj == 2 || unos_položaj == 4 ? 2 : 1); return;
            }
        }
        if (Word_SMS(vlasnik, "java/net/DatagramSocket")) {
            if (naredba_kod == 183 && Word_SMS(naziv_konstanta, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(I)V"))) {
                int broj_priključka = Word_SMS(서술상수, "()V") ? 0 : 빼기(1), objekt_Reference = 빼기(2); if (!objekt_VALUE(objekt_Reference, 15)) return;
                if (broj_priključka < 0 || broj_priključka > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = korisnik.otvoreno_mreža(broj_priključka); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[objekt_Reference + 2] = 열린파일번호; return;
            }
            if (naredba_kod == 182 && Word_SMS(naziv_konstanta, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), objekt_Reference = 빼기(2); if (!objekt_VALUE(objekt_Reference, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[objekt_Reference + 3] = 밀리초값; return;
            }
            if (naredba_kod == 182 && Word_SMS(naziv_konstanta, "getLocalPort") && Word_SMS(서술상수, "()I")) { int objekt_Reference = 빼기(2); if (objekt_VALUE(objekt_Reference, 15)) 넣기(힙[objekt_Reference + 2] < 0 ? -1 : korisnik.mreža_prebaciti(힙[objekt_Reference + 2]), 1); return; }
            if (naredba_kod == 182 && Word_SMS(naziv_konstanta, "isClosed") && Word_SMS(서술상수, "()Z")) { int objekt_Reference = 빼기(2); if (objekt_VALUE(objekt_Reference, 15)) 넣기(힙[objekt_Reference + 2] < 0 ? 1 : 0, 1); return; }
            if (naredba_kod == 182 && Word_SMS(naziv_konstanta, "close") && Word_SMS(서술상수, "()V")) { int objekt_Reference = 빼기(2); if (objekt_VALUE(objekt_Reference, 15) && 힙[objekt_Reference + 2] >= 0) { korisnik.파일서술자닫기(힙[objekt_Reference + 2]); 힙[objekt_Reference + 2] = -1; } return; }
            if (naredba_kod == 182 && (Word_SMS(naziv_konstanta, "send") || Word_SMS(naziv_konstanta, "receive")) && Word_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int paket = 빼기(2), objekt_Reference = 빼기(2); if (!objekt_VALUE(paket, 16) || !objekt_VALUE(objekt_Reference, 15)) return;
                int podaci_ARRAY = 힙[paket + 2], 유효길이 = 힙[paket + 3], 열린파일번호 = 힙[objekt_Reference + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_SMS(naziv_konstanta, "send")) {
                    if (!objekt_VALUE(힙[paket + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < 유효길이; Loop_INDEX++) 통신임시[Loop_INDEX] = 힙[podaci_ARRAY + 2 + Loop_INDEX];
                    if (korisnik.slati_mreža(열린파일번호, 힙[힙[paket + 4] + 2], 힙[paket + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int unos_COUNT = korisnik.primiti_mreža(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (unos_COUNT == -11) {
                        int redovno_TIME = korisnik.밀리초();
                        if (힙[objekt_Reference + 4] == 0) 힙[objekt_Reference + 4] = redovno_TIME + 1;
                        if (힙[objekt_Reference + 3] > 0 && redovno_TIME - (힙[objekt_Reference + 4] - 1) >= 힙[objekt_Reference + 3]) { 힙[objekt_Reference + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(objekt_Reference, 2); 넣기(paket, 2); kadar_položaj[kadar_INDEX] = 틀명령[kadar_INDEX]; promijeniti_zahtjev = true; return;
                    }
                    힙[objekt_Reference + 4] = 0;
                    if (unos_COUNT < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < unos_COUNT; Loop_INDEX++) 힙[podaci_ARRAY + 2 + Loop_INDEX] = (byte)통신임시[Loop_INDEX];
                    힙[paket + 3] = unos_COUNT; 힙[paket + 4] = adresa_objekt(통신임시[513]); 힙참조[paket + 4] = 1; 힙[paket + 5] = 통신임시[512];
                }
                return;
            }
        }
        kvar_VALUE("unsupported java.net method");
    }
    static boolean 흐름대기(int objekt_Reference) {
        int redovno_TIME = korisnik.밀리초();
        if (힙[objekt_Reference + 5] == 0) 힙[objekt_Reference + 5] = redovno_TIME + 1;
        if (힙[objekt_Reference + 3] > 0 && redovno_TIME - (힙[objekt_Reference + 5] - 1) >= 힙[objekt_Reference + 3]) { 힙[objekt_Reference + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        kadar_položaj[kadar_INDEX] = 틀명령[kadar_INDEX]; promijeniti_zahtjev = true; return true;
    }
    static void 흐름호출(int vlasnik, int naziv_konstanta, int 서술상수, int naredba_kod) {
        boolean primiti_dojaviti = Word_SMS(vlasnik, "java/net/ServerSocket"), tok = Word_SMS(vlasnik, "java/io/InputStream") || Word_SMS(vlasnik, "java/io/OutputStream");
        if (!tok && naredba_kod == 183 && Word_SMS(naziv_konstanta, "<init>")) {
            boolean 빈여부 = Word_SMS(서술상수, "()V"), 이름지정여부 = Word_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || primiti_dojaviti && Word_SMS(서술상수, "(I)V") || !primiti_dojaviti && (이름지정여부 || 주소지정여부))) { kvar_VALUE("unsupported socket constructor"); return; }
            int broj_priključka = 빈여부 ? 0 : 빼기(1), adresa_Reference = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, objekt_Reference = 빼기(2);
            if (!objekt_VALUE(objekt_Reference, primiti_dojaviti ? 18 : 17)) return;
            if (broj_priključka < 0 || broj_priključka > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !objekt_VALUE(adresa_Reference, 14)) return;
            int mrežni_ID = 이름지정여부 ? 주소해독(adresa_Reference) : 주소지정여부 ? 힙[adresa_Reference + 2] : 0x7f000001;
            if (GREŠKA || 던진객체 != 0) return;
            int 열린파일번호 = korisnik.tok_kontrola(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : primiti_dojaviti ? korisnik.tok_kontrola(1, 열린파일번호, broj_priključka) : korisnik.CONNECT_tok(열린파일번호, mrežni_ID, broj_priključka);
            if (처리값 < 0) { korisnik.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[objekt_Reference + 2] = 열린파일번호; 힙[objekt_Reference + 4] = broj_priključka; 힙[objekt_Reference + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!tok && Word_SMS(naziv_konstanta, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), objekt_Reference = 빼기(2); if (!objekt_VALUE(objekt_Reference, primiti_dojaviti ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[objekt_Reference + 3] = 밀리초값; return; }
        if (!tok && Word_SMS(naziv_konstanta, "close") && Word_SMS(서술상수, "()V")) { int objekt_Reference = 빼기(2); if (objekt_VALUE(objekt_Reference, primiti_dojaviti ? 18 : 17) && 힙[objekt_Reference + 2] >= 0) { korisnik.파일서술자닫기(힙[objekt_Reference + 2]); 힙[objekt_Reference + 2] = -1; } return; }
        if (!tok && (Word_SMS(naziv_konstanta, "getLocalPort") || Word_SMS(naziv_konstanta, "getPort") || Word_SMS(naziv_konstanta, "isClosed") || Word_SMS(naziv_konstanta, "isConnected"))) {
            int objekt_Reference = 빼기(2); if (!objekt_VALUE(objekt_Reference, primiti_dojaviti ? 18 : 17)) return;
            넣기(Word_SMS(naziv_konstanta, "isClosed") ? 힙[objekt_Reference + 2] < 0 ? 1 : 0 : Word_SMS(naziv_konstanta, "isConnected") ? 힙[objekt_Reference + 6] : Word_SMS(naziv_konstanta, "getPort") ? 힙[objekt_Reference + 4] : 힙[objekt_Reference + 2] < 0 ? -1 : korisnik.tok_kontrola(4, 힙[objekt_Reference + 2], 0), 1); return;
        }
        if (primiti_dojaviti && Word_SMS(naziv_konstanta, "accept") && Word_SMS(서술상수, "()Ljava/net/Socket;")) {
            int objekt_Reference = 빼기(2); if (!objekt_VALUE(objekt_Reference, 18)) return; int 열린파일번호 = korisnik.tok_kontrola(3, 힙[objekt_Reference + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(objekt_Reference)) 넣기(objekt_Reference, 2); return; }
            힙[objekt_Reference + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = dodijeli_Pohrana(17, 5); if (GREŠKA) { korisnik.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = korisnik.tok_kontrola(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!primiti_dojaviti && !tok && ((Word_SMS(naziv_konstanta, "getInputStream") && Word_SMS(서술상수, "()Ljava/io/InputStream;")) || (Word_SMS(naziv_konstanta, "getOutputStream") && Word_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int objekt_Reference = 빼기(2); if (!objekt_VALUE(objekt_Reference, 17)) return; if (힙[objekt_Reference + 2] < 0 || 힙[objekt_Reference + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = dodijeli_Pohrana(19, 4); if (GREŠKA) return; 힙[반환값 + 2] = objekt_Reference; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Word_SMS(naziv_konstanta, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (tok) {
            boolean 읽기여부 = Word_SMS(naziv_konstanta, "read"), odjel_informacijske_tehnologije_zapisivanje_operacija = Word_SMS(naziv_konstanta, "write"), blok = Word_SMS(서술상수, "([B)I") || Word_SMS(서술상수, "([B)V"), odjel_informacijske_tehnologije_SUBARRAY = Word_SMS(서술상수, "([BII)I") || Word_SMS(서술상수, "([BII)V");
            int unos_COUNT = odjel_informacijske_tehnologije_SUBARRAY ? 빼기(1) : 0, 시작변위 = odjel_informacijske_tehnologije_SUBARRAY ? 빼기(1) : 0, podaci_ARRAY = blok || odjel_informacijske_tehnologije_SUBARRAY ? 빼기(2) : 0;
            int podaci_VALUE = odjel_informacijske_tehnologije_zapisivanje_operacija && Word_SMS(서술상수, "(I)V") ? 빼기(1) : 0, objekt_Reference = 빼기(2);
            if (!objekt_VALUE(objekt_Reference, 19)) return; int roditeljski_Reference = 힙[objekt_Reference + 2], 열린파일번호 = 힙[roditeljski_Reference + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_SMS(naziv_konstanta, "close") && Word_SMS(서술상수, "()V")) { korisnik.파일서술자닫기(열린파일번호); 힙[roditeljski_Reference + 2] = -1; return; }
            if (Word_SMS(naziv_konstanta, "flush") && Word_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !odjel_informacijske_tehnologije_zapisivanje_operacija) || 읽기여부 != (힙[objekt_Reference + 3] == 0)) { kvar_VALUE("unsupported stream operation"); return; }
            if (blok || odjel_informacijske_tehnologije_SUBARRAY) { if (!objekt_VALUE(podaci_ARRAY, 20)) return; if (blok) unos_COUNT = 힙[podaci_ARRAY + 1]; if (시작변위 < 0 || unos_COUNT < 0 || 시작변위 > 힙[podaci_ARRAY + 1] - unos_COUNT) { 예외던짐(6, "stream array bounds"); return; } }
            else unos_COUNT = 1;
            if (unos_COUNT == 0) { if (읽기여부) 넣기(0, 1); return; }
            int Dovršeno_COUNT = odjel_informacijske_tehnologije_zapisivanje_operacija ? 힙[objekt_Reference + 4] : 0, 처리값 = 0;
            while (Dovršeno_COUNT < unos_COUNT) {
                처리값 = 읽기여부 ? korisnik.파일한바이트읽기(열린파일번호) : korisnik.파일한바이트쓰기(열린파일번호, blok || odjel_informacijske_tehnologije_SUBARRAY ? 힙[podaci_ARRAY + 2 + 시작변위 + Dovršeno_COUNT] : podaci_VALUE);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (blok || odjel_informacijske_tehnologije_SUBARRAY)) 힙[podaci_ARRAY + 2 + 시작변위 + Dovršeno_COUNT] = (byte)처리값;
                Dovršeno_COUNT++; if (읽기여부 && !(blok || odjel_informacijske_tehnologije_SUBARRAY)) break;
            }
            if (처리값 == -11 && (odjel_informacijske_tehnologije_zapisivanje_operacija || Dovršeno_COUNT == 0)) {
                힙[objekt_Reference + 4] = Dovršeno_COUNT;
                if (흐름대기(roditeljski_Reference)) { 넣기(objekt_Reference, 2); if (blok || odjel_informacijske_tehnologije_SUBARRAY) 넣기(podaci_ARRAY, 2); if (odjel_informacijske_tehnologije_SUBARRAY) { 넣기(시작변위, 1); 넣기(unos_COUNT, 1); } if (odjel_informacijske_tehnologije_zapisivanje_operacija && !(blok || odjel_informacijske_tehnologije_SUBARRAY)) 넣기(podaci_VALUE, 1); } return;
            }
            힙[objekt_Reference + 4] = 0; 힙[roditeljski_Reference + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(Dovršeno_COUNT == 0 && 처리값 == 256 ? -1 : blok || odjel_informacijske_tehnologije_SUBARRAY ? Dovršeno_COUNT : 처리값, 1); return;
        }
        kvar_VALUE("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int naziv_konstanta) {
        if (Word_SMS(naziv_konstanta, "hrvatski/vlastiti/Prozor")) return 24;
        if (Word_SMS(naziv_konstanta, "hrvatski/vlastiti/Natpis")) return 26;
        if (Word_SMS(naziv_konstanta, "hrvatski/vlastiti/gumb")) return 27;
        if (Word_SMS(naziv_konstanta, "hrvatski/vlastiti/tekstno_polje")) return 28;
        if (Word_SMS(naziv_konstanta, "hrvatski/vlastiti/akcija_obavijest")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int naziv_konstanta) {
        return 한국어화면종(naziv_konstanta) != 0 || Word_SMS(naziv_konstanta, "hrvatski/vlastiti/화면구성요소") || Word_SMS(naziv_konstanta, "hrvatski/vlastiti/događaj_red_čekanja");
    }
    static int 화면종(int naziv_konstanta) {
        int 한국어종 = 한국어화면종(naziv_konstanta); if (한국어종 != 0) return 한국어종;
        if (Word_SMS(naziv_konstanta, "javax/swing/JFrame")) return 24;
        if (Word_SMS(naziv_konstanta, "javax/swing/JPanel")) return 25;
        if (Word_SMS(naziv_konstanta, "javax/swing/JLabel")) return 26;
        if (Word_SMS(naziv_konstanta, "javax/swing/JButton")) return 27;
        if (Word_SMS(naziv_konstanta, "javax/swing/JTextField")) return 28;
        if (Word_SMS(naziv_konstanta, "java/awt/event/ActionEvent")) return 29;
        if (Word_SMS(naziv_konstanta, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int naziv_konstanta) {
        return 화면종(naziv_konstanta) != 0 || Word_SMS(naziv_konstanta, "java/awt/Component") || Word_SMS(naziv_konstanta, "java/awt/Container") || Word_SMS(naziv_konstanta, "javax/swing/JComponent") || Word_SMS(naziv_konstanta, "javax/swing/AbstractButton") || Word_SMS(naziv_konstanta, "javax/swing/text/JTextComponent") || Word_SMS(naziv_konstanta, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int objekt_Reference) { if (!객체유효(objekt_Reference)) return false; if (힙[objekt_Reference] < 24 || 힙[objekt_Reference] > 28) { kvar_VALUE("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int objekt_Reference, int SMS_Reference) {
        if (SMS_Reference != 0 && !objekt_VALUE(SMS_Reference, 1)) return;
        int unos_COUNT = SMS_Reference == 0 ? 0 : 힙[SMS_Reference + 1]; if (unos_COUNT > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < unos_COUNT; Loop_INDEX++) 화면글임시[Loop_INDEX] = 힙[SMS_Reference + 2 + Loop_INDEX];
        if (korisnik.화면글(힙[objekt_Reference + 2], 화면글임시, unos_COUNT) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[objekt_Reference + 3] = SMS_Reference; 힙참조[objekt_Reference + 3] = 1;
    }
    static int 화면문자읽기(int objekt_Reference) {
        int račun_VALUE = 힙[objekt_Reference + 2], unos_COUNT = korisnik.화면연결(8, račun_VALUE, 0, 0, 0, 0), 사용수 = 0;
        if (unos_COUNT < 0) { kvar_VALUE("GUI text read failed"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < unos_COUNT; Loop_INDEX++) { int 부호값 = korisnik.화면연결(9, račun_VALUE, Loop_INDEX, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = dodijeli_Pohrana(1, 사용수); if (!GREŠKA) for (int Loop_INDEX = 0; Loop_INDEX < 사용수; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 화면글임시[Loop_INDEX]; return 반환값;
    }
    /* hrvatski 객체를 직접 만들고 jezgra_sustava_VALUE 화면 기능에 연결한다. Swing objekt_VALUE/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int vlasnik, int naziv_konstanta, int 서술상수, int naredba_kod) {
        if (Word_SMS(vlasnik, "hrvatski/vlastiti/događaj_red_čekanja")) {
            if (naredba_kod == 184 && Word_SMS(naziv_konstanta, "나중에실행") && Word_SMS(서술상수, "(Lhrvatski/vlastiti/실행할일;)V")) {
                int obaveza_akcija = 빼기(2); if (!객체유효(obaveza_akcija)) return;
                if (나중수 == 8) { kvar_VALUE("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = obaveza_akcija; return;
            }
            if (naredba_kod == 184 && Word_SMS(naziv_konstanta, "사건처리중인가") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            kvar_VALUE("지원하지 않는 hrvatski 화면 일정 호출"); return;
        }
        if (Word_SMS(vlasnik, "hrvatski/vlastiti/akcija_obavijest")) {
            int obavijest = 빼기(2); if (!objekt_VALUE(obavijest, 29) || 힙[obavijest + 3] == 0) return;
            if (Word_SMS(naziv_konstanta, "izvor_događaja") && Word_SMS(서술상수, "()Lhrvatski/vlastiti/화면구성요소;")) 넣기(힙[obavijest + 2], 2);
            else if (Word_SMS(naziv_konstanta, "naredba_SMS") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[obavijest + 2]), 2);
            else if (Word_SMS(naziv_konstanta, "INDEX") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else kvar_VALUE("지원하지 않는 hrvatski Aktivnost obavijest 호출"); return;
        }
        if (naredba_kod == 183 && Word_SMS(naziv_konstanta, "<init>")) {
            int 종류 = 한국어화면종(vlasnik), 받이 = 0, 가로 = 0, Okomito_položaj = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Word_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (korisnik.화면너비() - 폭) / 2; Okomito_položaj = (korisnik.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Word_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Word_SMS(서술상수, "(Ljava/lang/String;IIIILhrvatski/vlastiti/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); Okomito_položaj = 빼기(1); 가로 = 빼기(1);
            } else { kvar_VALUE("지원하지 않는 hrvatski 화면 생성자"); return; }
            int Tekst = 빼기(2), element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || Okomito_položaj < 0 || 폭 > korisnik.화면너비() - 가로 || 높이 > korisnik.화면높이() - Okomito_položaj) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDEX = korisnik.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (INDEX < 1 || INDEX > 32) { kvar_VALUE("화면 element_VALUE 자리가 가득 찼습니다"); return; }
            힙[element_VALUE + 2] = INDEX; 화면참조[INDEX - 1] = element_VALUE;
            힙[element_VALUE + 5] = 가로; 힙[element_VALUE + 6] = Okomito_položaj; 힙[element_VALUE + 7] = 폭; 힙[element_VALUE + 8] = 높이; 힙[element_VALUE + 10] = 2;
            힙[element_VALUE + 4] = 받이; 힙참조[element_VALUE + 4] = 1; 힙[element_VALUE + 12] = 1;
            korisnik.화면연결(1, INDEX, 가로, Okomito_položaj, 폭, 높이);
            if (종류 == 24) korisnik.화면연결(7, INDEX, 2, 0, 0, 0);
            화면문자설정(element_VALUE, Tekst); return;
        }
        if (naredba_kod != 182) { kvar_VALUE("잘못된 hrvatski 화면 호출 Naredba"); return; }
        if (Word_SMS(naziv_konstanta, "zapisivanje_SMS") && Word_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int Tekst = 빼기(2), element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 화면문자설정(element_VALUE, Tekst); return;
        }
        if (Word_SMS(naziv_konstanta, "글읽기") && Word_SMS(서술상수, "()Ljava/lang/String;")) {
            int element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 넣기(화면문자읽기(element_VALUE), 2); return;
        }
        if (Word_SMS(naziv_konstanta, "동작맡기기") && Word_SMS(서술상수, "(Lhrvatski/vlastiti/동작받이;)V")) {
            int 받이 = 빼기(2), element_VALUE = 빼기(2);
            if (화면객체(element_VALUE)) { 힙[element_VALUE + 4] = 받이; 힙참조[element_VALUE + 4] = 1; 힙[element_VALUE + 12] = 1; } return;
        }
        if (Word_SMS(naziv_konstanta, "Dodaj_element") && Word_SMS(서술상수, "(Lhrvatski/vlastiti/화면구성요소;)V")) {
            int dijete_VALUE = 빼기(2), roditeljski_VALUE = 빼기(2); if (!화면객체(dijete_VALUE) || !화면객체(roditeljski_VALUE)) return;
            if (korisnik.화면연결(2, 힙[roditeljski_VALUE + 2], 힙[dijete_VALUE + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[dijete_VALUE + 11] = roditeljski_VALUE; 힙참조[dijete_VALUE + 11] = 1; return;
        }
        if (Word_SMS(naziv_konstanta, "자리정하기") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), Okomito_položaj = 빼기(1), 가로 = 빼기(1), element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (korisnik.화면연결(1, 힙[element_VALUE + 2], 가로, Okomito_položaj, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[element_VALUE + 5] = 가로; 힙[element_VALUE + 6] = Okomito_položaj; 힙[element_VALUE + 7] = 폭; 힙[element_VALUE + 8] = 높이; return;
        }
        if ((Word_SMS(naziv_konstanta, "emisija_prozor") || Word_SMS(naziv_konstanta, "Zatvori")) && Word_SMS(서술상수, "()V")) {
            boolean vidljivost_VALUE = Word_SMS(naziv_konstanta, "emisija_prozor"); int element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (korisnik.화면연결(vidljivost_VALUE ? 3 : 4, 힙[element_VALUE + 2], vidljivost_VALUE ? 1 : 0, 0, 0, 0) < 0) { kvar_VALUE("화면은 대화형 명령에서 실행해야 합니다"); return; }
            힙[element_VALUE + 9] = vidljivost_VALUE ? 1 : 0; return;
        }
        if (Word_SMS(naziv_konstanta, "보이는가") && Word_SMS(서술상수, "()Z")) { int element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 넣기(힙[element_VALUE + 9], 1); return; }
        kvar_VALUE("지원하지 않는 hrvatski 화면 postupak_VALUE");
    }
    static void 화면호출(int vlasnik, int naziv_konstanta, int 서술상수, int naredba_kod) {
        if (Word_SMS(vlasnik, "javax/swing/SwingUtilities")) {
            if (naredba_kod == 184 && Word_SMS(naziv_konstanta, "invokeLater") && Word_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int objekt_Reference = 빼기(2); if (!객체유효(objekt_Reference)) return; if (나중수 == 8) { kvar_VALUE("invokeLater queue full"); return; } 나중실행[나중수++] = objekt_Reference; return; }
            if (naredba_kod == 184 && Word_SMS(naziv_konstanta, "isEventDispatchThread") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            kvar_VALUE("unsupported SwingUtilities method"); return;
        }
        if (Word_SMS(vlasnik, "java/awt/event/ActionEvent")) {
            int objekt_Reference = 빼기(2); if (!objekt_VALUE(objekt_Reference, 29)) return;
            if (Word_SMS(naziv_konstanta, "getSource") && Word_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[objekt_Reference + 2], 2);
            else if (Word_SMS(naziv_konstanta, "getActionCommand") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[objekt_Reference + 2]), 2);
            else if (Word_SMS(naziv_konstanta, "getID") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else kvar_VALUE("unsupported ActionEvent method"); return;
        }
        if (naredba_kod == 183 && Word_SMS(naziv_konstanta, "<init>")) {
            int COLUMNS = 0, SMS_Reference = 0;
            if (Word_SMS(서술상수, "(I)V")) COLUMNS = 빼기(1);
            else if (Word_SMS(서술상수, "(Ljava/lang/String;I)V")) { COLUMNS = 빼기(1); SMS_Reference = 빼기(2); }
            else if (Word_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_Reference = 빼기(2);
            else if (Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_SMS(서술상수, "()V")) { kvar_VALUE("unsupported Swing constructor"); return; }
            int objekt_Reference = 빼기(2); if (!객체유효(objekt_Reference)) return;
            if (힙[objekt_Reference] == 30) { kvar_VALUE("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(objekt_Reference) || COLUMNS < 0) return;
            int račun_VALUE = korisnik.화면연결(0, 힙[objekt_Reference] - 23, 0, 0, 0, 0);
            if (račun_VALUE < 1 || račun_VALUE > 32) { kvar_VALUE("GUI widget slots exhausted"); return; }
            힙[objekt_Reference + 2] = račun_VALUE; 화면참조[račun_VALUE - 1] = objekt_Reference; 힙[objekt_Reference + 5] = 힙[objekt_Reference] == 24 ? 130 : 16; 힙[objekt_Reference + 6] = 힙[objekt_Reference] == 24 ? 110 : 16;
            힙[objekt_Reference + 7] = 힙[objekt_Reference] == 24 ? 380 : 220; 힙[objekt_Reference + 8] = 힙[objekt_Reference] == 24 ? 240 : 28; 힙[objekt_Reference + 10] = 1;
            화면문자설정(objekt_Reference, SMS_Reference); return;
        }
        if (Word_SMS(naziv_konstanta, "setText") || Word_SMS(naziv_konstanta, "setTitle")) { int SMS_Reference = 빼기(2), objekt_Reference = 빼기(2); if (화면객체(objekt_Reference) && Word_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(objekt_Reference, SMS_Reference); return; }
        if (Word_SMS(naziv_konstanta, "getText") || Word_SMS(naziv_konstanta, "getTitle")) { int objekt_Reference = 빼기(2); if (화면객체(objekt_Reference) && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(objekt_Reference), 2); return; }
        if (Word_SMS(naziv_konstanta, "addActionListener") && Word_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int primiti_Reference = 빼기(2), objekt_Reference = 빼기(2); if (화면객체(objekt_Reference)) { 힙[objekt_Reference + 4] = primiti_Reference; 힙참조[objekt_Reference + 4] = 1; } return; }
        if (Word_SMS(naziv_konstanta, "getContentPane") && Word_SMS(서술상수, "()Ljava/awt/Container;")) { int objekt_Reference = 빼기(2); if (화면객체(objekt_Reference)) 넣기(objekt_Reference, 2); return; }
        if (Word_SMS(naziv_konstanta, "setLayout") && Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Raspored_Reference = 빼기(2), objekt_Reference = 빼기(2); if (화면객체(objekt_Reference) && Raspored_Reference != 0) kvar_VALUE("only absolute layout (null) is supported"); return; }
        if (Word_SMS(naziv_konstanta, "add") && (Word_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Raspored_uvjet = Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Raspored_uvjet) 빼기(2);
            int dijete_Reference = 빼기(2), objekt_Reference = 빼기(2); if (!화면객체(dijete_Reference) || !화면객체(objekt_Reference)) return;
            if (korisnik.화면연결(2, 힙[objekt_Reference + 2], 힙[dijete_Reference + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[dijete_Reference + 11] = objekt_Reference; 힙참조[dijete_Reference + 11] = 1; if (!Raspored_uvjet) 넣기(dijete_Reference, 2); return;
        }
        if (Word_SMS(naziv_konstanta, "setBounds") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), koordinata_x = 빼기(1), objekt_Reference = 빼기(2); if (!화면객체(objekt_Reference)) return;
            if (korisnik.화면연결(1, 힙[objekt_Reference + 2], koordinata_x, 세로좌표, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[objekt_Reference + 5] = koordinata_x; 힙[objekt_Reference + 6] = 세로좌표; 힙[objekt_Reference + 7] = 너비; 힙[objekt_Reference + 8] = 높이; return;
        }
        if (Word_SMS(naziv_konstanta, "setSize") && Word_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), objekt_Reference = 빼기(2); if (!화면객체(objekt_Reference)) return;
            if (korisnik.화면연결(1, 힙[objekt_Reference + 2], 힙[objekt_Reference + 5], 힙[objekt_Reference + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[objekt_Reference + 7] = 너비; 힙[objekt_Reference + 8] = 높이; } return;
        }
        if (Word_SMS(naziv_konstanta, "setLocationRelativeTo") && Word_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), objekt_Reference = 빼기(2); if (!화면객체(objekt_Reference)) return; if (상대배치 != 0) { kvar_VALUE("only screen centering supported"); return; } 힙[objekt_Reference + 5] = (korisnik.화면너비() - 힙[objekt_Reference + 7]) / 2; 힙[objekt_Reference + 6] = (korisnik.화면높이() - 힙[objekt_Reference + 8]) / 2; korisnik.화면연결(1, 힙[objekt_Reference + 2], 힙[objekt_Reference + 5], 힙[objekt_Reference + 6], 힙[objekt_Reference + 7], 힙[objekt_Reference + 8]); return; }
        if (Word_SMS(naziv_konstanta, "setDefaultCloseOperation") && Word_SMS(서술상수, "(I)V")) { int pravila = 빼기(1), objekt_Reference = 빼기(2); if (화면객체(objekt_Reference)) { if (pravila < 0 || pravila > 3) 예외던짐(9, "close policy"); else { 힙[objekt_Reference + 10] = pravila; korisnik.화면연결(7, 힙[objekt_Reference + 2], pravila, 0, 0, 0); } } return; }
        if (Word_SMS(naziv_konstanta, "setVisible") && Word_SMS(서술상수, "(Z)V")) { int podaci_VALUE = 빼기(1), objekt_Reference = 빼기(2); if (화면객체(objekt_Reference)) { int 처리값 = korisnik.화면연결(3, 힙[objekt_Reference + 2], podaci_VALUE, 0, 0, 0); if (처리값 < 0) kvar_VALUE("Swing requires a standalone interactive command"); else 힙[objekt_Reference + 9] = podaci_VALUE; } return; }
        if (Word_SMS(naziv_konstanta, "dispose") && Word_SMS(서술상수, "()V")) { int objekt_Reference = 빼기(2); if (화면객체(objekt_Reference)) { korisnik.화면연결(4, 힙[objekt_Reference + 2], 0, 0, 0, 0); 힙[objekt_Reference + 9] = 0; } return; }
        if (Word_SMS(naziv_konstanta, "repaint") || Word_SMS(naziv_konstanta, "validate")) { int objekt_Reference = 빼기(2); if (!화면객체(objekt_Reference) || !Word_SMS(서술상수, "()V")) return; korisnik.화면연결(1, 힙[objekt_Reference + 2], 힙[objekt_Reference + 5], 힙[objekt_Reference + 6], 힙[objekt_Reference + 7], 힙[objekt_Reference + 8]); return; }
        if (Word_SMS(naziv_konstanta, "isVisible") && Word_SMS(서술상수, "()Z")) { int objekt_Reference = 빼기(2); if (화면객체(objekt_Reference)) 넣기(힙[objekt_Reference + 9], 1); return; }
        kvar_VALUE("unsupported Swing method (native subset)");
    }
    static void 사건실행(int cilj_adresa, int 사건번호, boolean hrvatski) {
        if (cilj_adresa < 1 || 힙[cilj_adresa] < 32) { kvar_VALUE("Java event listener required"); return; }
        int Datoteka_INDEX = naziv_postupak(힙[cilj_adresa] - 32, 사건번호 == 0 ? (hrvatski ? "Izvrši" : "run") : (hrvatski ? "primiti_akcija" : "actionPerformed"), 사건번호 == 0 ? "()V" : (hrvatski ? "(Lhrvatski/vlastiti/akcija_obavijest;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (Datoteka_INDEX < 0) { kvar_VALUE("event callback missing"); return; }
        redovno_nit = 0; nit_COUNT = 1; kadar_INDEX = 0; nit_Stanje[0] = 1; kadar_hrpa[0] = 0; kadar_zaključati[0] = 틀초기화[0] = 0; promijeniti_zahtjev = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 128; Loop_INDEX++) { lokalno_VALUE[Loop_INDEX] = lokalno_TYPE[Loop_INDEX] = 0; }
        kadar_postupak[0] = Datoteka_INDEX; kadar_položaj[0] = postupak_START[Datoteka_INDEX]; lokalno_VALUE[0] = cilj_adresa; lokalno_TYPE[0] = 2;
        if (사건번호 != 0) { lokalno_VALUE[1] = 사건번호; lokalno_TYPE[1] = 2; }
        사건중 = true; Izvrši_naredba(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!GREŠKA) {
            if (나중수 > 0) { int cilj_adresa = 나중실행[0], hrvatski = 나중한국어[0]; for (int Loop_INDEX = 1; Loop_INDEX < 나중수; Loop_INDEX++) { 나중실행[Loop_INDEX - 1] = 나중실행[Loop_INDEX]; 나중한국어[Loop_INDEX - 1] = 나중한국어[Loop_INDEX]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(cilj_adresa, 0, hrvatski != 0); continue; }
            if (korisnik.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = korisnik.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { kvar_VALUE("GUI event I/O failed"); return; }
            int račun_VALUE = 사건번호 & 65535; if (račun_VALUE < 1 || račun_VALUE > 32) continue; int objekt_Reference = 화면참조[račun_VALUE - 1]; if (objekt_Reference == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[objekt_Reference + 10] != 0) 힙[objekt_Reference + 9] = 0;
                if (힙[objekt_Reference + 10] == 3) for (int Loop_INDEX = 0; Loop_INDEX < 32; Loop_INDEX++) if (화면참조[Loop_INDEX] != 0 && 힙[화면참조[Loop_INDEX]] == 24) korisnik.화면연결(4, Loop_INDEX + 1, 0, 0, 0, 0);
            } else if (힙[objekt_Reference + 4] != 0) {
                int 안내참조 = dodijeli_Pohrana(29, 2); if (GREŠKA) return; 힙[안내참조 + 2] = objekt_Reference; 힙[안내참조 + 3] = 힙[objekt_Reference + 12]; 힙참조[안내참조 + 2] = 1; 사건실행(힙[objekt_Reference + 4], 안내참조, 힙[objekt_Reference + 12] != 0);
            }
        }
    }
    public static int Pokreni() {
        if (korisnik.인수개수() == 1 && 자바도구.같음(korisnik.Argumenti(0), "-version")) {
            korisnik.Zapisuj("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (korisnik.인수개수() < 1) { korisnik.Zapisuj("Usage: java CLASS [ARGS]\n"); return 2; }
        unos_poduka_definicija = dosje_poduka_definicija(domaćin_znak(korisnik.Argumenti(0))); if (GREŠKA || unos_poduka_definicija < 0) return 1;
        int unos_p_VALUE = naziv_postupak(unos_poduka_definicija, "Pokreni", "()V");
        boolean 한국어진입 = unos_p_VALUE >= 0 && (postupak_pristup[unos_p_VALUE] & 9) == 9;
        if (!한국어진입) unos_p_VALUE = naziv_postupak(unos_poduka_definicija, "main", "([Ljava/lang/String;)V");
        if (unos_p_VALUE < 0 || (postupak_pristup[unos_p_VALUE] & 9) != 9) kvar_VALUE("public static void Pokreni() or main(String[] args) required");
        if (GREŠKA) return 1;
        int Argumenti = dodijeli_Pohrana(3, korisnik.인수개수() - 1); element_polja[Argumenti] = -1;
        for (int 수 = 1; 수 < korisnik.인수개수() && !GREŠKA; 수++) 힙[Argumenti + 1 + 수] = domaćin_znak(korisnik.Argumenti(수));
        kadar_INDEX = 0; kadar_postupak[0] = unos_p_VALUE; kadar_položaj[0] = postupak_START[unos_p_VALUE]; lokalno_VALUE[0] = 한국어진입 ? 0 : Argumenti; lokalno_TYPE[0] = 한국어진입 ? 0 : 2;
        nit_Stanje[0] = 1; nit_objekt[0] = dodijeli_Pohrana(13, 2);
        Izvrši_naredba(); if (!GREŠKA) 화면사건들(); return GREŠKA ? 1 : 0;
    }
}
