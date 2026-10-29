// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Fitxer/스택/Referència/branca 경계를 Executa_ordre 중 검사한다. */
public final class 자바가상기계 {
    static int[] Fitxer = new int[16 * 16384], 임시파일 = new int[16384], nom_d_arxiu_SMS = new int[512];
    static int[] 상종류 = new int[8192], 상가 = new int[8192], 상나 = new int[8192], cadena_Referència = new int[8192];
    static int[] 함수명 = new int[512], 함수형 = new int[512], 함수권한 = new int[512], 함수주인 = new int[512];
    static int[] 함수시작 = new int[512], 함수끝 = new int[512], 함수스택 = new int[512], 함수지역 = new int[512];
    static int[] 함수인수수 = new int[512], 함수인수형 = new int[8192], 함수반환 = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] local_VALOR = new int[16384], local_TIPUS = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] 틀함수 = new int[128], marc_càrrec = new int[128], marc_Pila = new int[128], marc_instrucció = new int[128], inicialitzar_marc = new int[128];
    static int[] Classe_Definició_nom = new int[16], Classe_Definició_canviar_la_mida = new int[16], 종부모 = new int[16], Classe_Definició_Estat = new int[16], 종칸수 = new int[16], inicialitzar_Classe_Definició = new int[16];
    static int[] Classe_interfície = new int[16 * 16], Classe_interfície_COMPT = new int[16];
    static int[] 칸이름 = new int[512], 칸형 = new int[512], 칸주인 = new int[512], 칸권한 = new int[512], 칸위치 = new int[512], 칸값 = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], MATRIU_element = new int[32768], 정수저장 = new int[256];
    static int Mida, tancar_càrrec, 함수수, nom_de_classe, marc_INDEX = -1, 힙끝 = 1, tornar_les_tasques_TIPUS;
    static int Classe_Definició_COMPT, 칸수, 잡기수, 현재읽는종, 던진객체, 잠시수, mostrar_COMPT, població_COMPT;
    static int 현재가닥, fil_COMPT = 1, introducció_Classe_Definició;
    static int[] fil_marc = new int[4], fil_Estat = new int[4], fil_objecte = new int[4], fil_objectiu = new int[4], 가닥대기 = new int[4];
    static boolean s_ha_produït_un_error, canviar_sol_licitud;
    static int[] blocar_propietari = new int[32768], 잠금깊이 = new int[32768], marc_blocar = new int[128], Classe_blocar = new int[16], Classe_fil = new int[16];

    static void error_VALOR(String Word_SMS) {
        if (s_ha_produït_un_error) return;
        int Categoria_CODI = 0;
        if (자바도구.같음(Word_SMS, "ArithmeticException: / by zero")) Categoria_CODI = 4;
        if (자바도구.같음(Word_SMS, "NullPointerException") || 자바도구.같음(Word_SMS, "null or invalid array")) Categoria_CODI = 5;
        if (자바도구.같음(Word_SMS, "ArrayIndexOutOfBoundsException")) Categoria_CODI = 7;
        if (자바도구.같음(Word_SMS, "StringIndexOutOfBoundsException")) Categoria_CODI = 8;
        if (자바도구.같음(Word_SMS, "NumberFormatException")) Categoria_CODI = 10;
        if (자바도구.같음(Word_SMS, "FileNotFoundException: file open failed")) Categoria_CODI = 12;
        if (자바도구.같음(Word_SMS, "IOException: stream closed") || 자바도구.같음(Word_SMS, "IOException: read failed") || 자바도구.같음(Word_SMS, "IOException: write failed")) Categoria_CODI = 11;
        if (자바도구.같음(Word_SMS, "ClassCastException")) Categoria_CODI = 14;
        if (자바도구.같음(Word_SMS, "NegativeArraySizeException")) Categoria_CODI = 15;
        if (Categoria_CODI != 0 && marc_INDEX >= 0) { 예외던짐(Categoria_CODI, Word_SMS); return; }
        usuari.Escriptura("JVM error: "); usuari.Escriptura(Word_SMS); usuari.escriure_caràcter_VALOR(10); s_ha_produït_un_error = true;
    }
    static boolean clip(int Executa_2, int durada_VALOR) {
        if (Executa_2 < 0 || Executa_2 >= Fitxer.length || durada_VALOR < 0) return false;
        int Classe_Definició = Executa_2 / 16384;
        return Executa_2 % 16384 <= Classe_Definició_canviar_la_mida[Classe_Definició] && durada_VALOR <= Classe_Definició_canviar_la_mida[Classe_Definició] - Executa_2 % 16384;
    }
    static int byte_VALOR() {
        if (!clip(tancar_càrrec, 1)) { error_VALOR("truncated class file"); return 0; }
        return Fitxer[tancar_càrrec++];
    }
    static int 짧은수() { return byte_VALOR() << 8 | byte_VALOR(); }
    static int 정수() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int durada_VALOR) { if (!clip(tancar_càrrec, durada_VALOR)) error_VALOR("invalid attribute size"); else tancar_càrrec += durada_VALOR; }
    static boolean 상검사(int 수, int 종류) {
        if (수 <= 0 || 수 >= 상종류.length || 상종류[수] != 종류) { error_VALOR("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_interval(int Executa_2, int durada_VALOR, String Word_SMS) {
        if (!clip(Executa_2, durada_VALOR)) return false;
        int tancar_cursor = Executa_2, 끝 = Executa_2 + durada_VALOR;
        for (int Loop_INDEX = 0; Loop_INDEX < Word_SMS.length(); Loop_INDEX++) {
            int codi_de_caràcter = Word_SMS.charAt(Loop_INDEX);
            if (codi_de_caràcter > 0 && codi_de_caràcter < 128) { if (tancar_cursor >= 끝 || Fitxer[tancar_cursor++] != codi_de_caràcter) return false; }
            else if (codi_de_caràcter < 2048) {
                if (tancar_cursor + 2 > 끝 || Fitxer[tancar_cursor++] != (192 | (codi_de_caràcter >> 6)) || Fitxer[tancar_cursor++] != (128 | (codi_de_caràcter & 63))) return false;
            } else if (tancar_cursor + 3 > 끝 || Fitxer[tancar_cursor++] != (224 | (codi_de_caràcter >> 12)) || Fitxer[tancar_cursor++] != (128 | ((codi_de_caràcter >> 6) & 63)) || Fitxer[tancar_cursor++] != (128 | (codi_de_caràcter & 63))) return false;
        }
        return tancar_cursor == 끝;
    }
    static boolean Word_SMS(int 상수, String Word_SMS) { return 상검사(상수, 1) && SMS_interval(상가[상수], 상나[상수], Word_SMS); }
    static boolean 같은말(int 가, int 나) {
        if (!상검사(가, 1) || !상검사(나, 1) || 상나[가] != 상나[나]) return false;
        for (int 수 = 0; 수 < 상나[가]; 수++) if (Fitxer[상가[가] + 수] != Fitxer[상가[나] + 수]) return false;
        return true;
    }
    static int nom_de_classe_SMS(int 수) { return 상검사(수, 7) && 상검사(상가[수], 1) ? 상가[수] : 0; }
    static int Referència_nom(int 수) { return 상검사(수, 12) && 상검사(상가[수], 1) ? 상가[수] : 0; }
    static int Referència_TIPUS(int 수) { return 상검사(수, 12) && 상검사(상나[수], 1) ? 상나[수] : 0; }
    static int 서술형(int 끝, boolean 빈형) {
        if (tancar_càrrec >= 끝) { error_VALOR("invalid descriptor"); return 0; }
        int VALOR = byte_VALOR();
        if (VALOR == 'V' && 빈형) return 0;
        if (VALOR == 'I' || VALOR == 'B' || VALOR == 'C' || VALOR == 'S' || VALOR == 'Z') return 1;
        if (VALOR == '[') { 서술형(끝, false); return 2; }
        if (VALOR == 'L') {
            int Executa_2 = tancar_càrrec;
            while (tancar_càrrec < 끝 && Fitxer[tancar_càrrec] != ';') tancar_càrrec++;
            if (tancar_càrrec == 끝 || tancar_càrrec == Executa_2) error_VALOR("invalid reference descriptor");
            else tancar_càrrec++;
            return 2;
        }
        error_VALOR("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int FUNCIÓ_VALOR) {
        int 이전 = tancar_càrrec, 수 = 함수형[FUNCIÓ_VALOR];
        if (!상검사(수, 1)) return;
        tancar_càrrec = 상가[수]; int 끝 = tancar_càrrec + 상나[수];
        if (byte_VALOR() != '(') error_VALOR("invalid method descriptor");
        int element_COMPT = 0;
        while (!s_ha_produït_un_error && tancar_càrrec < 끝 && Fitxer[tancar_càrrec] != ')') {
            if (element_COMPT == 16) { error_VALOR("too many method arguments"); break; }
            함수인수형[FUNCIÓ_VALOR * 16 + element_COMPT++] = 서술형(끝, false);
        }
        if (tancar_càrrec >= 끝 || byte_VALOR() != ')') error_VALOR("invalid method descriptor");
        함수반환[FUNCIÓ_VALOR] = 서술형(끝, true); 함수인수수[FUNCIÓ_VALOR] = element_COMPT;
        if (tancar_càrrec != 끝) error_VALOR("invalid method descriptor");
        tancar_càrrec = 이전;
    }
    static int 상번호() { int VALOR = 짧은수(); return VALOR == 0 ? 0 : 현재읽는종 * 512 + VALOR; }
    static int 명상수() { return 함수주인[틀함수[marc_INDEX]] * 512 + 명짧(); }
    static void ometre_atribut() {
        int element_COMPT = 짧은수();
        for (int 수 = 0; 수 < element_COMPT && !s_ha_produït_un_error; 수++) { 상검사(상번호(), 1); 건너(정수()); }
    }
    static int ordre_durada(int VALOR) {
        if (VALOR == 16 || VALOR == 18 || VALOR == 21 || VALOR == 25 || VALOR == 54 || VALOR == 58 || VALOR == 188) return 2;
        if (VALOR == 17 || VALOR == 19 || VALOR == 132 || VALOR >= 153 && VALOR <= 167
            || VALOR >= 178 && VALOR <= 184 || VALOR == 187 || VALOR == 189 || VALOR == 192 || VALOR == 193 || VALOR == 198 || VALOR == 199) return 3;
        if (VALOR == 185 || VALOR == 200) return 5;
        if (VALOR >= 0 && VALOR <= 8 || VALOR >= 26 && VALOR <= 29 || VALOR >= 42 && VALOR <= 46 || VALOR >= 50 && VALOR <= 53
            || VALOR >= 59 && VALOR <= 62 || VALOR >= 75 && VALOR <= 79 || VALOR >= 83 && VALOR <= 95
            || VALOR == 96 || VALOR == 100 || VALOR == 104 || VALOR == 108 || VALOR == 112 || VALOR == 116
            || VALOR == 120 || VALOR == 122 || VALOR == 124 || VALOR == 126 || VALOR == 128 || VALOR == 130
            || VALOR >= 145 && VALOR <= 147 || VALOR == 172 || VALOR == 176 || VALOR == 177 || VALOR == 190 || VALOR == 191
            || VALOR == 194 || VALOR == 195) return 1;
        return 0;
    }
    static int 위치정수(int tancar_cursor) {
        if (!clip(tancar_cursor, 4)) { error_VALOR("truncated bytecode operand"); return 0; }
        return Fitxer[tancar_cursor] << 24 | Fitxer[tancar_cursor + 1] << 16 | Fitxer[tancar_cursor + 2] << 8 | Fitxer[tancar_cursor + 3];
    }
    static int tancar_durada(int tancar_cursor, int Executa_2, int 끝) {
        int VALOR = Fitxer[tancar_cursor], durada_VALOR = ordre_durada(VALOR);
        if (VALOR == 170 || VALOR == 171) {
            int BASE_càrrec = tancar_cursor + 1;
            while ((BASE_càrrec - Executa_2) % 4 != 0) BASE_càrrec++;
            if (끝 - BASE_càrrec < (VALOR == 170 ? 12 : 8)) return 0;
            int introducció_COMPT = VALOR == 170 ? 위치정수(BASE_càrrec + 8) - 위치정수(BASE_càrrec + 4) + 1 : 위치정수(BASE_càrrec + 4);
            if (introducció_COMPT < 0 || introducció_COMPT > 2048) return 0;
            durada_VALOR = BASE_càrrec - tancar_cursor + (VALOR == 170 ? 12 + 4 * introducció_COMPT : 8 + 8 * introducció_COMPT);
        }
        if (VALOR == 196 && tancar_cursor + 1 < 끝) {
            int Word_dades = Fitxer[tancar_cursor + 1]; durada_VALOR = Word_dades == 132 ? 6 : (Word_dades == 21 || Word_dades == 25 || Word_dades == 54 || Word_dades == 58) ? 4 : 0;
        }
        return durada_VALOR > 0 && durada_VALOR <= 끝 - tancar_cursor ? durada_VALOR : 0;
    }
    static void xec_destinació_VALOR(int destinació_VALOR, int FUNCIÓ_VALOR) {
        if (destinació_VALOR < 함수시작[FUNCIÓ_VALOR] || destinació_VALOR >= 함수끝[FUNCIÓ_VALOR] || 경계[destinació_VALOR] != FUNCIÓ_VALOR + 1) error_VALOR("invalid branch target");
    }
    static void tancar_Classe(int Classe_Definició) {
        현재읽는종 = Classe_Definició; tancar_càrrec = Classe_Definició * 16384; Mida = tancar_càrrec + Classe_Definició_canviar_la_mida[Classe_Definició];
        if (정수() != 0xcafebabe) { error_VALOR("not a class file"); return; }
        int 부판 = 짧은수(), versió_VALOR = 짧은수();
        if (versió_VALOR < 45 || versió_VALOR > 52 || 부판 != 0) { error_VALOR("supported class versions: 45..52, minor 0"); return; }
        int 상수수 = 짧은수(), BASE_càrrec = Classe_Definició * 512;
        if (상수수 < 1 || 상수수 > 512) { error_VALOR("constant pool limit (511)"); return; }
        for (int introducció_COMPT = 1; introducció_COMPT < 상수수 && !s_ha_produït_un_error; introducció_COMPT++) {
            int 수 = BASE_càrrec + introducció_COMPT, 종류 = byte_VALOR(); 상종류[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = tancar_càrrec; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = 정수();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); 상나[수] = 상번호(); }
            else error_VALOR("unsupported constant type");
        }
        int permís_VALOR = 짧은수();
        if ((permís_VALOR & (0x2000 | 0x4000)) != 0) error_VALOR("annotation/enum class unsupported");
        Classe_Definició_nom[Classe_Definició] = nom_de_classe_SMS(상번호());
        종부모[Classe_Definició] = nom_de_classe_SMS(상번호());
        int interfície_COMPT = 짧은수(); if (interfície_COMPT > 16) { error_VALOR("interface count limit"); return; }
        Classe_interfície_COMPT[Classe_Definició] = interfície_COMPT;
        for (int Loop_INDEX = 0; Loop_INDEX < interfície_COMPT; Loop_INDEX++) Classe_interfície[Classe_Definició * 16 + Loop_INDEX] = nom_de_classe_SMS(상번호());
        int camp_COMPT = 짧은수();
        if (camp_COMPT > 512 - 칸수) { error_VALOR("field count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < camp_COMPT && !s_ha_produït_un_error; Loop_INDEX++) {
            int arxiu_INDEX = 칸수++; 칸주인[arxiu_INDEX] = Classe_Definició; 칸권한[arxiu_INDEX] = 짧은수(); 칸이름[arxiu_INDEX] = 상번호(); 칸형[arxiu_INDEX] = 상번호();
            상검사(칸이름[arxiu_INDEX], 1); 상검사(칸형[arxiu_INDEX], 1);
            int 보존값 = tancar_càrrec; tancar_càrrec = 상가[칸형[arxiu_INDEX]]; int Categoria_CODI = 서술형(tancar_càrrec + 상나[칸형[arxiu_INDEX]], false); tancar_càrrec = 보존값;
            if ((칸권한[arxiu_INDEX] & 8) == 0) 칸위치[arxiu_INDEX] = 종칸수[Classe_Definició]++;
            int atribut_dades = 짧은수();
            for (int interna_càrrec = 0; interna_càrrec < atribut_dades && !s_ha_produït_un_error; interna_càrrec++) {
                int 이름상수 = 상번호(), 유효길이 = 정수();
                if (Word_SMS(이름상수, "ConstantValue") && 유효길이 == 2) {
                    int dades_VALOR = 상번호();
                    if (Categoria_CODI == 1 && 상검사(dades_VALOR, 3)) 칸값[arxiu_INDEX] = 상가[dades_VALOR];
                    else if (Categoria_CODI == 2 && 상검사(dades_VALOR, 8)) 칸값[arxiu_INDEX] = 상문자(상가[dades_VALOR]);
                } else 건너(유효길이);
            }
        }
        int element_COMPT = 짧은수();
        if (element_COMPT > 512 - 함수수) { error_VALOR("method count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < element_COMPT && !s_ha_produït_un_error; Loop_INDEX++) {
            int 수 = 함수수++; 함수주인[수] = Classe_Definició;
            함수권한[수] = 짧은수(); 함수명[수] = 상번호(); 함수형[수] = 상번호();
            상검사(함수명[수], 1); 서술읽기(수);
            if ((함수권한[수] & 8) == 0) {
                if (함수인수수[수] == 16) { error_VALOR("too many instance method arguments"); return; }
                for (int Comparació_càrrec = 함수인수수[수]; Comparació_càrrec > 0; Comparació_càrrec--) 함수인수형[수 * 16 + Comparació_càrrec] = 함수인수형[수 * 16 + Comparació_càrrec - 1];
                함수인수형[수 * 16] = 2; 함수인수수[수]++;
            }
            if ((함수권한[수] & 0x100) != 0) error_VALOR("user native method unsupported");
            if (Word_SMS(함수명[수], "<clinit>")) inicialitzar_Classe_Definició[Classe_Definició] = 수 + 1;
            for (int frontal_VALOR = 0; frontal_VALOR < 수; frontal_VALOR++) if (함수주인[frontal_VALOR] == Classe_Definició && 같은말(함수명[frontal_VALOR], 함수명[수]) && 같은말(함수형[frontal_VALOR], 함수형[수])) error_VALOR("duplicate method");
            int atribut_COMPT = 짧은수();
            for (int valor_d_atribut = 0; valor_d_atribut < atribut_COMPT && !s_ha_produït_un_error; valor_d_atribut++) {
                int Nom = 상번호(), durada_VALOR = 정수(), Executa_2 = tancar_càrrec;
                if (!clip(Executa_2, durada_VALOR)) { error_VALOR("truncated method attribute"); break; }
                if (Word_SMS(Nom, "Code")) {
                    if (함수시작[수] != 0) error_VALOR("duplicate Code attribute");
                    함수스택[수] = 짧은수(); 함수지역[수] = 짧은수(); int CODI_durada = 정수();
                    if (함수스택[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || CODI_durada < 1 || CODI_durada > 8192) error_VALOR("method memory limits exceeded");
                    함수시작[수] = tancar_càrrec; 건너(CODI_durada); 함수끝[수] = tancar_càrrec;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { error_VALOR("exception table limit"); return; }
                    for (int interna_càrrec = 0; interna_càrrec < 잡는수; interna_càrrec++) {
                        int error_Referència = 잡기수++; 잡기함수[error_Referència] = 수;
                        잡기시작[error_Referència] = 함수시작[수] + 짧은수(); 잡기끝[error_Referència] = 함수시작[수] + 짧은수();
                        잡기위치[error_Referència] = 함수시작[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[error_Referència] = 부호값 == 0 ? 0 : nom_de_classe_SMS(부호값);
                    }
                    ometre_atribut();
                    if (tancar_càrrec != Executa_2 + durada_VALOR) error_VALOR("Code attribute size mismatch");
                } else 건너(durada_VALOR);
            }
            if ((함수권한[수] & 0x400) != 0) continue;
            if (함수시작[수] == 0) error_VALOR("missing Code attribute");
            int 칸 = 함수시작[수];
            while (칸 < 함수끝[수] && !s_ha_produït_un_error) {
                int durada_VALOR = tancar_durada(칸, 함수시작[수], 함수끝[수]);
                if (durada_VALOR == 0) { error_VALOR("unsupported or truncated bytecode"); break; }
                경계[칸] = 수 + 1; 칸 += durada_VALOR;
            }
            칸 = 함수시작[수];
            while (칸 < 함수끝[수] && !s_ha_produït_un_error) {
                int VALOR = Fitxer[칸];
                if (VALOR >= 153 && VALOR <= 167 || VALOR == 198 || VALOR == 199) xec_destinació_VALOR(칸 + (short)(Fitxer[칸 + 1] << 8 | Fitxer[칸 + 2]), 수);
                if (VALOR == 200) xec_destinació_VALOR(칸 + 위치정수(칸 + 1), 수);
                if (VALOR == 170 || VALOR == 171) {
                    int tancar_cursor = 칸 + 1; while ((tancar_cursor - 함수시작[수]) % 4 != 0) tancar_cursor++;
                    xec_destinació_VALOR(칸 + 위치정수(tancar_cursor), 수);
                    int introducció_COMPT = VALOR == 170 ? 위치정수(tancar_cursor + 8) - 위치정수(tancar_cursor + 4) + 1 : 위치정수(tancar_cursor + 4);
                    tancar_cursor += VALOR == 170 ? 12 : 8;
                    for (int interna_càrrec = 0; interna_càrrec < introducció_COMPT; interna_càrrec++) xec_destinació_VALOR(칸 + 위치정수(tancar_cursor + interna_càrrec * (VALOR == 170 ? 4 : 8) + (VALOR == 170 ? 0 : 4)), 수);
                }
                칸 += tancar_durada(칸, 함수시작[수], 함수끝[수]);
            }
            for (int interna_càrrec = 0; interna_càrrec < 잡기수; interna_càrrec++) if (잡기함수[interna_càrrec] == 수) {
                xec_destinació_VALOR(잡기시작[interna_càrrec], 수); xec_destinació_VALOR(잡기위치[interna_càrrec], 수);
                if (잡기끝[interna_càrrec] != 함수끝[수]) xec_destinació_VALOR(잡기끝[interna_càrrec], 수);
                if (잡기시작[interna_càrrec] >= 잡기끝[interna_càrrec]) error_VALOR("invalid exception range");
            }
        }
        if (!s_ha_produït_un_error) ometre_atribut();
        if (tancar_càrrec != Mida) error_VALOR("extra class file data");
    }
    static int assignar_Emmagatzematge(int 종류, int durada_VALOR) { return 새기억(종류, durada_VALOR); }
    static boolean objecte_VALOR(int Referència, int 종류) {
        if (!객체유효(Referència)) return false;
        if (힙[Referència] != 종류) { error_VALOR("object type mismatch"); return false; }
        return true;
    }
    static int 상문자(int INDEX) {
        if (!상검사(INDEX, 1)) return 0;
        if (cadena_Referència[INDEX] != 0) return cadena_Referència[INDEX];
        int Referència = assignar_Emmagatzematge(1, 상나[INDEX]); if (s_ha_produït_un_error) return 0;
        int 끝 = 상가[INDEX] + 상나[INDEX], 수 = 상가[INDEX], durada_VALOR = 0;
        while (수 < 끝 && !s_ha_produït_un_error) {
            int VALOR = Fitxer[수++];
            if (VALOR == 0) error_VALOR("invalid modified UTF-8");
            else if (VALOR >= 192 && VALOR <= 223 && 수 < 끝) {
                int Següent_element = Fitxer[수++];
                if ((Següent_element & 192) != 128) error_VALOR("invalid modified UTF-8");
                VALOR = (VALOR & 31) << 6 | Següent_element & 63;
                if (VALOR != 0 && VALOR < 128) error_VALOR("overlong modified UTF-8");
            } else if (VALOR >= 224 && VALOR <= 239 && 수 + 1 < 끝) {
                int 가 = Fitxer[수++], 나 = Fitxer[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) error_VALOR("invalid modified UTF-8");
                VALOR = (VALOR & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (VALOR < 2048) error_VALOR("overlong modified UTF-8");
            } else if (VALOR >= 128) error_VALOR("invalid modified UTF-8");
            힙[Referència + 2 + durada_VALOR++] = VALOR;
        }
        힙[Referència + 1] = durada_VALOR; cadena_Referència[INDEX] = Referència; return Referència;
    }
    static int allotjar_caràcter(String VALOR) {
        int Referència = assignar_Emmagatzematge(1, VALOR.length()); if (s_ha_produït_un_error) return 0;
        for (int 수 = 0; 수 < VALOR.length(); 수++) 힙[Referència + 2 + 수] = VALOR.charAt(수);
        return Referència;
    }
    static void escriure_SMS(int Referència) {
        if (Referència == 0) { usuari.Escriptura("null"); return; }
        if (!objecte_VALOR(Referència, 1)) return;
        for (int 수 = 0; 수 < 힙[Referència + 1]; 수++) usuari.escriure_caràcter_VALOR(힙[Referència + 2 + 수]);
    }
    static int dígit_caràcter(int VALOR) {
        int Referència = assignar_Emmagatzematge(1, 11); if (s_ha_produït_un_error) return 0;
        int durada_VALOR = 0;
        if (VALOR < 0) 힙[Referència + 2 + durada_VALOR++] = '-'; else VALOR = -VALOR;
        int càrrec_INDEX = 1000000000; boolean Executa_2 = false;
        while (càrrec_INDEX != 0) {
            int 수 = -(VALOR / càrrec_INDEX);
            if (수 != 0 || Executa_2 || càrrec_INDEX == 1) { 힙[Referència + 2 + durada_VALOR++] = '0' + 수; Executa_2 = true; }
            VALOR %= càrrec_INDEX; càrrec_INDEX /= 10;
        }
        힙[Referència + 1] = durada_VALOR; return Referència;
    }
    static int 정수해독(int Referència) {
        if (!objecte_VALOR(Referència, 1)) return 0;
        int durada_VALOR = 힙[Referència + 1], 수 = 0, VALOR = 0; boolean 음수 = false;
        if (durada_VALOR > 0 && (힙[Referència + 2] == '-' || 힙[Referència + 2] == '+')) { 음수 = 힙[Referència + 2] == '-'; 수++; }
        if (수 == durada_VALOR) error_VALOR("NumberFormatException");
        for (; 수 < durada_VALOR && !s_ha_produït_un_error; 수++) {
            int dígit_VALOR = 힙[Referència + 2 + 수] - '0';
            if (dígit_VALOR < 0 || dígit_VALOR > 9 || VALOR < -214748364 || VALOR == -214748364 && dígit_VALOR > (음수 ? 8 : 7)) error_VALOR("NumberFormatException");
            VALOR = VALOR * 10 - dígit_VALOR;
        }
        return 음수 ? VALOR : -VALOR;
    }
    static void 넣기(int VALOR, int TIPUS_VALOR) {
        if (s_ha_produït_un_error) return;
        if (marc_INDEX < 0 || marc_Pila[marc_INDEX] >= 함수스택[틀함수[marc_INDEX]]) { error_VALOR("operand stack overflow"); return; }
        int 칸 = marc_INDEX * 128 + marc_Pila[marc_INDEX]++; 스택값[칸] = VALOR; 스택형[칸] = TIPUS_VALOR;
    }
    static int 빼기(int TIPUS_VALOR) {
        if (s_ha_produït_un_error) return 0;
        if (marc_INDEX < 0 || marc_Pila[marc_INDEX] < 1) { error_VALOR("operand stack underflow"); return 0; }
        int 칸 = marc_INDEX * 128 + --marc_Pila[marc_INDEX]; tornar_les_tasques_TIPUS = 스택형[칸];
        if (TIPUS_VALOR != 0 && tornar_les_tasques_TIPUS != TIPUS_VALOR) error_VALOR("operand type mismatch");
        if (tornar_les_tasques_TIPUS == 2) protegir_VALOR(스택값[칸]);
        return 스택값[칸];
    }
    static void tancar_local(int INDEX, int TIPUS_VALOR) {
        if (INDEX >= 함수지역[틀함수[marc_INDEX]] || INDEX < 0 || local_TIPUS[marc_INDEX * 128 + INDEX] != TIPUS_VALOR) { error_VALOR("invalid or uninitialized local"); return; }
        넣기(local_VALOR[marc_INDEX * 128 + INDEX], TIPUS_VALOR);
    }
    static void escriure_local(int INDEX, int TIPUS_VALOR) {
        if (INDEX >= 함수지역[틀함수[marc_INDEX]] || INDEX < 0) { error_VALOR("local index out of range"); return; }
        int VALOR = 빼기(TIPUS_VALOR); local_VALOR[marc_INDEX * 128 + INDEX] = VALOR; local_TIPUS[marc_INDEX * 128 + INDEX] = TIPUS_VALOR;
    }
    static int 명바() {
        int Posició = marc_càrrec[marc_INDEX];
        if (Posició < 함수시작[틀함수[marc_INDEX]] || Posició >= 함수끝[틀함수[marc_INDEX]]) { error_VALOR("instruction pointer out of range"); return 0; }
        marc_càrrec[marc_INDEX]++; return Fitxer[Posició];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void moure_VALOR(int Posició) {
        int FUNCIÓ_VALOR = 틀함수[marc_INDEX];
        if (Posició < 함수시작[FUNCIÓ_VALOR] || Posició >= 함수끝[FUNCIÓ_VALOR] || 경계[Posició] != FUNCIÓ_VALOR + 1) error_VALOR("invalid branch target");
        else marc_càrrec[marc_INDEX] = Posició;
    }
    static void 호출(int FUNCIÓ_VALOR) {
        if (marc_INDEX % 32 == 31) { error_VALOR("call stack limit (32)"); return; }
        int Següent_element = marc_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) local_TIPUS[Següent_element * 128 + 수] = 0;
        for (int 수 = 함수인수수[FUNCIÓ_VALOR] - 1; 수 >= 0; 수--) {
            local_VALOR[Següent_element * 128 + 수] = 빼기(함수인수형[FUNCIÓ_VALOR * 16 + 수]); local_TIPUS[Següent_element * 128 + 수] = 함수인수형[FUNCIÓ_VALOR * 16 + 수];
        }
        if (s_ha_produït_un_error) return;
        marc_INDEX = Següent_element; inicialitzar_marc[marc_INDEX] = 0; 틀함수[marc_INDEX] = FUNCIÓ_VALOR; marc_càrrec[marc_INDEX] = 함수시작[FUNCIÓ_VALOR]; marc_Pila[marc_INDEX] = 0;
    }
    static void tornar_les_tasques_mesura(int TIPUS_VALOR) {
        if (TIPUS_VALOR != 함수반환[틀함수[marc_INDEX]]) { error_VALOR("return type mismatch"); return; }
        int VALOR = TIPUS_VALOR == 0 ? 0 : 빼기(TIPUS_VALOR);
        if (inicialitzar_marc[marc_INDEX] != 0) Classe_Definició_Estat[inicialitzar_marc[marc_INDEX] - 1] = 2;
        if (marc_blocar[marc_INDEX] != 0) { versió_blocar(marc_blocar[marc_INDEX]); marc_blocar[marc_INDEX] = 0; }
        marc_INDEX--; if (marc_INDEX >= 현재가닥 * 32 && TIPUS_VALOR != 0) 넣기(VALOR, TIPUS_VALOR);
    }
    static int[] flux_nom_d_arxiu = new int[64];
    static void arxiu_flux_CRIDA(int propietari_VALOR, int Nom, int format_VALOR, int Ordre) {
        boolean Sortida = Word_SMS(propietari_VALOR, "java/io/FileOutputStream");
        int 종류 = Sortida ? 6 : 5;
        if (Ordre == 183 && Word_SMS(Nom, "<init>")) {
            boolean 이어 = false;
            if (Sortida && Word_SMS(format_VALOR, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(format_VALOR, "(Ljava/lang/String;)V")) { error_VALOR("unsupported file stream constructor"); return; }
            int arxiu_introducció_nom = 빼기(2), flux_VALOR = 빼기(2);
            if (!objecte_VALOR(arxiu_introducció_nom, 1) || !objecte_VALOR(flux_VALOR, 종류) || s_ha_produït_un_error) return;
            if (힙[flux_VALOR + 3] != 0) { error_VALOR("file stream already initialized"); return; }
            int durada_VALOR = 힙[arxiu_introducció_nom + 1];
            if (durada_VALOR < 1 || durada_VALOR > 63) { error_VALOR("invalid file name length"); return; }
            for (int 칸 = 0; 칸 < durada_VALOR; 칸++) {
                int VALOR = 힙[arxiu_introducció_nom + 2 + 칸];
                if (VALOR < 1) { error_VALOR("invalid file stream path"); return; }
                flux_nom_d_arxiu[칸] = VALOR;
            }
            flux_nom_d_arxiu[durada_VALOR] = 0;
            int 서술자 = usuari.파일서술자열기(flux_nom_d_arxiu, Sortida ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { error_VALOR("FileNotFoundException: file open failed"); return; }
            힙[flux_VALOR + 2] = 서술자; 힙[flux_VALOR + 3] = 1;
            return;
        }
        if (Ordre != 182) { error_VALOR("invalid file stream invocation"); return; }
        if ((Sortida && Word_SMS(Nom, "write") || !Sortida && Word_SMS(Nom, "read"))
            && (Word_SMS(format_VALOR, Sortida ? "([B)V" : "([B)I") || Word_SMS(format_VALOR, Sortida ? "([BII)V" : "([BII)I"))) {
            boolean clip_VALOR = Word_SMS(format_VALOR, Sortida ? "([BII)V" : "([BII)I");
            int introducció_COMPT = clip_VALOR ? 빼기(1) : 0, 시작점 = clip_VALOR ? 빼기(1) : 0, dades_MATRIU = 빼기(2), objecte_Referència = 빼기(2);
            if (!objecte_VALOR(dades_MATRIU, 20) || !objecte_VALOR(objecte_Referència, 종류)) return;
            if (!clip_VALOR) introducció_COMPT = 힙[dades_MATRIU + 1];
            if (시작점 < 0 || introducció_COMPT < 0 || 시작점 > 힙[dades_MATRIU + 1] - introducció_COMPT) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[objecte_Referència + 3] == 0 || 힙[objecte_Referència + 2] < 0) { error_VALOR("IOException: stream closed"); return; }
            int Completades_COMPT = 0;
            while (Completades_COMPT < introducció_COMPT && !s_ha_produït_un_error) {
                int 반환값 = Sortida ? usuari.파일한바이트쓰기(힙[objecte_Referència + 2], 힙[dades_MATRIU + 2 + 시작점 + Completades_COMPT]) : usuari.파일한바이트읽기(힙[objecte_Referència + 2]);
                if (반환값 < 0) { error_VALOR(Sortida ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!Sortida && 반환값 == 256) break;
                if (!Sortida) 힙[dades_MATRIU + 2 + 시작점 + Completades_COMPT] = (byte)반환값;
                Completades_COMPT++;
            }
            if (!Sortida) 넣기(introducció_COMPT != 0 && Completades_COMPT == 0 ? -1 : Completades_COMPT, 1);
            return;
        }
        if (Sortida && Word_SMS(Nom, "flush") && Word_SMS(format_VALOR, "()V")) { int objecte_Referència = 빼기(2); if (objecte_VALOR(objecte_Referència, 종류) && 힙[objecte_Referència + 2] < 0) error_VALOR("IOException: stream closed"); return; }
        int Acció = -1, VALOR = 0;
        if (Word_SMS(Nom, "close") && Word_SMS(format_VALOR, "()V")) Acció = 0;
        if (!Sortida && Word_SMS(Nom, "read") && Word_SMS(format_VALOR, "()I")) Acció = 1;
        if (Sortida && Word_SMS(Nom, "write") && Word_SMS(format_VALOR, "(I)V")) { Acció = 2; VALOR = 빼기(1); }
        if (Acció < 0) { error_VALOR("unsupported file stream method"); return; }
        int flux_VALOR = 빼기(2);
        if (!objecte_VALOR(flux_VALOR, 종류) || s_ha_produït_un_error) return;
        if (힙[flux_VALOR + 3] == 0) { error_VALOR("uninitialized file stream"); return; }
        int 서술자 = 힙[flux_VALOR + 2];
        if (Acció == 0) {
            if (서술자 >= 0 && usuari.파일서술자닫기(서술자) < 0) error_VALOR("IOException: close failed");
            힙[flux_VALOR + 2] = -1; return;
        }
        if (서술자 < 0) { error_VALOR("IOException: stream closed"); return; }
        if (Acció == 1) {
            int RESULTAT = usuari.파일한바이트읽기(서술자);
            if (RESULTAT < -1) error_VALOR("IOException: read failed"); else 넣기(RESULTAT == 256 ? -1 : RESULTAT, 1);
        } else if (usuari.파일한바이트쓰기(서술자, VALOR) != 1) error_VALOR("IOException: write failed");
    }
    static void 함수호출(int INDEX, int Ordre) {
        if (INDEX <= 0 || INDEX >= 상종류.length || (상종류[INDEX] != 10 && 상종류[INDEX] != 11)) { error_VALOR("invalid method reference"); return; }
        int propietari_VALOR = nom_de_classe_SMS(상가[INDEX]), Nom = Referència_nom(상나[INDEX]), format_VALOR = Referència_TIPUS(상나[INDEX]);
        if (s_ha_produït_un_error) return;
        if (기본호출(propietari_VALOR, Nom, format_VALOR, Ordre)) return;
        if (Word_SMS(propietari_VALOR, "java/io/FileInputStream") || Word_SMS(propietari_VALOR, "java/io/FileOutputStream")) {
            arxiu_flux_CRIDA(propietari_VALOR, Nom, format_VALOR, Ordre); return;
        }
        if (Ordre == 184 && Word_SMS(propietari_VALOR, "java/lang/Integer") && Word_SMS(Nom, "parseInt") && Word_SMS(format_VALOR, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Ordre == 182 && Word_SMS(propietari_VALOR, "java/io/PrintStream") && (Word_SMS(Nom, "println") || Word_SMS(Nom, "print"))) {
            int TIPUS_VALOR = 0, VALOR = 0;
            if (Word_SMS(format_VALOR, "(I)V")) { TIPUS_VALOR = 1; VALOR = 빼기(1); }
            else if (Word_SMS(format_VALOR, "(Z)V")) { TIPUS_VALOR = 2; VALOR = 빼기(1); }
            else if (Word_SMS(format_VALOR, "(C)V")) { TIPUS_VALOR = 3; VALOR = 빼기(1); }
            else if (Word_SMS(format_VALOR, "(Ljava/lang/String;)V")) { TIPUS_VALOR = 4; VALOR = 빼기(2); }
            else if (!Word_SMS(format_VALOR, "()V") || !Word_SMS(Nom, "println")) error_VALOR("unsupported print descriptor");
            if (빼기(2) != -1) error_VALOR("invalid PrintStream receiver");
            if (s_ha_produït_un_error) return;
            if (TIPUS_VALOR == 1) 자바도구.수쓰기(VALOR);
            if (TIPUS_VALOR == 2) usuari.Escriptura(VALOR == 0 ? "false" : "true");
            if (TIPUS_VALOR == 3) usuari.escriure_caràcter_VALOR(VALOR & 65535);
            if (TIPUS_VALOR == 4) escriure_SMS(VALOR);
            if (Word_SMS(Nom, "println")) usuari.escriure_caràcter_VALOR(10);
            return;
        }
        if (Ordre == 182 && Word_SMS(propietari_VALOR, "java/lang/String")) {
            if (Word_SMS(Nom, "length") && Word_SMS(format_VALOR, "()I")) {
                int Referència = 빼기(2); if (objecte_VALOR(Referència, 1)) 넣기(힙[Referència + 1], 1); return;
            }
            if (Word_SMS(Nom, "charAt") && Word_SMS(format_VALOR, "(I)C")) {
                int subíndex_VALOR = 빼기(1), Referència = 빼기(2);
                if (objecte_VALOR(Referència, 1)) {
                    if (subíndex_VALOR < 0 || subíndex_VALOR >= 힙[Referència + 1]) error_VALOR("StringIndexOutOfBoundsException"); else 넣기(힙[Referència + 2 + subíndex_VALOR], 1);
                }
                return;
            }
        }
        if (Word_SMS(propietari_VALOR, "java/lang/StringBuilder")) {
            if (Ordre == 183 && Word_SMS(Nom, "<init>") && Word_SMS(format_VALOR, "()V")) { objecte_VALOR(빼기(2), 4); return; }
            if (Ordre == 182 && Word_SMS(Nom, "toString") && Word_SMS(format_VALOR, "()Ljava/lang/String;")) {
                int Referència = 빼기(2); if (objecte_VALOR(Referència, 4)) 넣기(힙[Referència + 2] == 0 ? allotjar_caràcter("") : 힙[Referència + 2], 2); return;
            }
            if (Ordre == 182 && Word_SMS(Nom, "append")) {
                int SMS = 0;
                if (Word_SMS(format_VALOR, "(I)Ljava/lang/StringBuilder;")) SMS = dígit_caràcter(빼기(1));
                else if (Word_SMS(format_VALOR, "(Z)Ljava/lang/StringBuilder;")) SMS = allotjar_caràcter(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(format_VALOR, "(C)Ljava/lang/StringBuilder;")) {
                    int VALOR = 빼기(1); SMS = assignar_Emmagatzematge(1, 1); if (!s_ha_produït_un_error) 힙[SMS + 2] = VALOR & 65535;
                }
                else if (Word_SMS(format_VALOR, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { SMS = 빼기(2); if (SMS == 0) SMS = allotjar_caràcter("null"); }
                else { error_VALOR("unsupported StringBuilder append"); return; }
                int Referència = 빼기(2); if (!objecte_VALOR(Referència, 4) || !objecte_VALOR(SMS, 1)) return;
                int frontal_VALOR = 힙[Referència + 2], frontal_VALOR_durada = frontal_VALOR == 0 ? 0 : 힙[frontal_VALOR + 1], ENRERE_VALOR_durada = 힙[SMS + 1];
                int 새글 = assignar_Emmagatzematge(1, frontal_VALOR_durada + ENRERE_VALOR_durada); if (s_ha_produït_un_error) return;
                for (int 수 = 0; 수 < frontal_VALOR_durada; 수++) 힙[새글 + 2 + 수] = 힙[frontal_VALOR + 2 + 수];
                for (int 수 = 0; 수 < ENRERE_VALOR_durada; 수++) 힙[새글 + 2 + frontal_VALOR_durada + 수] = 힙[SMS + 2 + 수];
                힙[Referència + 2] = 새글; 넣기(Referència, 2); return;
            }
        }
        int Classe_Definició = BUSCA_Classe_Definició(propietari_VALOR); if (Classe_Definició < 0 || s_ha_produït_un_error) return;
        int arxiu_INDEX = 함수찾기(Classe_Definició, Nom, format_VALOR);
        if (arxiu_INDEX < 0) {
            for (int codi_de_caràcter = Classe_Definició, introducció_COMPT = 0; codi_de_caràcter >= 0 && introducció_COMPT < 16; introducció_COMPT++, codi_de_caràcter = 부모종(codi_de_caràcter))
                if (Word_SMS(종부모[codi_de_caràcter], "java/lang/Thread")) { 가닥호출(Nom, format_VALOR, Ordre); return; }
            error_VALOR("NoSuchMethodError"); return;
        }
        if (((함수권한[arxiu_INDEX] & 8) != 0) != (Ordre == 184)) { error_VALOR("method static/instance mismatch"); return; }
        if (Ordre == 184) { if (!inicialitzar(함수주인[arxiu_INDEX], marc_instrucció[marc_INDEX])) return; }
        else {
            int tancar_cursor = marc_Pila[marc_INDEX] - 함수인수수[arxiu_INDEX];
            if (tancar_cursor < 0 || 스택형[marc_INDEX * 128 + tancar_cursor] != 2) { error_VALOR("invalid method receiver"); return; }
            int objecte_Referència = 스택값[marc_INDEX * 128 + tancar_cursor];
            if (!객체유효(objecte_Referència)) return;
            if (힙[objecte_Referència] < 32 || !종포함(힙[objecte_Referència] - 32, propietari_VALOR)) { error_VALOR("method receiver type mismatch"); return; }
            if (Ordre != 183) arxiu_INDEX = 함수찾기(힙[objecte_Referència] - 32, Nom, format_VALOR);
        }
        if (arxiu_INDEX < 0 || (함수권한[arxiu_INDEX] & 0x400) != 0) { error_VALOR("AbstractMethodError"); return; }
        int blocar_Referència = 0;
        if ((함수권한[arxiu_INDEX] & 32) != 0) {
            if (Ordre == 184) { int codi_de_caràcter = 함수주인[arxiu_INDEX]; if (Classe_blocar[codi_de_caràcter] == 0) Classe_blocar[codi_de_caràcter] = assignar_Emmagatzematge(8, 0); blocar_Referència = Classe_blocar[codi_de_caràcter]; }
            else blocar_Referència = 스택값[marc_INDEX * 128 + marc_Pila[marc_INDEX] - 함수인수수[arxiu_INDEX]];
            if (!잠금얻기(blocar_Referència)) { if (!s_ha_produït_un_error) marc_càrrec[marc_INDEX] = marc_instrucció[marc_INDEX]; return; }
        }
        호출(arxiu_INDEX); if (!s_ha_produït_un_error) marc_blocar[marc_INDEX] = blocar_Referència;
    }
    static boolean 배열저장가능(int MATRIU_Referència, int dades_VALOR) {
        if (dades_VALOR == 0 || MATRIU_element[MATRIU_Referència] == 0) return true;
        boolean 성공여부 = MATRIU_element[MATRIU_Referència] == -1 ? (dades_VALOR > 0 && dades_VALOR < 힙끝 && 힙[dades_VALOR] == 1) : 맞는객체(dades_VALOR, MATRIU_element[MATRIU_Referència]);
        if (!성공여부 && !s_ha_produït_un_error) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int 배열칸(int Referència, int subíndex_VALOR, int TIPUS_VALOR) {
        if (!objecte_VALOR(Referència, TIPUS_VALOR)) return 0;
        if (subíndex_VALOR < 0 || subíndex_VALOR >= 힙[Referència + 1]) { error_VALOR("ArrayIndexOutOfBoundsException"); return 0; }
        return Referència + 2 + subíndex_VALOR;
    }
    static void Executa_ordre() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (s_ha_produït_un_error) { if (던진객체 != 0) control_excepció(); if (s_ha_produït_un_error || marc_INDEX < 현재가닥 * 32) break; }
            if (marc_INDEX < 현재가닥 * 32 || canviar_sol_licitud || --조각 == 0) { if (!canvi_fil()) break; 조각 = 100; }
            if (marc_INDEX == 0 && Classe_Definició_Estat[introducció_Classe_Definició] != 2 && !inicialitzar(introducció_Classe_Definició, marc_càrrec[marc_INDEX])) continue;
            if (marc_INDEX == 현재가닥 * 32 && 현재가닥 != 0 && (함수권한[틀함수[marc_INDEX]] & 32) != 0 && marc_blocar[marc_INDEX] == 0) {
                int objecte_Referència = fil_objectiu[현재가닥]; if (!잠금얻기(objecte_Referència)) { if (s_ha_produït_un_error) break; continue; } marc_blocar[marc_INDEX] = objecte_Referència;
            }
            잠시수 = 0;
            if (--남음 == 0) { error_VALOR("instruction limit (500000)"); break; }
            int Executa_2 = marc_càrrec[marc_INDEX]; marc_instrucció[marc_INDEX] = Executa_2; int VALOR = 명바();
            if (s_ha_produït_un_error) break;
            if (VALOR == 0) continue;
            if (VALOR == 1) { 넣기(0, 2); continue; }
            if (VALOR >= 2 && VALOR <= 8) { 넣기(VALOR - 3, 1); continue; }
            if (VALOR == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALOR == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALOR == 18 || VALOR == 19) {
                int 수 = 함수주인[틀함수[marc_INDEX]] * 512 + (VALOR == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= 상종류.length) error_VALOR("invalid ldc constant");
                else if (상종류[수] == 3) 넣기(상가[수], 1);
                else if (상종류[수] == 8) 넣기(상문자(상가[수]), 2);
                else error_VALOR("unsupported ldc constant");
                continue;
            }
            if (VALOR == 21 || VALOR == 25) { tancar_local(명바(), VALOR == 21 ? 1 : 2); continue; }
            if (VALOR >= 26 && VALOR <= 29) { tancar_local(VALOR - 26, 1); continue; }
            if (VALOR >= 42 && VALOR <= 45) { tancar_local(VALOR - 42, 2); continue; }
            if (VALOR == 54 || VALOR == 58) { escriure_local(명바(), VALOR == 54 ? 1 : 2); continue; }
            if (VALOR >= 59 && VALOR <= 62) { escriure_local(VALOR - 59, 1); continue; }
            if (VALOR >= 75 && VALOR <= 78) { escriure_local(VALOR - 75, 2); continue; }
            if (VALOR == 46 || VALOR >= 50 && VALOR <= 53) {
                int introducció_càrrec = 빼기(1), objecte_Referència = 빼기(2), Categoria_CODI = VALOR == 46 ? 2 : VALOR == 50 ? 3 : VALOR == 51 ? 20 : VALOR == 52 ? 22 : 23;
                if (VALOR == 51 && objecte_Referència > 0 && objecte_Referència < 힙끝 && 힙[objecte_Referència] == 21) Categoria_CODI = 21;
                int tancar_cursor = 배열칸(objecte_Referència, introducció_càrrec, Categoria_CODI); if (!s_ha_produït_un_error) 넣기(힙[tancar_cursor], VALOR == 50 ? 2 : 1); continue;
            }
            if (VALOR == 79 || VALOR >= 83 && VALOR <= 86) {
                int introducció_Referència = 빼기(VALOR == 83 ? 2 : 1), introducció_càrrec = 빼기(1), objecte_Referència = 빼기(2), Categoria_CODI = VALOR == 79 ? 2 : VALOR == 83 ? 3 : VALOR == 84 ? 20 : VALOR == 85 ? 22 : 23;
                if (VALOR == 84 && objecte_Referència > 0 && objecte_Referència < 힙끝 && 힙[objecte_Referència] == 21) Categoria_CODI = 21;
                int tancar_cursor = 배열칸(objecte_Referència, introducció_càrrec, Categoria_CODI);
                if (!s_ha_produït_un_error && Categoria_CODI == 3 && !배열저장가능(objecte_Referència, introducció_Referència)) continue;
                if (!s_ha_produït_un_error) 힙[tancar_cursor] = Categoria_CODI == 20 ? (byte)introducció_Referència : Categoria_CODI == 21 ? introducció_Referència & 1 : Categoria_CODI == 22 ? (char)introducció_Referència : Categoria_CODI == 23 ? (short)introducció_Referència : introducció_Referència;
                continue;
            }
            if (VALOR >= 87 && VALOR <= 95) { Pila_instrucció(VALOR); continue; }
            if (VALOR == 96 || VALOR == 100 || VALOR == 104 || VALOR == 108 || VALOR == 112 || VALOR == 120
                || VALOR == 122 || VALOR == 124 || VALOR == 126 || VALOR == 128 || VALOR == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), RESULTAT = 0;
                if ((VALOR == 108 || VALOR == 112) && 나 == 0) { error_VALOR("ArithmeticException: / by zero"); continue; }
                if (VALOR == 96) RESULTAT = 가 + 나;
                if (VALOR == 100) RESULTAT = 가 - 나;
                if (VALOR == 104) RESULTAT = 가 * 나;
                if (VALOR == 108) RESULTAT = 가 / 나;
                if (VALOR == 112) RESULTAT = 가 % 나;
                if (VALOR == 120) RESULTAT = 가 << 나;
                if (VALOR == 122) RESULTAT = 가 >> 나;
                if (VALOR == 124) RESULTAT = 가 >>> 나;
                if (VALOR == 126) RESULTAT = 가 & 나;
                if (VALOR == 128) RESULTAT = 가 | 나;
                if (VALOR == 130) RESULTAT = 가 ^ 나;
                넣기(RESULTAT, 1); continue;
            }
            if (VALOR == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALOR == 132) {
                int local_Àmbit = 명바(), 증분 = (byte)명바(); tancar_local(local_Àmbit, 1); 넣기(빼기(1) + 증분, 1); escriure_local(local_Àmbit, 1); continue;
            }
            if (VALOR >= 145 && VALOR <= 147) {
                int 수 = 빼기(1); 넣기(VALOR == 145 ? (byte)수 : VALOR == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (VALOR >= 153 && VALOR <= 167 || VALOR == 198 || VALOR == 199) {
                int destinació_VALOR = Executa_2 + (short)명짧(); boolean 갈까 = VALOR == 167;
                if (VALOR >= 153 && VALOR <= 158) {
                    int 수 = 빼기(1); 갈까 = VALOR == 153 ? 수 == 0 : VALOR == 154 ? 수 != 0 : VALOR == 155 ? 수 < 0 : VALOR == 156 ? 수 >= 0 : VALOR == 157 ? 수 > 0 : 수 <= 0;
                } else if (VALOR >= 159 && VALOR <= 166) {
                    int 나 = 빼기(VALOR >= 165 ? 2 : 1), 가 = 빼기(VALOR >= 165 ? 2 : 1);
                    갈까 = VALOR == 159 || VALOR == 165 ? 가 == 나 : VALOR == 160 || VALOR == 166 ? 가 != 나 : VALOR == 161 ? 가 < 나 : VALOR == 162 ? 가 >= 나 : VALOR == 163 ? 가 > 나 : 가 <= 나;
                } else if (VALOR == 198 || VALOR == 199) { int 수 = 빼기(2); 갈까 = VALOR == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) moure_VALOR(destinació_VALOR); continue;
            }
            if (VALOR == 172 || VALOR == 176 || VALOR == 177) { tornar_les_tasques_mesura(VALOR == 172 ? 1 : VALOR == 176 ? 2 : 0); continue; }
            if (VALOR >= 178 && VALOR <= 181) { 필드호출(명상수(), VALOR, Executa_2); continue; }
            if (VALOR >= 182 && VALOR <= 185) {
                int 부호값 = 명상수();
                if (VALOR == 185) { int total_COMPT = 명바(); if (total_COMPT == 0 || 명바() != 0) { error_VALOR("invalid invokeinterface operands"); continue; } }
                함수호출(부호값, VALOR); continue;
            }
            if (VALOR == 187) { 새객체(nom_de_classe_SMS(명상수()), Executa_2); continue; }
            if (VALOR == 188 || VALOR == 189) {
                int Categoria_CODI = 3, component = 0;
                if (VALOR == 188) { int 임시값 = 명바(); Categoria_CODI = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else component = nom_de_classe_SMS(명상수());
                if (Categoria_CODI == 0) { error_VALOR("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), objecte_Referència = assignar_Emmagatzematge(Categoria_CODI, 유효길이); if (!s_ha_produït_un_error) MATRIU_element[objecte_Referència] = component; 넣기(objecte_Referència, 2); continue;
            }
            if (VALOR == 190) {
                int objecte_Referència = 빼기(2);
                if (객체유효(objecte_Referència)) { int Comparació_càrrec = 힙[objecte_Referència]; if (Comparació_càrrec != 2 && Comparació_càrrec != 3 && (Comparació_càrrec < 20 || Comparació_càrrec > 23)) error_VALOR("not an array"); else 넣기(힙[objecte_Referència + 1], 1); }
                continue;
            }
            if (VALOR == 191) {
                int objecte_Referència = 빼기(2); if (객체유효(objecte_Referència)) { if (힙[objecte_Referència] != 9) error_VALOR("athrow requires supported Throwable"); else { 던진객체 = objecte_Referència; s_ha_produït_un_error = true; } }
                continue;
            }
            if (VALOR == 192 || VALOR == 193) {
                int 이름상수 = nom_de_classe_SMS(명상수()), objecte_Referència = 빼기(2); boolean COINCIDEIX = 맞는객체(objecte_Referència, 이름상수);
                if (VALOR == 193) 넣기(objecte_Referència != 0 && COINCIDEIX ? 1 : 0, 1);
                else { if (!COINCIDEIX && !s_ha_produït_un_error) error_VALOR("ClassCastException"); 넣기(objecte_Referència, 2); }
                continue;
            }
            if (VALOR == 170 || VALOR == 171) {
                int tancar_cursor = Executa_2 + 1, arxiu_INDEX = 틀함수[marc_INDEX], Clau_Referència = 빼기(1);
                while ((tancar_cursor - 함수시작[arxiu_INDEX]) % 4 != 0) tancar_cursor++;
                int objectiu_ADREÇA = 위치정수(tancar_cursor);
                if (VALOR == 170) { int 낮은값 = 위치정수(tancar_cursor + 4), 높은값 = 위치정수(tancar_cursor + 8); if (Clau_Referència >= 낮은값 && Clau_Referència <= 높은값) objectiu_ADREÇA = 위치정수(tancar_cursor + 12 + (Clau_Referència - 낮은값) * 4); }
                else { int total_COMPT = 위치정수(tancar_cursor + 4); for (int Loop_INDEX = 0; Loop_INDEX < total_COMPT; Loop_INDEX++) if (위치정수(tancar_cursor + 8 + Loop_INDEX * 8) == Clau_Referència) objectiu_ADREÇA = 위치정수(tancar_cursor + 12 + Loop_INDEX * 8); }
                moure_VALOR(Executa_2 + objectiu_ADREÇA); continue;
            }
            if (VALOR == 200) { moure_VALOR(Executa_2 + 위치정수(Executa_2 + 1)); continue; }
            if (VALOR == 194 || VALOR == 195) {
                int objecte_Referència = 빼기(2);
                if (VALOR == 195) versió_blocar(objecte_Referència);
                else if (!잠금얻기(objecte_Referència) && !s_ha_produït_un_error) { 넣기(objecte_Referència, 2); marc_càrrec[marc_INDEX] = Executa_2; }
                continue;
            }
            if (VALOR == 196) {
                int ordre_CODI = 명바(), introducció_càrrec = 명짧();
                if (ordre_CODI == 21 || ordre_CODI == 25) tancar_local(introducció_càrrec, ordre_CODI == 21 ? 1 : 2);
                else if (ordre_CODI == 54 || ordre_CODI == 58) escriure_local(introducció_càrrec, ordre_CODI == 54 ? 1 : 2);
                else if (ordre_CODI == 132) { int DELTA_VALOR = (short)명짧(); tancar_local(introducció_càrrec, 1); 넣기(빼기(1) + DELTA_VALOR, 1); escriure_local(introducció_càrrec, 1); }
                else error_VALOR("unsupported wide opcode");
                continue;
            }
            error_VALOR("unsupported bytecode");
        }
    }
    static int BUSCA_Classe_Definició(int Nom) {
        for (int Loop_INDEX = 0; Loop_INDEX < Classe_Definició_COMPT; Loop_INDEX++) if (Classe_Definició_nom[Loop_INDEX] != 0 && 같은말(Classe_Definició_nom[Loop_INDEX], Nom)) return Loop_INDEX;
        return càrrega_Classe_Definició(상문자(Nom));
    }
    static int càrrega_Classe_Definició(int nom_cadena) {
        if (!objecte_VALOR(nom_cadena, 1)) return -1;
        int durada_VALOR = 힙[nom_cadena + 1];
        if (durada_VALOR < 1 || durada_VALOR > 505 || Classe_Definició_COMPT == 16) { error_VALOR("class name/count limit"); return -1; }
        for (int Loop_INDEX = 0; Loop_INDEX < durada_VALOR; Loop_INDEX++) { int codi_de_caràcter = 힙[nom_cadena + 2 + Loop_INDEX]; nom_d_arxiu_SMS[Loop_INDEX] = codi_de_caràcter == '/' ? '.' : codi_de_caràcter; }
        nom_d_arxiu_SMS[durada_VALOR] = '.'; nom_d_arxiu_SMS[durada_VALOR + 1] = 'c'; nom_d_arxiu_SMS[durada_VALOR + 2] = 'l'; nom_d_arxiu_SMS[durada_VALOR + 3] = 'a'; nom_d_arxiu_SMS[durada_VALOR + 4] = 's'; nom_d_arxiu_SMS[durada_VALOR + 5] = 's'; nom_d_arxiu_SMS[durada_VALOR + 6] = 0;
        int Mida = usuari.tancar_arxiu(nom_d_arxiu_SMS, 임시파일);
        if (Mida < 0) { error_VALOR("ClassNotFoundException"); return -1; }
        int Classe_Definició = Classe_Definició_COMPT++; Classe_Definició_canviar_la_mida[Classe_Definició] = Mida;
        for (int Loop_INDEX = 0; Loop_INDEX < Mida; Loop_INDEX++) Fitxer[Classe_Definició * 16384 + Loop_INDEX] = 임시파일[Loop_INDEX];
        tancar_Classe(Classe_Definició); if (s_ha_produït_un_error) return -1;
        int real_dades = 상문자(Classe_Definició_nom[Classe_Definició]);
        if (!글같음(real_dades, nom_cadena, true)) { error_VALOR("class name does not match file"); return -1; }
        int 부모 = 종부모[Classe_Definició];
        if (부모 != 0 && !Word_SMS(부모, "java/lang/Object") && !Word_SMS(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 tornar_ho_a_provar_VALOR 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = BUSCA_Classe_Definició(부모);
            if (s_ha_produït_un_error || 위 < 0) return -1;
            int tancar_cursor = 위, fase_COMPT = 0;
            while (tancar_cursor >= 0 && fase_COMPT++ < 16) {
                if (tancar_cursor == Classe_Definició) { error_VALOR("cyclic inheritance"); return -1; }
                tancar_cursor = 부모종(tancar_cursor);
            }
            int 시작변위 = 종칸수[위];
            for (int arxiu_INDEX = 0; arxiu_INDEX < 칸수; arxiu_INDEX++) if (칸주인[arxiu_INDEX] == Classe_Definició && (칸권한[arxiu_INDEX] & 8) == 0) 칸위치[arxiu_INDEX] += 시작변위;
            종칸수[Classe_Definició] += 시작변위;
        }
        return Classe_Definició;
    }
    static int 부모종(int Classe_Definició) {
        int Nom = 종부모[Classe_Definició];
        for (int Loop_INDEX = 0; Loop_INDEX < Classe_Definició_COMPT; Loop_INDEX++) if (Nom != 0 && Classe_Definició_nom[Loop_INDEX] != 0 && 같은말(Classe_Definició_nom[Loop_INDEX], Nom)) return Loop_INDEX;
        return -1;
    }
    static int 함수찾기(int Classe_Definició, int Nom, int format_VALOR) {
        for (int 깊이 = 0; Classe_Definició >= 0 && 깊이 < 16; 깊이++, Classe_Definició = 부모종(Classe_Definició)) {
            for (int Loop_INDEX = 0; Loop_INDEX < 함수수; Loop_INDEX++) if (함수주인[Loop_INDEX] == Classe_Definició && 같은말(함수명[Loop_INDEX], Nom) && 같은말(함수형[Loop_INDEX], format_VALOR)) return Loop_INDEX;
        }
        return -1;
    }
    static int 이름함수(int Classe_Definició, String Nom, String format_VALOR) {
        for (int 깊이 = 0; Classe_Definició >= 0 && 깊이 < 16; 깊이++, Classe_Definició = 부모종(Classe_Definició))
            for (int Loop_INDEX = 0; Loop_INDEX < 함수수; Loop_INDEX++) if (함수주인[Loop_INDEX] == Classe_Definició && Word_SMS(함수명[Loop_INDEX], Nom) && Word_SMS(함수형[Loop_INDEX], format_VALOR)) return Loop_INDEX;
        return -1;
    }
    static int 형종류(int Nom) { return Fitxer[상가[Nom]] == 'L' || Fitxer[상가[Nom]] == '[' ? 2 : 1; }
    static boolean inicialitzar(int Classe_Definició, int ordre_Inici) {
        if (Classe_Definició < 0 || s_ha_produït_un_error) return false;
        if (Classe_Definició_Estat[Classe_Definició] == 3) { error_VALOR("NoClassDefFoundError: initialization failed"); return false; }
        if (Classe_Definició_Estat[Classe_Definició] == 1 && Classe_fil[Classe_Definició] != 현재가닥) { marc_càrrec[marc_INDEX] = ordre_Inici; canviar_sol_licitud = true; return false; }
        if (Classe_Definició_Estat[Classe_Definició] != 0) return true;
        int 위 = 부모종(Classe_Definició);
        if (위 >= 0 && !inicialitzar(위, ordre_Inici)) return false;
        Classe_Definició_Estat[Classe_Definició] = 1; Classe_fil[Classe_Definició] = 현재가닥;
        if (inicialitzar_Classe_Definició[Classe_Definició] != 0) {
            marc_càrrec[marc_INDEX] = ordre_Inici;
            호출(inicialitzar_Classe_Definició[Classe_Definició] - 1); if (!s_ha_produït_un_error) inicialitzar_marc[marc_INDEX] = Classe_Definició + 1;
            return false;
        }
        Classe_Definició_Estat[Classe_Definició] = 2; return true;
    }
    static void 필드호출(int INDEX, int Ordre, int Executa_2) {
        if (!상검사(INDEX, 9)) return;
        int propietari_VALOR = nom_de_classe_SMS(상가[INDEX]), Nom = Referència_nom(상나[INDEX]), format_VALOR = Referència_TIPUS(상나[INDEX]);
        if (Word_SMS(propietari_VALOR, "java/lang/System") && (Word_SMS(Nom, "out") || Word_SMS(Nom, "err")) && Word_SMS(format_VALOR, "Ljava/io/PrintStream;") && Ordre == 178) { 넣기(-1, 2); return; }
        int Classe_Definició = BUSCA_Classe_Definició(propietari_VALOR); if (Classe_Definició < 0 || s_ha_produït_un_error) return;
        int 찾음 = -1;
        for (int tancar_cursor = Classe_Definició, 깊이 = 0; tancar_cursor >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, tancar_cursor = 부모종(tancar_cursor))
            for (int arxiu_INDEX = 0; arxiu_INDEX < 칸수; arxiu_INDEX++) if (칸주인[arxiu_INDEX] == tancar_cursor && 같은말(칸이름[arxiu_INDEX], Nom) && 같은말(칸형[arxiu_INDEX], format_VALOR)) 찾음 = arxiu_INDEX;
        if (찾음 < 0) { error_VALOR("NoSuchFieldError"); return; }
        boolean estàtic_VALOR = Ordre == 178 || Ordre == 179;
        if (estàtic_VALOR != ((칸권한[찾음] & 8) != 0)) { error_VALOR("field static/instance mismatch"); return; }
        if (estàtic_VALOR && !inicialitzar(칸주인[찾음], Executa_2)) return;
        int TIPUS_VALOR = 형종류(format_VALOR), VALOR = 0;
        if (Ordre == 179 || Ordre == 181) VALOR = 빼기(TIPUS_VALOR);
        if (estàtic_VALOR) { if (Ordre == 178) 넣기(칸값[찾음], TIPUS_VALOR); else if (!s_ha_produït_un_error) 칸값[찾음] = VALOR; return; }
        int objecte_Referència = 빼기(2);
        if (!객체유효(objecte_Referència)) return;
        if (힙[objecte_Referència] < 32 || !종포함(힙[objecte_Referència] - 32, propietari_VALOR)) { error_VALOR("field receiver type mismatch"); return; }
        int 보관칸 = objecte_Referència + 2 + 칸위치[찾음];
        if (Ordre == 180) 넣기(힙[보관칸], TIPUS_VALOR);
        else if (!s_ha_produït_un_error) { 힙[보관칸] = VALOR; 힙참조[보관칸] = TIPUS_VALOR == 2 ? 1 : 0; }
    }
    static boolean 종포함(int Classe_Definició, int Nom) {
        for (int 중첩깊이 = 0; Classe_Definició >= 0 && 중첩깊이 < 16; 중첩깊이++, Classe_Definició = 부모종(Classe_Definició)) {
            if (같은말(Classe_Definició_nom[Classe_Definició], Nom) || (종부모[Classe_Definició] != 0 && 같은말(종부모[Classe_Definició], Nom))) return true;
            for (int interna_càrrec = 0; interna_càrrec < Classe_interfície_COMPT[Classe_Definició]; interna_càrrec++) if (같은말(Classe_interfície[Classe_Definició * 16 + interna_càrrec], Nom)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int byte_dades, boolean Camí) {
        if (첫값 == byte_dades) return true;
        if (첫값 <= 0 || byte_dades <= 0 || 힙[첫값] != 1 || 힙[byte_dades] != 1 || 힙[첫값 + 1] != 힙[byte_dades + 1]) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) {
            int X_coordenada = 힙[첫값 + 2 + Loop_INDEX], Y_coordenada = 힙[byte_dades + 2 + Loop_INDEX];
            if (Camí) { if (X_coordenada == '.') X_coordenada = '/'; if (Y_coordenada == '.') Y_coordenada = '/'; }
            if (X_coordenada != Y_coordenada) return false;
        }
        return true;
    }
    static boolean 객체유효(int objecte_Referència) {
        if (objecte_Referència == 0) { error_VALOR("NullPointerException"); return false; }
        if (objecte_Referència < 1 || objecte_Referència >= 힙끝 || 힙폭[objecte_Referència] < 2 || 힙[objecte_Referència] == 0) { error_VALOR("invalid object reference"); return false; }
        return true;
    }
    static void protegir_VALOR(int objecte_Referència) {
        if (objecte_Referència > 0 && objecte_Referència < 힙끝 && 힙폭[objecte_Referència] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = objecte_Referència;
    }
    static void mostrar_VALOR(int objecte_Referència) {
        if (objecte_Referència > 0 && objecte_Referència < 힙끝 && 힙폭[objecte_Referència] >= 2 && 힙[objecte_Referència] != 0 && 힙표시[objecte_Referència] == 0) {
            힙표시[objecte_Referència] = 1; 표시대기[mostrar_COMPT++] = objecte_Referència;
        }
    }
    static void 수거() {
        mostrar_COMPT = 0; població_COMPT++;
        for (int xec_càrrec = 1; xec_càrrec < 힙끝; xec_càrrec += 힙폭[xec_càrrec]) 힙표시[xec_càrrec] = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < cadena_Referència.length; Loop_INDEX++) mostrar_VALOR(cadena_Referència[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 칸수; Loop_INDEX++) if ((칸권한[Loop_INDEX] & 8) != 0 && 형종류(칸형[Loop_INDEX]) == 2) mostrar_VALOR(칸값[Loop_INDEX]);
        for (int 임시값 = 0; 임시값 < fil_COMPT; 임시값++) {
            mostrar_VALOR(fil_objecte[임시값]); mostrar_VALOR(fil_objectiu[임시값]);
            int 꼭대기자리 = 임시값 == 현재가닥 ? marc_INDEX : fil_marc[임시값];
            for (int arxiu_INDEX = 임시값 * 32; arxiu_INDEX <= 꼭대기자리; arxiu_INDEX++) {
                for (int interna_càrrec = 0; interna_càrrec < 함수지역[틀함수[arxiu_INDEX]]; interna_càrrec++) if (local_TIPUS[arxiu_INDEX * 128 + interna_càrrec] == 2) mostrar_VALOR(local_VALOR[arxiu_INDEX * 128 + interna_càrrec]);
                for (int interna_càrrec = 0; interna_càrrec < marc_Pila[arxiu_INDEX]; interna_càrrec++) if (스택형[arxiu_INDEX * 128 + interna_càrrec] == 2) mostrar_VALOR(스택값[arxiu_INDEX * 128 + interna_càrrec]);
            }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 화면참조.length; Loop_INDEX++) mostrar_VALOR(화면참조[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 나중수; Loop_INDEX++) mostrar_VALOR(나중실행[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 정수저장.length; Loop_INDEX++) mostrar_VALOR(정수저장[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Classe_Definició_COMPT; Loop_INDEX++) mostrar_VALOR(Classe_blocar[Loop_INDEX]);
        for (int xec_càrrec = 1; xec_càrrec < 힙끝; xec_càrrec += 힙폭[xec_càrrec]) if (잠금깊이[xec_càrrec] > 0) mostrar_VALOR(xec_càrrec);
        mostrar_VALOR(던진객체);
        for (int Loop_INDEX = 0; Loop_INDEX < 잠시수; Loop_INDEX++) mostrar_VALOR(잠시참조[Loop_INDEX]);
        while (mostrar_COMPT > 0) {
            int objecte_Referència = 표시대기[--mostrar_COMPT], Categoria_CODI = 힙[objecte_Referència];
            for (int Loop_INDEX = objecte_Referència + 2; Loop_INDEX < objecte_Referència + 힙폭[objecte_Referència]; Loop_INDEX++) if (Categoria_CODI == 3 || Categoria_CODI == 4 || 힙참조[Loop_INDEX] != 0) mostrar_VALOR(힙[Loop_INDEX]);
        }
        for (int xec_càrrec = 1; xec_càrrec < 힙끝; xec_càrrec += 힙폭[xec_càrrec]) if (힙표시[xec_càrrec] == 0) 힙[xec_càrrec] = 0;
        for (int xec_càrrec = 1; xec_càrrec < 힙끝; xec_càrrec += 힙폭[xec_càrrec]) if (힙[xec_càrrec] == 0) {
            while (xec_càrrec + 힙폭[xec_càrrec] < 힙끝 && 힙[xec_càrrec + 힙폭[xec_càrrec]] == 0) { int Següent_càrrec = xec_càrrec + 힙폭[xec_càrrec]; 힙폭[xec_càrrec] += 힙폭[Següent_càrrec]; 힙폭[Següent_càrrec] = 0; }
            if (xec_càrrec + 힙폭[xec_càrrec] == 힙끝) { 힙끝 = xec_càrrec; break; }
        }
    }
    static int 새기억(int 종류, int durada_VALOR) {
        if (durada_VALOR < 0) { error_VALOR("NegativeArraySizeException"); return 0; }
        if (durada_VALOR > 힙.length - 3) { error_VALOR("object heap exhausted"); return 0; }
        int 필요수 = durada_VALOR + 2, objecte_Referència = 0;
        if (필요수 <= 힙.length - 힙끝) { objecte_Referència = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int tancar_cursor = 1; tancar_cursor < 힙끝; tancar_cursor += 힙폭[tancar_cursor]) if (힙[tancar_cursor] == 0 && 힙폭[tancar_cursor] >= 필요수) { objecte_Referència = tancar_cursor; break; }
            if (objecte_Referència != 0) {
                int 남은길이 = 힙폭[objecte_Referència] - 필요수;
                if (남은길이 >= 2) { 힙폭[objecte_Referència + 필요수] = 남은길이; 힙[objecte_Referència + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { objecte_Referència = 힙끝; 힙끝 += 필요수; }
        }
        if (objecte_Referència == 0) { error_VALOR("object heap exhausted"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < 필요수; Loop_INDEX++) { 힙[objecte_Referència + Loop_INDEX] = 0; 힙참조[objecte_Referència + Loop_INDEX] = 0; 힙폭[objecte_Referència + Loop_INDEX] = 0; }
        MATRIU_element[objecte_Referència] = 0;
        힙폭[objecte_Referència] = 필요수; 힙[objecte_Referència] = 종류; 힙[objecte_Referència + 1] = durada_VALOR; protegir_VALOR(objecte_Referència); return objecte_Referència;
    }
    static int excepció_Classe(String 이름상수) {
        if (자바도구.같음(이름상수, "java/lang/Throwable")) return 1;
        if (자바도구.같음(이름상수, "java/lang/Exception")) return 2;
        if (자바도구.같음(이름상수, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(이름상수, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(이름상수, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(이름상수, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(이름상수, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(이름상수, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(이름상수, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(이름상수, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(이름상수, "java/io/IOException")) return 11;
        if (자바도구.같음(이름상수, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(이름상수, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(이름상수, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(이름상수, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int 예외상수(int Nom) {
        for (int Loop_INDEX = 1; Loop_INDEX <= 41; Loop_INDEX++) if (Word_SMS(Nom, excepció_nom(Loop_INDEX))) return Loop_INDEX;
        return 0;
    }
    static String excepció_nom(int compte_VALOR) {
        if (compte_VALOR == 40) return "java/lang/InterruptedException";
        if (compte_VALOR == 41) return "Català/propi/대기중단예외";
        if (compte_VALOR == 39) return "java/net/SocketException";
        if (compte_VALOR == 20) return "Català/propi/excepció";
        if (compte_VALOR == 21) return "Català/propi/실행예외";
        if (compte_VALOR == 22) return "Català/propi/E_S_excepció";
        if (compte_VALOR == 23) return "Català/propi/Espera_TIMEOUT_excepció";
        if (compte_VALOR == 24) return "Català/propi/ADREÇA_Cerca_excepció";
        if (compte_VALOR == 25) return "Català/propi/파일없음예외";
        if (compte_VALOR == 26) return "Català/propi/통신예외";
        if (compte_VALOR == 27) return "Català/propi/invàlid_arg_excepció";
        if (compte_VALOR == 28) return "Català/propi/숫자형식예외";
        if (compte_VALOR == 29) return "Català/propi/범위예외";
        if (compte_VALOR == 30) return "Català/propi/배열범위예외";
        if (compte_VALOR == 31) return "Català/propi/문자열범위예외";
        if (compte_VALOR == 32) return "Català/propi/NUL_Referència_excepció";
        if (compte_VALOR == 33) return "Català/propi/산술예외";
        if (compte_VALOR == 34) return "Català/propi/Estat_excepció";
        if (compte_VALOR == 35) return "Català/propi/TIPUS_conversió_excepció";
        if (compte_VALOR == 36) return "Català/propi/음수배열크기예외";
        if (compte_VALOR == 37) return "Català/propi/MATRIU_Store_error";
        if (compte_VALOR == 38) return "Català/propi/fil_Estat_excepció";
        if (compte_VALOR == 1) return "java/lang/Throwable"; if (compte_VALOR == 2) return "java/lang/Exception";
        if (compte_VALOR == 3) return "java/lang/RuntimeException"; if (compte_VALOR == 4) return "java/lang/ArithmeticException";
        if (compte_VALOR == 5) return "java/lang/NullPointerException"; if (compte_VALOR == 6) return "java/lang/IndexOutOfBoundsException";
        if (compte_VALOR == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (compte_VALOR == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (compte_VALOR == 9) return "java/lang/IllegalArgumentException"; if (compte_VALOR == 10) return "java/lang/NumberFormatException";
        if (compte_VALOR == 11) return "java/io/IOException"; if (compte_VALOR == 12) return "java/io/FileNotFoundException";
        if (compte_VALOR == 17) return "java/lang/ArrayStoreException";
        if (compte_VALOR == 18) return "java/net/UnknownHostException";
        if (compte_VALOR == 19) return "java/net/SocketTimeoutException";
        if (compte_VALOR == 16) return "java/lang/IllegalThreadStateException";
        if (compte_VALOR == 13) return "java/lang/IllegalStateException"; if (compte_VALOR == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int compte_VALOR) {
        if (compte_VALOR == 40) return 2;
        if (compte_VALOR == 41) return 40;
        if (compte_VALOR == 39) return 11;
        if (compte_VALOR == 1) return 0;
        if (compte_VALOR == 2) return 1;
        if (compte_VALOR == 3) return 2;
        if (compte_VALOR == 4) return 3;
        if (compte_VALOR == 5) return 3;
        if (compte_VALOR == 6) return 3;
        if (compte_VALOR == 7) return 6;
        if (compte_VALOR == 8) return 6;
        if (compte_VALOR == 9) return 3;
        if (compte_VALOR == 10) return 9;
        if (compte_VALOR == 11) return 2;
        if (compte_VALOR == 12) return 11;
        if (compte_VALOR == 13) return 3;
        if (compte_VALOR == 14) return 3;
        if (compte_VALOR == 15) return 3;
        if (compte_VALOR == 16) return 9;
        if (compte_VALOR == 17) return 3;
        if (compte_VALOR == 18) return 11;
        if (compte_VALOR == 19) return 11;
        if (compte_VALOR == 20) return 2;
        if (compte_VALOR == 21) return 3;
        if (compte_VALOR == 22) return 11;
        if (compte_VALOR == 23) return 22;
        if (compte_VALOR == 24) return 22;
        if (compte_VALOR == 25) return 22;
        if (compte_VALOR == 26) return 22;
        if (compte_VALOR == 27) return 9;
        if (compte_VALOR == 28) return 27;
        if (compte_VALOR == 29) return 6;
        if (compte_VALOR == 30) return 29;
        if (compte_VALOR == 31) return 29;
        if (compte_VALOR == 32) return 5;
        if (compte_VALOR == 33) return 4;
        if (compte_VALOR == 34) return 13;
        if (compte_VALOR == 35) return 14;
        if (compte_VALOR == 36) return 15;
        if (compte_VALOR == 37) return 17;
        if (compte_VALOR == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int real_VALOR, int 요구값) {
        for (int 깊이 = 0; real_VALOR != 0 && 깊이 < 16; 깊이++, real_VALOR = 예외부모(real_VALOR))
            if (real_VALOR == 요구값) return true;
        return false;
    }
    static void 예외던짐(int compte_VALOR, String LLEGIU_ME_Referència) {
        int objecte_Referència = 새기억(9, 2); if (s_ha_produït_un_error) return;
        힙[objecte_Referència + 2] = compte_VALOR; 힙[objecte_Referència + 3] = allotjar_caràcter(LLEGIU_ME_Referència); 힙참조[objecte_Referència + 3] = 1;
        던진객체 = objecte_Referència; s_ha_produït_un_error = true;
    }
    static boolean 맞는객체(int objecte_Referència, int Nom) {
        if (objecte_Referència == 0) return true;
        if (!객체유효(objecte_Referència)) return false;
        int Categoria_CODI = 힙[objecte_Referència];
        if (Word_SMS(Nom, "java/lang/Object")) return true;
        if (Categoria_CODI >= 32) return 종포함(Categoria_CODI - 32, Nom);
        if (Categoria_CODI == 9) { int objectiu_ADREÇA = 예외상수(Nom); return objectiu_ADREÇA != 0 && 예외포함(힙[objecte_Referència + 2], objectiu_ADREÇA); }
        if (Categoria_CODI == 1) return Word_SMS(Nom, "java/lang/String") || Word_SMS(Nom, "java/lang/CharSequence");
        if (Categoria_CODI == 4) return Word_SMS(Nom, "java/lang/StringBuilder") || Word_SMS(Nom, "java/lang/CharSequence");
        if (Categoria_CODI == 10) return Word_SMS(Nom, "java/util/ArrayList") || Word_SMS(Nom, "java/util/List");
        if (Categoria_CODI == 11) return Word_SMS(Nom, "java/util/HashMap") || Word_SMS(Nom, "java/util/Map");
        if (Categoria_CODI == 12) return Word_SMS(Nom, "java/lang/Integer") || Word_SMS(Nom, "java/lang/Number");
        if (Categoria_CODI >= 24 && Categoria_CODI <= 28 && 힙[objecte_Referència + 13] != 0) return 한국어화면종(Nom) == Categoria_CODI || Word_SMS(Nom, "Català/propi/화면구성요소");
        if (Categoria_CODI >= 24 && Categoria_CODI <= 28) return (한국어화면종(Nom) == 0 && 화면종(Nom) == Categoria_CODI) || Word_SMS(Nom, "java/awt/Component") || Word_SMS(Nom, "java/awt/Container") || Word_SMS(Nom, "javax/swing/JComponent");
        if (Categoria_CODI == 29) return Word_SMS(Nom, 힙[objecte_Referència + 3] != 0 ? "Català/propi/동작알림" : "java/awt/event/ActionEvent");
        if (Categoria_CODI == 30) return Word_SMS(Nom, "java/awt/FlowLayout") || Word_SMS(Nom, "java/awt/LayoutManager");
        if (Categoria_CODI == 17) return Word_SMS(Nom, "java/net/Socket");
        if (Categoria_CODI == 18) return Word_SMS(Nom, "java/net/ServerSocket");
        if (Categoria_CODI == 19) return Word_SMS(Nom, 힙[objecte_Referència + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (Categoria_CODI == 14) return Word_SMS(Nom, "java/net/InetAddress");
        if (Categoria_CODI == 15) return Word_SMS(Nom, "java/net/DatagramSocket");
        if (Categoria_CODI == 16) return Word_SMS(Nom, "java/net/DatagramPacket");
        if (Categoria_CODI == 13) return Word_SMS(Nom, 힙[objecte_Referència + 3] != 0 ? "Català/propi/작업가닥" : "java/lang/Thread");
        if (Categoria_CODI == 2) return Word_SMS(Nom, "[I"); if (Categoria_CODI == 20) return Word_SMS(Nom, "[B"); if (Categoria_CODI == 21) return Word_SMS(Nom, "[Z");
        if (Categoria_CODI == 22) return Word_SMS(Nom, "[C"); if (Categoria_CODI == 23) return Word_SMS(Nom, "[S");
        if (Categoria_CODI != 3) return false;
        if (Word_SMS(Nom, "[Ljava/lang/Object;")) return true;
        int component = MATRIU_element[objecte_Referència];
        if (component == -1) return Word_SMS(Nom, "[Ljava/lang/String;") || Word_SMS(Nom, "[Ljava/lang/CharSequence;");
        if (component == 0) return false;
        if (배열종비교(component, Nom)) return true;
        if ((Word_SMS(component, "java/lang/String") || Word_SMS(component, "java/lang/StringBuilder")) && Word_SMS(Nom, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDEX = 0; Loop_INDEX < Classe_Definició_COMPT; Loop_INDEX++) if (같은말(Classe_Definició_nom[Loop_INDEX], component)) {
            for (int codi_de_caràcter = Loop_INDEX, 중첩깊이 = 0; codi_de_caràcter >= 0 && 중첩깊이 < 16; 중첩깊이++, codi_de_caràcter = 부모종(codi_de_caràcter)) {
                if (배열종비교(종부모[codi_de_caràcter], Nom)) return true;
                for (int interna_càrrec = 0; interna_càrrec < Classe_interfície_COMPT[codi_de_caràcter]; interna_càrrec++) if (배열종비교(Classe_interfície[codi_de_caràcter * 16 + interna_càrrec], Nom)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int 이름상수, int 형식참조) {
        int xec_càrrec = 상가[형식참조], introducció_COMPT = 상나[형식참조];
        if (이름상수 == 0 || introducció_COMPT < 4 || Fitxer[xec_càrrec] != '[' || Fitxer[xec_càrrec + 1] != 'L' || Fitxer[xec_càrrec + introducció_COMPT - 1] != ';' || 상나[이름상수] != introducció_COMPT - 3) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < introducció_COMPT - 3; Loop_INDEX++) if (Fitxer[상가[이름상수] + Loop_INDEX] != Fitxer[xec_càrrec + 2 + Loop_INDEX]) return false;
        return true;
    }
    static void control_excepció() {
        if (던진객체 == 0) return;
        s_ha_produït_un_error = false;
        while (marc_INDEX >= 현재가닥 * 32) {
            int arxiu_INDEX = 틀함수[marc_INDEX], tancar_cursor = marc_instrucció[marc_INDEX];
            for (int Loop_INDEX = 0; Loop_INDEX < 잡기수; Loop_INDEX++) if (잡기함수[Loop_INDEX] == arxiu_INDEX && tancar_cursor >= 잡기시작[Loop_INDEX] && tancar_cursor < 잡기끝[Loop_INDEX]
                && (잡기종[Loop_INDEX] == 0 || 맞는객체(던진객체, 잡기종[Loop_INDEX]))) {
                marc_càrrec[marc_INDEX] = 잡기위치[Loop_INDEX]; marc_Pila[marc_INDEX] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (inicialitzar_marc[marc_INDEX] != 0) Classe_Definició_Estat[inicialitzar_marc[marc_INDEX] - 1] = 3;
            if (marc_blocar[marc_INDEX] != 0) { versió_blocar(marc_blocar[marc_INDEX]); marc_blocar[marc_INDEX] = 0; }
            marc_INDEX--;
        }
        usuari.Escriptura("Uncaught ");
        if (힙[던진객체] == 9) { usuari.Escriptura(excepció_nom(힙[던진객체 + 2])); usuari.Escriptura(": "); escriure_SMS(힙[던진객체 + 3]); }
        else usuari.Escriptura("user exception");
        usuari.escriure_caràcter_VALOR(10); 던진객체 = 0; s_ha_produït_un_error = true;
    }
    // 이 JVM의 스택 항목은 현재 category-1(int/reference)만 허용한다.
    static void Pila_instrucció(int ordre_CODI) {
        int 첫값 = 빼기(0), 첫형식 = tornar_les_tasques_TIPUS;
        if (ordre_CODI == 87) return;
        if (ordre_CODI == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int byte_dades = 빼기(0), SEGON_format = tornar_les_tasques_TIPUS;
        if (ordre_CODI == 88) return;
        if (ordre_CODI == 90) { 넣기(첫값, 첫형식); 넣기(byte_dades, SEGON_format); 넣기(첫값, 첫형식); return; }
        if (ordre_CODI == 92) { 넣기(byte_dades, SEGON_format); 넣기(첫값, 첫형식); 넣기(byte_dades, SEGON_format); 넣기(첫값, 첫형식); return; }
        if (ordre_CODI == 95) { 넣기(첫값, 첫형식); 넣기(byte_dades, SEGON_format); return; }
        int codi_de_caràcter = 빼기(0), 셋째형식 = tornar_les_tasques_TIPUS;
        if (ordre_CODI == 91) { 넣기(첫값, 첫형식); 넣기(codi_de_caràcter, 셋째형식); 넣기(byte_dades, SEGON_format); 넣기(첫값, 첫형식); return; }
        if (ordre_CODI == 93) { 넣기(byte_dades, SEGON_format); 넣기(첫값, 첫형식); 넣기(codi_de_caràcter, 셋째형식); 넣기(byte_dades, SEGON_format); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = tornar_les_tasques_TIPUS;
        넣기(byte_dades, SEGON_format); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(codi_de_caràcter, 셋째형식); 넣기(byte_dades, SEGON_format); 넣기(첫값, 첫형식);
    }
    static void 새객체(int 이름상수, int 시작점) {
        int Categoria_CODI = 0, 유효길이 = 0, excepció_Referència = 예외상수(이름상수);
        if (Word_SMS(이름상수, "java/lang/StringBuilder")) { Categoria_CODI = 4; 유효길이 = 1; }
        if (Word_SMS(이름상수, "java/io/FileInputStream")) { Categoria_CODI = 5; 유효길이 = 2; }
        if (Word_SMS(이름상수, "java/io/FileOutputStream")) { Categoria_CODI = 6; 유효길이 = 2; }
        if (excepció_Referència != 0) { Categoria_CODI = 9; 유효길이 = 2; }
        if (Word_SMS(이름상수, "java/util/ArrayList")) { Categoria_CODI = 10; 유효길이 = 2; }
        if (Word_SMS(이름상수, "java/util/HashMap")) { Categoria_CODI = 11; 유효길이 = 2; }
        if (Word_SMS(이름상수, "java/lang/Integer")) { Categoria_CODI = 12; 유효길이 = 1; }
        if (Word_SMS(이름상수, "java/net/Socket")) { Categoria_CODI = 17; 유효길이 = 5; }
        if (Word_SMS(이름상수, "java/net/ServerSocket")) { Categoria_CODI = 18; 유효길이 = 5; }
        if (Word_SMS(이름상수, "java/net/DatagramSocket")) { Categoria_CODI = 15; 유효길이 = 3; }
        if (Word_SMS(이름상수, "java/net/DatagramPacket")) { Categoria_CODI = 16; 유효길이 = 4; }
        if (Word_SMS(이름상수, "java/lang/Thread") || Word_SMS(이름상수, "Català/propi/작업가닥")) { Categoria_CODI = 13; 유효길이 = 2; }
        if (Word_SMS(이름상수, "java/lang/Object")) { Categoria_CODI = 8; }
        if (Categoria_CODI == 0 && 화면종(이름상수) != 0) { Categoria_CODI = 화면종(이름상수); 유효길이 = 12; }
        if (Categoria_CODI == 0) {
            int codi_de_caràcter = BUSCA_Classe_Definició(이름상수); if (codi_de_caràcter < 0 || s_ha_produït_un_error || !inicialitzar(codi_de_caràcter, 시작점)) return;
            Categoria_CODI = 32 + codi_de_caràcter; 유효길이 = 종칸수[codi_de_caràcter];
        }
        int objecte_Referència = assignar_Emmagatzematge(Categoria_CODI, 유효길이); if (s_ha_produït_un_error) return;
        if (Categoria_CODI == 13 && Word_SMS(이름상수, "Català/propi/작업가닥")) 힙[objecte_Referència + 3] = 1;
        if (Categoria_CODI >= 24 && Categoria_CODI <= 28 && 한국어화면종(이름상수) != 0) 힙[objecte_Referència + 13] = 1;
        if (Categoria_CODI == 5 || Categoria_CODI == 6 || Categoria_CODI == 15 || Categoria_CODI == 17 || Categoria_CODI == 18) 힙[objecte_Referència + 2] = -1;
        if (Categoria_CODI == 9) 힙[objecte_Referència + 2] = excepció_Referència;
        넣기(objecte_Referència, 2);
    }
    static boolean 값같음(int 첫값, int byte_dades) {
        if (첫값 == byte_dades) return true;
        if (첫값 == 0 || byte_dades == 0 || 첫값 < 0 || byte_dades < 0 || 첫값 >= 힙끝 || byte_dades >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[byte_dades] == 1) return 글같음(첫값, byte_dades, false);
        return 힙[첫값] == 12 && 힙[byte_dades] == 12 && 힙[첫값 + 2] == 힙[byte_dades + 2];
    }
    static int 글조각(int objecte_Referència, int Inici_càrrec, int finalitzar_càrrec) {
        if (!objecte_VALOR(objecte_Referència, 1)) return 0;
        if (Inici_càrrec < 0 || finalitzar_càrrec < Inici_càrrec || finalitzar_càrrec > 힙[objecte_Referència + 1]) { error_VALOR("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = assignar_Emmagatzematge(1, finalitzar_càrrec - Inici_càrrec); if (s_ha_produït_un_error) return 0;
        for (int Loop_INDEX = Inici_càrrec; Loop_INDEX < finalitzar_càrrec; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX - Inici_càrrec] = 힙[objecte_Referència + 2 + Loop_INDEX];
        return 반환값;
    }
    static int unió_SMS(int 첫값, int byte_dades) {
        if (!objecte_VALOR(첫값, 1) || !objecte_VALOR(byte_dades, 1)) return 0;
        int introducció_COMPT = 힙[첫값 + 1], 함수번호 = 힙[byte_dades + 1], 반환값 = assignar_Emmagatzematge(1, introducció_COMPT + 함수번호); if (s_ha_produït_un_error) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < introducció_COMPT; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 힙[첫값 + 2 + Loop_INDEX];
        for (int Loop_INDEX = 0; Loop_INDEX < 함수번호; Loop_INDEX++) 힙[반환값 + 2 + introducció_COMPT + Loop_INDEX] = 힙[byte_dades + 2 + Loop_INDEX];
        return 반환값;
    }
    static boolean 기본호출(int propietari, int 이름상수, int 서술상수, int ordre_CODI) {
        if (Word_SMS(propietari, "Català/propi/실행인수") && ordre_CODI == 184) {
            if (Word_SMS(이름상수, "element_COMPT") && Word_SMS(서술상수, "()I")) { 넣기(usuari.인수개수() - 1, 1); return true; }
            if (Word_SMS(이름상수, "SMS") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= usuari.인수개수() - 1) 예외던짐(29, "Executa_ordre 인수 범위를 벗어났습니다");
                else 넣기(allotjar_caràcter(usuari.인수(순번 + 1)), 2);
                return true;
            }
            error_VALOR("지원하지 않는 Català Executa_ordre 인수 호출"); return true;
        }
        if (Word_SMS(propietari, "Català/propi/작업가닥")) { Procés_fil(이름상수, 서술상수, ordre_CODI, true); return true; }
        if (한국어화면소유(propietari)) { 한국어화면호출(propietari, 이름상수, 서술상수, ordre_CODI); return true; }
        if (화면소유(propietari)) { 화면호출(propietari, 이름상수, 서술상수, ordre_CODI); return true; }
        if (Word_SMS(propietari, "java/net/Socket") || Word_SMS(propietari, "java/net/ServerSocket") || Word_SMS(propietari, "java/io/InputStream") || Word_SMS(propietari, "java/io/OutputStream")) { 흐름호출(propietari, 이름상수, 서술상수, ordre_CODI); return true; }
        if (Word_SMS(propietari, "Català/propi/nucli_VALOR") && ordre_CODI == 184) {
            if (Word_SMS(이름상수, "화면너비") && Word_SMS(서술상수, "()I")) { 넣기(usuari.화면너비(), 1); return true; }
            if (Word_SMS(이름상수, "화면높이") && Word_SMS(서술상수, "()I")) { 넣기(usuari.화면높이(), 1); return true; }
            if (Word_SMS(이름상수, "밀리초") && Word_SMS(서술상수, "()I")) { 넣기(usuari.밀리초(), 1); return true; }
            if (Word_SMS(이름상수, "그림대기") && Word_SMS(서술상수, "()I")) { 넣기(usuari.그림대기(), 1); return true; }
            if (Word_SMS(이름상수, "사각형") && Word_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), Y_coordenada = 빼기(1), X_coordenada = 빼기(1); 넣기(usuari.사각형(X_coordenada, Y_coordenada, 너비, 높이, 색상), 1); return true; }
        }
        if (Word_SMS(propietari, "java/net/InetAddress") || Word_SMS(propietari, "java/net/DatagramPacket") || Word_SMS(propietari, "java/net/DatagramSocket")) { 통신호출(propietari, 이름상수, 서술상수, ordre_CODI); return true; }
        if (Word_SMS(propietari, "java/lang/Thread")) { 가닥호출(이름상수, 서술상수, ordre_CODI); return true; }
        if (Word_SMS(propietari, "java/lang/Object")) {
            if (Word_SMS(이름상수, "<init>") && Word_SMS(서술상수, "()V") && ordre_CODI == 183) { 객체유효(빼기(2)); return true; }
            if (Word_SMS(이름상수, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int byte_dades = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == byte_dades ? 1 : 0, 1); return true; }
        }
        if (예외상수(propietari) != 0) {
            if (Word_SMS(이름상수, "<init>") && ordre_CODI == 183 && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int sol_licitar = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), objecte_Referència = 빼기(2);
                if (objecte_VALOR(objecte_Referència, 9)) { 힙[objecte_Referència + 3] = sol_licitar; 힙참조[objecte_Referència + 3] = 1; } return true;
            }
            if ((Word_SMS(이름상수, "getMessage") || Word_SMS(이름상수, "설명")) && Word_SMS(서술상수, "()Ljava/lang/String;")) { int objecte_Referència = 빼기(2); if (objecte_VALOR(objecte_Referència, 9)) 넣기(힙[objecte_Referència + 3], 2); return true; }
        }
        if (Word_SMS(propietari, "java/lang/String")) {
            if (ordre_CODI == 182 && Word_SMS(이름상수, "getBytes") && (Word_SMS(서술상수, "()[B") || Word_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int codificació_nom = Word_SMS(서술상수, "()[B") ? 0 : 빼기(2), objecte_Referència = 빼기(2);
                if (!objecte_VALOR(objecte_Referència, 1)) return true;
                if (codificació_nom != 0 && !글같음(codificació_nom, allotjar_caràcter("UTF-8"), false) && !글같음(codificació_nom, allotjar_caràcter("UTF8"), false) && !글같음(codificació_nom, allotjar_caràcter("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int introducció_COMPT = 힙[objecte_Referència + 1], 반환값 = assignar_Emmagatzematge(20, introducció_COMPT * 3), 사용수 = 0; if (s_ha_produït_un_error) return true;
                for (int interna_càrrec = 0; interna_càrrec < introducció_COMPT; interna_càrrec++) {
                    int codi_de_caràcter = 힙[objecte_Referència + 2 + interna_càrrec];
                    if (codi_de_caràcter >= 0xd800 && codi_de_caràcter <= 0xdbff && interna_càrrec + 1 < introducció_COMPT && 힙[objecte_Referència + 3 + interna_càrrec] >= 0xdc00 && 힙[objecte_Referència + 3 + interna_càrrec] <= 0xdfff) codi_de_caràcter = 0x10000 + ((codi_de_caràcter - 0xd800) << 10) + 힙[objecte_Referència + 2 + ++interna_càrrec] - 0xdc00;
                    else if (codi_de_caràcter >= 0xd800 && codi_de_caràcter <= 0xdfff) codi_de_caràcter = '?';
                    if (codi_de_caràcter < 128) 힙[반환값 + 2 + 사용수++] = codi_de_caràcter;
                    else { int byte_COMPT = codi_de_caràcter < 2048 ? 2 : codi_de_caràcter < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((byte_COMPT == 2 ? 192 : byte_COMPT == 3 ? 224 : 240) | codi_de_caràcter >> (6 * (byte_COMPT - 1))); for (int Comparació_càrrec = byte_COMPT - 1; Comparació_càrrec > 0; Comparació_càrrec--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | codi_de_caràcter >> (6 * (Comparació_càrrec - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (ordre_CODI == 184 && Word_SMS(이름상수, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(dígit_caràcter(빼기(1)), 2); return true; }
            if (ordre_CODI != 182) return false;
            if (Word_SMS(이름상수, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int byte_dades = 빼기(2), 첫값 = 빼기(2); if (objecte_VALOR(첫값, 1)) 넣기(글같음(첫값, byte_dades, false) ? 1 : 0, 1); return true; }
            if (Word_SMS(이름상수, "isEmpty") && Word_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (objecte_VALOR(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_SMS(이름상수, "substring") && (Word_SMS(서술상수, "(I)Ljava/lang/String;") || Word_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SEGON_VALOR = Word_SMS(서술상수, "(II)Ljava/lang/String;"); int finalitzar_càrrec = SEGON_VALOR ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (objecte_VALOR(첫값, 1)) 넣기(글조각(첫값, 시작점, SEGON_VALOR ? finalitzar_càrrec : 힙[첫값 + 1]), 2); return true;
            }
            if (Word_SMS(이름상수, "concat") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int byte_dades = 빼기(2), 첫값 = 빼기(2); 넣기(unió_SMS(첫값, byte_dades), 2); return true; }
            if (Word_SMS(이름상수, "hashCode") && Word_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), hash_VALOR = 0; if (objecte_VALOR(첫값, 1)) { for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) hash_VALOR = hash_VALOR * 31 + 힙[첫값 + 2 + Loop_INDEX]; 넣기(hash_VALOR, 1); } return true; }
            if (Word_SMS(이름상수, "toString") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (objecte_VALOR(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_SMS(propietari, "java/lang/Integer")) {
            if (ordre_CODI == 184 && Word_SMS(이름상수, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int dades_VALOR = 빼기(1), objecte_Referència = dades_VALOR >= -128 && dades_VALOR <= 127 ? 정수저장[dades_VALOR + 128] : 0; if (objecte_Referència == 0) { objecte_Referència = assignar_Emmagatzematge(12, 1); if (!s_ha_produït_un_error) { 힙[objecte_Referència + 2] = dades_VALOR; if (dades_VALOR >= -128 && dades_VALOR <= 127) 정수저장[dades_VALOR + 128] = objecte_Referència; } } 넣기(objecte_Referència, 2); return true; }
            if (ordre_CODI == 183 && Word_SMS(이름상수, "<init>") && Word_SMS(서술상수, "(I)V")) { int dades_VALOR = 빼기(1), objecte_Referència = 빼기(2); if (objecte_VALOR(objecte_Referència, 12)) 힙[objecte_Referència + 2] = dades_VALOR; return true; }
            if (ordre_CODI == 182 && Word_SMS(이름상수, "intValue") && Word_SMS(서술상수, "()I")) { int objecte_Referència = 빼기(2); if (objecte_VALOR(objecte_Referència, 12)) 넣기(힙[objecte_Referència + 2], 1); return true; }
            if (ordre_CODI == 184 && Word_SMS(이름상수, "toString") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(dígit_caràcter(빼기(1)), 2); return true; }
        }
        if (Word_SMS(propietari, "java/lang/Math") && ordre_CODI == 184) {
            if (Word_SMS(이름상수, "abs") && Word_SMS(서술상수, "(I)I")) { int tancar_VALOR = 빼기(1); 넣기(tancar_VALOR < 0 ? -tancar_VALOR : tancar_VALOR, 1); return true; }
            if ((Word_SMS(이름상수, "min") || Word_SMS(이름상수, "max")) && Word_SMS(서술상수, "(II)I")) { int byte_dades = 빼기(1), 첫값 = 빼기(1); 넣기(Word_SMS(이름상수, "min") ? (첫값 < byte_dades ? 첫값 : byte_dades) : (첫값 > byte_dades ? 첫값 : byte_dades), 1); return true; }
        }
        if (Word_SMS(propietari, "java/lang/System") && ordre_CODI == 184) {
            if (Word_SMS(이름상수, "gc") && Word_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Word_SMS(이름상수, "arraycopy") && Word_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int introducció_COMPT = 빼기(1), destinació_VALOR_INDEX = 빼기(1), byte_dades = 빼기(2), Inici_càrrec = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(byte_dades)) {
                    int Categoria_CODI = 힙[첫값];
                    if (힙[byte_dades] != Categoria_CODI || (Categoria_CODI != 2 && Categoria_CODI != 3 && (Categoria_CODI < 20 || Categoria_CODI > 23))) error_VALOR("arraycopy type mismatch");
                    else if (introducció_COMPT < 0 || Inici_càrrec < 0 || destinació_VALOR_INDEX < 0 || Inici_càrrec > 힙[첫값 + 1] - introducció_COMPT || destinació_VALOR_INDEX > 힙[byte_dades + 1] - introducció_COMPT) error_VALOR("ArrayIndexOutOfBoundsException");
                    else if (첫값 == byte_dades && destinació_VALOR_INDEX > Inici_càrrec) { for (int Loop_INDEX = introducció_COMPT - 1; Loop_INDEX >= 0; Loop_INDEX--) 힙[byte_dades + 2 + destinació_VALOR_INDEX + Loop_INDEX] = 힙[첫값 + 2 + Inici_càrrec + Loop_INDEX]; }
                    else { for (int Loop_INDEX = 0; Loop_INDEX < introducció_COMPT && !s_ha_produït_un_error; Loop_INDEX++) { int dades_VALOR = 힙[첫값 + 2 + Inici_càrrec + Loop_INDEX]; if (Categoria_CODI != 3 || 배열저장가능(byte_dades, dades_VALOR)) 힙[byte_dades + 2 + destinació_VALOR_INDEX + Loop_INDEX] = dades_VALOR; } }
                }
                return true;
            }
        }
        if (Word_SMS(propietari, "java/util/ArrayList") || Word_SMS(propietari, "java/util/List") || Word_SMS(propietari, "java/util/HashMap") || Word_SMS(propietari, "java/util/Map")) {
            모음호출(propietari, 이름상수, 서술상수, ordre_CODI); return true;
        }
        return false;
    }
    static void 모음늘리기(int objecte_Referència, int 필요수) {
        int 이전값 = 힙[objecte_Referència + 2], capacitat_dades = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (capacitat_dades >= 필요수) return;
        int Següent_càrrec = capacitat_dades < 8 ? 8 : capacitat_dades * 2; if (Següent_càrrec < 필요수) Següent_càrrec = 필요수;
        int dades_MATRIU = assignar_Emmagatzematge(3, Següent_càrrec); if (s_ha_produït_un_error) return;
        for (int Loop_INDEX = 0; Loop_INDEX < capacitat_dades; Loop_INDEX++) 힙[dades_MATRIU + 2 + Loop_INDEX] = 힙[이전값 + 2 + Loop_INDEX];
        힙[objecte_Referència + 2] = dades_MATRIU; 힙참조[objecte_Referència + 2] = 1;
    }
    static void 모음호출(int propietari, int 이름상수, int 서술상수, int ordre_CODI) {
        boolean 대응참조 = Word_SMS(propietari, "java/util/HashMap") || Word_SMS(propietari, "java/util/Map"); int Categoria_CODI = 대응참조 ? 11 : 10;
        if (Word_SMS(이름상수, "<init>") && ordre_CODI == 183 && Word_SMS(서술상수, "()V")) { int objecte_Referència = 빼기(2); if (objecte_VALOR(objecte_Referència, Categoria_CODI)) 모음늘리기(objecte_Referència, 8); return; }
        if (ordre_CODI != 182 && ordre_CODI != 185) { error_VALOR("invalid collection invocation"); return; }
        if (Word_SMS(이름상수, "size") && Word_SMS(서술상수, "()I") || Word_SMS(이름상수, "isEmpty") && Word_SMS(서술상수, "()Z")) {
            int objecte_Referència = 빼기(2); if (objecte_VALOR(objecte_Referència, Categoria_CODI)) 넣기(Word_SMS(이름상수, "size") ? 힙[objecte_Referència + 3] : 힙[objecte_Referència + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_SMS(이름상수, "clear") && Word_SMS(서술상수, "()V")) { int objecte_Referència = 빼기(2); if (objecte_VALOR(objecte_Referència, Categoria_CODI)) { int dades_MATRIU = 힙[objecte_Referència + 2]; for (int Loop_INDEX = 0; Loop_INDEX < 힙[dades_MATRIU + 1]; Loop_INDEX++) 힙[dades_MATRIU + 2 + Loop_INDEX] = 0; 힙[objecte_Referència + 3] = 0; } return; }
        if (!대응참조 && Word_SMS(이름상수, "add") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int dades_VALOR = 빼기(2), objecte_Referència = 빼기(2); if (!objecte_VALOR(objecte_Referència, 10)) return;
            int introducció_COMPT = 힙[objecte_Referència + 3]; 모음늘리기(objecte_Referència, introducció_COMPT + 1); if (!s_ha_produït_un_error) { 힙[힙[objecte_Referència + 2] + 2 + introducció_COMPT] = dades_VALOR; 힙[objecte_Referència + 3] = introducció_COMPT + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_SMS(이름상수, "get") || Word_SMS(이름상수, "remove")) && Word_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Word_SMS(이름상수, "set") && Word_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = Word_SMS(이름상수, "set"); int dades_VALOR = 지정여부 ? 빼기(2) : 0, introducció_càrrec = 빼기(1), objecte_Referència = 빼기(2);
            if (!objecte_VALOR(objecte_Referència, 10)) return;
            int introducció_COMPT = 힙[objecte_Referència + 3], dades_MATRIU = 힙[objecte_Referència + 2];
            if (introducció_càrrec < 0 || introducció_càrrec >= introducció_COMPT) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[dades_MATRIU + 2 + introducció_càrrec];
            if (지정여부) 힙[dades_MATRIU + 2 + introducció_càrrec] = dades_VALOR;
            if (Word_SMS(이름상수, "remove")) { for (int Loop_INDEX = introducció_càrrec + 1; Loop_INDEX < introducció_COMPT; Loop_INDEX++) 힙[dades_MATRIU + 1 + Loop_INDEX] = 힙[dades_MATRIU + 2 + Loop_INDEX]; 힙[dades_MATRIU + 1 + introducció_COMPT] = 0; 힙[objecte_Referència + 3] = introducció_COMPT - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Word_SMS(이름상수, "get") || Word_SMS(이름상수, "remove")) && Word_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(이름상수, "put") && Word_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(이름상수, "containsKey") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_SMS(이름상수, "put"), suprimir = Word_SMS(이름상수, "remove");
            int dades_VALOR = 넣기여부 ? 빼기(2) : 0, Clau_Referència = 빼기(2), objecte_Referència = 빼기(2); if (!objecte_VALOR(objecte_Referència, 11)) return;
            int introducció_COMPT = 힙[objecte_Referència + 3], dades_MATRIU = 힙[objecte_Referència + 2], 찾은여부 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < introducció_COMPT; Loop_INDEX++) if (값같음(Clau_Referència, 힙[dades_MATRIU + 2 + 2 * Loop_INDEX])) { 찾은여부 = Loop_INDEX; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[dades_MATRIU + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(objecte_Referència, (introducció_COMPT + 1) * 2); dades_MATRIU = 힙[objecte_Referència + 2]; 찾은여부 = introducció_COMPT; if (!s_ha_produït_un_error) 힙[objecte_Referència + 3] = introducció_COMPT + 1; }
                if (!s_ha_produït_un_error) { 힙[dades_MATRIU + 2 + 2 * 찾은여부] = Clau_Referència; 힙[dades_MATRIU + 3 + 2 * 찾은여부] = dades_VALOR; }
            }
            if (suprimir && 찾은여부 >= 0) { for (int Loop_INDEX = 찾은여부 + 1; Loop_INDEX < introducció_COMPT; Loop_INDEX++) { 힙[dades_MATRIU + 2 * Loop_INDEX] = 힙[dades_MATRIU + 2 + 2 * Loop_INDEX]; 힙[dades_MATRIU + 1 + 2 * Loop_INDEX] = 힙[dades_MATRIU + 3 + 2 * Loop_INDEX]; } 힙[dades_MATRIU + 2 * introducció_COMPT] = 0; 힙[dades_MATRIU + 1 + 2 * introducció_COMPT] = 0; 힙[objecte_Referència + 3] = introducció_COMPT - 1; }
            if (Word_SMS(이름상수, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        error_VALOR("unsupported collection method");
    }
    static boolean 잠금얻기(int objecte_Referència) {
        if (!객체유효(objecte_Referència)) return false;
        if (잠금깊이[objecte_Referència] != 0 && blocar_propietari[objecte_Referència] != 현재가닥 + 1) { canviar_sol_licitud = true; return false; }
        blocar_propietari[objecte_Referència] = 현재가닥 + 1; 잠금깊이[objecte_Referència]++; return true;
    }
    static void versió_blocar(int objecte_Referència) {
        if (!객체유효(objecte_Referència)) return;
        if (잠금깊이[objecte_Referència] == 0 || blocar_propietari[objecte_Referència] != 현재가닥 + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[objecte_Referència] == 0) blocar_propietari[objecte_Referència] = 0;
    }
    static boolean canvi_fil() {
        fil_marc[현재가닥] = marc_INDEX;
        if (marc_INDEX < 현재가닥 * 32) fil_Estat[현재가닥] = 3;
        for (int Loop_INDEX = 0; Loop_INDEX < fil_COMPT; Loop_INDEX++) if (fil_Estat[Loop_INDEX] == 2 && fil_Estat[가닥대기[Loop_INDEX]] == 3) fil_Estat[Loop_INDEX] = 1;
        for (int Loop_INDEX = 1; Loop_INDEX <= fil_COMPT; Loop_INDEX++) {
            int Següent_càrrec = (현재가닥 + Loop_INDEX) % fil_COMPT;
            if (fil_Estat[Següent_càrrec] == 1) { 현재가닥 = Següent_càrrec; marc_INDEX = fil_marc[Següent_càrrec]; canviar_sol_licitud = false; return true; }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < fil_COMPT; Loop_INDEX++) if (fil_Estat[Loop_INDEX] != 3) { error_VALOR("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int 이름상수, int 서술상수, int ordre_CODI) { Procés_fil(이름상수, 서술상수, ordre_CODI, false); }
    static void Procés_fil(int 이름상수, int 서술상수, int ordre_CODI, boolean Català) {
        if (ordre_CODI == 184 && Word_SMS(이름상수, Català ? "RENDTO_tasca" : "yield") && Word_SMS(서술상수, "()V")) { canviar_sol_licitud = true; return; }
        if (ordre_CODI == 184 && Word_SMS(이름상수, "currentThread") && Word_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(fil_objecte[현재가닥], 2); return; }
        if (ordre_CODI == 183 && Word_SMS(이름상수, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, Català ? "(LCatalà/propi/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int objectiu_ADREÇA = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), objecte_Referència = 빼기(2);
            if (!객체유효(objecte_Referència)) return;
            if (힙[objecte_Referència] == 13) { 힙[objecte_Referència + 2] = objectiu_ADREÇA; 힙참조[objecte_Referència + 2] = 1; }
            else if (objectiu_ADREÇA != 0) error_VALOR("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (ordre_CODI == 182 && (Word_SMS(이름상수, Català ? "Inici_tasca" : "start") || Word_SMS(이름상수, Català ? "기다리기" : "join")) && Word_SMS(서술상수, "()V") || ordre_CODI == 182 && Word_SMS(이름상수, Català ? "살아있는가" : "isAlive") && Word_SMS(서술상수, "()Z")) {
            int objecte_Referència = 빼기(2); if (!객체유효(objecte_Referència)) return;
            int compte_VALOR = -1; for (int Loop_INDEX = 0; Loop_INDEX < fil_COMPT; Loop_INDEX++) if (fil_objecte[Loop_INDEX] == objecte_Referència) compte_VALOR = Loop_INDEX;
            if (Word_SMS(이름상수, Català ? "살아있는가" : "isAlive")) { 넣기(compte_VALOR >= 0 && fil_Estat[compte_VALOR] != 3 ? 1 : 0, 1); return; }
            if (Word_SMS(이름상수, Català ? "기다리기" : "join")) { if (compte_VALOR >= 0 && fil_Estat[compte_VALOR] != 3) { 가닥대기[현재가닥] = compte_VALOR; fil_Estat[현재가닥] = 2; canviar_sol_licitud = true; } return; }
            if (compte_VALOR >= 0) { 예외던짐(Català ? 38 : 16, "thread already started"); return; }
            if (fil_COMPT == 4) { error_VALOR("thread limit (4 including main)"); return; }
            int objectiu_ADREÇA = 힙[objecte_Referència] == 13 ? 힙[objecte_Referència + 2] : objecte_Referència;
            int arxiu_INDEX = objectiu_ADREÇA > 0 && 힙[objectiu_ADREÇA] >= 32 ? 이름함수(힙[objectiu_ADREÇA] - 32, Català ? "Executa" : "run", "()V") : -1;
            if (objectiu_ADREÇA != 0 && arxiu_INDEX < 0) { error_VALOR("Runnable.run required"); return; }
            compte_VALOR = fil_COMPT++; fil_objecte[compte_VALOR] = objecte_Referència; fil_objectiu[compte_VALOR] = objectiu_ADREÇA;
            int marc = compte_VALOR * 32; fil_marc[compte_VALOR] = arxiu_INDEX < 0 ? marc - 1 : marc; fil_Estat[compte_VALOR] = arxiu_INDEX < 0 ? 3 : 1;
            if (arxiu_INDEX >= 0) { 틀함수[marc] = arxiu_INDEX; marc_càrrec[marc] = 함수시작[arxiu_INDEX]; local_VALOR[marc * 128] = objectiu_ADREÇA; local_TIPUS[marc * 128] = 2; }
            return;
        }
        error_VALOR("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], ADREÇA_SMS = new int[16];
    static int local_ADREÇA() { return ADREÇA_objecte(0x7f000001); }
    static int ADREÇA_objecte(int VALOR) { int objecte_Referència = assignar_Emmagatzematge(14, 1); if (!s_ha_produït_un_error) 힙[objecte_Referència + 2] = VALOR; return objecte_Referència; }
    static int 주소해독(int objecte_Referència) {
        if (objecte_Referència == 0 || 글같음(objecte_Referència, allotjar_caràcter("localhost"), false)) return 0x7f000001;
        if (!objecte_VALOR(objecte_Referència, 1)) return 0;
        int dades_VALOR = 0, total_COMPT = 0, ADREÇA_byte = 0, 자릿수 = 0, introducció_COMPT = 힙[objecte_Referència + 1];
        for (int Loop_INDEX = 0; Loop_INDEX <= introducció_COMPT; Loop_INDEX++) {
            int codi_de_caràcter = Loop_INDEX == introducció_COMPT ? '.' : 힙[objecte_Referència + 2 + Loop_INDEX];
            if (codi_de_caràcter == '.') { if (자릿수 == 0 || total_COMPT == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } dades_VALOR = dades_VALOR << 8 | ADREÇA_byte; total_COMPT++; ADREÇA_byte = 자릿수 = 0; }
            else { if (codi_de_caràcter < '0' || codi_de_caràcter > '9' || ++자릿수 > 3 || (ADREÇA_byte = ADREÇA_byte * 10 + codi_de_caràcter - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (total_COMPT != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return dades_VALOR;
    }
    static int ADREÇA_caràcter(int dades_VALOR) {
        int introducció_COMPT = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int ADREÇA_byte = dades_VALOR >>> 이동비트 & 255;
            if (ADREÇA_byte >= 100) ADREÇA_SMS[introducció_COMPT++] = '0' + ADREÇA_byte / 100;
            if (ADREÇA_byte >= 10) ADREÇA_SMS[introducció_COMPT++] = '0' + ADREÇA_byte / 10 % 10;
            ADREÇA_SMS[introducció_COMPT++] = '0' + ADREÇA_byte % 10; if (이동비트 != 0) ADREÇA_SMS[introducció_COMPT++] = '.';
        }
        int objecte_Referència = assignar_Emmagatzematge(1, introducció_COMPT); if (!s_ha_produït_un_error) for (int Loop_INDEX = 0; Loop_INDEX < introducció_COMPT; Loop_INDEX++) 힙[objecte_Referència + 2 + Loop_INDEX] = ADREÇA_SMS[Loop_INDEX]; return objecte_Referència;
    }
    static void 통신호출(int propietari, int 이름상수, int 서술상수, int ordre_CODI) {
        if (Word_SMS(propietari, "java/net/InetAddress")) {
            if (ordre_CODI == 184 && Word_SMS(이름상수, "getLoopbackAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(local_ADREÇA(), 2); return; }
            if (ordre_CODI == 184 && Word_SMS(이름상수, "getByName") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int dades_VALOR = 주소해독(빼기(2)); if (던진객체 == 0 && !s_ha_produït_un_error) 넣기(ADREÇA_objecte(dades_VALOR), 2); return;
            }
            if (ordre_CODI == 182 && Word_SMS(이름상수, "getHostAddress") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int objecte_Referència = 빼기(2); if (objecte_VALOR(objecte_Referència, 14)) 넣기(ADREÇA_caràcter(힙[objecte_Referència + 2]), 2); return; }
        }
        if (Word_SMS(propietari, "java/net/DatagramPacket")) {
            if (ordre_CODI == 183 && Word_SMS(이름상수, "<init>") && (Word_SMS(서술상수, "([BI)V") || Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean destinació_VALOR_Referència = Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int número_de_port = destinació_VALOR_Referència ? 빼기(1) : 0, ADREÇA_Referència = destinació_VALOR_Referència ? 빼기(2) : 0;
                int introducció_COMPT = 빼기(1), dades_MATRIU = 빼기(2), objecte_Referència = 빼기(2);
                if (!objecte_VALOR(objecte_Referència, 16) || !objecte_VALOR(dades_MATRIU, 20)) return;
                if (introducció_COMPT < 0 || introducció_COMPT > 힙[dades_MATRIU + 1] || número_de_port < 0 || número_de_port > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (ADREÇA_Referència != 0 && !objecte_VALOR(ADREÇA_Referència, 14)) return;
                힙[objecte_Referència + 2] = dades_MATRIU; 힙참조[objecte_Referència + 2] = 1; 힙[objecte_Referència + 3] = introducció_COMPT;
                힙[objecte_Referència + 4] = ADREÇA_Referència; 힙참조[objecte_Referència + 4] = 1; 힙[objecte_Referència + 5] = número_de_port; return;
            }
            if (ordre_CODI == 182 && Word_SMS(이름상수, "setLength") && Word_SMS(서술상수, "(I)V")) {
                int introducció_COMPT = 빼기(1), objecte_Referència = 빼기(2); if (!objecte_VALOR(objecte_Referència, 16)) return;
                if (introducció_COMPT < 0 || introducció_COMPT > 힙[힙[objecte_Referència + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[objecte_Referència + 3] = introducció_COMPT; return;
            }
            if (ordre_CODI == 182 && (Word_SMS(이름상수, "getData") && Word_SMS(서술상수, "()[B") || Word_SMS(이름상수, "getLength") && Word_SMS(서술상수, "()I") || Word_SMS(이름상수, "getAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;") || Word_SMS(이름상수, "getPort") && Word_SMS(서술상수, "()I"))) {
                int objecte_Referència = 빼기(2); if (!objecte_VALOR(objecte_Referència, 16)) return;
                int introducció_càrrec = Word_SMS(이름상수, "getData") ? 2 : Word_SMS(이름상수, "getLength") ? 3 : Word_SMS(이름상수, "getAddress") ? 4 : 5;
                넣기(힙[objecte_Referència + introducció_càrrec], introducció_càrrec == 2 || introducció_càrrec == 4 ? 2 : 1); return;
            }
        }
        if (Word_SMS(propietari, "java/net/DatagramSocket")) {
            if (ordre_CODI == 183 && Word_SMS(이름상수, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(I)V"))) {
                int número_de_port = Word_SMS(서술상수, "()V") ? 0 : 빼기(1), objecte_Referència = 빼기(2); if (!objecte_VALOR(objecte_Referència, 15)) return;
                if (número_de_port < 0 || número_de_port > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = usuari.crear_xarxa(número_de_port); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[objecte_Referència + 2] = 열린파일번호; return;
            }
            if (ordre_CODI == 182 && Word_SMS(이름상수, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), objecte_Referència = 빼기(2); if (!objecte_VALOR(objecte_Referència, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[objecte_Referència + 3] = 밀리초값; return;
            }
            if (ordre_CODI == 182 && Word_SMS(이름상수, "getLocalPort") && Word_SMS(서술상수, "()I")) { int objecte_Referència = 빼기(2); if (objecte_VALOR(objecte_Referència, 15)) 넣기(힙[objecte_Referència + 2] < 0 ? -1 : usuari.xarxa_port(힙[objecte_Referència + 2]), 1); return; }
            if (ordre_CODI == 182 && Word_SMS(이름상수, "isClosed") && Word_SMS(서술상수, "()Z")) { int objecte_Referència = 빼기(2); if (objecte_VALOR(objecte_Referència, 15)) 넣기(힙[objecte_Referència + 2] < 0 ? 1 : 0, 1); return; }
            if (ordre_CODI == 182 && Word_SMS(이름상수, "close") && Word_SMS(서술상수, "()V")) { int objecte_Referència = 빼기(2); if (objecte_VALOR(objecte_Referència, 15) && 힙[objecte_Referència + 2] >= 0) { usuari.파일서술자닫기(힙[objecte_Referència + 2]); 힙[objecte_Referència + 2] = -1; } return; }
            if (ordre_CODI == 182 && (Word_SMS(이름상수, "send") || Word_SMS(이름상수, "receive")) && Word_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int paquet_5cd5338b = 빼기(2), objecte_Referència = 빼기(2); if (!objecte_VALOR(paquet_5cd5338b, 16) || !objecte_VALOR(objecte_Referència, 15)) return;
                int dades_MATRIU = 힙[paquet_5cd5338b + 2], 유효길이 = 힙[paquet_5cd5338b + 3], 열린파일번호 = 힙[objecte_Referència + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_SMS(이름상수, "send")) {
                    if (!objecte_VALOR(힙[paquet_5cd5338b + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < 유효길이; Loop_INDEX++) 통신임시[Loop_INDEX] = 힙[dades_MATRIU + 2 + Loop_INDEX];
                    if (usuari.enviar_xarxa(열린파일번호, 힙[힙[paquet_5cd5338b + 4] + 2], 힙[paquet_5cd5338b + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int introducció_COMPT = usuari.rebre_xarxa(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (introducció_COMPT == -11) {
                        int 현재시각 = usuari.밀리초();
                        if (힙[objecte_Referència + 4] == 0) 힙[objecte_Referència + 4] = 현재시각 + 1;
                        if (힙[objecte_Referència + 3] > 0 && 현재시각 - (힙[objecte_Referència + 4] - 1) >= 힙[objecte_Referència + 3]) { 힙[objecte_Referència + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(objecte_Referència, 2); 넣기(paquet_5cd5338b, 2); marc_càrrec[marc_INDEX] = marc_instrucció[marc_INDEX]; canviar_sol_licitud = true; return;
                    }
                    힙[objecte_Referència + 4] = 0;
                    if (introducció_COMPT < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < introducció_COMPT; Loop_INDEX++) 힙[dades_MATRIU + 2 + Loop_INDEX] = (byte)통신임시[Loop_INDEX];
                    힙[paquet_5cd5338b + 3] = introducció_COMPT; 힙[paquet_5cd5338b + 4] = ADREÇA_objecte(통신임시[513]); 힙참조[paquet_5cd5338b + 4] = 1; 힙[paquet_5cd5338b + 5] = 통신임시[512];
                }
                return;
            }
        }
        error_VALOR("unsupported java.net method");
    }
    static boolean 흐름대기(int objecte_Referència) {
        int 현재시각 = usuari.밀리초();
        if (힙[objecte_Referència + 5] == 0) 힙[objecte_Referència + 5] = 현재시각 + 1;
        if (힙[objecte_Referència + 3] > 0 && 현재시각 - (힙[objecte_Referència + 5] - 1) >= 힙[objecte_Referència + 3]) { 힙[objecte_Referència + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        marc_càrrec[marc_INDEX] = marc_instrucció[marc_INDEX]; canviar_sol_licitud = true; return true;
    }
    static void 흐름호출(int propietari, int 이름상수, int 서술상수, int ordre_CODI) {
        boolean rebre_pàgina = Word_SMS(propietari, "java/net/ServerSocket"), flux = Word_SMS(propietari, "java/io/InputStream") || Word_SMS(propietari, "java/io/OutputStream");
        if (!flux && ordre_CODI == 183 && Word_SMS(이름상수, "<init>")) {
            boolean 빈여부 = Word_SMS(서술상수, "()V"), 이름지정여부 = Word_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || rebre_pàgina && Word_SMS(서술상수, "(I)V") || !rebre_pàgina && (이름지정여부 || 주소지정여부))) { error_VALOR("unsupported socket constructor"); return; }
            int número_de_port = 빈여부 ? 0 : 빼기(1), ADREÇA_Referència = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, objecte_Referència = 빼기(2);
            if (!objecte_VALOR(objecte_Referència, rebre_pàgina ? 18 : 17)) return;
            if (número_de_port < 0 || número_de_port > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !objecte_VALOR(ADREÇA_Referència, 14)) return;
            int xarxa_ADREÇA = 이름지정여부 ? 주소해독(ADREÇA_Referència) : 주소지정여부 ? 힙[ADREÇA_Referència + 2] : 0x7f000001;
            if (s_ha_produït_un_error || 던진객체 != 0) return;
            int 열린파일번호 = usuari.flux_control(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : rebre_pàgina ? usuari.flux_control(1, 열린파일번호, número_de_port) : usuari.CONNECTA_flux(열린파일번호, xarxa_ADREÇA, número_de_port);
            if (처리값 < 0) { usuari.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[objecte_Referència + 2] = 열린파일번호; 힙[objecte_Referència + 4] = número_de_port; 힙[objecte_Referència + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!flux && Word_SMS(이름상수, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), objecte_Referència = 빼기(2); if (!objecte_VALOR(objecte_Referència, rebre_pàgina ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[objecte_Referència + 3] = 밀리초값; return; }
        if (!flux && Word_SMS(이름상수, "close") && Word_SMS(서술상수, "()V")) { int objecte_Referència = 빼기(2); if (objecte_VALOR(objecte_Referència, rebre_pàgina ? 18 : 17) && 힙[objecte_Referència + 2] >= 0) { usuari.파일서술자닫기(힙[objecte_Referència + 2]); 힙[objecte_Referència + 2] = -1; } return; }
        if (!flux && (Word_SMS(이름상수, "getLocalPort") || Word_SMS(이름상수, "getPort") || Word_SMS(이름상수, "isClosed") || Word_SMS(이름상수, "isConnected"))) {
            int objecte_Referència = 빼기(2); if (!objecte_VALOR(objecte_Referència, rebre_pàgina ? 18 : 17)) return;
            넣기(Word_SMS(이름상수, "isClosed") ? 힙[objecte_Referència + 2] < 0 ? 1 : 0 : Word_SMS(이름상수, "isConnected") ? 힙[objecte_Referència + 6] : Word_SMS(이름상수, "getPort") ? 힙[objecte_Referència + 4] : 힙[objecte_Referència + 2] < 0 ? -1 : usuari.flux_control(4, 힙[objecte_Referència + 2], 0), 1); return;
        }
        if (rebre_pàgina && Word_SMS(이름상수, "accept") && Word_SMS(서술상수, "()Ljava/net/Socket;")) {
            int objecte_Referència = 빼기(2); if (!objecte_VALOR(objecte_Referència, 18)) return; int 열린파일번호 = usuari.flux_control(3, 힙[objecte_Referència + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(objecte_Referència)) 넣기(objecte_Referència, 2); return; }
            힙[objecte_Referència + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = assignar_Emmagatzematge(17, 5); if (s_ha_produït_un_error) { usuari.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = usuari.flux_control(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!rebre_pàgina && !flux && ((Word_SMS(이름상수, "getInputStream") && Word_SMS(서술상수, "()Ljava/io/InputStream;")) || (Word_SMS(이름상수, "getOutputStream") && Word_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int objecte_Referència = 빼기(2); if (!objecte_VALOR(objecte_Referència, 17)) return; if (힙[objecte_Referència + 2] < 0 || 힙[objecte_Referència + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = assignar_Emmagatzematge(19, 4); if (s_ha_produït_un_error) return; 힙[반환값 + 2] = objecte_Referència; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Word_SMS(이름상수, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (flux) {
            boolean 읽기여부 = Word_SMS(이름상수, "read"), tecnologies_de_la_informació_escriure_cirurgia = Word_SMS(이름상수, "write"), bloquejar = Word_SMS(서술상수, "([B)I") || Word_SMS(서술상수, "([B)V"), tecnologies_de_la_informació_SUBMATRIU = Word_SMS(서술상수, "([BII)I") || Word_SMS(서술상수, "([BII)V");
            int introducció_COMPT = tecnologies_de_la_informació_SUBMATRIU ? 빼기(1) : 0, 시작변위 = tecnologies_de_la_informació_SUBMATRIU ? 빼기(1) : 0, dades_MATRIU = bloquejar || tecnologies_de_la_informació_SUBMATRIU ? 빼기(2) : 0;
            int dades_VALOR = tecnologies_de_la_informació_escriure_cirurgia && Word_SMS(서술상수, "(I)V") ? 빼기(1) : 0, objecte_Referència = 빼기(2);
            if (!objecte_VALOR(objecte_Referència, 19)) return; int 부모참조 = 힙[objecte_Referència + 2], 열린파일번호 = 힙[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_SMS(이름상수, "close") && Word_SMS(서술상수, "()V")) { usuari.파일서술자닫기(열린파일번호); 힙[부모참조 + 2] = -1; return; }
            if (Word_SMS(이름상수, "flush") && Word_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !tecnologies_de_la_informació_escriure_cirurgia) || 읽기여부 != (힙[objecte_Referència + 3] == 0)) { error_VALOR("unsupported stream operation"); return; }
            if (bloquejar || tecnologies_de_la_informació_SUBMATRIU) { if (!objecte_VALOR(dades_MATRIU, 20)) return; if (bloquejar) introducció_COMPT = 힙[dades_MATRIU + 1]; if (시작변위 < 0 || introducció_COMPT < 0 || 시작변위 > 힙[dades_MATRIU + 1] - introducció_COMPT) { 예외던짐(6, "stream array bounds"); return; } }
            else introducció_COMPT = 1;
            if (introducció_COMPT == 0) { if (읽기여부) 넣기(0, 1); return; }
            int Completades_COMPT = tecnologies_de_la_informació_escriure_cirurgia ? 힙[objecte_Referència + 4] : 0, 처리값 = 0;
            while (Completades_COMPT < introducció_COMPT) {
                처리값 = 읽기여부 ? usuari.파일한바이트읽기(열린파일번호) : usuari.파일한바이트쓰기(열린파일번호, bloquejar || tecnologies_de_la_informació_SUBMATRIU ? 힙[dades_MATRIU + 2 + 시작변위 + Completades_COMPT] : dades_VALOR);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (bloquejar || tecnologies_de_la_informació_SUBMATRIU)) 힙[dades_MATRIU + 2 + 시작변위 + Completades_COMPT] = (byte)처리값;
                Completades_COMPT++; if (읽기여부 && !(bloquejar || tecnologies_de_la_informació_SUBMATRIU)) break;
            }
            if (처리값 == -11 && (tecnologies_de_la_informació_escriure_cirurgia || Completades_COMPT == 0)) {
                힙[objecte_Referència + 4] = Completades_COMPT;
                if (흐름대기(부모참조)) { 넣기(objecte_Referència, 2); if (bloquejar || tecnologies_de_la_informació_SUBMATRIU) 넣기(dades_MATRIU, 2); if (tecnologies_de_la_informació_SUBMATRIU) { 넣기(시작변위, 1); 넣기(introducció_COMPT, 1); } if (tecnologies_de_la_informació_escriure_cirurgia && !(bloquejar || tecnologies_de_la_informació_SUBMATRIU)) 넣기(dades_VALOR, 1); } return;
            }
            힙[objecte_Referència + 4] = 0; 힙[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(Completades_COMPT == 0 && 처리값 == 256 ? -1 : bloquejar || tecnologies_de_la_informació_SUBMATRIU ? Completades_COMPT : 처리값, 1); return;
        }
        error_VALOR("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int 이름상수) {
        if (Word_SMS(이름상수, "Català/propi/Finestra")) return 24;
        if (Word_SMS(이름상수, "Català/propi/Etiqueta")) return 26;
        if (Word_SMS(이름상수, "Català/propi/Botó")) return 27;
        if (Word_SMS(이름상수, "Català/propi/SMS_camp")) return 28;
        if (Word_SMS(이름상수, "Català/propi/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int 이름상수) {
        return 한국어화면종(이름상수) != 0 || Word_SMS(이름상수, "Català/propi/화면구성요소") || Word_SMS(이름상수, "Català/propi/incidència_cua");
    }
    static int 화면종(int 이름상수) {
        int 한국어종 = 한국어화면종(이름상수); if (한국어종 != 0) return 한국어종;
        if (Word_SMS(이름상수, "javax/swing/JFrame")) return 24;
        if (Word_SMS(이름상수, "javax/swing/JPanel")) return 25;
        if (Word_SMS(이름상수, "javax/swing/JLabel")) return 26;
        if (Word_SMS(이름상수, "javax/swing/JButton")) return 27;
        if (Word_SMS(이름상수, "javax/swing/JTextField")) return 28;
        if (Word_SMS(이름상수, "java/awt/event/ActionEvent")) return 29;
        if (Word_SMS(이름상수, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int 이름상수) {
        return 화면종(이름상수) != 0 || Word_SMS(이름상수, "java/awt/Component") || Word_SMS(이름상수, "java/awt/Container") || Word_SMS(이름상수, "javax/swing/JComponent") || Word_SMS(이름상수, "javax/swing/AbstractButton") || Word_SMS(이름상수, "javax/swing/text/JTextComponent") || Word_SMS(이름상수, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int objecte_Referència) { if (!객체유효(objecte_Referència)) return false; if (힙[objecte_Referència] < 24 || 힙[objecte_Referència] > 28) { error_VALOR("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int objecte_Referència, int SMS_Referència) {
        if (SMS_Referència != 0 && !objecte_VALOR(SMS_Referència, 1)) return;
        int introducció_COMPT = SMS_Referència == 0 ? 0 : 힙[SMS_Referència + 1]; if (introducció_COMPT > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < introducció_COMPT; Loop_INDEX++) 화면글임시[Loop_INDEX] = 힙[SMS_Referència + 2 + Loop_INDEX];
        if (usuari.화면글(힙[objecte_Referència + 2], 화면글임시, introducció_COMPT) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[objecte_Referència + 3] = SMS_Referència; 힙참조[objecte_Referència + 3] = 1;
    }
    static int 화면문자읽기(int objecte_Referència) {
        int compte_VALOR = 힙[objecte_Referència + 2], introducció_COMPT = usuari.화면연결(8, compte_VALOR, 0, 0, 0, 0), 사용수 = 0;
        if (introducció_COMPT < 0) { error_VALOR("GUI text read failed"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < introducció_COMPT; Loop_INDEX++) { int 부호값 = usuari.화면연결(9, compte_VALOR, Loop_INDEX, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = assignar_Emmagatzematge(1, 사용수); if (!s_ha_produït_un_error) for (int Loop_INDEX = 0; Loop_INDEX < 사용수; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 화면글임시[Loop_INDEX]; return 반환값;
    }
    /* Català 객체를 직접 만들고 nucli_VALOR 화면 기능에 연결한다. Swing objecte_VALOR/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int propietari, int 이름상수, int 서술상수, int ordre_CODI) {
        if (Word_SMS(propietari, "Català/propi/incidència_cua")) {
            if (ordre_CODI == 184 && Word_SMS(이름상수, "나중에실행") && Word_SMS(서술상수, "(LCatalà/propi/실행할일;)V")) {
                int tasca_acció = 빼기(2); if (!객체유효(tasca_acció)) return;
                if (나중수 == 8) { error_VALOR("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = tasca_acció; return;
            }
            if (ordre_CODI == 184 && Word_SMS(이름상수, "사건처리중인가") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            error_VALOR("지원하지 않는 Català 화면 일정 호출"); return;
        }
        if (Word_SMS(propietari, "Català/propi/동작알림")) {
            int 알림 = 빼기(2); if (!objecte_VALOR(알림, 29) || 힙[알림 + 3] == 0) return;
            if (Word_SMS(이름상수, "incidència_font") && Word_SMS(서술상수, "()LCatalà/propi/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (Word_SMS(이름상수, "ordre_SMS") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (Word_SMS(이름상수, "INDEX") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else error_VALOR("지원하지 않는 Català Acció 알림 호출"); return;
        }
        if (ordre_CODI == 183 && Word_SMS(이름상수, "<init>")) {
            int 종류 = 한국어화면종(propietari), 받이 = 0, 가로 = 0, Vertical_càrrec = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Word_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (usuari.화면너비() - 폭) / 2; Vertical_càrrec = (usuari.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Word_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Word_SMS(서술상수, "(Ljava/lang/String;IIIILCatalà/propi/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); Vertical_càrrec = 빼기(1); 가로 = 빼기(1);
            } else { error_VALOR("지원하지 않는 Català 화면 생성자"); return; }
            int SMS = 빼기(2), element_VALOR = 빼기(2); if (!화면객체(element_VALOR)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || Vertical_càrrec < 0 || 폭 > usuari.화면너비() - 가로 || 높이 > usuari.화면높이() - Vertical_càrrec) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDEX = usuari.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (INDEX < 1 || INDEX > 32) { error_VALOR("화면 element_VALOR 자리가 가득 찼습니다"); return; }
            힙[element_VALOR + 2] = INDEX; 화면참조[INDEX - 1] = element_VALOR;
            힙[element_VALOR + 5] = 가로; 힙[element_VALOR + 6] = Vertical_càrrec; 힙[element_VALOR + 7] = 폭; 힙[element_VALOR + 8] = 높이; 힙[element_VALOR + 10] = 2;
            힙[element_VALOR + 4] = 받이; 힙참조[element_VALOR + 4] = 1; 힙[element_VALOR + 12] = 1;
            usuari.화면연결(1, INDEX, 가로, Vertical_càrrec, 폭, 높이);
            if (종류 == 24) usuari.화면연결(7, INDEX, 2, 0, 0, 0);
            화면문자설정(element_VALOR, SMS); return;
        }
        if (ordre_CODI != 182) { error_VALOR("잘못된 Català 화면 호출 Ordre"); return; }
        if (Word_SMS(이름상수, "escriure_SMS") && Word_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int SMS = 빼기(2), element_VALOR = 빼기(2); if (화면객체(element_VALOR)) 화면문자설정(element_VALOR, SMS); return;
        }
        if (Word_SMS(이름상수, "tancar_SMS") && Word_SMS(서술상수, "()Ljava/lang/String;")) {
            int element_VALOR = 빼기(2); if (화면객체(element_VALOR)) 넣기(화면문자읽기(element_VALOR), 2); return;
        }
        if (Word_SMS(이름상수, "동작맡기기") && Word_SMS(서술상수, "(LCatalà/propi/동작받이;)V")) {
            int 받이 = 빼기(2), element_VALOR = 빼기(2);
            if (화면객체(element_VALOR)) { 힙[element_VALOR + 4] = 받이; 힙참조[element_VALOR + 4] = 1; 힙[element_VALOR + 12] = 1; } return;
        }
        if (Word_SMS(이름상수, "afegir_element") && Word_SMS(서술상수, "(LCatalà/propi/화면구성요소;)V")) {
            int nen_VALOR = 빼기(2), 부모 = 빼기(2); if (!화면객체(nen_VALOR) || !화면객체(부모)) return;
            if (usuari.화면연결(2, 힙[부모 + 2], 힙[nen_VALOR + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[nen_VALOR + 11] = 부모; 힙참조[nen_VALOR + 11] = 1; return;
        }
        if (Word_SMS(이름상수, "자리정하기") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), Vertical_càrrec = 빼기(1), 가로 = 빼기(1), element_VALOR = 빼기(2); if (!화면객체(element_VALOR)) return;
            if (usuari.화면연결(1, 힙[element_VALOR + 2], 가로, Vertical_càrrec, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[element_VALOR + 5] = 가로; 힙[element_VALOR + 6] = Vertical_càrrec; 힙[element_VALOR + 7] = 폭; 힙[element_VALOR + 8] = 높이; return;
        }
        if ((Word_SMS(이름상수, "mostrar_finestra") || Word_SMS(이름상수, "Tanca")) && Word_SMS(서술상수, "()V")) {
            boolean visibilitat_VALOR = Word_SMS(이름상수, "mostrar_finestra"); int element_VALOR = 빼기(2); if (!화면객체(element_VALOR)) return;
            if (usuari.화면연결(visibilitat_VALOR ? 3 : 4, 힙[element_VALOR + 2], visibilitat_VALOR ? 1 : 0, 0, 0, 0) < 0) { error_VALOR("화면은 interactiu 명령에서 실행해야 합니다"); return; }
            힙[element_VALOR + 9] = visibilitat_VALOR ? 1 : 0; return;
        }
        if (Word_SMS(이름상수, "보이는가") && Word_SMS(서술상수, "()Z")) { int element_VALOR = 빼기(2); if (화면객체(element_VALOR)) 넣기(힙[element_VALOR + 9], 1); return; }
        error_VALOR("지원하지 않는 Català 화면 메서드");
    }
    static void 화면호출(int propietari, int 이름상수, int 서술상수, int ordre_CODI) {
        if (Word_SMS(propietari, "javax/swing/SwingUtilities")) {
            if (ordre_CODI == 184 && Word_SMS(이름상수, "invokeLater") && Word_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int objecte_Referència = 빼기(2); if (!객체유효(objecte_Referència)) return; if (나중수 == 8) { error_VALOR("invokeLater queue full"); return; } 나중실행[나중수++] = objecte_Referència; return; }
            if (ordre_CODI == 184 && Word_SMS(이름상수, "isEventDispatchThread") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            error_VALOR("unsupported SwingUtilities method"); return;
        }
        if (Word_SMS(propietari, "java/awt/event/ActionEvent")) {
            int objecte_Referència = 빼기(2); if (!objecte_VALOR(objecte_Referència, 29)) return;
            if (Word_SMS(이름상수, "getSource") && Word_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[objecte_Referència + 2], 2);
            else if (Word_SMS(이름상수, "getActionCommand") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[objecte_Referència + 2]), 2);
            else if (Word_SMS(이름상수, "getID") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else error_VALOR("unsupported ActionEvent method"); return;
        }
        if (ordre_CODI == 183 && Word_SMS(이름상수, "<init>")) {
            int COLUMNES = 0, SMS_Referència = 0;
            if (Word_SMS(서술상수, "(I)V")) COLUMNES = 빼기(1);
            else if (Word_SMS(서술상수, "(Ljava/lang/String;I)V")) { COLUMNES = 빼기(1); SMS_Referència = 빼기(2); }
            else if (Word_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_Referència = 빼기(2);
            else if (Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_SMS(서술상수, "()V")) { error_VALOR("unsupported Swing constructor"); return; }
            int objecte_Referència = 빼기(2); if (!객체유효(objecte_Referència)) return;
            if (힙[objecte_Referència] == 30) { error_VALOR("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(objecte_Referència) || COLUMNES < 0) return;
            int compte_VALOR = usuari.화면연결(0, 힙[objecte_Referència] - 23, 0, 0, 0, 0);
            if (compte_VALOR < 1 || compte_VALOR > 32) { error_VALOR("GUI widget slots exhausted"); return; }
            힙[objecte_Referència + 2] = compte_VALOR; 화면참조[compte_VALOR - 1] = objecte_Referència; 힙[objecte_Referència + 5] = 힙[objecte_Referència] == 24 ? 130 : 16; 힙[objecte_Referència + 6] = 힙[objecte_Referència] == 24 ? 110 : 16;
            힙[objecte_Referència + 7] = 힙[objecte_Referència] == 24 ? 380 : 220; 힙[objecte_Referència + 8] = 힙[objecte_Referència] == 24 ? 240 : 28; 힙[objecte_Referència + 10] = 1;
            화면문자설정(objecte_Referència, SMS_Referència); return;
        }
        if (Word_SMS(이름상수, "setText") || Word_SMS(이름상수, "setTitle")) { int SMS_Referència = 빼기(2), objecte_Referència = 빼기(2); if (화면객체(objecte_Referència) && Word_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(objecte_Referència, SMS_Referència); return; }
        if (Word_SMS(이름상수, "getText") || Word_SMS(이름상수, "getTitle")) { int objecte_Referència = 빼기(2); if (화면객체(objecte_Referència) && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(objecte_Referència), 2); return; }
        if (Word_SMS(이름상수, "addActionListener") && Word_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int rebre_Referència = 빼기(2), objecte_Referència = 빼기(2); if (화면객체(objecte_Referència)) { 힙[objecte_Referència + 4] = rebre_Referència; 힙참조[objecte_Referència + 4] = 1; } return; }
        if (Word_SMS(이름상수, "getContentPane") && Word_SMS(서술상수, "()Ljava/awt/Container;")) { int objecte_Referència = 빼기(2); if (화면객체(objecte_Referència)) 넣기(objecte_Referència, 2); return; }
        if (Word_SMS(이름상수, "setLayout") && Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int disseny_Referència = 빼기(2), objecte_Referència = 빼기(2); if (화면객체(objecte_Referència) && disseny_Referència != 0) error_VALOR("only absolute layout (null) is supported"); return; }
        if (Word_SMS(이름상수, "add") && (Word_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean disseny_condició = Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (disseny_condició) 빼기(2);
            int nen_Referència = 빼기(2), objecte_Referència = 빼기(2); if (!화면객체(nen_Referència) || !화면객체(objecte_Referència)) return;
            if (usuari.화면연결(2, 힙[objecte_Referència + 2], 힙[nen_Referència + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[nen_Referència + 11] = objecte_Referència; 힙참조[nen_Referència + 11] = 1; if (!disseny_condició) 넣기(nen_Referència, 2); return;
        }
        if (Word_SMS(이름상수, "setBounds") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), Y_coordenada = 빼기(1), X_coordenada = 빼기(1), objecte_Referència = 빼기(2); if (!화면객체(objecte_Referència)) return;
            if (usuari.화면연결(1, 힙[objecte_Referència + 2], X_coordenada, Y_coordenada, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[objecte_Referència + 5] = X_coordenada; 힙[objecte_Referència + 6] = Y_coordenada; 힙[objecte_Referència + 7] = 너비; 힙[objecte_Referència + 8] = 높이; return;
        }
        if (Word_SMS(이름상수, "setSize") && Word_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), objecte_Referència = 빼기(2); if (!화면객체(objecte_Referència)) return;
            if (usuari.화면연결(1, 힙[objecte_Referència + 2], 힙[objecte_Referència + 5], 힙[objecte_Referència + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[objecte_Referència + 7] = 너비; 힙[objecte_Referència + 8] = 높이; } return;
        }
        if (Word_SMS(이름상수, "setLocationRelativeTo") && Word_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), objecte_Referència = 빼기(2); if (!화면객체(objecte_Referència)) return; if (상대배치 != 0) { error_VALOR("only screen centering supported"); return; } 힙[objecte_Referència + 5] = (usuari.화면너비() - 힙[objecte_Referència + 7]) / 2; 힙[objecte_Referència + 6] = (usuari.화면높이() - 힙[objecte_Referència + 8]) / 2; usuari.화면연결(1, 힙[objecte_Referència + 2], 힙[objecte_Referència + 5], 힙[objecte_Referència + 6], 힙[objecte_Referència + 7], 힙[objecte_Referència + 8]); return; }
        if (Word_SMS(이름상수, "setDefaultCloseOperation") && Word_SMS(서술상수, "(I)V")) { int norma = 빼기(1), objecte_Referència = 빼기(2); if (화면객체(objecte_Referència)) { if (norma < 0 || norma > 3) 예외던짐(9, "close policy"); else { 힙[objecte_Referència + 10] = norma; usuari.화면연결(7, 힙[objecte_Referència + 2], norma, 0, 0, 0); } } return; }
        if (Word_SMS(이름상수, "setVisible") && Word_SMS(서술상수, "(Z)V")) { int dades_VALOR = 빼기(1), objecte_Referència = 빼기(2); if (화면객체(objecte_Referència)) { int 처리값 = usuari.화면연결(3, 힙[objecte_Referència + 2], dades_VALOR, 0, 0, 0); if (처리값 < 0) error_VALOR("Swing requires a standalone interactive command"); else 힙[objecte_Referència + 9] = dades_VALOR; } return; }
        if (Word_SMS(이름상수, "dispose") && Word_SMS(서술상수, "()V")) { int objecte_Referència = 빼기(2); if (화면객체(objecte_Referència)) { usuari.화면연결(4, 힙[objecte_Referència + 2], 0, 0, 0, 0); 힙[objecte_Referència + 9] = 0; } return; }
        if (Word_SMS(이름상수, "repaint") || Word_SMS(이름상수, "validate")) { int objecte_Referència = 빼기(2); if (!화면객체(objecte_Referència) || !Word_SMS(서술상수, "()V")) return; usuari.화면연결(1, 힙[objecte_Referència + 2], 힙[objecte_Referència + 5], 힙[objecte_Referència + 6], 힙[objecte_Referència + 7], 힙[objecte_Referència + 8]); return; }
        if (Word_SMS(이름상수, "isVisible") && Word_SMS(서술상수, "()Z")) { int objecte_Referència = 빼기(2); if (화면객체(objecte_Referència)) 넣기(힙[objecte_Referència + 9], 1); return; }
        error_VALOR("unsupported Swing method (native subset)");
    }
    static void 사건실행(int objectiu_ADREÇA, int 사건번호, boolean Català) {
        if (objectiu_ADREÇA < 1 || 힙[objectiu_ADREÇA] < 32) { error_VALOR("Java event listener required"); return; }
        int arxiu_INDEX = 이름함수(힙[objectiu_ADREÇA] - 32, 사건번호 == 0 ? (Català ? "Executa" : "run") : (Català ? "rebre_acció" : "actionPerformed"), 사건번호 == 0 ? "()V" : (Català ? "(LCatalà/propi/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (arxiu_INDEX < 0) { error_VALOR("event callback missing"); return; }
        현재가닥 = 0; fil_COMPT = 1; marc_INDEX = 0; fil_Estat[0] = 1; marc_Pila[0] = 0; marc_blocar[0] = inicialitzar_marc[0] = 0; canviar_sol_licitud = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 128; Loop_INDEX++) { local_VALOR[Loop_INDEX] = local_TIPUS[Loop_INDEX] = 0; }
        틀함수[0] = arxiu_INDEX; marc_càrrec[0] = 함수시작[arxiu_INDEX]; local_VALOR[0] = objectiu_ADREÇA; local_TIPUS[0] = 2;
        if (사건번호 != 0) { local_VALOR[1] = 사건번호; local_TIPUS[1] = 2; }
        사건중 = true; Executa_ordre(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!s_ha_produït_un_error) {
            if (나중수 > 0) { int objectiu_ADREÇA = 나중실행[0], Català = 나중한국어[0]; for (int Loop_INDEX = 1; Loop_INDEX < 나중수; Loop_INDEX++) { 나중실행[Loop_INDEX - 1] = 나중실행[Loop_INDEX]; 나중한국어[Loop_INDEX - 1] = 나중한국어[Loop_INDEX]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(objectiu_ADREÇA, 0, Català != 0); continue; }
            if (usuari.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = usuari.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { error_VALOR("GUI event I/O failed"); return; }
            int compte_VALOR = 사건번호 & 65535; if (compte_VALOR < 1 || compte_VALOR > 32) continue; int objecte_Referència = 화면참조[compte_VALOR - 1]; if (objecte_Referència == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[objecte_Referència + 10] != 0) 힙[objecte_Referència + 9] = 0;
                if (힙[objecte_Referència + 10] == 3) for (int Loop_INDEX = 0; Loop_INDEX < 32; Loop_INDEX++) if (화면참조[Loop_INDEX] != 0 && 힙[화면참조[Loop_INDEX]] == 24) usuari.화면연결(4, Loop_INDEX + 1, 0, 0, 0, 0);
            } else if (힙[objecte_Referència + 4] != 0) {
                int LLEGIU_ME_Referència = assignar_Emmagatzematge(29, 2); if (s_ha_produït_un_error) return; 힙[LLEGIU_ME_Referència + 2] = objecte_Referència; 힙[LLEGIU_ME_Referència + 3] = 힙[objecte_Referència + 12]; 힙참조[LLEGIU_ME_Referència + 2] = 1; 사건실행(힙[objecte_Referència + 4], LLEGIU_ME_Referència, 힙[objecte_Referència + 12] != 0);
            }
        }
    }
    public static int Executa_2() {
        if (usuari.인수개수() == 1 && 자바도구.같음(usuari.인수(0), "-version")) {
            usuari.Escriptura("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (usuari.인수개수() < 1) { usuari.Escriptura("Usage: java CLASS [ARGS]\n"); return 2; }
        introducció_Classe_Definició = càrrega_Classe_Definició(allotjar_caràcter(usuari.인수(0))); if (s_ha_produït_un_error || introducció_Classe_Definició < 0) return 1;
        int introducció_p_VALOR = 이름함수(introducció_Classe_Definició, "Executa_2", "()V");
        boolean 한국어진입 = introducció_p_VALOR >= 0 && (함수권한[introducció_p_VALOR] & 9) == 9;
        if (!한국어진입) introducció_p_VALOR = 이름함수(introducció_Classe_Definició, "main", "([Ljava/lang/String;)V");
        if (introducció_p_VALOR < 0 || (함수권한[introducció_p_VALOR] & 9) != 9) error_VALOR("public static void Executa_2() or main(String[] args) required");
        if (s_ha_produït_un_error) return 1;
        int 인수 = assignar_Emmagatzematge(3, usuari.인수개수() - 1); MATRIU_element[인수] = -1;
        for (int 수 = 1; 수 < usuari.인수개수() && !s_ha_produït_un_error; 수++) 힙[인수 + 1 + 수] = allotjar_caràcter(usuari.인수(수));
        marc_INDEX = 0; 틀함수[0] = introducció_p_VALOR; marc_càrrec[0] = 함수시작[introducció_p_VALOR]; local_VALOR[0] = 한국어진입 ? 0 : 인수; local_TIPUS[0] = 한국어진입 ? 0 : 2;
        fil_Estat[0] = 1; fil_objecte[0] = assignar_Emmagatzematge(13, 2);
        Executa_ordre(); if (!s_ha_produït_un_error) 화면사건들(); return s_ha_produït_un_error ? 1 : 0;
    }
}
