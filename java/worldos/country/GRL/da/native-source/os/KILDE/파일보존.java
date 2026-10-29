// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_VÆRDI format_VÆRDI. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] fil_tabel = new int[1024];
    static int 바이트해시(int VÆRDI, int data) { return (VÆRDI ^ data) * 16777619; }
    static void rydde_data() {
        for (int INDEKS = 0; INDEKS < 512; INDEKS++) lagerenhed_forbindelse.sektion_data[INDEKS] = 0;
    }
    static int tabel_heltal(int Placering) {
        return fil_tabel[Placering] | fil_tabel[Placering + 1] << 8 | fil_tabel[Placering + 2] << 16 | fil_tabel[Placering + 3] << 24;
    }
    static void skrive_tabel_heltal(int Placering, int VÆRDI) {
        for (int INDEKS = 0; INDEKS < 4; INDEKS++) fil_tabel[Placering + INDEKS] = (VÆRDI >>> (INDEKS * 8)) & 255;
    }
    static boolean check_tabel() {
        for (int Fil = 0; Fil < 8; Fil++) {
            int varighed_VÆRDI = 0;
            for (int udvidelsesstik_post = 0; udvidelsesstik_post < 64; udvidelsesstik_post++) Hukommelse_filsystem.Navn[udvidelsesstik_post] = fil_tabel[Fil * 72 + udvidelsesstik_post];
            while (varighed_VÆRDI < 64 && Hukommelse_filsystem.Navn[varighed_VÆRDI] != 0) varighed_VÆRDI++;
            if (varighed_VÆRDI == 0) continue;
            if (!Hukommelse_filsystem.check_navn(Hukommelse_filsystem.Navn, varighed_VÆRDI)
                || tabel_heltal(Fil * 72 + 64) < 0 || tabel_heltal(Fil * 72 + 64) > 16384) return false;
            for (int frontvendt_VÆRDI = 0; frontvendt_VÆRDI < Fil; frontvendt_VÆRDI++) {
                boolean 같음 = fil_tabel[frontvendt_VÆRDI * 72 + varighed_VÆRDI] == 0;
                for (int udvidelsesstik_post = 0; udvidelsesstik_post < varighed_VÆRDI; udvidelsesstik_post++) if (fil_tabel[frontvendt_VÆRDI * 72 + udvidelsesstik_post] != Hukommelse_filsystem.Navn[udvidelsesstik_post]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int START_sektion = 1 + 보존본 * 259;
        if (lagerenhed_forbindelse.Læse(START_sektion) < 0 || lagerenhed_forbindelse.opdele_tekst_heltal(0) != 0x4a4b534e) return -1;
        int 세대 = lagerenhed_forbindelse.opdele_tekst_heltal(4), kontrolsum = lagerenhed_forbindelse.opdele_tekst_heltal(8);
        if (세대 < 1 || lagerenhed_forbindelse.opdele_tekst_heltal(12) != (세대 ^ kontrolsum ^ 0x4a4b534e)) return -1;
        int hash_fil = 0x811c9dc5;
        for (int sektion_VÆRDI = 0; sektion_VÆRDI < 258; sektion_VÆRDI++) {
            if (lagerenhed_forbindelse.Læse(START_sektion + 1 + sektion_VÆRDI) < 0) return -1;
            for (int udvidelsesstik_post = 0; udvidelsesstik_post < 512; udvidelsesstik_post++) {
                int VÆRDI = lagerenhed_forbindelse.sektion_data[udvidelsesstik_post];
                hash_fil = 바이트해시(hash_fil, VÆRDI);
                if (sektion_VÆRDI < 2) fil_tabel[sektion_VÆRDI * 512 + udvidelsesstik_post] = VÆRDI;
            }
        }
        return hash_fil == kontrolsum && check_tabel() ? 세대 : -1;
    }
    static int Belastning(int 보존본) {
        int START_sektion = 1 + 보존본 * 259;
        for (int sektion_VÆRDI = 0; sektion_VÆRDI < 2; sektion_VÆRDI++) {
            if (lagerenhed_forbindelse.Læse(START_sektion + 1 + sektion_VÆRDI) < 0) return -5;
            for (int udvidelsesstik_post = 0; udvidelsesstik_post < 512; udvidelsesstik_post++) fil_tabel[sektion_VÆRDI * 512 + udvidelsesstik_post] = lagerenhed_forbindelse.sektion_data[udvidelsesstik_post];
        }
        for (int Fil = 0; Fil < 8; Fil++) {
            for (int udvidelsesstik_post = 0; udvidelsesstik_post < 64; udvidelsesstik_post++) Hukommelse_filsystem.이름들[Fil * 64 + udvidelsesstik_post] = fil_tabel[Fil * 72 + udvidelsesstik_post];
            Hukommelse_filsystem.tilpasse_størrelse_Liste[Fil] = fil_tabel[Fil * 72] == 0 ? 0 : tabel_heltal(Fil * 72 + 64);
            Hukommelse_filsystem.허가들[Fil] = tabel_heltal(Fil * 72 + 68) & 511;
            for (int sektion_VÆRDI = 0; sektion_VÆRDI < 32; sektion_VÆRDI++) {
                if (lagerenhed_forbindelse.Læse(START_sektion + 3 + Fil * 32 + sektion_VÆRDI) < 0) return -5;
                int mail = enhed_VÆRDI.fil_Hukommelse() + Fil * 16384 + sektion_VÆRDI * 512;
                for (int udvidelsesstik_post = 0; udvidelsesstik_post < 512; udvidelsesstik_post++) enhed_VÆRDI.skrive_Hukommelse(mail + udvidelsesstik_post, lagerenhed_forbindelse.sektion_data[udvidelsesstik_post]);
            }
        }
        return 0;
    }
    static void Tilrettelæg() {
        if (lagerenhed_forbindelse.Læse(0) < 0 || lagerenhed_forbindelse.opdele_tekst_heltal(0) != 0x54534b4a
            || lagerenhed_forbindelse.opdele_tekst_heltal(4) != 0x3145524f || lagerenhed_forbindelse.opdele_tekst_heltal(8) != 2048
            || lagerenhed_forbindelse.opdele_tekst_heltal(12) != 0x3153464a) {
            sms_Terminal.Skrive("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        lagerenhed_forbindelse.it_Aktiv_9e72441a = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { sms_Terminal.Skrive("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (Belastning(현재보존본) < 0) {
            sms_Terminal.Skrive("STORE read failed; halted to preserve files\n"); enhed_VÆRDI.정지();
        }
        sms_Terminal.Skrive("STORE restored generation "); sms_Terminal.skrive_tal(세대번호); sms_Terminal.문자(10);
    }
    static int synkronisere() {
        if (!lagerenhed_forbindelse.it_Aktiv_9e72441a) return -19;
        if (세대번호 == 2147483647) return -75;
        int Næste_vare = 현재보존본 == 0 ? 1 : 0, START_sektion = 1 + Næste_vare * 259;
        // 새 본문보다 먼저 Forrige_vare commit을 무효화하고 enhed_VÆRDI 캐시를 비운다.
        rydde_data();
        if (lagerenhed_forbindelse.Skrive(START_sektion) < 0 || lagerenhed_forbindelse.밀어쓰기() < 0) return -5;
        for (int udvidelsesstik_post = 0; udvidelsesstik_post < 1024; udvidelsesstik_post++) fil_tabel[udvidelsesstik_post] = 0;
        for (int Fil = 0; Fil < 8; Fil++) if (Hukommelse_filsystem.이름들[Fil * 64] != 0) {
            for (int udvidelsesstik_post = 0; udvidelsesstik_post < 64; udvidelsesstik_post++) fil_tabel[Fil * 72 + udvidelsesstik_post] = Hukommelse_filsystem.이름들[Fil * 64 + udvidelsesstik_post];
            skrive_tabel_heltal(Fil * 72 + 64, Hukommelse_filsystem.tilpasse_størrelse_Liste[Fil]);
            skrive_tabel_heltal(Fil * 72 + 68, Hukommelse_filsystem.허가들[Fil]);
        }
        int hash_fil = 0x811c9dc5;
        for (int sektion_VÆRDI = 0; sektion_VÆRDI < 258; sektion_VÆRDI++) {
            for (int udvidelsesstik_post = 0; udvidelsesstik_post < 512; udvidelsesstik_post++) {
                int VÆRDI = 0;
                if (sektion_VÆRDI < 2) VÆRDI = fil_tabel[sektion_VÆRDI * 512 + udvidelsesstik_post];
                else {
                    int Fil = (sektion_VÆRDI - 2) / 32, Placering = (sektion_VÆRDI - 2) % 32 * 512 + udvidelsesstik_post;
                    if (fil_tabel[Fil * 72] != 0 && Placering < Hukommelse_filsystem.tilpasse_størrelse_Liste[Fil])
                        VÆRDI = enhed_VÆRDI.기억읽기(enhed_VÆRDI.fil_Hukommelse() + Fil * 16384 + Placering);
                }
                lagerenhed_forbindelse.sektion_data[udvidelsesstik_post] = VÆRDI; hash_fil = 바이트해시(hash_fil, VÆRDI);
            }
            if (lagerenhed_forbindelse.Skrive(START_sektion + 1 + sektion_VÆRDI) < 0) return -5;
        }
        if (lagerenhed_forbindelse.밀어쓰기() < 0) return -5;
        rydde_data(); lagerenhed_forbindelse.skrive_heltal_VÆRDI(0, 0x4a4b534e);
        lagerenhed_forbindelse.skrive_heltal_VÆRDI(4, 세대번호 + 1); lagerenhed_forbindelse.skrive_heltal_VÆRDI(8, hash_fil);
        lagerenhed_forbindelse.skrive_heltal_VÆRDI(12, (세대번호 + 1) ^ hash_fil ^ 0x4a4b534e);
        if (lagerenhed_forbindelse.Skrive(START_sektion) < 0 || lagerenhed_forbindelse.밀어쓰기() < 0) return -5;
        현재보존본 = Næste_vare; 세대번호++;
        return 0;
    }
}
