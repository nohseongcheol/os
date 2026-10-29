// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 interaktív felület 문법. 파이프는 순차 végrehajt_parancs, 환경은 같은 셸에서 공유한다. */
public final class felület_szintaxis {
    static int[] FORRÁS = new int[4 * 4096], Altípus_ÉRTÉK = new int[4 * 128], Futtatás = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] változó_név = new int[16 * 32], változó_adat = new int[16 * 256], 이름길이 = new int[16], ÉRTÉK_hossz = new int[16];
    static int[] parancsfájl_ÉRTÉK = new int[4 * 16384];
    static int Állapot_ÉRTÉK, 깊이, 쓴수;
    static boolean 연결중, parancsfájl_megszüntet, bővítmény_hiba;
    static boolean név_karakter(int kódpont) { return kódpont >= 'a' && kódpont <= 'z' || kódpont >= 'A' && kódpont <= 'Z' || kódpont == '_' || kódpont >= 128; }
    static boolean 이름뒤(int kódpont) { return név_karakter(kódpont) || kódpont >= '0' && kódpont <= '9'; }
    static void HIBA(String Szöveg) { fal.입출력전환(0); 단말.Írás("Parancs elemez_ÉRTÉK: "); 단말.Írás(Szöveg); 단말.문자(10); Állapot_ÉRTÉK = 2; }
    static int Olvasás(int bejegyzés_DARAB, int 중첩깊이) {
        int aktuális_INDEX = 0, összesen_DARAB = 0, ALAP_pozíció = 중첩깊이 * 4096, speciális_karakter = 중첩깊이 * 128;
        while (aktuális_INDEX < bejegyzés_DARAB) {
            while (aktuális_INDEX < bejegyzés_DARAB && (FORRÁS[ALAP_pozíció + aktuális_INDEX] == 32 || FORRÁS[ALAP_pozíció + aktuális_INDEX] == 9)) aktuális_INDEX++;
            if (aktuális_INDEX == bejegyzés_DARAB || FORRÁS[ALAP_pozíció + aktuális_INDEX] == '#') break;
            if (összesen_DARAB == 128) { HIBA("낱말이 너무 많습니다"); return -1; }
            int START_pozíció = aktuális_INDEX, kódpont = FORRÁS[ALAP_pozíció + aktuális_INDEX], adat_Altípus = 0;
            if (kódpont == ';') { adat_Altípus = 1; aktuális_INDEX++; }
            else if (kódpont == '&') { if (aktuális_INDEX + 1 >= bejegyzés_DARAB || FORRÁS[ALAP_pozíció + aktuális_INDEX + 1] != '&') { HIBA("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } adat_Altípus = 2; aktuális_INDEX += 2; }
            else if (kódpont == '|') { aktuális_INDEX++; adat_Altípus = aktuális_INDEX < bejegyzés_DARAB && FORRÁS[ALAP_pozíció + aktuális_INDEX] == '|' ? 3 : 4; if (adat_Altípus == 3) aktuális_INDEX++; }
            else if (kódpont == '>') { aktuális_INDEX++; adat_Altípus = aktuális_INDEX < bejegyzés_DARAB && FORRÁS[ALAP_pozíció + aktuális_INDEX] == '>' ? 6 : 5; if (adat_Altípus == 6) aktuális_INDEX++; }
            else if (kódpont == '<') { adat_Altípus = 7; aktuális_INDEX++; }
            else {
                int Idézet = 0;
                while (aktuális_INDEX < bejegyzés_DARAB) {
                    kódpont = FORRÁS[ALAP_pozíció + aktuális_INDEX];
                    if (kódpont == '`' && Idézet != 39 || kódpont == '$' && Idézet != 39 && aktuális_INDEX + 1 < bejegyzés_DARAB && FORRÁS[ALAP_pozíció + aktuális_INDEX + 1] == '(') { HIBA("Parancs KR 치환은 지원하지 않습니다"); return -1; }
                    if (kódpont == '\\' && Idézet != 39) { if (++aktuális_INDEX == bejegyzés_DARAB) { HIBA("Vonal 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } aktuális_INDEX++; continue; }
                    if (kódpont == Idézet) { Idézet = 0; aktuális_INDEX++; continue; }
                    if (Idézet == 0 && (kódpont == 39 || kódpont == 34)) { Idézet = kódpont; aktuális_INDEX++; continue; }
                    if (Idézet == 0 && (kódpont == 32 || kódpont == 9 || kódpont == ';' || kódpont == '&' || kódpont == '|' || kódpont == '<' || kódpont == '>')) break;
                    aktuális_INDEX++;
                }
                if (Idézet != 0) { HIBA("따옴표가 닫히지 않았습니다"); return -1; }
                if (aktuális_INDEX < bejegyzés_DARAB && (FORRÁS[ALAP_pozíció + aktuális_INDEX] == '>' || FORRÁS[ALAP_pozíció + aktuális_INDEX] == '<')) {
                    boolean 수치 = aktuális_INDEX > START_pozíció;
                    for (int Loop_INDEX = START_pozíció; Loop_INDEX < aktuális_INDEX; Loop_INDEX++) if (FORRÁS[ALAP_pozíció + Loop_INDEX] < '0' || FORRÁS[ALAP_pozíció + Loop_INDEX] > '9') 수치 = false;
                    if (수치) { HIBA("번호를 지정한 Fájl 서술자 I_O 전환은 지원하지 않습니다"); return -1; }
                }
            }
            Altípus_ÉRTÉK[speciális_karakter + összesen_DARAB] = adat_Altípus; Futtatás[speciális_karakter + összesen_DARAB] = START_pozíció; 끝[speciális_karakter + összesen_DARAB] = aktuális_INDEX; összesen_DARAB++;
        }
        boolean 낱말 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < összesen_DARAB; Loop_INDEX++) {
            int 임시값 = Altípus_ÉRTÉK[speciális_karakter + Loop_INDEX];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_INDEX == összesen_DARAB || Altípus_ÉRTÉK[speciális_karakter + Loop_INDEX] != 0) { HIBA("I_O 전환에 Fájl 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_INDEX == összesen_DARAB - 1 && 임시값 != 1) { HIBA("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (összesen_DARAB > 0 && !낱말 && Altípus_ÉRTÉK[speciális_karakter + összesen_DARAB - 1] != 1) { HIBA("명령이 빠졌습니다"); return -1; }
        return összesen_DARAB;
    }
    static boolean tartomány_SMS(int[] adat_TÖMB, int helyi_START, int bejegyzés_DARAB, String karakter_pozíció) {
        if (bejegyzés_DARAB != karakter_pozíció.length()) return false; for (int Loop_INDEX = 0; Loop_INDEX < bejegyzés_DARAB; Loop_INDEX++) if (adat_TÖMB[helyi_START + Loop_INDEX] != karakter_pozíció.charAt(Loop_INDEX)) return false; return true;
    }
    static void 넣기(int bájt_adat) {
        if (쓴수 >= 명령해석기.kód_ÉRTÉK.length) { if (!bővítmény_hiba) HIBA("변수를 펼친 명령이 너무 깁니다"); bővítmény_hiba = true; return; }
        명령해석기.kód_ÉRTÉK[쓴수++] = bájt_adat;
    }
    static void változó_ÉRTÉK(int[] adat_TÖMB, int START_pozíció, int bejegyzés_DARAB) {
        if (tartomány_SMS(adat_TÖMB, START_pozíció, bejegyzés_DARAB, "PWD")) { 넣기('/'); for (int Loop_INDEX = 0; Loop_INDEX < Memória_Files.aktuális_hossz; Loop_INDEX++) 넣기(Memória_Files.aktuális_cikk[Loop_INDEX]); return; }
        if (tartomány_SMS(adat_TÖMB, START_pozíció, bejegyzés_DARAB, "HOME")) { 넣기('/'); return; }
        if (tartomány_SMS(adat_TÖMB, START_pozíció, bejegyzés_DARAB, "?")) {
            int adat_ÉRTÉK = Állapot_ÉRTÉK, számjegy = 100; boolean 시작여부 = false;
            while (számjegy > 0) { int 뒷값 = adat_ÉRTÉK / számjegy; if (뒷값 != 0 || 시작여부 || számjegy == 1) { 넣기('0' + 뒷값); 시작여부 = true; } adat_ÉRTÉK %= számjegy; számjegy /= 10; } return;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] == bejegyzés_DARAB) {
            boolean HOL_VAN = true; for (int belső_pozíció = 0; belső_pozíció < bejegyzés_DARAB; belső_pozíció++) if (változó_név[Loop_INDEX * 32 + belső_pozíció] != adat_TÖMB[START_pozíció + belső_pozíció]) HOL_VAN = false;
            if (HOL_VAN) { for (int belső_pozíció = 0; belső_pozíció < ÉRTÉK_hossz[Loop_INDEX]; belső_pozíció++) 넣기(változó_adat[Loop_INDEX * 256 + belső_pozíció]); return; }
        }
    }
    static boolean szó_ÉRTÉK(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = Futtatás[중첩깊이 * 128 + 낱말번호], megszüntet_pozíció = 끝[중첩깊이 * 128 + 낱말번호], ALAP_pozíció = 중첩깊이 * 4096, Idézet = 0;
        if (읽는자리 < megszüntet_pozíció && FORRÁS[ALAP_pozíció + 읽는자리] == '~' && (읽는자리 + 1 == megszüntet_pozíció || FORRÁS[ALAP_pozíció + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < megszüntet_pozíció) {
            int kódpont = FORRÁS[ALAP_pozíció + 읽는자리++];
            if (kódpont == Idézet) { Idézet = 0; continue; }
            if (Idézet == 0 && (kódpont == 39 || kódpont == 34)) { Idézet = kódpont; continue; }
            if (kódpont == '\\' && Idézet != 39) { int Tovább_pozíció = FORRÁS[ALAP_pozíció + 읽는자리++]; if (Idézet == 34 && Tovább_pozíció != '$' && Tovább_pozíció != '"' && Tovább_pozíció != '\\') 넣기('\\'); 넣기(Tovább_pozíció); continue; }
            if (kódpont == '$' && Idézet != 39 && 읽는자리 < megszüntet_pozíció) {
                boolean 중괄호자리 = FORRÁS[ALAP_pozíció + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < megszüntet_pozíció && FORRÁS[ALAP_pozíció + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < megszüntet_pozíció && 이름뒤(FORRÁS[ALAP_pozíció + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == megszüntet_pozíció || FORRÁS[ALAP_pozíció + 읽는자리] != '}')) { HIBA("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                változó_ÉRTÉK(FORRÁS, ALAP_pozíció + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(kódpont);
        }
        return !bővítmény_hiba;
    }
    static int környezet_Gépház(int argumentum_INDEX, boolean eltávolít) {
        int helyi_START = 명령해석기.시작점[argumentum_INDEX], megszüntet_pozíció = helyi_START + 명령해석기.hossz_ÉRTÉK[argumentum_INDEX], 같음자리 = helyi_START;
        while (같음자리 < megszüntet_pozíció && 명령해석기.kód_ÉRTÉK[같음자리] != '=') 같음자리++;
        int bejegyzés_DARAB = 같음자리 - helyi_START;
        if (bejegyzés_DARAB < 1 || bejegyzés_DARAB > 31 || !név_karakter(명령해석기.kód_ÉRTÉK[helyi_START]) || !eltávolít && 같음자리 == megszüntet_pozíció || megszüntet_pozíció - 같음자리 - 1 > 255) return 2;
        for (int Loop_INDEX = helyi_START; Loop_INDEX < 같음자리; Loop_INDEX++) if (!이름뒤(명령해석기.kód_ÉRTÉK[Loop_INDEX])) return 2;
        if (tartomány_SMS(명령해석기.kód_ÉRTÉK, helyi_START, bejegyzés_DARAB, "PWD") || tartomány_SMS(명령해석기.kód_ÉRTÉK, helyi_START, bejegyzés_DARAB, "HOME")) return 2;
        int 찾은여부 = -1, informatikai_részleg_üres_Állapot = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] == 0) informatikai_részleg_üres_Állapot = Loop_INDEX;
            if (이름길이[Loop_INDEX] != bejegyzés_DARAB) continue;
            boolean HOL_VAN = true; for (int belső_pozíció = 0; belső_pozíció < bejegyzés_DARAB; belső_pozíció++) if (változó_név[Loop_INDEX * 32 + belső_pozíció] != 명령해석기.kód_ÉRTÉK[helyi_START + belső_pozíció]) HOL_VAN = false;
            if (HOL_VAN) 찾은여부 = Loop_INDEX;
        }
        if (eltávolít) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = informatikai_részleg_üres_Állapot; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = bejegyzés_DARAB; ÉRTÉK_hossz[찾은여부] = megszüntet_pozíció - 같음자리 - 1;
        for (int Loop_INDEX = 0; Loop_INDEX < bejegyzés_DARAB; Loop_INDEX++) változó_név[찾은여부 * 32 + Loop_INDEX] = 명령해석기.kód_ÉRTÉK[helyi_START + Loop_INDEX];
        for (int Loop_INDEX = 같음자리 + 1; Loop_INDEX < megszüntet_pozíció; Loop_INDEX++) változó_adat[찾은여부 * 256 + Loop_INDEX - 같음자리 - 1] = 명령해석기.kód_ÉRTÉK[Loop_INDEX];
        return 0;
    }
    static void bemutató_környezet() {
        단말.Írás("HOME=/\nPWD="); Memória_Files.aktuális_ír(); 단말.문자(10);
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] > 0) {
            for (int belső_pozíció = 0; belső_pozíció < 이름길이[Loop_INDEX]; belső_pozíció++) fal.직렬쓰기(változó_név[Loop_INDEX * 32 + belső_pozíció]); 단말.문자('=');
            for (int belső_pozíció = 0; belső_pozíció < ÉRTÉK_hossz[Loop_INDEX]; belső_pozíció++) fal.직렬쓰기(változó_adat[Loop_INDEX * 256 + belső_pozíció]); 단말.문자(10);
        }
    }
    static void végrehajt_parancs(int[] adat_TÖMB, int 시작변위, int bejegyzés_DARAB, int 중첩깊이) {
        if (중첩깊이 >= 4 || bejegyzés_DARAB > 4096) { HIBA("Parancs 파일의 beágyazás_ÉRTÉK 또는 Vonal hossz_ÉRTÉK 제한을 넘었습니다"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < bejegyzés_DARAB; Loop_INDEX++) FORRÁS[중첩깊이 * 4096 + Loop_INDEX] = adat_TÖMB[시작변위 + Loop_INDEX];
        int összesen_DARAB = Olvasás(bejegyzés_DARAB, 중첩깊이); if (összesen_DARAB < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < összesen_DARAB) {
            int Csoport_megszüntet = 읽는자리;
            while (Csoport_megszüntet < összesen_DARAB && (Altípus_ÉRTÉK[중첩깊이 * 128 + Csoport_megszüntet] == 0 || Altípus_ÉRTÉK[중첩깊이 * 128 + Csoport_megszüntet] >= 4)) Csoport_megszüntet++;
            boolean végrehajt = 조건성립 == 1 || 조건성립 == 2 && Állapot_ÉRTÉK == 0 || 조건성립 == 3 && Állapot_ÉRTÉK != 0;
            if (végrehajt) {
                boolean Előző_cikk_INDEX = false;
                while (읽는자리 < Csoport_megszüntet) {
                    int Tovább_pozíció = 읽는자리; while (Tovább_pozíció < Csoport_megszüntet && Altípus_ÉRTÉK[중첩깊이 * 128 + Tovább_pozíció] != 4) Tovább_pozíció++;
                    boolean KAPCSOLAT_Stream = Tovább_pozíció < Csoport_megszüntet; int bevitel_lap = -1, kimenet_lap = -1, 출력방식 = 0;
                    명령해석기.kód_DARAB = 0; 쓴수 = 0; bővítmény_hiba = false;
                    for (int Loop_INDEX = 읽는자리; Loop_INDEX < Tovább_pozíció; Loop_INDEX++) {
                        int adat_Altípus = Altípus_ÉRTÉK[중첩깊이 * 128 + Loop_INDEX];
                        if (adat_Altípus >= 5) { if (adat_Altípus == 7) { if (bevitel_lap >= 0) { HIBA("bevitel_ÉRTÉK 전환이 겹쳤습니다"); return; } bevitel_lap = ++Loop_INDEX; } else { if (kimenet_lap >= 0) { HIBA("Kimenet 전환이 겹쳤습니다"); return; } kimenet_lap = ++Loop_INDEX; 출력방식 = adat_Altípus; } continue; }
                        if (명령해석기.kód_DARAB == 32) { HIBA("인수가 너무 많습니다"); return; }
                        int argumentum_INDEX = 명령해석기.kód_DARAB++; 명령해석기.시작점[argumentum_INDEX] = 쓴수;
                        if (!szó_ÉRTÉK(Loop_INDEX, 중첩깊이)) return;
                        명령해석기.hossz_ÉRTÉK[argumentum_INDEX] = 쓴수 - 명령해석기.시작점[argumentum_INDEX];
                    }
                    연결중 = Előző_cikk_INDEX || KAPCSOLAT_Stream || bevitel_lap >= 0 || kimenet_lap >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { HIBA("interaktív 명령과 Parancs 파일은 I_O 전환이나 Stream_ÉRTÉK 연결에 쓸 szám 없습니다"); return; }
                    셸입출력.Futtatás(Előző_cikk_INDEX, KAPCSOLAT_Stream);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int bejegyzés_pozíció = 입출력바꿈 == 0 ? bevitel_lap : kimenet_lap; if (bejegyzés_pozíció < 0) continue;
                        int START_pozíció = 쓴수; if (!szó_ÉRTÉK(bejegyzés_pozíció, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = Memória_Files.útvonal_START(쓴수 - START_pozíció);
                        for (int belső_pozíció = START_pozíció; 처리값 >= 0 && belső_pozíció < 쓴수; belső_pozíció++) 처리값 = Memória_Files.útvonal_bájt(belső_pozíció - START_pozíció, 명령해석기.kód_ÉRTÉK[belső_pozíció]);
                        if (처리값 >= 0) 처리값 = Memória_Files.Megnyitás(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.HIBA(처리값); Állapot_ÉRTÉK = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.bemeneti_fájl = 처리값; else 셸입출력.kimeneti_fájl = 처리값;
                    }
                    셸입출력.engedélyez_interaktív = 중첩깊이 == 0 && 읽는자리 == 0 && Tovább_pozíció == összesen_DARAB;
                    깊이 = 중첩깊이; 명령해석기.KR = 0; fal.입출력전환(1);
                    명령해석기.Parancs();
                    fal.Terminál(3);
                    int 반환값 = 명령해석기.KR, Stream_hiba = 셸입출력.hiba_ÉRTÉK;
                    셸입출력.끝(); 연결중 = false;
                    Állapot_ÉRTÉK = Stream_hiba < 0 ? 1 : 반환값;
                    if (Stream_hiba < 0) { 명령해석기.HIBA(Stream_hiba); return; }
                    if (parancsfájl_megszüntet || 반환값 == -1005) return;
                    Előző_cikk_INDEX = true; 읽는자리 = Tovább_pozíció + 1;
                }
            }
            if (Csoport_megszüntet < összesen_DARAB) 조건성립 = Altípus_ÉRTÉK[중첩깊이 * 128 + Csoport_megszüntet];
            읽는자리 = Csoport_megszüntet + 1;
        }
    }
    static void végrehajt_Fájl() {
        if (명령해석기.kód_DARAB != 2 || 깊이 >= 3) { 명령해석기.KR = 2; 단말.Írás("사용법: sh Fájl (beágyazás_ÉRTÉK 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.ÚTVONAL(1); if (처리값 >= 0) 처리값 = Memória_Files.Megnyitás(0);
        if (처리값 < 0) { 명령해석기.HIBA(처리값); return; }
        int bejegyzés_DARAB = 0, bájt_adat;
        while ((bájt_adat = Memória_Files.Olvasás(처리값)) != 256 && bájt_adat >= 0 && bejegyzés_DARAB < 16384) parancsfájl_ÉRTÉK[중첩깊이 * 16384 + bejegyzés_DARAB++] = bájt_adat;
        Memória_Files.Bezárás(처리값); fal.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < bejegyzés_DARAB && !parancsfájl_megszüntet;) {
            int megszüntet_pozíció = 읽는자리; while (megszüntet_pozíció < bejegyzés_DARAB && parancsfájl_ÉRTÉK[중첩깊이 * 16384 + megszüntet_pozíció] != 10) megszüntet_pozíció++;
            int érvényes_hossz = megszüntet_pozíció - 읽는자리; if (érvényes_hossz > 0 && parancsfájl_ÉRTÉK[중첩깊이 * 16384 + megszüntet_pozíció - 1] == 13) érvényes_hossz--;
            végrehajt_parancs(parancsfájl_ÉRTÉK, 중첩깊이 * 16384 + 읽는자리, érvényes_hossz, 중첩깊이); 읽는자리 = megszüntet_pozíció + 1;
        }
        명령해석기.KR = Állapot_ÉRTÉK; parancsfájl_megszüntet = false; 깊이 = 중첩깊이 - 1;
    }
}
