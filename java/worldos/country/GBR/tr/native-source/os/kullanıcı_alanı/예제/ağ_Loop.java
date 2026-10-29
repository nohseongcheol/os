// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Boyut/홀수 süre_değer 데이터그램으로 fiili_veri RTL8139 almak_değer Loop_değer 순환을 시험한다. */
public final class ağ_Loop {
    public static int çalıştır() {
        if (kullanıcı_alanı.인수개수() != 1) { kullanıcı_alanı.Yazma("Usage: run stress PORT\n"); return 2; }
        String metin = kullanıcı_alanı.bağımsız_değişkenler(0);
        int taşımak_değer = 0;
        for (int Dizin = 0; Dizin < metin.length(); Dizin++) {
            if (metin.charAt(Dizin) < '0' || metin.charAt(Dizin) > '9' || taşımak_değer > 6553) return 2;
            taşımak_değer = taşımak_değer * 10 + metin.charAt(Dizin) - '0';
        }
        if (taşımak_değer < 1 || taşımak_değer > 65535) return 2;
        int sap_değer = kullanıcı_alanı.açık_ağ(0);
        if (sap_değer < 0) return 3;
        int[] veri = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int süre_değer = 1024 - (회차 & 1);
            for (int Dizin = 0; Dizin < süre_değer; Dizin++) veri[Dizin] = (Dizin + 회차) & 255;
            if (kullanıcı_alanı.göndermek_veri(sap_değer, 0x0a000202, taşımak_değer, veri, süre_değer) != süre_değer) return 4;
            if (kullanıcı_alanı.almak_veri(sap_değer, veri, 300) != süre_değer) return 5;
            for (int Dizin = 0; Dizin < süre_değer; Dizin++) if (veri[Dizin] != ((Dizin + 회차) & 255)) return 6;
        }
        kullanıcı_alanı.Kapat_ağ(sap_değer);
        kullanıcı_alanı.Yazma("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
