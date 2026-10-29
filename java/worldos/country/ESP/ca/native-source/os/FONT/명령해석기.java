// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Escriptura 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int durada_VALOR = 0;
    static boolean 앞줄복귀 = false;
    static boolean línia_sobreeiximent = false;

    static boolean Ordre(String Nom) {
        if (durada_VALOR < Nom.length()) return false;
        for (int INDEX = 0; INDEX < Nom.length(); INDEX++)
            if (입력[INDEX] != Nom.charAt(INDEX)) return false;
        return durada_VALOR == Nom.length() || 입력[Nom.length()] == ' ';
    }

    static void mostrar_ajuda() {
        SMS_Terminal.Escriptura("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Terminal.Escriptura("apps | run NAME [ARGS] | net\n");
        SMS_Terminal.Escriptura("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Terminal.Escriptura("sync (연결된 JKSTORE1 Store_VALOR 장치에 Fitxer 보존)\n");
    }

    static void Procés_VALOR_introducció() {
        if (durada_VALOR == 0) return;
        if (Ordre("help")) mostrar_ajuda();
        else if (Ordre("sync")) {
            int RESULTAT = 파일보존.sincronitzar();
            SMS_Terminal.Escriptura("Sync: "); SMS_Terminal.수쓰기(RESULTAT); SMS_Terminal.문자(10);
        }
        else if (Ordre("ls")) Memòria_sistema_d_arxius.introducció_Llista();
        else if (Ordre("edit")) Memòria_sistema_d_arxius.Ordre(입력, 4, durada_VALOR, 0);
        else if (Ordre("cat")) Memòria_sistema_d_arxius.Ordre(입력, 3, durada_VALOR, 1);
        else if (Ordre("rm")) Memòria_sistema_d_arxius.Ordre(입력, 2, durada_VALOR, 2);
        else if (Ordre("java") || Ordre("javac")) {
            int RESULTAT = 실행관리.Executa_ordre(입력, 0, durada_VALOR);
            SMS_Terminal.Escriptura("Exit: "); SMS_Terminal.수쓰기(RESULTAT); SMS_Terminal.문자(10);
        }
        else if (Ordre("apps")) 실행관리.introducció_Llista();
        else if (Ordre("net")) xarxa_Pila.Estat_VALOR();
        else if (Ordre("run")) {
            int RESULTAT = 실행관리.Executa_ordre(입력, 3, durada_VALOR);
            SMS_Terminal.Escriptura("Exit: "); SMS_Terminal.수쓰기(RESULTAT); SMS_Terminal.Escriptura("\n");
        } else if (Ordre("info")) {
            SMS_Terminal.Escriptura("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Ordre("mem")) {
            SMS_Terminal.Escriptura("위쪽 Memòria_VALOR 공간(KiB): "); SMS_Terminal.수쓰기(기억공간.MAJUSC_Memòria_canviar_la_mida());
            SMS_Terminal.Escriptura("\n배열 동적 Memòria_VALOR 공간(byte_VALOR): "); SMS_Terminal.수쓰기(dispositiu_VALOR.배열사용량());
            SMS_Terminal.Escriptura(" / 262144\n작업 공간 secció_VALOR: "); SMS_Terminal.수쓰기(기억공간.사용개수());
            SMS_Terminal.Escriptura(" / 8 (각 4096바이트)\n");
        } else if (Ordre("alloc")) {
            int INDEX = 기억공간.assignar_Emmagatzematge();
            SMS_Terminal.Escriptura("secció_VALOR INDEX: "); SMS_Terminal.수쓰기(INDEX); SMS_Terminal.Escriptura("\n");
        } else if (Ordre("free")) {
            if (durada_VALOR == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                SMS_Terminal.Escriptura(기억공간.tornar_les_tasques_mesura(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 secció_VALOR\n");
            } else SMS_Terminal.Escriptura("사용법: free 0..7\n");
        } else if (Ordre("echo")) {
            for (int INDEX = 5; INDEX < durada_VALOR; INDEX++) SMS_Terminal.문자(입력[INDEX]);
            SMS_Terminal.문자(10);
        } else if (Ordre("clear")) SMS_Terminal.esborrar_introducció();
        else if (Ordre("test")) nucli.시험();
        else if (Ordre("halt")) {
            SMS_Terminal.Escriptura("HALTED\n");
            dispositiu_VALOR.정지();
        } else SMS_Terminal.Escriptura("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void acceptar_I_escriure(int VALOR) {
        if (VALOR == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = VALOR == 13;
        if (VALOR == 10 || VALOR == 13) {
            SMS_Terminal.문자(10);
            if (Memòria_sistema_d_arxius.편집중) Memòria_sistema_d_arxius.Editats_línia(입력, durada_VALOR, línia_sobreeiximent);
            else Procés_VALOR_introducció();
            durada_VALOR = 0;
            línia_sobreeiximent = false;
            SMS_Terminal.Escriptura(Memòria_sistema_d_arxius.편집중 ? "...> " : "jkoros> ");
        } else if (VALOR == 8 || VALOR == 127) {
            if (durada_VALOR > 0) {
                durada_VALOR--;
                SMS_Terminal.직렬바이트(8); SMS_Terminal.직렬바이트(32); SMS_Terminal.직렬바이트(8);
                SMS_Terminal.화면문자(8);
            }
        } else if (VALOR >= 32 && VALOR < 127 && durada_VALOR < 입력.length) {
            입력[durada_VALOR++] = VALOR;
            SMS_Terminal.문자(VALOR);
        } else if (VALOR >= 32 && VALOR < 127) línia_sobreeiximent = true;
    }

    static void Executa_2() {
        mostrar_ajuda();
        SMS_Terminal.Escriptura("READY\njkoros> ");
        while (true) {
            int VALOR = SMS_Terminal.직렬읽기();
            if (VALOR < 0) VALOR = teclat.Lectura();
            if (VALOR >= 0) acceptar_I_escriure(VALOR);
            else { xarxa_Pila.verificar(); dispositiu_VALOR.잠시양보(); }
        }
    }
}
