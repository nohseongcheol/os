// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 язу 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int озынлык_VALUE = 0;
    static boolean 앞줄복귀 = false;
    static boolean юл_сыешмау = false;

    static boolean команда(String исем) {
        if (озынлык_VALUE < исем.length()) return false;
        for (int INDEX = 0; INDEX < исем.length(); INDEX++)
            if (입력[INDEX] != исем.charAt(INDEX)) return false;
        return озынлык_VALUE == исем.length() || 입력[исем.length()] == ' ';
    }

    static void күрсәтү_ярдәм() {
        СМС_Терминал.язу("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        СМС_Терминал.язу("apps | run NAME [ARGS] | net\n");
        СМС_Терминал.язу("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        СМС_Терминал.язу("sync (연결된 JKSTORE1 Store_VALUE 장치에 Birem 보존)\n");
    }

    static void Процесс_VALUE_кертү() {
        if (озынлык_VALUE == 0) return;
        if (команда("help")) күрсәтү_ярдәм();
        else if (команда("sync")) {
            int үлчәм = 파일보존.синхронлаштыру();
            СМС_Терминал.язу("Sync: "); СМС_Терминал.수쓰기(үлчәм); СМС_Терминал.문자(10);
        }
        else if (команда("ls")) Хәтер_файл_системасы.кертү_Исемлек();
        else if (команда("edit")) Хәтер_файл_системасы.команда(입력, 4, озынлык_VALUE, 0);
        else if (команда("cat")) Хәтер_файл_системасы.команда(입력, 3, озынлык_VALUE, 1);
        else if (команда("rm")) Хәтер_файл_системасы.команда(입력, 2, озынлык_VALUE, 2);
        else if (команда("java") || команда("javac")) {
            int үлчәм = 실행관리.үтәргә_команда(입력, 0, озынлык_VALUE);
            СМС_Терминал.язу("Exit: "); СМС_Терминал.수쓰기(үлчәм); СМС_Терминал.문자(10);
        }
        else if (команда("apps")) 실행관리.кертү_Исемлек();
        else if (команда("net")) Челтәр_Стәк.халәт_VALUE();
        else if (команда("run")) {
            int үлчәм = 실행관리.үтәргә_команда(입력, 3, озынлык_VALUE);
            СМС_Терминал.язу("Exit: "); СМС_Терминал.수쓰기(үлчәм); СМС_Терминал.язу("\n");
        } else if (команда("info")) {
            СМС_Терминал.язу("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (команда("mem")) {
            СМС_Терминал.язу("위쪽 Хәтер_VALUE 공간(KiB): "); СМС_Терминал.수쓰기(기억공간.UPPER_Хәтер_үлчәмен_үзгәртү());
            СМС_Терминал.язу("\n배열 동적 Хәтер_VALUE 공간(байт_VALUE): "); СМС_Терминал.수쓰기(мобиль_VALUE.МАССИВ_Таралыш());
            СМС_Терминал.язу(" / 262144\n작업 공간 өлеш_VALUE: "); СМС_Терминал.수쓰기(기억공간.사용개수());
            СМС_Терминал.язу(" / 8 (각 4096바이트)\n");
        } else if (команда("alloc")) {
            int INDEX = 기억공간.атап_бирү_Саклагыч();
            СМС_Терминал.язу("өлеш_VALUE INDEX: "); СМС_Терминал.수쓰기(INDEX); СМС_Терминал.язу("\n");
        } else if (команда("free")) {
            if (озынлык_VALUE == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                СМС_Терминал.язу(기억공간.кайтару_үлчәм(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 өлеш_VALUE\n");
            } else СМС_Терминал.язу("사용법: free 0..7\n");
        } else if (команда("echo")) {
            for (int INDEX = 5; INDEX < озынлык_VALUE; INDEX++) СМС_Терминал.문자(입력[INDEX]);
            СМС_Терминал.문자(10);
        } else if (команда("clear")) СМС_Терминал.지우기();
        else if (команда("test")) төш.시험();
        else if (команда("halt")) {
            СМС_Терминал.язу("HALTED\n");
            мобиль_VALUE.정지();
        } else СМС_Терминал.язу("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void кабул_итү_AND_язу(int VALUE) {
        if (VALUE == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = VALUE == 13;
        if (VALUE == 10 || VALUE == 13) {
            СМС_Терминал.문자(10);
            if (Хәтер_файл_системасы.편집중) Хәтер_файл_системасы.편집줄(입력, озынлык_VALUE, юл_сыешмау);
            else Процесс_VALUE_кертү();
            озынлык_VALUE = 0;
            юл_сыешмау = false;
            СМС_Терминал.язу(Хәтер_файл_системасы.편집중 ? "...> " : "jkoros> ");
        } else if (VALUE == 8 || VALUE == 127) {
            if (озынлык_VALUE > 0) {
                озынлык_VALUE--;
                СМС_Терминал.직렬바이트(8); СМС_Терминал.직렬바이트(32); СМС_Терминал.직렬바이트(8);
                СМС_Терминал.화면문자(8);
            }
        } else if (VALUE >= 32 && VALUE < 127 && озынлык_VALUE < 입력.length) {
            입력[озынлык_VALUE++] = VALUE;
            СМС_Терминал.문자(VALUE);
        } else if (VALUE >= 32 && VALUE < 127) юл_сыешмау = true;
    }

    static void эшләтү() {
        күрсәтү_ярдәм();
        СМС_Терминал.язу("READY\njkoros> ");
        while (true) {
            int VALUE = СМС_Терминал.직렬읽기();
            if (VALUE < 0) VALUE = төймәсар.읽기();
            if (VALUE >= 0) кабул_итү_AND_язу(VALUE);
            else { Челтәр_Стәк.раслау(); мобиль_VALUE.잠시양보(); }
        }
    }
}
