// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Fitxer/스택/Referència/branca 경계를 Executa_ordre 중 검사한다. */
public final class 자바가상기계 {
    static int[] Fitxer = new int[16384], nom_d_arxiu_SMS = new int[64];
    static int[] 상종류 = new int[512], 상가 = new int[512], 상나 = new int[512], cadena_Referència = new int[512];
    static int[] 함수명 = new int[32], 함수형 = new int[32], 함수권한 = new int[32];
    static int[] 함수시작 = new int[32], 함수끝 = new int[32], 함수스택 = new int[32], 함수지역 = new int[32];
    static int[] 함수인수수 = new int[32], 함수인수형 = new int[512], 함수반환 = new int[32];
    static int[] 경계 = new int[16384];
    static int[] local_VALOR = new int[4096], local_TIPUS = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] 틀함수 = new int[32], marc_càrrec = new int[32], marc_Pila = new int[32];
    static int[] 힙 = new int[8192];
    static int Mida, tancar_càrrec, 상수수, 함수수, nom_de_classe, marc_INDEX = -1, 힙끝 = 1, tornar_les_tasques_TIPUS;
    static boolean s_ha_produït_un_error;

    static void error_VALOR(String Word_SMS) {
        if (!s_ha_produït_un_error) { usuari.Escriptura("JVM error: "); usuari.Escriptura(Word_SMS); usuari.escriure_caràcter_VALOR(10); }
        s_ha_produït_un_error = true;
    }
    static boolean clip(int Executa_2, int durada_VALOR) { return Executa_2 >= 0 && durada_VALOR >= 0 && Executa_2 <= Mida - durada_VALOR; }
    static int byte_VALOR() {
        if (!clip(tancar_càrrec, 1)) { error_VALOR("truncated class file"); return 0; }
        return Fitxer[tancar_càrrec++];
    }
    static int 짧은수() { return byte_VALOR() << 8 | byte_VALOR(); }
    static int 정수() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int durada_VALOR) { if (!clip(tancar_càrrec, durada_VALOR)) error_VALOR("invalid attribute size"); else tancar_càrrec += durada_VALOR; }
    static boolean 상검사(int 수, int 종류) {
        if (수 <= 0 || 수 >= 상수수 || 상종류[수] != 종류) { error_VALOR("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_interval(int Executa_2, int durada_VALOR, String Word_SMS) {
        if (!clip(Executa_2, durada_VALOR) || durada_VALOR != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < durada_VALOR; 수++) if (Fitxer[Executa_2 + 수] != Word_SMS.charAt(수)) return false;
        return true;
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
    static void ometre_atribut() {
        int element_COMPT = 짧은수();
        for (int 수 = 0; 수 < element_COMPT && !s_ha_produït_un_error; 수++) { 상검사(짧은수(), 1); 건너(정수()); }
    }
    static int ordre_durada(int VALOR) {
        if (VALOR == 16 || VALOR == 18 || VALOR == 21 || VALOR == 25 || VALOR == 54 || VALOR == 58 || VALOR == 188) return 2;
        if (VALOR == 17 || VALOR == 19 || VALOR == 132 || VALOR >= 153 && VALOR <= 167
            || VALOR >= 178 && VALOR <= 184 || VALOR == 187 || VALOR == 189 || VALOR == 192 || VALOR == 198 || VALOR == 199) return 3;
        if (VALOR >= 0 && VALOR <= 8 || VALOR >= 26 && VALOR <= 29 || VALOR >= 42 && VALOR <= 46 || VALOR == 50
            || VALOR >= 59 && VALOR <= 62 || VALOR >= 75 && VALOR <= 79 || VALOR == 83 || VALOR == 87 || VALOR == 89 || VALOR == 95
            || VALOR == 96 || VALOR == 100 || VALOR == 104 || VALOR == 108 || VALOR == 112 || VALOR == 116
            || VALOR == 120 || VALOR == 122 || VALOR == 124 || VALOR == 126 || VALOR == 128 || VALOR == 130
            || VALOR >= 145 && VALOR <= 147 || VALOR == 172 || VALOR == 176 || VALOR == 177 || VALOR == 190) return 1;
        return 0;
    }
    static void tancar_Classe() {
        if (정수() != 0xcafebabe) error_VALOR("not a class file");
        int 부판 = 짧은수(), versió_VALOR = 짧은수();
        if (versió_VALOR < 45 || versió_VALOR > 52 || 부판 != 0) error_VALOR("supported class versions: 45..52, minor 0");
        상수수 = 짧은수();
        if (상수수 < 1 || 상수수 > 512) { error_VALOR("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < 상수수 && !s_ha_produït_un_error; 수++) {
            int 종류 = byte_VALOR(); 상종류[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = tancar_càrrec; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = 정수();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); 상나[수] = 짧은수(); }
            else error_VALOR("unsupported constant type");
        }
        int permís_VALOR = 짧은수();
        if ((permís_VALOR & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) error_VALOR("unsupported class flags");
        nom_de_classe = nom_de_classe_SMS(짧은수());
        if (!Word_SMS(nom_de_classe_SMS(짧은수()), "java/lang/Object")) error_VALOR("inheritance unsupported");
        if (짧은수() != 0) error_VALOR("interfaces unsupported");
        if (짧은수() != 0) error_VALOR("fields unsupported");
        함수수 = 짧은수();
        if (함수수 < 1 || 함수수 > 32) { error_VALOR("method count limit (32)"); return; }
        for (int 수 = 0; 수 < 함수수 && !s_ha_produït_un_error; 수++) {
            함수권한[수] = 짧은수(); 함수명[수] = 짧은수(); 함수형[수] = 짧은수();
            상검사(함수명[수], 1); 서술읽기(수);
            if ((함수권한[수] & (0x100 | 0x400 | 0x20)) != 0) error_VALOR("native, abstract and synchronized methods unsupported");
            if ((함수권한[수] & 8) == 0 && !Word_SMS(함수명[수], "<init>")) error_VALOR("instance methods unsupported");
            if (Word_SMS(함수명[수], "<clinit>")) error_VALOR("class initializers unsupported");
            for (int frontal_VALOR = 0; frontal_VALOR < 수; frontal_VALOR++) if (같은말(함수명[frontal_VALOR], 함수명[수]) && 같은말(함수형[frontal_VALOR], 함수형[수])) error_VALOR("duplicate method");
            int element_COMPT = 짧은수();
            for (int valor_d_atribut = 0; valor_d_atribut < element_COMPT && !s_ha_produït_un_error; valor_d_atribut++) {
                int Nom = 짧은수(), durada_VALOR = 정수(), Executa_2 = tancar_càrrec;
                if (!clip(Executa_2, durada_VALOR)) { error_VALOR("truncated method attribute"); break; }
                if (Word_SMS(Nom, "Code")) {
                    if (함수시작[수] != 0) error_VALOR("duplicate Code attribute");
                    함수스택[수] = 짧은수(); 함수지역[수] = 짧은수(); int CODI_durada = 정수();
                    if (함수스택[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || CODI_durada < 1 || CODI_durada > 8192) error_VALOR("method memory limits exceeded");
                    함수시작[수] = tancar_càrrec; 건너(CODI_durada); 함수끝[수] = tancar_càrrec;
                    if (짧은수() != 0) error_VALOR("exception handlers unsupported");
                    ometre_atribut();
                    if (tancar_càrrec != Executa_2 + durada_VALOR) error_VALOR("Code attribute size mismatch");
                } else 건너(durada_VALOR);
            }
            if (함수시작[수] == 0) error_VALOR("missing Code attribute");
            int 칸 = 함수시작[수];
            while (칸 < 함수끝[수] && !s_ha_produït_un_error) {
                int durada_VALOR = ordre_durada(Fitxer[칸]);
                if (durada_VALOR == 0 || durada_VALOR > 함수끝[수] - 칸) { error_VALOR("unsupported or truncated bytecode"); break; }
                경계[칸] = 수 + 1; 칸 += durada_VALOR;
            }
            // 실행하지 않는 경로에도 잘못된 branca 목적지를 허용하지 않는다.
            칸 = 함수시작[수];
            while (칸 < 함수끝[수] && !s_ha_produït_un_error) {
                int VALOR = Fitxer[칸];
                if (VALOR >= 153 && VALOR <= 167 || VALOR == 198 || VALOR == 199) {
                    int destinació_VALOR = 칸 + (short)(Fitxer[칸 + 1] << 8 | Fitxer[칸 + 2]);
                    if (destinació_VALOR < 함수시작[수] || destinació_VALOR >= 함수끝[수] || 경계[destinació_VALOR] != 수 + 1) error_VALOR("invalid branch target");
                }
                칸 += ordre_durada(VALOR);
            }
        }
        if (!s_ha_produït_un_error) ometre_atribut();
        if (tancar_càrrec != Mida) error_VALOR("extra class file data");
    }
    static int assignar_Emmagatzematge(int 종류, int durada_VALOR) {
        if (durada_VALOR < 0 || durada_VALOR > 힙.length - 힙끝 - 2) { error_VALOR("object heap exhausted or negative array size"); return 0; }
        int Referència = 힙끝; 힙끝 += durada_VALOR + 2; 힙[Referència] = 종류; 힙[Referència + 1] = durada_VALOR;
        return Referència;
    }
    static boolean objecte_VALOR(int Referència, int 종류) {
        if (Referència < 1 || Referència >= 힙끝 - 1 || 힙[Referència] != 종류) { error_VALOR("null or invalid object reference"); return false; }
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
        if (marc_INDEX == 31) { error_VALOR("call stack limit (32)"); return; }
        int Següent_element = marc_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) local_TIPUS[Següent_element * 128 + 수] = 0;
        for (int 수 = 함수인수수[FUNCIÓ_VALOR] - 1; 수 >= 0; 수--) {
            local_VALOR[Següent_element * 128 + 수] = 빼기(함수인수형[FUNCIÓ_VALOR * 16 + 수]); local_TIPUS[Següent_element * 128 + 수] = 함수인수형[FUNCIÓ_VALOR * 16 + 수];
        }
        marc_INDEX = Següent_element; 틀함수[marc_INDEX] = FUNCIÓ_VALOR; marc_càrrec[marc_INDEX] = 함수시작[FUNCIÓ_VALOR]; marc_Pila[marc_INDEX] = 0;
    }
    static void tornar_les_tasques_mesura(int TIPUS_VALOR) {
        if (TIPUS_VALOR != 함수반환[틀함수[marc_INDEX]]) { error_VALOR("return type mismatch"); return; }
        int VALOR = TIPUS_VALOR == 0 ? 0 : 빼기(TIPUS_VALOR);
        marc_INDEX--; if (marc_INDEX >= 0 && TIPUS_VALOR != 0) 넣기(VALOR, TIPUS_VALOR);
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
                if (VALOR < 1 || VALOR > 127) { error_VALOR("file stream paths currently require ASCII"); return; }
                flux_nom_d_arxiu[칸] = VALOR;
            }
            flux_nom_d_arxiu[durada_VALOR] = 0;
            int 서술자 = usuari.파일서술자열기(flux_nom_d_arxiu, Sortida ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { error_VALOR("FileNotFoundException: file open failed"); return; }
            힙[flux_VALOR + 2] = 서술자; 힙[flux_VALOR + 3] = 1;
            return;
        }
        if (Ordre != 182) { error_VALOR("invalid file stream invocation"); return; }
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
            if (RESULTAT < -1) error_VALOR("IOException: read failed"); else 넣기(RESULTAT, 1);
        } else if (usuari.파일한바이트쓰기(서술자, VALOR) != 1) error_VALOR("IOException: write failed");
    }
    static void 함수호출(int INDEX, int Ordre) {
        if (!상검사(INDEX, 10)) return;
        int propietari_VALOR = nom_de_classe_SMS(상가[INDEX]), Nom = Referència_nom(상나[INDEX]), format_VALOR = Referència_TIPUS(상나[INDEX]);
        if (s_ha_produït_un_error) return;
        if (같은말(propietari_VALOR, nom_de_classe)) {
            if (Ordre != 184) { error_VALOR("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < 함수수; 수++) if (같은말(Nom, 함수명[수]) && 같은말(format_VALOR, 함수형[수])) {
                if ((함수권한[수] & 8) == 0) error_VALOR("method is not static"); else 호출(수);
                return;
            }
            error_VALOR("NoSuchMethodError"); return;
        }
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
        error_VALOR("unsupported library method");
    }
    static int 배열칸(int Referència, int subíndex_VALOR, int TIPUS_VALOR) {
        if (!objecte_VALOR(Referència, TIPUS_VALOR)) return 0;
        if (subíndex_VALOR < 0 || subíndex_VALOR >= 힙[Referència + 1]) { error_VALOR("ArrayIndexOutOfBoundsException"); return 0; }
        return Referència + 2 + subíndex_VALOR;
    }
    static void Executa_ordre() {
        int 남음 = 500000;
        while (marc_INDEX >= 0 && !s_ha_produït_un_error) {
            if (--남음 == 0) { error_VALOR("instruction limit (500000)"); break; }
            int Executa_2 = marc_càrrec[marc_INDEX], VALOR = 명바();
            if (s_ha_produït_un_error) break;
            if (VALOR == 0) continue;
            if (VALOR == 1) { 넣기(0, 2); continue; }
            if (VALOR >= 2 && VALOR <= 8) { 넣기(VALOR - 3, 1); continue; }
            if (VALOR == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALOR == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALOR == 18 || VALOR == 19) {
                int 수 = VALOR == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= 상수수) error_VALOR("invalid ldc constant");
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
            if (VALOR == 46 || VALOR == 50) {
                int subíndex_VALOR = 빼기(1), Referència = 빼기(2), 칸 = 배열칸(Referència, subíndex_VALOR, VALOR == 46 ? 2 : 3);
                if (!s_ha_produït_un_error) 넣기(힙[칸], VALOR == 46 ? 1 : 2); continue;
            }
            if (VALOR == 79 || VALOR == 83) {
                int element_element = 빼기(VALOR == 79 ? 1 : 2), subíndex_VALOR = 빼기(1), Referència = 빼기(2), 칸 = 배열칸(Referència, subíndex_VALOR, VALOR == 79 ? 2 : 3);
                if (VALOR == 83 && element_element != 0) objecte_VALOR(element_element, 1);
                if (!s_ha_produït_un_error) 힙[칸] = element_element; continue;
            }
            if (VALOR == 87) { 빼기(0); continue; }
            if (VALOR == 89) { int 가 = 빼기(0), TIPUS_VALOR = tornar_les_tasques_TIPUS; 넣기(가, TIPUS_VALOR); 넣기(가, TIPUS_VALOR); continue; }
            if (VALOR == 95) { int 가 = 빼기(0), 가형 = tornar_les_tasques_TIPUS, 나 = 빼기(0), 나형 = tornar_les_tasques_TIPUS; 넣기(가, 가형); 넣기(나, 나형); continue; }
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
            if (VALOR == 178) {
                int 수 = 명짧(); if (!상검사(수, 9)) continue;
                if (!Word_SMS(nom_de_classe_SMS(상가[수]), "java/lang/System") || !Word_SMS(Referència_nom(상나[수]), "out")
                    || !Word_SMS(Referència_TIPUS(상나[수]), "Ljava/io/PrintStream;")) error_VALOR("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (VALOR == 182 || VALOR == 183 || VALOR == 184) { 함수호출(명짧(), VALOR); continue; }
            if (VALOR == 187) {
                int Nom = nom_de_classe_SMS(명짧());
                if (Word_SMS(Nom, "java/lang/StringBuilder")) 넣기(assignar_Emmagatzematge(4, 1), 2);
                else if (Word_SMS(Nom, "java/io/FileInputStream") || Word_SMS(Nom, "java/io/FileOutputStream")) {
                    int Referència = assignar_Emmagatzematge(Word_SMS(Nom, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!s_ha_produït_un_error) { 힙[Referència + 2] = -1; 넣기(Referència, 2); }
                } else error_VALOR("unsupported object construction");
                continue;
            }
            if (VALOR == 188 || VALOR == 189) {
                if (VALOR == 188) { if (명바() != 10) error_VALOR("only int[] newarray is supported"); }
                else if (!Word_SMS(nom_de_classe_SMS(명짧()), "java/lang/String")) error_VALOR("only String[] anewarray is supported");
                int durada_VALOR = 빼기(1); 넣기(assignar_Emmagatzematge(VALOR == 188 ? 2 : 3, durada_VALOR), 2); continue;
            }
            if (VALOR == 190) {
                int Referència = 빼기(2);
                if (Referència < 1 || Referència >= 힙끝 - 1 || (힙[Referència] != 2 && 힙[Referència] != 3)) error_VALOR("null or invalid array");
                else 넣기(힙[Referència + 1], 1); continue;
            }
            if (VALOR == 192) {
                int Nom = nom_de_classe_SMS(명짧()), Referència = 빼기(2);
                if (!Word_SMS(Nom, "java/lang/String")) error_VALOR("unsupported checkcast");
                else if (Referència != 0) objecte_VALOR(Referència, 1);
                넣기(Referència, 2); continue;
            }
            error_VALOR("unsupported bytecode");
        }
    }
    public static int Executa_2() {
        if (usuari.인수개수() == 1 && 자바도구.같음(usuari.인수(0), "-version")) {
            usuari.Escriptura("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (usuari.인수개수() < 1) { usuari.Escriptura("Usage: java CLASS [ARGS]\n"); return 2; }
        int durada_VALOR = 자바도구.Nom(nom_d_arxiu_SMS, usuari.인수(0));
        if (durada_VALOR < 1 || durada_VALOR > 57) { usuari.Escriptura("java: invalid class name\n"); return 2; }
        nom_d_arxiu_SMS[durada_VALOR] = '.'; nom_d_arxiu_SMS[durada_VALOR + 1] = 'c'; nom_d_arxiu_SMS[durada_VALOR + 2] = 'l'; nom_d_arxiu_SMS[durada_VALOR + 3] = 'a'; nom_d_arxiu_SMS[durada_VALOR + 4] = 's'; nom_d_arxiu_SMS[durada_VALOR + 5] = 's';
        Mida = usuari.tancar_arxiu(nom_d_arxiu_SMS, Fitxer);
        if (Mida < 0) { usuari.Escriptura("java: cannot read class: "); 자바도구.수쓰기(Mida); usuari.escriure_caràcter_VALOR(10); return 1; }
        tancar_Classe(); if (s_ha_produït_un_error) return 1;
        int caràcter_nom = 상문자(nom_de_classe);
        if (!s_ha_produït_un_error && 힙[caràcter_nom + 1] != durada_VALOR) error_VALOR("class name does not match file");
        for (int 수 = 0; 수 < durada_VALOR && !s_ha_produït_un_error; 수++) if (힙[caràcter_nom + 2 + 수] != nom_d_arxiu_SMS[수]) error_VALOR("class name does not match file");
        int introducció_p_VALOR = -1;
        for (int 수 = 0; 수 < 함수수; 수++) if (Word_SMS(함수명[수], "main") && Word_SMS(함수형[수], "([Ljava/lang/String;)V") && (함수권한[수] & 9) == 9) introducció_p_VALOR = 수;
        if (introducció_p_VALOR < 0) error_VALOR("public static void main(String[] args) required");
        if (s_ha_produït_un_error) return 1;
        int 인수 = assignar_Emmagatzematge(3, usuari.인수개수() - 1);
        for (int 수 = 1; 수 < usuari.인수개수() && !s_ha_produït_un_error; 수++) 힙[인수 + 1 + 수] = allotjar_caràcter(usuari.인수(수));
        marc_INDEX = 0; 틀함수[0] = introducció_p_VALOR; marc_càrrec[0] = 함수시작[introducció_p_VALOR]; local_VALOR[0] = 인수; local_TIPUS[0] = 2;
        Executa_ordre(); return s_ha_produït_un_error ? 1 : 0;
    }
}
