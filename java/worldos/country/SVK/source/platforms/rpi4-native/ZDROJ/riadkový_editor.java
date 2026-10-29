// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 Byte_VALUE 경계를 지키는 삽입/삭제, 방향키, Príkaz LOG_RECORD, Tab Dokončené_úlohy_VALUE. */
public final class riadkový_editor {
    static boolean príkazový_riadok;
    static int[] LOG_RECORD = new int[16 * 1024], LOG_dĺžka = new int[16], Store_VALUE = new int[4096], 후보 = new int[64];
    static int LOG_COUNT, LOG_RECORD_ukončiť_hovor, Hľadať_VALUE, 저장길이, Veľkosť, kurzor_VALUE, 후보수, 후보길이, START_okno;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd 보안셸 vzdialený_displej run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String položka_Zoznam, int START_pozícia, int ukončiť_hovor_pozícia, int vstup_dĺžka) {
        int Byte_COUNT=0;
        for(int pozičný_index=START_pozícia;pozičný_index<ukončiť_hovor_pozícia;pozičný_index++) {
            int bod_kódu=položka_Zoznam.charAt(pozičný_index);
            if(bod_kódu>=0xd800 && bod_kódu<=0xdbff && pozičný_index+1<ukončiť_hovor_pozícia)bod_kódu=0x10000+((bod_kódu-0xd800)<<10)+položka_Zoznam.charAt(++pozičný_index)-0xdc00;
            int 수=bod_kódu<128?1:bod_kódu<2048?2:bod_kódu<65536?3:4;
            if(Byte_COUNT+수>62)return;
            for(int SEQUENCE_VALUE=수-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--)명령후보[Byte_COUNT++]=수==1?bod_kódu:SEQUENCE_VALUE==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(bod_kódu>>(6*SEQUENCE_VALUE)):0x80|((bod_kódu>>(6*SEQUENCE_VALUE))&63);
        }
        if(Byte_COUNT<vstup_dĺžka)return;
        for(int pozičný_index=0;pozičný_index<vstup_dĺžka;pozičný_index++)if(명령후보[pozičný_index]!=명령해석기.riadok[pozičný_index])return;
        후보수++;후보길이=Byte_COUNT+1;
        for(int pozičný_index=0;pozičný_index<Byte_COUNT;pozičný_index++)후보[pozičný_index]=명령후보[pozičný_index];후보[Byte_COUNT]=' ';
    }
    static int predný_VALUE(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.riadok[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int BACK_VALUE(int 읽는자리) { if (읽는자리 < Veľkosť) { 읽는자리++; while (읽는자리 < Veľkosť && (명령해석기.riadok[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int START_pozícia, int cieľ_VALUE_INDEX) {
        int 글칸수 = 0;
        for (int Loop_INDEX = START_pozícia; Loop_INDEX < cieľ_VALUE_INDEX; Loop_INDEX++) { int Byte_údaje = 명령해석기.riadok[Loop_INDEX]; if ((Byte_údaje & 192) == 128) continue; 글칸수 += Byte_údaje >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void skúsiť_znova_VALUE() {
        단말.Zápis("\r\u001b[2K");
        단말.Zápis(príkazový_riadok ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 riadok 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int COLUMNS = Panel.Terminál(13) & 65535; return COLUMNS - (príkazový_riadok ? 18 : 9); }
    static void 보이는줄() {
        if (kurzor_VALUE < START_okno) START_okno = kurzor_VALUE;
        while (폭(START_okno, kurzor_VALUE) > 보이는폭()) START_okno = BACK_VALUE(START_okno);
        int ukončiť_hovor_pozícia = START_okno;
        while (ukončiť_hovor_pozícia < Veľkosť && 폭(START_okno, BACK_VALUE(ukončiť_hovor_pozícia)) <= 보이는폭()) ukončiť_hovor_pozícia = BACK_VALUE(ukončiť_hovor_pozícia);
        단말.Zápis("\r\u001b["); 단말.수(príkazový_riadok ? 16 : 7); 단말.Zápis("G\u001b[K");
        if (START_okno > 0) 단말.문자('<');
        for (int Loop_INDEX = START_okno; Loop_INDEX < ukončiť_hovor_pozícia; Loop_INDEX++) Panel.직렬쓰기(명령해석기.riadok[Loop_INDEX]);
        단말.문자(ukončiť_hovor_pozícia < Veľkosť ? '>' : ' ');
        단말.Zápis("\u001b["); 단말.수(폭(kurzor_VALUE, ukončiť_hovor_pozícia) + 1); 단말.문자('D');
        가로보기 = START_okno > 0 || ukončiť_hovor_pozícia < Veľkosť || 폭(0, Veľkosť) > 보이는폭();
    }
    static void Pripojiť_LOG() {
        if (!príkazový_riadok || Veľkosť == 0 || Veľkosť > 1024) return;
        if (LOG_COUNT > 0) {
            int 마지막자리 = (LOG_RECORD_ukončiť_hovor + 15) % 16; boolean 같은여부 = LOG_dĺžka[마지막자리] == Veľkosť;
            for (int Loop_INDEX = 0; 같은여부 && Loop_INDEX < Veľkosť; Loop_INDEX++) if (LOG_RECORD[마지막자리 * 1024 + Loop_INDEX] != 명령해석기.riadok[Loop_INDEX]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_dĺžka[LOG_RECORD_ukončiť_hovor] = Veľkosť; for (int Loop_INDEX = 0; Loop_INDEX < Veľkosť; Loop_INDEX++) LOG_RECORD[LOG_RECORD_ukončiť_hovor * 1024 + Loop_INDEX] = 명령해석기.riadok[Loop_INDEX];
        LOG_RECORD_ukončiť_hovor = (LOG_RECORD_ukončiť_hovor + 1) % 16; if (LOG_COUNT < 16) LOG_COUNT++;
    }
    static void 기록이동(int DELTA_VALUE) {
        if (!príkazový_riadok) return;
        if (Hľadať_VALUE == 0 && DELTA_VALUE > 0) { 저장길이 = Veľkosť; for (int Loop_INDEX = 0; Loop_INDEX < Veľkosť; Loop_INDEX++) Store_VALUE[Loop_INDEX] = 명령해석기.riadok[Loop_INDEX]; }
        int Ďalej_pozícia = Hľadať_VALUE + DELTA_VALUE; if (Ďalej_pozícia < 0 || Ďalej_pozícia > LOG_COUNT) return; Hľadať_VALUE = Ďalej_pozícia;
        if (Hľadať_VALUE == 0) { Veľkosť = 저장길이; for (int Loop_INDEX = 0; Loop_INDEX < Veľkosť; Loop_INDEX++) 명령해석기.riadok[Loop_INDEX] = Store_VALUE[Loop_INDEX]; }
        else { int 보관칸 = (LOG_RECORD_ukončiť_hovor + 16 - Hľadať_VALUE) % 16; Veľkosť = LOG_dĺžka[보관칸]; for (int Loop_INDEX = 0; Loop_INDEX < Veľkosť; Loop_INDEX++) 명령해석기.riadok[Loop_INDEX] = LOG_RECORD[보관칸 * 1024 + Loop_INDEX]; }
        kurzor_VALUE = Veľkosť; skúsiť_znova_VALUE();
    }
    static void zobraziť_LOG() {
        for (int položka_COUNT_8f7753a1 = 0; položka_COUNT_8f7753a1 < LOG_COUNT; položka_COUNT_8f7753a1++) {
            int 보관칸 = (LOG_RECORD_ukončiť_hovor + 16 - LOG_COUNT + položka_COUNT_8f7753a1) % 16; 단말.수(položka_COUNT_8f7753a1 + 1); 단말.Zápis("  ");
            for (int Loop_INDEX = 0; Loop_INDEX < LOG_dĺžka[보관칸]; Loop_INDEX++) Panel.직렬쓰기(LOG_RECORD[보관칸 * 1024 + Loop_INDEX]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] údaje_pole, int START_pozícia, int položka_COUNT_8f7753a1, int 접두말, int celkovo_COUNT, boolean 폴더번호) {
        if (položka_COUNT_8f7753a1 < celkovo_COUNT || položka_COUNT_8f7753a1 > 62) return;
        for (int Loop_INDEX = 0; Loop_INDEX < celkovo_COUNT; Loop_INDEX++) if (údaje_pole[START_pozícia + Loop_INDEX] != 명령해석기.riadok[접두말 + Loop_INDEX]) return;
        후보수++; 후보길이 = položka_COUNT_8f7753a1 + 1;
        for (int Loop_INDEX = 0; Loop_INDEX < položka_COUNT_8f7753a1; Loop_INDEX++) 후보[Loop_INDEX] = údaje_pole[START_pozícia + Loop_INDEX]; 후보[položka_COUNT_8f7753a1] = 폴더번호 ? '/' : ' ';
    }
    static void Dokončené_úlohy_VALUE() {
        if (!príkazový_riadok || kurzor_VALUE != Veľkosť) return;
        int 시작점 = Veľkosť; while (시작점 > 0 && 명령해석기.riadok[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDEX = 시작점; Loop_INDEX < Veľkosť; Loop_INDEX++) if (명령해석기.riadok[Loop_INDEX] == '/' || 명령해석기.riadok[Loop_INDEX] == '"' || 명령해석기.riadok[Loop_INDEX] == 39 || 명령해석기.riadok[Loop_INDEX] == '\\') return;
        후보수 = 0; int položka_COUNT_8f7753a1 = Veľkosť - 시작점;
        if (시작점 == 0) {
            for(int index_v_zozname=0;index_v_zozname<2;index_v_zozname++) {
                String položka_Zoznam=index_v_zozname==0?명령들:관리명령.Dokončené_úlohy_Word();
                int 읽는자리=0;
                while(읽는자리<položka_Zoznam.length()) {
                    int ukončiť_hovor_pozícia=읽는자리;while(ukončiť_hovor_pozícia<položka_Zoznam.length() && položka_Zoznam.charAt(ukončiť_hovor_pozícia)!=' ')ukončiť_hovor_pozícia++;
                    명령후보넣기(položka_Zoznam,읽는자리,ukončiť_hovor_pozícia,položka_COUNT_8f7753a1);읽는자리=ukončiť_hovor_pozícia+1;
                }
            }
        } else {
            Pamäť_Súbory.cesta_START(1); Pamäť_Súbory.cesta_Byte(0, '.'); Pamäť_Súbory.normalizovať_VALUE();
            for (int Loop_INDEX = 0; Loop_INDEX < Pamäť_Súbory.Súbor_COUNT; Loop_INDEX++) {
                int START_pozícia = Pamäť_Súbory.položka_START(Pamäť_Súbory.Názov, Loop_INDEX * 64, Pamäť_Súbory.이름길이[Loop_INDEX]);
                if (START_pozícia >= 0) 후보넣기(Pamäť_Súbory.Názov, Loop_INDEX * 64 + START_pozícia, Pamäť_Súbory.이름길이[Loop_INDEX] - START_pozícia, 시작점, položka_COUNT_8f7753a1, false);
            }
            for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
                int START_pozícia = Pamäť_Súbory.položka_START(Pamäť_Súbory.Adresár_názov, Loop_INDEX * 64, Pamäť_Súbory.Adresár_dĺžka[Loop_INDEX]);
                if (START_pozícia >= 0) 후보넣기(Pamäť_Súbory.Adresár_názov, Loop_INDEX * 64 + START_pozícia, Pamäť_Súbory.Adresár_dĺžka[Loop_INDEX] - START_pozícia, 시작점, položka_COUNT_8f7753a1, true);
            }
        }
        if (후보수 != 1) { Panel.직렬쓰기(7); return; }
        for (int Loop_INDEX = položka_COUNT_8f7753a1; Loop_INDEX < 후보길이 && Veľkosť < 명령해석기.riadok.length - 1; Loop_INDEX++) {
            if (후보[Loop_INDEX] == ' ' && Loop_INDEX != 후보길이 - 1) 명령해석기.riadok[Veľkosť++] = '\\';
            명령해석기.riadok[Veľkosť++] = 후보[Loop_INDEX];
        }
        kurzor_VALUE = Veľkosť; skúsiť_znova_VALUE();
    }
    static int 탈출읽기() {
        int 시작점 = Panel.밀리초();
        while (Panel.밀리초() - 시작점 < 80) { int Byte_údaje = Panel.직렬읽기(); if (Byte_údaje >= 0) return Byte_údaje; Panel.YIELD_procesor(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int položka_COUNT_8f7753a1 = 0, ukončiť_hovor_pozícia = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 12; Loop_INDEX++) { int Byte_údaje = 탈출읽기(); if (Byte_údaje < 0) return; if (Byte_údaje >= '0' && Byte_údaje <= '9') položka_COUNT_8f7753a1 = položka_COUNT_8f7753a1 * 10 + Byte_údaje - '0'; else { ukončiť_hovor_pozícia = Byte_údaje; break; } }
        if (ukončiť_hovor_pozícia == 'A') 기록이동(1);
        else if (ukončiť_hovor_pozícia == 'B') 기록이동(-1);
        else if (ukončiť_hovor_pozícia == 'C') { kurzor_VALUE = BACK_VALUE(kurzor_VALUE); skúsiť_znova_VALUE(); }
        else if (ukončiť_hovor_pozícia == 'D') { kurzor_VALUE = predný_VALUE(kurzor_VALUE); skúsiť_znova_VALUE(); }
        else if (ukončiť_hovor_pozícia == 'H' || ukončiť_hovor_pozícia == '~' && (položka_COUNT_8f7753a1 == 1 || položka_COUNT_8f7753a1 == 7)) { kurzor_VALUE = 0; skúsiť_znova_VALUE(); }
        else if (ukončiť_hovor_pozícia == 'F' || ukončiť_hovor_pozícia == '~' && (položka_COUNT_8f7753a1 == 4 || položka_COUNT_8f7753a1 == 8)) { kurzor_VALUE = Veľkosť; skúsiť_znova_VALUE(); }
        else if (ukončiť_hovor_pozícia == '~' && položka_COUNT_8f7753a1 == 3 && kurzor_VALUE < Veľkosť) {
            int Ďalej_pozícia = BACK_VALUE(kurzor_VALUE); for (int Loop_INDEX = Ďalej_pozícia; Loop_INDEX < Veľkosť; Loop_INDEX++) 명령해석기.riadok[Loop_INDEX - Ďalej_pozícia + kurzor_VALUE] = 명령해석기.riadok[Loop_INDEX]; Veľkosť -= Ďalej_pozícia - kurzor_VALUE; skúsiť_znova_VALUE();
        }
        else if (ukončiť_hovor_pozícia == '~' && (položka_COUNT_8f7753a1 == 5 || položka_COUNT_8f7753a1 == 6)) Panel.Terminál(položka_COUNT_8f7753a1 == 5 ? 5 : 6);
        else if (ukončiť_hovor_pozícia == '~' && položka_COUNT_8f7753a1 == 24 && príkazový_riadok) { 명령해석기.Terminál(true); }
    }
    static int Čítanie() {
        if (!okno_relácia.이어읽기) { Veľkosť = kurzor_VALUE = Hľadať_VALUE = START_okno = 0; 가로보기 = false; }
        else { okno_relácia.이어읽기 = false; skúsiť_znova_VALUE(); } boolean pretečenie = false;
        while (true) {
            int Byte_údaje = Panel.직렬읽기(); if (Byte_údaje == -4096) return -3;
            if (Panel.Terminál(14) != 0) skúsiť_znova_VALUE(); if (Byte_údaje < 0) { Panel.YIELD_procesor(); continue; }
            if (Byte_údaje == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = Byte_údaje == 13;
            if (Byte_údaje == 27) { 탈출(); continue; }
            if (Byte_údaje == 3) { 단말.Zápis("^C\n"); return -1; }
            if (Byte_údaje == 4 && Veľkosť == 0 && príkazový_riadok) { if (Panel.Terminál(2) != 0) 명령해석기.Terminál(true); return -1; }
            if (Byte_údaje == 13 || Byte_údaje == 10) { 단말.문자(10); if (!pretečenie) Pripojiť_LOG(); return pretečenie ? -2 : Veľkosť; }
            if (Byte_údaje == 9 && príkazový_riadok) { Dokončené_úlohy_VALUE(); continue; }
            if (Byte_údaje == 1 || Byte_údaje == 5) { kurzor_VALUE = Byte_údaje == 1 ? 0 : Veľkosť; skúsiť_znova_VALUE(); continue; }
            if (Byte_údaje == 8 || Byte_údaje == 127 || Byte_údaje == 21) {
                if (Byte_údaje == 21) { for (int Loop_INDEX = kurzor_VALUE; Loop_INDEX < Veľkosť; Loop_INDEX++) 명령해석기.riadok[Loop_INDEX - kurzor_VALUE] = 명령해석기.riadok[Loop_INDEX]; Veľkosť -= kurzor_VALUE; kurzor_VALUE = 0; }
                else if (kurzor_VALUE > 0) { int 변경전 = predný_VALUE(kurzor_VALUE); for (int Loop_INDEX = kurzor_VALUE; Loop_INDEX < Veľkosť; Loop_INDEX++) 명령해석기.riadok[Loop_INDEX - kurzor_VALUE + 변경전] = 명령해석기.riadok[Loop_INDEX]; Veľkosť -= kurzor_VALUE - 변경전; kurzor_VALUE = 변경전; }
                skúsiť_znova_VALUE(); continue;
            }
            if (Byte_údaje == 11) { Veľkosť = kurzor_VALUE; skúsiť_znova_VALUE(); continue; }
            if (Byte_údaje < 32 && Byte_údaje != 9) continue;
            if (Veľkosť == 명령해석기.riadok.length) { pretečenie = true; continue; }
            for (int Loop_INDEX = Veľkosť; Loop_INDEX > kurzor_VALUE; Loop_INDEX--) 명령해석기.riadok[Loop_INDEX] = 명령해석기.riadok[Loop_INDEX - 1];
            명령해석기.riadok[kurzor_VALUE++] = Byte_údaje; Veľkosť++;
            if (kurzor_VALUE == Veľkosť && !가로보기 && 폭(0, Veľkosť) <= 보이는폭()) Panel.직렬쓰기(Byte_údaje);
            else if (kurzor_VALUE == Veľkosť) 보이는줄(); else skúsiť_znova_VALUE();
        }
    }
}
