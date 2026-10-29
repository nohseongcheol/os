// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 bajt_VALUE 경계를 지키는 삽입/삭제, 방향키, Naredba LOG_red, Tab 완성. */
public final class redak_urednik {
    static boolean komandni_red;
    static int[] LOG_red = new int[16 * 1024], LOG_dužina = new int[16], Store_VALUE = new int[4096], 후보 = new int[64];
    static int LOG_COUNT, LOG_red_završiti, Traži_VALUE, 저장길이, Veličina, kursor_VALUE, 후보수, 후보길이, START_prozor;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd sigurno_ljuska udaljeno_ekran run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String unos_spisak, int START_položaj, int završiti_položaj, int 입력길이) {
        int bajt_COUNT=0;
        for(int položaj_INDEX=START_položaj;položaj_INDEX<završiti_položaj;položaj_INDEX++) {
            int kôd_znaka=unos_spisak.charAt(položaj_INDEX);
            if(kôd_znaka>=0xd800 && kôd_znaka<=0xdbff && položaj_INDEX+1<završiti_položaj)kôd_znaka=0x10000+((kôd_znaka-0xd800)<<10)+unos_spisak.charAt(++položaj_INDEX)-0xdc00;
            int 수=kôd_znaka<128?1:kôd_znaka<2048?2:kôd_znaka<65536?3:4;
            if(bajt_COUNT+수>62)return;
            for(int SEQUENCE_VALUE=수-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--)명령후보[bajt_COUNT++]=수==1?kôd_znaka:SEQUENCE_VALUE==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(kôd_znaka>>(6*SEQUENCE_VALUE)):0x80|((kôd_znaka>>(6*SEQUENCE_VALUE))&63);
        }
        if(bajt_COUNT<입력길이)return;
        for(int položaj_INDEX=0;položaj_INDEX<입력길이;položaj_INDEX++)if(명령후보[položaj_INDEX]!=명령해석기.Linija[položaj_INDEX])return;
        후보수++;후보길이=bajt_COUNT+1;
        for(int položaj_INDEX=0;položaj_INDEX<bajt_COUNT;položaj_INDEX++)후보[položaj_INDEX]=명령후보[položaj_INDEX];후보[bajt_COUNT]=' ';
    }
    static int 앞(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.Linija[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int ZAD_VALUE(int 읽는자리) { if (읽는자리 < Veličina) { 읽는자리++; while (읽는자리 < Veličina && (명령해석기.Linija[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int START_položaj, int odredište_VALUE_INDEX) {
        int 글칸수 = 0;
        for (int Loop_INDEX = START_položaj; Loop_INDEX < odredište_VALUE_INDEX; Loop_INDEX++) { int bajt_podaci = 명령해석기.Linija[Loop_INDEX]; if ((bajt_podaci & 192) == 128) continue; 글칸수 += bajt_podaci >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.Piši("\r\u001b[2K");
        단말.Piši(komandni_red ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 Linija 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int Kolone = ploča.Terminal(13) & 65535; return Kolone - (komandni_red ? 18 : 9); }
    static void 보이는줄() {
        if (kursor_VALUE < START_prozor) START_prozor = kursor_VALUE;
        while (폭(START_prozor, kursor_VALUE) > 보이는폭()) START_prozor = ZAD_VALUE(START_prozor);
        int završiti_položaj = START_prozor;
        while (završiti_položaj < Veličina && 폭(START_prozor, ZAD_VALUE(završiti_položaj)) <= 보이는폭()) završiti_položaj = ZAD_VALUE(završiti_položaj);
        단말.Piši("\r\u001b["); 단말.수(komandni_red ? 16 : 7); 단말.Piši("G\u001b[K");
        if (START_prozor > 0) 단말.문자('<');
        for (int Loop_INDEX = START_prozor; Loop_INDEX < završiti_položaj; Loop_INDEX++) ploča.직렬쓰기(명령해석기.Linija[Loop_INDEX]);
        단말.문자(završiti_položaj < Veličina ? '>' : ' ');
        단말.Piši("\u001b["); 단말.수(폭(kursor_VALUE, završiti_položaj) + 1); 단말.문자('D');
        가로보기 = START_prozor > 0 || završiti_položaj < Veličina || 폭(0, Veličina) > 보이는폭();
    }
    static void 기록넣기() {
        if (!komandni_red || Veličina == 0 || Veličina > 1024) return;
        if (LOG_COUNT > 0) {
            int 마지막자리 = (LOG_red_završiti + 15) % 16; boolean 같은여부 = LOG_dužina[마지막자리] == Veličina;
            for (int Loop_INDEX = 0; 같은여부 && Loop_INDEX < Veličina; Loop_INDEX++) if (LOG_red[마지막자리 * 1024 + Loop_INDEX] != 명령해석기.Linija[Loop_INDEX]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_dužina[LOG_red_završiti] = Veličina; for (int Loop_INDEX = 0; Loop_INDEX < Veličina; Loop_INDEX++) LOG_red[LOG_red_završiti * 1024 + Loop_INDEX] = 명령해석기.Linija[Loop_INDEX];
        LOG_red_završiti = (LOG_red_završiti + 1) % 16; if (LOG_COUNT < 16) LOG_COUNT++;
    }
    static void 기록이동(int DELTA_VALUE) {
        if (!komandni_red) return;
        if (Traži_VALUE == 0 && DELTA_VALUE > 0) { 저장길이 = Veličina; for (int Loop_INDEX = 0; Loop_INDEX < Veličina; Loop_INDEX++) Store_VALUE[Loop_INDEX] = 명령해석기.Linija[Loop_INDEX]; }
        int Dalje_položaj = Traži_VALUE + DELTA_VALUE; if (Dalje_položaj < 0 || Dalje_položaj > LOG_COUNT) return; Traži_VALUE = Dalje_položaj;
        if (Traži_VALUE == 0) { Veličina = 저장길이; for (int Loop_INDEX = 0; Loop_INDEX < Veličina; Loop_INDEX++) 명령해석기.Linija[Loop_INDEX] = Store_VALUE[Loop_INDEX]; }
        else { int 보관칸 = (LOG_red_završiti + 16 - Traži_VALUE) % 16; Veličina = LOG_dužina[보관칸]; for (int Loop_INDEX = 0; Loop_INDEX < Veličina; Loop_INDEX++) 명령해석기.Linija[Loop_INDEX] = LOG_red[보관칸 * 1024 + Loop_INDEX]; }
        kursor_VALUE = Veličina; 다시();
    }
    static void program_LOG() {
        for (int unos_COUNT = 0; unos_COUNT < LOG_COUNT; unos_COUNT++) {
            int 보관칸 = (LOG_red_završiti + 16 - LOG_COUNT + unos_COUNT) % 16; 단말.수(unos_COUNT + 1); 단말.Piši("  ");
            for (int Loop_INDEX = 0; Loop_INDEX < LOG_dužina[보관칸]; Loop_INDEX++) ploča.직렬쓰기(LOG_red[보관칸 * 1024 + Loop_INDEX]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] podaci_niz, int START_položaj, int unos_COUNT, int 접두말, int 총수, boolean 폴더번호) {
        if (unos_COUNT < 총수 || unos_COUNT > 62) return;
        for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) if (podaci_niz[START_položaj + Loop_INDEX] != 명령해석기.Linija[접두말 + Loop_INDEX]) return;
        후보수++; 후보길이 = unos_COUNT + 1;
        for (int Loop_INDEX = 0; Loop_INDEX < unos_COUNT; Loop_INDEX++) 후보[Loop_INDEX] = podaci_niz[START_položaj + Loop_INDEX]; 후보[unos_COUNT] = 폴더번호 ? '/' : ' ';
    }
    static void 완성() {
        if (!komandni_red || kursor_VALUE != Veličina) return;
        int 시작점 = Veličina; while (시작점 > 0 && 명령해석기.Linija[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDEX = 시작점; Loop_INDEX < Veličina; Loop_INDEX++) if (명령해석기.Linija[Loop_INDEX] == '/' || 명령해석기.Linija[Loop_INDEX] == '"' || 명령해석기.Linija[Loop_INDEX] == 39 || 명령해석기.Linija[Loop_INDEX] == '\\') return;
        후보수 = 0; int unos_COUNT = Veličina - 시작점;
        if (시작점 == 0) {
            for(int spisak_INDEX=0;spisak_INDEX<2;spisak_INDEX++) {
                String unos_spisak=spisak_INDEX==0?명령들:관리명령.완성어();
                int 읽는자리=0;
                while(읽는자리<unos_spisak.length()) {
                    int završiti_položaj=읽는자리;while(završiti_položaj<unos_spisak.length() && unos_spisak.charAt(završiti_položaj)!=' ')završiti_položaj++;
                    명령후보넣기(unos_spisak,읽는자리,završiti_položaj,unos_COUNT);읽는자리=završiti_položaj+1;
                }
            }
        } else {
            Memorija_Fajlovi.put_START(1); Memorija_Fajlovi.put_bajt(0, '.'); Memorija_Fajlovi.normalizirati_VALUE();
            for (int Loop_INDEX = 0; Loop_INDEX < Memorija_Fajlovi.fajl_COUNT; Loop_INDEX++) {
                int START_položaj = Memorija_Fajlovi.unos_START(Memorija_Fajlovi.Naziv, Loop_INDEX * 64, Memorija_Fajlovi.이름길이[Loop_INDEX]);
                if (START_položaj >= 0) 후보넣기(Memorija_Fajlovi.Naziv, Loop_INDEX * 64 + START_položaj, Memorija_Fajlovi.이름길이[Loop_INDEX] - START_položaj, 시작점, unos_COUNT, false);
            }
            for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
                int START_položaj = Memorija_Fajlovi.unos_START(Memorija_Fajlovi.Direktorij_naziv, Loop_INDEX * 64, Memorija_Fajlovi.Direktorij_dužina[Loop_INDEX]);
                if (START_položaj >= 0) 후보넣기(Memorija_Fajlovi.Direktorij_naziv, Loop_INDEX * 64 + START_položaj, Memorija_Fajlovi.Direktorij_dužina[Loop_INDEX] - START_položaj, 시작점, unos_COUNT, true);
            }
        }
        if (후보수 != 1) { ploča.직렬쓰기(7); return; }
        for (int Loop_INDEX = unos_COUNT; Loop_INDEX < 후보길이 && Veličina < 명령해석기.Linija.length - 1; Loop_INDEX++) {
            if (후보[Loop_INDEX] == ' ' && Loop_INDEX != 후보길이 - 1) 명령해석기.Linija[Veličina++] = '\\';
            명령해석기.Linija[Veličina++] = 후보[Loop_INDEX];
        }
        kursor_VALUE = Veličina; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = ploča.밀리초();
        while (ploča.밀리초() - 시작점 < 80) { int bajt_podaci = ploča.직렬읽기(); if (bajt_podaci >= 0) return bajt_podaci; ploča.YIELD_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int unos_COUNT = 0, završiti_položaj = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 12; Loop_INDEX++) { int bajt_podaci = 탈출읽기(); if (bajt_podaci < 0) return; if (bajt_podaci >= '0' && bajt_podaci <= '9') unos_COUNT = unos_COUNT * 10 + bajt_podaci - '0'; else { završiti_položaj = bajt_podaci; break; } }
        if (završiti_položaj == 'A') 기록이동(1);
        else if (završiti_položaj == 'B') 기록이동(-1);
        else if (završiti_položaj == 'C') { kursor_VALUE = ZAD_VALUE(kursor_VALUE); 다시(); }
        else if (završiti_položaj == 'D') { kursor_VALUE = 앞(kursor_VALUE); 다시(); }
        else if (završiti_položaj == 'H' || završiti_položaj == '~' && (unos_COUNT == 1 || unos_COUNT == 7)) { kursor_VALUE = 0; 다시(); }
        else if (završiti_položaj == 'F' || završiti_položaj == '~' && (unos_COUNT == 4 || unos_COUNT == 8)) { kursor_VALUE = Veličina; 다시(); }
        else if (završiti_položaj == '~' && unos_COUNT == 3 && kursor_VALUE < Veličina) {
            int Dalje_položaj = ZAD_VALUE(kursor_VALUE); for (int Loop_INDEX = Dalje_položaj; Loop_INDEX < Veličina; Loop_INDEX++) 명령해석기.Linija[Loop_INDEX - Dalje_položaj + kursor_VALUE] = 명령해석기.Linija[Loop_INDEX]; Veličina -= Dalje_položaj - kursor_VALUE; 다시();
        }
        else if (završiti_položaj == '~' && (unos_COUNT == 5 || unos_COUNT == 6)) ploča.Terminal(unos_COUNT == 5 ? 5 : 6);
        else if (završiti_položaj == '~' && unos_COUNT == 24 && komandni_red) { 명령해석기.Terminal(true); }
    }
    static int Čitaj() {
        if (!prozor_sesija.이어읽기) { Veličina = kursor_VALUE = Traži_VALUE = START_prozor = 0; 가로보기 = false; }
        else { prozor_sesija.이어읽기 = false; 다시(); } boolean prelijevanje = false;
        while (true) {
            int bajt_podaci = ploča.직렬읽기(); if (bajt_podaci == -4096) return -3;
            if (ploča.Terminal(14) != 0) 다시(); if (bajt_podaci < 0) { ploča.YIELD_CPU(); continue; }
            if (bajt_podaci == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = bajt_podaci == 13;
            if (bajt_podaci == 27) { 탈출(); continue; }
            if (bajt_podaci == 3) { 단말.Piši("^C\n"); return -1; }
            if (bajt_podaci == 4 && Veličina == 0 && komandni_red) { if (ploča.Terminal(2) != 0) 명령해석기.Terminal(true); return -1; }
            if (bajt_podaci == 13 || bajt_podaci == 10) { 단말.문자(10); if (!prelijevanje) 기록넣기(); return prelijevanje ? -2 : Veličina; }
            if (bajt_podaci == 9 && komandni_red) { 완성(); continue; }
            if (bajt_podaci == 1 || bajt_podaci == 5) { kursor_VALUE = bajt_podaci == 1 ? 0 : Veličina; 다시(); continue; }
            if (bajt_podaci == 8 || bajt_podaci == 127 || bajt_podaci == 21) {
                if (bajt_podaci == 21) { for (int Loop_INDEX = kursor_VALUE; Loop_INDEX < Veličina; Loop_INDEX++) 명령해석기.Linija[Loop_INDEX - kursor_VALUE] = 명령해석기.Linija[Loop_INDEX]; Veličina -= kursor_VALUE; kursor_VALUE = 0; }
                else if (kursor_VALUE > 0) { int 변경전 = 앞(kursor_VALUE); for (int Loop_INDEX = kursor_VALUE; Loop_INDEX < Veličina; Loop_INDEX++) 명령해석기.Linija[Loop_INDEX - kursor_VALUE + 변경전] = 명령해석기.Linija[Loop_INDEX]; Veličina -= kursor_VALUE - 변경전; kursor_VALUE = 변경전; }
                다시(); continue;
            }
            if (bajt_podaci == 11) { Veličina = kursor_VALUE; 다시(); continue; }
            if (bajt_podaci < 32 && bajt_podaci != 9) continue;
            if (Veličina == 명령해석기.Linija.length) { prelijevanje = true; continue; }
            for (int Loop_INDEX = Veličina; Loop_INDEX > kursor_VALUE; Loop_INDEX--) 명령해석기.Linija[Loop_INDEX] = 명령해석기.Linija[Loop_INDEX - 1];
            명령해석기.Linija[kursor_VALUE++] = bajt_podaci; Veličina++;
            if (kursor_VALUE == Veličina && !가로보기 && 폭(0, Veličina) <= 보이는폭()) ploča.직렬쓰기(bajt_podaci);
            else if (kursor_VALUE == Veličina) 보이는줄(); else 다시();
        }
    }
}
