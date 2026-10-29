// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class veri_iletişim {
    static int rakam_değer(String metin) {
        if (metin == null || metin.length() == 0) return -1;
        int sonuç = 0;
        for (int Dizin = 0; Dizin < metin.length(); Dizin++) {
            int değer = metin.charAt(Dizin) - '0';
            if (değer < 0 || değer > 9 || sonuç > 6553) return -1;
            sonuç = sonuç * 10 + değer;
            if (sonuç > 65535) return -1;
        }
        return sonuç;
    }
    static int ADRES(String metin) {
        if (metin == null) return 0;
        int değer = 0, sonuç = 0, 부분 = 0, 자릿수 = 0;
        for (int Dizin = 0; Dizin <= metin.length(); Dizin++) {
            int 문자 = Dizin == metin.length() ? '.' : metin.charAt(Dizin);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                sonuç = (sonuç << 8) | değer; 부분++; değer = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                değer = değer * 10 + 문자 - '0';
                if (++자릿수 > 3 || değer > 255) return 0;
            }
        }
        return 부분 == 4 ? sonuç : 0;
    }
    public static int çalıştır() {
        if (kullanıcı_alanı.인수개수() != 3) { kullanıcı_alanı.Yazma("Usage: run udp IP PORT TEXT\n"); return 2; }
        int ADRES = ADRES(kullanıcı_alanı.bağımsız_değişkenler(0)), taşımak_değer = rakam_değer(kullanıcı_alanı.bağımsız_değişkenler(1));
        String içerik_değer = kullanıcı_alanı.bağımsız_değişkenler(2);
        if (ADRES == 0 || taşımak_değer < 1 || içerik_değer.length() > 1024) { kullanıcı_alanı.Yazma("Bad destination\n"); return 2; }
        int sap_değer = kullanıcı_alanı.açık_ağ(0);
        if (sap_değer < 0) { kullanıcı_alanı.Yazma("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] veri = new int[1024];
        for (int Dizin = 0; Dizin < içerik_değer.length(); Dizin++) veri[Dizin] = içerik_değer.charAt(Dizin);
        if (kullanıcı_alanı.göndermek_veri(sap_değer, ADRES, taşımak_değer, veri, içerik_değer.length()) < 0) {
            kullanıcı_alanı.Yazma("UDP SEND FAILED\n"); kullanıcı_alanı.Kapat_ağ(sap_değer); return 4;
        }
        kullanıcı_alanı.Yazma("UDP SENT\n");
        int GETİRİ_süre = kullanıcı_alanı.almak_veri(sap_değer, veri, 1500);
        boolean 같음 = GETİRİ_süre == içerik_değer.length() && kullanıcı_alanı.보낸주소(sap_değer) == ADRES && kullanıcı_alanı.보낸창구(sap_değer) == taşımak_değer;
        if (같음) for (int Dizin = 0; Dizin < GETİRİ_süre; Dizin++) if (veri[Dizin] != içerik_değer.charAt(Dizin)) 같음 = false;
        kullanıcı_alanı.Kapat_ağ(sap_değer);
        if (GETİRİ_süre < 0) { kullanıcı_alanı.Yazma("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        kullanıcı_alanı.Yazma(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
