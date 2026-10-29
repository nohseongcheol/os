// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 bayt_değer 경계를 지키는 삽입/삭제, 방향키, komut LOG_KAYIT, Tab Bitenler_değer. */
public final class satır_düzenleyicisi {
    static boolean komut_satırı;
    static int[] LOG_KAYIT = new int[16 * 1024], LOG_süre = new int[16], depo_değer = new int[4096], aday = new int[64];
    static int LOG_BAĞ_DEĞ_SAY, LOG_KAYIT_Bitiş, Ara_değer, 저장길이, Boyut, imleç_değer, aday_BAĞ_DEĞ_SAY, aday_süre, Start_pencere;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd SSH uzak_monitör run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] komut_aday = new int[128];
    static void Ekle_komut_aday(String girdi_Liste, int Start_konum, int Bitiş_konum, int artış_süre) {
        int bayt_BAĞ_DEĞ_SAY=0;
        for(int konum_dizini=Start_konum;konum_dizini<Bitiş_konum;konum_dizini++) {
            int kod_noktası=girdi_Liste.charAt(konum_dizini);
            if(kod_noktası>=0xd800 && kod_noktası<=0xdbff && konum_dizini+1<Bitiş_konum)kod_noktası=0x10000+((kod_noktası-0xd800)<<10)+girdi_Liste.charAt(++konum_dizini)-0xdc00;
            int 수=kod_noktası<128?1:kod_noktası<2048?2:kod_noktası<65536?3:4;
            if(bayt_BAĞ_DEĞ_SAY+수>62)return;
            for(int dizi_değer=수-1;dizi_değer>=0;dizi_değer--)komut_aday[bayt_BAĞ_DEĞ_SAY++]=수==1?kod_noktası:dizi_değer==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(kod_noktası>>(6*dizi_değer)):0x80|((kod_noktası>>(6*dizi_değer))&63);
        }
        if(bayt_BAĞ_DEĞ_SAY<artış_süre)return;
        for(int konum_dizini=0;konum_dizini<artış_süre;konum_dizini++)if(komut_aday[konum_dizini]!=KomutYorumlayıcı.girdi_satırı[konum_dizini])return;
        aday_BAĞ_DEĞ_SAY++;aday_süre=bayt_BAĞ_DEĞ_SAY+1;
        for(int konum_dizini=0;konum_dizini<bayt_BAĞ_DEĞ_SAY;konum_dizini++)aday[konum_dizini]=komut_aday[konum_dizini];aday[bayt_BAĞ_DEĞ_SAY]=' ';
    }
    static int ön_kamera_değer(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (KomutYorumlayıcı.girdi_satırı[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int BACK_değer(int 읽는자리) { if (읽는자리 < Boyut) { 읽는자리++; while (읽는자리 < Boyut && (KomutYorumlayıcı.girdi_satırı[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int Start_konum, int hedef_değer_Dizin) {
        int 글칸수 = 0;
        for (int Loop_Dizin = Start_konum; Loop_Dizin < hedef_değer_Dizin; Loop_Dizin++) { int bayt_veri = KomutYorumlayıcı.girdi_satırı[Loop_Dizin]; if ((bayt_veri & 192) == 128) continue; 글칸수 += bayt_veri >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void yeniden_denemek_değer() {
        단말.Yazma("\r\u001b[2K");
        단말.Yazma(komut_satırı ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 girdi_satırı 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int SÜTUNSAY = Pano.uçbirim(13) & 65535; return SÜTUNSAY - (komut_satırı ? 18 : 9); }
    static void 보이는줄() {
        if (imleç_değer < Start_pencere) Start_pencere = imleç_değer;
        while (폭(Start_pencere, imleç_değer) > 보이는폭()) Start_pencere = BACK_değer(Start_pencere);
        int Bitiş_konum = Start_pencere;
        while (Bitiş_konum < Boyut && 폭(Start_pencere, BACK_değer(Bitiş_konum)) <= 보이는폭()) Bitiş_konum = BACK_değer(Bitiş_konum);
        단말.Yazma("\r\u001b["); 단말.수(komut_satırı ? 16 : 7); 단말.Yazma("G\u001b[K");
        if (Start_pencere > 0) 단말.문자('<');
        for (int Loop_Dizin = Start_pencere; Loop_Dizin < Bitiş_konum; Loop_Dizin++) Pano.직렬쓰기(KomutYorumlayıcı.girdi_satırı[Loop_Dizin]);
        단말.문자(Bitiş_konum < Boyut ? '>' : ' ');
        단말.Yazma("\u001b["); 단말.수(폭(imleç_değer, Bitiş_konum) + 1); 단말.문자('D');
        가로보기 = Start_pencere > 0 || Bitiş_konum < Boyut || 폭(0, Boyut) > 보이는폭();
    }
    static void Ekleme_LOG() {
        if (!komut_satırı || Boyut == 0 || Boyut > 1024) return;
        if (LOG_BAĞ_DEĞ_SAY > 0) {
            int 마지막자리 = (LOG_KAYIT_Bitiş + 15) % 16; boolean 같은여부 = LOG_süre[마지막자리] == Boyut;
            for (int Loop_Dizin = 0; 같은여부 && Loop_Dizin < Boyut; Loop_Dizin++) if (LOG_KAYIT[마지막자리 * 1024 + Loop_Dizin] != KomutYorumlayıcı.girdi_satırı[Loop_Dizin]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_süre[LOG_KAYIT_Bitiş] = Boyut; for (int Loop_Dizin = 0; Loop_Dizin < Boyut; Loop_Dizin++) LOG_KAYIT[LOG_KAYIT_Bitiş * 1024 + Loop_Dizin] = KomutYorumlayıcı.girdi_satırı[Loop_Dizin];
        LOG_KAYIT_Bitiş = (LOG_KAYIT_Bitiş + 1) % 16; if (LOG_BAĞ_DEĞ_SAY < 16) LOG_BAĞ_DEĞ_SAY++;
    }
    static void 기록이동(int DELTA_değer) {
        if (!komut_satırı) return;
        if (Ara_değer == 0 && DELTA_değer > 0) { 저장길이 = Boyut; for (int Loop_Dizin = 0; Loop_Dizin < Boyut; Loop_Dizin++) depo_değer[Loop_Dizin] = KomutYorumlayıcı.girdi_satırı[Loop_Dizin]; }
        int Sonraki_konum = Ara_değer + DELTA_değer; if (Sonraki_konum < 0 || Sonraki_konum > LOG_BAĞ_DEĞ_SAY) return; Ara_değer = Sonraki_konum;
        if (Ara_değer == 0) { Boyut = 저장길이; for (int Loop_Dizin = 0; Loop_Dizin < Boyut; Loop_Dizin++) KomutYorumlayıcı.girdi_satırı[Loop_Dizin] = depo_değer[Loop_Dizin]; }
        else { int 보관칸 = (LOG_KAYIT_Bitiş + 16 - Ara_değer) % 16; Boyut = LOG_süre[보관칸]; for (int Loop_Dizin = 0; Loop_Dizin < Boyut; Loop_Dizin++) KomutYorumlayıcı.girdi_satırı[Loop_Dizin] = LOG_KAYIT[보관칸 * 1024 + Loop_Dizin]; }
        imleç_değer = Boyut; yeniden_denemek_değer();
    }
    static void şov_LOG() {
        for (int girdi_BAĞ_DEĞ_SAY = 0; girdi_BAĞ_DEĞ_SAY < LOG_BAĞ_DEĞ_SAY; girdi_BAĞ_DEĞ_SAY++) {
            int 보관칸 = (LOG_KAYIT_Bitiş + 16 - LOG_BAĞ_DEĞ_SAY + girdi_BAĞ_DEĞ_SAY) % 16; 단말.수(girdi_BAĞ_DEĞ_SAY + 1); 단말.Yazma("  ");
            for (int Loop_Dizin = 0; Loop_Dizin < LOG_süre[보관칸]; Loop_Dizin++) Pano.직렬쓰기(LOG_KAYIT[보관칸 * 1024 + Loop_Dizin]); 단말.문자(10);
        }
    }
    static void Ekle_aday(int[] veri_DİZİ, int Start_konum, int girdi_BAĞ_DEĞ_SAY, int 접두말, int toplam_BAĞ_DEĞ_SAY, boolean 폴더번호) {
        if (girdi_BAĞ_DEĞ_SAY < toplam_BAĞ_DEĞ_SAY || girdi_BAĞ_DEĞ_SAY > 62) return;
        for (int Loop_Dizin = 0; Loop_Dizin < toplam_BAĞ_DEĞ_SAY; Loop_Dizin++) if (veri_DİZİ[Start_konum + Loop_Dizin] != KomutYorumlayıcı.girdi_satırı[접두말 + Loop_Dizin]) return;
        aday_BAĞ_DEĞ_SAY++; aday_süre = girdi_BAĞ_DEĞ_SAY + 1;
        for (int Loop_Dizin = 0; Loop_Dizin < girdi_BAĞ_DEĞ_SAY; Loop_Dizin++) aday[Loop_Dizin] = veri_DİZİ[Start_konum + Loop_Dizin]; aday[girdi_BAĞ_DEĞ_SAY] = 폴더번호 ? '/' : ' ';
    }
    static void Bitenler_değer() {
        if (!komut_satırı || imleç_değer != Boyut) return;
        int 시작점 = Boyut; while (시작점 > 0 && KomutYorumlayıcı.girdi_satırı[시작점 - 1] != ' ') 시작점--;
        for (int Loop_Dizin = 시작점; Loop_Dizin < Boyut; Loop_Dizin++) if (KomutYorumlayıcı.girdi_satırı[Loop_Dizin] == '/' || KomutYorumlayıcı.girdi_satırı[Loop_Dizin] == '"' || KomutYorumlayıcı.girdi_satırı[Loop_Dizin] == 39 || KomutYorumlayıcı.girdi_satırı[Loop_Dizin] == '\\') return;
        aday_BAĞ_DEĞ_SAY = 0; int girdi_BAĞ_DEĞ_SAY = Boyut - 시작점;
        if (시작점 == 0) {
            for(int liste_dizini=0;liste_dizini<2;liste_dizini++) {
                String girdi_Liste=liste_dizini==0?명령들:관리명령.Bitenler_Word();
                int 읽는자리=0;
                while(읽는자리<girdi_Liste.length()) {
                    int Bitiş_konum=읽는자리;while(Bitiş_konum<girdi_Liste.length() && girdi_Liste.charAt(Bitiş_konum)!=' ')Bitiş_konum++;
                    Ekle_komut_aday(girdi_Liste,읽는자리,Bitiş_konum,girdi_BAĞ_DEĞ_SAY);읽는자리=Bitiş_konum+1;
                }
            }
        } else {
            BellekDosyaları.yol_Start(1); BellekDosyaları.yol_bayt(0, '.'); BellekDosyaları.normalleştirmek_değer();
            for (int Loop_Dizin = 0; Loop_Dizin < BellekDosyaları.Dosya_BAĞ_DEĞ_SAY; Loop_Dizin++) {
                int Start_konum = BellekDosyaları.girdi_Start(BellekDosyaları.İsim, Loop_Dizin * 64, BellekDosyaları.이름길이[Loop_Dizin]);
                if (Start_konum >= 0) Ekle_aday(BellekDosyaları.İsim, Loop_Dizin * 64 + Start_konum, BellekDosyaları.이름길이[Loop_Dizin] - Start_konum, 시작점, girdi_BAĞ_DEĞ_SAY, false);
            }
            for (int Loop_Dizin = 0; Loop_Dizin < 16; Loop_Dizin++) {
                int Start_konum = BellekDosyaları.girdi_Start(BellekDosyaları.dizin_ad, Loop_Dizin * 64, BellekDosyaları.dizin_süre[Loop_Dizin]);
                if (Start_konum >= 0) Ekle_aday(BellekDosyaları.dizin_ad, Loop_Dizin * 64 + Start_konum, BellekDosyaları.dizin_süre[Loop_Dizin] - Start_konum, 시작점, girdi_BAĞ_DEĞ_SAY, true);
            }
        }
        if (aday_BAĞ_DEĞ_SAY != 1) { Pano.직렬쓰기(7); return; }
        for (int Loop_Dizin = girdi_BAĞ_DEĞ_SAY; Loop_Dizin < aday_süre && Boyut < KomutYorumlayıcı.girdi_satırı.length - 1; Loop_Dizin++) {
            if (aday[Loop_Dizin] == ' ' && Loop_Dizin != aday_süre - 1) KomutYorumlayıcı.girdi_satırı[Boyut++] = '\\';
            KomutYorumlayıcı.girdi_satırı[Boyut++] = aday[Loop_Dizin];
        }
        imleç_değer = Boyut; yeniden_denemek_değer();
    }
    static int 탈출읽기() {
        int 시작점 = Pano.밀리초();
        while (Pano.밀리초() - 시작점 < 80) { int bayt_veri = Pano.직렬읽기(); if (bayt_veri >= 0) return bayt_veri; Pano.ÖDEME_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int girdi_BAĞ_DEĞ_SAY = 0, Bitiş_konum = -1;
        for (int Loop_Dizin = 0; Loop_Dizin < 12; Loop_Dizin++) { int bayt_veri = 탈출읽기(); if (bayt_veri < 0) return; if (bayt_veri >= '0' && bayt_veri <= '9') girdi_BAĞ_DEĞ_SAY = girdi_BAĞ_DEĞ_SAY * 10 + bayt_veri - '0'; else { Bitiş_konum = bayt_veri; break; } }
        if (Bitiş_konum == 'A') 기록이동(1);
        else if (Bitiş_konum == 'B') 기록이동(-1);
        else if (Bitiş_konum == 'C') { imleç_değer = BACK_değer(imleç_değer); yeniden_denemek_değer(); }
        else if (Bitiş_konum == 'D') { imleç_değer = ön_kamera_değer(imleç_değer); yeniden_denemek_değer(); }
        else if (Bitiş_konum == 'H' || Bitiş_konum == '~' && (girdi_BAĞ_DEĞ_SAY == 1 || girdi_BAĞ_DEĞ_SAY == 7)) { imleç_değer = 0; yeniden_denemek_değer(); }
        else if (Bitiş_konum == 'F' || Bitiş_konum == '~' && (girdi_BAĞ_DEĞ_SAY == 4 || girdi_BAĞ_DEĞ_SAY == 8)) { imleç_değer = Boyut; yeniden_denemek_değer(); }
        else if (Bitiş_konum == '~' && girdi_BAĞ_DEĞ_SAY == 3 && imleç_değer < Boyut) {
            int Sonraki_konum = BACK_değer(imleç_değer); for (int Loop_Dizin = Sonraki_konum; Loop_Dizin < Boyut; Loop_Dizin++) KomutYorumlayıcı.girdi_satırı[Loop_Dizin - Sonraki_konum + imleç_değer] = KomutYorumlayıcı.girdi_satırı[Loop_Dizin]; Boyut -= Sonraki_konum - imleç_değer; yeniden_denemek_değer();
        }
        else if (Bitiş_konum == '~' && (girdi_BAĞ_DEĞ_SAY == 5 || girdi_BAĞ_DEĞ_SAY == 6)) Pano.uçbirim(girdi_BAĞ_DEĞ_SAY == 5 ? 5 : 6);
        else if (Bitiş_konum == '~' && girdi_BAĞ_DEĞ_SAY == 24 && komut_satırı) { KomutYorumlayıcı.uçbirim(true); }
    }
    static int Okuma() {
        if (!pencere_oturum.이어읽기) { Boyut = imleç_değer = Ara_değer = Start_pencere = 0; 가로보기 = false; }
        else { pencere_oturum.이어읽기 = false; yeniden_denemek_değer(); } boolean Taşma = false;
        while (true) {
            int bayt_veri = Pano.직렬읽기(); if (bayt_veri == -4096) return -3;
            if (Pano.uçbirim(14) != 0) yeniden_denemek_değer(); if (bayt_veri < 0) { Pano.ÖDEME_CPU(); continue; }
            if (bayt_veri == 10 && KomutYorumlayıcı.Önceki_hat) { KomutYorumlayıcı.Önceki_hat = false; continue; } KomutYorumlayıcı.Önceki_hat = bayt_veri == 13;
            if (bayt_veri == 27) { 탈출(); continue; }
            if (bayt_veri == 3) { 단말.Yazma("^C\n"); return -1; }
            if (bayt_veri == 4 && Boyut == 0 && komut_satırı) { if (Pano.uçbirim(2) != 0) KomutYorumlayıcı.uçbirim(true); return -1; }
            if (bayt_veri == 13 || bayt_veri == 10) { 단말.문자(10); if (!Taşma) Ekleme_LOG(); return Taşma ? -2 : Boyut; }
            if (bayt_veri == 9 && komut_satırı) { Bitenler_değer(); continue; }
            if (bayt_veri == 1 || bayt_veri == 5) { imleç_değer = bayt_veri == 1 ? 0 : Boyut; yeniden_denemek_değer(); continue; }
            if (bayt_veri == 8 || bayt_veri == 127 || bayt_veri == 21) {
                if (bayt_veri == 21) { for (int Loop_Dizin = imleç_değer; Loop_Dizin < Boyut; Loop_Dizin++) KomutYorumlayıcı.girdi_satırı[Loop_Dizin - imleç_değer] = KomutYorumlayıcı.girdi_satırı[Loop_Dizin]; Boyut -= imleç_değer; imleç_değer = 0; }
                else if (imleç_değer > 0) { int 변경전 = ön_kamera_değer(imleç_değer); for (int Loop_Dizin = imleç_değer; Loop_Dizin < Boyut; Loop_Dizin++) KomutYorumlayıcı.girdi_satırı[Loop_Dizin - imleç_değer + 변경전] = KomutYorumlayıcı.girdi_satırı[Loop_Dizin]; Boyut -= imleç_değer - 변경전; imleç_değer = 변경전; }
                yeniden_denemek_değer(); continue;
            }
            if (bayt_veri == 11) { Boyut = imleç_değer; yeniden_denemek_değer(); continue; }
            if (bayt_veri < 32 && bayt_veri != 9) continue;
            if (Boyut == KomutYorumlayıcı.girdi_satırı.length) { Taşma = true; continue; }
            for (int Loop_Dizin = Boyut; Loop_Dizin > imleç_değer; Loop_Dizin--) KomutYorumlayıcı.girdi_satırı[Loop_Dizin] = KomutYorumlayıcı.girdi_satırı[Loop_Dizin - 1];
            KomutYorumlayıcı.girdi_satırı[imleç_değer++] = bayt_veri; Boyut++;
            if (imleç_değer == Boyut && !가로보기 && 폭(0, Boyut) <= 보이는폭()) Pano.직렬쓰기(bayt_veri);
            else if (imleç_değer == Boyut) 보이는줄(); else yeniden_denemek_değer();
        }
    }
}
