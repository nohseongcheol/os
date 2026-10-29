// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 tár_ÉRTÉK formáz_ÉRTÉK. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] Fájl_tábla = new int[1024];
    static int 바이트해시(int ÉRTÉK, int adat) { return (ÉRTÉK ^ adat) * 16777619; }
    static void töröl_adat() {
        for (int INDEX = 0; INDEX < 512; INDEX++) tárolóeszköz_ismerős.szakasz_adat[INDEX] = 0;
    }
    static int tábla_egész_szám(int Pozíció) {
        return Fájl_tábla[Pozíció] | Fájl_tábla[Pozíció + 1] << 8 | Fájl_tábla[Pozíció + 2] << 16 | Fájl_tábla[Pozíció + 3] << 24;
    }
    static void ír_tábla_egész_szám(int Pozíció, int ÉRTÉK) {
        for (int INDEX = 0; INDEX < 4; INDEX++) Fájl_tábla[Pozíció + INDEX] = (ÉRTÉK >>> (INDEX * 8)) & 255;
    }
    static boolean csekk_tábla() {
        for (int Fájl = 0; Fájl < 8; Fájl++) {
            int hossz_ÉRTÉK = 0;
            for (int tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < 64; tárolóhely_bejegyzés++) Memória_fájlrendszer.Név[tárolóhely_bejegyzés] = Fájl_tábla[Fájl * 72 + tárolóhely_bejegyzés];
            while (hossz_ÉRTÉK < 64 && Memória_fájlrendszer.Név[hossz_ÉRTÉK] != 0) hossz_ÉRTÉK++;
            if (hossz_ÉRTÉK == 0) continue;
            if (!Memória_fájlrendszer.csekk_név(Memória_fájlrendszer.Név, hossz_ÉRTÉK)
                || tábla_egész_szám(Fájl * 72 + 64) < 0 || tábla_egész_szám(Fájl * 72 + 64) > 16384) return false;
            for (int elülső_kamera_ÉRTÉK = 0; elülső_kamera_ÉRTÉK < Fájl; elülső_kamera_ÉRTÉK++) {
                boolean 같음 = Fájl_tábla[elülső_kamera_ÉRTÉK * 72 + hossz_ÉRTÉK] == 0;
                for (int tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < hossz_ÉRTÉK; tárolóhely_bejegyzés++) if (Fájl_tábla[elülső_kamera_ÉRTÉK * 72 + tárolóhely_bejegyzés] != Memória_fájlrendszer.Név[tárolóhely_bejegyzés]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int START_szakasz = 1 + 보존본 * 259;
        if (tárolóeszköz_ismerős.Olvasás(START_szakasz) < 0 || tárolóeszköz_ismerős.elemez_egész_szám(0) != 0x4a4b534e) return -1;
        int 세대 = tárolóeszköz_ismerős.elemez_egész_szám(4), ellenőrzőösszeg = tárolóeszköz_ismerős.elemez_egész_szám(8);
        if (세대 < 1 || tárolóeszköz_ismerős.elemez_egész_szám(12) != (세대 ^ ellenőrzőösszeg ^ 0x4a4b534e)) return -1;
        int kivonat_Fájl = 0x811c9dc5;
        for (int szakasz_ÉRTÉK = 0; szakasz_ÉRTÉK < 258; szakasz_ÉRTÉK++) {
            if (tárolóeszköz_ismerős.Olvasás(START_szakasz + 1 + szakasz_ÉRTÉK) < 0) return -1;
            for (int tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < 512; tárolóhely_bejegyzés++) {
                int ÉRTÉK = tárolóeszköz_ismerős.szakasz_adat[tárolóhely_bejegyzés];
                kivonat_Fájl = 바이트해시(kivonat_Fájl, ÉRTÉK);
                if (szakasz_ÉRTÉK < 2) Fájl_tábla[szakasz_ÉRTÉK * 512 + tárolóhely_bejegyzés] = ÉRTÉK;
            }
        }
        return kivonat_Fájl == ellenőrzőösszeg && csekk_tábla() ? 세대 : -1;
    }
    static int Terhelés(int 보존본) {
        int START_szakasz = 1 + 보존본 * 259;
        for (int szakasz_ÉRTÉK = 0; szakasz_ÉRTÉK < 2; szakasz_ÉRTÉK++) {
            if (tárolóeszköz_ismerős.Olvasás(START_szakasz + 1 + szakasz_ÉRTÉK) < 0) return -5;
            for (int tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < 512; tárolóhely_bejegyzés++) Fájl_tábla[szakasz_ÉRTÉK * 512 + tárolóhely_bejegyzés] = tárolóeszköz_ismerős.szakasz_adat[tárolóhely_bejegyzés];
        }
        for (int Fájl = 0; Fájl < 8; Fájl++) {
            for (int tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < 64; tárolóhely_bejegyzés++) Memória_fájlrendszer.이름들[Fájl * 64 + tárolóhely_bejegyzés] = Fájl_tábla[Fájl * 72 + tárolóhely_bejegyzés];
            Memória_fájlrendszer.méretez_Lista[Fájl] = Fájl_tábla[Fájl * 72] == 0 ? 0 : tábla_egész_szám(Fájl * 72 + 64);
            Memória_fájlrendszer.허가들[Fájl] = tábla_egész_szám(Fájl * 72 + 68) & 511;
            for (int szakasz_ÉRTÉK = 0; szakasz_ÉRTÉK < 32; szakasz_ÉRTÉK++) {
                if (tárolóeszköz_ismerős.Olvasás(START_szakasz + 3 + Fájl * 32 + szakasz_ÉRTÉK) < 0) return -5;
                int CÍM = mobil_ÉRTÉK.Fájl_Memória() + Fájl * 16384 + szakasz_ÉRTÉK * 512;
                for (int tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < 512; tárolóhely_bejegyzés++) mobil_ÉRTÉK.ír_Memória(CÍM + tárolóhely_bejegyzés, tárolóeszköz_ismerős.szakasz_adat[tárolóhely_bejegyzés]);
            }
        }
        return 0;
    }
    static void Előkészítés() {
        if (tárolóeszköz_ismerős.Olvasás(0) < 0 || tárolóeszköz_ismerős.elemez_egész_szám(0) != 0x54534b4a
            || tárolóeszköz_ismerős.elemez_egész_szám(4) != 0x3145524f || tárolóeszköz_ismerős.elemez_egész_szám(8) != 2048
            || tárolóeszköz_ismerős.elemez_egész_szám(12) != 0x3153464a) {
            SMS_Terminál.Írás("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        tárolóeszköz_ismerős.informatikai_részleg_Aktív_9e72441a = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Terminál.Írás("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (Terhelés(현재보존본) < 0) {
            SMS_Terminál.Írás("STORE read failed; halted to preserve files\n"); mobil_ÉRTÉK.정지();
        }
        SMS_Terminál.Írás("STORE restored generation "); SMS_Terminál.ír_szám(세대번호); SMS_Terminál.문자(10);
    }
    static int szinkronizál() {
        if (!tárolóeszköz_ismerős.informatikai_részleg_Aktív_9e72441a) return -19;
        if (세대번호 == 2147483647) return -75;
        int Tovább_cikk = 현재보존본 == 0 ? 1 : 0, START_szakasz = 1 + Tovább_cikk * 259;
        // 새 본문보다 먼저 Előző_cikk commit을 무효화하고 mobil_ÉRTÉK 캐시를 비운다.
        töröl_adat();
        if (tárolóeszköz_ismerős.Írás(START_szakasz) < 0 || tárolóeszköz_ismerős.밀어쓰기() < 0) return -5;
        for (int tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < 1024; tárolóhely_bejegyzés++) Fájl_tábla[tárolóhely_bejegyzés] = 0;
        for (int Fájl = 0; Fájl < 8; Fájl++) if (Memória_fájlrendszer.이름들[Fájl * 64] != 0) {
            for (int tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < 64; tárolóhely_bejegyzés++) Fájl_tábla[Fájl * 72 + tárolóhely_bejegyzés] = Memória_fájlrendszer.이름들[Fájl * 64 + tárolóhely_bejegyzés];
            ír_tábla_egész_szám(Fájl * 72 + 64, Memória_fájlrendszer.méretez_Lista[Fájl]);
            ír_tábla_egész_szám(Fájl * 72 + 68, Memória_fájlrendszer.허가들[Fájl]);
        }
        int kivonat_Fájl = 0x811c9dc5;
        for (int szakasz_ÉRTÉK = 0; szakasz_ÉRTÉK < 258; szakasz_ÉRTÉK++) {
            for (int tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < 512; tárolóhely_bejegyzés++) {
                int ÉRTÉK = 0;
                if (szakasz_ÉRTÉK < 2) ÉRTÉK = Fájl_tábla[szakasz_ÉRTÉK * 512 + tárolóhely_bejegyzés];
                else {
                    int Fájl = (szakasz_ÉRTÉK - 2) / 32, Pozíció = (szakasz_ÉRTÉK - 2) % 32 * 512 + tárolóhely_bejegyzés;
                    if (Fájl_tábla[Fájl * 72] != 0 && Pozíció < Memória_fájlrendszer.méretez_Lista[Fájl])
                        ÉRTÉK = mobil_ÉRTÉK.기억읽기(mobil_ÉRTÉK.Fájl_Memória() + Fájl * 16384 + Pozíció);
                }
                tárolóeszköz_ismerős.szakasz_adat[tárolóhely_bejegyzés] = ÉRTÉK; kivonat_Fájl = 바이트해시(kivonat_Fájl, ÉRTÉK);
            }
            if (tárolóeszköz_ismerős.Írás(START_szakasz + 1 + szakasz_ÉRTÉK) < 0) return -5;
        }
        if (tárolóeszköz_ismerős.밀어쓰기() < 0) return -5;
        töröl_adat(); tárolóeszköz_ismerős.ír_egész_szám_ÉRTÉK(0, 0x4a4b534e);
        tárolóeszköz_ismerős.ír_egész_szám_ÉRTÉK(4, 세대번호 + 1); tárolóeszköz_ismerős.ír_egész_szám_ÉRTÉK(8, kivonat_Fájl);
        tárolóeszköz_ismerős.ír_egész_szám_ÉRTÉK(12, (세대번호 + 1) ^ kivonat_Fájl ^ 0x4a4b534e);
        if (tárolóeszköz_ismerős.Írás(START_szakasz) < 0 || tárolóeszköz_ismerős.밀어쓰기() < 0) return -5;
        현재보존본 = Tovább_cikk; 세대번호++;
        return 0;
    }
}
