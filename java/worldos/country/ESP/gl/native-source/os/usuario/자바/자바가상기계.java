// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Ficheiro/스택/Material_de_referencia/ramificación 경계를 executar_comando 중 검사한다. */
public final class 자바가상기계 {
    static int[] Ficheiro = new int[16384], Ficheiro_nome_SMS = new int[64];
    static int[] constante_etiqueta = new int[512], 상가 = new int[512], constante_SEGUNDO_VALOR = new int[512], cadea_Material_de_referencia = new int[512];
    static int[] 함수명 = new int[32], 함수형 = new int[32], 함수권한 = new int[32];
    static int[] 함수시작 = new int[32], 함수끝 = new int[32], 함수스택 = new int[32], 함수지역 = new int[32];
    static int[] 함수인수수 = new int[32], 함수인수형 = new int[512], 함수반환 = new int[32];
    static int[] 경계 = new int[16384];
    static int[] local_VALOR = new int[4096], local_TIPO = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] 틀함수 = new int[32], marco_cargo = new int[32], marco_Montón = new int[32];
    static int[] 힙 = new int[8192];
    static int Tamaño, 읽기위치, constante_CONTAR, 함수수, nome_de_clase, marco_ÍNDICE = -1, 힙끝 = 1, devolver_TIPO;
    static boolean ERRO;

    static void erro_VALOR(String Word_SMS) {
        if (!ERRO) { usuario.Escritura("JVM error: "); usuario.Escritura(Word_SMS); usuario.escribir_carácter_VALOR(10); }
        ERRO = true;
    }
    static boolean clip(int Executar_2, int duración_VALOR) { return Executar_2 >= 0 && duración_VALOR >= 0 && Executar_2 <= Tamaño - duración_VALOR; }
    static int byte_VALOR() {
        if (!clip(읽기위치, 1)) { erro_VALOR("truncated class file"); return 0; }
        return Ficheiro[읽기위치++];
    }
    static int 짧은수() { return byte_VALOR() << 8 | byte_VALOR(); }
    static int número_enteiro() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int duración_VALOR) { if (!clip(읽기위치, duración_VALOR)) erro_VALOR("invalid attribute size"); else 읽기위치 += duración_VALOR; }
    static boolean cheque_constante(int 수, int 종류) {
        if (수 <= 0 || 수 >= constante_CONTAR || constante_etiqueta[수] != 종류) { erro_VALOR("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_intervalo(int Executar_2, int duración_VALOR, String Word_SMS) {
        if (!clip(Executar_2, duración_VALOR) || duración_VALOR != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < duración_VALOR; 수++) if (Ficheiro[Executar_2 + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static boolean Word_SMS(int constante_VALOR, String Word_SMS) { return cheque_constante(constante_VALOR, 1) && SMS_intervalo(상가[constante_VALOR], constante_SEGUNDO_VALOR[constante_VALOR], Word_SMS); }
    static boolean 같은말(int 가, int 나) {
        if (!cheque_constante(가, 1) || !cheque_constante(나, 1) || constante_SEGUNDO_VALOR[가] != constante_SEGUNDO_VALOR[나]) return false;
        for (int 수 = 0; 수 < constante_SEGUNDO_VALOR[가]; 수++) if (Ficheiro[상가[가] + 수] != Ficheiro[상가[나] + 수]) return false;
        return true;
    }
    static int nome_de_clase_SMS(int 수) { return cheque_constante(수, 7) && cheque_constante(상가[수], 1) ? 상가[수] : 0; }
    static int Material_de_referencia_nome(int 수) { return cheque_constante(수, 12) && cheque_constante(상가[수], 1) ? 상가[수] : 0; }
    static int Material_de_referencia_TIPO(int 수) { return cheque_constante(수, 12) && cheque_constante(constante_SEGUNDO_VALOR[수], 1) ? constante_SEGUNDO_VALOR[수] : 0; }
    static int 서술형(int 끝, boolean baleiro_TIPO) {
        if (읽기위치 >= 끝) { erro_VALOR("invalid descriptor"); return 0; }
        int VALOR = byte_VALOR();
        if (VALOR == 'V' && baleiro_TIPO) return 0;
        if (VALOR == 'I' || VALOR == 'B' || VALOR == 'C' || VALOR == 'S' || VALOR == 'Z') return 1;
        if (VALOR == '[') { 서술형(끝, false); return 2; }
        if (VALOR == 'L') {
            int Executar_2 = 읽기위치;
            while (읽기위치 < 끝 && Ficheiro[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Executar_2) erro_VALOR("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        erro_VALOR("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int FUNCIÓN_VALOR) {
        int 이전 = 읽기위치, 수 = 함수형[FUNCIÓN_VALOR];
        if (!cheque_constante(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + constante_SEGUNDO_VALOR[수];
        if (byte_VALOR() != '(') erro_VALOR("invalid method descriptor");
        int elemento_CONTAR = 0;
        while (!ERRO && 읽기위치 < 끝 && Ficheiro[읽기위치] != ')') {
            if (elemento_CONTAR == 16) { erro_VALOR("too many method arguments"); break; }
            함수인수형[FUNCIÓN_VALOR * 16 + elemento_CONTAR++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || byte_VALOR() != ')') erro_VALOR("invalid method descriptor");
        함수반환[FUNCIÓN_VALOR] = 서술형(끝, true); 함수인수수[FUNCIÓN_VALOR] = elemento_CONTAR;
        if (읽기위치 != 끝) erro_VALOR("invalid method descriptor");
        읽기위치 = 이전;
    }
    static void 속성건너() {
        int elemento_CONTAR = 짧은수();
        for (int 수 = 0; 수 < elemento_CONTAR && !ERRO; 수++) { cheque_constante(짧은수(), 1); 건너(número_enteiro()); }
    }
    static int comando_duración(int VALOR) {
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
    static void 클래스읽기() {
        if (número_enteiro() != 0xcafebabe) erro_VALOR("not a class file");
        int 부판 = 짧은수(), versión_VALOR = 짧은수();
        if (versión_VALOR < 45 || versión_VALOR > 52 || 부판 != 0) erro_VALOR("supported class versions: 45..52, minor 0");
        constante_CONTAR = 짧은수();
        if (constante_CONTAR < 1 || constante_CONTAR > 512) { erro_VALOR("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < constante_CONTAR && !ERRO; 수++) {
            int 종류 = byte_VALOR(); constante_etiqueta[수] = 종류;
            if (종류 == 1) { constante_SEGUNDO_VALOR[수] = 짧은수(); 상가[수] = 읽기위치; 건너(constante_SEGUNDO_VALOR[수]); }
            else if (종류 == 3) 상가[수] = número_enteiro();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); constante_SEGUNDO_VALOR[수] = 짧은수(); }
            else erro_VALOR("unsupported constant type");
        }
        int permiso_VALOR = 짧은수();
        if ((permiso_VALOR & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) erro_VALOR("unsupported class flags");
        nome_de_clase = nome_de_clase_SMS(짧은수());
        if (!Word_SMS(nome_de_clase_SMS(짧은수()), "java/lang/Object")) erro_VALOR("inheritance unsupported");
        if (짧은수() != 0) erro_VALOR("interfaces unsupported");
        if (짧은수() != 0) erro_VALOR("fields unsupported");
        함수수 = 짧은수();
        if (함수수 < 1 || 함수수 > 32) { erro_VALOR("method count limit (32)"); return; }
        for (int 수 = 0; 수 < 함수수 && !ERRO; 수++) {
            함수권한[수] = 짧은수(); 함수명[수] = 짧은수(); 함수형[수] = 짧은수();
            cheque_constante(함수명[수], 1); 서술읽기(수);
            if ((함수권한[수] & (0x100 | 0x400 | 0x20)) != 0) erro_VALOR("native, abstract and synchronized methods unsupported");
            if ((함수권한[수] & 8) == 0 && !Word_SMS(함수명[수], "<init>")) erro_VALOR("instance methods unsupported");
            if (Word_SMS(함수명[수], "<clinit>")) erro_VALOR("class initializers unsupported");
            for (int frontal_VALOR = 0; frontal_VALOR < 수; frontal_VALOR++) if (같은말(함수명[frontal_VALOR], 함수명[수]) && 같은말(함수형[frontal_VALOR], 함수형[수])) erro_VALOR("duplicate method");
            int elemento_CONTAR = 짧은수();
            for (int atributo_VALOR = 0; atributo_VALOR < elemento_CONTAR && !ERRO; atributo_VALOR++) {
                int Nome = 짧은수(), duración_VALOR = número_enteiro(), Executar_2 = 읽기위치;
                if (!clip(Executar_2, duración_VALOR)) { erro_VALOR("truncated method attribute"); break; }
                if (Word_SMS(Nome, "Code")) {
                    if (함수시작[수] != 0) erro_VALOR("duplicate Code attribute");
                    함수스택[수] = 짧은수(); 함수지역[수] = 짧은수(); int CÓDIGO_duración = número_enteiro();
                    if (함수스택[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || CÓDIGO_duración < 1 || CÓDIGO_duración > 8192) erro_VALOR("method memory limits exceeded");
                    함수시작[수] = 읽기위치; 건너(CÓDIGO_duración); 함수끝[수] = 읽기위치;
                    if (짧은수() != 0) erro_VALOR("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != Executar_2 + duración_VALOR) erro_VALOR("Code attribute size mismatch");
                } else 건너(duración_VALOR);
            }
            if (함수시작[수] == 0) erro_VALOR("missing Code attribute");
            int 칸 = 함수시작[수];
            while (칸 < 함수끝[수] && !ERRO) {
                int duración_VALOR = comando_duración(Ficheiro[칸]);
                if (duración_VALOR == 0 || duración_VALOR > 함수끝[수] - 칸) { erro_VALOR("unsupported or truncated bytecode"); break; }
                경계[칸] = 수 + 1; 칸 += duración_VALOR;
            }
            // 실행하지 않는 경로에도 잘못된 ramificación 목적지를 허용하지 않는다.
            칸 = 함수시작[수];
            while (칸 < 함수끝[수] && !ERRO) {
                int VALOR = Ficheiro[칸];
                if (VALOR >= 153 && VALOR <= 167 || VALOR == 198 || VALOR == 199) {
                    int destino_VALOR = 칸 + (short)(Ficheiro[칸 + 1] << 8 | Ficheiro[칸 + 2]);
                    if (destino_VALOR < 함수시작[수] || destino_VALOR >= 함수끝[수] || 경계[destino_VALOR] != 수 + 1) erro_VALOR("invalid branch target");
                }
                칸 += comando_duración(VALOR);
            }
        }
        if (!ERRO) 속성건너();
        if (읽기위치 != Tamaño) erro_VALOR("extra class file data");
    }
    static int atribuír_Almacenamento(int 종류, int duración_VALOR) {
        if (duración_VALOR < 0 || duración_VALOR > 힙.length - 힙끝 - 2) { erro_VALOR("object heap exhausted or negative array size"); return 0; }
        int Material_de_referencia = 힙끝; 힙끝 += duración_VALOR + 2; 힙[Material_de_referencia] = 종류; 힙[Material_de_referencia + 1] = duración_VALOR;
        return Material_de_referencia;
    }
    static boolean obxecto_VALOR(int Material_de_referencia, int 종류) {
        if (Material_de_referencia < 1 || Material_de_referencia >= 힙끝 - 1 || 힙[Material_de_referencia] != 종류) { erro_VALOR("null or invalid object reference"); return false; }
        return true;
    }
    static int constante_SMS(int ÍNDICE) {
        if (!cheque_constante(ÍNDICE, 1)) return 0;
        if (cadea_Material_de_referencia[ÍNDICE] != 0) return cadea_Material_de_referencia[ÍNDICE];
        int Material_de_referencia = atribuír_Almacenamento(1, constante_SEGUNDO_VALOR[ÍNDICE]); if (ERRO) return 0;
        int 끝 = 상가[ÍNDICE] + constante_SEGUNDO_VALOR[ÍNDICE], 수 = 상가[ÍNDICE], duración_VALOR = 0;
        while (수 < 끝 && !ERRO) {
            int VALOR = Ficheiro[수++];
            if (VALOR == 0) erro_VALOR("invalid modified UTF-8");
            else if (VALOR >= 192 && VALOR <= 223 && 수 < 끝) {
                int Seguinte_elemento = Ficheiro[수++];
                if ((Seguinte_elemento & 192) != 128) erro_VALOR("invalid modified UTF-8");
                VALOR = (VALOR & 31) << 6 | Seguinte_elemento & 63;
                if (VALOR != 0 && VALOR < 128) erro_VALOR("overlong modified UTF-8");
            } else if (VALOR >= 224 && VALOR <= 239 && 수 + 1 < 끝) {
                int 가 = Ficheiro[수++], 나 = Ficheiro[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) erro_VALOR("invalid modified UTF-8");
                VALOR = (VALOR & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (VALOR < 2048) erro_VALOR("overlong modified UTF-8");
            } else if (VALOR >= 128) erro_VALOR("invalid modified UTF-8");
            힙[Material_de_referencia + 2 + duración_VALOR++] = VALOR;
        }
        힙[Material_de_referencia + 1] = duración_VALOR; cadea_Material_de_referencia[ÍNDICE] = Material_de_referencia; return Material_de_referencia;
    }
    static int hospedar_carácter(String VALOR) {
        int Material_de_referencia = atribuír_Almacenamento(1, VALOR.length()); if (ERRO) return 0;
        for (int 수 = 0; 수 < VALOR.length(); 수++) 힙[Material_de_referencia + 2 + 수] = VALOR.charAt(수);
        return Material_de_referencia;
    }
    static void escribir_SMS(int Material_de_referencia) {
        if (Material_de_referencia == 0) { usuario.Escritura("null"); return; }
        if (!obxecto_VALOR(Material_de_referencia, 1)) return;
        for (int 수 = 0; 수 < 힙[Material_de_referencia + 1]; 수++) usuario.escribir_carácter_VALOR(힙[Material_de_referencia + 2 + 수]);
    }
    static int díxito_carácter(int VALOR) {
        int Material_de_referencia = atribuír_Almacenamento(1, 11); if (ERRO) return 0;
        int duración_VALOR = 0;
        if (VALOR < 0) 힙[Material_de_referencia + 2 + duración_VALOR++] = '-'; else VALOR = -VALOR;
        int cargo_ÍNDICE = 1000000000; boolean Executar_2 = false;
        while (cargo_ÍNDICE != 0) {
            int 수 = -(VALOR / cargo_ÍNDICE);
            if (수 != 0 || Executar_2 || cargo_ÍNDICE == 1) { 힙[Material_de_referencia + 2 + duración_VALOR++] = '0' + 수; Executar_2 = true; }
            VALOR %= cargo_ÍNDICE; cargo_ÍNDICE /= 10;
        }
        힙[Material_de_referencia + 1] = duración_VALOR; return Material_de_referencia;
    }
    static int 정수해독(int Material_de_referencia) {
        if (!obxecto_VALOR(Material_de_referencia, 1)) return 0;
        int duración_VALOR = 힙[Material_de_referencia + 1], 수 = 0, VALOR = 0; boolean 음수 = false;
        if (duración_VALOR > 0 && (힙[Material_de_referencia + 2] == '-' || 힙[Material_de_referencia + 2] == '+')) { 음수 = 힙[Material_de_referencia + 2] == '-'; 수++; }
        if (수 == duración_VALOR) erro_VALOR("NumberFormatException");
        for (; 수 < duración_VALOR && !ERRO; 수++) {
            int díxito_VALOR = 힙[Material_de_referencia + 2 + 수] - '0';
            if (díxito_VALOR < 0 || díxito_VALOR > 9 || VALOR < -214748364 || VALOR == -214748364 && díxito_VALOR > (음수 ? 8 : 7)) erro_VALOR("NumberFormatException");
            VALOR = VALOR * 10 - díxito_VALOR;
        }
        return 음수 ? VALOR : -VALOR;
    }
    static void 넣기(int VALOR, int TIPO_VALOR) {
        if (ERRO) return;
        if (marco_ÍNDICE < 0 || marco_Montón[marco_ÍNDICE] >= 함수스택[틀함수[marco_ÍNDICE]]) { erro_VALOR("operand stack overflow"); return; }
        int 칸 = marco_ÍNDICE * 128 + marco_Montón[marco_ÍNDICE]++; 스택값[칸] = VALOR; 스택형[칸] = TIPO_VALOR;
    }
    static int 빼기(int TIPO_VALOR) {
        if (ERRO) return 0;
        if (marco_ÍNDICE < 0 || marco_Montón[marco_ÍNDICE] < 1) { erro_VALOR("operand stack underflow"); return 0; }
        int 칸 = marco_ÍNDICE * 128 + --marco_Montón[marco_ÍNDICE]; devolver_TIPO = 스택형[칸];
        if (TIPO_VALOR != 0 && devolver_TIPO != TIPO_VALOR) erro_VALOR("operand type mismatch");
        return 스택값[칸];
    }
    static void 지역읽기(int ÍNDICE, int TIPO_VALOR) {
        if (ÍNDICE >= 함수지역[틀함수[marco_ÍNDICE]] || ÍNDICE < 0 || local_TIPO[marco_ÍNDICE * 128 + ÍNDICE] != TIPO_VALOR) { erro_VALOR("invalid or uninitialized local"); return; }
        넣기(local_VALOR[marco_ÍNDICE * 128 + ÍNDICE], TIPO_VALOR);
    }
    static void escribir_local(int ÍNDICE, int TIPO_VALOR) {
        if (ÍNDICE >= 함수지역[틀함수[marco_ÍNDICE]] || ÍNDICE < 0) { erro_VALOR("local index out of range"); return; }
        int VALOR = 빼기(TIPO_VALOR); local_VALOR[marco_ÍNDICE * 128 + ÍNDICE] = VALOR; local_TIPO[marco_ÍNDICE * 128 + ÍNDICE] = TIPO_VALOR;
    }
    static int 명바() {
        int Posición = marco_cargo[marco_ÍNDICE];
        if (Posición < 함수시작[틀함수[marco_ÍNDICE]] || Posición >= 함수끝[틀함수[marco_ÍNDICE]]) { erro_VALOR("instruction pointer out of range"); return 0; }
        marco_cargo[marco_ÍNDICE]++; return Ficheiro[Posición];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void mover_VALOR(int Posición) {
        int FUNCIÓN_VALOR = 틀함수[marco_ÍNDICE];
        if (Posición < 함수시작[FUNCIÓN_VALOR] || Posición >= 함수끝[FUNCIÓN_VALOR] || 경계[Posición] != FUNCIÓN_VALOR + 1) erro_VALOR("invalid branch target");
        else marco_cargo[marco_ÍNDICE] = Posición;
    }
    static void 호출(int FUNCIÓN_VALOR) {
        if (marco_ÍNDICE == 31) { erro_VALOR("call stack limit (32)"); return; }
        int Seguinte_elemento = marco_ÍNDICE + 1;
        for (int 수 = 0; 수 < 128; 수++) local_TIPO[Seguinte_elemento * 128 + 수] = 0;
        for (int 수 = 함수인수수[FUNCIÓN_VALOR] - 1; 수 >= 0; 수--) {
            local_VALOR[Seguinte_elemento * 128 + 수] = 빼기(함수인수형[FUNCIÓN_VALOR * 16 + 수]); local_TIPO[Seguinte_elemento * 128 + 수] = 함수인수형[FUNCIÓN_VALOR * 16 + 수];
        }
        marco_ÍNDICE = Seguinte_elemento; 틀함수[marco_ÍNDICE] = FUNCIÓN_VALOR; marco_cargo[marco_ÍNDICE] = 함수시작[FUNCIÓN_VALOR]; marco_Montón[marco_ÍNDICE] = 0;
    }
    static void devolver_medida(int TIPO_VALOR) {
        if (TIPO_VALOR != 함수반환[틀함수[marco_ÍNDICE]]) { erro_VALOR("return type mismatch"); return; }
        int VALOR = TIPO_VALOR == 0 ? 0 : 빼기(TIPO_VALOR);
        marco_ÍNDICE--; if (marco_ÍNDICE >= 0 && TIPO_VALOR != 0) 넣기(VALOR, TIPO_VALOR);
    }
    static int[] fluxo_Ficheiro_nome = new int[64];
    static void Ficheiro_fluxo_CHAMAR(int propietario_VALOR, int Nome, int formato_VALOR, int Orde) {
        boolean Saída = Word_SMS(propietario_VALOR, "java/io/FileOutputStream");
        int 종류 = Saída ? 6 : 5;
        if (Orde == 183 && Word_SMS(Nome, "<init>")) {
            boolean 이어 = false;
            if (Saída && Word_SMS(formato_VALOR, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(formato_VALOR, "(Ljava/lang/String;)V")) { erro_VALOR("unsupported file stream constructor"); return; }
            int Ficheiro_introdución_nome = 빼기(2), fluxo_VALOR = 빼기(2);
            if (!obxecto_VALOR(Ficheiro_introdución_nome, 1) || !obxecto_VALOR(fluxo_VALOR, 종류) || ERRO) return;
            if (힙[fluxo_VALOR + 3] != 0) { erro_VALOR("file stream already initialized"); return; }
            int duración_VALOR = 힙[Ficheiro_introdución_nome + 1];
            if (duración_VALOR < 1 || duración_VALOR > 63) { erro_VALOR("invalid file name length"); return; }
            for (int 칸 = 0; 칸 < duración_VALOR; 칸++) {
                int VALOR = 힙[Ficheiro_introdución_nome + 2 + 칸];
                if (VALOR < 1 || VALOR > 127) { erro_VALOR("file stream paths currently require ASCII"); return; }
                fluxo_Ficheiro_nome[칸] = VALOR;
            }
            fluxo_Ficheiro_nome[duración_VALOR] = 0;
            int 서술자 = usuario.파일서술자열기(fluxo_Ficheiro_nome, Saída ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { erro_VALOR("FileNotFoundException: file open failed"); return; }
            힙[fluxo_VALOR + 2] = 서술자; 힙[fluxo_VALOR + 3] = 1;
            return;
        }
        if (Orde != 182) { erro_VALOR("invalid file stream invocation"); return; }
        int Acción = -1, VALOR = 0;
        if (Word_SMS(Nome, "close") && Word_SMS(formato_VALOR, "()V")) Acción = 0;
        if (!Saída && Word_SMS(Nome, "read") && Word_SMS(formato_VALOR, "()I")) Acción = 1;
        if (Saída && Word_SMS(Nome, "write") && Word_SMS(formato_VALOR, "(I)V")) { Acción = 2; VALOR = 빼기(1); }
        if (Acción < 0) { erro_VALOR("unsupported file stream method"); return; }
        int fluxo_VALOR = 빼기(2);
        if (!obxecto_VALOR(fluxo_VALOR, 종류) || ERRO) return;
        if (힙[fluxo_VALOR + 3] == 0) { erro_VALOR("uninitialized file stream"); return; }
        int 서술자 = 힙[fluxo_VALOR + 2];
        if (Acción == 0) {
            if (서술자 >= 0 && usuario.파일서술자닫기(서술자) < 0) erro_VALOR("IOException: close failed");
            힙[fluxo_VALOR + 2] = -1; return;
        }
        if (서술자 < 0) { erro_VALOR("IOException: stream closed"); return; }
        if (Acción == 1) {
            int RESULTANTE = usuario.파일한바이트읽기(서술자);
            if (RESULTANTE < -1) erro_VALOR("IOException: read failed"); else 넣기(RESULTANTE, 1);
        } else if (usuario.파일한바이트쓰기(서술자, VALOR) != 1) erro_VALOR("IOException: write failed");
    }
    static void 함수호출(int ÍNDICE, int Orde) {
        if (!cheque_constante(ÍNDICE, 10)) return;
        int propietario_VALOR = nome_de_clase_SMS(상가[ÍNDICE]), Nome = Material_de_referencia_nome(constante_SEGUNDO_VALOR[ÍNDICE]), formato_VALOR = Material_de_referencia_TIPO(constante_SEGUNDO_VALOR[ÍNDICE]);
        if (ERRO) return;
        if (같은말(propietario_VALOR, nome_de_clase)) {
            if (Orde != 184) { erro_VALOR("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < 함수수; 수++) if (같은말(Nome, 함수명[수]) && 같은말(formato_VALOR, 함수형[수])) {
                if ((함수권한[수] & 8) == 0) erro_VALOR("method is not static"); else 호출(수);
                return;
            }
            erro_VALOR("NoSuchMethodError"); return;
        }
        if (Word_SMS(propietario_VALOR, "java/io/FileInputStream") || Word_SMS(propietario_VALOR, "java/io/FileOutputStream")) {
            Ficheiro_fluxo_CHAMAR(propietario_VALOR, Nome, formato_VALOR, Orde); return;
        }
        if (Orde == 184 && Word_SMS(propietario_VALOR, "java/lang/Integer") && Word_SMS(Nome, "parseInt") && Word_SMS(formato_VALOR, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Orde == 182 && Word_SMS(propietario_VALOR, "java/io/PrintStream") && (Word_SMS(Nome, "println") || Word_SMS(Nome, "print"))) {
            int TIPO_VALOR = 0, VALOR = 0;
            if (Word_SMS(formato_VALOR, "(I)V")) { TIPO_VALOR = 1; VALOR = 빼기(1); }
            else if (Word_SMS(formato_VALOR, "(Z)V")) { TIPO_VALOR = 2; VALOR = 빼기(1); }
            else if (Word_SMS(formato_VALOR, "(C)V")) { TIPO_VALOR = 3; VALOR = 빼기(1); }
            else if (Word_SMS(formato_VALOR, "(Ljava/lang/String;)V")) { TIPO_VALOR = 4; VALOR = 빼기(2); }
            else if (!Word_SMS(formato_VALOR, "()V") || !Word_SMS(Nome, "println")) erro_VALOR("unsupported print descriptor");
            if (빼기(2) != -1) erro_VALOR("invalid PrintStream receiver");
            if (ERRO) return;
            if (TIPO_VALOR == 1) 자바도구.수쓰기(VALOR);
            if (TIPO_VALOR == 2) usuario.Escritura(VALOR == 0 ? "false" : "true");
            if (TIPO_VALOR == 3) usuario.escribir_carácter_VALOR(VALOR & 65535);
            if (TIPO_VALOR == 4) escribir_SMS(VALOR);
            if (Word_SMS(Nome, "println")) usuario.escribir_carácter_VALOR(10);
            return;
        }
        if (Orde == 182 && Word_SMS(propietario_VALOR, "java/lang/String")) {
            if (Word_SMS(Nome, "length") && Word_SMS(formato_VALOR, "()I")) {
                int Material_de_referencia = 빼기(2); if (obxecto_VALOR(Material_de_referencia, 1)) 넣기(힙[Material_de_referencia + 1], 1); return;
            }
            if (Word_SMS(Nome, "charAt") && Word_SMS(formato_VALOR, "(I)C")) {
                int subíndice_VALOR = 빼기(1), Material_de_referencia = 빼기(2);
                if (obxecto_VALOR(Material_de_referencia, 1)) {
                    if (subíndice_VALOR < 0 || subíndice_VALOR >= 힙[Material_de_referencia + 1]) erro_VALOR("StringIndexOutOfBoundsException"); else 넣기(힙[Material_de_referencia + 2 + subíndice_VALOR], 1);
                }
                return;
            }
        }
        if (Word_SMS(propietario_VALOR, "java/lang/StringBuilder")) {
            if (Orde == 183 && Word_SMS(Nome, "<init>") && Word_SMS(formato_VALOR, "()V")) { obxecto_VALOR(빼기(2), 4); return; }
            if (Orde == 182 && Word_SMS(Nome, "toString") && Word_SMS(formato_VALOR, "()Ljava/lang/String;")) {
                int Material_de_referencia = 빼기(2); if (obxecto_VALOR(Material_de_referencia, 4)) 넣기(힙[Material_de_referencia + 2] == 0 ? hospedar_carácter("") : 힙[Material_de_referencia + 2], 2); return;
            }
            if (Orde == 182 && Word_SMS(Nome, "append")) {
                int Texto = 0;
                if (Word_SMS(formato_VALOR, "(I)Ljava/lang/StringBuilder;")) Texto = díxito_carácter(빼기(1));
                else if (Word_SMS(formato_VALOR, "(Z)Ljava/lang/StringBuilder;")) Texto = hospedar_carácter(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(formato_VALOR, "(C)Ljava/lang/StringBuilder;")) {
                    int VALOR = 빼기(1); Texto = atribuír_Almacenamento(1, 1); if (!ERRO) 힙[Texto + 2] = VALOR & 65535;
                }
                else if (Word_SMS(formato_VALOR, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Texto = 빼기(2); if (Texto == 0) Texto = hospedar_carácter("null"); }
                else { erro_VALOR("unsupported StringBuilder append"); return; }
                int Material_de_referencia = 빼기(2); if (!obxecto_VALOR(Material_de_referencia, 4) || !obxecto_VALOR(Texto, 1)) return;
                int frontal_VALOR = 힙[Material_de_referencia + 2], frontal_VALOR_duración = frontal_VALOR == 0 ? 0 : 힙[frontal_VALOR + 1], ATRÁS_VALOR_duración = 힙[Texto + 1];
                int 새글 = atribuír_Almacenamento(1, frontal_VALOR_duración + ATRÁS_VALOR_duración); if (ERRO) return;
                for (int 수 = 0; 수 < frontal_VALOR_duración; 수++) 힙[새글 + 2 + 수] = 힙[frontal_VALOR + 2 + 수];
                for (int 수 = 0; 수 < ATRÁS_VALOR_duración; 수++) 힙[새글 + 2 + frontal_VALOR_duración + 수] = 힙[Texto + 2 + 수];
                힙[Material_de_referencia + 2] = 새글; 넣기(Material_de_referencia, 2); return;
            }
        }
        erro_VALOR("unsupported library method");
    }
    static int 배열칸(int Material_de_referencia, int subíndice_VALOR, int TIPO_VALOR) {
        if (!obxecto_VALOR(Material_de_referencia, TIPO_VALOR)) return 0;
        if (subíndice_VALOR < 0 || subíndice_VALOR >= 힙[Material_de_referencia + 1]) { erro_VALOR("ArrayIndexOutOfBoundsException"); return 0; }
        return Material_de_referencia + 2 + subíndice_VALOR;
    }
    static void executar_comando() {
        int 남음 = 500000;
        while (marco_ÍNDICE >= 0 && !ERRO) {
            if (--남음 == 0) { erro_VALOR("instruction limit (500000)"); break; }
            int Executar_2 = marco_cargo[marco_ÍNDICE], VALOR = 명바();
            if (ERRO) break;
            if (VALOR == 0) continue;
            if (VALOR == 1) { 넣기(0, 2); continue; }
            if (VALOR >= 2 && VALOR <= 8) { 넣기(VALOR - 3, 1); continue; }
            if (VALOR == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALOR == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALOR == 18 || VALOR == 19) {
                int 수 = VALOR == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= constante_CONTAR) erro_VALOR("invalid ldc constant");
                else if (constante_etiqueta[수] == 3) 넣기(상가[수], 1);
                else if (constante_etiqueta[수] == 8) 넣기(constante_SMS(상가[수]), 2);
                else erro_VALOR("unsupported ldc constant");
                continue;
            }
            if (VALOR == 21 || VALOR == 25) { 지역읽기(명바(), VALOR == 21 ? 1 : 2); continue; }
            if (VALOR >= 26 && VALOR <= 29) { 지역읽기(VALOR - 26, 1); continue; }
            if (VALOR >= 42 && VALOR <= 45) { 지역읽기(VALOR - 42, 2); continue; }
            if (VALOR == 54 || VALOR == 58) { escribir_local(명바(), VALOR == 54 ? 1 : 2); continue; }
            if (VALOR >= 59 && VALOR <= 62) { escribir_local(VALOR - 59, 1); continue; }
            if (VALOR >= 75 && VALOR <= 78) { escribir_local(VALOR - 75, 2); continue; }
            if (VALOR == 46 || VALOR == 50) {
                int subíndice_VALOR = 빼기(1), Material_de_referencia = 빼기(2), 칸 = 배열칸(Material_de_referencia, subíndice_VALOR, VALOR == 46 ? 2 : 3);
                if (!ERRO) 넣기(힙[칸], VALOR == 46 ? 1 : 2); continue;
            }
            if (VALOR == 79 || VALOR == 83) {
                int elemento_elemento = 빼기(VALOR == 79 ? 1 : 2), subíndice_VALOR = 빼기(1), Material_de_referencia = 빼기(2), 칸 = 배열칸(Material_de_referencia, subíndice_VALOR, VALOR == 79 ? 2 : 3);
                if (VALOR == 83 && elemento_elemento != 0) obxecto_VALOR(elemento_elemento, 1);
                if (!ERRO) 힙[칸] = elemento_elemento; continue;
            }
            if (VALOR == 87) { 빼기(0); continue; }
            if (VALOR == 89) { int 가 = 빼기(0), TIPO_VALOR = devolver_TIPO; 넣기(가, TIPO_VALOR); 넣기(가, TIPO_VALOR); continue; }
            if (VALOR == 95) { int 가 = 빼기(0), 가형 = devolver_TIPO, 나 = 빼기(0), 나형 = devolver_TIPO; 넣기(가, 가형); 넣기(나, 나형); continue; }
            if (VALOR == 96 || VALOR == 100 || VALOR == 104 || VALOR == 108 || VALOR == 112 || VALOR == 120
                || VALOR == 122 || VALOR == 124 || VALOR == 126 || VALOR == 128 || VALOR == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), RESULTANTE = 0;
                if ((VALOR == 108 || VALOR == 112) && 나 == 0) { erro_VALOR("ArithmeticException: / by zero"); continue; }
                if (VALOR == 96) RESULTANTE = 가 + 나;
                if (VALOR == 100) RESULTANTE = 가 - 나;
                if (VALOR == 104) RESULTANTE = 가 * 나;
                if (VALOR == 108) RESULTANTE = 가 / 나;
                if (VALOR == 112) RESULTANTE = 가 % 나;
                if (VALOR == 120) RESULTANTE = 가 << 나;
                if (VALOR == 122) RESULTANTE = 가 >> 나;
                if (VALOR == 124) RESULTANTE = 가 >>> 나;
                if (VALOR == 126) RESULTANTE = 가 & 나;
                if (VALOR == 128) RESULTANTE = 가 | 나;
                if (VALOR == 130) RESULTANTE = 가 ^ 나;
                넣기(RESULTANTE, 1); continue;
            }
            if (VALOR == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALOR == 132) {
                int local_Ámbito = 명바(), 증분 = (byte)명바(); 지역읽기(local_Ámbito, 1); 넣기(빼기(1) + 증분, 1); escribir_local(local_Ámbito, 1); continue;
            }
            if (VALOR >= 145 && VALOR <= 147) {
                int 수 = 빼기(1); 넣기(VALOR == 145 ? (byte)수 : VALOR == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (VALOR >= 153 && VALOR <= 167 || VALOR == 198 || VALOR == 199) {
                int destino_VALOR = Executar_2 + (short)명짧(); boolean 갈까 = VALOR == 167;
                if (VALOR >= 153 && VALOR <= 158) {
                    int 수 = 빼기(1); 갈까 = VALOR == 153 ? 수 == 0 : VALOR == 154 ? 수 != 0 : VALOR == 155 ? 수 < 0 : VALOR == 156 ? 수 >= 0 : VALOR == 157 ? 수 > 0 : 수 <= 0;
                } else if (VALOR >= 159 && VALOR <= 166) {
                    int 나 = 빼기(VALOR >= 165 ? 2 : 1), 가 = 빼기(VALOR >= 165 ? 2 : 1);
                    갈까 = VALOR == 159 || VALOR == 165 ? 가 == 나 : VALOR == 160 || VALOR == 166 ? 가 != 나 : VALOR == 161 ? 가 < 나 : VALOR == 162 ? 가 >= 나 : VALOR == 163 ? 가 > 나 : 가 <= 나;
                } else if (VALOR == 198 || VALOR == 199) { int 수 = 빼기(2); 갈까 = VALOR == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) mover_VALOR(destino_VALOR); continue;
            }
            if (VALOR == 172 || VALOR == 176 || VALOR == 177) { devolver_medida(VALOR == 172 ? 1 : VALOR == 176 ? 2 : 0); continue; }
            if (VALOR == 178) {
                int 수 = 명짧(); if (!cheque_constante(수, 9)) continue;
                if (!Word_SMS(nome_de_clase_SMS(상가[수]), "java/lang/System") || !Word_SMS(Material_de_referencia_nome(constante_SEGUNDO_VALOR[수]), "out")
                    || !Word_SMS(Material_de_referencia_TIPO(constante_SEGUNDO_VALOR[수]), "Ljava/io/PrintStream;")) erro_VALOR("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (VALOR == 182 || VALOR == 183 || VALOR == 184) { 함수호출(명짧(), VALOR); continue; }
            if (VALOR == 187) {
                int Nome = nome_de_clase_SMS(명짧());
                if (Word_SMS(Nome, "java/lang/StringBuilder")) 넣기(atribuír_Almacenamento(4, 1), 2);
                else if (Word_SMS(Nome, "java/io/FileInputStream") || Word_SMS(Nome, "java/io/FileOutputStream")) {
                    int Material_de_referencia = atribuír_Almacenamento(Word_SMS(Nome, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!ERRO) { 힙[Material_de_referencia + 2] = -1; 넣기(Material_de_referencia, 2); }
                } else erro_VALOR("unsupported object construction");
                continue;
            }
            if (VALOR == 188 || VALOR == 189) {
                if (VALOR == 188) { if (명바() != 10) erro_VALOR("only int[] newarray is supported"); }
                else if (!Word_SMS(nome_de_clase_SMS(명짧()), "java/lang/String")) erro_VALOR("only String[] anewarray is supported");
                int duración_VALOR = 빼기(1); 넣기(atribuír_Almacenamento(VALOR == 188 ? 2 : 3, duración_VALOR), 2); continue;
            }
            if (VALOR == 190) {
                int Material_de_referencia = 빼기(2);
                if (Material_de_referencia < 1 || Material_de_referencia >= 힙끝 - 1 || (힙[Material_de_referencia] != 2 && 힙[Material_de_referencia] != 3)) erro_VALOR("null or invalid array");
                else 넣기(힙[Material_de_referencia + 1], 1); continue;
            }
            if (VALOR == 192) {
                int Nome = nome_de_clase_SMS(명짧()), Material_de_referencia = 빼기(2);
                if (!Word_SMS(Nome, "java/lang/String")) erro_VALOR("unsupported checkcast");
                else if (Material_de_referencia != 0) obxecto_VALOR(Material_de_referencia, 1);
                넣기(Material_de_referencia, 2); continue;
            }
            erro_VALOR("unsupported bytecode");
        }
    }
    public static int Executar_2() {
        if (usuario.인수개수() == 1 && 자바도구.같음(usuario.Argumentos(0), "-version")) {
            usuario.Escritura("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (usuario.인수개수() < 1) { usuario.Escritura("Usage: java CLASS [ARGS]\n"); return 2; }
        int duración_VALOR = 자바도구.Nome(Ficheiro_nome_SMS, usuario.Argumentos(0));
        if (duración_VALOR < 1 || duración_VALOR > 57) { usuario.Escritura("java: invalid class name\n"); return 2; }
        Ficheiro_nome_SMS[duración_VALOR] = '.'; Ficheiro_nome_SMS[duración_VALOR + 1] = 'c'; Ficheiro_nome_SMS[duración_VALOR + 2] = 'l'; Ficheiro_nome_SMS[duración_VALOR + 3] = 'a'; Ficheiro_nome_SMS[duración_VALOR + 4] = 's'; Ficheiro_nome_SMS[duración_VALOR + 5] = 's';
        Tamaño = usuario.파일읽기(Ficheiro_nome_SMS, Ficheiro);
        if (Tamaño < 0) { usuario.Escritura("java: cannot read class: "); 자바도구.수쓰기(Tamaño); usuario.escribir_carácter_VALOR(10); return 1; }
        클래스읽기(); if (ERRO) return 1;
        int carácter_nome = constante_SMS(nome_de_clase);
        if (!ERRO && 힙[carácter_nome + 1] != duración_VALOR) erro_VALOR("class name does not match file");
        for (int 수 = 0; 수 < duración_VALOR && !ERRO; 수++) if (힙[carácter_nome + 2 + 수] != Ficheiro_nome_SMS[수]) erro_VALOR("class name does not match file");
        int introdución_p_VALOR = -1;
        for (int 수 = 0; 수 < 함수수; 수++) if (Word_SMS(함수명[수], "main") && Word_SMS(함수형[수], "([Ljava/lang/String;)V") && (함수권한[수] & 9) == 9) introdución_p_VALOR = 수;
        if (introdución_p_VALOR < 0) erro_VALOR("public static void main(String[] args) required");
        if (ERRO) return 1;
        int Argumentos = atribuír_Almacenamento(3, usuario.인수개수() - 1);
        for (int 수 = 1; 수 < usuario.인수개수() && !ERRO; 수++) 힙[Argumentos + 1 + 수] = hospedar_carácter(usuario.Argumentos(수));
        marco_ÍNDICE = 0; 틀함수[0] = introdución_p_VALOR; marco_cargo[0] = 함수시작[introdución_p_VALOR]; local_VALOR[0] = Argumentos; local_TIPO[0] = 2;
        executar_comando(); return ERRO ? 1 : 0;
    }
}
