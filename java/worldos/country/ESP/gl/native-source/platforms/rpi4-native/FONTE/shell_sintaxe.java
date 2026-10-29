// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 interactivo shell 문법. 파이프는 순차 executar_comando, 환경은 같은 셸에서 공유한다. */
public final class shell_sintaxe {
    static int[] FONTE = new int[4 * 4096], 종류 = new int[4 * 128], Executar_2 = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], VALOR_duración = new int[16];
    static int[] script_VALOR = new int[4 * 16384];
    static int Estado_VALOR, 깊이, 쓴수;
    static boolean 연결중, script_finalizar, extensión_erro;
    static boolean nome_carácter(int código_de_carácter) { return código_de_carácter >= 'a' && código_de_carácter <= 'z' || código_de_carácter >= 'A' && código_de_carácter <= 'Z' || código_de_carácter == '_' || código_de_carácter >= 128; }
    static boolean 이름뒤(int código_de_carácter) { return nome_carácter(código_de_carácter) || código_de_carácter >= '0' && código_de_carácter <= '9'; }
    static void ERRO(String Texto) { Panel.입출력전환(0); 단말.Escritura("Orde analizar_VALOR: "); 단말.Escritura(Texto); 단말.문자(10); Estado_VALOR = 2; }
    static int Lectura(int introdución_CONTAR, int 중첩깊이) {
        int ao_corrente_ÍNDICE = 0, 총수 = 0, BASE_cargo = 중첩깊이 * 4096, carácter_especial = 중첩깊이 * 128;
        while (ao_corrente_ÍNDICE < introdución_CONTAR) {
            while (ao_corrente_ÍNDICE < introdución_CONTAR && (FONTE[BASE_cargo + ao_corrente_ÍNDICE] == 32 || FONTE[BASE_cargo + ao_corrente_ÍNDICE] == 9)) ao_corrente_ÍNDICE++;
            if (ao_corrente_ÍNDICE == introdución_CONTAR || FONTE[BASE_cargo + ao_corrente_ÍNDICE] == '#') break;
            if (총수 == 128) { ERRO("낱말이 너무 많습니다"); return -1; }
            int START_cargo = ao_corrente_ÍNDICE, código_de_carácter = FONTE[BASE_cargo + ao_corrente_ÍNDICE], 자료종류 = 0;
            if (código_de_carácter == ';') { 자료종류 = 1; ao_corrente_ÍNDICE++; }
            else if (código_de_carácter == '&') { if (ao_corrente_ÍNDICE + 1 >= introdución_CONTAR || FONTE[BASE_cargo + ao_corrente_ÍNDICE + 1] != '&') { ERRO("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; ao_corrente_ÍNDICE += 2; }
            else if (código_de_carácter == '|') { ao_corrente_ÍNDICE++; 자료종류 = ao_corrente_ÍNDICE < introdución_CONTAR && FONTE[BASE_cargo + ao_corrente_ÍNDICE] == '|' ? 3 : 4; if (자료종류 == 3) ao_corrente_ÍNDICE++; }
            else if (código_de_carácter == '>') { ao_corrente_ÍNDICE++; 자료종류 = ao_corrente_ÍNDICE < introdución_CONTAR && FONTE[BASE_cargo + ao_corrente_ÍNDICE] == '>' ? 6 : 5; if (자료종류 == 6) ao_corrente_ÍNDICE++; }
            else if (código_de_carácter == '<') { 자료종류 = 7; ao_corrente_ÍNDICE++; }
            else {
                int Cita = 0;
                while (ao_corrente_ÍNDICE < introdución_CONTAR) {
                    código_de_carácter = FONTE[BASE_cargo + ao_corrente_ÍNDICE];
                    if (código_de_carácter == '`' && Cita != 39 || código_de_carácter == '$' && Cita != 39 && ao_corrente_ÍNDICE + 1 < introdución_CONTAR && FONTE[BASE_cargo + ao_corrente_ÍNDICE + 1] == '(') { ERRO("Orde RESULTANTE 치환은 지원하지 않습니다"); return -1; }
                    if (código_de_carácter == '\\' && Cita != 39) { if (++ao_corrente_ÍNDICE == introdución_CONTAR) { ERRO("Liña 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } ao_corrente_ÍNDICE++; continue; }
                    if (código_de_carácter == Cita) { Cita = 0; ao_corrente_ÍNDICE++; continue; }
                    if (Cita == 0 && (código_de_carácter == 39 || código_de_carácter == 34)) { Cita = código_de_carácter; ao_corrente_ÍNDICE++; continue; }
                    if (Cita == 0 && (código_de_carácter == 32 || código_de_carácter == 9 || código_de_carácter == ';' || código_de_carácter == '&' || código_de_carácter == '|' || código_de_carácter == '<' || código_de_carácter == '>')) break;
                    ao_corrente_ÍNDICE++;
                }
                if (Cita != 0) { ERRO("따옴표가 닫히지 않았습니다"); return -1; }
                if (ao_corrente_ÍNDICE < introdución_CONTAR && (FONTE[BASE_cargo + ao_corrente_ÍNDICE] == '>' || FONTE[BASE_cargo + ao_corrente_ÍNDICE] == '<')) {
                    boolean 수치 = ao_corrente_ÍNDICE > START_cargo;
                    for (int Loop_ÍNDICE = START_cargo; Loop_ÍNDICE < ao_corrente_ÍNDICE; Loop_ÍNDICE++) if (FONTE[BASE_cargo + Loop_ÍNDICE] < '0' || FONTE[BASE_cargo + Loop_ÍNDICE] > '9') 수치 = false;
                    if (수치) { ERRO("번호를 지정한 Ficheiro 서술자 E_S 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[carácter_especial + 총수] = 자료종류; Executar_2[carácter_especial + 총수] = START_cargo; 끝[carácter_especial + 총수] = ao_corrente_ÍNDICE; 총수++;
        }
        boolean 낱말 = false;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 총수; Loop_ÍNDICE++) {
            int 임시값 = 종류[carácter_especial + Loop_ÍNDICE];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_ÍNDICE == 총수 || 종류[carácter_especial + Loop_ÍNDICE] != 0) { ERRO("E_S 전환에 Ficheiro 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_ÍNDICE == 총수 - 1 && 임시값 != 1) { ERRO("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (총수 > 0 && !낱말 && 종류[carácter_especial + 총수 - 1] != 1) { ERRO("명령이 빠졌습니다"); return -1; }
        return 총수;
    }
    static boolean intervalo_SMS(int[] datos_MATRIZ, int local_START, int introdución_CONTAR, String carácter_cargo) {
        if (introdución_CONTAR != carácter_cargo.length()) return false; for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < introdución_CONTAR; Loop_ÍNDICE++) if (datos_MATRIZ[local_START + Loop_ÍNDICE] != carácter_cargo.charAt(Loop_ÍNDICE)) return false; return true;
    }
    static void 넣기(int byte_datos) {
        if (쓴수 >= 명령해석기.ficha_VALOR.length) { if (!extensión_erro) ERRO("변수를 펼친 명령이 너무 깁니다"); extensión_erro = true; return; }
        명령해석기.ficha_VALOR[쓴수++] = byte_datos;
    }
    static void 변수(int[] datos_MATRIZ, int START_cargo, int introdución_CONTAR) {
        if (intervalo_SMS(datos_MATRIZ, START_cargo, introdución_CONTAR, "PWD")) { 넣기('/'); for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Memoria_Ficheiros.ao_corrente_duración; Loop_ÍNDICE++) 넣기(Memoria_Ficheiros.ao_corrente_elemento[Loop_ÍNDICE]); return; }
        if (intervalo_SMS(datos_MATRIZ, START_cargo, introdución_CONTAR, "HOME")) { 넣기('/'); return; }
        if (intervalo_SMS(datos_MATRIZ, START_cargo, introdución_CONTAR, "?")) {
            int datos_VALOR = Estado_VALOR, díxito = 100; boolean 시작여부 = false;
            while (díxito > 0) { int 뒷값 = datos_VALOR / díxito; if (뒷값 != 0 || 시작여부 || díxito == 1) { 넣기('0' + 뒷값); 시작여부 = true; } datos_VALOR %= díxito; díxito /= 10; } return;
        }
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 16; Loop_ÍNDICE++) if (이름길이[Loop_ÍNDICE] == introdución_CONTAR) {
            boolean CORRESP = true; for (int interna_cargo = 0; interna_cargo < introdución_CONTAR; interna_cargo++) if (변수이름[Loop_ÍNDICE * 32 + interna_cargo] != datos_MATRIZ[START_cargo + interna_cargo]) CORRESP = false;
            if (CORRESP) { for (int interna_cargo = 0; interna_cargo < VALOR_duración[Loop_ÍNDICE]; interna_cargo++) 넣기(변수값[Loop_ÍNDICE * 256 + interna_cargo]); return; }
        }
    }
    static boolean Word_VALOR(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = Executar_2[중첩깊이 * 128 + 낱말번호], finalizar_cargo = 끝[중첩깊이 * 128 + 낱말번호], BASE_cargo = 중첩깊이 * 4096, Cita = 0;
        if (읽는자리 < finalizar_cargo && FONTE[BASE_cargo + 읽는자리] == '~' && (읽는자리 + 1 == finalizar_cargo || FONTE[BASE_cargo + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < finalizar_cargo) {
            int código_de_carácter = FONTE[BASE_cargo + 읽는자리++];
            if (código_de_carácter == Cita) { Cita = 0; continue; }
            if (Cita == 0 && (código_de_carácter == 39 || código_de_carácter == 34)) { Cita = código_de_carácter; continue; }
            if (código_de_carácter == '\\' && Cita != 39) { int Seguinte_cargo = FONTE[BASE_cargo + 읽는자리++]; if (Cita == 34 && Seguinte_cargo != '$' && Seguinte_cargo != '"' && Seguinte_cargo != '\\') 넣기('\\'); 넣기(Seguinte_cargo); continue; }
            if (código_de_carácter == '$' && Cita != 39 && 읽는자리 < finalizar_cargo) {
                boolean 중괄호자리 = FONTE[BASE_cargo + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < finalizar_cargo && FONTE[BASE_cargo + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < finalizar_cargo && 이름뒤(FONTE[BASE_cargo + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == finalizar_cargo || FONTE[BASE_cargo + 읽는자리] != '}')) { ERRO("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(FONTE, BASE_cargo + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(código_de_carácter);
        }
        return !extensión_erro;
    }
    static int 환경설정(int argumento_ÍNDICE, boolean eliminar) {
        int local_START = 명령해석기.시작점[argumento_ÍNDICE], finalizar_cargo = local_START + 명령해석기.duración_VALOR[argumento_ÍNDICE], 같음자리 = local_START;
        while (같음자리 < finalizar_cargo && 명령해석기.ficha_VALOR[같음자리] != '=') 같음자리++;
        int introdución_CONTAR = 같음자리 - local_START;
        if (introdución_CONTAR < 1 || introdución_CONTAR > 31 || !nome_carácter(명령해석기.ficha_VALOR[local_START]) || !eliminar && 같음자리 == finalizar_cargo || finalizar_cargo - 같음자리 - 1 > 255) return 2;
        for (int Loop_ÍNDICE = local_START; Loop_ÍNDICE < 같음자리; Loop_ÍNDICE++) if (!이름뒤(명령해석기.ficha_VALOR[Loop_ÍNDICE])) return 2;
        if (intervalo_SMS(명령해석기.ficha_VALOR, local_START, introdución_CONTAR, "PWD") || intervalo_SMS(명령해석기.ficha_VALOR, local_START, introdución_CONTAR, "HOME")) return 2;
        int 찾은여부 = -1, Tecnoloxía_da_información_TI_baleiro_Estado = -1;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 16; Loop_ÍNDICE++) {
            if (이름길이[Loop_ÍNDICE] == 0) Tecnoloxía_da_información_TI_baleiro_Estado = Loop_ÍNDICE;
            if (이름길이[Loop_ÍNDICE] != introdución_CONTAR) continue;
            boolean CORRESP = true; for (int interna_cargo = 0; interna_cargo < introdución_CONTAR; interna_cargo++) if (변수이름[Loop_ÍNDICE * 32 + interna_cargo] != 명령해석기.ficha_VALOR[local_START + interna_cargo]) CORRESP = false;
            if (CORRESP) 찾은여부 = Loop_ÍNDICE;
        }
        if (eliminar) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = Tecnoloxía_da_información_TI_baleiro_Estado; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = introdución_CONTAR; VALOR_duración[찾은여부] = finalizar_cargo - 같음자리 - 1;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < introdución_CONTAR; Loop_ÍNDICE++) 변수이름[찾은여부 * 32 + Loop_ÍNDICE] = 명령해석기.ficha_VALOR[local_START + Loop_ÍNDICE];
        for (int Loop_ÍNDICE = 같음자리 + 1; Loop_ÍNDICE < finalizar_cargo; Loop_ÍNDICE++) 변수값[찾은여부 * 256 + Loop_ÍNDICE - 같음자리 - 1] = 명령해석기.ficha_VALOR[Loop_ÍNDICE];
        return 0;
    }
    static void 환경보기() {
        단말.Escritura("HOME=/\nPWD="); Memoria_Ficheiros.ao_corrente_escribir(); 단말.문자(10);
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 16; Loop_ÍNDICE++) if (이름길이[Loop_ÍNDICE] > 0) {
            for (int interna_cargo = 0; interna_cargo < 이름길이[Loop_ÍNDICE]; interna_cargo++) Panel.직렬쓰기(변수이름[Loop_ÍNDICE * 32 + interna_cargo]); 단말.문자('=');
            for (int interna_cargo = 0; interna_cargo < VALOR_duración[Loop_ÍNDICE]; interna_cargo++) Panel.직렬쓰기(변수값[Loop_ÍNDICE * 256 + interna_cargo]); 단말.문자(10);
        }
    }
    static void executar_comando(int[] datos_MATRIZ, int 시작변위, int introdución_CONTAR, int 중첩깊이) {
        if (중첩깊이 >= 4 || introdución_CONTAR > 4096) { ERRO("Orde 파일의 aniñamento_VALOR 또는 Liña duración_VALOR 제한을 넘었습니다"); return; }
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < introdución_CONTAR; Loop_ÍNDICE++) FONTE[중첩깊이 * 4096 + Loop_ÍNDICE] = datos_MATRIZ[시작변위 + Loop_ÍNDICE];
        int 총수 = Lectura(introdución_CONTAR, 중첩깊이); if (총수 < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < 총수) {
            int Grupo_finalizar = 읽는자리;
            while (Grupo_finalizar < 총수 && (종류[중첩깊이 * 128 + Grupo_finalizar] == 0 || 종류[중첩깊이 * 128 + Grupo_finalizar] >= 4)) Grupo_finalizar++;
            boolean executar = 조건성립 == 1 || 조건성립 == 2 && Estado_VALOR == 0 || 조건성립 == 3 && Estado_VALOR != 0;
            if (executar) {
                boolean 이전자리 = false;
                while (읽는자리 < Grupo_finalizar) {
                    int Seguinte_cargo = 읽는자리; while (Seguinte_cargo < Grupo_finalizar && 종류[중첩깊이 * 128 + Seguinte_cargo] != 4) Seguinte_cargo++;
                    boolean CONECTAR_fluxo = Seguinte_cargo < Grupo_finalizar; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.ficha_CONTAR = 0; 쓴수 = 0; extensión_erro = false;
                    for (int Loop_ÍNDICE = 읽는자리; Loop_ÍNDICE < Seguinte_cargo; Loop_ÍNDICE++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + Loop_ÍNDICE];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { ERRO("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++Loop_ÍNDICE; } else { if (출력쪽 >= 0) { ERRO("Saída 전환이 겹쳤습니다"); return; } 출력쪽 = ++Loop_ÍNDICE; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.ficha_CONTAR == 32) { ERRO("인수가 너무 많습니다"); return; }
                        int argumento_ÍNDICE = 명령해석기.ficha_CONTAR++; 명령해석기.시작점[argumento_ÍNDICE] = 쓴수;
                        if (!Word_VALOR(Loop_ÍNDICE, 중첩깊이)) return;
                        명령해석기.duración_VALOR[argumento_ÍNDICE] = 쓴수 - 명령해석기.시작점[argumento_ÍNDICE];
                    }
                    연결중 = 이전자리 || CONECTAR_fluxo || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { ERRO("interactivo 명령과 Orde 파일은 E_S 전환이나 fluxo_VALOR 연결에 쓸 수 없습니다"); return; }
                    셸입출력.Executar_2(이전자리, CONECTAR_fluxo);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int introdución_cargo = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (introdución_cargo < 0) continue;
                        int START_cargo = 쓴수; if (!Word_VALOR(introdución_cargo, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = Memoria_Ficheiros.camiño_START(쓴수 - START_cargo);
                        for (int interna_cargo = START_cargo; 처리값 >= 0 && interna_cargo < 쓴수; interna_cargo++) 처리값 = Memoria_Ficheiros.camiño_byte(interna_cargo - START_cargo, 명령해석기.ficha_VALOR[interna_cargo]);
                        if (처리값 >= 0) 처리값 = Memoria_Ficheiros.Abrir(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.ERRO(처리값); Estado_VALOR = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.ficheiro_de_entrada = 처리값; else 셸입출력.출력파일 = 처리값;
                    }
                    셸입출력.Permitir_interactivo = 중첩깊이 == 0 && 읽는자리 == 0 && Seguinte_cargo == 총수;
                    깊이 = 중첩깊이; 명령해석기.RESULTANTE = 0; Panel.입출력전환(1);
                    명령해석기.Orde();
                    Panel.Terminal(3);
                    int 반환값 = 명령해석기.RESULTANTE, fluxo_erro = 셸입출력.erro_VALOR;
                    셸입출력.끝(); 연결중 = false;
                    Estado_VALOR = fluxo_erro < 0 ? 1 : 반환값;
                    if (fluxo_erro < 0) { 명령해석기.ERRO(fluxo_erro); return; }
                    if (script_finalizar || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = Seguinte_cargo + 1;
                }
            }
            if (Grupo_finalizar < 총수) 조건성립 = 종류[중첩깊이 * 128 + Grupo_finalizar];
            읽는자리 = Grupo_finalizar + 1;
        }
    }
    static void executar_Ficheiro() {
        if (명령해석기.ficha_CONTAR != 2 || 깊이 >= 3) { 명령해석기.RESULTANTE = 2; 단말.Escritura("사용법: sh Ficheiro (aniñamento_VALOR 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.CAMIÑO(1); if (처리값 >= 0) 처리값 = Memoria_Ficheiros.Abrir(0);
        if (처리값 < 0) { 명령해석기.ERRO(처리값); return; }
        int introdución_CONTAR = 0, byte_datos;
        while ((byte_datos = Memoria_Ficheiros.Lectura(처리값)) != 256 && byte_datos >= 0 && introdución_CONTAR < 16384) script_VALOR[중첩깊이 * 16384 + introdución_CONTAR++] = byte_datos;
        Memoria_Ficheiros.Pechar(처리값); Panel.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < introdución_CONTAR && !script_finalizar;) {
            int finalizar_cargo = 읽는자리; while (finalizar_cargo < introdución_CONTAR && script_VALOR[중첩깊이 * 16384 + finalizar_cargo] != 10) finalizar_cargo++;
            int 유효길이 = finalizar_cargo - 읽는자리; if (유효길이 > 0 && script_VALOR[중첩깊이 * 16384 + finalizar_cargo - 1] == 13) 유효길이--;
            executar_comando(script_VALOR, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = finalizar_cargo + 1;
        }
        명령해석기.RESULTANTE = Estado_VALOR; script_finalizar = false; 깊이 = 중첩깊이 - 1;
    }
}
