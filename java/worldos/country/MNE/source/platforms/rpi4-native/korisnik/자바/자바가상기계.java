// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Datoteka/operand_stek/referenca/grana 경계를 Izvrši_komanda 중 검사한다. */
public final class 자바가상기계 {
    static int[] Datoteka = new int[16 * 16384], privremena_datoteka = new int[16384], ime_datoteke_SMS = new int[512];
    static int[] konstanta_oznaka = new int[8192], 상가 = new int[8192], konstanta_SECOND_VALUE = new int[8192], niska_referenca = new int[8192];
    static int[] metod_ime_SMS = new int[512], metod_tip = new int[512], metod_pristup = new int[512], metod_vlasnik = new int[512];
    static int[] metod_START = new int[512], metod_završiti_razgovor = new int[512], metod_stek = new int[512], 함수지역 = new int[512];
    static int[] metod_argument_COUNT = new int[512], metod_argument_tip = new int[8192], metod_vratiti = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] lokalni_VALUE = new int[16384], lokalni_tip = new int[16384], operand_stek_VALUE = new int[16384], operand_stek_tip = new int[16384];
    static int[] kadar_metod = new int[128], kadar_pozicija = new int[128], kadar_stek = new int[128], 틀명령 = new int[128], 틀초기화 = new int[128];
    static int[] Razred_Definicija_ime = new int[16], Razred_Definicija_promeniti_veličinu = new int[16], Razred_Definicija_nadređen = new int[16], Razred_Definicija_Status = new int[16], 종칸수 = new int[16], 종초기화 = new int[16];
    static int[] Razred_interfejs = new int[16 * 16], Razred_interfejs_COUNT = new int[16];
    static int[] 칸이름 = new int[512], 칸형 = new int[512], 칸주인 = new int[512], 칸권한 = new int[512], 칸위치 = new int[512], 칸값 = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], element_niza = new int[32768], Store_ceo_broj = new int[256];
    static int promeniti_veličinu, 읽기위치, metod_COUNT, ime_klase, kadar_INDEX = -1, 힙끝 = 1, vratiti_tip;
    static int Razred_Definicija_COUNT, 칸수, 잡기수, 현재읽는종, 던진객체, 잠시수, ekran_COUNT, korpus_COUNT;
    static int aktuelno_nit, nit_COUNT = 1, stavka_Razred_Definicija;
    static int[] nit_kadar = new int[4], nit_Status = new int[4], nit_objekat = new int[4], nit_cilj = new int[4], 가닥대기 = new int[4];
    static boolean greška, promeniti_zahtev;
    static int[] zaključati_vlasnik = new int[32768], 잠금깊이 = new int[32768], kadar_zaključati = new int[128], Razred_zaključati = new int[16], Razred_nit = new int[16];

    static void otkazivanje_VALUE(String Word_SMS) {
        if (greška) return;
        int oblast_kôd = 0;
        if (자바도구.같음(Word_SMS, "ArithmeticException: / by zero")) oblast_kôd = 4;
        if (자바도구.같음(Word_SMS, "NullPointerException") || 자바도구.같음(Word_SMS, "null or invalid array")) oblast_kôd = 5;
        if (자바도구.같음(Word_SMS, "ArrayIndexOutOfBoundsException")) oblast_kôd = 7;
        if (자바도구.같음(Word_SMS, "StringIndexOutOfBoundsException")) oblast_kôd = 8;
        if (자바도구.같음(Word_SMS, "NumberFormatException")) oblast_kôd = 10;
        if (자바도구.같음(Word_SMS, "FileNotFoundException: file open failed")) oblast_kôd = 12;
        if (자바도구.같음(Word_SMS, "IOException: stream closed") || 자바도구.같음(Word_SMS, "IOException: read failed") || 자바도구.같음(Word_SMS, "IOException: write failed")) oblast_kôd = 11;
        if (자바도구.같음(Word_SMS, "ClassCastException")) oblast_kôd = 14;
        if (자바도구.같음(Word_SMS, "NegativeArraySizeException")) oblast_kôd = 15;
        if (oblast_kôd != 0 && kadar_INDEX >= 0) { 예외던짐(oblast_kôd, Word_SMS); return; }
        korisnik.쓰기("JVM error: "); korisnik.쓰기(Word_SMS); korisnik.문자쓰기(10); greška = true;
    }
    static boolean klip(int koristiti, int 길이) {
        if (koristiti < 0 || koristiti >= Datoteka.length || 길이 < 0) return false;
        int Razred_Definicija = koristiti / 16384;
        return koristiti % 16384 <= Razred_Definicija_promeniti_veličinu[Razred_Definicija] && 길이 <= Razred_Definicija_promeniti_veličinu[Razred_Definicija] - koristiti % 16384;
    }
    static int bajt_VALUE() {
        if (!klip(읽기위치, 1)) { otkazivanje_VALUE("truncated class file"); return 0; }
        return Datoteka[읽기위치++];
    }
    static int 짧은수() { return bajt_VALUE() << 8 | bajt_VALUE(); }
    static int ceo_broj() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int 길이) { if (!klip(읽기위치, 길이)) otkazivanje_VALUE("invalid attribute size"); else 읽기위치 += 길이; }
    static boolean proveriti_konstanta(int 수, int 종류) {
        if (수 <= 0 || 수 >= konstanta_oznaka.length || konstanta_oznaka[수] != 종류) { otkazivanje_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_opseg(int koristiti, int 길이, String Word_SMS) {
        if (!klip(koristiti, 길이)) return false;
        int 읽는자리 = koristiti, 끝 = koristiti + 길이;
        for (int Loop_INDEX = 0; Loop_INDEX < Word_SMS.length(); Loop_INDEX++) {
            int kôd_znaka = Word_SMS.charAt(Loop_INDEX);
            if (kôd_znaka > 0 && kôd_znaka < 128) { if (읽는자리 >= 끝 || Datoteka[읽는자리++] != kôd_znaka) return false; }
            else if (kôd_znaka < 2048) {
                if (읽는자리 + 2 > 끝 || Datoteka[읽는자리++] != (192 | (kôd_znaka >> 6)) || Datoteka[읽는자리++] != (128 | (kôd_znaka & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Datoteka[읽는자리++] != (224 | (kôd_znaka >> 12)) || Datoteka[읽는자리++] != (128 | ((kôd_znaka >> 6) & 63)) || Datoteka[읽는자리++] != (128 | (kôd_znaka & 63))) return false;
        }
        return 읽는자리 == 끝;
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
    static int 상번호() { int VALUE = 짧은수(); return VALUE == 0 ? 0 : 현재읽는종 * 512 + VALUE; }
    static int 명상수() { return metod_vlasnik[kadar_metod[kadar_INDEX]] * 512 + 명짧(); }
    static void 속성건너() {
        int stavka_COUNT = 짧은수();
        for (int 수 = 0; 수 < stavka_COUNT && !greška; 수++) { proveriti_konstanta(상번호(), 1); 건너(ceo_broj()); }
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
    static int pozicija_ceo_broj(int 읽는자리) {
        if (!klip(읽는자리, 4)) { otkazivanje_VALUE("truncated bytecode operand"); return 0; }
        return Datoteka[읽는자리] << 24 | Datoteka[읽는자리 + 1] << 16 | Datoteka[읽는자리 + 2] << 8 | Datoteka[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int koristiti, int 끝) {
        int VALUE = Datoteka[읽는자리], 길이 = 명령길이(VALUE);
        if (VALUE == 170 || VALUE == 171) {
            int BASE_pozicija = 읽는자리 + 1;
            while ((BASE_pozicija - koristiti) % 4 != 0) BASE_pozicija++;
            if (끝 - BASE_pozicija < (VALUE == 170 ? 12 : 8)) return 0;
            int stavka_COUNT_8f7753a1 = VALUE == 170 ? pozicija_ceo_broj(BASE_pozicija + 8) - pozicija_ceo_broj(BASE_pozicija + 4) + 1 : pozicija_ceo_broj(BASE_pozicija + 4);
            if (stavka_COUNT_8f7753a1 < 0 || stavka_COUNT_8f7753a1 > 2048) return 0;
            길이 = BASE_pozicija - 읽는자리 + (VALUE == 170 ? 12 + 4 * stavka_COUNT_8f7753a1 : 8 + 8 * stavka_COUNT_8f7753a1);
        }
        if (VALUE == 196 && 읽는자리 + 1 < 끝) {
            int Word_podaci = Datoteka[읽는자리 + 1]; 길이 = Word_podaci == 132 ? 6 : (Word_podaci == 21 || Word_podaci == 25 || Word_podaci == 54 || Word_podaci == 58) ? 4 : 0;
        }
        return 길이 > 0 && 길이 <= 끝 - 읽는자리 ? 길이 : 0;
    }
    static void proveriti_odredište_VALUE(int odredište_VALUE, int FUNCTION_VALUE) {
        if (odredište_VALUE < metod_START[FUNCTION_VALUE] || odredište_VALUE >= metod_završiti_razgovor[FUNCTION_VALUE] || 경계[odredište_VALUE] != FUNCTION_VALUE + 1) otkazivanje_VALUE("invalid branch target");
    }
    static void 클래스읽기(int Razred_Definicija) {
        현재읽는종 = Razred_Definicija; 읽기위치 = Razred_Definicija * 16384; promeniti_veličinu = 읽기위치 + Razred_Definicija_promeniti_veličinu[Razred_Definicija];
        if (ceo_broj() != 0xcafebabe) { otkazivanje_VALUE("not a class file"); return; }
        int 부판 = 짧은수(), verzija_VALUE = 짧은수();
        if (verzija_VALUE < 45 || verzija_VALUE > 52 || 부판 != 0) { otkazivanje_VALUE("supported class versions: 45..52, minor 0"); return; }
        int konstanta_COUNT = 짧은수(), BASE_pozicija = Razred_Definicija * 512;
        if (konstanta_COUNT < 1 || konstanta_COUNT > 512) { otkazivanje_VALUE("constant pool limit (511)"); return; }
        for (int stavka_COUNT_8f7753a1 = 1; stavka_COUNT_8f7753a1 < konstanta_COUNT && !greška; stavka_COUNT_8f7753a1++) {
            int 수 = BASE_pozicija + stavka_COUNT_8f7753a1, 종류 = bajt_VALUE(); konstanta_oznaka[수] = 종류;
            if (종류 == 1) { konstanta_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(konstanta_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = ceo_broj();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); konstanta_SECOND_VALUE[수] = 상번호(); }
            else otkazivanje_VALUE("unsupported constant type");
        }
        int dozvola_VALUE = 짧은수();
        if ((dozvola_VALUE & (0x2000 | 0x4000)) != 0) otkazivanje_VALUE("annotation/enum class unsupported");
        Razred_Definicija_ime[Razred_Definicija] = ime_klase_SMS(상번호());
        Razred_Definicija_nadređen[Razred_Definicija] = ime_klase_SMS(상번호());
        int interfejs_COUNT = 짧은수(); if (interfejs_COUNT > 16) { otkazivanje_VALUE("interface count limit"); return; }
        Razred_interfejs_COUNT[Razred_Definicija] = interfejs_COUNT;
        for (int Loop_INDEX = 0; Loop_INDEX < interfejs_COUNT; Loop_INDEX++) Razred_interfejs[Razred_Definicija * 16 + Loop_INDEX] = ime_klase_SMS(상번호());
        int polje_COUNT = 짧은수();
        if (polje_COUNT > 512 - 칸수) { otkazivanje_VALUE("field count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < polje_COUNT && !greška; Loop_INDEX++) {
            int Datoteka_INDEX = 칸수++; 칸주인[Datoteka_INDEX] = Razred_Definicija; 칸권한[Datoteka_INDEX] = 짧은수(); 칸이름[Datoteka_INDEX] = 상번호(); 칸형[Datoteka_INDEX] = 상번호();
            proveriti_konstanta(칸이름[Datoteka_INDEX], 1); proveriti_konstanta(칸형[Datoteka_INDEX], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[칸형[Datoteka_INDEX]]; int oblast_kôd = 서술형(읽기위치 + konstanta_SECOND_VALUE[칸형[Datoteka_INDEX]], false); 읽기위치 = 보존값;
            if ((칸권한[Datoteka_INDEX] & 8) == 0) 칸위치[Datoteka_INDEX] = 종칸수[Razred_Definicija]++;
            int atribut_podaci = 짧은수();
            for (int unutrašnje_pozicija = 0; unutrašnje_pozicija < atribut_podaci && !greška; unutrašnje_pozicija++) {
                int ime_konstanta = 상번호(), 유효길이 = ceo_broj();
                if (Word_SMS(ime_konstanta, "ConstantValue") && 유효길이 == 2) {
                    int podaci_VALUE = 상번호();
                    if (oblast_kôd == 1 && proveriti_konstanta(podaci_VALUE, 3)) 칸값[Datoteka_INDEX] = 상가[podaci_VALUE];
                    else if (oblast_kôd == 2 && proveriti_konstanta(podaci_VALUE, 8)) 칸값[Datoteka_INDEX] = konstanta_SMS(상가[podaci_VALUE]);
                } else 건너(유효길이);
            }
        }
        int stavka_COUNT = 짧은수();
        if (stavka_COUNT > 512 - metod_COUNT) { otkazivanje_VALUE("method count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < stavka_COUNT && !greška; Loop_INDEX++) {
            int 수 = metod_COUNT++; metod_vlasnik[수] = Razred_Definicija;
            metod_pristup[수] = 짧은수(); metod_ime_SMS[수] = 상번호(); metod_tip[수] = 상번호();
            proveriti_konstanta(metod_ime_SMS[수], 1); 서술읽기(수);
            if ((metod_pristup[수] & 8) == 0) {
                if (metod_argument_COUNT[수] == 16) { otkazivanje_VALUE("too many instance method arguments"); return; }
                for (int Poređenje_pozicija = metod_argument_COUNT[수]; Poređenje_pozicija > 0; Poređenje_pozicija--) metod_argument_tip[수 * 16 + Poređenje_pozicija] = metod_argument_tip[수 * 16 + Poređenje_pozicija - 1];
                metod_argument_tip[수 * 16] = 2; metod_argument_COUNT[수]++;
            }
            if ((metod_pristup[수] & 0x100) != 0) otkazivanje_VALUE("user native method unsupported");
            if (Word_SMS(metod_ime_SMS[수], "<clinit>")) 종초기화[Razred_Definicija] = 수 + 1;
            for (int čeona_kamera_VALUE = 0; čeona_kamera_VALUE < 수; čeona_kamera_VALUE++) if (metod_vlasnik[čeona_kamera_VALUE] == Razred_Definicija && 같은말(metod_ime_SMS[čeona_kamera_VALUE], metod_ime_SMS[수]) && 같은말(metod_tip[čeona_kamera_VALUE], metod_tip[수])) otkazivanje_VALUE("duplicate method");
            int atribut_COUNT = 짧은수();
            for (int atribut_VALUE = 0; atribut_VALUE < atribut_COUNT && !greška; atribut_VALUE++) {
                int ime = 상번호(), 길이 = ceo_broj(), koristiti = 읽기위치;
                if (!klip(koristiti, 길이)) { otkazivanje_VALUE("truncated method attribute"); break; }
                if (Word_SMS(ime, "Code")) {
                    if (metod_START[수] != 0) otkazivanje_VALUE("duplicate Code attribute");
                    metod_stek[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = ceo_broj();
                    if (metod_stek[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < metod_argument_COUNT[수]
                        || 코드길이 < 1 || 코드길이 > 8192) otkazivanje_VALUE("method memory limits exceeded");
                    metod_START[수] = 읽기위치; 건너(코드길이); metod_završiti_razgovor[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { otkazivanje_VALUE("exception table limit"); return; }
                    for (int unutrašnje_pozicija = 0; unutrašnje_pozicija < 잡는수; unutrašnje_pozicija++) {
                        int greška_referenca = 잡기수++; 잡기함수[greška_referenca] = 수;
                        잡기시작[greška_referenca] = metod_START[수] + 짧은수(); 잡기끝[greška_referenca] = metod_START[수] + 짧은수();
                        잡기위치[greška_referenca] = metod_START[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[greška_referenca] = 부호값 == 0 ? 0 : ime_klase_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != koristiti + 길이) otkazivanje_VALUE("Code attribute size mismatch");
                } else 건너(길이);
            }
            if ((metod_pristup[수] & 0x400) != 0) continue;
            if (metod_START[수] == 0) otkazivanje_VALUE("missing Code attribute");
            int 칸 = metod_START[수];
            while (칸 < metod_završiti_razgovor[수] && !greška) {
                int 길이 = 길이읽기(칸, metod_START[수], metod_završiti_razgovor[수]);
                if (길이 == 0) { otkazivanje_VALUE("unsupported or truncated bytecode"); break; }
                경계[칸] = 수 + 1; 칸 += 길이;
            }
            칸 = metod_START[수];
            while (칸 < metod_završiti_razgovor[수] && !greška) {
                int VALUE = Datoteka[칸];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) proveriti_odredište_VALUE(칸 + (short)(Datoteka[칸 + 1] << 8 | Datoteka[칸 + 2]), 수);
                if (VALUE == 200) proveriti_odredište_VALUE(칸 + pozicija_ceo_broj(칸 + 1), 수);
                if (VALUE == 170 || VALUE == 171) {
                    int 읽는자리 = 칸 + 1; while ((읽는자리 - metod_START[수]) % 4 != 0) 읽는자리++;
                    proveriti_odredište_VALUE(칸 + pozicija_ceo_broj(읽는자리), 수);
                    int stavka_COUNT_8f7753a1 = VALUE == 170 ? pozicija_ceo_broj(읽는자리 + 8) - pozicija_ceo_broj(읽는자리 + 4) + 1 : pozicija_ceo_broj(읽는자리 + 4);
                    읽는자리 += VALUE == 170 ? 12 : 8;
                    for (int unutrašnje_pozicija = 0; unutrašnje_pozicija < stavka_COUNT_8f7753a1; unutrašnje_pozicija++) proveriti_odredište_VALUE(칸 + pozicija_ceo_broj(읽는자리 + unutrašnje_pozicija * (VALUE == 170 ? 4 : 8) + (VALUE == 170 ? 0 : 4)), 수);
                }
                칸 += 길이읽기(칸, metod_START[수], metod_završiti_razgovor[수]);
            }
            for (int unutrašnje_pozicija = 0; unutrašnje_pozicija < 잡기수; unutrašnje_pozicija++) if (잡기함수[unutrašnje_pozicija] == 수) {
                proveriti_odredište_VALUE(잡기시작[unutrašnje_pozicija], 수); proveriti_odredište_VALUE(잡기위치[unutrašnje_pozicija], 수);
                if (잡기끝[unutrašnje_pozicija] != metod_završiti_razgovor[수]) proveriti_odredište_VALUE(잡기끝[unutrašnje_pozicija], 수);
                if (잡기시작[unutrašnje_pozicija] >= 잡기끝[unutrašnje_pozicija]) otkazivanje_VALUE("invalid exception range");
            }
        }
        if (!greška) 속성건너();
        if (읽기위치 != promeniti_veličinu) otkazivanje_VALUE("extra class file data");
    }
    static int dodeliti_Skladište(int 종류, int 길이) { return 새기억(종류, 길이); }
    static boolean objekat_VALUE(int referenca, int 종류) {
        if (!객체유효(referenca)) return false;
        if (힙[referenca] != 종류) { otkazivanje_VALUE("object type mismatch"); return false; }
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
        if (vratiti_tip == 2) zaštititi_VALUE(operand_stek_VALUE[칸]);
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
        if (kadar_INDEX % 32 == 31) { otkazivanje_VALUE("call stack limit (32)"); return; }
        int Dalje_stavka = kadar_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) lokalni_tip[Dalje_stavka * 128 + 수] = 0;
        for (int 수 = metod_argument_COUNT[FUNCTION_VALUE] - 1; 수 >= 0; 수--) {
            lokalni_VALUE[Dalje_stavka * 128 + 수] = 빼기(metod_argument_tip[FUNCTION_VALUE * 16 + 수]); lokalni_tip[Dalje_stavka * 128 + 수] = metod_argument_tip[FUNCTION_VALUE * 16 + 수];
        }
        if (greška) return;
        kadar_INDEX = Dalje_stavka; 틀초기화[kadar_INDEX] = 0; kadar_metod[kadar_INDEX] = FUNCTION_VALUE; kadar_pozicija[kadar_INDEX] = metod_START[FUNCTION_VALUE]; kadar_stek[kadar_INDEX] = 0;
    }
    static void vratiti_KR(int tip_VALUE) {
        if (tip_VALUE != metod_vratiti[kadar_metod[kadar_INDEX]]) { otkazivanje_VALUE("return type mismatch"); return; }
        int VALUE = tip_VALUE == 0 ? 0 : 빼기(tip_VALUE);
        if (틀초기화[kadar_INDEX] != 0) Razred_Definicija_Status[틀초기화[kadar_INDEX] - 1] = 2;
        if (kadar_zaključati[kadar_INDEX] != 0) { izdanje_zaključati(kadar_zaključati[kadar_INDEX]); kadar_zaključati[kadar_INDEX] = 0; }
        kadar_INDEX--; if (kadar_INDEX >= aktuelno_nit * 32 && tip_VALUE != 0) 넣기(VALUE, tip_VALUE);
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
                if (VALUE < 1) { otkazivanje_VALUE("invalid file stream path"); return; }
                tok_ime_datoteke[칸] = VALUE;
            }
            tok_ime_datoteke[길이] = 0;
            int 서술자 = korisnik.파일서술자열기(tok_ime_datoteke, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { otkazivanje_VALUE("FileNotFoundException: file open failed"); return; }
            힙[tok_VALUE + 2] = 서술자; 힙[tok_VALUE + 3] = 1;
            return;
        }
        if (komanda != 182) { otkazivanje_VALUE("invalid file stream invocation"); return; }
        if ((출력 && Word_SMS(ime, "write") || !출력 && Word_SMS(ime, "read"))
            && (Word_SMS(format_VALUE, 출력 ? "([B)V" : "([B)I") || Word_SMS(format_VALUE, 출력 ? "([BII)V" : "([BII)I"))) {
            boolean klip_VALUE = Word_SMS(format_VALUE, 출력 ? "([BII)V" : "([BII)I");
            int stavka_COUNT_8f7753a1 = klip_VALUE ? 빼기(1) : 0, 시작점 = klip_VALUE ? 빼기(1) : 0, podaci_niz = 빼기(2), objekat_referenca = 빼기(2);
            if (!objekat_VALUE(podaci_niz, 20) || !objekat_VALUE(objekat_referenca, 종류)) return;
            if (!klip_VALUE) stavka_COUNT_8f7753a1 = 힙[podaci_niz + 1];
            if (시작점 < 0 || stavka_COUNT_8f7753a1 < 0 || 시작점 > 힙[podaci_niz + 1] - stavka_COUNT_8f7753a1) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[objekat_referenca + 3] == 0 || 힙[objekat_referenca + 2] < 0) { otkazivanje_VALUE("IOException: stream closed"); return; }
            int Dovršeno_COUNT = 0;
            while (Dovršeno_COUNT < stavka_COUNT_8f7753a1 && !greška) {
                int 반환값 = 출력 ? korisnik.파일한바이트쓰기(힙[objekat_referenca + 2], 힙[podaci_niz + 2 + 시작점 + Dovršeno_COUNT]) : korisnik.파일한바이트읽기(힙[objekat_referenca + 2]);
                if (반환값 < 0) { otkazivanje_VALUE(출력 ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!출력 && 반환값 == 256) break;
                if (!출력) 힙[podaci_niz + 2 + 시작점 + Dovršeno_COUNT] = (byte)반환값;
                Dovršeno_COUNT++;
            }
            if (!출력) 넣기(stavka_COUNT_8f7753a1 != 0 && Dovršeno_COUNT == 0 ? -1 : Dovršeno_COUNT, 1);
            return;
        }
        if (출력 && Word_SMS(ime, "flush") && Word_SMS(format_VALUE, "()V")) { int objekat_referenca = 빼기(2); if (objekat_VALUE(objekat_referenca, 종류) && 힙[objekat_referenca + 2] < 0) otkazivanje_VALUE("IOException: stream closed"); return; }
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
            if (KR < -1) otkazivanje_VALUE("IOException: read failed"); else 넣기(KR == 256 ? -1 : KR, 1);
        } else if (korisnik.파일한바이트쓰기(서술자, VALUE) != 1) otkazivanje_VALUE("IOException: write failed");
    }
    static void CALL_metod(int INDEX, int komanda) {
        if (INDEX <= 0 || INDEX >= konstanta_oznaka.length || (konstanta_oznaka[INDEX] != 10 && konstanta_oznaka[INDEX] != 11)) { otkazivanje_VALUE("invalid method reference"); return; }
        int vlasnik_VALUE = ime_klase_SMS(상가[INDEX]), ime = referenca_ime(konstanta_SECOND_VALUE[INDEX]), format_VALUE = referenca_tip(konstanta_SECOND_VALUE[INDEX]);
        if (greška) return;
        if (기본호출(vlasnik_VALUE, ime, format_VALUE, komanda)) return;
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
        int Razred_Definicija = FIND_Razred_Definicija(vlasnik_VALUE); if (Razred_Definicija < 0 || greška) return;
        int Datoteka_INDEX = FIND_metod(Razred_Definicija, ime, format_VALUE);
        if (Datoteka_INDEX < 0) {
            for (int kôd_znaka = Razred_Definicija, stavka_COUNT_8f7753a1 = 0; kôd_znaka >= 0 && stavka_COUNT_8f7753a1 < 16; stavka_COUNT_8f7753a1++, kôd_znaka = nadređen_Razred(kôd_znaka))
                if (Word_SMS(Razred_Definicija_nadređen[kôd_znaka], "java/lang/Thread")) { 가닥호출(ime, format_VALUE, komanda); return; }
            otkazivanje_VALUE("NoSuchMethodError"); return;
        }
        if (((metod_pristup[Datoteka_INDEX] & 8) != 0) != (komanda == 184)) { otkazivanje_VALUE("method static/instance mismatch"); return; }
        if (komanda == 184) { if (!초기화(metod_vlasnik[Datoteka_INDEX], 틀명령[kadar_INDEX])) return; }
        else {
            int 읽는자리 = kadar_stek[kadar_INDEX] - metod_argument_COUNT[Datoteka_INDEX];
            if (읽는자리 < 0 || operand_stek_tip[kadar_INDEX * 128 + 읽는자리] != 2) { otkazivanje_VALUE("invalid method receiver"); return; }
            int objekat_referenca = operand_stek_VALUE[kadar_INDEX * 128 + 읽는자리];
            if (!객체유효(objekat_referenca)) return;
            if (힙[objekat_referenca] < 32 || !종포함(힙[objekat_referenca] - 32, vlasnik_VALUE)) { otkazivanje_VALUE("method receiver type mismatch"); return; }
            if (komanda != 183) Datoteka_INDEX = FIND_metod(힙[objekat_referenca] - 32, ime, format_VALUE);
        }
        if (Datoteka_INDEX < 0 || (metod_pristup[Datoteka_INDEX] & 0x400) != 0) { otkazivanje_VALUE("AbstractMethodError"); return; }
        int zaključati_referenca = 0;
        if ((metod_pristup[Datoteka_INDEX] & 32) != 0) {
            if (komanda == 184) { int kôd_znaka = metod_vlasnik[Datoteka_INDEX]; if (Razred_zaključati[kôd_znaka] == 0) Razred_zaključati[kôd_znaka] = dodeliti_Skladište(8, 0); zaključati_referenca = Razred_zaključati[kôd_znaka]; }
            else zaključati_referenca = operand_stek_VALUE[kadar_INDEX * 128 + kadar_stek[kadar_INDEX] - metod_argument_COUNT[Datoteka_INDEX]];
            if (!잠금얻기(zaključati_referenca)) { if (!greška) kadar_pozicija[kadar_INDEX] = 틀명령[kadar_INDEX]; return; }
        }
        호출(Datoteka_INDEX); if (!greška) kadar_zaključati[kadar_INDEX] = zaključati_referenca;
    }
    static boolean 배열저장가능(int niz_referenca, int podaci_VALUE) {
        if (podaci_VALUE == 0 || element_niza[niz_referenca] == 0) return true;
        boolean 성공여부 = element_niza[niz_referenca] == -1 ? (podaci_VALUE > 0 && podaci_VALUE < 힙끝 && 힙[podaci_VALUE] == 1) : 맞는객체(podaci_VALUE, element_niza[niz_referenca]);
        if (!성공여부 && !greška) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int 배열칸(int referenca, int indeksni_tekst_VALUE, int tip_VALUE) {
        if (!objekat_VALUE(referenca, tip_VALUE)) return 0;
        if (indeksni_tekst_VALUE < 0 || indeksni_tekst_VALUE >= 힙[referenca + 1]) { otkazivanje_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return referenca + 2 + indeksni_tekst_VALUE;
    }
    static void Izvrši_komanda() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (greška) { if (던진객체 != 0) pokazivač_izuzetak(); if (greška || kadar_INDEX < aktuelno_nit * 32) break; }
            if (kadar_INDEX < aktuelno_nit * 32 || promeniti_zahtev || --조각 == 0) { if (!SWITCH_nit()) break; 조각 = 100; }
            if (kadar_INDEX == 0 && Razred_Definicija_Status[stavka_Razred_Definicija] != 2 && !초기화(stavka_Razred_Definicija, kadar_pozicija[kadar_INDEX])) continue;
            if (kadar_INDEX == aktuelno_nit * 32 && aktuelno_nit != 0 && (metod_pristup[kadar_metod[kadar_INDEX]] & 32) != 0 && kadar_zaključati[kadar_INDEX] == 0) {
                int objekat_referenca = nit_cilj[aktuelno_nit]; if (!잠금얻기(objekat_referenca)) { if (greška) break; continue; } kadar_zaključati[kadar_INDEX] = objekat_referenca;
            }
            잠시수 = 0;
            if (--남음 == 0) { otkazivanje_VALUE("instruction limit (500000)"); break; }
            int koristiti = kadar_pozicija[kadar_INDEX]; 틀명령[kadar_INDEX] = koristiti; int VALUE = 명바();
            if (greška) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = metod_vlasnik[kadar_metod[kadar_INDEX]] * 512 + (VALUE == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= konstanta_oznaka.length) otkazivanje_VALUE("invalid ldc constant");
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
            if (VALUE == 46 || VALUE >= 50 && VALUE <= 53) {
                int stavka_pozicija = 빼기(1), objekat_referenca = 빼기(2), oblast_kôd = VALUE == 46 ? 2 : VALUE == 50 ? 3 : VALUE == 51 ? 20 : VALUE == 52 ? 22 : 23;
                if (VALUE == 51 && objekat_referenca > 0 && objekat_referenca < 힙끝 && 힙[objekat_referenca] == 21) oblast_kôd = 21;
                int 읽는자리 = 배열칸(objekat_referenca, stavka_pozicija, oblast_kôd); if (!greška) 넣기(힙[읽는자리], VALUE == 50 ? 2 : 1); continue;
            }
            if (VALUE == 79 || VALUE >= 83 && VALUE <= 86) {
                int stavka_referenca = 빼기(VALUE == 83 ? 2 : 1), stavka_pozicija = 빼기(1), objekat_referenca = 빼기(2), oblast_kôd = VALUE == 79 ? 2 : VALUE == 83 ? 3 : VALUE == 84 ? 20 : VALUE == 85 ? 22 : 23;
                if (VALUE == 84 && objekat_referenca > 0 && objekat_referenca < 힙끝 && 힙[objekat_referenca] == 21) oblast_kôd = 21;
                int 읽는자리 = 배열칸(objekat_referenca, stavka_pozicija, oblast_kôd);
                if (!greška && oblast_kôd == 3 && !배열저장가능(objekat_referenca, stavka_referenca)) continue;
                if (!greška) 힙[읽는자리] = oblast_kôd == 20 ? (byte)stavka_referenca : oblast_kôd == 21 ? stavka_referenca & 1 : oblast_kôd == 22 ? (char)stavka_referenca : oblast_kôd == 23 ? (short)stavka_referenca : stavka_referenca;
                continue;
            }
            if (VALUE >= 87 && VALUE <= 95) { 스택명령(VALUE); continue; }
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
            if (VALUE >= 178 && VALUE <= 181) { 필드호출(명상수(), VALUE, koristiti); continue; }
            if (VALUE >= 182 && VALUE <= 185) {
                int 부호값 = 명상수();
                if (VALUE == 185) { int ukupan_COUNT = 명바(); if (ukupan_COUNT == 0 || 명바() != 0) { otkazivanje_VALUE("invalid invokeinterface operands"); continue; } }
                CALL_metod(부호값, VALUE); continue;
            }
            if (VALUE == 187) { 새객체(ime_klase_SMS(명상수()), koristiti); continue; }
            if (VALUE == 188 || VALUE == 189) {
                int oblast_kôd = 3, komponenta = 0;
                if (VALUE == 188) { int 임시값 = 명바(); oblast_kôd = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else komponenta = ime_klase_SMS(명상수());
                if (oblast_kôd == 0) { otkazivanje_VALUE("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), objekat_referenca = dodeliti_Skladište(oblast_kôd, 유효길이); if (!greška) element_niza[objekat_referenca] = komponenta; 넣기(objekat_referenca, 2); continue;
            }
            if (VALUE == 190) {
                int objekat_referenca = 빼기(2);
                if (객체유효(objekat_referenca)) { int Poređenje_pozicija = 힙[objekat_referenca]; if (Poređenje_pozicija != 2 && Poređenje_pozicija != 3 && (Poređenje_pozicija < 20 || Poređenje_pozicija > 23)) otkazivanje_VALUE("not an array"); else 넣기(힙[objekat_referenca + 1], 1); }
                continue;
            }
            if (VALUE == 191) {
                int objekat_referenca = 빼기(2); if (객체유효(objekat_referenca)) { if (힙[objekat_referenca] != 9) otkazivanje_VALUE("athrow requires supported Throwable"); else { 던진객체 = objekat_referenca; greška = true; } }
                continue;
            }
            if (VALUE == 192 || VALUE == 193) {
                int ime_konstanta = ime_klase_SMS(명상수()), objekat_referenca = 빼기(2); boolean MATCH = 맞는객체(objekat_referenca, ime_konstanta);
                if (VALUE == 193) 넣기(objekat_referenca != 0 && MATCH ? 1 : 0, 1);
                else { if (!MATCH && !greška) otkazivanje_VALUE("ClassCastException"); 넣기(objekat_referenca, 2); }
                continue;
            }
            if (VALUE == 170 || VALUE == 171) {
                int 읽는자리 = koristiti + 1, Datoteka_INDEX = kadar_metod[kadar_INDEX], Ključ_referenca = 빼기(1);
                while ((읽는자리 - metod_START[Datoteka_INDEX]) % 4 != 0) 읽는자리++;
                int cilj_adresa = pozicija_ceo_broj(읽는자리);
                if (VALUE == 170) { int 낮은값 = pozicija_ceo_broj(읽는자리 + 4), 높은값 = pozicija_ceo_broj(읽는자리 + 8); if (Ključ_referenca >= 낮은값 && Ključ_referenca <= 높은값) cilj_adresa = pozicija_ceo_broj(읽는자리 + 12 + (Ključ_referenca - 낮은값) * 4); }
                else { int ukupan_COUNT = pozicija_ceo_broj(읽는자리 + 4); for (int Loop_INDEX = 0; Loop_INDEX < ukupan_COUNT; Loop_INDEX++) if (pozicija_ceo_broj(읽는자리 + 8 + Loop_INDEX * 8) == Ključ_referenca) cilj_adresa = pozicija_ceo_broj(읽는자리 + 12 + Loop_INDEX * 8); }
                premestiti_VALUE(koristiti + cilj_adresa); continue;
            }
            if (VALUE == 200) { premestiti_VALUE(koristiti + pozicija_ceo_broj(koristiti + 1)); continue; }
            if (VALUE == 194 || VALUE == 195) {
                int objekat_referenca = 빼기(2);
                if (VALUE == 195) izdanje_zaključati(objekat_referenca);
                else if (!잠금얻기(objekat_referenca) && !greška) { 넣기(objekat_referenca, 2); kadar_pozicija[kadar_INDEX] = koristiti; }
                continue;
            }
            if (VALUE == 196) {
                int komanda_kôd = 명바(), stavka_pozicija = 명짧();
                if (komanda_kôd == 21 || komanda_kôd == 25) 지역읽기(stavka_pozicija, komanda_kôd == 21 ? 1 : 2);
                else if (komanda_kôd == 54 || komanda_kôd == 58) 지역쓰기(stavka_pozicija, komanda_kôd == 54 ? 1 : 2);
                else if (komanda_kôd == 132) { int DELTA_VALUE = (short)명짧(); 지역읽기(stavka_pozicija, 1); 넣기(빼기(1) + DELTA_VALUE, 1); 지역쓰기(stavka_pozicija, 1); }
                else otkazivanje_VALUE("unsupported wide opcode");
                continue;
            }
            otkazivanje_VALUE("unsupported bytecode");
        }
    }
    static int FIND_Razred_Definicija(int ime) {
        for (int Loop_INDEX = 0; Loop_INDEX < Razred_Definicija_COUNT; Loop_INDEX++) if (Razred_Definicija_ime[Loop_INDEX] != 0 && 같은말(Razred_Definicija_ime[Loop_INDEX], ime)) return Loop_INDEX;
        return zbirka_Razred_Definicija(konstanta_SMS(ime));
    }
    static int zbirka_Razred_Definicija(int ime_niska) {
        if (!objekat_VALUE(ime_niska, 1)) return -1;
        int 길이 = 힙[ime_niska + 1];
        if (길이 < 1 || 길이 > 505 || Razred_Definicija_COUNT == 16) { otkazivanje_VALUE("class name/count limit"); return -1; }
        for (int Loop_INDEX = 0; Loop_INDEX < 길이; Loop_INDEX++) { int kôd_znaka = 힙[ime_niska + 2 + Loop_INDEX]; ime_datoteke_SMS[Loop_INDEX] = kôd_znaka == '/' ? '.' : kôd_znaka; }
        ime_datoteke_SMS[길이] = '.'; ime_datoteke_SMS[길이 + 1] = 'c'; ime_datoteke_SMS[길이 + 2] = 'l'; ime_datoteke_SMS[길이 + 3] = 'a'; ime_datoteke_SMS[길이 + 4] = 's'; ime_datoteke_SMS[길이 + 5] = 's'; ime_datoteke_SMS[길이 + 6] = 0;
        int promeniti_veličinu = korisnik.파일읽기(ime_datoteke_SMS, privremena_datoteka);
        if (promeniti_veličinu < 0) { otkazivanje_VALUE("ClassNotFoundException"); return -1; }
        int Razred_Definicija = Razred_Definicija_COUNT++; Razred_Definicija_promeniti_veličinu[Razred_Definicija] = promeniti_veličinu;
        for (int Loop_INDEX = 0; Loop_INDEX < promeniti_veličinu; Loop_INDEX++) Datoteka[Razred_Definicija * 16384 + Loop_INDEX] = privremena_datoteka[Loop_INDEX];
        클래스읽기(Razred_Definicija); if (greška) return -1;
        int stvarni_podaci = konstanta_SMS(Razred_Definicija_ime[Razred_Definicija]);
        if (!글같음(stvarni_podaci, ime_niska, true)) { otkazivanje_VALUE("class name does not match file"); return -1; }
        int nadređen_VALUE = Razred_Definicija_nadređen[Razred_Definicija];
        if (nadređen_VALUE != 0 && !Word_SMS(nadređen_VALUE, "java/lang/Object") && !Word_SMS(nadređen_VALUE, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 pokušati_ponovo_VALUE 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = FIND_Razred_Definicija(nadređen_VALUE);
            if (greška || 위 < 0) return -1;
            int 읽는자리 = 위, faza_COUNT = 0;
            while (읽는자리 >= 0 && faza_COUNT++ < 16) {
                if (읽는자리 == Razred_Definicija) { otkazivanje_VALUE("cyclic inheritance"); return -1; }
                읽는자리 = nadređen_Razred(읽는자리);
            }
            int 시작변위 = 종칸수[위];
            for (int Datoteka_INDEX = 0; Datoteka_INDEX < 칸수; Datoteka_INDEX++) if (칸주인[Datoteka_INDEX] == Razred_Definicija && (칸권한[Datoteka_INDEX] & 8) == 0) 칸위치[Datoteka_INDEX] += 시작변위;
            종칸수[Razred_Definicija] += 시작변위;
        }
        return Razred_Definicija;
    }
    static int nadređen_Razred(int Razred_Definicija) {
        int ime = Razred_Definicija_nadređen[Razred_Definicija];
        for (int Loop_INDEX = 0; Loop_INDEX < Razred_Definicija_COUNT; Loop_INDEX++) if (ime != 0 && Razred_Definicija_ime[Loop_INDEX] != 0 && 같은말(Razred_Definicija_ime[Loop_INDEX], ime)) return Loop_INDEX;
        return -1;
    }
    static int FIND_metod(int Razred_Definicija, int ime, int format_VALUE) {
        for (int 깊이 = 0; Razred_Definicija >= 0 && 깊이 < 16; 깊이++, Razred_Definicija = nadređen_Razred(Razred_Definicija)) {
            for (int Loop_INDEX = 0; Loop_INDEX < metod_COUNT; Loop_INDEX++) if (metod_vlasnik[Loop_INDEX] == Razred_Definicija && 같은말(metod_ime_SMS[Loop_INDEX], ime) && 같은말(metod_tip[Loop_INDEX], format_VALUE)) return Loop_INDEX;
        }
        return -1;
    }
    static int ime_metod(int Razred_Definicija, String ime, String format_VALUE) {
        for (int 깊이 = 0; Razred_Definicija >= 0 && 깊이 < 16; 깊이++, Razred_Definicija = nadređen_Razred(Razred_Definicija))
            for (int Loop_INDEX = 0; Loop_INDEX < metod_COUNT; Loop_INDEX++) if (metod_vlasnik[Loop_INDEX] == Razred_Definicija && Word_SMS(metod_ime_SMS[Loop_INDEX], ime) && Word_SMS(metod_tip[Loop_INDEX], format_VALUE)) return Loop_INDEX;
        return -1;
    }
    static int 형종류(int ime) { return Datoteka[상가[ime]] == 'L' || Datoteka[상가[ime]] == '[' ? 2 : 1; }
    static boolean 초기화(int Razred_Definicija, int komanda_START) {
        if (Razred_Definicija < 0 || greška) return false;
        if (Razred_Definicija_Status[Razred_Definicija] == 3) { otkazivanje_VALUE("NoClassDefFoundError: initialization failed"); return false; }
        if (Razred_Definicija_Status[Razred_Definicija] == 1 && Razred_nit[Razred_Definicija] != aktuelno_nit) { kadar_pozicija[kadar_INDEX] = komanda_START; promeniti_zahtev = true; return false; }
        if (Razred_Definicija_Status[Razred_Definicija] != 0) return true;
        int 위 = nadređen_Razred(Razred_Definicija);
        if (위 >= 0 && !초기화(위, komanda_START)) return false;
        Razred_Definicija_Status[Razred_Definicija] = 1; Razred_nit[Razred_Definicija] = aktuelno_nit;
        if (종초기화[Razred_Definicija] != 0) {
            kadar_pozicija[kadar_INDEX] = komanda_START;
            호출(종초기화[Razred_Definicija] - 1); if (!greška) 틀초기화[kadar_INDEX] = Razred_Definicija + 1;
            return false;
        }
        Razred_Definicija_Status[Razred_Definicija] = 2; return true;
    }
    static void 필드호출(int INDEX, int komanda, int koristiti) {
        if (!proveriti_konstanta(INDEX, 9)) return;
        int vlasnik_VALUE = ime_klase_SMS(상가[INDEX]), ime = referenca_ime(konstanta_SECOND_VALUE[INDEX]), format_VALUE = referenca_tip(konstanta_SECOND_VALUE[INDEX]);
        if (Word_SMS(vlasnik_VALUE, "java/lang/System") && (Word_SMS(ime, "out") || Word_SMS(ime, "err")) && Word_SMS(format_VALUE, "Ljava/io/PrintStream;") && komanda == 178) { 넣기(-1, 2); return; }
        int Razred_Definicija = FIND_Razred_Definicija(vlasnik_VALUE); if (Razred_Definicija < 0 || greška) return;
        int 찾음 = -1;
        for (int 읽는자리 = Razred_Definicija, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = nadređen_Razred(읽는자리))
            for (int Datoteka_INDEX = 0; Datoteka_INDEX < 칸수; Datoteka_INDEX++) if (칸주인[Datoteka_INDEX] == 읽는자리 && 같은말(칸이름[Datoteka_INDEX], ime) && 같은말(칸형[Datoteka_INDEX], format_VALUE)) 찾음 = Datoteka_INDEX;
        if (찾음 < 0) { otkazivanje_VALUE("NoSuchFieldError"); return; }
        boolean 정적 = komanda == 178 || komanda == 179;
        if (정적 != ((칸권한[찾음] & 8) != 0)) { otkazivanje_VALUE("field static/instance mismatch"); return; }
        if (정적 && !초기화(칸주인[찾음], koristiti)) return;
        int tip_VALUE = 형종류(format_VALUE), VALUE = 0;
        if (komanda == 179 || komanda == 181) VALUE = 빼기(tip_VALUE);
        if (정적) { if (komanda == 178) 넣기(칸값[찾음], tip_VALUE); else if (!greška) 칸값[찾음] = VALUE; return; }
        int objekat_referenca = 빼기(2);
        if (!객체유효(objekat_referenca)) return;
        if (힙[objekat_referenca] < 32 || !종포함(힙[objekat_referenca] - 32, vlasnik_VALUE)) { otkazivanje_VALUE("field receiver type mismatch"); return; }
        int 보관칸 = objekat_referenca + 2 + 칸위치[찾음];
        if (komanda == 180) 넣기(힙[보관칸], tip_VALUE);
        else if (!greška) { 힙[보관칸] = VALUE; 힙참조[보관칸] = tip_VALUE == 2 ? 1 : 0; }
    }
    static boolean 종포함(int Razred_Definicija, int ime) {
        for (int 중첩깊이 = 0; Razred_Definicija >= 0 && 중첩깊이 < 16; 중첩깊이++, Razred_Definicija = nadređen_Razred(Razred_Definicija)) {
            if (같은말(Razred_Definicija_ime[Razred_Definicija], ime) || (Razred_Definicija_nadređen[Razred_Definicija] != 0 && 같은말(Razred_Definicija_nadređen[Razred_Definicija], ime))) return true;
            for (int unutrašnje_pozicija = 0; unutrašnje_pozicija < Razred_interfejs_COUNT[Razred_Definicija]; unutrašnje_pozicija++) if (같은말(Razred_interfejs[Razred_Definicija * 16 + unutrašnje_pozicija], ime)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int bajt_podaci, boolean putanja) {
        if (첫값 == bajt_podaci) return true;
        if (첫값 <= 0 || bajt_podaci <= 0 || 힙[첫값] != 1 || 힙[bajt_podaci] != 1 || 힙[첫값 + 1] != 힙[bajt_podaci + 1]) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) {
            int x_koordinata = 힙[첫값 + 2 + Loop_INDEX], 세로좌표 = 힙[bajt_podaci + 2 + Loop_INDEX];
            if (putanja) { if (x_koordinata == '.') x_koordinata = '/'; if (세로좌표 == '.') 세로좌표 = '/'; }
            if (x_koordinata != 세로좌표) return false;
        }
        return true;
    }
    static boolean 객체유효(int objekat_referenca) {
        if (objekat_referenca == 0) { otkazivanje_VALUE("NullPointerException"); return false; }
        if (objekat_referenca < 1 || objekat_referenca >= 힙끝 || 힙폭[objekat_referenca] < 2 || 힙[objekat_referenca] == 0) { otkazivanje_VALUE("invalid object reference"); return false; }
        return true;
    }
    static void zaštititi_VALUE(int objekat_referenca) {
        if (objekat_referenca > 0 && objekat_referenca < 힙끝 && 힙폭[objekat_referenca] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = objekat_referenca;
    }
    static void emisija_VALUE(int objekat_referenca) {
        if (objekat_referenca > 0 && objekat_referenca < 힙끝 && 힙폭[objekat_referenca] >= 2 && 힙[objekat_referenca] != 0 && 힙표시[objekat_referenca] == 0) {
            힙표시[objekat_referenca] = 1; 표시대기[ekran_COUNT++] = objekat_referenca;
        }
    }
    static void 수거() {
        ekran_COUNT = 0; korpus_COUNT++;
        for (int proveriti_pozicija = 1; proveriti_pozicija < 힙끝; proveriti_pozicija += 힙폭[proveriti_pozicija]) 힙표시[proveriti_pozicija] = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < niska_referenca.length; Loop_INDEX++) emisija_VALUE(niska_referenca[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 칸수; Loop_INDEX++) if ((칸권한[Loop_INDEX] & 8) != 0 && 형종류(칸형[Loop_INDEX]) == 2) emisija_VALUE(칸값[Loop_INDEX]);
        for (int 임시값 = 0; 임시값 < nit_COUNT; 임시값++) {
            emisija_VALUE(nit_objekat[임시값]); emisija_VALUE(nit_cilj[임시값]);
            int 꼭대기자리 = 임시값 == aktuelno_nit ? kadar_INDEX : nit_kadar[임시값];
            for (int Datoteka_INDEX = 임시값 * 32; Datoteka_INDEX <= 꼭대기자리; Datoteka_INDEX++) {
                for (int unutrašnje_pozicija = 0; unutrašnje_pozicija < 함수지역[kadar_metod[Datoteka_INDEX]]; unutrašnje_pozicija++) if (lokalni_tip[Datoteka_INDEX * 128 + unutrašnje_pozicija] == 2) emisija_VALUE(lokalni_VALUE[Datoteka_INDEX * 128 + unutrašnje_pozicija]);
                for (int unutrašnje_pozicija = 0; unutrašnje_pozicija < kadar_stek[Datoteka_INDEX]; unutrašnje_pozicija++) if (operand_stek_tip[Datoteka_INDEX * 128 + unutrašnje_pozicija] == 2) emisija_VALUE(operand_stek_VALUE[Datoteka_INDEX * 128 + unutrašnje_pozicija]);
            }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 화면참조.length; Loop_INDEX++) emisija_VALUE(화면참조[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 나중수; Loop_INDEX++) emisija_VALUE(나중실행[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Store_ceo_broj.length; Loop_INDEX++) emisija_VALUE(Store_ceo_broj[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Razred_Definicija_COUNT; Loop_INDEX++) emisija_VALUE(Razred_zaključati[Loop_INDEX]);
        for (int proveriti_pozicija = 1; proveriti_pozicija < 힙끝; proveriti_pozicija += 힙폭[proveriti_pozicija]) if (잠금깊이[proveriti_pozicija] > 0) emisija_VALUE(proveriti_pozicija);
        emisija_VALUE(던진객체);
        for (int Loop_INDEX = 0; Loop_INDEX < 잠시수; Loop_INDEX++) emisija_VALUE(잠시참조[Loop_INDEX]);
        while (ekran_COUNT > 0) {
            int objekat_referenca = 표시대기[--ekran_COUNT], oblast_kôd = 힙[objekat_referenca];
            for (int Loop_INDEX = objekat_referenca + 2; Loop_INDEX < objekat_referenca + 힙폭[objekat_referenca]; Loop_INDEX++) if (oblast_kôd == 3 || oblast_kôd == 4 || 힙참조[Loop_INDEX] != 0) emisija_VALUE(힙[Loop_INDEX]);
        }
        for (int proveriti_pozicija = 1; proveriti_pozicija < 힙끝; proveriti_pozicija += 힙폭[proveriti_pozicija]) if (힙표시[proveriti_pozicija] == 0) 힙[proveriti_pozicija] = 0;
        for (int proveriti_pozicija = 1; proveriti_pozicija < 힙끝; proveriti_pozicija += 힙폭[proveriti_pozicija]) if (힙[proveriti_pozicija] == 0) {
            while (proveriti_pozicija + 힙폭[proveriti_pozicija] < 힙끝 && 힙[proveriti_pozicija + 힙폭[proveriti_pozicija]] == 0) { int Dalje_pozicija = proveriti_pozicija + 힙폭[proveriti_pozicija]; 힙폭[proveriti_pozicija] += 힙폭[Dalje_pozicija]; 힙폭[Dalje_pozicija] = 0; }
            if (proveriti_pozicija + 힙폭[proveriti_pozicija] == 힙끝) { 힙끝 = proveriti_pozicija; break; }
        }
    }
    static int 새기억(int 종류, int 길이) {
        if (길이 < 0) { otkazivanje_VALUE("NegativeArraySizeException"); return 0; }
        if (길이 > 힙.length - 3) { otkazivanje_VALUE("object heap exhausted"); return 0; }
        int 필요수 = 길이 + 2, objekat_referenca = 0;
        if (필요수 <= 힙.length - 힙끝) { objekat_referenca = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { objekat_referenca = 읽는자리; break; }
            if (objekat_referenca != 0) {
                int 남은길이 = 힙폭[objekat_referenca] - 필요수;
                if (남은길이 >= 2) { 힙폭[objekat_referenca + 필요수] = 남은길이; 힙[objekat_referenca + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { objekat_referenca = 힙끝; 힙끝 += 필요수; }
        }
        if (objekat_referenca == 0) { otkazivanje_VALUE("object heap exhausted"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < 필요수; Loop_INDEX++) { 힙[objekat_referenca + Loop_INDEX] = 0; 힙참조[objekat_referenca + Loop_INDEX] = 0; 힙폭[objekat_referenca + Loop_INDEX] = 0; }
        element_niza[objekat_referenca] = 0;
        힙폭[objekat_referenca] = 필요수; 힙[objekat_referenca] = 종류; 힙[objekat_referenca + 1] = 길이; zaštititi_VALUE(objekat_referenca); return objekat_referenca;
    }
    static int izuzetak_Razred(String ime_konstanta) {
        if (자바도구.같음(ime_konstanta, "java/lang/Throwable")) return 1;
        if (자바도구.같음(ime_konstanta, "java/lang/Exception")) return 2;
        if (자바도구.같음(ime_konstanta, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(ime_konstanta, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(ime_konstanta, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(ime_konstanta, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(ime_konstanta, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(ime_konstanta, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(ime_konstanta, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(ime_konstanta, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(ime_konstanta, "java/io/IOException")) return 11;
        if (자바도구.같음(ime_konstanta, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(ime_konstanta, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(ime_konstanta, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(ime_konstanta, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int izuzetak_konstanta(int ime) {
        for (int Loop_INDEX = 1; Loop_INDEX <= 41; Loop_INDEX++) if (Word_SMS(ime, izuzetak_ime(Loop_INDEX))) return Loop_INDEX;
        return 0;
    }
    static String izuzetak_ime(int nalog_VALUE) {
        if (nalog_VALUE == 40) return "java/lang/InterruptedException";
        if (nalog_VALUE == 41) return "한국어/자체/대기중단예외";
        if (nalog_VALUE == 39) return "java/net/SocketException";
        if (nalog_VALUE == 20) return "한국어/자체/izuzetak";
        if (nalog_VALUE == 21) return "한국어/자체/실행예외";
        if (nalog_VALUE == 22) return "한국어/자체/U_I_izuzetak";
        if (nalog_VALUE == 23) return "한국어/자체/čekaj_TIMEOUT_izuzetak";
        if (nalog_VALUE == 24) return "한국어/자체/adresa_LOOKUP_izuzetak";
        if (nalog_VALUE == 25) return "한국어/자체/파일없음예외";
        if (nalog_VALUE == 26) return "한국어/자체/통신예외";
        if (nalog_VALUE == 27) return "한국어/자체/nevažeći_argument_izuzetak";
        if (nalog_VALUE == 28) return "한국어/자체/숫자형식예외";
        if (nalog_VALUE == 29) return "한국어/자체/범위예외";
        if (nalog_VALUE == 30) return "한국어/자체/배열범위예외";
        if (nalog_VALUE == 31) return "한국어/자체/문자열범위예외";
        if (nalog_VALUE == 32) return "한국어/자체/NULL_referenca_izuzetak";
        if (nalog_VALUE == 33) return "한국어/자체/산술예외";
        if (nalog_VALUE == 34) return "한국어/자체/Status_izuzetak";
        if (nalog_VALUE == 35) return "한국어/자체/tip_Emitovanje_izuzetak";
        if (nalog_VALUE == 36) return "한국어/자체/음수배열크기예외";
        if (nalog_VALUE == 37) return "한국어/자체/niz_Store_otkazivanje";
        if (nalog_VALUE == 38) return "한국어/자체/nit_Status_izuzetak";
        if (nalog_VALUE == 1) return "java/lang/Throwable"; if (nalog_VALUE == 2) return "java/lang/Exception";
        if (nalog_VALUE == 3) return "java/lang/RuntimeException"; if (nalog_VALUE == 4) return "java/lang/ArithmeticException";
        if (nalog_VALUE == 5) return "java/lang/NullPointerException"; if (nalog_VALUE == 6) return "java/lang/IndexOutOfBoundsException";
        if (nalog_VALUE == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (nalog_VALUE == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (nalog_VALUE == 9) return "java/lang/IllegalArgumentException"; if (nalog_VALUE == 10) return "java/lang/NumberFormatException";
        if (nalog_VALUE == 11) return "java/io/IOException"; if (nalog_VALUE == 12) return "java/io/FileNotFoundException";
        if (nalog_VALUE == 17) return "java/lang/ArrayStoreException";
        if (nalog_VALUE == 18) return "java/net/UnknownHostException";
        if (nalog_VALUE == 19) return "java/net/SocketTimeoutException";
        if (nalog_VALUE == 16) return "java/lang/IllegalThreadStateException";
        if (nalog_VALUE == 13) return "java/lang/IllegalStateException"; if (nalog_VALUE == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int izuzetak_nadređen(int nalog_VALUE) {
        if (nalog_VALUE == 40) return 2;
        if (nalog_VALUE == 41) return 40;
        if (nalog_VALUE == 39) return 11;
        if (nalog_VALUE == 1) return 0;
        if (nalog_VALUE == 2) return 1;
        if (nalog_VALUE == 3) return 2;
        if (nalog_VALUE == 4) return 3;
        if (nalog_VALUE == 5) return 3;
        if (nalog_VALUE == 6) return 3;
        if (nalog_VALUE == 7) return 6;
        if (nalog_VALUE == 8) return 6;
        if (nalog_VALUE == 9) return 3;
        if (nalog_VALUE == 10) return 9;
        if (nalog_VALUE == 11) return 2;
        if (nalog_VALUE == 12) return 11;
        if (nalog_VALUE == 13) return 3;
        if (nalog_VALUE == 14) return 3;
        if (nalog_VALUE == 15) return 3;
        if (nalog_VALUE == 16) return 9;
        if (nalog_VALUE == 17) return 3;
        if (nalog_VALUE == 18) return 11;
        if (nalog_VALUE == 19) return 11;
        if (nalog_VALUE == 20) return 2;
        if (nalog_VALUE == 21) return 3;
        if (nalog_VALUE == 22) return 11;
        if (nalog_VALUE == 23) return 22;
        if (nalog_VALUE == 24) return 22;
        if (nalog_VALUE == 25) return 22;
        if (nalog_VALUE == 26) return 22;
        if (nalog_VALUE == 27) return 9;
        if (nalog_VALUE == 28) return 27;
        if (nalog_VALUE == 29) return 6;
        if (nalog_VALUE == 30) return 29;
        if (nalog_VALUE == 31) return 29;
        if (nalog_VALUE == 32) return 5;
        if (nalog_VALUE == 33) return 4;
        if (nalog_VALUE == 34) return 13;
        if (nalog_VALUE == 35) return 14;
        if (nalog_VALUE == 36) return 15;
        if (nalog_VALUE == 37) return 17;
        if (nalog_VALUE == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int stvarna_vrednost, int 요구값) {
        for (int 깊이 = 0; stvarna_vrednost != 0 && 깊이 < 16; 깊이++, stvarna_vrednost = izuzetak_nadređen(stvarna_vrednost))
            if (stvarna_vrednost == 요구값) return true;
        return false;
    }
    static void 예외던짐(int nalog_VALUE, String 안내참조) {
        int objekat_referenca = 새기억(9, 2); if (greška) return;
        힙[objekat_referenca + 2] = nalog_VALUE; 힙[objekat_referenca + 3] = host_znak(안내참조); 힙참조[objekat_referenca + 3] = 1;
        던진객체 = objekat_referenca; greška = true;
    }
    static boolean 맞는객체(int objekat_referenca, int ime) {
        if (objekat_referenca == 0) return true;
        if (!객체유효(objekat_referenca)) return false;
        int oblast_kôd = 힙[objekat_referenca];
        if (Word_SMS(ime, "java/lang/Object")) return true;
        if (oblast_kôd >= 32) return 종포함(oblast_kôd - 32, ime);
        if (oblast_kôd == 9) { int cilj_adresa = izuzetak_konstanta(ime); return cilj_adresa != 0 && 예외포함(힙[objekat_referenca + 2], cilj_adresa); }
        if (oblast_kôd == 1) return Word_SMS(ime, "java/lang/String") || Word_SMS(ime, "java/lang/CharSequence");
        if (oblast_kôd == 4) return Word_SMS(ime, "java/lang/StringBuilder") || Word_SMS(ime, "java/lang/CharSequence");
        if (oblast_kôd == 10) return Word_SMS(ime, "java/util/ArrayList") || Word_SMS(ime, "java/util/List");
        if (oblast_kôd == 11) return Word_SMS(ime, "java/util/HashMap") || Word_SMS(ime, "java/util/Map");
        if (oblast_kôd == 12) return Word_SMS(ime, "java/lang/Integer") || Word_SMS(ime, "java/lang/Number");
        if (oblast_kôd >= 24 && oblast_kôd <= 28 && 힙[objekat_referenca + 13] != 0) return 한국어화면종(ime) == oblast_kôd || Word_SMS(ime, "한국어/자체/화면구성요소");
        if (oblast_kôd >= 24 && oblast_kôd <= 28) return (한국어화면종(ime) == 0 && 화면종(ime) == oblast_kôd) || Word_SMS(ime, "java/awt/Component") || Word_SMS(ime, "java/awt/Container") || Word_SMS(ime, "javax/swing/JComponent");
        if (oblast_kôd == 29) return Word_SMS(ime, 힙[objekat_referenca + 3] != 0 ? "한국어/자체/radnja_obaveštavanje" : "java/awt/event/ActionEvent");
        if (oblast_kôd == 30) return Word_SMS(ime, "java/awt/FlowLayout") || Word_SMS(ime, "java/awt/LayoutManager");
        if (oblast_kôd == 17) return Word_SMS(ime, "java/net/Socket");
        if (oblast_kôd == 18) return Word_SMS(ime, "java/net/ServerSocket");
        if (oblast_kôd == 19) return Word_SMS(ime, 힙[objekat_referenca + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (oblast_kôd == 14) return Word_SMS(ime, "java/net/InetAddress");
        if (oblast_kôd == 15) return Word_SMS(ime, "java/net/DatagramSocket");
        if (oblast_kôd == 16) return Word_SMS(ime, "java/net/DatagramPacket");
        if (oblast_kôd == 13) return Word_SMS(ime, 힙[objekat_referenca + 3] != 0 ? "한국어/자체/작업가닥" : "java/lang/Thread");
        if (oblast_kôd == 2) return Word_SMS(ime, "[I"); if (oblast_kôd == 20) return Word_SMS(ime, "[B"); if (oblast_kôd == 21) return Word_SMS(ime, "[Z");
        if (oblast_kôd == 22) return Word_SMS(ime, "[C"); if (oblast_kôd == 23) return Word_SMS(ime, "[S");
        if (oblast_kôd != 3) return false;
        if (Word_SMS(ime, "[Ljava/lang/Object;")) return true;
        int komponenta = element_niza[objekat_referenca];
        if (komponenta == -1) return Word_SMS(ime, "[Ljava/lang/String;") || Word_SMS(ime, "[Ljava/lang/CharSequence;");
        if (komponenta == 0) return false;
        if (배열종비교(komponenta, ime)) return true;
        if ((Word_SMS(komponenta, "java/lang/String") || Word_SMS(komponenta, "java/lang/StringBuilder")) && Word_SMS(ime, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDEX = 0; Loop_INDEX < Razred_Definicija_COUNT; Loop_INDEX++) if (같은말(Razred_Definicija_ime[Loop_INDEX], komponenta)) {
            for (int kôd_znaka = Loop_INDEX, 중첩깊이 = 0; kôd_znaka >= 0 && 중첩깊이 < 16; 중첩깊이++, kôd_znaka = nadređen_Razred(kôd_znaka)) {
                if (배열종비교(Razred_Definicija_nadređen[kôd_znaka], ime)) return true;
                for (int unutrašnje_pozicija = 0; unutrašnje_pozicija < Razred_interfejs_COUNT[kôd_znaka]; unutrašnje_pozicija++) if (배열종비교(Razred_interfejs[kôd_znaka * 16 + unutrašnje_pozicija], ime)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int ime_konstanta, int 형식참조) {
        int proveriti_pozicija = 상가[형식참조], stavka_COUNT_8f7753a1 = konstanta_SECOND_VALUE[형식참조];
        if (ime_konstanta == 0 || stavka_COUNT_8f7753a1 < 4 || Datoteka[proveriti_pozicija] != '[' || Datoteka[proveriti_pozicija + 1] != 'L' || Datoteka[proveriti_pozicija + stavka_COUNT_8f7753a1 - 1] != ';' || konstanta_SECOND_VALUE[ime_konstanta] != stavka_COUNT_8f7753a1 - 3) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < stavka_COUNT_8f7753a1 - 3; Loop_INDEX++) if (Datoteka[상가[ime_konstanta] + Loop_INDEX] != Datoteka[proveriti_pozicija + 2 + Loop_INDEX]) return false;
        return true;
    }
    static void pokazivač_izuzetak() {
        if (던진객체 == 0) return;
        greška = false;
        while (kadar_INDEX >= aktuelno_nit * 32) {
            int Datoteka_INDEX = kadar_metod[kadar_INDEX], 읽는자리 = 틀명령[kadar_INDEX];
            for (int Loop_INDEX = 0; Loop_INDEX < 잡기수; Loop_INDEX++) if (잡기함수[Loop_INDEX] == Datoteka_INDEX && 읽는자리 >= 잡기시작[Loop_INDEX] && 읽는자리 < 잡기끝[Loop_INDEX]
                && (잡기종[Loop_INDEX] == 0 || 맞는객체(던진객체, 잡기종[Loop_INDEX]))) {
                kadar_pozicija[kadar_INDEX] = 잡기위치[Loop_INDEX]; kadar_stek[kadar_INDEX] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (틀초기화[kadar_INDEX] != 0) Razred_Definicija_Status[틀초기화[kadar_INDEX] - 1] = 3;
            if (kadar_zaključati[kadar_INDEX] != 0) { izdanje_zaključati(kadar_zaključati[kadar_INDEX]); kadar_zaključati[kadar_INDEX] = 0; }
            kadar_INDEX--;
        }
        korisnik.쓰기("Uncaught ");
        if (힙[던진객체] == 9) { korisnik.쓰기(izuzetak_ime(힙[던진객체 + 2])); korisnik.쓰기(": "); 글쓰기(힙[던진객체 + 3]); }
        else korisnik.쓰기("user exception");
        korisnik.문자쓰기(10); 던진객체 = 0; greška = true;
    }
    // 이 JVM의 operand_stek 항목은 aktuelno_stavka category-1(int/reference)만 허용한다.
    static void 스택명령(int komanda_kôd) {
        int 첫값 = 빼기(0), 첫형식 = vratiti_tip;
        if (komanda_kôd == 87) return;
        if (komanda_kôd == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int bajt_podaci = 빼기(0), SECOND_format = vratiti_tip;
        if (komanda_kôd == 88) return;
        if (komanda_kôd == 90) { 넣기(첫값, 첫형식); 넣기(bajt_podaci, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (komanda_kôd == 92) { 넣기(bajt_podaci, SECOND_format); 넣기(첫값, 첫형식); 넣기(bajt_podaci, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (komanda_kôd == 95) { 넣기(첫값, 첫형식); 넣기(bajt_podaci, SECOND_format); return; }
        int kôd_znaka = 빼기(0), 셋째형식 = vratiti_tip;
        if (komanda_kôd == 91) { 넣기(첫값, 첫형식); 넣기(kôd_znaka, 셋째형식); 넣기(bajt_podaci, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (komanda_kôd == 93) { 넣기(bajt_podaci, SECOND_format); 넣기(첫값, 첫형식); 넣기(kôd_znaka, 셋째형식); 넣기(bajt_podaci, SECOND_format); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = vratiti_tip;
        넣기(bajt_podaci, SECOND_format); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(kôd_znaka, 셋째형식); 넣기(bajt_podaci, SECOND_format); 넣기(첫값, 첫형식);
    }
    static void 새객체(int ime_konstanta, int 시작점) {
        int oblast_kôd = 0, 유효길이 = 0, izuzetak_referenca = izuzetak_konstanta(ime_konstanta);
        if (Word_SMS(ime_konstanta, "java/lang/StringBuilder")) { oblast_kôd = 4; 유효길이 = 1; }
        if (Word_SMS(ime_konstanta, "java/io/FileInputStream")) { oblast_kôd = 5; 유효길이 = 2; }
        if (Word_SMS(ime_konstanta, "java/io/FileOutputStream")) { oblast_kôd = 6; 유효길이 = 2; }
        if (izuzetak_referenca != 0) { oblast_kôd = 9; 유효길이 = 2; }
        if (Word_SMS(ime_konstanta, "java/util/ArrayList")) { oblast_kôd = 10; 유효길이 = 2; }
        if (Word_SMS(ime_konstanta, "java/util/HashMap")) { oblast_kôd = 11; 유효길이 = 2; }
        if (Word_SMS(ime_konstanta, "java/lang/Integer")) { oblast_kôd = 12; 유효길이 = 1; }
        if (Word_SMS(ime_konstanta, "java/net/Socket")) { oblast_kôd = 17; 유효길이 = 5; }
        if (Word_SMS(ime_konstanta, "java/net/ServerSocket")) { oblast_kôd = 18; 유효길이 = 5; }
        if (Word_SMS(ime_konstanta, "java/net/DatagramSocket")) { oblast_kôd = 15; 유효길이 = 3; }
        if (Word_SMS(ime_konstanta, "java/net/DatagramPacket")) { oblast_kôd = 16; 유효길이 = 4; }
        if (Word_SMS(ime_konstanta, "java/lang/Thread") || Word_SMS(ime_konstanta, "한국어/자체/작업가닥")) { oblast_kôd = 13; 유효길이 = 2; }
        if (Word_SMS(ime_konstanta, "java/lang/Object")) { oblast_kôd = 8; }
        if (oblast_kôd == 0 && 화면종(ime_konstanta) != 0) { oblast_kôd = 화면종(ime_konstanta); 유효길이 = 12; }
        if (oblast_kôd == 0) {
            int kôd_znaka = FIND_Razred_Definicija(ime_konstanta); if (kôd_znaka < 0 || greška || !초기화(kôd_znaka, 시작점)) return;
            oblast_kôd = 32 + kôd_znaka; 유효길이 = 종칸수[kôd_znaka];
        }
        int objekat_referenca = dodeliti_Skladište(oblast_kôd, 유효길이); if (greška) return;
        if (oblast_kôd == 13 && Word_SMS(ime_konstanta, "한국어/자체/작업가닥")) 힙[objekat_referenca + 3] = 1;
        if (oblast_kôd >= 24 && oblast_kôd <= 28 && 한국어화면종(ime_konstanta) != 0) 힙[objekat_referenca + 13] = 1;
        if (oblast_kôd == 5 || oblast_kôd == 6 || oblast_kôd == 15 || oblast_kôd == 17 || oblast_kôd == 18) 힙[objekat_referenca + 2] = -1;
        if (oblast_kôd == 9) 힙[objekat_referenca + 2] = izuzetak_referenca;
        넣기(objekat_referenca, 2);
    }
    static boolean 값같음(int 첫값, int bajt_podaci) {
        if (첫값 == bajt_podaci) return true;
        if (첫값 == 0 || bajt_podaci == 0 || 첫값 < 0 || bajt_podaci < 0 || 첫값 >= 힙끝 || bajt_podaci >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[bajt_podaci] == 1) return 글같음(첫값, bajt_podaci, false);
        return 힙[첫값] == 12 && 힙[bajt_podaci] == 12 && 힙[첫값 + 2] == 힙[bajt_podaci + 2];
    }
    static int 글조각(int objekat_referenca, int START_pozicija, int završiti_razgovor_pozicija) {
        if (!objekat_VALUE(objekat_referenca, 1)) return 0;
        if (START_pozicija < 0 || završiti_razgovor_pozicija < START_pozicija || završiti_razgovor_pozicija > 힙[objekat_referenca + 1]) { otkazivanje_VALUE("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = dodeliti_Skladište(1, završiti_razgovor_pozicija - START_pozicija); if (greška) return 0;
        for (int Loop_INDEX = START_pozicija; Loop_INDEX < završiti_razgovor_pozicija; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX - START_pozicija] = 힙[objekat_referenca + 2 + Loop_INDEX];
        return 반환값;
    }
    static int spoj_SMS(int 첫값, int bajt_podaci) {
        if (!objekat_VALUE(첫값, 1) || !objekat_VALUE(bajt_podaci, 1)) return 0;
        int stavka_COUNT_8f7753a1 = 힙[첫값 + 1], metod_INDEX = 힙[bajt_podaci + 1], 반환값 = dodeliti_Skladište(1, stavka_COUNT_8f7753a1 + metod_INDEX); if (greška) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < stavka_COUNT_8f7753a1; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 힙[첫값 + 2 + Loop_INDEX];
        for (int Loop_INDEX = 0; Loop_INDEX < metod_INDEX; Loop_INDEX++) 힙[반환값 + 2 + stavka_COUNT_8f7753a1 + Loop_INDEX] = 힙[bajt_podaci + 2 + Loop_INDEX];
        return 반환값;
    }
    static boolean 기본호출(int vlasnik, int ime_konstanta, int 서술상수, int komanda_kôd) {
        if (Word_SMS(vlasnik, "한국어/자체/실행인수") && komanda_kôd == 184) {
            if (Word_SMS(ime_konstanta, "stavka_COUNT") && Word_SMS(서술상수, "()I")) { 넣기(korisnik.인수개수() - 1, 1); return true; }
            if (Word_SMS(ime_konstanta, "SMS") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= korisnik.인수개수() - 1) 예외던짐(29, "Izvrši_komanda 인수 범위를 벗어났습니다");
                else 넣기(host_znak(korisnik.인수(순번 + 1)), 2);
                return true;
            }
            otkazivanje_VALUE("지원하지 않는 한국어 Izvrši_komanda 인수 호출"); return true;
        }
        if (Word_SMS(vlasnik, "한국어/자체/작업가닥")) { Proces_nit(ime_konstanta, 서술상수, komanda_kôd, true); return true; }
        if (한국어화면소유(vlasnik)) { 한국어화면호출(vlasnik, ime_konstanta, 서술상수, komanda_kôd); return true; }
        if (화면소유(vlasnik)) { 화면호출(vlasnik, ime_konstanta, 서술상수, komanda_kôd); return true; }
        if (Word_SMS(vlasnik, "java/net/Socket") || Word_SMS(vlasnik, "java/net/ServerSocket") || Word_SMS(vlasnik, "java/io/InputStream") || Word_SMS(vlasnik, "java/io/OutputStream")) { 흐름호출(vlasnik, ime_konstanta, 서술상수, komanda_kôd); return true; }
        if (Word_SMS(vlasnik, "한국어/자체/jezgro_VALUE") && komanda_kôd == 184) {
            if (Word_SMS(ime_konstanta, "화면너비") && Word_SMS(서술상수, "()I")) { 넣기(korisnik.화면너비(), 1); return true; }
            if (Word_SMS(ime_konstanta, "화면높이") && Word_SMS(서술상수, "()I")) { 넣기(korisnik.화면높이(), 1); return true; }
            if (Word_SMS(ime_konstanta, "밀리초") && Word_SMS(서술상수, "()I")) { 넣기(korisnik.밀리초(), 1); return true; }
            if (Word_SMS(ime_konstanta, "그림대기") && Word_SMS(서술상수, "()I")) { 넣기(korisnik.그림대기(), 1); return true; }
            if (Word_SMS(ime_konstanta, "사각형") && Word_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), x_koordinata = 빼기(1); 넣기(korisnik.사각형(x_koordinata, 세로좌표, 너비, 높이, 색상), 1); return true; }
        }
        if (Word_SMS(vlasnik, "java/net/InetAddress") || Word_SMS(vlasnik, "java/net/DatagramPacket") || Word_SMS(vlasnik, "java/net/DatagramSocket")) { 통신호출(vlasnik, ime_konstanta, 서술상수, komanda_kôd); return true; }
        if (Word_SMS(vlasnik, "java/lang/Thread")) { 가닥호출(ime_konstanta, 서술상수, komanda_kôd); return true; }
        if (Word_SMS(vlasnik, "java/lang/Object")) {
            if (Word_SMS(ime_konstanta, "<init>") && Word_SMS(서술상수, "()V") && komanda_kôd == 183) { 객체유효(빼기(2)); return true; }
            if (Word_SMS(ime_konstanta, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int bajt_podaci = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == bajt_podaci ? 1 : 0, 1); return true; }
        }
        if (izuzetak_konstanta(vlasnik) != 0) {
            if (Word_SMS(ime_konstanta, "<init>") && komanda_kôd == 183 && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int odziv = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), objekat_referenca = 빼기(2);
                if (objekat_VALUE(objekat_referenca, 9)) { 힙[objekat_referenca + 3] = odziv; 힙참조[objekat_referenca + 3] = 1; } return true;
            }
            if ((Word_SMS(ime_konstanta, "getMessage") || Word_SMS(ime_konstanta, "설명")) && Word_SMS(서술상수, "()Ljava/lang/String;")) { int objekat_referenca = 빼기(2); if (objekat_VALUE(objekat_referenca, 9)) 넣기(힙[objekat_referenca + 3], 2); return true; }
        }
        if (Word_SMS(vlasnik, "java/lang/String")) {
            if (komanda_kôd == 182 && Word_SMS(ime_konstanta, "getBytes") && (Word_SMS(서술상수, "()[B") || Word_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int kodiranje_ime = Word_SMS(서술상수, "()[B") ? 0 : 빼기(2), objekat_referenca = 빼기(2);
                if (!objekat_VALUE(objekat_referenca, 1)) return true;
                if (kodiranje_ime != 0 && !글같음(kodiranje_ime, host_znak("UTF-8"), false) && !글같음(kodiranje_ime, host_znak("UTF8"), false) && !글같음(kodiranje_ime, host_znak("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int stavka_COUNT_8f7753a1 = 힙[objekat_referenca + 1], 반환값 = dodeliti_Skladište(20, stavka_COUNT_8f7753a1 * 3), 사용수 = 0; if (greška) return true;
                for (int unutrašnje_pozicija = 0; unutrašnje_pozicija < stavka_COUNT_8f7753a1; unutrašnje_pozicija++) {
                    int kôd_znaka = 힙[objekat_referenca + 2 + unutrašnje_pozicija];
                    if (kôd_znaka >= 0xd800 && kôd_znaka <= 0xdbff && unutrašnje_pozicija + 1 < stavka_COUNT_8f7753a1 && 힙[objekat_referenca + 3 + unutrašnje_pozicija] >= 0xdc00 && 힙[objekat_referenca + 3 + unutrašnje_pozicija] <= 0xdfff) kôd_znaka = 0x10000 + ((kôd_znaka - 0xd800) << 10) + 힙[objekat_referenca + 2 + ++unutrašnje_pozicija] - 0xdc00;
                    else if (kôd_znaka >= 0xd800 && kôd_znaka <= 0xdfff) kôd_znaka = '?';
                    if (kôd_znaka < 128) 힙[반환값 + 2 + 사용수++] = kôd_znaka;
                    else { int bajt_COUNT = kôd_znaka < 2048 ? 2 : kôd_znaka < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((bajt_COUNT == 2 ? 192 : bajt_COUNT == 3 ? 224 : 240) | kôd_znaka >> (6 * (bajt_COUNT - 1))); for (int Poređenje_pozicija = bajt_COUNT - 1; Poređenje_pozicija > 0; Poređenje_pozicija--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | kôd_znaka >> (6 * (Poređenje_pozicija - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (komanda_kôd == 184 && Word_SMS(ime_konstanta, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(cifra_znak(빼기(1)), 2); return true; }
            if (komanda_kôd != 182) return false;
            if (Word_SMS(ime_konstanta, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int bajt_podaci = 빼기(2), 첫값 = 빼기(2); if (objekat_VALUE(첫값, 1)) 넣기(글같음(첫값, bajt_podaci, false) ? 1 : 0, 1); return true; }
            if (Word_SMS(ime_konstanta, "isEmpty") && Word_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (objekat_VALUE(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_SMS(ime_konstanta, "substring") && (Word_SMS(서술상수, "(I)Ljava/lang/String;") || Word_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SECOND_VALUE = Word_SMS(서술상수, "(II)Ljava/lang/String;"); int završiti_razgovor_pozicija = SECOND_VALUE ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (objekat_VALUE(첫값, 1)) 넣기(글조각(첫값, 시작점, SECOND_VALUE ? završiti_razgovor_pozicija : 힙[첫값 + 1]), 2); return true;
            }
            if (Word_SMS(ime_konstanta, "concat") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int bajt_podaci = 빼기(2), 첫값 = 빼기(2); 넣기(spoj_SMS(첫값, bajt_podaci), 2); return true; }
            if (Word_SMS(ime_konstanta, "hashCode") && Word_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), heš_VALUE = 0; if (objekat_VALUE(첫값, 1)) { for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) heš_VALUE = heš_VALUE * 31 + 힙[첫값 + 2 + Loop_INDEX]; 넣기(heš_VALUE, 1); } return true; }
            if (Word_SMS(ime_konstanta, "toString") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (objekat_VALUE(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_SMS(vlasnik, "java/lang/Integer")) {
            if (komanda_kôd == 184 && Word_SMS(ime_konstanta, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int podaci_VALUE = 빼기(1), objekat_referenca = podaci_VALUE >= -128 && podaci_VALUE <= 127 ? Store_ceo_broj[podaci_VALUE + 128] : 0; if (objekat_referenca == 0) { objekat_referenca = dodeliti_Skladište(12, 1); if (!greška) { 힙[objekat_referenca + 2] = podaci_VALUE; if (podaci_VALUE >= -128 && podaci_VALUE <= 127) Store_ceo_broj[podaci_VALUE + 128] = objekat_referenca; } } 넣기(objekat_referenca, 2); return true; }
            if (komanda_kôd == 183 && Word_SMS(ime_konstanta, "<init>") && Word_SMS(서술상수, "(I)V")) { int podaci_VALUE = 빼기(1), objekat_referenca = 빼기(2); if (objekat_VALUE(objekat_referenca, 12)) 힙[objekat_referenca + 2] = podaci_VALUE; return true; }
            if (komanda_kôd == 182 && Word_SMS(ime_konstanta, "intValue") && Word_SMS(서술상수, "()I")) { int objekat_referenca = 빼기(2); if (objekat_VALUE(objekat_referenca, 12)) 넣기(힙[objekat_referenca + 2], 1); return true; }
            if (komanda_kôd == 184 && Word_SMS(ime_konstanta, "toString") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(cifra_znak(빼기(1)), 2); return true; }
        }
        if (Word_SMS(vlasnik, "java/lang/Math") && komanda_kôd == 184) {
            if (Word_SMS(ime_konstanta, "abs") && Word_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_SMS(ime_konstanta, "min") || Word_SMS(ime_konstanta, "max")) && Word_SMS(서술상수, "(II)I")) { int bajt_podaci = 빼기(1), 첫값 = 빼기(1); 넣기(Word_SMS(ime_konstanta, "min") ? (첫값 < bajt_podaci ? 첫값 : bajt_podaci) : (첫값 > bajt_podaci ? 첫값 : bajt_podaci), 1); return true; }
        }
        if (Word_SMS(vlasnik, "java/lang/System") && komanda_kôd == 184) {
            if (Word_SMS(ime_konstanta, "gc") && Word_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Word_SMS(ime_konstanta, "arraycopy") && Word_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int stavka_COUNT_8f7753a1 = 빼기(1), odredište_VALUE_INDEX = 빼기(1), bajt_podaci = 빼기(2), START_pozicija = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(bajt_podaci)) {
                    int oblast_kôd = 힙[첫값];
                    if (힙[bajt_podaci] != oblast_kôd || (oblast_kôd != 2 && oblast_kôd != 3 && (oblast_kôd < 20 || oblast_kôd > 23))) otkazivanje_VALUE("arraycopy type mismatch");
                    else if (stavka_COUNT_8f7753a1 < 0 || START_pozicija < 0 || odredište_VALUE_INDEX < 0 || START_pozicija > 힙[첫값 + 1] - stavka_COUNT_8f7753a1 || odredište_VALUE_INDEX > 힙[bajt_podaci + 1] - stavka_COUNT_8f7753a1) otkazivanje_VALUE("ArrayIndexOutOfBoundsException");
                    else if (첫값 == bajt_podaci && odredište_VALUE_INDEX > START_pozicija) { for (int Loop_INDEX = stavka_COUNT_8f7753a1 - 1; Loop_INDEX >= 0; Loop_INDEX--) 힙[bajt_podaci + 2 + odredište_VALUE_INDEX + Loop_INDEX] = 힙[첫값 + 2 + START_pozicija + Loop_INDEX]; }
                    else { for (int Loop_INDEX = 0; Loop_INDEX < stavka_COUNT_8f7753a1 && !greška; Loop_INDEX++) { int podaci_VALUE = 힙[첫값 + 2 + START_pozicija + Loop_INDEX]; if (oblast_kôd != 3 || 배열저장가능(bajt_podaci, podaci_VALUE)) 힙[bajt_podaci + 2 + odredište_VALUE_INDEX + Loop_INDEX] = podaci_VALUE; } }
                }
                return true;
            }
        }
        if (Word_SMS(vlasnik, "java/util/ArrayList") || Word_SMS(vlasnik, "java/util/List") || Word_SMS(vlasnik, "java/util/HashMap") || Word_SMS(vlasnik, "java/util/Map")) {
            모음호출(vlasnik, ime_konstanta, 서술상수, komanda_kôd); return true;
        }
        return false;
    }
    static void 모음늘리기(int objekat_referenca, int 필요수) {
        int 이전값 = 힙[objekat_referenca + 2], kapacitet_podaci = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (kapacitet_podaci >= 필요수) return;
        int Dalje_pozicija = kapacitet_podaci < 8 ? 8 : kapacitet_podaci * 2; if (Dalje_pozicija < 필요수) Dalje_pozicija = 필요수;
        int podaci_niz = dodeliti_Skladište(3, Dalje_pozicija); if (greška) return;
        for (int Loop_INDEX = 0; Loop_INDEX < kapacitet_podaci; Loop_INDEX++) 힙[podaci_niz + 2 + Loop_INDEX] = 힙[이전값 + 2 + Loop_INDEX];
        힙[objekat_referenca + 2] = podaci_niz; 힙참조[objekat_referenca + 2] = 1;
    }
    static void 모음호출(int vlasnik, int ime_konstanta, int 서술상수, int komanda_kôd) {
        boolean 대응참조 = Word_SMS(vlasnik, "java/util/HashMap") || Word_SMS(vlasnik, "java/util/Map"); int oblast_kôd = 대응참조 ? 11 : 10;
        if (Word_SMS(ime_konstanta, "<init>") && komanda_kôd == 183 && Word_SMS(서술상수, "()V")) { int objekat_referenca = 빼기(2); if (objekat_VALUE(objekat_referenca, oblast_kôd)) 모음늘리기(objekat_referenca, 8); return; }
        if (komanda_kôd != 182 && komanda_kôd != 185) { otkazivanje_VALUE("invalid collection invocation"); return; }
        if (Word_SMS(ime_konstanta, "size") && Word_SMS(서술상수, "()I") || Word_SMS(ime_konstanta, "isEmpty") && Word_SMS(서술상수, "()Z")) {
            int objekat_referenca = 빼기(2); if (objekat_VALUE(objekat_referenca, oblast_kôd)) 넣기(Word_SMS(ime_konstanta, "size") ? 힙[objekat_referenca + 3] : 힙[objekat_referenca + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_SMS(ime_konstanta, "clear") && Word_SMS(서술상수, "()V")) { int objekat_referenca = 빼기(2); if (objekat_VALUE(objekat_referenca, oblast_kôd)) { int podaci_niz = 힙[objekat_referenca + 2]; for (int Loop_INDEX = 0; Loop_INDEX < 힙[podaci_niz + 1]; Loop_INDEX++) 힙[podaci_niz + 2 + Loop_INDEX] = 0; 힙[objekat_referenca + 3] = 0; } return; }
        if (!대응참조 && Word_SMS(ime_konstanta, "add") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int podaci_VALUE = 빼기(2), objekat_referenca = 빼기(2); if (!objekat_VALUE(objekat_referenca, 10)) return;
            int stavka_COUNT_8f7753a1 = 힙[objekat_referenca + 3]; 모음늘리기(objekat_referenca, stavka_COUNT_8f7753a1 + 1); if (!greška) { 힙[힙[objekat_referenca + 2] + 2 + stavka_COUNT_8f7753a1] = podaci_VALUE; 힙[objekat_referenca + 3] = stavka_COUNT_8f7753a1 + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_SMS(ime_konstanta, "get") || Word_SMS(ime_konstanta, "remove")) && Word_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Word_SMS(ime_konstanta, "set") && Word_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean informatičko_odeljenje_Dodeljen = Word_SMS(ime_konstanta, "set"); int podaci_VALUE = informatičko_odeljenje_Dodeljen ? 빼기(2) : 0, stavka_pozicija = 빼기(1), objekat_referenca = 빼기(2);
            if (!objekat_VALUE(objekat_referenca, 10)) return;
            int stavka_COUNT_8f7753a1 = 힙[objekat_referenca + 3], podaci_niz = 힙[objekat_referenca + 2];
            if (stavka_pozicija < 0 || stavka_pozicija >= stavka_COUNT_8f7753a1) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[podaci_niz + 2 + stavka_pozicija];
            if (informatičko_odeljenje_Dodeljen) 힙[podaci_niz + 2 + stavka_pozicija] = podaci_VALUE;
            if (Word_SMS(ime_konstanta, "remove")) { for (int Loop_INDEX = stavka_pozicija + 1; Loop_INDEX < stavka_COUNT_8f7753a1; Loop_INDEX++) 힙[podaci_niz + 1 + Loop_INDEX] = 힙[podaci_niz + 2 + Loop_INDEX]; 힙[podaci_niz + 1 + stavka_COUNT_8f7753a1] = 0; 힙[objekat_referenca + 3] = stavka_COUNT_8f7753a1 - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Word_SMS(ime_konstanta, "get") || Word_SMS(ime_konstanta, "remove")) && Word_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(ime_konstanta, "put") && Word_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(ime_konstanta, "containsKey") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_SMS(ime_konstanta, "put"), ukloniti = Word_SMS(ime_konstanta, "remove");
            int podaci_VALUE = 넣기여부 ? 빼기(2) : 0, Ključ_referenca = 빼기(2), objekat_referenca = 빼기(2); if (!objekat_VALUE(objekat_referenca, 11)) return;
            int stavka_COUNT_8f7753a1 = 힙[objekat_referenca + 3], podaci_niz = 힙[objekat_referenca + 2], 찾은여부 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < stavka_COUNT_8f7753a1; Loop_INDEX++) if (값같음(Ključ_referenca, 힙[podaci_niz + 2 + 2 * Loop_INDEX])) { 찾은여부 = Loop_INDEX; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[podaci_niz + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(objekat_referenca, (stavka_COUNT_8f7753a1 + 1) * 2); podaci_niz = 힙[objekat_referenca + 2]; 찾은여부 = stavka_COUNT_8f7753a1; if (!greška) 힙[objekat_referenca + 3] = stavka_COUNT_8f7753a1 + 1; }
                if (!greška) { 힙[podaci_niz + 2 + 2 * 찾은여부] = Ključ_referenca; 힙[podaci_niz + 3 + 2 * 찾은여부] = podaci_VALUE; }
            }
            if (ukloniti && 찾은여부 >= 0) { for (int Loop_INDEX = 찾은여부 + 1; Loop_INDEX < stavka_COUNT_8f7753a1; Loop_INDEX++) { 힙[podaci_niz + 2 * Loop_INDEX] = 힙[podaci_niz + 2 + 2 * Loop_INDEX]; 힙[podaci_niz + 1 + 2 * Loop_INDEX] = 힙[podaci_niz + 3 + 2 * Loop_INDEX]; } 힙[podaci_niz + 2 * stavka_COUNT_8f7753a1] = 0; 힙[podaci_niz + 1 + 2 * stavka_COUNT_8f7753a1] = 0; 힙[objekat_referenca + 3] = stavka_COUNT_8f7753a1 - 1; }
            if (Word_SMS(ime_konstanta, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        otkazivanje_VALUE("unsupported collection method");
    }
    static boolean 잠금얻기(int objekat_referenca) {
        if (!객체유효(objekat_referenca)) return false;
        if (잠금깊이[objekat_referenca] != 0 && zaključati_vlasnik[objekat_referenca] != aktuelno_nit + 1) { promeniti_zahtev = true; return false; }
        zaključati_vlasnik[objekat_referenca] = aktuelno_nit + 1; 잠금깊이[objekat_referenca]++; return true;
    }
    static void izdanje_zaključati(int objekat_referenca) {
        if (!객체유효(objekat_referenca)) return;
        if (잠금깊이[objekat_referenca] == 0 || zaključati_vlasnik[objekat_referenca] != aktuelno_nit + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[objekat_referenca] == 0) zaključati_vlasnik[objekat_referenca] = 0;
    }
    static boolean SWITCH_nit() {
        nit_kadar[aktuelno_nit] = kadar_INDEX;
        if (kadar_INDEX < aktuelno_nit * 32) nit_Status[aktuelno_nit] = 3;
        for (int Loop_INDEX = 0; Loop_INDEX < nit_COUNT; Loop_INDEX++) if (nit_Status[Loop_INDEX] == 2 && nit_Status[가닥대기[Loop_INDEX]] == 3) nit_Status[Loop_INDEX] = 1;
        for (int Loop_INDEX = 1; Loop_INDEX <= nit_COUNT; Loop_INDEX++) {
            int Dalje_pozicija = (aktuelno_nit + Loop_INDEX) % nit_COUNT;
            if (nit_Status[Dalje_pozicija] == 1) { aktuelno_nit = Dalje_pozicija; kadar_INDEX = nit_kadar[Dalje_pozicija]; promeniti_zahtev = false; return true; }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < nit_COUNT; Loop_INDEX++) if (nit_Status[Loop_INDEX] != 3) { otkazivanje_VALUE("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int ime_konstanta, int 서술상수, int komanda_kôd) { Proces_nit(ime_konstanta, 서술상수, komanda_kôd, false); }
    static void Proces_nit(int ime_konstanta, int 서술상수, int komanda_kôd, boolean 한국어) {
        if (komanda_kôd == 184 && Word_SMS(ime_konstanta, 한국어 ? "YIELD_obaveza" : "yield") && Word_SMS(서술상수, "()V")) { promeniti_zahtev = true; return; }
        if (komanda_kôd == 184 && Word_SMS(ime_konstanta, "currentThread") && Word_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(nit_objekat[aktuelno_nit], 2); return; }
        if (komanda_kôd == 183 && Word_SMS(ime_konstanta, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, 한국어 ? "(L한국어/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int cilj_adresa = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), objekat_referenca = 빼기(2);
            if (!객체유효(objekat_referenca)) return;
            if (힙[objekat_referenca] == 13) { 힙[objekat_referenca + 2] = cilj_adresa; 힙참조[objekat_referenca + 2] = 1; }
            else if (cilj_adresa != 0) otkazivanje_VALUE("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (komanda_kôd == 182 && (Word_SMS(ime_konstanta, 한국어 ? "START_obaveza" : "start") || Word_SMS(ime_konstanta, 한국어 ? "기다리기" : "join")) && Word_SMS(서술상수, "()V") || komanda_kôd == 182 && Word_SMS(ime_konstanta, 한국어 ? "살아있는가" : "isAlive") && Word_SMS(서술상수, "()Z")) {
            int objekat_referenca = 빼기(2); if (!객체유효(objekat_referenca)) return;
            int nalog_VALUE = -1; for (int Loop_INDEX = 0; Loop_INDEX < nit_COUNT; Loop_INDEX++) if (nit_objekat[Loop_INDEX] == objekat_referenca) nalog_VALUE = Loop_INDEX;
            if (Word_SMS(ime_konstanta, 한국어 ? "살아있는가" : "isAlive")) { 넣기(nalog_VALUE >= 0 && nit_Status[nalog_VALUE] != 3 ? 1 : 0, 1); return; }
            if (Word_SMS(ime_konstanta, 한국어 ? "기다리기" : "join")) { if (nalog_VALUE >= 0 && nit_Status[nalog_VALUE] != 3) { 가닥대기[aktuelno_nit] = nalog_VALUE; nit_Status[aktuelno_nit] = 2; promeniti_zahtev = true; } return; }
            if (nalog_VALUE >= 0) { 예외던짐(한국어 ? 38 : 16, "thread already started"); return; }
            if (nit_COUNT == 4) { otkazivanje_VALUE("thread limit (4 including main)"); return; }
            int cilj_adresa = 힙[objekat_referenca] == 13 ? 힙[objekat_referenca + 2] : objekat_referenca;
            int Datoteka_INDEX = cilj_adresa > 0 && 힙[cilj_adresa] >= 32 ? ime_metod(힙[cilj_adresa] - 32, 한국어 ? "Izvrši_obaveza" : "run", "()V") : -1;
            if (cilj_adresa != 0 && Datoteka_INDEX < 0) { otkazivanje_VALUE("Runnable.run required"); return; }
            nalog_VALUE = nit_COUNT++; nit_objekat[nalog_VALUE] = objekat_referenca; nit_cilj[nalog_VALUE] = cilj_adresa;
            int kadar = nalog_VALUE * 32; nit_kadar[nalog_VALUE] = Datoteka_INDEX < 0 ? kadar - 1 : kadar; nit_Status[nalog_VALUE] = Datoteka_INDEX < 0 ? 3 : 1;
            if (Datoteka_INDEX >= 0) { kadar_metod[kadar] = Datoteka_INDEX; kadar_pozicija[kadar] = metod_START[Datoteka_INDEX]; lokalni_VALUE[kadar * 128] = cilj_adresa; lokalni_tip[kadar * 128] = 2; }
            return;
        }
        otkazivanje_VALUE("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], adresa_SMS = new int[16];
    static int lokalni_adresa() { return adresa_objekat(0x7f000001); }
    static int adresa_objekat(int VALUE) { int objekat_referenca = dodeliti_Skladište(14, 1); if (!greška) 힙[objekat_referenca + 2] = VALUE; return objekat_referenca; }
    static int 주소해독(int objekat_referenca) {
        if (objekat_referenca == 0 || 글같음(objekat_referenca, host_znak("localhost"), false)) return 0x7f000001;
        if (!objekat_VALUE(objekat_referenca, 1)) return 0;
        int podaci_VALUE = 0, ukupan_COUNT = 0, adresa_bajt = 0, 자릿수 = 0, stavka_COUNT_8f7753a1 = 힙[objekat_referenca + 1];
        for (int Loop_INDEX = 0; Loop_INDEX <= stavka_COUNT_8f7753a1; Loop_INDEX++) {
            int kôd_znaka = Loop_INDEX == stavka_COUNT_8f7753a1 ? '.' : 힙[objekat_referenca + 2 + Loop_INDEX];
            if (kôd_znaka == '.') { if (자릿수 == 0 || ukupan_COUNT == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } podaci_VALUE = podaci_VALUE << 8 | adresa_bajt; ukupan_COUNT++; adresa_bajt = 자릿수 = 0; }
            else { if (kôd_znaka < '0' || kôd_znaka > '9' || ++자릿수 > 3 || (adresa_bajt = adresa_bajt * 10 + kôd_znaka - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (ukupan_COUNT != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return podaci_VALUE;
    }
    static int adresa_znak(int podaci_VALUE) {
        int stavka_COUNT_8f7753a1 = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int adresa_bajt = podaci_VALUE >>> 이동비트 & 255;
            if (adresa_bajt >= 100) adresa_SMS[stavka_COUNT_8f7753a1++] = '0' + adresa_bajt / 100;
            if (adresa_bajt >= 10) adresa_SMS[stavka_COUNT_8f7753a1++] = '0' + adresa_bajt / 10 % 10;
            adresa_SMS[stavka_COUNT_8f7753a1++] = '0' + adresa_bajt % 10; if (이동비트 != 0) adresa_SMS[stavka_COUNT_8f7753a1++] = '.';
        }
        int objekat_referenca = dodeliti_Skladište(1, stavka_COUNT_8f7753a1); if (!greška) for (int Loop_INDEX = 0; Loop_INDEX < stavka_COUNT_8f7753a1; Loop_INDEX++) 힙[objekat_referenca + 2 + Loop_INDEX] = adresa_SMS[Loop_INDEX]; return objekat_referenca;
    }
    static void 통신호출(int vlasnik, int ime_konstanta, int 서술상수, int komanda_kôd) {
        if (Word_SMS(vlasnik, "java/net/InetAddress")) {
            if (komanda_kôd == 184 && Word_SMS(ime_konstanta, "getLoopbackAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(lokalni_adresa(), 2); return; }
            if (komanda_kôd == 184 && Word_SMS(ime_konstanta, "getByName") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int podaci_VALUE = 주소해독(빼기(2)); if (던진객체 == 0 && !greška) 넣기(adresa_objekat(podaci_VALUE), 2); return;
            }
            if (komanda_kôd == 182 && Word_SMS(ime_konstanta, "getHostAddress") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int objekat_referenca = 빼기(2); if (objekat_VALUE(objekat_referenca, 14)) 넣기(adresa_znak(힙[objekat_referenca + 2]), 2); return; }
        }
        if (Word_SMS(vlasnik, "java/net/DatagramPacket")) {
            if (komanda_kôd == 183 && Word_SMS(ime_konstanta, "<init>") && (Word_SMS(서술상수, "([BI)V") || Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean odredište_VALUE_referenca = Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int broj_porta = odredište_VALUE_referenca ? 빼기(1) : 0, adresa_referenca = odredište_VALUE_referenca ? 빼기(2) : 0;
                int stavka_COUNT_8f7753a1 = 빼기(1), podaci_niz = 빼기(2), objekat_referenca = 빼기(2);
                if (!objekat_VALUE(objekat_referenca, 16) || !objekat_VALUE(podaci_niz, 20)) return;
                if (stavka_COUNT_8f7753a1 < 0 || stavka_COUNT_8f7753a1 > 힙[podaci_niz + 1] || broj_porta < 0 || broj_porta > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (adresa_referenca != 0 && !objekat_VALUE(adresa_referenca, 14)) return;
                힙[objekat_referenca + 2] = podaci_niz; 힙참조[objekat_referenca + 2] = 1; 힙[objekat_referenca + 3] = stavka_COUNT_8f7753a1;
                힙[objekat_referenca + 4] = adresa_referenca; 힙참조[objekat_referenca + 4] = 1; 힙[objekat_referenca + 5] = broj_porta; return;
            }
            if (komanda_kôd == 182 && Word_SMS(ime_konstanta, "setLength") && Word_SMS(서술상수, "(I)V")) {
                int stavka_COUNT_8f7753a1 = 빼기(1), objekat_referenca = 빼기(2); if (!objekat_VALUE(objekat_referenca, 16)) return;
                if (stavka_COUNT_8f7753a1 < 0 || stavka_COUNT_8f7753a1 > 힙[힙[objekat_referenca + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[objekat_referenca + 3] = stavka_COUNT_8f7753a1; return;
            }
            if (komanda_kôd == 182 && (Word_SMS(ime_konstanta, "getData") && Word_SMS(서술상수, "()[B") || Word_SMS(ime_konstanta, "getLength") && Word_SMS(서술상수, "()I") || Word_SMS(ime_konstanta, "getAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;") || Word_SMS(ime_konstanta, "getPort") && Word_SMS(서술상수, "()I"))) {
                int objekat_referenca = 빼기(2); if (!objekat_VALUE(objekat_referenca, 16)) return;
                int stavka_pozicija = Word_SMS(ime_konstanta, "getData") ? 2 : Word_SMS(ime_konstanta, "getLength") ? 3 : Word_SMS(ime_konstanta, "getAddress") ? 4 : 5;
                넣기(힙[objekat_referenca + stavka_pozicija], stavka_pozicija == 2 || stavka_pozicija == 4 ? 2 : 1); return;
            }
        }
        if (Word_SMS(vlasnik, "java/net/DatagramSocket")) {
            if (komanda_kôd == 183 && Word_SMS(ime_konstanta, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(I)V"))) {
                int broj_porta = Word_SMS(서술상수, "()V") ? 0 : 빼기(1), objekat_referenca = 빼기(2); if (!objekat_VALUE(objekat_referenca, 15)) return;
                if (broj_porta < 0 || broj_porta > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = korisnik.otvoren_Mreža(broj_porta); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[objekat_referenca + 2] = 열린파일번호; return;
            }
            if (komanda_kôd == 182 && Word_SMS(ime_konstanta, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), objekat_referenca = 빼기(2); if (!objekat_VALUE(objekat_referenca, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[objekat_referenca + 3] = 밀리초값; return;
            }
            if (komanda_kôd == 182 && Word_SMS(ime_konstanta, "getLocalPort") && Word_SMS(서술상수, "()I")) { int objekat_referenca = 빼기(2); if (objekat_VALUE(objekat_referenca, 15)) 넣기(힙[objekat_referenca + 2] < 0 ? -1 : korisnik.Mreža_port(힙[objekat_referenca + 2]), 1); return; }
            if (komanda_kôd == 182 && Word_SMS(ime_konstanta, "isClosed") && Word_SMS(서술상수, "()Z")) { int objekat_referenca = 빼기(2); if (objekat_VALUE(objekat_referenca, 15)) 넣기(힙[objekat_referenca + 2] < 0 ? 1 : 0, 1); return; }
            if (komanda_kôd == 182 && Word_SMS(ime_konstanta, "close") && Word_SMS(서술상수, "()V")) { int objekat_referenca = 빼기(2); if (objekat_VALUE(objekat_referenca, 15) && 힙[objekat_referenca + 2] >= 0) { korisnik.파일서술자닫기(힙[objekat_referenca + 2]); 힙[objekat_referenca + 2] = -1; } return; }
            if (komanda_kôd == 182 && (Word_SMS(ime_konstanta, "send") || Word_SMS(ime_konstanta, "receive")) && Word_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int paket = 빼기(2), objekat_referenca = 빼기(2); if (!objekat_VALUE(paket, 16) || !objekat_VALUE(objekat_referenca, 15)) return;
                int podaci_niz = 힙[paket + 2], 유효길이 = 힙[paket + 3], 열린파일번호 = 힙[objekat_referenca + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_SMS(ime_konstanta, "send")) {
                    if (!objekat_VALUE(힙[paket + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < 유효길이; Loop_INDEX++) 통신임시[Loop_INDEX] = 힙[podaci_niz + 2 + Loop_INDEX];
                    if (korisnik.poslati_Mreža(열린파일번호, 힙[힙[paket + 4] + 2], 힙[paket + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int stavka_COUNT_8f7753a1 = korisnik.primiti_Mreža(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (stavka_COUNT_8f7753a1 == -11) {
                        int aktuelno_TIME = korisnik.밀리초();
                        if (힙[objekat_referenca + 4] == 0) 힙[objekat_referenca + 4] = aktuelno_TIME + 1;
                        if (힙[objekat_referenca + 3] > 0 && aktuelno_TIME - (힙[objekat_referenca + 4] - 1) >= 힙[objekat_referenca + 3]) { 힙[objekat_referenca + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(objekat_referenca, 2); 넣기(paket, 2); kadar_pozicija[kadar_INDEX] = 틀명령[kadar_INDEX]; promeniti_zahtev = true; return;
                    }
                    힙[objekat_referenca + 4] = 0;
                    if (stavka_COUNT_8f7753a1 < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < stavka_COUNT_8f7753a1; Loop_INDEX++) 힙[podaci_niz + 2 + Loop_INDEX] = (byte)통신임시[Loop_INDEX];
                    힙[paket + 3] = stavka_COUNT_8f7753a1; 힙[paket + 4] = adresa_objekat(통신임시[513]); 힙참조[paket + 4] = 1; 힙[paket + 5] = 통신임시[512];
                }
                return;
            }
        }
        otkazivanje_VALUE("unsupported java.net method");
    }
    static boolean 흐름대기(int objekat_referenca) {
        int aktuelno_TIME = korisnik.밀리초();
        if (힙[objekat_referenca + 5] == 0) 힙[objekat_referenca + 5] = aktuelno_TIME + 1;
        if (힙[objekat_referenca + 3] > 0 && aktuelno_TIME - (힙[objekat_referenca + 5] - 1) >= 힙[objekat_referenca + 3]) { 힙[objekat_referenca + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        kadar_pozicija[kadar_INDEX] = 틀명령[kadar_INDEX]; promeniti_zahtev = true; return true;
    }
    static void 흐름호출(int vlasnik, int ime_konstanta, int 서술상수, int komanda_kôd) {
        boolean primiti_stranica = Word_SMS(vlasnik, "java/net/ServerSocket"), tok = Word_SMS(vlasnik, "java/io/InputStream") || Word_SMS(vlasnik, "java/io/OutputStream");
        if (!tok && komanda_kôd == 183 && Word_SMS(ime_konstanta, "<init>")) {
            boolean 빈여부 = Word_SMS(서술상수, "()V"), 이름지정여부 = Word_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || primiti_stranica && Word_SMS(서술상수, "(I)V") || !primiti_stranica && (이름지정여부 || 주소지정여부))) { otkazivanje_VALUE("unsupported socket constructor"); return; }
            int broj_porta = 빈여부 ? 0 : 빼기(1), adresa_referenca = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, objekat_referenca = 빼기(2);
            if (!objekat_VALUE(objekat_referenca, primiti_stranica ? 18 : 17)) return;
            if (broj_porta < 0 || broj_porta > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !objekat_VALUE(adresa_referenca, 14)) return;
            int ID_mreže = 이름지정여부 ? 주소해독(adresa_referenca) : 주소지정여부 ? 힙[adresa_referenca + 2] : 0x7f000001;
            if (greška || 던진객체 != 0) return;
            int 열린파일번호 = korisnik.tok_kontrola(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : primiti_stranica ? korisnik.tok_kontrola(1, 열린파일번호, broj_porta) : korisnik.veze_tok(열린파일번호, ID_mreže, broj_porta);
            if (처리값 < 0) { korisnik.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[objekat_referenca + 2] = 열린파일번호; 힙[objekat_referenca + 4] = broj_porta; 힙[objekat_referenca + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!tok && Word_SMS(ime_konstanta, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), objekat_referenca = 빼기(2); if (!objekat_VALUE(objekat_referenca, primiti_stranica ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[objekat_referenca + 3] = 밀리초값; return; }
        if (!tok && Word_SMS(ime_konstanta, "close") && Word_SMS(서술상수, "()V")) { int objekat_referenca = 빼기(2); if (objekat_VALUE(objekat_referenca, primiti_stranica ? 18 : 17) && 힙[objekat_referenca + 2] >= 0) { korisnik.파일서술자닫기(힙[objekat_referenca + 2]); 힙[objekat_referenca + 2] = -1; } return; }
        if (!tok && (Word_SMS(ime_konstanta, "getLocalPort") || Word_SMS(ime_konstanta, "getPort") || Word_SMS(ime_konstanta, "isClosed") || Word_SMS(ime_konstanta, "isConnected"))) {
            int objekat_referenca = 빼기(2); if (!objekat_VALUE(objekat_referenca, primiti_stranica ? 18 : 17)) return;
            넣기(Word_SMS(ime_konstanta, "isClosed") ? 힙[objekat_referenca + 2] < 0 ? 1 : 0 : Word_SMS(ime_konstanta, "isConnected") ? 힙[objekat_referenca + 6] : Word_SMS(ime_konstanta, "getPort") ? 힙[objekat_referenca + 4] : 힙[objekat_referenca + 2] < 0 ? -1 : korisnik.tok_kontrola(4, 힙[objekat_referenca + 2], 0), 1); return;
        }
        if (primiti_stranica && Word_SMS(ime_konstanta, "accept") && Word_SMS(서술상수, "()Ljava/net/Socket;")) {
            int objekat_referenca = 빼기(2); if (!objekat_VALUE(objekat_referenca, 18)) return; int 열린파일번호 = korisnik.tok_kontrola(3, 힙[objekat_referenca + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(objekat_referenca)) 넣기(objekat_referenca, 2); return; }
            힙[objekat_referenca + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = dodeliti_Skladište(17, 5); if (greška) { korisnik.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = korisnik.tok_kontrola(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!primiti_stranica && !tok && ((Word_SMS(ime_konstanta, "getInputStream") && Word_SMS(서술상수, "()Ljava/io/InputStream;")) || (Word_SMS(ime_konstanta, "getOutputStream") && Word_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int objekat_referenca = 빼기(2); if (!objekat_VALUE(objekat_referenca, 17)) return; if (힙[objekat_referenca + 2] < 0 || 힙[objekat_referenca + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = dodeliti_Skladište(19, 4); if (greška) return; 힙[반환값 + 2] = objekat_referenca; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Word_SMS(ime_konstanta, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (tok) {
            boolean 읽기여부 = Word_SMS(ime_konstanta, "read"), 쓰기여부 = Word_SMS(ime_konstanta, "write"), blok = Word_SMS(서술상수, "([B)I") || Word_SMS(서술상수, "([B)V"), informatičko_odeljenje_SUBARRAY = Word_SMS(서술상수, "([BII)I") || Word_SMS(서술상수, "([BII)V");
            int stavka_COUNT_8f7753a1 = informatičko_odeljenje_SUBARRAY ? 빼기(1) : 0, 시작변위 = informatičko_odeljenje_SUBARRAY ? 빼기(1) : 0, podaci_niz = blok || informatičko_odeljenje_SUBARRAY ? 빼기(2) : 0;
            int podaci_VALUE = 쓰기여부 && Word_SMS(서술상수, "(I)V") ? 빼기(1) : 0, objekat_referenca = 빼기(2);
            if (!objekat_VALUE(objekat_referenca, 19)) return; int nadređen_referenca = 힙[objekat_referenca + 2], 열린파일번호 = 힙[nadređen_referenca + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_SMS(ime_konstanta, "close") && Word_SMS(서술상수, "()V")) { korisnik.파일서술자닫기(열린파일번호); 힙[nadređen_referenca + 2] = -1; return; }
            if (Word_SMS(ime_konstanta, "flush") && Word_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !쓰기여부) || 읽기여부 != (힙[objekat_referenca + 3] == 0)) { otkazivanje_VALUE("unsupported stream operation"); return; }
            if (blok || informatičko_odeljenje_SUBARRAY) { if (!objekat_VALUE(podaci_niz, 20)) return; if (blok) stavka_COUNT_8f7753a1 = 힙[podaci_niz + 1]; if (시작변위 < 0 || stavka_COUNT_8f7753a1 < 0 || 시작변위 > 힙[podaci_niz + 1] - stavka_COUNT_8f7753a1) { 예외던짐(6, "stream array bounds"); return; } }
            else stavka_COUNT_8f7753a1 = 1;
            if (stavka_COUNT_8f7753a1 == 0) { if (읽기여부) 넣기(0, 1); return; }
            int Dovršeno_COUNT = 쓰기여부 ? 힙[objekat_referenca + 4] : 0, 처리값 = 0;
            while (Dovršeno_COUNT < stavka_COUNT_8f7753a1) {
                처리값 = 읽기여부 ? korisnik.파일한바이트읽기(열린파일번호) : korisnik.파일한바이트쓰기(열린파일번호, blok || informatičko_odeljenje_SUBARRAY ? 힙[podaci_niz + 2 + 시작변위 + Dovršeno_COUNT] : podaci_VALUE);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (blok || informatičko_odeljenje_SUBARRAY)) 힙[podaci_niz + 2 + 시작변위 + Dovršeno_COUNT] = (byte)처리값;
                Dovršeno_COUNT++; if (읽기여부 && !(blok || informatičko_odeljenje_SUBARRAY)) break;
            }
            if (처리값 == -11 && (쓰기여부 || Dovršeno_COUNT == 0)) {
                힙[objekat_referenca + 4] = Dovršeno_COUNT;
                if (흐름대기(nadređen_referenca)) { 넣기(objekat_referenca, 2); if (blok || informatičko_odeljenje_SUBARRAY) 넣기(podaci_niz, 2); if (informatičko_odeljenje_SUBARRAY) { 넣기(시작변위, 1); 넣기(stavka_COUNT_8f7753a1, 1); } if (쓰기여부 && !(blok || informatičko_odeljenje_SUBARRAY)) 넣기(podaci_VALUE, 1); } return;
            }
            힙[objekat_referenca + 4] = 0; 힙[nadređen_referenca + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(Dovršeno_COUNT == 0 && 처리값 == 256 ? -1 : blok || informatičko_odeljenje_SUBARRAY ? Dovršeno_COUNT : 처리값, 1); return;
        }
        otkazivanje_VALUE("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int ime_konstanta) {
        if (Word_SMS(ime_konstanta, "한국어/자체/prozor")) return 24;
        if (Word_SMS(ime_konstanta, "한국어/자체/oznaka")) return 26;
        if (Word_SMS(ime_konstanta, "한국어/자체/taster")) return 27;
        if (Word_SMS(ime_konstanta, "한국어/자체/tekstualno_polje")) return 28;
        if (Word_SMS(ime_konstanta, "한국어/자체/radnja_obaveštavanje")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int ime_konstanta) {
        return 한국어화면종(ime_konstanta) != 0 || Word_SMS(ime_konstanta, "한국어/자체/화면구성요소") || Word_SMS(ime_konstanta, "한국어/자체/događaj_red");
    }
    static int 화면종(int ime_konstanta) {
        int 한국어종 = 한국어화면종(ime_konstanta); if (한국어종 != 0) return 한국어종;
        if (Word_SMS(ime_konstanta, "javax/swing/JFrame")) return 24;
        if (Word_SMS(ime_konstanta, "javax/swing/JPanel")) return 25;
        if (Word_SMS(ime_konstanta, "javax/swing/JLabel")) return 26;
        if (Word_SMS(ime_konstanta, "javax/swing/JButton")) return 27;
        if (Word_SMS(ime_konstanta, "javax/swing/JTextField")) return 28;
        if (Word_SMS(ime_konstanta, "java/awt/event/ActionEvent")) return 29;
        if (Word_SMS(ime_konstanta, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int ime_konstanta) {
        return 화면종(ime_konstanta) != 0 || Word_SMS(ime_konstanta, "java/awt/Component") || Word_SMS(ime_konstanta, "java/awt/Container") || Word_SMS(ime_konstanta, "javax/swing/JComponent") || Word_SMS(ime_konstanta, "javax/swing/AbstractButton") || Word_SMS(ime_konstanta, "javax/swing/text/JTextComponent") || Word_SMS(ime_konstanta, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int objekat_referenca) { if (!객체유효(objekat_referenca)) return false; if (힙[objekat_referenca] < 24 || 힙[objekat_referenca] > 28) { otkazivanje_VALUE("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int objekat_referenca, int SMS_referenca) {
        if (SMS_referenca != 0 && !objekat_VALUE(SMS_referenca, 1)) return;
        int stavka_COUNT_8f7753a1 = SMS_referenca == 0 ? 0 : 힙[SMS_referenca + 1]; if (stavka_COUNT_8f7753a1 > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < stavka_COUNT_8f7753a1; Loop_INDEX++) 화면글임시[Loop_INDEX] = 힙[SMS_referenca + 2 + Loop_INDEX];
        if (korisnik.화면글(힙[objekat_referenca + 2], 화면글임시, stavka_COUNT_8f7753a1) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[objekat_referenca + 3] = SMS_referenca; 힙참조[objekat_referenca + 3] = 1;
    }
    static int 화면문자읽기(int objekat_referenca) {
        int nalog_VALUE = 힙[objekat_referenca + 2], stavka_COUNT_8f7753a1 = korisnik.화면연결(8, nalog_VALUE, 0, 0, 0, 0), 사용수 = 0;
        if (stavka_COUNT_8f7753a1 < 0) { otkazivanje_VALUE("GUI text read failed"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < stavka_COUNT_8f7753a1; Loop_INDEX++) { int 부호값 = korisnik.화면연결(9, nalog_VALUE, Loop_INDEX, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = dodeliti_Skladište(1, 사용수); if (!greška) for (int Loop_INDEX = 0; Loop_INDEX < 사용수; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 화면글임시[Loop_INDEX]; return 반환값;
    }
    /* 한국어 객체를 직접 만들고 jezgro_VALUE 화면 기능에 연결한다. Swing objekat_VALUE/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int vlasnik, int ime_konstanta, int 서술상수, int komanda_kôd) {
        if (Word_SMS(vlasnik, "한국어/자체/događaj_red")) {
            if (komanda_kôd == 184 && Word_SMS(ime_konstanta, "나중에실행") && Word_SMS(서술상수, "(L한국어/자체/실행할일;)V")) {
                int obaveza_radnja = 빼기(2); if (!객체유효(obaveza_radnja)) return;
                if (나중수 == 8) { otkazivanje_VALUE("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = obaveza_radnja; return;
            }
            if (komanda_kôd == 184 && Word_SMS(ime_konstanta, "사건처리중인가") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            otkazivanje_VALUE("지원하지 않는 한국어 화면 일정 호출"); return;
        }
        if (Word_SMS(vlasnik, "한국어/자체/radnja_obaveštavanje")) {
            int obaveštavanje = 빼기(2); if (!objekat_VALUE(obaveštavanje, 29) || 힙[obaveštavanje + 3] == 0) return;
            if (Word_SMS(ime_konstanta, "izvor_događaja") && Word_SMS(서술상수, "()L한국어/자체/화면구성요소;")) 넣기(힙[obaveštavanje + 2], 2);
            else if (Word_SMS(ime_konstanta, "komanda_SMS") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[obaveštavanje + 2]), 2);
            else if (Word_SMS(ime_konstanta, "INDEX") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else otkazivanje_VALUE("지원하지 않는 한국어 radnja obaveštavanje 호출"); return;
        }
        if (komanda_kôd == 183 && Word_SMS(ime_konstanta, "<init>")) {
            int 종류 = 한국어화면종(vlasnik), 받이 = 0, 가로 = 0, vertikala_pozicija = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Word_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (korisnik.화면너비() - 폭) / 2; vertikala_pozicija = (korisnik.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Word_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Word_SMS(서술상수, "(Ljava/lang/String;IIIIL한국어/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); vertikala_pozicija = 빼기(1); 가로 = 빼기(1);
            } else { otkazivanje_VALUE("지원하지 않는 한국어 화면 생성자"); return; }
            int SMS = 빼기(2), element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || vertikala_pozicija < 0 || 폭 > korisnik.화면너비() - 가로 || 높이 > korisnik.화면높이() - vertikala_pozicija) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDEX = korisnik.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (INDEX < 1 || INDEX > 32) { otkazivanje_VALUE("화면 element_VALUE 자리가 가득 찼습니다"); return; }
            힙[element_VALUE + 2] = INDEX; 화면참조[INDEX - 1] = element_VALUE;
            힙[element_VALUE + 5] = 가로; 힙[element_VALUE + 6] = vertikala_pozicija; 힙[element_VALUE + 7] = 폭; 힙[element_VALUE + 8] = 높이; 힙[element_VALUE + 10] = 2;
            힙[element_VALUE + 4] = 받이; 힙참조[element_VALUE + 4] = 1; 힙[element_VALUE + 12] = 1;
            korisnik.화면연결(1, INDEX, 가로, vertikala_pozicija, 폭, 높이);
            if (종류 == 24) korisnik.화면연결(7, INDEX, 2, 0, 0, 0);
            화면문자설정(element_VALUE, SMS); return;
        }
        if (komanda_kôd != 182) { otkazivanje_VALUE("잘못된 한국어 화면 호출 komanda"); return; }
        if (Word_SMS(ime_konstanta, "글쓰기") && Word_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int SMS = 빼기(2), element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 화면문자설정(element_VALUE, SMS); return;
        }
        if (Word_SMS(ime_konstanta, "글읽기") && Word_SMS(서술상수, "()Ljava/lang/String;")) {
            int element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 넣기(화면문자읽기(element_VALUE), 2); return;
        }
        if (Word_SMS(ime_konstanta, "동작맡기기") && Word_SMS(서술상수, "(L한국어/자체/동작받이;)V")) {
            int 받이 = 빼기(2), element_VALUE = 빼기(2);
            if (화면객체(element_VALUE)) { 힙[element_VALUE + 4] = 받이; 힙참조[element_VALUE + 4] = 1; 힙[element_VALUE + 12] = 1; } return;
        }
        if (Word_SMS(ime_konstanta, "Dodaj_element") && Word_SMS(서술상수, "(L한국어/자체/화면구성요소;)V")) {
            int dete_VALUE = 빼기(2), nadređen_VALUE = 빼기(2); if (!화면객체(dete_VALUE) || !화면객체(nadređen_VALUE)) return;
            if (korisnik.화면연결(2, 힙[nadređen_VALUE + 2], 힙[dete_VALUE + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[dete_VALUE + 11] = nadređen_VALUE; 힙참조[dete_VALUE + 11] = 1; return;
        }
        if (Word_SMS(ime_konstanta, "자리정하기") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), vertikala_pozicija = 빼기(1), 가로 = 빼기(1), element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (korisnik.화면연결(1, 힙[element_VALUE + 2], 가로, vertikala_pozicija, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[element_VALUE + 5] = 가로; 힙[element_VALUE + 6] = vertikala_pozicija; 힙[element_VALUE + 7] = 폭; 힙[element_VALUE + 8] = 높이; return;
        }
        if ((Word_SMS(ime_konstanta, "emisija_prozor") || Word_SMS(ime_konstanta, "Zatvori")) && Word_SMS(서술상수, "()V")) {
            boolean vidljivost_VALUE = Word_SMS(ime_konstanta, "emisija_prozor"); int element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (korisnik.화면연결(vidljivost_VALUE ? 3 : 4, 힙[element_VALUE + 2], vidljivost_VALUE ? 1 : 0, 0, 0, 0) < 0) { otkazivanje_VALUE("화면은 대화형 명령에서 실행해야 합니다"); return; }
            힙[element_VALUE + 9] = vidljivost_VALUE ? 1 : 0; return;
        }
        if (Word_SMS(ime_konstanta, "보이는가") && Word_SMS(서술상수, "()Z")) { int element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 넣기(힙[element_VALUE + 9], 1); return; }
        otkazivanje_VALUE("지원하지 않는 한국어 화면 metod_VALUE");
    }
    static void 화면호출(int vlasnik, int ime_konstanta, int 서술상수, int komanda_kôd) {
        if (Word_SMS(vlasnik, "javax/swing/SwingUtilities")) {
            if (komanda_kôd == 184 && Word_SMS(ime_konstanta, "invokeLater") && Word_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int objekat_referenca = 빼기(2); if (!객체유효(objekat_referenca)) return; if (나중수 == 8) { otkazivanje_VALUE("invokeLater queue full"); return; } 나중실행[나중수++] = objekat_referenca; return; }
            if (komanda_kôd == 184 && Word_SMS(ime_konstanta, "isEventDispatchThread") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            otkazivanje_VALUE("unsupported SwingUtilities method"); return;
        }
        if (Word_SMS(vlasnik, "java/awt/event/ActionEvent")) {
            int objekat_referenca = 빼기(2); if (!objekat_VALUE(objekat_referenca, 29)) return;
            if (Word_SMS(ime_konstanta, "getSource") && Word_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[objekat_referenca + 2], 2);
            else if (Word_SMS(ime_konstanta, "getActionCommand") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[objekat_referenca + 2]), 2);
            else if (Word_SMS(ime_konstanta, "getID") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else otkazivanje_VALUE("unsupported ActionEvent method"); return;
        }
        if (komanda_kôd == 183 && Word_SMS(ime_konstanta, "<init>")) {
            int COLUMNS = 0, SMS_referenca = 0;
            if (Word_SMS(서술상수, "(I)V")) COLUMNS = 빼기(1);
            else if (Word_SMS(서술상수, "(Ljava/lang/String;I)V")) { COLUMNS = 빼기(1); SMS_referenca = 빼기(2); }
            else if (Word_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_referenca = 빼기(2);
            else if (Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_SMS(서술상수, "()V")) { otkazivanje_VALUE("unsupported Swing constructor"); return; }
            int objekat_referenca = 빼기(2); if (!객체유효(objekat_referenca)) return;
            if (힙[objekat_referenca] == 30) { otkazivanje_VALUE("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(objekat_referenca) || COLUMNS < 0) return;
            int nalog_VALUE = korisnik.화면연결(0, 힙[objekat_referenca] - 23, 0, 0, 0, 0);
            if (nalog_VALUE < 1 || nalog_VALUE > 32) { otkazivanje_VALUE("GUI widget slots exhausted"); return; }
            힙[objekat_referenca + 2] = nalog_VALUE; 화면참조[nalog_VALUE - 1] = objekat_referenca; 힙[objekat_referenca + 5] = 힙[objekat_referenca] == 24 ? 130 : 16; 힙[objekat_referenca + 6] = 힙[objekat_referenca] == 24 ? 110 : 16;
            힙[objekat_referenca + 7] = 힙[objekat_referenca] == 24 ? 380 : 220; 힙[objekat_referenca + 8] = 힙[objekat_referenca] == 24 ? 240 : 28; 힙[objekat_referenca + 10] = 1;
            화면문자설정(objekat_referenca, SMS_referenca); return;
        }
        if (Word_SMS(ime_konstanta, "setText") || Word_SMS(ime_konstanta, "setTitle")) { int SMS_referenca = 빼기(2), objekat_referenca = 빼기(2); if (화면객체(objekat_referenca) && Word_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(objekat_referenca, SMS_referenca); return; }
        if (Word_SMS(ime_konstanta, "getText") || Word_SMS(ime_konstanta, "getTitle")) { int objekat_referenca = 빼기(2); if (화면객체(objekat_referenca) && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(objekat_referenca), 2); return; }
        if (Word_SMS(ime_konstanta, "addActionListener") && Word_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int primiti_referenca = 빼기(2), objekat_referenca = 빼기(2); if (화면객체(objekat_referenca)) { 힙[objekat_referenca + 4] = primiti_referenca; 힙참조[objekat_referenca + 4] = 1; } return; }
        if (Word_SMS(ime_konstanta, "getContentPane") && Word_SMS(서술상수, "()Ljava/awt/Container;")) { int objekat_referenca = 빼기(2); if (화면객체(objekat_referenca)) 넣기(objekat_referenca, 2); return; }
        if (Word_SMS(ime_konstanta, "setLayout") && Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Raspored_referenca = 빼기(2), objekat_referenca = 빼기(2); if (화면객체(objekat_referenca) && Raspored_referenca != 0) otkazivanje_VALUE("only absolute layout (null) is supported"); return; }
        if (Word_SMS(ime_konstanta, "add") && (Word_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Raspored_stanje = Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Raspored_stanje) 빼기(2);
            int dete_referenca = 빼기(2), objekat_referenca = 빼기(2); if (!화면객체(dete_referenca) || !화면객체(objekat_referenca)) return;
            if (korisnik.화면연결(2, 힙[objekat_referenca + 2], 힙[dete_referenca + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[dete_referenca + 11] = objekat_referenca; 힙참조[dete_referenca + 11] = 1; if (!Raspored_stanje) 넣기(dete_referenca, 2); return;
        }
        if (Word_SMS(ime_konstanta, "setBounds") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), x_koordinata = 빼기(1), objekat_referenca = 빼기(2); if (!화면객체(objekat_referenca)) return;
            if (korisnik.화면연결(1, 힙[objekat_referenca + 2], x_koordinata, 세로좌표, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[objekat_referenca + 5] = x_koordinata; 힙[objekat_referenca + 6] = 세로좌표; 힙[objekat_referenca + 7] = 너비; 힙[objekat_referenca + 8] = 높이; return;
        }
        if (Word_SMS(ime_konstanta, "setSize") && Word_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), objekat_referenca = 빼기(2); if (!화면객체(objekat_referenca)) return;
            if (korisnik.화면연결(1, 힙[objekat_referenca + 2], 힙[objekat_referenca + 5], 힙[objekat_referenca + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[objekat_referenca + 7] = 너비; 힙[objekat_referenca + 8] = 높이; } return;
        }
        if (Word_SMS(ime_konstanta, "setLocationRelativeTo") && Word_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), objekat_referenca = 빼기(2); if (!화면객체(objekat_referenca)) return; if (상대배치 != 0) { otkazivanje_VALUE("only screen centering supported"); return; } 힙[objekat_referenca + 5] = (korisnik.화면너비() - 힙[objekat_referenca + 7]) / 2; 힙[objekat_referenca + 6] = (korisnik.화면높이() - 힙[objekat_referenca + 8]) / 2; korisnik.화면연결(1, 힙[objekat_referenca + 2], 힙[objekat_referenca + 5], 힙[objekat_referenca + 6], 힙[objekat_referenca + 7], 힙[objekat_referenca + 8]); return; }
        if (Word_SMS(ime_konstanta, "setDefaultCloseOperation") && Word_SMS(서술상수, "(I)V")) { int propis = 빼기(1), objekat_referenca = 빼기(2); if (화면객체(objekat_referenca)) { if (propis < 0 || propis > 3) 예외던짐(9, "close policy"); else { 힙[objekat_referenca + 10] = propis; korisnik.화면연결(7, 힙[objekat_referenca + 2], propis, 0, 0, 0); } } return; }
        if (Word_SMS(ime_konstanta, "setVisible") && Word_SMS(서술상수, "(Z)V")) { int podaci_VALUE = 빼기(1), objekat_referenca = 빼기(2); if (화면객체(objekat_referenca)) { int 처리값 = korisnik.화면연결(3, 힙[objekat_referenca + 2], podaci_VALUE, 0, 0, 0); if (처리값 < 0) otkazivanje_VALUE("Swing requires a standalone interactive command"); else 힙[objekat_referenca + 9] = podaci_VALUE; } return; }
        if (Word_SMS(ime_konstanta, "dispose") && Word_SMS(서술상수, "()V")) { int objekat_referenca = 빼기(2); if (화면객체(objekat_referenca)) { korisnik.화면연결(4, 힙[objekat_referenca + 2], 0, 0, 0, 0); 힙[objekat_referenca + 9] = 0; } return; }
        if (Word_SMS(ime_konstanta, "repaint") || Word_SMS(ime_konstanta, "validate")) { int objekat_referenca = 빼기(2); if (!화면객체(objekat_referenca) || !Word_SMS(서술상수, "()V")) return; korisnik.화면연결(1, 힙[objekat_referenca + 2], 힙[objekat_referenca + 5], 힙[objekat_referenca + 6], 힙[objekat_referenca + 7], 힙[objekat_referenca + 8]); return; }
        if (Word_SMS(ime_konstanta, "isVisible") && Word_SMS(서술상수, "()Z")) { int objekat_referenca = 빼기(2); if (화면객체(objekat_referenca)) 넣기(힙[objekat_referenca + 9], 1); return; }
        otkazivanje_VALUE("unsupported Swing method (native subset)");
    }
    static void 사건실행(int cilj_adresa, int 사건번호, boolean 한국어) {
        if (cilj_adresa < 1 || 힙[cilj_adresa] < 32) { otkazivanje_VALUE("Java event listener required"); return; }
        int Datoteka_INDEX = ime_metod(힙[cilj_adresa] - 32, 사건번호 == 0 ? (한국어 ? "Izvrši_obaveza" : "run") : (한국어 ? "primiti_radnja" : "actionPerformed"), 사건번호 == 0 ? "()V" : (한국어 ? "(L한국어/자체/radnja_obaveštavanje;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (Datoteka_INDEX < 0) { otkazivanje_VALUE("event callback missing"); return; }
        aktuelno_nit = 0; nit_COUNT = 1; kadar_INDEX = 0; nit_Status[0] = 1; kadar_stek[0] = 0; kadar_zaključati[0] = 틀초기화[0] = 0; promeniti_zahtev = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 128; Loop_INDEX++) { lokalni_VALUE[Loop_INDEX] = lokalni_tip[Loop_INDEX] = 0; }
        kadar_metod[0] = Datoteka_INDEX; kadar_pozicija[0] = metod_START[Datoteka_INDEX]; lokalni_VALUE[0] = cilj_adresa; lokalni_tip[0] = 2;
        if (사건번호 != 0) { lokalni_VALUE[1] = 사건번호; lokalni_tip[1] = 2; }
        사건중 = true; Izvrši_komanda(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!greška) {
            if (나중수 > 0) { int cilj_adresa = 나중실행[0], 한국어 = 나중한국어[0]; for (int Loop_INDEX = 1; Loop_INDEX < 나중수; Loop_INDEX++) { 나중실행[Loop_INDEX - 1] = 나중실행[Loop_INDEX]; 나중한국어[Loop_INDEX - 1] = 나중한국어[Loop_INDEX]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(cilj_adresa, 0, 한국어 != 0); continue; }
            if (korisnik.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = korisnik.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { otkazivanje_VALUE("GUI event I/O failed"); return; }
            int nalog_VALUE = 사건번호 & 65535; if (nalog_VALUE < 1 || nalog_VALUE > 32) continue; int objekat_referenca = 화면참조[nalog_VALUE - 1]; if (objekat_referenca == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[objekat_referenca + 10] != 0) 힙[objekat_referenca + 9] = 0;
                if (힙[objekat_referenca + 10] == 3) for (int Loop_INDEX = 0; Loop_INDEX < 32; Loop_INDEX++) if (화면참조[Loop_INDEX] != 0 && 힙[화면참조[Loop_INDEX]] == 24) korisnik.화면연결(4, Loop_INDEX + 1, 0, 0, 0, 0);
            } else if (힙[objekat_referenca + 4] != 0) {
                int 안내참조 = dodeliti_Skladište(29, 2); if (greška) return; 힙[안내참조 + 2] = objekat_referenca; 힙[안내참조 + 3] = 힙[objekat_referenca + 12]; 힙참조[안내참조 + 2] = 1; 사건실행(힙[objekat_referenca + 4], 안내참조, 힙[objekat_referenca + 12] != 0);
            }
        }
    }
    public static int koristiti() {
        if (korisnik.인수개수() == 1 && 자바도구.같음(korisnik.인수(0), "-version")) {
            korisnik.쓰기("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (korisnik.인수개수() < 1) { korisnik.쓰기("Usage: java CLASS [ARGS]\n"); return 2; }
        stavka_Razred_Definicija = zbirka_Razred_Definicija(host_znak(korisnik.인수(0))); if (greška || stavka_Razred_Definicija < 0) return 1;
        int stavka_p_VALUE = ime_metod(stavka_Razred_Definicija, "koristiti", "()V");
        boolean 한국어진입 = stavka_p_VALUE >= 0 && (metod_pristup[stavka_p_VALUE] & 9) == 9;
        if (!한국어진입) stavka_p_VALUE = ime_metod(stavka_Razred_Definicija, "main", "([Ljava/lang/String;)V");
        if (stavka_p_VALUE < 0 || (metod_pristup[stavka_p_VALUE] & 9) != 9) otkazivanje_VALUE("public static void koristiti() or main(String[] args) required");
        if (greška) return 1;
        int 인수 = dodeliti_Skladište(3, korisnik.인수개수() - 1); element_niza[인수] = -1;
        for (int 수 = 1; 수 < korisnik.인수개수() && !greška; 수++) 힙[인수 + 1 + 수] = host_znak(korisnik.인수(수));
        kadar_INDEX = 0; kadar_metod[0] = stavka_p_VALUE; kadar_pozicija[0] = metod_START[stavka_p_VALUE]; lokalni_VALUE[0] = 한국어진입 ? 0 : 인수; lokalni_tip[0] = 한국어진입 ? 0 : 2;
        nit_Status[0] = 1; nit_objekat[0] = dodeliti_Skladište(13, 2);
        Izvrši_komanda(); if (!greška) 화면사건들(); return greška ? 1 : 0;
    }
}
