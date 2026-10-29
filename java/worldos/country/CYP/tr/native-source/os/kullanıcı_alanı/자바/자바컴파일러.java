// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java kaynak_ağaç -> 표준 버전 49 class derleyici. */
public final class 자바컴파일러 {
    static int[] kaynakKod = new int[16384], metinÇıktısı = new int[16384], KOD_değer = new int[4096];
    static int[] belirteç_Tip = new int[2048], belirteç_konum = new int[2048], belirteç_süre = new int[2048];
    static int[] sabit_değer = new int[4096], sabit_Ofset = new int[512];
    static int[] 문자 = new int[512], dosya_adı_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int kaynak_boyutlandırmak, belirteç_BAĞ_DEĞ_SAY, konum, KOD_boyutlandırmak, sabit_boyutlandırmak, sabit_BAĞ_DEĞ_SAY = 1, çıktı_boyutlandırmak, karakter_süre;
    static boolean hata;
    static int Sınıf_belirteç, Sınıf_sabit, ana_sabit, KOD_sabit;
    static int[] metot_girdi_ad = new int[32], metot_İade = new int[32], metot_bağımsız_değişken_BAĞ_DEĞ_SAY = new int[32];
    static int[] metot_bağımsız_değişken_ad = new int[512], metot_bağımsız_değişken_TÜR = new int[512];
    static int[] metot_gövdesi = new int[32], metot_Bitiş = new int[32], metot_KOD = new int[32];
    static int[] metot_süre = new int[32], 함수지역 = new int[32], metot_ad_sabit = new int[32], metot_tanımlayıcı_sabit = new int[32];
    static int[] metot_erişim = new int[32];
    static int metot_BAĞ_DEĞ_SAY, geçerli_metot, yerel_BAĞ_DEĞ_SAY, 깊이, 식깊이;
    static int[] yerel_ad = new int[128], yerel_TÜR = new int[128], 지역깊이 = new int[128];

