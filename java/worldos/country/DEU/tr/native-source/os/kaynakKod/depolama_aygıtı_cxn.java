// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 bölüm_değer_366e0bfa. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class depolama_aygıtı_cxn {
    static boolean bilgi_teknolojisi_Aktif_9e72441a = false;
    static int[] bölüm_veri = new int[512];
    static void 잠깐기다리기() {
        for (int Dizin = 0; Dizin < 4; Dizin++) cihaz_değer.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int çalıştır = cihaz_değer.밀리초();
        while (cihaz_değer.밀리초() - çalıştır < 500) {
            int Durum_değer = cihaz_değer.입출력바이트읽기(0x1f7);
            if (Durum_değer == 0 || Durum_değer == 255) return -19;
            if ((Durum_değer & 128) == 0) {
                if ((Durum_değer & 33) != 0) return -5;
                if (!자료필요 || (Durum_değer & 8) != 0) return 0;
            }
            cihaz_değer.잠시양보();
        }
        return -110;
    }
    static int istek(int bölüm_değer_366e0bfa, int komut) {
        if (bölüm_değer_366e0bfa < 0 || bölüm_değer_366e0bfa >= 2048) return -22;
        cihaz_değer.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ kullanmak_değer 안 함
        cihaz_değer.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int sonuç = 준비기다리기(false);
        if (sonuç < 0) return sonuç;
        cihaz_değer.입출력바이트쓰기(0x1f2, 1);
        cihaz_değer.입출력바이트쓰기(0x1f3, bölüm_değer_366e0bfa & 255);
        cihaz_değer.입출력바이트쓰기(0x1f4, (bölüm_değer_366e0bfa >>> 8) & 255);
        cihaz_değer.입출력바이트쓰기(0x1f5, 0);
        cihaz_değer.입출력바이트쓰기(0x1f7, komut); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Okuma(int bölüm_değer_366e0bfa) {
        int sonuç = istek(bölüm_değer_366e0bfa, 0x20);
        if (sonuç < 0) return sonuç;
        for (int Dizin = 0; Dizin < 256; Dizin++) {
            int değer = cihaz_değer.입출력짧은수읽기(0x1f0);
            bölüm_veri[Dizin * 2] = değer & 255; bölüm_veri[Dizin * 2 + 1] = değer >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Yazma(int bölüm_değer_366e0bfa) {
        if (!bilgi_teknolojisi_Aktif_9e72441a || bölüm_değer_366e0bfa < 1 || bölüm_değer_366e0bfa > 518) return -19;
        int sonuç = istek(bölüm_değer_366e0bfa, 0x30);
        if (sonuç < 0) return sonuç;
        for (int Dizin = 0; Dizin < 256; Dizin++)
            cihaz_değer.입출력짧은수쓰기(0x1f0, bölüm_veri[Dizin * 2] | bölüm_veri[Dizin * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int boşaltmak_çıktı() {
        if (!bilgi_teknolojisi_Aktif_9e72441a) return -19;
        cihaz_değer.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int ayrıştırmak_bilgi(int konum) {
        return bölüm_veri[konum] | bölüm_veri[konum + 1] << 8 | bölüm_veri[konum + 2] << 16 | bölüm_veri[konum + 3] << 24;
    }
    static void yazma_bilgi_değer(int konum, int değer) {
        for (int Dizin = 0; Dizin < 4; Dizin++) bölüm_veri[konum + Dizin] = (değer >>> (Dizin * 8)) & 255;
    }
}
