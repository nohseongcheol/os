// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 shell 내장 Ferramentas. */
public final class shell_Ferramentas {
    static int[] datos = new int[16384];
    static int ficheiro_de_entrada = -1;
    static int abrir_Ficheiro(int argumento_ÍNDICE, int Proceso_MODO) {
        int 처리값 = 명령해석기.CAMIÑO(argumento_ÍNDICE); return 처리값 < 0 ? 처리값 : Memoria_Ficheiros.Abrir(Proceso_MODO);
    }
    static boolean 입력준비(int argumento_ÍNDICE) {
        ficheiro_de_entrada = -1;
        if (argumento_ÍNDICE < 명령해석기.ficha_CONTAR) {
            ficheiro_de_entrada = abrir_Ficheiro(argumento_ÍNDICE, 0);
            if (ficheiro_de_entrada < 0) { 명령해석기.ERRO(ficheiro_de_entrada); return false; }
        }
        return true;
    }
    static int Lectura() {
        if (ficheiro_de_entrada >= 3) return Memoria_Ficheiros.Lectura(ficheiro_de_entrada);
        while (true) {
            int byte_datos = Panel.직렬읽기(); if (byte_datos == -2 || byte_datos == 4) return 256;
            if (byte_datos == 3) { 명령해석기.RESULTANTE = 130; return 256; }
            if (byte_datos >= 0) return byte_datos; Panel.suspender_CPU();
        }
    }
    static void Pechar() { if (ficheiro_de_entrada >= 3) Memoria_Ficheiros.Pechar(ficheiro_de_entrada); ficheiro_de_entrada = -1; }
    static void ver_VALOR() {
        int 마지막자리 = 명령해석기.ficha_CONTAR == 1 ? 2 : 명령해석기.ficha_CONTAR;
        for (int argumento_ÍNDICE = 1; argumento_ÍNDICE < 마지막자리; argumento_ÍNDICE++) {
            if (!입력준비(argumento_ÍNDICE)) continue;
            int byte_datos; while ((byte_datos = Lectura()) != 256 && byte_datos >= 0) Panel.직렬쓰기(byte_datos);
            if (byte_datos < 0) 명령해석기.ERRO(byte_datos); Pechar();
        }
    }
    static void Ficheiro_caso(String 동작번호) {
        if (명령해석기.ficha_CONTAR != 2) { 명령해석기.RESULTANTE = 2; 단말.Escritura("사용법: mkdir/rmdir/touch Ficheiro\n"); return; }
        int 처리값 = 명령해석기.CAMIÑO(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = Memoria_Ficheiros.crear_directorio();
            else if (동작번호.charAt(0) == 'r') 처리값 = Memoria_Ficheiros.eliminar_directorio();
            else { 처리값 = Memoria_Ficheiros.Abrir(65); if (처리값 >= 3) 처리값 = Memoria_Ficheiros.Pechar(처리값); }
        }
        if (처리값 < 0) 명령해석기.ERRO(처리값);
    }
    static void copiar_VALOR(boolean 이동여부) {
        if (명령해석기.ficha_CONTAR != 3) { 명령해석기.RESULTANTE = 2; 단말.Escritura("사용법: cp/mv 원본 destino_extremo (Ficheiro)\n"); return; }
        int 처리값 = 명령해석기.CAMIÑO(1); if (처리값 >= 0) 처리값 = Memoria_Ficheiros.organizar_VALOR();
        if (처리값 < 0) { 명령해석기.ERRO(처리값); return; }
        int 원본번호 = Memoria_Ficheiros.Busca_introdución(); if (원본번호 < 0) { 명령해석기.ERRO(-2); return; }
        int introdución_CONTAR = Memoria_Ficheiros.duración_VALOR[원본번호]; for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < introdución_CONTAR; Loop_ÍNDICE++) datos[Loop_ÍNDICE] = Memoria_Ficheiros.자료읽기(원본번호, Loop_ÍNDICE);
        처리값 = 명령해석기.CAMIÑO(2); if (처리값 >= 0) 처리값 = Memoria_Ficheiros.organizar_VALOR();
        if (처리값 < 0) { 명령해석기.ERRO(처리값); return; }
        if (Memoria_Ficheiros.Busca_introdución() == 원본번호) { if (!이동여부) 명령해석기.ERRO(-22); return; }
        if (이동여부) { 처리값 = Memoria_Ficheiros.이름바꾸기(원본번호); if (처리값 < 0) 명령해석기.ERRO(처리값); return; }
        int 열린파일번호 = Memoria_Ficheiros.Abrir(577); if (열린파일번호 < 0) { 명령해석기.ERRO(열린파일번호); return; }
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < introdución_CONTAR; Loop_ÍNDICE++) { 처리값 = Memoria_Ficheiros.Escritura(열린파일번호, datos[Loop_ÍNDICE]); if (처리값 < 0) { 명령해석기.ERRO(처리값); break; } }
        Memoria_Ficheiros.Pechar(열린파일번호);
    }
    static int díxito_VALOR(int argumento_ÍNDICE) {
        if (argumento_ÍNDICE >= 명령해석기.ficha_CONTAR) return -1;
        int introdución_CONTAR = 0; for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 명령해석기.duración_VALOR[argumento_ÍNDICE]; Loop_ÍNDICE++) { int código_de_carácter = 명령해석기.ficha_VALOR[명령해석기.시작점[argumento_ÍNDICE] + Loop_ÍNDICE]; if (código_de_carácter < '0' || código_de_carácter > '9' || introdución_CONTAR > 10000) return -1; introdución_CONTAR = introdución_CONTAR * 10 + código_de_carácter - '0'; } return introdución_CONTAR;
    }
    static void 세기() {
        int argumento_ÍNDICE = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; argumento_ÍNDICE++; }
        if (명령해석기.ficha_CONTAR > argumento_ÍNDICE + 1) { 명령해석기.RESULTANTE = 2; 단말.Escritura("사용법: wc [-c|-l|-w] [Ficheiro]\n"); return; }
        if (!입력준비(argumento_ÍNDICE)) return;
        int byte_CONTAR = 0, 줄수 = 0, 낱말수 = 0, byte_datos; boolean 낱말 = false;
        while ((byte_datos = Lectura()) >= 0 && byte_datos != 256) { byte_CONTAR++; if (byte_datos == 10) 줄수++; boolean espazo = byte_datos == 32 || byte_datos >= 9 && byte_datos <= 13; if (!espazo && !낱말) 낱말수++; 낱말 = !espazo; }
        Pechar(); if (byte_datos < 0) { 명령해석기.ERRO(byte_datos); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? byte_CONTAR : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(byte_CONTAR); } 단말.문자(10);
    }
    static void Busca_introdución() {
        if (명령해석기.ficha_CONTAR < 2 || 명령해석기.ficha_CONTAR > 3) { 명령해석기.RESULTANTE = 2; 단말.Escritura("사용법: grep 찾을문구 [Ficheiro]\n"); return; }
        if (!입력준비(2)) return;
        int introdución_CONTAR = 0, byte_datos, 일치수 = 0;
        while (true) {
            byte_datos = Lectura();
            if (byte_datos == 10 || byte_datos == 256 || byte_datos < 0) {
                boolean 찾은여부 = false;
                for (int Loop_ÍNDICE = 0; Loop_ÍNDICE <= introdución_CONTAR - 명령해석기.duración_VALOR[1]; Loop_ÍNDICE++) {
                    boolean 같은여부 = true; for (int interna_cargo = 0; interna_cargo < 명령해석기.duración_VALOR[1]; interna_cargo++) if (datos[Loop_ÍNDICE + interna_cargo] != 명령해석기.ficha_VALOR[명령해석기.시작점[1] + interna_cargo]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (introdución_CONTAR > 0 || byte_datos == 10)) { for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < introdución_CONTAR; Loop_ÍNDICE++) Panel.직렬쓰기(datos[Loop_ÍNDICE]); 단말.문자(10); 일치수++; }
                introdución_CONTAR = 0; if (byte_datos != 10) break;
            } else if (introdución_CONTAR < datos.length) datos[introdución_CONTAR++] = byte_datos;
            else { 명령해석기.ERRO(-28); Pechar(); return; }
        }
        Pechar(); if (byte_datos < 0) 명령해석기.ERRO(byte_datos); else if (명령해석기.RESULTANTE == 0) 명령해석기.RESULTANTE = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int argumento_ÍNDICE = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = díxito_VALOR(2); argumento_ÍNDICE = 3; }
        if (줄수 < 0 || 명령해석기.ficha_CONTAR > argumento_ÍNDICE + 1) { 명령해석기.RESULTANTE = 2; 단말.Escritura("사용법: head/tail [-n 줄수] [Ficheiro]\n"); return; }
        if (!입력준비(argumento_ÍNDICE)) return;
        int introdución_CONTAR = 0, byte_datos;
        while ((byte_datos = Lectura()) != 256 && byte_datos >= 0) { if (introdución_CONTAR == datos.length) { 명령해석기.ERRO(-28); Pechar(); return; } datos[introdución_CONTAR++] = byte_datos; }
        Pechar(); if (byte_datos < 0) { 명령해석기.ERRO(byte_datos); return; }
        int local_START = 0, finalizar_cargo = introdución_CONTAR;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int 총수 = 0; for (int Loop_ÍNDICE = introdución_CONTAR - 2; Loop_ÍNDICE >= 0; Loop_ÍNDICE--) if (datos[Loop_ÍNDICE] == 10 && ++총수 == 줄수) { local_START = Loop_ÍNDICE + 1; break; } }
        else { int 총수 = 0; for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < introdución_CONTAR; Loop_ÍNDICE++) if (datos[Loop_ÍNDICE] == 10 && ++총수 == 줄수) { finalizar_cargo = Loop_ÍNDICE + 1; break; } }
        for (int Loop_ÍNDICE = local_START; Loop_ÍNDICE < finalizar_cargo; Loop_ÍNDICE++) Panel.직렬쓰기(datos[Loop_ÍNDICE]);
    }
    static void escribir_Xuntos() {
        boolean Anexar = 명령해석기.같음(1, "-a"); int argumento_ÍNDICE = Anexar ? 2 : 1;
        if (명령해석기.ficha_CONTAR != argumento_ÍNDICE + 1) { 명령해석기.RESULTANTE = 2; 단말.Escritura("사용법: tee [-a] Ficheiro\n"); return; }
        int 열린파일번호 = abrir_Ficheiro(argumento_ÍNDICE, Anexar ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.ERRO(열린파일번호); return; }
        ficheiro_de_entrada = -1; int byte_datos;
        while ((byte_datos = Lectura()) != 256 && byte_datos >= 0) { int 처리값 = Memoria_Ficheiros.Escritura(열린파일번호, byte_datos); if (처리값 < 0) { 명령해석기.ERRO(처리값); break; } Panel.직렬쓰기(byte_datos); }
        Memoria_Ficheiros.Pechar(열린파일번호);
    }
}