    static void hata_değer(String 이유) {
        if (!hata) {
            kullanıcı_alanı.Yazma("javac error: "); kullanıcı_alanı.Yazma(이유);
            kullanıcı_alanı.Yazma(" at line ");
            int girdi_satırı = 1, 끝 = konum < belirteç_BAĞ_DEĞ_SAY ? belirteç_konum[konum] : kaynak_boyutlandırmak;
            for (int 수 = 0; 수 < 끝; 수++) if (kaynakKod[수] == 10) girdi_satırı++;
            자바도구.수쓰기(girdi_satırı); kullanıcı_alanı.yazma_karakter_değer(10);
        }
        hata = true;
    }
    static boolean karakter_değer(int değer) { return 문자이름규칙.첫글자(değer); }
    static boolean rakam_değer(int değer) { return değer >= '0' && değer <= '9'; }
    static boolean 이름같음(int 가, int SANİYE_işlenen) {
        if (가 < 0 || SANİYE_işlenen < 0 || 가 >= belirteç_BAĞ_DEĞ_SAY || SANİYE_işlenen >= belirteç_BAĞ_DEĞ_SAY || belirteç_süre[가] != belirteç_süre[SANİYE_işlenen]) return false;
        for (int 수 = 0; 수 < belirteç_süre[가]; 수++) if (kaynakKod[belirteç_konum[가] + 수] != kaynakKod[belirteç_konum[SANİYE_işlenen] + 수]) return false;
        return true;
    }
    static boolean Word_değer(int belirteç_değer, String Word_SMS) {
        if (belirteç_değer < 0 || belirteç_değer >= belirteç_BAĞ_DEĞ_SAY || belirteç_süre[belirteç_değer] != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < Word_SMS.length(); 수++) if (kaynakKod[belirteç_konum[belirteç_değer] + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static int Tip_değer() { return konum < belirteç_BAĞ_DEĞ_SAY ? belirteç_Tip[konum] : 0; }
    static boolean almak(int değer) { if (Tip_değer() != değer) return false; konum++; return true; }
    static void gereksinim_değer(int değer) { if (!almak(değer)) hata_değer("unexpected token"); }
    static boolean AL_Word(String Word_SMS) { if (!Word_değer(konum, Word_SMS)) return false; konum++; return true; }
    static void 말요구(String Word_SMS) { if (!AL_Word(Word_SMS)) hata_değer(Word_SMS); }
    static int tanımlayıcı_değer() {
        int sonuç = konum;
        if (Tip_değer() != 256) hata_değer("identifier required"); else konum++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int çalıştır = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - çalıştır == belirteç_süre[sonuç];
                for (int yuva_girdi = çalıştır; 같음 && yuva_girdi < 수; yuva_girdi++) if (예약어.charAt(yuva_girdi) != kaynakKod[belirteç_konum[sonuç] + yuva_girdi - çalıştır]) 같음 = false;
                if (같음) hata_değer("reserved word cannot be an identifier");
                çalıştır = 수 + 1;
            }
        }
        return sonuç;
    }
    static void kesmek_değer() {
        int 수 = 0;
        while (수 < kaynak_boyutlandırmak && !hata) {
            int değer = kaynakKod[수], çalıştır = 수, Tip_değer = değer;
            if (değer == 32 || değer == 9 || değer == 10 || değer == 13) { 수++; continue; }
            if (değer == '/' && 수 + 1 < kaynak_boyutlandırmak && kaynakKod[수 + 1] == '/') {
                while (수 < kaynak_boyutlandırmak && kaynakKod[수] != 10) 수++;
                continue;
            }
            if (değer == '/' && 수 + 1 < kaynak_boyutlandırmak && kaynakKod[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < kaynak_boyutlandırmak && !(kaynakKod[수] == '*' && kaynakKod[수 + 1] == '/')) 수++;
                if (수 + 1 >= kaynak_boyutlandırmak) { hata_değer("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (karakter_değer(değer)) { Tip_değer = 256; while (수 < kaynak_boyutlandırmak && 문자이름규칙.이어진글자(kaynakKod[수])) 수++; }
            else if (rakam_değer(değer)) { Tip_değer = 257; while (수 < kaynak_boyutlandırmak && rakam_değer(kaynakKod[수])) 수++; }
            else if (değer == '"' || değer == '\'') {
                Tip_değer = değer == '"' ? 258 : 259; 수++;
                while (수 < kaynak_boyutlandırmak && kaynakKod[수] != değer && kaynakKod[수] != 10 && kaynakKod[수] != 13) {
                    if (kaynakKod[수] == '\\') 수++;
                    수++;
                }
                if (수 >= kaynak_boyutlandırmak || kaynakKod[수] != değer) { hata_değer("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < kaynak_boyutlandırmak) {
                    int Sonraki_öğe = kaynakKod[수];
                    if (değer == '=' && Sonraki_öğe == '=') Tip_değer = 300;
                    if (değer == '!' && Sonraki_öğe == '=') Tip_değer = 301;
                    if (değer == '<' && Sonraki_öğe == '=') Tip_değer = 302;
                    if (değer == '>' && Sonraki_öğe == '=') Tip_değer = 303;
                    if (değer == '&' && Sonraki_öğe == '&') Tip_değer = 304;
                    if (değer == '|' && Sonraki_öğe == '|') Tip_değer = 305;
                    if (değer == '+' && Sonraki_öğe == '+') Tip_değer = 306;
                    if (değer == '-' && Sonraki_öğe == '-') Tip_değer = 307;
                    if (değer == '+' && Sonraki_öğe == '=') Tip_değer = 308;
                    if (değer == '-' && Sonraki_öğe == '=') Tip_değer = 309;
                    if (değer == '*' && Sonraki_öğe == '=') Tip_değer = 310;
                    if (değer == '/' && Sonraki_öğe == '=') Tip_değer = 311;
                    if (değer == '%' && Sonraki_öğe == '=') Tip_değer = 312;
                    if (Tip_değer >= 300) 수++;
                }
            }
            if (belirteç_BAĞ_DEĞ_SAY == belirteç_Tip.length - 1) { hata_değer("too many tokens (2047 maximum)"); break; }
            belirteç_Tip[belirteç_BAĞ_DEĞ_SAY] = Tip_değer; belirteç_konum[belirteç_BAĞ_DEĞ_SAY] = çalıştır; belirteç_süre[belirteç_BAĞ_DEĞ_SAY++] = 수 - çalıştır;
        }
    }
    static void yazma_sabit_bayt(int değer) {
        if (sabit_boyutlandırmak == sabit_değer.length) { hata_değer("constant pool too large"); return; }
        sabit_değer[sabit_boyutlandırmak++] = değer & 255;
    }
    static void 상짧(int değer) { yazma_sabit_bayt(değer >> 8); yazma_sabit_bayt(değer); }
    static int yazmaç_sabit(int çalıştır) {
        for (int 수 = 1; 수 < sabit_BAĞ_DEĞ_SAY; 수++) {
            int ön_kamera_değer = sabit_Ofset[수], süre_değer = (수 + 1 < sabit_BAĞ_DEĞ_SAY ? sabit_Ofset[수 + 1] : çalıştır) - ön_kamera_değer;
            if (süre_değer != sabit_boyutlandırmak - çalıştır) continue;
            boolean 같음 = true;
            for (int yuva_girdi = 0; yuva_girdi < süre_değer; yuva_girdi++) if (sabit_değer[ön_kamera_değer + yuva_girdi] != sabit_değer[çalıştır + yuva_girdi]) 같음 = false;
            if (같음) { sabit_boyutlandırmak = çalıştır; return 수; }
        }
        if (sabit_BAĞ_DEĞ_SAY == sabit_Ofset.length) { hata_değer("too many constants"); return 0; }
        sabit_Ofset[sabit_BAĞ_DEĞ_SAY] = çalıştır;
        return sabit_BAĞ_DEĞ_SAY++;
    }
    static void Ekleme_SMS(int değer) {
        if (karakter_süre == 문자.length) { hata_değer("text too long"); return; }
        문자[karakter_süre++] = değer;
    }
    static void Ekleme_Word(String Word_SMS) { for (int 수 = 0; 수 < Word_SMS.length(); 수++) Ekleme_SMS(Word_SMS.charAt(수)); }
    static int karakter_sabit() {
        int çalıştır = sabit_boyutlandırmak; yazma_sabit_bayt(1); 상짧(0);
        for (int 수 = 0; 수 < karakter_süre; 수++) {
            int değer = 문자[수];
            if (değer > 0 && değer < 128) yazma_sabit_bayt(değer);
            else if (değer < 2048) { yazma_sabit_bayt(192 | değer >> 6); yazma_sabit_bayt(128 | değer & 63); }
            else { yazma_sabit_bayt(224 | değer >> 12); yazma_sabit_bayt(128 | değer >> 6 & 63); yazma_sabit_bayt(128 | değer & 63); }
        }
        if (hata) return 0;
        int süre_değer = sabit_boyutlandırmak - çalıştır - 3;
        sabit_değer[çalıştır + 1] = süre_değer >> 8; sabit_değer[çalıştır + 2] = süre_değer & 255;
        return yazmaç_sabit(çalıştır);
    }
    static int Word_sabit(String Word_SMS) { karakter_süre = 0; Ekleme_Word(Word_SMS); return karakter_sabit(); }
    static int belirteç_sabit(int belirteç_değer) {
        karakter_süre = 0;
        for (int 수 = 0; 수 < belirteç_süre[belirteç_değer]; 수++) Ekleme_SMS(kaynakKod[belirteç_konum[belirteç_değer] + 수]);
        return karakter_sabit();
    }
    static int Başvuru(int Tip_değer, int 가, int SANİYE_işlenen) {
        int çalıştır = sabit_boyutlandırmak; yazma_sabit_bayt(Tip_değer); 상짧(가);
        if (Tip_değer == 9 || Tip_değer == 10 || Tip_değer == 12) 상짧(SANİYE_işlenen);
        return yazmaç_sabit(çalıştır);
    }
    static int dış_Başvuru(int Tip_değer, String sahip_değer, String İsim, String 서술) {
        int sahip_tanımlayıcı = Başvuru(7, Word_sabit(sahip_değer), 0);
        int ad_BAĞ_DEĞ_SAY = Word_sabit(İsim), biçim_BAĞ_DEĞ_SAY = Word_sabit(서술);
        return Başvuru(Tip_değer, sahip_tanımlayıcı, Başvuru(12, ad_BAĞ_DEĞ_SAY, biçim_BAĞ_DEĞ_SAY));
    }
    static void 내보내기(int değer) {
        if (KOD_boyutlandırmak == KOD_değer.length) { hata_değer("bytecode too large"); return; }
        KOD_değer[KOD_boyutlandırmak++] = değer & 255;
    }
    static void komut(int değer, int bağımsız_değişkenler) { 내보내기(değer); 내보내기(bağımsız_değişkenler >> 8); 내보내기(bağımsız_değişkenler); }
    static void 수상수(int değer) {
        if (değer >= -1 && değer <= 5) { 내보내기(değer + 3); return; }
        int çalıştır = sabit_boyutlandırmak; yazma_sabit_bayt(3); 상짧(değer >>> 16); 상짧(değer);
        komut(19, yazmaç_sabit(çalıştır));
    }
    static int dal(int komut) { int sonuç = KOD_boyutlandırmak; komut(komut, 0); return sonuç; }
    static void köprü_değer(int dal, int hedef_nesne) {
        if (hata) return;
        int 거리 = hedef_nesne - dal;
        if (거리 < -32768 || 거리 > 32767 || dal < 0 || dal + 2 >= KOD_boyutlandırmak) { hata_değer("invalid branch"); return; }
        KOD_değer[dal + 1] = 거리 >> 8 & 255; KOD_değer[dal + 2] = 거리 & 255;
    }
    static void Karşılaştırma_değer(int komut) {
        int DOĞRU_değer = dal(komut); 내보내기(3); int 끝 = dal(167);
        köprü_değer(DOĞRU_değer, KOD_boyutlandırmak); 내보내기(4); köprü_değer(끝, KOD_boyutlandırmak);
    }
    static int biçim_değer() {
        if (AL_Word("void")) return 0;
        if (AL_Word("int")) return 1;
        if (AL_Word("boolean")) return 2;
        if (AL_Word("char")) return 5;
        if (AL_Word("FileInputStream")) return 6;
        if (AL_Word("FileOutputStream")) return 7;
        if (AL_Word("String")) { if (almak('[')) { gereksinim_değer(']'); return 4; } return 3; }
        hata_değer("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void Ekle_biçim(int TÜR_değer) {
        if (TÜR_değer == 0) Ekleme_SMS('V');
        if (TÜR_değer == 1) Ekleme_SMS('I');
        if (TÜR_değer == 2) Ekleme_SMS('Z');
        if (TÜR_değer == 3) Ekleme_Word("Ljava/lang/String;");
        if (TÜR_değer == 4) Ekleme_Word("[Ljava/lang/String;");
        if (TÜR_değer == 5) Ekleme_SMS('C');
        if (TÜR_değer == 6) Ekleme_Word("Ljava/io/FileInputStream;");
        if (TÜR_değer == 7) Ekleme_Word("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws bildirim. özel_durum işlem_değer_girdi 본문은 konak javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = AL_Word("Türkçe");
        if (한국어묶음) { gereksinim_değer('.'); 말요구("Öz"); gereksinim_değer('.'); }
        if (!한국어묶음 && (AL_Word("Exception") || AL_Word("IOException"))) return;
        if (AL_Word("özel_durum") || AL_Word("yürütme_özel_durum") || AL_Word("G_Ç_özel_durum") || AL_Word("bekle_ZAMANAŞIMI_özel_durum") || AL_Word("ADRES_ARA_özel_durum") || AL_Word("파일없음예외") || AL_Word("iletişim_özel_durum") || AL_Word("geçersiz_bağımsız_değişken_özel_durum") || AL_Word("숫자형식예외") || AL_Word("범위예외") || AL_Word("배열범위예외") || AL_Word("문자열범위예외") || AL_Word("boş_referans_özel_durum") || AL_Word("산술예외") || AL_Word("Durum_özel_durum") || AL_Word("TÜR_Yayın_özel_durum") || AL_Word("Negatif_DİZİ_boyutlandırmak_hata") || AL_Word("DİZİ_depo_hata") || AL_Word("yazışma_Durum_özel_durum") || AL_Word("대기중단예외")) return;
        hata_değer("unsupported throws type");
    }
    static void 선언읽기() {
        while (AL_Word("import")) {
            if (Word_değer(konum, "Türkçe")) 예외이름읽기();
            else {
                말요구("java"); gereksinim_değer('.'); 말요구("io"); gereksinim_değer('.');
                if (!(AL_Word("FileInputStream") || AL_Word("FileOutputStream") || AL_Word("IOException"))) hata_değer("unsupported import");
            }
            gereksinim_değer(';');
        }
        AL_Word("public"); AL_Word("final"); 말요구("class"); Sınıf_belirteç = tanımlayıcı_değer();
        Sınıf_sabit = Başvuru(7, belirteç_sabit(Sınıf_belirteç), 0);
        ana_sabit = Başvuru(7, Word_sabit("java/lang/Object"), 0); KOD_sabit = Word_sabit("Code"); gereksinim_değer('{');
        while (!hata && Tip_değer() != '}') {
            if (metot_BAĞ_DEĞ_SAY == 32) { hata_değer("too many methods"); break; }
            int erişim_girdi = AL_Word("public") ? 1 : AL_Word("private") ? 2 : 0; 말요구("static");
            int işlev_değer = metot_BAĞ_DEĞ_SAY++;
            metot_erişim[işlev_değer] = erişim_girdi | 8;
            metot_İade[işlev_değer] = biçim_değer(); metot_girdi_ad[işlev_değer] = tanımlayıcı_değer(); gereksinim_değer('(');
            for (int ön_kamera_değer = 0; ön_kamera_değer < işlev_değer; ön_kamera_değer++) if (이름같음(metot_girdi_ad[ön_kamera_değer], metot_girdi_ad[işlev_değer])) hata_değer("duplicate method (overloading unsupported)");
            while (!hata && Tip_değer() != ')') {
                int 수 = metot_bağımsız_değişken_BAĞ_DEĞ_SAY[işlev_değer];
                if (수 == 16) { hata_değer("too many parameters"); break; }
                int TÜR_değer = biçim_değer(); if (TÜR_değer == 0) hata_değer("void parameter");
                metot_bağımsız_değişken_TÜR[işlev_değer * 16 + 수] = TÜR_değer; metot_bağımsız_değişken_ad[işlev_değer * 16 + 수] = tanımlayıcı_değer();
                metot_bağımsız_değişken_BAĞ_DEĞ_SAY[işlev_değer]++;
                if (!almak(',')) break;
            }
            gereksinim_değer(')');
            if (AL_Word("throws")) {
                do { 예외이름읽기(); } while (!hata && almak(','));
            }
            metot_gövdesi[işlev_değer] = konum; gereksinim_değer('{');
            int iç_içe_yerleştirme_değer = 1;
            while (konum < belirteç_BAĞ_DEĞ_SAY && iç_içe_yerleştirme_değer > 0) {
                if (Tip_değer() == '{') iç_içe_yerleştirme_değer++;
                if (Tip_değer() == '}') iç_içe_yerleştirme_değer--;
                konum++;
            }
            if (iç_içe_yerleştirme_değer != 0) hata_değer("unclosed method body");
            metot_Bitiş[işlev_değer] = konum;
            metot_ad_sabit[işlev_değer] = belirteç_sabit(metot_girdi_ad[işlev_değer]);
            karakter_süre = 0; Ekleme_SMS('(');
            for (int 수 = 0; 수 < metot_bağımsız_değişken_BAĞ_DEĞ_SAY[işlev_değer]; 수++) Ekle_biçim(metot_bağımsız_değişken_TÜR[işlev_değer * 16 + 수]);
            Ekleme_SMS(')'); Ekle_biçim(metot_İade[işlev_değer]); metot_tanımlayıcı_sabit[işlev_değer] = karakter_sabit();
        }
        gereksinim_değer('}'); if (konum != belirteç_BAĞ_DEĞ_SAY) hata_değer("extra input after class");
    }
    static int BUL_yerel(int İsim) {
        for (int 수 = yerel_BAĞ_DEĞ_SAY - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(yerel_ad[수], İsim)) return 수;
        hata_değer("unknown variable"); return 0;
    }
    static int Ekle_yerel(int İsim, int TÜR_değer) {
        for (int 수 = 0; 수 < yerel_BAĞ_DEĞ_SAY; 수++) if (지역깊이[수] >= 0 && 이름같음(yerel_ad[수], İsim)) hata_değer("duplicate local variable");
        if (yerel_BAĞ_DEĞ_SAY == 128) { hata_değer("too many locals"); return 0; }
        yerel_ad[yerel_BAĞ_DEĞ_SAY] = İsim; yerel_TÜR[yerel_BAĞ_DEĞ_SAY] = TÜR_değer; 지역깊이[yerel_BAĞ_DEĞ_SAY] = 깊이;
        return yerel_BAĞ_DEĞ_SAY++;
    }
    static boolean bilgi_TÜR(int TÜR_değer) { return TÜR_değer == 1 || TÜR_değer == 5; }
    static void 지역읽기(int 수) { 내보내기(yerel_TÜR[수] <= 2 || yerel_TÜR[수] == 5 ? 21 : 25); 내보내기(수); }
    static void yazma_yerel(int 수) { 내보내기(yerel_TÜR[수] <= 2 || yerel_TÜR[수] == 5 ? 54 : 58); 내보내기(수); }
    static void doğrulamak_TÜR(int fiili_veri, int 기대) { if (fiili_veri != 기대 && !(fiili_veri == 5 && 기대 == 1)) hata_değer("type mismatch"); }
    static void 문자읽기(int belirteç_değer) {
        karakter_süre = 0; int çalıştır = belirteç_konum[belirteç_değer] + 1, 끝 = belirteç_konum[belirteç_değer] + belirteç_süre[belirteç_değer] - 1;
        while (çalıştır < 끝 && !hata) {
            int değer = kaynakKod[çalıştır++];
            if (değer == '\\') {
                if (çalıştır == 끝) { hata_değer("invalid escape"); break; }
                değer = kaynakKod[çalıştır++];
                if (değer == 'n') değer = 10;
                else if (değer == 'r') değer = 13;
                else if (değer == 't') değer = 9;
                else if (değer == 'b') değer = 8;
                else if (değer == 'f') değer = 12;
                else if (değer != '\\' && değer != '"' && değer != '\'') hata_değer("unsupported escape");
            }
            Ekleme_SMS(değer);
        }
    }
    static int ayrıştırmak_bilgi(int belirteç_değer, boolean Negatif_değer) {
        if (belirteç_süre[belirteç_değer] > 1 && kaynakKod[belirteç_konum[belirteç_değer]] == '0') hata_değer("octal literals unsupported");
        int değer = 0;
        for (int 수 = 0; 수 < belirteç_süre[belirteç_değer]; 수++) {
            int rakam_öğe = kaynakKod[belirteç_konum[belirteç_değer] + 수] - '0';
            if (değer < -214748364 || değer == -214748364 && rakam_öğe > (Negatif_değer ? 8 : 7)) hata_değer("integer literal out of range");
            değer = değer * 10 - rakam_öğe;
        }
        return Negatif_değer ? değer : -değer;
    }
    static int 기본식() {
        if (AL_Word("new")) {
            int TÜR_değer = biçim_değer();
            if (TÜR_değer != 6 && TÜR_değer != 7) { hata_değer("only file streams supported by new in source"); return 0; }
            String sahip_değer = TÜR_değer == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            komut(187, Başvuru(7, Word_sabit(sahip_değer), 0)); 내보내기(89);
            gereksinim_değer('('); doğrulamak_TÜR(ifade_değer(), 3); boolean 이어 = false;
            if (almak(',')) { if (TÜR_değer != 7) hata_değer("input stream constructor arguments"); doğrulamak_TÜR(ifade_değer(), 2); 이어 = true; }
            gereksinim_değer(')');
            komut(183, dış_Başvuru(10, sahip_değer, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TÜR_değer;
        }
        if (almak('(')) { int TÜR_değer = ifade_değer(); gereksinim_değer(')'); return TÜR_değer; }
        if (Tip_değer() == 257) { 수상수(ayrıştırmak_bilgi(konum++, false)); return 1; }
        if (Tip_değer() == 258) { 문자읽기(konum++); komut(19, Başvuru(8, karakter_sabit(), 0)); return 3; }
        if (Tip_değer() == 259) { 문자읽기(konum++); if (karakter_süre != 1) hata_değer("character literal length"); 수상수(문자[0]); return 5; }
        if (AL_Word("true")) { 내보내기(4); return 2; }
        if (AL_Word("false")) { 내보내기(3); return 2; }
        if (AL_Word("Türkçe")) {
            gereksinim_değer('.'); 말요구("Öz"); gereksinim_değer('.');
            String sahip_değer = "", metot_değer = "", 서술 = ""; int 가 = 0, SANİYE_işlenen = 0, 다 = 0, 라 = 0, 마 = 0, sonuç = 0;
            if (AL_Word("metinÇıktısı")) {
                sahip_değer = "Türkçe/Öz/metinÇıktısı"; gereksinim_değer('.');
                if (AL_Word("yazma_hat")) { metot_değer = "yazma_hat"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (AL_Word("Yazma")) { metot_değer = "Yazma"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (AL_Word("수쓰기")) { metot_değer = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else hata_değer("unknown Korean output method");
            } else if (AL_Word("문자")) {
                sahip_değer = "Türkçe/Öz/문자"; gereksinim_değer('.'); 가 = 3;
                if (AL_Word("süre_değer")) { metot_değer = "süre_değer"; 서술 = "(Ljava/lang/String;)I"; sonuç = 1; }
                else if (AL_Word("kod_öğesi_BAĞ_DEĞ_SAY")) { metot_değer = "kod_öğesi_BAĞ_DEĞ_SAY"; 서술 = "(Ljava/lang/String;)I"; sonuç = 1; }
                else if (AL_Word("ayrıştırmak_bilgi")) { metot_değer = "ayrıştırmak_bilgi"; 서술 = "(Ljava/lang/String;)I"; sonuç = 1; }
                else if (AL_Word("yazma_bilgi_değer")) { metot_değer = "yazma_bilgi_değer"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; sonuç = 3; }
                else if (AL_Word("같음")) { metot_değer = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; SANİYE_işlenen = 3; sonuç = 2; }
                else if (AL_Word("yapıştırmak_SMS")) { metot_değer = "yapıştırmak_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; SANİYE_işlenen = 3; sonuç = 3; }
                else if (AL_Word("kesmek_değer")) { metot_değer = "kesmek_değer"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; SANİYE_işlenen = 1; 다 = 1; sonuç = 3; }
                else hata_değer("unknown Korean text method");
            } else if (AL_Word("dosya")) {
                sahip_değer = "Türkçe/Öz/dosya"; gereksinim_değer('.'); 가 = 3;
                if (AL_Word("Okuma")) { metot_değer = "Okuma"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; sonuç = 3; }
                else if (AL_Word("Yazma")) { metot_değer = "Yazma"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; SANİYE_işlenen = 3; }
                else hata_değer("unknown Korean file method");
            } else if (AL_Word("화면")) {
                sahip_değer = "Türkçe/Öz/화면"; gereksinim_değer('.');
                if (AL_Word("너비")) { metot_değer = "너비"; 서술 = "()I"; sonuç = 1; }
                else if (AL_Word("높이")) { metot_değer = "높이"; 서술 = "()I"; sonuç = 1; }
                else if (AL_Word("dikdörtgen")) { metot_değer = "dikdörtgen"; 서술 = "(IIIII)V"; 가 = 1; SANİYE_işlenen = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (AL_Word("silmek_girdi")) { metot_değer = "silmek_girdi"; 서술 = "(I)V"; 가 = 1; }
                else if (AL_Word("기다리기")) { metot_değer = "기다리기"; 서술 = "()V"; }
                else hata_değer("unknown Korean framebuffer method");
            } else hata_değer("unsupported Korean library class");
            gereksinim_değer('('); if (가 != 0) doğrulamak_TÜR(ifade_değer(), 가);
            if (SANİYE_işlenen != 0) { gereksinim_değer(','); doğrulamak_TÜR(ifade_değer(), SANİYE_işlenen); }
            if (다 != 0) { gereksinim_değer(','); doğrulamak_TÜR(ifade_değer(), 다); }
            if (라 != 0) { gereksinim_değer(','); doğrulamak_TÜR(ifade_değer(), 라); }
            if (마 != 0) { gereksinim_değer(','); doğrulamak_TÜR(ifade_değer(), 마); }
            gereksinim_değer(')'); komut(184, dış_Başvuru(10, sahip_değer, metot_değer, 서술)); return sonuç;
        }
        if (AL_Word("Integer")) {
            gereksinim_değer('.'); 말요구("parseInt"); gereksinim_değer('('); doğrulamak_TÜR(ifade_değer(), 3); gereksinim_değer(')');
            komut(184, dış_Başvuru(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int İsim = tanımlayıcı_değer();
        if (almak('(')) {
            int işlev_değer = -1;
            for (int 수 = 0; 수 < metot_BAĞ_DEĞ_SAY; 수++) if (이름같음(İsim, metot_girdi_ad[수])) işlev_değer = 수;
            if (işlev_değer < 0) { hata_değer("unknown static method"); return 0; }
            int 수 = 0;
            while (!hata && Tip_değer() != ')') {
                if (수 >= metot_bağımsız_değişken_BAĞ_DEĞ_SAY[işlev_değer]) { hata_değer("too many arguments"); break; }
                doğrulamak_TÜR(ifade_değer(), metot_bağımsız_değişken_TÜR[işlev_değer * 16 + 수++]); if (!almak(',')) break;
            }
            gereksinim_değer(')'); if (수 != metot_bağımsız_değişken_BAĞ_DEĞ_SAY[işlev_değer]) hata_değer("argument count mismatch");
            komut(184, Başvuru(10, Sınıf_sabit, Başvuru(12, metot_ad_sabit[işlev_değer], metot_tanımlayıcı_sabit[işlev_değer])));
            return metot_İade[işlev_değer];
        }
        int yerel_Scope = BUL_yerel(İsim), TÜR_değer = yerel_TÜR[yerel_Scope]; 지역읽기(yerel_Scope);
        while (!hata) {
            if (almak('[')) { doğrulamak_TÜR(TÜR_değer, 4); doğrulamak_TÜR(ifade_değer(), 1); gereksinim_değer(']'); 내보내기(50); TÜR_değer = 3; }
            else if (almak('.')) {
                if (TÜR_değer == 6 || TÜR_değer == 7) {
                    String sahip_değer = TÜR_değer == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (AL_Word("close")) { gereksinim_değer('('); gereksinim_değer(')'); komut(182, dış_Başvuru(10, sahip_değer, "close", "()V")); TÜR_değer = 0; }
                    else if (TÜR_değer == 6 && AL_Word("read")) { gereksinim_değer('('); gereksinim_değer(')'); komut(182, dış_Başvuru(10, sahip_değer, "read", "()I")); TÜR_değer = 1; }
                    else if (TÜR_değer == 7 && AL_Word("write")) { gereksinim_değer('('); doğrulamak_TÜR(ifade_değer(), 1); gereksinim_değer(')'); komut(182, dış_Başvuru(10, sahip_değer, "write", "(I)V")); TÜR_değer = 0; }
                    else { hata_değer("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TÜR_değer == 4) { 내보내기(190); TÜR_değer = 1; }
                else { doğrulamak_TÜR(TÜR_değer, 3); gereksinim_değer('('); gereksinim_değer(')'); komut(182, dış_Başvuru(10, "java/lang/String", "length", "()I")); TÜR_değer = 1; }
            } else break;
        }
        return TÜR_değer;
    }
    static int 단항() {
        if (++식깊이 > 64) { hata_değer("expression nesting too deep"); 식깊이--; return 0; }
        int TÜR_değer;
        if (almak('!')) { doğrulamak_TÜR(단항(), 2); Karşılaştırma_değer(153); TÜR_değer = 2; }
        else if (almak('-')) {
            if (Tip_değer() == 257) 수상수(ayrıştırmak_bilgi(konum++, true));
            else { doğrulamak_TÜR(단항(), 1); 내보내기(116); }
            TÜR_değer = 1;
        } else if (almak('+')) { doğrulamak_TÜR(단항(), 1); TÜR_değer = 1; }
        else TÜR_değer = 기본식();
        식깊이--; return TÜR_değer;
    }
    static int 곱식() {
        int TÜR_değer = 단항();
        while (!hata && (Tip_değer() == '*' || Tip_değer() == '/' || Tip_değer() == '%')) {
            int kodlama_değer = Tip_değer(); konum++; doğrulamak_TÜR(TÜR_değer, 1); doğrulamak_TÜR(단항(), 1);
            내보내기(kodlama_değer == '*' ? 104 : kodlama_değer == '/' ? 108 : 112); TÜR_değer = 1;
        }
        return TÜR_değer;
    }
    static int 합식() {
        int TÜR_değer = 곱식();
        while (!hata && (Tip_değer() == '+' || Tip_değer() == '-')) {
            int kodlama_değer = Tip_değer(); konum++; int sınır_değer = KOD_boyutlandırmak, BACK_değer_türü = 곱식();
            if (kodlama_değer == '+' && (TÜR_değer == 3 || BACK_değer_türü == 3)) { 결합(sınır_değer, TÜR_değer, BACK_değer_türü); TÜR_değer = 3; }
            else { doğrulamak_TÜR(TÜR_değer, 1); doğrulamak_TÜR(BACK_değer_türü, 1); 내보내기(kodlama_değer == '+' ? 96 : 100); TÜR_değer = 1; }
        }
        return TÜR_değer;
    }
    static int takılı_Başvuru(int TÜR_değer) {
        if (TÜR_değer != 1 && TÜR_değer != 2 && TÜR_değer != 3 && TÜR_değer != 5) hata_değer("unsupported concatenation type");
        return dış_Başvuru(10, "java/lang/StringBuilder", "append", TÜR_değer == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TÜR_değer == 2 ? "(Z)Ljava/lang/StringBuilder;" : TÜR_değer == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int sınır_değer, int ön_kamera_değer_türü, int BACK_değer_türü) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 hak KOD_değer 앞에 oluşturmak 코드를 삽입한다.
        // hak ifade_değer 내부의 eş_değer dal 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = KOD_boyutlandırmak;
        komut(187, Başvuru(7, Word_sabit("java/lang/StringBuilder"), 0)); 내보내기(89);
        komut(183, dış_Başvuru(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); komut(182, takılı_Başvuru(ön_kamera_değer_türü));
        if (hata) return;
        int süre_değer = KOD_boyutlandırmak - 끝;
        for (int 수 = 0; 수 < süre_değer; 수++) 삽입코드[수] = KOD_değer[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= sınır_değer; 수--) KOD_değer[수 + süre_değer] = KOD_değer[수];
        for (int 수 = 0; 수 < süre_değer; 수++) KOD_değer[sınır_değer + 수] = 삽입코드[수];
        komut(182, takılı_Başvuru(BACK_değer_türü)); komut(182, dış_Başvuru(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Karşılaştırma_ifade() {
        int TÜR_değer = 합식();
        while (!hata && (Tip_değer() == '<' || Tip_değer() == '>' || Tip_değer() == 302 || Tip_değer() == 303)) {
            int kodlama_değer = Tip_değer(); konum++; doğrulamak_TÜR(TÜR_değer, 1); doğrulamak_TÜR(합식(), 1);
            Karşılaştırma_değer(kodlama_değer == '<' ? 161 : kodlama_değer == '>' ? 163 : kodlama_değer == 302 ? 164 : 162); TÜR_değer = 2;
        }
        return TÜR_değer;
    }
    static int 동등식() {
        int TÜR_değer = Karşılaştırma_ifade();
        while (!hata && (Tip_değer() == 300 || Tip_değer() == 301)) {
            int kodlama_değer = Tip_değer(); konum++; int BACK_değer_türü = Karşılaştırma_ifade();
            if (TÜR_değer == 0 || BACK_değer_türü == 0) hata_değer("void expression");
            if (!(bilgi_TÜR(TÜR_değer) && bilgi_TÜR(BACK_değer_türü))) doğrulamak_TÜR(BACK_değer_türü, TÜR_değer);
            Karşılaştırma_değer((TÜR_değer <= 2 || TÜR_değer == 5 ? 159 : 165) + (kodlama_değer == 301 ? 1 : 0)); TÜR_değer = 2;
        }
        return TÜR_değer;
    }
    static int VE() {
        int TÜR_değer = 동등식();
        while (!hata && almak(304)) {
            doğrulamak_TÜR(TÜR_değer, 2); int 가 = dal(153); doğrulamak_TÜR(동등식(), 2); int SANİYE_işlenen = dal(153);
            내보내기(4); int 끝 = dal(167); köprü_değer(가, KOD_boyutlandırmak); köprü_değer(SANİYE_işlenen, KOD_boyutlandırmak); 내보내기(3); köprü_değer(끝, KOD_boyutlandırmak); TÜR_değer = 2;
        }
        return TÜR_değer;
    }
    static int ifade_değer() {
        int TÜR_değer = VE();
        while (!hata && almak(305)) {
            doğrulamak_TÜR(TÜR_değer, 2); int 가 = dal(154); doğrulamak_TÜR(VE(), 2); int SANİYE_işlenen = dal(154);
            내보내기(3); int 끝 = dal(167); köprü_değer(가, KOD_boyutlandırmak); köprü_değer(SANİYE_işlenen, KOD_boyutlandırmak); 내보내기(4); köprü_değer(끝, KOD_boyutlandırmak); TÜR_değer = 2;
        }
        return TÜR_değer;
    }
    static void ödev_değer(boolean İzin_Ver_bildirim) {
        if (Word_değer(konum, "int") || Word_değer(konum, "boolean") || Word_değer(konum, "String") || Word_değer(konum, "char")
            || Word_değer(konum, "FileInputStream") || Word_değer(konum, "FileOutputStream")) {
            if (!İzin_Ver_bildirim) hata_değer("declaration not allowed here");
            int TÜR_değer = biçim_değer(), İsim = tanımlayıcı_değer(); gereksinim_değer('='); doğrulamak_TÜR(ifade_değer(), TÜR_değer);
            yazma_yerel(Ekle_yerel(İsim, TÜR_değer)); return;
        }
        int İsim = tanımlayıcı_değer(), yerel_Scope = BUL_yerel(İsim);
        if (almak('=')) { doğrulamak_TÜR(ifade_değer(), yerel_TÜR[yerel_Scope]); yazma_yerel(yerel_Scope); }
        else if (Tip_değer() >= 308 && Tip_değer() <= 312) {
            int kodlama_değer = Tip_değer(); konum++; 지역읽기(yerel_Scope); int sınır_değer = KOD_boyutlandırmak, BACK_değer_türü = ifade_değer();
            if (kodlama_değer == 308 && yerel_TÜR[yerel_Scope] == 3) 결합(sınır_değer, 3, BACK_değer_türü);
            else {
                doğrulamak_TÜR(yerel_TÜR[yerel_Scope], 1); doğrulamak_TÜR(BACK_değer_türü, 1);
                내보내기(kodlama_değer == 308 ? 96 : kodlama_değer == 309 ? 100 : kodlama_değer == 310 ? 104 : kodlama_değer == 311 ? 108 : 112);
                if (yerel_TÜR[yerel_Scope] == 5) 내보내기(146);
            }
            yazma_yerel(yerel_Scope);
        }
        else if (Tip_değer() == 306 || Tip_değer() == 307) {
            doğrulamak_TÜR(yerel_TÜR[yerel_Scope], 1); 내보내기(132); 내보내기(yerel_Scope); 내보내기(Tip_değer() == 306 ? 1 : 255); konum++;
            if (yerel_TÜR[yerel_Scope] == 5) { 지역읽기(yerel_Scope); 내보내기(146); yazma_yerel(yerel_Scope); }
        } else hata_değer("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); gereksinim_değer('.'); 말요구("out"); gereksinim_değer('.');
        boolean 줄바꿈 = AL_Word("println"); if (!줄바꿈) 말요구("print"); gereksinim_değer('(');
        komut(178, dış_Başvuru(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean boş_bağımsız_değişken = Tip_değer() == ')';
        int TÜR_değer = boş_bağımsız_değişken ? 0 : ifade_değer(); gereksinim_değer(')'); gereksinim_değer(';');
        String 서술 = TÜR_değer == 0 ? "()V" : TÜR_değer == 1 ? "(I)V" : TÜR_değer == 2 ? "(Z)V" : TÜR_değer == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TÜR_değer == 4 || TÜR_değer >= 6 || TÜR_değer == 0 && (!줄바꿈 || !boş_bağımsız_değişken)) hata_değer("unsupported print argument");
        komut(182, dış_Başvuru(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean deyim_değer() {
        if (hata) return false;
        if (깊이 > 32) { hata_değer("statement nesting too deep"); return false; }
        if (almak('{')) {
            깊이++; boolean İade_KR = false;
            while (!hata && Tip_değer() != '}') { if (İade_KR) hata_değer("unreachable statement"); İade_KR = deyim_değer(); }
            gereksinim_değer('}'); for (int 수 = 0; 수 < yerel_BAĞ_DEĞ_SAY; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return İade_KR;
        }
        if (almak(';')) return false;
        if (AL_Word("return")) {
            int TÜR_değer = Tip_değer() == ';' ? 0 : ifade_değer(); doğrulamak_TÜR(TÜR_değer, metot_İade[geçerli_metot]); gereksinim_değer(';');
            내보내기(TÜR_değer == 0 ? 177 : TÜR_değer <= 2 || TÜR_değer == 5 ? 172 : 176); return true;
        }
        if (AL_Word("if")) {
            gereksinim_değer('('); doğrulamak_TÜR(ifade_değer(), 2); gereksinim_değer(')'); int YANLIŞ_değer = dal(153);
            깊이++; boolean 가 = denetim_deyim(); 깊이--;
            if (AL_Word("else")) { int 끝 = dal(167); köprü_değer(YANLIŞ_değer, KOD_boyutlandırmak); 깊이++; boolean SANİYE_işlenen = denetim_deyim(); 깊이--; köprü_değer(끝, KOD_boyutlandırmak); return 가 && SANİYE_işlenen; }
            köprü_değer(YANLIŞ_değer, KOD_boyutlandırmak); return false;
        }
        if (AL_Word("while")) {
            int çalıştır = KOD_boyutlandırmak; gereksinim_değer('('); doğrulamak_TÜR(ifade_değer(), 2); gereksinim_değer(')'); int 끝 = dal(153);
            깊이++; denetim_deyim(); 깊이--; köprü_değer(dal(167), çalıştır); köprü_değer(끝, KOD_boyutlandırmak); return false;
        }
        if (AL_Word("for")) {
            깊이++; gereksinim_değer('('); if (Tip_değer() != ';') ödev_değer(true); gereksinim_değer(';');
            int koşul = KOD_boyutlandırmak; if (Tip_değer() == ';') 내보내기(4); else doğrulamak_TÜR(ifade_değer(), 2); gereksinim_değer(';');
            int 끝 = dal(153), gövde_metni = dal(167), yenilemek = KOD_boyutlandırmak;
            if (Tip_değer() != ')') ödev_değer(false); gereksinim_değer(')'); köprü_değer(dal(167), koşul); köprü_değer(gövde_metni, KOD_boyutlandırmak);
            denetim_deyim(); köprü_değer(dal(167), yenilemek); köprü_değer(끝, KOD_boyutlandırmak);
            for (int 수 = 0; 수 < yerel_BAĞ_DEĞ_SAY; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Word_değer(konum, "System")) { 화면출력(); return false; }
        if (Tip_değer() == 256 && konum + 1 < belirteç_BAĞ_DEĞ_SAY && (belirteç_Tip[konum + 1] == '(' || belirteç_Tip[konum + 1] == '.')) {
            int TÜR_değer = ifade_değer(); if (TÜR_değer != 0) 내보내기(87); gereksinim_değer(';'); return false;
        }
        ödev_değer(true); gereksinim_değer(';'); return false;
    }
    static boolean denetim_deyim() {
        if (Word_değer(konum, "int") || Word_değer(konum, "boolean") || Word_değer(konum, "char") || Word_değer(konum, "String")
            || Word_değer(konum, "FileInputStream") || Word_değer(konum, "FileOutputStream")) hata_değer("local declaration requires braces");
        return deyim_değer();
    }
    static void 출바(int değer) { if (çıktı_boyutlandırmak == metinÇıktısı.length) hata_değer("class file too large"); else metinÇıktısı[çıktı_boyutlandırmak++] = değer & 255; }
    static void 출짧(int değer) { 출바(değer >> 8); 출바(değer); }
    static void 출정(int değer) { 출짧(değer >>> 16); 출짧(değer); }
    static void yazma_Sınıf() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(sabit_BAĞ_DEĞ_SAY);
        for (int 수 = 0; 수 < sabit_boyutlandırmak; 수++) 출바(sabit_değer[수]);
        출짧(0x21); 출짧(Sınıf_sabit); 출짧(ana_sabit); 출짧(0); 출짧(0); 출짧(metot_BAĞ_DEĞ_SAY);
        for (int 수 = 0; 수 < metot_BAĞ_DEĞ_SAY; 수++) {
            출짧(metot_erişim[수]); 출짧(metot_ad_sabit[수]); 출짧(metot_tanımlayıcı_sabit[수]); 출짧(1); 출짧(KOD_sabit);
            출정(12 + metot_süre[수]); 출짧(128); 출짧(함수지역[수]); 출정(metot_süre[수]);
            for (int yuva_girdi = 0; yuva_girdi < metot_süre[수]; yuva_girdi++) 출바(KOD_değer[metot_KOD[수] + yuva_girdi]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int çalıştır() {
        if (kullanıcı_alanı.인수개수() == 1 && 자바도구.같음(kullanıcı_alanı.bağımsız_değişkenler(0), "-version")) {
            kullanıcı_alanı.Yazma("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (kullanıcı_alanı.인수개수() != 1) { kullanıcı_alanı.Yazma("Usage: javac FILE.java\n"); return 2; }
        int ad_boyutlandırmak = 자바도구.İsim(dosya_adı_SMS, kullanıcı_alanı.bağımsız_değişkenler(0));
        if (ad_boyutlandırmak < 6 || ad_boyutlandırmak > 62 || dosya_adı_SMS[ad_boyutlandırmak - 5] != '.' || dosya_adı_SMS[ad_boyutlandırmak - 4] != 'j'
            || dosya_adı_SMS[ad_boyutlandırmak - 3] != 'a' || dosya_adı_SMS[ad_boyutlandırmak - 2] != 'v' || dosya_adı_SMS[ad_boyutlandırmak - 1] != 'a') {
            kullanıcı_alanı.Yazma("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        kaynak_boyutlandırmak = kullanıcı_alanı.파일읽기(dosya_adı_SMS, kaynakKod);
        if (kaynak_boyutlandırmak < 0) { kullanıcı_alanı.Yazma("javac: cannot read source: "); 자바도구.수쓰기(kaynak_boyutlandırmak); kullanıcı_alanı.yazma_karakter_değer(10); return 1; }
        kaynak_boyutlandırmak = 자바도구.원문해독(kaynakKod, kaynak_boyutlandırmak);
        if (kaynak_boyutlandırmak < 0) { kullanıcı_alanı.Yazma("javac error: invalid UTF-8 source\n"); return 1; }
        kesmek_değer(); if (!hata) 선언읽기();
        if (!hata) {
            if (belirteç_süre[Sınıf_belirteç] != ad_boyutlandırmak - 5) hata_değer("class name must match file name");
            for (int 수 = 0; 수 < ad_boyutlandırmak - 5; 수++) if (kaynakKod[belirteç_konum[Sınıf_belirteç] + 수] != dosya_adı_SMS[수]) hata_değer("class name must match file name");
        }
        for (geçerli_metot = 0; geçerli_metot < metot_BAĞ_DEĞ_SAY && !hata; geçerli_metot++) {
            konum = metot_gövdesi[geçerli_metot]; metot_KOD[geçerli_metot] = KOD_boyutlandırmak; yerel_BAĞ_DEĞ_SAY = 0; 깊이 = 0;
            for (int 수 = 0; 수 < metot_bağımsız_değişken_BAĞ_DEĞ_SAY[geçerli_metot]; 수++) Ekle_yerel(metot_bağımsız_değişken_ad[geçerli_metot * 16 + 수], metot_bağımsız_değişken_TÜR[geçerli_metot * 16 + 수]);
            boolean İade_KR = deyim_değer();
            if (!İade_KR && metot_İade[geçerli_metot] != 0) hata_değer("missing return");
            // dal 뒤의 합류 지점은 반드시 fiili_veri 명령이어야 한다 (버전 49 검증기).
            if (metot_İade[geçerli_metot] == 0) 내보내기(177);
            else { boolean bilgi = metot_İade[geçerli_metot] <= 2 || metot_İade[geçerli_metot] == 5; 내보내기(bilgi ? 3 : 1); 내보내기(bilgi ? 172 : 176); }
            if (konum != metot_Bitiş[geçerli_metot]) hata_değer("invalid method body");
            함수지역[geçerli_metot] = yerel_BAĞ_DEĞ_SAY; metot_süre[geçerli_metot] = KOD_boyutlandırmak - metot_KOD[geçerli_metot];
        }
        if (hata) return 1;
        yazma_Sınıf(); if (hata) return 1;
        dosya_adı_SMS[ad_boyutlandırmak - 4] = 'c'; dosya_adı_SMS[ad_boyutlandırmak - 3] = 'l'; dosya_adı_SMS[ad_boyutlandırmak - 2] = 'a';
        dosya_adı_SMS[ad_boyutlandırmak - 1] = 's'; dosya_adı_SMS[ad_boyutlandırmak] = 's'; dosya_adı_SMS[ad_boyutlandırmak + 1] = 0;
        int sonuç = kullanıcı_alanı.yazma_Dosya(dosya_adı_SMS, metinÇıktısı, çıktı_boyutlandırmak);
        if (sonuç < 0) { kullanıcı_alanı.Yazma("javac: cannot save class: "); 자바도구.수쓰기(sonuç); kullanıcı_alanı.yazma_karakter_değer(10); return 1; }
        kullanıcı_alanı.Yazma("Compiled: "); for (int 수 = 0; dosya_adı_SMS[수] != 0; 수++) kullanıcı_alanı.yazma_karakter_değer(dosya_adı_SMS[수]);
        kullanıcı_alanı.Yazma(" (JVM class version 49)\n"); return 0;
    }
}
