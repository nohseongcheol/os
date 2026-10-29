// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_VALUE formatas_VALUE. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] Failas_lentelė = new int[1024];
    static int 바이트해시(int VALUE, int duomenys) { return (VALUE ^ duomenys) * 16777619; }
    static void apmokėti_duomenys() {
        for (int INDEX = 0; INDEX < 512; INDEX++) saugojimo_įrenginys_ryšys.sekcija_duomenys[INDEX] = 0;
    }
    static int lentelė_sveikasis_skaičius(int Pozicija) {
        return Failas_lentelė[Pozicija] | Failas_lentelė[Pozicija + 1] << 8 | Failas_lentelė[Pozicija + 2] << 16 | Failas_lentelė[Pozicija + 3] << 24;
    }
    static void rašymas_lentelė_sveikasis_skaičius(int Pozicija, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) Failas_lentelė[Pozicija + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
    static boolean čekis_lentelė() {
        for (int Failas = 0; Failas < 8; Failas++) {
            int 길이 = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) atmintis_failų_sistema.Pavadinimas_2[칸] = Failas_lentelė[Failas * 72 + 칸];
            while (길이 < 64 && atmintis_failų_sistema.Pavadinimas_2[길이] != 0) 길이++;
            if (길이 == 0) continue;
            if (!atmintis_failų_sistema.čekis_pavadinimas(atmintis_failų_sistema.Pavadinimas_2, 길이)
                || lentelė_sveikasis_skaičius(Failas * 72 + 64) < 0 || lentelė_sveikasis_skaičius(Failas * 72 + 64) > 16384) return false;
            for (int priekinis_VALUE = 0; priekinis_VALUE < Failas; priekinis_VALUE++) {
                boolean 같음 = Failas_lentelė[priekinis_VALUE * 72 + 길이] == 0;
                for (int 칸 = 0; 칸 < 길이; 칸++) if (Failas_lentelė[priekinis_VALUE * 72 + 칸] != atmintis_failų_sistema.Pavadinimas_2[칸]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int Start_sekcija = 1 + 보존본 * 259;
        if (saugojimo_įrenginys_ryšys.Skaitymas(Start_sekcija) < 0 || saugojimo_įrenginys_ryšys.analizuoti_sintaksę_sveikasis_skaičius(0) != 0x4a4b534e) return -1;
        int 세대 = saugojimo_įrenginys_ryšys.analizuoti_sintaksę_sveikasis_skaičius(4), kontrolinė_suma = saugojimo_įrenginys_ryšys.analizuoti_sintaksę_sveikasis_skaičius(8);
        if (세대 < 1 || saugojimo_įrenginys_ryšys.analizuoti_sintaksę_sveikasis_skaičius(12) != (세대 ^ kontrolinė_suma ^ 0x4a4b534e)) return -1;
        int maiša_Failas = 0x811c9dc5;
        for (int sekcija_VALUE = 0; sekcija_VALUE < 258; sekcija_VALUE++) {
            if (saugojimo_įrenginys_ryšys.Skaitymas(Start_sekcija + 1 + sekcija_VALUE) < 0) return -1;
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int VALUE = saugojimo_įrenginys_ryšys.sekcija_duomenys[칸];
                maiša_Failas = 바이트해시(maiša_Failas, VALUE);
                if (sekcija_VALUE < 2) Failas_lentelė[sekcija_VALUE * 512 + 칸] = VALUE;
            }
        }
        return maiša_Failas == kontrolinė_suma && čekis_lentelė() ? 세대 : -1;
    }
    static int Apkrova(int 보존본) {
        int Start_sekcija = 1 + 보존본 * 259;
        for (int sekcija_VALUE = 0; sekcija_VALUE < 2; sekcija_VALUE++) {
            if (saugojimo_įrenginys_ryšys.Skaitymas(Start_sekcija + 1 + sekcija_VALUE) < 0) return -5;
            for (int 칸 = 0; 칸 < 512; 칸++) Failas_lentelė[sekcija_VALUE * 512 + 칸] = saugojimo_įrenginys_ryšys.sekcija_duomenys[칸];
        }
        for (int Failas = 0; Failas < 8; Failas++) {
            for (int 칸 = 0; 칸 < 64; 칸++) atmintis_failų_sistema.이름들[Failas * 64 + 칸] = Failas_lentelė[Failas * 72 + 칸];
            atmintis_failų_sistema.dydis_Sąrašas[Failas] = Failas_lentelė[Failas * 72] == 0 ? 0 : lentelė_sveikasis_skaičius(Failas * 72 + 64);
            atmintis_failų_sistema.허가들[Failas] = lentelė_sveikasis_skaičius(Failas * 72 + 68) & 511;
            for (int sekcija_VALUE = 0; sekcija_VALUE < 32; sekcija_VALUE++) {
                if (saugojimo_įrenginys_ryšys.Skaitymas(Start_sekcija + 3 + Failas * 32 + sekcija_VALUE) < 0) return -5;
                int ADDRESS = įrenginys_VALUE.Failas_atmintis() + Failas * 16384 + sekcija_VALUE * 512;
                for (int 칸 = 0; 칸 < 512; 칸++) įrenginys_VALUE.rašymas_atmintis(ADDRESS + 칸, saugojimo_įrenginys_ryšys.sekcija_duomenys[칸]);
            }
        }
        return 0;
    }
    static void Parengti() {
        if (saugojimo_įrenginys_ryšys.Skaitymas(0) < 0 || saugojimo_įrenginys_ryšys.analizuoti_sintaksę_sveikasis_skaičius(0) != 0x54534b4a
            || saugojimo_įrenginys_ryšys.analizuoti_sintaksę_sveikasis_skaičius(4) != 0x3145524f || saugojimo_įrenginys_ryšys.analizuoti_sintaksę_sveikasis_skaičius(8) != 2048
            || saugojimo_įrenginys_ryšys.analizuoti_sintaksę_sveikasis_skaičius(12) != 0x3153464a) {
            SMS_Terminalas.Rašymas("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        saugojimo_įrenginys_ryšys.informacinės_technologijos_Aktyvus_9e72441a = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Terminalas.Rašymas("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (Apkrova(현재보존본) < 0) {
            SMS_Terminalas.Rašymas("STORE read failed; halted to preserve files\n"); įrenginys_VALUE.정지();
        }
        SMS_Terminalas.Rašymas("STORE restored generation "); SMS_Terminalas.rašymas_numeris(세대번호); SMS_Terminalas.문자(10);
    }
    static int sinchronizuoti() {
        if (!saugojimo_įrenginys_ryšys.informacinės_technologijos_Aktyvus_9e72441a) return -19;
        if (세대번호 == 2147483647) return -75;
        int toliau_prekė = 현재보존본 == 0 ? 1 : 0, Start_sekcija = 1 + toliau_prekė * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 įrenginys_VALUE 캐시를 비운다.
        apmokėti_duomenys();
        if (saugojimo_įrenginys_ryšys.Rašymas(Start_sekcija) < 0 || saugojimo_įrenginys_ryšys.밀어쓰기() < 0) return -5;
        for (int 칸 = 0; 칸 < 1024; 칸++) Failas_lentelė[칸] = 0;
        for (int Failas = 0; Failas < 8; Failas++) if (atmintis_failų_sistema.이름들[Failas * 64] != 0) {
            for (int 칸 = 0; 칸 < 64; 칸++) Failas_lentelė[Failas * 72 + 칸] = atmintis_failų_sistema.이름들[Failas * 64 + 칸];
            rašymas_lentelė_sveikasis_skaičius(Failas * 72 + 64, atmintis_failų_sistema.dydis_Sąrašas[Failas]);
            rašymas_lentelė_sveikasis_skaičius(Failas * 72 + 68, atmintis_failų_sistema.허가들[Failas]);
        }
        int maiša_Failas = 0x811c9dc5;
        for (int sekcija_VALUE = 0; sekcija_VALUE < 258; sekcija_VALUE++) {
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int VALUE = 0;
                if (sekcija_VALUE < 2) VALUE = Failas_lentelė[sekcija_VALUE * 512 + 칸];
                else {
                    int Failas = (sekcija_VALUE - 2) / 32, Pozicija = (sekcija_VALUE - 2) % 32 * 512 + 칸;
                    if (Failas_lentelė[Failas * 72] != 0 && Pozicija < atmintis_failų_sistema.dydis_Sąrašas[Failas])
                        VALUE = įrenginys_VALUE.기억읽기(įrenginys_VALUE.Failas_atmintis() + Failas * 16384 + Pozicija);
                }
                saugojimo_įrenginys_ryšys.sekcija_duomenys[칸] = VALUE; maiša_Failas = 바이트해시(maiša_Failas, VALUE);
            }
            if (saugojimo_įrenginys_ryšys.Rašymas(Start_sekcija + 1 + sekcija_VALUE) < 0) return -5;
        }
        if (saugojimo_įrenginys_ryšys.밀어쓰기() < 0) return -5;
        apmokėti_duomenys(); saugojimo_įrenginys_ryšys.rašymas_sveikasis_skaičius_VALUE(0, 0x4a4b534e);
        saugojimo_įrenginys_ryšys.rašymas_sveikasis_skaičius_VALUE(4, 세대번호 + 1); saugojimo_įrenginys_ryšys.rašymas_sveikasis_skaičius_VALUE(8, maiša_Failas);
        saugojimo_įrenginys_ryšys.rašymas_sveikasis_skaičius_VALUE(12, (세대번호 + 1) ^ maiša_Failas ^ 0x4a4b534e);
        if (saugojimo_įrenginys_ryšys.Rašymas(Start_sekcija) < 0 || saugojimo_įrenginys_ryšys.밀어쓰기() < 0) return -5;
        현재보존본 = toliau_prekė; 세대번호++;
        return 0;
    }
}
