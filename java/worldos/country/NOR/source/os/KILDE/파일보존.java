// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_VERDI format_VERDI. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] Fil_tabell = new int[1024];
    static int 바이트해시(int VERDI, int data) { return (VERDI ^ data) * 16777619; }
    static void tømme_data() {
        for (int INDEKS = 0; INDEKS < 512; INDEKS++) lagringsenhet_kontakt.inndeling_data[INDEKS] = 0;
    }
    static int tabell_heltall(int Posisjon) {
        return Fil_tabell[Posisjon] | Fil_tabell[Posisjon + 1] << 8 | Fil_tabell[Posisjon + 2] << 16 | Fil_tabell[Posisjon + 3] << 24;
    }
    static void skrive_tabell_heltall(int Posisjon, int VERDI) {
        for (int INDEKS = 0; INDEKS < 4; INDEKS++) Fil_tabell[Posisjon + INDEKS] = (VERDI >>> (INDEKS * 8)) & 255;
    }
    static boolean sjekk_tabell() {
        for (int Fil = 0; Fil < 8; Fil++) {
            int lengde_VERDI = 0;
            for (int åpning_oppføring = 0; åpning_oppføring < 64; åpning_oppføring++) Minne_filsystem.Navn[åpning_oppføring] = Fil_tabell[Fil * 72 + åpning_oppføring];
            while (lengde_VERDI < 64 && Minne_filsystem.Navn[lengde_VERDI] != 0) lengde_VERDI++;
            if (lengde_VERDI == 0) continue;
            if (!Minne_filsystem.sjekk_navn(Minne_filsystem.Navn, lengde_VERDI)
                || tabell_heltall(Fil * 72 + 64) < 0 || tabell_heltall(Fil * 72 + 64) > 16384) return false;
            for (int frontkamera_VERDI = 0; frontkamera_VERDI < Fil; frontkamera_VERDI++) {
                boolean 같음 = Fil_tabell[frontkamera_VERDI * 72 + lengde_VERDI] == 0;
                for (int åpning_oppføring = 0; åpning_oppføring < lengde_VERDI; åpning_oppføring++) if (Fil_tabell[frontkamera_VERDI * 72 + åpning_oppføring] != Minne_filsystem.Navn[åpning_oppføring]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int START_inndeling = 1 + 보존본 * 259;
        if (lagringsenhet_kontakt.Les(START_inndeling) < 0 || lagringsenhet_kontakt.dele_opp_heltall(0) != 0x4a4b534e) return -1;
        int 세대 = lagringsenhet_kontakt.dele_opp_heltall(4), kontrollsum = lagringsenhet_kontakt.dele_opp_heltall(8);
        if (세대 < 1 || lagringsenhet_kontakt.dele_opp_heltall(12) != (세대 ^ kontrollsum ^ 0x4a4b534e)) return -1;
        int hash_Fil = 0x811c9dc5;
        for (int inndeling_VERDI = 0; inndeling_VERDI < 258; inndeling_VERDI++) {
            if (lagringsenhet_kontakt.Les(START_inndeling + 1 + inndeling_VERDI) < 0) return -1;
            for (int åpning_oppføring = 0; åpning_oppføring < 512; åpning_oppføring++) {
                int VERDI = lagringsenhet_kontakt.inndeling_data[åpning_oppføring];
                hash_Fil = 바이트해시(hash_Fil, VERDI);
                if (inndeling_VERDI < 2) Fil_tabell[inndeling_VERDI * 512 + åpning_oppføring] = VERDI;
            }
        }
        return hash_Fil == kontrollsum && sjekk_tabell() ? 세대 : -1;
    }
    static int Belastning(int 보존본) {
        int START_inndeling = 1 + 보존본 * 259;
        for (int inndeling_VERDI = 0; inndeling_VERDI < 2; inndeling_VERDI++) {
            if (lagringsenhet_kontakt.Les(START_inndeling + 1 + inndeling_VERDI) < 0) return -5;
            for (int åpning_oppføring = 0; åpning_oppføring < 512; åpning_oppføring++) Fil_tabell[inndeling_VERDI * 512 + åpning_oppføring] = lagringsenhet_kontakt.inndeling_data[åpning_oppføring];
        }
        for (int Fil = 0; Fil < 8; Fil++) {
            for (int åpning_oppføring = 0; åpning_oppføring < 64; åpning_oppføring++) Minne_filsystem.이름들[Fil * 64 + åpning_oppføring] = Fil_tabell[Fil * 72 + åpning_oppføring];
            Minne_filsystem.skalere_Liste[Fil] = Fil_tabell[Fil * 72] == 0 ? 0 : tabell_heltall(Fil * 72 + 64);
            Minne_filsystem.허가들[Fil] = tabell_heltall(Fil * 72 + 68) & 511;
            for (int inndeling_VERDI = 0; inndeling_VERDI < 32; inndeling_VERDI++) {
                if (lagringsenhet_kontakt.Les(START_inndeling + 3 + Fil * 32 + inndeling_VERDI) < 0) return -5;
                int e_post = enhet_VERDI.Fil_Minne() + Fil * 16384 + inndeling_VERDI * 512;
                for (int åpning_oppføring = 0; åpning_oppføring < 512; åpning_oppføring++) enhet_VERDI.skrive_Minne(e_post + åpning_oppføring, lagringsenhet_kontakt.inndeling_data[åpning_oppføring]);
            }
        }
        return 0;
    }
    static void Forbered() {
        if (lagringsenhet_kontakt.Les(0) < 0 || lagringsenhet_kontakt.dele_opp_heltall(0) != 0x54534b4a
            || lagringsenhet_kontakt.dele_opp_heltall(4) != 0x3145524f || lagringsenhet_kontakt.dele_opp_heltall(8) != 2048
            || lagringsenhet_kontakt.dele_opp_heltall(12) != 0x3153464a) {
            SMS_Terminal.Skriv("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        lagringsenhet_kontakt.informasjonssystemer_Aktiv_9e72441a = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Terminal.Skriv("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (Belastning(현재보존본) < 0) {
            SMS_Terminal.Skriv("STORE read failed; halted to preserve files\n"); enhet_VERDI.정지();
        }
        SMS_Terminal.Skriv("STORE restored generation "); SMS_Terminal.skrive_nummer(세대번호); SMS_Terminal.문자(10);
    }
    static int synkronisere() {
        if (!lagringsenhet_kontakt.informasjonssystemer_Aktiv_9e72441a) return -19;
        if (세대번호 == 2147483647) return -75;
        int Neste_vare = 현재보존본 == 0 ? 1 : 0, START_inndeling = 1 + Neste_vare * 259;
        // 새 본문보다 먼저 Forrige_vare commit을 무효화하고 enhet_VERDI 캐시를 비운다.
        tømme_data();
        if (lagringsenhet_kontakt.Skriv(START_inndeling) < 0 || lagringsenhet_kontakt.밀어쓰기() < 0) return -5;
        for (int åpning_oppføring = 0; åpning_oppføring < 1024; åpning_oppføring++) Fil_tabell[åpning_oppføring] = 0;
        for (int Fil = 0; Fil < 8; Fil++) if (Minne_filsystem.이름들[Fil * 64] != 0) {
            for (int åpning_oppføring = 0; åpning_oppføring < 64; åpning_oppføring++) Fil_tabell[Fil * 72 + åpning_oppføring] = Minne_filsystem.이름들[Fil * 64 + åpning_oppføring];
            skrive_tabell_heltall(Fil * 72 + 64, Minne_filsystem.skalere_Liste[Fil]);
            skrive_tabell_heltall(Fil * 72 + 68, Minne_filsystem.허가들[Fil]);
        }
        int hash_Fil = 0x811c9dc5;
        for (int inndeling_VERDI = 0; inndeling_VERDI < 258; inndeling_VERDI++) {
            for (int åpning_oppføring = 0; åpning_oppføring < 512; åpning_oppføring++) {
                int VERDI = 0;
                if (inndeling_VERDI < 2) VERDI = Fil_tabell[inndeling_VERDI * 512 + åpning_oppføring];
                else {
                    int Fil = (inndeling_VERDI - 2) / 32, Posisjon = (inndeling_VERDI - 2) % 32 * 512 + åpning_oppføring;
                    if (Fil_tabell[Fil * 72] != 0 && Posisjon < Minne_filsystem.skalere_Liste[Fil])
                        VERDI = enhet_VERDI.기억읽기(enhet_VERDI.Fil_Minne() + Fil * 16384 + Posisjon);
                }
                lagringsenhet_kontakt.inndeling_data[åpning_oppføring] = VERDI; hash_Fil = 바이트해시(hash_Fil, VERDI);
            }
            if (lagringsenhet_kontakt.Skriv(START_inndeling + 1 + inndeling_VERDI) < 0) return -5;
        }
        if (lagringsenhet_kontakt.밀어쓰기() < 0) return -5;
        tømme_data(); lagringsenhet_kontakt.skrive_heltall_VERDI(0, 0x4a4b534e);
        lagringsenhet_kontakt.skrive_heltall_VERDI(4, 세대번호 + 1); lagringsenhet_kontakt.skrive_heltall_VERDI(8, hash_Fil);
        lagringsenhet_kontakt.skrive_heltall_VERDI(12, (세대번호 + 1) ^ hash_Fil ^ 0x4a4b534e);
        if (lagringsenhet_kontakt.Skriv(START_inndeling) < 0 || lagringsenhet_kontakt.밀어쓰기() < 0) return -5;
        현재보존본 = Neste_vare; 세대번호++;
        return 0;
    }
}
