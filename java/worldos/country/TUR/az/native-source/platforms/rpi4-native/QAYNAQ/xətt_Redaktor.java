// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 bayt_VALUE 경계를 지키는 삽입/삭제, 방향키, Əmr LOG_yaz, Tab 완성. */
public final class xətt_Redaktor {
    static boolean əmr_sətri;
    static int[] LOG_yaz = new int[16 * 1024], LOG_uzunluq = new int[16], Store_VALUE = new int[4096], 후보 = new int[64];
    static int LOG_COUNT, LOG_yaz_bitirmək, SEARCH_VALUE, 저장길이, Böyüklük, kursor_VALUE, 후보수, 후보길이, Başla_pəncərə;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd təhlükəsiz_örtük uzaq_displey run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String daxiletmə_Siyahı, int Başla_yerinə_qoymaq, int bitirmək_yerinə_qoymaq, int 입력길이) {
        int bayt_COUNT=0;
        for(int yerinə_qoymaq_INDEX=Başla_yerinə_qoymaq;yerinə_qoymaq_INDEX<bitirmək_yerinə_qoymaq;yerinə_qoymaq_INDEX++) {
            int simvol_kodu=daxiletmə_Siyahı.charAt(yerinə_qoymaq_INDEX);
            if(simvol_kodu>=0xd800 && simvol_kodu<=0xdbff && yerinə_qoymaq_INDEX+1<bitirmək_yerinə_qoymaq)simvol_kodu=0x10000+((simvol_kodu-0xd800)<<10)+daxiletmə_Siyahı.charAt(++yerinə_qoymaq_INDEX)-0xdc00;
            int 수=simvol_kodu<128?1:simvol_kodu<2048?2:simvol_kodu<65536?3:4;
            if(bayt_COUNT+수>62)return;
            for(int SEQUENCE_VALUE=수-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--)명령후보[bayt_COUNT++]=수==1?simvol_kodu:SEQUENCE_VALUE==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(simvol_kodu>>(6*SEQUENCE_VALUE)):0x80|((simvol_kodu>>(6*SEQUENCE_VALUE))&63);
        }
        if(bayt_COUNT<입력길이)return;
        for(int yerinə_qoymaq_INDEX=0;yerinə_qoymaq_INDEX<입력길이;yerinə_qoymaq_INDEX++)if(명령후보[yerinə_qoymaq_INDEX]!=명령해석기.Giriş[yerinə_qoymaq_INDEX])return;
        후보수++;후보길이=bayt_COUNT+1;
        for(int yerinə_qoymaq_INDEX=0;yerinə_qoymaq_INDEX<bayt_COUNT;yerinə_qoymaq_INDEX++)후보[yerinə_qoymaq_INDEX]=명령후보[yerinə_qoymaq_INDEX];후보[bayt_COUNT]=' ';
    }
    static int ön_VALUE(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.Giriş[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int GERİ_VALUE(int 읽는자리) { if (읽는자리 < Böyüklük) { 읽는자리++; while (읽는자리 < Böyüklük && (명령해석기.Giriş[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int Başla_yerinə_qoymaq, int təyinat_VALUE_INDEX) {
        int 글칸수 = 0;
        for (int Loop_INDEX = Başla_yerinə_qoymaq; Loop_INDEX < təyinat_VALUE_INDEX; Loop_INDEX++) { int bayt_verilənlər = 명령해석기.Giriş[Loop_INDEX]; if ((bayt_verilənlər & 192) == 128) continue; 글칸수 += bayt_verilənlər >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.Yazma("\r\u001b[2K");
        단말.Yazma(əmr_sətri ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 Giriş 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int COLUMNS = lövhə.Terminal(13) & 65535; return COLUMNS - (əmr_sətri ? 18 : 9); }
    static void 보이는줄() {
        if (kursor_VALUE < Başla_pəncərə) Başla_pəncərə = kursor_VALUE;
        while (폭(Başla_pəncərə, kursor_VALUE) > 보이는폭()) Başla_pəncərə = GERİ_VALUE(Başla_pəncərə);
        int bitirmək_yerinə_qoymaq = Başla_pəncərə;
        while (bitirmək_yerinə_qoymaq < Böyüklük && 폭(Başla_pəncərə, GERİ_VALUE(bitirmək_yerinə_qoymaq)) <= 보이는폭()) bitirmək_yerinə_qoymaq = GERİ_VALUE(bitirmək_yerinə_qoymaq);
        단말.Yazma("\r\u001b["); 단말.수(əmr_sətri ? 16 : 7); 단말.Yazma("G\u001b[K");
        if (Başla_pəncərə > 0) 단말.문자('<');
        for (int Loop_INDEX = Başla_pəncərə; Loop_INDEX < bitirmək_yerinə_qoymaq; Loop_INDEX++) lövhə.직렬쓰기(명령해석기.Giriş[Loop_INDEX]);
        단말.문자(bitirmək_yerinə_qoymaq < Böyüklük ? '>' : ' ');
        단말.Yazma("\u001b["); 단말.수(폭(kursor_VALUE, bitirmək_yerinə_qoymaq) + 1); 단말.문자('D');
        가로보기 = Başla_pəncərə > 0 || bitirmək_yerinə_qoymaq < Böyüklük || 폭(0, Böyüklük) > 보이는폭();
    }
    static void 기록넣기() {
        if (!əmr_sətri || Böyüklük == 0 || Böyüklük > 1024) return;
        if (LOG_COUNT > 0) {
            int 마지막자리 = (LOG_yaz_bitirmək + 15) % 16; boolean 같은여부 = LOG_uzunluq[마지막자리] == Böyüklük;
            for (int Loop_INDEX = 0; 같은여부 && Loop_INDEX < Böyüklük; Loop_INDEX++) if (LOG_yaz[마지막자리 * 1024 + Loop_INDEX] != 명령해석기.Giriş[Loop_INDEX]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_uzunluq[LOG_yaz_bitirmək] = Böyüklük; for (int Loop_INDEX = 0; Loop_INDEX < Böyüklük; Loop_INDEX++) LOG_yaz[LOG_yaz_bitirmək * 1024 + Loop_INDEX] = 명령해석기.Giriş[Loop_INDEX];
        LOG_yaz_bitirmək = (LOG_yaz_bitirmək + 1) % 16; if (LOG_COUNT < 16) LOG_COUNT++;
    }
    static void 기록이동(int DELTA_VALUE) {
        if (!əmr_sətri) return;
        if (SEARCH_VALUE == 0 && DELTA_VALUE > 0) { 저장길이 = Böyüklük; for (int Loop_INDEX = 0; Loop_INDEX < Böyüklük; Loop_INDEX++) Store_VALUE[Loop_INDEX] = 명령해석기.Giriş[Loop_INDEX]; }
        int Sonrakı_yerinə_qoymaq = SEARCH_VALUE + DELTA_VALUE; if (Sonrakı_yerinə_qoymaq < 0 || Sonrakı_yerinə_qoymaq > LOG_COUNT) return; SEARCH_VALUE = Sonrakı_yerinə_qoymaq;
        if (SEARCH_VALUE == 0) { Böyüklük = 저장길이; for (int Loop_INDEX = 0; Loop_INDEX < Böyüklük; Loop_INDEX++) 명령해석기.Giriş[Loop_INDEX] = Store_VALUE[Loop_INDEX]; }
        else { int 보관칸 = (LOG_yaz_bitirmək + 16 - SEARCH_VALUE) % 16; Böyüklük = LOG_uzunluq[보관칸]; for (int Loop_INDEX = 0; Loop_INDEX < Böyüklük; Loop_INDEX++) 명령해석기.Giriş[Loop_INDEX] = LOG_yaz[보관칸 * 1024 + Loop_INDEX]; }
        kursor_VALUE = Böyüklük; 다시();
    }
    static void göstərmək_LOG() {
        for (int daxiletmə_COUNT = 0; daxiletmə_COUNT < LOG_COUNT; daxiletmə_COUNT++) {
            int 보관칸 = (LOG_yaz_bitirmək + 16 - LOG_COUNT + daxiletmə_COUNT) % 16; 단말.수(daxiletmə_COUNT + 1); 단말.Yazma("  ");
            for (int Loop_INDEX = 0; Loop_INDEX < LOG_uzunluq[보관칸]; Loop_INDEX++) lövhə.직렬쓰기(LOG_yaz[보관칸 * 1024 + Loop_INDEX]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] verilənlər_ARRAY, int Başla_yerinə_qoymaq, int daxiletmə_COUNT, int 접두말, int 총수, boolean 폴더번호) {
        if (daxiletmə_COUNT < 총수 || daxiletmə_COUNT > 62) return;
        for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) if (verilənlər_ARRAY[Başla_yerinə_qoymaq + Loop_INDEX] != 명령해석기.Giriş[접두말 + Loop_INDEX]) return;
        후보수++; 후보길이 = daxiletmə_COUNT + 1;
        for (int Loop_INDEX = 0; Loop_INDEX < daxiletmə_COUNT; Loop_INDEX++) 후보[Loop_INDEX] = verilənlər_ARRAY[Başla_yerinə_qoymaq + Loop_INDEX]; 후보[daxiletmə_COUNT] = 폴더번호 ? '/' : ' ';
    }
    static void 완성() {
        if (!əmr_sətri || kursor_VALUE != Böyüklük) return;
        int 시작점 = Böyüklük; while (시작점 > 0 && 명령해석기.Giriş[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDEX = 시작점; Loop_INDEX < Böyüklük; Loop_INDEX++) if (명령해석기.Giriş[Loop_INDEX] == '/' || 명령해석기.Giriş[Loop_INDEX] == '"' || 명령해석기.Giriş[Loop_INDEX] == 39 || 명령해석기.Giriş[Loop_INDEX] == '\\') return;
        후보수 = 0; int daxiletmə_COUNT = Böyüklük - 시작점;
        if (시작점 == 0) {
            for(int Siyahı_INDEX=0;Siyahı_INDEX<2;Siyahı_INDEX++) {
                String daxiletmə_Siyahı=Siyahı_INDEX==0?명령들:관리명령.완성어();
                int 읽는자리=0;
                while(읽는자리<daxiletmə_Siyahı.length()) {
                    int bitirmək_yerinə_qoymaq=읽는자리;while(bitirmək_yerinə_qoymaq<daxiletmə_Siyahı.length() && daxiletmə_Siyahı.charAt(bitirmək_yerinə_qoymaq)!=' ')bitirmək_yerinə_qoymaq++;
                    명령후보넣기(daxiletmə_Siyahı,읽는자리,bitirmək_yerinə_qoymaq,daxiletmə_COUNT);읽는자리=bitirmək_yerinə_qoymaq+1;
                }
            }
        } else {
            Yaddaş_Fayllar.yol_Başla(1); Yaddaş_Fayllar.yol_bayt(0, '.'); Yaddaş_Fayllar.normallaşdırmaq_VALUE();
            for (int Loop_INDEX = 0; Loop_INDEX < Yaddaş_Fayllar.fayl_COUNT; Loop_INDEX++) {
                int Başla_yerinə_qoymaq = Yaddaş_Fayllar.daxiletmə_Başla(Yaddaş_Fayllar.Ad, Loop_INDEX * 64, Yaddaş_Fayllar.이름길이[Loop_INDEX]);
                if (Başla_yerinə_qoymaq >= 0) 후보넣기(Yaddaş_Fayllar.Ad, Loop_INDEX * 64 + Başla_yerinə_qoymaq, Yaddaş_Fayllar.이름길이[Loop_INDEX] - Başla_yerinə_qoymaq, 시작점, daxiletmə_COUNT, false);
            }
            for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
                int Başla_yerinə_qoymaq = Yaddaş_Fayllar.daxiletmə_Başla(Yaddaş_Fayllar.kataloq_ad, Loop_INDEX * 64, Yaddaş_Fayllar.kataloq_uzunluq[Loop_INDEX]);
                if (Başla_yerinə_qoymaq >= 0) 후보넣기(Yaddaş_Fayllar.kataloq_ad, Loop_INDEX * 64 + Başla_yerinə_qoymaq, Yaddaş_Fayllar.kataloq_uzunluq[Loop_INDEX] - Başla_yerinə_qoymaq, 시작점, daxiletmə_COUNT, true);
            }
        }
        if (후보수 != 1) { lövhə.직렬쓰기(7); return; }
        for (int Loop_INDEX = daxiletmə_COUNT; Loop_INDEX < 후보길이 && Böyüklük < 명령해석기.Giriş.length - 1; Loop_INDEX++) {
            if (후보[Loop_INDEX] == ' ' && Loop_INDEX != 후보길이 - 1) 명령해석기.Giriş[Böyüklük++] = '\\';
            명령해석기.Giriş[Böyüklük++] = 후보[Loop_INDEX];
        }
        kursor_VALUE = Böyüklük; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = lövhə.밀리초();
        while (lövhə.밀리초() - 시작점 < 80) { int bayt_verilənlər = lövhə.직렬읽기(); if (bayt_verilənlər >= 0) return bayt_verilənlər; lövhə.YIELD_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int daxiletmə_COUNT = 0, bitirmək_yerinə_qoymaq = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 12; Loop_INDEX++) { int bayt_verilənlər = 탈출읽기(); if (bayt_verilənlər < 0) return; if (bayt_verilənlər >= '0' && bayt_verilənlər <= '9') daxiletmə_COUNT = daxiletmə_COUNT * 10 + bayt_verilənlər - '0'; else { bitirmək_yerinə_qoymaq = bayt_verilənlər; break; } }
        if (bitirmək_yerinə_qoymaq == 'A') 기록이동(1);
        else if (bitirmək_yerinə_qoymaq == 'B') 기록이동(-1);
        else if (bitirmək_yerinə_qoymaq == 'C') { kursor_VALUE = GERİ_VALUE(kursor_VALUE); 다시(); }
        else if (bitirmək_yerinə_qoymaq == 'D') { kursor_VALUE = ön_VALUE(kursor_VALUE); 다시(); }
        else if (bitirmək_yerinə_qoymaq == 'H' || bitirmək_yerinə_qoymaq == '~' && (daxiletmə_COUNT == 1 || daxiletmə_COUNT == 7)) { kursor_VALUE = 0; 다시(); }
        else if (bitirmək_yerinə_qoymaq == 'F' || bitirmək_yerinə_qoymaq == '~' && (daxiletmə_COUNT == 4 || daxiletmə_COUNT == 8)) { kursor_VALUE = Böyüklük; 다시(); }
        else if (bitirmək_yerinə_qoymaq == '~' && daxiletmə_COUNT == 3 && kursor_VALUE < Böyüklük) {
            int Sonrakı_yerinə_qoymaq = GERİ_VALUE(kursor_VALUE); for (int Loop_INDEX = Sonrakı_yerinə_qoymaq; Loop_INDEX < Böyüklük; Loop_INDEX++) 명령해석기.Giriş[Loop_INDEX - Sonrakı_yerinə_qoymaq + kursor_VALUE] = 명령해석기.Giriş[Loop_INDEX]; Böyüklük -= Sonrakı_yerinə_qoymaq - kursor_VALUE; 다시();
        }
        else if (bitirmək_yerinə_qoymaq == '~' && (daxiletmə_COUNT == 5 || daxiletmə_COUNT == 6)) lövhə.Terminal(daxiletmə_COUNT == 5 ? 5 : 6);
        else if (bitirmək_yerinə_qoymaq == '~' && daxiletmə_COUNT == 24 && əmr_sətri) { 명령해석기.Terminal(true); }
    }
    static int Oxuma() {
        if (!pəncərə_seans.이어읽기) { Böyüklük = kursor_VALUE = SEARCH_VALUE = Başla_pəncərə = 0; 가로보기 = false; }
        else { pəncərə_seans.이어읽기 = false; 다시(); } boolean dolub_daşma = false;
        while (true) {
            int bayt_verilənlər = lövhə.직렬읽기(); if (bayt_verilənlər == -4096) return -3;
            if (lövhə.Terminal(14) != 0) 다시(); if (bayt_verilənlər < 0) { lövhə.YIELD_CPU(); continue; }
            if (bayt_verilənlər == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = bayt_verilənlər == 13;
            if (bayt_verilənlər == 27) { 탈출(); continue; }
            if (bayt_verilənlər == 3) { 단말.Yazma("^C\n"); return -1; }
            if (bayt_verilənlər == 4 && Böyüklük == 0 && əmr_sətri) { if (lövhə.Terminal(2) != 0) 명령해석기.Terminal(true); return -1; }
            if (bayt_verilənlər == 13 || bayt_verilənlər == 10) { 단말.문자(10); if (!dolub_daşma) 기록넣기(); return dolub_daşma ? -2 : Böyüklük; }
            if (bayt_verilənlər == 9 && əmr_sətri) { 완성(); continue; }
            if (bayt_verilənlər == 1 || bayt_verilənlər == 5) { kursor_VALUE = bayt_verilənlər == 1 ? 0 : Böyüklük; 다시(); continue; }
            if (bayt_verilənlər == 8 || bayt_verilənlər == 127 || bayt_verilənlər == 21) {
                if (bayt_verilənlər == 21) { for (int Loop_INDEX = kursor_VALUE; Loop_INDEX < Böyüklük; Loop_INDEX++) 명령해석기.Giriş[Loop_INDEX - kursor_VALUE] = 명령해석기.Giriş[Loop_INDEX]; Böyüklük -= kursor_VALUE; kursor_VALUE = 0; }
                else if (kursor_VALUE > 0) { int 변경전 = ön_VALUE(kursor_VALUE); for (int Loop_INDEX = kursor_VALUE; Loop_INDEX < Böyüklük; Loop_INDEX++) 명령해석기.Giriş[Loop_INDEX - kursor_VALUE + 변경전] = 명령해석기.Giriş[Loop_INDEX]; Böyüklük -= kursor_VALUE - 변경전; kursor_VALUE = 변경전; }
                다시(); continue;
            }
            if (bayt_verilənlər == 11) { Böyüklük = kursor_VALUE; 다시(); continue; }
            if (bayt_verilənlər < 32 && bayt_verilənlər != 9) continue;
            if (Böyüklük == 명령해석기.Giriş.length) { dolub_daşma = true; continue; }
            for (int Loop_INDEX = Böyüklük; Loop_INDEX > kursor_VALUE; Loop_INDEX--) 명령해석기.Giriş[Loop_INDEX] = 명령해석기.Giriş[Loop_INDEX - 1];
            명령해석기.Giriş[kursor_VALUE++] = bayt_verilənlər; Böyüklük++;
            if (kursor_VALUE == Böyüklük && !가로보기 && 폭(0, Böyüklük) <= 보이는폭()) lövhə.직렬쓰기(bayt_verilənlər);
            else if (kursor_VALUE == Böyüklük) 보이는줄(); else 다시();
        }
    }
}
