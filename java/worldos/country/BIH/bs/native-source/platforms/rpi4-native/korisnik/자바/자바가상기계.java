// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Fajl/operand_snop/Reference/ogranak 경계를 Izvrši_komanda 중 검사한다. */
public final class 자바가상기계 {
    static int[] Fajl = new int[16 * 16384], 임시파일 = new int[16384], fajl_naziv_SMS = new int[512];
    static int[] konstanta_oznaka = new int[8192], 상가 = new int[8192], konstanta_SECOND_VALUE = new int[8192], string_Reference = new int[8192];
    static int[] metoda_naziv_SMS = new int[512], metoda_TYPE = new int[512], metoda_pristup = new int[512], metoda_vlasnik = new int[512];
    static int[] metoda_START = new int[512], metoda_završiti = new int[512], metoda_snop = new int[512], 함수지역 = new int[512];
    static int[] metoda_argument_COUNT = new int[512], metoda_argument_TYPE = new int[8192], metoda_vratiti = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] lokalni_VALUE = new int[16384], lokalni_TYPE = new int[16384], operand_snop_VALUE = new int[16384], operand_snop_TYPE = new int[16384];
    static int[] kadar_metoda = new int[128], kadar_položaj = new int[128], kadar_snop = new int[128], kadar_programska_naredba = new int[128], inicijalizirati_kadar = new int[128];
    static int[] klasa_Definicija_naziv = new int[16], klasa_Definicija_podesiti_veličinu = new int[16], klasa_Definicija_roditelj = new int[16], klasa_Definicija_stanje = new int[16], klasa_prostor_za_unos_COUNT = new int[16], inicijalizirati_klasa_Definicija = new int[16];
    static int[] klasa_interfejs = new int[16 * 16], klasa_interfejs_COUNT = new int[16];
    static int[] prostor_za_unos_naziv = new int[512], prostor_za_unos_TYPE = new int[512], prostor_za_unos_vlasnik = new int[512], prostor_za_unos_dozvole = new int[512], prostor_za_unos_položaj = new int[512], prostor_za_unos_podaci = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], niz_element = new int[32768], Store_cijeli_broj = new int[256];
    static int Veličina, 읽기위치, metoda_COUNT, naziv_klase, kadar_INDEX = -1, 힙끝 = 1, vratiti_TYPE;
    static int klasa_Definicija_COUNT, prostor_za_unos_COUNT, 잡기수, 현재읽는종, 던진객체, 잠시수, ekran_COUNT, Kolekcija_COUNT;
    static int trenutno_nit, nit_COUNT = 1, unos_klasa_Definicija;
    static int[] nit_kadar = new int[4], nit_stanje = new int[4], nit_objekt = new int[4], nit_cilj = new int[4], 가닥대기 = new int[4];
    static boolean GRESKA, promijeniti_HTTP_zahtjev;
    static int[] 잠금주인 = new int[32768], 잠금깊이 = new int[32768], 틀잠금 = new int[128], 종잠금 = new int[16], klasa_nit = new int[16];

    static void neuspjeh_VALUE(String Word_SMS) {
        if (GRESKA) return;
        int oblast_kod = 0;
        if (자바도구.같음(Word_SMS, "ArithmeticException: / by zero")) oblast_kod = 4;
        if (자바도구.같음(Word_SMS, "NullPointerException") || 자바도구.같음(Word_SMS, "null or invalid array")) oblast_kod = 5;
        if (자바도구.같음(Word_SMS, "ArrayIndexOutOfBoundsException")) oblast_kod = 7;
        if (자바도구.같음(Word_SMS, "StringIndexOutOfBoundsException")) oblast_kod = 8;
        if (자바도구.같음(Word_SMS, "NumberFormatException")) oblast_kod = 10;
        if (자바도구.같음(Word_SMS, "FileNotFoundException: file open failed")) oblast_kod = 12;
        if (자바도구.같음(Word_SMS, "IOException: stream closed") || 자바도구.같음(Word_SMS, "IOException: read failed") || 자바도구.같음(Word_SMS, "IOException: write failed")) oblast_kod = 11;
        if (자바도구.같음(Word_SMS, "ClassCastException")) oblast_kod = 14;
        if (자바도구.같음(Word_SMS, "NegativeArraySizeException")) oblast_kod = 15;
        if (oblast_kod != 0 && kadar_INDEX >= 0) { 예외던짐(oblast_kod, Word_SMS); return; }
        korisnik.Piši("JVM error: "); korisnik.Piši(Word_SMS); korisnik.pisati_znak_VALUE(10); GRESKA = true;
    }
    static boolean isječak(int Pokreni, int dužina_VALUE) {
        if (Pokreni < 0 || Pokreni >= Fajl.length || dužina_VALUE < 0) return false;
        int klasa_Definicija = Pokreni / 16384;
        return Pokreni % 16384 <= klasa_Definicija_podesiti_veličinu[klasa_Definicija] && dužina_VALUE <= klasa_Definicija_podesiti_veličinu[klasa_Definicija] - Pokreni % 16384;
    }
    static int bajt_VALUE() {
        if (!isječak(읽기위치, 1)) { neuspjeh_VALUE("truncated class file"); return 0; }
        return Fajl[읽기위치++];
    }
    static int 짧은수() { return bajt_VALUE() << 8 | bajt_VALUE(); }
    static int cijeli_broj() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int dužina_VALUE) { if (!isječak(읽기위치, dužina_VALUE)) neuspjeh_VALUE("invalid attribute size"); else 읽기위치 += dužina_VALUE; }
    static boolean ček_konstanta(int 수, int 종류) {
        if (수 <= 0 || 수 >= konstanta_oznaka.length || konstanta_oznaka[수] != 종류) { neuspjeh_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Pokreni, int dužina_VALUE, String Word_SMS) {
        if (!isječak(Pokreni, dužina_VALUE)) return false;
        int 읽는자리 = Pokreni, 끝 = Pokreni + dužina_VALUE;
        for (int Loop_INDEX = 0; Loop_INDEX < Word_SMS.length(); Loop_INDEX++) {
            int kôd_znaka = Word_SMS.charAt(Loop_INDEX);
            if (kôd_znaka > 0 && kôd_znaka < 128) { if (읽는자리 >= 끝 || Fajl[읽는자리++] != kôd_znaka) return false; }
            else if (kôd_znaka < 2048) {
                if (읽는자리 + 2 > 끝 || Fajl[읽는자리++] != (192 | (kôd_znaka >> 6)) || Fajl[읽는자리++] != (128 | (kôd_znaka & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Fajl[읽는자리++] != (224 | (kôd_znaka >> 12)) || Fajl[읽는자리++] != (128 | ((kôd_znaka >> 6) & 63)) || Fajl[읽는자리++] != (128 | (kôd_znaka & 63))) return false;
        }
        return 읽는자리 == 끝;
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
    static int 상번호() { int VALUE = 짧은수(); return VALUE == 0 ? 0 : 현재읽는종 * 512 + VALUE; }
    static int 명상수() { return metoda_vlasnik[kadar_metoda[kadar_INDEX]] * 512 + 명짧(); }
    static void 속성건너() {
        int stavka_COUNT = 짧은수();
        for (int 수 = 0; 수 < stavka_COUNT && !GRESKA; 수++) { ček_konstanta(상번호(), 1); 건너(cijeli_broj()); }
    }
    static int komanda_dužina(int VALUE) {
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
        if (!isječak(읽는자리, 4)) { neuspjeh_VALUE("truncated bytecode operand"); return 0; }
        return Fajl[읽는자리] << 24 | Fajl[읽는자리 + 1] << 16 | Fajl[읽는자리 + 2] << 8 | Fajl[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Pokreni, int 끝) {
        int VALUE = Fajl[읽는자리], dužina_VALUE = komanda_dužina(VALUE);
        if (VALUE == 170 || VALUE == 171) {
            int BASE_položaj = 읽는자리 + 1;
            while ((BASE_položaj - Pokreni) % 4 != 0) BASE_položaj++;
            if (끝 - BASE_položaj < (VALUE == 170 ? 12 : 8)) return 0;
            int unos_COUNT = VALUE == 170 ? položaj_cijeli_broj(BASE_položaj + 8) - položaj_cijeli_broj(BASE_položaj + 4) + 1 : položaj_cijeli_broj(BASE_položaj + 4);
            if (unos_COUNT < 0 || unos_COUNT > 2048) return 0;
            dužina_VALUE = BASE_položaj - 읽는자리 + (VALUE == 170 ? 12 + 4 * unos_COUNT : 8 + 8 * unos_COUNT);
        }
        if (VALUE == 196 && 읽는자리 + 1 < 끝) {
            int Word_podaci = Fajl[읽는자리 + 1]; dužina_VALUE = Word_podaci == 132 ? 6 : (Word_podaci == 21 || Word_podaci == 25 || Word_podaci == 54 || Word_podaci == 58) ? 4 : 0;
        }
        return dužina_VALUE > 0 && dužina_VALUE <= 끝 - 읽는자리 ? dužina_VALUE : 0;
    }
    static void ček_odredište_VALUE(int odredište_VALUE, int FUNCTION_VALUE) {
        if (odredište_VALUE < metoda_START[FUNCTION_VALUE] || odredište_VALUE >= metoda_završiti[FUNCTION_VALUE] || 경계[odredište_VALUE] != FUNCTION_VALUE + 1) neuspjeh_VALUE("invalid branch target");
    }
    static void 클래스읽기(int klasa_Definicija) {
        현재읽는종 = klasa_Definicija; 읽기위치 = klasa_Definicija * 16384; Veličina = 읽기위치 + klasa_Definicija_podesiti_veličinu[klasa_Definicija];
        if (cijeli_broj() != 0xcafebabe) { neuspjeh_VALUE("not a class file"); return; }
        int 부판 = 짧은수(), verzija_VALUE = 짧은수();
        if (verzija_VALUE < 45 || verzija_VALUE > 52 || 부판 != 0) { neuspjeh_VALUE("supported class versions: 45..52, minor 0"); return; }
        int konstanta_COUNT = 짧은수(), BASE_položaj = klasa_Definicija * 512;
        if (konstanta_COUNT < 1 || konstanta_COUNT > 512) { neuspjeh_VALUE("constant pool limit (511)"); return; }
        for (int unos_COUNT = 1; unos_COUNT < konstanta_COUNT && !GRESKA; unos_COUNT++) {
            int 수 = BASE_položaj + unos_COUNT, 종류 = bajt_VALUE(); konstanta_oznaka[수] = 종류;
            if (종류 == 1) { konstanta_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(konstanta_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = cijeli_broj();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); konstanta_SECOND_VALUE[수] = 상번호(); }
            else neuspjeh_VALUE("unsupported constant type");
        }
        int dozvola_VALUE = 짧은수();
        if ((dozvola_VALUE & (0x2000 | 0x4000)) != 0) neuspjeh_VALUE("annotation/enum class unsupported");
        klasa_Definicija_naziv[klasa_Definicija] = naziv_klase_SMS(상번호());
        klasa_Definicija_roditelj[klasa_Definicija] = naziv_klase_SMS(상번호());
        int interfejs_COUNT = 짧은수(); if (interfejs_COUNT > 16) { neuspjeh_VALUE("interface count limit"); return; }
        klasa_interfejs_COUNT[klasa_Definicija] = interfejs_COUNT;
        for (int Loop_INDEX = 0; Loop_INDEX < interfejs_COUNT; Loop_INDEX++) klasa_interfejs[klasa_Definicija * 16 + Loop_INDEX] = naziv_klase_SMS(상번호());
        int polje_COUNT = 짧은수();
        if (polje_COUNT > 512 - prostor_za_unos_COUNT) { neuspjeh_VALUE("field count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < polje_COUNT && !GRESKA; Loop_INDEX++) {
            int fajl_INDEX = prostor_za_unos_COUNT++; prostor_za_unos_vlasnik[fajl_INDEX] = klasa_Definicija; prostor_za_unos_dozvole[fajl_INDEX] = 짧은수(); prostor_za_unos_naziv[fajl_INDEX] = 상번호(); prostor_za_unos_TYPE[fajl_INDEX] = 상번호();
            ček_konstanta(prostor_za_unos_naziv[fajl_INDEX], 1); ček_konstanta(prostor_za_unos_TYPE[fajl_INDEX], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[prostor_za_unos_TYPE[fajl_INDEX]]; int oblast_kod = 서술형(읽기위치 + konstanta_SECOND_VALUE[prostor_za_unos_TYPE[fajl_INDEX]], false); 읽기위치 = 보존값;
            if ((prostor_za_unos_dozvole[fajl_INDEX] & 8) == 0) prostor_za_unos_položaj[fajl_INDEX] = klasa_prostor_za_unos_COUNT[klasa_Definicija]++;
            int atribut_podaci = 짧은수();
            for (int unutrašnje_spajanje_položaj = 0; unutrašnje_spajanje_položaj < atribut_podaci && !GRESKA; unutrašnje_spajanje_položaj++) {
                int naziv_konstanta = 상번호(), 유효길이 = cijeli_broj();
                if (Word_SMS(naziv_konstanta, "ConstantValue") && 유효길이 == 2) {
                    int podaci_VALUE = 상번호();
                    if (oblast_kod == 1 && ček_konstanta(podaci_VALUE, 3)) prostor_za_unos_podaci[fajl_INDEX] = 상가[podaci_VALUE];
                    else if (oblast_kod == 2 && ček_konstanta(podaci_VALUE, 8)) prostor_za_unos_podaci[fajl_INDEX] = konstanta_SMS(상가[podaci_VALUE]);
                } else 건너(유효길이);
            }
        }
        int stavka_COUNT = 짧은수();
        if (stavka_COUNT > 512 - metoda_COUNT) { neuspjeh_VALUE("method count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < stavka_COUNT && !GRESKA; Loop_INDEX++) {
            int 수 = metoda_COUNT++; metoda_vlasnik[수] = klasa_Definicija;
            metoda_pristup[수] = 짧은수(); metoda_naziv_SMS[수] = 상번호(); metoda_TYPE[수] = 상번호();
            ček_konstanta(metoda_naziv_SMS[수], 1); 서술읽기(수);
            if ((metoda_pristup[수] & 8) == 0) {
                if (metoda_argument_COUNT[수] == 16) { neuspjeh_VALUE("too many instance method arguments"); return; }
                for (int Poređenje_položaj = metoda_argument_COUNT[수]; Poređenje_položaj > 0; Poređenje_položaj--) metoda_argument_TYPE[수 * 16 + Poređenje_položaj] = metoda_argument_TYPE[수 * 16 + Poređenje_položaj - 1];
                metoda_argument_TYPE[수 * 16] = 2; metoda_argument_COUNT[수]++;
            }
            if ((metoda_pristup[수] & 0x100) != 0) neuspjeh_VALUE("user native method unsupported");
            if (Word_SMS(metoda_naziv_SMS[수], "<clinit>")) inicijalizirati_klasa_Definicija[klasa_Definicija] = 수 + 1;
            for (int 앞 = 0; 앞 < 수; 앞++) if (metoda_vlasnik[앞] == klasa_Definicija && 같은말(metoda_naziv_SMS[앞], metoda_naziv_SMS[수]) && 같은말(metoda_TYPE[앞], metoda_TYPE[수])) neuspjeh_VALUE("duplicate method");
            int atribut_COUNT = 짧은수();
            for (int atribut_VALUE = 0; atribut_VALUE < atribut_COUNT && !GRESKA; atribut_VALUE++) {
                int Naziv = 상번호(), dužina_VALUE = cijeli_broj(), Pokreni = 읽기위치;
                if (!isječak(Pokreni, dužina_VALUE)) { neuspjeh_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Naziv, "Code")) {
                    if (metoda_START[수] != 0) neuspjeh_VALUE("duplicate Code attribute");
                    metoda_snop[수] = 짧은수(); 함수지역[수] = 짧은수(); int kod_dužina = cijeli_broj();
                    if (metoda_snop[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < metoda_argument_COUNT[수]
                        || kod_dužina < 1 || kod_dužina > 8192) neuspjeh_VALUE("method memory limits exceeded");
                    metoda_START[수] = 읽기위치; 건너(kod_dužina); metoda_završiti[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { neuspjeh_VALUE("exception table limit"); return; }
                    for (int unutrašnje_spajanje_položaj = 0; unutrašnje_spajanje_položaj < 잡는수; unutrašnje_spajanje_položaj++) {
                        int greška_Reference = 잡기수++; 잡기함수[greška_Reference] = 수;
                        잡기시작[greška_Reference] = metoda_START[수] + 짧은수(); 잡기끝[greška_Reference] = metoda_START[수] + 짧은수();
                        잡기위치[greška_Reference] = metoda_START[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[greška_Reference] = 부호값 == 0 ? 0 : naziv_klase_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != Pokreni + dužina_VALUE) neuspjeh_VALUE("Code attribute size mismatch");
                } else 건너(dužina_VALUE);
            }
            if ((metoda_pristup[수] & 0x400) != 0) continue;
            if (metoda_START[수] == 0) neuspjeh_VALUE("missing Code attribute");
            int prostor_za_unos_unos = metoda_START[수];
            while (prostor_za_unos_unos < metoda_završiti[수] && !GRESKA) {
                int dužina_VALUE = 길이읽기(prostor_za_unos_unos, metoda_START[수], metoda_završiti[수]);
                if (dužina_VALUE == 0) { neuspjeh_VALUE("unsupported or truncated bytecode"); break; }
                경계[prostor_za_unos_unos] = 수 + 1; prostor_za_unos_unos += dužina_VALUE;
            }
            prostor_za_unos_unos = metoda_START[수];
            while (prostor_za_unos_unos < metoda_završiti[수] && !GRESKA) {
                int VALUE = Fajl[prostor_za_unos_unos];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) ček_odredište_VALUE(prostor_za_unos_unos + (short)(Fajl[prostor_za_unos_unos + 1] << 8 | Fajl[prostor_za_unos_unos + 2]), 수);
                if (VALUE == 200) ček_odredište_VALUE(prostor_za_unos_unos + položaj_cijeli_broj(prostor_za_unos_unos + 1), 수);
                if (VALUE == 170 || VALUE == 171) {
                    int 읽는자리 = prostor_za_unos_unos + 1; while ((읽는자리 - metoda_START[수]) % 4 != 0) 읽는자리++;
                    ček_odredište_VALUE(prostor_za_unos_unos + položaj_cijeli_broj(읽는자리), 수);
                    int unos_COUNT = VALUE == 170 ? položaj_cijeli_broj(읽는자리 + 8) - položaj_cijeli_broj(읽는자리 + 4) + 1 : položaj_cijeli_broj(읽는자리 + 4);
                    읽는자리 += VALUE == 170 ? 12 : 8;
                    for (int unutrašnje_spajanje_položaj = 0; unutrašnje_spajanje_položaj < unos_COUNT; unutrašnje_spajanje_položaj++) ček_odredište_VALUE(prostor_za_unos_unos + položaj_cijeli_broj(읽는자리 + unutrašnje_spajanje_položaj * (VALUE == 170 ? 4 : 8) + (VALUE == 170 ? 0 : 4)), 수);
                }
                prostor_za_unos_unos += 길이읽기(prostor_za_unos_unos, metoda_START[수], metoda_završiti[수]);
            }
            for (int unutrašnje_spajanje_položaj = 0; unutrašnje_spajanje_položaj < 잡기수; unutrašnje_spajanje_položaj++) if (잡기함수[unutrašnje_spajanje_položaj] == 수) {
                ček_odredište_VALUE(잡기시작[unutrašnje_spajanje_položaj], 수); ček_odredište_VALUE(잡기위치[unutrašnje_spajanje_položaj], 수);
                if (잡기끝[unutrašnje_spajanje_položaj] != metoda_završiti[수]) ček_odredište_VALUE(잡기끝[unutrašnje_spajanje_položaj], 수);
                if (잡기시작[unutrašnje_spajanje_položaj] >= 잡기끝[unutrašnje_spajanje_položaj]) neuspjeh_VALUE("invalid exception range");
            }
        }
        if (!GRESKA) 속성건너();
        if (읽기위치 != Veličina) neuspjeh_VALUE("extra class file data");
    }
    static int dodijeliti_Pohrana(int 종류, int dužina_VALUE) { return 새기억(종류, dužina_VALUE); }
    static boolean objekt_VALUE(int Reference, int 종류) {
        if (!객체유효(Reference)) return false;
        if (힙[Reference] != 종류) { neuspjeh_VALUE("object type mismatch"); return false; }
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
        if (vratiti_TYPE == 2) zaštititi_VALUE(operand_snop_VALUE[prostor_za_unos_unos]);
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
        if (kadar_INDEX % 32 == 31) { neuspjeh_VALUE("call stack limit (32)"); return; }
        int Dalje_stavka = kadar_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) lokalni_TYPE[Dalje_stavka * 128 + 수] = 0;
        for (int 수 = metoda_argument_COUNT[FUNCTION_VALUE] - 1; 수 >= 0; 수--) {
            lokalni_VALUE[Dalje_stavka * 128 + 수] = 빼기(metoda_argument_TYPE[FUNCTION_VALUE * 16 + 수]); lokalni_TYPE[Dalje_stavka * 128 + 수] = metoda_argument_TYPE[FUNCTION_VALUE * 16 + 수];
        }
        if (GRESKA) return;
        kadar_INDEX = Dalje_stavka; inicijalizirati_kadar[kadar_INDEX] = 0; kadar_metoda[kadar_INDEX] = FUNCTION_VALUE; kadar_položaj[kadar_INDEX] = metoda_START[FUNCTION_VALUE]; kadar_snop[kadar_INDEX] = 0;
    }
    static void vratiti_mjera(int TYPE_VALUE) {
        if (TYPE_VALUE != metoda_vratiti[kadar_metoda[kadar_INDEX]]) { neuspjeh_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        if (inicijalizirati_kadar[kadar_INDEX] != 0) klasa_Definicija_stanje[inicijalizirati_kadar[kadar_INDEX] - 1] = 2;
        if (틀잠금[kadar_INDEX] != 0) { 잠금풀기(틀잠금[kadar_INDEX]); 틀잠금[kadar_INDEX] = 0; }
        kadar_INDEX--; if (kadar_INDEX >= trenutno_nit * 32 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
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
                if (VALUE < 1) { neuspjeh_VALUE("invalid file stream path"); return; }
                tok_fajl_naziv[prostor_za_unos_unos] = VALUE;
            }
            tok_fajl_naziv[dužina_VALUE] = 0;
            int 서술자 = korisnik.파일서술자열기(tok_fajl_naziv, Ispis ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { neuspjeh_VALUE("FileNotFoundException: file open failed"); return; }
            힙[tok_VALUE + 2] = 서술자; 힙[tok_VALUE + 3] = 1;
            return;
        }
        if (Naredba != 182) { neuspjeh_VALUE("invalid file stream invocation"); return; }
        if ((Ispis && Word_SMS(Naziv, "write") || !Ispis && Word_SMS(Naziv, "read"))
            && (Word_SMS(format_VALUE, Ispis ? "([B)V" : "([B)I") || Word_SMS(format_VALUE, Ispis ? "([BII)V" : "([BII)I"))) {
            boolean isječak_VALUE = Word_SMS(format_VALUE, Ispis ? "([BII)V" : "([BII)I");
            int unos_COUNT = isječak_VALUE ? 빼기(1) : 0, 시작점 = isječak_VALUE ? 빼기(1) : 0, podaci_niz = 빼기(2), objekt_Reference = 빼기(2);
            if (!objekt_VALUE(podaci_niz, 20) || !objekt_VALUE(objekt_Reference, 종류)) return;
            if (!isječak_VALUE) unos_COUNT = 힙[podaci_niz + 1];
            if (시작점 < 0 || unos_COUNT < 0 || 시작점 > 힙[podaci_niz + 1] - unos_COUNT) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[objekt_Reference + 3] == 0 || 힙[objekt_Reference + 2] < 0) { neuspjeh_VALUE("IOException: stream closed"); return; }
            int 완료수 = 0;
            while (완료수 < unos_COUNT && !GRESKA) {
                int 반환값 = Ispis ? korisnik.파일한바이트쓰기(힙[objekt_Reference + 2], 힙[podaci_niz + 2 + 시작점 + 완료수]) : korisnik.파일한바이트읽기(힙[objekt_Reference + 2]);
                if (반환값 < 0) { neuspjeh_VALUE(Ispis ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!Ispis && 반환값 == 256) break;
                if (!Ispis) 힙[podaci_niz + 2 + 시작점 + 완료수] = (byte)반환값;
                완료수++;
            }
            if (!Ispis) 넣기(unos_COUNT != 0 && 완료수 == 0 ? -1 : 완료수, 1);
            return;
        }
        if (Ispis && Word_SMS(Naziv, "flush") && Word_SMS(format_VALUE, "()V")) { int objekt_Reference = 빼기(2); if (objekt_VALUE(objekt_Reference, 종류) && 힙[objekt_Reference + 2] < 0) neuspjeh_VALUE("IOException: stream closed"); return; }
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
            if (mjera < -1) neuspjeh_VALUE("IOException: read failed"); else 넣기(mjera == 256 ? -1 : mjera, 1);
        } else if (korisnik.파일한바이트쓰기(서술자, VALUE) != 1) neuspjeh_VALUE("IOException: write failed");
    }
    static void CALL_metoda(int INDEX, int Naredba) {
        if (INDEX <= 0 || INDEX >= konstanta_oznaka.length || (konstanta_oznaka[INDEX] != 10 && konstanta_oznaka[INDEX] != 11)) { neuspjeh_VALUE("invalid method reference"); return; }
        int vlasnik_VALUE = naziv_klase_SMS(상가[INDEX]), Naziv = Reference_naziv(konstanta_SECOND_VALUE[INDEX]), format_VALUE = Reference_TYPE(konstanta_SECOND_VALUE[INDEX]);
        if (GRESKA) return;
        if (기본호출(vlasnik_VALUE, Naziv, format_VALUE, Naredba)) return;
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
        int klasa_Definicija = FIND_klasa_Definicija(vlasnik_VALUE); if (klasa_Definicija < 0 || GRESKA) return;
        int fajl_INDEX = FIND_metoda(klasa_Definicija, Naziv, format_VALUE);
        if (fajl_INDEX < 0) {
            for (int kôd_znaka = klasa_Definicija, unos_COUNT = 0; kôd_znaka >= 0 && unos_COUNT < 16; unos_COUNT++, kôd_znaka = roditelj_klasa(kôd_znaka))
                if (Word_SMS(klasa_Definicija_roditelj[kôd_znaka], "java/lang/Thread")) { 가닥호출(Naziv, format_VALUE, Naredba); return; }
            neuspjeh_VALUE("NoSuchMethodError"); return;
        }
        if (((metoda_pristup[fajl_INDEX] & 8) != 0) != (Naredba == 184)) { neuspjeh_VALUE("method static/instance mismatch"); return; }
        if (Naredba == 184) { if (!inicijalizirati(metoda_vlasnik[fajl_INDEX], kadar_programska_naredba[kadar_INDEX])) return; }
        else {
            int 읽는자리 = kadar_snop[kadar_INDEX] - metoda_argument_COUNT[fajl_INDEX];
            if (읽는자리 < 0 || operand_snop_TYPE[kadar_INDEX * 128 + 읽는자리] != 2) { neuspjeh_VALUE("invalid method receiver"); return; }
            int objekt_Reference = operand_snop_VALUE[kadar_INDEX * 128 + 읽는자리];
            if (!객체유효(objekt_Reference)) return;
            if (힙[objekt_Reference] < 32 || !종포함(힙[objekt_Reference] - 32, vlasnik_VALUE)) { neuspjeh_VALUE("method receiver type mismatch"); return; }
            if (Naredba != 183) fajl_INDEX = FIND_metoda(힙[objekt_Reference] - 32, Naziv, format_VALUE);
        }
        if (fajl_INDEX < 0 || (metoda_pristup[fajl_INDEX] & 0x400) != 0) { neuspjeh_VALUE("AbstractMethodError"); return; }
        int 잠금참조 = 0;
        if ((metoda_pristup[fajl_INDEX] & 32) != 0) {
            if (Naredba == 184) { int kôd_znaka = metoda_vlasnik[fajl_INDEX]; if (종잠금[kôd_znaka] == 0) 종잠금[kôd_znaka] = dodijeliti_Pohrana(8, 0); 잠금참조 = 종잠금[kôd_znaka]; }
            else 잠금참조 = operand_snop_VALUE[kadar_INDEX * 128 + kadar_snop[kadar_INDEX] - metoda_argument_COUNT[fajl_INDEX]];
            if (!잠금얻기(잠금참조)) { if (!GRESKA) kadar_položaj[kadar_INDEX] = kadar_programska_naredba[kadar_INDEX]; return; }
        }
        호출(fajl_INDEX); if (!GRESKA) 틀잠금[kadar_INDEX] = 잠금참조;
    }
    static boolean 배열저장가능(int niz_Reference, int podaci_VALUE) {
        if (podaci_VALUE == 0 || niz_element[niz_Reference] == 0) return true;
        boolean 성공여부 = niz_element[niz_Reference] == -1 ? (podaci_VALUE > 0 && podaci_VALUE < 힙끝 && 힙[podaci_VALUE] == 1) : 맞는객체(podaci_VALUE, niz_element[niz_Reference]);
        if (!성공여부 && !GRESKA) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int niz_prostor_za_unos(int Reference, int indeks_VALUE, int TYPE_VALUE) {
        if (!objekt_VALUE(Reference, TYPE_VALUE)) return 0;
        if (indeks_VALUE < 0 || indeks_VALUE >= 힙[Reference + 1]) { neuspjeh_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return Reference + 2 + indeks_VALUE;
    }
    static void Izvrši_komanda() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (GRESKA) { if (던진객체 != 0) hvatište_izuzetak(); if (GRESKA || kadar_INDEX < trenutno_nit * 32) break; }
            if (kadar_INDEX < trenutno_nit * 32 || promijeniti_HTTP_zahtjev || --조각 == 0) { if (!SWITCH_nit()) break; 조각 = 100; }
            if (kadar_INDEX == 0 && klasa_Definicija_stanje[unos_klasa_Definicija] != 2 && !inicijalizirati(unos_klasa_Definicija, kadar_položaj[kadar_INDEX])) continue;
            if (kadar_INDEX == trenutno_nit * 32 && trenutno_nit != 0 && (metoda_pristup[kadar_metoda[kadar_INDEX]] & 32) != 0 && 틀잠금[kadar_INDEX] == 0) {
                int objekt_Reference = nit_cilj[trenutno_nit]; if (!잠금얻기(objekt_Reference)) { if (GRESKA) break; continue; } 틀잠금[kadar_INDEX] = objekt_Reference;
            }
            잠시수 = 0;
            if (--남음 == 0) { neuspjeh_VALUE("instruction limit (500000)"); break; }
            int Pokreni = kadar_položaj[kadar_INDEX]; kadar_programska_naredba[kadar_INDEX] = Pokreni; int VALUE = 명바();
            if (GRESKA) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = metoda_vlasnik[kadar_metoda[kadar_INDEX]] * 512 + (VALUE == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= konstanta_oznaka.length) neuspjeh_VALUE("invalid ldc constant");
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
            if (VALUE == 46 || VALUE >= 50 && VALUE <= 53) {
                int unos_položaj = 빼기(1), objekt_Reference = 빼기(2), oblast_kod = VALUE == 46 ? 2 : VALUE == 50 ? 3 : VALUE == 51 ? 20 : VALUE == 52 ? 22 : 23;
                if (VALUE == 51 && objekt_Reference > 0 && objekt_Reference < 힙끝 && 힙[objekt_Reference] == 21) oblast_kod = 21;
                int 읽는자리 = niz_prostor_za_unos(objekt_Reference, unos_položaj, oblast_kod); if (!GRESKA) 넣기(힙[읽는자리], VALUE == 50 ? 2 : 1); continue;
            }
            if (VALUE == 79 || VALUE >= 83 && VALUE <= 86) {
                int unos_Reference = 빼기(VALUE == 83 ? 2 : 1), unos_položaj = 빼기(1), objekt_Reference = 빼기(2), oblast_kod = VALUE == 79 ? 2 : VALUE == 83 ? 3 : VALUE == 84 ? 20 : VALUE == 85 ? 22 : 23;
                if (VALUE == 84 && objekt_Reference > 0 && objekt_Reference < 힙끝 && 힙[objekt_Reference] == 21) oblast_kod = 21;
                int 읽는자리 = niz_prostor_za_unos(objekt_Reference, unos_položaj, oblast_kod);
                if (!GRESKA && oblast_kod == 3 && !배열저장가능(objekt_Reference, unos_Reference)) continue;
                if (!GRESKA) 힙[읽는자리] = oblast_kod == 20 ? (byte)unos_Reference : oblast_kod == 21 ? unos_Reference & 1 : oblast_kod == 22 ? (char)unos_Reference : oblast_kod == 23 ? (short)unos_Reference : unos_Reference;
                continue;
            }
            if (VALUE >= 87 && VALUE <= 95) { snop_programska_naredba(VALUE); continue; }
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
            if (VALUE >= 178 && VALUE <= 181) { 필드호출(명상수(), VALUE, Pokreni); continue; }
            if (VALUE >= 182 && VALUE <= 185) {
                int 부호값 = 명상수();
                if (VALUE == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { neuspjeh_VALUE("invalid invokeinterface operands"); continue; } }
                CALL_metoda(부호값, VALUE); continue;
            }
            if (VALUE == 187) { 새객체(naziv_klase_SMS(명상수()), Pokreni); continue; }
            if (VALUE == 188 || VALUE == 189) {
                int oblast_kod = 3, komponenta = 0;
                if (VALUE == 188) { int 임시값 = 명바(); oblast_kod = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else komponenta = naziv_klase_SMS(명상수());
                if (oblast_kod == 0) { neuspjeh_VALUE("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), objekt_Reference = dodijeliti_Pohrana(oblast_kod, 유효길이); if (!GRESKA) niz_element[objekt_Reference] = komponenta; 넣기(objekt_Reference, 2); continue;
            }
            if (VALUE == 190) {
                int objekt_Reference = 빼기(2);
                if (객체유효(objekt_Reference)) { int Poređenje_položaj = 힙[objekt_Reference]; if (Poređenje_položaj != 2 && Poređenje_položaj != 3 && (Poređenje_položaj < 20 || Poređenje_položaj > 23)) neuspjeh_VALUE("not an array"); else 넣기(힙[objekt_Reference + 1], 1); }
                continue;
            }
            if (VALUE == 191) {
                int objekt_Reference = 빼기(2); if (객체유효(objekt_Reference)) { if (힙[objekt_Reference] != 9) neuspjeh_VALUE("athrow requires supported Throwable"); else { 던진객체 = objekt_Reference; GRESKA = true; } }
                continue;
            }
            if (VALUE == 192 || VALUE == 193) {
                int naziv_konstanta = naziv_klase_SMS(명상수()), objekt_Reference = 빼기(2); boolean MATCH = 맞는객체(objekt_Reference, naziv_konstanta);
                if (VALUE == 193) 넣기(objekt_Reference != 0 && MATCH ? 1 : 0, 1);
                else { if (!MATCH && !GRESKA) neuspjeh_VALUE("ClassCastException"); 넣기(objekt_Reference, 2); }
                continue;
            }
            if (VALUE == 170 || VALUE == 171) {
                int 읽는자리 = Pokreni + 1, fajl_INDEX = kadar_metoda[kadar_INDEX], ključ_Reference = 빼기(1);
                while ((읽는자리 - metoda_START[fajl_INDEX]) % 4 != 0) 읽는자리++;
                int cilj_adresa = položaj_cijeli_broj(읽는자리);
                if (VALUE == 170) { int 낮은값 = položaj_cijeli_broj(읽는자리 + 4), 높은값 = položaj_cijeli_broj(읽는자리 + 8); if (ključ_Reference >= 낮은값 && ključ_Reference <= 높은값) cilj_adresa = položaj_cijeli_broj(읽는자리 + 12 + (ključ_Reference - 낮은값) * 4); }
                else { int 총수 = položaj_cijeli_broj(읽는자리 + 4); for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) if (položaj_cijeli_broj(읽는자리 + 8 + Loop_INDEX * 8) == ključ_Reference) cilj_adresa = položaj_cijeli_broj(읽는자리 + 12 + Loop_INDEX * 8); }
                pomaći_VALUE(Pokreni + cilj_adresa); continue;
            }
            if (VALUE == 200) { pomaći_VALUE(Pokreni + položaj_cijeli_broj(Pokreni + 1)); continue; }
            if (VALUE == 194 || VALUE == 195) {
                int objekt_Reference = 빼기(2);
                if (VALUE == 195) 잠금풀기(objekt_Reference);
                else if (!잠금얻기(objekt_Reference) && !GRESKA) { 넣기(objekt_Reference, 2); kadar_položaj[kadar_INDEX] = Pokreni; }
                continue;
            }
            if (VALUE == 196) {
                int komanda_kod = 명바(), unos_položaj = 명짧();
                if (komanda_kod == 21 || komanda_kod == 25) 지역읽기(unos_položaj, komanda_kod == 21 ? 1 : 2);
                else if (komanda_kod == 54 || komanda_kod == 58) pisati_lokalni(unos_položaj, komanda_kod == 54 ? 1 : 2);
                else if (komanda_kod == 132) { int DELTA_VALUE = (short)명짧(); 지역읽기(unos_položaj, 1); 넣기(빼기(1) + DELTA_VALUE, 1); pisati_lokalni(unos_položaj, 1); }
                else neuspjeh_VALUE("unsupported wide opcode");
                continue;
            }
            neuspjeh_VALUE("unsupported bytecode");
        }
    }
    static int FIND_klasa_Definicija(int Naziv) {
        for (int Loop_INDEX = 0; Loop_INDEX < klasa_Definicija_COUNT; Loop_INDEX++) if (klasa_Definicija_naziv[Loop_INDEX] != 0 && 같은말(klasa_Definicija_naziv[Loop_INDEX], Naziv)) return Loop_INDEX;
        return učitati_klasa_Definicija(konstanta_SMS(Naziv));
    }
    static int učitati_klasa_Definicija(int naziv_string) {
        if (!objekt_VALUE(naziv_string, 1)) return -1;
        int dužina_VALUE = 힙[naziv_string + 1];
        if (dužina_VALUE < 1 || dužina_VALUE > 505 || klasa_Definicija_COUNT == 16) { neuspjeh_VALUE("class name/count limit"); return -1; }
        for (int Loop_INDEX = 0; Loop_INDEX < dužina_VALUE; Loop_INDEX++) { int kôd_znaka = 힙[naziv_string + 2 + Loop_INDEX]; fajl_naziv_SMS[Loop_INDEX] = kôd_znaka == '/' ? '.' : kôd_znaka; }
        fajl_naziv_SMS[dužina_VALUE] = '.'; fajl_naziv_SMS[dužina_VALUE + 1] = 'c'; fajl_naziv_SMS[dužina_VALUE + 2] = 'l'; fajl_naziv_SMS[dužina_VALUE + 3] = 'a'; fajl_naziv_SMS[dužina_VALUE + 4] = 's'; fajl_naziv_SMS[dužina_VALUE + 5] = 's'; fajl_naziv_SMS[dužina_VALUE + 6] = 0;
        int Veličina = korisnik.파일읽기(fajl_naziv_SMS, 임시파일);
        if (Veličina < 0) { neuspjeh_VALUE("ClassNotFoundException"); return -1; }
        int klasa_Definicija = klasa_Definicija_COUNT++; klasa_Definicija_podesiti_veličinu[klasa_Definicija] = Veličina;
        for (int Loop_INDEX = 0; Loop_INDEX < Veličina; Loop_INDEX++) Fajl[klasa_Definicija * 16384 + Loop_INDEX] = 임시파일[Loop_INDEX];
        클래스읽기(klasa_Definicija); if (GRESKA) return -1;
        int stvaran_podaci = konstanta_SMS(klasa_Definicija_naziv[klasa_Definicija]);
        if (!글같음(stvaran_podaci, naziv_string, true)) { neuspjeh_VALUE("class name does not match file"); return -1; }
        int roditelj_VALUE = klasa_Definicija_roditelj[klasa_Definicija];
        if (roditelj_VALUE != 0 && !Word_SMS(roditelj_VALUE, "java/lang/Object") && !Word_SMS(roditelj_VALUE, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = FIND_klasa_Definicija(roditelj_VALUE);
            if (GRESKA || 위 < 0) return -1;
            int 읽는자리 = 위, faza_COUNT = 0;
            while (읽는자리 >= 0 && faza_COUNT++ < 16) {
                if (읽는자리 == klasa_Definicija) { neuspjeh_VALUE("cyclic inheritance"); return -1; }
                읽는자리 = roditelj_klasa(읽는자리);
            }
            int 시작변위 = klasa_prostor_za_unos_COUNT[위];
            for (int fajl_INDEX = 0; fajl_INDEX < prostor_za_unos_COUNT; fajl_INDEX++) if (prostor_za_unos_vlasnik[fajl_INDEX] == klasa_Definicija && (prostor_za_unos_dozvole[fajl_INDEX] & 8) == 0) prostor_za_unos_položaj[fajl_INDEX] += 시작변위;
            klasa_prostor_za_unos_COUNT[klasa_Definicija] += 시작변위;
        }
        return klasa_Definicija;
    }
    static int roditelj_klasa(int klasa_Definicija) {
        int Naziv = klasa_Definicija_roditelj[klasa_Definicija];
        for (int Loop_INDEX = 0; Loop_INDEX < klasa_Definicija_COUNT; Loop_INDEX++) if (Naziv != 0 && klasa_Definicija_naziv[Loop_INDEX] != 0 && 같은말(klasa_Definicija_naziv[Loop_INDEX], Naziv)) return Loop_INDEX;
        return -1;
    }
    static int FIND_metoda(int klasa_Definicija, int Naziv, int format_VALUE) {
        for (int 깊이 = 0; klasa_Definicija >= 0 && 깊이 < 16; 깊이++, klasa_Definicija = roditelj_klasa(klasa_Definicija)) {
            for (int Loop_INDEX = 0; Loop_INDEX < metoda_COUNT; Loop_INDEX++) if (metoda_vlasnik[Loop_INDEX] == klasa_Definicija && 같은말(metoda_naziv_SMS[Loop_INDEX], Naziv) && 같은말(metoda_TYPE[Loop_INDEX], format_VALUE)) return Loop_INDEX;
        }
        return -1;
    }
    static int naziv_metoda(int klasa_Definicija, String Naziv, String format_VALUE) {
        for (int 깊이 = 0; klasa_Definicija >= 0 && 깊이 < 16; 깊이++, klasa_Definicija = roditelj_klasa(klasa_Definicija))
            for (int Loop_INDEX = 0; Loop_INDEX < metoda_COUNT; Loop_INDEX++) if (metoda_vlasnik[Loop_INDEX] == klasa_Definicija && Word_SMS(metoda_naziv_SMS[Loop_INDEX], Naziv) && Word_SMS(metoda_TYPE[Loop_INDEX], format_VALUE)) return Loop_INDEX;
        return -1;
    }
    static int 형종류(int Naziv) { return Fajl[상가[Naziv]] == 'L' || Fajl[상가[Naziv]] == '[' ? 2 : 1; }
    static boolean inicijalizirati(int klasa_Definicija, int komanda_START) {
        if (klasa_Definicija < 0 || GRESKA) return false;
        if (klasa_Definicija_stanje[klasa_Definicija] == 3) { neuspjeh_VALUE("NoClassDefFoundError: initialization failed"); return false; }
        if (klasa_Definicija_stanje[klasa_Definicija] == 1 && klasa_nit[klasa_Definicija] != trenutno_nit) { kadar_položaj[kadar_INDEX] = komanda_START; promijeniti_HTTP_zahtjev = true; return false; }
        if (klasa_Definicija_stanje[klasa_Definicija] != 0) return true;
        int 위 = roditelj_klasa(klasa_Definicija);
        if (위 >= 0 && !inicijalizirati(위, komanda_START)) return false;
        klasa_Definicija_stanje[klasa_Definicija] = 1; klasa_nit[klasa_Definicija] = trenutno_nit;
        if (inicijalizirati_klasa_Definicija[klasa_Definicija] != 0) {
            kadar_položaj[kadar_INDEX] = komanda_START;
            호출(inicijalizirati_klasa_Definicija[klasa_Definicija] - 1); if (!GRESKA) inicijalizirati_kadar[kadar_INDEX] = klasa_Definicija + 1;
            return false;
        }
        klasa_Definicija_stanje[klasa_Definicija] = 2; return true;
    }
    static void 필드호출(int INDEX, int Naredba, int Pokreni) {
        if (!ček_konstanta(INDEX, 9)) return;
        int vlasnik_VALUE = naziv_klase_SMS(상가[INDEX]), Naziv = Reference_naziv(konstanta_SECOND_VALUE[INDEX]), format_VALUE = Reference_TYPE(konstanta_SECOND_VALUE[INDEX]);
        if (Word_SMS(vlasnik_VALUE, "java/lang/System") && (Word_SMS(Naziv, "out") || Word_SMS(Naziv, "err")) && Word_SMS(format_VALUE, "Ljava/io/PrintStream;") && Naredba == 178) { 넣기(-1, 2); return; }
        int klasa_Definicija = FIND_klasa_Definicija(vlasnik_VALUE); if (klasa_Definicija < 0 || GRESKA) return;
        int 찾음 = -1;
        for (int 읽는자리 = klasa_Definicija, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = roditelj_klasa(읽는자리))
            for (int fajl_INDEX = 0; fajl_INDEX < prostor_za_unos_COUNT; fajl_INDEX++) if (prostor_za_unos_vlasnik[fajl_INDEX] == 읽는자리 && 같은말(prostor_za_unos_naziv[fajl_INDEX], Naziv) && 같은말(prostor_za_unos_TYPE[fajl_INDEX], format_VALUE)) 찾음 = fajl_INDEX;
        if (찾음 < 0) { neuspjeh_VALUE("NoSuchFieldError"); return; }
        boolean statični_VALUE = Naredba == 178 || Naredba == 179;
        if (statični_VALUE != ((prostor_za_unos_dozvole[찾음] & 8) != 0)) { neuspjeh_VALUE("field static/instance mismatch"); return; }
        if (statični_VALUE && !inicijalizirati(prostor_za_unos_vlasnik[찾음], Pokreni)) return;
        int TYPE_VALUE = 형종류(format_VALUE), VALUE = 0;
        if (Naredba == 179 || Naredba == 181) VALUE = 빼기(TYPE_VALUE);
        if (statični_VALUE) { if (Naredba == 178) 넣기(prostor_za_unos_podaci[찾음], TYPE_VALUE); else if (!GRESKA) prostor_za_unos_podaci[찾음] = VALUE; return; }
        int objekt_Reference = 빼기(2);
        if (!객체유효(objekt_Reference)) return;
        if (힙[objekt_Reference] < 32 || !종포함(힙[objekt_Reference] - 32, vlasnik_VALUE)) { neuspjeh_VALUE("field receiver type mismatch"); return; }
        int 보관칸 = objekt_Reference + 2 + prostor_za_unos_položaj[찾음];
        if (Naredba == 180) 넣기(힙[보관칸], TYPE_VALUE);
        else if (!GRESKA) { 힙[보관칸] = VALUE; 힙참조[보관칸] = TYPE_VALUE == 2 ? 1 : 0; }
    }
    static boolean 종포함(int klasa_Definicija, int Naziv) {
        for (int 중첩깊이 = 0; klasa_Definicija >= 0 && 중첩깊이 < 16; 중첩깊이++, klasa_Definicija = roditelj_klasa(klasa_Definicija)) {
            if (같은말(klasa_Definicija_naziv[klasa_Definicija], Naziv) || (klasa_Definicija_roditelj[klasa_Definicija] != 0 && 같은말(klasa_Definicija_roditelj[klasa_Definicija], Naziv))) return true;
            for (int unutrašnje_spajanje_položaj = 0; unutrašnje_spajanje_položaj < klasa_interfejs_COUNT[klasa_Definicija]; unutrašnje_spajanje_položaj++) if (같은말(klasa_interfejs[klasa_Definicija * 16 + unutrašnje_spajanje_položaj], Naziv)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int bajt_podaci, boolean Putanja) {
        if (첫값 == bajt_podaci) return true;
        if (첫값 <= 0 || bajt_podaci <= 0 || 힙[첫값] != 1 || 힙[bajt_podaci] != 1 || 힙[첫값 + 1] != 힙[bajt_podaci + 1]) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) {
            int koordinata_x = 힙[첫값 + 2 + Loop_INDEX], Y_koordinata = 힙[bajt_podaci + 2 + Loop_INDEX];
            if (Putanja) { if (koordinata_x == '.') koordinata_x = '/'; if (Y_koordinata == '.') Y_koordinata = '/'; }
            if (koordinata_x != Y_koordinata) return false;
        }
        return true;
    }
    static boolean 객체유효(int objekt_Reference) {
        if (objekt_Reference == 0) { neuspjeh_VALUE("NullPointerException"); return false; }
        if (objekt_Reference < 1 || objekt_Reference >= 힙끝 || 힙폭[objekt_Reference] < 2 || 힙[objekt_Reference] == 0) { neuspjeh_VALUE("invalid object reference"); return false; }
        return true;
    }
    static void zaštititi_VALUE(int objekt_Reference) {
        if (objekt_Reference > 0 && objekt_Reference < 힙끝 && 힙폭[objekt_Reference] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = objekt_Reference;
    }
    static void program_VALUE(int objekt_Reference) {
        if (objekt_Reference > 0 && objekt_Reference < 힙끝 && 힙폭[objekt_Reference] >= 2 && 힙[objekt_Reference] != 0 && 힙표시[objekt_Reference] == 0) {
            힙표시[objekt_Reference] = 1; 표시대기[ekran_COUNT++] = objekt_Reference;
        }
    }
    static void 수거() {
        ekran_COUNT = 0; Kolekcija_COUNT++;
        for (int ček_položaj = 1; ček_položaj < 힙끝; ček_položaj += 힙폭[ček_položaj]) 힙표시[ček_položaj] = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < string_Reference.length; Loop_INDEX++) program_VALUE(string_Reference[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < prostor_za_unos_COUNT; Loop_INDEX++) if ((prostor_za_unos_dozvole[Loop_INDEX] & 8) != 0 && 형종류(prostor_za_unos_TYPE[Loop_INDEX]) == 2) program_VALUE(prostor_za_unos_podaci[Loop_INDEX]);
        for (int 임시값 = 0; 임시값 < nit_COUNT; 임시값++) {
            program_VALUE(nit_objekt[임시값]); program_VALUE(nit_cilj[임시값]);
            int 꼭대기자리 = 임시값 == trenutno_nit ? kadar_INDEX : nit_kadar[임시값];
            for (int fajl_INDEX = 임시값 * 32; fajl_INDEX <= 꼭대기자리; fajl_INDEX++) {
                for (int unutrašnje_spajanje_položaj = 0; unutrašnje_spajanje_položaj < 함수지역[kadar_metoda[fajl_INDEX]]; unutrašnje_spajanje_položaj++) if (lokalni_TYPE[fajl_INDEX * 128 + unutrašnje_spajanje_položaj] == 2) program_VALUE(lokalni_VALUE[fajl_INDEX * 128 + unutrašnje_spajanje_položaj]);
                for (int unutrašnje_spajanje_položaj = 0; unutrašnje_spajanje_položaj < kadar_snop[fajl_INDEX]; unutrašnje_spajanje_položaj++) if (operand_snop_TYPE[fajl_INDEX * 128 + unutrašnje_spajanje_položaj] == 2) program_VALUE(operand_snop_VALUE[fajl_INDEX * 128 + unutrašnje_spajanje_položaj]);
            }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 화면참조.length; Loop_INDEX++) program_VALUE(화면참조[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 나중수; Loop_INDEX++) program_VALUE(나중실행[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Store_cijeli_broj.length; Loop_INDEX++) program_VALUE(Store_cijeli_broj[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < klasa_Definicija_COUNT; Loop_INDEX++) program_VALUE(종잠금[Loop_INDEX]);
        for (int ček_položaj = 1; ček_položaj < 힙끝; ček_položaj += 힙폭[ček_položaj]) if (잠금깊이[ček_položaj] > 0) program_VALUE(ček_položaj);
        program_VALUE(던진객체);
        for (int Loop_INDEX = 0; Loop_INDEX < 잠시수; Loop_INDEX++) program_VALUE(잠시참조[Loop_INDEX]);
        while (ekran_COUNT > 0) {
            int objekt_Reference = 표시대기[--ekran_COUNT], oblast_kod = 힙[objekt_Reference];
            for (int Loop_INDEX = objekt_Reference + 2; Loop_INDEX < objekt_Reference + 힙폭[objekt_Reference]; Loop_INDEX++) if (oblast_kod == 3 || oblast_kod == 4 || 힙참조[Loop_INDEX] != 0) program_VALUE(힙[Loop_INDEX]);
        }
        for (int ček_položaj = 1; ček_položaj < 힙끝; ček_položaj += 힙폭[ček_položaj]) if (힙표시[ček_položaj] == 0) 힙[ček_položaj] = 0;
        for (int ček_položaj = 1; ček_položaj < 힙끝; ček_položaj += 힙폭[ček_položaj]) if (힙[ček_položaj] == 0) {
            while (ček_položaj + 힙폭[ček_položaj] < 힙끝 && 힙[ček_položaj + 힙폭[ček_položaj]] == 0) { int Dalje_položaj = ček_položaj + 힙폭[ček_položaj]; 힙폭[ček_položaj] += 힙폭[Dalje_položaj]; 힙폭[Dalje_položaj] = 0; }
            if (ček_položaj + 힙폭[ček_položaj] == 힙끝) { 힙끝 = ček_položaj; break; }
        }
    }
    static int 새기억(int 종류, int dužina_VALUE) {
        if (dužina_VALUE < 0) { neuspjeh_VALUE("NegativeArraySizeException"); return 0; }
        if (dužina_VALUE > 힙.length - 3) { neuspjeh_VALUE("object heap exhausted"); return 0; }
        int 필요수 = dužina_VALUE + 2, objekt_Reference = 0;
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
        if (objekt_Reference == 0) { neuspjeh_VALUE("object heap exhausted"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < 필요수; Loop_INDEX++) { 힙[objekt_Reference + Loop_INDEX] = 0; 힙참조[objekt_Reference + Loop_INDEX] = 0; 힙폭[objekt_Reference + Loop_INDEX] = 0; }
        niz_element[objekt_Reference] = 0;
        힙폭[objekt_Reference] = 필요수; 힙[objekt_Reference] = 종류; 힙[objekt_Reference + 1] = dužina_VALUE; zaštititi_VALUE(objekt_Reference); return objekt_Reference;
    }
    static int izuzetak_klasa(String naziv_konstanta) {
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
    static int izuzetak_konstanta(int Naziv) {
        for (int Loop_INDEX = 1; Loop_INDEX <= 41; Loop_INDEX++) if (Word_SMS(Naziv, izuzetak_naziv(Loop_INDEX))) return Loop_INDEX;
        return 0;
    }
    static String izuzetak_naziv(int račun_VALUE) {
        if (račun_VALUE == 40) return "java/lang/InterruptedException";
        if (račun_VALUE == 41) return "한국어/자체/대기중단예외";
        if (račun_VALUE == 39) return "java/net/SocketException";
        if (račun_VALUE == 20) return "한국어/자체/izuzetak";
        if (račun_VALUE == 21) return "한국어/자체/실행예외";
        if (račun_VALUE == 22) return "한국어/자체/U_I_izuzetak";
        if (račun_VALUE == 23) return "한국어/자체/čekaj_TIMEOUT_izuzetak";
        if (račun_VALUE == 24) return "한국어/자체/adresa_LOOKUP_izuzetak";
        if (račun_VALUE == 25) return "한국어/자체/파일없음예외";
        if (račun_VALUE == 26) return "한국어/자체/통신예외";
        if (račun_VALUE == 27) return "한국어/자체/nevažeće_argument_izuzetak";
        if (račun_VALUE == 28) return "한국어/자체/숫자형식예외";
        if (račun_VALUE == 29) return "한국어/자체/범위예외";
        if (račun_VALUE == 30) return "한국어/자체/배열범위예외";
        if (račun_VALUE == 31) return "한국어/자체/문자열범위예외";
        if (račun_VALUE == 32) return "한국어/자체/NULL_Reference_izuzetak";
        if (račun_VALUE == 33) return "한국어/자체/산술예외";
        if (račun_VALUE == 34) return "한국어/자체/stanje_izuzetak";
        if (račun_VALUE == 35) return "한국어/자체/TYPE_Emitiranje_izuzetak";
        if (račun_VALUE == 36) return "한국어/자체/음수배열크기예외";
        if (račun_VALUE == 37) return "한국어/자체/niz_Store_neuspjeh";
        if (račun_VALUE == 38) return "한국어/자체/nit_stanje_izuzetak";
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
    static int izuzetak_roditelj(int račun_VALUE) {
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
    static boolean 예외포함(int stvaran_VALUE, int 요구값) {
        for (int 깊이 = 0; stvaran_VALUE != 0 && 깊이 < 16; 깊이++, stvaran_VALUE = izuzetak_roditelj(stvaran_VALUE))
            if (stvaran_VALUE == 요구값) return true;
        return false;
    }
    static void 예외던짐(int račun_VALUE, String Pročitaj_me_Reference) {
        int objekt_Reference = 새기억(9, 2); if (GRESKA) return;
        힙[objekt_Reference + 2] = račun_VALUE; 힙[objekt_Reference + 3] = organizator_znak(Pročitaj_me_Reference); 힙참조[objekt_Reference + 3] = 1;
        던진객체 = objekt_Reference; GRESKA = true;
    }
    static boolean 맞는객체(int objekt_Reference, int Naziv) {
        if (objekt_Reference == 0) return true;
        if (!객체유효(objekt_Reference)) return false;
        int oblast_kod = 힙[objekt_Reference];
        if (Word_SMS(Naziv, "java/lang/Object")) return true;
        if (oblast_kod >= 32) return 종포함(oblast_kod - 32, Naziv);
        if (oblast_kod == 9) { int cilj_adresa = izuzetak_konstanta(Naziv); return cilj_adresa != 0 && 예외포함(힙[objekt_Reference + 2], cilj_adresa); }
        if (oblast_kod == 1) return Word_SMS(Naziv, "java/lang/String") || Word_SMS(Naziv, "java/lang/CharSequence");
        if (oblast_kod == 4) return Word_SMS(Naziv, "java/lang/StringBuilder") || Word_SMS(Naziv, "java/lang/CharSequence");
        if (oblast_kod == 10) return Word_SMS(Naziv, "java/util/ArrayList") || Word_SMS(Naziv, "java/util/List");
        if (oblast_kod == 11) return Word_SMS(Naziv, "java/util/HashMap") || Word_SMS(Naziv, "java/util/Map");
        if (oblast_kod == 12) return Word_SMS(Naziv, "java/lang/Integer") || Word_SMS(Naziv, "java/lang/Number");
        if (oblast_kod >= 24 && oblast_kod <= 28 && 힙[objekt_Reference + 13] != 0) return 한국어화면종(Naziv) == oblast_kod || Word_SMS(Naziv, "한국어/자체/화면구성요소");
        if (oblast_kod >= 24 && oblast_kod <= 28) return (한국어화면종(Naziv) == 0 && 화면종(Naziv) == oblast_kod) || Word_SMS(Naziv, "java/awt/Component") || Word_SMS(Naziv, "java/awt/Container") || Word_SMS(Naziv, "javax/swing/JComponent");
        if (oblast_kod == 29) return Word_SMS(Naziv, 힙[objekt_Reference + 3] != 0 ? "한국어/자체/동작알림" : "java/awt/event/ActionEvent");
        if (oblast_kod == 30) return Word_SMS(Naziv, "java/awt/FlowLayout") || Word_SMS(Naziv, "java/awt/LayoutManager");
        if (oblast_kod == 17) return Word_SMS(Naziv, "java/net/Socket");
        if (oblast_kod == 18) return Word_SMS(Naziv, "java/net/ServerSocket");
        if (oblast_kod == 19) return Word_SMS(Naziv, 힙[objekt_Reference + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (oblast_kod == 14) return Word_SMS(Naziv, "java/net/InetAddress");
        if (oblast_kod == 15) return Word_SMS(Naziv, "java/net/DatagramSocket");
        if (oblast_kod == 16) return Word_SMS(Naziv, "java/net/DatagramPacket");
        if (oblast_kod == 13) return Word_SMS(Naziv, 힙[objekt_Reference + 3] != 0 ? "한국어/자체/작업가닥" : "java/lang/Thread");
        if (oblast_kod == 2) return Word_SMS(Naziv, "[I"); if (oblast_kod == 20) return Word_SMS(Naziv, "[B"); if (oblast_kod == 21) return Word_SMS(Naziv, "[Z");
        if (oblast_kod == 22) return Word_SMS(Naziv, "[C"); if (oblast_kod == 23) return Word_SMS(Naziv, "[S");
        if (oblast_kod != 3) return false;
        if (Word_SMS(Naziv, "[Ljava/lang/Object;")) return true;
        int komponenta = niz_element[objekt_Reference];
        if (komponenta == -1) return Word_SMS(Naziv, "[Ljava/lang/String;") || Word_SMS(Naziv, "[Ljava/lang/CharSequence;");
        if (komponenta == 0) return false;
        if (배열종비교(komponenta, Naziv)) return true;
        if ((Word_SMS(komponenta, "java/lang/String") || Word_SMS(komponenta, "java/lang/StringBuilder")) && Word_SMS(Naziv, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDEX = 0; Loop_INDEX < klasa_Definicija_COUNT; Loop_INDEX++) if (같은말(klasa_Definicija_naziv[Loop_INDEX], komponenta)) {
            for (int kôd_znaka = Loop_INDEX, 중첩깊이 = 0; kôd_znaka >= 0 && 중첩깊이 < 16; 중첩깊이++, kôd_znaka = roditelj_klasa(kôd_znaka)) {
                if (배열종비교(klasa_Definicija_roditelj[kôd_znaka], Naziv)) return true;
                for (int unutrašnje_spajanje_položaj = 0; unutrašnje_spajanje_položaj < klasa_interfejs_COUNT[kôd_znaka]; unutrašnje_spajanje_položaj++) if (배열종비교(klasa_interfejs[kôd_znaka * 16 + unutrašnje_spajanje_položaj], Naziv)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int naziv_konstanta, int 형식참조) {
        int ček_položaj = 상가[형식참조], unos_COUNT = konstanta_SECOND_VALUE[형식참조];
        if (naziv_konstanta == 0 || unos_COUNT < 4 || Fajl[ček_položaj] != '[' || Fajl[ček_položaj + 1] != 'L' || Fajl[ček_položaj + unos_COUNT - 1] != ';' || konstanta_SECOND_VALUE[naziv_konstanta] != unos_COUNT - 3) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < unos_COUNT - 3; Loop_INDEX++) if (Fajl[상가[naziv_konstanta] + Loop_INDEX] != Fajl[ček_položaj + 2 + Loop_INDEX]) return false;
        return true;
    }
    static void hvatište_izuzetak() {
        if (던진객체 == 0) return;
        GRESKA = false;
        while (kadar_INDEX >= trenutno_nit * 32) {
            int fajl_INDEX = kadar_metoda[kadar_INDEX], 읽는자리 = kadar_programska_naredba[kadar_INDEX];
            for (int Loop_INDEX = 0; Loop_INDEX < 잡기수; Loop_INDEX++) if (잡기함수[Loop_INDEX] == fajl_INDEX && 읽는자리 >= 잡기시작[Loop_INDEX] && 읽는자리 < 잡기끝[Loop_INDEX]
                && (잡기종[Loop_INDEX] == 0 || 맞는객체(던진객체, 잡기종[Loop_INDEX]))) {
                kadar_položaj[kadar_INDEX] = 잡기위치[Loop_INDEX]; kadar_snop[kadar_INDEX] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (inicijalizirati_kadar[kadar_INDEX] != 0) klasa_Definicija_stanje[inicijalizirati_kadar[kadar_INDEX] - 1] = 3;
            if (틀잠금[kadar_INDEX] != 0) { 잠금풀기(틀잠금[kadar_INDEX]); 틀잠금[kadar_INDEX] = 0; }
            kadar_INDEX--;
        }
        korisnik.Piši("Uncaught ");
        if (힙[던진객체] == 9) { korisnik.Piši(izuzetak_naziv(힙[던진객체 + 2])); korisnik.Piši(": "); pisati_SMS(힙[던진객체 + 3]); }
        else korisnik.Piši("user exception");
        korisnik.pisati_znak_VALUE(10); 던진객체 = 0; GRESKA = true;
    }
    // 이 JVM의 operand_snop 항목은 trenutno_stavka category-1(int/reference)만 허용한다.
    static void snop_programska_naredba(int komanda_kod) {
        int 첫값 = 빼기(0), 첫형식 = vratiti_TYPE;
        if (komanda_kod == 87) return;
        if (komanda_kod == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int bajt_podaci = 빼기(0), SECOND_format = vratiti_TYPE;
        if (komanda_kod == 88) return;
        if (komanda_kod == 90) { 넣기(첫값, 첫형식); 넣기(bajt_podaci, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (komanda_kod == 92) { 넣기(bajt_podaci, SECOND_format); 넣기(첫값, 첫형식); 넣기(bajt_podaci, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (komanda_kod == 95) { 넣기(첫값, 첫형식); 넣기(bajt_podaci, SECOND_format); return; }
        int kôd_znaka = 빼기(0), 셋째형식 = vratiti_TYPE;
        if (komanda_kod == 91) { 넣기(첫값, 첫형식); 넣기(kôd_znaka, 셋째형식); 넣기(bajt_podaci, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (komanda_kod == 93) { 넣기(bajt_podaci, SECOND_format); 넣기(첫값, 첫형식); 넣기(kôd_znaka, 셋째형식); 넣기(bajt_podaci, SECOND_format); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = vratiti_TYPE;
        넣기(bajt_podaci, SECOND_format); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(kôd_znaka, 셋째형식); 넣기(bajt_podaci, SECOND_format); 넣기(첫값, 첫형식);
    }
    static void 새객체(int naziv_konstanta, int 시작점) {
        int oblast_kod = 0, 유효길이 = 0, izuzetak_Reference = izuzetak_konstanta(naziv_konstanta);
        if (Word_SMS(naziv_konstanta, "java/lang/StringBuilder")) { oblast_kod = 4; 유효길이 = 1; }
        if (Word_SMS(naziv_konstanta, "java/io/FileInputStream")) { oblast_kod = 5; 유효길이 = 2; }
        if (Word_SMS(naziv_konstanta, "java/io/FileOutputStream")) { oblast_kod = 6; 유효길이 = 2; }
        if (izuzetak_Reference != 0) { oblast_kod = 9; 유효길이 = 2; }
        if (Word_SMS(naziv_konstanta, "java/util/ArrayList")) { oblast_kod = 10; 유효길이 = 2; }
        if (Word_SMS(naziv_konstanta, "java/util/HashMap")) { oblast_kod = 11; 유효길이 = 2; }
        if (Word_SMS(naziv_konstanta, "java/lang/Integer")) { oblast_kod = 12; 유효길이 = 1; }
        if (Word_SMS(naziv_konstanta, "java/net/Socket")) { oblast_kod = 17; 유효길이 = 5; }
        if (Word_SMS(naziv_konstanta, "java/net/ServerSocket")) { oblast_kod = 18; 유효길이 = 5; }
        if (Word_SMS(naziv_konstanta, "java/net/DatagramSocket")) { oblast_kod = 15; 유효길이 = 3; }
        if (Word_SMS(naziv_konstanta, "java/net/DatagramPacket")) { oblast_kod = 16; 유효길이 = 4; }
        if (Word_SMS(naziv_konstanta, "java/lang/Thread") || Word_SMS(naziv_konstanta, "한국어/자체/작업가닥")) { oblast_kod = 13; 유효길이 = 2; }
        if (Word_SMS(naziv_konstanta, "java/lang/Object")) { oblast_kod = 8; }
        if (oblast_kod == 0 && 화면종(naziv_konstanta) != 0) { oblast_kod = 화면종(naziv_konstanta); 유효길이 = 12; }
        if (oblast_kod == 0) {
            int kôd_znaka = FIND_klasa_Definicija(naziv_konstanta); if (kôd_znaka < 0 || GRESKA || !inicijalizirati(kôd_znaka, 시작점)) return;
            oblast_kod = 32 + kôd_znaka; 유효길이 = klasa_prostor_za_unos_COUNT[kôd_znaka];
        }
        int objekt_Reference = dodijeliti_Pohrana(oblast_kod, 유효길이); if (GRESKA) return;
        if (oblast_kod == 13 && Word_SMS(naziv_konstanta, "한국어/자체/작업가닥")) 힙[objekt_Reference + 3] = 1;
        if (oblast_kod >= 24 && oblast_kod <= 28 && 한국어화면종(naziv_konstanta) != 0) 힙[objekt_Reference + 13] = 1;
        if (oblast_kod == 5 || oblast_kod == 6 || oblast_kod == 15 || oblast_kod == 17 || oblast_kod == 18) 힙[objekt_Reference + 2] = -1;
        if (oblast_kod == 9) 힙[objekt_Reference + 2] = izuzetak_Reference;
        넣기(objekt_Reference, 2);
    }
    static boolean 값같음(int 첫값, int bajt_podaci) {
        if (첫값 == bajt_podaci) return true;
        if (첫값 == 0 || bajt_podaci == 0 || 첫값 < 0 || bajt_podaci < 0 || 첫값 >= 힙끝 || bajt_podaci >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[bajt_podaci] == 1) return 글같음(첫값, bajt_podaci, false);
        return 힙[첫값] == 12 && 힙[bajt_podaci] == 12 && 힙[첫값 + 2] == 힙[bajt_podaci + 2];
    }
    static int 글조각(int objekt_Reference, int START_položaj, int završiti_položaj) {
        if (!objekt_VALUE(objekt_Reference, 1)) return 0;
        if (START_položaj < 0 || završiti_položaj < START_položaj || završiti_položaj > 힙[objekt_Reference + 1]) { neuspjeh_VALUE("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = dodijeliti_Pohrana(1, završiti_položaj - START_položaj); if (GRESKA) return 0;
        for (int Loop_INDEX = START_položaj; Loop_INDEX < završiti_položaj; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX - START_položaj] = 힙[objekt_Reference + 2 + Loop_INDEX];
        return 반환값;
    }
    static int spoj_SMS(int 첫값, int bajt_podaci) {
        if (!objekt_VALUE(첫값, 1) || !objekt_VALUE(bajt_podaci, 1)) return 0;
        int unos_COUNT = 힙[첫값 + 1], metoda_INDEX = 힙[bajt_podaci + 1], 반환값 = dodijeliti_Pohrana(1, unos_COUNT + metoda_INDEX); if (GRESKA) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < unos_COUNT; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 힙[첫값 + 2 + Loop_INDEX];
        for (int Loop_INDEX = 0; Loop_INDEX < metoda_INDEX; Loop_INDEX++) 힙[반환값 + 2 + unos_COUNT + Loop_INDEX] = 힙[bajt_podaci + 2 + Loop_INDEX];
        return 반환값;
    }
    static boolean 기본호출(int vlasnik, int naziv_konstanta, int 서술상수, int komanda_kod) {
        if (Word_SMS(vlasnik, "한국어/자체/실행인수") && komanda_kod == 184) {
            if (Word_SMS(naziv_konstanta, "stavka_COUNT") && Word_SMS(서술상수, "()I")) { 넣기(korisnik.인수개수() - 1, 1); return true; }
            if (Word_SMS(naziv_konstanta, "Tekst") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= korisnik.인수개수() - 1) 예외던짐(29, "Izvrši_komanda Argumenti 범위를 벗어났습니다");
                else 넣기(organizator_znak(korisnik.Argumenti(순번 + 1)), 2);
                return true;
            }
            neuspjeh_VALUE("지원하지 않는 한국어 Izvrši_komanda Argumenti 호출"); return true;
        }
        if (Word_SMS(vlasnik, "한국어/자체/작업가닥")) { proces_nit(naziv_konstanta, 서술상수, komanda_kod, true); return true; }
        if (한국어화면소유(vlasnik)) { 한국어화면호출(vlasnik, naziv_konstanta, 서술상수, komanda_kod); return true; }
        if (화면소유(vlasnik)) { 화면호출(vlasnik, naziv_konstanta, 서술상수, komanda_kod); return true; }
        if (Word_SMS(vlasnik, "java/net/Socket") || Word_SMS(vlasnik, "java/net/ServerSocket") || Word_SMS(vlasnik, "java/io/InputStream") || Word_SMS(vlasnik, "java/io/OutputStream")) { 흐름호출(vlasnik, naziv_konstanta, 서술상수, komanda_kod); return true; }
        if (Word_SMS(vlasnik, "한국어/자체/jezgro_VALUE") && komanda_kod == 184) {
            if (Word_SMS(naziv_konstanta, "화면너비") && Word_SMS(서술상수, "()I")) { 넣기(korisnik.화면너비(), 1); return true; }
            if (Word_SMS(naziv_konstanta, "화면높이") && Word_SMS(서술상수, "()I")) { 넣기(korisnik.화면높이(), 1); return true; }
            if (Word_SMS(naziv_konstanta, "밀리초") && Word_SMS(서술상수, "()I")) { 넣기(korisnik.밀리초(), 1); return true; }
            if (Word_SMS(naziv_konstanta, "그림대기") && Word_SMS(서술상수, "()I")) { 넣기(korisnik.그림대기(), 1); return true; }
            if (Word_SMS(naziv_konstanta, "사각형") && Word_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), Y_koordinata = 빼기(1), koordinata_x = 빼기(1); 넣기(korisnik.사각형(koordinata_x, Y_koordinata, 너비, 높이, 색상), 1); return true; }
        }
        if (Word_SMS(vlasnik, "java/net/InetAddress") || Word_SMS(vlasnik, "java/net/DatagramPacket") || Word_SMS(vlasnik, "java/net/DatagramSocket")) { 통신호출(vlasnik, naziv_konstanta, 서술상수, komanda_kod); return true; }
        if (Word_SMS(vlasnik, "java/lang/Thread")) { 가닥호출(naziv_konstanta, 서술상수, komanda_kod); return true; }
        if (Word_SMS(vlasnik, "java/lang/Object")) {
            if (Word_SMS(naziv_konstanta, "<init>") && Word_SMS(서술상수, "()V") && komanda_kod == 183) { 객체유효(빼기(2)); return true; }
            if (Word_SMS(naziv_konstanta, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int bajt_podaci = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == bajt_podaci ? 1 : 0, 1); return true; }
        }
        if (izuzetak_konstanta(vlasnik) != 0) {
            if (Word_SMS(naziv_konstanta, "<init>") && komanda_kod == 183 && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int upit = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), objekt_Reference = 빼기(2);
                if (objekt_VALUE(objekt_Reference, 9)) { 힙[objekt_Reference + 3] = upit; 힙참조[objekt_Reference + 3] = 1; } return true;
            }
            if ((Word_SMS(naziv_konstanta, "getMessage") || Word_SMS(naziv_konstanta, "설명")) && Word_SMS(서술상수, "()Ljava/lang/String;")) { int objekt_Reference = 빼기(2); if (objekt_VALUE(objekt_Reference, 9)) 넣기(힙[objekt_Reference + 3], 2); return true; }
        }
        if (Word_SMS(vlasnik, "java/lang/String")) {
            if (komanda_kod == 182 && Word_SMS(naziv_konstanta, "getBytes") && (Word_SMS(서술상수, "()[B") || Word_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int kodiranje_naziv = Word_SMS(서술상수, "()[B") ? 0 : 빼기(2), objekt_Reference = 빼기(2);
                if (!objekt_VALUE(objekt_Reference, 1)) return true;
                if (kodiranje_naziv != 0 && !글같음(kodiranje_naziv, organizator_znak("UTF-8"), false) && !글같음(kodiranje_naziv, organizator_znak("UTF8"), false) && !글같음(kodiranje_naziv, organizator_znak("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int unos_COUNT = 힙[objekt_Reference + 1], 반환값 = dodijeliti_Pohrana(20, unos_COUNT * 3), 사용수 = 0; if (GRESKA) return true;
                for (int unutrašnje_spajanje_položaj = 0; unutrašnje_spajanje_položaj < unos_COUNT; unutrašnje_spajanje_položaj++) {
                    int kôd_znaka = 힙[objekt_Reference + 2 + unutrašnje_spajanje_položaj];
                    if (kôd_znaka >= 0xd800 && kôd_znaka <= 0xdbff && unutrašnje_spajanje_položaj + 1 < unos_COUNT && 힙[objekt_Reference + 3 + unutrašnje_spajanje_položaj] >= 0xdc00 && 힙[objekt_Reference + 3 + unutrašnje_spajanje_položaj] <= 0xdfff) kôd_znaka = 0x10000 + ((kôd_znaka - 0xd800) << 10) + 힙[objekt_Reference + 2 + ++unutrašnje_spajanje_položaj] - 0xdc00;
                    else if (kôd_znaka >= 0xd800 && kôd_znaka <= 0xdfff) kôd_znaka = '?';
                    if (kôd_znaka < 128) 힙[반환값 + 2 + 사용수++] = kôd_znaka;
                    else { int bajt_COUNT = kôd_znaka < 2048 ? 2 : kôd_znaka < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((bajt_COUNT == 2 ? 192 : bajt_COUNT == 3 ? 224 : 240) | kôd_znaka >> (6 * (bajt_COUNT - 1))); for (int Poređenje_položaj = bajt_COUNT - 1; Poređenje_položaj > 0; Poređenje_položaj--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | kôd_znaka >> (6 * (Poređenje_položaj - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (komanda_kod == 184 && Word_SMS(naziv_konstanta, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(cifra_znak(빼기(1)), 2); return true; }
            if (komanda_kod != 182) return false;
            if (Word_SMS(naziv_konstanta, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int bajt_podaci = 빼기(2), 첫값 = 빼기(2); if (objekt_VALUE(첫값, 1)) 넣기(글같음(첫값, bajt_podaci, false) ? 1 : 0, 1); return true; }
            if (Word_SMS(naziv_konstanta, "isEmpty") && Word_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (objekt_VALUE(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_SMS(naziv_konstanta, "substring") && (Word_SMS(서술상수, "(I)Ljava/lang/String;") || Word_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SECOND_VALUE = Word_SMS(서술상수, "(II)Ljava/lang/String;"); int završiti_položaj = SECOND_VALUE ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (objekt_VALUE(첫값, 1)) 넣기(글조각(첫값, 시작점, SECOND_VALUE ? završiti_položaj : 힙[첫값 + 1]), 2); return true;
            }
            if (Word_SMS(naziv_konstanta, "concat") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int bajt_podaci = 빼기(2), 첫값 = 빼기(2); 넣기(spoj_SMS(첫값, bajt_podaci), 2); return true; }
            if (Word_SMS(naziv_konstanta, "hashCode") && Word_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), raspršivanje_VALUE = 0; if (objekt_VALUE(첫값, 1)) { for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) raspršivanje_VALUE = raspršivanje_VALUE * 31 + 힙[첫값 + 2 + Loop_INDEX]; 넣기(raspršivanje_VALUE, 1); } return true; }
            if (Word_SMS(naziv_konstanta, "toString") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (objekt_VALUE(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_SMS(vlasnik, "java/lang/Integer")) {
            if (komanda_kod == 184 && Word_SMS(naziv_konstanta, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int podaci_VALUE = 빼기(1), objekt_Reference = podaci_VALUE >= -128 && podaci_VALUE <= 127 ? Store_cijeli_broj[podaci_VALUE + 128] : 0; if (objekt_Reference == 0) { objekt_Reference = dodijeliti_Pohrana(12, 1); if (!GRESKA) { 힙[objekt_Reference + 2] = podaci_VALUE; if (podaci_VALUE >= -128 && podaci_VALUE <= 127) Store_cijeli_broj[podaci_VALUE + 128] = objekt_Reference; } } 넣기(objekt_Reference, 2); return true; }
            if (komanda_kod == 183 && Word_SMS(naziv_konstanta, "<init>") && Word_SMS(서술상수, "(I)V")) { int podaci_VALUE = 빼기(1), objekt_Reference = 빼기(2); if (objekt_VALUE(objekt_Reference, 12)) 힙[objekt_Reference + 2] = podaci_VALUE; return true; }
            if (komanda_kod == 182 && Word_SMS(naziv_konstanta, "intValue") && Word_SMS(서술상수, "()I")) { int objekt_Reference = 빼기(2); if (objekt_VALUE(objekt_Reference, 12)) 넣기(힙[objekt_Reference + 2], 1); return true; }
            if (komanda_kod == 184 && Word_SMS(naziv_konstanta, "toString") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(cifra_znak(빼기(1)), 2); return true; }
        }
        if (Word_SMS(vlasnik, "java/lang/Math") && komanda_kod == 184) {
            if (Word_SMS(naziv_konstanta, "abs") && Word_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_SMS(naziv_konstanta, "min") || Word_SMS(naziv_konstanta, "max")) && Word_SMS(서술상수, "(II)I")) { int bajt_podaci = 빼기(1), 첫값 = 빼기(1); 넣기(Word_SMS(naziv_konstanta, "min") ? (첫값 < bajt_podaci ? 첫값 : bajt_podaci) : (첫값 > bajt_podaci ? 첫값 : bajt_podaci), 1); return true; }
        }
        if (Word_SMS(vlasnik, "java/lang/System") && komanda_kod == 184) {
            if (Word_SMS(naziv_konstanta, "gc") && Word_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Word_SMS(naziv_konstanta, "arraycopy") && Word_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int unos_COUNT = 빼기(1), odredište_VALUE_INDEX = 빼기(1), bajt_podaci = 빼기(2), START_položaj = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(bajt_podaci)) {
                    int oblast_kod = 힙[첫값];
                    if (힙[bajt_podaci] != oblast_kod || (oblast_kod != 2 && oblast_kod != 3 && (oblast_kod < 20 || oblast_kod > 23))) neuspjeh_VALUE("arraycopy type mismatch");
                    else if (unos_COUNT < 0 || START_položaj < 0 || odredište_VALUE_INDEX < 0 || START_položaj > 힙[첫값 + 1] - unos_COUNT || odredište_VALUE_INDEX > 힙[bajt_podaci + 1] - unos_COUNT) neuspjeh_VALUE("ArrayIndexOutOfBoundsException");
                    else if (첫값 == bajt_podaci && odredište_VALUE_INDEX > START_položaj) { for (int Loop_INDEX = unos_COUNT - 1; Loop_INDEX >= 0; Loop_INDEX--) 힙[bajt_podaci + 2 + odredište_VALUE_INDEX + Loop_INDEX] = 힙[첫값 + 2 + START_položaj + Loop_INDEX]; }
                    else { for (int Loop_INDEX = 0; Loop_INDEX < unos_COUNT && !GRESKA; Loop_INDEX++) { int podaci_VALUE = 힙[첫값 + 2 + START_položaj + Loop_INDEX]; if (oblast_kod != 3 || 배열저장가능(bajt_podaci, podaci_VALUE)) 힙[bajt_podaci + 2 + odredište_VALUE_INDEX + Loop_INDEX] = podaci_VALUE; } }
                }
                return true;
            }
        }
        if (Word_SMS(vlasnik, "java/util/ArrayList") || Word_SMS(vlasnik, "java/util/List") || Word_SMS(vlasnik, "java/util/HashMap") || Word_SMS(vlasnik, "java/util/Map")) {
            모음호출(vlasnik, naziv_konstanta, 서술상수, komanda_kod); return true;
        }
        return false;
    }
    static void 모음늘리기(int objekt_Reference, int 필요수) {
        int 이전값 = 힙[objekt_Reference + 2], 용량값 = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (용량값 >= 필요수) return;
        int Dalje_položaj = 용량값 < 8 ? 8 : 용량값 * 2; if (Dalje_položaj < 필요수) Dalje_položaj = 필요수;
        int podaci_niz = dodijeliti_Pohrana(3, Dalje_položaj); if (GRESKA) return;
        for (int Loop_INDEX = 0; Loop_INDEX < 용량값; Loop_INDEX++) 힙[podaci_niz + 2 + Loop_INDEX] = 힙[이전값 + 2 + Loop_INDEX];
        힙[objekt_Reference + 2] = podaci_niz; 힙참조[objekt_Reference + 2] = 1;
    }
    static void 모음호출(int vlasnik, int naziv_konstanta, int 서술상수, int komanda_kod) {
        boolean 대응참조 = Word_SMS(vlasnik, "java/util/HashMap") || Word_SMS(vlasnik, "java/util/Map"); int oblast_kod = 대응참조 ? 11 : 10;
        if (Word_SMS(naziv_konstanta, "<init>") && komanda_kod == 183 && Word_SMS(서술상수, "()V")) { int objekt_Reference = 빼기(2); if (objekt_VALUE(objekt_Reference, oblast_kod)) 모음늘리기(objekt_Reference, 8); return; }
        if (komanda_kod != 182 && komanda_kod != 185) { neuspjeh_VALUE("invalid collection invocation"); return; }
        if (Word_SMS(naziv_konstanta, "size") && Word_SMS(서술상수, "()I") || Word_SMS(naziv_konstanta, "isEmpty") && Word_SMS(서술상수, "()Z")) {
            int objekt_Reference = 빼기(2); if (objekt_VALUE(objekt_Reference, oblast_kod)) 넣기(Word_SMS(naziv_konstanta, "size") ? 힙[objekt_Reference + 3] : 힙[objekt_Reference + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_SMS(naziv_konstanta, "clear") && Word_SMS(서술상수, "()V")) { int objekt_Reference = 빼기(2); if (objekt_VALUE(objekt_Reference, oblast_kod)) { int podaci_niz = 힙[objekt_Reference + 2]; for (int Loop_INDEX = 0; Loop_INDEX < 힙[podaci_niz + 1]; Loop_INDEX++) 힙[podaci_niz + 2 + Loop_INDEX] = 0; 힙[objekt_Reference + 3] = 0; } return; }
        if (!대응참조 && Word_SMS(naziv_konstanta, "add") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int podaci_VALUE = 빼기(2), objekt_Reference = 빼기(2); if (!objekt_VALUE(objekt_Reference, 10)) return;
            int unos_COUNT = 힙[objekt_Reference + 3]; 모음늘리기(objekt_Reference, unos_COUNT + 1); if (!GRESKA) { 힙[힙[objekt_Reference + 2] + 2 + unos_COUNT] = podaci_VALUE; 힙[objekt_Reference + 3] = unos_COUNT + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_SMS(naziv_konstanta, "get") || Word_SMS(naziv_konstanta, "remove")) && Word_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Word_SMS(naziv_konstanta, "set") && Word_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = Word_SMS(naziv_konstanta, "set"); int podaci_VALUE = 지정여부 ? 빼기(2) : 0, unos_položaj = 빼기(1), objekt_Reference = 빼기(2);
            if (!objekt_VALUE(objekt_Reference, 10)) return;
            int unos_COUNT = 힙[objekt_Reference + 3], podaci_niz = 힙[objekt_Reference + 2];
            if (unos_položaj < 0 || unos_položaj >= unos_COUNT) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[podaci_niz + 2 + unos_položaj];
            if (지정여부) 힙[podaci_niz + 2 + unos_položaj] = podaci_VALUE;
            if (Word_SMS(naziv_konstanta, "remove")) { for (int Loop_INDEX = unos_položaj + 1; Loop_INDEX < unos_COUNT; Loop_INDEX++) 힙[podaci_niz + 1 + Loop_INDEX] = 힙[podaci_niz + 2 + Loop_INDEX]; 힙[podaci_niz + 1 + unos_COUNT] = 0; 힙[objekt_Reference + 3] = unos_COUNT - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Word_SMS(naziv_konstanta, "get") || Word_SMS(naziv_konstanta, "remove")) && Word_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(naziv_konstanta, "put") && Word_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(naziv_konstanta, "containsKey") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_SMS(naziv_konstanta, "put"), ukloniti = Word_SMS(naziv_konstanta, "remove");
            int podaci_VALUE = 넣기여부 ? 빼기(2) : 0, ključ_Reference = 빼기(2), objekt_Reference = 빼기(2); if (!objekt_VALUE(objekt_Reference, 11)) return;
            int unos_COUNT = 힙[objekt_Reference + 3], podaci_niz = 힙[objekt_Reference + 2], 찾은여부 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < unos_COUNT; Loop_INDEX++) if (값같음(ključ_Reference, 힙[podaci_niz + 2 + 2 * Loop_INDEX])) { 찾은여부 = Loop_INDEX; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[podaci_niz + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(objekt_Reference, (unos_COUNT + 1) * 2); podaci_niz = 힙[objekt_Reference + 2]; 찾은여부 = unos_COUNT; if (!GRESKA) 힙[objekt_Reference + 3] = unos_COUNT + 1; }
                if (!GRESKA) { 힙[podaci_niz + 2 + 2 * 찾은여부] = ključ_Reference; 힙[podaci_niz + 3 + 2 * 찾은여부] = podaci_VALUE; }
            }
            if (ukloniti && 찾은여부 >= 0) { for (int Loop_INDEX = 찾은여부 + 1; Loop_INDEX < unos_COUNT; Loop_INDEX++) { 힙[podaci_niz + 2 * Loop_INDEX] = 힙[podaci_niz + 2 + 2 * Loop_INDEX]; 힙[podaci_niz + 1 + 2 * Loop_INDEX] = 힙[podaci_niz + 3 + 2 * Loop_INDEX]; } 힙[podaci_niz + 2 * unos_COUNT] = 0; 힙[podaci_niz + 1 + 2 * unos_COUNT] = 0; 힙[objekt_Reference + 3] = unos_COUNT - 1; }
            if (Word_SMS(naziv_konstanta, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        neuspjeh_VALUE("unsupported collection method");
    }
    static boolean 잠금얻기(int objekt_Reference) {
        if (!객체유효(objekt_Reference)) return false;
        if (잠금깊이[objekt_Reference] != 0 && 잠금주인[objekt_Reference] != trenutno_nit + 1) { promijeniti_HTTP_zahtjev = true; return false; }
        잠금주인[objekt_Reference] = trenutno_nit + 1; 잠금깊이[objekt_Reference]++; return true;
    }
    static void 잠금풀기(int objekt_Reference) {
        if (!객체유효(objekt_Reference)) return;
        if (잠금깊이[objekt_Reference] == 0 || 잠금주인[objekt_Reference] != trenutno_nit + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[objekt_Reference] == 0) 잠금주인[objekt_Reference] = 0;
    }
    static boolean SWITCH_nit() {
        nit_kadar[trenutno_nit] = kadar_INDEX;
        if (kadar_INDEX < trenutno_nit * 32) nit_stanje[trenutno_nit] = 3;
        for (int Loop_INDEX = 0; Loop_INDEX < nit_COUNT; Loop_INDEX++) if (nit_stanje[Loop_INDEX] == 2 && nit_stanje[가닥대기[Loop_INDEX]] == 3) nit_stanje[Loop_INDEX] = 1;
        for (int Loop_INDEX = 1; Loop_INDEX <= nit_COUNT; Loop_INDEX++) {
            int Dalje_položaj = (trenutno_nit + Loop_INDEX) % nit_COUNT;
            if (nit_stanje[Dalje_položaj] == 1) { trenutno_nit = Dalje_položaj; kadar_INDEX = nit_kadar[Dalje_položaj]; promijeniti_HTTP_zahtjev = false; return true; }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < nit_COUNT; Loop_INDEX++) if (nit_stanje[Loop_INDEX] != 3) { neuspjeh_VALUE("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int naziv_konstanta, int 서술상수, int komanda_kod) { proces_nit(naziv_konstanta, 서술상수, komanda_kod, false); }
    static void proces_nit(int naziv_konstanta, int 서술상수, int komanda_kod, boolean 한국어) {
        if (komanda_kod == 184 && Word_SMS(naziv_konstanta, 한국어 ? "YIELD_zadatak" : "yield") && Word_SMS(서술상수, "()V")) { promijeniti_HTTP_zahtjev = true; return; }
        if (komanda_kod == 184 && Word_SMS(naziv_konstanta, "currentThread") && Word_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(nit_objekt[trenutno_nit], 2); return; }
        if (komanda_kod == 183 && Word_SMS(naziv_konstanta, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, 한국어 ? "(L한국어/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int cilj_adresa = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), objekt_Reference = 빼기(2);
            if (!객체유효(objekt_Reference)) return;
            if (힙[objekt_Reference] == 13) { 힙[objekt_Reference + 2] = cilj_adresa; 힙참조[objekt_Reference + 2] = 1; }
            else if (cilj_adresa != 0) neuspjeh_VALUE("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (komanda_kod == 182 && (Word_SMS(naziv_konstanta, 한국어 ? "START_zadatak" : "start") || Word_SMS(naziv_konstanta, 한국어 ? "기다리기" : "join")) && Word_SMS(서술상수, "()V") || komanda_kod == 182 && Word_SMS(naziv_konstanta, 한국어 ? "살아있는가" : "isAlive") && Word_SMS(서술상수, "()Z")) {
            int objekt_Reference = 빼기(2); if (!객체유효(objekt_Reference)) return;
            int račun_VALUE = -1; for (int Loop_INDEX = 0; Loop_INDEX < nit_COUNT; Loop_INDEX++) if (nit_objekt[Loop_INDEX] == objekt_Reference) račun_VALUE = Loop_INDEX;
            if (Word_SMS(naziv_konstanta, 한국어 ? "살아있는가" : "isAlive")) { 넣기(račun_VALUE >= 0 && nit_stanje[račun_VALUE] != 3 ? 1 : 0, 1); return; }
            if (Word_SMS(naziv_konstanta, 한국어 ? "기다리기" : "join")) { if (račun_VALUE >= 0 && nit_stanje[račun_VALUE] != 3) { 가닥대기[trenutno_nit] = račun_VALUE; nit_stanje[trenutno_nit] = 2; promijeniti_HTTP_zahtjev = true; } return; }
            if (račun_VALUE >= 0) { 예외던짐(한국어 ? 38 : 16, "thread already started"); return; }
            if (nit_COUNT == 4) { neuspjeh_VALUE("thread limit (4 including main)"); return; }
            int cilj_adresa = 힙[objekt_Reference] == 13 ? 힙[objekt_Reference + 2] : objekt_Reference;
            int fajl_INDEX = cilj_adresa > 0 && 힙[cilj_adresa] >= 32 ? naziv_metoda(힙[cilj_adresa] - 32, 한국어 ? "Izvrši" : "run", "()V") : -1;
            if (cilj_adresa != 0 && fajl_INDEX < 0) { neuspjeh_VALUE("Runnable.run required"); return; }
            račun_VALUE = nit_COUNT++; nit_objekt[račun_VALUE] = objekt_Reference; nit_cilj[račun_VALUE] = cilj_adresa;
            int kadar = račun_VALUE * 32; nit_kadar[račun_VALUE] = fajl_INDEX < 0 ? kadar - 1 : kadar; nit_stanje[račun_VALUE] = fajl_INDEX < 0 ? 3 : 1;
            if (fajl_INDEX >= 0) { kadar_metoda[kadar] = fajl_INDEX; kadar_položaj[kadar] = metoda_START[fajl_INDEX]; lokalni_VALUE[kadar * 128] = cilj_adresa; lokalni_TYPE[kadar * 128] = 2; }
            return;
        }
        neuspjeh_VALUE("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], adresa_SMS = new int[16];
    static int lokalni_adresa() { return adresa_objekt(0x7f000001); }
    static int adresa_objekt(int VALUE) { int objekt_Reference = dodijeliti_Pohrana(14, 1); if (!GRESKA) 힙[objekt_Reference + 2] = VALUE; return objekt_Reference; }
    static int 주소해독(int objekt_Reference) {
        if (objekt_Reference == 0 || 글같음(objekt_Reference, organizator_znak("localhost"), false)) return 0x7f000001;
        if (!objekt_VALUE(objekt_Reference, 1)) return 0;
        int podaci_VALUE = 0, 총수 = 0, adresa_bajt = 0, 자릿수 = 0, unos_COUNT = 힙[objekt_Reference + 1];
        for (int Loop_INDEX = 0; Loop_INDEX <= unos_COUNT; Loop_INDEX++) {
            int kôd_znaka = Loop_INDEX == unos_COUNT ? '.' : 힙[objekt_Reference + 2 + Loop_INDEX];
            if (kôd_znaka == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } podaci_VALUE = podaci_VALUE << 8 | adresa_bajt; 총수++; adresa_bajt = 자릿수 = 0; }
            else { if (kôd_znaka < '0' || kôd_znaka > '9' || ++자릿수 > 3 || (adresa_bajt = adresa_bajt * 10 + kôd_znaka - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return podaci_VALUE;
    }
    static int adresa_znak(int podaci_VALUE) {
        int unos_COUNT = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int adresa_bajt = podaci_VALUE >>> 이동비트 & 255;
            if (adresa_bajt >= 100) adresa_SMS[unos_COUNT++] = '0' + adresa_bajt / 100;
            if (adresa_bajt >= 10) adresa_SMS[unos_COUNT++] = '0' + adresa_bajt / 10 % 10;
            adresa_SMS[unos_COUNT++] = '0' + adresa_bajt % 10; if (이동비트 != 0) adresa_SMS[unos_COUNT++] = '.';
        }
        int objekt_Reference = dodijeliti_Pohrana(1, unos_COUNT); if (!GRESKA) for (int Loop_INDEX = 0; Loop_INDEX < unos_COUNT; Loop_INDEX++) 힙[objekt_Reference + 2 + Loop_INDEX] = adresa_SMS[Loop_INDEX]; return objekt_Reference;
    }
    static void 통신호출(int vlasnik, int naziv_konstanta, int 서술상수, int komanda_kod) {
        if (Word_SMS(vlasnik, "java/net/InetAddress")) {
            if (komanda_kod == 184 && Word_SMS(naziv_konstanta, "getLoopbackAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(lokalni_adresa(), 2); return; }
            if (komanda_kod == 184 && Word_SMS(naziv_konstanta, "getByName") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int podaci_VALUE = 주소해독(빼기(2)); if (던진객체 == 0 && !GRESKA) 넣기(adresa_objekt(podaci_VALUE), 2); return;
            }
            if (komanda_kod == 182 && Word_SMS(naziv_konstanta, "getHostAddress") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int objekt_Reference = 빼기(2); if (objekt_VALUE(objekt_Reference, 14)) 넣기(adresa_znak(힙[objekt_Reference + 2]), 2); return; }
        }
        if (Word_SMS(vlasnik, "java/net/DatagramPacket")) {
            if (komanda_kod == 183 && Word_SMS(naziv_konstanta, "<init>") && (Word_SMS(서술상수, "([BI)V") || Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean odredište_VALUE_Reference = Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int broj_priključka = odredište_VALUE_Reference ? 빼기(1) : 0, adresa_Reference = odredište_VALUE_Reference ? 빼기(2) : 0;
                int unos_COUNT = 빼기(1), podaci_niz = 빼기(2), objekt_Reference = 빼기(2);
                if (!objekt_VALUE(objekt_Reference, 16) || !objekt_VALUE(podaci_niz, 20)) return;
                if (unos_COUNT < 0 || unos_COUNT > 힙[podaci_niz + 1] || broj_priključka < 0 || broj_priključka > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (adresa_Reference != 0 && !objekt_VALUE(adresa_Reference, 14)) return;
                힙[objekt_Reference + 2] = podaci_niz; 힙참조[objekt_Reference + 2] = 1; 힙[objekt_Reference + 3] = unos_COUNT;
                힙[objekt_Reference + 4] = adresa_Reference; 힙참조[objekt_Reference + 4] = 1; 힙[objekt_Reference + 5] = broj_priključka; return;
            }
            if (komanda_kod == 182 && Word_SMS(naziv_konstanta, "setLength") && Word_SMS(서술상수, "(I)V")) {
                int unos_COUNT = 빼기(1), objekt_Reference = 빼기(2); if (!objekt_VALUE(objekt_Reference, 16)) return;
                if (unos_COUNT < 0 || unos_COUNT > 힙[힙[objekt_Reference + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[objekt_Reference + 3] = unos_COUNT; return;
            }
            if (komanda_kod == 182 && (Word_SMS(naziv_konstanta, "getData") && Word_SMS(서술상수, "()[B") || Word_SMS(naziv_konstanta, "getLength") && Word_SMS(서술상수, "()I") || Word_SMS(naziv_konstanta, "getAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;") || Word_SMS(naziv_konstanta, "getPort") && Word_SMS(서술상수, "()I"))) {
                int objekt_Reference = 빼기(2); if (!objekt_VALUE(objekt_Reference, 16)) return;
                int unos_položaj = Word_SMS(naziv_konstanta, "getData") ? 2 : Word_SMS(naziv_konstanta, "getLength") ? 3 : Word_SMS(naziv_konstanta, "getAddress") ? 4 : 5;
                넣기(힙[objekt_Reference + unos_položaj], unos_položaj == 2 || unos_položaj == 4 ? 2 : 1); return;
            }
        }
        if (Word_SMS(vlasnik, "java/net/DatagramSocket")) {
            if (komanda_kod == 183 && Word_SMS(naziv_konstanta, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(I)V"))) {
                int broj_priključka = Word_SMS(서술상수, "()V") ? 0 : 빼기(1), objekt_Reference = 빼기(2); if (!objekt_VALUE(objekt_Reference, 15)) return;
                if (broj_priključka < 0 || broj_priključka > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = korisnik.kreirati_Mreža(broj_priključka); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[objekt_Reference + 2] = 열린파일번호; return;
            }
            if (komanda_kod == 182 && Word_SMS(naziv_konstanta, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), objekt_Reference = 빼기(2); if (!objekt_VALUE(objekt_Reference, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[objekt_Reference + 3] = 밀리초값; return;
            }
            if (komanda_kod == 182 && Word_SMS(naziv_konstanta, "getLocalPort") && Word_SMS(서술상수, "()I")) { int objekt_Reference = 빼기(2); if (objekt_VALUE(objekt_Reference, 15)) 넣기(힙[objekt_Reference + 2] < 0 ? -1 : korisnik.Mreža_port(힙[objekt_Reference + 2]), 1); return; }
            if (komanda_kod == 182 && Word_SMS(naziv_konstanta, "isClosed") && Word_SMS(서술상수, "()Z")) { int objekt_Reference = 빼기(2); if (objekt_VALUE(objekt_Reference, 15)) 넣기(힙[objekt_Reference + 2] < 0 ? 1 : 0, 1); return; }
            if (komanda_kod == 182 && Word_SMS(naziv_konstanta, "close") && Word_SMS(서술상수, "()V")) { int objekt_Reference = 빼기(2); if (objekt_VALUE(objekt_Reference, 15) && 힙[objekt_Reference + 2] >= 0) { korisnik.파일서술자닫기(힙[objekt_Reference + 2]); 힙[objekt_Reference + 2] = -1; } return; }
            if (komanda_kod == 182 && (Word_SMS(naziv_konstanta, "send") || Word_SMS(naziv_konstanta, "receive")) && Word_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int paket_5cd5338b = 빼기(2), objekt_Reference = 빼기(2); if (!objekt_VALUE(paket_5cd5338b, 16) || !objekt_VALUE(objekt_Reference, 15)) return;
                int podaci_niz = 힙[paket_5cd5338b + 2], 유효길이 = 힙[paket_5cd5338b + 3], 열린파일번호 = 힙[objekt_Reference + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_SMS(naziv_konstanta, "send")) {
                    if (!objekt_VALUE(힙[paket_5cd5338b + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < 유효길이; Loop_INDEX++) 통신임시[Loop_INDEX] = 힙[podaci_niz + 2 + Loop_INDEX];
                    if (korisnik.poslati_Mreža(열린파일번호, 힙[힙[paket_5cd5338b + 4] + 2], 힙[paket_5cd5338b + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int unos_COUNT = korisnik.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (unos_COUNT == -11) {
                        int trenutno_TIME = korisnik.밀리초();
                        if (힙[objekt_Reference + 4] == 0) 힙[objekt_Reference + 4] = trenutno_TIME + 1;
                        if (힙[objekt_Reference + 3] > 0 && trenutno_TIME - (힙[objekt_Reference + 4] - 1) >= 힙[objekt_Reference + 3]) { 힙[objekt_Reference + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(objekt_Reference, 2); 넣기(paket_5cd5338b, 2); kadar_položaj[kadar_INDEX] = kadar_programska_naredba[kadar_INDEX]; promijeniti_HTTP_zahtjev = true; return;
                    }
                    힙[objekt_Reference + 4] = 0;
                    if (unos_COUNT < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < unos_COUNT; Loop_INDEX++) 힙[podaci_niz + 2 + Loop_INDEX] = (byte)통신임시[Loop_INDEX];
                    힙[paket_5cd5338b + 3] = unos_COUNT; 힙[paket_5cd5338b + 4] = adresa_objekt(통신임시[513]); 힙참조[paket_5cd5338b + 4] = 1; 힙[paket_5cd5338b + 5] = 통신임시[512];
                }
                return;
            }
        }
        neuspjeh_VALUE("unsupported java.net method");
    }
    static boolean 흐름대기(int objekt_Reference) {
        int trenutno_TIME = korisnik.밀리초();
        if (힙[objekt_Reference + 5] == 0) 힙[objekt_Reference + 5] = trenutno_TIME + 1;
        if (힙[objekt_Reference + 3] > 0 && trenutno_TIME - (힙[objekt_Reference + 5] - 1) >= 힙[objekt_Reference + 3]) { 힙[objekt_Reference + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        kadar_položaj[kadar_INDEX] = kadar_programska_naredba[kadar_INDEX]; promijeniti_HTTP_zahtjev = true; return true;
    }
    static void 흐름호출(int vlasnik, int naziv_konstanta, int 서술상수, int komanda_kod) {
        boolean 수신쪽 = Word_SMS(vlasnik, "java/net/ServerSocket"), tok = Word_SMS(vlasnik, "java/io/InputStream") || Word_SMS(vlasnik, "java/io/OutputStream");
        if (!tok && komanda_kod == 183 && Word_SMS(naziv_konstanta, "<init>")) {
            boolean odjel_za_informacijske_tehnologije_prazno_stanje = Word_SMS(서술상수, "()V"), 이름지정여부 = Word_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(odjel_za_informacijske_tehnologije_prazno_stanje || 수신쪽 && Word_SMS(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { neuspjeh_VALUE("unsupported socket constructor"); return; }
            int broj_priključka = odjel_za_informacijske_tehnologije_prazno_stanje ? 0 : 빼기(1), adresa_Reference = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, objekt_Reference = 빼기(2);
            if (!objekt_VALUE(objekt_Reference, 수신쪽 ? 18 : 17)) return;
            if (broj_priključka < 0 || broj_priključka > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !objekt_VALUE(adresa_Reference, 14)) return;
            int Mreža_adresa = 이름지정여부 ? 주소해독(adresa_Reference) : 주소지정여부 ? 힙[adresa_Reference + 2] : 0x7f000001;
            if (GRESKA || 던진객체 != 0) return;
            int 열린파일번호 = korisnik.tok_kontrola(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = odjel_za_informacijske_tehnologije_prazno_stanje ? 0 : 수신쪽 ? korisnik.tok_kontrola(1, 열린파일번호, broj_priključka) : korisnik.povezati_tok(열린파일번호, Mreža_adresa, broj_priključka);
            if (처리값 < 0) { korisnik.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[objekt_Reference + 2] = 열린파일번호; 힙[objekt_Reference + 4] = broj_priključka; 힙[objekt_Reference + 6] = odjel_za_informacijske_tehnologije_prazno_stanje ? 0 : 1; return;
        }
        if (!tok && Word_SMS(naziv_konstanta, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), objekt_Reference = 빼기(2); if (!objekt_VALUE(objekt_Reference, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[objekt_Reference + 3] = 밀리초값; return; }
        if (!tok && Word_SMS(naziv_konstanta, "close") && Word_SMS(서술상수, "()V")) { int objekt_Reference = 빼기(2); if (objekt_VALUE(objekt_Reference, 수신쪽 ? 18 : 17) && 힙[objekt_Reference + 2] >= 0) { korisnik.파일서술자닫기(힙[objekt_Reference + 2]); 힙[objekt_Reference + 2] = -1; } return; }
        if (!tok && (Word_SMS(naziv_konstanta, "getLocalPort") || Word_SMS(naziv_konstanta, "getPort") || Word_SMS(naziv_konstanta, "isClosed") || Word_SMS(naziv_konstanta, "isConnected"))) {
            int objekt_Reference = 빼기(2); if (!objekt_VALUE(objekt_Reference, 수신쪽 ? 18 : 17)) return;
            넣기(Word_SMS(naziv_konstanta, "isClosed") ? 힙[objekt_Reference + 2] < 0 ? 1 : 0 : Word_SMS(naziv_konstanta, "isConnected") ? 힙[objekt_Reference + 6] : Word_SMS(naziv_konstanta, "getPort") ? 힙[objekt_Reference + 4] : 힙[objekt_Reference + 2] < 0 ? -1 : korisnik.tok_kontrola(4, 힙[objekt_Reference + 2], 0), 1); return;
        }
        if (수신쪽 && Word_SMS(naziv_konstanta, "accept") && Word_SMS(서술상수, "()Ljava/net/Socket;")) {
            int objekt_Reference = 빼기(2); if (!objekt_VALUE(objekt_Reference, 18)) return; int 열린파일번호 = korisnik.tok_kontrola(3, 힙[objekt_Reference + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(objekt_Reference)) 넣기(objekt_Reference, 2); return; }
            힙[objekt_Reference + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = dodijeliti_Pohrana(17, 5); if (GRESKA) { korisnik.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = korisnik.tok_kontrola(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !tok && ((Word_SMS(naziv_konstanta, "getInputStream") && Word_SMS(서술상수, "()Ljava/io/InputStream;")) || (Word_SMS(naziv_konstanta, "getOutputStream") && Word_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int objekt_Reference = 빼기(2); if (!objekt_VALUE(objekt_Reference, 17)) return; if (힙[objekt_Reference + 2] < 0 || 힙[objekt_Reference + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = dodijeliti_Pohrana(19, 4); if (GRESKA) return; 힙[반환값 + 2] = objekt_Reference; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Word_SMS(naziv_konstanta, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (tok) {
            boolean 읽기여부 = Word_SMS(naziv_konstanta, "read"), odjel_za_informacijske_tehnologije_pisati_operacija = Word_SMS(naziv_konstanta, "write"), blokirati = Word_SMS(서술상수, "([B)I") || Word_SMS(서술상수, "([B)V"), odjel_za_informacijske_tehnologije_SUBARRAY = Word_SMS(서술상수, "([BII)I") || Word_SMS(서술상수, "([BII)V");
            int unos_COUNT = odjel_za_informacijske_tehnologije_SUBARRAY ? 빼기(1) : 0, 시작변위 = odjel_za_informacijske_tehnologije_SUBARRAY ? 빼기(1) : 0, podaci_niz = blokirati || odjel_za_informacijske_tehnologije_SUBARRAY ? 빼기(2) : 0;
            int podaci_VALUE = odjel_za_informacijske_tehnologije_pisati_operacija && Word_SMS(서술상수, "(I)V") ? 빼기(1) : 0, objekt_Reference = 빼기(2);
            if (!objekt_VALUE(objekt_Reference, 19)) return; int roditelj_Reference = 힙[objekt_Reference + 2], 열린파일번호 = 힙[roditelj_Reference + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_SMS(naziv_konstanta, "close") && Word_SMS(서술상수, "()V")) { korisnik.파일서술자닫기(열린파일번호); 힙[roditelj_Reference + 2] = -1; return; }
            if (Word_SMS(naziv_konstanta, "flush") && Word_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !odjel_za_informacijske_tehnologije_pisati_operacija) || 읽기여부 != (힙[objekt_Reference + 3] == 0)) { neuspjeh_VALUE("unsupported stream operation"); return; }
            if (blokirati || odjel_za_informacijske_tehnologije_SUBARRAY) { if (!objekt_VALUE(podaci_niz, 20)) return; if (blokirati) unos_COUNT = 힙[podaci_niz + 1]; if (시작변위 < 0 || unos_COUNT < 0 || 시작변위 > 힙[podaci_niz + 1] - unos_COUNT) { 예외던짐(6, "stream array bounds"); return; } }
            else unos_COUNT = 1;
            if (unos_COUNT == 0) { if (읽기여부) 넣기(0, 1); return; }
            int 완료수 = odjel_za_informacijske_tehnologije_pisati_operacija ? 힙[objekt_Reference + 4] : 0, 처리값 = 0;
            while (완료수 < unos_COUNT) {
                처리값 = 읽기여부 ? korisnik.파일한바이트읽기(열린파일번호) : korisnik.파일한바이트쓰기(열린파일번호, blokirati || odjel_za_informacijske_tehnologije_SUBARRAY ? 힙[podaci_niz + 2 + 시작변위 + 완료수] : podaci_VALUE);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (blokirati || odjel_za_informacijske_tehnologije_SUBARRAY)) 힙[podaci_niz + 2 + 시작변위 + 완료수] = (byte)처리값;
                완료수++; if (읽기여부 && !(blokirati || odjel_za_informacijske_tehnologije_SUBARRAY)) break;
            }
            if (처리값 == -11 && (odjel_za_informacijske_tehnologije_pisati_operacija || 완료수 == 0)) {
                힙[objekt_Reference + 4] = 완료수;
                if (흐름대기(roditelj_Reference)) { 넣기(objekt_Reference, 2); if (blokirati || odjel_za_informacijske_tehnologije_SUBARRAY) 넣기(podaci_niz, 2); if (odjel_za_informacijske_tehnologije_SUBARRAY) { 넣기(시작변위, 1); 넣기(unos_COUNT, 1); } if (odjel_za_informacijske_tehnologije_pisati_operacija && !(blokirati || odjel_za_informacijske_tehnologije_SUBARRAY)) 넣기(podaci_VALUE, 1); } return;
            }
            힙[objekt_Reference + 4] = 0; 힙[roditelj_Reference + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(완료수 == 0 && 처리값 == 256 ? -1 : blokirati || odjel_za_informacijske_tehnologije_SUBARRAY ? 완료수 : 처리값, 1); return;
        }
        neuspjeh_VALUE("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int naziv_konstanta) {
        if (Word_SMS(naziv_konstanta, "한국어/자체/prozor")) return 24;
        if (Word_SMS(naziv_konstanta, "한국어/자체/Oznaka")) return 26;
        if (Word_SMS(naziv_konstanta, "한국어/자체/dugme")) return 27;
        if (Word_SMS(naziv_konstanta, "한국어/자체/SMS_polje")) return 28;
        if (Word_SMS(naziv_konstanta, "한국어/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int naziv_konstanta) {
        return 한국어화면종(naziv_konstanta) != 0 || Word_SMS(naziv_konstanta, "한국어/자체/화면구성요소") || Word_SMS(naziv_konstanta, "한국어/자체/događaj_redoslijed");
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
    static boolean 화면객체(int objekt_Reference) { if (!객체유효(objekt_Reference)) return false; if (힙[objekt_Reference] < 24 || 힙[objekt_Reference] > 28) { neuspjeh_VALUE("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int objekt_Reference, int SMS_Reference) {
        if (SMS_Reference != 0 && !objekt_VALUE(SMS_Reference, 1)) return;
        int unos_COUNT = SMS_Reference == 0 ? 0 : 힙[SMS_Reference + 1]; if (unos_COUNT > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < unos_COUNT; Loop_INDEX++) 화면글임시[Loop_INDEX] = 힙[SMS_Reference + 2 + Loop_INDEX];
        if (korisnik.화면글(힙[objekt_Reference + 2], 화면글임시, unos_COUNT) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[objekt_Reference + 3] = SMS_Reference; 힙참조[objekt_Reference + 3] = 1;
    }
    static int 화면문자읽기(int objekt_Reference) {
        int račun_VALUE = 힙[objekt_Reference + 2], unos_COUNT = korisnik.화면연결(8, račun_VALUE, 0, 0, 0, 0), 사용수 = 0;
        if (unos_COUNT < 0) { neuspjeh_VALUE("GUI text read failed"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < unos_COUNT; Loop_INDEX++) { int 부호값 = korisnik.화면연결(9, račun_VALUE, Loop_INDEX, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = dodijeliti_Pohrana(1, 사용수); if (!GRESKA) for (int Loop_INDEX = 0; Loop_INDEX < 사용수; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 화면글임시[Loop_INDEX]; return 반환값;
    }
    /* 한국어 객체를 직접 만들고 jezgro_VALUE 화면 기능에 연결한다. Swing objekt_VALUE/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int vlasnik, int naziv_konstanta, int 서술상수, int komanda_kod) {
        if (Word_SMS(vlasnik, "한국어/자체/događaj_redoslijed")) {
            if (komanda_kod == 184 && Word_SMS(naziv_konstanta, "나중에실행") && Word_SMS(서술상수, "(L한국어/자체/실행할일;)V")) {
                int zadatak_radnja = 빼기(2); if (!객체유효(zadatak_radnja)) return;
                if (나중수 == 8) { neuspjeh_VALUE("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = zadatak_radnja; return;
            }
            if (komanda_kod == 184 && Word_SMS(naziv_konstanta, "사건처리중인가") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            neuspjeh_VALUE("지원하지 않는 한국어 화면 일정 호출"); return;
        }
        if (Word_SMS(vlasnik, "한국어/자체/동작알림")) {
            int 알림 = 빼기(2); if (!objekt_VALUE(알림, 29) || 힙[알림 + 3] == 0) return;
            if (Word_SMS(naziv_konstanta, "događaj_izvor") && Word_SMS(서술상수, "()L한국어/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (Word_SMS(naziv_konstanta, "komanda_SMS") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (Word_SMS(naziv_konstanta, "INDEX") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else neuspjeh_VALUE("지원하지 않는 한국어 radnja 알림 호출"); return;
        }
        if (komanda_kod == 183 && Word_SMS(naziv_konstanta, "<init>")) {
            int 종류 = 한국어화면종(vlasnik), 받이 = 0, 가로 = 0, Vertikalno_položaj = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Word_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (korisnik.화면너비() - 폭) / 2; Vertikalno_položaj = (korisnik.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Word_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Word_SMS(서술상수, "(Ljava/lang/String;IIIIL한국어/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); Vertikalno_položaj = 빼기(1); 가로 = 빼기(1);
            } else { neuspjeh_VALUE("지원하지 않는 한국어 화면 생성자"); return; }
            int Tekst = 빼기(2), element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || Vertikalno_položaj < 0 || 폭 > korisnik.화면너비() - 가로 || 높이 > korisnik.화면높이() - Vertikalno_položaj) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDEX = korisnik.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (INDEX < 1 || INDEX > 32) { neuspjeh_VALUE("화면 element_VALUE 자리가 가득 찼습니다"); return; }
            힙[element_VALUE + 2] = INDEX; 화면참조[INDEX - 1] = element_VALUE;
            힙[element_VALUE + 5] = 가로; 힙[element_VALUE + 6] = Vertikalno_položaj; 힙[element_VALUE + 7] = 폭; 힙[element_VALUE + 8] = 높이; 힙[element_VALUE + 10] = 2;
            힙[element_VALUE + 4] = 받이; 힙참조[element_VALUE + 4] = 1; 힙[element_VALUE + 12] = 1;
            korisnik.화면연결(1, INDEX, 가로, Vertikalno_položaj, 폭, 높이);
            if (종류 == 24) korisnik.화면연결(7, INDEX, 2, 0, 0, 0);
            화면문자설정(element_VALUE, Tekst); return;
        }
        if (komanda_kod != 182) { neuspjeh_VALUE("잘못된 한국어 화면 호출 Naredba"); return; }
        if (Word_SMS(naziv_konstanta, "pisati_SMS") && Word_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int Tekst = 빼기(2), element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 화면문자설정(element_VALUE, Tekst); return;
        }
        if (Word_SMS(naziv_konstanta, "글읽기") && Word_SMS(서술상수, "()Ljava/lang/String;")) {
            int element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 넣기(화면문자읽기(element_VALUE), 2); return;
        }
        if (Word_SMS(naziv_konstanta, "동작맡기기") && Word_SMS(서술상수, "(L한국어/자체/동작받이;)V")) {
            int 받이 = 빼기(2), element_VALUE = 빼기(2);
            if (화면객체(element_VALUE)) { 힙[element_VALUE + 4] = 받이; 힙참조[element_VALUE + 4] = 1; 힙[element_VALUE + 12] = 1; } return;
        }
        if (Word_SMS(naziv_konstanta, "dodati_element") && Word_SMS(서술상수, "(L한국어/자체/화면구성요소;)V")) {
            int dijete_VALUE = 빼기(2), roditelj_VALUE = 빼기(2); if (!화면객체(dijete_VALUE) || !화면객체(roditelj_VALUE)) return;
            if (korisnik.화면연결(2, 힙[roditelj_VALUE + 2], 힙[dijete_VALUE + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[dijete_VALUE + 11] = roditelj_VALUE; 힙참조[dijete_VALUE + 11] = 1; return;
        }
        if (Word_SMS(naziv_konstanta, "자리정하기") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), Vertikalno_položaj = 빼기(1), 가로 = 빼기(1), element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (korisnik.화면연결(1, 힙[element_VALUE + 2], 가로, Vertikalno_položaj, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[element_VALUE + 5] = 가로; 힙[element_VALUE + 6] = Vertikalno_položaj; 힙[element_VALUE + 7] = 폭; 힙[element_VALUE + 8] = 높이; return;
        }
        if ((Word_SMS(naziv_konstanta, "program_prozor") || Word_SMS(naziv_konstanta, "Zatvori")) && Word_SMS(서술상수, "()V")) {
            boolean vidljivost_VALUE = Word_SMS(naziv_konstanta, "program_prozor"); int element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (korisnik.화면연결(vidljivost_VALUE ? 3 : 4, 힙[element_VALUE + 2], vidljivost_VALUE ? 1 : 0, 0, 0, 0) < 0) { neuspjeh_VALUE("화면은 interaktivno 명령에서 실행해야 합니다"); return; }
            힙[element_VALUE + 9] = vidljivost_VALUE ? 1 : 0; return;
        }
        if (Word_SMS(naziv_konstanta, "보이는가") && Word_SMS(서술상수, "()Z")) { int element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 넣기(힙[element_VALUE + 9], 1); return; }
        neuspjeh_VALUE("지원하지 않는 한국어 화면 metoda_VALUE");
    }
    static void 화면호출(int vlasnik, int naziv_konstanta, int 서술상수, int komanda_kod) {
        if (Word_SMS(vlasnik, "javax/swing/SwingUtilities")) {
            if (komanda_kod == 184 && Word_SMS(naziv_konstanta, "invokeLater") && Word_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int objekt_Reference = 빼기(2); if (!객체유효(objekt_Reference)) return; if (나중수 == 8) { neuspjeh_VALUE("invokeLater queue full"); return; } 나중실행[나중수++] = objekt_Reference; return; }
            if (komanda_kod == 184 && Word_SMS(naziv_konstanta, "isEventDispatchThread") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            neuspjeh_VALUE("unsupported SwingUtilities method"); return;
        }
        if (Word_SMS(vlasnik, "java/awt/event/ActionEvent")) {
            int objekt_Reference = 빼기(2); if (!objekt_VALUE(objekt_Reference, 29)) return;
            if (Word_SMS(naziv_konstanta, "getSource") && Word_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[objekt_Reference + 2], 2);
            else if (Word_SMS(naziv_konstanta, "getActionCommand") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[objekt_Reference + 2]), 2);
            else if (Word_SMS(naziv_konstanta, "getID") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else neuspjeh_VALUE("unsupported ActionEvent method"); return;
        }
        if (komanda_kod == 183 && Word_SMS(naziv_konstanta, "<init>")) {
            int Kolone = 0, SMS_Reference = 0;
            if (Word_SMS(서술상수, "(I)V")) Kolone = 빼기(1);
            else if (Word_SMS(서술상수, "(Ljava/lang/String;I)V")) { Kolone = 빼기(1); SMS_Reference = 빼기(2); }
            else if (Word_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_Reference = 빼기(2);
            else if (Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_SMS(서술상수, "()V")) { neuspjeh_VALUE("unsupported Swing constructor"); return; }
            int objekt_Reference = 빼기(2); if (!객체유효(objekt_Reference)) return;
            if (힙[objekt_Reference] == 30) { neuspjeh_VALUE("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(objekt_Reference) || Kolone < 0) return;
            int račun_VALUE = korisnik.화면연결(0, 힙[objekt_Reference] - 23, 0, 0, 0, 0);
            if (račun_VALUE < 1 || račun_VALUE > 32) { neuspjeh_VALUE("GUI widget slots exhausted"); return; }
            힙[objekt_Reference + 2] = račun_VALUE; 화면참조[račun_VALUE - 1] = objekt_Reference; 힙[objekt_Reference + 5] = 힙[objekt_Reference] == 24 ? 130 : 16; 힙[objekt_Reference + 6] = 힙[objekt_Reference] == 24 ? 110 : 16;
            힙[objekt_Reference + 7] = 힙[objekt_Reference] == 24 ? 380 : 220; 힙[objekt_Reference + 8] = 힙[objekt_Reference] == 24 ? 240 : 28; 힙[objekt_Reference + 10] = 1;
            화면문자설정(objekt_Reference, SMS_Reference); return;
        }
        if (Word_SMS(naziv_konstanta, "setText") || Word_SMS(naziv_konstanta, "setTitle")) { int SMS_Reference = 빼기(2), objekt_Reference = 빼기(2); if (화면객체(objekt_Reference) && Word_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(objekt_Reference, SMS_Reference); return; }
        if (Word_SMS(naziv_konstanta, "getText") || Word_SMS(naziv_konstanta, "getTitle")) { int objekt_Reference = 빼기(2); if (화면객체(objekt_Reference) && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(objekt_Reference), 2); return; }
        if (Word_SMS(naziv_konstanta, "addActionListener") && Word_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), objekt_Reference = 빼기(2); if (화면객체(objekt_Reference)) { 힙[objekt_Reference + 4] = 수신참조; 힙참조[objekt_Reference + 4] = 1; } return; }
        if (Word_SMS(naziv_konstanta, "getContentPane") && Word_SMS(서술상수, "()Ljava/awt/Container;")) { int objekt_Reference = 빼기(2); if (화면객체(objekt_Reference)) 넣기(objekt_Reference, 2); return; }
        if (Word_SMS(naziv_konstanta, "setLayout") && Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int izgled_Reference = 빼기(2), objekt_Reference = 빼기(2); if (화면객체(objekt_Reference) && izgled_Reference != 0) neuspjeh_VALUE("only absolute layout (null) is supported"); return; }
        if (Word_SMS(naziv_konstanta, "add") && (Word_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean izgled_uvjet = Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (izgled_uvjet) 빼기(2);
            int dijete_Reference = 빼기(2), objekt_Reference = 빼기(2); if (!화면객체(dijete_Reference) || !화면객체(objekt_Reference)) return;
            if (korisnik.화면연결(2, 힙[objekt_Reference + 2], 힙[dijete_Reference + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[dijete_Reference + 11] = objekt_Reference; 힙참조[dijete_Reference + 11] = 1; if (!izgled_uvjet) 넣기(dijete_Reference, 2); return;
        }
        if (Word_SMS(naziv_konstanta, "setBounds") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), Y_koordinata = 빼기(1), koordinata_x = 빼기(1), objekt_Reference = 빼기(2); if (!화면객체(objekt_Reference)) return;
            if (korisnik.화면연결(1, 힙[objekt_Reference + 2], koordinata_x, Y_koordinata, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[objekt_Reference + 5] = koordinata_x; 힙[objekt_Reference + 6] = Y_koordinata; 힙[objekt_Reference + 7] = 너비; 힙[objekt_Reference + 8] = 높이; return;
        }
        if (Word_SMS(naziv_konstanta, "setSize") && Word_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), objekt_Reference = 빼기(2); if (!화면객체(objekt_Reference)) return;
            if (korisnik.화면연결(1, 힙[objekt_Reference + 2], 힙[objekt_Reference + 5], 힙[objekt_Reference + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[objekt_Reference + 7] = 너비; 힙[objekt_Reference + 8] = 높이; } return;
        }
        if (Word_SMS(naziv_konstanta, "setLocationRelativeTo") && Word_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), objekt_Reference = 빼기(2); if (!화면객체(objekt_Reference)) return; if (상대배치 != 0) { neuspjeh_VALUE("only screen centering supported"); return; } 힙[objekt_Reference + 5] = (korisnik.화면너비() - 힙[objekt_Reference + 7]) / 2; 힙[objekt_Reference + 6] = (korisnik.화면높이() - 힙[objekt_Reference + 8]) / 2; korisnik.화면연결(1, 힙[objekt_Reference + 2], 힙[objekt_Reference + 5], 힙[objekt_Reference + 6], 힙[objekt_Reference + 7], 힙[objekt_Reference + 8]); return; }
        if (Word_SMS(naziv_konstanta, "setDefaultCloseOperation") && Word_SMS(서술상수, "(I)V")) { int pravilo = 빼기(1), objekt_Reference = 빼기(2); if (화면객체(objekt_Reference)) { if (pravilo < 0 || pravilo > 3) 예외던짐(9, "close policy"); else { 힙[objekt_Reference + 10] = pravilo; korisnik.화면연결(7, 힙[objekt_Reference + 2], pravilo, 0, 0, 0); } } return; }
        if (Word_SMS(naziv_konstanta, "setVisible") && Word_SMS(서술상수, "(Z)V")) { int podaci_VALUE = 빼기(1), objekt_Reference = 빼기(2); if (화면객체(objekt_Reference)) { int 처리값 = korisnik.화면연결(3, 힙[objekt_Reference + 2], podaci_VALUE, 0, 0, 0); if (처리값 < 0) neuspjeh_VALUE("Swing requires a standalone interactive command"); else 힙[objekt_Reference + 9] = podaci_VALUE; } return; }
        if (Word_SMS(naziv_konstanta, "dispose") && Word_SMS(서술상수, "()V")) { int objekt_Reference = 빼기(2); if (화면객체(objekt_Reference)) { korisnik.화면연결(4, 힙[objekt_Reference + 2], 0, 0, 0, 0); 힙[objekt_Reference + 9] = 0; } return; }
        if (Word_SMS(naziv_konstanta, "repaint") || Word_SMS(naziv_konstanta, "validate")) { int objekt_Reference = 빼기(2); if (!화면객체(objekt_Reference) || !Word_SMS(서술상수, "()V")) return; korisnik.화면연결(1, 힙[objekt_Reference + 2], 힙[objekt_Reference + 5], 힙[objekt_Reference + 6], 힙[objekt_Reference + 7], 힙[objekt_Reference + 8]); return; }
        if (Word_SMS(naziv_konstanta, "isVisible") && Word_SMS(서술상수, "()Z")) { int objekt_Reference = 빼기(2); if (화면객체(objekt_Reference)) 넣기(힙[objekt_Reference + 9], 1); return; }
        neuspjeh_VALUE("unsupported Swing method (native subset)");
    }
    static void 사건실행(int cilj_adresa, int 사건번호, boolean 한국어) {
        if (cilj_adresa < 1 || 힙[cilj_adresa] < 32) { neuspjeh_VALUE("Java event listener required"); return; }
        int fajl_INDEX = naziv_metoda(힙[cilj_adresa] - 32, 사건번호 == 0 ? (한국어 ? "Izvrši" : "run") : (한국어 ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (한국어 ? "(L한국어/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (fajl_INDEX < 0) { neuspjeh_VALUE("event callback missing"); return; }
        trenutno_nit = 0; nit_COUNT = 1; kadar_INDEX = 0; nit_stanje[0] = 1; kadar_snop[0] = 0; 틀잠금[0] = inicijalizirati_kadar[0] = 0; promijeniti_HTTP_zahtjev = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 128; Loop_INDEX++) { lokalni_VALUE[Loop_INDEX] = lokalni_TYPE[Loop_INDEX] = 0; }
        kadar_metoda[0] = fajl_INDEX; kadar_položaj[0] = metoda_START[fajl_INDEX]; lokalni_VALUE[0] = cilj_adresa; lokalni_TYPE[0] = 2;
        if (사건번호 != 0) { lokalni_VALUE[1] = 사건번호; lokalni_TYPE[1] = 2; }
        사건중 = true; Izvrši_komanda(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!GRESKA) {
            if (나중수 > 0) { int cilj_adresa = 나중실행[0], 한국어 = 나중한국어[0]; for (int Loop_INDEX = 1; Loop_INDEX < 나중수; Loop_INDEX++) { 나중실행[Loop_INDEX - 1] = 나중실행[Loop_INDEX]; 나중한국어[Loop_INDEX - 1] = 나중한국어[Loop_INDEX]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(cilj_adresa, 0, 한국어 != 0); continue; }
            if (korisnik.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = korisnik.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { neuspjeh_VALUE("GUI event I/O failed"); return; }
            int račun_VALUE = 사건번호 & 65535; if (račun_VALUE < 1 || račun_VALUE > 32) continue; int objekt_Reference = 화면참조[račun_VALUE - 1]; if (objekt_Reference == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[objekt_Reference + 10] != 0) 힙[objekt_Reference + 9] = 0;
                if (힙[objekt_Reference + 10] == 3) for (int Loop_INDEX = 0; Loop_INDEX < 32; Loop_INDEX++) if (화면참조[Loop_INDEX] != 0 && 힙[화면참조[Loop_INDEX]] == 24) korisnik.화면연결(4, Loop_INDEX + 1, 0, 0, 0, 0);
            } else if (힙[objekt_Reference + 4] != 0) {
                int Pročitaj_me_Reference = dodijeliti_Pohrana(29, 2); if (GRESKA) return; 힙[Pročitaj_me_Reference + 2] = objekt_Reference; 힙[Pročitaj_me_Reference + 3] = 힙[objekt_Reference + 12]; 힙참조[Pročitaj_me_Reference + 2] = 1; 사건실행(힙[objekt_Reference + 4], Pročitaj_me_Reference, 힙[objekt_Reference + 12] != 0);
            }
        }
    }
    public static int Pokreni() {
        if (korisnik.인수개수() == 1 && 자바도구.같음(korisnik.Argumenti(0), "-version")) {
            korisnik.Piši("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (korisnik.인수개수() < 1) { korisnik.Piši("Usage: java CLASS [ARGS]\n"); return 2; }
        unos_klasa_Definicija = učitati_klasa_Definicija(organizator_znak(korisnik.Argumenti(0))); if (GRESKA || unos_klasa_Definicija < 0) return 1;
        int unos_p_VALUE = naziv_metoda(unos_klasa_Definicija, "Pokreni", "()V");
        boolean 한국어진입 = unos_p_VALUE >= 0 && (metoda_pristup[unos_p_VALUE] & 9) == 9;
        if (!한국어진입) unos_p_VALUE = naziv_metoda(unos_klasa_Definicija, "main", "([Ljava/lang/String;)V");
        if (unos_p_VALUE < 0 || (metoda_pristup[unos_p_VALUE] & 9) != 9) neuspjeh_VALUE("public static void Pokreni() or main(String[] args) required");
        if (GRESKA) return 1;
        int Argumenti = dodijeliti_Pohrana(3, korisnik.인수개수() - 1); niz_element[Argumenti] = -1;
        for (int 수 = 1; 수 < korisnik.인수개수() && !GRESKA; 수++) 힙[Argumenti + 1 + 수] = organizator_znak(korisnik.Argumenti(수));
        kadar_INDEX = 0; kadar_metoda[0] = unos_p_VALUE; kadar_položaj[0] = metoda_START[unos_p_VALUE]; lokalni_VALUE[0] = 한국어진입 ? 0 : Argumenti; lokalni_TYPE[0] = 한국어진입 ? 0 : 2;
        nit_stanje[0] = 1; nit_objekt[0] = dodijeliti_Pohrana(13, 2);
        Izvrši_komanda(); if (!GRESKA) 화면사건들(); return GRESKA ? 1 : 0;
    }
}
