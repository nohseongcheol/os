// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 bajt_HODNOTA 경계를 지키는 삽입/삭제, 방향키, příkaz LOGZ_ZÁZNAM, Tab dokončeno_HODNOTA. */
public final class čára_Editor {
    static boolean příkazový_řádek;
    static int[] LOGZ_ZÁZNAM = new int[16 * 1024], LOGZ_délka = new int[16], Store_HODNOTA = new int[4096], 후보 = new int[64];
    static int LOGZ_POČET, LOGZ_ZÁZNAM_konec, HLEDAT_HODNOTA, 저장길이, Velikost, kurzor_HODNOTA, 후보수, 후보길이, START_okno;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd SSH vzdálený_displej run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String položka_Seznam, int START_pozice, int konec_pozice, int vstup_délka) {
        int bajt_POČET=0;
        for(int poziční_index=START_pozice;poziční_index<konec_pozice;poziční_index++) {
            int bod_kódu=položka_Seznam.charAt(poziční_index);
            if(bod_kódu>=0xd800 && bod_kódu<=0xdbff && poziční_index+1<konec_pozice)bod_kódu=0x10000+((bod_kódu-0xd800)<<10)+položka_Seznam.charAt(++poziční_index)-0xdc00;
            int číslo=bod_kódu<128?1:bod_kódu<2048?2:bod_kódu<65536?3:4;
            if(bajt_POČET+číslo>62)return;
            for(int SEQUENCE_HODNOTA=číslo-1;SEQUENCE_HODNOTA>=0;SEQUENCE_HODNOTA--)명령후보[bajt_POČET++]=číslo==1?bod_kódu:SEQUENCE_HODNOTA==číslo-1?(číslo==2?0xc0:číslo==3?0xe0:0xf0)|(bod_kódu>>(6*SEQUENCE_HODNOTA)):0x80|((bod_kódu>>(6*SEQUENCE_HODNOTA))&63);
        }
        if(bajt_POČET<vstup_délka)return;
        for(int poziční_index=0;poziční_index<vstup_délka;poziční_index++)if(명령후보[poziční_index]!=příkaz_interpret.vstupní_řádek[poziční_index])return;
        후보수++;후보길이=bajt_POČET+1;
        for(int poziční_index=0;poziční_index<bajt_POČET;poziční_index++)후보[poziční_index]=명령후보[poziční_index];후보[bajt_POČET]=' ';
    }
    static int přední_fotoaparát_HODNOTA(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (příkaz_interpret.vstupní_řádek[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int BACK_HODNOTA(int 읽는자리) { if (읽는자리 < Velikost) { 읽는자리++; while (읽는자리 < Velikost && (příkaz_interpret.vstupní_řádek[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int START_pozice, int cíl_HODNOTA_INDEX) {
        int 글칸수 = 0;
        for (int Loop_INDEX = START_pozice; Loop_INDEX < cíl_HODNOTA_INDEX; Loop_INDEX++) { int bajt_data = příkaz_interpret.vstupní_řádek[Loop_INDEX]; if ((bajt_data & 192) == 128) continue; 글칸수 += bajt_data >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void zkusit_znovu_HODNOTA() {
        단말.Zápis("\r\u001b[2K");
        단말.Zápis(příkazový_řádek ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 vstupní_řádek 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int SLOUPCE = Panel.interpret_příkazů(13) & 65535; return SLOUPCE - (příkazový_řádek ? 18 : 9); }
    static void 보이는줄() {
        if (kurzor_HODNOTA < START_okno) START_okno = kurzor_HODNOTA;
        while (폭(START_okno, kurzor_HODNOTA) > 보이는폭()) START_okno = BACK_HODNOTA(START_okno);
        int konec_pozice = START_okno;
        while (konec_pozice < Velikost && 폭(START_okno, BACK_HODNOTA(konec_pozice)) <= 보이는폭()) konec_pozice = BACK_HODNOTA(konec_pozice);
        단말.Zápis("\r\u001b["); 단말.číslo(příkazový_řádek ? 16 : 7); 단말.Zápis("G\u001b[K");
        if (START_okno > 0) 단말.문자('<');
        for (int Loop_INDEX = START_okno; Loop_INDEX < konec_pozice; Loop_INDEX++) Panel.직렬쓰기(příkaz_interpret.vstupní_řádek[Loop_INDEX]);
        단말.문자(konec_pozice < Velikost ? '>' : ' ');
        단말.Zápis("\u001b["); 단말.číslo(폭(kurzor_HODNOTA, konec_pozice) + 1); 단말.문자('D');
        가로보기 = START_okno > 0 || konec_pozice < Velikost || 폭(0, Velikost) > 보이는폭();
    }
    static void Připojit_LOGZ() {
        if (!příkazový_řádek || Velikost == 0 || Velikost > 1024) return;
        if (LOGZ_POČET > 0) {
            int 마지막자리 = (LOGZ_ZÁZNAM_konec + 15) % 16; boolean 같은여부 = LOGZ_délka[마지막자리] == Velikost;
            for (int Loop_INDEX = 0; 같은여부 && Loop_INDEX < Velikost; Loop_INDEX++) if (LOGZ_ZÁZNAM[마지막자리 * 1024 + Loop_INDEX] != příkaz_interpret.vstupní_řádek[Loop_INDEX]) 같은여부 = false;
            if (같은여부) return;
        }
        LOGZ_délka[LOGZ_ZÁZNAM_konec] = Velikost; for (int Loop_INDEX = 0; Loop_INDEX < Velikost; Loop_INDEX++) LOGZ_ZÁZNAM[LOGZ_ZÁZNAM_konec * 1024 + Loop_INDEX] = příkaz_interpret.vstupní_řádek[Loop_INDEX];
        LOGZ_ZÁZNAM_konec = (LOGZ_ZÁZNAM_konec + 1) % 16; if (LOGZ_POČET < 16) LOGZ_POČET++;
    }
    static void 기록이동(int DELTA_HODNOTA) {
        if (!příkazový_řádek) return;
        if (HLEDAT_HODNOTA == 0 && DELTA_HODNOTA > 0) { 저장길이 = Velikost; for (int Loop_INDEX = 0; Loop_INDEX < Velikost; Loop_INDEX++) Store_HODNOTA[Loop_INDEX] = příkaz_interpret.vstupní_řádek[Loop_INDEX]; }
        int Další_pozice = HLEDAT_HODNOTA + DELTA_HODNOTA; if (Další_pozice < 0 || Další_pozice > LOGZ_POČET) return; HLEDAT_HODNOTA = Další_pozice;
        if (HLEDAT_HODNOTA == 0) { Velikost = 저장길이; for (int Loop_INDEX = 0; Loop_INDEX < Velikost; Loop_INDEX++) příkaz_interpret.vstupní_řádek[Loop_INDEX] = Store_HODNOTA[Loop_INDEX]; }
        else { int 보관칸 = (LOGZ_ZÁZNAM_konec + 16 - HLEDAT_HODNOTA) % 16; Velikost = LOGZ_délka[보관칸]; for (int Loop_INDEX = 0; Loop_INDEX < Velikost; Loop_INDEX++) příkaz_interpret.vstupní_řádek[Loop_INDEX] = LOGZ_ZÁZNAM[보관칸 * 1024 + Loop_INDEX]; }
        kurzor_HODNOTA = Velikost; zkusit_znovu_HODNOTA();
    }
    static void zobrazit_LOGZ() {
        for (int položka_POČET = 0; položka_POČET < LOGZ_POČET; položka_POČET++) {
            int 보관칸 = (LOGZ_ZÁZNAM_konec + 16 - LOGZ_POČET + položka_POČET) % 16; 단말.číslo(položka_POČET + 1); 단말.Zápis("  ");
            for (int Loop_INDEX = 0; Loop_INDEX < LOGZ_délka[보관칸]; Loop_INDEX++) Panel.직렬쓰기(LOGZ_ZÁZNAM[보관칸 * 1024 + Loop_INDEX]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] data_pole, int START_pozice, int položka_POČET, int 접두말, int celkem_POČET, boolean Adresář_číslo) {
        if (položka_POČET < celkem_POČET || položka_POČET > 62) return;
        for (int Loop_INDEX = 0; Loop_INDEX < celkem_POČET; Loop_INDEX++) if (data_pole[START_pozice + Loop_INDEX] != příkaz_interpret.vstupní_řádek[접두말 + Loop_INDEX]) return;
        후보수++; 후보길이 = položka_POČET + 1;
        for (int Loop_INDEX = 0; Loop_INDEX < položka_POČET; Loop_INDEX++) 후보[Loop_INDEX] = data_pole[START_pozice + Loop_INDEX]; 후보[položka_POČET] = Adresář_číslo ? '/' : ' ';
    }
    static void dokončeno_HODNOTA() {
        if (!příkazový_řádek || kurzor_HODNOTA != Velikost) return;
        int 시작점 = Velikost; while (시작점 > 0 && příkaz_interpret.vstupní_řádek[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDEX = 시작점; Loop_INDEX < Velikost; Loop_INDEX++) if (příkaz_interpret.vstupní_řádek[Loop_INDEX] == '/' || příkaz_interpret.vstupní_řádek[Loop_INDEX] == '"' || příkaz_interpret.vstupní_řádek[Loop_INDEX] == 39 || příkaz_interpret.vstupní_řádek[Loop_INDEX] == '\\') return;
        후보수 = 0; int položka_POČET = Velikost - 시작점;
        if (시작점 == 0) {
            for(int index_seznamu=0;index_seznamu<2;index_seznamu++) {
                String položka_Seznam=index_seznamu==0?명령들:관리명령.dokončeno_Word();
                int 읽는자리=0;
                while(읽는자리<položka_Seznam.length()) {
                    int konec_pozice=읽는자리;while(konec_pozice<položka_Seznam.length() && položka_Seznam.charAt(konec_pozice)!=' ')konec_pozice++;
                    명령후보넣기(položka_Seznam,읽는자리,konec_pozice,položka_POČET);읽는자리=konec_pozice+1;
                }
            }
        } else {
            Paměť_Files.cesta_START(1); Paměť_Files.cesta_bajt(0, '.'); Paměť_Files.normalizovat_HODNOTA();
            for (int Loop_INDEX = 0; Loop_INDEX < Paměť_Files.Soubor_POČET; Loop_INDEX++) {
                int START_pozice = Paměť_Files.položka_START(Paměť_Files.Název, Loop_INDEX * 64, Paměť_Files.이름길이[Loop_INDEX]);
                if (START_pozice >= 0) 후보넣기(Paměť_Files.Název, Loop_INDEX * 64 + START_pozice, Paměť_Files.이름길이[Loop_INDEX] - START_pozice, 시작점, položka_POČET, false);
            }
            for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
                int START_pozice = Paměť_Files.položka_START(Paměť_Files.Adresář_název, Loop_INDEX * 64, Paměť_Files.Adresář_délka[Loop_INDEX]);
                if (START_pozice >= 0) 후보넣기(Paměť_Files.Adresář_název, Loop_INDEX * 64 + START_pozice, Paměť_Files.Adresář_délka[Loop_INDEX] - START_pozice, 시작점, položka_POČET, true);
            }
        }
        if (후보수 != 1) { Panel.직렬쓰기(7); return; }
        for (int Loop_INDEX = položka_POČET; Loop_INDEX < 후보길이 && Velikost < příkaz_interpret.vstupní_řádek.length - 1; Loop_INDEX++) {
            if (후보[Loop_INDEX] == ' ' && Loop_INDEX != 후보길이 - 1) příkaz_interpret.vstupní_řádek[Velikost++] = '\\';
            příkaz_interpret.vstupní_řádek[Velikost++] = 후보[Loop_INDEX];
        }
        kurzor_HODNOTA = Velikost; zkusit_znovu_HODNOTA();
    }
    static int 탈출읽기() {
        int 시작점 = Panel.밀리초();
        while (Panel.밀리초() - 시작점 < 80) { int bajt_data = Panel.직렬읽기(); if (bajt_data >= 0) return bajt_data; Panel.YIELD_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int položka_POČET = 0, konec_pozice = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 12; Loop_INDEX++) { int bajt_data = 탈출읽기(); if (bajt_data < 0) return; if (bajt_data >= '0' && bajt_data <= '9') položka_POČET = položka_POČET * 10 + bajt_data - '0'; else { konec_pozice = bajt_data; break; } }
        if (konec_pozice == 'A') 기록이동(1);
        else if (konec_pozice == 'B') 기록이동(-1);
        else if (konec_pozice == 'C') { kurzor_HODNOTA = BACK_HODNOTA(kurzor_HODNOTA); zkusit_znovu_HODNOTA(); }
        else if (konec_pozice == 'D') { kurzor_HODNOTA = přední_fotoaparát_HODNOTA(kurzor_HODNOTA); zkusit_znovu_HODNOTA(); }
        else if (konec_pozice == 'H' || konec_pozice == '~' && (položka_POČET == 1 || položka_POČET == 7)) { kurzor_HODNOTA = 0; zkusit_znovu_HODNOTA(); }
        else if (konec_pozice == 'F' || konec_pozice == '~' && (položka_POČET == 4 || položka_POČET == 8)) { kurzor_HODNOTA = Velikost; zkusit_znovu_HODNOTA(); }
        else if (konec_pozice == '~' && položka_POČET == 3 && kurzor_HODNOTA < Velikost) {
            int Další_pozice = BACK_HODNOTA(kurzor_HODNOTA); for (int Loop_INDEX = Další_pozice; Loop_INDEX < Velikost; Loop_INDEX++) příkaz_interpret.vstupní_řádek[Loop_INDEX - Další_pozice + kurzor_HODNOTA] = příkaz_interpret.vstupní_řádek[Loop_INDEX]; Velikost -= Další_pozice - kurzor_HODNOTA; zkusit_znovu_HODNOTA();
        }
        else if (konec_pozice == '~' && (položka_POČET == 5 || položka_POČET == 6)) Panel.interpret_příkazů(položka_POČET == 5 ? 5 : 6);
        else if (konec_pozice == '~' && položka_POČET == 24 && příkazový_řádek) { příkaz_interpret.interpret_příkazů(true); }
    }
    static int Čtení() {
        if (!okno_relace.이어읽기) { Velikost = kurzor_HODNOTA = HLEDAT_HODNOTA = START_okno = 0; 가로보기 = false; }
        else { okno_relace.이어읽기 = false; zkusit_znovu_HODNOTA(); } boolean přetečení = false;
        while (true) {
            int bajt_data = Panel.직렬읽기(); if (bajt_data == -4096) return -3;
            if (Panel.interpret_příkazů(14) != 0) zkusit_znovu_HODNOTA(); if (bajt_data < 0) { Panel.YIELD_CPU(); continue; }
            if (bajt_data == 10 && příkaz_interpret.Předchozí_čára) { příkaz_interpret.Předchozí_čára = false; continue; } příkaz_interpret.Předchozí_čára = bajt_data == 13;
            if (bajt_data == 27) { 탈출(); continue; }
            if (bajt_data == 3) { 단말.Zápis("^C\n"); return -1; }
            if (bajt_data == 4 && Velikost == 0 && příkazový_řádek) { if (Panel.interpret_příkazů(2) != 0) příkaz_interpret.interpret_příkazů(true); return -1; }
            if (bajt_data == 13 || bajt_data == 10) { 단말.문자(10); if (!přetečení) Připojit_LOGZ(); return přetečení ? -2 : Velikost; }
            if (bajt_data == 9 && příkazový_řádek) { dokončeno_HODNOTA(); continue; }
            if (bajt_data == 1 || bajt_data == 5) { kurzor_HODNOTA = bajt_data == 1 ? 0 : Velikost; zkusit_znovu_HODNOTA(); continue; }
            if (bajt_data == 8 || bajt_data == 127 || bajt_data == 21) {
                if (bajt_data == 21) { for (int Loop_INDEX = kurzor_HODNOTA; Loop_INDEX < Velikost; Loop_INDEX++) příkaz_interpret.vstupní_řádek[Loop_INDEX - kurzor_HODNOTA] = příkaz_interpret.vstupní_řádek[Loop_INDEX]; Velikost -= kurzor_HODNOTA; kurzor_HODNOTA = 0; }
                else if (kurzor_HODNOTA > 0) { int 변경전 = přední_fotoaparát_HODNOTA(kurzor_HODNOTA); for (int Loop_INDEX = kurzor_HODNOTA; Loop_INDEX < Velikost; Loop_INDEX++) příkaz_interpret.vstupní_řádek[Loop_INDEX - kurzor_HODNOTA + 변경전] = příkaz_interpret.vstupní_řádek[Loop_INDEX]; Velikost -= kurzor_HODNOTA - 변경전; kurzor_HODNOTA = 변경전; }
                zkusit_znovu_HODNOTA(); continue;
            }
            if (bajt_data == 11) { Velikost = kurzor_HODNOTA; zkusit_znovu_HODNOTA(); continue; }
            if (bajt_data < 32 && bajt_data != 9) continue;
            if (Velikost == příkaz_interpret.vstupní_řádek.length) { přetečení = true; continue; }
            for (int Loop_INDEX = Velikost; Loop_INDEX > kurzor_HODNOTA; Loop_INDEX--) příkaz_interpret.vstupní_řádek[Loop_INDEX] = příkaz_interpret.vstupní_řádek[Loop_INDEX - 1];
            příkaz_interpret.vstupní_řádek[kurzor_HODNOTA++] = bajt_data; Velikost++;
            if (kurzor_HODNOTA == Velikost && !가로보기 && 폭(0, Velikost) <= 보이는폭()) Panel.직렬쓰기(bajt_data);
            else if (kurzor_HODNOTA == Velikost) 보이는줄(); else zkusit_znovu_HODNOTA();
        }
    }
}
