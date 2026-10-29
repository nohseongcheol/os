// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 bajt_VALUE 경계를 지키는 삽입/삭제, 방향키, Naredba LOG_zapis, Tab Dovršeno_VALUE. */
public final class uređivač_redaka {
    static boolean naredbeni_redak;
    static int[] LOG_zapis = new int[16 * 1024], 기록길이 = new int[16], Store_VALUE = new int[4096], 후보 = new int[64];
    static int LOG_COUNT, LOG_zapis_završiti_razgovor, Traži_VALUE, 저장길이, Veličina, kursor_VALUE, 후보수, 후보길이, START_prozor;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd sigurno_ljuska udaljeno_zaslon run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String unos_Popis, int START_položaj, int završiti_razgovor_položaj, int 입력길이) {
        int bajt_COUNT=0;
        for(int indeks_položaja=START_položaj;indeks_položaja<završiti_razgovor_položaj;indeks_položaja++) {
            int kodna_točka=unos_Popis.charAt(indeks_položaja);
            if(kodna_točka>=0xd800 && kodna_točka<=0xdbff && indeks_položaja+1<završiti_razgovor_položaj)kodna_točka=0x10000+((kodna_točka-0xd800)<<10)+unos_Popis.charAt(++indeks_položaja)-0xdc00;
            int 수=kodna_točka<128?1:kodna_točka<2048?2:kodna_točka<65536?3:4;
            if(bajt_COUNT+수>62)return;
            for(int SEQUENCE_VALUE=수-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--)명령후보[bajt_COUNT++]=수==1?kodna_točka:SEQUENCE_VALUE==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(kodna_točka>>(6*SEQUENCE_VALUE)):0x80|((kodna_točka>>(6*SEQUENCE_VALUE))&63);
        }
        if(bajt_COUNT<입력길이)return;
        for(int indeks_položaja=0;indeks_položaja<입력길이;indeks_položaja++)if(명령후보[indeks_položaja]!=명령해석기.red[indeks_položaja])return;
        후보수++;후보길이=bajt_COUNT+1;
        for(int indeks_položaja=0;indeks_položaja<bajt_COUNT;indeks_položaja++)후보[indeks_položaja]=명령후보[indeks_položaja];후보[bajt_COUNT]=' ';
    }
    static int prednja_VALUE(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.red[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int TRAG_VALUE(int 읽는자리) { if (읽는자리 < Veličina) { 읽는자리++; while (읽는자리 < Veličina && (명령해석기.red[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int START_položaj, int odredište_VALUE_INDEX) {
        int 글칸수 = 0;
        for (int Loop_INDEX = START_položaj; Loop_INDEX < odredište_VALUE_INDEX; Loop_INDEX++) { int bajt_podaci = 명령해석기.red[Loop_INDEX]; if ((bajt_podaci & 192) == 128) continue; 글칸수 += bajt_podaci >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void pokušati_ponovno_VALUE() {
        단말.Zapisuj("\r\u001b[2K");
        단말.Zapisuj(naredbeni_redak ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 red 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int COLUMNS = pano.Terminal(13) & 65535; return COLUMNS - (naredbeni_redak ? 18 : 9); }
    static void 보이는줄() {
        if (kursor_VALUE < START_prozor) START_prozor = kursor_VALUE;
        while (폭(START_prozor, kursor_VALUE) > 보이는폭()) START_prozor = TRAG_VALUE(START_prozor);
        int završiti_razgovor_položaj = START_prozor;
        while (završiti_razgovor_položaj < Veličina && 폭(START_prozor, TRAG_VALUE(završiti_razgovor_položaj)) <= 보이는폭()) završiti_razgovor_položaj = TRAG_VALUE(završiti_razgovor_položaj);
        단말.Zapisuj("\r\u001b["); 단말.수(naredbeni_redak ? 16 : 7); 단말.Zapisuj("G\u001b[K");
        if (START_prozor > 0) 단말.문자('<');
        for (int Loop_INDEX = START_prozor; Loop_INDEX < završiti_razgovor_položaj; Loop_INDEX++) pano.직렬쓰기(명령해석기.red[Loop_INDEX]);
        단말.문자(završiti_razgovor_položaj < Veličina ? '>' : ' ');
        단말.Zapisuj("\u001b["); 단말.수(폭(kursor_VALUE, završiti_razgovor_položaj) + 1); 단말.문자('D');
        가로보기 = START_prozor > 0 || završiti_razgovor_položaj < Veličina || 폭(0, Veličina) > 보이는폭();
    }
    static void dodati_LOG() {
        if (!naredbeni_redak || Veličina == 0 || Veličina > 1024) return;
        if (LOG_COUNT > 0) {
            int 마지막자리 = (LOG_zapis_završiti_razgovor + 15) % 16; boolean 같은여부 = 기록길이[마지막자리] == Veličina;
            for (int Loop_INDEX = 0; 같은여부 && Loop_INDEX < Veličina; Loop_INDEX++) if (LOG_zapis[마지막자리 * 1024 + Loop_INDEX] != 명령해석기.red[Loop_INDEX]) 같은여부 = false;
            if (같은여부) return;
        }
        기록길이[LOG_zapis_završiti_razgovor] = Veličina; for (int Loop_INDEX = 0; Loop_INDEX < Veličina; Loop_INDEX++) LOG_zapis[LOG_zapis_završiti_razgovor * 1024 + Loop_INDEX] = 명령해석기.red[Loop_INDEX];
        LOG_zapis_završiti_razgovor = (LOG_zapis_završiti_razgovor + 1) % 16; if (LOG_COUNT < 16) LOG_COUNT++;
    }
    static void 기록이동(int DELTA_VALUE) {
        if (!naredbeni_redak) return;
        if (Traži_VALUE == 0 && DELTA_VALUE > 0) { 저장길이 = Veličina; for (int Loop_INDEX = 0; Loop_INDEX < Veličina; Loop_INDEX++) Store_VALUE[Loop_INDEX] = 명령해석기.red[Loop_INDEX]; }
        int Dalje_položaj = Traži_VALUE + DELTA_VALUE; if (Dalje_položaj < 0 || Dalje_položaj > LOG_COUNT) return; Traži_VALUE = Dalje_položaj;
        if (Traži_VALUE == 0) { Veličina = 저장길이; for (int Loop_INDEX = 0; Loop_INDEX < Veličina; Loop_INDEX++) 명령해석기.red[Loop_INDEX] = Store_VALUE[Loop_INDEX]; }
        else { int 보관칸 = (LOG_zapis_završiti_razgovor + 16 - Traži_VALUE) % 16; Veličina = 기록길이[보관칸]; for (int Loop_INDEX = 0; Loop_INDEX < Veličina; Loop_INDEX++) 명령해석기.red[Loop_INDEX] = LOG_zapis[보관칸 * 1024 + Loop_INDEX]; }
        kursor_VALUE = Veličina; pokušati_ponovno_VALUE();
    }
    static void emisija_LOG() {
        for (int unos_COUNT = 0; unos_COUNT < LOG_COUNT; unos_COUNT++) {
            int 보관칸 = (LOG_zapis_završiti_razgovor + 16 - LOG_COUNT + unos_COUNT) % 16; 단말.수(unos_COUNT + 1); 단말.Zapisuj("  ");
            for (int Loop_INDEX = 0; Loop_INDEX < 기록길이[보관칸]; Loop_INDEX++) pano.직렬쓰기(LOG_zapis[보관칸 * 1024 + Loop_INDEX]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] podaci_ARRAY, int START_položaj, int unos_COUNT, int 접두말, int ukupni_zbroj_COUNT, boolean 폴더번호) {
        if (unos_COUNT < ukupni_zbroj_COUNT || unos_COUNT > 62) return;
        for (int Loop_INDEX = 0; Loop_INDEX < ukupni_zbroj_COUNT; Loop_INDEX++) if (podaci_ARRAY[START_položaj + Loop_INDEX] != 명령해석기.red[접두말 + Loop_INDEX]) return;
        후보수++; 후보길이 = unos_COUNT + 1;
        for (int Loop_INDEX = 0; Loop_INDEX < unos_COUNT; Loop_INDEX++) 후보[Loop_INDEX] = podaci_ARRAY[START_položaj + Loop_INDEX]; 후보[unos_COUNT] = 폴더번호 ? '/' : ' ';
    }
    static void Dovršeno_VALUE() {
        if (!naredbeni_redak || kursor_VALUE != Veličina) return;
        int 시작점 = Veličina; while (시작점 > 0 && 명령해석기.red[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDEX = 시작점; Loop_INDEX < Veličina; Loop_INDEX++) if (명령해석기.red[Loop_INDEX] == '/' || 명령해석기.red[Loop_INDEX] == '"' || 명령해석기.red[Loop_INDEX] == 39 || 명령해석기.red[Loop_INDEX] == '\\') return;
        후보수 = 0; int unos_COUNT = Veličina - 시작점;
        if (시작점 == 0) {
            for(int indeks_popisa=0;indeks_popisa<2;indeks_popisa++) {
                String unos_Popis=indeks_popisa==0?명령들:관리명령.Dovršeno_Word();
                int 읽는자리=0;
                while(읽는자리<unos_Popis.length()) {
                    int završiti_razgovor_položaj=읽는자리;while(završiti_razgovor_položaj<unos_Popis.length() && unos_Popis.charAt(završiti_razgovor_položaj)!=' ')završiti_razgovor_položaj++;
                    명령후보넣기(unos_Popis,읽는자리,završiti_razgovor_položaj,unos_COUNT);읽는자리=završiti_razgovor_položaj+1;
                }
            }
        } else {
            Memorija_Datoteke.put_START(1); Memorija_Datoteke.put_bajt(0, '.'); Memorija_Datoteke.normalizirati_VALUE();
            for (int Loop_INDEX = 0; Loop_INDEX < Memorija_Datoteke.Datoteka_COUNT; Loop_INDEX++) {
                int START_položaj = Memorija_Datoteke.unos_START(Memorija_Datoteke.Ime, Loop_INDEX * 64, Memorija_Datoteke.이름길이[Loop_INDEX]);
                if (START_položaj >= 0) 후보넣기(Memorija_Datoteke.Ime, Loop_INDEX * 64 + START_položaj, Memorija_Datoteke.이름길이[Loop_INDEX] - START_položaj, 시작점, unos_COUNT, false);
            }
            for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
                int START_položaj = Memorija_Datoteke.unos_START(Memorija_Datoteke.imenik_naziv, Loop_INDEX * 64, Memorija_Datoteke.폴더길이[Loop_INDEX]);
                if (START_položaj >= 0) 후보넣기(Memorija_Datoteke.imenik_naziv, Loop_INDEX * 64 + START_položaj, Memorija_Datoteke.폴더길이[Loop_INDEX] - START_položaj, 시작점, unos_COUNT, true);
            }
        }
        if (후보수 != 1) { pano.직렬쓰기(7); return; }
        for (int Loop_INDEX = unos_COUNT; Loop_INDEX < 후보길이 && Veličina < 명령해석기.red.length - 1; Loop_INDEX++) {
            if (후보[Loop_INDEX] == ' ' && Loop_INDEX != 후보길이 - 1) 명령해석기.red[Veličina++] = '\\';
            명령해석기.red[Veličina++] = 후보[Loop_INDEX];
        }
        kursor_VALUE = Veličina; pokušati_ponovno_VALUE();
    }
    static int 탈출읽기() {
        int 시작점 = pano.밀리초();
        while (pano.밀리초() - 시작점 < 80) { int bajt_podaci = pano.직렬읽기(); if (bajt_podaci >= 0) return bajt_podaci; pano.YIELD_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int unos_COUNT = 0, završiti_razgovor_položaj = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 12; Loop_INDEX++) { int bajt_podaci = 탈출읽기(); if (bajt_podaci < 0) return; if (bajt_podaci >= '0' && bajt_podaci <= '9') unos_COUNT = unos_COUNT * 10 + bajt_podaci - '0'; else { završiti_razgovor_položaj = bajt_podaci; break; } }
        if (završiti_razgovor_položaj == 'A') 기록이동(1);
        else if (završiti_razgovor_položaj == 'B') 기록이동(-1);
        else if (završiti_razgovor_položaj == 'C') { kursor_VALUE = TRAG_VALUE(kursor_VALUE); pokušati_ponovno_VALUE(); }
        else if (završiti_razgovor_položaj == 'D') { kursor_VALUE = prednja_VALUE(kursor_VALUE); pokušati_ponovno_VALUE(); }
        else if (završiti_razgovor_položaj == 'H' || završiti_razgovor_položaj == '~' && (unos_COUNT == 1 || unos_COUNT == 7)) { kursor_VALUE = 0; pokušati_ponovno_VALUE(); }
        else if (završiti_razgovor_položaj == 'F' || završiti_razgovor_položaj == '~' && (unos_COUNT == 4 || unos_COUNT == 8)) { kursor_VALUE = Veličina; pokušati_ponovno_VALUE(); }
        else if (završiti_razgovor_položaj == '~' && unos_COUNT == 3 && kursor_VALUE < Veličina) {
            int Dalje_položaj = TRAG_VALUE(kursor_VALUE); for (int Loop_INDEX = Dalje_položaj; Loop_INDEX < Veličina; Loop_INDEX++) 명령해석기.red[Loop_INDEX - Dalje_položaj + kursor_VALUE] = 명령해석기.red[Loop_INDEX]; Veličina -= Dalje_položaj - kursor_VALUE; pokušati_ponovno_VALUE();
        }
        else if (završiti_razgovor_položaj == '~' && (unos_COUNT == 5 || unos_COUNT == 6)) pano.Terminal(unos_COUNT == 5 ? 5 : 6);
        else if (završiti_razgovor_položaj == '~' && unos_COUNT == 24 && naredbeni_redak) { 명령해석기.Terminal(true); }
    }
    static int Čitaj() {
        if (!prozor_sesija.이어읽기) { Veličina = kursor_VALUE = Traži_VALUE = START_prozor = 0; 가로보기 = false; }
        else { prozor_sesija.이어읽기 = false; pokušati_ponovno_VALUE(); } boolean preljev = false;
        while (true) {
            int bajt_podaci = pano.직렬읽기(); if (bajt_podaci == -4096) return -3;
            if (pano.Terminal(14) != 0) pokušati_ponovno_VALUE(); if (bajt_podaci < 0) { pano.YIELD_CPU(); continue; }
            if (bajt_podaci == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = bajt_podaci == 13;
            if (bajt_podaci == 27) { 탈출(); continue; }
            if (bajt_podaci == 3) { 단말.Zapisuj("^C\n"); return -1; }
            if (bajt_podaci == 4 && Veličina == 0 && naredbeni_redak) { if (pano.Terminal(2) != 0) 명령해석기.Terminal(true); return -1; }
            if (bajt_podaci == 13 || bajt_podaci == 10) { 단말.문자(10); if (!preljev) dodati_LOG(); return preljev ? -2 : Veličina; }
            if (bajt_podaci == 9 && naredbeni_redak) { Dovršeno_VALUE(); continue; }
            if (bajt_podaci == 1 || bajt_podaci == 5) { kursor_VALUE = bajt_podaci == 1 ? 0 : Veličina; pokušati_ponovno_VALUE(); continue; }
            if (bajt_podaci == 8 || bajt_podaci == 127 || bajt_podaci == 21) {
                if (bajt_podaci == 21) { for (int Loop_INDEX = kursor_VALUE; Loop_INDEX < Veličina; Loop_INDEX++) 명령해석기.red[Loop_INDEX - kursor_VALUE] = 명령해석기.red[Loop_INDEX]; Veličina -= kursor_VALUE; kursor_VALUE = 0; }
                else if (kursor_VALUE > 0) { int 변경전 = prednja_VALUE(kursor_VALUE); for (int Loop_INDEX = kursor_VALUE; Loop_INDEX < Veličina; Loop_INDEX++) 명령해석기.red[Loop_INDEX - kursor_VALUE + 변경전] = 명령해석기.red[Loop_INDEX]; Veličina -= kursor_VALUE - 변경전; kursor_VALUE = 변경전; }
                pokušati_ponovno_VALUE(); continue;
            }
            if (bajt_podaci == 11) { Veličina = kursor_VALUE; pokušati_ponovno_VALUE(); continue; }
            if (bajt_podaci < 32 && bajt_podaci != 9) continue;
            if (Veličina == 명령해석기.red.length) { preljev = true; continue; }
            for (int Loop_INDEX = Veličina; Loop_INDEX > kursor_VALUE; Loop_INDEX--) 명령해석기.red[Loop_INDEX] = 명령해석기.red[Loop_INDEX - 1];
            명령해석기.red[kursor_VALUE++] = bajt_podaci; Veličina++;
            if (kursor_VALUE == Veličina && !가로보기 && 폭(0, Veličina) <= 보이는폭()) pano.직렬쓰기(bajt_podaci);
            else if (kursor_VALUE == Veličina) 보이는줄(); else pokušati_ponovno_VALUE();
        }
    }
}
