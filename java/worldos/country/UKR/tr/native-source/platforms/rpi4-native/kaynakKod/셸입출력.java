// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] artış_veri = new int[16384], çıktı_veri = new int[16384];
    static int artış_süre, artış_konum, çıktı_süre, giriş_dosyası = -1, çıkış_dosyası = -1;
    static boolean kanal_artış, kanal_çıktı;
    static int hata_değer;
    static boolean İzin_Ver_devralmak = true;
    public static int bilgi_teknolojisi_devralmak() { return İzin_Ver_devralmak && giriş_dosyası < 3 && çıkış_dosyası < 3 && !kanal_artış && !kanal_çıktı ? 1 : 0; }
    public static int metinÇıktısı(int Kanal_değer, int değer) {
        if (Kanal_değer != 1) return 0;
        if (çıkış_dosyası >= 3) { int 처리값 = BellekDosyaları.Yazma(çıkış_dosyası, değer); if (처리값 < 0) hata_değer = 처리값; return 1; }
        if (!kanal_çıktı) return 0;
        if (çıktı_süre == çıktı_veri.length) hata_değer = -28;
        else çıktı_veri[çıktı_süre++] = değer;
        return 1;
    }
    public static int artış_değer() {
        if (giriş_dosyası >= 3) { int 처리값 = BellekDosyaları.Okuma(giriş_dosyası); return 처리값 == 256 ? -2 : 처리값; }
        if (kanal_artış) return artış_konum < artış_süre ? artış_veri[artış_konum++] : -2;
        return -3; // UART로 İleri_değer
    }
    static void çalıştır(boolean satır_aralığı_kanal, boolean 뒤파이프) {
        kanal_artış = satır_aralığı_kanal; kanal_çıktı = 뒤파이프;
        artış_konum = 0; çıktı_süre = 0; giriş_dosyası = -1; çıkış_dosyası = -1; hata_değer = 0;
    }
    static void 끝() {
        Pano.입출력전환(0);
        if (giriş_dosyası >= 3) BellekDosyaları.Kapat(giriş_dosyası);
        if (çıkış_dosyası >= 3) BellekDosyaları.Kapat(çıkış_dosyası);
        if (kanal_çıktı) { artış_süre = çıktı_süre; for (int Loop_Dizin = 0; Loop_Dizin < çıktı_süre; Loop_Dizin++) artış_veri[Loop_Dizin] = çıktı_veri[Loop_Dizin]; }
        giriş_dosyası = -1; çıkış_dosyası = -1; kanal_artış = false; kanal_çıktı = false;
    }
}
