// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 byte_VALUE 경계를 지키는 삽입/삭제, 방향키, Komanda LOG_RECORD, Tab Pabeigti_VALUE. */
public final class rindiņas_redaktors {
    static boolean komandrinda;
    static int[] LOG_RECORD = new int[16 * 1024], 기록길이 = new int[16], Store_VALUE = new int[4096], 후보 = new int[64];
    static int LOG_COUNT, LOG_RECORD_beigt_zvanu, Meklēt_VALUE, 저장길이, Izmērs, kursors_VALUE, 후보수, 후보길이, Sākt_logs;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd drošs_čaula attāls_rādīt run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String ievade_Saraksts, int Sākt_amats, int beigt_zvanu_amats, int 입력길이) {
        int byte_COUNT=0;
        for(int pozīcijas_indekss=Sākt_amats;pozīcijas_indekss<beigt_zvanu_amats;pozīcijas_indekss++) {
            int koda_punkts=ievade_Saraksts.charAt(pozīcijas_indekss);
            if(koda_punkts>=0xd800 && koda_punkts<=0xdbff && pozīcijas_indekss+1<beigt_zvanu_amats)koda_punkts=0x10000+((koda_punkts-0xd800)<<10)+ievade_Saraksts.charAt(++pozīcijas_indekss)-0xdc00;
            int numurs=koda_punkts<128?1:koda_punkts<2048?2:koda_punkts<65536?3:4;
            if(byte_COUNT+numurs>62)return;
            for(int SEQUENCE_VALUE=numurs-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--)명령후보[byte_COUNT++]=numurs==1?koda_punkts:SEQUENCE_VALUE==numurs-1?(numurs==2?0xc0:numurs==3?0xe0:0xf0)|(koda_punkts>>(6*SEQUENCE_VALUE)):0x80|((koda_punkts>>(6*SEQUENCE_VALUE))&63);
        }
        if(byte_COUNT<입력길이)return;
        for(int pozīcijas_indekss=0;pozīcijas_indekss<입력길이;pozīcijas_indekss++)if(명령후보[pozīcijas_indekss]!=명령해석기.Līniju[pozīcijas_indekss])return;
        후보수++;후보길이=byte_COUNT+1;
        for(int pozīcijas_indekss=0;pozīcijas_indekss<byte_COUNT;pozīcijas_indekss++)후보[pozīcijas_indekss]=명령후보[pozīcijas_indekss];후보[byte_COUNT]=' ';
    }
    static int priekšējā_VALUE(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.Līniju[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int ATPAKAĻ_VALUE(int 읽는자리) { if (읽는자리 < Izmērs) { 읽는자리++; while (읽는자리 < Izmērs && (명령해석기.Līniju[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int Sākt_amats, int mērķis_VALUE_INDEX) {
        int 글칸수 = 0;
        for (int Loop_INDEX = Sākt_amats; Loop_INDEX < mērķis_VALUE_INDEX; Loop_INDEX++) { int byte_dati = 명령해석기.Līniju[Loop_INDEX]; if ((byte_dati & 192) == 128) continue; 글칸수 += byte_dati >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void mēģināt_vēlreiz_VALUE() {
        단말.Rakstīt("\r\u001b[2K");
        단말.Rakstīt(komandrinda ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 Līniju 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int COLUMNS = Panelis.Terminālis(13) & 65535; return COLUMNS - (komandrinda ? 18 : 9); }
    static void 보이는줄() {
        if (kursors_VALUE < Sākt_logs) Sākt_logs = kursors_VALUE;
        while (폭(Sākt_logs, kursors_VALUE) > 보이는폭()) Sākt_logs = ATPAKAĻ_VALUE(Sākt_logs);
        int beigt_zvanu_amats = Sākt_logs;
        while (beigt_zvanu_amats < Izmērs && 폭(Sākt_logs, ATPAKAĻ_VALUE(beigt_zvanu_amats)) <= 보이는폭()) beigt_zvanu_amats = ATPAKAĻ_VALUE(beigt_zvanu_amats);
        단말.Rakstīt("\r\u001b["); 단말.numurs(komandrinda ? 16 : 7); 단말.Rakstīt("G\u001b[K");
        if (Sākt_logs > 0) 단말.문자('<');
        for (int Loop_INDEX = Sākt_logs; Loop_INDEX < beigt_zvanu_amats; Loop_INDEX++) Panelis.직렬쓰기(명령해석기.Līniju[Loop_INDEX]);
        단말.문자(beigt_zvanu_amats < Izmērs ? '>' : ' ');
        단말.Rakstīt("\u001b["); 단말.numurs(폭(kursors_VALUE, beigt_zvanu_amats) + 1); 단말.문자('D');
        가로보기 = Sākt_logs > 0 || beigt_zvanu_amats < Izmērs || 폭(0, Izmērs) > 보이는폭();
    }
    static void Pievienot_LOG() {
        if (!komandrinda || Izmērs == 0 || Izmērs > 1024) return;
        if (LOG_COUNT > 0) {
            int 마지막자리 = (LOG_RECORD_beigt_zvanu + 15) % 16; boolean 같은여부 = 기록길이[마지막자리] == Izmērs;
            for (int Loop_INDEX = 0; 같은여부 && Loop_INDEX < Izmērs; Loop_INDEX++) if (LOG_RECORD[마지막자리 * 1024 + Loop_INDEX] != 명령해석기.Līniju[Loop_INDEX]) 같은여부 = false;
            if (같은여부) return;
        }
        기록길이[LOG_RECORD_beigt_zvanu] = Izmērs; for (int Loop_INDEX = 0; Loop_INDEX < Izmērs; Loop_INDEX++) LOG_RECORD[LOG_RECORD_beigt_zvanu * 1024 + Loop_INDEX] = 명령해석기.Līniju[Loop_INDEX];
        LOG_RECORD_beigt_zvanu = (LOG_RECORD_beigt_zvanu + 1) % 16; if (LOG_COUNT < 16) LOG_COUNT++;
    }
    static void 기록이동(int DELTA_VALUE) {
        if (!komandrinda) return;
        if (Meklēt_VALUE == 0 && DELTA_VALUE > 0) { 저장길이 = Izmērs; for (int Loop_INDEX = 0; Loop_INDEX < Izmērs; Loop_INDEX++) Store_VALUE[Loop_INDEX] = 명령해석기.Līniju[Loop_INDEX]; }
        int Tālāk_amats = Meklēt_VALUE + DELTA_VALUE; if (Tālāk_amats < 0 || Tālāk_amats > LOG_COUNT) return; Meklēt_VALUE = Tālāk_amats;
        if (Meklēt_VALUE == 0) { Izmērs = 저장길이; for (int Loop_INDEX = 0; Loop_INDEX < Izmērs; Loop_INDEX++) 명령해석기.Līniju[Loop_INDEX] = Store_VALUE[Loop_INDEX]; }
        else { int 보관칸 = (LOG_RECORD_beigt_zvanu + 16 - Meklēt_VALUE) % 16; Izmērs = 기록길이[보관칸]; for (int Loop_INDEX = 0; Loop_INDEX < Izmērs; Loop_INDEX++) 명령해석기.Līniju[Loop_INDEX] = LOG_RECORD[보관칸 * 1024 + Loop_INDEX]; }
        kursors_VALUE = Izmērs; mēģināt_vēlreiz_VALUE();
    }
    static void rādīt_LOG() {
        for (int ievade_COUNT = 0; ievade_COUNT < LOG_COUNT; ievade_COUNT++) {
            int 보관칸 = (LOG_RECORD_beigt_zvanu + 16 - LOG_COUNT + ievade_COUNT) % 16; 단말.numurs(ievade_COUNT + 1); 단말.Rakstīt("  ");
            for (int Loop_INDEX = 0; Loop_INDEX < 기록길이[보관칸]; Loop_INDEX++) Panelis.직렬쓰기(LOG_RECORD[보관칸 * 1024 + Loop_INDEX]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] dati_ARRAY, int Sākt_amats, int ievade_COUNT, int 접두말, int kopsumma_COUNT, boolean Direktorijs_numurs) {
        if (ievade_COUNT < kopsumma_COUNT || ievade_COUNT > 62) return;
        for (int Loop_INDEX = 0; Loop_INDEX < kopsumma_COUNT; Loop_INDEX++) if (dati_ARRAY[Sākt_amats + Loop_INDEX] != 명령해석기.Līniju[접두말 + Loop_INDEX]) return;
        후보수++; 후보길이 = ievade_COUNT + 1;
        for (int Loop_INDEX = 0; Loop_INDEX < ievade_COUNT; Loop_INDEX++) 후보[Loop_INDEX] = dati_ARRAY[Sākt_amats + Loop_INDEX]; 후보[ievade_COUNT] = Direktorijs_numurs ? '/' : ' ';
    }
    static void Pabeigti_VALUE() {
        if (!komandrinda || kursors_VALUE != Izmērs) return;
        int 시작점 = Izmērs; while (시작점 > 0 && 명령해석기.Līniju[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDEX = 시작점; Loop_INDEX < Izmērs; Loop_INDEX++) if (명령해석기.Līniju[Loop_INDEX] == '/' || 명령해석기.Līniju[Loop_INDEX] == '"' || 명령해석기.Līniju[Loop_INDEX] == 39 || 명령해석기.Līniju[Loop_INDEX] == '\\') return;
        후보수 = 0; int ievade_COUNT = Izmērs - 시작점;
        if (시작점 == 0) {
            for(int satura_indekss=0;satura_indekss<2;satura_indekss++) {
                String ievade_Saraksts=satura_indekss==0?명령들:관리명령.Pabeigti_Word();
                int 읽는자리=0;
                while(읽는자리<ievade_Saraksts.length()) {
                    int beigt_zvanu_amats=읽는자리;while(beigt_zvanu_amats<ievade_Saraksts.length() && ievade_Saraksts.charAt(beigt_zvanu_amats)!=' ')beigt_zvanu_amats++;
                    명령후보넣기(ievade_Saraksts,읽는자리,beigt_zvanu_amats,ievade_COUNT);읽는자리=beigt_zvanu_amats+1;
                }
            }
        } else {
            atmiņa_Faili.ceļš_Sākt(1); atmiņa_Faili.ceļš_byte(0, '.'); atmiņa_Faili.normalizēt_VALUE();
            for (int Loop_INDEX = 0; Loop_INDEX < atmiņa_Faili.Fails_COUNT; Loop_INDEX++) {
                int Sākt_amats = atmiņa_Faili.ievade_Sākt(atmiņa_Faili.Nosaukums, Loop_INDEX * 64, atmiņa_Faili.이름길이[Loop_INDEX]);
                if (Sākt_amats >= 0) 후보넣기(atmiņa_Faili.Nosaukums, Loop_INDEX * 64 + Sākt_amats, atmiņa_Faili.이름길이[Loop_INDEX] - Sākt_amats, 시작점, ievade_COUNT, false);
            }
            for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
                int Sākt_amats = atmiņa_Faili.ievade_Sākt(atmiņa_Faili.Direktorijs_nosaukums, Loop_INDEX * 64, atmiņa_Faili.폴더길이[Loop_INDEX]);
                if (Sākt_amats >= 0) 후보넣기(atmiņa_Faili.Direktorijs_nosaukums, Loop_INDEX * 64 + Sākt_amats, atmiņa_Faili.폴더길이[Loop_INDEX] - Sākt_amats, 시작점, ievade_COUNT, true);
            }
        }
        if (후보수 != 1) { Panelis.직렬쓰기(7); return; }
        for (int Loop_INDEX = ievade_COUNT; Loop_INDEX < 후보길이 && Izmērs < 명령해석기.Līniju.length - 1; Loop_INDEX++) {
            if (후보[Loop_INDEX] == ' ' && Loop_INDEX != 후보길이 - 1) 명령해석기.Līniju[Izmērs++] = '\\';
            명령해석기.Līniju[Izmērs++] = 후보[Loop_INDEX];
        }
        kursors_VALUE = Izmērs; mēģināt_vēlreiz_VALUE();
    }
    static int 탈출읽기() {
        int 시작점 = Panelis.밀리초();
        while (Panelis.밀리초() - 시작점 < 80) { int byte_dati = Panelis.직렬읽기(); if (byte_dati >= 0) return byte_dati; Panelis.YIELD_apstrādātājs(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int ievade_COUNT = 0, beigt_zvanu_amats = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 12; Loop_INDEX++) { int byte_dati = 탈출읽기(); if (byte_dati < 0) return; if (byte_dati >= '0' && byte_dati <= '9') ievade_COUNT = ievade_COUNT * 10 + byte_dati - '0'; else { beigt_zvanu_amats = byte_dati; break; } }
        if (beigt_zvanu_amats == 'A') 기록이동(1);
        else if (beigt_zvanu_amats == 'B') 기록이동(-1);
        else if (beigt_zvanu_amats == 'C') { kursors_VALUE = ATPAKAĻ_VALUE(kursors_VALUE); mēģināt_vēlreiz_VALUE(); }
        else if (beigt_zvanu_amats == 'D') { kursors_VALUE = priekšējā_VALUE(kursors_VALUE); mēģināt_vēlreiz_VALUE(); }
        else if (beigt_zvanu_amats == 'H' || beigt_zvanu_amats == '~' && (ievade_COUNT == 1 || ievade_COUNT == 7)) { kursors_VALUE = 0; mēģināt_vēlreiz_VALUE(); }
        else if (beigt_zvanu_amats == 'F' || beigt_zvanu_amats == '~' && (ievade_COUNT == 4 || ievade_COUNT == 8)) { kursors_VALUE = Izmērs; mēģināt_vēlreiz_VALUE(); }
        else if (beigt_zvanu_amats == '~' && ievade_COUNT == 3 && kursors_VALUE < Izmērs) {
            int Tālāk_amats = ATPAKAĻ_VALUE(kursors_VALUE); for (int Loop_INDEX = Tālāk_amats; Loop_INDEX < Izmērs; Loop_INDEX++) 명령해석기.Līniju[Loop_INDEX - Tālāk_amats + kursors_VALUE] = 명령해석기.Līniju[Loop_INDEX]; Izmērs -= Tālāk_amats - kursors_VALUE; mēģināt_vēlreiz_VALUE();
        }
        else if (beigt_zvanu_amats == '~' && (ievade_COUNT == 5 || ievade_COUNT == 6)) Panelis.Terminālis(ievade_COUNT == 5 ? 5 : 6);
        else if (beigt_zvanu_amats == '~' && ievade_COUNT == 24 && komandrinda) { 명령해석기.Terminālis(true); }
    }
    static int Lasīt() {
        if (!logs_sesija.이어읽기) { Izmērs = kursors_VALUE = Meklēt_VALUE = Sākt_logs = 0; 가로보기 = false; }
        else { logs_sesija.이어읽기 = false; mēģināt_vēlreiz_VALUE(); } boolean pārpilde = false;
        while (true) {
            int byte_dati = Panelis.직렬읽기(); if (byte_dati == -4096) return -3;
            if (Panelis.Terminālis(14) != 0) mēģināt_vēlreiz_VALUE(); if (byte_dati < 0) { Panelis.YIELD_apstrādātājs(); continue; }
            if (byte_dati == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = byte_dati == 13;
            if (byte_dati == 27) { 탈출(); continue; }
            if (byte_dati == 3) { 단말.Rakstīt("^C\n"); return -1; }
            if (byte_dati == 4 && Izmērs == 0 && komandrinda) { if (Panelis.Terminālis(2) != 0) 명령해석기.Terminālis(true); return -1; }
            if (byte_dati == 13 || byte_dati == 10) { 단말.문자(10); if (!pārpilde) Pievienot_LOG(); return pārpilde ? -2 : Izmērs; }
            if (byte_dati == 9 && komandrinda) { Pabeigti_VALUE(); continue; }
            if (byte_dati == 1 || byte_dati == 5) { kursors_VALUE = byte_dati == 1 ? 0 : Izmērs; mēģināt_vēlreiz_VALUE(); continue; }
            if (byte_dati == 8 || byte_dati == 127 || byte_dati == 21) {
                if (byte_dati == 21) { for (int Loop_INDEX = kursors_VALUE; Loop_INDEX < Izmērs; Loop_INDEX++) 명령해석기.Līniju[Loop_INDEX - kursors_VALUE] = 명령해석기.Līniju[Loop_INDEX]; Izmērs -= kursors_VALUE; kursors_VALUE = 0; }
                else if (kursors_VALUE > 0) { int 변경전 = priekšējā_VALUE(kursors_VALUE); for (int Loop_INDEX = kursors_VALUE; Loop_INDEX < Izmērs; Loop_INDEX++) 명령해석기.Līniju[Loop_INDEX - kursors_VALUE + 변경전] = 명령해석기.Līniju[Loop_INDEX]; Izmērs -= kursors_VALUE - 변경전; kursors_VALUE = 변경전; }
                mēģināt_vēlreiz_VALUE(); continue;
            }
            if (byte_dati == 11) { Izmērs = kursors_VALUE; mēģināt_vēlreiz_VALUE(); continue; }
            if (byte_dati < 32 && byte_dati != 9) continue;
            if (Izmērs == 명령해석기.Līniju.length) { pārpilde = true; continue; }
            for (int Loop_INDEX = Izmērs; Loop_INDEX > kursors_VALUE; Loop_INDEX--) 명령해석기.Līniju[Loop_INDEX] = 명령해석기.Līniju[Loop_INDEX - 1];
            명령해석기.Līniju[kursors_VALUE++] = byte_dati; Izmērs++;
            if (kursors_VALUE == Izmērs && !가로보기 && 폭(0, Izmērs) <= 보이는폭()) Panelis.직렬쓰기(byte_dati);
            else if (kursors_VALUE == Izmērs) 보이는줄(); else mēģināt_vēlreiz_VALUE();
        }
    }
}
