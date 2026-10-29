// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 byte_VALUE 경계를 지키는 삽입/삭제, 방향키, utos LOG_hanay, Tab 완성. */
public final class linya_Editor {
    static boolean linya_ng_utos;
    static int[] LOG_hanay = new int[16 * 1024], LOG_haba = new int[16], Store_VALUE = new int[4096], 후보 = new int[64];
    static int LOG_COUNT, LOG_hanay_tapusin, SEARCH_VALUE, 저장길이, sukat_82232621, kursor_VALUE, 후보수, 후보길이, Start_window;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd secure_shell malayuan_display run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String pagpasok_list, int Start_posisyon, int tapusin_posisyon, int 입력길이) {
        int byte_COUNT=0;
        for(int posisyon_INDEX=Start_posisyon;posisyon_INDEX<tapusin_posisyon;posisyon_INDEX++) {
            int character_code=pagpasok_list.charAt(posisyon_INDEX);
            if(character_code>=0xd800 && character_code<=0xdbff && posisyon_INDEX+1<tapusin_posisyon)character_code=0x10000+((character_code-0xd800)<<10)+pagpasok_list.charAt(++posisyon_INDEX)-0xdc00;
            int 수=character_code<128?1:character_code<2048?2:character_code<65536?3:4;
            if(byte_COUNT+수>62)return;
            for(int SEQUENCE_VALUE=수-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--)명령후보[byte_COUNT++]=수==1?character_code:SEQUENCE_VALUE==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(character_code>>(6*SEQUENCE_VALUE)):0x80|((character_code>>(6*SEQUENCE_VALUE))&63);
        }
        if(byte_COUNT<입력길이)return;
        for(int posisyon_INDEX=0;posisyon_INDEX<입력길이;posisyon_INDEX++)if(명령후보[posisyon_INDEX]!=명령해석기.linya[posisyon_INDEX])return;
        후보수++;후보길이=byte_COUNT+1;
        for(int posisyon_INDEX=0;posisyon_INDEX<byte_COUNT;posisyon_INDEX++)후보[posisyon_INDEX]=명령후보[posisyon_INDEX];후보[byte_COUNT]=' ';
    }
    static int nasa_harap_VALUE(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.linya[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int Bumalik_VALUE(int 읽는자리) { if (읽는자리 < sukat_82232621) { 읽는자리++; while (읽는자리 < sukat_82232621 && (명령해석기.linya[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int Start_posisyon, int patutunguhan_VALUE_INDEX) {
        int 글칸수 = 0;
        for (int Loop_INDEX = Start_posisyon; Loop_INDEX < patutunguhan_VALUE_INDEX; Loop_INDEX++) { int byte_data = 명령해석기.linya[Loop_INDEX]; if ((byte_data & 192) == 128) continue; 글칸수 += byte_data >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.sumulat("\r\u001b[2K");
        단말.sumulat(linya_ng_utos ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 linya 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int COLUMNS = board.Terminal(13) & 65535; return COLUMNS - (linya_ng_utos ? 18 : 9); }
    static void 보이는줄() {
        if (kursor_VALUE < Start_window) Start_window = kursor_VALUE;
        while (폭(Start_window, kursor_VALUE) > 보이는폭()) Start_window = Bumalik_VALUE(Start_window);
        int tapusin_posisyon = Start_window;
        while (tapusin_posisyon < sukat_82232621 && 폭(Start_window, Bumalik_VALUE(tapusin_posisyon)) <= 보이는폭()) tapusin_posisyon = Bumalik_VALUE(tapusin_posisyon);
        단말.sumulat("\r\u001b["); 단말.수(linya_ng_utos ? 16 : 7); 단말.sumulat("G\u001b[K");
        if (Start_window > 0) 단말.문자('<');
        for (int Loop_INDEX = Start_window; Loop_INDEX < tapusin_posisyon; Loop_INDEX++) board.직렬쓰기(명령해석기.linya[Loop_INDEX]);
        단말.문자(tapusin_posisyon < sukat_82232621 ? '>' : ' ');
        단말.sumulat("\u001b["); 단말.수(폭(kursor_VALUE, tapusin_posisyon) + 1); 단말.문자('D');
        가로보기 = Start_window > 0 || tapusin_posisyon < sukat_82232621 || 폭(0, sukat_82232621) > 보이는폭();
    }
    static void 기록넣기() {
        if (!linya_ng_utos || sukat_82232621 == 0 || sukat_82232621 > 1024) return;
        if (LOG_COUNT > 0) {
            int 마지막자리 = (LOG_hanay_tapusin + 15) % 16; boolean 같은여부 = LOG_haba[마지막자리] == sukat_82232621;
            for (int Loop_INDEX = 0; 같은여부 && Loop_INDEX < sukat_82232621; Loop_INDEX++) if (LOG_hanay[마지막자리 * 1024 + Loop_INDEX] != 명령해석기.linya[Loop_INDEX]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_haba[LOG_hanay_tapusin] = sukat_82232621; for (int Loop_INDEX = 0; Loop_INDEX < sukat_82232621; Loop_INDEX++) LOG_hanay[LOG_hanay_tapusin * 1024 + Loop_INDEX] = 명령해석기.linya[Loop_INDEX];
        LOG_hanay_tapusin = (LOG_hanay_tapusin + 1) % 16; if (LOG_COUNT < 16) LOG_COUNT++;
    }
    static void 기록이동(int DELTA_VALUE) {
        if (!linya_ng_utos) return;
        if (SEARCH_VALUE == 0 && DELTA_VALUE > 0) { 저장길이 = sukat_82232621; for (int Loop_INDEX = 0; Loop_INDEX < sukat_82232621; Loop_INDEX++) Store_VALUE[Loop_INDEX] = 명령해석기.linya[Loop_INDEX]; }
        int Susunod_posisyon = SEARCH_VALUE + DELTA_VALUE; if (Susunod_posisyon < 0 || Susunod_posisyon > LOG_COUNT) return; SEARCH_VALUE = Susunod_posisyon;
        if (SEARCH_VALUE == 0) { sukat_82232621 = 저장길이; for (int Loop_INDEX = 0; Loop_INDEX < sukat_82232621; Loop_INDEX++) 명령해석기.linya[Loop_INDEX] = Store_VALUE[Loop_INDEX]; }
        else { int 보관칸 = (LOG_hanay_tapusin + 16 - SEARCH_VALUE) % 16; sukat_82232621 = LOG_haba[보관칸]; for (int Loop_INDEX = 0; Loop_INDEX < sukat_82232621; Loop_INDEX++) 명령해석기.linya[Loop_INDEX] = LOG_hanay[보관칸 * 1024 + Loop_INDEX]; }
        kursor_VALUE = sukat_82232621; 다시();
    }
    static void ipakita_LOG() {
        for (int pagpasok_COUNT = 0; pagpasok_COUNT < LOG_COUNT; pagpasok_COUNT++) {
            int 보관칸 = (LOG_hanay_tapusin + 16 - LOG_COUNT + pagpasok_COUNT) % 16; 단말.수(pagpasok_COUNT + 1); 단말.sumulat("  ");
            for (int Loop_INDEX = 0; Loop_INDEX < LOG_haba[보관칸]; Loop_INDEX++) board.직렬쓰기(LOG_hanay[보관칸 * 1024 + Loop_INDEX]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] data_ARRAY, int Start_posisyon, int pagpasok_COUNT, int 접두말, int 총수, boolean 폴더번호) {
        if (pagpasok_COUNT < 총수 || pagpasok_COUNT > 62) return;
        for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) if (data_ARRAY[Start_posisyon + Loop_INDEX] != 명령해석기.linya[접두말 + Loop_INDEX]) return;
        후보수++; 후보길이 = pagpasok_COUNT + 1;
        for (int Loop_INDEX = 0; Loop_INDEX < pagpasok_COUNT; Loop_INDEX++) 후보[Loop_INDEX] = data_ARRAY[Start_posisyon + Loop_INDEX]; 후보[pagpasok_COUNT] = 폴더번호 ? '/' : ' ';
    }
    static void 완성() {
        if (!linya_ng_utos || kursor_VALUE != sukat_82232621) return;
        int 시작점 = sukat_82232621; while (시작점 > 0 && 명령해석기.linya[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDEX = 시작점; Loop_INDEX < sukat_82232621; Loop_INDEX++) if (명령해석기.linya[Loop_INDEX] == '/' || 명령해석기.linya[Loop_INDEX] == '"' || 명령해석기.linya[Loop_INDEX] == 39 || 명령해석기.linya[Loop_INDEX] == '\\') return;
        후보수 = 0; int pagpasok_COUNT = sukat_82232621 - 시작점;
        if (시작점 == 0) {
            for(int list_INDEX=0;list_INDEX<2;list_INDEX++) {
                String pagpasok_list=list_INDEX==0?명령들:관리명령.완성어();
                int 읽는자리=0;
                while(읽는자리<pagpasok_list.length()) {
                    int tapusin_posisyon=읽는자리;while(tapusin_posisyon<pagpasok_list.length() && pagpasok_list.charAt(tapusin_posisyon)!=' ')tapusin_posisyon++;
                    명령후보넣기(pagpasok_list,읽는자리,tapusin_posisyon,pagpasok_COUNT);읽는자리=tapusin_posisyon+1;
                }
            }
        } else {
            Memory_Mga_File.path_Start(1); Memory_Mga_File.path_byte(0, '.'); Memory_Mga_File.normalisahin_VALUE();
            for (int Loop_INDEX = 0; Loop_INDEX < Memory_Mga_File.file_COUNT; Loop_INDEX++) {
                int Start_posisyon = Memory_Mga_File.pagpasok_Start(Memory_Mga_File.pangalan, Loop_INDEX * 64, Memory_Mga_File.이름길이[Loop_INDEX]);
                if (Start_posisyon >= 0) 후보넣기(Memory_Mga_File.pangalan, Loop_INDEX * 64 + Start_posisyon, Memory_Mga_File.이름길이[Loop_INDEX] - Start_posisyon, 시작점, pagpasok_COUNT, false);
            }
            for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
                int Start_posisyon = Memory_Mga_File.pagpasok_Start(Memory_Mga_File.Directory_pangalan, Loop_INDEX * 64, Memory_Mga_File.Directory_haba[Loop_INDEX]);
                if (Start_posisyon >= 0) 후보넣기(Memory_Mga_File.Directory_pangalan, Loop_INDEX * 64 + Start_posisyon, Memory_Mga_File.Directory_haba[Loop_INDEX] - Start_posisyon, 시작점, pagpasok_COUNT, true);
            }
        }
        if (후보수 != 1) { board.직렬쓰기(7); return; }
        for (int Loop_INDEX = pagpasok_COUNT; Loop_INDEX < 후보길이 && sukat_82232621 < 명령해석기.linya.length - 1; Loop_INDEX++) {
            if (후보[Loop_INDEX] == ' ' && Loop_INDEX != 후보길이 - 1) 명령해석기.linya[sukat_82232621++] = '\\';
            명령해석기.linya[sukat_82232621++] = 후보[Loop_INDEX];
        }
        kursor_VALUE = sukat_82232621; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = board.밀리초();
        while (board.밀리초() - 시작점 < 80) { int byte_data = board.직렬읽기(); if (byte_data >= 0) return byte_data; board.YIELD_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int pagpasok_COUNT = 0, tapusin_posisyon = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 12; Loop_INDEX++) { int byte_data = 탈출읽기(); if (byte_data < 0) return; if (byte_data >= '0' && byte_data <= '9') pagpasok_COUNT = pagpasok_COUNT * 10 + byte_data - '0'; else { tapusin_posisyon = byte_data; break; } }
        if (tapusin_posisyon == 'A') 기록이동(1);
        else if (tapusin_posisyon == 'B') 기록이동(-1);
        else if (tapusin_posisyon == 'C') { kursor_VALUE = Bumalik_VALUE(kursor_VALUE); 다시(); }
        else if (tapusin_posisyon == 'D') { kursor_VALUE = nasa_harap_VALUE(kursor_VALUE); 다시(); }
        else if (tapusin_posisyon == 'H' || tapusin_posisyon == '~' && (pagpasok_COUNT == 1 || pagpasok_COUNT == 7)) { kursor_VALUE = 0; 다시(); }
        else if (tapusin_posisyon == 'F' || tapusin_posisyon == '~' && (pagpasok_COUNT == 4 || pagpasok_COUNT == 8)) { kursor_VALUE = sukat_82232621; 다시(); }
        else if (tapusin_posisyon == '~' && pagpasok_COUNT == 3 && kursor_VALUE < sukat_82232621) {
            int Susunod_posisyon = Bumalik_VALUE(kursor_VALUE); for (int Loop_INDEX = Susunod_posisyon; Loop_INDEX < sukat_82232621; Loop_INDEX++) 명령해석기.linya[Loop_INDEX - Susunod_posisyon + kursor_VALUE] = 명령해석기.linya[Loop_INDEX]; sukat_82232621 -= Susunod_posisyon - kursor_VALUE; 다시();
        }
        else if (tapusin_posisyon == '~' && (pagpasok_COUNT == 5 || pagpasok_COUNT == 6)) board.Terminal(pagpasok_COUNT == 5 ? 5 : 6);
        else if (tapusin_posisyon == '~' && pagpasok_COUNT == 24 && linya_ng_utos) { 명령해석기.Terminal(true); }
    }
    static int 읽기() {
        if (!window_sesyon.이어읽기) { sukat_82232621 = kursor_VALUE = SEARCH_VALUE = Start_window = 0; 가로보기 = false; }
        else { window_sesyon.이어읽기 = false; 다시(); } boolean sobrang_teksto = false;
        while (true) {
            int byte_data = board.직렬읽기(); if (byte_data == -4096) return -3;
            if (board.Terminal(14) != 0) 다시(); if (byte_data < 0) { board.YIELD_CPU(); continue; }
            if (byte_data == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = byte_data == 13;
            if (byte_data == 27) { 탈출(); continue; }
            if (byte_data == 3) { 단말.sumulat("^C\n"); return -1; }
            if (byte_data == 4 && sukat_82232621 == 0 && linya_ng_utos) { if (board.Terminal(2) != 0) 명령해석기.Terminal(true); return -1; }
            if (byte_data == 13 || byte_data == 10) { 단말.문자(10); if (!sobrang_teksto) 기록넣기(); return sobrang_teksto ? -2 : sukat_82232621; }
            if (byte_data == 9 && linya_ng_utos) { 완성(); continue; }
            if (byte_data == 1 || byte_data == 5) { kursor_VALUE = byte_data == 1 ? 0 : sukat_82232621; 다시(); continue; }
            if (byte_data == 8 || byte_data == 127 || byte_data == 21) {
                if (byte_data == 21) { for (int Loop_INDEX = kursor_VALUE; Loop_INDEX < sukat_82232621; Loop_INDEX++) 명령해석기.linya[Loop_INDEX - kursor_VALUE] = 명령해석기.linya[Loop_INDEX]; sukat_82232621 -= kursor_VALUE; kursor_VALUE = 0; }
                else if (kursor_VALUE > 0) { int 변경전 = nasa_harap_VALUE(kursor_VALUE); for (int Loop_INDEX = kursor_VALUE; Loop_INDEX < sukat_82232621; Loop_INDEX++) 명령해석기.linya[Loop_INDEX - kursor_VALUE + 변경전] = 명령해석기.linya[Loop_INDEX]; sukat_82232621 -= kursor_VALUE - 변경전; kursor_VALUE = 변경전; }
                다시(); continue;
            }
            if (byte_data == 11) { sukat_82232621 = kursor_VALUE; 다시(); continue; }
            if (byte_data < 32 && byte_data != 9) continue;
            if (sukat_82232621 == 명령해석기.linya.length) { sobrang_teksto = true; continue; }
            for (int Loop_INDEX = sukat_82232621; Loop_INDEX > kursor_VALUE; Loop_INDEX--) 명령해석기.linya[Loop_INDEX] = 명령해석기.linya[Loop_INDEX - 1];
            명령해석기.linya[kursor_VALUE++] = byte_data; sukat_82232621++;
            if (kursor_VALUE == sukat_82232621 && !가로보기 && 폭(0, sukat_82232621) <= 보이는폭()) board.직렬쓰기(byte_data);
            else if (kursor_VALUE == sukat_82232621) 보이는줄(); else 다시();
        }
    }
}
