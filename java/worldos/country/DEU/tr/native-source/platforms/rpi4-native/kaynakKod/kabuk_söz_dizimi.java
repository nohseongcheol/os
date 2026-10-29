// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 devralmak kabuk 문법. 파이프는 순차 yürütmek_komut, 환경은 같은 셸에서 공유한다. */
public final class kabuk_söz_dizimi {
    static int[] kaynakKod = new int[4 * 4096], Tip_değer = new int[4 * 128], çalıştır = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] değişken_ad = new int[16 * 32], değişken_veri = new int[16 * 256], 이름길이 = new int[16], değer_süre = new int[16];
    static int[] betik_değer = new int[4 * 16384];
    static int Durum_değer, 깊이, 쓴수;
    static boolean 연결중, betik_Bitiş, uzantı_hata;
    static boolean ad_karakter(int kod_noktası) { return kod_noktası >= 'a' && kod_noktası <= 'z' || kod_noktası >= 'A' && kod_noktası <= 'Z' || kod_noktası == '_' || kod_noktası >= 128; }
    static boolean 이름뒤(int kod_noktası) { return ad_karakter(kod_noktası) || kod_noktası >= '0' && kod_noktası <= '9'; }
    static void hata(String metin) { Pano.입출력전환(0); 단말.Yazma("komut ayrıştırmak_değer: "); 단말.Yazma(metin); 단말.문자(10); Durum_değer = 2; }
    static int Okuma(int girdi_BAĞ_DEĞ_SAY, int 중첩깊이) {
        int geçerli_Dizin = 0, toplam_BAĞ_DEĞ_SAY = 0, TABAN_konum = 중첩깊이 * 4096, özel_karakter = 중첩깊이 * 128;
        while (geçerli_Dizin < girdi_BAĞ_DEĞ_SAY) {
            while (geçerli_Dizin < girdi_BAĞ_DEĞ_SAY && (kaynakKod[TABAN_konum + geçerli_Dizin] == 32 || kaynakKod[TABAN_konum + geçerli_Dizin] == 9)) geçerli_Dizin++;
            if (geçerli_Dizin == girdi_BAĞ_DEĞ_SAY || kaynakKod[TABAN_konum + geçerli_Dizin] == '#') break;
            if (toplam_BAĞ_DEĞ_SAY == 128) { hata("낱말이 너무 많습니다"); return -1; }
            int Start_konum = geçerli_Dizin, kod_noktası = kaynakKod[TABAN_konum + geçerli_Dizin], veri_Tip = 0;
            if (kod_noktası == ';') { veri_Tip = 1; geçerli_Dizin++; }
            else if (kod_noktası == '&') { if (geçerli_Dizin + 1 >= girdi_BAĞ_DEĞ_SAY || kaynakKod[TABAN_konum + geçerli_Dizin + 1] != '&') { hata("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } veri_Tip = 2; geçerli_Dizin += 2; }
            else if (kod_noktası == '|') { geçerli_Dizin++; veri_Tip = geçerli_Dizin < girdi_BAĞ_DEĞ_SAY && kaynakKod[TABAN_konum + geçerli_Dizin] == '|' ? 3 : 4; if (veri_Tip == 3) geçerli_Dizin++; }
            else if (kod_noktası == '>') { geçerli_Dizin++; veri_Tip = geçerli_Dizin < girdi_BAĞ_DEĞ_SAY && kaynakKod[TABAN_konum + geçerli_Dizin] == '>' ? 6 : 5; if (veri_Tip == 6) geçerli_Dizin++; }
            else if (kod_noktası == '<') { veri_Tip = 7; geçerli_Dizin++; }
            else {
                int Alıntı = 0;
                while (geçerli_Dizin < girdi_BAĞ_DEĞ_SAY) {
                    kod_noktası = kaynakKod[TABAN_konum + geçerli_Dizin];
                    if (kod_noktası == '`' && Alıntı != 39 || kod_noktası == '$' && Alıntı != 39 && geçerli_Dizin + 1 < girdi_BAĞ_DEĞ_SAY && kaynakKod[TABAN_konum + geçerli_Dizin + 1] == '(') { hata("komut sonuç 치환은 지원하지 않습니다"); return -1; }
                    if (kod_noktası == '\\' && Alıntı != 39) { if (++geçerli_Dizin == girdi_BAĞ_DEĞ_SAY) { hata("girdi_satırı 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } geçerli_Dizin++; continue; }
                    if (kod_noktası == Alıntı) { Alıntı = 0; geçerli_Dizin++; continue; }
                    if (Alıntı == 0 && (kod_noktası == 39 || kod_noktası == 34)) { Alıntı = kod_noktası; geçerli_Dizin++; continue; }
                    if (Alıntı == 0 && (kod_noktası == 32 || kod_noktası == 9 || kod_noktası == ';' || kod_noktası == '&' || kod_noktası == '|' || kod_noktası == '<' || kod_noktası == '>')) break;
                    geçerli_Dizin++;
                }
                if (Alıntı != 0) { hata("따옴표가 닫히지 않았습니다"); return -1; }
                if (geçerli_Dizin < girdi_BAĞ_DEĞ_SAY && (kaynakKod[TABAN_konum + geçerli_Dizin] == '>' || kaynakKod[TABAN_konum + geçerli_Dizin] == '<')) {
                    boolean 수치 = geçerli_Dizin > Start_konum;
                    for (int Loop_Dizin = Start_konum; Loop_Dizin < geçerli_Dizin; Loop_Dizin++) if (kaynakKod[TABAN_konum + Loop_Dizin] < '0' || kaynakKod[TABAN_konum + Loop_Dizin] > '9') 수치 = false;
                    if (수치) { hata("번호를 지정한 dosya tanımlayıcı_girdi G_Ç 전환은 지원하지 않습니다"); return -1; }
                }
            }
            Tip_değer[özel_karakter + toplam_BAĞ_DEĞ_SAY] = veri_Tip; çalıştır[özel_karakter + toplam_BAĞ_DEĞ_SAY] = Start_konum; 끝[özel_karakter + toplam_BAĞ_DEĞ_SAY] = geçerli_Dizin; toplam_BAĞ_DEĞ_SAY++;
        }
        boolean 낱말 = false;
        for (int Loop_Dizin = 0; Loop_Dizin < toplam_BAĞ_DEĞ_SAY; Loop_Dizin++) {
            int 임시값 = Tip_değer[özel_karakter + Loop_Dizin];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_Dizin == toplam_BAĞ_DEĞ_SAY || Tip_değer[özel_karakter + Loop_Dizin] != 0) { hata("G_Ç 전환에 dosya 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_Dizin == toplam_BAĞ_DEĞ_SAY - 1 && 임시값 != 1) { hata("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (toplam_BAĞ_DEĞ_SAY > 0 && !낱말 && Tip_değer[özel_karakter + toplam_BAĞ_DEĞ_SAY - 1] != 1) { hata("명령이 빠졌습니다"); return -1; }
        return toplam_BAĞ_DEĞ_SAY;
    }
    static boolean aralık_SMS(int[] veri_DİZİ, int yerel_Start, int girdi_BAĞ_DEĞ_SAY, String karakter_konum) {
        if (girdi_BAĞ_DEĞ_SAY != karakter_konum.length()) return false; for (int Loop_Dizin = 0; Loop_Dizin < girdi_BAĞ_DEĞ_SAY; Loop_Dizin++) if (veri_DİZİ[yerel_Start + Loop_Dizin] != karakter_konum.charAt(Loop_Dizin)) return false; return true;
    }
    static void 넣기(int bayt_veri) {
        if (쓴수 >= KomutYorumlayıcı.belirteç_değer.length) { if (!uzantı_hata) hata("변수를 펼친 명령이 너무 깁니다"); uzantı_hata = true; return; }
        KomutYorumlayıcı.belirteç_değer[쓴수++] = bayt_veri;
    }
    static void değişken_değer(int[] veri_DİZİ, int Start_konum, int girdi_BAĞ_DEĞ_SAY) {
        if (aralık_SMS(veri_DİZİ, Start_konum, girdi_BAĞ_DEĞ_SAY, "PWD")) { 넣기('/'); for (int Loop_Dizin = 0; Loop_Dizin < BellekDosyaları.geçerli_süre_6ac7278b; Loop_Dizin++) 넣기(BellekDosyaları.geçerli_öğe[Loop_Dizin]); return; }
        if (aralık_SMS(veri_DİZİ, Start_konum, girdi_BAĞ_DEĞ_SAY, "HOME")) { 넣기('/'); return; }
        if (aralık_SMS(veri_DİZİ, Start_konum, girdi_BAĞ_DEĞ_SAY, "?")) {
            int veri_değer = Durum_değer, rakam = 100; boolean 시작여부 = false;
            while (rakam > 0) { int 뒷값 = veri_değer / rakam; if (뒷값 != 0 || 시작여부 || rakam == 1) { 넣기('0' + 뒷값); 시작여부 = true; } veri_değer %= rakam; rakam /= 10; } return;
        }
        for (int Loop_Dizin = 0; Loop_Dizin < 16; Loop_Dizin++) if (이름길이[Loop_Dizin] == girdi_BAĞ_DEĞ_SAY) {
            boolean KAÇINCI = true; for (int iç_konum = 0; iç_konum < girdi_BAĞ_DEĞ_SAY; iç_konum++) if (değişken_ad[Loop_Dizin * 32 + iç_konum] != veri_DİZİ[Start_konum + iç_konum]) KAÇINCI = false;
            if (KAÇINCI) { for (int iç_konum = 0; iç_konum < değer_süre[Loop_Dizin]; iç_konum++) 넣기(değişken_veri[Loop_Dizin * 256 + iç_konum]); return; }
        }
    }
    static boolean Word_değer(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = çalıştır[중첩깊이 * 128 + 낱말번호], Bitiş_konum = 끝[중첩깊이 * 128 + 낱말번호], TABAN_konum = 중첩깊이 * 4096, Alıntı = 0;
        if (읽는자리 < Bitiş_konum && kaynakKod[TABAN_konum + 읽는자리] == '~' && (읽는자리 + 1 == Bitiş_konum || kaynakKod[TABAN_konum + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < Bitiş_konum) {
            int kod_noktası = kaynakKod[TABAN_konum + 읽는자리++];
            if (kod_noktası == Alıntı) { Alıntı = 0; continue; }
            if (Alıntı == 0 && (kod_noktası == 39 || kod_noktası == 34)) { Alıntı = kod_noktası; continue; }
            if (kod_noktası == '\\' && Alıntı != 39) { int Sonraki_konum = kaynakKod[TABAN_konum + 읽는자리++]; if (Alıntı == 34 && Sonraki_konum != '$' && Sonraki_konum != '"' && Sonraki_konum != '\\') 넣기('\\'); 넣기(Sonraki_konum); continue; }
            if (kod_noktası == '$' && Alıntı != 39 && 읽는자리 < Bitiş_konum) {
                boolean 중괄호자리 = kaynakKod[TABAN_konum + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < Bitiş_konum && kaynakKod[TABAN_konum + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < Bitiş_konum && 이름뒤(kaynakKod[TABAN_konum + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == Bitiş_konum || kaynakKod[TABAN_konum + 읽는자리] != '}')) { hata("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                değişken_değer(kaynakKod, TABAN_konum + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(kod_noktası);
        }
        return !uzantı_hata;
    }
    static int ortam_Ayarlar(int bağımsız_değişken_Dizin, boolean kaldırmak) {
        int yerel_Start = KomutYorumlayıcı.시작점[bağımsız_değişken_Dizin], Bitiş_konum = yerel_Start + KomutYorumlayıcı.süre_değer[bağımsız_değişken_Dizin], 같음자리 = yerel_Start;
        while (같음자리 < Bitiş_konum && KomutYorumlayıcı.belirteç_değer[같음자리] != '=') 같음자리++;
        int girdi_BAĞ_DEĞ_SAY = 같음자리 - yerel_Start;
        if (girdi_BAĞ_DEĞ_SAY < 1 || girdi_BAĞ_DEĞ_SAY > 31 || !ad_karakter(KomutYorumlayıcı.belirteç_değer[yerel_Start]) || !kaldırmak && 같음자리 == Bitiş_konum || Bitiş_konum - 같음자리 - 1 > 255) return 2;
        for (int Loop_Dizin = yerel_Start; Loop_Dizin < 같음자리; Loop_Dizin++) if (!이름뒤(KomutYorumlayıcı.belirteç_değer[Loop_Dizin])) return 2;
        if (aralık_SMS(KomutYorumlayıcı.belirteç_değer, yerel_Start, girdi_BAĞ_DEĞ_SAY, "PWD") || aralık_SMS(KomutYorumlayıcı.belirteç_değer, yerel_Start, girdi_BAĞ_DEĞ_SAY, "HOME")) return 2;
        int 찾은여부 = -1, bilgi_teknolojisi_boş_Durum = -1;
        for (int Loop_Dizin = 0; Loop_Dizin < 16; Loop_Dizin++) {
            if (이름길이[Loop_Dizin] == 0) bilgi_teknolojisi_boş_Durum = Loop_Dizin;
            if (이름길이[Loop_Dizin] != girdi_BAĞ_DEĞ_SAY) continue;
            boolean KAÇINCI = true; for (int iç_konum = 0; iç_konum < girdi_BAĞ_DEĞ_SAY; iç_konum++) if (değişken_ad[Loop_Dizin * 32 + iç_konum] != KomutYorumlayıcı.belirteç_değer[yerel_Start + iç_konum]) KAÇINCI = false;
            if (KAÇINCI) 찾은여부 = Loop_Dizin;
        }
        if (kaldırmak) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = bilgi_teknolojisi_boş_Durum; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = girdi_BAĞ_DEĞ_SAY; değer_süre[찾은여부] = Bitiş_konum - 같음자리 - 1;
        for (int Loop_Dizin = 0; Loop_Dizin < girdi_BAĞ_DEĞ_SAY; Loop_Dizin++) değişken_ad[찾은여부 * 32 + Loop_Dizin] = KomutYorumlayıcı.belirteç_değer[yerel_Start + Loop_Dizin];
        for (int Loop_Dizin = 같음자리 + 1; Loop_Dizin < Bitiş_konum; Loop_Dizin++) değişken_veri[찾은여부 * 256 + Loop_Dizin - 같음자리 - 1] = KomutYorumlayıcı.belirteç_değer[Loop_Dizin];
        return 0;
    }
    static void şov_ortam() {
        단말.Yazma("HOME=/\nPWD="); BellekDosyaları.geçerli_yazma(); 단말.문자(10);
        for (int Loop_Dizin = 0; Loop_Dizin < 16; Loop_Dizin++) if (이름길이[Loop_Dizin] > 0) {
            for (int iç_konum = 0; iç_konum < 이름길이[Loop_Dizin]; iç_konum++) Pano.직렬쓰기(değişken_ad[Loop_Dizin * 32 + iç_konum]); 단말.문자('=');
            for (int iç_konum = 0; iç_konum < değer_süre[Loop_Dizin]; iç_konum++) Pano.직렬쓰기(değişken_veri[Loop_Dizin * 256 + iç_konum]); 단말.문자(10);
        }
    }
    static void yürütmek_komut(int[] veri_DİZİ, int 시작변위, int girdi_BAĞ_DEĞ_SAY, int 중첩깊이) {
        if (중첩깊이 >= 4 || girdi_BAĞ_DEĞ_SAY > 4096) { hata("komut 파일의 iç_içe_yerleştirme_değer 또는 girdi_satırı süre_değer 제한을 넘었습니다"); return; }
        for (int Loop_Dizin = 0; Loop_Dizin < girdi_BAĞ_DEĞ_SAY; Loop_Dizin++) kaynakKod[중첩깊이 * 4096 + Loop_Dizin] = veri_DİZİ[시작변위 + Loop_Dizin];
        int toplam_BAĞ_DEĞ_SAY = Okuma(girdi_BAĞ_DEĞ_SAY, 중첩깊이); if (toplam_BAĞ_DEĞ_SAY < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < toplam_BAĞ_DEĞ_SAY) {
            int Grup_Bitiş = 읽는자리;
            while (Grup_Bitiş < toplam_BAĞ_DEĞ_SAY && (Tip_değer[중첩깊이 * 128 + Grup_Bitiş] == 0 || Tip_değer[중첩깊이 * 128 + Grup_Bitiş] >= 4)) Grup_Bitiş++;
            boolean yürütmek = 조건성립 == 1 || 조건성립 == 2 && Durum_değer == 0 || 조건성립 == 3 && Durum_değer != 0;
            if (yürütmek) {
                boolean Önceki_öğe_Dizin = false;
                while (읽는자리 < Grup_Bitiş) {
                    int Sonraki_konum = 읽는자리; while (Sonraki_konum < Grup_Bitiş && Tip_değer[중첩깊이 * 128 + Sonraki_konum] != 4) Sonraki_konum++;
                    boolean bağla_akış = Sonraki_konum < Grup_Bitiş; int artış_sayfa = -1, çıktı_sayfa = -1, 출력방식 = 0;
                    KomutYorumlayıcı.belirteç_BAĞ_DEĞ_SAY = 0; 쓴수 = 0; uzantı_hata = false;
                    for (int Loop_Dizin = 읽는자리; Loop_Dizin < Sonraki_konum; Loop_Dizin++) {
                        int veri_Tip = Tip_değer[중첩깊이 * 128 + Loop_Dizin];
                        if (veri_Tip >= 5) { if (veri_Tip == 7) { if (artış_sayfa >= 0) { hata("artış_değer 전환이 겹쳤습니다"); return; } artış_sayfa = ++Loop_Dizin; } else { if (çıktı_sayfa >= 0) { hata("metinÇıktısı 전환이 겹쳤습니다"); return; } çıktı_sayfa = ++Loop_Dizin; 출력방식 = veri_Tip; } continue; }
                        if (KomutYorumlayıcı.belirteç_BAĞ_DEĞ_SAY == 32) { hata("인수가 너무 많습니다"); return; }
                        int bağımsız_değişken_Dizin = KomutYorumlayıcı.belirteç_BAĞ_DEĞ_SAY++; KomutYorumlayıcı.시작점[bağımsız_değişken_Dizin] = 쓴수;
                        if (!Word_değer(Loop_Dizin, 중첩깊이)) return;
                        KomutYorumlayıcı.süre_değer[bağımsız_değişken_Dizin] = 쓴수 - KomutYorumlayıcı.시작점[bağımsız_değişken_Dizin];
                    }
                    연결중 = Önceki_öğe_Dizin || bağla_akış || artış_sayfa >= 0 || çıktı_sayfa >= 0;
                    if (연결중 && (KomutYorumlayıcı.같음(0, "vi") || KomutYorumlayıcı.같음(0, "edit") || KomutYorumlayıcı.같음(0, "load") || KomutYorumlayıcı.같음(0, "gui") || KomutYorumlayıcı.같음(0, "terminal") || KomutYorumlayıcı.같음(0, "sh") || KomutYorumlayıcı.같음(0, "source"))) { hata("devralmak 명령과 komut 파일은 G_Ç 전환이나 akış_değer 연결에 쓸 수 없습니다"); return; }
                    셸입출력.çalıştır(Önceki_öğe_Dizin, bağla_akış);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int girdi_konum = 입출력바꿈 == 0 ? artış_sayfa : çıktı_sayfa; if (girdi_konum < 0) continue;
                        int Start_konum = 쓴수; if (!Word_değer(girdi_konum, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = BellekDosyaları.yol_Start(쓴수 - Start_konum);
                        for (int iç_konum = Start_konum; 처리값 >= 0 && iç_konum < 쓴수; iç_konum++) 처리값 = BellekDosyaları.yol_bayt(iç_konum - Start_konum, KomutYorumlayıcı.belirteç_değer[iç_konum]);
                        if (처리값 >= 0) 처리값 = BellekDosyaları.Aç(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); KomutYorumlayıcı.hata(처리값); Durum_değer = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.giriş_dosyası = 처리값; else 셸입출력.çıkış_dosyası = 처리값;
                    }
                    셸입출력.İzin_Ver_devralmak = 중첩깊이 == 0 && 읽는자리 == 0 && Sonraki_konum == toplam_BAĞ_DEĞ_SAY;
                    깊이 = 중첩깊이; KomutYorumlayıcı.sonuç = 0; Pano.입출력전환(1);
                    KomutYorumlayıcı.komut();
                    Pano.uçbirim(3);
                    int 반환값 = KomutYorumlayıcı.sonuç, akış_hata = 셸입출력.hata_değer;
                    셸입출력.끝(); 연결중 = false;
                    Durum_değer = akış_hata < 0 ? 1 : 반환값;
                    if (akış_hata < 0) { KomutYorumlayıcı.hata(akış_hata); return; }
                    if (betik_Bitiş || 반환값 == -1005) return;
                    Önceki_öğe_Dizin = true; 읽는자리 = Sonraki_konum + 1;
                }
            }
            if (Grup_Bitiş < toplam_BAĞ_DEĞ_SAY) 조건성립 = Tip_değer[중첩깊이 * 128 + Grup_Bitiş];
            읽는자리 = Grup_Bitiş + 1;
        }
    }
    static void yürütmek_Dosya() {
        if (KomutYorumlayıcı.belirteç_BAĞ_DEĞ_SAY != 2 || 깊이 >= 3) { KomutYorumlayıcı.sonuç = 2; 단말.Yazma("사용법: sh dosya (iç_içe_yerleştirme_değer 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = KomutYorumlayıcı.yol(1); if (처리값 >= 0) 처리값 = BellekDosyaları.Aç(0);
        if (처리값 < 0) { KomutYorumlayıcı.hata(처리값); return; }
        int girdi_BAĞ_DEĞ_SAY = 0, bayt_veri;
        while ((bayt_veri = BellekDosyaları.Okuma(처리값)) != 256 && bayt_veri >= 0 && girdi_BAĞ_DEĞ_SAY < 16384) betik_değer[중첩깊이 * 16384 + girdi_BAĞ_DEĞ_SAY++] = bayt_veri;
        BellekDosyaları.Kapat(처리값); Pano.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < girdi_BAĞ_DEĞ_SAY && !betik_Bitiş;) {
            int Bitiş_konum = 읽는자리; while (Bitiş_konum < girdi_BAĞ_DEĞ_SAY && betik_değer[중첩깊이 * 16384 + Bitiş_konum] != 10) Bitiş_konum++;
            int geçerli_süre = Bitiş_konum - 읽는자리; if (geçerli_süre > 0 && betik_değer[중첩깊이 * 16384 + Bitiş_konum - 1] == 13) geçerli_süre--;
            yürütmek_komut(betik_değer, 중첩깊이 * 16384 + 읽는자리, geçerli_süre, 중첩깊이); 읽는자리 = Bitiş_konum + 1;
        }
        KomutYorumlayıcı.sonuç = Durum_değer; betik_Bitiş = false; 깊이 = 중첩깊이 - 1;
    }
}
