// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_värde format_värde. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] fil_tabell = new int[1024];
    static int 바이트해시(int värde, int data) { return (värde ^ data) * 16777619; }
    static void rensa_data() {
        for (int INDEX = 0; INDEX < 512; INDEX++) lagringsenhet_kontakt.avsnitt_data[INDEX] = 0;
    }
    static int tabell_heltal(int position) {
        return fil_tabell[position] | fil_tabell[position + 1] << 8 | fil_tabell[position + 2] << 16 | fil_tabell[position + 3] << 24;
    }
    static void skriva_tabell_heltal(int position, int värde) {
        for (int INDEX = 0; INDEX < 4; INDEX++) fil_tabell[position + INDEX] = (värde >>> (INDEX * 8)) & 255;
    }
    static boolean check_tabell() {
        for (int filnamn = 0; filnamn < 8; filnamn++) {
            int längd_värde = 0;
            for (int fack_post = 0; fack_post < 64; fack_post++) Minne_filsystem.Namn[fack_post] = fil_tabell[filnamn * 72 + fack_post];
            while (längd_värde < 64 && Minne_filsystem.Namn[längd_värde] != 0) längd_värde++;
            if (längd_värde == 0) continue;
            if (!Minne_filsystem.check_namn(Minne_filsystem.Namn, längd_värde)
                || tabell_heltal(filnamn * 72 + 64) < 0 || tabell_heltal(filnamn * 72 + 64) > 16384) return false;
            for (int framåtvänd_värde = 0; framåtvänd_värde < filnamn; framåtvänd_värde++) {
                boolean 같음 = fil_tabell[framåtvänd_värde * 72 + längd_värde] == 0;
                for (int fack_post = 0; fack_post < längd_värde; fack_post++) if (fil_tabell[framåtvänd_värde * 72 + fack_post] != Minne_filsystem.Namn[fack_post]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int START_avsnitt = 1 + 보존본 * 259;
        if (lagringsenhet_kontakt.Läs(START_avsnitt) < 0 || lagringsenhet_kontakt.parsa_heltal(0) != 0x4a4b534e) return -1;
        int 세대 = lagringsenhet_kontakt.parsa_heltal(4), kontrollsumma = lagringsenhet_kontakt.parsa_heltal(8);
        if (세대 < 1 || lagringsenhet_kontakt.parsa_heltal(12) != (세대 ^ kontrollsumma ^ 0x4a4b534e)) return -1;
        int hash_fil = 0x811c9dc5;
        for (int avsnitt_värde = 0; avsnitt_värde < 258; avsnitt_värde++) {
            if (lagringsenhet_kontakt.Läs(START_avsnitt + 1 + avsnitt_värde) < 0) return -1;
            for (int fack_post = 0; fack_post < 512; fack_post++) {
                int värde = lagringsenhet_kontakt.avsnitt_data[fack_post];
                hash_fil = 바이트해시(hash_fil, värde);
                if (avsnitt_värde < 2) fil_tabell[avsnitt_värde * 512 + fack_post] = värde;
            }
        }
        return hash_fil == kontrollsumma && check_tabell() ? 세대 : -1;
    }
    static int Belastning(int 보존본) {
        int START_avsnitt = 1 + 보존본 * 259;
        for (int avsnitt_värde = 0; avsnitt_värde < 2; avsnitt_värde++) {
            if (lagringsenhet_kontakt.Läs(START_avsnitt + 1 + avsnitt_värde) < 0) return -5;
            for (int fack_post = 0; fack_post < 512; fack_post++) fil_tabell[avsnitt_värde * 512 + fack_post] = lagringsenhet_kontakt.avsnitt_data[fack_post];
        }
        for (int filnamn = 0; filnamn < 8; filnamn++) {
            for (int fack_post = 0; fack_post < 64; fack_post++) Minne_filsystem.이름들[filnamn * 64 + fack_post] = fil_tabell[filnamn * 72 + fack_post];
            Minne_filsystem.storlek_ange[filnamn] = fil_tabell[filnamn * 72] == 0 ? 0 : tabell_heltal(filnamn * 72 + 64);
            Minne_filsystem.허가들[filnamn] = tabell_heltal(filnamn * 72 + 68) & 511;
            for (int avsnitt_värde = 0; avsnitt_värde < 32; avsnitt_värde++) {
                if (lagringsenhet_kontakt.Läs(START_avsnitt + 3 + filnamn * 32 + avsnitt_värde) < 0) return -5;
                int Adress = enhet_värde.fil_Minne() + filnamn * 16384 + avsnitt_värde * 512;
                for (int fack_post = 0; fack_post < 512; fack_post++) enhet_värde.skriva_Minne(Adress + fack_post, lagringsenhet_kontakt.avsnitt_data[fack_post]);
            }
        }
        return 0;
    }
    static void Förbereda() {
        if (lagringsenhet_kontakt.Läs(0) < 0 || lagringsenhet_kontakt.parsa_heltal(0) != 0x54534b4a
            || lagringsenhet_kontakt.parsa_heltal(4) != 0x3145524f || lagringsenhet_kontakt.parsa_heltal(8) != 2048
            || lagringsenhet_kontakt.parsa_heltal(12) != 0x3153464a) {
            SMS_Terminal.Skriv("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        lagringsenhet_kontakt.informationsteknik_Aktiv_9e72441a = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Terminal.Skriv("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (Belastning(현재보존본) < 0) {
            SMS_Terminal.Skriv("STORE read failed; halted to preserve files\n"); enhet_värde.정지();
        }
        SMS_Terminal.Skriv("STORE restored generation "); SMS_Terminal.skriva_nummer(세대번호); SMS_Terminal.문자(10);
    }
    static int synka() {
        if (!lagringsenhet_kontakt.informationsteknik_Aktiv_9e72441a) return -19;
        if (세대번호 == 2147483647) return -75;
        int Nästa_objekt = 현재보존본 == 0 ? 1 : 0, START_avsnitt = 1 + Nästa_objekt * 259;
        // 새 본문보다 먼저 Föregående_objekt commit을 무효화하고 enhet_värde 캐시를 비운다.
        rensa_data();
        if (lagringsenhet_kontakt.Skriv(START_avsnitt) < 0 || lagringsenhet_kontakt.tömma_utleverans() < 0) return -5;
        for (int fack_post = 0; fack_post < 1024; fack_post++) fil_tabell[fack_post] = 0;
        for (int filnamn = 0; filnamn < 8; filnamn++) if (Minne_filsystem.이름들[filnamn * 64] != 0) {
            for (int fack_post = 0; fack_post < 64; fack_post++) fil_tabell[filnamn * 72 + fack_post] = Minne_filsystem.이름들[filnamn * 64 + fack_post];
            skriva_tabell_heltal(filnamn * 72 + 64, Minne_filsystem.storlek_ange[filnamn]);
            skriva_tabell_heltal(filnamn * 72 + 68, Minne_filsystem.허가들[filnamn]);
        }
        int hash_fil = 0x811c9dc5;
        for (int avsnitt_värde = 0; avsnitt_värde < 258; avsnitt_värde++) {
            for (int fack_post = 0; fack_post < 512; fack_post++) {
                int värde = 0;
                if (avsnitt_värde < 2) värde = fil_tabell[avsnitt_värde * 512 + fack_post];
                else {
                    int filnamn = (avsnitt_värde - 2) / 32, position = (avsnitt_värde - 2) % 32 * 512 + fack_post;
                    if (fil_tabell[filnamn * 72] != 0 && position < Minne_filsystem.storlek_ange[filnamn])
                        värde = enhet_värde.läsa_Minne(enhet_värde.fil_Minne() + filnamn * 16384 + position);
                }
                lagringsenhet_kontakt.avsnitt_data[fack_post] = värde; hash_fil = 바이트해시(hash_fil, värde);
            }
            if (lagringsenhet_kontakt.Skriv(START_avsnitt + 1 + avsnitt_värde) < 0) return -5;
        }
        if (lagringsenhet_kontakt.tömma_utleverans() < 0) return -5;
        rensa_data(); lagringsenhet_kontakt.skriva_heltal_värde(0, 0x4a4b534e);
        lagringsenhet_kontakt.skriva_heltal_värde(4, 세대번호 + 1); lagringsenhet_kontakt.skriva_heltal_värde(8, hash_fil);
        lagringsenhet_kontakt.skriva_heltal_värde(12, (세대번호 + 1) ^ hash_fil ^ 0x4a4b534e);
        if (lagringsenhet_kontakt.Skriv(START_avsnitt) < 0 || lagringsenhet_kontakt.tömma_utleverans() < 0) return -5;
        현재보존본 = Nästa_objekt; 세대번호++;
        return 0;
    }
}
