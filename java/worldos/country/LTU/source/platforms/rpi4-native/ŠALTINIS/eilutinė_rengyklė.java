// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 baitas_VALUE 경계를 지키는 삽입/삭제, 방향키, Komanda LOG_RECORD, Tab baigta_VALUE. */
public final class eilutinė_rengyklė {
    static boolean komandų_eilutė;
    static int[] LOG_RECORD = new int[16 * 1024], 기록길이 = new int[16], Store_VALUE = new int[4096], 후보 = new int[64];
    static int LOG_COUNT, LOG_RECORD_baigti_pokalbį, Ieška_VALUE, 저장길이, Dydis, žymiklis_VALUE, 후보수, 후보길이, Start_langas;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd saugus_apvalkalas nuotolinis_rodyti run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String įrašas_Sąrašas, int Start_padėtis, int baigti_pokalbį_padėtis, int 입력길이) {
        int baitas_COUNT=0;
        for(int vietos_rodyklė=Start_padėtis;vietos_rodyklė<baigti_pokalbį_padėtis;vietos_rodyklė++) {
            int simbolio_kodas=įrašas_Sąrašas.charAt(vietos_rodyklė);
            if(simbolio_kodas>=0xd800 && simbolio_kodas<=0xdbff && vietos_rodyklė+1<baigti_pokalbį_padėtis)simbolio_kodas=0x10000+((simbolio_kodas-0xd800)<<10)+įrašas_Sąrašas.charAt(++vietos_rodyklė)-0xdc00;
            int numeris=simbolio_kodas<128?1:simbolio_kodas<2048?2:simbolio_kodas<65536?3:4;
            if(baitas_COUNT+numeris>62)return;
            for(int SEQUENCE_VALUE=numeris-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--)명령후보[baitas_COUNT++]=numeris==1?simbolio_kodas:SEQUENCE_VALUE==numeris-1?(numeris==2?0xc0:numeris==3?0xe0:0xf0)|(simbolio_kodas>>(6*SEQUENCE_VALUE)):0x80|((simbolio_kodas>>(6*SEQUENCE_VALUE))&63);
        }
        if(baitas_COUNT<입력길이)return;
        for(int vietos_rodyklė=0;vietos_rodyklė<입력길이;vietos_rodyklė++)if(명령후보[vietos_rodyklė]!=명령해석기.Eilutė[vietos_rodyklė])return;
        후보수++;후보길이=baitas_COUNT+1;
        for(int vietos_rodyklė=0;vietos_rodyklė<baitas_COUNT;vietos_rodyklė++)후보[vietos_rodyklė]=명령후보[vietos_rodyklė];후보[baitas_COUNT]=' ';
    }
    static int priekinis_VALUE(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.Eilutė[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int ATGAL_VALUE(int 읽는자리) { if (읽는자리 < Dydis) { 읽는자리++; while (읽는자리 < Dydis && (명령해석기.Eilutė[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int Start_padėtis, int vieta_VALUE_INDEX) {
        int 글칸수 = 0;
        for (int Loop_INDEX = Start_padėtis; Loop_INDEX < vieta_VALUE_INDEX; Loop_INDEX++) { int baitas_duomenys = 명령해석기.Eilutė[Loop_INDEX]; if ((baitas_duomenys & 192) == 128) continue; 글칸수 += baitas_duomenys >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void kartoti_VALUE() {
        단말.Rašymas("\r\u001b[2K");
        단말.Rašymas(komandų_eilutė ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 Eilutė 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int COLUMNS = Lenta.Terminalas(13) & 65535; return COLUMNS - (komandų_eilutė ? 18 : 9); }
    static void 보이는줄() {
        if (žymiklis_VALUE < Start_langas) Start_langas = žymiklis_VALUE;
        while (폭(Start_langas, žymiklis_VALUE) > 보이는폭()) Start_langas = ATGAL_VALUE(Start_langas);
        int baigti_pokalbį_padėtis = Start_langas;
        while (baigti_pokalbį_padėtis < Dydis && 폭(Start_langas, ATGAL_VALUE(baigti_pokalbį_padėtis)) <= 보이는폭()) baigti_pokalbį_padėtis = ATGAL_VALUE(baigti_pokalbį_padėtis);
        단말.Rašymas("\r\u001b["); 단말.numeris(komandų_eilutė ? 16 : 7); 단말.Rašymas("G\u001b[K");
        if (Start_langas > 0) 단말.문자('<');
        for (int Loop_INDEX = Start_langas; Loop_INDEX < baigti_pokalbį_padėtis; Loop_INDEX++) Lenta.직렬쓰기(명령해석기.Eilutė[Loop_INDEX]);
        단말.문자(baigti_pokalbį_padėtis < Dydis ? '>' : ' ');
        단말.Rašymas("\u001b["); 단말.numeris(폭(žymiklis_VALUE, baigti_pokalbį_padėtis) + 1); 단말.문자('D');
        가로보기 = Start_langas > 0 || baigti_pokalbį_padėtis < Dydis || 폭(0, Dydis) > 보이는폭();
    }
    static void sujungti_LOG() {
        if (!komandų_eilutė || Dydis == 0 || Dydis > 1024) return;
        if (LOG_COUNT > 0) {
            int 마지막자리 = (LOG_RECORD_baigti_pokalbį + 15) % 16; boolean 같은여부 = 기록길이[마지막자리] == Dydis;
            for (int Loop_INDEX = 0; 같은여부 && Loop_INDEX < Dydis; Loop_INDEX++) if (LOG_RECORD[마지막자리 * 1024 + Loop_INDEX] != 명령해석기.Eilutė[Loop_INDEX]) 같은여부 = false;
            if (같은여부) return;
        }
        기록길이[LOG_RECORD_baigti_pokalbį] = Dydis; for (int Loop_INDEX = 0; Loop_INDEX < Dydis; Loop_INDEX++) LOG_RECORD[LOG_RECORD_baigti_pokalbį * 1024 + Loop_INDEX] = 명령해석기.Eilutė[Loop_INDEX];
        LOG_RECORD_baigti_pokalbį = (LOG_RECORD_baigti_pokalbį + 1) % 16; if (LOG_COUNT < 16) LOG_COUNT++;
    }
    static void 기록이동(int DELTA_VALUE) {
        if (!komandų_eilutė) return;
        if (Ieška_VALUE == 0 && DELTA_VALUE > 0) { 저장길이 = Dydis; for (int Loop_INDEX = 0; Loop_INDEX < Dydis; Loop_INDEX++) Store_VALUE[Loop_INDEX] = 명령해석기.Eilutė[Loop_INDEX]; }
        int toliau_padėtis = Ieška_VALUE + DELTA_VALUE; if (toliau_padėtis < 0 || toliau_padėtis > LOG_COUNT) return; Ieška_VALUE = toliau_padėtis;
        if (Ieška_VALUE == 0) { Dydis = 저장길이; for (int Loop_INDEX = 0; Loop_INDEX < Dydis; Loop_INDEX++) 명령해석기.Eilutė[Loop_INDEX] = Store_VALUE[Loop_INDEX]; }
        else { int 보관칸 = (LOG_RECORD_baigti_pokalbį + 16 - Ieška_VALUE) % 16; Dydis = 기록길이[보관칸]; for (int Loop_INDEX = 0; Loop_INDEX < Dydis; Loop_INDEX++) 명령해석기.Eilutė[Loop_INDEX] = LOG_RECORD[보관칸 * 1024 + Loop_INDEX]; }
        žymiklis_VALUE = Dydis; kartoti_VALUE();
    }
    static void laida_LOG() {
        for (int įrašas_COUNT = 0; įrašas_COUNT < LOG_COUNT; įrašas_COUNT++) {
            int 보관칸 = (LOG_RECORD_baigti_pokalbį + 16 - LOG_COUNT + įrašas_COUNT) % 16; 단말.numeris(įrašas_COUNT + 1); 단말.Rašymas("  ");
            for (int Loop_INDEX = 0; Loop_INDEX < 기록길이[보관칸]; Loop_INDEX++) Lenta.직렬쓰기(LOG_RECORD[보관칸 * 1024 + Loop_INDEX]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] duomenys_ARRAY, int Start_padėtis, int įrašas_COUNT, int 접두말, int bendras_COUNT, boolean Katalogas_numeris) {
        if (įrašas_COUNT < bendras_COUNT || įrašas_COUNT > 62) return;
        for (int Loop_INDEX = 0; Loop_INDEX < bendras_COUNT; Loop_INDEX++) if (duomenys_ARRAY[Start_padėtis + Loop_INDEX] != 명령해석기.Eilutė[접두말 + Loop_INDEX]) return;
        후보수++; 후보길이 = įrašas_COUNT + 1;
        for (int Loop_INDEX = 0; Loop_INDEX < įrašas_COUNT; Loop_INDEX++) 후보[Loop_INDEX] = duomenys_ARRAY[Start_padėtis + Loop_INDEX]; 후보[įrašas_COUNT] = Katalogas_numeris ? '/' : ' ';
    }
    static void baigta_VALUE() {
        if (!komandų_eilutė || žymiklis_VALUE != Dydis) return;
        int 시작점 = Dydis; while (시작점 > 0 && 명령해석기.Eilutė[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDEX = 시작점; Loop_INDEX < Dydis; Loop_INDEX++) if (명령해석기.Eilutė[Loop_INDEX] == '/' || 명령해석기.Eilutė[Loop_INDEX] == '"' || 명령해석기.Eilutė[Loop_INDEX] == 39 || 명령해석기.Eilutė[Loop_INDEX] == '\\') return;
        후보수 = 0; int įrašas_COUNT = Dydis - 시작점;
        if (시작점 == 0) {
            for(int sąrašo_rodyklė=0;sąrašo_rodyklė<2;sąrašo_rodyklė++) {
                String įrašas_Sąrašas=sąrašo_rodyklė==0?명령들:관리명령.baigta_Word();
                int 읽는자리=0;
                while(읽는자리<įrašas_Sąrašas.length()) {
                    int baigti_pokalbį_padėtis=읽는자리;while(baigti_pokalbį_padėtis<įrašas_Sąrašas.length() && įrašas_Sąrašas.charAt(baigti_pokalbį_padėtis)!=' ')baigti_pokalbį_padėtis++;
                    명령후보넣기(įrašas_Sąrašas,읽는자리,baigti_pokalbį_padėtis,įrašas_COUNT);읽는자리=baigti_pokalbį_padėtis+1;
                }
            }
        } else {
            atmintis_Failai.kelias_Start(1); atmintis_Failai.kelias_baitas(0, '.'); atmintis_Failai.normalizuoti_VALUE();
            for (int Loop_INDEX = 0; Loop_INDEX < atmintis_Failai.Failas_COUNT; Loop_INDEX++) {
                int Start_padėtis = atmintis_Failai.įrašas_Start(atmintis_Failai.Pavadinimas_2, Loop_INDEX * 64, atmintis_Failai.이름길이[Loop_INDEX]);
                if (Start_padėtis >= 0) 후보넣기(atmintis_Failai.Pavadinimas_2, Loop_INDEX * 64 + Start_padėtis, atmintis_Failai.이름길이[Loop_INDEX] - Start_padėtis, 시작점, įrašas_COUNT, false);
            }
            for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
                int Start_padėtis = atmintis_Failai.įrašas_Start(atmintis_Failai.Katalogas_pavadinimas, Loop_INDEX * 64, atmintis_Failai.폴더길이[Loop_INDEX]);
                if (Start_padėtis >= 0) 후보넣기(atmintis_Failai.Katalogas_pavadinimas, Loop_INDEX * 64 + Start_padėtis, atmintis_Failai.폴더길이[Loop_INDEX] - Start_padėtis, 시작점, įrašas_COUNT, true);
            }
        }
        if (후보수 != 1) { Lenta.직렬쓰기(7); return; }
        for (int Loop_INDEX = įrašas_COUNT; Loop_INDEX < 후보길이 && Dydis < 명령해석기.Eilutė.length - 1; Loop_INDEX++) {
            if (후보[Loop_INDEX] == ' ' && Loop_INDEX != 후보길이 - 1) 명령해석기.Eilutė[Dydis++] = '\\';
            명령해석기.Eilutė[Dydis++] = 후보[Loop_INDEX];
        }
        žymiklis_VALUE = Dydis; kartoti_VALUE();
    }
    static int 탈출읽기() {
        int 시작점 = Lenta.밀리초();
        while (Lenta.밀리초() - 시작점 < 80) { int baitas_duomenys = Lenta.직렬읽기(); if (baitas_duomenys >= 0) return baitas_duomenys; Lenta.YIELD_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int įrašas_COUNT = 0, baigti_pokalbį_padėtis = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 12; Loop_INDEX++) { int baitas_duomenys = 탈출읽기(); if (baitas_duomenys < 0) return; if (baitas_duomenys >= '0' && baitas_duomenys <= '9') įrašas_COUNT = įrašas_COUNT * 10 + baitas_duomenys - '0'; else { baigti_pokalbį_padėtis = baitas_duomenys; break; } }
        if (baigti_pokalbį_padėtis == 'A') 기록이동(1);
        else if (baigti_pokalbį_padėtis == 'B') 기록이동(-1);
        else if (baigti_pokalbį_padėtis == 'C') { žymiklis_VALUE = ATGAL_VALUE(žymiklis_VALUE); kartoti_VALUE(); }
        else if (baigti_pokalbį_padėtis == 'D') { žymiklis_VALUE = priekinis_VALUE(žymiklis_VALUE); kartoti_VALUE(); }
        else if (baigti_pokalbį_padėtis == 'H' || baigti_pokalbį_padėtis == '~' && (įrašas_COUNT == 1 || įrašas_COUNT == 7)) { žymiklis_VALUE = 0; kartoti_VALUE(); }
        else if (baigti_pokalbį_padėtis == 'F' || baigti_pokalbį_padėtis == '~' && (įrašas_COUNT == 4 || įrašas_COUNT == 8)) { žymiklis_VALUE = Dydis; kartoti_VALUE(); }
        else if (baigti_pokalbį_padėtis == '~' && įrašas_COUNT == 3 && žymiklis_VALUE < Dydis) {
            int toliau_padėtis = ATGAL_VALUE(žymiklis_VALUE); for (int Loop_INDEX = toliau_padėtis; Loop_INDEX < Dydis; Loop_INDEX++) 명령해석기.Eilutė[Loop_INDEX - toliau_padėtis + žymiklis_VALUE] = 명령해석기.Eilutė[Loop_INDEX]; Dydis -= toliau_padėtis - žymiklis_VALUE; kartoti_VALUE();
        }
        else if (baigti_pokalbį_padėtis == '~' && (įrašas_COUNT == 5 || įrašas_COUNT == 6)) Lenta.Terminalas(įrašas_COUNT == 5 ? 5 : 6);
        else if (baigti_pokalbį_padėtis == '~' && įrašas_COUNT == 24 && komandų_eilutė) { 명령해석기.Terminalas(true); }
    }
    static int Skaitymas() {
        if (!langas_seansas.이어읽기) { Dydis = žymiklis_VALUE = Ieška_VALUE = Start_langas = 0; 가로보기 = false; }
        else { langas_seansas.이어읽기 = false; kartoti_VALUE(); } boolean perpilda = false;
        while (true) {
            int baitas_duomenys = Lenta.직렬읽기(); if (baitas_duomenys == -4096) return -3;
            if (Lenta.Terminalas(14) != 0) kartoti_VALUE(); if (baitas_duomenys < 0) { Lenta.YIELD_CPU(); continue; }
            if (baitas_duomenys == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = baitas_duomenys == 13;
            if (baitas_duomenys == 27) { 탈출(); continue; }
            if (baitas_duomenys == 3) { 단말.Rašymas("^C\n"); return -1; }
            if (baitas_duomenys == 4 && Dydis == 0 && komandų_eilutė) { if (Lenta.Terminalas(2) != 0) 명령해석기.Terminalas(true); return -1; }
            if (baitas_duomenys == 13 || baitas_duomenys == 10) { 단말.문자(10); if (!perpilda) sujungti_LOG(); return perpilda ? -2 : Dydis; }
            if (baitas_duomenys == 9 && komandų_eilutė) { baigta_VALUE(); continue; }
            if (baitas_duomenys == 1 || baitas_duomenys == 5) { žymiklis_VALUE = baitas_duomenys == 1 ? 0 : Dydis; kartoti_VALUE(); continue; }
            if (baitas_duomenys == 8 || baitas_duomenys == 127 || baitas_duomenys == 21) {
                if (baitas_duomenys == 21) { for (int Loop_INDEX = žymiklis_VALUE; Loop_INDEX < Dydis; Loop_INDEX++) 명령해석기.Eilutė[Loop_INDEX - žymiklis_VALUE] = 명령해석기.Eilutė[Loop_INDEX]; Dydis -= žymiklis_VALUE; žymiklis_VALUE = 0; }
                else if (žymiklis_VALUE > 0) { int 변경전 = priekinis_VALUE(žymiklis_VALUE); for (int Loop_INDEX = žymiklis_VALUE; Loop_INDEX < Dydis; Loop_INDEX++) 명령해석기.Eilutė[Loop_INDEX - žymiklis_VALUE + 변경전] = 명령해석기.Eilutė[Loop_INDEX]; Dydis -= žymiklis_VALUE - 변경전; žymiklis_VALUE = 변경전; }
                kartoti_VALUE(); continue;
            }
            if (baitas_duomenys == 11) { Dydis = žymiklis_VALUE; kartoti_VALUE(); continue; }
            if (baitas_duomenys < 32 && baitas_duomenys != 9) continue;
            if (Dydis == 명령해석기.Eilutė.length) { perpilda = true; continue; }
            for (int Loop_INDEX = Dydis; Loop_INDEX > žymiklis_VALUE; Loop_INDEX--) 명령해석기.Eilutė[Loop_INDEX] = 명령해석기.Eilutė[Loop_INDEX - 1];
            명령해석기.Eilutė[žymiklis_VALUE++] = baitas_duomenys; Dydis++;
            if (žymiklis_VALUE == Dydis && !가로보기 && 폭(0, Dydis) <= 보이는폭()) Lenta.직렬쓰기(baitas_duomenys);
            else if (žymiklis_VALUE == Dydis) 보이는줄(); else kartoti_VALUE();
        }
    }
}
