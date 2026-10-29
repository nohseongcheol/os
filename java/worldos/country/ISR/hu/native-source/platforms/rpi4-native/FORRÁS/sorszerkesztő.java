// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 bájt_ÉRTÉK 경계를 지키는 삽입/삭제, 방향키, Parancs LOG_REKORD, Tab Kész_ÉRTÉK. */
public final class sorszerkesztő {
    static boolean parancssor;
    static int[] LOG_REKORD = new int[16 * 1024], LOG_hossz = new int[16], tár_ÉRTÉK = new int[4096], 후보 = new int[64];
    static int LOG_DARAB, LOG_REKORD_megszüntet, keres_ÉRTÉK, 저장길이, Méret, kurzor_ÉRTÉK, 후보수, 후보길이, START_ablak;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd biztonságos_felület távoli_kijelző run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String bejegyzés_Lista, int START_pozíció, int megszüntet_pozíció, int bevitel_hossz) {
        int bájt_DARAB=0;
        for(int helyzetindex=START_pozíció;helyzetindex<megszüntet_pozíció;helyzetindex++) {
            int kódpont=bejegyzés_Lista.charAt(helyzetindex);
            if(kódpont>=0xd800 && kódpont<=0xdbff && helyzetindex+1<megszüntet_pozíció)kódpont=0x10000+((kódpont-0xd800)<<10)+bejegyzés_Lista.charAt(++helyzetindex)-0xdc00;
            int szám=kódpont<128?1:kódpont<2048?2:kódpont<65536?3:4;
            if(bájt_DARAB+szám>62)return;
            for(int szekvencia_ÉRTÉK=szám-1;szekvencia_ÉRTÉK>=0;szekvencia_ÉRTÉK--)명령후보[bájt_DARAB++]=szám==1?kódpont:szekvencia_ÉRTÉK==szám-1?(szám==2?0xc0:szám==3?0xe0:0xf0)|(kódpont>>(6*szekvencia_ÉRTÉK)):0x80|((kódpont>>(6*szekvencia_ÉRTÉK))&63);
        }
        if(bájt_DARAB<bevitel_hossz)return;
        for(int helyzetindex=0;helyzetindex<bevitel_hossz;helyzetindex++)if(명령후보[helyzetindex]!=명령해석기.Vonal[helyzetindex])return;
        후보수++;후보길이=bájt_DARAB+1;
        for(int helyzetindex=0;helyzetindex<bájt_DARAB;helyzetindex++)후보[helyzetindex]=명령후보[helyzetindex];후보[bájt_DARAB]=' ';
    }
    static int elülső_kamera_ÉRTÉK(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.Vonal[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int BACK_ÉRTÉK(int 읽는자리) { if (읽는자리 < Méret) { 읽는자리++; while (읽는자리 < Méret && (명령해석기.Vonal[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int START_pozíció, int cél_ÉRTÉK_INDEX) {
        int 글칸수 = 0;
        for (int Loop_INDEX = START_pozíció; Loop_INDEX < cél_ÉRTÉK_INDEX; Loop_INDEX++) { int bájt_adat = 명령해석기.Vonal[Loop_INDEX]; if ((bájt_adat & 192) == 128) continue; 글칸수 += bájt_adat >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void újrapróbál_ÉRTÉK() {
        단말.Írás("\r\u001b[2K");
        단말.Írás(parancssor ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 Vonal 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int OSZLOPOK = fal.Terminál(13) & 65535; return OSZLOPOK - (parancssor ? 18 : 9); }
    static void 보이는줄() {
        if (kurzor_ÉRTÉK < START_ablak) START_ablak = kurzor_ÉRTÉK;
        while (폭(START_ablak, kurzor_ÉRTÉK) > 보이는폭()) START_ablak = BACK_ÉRTÉK(START_ablak);
        int megszüntet_pozíció = START_ablak;
        while (megszüntet_pozíció < Méret && 폭(START_ablak, BACK_ÉRTÉK(megszüntet_pozíció)) <= 보이는폭()) megszüntet_pozíció = BACK_ÉRTÉK(megszüntet_pozíció);
        단말.Írás("\r\u001b["); 단말.szám(parancssor ? 16 : 7); 단말.Írás("G\u001b[K");
        if (START_ablak > 0) 단말.문자('<');
        for (int Loop_INDEX = START_ablak; Loop_INDEX < megszüntet_pozíció; Loop_INDEX++) fal.직렬쓰기(명령해석기.Vonal[Loop_INDEX]);
        단말.문자(megszüntet_pozíció < Méret ? '>' : ' ');
        단말.Írás("\u001b["); 단말.szám(폭(kurzor_ÉRTÉK, megszüntet_pozíció) + 1); 단말.문자('D');
        가로보기 = START_ablak > 0 || megszüntet_pozíció < Méret || 폭(0, Méret) > 보이는폭();
    }
    static void hozzáfűz_LOG() {
        if (!parancssor || Méret == 0 || Méret > 1024) return;
        if (LOG_DARAB > 0) {
            int 마지막자리 = (LOG_REKORD_megszüntet + 15) % 16; boolean 같은여부 = LOG_hossz[마지막자리] == Méret;
            for (int Loop_INDEX = 0; 같은여부 && Loop_INDEX < Méret; Loop_INDEX++) if (LOG_REKORD[마지막자리 * 1024 + Loop_INDEX] != 명령해석기.Vonal[Loop_INDEX]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_hossz[LOG_REKORD_megszüntet] = Méret; for (int Loop_INDEX = 0; Loop_INDEX < Méret; Loop_INDEX++) LOG_REKORD[LOG_REKORD_megszüntet * 1024 + Loop_INDEX] = 명령해석기.Vonal[Loop_INDEX];
        LOG_REKORD_megszüntet = (LOG_REKORD_megszüntet + 1) % 16; if (LOG_DARAB < 16) LOG_DARAB++;
    }
    static void 기록이동(int DELTA_ÉRTÉK) {
        if (!parancssor) return;
        if (keres_ÉRTÉK == 0 && DELTA_ÉRTÉK > 0) { 저장길이 = Méret; for (int Loop_INDEX = 0; Loop_INDEX < Méret; Loop_INDEX++) tár_ÉRTÉK[Loop_INDEX] = 명령해석기.Vonal[Loop_INDEX]; }
        int Tovább_pozíció = keres_ÉRTÉK + DELTA_ÉRTÉK; if (Tovább_pozíció < 0 || Tovább_pozíció > LOG_DARAB) return; keres_ÉRTÉK = Tovább_pozíció;
        if (keres_ÉRTÉK == 0) { Méret = 저장길이; for (int Loop_INDEX = 0; Loop_INDEX < Méret; Loop_INDEX++) 명령해석기.Vonal[Loop_INDEX] = tár_ÉRTÉK[Loop_INDEX]; }
        else { int 보관칸 = (LOG_REKORD_megszüntet + 16 - keres_ÉRTÉK) % 16; Méret = LOG_hossz[보관칸]; for (int Loop_INDEX = 0; Loop_INDEX < Méret; Loop_INDEX++) 명령해석기.Vonal[Loop_INDEX] = LOG_REKORD[보관칸 * 1024 + Loop_INDEX]; }
        kurzor_ÉRTÉK = Méret; újrapróbál_ÉRTÉK();
    }
    static void bemutató_LOG() {
        for (int bejegyzés_DARAB = 0; bejegyzés_DARAB < LOG_DARAB; bejegyzés_DARAB++) {
            int 보관칸 = (LOG_REKORD_megszüntet + 16 - LOG_DARAB + bejegyzés_DARAB) % 16; 단말.szám(bejegyzés_DARAB + 1); 단말.Írás("  ");
            for (int Loop_INDEX = 0; Loop_INDEX < LOG_hossz[보관칸]; Loop_INDEX++) fal.직렬쓰기(LOG_REKORD[보관칸 * 1024 + Loop_INDEX]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] adat_TÖMB, int START_pozíció, int bejegyzés_DARAB, int 접두말, int összesen_DARAB, boolean címtár_szám) {
        if (bejegyzés_DARAB < összesen_DARAB || bejegyzés_DARAB > 62) return;
        for (int Loop_INDEX = 0; Loop_INDEX < összesen_DARAB; Loop_INDEX++) if (adat_TÖMB[START_pozíció + Loop_INDEX] != 명령해석기.Vonal[접두말 + Loop_INDEX]) return;
        후보수++; 후보길이 = bejegyzés_DARAB + 1;
        for (int Loop_INDEX = 0; Loop_INDEX < bejegyzés_DARAB; Loop_INDEX++) 후보[Loop_INDEX] = adat_TÖMB[START_pozíció + Loop_INDEX]; 후보[bejegyzés_DARAB] = címtár_szám ? '/' : ' ';
    }
    static void Kész_ÉRTÉK() {
        if (!parancssor || kurzor_ÉRTÉK != Méret) return;
        int 시작점 = Méret; while (시작점 > 0 && 명령해석기.Vonal[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDEX = 시작점; Loop_INDEX < Méret; Loop_INDEX++) if (명령해석기.Vonal[Loop_INDEX] == '/' || 명령해석기.Vonal[Loop_INDEX] == '"' || 명령해석기.Vonal[Loop_INDEX] == 39 || 명령해석기.Vonal[Loop_INDEX] == '\\') return;
        후보수 = 0; int bejegyzés_DARAB = Méret - 시작점;
        if (시작점 == 0) {
            for(int listaindex=0;listaindex<2;listaindex++) {
                String bejegyzés_Lista=listaindex==0?명령들:관리명령.Kész_szó();
                int 읽는자리=0;
                while(읽는자리<bejegyzés_Lista.length()) {
                    int megszüntet_pozíció=읽는자리;while(megszüntet_pozíció<bejegyzés_Lista.length() && bejegyzés_Lista.charAt(megszüntet_pozíció)!=' ')megszüntet_pozíció++;
                    명령후보넣기(bejegyzés_Lista,읽는자리,megszüntet_pozíció,bejegyzés_DARAB);읽는자리=megszüntet_pozíció+1;
                }
            }
        } else {
            Memória_Files.útvonal_START(1); Memória_Files.útvonal_bájt(0, '.'); Memória_Files.normalizál_ÉRTÉK();
            for (int Loop_INDEX = 0; Loop_INDEX < Memória_Files.Fájl_DARAB; Loop_INDEX++) {
                int START_pozíció = Memória_Files.bejegyzés_START(Memória_Files.Név, Loop_INDEX * 64, Memória_Files.이름길이[Loop_INDEX]);
                if (START_pozíció >= 0) 후보넣기(Memória_Files.Név, Loop_INDEX * 64 + START_pozíció, Memória_Files.이름길이[Loop_INDEX] - START_pozíció, 시작점, bejegyzés_DARAB, false);
            }
            for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
                int START_pozíció = Memória_Files.bejegyzés_START(Memória_Files.címtár_név, Loop_INDEX * 64, Memória_Files.címtár_hossz[Loop_INDEX]);
                if (START_pozíció >= 0) 후보넣기(Memória_Files.címtár_név, Loop_INDEX * 64 + START_pozíció, Memória_Files.címtár_hossz[Loop_INDEX] - START_pozíció, 시작점, bejegyzés_DARAB, true);
            }
        }
        if (후보수 != 1) { fal.직렬쓰기(7); return; }
        for (int Loop_INDEX = bejegyzés_DARAB; Loop_INDEX < 후보길이 && Méret < 명령해석기.Vonal.length - 1; Loop_INDEX++) {
            if (후보[Loop_INDEX] == ' ' && Loop_INDEX != 후보길이 - 1) 명령해석기.Vonal[Méret++] = '\\';
            명령해석기.Vonal[Méret++] = 후보[Loop_INDEX];
        }
        kurzor_ÉRTÉK = Méret; újrapróbál_ÉRTÉK();
    }
    static int 탈출읽기() {
        int 시작점 = fal.밀리초();
        while (fal.밀리초() - 시작점 < 80) { int bájt_adat = fal.직렬읽기(); if (bájt_adat >= 0) return bájt_adat; fal.HOZAM_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int bejegyzés_DARAB = 0, megszüntet_pozíció = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 12; Loop_INDEX++) { int bájt_adat = 탈출읽기(); if (bájt_adat < 0) return; if (bájt_adat >= '0' && bájt_adat <= '9') bejegyzés_DARAB = bejegyzés_DARAB * 10 + bájt_adat - '0'; else { megszüntet_pozíció = bájt_adat; break; } }
        if (megszüntet_pozíció == 'A') 기록이동(1);
        else if (megszüntet_pozíció == 'B') 기록이동(-1);
        else if (megszüntet_pozíció == 'C') { kurzor_ÉRTÉK = BACK_ÉRTÉK(kurzor_ÉRTÉK); újrapróbál_ÉRTÉK(); }
        else if (megszüntet_pozíció == 'D') { kurzor_ÉRTÉK = elülső_kamera_ÉRTÉK(kurzor_ÉRTÉK); újrapróbál_ÉRTÉK(); }
        else if (megszüntet_pozíció == 'H' || megszüntet_pozíció == '~' && (bejegyzés_DARAB == 1 || bejegyzés_DARAB == 7)) { kurzor_ÉRTÉK = 0; újrapróbál_ÉRTÉK(); }
        else if (megszüntet_pozíció == 'F' || megszüntet_pozíció == '~' && (bejegyzés_DARAB == 4 || bejegyzés_DARAB == 8)) { kurzor_ÉRTÉK = Méret; újrapróbál_ÉRTÉK(); }
        else if (megszüntet_pozíció == '~' && bejegyzés_DARAB == 3 && kurzor_ÉRTÉK < Méret) {
            int Tovább_pozíció = BACK_ÉRTÉK(kurzor_ÉRTÉK); for (int Loop_INDEX = Tovább_pozíció; Loop_INDEX < Méret; Loop_INDEX++) 명령해석기.Vonal[Loop_INDEX - Tovább_pozíció + kurzor_ÉRTÉK] = 명령해석기.Vonal[Loop_INDEX]; Méret -= Tovább_pozíció - kurzor_ÉRTÉK; újrapróbál_ÉRTÉK();
        }
        else if (megszüntet_pozíció == '~' && (bejegyzés_DARAB == 5 || bejegyzés_DARAB == 6)) fal.Terminál(bejegyzés_DARAB == 5 ? 5 : 6);
        else if (megszüntet_pozíció == '~' && bejegyzés_DARAB == 24 && parancssor) { 명령해석기.Terminál(true); }
    }
    static int Olvasás() {
        if (!ablak_munkamenet.이어읽기) { Méret = kurzor_ÉRTÉK = keres_ÉRTÉK = START_ablak = 0; 가로보기 = false; }
        else { ablak_munkamenet.이어읽기 = false; újrapróbál_ÉRTÉK(); } boolean túlfolyás = false;
        while (true) {
            int bájt_adat = fal.직렬읽기(); if (bájt_adat == -4096) return -3;
            if (fal.Terminál(14) != 0) újrapróbál_ÉRTÉK(); if (bájt_adat < 0) { fal.HOZAM_CPU(); continue; }
            if (bájt_adat == 10 && 명령해석기.Előző_sor) { 명령해석기.Előző_sor = false; continue; } 명령해석기.Előző_sor = bájt_adat == 13;
            if (bájt_adat == 27) { 탈출(); continue; }
            if (bájt_adat == 3) { 단말.Írás("^C\n"); return -1; }
            if (bájt_adat == 4 && Méret == 0 && parancssor) { if (fal.Terminál(2) != 0) 명령해석기.Terminál(true); return -1; }
            if (bájt_adat == 13 || bájt_adat == 10) { 단말.문자(10); if (!túlfolyás) hozzáfűz_LOG(); return túlfolyás ? -2 : Méret; }
            if (bájt_adat == 9 && parancssor) { Kész_ÉRTÉK(); continue; }
            if (bájt_adat == 1 || bájt_adat == 5) { kurzor_ÉRTÉK = bájt_adat == 1 ? 0 : Méret; újrapróbál_ÉRTÉK(); continue; }
            if (bájt_adat == 8 || bájt_adat == 127 || bájt_adat == 21) {
                if (bájt_adat == 21) { for (int Loop_INDEX = kurzor_ÉRTÉK; Loop_INDEX < Méret; Loop_INDEX++) 명령해석기.Vonal[Loop_INDEX - kurzor_ÉRTÉK] = 명령해석기.Vonal[Loop_INDEX]; Méret -= kurzor_ÉRTÉK; kurzor_ÉRTÉK = 0; }
                else if (kurzor_ÉRTÉK > 0) { int 변경전 = elülső_kamera_ÉRTÉK(kurzor_ÉRTÉK); for (int Loop_INDEX = kurzor_ÉRTÉK; Loop_INDEX < Méret; Loop_INDEX++) 명령해석기.Vonal[Loop_INDEX - kurzor_ÉRTÉK + 변경전] = 명령해석기.Vonal[Loop_INDEX]; Méret -= kurzor_ÉRTÉK - 변경전; kurzor_ÉRTÉK = 변경전; }
                újrapróbál_ÉRTÉK(); continue;
            }
            if (bájt_adat == 11) { Méret = kurzor_ÉRTÉK; újrapróbál_ÉRTÉK(); continue; }
            if (bájt_adat < 32 && bájt_adat != 9) continue;
            if (Méret == 명령해석기.Vonal.length) { túlfolyás = true; continue; }
            for (int Loop_INDEX = Méret; Loop_INDEX > kurzor_ÉRTÉK; Loop_INDEX--) 명령해석기.Vonal[Loop_INDEX] = 명령해석기.Vonal[Loop_INDEX - 1];
            명령해석기.Vonal[kurzor_ÉRTÉK++] = bájt_adat; Méret++;
            if (kurzor_ÉRTÉK == Méret && !가로보기 && 폭(0, Méret) <= 보이는폭()) fal.직렬쓰기(bájt_adat);
            else if (kurzor_ÉRTÉK == Méret) 보이는줄(); else újrapróbál_ÉRTÉK();
        }
    }
}
