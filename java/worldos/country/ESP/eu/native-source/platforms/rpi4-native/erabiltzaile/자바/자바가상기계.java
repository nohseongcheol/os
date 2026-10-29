// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Fitxategia/스택/Erreferentzia_materiala/adar 경계를 exekutatu_komando 중 검사한다. */
public final class 자바가상기계 {
    static int[] Fitxategia = new int[16 * 16384], 임시파일 = new int[16384], fitxategi_izen_SMS = new int[512];
    static int[] konstante_etiketa = new int[8192], 상가 = new int[8192], konstante_SEGUNDOA_balio = new int[8192], kate_Erreferentzia_materiala = new int[8192];
    static int[] 함수명 = new int[512], 함수형 = new int[512], 함수권한 = new int[512], 함수주인 = new int[512];
    static int[] 함수시작 = new int[512], 함수끝 = new int[512], 함수스택 = new int[512], 함수지역 = new int[512];
    static int[] 함수인수수 = new int[512], 함수인수형 = new int[8192], 함수반환 = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] lokal_balio = new int[16384], lokal_MOTA = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] 틀함수 = new int[128], marko_kargu = new int[128], marko_pila = new int[128], marko_instrukzio = new int[128], hasieratu_marko = new int[128];
    static int[] Gela_Definizioa_izen = new int[16], 종크기 = new int[16], 종부모 = new int[16], Gela_Definizioa_Egoera = new int[16], 종칸수 = new int[16], hasieratu_Gela_Definizioa = new int[16];
    static int[] Gela_interfaze = new int[16 * 16], Gela_interfaze_ZENBATU = new int[16];
    static int[] 칸이름 = new int[512], 칸형 = new int[512], 칸주인 = new int[512], 칸권한 = new int[512], 칸위치 = new int[512], 칸값 = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], matrize_elementu = new int[32768], Store_osoko_zenbaki = new int[256];
    static int Tamaina, 읽기위치, 함수수, klasearen_izen, marko_INDIZE = -1, 힙끝 = 1, itzuli_MOTA;
    static int Gela_Definizioa_ZENBATU, 칸수, 잡기수, 현재읽는종, 던진객체, 잠시수, pantaila_ZENBATU, Bilduma_ZENBATU;
    static int 현재가닥, hari_ZENBATU = 1, sarrera_Gela_Definizioa;
    static int[] hari_marko = new int[4], hari_Egoera = new int[4], hari_objektu = new int[4], hari_helburu = new int[4], 가닥대기 = new int[4];
    static boolean errorea, aldatu_eskaera;
    static int[] 잠금주인 = new int[32768], 잠금깊이 = new int[32768], 틀잠금 = new int[128], 종잠금 = new int[16], Gela_hari = new int[16];

    static void hutsegite_balio(String Word_SMS) {
        if (errorea) return;
        int Kategoria_KODE = 0;
        if (자바도구.같음(Word_SMS, "ArithmeticException: / by zero")) Kategoria_KODE = 4;
        if (자바도구.같음(Word_SMS, "NullPointerException") || 자바도구.같음(Word_SMS, "null or invalid array")) Kategoria_KODE = 5;
        if (자바도구.같음(Word_SMS, "ArrayIndexOutOfBoundsException")) Kategoria_KODE = 7;
        if (자바도구.같음(Word_SMS, "StringIndexOutOfBoundsException")) Kategoria_KODE = 8;
        if (자바도구.같음(Word_SMS, "NumberFormatException")) Kategoria_KODE = 10;
        if (자바도구.같음(Word_SMS, "FileNotFoundException: file open failed")) Kategoria_KODE = 12;
        if (자바도구.같음(Word_SMS, "IOException: stream closed") || 자바도구.같음(Word_SMS, "IOException: read failed") || 자바도구.같음(Word_SMS, "IOException: write failed")) Kategoria_KODE = 11;
        if (자바도구.같음(Word_SMS, "ClassCastException")) Kategoria_KODE = 14;
        if (자바도구.같음(Word_SMS, "NegativeArraySizeException")) Kategoria_KODE = 15;
        if (Kategoria_KODE != 0 && marko_INDIZE >= 0) { 예외던짐(Kategoria_KODE, Word_SMS); return; }
        erabiltzaile.Idatzi("JVM error: "); erabiltzaile.Idatzi(Word_SMS); erabiltzaile.idatzi_karaktere_balio(10); errorea = true;
    }
    static boolean klip(int Exekutatu_2, int luzera_balio) {
        if (Exekutatu_2 < 0 || Exekutatu_2 >= Fitxategia.length || luzera_balio < 0) return false;
        int Gela_Definizioa = Exekutatu_2 / 16384;
        return Exekutatu_2 % 16384 <= 종크기[Gela_Definizioa] && luzera_balio <= 종크기[Gela_Definizioa] - Exekutatu_2 % 16384;
    }
    static int byte_balio() {
        if (!klip(읽기위치, 1)) { hutsegite_balio("truncated class file"); return 0; }
        return Fitxategia[읽기위치++];
    }
    static int 짧은수() { return byte_balio() << 8 | byte_balio(); }
    static int osoko_zenbaki() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int luzera_balio) { if (!klip(읽기위치, luzera_balio)) hutsegite_balio("invalid attribute size"); else 읽기위치 += luzera_balio; }
    static boolean txeke_konstante(int 수, int 종류) {
        if (수 <= 0 || 수 >= konstante_etiketa.length || konstante_etiketa[수] != 종류) { hutsegite_balio("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_barruti(int Exekutatu_2, int luzera_balio, String Word_SMS) {
        if (!klip(Exekutatu_2, luzera_balio)) return false;
        int 읽는자리 = Exekutatu_2, 끝 = Exekutatu_2 + luzera_balio;
        for (int Loop_INDIZE = 0; Loop_INDIZE < Word_SMS.length(); Loop_INDIZE++) {
            int karaktere_kode = Word_SMS.charAt(Loop_INDIZE);
            if (karaktere_kode > 0 && karaktere_kode < 128) { if (읽는자리 >= 끝 || Fitxategia[읽는자리++] != karaktere_kode) return false; }
            else if (karaktere_kode < 2048) {
                if (읽는자리 + 2 > 끝 || Fitxategia[읽는자리++] != (192 | (karaktere_kode >> 6)) || Fitxategia[읽는자리++] != (128 | (karaktere_kode & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Fitxategia[읽는자리++] != (224 | (karaktere_kode >> 12)) || Fitxategia[읽는자리++] != (128 | ((karaktere_kode >> 6) & 63)) || Fitxategia[읽는자리++] != (128 | (karaktere_kode & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean Word_SMS(int konstante_balio, String Word_SMS) { return txeke_konstante(konstante_balio, 1) && SMS_barruti(상가[konstante_balio], konstante_SEGUNDOA_balio[konstante_balio], Word_SMS); }
    static boolean 같은말(int 가, int 나) {
        if (!txeke_konstante(가, 1) || !txeke_konstante(나, 1) || konstante_SEGUNDOA_balio[가] != konstante_SEGUNDOA_balio[나]) return false;
        for (int 수 = 0; 수 < konstante_SEGUNDOA_balio[가]; 수++) if (Fitxategia[상가[가] + 수] != Fitxategia[상가[나] + 수]) return false;
        return true;
    }
    static int klasearen_izen_SMS(int 수) { return txeke_konstante(수, 7) && txeke_konstante(상가[수], 1) ? 상가[수] : 0; }
    static int Erreferentzia_materiala_izen(int 수) { return txeke_konstante(수, 12) && txeke_konstante(상가[수], 1) ? 상가[수] : 0; }
    static int Erreferentzia_materiala_MOTA(int 수) { return txeke_konstante(수, 12) && txeke_konstante(konstante_SEGUNDOA_balio[수], 1) ? konstante_SEGUNDOA_balio[수] : 0; }
    static int 서술형(int 끝, boolean 빈형) {
        if (읽기위치 >= 끝) { hutsegite_balio("invalid descriptor"); return 0; }
        int balio = byte_balio();
        if (balio == 'V' && 빈형) return 0;
        if (balio == 'I' || balio == 'B' || balio == 'C' || balio == 'S' || balio == 'Z') return 1;
        if (balio == '[') { 서술형(끝, false); return 2; }
        if (balio == 'L') {
            int Exekutatu_2 = 읽기위치;
            while (읽기위치 < 끝 && Fitxategia[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Exekutatu_2) hutsegite_balio("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        hutsegite_balio("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int FUNTZIOA_balio) {
        int 이전 = 읽기위치, 수 = 함수형[FUNTZIOA_balio];
        if (!txeke_konstante(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + konstante_SEGUNDOA_balio[수];
        if (byte_balio() != '(') hutsegite_balio("invalid method descriptor");
        int elementu_ZENBATU = 0;
        while (!errorea && 읽기위치 < 끝 && Fitxategia[읽기위치] != ')') {
            if (elementu_ZENBATU == 16) { hutsegite_balio("too many method arguments"); break; }
            함수인수형[FUNTZIOA_balio * 16 + elementu_ZENBATU++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || byte_balio() != ')') hutsegite_balio("invalid method descriptor");
        함수반환[FUNTZIOA_balio] = 서술형(끝, true); 함수인수수[FUNTZIOA_balio] = elementu_ZENBATU;
        if (읽기위치 != 끝) hutsegite_balio("invalid method descriptor");
        읽기위치 = 이전;
    }
    static int 상번호() { int balio = 짧은수(); return balio == 0 ? 0 : 현재읽는종 * 512 + balio; }
    static int 명상수() { return 함수주인[틀함수[marko_INDIZE]] * 512 + 명짧(); }
    static void 속성건너() {
        int elementu_ZENBATU = 짧은수();
        for (int 수 = 0; 수 < elementu_ZENBATU && !errorea; 수++) { txeke_konstante(상번호(), 1); 건너(osoko_zenbaki()); }
    }
    static int komando_luzera(int balio) {
        if (balio == 16 || balio == 18 || balio == 21 || balio == 25 || balio == 54 || balio == 58 || balio == 188) return 2;
        if (balio == 17 || balio == 19 || balio == 132 || balio >= 153 && balio <= 167
            || balio >= 178 && balio <= 184 || balio == 187 || balio == 189 || balio == 192 || balio == 193 || balio == 198 || balio == 199) return 3;
        if (balio == 185 || balio == 200) return 5;
        if (balio >= 0 && balio <= 8 || balio >= 26 && balio <= 29 || balio >= 42 && balio <= 46 || balio >= 50 && balio <= 53
            || balio >= 59 && balio <= 62 || balio >= 75 && balio <= 79 || balio >= 83 && balio <= 95
            || balio == 96 || balio == 100 || balio == 104 || balio == 108 || balio == 112 || balio == 116
            || balio == 120 || balio == 122 || balio == 124 || balio == 126 || balio == 128 || balio == 130
            || balio >= 145 && balio <= 147 || balio == 172 || balio == 176 || balio == 177 || balio == 190 || balio == 191
            || balio == 194 || balio == 195) return 1;
        return 0;
    }
    static int kargu_osoko_zenbaki(int 읽는자리) {
        if (!klip(읽는자리, 4)) { hutsegite_balio("truncated bytecode operand"); return 0; }
        return Fitxategia[읽는자리] << 24 | Fitxategia[읽는자리 + 1] << 16 | Fitxategia[읽는자리 + 2] << 8 | Fitxategia[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Exekutatu_2, int 끝) {
        int balio = Fitxategia[읽는자리], luzera_balio = komando_luzera(balio);
        if (balio == 170 || balio == 171) {
            int BASE_kargu = 읽는자리 + 1;
            while ((BASE_kargu - Exekutatu_2) % 4 != 0) BASE_kargu++;
            if (끝 - BASE_kargu < (balio == 170 ? 12 : 8)) return 0;
            int sarrera_ZENBATU = balio == 170 ? kargu_osoko_zenbaki(BASE_kargu + 8) - kargu_osoko_zenbaki(BASE_kargu + 4) + 1 : kargu_osoko_zenbaki(BASE_kargu + 4);
            if (sarrera_ZENBATU < 0 || sarrera_ZENBATU > 2048) return 0;
            luzera_balio = BASE_kargu - 읽는자리 + (balio == 170 ? 12 + 4 * sarrera_ZENBATU : 8 + 8 * sarrera_ZENBATU);
        }
        if (balio == 196 && 읽는자리 + 1 < 끝) {
            int Word_datuak = Fitxategia[읽는자리 + 1]; luzera_balio = Word_datuak == 132 ? 6 : (Word_datuak == 21 || Word_datuak == 25 || Word_datuak == 54 || Word_datuak == 58) ? 4 : 0;
        }
        return luzera_balio > 0 && luzera_balio <= 끝 - 읽는자리 ? luzera_balio : 0;
    }
    static void txeke_helburu_balio(int helburu_balio_a0fbc067, int FUNTZIOA_balio) {
        if (helburu_balio_a0fbc067 < 함수시작[FUNTZIOA_balio] || helburu_balio_a0fbc067 >= 함수끝[FUNTZIOA_balio] || 경계[helburu_balio_a0fbc067] != FUNTZIOA_balio + 1) hutsegite_balio("invalid branch target");
    }
    static void 클래스읽기(int Gela_Definizioa) {
        현재읽는종 = Gela_Definizioa; 읽기위치 = Gela_Definizioa * 16384; Tamaina = 읽기위치 + 종크기[Gela_Definizioa];
        if (osoko_zenbaki() != 0xcafebabe) { hutsegite_balio("not a class file"); return; }
        int 부판 = 짧은수(), bertsio_balio = 짧은수();
        if (bertsio_balio < 45 || bertsio_balio > 52 || 부판 != 0) { hutsegite_balio("supported class versions: 45..52, minor 0"); return; }
        int konstante_ZENBATU = 짧은수(), BASE_kargu = Gela_Definizioa * 512;
        if (konstante_ZENBATU < 1 || konstante_ZENBATU > 512) { hutsegite_balio("constant pool limit (511)"); return; }
        for (int sarrera_ZENBATU = 1; sarrera_ZENBATU < konstante_ZENBATU && !errorea; sarrera_ZENBATU++) {
            int 수 = BASE_kargu + sarrera_ZENBATU, 종류 = byte_balio(); konstante_etiketa[수] = 종류;
            if (종류 == 1) { konstante_SEGUNDOA_balio[수] = 짧은수(); 상가[수] = 읽기위치; 건너(konstante_SEGUNDOA_balio[수]); }
            else if (종류 == 3) 상가[수] = osoko_zenbaki();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); konstante_SEGUNDOA_balio[수] = 상번호(); }
            else hutsegite_balio("unsupported constant type");
        }
        int baimen_balio = 짧은수();
        if ((baimen_balio & (0x2000 | 0x4000)) != 0) hutsegite_balio("annotation/enum class unsupported");
        Gela_Definizioa_izen[Gela_Definizioa] = klasearen_izen_SMS(상번호());
        종부모[Gela_Definizioa] = klasearen_izen_SMS(상번호());
        int interfaze_ZENBATU = 짧은수(); if (interfaze_ZENBATU > 16) { hutsegite_balio("interface count limit"); return; }
        Gela_interfaze_ZENBATU[Gela_Definizioa] = interfaze_ZENBATU;
        for (int Loop_INDIZE = 0; Loop_INDIZE < interfaze_ZENBATU; Loop_INDIZE++) Gela_interfaze[Gela_Definizioa * 16 + Loop_INDIZE] = klasearen_izen_SMS(상번호());
        int eremu_ZENBATU = 짧은수();
        if (eremu_ZENBATU > 512 - 칸수) { hutsegite_balio("field count limit (512)"); return; }
        for (int Loop_INDIZE = 0; Loop_INDIZE < eremu_ZENBATU && !errorea; Loop_INDIZE++) {
            int fitxategi_INDIZE = 칸수++; 칸주인[fitxategi_INDIZE] = Gela_Definizioa; 칸권한[fitxategi_INDIZE] = 짧은수(); 칸이름[fitxategi_INDIZE] = 상번호(); 칸형[fitxategi_INDIZE] = 상번호();
            txeke_konstante(칸이름[fitxategi_INDIZE], 1); txeke_konstante(칸형[fitxategi_INDIZE], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[칸형[fitxategi_INDIZE]]; int Kategoria_KODE = 서술형(읽기위치 + konstante_SEGUNDOA_balio[칸형[fitxategi_INDIZE]], false); 읽기위치 = 보존값;
            if ((칸권한[fitxategi_INDIZE] & 8) == 0) 칸위치[fitxategi_INDIZE] = 종칸수[Gela_Definizioa]++;
            int atributu_datuak = 짧은수();
            for (int barnekoa_kargu = 0; barnekoa_kargu < atributu_datuak && !errorea; barnekoa_kargu++) {
                int izen_konstante = 상번호(), 유효길이 = osoko_zenbaki();
                if (Word_SMS(izen_konstante, "ConstantValue") && 유효길이 == 2) {
                    int datuak_balio = 상번호();
                    if (Kategoria_KODE == 1 && txeke_konstante(datuak_balio, 3)) 칸값[fitxategi_INDIZE] = 상가[datuak_balio];
                    else if (Kategoria_KODE == 2 && txeke_konstante(datuak_balio, 8)) 칸값[fitxategi_INDIZE] = konstante_SMS(상가[datuak_balio]);
                } else 건너(유효길이);
            }
        }
        int elementu_ZENBATU = 짧은수();
        if (elementu_ZENBATU > 512 - 함수수) { hutsegite_balio("method count limit (512)"); return; }
        for (int Loop_INDIZE = 0; Loop_INDIZE < elementu_ZENBATU && !errorea; Loop_INDIZE++) {
            int 수 = 함수수++; 함수주인[수] = Gela_Definizioa;
            함수권한[수] = 짧은수(); 함수명[수] = 상번호(); 함수형[수] = 상번호();
            txeke_konstante(함수명[수], 1); 서술읽기(수);
            if ((함수권한[수] & 8) == 0) {
                if (함수인수수[수] == 16) { hutsegite_balio("too many instance method arguments"); return; }
                for (int Konparazioa_kargu = 함수인수수[수]; Konparazioa_kargu > 0; Konparazioa_kargu--) 함수인수형[수 * 16 + Konparazioa_kargu] = 함수인수형[수 * 16 + Konparazioa_kargu - 1];
                함수인수형[수 * 16] = 2; 함수인수수[수]++;
            }
            if ((함수권한[수] & 0x100) != 0) hutsegite_balio("user native method unsupported");
            if (Word_SMS(함수명[수], "<clinit>")) hasieratu_Gela_Definizioa[Gela_Definizioa] = 수 + 1;
            for (int aurrekoa_balio = 0; aurrekoa_balio < 수; aurrekoa_balio++) if (함수주인[aurrekoa_balio] == Gela_Definizioa && 같은말(함수명[aurrekoa_balio], 함수명[수]) && 같은말(함수형[aurrekoa_balio], 함수형[수])) hutsegite_balio("duplicate method");
            int atributu_ZENBATU = 짧은수();
            for (int atributu_balio = 0; atributu_balio < atributu_ZENBATU && !errorea; atributu_balio++) {
                int Izena = 상번호(), luzera_balio = osoko_zenbaki(), Exekutatu_2 = 읽기위치;
                if (!klip(Exekutatu_2, luzera_balio)) { hutsegite_balio("truncated method attribute"); break; }
                if (Word_SMS(Izena, "Code")) {
                    if (함수시작[수] != 0) hutsegite_balio("duplicate Code attribute");
                    함수스택[수] = 짧은수(); 함수지역[수] = 짧은수(); int KODE_luzera = osoko_zenbaki();
                    if (함수스택[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || KODE_luzera < 1 || KODE_luzera > 8192) hutsegite_balio("method memory limits exceeded");
                    함수시작[수] = 읽기위치; 건너(KODE_luzera); 함수끝[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { hutsegite_balio("exception table limit"); return; }
                    for (int barnekoa_kargu = 0; barnekoa_kargu < 잡는수; barnekoa_kargu++) {
                        int errore_Erreferentzia_materiala = 잡기수++; 잡기함수[errore_Erreferentzia_materiala] = 수;
                        잡기시작[errore_Erreferentzia_materiala] = 함수시작[수] + 짧은수(); 잡기끝[errore_Erreferentzia_materiala] = 함수시작[수] + 짧은수();
                        잡기위치[errore_Erreferentzia_materiala] = 함수시작[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[errore_Erreferentzia_materiala] = 부호값 == 0 ? 0 : klasearen_izen_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != Exekutatu_2 + luzera_balio) hutsegite_balio("Code attribute size mismatch");
                } else 건너(luzera_balio);
            }
            if ((함수권한[수] & 0x400) != 0) continue;
            if (함수시작[수] == 0) hutsegite_balio("missing Code attribute");
            int 칸 = 함수시작[수];
            while (칸 < 함수끝[수] && !errorea) {
                int luzera_balio = 길이읽기(칸, 함수시작[수], 함수끝[수]);
                if (luzera_balio == 0) { hutsegite_balio("unsupported or truncated bytecode"); break; }
                경계[칸] = 수 + 1; 칸 += luzera_balio;
            }
            칸 = 함수시작[수];
            while (칸 < 함수끝[수] && !errorea) {
                int balio = Fitxategia[칸];
                if (balio >= 153 && balio <= 167 || balio == 198 || balio == 199) txeke_helburu_balio(칸 + (short)(Fitxategia[칸 + 1] << 8 | Fitxategia[칸 + 2]), 수);
                if (balio == 200) txeke_helburu_balio(칸 + kargu_osoko_zenbaki(칸 + 1), 수);
                if (balio == 170 || balio == 171) {
                    int 읽는자리 = 칸 + 1; while ((읽는자리 - 함수시작[수]) % 4 != 0) 읽는자리++;
                    txeke_helburu_balio(칸 + kargu_osoko_zenbaki(읽는자리), 수);
                    int sarrera_ZENBATU = balio == 170 ? kargu_osoko_zenbaki(읽는자리 + 8) - kargu_osoko_zenbaki(읽는자리 + 4) + 1 : kargu_osoko_zenbaki(읽는자리 + 4);
                    읽는자리 += balio == 170 ? 12 : 8;
                    for (int barnekoa_kargu = 0; barnekoa_kargu < sarrera_ZENBATU; barnekoa_kargu++) txeke_helburu_balio(칸 + kargu_osoko_zenbaki(읽는자리 + barnekoa_kargu * (balio == 170 ? 4 : 8) + (balio == 170 ? 0 : 4)), 수);
                }
                칸 += 길이읽기(칸, 함수시작[수], 함수끝[수]);
            }
            for (int barnekoa_kargu = 0; barnekoa_kargu < 잡기수; barnekoa_kargu++) if (잡기함수[barnekoa_kargu] == 수) {
                txeke_helburu_balio(잡기시작[barnekoa_kargu], 수); txeke_helburu_balio(잡기위치[barnekoa_kargu], 수);
                if (잡기끝[barnekoa_kargu] != 함수끝[수]) txeke_helburu_balio(잡기끝[barnekoa_kargu], 수);
                if (잡기시작[barnekoa_kargu] >= 잡기끝[barnekoa_kargu]) hutsegite_balio("invalid exception range");
            }
        }
        if (!errorea) 속성건너();
        if (읽기위치 != Tamaina) hutsegite_balio("extra class file data");
    }
    static int esleitu_biltegi(int 종류, int luzera_balio) { return 새기억(종류, luzera_balio); }
    static boolean objektu_balio(int Erreferentzia_materiala, int 종류) {
        if (!객체유효(Erreferentzia_materiala)) return false;
        if (힙[Erreferentzia_materiala] != 종류) { hutsegite_balio("object type mismatch"); return false; }
        return true;
    }
    static int konstante_SMS(int INDIZE) {
        if (!txeke_konstante(INDIZE, 1)) return 0;
        if (kate_Erreferentzia_materiala[INDIZE] != 0) return kate_Erreferentzia_materiala[INDIZE];
        int Erreferentzia_materiala = esleitu_biltegi(1, konstante_SEGUNDOA_balio[INDIZE]); if (errorea) return 0;
        int 끝 = 상가[INDIZE] + konstante_SEGUNDOA_balio[INDIZE], 수 = 상가[INDIZE], luzera_balio = 0;
        while (수 < 끝 && !errorea) {
            int balio = Fitxategia[수++];
            if (balio == 0) hutsegite_balio("invalid modified UTF-8");
            else if (balio >= 192 && balio <= 223 && 수 < 끝) {
                int Hurrengoa_elementu = Fitxategia[수++];
                if ((Hurrengoa_elementu & 192) != 128) hutsegite_balio("invalid modified UTF-8");
                balio = (balio & 31) << 6 | Hurrengoa_elementu & 63;
                if (balio != 0 && balio < 128) hutsegite_balio("overlong modified UTF-8");
            } else if (balio >= 224 && balio <= 239 && 수 + 1 < 끝) {
                int 가 = Fitxategia[수++], 나 = Fitxategia[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) hutsegite_balio("invalid modified UTF-8");
                balio = (balio & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (balio < 2048) hutsegite_balio("overlong modified UTF-8");
            } else if (balio >= 128) hutsegite_balio("invalid modified UTF-8");
            힙[Erreferentzia_materiala + 2 + luzera_balio++] = balio;
        }
        힙[Erreferentzia_materiala + 1] = luzera_balio; kate_Erreferentzia_materiala[INDIZE] = Erreferentzia_materiala; return Erreferentzia_materiala;
    }
    static int Ostalari_karaktere(String balio) {
        int Erreferentzia_materiala = esleitu_biltegi(1, balio.length()); if (errorea) return 0;
        for (int 수 = 0; 수 < balio.length(); 수++) 힙[Erreferentzia_materiala + 2 + 수] = balio.charAt(수);
        return Erreferentzia_materiala;
    }
    static void idatzi_SMS(int Erreferentzia_materiala) {
        if (Erreferentzia_materiala == 0) { erabiltzaile.Idatzi("null"); return; }
        if (!objektu_balio(Erreferentzia_materiala, 1)) return;
        for (int 수 = 0; 수 < 힙[Erreferentzia_materiala + 1]; 수++) erabiltzaile.idatzi_karaktere_balio(힙[Erreferentzia_materiala + 2 + 수]);
    }
    static int digitu_karaktere(int balio) {
        int Erreferentzia_materiala = esleitu_biltegi(1, 11); if (errorea) return 0;
        int luzera_balio = 0;
        if (balio < 0) 힙[Erreferentzia_materiala + 2 + luzera_balio++] = '-'; else balio = -balio;
        int kargu_INDIZE = 1000000000; boolean Exekutatu_2 = false;
        while (kargu_INDIZE != 0) {
            int 수 = -(balio / kargu_INDIZE);
            if (수 != 0 || Exekutatu_2 || kargu_INDIZE == 1) { 힙[Erreferentzia_materiala + 2 + luzera_balio++] = '0' + 수; Exekutatu_2 = true; }
            balio %= kargu_INDIZE; kargu_INDIZE /= 10;
        }
        힙[Erreferentzia_materiala + 1] = luzera_balio; return Erreferentzia_materiala;
    }
    static int 정수해독(int Erreferentzia_materiala) {
        if (!objektu_balio(Erreferentzia_materiala, 1)) return 0;
        int luzera_balio = 힙[Erreferentzia_materiala + 1], 수 = 0, balio = 0; boolean 음수 = false;
        if (luzera_balio > 0 && (힙[Erreferentzia_materiala + 2] == '-' || 힙[Erreferentzia_materiala + 2] == '+')) { 음수 = 힙[Erreferentzia_materiala + 2] == '-'; 수++; }
        if (수 == luzera_balio) hutsegite_balio("NumberFormatException");
        for (; 수 < luzera_balio && !errorea; 수++) {
            int digitu_balio = 힙[Erreferentzia_materiala + 2 + 수] - '0';
            if (digitu_balio < 0 || digitu_balio > 9 || balio < -214748364 || balio == -214748364 && digitu_balio > (음수 ? 8 : 7)) hutsegite_balio("NumberFormatException");
            balio = balio * 10 - digitu_balio;
        }
        return 음수 ? balio : -balio;
    }
    static void 넣기(int balio, int MOTA_balio) {
        if (errorea) return;
        if (marko_INDIZE < 0 || marko_pila[marko_INDIZE] >= 함수스택[틀함수[marko_INDIZE]]) { hutsegite_balio("operand stack overflow"); return; }
        int 칸 = marko_INDIZE * 128 + marko_pila[marko_INDIZE]++; 스택값[칸] = balio; 스택형[칸] = MOTA_balio;
    }
    static int 빼기(int MOTA_balio) {
        if (errorea) return 0;
        if (marko_INDIZE < 0 || marko_pila[marko_INDIZE] < 1) { hutsegite_balio("operand stack underflow"); return 0; }
        int 칸 = marko_INDIZE * 128 + --marko_pila[marko_INDIZE]; itzuli_MOTA = 스택형[칸];
        if (MOTA_balio != 0 && itzuli_MOTA != MOTA_balio) hutsegite_balio("operand type mismatch");
        if (itzuli_MOTA == 2) babestu_balio(스택값[칸]);
        return 스택값[칸];
    }
    static void 지역읽기(int INDIZE, int MOTA_balio) {
        if (INDIZE >= 함수지역[틀함수[marko_INDIZE]] || INDIZE < 0 || lokal_MOTA[marko_INDIZE * 128 + INDIZE] != MOTA_balio) { hutsegite_balio("invalid or uninitialized local"); return; }
        넣기(lokal_balio[marko_INDIZE * 128 + INDIZE], MOTA_balio);
    }
    static void idatzi_lokal(int INDIZE, int MOTA_balio) {
        if (INDIZE >= 함수지역[틀함수[marko_INDIZE]] || INDIZE < 0) { hutsegite_balio("local index out of range"); return; }
        int balio = 빼기(MOTA_balio); lokal_balio[marko_INDIZE * 128 + INDIZE] = balio; lokal_MOTA[marko_INDIZE * 128 + INDIZE] = MOTA_balio;
    }
    static int 명바() {
        int Posizioa = marko_kargu[marko_INDIZE];
        if (Posizioa < 함수시작[틀함수[marko_INDIZE]] || Posizioa >= 함수끝[틀함수[marko_INDIZE]]) { hutsegite_balio("instruction pointer out of range"); return 0; }
        marko_kargu[marko_INDIZE]++; return Fitxategia[Posizioa];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void eraman_balio(int Posizioa) {
        int FUNTZIOA_balio = 틀함수[marko_INDIZE];
        if (Posizioa < 함수시작[FUNTZIOA_balio] || Posizioa >= 함수끝[FUNTZIOA_balio] || 경계[Posizioa] != FUNTZIOA_balio + 1) hutsegite_balio("invalid branch target");
        else marko_kargu[marko_INDIZE] = Posizioa;
    }
    static void 호출(int FUNTZIOA_balio) {
        if (marko_INDIZE % 32 == 31) { hutsegite_balio("call stack limit (32)"); return; }
        int Hurrengoa_elementu = marko_INDIZE + 1;
        for (int 수 = 0; 수 < 128; 수++) lokal_MOTA[Hurrengoa_elementu * 128 + 수] = 0;
        for (int 수 = 함수인수수[FUNTZIOA_balio] - 1; 수 >= 0; 수--) {
            lokal_balio[Hurrengoa_elementu * 128 + 수] = 빼기(함수인수형[FUNTZIOA_balio * 16 + 수]); lokal_MOTA[Hurrengoa_elementu * 128 + 수] = 함수인수형[FUNTZIOA_balio * 16 + 수];
        }
        if (errorea) return;
        marko_INDIZE = Hurrengoa_elementu; hasieratu_marko[marko_INDIZE] = 0; 틀함수[marko_INDIZE] = FUNTZIOA_balio; marko_kargu[marko_INDIZE] = 함수시작[FUNTZIOA_balio]; marko_pila[marko_INDIZE] = 0;
    }
    static void itzuli_neurria(int MOTA_balio) {
        if (MOTA_balio != 함수반환[틀함수[marko_INDIZE]]) { hutsegite_balio("return type mismatch"); return; }
        int balio = MOTA_balio == 0 ? 0 : 빼기(MOTA_balio);
        if (hasieratu_marko[marko_INDIZE] != 0) Gela_Definizioa_Egoera[hasieratu_marko[marko_INDIZE] - 1] = 2;
        if (틀잠금[marko_INDIZE] != 0) { 잠금풀기(틀잠금[marko_INDIZE]); 틀잠금[marko_INDIZE] = 0; }
        marko_INDIZE--; if (marko_INDIZE >= 현재가닥 * 32 && MOTA_balio != 0) 넣기(balio, MOTA_balio);
    }
    static int[] Stream_fitxategi_izen = new int[64];
    static void fitxategi_Stream_dei(int jabe_balio, int Izena, int formatu_balio, int Komandoa) {
        boolean Irteera = Word_SMS(jabe_balio, "java/io/FileOutputStream");
        int 종류 = Irteera ? 6 : 5;
        if (Komandoa == 183 && Word_SMS(Izena, "<init>")) {
            boolean 이어 = false;
            if (Irteera && Word_SMS(formatu_balio, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(formatu_balio, "(Ljava/lang/String;)V")) { hutsegite_balio("unsupported file stream constructor"); return; }
            int fitxategi_sarrera_izen = 빼기(2), Stream_balio = 빼기(2);
            if (!objektu_balio(fitxategi_sarrera_izen, 1) || !objektu_balio(Stream_balio, 종류) || errorea) return;
            if (힙[Stream_balio + 3] != 0) { hutsegite_balio("file stream already initialized"); return; }
            int luzera_balio = 힙[fitxategi_sarrera_izen + 1];
            if (luzera_balio < 1 || luzera_balio > 63) { hutsegite_balio("invalid file name length"); return; }
            for (int 칸 = 0; 칸 < luzera_balio; 칸++) {
                int balio = 힙[fitxategi_sarrera_izen + 2 + 칸];
                if (balio < 1) { hutsegite_balio("invalid file stream path"); return; }
                Stream_fitxategi_izen[칸] = balio;
            }
            Stream_fitxategi_izen[luzera_balio] = 0;
            int 서술자 = erabiltzaile.파일서술자열기(Stream_fitxategi_izen, Irteera ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { hutsegite_balio("FileNotFoundException: file open failed"); return; }
            힙[Stream_balio + 2] = 서술자; 힙[Stream_balio + 3] = 1;
            return;
        }
        if (Komandoa != 182) { hutsegite_balio("invalid file stream invocation"); return; }
        if ((Irteera && Word_SMS(Izena, "write") || !Irteera && Word_SMS(Izena, "read"))
            && (Word_SMS(formatu_balio, Irteera ? "([B)V" : "([B)I") || Word_SMS(formatu_balio, Irteera ? "([BII)V" : "([BII)I"))) {
            boolean klip_balio = Word_SMS(formatu_balio, Irteera ? "([BII)V" : "([BII)I");
            int sarrera_ZENBATU = klip_balio ? 빼기(1) : 0, 시작점 = klip_balio ? 빼기(1) : 0, datuak_matrize = 빼기(2), objektu_Erreferentzia_materiala = 빼기(2);
            if (!objektu_balio(datuak_matrize, 20) || !objektu_balio(objektu_Erreferentzia_materiala, 종류)) return;
            if (!klip_balio) sarrera_ZENBATU = 힙[datuak_matrize + 1];
            if (시작점 < 0 || sarrera_ZENBATU < 0 || 시작점 > 힙[datuak_matrize + 1] - sarrera_ZENBATU) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[objektu_Erreferentzia_materiala + 3] == 0 || 힙[objektu_Erreferentzia_materiala + 2] < 0) { hutsegite_balio("IOException: stream closed"); return; }
            int Osatutakoak_ZENBATU = 0;
            while (Osatutakoak_ZENBATU < sarrera_ZENBATU && !errorea) {
                int 반환값 = Irteera ? erabiltzaile.파일한바이트쓰기(힙[objektu_Erreferentzia_materiala + 2], 힙[datuak_matrize + 2 + 시작점 + Osatutakoak_ZENBATU]) : erabiltzaile.파일한바이트읽기(힙[objektu_Erreferentzia_materiala + 2]);
                if (반환값 < 0) { hutsegite_balio(Irteera ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!Irteera && 반환값 == 256) break;
                if (!Irteera) 힙[datuak_matrize + 2 + 시작점 + Osatutakoak_ZENBATU] = (byte)반환값;
                Osatutakoak_ZENBATU++;
            }
            if (!Irteera) 넣기(sarrera_ZENBATU != 0 && Osatutakoak_ZENBATU == 0 ? -1 : Osatutakoak_ZENBATU, 1);
            return;
        }
        if (Irteera && Word_SMS(Izena, "flush") && Word_SMS(formatu_balio, "()V")) { int objektu_Erreferentzia_materiala = 빼기(2); if (objektu_balio(objektu_Erreferentzia_materiala, 종류) && 힙[objektu_Erreferentzia_materiala + 2] < 0) hutsegite_balio("IOException: stream closed"); return; }
        int Ekintza = -1, balio = 0;
        if (Word_SMS(Izena, "close") && Word_SMS(formatu_balio, "()V")) Ekintza = 0;
        if (!Irteera && Word_SMS(Izena, "read") && Word_SMS(formatu_balio, "()I")) Ekintza = 1;
        if (Irteera && Word_SMS(Izena, "write") && Word_SMS(formatu_balio, "(I)V")) { Ekintza = 2; balio = 빼기(1); }
        if (Ekintza < 0) { hutsegite_balio("unsupported file stream method"); return; }
        int Stream_balio = 빼기(2);
        if (!objektu_balio(Stream_balio, 종류) || errorea) return;
        if (힙[Stream_balio + 3] == 0) { hutsegite_balio("uninitialized file stream"); return; }
        int 서술자 = 힙[Stream_balio + 2];
        if (Ekintza == 0) {
            if (서술자 >= 0 && erabiltzaile.파일서술자닫기(서술자) < 0) hutsegite_balio("IOException: close failed");
            힙[Stream_balio + 2] = -1; return;
        }
        if (서술자 < 0) { hutsegite_balio("IOException: stream closed"); return; }
        if (Ekintza == 1) {
            int EMAITZA = erabiltzaile.파일한바이트읽기(서술자);
            if (EMAITZA < -1) hutsegite_balio("IOException: read failed"); else 넣기(EMAITZA == 256 ? -1 : EMAITZA, 1);
        } else if (erabiltzaile.파일한바이트쓰기(서술자, balio) != 1) hutsegite_balio("IOException: write failed");
    }
    static void 함수호출(int INDIZE, int Komandoa) {
        if (INDIZE <= 0 || INDIZE >= konstante_etiketa.length || (konstante_etiketa[INDIZE] != 10 && konstante_etiketa[INDIZE] != 11)) { hutsegite_balio("invalid method reference"); return; }
        int jabe_balio = klasearen_izen_SMS(상가[INDIZE]), Izena = Erreferentzia_materiala_izen(konstante_SEGUNDOA_balio[INDIZE]), formatu_balio = Erreferentzia_materiala_MOTA(konstante_SEGUNDOA_balio[INDIZE]);
        if (errorea) return;
        if (기본호출(jabe_balio, Izena, formatu_balio, Komandoa)) return;
        if (Word_SMS(jabe_balio, "java/io/FileInputStream") || Word_SMS(jabe_balio, "java/io/FileOutputStream")) {
            fitxategi_Stream_dei(jabe_balio, Izena, formatu_balio, Komandoa); return;
        }
        if (Komandoa == 184 && Word_SMS(jabe_balio, "java/lang/Integer") && Word_SMS(Izena, "parseInt") && Word_SMS(formatu_balio, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Komandoa == 182 && Word_SMS(jabe_balio, "java/io/PrintStream") && (Word_SMS(Izena, "println") || Word_SMS(Izena, "print"))) {
            int MOTA_balio = 0, balio = 0;
            if (Word_SMS(formatu_balio, "(I)V")) { MOTA_balio = 1; balio = 빼기(1); }
            else if (Word_SMS(formatu_balio, "(Z)V")) { MOTA_balio = 2; balio = 빼기(1); }
            else if (Word_SMS(formatu_balio, "(C)V")) { MOTA_balio = 3; balio = 빼기(1); }
            else if (Word_SMS(formatu_balio, "(Ljava/lang/String;)V")) { MOTA_balio = 4; balio = 빼기(2); }
            else if (!Word_SMS(formatu_balio, "()V") || !Word_SMS(Izena, "println")) hutsegite_balio("unsupported print descriptor");
            if (빼기(2) != -1) hutsegite_balio("invalid PrintStream receiver");
            if (errorea) return;
            if (MOTA_balio == 1) 자바도구.수쓰기(balio);
            if (MOTA_balio == 2) erabiltzaile.Idatzi(balio == 0 ? "false" : "true");
            if (MOTA_balio == 3) erabiltzaile.idatzi_karaktere_balio(balio & 65535);
            if (MOTA_balio == 4) idatzi_SMS(balio);
            if (Word_SMS(Izena, "println")) erabiltzaile.idatzi_karaktere_balio(10);
            return;
        }
        if (Komandoa == 182 && Word_SMS(jabe_balio, "java/lang/String")) {
            if (Word_SMS(Izena, "length") && Word_SMS(formatu_balio, "()I")) {
                int Erreferentzia_materiala = 빼기(2); if (objektu_balio(Erreferentzia_materiala, 1)) 넣기(힙[Erreferentzia_materiala + 1], 1); return;
            }
            if (Word_SMS(Izena, "charAt") && Word_SMS(formatu_balio, "(I)C")) {
                int azpiindize_balio = 빼기(1), Erreferentzia_materiala = 빼기(2);
                if (objektu_balio(Erreferentzia_materiala, 1)) {
                    if (azpiindize_balio < 0 || azpiindize_balio >= 힙[Erreferentzia_materiala + 1]) hutsegite_balio("StringIndexOutOfBoundsException"); else 넣기(힙[Erreferentzia_materiala + 2 + azpiindize_balio], 1);
                }
                return;
            }
        }
        if (Word_SMS(jabe_balio, "java/lang/StringBuilder")) {
            if (Komandoa == 183 && Word_SMS(Izena, "<init>") && Word_SMS(formatu_balio, "()V")) { objektu_balio(빼기(2), 4); return; }
            if (Komandoa == 182 && Word_SMS(Izena, "toString") && Word_SMS(formatu_balio, "()Ljava/lang/String;")) {
                int Erreferentzia_materiala = 빼기(2); if (objektu_balio(Erreferentzia_materiala, 4)) 넣기(힙[Erreferentzia_materiala + 2] == 0 ? Ostalari_karaktere("") : 힙[Erreferentzia_materiala + 2], 2); return;
            }
            if (Komandoa == 182 && Word_SMS(Izena, "append")) {
                int Testua = 0;
                if (Word_SMS(formatu_balio, "(I)Ljava/lang/StringBuilder;")) Testua = digitu_karaktere(빼기(1));
                else if (Word_SMS(formatu_balio, "(Z)Ljava/lang/StringBuilder;")) Testua = Ostalari_karaktere(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(formatu_balio, "(C)Ljava/lang/StringBuilder;")) {
                    int balio = 빼기(1); Testua = esleitu_biltegi(1, 1); if (!errorea) 힙[Testua + 2] = balio & 65535;
                }
                else if (Word_SMS(formatu_balio, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Testua = 빼기(2); if (Testua == 0) Testua = Ostalari_karaktere("null"); }
                else { hutsegite_balio("unsupported StringBuilder append"); return; }
                int Erreferentzia_materiala = 빼기(2); if (!objektu_balio(Erreferentzia_materiala, 4) || !objektu_balio(Testua, 1)) return;
                int aurrekoa_balio = 힙[Erreferentzia_materiala + 2], aurrekoa_balio_luzera = aurrekoa_balio == 0 ? 0 : 힙[aurrekoa_balio + 1], ATZERA_balio_luzera = 힙[Testua + 1];
                int 새글 = esleitu_biltegi(1, aurrekoa_balio_luzera + ATZERA_balio_luzera); if (errorea) return;
                for (int 수 = 0; 수 < aurrekoa_balio_luzera; 수++) 힙[새글 + 2 + 수] = 힙[aurrekoa_balio + 2 + 수];
                for (int 수 = 0; 수 < ATZERA_balio_luzera; 수++) 힙[새글 + 2 + aurrekoa_balio_luzera + 수] = 힙[Testua + 2 + 수];
                힙[Erreferentzia_materiala + 2] = 새글; 넣기(Erreferentzia_materiala, 2); return;
            }
        }
        int Gela_Definizioa = Bilatu_Gela_Definizioa(jabe_balio); if (Gela_Definizioa < 0 || errorea) return;
        int fitxategi_INDIZE = 함수찾기(Gela_Definizioa, Izena, formatu_balio);
        if (fitxategi_INDIZE < 0) {
            for (int karaktere_kode = Gela_Definizioa, sarrera_ZENBATU = 0; karaktere_kode >= 0 && sarrera_ZENBATU < 16; sarrera_ZENBATU++, karaktere_kode = 부모종(karaktere_kode))
                if (Word_SMS(종부모[karaktere_kode], "java/lang/Thread")) { 가닥호출(Izena, formatu_balio, Komandoa); return; }
            hutsegite_balio("NoSuchMethodError"); return;
        }
        if (((함수권한[fitxategi_INDIZE] & 8) != 0) != (Komandoa == 184)) { hutsegite_balio("method static/instance mismatch"); return; }
        if (Komandoa == 184) { if (!hasieratu(함수주인[fitxategi_INDIZE], marko_instrukzio[marko_INDIZE])) return; }
        else {
            int 읽는자리 = marko_pila[marko_INDIZE] - 함수인수수[fitxategi_INDIZE];
            if (읽는자리 < 0 || 스택형[marko_INDIZE * 128 + 읽는자리] != 2) { hutsegite_balio("invalid method receiver"); return; }
            int objektu_Erreferentzia_materiala = 스택값[marko_INDIZE * 128 + 읽는자리];
            if (!객체유효(objektu_Erreferentzia_materiala)) return;
            if (힙[objektu_Erreferentzia_materiala] < 32 || !종포함(힙[objektu_Erreferentzia_materiala] - 32, jabe_balio)) { hutsegite_balio("method receiver type mismatch"); return; }
            if (Komandoa != 183) fitxategi_INDIZE = 함수찾기(힙[objektu_Erreferentzia_materiala] - 32, Izena, formatu_balio);
        }
        if (fitxategi_INDIZE < 0 || (함수권한[fitxategi_INDIZE] & 0x400) != 0) { hutsegite_balio("AbstractMethodError"); return; }
        int 잠금참조 = 0;
        if ((함수권한[fitxategi_INDIZE] & 32) != 0) {
            if (Komandoa == 184) { int karaktere_kode = 함수주인[fitxategi_INDIZE]; if (종잠금[karaktere_kode] == 0) 종잠금[karaktere_kode] = esleitu_biltegi(8, 0); 잠금참조 = 종잠금[karaktere_kode]; }
            else 잠금참조 = 스택값[marko_INDIZE * 128 + marko_pila[marko_INDIZE] - 함수인수수[fitxategi_INDIZE]];
            if (!잠금얻기(잠금참조)) { if (!errorea) marko_kargu[marko_INDIZE] = marko_instrukzio[marko_INDIZE]; return; }
        }
        호출(fitxategi_INDIZE); if (!errorea) 틀잠금[marko_INDIZE] = 잠금참조;
    }
    static boolean 배열저장가능(int matrize_Erreferentzia_materiala, int datuak_balio) {
        if (datuak_balio == 0 || matrize_elementu[matrize_Erreferentzia_materiala] == 0) return true;
        boolean 성공여부 = matrize_elementu[matrize_Erreferentzia_materiala] == -1 ? (datuak_balio > 0 && datuak_balio < 힙끝 && 힙[datuak_balio] == 1) : 맞는객체(datuak_balio, matrize_elementu[matrize_Erreferentzia_materiala]);
        if (!성공여부 && !errorea) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int 배열칸(int Erreferentzia_materiala, int azpiindize_balio, int MOTA_balio) {
        if (!objektu_balio(Erreferentzia_materiala, MOTA_balio)) return 0;
        if (azpiindize_balio < 0 || azpiindize_balio >= 힙[Erreferentzia_materiala + 1]) { hutsegite_balio("ArrayIndexOutOfBoundsException"); return 0; }
        return Erreferentzia_materiala + 2 + azpiindize_balio;
    }
    static void exekutatu_komando() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (errorea) { if (던진객체 != 0) helduleku_salbuespen(); if (errorea || marko_INDIZE < 현재가닥 * 32) break; }
            if (marko_INDIZE < 현재가닥 * 32 || aldatu_eskaera || --조각 == 0) { if (!ALDATU_hari()) break; 조각 = 100; }
            if (marko_INDIZE == 0 && Gela_Definizioa_Egoera[sarrera_Gela_Definizioa] != 2 && !hasieratu(sarrera_Gela_Definizioa, marko_kargu[marko_INDIZE])) continue;
            if (marko_INDIZE == 현재가닥 * 32 && 현재가닥 != 0 && (함수권한[틀함수[marko_INDIZE]] & 32) != 0 && 틀잠금[marko_INDIZE] == 0) {
                int objektu_Erreferentzia_materiala = hari_helburu[현재가닥]; if (!잠금얻기(objektu_Erreferentzia_materiala)) { if (errorea) break; continue; } 틀잠금[marko_INDIZE] = objektu_Erreferentzia_materiala;
            }
            잠시수 = 0;
            if (--남음 == 0) { hutsegite_balio("instruction limit (500000)"); break; }
            int Exekutatu_2 = marko_kargu[marko_INDIZE]; marko_instrukzio[marko_INDIZE] = Exekutatu_2; int balio = 명바();
            if (errorea) break;
            if (balio == 0) continue;
            if (balio == 1) { 넣기(0, 2); continue; }
            if (balio >= 2 && balio <= 8) { 넣기(balio - 3, 1); continue; }
            if (balio == 16) { 넣기((byte)명바(), 1); continue; }
            if (balio == 17) { 넣기((short)명짧(), 1); continue; }
            if (balio == 18 || balio == 19) {
                int 수 = 함수주인[틀함수[marko_INDIZE]] * 512 + (balio == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= konstante_etiketa.length) hutsegite_balio("invalid ldc constant");
                else if (konstante_etiketa[수] == 3) 넣기(상가[수], 1);
                else if (konstante_etiketa[수] == 8) 넣기(konstante_SMS(상가[수]), 2);
                else hutsegite_balio("unsupported ldc constant");
                continue;
            }
            if (balio == 21 || balio == 25) { 지역읽기(명바(), balio == 21 ? 1 : 2); continue; }
            if (balio >= 26 && balio <= 29) { 지역읽기(balio - 26, 1); continue; }
            if (balio >= 42 && balio <= 45) { 지역읽기(balio - 42, 2); continue; }
            if (balio == 54 || balio == 58) { idatzi_lokal(명바(), balio == 54 ? 1 : 2); continue; }
            if (balio >= 59 && balio <= 62) { idatzi_lokal(balio - 59, 1); continue; }
            if (balio >= 75 && balio <= 78) { idatzi_lokal(balio - 75, 2); continue; }
            if (balio == 46 || balio >= 50 && balio <= 53) {
                int sarrera_kargu = 빼기(1), objektu_Erreferentzia_materiala = 빼기(2), Kategoria_KODE = balio == 46 ? 2 : balio == 50 ? 3 : balio == 51 ? 20 : balio == 52 ? 22 : 23;
                if (balio == 51 && objektu_Erreferentzia_materiala > 0 && objektu_Erreferentzia_materiala < 힙끝 && 힙[objektu_Erreferentzia_materiala] == 21) Kategoria_KODE = 21;
                int 읽는자리 = 배열칸(objektu_Erreferentzia_materiala, sarrera_kargu, Kategoria_KODE); if (!errorea) 넣기(힙[읽는자리], balio == 50 ? 2 : 1); continue;
            }
            if (balio == 79 || balio >= 83 && balio <= 86) {
                int sarrera_Erreferentzia_materiala = 빼기(balio == 83 ? 2 : 1), sarrera_kargu = 빼기(1), objektu_Erreferentzia_materiala = 빼기(2), Kategoria_KODE = balio == 79 ? 2 : balio == 83 ? 3 : balio == 84 ? 20 : balio == 85 ? 22 : 23;
                if (balio == 84 && objektu_Erreferentzia_materiala > 0 && objektu_Erreferentzia_materiala < 힙끝 && 힙[objektu_Erreferentzia_materiala] == 21) Kategoria_KODE = 21;
                int 읽는자리 = 배열칸(objektu_Erreferentzia_materiala, sarrera_kargu, Kategoria_KODE);
                if (!errorea && Kategoria_KODE == 3 && !배열저장가능(objektu_Erreferentzia_materiala, sarrera_Erreferentzia_materiala)) continue;
                if (!errorea) 힙[읽는자리] = Kategoria_KODE == 20 ? (byte)sarrera_Erreferentzia_materiala : Kategoria_KODE == 21 ? sarrera_Erreferentzia_materiala & 1 : Kategoria_KODE == 22 ? (char)sarrera_Erreferentzia_materiala : Kategoria_KODE == 23 ? (short)sarrera_Erreferentzia_materiala : sarrera_Erreferentzia_materiala;
                continue;
            }
            if (balio >= 87 && balio <= 95) { pila_instrukzio(balio); continue; }
            if (balio == 96 || balio == 100 || balio == 104 || balio == 108 || balio == 112 || balio == 120
                || balio == 122 || balio == 124 || balio == 126 || balio == 128 || balio == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), EMAITZA = 0;
                if ((balio == 108 || balio == 112) && 나 == 0) { hutsegite_balio("ArithmeticException: / by zero"); continue; }
                if (balio == 96) EMAITZA = 가 + 나;
                if (balio == 100) EMAITZA = 가 - 나;
                if (balio == 104) EMAITZA = 가 * 나;
                if (balio == 108) EMAITZA = 가 / 나;
                if (balio == 112) EMAITZA = 가 % 나;
                if (balio == 120) EMAITZA = 가 << 나;
                if (balio == 122) EMAITZA = 가 >> 나;
                if (balio == 124) EMAITZA = 가 >>> 나;
                if (balio == 126) EMAITZA = 가 & 나;
                if (balio == 128) EMAITZA = 가 | 나;
                if (balio == 130) EMAITZA = 가 ^ 나;
                넣기(EMAITZA, 1); continue;
            }
            if (balio == 116) { 넣기(-빼기(1), 1); continue; }
            if (balio == 132) {
                int lokal_esparru = 명바(), 증분 = (byte)명바(); 지역읽기(lokal_esparru, 1); 넣기(빼기(1) + 증분, 1); idatzi_lokal(lokal_esparru, 1); continue;
            }
            if (balio >= 145 && balio <= 147) {
                int 수 = 빼기(1); 넣기(balio == 145 ? (byte)수 : balio == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (balio >= 153 && balio <= 167 || balio == 198 || balio == 199) {
                int helburu_balio_a0fbc067 = Exekutatu_2 + (short)명짧(); boolean 갈까 = balio == 167;
                if (balio >= 153 && balio <= 158) {
                    int 수 = 빼기(1); 갈까 = balio == 153 ? 수 == 0 : balio == 154 ? 수 != 0 : balio == 155 ? 수 < 0 : balio == 156 ? 수 >= 0 : balio == 157 ? 수 > 0 : 수 <= 0;
                } else if (balio >= 159 && balio <= 166) {
                    int 나 = 빼기(balio >= 165 ? 2 : 1), 가 = 빼기(balio >= 165 ? 2 : 1);
                    갈까 = balio == 159 || balio == 165 ? 가 == 나 : balio == 160 || balio == 166 ? 가 != 나 : balio == 161 ? 가 < 나 : balio == 162 ? 가 >= 나 : balio == 163 ? 가 > 나 : 가 <= 나;
                } else if (balio == 198 || balio == 199) { int 수 = 빼기(2); 갈까 = balio == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) eraman_balio(helburu_balio_a0fbc067); continue;
            }
            if (balio == 172 || balio == 176 || balio == 177) { itzuli_neurria(balio == 172 ? 1 : balio == 176 ? 2 : 0); continue; }
            if (balio >= 178 && balio <= 181) { 필드호출(명상수(), balio, Exekutatu_2); continue; }
            if (balio >= 182 && balio <= 185) {
                int 부호값 = 명상수();
                if (balio == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { hutsegite_balio("invalid invokeinterface operands"); continue; } }
                함수호출(부호값, balio); continue;
            }
            if (balio == 187) { 새객체(klasearen_izen_SMS(명상수()), Exekutatu_2); continue; }
            if (balio == 188 || balio == 189) {
                int Kategoria_KODE = 3, osagai = 0;
                if (balio == 188) { int 임시값 = 명바(); Kategoria_KODE = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else osagai = klasearen_izen_SMS(명상수());
                if (Kategoria_KODE == 0) { hutsegite_balio("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), objektu_Erreferentzia_materiala = esleitu_biltegi(Kategoria_KODE, 유효길이); if (!errorea) matrize_elementu[objektu_Erreferentzia_materiala] = osagai; 넣기(objektu_Erreferentzia_materiala, 2); continue;
            }
            if (balio == 190) {
                int objektu_Erreferentzia_materiala = 빼기(2);
                if (객체유효(objektu_Erreferentzia_materiala)) { int Konparazioa_kargu = 힙[objektu_Erreferentzia_materiala]; if (Konparazioa_kargu != 2 && Konparazioa_kargu != 3 && (Konparazioa_kargu < 20 || Konparazioa_kargu > 23)) hutsegite_balio("not an array"); else 넣기(힙[objektu_Erreferentzia_materiala + 1], 1); }
                continue;
            }
            if (balio == 191) {
                int objektu_Erreferentzia_materiala = 빼기(2); if (객체유효(objektu_Erreferentzia_materiala)) { if (힙[objektu_Erreferentzia_materiala] != 9) hutsegite_balio("athrow requires supported Throwable"); else { 던진객체 = objektu_Erreferentzia_materiala; errorea = true; } }
                continue;
            }
            if (balio == 192 || balio == 193) {
                int izen_konstante = klasearen_izen_SMS(명상수()), objektu_Erreferentzia_materiala = 빼기(2); boolean BATDATOR = 맞는객체(objektu_Erreferentzia_materiala, izen_konstante);
                if (balio == 193) 넣기(objektu_Erreferentzia_materiala != 0 && BATDATOR ? 1 : 0, 1);
                else { if (!BATDATOR && !errorea) hutsegite_balio("ClassCastException"); 넣기(objektu_Erreferentzia_materiala, 2); }
                continue;
            }
            if (balio == 170 || balio == 171) {
                int 읽는자리 = Exekutatu_2 + 1, fitxategi_INDIZE = 틀함수[marko_INDIZE], gako_Erreferentzia_materiala = 빼기(1);
                while ((읽는자리 - 함수시작[fitxategi_INDIZE]) % 4 != 0) 읽는자리++;
                int helburu_helbide = kargu_osoko_zenbaki(읽는자리);
                if (balio == 170) { int 낮은값 = kargu_osoko_zenbaki(읽는자리 + 4), 높은값 = kargu_osoko_zenbaki(읽는자리 + 8); if (gako_Erreferentzia_materiala >= 낮은값 && gako_Erreferentzia_materiala <= 높은값) helburu_helbide = kargu_osoko_zenbaki(읽는자리 + 12 + (gako_Erreferentzia_materiala - 낮은값) * 4); }
                else { int 총수 = kargu_osoko_zenbaki(읽는자리 + 4); for (int Loop_INDIZE = 0; Loop_INDIZE < 총수; Loop_INDIZE++) if (kargu_osoko_zenbaki(읽는자리 + 8 + Loop_INDIZE * 8) == gako_Erreferentzia_materiala) helburu_helbide = kargu_osoko_zenbaki(읽는자리 + 12 + Loop_INDIZE * 8); }
                eraman_balio(Exekutatu_2 + helburu_helbide); continue;
            }
            if (balio == 200) { eraman_balio(Exekutatu_2 + kargu_osoko_zenbaki(Exekutatu_2 + 1)); continue; }
            if (balio == 194 || balio == 195) {
                int objektu_Erreferentzia_materiala = 빼기(2);
                if (balio == 195) 잠금풀기(objektu_Erreferentzia_materiala);
                else if (!잠금얻기(objektu_Erreferentzia_materiala) && !errorea) { 넣기(objektu_Erreferentzia_materiala, 2); marko_kargu[marko_INDIZE] = Exekutatu_2; }
                continue;
            }
            if (balio == 196) {
                int komando_KODE = 명바(), sarrera_kargu = 명짧();
                if (komando_KODE == 21 || komando_KODE == 25) 지역읽기(sarrera_kargu, komando_KODE == 21 ? 1 : 2);
                else if (komando_KODE == 54 || komando_KODE == 58) idatzi_lokal(sarrera_kargu, komando_KODE == 54 ? 1 : 2);
                else if (komando_KODE == 132) { int DELTA_balio = (short)명짧(); 지역읽기(sarrera_kargu, 1); 넣기(빼기(1) + DELTA_balio, 1); idatzi_lokal(sarrera_kargu, 1); }
                else hutsegite_balio("unsupported wide opcode");
                continue;
            }
            hutsegite_balio("unsupported bytecode");
        }
    }
    static int Bilatu_Gela_Definizioa(int Izena) {
        for (int Loop_INDIZE = 0; Loop_INDIZE < Gela_Definizioa_ZENBATU; Loop_INDIZE++) if (Gela_Definizioa_izen[Loop_INDIZE] != 0 && 같은말(Gela_Definizioa_izen[Loop_INDIZE], Izena)) return Loop_INDIZE;
        return karga_Gela_Definizioa(konstante_SMS(Izena));
    }
    static int karga_Gela_Definizioa(int izen_kate) {
        if (!objektu_balio(izen_kate, 1)) return -1;
        int luzera_balio = 힙[izen_kate + 1];
        if (luzera_balio < 1 || luzera_balio > 505 || Gela_Definizioa_ZENBATU == 16) { hutsegite_balio("class name/count limit"); return -1; }
        for (int Loop_INDIZE = 0; Loop_INDIZE < luzera_balio; Loop_INDIZE++) { int karaktere_kode = 힙[izen_kate + 2 + Loop_INDIZE]; fitxategi_izen_SMS[Loop_INDIZE] = karaktere_kode == '/' ? '.' : karaktere_kode; }
        fitxategi_izen_SMS[luzera_balio] = '.'; fitxategi_izen_SMS[luzera_balio + 1] = 'c'; fitxategi_izen_SMS[luzera_balio + 2] = 'l'; fitxategi_izen_SMS[luzera_balio + 3] = 'a'; fitxategi_izen_SMS[luzera_balio + 4] = 's'; fitxategi_izen_SMS[luzera_balio + 5] = 's'; fitxategi_izen_SMS[luzera_balio + 6] = 0;
        int Tamaina = erabiltzaile.파일읽기(fitxategi_izen_SMS, 임시파일);
        if (Tamaina < 0) { hutsegite_balio("ClassNotFoundException"); return -1; }
        int Gela_Definizioa = Gela_Definizioa_ZENBATU++; 종크기[Gela_Definizioa] = Tamaina;
        for (int Loop_INDIZE = 0; Loop_INDIZE < Tamaina; Loop_INDIZE++) Fitxategia[Gela_Definizioa * 16384 + Loop_INDIZE] = 임시파일[Loop_INDIZE];
        클래스읽기(Gela_Definizioa); if (errorea) return -1;
        int benetako_datuak = konstante_SMS(Gela_Definizioa_izen[Gela_Definizioa]);
        if (!글같음(benetako_datuak, izen_kate, true)) { hutsegite_balio("class name does not match file"); return -1; }
        int 부모 = 종부모[Gela_Definizioa];
        if (부모 != 0 && !Word_SMS(부모, "java/lang/Object") && !Word_SMS(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = Bilatu_Gela_Definizioa(부모);
            if (errorea || 위 < 0) return -1;
            int 읽는자리 = 위, fase_ZENBATU = 0;
            while (읽는자리 >= 0 && fase_ZENBATU++ < 16) {
                if (읽는자리 == Gela_Definizioa) { hutsegite_balio("cyclic inheritance"); return -1; }
                읽는자리 = 부모종(읽는자리);
            }
            int 시작변위 = 종칸수[위];
            for (int fitxategi_INDIZE = 0; fitxategi_INDIZE < 칸수; fitxategi_INDIZE++) if (칸주인[fitxategi_INDIZE] == Gela_Definizioa && (칸권한[fitxategi_INDIZE] & 8) == 0) 칸위치[fitxategi_INDIZE] += 시작변위;
            종칸수[Gela_Definizioa] += 시작변위;
        }
        return Gela_Definizioa;
    }
    static int 부모종(int Gela_Definizioa) {
        int Izena = 종부모[Gela_Definizioa];
        for (int Loop_INDIZE = 0; Loop_INDIZE < Gela_Definizioa_ZENBATU; Loop_INDIZE++) if (Izena != 0 && Gela_Definizioa_izen[Loop_INDIZE] != 0 && 같은말(Gela_Definizioa_izen[Loop_INDIZE], Izena)) return Loop_INDIZE;
        return -1;
    }
    static int 함수찾기(int Gela_Definizioa, int Izena, int formatu_balio) {
        for (int 깊이 = 0; Gela_Definizioa >= 0 && 깊이 < 16; 깊이++, Gela_Definizioa = 부모종(Gela_Definizioa)) {
            for (int Loop_INDIZE = 0; Loop_INDIZE < 함수수; Loop_INDIZE++) if (함수주인[Loop_INDIZE] == Gela_Definizioa && 같은말(함수명[Loop_INDIZE], Izena) && 같은말(함수형[Loop_INDIZE], formatu_balio)) return Loop_INDIZE;
        }
        return -1;
    }
    static int 이름함수(int Gela_Definizioa, String Izena, String formatu_balio) {
        for (int 깊이 = 0; Gela_Definizioa >= 0 && 깊이 < 16; 깊이++, Gela_Definizioa = 부모종(Gela_Definizioa))
            for (int Loop_INDIZE = 0; Loop_INDIZE < 함수수; Loop_INDIZE++) if (함수주인[Loop_INDIZE] == Gela_Definizioa && Word_SMS(함수명[Loop_INDIZE], Izena) && Word_SMS(함수형[Loop_INDIZE], formatu_balio)) return Loop_INDIZE;
        return -1;
    }
    static int 형종류(int Izena) { return Fitxategia[상가[Izena]] == 'L' || Fitxategia[상가[Izena]] == '[' ? 2 : 1; }
    static boolean hasieratu(int Gela_Definizioa, int komando_HASI) {
        if (Gela_Definizioa < 0 || errorea) return false;
        if (Gela_Definizioa_Egoera[Gela_Definizioa] == 3) { hutsegite_balio("NoClassDefFoundError: initialization failed"); return false; }
        if (Gela_Definizioa_Egoera[Gela_Definizioa] == 1 && Gela_hari[Gela_Definizioa] != 현재가닥) { marko_kargu[marko_INDIZE] = komando_HASI; aldatu_eskaera = true; return false; }
        if (Gela_Definizioa_Egoera[Gela_Definizioa] != 0) return true;
        int 위 = 부모종(Gela_Definizioa);
        if (위 >= 0 && !hasieratu(위, komando_HASI)) return false;
        Gela_Definizioa_Egoera[Gela_Definizioa] = 1; Gela_hari[Gela_Definizioa] = 현재가닥;
        if (hasieratu_Gela_Definizioa[Gela_Definizioa] != 0) {
            marko_kargu[marko_INDIZE] = komando_HASI;
            호출(hasieratu_Gela_Definizioa[Gela_Definizioa] - 1); if (!errorea) hasieratu_marko[marko_INDIZE] = Gela_Definizioa + 1;
            return false;
        }
        Gela_Definizioa_Egoera[Gela_Definizioa] = 2; return true;
    }
    static void 필드호출(int INDIZE, int Komandoa, int Exekutatu_2) {
        if (!txeke_konstante(INDIZE, 9)) return;
        int jabe_balio = klasearen_izen_SMS(상가[INDIZE]), Izena = Erreferentzia_materiala_izen(konstante_SEGUNDOA_balio[INDIZE]), formatu_balio = Erreferentzia_materiala_MOTA(konstante_SEGUNDOA_balio[INDIZE]);
        if (Word_SMS(jabe_balio, "java/lang/System") && (Word_SMS(Izena, "out") || Word_SMS(Izena, "err")) && Word_SMS(formatu_balio, "Ljava/io/PrintStream;") && Komandoa == 178) { 넣기(-1, 2); return; }
        int Gela_Definizioa = Bilatu_Gela_Definizioa(jabe_balio); if (Gela_Definizioa < 0 || errorea) return;
        int 찾음 = -1;
        for (int 읽는자리 = Gela_Definizioa, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = 부모종(읽는자리))
            for (int fitxategi_INDIZE = 0; fitxategi_INDIZE < 칸수; fitxategi_INDIZE++) if (칸주인[fitxategi_INDIZE] == 읽는자리 && 같은말(칸이름[fitxategi_INDIZE], Izena) && 같은말(칸형[fitxategi_INDIZE], formatu_balio)) 찾음 = fitxategi_INDIZE;
        if (찾음 < 0) { hutsegite_balio("NoSuchFieldError"); return; }
        boolean estatiko_balio = Komandoa == 178 || Komandoa == 179;
        if (estatiko_balio != ((칸권한[찾음] & 8) != 0)) { hutsegite_balio("field static/instance mismatch"); return; }
        if (estatiko_balio && !hasieratu(칸주인[찾음], Exekutatu_2)) return;
        int MOTA_balio = 형종류(formatu_balio), balio = 0;
        if (Komandoa == 179 || Komandoa == 181) balio = 빼기(MOTA_balio);
        if (estatiko_balio) { if (Komandoa == 178) 넣기(칸값[찾음], MOTA_balio); else if (!errorea) 칸값[찾음] = balio; return; }
        int objektu_Erreferentzia_materiala = 빼기(2);
        if (!객체유효(objektu_Erreferentzia_materiala)) return;
        if (힙[objektu_Erreferentzia_materiala] < 32 || !종포함(힙[objektu_Erreferentzia_materiala] - 32, jabe_balio)) { hutsegite_balio("field receiver type mismatch"); return; }
        int 보관칸 = objektu_Erreferentzia_materiala + 2 + 칸위치[찾음];
        if (Komandoa == 180) 넣기(힙[보관칸], MOTA_balio);
        else if (!errorea) { 힙[보관칸] = balio; 힙참조[보관칸] = MOTA_balio == 2 ? 1 : 0; }
    }
    static boolean 종포함(int Gela_Definizioa, int Izena) {
        for (int 중첩깊이 = 0; Gela_Definizioa >= 0 && 중첩깊이 < 16; 중첩깊이++, Gela_Definizioa = 부모종(Gela_Definizioa)) {
            if (같은말(Gela_Definizioa_izen[Gela_Definizioa], Izena) || (종부모[Gela_Definizioa] != 0 && 같은말(종부모[Gela_Definizioa], Izena))) return true;
            for (int barnekoa_kargu = 0; barnekoa_kargu < Gela_interfaze_ZENBATU[Gela_Definizioa]; barnekoa_kargu++) if (같은말(Gela_interfaze[Gela_Definizioa * 16 + barnekoa_kargu], Izena)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int byte_datuak, boolean Bide_izena) {
        if (첫값 == byte_datuak) return true;
        if (첫값 <= 0 || byte_datuak <= 0 || 힙[첫값] != 1 || 힙[byte_datuak] != 1 || 힙[첫값 + 1] != 힙[byte_datuak + 1]) return false;
        for (int Loop_INDIZE = 0; Loop_INDIZE < 힙[첫값 + 1]; Loop_INDIZE++) {
            int X_koordenatu = 힙[첫값 + 2 + Loop_INDIZE], Y_koordenatu = 힙[byte_datuak + 2 + Loop_INDIZE];
            if (Bide_izena) { if (X_koordenatu == '.') X_koordenatu = '/'; if (Y_koordenatu == '.') Y_koordenatu = '/'; }
            if (X_koordenatu != Y_koordenatu) return false;
        }
        return true;
    }
    static boolean 객체유효(int objektu_Erreferentzia_materiala) {
        if (objektu_Erreferentzia_materiala == 0) { hutsegite_balio("NullPointerException"); return false; }
        if (objektu_Erreferentzia_materiala < 1 || objektu_Erreferentzia_materiala >= 힙끝 || 힙폭[objektu_Erreferentzia_materiala] < 2 || 힙[objektu_Erreferentzia_materiala] == 0) { hutsegite_balio("invalid object reference"); return false; }
        return true;
    }
    static void babestu_balio(int objektu_Erreferentzia_materiala) {
        if (objektu_Erreferentzia_materiala > 0 && objektu_Erreferentzia_materiala < 힙끝 && 힙폭[objektu_Erreferentzia_materiala] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = objektu_Erreferentzia_materiala;
    }
    static void erakutsi_balio(int objektu_Erreferentzia_materiala) {
        if (objektu_Erreferentzia_materiala > 0 && objektu_Erreferentzia_materiala < 힙끝 && 힙폭[objektu_Erreferentzia_materiala] >= 2 && 힙[objektu_Erreferentzia_materiala] != 0 && 힙표시[objektu_Erreferentzia_materiala] == 0) {
            힙표시[objektu_Erreferentzia_materiala] = 1; 표시대기[pantaila_ZENBATU++] = objektu_Erreferentzia_materiala;
        }
    }
    static void 수거() {
        pantaila_ZENBATU = 0; Bilduma_ZENBATU++;
        for (int txeke_kargu = 1; txeke_kargu < 힙끝; txeke_kargu += 힙폭[txeke_kargu]) 힙표시[txeke_kargu] = 0;
        for (int Loop_INDIZE = 0; Loop_INDIZE < kate_Erreferentzia_materiala.length; Loop_INDIZE++) erakutsi_balio(kate_Erreferentzia_materiala[Loop_INDIZE]);
        for (int Loop_INDIZE = 0; Loop_INDIZE < 칸수; Loop_INDIZE++) if ((칸권한[Loop_INDIZE] & 8) != 0 && 형종류(칸형[Loop_INDIZE]) == 2) erakutsi_balio(칸값[Loop_INDIZE]);
        for (int 임시값 = 0; 임시값 < hari_ZENBATU; 임시값++) {
            erakutsi_balio(hari_objektu[임시값]); erakutsi_balio(hari_helburu[임시값]);
            int 꼭대기자리 = 임시값 == 현재가닥 ? marko_INDIZE : hari_marko[임시값];
            for (int fitxategi_INDIZE = 임시값 * 32; fitxategi_INDIZE <= 꼭대기자리; fitxategi_INDIZE++) {
                for (int barnekoa_kargu = 0; barnekoa_kargu < 함수지역[틀함수[fitxategi_INDIZE]]; barnekoa_kargu++) if (lokal_MOTA[fitxategi_INDIZE * 128 + barnekoa_kargu] == 2) erakutsi_balio(lokal_balio[fitxategi_INDIZE * 128 + barnekoa_kargu]);
                for (int barnekoa_kargu = 0; barnekoa_kargu < marko_pila[fitxategi_INDIZE]; barnekoa_kargu++) if (스택형[fitxategi_INDIZE * 128 + barnekoa_kargu] == 2) erakutsi_balio(스택값[fitxategi_INDIZE * 128 + barnekoa_kargu]);
            }
        }
        for (int Loop_INDIZE = 0; Loop_INDIZE < 화면참조.length; Loop_INDIZE++) erakutsi_balio(화면참조[Loop_INDIZE]);
        for (int Loop_INDIZE = 0; Loop_INDIZE < 나중수; Loop_INDIZE++) erakutsi_balio(나중실행[Loop_INDIZE]);
        for (int Loop_INDIZE = 0; Loop_INDIZE < Store_osoko_zenbaki.length; Loop_INDIZE++) erakutsi_balio(Store_osoko_zenbaki[Loop_INDIZE]);
        for (int Loop_INDIZE = 0; Loop_INDIZE < Gela_Definizioa_ZENBATU; Loop_INDIZE++) erakutsi_balio(종잠금[Loop_INDIZE]);
        for (int txeke_kargu = 1; txeke_kargu < 힙끝; txeke_kargu += 힙폭[txeke_kargu]) if (잠금깊이[txeke_kargu] > 0) erakutsi_balio(txeke_kargu);
        erakutsi_balio(던진객체);
        for (int Loop_INDIZE = 0; Loop_INDIZE < 잠시수; Loop_INDIZE++) erakutsi_balio(잠시참조[Loop_INDIZE]);
        while (pantaila_ZENBATU > 0) {
            int objektu_Erreferentzia_materiala = 표시대기[--pantaila_ZENBATU], Kategoria_KODE = 힙[objektu_Erreferentzia_materiala];
            for (int Loop_INDIZE = objektu_Erreferentzia_materiala + 2; Loop_INDIZE < objektu_Erreferentzia_materiala + 힙폭[objektu_Erreferentzia_materiala]; Loop_INDIZE++) if (Kategoria_KODE == 3 || Kategoria_KODE == 4 || 힙참조[Loop_INDIZE] != 0) erakutsi_balio(힙[Loop_INDIZE]);
        }
        for (int txeke_kargu = 1; txeke_kargu < 힙끝; txeke_kargu += 힙폭[txeke_kargu]) if (힙표시[txeke_kargu] == 0) 힙[txeke_kargu] = 0;
        for (int txeke_kargu = 1; txeke_kargu < 힙끝; txeke_kargu += 힙폭[txeke_kargu]) if (힙[txeke_kargu] == 0) {
            while (txeke_kargu + 힙폭[txeke_kargu] < 힙끝 && 힙[txeke_kargu + 힙폭[txeke_kargu]] == 0) { int Hurrengoa_kargu = txeke_kargu + 힙폭[txeke_kargu]; 힙폭[txeke_kargu] += 힙폭[Hurrengoa_kargu]; 힙폭[Hurrengoa_kargu] = 0; }
            if (txeke_kargu + 힙폭[txeke_kargu] == 힙끝) { 힙끝 = txeke_kargu; break; }
        }
    }
    static int 새기억(int 종류, int luzera_balio) {
        if (luzera_balio < 0) { hutsegite_balio("NegativeArraySizeException"); return 0; }
        if (luzera_balio > 힙.length - 3) { hutsegite_balio("object heap exhausted"); return 0; }
        int 필요수 = luzera_balio + 2, objektu_Erreferentzia_materiala = 0;
        if (필요수 <= 힙.length - 힙끝) { objektu_Erreferentzia_materiala = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { objektu_Erreferentzia_materiala = 읽는자리; break; }
            if (objektu_Erreferentzia_materiala != 0) {
                int 남은길이 = 힙폭[objektu_Erreferentzia_materiala] - 필요수;
                if (남은길이 >= 2) { 힙폭[objektu_Erreferentzia_materiala + 필요수] = 남은길이; 힙[objektu_Erreferentzia_materiala + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { objektu_Erreferentzia_materiala = 힙끝; 힙끝 += 필요수; }
        }
        if (objektu_Erreferentzia_materiala == 0) { hutsegite_balio("object heap exhausted"); return 0; }
        for (int Loop_INDIZE = 0; Loop_INDIZE < 필요수; Loop_INDIZE++) { 힙[objektu_Erreferentzia_materiala + Loop_INDIZE] = 0; 힙참조[objektu_Erreferentzia_materiala + Loop_INDIZE] = 0; 힙폭[objektu_Erreferentzia_materiala + Loop_INDIZE] = 0; }
        matrize_elementu[objektu_Erreferentzia_materiala] = 0;
        힙폭[objektu_Erreferentzia_materiala] = 필요수; 힙[objektu_Erreferentzia_materiala] = 종류; 힙[objektu_Erreferentzia_materiala + 1] = luzera_balio; babestu_balio(objektu_Erreferentzia_materiala); return objektu_Erreferentzia_materiala;
    }
    static int salbuespen_Gela(String izen_konstante) {
        if (자바도구.같음(izen_konstante, "java/lang/Throwable")) return 1;
        if (자바도구.같음(izen_konstante, "java/lang/Exception")) return 2;
        if (자바도구.같음(izen_konstante, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(izen_konstante, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(izen_konstante, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(izen_konstante, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(izen_konstante, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(izen_konstante, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(izen_konstante, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(izen_konstante, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(izen_konstante, "java/io/IOException")) return 11;
        if (자바도구.같음(izen_konstante, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(izen_konstante, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(izen_konstante, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(izen_konstante, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int salbuespen_konstante(int Izena) {
        for (int Loop_INDIZE = 1; Loop_INDIZE <= 41; Loop_INDIZE++) if (Word_SMS(Izena, salbuespen_izen(Loop_INDIZE))) return Loop_INDIZE;
        return 0;
    }
    static String salbuespen_izen(int kontu_balio) {
        if (kontu_balio == 40) return "java/lang/InterruptedException";
        if (kontu_balio == 41) return "Euskara/자체/대기중단예외";
        if (kontu_balio == 39) return "java/net/SocketException";
        if (kontu_balio == 20) return "Euskara/자체/salbuespen";
        if (kontu_balio == 21) return "Euskara/자체/실행예외";
        if (kontu_balio == 22) return "Euskara/자체/S_I_salbuespen";
        if (kontu_balio == 23) return "Euskara/자체/itxaron_DENBORA_MUGA_salbuespen";
        if (kontu_balio == 24) return "Euskara/자체/helbide_BEGIRATU_salbuespen";
        if (kontu_balio == 25) return "Euskara/자체/파일없음예외";
        if (kontu_balio == 26) return "Euskara/자체/통신예외";
        if (kontu_balio == 27) return "Euskara/자체/baliogabe_arg_salbuespen";
        if (kontu_balio == 28) return "Euskara/자체/숫자형식예외";
        if (kontu_balio == 29) return "Euskara/자체/범위예외";
        if (kontu_balio == 30) return "Euskara/자체/배열범위예외";
        if (kontu_balio == 31) return "Euskara/자체/문자열범위예외";
        if (kontu_balio == 32) return "Euskara/자체/nulu_Erreferentzia_materiala_salbuespen";
        if (kontu_balio == 33) return "Euskara/자체/산술예외";
        if (kontu_balio == 34) return "Euskara/자체/Egoera_salbuespen";
        if (kontu_balio == 35) return "Euskara/자체/MOTA_igorri_salbuespen";
        if (kontu_balio == 36) return "Euskara/자체/음수배열크기예외";
        if (kontu_balio == 37) return "Euskara/자체/matrize_Store_hutsegite";
        if (kontu_balio == 38) return "Euskara/자체/hari_Egoera_salbuespen";
        if (kontu_balio == 1) return "java/lang/Throwable"; if (kontu_balio == 2) return "java/lang/Exception";
        if (kontu_balio == 3) return "java/lang/RuntimeException"; if (kontu_balio == 4) return "java/lang/ArithmeticException";
        if (kontu_balio == 5) return "java/lang/NullPointerException"; if (kontu_balio == 6) return "java/lang/IndexOutOfBoundsException";
        if (kontu_balio == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (kontu_balio == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (kontu_balio == 9) return "java/lang/IllegalArgumentException"; if (kontu_balio == 10) return "java/lang/NumberFormatException";
        if (kontu_balio == 11) return "java/io/IOException"; if (kontu_balio == 12) return "java/io/FileNotFoundException";
        if (kontu_balio == 17) return "java/lang/ArrayStoreException";
        if (kontu_balio == 18) return "java/net/UnknownHostException";
        if (kontu_balio == 19) return "java/net/SocketTimeoutException";
        if (kontu_balio == 16) return "java/lang/IllegalThreadStateException";
        if (kontu_balio == 13) return "java/lang/IllegalStateException"; if (kontu_balio == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int kontu_balio) {
        if (kontu_balio == 40) return 2;
        if (kontu_balio == 41) return 40;
        if (kontu_balio == 39) return 11;
        if (kontu_balio == 1) return 0;
        if (kontu_balio == 2) return 1;
        if (kontu_balio == 3) return 2;
        if (kontu_balio == 4) return 3;
        if (kontu_balio == 5) return 3;
        if (kontu_balio == 6) return 3;
        if (kontu_balio == 7) return 6;
        if (kontu_balio == 8) return 6;
        if (kontu_balio == 9) return 3;
        if (kontu_balio == 10) return 9;
        if (kontu_balio == 11) return 2;
        if (kontu_balio == 12) return 11;
        if (kontu_balio == 13) return 3;
        if (kontu_balio == 14) return 3;
        if (kontu_balio == 15) return 3;
        if (kontu_balio == 16) return 9;
        if (kontu_balio == 17) return 3;
        if (kontu_balio == 18) return 11;
        if (kontu_balio == 19) return 11;
        if (kontu_balio == 20) return 2;
        if (kontu_balio == 21) return 3;
        if (kontu_balio == 22) return 11;
        if (kontu_balio == 23) return 22;
        if (kontu_balio == 24) return 22;
        if (kontu_balio == 25) return 22;
        if (kontu_balio == 26) return 22;
        if (kontu_balio == 27) return 9;
        if (kontu_balio == 28) return 27;
        if (kontu_balio == 29) return 6;
        if (kontu_balio == 30) return 29;
        if (kontu_balio == 31) return 29;
        if (kontu_balio == 32) return 5;
        if (kontu_balio == 33) return 4;
        if (kontu_balio == 34) return 13;
        if (kontu_balio == 35) return 14;
        if (kontu_balio == 36) return 15;
        if (kontu_balio == 37) return 17;
        if (kontu_balio == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int benetako_balio, int 요구값) {
        for (int 깊이 = 0; benetako_balio != 0 && 깊이 < 16; 깊이++, benetako_balio = 예외부모(benetako_balio))
            if (benetako_balio == 요구값) return true;
        return false;
    }
    static void 예외던짐(int kontu_balio, String IRAKHAU_Erreferentzia_materiala) {
        int objektu_Erreferentzia_materiala = 새기억(9, 2); if (errorea) return;
        힙[objektu_Erreferentzia_materiala + 2] = kontu_balio; 힙[objektu_Erreferentzia_materiala + 3] = Ostalari_karaktere(IRAKHAU_Erreferentzia_materiala); 힙참조[objektu_Erreferentzia_materiala + 3] = 1;
        던진객체 = objektu_Erreferentzia_materiala; errorea = true;
    }
    static boolean 맞는객체(int objektu_Erreferentzia_materiala, int Izena) {
        if (objektu_Erreferentzia_materiala == 0) return true;
        if (!객체유효(objektu_Erreferentzia_materiala)) return false;
        int Kategoria_KODE = 힙[objektu_Erreferentzia_materiala];
        if (Word_SMS(Izena, "java/lang/Object")) return true;
        if (Kategoria_KODE >= 32) return 종포함(Kategoria_KODE - 32, Izena);
        if (Kategoria_KODE == 9) { int helburu_helbide = salbuespen_konstante(Izena); return helburu_helbide != 0 && 예외포함(힙[objektu_Erreferentzia_materiala + 2], helburu_helbide); }
        if (Kategoria_KODE == 1) return Word_SMS(Izena, "java/lang/String") || Word_SMS(Izena, "java/lang/CharSequence");
        if (Kategoria_KODE == 4) return Word_SMS(Izena, "java/lang/StringBuilder") || Word_SMS(Izena, "java/lang/CharSequence");
        if (Kategoria_KODE == 10) return Word_SMS(Izena, "java/util/ArrayList") || Word_SMS(Izena, "java/util/List");
        if (Kategoria_KODE == 11) return Word_SMS(Izena, "java/util/HashMap") || Word_SMS(Izena, "java/util/Map");
        if (Kategoria_KODE == 12) return Word_SMS(Izena, "java/lang/Integer") || Word_SMS(Izena, "java/lang/Number");
        if (Kategoria_KODE >= 24 && Kategoria_KODE <= 28 && 힙[objektu_Erreferentzia_materiala + 13] != 0) return 한국어화면종(Izena) == Kategoria_KODE || Word_SMS(Izena, "Euskara/자체/화면구성요소");
        if (Kategoria_KODE >= 24 && Kategoria_KODE <= 28) return (한국어화면종(Izena) == 0 && 화면종(Izena) == Kategoria_KODE) || Word_SMS(Izena, "java/awt/Component") || Word_SMS(Izena, "java/awt/Container") || Word_SMS(Izena, "javax/swing/JComponent");
        if (Kategoria_KODE == 29) return Word_SMS(Izena, 힙[objektu_Erreferentzia_materiala + 3] != 0 ? "Euskara/자체/동작알림" : "java/awt/event/ActionEvent");
        if (Kategoria_KODE == 30) return Word_SMS(Izena, "java/awt/FlowLayout") || Word_SMS(Izena, "java/awt/LayoutManager");
        if (Kategoria_KODE == 17) return Word_SMS(Izena, "java/net/Socket");
        if (Kategoria_KODE == 18) return Word_SMS(Izena, "java/net/ServerSocket");
        if (Kategoria_KODE == 19) return Word_SMS(Izena, 힙[objektu_Erreferentzia_materiala + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (Kategoria_KODE == 14) return Word_SMS(Izena, "java/net/InetAddress");
        if (Kategoria_KODE == 15) return Word_SMS(Izena, "java/net/DatagramSocket");
        if (Kategoria_KODE == 16) return Word_SMS(Izena, "java/net/DatagramPacket");
        if (Kategoria_KODE == 13) return Word_SMS(Izena, 힙[objektu_Erreferentzia_materiala + 3] != 0 ? "Euskara/자체/작업가닥" : "java/lang/Thread");
        if (Kategoria_KODE == 2) return Word_SMS(Izena, "[I"); if (Kategoria_KODE == 20) return Word_SMS(Izena, "[B"); if (Kategoria_KODE == 21) return Word_SMS(Izena, "[Z");
        if (Kategoria_KODE == 22) return Word_SMS(Izena, "[C"); if (Kategoria_KODE == 23) return Word_SMS(Izena, "[S");
        if (Kategoria_KODE != 3) return false;
        if (Word_SMS(Izena, "[Ljava/lang/Object;")) return true;
        int osagai = matrize_elementu[objektu_Erreferentzia_materiala];
        if (osagai == -1) return Word_SMS(Izena, "[Ljava/lang/String;") || Word_SMS(Izena, "[Ljava/lang/CharSequence;");
        if (osagai == 0) return false;
        if (배열종비교(osagai, Izena)) return true;
        if ((Word_SMS(osagai, "java/lang/String") || Word_SMS(osagai, "java/lang/StringBuilder")) && Word_SMS(Izena, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDIZE = 0; Loop_INDIZE < Gela_Definizioa_ZENBATU; Loop_INDIZE++) if (같은말(Gela_Definizioa_izen[Loop_INDIZE], osagai)) {
            for (int karaktere_kode = Loop_INDIZE, 중첩깊이 = 0; karaktere_kode >= 0 && 중첩깊이 < 16; 중첩깊이++, karaktere_kode = 부모종(karaktere_kode)) {
                if (배열종비교(종부모[karaktere_kode], Izena)) return true;
                for (int barnekoa_kargu = 0; barnekoa_kargu < Gela_interfaze_ZENBATU[karaktere_kode]; barnekoa_kargu++) if (배열종비교(Gela_interfaze[karaktere_kode * 16 + barnekoa_kargu], Izena)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int izen_konstante, int 형식참조) {
        int txeke_kargu = 상가[형식참조], sarrera_ZENBATU = konstante_SEGUNDOA_balio[형식참조];
        if (izen_konstante == 0 || sarrera_ZENBATU < 4 || Fitxategia[txeke_kargu] != '[' || Fitxategia[txeke_kargu + 1] != 'L' || Fitxategia[txeke_kargu + sarrera_ZENBATU - 1] != ';' || konstante_SEGUNDOA_balio[izen_konstante] != sarrera_ZENBATU - 3) return false;
        for (int Loop_INDIZE = 0; Loop_INDIZE < sarrera_ZENBATU - 3; Loop_INDIZE++) if (Fitxategia[상가[izen_konstante] + Loop_INDIZE] != Fitxategia[txeke_kargu + 2 + Loop_INDIZE]) return false;
        return true;
    }
    static void helduleku_salbuespen() {
        if (던진객체 == 0) return;
        errorea = false;
        while (marko_INDIZE >= 현재가닥 * 32) {
            int fitxategi_INDIZE = 틀함수[marko_INDIZE], 읽는자리 = marko_instrukzio[marko_INDIZE];
            for (int Loop_INDIZE = 0; Loop_INDIZE < 잡기수; Loop_INDIZE++) if (잡기함수[Loop_INDIZE] == fitxategi_INDIZE && 읽는자리 >= 잡기시작[Loop_INDIZE] && 읽는자리 < 잡기끝[Loop_INDIZE]
                && (잡기종[Loop_INDIZE] == 0 || 맞는객체(던진객체, 잡기종[Loop_INDIZE]))) {
                marko_kargu[marko_INDIZE] = 잡기위치[Loop_INDIZE]; marko_pila[marko_INDIZE] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (hasieratu_marko[marko_INDIZE] != 0) Gela_Definizioa_Egoera[hasieratu_marko[marko_INDIZE] - 1] = 3;
            if (틀잠금[marko_INDIZE] != 0) { 잠금풀기(틀잠금[marko_INDIZE]); 틀잠금[marko_INDIZE] = 0; }
            marko_INDIZE--;
        }
        erabiltzaile.Idatzi("Uncaught ");
        if (힙[던진객체] == 9) { erabiltzaile.Idatzi(salbuespen_izen(힙[던진객체 + 2])); erabiltzaile.Idatzi(": "); idatzi_SMS(힙[던진객체 + 3]); }
        else erabiltzaile.Idatzi("user exception");
        erabiltzaile.idatzi_karaktere_balio(10); 던진객체 = 0; errorea = true;
    }
    // 이 JVM의 스택 항목은 현재 category-1(int/reference)만 허용한다.
    static void pila_instrukzio(int komando_KODE) {
        int 첫값 = 빼기(0), 첫형식 = itzuli_MOTA;
        if (komando_KODE == 87) return;
        if (komando_KODE == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int byte_datuak = 빼기(0), SEGUNDOA_formatu = itzuli_MOTA;
        if (komando_KODE == 88) return;
        if (komando_KODE == 90) { 넣기(첫값, 첫형식); 넣기(byte_datuak, SEGUNDOA_formatu); 넣기(첫값, 첫형식); return; }
        if (komando_KODE == 92) { 넣기(byte_datuak, SEGUNDOA_formatu); 넣기(첫값, 첫형식); 넣기(byte_datuak, SEGUNDOA_formatu); 넣기(첫값, 첫형식); return; }
        if (komando_KODE == 95) { 넣기(첫값, 첫형식); 넣기(byte_datuak, SEGUNDOA_formatu); return; }
        int karaktere_kode = 빼기(0), 셋째형식 = itzuli_MOTA;
        if (komando_KODE == 91) { 넣기(첫값, 첫형식); 넣기(karaktere_kode, 셋째형식); 넣기(byte_datuak, SEGUNDOA_formatu); 넣기(첫값, 첫형식); return; }
        if (komando_KODE == 93) { 넣기(byte_datuak, SEGUNDOA_formatu); 넣기(첫값, 첫형식); 넣기(karaktere_kode, 셋째형식); 넣기(byte_datuak, SEGUNDOA_formatu); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = itzuli_MOTA;
        넣기(byte_datuak, SEGUNDOA_formatu); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(karaktere_kode, 셋째형식); 넣기(byte_datuak, SEGUNDOA_formatu); 넣기(첫값, 첫형식);
    }
    static void 새객체(int izen_konstante, int 시작점) {
        int Kategoria_KODE = 0, 유효길이 = 0, salbuespen_Erreferentzia_materiala = salbuespen_konstante(izen_konstante);
        if (Word_SMS(izen_konstante, "java/lang/StringBuilder")) { Kategoria_KODE = 4; 유효길이 = 1; }
        if (Word_SMS(izen_konstante, "java/io/FileInputStream")) { Kategoria_KODE = 5; 유효길이 = 2; }
        if (Word_SMS(izen_konstante, "java/io/FileOutputStream")) { Kategoria_KODE = 6; 유효길이 = 2; }
        if (salbuespen_Erreferentzia_materiala != 0) { Kategoria_KODE = 9; 유효길이 = 2; }
        if (Word_SMS(izen_konstante, "java/util/ArrayList")) { Kategoria_KODE = 10; 유효길이 = 2; }
        if (Word_SMS(izen_konstante, "java/util/HashMap")) { Kategoria_KODE = 11; 유효길이 = 2; }
        if (Word_SMS(izen_konstante, "java/lang/Integer")) { Kategoria_KODE = 12; 유효길이 = 1; }
        if (Word_SMS(izen_konstante, "java/net/Socket")) { Kategoria_KODE = 17; 유효길이 = 5; }
        if (Word_SMS(izen_konstante, "java/net/ServerSocket")) { Kategoria_KODE = 18; 유효길이 = 5; }
        if (Word_SMS(izen_konstante, "java/net/DatagramSocket")) { Kategoria_KODE = 15; 유효길이 = 3; }
        if (Word_SMS(izen_konstante, "java/net/DatagramPacket")) { Kategoria_KODE = 16; 유효길이 = 4; }
        if (Word_SMS(izen_konstante, "java/lang/Thread") || Word_SMS(izen_konstante, "Euskara/자체/작업가닥")) { Kategoria_KODE = 13; 유효길이 = 2; }
        if (Word_SMS(izen_konstante, "java/lang/Object")) { Kategoria_KODE = 8; }
        if (Kategoria_KODE == 0 && 화면종(izen_konstante) != 0) { Kategoria_KODE = 화면종(izen_konstante); 유효길이 = 12; }
        if (Kategoria_KODE == 0) {
            int karaktere_kode = Bilatu_Gela_Definizioa(izen_konstante); if (karaktere_kode < 0 || errorea || !hasieratu(karaktere_kode, 시작점)) return;
            Kategoria_KODE = 32 + karaktere_kode; 유효길이 = 종칸수[karaktere_kode];
        }
        int objektu_Erreferentzia_materiala = esleitu_biltegi(Kategoria_KODE, 유효길이); if (errorea) return;
        if (Kategoria_KODE == 13 && Word_SMS(izen_konstante, "Euskara/자체/작업가닥")) 힙[objektu_Erreferentzia_materiala + 3] = 1;
        if (Kategoria_KODE >= 24 && Kategoria_KODE <= 28 && 한국어화면종(izen_konstante) != 0) 힙[objektu_Erreferentzia_materiala + 13] = 1;
        if (Kategoria_KODE == 5 || Kategoria_KODE == 6 || Kategoria_KODE == 15 || Kategoria_KODE == 17 || Kategoria_KODE == 18) 힙[objektu_Erreferentzia_materiala + 2] = -1;
        if (Kategoria_KODE == 9) 힙[objektu_Erreferentzia_materiala + 2] = salbuespen_Erreferentzia_materiala;
        넣기(objektu_Erreferentzia_materiala, 2);
    }
    static boolean 값같음(int 첫값, int byte_datuak) {
        if (첫값 == byte_datuak) return true;
        if (첫값 == 0 || byte_datuak == 0 || 첫값 < 0 || byte_datuak < 0 || 첫값 >= 힙끝 || byte_datuak >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[byte_datuak] == 1) return 글같음(첫값, byte_datuak, false);
        return 힙[첫값] == 12 && 힙[byte_datuak] == 12 && 힙[첫값 + 2] == 힙[byte_datuak + 2];
    }
    static int 글조각(int objektu_Erreferentzia_materiala, int HASI_kargu, int amaitu_kargu) {
        if (!objektu_balio(objektu_Erreferentzia_materiala, 1)) return 0;
        if (HASI_kargu < 0 || amaitu_kargu < HASI_kargu || amaitu_kargu > 힙[objektu_Erreferentzia_materiala + 1]) { hutsegite_balio("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = esleitu_biltegi(1, amaitu_kargu - HASI_kargu); if (errorea) return 0;
        for (int Loop_INDIZE = HASI_kargu; Loop_INDIZE < amaitu_kargu; Loop_INDIZE++) 힙[반환값 + 2 + Loop_INDIZE - HASI_kargu] = 힙[objektu_Erreferentzia_materiala + 2 + Loop_INDIZE];
        return 반환값;
    }
    static int sartu_SMS(int 첫값, int byte_datuak) {
        if (!objektu_balio(첫값, 1) || !objektu_balio(byte_datuak, 1)) return 0;
        int sarrera_ZENBATU = 힙[첫값 + 1], 함수번호 = 힙[byte_datuak + 1], 반환값 = esleitu_biltegi(1, sarrera_ZENBATU + 함수번호); if (errorea) return 0;
        for (int Loop_INDIZE = 0; Loop_INDIZE < sarrera_ZENBATU; Loop_INDIZE++) 힙[반환값 + 2 + Loop_INDIZE] = 힙[첫값 + 2 + Loop_INDIZE];
        for (int Loop_INDIZE = 0; Loop_INDIZE < 함수번호; Loop_INDIZE++) 힙[반환값 + 2 + sarrera_ZENBATU + Loop_INDIZE] = 힙[byte_datuak + 2 + Loop_INDIZE];
        return 반환값;
    }
    static boolean 기본호출(int jabe, int izen_konstante, int 서술상수, int komando_KODE) {
        if (Word_SMS(jabe, "Euskara/자체/실행인수") && komando_KODE == 184) {
            if (Word_SMS(izen_konstante, "elementu_ZENBATU") && Word_SMS(서술상수, "()I")) { 넣기(erabiltzaile.인수개수() - 1, 1); return true; }
            if (Word_SMS(izen_konstante, "Testua") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= erabiltzaile.인수개수() - 1) 예외던짐(29, "exekutatu_komando Argumentuak 범위를 벗어났습니다");
                else 넣기(Ostalari_karaktere(erabiltzaile.Argumentuak(순번 + 1)), 2);
                return true;
            }
            hutsegite_balio("지원하지 않는 Euskara exekutatu_komando Argumentuak 호출"); return true;
        }
        if (Word_SMS(jabe, "Euskara/자체/작업가닥")) { prozesu_hari(izen_konstante, 서술상수, komando_KODE, true); return true; }
        if (한국어화면소유(jabe)) { 한국어화면호출(jabe, izen_konstante, 서술상수, komando_KODE); return true; }
        if (화면소유(jabe)) { 화면호출(jabe, izen_konstante, 서술상수, komando_KODE); return true; }
        if (Word_SMS(jabe, "java/net/Socket") || Word_SMS(jabe, "java/net/ServerSocket") || Word_SMS(jabe, "java/io/InputStream") || Word_SMS(jabe, "java/io/OutputStream")) { 흐름호출(jabe, izen_konstante, 서술상수, komando_KODE); return true; }
        if (Word_SMS(jabe, "Euskara/자체/nukleo_balio") && komando_KODE == 184) {
            if (Word_SMS(izen_konstante, "화면너비") && Word_SMS(서술상수, "()I")) { 넣기(erabiltzaile.화면너비(), 1); return true; }
            if (Word_SMS(izen_konstante, "화면높이") && Word_SMS(서술상수, "()I")) { 넣기(erabiltzaile.화면높이(), 1); return true; }
            if (Word_SMS(izen_konstante, "밀리초") && Word_SMS(서술상수, "()I")) { 넣기(erabiltzaile.밀리초(), 1); return true; }
            if (Word_SMS(izen_konstante, "그림대기") && Word_SMS(서술상수, "()I")) { 넣기(erabiltzaile.그림대기(), 1); return true; }
            if (Word_SMS(izen_konstante, "사각형") && Word_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), Y_koordenatu = 빼기(1), X_koordenatu = 빼기(1); 넣기(erabiltzaile.사각형(X_koordenatu, Y_koordenatu, 너비, 높이, 색상), 1); return true; }
        }
        if (Word_SMS(jabe, "java/net/InetAddress") || Word_SMS(jabe, "java/net/DatagramPacket") || Word_SMS(jabe, "java/net/DatagramSocket")) { 통신호출(jabe, izen_konstante, 서술상수, komando_KODE); return true; }
        if (Word_SMS(jabe, "java/lang/Thread")) { 가닥호출(izen_konstante, 서술상수, komando_KODE); return true; }
        if (Word_SMS(jabe, "java/lang/Object")) {
            if (Word_SMS(izen_konstante, "<init>") && Word_SMS(서술상수, "()V") && komando_KODE == 183) { 객체유효(빼기(2)); return true; }
            if (Word_SMS(izen_konstante, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int byte_datuak = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == byte_datuak ? 1 : 0, 1); return true; }
        }
        if (salbuespen_konstante(jabe) != 0) {
            if (Word_SMS(izen_konstante, "<init>") && komando_KODE == 183 && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int eskatu = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), objektu_Erreferentzia_materiala = 빼기(2);
                if (objektu_balio(objektu_Erreferentzia_materiala, 9)) { 힙[objektu_Erreferentzia_materiala + 3] = eskatu; 힙참조[objektu_Erreferentzia_materiala + 3] = 1; } return true;
            }
            if ((Word_SMS(izen_konstante, "getMessage") || Word_SMS(izen_konstante, "설명")) && Word_SMS(서술상수, "()Ljava/lang/String;")) { int objektu_Erreferentzia_materiala = 빼기(2); if (objektu_balio(objektu_Erreferentzia_materiala, 9)) 넣기(힙[objektu_Erreferentzia_materiala + 3], 2); return true; }
        }
        if (Word_SMS(jabe, "java/lang/String")) {
            if (komando_KODE == 182 && Word_SMS(izen_konstante, "getBytes") && (Word_SMS(서술상수, "()[B") || Word_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int kodeketa_izen = Word_SMS(서술상수, "()[B") ? 0 : 빼기(2), objektu_Erreferentzia_materiala = 빼기(2);
                if (!objektu_balio(objektu_Erreferentzia_materiala, 1)) return true;
                if (kodeketa_izen != 0 && !글같음(kodeketa_izen, Ostalari_karaktere("UTF-8"), false) && !글같음(kodeketa_izen, Ostalari_karaktere("UTF8"), false) && !글같음(kodeketa_izen, Ostalari_karaktere("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int sarrera_ZENBATU = 힙[objektu_Erreferentzia_materiala + 1], 반환값 = esleitu_biltegi(20, sarrera_ZENBATU * 3), 사용수 = 0; if (errorea) return true;
                for (int barnekoa_kargu = 0; barnekoa_kargu < sarrera_ZENBATU; barnekoa_kargu++) {
                    int karaktere_kode = 힙[objektu_Erreferentzia_materiala + 2 + barnekoa_kargu];
                    if (karaktere_kode >= 0xd800 && karaktere_kode <= 0xdbff && barnekoa_kargu + 1 < sarrera_ZENBATU && 힙[objektu_Erreferentzia_materiala + 3 + barnekoa_kargu] >= 0xdc00 && 힙[objektu_Erreferentzia_materiala + 3 + barnekoa_kargu] <= 0xdfff) karaktere_kode = 0x10000 + ((karaktere_kode - 0xd800) << 10) + 힙[objektu_Erreferentzia_materiala + 2 + ++barnekoa_kargu] - 0xdc00;
                    else if (karaktere_kode >= 0xd800 && karaktere_kode <= 0xdfff) karaktere_kode = '?';
                    if (karaktere_kode < 128) 힙[반환값 + 2 + 사용수++] = karaktere_kode;
                    else { int byte_ZENBATU = karaktere_kode < 2048 ? 2 : karaktere_kode < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((byte_ZENBATU == 2 ? 192 : byte_ZENBATU == 3 ? 224 : 240) | karaktere_kode >> (6 * (byte_ZENBATU - 1))); for (int Konparazioa_kargu = byte_ZENBATU - 1; Konparazioa_kargu > 0; Konparazioa_kargu--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | karaktere_kode >> (6 * (Konparazioa_kargu - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (komando_KODE == 184 && Word_SMS(izen_konstante, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(digitu_karaktere(빼기(1)), 2); return true; }
            if (komando_KODE != 182) return false;
            if (Word_SMS(izen_konstante, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int byte_datuak = 빼기(2), 첫값 = 빼기(2); if (objektu_balio(첫값, 1)) 넣기(글같음(첫값, byte_datuak, false) ? 1 : 0, 1); return true; }
            if (Word_SMS(izen_konstante, "isEmpty") && Word_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (objektu_balio(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_SMS(izen_konstante, "substring") && (Word_SMS(서술상수, "(I)Ljava/lang/String;") || Word_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SEGUNDOA_balio = Word_SMS(서술상수, "(II)Ljava/lang/String;"); int amaitu_kargu = SEGUNDOA_balio ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (objektu_balio(첫값, 1)) 넣기(글조각(첫값, 시작점, SEGUNDOA_balio ? amaitu_kargu : 힙[첫값 + 1]), 2); return true;
            }
            if (Word_SMS(izen_konstante, "concat") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int byte_datuak = 빼기(2), 첫값 = 빼기(2); 넣기(sartu_SMS(첫값, byte_datuak), 2); return true; }
            if (Word_SMS(izen_konstante, "hashCode") && Word_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), hash_balio = 0; if (objektu_balio(첫값, 1)) { for (int Loop_INDIZE = 0; Loop_INDIZE < 힙[첫값 + 1]; Loop_INDIZE++) hash_balio = hash_balio * 31 + 힙[첫값 + 2 + Loop_INDIZE]; 넣기(hash_balio, 1); } return true; }
            if (Word_SMS(izen_konstante, "toString") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (objektu_balio(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_SMS(jabe, "java/lang/Integer")) {
            if (komando_KODE == 184 && Word_SMS(izen_konstante, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int datuak_balio = 빼기(1), objektu_Erreferentzia_materiala = datuak_balio >= -128 && datuak_balio <= 127 ? Store_osoko_zenbaki[datuak_balio + 128] : 0; if (objektu_Erreferentzia_materiala == 0) { objektu_Erreferentzia_materiala = esleitu_biltegi(12, 1); if (!errorea) { 힙[objektu_Erreferentzia_materiala + 2] = datuak_balio; if (datuak_balio >= -128 && datuak_balio <= 127) Store_osoko_zenbaki[datuak_balio + 128] = objektu_Erreferentzia_materiala; } } 넣기(objektu_Erreferentzia_materiala, 2); return true; }
            if (komando_KODE == 183 && Word_SMS(izen_konstante, "<init>") && Word_SMS(서술상수, "(I)V")) { int datuak_balio = 빼기(1), objektu_Erreferentzia_materiala = 빼기(2); if (objektu_balio(objektu_Erreferentzia_materiala, 12)) 힙[objektu_Erreferentzia_materiala + 2] = datuak_balio; return true; }
            if (komando_KODE == 182 && Word_SMS(izen_konstante, "intValue") && Word_SMS(서술상수, "()I")) { int objektu_Erreferentzia_materiala = 빼기(2); if (objektu_balio(objektu_Erreferentzia_materiala, 12)) 넣기(힙[objektu_Erreferentzia_materiala + 2], 1); return true; }
            if (komando_KODE == 184 && Word_SMS(izen_konstante, "toString") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(digitu_karaktere(빼기(1)), 2); return true; }
        }
        if (Word_SMS(jabe, "java/lang/Math") && komando_KODE == 184) {
            if (Word_SMS(izen_konstante, "abs") && Word_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_SMS(izen_konstante, "min") || Word_SMS(izen_konstante, "max")) && Word_SMS(서술상수, "(II)I")) { int byte_datuak = 빼기(1), 첫값 = 빼기(1); 넣기(Word_SMS(izen_konstante, "min") ? (첫값 < byte_datuak ? 첫값 : byte_datuak) : (첫값 > byte_datuak ? 첫값 : byte_datuak), 1); return true; }
        }
        if (Word_SMS(jabe, "java/lang/System") && komando_KODE == 184) {
            if (Word_SMS(izen_konstante, "gc") && Word_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Word_SMS(izen_konstante, "arraycopy") && Word_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int sarrera_ZENBATU = 빼기(1), helburu_balio_INDIZE = 빼기(1), byte_datuak = 빼기(2), HASI_kargu = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(byte_datuak)) {
                    int Kategoria_KODE = 힙[첫값];
                    if (힙[byte_datuak] != Kategoria_KODE || (Kategoria_KODE != 2 && Kategoria_KODE != 3 && (Kategoria_KODE < 20 || Kategoria_KODE > 23))) hutsegite_balio("arraycopy type mismatch");
                    else if (sarrera_ZENBATU < 0 || HASI_kargu < 0 || helburu_balio_INDIZE < 0 || HASI_kargu > 힙[첫값 + 1] - sarrera_ZENBATU || helburu_balio_INDIZE > 힙[byte_datuak + 1] - sarrera_ZENBATU) hutsegite_balio("ArrayIndexOutOfBoundsException");
                    else if (첫값 == byte_datuak && helburu_balio_INDIZE > HASI_kargu) { for (int Loop_INDIZE = sarrera_ZENBATU - 1; Loop_INDIZE >= 0; Loop_INDIZE--) 힙[byte_datuak + 2 + helburu_balio_INDIZE + Loop_INDIZE] = 힙[첫값 + 2 + HASI_kargu + Loop_INDIZE]; }
                    else { for (int Loop_INDIZE = 0; Loop_INDIZE < sarrera_ZENBATU && !errorea; Loop_INDIZE++) { int datuak_balio = 힙[첫값 + 2 + HASI_kargu + Loop_INDIZE]; if (Kategoria_KODE != 3 || 배열저장가능(byte_datuak, datuak_balio)) 힙[byte_datuak + 2 + helburu_balio_INDIZE + Loop_INDIZE] = datuak_balio; } }
                }
                return true;
            }
        }
        if (Word_SMS(jabe, "java/util/ArrayList") || Word_SMS(jabe, "java/util/List") || Word_SMS(jabe, "java/util/HashMap") || Word_SMS(jabe, "java/util/Map")) {
            모음호출(jabe, izen_konstante, 서술상수, komando_KODE); return true;
        }
        return false;
    }
    static void 모음늘리기(int objektu_Erreferentzia_materiala, int 필요수) {
        int 이전값 = 힙[objektu_Erreferentzia_materiala + 2], ahalmen_datuak = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (ahalmen_datuak >= 필요수) return;
        int Hurrengoa_kargu = ahalmen_datuak < 8 ? 8 : ahalmen_datuak * 2; if (Hurrengoa_kargu < 필요수) Hurrengoa_kargu = 필요수;
        int datuak_matrize = esleitu_biltegi(3, Hurrengoa_kargu); if (errorea) return;
        for (int Loop_INDIZE = 0; Loop_INDIZE < ahalmen_datuak; Loop_INDIZE++) 힙[datuak_matrize + 2 + Loop_INDIZE] = 힙[이전값 + 2 + Loop_INDIZE];
        힙[objektu_Erreferentzia_materiala + 2] = datuak_matrize; 힙참조[objektu_Erreferentzia_materiala + 2] = 1;
    }
    static void 모음호출(int jabe, int izen_konstante, int 서술상수, int komando_KODE) {
        boolean 대응참조 = Word_SMS(jabe, "java/util/HashMap") || Word_SMS(jabe, "java/util/Map"); int Kategoria_KODE = 대응참조 ? 11 : 10;
        if (Word_SMS(izen_konstante, "<init>") && komando_KODE == 183 && Word_SMS(서술상수, "()V")) { int objektu_Erreferentzia_materiala = 빼기(2); if (objektu_balio(objektu_Erreferentzia_materiala, Kategoria_KODE)) 모음늘리기(objektu_Erreferentzia_materiala, 8); return; }
        if (komando_KODE != 182 && komando_KODE != 185) { hutsegite_balio("invalid collection invocation"); return; }
        if (Word_SMS(izen_konstante, "size") && Word_SMS(서술상수, "()I") || Word_SMS(izen_konstante, "isEmpty") && Word_SMS(서술상수, "()Z")) {
            int objektu_Erreferentzia_materiala = 빼기(2); if (objektu_balio(objektu_Erreferentzia_materiala, Kategoria_KODE)) 넣기(Word_SMS(izen_konstante, "size") ? 힙[objektu_Erreferentzia_materiala + 3] : 힙[objektu_Erreferentzia_materiala + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_SMS(izen_konstante, "clear") && Word_SMS(서술상수, "()V")) { int objektu_Erreferentzia_materiala = 빼기(2); if (objektu_balio(objektu_Erreferentzia_materiala, Kategoria_KODE)) { int datuak_matrize = 힙[objektu_Erreferentzia_materiala + 2]; for (int Loop_INDIZE = 0; Loop_INDIZE < 힙[datuak_matrize + 1]; Loop_INDIZE++) 힙[datuak_matrize + 2 + Loop_INDIZE] = 0; 힙[objektu_Erreferentzia_materiala + 3] = 0; } return; }
        if (!대응참조 && Word_SMS(izen_konstante, "add") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int datuak_balio = 빼기(2), objektu_Erreferentzia_materiala = 빼기(2); if (!objektu_balio(objektu_Erreferentzia_materiala, 10)) return;
            int sarrera_ZENBATU = 힙[objektu_Erreferentzia_materiala + 3]; 모음늘리기(objektu_Erreferentzia_materiala, sarrera_ZENBATU + 1); if (!errorea) { 힙[힙[objektu_Erreferentzia_materiala + 2] + 2 + sarrera_ZENBATU] = datuak_balio; 힙[objektu_Erreferentzia_materiala + 3] = sarrera_ZENBATU + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_SMS(izen_konstante, "get") || Word_SMS(izen_konstante, "remove")) && Word_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Word_SMS(izen_konstante, "set") && Word_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = Word_SMS(izen_konstante, "set"); int datuak_balio = 지정여부 ? 빼기(2) : 0, sarrera_kargu = 빼기(1), objektu_Erreferentzia_materiala = 빼기(2);
            if (!objektu_balio(objektu_Erreferentzia_materiala, 10)) return;
            int sarrera_ZENBATU = 힙[objektu_Erreferentzia_materiala + 3], datuak_matrize = 힙[objektu_Erreferentzia_materiala + 2];
            if (sarrera_kargu < 0 || sarrera_kargu >= sarrera_ZENBATU) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[datuak_matrize + 2 + sarrera_kargu];
            if (지정여부) 힙[datuak_matrize + 2 + sarrera_kargu] = datuak_balio;
            if (Word_SMS(izen_konstante, "remove")) { for (int Loop_INDIZE = sarrera_kargu + 1; Loop_INDIZE < sarrera_ZENBATU; Loop_INDIZE++) 힙[datuak_matrize + 1 + Loop_INDIZE] = 힙[datuak_matrize + 2 + Loop_INDIZE]; 힙[datuak_matrize + 1 + sarrera_ZENBATU] = 0; 힙[objektu_Erreferentzia_materiala + 3] = sarrera_ZENBATU - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Word_SMS(izen_konstante, "get") || Word_SMS(izen_konstante, "remove")) && Word_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(izen_konstante, "put") && Word_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(izen_konstante, "containsKey") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_SMS(izen_konstante, "put"), kendu = Word_SMS(izen_konstante, "remove");
            int datuak_balio = 넣기여부 ? 빼기(2) : 0, gako_Erreferentzia_materiala = 빼기(2), objektu_Erreferentzia_materiala = 빼기(2); if (!objektu_balio(objektu_Erreferentzia_materiala, 11)) return;
            int sarrera_ZENBATU = 힙[objektu_Erreferentzia_materiala + 3], datuak_matrize = 힙[objektu_Erreferentzia_materiala + 2], 찾은여부 = -1;
            for (int Loop_INDIZE = 0; Loop_INDIZE < sarrera_ZENBATU; Loop_INDIZE++) if (값같음(gako_Erreferentzia_materiala, 힙[datuak_matrize + 2 + 2 * Loop_INDIZE])) { 찾은여부 = Loop_INDIZE; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[datuak_matrize + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(objektu_Erreferentzia_materiala, (sarrera_ZENBATU + 1) * 2); datuak_matrize = 힙[objektu_Erreferentzia_materiala + 2]; 찾은여부 = sarrera_ZENBATU; if (!errorea) 힙[objektu_Erreferentzia_materiala + 3] = sarrera_ZENBATU + 1; }
                if (!errorea) { 힙[datuak_matrize + 2 + 2 * 찾은여부] = gako_Erreferentzia_materiala; 힙[datuak_matrize + 3 + 2 * 찾은여부] = datuak_balio; }
            }
            if (kendu && 찾은여부 >= 0) { for (int Loop_INDIZE = 찾은여부 + 1; Loop_INDIZE < sarrera_ZENBATU; Loop_INDIZE++) { 힙[datuak_matrize + 2 * Loop_INDIZE] = 힙[datuak_matrize + 2 + 2 * Loop_INDIZE]; 힙[datuak_matrize + 1 + 2 * Loop_INDIZE] = 힙[datuak_matrize + 3 + 2 * Loop_INDIZE]; } 힙[datuak_matrize + 2 * sarrera_ZENBATU] = 0; 힙[datuak_matrize + 1 + 2 * sarrera_ZENBATU] = 0; 힙[objektu_Erreferentzia_materiala + 3] = sarrera_ZENBATU - 1; }
            if (Word_SMS(izen_konstante, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        hutsegite_balio("unsupported collection method");
    }
    static boolean 잠금얻기(int objektu_Erreferentzia_materiala) {
        if (!객체유효(objektu_Erreferentzia_materiala)) return false;
        if (잠금깊이[objektu_Erreferentzia_materiala] != 0 && 잠금주인[objektu_Erreferentzia_materiala] != 현재가닥 + 1) { aldatu_eskaera = true; return false; }
        잠금주인[objektu_Erreferentzia_materiala] = 현재가닥 + 1; 잠금깊이[objektu_Erreferentzia_materiala]++; return true;
    }
    static void 잠금풀기(int objektu_Erreferentzia_materiala) {
        if (!객체유효(objektu_Erreferentzia_materiala)) return;
        if (잠금깊이[objektu_Erreferentzia_materiala] == 0 || 잠금주인[objektu_Erreferentzia_materiala] != 현재가닥 + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[objektu_Erreferentzia_materiala] == 0) 잠금주인[objektu_Erreferentzia_materiala] = 0;
    }
    static boolean ALDATU_hari() {
        hari_marko[현재가닥] = marko_INDIZE;
        if (marko_INDIZE < 현재가닥 * 32) hari_Egoera[현재가닥] = 3;
        for (int Loop_INDIZE = 0; Loop_INDIZE < hari_ZENBATU; Loop_INDIZE++) if (hari_Egoera[Loop_INDIZE] == 2 && hari_Egoera[가닥대기[Loop_INDIZE]] == 3) hari_Egoera[Loop_INDIZE] = 1;
        for (int Loop_INDIZE = 1; Loop_INDIZE <= hari_ZENBATU; Loop_INDIZE++) {
            int Hurrengoa_kargu = (현재가닥 + Loop_INDIZE) % hari_ZENBATU;
            if (hari_Egoera[Hurrengoa_kargu] == 1) { 현재가닥 = Hurrengoa_kargu; marko_INDIZE = hari_marko[Hurrengoa_kargu]; aldatu_eskaera = false; return true; }
        }
        for (int Loop_INDIZE = 0; Loop_INDIZE < hari_ZENBATU; Loop_INDIZE++) if (hari_Egoera[Loop_INDIZE] != 3) { hutsegite_balio("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int izen_konstante, int 서술상수, int komando_KODE) { prozesu_hari(izen_konstante, 서술상수, komando_KODE, false); }
    static void prozesu_hari(int izen_konstante, int 서술상수, int komando_KODE, boolean Euskara) {
        if (komando_KODE == 184 && Word_SMS(izen_konstante, Euskara ? "YIELD_ataza" : "yield") && Word_SMS(서술상수, "()V")) { aldatu_eskaera = true; return; }
        if (komando_KODE == 184 && Word_SMS(izen_konstante, "currentThread") && Word_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(hari_objektu[현재가닥], 2); return; }
        if (komando_KODE == 183 && Word_SMS(izen_konstante, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, Euskara ? "(LEuskara/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int helburu_helbide = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), objektu_Erreferentzia_materiala = 빼기(2);
            if (!객체유효(objektu_Erreferentzia_materiala)) return;
            if (힙[objektu_Erreferentzia_materiala] == 13) { 힙[objektu_Erreferentzia_materiala + 2] = helburu_helbide; 힙참조[objektu_Erreferentzia_materiala + 2] = 1; }
            else if (helburu_helbide != 0) hutsegite_balio("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (komando_KODE == 182 && (Word_SMS(izen_konstante, Euskara ? "HASI_ataza" : "start") || Word_SMS(izen_konstante, Euskara ? "기다리기" : "join")) && Word_SMS(서술상수, "()V") || komando_KODE == 182 && Word_SMS(izen_konstante, Euskara ? "살아있는가" : "isAlive") && Word_SMS(서술상수, "()Z")) {
            int objektu_Erreferentzia_materiala = 빼기(2); if (!객체유효(objektu_Erreferentzia_materiala)) return;
            int kontu_balio = -1; for (int Loop_INDIZE = 0; Loop_INDIZE < hari_ZENBATU; Loop_INDIZE++) if (hari_objektu[Loop_INDIZE] == objektu_Erreferentzia_materiala) kontu_balio = Loop_INDIZE;
            if (Word_SMS(izen_konstante, Euskara ? "살아있는가" : "isAlive")) { 넣기(kontu_balio >= 0 && hari_Egoera[kontu_balio] != 3 ? 1 : 0, 1); return; }
            if (Word_SMS(izen_konstante, Euskara ? "기다리기" : "join")) { if (kontu_balio >= 0 && hari_Egoera[kontu_balio] != 3) { 가닥대기[현재가닥] = kontu_balio; hari_Egoera[현재가닥] = 2; aldatu_eskaera = true; } return; }
            if (kontu_balio >= 0) { 예외던짐(Euskara ? 38 : 16, "thread already started"); return; }
            if (hari_ZENBATU == 4) { hutsegite_balio("thread limit (4 including main)"); return; }
            int helburu_helbide = 힙[objektu_Erreferentzia_materiala] == 13 ? 힙[objektu_Erreferentzia_materiala + 2] : objektu_Erreferentzia_materiala;
            int fitxategi_INDIZE = helburu_helbide > 0 && 힙[helburu_helbide] >= 32 ? 이름함수(힙[helburu_helbide] - 32, Euskara ? "Exekutatu" : "run", "()V") : -1;
            if (helburu_helbide != 0 && fitxategi_INDIZE < 0) { hutsegite_balio("Runnable.run required"); return; }
            kontu_balio = hari_ZENBATU++; hari_objektu[kontu_balio] = objektu_Erreferentzia_materiala; hari_helburu[kontu_balio] = helburu_helbide;
            int marko = kontu_balio * 32; hari_marko[kontu_balio] = fitxategi_INDIZE < 0 ? marko - 1 : marko; hari_Egoera[kontu_balio] = fitxategi_INDIZE < 0 ? 3 : 1;
            if (fitxategi_INDIZE >= 0) { 틀함수[marko] = fitxategi_INDIZE; marko_kargu[marko] = 함수시작[fitxategi_INDIZE]; lokal_balio[marko * 128] = helburu_helbide; lokal_MOTA[marko * 128] = 2; }
            return;
        }
        hutsegite_balio("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], helbide_SMS = new int[16];
    static int lokal_helbide() { return helbide_objektu(0x7f000001); }
    static int helbide_objektu(int balio) { int objektu_Erreferentzia_materiala = esleitu_biltegi(14, 1); if (!errorea) 힙[objektu_Erreferentzia_materiala + 2] = balio; return objektu_Erreferentzia_materiala; }
    static int 주소해독(int objektu_Erreferentzia_materiala) {
        if (objektu_Erreferentzia_materiala == 0 || 글같음(objektu_Erreferentzia_materiala, Ostalari_karaktere("localhost"), false)) return 0x7f000001;
        if (!objektu_balio(objektu_Erreferentzia_materiala, 1)) return 0;
        int datuak_balio = 0, 총수 = 0, helbide_byte = 0, 자릿수 = 0, sarrera_ZENBATU = 힙[objektu_Erreferentzia_materiala + 1];
        for (int Loop_INDIZE = 0; Loop_INDIZE <= sarrera_ZENBATU; Loop_INDIZE++) {
            int karaktere_kode = Loop_INDIZE == sarrera_ZENBATU ? '.' : 힙[objektu_Erreferentzia_materiala + 2 + Loop_INDIZE];
            if (karaktere_kode == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } datuak_balio = datuak_balio << 8 | helbide_byte; 총수++; helbide_byte = 자릿수 = 0; }
            else { if (karaktere_kode < '0' || karaktere_kode > '9' || ++자릿수 > 3 || (helbide_byte = helbide_byte * 10 + karaktere_kode - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return datuak_balio;
    }
    static int helbide_karaktere(int datuak_balio) {
        int sarrera_ZENBATU = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int helbide_byte = datuak_balio >>> 이동비트 & 255;
            if (helbide_byte >= 100) helbide_SMS[sarrera_ZENBATU++] = '0' + helbide_byte / 100;
            if (helbide_byte >= 10) helbide_SMS[sarrera_ZENBATU++] = '0' + helbide_byte / 10 % 10;
            helbide_SMS[sarrera_ZENBATU++] = '0' + helbide_byte % 10; if (이동비트 != 0) helbide_SMS[sarrera_ZENBATU++] = '.';
        }
        int objektu_Erreferentzia_materiala = esleitu_biltegi(1, sarrera_ZENBATU); if (!errorea) for (int Loop_INDIZE = 0; Loop_INDIZE < sarrera_ZENBATU; Loop_INDIZE++) 힙[objektu_Erreferentzia_materiala + 2 + Loop_INDIZE] = helbide_SMS[Loop_INDIZE]; return objektu_Erreferentzia_materiala;
    }
    static void 통신호출(int jabe, int izen_konstante, int 서술상수, int komando_KODE) {
        if (Word_SMS(jabe, "java/net/InetAddress")) {
            if (komando_KODE == 184 && Word_SMS(izen_konstante, "getLoopbackAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(lokal_helbide(), 2); return; }
            if (komando_KODE == 184 && Word_SMS(izen_konstante, "getByName") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int datuak_balio = 주소해독(빼기(2)); if (던진객체 == 0 && !errorea) 넣기(helbide_objektu(datuak_balio), 2); return;
            }
            if (komando_KODE == 182 && Word_SMS(izen_konstante, "getHostAddress") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int objektu_Erreferentzia_materiala = 빼기(2); if (objektu_balio(objektu_Erreferentzia_materiala, 14)) 넣기(helbide_karaktere(힙[objektu_Erreferentzia_materiala + 2]), 2); return; }
        }
        if (Word_SMS(jabe, "java/net/DatagramPacket")) {
            if (komando_KODE == 183 && Word_SMS(izen_konstante, "<init>") && (Word_SMS(서술상수, "([BI)V") || Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean helburu_balio_Erreferentzia_materiala = Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int ataka_zenbaki = helburu_balio_Erreferentzia_materiala ? 빼기(1) : 0, helbide_Erreferentzia_materiala = helburu_balio_Erreferentzia_materiala ? 빼기(2) : 0;
                int sarrera_ZENBATU = 빼기(1), datuak_matrize = 빼기(2), objektu_Erreferentzia_materiala = 빼기(2);
                if (!objektu_balio(objektu_Erreferentzia_materiala, 16) || !objektu_balio(datuak_matrize, 20)) return;
                if (sarrera_ZENBATU < 0 || sarrera_ZENBATU > 힙[datuak_matrize + 1] || ataka_zenbaki < 0 || ataka_zenbaki > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (helbide_Erreferentzia_materiala != 0 && !objektu_balio(helbide_Erreferentzia_materiala, 14)) return;
                힙[objektu_Erreferentzia_materiala + 2] = datuak_matrize; 힙참조[objektu_Erreferentzia_materiala + 2] = 1; 힙[objektu_Erreferentzia_materiala + 3] = sarrera_ZENBATU;
                힙[objektu_Erreferentzia_materiala + 4] = helbide_Erreferentzia_materiala; 힙참조[objektu_Erreferentzia_materiala + 4] = 1; 힙[objektu_Erreferentzia_materiala + 5] = ataka_zenbaki; return;
            }
            if (komando_KODE == 182 && Word_SMS(izen_konstante, "setLength") && Word_SMS(서술상수, "(I)V")) {
                int sarrera_ZENBATU = 빼기(1), objektu_Erreferentzia_materiala = 빼기(2); if (!objektu_balio(objektu_Erreferentzia_materiala, 16)) return;
                if (sarrera_ZENBATU < 0 || sarrera_ZENBATU > 힙[힙[objektu_Erreferentzia_materiala + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[objektu_Erreferentzia_materiala + 3] = sarrera_ZENBATU; return;
            }
            if (komando_KODE == 182 && (Word_SMS(izen_konstante, "getData") && Word_SMS(서술상수, "()[B") || Word_SMS(izen_konstante, "getLength") && Word_SMS(서술상수, "()I") || Word_SMS(izen_konstante, "getAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;") || Word_SMS(izen_konstante, "getPort") && Word_SMS(서술상수, "()I"))) {
                int objektu_Erreferentzia_materiala = 빼기(2); if (!objektu_balio(objektu_Erreferentzia_materiala, 16)) return;
                int sarrera_kargu = Word_SMS(izen_konstante, "getData") ? 2 : Word_SMS(izen_konstante, "getLength") ? 3 : Word_SMS(izen_konstante, "getAddress") ? 4 : 5;
                넣기(힙[objektu_Erreferentzia_materiala + sarrera_kargu], sarrera_kargu == 2 || sarrera_kargu == 4 ? 2 : 1); return;
            }
        }
        if (Word_SMS(jabe, "java/net/DatagramSocket")) {
            if (komando_KODE == 183 && Word_SMS(izen_konstante, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(I)V"))) {
                int ataka_zenbaki = Word_SMS(서술상수, "()V") ? 0 : 빼기(1), objektu_Erreferentzia_materiala = 빼기(2); if (!objektu_balio(objektu_Erreferentzia_materiala, 15)) return;
                if (ataka_zenbaki < 0 || ataka_zenbaki > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = erabiltzaile.ireki_sare(ataka_zenbaki); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[objektu_Erreferentzia_materiala + 2] = 열린파일번호; return;
            }
            if (komando_KODE == 182 && Word_SMS(izen_konstante, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), objektu_Erreferentzia_materiala = 빼기(2); if (!objektu_balio(objektu_Erreferentzia_materiala, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[objektu_Erreferentzia_materiala + 3] = 밀리초값; return;
            }
            if (komando_KODE == 182 && Word_SMS(izen_konstante, "getLocalPort") && Word_SMS(서술상수, "()I")) { int objektu_Erreferentzia_materiala = 빼기(2); if (objektu_balio(objektu_Erreferentzia_materiala, 15)) 넣기(힙[objektu_Erreferentzia_materiala + 2] < 0 ? -1 : erabiltzaile.sare_ataka(힙[objektu_Erreferentzia_materiala + 2]), 1); return; }
            if (komando_KODE == 182 && Word_SMS(izen_konstante, "isClosed") && Word_SMS(서술상수, "()Z")) { int objektu_Erreferentzia_materiala = 빼기(2); if (objektu_balio(objektu_Erreferentzia_materiala, 15)) 넣기(힙[objektu_Erreferentzia_materiala + 2] < 0 ? 1 : 0, 1); return; }
            if (komando_KODE == 182 && Word_SMS(izen_konstante, "close") && Word_SMS(서술상수, "()V")) { int objektu_Erreferentzia_materiala = 빼기(2); if (objektu_balio(objektu_Erreferentzia_materiala, 15) && 힙[objektu_Erreferentzia_materiala + 2] >= 0) { erabiltzaile.파일서술자닫기(힙[objektu_Erreferentzia_materiala + 2]); 힙[objektu_Erreferentzia_materiala + 2] = -1; } return; }
            if (komando_KODE == 182 && (Word_SMS(izen_konstante, "send") || Word_SMS(izen_konstante, "receive")) && Word_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int pakete = 빼기(2), objektu_Erreferentzia_materiala = 빼기(2); if (!objektu_balio(pakete, 16) || !objektu_balio(objektu_Erreferentzia_materiala, 15)) return;
                int datuak_matrize = 힙[pakete + 2], 유효길이 = 힙[pakete + 3], 열린파일번호 = 힙[objektu_Erreferentzia_materiala + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_SMS(izen_konstante, "send")) {
                    if (!objektu_balio(힙[pakete + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDIZE = 0; Loop_INDIZE < 유효길이; Loop_INDIZE++) 통신임시[Loop_INDIZE] = 힙[datuak_matrize + 2 + Loop_INDIZE];
                    if (erabiltzaile.bidali_sare(열린파일번호, 힙[힙[pakete + 4] + 2], 힙[pakete + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int sarrera_ZENBATU = erabiltzaile.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (sarrera_ZENBATU == -11) {
                        int 현재시각 = erabiltzaile.밀리초();
                        if (힙[objektu_Erreferentzia_materiala + 4] == 0) 힙[objektu_Erreferentzia_materiala + 4] = 현재시각 + 1;
                        if (힙[objektu_Erreferentzia_materiala + 3] > 0 && 현재시각 - (힙[objektu_Erreferentzia_materiala + 4] - 1) >= 힙[objektu_Erreferentzia_materiala + 3]) { 힙[objektu_Erreferentzia_materiala + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(objektu_Erreferentzia_materiala, 2); 넣기(pakete, 2); marko_kargu[marko_INDIZE] = marko_instrukzio[marko_INDIZE]; aldatu_eskaera = true; return;
                    }
                    힙[objektu_Erreferentzia_materiala + 4] = 0;
                    if (sarrera_ZENBATU < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDIZE = 0; Loop_INDIZE < sarrera_ZENBATU; Loop_INDIZE++) 힙[datuak_matrize + 2 + Loop_INDIZE] = (byte)통신임시[Loop_INDIZE];
                    힙[pakete + 3] = sarrera_ZENBATU; 힙[pakete + 4] = helbide_objektu(통신임시[513]); 힙참조[pakete + 4] = 1; 힙[pakete + 5] = 통신임시[512];
                }
                return;
            }
        }
        hutsegite_balio("unsupported java.net method");
    }
    static boolean 흐름대기(int objektu_Erreferentzia_materiala) {
        int 현재시각 = erabiltzaile.밀리초();
        if (힙[objektu_Erreferentzia_materiala + 5] == 0) 힙[objektu_Erreferentzia_materiala + 5] = 현재시각 + 1;
        if (힙[objektu_Erreferentzia_materiala + 3] > 0 && 현재시각 - (힙[objektu_Erreferentzia_materiala + 5] - 1) >= 힙[objektu_Erreferentzia_materiala + 3]) { 힙[objektu_Erreferentzia_materiala + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        marko_kargu[marko_INDIZE] = marko_instrukzio[marko_INDIZE]; aldatu_eskaera = true; return true;
    }
    static void 흐름호출(int jabe, int izen_konstante, int 서술상수, int komando_KODE) {
        boolean 수신쪽 = Word_SMS(jabe, "java/net/ServerSocket"), Stream = Word_SMS(jabe, "java/io/InputStream") || Word_SMS(jabe, "java/io/OutputStream");
        if (!Stream && komando_KODE == 183 && Word_SMS(izen_konstante, "<init>")) {
            boolean 빈여부 = Word_SMS(서술상수, "()V"), 이름지정여부 = Word_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || 수신쪽 && Word_SMS(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { hutsegite_balio("unsupported socket constructor"); return; }
            int ataka_zenbaki = 빈여부 ? 0 : 빼기(1), helbide_Erreferentzia_materiala = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, objektu_Erreferentzia_materiala = 빼기(2);
            if (!objektu_balio(objektu_Erreferentzia_materiala, 수신쪽 ? 18 : 17)) return;
            if (ataka_zenbaki < 0 || ataka_zenbaki > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !objektu_balio(helbide_Erreferentzia_materiala, 14)) return;
            int sare_helbide = 이름지정여부 ? 주소해독(helbide_Erreferentzia_materiala) : 주소지정여부 ? 힙[helbide_Erreferentzia_materiala + 2] : 0x7f000001;
            if (errorea || 던진객체 != 0) return;
            int 열린파일번호 = erabiltzaile.Stream_kontrol(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : 수신쪽 ? erabiltzaile.Stream_kontrol(1, 열린파일번호, ataka_zenbaki) : erabiltzaile.KONEKTATU_Stream(열린파일번호, sare_helbide, ataka_zenbaki);
            if (처리값 < 0) { erabiltzaile.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[objektu_Erreferentzia_materiala + 2] = 열린파일번호; 힙[objektu_Erreferentzia_materiala + 4] = ataka_zenbaki; 힙[objektu_Erreferentzia_materiala + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!Stream && Word_SMS(izen_konstante, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), objektu_Erreferentzia_materiala = 빼기(2); if (!objektu_balio(objektu_Erreferentzia_materiala, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[objektu_Erreferentzia_materiala + 3] = 밀리초값; return; }
        if (!Stream && Word_SMS(izen_konstante, "close") && Word_SMS(서술상수, "()V")) { int objektu_Erreferentzia_materiala = 빼기(2); if (objektu_balio(objektu_Erreferentzia_materiala, 수신쪽 ? 18 : 17) && 힙[objektu_Erreferentzia_materiala + 2] >= 0) { erabiltzaile.파일서술자닫기(힙[objektu_Erreferentzia_materiala + 2]); 힙[objektu_Erreferentzia_materiala + 2] = -1; } return; }
        if (!Stream && (Word_SMS(izen_konstante, "getLocalPort") || Word_SMS(izen_konstante, "getPort") || Word_SMS(izen_konstante, "isClosed") || Word_SMS(izen_konstante, "isConnected"))) {
            int objektu_Erreferentzia_materiala = 빼기(2); if (!objektu_balio(objektu_Erreferentzia_materiala, 수신쪽 ? 18 : 17)) return;
            넣기(Word_SMS(izen_konstante, "isClosed") ? 힙[objektu_Erreferentzia_materiala + 2] < 0 ? 1 : 0 : Word_SMS(izen_konstante, "isConnected") ? 힙[objektu_Erreferentzia_materiala + 6] : Word_SMS(izen_konstante, "getPort") ? 힙[objektu_Erreferentzia_materiala + 4] : 힙[objektu_Erreferentzia_materiala + 2] < 0 ? -1 : erabiltzaile.Stream_kontrol(4, 힙[objektu_Erreferentzia_materiala + 2], 0), 1); return;
        }
        if (수신쪽 && Word_SMS(izen_konstante, "accept") && Word_SMS(서술상수, "()Ljava/net/Socket;")) {
            int objektu_Erreferentzia_materiala = 빼기(2); if (!objektu_balio(objektu_Erreferentzia_materiala, 18)) return; int 열린파일번호 = erabiltzaile.Stream_kontrol(3, 힙[objektu_Erreferentzia_materiala + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(objektu_Erreferentzia_materiala)) 넣기(objektu_Erreferentzia_materiala, 2); return; }
            힙[objektu_Erreferentzia_materiala + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = esleitu_biltegi(17, 5); if (errorea) { erabiltzaile.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = erabiltzaile.Stream_kontrol(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !Stream && ((Word_SMS(izen_konstante, "getInputStream") && Word_SMS(서술상수, "()Ljava/io/InputStream;")) || (Word_SMS(izen_konstante, "getOutputStream") && Word_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int objektu_Erreferentzia_materiala = 빼기(2); if (!objektu_balio(objektu_Erreferentzia_materiala, 17)) return; if (힙[objektu_Erreferentzia_materiala + 2] < 0 || 힙[objektu_Erreferentzia_materiala + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = esleitu_biltegi(19, 4); if (errorea) return; 힙[반환값 + 2] = objektu_Erreferentzia_materiala; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Word_SMS(izen_konstante, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (Stream) {
            boolean 읽기여부 = Word_SMS(izen_konstante, "read"), informatika_idatzi_kirurgia = Word_SMS(izen_konstante, "write"), blokeatu = Word_SMS(서술상수, "([B)I") || Word_SMS(서술상수, "([B)V"), informatika_AZPIMATRIZEA = Word_SMS(서술상수, "([BII)I") || Word_SMS(서술상수, "([BII)V");
            int sarrera_ZENBATU = informatika_AZPIMATRIZEA ? 빼기(1) : 0, 시작변위 = informatika_AZPIMATRIZEA ? 빼기(1) : 0, datuak_matrize = blokeatu || informatika_AZPIMATRIZEA ? 빼기(2) : 0;
            int datuak_balio = informatika_idatzi_kirurgia && Word_SMS(서술상수, "(I)V") ? 빼기(1) : 0, objektu_Erreferentzia_materiala = 빼기(2);
            if (!objektu_balio(objektu_Erreferentzia_materiala, 19)) return; int 부모참조 = 힙[objektu_Erreferentzia_materiala + 2], 열린파일번호 = 힙[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_SMS(izen_konstante, "close") && Word_SMS(서술상수, "()V")) { erabiltzaile.파일서술자닫기(열린파일번호); 힙[부모참조 + 2] = -1; return; }
            if (Word_SMS(izen_konstante, "flush") && Word_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !informatika_idatzi_kirurgia) || 읽기여부 != (힙[objektu_Erreferentzia_materiala + 3] == 0)) { hutsegite_balio("unsupported stream operation"); return; }
            if (blokeatu || informatika_AZPIMATRIZEA) { if (!objektu_balio(datuak_matrize, 20)) return; if (blokeatu) sarrera_ZENBATU = 힙[datuak_matrize + 1]; if (시작변위 < 0 || sarrera_ZENBATU < 0 || 시작변위 > 힙[datuak_matrize + 1] - sarrera_ZENBATU) { 예외던짐(6, "stream array bounds"); return; } }
            else sarrera_ZENBATU = 1;
            if (sarrera_ZENBATU == 0) { if (읽기여부) 넣기(0, 1); return; }
            int Osatutakoak_ZENBATU = informatika_idatzi_kirurgia ? 힙[objektu_Erreferentzia_materiala + 4] : 0, 처리값 = 0;
            while (Osatutakoak_ZENBATU < sarrera_ZENBATU) {
                처리값 = 읽기여부 ? erabiltzaile.파일한바이트읽기(열린파일번호) : erabiltzaile.파일한바이트쓰기(열린파일번호, blokeatu || informatika_AZPIMATRIZEA ? 힙[datuak_matrize + 2 + 시작변위 + Osatutakoak_ZENBATU] : datuak_balio);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (blokeatu || informatika_AZPIMATRIZEA)) 힙[datuak_matrize + 2 + 시작변위 + Osatutakoak_ZENBATU] = (byte)처리값;
                Osatutakoak_ZENBATU++; if (읽기여부 && !(blokeatu || informatika_AZPIMATRIZEA)) break;
            }
            if (처리값 == -11 && (informatika_idatzi_kirurgia || Osatutakoak_ZENBATU == 0)) {
                힙[objektu_Erreferentzia_materiala + 4] = Osatutakoak_ZENBATU;
                if (흐름대기(부모참조)) { 넣기(objektu_Erreferentzia_materiala, 2); if (blokeatu || informatika_AZPIMATRIZEA) 넣기(datuak_matrize, 2); if (informatika_AZPIMATRIZEA) { 넣기(시작변위, 1); 넣기(sarrera_ZENBATU, 1); } if (informatika_idatzi_kirurgia && !(blokeatu || informatika_AZPIMATRIZEA)) 넣기(datuak_balio, 1); } return;
            }
            힙[objektu_Erreferentzia_materiala + 4] = 0; 힙[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(Osatutakoak_ZENBATU == 0 && 처리값 == 256 ? -1 : blokeatu || informatika_AZPIMATRIZEA ? Osatutakoak_ZENBATU : 처리값, 1); return;
        }
        hutsegite_balio("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int izen_konstante) {
        if (Word_SMS(izen_konstante, "Euskara/자체/Leihoa")) return 24;
        if (Word_SMS(izen_konstante, "Euskara/자체/Etiketa")) return 26;
        if (Word_SMS(izen_konstante, "Euskara/자체/botoia")) return 27;
        if (Word_SMS(izen_konstante, "Euskara/자체/SMS_eremu")) return 28;
        if (Word_SMS(izen_konstante, "Euskara/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int izen_konstante) {
        return 한국어화면종(izen_konstante) != 0 || Word_SMS(izen_konstante, "Euskara/자체/화면구성요소") || Word_SMS(izen_konstante, "Euskara/자체/gertaera_ilara");
    }
    static int 화면종(int izen_konstante) {
        int 한국어종 = 한국어화면종(izen_konstante); if (한국어종 != 0) return 한국어종;
        if (Word_SMS(izen_konstante, "javax/swing/JFrame")) return 24;
        if (Word_SMS(izen_konstante, "javax/swing/JPanel")) return 25;
        if (Word_SMS(izen_konstante, "javax/swing/JLabel")) return 26;
        if (Word_SMS(izen_konstante, "javax/swing/JButton")) return 27;
        if (Word_SMS(izen_konstante, "javax/swing/JTextField")) return 28;
        if (Word_SMS(izen_konstante, "java/awt/event/ActionEvent")) return 29;
        if (Word_SMS(izen_konstante, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int izen_konstante) {
        return 화면종(izen_konstante) != 0 || Word_SMS(izen_konstante, "java/awt/Component") || Word_SMS(izen_konstante, "java/awt/Container") || Word_SMS(izen_konstante, "javax/swing/JComponent") || Word_SMS(izen_konstante, "javax/swing/AbstractButton") || Word_SMS(izen_konstante, "javax/swing/text/JTextComponent") || Word_SMS(izen_konstante, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int objektu_Erreferentzia_materiala) { if (!객체유효(objektu_Erreferentzia_materiala)) return false; if (힙[objektu_Erreferentzia_materiala] < 24 || 힙[objektu_Erreferentzia_materiala] > 28) { hutsegite_balio("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int objektu_Erreferentzia_materiala, int SMS_Erreferentzia_materiala) {
        if (SMS_Erreferentzia_materiala != 0 && !objektu_balio(SMS_Erreferentzia_materiala, 1)) return;
        int sarrera_ZENBATU = SMS_Erreferentzia_materiala == 0 ? 0 : 힙[SMS_Erreferentzia_materiala + 1]; if (sarrera_ZENBATU > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDIZE = 0; Loop_INDIZE < sarrera_ZENBATU; Loop_INDIZE++) 화면글임시[Loop_INDIZE] = 힙[SMS_Erreferentzia_materiala + 2 + Loop_INDIZE];
        if (erabiltzaile.화면글(힙[objektu_Erreferentzia_materiala + 2], 화면글임시, sarrera_ZENBATU) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[objektu_Erreferentzia_materiala + 3] = SMS_Erreferentzia_materiala; 힙참조[objektu_Erreferentzia_materiala + 3] = 1;
    }
    static int 화면문자읽기(int objektu_Erreferentzia_materiala) {
        int kontu_balio = 힙[objektu_Erreferentzia_materiala + 2], sarrera_ZENBATU = erabiltzaile.화면연결(8, kontu_balio, 0, 0, 0, 0), 사용수 = 0;
        if (sarrera_ZENBATU < 0) { hutsegite_balio("GUI text read failed"); return 0; }
        for (int Loop_INDIZE = 0; Loop_INDIZE < sarrera_ZENBATU; Loop_INDIZE++) { int 부호값 = erabiltzaile.화면연결(9, kontu_balio, Loop_INDIZE, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = esleitu_biltegi(1, 사용수); if (!errorea) for (int Loop_INDIZE = 0; Loop_INDIZE < 사용수; Loop_INDIZE++) 힙[반환값 + 2 + Loop_INDIZE] = 화면글임시[Loop_INDIZE]; return 반환값;
    }
    /* Euskara 객체를 직접 만들고 nukleo_balio 화면 기능에 연결한다. Swing objektu_balio/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int jabe, int izen_konstante, int 서술상수, int komando_KODE) {
        if (Word_SMS(jabe, "Euskara/자체/gertaera_ilara")) {
            if (komando_KODE == 184 && Word_SMS(izen_konstante, "나중에실행") && Word_SMS(서술상수, "(LEuskara/자체/실행할일;)V")) {
                int ataza_ekintza = 빼기(2); if (!객체유효(ataza_ekintza)) return;
                if (나중수 == 8) { hutsegite_balio("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = ataza_ekintza; return;
            }
            if (komando_KODE == 184 && Word_SMS(izen_konstante, "사건처리중인가") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            hutsegite_balio("지원하지 않는 Euskara 화면 일정 호출"); return;
        }
        if (Word_SMS(jabe, "Euskara/자체/동작알림")) {
            int 알림 = 빼기(2); if (!objektu_balio(알림, 29) || 힙[알림 + 3] == 0) return;
            if (Word_SMS(izen_konstante, "gertaera_iturburu") && Word_SMS(서술상수, "()LEuskara/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (Word_SMS(izen_konstante, "komando_SMS") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (Word_SMS(izen_konstante, "INDIZE") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else hutsegite_balio("지원하지 않는 Euskara Ekintza 알림 호출"); return;
        }
        if (komando_KODE == 183 && Word_SMS(izen_konstante, "<init>")) {
            int 종류 = 한국어화면종(jabe), 받이 = 0, 가로 = 0, Bertikala_kargu = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Word_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (erabiltzaile.화면너비() - 폭) / 2; Bertikala_kargu = (erabiltzaile.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Word_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Word_SMS(서술상수, "(Ljava/lang/String;IIIILEuskara/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); Bertikala_kargu = 빼기(1); 가로 = 빼기(1);
            } else { hutsegite_balio("지원하지 않는 Euskara 화면 생성자"); return; }
            int Testua = 빼기(2), elementu_balio = 빼기(2); if (!화면객체(elementu_balio)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || Bertikala_kargu < 0 || 폭 > erabiltzaile.화면너비() - 가로 || 높이 > erabiltzaile.화면높이() - Bertikala_kargu) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDIZE = erabiltzaile.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (INDIZE < 1 || INDIZE > 32) { hutsegite_balio("화면 elementu_balio 자리가 가득 찼습니다"); return; }
            힙[elementu_balio + 2] = INDIZE; 화면참조[INDIZE - 1] = elementu_balio;
            힙[elementu_balio + 5] = 가로; 힙[elementu_balio + 6] = Bertikala_kargu; 힙[elementu_balio + 7] = 폭; 힙[elementu_balio + 8] = 높이; 힙[elementu_balio + 10] = 2;
            힙[elementu_balio + 4] = 받이; 힙참조[elementu_balio + 4] = 1; 힙[elementu_balio + 12] = 1;
            erabiltzaile.화면연결(1, INDIZE, 가로, Bertikala_kargu, 폭, 높이);
            if (종류 == 24) erabiltzaile.화면연결(7, INDIZE, 2, 0, 0, 0);
            화면문자설정(elementu_balio, Testua); return;
        }
        if (komando_KODE != 182) { hutsegite_balio("잘못된 Euskara 화면 호출 Komandoa"); return; }
        if (Word_SMS(izen_konstante, "idatzi_SMS") && Word_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int Testua = 빼기(2), elementu_balio = 빼기(2); if (화면객체(elementu_balio)) 화면문자설정(elementu_balio, Testua); return;
        }
        if (Word_SMS(izen_konstante, "글읽기") && Word_SMS(서술상수, "()Ljava/lang/String;")) {
            int elementu_balio = 빼기(2); if (화면객체(elementu_balio)) 넣기(화면문자읽기(elementu_balio), 2); return;
        }
        if (Word_SMS(izen_konstante, "동작맡기기") && Word_SMS(서술상수, "(LEuskara/자체/동작받이;)V")) {
            int 받이 = 빼기(2), elementu_balio = 빼기(2);
            if (화면객체(elementu_balio)) { 힙[elementu_balio + 4] = 받이; 힙참조[elementu_balio + 4] = 1; 힙[elementu_balio + 12] = 1; } return;
        }
        if (Word_SMS(izen_konstante, "gehitu_elementu") && Word_SMS(서술상수, "(LEuskara/자체/화면구성요소;)V")) {
            int haur_balio = 빼기(2), 부모 = 빼기(2); if (!화면객체(haur_balio) || !화면객체(부모)) return;
            if (erabiltzaile.화면연결(2, 힙[부모 + 2], 힙[haur_balio + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[haur_balio + 11] = 부모; 힙참조[haur_balio + 11] = 1; return;
        }
        if (Word_SMS(izen_konstante, "자리정하기") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), Bertikala_kargu = 빼기(1), 가로 = 빼기(1), elementu_balio = 빼기(2); if (!화면객체(elementu_balio)) return;
            if (erabiltzaile.화면연결(1, 힙[elementu_balio + 2], 가로, Bertikala_kargu, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[elementu_balio + 5] = 가로; 힙[elementu_balio + 6] = Bertikala_kargu; 힙[elementu_balio + 7] = 폭; 힙[elementu_balio + 8] = 높이; return;
        }
        if ((Word_SMS(izen_konstante, "erakutsi_leiho") || Word_SMS(izen_konstante, "Itxi")) && Word_SMS(서술상수, "()V")) {
            boolean ikusgaitasun_balio = Word_SMS(izen_konstante, "erakutsi_leiho"); int elementu_balio = 빼기(2); if (!화면객체(elementu_balio)) return;
            if (erabiltzaile.화면연결(ikusgaitasun_balio ? 3 : 4, 힙[elementu_balio + 2], ikusgaitasun_balio ? 1 : 0, 0, 0, 0) < 0) { hutsegite_balio("화면은 interaktibo 명령에서 실행해야 합니다"); return; }
            힙[elementu_balio + 9] = ikusgaitasun_balio ? 1 : 0; return;
        }
        if (Word_SMS(izen_konstante, "보이는가") && Word_SMS(서술상수, "()Z")) { int elementu_balio = 빼기(2); if (화면객체(elementu_balio)) 넣기(힙[elementu_balio + 9], 1); return; }
        hutsegite_balio("지원하지 않는 Euskara 화면 메서드");
    }
    static void 화면호출(int jabe, int izen_konstante, int 서술상수, int komando_KODE) {
        if (Word_SMS(jabe, "javax/swing/SwingUtilities")) {
            if (komando_KODE == 184 && Word_SMS(izen_konstante, "invokeLater") && Word_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int objektu_Erreferentzia_materiala = 빼기(2); if (!객체유효(objektu_Erreferentzia_materiala)) return; if (나중수 == 8) { hutsegite_balio("invokeLater queue full"); return; } 나중실행[나중수++] = objektu_Erreferentzia_materiala; return; }
            if (komando_KODE == 184 && Word_SMS(izen_konstante, "isEventDispatchThread") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            hutsegite_balio("unsupported SwingUtilities method"); return;
        }
        if (Word_SMS(jabe, "java/awt/event/ActionEvent")) {
            int objektu_Erreferentzia_materiala = 빼기(2); if (!objektu_balio(objektu_Erreferentzia_materiala, 29)) return;
            if (Word_SMS(izen_konstante, "getSource") && Word_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[objektu_Erreferentzia_materiala + 2], 2);
            else if (Word_SMS(izen_konstante, "getActionCommand") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[objektu_Erreferentzia_materiala + 2]), 2);
            else if (Word_SMS(izen_konstante, "getID") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else hutsegite_balio("unsupported ActionEvent method"); return;
        }
        if (komando_KODE == 183 && Word_SMS(izen_konstante, "<init>")) {
            int ZUTABEAK = 0, SMS_Erreferentzia_materiala = 0;
            if (Word_SMS(서술상수, "(I)V")) ZUTABEAK = 빼기(1);
            else if (Word_SMS(서술상수, "(Ljava/lang/String;I)V")) { ZUTABEAK = 빼기(1); SMS_Erreferentzia_materiala = 빼기(2); }
            else if (Word_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_Erreferentzia_materiala = 빼기(2);
            else if (Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_SMS(서술상수, "()V")) { hutsegite_balio("unsupported Swing constructor"); return; }
            int objektu_Erreferentzia_materiala = 빼기(2); if (!객체유효(objektu_Erreferentzia_materiala)) return;
            if (힙[objektu_Erreferentzia_materiala] == 30) { hutsegite_balio("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(objektu_Erreferentzia_materiala) || ZUTABEAK < 0) return;
            int kontu_balio = erabiltzaile.화면연결(0, 힙[objektu_Erreferentzia_materiala] - 23, 0, 0, 0, 0);
            if (kontu_balio < 1 || kontu_balio > 32) { hutsegite_balio("GUI widget slots exhausted"); return; }
            힙[objektu_Erreferentzia_materiala + 2] = kontu_balio; 화면참조[kontu_balio - 1] = objektu_Erreferentzia_materiala; 힙[objektu_Erreferentzia_materiala + 5] = 힙[objektu_Erreferentzia_materiala] == 24 ? 130 : 16; 힙[objektu_Erreferentzia_materiala + 6] = 힙[objektu_Erreferentzia_materiala] == 24 ? 110 : 16;
            힙[objektu_Erreferentzia_materiala + 7] = 힙[objektu_Erreferentzia_materiala] == 24 ? 380 : 220; 힙[objektu_Erreferentzia_materiala + 8] = 힙[objektu_Erreferentzia_materiala] == 24 ? 240 : 28; 힙[objektu_Erreferentzia_materiala + 10] = 1;
            화면문자설정(objektu_Erreferentzia_materiala, SMS_Erreferentzia_materiala); return;
        }
        if (Word_SMS(izen_konstante, "setText") || Word_SMS(izen_konstante, "setTitle")) { int SMS_Erreferentzia_materiala = 빼기(2), objektu_Erreferentzia_materiala = 빼기(2); if (화면객체(objektu_Erreferentzia_materiala) && Word_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(objektu_Erreferentzia_materiala, SMS_Erreferentzia_materiala); return; }
        if (Word_SMS(izen_konstante, "getText") || Word_SMS(izen_konstante, "getTitle")) { int objektu_Erreferentzia_materiala = 빼기(2); if (화면객체(objektu_Erreferentzia_materiala) && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(objektu_Erreferentzia_materiala), 2); return; }
        if (Word_SMS(izen_konstante, "addActionListener") && Word_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), objektu_Erreferentzia_materiala = 빼기(2); if (화면객체(objektu_Erreferentzia_materiala)) { 힙[objektu_Erreferentzia_materiala + 4] = 수신참조; 힙참조[objektu_Erreferentzia_materiala + 4] = 1; } return; }
        if (Word_SMS(izen_konstante, "getContentPane") && Word_SMS(서술상수, "()Ljava/awt/Container;")) { int objektu_Erreferentzia_materiala = 빼기(2); if (화면객체(objektu_Erreferentzia_materiala)) 넣기(objektu_Erreferentzia_materiala, 2); return; }
        if (Word_SMS(izen_konstante, "setLayout") && Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int diseinu_Erreferentzia_materiala = 빼기(2), objektu_Erreferentzia_materiala = 빼기(2); if (화면객체(objektu_Erreferentzia_materiala) && diseinu_Erreferentzia_materiala != 0) hutsegite_balio("only absolute layout (null) is supported"); return; }
        if (Word_SMS(izen_konstante, "add") && (Word_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean diseinu_baldintza = Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (diseinu_baldintza) 빼기(2);
            int haur_Erreferentzia_materiala = 빼기(2), objektu_Erreferentzia_materiala = 빼기(2); if (!화면객체(haur_Erreferentzia_materiala) || !화면객체(objektu_Erreferentzia_materiala)) return;
            if (erabiltzaile.화면연결(2, 힙[objektu_Erreferentzia_materiala + 2], 힙[haur_Erreferentzia_materiala + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[haur_Erreferentzia_materiala + 11] = objektu_Erreferentzia_materiala; 힙참조[haur_Erreferentzia_materiala + 11] = 1; if (!diseinu_baldintza) 넣기(haur_Erreferentzia_materiala, 2); return;
        }
        if (Word_SMS(izen_konstante, "setBounds") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), Y_koordenatu = 빼기(1), X_koordenatu = 빼기(1), objektu_Erreferentzia_materiala = 빼기(2); if (!화면객체(objektu_Erreferentzia_materiala)) return;
            if (erabiltzaile.화면연결(1, 힙[objektu_Erreferentzia_materiala + 2], X_koordenatu, Y_koordenatu, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[objektu_Erreferentzia_materiala + 5] = X_koordenatu; 힙[objektu_Erreferentzia_materiala + 6] = Y_koordenatu; 힙[objektu_Erreferentzia_materiala + 7] = 너비; 힙[objektu_Erreferentzia_materiala + 8] = 높이; return;
        }
        if (Word_SMS(izen_konstante, "setSize") && Word_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), objektu_Erreferentzia_materiala = 빼기(2); if (!화면객체(objektu_Erreferentzia_materiala)) return;
            if (erabiltzaile.화면연결(1, 힙[objektu_Erreferentzia_materiala + 2], 힙[objektu_Erreferentzia_materiala + 5], 힙[objektu_Erreferentzia_materiala + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[objektu_Erreferentzia_materiala + 7] = 너비; 힙[objektu_Erreferentzia_materiala + 8] = 높이; } return;
        }
        if (Word_SMS(izen_konstante, "setLocationRelativeTo") && Word_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), objektu_Erreferentzia_materiala = 빼기(2); if (!화면객체(objektu_Erreferentzia_materiala)) return; if (상대배치 != 0) { hutsegite_balio("only screen centering supported"); return; } 힙[objektu_Erreferentzia_materiala + 5] = (erabiltzaile.화면너비() - 힙[objektu_Erreferentzia_materiala + 7]) / 2; 힙[objektu_Erreferentzia_materiala + 6] = (erabiltzaile.화면높이() - 힙[objektu_Erreferentzia_materiala + 8]) / 2; erabiltzaile.화면연결(1, 힙[objektu_Erreferentzia_materiala + 2], 힙[objektu_Erreferentzia_materiala + 5], 힙[objektu_Erreferentzia_materiala + 6], 힙[objektu_Erreferentzia_materiala + 7], 힙[objektu_Erreferentzia_materiala + 8]); return; }
        if (Word_SMS(izen_konstante, "setDefaultCloseOperation") && Word_SMS(서술상수, "(I)V")) { int gidalerro = 빼기(1), objektu_Erreferentzia_materiala = 빼기(2); if (화면객체(objektu_Erreferentzia_materiala)) { if (gidalerro < 0 || gidalerro > 3) 예외던짐(9, "close policy"); else { 힙[objektu_Erreferentzia_materiala + 10] = gidalerro; erabiltzaile.화면연결(7, 힙[objektu_Erreferentzia_materiala + 2], gidalerro, 0, 0, 0); } } return; }
        if (Word_SMS(izen_konstante, "setVisible") && Word_SMS(서술상수, "(Z)V")) { int datuak_balio = 빼기(1), objektu_Erreferentzia_materiala = 빼기(2); if (화면객체(objektu_Erreferentzia_materiala)) { int 처리값 = erabiltzaile.화면연결(3, 힙[objektu_Erreferentzia_materiala + 2], datuak_balio, 0, 0, 0); if (처리값 < 0) hutsegite_balio("Swing requires a standalone interactive command"); else 힙[objektu_Erreferentzia_materiala + 9] = datuak_balio; } return; }
        if (Word_SMS(izen_konstante, "dispose") && Word_SMS(서술상수, "()V")) { int objektu_Erreferentzia_materiala = 빼기(2); if (화면객체(objektu_Erreferentzia_materiala)) { erabiltzaile.화면연결(4, 힙[objektu_Erreferentzia_materiala + 2], 0, 0, 0, 0); 힙[objektu_Erreferentzia_materiala + 9] = 0; } return; }
        if (Word_SMS(izen_konstante, "repaint") || Word_SMS(izen_konstante, "validate")) { int objektu_Erreferentzia_materiala = 빼기(2); if (!화면객체(objektu_Erreferentzia_materiala) || !Word_SMS(서술상수, "()V")) return; erabiltzaile.화면연결(1, 힙[objektu_Erreferentzia_materiala + 2], 힙[objektu_Erreferentzia_materiala + 5], 힙[objektu_Erreferentzia_materiala + 6], 힙[objektu_Erreferentzia_materiala + 7], 힙[objektu_Erreferentzia_materiala + 8]); return; }
        if (Word_SMS(izen_konstante, "isVisible") && Word_SMS(서술상수, "()Z")) { int objektu_Erreferentzia_materiala = 빼기(2); if (화면객체(objektu_Erreferentzia_materiala)) 넣기(힙[objektu_Erreferentzia_materiala + 9], 1); return; }
        hutsegite_balio("unsupported Swing method (native subset)");
    }
    static void 사건실행(int helburu_helbide, int 사건번호, boolean Euskara) {
        if (helburu_helbide < 1 || 힙[helburu_helbide] < 32) { hutsegite_balio("Java event listener required"); return; }
        int fitxategi_INDIZE = 이름함수(힙[helburu_helbide] - 32, 사건번호 == 0 ? (Euskara ? "Exekutatu" : "run") : (Euskara ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (Euskara ? "(LEuskara/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (fitxategi_INDIZE < 0) { hutsegite_balio("event callback missing"); return; }
        현재가닥 = 0; hari_ZENBATU = 1; marko_INDIZE = 0; hari_Egoera[0] = 1; marko_pila[0] = 0; 틀잠금[0] = hasieratu_marko[0] = 0; aldatu_eskaera = false;
        for (int Loop_INDIZE = 0; Loop_INDIZE < 128; Loop_INDIZE++) { lokal_balio[Loop_INDIZE] = lokal_MOTA[Loop_INDIZE] = 0; }
        틀함수[0] = fitxategi_INDIZE; marko_kargu[0] = 함수시작[fitxategi_INDIZE]; lokal_balio[0] = helburu_helbide; lokal_MOTA[0] = 2;
        if (사건번호 != 0) { lokal_balio[1] = 사건번호; lokal_MOTA[1] = 2; }
        사건중 = true; exekutatu_komando(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!errorea) {
            if (나중수 > 0) { int helburu_helbide = 나중실행[0], Euskara = 나중한국어[0]; for (int Loop_INDIZE = 1; Loop_INDIZE < 나중수; Loop_INDIZE++) { 나중실행[Loop_INDIZE - 1] = 나중실행[Loop_INDIZE]; 나중한국어[Loop_INDIZE - 1] = 나중한국어[Loop_INDIZE]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(helburu_helbide, 0, Euskara != 0); continue; }
            if (erabiltzaile.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = erabiltzaile.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { hutsegite_balio("GUI event I/O failed"); return; }
            int kontu_balio = 사건번호 & 65535; if (kontu_balio < 1 || kontu_balio > 32) continue; int objektu_Erreferentzia_materiala = 화면참조[kontu_balio - 1]; if (objektu_Erreferentzia_materiala == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[objektu_Erreferentzia_materiala + 10] != 0) 힙[objektu_Erreferentzia_materiala + 9] = 0;
                if (힙[objektu_Erreferentzia_materiala + 10] == 3) for (int Loop_INDIZE = 0; Loop_INDIZE < 32; Loop_INDIZE++) if (화면참조[Loop_INDIZE] != 0 && 힙[화면참조[Loop_INDIZE]] == 24) erabiltzaile.화면연결(4, Loop_INDIZE + 1, 0, 0, 0, 0);
            } else if (힙[objektu_Erreferentzia_materiala + 4] != 0) {
                int IRAKHAU_Erreferentzia_materiala = esleitu_biltegi(29, 2); if (errorea) return; 힙[IRAKHAU_Erreferentzia_materiala + 2] = objektu_Erreferentzia_materiala; 힙[IRAKHAU_Erreferentzia_materiala + 3] = 힙[objektu_Erreferentzia_materiala + 12]; 힙참조[IRAKHAU_Erreferentzia_materiala + 2] = 1; 사건실행(힙[objektu_Erreferentzia_materiala + 4], IRAKHAU_Erreferentzia_materiala, 힙[objektu_Erreferentzia_materiala + 12] != 0);
            }
        }
    }
    public static int Exekutatu_2() {
        if (erabiltzaile.인수개수() == 1 && 자바도구.같음(erabiltzaile.Argumentuak(0), "-version")) {
            erabiltzaile.Idatzi("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (erabiltzaile.인수개수() < 1) { erabiltzaile.Idatzi("Usage: java CLASS [ARGS]\n"); return 2; }
        sarrera_Gela_Definizioa = karga_Gela_Definizioa(Ostalari_karaktere(erabiltzaile.Argumentuak(0))); if (errorea || sarrera_Gela_Definizioa < 0) return 1;
        int sarrera_p_balio = 이름함수(sarrera_Gela_Definizioa, "Exekutatu_2", "()V");
        boolean 한국어진입 = sarrera_p_balio >= 0 && (함수권한[sarrera_p_balio] & 9) == 9;
        if (!한국어진입) sarrera_p_balio = 이름함수(sarrera_Gela_Definizioa, "main", "([Ljava/lang/String;)V");
        if (sarrera_p_balio < 0 || (함수권한[sarrera_p_balio] & 9) != 9) hutsegite_balio("public static void Exekutatu_2() or main(String[] args) required");
        if (errorea) return 1;
        int Argumentuak = esleitu_biltegi(3, erabiltzaile.인수개수() - 1); matrize_elementu[Argumentuak] = -1;
        for (int 수 = 1; 수 < erabiltzaile.인수개수() && !errorea; 수++) 힙[Argumentuak + 1 + 수] = Ostalari_karaktere(erabiltzaile.Argumentuak(수));
        marko_INDIZE = 0; 틀함수[0] = sarrera_p_balio; marko_kargu[0] = 함수시작[sarrera_p_balio]; lokal_balio[0] = 한국어진입 ? 0 : Argumentuak; lokal_MOTA[0] = 한국어진입 ? 0 : 2;
        hari_Egoera[0] = 1; hari_objektu[0] = esleitu_biltegi(13, 2);
        exekutatu_komando(); if (!errorea) 화면사건들(); return errorea ? 1 : 0;
    }
}
