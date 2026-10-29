// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 байт_VALUE 경계를 지키는 삽입/삭제, 방향키, команда LOG_юл, Tab 완성. */
public final class юл_Редактор {
    static boolean команда_юлы;
    static int[] LOG_юл = new int[16 * 1024], LOG_озынлык = new int[16], Store_VALUE = new int[4096], 후보 = new int[64];
    static int LOG_COUNT, LOG_юл_тәмамлау, Эзләү_VALUE, 저장길이, үлчәмен_үзгәртү, курсор_VALUE, 후보수, 후보길이, Start_тәрәз;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd имин_тышча читтәге_дисплей run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String кертү_Исемлек, int Start_урнаштыру, int тәмамлау_урнаштыру, int 입력길이) {
        int байт_COUNT=0;
        for(int урнаштыру_INDEX=Start_урнаштыру;урнаштыру_INDEX<тәмамлау_урнаштыру;урнаштыру_INDEX++) {
            int символ_коды=кертү_Исемлек.charAt(урнаштыру_INDEX);
            if(символ_коды>=0xd800 && символ_коды<=0xdbff && урнаштыру_INDEX+1<тәмамлау_урнаштыру)символ_коды=0x10000+((символ_коды-0xd800)<<10)+кертү_Исемлек.charAt(++урнаштыру_INDEX)-0xdc00;
            int 수=символ_коды<128?1:символ_коды<2048?2:символ_коды<65536?3:4;
            if(байт_COUNT+수>62)return;
            for(int SEQUENCE_VALUE=수-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--)명령후보[байт_COUNT++]=수==1?символ_коды:SEQUENCE_VALUE==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(символ_коды>>(6*SEQUENCE_VALUE)):0x80|((символ_коды>>(6*SEQUENCE_VALUE))&63);
        }
        if(байт_COUNT<입력길이)return;
        for(int урнаштыру_INDEX=0;урнаштыру_INDEX<입력길이;урнаштыру_INDEX++)if(명령후보[урнаштыру_INDEX]!=명령해석기.юл[урнаштыру_INDEX])return;
        후보수++;후보길이=байт_COUNT+1;
        for(int урнаштыру_INDEX=0;урнаштыру_INDEX<байт_COUNT;урнаштыру_INDEX++)후보[урнаштыру_INDEX]=명령후보[урнаштыру_INDEX];후보[байт_COUNT]=' ';
    }
    static int 앞(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.юл[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int Артка_VALUE(int 읽는자리) { if (읽는자리 < үлчәмен_үзгәртү) { 읽는자리++; while (읽는자리 < үлчәмен_үзгәртү && (명령해석기.юл[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int Start_урнаштыру, int күчерү_урыны_VALUE_INDEX) {
        int 글칸수 = 0;
        for (int Loop_INDEX = Start_урнаштыру; Loop_INDEX < күчерү_урыны_VALUE_INDEX; Loop_INDEX++) { int байт_мәгълүмат = 명령해석기.юл[Loop_INDEX]; if ((байт_мәгълүмат & 192) == 128) continue; 글칸수 += байт_мәгълүмат >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.язу("\r\u001b[2K");
        단말.язу(команда_юлы ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 юл 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int COLUMNS = такта.Терминал(13) & 65535; return COLUMNS - (команда_юлы ? 18 : 9); }
    static void 보이는줄() {
        if (курсор_VALUE < Start_тәрәз) Start_тәрәз = курсор_VALUE;
        while (폭(Start_тәрәз, курсор_VALUE) > 보이는폭()) Start_тәрәз = Артка_VALUE(Start_тәрәз);
        int тәмамлау_урнаштыру = Start_тәрәз;
        while (тәмамлау_урнаштыру < үлчәмен_үзгәртү && 폭(Start_тәрәз, Артка_VALUE(тәмамлау_урнаштыру)) <= 보이는폭()) тәмамлау_урнаштыру = Артка_VALUE(тәмамлау_урнаштыру);
        단말.язу("\r\u001b["); 단말.수(команда_юлы ? 16 : 7); 단말.язу("G\u001b[K");
        if (Start_тәрәз > 0) 단말.문자('<');
        for (int Loop_INDEX = Start_тәрәз; Loop_INDEX < тәмамлау_урнаштыру; Loop_INDEX++) такта.직렬쓰기(명령해석기.юл[Loop_INDEX]);
        단말.문자(тәмамлау_урнаштыру < үлчәмен_үзгәртү ? '>' : ' ');
        단말.язу("\u001b["); 단말.수(폭(курсор_VALUE, тәмамлау_урнаштыру) + 1); 단말.문자('D');
        가로보기 = Start_тәрәз > 0 || тәмамлау_урнаштыру < үлчәмен_үзгәртү || 폭(0, үлчәмен_үзгәртү) > 보이는폭();
    }
    static void 기록넣기() {
        if (!команда_юлы || үлчәмен_үзгәртү == 0 || үлчәмен_үзгәртү > 1024) return;
        if (LOG_COUNT > 0) {
            int 마지막자리 = (LOG_юл_тәмамлау + 15) % 16; boolean 같은여부 = LOG_озынлык[마지막자리] == үлчәмен_үзгәртү;
            for (int Loop_INDEX = 0; 같은여부 && Loop_INDEX < үлчәмен_үзгәртү; Loop_INDEX++) if (LOG_юл[마지막자리 * 1024 + Loop_INDEX] != 명령해석기.юл[Loop_INDEX]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_озынлык[LOG_юл_тәмамлау] = үлчәмен_үзгәртү; for (int Loop_INDEX = 0; Loop_INDEX < үлчәмен_үзгәртү; Loop_INDEX++) LOG_юл[LOG_юл_тәмамлау * 1024 + Loop_INDEX] = 명령해석기.юл[Loop_INDEX];
        LOG_юл_тәмамлау = (LOG_юл_тәмамлау + 1) % 16; if (LOG_COUNT < 16) LOG_COUNT++;
    }
    static void 기록이동(int DELTA_VALUE) {
        if (!команда_юлы) return;
        if (Эзләү_VALUE == 0 && DELTA_VALUE > 0) { 저장길이 = үлчәмен_үзгәртү; for (int Loop_INDEX = 0; Loop_INDEX < үлчәмен_үзгәртү; Loop_INDEX++) Store_VALUE[Loop_INDEX] = 명령해석기.юл[Loop_INDEX]; }
        int Киләсе_урнаштыру = Эзләү_VALUE + DELTA_VALUE; if (Киләсе_урнаштыру < 0 || Киләсе_урнаштыру > LOG_COUNT) return; Эзләү_VALUE = Киләсе_урнаштыру;
        if (Эзләү_VALUE == 0) { үлчәмен_үзгәртү = 저장길이; for (int Loop_INDEX = 0; Loop_INDEX < үлчәмен_үзгәртү; Loop_INDEX++) 명령해석기.юл[Loop_INDEX] = Store_VALUE[Loop_INDEX]; }
        else { int 보관칸 = (LOG_юл_тәмамлау + 16 - Эзләү_VALUE) % 16; үлчәмен_үзгәртү = LOG_озынлык[보관칸]; for (int Loop_INDEX = 0; Loop_INDEX < үлчәмен_үзгәртү; Loop_INDEX++) 명령해석기.юл[Loop_INDEX] = LOG_юл[보관칸 * 1024 + Loop_INDEX]; }
        курсор_VALUE = үлчәмен_үзгәртү; 다시();
    }
    static void күрсәтү_LOG() {
        for (int кертү_COUNT = 0; кертү_COUNT < LOG_COUNT; кертү_COUNT++) {
            int 보관칸 = (LOG_юл_тәмамлау + 16 - LOG_COUNT + кертү_COUNT) % 16; 단말.수(кертү_COUNT + 1); 단말.язу("  ");
            for (int Loop_INDEX = 0; Loop_INDEX < LOG_озынлык[보관칸]; Loop_INDEX++) такта.직렬쓰기(LOG_юл[보관칸 * 1024 + Loop_INDEX]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] мәгълүмат_МАССИВ, int Start_урнаштыру, int кертү_COUNT, int 접두말, int 총수, boolean 폴더번호) {
        if (кертү_COUNT < 총수 || кертү_COUNT > 62) return;
        for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) if (мәгълүмат_МАССИВ[Start_урнаштыру + Loop_INDEX] != 명령해석기.юл[접두말 + Loop_INDEX]) return;
        후보수++; 후보길이 = кертү_COUNT + 1;
        for (int Loop_INDEX = 0; Loop_INDEX < кертү_COUNT; Loop_INDEX++) 후보[Loop_INDEX] = мәгълүмат_МАССИВ[Start_урнаштыру + Loop_INDEX]; 후보[кертү_COUNT] = 폴더번호 ? '/' : ' ';
    }
    static void 완성() {
        if (!команда_юлы || курсор_VALUE != үлчәмен_үзгәртү) return;
        int 시작점 = үлчәмен_үзгәртү; while (시작점 > 0 && 명령해석기.юл[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDEX = 시작점; Loop_INDEX < үлчәмен_үзгәртү; Loop_INDEX++) if (명령해석기.юл[Loop_INDEX] == '/' || 명령해석기.юл[Loop_INDEX] == '"' || 명령해석기.юл[Loop_INDEX] == 39 || 명령해석기.юл[Loop_INDEX] == '\\') return;
        후보수 = 0; int кертү_COUNT = үлчәмен_үзгәртү - 시작점;
        if (시작점 == 0) {
            for(int Исемлек_INDEX=0;Исемлек_INDEX<2;Исемлек_INDEX++) {
                String кертү_Исемлек=Исемлек_INDEX==0?명령들:관리명령.완성어();
                int 읽는자리=0;
                while(읽는자리<кертү_Исемлек.length()) {
                    int тәмамлау_урнаштыру=읽는자리;while(тәмамлау_урнаштыру<кертү_Исемлек.length() && кертү_Исемлек.charAt(тәмамлау_урнаштыру)!=' ')тәмамлау_урнаштыру++;
                    명령후보넣기(кертү_Исемлек,읽는자리,тәмамлау_урнаштыру,кертү_COUNT);읽는자리=тәмамлау_урнаштыру+1;
                }
            }
        } else {
            Хәтер_Файллар.юл_Start(1); Хәтер_Файллар.юл_байт(0, '.'); Хәтер_Файллар.нормальләштерү_VALUE();
            for (int Loop_INDEX = 0; Loop_INDEX < Хәтер_Файллар.файл_COUNT; Loop_INDEX++) {
                int Start_урнаштыру = Хәтер_Файллар.кертү_Start(Хәтер_Файллар.исем, Loop_INDEX * 64, Хәтер_Файллар.이름길이[Loop_INDEX]);
                if (Start_урнаштыру >= 0) 후보넣기(Хәтер_Файллар.исем, Loop_INDEX * 64 + Start_урнаштыру, Хәтер_Файллар.이름길이[Loop_INDEX] - Start_урнаштыру, 시작점, кертү_COUNT, false);
            }
            for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
                int Start_урнаштыру = Хәтер_Файллар.кертү_Start(Хәтер_Файллар.каталог_исем, Loop_INDEX * 64, Хәтер_Файллар.каталог_озынлык[Loop_INDEX]);
                if (Start_урнаштыру >= 0) 후보넣기(Хәтер_Файллар.каталог_исем, Loop_INDEX * 64 + Start_урнаштыру, Хәтер_Файллар.каталог_озынлык[Loop_INDEX] - Start_урнаштыру, 시작점, кертү_COUNT, true);
            }
        }
        if (후보수 != 1) { такта.직렬쓰기(7); return; }
        for (int Loop_INDEX = кертү_COUNT; Loop_INDEX < 후보길이 && үлчәмен_үзгәртү < 명령해석기.юл.length - 1; Loop_INDEX++) {
            if (후보[Loop_INDEX] == ' ' && Loop_INDEX != 후보길이 - 1) 명령해석기.юл[үлчәмен_үзгәртү++] = '\\';
            명령해석기.юл[үлчәмен_үзгәртү++] = 후보[Loop_INDEX];
        }
        курсор_VALUE = үлчәмен_үзгәртү; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = такта.밀리초();
        while (такта.밀리초() - 시작점 < 80) { int байт_мәгълүмат = такта.직렬읽기(); if (байт_мәгълүмат >= 0) return байт_мәгълүмат; такта.YIELD_процессор(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int кертү_COUNT = 0, тәмамлау_урнаштыру = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 12; Loop_INDEX++) { int байт_мәгълүмат = 탈출읽기(); if (байт_мәгълүмат < 0) return; if (байт_мәгълүмат >= '0' && байт_мәгълүмат <= '9') кертү_COUNT = кертү_COUNT * 10 + байт_мәгълүмат - '0'; else { тәмамлау_урнаштыру = байт_мәгълүмат; break; } }
        if (тәмамлау_урнаштыру == 'A') 기록이동(1);
        else if (тәмамлау_урнаштыру == 'B') 기록이동(-1);
        else if (тәмамлау_урнаштыру == 'C') { курсор_VALUE = Артка_VALUE(курсор_VALUE); 다시(); }
        else if (тәмамлау_урнаштыру == 'D') { курсор_VALUE = 앞(курсор_VALUE); 다시(); }
        else if (тәмамлау_урнаштыру == 'H' || тәмамлау_урнаштыру == '~' && (кертү_COUNT == 1 || кертү_COUNT == 7)) { курсор_VALUE = 0; 다시(); }
        else if (тәмамлау_урнаштыру == 'F' || тәмамлау_урнаштыру == '~' && (кертү_COUNT == 4 || кертү_COUNT == 8)) { курсор_VALUE = үлчәмен_үзгәртү; 다시(); }
        else if (тәмамлау_урнаштыру == '~' && кертү_COUNT == 3 && курсор_VALUE < үлчәмен_үзгәртү) {
            int Киләсе_урнаштыру = Артка_VALUE(курсор_VALUE); for (int Loop_INDEX = Киләсе_урнаштыру; Loop_INDEX < үлчәмен_үзгәртү; Loop_INDEX++) 명령해석기.юл[Loop_INDEX - Киләсе_урнаштыру + курсор_VALUE] = 명령해석기.юл[Loop_INDEX]; үлчәмен_үзгәртү -= Киләсе_урнаштыру - курсор_VALUE; 다시();
        }
        else if (тәмамлау_урнаштыру == '~' && (кертү_COUNT == 5 || кертү_COUNT == 6)) такта.Терминал(кертү_COUNT == 5 ? 5 : 6);
        else if (тәмамлау_урнаштыру == '~' && кертү_COUNT == 24 && команда_юлы) { 명령해석기.Терминал(true); }
    }
    static int 읽기() {
        if (!тәрәз_сеанс.이어읽기) { үлчәмен_үзгәртү = курсор_VALUE = Эзләү_VALUE = Start_тәрәз = 0; 가로보기 = false; }
        else { тәрәз_сеанс.이어읽기 = false; 다시(); } boolean сыешмау = false;
        while (true) {
            int байт_мәгълүмат = такта.직렬읽기(); if (байт_мәгълүмат == -4096) return -3;
            if (такта.Терминал(14) != 0) 다시(); if (байт_мәгълүмат < 0) { такта.YIELD_процессор(); continue; }
            if (байт_мәгълүмат == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = байт_мәгълүмат == 13;
            if (байт_мәгълүмат == 27) { 탈출(); continue; }
            if (байт_мәгълүмат == 3) { 단말.язу("^C\n"); return -1; }
            if (байт_мәгълүмат == 4 && үлчәмен_үзгәртү == 0 && команда_юлы) { if (такта.Терминал(2) != 0) 명령해석기.Терминал(true); return -1; }
            if (байт_мәгълүмат == 13 || байт_мәгълүмат == 10) { 단말.문자(10); if (!сыешмау) 기록넣기(); return сыешмау ? -2 : үлчәмен_үзгәртү; }
            if (байт_мәгълүмат == 9 && команда_юлы) { 완성(); continue; }
            if (байт_мәгълүмат == 1 || байт_мәгълүмат == 5) { курсор_VALUE = байт_мәгълүмат == 1 ? 0 : үлчәмен_үзгәртү; 다시(); continue; }
            if (байт_мәгълүмат == 8 || байт_мәгълүмат == 127 || байт_мәгълүмат == 21) {
                if (байт_мәгълүмат == 21) { for (int Loop_INDEX = курсор_VALUE; Loop_INDEX < үлчәмен_үзгәртү; Loop_INDEX++) 명령해석기.юл[Loop_INDEX - курсор_VALUE] = 명령해석기.юл[Loop_INDEX]; үлчәмен_үзгәртү -= курсор_VALUE; курсор_VALUE = 0; }
                else if (курсор_VALUE > 0) { int 변경전 = 앞(курсор_VALUE); for (int Loop_INDEX = курсор_VALUE; Loop_INDEX < үлчәмен_үзгәртү; Loop_INDEX++) 명령해석기.юл[Loop_INDEX - курсор_VALUE + 변경전] = 명령해석기.юл[Loop_INDEX]; үлчәмен_үзгәртү -= курсор_VALUE - 변경전; курсор_VALUE = 변경전; }
                다시(); continue;
            }
            if (байт_мәгълүмат == 11) { үлчәмен_үзгәртү = курсор_VALUE; 다시(); continue; }
            if (байт_мәгълүмат < 32 && байт_мәгълүмат != 9) continue;
            if (үлчәмен_үзгәртү == 명령해석기.юл.length) { сыешмау = true; continue; }
            for (int Loop_INDEX = үлчәмен_үзгәртү; Loop_INDEX > курсор_VALUE; Loop_INDEX--) 명령해석기.юл[Loop_INDEX] = 명령해석기.юл[Loop_INDEX - 1];
            명령해석기.юл[курсор_VALUE++] = байт_мәгълүмат; үлчәмен_үзгәртү++;
            if (курсор_VALUE == үлчәмен_үзгәртү && !가로보기 && 폭(0, үлчәмен_үзгәртү) <= 보이는폭()) такта.직렬쓰기(байт_мәгълүмат);
            else if (курсор_VALUE == үлчәмен_үзгәртү) 보이는줄(); else 다시();
        }
    }
}
