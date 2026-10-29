// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_VALUE format_VALUE. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] Datoteka_tabela = new int[1024];
    static int 바이트해시(int VALUE, int podaci) { return (VALUE ^ podaci) * 16777619; }
    static void obrisati_podaci() {
        for (int INDEX = 0; INDEX < 512; INDEX++) uređaj_za_skladištenje_veza.odeljak_podaci[INDEX] = 0;
    }
    static int tabela_ceo_broj(int pozicija) {
        return Datoteka_tabela[pozicija] | Datoteka_tabela[pozicija + 1] << 8 | Datoteka_tabela[pozicija + 2] << 16 | Datoteka_tabela[pozicija + 3] << 24;
    }
    static void 표정수쓰기(int pozicija, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) Datoteka_tabela[pozicija + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
    static boolean proveriti_tabela() {
        for (int Datoteka = 0; Datoteka < 8; Datoteka++) {
            int 길이 = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) Memorija_sistem_datoteka.ime[칸] = Datoteka_tabela[Datoteka * 72 + 칸];
            while (길이 < 64 && Memorija_sistem_datoteka.ime[길이] != 0) 길이++;
            if (길이 == 0) continue;
            if (!Memorija_sistem_datoteka.proveriti_ime(Memorija_sistem_datoteka.ime, 길이)
                || tabela_ceo_broj(Datoteka * 72 + 64) < 0 || tabela_ceo_broj(Datoteka * 72 + 64) > 16384) return false;
            for (int čeona_kamera_VALUE = 0; čeona_kamera_VALUE < Datoteka; čeona_kamera_VALUE++) {
                boolean 같음 = Datoteka_tabela[čeona_kamera_VALUE * 72 + 길이] == 0;
                for (int 칸 = 0; 칸 < 길이; 칸++) if (Datoteka_tabela[čeona_kamera_VALUE * 72 + 칸] != Memorija_sistem_datoteka.ime[칸]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int START_odeljak = 1 + 보존본 * 259;
        if (uređaj_za_skladištenje_veza.읽기(START_odeljak) < 0 || uređaj_za_skladištenje_veza.raščlaniti_ceo_broj(0) != 0x4a4b534e) return -1;
        int 세대 = uređaj_za_skladištenje_veza.raščlaniti_ceo_broj(4), kontrolni_zbir = uređaj_za_skladištenje_veza.raščlaniti_ceo_broj(8);
        if (세대 < 1 || uređaj_za_skladištenje_veza.raščlaniti_ceo_broj(12) != (세대 ^ kontrolni_zbir ^ 0x4a4b534e)) return -1;
        int heš_Datoteka = 0x811c9dc5;
        for (int odeljak_VALUE = 0; odeljak_VALUE < 258; odeljak_VALUE++) {
            if (uređaj_za_skladištenje_veza.읽기(START_odeljak + 1 + odeljak_VALUE) < 0) return -1;
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int VALUE = uređaj_za_skladištenje_veza.odeljak_podaci[칸];
                heš_Datoteka = 바이트해시(heš_Datoteka, VALUE);
                if (odeljak_VALUE < 2) Datoteka_tabela[odeljak_VALUE * 512 + 칸] = VALUE;
            }
        }
        return heš_Datoteka == kontrolni_zbir && proveriti_tabela() ? 세대 : -1;
    }
    static int zbirka(int 보존본) {
        int START_odeljak = 1 + 보존본 * 259;
        for (int odeljak_VALUE = 0; odeljak_VALUE < 2; odeljak_VALUE++) {
            if (uređaj_za_skladištenje_veza.읽기(START_odeljak + 1 + odeljak_VALUE) < 0) return -5;
            for (int 칸 = 0; 칸 < 512; 칸++) Datoteka_tabela[odeljak_VALUE * 512 + 칸] = uređaj_za_skladištenje_veza.odeljak_podaci[칸];
        }
        for (int Datoteka = 0; Datoteka < 8; Datoteka++) {
            for (int 칸 = 0; 칸 < 64; 칸++) Memorija_sistem_datoteka.이름들[Datoteka * 64 + 칸] = Datoteka_tabela[Datoteka * 72 + 칸];
            Memorija_sistem_datoteka.promeniti_veličinu_Lista[Datoteka] = Datoteka_tabela[Datoteka * 72] == 0 ? 0 : tabela_ceo_broj(Datoteka * 72 + 64);
            Memorija_sistem_datoteka.허가들[Datoteka] = tabela_ceo_broj(Datoteka * 72 + 68) & 511;
            for (int odeljak_VALUE = 0; odeljak_VALUE < 32; odeljak_VALUE++) {
                if (uređaj_za_skladištenje_veza.읽기(START_odeljak + 3 + Datoteka * 32 + odeljak_VALUE) < 0) return -5;
                int adresa = uređaj_VALUE.Datoteka_Memorija() + Datoteka * 16384 + odeljak_VALUE * 512;
                for (int 칸 = 0; 칸 < 512; 칸++) uređaj_VALUE.기억쓰기(adresa + 칸, uređaj_za_skladištenje_veza.odeljak_podaci[칸]);
            }
        }
        return 0;
    }
    static void Pripremi() {
        if (uređaj_za_skladištenje_veza.읽기(0) < 0 || uređaj_za_skladištenje_veza.raščlaniti_ceo_broj(0) != 0x54534b4a
            || uređaj_za_skladištenje_veza.raščlaniti_ceo_broj(4) != 0x3145524f || uređaj_za_skladištenje_veza.raščlaniti_ceo_broj(8) != 2048
            || uređaj_za_skladištenje_veza.raščlaniti_ceo_broj(12) != 0x3153464a) {
            SMS_Terminal.쓰기("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        uređaj_za_skladištenje_veza.informatičko_odeljenje_Aktivan_9e72441a = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Terminal.쓰기("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (zbirka(현재보존본) < 0) {
            SMS_Terminal.쓰기("STORE read failed; halted to preserve files\n"); uređaj_VALUE.정지();
        }
        SMS_Terminal.쓰기("STORE restored generation "); SMS_Terminal.수쓰기(세대번호); SMS_Terminal.문자(10);
    }
    static int sinhronizovati() {
        if (!uređaj_za_skladištenje_veza.informatičko_odeljenje_Aktivan_9e72441a) return -19;
        if (세대번호 == 2147483647) return -75;
        int Dalje_stavka = 현재보존본 == 0 ? 1 : 0, START_odeljak = 1 + Dalje_stavka * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 uređaj_VALUE 캐시를 비운다.
        obrisati_podaci();
        if (uređaj_za_skladištenje_veza.쓰기(START_odeljak) < 0 || uređaj_za_skladištenje_veza.밀어쓰기() < 0) return -5;
        for (int 칸 = 0; 칸 < 1024; 칸++) Datoteka_tabela[칸] = 0;
        for (int Datoteka = 0; Datoteka < 8; Datoteka++) if (Memorija_sistem_datoteka.이름들[Datoteka * 64] != 0) {
            for (int 칸 = 0; 칸 < 64; 칸++) Datoteka_tabela[Datoteka * 72 + 칸] = Memorija_sistem_datoteka.이름들[Datoteka * 64 + 칸];
            표정수쓰기(Datoteka * 72 + 64, Memorija_sistem_datoteka.promeniti_veličinu_Lista[Datoteka]);
            표정수쓰기(Datoteka * 72 + 68, Memorija_sistem_datoteka.허가들[Datoteka]);
        }
        int heš_Datoteka = 0x811c9dc5;
        for (int odeljak_VALUE = 0; odeljak_VALUE < 258; odeljak_VALUE++) {
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int VALUE = 0;
                if (odeljak_VALUE < 2) VALUE = Datoteka_tabela[odeljak_VALUE * 512 + 칸];
                else {
                    int Datoteka = (odeljak_VALUE - 2) / 32, pozicija = (odeljak_VALUE - 2) % 32 * 512 + 칸;
                    if (Datoteka_tabela[Datoteka * 72] != 0 && pozicija < Memorija_sistem_datoteka.promeniti_veličinu_Lista[Datoteka])
                        VALUE = uređaj_VALUE.기억읽기(uređaj_VALUE.Datoteka_Memorija() + Datoteka * 16384 + pozicija);
                }
                uređaj_za_skladištenje_veza.odeljak_podaci[칸] = VALUE; heš_Datoteka = 바이트해시(heš_Datoteka, VALUE);
            }
            if (uređaj_za_skladištenje_veza.쓰기(START_odeljak + 1 + odeljak_VALUE) < 0) return -5;
        }
        if (uređaj_za_skladištenje_veza.밀어쓰기() < 0) return -5;
        obrisati_podaci(); uređaj_za_skladištenje_veza.정수쓰기(0, 0x4a4b534e);
        uređaj_za_skladištenje_veza.정수쓰기(4, 세대번호 + 1); uređaj_za_skladištenje_veza.정수쓰기(8, heš_Datoteka);
        uređaj_za_skladištenje_veza.정수쓰기(12, (세대번호 + 1) ^ heš_Datoteka ^ 0x4a4b534e);
        if (uređaj_za_skladištenje_veza.쓰기(START_odeljak) < 0 || uređaj_za_skladištenje_veza.밀어쓰기() < 0) return -5;
        현재보존본 = Dalje_stavka; 세대번호++;
        return 0;
    }
}
