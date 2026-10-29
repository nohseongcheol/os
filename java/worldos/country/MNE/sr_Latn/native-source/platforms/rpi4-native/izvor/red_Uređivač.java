// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 bajt_VALUE 경계를 지키는 삽입/삭제, 방향키, komanda LOG_snimi, Tab Dovršeno_VALUE. */
public final class red_Uređivač {
    static boolean komandna_linija;
    static int[] LOG_snimi = new int[16 * 1024], 기록길이 = new int[16], Store_VALUE = new int[4096], 후보 = new int[64];
    static int LOG_COUNT, LOG_snimi_završiti_razgovor, SEARCH_VALUE, 저장길이, promeniti_veličinu, kursor_VALUE, 후보수, 후보길이, START_prozor;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd bezbedan_ljuska udaljen_ekran run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String stavka_Lista, int START_pozicija, int završiti_razgovor_pozicija, int 입력길이) {
        int bajt_COUNT=0;
        for(int indeks_pozicije=START_pozicija;indeks_pozicije<završiti_razgovor_pozicija;indeks_pozicije++) {
            int kôd_znaka=stavka_Lista.charAt(indeks_pozicije);
            if(kôd_znaka>=0xd800 && kôd_znaka<=0xdbff && indeks_pozicije+1<završiti_razgovor_pozicija)kôd_znaka=0x10000+((kôd_znaka-0xd800)<<10)+stavka_Lista.charAt(++indeks_pozicije)-0xdc00;
            int 수=kôd_znaka<128?1:kôd_znaka<2048?2:kôd_znaka<65536?3:4;
            if(bajt_COUNT+수>62)return;
            for(int SEQUENCE_VALUE=수-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--)명령후보[bajt_COUNT++]=수==1?kôd_znaka:SEQUENCE_VALUE==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(kôd_znaka>>(6*SEQUENCE_VALUE)):0x80|((kôd_znaka>>(6*SEQUENCE_VALUE))&63);
        }
        if(bajt_COUNT<입력길이)return;
        for(int indeks_pozicije=0;indeks_pozicije<입력길이;indeks_pozicije++)if(명령후보[indeks_pozicije]!=명령해석기.red[indeks_pozicije])return;
        후보수++;후보길이=bajt_COUNT+1;
        for(int indeks_pozicije=0;indeks_pozicije<bajt_COUNT;indeks_pozicije++)후보[indeks_pozicije]=명령후보[indeks_pozicije];후보[bajt_COUNT]=' ';
    }
    static int čeona_kamera_VALUE(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.red[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int NAZAD_VALUE(int 읽는자리) { if (읽는자리 < promeniti_veličinu) { 읽는자리++; while (읽는자리 < promeniti_veličinu && (명령해석기.red[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int START_pozicija, int odredište_VALUE_INDEX) {
        int 글칸수 = 0;
        for (int Loop_INDEX = START_pozicija; Loop_INDEX < odredište_VALUE_INDEX; Loop_INDEX++) { int bajt_podaci = 명령해석기.red[Loop_INDEX]; if ((bajt_podaci & 192) == 128) continue; 글칸수 += bajt_podaci >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void pokušati_ponovo_VALUE() {
        단말.쓰기("\r\u001b[2K");
        단말.쓰기(komandna_linija ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 red 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int COLUMNS = Tabla.Terminal(13) & 65535; return COLUMNS - (komandna_linija ? 18 : 9); }
    static void 보이는줄() {
        if (kursor_VALUE < START_prozor) START_prozor = kursor_VALUE;
        while (폭(START_prozor, kursor_VALUE) > 보이는폭()) START_prozor = NAZAD_VALUE(START_prozor);
        int završiti_razgovor_pozicija = START_prozor;
        while (završiti_razgovor_pozicija < promeniti_veličinu && 폭(START_prozor, NAZAD_VALUE(završiti_razgovor_pozicija)) <= 보이는폭()) završiti_razgovor_pozicija = NAZAD_VALUE(završiti_razgovor_pozicija);
        단말.쓰기("\r\u001b["); 단말.수(komandna_linija ? 16 : 7); 단말.쓰기("G\u001b[K");
        if (START_prozor > 0) 단말.문자('<');
        for (int Loop_INDEX = START_prozor; Loop_INDEX < završiti_razgovor_pozicija; Loop_INDEX++) Tabla.직렬쓰기(명령해석기.red[Loop_INDEX]);
        단말.문자(završiti_razgovor_pozicija < promeniti_veličinu ? '>' : ' ');
        단말.쓰기("\u001b["); 단말.수(폭(kursor_VALUE, završiti_razgovor_pozicija) + 1); 단말.문자('D');
        가로보기 = START_prozor > 0 || završiti_razgovor_pozicija < promeniti_veličinu || 폭(0, promeniti_veličinu) > 보이는폭();
    }
    static void dodati_LOG() {
        if (!komandna_linija || promeniti_veličinu == 0 || promeniti_veličinu > 1024) return;
        if (LOG_COUNT > 0) {
            int 마지막자리 = (LOG_snimi_završiti_razgovor + 15) % 16; boolean 같은여부 = 기록길이[마지막자리] == promeniti_veličinu;
            for (int Loop_INDEX = 0; 같은여부 && Loop_INDEX < promeniti_veličinu; Loop_INDEX++) if (LOG_snimi[마지막자리 * 1024 + Loop_INDEX] != 명령해석기.red[Loop_INDEX]) 같은여부 = false;
            if (같은여부) return;
        }
        기록길이[LOG_snimi_završiti_razgovor] = promeniti_veličinu; for (int Loop_INDEX = 0; Loop_INDEX < promeniti_veličinu; Loop_INDEX++) LOG_snimi[LOG_snimi_završiti_razgovor * 1024 + Loop_INDEX] = 명령해석기.red[Loop_INDEX];
        LOG_snimi_završiti_razgovor = (LOG_snimi_završiti_razgovor + 1) % 16; if (LOG_COUNT < 16) LOG_COUNT++;
    }
    static void 기록이동(int DELTA_VALUE) {
        if (!komandna_linija) return;
        if (SEARCH_VALUE == 0 && DELTA_VALUE > 0) { 저장길이 = promeniti_veličinu; for (int Loop_INDEX = 0; Loop_INDEX < promeniti_veličinu; Loop_INDEX++) Store_VALUE[Loop_INDEX] = 명령해석기.red[Loop_INDEX]; }
        int Dalje_pozicija = SEARCH_VALUE + DELTA_VALUE; if (Dalje_pozicija < 0 || Dalje_pozicija > LOG_COUNT) return; SEARCH_VALUE = Dalje_pozicija;
        if (SEARCH_VALUE == 0) { promeniti_veličinu = 저장길이; for (int Loop_INDEX = 0; Loop_INDEX < promeniti_veličinu; Loop_INDEX++) 명령해석기.red[Loop_INDEX] = Store_VALUE[Loop_INDEX]; }
        else { int 보관칸 = (LOG_snimi_završiti_razgovor + 16 - SEARCH_VALUE) % 16; promeniti_veličinu = 기록길이[보관칸]; for (int Loop_INDEX = 0; Loop_INDEX < promeniti_veličinu; Loop_INDEX++) 명령해석기.red[Loop_INDEX] = LOG_snimi[보관칸 * 1024 + Loop_INDEX]; }
        kursor_VALUE = promeniti_veličinu; pokušati_ponovo_VALUE();
    }
    static void emisija_LOG() {
        for (int stavka_COUNT_8f7753a1 = 0; stavka_COUNT_8f7753a1 < LOG_COUNT; stavka_COUNT_8f7753a1++) {
            int 보관칸 = (LOG_snimi_završiti_razgovor + 16 - LOG_COUNT + stavka_COUNT_8f7753a1) % 16; 단말.수(stavka_COUNT_8f7753a1 + 1); 단말.쓰기("  ");
            for (int Loop_INDEX = 0; Loop_INDEX < 기록길이[보관칸]; Loop_INDEX++) Tabla.직렬쓰기(LOG_snimi[보관칸 * 1024 + Loop_INDEX]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] podaci_niz, int START_pozicija, int stavka_COUNT_8f7753a1, int 접두말, int ukupan_COUNT, boolean 폴더번호) {
        if (stavka_COUNT_8f7753a1 < ukupan_COUNT || stavka_COUNT_8f7753a1 > 62) return;
        for (int Loop_INDEX = 0; Loop_INDEX < ukupan_COUNT; Loop_INDEX++) if (podaci_niz[START_pozicija + Loop_INDEX] != 명령해석기.red[접두말 + Loop_INDEX]) return;
        후보수++; 후보길이 = stavka_COUNT_8f7753a1 + 1;
        for (int Loop_INDEX = 0; Loop_INDEX < stavka_COUNT_8f7753a1; Loop_INDEX++) 후보[Loop_INDEX] = podaci_niz[START_pozicija + Loop_INDEX]; 후보[stavka_COUNT_8f7753a1] = 폴더번호 ? '/' : ' ';
    }
    static void Dovršeno_VALUE() {
        if (!komandna_linija || kursor_VALUE != promeniti_veličinu) return;
        int 시작점 = promeniti_veličinu; while (시작점 > 0 && 명령해석기.red[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDEX = 시작점; Loop_INDEX < promeniti_veličinu; Loop_INDEX++) if (명령해석기.red[Loop_INDEX] == '/' || 명령해석기.red[Loop_INDEX] == '"' || 명령해석기.red[Loop_INDEX] == 39 || 명령해석기.red[Loop_INDEX] == '\\') return;
        후보수 = 0; int stavka_COUNT_8f7753a1 = promeniti_veličinu - 시작점;
        if (시작점 == 0) {
            for(int indeks_liste=0;indeks_liste<2;indeks_liste++) {
                String stavka_Lista=indeks_liste==0?명령들:관리명령.Dovršeno_Word();
                int 읽는자리=0;
                while(읽는자리<stavka_Lista.length()) {
                    int završiti_razgovor_pozicija=읽는자리;while(završiti_razgovor_pozicija<stavka_Lista.length() && stavka_Lista.charAt(završiti_razgovor_pozicija)!=' ')završiti_razgovor_pozicija++;
                    명령후보넣기(stavka_Lista,읽는자리,završiti_razgovor_pozicija,stavka_COUNT_8f7753a1);읽는자리=završiti_razgovor_pozicija+1;
                }
            }
        } else {
            Memorija_Datoteke.putanja_START(1); Memorija_Datoteke.putanja_bajt(0, '.'); Memorija_Datoteke.normalizovati_VALUE();
            for (int Loop_INDEX = 0; Loop_INDEX < Memorija_Datoteke.Datoteka_COUNT; Loop_INDEX++) {
                int START_pozicija = Memorija_Datoteke.stavka_START(Memorija_Datoteke.ime, Loop_INDEX * 64, Memorija_Datoteke.이름길이[Loop_INDEX]);
                if (START_pozicija >= 0) 후보넣기(Memorija_Datoteke.ime, Loop_INDEX * 64 + START_pozicija, Memorija_Datoteke.이름길이[Loop_INDEX] - START_pozicija, 시작점, stavka_COUNT_8f7753a1, false);
            }
            for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
                int START_pozicija = Memorija_Datoteke.stavka_START(Memorija_Datoteke.Imenik_ime, Loop_INDEX * 64, Memorija_Datoteke.폴더길이[Loop_INDEX]);
                if (START_pozicija >= 0) 후보넣기(Memorija_Datoteke.Imenik_ime, Loop_INDEX * 64 + START_pozicija, Memorija_Datoteke.폴더길이[Loop_INDEX] - START_pozicija, 시작점, stavka_COUNT_8f7753a1, true);
            }
        }
        if (후보수 != 1) { Tabla.직렬쓰기(7); return; }
        for (int Loop_INDEX = stavka_COUNT_8f7753a1; Loop_INDEX < 후보길이 && promeniti_veličinu < 명령해석기.red.length - 1; Loop_INDEX++) {
            if (후보[Loop_INDEX] == ' ' && Loop_INDEX != 후보길이 - 1) 명령해석기.red[promeniti_veličinu++] = '\\';
            명령해석기.red[promeniti_veličinu++] = 후보[Loop_INDEX];
        }
        kursor_VALUE = promeniti_veličinu; pokušati_ponovo_VALUE();
    }
    static int 탈출읽기() {
        int 시작점 = Tabla.밀리초();
        while (Tabla.밀리초() - 시작점 < 80) { int bajt_podaci = Tabla.직렬읽기(); if (bajt_podaci >= 0) return bajt_podaci; Tabla.YIELD_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int stavka_COUNT_8f7753a1 = 0, završiti_razgovor_pozicija = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 12; Loop_INDEX++) { int bajt_podaci = 탈출읽기(); if (bajt_podaci < 0) return; if (bajt_podaci >= '0' && bajt_podaci <= '9') stavka_COUNT_8f7753a1 = stavka_COUNT_8f7753a1 * 10 + bajt_podaci - '0'; else { završiti_razgovor_pozicija = bajt_podaci; break; } }
        if (završiti_razgovor_pozicija == 'A') 기록이동(1);
        else if (završiti_razgovor_pozicija == 'B') 기록이동(-1);
        else if (završiti_razgovor_pozicija == 'C') { kursor_VALUE = NAZAD_VALUE(kursor_VALUE); pokušati_ponovo_VALUE(); }
        else if (završiti_razgovor_pozicija == 'D') { kursor_VALUE = čeona_kamera_VALUE(kursor_VALUE); pokušati_ponovo_VALUE(); }
        else if (završiti_razgovor_pozicija == 'H' || završiti_razgovor_pozicija == '~' && (stavka_COUNT_8f7753a1 == 1 || stavka_COUNT_8f7753a1 == 7)) { kursor_VALUE = 0; pokušati_ponovo_VALUE(); }
        else if (završiti_razgovor_pozicija == 'F' || završiti_razgovor_pozicija == '~' && (stavka_COUNT_8f7753a1 == 4 || stavka_COUNT_8f7753a1 == 8)) { kursor_VALUE = promeniti_veličinu; pokušati_ponovo_VALUE(); }
        else if (završiti_razgovor_pozicija == '~' && stavka_COUNT_8f7753a1 == 3 && kursor_VALUE < promeniti_veličinu) {
            int Dalje_pozicija = NAZAD_VALUE(kursor_VALUE); for (int Loop_INDEX = Dalje_pozicija; Loop_INDEX < promeniti_veličinu; Loop_INDEX++) 명령해석기.red[Loop_INDEX - Dalje_pozicija + kursor_VALUE] = 명령해석기.red[Loop_INDEX]; promeniti_veličinu -= Dalje_pozicija - kursor_VALUE; pokušati_ponovo_VALUE();
        }
        else if (završiti_razgovor_pozicija == '~' && (stavka_COUNT_8f7753a1 == 5 || stavka_COUNT_8f7753a1 == 6)) Tabla.Terminal(stavka_COUNT_8f7753a1 == 5 ? 5 : 6);
        else if (završiti_razgovor_pozicija == '~' && stavka_COUNT_8f7753a1 == 24 && komandna_linija) { 명령해석기.Terminal(true); }
    }
    static int 읽기() {
        if (!prozor_sesija.이어읽기) { promeniti_veličinu = kursor_VALUE = SEARCH_VALUE = START_prozor = 0; 가로보기 = false; }
        else { prozor_sesija.이어읽기 = false; pokušati_ponovo_VALUE(); } boolean višak = false;
        while (true) {
            int bajt_podaci = Tabla.직렬읽기(); if (bajt_podaci == -4096) return -3;
            if (Tabla.Terminal(14) != 0) pokušati_ponovo_VALUE(); if (bajt_podaci < 0) { Tabla.YIELD_CPU(); continue; }
            if (bajt_podaci == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = bajt_podaci == 13;
            if (bajt_podaci == 27) { 탈출(); continue; }
            if (bajt_podaci == 3) { 단말.쓰기("^C\n"); return -1; }
            if (bajt_podaci == 4 && promeniti_veličinu == 0 && komandna_linija) { if (Tabla.Terminal(2) != 0) 명령해석기.Terminal(true); return -1; }
            if (bajt_podaci == 13 || bajt_podaci == 10) { 단말.문자(10); if (!višak) dodati_LOG(); return višak ? -2 : promeniti_veličinu; }
            if (bajt_podaci == 9 && komandna_linija) { Dovršeno_VALUE(); continue; }
            if (bajt_podaci == 1 || bajt_podaci == 5) { kursor_VALUE = bajt_podaci == 1 ? 0 : promeniti_veličinu; pokušati_ponovo_VALUE(); continue; }
            if (bajt_podaci == 8 || bajt_podaci == 127 || bajt_podaci == 21) {
                if (bajt_podaci == 21) { for (int Loop_INDEX = kursor_VALUE; Loop_INDEX < promeniti_veličinu; Loop_INDEX++) 명령해석기.red[Loop_INDEX - kursor_VALUE] = 명령해석기.red[Loop_INDEX]; promeniti_veličinu -= kursor_VALUE; kursor_VALUE = 0; }
                else if (kursor_VALUE > 0) { int 변경전 = čeona_kamera_VALUE(kursor_VALUE); for (int Loop_INDEX = kursor_VALUE; Loop_INDEX < promeniti_veličinu; Loop_INDEX++) 명령해석기.red[Loop_INDEX - kursor_VALUE + 변경전] = 명령해석기.red[Loop_INDEX]; promeniti_veličinu -= kursor_VALUE - 변경전; kursor_VALUE = 변경전; }
                pokušati_ponovo_VALUE(); continue;
            }
            if (bajt_podaci == 11) { promeniti_veličinu = kursor_VALUE; pokušati_ponovo_VALUE(); continue; }
            if (bajt_podaci < 32 && bajt_podaci != 9) continue;
            if (promeniti_veličinu == 명령해석기.red.length) { višak = true; continue; }
            for (int Loop_INDEX = promeniti_veličinu; Loop_INDEX > kursor_VALUE; Loop_INDEX--) 명령해석기.red[Loop_INDEX] = 명령해석기.red[Loop_INDEX - 1];
            명령해석기.red[kursor_VALUE++] = bajt_podaci; promeniti_veličinu++;
            if (kursor_VALUE == promeniti_veličinu && !가로보기 && 폭(0, promeniti_veličinu) <= 보이는폭()) Tabla.직렬쓰기(bajt_podaci);
            else if (kursor_VALUE == promeniti_veličinu) 보이는줄(); else pokušati_ponovo_VALUE();
        }
    }
}
