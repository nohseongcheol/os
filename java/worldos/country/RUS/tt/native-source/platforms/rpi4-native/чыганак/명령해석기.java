// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 команда_юлы. Куштырнаклар, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] юл = new int[4096], токен_VALUE = new int[4096], 시작점 = new int[32], озынлык_VALUE = new int[32];
    static int[] 편집내용 = new int[16384], төзәтү_исем = new int[63];
    static int токен_COUNT, төзәтү_исем_озынлык, үлчәм;
    static boolean 앞줄;
    static void 원바이트(int VALUE) { такта.직렬쓰기(VALUE); }
    static int 줄읽기() { return юл_Редактор.읽기(); }
    static boolean 나누기(int үлчәмен_үзгәртү) {
        int урнаштыру = 0, 끝 = 0; токен_COUNT = 0;
        while (урнаштыру < үлчәмен_үзгәртү) {
            while (урнаштыру < үлчәмен_үзгәртү && (юл[урнаштыру] == 32 || юл[урнаштыру] == 9)) урнаштыру++;
            if (урнаштыру == үлчәмен_үзгәртү) break;
            if (токен_COUNT == 16) { 단말.язу("команда бүлү_VALUE: 인수가 너무 많습니다\n"); return false; }
            시작점[токен_COUNT] = 끝; int Куштырнаклар_VALUE = 0;
            while (урнаштыру < үлчәмен_үзгәртү) {
                int VALUE = юл[урнаштыру++];
                if (Куштырнаклар_VALUE == 0 && (VALUE == 32 || VALUE == 9)) break;
                if (VALUE == Куштырнаклар_VALUE) { Куштырнаклар_VALUE = 0; continue; }
                if (Куштырнаклар_VALUE == 0 && (VALUE == 39 || VALUE == 34)) { Куштырнаклар_VALUE = VALUE; continue; }
                токен_VALUE[끝++] = VALUE;
            }
            if (Куштырнаклар_VALUE != 0) { 단말.язу("команда бүлү_VALUE: 따옴표가 닫히지 않았습니다\n"); return false; }
            озынлык_VALUE[токен_COUNT] = 끝 - 시작점[токен_COUNT]; токен_COUNT++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String Word_СМС) {
        if (INDEX >= токен_COUNT) return false;
        int урнаштыру_INDEX=0;
        for (int 순번=0; 순번<Word_СМС.length(); 순번++) {
            int символ_коды=Word_СМС.charAt(순번);
            if (символ_коды>=0xd800 && символ_коды<=0xdbff && 순번+1<Word_СМС.length()) символ_коды=0x10000+((символ_коды-0xd800)<<10)+Word_СМС.charAt(++순번)-0xdc00;
            int байт_COUNT=символ_коды<128?1:символ_коды<2048?2:символ_коды<65536?3:4;
            for (int SEQUENCE_VALUE=байт_COUNT-1; SEQUENCE_VALUE>=0; SEQUENCE_VALUE--) {
                int VALUE=байт_COUNT==1?символ_коды:SEQUENCE_VALUE==байт_COUNT-1?(байт_COUNT==2?0xc0:байт_COUNT==3?0xe0:0xf0)|(символ_коды>>(6*SEQUENCE_VALUE)):0x80|((символ_коды>>(6*SEQUENCE_VALUE))&63);
                if (урнаштыру_INDEX>=озынлык_VALUE[INDEX] || токен_VALUE[시작점[INDEX]+урнаштыру_INDEX++]!=VALUE) return false;
            }
        }
        return урнаштыру_INDEX==озынлык_VALUE[INDEX];
    }
    static int Yul(int INDEX) {
        if (INDEX >= токен_COUNT) return -22;
        int үлчәм = Хәтер_Файллар.юл_Start(озынлык_VALUE[INDEX]); if (үлчәм < 0) return үлчәм;
        for (int Loop_INDEX = 0; Loop_INDEX < озынлык_VALUE[INDEX]; Loop_INDEX++) {
            үлчәм = Хәтер_Файллар.юл_байт(Loop_INDEX, токен_VALUE[시작점[INDEX] + Loop_INDEX]); if (үлчәм < 0) return үлчәм;
        }
        return 0;
    }
    static void Хата(int INDEX) { үлчәм = 1; 단말.язу("Хата "); 단말.수(INDEX); 단말.문자(10); }
    static void карау_VALUE() {
        if (токен_COUNT != 2) { 단말.язу("사용법: cat Birem\n"); return; }
        int үлчәм = Yul(1); if (үлчәм < 0) { Хата(үлчәм); return; }
        int Birem = Хәтер_Файллар.ачу(0); if (Birem < 0) { Хата(Birem); return; }
        while (true) { int VALUE = Хәтер_Файллар.읽기(Birem); if (VALUE == 256) break; if (VALUE < 0) { Хата(VALUE); break; } 원바이트(VALUE); }
        Хәтер_Файллар.Yap(Birem); 단말.문자(10);
    }
    static void төзәтү_VALUE() {
        if (токен_COUNT != 2) { 단말.язу("사용법: edit Birem\n"); return; }
        int үлчәм = Yul(1); if (үлчәм < 0) { Хата(үлчәм); return; }
        төзәтү_исем_озынлык = озынлык_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < төзәтү_исем_озынлык; Loop_INDEX++) төзәтү_исем[Loop_INDEX] = токен_VALUE[시작점[1] + Loop_INDEX];
        단말.язу("EDIT: Birem 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int үлчәмен_үзгәртү = 0;
        while (true) {
            단말.язу("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.язу("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && юл[0] == '.') break;
            if (입력 + 1 > 편집내용.length - үлчәмен_үзгәртү) { 단말.язу("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) 편집내용[үлчәмен_үзгәртү++] = юл[Loop_INDEX];
            편집내용[үлчәмен_үзгәртү++] = 10;
        }
        Хәтер_Файллар.юл_Start(төзәтү_исем_озынлык);
        for (int Loop_INDEX = 0; Loop_INDEX < төзәтү_исем_озынлык; Loop_INDEX++) Хәтер_Файллар.юл_байт(Loop_INDEX, төзәтү_исем[Loop_INDEX]);
        int Birem = Хәтер_Файллар.ачу(577); if (Birem < 0) { Хата(Birem); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < үлчәмен_үзгәртү; Loop_INDEX++) Хәтер_Файллар.язу(Birem, 편집내용[Loop_INDEX]);
        Хәтер_Файллар.Yap(Birem); 단말.язу("SAVED "); 단말.수(үлчәмен_үзгәртү); 단말.язу("байт_VALUE(주기억 Birem)\n");
    }
    static int уналтынчы_VALUE(int VALUE) {
        if (VALUE >= '0' && VALUE <= '9') return VALUE - '0';
        if (VALUE >= 'a' && VALUE <= 'f') return VALUE - 'a' + 10;
        if (VALUE >= 'A' && VALUE <= 'F') return VALUE - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (токен_COUNT != 2) { 단말.язу("사용법: load Birem | hex Birem\n"); return; }
        int үлчәм = Yul(1); if (үлчәм < 0) { Хата(үлчәм); return; }
        if (!넣기) {
            int Birem = Хәтер_Файллар.ачу(0); if (Birem < 0) { Хата(Birem); return; }
            단말.язу("HEX BEGIN "); 단말.수(Хәтер_Файллар.үлчәмен_үзгәртү(Birem)); 단말.문자(10);
            int кертү_COUNT = 0;
            while (true) {
                int VALUE = Хәтер_Файллар.읽기(Birem); if (VALUE < 0 || VALUE == 256) break;
                단말.문자("0123456789abcdef".charAt(VALUE >> 4)); 단말.문자("0123456789abcdef".charAt(VALUE & 15));
                if (++кертү_COUNT % 32 == 0) 단말.문자(10);
            }
            if (кертү_COUNT % 32 != 0) 단말.문자(10);
            Хәтер_Файллар.Yap(Birem); 단말.язу("HEX END\n"); return;
        }
        төзәтү_исем_озынлык = озынлык_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < төзәтү_исем_озынлык; Loop_INDEX++) төзәтү_исем[Loop_INDEX] = токен_VALUE[시작점[1] + Loop_INDEX];
        단말.язу("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int үлчәмен_үзгәртү = 0;
        while (true) {
            단말.язу("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.язу("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && юл[0] == '.') break;
            int 앞 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) {
                if (юл[Loop_INDEX] == 32 || юл[Loop_INDEX] == 9) continue;
                int VALUE = уналтынчы_VALUE(юл[Loop_INDEX]);
                if (VALUE < 0 || үлчәмен_үзгәртү >= 편집내용.length) { 단말.язу("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (앞 < 0) 앞 = VALUE; else { 편집내용[үлчәмен_үзгәртү++] = 앞 * 16 + VALUE; 앞 = -1; }
            }
            if (앞 >= 0) { 단말.язу("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Хәтер_Файллар.юл_Start(төзәтү_исем_озынлык);
        for (int Loop_INDEX = 0; Loop_INDEX < төзәтү_исем_озынлык; Loop_INDEX++) Хәтер_Файллар.юл_байт(Loop_INDEX, төзәтү_исем[Loop_INDEX]);
        int Birem = Хәтер_Файллар.ачу(577); if (Birem < 0) { Хата(Birem); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < үлчәмен_үзгәртү; Loop_INDEX++) Хәтер_Файллар.язу(Birem, 편집내용[Loop_INDEX]);
        Хәтер_Файллар.Yap(Birem); 단말.язу("LOADED "); 단말.수(үлчәмен_үзгәртү); 단말.язу("байт_VALUE(주기억 Birem)\n");
    }
    static int Кораллар(int INDEX) {
        return чара_кертү(INDEX, 1);
    }
    static int чара_кертү(int INDEX, int эшләтү) {
        if (токен_COUNT - эшләтү > 8) return -22;
        такта.인수준비(токен_COUNT - эшләтү);
        for (int 첫값 = эшләтү; 첫값 < токен_COUNT; 첫값++) {
            if (озынлык_VALUE[첫값] > 255) return -36;
            for (int Loop_INDEX = 0; Loop_INDEX < озынлык_VALUE[첫값]; Loop_INDEX++) такта.аргумент_байт(첫값 - эшләтү, Loop_INDEX, токен_VALUE[시작점[첫값] + Loop_INDEX]);
        }
        return INDEX == -2 ? такта.리눅스파일실행() : INDEX < 0 ? такта.үтәргә_кулланучы_файл() : такта.эшләтү_кулланучы_кушымта(INDEX);
    }
    static int PYTHON_пакет() {
        if (токен_COUNT > 8) return -22;
        такта.인수준비(токен_COUNT);
        String Yul = "/lib/пакет.py";
        // Java 문자열을 셸의 UTF-8 인수 버퍼에 기록한다.
        int урнаштыру_INDEX = 0;
        for (int 순번 = 0; 순번 < Yul.length(); 순번++) {
            int символ_VALUE_068c2631 = Yul.charAt(순번);
            if (символ_VALUE_068c2631 < 128) такта.аргумент_байт(0, урнаштыру_INDEX++, символ_VALUE_068c2631);
            else { такта.аргумент_байт(0, урнаштыру_INDEX++, 0xe0 | (символ_VALUE_068c2631 >> 12)); такта.аргумент_байт(0, урнаштыру_INDEX++, 0x80 | ((символ_VALUE_068c2631 >> 6) & 63)); такта.аргумент_байт(0, урнаштыру_INDEX++, 0x80 | (символ_VALUE_068c2631 & 63)); }
        }
        for (int 순번 = 1; 순번 < токен_COUNT; 순번++) {
            if (озынлык_VALUE[순번] > 255) return -36;
            for (int символ_VALUE_068c2631 = 0; символ_VALUE_068c2631 < озынлык_VALUE[순번]; символ_VALUE_068c2631++) такта.аргумент_байт(순번, символ_VALUE_068c2631, токен_VALUE[시작점[순번] + символ_VALUE_068c2631]);
        }
        return такта.эшләтү_кулланучы_кушымта(12);
    }
    static int 실행형식() {
        int 처리값 = Yul(0); if (처리값 < 0) return 처리값;
        int Birem = Хәтер_Файллар.ачу(0); if (Birem < 0) return Birem;
        int 첫값 = Хәтер_Файллар.읽기(Birem), байт_мәгълүмат = Хәтер_Файллар.읽기(Birem), символ_коды = Хәтер_Файллар.읽기(Birem), 뒷값 = Хәтер_Файллар.읽기(Birem);
        Хәтер_Файллар.Yap(Birem);
        if (첫값 == 127 && байт_мәгълүмат == 'E' && символ_коды == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && байт_мәгълүмат == 'K' && символ_коды == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String 인수) {
        такта.인수준비(1);
        for (int Loop_INDEX = 0; Loop_INDEX < 인수.length(); Loop_INDEX++) такта.аргумент_байт(0, Loop_INDEX, 인수.charAt(Loop_INDEX));
        return такта.эшләтү_кулланучы_кушымта(INDEX);
    }
    static void СМС_байт(int Birem, int VALUE) { Хәтер_Файллар.язу(Birem, VALUE); }
    static void статик_файл(String исем, String Эчтәлек_VALUE) {
        // пакет 파일명은 ASCII. Birem 내용은 UTF-8로 저장한다.
        Хәтер_Файллар.юл_Start(исем.length());
        for (int Loop_INDEX = 0; Loop_INDEX < исем.length(); Loop_INDEX++) Хәтер_Файллар.юл_байт(Loop_INDEX, исем.charAt(Loop_INDEX));
        int Birem = Хәтер_Файллар.ачу(193); if (Birem < 0) return;
        for (int Loop_INDEX = 0; Loop_INDEX < Эчтәлек_VALUE.length(); Loop_INDEX++) {
            int символ_коды = Эчтәлек_VALUE.charAt(Loop_INDEX);
            if (символ_коды >= 0xd800 && символ_коды <= 0xdbff && Loop_INDEX + 1 < Эчтәлек_VALUE.length()) символ_коды = 0x10000 + ((символ_коды - 0xd800) << 10) + Эчтәлек_VALUE.charAt(++Loop_INDEX) - 0xdc00;
            if (символ_коды < 128) СМС_байт(Birem, символ_коды);
            else {
                int 수 = символ_коды < 2048 ? 2 : символ_коды < 65536 ? 3 : 4;
                СМС_байт(Birem, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (символ_коды >> (6 * (수 - 1))));
                for (int кертү_COUNT = 수 - 1; кертү_COUNT > 0; кертү_COUNT--) СМС_байт(Birem, 0x80 | ((символ_коды >> (6 * (кертү_COUNT - 1))) & 63));
            }
        }
        Хәтер_Файллар.Yap(Birem);
    }
    static void 한글도움말() {
        단말.язу("F9 / Shift+Space: [EN] ↔ [tt]\n");
        단말.язу("  [TT] keyboard; [EN] ASCII\n");
        단말.язу("  a → a\n");
        단말.язу("  F9: EN ↔ tt | Ctrl+Shift+V: UTF-8\n");
        단말.язу("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.язу("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String исем) {
        int байт_COUNT = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < исем.length(); Loop_INDEX++) { int символ_коды = исем.charAt(Loop_INDEX); if (символ_коды >= 0xd800 && символ_коды <= 0xdfff) return -22; байт_COUNT += символ_коды < 128 ? 1 : символ_коды < 2048 ? 2 : 3; }
        int 처리값 = Хәтер_Файллар.юл_Start(байт_COUNT); if (처리값 < 0) return 처리값;
        int урнаштыру_INDEX = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < исем.length(); Loop_INDEX++) {
            int символ_коды = исем.charAt(Loop_INDEX);
            if (символ_коды < 128) Хәтер_Файллар.юл_байт(урнаштыру_INDEX++, символ_коды);
            else if (символ_коды < 2048) { Хәтер_Файллар.юл_байт(урнаштыру_INDEX++, 0xc0 | (символ_коды >> 6)); Хәтер_Файллар.юл_байт(урнаштыру_INDEX++, 0x80 | (символ_коды & 63)); }
            else { Хәтер_Файллар.юл_байт(урнаштыру_INDEX++, 0xe0 | (символ_коды >> 12)); Хәтер_Файллар.юл_байт(урнаштыру_INDEX++, 0x80 | ((символ_коды >> 6) & 63)); Хәтер_Файллар.юл_байт(урнаштыру_INDEX++, 0x80 | (символ_коды & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String исем) {
        int 처리값 = 예제경로(исем); if (처리값 < 0) return 처리값;
        처리값 = Хәтер_Файллар.Төзү_каталог(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String исем, String мәгълүмат) {
        int 처리값 = 예제경로(исем); if (처리값 < 0) return 처리값;
        int Birem = Хәтер_Файллар.ачу(193); if (Birem == -17) return 0; if (Birem < 0) return Birem;
        for (int Loop_INDEX = 0; Loop_INDEX < мәгълүмат.length(); Loop_INDEX += 2) {
            처리값 = Хәтер_Файллар.язу(Birem, уналтынчы_VALUE(мәгълүмат.charAt(Loop_INDEX)) * 16 + уналтынчы_VALUE(мәгълүмат.charAt(Loop_INDEX + 1)));
            if (처리값 < 0) { Хәтер_Файллар.Yap(Birem); return 처리값; }
        }
        return Хәтер_Файллар.Yap(Birem);
    }
    static void күрсәтү_ярдәм() {
        система_чара.күрсәтү_ярдәм();
        단말.язу("sshd / имин_тышча start|stop|status: SSH :22 (user, 장치별 серсүз_VALUE)\n");
        단말.язу("vncd / читтәге_дисплей start|stop|status: VNC :5900 (장치별 серсүз_VALUE)\n");
        단말.язу("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.язу("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.язу("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.язу("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.язу("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.язу("모서리 + 왼쪽 버튼 сөйрәү_VALUE: Терминал үлчәмен_үзгәртү үзгәртү_VALUE; terminal size: COLUMN_VALUE/юл_VALUE_fc48bc81\n");
        단말.язу("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.язу("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.язу("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.язу("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.язу("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.язу("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.язу("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.язу("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.язу("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.язу("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.язу("pip: MicroPython чыганак_агач урнаштыру_VALUE_6a28baa5; хост --network --pip 필요; /lib는 RAM\n");
        단말.язу("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.язу("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.язу("/example/java /example/c /example/python: examples ready at boot\n");
        단말.язу("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void Терминал(boolean 전환여부) {
        if (전환여부 && такта.Терминал(2) != 0) { такта.Терминал(0); 단말.язу("TERMINAL CLOSED\n"); }
        else if (такта.Терминал(1) < 0) Хата(-19);
        else 단말.язу("TERMINAL READY — tt terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void команда() {
        if (токен_COUNT == 0) return;
        if (система_чара.үтәргә_команда()) return;
        if (같음(0,"sshd") || 같음(0,"имин_тышча") || 같음(0,"vncd") || 같음(0,"читтәге_дисплей")) {
            int 종류=같음(0,"vncd")||같음(0,"читтәге_дисплей")?1:0;
            int Гамәл=같음(1,"start")||같음(1,"эшләтү")?1:같음(1,"stop")||같음(1,"туктату")?0:2;
            int халәт_VALUE=такта.читтән_идарә(종류,Гамәл);
            if(халәт_VALUE<0)Хата(халәт_VALUE);else 단말.язу(такта.читтән_идарә(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else күрсәтү_ярдәм(); }
        else if (같음(0, "info") || 같음(0, "i")) төш.msinfo32_exe();
        else if (같음(0, "pwd")) { Хәтер_Файллар.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (токен_COUNT == 1) { Хәтер_Файллар.юл_Start(1); 처리값 = Хәтер_Файллар.юл_байт(0, '/'); } else 처리값 = токен_COUNT == 2 ? Yul(1) : -22;
            if (처리값 >= 0) 처리값 = Хәтер_Файллар.үзгәртү_каталог(); if (처리값 < 0) Хата(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int аргумент_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (токен_COUNT == аргумент_INDEX) { Хәтер_Файллар.юл_Start(1); 처리값 = Хәтер_Файллар.юл_байт(0, '.'); } else 처리값 = токен_COUNT == аргумент_INDEX + 1 ? Yul(аргумент_INDEX) : -22;
            if (처리값 >= 0) 처리값 = Хәтер_Файллар.경로목록(); if (처리값 < 0) Хата(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) тышча_Кораллар.файл_бирем(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) тышча_Кораллар.экземпляр_VALUE(같음(0, "mv"));
        else if (같음(0, "cat")) тышча_Кораллар.карау_VALUE();
        else if (같음(0, "wc")) тышча_Кораллар.세기();
        else if (같음(0, "grep")) тышча_Кораллар.FIND_кертү();
        else if (같음(0, "head") || 같음(0, "tail")) тышча_Кораллар.머리(같음(0, "tail"));
        else if (같음(0, "tee")) тышча_Кораллар.함께쓰기();
        else if (같음(0, "env")) тышча_синтаксис.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (токен_COUNT == 1) тышча_синтаксис.환경보기();
            for (int Loop_INDEX = 1; Loop_INDEX < токен_COUNT; Loop_INDEX++) { int 처리값 = тышча_синтаксис.환경설정(Loop_INDEX, 같음(0, "unset")); if (처리값 != 0) { үлчәм = 처리값; 단말.язу("команда бүлү_VALUE: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) тышча_синтаксис.үтәргә_файл();
        else if (같음(0, "true")) үлчәм = 0;
        else if (같음(0, "false")) үлчәм = 1;
        else if (같음(0, "history")) юл_Редактор.күрсәтү_LOG();
        else if (같음(0, "exit")) {
            if (тышча_синтаксис.깊이 > 0) { үлчәм = токен_COUNT == 1 ? тышча_синтаксис.халәт_VALUE : тышча_Кораллар.сан_VALUE(1); if (үлчәм < 0 || үлчәм > 255) үлчәм = 2; тышча_синтаксис.сценарий_тәмамлау = true; }
            else if (такта.Терминал(2) != 0) Терминал(true);
            else 단말.язу("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) төзәтү_VALUE();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (токен_COUNT < 2) { үлчәм = 2; 단말.язу("사용법: rm Birem...\n"); }
            for (int Loop_INDEX = 1; Loop_INDEX < токен_COUNT; Loop_INDEX++) { int 처리값 = Yul(Loop_INDEX); if (처리값 == 0) 처리값 = Хәтер_Файллар.지우기(); if (처리값 < 0) Хата(처리값); }
        }
        else if (같음(0, "echo")) {
            int Start_урнаштыру = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = Start_урнаштыру; 첫값 < токен_COUNT; 첫값++) { if (첫값 > Start_урнаштыру) 단말.문자(32); for (int Loop_INDEX = 0; Loop_INDEX < озынлык_VALUE[첫값]; Loop_INDEX++) такта.직렬쓰기(токен_VALUE[시작점[첫값] + Loop_INDEX]); }
            if (Start_урнаштыру == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.язу("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_пакет() : Кораллар(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); үлчәм = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !тышча_синтаксис.연결중) { 단말.язу("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Кораллар(13); үлчәм = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Кораллар(15); үлчәм = 처리값 < 0 ? 126 : 처리값; if (!тышча_синтаксис.연결중) { 단말.язу("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Кораллар(16); үлчәм = 처리값 < 0 ? 126 : 처리값; if (!тышча_синтаксис.연결중) { 단말.язу("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int үлчәмен_үзгәртү = такта.Терминал(13); 단말.язу("TERMINAL SIZE "); 단말.수(үлчәмен_үзгәртү & 65535); 단말.문자('x'); 단말.수(үлчәмен_үзгәртү >>> 16); 단말.문자(10); }
            else Терминал(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { такта.Терминал(9); классик.үтәргә_команда(); }
        else if (같음(0, "c")) төш.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) төш.작업시험();
        else if (같음(0, "g")) төш.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) төш.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = такта.эшләтү_кулланучы_кушымта(0); if (처리값 == 0) 단말.язу("ELF DEMO PASS\n"); else Хата(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? чара_кертү(-2, 2) : Кораллар(-1); үлчәм = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !тышча_синтаксис.연결중) { 단말.язу("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) төш.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = такта.файл_күчерү_хезмәт(1); if (처리값 < 0) Хата(처리값); else { 단말.язу("FTP listening "); система_чара.язу_адрес(такта.Челтәр_халәт(0,0)); 단말.язу(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { такта.файл_күчерү_хезмәт(0); 단말.язу("FTP stopped\n"); }
            else 단말.язу(такта.файл_күчерү_хезмәт(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { пакет.Әзерләү(); 단말.язу("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int тел = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (токен_COUNT != 2 || тел < 0) 단말.язу("example java|c|python: 출력, Birem, 네트워크, 그래픽, Java Swing тәрәз 예제\n");
            else { int 처리값 = 예제꾸러미.урнаштыру_VALUE_6a28baa5(тел); if (처리값 < 0) { Хата(처리값); if (처리값 == -28) 단말.язу("RAM full: remove unused files, then retry example\n"); } else 단말.язу("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int формат_VALUE = 실행형식();
            if (формат_VALUE == 1 || формат_VALUE == 2) {
                int 처리값 = чара_кертү(формат_VALUE == 1 ? -1 : 14, 0); үлчәм = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !тышча_синтаксис.연결중) { 단말.язу("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (формат_VALUE == 0) { үлчәм = 126; 단말.язу("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { үлчәм = 127; 단말.язу("Unknown command. help: commands\n"); }
        }
    }
    public static void үтәргә_команда() {
        пакет.Әзерләү();
        for (int тел = 0; тел < 3; тел++) { int 처리값 = 예제꾸러미.урнаштыру_VALUE_6a28baa5(тел); if (처리값 < 0) Хата(처리값); }
        күрсәтү_ярдәм();
        while (true) {
            тәрәз_сеанс.Процесс_VALUE_кертү(); if (тәрәз_сеанс.재개()) continue;
            if (!тәрәз_сеанс.이어읽기) 단말.язу("jkoros-native> "); юл_Редактор.команда_юлы = true; такта.원격대기(1); int үлчәмен_үзгәртү = 줄읽기(); такта.원격대기(0); юл_Редактор.команда_юлы = false;
            if (үлчәмен_үзгәртү == -3) continue;
            if (үлчәмен_үзгәртү == -2) 단말.язу("команда бүлү_VALUE: 명령줄이 너무 깁니다\n");
            if (үлчәмен_үзгәртү >= 0) { тышча_синтаксис.сценарий_тәмамлау = false; тышча_синтаксис.үтәргә_команда(юл, 0, үлчәмен_үзгәртү, 0); } else тышча_синтаксис.халәт_VALUE = 130;
            такта.тәмамлау_читтәге_команда(тышча_синтаксис.халәт_VALUE);
            юл_Редактор.үлчәмен_үзгәртү = юл_Редактор.курсор_VALUE = юл_Редактор.Start_тәрәз = 0;
        }
    }
}
