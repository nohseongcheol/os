// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 depo_değer biçim_değer. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] Dosya_tablo = new int[1024];
    static int 바이트해시(int değer, int veri) { return (değer ^ veri) * 16777619; }
    static void takas_veri() {
        for (int Dizin = 0; Dizin < 512; Dizin++) depolama_aygıtı_cxn.bölüm_veri[Dizin] = 0;
    }
    static int tablo_bilgi(int konum) {
        return Dosya_tablo[konum] | Dosya_tablo[konum + 1] << 8 | Dosya_tablo[konum + 2] << 16 | Dosya_tablo[konum + 3] << 24;
    }
    static void yazma_tablo_bilgi(int konum, int değer) {
        for (int Dizin = 0; Dizin < 4; Dizin++) Dosya_tablo[konum + Dizin] = (değer >>> (Dizin * 8)) & 255;
    }
    static boolean çek_tablo() {
        for (int dosya = 0; dosya < 8; dosya++) {
            int süre_değer = 0;
            for (int yuva_girdi = 0; yuva_girdi < 64; yuva_girdi++) Bellek_dosya_sistemi.İsim[yuva_girdi] = Dosya_tablo[dosya * 72 + yuva_girdi];
            while (süre_değer < 64 && Bellek_dosya_sistemi.İsim[süre_değer] != 0) süre_değer++;
            if (süre_değer == 0) continue;
            if (!Bellek_dosya_sistemi.çek_ad(Bellek_dosya_sistemi.İsim, süre_değer)
                || tablo_bilgi(dosya * 72 + 64) < 0 || tablo_bilgi(dosya * 72 + 64) > 16384) return false;
            for (int ön_kamera_değer = 0; ön_kamera_değer < dosya; ön_kamera_değer++) {
                boolean 같음 = Dosya_tablo[ön_kamera_değer * 72 + süre_değer] == 0;
                for (int yuva_girdi = 0; yuva_girdi < süre_değer; yuva_girdi++) if (Dosya_tablo[ön_kamera_değer * 72 + yuva_girdi] != Bellek_dosya_sistemi.İsim[yuva_girdi]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int Start_bölüm = 1 + 보존본 * 259;
        if (depolama_aygıtı_cxn.Okuma(Start_bölüm) < 0 || depolama_aygıtı_cxn.ayrıştırmak_bilgi(0) != 0x4a4b534e) return -1;
        int 세대 = depolama_aygıtı_cxn.ayrıştırmak_bilgi(4), sağlama_toplamı = depolama_aygıtı_cxn.ayrıştırmak_bilgi(8);
        if (세대 < 1 || depolama_aygıtı_cxn.ayrıştırmak_bilgi(12) != (세대 ^ sağlama_toplamı ^ 0x4a4b534e)) return -1;
        int özet_Dosya = 0x811c9dc5;
        for (int bölüm_değer_366e0bfa = 0; bölüm_değer_366e0bfa < 258; bölüm_değer_366e0bfa++) {
            if (depolama_aygıtı_cxn.Okuma(Start_bölüm + 1 + bölüm_değer_366e0bfa) < 0) return -1;
            for (int yuva_girdi = 0; yuva_girdi < 512; yuva_girdi++) {
                int değer = depolama_aygıtı_cxn.bölüm_veri[yuva_girdi];
                özet_Dosya = 바이트해시(özet_Dosya, değer);
                if (bölüm_değer_366e0bfa < 2) Dosya_tablo[bölüm_değer_366e0bfa * 512 + yuva_girdi] = değer;
            }
        }
        return özet_Dosya == sağlama_toplamı && çek_tablo() ? 세대 : -1;
    }
    static int kaynakYükle(int 보존본) {
        int Start_bölüm = 1 + 보존본 * 259;
        for (int bölüm_değer_366e0bfa = 0; bölüm_değer_366e0bfa < 2; bölüm_değer_366e0bfa++) {
            if (depolama_aygıtı_cxn.Okuma(Start_bölüm + 1 + bölüm_değer_366e0bfa) < 0) return -5;
            for (int yuva_girdi = 0; yuva_girdi < 512; yuva_girdi++) Dosya_tablo[bölüm_değer_366e0bfa * 512 + yuva_girdi] = depolama_aygıtı_cxn.bölüm_veri[yuva_girdi];
        }
        for (int dosya = 0; dosya < 8; dosya++) {
            for (int yuva_girdi = 0; yuva_girdi < 64; yuva_girdi++) Bellek_dosya_sistemi.이름들[dosya * 64 + yuva_girdi] = Dosya_tablo[dosya * 72 + yuva_girdi];
            Bellek_dosya_sistemi.boyutlandırmak_Liste[dosya] = Dosya_tablo[dosya * 72] == 0 ? 0 : tablo_bilgi(dosya * 72 + 64);
            Bellek_dosya_sistemi.허가들[dosya] = tablo_bilgi(dosya * 72 + 68) & 511;
            for (int bölüm_değer_366e0bfa = 0; bölüm_değer_366e0bfa < 32; bölüm_değer_366e0bfa++) {
                if (depolama_aygıtı_cxn.Okuma(Start_bölüm + 3 + dosya * 32 + bölüm_değer_366e0bfa) < 0) return -5;
                int ADRES = cihaz_değer.Dosya_Bellek() + dosya * 16384 + bölüm_değer_366e0bfa * 512;
                for (int yuva_girdi = 0; yuva_girdi < 512; yuva_girdi++) cihaz_değer.yazma_Bellek(ADRES + yuva_girdi, depolama_aygıtı_cxn.bölüm_veri[yuva_girdi]);
            }
        }
        return 0;
    }
    static void Hazırlan() {
        if (depolama_aygıtı_cxn.Okuma(0) < 0 || depolama_aygıtı_cxn.ayrıştırmak_bilgi(0) != 0x54534b4a
            || depolama_aygıtı_cxn.ayrıştırmak_bilgi(4) != 0x3145524f || depolama_aygıtı_cxn.ayrıştırmak_bilgi(8) != 2048
            || depolama_aygıtı_cxn.ayrıştırmak_bilgi(12) != 0x3153464a) {
            SMS_Terminal.Yazma("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        depolama_aygıtı_cxn.bilgi_teknolojisi_Aktif_9e72441a = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Terminal.Yazma("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (kaynakYükle(현재보존본) < 0) {
            SMS_Terminal.Yazma("STORE read failed; halted to preserve files\n"); cihaz_değer.정지();
        }
        SMS_Terminal.Yazma("STORE restored generation "); SMS_Terminal.수쓰기(세대번호); SMS_Terminal.문자(10);
    }
    static int eşitlemek() {
        if (!depolama_aygıtı_cxn.bilgi_teknolojisi_Aktif_9e72441a) return -19;
        if (세대번호 == 2147483647) return -75;
        int Sonraki_öğe = 현재보존본 == 0 ? 1 : 0, Start_bölüm = 1 + Sonraki_öğe * 259;
        // 새 본문보다 먼저 Önceki_öğe commit을 무효화하고 cihaz_değer 캐시를 비운다.
        takas_veri();
        if (depolama_aygıtı_cxn.Yazma(Start_bölüm) < 0 || depolama_aygıtı_cxn.boşaltmak_çıktı() < 0) return -5;
        for (int yuva_girdi = 0; yuva_girdi < 1024; yuva_girdi++) Dosya_tablo[yuva_girdi] = 0;
        for (int dosya = 0; dosya < 8; dosya++) if (Bellek_dosya_sistemi.이름들[dosya * 64] != 0) {
            for (int yuva_girdi = 0; yuva_girdi < 64; yuva_girdi++) Dosya_tablo[dosya * 72 + yuva_girdi] = Bellek_dosya_sistemi.이름들[dosya * 64 + yuva_girdi];
            yazma_tablo_bilgi(dosya * 72 + 64, Bellek_dosya_sistemi.boyutlandırmak_Liste[dosya]);
            yazma_tablo_bilgi(dosya * 72 + 68, Bellek_dosya_sistemi.허가들[dosya]);
        }
        int özet_Dosya = 0x811c9dc5;
        for (int bölüm_değer_366e0bfa = 0; bölüm_değer_366e0bfa < 258; bölüm_değer_366e0bfa++) {
            for (int yuva_girdi = 0; yuva_girdi < 512; yuva_girdi++) {
                int değer = 0;
                if (bölüm_değer_366e0bfa < 2) değer = Dosya_tablo[bölüm_değer_366e0bfa * 512 + yuva_girdi];
                else {
                    int dosya = (bölüm_değer_366e0bfa - 2) / 32, konum = (bölüm_değer_366e0bfa - 2) % 32 * 512 + yuva_girdi;
                    if (Dosya_tablo[dosya * 72] != 0 && konum < Bellek_dosya_sistemi.boyutlandırmak_Liste[dosya])
                        değer = cihaz_değer.기억읽기(cihaz_değer.Dosya_Bellek() + dosya * 16384 + konum);
                }
                depolama_aygıtı_cxn.bölüm_veri[yuva_girdi] = değer; özet_Dosya = 바이트해시(özet_Dosya, değer);
            }
            if (depolama_aygıtı_cxn.Yazma(Start_bölüm + 1 + bölüm_değer_366e0bfa) < 0) return -5;
        }
        if (depolama_aygıtı_cxn.boşaltmak_çıktı() < 0) return -5;
        takas_veri(); depolama_aygıtı_cxn.yazma_bilgi_değer(0, 0x4a4b534e);
        depolama_aygıtı_cxn.yazma_bilgi_değer(4, 세대번호 + 1); depolama_aygıtı_cxn.yazma_bilgi_değer(8, özet_Dosya);
        depolama_aygıtı_cxn.yazma_bilgi_değer(12, (세대번호 + 1) ^ özet_Dosya ^ 0x4a4b534e);
        if (depolama_aygıtı_cxn.Yazma(Start_bölüm) < 0 || depolama_aygıtı_cxn.boşaltmak_çıktı() < 0) return -5;
        현재보존본 = Sonraki_öğe; 세대번호++;
        return 0;
    }
}
