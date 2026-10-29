// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_VALUE formát_VALUE. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] Súbor_tabuľka = new int[1024];
    static int 바이트해시(int VALUE, int údaje) { return (VALUE ^ údaje) * 16777619; }
    static void vymazať_údaje() {
        for (int INDEX = 0; INDEX < 512; INDEX++) úložné_zariadenie_kontakt.sekcia_údaje[INDEX] = 0;
    }
    static int tabuľka_celé_číslo(int Pozícia) {
        return Súbor_tabuľka[Pozícia] | Súbor_tabuľka[Pozícia + 1] << 8 | Súbor_tabuľka[Pozícia + 2] << 16 | Súbor_tabuľka[Pozícia + 3] << 24;
    }
    static void zapísať_tabuľka_celé_číslo(int Pozícia, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) Súbor_tabuľka[Pozícia + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
    static boolean skontrolovať_tabuľka() {
        for (int Súbor = 0; Súbor < 8; Súbor++) {
            int dĺžka_VALUE = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) Pamäť_systém_súborov.Názov[칸] = Súbor_tabuľka[Súbor * 72 + 칸];
            while (dĺžka_VALUE < 64 && Pamäť_systém_súborov.Názov[dĺžka_VALUE] != 0) dĺžka_VALUE++;
            if (dĺžka_VALUE == 0) continue;
            if (!Pamäť_systém_súborov.skontrolovať_názov(Pamäť_systém_súborov.Názov, dĺžka_VALUE)
                || tabuľka_celé_číslo(Súbor * 72 + 64) < 0 || tabuľka_celé_číslo(Súbor * 72 + 64) > 16384) return false;
            for (int predný_VALUE = 0; predný_VALUE < Súbor; predný_VALUE++) {
                boolean 같음 = Súbor_tabuľka[predný_VALUE * 72 + dĺžka_VALUE] == 0;
                for (int 칸 = 0; 칸 < dĺžka_VALUE; 칸++) if (Súbor_tabuľka[predný_VALUE * 72 + 칸] != Pamäť_systém_súborov.Názov[칸]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int START_sekcia = 1 + 보존본 * 259;
        if (úložné_zariadenie_kontakt.Čítanie(START_sekcia) < 0 || úložné_zariadenie_kontakt.analyzovať_celé_číslo(0) != 0x4a4b534e) return -1;
        int 세대 = úložné_zariadenie_kontakt.analyzovať_celé_číslo(4), kontrolný_súčet = úložné_zariadenie_kontakt.analyzovať_celé_číslo(8);
        if (세대 < 1 || úložné_zariadenie_kontakt.analyzovať_celé_číslo(12) != (세대 ^ kontrolný_súčet ^ 0x4a4b534e)) return -1;
        int hodnota_hash_Súbor = 0x811c9dc5;
        for (int sekcia_VALUE = 0; sekcia_VALUE < 258; sekcia_VALUE++) {
            if (úložné_zariadenie_kontakt.Čítanie(START_sekcia + 1 + sekcia_VALUE) < 0) return -1;
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int VALUE = úložné_zariadenie_kontakt.sekcia_údaje[칸];
                hodnota_hash_Súbor = 바이트해시(hodnota_hash_Súbor, VALUE);
                if (sekcia_VALUE < 2) Súbor_tabuľka[sekcia_VALUE * 512 + 칸] = VALUE;
            }
        }
        return hodnota_hash_Súbor == kontrolný_súčet && skontrolovať_tabuľka() ? 세대 : -1;
    }
    static int Zaťaženie(int 보존본) {
        int START_sekcia = 1 + 보존본 * 259;
        for (int sekcia_VALUE = 0; sekcia_VALUE < 2; sekcia_VALUE++) {
            if (úložné_zariadenie_kontakt.Čítanie(START_sekcia + 1 + sekcia_VALUE) < 0) return -5;
            for (int 칸 = 0; 칸 < 512; 칸++) Súbor_tabuľka[sekcia_VALUE * 512 + 칸] = úložné_zariadenie_kontakt.sekcia_údaje[칸];
        }
        for (int Súbor = 0; Súbor < 8; Súbor++) {
            for (int 칸 = 0; 칸 < 64; 칸++) Pamäť_systém_súborov.이름들[Súbor * 64 + 칸] = Súbor_tabuľka[Súbor * 72 + 칸];
            Pamäť_systém_súborov.zmeniť_veľkosť_Zoznam[Súbor] = Súbor_tabuľka[Súbor * 72] == 0 ? 0 : tabuľka_celé_číslo(Súbor * 72 + 64);
            Pamäť_systém_súborov.허가들[Súbor] = tabuľka_celé_číslo(Súbor * 72 + 68) & 511;
            for (int sekcia_VALUE = 0; sekcia_VALUE < 32; sekcia_VALUE++) {
                if (úložné_zariadenie_kontakt.Čítanie(START_sekcia + 3 + Súbor * 32 + sekcia_VALUE) < 0) return -5;
                int adresa = telefón_VALUE.Súbor_Pamäť() + Súbor * 16384 + sekcia_VALUE * 512;
                for (int 칸 = 0; 칸 < 512; 칸++) telefón_VALUE.zapísať_Pamäť(adresa + 칸, úložné_zariadenie_kontakt.sekcia_údaje[칸]);
            }
        }
        return 0;
    }
    static void Pripraviť() {
        if (úložné_zariadenie_kontakt.Čítanie(0) < 0 || úložné_zariadenie_kontakt.analyzovať_celé_číslo(0) != 0x54534b4a
            || úložné_zariadenie_kontakt.analyzovať_celé_číslo(4) != 0x3145524f || úložné_zariadenie_kontakt.analyzovať_celé_číslo(8) != 2048
            || úložné_zariadenie_kontakt.analyzovať_celé_číslo(12) != 0x3153464a) {
            SMS_Terminál.Zápis("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        úložné_zariadenie_kontakt.Informačné_systémy_Aktívny_9e72441a = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Terminál.Zápis("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (Zaťaženie(현재보존본) < 0) {
            SMS_Terminál.Zápis("STORE read failed; halted to preserve files\n"); telefón_VALUE.정지();
        }
        SMS_Terminál.Zápis("STORE restored generation "); SMS_Terminál.수쓰기(세대번호); SMS_Terminál.문자(10);
    }
    static int synchronizovať() {
        if (!úložné_zariadenie_kontakt.Informačné_systémy_Aktívny_9e72441a) return -19;
        if (세대번호 == 2147483647) return -75;
        int Ďalej_položka = 현재보존본 == 0 ? 1 : 0, START_sekcia = 1 + Ďalej_položka * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 telefón_VALUE 캐시를 비운다.
        vymazať_údaje();
        if (úložné_zariadenie_kontakt.Zápis(START_sekcia) < 0 || úložné_zariadenie_kontakt.밀어쓰기() < 0) return -5;
        for (int 칸 = 0; 칸 < 1024; 칸++) Súbor_tabuľka[칸] = 0;
        for (int Súbor = 0; Súbor < 8; Súbor++) if (Pamäť_systém_súborov.이름들[Súbor * 64] != 0) {
            for (int 칸 = 0; 칸 < 64; 칸++) Súbor_tabuľka[Súbor * 72 + 칸] = Pamäť_systém_súborov.이름들[Súbor * 64 + 칸];
            zapísať_tabuľka_celé_číslo(Súbor * 72 + 64, Pamäť_systém_súborov.zmeniť_veľkosť_Zoznam[Súbor]);
            zapísať_tabuľka_celé_číslo(Súbor * 72 + 68, Pamäť_systém_súborov.허가들[Súbor]);
        }
        int hodnota_hash_Súbor = 0x811c9dc5;
        for (int sekcia_VALUE = 0; sekcia_VALUE < 258; sekcia_VALUE++) {
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int VALUE = 0;
                if (sekcia_VALUE < 2) VALUE = Súbor_tabuľka[sekcia_VALUE * 512 + 칸];
                else {
                    int Súbor = (sekcia_VALUE - 2) / 32, Pozícia = (sekcia_VALUE - 2) % 32 * 512 + 칸;
                    if (Súbor_tabuľka[Súbor * 72] != 0 && Pozícia < Pamäť_systém_súborov.zmeniť_veľkosť_Zoznam[Súbor])
                        VALUE = telefón_VALUE.기억읽기(telefón_VALUE.Súbor_Pamäť() + Súbor * 16384 + Pozícia);
                }
                úložné_zariadenie_kontakt.sekcia_údaje[칸] = VALUE; hodnota_hash_Súbor = 바이트해시(hodnota_hash_Súbor, VALUE);
            }
            if (úložné_zariadenie_kontakt.Zápis(START_sekcia + 1 + sekcia_VALUE) < 0) return -5;
        }
        if (úložné_zariadenie_kontakt.밀어쓰기() < 0) return -5;
        vymazať_údaje(); úložné_zariadenie_kontakt.zapísať_celé_číslo_VALUE(0, 0x4a4b534e);
        úložné_zariadenie_kontakt.zapísať_celé_číslo_VALUE(4, 세대번호 + 1); úložné_zariadenie_kontakt.zapísať_celé_číslo_VALUE(8, hodnota_hash_Súbor);
        úložné_zariadenie_kontakt.zapísať_celé_číslo_VALUE(12, (세대번호 + 1) ^ hodnota_hash_Súbor ^ 0x4a4b534e);
        if (úložné_zariadenie_kontakt.Zápis(START_sekcia) < 0 || úložné_zariadenie_kontakt.밀어쓰기() < 0) return -5;
        현재보존본 = Ďalej_položka; 세대번호++;
        return 0;
    }
}
