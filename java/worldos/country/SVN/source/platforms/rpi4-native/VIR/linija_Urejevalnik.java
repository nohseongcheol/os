// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 bajt_VALUE 경계를 지키는 삽입/삭제, 방향키, Ukaz LOG_zapis, Tab Dokončano_VALUE. */
public final class linija_Urejevalnik {
    static boolean ukazna_vrstica;
    static int[] LOG_zapis = new int[16 * 1024], 기록길이 = new int[16], Store_VALUE = new int[4096], 후보 = new int[64];
    static int LOG_COUNT, LOG_zapis_končati_klic, Išči_VALUE, 저장길이, Velikost, kazalec_VALUE, 후보수, 후보길이, Start_okno;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd varen_lupina oddaljen_zaslon run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String vnos_Seznam, int Start_položaj, int končati_klic_položaj, int 입력길이) {
        int bajt_COUNT=0;
        for(int kazalec_mesta=Start_položaj;kazalec_mesta<končati_klic_položaj;kazalec_mesta++) {
            int koda_znaka=vnos_Seznam.charAt(kazalec_mesta);
            if(koda_znaka>=0xd800 && koda_znaka<=0xdbff && kazalec_mesta+1<končati_klic_položaj)koda_znaka=0x10000+((koda_znaka-0xd800)<<10)+vnos_Seznam.charAt(++kazalec_mesta)-0xdc00;
            int 수=koda_znaka<128?1:koda_znaka<2048?2:koda_znaka<65536?3:4;
            if(bajt_COUNT+수>62)return;
            for(int SEQUENCE_VALUE=수-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--)명령후보[bajt_COUNT++]=수==1?koda_znaka:SEQUENCE_VALUE==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(koda_znaka>>(6*SEQUENCE_VALUE)):0x80|((koda_znaka>>(6*SEQUENCE_VALUE))&63);
        }
        if(bajt_COUNT<입력길이)return;
        for(int kazalec_mesta=0;kazalec_mesta<입력길이;kazalec_mesta++)if(명령후보[kazalec_mesta]!=명령해석기.Črtni[kazalec_mesta])return;
        후보수++;후보길이=bajt_COUNT+1;
        for(int kazalec_mesta=0;kazalec_mesta<bajt_COUNT;kazalec_mesta++)후보[kazalec_mesta]=명령후보[kazalec_mesta];후보[bajt_COUNT]=' ';
    }
    static int sprednja_VALUE(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.Črtni[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int ZAJ_VALUE(int 읽는자리) { if (읽는자리 < Velikost) { 읽는자리++; while (읽는자리 < Velikost && (명령해석기.Črtni[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int Start_položaj, int cilj_VALUE_INDEX) {
        int 글칸수 = 0;
        for (int Loop_INDEX = Start_položaj; Loop_INDEX < cilj_VALUE_INDEX; Loop_INDEX++) { int bajt_podatki = 명령해석기.Črtni[Loop_INDEX]; if ((bajt_podatki & 192) == 128) continue; 글칸수 += bajt_podatki >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void znova_poskusiti_VALUE() {
        단말.Pisanje("\r\u001b[2K");
        단말.Pisanje(ukazna_vrstica ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 Črtni 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int COLUMNS = Tabla.Terminal(13) & 65535; return COLUMNS - (ukazna_vrstica ? 18 : 9); }
    static void 보이는줄() {
        if (kazalec_VALUE < Start_okno) Start_okno = kazalec_VALUE;
        while (폭(Start_okno, kazalec_VALUE) > 보이는폭()) Start_okno = ZAJ_VALUE(Start_okno);
        int končati_klic_položaj = Start_okno;
        while (končati_klic_položaj < Velikost && 폭(Start_okno, ZAJ_VALUE(končati_klic_položaj)) <= 보이는폭()) končati_klic_položaj = ZAJ_VALUE(končati_klic_položaj);
        단말.Pisanje("\r\u001b["); 단말.수(ukazna_vrstica ? 16 : 7); 단말.Pisanje("G\u001b[K");
        if (Start_okno > 0) 단말.문자('<');
        for (int Loop_INDEX = Start_okno; Loop_INDEX < končati_klic_položaj; Loop_INDEX++) Tabla.직렬쓰기(명령해석기.Črtni[Loop_INDEX]);
        단말.문자(končati_klic_položaj < Velikost ? '>' : ' ');
        단말.Pisanje("\u001b["); 단말.수(폭(kazalec_VALUE, končati_klic_položaj) + 1); 단말.문자('D');
        가로보기 = Start_okno > 0 || končati_klic_položaj < Velikost || 폭(0, Velikost) > 보이는폭();
    }
    static void dodati_LOG() {
        if (!ukazna_vrstica || Velikost == 0 || Velikost > 1024) return;
        if (LOG_COUNT > 0) {
            int 마지막자리 = (LOG_zapis_končati_klic + 15) % 16; boolean 같은여부 = 기록길이[마지막자리] == Velikost;
            for (int Loop_INDEX = 0; 같은여부 && Loop_INDEX < Velikost; Loop_INDEX++) if (LOG_zapis[마지막자리 * 1024 + Loop_INDEX] != 명령해석기.Črtni[Loop_INDEX]) 같은여부 = false;
            if (같은여부) return;
        }
        기록길이[LOG_zapis_končati_klic] = Velikost; for (int Loop_INDEX = 0; Loop_INDEX < Velikost; Loop_INDEX++) LOG_zapis[LOG_zapis_končati_klic * 1024 + Loop_INDEX] = 명령해석기.Črtni[Loop_INDEX];
        LOG_zapis_končati_klic = (LOG_zapis_končati_klic + 1) % 16; if (LOG_COUNT < 16) LOG_COUNT++;
    }
    static void 기록이동(int DELTA_VALUE) {
        if (!ukazna_vrstica) return;
        if (Išči_VALUE == 0 && DELTA_VALUE > 0) { 저장길이 = Velikost; for (int Loop_INDEX = 0; Loop_INDEX < Velikost; Loop_INDEX++) Store_VALUE[Loop_INDEX] = 명령해석기.Črtni[Loop_INDEX]; }
        int Naprej_položaj = Išči_VALUE + DELTA_VALUE; if (Naprej_položaj < 0 || Naprej_položaj > LOG_COUNT) return; Išči_VALUE = Naprej_položaj;
        if (Išči_VALUE == 0) { Velikost = 저장길이; for (int Loop_INDEX = 0; Loop_INDEX < Velikost; Loop_INDEX++) 명령해석기.Črtni[Loop_INDEX] = Store_VALUE[Loop_INDEX]; }
        else { int 보관칸 = (LOG_zapis_končati_klic + 16 - Išči_VALUE) % 16; Velikost = 기록길이[보관칸]; for (int Loop_INDEX = 0; Loop_INDEX < Velikost; Loop_INDEX++) 명령해석기.Črtni[Loop_INDEX] = LOG_zapis[보관칸 * 1024 + Loop_INDEX]; }
        kazalec_VALUE = Velikost; znova_poskusiti_VALUE();
    }
    static void oddaja_LOG() {
        for (int vnos_COUNT = 0; vnos_COUNT < LOG_COUNT; vnos_COUNT++) {
            int 보관칸 = (LOG_zapis_končati_klic + 16 - LOG_COUNT + vnos_COUNT) % 16; 단말.수(vnos_COUNT + 1); 단말.Pisanje("  ");
            for (int Loop_INDEX = 0; Loop_INDEX < 기록길이[보관칸]; Loop_INDEX++) Tabla.직렬쓰기(LOG_zapis[보관칸 * 1024 + Loop_INDEX]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] podatki_ARRAY, int Start_položaj, int vnos_COUNT, int 접두말, int skupaj_COUNT, boolean 폴더번호) {
        if (vnos_COUNT < skupaj_COUNT || vnos_COUNT > 62) return;
        for (int Loop_INDEX = 0; Loop_INDEX < skupaj_COUNT; Loop_INDEX++) if (podatki_ARRAY[Start_položaj + Loop_INDEX] != 명령해석기.Črtni[접두말 + Loop_INDEX]) return;
        후보수++; 후보길이 = vnos_COUNT + 1;
        for (int Loop_INDEX = 0; Loop_INDEX < vnos_COUNT; Loop_INDEX++) 후보[Loop_INDEX] = podatki_ARRAY[Start_položaj + Loop_INDEX]; 후보[vnos_COUNT] = 폴더번호 ? '/' : ' ';
    }
    static void Dokončano_VALUE() {
        if (!ukazna_vrstica || kazalec_VALUE != Velikost) return;
        int 시작점 = Velikost; while (시작점 > 0 && 명령해석기.Črtni[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDEX = 시작점; Loop_INDEX < Velikost; Loop_INDEX++) if (명령해석기.Črtni[Loop_INDEX] == '/' || 명령해석기.Črtni[Loop_INDEX] == '"' || 명령해석기.Črtni[Loop_INDEX] == 39 || 명령해석기.Črtni[Loop_INDEX] == '\\') return;
        후보수 = 0; int vnos_COUNT = Velikost - 시작점;
        if (시작점 == 0) {
            for(int Seznam_INDEX=0;Seznam_INDEX<2;Seznam_INDEX++) {
                String vnos_Seznam=Seznam_INDEX==0?명령들:관리명령.Dokončano_Word();
                int 읽는자리=0;
                while(읽는자리<vnos_Seznam.length()) {
                    int končati_klic_položaj=읽는자리;while(končati_klic_položaj<vnos_Seznam.length() && vnos_Seznam.charAt(končati_klic_položaj)!=' ')končati_klic_položaj++;
                    명령후보넣기(vnos_Seznam,읽는자리,končati_klic_položaj,vnos_COUNT);읽는자리=končati_klic_položaj+1;
                }
            }
        } else {
            pomnilnik_Datoteke.pot_Start(1); pomnilnik_Datoteke.pot_bajt(0, '.'); pomnilnik_Datoteke.normalizirati_VALUE();
            for (int Loop_INDEX = 0; Loop_INDEX < pomnilnik_Datoteke.Datoteka_COUNT; Loop_INDEX++) {
                int Start_položaj = pomnilnik_Datoteke.vnos_Start(pomnilnik_Datoteke.Ime, Loop_INDEX * 64, pomnilnik_Datoteke.이름길이[Loop_INDEX]);
                if (Start_položaj >= 0) 후보넣기(pomnilnik_Datoteke.Ime, Loop_INDEX * 64 + Start_položaj, pomnilnik_Datoteke.이름길이[Loop_INDEX] - Start_položaj, 시작점, vnos_COUNT, false);
            }
            for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
                int Start_položaj = pomnilnik_Datoteke.vnos_Start(pomnilnik_Datoteke.Imenik_ime, Loop_INDEX * 64, pomnilnik_Datoteke.폴더길이[Loop_INDEX]);
                if (Start_položaj >= 0) 후보넣기(pomnilnik_Datoteke.Imenik_ime, Loop_INDEX * 64 + Start_položaj, pomnilnik_Datoteke.폴더길이[Loop_INDEX] - Start_položaj, 시작점, vnos_COUNT, true);
            }
        }
        if (후보수 != 1) { Tabla.직렬쓰기(7); return; }
        for (int Loop_INDEX = vnos_COUNT; Loop_INDEX < 후보길이 && Velikost < 명령해석기.Črtni.length - 1; Loop_INDEX++) {
            if (후보[Loop_INDEX] == ' ' && Loop_INDEX != 후보길이 - 1) 명령해석기.Črtni[Velikost++] = '\\';
            명령해석기.Črtni[Velikost++] = 후보[Loop_INDEX];
        }
        kazalec_VALUE = Velikost; znova_poskusiti_VALUE();
    }
    static int 탈출읽기() {
        int 시작점 = Tabla.밀리초();
        while (Tabla.밀리초() - 시작점 < 80) { int bajt_podatki = Tabla.직렬읽기(); if (bajt_podatki >= 0) return bajt_podatki; Tabla.YIELD_CPE(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int vnos_COUNT = 0, končati_klic_položaj = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 12; Loop_INDEX++) { int bajt_podatki = 탈출읽기(); if (bajt_podatki < 0) return; if (bajt_podatki >= '0' && bajt_podatki <= '9') vnos_COUNT = vnos_COUNT * 10 + bajt_podatki - '0'; else { končati_klic_položaj = bajt_podatki; break; } }
        if (končati_klic_položaj == 'A') 기록이동(1);
        else if (končati_klic_položaj == 'B') 기록이동(-1);
        else if (končati_klic_položaj == 'C') { kazalec_VALUE = ZAJ_VALUE(kazalec_VALUE); znova_poskusiti_VALUE(); }
        else if (končati_klic_položaj == 'D') { kazalec_VALUE = sprednja_VALUE(kazalec_VALUE); znova_poskusiti_VALUE(); }
        else if (končati_klic_položaj == 'H' || končati_klic_položaj == '~' && (vnos_COUNT == 1 || vnos_COUNT == 7)) { kazalec_VALUE = 0; znova_poskusiti_VALUE(); }
        else if (končati_klic_položaj == 'F' || končati_klic_položaj == '~' && (vnos_COUNT == 4 || vnos_COUNT == 8)) { kazalec_VALUE = Velikost; znova_poskusiti_VALUE(); }
        else if (končati_klic_položaj == '~' && vnos_COUNT == 3 && kazalec_VALUE < Velikost) {
            int Naprej_položaj = ZAJ_VALUE(kazalec_VALUE); for (int Loop_INDEX = Naprej_položaj; Loop_INDEX < Velikost; Loop_INDEX++) 명령해석기.Črtni[Loop_INDEX - Naprej_položaj + kazalec_VALUE] = 명령해석기.Črtni[Loop_INDEX]; Velikost -= Naprej_položaj - kazalec_VALUE; znova_poskusiti_VALUE();
        }
        else if (končati_klic_položaj == '~' && (vnos_COUNT == 5 || vnos_COUNT == 6)) Tabla.Terminal(vnos_COUNT == 5 ? 5 : 6);
        else if (končati_klic_položaj == '~' && vnos_COUNT == 24 && ukazna_vrstica) { 명령해석기.Terminal(true); }
    }
    static int Branje() {
        if (!okno_seja.이어읽기) { Velikost = kazalec_VALUE = Išči_VALUE = Start_okno = 0; 가로보기 = false; }
        else { okno_seja.이어읽기 = false; znova_poskusiti_VALUE(); } boolean presežek = false;
        while (true) {
            int bajt_podatki = Tabla.직렬읽기(); if (bajt_podatki == -4096) return -3;
            if (Tabla.Terminal(14) != 0) znova_poskusiti_VALUE(); if (bajt_podatki < 0) { Tabla.YIELD_CPE(); continue; }
            if (bajt_podatki == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = bajt_podatki == 13;
            if (bajt_podatki == 27) { 탈출(); continue; }
            if (bajt_podatki == 3) { 단말.Pisanje("^C\n"); return -1; }
            if (bajt_podatki == 4 && Velikost == 0 && ukazna_vrstica) { if (Tabla.Terminal(2) != 0) 명령해석기.Terminal(true); return -1; }
            if (bajt_podatki == 13 || bajt_podatki == 10) { 단말.문자(10); if (!presežek) dodati_LOG(); return presežek ? -2 : Velikost; }
            if (bajt_podatki == 9 && ukazna_vrstica) { Dokončano_VALUE(); continue; }
            if (bajt_podatki == 1 || bajt_podatki == 5) { kazalec_VALUE = bajt_podatki == 1 ? 0 : Velikost; znova_poskusiti_VALUE(); continue; }
            if (bajt_podatki == 8 || bajt_podatki == 127 || bajt_podatki == 21) {
                if (bajt_podatki == 21) { for (int Loop_INDEX = kazalec_VALUE; Loop_INDEX < Velikost; Loop_INDEX++) 명령해석기.Črtni[Loop_INDEX - kazalec_VALUE] = 명령해석기.Črtni[Loop_INDEX]; Velikost -= kazalec_VALUE; kazalec_VALUE = 0; }
                else if (kazalec_VALUE > 0) { int 변경전 = sprednja_VALUE(kazalec_VALUE); for (int Loop_INDEX = kazalec_VALUE; Loop_INDEX < Velikost; Loop_INDEX++) 명령해석기.Črtni[Loop_INDEX - kazalec_VALUE + 변경전] = 명령해석기.Črtni[Loop_INDEX]; Velikost -= kazalec_VALUE - 변경전; kazalec_VALUE = 변경전; }
                znova_poskusiti_VALUE(); continue;
            }
            if (bajt_podatki == 11) { Velikost = kazalec_VALUE; znova_poskusiti_VALUE(); continue; }
            if (bajt_podatki < 32 && bajt_podatki != 9) continue;
            if (Velikost == 명령해석기.Črtni.length) { presežek = true; continue; }
            for (int Loop_INDEX = Velikost; Loop_INDEX > kazalec_VALUE; Loop_INDEX--) 명령해석기.Črtni[Loop_INDEX] = 명령해석기.Črtni[Loop_INDEX - 1];
            명령해석기.Črtni[kazalec_VALUE++] = bajt_podatki; Velikost++;
            if (kazalec_VALUE == Velikost && !가로보기 && 폭(0, Velikost) <= 보이는폭()) Tabla.직렬쓰기(bajt_podatki);
            else if (kazalec_VALUE == Velikost) 보이는줄(); else znova_poskusiti_VALUE();
        }
    }
}
