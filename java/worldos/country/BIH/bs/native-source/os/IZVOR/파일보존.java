// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_VALUE format_VALUE. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] fajl_tabela = new int[1024];
    static int 바이트해시(int VALUE, int podaci) { return (VALUE ^ podaci) * 16777619; }
    static void obrisati_podaci() {
        for (int INDEX = 0; INDEX < 512; INDEX++) Pohrana_uređaj_veza.sekcija_podaci[INDEX] = 0;
    }
    static int tabela_cijeli_broj(int Pozicija) {
        return fajl_tabela[Pozicija] | fajl_tabela[Pozicija + 1] << 8 | fajl_tabela[Pozicija + 2] << 16 | fajl_tabela[Pozicija + 3] << 24;
    }
    static void pisati_tabela_cijeli_broj(int Pozicija, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) fajl_tabela[Pozicija + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
    static boolean ček_tabela() {
        for (int Fajl = 0; Fajl < 8; Fajl++) {
            int dužina_VALUE = 0;
            for (int prostor_za_unos_unos = 0; prostor_za_unos_unos < 64; prostor_za_unos_unos++) Memorija_fajl_sistem.Naziv[prostor_za_unos_unos] = fajl_tabela[Fajl * 72 + prostor_za_unos_unos];
            while (dužina_VALUE < 64 && Memorija_fajl_sistem.Naziv[dužina_VALUE] != 0) dužina_VALUE++;
            if (dužina_VALUE == 0) continue;
            if (!Memorija_fajl_sistem.ček_naziv(Memorija_fajl_sistem.Naziv, dužina_VALUE)
                || tabela_cijeli_broj(Fajl * 72 + 64) < 0 || tabela_cijeli_broj(Fajl * 72 + 64) > 16384) return false;
            for (int 앞 = 0; 앞 < Fajl; 앞++) {
                boolean 같음 = fajl_tabela[앞 * 72 + dužina_VALUE] == 0;
                for (int prostor_za_unos_unos = 0; prostor_za_unos_unos < dužina_VALUE; prostor_za_unos_unos++) if (fajl_tabela[앞 * 72 + prostor_za_unos_unos] != Memorija_fajl_sistem.Naziv[prostor_za_unos_unos]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int START_sekcija = 1 + 보존본 * 259;
        if (Pohrana_uređaj_veza.Čitaj(START_sekcija) < 0 || Pohrana_uređaj_veza.raščlanjivati_cijeli_broj(0) != 0x4a4b534e) return -1;
        int 세대 = Pohrana_uređaj_veza.raščlanjivati_cijeli_broj(4), kontrolni_zbir = Pohrana_uređaj_veza.raščlanjivati_cijeli_broj(8);
        if (세대 < 1 || Pohrana_uređaj_veza.raščlanjivati_cijeli_broj(12) != (세대 ^ kontrolni_zbir ^ 0x4a4b534e)) return -1;
        int raspršivanje_fajl = 0x811c9dc5;
        for (int sekcija_VALUE = 0; sekcija_VALUE < 258; sekcija_VALUE++) {
            if (Pohrana_uređaj_veza.Čitaj(START_sekcija + 1 + sekcija_VALUE) < 0) return -1;
            for (int prostor_za_unos_unos = 0; prostor_za_unos_unos < 512; prostor_za_unos_unos++) {
                int VALUE = Pohrana_uređaj_veza.sekcija_podaci[prostor_za_unos_unos];
                raspršivanje_fajl = 바이트해시(raspršivanje_fajl, VALUE);
                if (sekcija_VALUE < 2) fajl_tabela[sekcija_VALUE * 512 + prostor_za_unos_unos] = VALUE;
            }
        }
        return raspršivanje_fajl == kontrolni_zbir && ček_tabela() ? 세대 : -1;
    }
    static int Opterećenje(int 보존본) {
        int START_sekcija = 1 + 보존본 * 259;
        for (int sekcija_VALUE = 0; sekcija_VALUE < 2; sekcija_VALUE++) {
            if (Pohrana_uređaj_veza.Čitaj(START_sekcija + 1 + sekcija_VALUE) < 0) return -5;
            for (int prostor_za_unos_unos = 0; prostor_za_unos_unos < 512; prostor_za_unos_unos++) fajl_tabela[sekcija_VALUE * 512 + prostor_za_unos_unos] = Pohrana_uređaj_veza.sekcija_podaci[prostor_za_unos_unos];
        }
        for (int Fajl = 0; Fajl < 8; Fajl++) {
            for (int prostor_za_unos_unos = 0; prostor_za_unos_unos < 64; prostor_za_unos_unos++) Memorija_fajl_sistem.이름들[Fajl * 64 + prostor_za_unos_unos] = fajl_tabela[Fajl * 72 + prostor_za_unos_unos];
            Memorija_fajl_sistem.podesiti_veličinu_spisak[Fajl] = fajl_tabela[Fajl * 72] == 0 ? 0 : tabela_cijeli_broj(Fajl * 72 + 64);
            Memorija_fajl_sistem.허가들[Fajl] = tabela_cijeli_broj(Fajl * 72 + 68) & 511;
            for (int sekcija_VALUE = 0; sekcija_VALUE < 32; sekcija_VALUE++) {
                if (Pohrana_uređaj_veza.Čitaj(START_sekcija + 3 + Fajl * 32 + sekcija_VALUE) < 0) return -5;
                int adresa = uređaj_VALUE.fajl_Memorija() + Fajl * 16384 + sekcija_VALUE * 512;
                for (int prostor_za_unos_unos = 0; prostor_za_unos_unos < 512; prostor_za_unos_unos++) uređaj_VALUE.pisati_Memorija(adresa + prostor_za_unos_unos, Pohrana_uređaj_veza.sekcija_podaci[prostor_za_unos_unos]);
            }
        }
        return 0;
    }
    static void Pripremiti() {
        if (Pohrana_uređaj_veza.Čitaj(0) < 0 || Pohrana_uređaj_veza.raščlanjivati_cijeli_broj(0) != 0x54534b4a
            || Pohrana_uređaj_veza.raščlanjivati_cijeli_broj(4) != 0x3145524f || Pohrana_uređaj_veza.raščlanjivati_cijeli_broj(8) != 2048
            || Pohrana_uređaj_veza.raščlanjivati_cijeli_broj(12) != 0x3153464a) {
            SMS_Terminal.Piši("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        Pohrana_uređaj_veza.odjel_za_informacijske_tehnologije_dostupan = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Terminal.Piši("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (Opterećenje(현재보존본) < 0) {
            SMS_Terminal.Piši("STORE read failed; halted to preserve files\n"); uređaj_VALUE.정지();
        }
        SMS_Terminal.Piši("STORE restored generation "); SMS_Terminal.수쓰기(세대번호); SMS_Terminal.문자(10);
    }
    static int sinhronizirati() {
        if (!Pohrana_uređaj_veza.odjel_za_informacijske_tehnologije_dostupan) return -19;
        if (세대번호 == 2147483647) return -75;
        int Dalje_stavka = 현재보존본 == 0 ? 1 : 0, START_sekcija = 1 + Dalje_stavka * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 uređaj_VALUE 캐시를 비운다.
        obrisati_podaci();
        if (Pohrana_uređaj_veza.Piši(START_sekcija) < 0 || Pohrana_uređaj_veza.밀어쓰기() < 0) return -5;
        for (int prostor_za_unos_unos = 0; prostor_za_unos_unos < 1024; prostor_za_unos_unos++) fajl_tabela[prostor_za_unos_unos] = 0;
        for (int Fajl = 0; Fajl < 8; Fajl++) if (Memorija_fajl_sistem.이름들[Fajl * 64] != 0) {
            for (int prostor_za_unos_unos = 0; prostor_za_unos_unos < 64; prostor_za_unos_unos++) fajl_tabela[Fajl * 72 + prostor_za_unos_unos] = Memorija_fajl_sistem.이름들[Fajl * 64 + prostor_za_unos_unos];
            pisati_tabela_cijeli_broj(Fajl * 72 + 64, Memorija_fajl_sistem.podesiti_veličinu_spisak[Fajl]);
            pisati_tabela_cijeli_broj(Fajl * 72 + 68, Memorija_fajl_sistem.허가들[Fajl]);
        }
        int raspršivanje_fajl = 0x811c9dc5;
        for (int sekcija_VALUE = 0; sekcija_VALUE < 258; sekcija_VALUE++) {
            for (int prostor_za_unos_unos = 0; prostor_za_unos_unos < 512; prostor_za_unos_unos++) {
                int VALUE = 0;
                if (sekcija_VALUE < 2) VALUE = fajl_tabela[sekcija_VALUE * 512 + prostor_za_unos_unos];
                else {
                    int Fajl = (sekcija_VALUE - 2) / 32, Pozicija = (sekcija_VALUE - 2) % 32 * 512 + prostor_za_unos_unos;
                    if (fajl_tabela[Fajl * 72] != 0 && Pozicija < Memorija_fajl_sistem.podesiti_veličinu_spisak[Fajl])
                        VALUE = uređaj_VALUE.기억읽기(uređaj_VALUE.fajl_Memorija() + Fajl * 16384 + Pozicija);
                }
                Pohrana_uređaj_veza.sekcija_podaci[prostor_za_unos_unos] = VALUE; raspršivanje_fajl = 바이트해시(raspršivanje_fajl, VALUE);
            }
            if (Pohrana_uređaj_veza.Piši(START_sekcija + 1 + sekcija_VALUE) < 0) return -5;
        }
        if (Pohrana_uređaj_veza.밀어쓰기() < 0) return -5;
        obrisati_podaci(); Pohrana_uređaj_veza.pisati_cijeli_broj_VALUE(0, 0x4a4b534e);
        Pohrana_uređaj_veza.pisati_cijeli_broj_VALUE(4, 세대번호 + 1); Pohrana_uređaj_veza.pisati_cijeli_broj_VALUE(8, raspršivanje_fajl);
        Pohrana_uređaj_veza.pisati_cijeli_broj_VALUE(12, (세대번호 + 1) ^ raspršivanje_fajl ^ 0x4a4b534e);
        if (Pohrana_uređaj_veza.Piši(START_sekcija) < 0 || Pohrana_uređaj_veza.밀어쓰기() < 0) return -5;
        현재보존본 = Dalje_stavka; 세대번호++;
        return 0;
    }
}
