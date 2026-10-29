// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Fitxategia/스택/Erreferentzia_materiala/adar 경계를 exekutatu_komando 중 검사한다. */
public final class 자바가상기계 {
    static int[] Fitxategia = new int[16384], fitxategi_izen_SMS = new int[64];
    static int[] konstante_etiketa = new int[512], 상가 = new int[512], konstante_SEGUNDOA_balio = new int[512], kate_Erreferentzia_materiala = new int[512];
    static int[] 함수명 = new int[32], 함수형 = new int[32], 함수권한 = new int[32];
    static int[] 함수시작 = new int[32], 함수끝 = new int[32], 함수스택 = new int[32], 함수지역 = new int[32];
    static int[] 함수인수수 = new int[32], 함수인수형 = new int[512], 함수반환 = new int[32];
    static int[] 경계 = new int[16384];
    static int[] lokal_balio = new int[4096], lokal_MOTA = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] 틀함수 = new int[32], marko_kargu = new int[32], marko_pila = new int[32];
    static int[] 힙 = new int[8192];
    static int Tamaina, 읽기위치, konstante_ZENBATU, 함수수, klasearen_izen, marko_INDIZE = -1, 힙끝 = 1, itzuli_MOTA;
    static boolean errorea;

    static void hutsegite_balio(String Word_SMS) {
        if (!errorea) { erabiltzaile.Idatzi("JVM error: "); erabiltzaile.Idatzi(Word_SMS); erabiltzaile.idatzi_karaktere_balio(10); }
        errorea = true;
    }
    static boolean klip(int Exekutatu_2, int luzera_balio) { return Exekutatu_2 >= 0 && luzera_balio >= 0 && Exekutatu_2 <= Tamaina - luzera_balio; }
    static int byte_balio() {
        if (!klip(읽기위치, 1)) { hutsegite_balio("truncated class file"); return 0; }
        return Fitxategia[읽기위치++];
    }
    static int 짧은수() { return byte_balio() << 8 | byte_balio(); }
    static int osoko_zenbaki() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int luzera_balio) { if (!klip(읽기위치, luzera_balio)) hutsegite_balio("invalid attribute size"); else 읽기위치 += luzera_balio; }
    static boolean txeke_konstante(int 수, int 종류) {
        if (수 <= 0 || 수 >= konstante_ZENBATU || konstante_etiketa[수] != 종류) { hutsegite_balio("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_barruti(int Exekutatu_2, int luzera_balio, String Word_SMS) {
        if (!klip(Exekutatu_2, luzera_balio) || luzera_balio != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < luzera_balio; 수++) if (Fitxategia[Exekutatu_2 + 수] != Word_SMS.charAt(수)) return false;
        return true;
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
    static void 속성건너() {
        int elementu_ZENBATU = 짧은수();
        for (int 수 = 0; 수 < elementu_ZENBATU && !errorea; 수++) { txeke_konstante(짧은수(), 1); 건너(osoko_zenbaki()); }
    }
    static int komando_luzera(int balio) {
        if (balio == 16 || balio == 18 || balio == 21 || balio == 25 || balio == 54 || balio == 58 || balio == 188) return 2;
        if (balio == 17 || balio == 19 || balio == 132 || balio >= 153 && balio <= 167
            || balio >= 178 && balio <= 184 || balio == 187 || balio == 189 || balio == 192 || balio == 198 || balio == 199) return 3;
        if (balio >= 0 && balio <= 8 || balio >= 26 && balio <= 29 || balio >= 42 && balio <= 46 || balio == 50
            || balio >= 59 && balio <= 62 || balio >= 75 && balio <= 79 || balio == 83 || balio == 87 || balio == 89 || balio == 95
            || balio == 96 || balio == 100 || balio == 104 || balio == 108 || balio == 112 || balio == 116
            || balio == 120 || balio == 122 || balio == 124 || balio == 126 || balio == 128 || balio == 130
            || balio >= 145 && balio <= 147 || balio == 172 || balio == 176 || balio == 177 || balio == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (osoko_zenbaki() != 0xcafebabe) hutsegite_balio("not a class file");
        int 부판 = 짧은수(), bertsio_balio = 짧은수();
        if (bertsio_balio < 45 || bertsio_balio > 52 || 부판 != 0) hutsegite_balio("supported class versions: 45..52, minor 0");
        konstante_ZENBATU = 짧은수();
        if (konstante_ZENBATU < 1 || konstante_ZENBATU > 512) { hutsegite_balio("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < konstante_ZENBATU && !errorea; 수++) {
            int 종류 = byte_balio(); konstante_etiketa[수] = 종류;
            if (종류 == 1) { konstante_SEGUNDOA_balio[수] = 짧은수(); 상가[수] = 읽기위치; 건너(konstante_SEGUNDOA_balio[수]); }
            else if (종류 == 3) 상가[수] = osoko_zenbaki();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); konstante_SEGUNDOA_balio[수] = 짧은수(); }
            else hutsegite_balio("unsupported constant type");
        }
        int baimen_balio = 짧은수();
        if ((baimen_balio & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) hutsegite_balio("unsupported class flags");
        klasearen_izen = klasearen_izen_SMS(짧은수());
        if (!Word_SMS(klasearen_izen_SMS(짧은수()), "java/lang/Object")) hutsegite_balio("inheritance unsupported");
        if (짧은수() != 0) hutsegite_balio("interfaces unsupported");
        if (짧은수() != 0) hutsegite_balio("fields unsupported");
        함수수 = 짧은수();
        if (함수수 < 1 || 함수수 > 32) { hutsegite_balio("method count limit (32)"); return; }
        for (int 수 = 0; 수 < 함수수 && !errorea; 수++) {
            함수권한[수] = 짧은수(); 함수명[수] = 짧은수(); 함수형[수] = 짧은수();
            txeke_konstante(함수명[수], 1); 서술읽기(수);
            if ((함수권한[수] & (0x100 | 0x400 | 0x20)) != 0) hutsegite_balio("native, abstract and synchronized methods unsupported");
            if ((함수권한[수] & 8) == 0 && !Word_SMS(함수명[수], "<init>")) hutsegite_balio("instance methods unsupported");
            if (Word_SMS(함수명[수], "<clinit>")) hutsegite_balio("class initializers unsupported");
            for (int aurrekoa_balio = 0; aurrekoa_balio < 수; aurrekoa_balio++) if (같은말(함수명[aurrekoa_balio], 함수명[수]) && 같은말(함수형[aurrekoa_balio], 함수형[수])) hutsegite_balio("duplicate method");
            int elementu_ZENBATU = 짧은수();
            for (int atributu_balio = 0; atributu_balio < elementu_ZENBATU && !errorea; atributu_balio++) {
                int Izena = 짧은수(), luzera_balio = osoko_zenbaki(), Exekutatu_2 = 읽기위치;
                if (!klip(Exekutatu_2, luzera_balio)) { hutsegite_balio("truncated method attribute"); break; }
                if (Word_SMS(Izena, "Code")) {
                    if (함수시작[수] != 0) hutsegite_balio("duplicate Code attribute");
                    함수스택[수] = 짧은수(); 함수지역[수] = 짧은수(); int KODE_luzera = osoko_zenbaki();
                    if (함수스택[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || KODE_luzera < 1 || KODE_luzera > 8192) hutsegite_balio("method memory limits exceeded");
                    함수시작[수] = 읽기위치; 건너(KODE_luzera); 함수끝[수] = 읽기위치;
                    if (짧은수() != 0) hutsegite_balio("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != Exekutatu_2 + luzera_balio) hutsegite_balio("Code attribute size mismatch");
                } else 건너(luzera_balio);
            }
            if (함수시작[수] == 0) hutsegite_balio("missing Code attribute");
            int 칸 = 함수시작[수];
            while (칸 < 함수끝[수] && !errorea) {
                int luzera_balio = komando_luzera(Fitxategia[칸]);
                if (luzera_balio == 0 || luzera_balio > 함수끝[수] - 칸) { hutsegite_balio("unsupported or truncated bytecode"); break; }
                경계[칸] = 수 + 1; 칸 += luzera_balio;
            }
            // 실행하지 않는 경로에도 잘못된 adar 목적지를 허용하지 않는다.
            칸 = 함수시작[수];
            while (칸 < 함수끝[수] && !errorea) {
                int balio = Fitxategia[칸];
                if (balio >= 153 && balio <= 167 || balio == 198 || balio == 199) {
                    int helburu_balio_a0fbc067 = 칸 + (short)(Fitxategia[칸 + 1] << 8 | Fitxategia[칸 + 2]);
                    if (helburu_balio_a0fbc067 < 함수시작[수] || helburu_balio_a0fbc067 >= 함수끝[수] || 경계[helburu_balio_a0fbc067] != 수 + 1) hutsegite_balio("invalid branch target");
                }
                칸 += komando_luzera(balio);
            }
        }
        if (!errorea) 속성건너();
        if (읽기위치 != Tamaina) hutsegite_balio("extra class file data");
    }
    static int esleitu_biltegi(int 종류, int luzera_balio) {
        if (luzera_balio < 0 || luzera_balio > 힙.length - 힙끝 - 2) { hutsegite_balio("object heap exhausted or negative array size"); return 0; }
        int Erreferentzia_materiala = 힙끝; 힙끝 += luzera_balio + 2; 힙[Erreferentzia_materiala] = 종류; 힙[Erreferentzia_materiala + 1] = luzera_balio;
        return Erreferentzia_materiala;
    }
    static boolean objektu_balio(int Erreferentzia_materiala, int 종류) {
        if (Erreferentzia_materiala < 1 || Erreferentzia_materiala >= 힙끝 - 1 || 힙[Erreferentzia_materiala] != 종류) { hutsegite_balio("null or invalid object reference"); return false; }
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
        if (marko_INDIZE == 31) { hutsegite_balio("call stack limit (32)"); return; }
        int Hurrengoa_elementu = marko_INDIZE + 1;
        for (int 수 = 0; 수 < 128; 수++) lokal_MOTA[Hurrengoa_elementu * 128 + 수] = 0;
        for (int 수 = 함수인수수[FUNTZIOA_balio] - 1; 수 >= 0; 수--) {
            lokal_balio[Hurrengoa_elementu * 128 + 수] = 빼기(함수인수형[FUNTZIOA_balio * 16 + 수]); lokal_MOTA[Hurrengoa_elementu * 128 + 수] = 함수인수형[FUNTZIOA_balio * 16 + 수];
        }
        marko_INDIZE = Hurrengoa_elementu; 틀함수[marko_INDIZE] = FUNTZIOA_balio; marko_kargu[marko_INDIZE] = 함수시작[FUNTZIOA_balio]; marko_pila[marko_INDIZE] = 0;
    }
    static void itzuli_neurria(int MOTA_balio) {
        if (MOTA_balio != 함수반환[틀함수[marko_INDIZE]]) { hutsegite_balio("return type mismatch"); return; }
        int balio = MOTA_balio == 0 ? 0 : 빼기(MOTA_balio);
        marko_INDIZE--; if (marko_INDIZE >= 0 && MOTA_balio != 0) 넣기(balio, MOTA_balio);
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
                if (balio < 1 || balio > 127) { hutsegite_balio("file stream paths currently require ASCII"); return; }
                Stream_fitxategi_izen[칸] = balio;
            }
            Stream_fitxategi_izen[luzera_balio] = 0;
            int 서술자 = erabiltzaile.파일서술자열기(Stream_fitxategi_izen, Irteera ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { hutsegite_balio("FileNotFoundException: file open failed"); return; }
            힙[Stream_balio + 2] = 서술자; 힙[Stream_balio + 3] = 1;
            return;
        }
        if (Komandoa != 182) { hutsegite_balio("invalid file stream invocation"); return; }
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
            if (EMAITZA < -1) hutsegite_balio("IOException: read failed"); else 넣기(EMAITZA, 1);
        } else if (erabiltzaile.파일한바이트쓰기(서술자, balio) != 1) hutsegite_balio("IOException: write failed");
    }
    static void 함수호출(int INDIZE, int Komandoa) {
        if (!txeke_konstante(INDIZE, 10)) return;
        int jabe_balio = klasearen_izen_SMS(상가[INDIZE]), Izena = Erreferentzia_materiala_izen(konstante_SEGUNDOA_balio[INDIZE]), formatu_balio = Erreferentzia_materiala_MOTA(konstante_SEGUNDOA_balio[INDIZE]);
        if (errorea) return;
        if (같은말(jabe_balio, klasearen_izen)) {
            if (Komandoa != 184) { hutsegite_balio("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < 함수수; 수++) if (같은말(Izena, 함수명[수]) && 같은말(formatu_balio, 함수형[수])) {
                if ((함수권한[수] & 8) == 0) hutsegite_balio("method is not static"); else 호출(수);
                return;
            }
            hutsegite_balio("NoSuchMethodError"); return;
        }
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
        hutsegite_balio("unsupported library method");
    }
    static int 배열칸(int Erreferentzia_materiala, int azpiindize_balio, int MOTA_balio) {
        if (!objektu_balio(Erreferentzia_materiala, MOTA_balio)) return 0;
        if (azpiindize_balio < 0 || azpiindize_balio >= 힙[Erreferentzia_materiala + 1]) { hutsegite_balio("ArrayIndexOutOfBoundsException"); return 0; }
        return Erreferentzia_materiala + 2 + azpiindize_balio;
    }
    static void exekutatu_komando() {
        int 남음 = 500000;
        while (marko_INDIZE >= 0 && !errorea) {
            if (--남음 == 0) { hutsegite_balio("instruction limit (500000)"); break; }
            int Exekutatu_2 = marko_kargu[marko_INDIZE], balio = 명바();
            if (errorea) break;
            if (balio == 0) continue;
            if (balio == 1) { 넣기(0, 2); continue; }
            if (balio >= 2 && balio <= 8) { 넣기(balio - 3, 1); continue; }
            if (balio == 16) { 넣기((byte)명바(), 1); continue; }
            if (balio == 17) { 넣기((short)명짧(), 1); continue; }
            if (balio == 18 || balio == 19) {
                int 수 = balio == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= konstante_ZENBATU) hutsegite_balio("invalid ldc constant");
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
            if (balio == 46 || balio == 50) {
                int azpiindize_balio = 빼기(1), Erreferentzia_materiala = 빼기(2), 칸 = 배열칸(Erreferentzia_materiala, azpiindize_balio, balio == 46 ? 2 : 3);
                if (!errorea) 넣기(힙[칸], balio == 46 ? 1 : 2); continue;
            }
            if (balio == 79 || balio == 83) {
                int elementu_elementu = 빼기(balio == 79 ? 1 : 2), azpiindize_balio = 빼기(1), Erreferentzia_materiala = 빼기(2), 칸 = 배열칸(Erreferentzia_materiala, azpiindize_balio, balio == 79 ? 2 : 3);
                if (balio == 83 && elementu_elementu != 0) objektu_balio(elementu_elementu, 1);
                if (!errorea) 힙[칸] = elementu_elementu; continue;
            }
            if (balio == 87) { 빼기(0); continue; }
            if (balio == 89) { int 가 = 빼기(0), MOTA_balio = itzuli_MOTA; 넣기(가, MOTA_balio); 넣기(가, MOTA_balio); continue; }
            if (balio == 95) { int 가 = 빼기(0), 가형 = itzuli_MOTA, 나 = 빼기(0), 나형 = itzuli_MOTA; 넣기(가, 가형); 넣기(나, 나형); continue; }
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
            if (balio == 178) {
                int 수 = 명짧(); if (!txeke_konstante(수, 9)) continue;
                if (!Word_SMS(klasearen_izen_SMS(상가[수]), "java/lang/System") || !Word_SMS(Erreferentzia_materiala_izen(konstante_SEGUNDOA_balio[수]), "out")
                    || !Word_SMS(Erreferentzia_materiala_MOTA(konstante_SEGUNDOA_balio[수]), "Ljava/io/PrintStream;")) hutsegite_balio("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (balio == 182 || balio == 183 || balio == 184) { 함수호출(명짧(), balio); continue; }
            if (balio == 187) {
                int Izena = klasearen_izen_SMS(명짧());
                if (Word_SMS(Izena, "java/lang/StringBuilder")) 넣기(esleitu_biltegi(4, 1), 2);
                else if (Word_SMS(Izena, "java/io/FileInputStream") || Word_SMS(Izena, "java/io/FileOutputStream")) {
                    int Erreferentzia_materiala = esleitu_biltegi(Word_SMS(Izena, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!errorea) { 힙[Erreferentzia_materiala + 2] = -1; 넣기(Erreferentzia_materiala, 2); }
                } else hutsegite_balio("unsupported object construction");
                continue;
            }
            if (balio == 188 || balio == 189) {
                if (balio == 188) { if (명바() != 10) hutsegite_balio("only int[] newarray is supported"); }
                else if (!Word_SMS(klasearen_izen_SMS(명짧()), "java/lang/String")) hutsegite_balio("only String[] anewarray is supported");
                int luzera_balio = 빼기(1); 넣기(esleitu_biltegi(balio == 188 ? 2 : 3, luzera_balio), 2); continue;
            }
            if (balio == 190) {
                int Erreferentzia_materiala = 빼기(2);
                if (Erreferentzia_materiala < 1 || Erreferentzia_materiala >= 힙끝 - 1 || (힙[Erreferentzia_materiala] != 2 && 힙[Erreferentzia_materiala] != 3)) hutsegite_balio("null or invalid array");
                else 넣기(힙[Erreferentzia_materiala + 1], 1); continue;
            }
            if (balio == 192) {
                int Izena = klasearen_izen_SMS(명짧()), Erreferentzia_materiala = 빼기(2);
                if (!Word_SMS(Izena, "java/lang/String")) hutsegite_balio("unsupported checkcast");
                else if (Erreferentzia_materiala != 0) objektu_balio(Erreferentzia_materiala, 1);
                넣기(Erreferentzia_materiala, 2); continue;
            }
            hutsegite_balio("unsupported bytecode");
        }
    }
    public static int Exekutatu_2() {
        if (erabiltzaile.인수개수() == 1 && 자바도구.같음(erabiltzaile.Argumentuak(0), "-version")) {
            erabiltzaile.Idatzi("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (erabiltzaile.인수개수() < 1) { erabiltzaile.Idatzi("Usage: java CLASS [ARGS]\n"); return 2; }
        int luzera_balio = 자바도구.Izena(fitxategi_izen_SMS, erabiltzaile.Argumentuak(0));
        if (luzera_balio < 1 || luzera_balio > 57) { erabiltzaile.Idatzi("java: invalid class name\n"); return 2; }
        fitxategi_izen_SMS[luzera_balio] = '.'; fitxategi_izen_SMS[luzera_balio + 1] = 'c'; fitxategi_izen_SMS[luzera_balio + 2] = 'l'; fitxategi_izen_SMS[luzera_balio + 3] = 'a'; fitxategi_izen_SMS[luzera_balio + 4] = 's'; fitxategi_izen_SMS[luzera_balio + 5] = 's';
        Tamaina = erabiltzaile.파일읽기(fitxategi_izen_SMS, Fitxategia);
        if (Tamaina < 0) { erabiltzaile.Idatzi("java: cannot read class: "); 자바도구.수쓰기(Tamaina); erabiltzaile.idatzi_karaktere_balio(10); return 1; }
        클래스읽기(); if (errorea) return 1;
        int karaktere_izen = konstante_SMS(klasearen_izen);
        if (!errorea && 힙[karaktere_izen + 1] != luzera_balio) hutsegite_balio("class name does not match file");
        for (int 수 = 0; 수 < luzera_balio && !errorea; 수++) if (힙[karaktere_izen + 2 + 수] != fitxategi_izen_SMS[수]) hutsegite_balio("class name does not match file");
        int sarrera_p_balio = -1;
        for (int 수 = 0; 수 < 함수수; 수++) if (Word_SMS(함수명[수], "main") && Word_SMS(함수형[수], "([Ljava/lang/String;)V") && (함수권한[수] & 9) == 9) sarrera_p_balio = 수;
        if (sarrera_p_balio < 0) hutsegite_balio("public static void main(String[] args) required");
        if (errorea) return 1;
        int Argumentuak = esleitu_biltegi(3, erabiltzaile.인수개수() - 1);
        for (int 수 = 1; 수 < erabiltzaile.인수개수() && !errorea; 수++) 힙[Argumentuak + 1 + 수] = Ostalari_karaktere(erabiltzaile.Argumentuak(수));
        marko_INDIZE = 0; 틀함수[0] = sarrera_p_balio; marko_kargu[0] = 함수시작[sarrera_p_balio]; lokal_balio[0] = Argumentuak; lokal_MOTA[0] = 2;
        exekutatu_komando(); return errorea ? 1 : 0;
    }
}
