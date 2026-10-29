// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Ajiye_Daraja zubi_Daraja. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] Fayil_tebur = new int[1024];
    static int 바이트해시(int Daraja, int Tarin_bayani) { return (Daraja ^ Tarin_bayani) * 16777619; }
    static void Share_Tarin_bayani() {
        for (int Indes = 0; Indes < 512; Indes++) Wurin_adana_na_ura_haɗi.Sashi_Tarin_bayani[Indes] = 0;
    }
    static int tebur_Lamba_mara(int 위치) {
        return Fayil_tebur[위치] | Fayil_tebur[위치 + 1] << 8 | Fayil_tebur[위치 + 2] << 16 | Fayil_tebur[위치 + 3] << 24;
    }
    static void Rubuta_tebur_Lamba_mara(int 위치, int Daraja) {
        for (int Indes = 0; Indes < 4; Indes++) Fayil_tebur[위치 + Indes] = (Daraja >>> (Indes * 8)) & 255;
    }
    static boolean Bincika_tebur() {
        for (int Fayil = 0; Fayil < 8; Fayil++) {
            int Tsawo_Daraja = 0;
            for (int rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < 64; rami_Mashigar_bayanai++) Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.Suna[rami_Mashigar_bayanai] = Fayil_tebur[Fayil * 72 + rami_Mashigar_bayanai];
            while (Tsawo_Daraja < 64 && Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.Suna[Tsawo_Daraja] != 0) Tsawo_Daraja++;
            if (Tsawo_Daraja == 0) continue;
            if (!Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.Bincika_Suna(Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.Suna, Tsawo_Daraja)
                || tebur_Lamba_mara(Fayil * 72 + 64) < 0 || tebur_Lamba_mara(Fayil * 72 + 64) > 16384) return false;
            for (int kyamarar_gaba_Daraja = 0; kyamarar_gaba_Daraja < Fayil; kyamarar_gaba_Daraja++) {
                boolean 같음 = Fayil_tebur[kyamarar_gaba_Daraja * 72 + Tsawo_Daraja] == 0;
                for (int rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < Tsawo_Daraja; rami_Mashigar_bayanai++) if (Fayil_tebur[kyamarar_gaba_Daraja * 72 + rami_Mashigar_bayanai] != Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.Suna[rami_Mashigar_bayanai]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int Fara_Sashi = 1 + 보존본 * 259;
        if (Wurin_adana_na_ura_haɗi.Yi_Karatu(Fara_Sashi) < 0 || Wurin_adana_na_ura_haɗi.Daddatse_Lamba_mara(0) != 0x4a4b534e) return -1;
        int 세대 = Wurin_adana_na_ura_haɗi.Daddatse_Lamba_mara(4), checksum = Wurin_adana_na_ura_haɗi.Daddatse_Lamba_mara(8);
        if (세대 < 1 || Wurin_adana_na_ura_haɗi.Daddatse_Lamba_mara(12) != (세대 ^ checksum ^ 0x4a4b534e)) return -1;
        int hash_Fayil = 0x811c9dc5;
        for (int Sashi_Daraja = 0; Sashi_Daraja < 258; Sashi_Daraja++) {
            if (Wurin_adana_na_ura_haɗi.Yi_Karatu(Fara_Sashi + 1 + Sashi_Daraja) < 0) return -1;
            for (int rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < 512; rami_Mashigar_bayanai++) {
                int Daraja = Wurin_adana_na_ura_haɗi.Sashi_Tarin_bayani[rami_Mashigar_bayanai];
                hash_Fayil = 바이트해시(hash_Fayil, Daraja);
                if (Sashi_Daraja < 2) Fayil_tebur[Sashi_Daraja * 512 + rami_Mashigar_bayanai] = Daraja;
            }
        }
        return hash_Fayil == checksum && Bincika_tebur() ? 세대 : -1;
    }
    static int loda(int 보존본) {
        int Fara_Sashi = 1 + 보존본 * 259;
        for (int Sashi_Daraja = 0; Sashi_Daraja < 2; Sashi_Daraja++) {
            if (Wurin_adana_na_ura_haɗi.Yi_Karatu(Fara_Sashi + 1 + Sashi_Daraja) < 0) return -5;
            for (int rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < 512; rami_Mashigar_bayanai++) Fayil_tebur[Sashi_Daraja * 512 + rami_Mashigar_bayanai] = Wurin_adana_na_ura_haɗi.Sashi_Tarin_bayani[rami_Mashigar_bayanai];
        }
        for (int Fayil = 0; Fayil < 8; Fayil++) {
            for (int rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < 64; rami_Mashigar_bayanai++) Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.이름들[Fayil * 64 + rami_Mashigar_bayanai] = Fayil_tebur[Fayil * 72 + rami_Mashigar_bayanai];
            Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.girma_Jeri[Fayil] = Fayil_tebur[Fayil * 72] == 0 ? 0 : tebur_Lamba_mara(Fayil * 72 + 64);
            Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.허가들[Fayil] = tebur_Lamba_mara(Fayil * 72 + 68) & 511;
            for (int Sashi_Daraja = 0; Sashi_Daraja < 32; Sashi_Daraja++) {
                if (Wurin_adana_na_ura_haɗi.Yi_Karatu(Fara_Sashi + 3 + Fayil * 32 + Sashi_Daraja) < 0) return -5;
                int imel = na_ura_Daraja.Fayil_Mahardatar_kwamfuta() + Fayil * 16384 + Sashi_Daraja * 512;
                for (int rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < 512; rami_Mashigar_bayanai++) na_ura_Daraja.Rubuta_Mahardatar_kwamfuta(imel + rami_Mashigar_bayanai, Wurin_adana_na_ura_haɗi.Sashi_Tarin_bayani[rami_Mashigar_bayanai]);
            }
        }
        return 0;
    }
    static void Shirya() {
        if (Wurin_adana_na_ura_haɗi.Yi_Karatu(0) < 0 || Wurin_adana_na_ura_haɗi.Daddatse_Lamba_mara(0) != 0x54534b4a
            || Wurin_adana_na_ura_haɗi.Daddatse_Lamba_mara(4) != 0x3145524f || Wurin_adana_na_ura_haɗi.Daddatse_Lamba_mara(8) != 2048
            || Wurin_adana_na_ura_haɗi.Daddatse_Lamba_mara(12) != 0x3153464a) {
            문자단말.Yi_Rubutu("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        Wurin_adana_na_ura_haɗi.kimiyar_bayanai_Aiki_9e72441a = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { 문자단말.Yi_Rubutu("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (loda(현재보존본) < 0) {
            문자단말.Yi_Rubutu("STORE read failed; halted to preserve files\n"); na_ura_Daraja.정지();
        }
        문자단말.Yi_Rubutu("STORE restored generation "); 문자단말.수쓰기(세대번호); 문자단말.문자(10);
    }
    static int daidaita() {
        if (!Wurin_adana_na_ura_haɗi.kimiyar_bayanai_Aiki_9e72441a) return -19;
        if (세대번호 == 2147483647) return -75;
        int 다음 = 현재보존본 == 0 ? 1 : 0, Fara_Sashi = 1 + 다음 * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 na_ura_Daraja 캐시를 비운다.
        Share_Tarin_bayani();
        if (Wurin_adana_na_ura_haɗi.Yi_Rubutu(Fara_Sashi) < 0 || Wurin_adana_na_ura_haɗi.밀어쓰기() < 0) return -5;
        for (int rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < 1024; rami_Mashigar_bayanai++) Fayil_tebur[rami_Mashigar_bayanai] = 0;
        for (int Fayil = 0; Fayil < 8; Fayil++) if (Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.이름들[Fayil * 64] != 0) {
            for (int rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < 64; rami_Mashigar_bayanai++) Fayil_tebur[Fayil * 72 + rami_Mashigar_bayanai] = Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.이름들[Fayil * 64 + rami_Mashigar_bayanai];
            Rubuta_tebur_Lamba_mara(Fayil * 72 + 64, Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.girma_Jeri[Fayil]);
            Rubuta_tebur_Lamba_mara(Fayil * 72 + 68, Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.허가들[Fayil]);
        }
        int hash_Fayil = 0x811c9dc5;
        for (int Sashi_Daraja = 0; Sashi_Daraja < 258; Sashi_Daraja++) {
            for (int rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < 512; rami_Mashigar_bayanai++) {
                int Daraja = 0;
                if (Sashi_Daraja < 2) Daraja = Fayil_tebur[Sashi_Daraja * 512 + rami_Mashigar_bayanai];
                else {
                    int Fayil = (Sashi_Daraja - 2) / 32, 위치 = (Sashi_Daraja - 2) % 32 * 512 + rami_Mashigar_bayanai;
                    if (Fayil_tebur[Fayil * 72] != 0 && 위치 < Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.girma_Jeri[Fayil])
                        Daraja = na_ura_Daraja.기억읽기(na_ura_Daraja.Fayil_Mahardatar_kwamfuta() + Fayil * 16384 + 위치);
                }
                Wurin_adana_na_ura_haɗi.Sashi_Tarin_bayani[rami_Mashigar_bayanai] = Daraja; hash_Fayil = 바이트해시(hash_Fayil, Daraja);
            }
            if (Wurin_adana_na_ura_haɗi.Yi_Rubutu(Fara_Sashi + 1 + Sashi_Daraja) < 0) return -5;
        }
        if (Wurin_adana_na_ura_haɗi.밀어쓰기() < 0) return -5;
        Share_Tarin_bayani(); Wurin_adana_na_ura_haɗi.Rubuta_Lamba_mara_Daraja(0, 0x4a4b534e);
        Wurin_adana_na_ura_haɗi.Rubuta_Lamba_mara_Daraja(4, 세대번호 + 1); Wurin_adana_na_ura_haɗi.Rubuta_Lamba_mara_Daraja(8, hash_Fayil);
        Wurin_adana_na_ura_haɗi.Rubuta_Lamba_mara_Daraja(12, (세대번호 + 1) ^ hash_Fayil ^ 0x4a4b534e);
        if (Wurin_adana_na_ura_haɗi.Yi_Rubutu(Fara_Sashi) < 0 || Wurin_adana_na_ura_haɗi.밀어쓰기() < 0) return -5;
        현재보존본 = 다음; 세대번호++;
        return 0;
    }
}
