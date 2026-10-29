// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Escritura 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int duración_VALOR = 0;
    static boolean 앞줄복귀 = false;
    static boolean 줄넘침 = false;

    static boolean Orde(String Nome) {
        if (duración_VALOR < Nome.length()) return false;
        for (int ÍNDICE = 0; ÍNDICE < Nome.length(); ÍNDICE++)
            if (입력[ÍNDICE] != Nome.charAt(ÍNDICE)) return false;
        return duración_VALOR == Nome.length() || 입력[Nome.length()] == ' ';
    }

    static void mostrar_axuda() {
        SMS_Terminal.Escritura("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Terminal.Escritura("apps | run NAME [ARGS] | net\n");
        SMS_Terminal.Escritura("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Terminal.Escritura("sync (연결된 JKSTORE1 Store_VALOR 장치에 Ficheiro 보존)\n");
    }

    static void Proceso_VALOR_introdución() {
        if (duración_VALOR == 0) return;
        if (Orde("help")) mostrar_axuda();
        else if (Orde("sync")) {
            int RESULTANTE = 파일보존.sinc();
            SMS_Terminal.Escritura("Sync: "); SMS_Terminal.수쓰기(RESULTANTE); SMS_Terminal.문자(10);
        }
        else if (Orde("ls")) Memoria_sistema_de_ficheiros.introdución_Lista();
        else if (Orde("edit")) Memoria_sistema_de_ficheiros.Orde(입력, 4, duración_VALOR, 0);
        else if (Orde("cat")) Memoria_sistema_de_ficheiros.Orde(입력, 3, duración_VALOR, 1);
        else if (Orde("rm")) Memoria_sistema_de_ficheiros.Orde(입력, 2, duración_VALOR, 2);
        else if (Orde("java") || Orde("javac")) {
            int RESULTANTE = 실행관리.executar_comando(입력, 0, duración_VALOR);
            SMS_Terminal.Escritura("Exit: "); SMS_Terminal.수쓰기(RESULTANTE); SMS_Terminal.문자(10);
        }
        else if (Orde("apps")) 실행관리.introdución_Lista();
        else if (Orde("net")) Rede_Montón.Estado_VALOR();
        else if (Orde("run")) {
            int RESULTANTE = 실행관리.executar_comando(입력, 3, duración_VALOR);
            SMS_Terminal.Escritura("Exit: "); SMS_Terminal.수쓰기(RESULTANTE); SMS_Terminal.Escritura("\n");
        } else if (Orde("info")) {
            SMS_Terminal.Escritura("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Orde("mem")) {
            SMS_Terminal.Escritura("위쪽 Memoria_VALOR 공간(KiB): "); SMS_Terminal.수쓰기(기억공간.위쪽기억크기());
            SMS_Terminal.Escritura("\n배열 동적 Memoria_VALOR 공간(byte_VALOR): "); SMS_Terminal.수쓰기(dispositivo_VALOR.MATRIZ_uso());
            SMS_Terminal.Escritura(" / 262144\n작업 공간 sección_VALOR: "); SMS_Terminal.수쓰기(기억공간.사용개수());
            SMS_Terminal.Escritura(" / 8 (각 4096바이트)\n");
        } else if (Orde("alloc")) {
            int ÍNDICE = 기억공간.atribuír_Almacenamento();
            SMS_Terminal.Escritura("sección_VALOR ÍNDICE: "); SMS_Terminal.수쓰기(ÍNDICE); SMS_Terminal.Escritura("\n");
        } else if (Orde("free")) {
            if (duración_VALOR == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                SMS_Terminal.Escritura(기억공간.devolver_medida(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 sección_VALOR\n");
            } else SMS_Terminal.Escritura("사용법: free 0..7\n");
        } else if (Orde("echo")) {
            for (int ÍNDICE = 5; ÍNDICE < duración_VALOR; ÍNDICE++) SMS_Terminal.문자(입력[ÍNDICE]);
            SMS_Terminal.문자(10);
        } else if (Orde("clear")) SMS_Terminal.borrar_introdución();
        else if (Orde("test")) kernel.시험();
        else if (Orde("halt")) {
            SMS_Terminal.Escritura("HALTED\n");
            dispositivo_VALOR.정지();
        } else SMS_Terminal.Escritura("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void aceptar_E_escribir(int VALOR) {
        if (VALOR == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = VALOR == 13;
        if (VALOR == 10 || VALOR == 13) {
            SMS_Terminal.문자(10);
            if (Memoria_sistema_de_ficheiros.편집중) Memoria_sistema_de_ficheiros.Edición_liña(입력, duración_VALOR, 줄넘침);
            else Proceso_VALOR_introdución();
            duración_VALOR = 0;
            줄넘침 = false;
            SMS_Terminal.Escritura(Memoria_sistema_de_ficheiros.편집중 ? "...> " : "jkoros> ");
        } else if (VALOR == 8 || VALOR == 127) {
            if (duración_VALOR > 0) {
                duración_VALOR--;
                SMS_Terminal.직렬바이트(8); SMS_Terminal.직렬바이트(32); SMS_Terminal.직렬바이트(8);
                SMS_Terminal.화면문자(8);
            }
        } else if (VALOR >= 32 && VALOR < 127 && duración_VALOR < 입력.length) {
            입력[duración_VALOR++] = VALOR;
            SMS_Terminal.문자(VALOR);
        } else if (VALOR >= 32 && VALOR < 127) 줄넘침 = true;
    }

    static void Executar_2() {
        mostrar_axuda();
        SMS_Terminal.Escritura("READY\njkoros> ");
        while (true) {
            int VALOR = SMS_Terminal.직렬읽기();
            if (VALOR < 0) VALOR = teclado.Lectura();
            if (VALOR >= 0) aceptar_E_escribir(VALOR);
            else { Rede_Montón.verificar(); dispositivo_VALOR.잠시양보(); }
        }
    }
}
