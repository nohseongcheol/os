// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_HODNOTA formát_HODNOTA. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] Soubor_tabulka = new int[1024];
    static int 바이트해시(int HODNOTA, int data) { return (HODNOTA ^ data) * 16777619; }
    static void vymazat_data() {
        for (int INDEX = 0; INDEX < 512; INDEX++) úložiště_kontakt.oddíl_data[INDEX] = 0;
    }
    static int tabulka_integer(int pozice) {
        return Soubor_tabulka[pozice] | Soubor_tabulka[pozice + 1] << 8 | Soubor_tabulka[pozice + 2] << 16 | Soubor_tabulka[pozice + 3] << 24;
    }
    static void zápis_tabulka_integer(int pozice, int HODNOTA) {
        for (int INDEX = 0; INDEX < 4; INDEX++) Soubor_tabulka[pozice + INDEX] = (HODNOTA >>> (INDEX * 8)) & 255;
    }
    static boolean šek_tabulka() {
        for (int název_souboru = 0; název_souboru < 8; název_souboru++) {
            int délka_HODNOTA = 0;
            for (int přihrádka_položka = 0; přihrádka_položka < 64; přihrádka_položka++) Paměť_systém_souborů.Název[přihrádka_položka] = Soubor_tabulka[název_souboru * 72 + přihrádka_položka];
            while (délka_HODNOTA < 64 && Paměť_systém_souborů.Název[délka_HODNOTA] != 0) délka_HODNOTA++;
            if (délka_HODNOTA == 0) continue;
            if (!Paměť_systém_souborů.šek_název(Paměť_systém_souborů.Název, délka_HODNOTA)
                || tabulka_integer(název_souboru * 72 + 64) < 0 || tabulka_integer(název_souboru * 72 + 64) > 16384) return false;
            for (int přední_fotoaparát_HODNOTA = 0; přední_fotoaparát_HODNOTA < název_souboru; přední_fotoaparát_HODNOTA++) {
                boolean 같음 = Soubor_tabulka[přední_fotoaparát_HODNOTA * 72 + délka_HODNOTA] == 0;
                for (int přihrádka_položka = 0; přihrádka_položka < délka_HODNOTA; přihrádka_položka++) if (Soubor_tabulka[přední_fotoaparát_HODNOTA * 72 + přihrádka_položka] != Paměť_systém_souborů.Název[přihrádka_položka]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int START_oddíl = 1 + 보존본 * 259;
        if (úložiště_kontakt.Čtení(START_oddíl) < 0 || úložiště_kontakt.parsovat_integer(0) != 0x4a4b534e) return -1;
        int 세대 = úložiště_kontakt.parsovat_integer(4), kontrolní_součet = úložiště_kontakt.parsovat_integer(8);
        if (세대 < 1 || úložiště_kontakt.parsovat_integer(12) != (세대 ^ kontrolní_součet ^ 0x4a4b534e)) return -1;
        int hodnota_hash_Soubor = 0x811c9dc5;
        for (int oddíl_HODNOTA_366e0bfa = 0; oddíl_HODNOTA_366e0bfa < 258; oddíl_HODNOTA_366e0bfa++) {
            if (úložiště_kontakt.Čtení(START_oddíl + 1 + oddíl_HODNOTA_366e0bfa) < 0) return -1;
            for (int přihrádka_položka = 0; přihrádka_položka < 512; přihrádka_položka++) {
                int HODNOTA = úložiště_kontakt.oddíl_data[přihrádka_položka];
                hodnota_hash_Soubor = 바이트해시(hodnota_hash_Soubor, HODNOTA);
                if (oddíl_HODNOTA_366e0bfa < 2) Soubor_tabulka[oddíl_HODNOTA_366e0bfa * 512 + přihrádka_položka] = HODNOTA;
            }
        }
        return hodnota_hash_Soubor == kontrolní_součet && šek_tabulka() ? 세대 : -1;
    }
    static int Zátěž(int 보존본) {
        int START_oddíl = 1 + 보존본 * 259;
        for (int oddíl_HODNOTA_366e0bfa = 0; oddíl_HODNOTA_366e0bfa < 2; oddíl_HODNOTA_366e0bfa++) {
            if (úložiště_kontakt.Čtení(START_oddíl + 1 + oddíl_HODNOTA_366e0bfa) < 0) return -5;
            for (int přihrádka_položka = 0; přihrádka_položka < 512; přihrádka_položka++) Soubor_tabulka[oddíl_HODNOTA_366e0bfa * 512 + přihrádka_položka] = úložiště_kontakt.oddíl_data[přihrádka_položka];
        }
        for (int název_souboru = 0; název_souboru < 8; název_souboru++) {
            for (int přihrádka_položka = 0; přihrádka_položka < 64; přihrádka_položka++) Paměť_systém_souborů.이름들[název_souboru * 64 + přihrádka_položka] = Soubor_tabulka[název_souboru * 72 + přihrádka_položka];
            Paměť_systém_souborů.změnit_velikost_Seznam[název_souboru] = Soubor_tabulka[název_souboru * 72] == 0 ? 0 : tabulka_integer(název_souboru * 72 + 64);
            Paměť_systém_souborů.허가들[název_souboru] = tabulka_integer(název_souboru * 72 + 68) & 511;
            for (int oddíl_HODNOTA_366e0bfa = 0; oddíl_HODNOTA_366e0bfa < 32; oddíl_HODNOTA_366e0bfa++) {
                if (úložiště_kontakt.Čtení(START_oddíl + 3 + název_souboru * 32 + oddíl_HODNOTA_366e0bfa) < 0) return -5;
                int Adresa = mobilní_HODNOTA.Soubor_Paměť() + název_souboru * 16384 + oddíl_HODNOTA_366e0bfa * 512;
                for (int přihrádka_položka = 0; přihrádka_položka < 512; přihrádka_položka++) mobilní_HODNOTA.zápis_Paměť(Adresa + přihrádka_položka, úložiště_kontakt.oddíl_data[přihrádka_položka]);
            }
        }
        return 0;
    }
    static void Připravit() {
        if (úložiště_kontakt.Čtení(0) < 0 || úložiště_kontakt.parsovat_integer(0) != 0x54534b4a
            || úložiště_kontakt.parsovat_integer(4) != 0x3145524f || úložiště_kontakt.parsovat_integer(8) != 2048
            || úložiště_kontakt.parsovat_integer(12) != 0x3153464a) {
            SMS_Terminál.Zápis("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        úložiště_kontakt.informační_systémy_online = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Terminál.Zápis("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (Zátěž(현재보존본) < 0) {
            SMS_Terminál.Zápis("STORE read failed; halted to preserve files\n"); mobilní_HODNOTA.정지();
        }
        SMS_Terminál.Zápis("STORE restored generation "); SMS_Terminál.zápis_číslo(세대번호); SMS_Terminál.문자(10);
    }
    static int synchronizovat() {
        if (!úložiště_kontakt.informační_systémy_online) return -19;
        if (세대번호 == 2147483647) return -75;
        int Další_zboží = 현재보존본 == 0 ? 1 : 0, START_oddíl = 1 + Další_zboží * 259;
        // 새 본문보다 먼저 Předchozí_zboží commit을 무효화하고 mobilní_HODNOTA 캐시를 비운다.
        vymazat_data();
        if (úložiště_kontakt.Zápis(START_oddíl) < 0 || úložiště_kontakt.vyprázdnit_výstup() < 0) return -5;
        for (int přihrádka_položka = 0; přihrádka_položka < 1024; přihrádka_položka++) Soubor_tabulka[přihrádka_položka] = 0;
        for (int název_souboru = 0; název_souboru < 8; název_souboru++) if (Paměť_systém_souborů.이름들[název_souboru * 64] != 0) {
            for (int přihrádka_položka = 0; přihrádka_položka < 64; přihrádka_položka++) Soubor_tabulka[název_souboru * 72 + přihrádka_položka] = Paměť_systém_souborů.이름들[název_souboru * 64 + přihrádka_položka];
            zápis_tabulka_integer(název_souboru * 72 + 64, Paměť_systém_souborů.změnit_velikost_Seznam[název_souboru]);
            zápis_tabulka_integer(název_souboru * 72 + 68, Paměť_systém_souborů.허가들[název_souboru]);
        }
        int hodnota_hash_Soubor = 0x811c9dc5;
        for (int oddíl_HODNOTA_366e0bfa = 0; oddíl_HODNOTA_366e0bfa < 258; oddíl_HODNOTA_366e0bfa++) {
            for (int přihrádka_položka = 0; přihrádka_položka < 512; přihrádka_položka++) {
                int HODNOTA = 0;
                if (oddíl_HODNOTA_366e0bfa < 2) HODNOTA = Soubor_tabulka[oddíl_HODNOTA_366e0bfa * 512 + přihrádka_položka];
                else {
                    int název_souboru = (oddíl_HODNOTA_366e0bfa - 2) / 32, pozice = (oddíl_HODNOTA_366e0bfa - 2) % 32 * 512 + přihrádka_položka;
                    if (Soubor_tabulka[název_souboru * 72] != 0 && pozice < Paměť_systém_souborů.změnit_velikost_Seznam[název_souboru])
                        HODNOTA = mobilní_HODNOTA.기억읽기(mobilní_HODNOTA.Soubor_Paměť() + název_souboru * 16384 + pozice);
                }
                úložiště_kontakt.oddíl_data[přihrádka_položka] = HODNOTA; hodnota_hash_Soubor = 바이트해시(hodnota_hash_Soubor, HODNOTA);
            }
            if (úložiště_kontakt.Zápis(START_oddíl + 1 + oddíl_HODNOTA_366e0bfa) < 0) return -5;
        }
        if (úložiště_kontakt.vyprázdnit_výstup() < 0) return -5;
        vymazat_data(); úložiště_kontakt.zápis_integer_HODNOTA(0, 0x4a4b534e);
        úložiště_kontakt.zápis_integer_HODNOTA(4, 세대번호 + 1); úložiště_kontakt.zápis_integer_HODNOTA(8, hodnota_hash_Soubor);
        úložiště_kontakt.zápis_integer_HODNOTA(12, (세대번호 + 1) ^ hodnota_hash_Soubor ^ 0x4a4b534e);
        if (úložiště_kontakt.Zápis(START_oddíl) < 0 || úložiště_kontakt.vyprázdnit_výstup() < 0) return -5;
        현재보존본 = Další_zboží; 세대번호++;
        return 0;
    }
}
