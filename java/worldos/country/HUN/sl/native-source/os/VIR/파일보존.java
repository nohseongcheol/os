// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_VALUE oblika_VALUE. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] Datoteka_tabela = new int[1024];
    static int 바이트해시(int VALUE, int podatki) { return (VALUE ^ podatki) * 16777619; }
    static void počistiti_podatki() {
        for (int INDEX = 0; INDEX < 512; INDEX++) naprava_za_shranjevanje_povezava.odsek_podatki[INDEX] = 0;
    }
    static int tabela_celo_število(int Položaj) {
        return Datoteka_tabela[Položaj] | Datoteka_tabela[Položaj + 1] << 8 | Datoteka_tabela[Položaj + 2] << 16 | Datoteka_tabela[Položaj + 3] << 24;
    }
    static void pisati_tabela_celo_število(int Položaj, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) Datoteka_tabela[Položaj + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
    static boolean preveriti_tabela() {
        for (int Datoteka = 0; Datoteka < 8; Datoteka++) {
            int 길이 = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) pomnilnik_datotečni_sistem.Ime[칸] = Datoteka_tabela[Datoteka * 72 + 칸];
            while (길이 < 64 && pomnilnik_datotečni_sistem.Ime[길이] != 0) 길이++;
            if (길이 == 0) continue;
            if (!pomnilnik_datotečni_sistem.preveriti_ime(pomnilnik_datotečni_sistem.Ime, 길이)
                || tabela_celo_število(Datoteka * 72 + 64) < 0 || tabela_celo_število(Datoteka * 72 + 64) > 16384) return false;
            for (int sprednja_VALUE = 0; sprednja_VALUE < Datoteka; sprednja_VALUE++) {
                boolean 같음 = Datoteka_tabela[sprednja_VALUE * 72 + 길이] == 0;
                for (int 칸 = 0; 칸 < 길이; 칸++) if (Datoteka_tabela[sprednja_VALUE * 72 + 칸] != pomnilnik_datotečni_sistem.Ime[칸]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int Start_odsek = 1 + 보존본 * 259;
        if (naprava_za_shranjevanje_povezava.Branje(Start_odsek) < 0 || naprava_za_shranjevanje_povezava.razčlenjevati_celo_število(0) != 0x4a4b534e) return -1;
        int 세대 = naprava_za_shranjevanje_povezava.razčlenjevati_celo_število(4), kontrolna_vsota = naprava_za_shranjevanje_povezava.razčlenjevati_celo_število(8);
        if (세대 < 1 || naprava_za_shranjevanje_povezava.razčlenjevati_celo_število(12) != (세대 ^ kontrolna_vsota ^ 0x4a4b534e)) return -1;
        int zgoščena_vrednost_Datoteka = 0x811c9dc5;
        for (int odsek_VALUE = 0; odsek_VALUE < 258; odsek_VALUE++) {
            if (naprava_za_shranjevanje_povezava.Branje(Start_odsek + 1 + odsek_VALUE) < 0) return -1;
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int VALUE = naprava_za_shranjevanje_povezava.odsek_podatki[칸];
                zgoščena_vrednost_Datoteka = 바이트해시(zgoščena_vrednost_Datoteka, VALUE);
                if (odsek_VALUE < 2) Datoteka_tabela[odsek_VALUE * 512 + 칸] = VALUE;
            }
        }
        return zgoščena_vrednost_Datoteka == kontrolna_vsota && preveriti_tabela() ? 세대 : -1;
    }
    static int Obremenjenost(int 보존본) {
        int Start_odsek = 1 + 보존본 * 259;
        for (int odsek_VALUE = 0; odsek_VALUE < 2; odsek_VALUE++) {
            if (naprava_za_shranjevanje_povezava.Branje(Start_odsek + 1 + odsek_VALUE) < 0) return -5;
            for (int 칸 = 0; 칸 < 512; 칸++) Datoteka_tabela[odsek_VALUE * 512 + 칸] = naprava_za_shranjevanje_povezava.odsek_podatki[칸];
        }
        for (int Datoteka = 0; Datoteka < 8; Datoteka++) {
            for (int 칸 = 0; 칸 < 64; 칸++) pomnilnik_datotečni_sistem.이름들[Datoteka * 64 + 칸] = Datoteka_tabela[Datoteka * 72 + 칸];
            pomnilnik_datotečni_sistem.spremeniti_velikost_Seznam[Datoteka] = Datoteka_tabela[Datoteka * 72] == 0 ? 0 : tabela_celo_število(Datoteka * 72 + 64);
            pomnilnik_datotečni_sistem.허가들[Datoteka] = tabela_celo_število(Datoteka * 72 + 68) & 511;
            for (int odsek_VALUE = 0; odsek_VALUE < 32; odsek_VALUE++) {
                if (naprava_za_shranjevanje_povezava.Branje(Start_odsek + 3 + Datoteka * 32 + odsek_VALUE) < 0) return -5;
                int naslov = naprava_VALUE.Datoteka_pomnilnik() + Datoteka * 16384 + odsek_VALUE * 512;
                for (int 칸 = 0; 칸 < 512; 칸++) naprava_VALUE.pisati_pomnilnik(naslov + 칸, naprava_za_shranjevanje_povezava.odsek_podatki[칸]);
            }
        }
        return 0;
    }
    static void Pripravi() {
        if (naprava_za_shranjevanje_povezava.Branje(0) < 0 || naprava_za_shranjevanje_povezava.razčlenjevati_celo_število(0) != 0x54534b4a
            || naprava_za_shranjevanje_povezava.razčlenjevati_celo_število(4) != 0x3145524f || naprava_za_shranjevanje_povezava.razčlenjevati_celo_število(8) != 2048
            || naprava_za_shranjevanje_povezava.razčlenjevati_celo_število(12) != 0x3153464a) {
            SMS_Terminal.Pisanje("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        naprava_za_shranjevanje_povezava.informacijska_tehnologija_Dejaven_9e72441a = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Terminal.Pisanje("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (Obremenjenost(현재보존본) < 0) {
            SMS_Terminal.Pisanje("STORE read failed; halted to preserve files\n"); naprava_VALUE.정지();
        }
        SMS_Terminal.Pisanje("STORE restored generation "); SMS_Terminal.수쓰기(세대번호); SMS_Terminal.문자(10);
    }
    static int sinhronizirati() {
        if (!naprava_za_shranjevanje_povezava.informacijska_tehnologija_Dejaven_9e72441a) return -19;
        if (세대번호 == 2147483647) return -75;
        int Naprej_element = 현재보존본 == 0 ? 1 : 0, Start_odsek = 1 + Naprej_element * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 naprava_VALUE 캐시를 비운다.
        počistiti_podatki();
        if (naprava_za_shranjevanje_povezava.Pisanje(Start_odsek) < 0 || naprava_za_shranjevanje_povezava.밀어쓰기() < 0) return -5;
        for (int 칸 = 0; 칸 < 1024; 칸++) Datoteka_tabela[칸] = 0;
        for (int Datoteka = 0; Datoteka < 8; Datoteka++) if (pomnilnik_datotečni_sistem.이름들[Datoteka * 64] != 0) {
            for (int 칸 = 0; 칸 < 64; 칸++) Datoteka_tabela[Datoteka * 72 + 칸] = pomnilnik_datotečni_sistem.이름들[Datoteka * 64 + 칸];
            pisati_tabela_celo_število(Datoteka * 72 + 64, pomnilnik_datotečni_sistem.spremeniti_velikost_Seznam[Datoteka]);
            pisati_tabela_celo_število(Datoteka * 72 + 68, pomnilnik_datotečni_sistem.허가들[Datoteka]);
        }
        int zgoščena_vrednost_Datoteka = 0x811c9dc5;
        for (int odsek_VALUE = 0; odsek_VALUE < 258; odsek_VALUE++) {
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int VALUE = 0;
                if (odsek_VALUE < 2) VALUE = Datoteka_tabela[odsek_VALUE * 512 + 칸];
                else {
                    int Datoteka = (odsek_VALUE - 2) / 32, Položaj = (odsek_VALUE - 2) % 32 * 512 + 칸;
                    if (Datoteka_tabela[Datoteka * 72] != 0 && Položaj < pomnilnik_datotečni_sistem.spremeniti_velikost_Seznam[Datoteka])
                        VALUE = naprava_VALUE.기억읽기(naprava_VALUE.Datoteka_pomnilnik() + Datoteka * 16384 + Položaj);
                }
                naprava_za_shranjevanje_povezava.odsek_podatki[칸] = VALUE; zgoščena_vrednost_Datoteka = 바이트해시(zgoščena_vrednost_Datoteka, VALUE);
            }
            if (naprava_za_shranjevanje_povezava.Pisanje(Start_odsek + 1 + odsek_VALUE) < 0) return -5;
        }
        if (naprava_za_shranjevanje_povezava.밀어쓰기() < 0) return -5;
        počistiti_podatki(); naprava_za_shranjevanje_povezava.pisati_celo_število_VALUE(0, 0x4a4b534e);
        naprava_za_shranjevanje_povezava.pisati_celo_število_VALUE(4, 세대번호 + 1); naprava_za_shranjevanje_povezava.pisati_celo_število_VALUE(8, zgoščena_vrednost_Datoteka);
        naprava_za_shranjevanje_povezava.pisati_celo_število_VALUE(12, (세대번호 + 1) ^ zgoščena_vrednost_Datoteka ^ 0x4a4b534e);
        if (naprava_za_shranjevanje_povezava.Pisanje(Start_odsek) < 0 || naprava_za_shranjevanje_povezava.밀어쓰기() < 0) return -5;
        현재보존본 = Naprej_element; 세대번호++;
        return 0;
    }
}
