// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 bæti_VALUE 경계를 지키는 삽입/삭제, 방향키, Skipun LOG_lína, Tab lokið_VALUE. */
public final class lína_ritill {
    static boolean skipanalína;
    static int[] LOG_lína = new int[16 * 1024], LOG_lengd = new int[16], Store_VALUE = new int[4096], 후보 = new int[64];
    static int LOG_COUNT, LOG_lína_ljúka, Leit_VALUE, 저장길이, Stærð, bendill_VALUE, 후보수, 후보길이, Opna_gluggi;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd öruggt_skel fjartengdur_birta run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String færsla_Listi, int Opna_staða, int ljúka_staða, int 입력길이) {
        int bæti_COUNT=0;
        for(int staða_INDEX=Opna_staða;staða_INDEX<ljúka_staða;staða_INDEX++) {
            int stafkóði=færsla_Listi.charAt(staða_INDEX);
            if(stafkóði>=0xd800 && stafkóði<=0xdbff && staða_INDEX+1<ljúka_staða)stafkóði=0x10000+((stafkóði-0xd800)<<10)+færsla_Listi.charAt(++staða_INDEX)-0xdc00;
            int númer=stafkóði<128?1:stafkóði<2048?2:stafkóði<65536?3:4;
            if(bæti_COUNT+númer>62)return;
            for(int SEQUENCE_VALUE=númer-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--)명령후보[bæti_COUNT++]=númer==1?stafkóði:SEQUENCE_VALUE==númer-1?(númer==2?0xc0:númer==3?0xe0:0xf0)|(stafkóði>>(6*SEQUENCE_VALUE)):0x80|((stafkóði>>(6*SEQUENCE_VALUE))&63);
        }
        if(bæti_COUNT<입력길이)return;
        for(int staða_INDEX=0;staða_INDEX<입력길이;staða_INDEX++)if(명령후보[staða_INDEX]!=명령해석기.Lína[staða_INDEX])return;
        후보수++;후보길이=bæti_COUNT+1;
        for(int staða_INDEX=0;staða_INDEX<bæti_COUNT;staða_INDEX++)후보[staða_INDEX]=명령후보[staða_INDEX];후보[bæti_COUNT]=' ';
    }
    static int myndavél_að_framan_VALUE(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.Lína[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int TIL_BAKA_VALUE(int 읽는자리) { if (읽는자리 < Stærð) { 읽는자리++; while (읽는자리 < Stærð && (명령해석기.Lína[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int Opna_staða, int endastaður_VALUE_INDEX) {
        int 글칸수 = 0;
        for (int Loop_INDEX = Opna_staða; Loop_INDEX < endastaður_VALUE_INDEX; Loop_INDEX++) { int bæti_gögn = 명령해석기.Lína[Loop_INDEX]; if ((bæti_gögn & 192) == 128) continue; 글칸수 += bæti_gögn >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.Skrift("\r\u001b[2K");
        단말.Skrift(skipanalína ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 Lína 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int COLUMNS = bretti.Skjáhermir(13) & 65535; return COLUMNS - (skipanalína ? 18 : 9); }
    static void 보이는줄() {
        if (bendill_VALUE < Opna_gluggi) Opna_gluggi = bendill_VALUE;
        while (폭(Opna_gluggi, bendill_VALUE) > 보이는폭()) Opna_gluggi = TIL_BAKA_VALUE(Opna_gluggi);
        int ljúka_staða = Opna_gluggi;
        while (ljúka_staða < Stærð && 폭(Opna_gluggi, TIL_BAKA_VALUE(ljúka_staða)) <= 보이는폭()) ljúka_staða = TIL_BAKA_VALUE(ljúka_staða);
        단말.Skrift("\r\u001b["); 단말.númer(skipanalína ? 16 : 7); 단말.Skrift("G\u001b[K");
        if (Opna_gluggi > 0) 단말.문자('<');
        for (int Loop_INDEX = Opna_gluggi; Loop_INDEX < ljúka_staða; Loop_INDEX++) bretti.직렬쓰기(명령해석기.Lína[Loop_INDEX]);
        단말.문자(ljúka_staða < Stærð ? '>' : ' ');
        단말.Skrift("\u001b["); 단말.númer(폭(bendill_VALUE, ljúka_staða) + 1); 단말.문자('D');
        가로보기 = Opna_gluggi > 0 || ljúka_staða < Stærð || 폭(0, Stærð) > 보이는폭();
    }
    static void 기록넣기() {
        if (!skipanalína || Stærð == 0 || Stærð > 1024) return;
        if (LOG_COUNT > 0) {
            int 마지막자리 = (LOG_lína_ljúka + 15) % 16; boolean 같은여부 = LOG_lengd[마지막자리] == Stærð;
            for (int Loop_INDEX = 0; 같은여부 && Loop_INDEX < Stærð; Loop_INDEX++) if (LOG_lína[마지막자리 * 1024 + Loop_INDEX] != 명령해석기.Lína[Loop_INDEX]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_lengd[LOG_lína_ljúka] = Stærð; for (int Loop_INDEX = 0; Loop_INDEX < Stærð; Loop_INDEX++) LOG_lína[LOG_lína_ljúka * 1024 + Loop_INDEX] = 명령해석기.Lína[Loop_INDEX];
        LOG_lína_ljúka = (LOG_lína_ljúka + 1) % 16; if (LOG_COUNT < 16) LOG_COUNT++;
    }
    static void 기록이동(int DELTA_VALUE) {
        if (!skipanalína) return;
        if (Leit_VALUE == 0 && DELTA_VALUE > 0) { 저장길이 = Stærð; for (int Loop_INDEX = 0; Loop_INDEX < Stærð; Loop_INDEX++) Store_VALUE[Loop_INDEX] = 명령해석기.Lína[Loop_INDEX]; }
        int Áfram_staða = Leit_VALUE + DELTA_VALUE; if (Áfram_staða < 0 || Áfram_staða > LOG_COUNT) return; Leit_VALUE = Áfram_staða;
        if (Leit_VALUE == 0) { Stærð = 저장길이; for (int Loop_INDEX = 0; Loop_INDEX < Stærð; Loop_INDEX++) 명령해석기.Lína[Loop_INDEX] = Store_VALUE[Loop_INDEX]; }
        else { int 보관칸 = (LOG_lína_ljúka + 16 - Leit_VALUE) % 16; Stærð = LOG_lengd[보관칸]; for (int Loop_INDEX = 0; Loop_INDEX < Stærð; Loop_INDEX++) 명령해석기.Lína[Loop_INDEX] = LOG_lína[보관칸 * 1024 + Loop_INDEX]; }
        bendill_VALUE = Stærð; 다시();
    }
    static void sýna_LOG() {
        for (int færsla_COUNT = 0; færsla_COUNT < LOG_COUNT; færsla_COUNT++) {
            int 보관칸 = (LOG_lína_ljúka + 16 - LOG_COUNT + færsla_COUNT) % 16; 단말.númer(færsla_COUNT + 1); 단말.Skrift("  ");
            for (int Loop_INDEX = 0; Loop_INDEX < LOG_lengd[보관칸]; Loop_INDEX++) bretti.직렬쓰기(LOG_lína[보관칸 * 1024 + Loop_INDEX]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] gögn_ARRAY, int Opna_staða, int færsla_COUNT, int 접두말, int samtala_COUNT, boolean skráasafn_númer) {
        if (færsla_COUNT < samtala_COUNT || færsla_COUNT > 62) return;
        for (int Loop_INDEX = 0; Loop_INDEX < samtala_COUNT; Loop_INDEX++) if (gögn_ARRAY[Opna_staða + Loop_INDEX] != 명령해석기.Lína[접두말 + Loop_INDEX]) return;
        후보수++; 후보길이 = færsla_COUNT + 1;
        for (int Loop_INDEX = 0; Loop_INDEX < færsla_COUNT; Loop_INDEX++) 후보[Loop_INDEX] = gögn_ARRAY[Opna_staða + Loop_INDEX]; 후보[færsla_COUNT] = skráasafn_númer ? '/' : ' ';
    }
    static void lokið_VALUE() {
        if (!skipanalína || bendill_VALUE != Stærð) return;
        int 시작점 = Stærð; while (시작점 > 0 && 명령해석기.Lína[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDEX = 시작점; Loop_INDEX < Stærð; Loop_INDEX++) if (명령해석기.Lína[Loop_INDEX] == '/' || 명령해석기.Lína[Loop_INDEX] == '"' || 명령해석기.Lína[Loop_INDEX] == 39 || 명령해석기.Lína[Loop_INDEX] == '\\') return;
        후보수 = 0; int færsla_COUNT = Stærð - 시작점;
        if (시작점 == 0) {
            for(int Listi_INDEX=0;Listi_INDEX<2;Listi_INDEX++) {
                String færsla_Listi=Listi_INDEX==0?명령들:관리명령.lokið_Word();
                int 읽는자리=0;
                while(읽는자리<færsla_Listi.length()) {
                    int ljúka_staða=읽는자리;while(ljúka_staða<færsla_Listi.length() && færsla_Listi.charAt(ljúka_staða)!=' ')ljúka_staða++;
                    명령후보넣기(færsla_Listi,읽는자리,ljúka_staða,færsla_COUNT);읽는자리=ljúka_staða+1;
                }
            }
        } else {
            Minni_Skrár.slóð_Opna(1); Minni_Skrár.slóð_bæti(0, '.'); Minni_Skrár.staðla_VALUE();
            for (int Loop_INDEX = 0; Loop_INDEX < Minni_Skrár.skrá_COUNT; Loop_INDEX++) {
                int Opna_staða = Minni_Skrár.færsla_Opna(Minni_Skrár.Heiti, Loop_INDEX * 64, Minni_Skrár.이름길이[Loop_INDEX]);
                if (Opna_staða >= 0) 후보넣기(Minni_Skrár.Heiti, Loop_INDEX * 64 + Opna_staða, Minni_Skrár.이름길이[Loop_INDEX] - Opna_staða, 시작점, færsla_COUNT, false);
            }
            for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
                int Opna_staða = Minni_Skrár.færsla_Opna(Minni_Skrár.skráasafn_heiti, Loop_INDEX * 64, Minni_Skrár.skráasafn_lengd[Loop_INDEX]);
                if (Opna_staða >= 0) 후보넣기(Minni_Skrár.skráasafn_heiti, Loop_INDEX * 64 + Opna_staða, Minni_Skrár.skráasafn_lengd[Loop_INDEX] - Opna_staða, 시작점, færsla_COUNT, true);
            }
        }
        if (후보수 != 1) { bretti.직렬쓰기(7); return; }
        for (int Loop_INDEX = færsla_COUNT; Loop_INDEX < 후보길이 && Stærð < 명령해석기.Lína.length - 1; Loop_INDEX++) {
            if (후보[Loop_INDEX] == ' ' && Loop_INDEX != 후보길이 - 1) 명령해석기.Lína[Stærð++] = '\\';
            명령해석기.Lína[Stærð++] = 후보[Loop_INDEX];
        }
        bendill_VALUE = Stærð; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = bretti.밀리초();
        while (bretti.밀리초() - 시작점 < 80) { int bæti_gögn = bretti.직렬읽기(); if (bæti_gögn >= 0) return bæti_gögn; bretti.YIELD_örgjörvi(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int færsla_COUNT = 0, ljúka_staða = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 12; Loop_INDEX++) { int bæti_gögn = 탈출읽기(); if (bæti_gögn < 0) return; if (bæti_gögn >= '0' && bæti_gögn <= '9') færsla_COUNT = færsla_COUNT * 10 + bæti_gögn - '0'; else { ljúka_staða = bæti_gögn; break; } }
        if (ljúka_staða == 'A') 기록이동(1);
        else if (ljúka_staða == 'B') 기록이동(-1);
        else if (ljúka_staða == 'C') { bendill_VALUE = TIL_BAKA_VALUE(bendill_VALUE); 다시(); }
        else if (ljúka_staða == 'D') { bendill_VALUE = myndavél_að_framan_VALUE(bendill_VALUE); 다시(); }
        else if (ljúka_staða == 'H' || ljúka_staða == '~' && (færsla_COUNT == 1 || færsla_COUNT == 7)) { bendill_VALUE = 0; 다시(); }
        else if (ljúka_staða == 'F' || ljúka_staða == '~' && (færsla_COUNT == 4 || færsla_COUNT == 8)) { bendill_VALUE = Stærð; 다시(); }
        else if (ljúka_staða == '~' && færsla_COUNT == 3 && bendill_VALUE < Stærð) {
            int Áfram_staða = TIL_BAKA_VALUE(bendill_VALUE); for (int Loop_INDEX = Áfram_staða; Loop_INDEX < Stærð; Loop_INDEX++) 명령해석기.Lína[Loop_INDEX - Áfram_staða + bendill_VALUE] = 명령해석기.Lína[Loop_INDEX]; Stærð -= Áfram_staða - bendill_VALUE; 다시();
        }
        else if (ljúka_staða == '~' && (færsla_COUNT == 5 || færsla_COUNT == 6)) bretti.Skjáhermir(færsla_COUNT == 5 ? 5 : 6);
        else if (ljúka_staða == '~' && færsla_COUNT == 24 && skipanalína) { 명령해석기.Skjáhermir(true); }
    }
    static int Lestur() {
        if (!gluggi_lota.이어읽기) { Stærð = bendill_VALUE = Leit_VALUE = Opna_gluggi = 0; 가로보기 = false; }
        else { gluggi_lota.이어읽기 = false; 다시(); } boolean yfirflæði = false;
        while (true) {
            int bæti_gögn = bretti.직렬읽기(); if (bæti_gögn == -4096) return -3;
            if (bretti.Skjáhermir(14) != 0) 다시(); if (bæti_gögn < 0) { bretti.YIELD_örgjörvi(); continue; }
            if (bæti_gögn == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = bæti_gögn == 13;
            if (bæti_gögn == 27) { 탈출(); continue; }
            if (bæti_gögn == 3) { 단말.Skrift("^C\n"); return -1; }
            if (bæti_gögn == 4 && Stærð == 0 && skipanalína) { if (bretti.Skjáhermir(2) != 0) 명령해석기.Skjáhermir(true); return -1; }
            if (bæti_gögn == 13 || bæti_gögn == 10) { 단말.문자(10); if (!yfirflæði) 기록넣기(); return yfirflæði ? -2 : Stærð; }
            if (bæti_gögn == 9 && skipanalína) { lokið_VALUE(); continue; }
            if (bæti_gögn == 1 || bæti_gögn == 5) { bendill_VALUE = bæti_gögn == 1 ? 0 : Stærð; 다시(); continue; }
            if (bæti_gögn == 8 || bæti_gögn == 127 || bæti_gögn == 21) {
                if (bæti_gögn == 21) { for (int Loop_INDEX = bendill_VALUE; Loop_INDEX < Stærð; Loop_INDEX++) 명령해석기.Lína[Loop_INDEX - bendill_VALUE] = 명령해석기.Lína[Loop_INDEX]; Stærð -= bendill_VALUE; bendill_VALUE = 0; }
                else if (bendill_VALUE > 0) { int 변경전 = myndavél_að_framan_VALUE(bendill_VALUE); for (int Loop_INDEX = bendill_VALUE; Loop_INDEX < Stærð; Loop_INDEX++) 명령해석기.Lína[Loop_INDEX - bendill_VALUE + 변경전] = 명령해석기.Lína[Loop_INDEX]; Stærð -= bendill_VALUE - 변경전; bendill_VALUE = 변경전; }
                다시(); continue;
            }
            if (bæti_gögn == 11) { Stærð = bendill_VALUE; 다시(); continue; }
            if (bæti_gögn < 32 && bæti_gögn != 9) continue;
            if (Stærð == 명령해석기.Lína.length) { yfirflæði = true; continue; }
            for (int Loop_INDEX = Stærð; Loop_INDEX > bendill_VALUE; Loop_INDEX--) 명령해석기.Lína[Loop_INDEX] = 명령해석기.Lína[Loop_INDEX - 1];
            명령해석기.Lína[bendill_VALUE++] = bæti_gögn; Stærð++;
            if (bendill_VALUE == Stærð && !가로보기 && 폭(0, Stærð) <= 보이는폭()) bretti.직렬쓰기(bæti_gögn);
            else if (bendill_VALUE == Stærð) 보이는줄(); else 다시();
        }
    }
}
