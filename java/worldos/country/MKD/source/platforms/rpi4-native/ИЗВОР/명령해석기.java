// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 командна_линија. Цитат, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] ред = new int[4096], токен_VALUE = new int[4096], 시작점 = new int[32], должина_VALUE = new int[32];
    static int[] 편집내용 = new int[16384], уреди_име = new int[63];
    static int токен_COUNT, уреди_име_должина, мерка;
    static boolean 앞줄;
    static void 원바이트(int VALUE) { табла.직렬쓰기(VALUE); }
    static int 줄읽기() { return ред_Уредник.Читај(); }
    static boolean 나누기(int Големина) {
        int Позиција = 0, 끝 = 0; токен_COUNT = 0;
        while (Позиција < Големина) {
            while (Позиција < Големина && (ред[Позиција] == 32 || ред[Позиција] == 9)) Позиција++;
            if (Позиција == Големина) break;
            if (токен_COUNT == 16) { 단말.Запиши("Команда разложи_VALUE: 인수가 너무 많습니다\n"); return false; }
            시작점[токен_COUNT] = 끝; int Цитат_VALUE = 0;
            while (Позиција < Големина) {
                int VALUE = ред[Позиција++];
                if (Цитат_VALUE == 0 && (VALUE == 32 || VALUE == 9)) break;
                if (VALUE == Цитат_VALUE) { Цитат_VALUE = 0; continue; }
                if (Цитат_VALUE == 0 && (VALUE == 39 || VALUE == 34)) { Цитат_VALUE = VALUE; continue; }
                токен_VALUE[끝++] = VALUE;
            }
            if (Цитат_VALUE != 0) { 단말.Запиши("Команда разложи_VALUE: 따옴표가 닫히지 않았습니다\n"); return false; }
            должина_VALUE[токен_COUNT] = 끝 - 시작점[токен_COUNT]; токен_COUNT++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String Word_СМС) {
        if (INDEX >= токен_COUNT) return false;
        int позиционирање_INDEX=0;
        for (int 순번=0; 순번<Word_СМС.length(); 순번++) {
            int кодна_точка=Word_СМС.charAt(순번);
            if (кодна_точка>=0xd800 && кодна_точка<=0xdbff && 순번+1<Word_СМС.length()) кодна_точка=0x10000+((кодна_точка-0xd800)<<10)+Word_СМС.charAt(++순번)-0xdc00;
            int бајт_COUNT=кодна_точка<128?1:кодна_точка<2048?2:кодна_точка<65536?3:4;
            for (int SEQUENCE_VALUE=бајт_COUNT-1; SEQUENCE_VALUE>=0; SEQUENCE_VALUE--) {
                int VALUE=бајт_COUNT==1?кодна_точка:SEQUENCE_VALUE==бајт_COUNT-1?(бајт_COUNT==2?0xc0:бајт_COUNT==3?0xe0:0xf0)|(кодна_точка>>(6*SEQUENCE_VALUE)):0x80|((кодна_точка>>(6*SEQUENCE_VALUE))&63);
                if (позиционирање_INDEX>=должина_VALUE[INDEX] || токен_VALUE[시작점[INDEX]+позиционирање_INDEX++]!=VALUE) return false;
            }
        }
        return позиционирање_INDEX==должина_VALUE[INDEX];
    }
    static int ПАТЕКА(int INDEX) {
        if (INDEX >= токен_COUNT) return -22;
        int мерка = Меморија_Датотеки.патека_Start(должина_VALUE[INDEX]); if (мерка < 0) return мерка;
        for (int Loop_INDEX = 0; Loop_INDEX < должина_VALUE[INDEX]; Loop_INDEX++) {
            мерка = Меморија_Датотеки.патека_бајт(Loop_INDEX, токен_VALUE[시작점[INDEX] + Loop_INDEX]); if (мерка < 0) return мерка;
        }
        return 0;
    }
    static void ГРЕШКА(int INDEX) { мерка = 1; 단말.Запиши("ГРЕШКА "); 단말.수(INDEX); 단말.문자(10); }
    static void Приказ_VALUE() {
        if (токен_COUNT != 2) { 단말.Запиши("사용법: cat Датотека\n"); return; }
        int мерка = ПАТЕКА(1); if (мерка < 0) { ГРЕШКА(мерка); return; }
        int Датотека = Меморија_Датотеки.Отвори(0); if (Датотека < 0) { ГРЕШКА(Датотека); return; }
        while (true) { int VALUE = Меморија_Датотеки.Читај(Датотека); if (VALUE == 256) break; if (VALUE < 0) { ГРЕШКА(VALUE); break; } 원바이트(VALUE); }
        Меморија_Датотеки.Затвори(Датотека); 단말.문자(10);
    }
    static void уреди_VALUE() {
        if (токен_COUNT != 2) { 단말.Запиши("사용법: edit Датотека\n"); return; }
        int мерка = ПАТЕКА(1); if (мерка < 0) { ГРЕШКА(мерка); return; }
        уреди_име_должина = должина_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < уреди_име_должина; Loop_INDEX++) уреди_име[Loop_INDEX] = токен_VALUE[시작점[1] + Loop_INDEX];
        단말.Запиши("EDIT: Датотека 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Големина = 0;
        while (true) {
            단말.Запиши("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Запиши("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && ред[0] == '.') break;
            if (입력 + 1 > 편집내용.length - Големина) { 단말.Запиши("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) 편집내용[Големина++] = ред[Loop_INDEX];
            편집내용[Големина++] = 10;
        }
        Меморија_Датотеки.патека_Start(уреди_име_должина);
        for (int Loop_INDEX = 0; Loop_INDEX < уреди_име_должина; Loop_INDEX++) Меморија_Датотеки.патека_бајт(Loop_INDEX, уреди_име[Loop_INDEX]);
        int Датотека = Меморија_Датотеки.Отвори(577); if (Датотека < 0) { ГРЕШКА(Датотека); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Големина; Loop_INDEX++) Меморија_Датотеки.Запиши(Датотека, 편집내용[Loop_INDEX]);
        Меморија_Датотеки.Затвори(Датотека); 단말.Запиши("SAVED "); 단말.수(Големина); 단말.Запиши("бајт_VALUE(주기억 Датотека)\n");
    }
    static int хексадецимално_VALUE(int VALUE) {
        if (VALUE >= '0' && VALUE <= '9') return VALUE - '0';
        if (VALUE >= 'a' && VALUE <= 'f') return VALUE - 'a' + 10;
        if (VALUE >= 'A' && VALUE <= 'F') return VALUE - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (токен_COUNT != 2) { 단말.Запиши("사용법: load Датотека | hex Датотека\n"); return; }
        int мерка = ПАТЕКА(1); if (мерка < 0) { ГРЕШКА(мерка); return; }
        if (!넣기) {
            int Датотека = Меморија_Датотеки.Отвори(0); if (Датотека < 0) { ГРЕШКА(Датотека); return; }
            단말.Запиши("HEX BEGIN "); 단말.수(Меморија_Датотеки.Големина(Датотека)); 단말.문자(10);
            int внес_COUNT = 0;
            while (true) {
                int VALUE = Меморија_Датотеки.Читај(Датотека); if (VALUE < 0 || VALUE == 256) break;
                단말.문자("0123456789abcdef".charAt(VALUE >> 4)); 단말.문자("0123456789abcdef".charAt(VALUE & 15));
                if (++внес_COUNT % 32 == 0) 단말.문자(10);
            }
            if (внес_COUNT % 32 != 0) 단말.문자(10);
            Меморија_Датотеки.Затвори(Датотека); 단말.Запиши("HEX END\n"); return;
        }
        уреди_име_должина = должина_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < уреди_име_должина; Loop_INDEX++) уреди_име[Loop_INDEX] = токен_VALUE[시작점[1] + Loop_INDEX];
        단말.Запиши("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Големина = 0;
        while (true) {
            단말.Запиши("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Запиши("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && ред[0] == '.') break;
            int предна_VALUE = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) {
                if (ред[Loop_INDEX] == 32 || ред[Loop_INDEX] == 9) continue;
                int VALUE = хексадецимално_VALUE(ред[Loop_INDEX]);
                if (VALUE < 0 || Големина >= 편집내용.length) { 단말.Запиши("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (предна_VALUE < 0) предна_VALUE = VALUE; else { 편집내용[Големина++] = предна_VALUE * 16 + VALUE; предна_VALUE = -1; }
            }
            if (предна_VALUE >= 0) { 단말.Запиши("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Меморија_Датотеки.патека_Start(уреди_име_должина);
        for (int Loop_INDEX = 0; Loop_INDEX < уреди_име_должина; Loop_INDEX++) Меморија_Датотеки.патека_бајт(Loop_INDEX, уреди_име[Loop_INDEX]);
        int Датотека = Меморија_Датотеки.Отвори(577); if (Датотека < 0) { ГРЕШКА(Датотека); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Големина; Loop_INDEX++) Меморија_Датотеки.Запиши(Датотека, 편집내용[Loop_INDEX]);
        Меморија_Датотеки.Затвори(Датотека); 단말.Запиши("LOADED "); 단말.수(Големина); 단말.Запиши("бајт_VALUE(주기억 Датотека)\n");
    }
    static int Алатки(int INDEX) {
        return алатка_внес(INDEX, 1);
    }
    static int алатка_внес(int INDEX, int Изврши_2) {
        if (токен_COUNT - Изврши_2 > 8) return -22;
        табла.인수준비(токен_COUNT - Изврши_2);
        for (int 첫값 = Изврши_2; 첫값 < токен_COUNT; 첫값++) {
            if (должина_VALUE[첫값] > 255) return -36;
            for (int Loop_INDEX = 0; Loop_INDEX < должина_VALUE[첫값]; Loop_INDEX++) табла.аргумент_бајт(첫값 - Изврши_2, Loop_INDEX, токен_VALUE[시작점[첫값] + Loop_INDEX]);
        }
        return INDEX == -2 ? табла.리눅스파일실행() : INDEX < 0 ? табла.Изврши_корисник_датотека() : табла.изврши_корисник_програма(INDEX);
    }
    static int PYTHON_пакет() {
        if (токен_COUNT > 8) return -22;
        табла.인수준비(токен_COUNT);
        String ПАТЕКА = "/lib/пакет.py";
        // Java 문자열을 셸의 UTF-8 Аргументи 버퍼에 기록한다.
        int позиционирање_INDEX = 0;
        for (int 순번 = 0; 순번 < ПАТЕКА.length(); 순번++) {
            int знак_VALUE = ПАТЕКА.charAt(순번);
            if (знак_VALUE < 128) табла.аргумент_бајт(0, позиционирање_INDEX++, знак_VALUE);
            else { табла.аргумент_бајт(0, позиционирање_INDEX++, 0xe0 | (знак_VALUE >> 12)); табла.аргумент_бајт(0, позиционирање_INDEX++, 0x80 | ((знак_VALUE >> 6) & 63)); табла.аргумент_бајт(0, позиционирање_INDEX++, 0x80 | (знак_VALUE & 63)); }
        }
        for (int 순번 = 1; 순번 < токен_COUNT; 순번++) {
            if (должина_VALUE[순번] > 255) return -36;
            for (int знак_VALUE = 0; знак_VALUE < должина_VALUE[순번]; знак_VALUE++) табла.аргумент_бајт(순번, знак_VALUE, токен_VALUE[시작점[순번] + знак_VALUE]);
        }
        return табла.изврши_корисник_програма(12);
    }
    static int 실행형식() {
        int 처리값 = ПАТЕКА(0); if (처리값 < 0) return 처리값;
        int Датотека = Меморија_Датотеки.Отвори(0); if (Датотека < 0) return Датотека;
        int 첫값 = Меморија_Датотеки.Читај(Датотека), бајт_податоци = Меморија_Датотеки.Читај(Датотека), кодна_точка = Меморија_Датотеки.Читај(Датотека), 뒷값 = Меморија_Датотеки.Читај(Датотека);
        Меморија_Датотеки.Затвори(Датотека);
        if (첫값 == 127 && бајт_податоци == 'E' && кодна_точка == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && бајт_податоци == 'K' && кодна_точка == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String Аргументи) {
        табла.인수준비(1);
        for (int Loop_INDEX = 0; Loop_INDEX < Аргументи.length(); Loop_INDEX++) табла.аргумент_бајт(0, Loop_INDEX, Аргументи.charAt(Loop_INDEX));
        return табла.изврши_корисник_програма(INDEX);
    }
    static void СМС_бајт(int Датотека, int VALUE) { Меморија_Датотеки.Запиши(Датотека, VALUE); }
    static void статичен_датотека(String Име, String Содржина_VALUE) {
        // пакет 파일명은 ASCII. Датотека 내용은 UTF-8로 저장한다.
        Меморија_Датотеки.патека_Start(Име.length());
        for (int Loop_INDEX = 0; Loop_INDEX < Име.length(); Loop_INDEX++) Меморија_Датотеки.патека_бајт(Loop_INDEX, Име.charAt(Loop_INDEX));
        int Датотека = Меморија_Датотеки.Отвори(193); if (Датотека < 0) return;
        for (int Loop_INDEX = 0; Loop_INDEX < Содржина_VALUE.length(); Loop_INDEX++) {
            int кодна_точка = Содржина_VALUE.charAt(Loop_INDEX);
            if (кодна_точка >= 0xd800 && кодна_точка <= 0xdbff && Loop_INDEX + 1 < Содржина_VALUE.length()) кодна_точка = 0x10000 + ((кодна_точка - 0xd800) << 10) + Содржина_VALUE.charAt(++Loop_INDEX) - 0xdc00;
            if (кодна_точка < 128) СМС_бајт(Датотека, кодна_точка);
            else {
                int 수 = кодна_точка < 2048 ? 2 : кодна_точка < 65536 ? 3 : 4;
                СМС_бајт(Датотека, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (кодна_точка >> (6 * (수 - 1))));
                for (int внес_COUNT = 수 - 1; внес_COUNT > 0; внес_COUNT--) СМС_бајт(Датотека, 0x80 | ((кодна_точка >> (6 * (внес_COUNT - 1))) & 63));
            }
        }
        Меморија_Датотеки.Затвори(Датотека);
    }
    static void 한글도움말() {
        단말.Запиши("F9 / Shift+Space: [EN] ↔ [Македонски]\n");
        단말.Запиши("  [MK] keyboard; [EN] ASCII\n");
        단말.Запиши("  @ → „\n");
        단말.Запиши("  F9: EN ↔ Македонски | Ctrl+Shift+V: UTF-8\n");
        단말.Запиши("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Запиши("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Име) {
        int бајт_COUNT = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Име.length(); Loop_INDEX++) { int кодна_точка = Име.charAt(Loop_INDEX); if (кодна_точка >= 0xd800 && кодна_точка <= 0xdfff) return -22; бајт_COUNT += кодна_точка < 128 ? 1 : кодна_точка < 2048 ? 2 : 3; }
        int 처리값 = Меморија_Датотеки.патека_Start(бајт_COUNT); if (처리값 < 0) return 처리값;
        int позиционирање_INDEX = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Име.length(); Loop_INDEX++) {
            int кодна_точка = Име.charAt(Loop_INDEX);
            if (кодна_точка < 128) Меморија_Датотеки.патека_бајт(позиционирање_INDEX++, кодна_точка);
            else if (кодна_точка < 2048) { Меморија_Датотеки.патека_бајт(позиционирање_INDEX++, 0xc0 | (кодна_точка >> 6)); Меморија_Датотеки.патека_бајт(позиционирање_INDEX++, 0x80 | (кодна_точка & 63)); }
            else { Меморија_Датотеки.патека_бајт(позиционирање_INDEX++, 0xe0 | (кодна_точка >> 12)); Меморија_Датотеки.патека_бајт(позиционирање_INDEX++, 0x80 | ((кодна_точка >> 6) & 63)); Меморија_Датотеки.патека_бајт(позиционирање_INDEX++, 0x80 | (кодна_точка & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Име) {
        int 처리값 = 예제경로(Име); if (처리값 < 0) return 처리값;
        처리값 = Меморија_Датотеки.Create_Именик(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Име, String податоци) {
        int 처리값 = 예제경로(Име); if (처리값 < 0) return 처리값;
        int Датотека = Меморија_Датотеки.Отвори(193); if (Датотека == -17) return 0; if (Датотека < 0) return Датотека;
        for (int Loop_INDEX = 0; Loop_INDEX < податоци.length(); Loop_INDEX += 2) {
            처리값 = Меморија_Датотеки.Запиши(Датотека, хексадецимално_VALUE(податоци.charAt(Loop_INDEX)) * 16 + хексадецимално_VALUE(податоци.charAt(Loop_INDEX + 1)));
            if (처리값 < 0) { Меморија_Датотеки.Затвори(Датотека); return 처리값; }
        }
        return Меморија_Датотеки.Затвори(Датотека);
    }
    static void прикажи_помош() {
        систем_алатка.прикажи_помош();
        단말.Запиши("sshd / безбедно_обвивка start|stop|status: SSH :22 (user, 장치별 лозинка_VALUE)\n");
        단말.Запиши("vncd / далечинскo_екран start|stop|status: VNC :5900 (장치별 лозинка_VALUE)\n");
        단말.Запиши("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Запиши("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Запиши("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Запиши("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Запиши("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Запиши("모서리 + 왼쪽 버튼 влечи_VALUE: Терминал Големина измени_VALUE; terminal size: COLUMN_VALUE/ROW_VALUE\n");
        단말.Запиши("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Запиши("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Запиши("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Запиши("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Запиши("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Запиши("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Запиши("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Запиши("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Запиши("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Запиши("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Запиши("pip: MicroPython извор_дрво инсталирај_VALUE; вдоми --network --pip 필요; /lib는 RAM\n");
        단말.Запиши("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Запиши("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Запиши("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Запиши("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void Терминал(boolean 전환여부) {
        if (전환여부 && табла.Терминал(2) != 0) { табла.Терминал(0); 단말.Запиши("TERMINAL CLOSED\n"); }
        else if (табла.Терминал(1) < 0) ГРЕШКА(-19);
        else 단말.Запиши("TERMINAL READY — Македонски terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Команда() {
        if (токен_COUNT == 0) return;
        if (систем_алатка.Изврши_наредба()) return;
        if (같음(0,"sshd") || 같음(0,"безбедно_обвивка") || 같음(0,"vncd") || 같음(0,"далечинскo_екран")) {
            int 종류=같음(0,"vncd")||같음(0,"далечинскo_екран")?1:0;
            int Дејство=같음(1,"start")||같음(1,"Изврши_2")?1:같음(1,"stop")||같음(1,"Стоп")?0:2;
            int статус_VALUE=табла.набљудување(종류,Дејство);
            if(статус_VALUE<0)ГРЕШКА(статус_VALUE);else 단말.Запиши(табла.набљудување(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else прикажи_помош(); }
        else if (같음(0, "info") || 같음(0, "i")) јадро.msinfo32_exe();
        else if (같음(0, "pwd")) { Меморија_Датотеки.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (токен_COUNT == 1) { Меморија_Датотеки.патека_Start(1); 처리값 = Меморија_Датотеки.патека_бајт(0, '/'); } else 처리값 = токен_COUNT == 2 ? ПАТЕКА(1) : -22;
            if (처리값 >= 0) 처리값 = Меморија_Датотеки.измени_Именик(); if (처리값 < 0) ГРЕШКА(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int аргумент_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (токен_COUNT == аргумент_INDEX) { Меморија_Датотеки.патека_Start(1); 처리값 = Меморија_Датотеки.патека_бајт(0, '.'); } else 처리값 = токен_COUNT == аргумент_INDEX + 1 ? ПАТЕКА(аргумент_INDEX) : -22;
            if (처리값 >= 0) 처리값 = Меморија_Датотеки.경로목록(); if (처리값 < 0) ГРЕШКА(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) обвивка_Алатки.датотека_Задача(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) обвивка_Алатки.копирај_VALUE(같음(0, "mv"));
        else if (같음(0, "cat")) обвивка_Алатки.Приказ_VALUE();
        else if (같음(0, "wc")) обвивка_Алатки.세기();
        else if (같음(0, "grep")) обвивка_Алатки.FIND_внес();
        else if (같음(0, "head") || 같음(0, "tail")) обвивка_Алатки.머리(같음(0, "tail"));
        else if (같음(0, "tee")) обвивка_Алатки.함께쓰기();
        else if (같음(0, "env")) обвивка_синтакса.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (токен_COUNT == 1) обвивка_синтакса.환경보기();
            for (int Loop_INDEX = 1; Loop_INDEX < токен_COUNT; Loop_INDEX++) { int 처리값 = обвивка_синтакса.환경설정(Loop_INDEX, 같음(0, "unset")); if (처리값 != 0) { мерка = 처리값; 단말.Запиши("Команда разложи_VALUE: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) обвивка_синтакса.Изврши_датотека();
        else if (같음(0, "true")) мерка = 0;
        else if (같음(0, "false")) мерка = 1;
        else if (같음(0, "history")) ред_Уредник.прикажи_LOG();
        else if (같음(0, "exit")) {
            if (обвивка_синтакса.깊이 > 0) { мерка = токен_COUNT == 1 ? обвивка_синтакса.статус_VALUE : обвивка_Алатки.цифра_VALUE(1); if (мерка < 0 || мерка > 255) мерка = 2; обвивка_синтакса.скрипта_крај = true; }
            else if (табла.Терминал(2) != 0) Терминал(true);
            else 단말.Запиши("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) уреди_VALUE();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (токен_COUNT < 2) { мерка = 2; 단말.Запиши("사용법: rm Датотека...\n"); }
            for (int Loop_INDEX = 1; Loop_INDEX < токен_COUNT; Loop_INDEX++) { int 처리값 = ПАТЕКА(Loop_INDEX); if (처리값 == 0) 처리값 = Меморија_Датотеки.избриши_внес(); if (처리값 < 0) ГРЕШКА(처리값); }
        }
        else if (같음(0, "echo")) {
            int Start_позиционирање = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = Start_позиционирање; 첫값 < токен_COUNT; 첫값++) { if (첫값 > Start_позиционирање) 단말.문자(32); for (int Loop_INDEX = 0; Loop_INDEX < должина_VALUE[첫값]; Loop_INDEX++) табла.직렬쓰기(токен_VALUE[시작점[첫값] + Loop_INDEX]); }
            if (Start_позиционирање == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Запиши("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_пакет() : Алатки(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); мерка = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !обвивка_синтакса.연결중) { 단말.Запиши("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Алатки(13); мерка = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Алатки(15); мерка = 처리값 < 0 ? 126 : 처리값; if (!обвивка_синтакса.연결중) { 단말.Запиши("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Алатки(16); мерка = 처리값 < 0 ? 126 : 처리값; if (!обвивка_синтакса.연결중) { 단말.Запиши("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Големина = табла.Терминал(13); 단말.Запиши("TERMINAL SIZE "); 단말.수(Големина & 65535); 단말.문자('x'); 단말.수(Големина >>> 16); 단말.문자(10); }
            else Терминал(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { табла.Терминал(9); десктоп.Изврши_наредба(); }
        else if (같음(0, "c")) јадро.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) јадро.작업시험();
        else if (같음(0, "g")) јадро.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) јадро.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = табла.изврши_корисник_програма(0); if (처리값 == 0) 단말.Запиши("ELF DEMO PASS\n"); else ГРЕШКА(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? алатка_внес(-2, 2) : Алатки(-1); мерка = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !обвивка_синтакса.연결중) { 단말.Запиши("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) јадро.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = табла.датотека_пренос_услуга(1); if (처리값 < 0) ГРЕШКА(처리값); else { 단말.Запиши("FTP listening "); систем_алатка.запиши_адреса(табла.Мрежа_статус(0,0)); 단말.Запиши(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { табла.датотека_пренос_услуга(0); 단말.Запиши("FTP stopped\n"); }
            else 단말.Запиши(табла.датотека_пренос_услуга(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { пакет.Подготви(); 단말.Запиши("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int јазик = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (токен_COUNT != 2 || јазик < 0) 단말.Запиши("example java|c|python: 출력, Датотека, 네트워크, 그래픽, Java Swing прозорец 예제\n");
            else { int 처리값 = 예제꾸러미.инсталирај_VALUE(јазик); if (처리값 < 0) { ГРЕШКА(처리값); if (처리값 == -28) 단말.Запиши("RAM full: remove unused files, then retry example\n"); } else 단말.Запиши("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int формат_VALUE = 실행형식();
            if (формат_VALUE == 1 || формат_VALUE == 2) {
                int 처리값 = алатка_внес(формат_VALUE == 1 ? -1 : 14, 0); мерка = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !обвивка_синтакса.연결중) { 단말.Запиши("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (формат_VALUE == 0) { мерка = 126; 단말.Запиши("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { мерка = 127; 단말.Запиши("Unknown command. help: commands\n"); }
        }
    }
    public static void Изврши_наредба() {
        пакет.Подготви();
        for (int јазик = 0; јазик < 3; јазик++) { int 처리값 = 예제꾸러미.инсталирај_VALUE(јазик); if (처리값 < 0) ГРЕШКА(처리값); }
        прикажи_помош();
        while (true) {
            прозорец_сесија.Процес_VALUE_внес(); if (прозорец_сесија.재개()) continue;
            if (!прозорец_сесија.이어읽기) 단말.Запиши("jkoros-native> "); ред_Уредник.командна_линија = true; табла.далечинскo_почекај(1); int Големина = 줄읽기(); табла.далечинскo_почекај(0); ред_Уредник.командна_линија = false;
            if (Големина == -3) continue;
            if (Големина == -2) 단말.Запиши("Команда разложи_VALUE: 명령줄이 너무 깁니다\n");
            if (Големина >= 0) { обвивка_синтакса.скрипта_крај = false; обвивка_синтакса.Изврши_наредба(ред, 0, Големина, 0); } else обвивка_синтакса.статус_VALUE = 130;
            табла.крај_далечинскo_наредба(обвивка_синтакса.статус_VALUE);
            ред_Уредник.Големина = ред_Уредник.покажувач_VALUE = ред_Уредник.Start_прозорец = 0;
        }
    }
}
