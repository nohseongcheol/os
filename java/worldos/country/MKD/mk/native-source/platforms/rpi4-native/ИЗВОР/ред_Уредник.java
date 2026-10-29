// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 бајт_VALUE 경계를 지키는 삽입/삭제, 방향키, Команда LOG_ред, Tab 완성. */
public final class ред_Уредник {
    static boolean командна_линија;
    static int[] LOG_ред = new int[16 * 1024], LOG_должина = new int[16], Store_VALUE = new int[4096], 후보 = new int[64];
    static int LOG_COUNT, LOG_ред_крај, SEARCH_VALUE, 저장길이, Големина, покажувач_VALUE, 후보수, 후보길이, Start_прозорец;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd безбедно_обвивка далечинскo_екран run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String внес_Список, int Start_позиционирање, int крај_позиционирање, int 입력길이) {
        int бајт_COUNT=0;
        for(int позиционирање_INDEX=Start_позиционирање;позиционирање_INDEX<крај_позиционирање;позиционирање_INDEX++) {
            int кодна_точка=внес_Список.charAt(позиционирање_INDEX);
            if(кодна_точка>=0xd800 && кодна_точка<=0xdbff && позиционирање_INDEX+1<крај_позиционирање)кодна_точка=0x10000+((кодна_точка-0xd800)<<10)+внес_Список.charAt(++позиционирање_INDEX)-0xdc00;
            int 수=кодна_точка<128?1:кодна_точка<2048?2:кодна_точка<65536?3:4;
            if(бајт_COUNT+수>62)return;
            for(int SEQUENCE_VALUE=수-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--)명령후보[бајт_COUNT++]=수==1?кодна_точка:SEQUENCE_VALUE==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(кодна_точка>>(6*SEQUENCE_VALUE)):0x80|((кодна_точка>>(6*SEQUENCE_VALUE))&63);
        }
        if(бајт_COUNT<입력길이)return;
        for(int позиционирање_INDEX=0;позиционирање_INDEX<입력길이;позиционирање_INDEX++)if(명령후보[позиционирање_INDEX]!=명령해석기.ред[позиционирање_INDEX])return;
        후보수++;후보길이=бајт_COUNT+1;
        for(int позиционирање_INDEX=0;позиционирање_INDEX<бајт_COUNT;позиционирање_INDEX++)후보[позиционирање_INDEX]=명령후보[позиционирање_INDEX];후보[бајт_COUNT]=' ';
    }
    static int предна_VALUE(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.ред[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int Назад_VALUE(int 읽는자리) { if (읽는자리 < Големина) { 읽는자리++; while (읽는자리 < Големина && (명령해석기.ред[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int Start_позиционирање, int одредиште_VALUE_INDEX) {
        int 글칸수 = 0;
        for (int Loop_INDEX = Start_позиционирање; Loop_INDEX < одредиште_VALUE_INDEX; Loop_INDEX++) { int бајт_податоци = 명령해석기.ред[Loop_INDEX]; if ((бајт_податоци & 192) == 128) continue; 글칸수 += бајт_податоци >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.Запиши("\r\u001b[2K");
        단말.Запиши(командна_линија ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 ред 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int COLUMNS = табла.Терминал(13) & 65535; return COLUMNS - (командна_линија ? 18 : 9); }
    static void 보이는줄() {
        if (покажувач_VALUE < Start_прозорец) Start_прозорец = покажувач_VALUE;
        while (폭(Start_прозорец, покажувач_VALUE) > 보이는폭()) Start_прозорец = Назад_VALUE(Start_прозорец);
        int крај_позиционирање = Start_прозорец;
        while (крај_позиционирање < Големина && 폭(Start_прозорец, Назад_VALUE(крај_позиционирање)) <= 보이는폭()) крај_позиционирање = Назад_VALUE(крај_позиционирање);
        단말.Запиши("\r\u001b["); 단말.수(командна_линија ? 16 : 7); 단말.Запиши("G\u001b[K");
        if (Start_прозорец > 0) 단말.문자('<');
        for (int Loop_INDEX = Start_прозорец; Loop_INDEX < крај_позиционирање; Loop_INDEX++) табла.직렬쓰기(명령해석기.ред[Loop_INDEX]);
        단말.문자(крај_позиционирање < Големина ? '>' : ' ');
        단말.Запиши("\u001b["); 단말.수(폭(покажувач_VALUE, крај_позиционирање) + 1); 단말.문자('D');
        가로보기 = Start_прозорец > 0 || крај_позиционирање < Големина || 폭(0, Големина) > 보이는폭();
    }
    static void 기록넣기() {
        if (!командна_линија || Големина == 0 || Големина > 1024) return;
        if (LOG_COUNT > 0) {
            int 마지막자리 = (LOG_ред_крај + 15) % 16; boolean 같은여부 = LOG_должина[마지막자리] == Големина;
            for (int Loop_INDEX = 0; 같은여부 && Loop_INDEX < Големина; Loop_INDEX++) if (LOG_ред[마지막자리 * 1024 + Loop_INDEX] != 명령해석기.ред[Loop_INDEX]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_должина[LOG_ред_крај] = Големина; for (int Loop_INDEX = 0; Loop_INDEX < Големина; Loop_INDEX++) LOG_ред[LOG_ред_крај * 1024 + Loop_INDEX] = 명령해석기.ред[Loop_INDEX];
        LOG_ред_крај = (LOG_ред_крај + 1) % 16; if (LOG_COUNT < 16) LOG_COUNT++;
    }
    static void 기록이동(int DELTA_VALUE) {
        if (!командна_линија) return;
        if (SEARCH_VALUE == 0 && DELTA_VALUE > 0) { 저장길이 = Големина; for (int Loop_INDEX = 0; Loop_INDEX < Големина; Loop_INDEX++) Store_VALUE[Loop_INDEX] = 명령해석기.ред[Loop_INDEX]; }
        int Следно_позиционирање = SEARCH_VALUE + DELTA_VALUE; if (Следно_позиционирање < 0 || Следно_позиционирање > LOG_COUNT) return; SEARCH_VALUE = Следно_позиционирање;
        if (SEARCH_VALUE == 0) { Големина = 저장길이; for (int Loop_INDEX = 0; Loop_INDEX < Големина; Loop_INDEX++) 명령해석기.ред[Loop_INDEX] = Store_VALUE[Loop_INDEX]; }
        else { int 보관칸 = (LOG_ред_крај + 16 - SEARCH_VALUE) % 16; Големина = LOG_должина[보관칸]; for (int Loop_INDEX = 0; Loop_INDEX < Големина; Loop_INDEX++) 명령해석기.ред[Loop_INDEX] = LOG_ред[보관칸 * 1024 + Loop_INDEX]; }
        покажувач_VALUE = Големина; 다시();
    }
    static void прикажи_LOG() {
        for (int внес_COUNT = 0; внес_COUNT < LOG_COUNT; внес_COUNT++) {
            int 보관칸 = (LOG_ред_крај + 16 - LOG_COUNT + внес_COUNT) % 16; 단말.수(внес_COUNT + 1); 단말.Запиши("  ");
            for (int Loop_INDEX = 0; Loop_INDEX < LOG_должина[보관칸]; Loop_INDEX++) табла.직렬쓰기(LOG_ред[보관칸 * 1024 + Loop_INDEX]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] податоци_низа, int Start_позиционирање, int внес_COUNT, int 접두말, int 총수, boolean 폴더번호) {
        if (внес_COUNT < 총수 || внес_COUNT > 62) return;
        for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) if (податоци_низа[Start_позиционирање + Loop_INDEX] != 명령해석기.ред[접두말 + Loop_INDEX]) return;
        후보수++; 후보길이 = внес_COUNT + 1;
        for (int Loop_INDEX = 0; Loop_INDEX < внес_COUNT; Loop_INDEX++) 후보[Loop_INDEX] = податоци_низа[Start_позиционирање + Loop_INDEX]; 후보[внес_COUNT] = 폴더번호 ? '/' : ' ';
    }
    static void 완성() {
        if (!командна_линија || покажувач_VALUE != Големина) return;
        int 시작점 = Големина; while (시작점 > 0 && 명령해석기.ред[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDEX = 시작점; Loop_INDEX < Големина; Loop_INDEX++) if (명령해석기.ред[Loop_INDEX] == '/' || 명령해석기.ред[Loop_INDEX] == '"' || 명령해석기.ред[Loop_INDEX] == 39 || 명령해석기.ред[Loop_INDEX] == '\\') return;
        후보수 = 0; int внес_COUNT = Големина - 시작점;
        if (시작점 == 0) {
            for(int Список_INDEX=0;Список_INDEX<2;Список_INDEX++) {
                String внес_Список=Список_INDEX==0?명령들:관리명령.완성어();
                int 읽는자리=0;
                while(읽는자리<внес_Список.length()) {
                    int крај_позиционирање=읽는자리;while(крај_позиционирање<внес_Список.length() && внес_Список.charAt(крај_позиционирање)!=' ')крај_позиционирање++;
                    명령후보넣기(внес_Список,읽는자리,крај_позиционирање,внес_COUNT);읽는자리=крај_позиционирање+1;
                }
            }
        } else {
            Меморија_Датотеки.патека_Start(1); Меморија_Датотеки.патека_бајт(0, '.'); Меморија_Датотеки.нормализирање_VALUE();
            for (int Loop_INDEX = 0; Loop_INDEX < Меморија_Датотеки.датотека_COUNT; Loop_INDEX++) {
                int Start_позиционирање = Меморија_Датотеки.внес_Start(Меморија_Датотеки.Име, Loop_INDEX * 64, Меморија_Датотеки.이름길이[Loop_INDEX]);
                if (Start_позиционирање >= 0) 후보넣기(Меморија_Датотеки.Име, Loop_INDEX * 64 + Start_позиционирање, Меморија_Датотеки.이름길이[Loop_INDEX] - Start_позиционирање, 시작점, внес_COUNT, false);
            }
            for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
                int Start_позиционирање = Меморија_Датотеки.внес_Start(Меморија_Датотеки.Именик_име, Loop_INDEX * 64, Меморија_Датотеки.Именик_должина[Loop_INDEX]);
                if (Start_позиционирање >= 0) 후보넣기(Меморија_Датотеки.Именик_име, Loop_INDEX * 64 + Start_позиционирање, Меморија_Датотеки.Именик_должина[Loop_INDEX] - Start_позиционирање, 시작점, внес_COUNT, true);
            }
        }
        if (후보수 != 1) { табла.직렬쓰기(7); return; }
        for (int Loop_INDEX = внес_COUNT; Loop_INDEX < 후보길이 && Големина < 명령해석기.ред.length - 1; Loop_INDEX++) {
            if (후보[Loop_INDEX] == ' ' && Loop_INDEX != 후보길이 - 1) 명령해석기.ред[Големина++] = '\\';
            명령해석기.ред[Големина++] = 후보[Loop_INDEX];
        }
        покажувач_VALUE = Големина; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = табла.밀리초();
        while (табла.밀리초() - 시작점 < 80) { int бајт_податоци = табла.직렬읽기(); if (бајт_податоци >= 0) return бајт_податоци; табла.YIELD_ЦПУ(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int внес_COUNT = 0, крај_позиционирање = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 12; Loop_INDEX++) { int бајт_податоци = 탈출읽기(); if (бајт_податоци < 0) return; if (бајт_податоци >= '0' && бајт_податоци <= '9') внес_COUNT = внес_COUNT * 10 + бајт_податоци - '0'; else { крај_позиционирање = бајт_податоци; break; } }
        if (крај_позиционирање == 'A') 기록이동(1);
        else if (крај_позиционирање == 'B') 기록이동(-1);
        else if (крај_позиционирање == 'C') { покажувач_VALUE = Назад_VALUE(покажувач_VALUE); 다시(); }
        else if (крај_позиционирање == 'D') { покажувач_VALUE = предна_VALUE(покажувач_VALUE); 다시(); }
        else if (крај_позиционирање == 'H' || крај_позиционирање == '~' && (внес_COUNT == 1 || внес_COUNT == 7)) { покажувач_VALUE = 0; 다시(); }
        else if (крај_позиционирање == 'F' || крај_позиционирање == '~' && (внес_COUNT == 4 || внес_COUNT == 8)) { покажувач_VALUE = Големина; 다시(); }
        else if (крај_позиционирање == '~' && внес_COUNT == 3 && покажувач_VALUE < Големина) {
            int Следно_позиционирање = Назад_VALUE(покажувач_VALUE); for (int Loop_INDEX = Следно_позиционирање; Loop_INDEX < Големина; Loop_INDEX++) 명령해석기.ред[Loop_INDEX - Следно_позиционирање + покажувач_VALUE] = 명령해석기.ред[Loop_INDEX]; Големина -= Следно_позиционирање - покажувач_VALUE; 다시();
        }
        else if (крај_позиционирање == '~' && (внес_COUNT == 5 || внес_COUNT == 6)) табла.Терминал(внес_COUNT == 5 ? 5 : 6);
        else if (крај_позиционирање == '~' && внес_COUNT == 24 && командна_линија) { 명령해석기.Терминал(true); }
    }
    static int Читај() {
        if (!прозорец_сесија.이어읽기) { Големина = покажувач_VALUE = SEARCH_VALUE = Start_прозорец = 0; 가로보기 = false; }
        else { прозорец_сесија.이어읽기 = false; 다시(); } boolean прелевање = false;
        while (true) {
            int бајт_податоци = табла.직렬읽기(); if (бајт_податоци == -4096) return -3;
            if (табла.Терминал(14) != 0) 다시(); if (бајт_податоци < 0) { табла.YIELD_ЦПУ(); continue; }
            if (бајт_податоци == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = бајт_податоци == 13;
            if (бајт_податоци == 27) { 탈출(); continue; }
            if (бајт_податоци == 3) { 단말.Запиши("^C\n"); return -1; }
            if (бајт_податоци == 4 && Големина == 0 && командна_линија) { if (табла.Терминал(2) != 0) 명령해석기.Терминал(true); return -1; }
            if (бајт_податоци == 13 || бајт_податоци == 10) { 단말.문자(10); if (!прелевање) 기록넣기(); return прелевање ? -2 : Големина; }
            if (бајт_податоци == 9 && командна_линија) { 완성(); continue; }
            if (бајт_податоци == 1 || бајт_податоци == 5) { покажувач_VALUE = бајт_податоци == 1 ? 0 : Големина; 다시(); continue; }
            if (бајт_податоци == 8 || бајт_податоци == 127 || бајт_податоци == 21) {
                if (бајт_податоци == 21) { for (int Loop_INDEX = покажувач_VALUE; Loop_INDEX < Големина; Loop_INDEX++) 명령해석기.ред[Loop_INDEX - покажувач_VALUE] = 명령해석기.ред[Loop_INDEX]; Големина -= покажувач_VALUE; покажувач_VALUE = 0; }
                else if (покажувач_VALUE > 0) { int 변경전 = предна_VALUE(покажувач_VALUE); for (int Loop_INDEX = покажувач_VALUE; Loop_INDEX < Големина; Loop_INDEX++) 명령해석기.ред[Loop_INDEX - покажувач_VALUE + 변경전] = 명령해석기.ред[Loop_INDEX]; Големина -= покажувач_VALUE - 변경전; покажувач_VALUE = 변경전; }
                다시(); continue;
            }
            if (бајт_податоци == 11) { Големина = покажувач_VALUE; 다시(); continue; }
            if (бајт_податоци < 32 && бајт_податоци != 9) continue;
            if (Големина == 명령해석기.ред.length) { прелевање = true; continue; }
            for (int Loop_INDEX = Големина; Loop_INDEX > покажувач_VALUE; Loop_INDEX--) 명령해석기.ред[Loop_INDEX] = 명령해석기.ред[Loop_INDEX - 1];
            명령해석기.ред[покажувач_VALUE++] = бајт_податоци; Големина++;
            if (покажувач_VALUE == Големина && !가로보기 && 폭(0, Големина) <= 보이는폭()) табла.직렬쓰기(бајт_податоци);
            else if (покажувач_VALUE == Големина) 보이는줄(); else 다시();
        }
    }
}
