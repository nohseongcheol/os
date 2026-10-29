// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_uara hōputu_uara. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] kōnae_ripanga = new int[1024];
    static int 바이트해시(int uara, int raraunga) { return (uara ^ raraunga) * 16777619; }
    static void ūkui_raraunga() {
        for (int INDEX = 0; INDEX < 512; INDEX++) Rokiroki_pūkoro_hononga.wāhanga_raraunga[INDEX] = 0;
    }
    static int ripanga_tau_tōpū(int tūranga) {
        return kōnae_ripanga[tūranga] | kōnae_ripanga[tūranga + 1] << 8 | kōnae_ripanga[tūranga + 2] << 16 | kōnae_ripanga[tūranga + 3] << 24;
    }
    static void tuhi_ripanga_tau_tōpū(int tūranga, int uara) {
        for (int INDEX = 0; INDEX < 4; INDEX++) kōnae_ripanga[tūranga + INDEX] = (uara >>> (INDEX * 8)) & 255;
    }
    static boolean taki_ripanga() {
        for (int Kōnae = 0; Kōnae < 8; Kōnae++) {
            int roa_uara = 0;
            for (int kāniwha_tāurunga = 0; kāniwha_tāurunga < 64; kāniwha_tāurunga++) Pūmahara_pūnaha_kōnae.Ingoa[kāniwha_tāurunga] = kōnae_ripanga[Kōnae * 72 + kāniwha_tāurunga];
            while (roa_uara < 64 && Pūmahara_pūnaha_kōnae.Ingoa[roa_uara] != 0) roa_uara++;
            if (roa_uara == 0) continue;
            if (!Pūmahara_pūnaha_kōnae.taki_ingoa(Pūmahara_pūnaha_kōnae.Ingoa, roa_uara)
                || ripanga_tau_tōpū(Kōnae * 72 + 64) < 0 || ripanga_tau_tōpū(Kōnae * 72 + 64) > 16384) return false;
            for (int 앞 = 0; 앞 < Kōnae; 앞++) {
                boolean 같음 = kōnae_ripanga[앞 * 72 + roa_uara] == 0;
                for (int kāniwha_tāurunga = 0; kāniwha_tāurunga < roa_uara; kāniwha_tāurunga++) if (kōnae_ripanga[앞 * 72 + kāniwha_tāurunga] != Pūmahara_pūnaha_kōnae.Ingoa[kāniwha_tāurunga]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int Start_wāhanga = 1 + 보존본 * 259;
        if (Rokiroki_pūkoro_hononga.Pānuitia(Start_wāhanga) < 0 || Rokiroki_pūkoro_hononga.poroporo_tau_tōpū(0) != 0x4a4b534e) return -1;
        int 세대 = Rokiroki_pūkoro_hononga.poroporo_tau_tōpū(4), 검사합 = Rokiroki_pūkoro_hononga.poroporo_tau_tōpū(8);
        if (세대 < 1 || Rokiroki_pūkoro_hononga.poroporo_tau_tōpū(12) != (세대 ^ 검사합 ^ 0x4a4b534e)) return -1;
        int hash_kōnae = 0x811c9dc5;
        for (int wāhanga_uara = 0; wāhanga_uara < 258; wāhanga_uara++) {
            if (Rokiroki_pūkoro_hononga.Pānuitia(Start_wāhanga + 1 + wāhanga_uara) < 0) return -1;
            for (int kāniwha_tāurunga = 0; kāniwha_tāurunga < 512; kāniwha_tāurunga++) {
                int uara = Rokiroki_pūkoro_hononga.wāhanga_raraunga[kāniwha_tāurunga];
                hash_kōnae = 바이트해시(hash_kōnae, uara);
                if (wāhanga_uara < 2) kōnae_ripanga[wāhanga_uara * 512 + kāniwha_tāurunga] = uara;
            }
        }
        return hash_kōnae == 검사합 && taki_ripanga() ? 세대 : -1;
    }
    static int uta(int 보존본) {
        int Start_wāhanga = 1 + 보존본 * 259;
        for (int wāhanga_uara = 0; wāhanga_uara < 2; wāhanga_uara++) {
            if (Rokiroki_pūkoro_hononga.Pānuitia(Start_wāhanga + 1 + wāhanga_uara) < 0) return -5;
            for (int kāniwha_tāurunga = 0; kāniwha_tāurunga < 512; kāniwha_tāurunga++) kōnae_ripanga[wāhanga_uara * 512 + kāniwha_tāurunga] = Rokiroki_pūkoro_hononga.wāhanga_raraunga[kāniwha_tāurunga];
        }
        for (int Kōnae = 0; Kōnae < 8; Kōnae++) {
            for (int kāniwha_tāurunga = 0; kāniwha_tāurunga < 64; kāniwha_tāurunga++) Pūmahara_pūnaha_kōnae.이름들[Kōnae * 64 + kāniwha_tāurunga] = kōnae_ripanga[Kōnae * 72 + kāniwha_tāurunga];
            Pūmahara_pūnaha_kōnae.rahi_Rārangi[Kōnae] = kōnae_ripanga[Kōnae * 72] == 0 ? 0 : ripanga_tau_tōpū(Kōnae * 72 + 64);
            Pūmahara_pūnaha_kōnae.허가들[Kōnae] = ripanga_tau_tōpū(Kōnae * 72 + 68) & 511;
            for (int wāhanga_uara = 0; wāhanga_uara < 32; wāhanga_uara++) {
                if (Rokiroki_pūkoro_hononga.Pānuitia(Start_wāhanga + 3 + Kōnae * 32 + wāhanga_uara) < 0) return -5;
                int ADDRESS = pūkoro_uara.kōnae_Pūmahara() + Kōnae * 16384 + wāhanga_uara * 512;
                for (int kāniwha_tāurunga = 0; kāniwha_tāurunga < 512; kāniwha_tāurunga++) pūkoro_uara.tuhi_Pūmahara(ADDRESS + kāniwha_tāurunga, Rokiroki_pūkoro_hononga.wāhanga_raraunga[kāniwha_tāurunga]);
            }
        }
        return 0;
    }
    static void Whakarite() {
        if (Rokiroki_pūkoro_hononga.Pānuitia(0) < 0 || Rokiroki_pūkoro_hononga.poroporo_tau_tōpū(0) != 0x54534b4a
            || Rokiroki_pūkoro_hononga.poroporo_tau_tōpū(4) != 0x3145524f || Rokiroki_pūkoro_hononga.poroporo_tau_tōpū(8) != 2048
            || Rokiroki_pūkoro_hononga.poroporo_tau_tōpū(12) != 0x3153464a) {
            TEXT_Tauranga.Tuhia("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        Rokiroki_pūkoro_hononga.사용가능 = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { TEXT_Tauranga.Tuhia("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (uta(현재보존본) < 0) {
            TEXT_Tauranga.Tuhia("STORE read failed; halted to preserve files\n"); pūkoro_uara.정지();
        }
        TEXT_Tauranga.Tuhia("STORE restored generation "); TEXT_Tauranga.수쓰기(세대번호); TEXT_Tauranga.문자(10);
    }
    static int tukutahi() {
        if (!Rokiroki_pūkoro_hononga.사용가능) return -19;
        if (세대번호 == 2147483647) return -75;
        int Panuku_tuemi = 현재보존본 == 0 ? 1 : 0, Start_wāhanga = 1 + Panuku_tuemi * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 pūkoro_uara 캐시를 비운다.
        ūkui_raraunga();
        if (Rokiroki_pūkoro_hononga.Tuhia(Start_wāhanga) < 0 || Rokiroki_pūkoro_hononga.밀어쓰기() < 0) return -5;
        for (int kāniwha_tāurunga = 0; kāniwha_tāurunga < 1024; kāniwha_tāurunga++) kōnae_ripanga[kāniwha_tāurunga] = 0;
        for (int Kōnae = 0; Kōnae < 8; Kōnae++) if (Pūmahara_pūnaha_kōnae.이름들[Kōnae * 64] != 0) {
            for (int kāniwha_tāurunga = 0; kāniwha_tāurunga < 64; kāniwha_tāurunga++) kōnae_ripanga[Kōnae * 72 + kāniwha_tāurunga] = Pūmahara_pūnaha_kōnae.이름들[Kōnae * 64 + kāniwha_tāurunga];
            tuhi_ripanga_tau_tōpū(Kōnae * 72 + 64, Pūmahara_pūnaha_kōnae.rahi_Rārangi[Kōnae]);
            tuhi_ripanga_tau_tōpū(Kōnae * 72 + 68, Pūmahara_pūnaha_kōnae.허가들[Kōnae]);
        }
        int hash_kōnae = 0x811c9dc5;
        for (int wāhanga_uara = 0; wāhanga_uara < 258; wāhanga_uara++) {
            for (int kāniwha_tāurunga = 0; kāniwha_tāurunga < 512; kāniwha_tāurunga++) {
                int uara = 0;
                if (wāhanga_uara < 2) uara = kōnae_ripanga[wāhanga_uara * 512 + kāniwha_tāurunga];
                else {
                    int Kōnae = (wāhanga_uara - 2) / 32, tūranga = (wāhanga_uara - 2) % 32 * 512 + kāniwha_tāurunga;
                    if (kōnae_ripanga[Kōnae * 72] != 0 && tūranga < Pūmahara_pūnaha_kōnae.rahi_Rārangi[Kōnae])
                        uara = pūkoro_uara.기억읽기(pūkoro_uara.kōnae_Pūmahara() + Kōnae * 16384 + tūranga);
                }
                Rokiroki_pūkoro_hononga.wāhanga_raraunga[kāniwha_tāurunga] = uara; hash_kōnae = 바이트해시(hash_kōnae, uara);
            }
            if (Rokiroki_pūkoro_hononga.Tuhia(Start_wāhanga + 1 + wāhanga_uara) < 0) return -5;
        }
        if (Rokiroki_pūkoro_hononga.밀어쓰기() < 0) return -5;
        ūkui_raraunga(); Rokiroki_pūkoro_hononga.tuhi_tau_tōpū_uara(0, 0x4a4b534e);
        Rokiroki_pūkoro_hononga.tuhi_tau_tōpū_uara(4, 세대번호 + 1); Rokiroki_pūkoro_hononga.tuhi_tau_tōpū_uara(8, hash_kōnae);
        Rokiroki_pūkoro_hononga.tuhi_tau_tōpū_uara(12, (세대번호 + 1) ^ hash_kōnae ^ 0x4a4b534e);
        if (Rokiroki_pūkoro_hononga.Tuhia(Start_wāhanga) < 0 || Rokiroki_pūkoro_hononga.밀어쓰기() < 0) return -5;
        현재보존본 = Panuku_tuemi; 세대번호++;
        return 0;
    }
}
