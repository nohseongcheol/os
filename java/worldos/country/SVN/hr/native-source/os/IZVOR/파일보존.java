// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_VALUE oblik_VALUE. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] Datoteka_tablica = new int[1024];
    static int 바이트해시(int VALUE, int podaci) { return (VALUE ^ podaci) * 16777619; }
    static void očistiti_podaci() {
        for (int INDEX = 0; INDEX < 512; INDEX++) uređaj_za_pohranu_veza.sekcija_podaci[INDEX] = 0;
    }
    static int tablica_cijeli_broj(int Položaj) {
        return Datoteka_tablica[Položaj] | Datoteka_tablica[Položaj + 1] << 8 | Datoteka_tablica[Položaj + 2] << 16 | Datoteka_tablica[Položaj + 3] << 24;
    }
    static void zapisivanje_tablica_cijeli_broj(int Položaj, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) Datoteka_tablica[Položaj + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
    static boolean 표검사() {
        for (int Datoteka = 0; Datoteka < 8; Datoteka++) {
            int 길이 = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) Memorija_datotečni_sustav.Ime[칸] = Datoteka_tablica[Datoteka * 72 + 칸];
            while (길이 < 64 && Memorija_datotečni_sustav.Ime[길이] != 0) 길이++;
            if (길이 == 0) continue;
            if (!Memorija_datotečni_sustav.이름검사(Memorija_datotečni_sustav.Ime, 길이)
                || tablica_cijeli_broj(Datoteka * 72 + 64) < 0 || tablica_cijeli_broj(Datoteka * 72 + 64) > 16384) return false;
            for (int prednja_VALUE = 0; prednja_VALUE < Datoteka; prednja_VALUE++) {
                boolean 같음 = Datoteka_tablica[prednja_VALUE * 72 + 길이] == 0;
                for (int 칸 = 0; 칸 < 길이; 칸++) if (Datoteka_tablica[prednja_VALUE * 72 + 칸] != Memorija_datotečni_sustav.Ime[칸]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int START_sekcija = 1 + 보존본 * 259;
        if (uređaj_za_pohranu_veza.Čitaj(START_sekcija) < 0 || uređaj_za_pohranu_veza.rastavljati_cijeli_broj(0) != 0x4a4b534e) return -1;
        int 세대 = uređaj_za_pohranu_veza.rastavljati_cijeli_broj(4), kontrolni_zbroj = uređaj_za_pohranu_veza.rastavljati_cijeli_broj(8);
        if (세대 < 1 || uređaj_za_pohranu_veza.rastavljati_cijeli_broj(12) != (세대 ^ kontrolni_zbroj ^ 0x4a4b534e)) return -1;
        int raspršivanje_Datoteka = 0x811c9dc5;
        for (int sekcija_VALUE = 0; sekcija_VALUE < 258; sekcija_VALUE++) {
            if (uređaj_za_pohranu_veza.Čitaj(START_sekcija + 1 + sekcija_VALUE) < 0) return -1;
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int VALUE = uređaj_za_pohranu_veza.sekcija_podaci[칸];
                raspršivanje_Datoteka = 바이트해시(raspršivanje_Datoteka, VALUE);
                if (sekcija_VALUE < 2) Datoteka_tablica[sekcija_VALUE * 512 + 칸] = VALUE;
            }
        }
        return raspršivanje_Datoteka == kontrolni_zbroj && 표검사() ? 세대 : -1;
    }
    static int Opterečenje(int 보존본) {
        int START_sekcija = 1 + 보존본 * 259;
        for (int sekcija_VALUE = 0; sekcija_VALUE < 2; sekcija_VALUE++) {
            if (uređaj_za_pohranu_veza.Čitaj(START_sekcija + 1 + sekcija_VALUE) < 0) return -5;
            for (int 칸 = 0; 칸 < 512; 칸++) Datoteka_tablica[sekcija_VALUE * 512 + 칸] = uređaj_za_pohranu_veza.sekcija_podaci[칸];
        }
        for (int Datoteka = 0; Datoteka < 8; Datoteka++) {
            for (int 칸 = 0; 칸 < 64; 칸++) Memorija_datotečni_sustav.이름들[Datoteka * 64 + 칸] = Datoteka_tablica[Datoteka * 72 + 칸];
            Memorija_datotečni_sustav.promijeniti_veličinu_Popis[Datoteka] = Datoteka_tablica[Datoteka * 72] == 0 ? 0 : tablica_cijeli_broj(Datoteka * 72 + 64);
            Memorija_datotečni_sustav.허가들[Datoteka] = tablica_cijeli_broj(Datoteka * 72 + 68) & 511;
            for (int sekcija_VALUE = 0; sekcija_VALUE < 32; sekcija_VALUE++) {
                if (uređaj_za_pohranu_veza.Čitaj(START_sekcija + 3 + Datoteka * 32 + sekcija_VALUE) < 0) return -5;
                int adresa = uređaj_VALUE.Datoteka_Memorija() + Datoteka * 16384 + sekcija_VALUE * 512;
                for (int 칸 = 0; 칸 < 512; 칸++) uređaj_VALUE.zapisivanje_Memorija(adresa + 칸, uređaj_za_pohranu_veza.sekcija_podaci[칸]);
            }
        }
        return 0;
    }
    static void Pripremi() {
        if (uređaj_za_pohranu_veza.Čitaj(0) < 0 || uređaj_za_pohranu_veza.rastavljati_cijeli_broj(0) != 0x54534b4a
            || uređaj_za_pohranu_veza.rastavljati_cijeli_broj(4) != 0x3145524f || uređaj_za_pohranu_veza.rastavljati_cijeli_broj(8) != 2048
            || uređaj_za_pohranu_veza.rastavljati_cijeli_broj(12) != 0x3153464a) {
            SMS_Terminal.Zapisuj("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        uređaj_za_pohranu_veza.odjel_informacijske_tehnologije_Aktivan_9e72441a = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Terminal.Zapisuj("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (Opterečenje(현재보존본) < 0) {
            SMS_Terminal.Zapisuj("STORE read failed; halted to preserve files\n"); uređaj_VALUE.정지();
        }
        SMS_Terminal.Zapisuj("STORE restored generation "); SMS_Terminal.수쓰기(세대번호); SMS_Terminal.문자(10);
    }
    static int sinkronizacija() {
        if (!uređaj_za_pohranu_veza.odjel_informacijske_tehnologije_Aktivan_9e72441a) return -19;
        if (세대번호 == 2147483647) return -75;
        int Dalje_artikl = 현재보존본 == 0 ? 1 : 0, START_sekcija = 1 + Dalje_artikl * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 uređaj_VALUE 캐시를 비운다.
        očistiti_podaci();
        if (uređaj_za_pohranu_veza.Zapisuj(START_sekcija) < 0 || uređaj_za_pohranu_veza.밀어쓰기() < 0) return -5;
        for (int 칸 = 0; 칸 < 1024; 칸++) Datoteka_tablica[칸] = 0;
        for (int Datoteka = 0; Datoteka < 8; Datoteka++) if (Memorija_datotečni_sustav.이름들[Datoteka * 64] != 0) {
            for (int 칸 = 0; 칸 < 64; 칸++) Datoteka_tablica[Datoteka * 72 + 칸] = Memorija_datotečni_sustav.이름들[Datoteka * 64 + 칸];
            zapisivanje_tablica_cijeli_broj(Datoteka * 72 + 64, Memorija_datotečni_sustav.promijeniti_veličinu_Popis[Datoteka]);
            zapisivanje_tablica_cijeli_broj(Datoteka * 72 + 68, Memorija_datotečni_sustav.허가들[Datoteka]);
        }
        int raspršivanje_Datoteka = 0x811c9dc5;
        for (int sekcija_VALUE = 0; sekcija_VALUE < 258; sekcija_VALUE++) {
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int VALUE = 0;
                if (sekcija_VALUE < 2) VALUE = Datoteka_tablica[sekcija_VALUE * 512 + 칸];
                else {
                    int Datoteka = (sekcija_VALUE - 2) / 32, Položaj = (sekcija_VALUE - 2) % 32 * 512 + 칸;
                    if (Datoteka_tablica[Datoteka * 72] != 0 && Položaj < Memorija_datotečni_sustav.promijeniti_veličinu_Popis[Datoteka])
                        VALUE = uređaj_VALUE.기억읽기(uređaj_VALUE.Datoteka_Memorija() + Datoteka * 16384 + Položaj);
                }
                uređaj_za_pohranu_veza.sekcija_podaci[칸] = VALUE; raspršivanje_Datoteka = 바이트해시(raspršivanje_Datoteka, VALUE);
            }
            if (uređaj_za_pohranu_veza.Zapisuj(START_sekcija + 1 + sekcija_VALUE) < 0) return -5;
        }
        if (uređaj_za_pohranu_veza.밀어쓰기() < 0) return -5;
        očistiti_podaci(); uređaj_za_pohranu_veza.zapisivanje_cijeli_broj_VALUE(0, 0x4a4b534e);
        uređaj_za_pohranu_veza.zapisivanje_cijeli_broj_VALUE(4, 세대번호 + 1); uređaj_za_pohranu_veza.zapisivanje_cijeli_broj_VALUE(8, raspršivanje_Datoteka);
        uređaj_za_pohranu_veza.zapisivanje_cijeli_broj_VALUE(12, (세대번호 + 1) ^ raspršivanje_Datoteka ^ 0x4a4b534e);
        if (uređaj_za_pohranu_veza.Zapisuj(START_sekcija) < 0 || uređaj_za_pohranu_veza.밀어쓰기() < 0) return -5;
        현재보존본 = Dalje_artikl; 세대번호++;
        return 0;
    }
}
