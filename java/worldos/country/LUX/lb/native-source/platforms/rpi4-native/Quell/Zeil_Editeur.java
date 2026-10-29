// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 Byte_VALUE 경계를 지키는 삽입/삭제, 방향키, Befeel LOG_Rei, Tab 완성. */
public final class Zeil_Editeur {
    static boolean Befeelszeil;
    static int[] LOG_Rei = new int[16 * 1024], LOG_Längt = new int[16], Store_VALUE = new int[4096], 후보 = new int[64];
    static int LOG_COUNT, LOG_Rei_bëennegen, Sich_VALUE, 저장길이, d_Gréisst_veränneren, Curseur_VALUE, 후보수, 후보길이, Start_Fënster;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd sécher_Shell extern_Bildschierm run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String Agab_Lëscht, int Start_positionéieren, int bëennegen_positionéieren, int 입력길이) {
        int Byte_COUNT=0;
        for(int positionéieren_INDEX=Start_positionéieren;positionéieren_INDEX<bëennegen_positionéieren;positionéieren_INDEX++) {
            int Zeechecode=Agab_Lëscht.charAt(positionéieren_INDEX);
            if(Zeechecode>=0xd800 && Zeechecode<=0xdbff && positionéieren_INDEX+1<bëennegen_positionéieren)Zeechecode=0x10000+((Zeechecode-0xd800)<<10)+Agab_Lëscht.charAt(++positionéieren_INDEX)-0xdc00;
            int 수=Zeechecode<128?1:Zeechecode<2048?2:Zeechecode<65536?3:4;
            if(Byte_COUNT+수>62)return;
            for(int SEQUENCE_VALUE=수-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--)명령후보[Byte_COUNT++]=수==1?Zeechecode:SEQUENCE_VALUE==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(Zeechecode>>(6*SEQUENCE_VALUE)):0x80|((Zeechecode>>(6*SEQUENCE_VALUE))&63);
        }
        if(Byte_COUNT<입력길이)return;
        for(int positionéieren_INDEX=0;positionéieren_INDEX<입력길이;positionéieren_INDEX++)if(명령후보[positionéieren_INDEX]!=명령해석기.Zeil[positionéieren_INDEX])return;
        후보수++;후보길이=Byte_COUNT+1;
        for(int positionéieren_INDEX=0;positionéieren_INDEX<Byte_COUNT;positionéieren_INDEX++)후보[positionéieren_INDEX]=명령후보[positionéieren_INDEX];후보[Byte_COUNT]=' ';
    }
    static int 앞(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.Zeil[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int Zeréck_VALUE(int 읽는자리) { if (읽는자리 < d_Gréisst_veränneren) { 읽는자리++; while (읽는자리 < d_Gréisst_veränneren && (명령해석기.Zeil[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int Start_positionéieren, int Zil_VALUE_INDEX) {
        int 글칸수 = 0;
        for (int Loop_INDEX = Start_positionéieren; Loop_INDEX < Zil_VALUE_INDEX; Loop_INDEX++) { int Byte_Daten = 명령해석기.Zeil[Loop_INDEX]; if ((Byte_Daten & 192) == 128) continue; 글칸수 += Byte_Daten >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.schreiwen("\r\u001b[2K");
        단말.schreiwen(Befeelszeil ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 Zeil 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int COLUMNS = Board.Terminal(13) & 65535; return COLUMNS - (Befeelszeil ? 18 : 9); }
    static void 보이는줄() {
        if (Curseur_VALUE < Start_Fënster) Start_Fënster = Curseur_VALUE;
        while (폭(Start_Fënster, Curseur_VALUE) > 보이는폭()) Start_Fënster = Zeréck_VALUE(Start_Fënster);
        int bëennegen_positionéieren = Start_Fënster;
        while (bëennegen_positionéieren < d_Gréisst_veränneren && 폭(Start_Fënster, Zeréck_VALUE(bëennegen_positionéieren)) <= 보이는폭()) bëennegen_positionéieren = Zeréck_VALUE(bëennegen_positionéieren);
        단말.schreiwen("\r\u001b["); 단말.수(Befeelszeil ? 16 : 7); 단말.schreiwen("G\u001b[K");
        if (Start_Fënster > 0) 단말.문자('<');
        for (int Loop_INDEX = Start_Fënster; Loop_INDEX < bëennegen_positionéieren; Loop_INDEX++) Board.직렬쓰기(명령해석기.Zeil[Loop_INDEX]);
        단말.문자(bëennegen_positionéieren < d_Gréisst_veränneren ? '>' : ' ');
        단말.schreiwen("\u001b["); 단말.수(폭(Curseur_VALUE, bëennegen_positionéieren) + 1); 단말.문자('D');
        가로보기 = Start_Fënster > 0 || bëennegen_positionéieren < d_Gréisst_veränneren || 폭(0, d_Gréisst_veränneren) > 보이는폭();
    }
    static void 기록넣기() {
        if (!Befeelszeil || d_Gréisst_veränneren == 0 || d_Gréisst_veränneren > 1024) return;
        if (LOG_COUNT > 0) {
            int 마지막자리 = (LOG_Rei_bëennegen + 15) % 16; boolean 같은여부 = LOG_Längt[마지막자리] == d_Gréisst_veränneren;
            for (int Loop_INDEX = 0; 같은여부 && Loop_INDEX < d_Gréisst_veränneren; Loop_INDEX++) if (LOG_Rei[마지막자리 * 1024 + Loop_INDEX] != 명령해석기.Zeil[Loop_INDEX]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_Längt[LOG_Rei_bëennegen] = d_Gréisst_veränneren; for (int Loop_INDEX = 0; Loop_INDEX < d_Gréisst_veränneren; Loop_INDEX++) LOG_Rei[LOG_Rei_bëennegen * 1024 + Loop_INDEX] = 명령해석기.Zeil[Loop_INDEX];
        LOG_Rei_bëennegen = (LOG_Rei_bëennegen + 1) % 16; if (LOG_COUNT < 16) LOG_COUNT++;
    }
    static void 기록이동(int DELTA_VALUE) {
        if (!Befeelszeil) return;
        if (Sich_VALUE == 0 && DELTA_VALUE > 0) { 저장길이 = d_Gréisst_veränneren; for (int Loop_INDEX = 0; Loop_INDEX < d_Gréisst_veränneren; Loop_INDEX++) Store_VALUE[Loop_INDEX] = 명령해석기.Zeil[Loop_INDEX]; }
        int Weider_positionéieren = Sich_VALUE + DELTA_VALUE; if (Weider_positionéieren < 0 || Weider_positionéieren > LOG_COUNT) return; Sich_VALUE = Weider_positionéieren;
        if (Sich_VALUE == 0) { d_Gréisst_veränneren = 저장길이; for (int Loop_INDEX = 0; Loop_INDEX < d_Gréisst_veränneren; Loop_INDEX++) 명령해석기.Zeil[Loop_INDEX] = Store_VALUE[Loop_INDEX]; }
        else { int 보관칸 = (LOG_Rei_bëennegen + 16 - Sich_VALUE) % 16; d_Gréisst_veränneren = LOG_Längt[보관칸]; for (int Loop_INDEX = 0; Loop_INDEX < d_Gréisst_veränneren; Loop_INDEX++) 명령해석기.Zeil[Loop_INDEX] = LOG_Rei[보관칸 * 1024 + Loop_INDEX]; }
        Curseur_VALUE = d_Gréisst_veränneren; 다시();
    }
    static void Show_LOG() {
        for (int Agab_COUNT = 0; Agab_COUNT < LOG_COUNT; Agab_COUNT++) {
            int 보관칸 = (LOG_Rei_bëennegen + 16 - LOG_COUNT + Agab_COUNT) % 16; 단말.수(Agab_COUNT + 1); 단말.schreiwen("  ");
            for (int Loop_INDEX = 0; Loop_INDEX < LOG_Längt[보관칸]; Loop_INDEX++) Board.직렬쓰기(LOG_Rei[보관칸 * 1024 + Loop_INDEX]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] Daten_ARRAY, int Start_positionéieren, int Agab_COUNT, int 접두말, int 총수, boolean 폴더번호) {
        if (Agab_COUNT < 총수 || Agab_COUNT > 62) return;
        for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) if (Daten_ARRAY[Start_positionéieren + Loop_INDEX] != 명령해석기.Zeil[접두말 + Loop_INDEX]) return;
        후보수++; 후보길이 = Agab_COUNT + 1;
        for (int Loop_INDEX = 0; Loop_INDEX < Agab_COUNT; Loop_INDEX++) 후보[Loop_INDEX] = Daten_ARRAY[Start_positionéieren + Loop_INDEX]; 후보[Agab_COUNT] = 폴더번호 ? '/' : ' ';
    }
    static void 완성() {
        if (!Befeelszeil || Curseur_VALUE != d_Gréisst_veränneren) return;
        int 시작점 = d_Gréisst_veränneren; while (시작점 > 0 && 명령해석기.Zeil[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDEX = 시작점; Loop_INDEX < d_Gréisst_veränneren; Loop_INDEX++) if (명령해석기.Zeil[Loop_INDEX] == '/' || 명령해석기.Zeil[Loop_INDEX] == '"' || 명령해석기.Zeil[Loop_INDEX] == 39 || 명령해석기.Zeil[Loop_INDEX] == '\\') return;
        후보수 = 0; int Agab_COUNT = d_Gréisst_veränneren - 시작점;
        if (시작점 == 0) {
            for(int Lëscht_INDEX=0;Lëscht_INDEX<2;Lëscht_INDEX++) {
                String Agab_Lëscht=Lëscht_INDEX==0?명령들:관리명령.완성어();
                int 읽는자리=0;
                while(읽는자리<Agab_Lëscht.length()) {
                    int bëennegen_positionéieren=읽는자리;while(bëennegen_positionéieren<Agab_Lëscht.length() && Agab_Lëscht.charAt(bëennegen_positionéieren)!=' ')bëennegen_positionéieren++;
                    명령후보넣기(Agab_Lëscht,읽는자리,bëennegen_positionéieren,Agab_COUNT);읽는자리=bëennegen_positionéieren+1;
                }
            }
        } else {
            Späicher_Fichieren.Wee_Start(1); Späicher_Fichieren.Wee_Byte(0, '.'); Späicher_Fichieren.normaliséieren_VALUE();
            for (int Loop_INDEX = 0; Loop_INDEX < Späicher_Fichieren.Fichier_COUNT; Loop_INDEX++) {
                int Start_positionéieren = Späicher_Fichieren.Agab_Start(Späicher_Fichieren.Numm, Loop_INDEX * 64, Späicher_Fichieren.이름길이[Loop_INDEX]);
                if (Start_positionéieren >= 0) 후보넣기(Späicher_Fichieren.Numm, Loop_INDEX * 64 + Start_positionéieren, Späicher_Fichieren.이름길이[Loop_INDEX] - Start_positionéieren, 시작점, Agab_COUNT, false);
            }
            for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
                int Start_positionéieren = Späicher_Fichieren.Agab_Start(Späicher_Fichieren.Verzeechnes_Numm, Loop_INDEX * 64, Späicher_Fichieren.Verzeechnes_Längt[Loop_INDEX]);
                if (Start_positionéieren >= 0) 후보넣기(Späicher_Fichieren.Verzeechnes_Numm, Loop_INDEX * 64 + Start_positionéieren, Späicher_Fichieren.Verzeechnes_Längt[Loop_INDEX] - Start_positionéieren, 시작점, Agab_COUNT, true);
            }
        }
        if (후보수 != 1) { Board.직렬쓰기(7); return; }
        for (int Loop_INDEX = Agab_COUNT; Loop_INDEX < 후보길이 && d_Gréisst_veränneren < 명령해석기.Zeil.length - 1; Loop_INDEX++) {
            if (후보[Loop_INDEX] == ' ' && Loop_INDEX != 후보길이 - 1) 명령해석기.Zeil[d_Gréisst_veränneren++] = '\\';
            명령해석기.Zeil[d_Gréisst_veränneren++] = 후보[Loop_INDEX];
        }
        Curseur_VALUE = d_Gréisst_veränneren; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = Board.밀리초();
        while (Board.밀리초() - 시작점 < 80) { int Byte_Daten = Board.직렬읽기(); if (Byte_Daten >= 0) return Byte_Daten; Board.YIELD_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int Agab_COUNT = 0, bëennegen_positionéieren = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 12; Loop_INDEX++) { int Byte_Daten = 탈출읽기(); if (Byte_Daten < 0) return; if (Byte_Daten >= '0' && Byte_Daten <= '9') Agab_COUNT = Agab_COUNT * 10 + Byte_Daten - '0'; else { bëennegen_positionéieren = Byte_Daten; break; } }
        if (bëennegen_positionéieren == 'A') 기록이동(1);
        else if (bëennegen_positionéieren == 'B') 기록이동(-1);
        else if (bëennegen_positionéieren == 'C') { Curseur_VALUE = Zeréck_VALUE(Curseur_VALUE); 다시(); }
        else if (bëennegen_positionéieren == 'D') { Curseur_VALUE = 앞(Curseur_VALUE); 다시(); }
        else if (bëennegen_positionéieren == 'H' || bëennegen_positionéieren == '~' && (Agab_COUNT == 1 || Agab_COUNT == 7)) { Curseur_VALUE = 0; 다시(); }
        else if (bëennegen_positionéieren == 'F' || bëennegen_positionéieren == '~' && (Agab_COUNT == 4 || Agab_COUNT == 8)) { Curseur_VALUE = d_Gréisst_veränneren; 다시(); }
        else if (bëennegen_positionéieren == '~' && Agab_COUNT == 3 && Curseur_VALUE < d_Gréisst_veränneren) {
            int Weider_positionéieren = Zeréck_VALUE(Curseur_VALUE); for (int Loop_INDEX = Weider_positionéieren; Loop_INDEX < d_Gréisst_veränneren; Loop_INDEX++) 명령해석기.Zeil[Loop_INDEX - Weider_positionéieren + Curseur_VALUE] = 명령해석기.Zeil[Loop_INDEX]; d_Gréisst_veränneren -= Weider_positionéieren - Curseur_VALUE; 다시();
        }
        else if (bëennegen_positionéieren == '~' && (Agab_COUNT == 5 || Agab_COUNT == 6)) Board.Terminal(Agab_COUNT == 5 ? 5 : 6);
        else if (bëennegen_positionéieren == '~' && Agab_COUNT == 24 && Befeelszeil) { 명령해석기.Terminal(true); }
    }
    static int 읽기() {
        if (!Fënster_Sessioun.이어읽기) { d_Gréisst_veränneren = Curseur_VALUE = Sich_VALUE = Start_Fënster = 0; 가로보기 = false; }
        else { Fënster_Sessioun.이어읽기 = false; 다시(); } boolean Iwwerlaf = false;
        while (true) {
            int Byte_Daten = Board.직렬읽기(); if (Byte_Daten == -4096) return -3;
            if (Board.Terminal(14) != 0) 다시(); if (Byte_Daten < 0) { Board.YIELD_CPU(); continue; }
            if (Byte_Daten == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = Byte_Daten == 13;
            if (Byte_Daten == 27) { 탈출(); continue; }
            if (Byte_Daten == 3) { 단말.schreiwen("^C\n"); return -1; }
            if (Byte_Daten == 4 && d_Gréisst_veränneren == 0 && Befeelszeil) { if (Board.Terminal(2) != 0) 명령해석기.Terminal(true); return -1; }
            if (Byte_Daten == 13 || Byte_Daten == 10) { 단말.문자(10); if (!Iwwerlaf) 기록넣기(); return Iwwerlaf ? -2 : d_Gréisst_veränneren; }
            if (Byte_Daten == 9 && Befeelszeil) { 완성(); continue; }
            if (Byte_Daten == 1 || Byte_Daten == 5) { Curseur_VALUE = Byte_Daten == 1 ? 0 : d_Gréisst_veränneren; 다시(); continue; }
            if (Byte_Daten == 8 || Byte_Daten == 127 || Byte_Daten == 21) {
                if (Byte_Daten == 21) { for (int Loop_INDEX = Curseur_VALUE; Loop_INDEX < d_Gréisst_veränneren; Loop_INDEX++) 명령해석기.Zeil[Loop_INDEX - Curseur_VALUE] = 명령해석기.Zeil[Loop_INDEX]; d_Gréisst_veränneren -= Curseur_VALUE; Curseur_VALUE = 0; }
                else if (Curseur_VALUE > 0) { int 변경전 = 앞(Curseur_VALUE); for (int Loop_INDEX = Curseur_VALUE; Loop_INDEX < d_Gréisst_veränneren; Loop_INDEX++) 명령해석기.Zeil[Loop_INDEX - Curseur_VALUE + 변경전] = 명령해석기.Zeil[Loop_INDEX]; d_Gréisst_veränneren -= Curseur_VALUE - 변경전; Curseur_VALUE = 변경전; }
                다시(); continue;
            }
            if (Byte_Daten == 11) { d_Gréisst_veränneren = Curseur_VALUE; 다시(); continue; }
            if (Byte_Daten < 32 && Byte_Daten != 9) continue;
            if (d_Gréisst_veränneren == 명령해석기.Zeil.length) { Iwwerlaf = true; continue; }
            for (int Loop_INDEX = d_Gréisst_veränneren; Loop_INDEX > Curseur_VALUE; Loop_INDEX--) 명령해석기.Zeil[Loop_INDEX] = 명령해석기.Zeil[Loop_INDEX - 1];
            명령해석기.Zeil[Curseur_VALUE++] = Byte_Daten; d_Gréisst_veränneren++;
            if (Curseur_VALUE == d_Gréisst_veränneren && !가로보기 && 폭(0, d_Gréisst_veränneren) <= 보이는폭()) Board.직렬쓰기(Byte_Daten);
            else if (Curseur_VALUE == d_Gréisst_veränneren) 보이는줄(); else 다시();
        }
    }
}
