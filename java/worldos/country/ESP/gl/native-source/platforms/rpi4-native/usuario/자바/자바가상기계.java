// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Ficheiro/스택/Material_de_referencia/ramificación 경계를 executar_comando 중 검사한다. */
public final class 자바가상기계 {
    static int[] Ficheiro = new int[16 * 16384], 임시파일 = new int[16384], Ficheiro_nome_SMS = new int[512];
    static int[] constante_etiqueta = new int[8192], 상가 = new int[8192], constante_SEGUNDO_VALOR = new int[8192], cadea_Material_de_referencia = new int[8192];
    static int[] 함수명 = new int[512], 함수형 = new int[512], 함수권한 = new int[512], 함수주인 = new int[512];
    static int[] 함수시작 = new int[512], 함수끝 = new int[512], 함수스택 = new int[512], 함수지역 = new int[512];
    static int[] 함수인수수 = new int[512], 함수인수형 = new int[8192], 함수반환 = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] local_VALOR = new int[16384], local_TIPO = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] 틀함수 = new int[128], marco_cargo = new int[128], marco_Montón = new int[128], marco_instrución = new int[128], iniciar_marco = new int[128];
    static int[] Clase_Definición_nome = new int[16], 종크기 = new int[16], 종부모 = new int[16], Clase_Definición_Estado = new int[16], 종칸수 = new int[16], iniciar_Clase_Definición = new int[16];
    static int[] Clase_interface = new int[16 * 16], Clase_interface_CONTAR = new int[16];
    static int[] 칸이름 = new int[512], 칸형 = new int[512], 칸주인 = new int[512], 칸권한 = new int[512], 칸위치 = new int[512], 칸값 = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], MATRIZ_elemento = new int[32768], Store_número_enteiro = new int[256];
    static int Tamaño, 읽기위치, 함수수, nome_de_clase, marco_ÍNDICE = -1, 힙끝 = 1, devolver_TIPO;
    static int Clase_Definición_CONTAR, 칸수, 잡기수, 현재읽는종, 던진객체, 잠시수, mostrar_CONTAR, Colección_CONTAR;
    static int ao_corrente_tema, tema_CONTAR = 1, introdución_Clase_Definición;
    static int[] tema_marco = new int[4], tema_Estado = new int[4], tema_obxecto = new int[4], tema_obxectivo = new int[4], 가닥대기 = new int[4];
    static boolean ERRO, modificar_solicitude;
    static int[] bloquear_propietario = new int[32768], 잠금깊이 = new int[32768], marco_bloquear = new int[128], Clase_bloquear = new int[16], Clase_tema = new int[16];

    static void erro_VALOR(String Word_SMS) {
        if (ERRO) return;
        int Categoría_CÓDIGO = 0;
        if (자바도구.같음(Word_SMS, "ArithmeticException: / by zero")) Categoría_CÓDIGO = 4;
        if (자바도구.같음(Word_SMS, "NullPointerException") || 자바도구.같음(Word_SMS, "null or invalid array")) Categoría_CÓDIGO = 5;
        if (자바도구.같음(Word_SMS, "ArrayIndexOutOfBoundsException")) Categoría_CÓDIGO = 7;
        if (자바도구.같음(Word_SMS, "StringIndexOutOfBoundsException")) Categoría_CÓDIGO = 8;
        if (자바도구.같음(Word_SMS, "NumberFormatException")) Categoría_CÓDIGO = 10;
        if (자바도구.같음(Word_SMS, "FileNotFoundException: file open failed")) Categoría_CÓDIGO = 12;
        if (자바도구.같음(Word_SMS, "IOException: stream closed") || 자바도구.같음(Word_SMS, "IOException: read failed") || 자바도구.같음(Word_SMS, "IOException: write failed")) Categoría_CÓDIGO = 11;
        if (자바도구.같음(Word_SMS, "ClassCastException")) Categoría_CÓDIGO = 14;
        if (자바도구.같음(Word_SMS, "NegativeArraySizeException")) Categoría_CÓDIGO = 15;
        if (Categoría_CÓDIGO != 0 && marco_ÍNDICE >= 0) { 예외던짐(Categoría_CÓDIGO, Word_SMS); return; }
        usuario.Escritura("JVM error: "); usuario.Escritura(Word_SMS); usuario.escribir_carácter_VALOR(10); ERRO = true;
    }
    static boolean clip(int Executar_2, int duración_VALOR) {
        if (Executar_2 < 0 || Executar_2 >= Ficheiro.length || duración_VALOR < 0) return false;
        int Clase_Definición = Executar_2 / 16384;
        return Executar_2 % 16384 <= 종크기[Clase_Definición] && duración_VALOR <= 종크기[Clase_Definición] - Executar_2 % 16384;
    }
    static int byte_VALOR() {
        if (!clip(읽기위치, 1)) { erro_VALOR("truncated class file"); return 0; }
        return Ficheiro[읽기위치++];
    }
    static int 짧은수() { return byte_VALOR() << 8 | byte_VALOR(); }
    static int número_enteiro() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int duración_VALOR) { if (!clip(읽기위치, duración_VALOR)) erro_VALOR("invalid attribute size"); else 읽기위치 += duración_VALOR; }
    static boolean cheque_constante(int 수, int 종류) {
        if (수 <= 0 || 수 >= constante_etiqueta.length || constante_etiqueta[수] != 종류) { erro_VALOR("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_intervalo(int Executar_2, int duración_VALOR, String Word_SMS) {
        if (!clip(Executar_2, duración_VALOR)) return false;
        int 읽는자리 = Executar_2, 끝 = Executar_2 + duración_VALOR;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Word_SMS.length(); Loop_ÍNDICE++) {
            int código_de_carácter = Word_SMS.charAt(Loop_ÍNDICE);
            if (código_de_carácter > 0 && código_de_carácter < 128) { if (읽는자리 >= 끝 || Ficheiro[읽는자리++] != código_de_carácter) return false; }
            else if (código_de_carácter < 2048) {
                if (읽는자리 + 2 > 끝 || Ficheiro[읽는자리++] != (192 | (código_de_carácter >> 6)) || Ficheiro[읽는자리++] != (128 | (código_de_carácter & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Ficheiro[읽는자리++] != (224 | (código_de_carácter >> 12)) || Ficheiro[읽는자리++] != (128 | ((código_de_carácter >> 6) & 63)) || Ficheiro[읽는자리++] != (128 | (código_de_carácter & 63))) return false;
        }
        return 읽는자리 == 끝;
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
    static int 상번호() { int VALOR = 짧은수(); return VALOR == 0 ? 0 : 현재읽는종 * 512 + VALOR; }
    static int 명상수() { return 함수주인[틀함수[marco_ÍNDICE]] * 512 + 명짧(); }
    static void 속성건너() {
        int elemento_CONTAR = 짧은수();
        for (int 수 = 0; 수 < elemento_CONTAR && !ERRO; 수++) { cheque_constante(상번호(), 1); 건너(número_enteiro()); }
    }
    static int comando_duración(int VALOR) {
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
    static int cargo_número_enteiro(int 읽는자리) {
        if (!clip(읽는자리, 4)) { erro_VALOR("truncated bytecode operand"); return 0; }
        return Ficheiro[읽는자리] << 24 | Ficheiro[읽는자리 + 1] << 16 | Ficheiro[읽는자리 + 2] << 8 | Ficheiro[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Executar_2, int 끝) {
        int VALOR = Ficheiro[읽는자리], duración_VALOR = comando_duración(VALOR);
        if (VALOR == 170 || VALOR == 171) {
            int BASE_cargo = 읽는자리 + 1;
            while ((BASE_cargo - Executar_2) % 4 != 0) BASE_cargo++;
            if (끝 - BASE_cargo < (VALOR == 170 ? 12 : 8)) return 0;
            int introdución_CONTAR = VALOR == 170 ? cargo_número_enteiro(BASE_cargo + 8) - cargo_número_enteiro(BASE_cargo + 4) + 1 : cargo_número_enteiro(BASE_cargo + 4);
            if (introdución_CONTAR < 0 || introdución_CONTAR > 2048) return 0;
            duración_VALOR = BASE_cargo - 읽는자리 + (VALOR == 170 ? 12 + 4 * introdución_CONTAR : 8 + 8 * introdución_CONTAR);
        }
        if (VALOR == 196 && 읽는자리 + 1 < 끝) {
            int Word_datos = Ficheiro[읽는자리 + 1]; duración_VALOR = Word_datos == 132 ? 6 : (Word_datos == 21 || Word_datos == 25 || Word_datos == 54 || Word_datos == 58) ? 4 : 0;
        }
        return duración_VALOR > 0 && duración_VALOR <= 끝 - 읽는자리 ? duración_VALOR : 0;
    }
    static void cheque_destino_VALOR(int destino_VALOR, int FUNCIÓN_VALOR) {
        if (destino_VALOR < 함수시작[FUNCIÓN_VALOR] || destino_VALOR >= 함수끝[FUNCIÓN_VALOR] || 경계[destino_VALOR] != FUNCIÓN_VALOR + 1) erro_VALOR("invalid branch target");
    }
    static void 클래스읽기(int Clase_Definición) {
        현재읽는종 = Clase_Definición; 읽기위치 = Clase_Definición * 16384; Tamaño = 읽기위치 + 종크기[Clase_Definición];
        if (número_enteiro() != 0xcafebabe) { erro_VALOR("not a class file"); return; }
        int 부판 = 짧은수(), versión_VALOR = 짧은수();
        if (versión_VALOR < 45 || versión_VALOR > 52 || 부판 != 0) { erro_VALOR("supported class versions: 45..52, minor 0"); return; }
        int constante_CONTAR = 짧은수(), BASE_cargo = Clase_Definición * 512;
        if (constante_CONTAR < 1 || constante_CONTAR > 512) { erro_VALOR("constant pool limit (511)"); return; }
        for (int introdución_CONTAR = 1; introdución_CONTAR < constante_CONTAR && !ERRO; introdución_CONTAR++) {
            int 수 = BASE_cargo + introdución_CONTAR, 종류 = byte_VALOR(); constante_etiqueta[수] = 종류;
            if (종류 == 1) { constante_SEGUNDO_VALOR[수] = 짧은수(); 상가[수] = 읽기위치; 건너(constante_SEGUNDO_VALOR[수]); }
            else if (종류 == 3) 상가[수] = número_enteiro();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); constante_SEGUNDO_VALOR[수] = 상번호(); }
            else erro_VALOR("unsupported constant type");
        }
        int permiso_VALOR = 짧은수();
        if ((permiso_VALOR & (0x2000 | 0x4000)) != 0) erro_VALOR("annotation/enum class unsupported");
        Clase_Definición_nome[Clase_Definición] = nome_de_clase_SMS(상번호());
        종부모[Clase_Definición] = nome_de_clase_SMS(상번호());
        int interface_CONTAR = 짧은수(); if (interface_CONTAR > 16) { erro_VALOR("interface count limit"); return; }
        Clase_interface_CONTAR[Clase_Definición] = interface_CONTAR;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < interface_CONTAR; Loop_ÍNDICE++) Clase_interface[Clase_Definición * 16 + Loop_ÍNDICE] = nome_de_clase_SMS(상번호());
        int campo_CONTAR = 짧은수();
        if (campo_CONTAR > 512 - 칸수) { erro_VALOR("field count limit (512)"); return; }
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < campo_CONTAR && !ERRO; Loop_ÍNDICE++) {
            int Ficheiro_ÍNDICE = 칸수++; 칸주인[Ficheiro_ÍNDICE] = Clase_Definición; 칸권한[Ficheiro_ÍNDICE] = 짧은수(); 칸이름[Ficheiro_ÍNDICE] = 상번호(); 칸형[Ficheiro_ÍNDICE] = 상번호();
            cheque_constante(칸이름[Ficheiro_ÍNDICE], 1); cheque_constante(칸형[Ficheiro_ÍNDICE], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[칸형[Ficheiro_ÍNDICE]]; int Categoría_CÓDIGO = 서술형(읽기위치 + constante_SEGUNDO_VALOR[칸형[Ficheiro_ÍNDICE]], false); 읽기위치 = 보존값;
            if ((칸권한[Ficheiro_ÍNDICE] & 8) == 0) 칸위치[Ficheiro_ÍNDICE] = 종칸수[Clase_Definición]++;
            int atributo_datos = 짧은수();
            for (int interna_cargo = 0; interna_cargo < atributo_datos && !ERRO; interna_cargo++) {
                int nome_constante = 상번호(), 유효길이 = número_enteiro();
                if (Word_SMS(nome_constante, "ConstantValue") && 유효길이 == 2) {
                    int datos_VALOR = 상번호();
                    if (Categoría_CÓDIGO == 1 && cheque_constante(datos_VALOR, 3)) 칸값[Ficheiro_ÍNDICE] = 상가[datos_VALOR];
                    else if (Categoría_CÓDIGO == 2 && cheque_constante(datos_VALOR, 8)) 칸값[Ficheiro_ÍNDICE] = constante_SMS(상가[datos_VALOR]);
                } else 건너(유효길이);
            }
        }
        int elemento_CONTAR = 짧은수();
        if (elemento_CONTAR > 512 - 함수수) { erro_VALOR("method count limit (512)"); return; }
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < elemento_CONTAR && !ERRO; Loop_ÍNDICE++) {
            int 수 = 함수수++; 함수주인[수] = Clase_Definición;
            함수권한[수] = 짧은수(); 함수명[수] = 상번호(); 함수형[수] = 상번호();
            cheque_constante(함수명[수], 1); 서술읽기(수);
            if ((함수권한[수] & 8) == 0) {
                if (함수인수수[수] == 16) { erro_VALOR("too many instance method arguments"); return; }
                for (int Comparación_cargo = 함수인수수[수]; Comparación_cargo > 0; Comparación_cargo--) 함수인수형[수 * 16 + Comparación_cargo] = 함수인수형[수 * 16 + Comparación_cargo - 1];
                함수인수형[수 * 16] = 2; 함수인수수[수]++;
            }
            if ((함수권한[수] & 0x100) != 0) erro_VALOR("user native method unsupported");
            if (Word_SMS(함수명[수], "<clinit>")) iniciar_Clase_Definición[Clase_Definición] = 수 + 1;
            for (int frontal_VALOR = 0; frontal_VALOR < 수; frontal_VALOR++) if (함수주인[frontal_VALOR] == Clase_Definición && 같은말(함수명[frontal_VALOR], 함수명[수]) && 같은말(함수형[frontal_VALOR], 함수형[수])) erro_VALOR("duplicate method");
            int atributo_CONTAR = 짧은수();
            for (int atributo_VALOR = 0; atributo_VALOR < atributo_CONTAR && !ERRO; atributo_VALOR++) {
                int Nome = 상번호(), duración_VALOR = número_enteiro(), Executar_2 = 읽기위치;
                if (!clip(Executar_2, duración_VALOR)) { erro_VALOR("truncated method attribute"); break; }
                if (Word_SMS(Nome, "Code")) {
                    if (함수시작[수] != 0) erro_VALOR("duplicate Code attribute");
                    함수스택[수] = 짧은수(); 함수지역[수] = 짧은수(); int CÓDIGO_duración = número_enteiro();
                    if (함수스택[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || CÓDIGO_duración < 1 || CÓDIGO_duración > 8192) erro_VALOR("method memory limits exceeded");
                    함수시작[수] = 읽기위치; 건너(CÓDIGO_duración); 함수끝[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { erro_VALOR("exception table limit"); return; }
                    for (int interna_cargo = 0; interna_cargo < 잡는수; interna_cargo++) {
                        int erro_Material_de_referencia = 잡기수++; 잡기함수[erro_Material_de_referencia] = 수;
                        잡기시작[erro_Material_de_referencia] = 함수시작[수] + 짧은수(); 잡기끝[erro_Material_de_referencia] = 함수시작[수] + 짧은수();
                        잡기위치[erro_Material_de_referencia] = 함수시작[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[erro_Material_de_referencia] = 부호값 == 0 ? 0 : nome_de_clase_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != Executar_2 + duración_VALOR) erro_VALOR("Code attribute size mismatch");
                } else 건너(duración_VALOR);
            }
            if ((함수권한[수] & 0x400) != 0) continue;
            if (함수시작[수] == 0) erro_VALOR("missing Code attribute");
            int 칸 = 함수시작[수];
            while (칸 < 함수끝[수] && !ERRO) {
                int duración_VALOR = 길이읽기(칸, 함수시작[수], 함수끝[수]);
                if (duración_VALOR == 0) { erro_VALOR("unsupported or truncated bytecode"); break; }
                경계[칸] = 수 + 1; 칸 += duración_VALOR;
            }
            칸 = 함수시작[수];
            while (칸 < 함수끝[수] && !ERRO) {
                int VALOR = Ficheiro[칸];
                if (VALOR >= 153 && VALOR <= 167 || VALOR == 198 || VALOR == 199) cheque_destino_VALOR(칸 + (short)(Ficheiro[칸 + 1] << 8 | Ficheiro[칸 + 2]), 수);
                if (VALOR == 200) cheque_destino_VALOR(칸 + cargo_número_enteiro(칸 + 1), 수);
                if (VALOR == 170 || VALOR == 171) {
                    int 읽는자리 = 칸 + 1; while ((읽는자리 - 함수시작[수]) % 4 != 0) 읽는자리++;
                    cheque_destino_VALOR(칸 + cargo_número_enteiro(읽는자리), 수);
                    int introdución_CONTAR = VALOR == 170 ? cargo_número_enteiro(읽는자리 + 8) - cargo_número_enteiro(읽는자리 + 4) + 1 : cargo_número_enteiro(읽는자리 + 4);
                    읽는자리 += VALOR == 170 ? 12 : 8;
                    for (int interna_cargo = 0; interna_cargo < introdución_CONTAR; interna_cargo++) cheque_destino_VALOR(칸 + cargo_número_enteiro(읽는자리 + interna_cargo * (VALOR == 170 ? 4 : 8) + (VALOR == 170 ? 0 : 4)), 수);
                }
                칸 += 길이읽기(칸, 함수시작[수], 함수끝[수]);
            }
            for (int interna_cargo = 0; interna_cargo < 잡기수; interna_cargo++) if (잡기함수[interna_cargo] == 수) {
                cheque_destino_VALOR(잡기시작[interna_cargo], 수); cheque_destino_VALOR(잡기위치[interna_cargo], 수);
                if (잡기끝[interna_cargo] != 함수끝[수]) cheque_destino_VALOR(잡기끝[interna_cargo], 수);
                if (잡기시작[interna_cargo] >= 잡기끝[interna_cargo]) erro_VALOR("invalid exception range");
            }
        }
        if (!ERRO) 속성건너();
        if (읽기위치 != Tamaño) erro_VALOR("extra class file data");
    }
    static int atribuír_Almacenamento(int 종류, int duración_VALOR) { return 새기억(종류, duración_VALOR); }
    static boolean obxecto_VALOR(int Material_de_referencia, int 종류) {
        if (!객체유효(Material_de_referencia)) return false;
        if (힙[Material_de_referencia] != 종류) { erro_VALOR("object type mismatch"); return false; }
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
        if (devolver_TIPO == 2) protexer_VALOR(스택값[칸]);
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
        if (marco_ÍNDICE % 32 == 31) { erro_VALOR("call stack limit (32)"); return; }
        int Seguinte_elemento = marco_ÍNDICE + 1;
        for (int 수 = 0; 수 < 128; 수++) local_TIPO[Seguinte_elemento * 128 + 수] = 0;
        for (int 수 = 함수인수수[FUNCIÓN_VALOR] - 1; 수 >= 0; 수--) {
            local_VALOR[Seguinte_elemento * 128 + 수] = 빼기(함수인수형[FUNCIÓN_VALOR * 16 + 수]); local_TIPO[Seguinte_elemento * 128 + 수] = 함수인수형[FUNCIÓN_VALOR * 16 + 수];
        }
        if (ERRO) return;
        marco_ÍNDICE = Seguinte_elemento; iniciar_marco[marco_ÍNDICE] = 0; 틀함수[marco_ÍNDICE] = FUNCIÓN_VALOR; marco_cargo[marco_ÍNDICE] = 함수시작[FUNCIÓN_VALOR]; marco_Montón[marco_ÍNDICE] = 0;
    }
    static void devolver_medida(int TIPO_VALOR) {
        if (TIPO_VALOR != 함수반환[틀함수[marco_ÍNDICE]]) { erro_VALOR("return type mismatch"); return; }
        int VALOR = TIPO_VALOR == 0 ? 0 : 빼기(TIPO_VALOR);
        if (iniciar_marco[marco_ÍNDICE] != 0) Clase_Definición_Estado[iniciar_marco[marco_ÍNDICE] - 1] = 2;
        if (marco_bloquear[marco_ÍNDICE] != 0) { liberar_bloquear(marco_bloquear[marco_ÍNDICE]); marco_bloquear[marco_ÍNDICE] = 0; }
        marco_ÍNDICE--; if (marco_ÍNDICE >= ao_corrente_tema * 32 && TIPO_VALOR != 0) 넣기(VALOR, TIPO_VALOR);
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
                if (VALOR < 1) { erro_VALOR("invalid file stream path"); return; }
                fluxo_Ficheiro_nome[칸] = VALOR;
            }
            fluxo_Ficheiro_nome[duración_VALOR] = 0;
            int 서술자 = usuario.파일서술자열기(fluxo_Ficheiro_nome, Saída ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { erro_VALOR("FileNotFoundException: file open failed"); return; }
            힙[fluxo_VALOR + 2] = 서술자; 힙[fluxo_VALOR + 3] = 1;
            return;
        }
        if (Orde != 182) { erro_VALOR("invalid file stream invocation"); return; }
        if ((Saída && Word_SMS(Nome, "write") || !Saída && Word_SMS(Nome, "read"))
            && (Word_SMS(formato_VALOR, Saída ? "([B)V" : "([B)I") || Word_SMS(formato_VALOR, Saída ? "([BII)V" : "([BII)I"))) {
            boolean clip_VALOR = Word_SMS(formato_VALOR, Saída ? "([BII)V" : "([BII)I");
            int introdución_CONTAR = clip_VALOR ? 빼기(1) : 0, 시작점 = clip_VALOR ? 빼기(1) : 0, datos_MATRIZ = 빼기(2), obxecto_Material_de_referencia = 빼기(2);
            if (!obxecto_VALOR(datos_MATRIZ, 20) || !obxecto_VALOR(obxecto_Material_de_referencia, 종류)) return;
            if (!clip_VALOR) introdución_CONTAR = 힙[datos_MATRIZ + 1];
            if (시작점 < 0 || introdución_CONTAR < 0 || 시작점 > 힙[datos_MATRIZ + 1] - introdución_CONTAR) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[obxecto_Material_de_referencia + 3] == 0 || 힙[obxecto_Material_de_referencia + 2] < 0) { erro_VALOR("IOException: stream closed"); return; }
            int Completadas_CONTAR = 0;
            while (Completadas_CONTAR < introdución_CONTAR && !ERRO) {
                int 반환값 = Saída ? usuario.파일한바이트쓰기(힙[obxecto_Material_de_referencia + 2], 힙[datos_MATRIZ + 2 + 시작점 + Completadas_CONTAR]) : usuario.파일한바이트읽기(힙[obxecto_Material_de_referencia + 2]);
                if (반환값 < 0) { erro_VALOR(Saída ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!Saída && 반환값 == 256) break;
                if (!Saída) 힙[datos_MATRIZ + 2 + 시작점 + Completadas_CONTAR] = (byte)반환값;
                Completadas_CONTAR++;
            }
            if (!Saída) 넣기(introdución_CONTAR != 0 && Completadas_CONTAR == 0 ? -1 : Completadas_CONTAR, 1);
            return;
        }
        if (Saída && Word_SMS(Nome, "flush") && Word_SMS(formato_VALOR, "()V")) { int obxecto_Material_de_referencia = 빼기(2); if (obxecto_VALOR(obxecto_Material_de_referencia, 종류) && 힙[obxecto_Material_de_referencia + 2] < 0) erro_VALOR("IOException: stream closed"); return; }
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
            if (RESULTANTE < -1) erro_VALOR("IOException: read failed"); else 넣기(RESULTANTE == 256 ? -1 : RESULTANTE, 1);
        } else if (usuario.파일한바이트쓰기(서술자, VALOR) != 1) erro_VALOR("IOException: write failed");
    }
    static void 함수호출(int ÍNDICE, int Orde) {
        if (ÍNDICE <= 0 || ÍNDICE >= constante_etiqueta.length || (constante_etiqueta[ÍNDICE] != 10 && constante_etiqueta[ÍNDICE] != 11)) { erro_VALOR("invalid method reference"); return; }
        int propietario_VALOR = nome_de_clase_SMS(상가[ÍNDICE]), Nome = Material_de_referencia_nome(constante_SEGUNDO_VALOR[ÍNDICE]), formato_VALOR = Material_de_referencia_TIPO(constante_SEGUNDO_VALOR[ÍNDICE]);
        if (ERRO) return;
        if (기본호출(propietario_VALOR, Nome, formato_VALOR, Orde)) return;
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
        int Clase_Definición = Busca_Clase_Definición(propietario_VALOR); if (Clase_Definición < 0 || ERRO) return;
        int Ficheiro_ÍNDICE = 함수찾기(Clase_Definición, Nome, formato_VALOR);
        if (Ficheiro_ÍNDICE < 0) {
            for (int código_de_carácter = Clase_Definición, introdución_CONTAR = 0; código_de_carácter >= 0 && introdución_CONTAR < 16; introdución_CONTAR++, código_de_carácter = 부모종(código_de_carácter))
                if (Word_SMS(종부모[código_de_carácter], "java/lang/Thread")) { 가닥호출(Nome, formato_VALOR, Orde); return; }
            erro_VALOR("NoSuchMethodError"); return;
        }
        if (((함수권한[Ficheiro_ÍNDICE] & 8) != 0) != (Orde == 184)) { erro_VALOR("method static/instance mismatch"); return; }
        if (Orde == 184) { if (!iniciar(함수주인[Ficheiro_ÍNDICE], marco_instrución[marco_ÍNDICE])) return; }
        else {
            int 읽는자리 = marco_Montón[marco_ÍNDICE] - 함수인수수[Ficheiro_ÍNDICE];
            if (읽는자리 < 0 || 스택형[marco_ÍNDICE * 128 + 읽는자리] != 2) { erro_VALOR("invalid method receiver"); return; }
            int obxecto_Material_de_referencia = 스택값[marco_ÍNDICE * 128 + 읽는자리];
            if (!객체유효(obxecto_Material_de_referencia)) return;
            if (힙[obxecto_Material_de_referencia] < 32 || !종포함(힙[obxecto_Material_de_referencia] - 32, propietario_VALOR)) { erro_VALOR("method receiver type mismatch"); return; }
            if (Orde != 183) Ficheiro_ÍNDICE = 함수찾기(힙[obxecto_Material_de_referencia] - 32, Nome, formato_VALOR);
        }
        if (Ficheiro_ÍNDICE < 0 || (함수권한[Ficheiro_ÍNDICE] & 0x400) != 0) { erro_VALOR("AbstractMethodError"); return; }
        int bloquear_Material_de_referencia = 0;
        if ((함수권한[Ficheiro_ÍNDICE] & 32) != 0) {
            if (Orde == 184) { int código_de_carácter = 함수주인[Ficheiro_ÍNDICE]; if (Clase_bloquear[código_de_carácter] == 0) Clase_bloquear[código_de_carácter] = atribuír_Almacenamento(8, 0); bloquear_Material_de_referencia = Clase_bloquear[código_de_carácter]; }
            else bloquear_Material_de_referencia = 스택값[marco_ÍNDICE * 128 + marco_Montón[marco_ÍNDICE] - 함수인수수[Ficheiro_ÍNDICE]];
            if (!잠금얻기(bloquear_Material_de_referencia)) { if (!ERRO) marco_cargo[marco_ÍNDICE] = marco_instrución[marco_ÍNDICE]; return; }
        }
        호출(Ficheiro_ÍNDICE); if (!ERRO) marco_bloquear[marco_ÍNDICE] = bloquear_Material_de_referencia;
    }
    static boolean 배열저장가능(int MATRIZ_Material_de_referencia, int datos_VALOR) {
        if (datos_VALOR == 0 || MATRIZ_elemento[MATRIZ_Material_de_referencia] == 0) return true;
        boolean 성공여부 = MATRIZ_elemento[MATRIZ_Material_de_referencia] == -1 ? (datos_VALOR > 0 && datos_VALOR < 힙끝 && 힙[datos_VALOR] == 1) : 맞는객체(datos_VALOR, MATRIZ_elemento[MATRIZ_Material_de_referencia]);
        if (!성공여부 && !ERRO) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int 배열칸(int Material_de_referencia, int subíndice_VALOR, int TIPO_VALOR) {
        if (!obxecto_VALOR(Material_de_referencia, TIPO_VALOR)) return 0;
        if (subíndice_VALOR < 0 || subíndice_VALOR >= 힙[Material_de_referencia + 1]) { erro_VALOR("ArrayIndexOutOfBoundsException"); return 0; }
        return Material_de_referencia + 2 + subíndice_VALOR;
    }
    static void executar_comando() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (ERRO) { if (던진객체 != 0) agarradoira_excepción(); if (ERRO || marco_ÍNDICE < ao_corrente_tema * 32) break; }
            if (marco_ÍNDICE < ao_corrente_tema * 32 || modificar_solicitude || --조각 == 0) { if (!mudar_tema()) break; 조각 = 100; }
            if (marco_ÍNDICE == 0 && Clase_Definición_Estado[introdución_Clase_Definición] != 2 && !iniciar(introdución_Clase_Definición, marco_cargo[marco_ÍNDICE])) continue;
            if (marco_ÍNDICE == ao_corrente_tema * 32 && ao_corrente_tema != 0 && (함수권한[틀함수[marco_ÍNDICE]] & 32) != 0 && marco_bloquear[marco_ÍNDICE] == 0) {
                int obxecto_Material_de_referencia = tema_obxectivo[ao_corrente_tema]; if (!잠금얻기(obxecto_Material_de_referencia)) { if (ERRO) break; continue; } marco_bloquear[marco_ÍNDICE] = obxecto_Material_de_referencia;
            }
            잠시수 = 0;
            if (--남음 == 0) { erro_VALOR("instruction limit (500000)"); break; }
            int Executar_2 = marco_cargo[marco_ÍNDICE]; marco_instrución[marco_ÍNDICE] = Executar_2; int VALOR = 명바();
            if (ERRO) break;
            if (VALOR == 0) continue;
            if (VALOR == 1) { 넣기(0, 2); continue; }
            if (VALOR >= 2 && VALOR <= 8) { 넣기(VALOR - 3, 1); continue; }
            if (VALOR == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALOR == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALOR == 18 || VALOR == 19) {
                int 수 = 함수주인[틀함수[marco_ÍNDICE]] * 512 + (VALOR == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= constante_etiqueta.length) erro_VALOR("invalid ldc constant");
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
            if (VALOR == 46 || VALOR >= 50 && VALOR <= 53) {
                int introdución_cargo = 빼기(1), obxecto_Material_de_referencia = 빼기(2), Categoría_CÓDIGO = VALOR == 46 ? 2 : VALOR == 50 ? 3 : VALOR == 51 ? 20 : VALOR == 52 ? 22 : 23;
                if (VALOR == 51 && obxecto_Material_de_referencia > 0 && obxecto_Material_de_referencia < 힙끝 && 힙[obxecto_Material_de_referencia] == 21) Categoría_CÓDIGO = 21;
                int 읽는자리 = 배열칸(obxecto_Material_de_referencia, introdución_cargo, Categoría_CÓDIGO); if (!ERRO) 넣기(힙[읽는자리], VALOR == 50 ? 2 : 1); continue;
            }
            if (VALOR == 79 || VALOR >= 83 && VALOR <= 86) {
                int introdución_Material_de_referencia = 빼기(VALOR == 83 ? 2 : 1), introdución_cargo = 빼기(1), obxecto_Material_de_referencia = 빼기(2), Categoría_CÓDIGO = VALOR == 79 ? 2 : VALOR == 83 ? 3 : VALOR == 84 ? 20 : VALOR == 85 ? 22 : 23;
                if (VALOR == 84 && obxecto_Material_de_referencia > 0 && obxecto_Material_de_referencia < 힙끝 && 힙[obxecto_Material_de_referencia] == 21) Categoría_CÓDIGO = 21;
                int 읽는자리 = 배열칸(obxecto_Material_de_referencia, introdución_cargo, Categoría_CÓDIGO);
                if (!ERRO && Categoría_CÓDIGO == 3 && !배열저장가능(obxecto_Material_de_referencia, introdución_Material_de_referencia)) continue;
                if (!ERRO) 힙[읽는자리] = Categoría_CÓDIGO == 20 ? (byte)introdución_Material_de_referencia : Categoría_CÓDIGO == 21 ? introdución_Material_de_referencia & 1 : Categoría_CÓDIGO == 22 ? (char)introdución_Material_de_referencia : Categoría_CÓDIGO == 23 ? (short)introdución_Material_de_referencia : introdución_Material_de_referencia;
                continue;
            }
            if (VALOR >= 87 && VALOR <= 95) { Montón_instrución(VALOR); continue; }
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
            if (VALOR >= 178 && VALOR <= 181) { 필드호출(명상수(), VALOR, Executar_2); continue; }
            if (VALOR >= 182 && VALOR <= 185) {
                int 부호값 = 명상수();
                if (VALOR == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { erro_VALOR("invalid invokeinterface operands"); continue; } }
                함수호출(부호값, VALOR); continue;
            }
            if (VALOR == 187) { 새객체(nome_de_clase_SMS(명상수()), Executar_2); continue; }
            if (VALOR == 188 || VALOR == 189) {
                int Categoría_CÓDIGO = 3, compoñente = 0;
                if (VALOR == 188) { int 임시값 = 명바(); Categoría_CÓDIGO = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else compoñente = nome_de_clase_SMS(명상수());
                if (Categoría_CÓDIGO == 0) { erro_VALOR("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), obxecto_Material_de_referencia = atribuír_Almacenamento(Categoría_CÓDIGO, 유효길이); if (!ERRO) MATRIZ_elemento[obxecto_Material_de_referencia] = compoñente; 넣기(obxecto_Material_de_referencia, 2); continue;
            }
            if (VALOR == 190) {
                int obxecto_Material_de_referencia = 빼기(2);
                if (객체유효(obxecto_Material_de_referencia)) { int Comparación_cargo = 힙[obxecto_Material_de_referencia]; if (Comparación_cargo != 2 && Comparación_cargo != 3 && (Comparación_cargo < 20 || Comparación_cargo > 23)) erro_VALOR("not an array"); else 넣기(힙[obxecto_Material_de_referencia + 1], 1); }
                continue;
            }
            if (VALOR == 191) {
                int obxecto_Material_de_referencia = 빼기(2); if (객체유효(obxecto_Material_de_referencia)) { if (힙[obxecto_Material_de_referencia] != 9) erro_VALOR("athrow requires supported Throwable"); else { 던진객체 = obxecto_Material_de_referencia; ERRO = true; } }
                continue;
            }
            if (VALOR == 192 || VALOR == 193) {
                int nome_constante = nome_de_clase_SMS(명상수()), obxecto_Material_de_referencia = 빼기(2); boolean CORRESP = 맞는객체(obxecto_Material_de_referencia, nome_constante);
                if (VALOR == 193) 넣기(obxecto_Material_de_referencia != 0 && CORRESP ? 1 : 0, 1);
                else { if (!CORRESP && !ERRO) erro_VALOR("ClassCastException"); 넣기(obxecto_Material_de_referencia, 2); }
                continue;
            }
            if (VALOR == 170 || VALOR == 171) {
                int 읽는자리 = Executar_2 + 1, Ficheiro_ÍNDICE = 틀함수[marco_ÍNDICE], Chave_Material_de_referencia = 빼기(1);
                while ((읽는자리 - 함수시작[Ficheiro_ÍNDICE]) % 4 != 0) 읽는자리++;
                int obxectivo_ENDEREZO = cargo_número_enteiro(읽는자리);
                if (VALOR == 170) { int 낮은값 = cargo_número_enteiro(읽는자리 + 4), 높은값 = cargo_número_enteiro(읽는자리 + 8); if (Chave_Material_de_referencia >= 낮은값 && Chave_Material_de_referencia <= 높은값) obxectivo_ENDEREZO = cargo_número_enteiro(읽는자리 + 12 + (Chave_Material_de_referencia - 낮은값) * 4); }
                else { int 총수 = cargo_número_enteiro(읽는자리 + 4); for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 총수; Loop_ÍNDICE++) if (cargo_número_enteiro(읽는자리 + 8 + Loop_ÍNDICE * 8) == Chave_Material_de_referencia) obxectivo_ENDEREZO = cargo_número_enteiro(읽는자리 + 12 + Loop_ÍNDICE * 8); }
                mover_VALOR(Executar_2 + obxectivo_ENDEREZO); continue;
            }
            if (VALOR == 200) { mover_VALOR(Executar_2 + cargo_número_enteiro(Executar_2 + 1)); continue; }
            if (VALOR == 194 || VALOR == 195) {
                int obxecto_Material_de_referencia = 빼기(2);
                if (VALOR == 195) liberar_bloquear(obxecto_Material_de_referencia);
                else if (!잠금얻기(obxecto_Material_de_referencia) && !ERRO) { 넣기(obxecto_Material_de_referencia, 2); marco_cargo[marco_ÍNDICE] = Executar_2; }
                continue;
            }
            if (VALOR == 196) {
                int comando_CÓDIGO = 명바(), introdución_cargo = 명짧();
                if (comando_CÓDIGO == 21 || comando_CÓDIGO == 25) 지역읽기(introdución_cargo, comando_CÓDIGO == 21 ? 1 : 2);
                else if (comando_CÓDIGO == 54 || comando_CÓDIGO == 58) escribir_local(introdución_cargo, comando_CÓDIGO == 54 ? 1 : 2);
                else if (comando_CÓDIGO == 132) { int DELTA_VALOR = (short)명짧(); 지역읽기(introdución_cargo, 1); 넣기(빼기(1) + DELTA_VALOR, 1); escribir_local(introdución_cargo, 1); }
                else erro_VALOR("unsupported wide opcode");
                continue;
            }
            erro_VALOR("unsupported bytecode");
        }
    }
    static int Busca_Clase_Definición(int Nome) {
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Clase_Definición_CONTAR; Loop_ÍNDICE++) if (Clase_Definición_nome[Loop_ÍNDICE] != 0 && 같은말(Clase_Definición_nome[Loop_ÍNDICE], Nome)) return Loop_ÍNDICE;
        return carga_Clase_Definición(constante_SMS(Nome));
    }
    static int carga_Clase_Definición(int nome_cadea) {
        if (!obxecto_VALOR(nome_cadea, 1)) return -1;
        int duración_VALOR = 힙[nome_cadea + 1];
        if (duración_VALOR < 1 || duración_VALOR > 505 || Clase_Definición_CONTAR == 16) { erro_VALOR("class name/count limit"); return -1; }
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < duración_VALOR; Loop_ÍNDICE++) { int código_de_carácter = 힙[nome_cadea + 2 + Loop_ÍNDICE]; Ficheiro_nome_SMS[Loop_ÍNDICE] = código_de_carácter == '/' ? '.' : código_de_carácter; }
        Ficheiro_nome_SMS[duración_VALOR] = '.'; Ficheiro_nome_SMS[duración_VALOR + 1] = 'c'; Ficheiro_nome_SMS[duración_VALOR + 2] = 'l'; Ficheiro_nome_SMS[duración_VALOR + 3] = 'a'; Ficheiro_nome_SMS[duración_VALOR + 4] = 's'; Ficheiro_nome_SMS[duración_VALOR + 5] = 's'; Ficheiro_nome_SMS[duración_VALOR + 6] = 0;
        int Tamaño = usuario.파일읽기(Ficheiro_nome_SMS, 임시파일);
        if (Tamaño < 0) { erro_VALOR("ClassNotFoundException"); return -1; }
        int Clase_Definición = Clase_Definición_CONTAR++; 종크기[Clase_Definición] = Tamaño;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Tamaño; Loop_ÍNDICE++) Ficheiro[Clase_Definición * 16384 + Loop_ÍNDICE] = 임시파일[Loop_ÍNDICE];
        클래스읽기(Clase_Definición); if (ERRO) return -1;
        int real_datos = constante_SMS(Clase_Definición_nome[Clase_Definición]);
        if (!글같음(real_datos, nome_cadea, true)) { erro_VALOR("class name does not match file"); return -1; }
        int 부모 = 종부모[Clase_Definición];
        if (부모 != 0 && !Word_SMS(부모, "java/lang/Object") && !Word_SMS(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = Busca_Clase_Definición(부모);
            if (ERRO || 위 < 0) return -1;
            int 읽는자리 = 위, fase_CONTAR = 0;
            while (읽는자리 >= 0 && fase_CONTAR++ < 16) {
                if (읽는자리 == Clase_Definición) { erro_VALOR("cyclic inheritance"); return -1; }
                읽는자리 = 부모종(읽는자리);
            }
            int 시작변위 = 종칸수[위];
            for (int Ficheiro_ÍNDICE = 0; Ficheiro_ÍNDICE < 칸수; Ficheiro_ÍNDICE++) if (칸주인[Ficheiro_ÍNDICE] == Clase_Definición && (칸권한[Ficheiro_ÍNDICE] & 8) == 0) 칸위치[Ficheiro_ÍNDICE] += 시작변위;
            종칸수[Clase_Definición] += 시작변위;
        }
        return Clase_Definición;
    }
    static int 부모종(int Clase_Definición) {
        int Nome = 종부모[Clase_Definición];
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Clase_Definición_CONTAR; Loop_ÍNDICE++) if (Nome != 0 && Clase_Definición_nome[Loop_ÍNDICE] != 0 && 같은말(Clase_Definición_nome[Loop_ÍNDICE], Nome)) return Loop_ÍNDICE;
        return -1;
    }
    static int 함수찾기(int Clase_Definición, int Nome, int formato_VALOR) {
        for (int 깊이 = 0; Clase_Definición >= 0 && 깊이 < 16; 깊이++, Clase_Definición = 부모종(Clase_Definición)) {
            for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 함수수; Loop_ÍNDICE++) if (함수주인[Loop_ÍNDICE] == Clase_Definición && 같은말(함수명[Loop_ÍNDICE], Nome) && 같은말(함수형[Loop_ÍNDICE], formato_VALOR)) return Loop_ÍNDICE;
        }
        return -1;
    }
    static int 이름함수(int Clase_Definición, String Nome, String formato_VALOR) {
        for (int 깊이 = 0; Clase_Definición >= 0 && 깊이 < 16; 깊이++, Clase_Definición = 부모종(Clase_Definición))
            for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 함수수; Loop_ÍNDICE++) if (함수주인[Loop_ÍNDICE] == Clase_Definición && Word_SMS(함수명[Loop_ÍNDICE], Nome) && Word_SMS(함수형[Loop_ÍNDICE], formato_VALOR)) return Loop_ÍNDICE;
        return -1;
    }
    static int 형종류(int Nome) { return Ficheiro[상가[Nome]] == 'L' || Ficheiro[상가[Nome]] == '[' ? 2 : 1; }
    static boolean iniciar(int Clase_Definición, int comando_START) {
        if (Clase_Definición < 0 || ERRO) return false;
        if (Clase_Definición_Estado[Clase_Definición] == 3) { erro_VALOR("NoClassDefFoundError: initialization failed"); return false; }
        if (Clase_Definición_Estado[Clase_Definición] == 1 && Clase_tema[Clase_Definición] != ao_corrente_tema) { marco_cargo[marco_ÍNDICE] = comando_START; modificar_solicitude = true; return false; }
        if (Clase_Definición_Estado[Clase_Definición] != 0) return true;
        int 위 = 부모종(Clase_Definición);
        if (위 >= 0 && !iniciar(위, comando_START)) return false;
        Clase_Definición_Estado[Clase_Definición] = 1; Clase_tema[Clase_Definición] = ao_corrente_tema;
        if (iniciar_Clase_Definición[Clase_Definición] != 0) {
            marco_cargo[marco_ÍNDICE] = comando_START;
            호출(iniciar_Clase_Definición[Clase_Definición] - 1); if (!ERRO) iniciar_marco[marco_ÍNDICE] = Clase_Definición + 1;
            return false;
        }
        Clase_Definición_Estado[Clase_Definición] = 2; return true;
    }
    static void 필드호출(int ÍNDICE, int Orde, int Executar_2) {
        if (!cheque_constante(ÍNDICE, 9)) return;
        int propietario_VALOR = nome_de_clase_SMS(상가[ÍNDICE]), Nome = Material_de_referencia_nome(constante_SEGUNDO_VALOR[ÍNDICE]), formato_VALOR = Material_de_referencia_TIPO(constante_SEGUNDO_VALOR[ÍNDICE]);
        if (Word_SMS(propietario_VALOR, "java/lang/System") && (Word_SMS(Nome, "out") || Word_SMS(Nome, "err")) && Word_SMS(formato_VALOR, "Ljava/io/PrintStream;") && Orde == 178) { 넣기(-1, 2); return; }
        int Clase_Definición = Busca_Clase_Definición(propietario_VALOR); if (Clase_Definición < 0 || ERRO) return;
        int 찾음 = -1;
        for (int 읽는자리 = Clase_Definición, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = 부모종(읽는자리))
            for (int Ficheiro_ÍNDICE = 0; Ficheiro_ÍNDICE < 칸수; Ficheiro_ÍNDICE++) if (칸주인[Ficheiro_ÍNDICE] == 읽는자리 && 같은말(칸이름[Ficheiro_ÍNDICE], Nome) && 같은말(칸형[Ficheiro_ÍNDICE], formato_VALOR)) 찾음 = Ficheiro_ÍNDICE;
        if (찾음 < 0) { erro_VALOR("NoSuchFieldError"); return; }
        boolean estático_VALOR = Orde == 178 || Orde == 179;
        if (estático_VALOR != ((칸권한[찾음] & 8) != 0)) { erro_VALOR("field static/instance mismatch"); return; }
        if (estático_VALOR && !iniciar(칸주인[찾음], Executar_2)) return;
        int TIPO_VALOR = 형종류(formato_VALOR), VALOR = 0;
        if (Orde == 179 || Orde == 181) VALOR = 빼기(TIPO_VALOR);
        if (estático_VALOR) { if (Orde == 178) 넣기(칸값[찾음], TIPO_VALOR); else if (!ERRO) 칸값[찾음] = VALOR; return; }
        int obxecto_Material_de_referencia = 빼기(2);
        if (!객체유효(obxecto_Material_de_referencia)) return;
        if (힙[obxecto_Material_de_referencia] < 32 || !종포함(힙[obxecto_Material_de_referencia] - 32, propietario_VALOR)) { erro_VALOR("field receiver type mismatch"); return; }
        int 보관칸 = obxecto_Material_de_referencia + 2 + 칸위치[찾음];
        if (Orde == 180) 넣기(힙[보관칸], TIPO_VALOR);
        else if (!ERRO) { 힙[보관칸] = VALOR; 힙참조[보관칸] = TIPO_VALOR == 2 ? 1 : 0; }
    }
    static boolean 종포함(int Clase_Definición, int Nome) {
        for (int 중첩깊이 = 0; Clase_Definición >= 0 && 중첩깊이 < 16; 중첩깊이++, Clase_Definición = 부모종(Clase_Definición)) {
            if (같은말(Clase_Definición_nome[Clase_Definición], Nome) || (종부모[Clase_Definición] != 0 && 같은말(종부모[Clase_Definición], Nome))) return true;
            for (int interna_cargo = 0; interna_cargo < Clase_interface_CONTAR[Clase_Definición]; interna_cargo++) if (같은말(Clase_interface[Clase_Definición * 16 + interna_cargo], Nome)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int byte_datos, boolean CAMIÑO) {
        if (첫값 == byte_datos) return true;
        if (첫값 <= 0 || byte_datos <= 0 || 힙[첫값] != 1 || 힙[byte_datos] != 1 || 힙[첫값 + 1] != 힙[byte_datos + 1]) return false;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 힙[첫값 + 1]; Loop_ÍNDICE++) {
            int X_coordenada = 힙[첫값 + 2 + Loop_ÍNDICE], Y_coordenada = 힙[byte_datos + 2 + Loop_ÍNDICE];
            if (CAMIÑO) { if (X_coordenada == '.') X_coordenada = '/'; if (Y_coordenada == '.') Y_coordenada = '/'; }
            if (X_coordenada != Y_coordenada) return false;
        }
        return true;
    }
    static boolean 객체유효(int obxecto_Material_de_referencia) {
        if (obxecto_Material_de_referencia == 0) { erro_VALOR("NullPointerException"); return false; }
        if (obxecto_Material_de_referencia < 1 || obxecto_Material_de_referencia >= 힙끝 || 힙폭[obxecto_Material_de_referencia] < 2 || 힙[obxecto_Material_de_referencia] == 0) { erro_VALOR("invalid object reference"); return false; }
        return true;
    }
    static void protexer_VALOR(int obxecto_Material_de_referencia) {
        if (obxecto_Material_de_referencia > 0 && obxecto_Material_de_referencia < 힙끝 && 힙폭[obxecto_Material_de_referencia] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = obxecto_Material_de_referencia;
    }
    static void mostrar_VALOR(int obxecto_Material_de_referencia) {
        if (obxecto_Material_de_referencia > 0 && obxecto_Material_de_referencia < 힙끝 && 힙폭[obxecto_Material_de_referencia] >= 2 && 힙[obxecto_Material_de_referencia] != 0 && 힙표시[obxecto_Material_de_referencia] == 0) {
            힙표시[obxecto_Material_de_referencia] = 1; 표시대기[mostrar_CONTAR++] = obxecto_Material_de_referencia;
        }
    }
    static void 수거() {
        mostrar_CONTAR = 0; Colección_CONTAR++;
        for (int cheque_cargo = 1; cheque_cargo < 힙끝; cheque_cargo += 힙폭[cheque_cargo]) 힙표시[cheque_cargo] = 0;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < cadea_Material_de_referencia.length; Loop_ÍNDICE++) mostrar_VALOR(cadea_Material_de_referencia[Loop_ÍNDICE]);
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 칸수; Loop_ÍNDICE++) if ((칸권한[Loop_ÍNDICE] & 8) != 0 && 형종류(칸형[Loop_ÍNDICE]) == 2) mostrar_VALOR(칸값[Loop_ÍNDICE]);
        for (int 임시값 = 0; 임시값 < tema_CONTAR; 임시값++) {
            mostrar_VALOR(tema_obxecto[임시값]); mostrar_VALOR(tema_obxectivo[임시값]);
            int 꼭대기자리 = 임시값 == ao_corrente_tema ? marco_ÍNDICE : tema_marco[임시값];
            for (int Ficheiro_ÍNDICE = 임시값 * 32; Ficheiro_ÍNDICE <= 꼭대기자리; Ficheiro_ÍNDICE++) {
                for (int interna_cargo = 0; interna_cargo < 함수지역[틀함수[Ficheiro_ÍNDICE]]; interna_cargo++) if (local_TIPO[Ficheiro_ÍNDICE * 128 + interna_cargo] == 2) mostrar_VALOR(local_VALOR[Ficheiro_ÍNDICE * 128 + interna_cargo]);
                for (int interna_cargo = 0; interna_cargo < marco_Montón[Ficheiro_ÍNDICE]; interna_cargo++) if (스택형[Ficheiro_ÍNDICE * 128 + interna_cargo] == 2) mostrar_VALOR(스택값[Ficheiro_ÍNDICE * 128 + interna_cargo]);
            }
        }
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 화면참조.length; Loop_ÍNDICE++) mostrar_VALOR(화면참조[Loop_ÍNDICE]);
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 나중수; Loop_ÍNDICE++) mostrar_VALOR(나중실행[Loop_ÍNDICE]);
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Store_número_enteiro.length; Loop_ÍNDICE++) mostrar_VALOR(Store_número_enteiro[Loop_ÍNDICE]);
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Clase_Definición_CONTAR; Loop_ÍNDICE++) mostrar_VALOR(Clase_bloquear[Loop_ÍNDICE]);
        for (int cheque_cargo = 1; cheque_cargo < 힙끝; cheque_cargo += 힙폭[cheque_cargo]) if (잠금깊이[cheque_cargo] > 0) mostrar_VALOR(cheque_cargo);
        mostrar_VALOR(던진객체);
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 잠시수; Loop_ÍNDICE++) mostrar_VALOR(잠시참조[Loop_ÍNDICE]);
        while (mostrar_CONTAR > 0) {
            int obxecto_Material_de_referencia = 표시대기[--mostrar_CONTAR], Categoría_CÓDIGO = 힙[obxecto_Material_de_referencia];
            for (int Loop_ÍNDICE = obxecto_Material_de_referencia + 2; Loop_ÍNDICE < obxecto_Material_de_referencia + 힙폭[obxecto_Material_de_referencia]; Loop_ÍNDICE++) if (Categoría_CÓDIGO == 3 || Categoría_CÓDIGO == 4 || 힙참조[Loop_ÍNDICE] != 0) mostrar_VALOR(힙[Loop_ÍNDICE]);
        }
        for (int cheque_cargo = 1; cheque_cargo < 힙끝; cheque_cargo += 힙폭[cheque_cargo]) if (힙표시[cheque_cargo] == 0) 힙[cheque_cargo] = 0;
        for (int cheque_cargo = 1; cheque_cargo < 힙끝; cheque_cargo += 힙폭[cheque_cargo]) if (힙[cheque_cargo] == 0) {
            while (cheque_cargo + 힙폭[cheque_cargo] < 힙끝 && 힙[cheque_cargo + 힙폭[cheque_cargo]] == 0) { int Seguinte_cargo = cheque_cargo + 힙폭[cheque_cargo]; 힙폭[cheque_cargo] += 힙폭[Seguinte_cargo]; 힙폭[Seguinte_cargo] = 0; }
            if (cheque_cargo + 힙폭[cheque_cargo] == 힙끝) { 힙끝 = cheque_cargo; break; }
        }
    }
    static int 새기억(int 종류, int duración_VALOR) {
        if (duración_VALOR < 0) { erro_VALOR("NegativeArraySizeException"); return 0; }
        if (duración_VALOR > 힙.length - 3) { erro_VALOR("object heap exhausted"); return 0; }
        int 필요수 = duración_VALOR + 2, obxecto_Material_de_referencia = 0;
        if (필요수 <= 힙.length - 힙끝) { obxecto_Material_de_referencia = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { obxecto_Material_de_referencia = 읽는자리; break; }
            if (obxecto_Material_de_referencia != 0) {
                int 남은길이 = 힙폭[obxecto_Material_de_referencia] - 필요수;
                if (남은길이 >= 2) { 힙폭[obxecto_Material_de_referencia + 필요수] = 남은길이; 힙[obxecto_Material_de_referencia + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { obxecto_Material_de_referencia = 힙끝; 힙끝 += 필요수; }
        }
        if (obxecto_Material_de_referencia == 0) { erro_VALOR("object heap exhausted"); return 0; }
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 필요수; Loop_ÍNDICE++) { 힙[obxecto_Material_de_referencia + Loop_ÍNDICE] = 0; 힙참조[obxecto_Material_de_referencia + Loop_ÍNDICE] = 0; 힙폭[obxecto_Material_de_referencia + Loop_ÍNDICE] = 0; }
        MATRIZ_elemento[obxecto_Material_de_referencia] = 0;
        힙폭[obxecto_Material_de_referencia] = 필요수; 힙[obxecto_Material_de_referencia] = 종류; 힙[obxecto_Material_de_referencia + 1] = duración_VALOR; protexer_VALOR(obxecto_Material_de_referencia); return obxecto_Material_de_referencia;
    }
    static int excepción_Clase(String nome_constante) {
        if (자바도구.같음(nome_constante, "java/lang/Throwable")) return 1;
        if (자바도구.같음(nome_constante, "java/lang/Exception")) return 2;
        if (자바도구.같음(nome_constante, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(nome_constante, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(nome_constante, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(nome_constante, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(nome_constante, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(nome_constante, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(nome_constante, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(nome_constante, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(nome_constante, "java/io/IOException")) return 11;
        if (자바도구.같음(nome_constante, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(nome_constante, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(nome_constante, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(nome_constante, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int excepción_constante(int Nome) {
        for (int Loop_ÍNDICE = 1; Loop_ÍNDICE <= 41; Loop_ÍNDICE++) if (Word_SMS(Nome, excepción_nome(Loop_ÍNDICE))) return Loop_ÍNDICE;
        return 0;
    }
    static String excepción_nome(int conta_VALOR) {
        if (conta_VALOR == 40) return "java/lang/InterruptedException";
        if (conta_VALOR == 41) return "Galego/자체/대기중단예외";
        if (conta_VALOR == 39) return "java/net/SocketException";
        if (conta_VALOR == 20) return "Galego/자체/excepción";
        if (conta_VALOR == 21) return "Galego/자체/실행예외";
        if (conta_VALOR == 22) return "Galego/자체/E_S_excepción";
        if (conta_VALOR == 23) return "Galego/자체/agarda_TIMEOUT_excepción";
        if (conta_VALOR == 24) return "Galego/자체/ENDEREZO_Busca_excepción";
        if (conta_VALOR == 25) return "Galego/자체/파일없음예외";
        if (conta_VALOR == 26) return "Galego/자체/통신예외";
        if (conta_VALOR == 27) return "Galego/자체/non_válido_argumento_excepción";
        if (conta_VALOR == 28) return "Galego/자체/숫자형식예외";
        if (conta_VALOR == 29) return "Galego/자체/범위예외";
        if (conta_VALOR == 30) return "Galego/자체/배열범위예외";
        if (conta_VALOR == 31) return "Galego/자체/문자열범위예외";
        if (conta_VALOR == 32) return "Galego/자체/NULO_Material_de_referencia_excepción";
        if (conta_VALOR == 33) return "Galego/자체/산술예외";
        if (conta_VALOR == 34) return "Galego/자체/Estado_excepción";
        if (conta_VALOR == 35) return "Galego/자체/TIPO_conversión_excepción";
        if (conta_VALOR == 36) return "Galego/자체/음수배열크기예외";
        if (conta_VALOR == 37) return "Galego/자체/MATRIZ_Store_erro";
        if (conta_VALOR == 38) return "Galego/자체/tema_Estado_excepción";
        if (conta_VALOR == 1) return "java/lang/Throwable"; if (conta_VALOR == 2) return "java/lang/Exception";
        if (conta_VALOR == 3) return "java/lang/RuntimeException"; if (conta_VALOR == 4) return "java/lang/ArithmeticException";
        if (conta_VALOR == 5) return "java/lang/NullPointerException"; if (conta_VALOR == 6) return "java/lang/IndexOutOfBoundsException";
        if (conta_VALOR == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (conta_VALOR == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (conta_VALOR == 9) return "java/lang/IllegalArgumentException"; if (conta_VALOR == 10) return "java/lang/NumberFormatException";
        if (conta_VALOR == 11) return "java/io/IOException"; if (conta_VALOR == 12) return "java/io/FileNotFoundException";
        if (conta_VALOR == 17) return "java/lang/ArrayStoreException";
        if (conta_VALOR == 18) return "java/net/UnknownHostException";
        if (conta_VALOR == 19) return "java/net/SocketTimeoutException";
        if (conta_VALOR == 16) return "java/lang/IllegalThreadStateException";
        if (conta_VALOR == 13) return "java/lang/IllegalStateException"; if (conta_VALOR == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int conta_VALOR) {
        if (conta_VALOR == 40) return 2;
        if (conta_VALOR == 41) return 40;
        if (conta_VALOR == 39) return 11;
        if (conta_VALOR == 1) return 0;
        if (conta_VALOR == 2) return 1;
        if (conta_VALOR == 3) return 2;
        if (conta_VALOR == 4) return 3;
        if (conta_VALOR == 5) return 3;
        if (conta_VALOR == 6) return 3;
        if (conta_VALOR == 7) return 6;
        if (conta_VALOR == 8) return 6;
        if (conta_VALOR == 9) return 3;
        if (conta_VALOR == 10) return 9;
        if (conta_VALOR == 11) return 2;
        if (conta_VALOR == 12) return 11;
        if (conta_VALOR == 13) return 3;
        if (conta_VALOR == 14) return 3;
        if (conta_VALOR == 15) return 3;
        if (conta_VALOR == 16) return 9;
        if (conta_VALOR == 17) return 3;
        if (conta_VALOR == 18) return 11;
        if (conta_VALOR == 19) return 11;
        if (conta_VALOR == 20) return 2;
        if (conta_VALOR == 21) return 3;
        if (conta_VALOR == 22) return 11;
        if (conta_VALOR == 23) return 22;
        if (conta_VALOR == 24) return 22;
        if (conta_VALOR == 25) return 22;
        if (conta_VALOR == 26) return 22;
        if (conta_VALOR == 27) return 9;
        if (conta_VALOR == 28) return 27;
        if (conta_VALOR == 29) return 6;
        if (conta_VALOR == 30) return 29;
        if (conta_VALOR == 31) return 29;
        if (conta_VALOR == 32) return 5;
        if (conta_VALOR == 33) return 4;
        if (conta_VALOR == 34) return 13;
        if (conta_VALOR == 35) return 14;
        if (conta_VALOR == 36) return 15;
        if (conta_VALOR == 37) return 17;
        if (conta_VALOR == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int real_VALOR, int 요구값) {
        for (int 깊이 = 0; real_VALOR != 0 && 깊이 < 16; 깊이++, real_VALOR = 예외부모(real_VALOR))
            if (real_VALOR == 요구값) return true;
        return false;
    }
    static void 예외던짐(int conta_VALOR, String Léame_Material_de_referencia) {
        int obxecto_Material_de_referencia = 새기억(9, 2); if (ERRO) return;
        힙[obxecto_Material_de_referencia + 2] = conta_VALOR; 힙[obxecto_Material_de_referencia + 3] = hospedar_carácter(Léame_Material_de_referencia); 힙참조[obxecto_Material_de_referencia + 3] = 1;
        던진객체 = obxecto_Material_de_referencia; ERRO = true;
    }
    static boolean 맞는객체(int obxecto_Material_de_referencia, int Nome) {
        if (obxecto_Material_de_referencia == 0) return true;
        if (!객체유효(obxecto_Material_de_referencia)) return false;
        int Categoría_CÓDIGO = 힙[obxecto_Material_de_referencia];
        if (Word_SMS(Nome, "java/lang/Object")) return true;
        if (Categoría_CÓDIGO >= 32) return 종포함(Categoría_CÓDIGO - 32, Nome);
        if (Categoría_CÓDIGO == 9) { int obxectivo_ENDEREZO = excepción_constante(Nome); return obxectivo_ENDEREZO != 0 && 예외포함(힙[obxecto_Material_de_referencia + 2], obxectivo_ENDEREZO); }
        if (Categoría_CÓDIGO == 1) return Word_SMS(Nome, "java/lang/String") || Word_SMS(Nome, "java/lang/CharSequence");
        if (Categoría_CÓDIGO == 4) return Word_SMS(Nome, "java/lang/StringBuilder") || Word_SMS(Nome, "java/lang/CharSequence");
        if (Categoría_CÓDIGO == 10) return Word_SMS(Nome, "java/util/ArrayList") || Word_SMS(Nome, "java/util/List");
        if (Categoría_CÓDIGO == 11) return Word_SMS(Nome, "java/util/HashMap") || Word_SMS(Nome, "java/util/Map");
        if (Categoría_CÓDIGO == 12) return Word_SMS(Nome, "java/lang/Integer") || Word_SMS(Nome, "java/lang/Number");
        if (Categoría_CÓDIGO >= 24 && Categoría_CÓDIGO <= 28 && 힙[obxecto_Material_de_referencia + 13] != 0) return 한국어화면종(Nome) == Categoría_CÓDIGO || Word_SMS(Nome, "Galego/자체/화면구성요소");
        if (Categoría_CÓDIGO >= 24 && Categoría_CÓDIGO <= 28) return (한국어화면종(Nome) == 0 && 화면종(Nome) == Categoría_CÓDIGO) || Word_SMS(Nome, "java/awt/Component") || Word_SMS(Nome, "java/awt/Container") || Word_SMS(Nome, "javax/swing/JComponent");
        if (Categoría_CÓDIGO == 29) return Word_SMS(Nome, 힙[obxecto_Material_de_referencia + 3] != 0 ? "Galego/자체/동작알림" : "java/awt/event/ActionEvent");
        if (Categoría_CÓDIGO == 30) return Word_SMS(Nome, "java/awt/FlowLayout") || Word_SMS(Nome, "java/awt/LayoutManager");
        if (Categoría_CÓDIGO == 17) return Word_SMS(Nome, "java/net/Socket");
        if (Categoría_CÓDIGO == 18) return Word_SMS(Nome, "java/net/ServerSocket");
        if (Categoría_CÓDIGO == 19) return Word_SMS(Nome, 힙[obxecto_Material_de_referencia + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (Categoría_CÓDIGO == 14) return Word_SMS(Nome, "java/net/InetAddress");
        if (Categoría_CÓDIGO == 15) return Word_SMS(Nome, "java/net/DatagramSocket");
        if (Categoría_CÓDIGO == 16) return Word_SMS(Nome, "java/net/DatagramPacket");
        if (Categoría_CÓDIGO == 13) return Word_SMS(Nome, 힙[obxecto_Material_de_referencia + 3] != 0 ? "Galego/자체/작업가닥" : "java/lang/Thread");
        if (Categoría_CÓDIGO == 2) return Word_SMS(Nome, "[I"); if (Categoría_CÓDIGO == 20) return Word_SMS(Nome, "[B"); if (Categoría_CÓDIGO == 21) return Word_SMS(Nome, "[Z");
        if (Categoría_CÓDIGO == 22) return Word_SMS(Nome, "[C"); if (Categoría_CÓDIGO == 23) return Word_SMS(Nome, "[S");
        if (Categoría_CÓDIGO != 3) return false;
        if (Word_SMS(Nome, "[Ljava/lang/Object;")) return true;
        int compoñente = MATRIZ_elemento[obxecto_Material_de_referencia];
        if (compoñente == -1) return Word_SMS(Nome, "[Ljava/lang/String;") || Word_SMS(Nome, "[Ljava/lang/CharSequence;");
        if (compoñente == 0) return false;
        if (배열종비교(compoñente, Nome)) return true;
        if ((Word_SMS(compoñente, "java/lang/String") || Word_SMS(compoñente, "java/lang/StringBuilder")) && Word_SMS(Nome, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Clase_Definición_CONTAR; Loop_ÍNDICE++) if (같은말(Clase_Definición_nome[Loop_ÍNDICE], compoñente)) {
            for (int código_de_carácter = Loop_ÍNDICE, 중첩깊이 = 0; código_de_carácter >= 0 && 중첩깊이 < 16; 중첩깊이++, código_de_carácter = 부모종(código_de_carácter)) {
                if (배열종비교(종부모[código_de_carácter], Nome)) return true;
                for (int interna_cargo = 0; interna_cargo < Clase_interface_CONTAR[código_de_carácter]; interna_cargo++) if (배열종비교(Clase_interface[código_de_carácter * 16 + interna_cargo], Nome)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int nome_constante, int 형식참조) {
        int cheque_cargo = 상가[형식참조], introdución_CONTAR = constante_SEGUNDO_VALOR[형식참조];
        if (nome_constante == 0 || introdución_CONTAR < 4 || Ficheiro[cheque_cargo] != '[' || Ficheiro[cheque_cargo + 1] != 'L' || Ficheiro[cheque_cargo + introdución_CONTAR - 1] != ';' || constante_SEGUNDO_VALOR[nome_constante] != introdución_CONTAR - 3) return false;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < introdución_CONTAR - 3; Loop_ÍNDICE++) if (Ficheiro[상가[nome_constante] + Loop_ÍNDICE] != Ficheiro[cheque_cargo + 2 + Loop_ÍNDICE]) return false;
        return true;
    }
    static void agarradoira_excepción() {
        if (던진객체 == 0) return;
        ERRO = false;
        while (marco_ÍNDICE >= ao_corrente_tema * 32) {
            int Ficheiro_ÍNDICE = 틀함수[marco_ÍNDICE], 읽는자리 = marco_instrución[marco_ÍNDICE];
            for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 잡기수; Loop_ÍNDICE++) if (잡기함수[Loop_ÍNDICE] == Ficheiro_ÍNDICE && 읽는자리 >= 잡기시작[Loop_ÍNDICE] && 읽는자리 < 잡기끝[Loop_ÍNDICE]
                && (잡기종[Loop_ÍNDICE] == 0 || 맞는객체(던진객체, 잡기종[Loop_ÍNDICE]))) {
                marco_cargo[marco_ÍNDICE] = 잡기위치[Loop_ÍNDICE]; marco_Montón[marco_ÍNDICE] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (iniciar_marco[marco_ÍNDICE] != 0) Clase_Definición_Estado[iniciar_marco[marco_ÍNDICE] - 1] = 3;
            if (marco_bloquear[marco_ÍNDICE] != 0) { liberar_bloquear(marco_bloquear[marco_ÍNDICE]); marco_bloquear[marco_ÍNDICE] = 0; }
            marco_ÍNDICE--;
        }
        usuario.Escritura("Uncaught ");
        if (힙[던진객체] == 9) { usuario.Escritura(excepción_nome(힙[던진객체 + 2])); usuario.Escritura(": "); escribir_SMS(힙[던진객체 + 3]); }
        else usuario.Escritura("user exception");
        usuario.escribir_carácter_VALOR(10); 던진객체 = 0; ERRO = true;
    }
    // 이 JVM의 스택 항목은 ao_corrente_elemento category-1(int/reference)만 허용한다.
    static void Montón_instrución(int comando_CÓDIGO) {
        int 첫값 = 빼기(0), 첫형식 = devolver_TIPO;
        if (comando_CÓDIGO == 87) return;
        if (comando_CÓDIGO == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int byte_datos = 빼기(0), SEGUNDO_formato = devolver_TIPO;
        if (comando_CÓDIGO == 88) return;
        if (comando_CÓDIGO == 90) { 넣기(첫값, 첫형식); 넣기(byte_datos, SEGUNDO_formato); 넣기(첫값, 첫형식); return; }
        if (comando_CÓDIGO == 92) { 넣기(byte_datos, SEGUNDO_formato); 넣기(첫값, 첫형식); 넣기(byte_datos, SEGUNDO_formato); 넣기(첫값, 첫형식); return; }
        if (comando_CÓDIGO == 95) { 넣기(첫값, 첫형식); 넣기(byte_datos, SEGUNDO_formato); return; }
        int código_de_carácter = 빼기(0), 셋째형식 = devolver_TIPO;
        if (comando_CÓDIGO == 91) { 넣기(첫값, 첫형식); 넣기(código_de_carácter, 셋째형식); 넣기(byte_datos, SEGUNDO_formato); 넣기(첫값, 첫형식); return; }
        if (comando_CÓDIGO == 93) { 넣기(byte_datos, SEGUNDO_formato); 넣기(첫값, 첫형식); 넣기(código_de_carácter, 셋째형식); 넣기(byte_datos, SEGUNDO_formato); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = devolver_TIPO;
        넣기(byte_datos, SEGUNDO_formato); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(código_de_carácter, 셋째형식); 넣기(byte_datos, SEGUNDO_formato); 넣기(첫값, 첫형식);
    }
    static void 새객체(int nome_constante, int 시작점) {
        int Categoría_CÓDIGO = 0, 유효길이 = 0, excepción_Material_de_referencia = excepción_constante(nome_constante);
        if (Word_SMS(nome_constante, "java/lang/StringBuilder")) { Categoría_CÓDIGO = 4; 유효길이 = 1; }
        if (Word_SMS(nome_constante, "java/io/FileInputStream")) { Categoría_CÓDIGO = 5; 유효길이 = 2; }
        if (Word_SMS(nome_constante, "java/io/FileOutputStream")) { Categoría_CÓDIGO = 6; 유효길이 = 2; }
        if (excepción_Material_de_referencia != 0) { Categoría_CÓDIGO = 9; 유효길이 = 2; }
        if (Word_SMS(nome_constante, "java/util/ArrayList")) { Categoría_CÓDIGO = 10; 유효길이 = 2; }
        if (Word_SMS(nome_constante, "java/util/HashMap")) { Categoría_CÓDIGO = 11; 유효길이 = 2; }
        if (Word_SMS(nome_constante, "java/lang/Integer")) { Categoría_CÓDIGO = 12; 유효길이 = 1; }
        if (Word_SMS(nome_constante, "java/net/Socket")) { Categoría_CÓDIGO = 17; 유효길이 = 5; }
        if (Word_SMS(nome_constante, "java/net/ServerSocket")) { Categoría_CÓDIGO = 18; 유효길이 = 5; }
        if (Word_SMS(nome_constante, "java/net/DatagramSocket")) { Categoría_CÓDIGO = 15; 유효길이 = 3; }
        if (Word_SMS(nome_constante, "java/net/DatagramPacket")) { Categoría_CÓDIGO = 16; 유효길이 = 4; }
        if (Word_SMS(nome_constante, "java/lang/Thread") || Word_SMS(nome_constante, "Galego/자체/작업가닥")) { Categoría_CÓDIGO = 13; 유효길이 = 2; }
        if (Word_SMS(nome_constante, "java/lang/Object")) { Categoría_CÓDIGO = 8; }
        if (Categoría_CÓDIGO == 0 && 화면종(nome_constante) != 0) { Categoría_CÓDIGO = 화면종(nome_constante); 유효길이 = 12; }
        if (Categoría_CÓDIGO == 0) {
            int código_de_carácter = Busca_Clase_Definición(nome_constante); if (código_de_carácter < 0 || ERRO || !iniciar(código_de_carácter, 시작점)) return;
            Categoría_CÓDIGO = 32 + código_de_carácter; 유효길이 = 종칸수[código_de_carácter];
        }
        int obxecto_Material_de_referencia = atribuír_Almacenamento(Categoría_CÓDIGO, 유효길이); if (ERRO) return;
        if (Categoría_CÓDIGO == 13 && Word_SMS(nome_constante, "Galego/자체/작업가닥")) 힙[obxecto_Material_de_referencia + 3] = 1;
        if (Categoría_CÓDIGO >= 24 && Categoría_CÓDIGO <= 28 && 한국어화면종(nome_constante) != 0) 힙[obxecto_Material_de_referencia + 13] = 1;
        if (Categoría_CÓDIGO == 5 || Categoría_CÓDIGO == 6 || Categoría_CÓDIGO == 15 || Categoría_CÓDIGO == 17 || Categoría_CÓDIGO == 18) 힙[obxecto_Material_de_referencia + 2] = -1;
        if (Categoría_CÓDIGO == 9) 힙[obxecto_Material_de_referencia + 2] = excepción_Material_de_referencia;
        넣기(obxecto_Material_de_referencia, 2);
    }
    static boolean 값같음(int 첫값, int byte_datos) {
        if (첫값 == byte_datos) return true;
        if (첫값 == 0 || byte_datos == 0 || 첫값 < 0 || byte_datos < 0 || 첫값 >= 힙끝 || byte_datos >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[byte_datos] == 1) return 글같음(첫값, byte_datos, false);
        return 힙[첫값] == 12 && 힙[byte_datos] == 12 && 힙[첫값 + 2] == 힙[byte_datos + 2];
    }
    static int 글조각(int obxecto_Material_de_referencia, int START_cargo, int finalizar_cargo) {
        if (!obxecto_VALOR(obxecto_Material_de_referencia, 1)) return 0;
        if (START_cargo < 0 || finalizar_cargo < START_cargo || finalizar_cargo > 힙[obxecto_Material_de_referencia + 1]) { erro_VALOR("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = atribuír_Almacenamento(1, finalizar_cargo - START_cargo); if (ERRO) return 0;
        for (int Loop_ÍNDICE = START_cargo; Loop_ÍNDICE < finalizar_cargo; Loop_ÍNDICE++) 힙[반환값 + 2 + Loop_ÍNDICE - START_cargo] = 힙[obxecto_Material_de_referencia + 2 + Loop_ÍNDICE];
        return 반환값;
    }
    static int unirse_SMS(int 첫값, int byte_datos) {
        if (!obxecto_VALOR(첫값, 1) || !obxecto_VALOR(byte_datos, 1)) return 0;
        int introdución_CONTAR = 힙[첫값 + 1], 함수번호 = 힙[byte_datos + 1], 반환값 = atribuír_Almacenamento(1, introdución_CONTAR + 함수번호); if (ERRO) return 0;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < introdución_CONTAR; Loop_ÍNDICE++) 힙[반환값 + 2 + Loop_ÍNDICE] = 힙[첫값 + 2 + Loop_ÍNDICE];
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 함수번호; Loop_ÍNDICE++) 힙[반환값 + 2 + introdución_CONTAR + Loop_ÍNDICE] = 힙[byte_datos + 2 + Loop_ÍNDICE];
        return 반환값;
    }
    static boolean 기본호출(int propietario, int nome_constante, int 서술상수, int comando_CÓDIGO) {
        if (Word_SMS(propietario, "Galego/자체/실행인수") && comando_CÓDIGO == 184) {
            if (Word_SMS(nome_constante, "elemento_CONTAR") && Word_SMS(서술상수, "()I")) { 넣기(usuario.인수개수() - 1, 1); return true; }
            if (Word_SMS(nome_constante, "Texto") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= usuario.인수개수() - 1) 예외던짐(29, "executar_comando Argumentos 범위를 벗어났습니다");
                else 넣기(hospedar_carácter(usuario.Argumentos(순번 + 1)), 2);
                return true;
            }
            erro_VALOR("지원하지 않는 Galego executar_comando Argumentos 호출"); return true;
        }
        if (Word_SMS(propietario, "Galego/자체/작업가닥")) { Proceso_tema(nome_constante, 서술상수, comando_CÓDIGO, true); return true; }
        if (한국어화면소유(propietario)) { 한국어화면호출(propietario, nome_constante, 서술상수, comando_CÓDIGO); return true; }
        if (화면소유(propietario)) { 화면호출(propietario, nome_constante, 서술상수, comando_CÓDIGO); return true; }
        if (Word_SMS(propietario, "java/net/Socket") || Word_SMS(propietario, "java/net/ServerSocket") || Word_SMS(propietario, "java/io/InputStream") || Word_SMS(propietario, "java/io/OutputStream")) { 흐름호출(propietario, nome_constante, 서술상수, comando_CÓDIGO); return true; }
        if (Word_SMS(propietario, "Galego/자체/kernel_VALOR") && comando_CÓDIGO == 184) {
            if (Word_SMS(nome_constante, "화면너비") && Word_SMS(서술상수, "()I")) { 넣기(usuario.화면너비(), 1); return true; }
            if (Word_SMS(nome_constante, "화면높이") && Word_SMS(서술상수, "()I")) { 넣기(usuario.화면높이(), 1); return true; }
            if (Word_SMS(nome_constante, "밀리초") && Word_SMS(서술상수, "()I")) { 넣기(usuario.밀리초(), 1); return true; }
            if (Word_SMS(nome_constante, "그림대기") && Word_SMS(서술상수, "()I")) { 넣기(usuario.그림대기(), 1); return true; }
            if (Word_SMS(nome_constante, "사각형") && Word_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), Y_coordenada = 빼기(1), X_coordenada = 빼기(1); 넣기(usuario.사각형(X_coordenada, Y_coordenada, 너비, 높이, 색상), 1); return true; }
        }
        if (Word_SMS(propietario, "java/net/InetAddress") || Word_SMS(propietario, "java/net/DatagramPacket") || Word_SMS(propietario, "java/net/DatagramSocket")) { 통신호출(propietario, nome_constante, 서술상수, comando_CÓDIGO); return true; }
        if (Word_SMS(propietario, "java/lang/Thread")) { 가닥호출(nome_constante, 서술상수, comando_CÓDIGO); return true; }
        if (Word_SMS(propietario, "java/lang/Object")) {
            if (Word_SMS(nome_constante, "<init>") && Word_SMS(서술상수, "()V") && comando_CÓDIGO == 183) { 객체유효(빼기(2)); return true; }
            if (Word_SMS(nome_constante, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int byte_datos = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == byte_datos ? 1 : 0, 1); return true; }
        }
        if (excepción_constante(propietario) != 0) {
            if (Word_SMS(nome_constante, "<init>") && comando_CÓDIGO == 183 && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int avisar = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), obxecto_Material_de_referencia = 빼기(2);
                if (obxecto_VALOR(obxecto_Material_de_referencia, 9)) { 힙[obxecto_Material_de_referencia + 3] = avisar; 힙참조[obxecto_Material_de_referencia + 3] = 1; } return true;
            }
            if ((Word_SMS(nome_constante, "getMessage") || Word_SMS(nome_constante, "설명")) && Word_SMS(서술상수, "()Ljava/lang/String;")) { int obxecto_Material_de_referencia = 빼기(2); if (obxecto_VALOR(obxecto_Material_de_referencia, 9)) 넣기(힙[obxecto_Material_de_referencia + 3], 2); return true; }
        }
        if (Word_SMS(propietario, "java/lang/String")) {
            if (comando_CÓDIGO == 182 && Word_SMS(nome_constante, "getBytes") && (Word_SMS(서술상수, "()[B") || Word_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int codificación_nome = Word_SMS(서술상수, "()[B") ? 0 : 빼기(2), obxecto_Material_de_referencia = 빼기(2);
                if (!obxecto_VALOR(obxecto_Material_de_referencia, 1)) return true;
                if (codificación_nome != 0 && !글같음(codificación_nome, hospedar_carácter("UTF-8"), false) && !글같음(codificación_nome, hospedar_carácter("UTF8"), false) && !글같음(codificación_nome, hospedar_carácter("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int introdución_CONTAR = 힙[obxecto_Material_de_referencia + 1], 반환값 = atribuír_Almacenamento(20, introdución_CONTAR * 3), 사용수 = 0; if (ERRO) return true;
                for (int interna_cargo = 0; interna_cargo < introdución_CONTAR; interna_cargo++) {
                    int código_de_carácter = 힙[obxecto_Material_de_referencia + 2 + interna_cargo];
                    if (código_de_carácter >= 0xd800 && código_de_carácter <= 0xdbff && interna_cargo + 1 < introdución_CONTAR && 힙[obxecto_Material_de_referencia + 3 + interna_cargo] >= 0xdc00 && 힙[obxecto_Material_de_referencia + 3 + interna_cargo] <= 0xdfff) código_de_carácter = 0x10000 + ((código_de_carácter - 0xd800) << 10) + 힙[obxecto_Material_de_referencia + 2 + ++interna_cargo] - 0xdc00;
                    else if (código_de_carácter >= 0xd800 && código_de_carácter <= 0xdfff) código_de_carácter = '?';
                    if (código_de_carácter < 128) 힙[반환값 + 2 + 사용수++] = código_de_carácter;
                    else { int byte_CONTAR = código_de_carácter < 2048 ? 2 : código_de_carácter < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((byte_CONTAR == 2 ? 192 : byte_CONTAR == 3 ? 224 : 240) | código_de_carácter >> (6 * (byte_CONTAR - 1))); for (int Comparación_cargo = byte_CONTAR - 1; Comparación_cargo > 0; Comparación_cargo--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | código_de_carácter >> (6 * (Comparación_cargo - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (comando_CÓDIGO == 184 && Word_SMS(nome_constante, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(díxito_carácter(빼기(1)), 2); return true; }
            if (comando_CÓDIGO != 182) return false;
            if (Word_SMS(nome_constante, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int byte_datos = 빼기(2), 첫값 = 빼기(2); if (obxecto_VALOR(첫값, 1)) 넣기(글같음(첫값, byte_datos, false) ? 1 : 0, 1); return true; }
            if (Word_SMS(nome_constante, "isEmpty") && Word_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (obxecto_VALOR(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_SMS(nome_constante, "substring") && (Word_SMS(서술상수, "(I)Ljava/lang/String;") || Word_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SEGUNDO_VALOR = Word_SMS(서술상수, "(II)Ljava/lang/String;"); int finalizar_cargo = SEGUNDO_VALOR ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (obxecto_VALOR(첫값, 1)) 넣기(글조각(첫값, 시작점, SEGUNDO_VALOR ? finalizar_cargo : 힙[첫값 + 1]), 2); return true;
            }
            if (Word_SMS(nome_constante, "concat") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int byte_datos = 빼기(2), 첫값 = 빼기(2); 넣기(unirse_SMS(첫값, byte_datos), 2); return true; }
            if (Word_SMS(nome_constante, "hashCode") && Word_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), hash_VALOR = 0; if (obxecto_VALOR(첫값, 1)) { for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 힙[첫값 + 1]; Loop_ÍNDICE++) hash_VALOR = hash_VALOR * 31 + 힙[첫값 + 2 + Loop_ÍNDICE]; 넣기(hash_VALOR, 1); } return true; }
            if (Word_SMS(nome_constante, "toString") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (obxecto_VALOR(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_SMS(propietario, "java/lang/Integer")) {
            if (comando_CÓDIGO == 184 && Word_SMS(nome_constante, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int datos_VALOR = 빼기(1), obxecto_Material_de_referencia = datos_VALOR >= -128 && datos_VALOR <= 127 ? Store_número_enteiro[datos_VALOR + 128] : 0; if (obxecto_Material_de_referencia == 0) { obxecto_Material_de_referencia = atribuír_Almacenamento(12, 1); if (!ERRO) { 힙[obxecto_Material_de_referencia + 2] = datos_VALOR; if (datos_VALOR >= -128 && datos_VALOR <= 127) Store_número_enteiro[datos_VALOR + 128] = obxecto_Material_de_referencia; } } 넣기(obxecto_Material_de_referencia, 2); return true; }
            if (comando_CÓDIGO == 183 && Word_SMS(nome_constante, "<init>") && Word_SMS(서술상수, "(I)V")) { int datos_VALOR = 빼기(1), obxecto_Material_de_referencia = 빼기(2); if (obxecto_VALOR(obxecto_Material_de_referencia, 12)) 힙[obxecto_Material_de_referencia + 2] = datos_VALOR; return true; }
            if (comando_CÓDIGO == 182 && Word_SMS(nome_constante, "intValue") && Word_SMS(서술상수, "()I")) { int obxecto_Material_de_referencia = 빼기(2); if (obxecto_VALOR(obxecto_Material_de_referencia, 12)) 넣기(힙[obxecto_Material_de_referencia + 2], 1); return true; }
            if (comando_CÓDIGO == 184 && Word_SMS(nome_constante, "toString") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(díxito_carácter(빼기(1)), 2); return true; }
        }
        if (Word_SMS(propietario, "java/lang/Math") && comando_CÓDIGO == 184) {
            if (Word_SMS(nome_constante, "abs") && Word_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_SMS(nome_constante, "min") || Word_SMS(nome_constante, "max")) && Word_SMS(서술상수, "(II)I")) { int byte_datos = 빼기(1), 첫값 = 빼기(1); 넣기(Word_SMS(nome_constante, "min") ? (첫값 < byte_datos ? 첫값 : byte_datos) : (첫값 > byte_datos ? 첫값 : byte_datos), 1); return true; }
        }
        if (Word_SMS(propietario, "java/lang/System") && comando_CÓDIGO == 184) {
            if (Word_SMS(nome_constante, "gc") && Word_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Word_SMS(nome_constante, "arraycopy") && Word_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int introdución_CONTAR = 빼기(1), destino_VALOR_ÍNDICE = 빼기(1), byte_datos = 빼기(2), START_cargo = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(byte_datos)) {
                    int Categoría_CÓDIGO = 힙[첫값];
                    if (힙[byte_datos] != Categoría_CÓDIGO || (Categoría_CÓDIGO != 2 && Categoría_CÓDIGO != 3 && (Categoría_CÓDIGO < 20 || Categoría_CÓDIGO > 23))) erro_VALOR("arraycopy type mismatch");
                    else if (introdución_CONTAR < 0 || START_cargo < 0 || destino_VALOR_ÍNDICE < 0 || START_cargo > 힙[첫값 + 1] - introdución_CONTAR || destino_VALOR_ÍNDICE > 힙[byte_datos + 1] - introdución_CONTAR) erro_VALOR("ArrayIndexOutOfBoundsException");
                    else if (첫값 == byte_datos && destino_VALOR_ÍNDICE > START_cargo) { for (int Loop_ÍNDICE = introdución_CONTAR - 1; Loop_ÍNDICE >= 0; Loop_ÍNDICE--) 힙[byte_datos + 2 + destino_VALOR_ÍNDICE + Loop_ÍNDICE] = 힙[첫값 + 2 + START_cargo + Loop_ÍNDICE]; }
                    else { for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < introdución_CONTAR && !ERRO; Loop_ÍNDICE++) { int datos_VALOR = 힙[첫값 + 2 + START_cargo + Loop_ÍNDICE]; if (Categoría_CÓDIGO != 3 || 배열저장가능(byte_datos, datos_VALOR)) 힙[byte_datos + 2 + destino_VALOR_ÍNDICE + Loop_ÍNDICE] = datos_VALOR; } }
                }
                return true;
            }
        }
        if (Word_SMS(propietario, "java/util/ArrayList") || Word_SMS(propietario, "java/util/List") || Word_SMS(propietario, "java/util/HashMap") || Word_SMS(propietario, "java/util/Map")) {
            모음호출(propietario, nome_constante, 서술상수, comando_CÓDIGO); return true;
        }
        return false;
    }
    static void 모음늘리기(int obxecto_Material_de_referencia, int 필요수) {
        int 이전값 = 힙[obxecto_Material_de_referencia + 2], capacidade_datos = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (capacidade_datos >= 필요수) return;
        int Seguinte_cargo = capacidade_datos < 8 ? 8 : capacidade_datos * 2; if (Seguinte_cargo < 필요수) Seguinte_cargo = 필요수;
        int datos_MATRIZ = atribuír_Almacenamento(3, Seguinte_cargo); if (ERRO) return;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < capacidade_datos; Loop_ÍNDICE++) 힙[datos_MATRIZ + 2 + Loop_ÍNDICE] = 힙[이전값 + 2 + Loop_ÍNDICE];
        힙[obxecto_Material_de_referencia + 2] = datos_MATRIZ; 힙참조[obxecto_Material_de_referencia + 2] = 1;
    }
    static void 모음호출(int propietario, int nome_constante, int 서술상수, int comando_CÓDIGO) {
        boolean 대응참조 = Word_SMS(propietario, "java/util/HashMap") || Word_SMS(propietario, "java/util/Map"); int Categoría_CÓDIGO = 대응참조 ? 11 : 10;
        if (Word_SMS(nome_constante, "<init>") && comando_CÓDIGO == 183 && Word_SMS(서술상수, "()V")) { int obxecto_Material_de_referencia = 빼기(2); if (obxecto_VALOR(obxecto_Material_de_referencia, Categoría_CÓDIGO)) 모음늘리기(obxecto_Material_de_referencia, 8); return; }
        if (comando_CÓDIGO != 182 && comando_CÓDIGO != 185) { erro_VALOR("invalid collection invocation"); return; }
        if (Word_SMS(nome_constante, "size") && Word_SMS(서술상수, "()I") || Word_SMS(nome_constante, "isEmpty") && Word_SMS(서술상수, "()Z")) {
            int obxecto_Material_de_referencia = 빼기(2); if (obxecto_VALOR(obxecto_Material_de_referencia, Categoría_CÓDIGO)) 넣기(Word_SMS(nome_constante, "size") ? 힙[obxecto_Material_de_referencia + 3] : 힙[obxecto_Material_de_referencia + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_SMS(nome_constante, "clear") && Word_SMS(서술상수, "()V")) { int obxecto_Material_de_referencia = 빼기(2); if (obxecto_VALOR(obxecto_Material_de_referencia, Categoría_CÓDIGO)) { int datos_MATRIZ = 힙[obxecto_Material_de_referencia + 2]; for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 힙[datos_MATRIZ + 1]; Loop_ÍNDICE++) 힙[datos_MATRIZ + 2 + Loop_ÍNDICE] = 0; 힙[obxecto_Material_de_referencia + 3] = 0; } return; }
        if (!대응참조 && Word_SMS(nome_constante, "add") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int datos_VALOR = 빼기(2), obxecto_Material_de_referencia = 빼기(2); if (!obxecto_VALOR(obxecto_Material_de_referencia, 10)) return;
            int introdución_CONTAR = 힙[obxecto_Material_de_referencia + 3]; 모음늘리기(obxecto_Material_de_referencia, introdución_CONTAR + 1); if (!ERRO) { 힙[힙[obxecto_Material_de_referencia + 2] + 2 + introdución_CONTAR] = datos_VALOR; 힙[obxecto_Material_de_referencia + 3] = introdución_CONTAR + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_SMS(nome_constante, "get") || Word_SMS(nome_constante, "remove")) && Word_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Word_SMS(nome_constante, "set") && Word_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = Word_SMS(nome_constante, "set"); int datos_VALOR = 지정여부 ? 빼기(2) : 0, introdución_cargo = 빼기(1), obxecto_Material_de_referencia = 빼기(2);
            if (!obxecto_VALOR(obxecto_Material_de_referencia, 10)) return;
            int introdución_CONTAR = 힙[obxecto_Material_de_referencia + 3], datos_MATRIZ = 힙[obxecto_Material_de_referencia + 2];
            if (introdución_cargo < 0 || introdución_cargo >= introdución_CONTAR) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[datos_MATRIZ + 2 + introdución_cargo];
            if (지정여부) 힙[datos_MATRIZ + 2 + introdución_cargo] = datos_VALOR;
            if (Word_SMS(nome_constante, "remove")) { for (int Loop_ÍNDICE = introdución_cargo + 1; Loop_ÍNDICE < introdución_CONTAR; Loop_ÍNDICE++) 힙[datos_MATRIZ + 1 + Loop_ÍNDICE] = 힙[datos_MATRIZ + 2 + Loop_ÍNDICE]; 힙[datos_MATRIZ + 1 + introdución_CONTAR] = 0; 힙[obxecto_Material_de_referencia + 3] = introdución_CONTAR - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Word_SMS(nome_constante, "get") || Word_SMS(nome_constante, "remove")) && Word_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(nome_constante, "put") && Word_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(nome_constante, "containsKey") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_SMS(nome_constante, "put"), eliminar = Word_SMS(nome_constante, "remove");
            int datos_VALOR = 넣기여부 ? 빼기(2) : 0, Chave_Material_de_referencia = 빼기(2), obxecto_Material_de_referencia = 빼기(2); if (!obxecto_VALOR(obxecto_Material_de_referencia, 11)) return;
            int introdución_CONTAR = 힙[obxecto_Material_de_referencia + 3], datos_MATRIZ = 힙[obxecto_Material_de_referencia + 2], 찾은여부 = -1;
            for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < introdución_CONTAR; Loop_ÍNDICE++) if (값같음(Chave_Material_de_referencia, 힙[datos_MATRIZ + 2 + 2 * Loop_ÍNDICE])) { 찾은여부 = Loop_ÍNDICE; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[datos_MATRIZ + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(obxecto_Material_de_referencia, (introdución_CONTAR + 1) * 2); datos_MATRIZ = 힙[obxecto_Material_de_referencia + 2]; 찾은여부 = introdución_CONTAR; if (!ERRO) 힙[obxecto_Material_de_referencia + 3] = introdución_CONTAR + 1; }
                if (!ERRO) { 힙[datos_MATRIZ + 2 + 2 * 찾은여부] = Chave_Material_de_referencia; 힙[datos_MATRIZ + 3 + 2 * 찾은여부] = datos_VALOR; }
            }
            if (eliminar && 찾은여부 >= 0) { for (int Loop_ÍNDICE = 찾은여부 + 1; Loop_ÍNDICE < introdución_CONTAR; Loop_ÍNDICE++) { 힙[datos_MATRIZ + 2 * Loop_ÍNDICE] = 힙[datos_MATRIZ + 2 + 2 * Loop_ÍNDICE]; 힙[datos_MATRIZ + 1 + 2 * Loop_ÍNDICE] = 힙[datos_MATRIZ + 3 + 2 * Loop_ÍNDICE]; } 힙[datos_MATRIZ + 2 * introdución_CONTAR] = 0; 힙[datos_MATRIZ + 1 + 2 * introdución_CONTAR] = 0; 힙[obxecto_Material_de_referencia + 3] = introdución_CONTAR - 1; }
            if (Word_SMS(nome_constante, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        erro_VALOR("unsupported collection method");
    }
    static boolean 잠금얻기(int obxecto_Material_de_referencia) {
        if (!객체유효(obxecto_Material_de_referencia)) return false;
        if (잠금깊이[obxecto_Material_de_referencia] != 0 && bloquear_propietario[obxecto_Material_de_referencia] != ao_corrente_tema + 1) { modificar_solicitude = true; return false; }
        bloquear_propietario[obxecto_Material_de_referencia] = ao_corrente_tema + 1; 잠금깊이[obxecto_Material_de_referencia]++; return true;
    }
    static void liberar_bloquear(int obxecto_Material_de_referencia) {
        if (!객체유효(obxecto_Material_de_referencia)) return;
        if (잠금깊이[obxecto_Material_de_referencia] == 0 || bloquear_propietario[obxecto_Material_de_referencia] != ao_corrente_tema + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[obxecto_Material_de_referencia] == 0) bloquear_propietario[obxecto_Material_de_referencia] = 0;
    }
    static boolean mudar_tema() {
        tema_marco[ao_corrente_tema] = marco_ÍNDICE;
        if (marco_ÍNDICE < ao_corrente_tema * 32) tema_Estado[ao_corrente_tema] = 3;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < tema_CONTAR; Loop_ÍNDICE++) if (tema_Estado[Loop_ÍNDICE] == 2 && tema_Estado[가닥대기[Loop_ÍNDICE]] == 3) tema_Estado[Loop_ÍNDICE] = 1;
        for (int Loop_ÍNDICE = 1; Loop_ÍNDICE <= tema_CONTAR; Loop_ÍNDICE++) {
            int Seguinte_cargo = (ao_corrente_tema + Loop_ÍNDICE) % tema_CONTAR;
            if (tema_Estado[Seguinte_cargo] == 1) { ao_corrente_tema = Seguinte_cargo; marco_ÍNDICE = tema_marco[Seguinte_cargo]; modificar_solicitude = false; return true; }
        }
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < tema_CONTAR; Loop_ÍNDICE++) if (tema_Estado[Loop_ÍNDICE] != 3) { erro_VALOR("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int nome_constante, int 서술상수, int comando_CÓDIGO) { Proceso_tema(nome_constante, 서술상수, comando_CÓDIGO, false); }
    static void Proceso_tema(int nome_constante, int 서술상수, int comando_CÓDIGO, boolean Galego) {
        if (comando_CÓDIGO == 184 && Word_SMS(nome_constante, Galego ? "suspender_tarefa" : "yield") && Word_SMS(서술상수, "()V")) { modificar_solicitude = true; return; }
        if (comando_CÓDIGO == 184 && Word_SMS(nome_constante, "currentThread") && Word_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(tema_obxecto[ao_corrente_tema], 2); return; }
        if (comando_CÓDIGO == 183 && Word_SMS(nome_constante, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, Galego ? "(LGalego/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int obxectivo_ENDEREZO = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), obxecto_Material_de_referencia = 빼기(2);
            if (!객체유효(obxecto_Material_de_referencia)) return;
            if (힙[obxecto_Material_de_referencia] == 13) { 힙[obxecto_Material_de_referencia + 2] = obxectivo_ENDEREZO; 힙참조[obxecto_Material_de_referencia + 2] = 1; }
            else if (obxectivo_ENDEREZO != 0) erro_VALOR("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (comando_CÓDIGO == 182 && (Word_SMS(nome_constante, Galego ? "START_tarefa" : "start") || Word_SMS(nome_constante, Galego ? "기다리기" : "join")) && Word_SMS(서술상수, "()V") || comando_CÓDIGO == 182 && Word_SMS(nome_constante, Galego ? "살아있는가" : "isAlive") && Word_SMS(서술상수, "()Z")) {
            int obxecto_Material_de_referencia = 빼기(2); if (!객체유효(obxecto_Material_de_referencia)) return;
            int conta_VALOR = -1; for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < tema_CONTAR; Loop_ÍNDICE++) if (tema_obxecto[Loop_ÍNDICE] == obxecto_Material_de_referencia) conta_VALOR = Loop_ÍNDICE;
            if (Word_SMS(nome_constante, Galego ? "살아있는가" : "isAlive")) { 넣기(conta_VALOR >= 0 && tema_Estado[conta_VALOR] != 3 ? 1 : 0, 1); return; }
            if (Word_SMS(nome_constante, Galego ? "기다리기" : "join")) { if (conta_VALOR >= 0 && tema_Estado[conta_VALOR] != 3) { 가닥대기[ao_corrente_tema] = conta_VALOR; tema_Estado[ao_corrente_tema] = 2; modificar_solicitude = true; } return; }
            if (conta_VALOR >= 0) { 예외던짐(Galego ? 38 : 16, "thread already started"); return; }
            if (tema_CONTAR == 4) { erro_VALOR("thread limit (4 including main)"); return; }
            int obxectivo_ENDEREZO = 힙[obxecto_Material_de_referencia] == 13 ? 힙[obxecto_Material_de_referencia + 2] : obxecto_Material_de_referencia;
            int Ficheiro_ÍNDICE = obxectivo_ENDEREZO > 0 && 힙[obxectivo_ENDEREZO] >= 32 ? 이름함수(힙[obxectivo_ENDEREZO] - 32, Galego ? "Executar" : "run", "()V") : -1;
            if (obxectivo_ENDEREZO != 0 && Ficheiro_ÍNDICE < 0) { erro_VALOR("Runnable.run required"); return; }
            conta_VALOR = tema_CONTAR++; tema_obxecto[conta_VALOR] = obxecto_Material_de_referencia; tema_obxectivo[conta_VALOR] = obxectivo_ENDEREZO;
            int marco = conta_VALOR * 32; tema_marco[conta_VALOR] = Ficheiro_ÍNDICE < 0 ? marco - 1 : marco; tema_Estado[conta_VALOR] = Ficheiro_ÍNDICE < 0 ? 3 : 1;
            if (Ficheiro_ÍNDICE >= 0) { 틀함수[marco] = Ficheiro_ÍNDICE; marco_cargo[marco] = 함수시작[Ficheiro_ÍNDICE]; local_VALOR[marco * 128] = obxectivo_ENDEREZO; local_TIPO[marco * 128] = 2; }
            return;
        }
        erro_VALOR("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], ENDEREZO_SMS = new int[16];
    static int local_ENDEREZO() { return ENDEREZO_obxecto(0x7f000001); }
    static int ENDEREZO_obxecto(int VALOR) { int obxecto_Material_de_referencia = atribuír_Almacenamento(14, 1); if (!ERRO) 힙[obxecto_Material_de_referencia + 2] = VALOR; return obxecto_Material_de_referencia; }
    static int 주소해독(int obxecto_Material_de_referencia) {
        if (obxecto_Material_de_referencia == 0 || 글같음(obxecto_Material_de_referencia, hospedar_carácter("localhost"), false)) return 0x7f000001;
        if (!obxecto_VALOR(obxecto_Material_de_referencia, 1)) return 0;
        int datos_VALOR = 0, 총수 = 0, ENDEREZO_byte = 0, 자릿수 = 0, introdución_CONTAR = 힙[obxecto_Material_de_referencia + 1];
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE <= introdución_CONTAR; Loop_ÍNDICE++) {
            int código_de_carácter = Loop_ÍNDICE == introdución_CONTAR ? '.' : 힙[obxecto_Material_de_referencia + 2 + Loop_ÍNDICE];
            if (código_de_carácter == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } datos_VALOR = datos_VALOR << 8 | ENDEREZO_byte; 총수++; ENDEREZO_byte = 자릿수 = 0; }
            else { if (código_de_carácter < '0' || código_de_carácter > '9' || ++자릿수 > 3 || (ENDEREZO_byte = ENDEREZO_byte * 10 + código_de_carácter - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return datos_VALOR;
    }
    static int ENDEREZO_carácter(int datos_VALOR) {
        int introdución_CONTAR = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int ENDEREZO_byte = datos_VALOR >>> 이동비트 & 255;
            if (ENDEREZO_byte >= 100) ENDEREZO_SMS[introdución_CONTAR++] = '0' + ENDEREZO_byte / 100;
            if (ENDEREZO_byte >= 10) ENDEREZO_SMS[introdución_CONTAR++] = '0' + ENDEREZO_byte / 10 % 10;
            ENDEREZO_SMS[introdución_CONTAR++] = '0' + ENDEREZO_byte % 10; if (이동비트 != 0) ENDEREZO_SMS[introdución_CONTAR++] = '.';
        }
        int obxecto_Material_de_referencia = atribuír_Almacenamento(1, introdución_CONTAR); if (!ERRO) for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < introdución_CONTAR; Loop_ÍNDICE++) 힙[obxecto_Material_de_referencia + 2 + Loop_ÍNDICE] = ENDEREZO_SMS[Loop_ÍNDICE]; return obxecto_Material_de_referencia;
    }
    static void 통신호출(int propietario, int nome_constante, int 서술상수, int comando_CÓDIGO) {
        if (Word_SMS(propietario, "java/net/InetAddress")) {
            if (comando_CÓDIGO == 184 && Word_SMS(nome_constante, "getLoopbackAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(local_ENDEREZO(), 2); return; }
            if (comando_CÓDIGO == 184 && Word_SMS(nome_constante, "getByName") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int datos_VALOR = 주소해독(빼기(2)); if (던진객체 == 0 && !ERRO) 넣기(ENDEREZO_obxecto(datos_VALOR), 2); return;
            }
            if (comando_CÓDIGO == 182 && Word_SMS(nome_constante, "getHostAddress") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int obxecto_Material_de_referencia = 빼기(2); if (obxecto_VALOR(obxecto_Material_de_referencia, 14)) 넣기(ENDEREZO_carácter(힙[obxecto_Material_de_referencia + 2]), 2); return; }
        }
        if (Word_SMS(propietario, "java/net/DatagramPacket")) {
            if (comando_CÓDIGO == 183 && Word_SMS(nome_constante, "<init>") && (Word_SMS(서술상수, "([BI)V") || Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean destino_VALOR_Material_de_referencia = Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int número_do_porto = destino_VALOR_Material_de_referencia ? 빼기(1) : 0, ENDEREZO_Material_de_referencia = destino_VALOR_Material_de_referencia ? 빼기(2) : 0;
                int introdución_CONTAR = 빼기(1), datos_MATRIZ = 빼기(2), obxecto_Material_de_referencia = 빼기(2);
                if (!obxecto_VALOR(obxecto_Material_de_referencia, 16) || !obxecto_VALOR(datos_MATRIZ, 20)) return;
                if (introdución_CONTAR < 0 || introdución_CONTAR > 힙[datos_MATRIZ + 1] || número_do_porto < 0 || número_do_porto > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (ENDEREZO_Material_de_referencia != 0 && !obxecto_VALOR(ENDEREZO_Material_de_referencia, 14)) return;
                힙[obxecto_Material_de_referencia + 2] = datos_MATRIZ; 힙참조[obxecto_Material_de_referencia + 2] = 1; 힙[obxecto_Material_de_referencia + 3] = introdución_CONTAR;
                힙[obxecto_Material_de_referencia + 4] = ENDEREZO_Material_de_referencia; 힙참조[obxecto_Material_de_referencia + 4] = 1; 힙[obxecto_Material_de_referencia + 5] = número_do_porto; return;
            }
            if (comando_CÓDIGO == 182 && Word_SMS(nome_constante, "setLength") && Word_SMS(서술상수, "(I)V")) {
                int introdución_CONTAR = 빼기(1), obxecto_Material_de_referencia = 빼기(2); if (!obxecto_VALOR(obxecto_Material_de_referencia, 16)) return;
                if (introdución_CONTAR < 0 || introdución_CONTAR > 힙[힙[obxecto_Material_de_referencia + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[obxecto_Material_de_referencia + 3] = introdución_CONTAR; return;
            }
            if (comando_CÓDIGO == 182 && (Word_SMS(nome_constante, "getData") && Word_SMS(서술상수, "()[B") || Word_SMS(nome_constante, "getLength") && Word_SMS(서술상수, "()I") || Word_SMS(nome_constante, "getAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;") || Word_SMS(nome_constante, "getPort") && Word_SMS(서술상수, "()I"))) {
                int obxecto_Material_de_referencia = 빼기(2); if (!obxecto_VALOR(obxecto_Material_de_referencia, 16)) return;
                int introdución_cargo = Word_SMS(nome_constante, "getData") ? 2 : Word_SMS(nome_constante, "getLength") ? 3 : Word_SMS(nome_constante, "getAddress") ? 4 : 5;
                넣기(힙[obxecto_Material_de_referencia + introdución_cargo], introdución_cargo == 2 || introdución_cargo == 4 ? 2 : 1); return;
            }
        }
        if (Word_SMS(propietario, "java/net/DatagramSocket")) {
            if (comando_CÓDIGO == 183 && Word_SMS(nome_constante, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(I)V"))) {
                int número_do_porto = Word_SMS(서술상수, "()V") ? 0 : 빼기(1), obxecto_Material_de_referencia = 빼기(2); if (!obxecto_VALOR(obxecto_Material_de_referencia, 15)) return;
                if (número_do_porto < 0 || número_do_porto > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = usuario.abrir_Rede(número_do_porto); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[obxecto_Material_de_referencia + 2] = 열린파일번호; return;
            }
            if (comando_CÓDIGO == 182 && Word_SMS(nome_constante, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), obxecto_Material_de_referencia = 빼기(2); if (!obxecto_VALOR(obxecto_Material_de_referencia, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[obxecto_Material_de_referencia + 3] = 밀리초값; return;
            }
            if (comando_CÓDIGO == 182 && Word_SMS(nome_constante, "getLocalPort") && Word_SMS(서술상수, "()I")) { int obxecto_Material_de_referencia = 빼기(2); if (obxecto_VALOR(obxecto_Material_de_referencia, 15)) 넣기(힙[obxecto_Material_de_referencia + 2] < 0 ? -1 : usuario.Rede_porto(힙[obxecto_Material_de_referencia + 2]), 1); return; }
            if (comando_CÓDIGO == 182 && Word_SMS(nome_constante, "isClosed") && Word_SMS(서술상수, "()Z")) { int obxecto_Material_de_referencia = 빼기(2); if (obxecto_VALOR(obxecto_Material_de_referencia, 15)) 넣기(힙[obxecto_Material_de_referencia + 2] < 0 ? 1 : 0, 1); return; }
            if (comando_CÓDIGO == 182 && Word_SMS(nome_constante, "close") && Word_SMS(서술상수, "()V")) { int obxecto_Material_de_referencia = 빼기(2); if (obxecto_VALOR(obxecto_Material_de_referencia, 15) && 힙[obxecto_Material_de_referencia + 2] >= 0) { usuario.파일서술자닫기(힙[obxecto_Material_de_referencia + 2]); 힙[obxecto_Material_de_referencia + 2] = -1; } return; }
            if (comando_CÓDIGO == 182 && (Word_SMS(nome_constante, "send") || Word_SMS(nome_constante, "receive")) && Word_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int paquete_5cd5338b = 빼기(2), obxecto_Material_de_referencia = 빼기(2); if (!obxecto_VALOR(paquete_5cd5338b, 16) || !obxecto_VALOR(obxecto_Material_de_referencia, 15)) return;
                int datos_MATRIZ = 힙[paquete_5cd5338b + 2], 유효길이 = 힙[paquete_5cd5338b + 3], 열린파일번호 = 힙[obxecto_Material_de_referencia + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_SMS(nome_constante, "send")) {
                    if (!obxecto_VALOR(힙[paquete_5cd5338b + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 유효길이; Loop_ÍNDICE++) 통신임시[Loop_ÍNDICE] = 힙[datos_MATRIZ + 2 + Loop_ÍNDICE];
                    if (usuario.enviar_Rede(열린파일번호, 힙[힙[paquete_5cd5338b + 4] + 2], 힙[paquete_5cd5338b + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int introdución_CONTAR = usuario.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (introdución_CONTAR == -11) {
                        int ao_corrente_hora = usuario.밀리초();
                        if (힙[obxecto_Material_de_referencia + 4] == 0) 힙[obxecto_Material_de_referencia + 4] = ao_corrente_hora + 1;
                        if (힙[obxecto_Material_de_referencia + 3] > 0 && ao_corrente_hora - (힙[obxecto_Material_de_referencia + 4] - 1) >= 힙[obxecto_Material_de_referencia + 3]) { 힙[obxecto_Material_de_referencia + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(obxecto_Material_de_referencia, 2); 넣기(paquete_5cd5338b, 2); marco_cargo[marco_ÍNDICE] = marco_instrución[marco_ÍNDICE]; modificar_solicitude = true; return;
                    }
                    힙[obxecto_Material_de_referencia + 4] = 0;
                    if (introdución_CONTAR < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < introdución_CONTAR; Loop_ÍNDICE++) 힙[datos_MATRIZ + 2 + Loop_ÍNDICE] = (byte)통신임시[Loop_ÍNDICE];
                    힙[paquete_5cd5338b + 3] = introdución_CONTAR; 힙[paquete_5cd5338b + 4] = ENDEREZO_obxecto(통신임시[513]); 힙참조[paquete_5cd5338b + 4] = 1; 힙[paquete_5cd5338b + 5] = 통신임시[512];
                }
                return;
            }
        }
        erro_VALOR("unsupported java.net method");
    }
    static boolean 흐름대기(int obxecto_Material_de_referencia) {
        int ao_corrente_hora = usuario.밀리초();
        if (힙[obxecto_Material_de_referencia + 5] == 0) 힙[obxecto_Material_de_referencia + 5] = ao_corrente_hora + 1;
        if (힙[obxecto_Material_de_referencia + 3] > 0 && ao_corrente_hora - (힙[obxecto_Material_de_referencia + 5] - 1) >= 힙[obxecto_Material_de_referencia + 3]) { 힙[obxecto_Material_de_referencia + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        marco_cargo[marco_ÍNDICE] = marco_instrución[marco_ÍNDICE]; modificar_solicitude = true; return true;
    }
    static void 흐름호출(int propietario, int nome_constante, int 서술상수, int comando_CÓDIGO) {
        boolean 수신쪽 = Word_SMS(propietario, "java/net/ServerSocket"), fluxo = Word_SMS(propietario, "java/io/InputStream") || Word_SMS(propietario, "java/io/OutputStream");
        if (!fluxo && comando_CÓDIGO == 183 && Word_SMS(nome_constante, "<init>")) {
            boolean Tecnoloxía_da_información_TI_baleiro_Estado = Word_SMS(서술상수, "()V"), 이름지정여부 = Word_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(Tecnoloxía_da_información_TI_baleiro_Estado || 수신쪽 && Word_SMS(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { erro_VALOR("unsupported socket constructor"); return; }
            int número_do_porto = Tecnoloxía_da_información_TI_baleiro_Estado ? 0 : 빼기(1), ENDEREZO_Material_de_referencia = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, obxecto_Material_de_referencia = 빼기(2);
            if (!obxecto_VALOR(obxecto_Material_de_referencia, 수신쪽 ? 18 : 17)) return;
            if (número_do_porto < 0 || número_do_porto > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !obxecto_VALOR(ENDEREZO_Material_de_referencia, 14)) return;
            int Rede_ENDEREZO = 이름지정여부 ? 주소해독(ENDEREZO_Material_de_referencia) : 주소지정여부 ? 힙[ENDEREZO_Material_de_referencia + 2] : 0x7f000001;
            if (ERRO || 던진객체 != 0) return;
            int 열린파일번호 = usuario.fluxo_control(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = Tecnoloxía_da_información_TI_baleiro_Estado ? 0 : 수신쪽 ? usuario.fluxo_control(1, 열린파일번호, número_do_porto) : usuario.CONECTAR_fluxo(열린파일번호, Rede_ENDEREZO, número_do_porto);
            if (처리값 < 0) { usuario.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[obxecto_Material_de_referencia + 2] = 열린파일번호; 힙[obxecto_Material_de_referencia + 4] = número_do_porto; 힙[obxecto_Material_de_referencia + 6] = Tecnoloxía_da_información_TI_baleiro_Estado ? 0 : 1; return;
        }
        if (!fluxo && Word_SMS(nome_constante, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), obxecto_Material_de_referencia = 빼기(2); if (!obxecto_VALOR(obxecto_Material_de_referencia, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[obxecto_Material_de_referencia + 3] = 밀리초값; return; }
        if (!fluxo && Word_SMS(nome_constante, "close") && Word_SMS(서술상수, "()V")) { int obxecto_Material_de_referencia = 빼기(2); if (obxecto_VALOR(obxecto_Material_de_referencia, 수신쪽 ? 18 : 17) && 힙[obxecto_Material_de_referencia + 2] >= 0) { usuario.파일서술자닫기(힙[obxecto_Material_de_referencia + 2]); 힙[obxecto_Material_de_referencia + 2] = -1; } return; }
        if (!fluxo && (Word_SMS(nome_constante, "getLocalPort") || Word_SMS(nome_constante, "getPort") || Word_SMS(nome_constante, "isClosed") || Word_SMS(nome_constante, "isConnected"))) {
            int obxecto_Material_de_referencia = 빼기(2); if (!obxecto_VALOR(obxecto_Material_de_referencia, 수신쪽 ? 18 : 17)) return;
            넣기(Word_SMS(nome_constante, "isClosed") ? 힙[obxecto_Material_de_referencia + 2] < 0 ? 1 : 0 : Word_SMS(nome_constante, "isConnected") ? 힙[obxecto_Material_de_referencia + 6] : Word_SMS(nome_constante, "getPort") ? 힙[obxecto_Material_de_referencia + 4] : 힙[obxecto_Material_de_referencia + 2] < 0 ? -1 : usuario.fluxo_control(4, 힙[obxecto_Material_de_referencia + 2], 0), 1); return;
        }
        if (수신쪽 && Word_SMS(nome_constante, "accept") && Word_SMS(서술상수, "()Ljava/net/Socket;")) {
            int obxecto_Material_de_referencia = 빼기(2); if (!obxecto_VALOR(obxecto_Material_de_referencia, 18)) return; int 열린파일번호 = usuario.fluxo_control(3, 힙[obxecto_Material_de_referencia + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(obxecto_Material_de_referencia)) 넣기(obxecto_Material_de_referencia, 2); return; }
            힙[obxecto_Material_de_referencia + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = atribuír_Almacenamento(17, 5); if (ERRO) { usuario.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = usuario.fluxo_control(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !fluxo && ((Word_SMS(nome_constante, "getInputStream") && Word_SMS(서술상수, "()Ljava/io/InputStream;")) || (Word_SMS(nome_constante, "getOutputStream") && Word_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int obxecto_Material_de_referencia = 빼기(2); if (!obxecto_VALOR(obxecto_Material_de_referencia, 17)) return; if (힙[obxecto_Material_de_referencia + 2] < 0 || 힙[obxecto_Material_de_referencia + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = atribuír_Almacenamento(19, 4); if (ERRO) return; 힙[반환값 + 2] = obxecto_Material_de_referencia; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Word_SMS(nome_constante, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (fluxo) {
            boolean 읽기여부 = Word_SMS(nome_constante, "read"), Tecnoloxía_da_información_TI_escribir_cirurxía = Word_SMS(nome_constante, "write"), bloquear = Word_SMS(서술상수, "([B)I") || Word_SMS(서술상수, "([B)V"), Tecnoloxía_da_información_TI_SUBMATRIZ = Word_SMS(서술상수, "([BII)I") || Word_SMS(서술상수, "([BII)V");
            int introdución_CONTAR = Tecnoloxía_da_información_TI_SUBMATRIZ ? 빼기(1) : 0, 시작변위 = Tecnoloxía_da_información_TI_SUBMATRIZ ? 빼기(1) : 0, datos_MATRIZ = bloquear || Tecnoloxía_da_información_TI_SUBMATRIZ ? 빼기(2) : 0;
            int datos_VALOR = Tecnoloxía_da_información_TI_escribir_cirurxía && Word_SMS(서술상수, "(I)V") ? 빼기(1) : 0, obxecto_Material_de_referencia = 빼기(2);
            if (!obxecto_VALOR(obxecto_Material_de_referencia, 19)) return; int 부모참조 = 힙[obxecto_Material_de_referencia + 2], 열린파일번호 = 힙[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_SMS(nome_constante, "close") && Word_SMS(서술상수, "()V")) { usuario.파일서술자닫기(열린파일번호); 힙[부모참조 + 2] = -1; return; }
            if (Word_SMS(nome_constante, "flush") && Word_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !Tecnoloxía_da_información_TI_escribir_cirurxía) || 읽기여부 != (힙[obxecto_Material_de_referencia + 3] == 0)) { erro_VALOR("unsupported stream operation"); return; }
            if (bloquear || Tecnoloxía_da_información_TI_SUBMATRIZ) { if (!obxecto_VALOR(datos_MATRIZ, 20)) return; if (bloquear) introdución_CONTAR = 힙[datos_MATRIZ + 1]; if (시작변위 < 0 || introdución_CONTAR < 0 || 시작변위 > 힙[datos_MATRIZ + 1] - introdución_CONTAR) { 예외던짐(6, "stream array bounds"); return; } }
            else introdución_CONTAR = 1;
            if (introdución_CONTAR == 0) { if (읽기여부) 넣기(0, 1); return; }
            int Completadas_CONTAR = Tecnoloxía_da_información_TI_escribir_cirurxía ? 힙[obxecto_Material_de_referencia + 4] : 0, 처리값 = 0;
            while (Completadas_CONTAR < introdución_CONTAR) {
                처리값 = 읽기여부 ? usuario.파일한바이트읽기(열린파일번호) : usuario.파일한바이트쓰기(열린파일번호, bloquear || Tecnoloxía_da_información_TI_SUBMATRIZ ? 힙[datos_MATRIZ + 2 + 시작변위 + Completadas_CONTAR] : datos_VALOR);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (bloquear || Tecnoloxía_da_información_TI_SUBMATRIZ)) 힙[datos_MATRIZ + 2 + 시작변위 + Completadas_CONTAR] = (byte)처리값;
                Completadas_CONTAR++; if (읽기여부 && !(bloquear || Tecnoloxía_da_información_TI_SUBMATRIZ)) break;
            }
            if (처리값 == -11 && (Tecnoloxía_da_información_TI_escribir_cirurxía || Completadas_CONTAR == 0)) {
                힙[obxecto_Material_de_referencia + 4] = Completadas_CONTAR;
                if (흐름대기(부모참조)) { 넣기(obxecto_Material_de_referencia, 2); if (bloquear || Tecnoloxía_da_información_TI_SUBMATRIZ) 넣기(datos_MATRIZ, 2); if (Tecnoloxía_da_información_TI_SUBMATRIZ) { 넣기(시작변위, 1); 넣기(introdución_CONTAR, 1); } if (Tecnoloxía_da_información_TI_escribir_cirurxía && !(bloquear || Tecnoloxía_da_información_TI_SUBMATRIZ)) 넣기(datos_VALOR, 1); } return;
            }
            힙[obxecto_Material_de_referencia + 4] = 0; 힙[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(Completadas_CONTAR == 0 && 처리값 == 256 ? -1 : bloquear || Tecnoloxía_da_información_TI_SUBMATRIZ ? Completadas_CONTAR : 처리값, 1); return;
        }
        erro_VALOR("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int nome_constante) {
        if (Word_SMS(nome_constante, "Galego/자체/Xanela")) return 24;
        if (Word_SMS(nome_constante, "Galego/자체/Etiqueta")) return 26;
        if (Word_SMS(nome_constante, "Galego/자체/botón")) return 27;
        if (Word_SMS(nome_constante, "Galego/자체/SMS_campo")) return 28;
        if (Word_SMS(nome_constante, "Galego/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int nome_constante) {
        return 한국어화면종(nome_constante) != 0 || Word_SMS(nome_constante, "Galego/자체/화면구성요소") || Word_SMS(nome_constante, "Galego/자체/evento_cola");
    }
    static int 화면종(int nome_constante) {
        int 한국어종 = 한국어화면종(nome_constante); if (한국어종 != 0) return 한국어종;
        if (Word_SMS(nome_constante, "javax/swing/JFrame")) return 24;
        if (Word_SMS(nome_constante, "javax/swing/JPanel")) return 25;
        if (Word_SMS(nome_constante, "javax/swing/JLabel")) return 26;
        if (Word_SMS(nome_constante, "javax/swing/JButton")) return 27;
        if (Word_SMS(nome_constante, "javax/swing/JTextField")) return 28;
        if (Word_SMS(nome_constante, "java/awt/event/ActionEvent")) return 29;
        if (Word_SMS(nome_constante, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int nome_constante) {
        return 화면종(nome_constante) != 0 || Word_SMS(nome_constante, "java/awt/Component") || Word_SMS(nome_constante, "java/awt/Container") || Word_SMS(nome_constante, "javax/swing/JComponent") || Word_SMS(nome_constante, "javax/swing/AbstractButton") || Word_SMS(nome_constante, "javax/swing/text/JTextComponent") || Word_SMS(nome_constante, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int obxecto_Material_de_referencia) { if (!객체유효(obxecto_Material_de_referencia)) return false; if (힙[obxecto_Material_de_referencia] < 24 || 힙[obxecto_Material_de_referencia] > 28) { erro_VALOR("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int obxecto_Material_de_referencia, int SMS_Material_de_referencia) {
        if (SMS_Material_de_referencia != 0 && !obxecto_VALOR(SMS_Material_de_referencia, 1)) return;
        int introdución_CONTAR = SMS_Material_de_referencia == 0 ? 0 : 힙[SMS_Material_de_referencia + 1]; if (introdución_CONTAR > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < introdución_CONTAR; Loop_ÍNDICE++) 화면글임시[Loop_ÍNDICE] = 힙[SMS_Material_de_referencia + 2 + Loop_ÍNDICE];
        if (usuario.화면글(힙[obxecto_Material_de_referencia + 2], 화면글임시, introdución_CONTAR) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[obxecto_Material_de_referencia + 3] = SMS_Material_de_referencia; 힙참조[obxecto_Material_de_referencia + 3] = 1;
    }
    static int 화면문자읽기(int obxecto_Material_de_referencia) {
        int conta_VALOR = 힙[obxecto_Material_de_referencia + 2], introdución_CONTAR = usuario.화면연결(8, conta_VALOR, 0, 0, 0, 0), 사용수 = 0;
        if (introdución_CONTAR < 0) { erro_VALOR("GUI text read failed"); return 0; }
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < introdución_CONTAR; Loop_ÍNDICE++) { int 부호값 = usuario.화면연결(9, conta_VALOR, Loop_ÍNDICE, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = atribuír_Almacenamento(1, 사용수); if (!ERRO) for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 사용수; Loop_ÍNDICE++) 힙[반환값 + 2 + Loop_ÍNDICE] = 화면글임시[Loop_ÍNDICE]; return 반환값;
    }
    /* Galego 객체를 직접 만들고 kernel_VALOR 화면 기능에 연결한다. Swing obxecto_VALOR/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int propietario, int nome_constante, int 서술상수, int comando_CÓDIGO) {
        if (Word_SMS(propietario, "Galego/자체/evento_cola")) {
            if (comando_CÓDIGO == 184 && Word_SMS(nome_constante, "나중에실행") && Word_SMS(서술상수, "(LGalego/자체/실행할일;)V")) {
                int tarefa_acción = 빼기(2); if (!객체유효(tarefa_acción)) return;
                if (나중수 == 8) { erro_VALOR("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = tarefa_acción; return;
            }
            if (comando_CÓDIGO == 184 && Word_SMS(nome_constante, "사건처리중인가") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            erro_VALOR("지원하지 않는 Galego 화면 일정 호출"); return;
        }
        if (Word_SMS(propietario, "Galego/자체/동작알림")) {
            int 알림 = 빼기(2); if (!obxecto_VALOR(알림, 29) || 힙[알림 + 3] == 0) return;
            if (Word_SMS(nome_constante, "evento_fonte") && Word_SMS(서술상수, "()LGalego/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (Word_SMS(nome_constante, "comando_SMS") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (Word_SMS(nome_constante, "ÍNDICE") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else erro_VALOR("지원하지 않는 Galego Acción 알림 호출"); return;
        }
        if (comando_CÓDIGO == 183 && Word_SMS(nome_constante, "<init>")) {
            int 종류 = 한국어화면종(propietario), 받이 = 0, 가로 = 0, Vertical_cargo = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Word_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (usuario.화면너비() - 폭) / 2; Vertical_cargo = (usuario.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Word_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Word_SMS(서술상수, "(Ljava/lang/String;IIIILGalego/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); Vertical_cargo = 빼기(1); 가로 = 빼기(1);
            } else { erro_VALOR("지원하지 않는 Galego 화면 생성자"); return; }
            int Texto = 빼기(2), elemento_VALOR = 빼기(2); if (!화면객체(elemento_VALOR)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || Vertical_cargo < 0 || 폭 > usuario.화면너비() - 가로 || 높이 > usuario.화면높이() - Vertical_cargo) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int ÍNDICE = usuario.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (ÍNDICE < 1 || ÍNDICE > 32) { erro_VALOR("화면 elemento_VALOR 자리가 가득 찼습니다"); return; }
            힙[elemento_VALOR + 2] = ÍNDICE; 화면참조[ÍNDICE - 1] = elemento_VALOR;
            힙[elemento_VALOR + 5] = 가로; 힙[elemento_VALOR + 6] = Vertical_cargo; 힙[elemento_VALOR + 7] = 폭; 힙[elemento_VALOR + 8] = 높이; 힙[elemento_VALOR + 10] = 2;
            힙[elemento_VALOR + 4] = 받이; 힙참조[elemento_VALOR + 4] = 1; 힙[elemento_VALOR + 12] = 1;
            usuario.화면연결(1, ÍNDICE, 가로, Vertical_cargo, 폭, 높이);
            if (종류 == 24) usuario.화면연결(7, ÍNDICE, 2, 0, 0, 0);
            화면문자설정(elemento_VALOR, Texto); return;
        }
        if (comando_CÓDIGO != 182) { erro_VALOR("잘못된 Galego 화면 호출 Orde"); return; }
        if (Word_SMS(nome_constante, "escribir_SMS") && Word_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int Texto = 빼기(2), elemento_VALOR = 빼기(2); if (화면객체(elemento_VALOR)) 화면문자설정(elemento_VALOR, Texto); return;
        }
        if (Word_SMS(nome_constante, "글읽기") && Word_SMS(서술상수, "()Ljava/lang/String;")) {
            int elemento_VALOR = 빼기(2); if (화면객체(elemento_VALOR)) 넣기(화면문자읽기(elemento_VALOR), 2); return;
        }
        if (Word_SMS(nome_constante, "동작맡기기") && Word_SMS(서술상수, "(LGalego/자체/동작받이;)V")) {
            int 받이 = 빼기(2), elemento_VALOR = 빼기(2);
            if (화면객체(elemento_VALOR)) { 힙[elemento_VALOR + 4] = 받이; 힙참조[elemento_VALOR + 4] = 1; 힙[elemento_VALOR + 12] = 1; } return;
        }
        if (Word_SMS(nome_constante, "engadir_elemento") && Word_SMS(서술상수, "(LGalego/자체/화면구성요소;)V")) {
            int neno_VALOR = 빼기(2), 부모 = 빼기(2); if (!화면객체(neno_VALOR) || !화면객체(부모)) return;
            if (usuario.화면연결(2, 힙[부모 + 2], 힙[neno_VALOR + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[neno_VALOR + 11] = 부모; 힙참조[neno_VALOR + 11] = 1; return;
        }
        if (Word_SMS(nome_constante, "자리정하기") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), Vertical_cargo = 빼기(1), 가로 = 빼기(1), elemento_VALOR = 빼기(2); if (!화면객체(elemento_VALOR)) return;
            if (usuario.화면연결(1, 힙[elemento_VALOR + 2], 가로, Vertical_cargo, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[elemento_VALOR + 5] = 가로; 힙[elemento_VALOR + 6] = Vertical_cargo; 힙[elemento_VALOR + 7] = 폭; 힙[elemento_VALOR + 8] = 높이; return;
        }
        if ((Word_SMS(nome_constante, "mostrar_ventá") || Word_SMS(nome_constante, "Pechar")) && Word_SMS(서술상수, "()V")) {
            boolean visibilidade_VALOR = Word_SMS(nome_constante, "mostrar_ventá"); int elemento_VALOR = 빼기(2); if (!화면객체(elemento_VALOR)) return;
            if (usuario.화면연결(visibilidade_VALOR ? 3 : 4, 힙[elemento_VALOR + 2], visibilidade_VALOR ? 1 : 0, 0, 0, 0) < 0) { erro_VALOR("화면은 interactivo 명령에서 실행해야 합니다"); return; }
            힙[elemento_VALOR + 9] = visibilidade_VALOR ? 1 : 0; return;
        }
        if (Word_SMS(nome_constante, "보이는가") && Word_SMS(서술상수, "()Z")) { int elemento_VALOR = 빼기(2); if (화면객체(elemento_VALOR)) 넣기(힙[elemento_VALOR + 9], 1); return; }
        erro_VALOR("지원하지 않는 Galego 화면 메서드");
    }
    static void 화면호출(int propietario, int nome_constante, int 서술상수, int comando_CÓDIGO) {
        if (Word_SMS(propietario, "javax/swing/SwingUtilities")) {
            if (comando_CÓDIGO == 184 && Word_SMS(nome_constante, "invokeLater") && Word_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int obxecto_Material_de_referencia = 빼기(2); if (!객체유효(obxecto_Material_de_referencia)) return; if (나중수 == 8) { erro_VALOR("invokeLater queue full"); return; } 나중실행[나중수++] = obxecto_Material_de_referencia; return; }
            if (comando_CÓDIGO == 184 && Word_SMS(nome_constante, "isEventDispatchThread") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            erro_VALOR("unsupported SwingUtilities method"); return;
        }
        if (Word_SMS(propietario, "java/awt/event/ActionEvent")) {
            int obxecto_Material_de_referencia = 빼기(2); if (!obxecto_VALOR(obxecto_Material_de_referencia, 29)) return;
            if (Word_SMS(nome_constante, "getSource") && Word_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[obxecto_Material_de_referencia + 2], 2);
            else if (Word_SMS(nome_constante, "getActionCommand") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[obxecto_Material_de_referencia + 2]), 2);
            else if (Word_SMS(nome_constante, "getID") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else erro_VALOR("unsupported ActionEvent method"); return;
        }
        if (comando_CÓDIGO == 183 && Word_SMS(nome_constante, "<init>")) {
            int COLUMNAS = 0, SMS_Material_de_referencia = 0;
            if (Word_SMS(서술상수, "(I)V")) COLUMNAS = 빼기(1);
            else if (Word_SMS(서술상수, "(Ljava/lang/String;I)V")) { COLUMNAS = 빼기(1); SMS_Material_de_referencia = 빼기(2); }
            else if (Word_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_Material_de_referencia = 빼기(2);
            else if (Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_SMS(서술상수, "()V")) { erro_VALOR("unsupported Swing constructor"); return; }
            int obxecto_Material_de_referencia = 빼기(2); if (!객체유효(obxecto_Material_de_referencia)) return;
            if (힙[obxecto_Material_de_referencia] == 30) { erro_VALOR("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(obxecto_Material_de_referencia) || COLUMNAS < 0) return;
            int conta_VALOR = usuario.화면연결(0, 힙[obxecto_Material_de_referencia] - 23, 0, 0, 0, 0);
            if (conta_VALOR < 1 || conta_VALOR > 32) { erro_VALOR("GUI widget slots exhausted"); return; }
            힙[obxecto_Material_de_referencia + 2] = conta_VALOR; 화면참조[conta_VALOR - 1] = obxecto_Material_de_referencia; 힙[obxecto_Material_de_referencia + 5] = 힙[obxecto_Material_de_referencia] == 24 ? 130 : 16; 힙[obxecto_Material_de_referencia + 6] = 힙[obxecto_Material_de_referencia] == 24 ? 110 : 16;
            힙[obxecto_Material_de_referencia + 7] = 힙[obxecto_Material_de_referencia] == 24 ? 380 : 220; 힙[obxecto_Material_de_referencia + 8] = 힙[obxecto_Material_de_referencia] == 24 ? 240 : 28; 힙[obxecto_Material_de_referencia + 10] = 1;
            화면문자설정(obxecto_Material_de_referencia, SMS_Material_de_referencia); return;
        }
        if (Word_SMS(nome_constante, "setText") || Word_SMS(nome_constante, "setTitle")) { int SMS_Material_de_referencia = 빼기(2), obxecto_Material_de_referencia = 빼기(2); if (화면객체(obxecto_Material_de_referencia) && Word_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(obxecto_Material_de_referencia, SMS_Material_de_referencia); return; }
        if (Word_SMS(nome_constante, "getText") || Word_SMS(nome_constante, "getTitle")) { int obxecto_Material_de_referencia = 빼기(2); if (화면객체(obxecto_Material_de_referencia) && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(obxecto_Material_de_referencia), 2); return; }
        if (Word_SMS(nome_constante, "addActionListener") && Word_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), obxecto_Material_de_referencia = 빼기(2); if (화면객체(obxecto_Material_de_referencia)) { 힙[obxecto_Material_de_referencia + 4] = 수신참조; 힙참조[obxecto_Material_de_referencia + 4] = 1; } return; }
        if (Word_SMS(nome_constante, "getContentPane") && Word_SMS(서술상수, "()Ljava/awt/Container;")) { int obxecto_Material_de_referencia = 빼기(2); if (화면객체(obxecto_Material_de_referencia)) 넣기(obxecto_Material_de_referencia, 2); return; }
        if (Word_SMS(nome_constante, "setLayout") && Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int deseño_Material_de_referencia = 빼기(2), obxecto_Material_de_referencia = 빼기(2); if (화면객체(obxecto_Material_de_referencia) && deseño_Material_de_referencia != 0) erro_VALOR("only absolute layout (null) is supported"); return; }
        if (Word_SMS(nome_constante, "add") && (Word_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean deseño_condición = Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (deseño_condición) 빼기(2);
            int neno_Material_de_referencia = 빼기(2), obxecto_Material_de_referencia = 빼기(2); if (!화면객체(neno_Material_de_referencia) || !화면객체(obxecto_Material_de_referencia)) return;
            if (usuario.화면연결(2, 힙[obxecto_Material_de_referencia + 2], 힙[neno_Material_de_referencia + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[neno_Material_de_referencia + 11] = obxecto_Material_de_referencia; 힙참조[neno_Material_de_referencia + 11] = 1; if (!deseño_condición) 넣기(neno_Material_de_referencia, 2); return;
        }
        if (Word_SMS(nome_constante, "setBounds") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), Y_coordenada = 빼기(1), X_coordenada = 빼기(1), obxecto_Material_de_referencia = 빼기(2); if (!화면객체(obxecto_Material_de_referencia)) return;
            if (usuario.화면연결(1, 힙[obxecto_Material_de_referencia + 2], X_coordenada, Y_coordenada, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[obxecto_Material_de_referencia + 5] = X_coordenada; 힙[obxecto_Material_de_referencia + 6] = Y_coordenada; 힙[obxecto_Material_de_referencia + 7] = 너비; 힙[obxecto_Material_de_referencia + 8] = 높이; return;
        }
        if (Word_SMS(nome_constante, "setSize") && Word_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), obxecto_Material_de_referencia = 빼기(2); if (!화면객체(obxecto_Material_de_referencia)) return;
            if (usuario.화면연결(1, 힙[obxecto_Material_de_referencia + 2], 힙[obxecto_Material_de_referencia + 5], 힙[obxecto_Material_de_referencia + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[obxecto_Material_de_referencia + 7] = 너비; 힙[obxecto_Material_de_referencia + 8] = 높이; } return;
        }
        if (Word_SMS(nome_constante, "setLocationRelativeTo") && Word_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), obxecto_Material_de_referencia = 빼기(2); if (!화면객체(obxecto_Material_de_referencia)) return; if (상대배치 != 0) { erro_VALOR("only screen centering supported"); return; } 힙[obxecto_Material_de_referencia + 5] = (usuario.화면너비() - 힙[obxecto_Material_de_referencia + 7]) / 2; 힙[obxecto_Material_de_referencia + 6] = (usuario.화면높이() - 힙[obxecto_Material_de_referencia + 8]) / 2; usuario.화면연결(1, 힙[obxecto_Material_de_referencia + 2], 힙[obxecto_Material_de_referencia + 5], 힙[obxecto_Material_de_referencia + 6], 힙[obxecto_Material_de_referencia + 7], 힙[obxecto_Material_de_referencia + 8]); return; }
        if (Word_SMS(nome_constante, "setDefaultCloseOperation") && Word_SMS(서술상수, "(I)V")) { int política = 빼기(1), obxecto_Material_de_referencia = 빼기(2); if (화면객체(obxecto_Material_de_referencia)) { if (política < 0 || política > 3) 예외던짐(9, "close policy"); else { 힙[obxecto_Material_de_referencia + 10] = política; usuario.화면연결(7, 힙[obxecto_Material_de_referencia + 2], política, 0, 0, 0); } } return; }
        if (Word_SMS(nome_constante, "setVisible") && Word_SMS(서술상수, "(Z)V")) { int datos_VALOR = 빼기(1), obxecto_Material_de_referencia = 빼기(2); if (화면객체(obxecto_Material_de_referencia)) { int 처리값 = usuario.화면연결(3, 힙[obxecto_Material_de_referencia + 2], datos_VALOR, 0, 0, 0); if (처리값 < 0) erro_VALOR("Swing requires a standalone interactive command"); else 힙[obxecto_Material_de_referencia + 9] = datos_VALOR; } return; }
        if (Word_SMS(nome_constante, "dispose") && Word_SMS(서술상수, "()V")) { int obxecto_Material_de_referencia = 빼기(2); if (화면객체(obxecto_Material_de_referencia)) { usuario.화면연결(4, 힙[obxecto_Material_de_referencia + 2], 0, 0, 0, 0); 힙[obxecto_Material_de_referencia + 9] = 0; } return; }
        if (Word_SMS(nome_constante, "repaint") || Word_SMS(nome_constante, "validate")) { int obxecto_Material_de_referencia = 빼기(2); if (!화면객체(obxecto_Material_de_referencia) || !Word_SMS(서술상수, "()V")) return; usuario.화면연결(1, 힙[obxecto_Material_de_referencia + 2], 힙[obxecto_Material_de_referencia + 5], 힙[obxecto_Material_de_referencia + 6], 힙[obxecto_Material_de_referencia + 7], 힙[obxecto_Material_de_referencia + 8]); return; }
        if (Word_SMS(nome_constante, "isVisible") && Word_SMS(서술상수, "()Z")) { int obxecto_Material_de_referencia = 빼기(2); if (화면객체(obxecto_Material_de_referencia)) 넣기(힙[obxecto_Material_de_referencia + 9], 1); return; }
        erro_VALOR("unsupported Swing method (native subset)");
    }
    static void 사건실행(int obxectivo_ENDEREZO, int 사건번호, boolean Galego) {
        if (obxectivo_ENDEREZO < 1 || 힙[obxectivo_ENDEREZO] < 32) { erro_VALOR("Java event listener required"); return; }
        int Ficheiro_ÍNDICE = 이름함수(힙[obxectivo_ENDEREZO] - 32, 사건번호 == 0 ? (Galego ? "Executar" : "run") : (Galego ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (Galego ? "(LGalego/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (Ficheiro_ÍNDICE < 0) { erro_VALOR("event callback missing"); return; }
        ao_corrente_tema = 0; tema_CONTAR = 1; marco_ÍNDICE = 0; tema_Estado[0] = 1; marco_Montón[0] = 0; marco_bloquear[0] = iniciar_marco[0] = 0; modificar_solicitude = false;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 128; Loop_ÍNDICE++) { local_VALOR[Loop_ÍNDICE] = local_TIPO[Loop_ÍNDICE] = 0; }
        틀함수[0] = Ficheiro_ÍNDICE; marco_cargo[0] = 함수시작[Ficheiro_ÍNDICE]; local_VALOR[0] = obxectivo_ENDEREZO; local_TIPO[0] = 2;
        if (사건번호 != 0) { local_VALOR[1] = 사건번호; local_TIPO[1] = 2; }
        사건중 = true; executar_comando(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!ERRO) {
            if (나중수 > 0) { int obxectivo_ENDEREZO = 나중실행[0], Galego = 나중한국어[0]; for (int Loop_ÍNDICE = 1; Loop_ÍNDICE < 나중수; Loop_ÍNDICE++) { 나중실행[Loop_ÍNDICE - 1] = 나중실행[Loop_ÍNDICE]; 나중한국어[Loop_ÍNDICE - 1] = 나중한국어[Loop_ÍNDICE]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(obxectivo_ENDEREZO, 0, Galego != 0); continue; }
            if (usuario.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = usuario.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { erro_VALOR("GUI event I/O failed"); return; }
            int conta_VALOR = 사건번호 & 65535; if (conta_VALOR < 1 || conta_VALOR > 32) continue; int obxecto_Material_de_referencia = 화면참조[conta_VALOR - 1]; if (obxecto_Material_de_referencia == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[obxecto_Material_de_referencia + 10] != 0) 힙[obxecto_Material_de_referencia + 9] = 0;
                if (힙[obxecto_Material_de_referencia + 10] == 3) for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 32; Loop_ÍNDICE++) if (화면참조[Loop_ÍNDICE] != 0 && 힙[화면참조[Loop_ÍNDICE]] == 24) usuario.화면연결(4, Loop_ÍNDICE + 1, 0, 0, 0, 0);
            } else if (힙[obxecto_Material_de_referencia + 4] != 0) {
                int Léame_Material_de_referencia = atribuír_Almacenamento(29, 2); if (ERRO) return; 힙[Léame_Material_de_referencia + 2] = obxecto_Material_de_referencia; 힙[Léame_Material_de_referencia + 3] = 힙[obxecto_Material_de_referencia + 12]; 힙참조[Léame_Material_de_referencia + 2] = 1; 사건실행(힙[obxecto_Material_de_referencia + 4], Léame_Material_de_referencia, 힙[obxecto_Material_de_referencia + 12] != 0);
            }
        }
    }
    public static int Executar_2() {
        if (usuario.인수개수() == 1 && 자바도구.같음(usuario.Argumentos(0), "-version")) {
            usuario.Escritura("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (usuario.인수개수() < 1) { usuario.Escritura("Usage: java CLASS [ARGS]\n"); return 2; }
        introdución_Clase_Definición = carga_Clase_Definición(hospedar_carácter(usuario.Argumentos(0))); if (ERRO || introdución_Clase_Definición < 0) return 1;
        int introdución_p_VALOR = 이름함수(introdución_Clase_Definición, "Executar_2", "()V");
        boolean 한국어진입 = introdución_p_VALOR >= 0 && (함수권한[introdución_p_VALOR] & 9) == 9;
        if (!한국어진입) introdución_p_VALOR = 이름함수(introdución_Clase_Definición, "main", "([Ljava/lang/String;)V");
        if (introdución_p_VALOR < 0 || (함수권한[introdución_p_VALOR] & 9) != 9) erro_VALOR("public static void Executar_2() or main(String[] args) required");
        if (ERRO) return 1;
        int Argumentos = atribuír_Almacenamento(3, usuario.인수개수() - 1); MATRIZ_elemento[Argumentos] = -1;
        for (int 수 = 1; 수 < usuario.인수개수() && !ERRO; 수++) 힙[Argumentos + 1 + 수] = hospedar_carácter(usuario.Argumentos(수));
        marco_ÍNDICE = 0; 틀함수[0] = introdución_p_VALOR; marco_cargo[0] = 함수시작[introdución_p_VALOR]; local_VALOR[0] = 한국어진입 ? 0 : Argumentos; local_TIPO[0] = 한국어진입 ? 0 : 2;
        tema_Estado[0] = 1; tema_obxecto[0] = atribuír_Almacenamento(13, 2);
        executar_comando(); if (!ERRO) 화면사건들(); return ERRO ? 1 : 0;
    }
}
