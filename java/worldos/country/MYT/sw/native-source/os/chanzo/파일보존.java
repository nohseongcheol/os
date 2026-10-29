// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_thamani umbiza_thamani. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] faili_jedwali = new int[1024];
    static int 바이트해시(int thamani, int data) { return (thamani ^ data) * 16777619; }
    static void ondoa_data() {
        for (int kielezo = 0; kielezo < 512; kielezo++) Hifadhi_kifaa_muunganisho.sehemu_data[kielezo] = 0;
    }
    static int jedwali_namba_kamili(int 위치) {
        return faili_jedwali[위치] | faili_jedwali[위치 + 1] << 8 | faili_jedwali[위치 + 2] << 16 | faili_jedwali[위치 + 3] << 24;
    }
    static void andika_jedwali_namba_kamili(int 위치, int thamani) {
        for (int kielezo = 0; kielezo < 4; kielezo++) faili_jedwali[위치 + kielezo] = (thamani >>> (kielezo * 8)) & 255;
    }
    static boolean hundi_jedwali() {
        for (int faili = 0; faili < 8; faili++) {
            int urefu_thamani = 0;
            for (int Sloti_ingizo = 0; Sloti_ingizo < 64; Sloti_ingizo++) kumbukumbu_mfumo_ya_mafaili.Jina[Sloti_ingizo] = faili_jedwali[faili * 72 + Sloti_ingizo];
            while (urefu_thamani < 64 && kumbukumbu_mfumo_ya_mafaili.Jina[urefu_thamani] != 0) urefu_thamani++;
            if (urefu_thamani == 0) continue;
            if (!kumbukumbu_mfumo_ya_mafaili.hundi_jina(kumbukumbu_mfumo_ya_mafaili.Jina, urefu_thamani)
                || jedwali_namba_kamili(faili * 72 + 64) < 0 || jedwali_namba_kamili(faili * 72 + 64) > 16384) return false;
            for (int mbele_thamani = 0; mbele_thamani < faili; mbele_thamani++) {
                boolean 같음 = faili_jedwali[mbele_thamani * 72 + urefu_thamani] == 0;
                for (int Sloti_ingizo = 0; Sloti_ingizo < urefu_thamani; Sloti_ingizo++) if (faili_jedwali[mbele_thamani * 72 + Sloti_ingizo] != kumbukumbu_mfumo_ya_mafaili.Jina[Sloti_ingizo]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int Anza_sehemu = 1 + 보존본 * 259;
        if (Hifadhi_kifaa_muunganisho.읽기(Anza_sehemu) < 0 || Hifadhi_kifaa_muunganisho.changanua_namba_kamili(0) != 0x4a4b534e) return -1;
        int 세대 = Hifadhi_kifaa_muunganisho.changanua_namba_kamili(4), jumla = Hifadhi_kifaa_muunganisho.changanua_namba_kamili(8);
        if (세대 < 1 || Hifadhi_kifaa_muunganisho.changanua_namba_kamili(12) != (세대 ^ jumla ^ 0x4a4b534e)) return -1;
        int kali_faili = 0x811c9dc5;
        for (int sehemu_thamani = 0; sehemu_thamani < 258; sehemu_thamani++) {
            if (Hifadhi_kifaa_muunganisho.읽기(Anza_sehemu + 1 + sehemu_thamani) < 0) return -1;
            for (int Sloti_ingizo = 0; Sloti_ingizo < 512; Sloti_ingizo++) {
                int thamani = Hifadhi_kifaa_muunganisho.sehemu_data[Sloti_ingizo];
                kali_faili = 바이트해시(kali_faili, thamani);
                if (sehemu_thamani < 2) faili_jedwali[sehemu_thamani * 512 + Sloti_ingizo] = thamani;
            }
        }
        return kali_faili == jumla && hundi_jedwali() ? 세대 : -1;
    }
    static int pakia(int 보존본) {
        int Anza_sehemu = 1 + 보존본 * 259;
        for (int sehemu_thamani = 0; sehemu_thamani < 2; sehemu_thamani++) {
            if (Hifadhi_kifaa_muunganisho.읽기(Anza_sehemu + 1 + sehemu_thamani) < 0) return -5;
            for (int Sloti_ingizo = 0; Sloti_ingizo < 512; Sloti_ingizo++) faili_jedwali[sehemu_thamani * 512 + Sloti_ingizo] = Hifadhi_kifaa_muunganisho.sehemu_data[Sloti_ingizo];
        }
        for (int faili = 0; faili < 8; faili++) {
            for (int Sloti_ingizo = 0; Sloti_ingizo < 64; Sloti_ingizo++) kumbukumbu_mfumo_ya_mafaili.이름들[faili * 64 + Sloti_ingizo] = faili_jedwali[faili * 72 + Sloti_ingizo];
            kumbukumbu_mfumo_ya_mafaili.panga_ukubwa_Orodha[faili] = faili_jedwali[faili * 72] == 0 ? 0 : jedwali_namba_kamili(faili * 72 + 64);
            kumbukumbu_mfumo_ya_mafaili.허가들[faili] = jedwali_namba_kamili(faili * 72 + 68) & 511;
            for (int sehemu_thamani = 0; sehemu_thamani < 32; sehemu_thamani++) {
                if (Hifadhi_kifaa_muunganisho.읽기(Anza_sehemu + 3 + faili * 32 + sehemu_thamani) < 0) return -5;
                int anwani = kifaa_thamani.faili_kumbukumbu() + faili * 16384 + sehemu_thamani * 512;
                for (int Sloti_ingizo = 0; Sloti_ingizo < 512; Sloti_ingizo++) kifaa_thamani.andika_kumbukumbu(anwani + Sloti_ingizo, Hifadhi_kifaa_muunganisho.sehemu_data[Sloti_ingizo]);
            }
        }
        return 0;
    }
    static void Andaa() {
        if (Hifadhi_kifaa_muunganisho.읽기(0) < 0 || Hifadhi_kifaa_muunganisho.changanua_namba_kamili(0) != 0x54534b4a
            || Hifadhi_kifaa_muunganisho.changanua_namba_kamili(4) != 0x3145524f || Hifadhi_kifaa_muunganisho.changanua_namba_kamili(8) != 2048
            || Hifadhi_kifaa_muunganisho.changanua_namba_kamili(12) != 0x3153464a) {
            문자단말.andika("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        Hifadhi_kifaa_muunganisho.teknolojia_ya_maelezo_Amilifu_9e72441a = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { 문자단말.andika("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (pakia(현재보존본) < 0) {
            문자단말.andika("STORE read failed; halted to preserve files\n"); kifaa_thamani.정지();
        }
        문자단말.andika("STORE restored generation "); 문자단말.수쓰기(세대번호); 문자단말.문자(10);
    }
    static int landanisha() {
        if (!Hifadhi_kifaa_muunganisho.teknolojia_ya_maelezo_Amilifu_9e72441a) return -19;
        if (세대번호 == 2147483647) return -75;
        int 다음 = 현재보존본 == 0 ? 1 : 0, Anza_sehemu = 1 + 다음 * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 kifaa_thamani 캐시를 비운다.
        ondoa_data();
        if (Hifadhi_kifaa_muunganisho.andika(Anza_sehemu) < 0 || Hifadhi_kifaa_muunganisho.밀어쓰기() < 0) return -5;
        for (int Sloti_ingizo = 0; Sloti_ingizo < 1024; Sloti_ingizo++) faili_jedwali[Sloti_ingizo] = 0;
        for (int faili = 0; faili < 8; faili++) if (kumbukumbu_mfumo_ya_mafaili.이름들[faili * 64] != 0) {
            for (int Sloti_ingizo = 0; Sloti_ingizo < 64; Sloti_ingizo++) faili_jedwali[faili * 72 + Sloti_ingizo] = kumbukumbu_mfumo_ya_mafaili.이름들[faili * 64 + Sloti_ingizo];
            andika_jedwali_namba_kamili(faili * 72 + 64, kumbukumbu_mfumo_ya_mafaili.panga_ukubwa_Orodha[faili]);
            andika_jedwali_namba_kamili(faili * 72 + 68, kumbukumbu_mfumo_ya_mafaili.허가들[faili]);
        }
        int kali_faili = 0x811c9dc5;
        for (int sehemu_thamani = 0; sehemu_thamani < 258; sehemu_thamani++) {
            for (int Sloti_ingizo = 0; Sloti_ingizo < 512; Sloti_ingizo++) {
                int thamani = 0;
                if (sehemu_thamani < 2) thamani = faili_jedwali[sehemu_thamani * 512 + Sloti_ingizo];
                else {
                    int faili = (sehemu_thamani - 2) / 32, 위치 = (sehemu_thamani - 2) % 32 * 512 + Sloti_ingizo;
                    if (faili_jedwali[faili * 72] != 0 && 위치 < kumbukumbu_mfumo_ya_mafaili.panga_ukubwa_Orodha[faili])
                        thamani = kifaa_thamani.기억읽기(kifaa_thamani.faili_kumbukumbu() + faili * 16384 + 위치);
                }
                Hifadhi_kifaa_muunganisho.sehemu_data[Sloti_ingizo] = thamani; kali_faili = 바이트해시(kali_faili, thamani);
            }
            if (Hifadhi_kifaa_muunganisho.andika(Anza_sehemu + 1 + sehemu_thamani) < 0) return -5;
        }
        if (Hifadhi_kifaa_muunganisho.밀어쓰기() < 0) return -5;
        ondoa_data(); Hifadhi_kifaa_muunganisho.andika_namba_kamili_thamani(0, 0x4a4b534e);
        Hifadhi_kifaa_muunganisho.andika_namba_kamili_thamani(4, 세대번호 + 1); Hifadhi_kifaa_muunganisho.andika_namba_kamili_thamani(8, kali_faili);
        Hifadhi_kifaa_muunganisho.andika_namba_kamili_thamani(12, (세대번호 + 1) ^ kali_faili ^ 0x4a4b534e);
        if (Hifadhi_kifaa_muunganisho.andika(Anza_sehemu) < 0 || Hifadhi_kifaa_muunganisho.밀어쓰기() < 0) return -5;
        현재보존본 = 다음; 세대번호++;
        return 0;
    }
}
