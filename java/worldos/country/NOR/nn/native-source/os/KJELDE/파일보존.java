// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_VALUE format_VALUE. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] fil_tabell = new int[1024];
    static int 바이트해시(int VALUE, int data) { return (VALUE ^ data) * 16777619; }
    static void fjerne_data() {
        for (int INDEX = 0; INDEX < 512; INDEX++) Lagring_mobil_kontakt.del_data[INDEX] = 0;
    }
    static int tabell_heiltal(int Posisjon) {
        return fil_tabell[Posisjon] | fil_tabell[Posisjon + 1] << 8 | fil_tabell[Posisjon + 2] << 16 | fil_tabell[Posisjon + 3] << 24;
    }
    static void skrive_tabell_heiltal(int Posisjon, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) fil_tabell[Posisjon + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
    static boolean sjekk_tabell() {
        for (int Fil = 0; Fil < 8; Fil++) {
            int lengd_VALUE = 0;
            for (int felt_oppføring = 0; felt_oppføring < 64; felt_oppføring++) Minne_filsystem.Namn[felt_oppføring] = fil_tabell[Fil * 72 + felt_oppføring];
            while (lengd_VALUE < 64 && Minne_filsystem.Namn[lengd_VALUE] != 0) lengd_VALUE++;
            if (lengd_VALUE == 0) continue;
            if (!Minne_filsystem.sjekk_namn(Minne_filsystem.Namn, lengd_VALUE)
                || tabell_heiltal(Fil * 72 + 64) < 0 || tabell_heiltal(Fil * 72 + 64) > 16384) return false;
            for (int 앞 = 0; 앞 < Fil; 앞++) {
                boolean 같음 = fil_tabell[앞 * 72 + lengd_VALUE] == 0;
                for (int felt_oppføring = 0; felt_oppføring < lengd_VALUE; felt_oppføring++) if (fil_tabell[앞 * 72 + felt_oppføring] != Minne_filsystem.Namn[felt_oppføring]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int START_del = 1 + 보존본 * 259;
        if (Lagring_mobil_kontakt.Les(START_del) < 0 || Lagring_mobil_kontakt.dele_opp_heiltal(0) != 0x4a4b534e) return -1;
        int 세대 = Lagring_mobil_kontakt.dele_opp_heiltal(4), kontrollsum = Lagring_mobil_kontakt.dele_opp_heiltal(8);
        if (세대 < 1 || Lagring_mobil_kontakt.dele_opp_heiltal(12) != (세대 ^ kontrollsum ^ 0x4a4b534e)) return -1;
        int hash_fil = 0x811c9dc5;
        for (int del_VALUE = 0; del_VALUE < 258; del_VALUE++) {
            if (Lagring_mobil_kontakt.Les(START_del + 1 + del_VALUE) < 0) return -1;
            for (int felt_oppføring = 0; felt_oppføring < 512; felt_oppføring++) {
                int VALUE = Lagring_mobil_kontakt.del_data[felt_oppføring];
                hash_fil = 바이트해시(hash_fil, VALUE);
                if (del_VALUE < 2) fil_tabell[del_VALUE * 512 + felt_oppføring] = VALUE;
            }
        }
        return hash_fil == kontrollsum && sjekk_tabell() ? 세대 : -1;
    }
    static int Last(int 보존본) {
        int START_del = 1 + 보존본 * 259;
        for (int del_VALUE = 0; del_VALUE < 2; del_VALUE++) {
            if (Lagring_mobil_kontakt.Les(START_del + 1 + del_VALUE) < 0) return -5;
            for (int felt_oppføring = 0; felt_oppføring < 512; felt_oppføring++) fil_tabell[del_VALUE * 512 + felt_oppføring] = Lagring_mobil_kontakt.del_data[felt_oppføring];
        }
        for (int Fil = 0; Fil < 8; Fil++) {
            for (int felt_oppføring = 0; felt_oppføring < 64; felt_oppføring++) Minne_filsystem.이름들[Fil * 64 + felt_oppføring] = fil_tabell[Fil * 72 + felt_oppføring];
            Minne_filsystem.endre_storleik_Liste[Fil] = fil_tabell[Fil * 72] == 0 ? 0 : tabell_heiltal(Fil * 72 + 64);
            Minne_filsystem.허가들[Fil] = tabell_heiltal(Fil * 72 + 68) & 511;
            for (int del_VALUE = 0; del_VALUE < 32; del_VALUE++) {
                if (Lagring_mobil_kontakt.Les(START_del + 3 + Fil * 32 + del_VALUE) < 0) return -5;
                int ADDRESS = mobil_VALUE.fil_Minne() + Fil * 16384 + del_VALUE * 512;
                for (int felt_oppføring = 0; felt_oppføring < 512; felt_oppføring++) mobil_VALUE.skrive_Minne(ADDRESS + felt_oppføring, Lagring_mobil_kontakt.del_data[felt_oppføring]);
            }
        }
        return 0;
    }
    static void Klargjer() {
        if (Lagring_mobil_kontakt.Les(0) < 0 || Lagring_mobil_kontakt.dele_opp_heiltal(0) != 0x54534b4a
            || Lagring_mobil_kontakt.dele_opp_heiltal(4) != 0x3145524f || Lagring_mobil_kontakt.dele_opp_heiltal(8) != 2048
            || Lagring_mobil_kontakt.dele_opp_heiltal(12) != 0x3153464a) {
            SMS_Terminal.Skriv("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        Lagring_mobil_kontakt.informasjonsteknologi_barn = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Terminal.Skriv("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (Last(현재보존본) < 0) {
            SMS_Terminal.Skriv("STORE read failed; halted to preserve files\n"); mobil_VALUE.정지();
        }
        SMS_Terminal.Skriv("STORE restored generation "); SMS_Terminal.수쓰기(세대번호); SMS_Terminal.문자(10);
    }
    static int synkronisere() {
        if (!Lagring_mobil_kontakt.informasjonsteknologi_barn) return -19;
        if (세대번호 == 2147483647) return -75;
        int Neste_vare = 현재보존본 == 0 ? 1 : 0, START_del = 1 + Neste_vare * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 mobil_VALUE 캐시를 비운다.
        fjerne_data();
        if (Lagring_mobil_kontakt.Skriv(START_del) < 0 || Lagring_mobil_kontakt.밀어쓰기() < 0) return -5;
        for (int felt_oppføring = 0; felt_oppføring < 1024; felt_oppføring++) fil_tabell[felt_oppføring] = 0;
        for (int Fil = 0; Fil < 8; Fil++) if (Minne_filsystem.이름들[Fil * 64] != 0) {
            for (int felt_oppføring = 0; felt_oppføring < 64; felt_oppføring++) fil_tabell[Fil * 72 + felt_oppføring] = Minne_filsystem.이름들[Fil * 64 + felt_oppføring];
            skrive_tabell_heiltal(Fil * 72 + 64, Minne_filsystem.endre_storleik_Liste[Fil]);
            skrive_tabell_heiltal(Fil * 72 + 68, Minne_filsystem.허가들[Fil]);
        }
        int hash_fil = 0x811c9dc5;
        for (int del_VALUE = 0; del_VALUE < 258; del_VALUE++) {
            for (int felt_oppføring = 0; felt_oppføring < 512; felt_oppføring++) {
                int VALUE = 0;
                if (del_VALUE < 2) VALUE = fil_tabell[del_VALUE * 512 + felt_oppføring];
                else {
                    int Fil = (del_VALUE - 2) / 32, Posisjon = (del_VALUE - 2) % 32 * 512 + felt_oppføring;
                    if (fil_tabell[Fil * 72] != 0 && Posisjon < Minne_filsystem.endre_storleik_Liste[Fil])
                        VALUE = mobil_VALUE.기억읽기(mobil_VALUE.fil_Minne() + Fil * 16384 + Posisjon);
                }
                Lagring_mobil_kontakt.del_data[felt_oppføring] = VALUE; hash_fil = 바이트해시(hash_fil, VALUE);
            }
            if (Lagring_mobil_kontakt.Skriv(START_del + 1 + del_VALUE) < 0) return -5;
        }
        if (Lagring_mobil_kontakt.밀어쓰기() < 0) return -5;
        fjerne_data(); Lagring_mobil_kontakt.skrive_heiltal_VALUE(0, 0x4a4b534e);
        Lagring_mobil_kontakt.skrive_heiltal_VALUE(4, 세대번호 + 1); Lagring_mobil_kontakt.skrive_heiltal_VALUE(8, hash_fil);
        Lagring_mobil_kontakt.skrive_heiltal_VALUE(12, (세대번호 + 1) ^ hash_fil ^ 0x4a4b534e);
        if (Lagring_mobil_kontakt.Skriv(START_del) < 0 || Lagring_mobil_kontakt.밀어쓰기() < 0) return -5;
        현재보존본 = Neste_vare; 세대번호++;
        return 0;
    }
}
