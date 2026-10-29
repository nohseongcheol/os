// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM dosya 64개, 파일당 16384바이트, tanımlayıcı_girdi 16개. 모든 veri/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. Negatif_değer 반환은 hata 번호다.
 */
public final class BellekDosyaları {
    static final int Dosya_BAĞ_DEĞ_SAY = 64;
    static int[] İsim = new int[Dosya_BAĞ_DEĞ_SAY * 64];
    static int[] 이름길이 = new int[Dosya_BAĞ_DEĞ_SAY];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] içerik_değer = new int[Dosya_BAĞ_DEĞ_SAY * 4096];
    static int[] süre_değer = new int[Dosya_BAĞ_DEĞ_SAY];
    static int[] Başvuru_BAĞ_DEĞ_SAY = new int[Dosya_BAĞ_DEĞ_SAY];
    static int[] kullanmak_değer = new int[16];
    static int[] hedef = new int[16];
    static int[] konum = new int[16];
    static int[] metot_mod = new int[16];
    static int[] yol = new int[64];
    static int yol_süre;

    public static int 파일한도() { return Dosya_BAĞ_DEĞ_SAY; }
    static int 자료읽기(int dosya, int konum_dizini) { return (içerik_değer[dosya * 4096 + konum_dizini / 4] >>> ((konum_dizini & 3) * 8)) & 255; }
    static void yazma_veri(int dosya, int konum_dizini, int değer) {
        int yuva_girdi = dosya * 4096 + konum_dizini / 4, taşımak_değer_83b651b8 = (konum_dizini & 3) * 8;
        içerik_değer[yuva_girdi] = (içerik_değer[yuva_girdi] & ~(255 << taşımak_değer_83b651b8)) | ((değer & 255) << taşımak_değer_83b651b8);
    }

    public static int yol_Start(int Boyut) {
        yol_süre = 0;
        if (Boyut < 1 || Boyut > 63) return -36;
        yol_süre = Boyut;
        for (int Loop_Dizin = 0; Loop_Dizin < Boyut; Loop_Dizin++) yol[Loop_Dizin] = 0;
        return 0;
    }
    public static int yol_bayt(int Dizin, int değer) {
        if (Dizin < 0 || Dizin >= yol_süre || değer < 1 || değer > 255) return -22;
        yol[Dizin] = değer; return 0;
    }
    static int BUL_girdi() {
        for (int Dosya_Dizin = 0; Dosya_Dizin < Dosya_BAĞ_DEĞ_SAY; Dosya_Dizin++) if (이름길이[Dosya_Dizin] > 0 && 이름길이[Dosya_Dizin] == Canonical_süre && 접두(İsim, Dosya_Dizin * 64, 이름길이[Dosya_Dizin], Canonical_değer, Canonical_süre)) return Dosya_Dizin;
        return -1;
    }
    public static int Aç(int 플래그) {
        if (yol_süre == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_Dizin = 0; Loop_Dizin < yol_süre; Loop_Dizin++) if (yol[Loop_Dizin] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int sonuç = normalleştirmek_değer(); if (sonuç < 0) return sonuç;
        if (BUL_dizin(Canonical_süre) >= 0) return -21;
        sonuç = çek_ana(); if (sonuç < 0) return sonuç;
        int dosya = BUL_girdi();
        if (dosya >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (dosya < 0 && (플래그 & 0x40) == 0) return -2;
        int tanımlayıcı_girdi = -1;
        for (int Loop_Dizin = 0; Loop_Dizin < 16; Loop_Dizin++) if (kullanmak_değer[Loop_Dizin] == 0) { tanımlayıcı_girdi = Loop_Dizin; break; }
        if (tanımlayıcı_girdi < 0) return -24;
        if (dosya < 0) {
            for (int Loop_Dizin = 0; Loop_Dizin < Dosya_BAĞ_DEĞ_SAY; Loop_Dizin++) if (이름길이[Loop_Dizin] == 0 && Başvuru_BAĞ_DEĞ_SAY[Loop_Dizin] == 0) { dosya = Loop_Dizin; break; }
            if (dosya < 0) return -28;
            이름길이[dosya] = Canonical_süre;
            for (int Loop_Dizin = 0; Loop_Dizin < Canonical_süre; Loop_Dizin++) İsim[dosya * 64 + Loop_Dizin] = Canonical_değer[Loop_Dizin];
            süre_değer[dosya] = 0;
        }
        if ((플래그 & 0x200) != 0) süre_değer[dosya] = 0;
        kullanmak_değer[tanımlayıcı_girdi] = 1; hedef[tanımlayıcı_girdi] = dosya; konum[tanımlayıcı_girdi] = 0; metot_mod[tanımlayıcı_girdi] = 플래그;
        Başvuru_BAĞ_DEĞ_SAY[dosya]++;
        return tanımlayıcı_girdi + 3;
    }
    static int doğrulamak(int tanımlayıcı_girdi) {
        return tanımlayıcı_girdi >= 3 && tanımlayıcı_girdi < 19 && kullanmak_değer[tanımlayıcı_girdi - 3] != 0 ? tanımlayıcı_girdi - 3 : -1;
    }
    public static int Okuma(int tanımlayıcı_girdi) {
        int yuva_girdi = doğrulamak(tanımlayıcı_girdi);
        if (yuva_girdi < 0 || (metot_mod[yuva_girdi] & 3) == 1) return -9;
        int dosya = hedef[yuva_girdi];
        if (konum[yuva_girdi] >= süre_değer[dosya]) return 256; // EOF와 fiili_veri 0x00..0xff 구별
        return 자료읽기(dosya, konum[yuva_girdi]++);
    }
    public static int Yazma(int tanımlayıcı_girdi, int değer) {
        int yuva_girdi = doğrulamak(tanımlayıcı_girdi);
        if (yuva_girdi < 0 || (metot_mod[yuva_girdi] & 3) == 0) return -9;
        int dosya = hedef[yuva_girdi];
        if ((metot_mod[yuva_girdi] & 0x400) != 0) konum[yuva_girdi] = süre_değer[dosya];
        if (konum[yuva_girdi] >= 16384) return -28;
        while (süre_değer[dosya] < konum[yuva_girdi]) yazma_veri(dosya, süre_değer[dosya]++, 0);
        yazma_veri(dosya, konum[yuva_girdi]++, değer);
        if (süre_değer[dosya] < konum[yuva_girdi]) süre_değer[dosya] = konum[yuva_girdi];
        return 1;
    }
    public static int arama_konum(int tanımlayıcı_girdi, int 거리, int işlem_kök) {
        int yuva_girdi = doğrulamak(tanımlayıcı_girdi);
        if (yuva_girdi < 0) return -9;
        if (işlem_kök < 0 || işlem_kök > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (işlem_kök == 0 ? 0 : işlem_kök == 1 ? konum[yuva_girdi] : süre_değer[hedef[yuva_girdi]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        konum[yuva_girdi] = 새위치; return 새위치;
    }
    public static int Kapat(int tanımlayıcı_girdi) {
        int yuva_girdi = doğrulamak(tanımlayıcı_girdi);
        if (yuva_girdi < 0) return -9;
        Başvuru_BAĞ_DEĞ_SAY[hedef[yuva_girdi]]--; kullanmak_değer[yuva_girdi] = 0; return 0;
    }
    public static int Boyut(int tanımlayıcı_girdi) {
        int yuva_girdi = doğrulamak(tanımlayıcı_girdi); return yuva_girdi < 0 ? -9 : süre_değer[hedef[yuva_girdi]];
    }
    public static int küme_süre(int tanımlayıcı_girdi, int Boyut) {
        int yuva_girdi = doğrulamak(tanımlayıcı_girdi);
        if (yuva_girdi < 0 || (metot_mod[yuva_girdi] & 3) == 0) return -9;
        if (Boyut < 0 || Boyut > 16384) return -22;
        int dosya = hedef[yuva_girdi];
        while (süre_değer[dosya] < Boyut) yazma_veri(dosya, süre_değer[dosya]++, 0);
        süre_değer[dosya] = Boyut; return 0;
    }
    public static int silmek_girdi() {
        if (yol_süre == 0) return -22;
        int sonuç = normalleştirmek_değer(); if (sonuç < 0) return sonuç;
        if (BUL_dizin(Canonical_süre) >= 0) return -21;
        sonuç = çek_ana(); if (sonuç < 0) return sonuç;
        int dosya = BUL_girdi();
        if (dosya < 0) return -2;
        이름길이[dosya] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void girdi_Liste() {
        yol_Start(1); yol_bayt(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int Dizin) {
        if (Dizin < 0 || Dizin >= Dosya_BAĞ_DEĞ_SAY || 이름길이[Dizin] == 0) return 0;
        for (int Loop_Dizin = 0; Loop_Dizin < 이름길이[Dizin]; Loop_Dizin++) if (İsim[Dizin * 64 + Loop_Dizin] == '/') return 0;
        return 이름길이[Dizin];
    }
    public static int 공개이름바이트(int Dizin, int konum_dizini) {
        return Dizin >= 0 && Dizin < Dosya_BAĞ_DEĞ_SAY && konum_dizini >= 0 && konum_dizini < 이름길이[Dizin] ? İsim[Dizin * 64 + konum_dizini] : -22;
    }
    public static int 공개파일크기(int Dizin) { return Dizin >= 0 && Dizin < Dosya_BAĞ_DEĞ_SAY ? süre_değer[Dizin] : -22; }
    static int[] Canonical_değer = new int[64], geçerli_öğe = new int[64], dizin_ad = new int[16 * 64], dizin_süre = new int[16];
    static int Canonical_süre, geçerli_süre_6ac7278b;
    static boolean 접두(int[] 이름들, int çalıştır, int yol_değer, int[] ön_kamera_değer, int satır_aralığı_yol) {
        if (yol_değer < satır_aralığı_yol) return false;
        for (int Loop_Dizin = 0; Loop_Dizin < satır_aralığı_yol; Loop_Dizin++) if (이름들[çalıştır + Loop_Dizin] != ön_kamera_değer[Loop_Dizin]) return false;
        return true;
    }
    static int normalleştirmek_değer() {
        if (yol_süre == 0) return -22;
        Canonical_süre = yol[0] == '/' ? 0 : geçerli_süre_6ac7278b;
        for (int Loop_Dizin = 0; Loop_Dizin < Canonical_süre; Loop_Dizin++) Canonical_değer[Loop_Dizin] = geçerli_öğe[Loop_Dizin];
        int 읽는자리 = 0;
        while (읽는자리 < yol_süre) {
            while (읽는자리 < yol_süre && yol[읽는자리] == '/') 읽는자리++;
            int Start_konum = 읽는자리; while (읽는자리 < yol_süre && yol[읽는자리] != '/') { if (yol[읽는자리] == 0) return -22; 읽는자리++; }
            int girdi_BAĞ_DEĞ_SAY = 읽는자리 - Start_konum; if (girdi_BAĞ_DEĞ_SAY == 0 || girdi_BAĞ_DEĞ_SAY == 1 && yol[Start_konum] == '.') continue;
            if (girdi_BAĞ_DEĞ_SAY == 2 && yol[Start_konum] == '.' && yol[Start_konum + 1] == '.') {
                while (Canonical_süre > 0 && Canonical_değer[Canonical_süre - 1] != '/') Canonical_süre--;
                if (Canonical_süre > 0) Canonical_süre--;
                continue;
            }
            if (Canonical_süre + girdi_BAĞ_DEĞ_SAY + (Canonical_süre == 0 ? 0 : 1) > 63) return -36;
            if (Canonical_süre > 0) Canonical_değer[Canonical_süre++] = '/';
            for (int Loop_Dizin = Start_konum; Loop_Dizin < 읽는자리; Loop_Dizin++) Canonical_değer[Canonical_süre++] = yol[Loop_Dizin];
        }
        return 0;
    }
    static int BUL_dizin(int girdi_BAĞ_DEĞ_SAY) {
        if (girdi_BAĞ_DEĞ_SAY == 0) return 0;
        for (int Loop_Dizin = 1; Loop_Dizin < 16; Loop_Dizin++) if (dizin_süre[Loop_Dizin] == girdi_BAĞ_DEĞ_SAY && 접두(dizin_ad, Loop_Dizin * 64, girdi_BAĞ_DEĞ_SAY, Canonical_değer, girdi_BAĞ_DEĞ_SAY)) return Loop_Dizin;
        return -1;
    }
    static int çek_ana() {
        int girdi_BAĞ_DEĞ_SAY = Canonical_süre; while (girdi_BAĞ_DEĞ_SAY > 0 && Canonical_değer[girdi_BAĞ_DEĞ_SAY - 1] != '/') girdi_BAĞ_DEĞ_SAY--;
        return BUL_dizin(girdi_BAĞ_DEĞ_SAY == 0 ? 0 : girdi_BAĞ_DEĞ_SAY - 1) < 0 ? -2 : 0;
    }
    public static int açmak_dizin() {
        int 처리값 = normalleştirmek_değer(); if (처리값 < 0) return 처리값;
        if (BUL_dizin(Canonical_süre) >= 0 || BUL_girdi() >= 0) return -17;
        처리값 = çek_ana(); if (처리값 < 0) return 처리값;
        for (int Loop_Dizin = 1; Loop_Dizin < 16; Loop_Dizin++) if (dizin_süre[Loop_Dizin] == 0) {
            dizin_süre[Loop_Dizin] = Canonical_süre; for (int iç_konum = 0; iç_konum < Canonical_süre; iç_konum++) dizin_ad[Loop_Dizin * 64 + iç_konum] = Canonical_değer[iç_konum]; return 0;
        }
        return -28;
    }
    public static int girdi_Tip() {
        int 처리값 = normalleştirmek_değer(); if (처리값 < 0) return 처리값;
        if (BUL_dizin(Canonical_süre) >= 0) return 2;
        return BUL_girdi() >= 0 ? 1 : 0;
    }
    public static int değiştirmek_dizin() {
        int 처리값 = normalleştirmek_değer(); if (처리값 < 0) return 처리값;
        if (BUL_dizin(Canonical_süre) < 0) return -2;
        geçerli_süre_6ac7278b = Canonical_süre; for (int Loop_Dizin = 0; Loop_Dizin < geçerli_süre_6ac7278b; Loop_Dizin++) geçerli_öğe[Loop_Dizin] = Canonical_değer[Loop_Dizin]; return 0;
    }
    public static int kaldırmak_dizin() {
        int 처리값 = normalleştirmek_değer(); if (처리값 < 0) return 처리값;
        int 폴더번호 = BUL_dizin(Canonical_süre); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (geçerli_süre_6ac7278b == Canonical_süre && 접두(geçerli_öğe, 0, geçerli_süre_6ac7278b, Canonical_değer, Canonical_süre)) return -16;
        for (int Loop_Dizin = 0; Loop_Dizin < Dosya_BAĞ_DEĞ_SAY; Loop_Dizin++) {
            if (이름길이[Loop_Dizin] > Canonical_süre && 접두(İsim, Loop_Dizin * 64, 이름길이[Loop_Dizin], Canonical_değer, Canonical_süre) && İsim[Loop_Dizin * 64 + Canonical_süre] == '/') return -39;
        }
        for (int Loop_Dizin = 0; Loop_Dizin < 16; Loop_Dizin++) {
            if (dizin_süre[Loop_Dizin] > Canonical_süre && 접두(dizin_ad, Loop_Dizin * 64, dizin_süre[Loop_Dizin], Canonical_değer, Canonical_süre) && dizin_ad[Loop_Dizin * 64 + Canonical_süre] == '/') return -39;
        }
        dizin_süre[폴더번호] = 0; return 0;
    }
    public static int Yeniden_Adlandır_girdi(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= Dosya_BAĞ_DEĞ_SAY || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normalleştirmek_değer(); if (처리값 < 0) return 처리값;
        if (BUL_dizin(Canonical_süre) >= 0) return -21;
        처리값 = çek_ana(); if (처리값 < 0) return 처리값;
        int Önceki_değer = BUL_girdi(); if (Önceki_değer == 원본번호) return 0;
        if (Önceki_değer >= 0) 이름길이[Önceki_değer] = 0;
        이름길이[원본번호] = Canonical_süre; for (int Loop_Dizin = 0; Loop_Dizin < Canonical_süre; Loop_Dizin++) İsim[원본번호 * 64 + Loop_Dizin] = Canonical_değer[Loop_Dizin]; return 0;
    }
    static int girdi_Start(int[] veri_DİZİ, int 시작점, int girdi_BAĞ_DEĞ_SAY) {
        if (!접두(veri_DİZİ, 시작점, girdi_BAĞ_DEĞ_SAY, Canonical_değer, Canonical_süre)) return -1;
        int Start_konum = Canonical_süre;
        if (Start_konum > 0) { if (girdi_BAĞ_DEĞ_SAY <= Start_konum || veri_DİZİ[시작점 + Start_konum] != '/') return -1; Start_konum++; }
        if (girdi_BAĞ_DEĞ_SAY <= Start_konum) return -1;
        for (int Loop_Dizin = Start_konum; Loop_Dizin < girdi_BAĞ_DEĞ_SAY; Loop_Dizin++) if (veri_DİZİ[시작점 + Loop_Dizin] == '/') return -1;
        return Start_konum;
    }
    static void geçerli_yazma() { 단말.문자('/'); for (int Loop_Dizin = 0; Loop_Dizin < geçerli_süre_6ac7278b; Loop_Dizin++) Pano.직렬쓰기(geçerli_öğe[Loop_Dizin]); }
    static int 경로목록() {
        int 처리값 = normalleştirmek_değer(); if (처리값 < 0) return 처리값;
        int Dosya_hedef = BUL_girdi();
        if (Dosya_hedef >= 0) { for (int Loop_Dizin = 0; Loop_Dizin < Canonical_süre; Loop_Dizin++) Pano.직렬쓰기(Canonical_değer[Loop_Dizin]); 단말.Yazma("  "); 단말.수(süre_değer[Dosya_hedef]); 단말.Yazma("bayt_değer(주기억 dosya)\n"); return 0; }
        if (BUL_dizin(Canonical_süre) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (dizin_süre[뒷값] > 0) {
            int Start_konum = girdi_Start(dizin_ad, 뒷값 * 64, dizin_süre[뒷값]); if (Start_konum < 0) continue;
            for (int Loop_Dizin = Start_konum; Loop_Dizin < dizin_süre[뒷값]; Loop_Dizin++) Pano.직렬쓰기(dizin_ad[뒷값 * 64 + Loop_Dizin]); 단말.Yazma("/\n");
        }
        for (int Dosya_Dizin = 0; Dosya_Dizin < Dosya_BAĞ_DEĞ_SAY; Dosya_Dizin++) if (이름길이[Dosya_Dizin] > 0) {
            int Start_konum = girdi_Start(İsim, Dosya_Dizin * 64, 이름길이[Dosya_Dizin]); if (Start_konum < 0) continue;
            for (int Loop_Dizin = Start_konum; Loop_Dizin < 이름길이[Dosya_Dizin]; Loop_Dizin++) Pano.직렬쓰기(İsim[Dosya_Dizin * 64 + Loop_Dizin]);
            단말.Yazma("  "); 단말.수(süre_değer[Dosya_Dizin]); 단말.Yazma("bayt_değer(주기억 dosya)\n");
        }
        return 0;
    }
}
