// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_VALUE format_VALUE. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] Fișier_tabel = new int[1024];
    static int 바이트해시(int VALUE, int date) { return (VALUE ^ date) * 16777619; }
    static void goli_date() {
        for (int INDEX = 0; INDEX < 512; INDEX++) dispozitiv_de_stocare_conexiune.secțiune_date[INDEX] = 0;
    }
    static int tabel_întreg(int Poziție) {
        return Fișier_tabel[Poziție] | Fișier_tabel[Poziție + 1] << 8 | Fișier_tabel[Poziție + 2] << 16 | Fișier_tabel[Poziție + 3] << 24;
    }
    static void scriere_tabel_întreg(int Poziție, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) Fișier_tabel[Poziție + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
    static boolean verifica_tabel() {
        for (int Fișier = 0; Fișier < 8; Fișier++) {
            int lungime_VALUE = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) Memorie_sistem_de_fișiere.Nume[칸] = Fișier_tabel[Fișier * 72 + 칸];
            while (lungime_VALUE < 64 && Memorie_sistem_de_fișiere.Nume[lungime_VALUE] != 0) lungime_VALUE++;
            if (lungime_VALUE == 0) continue;
            if (!Memorie_sistem_de_fișiere.verifica_nume(Memorie_sistem_de_fișiere.Nume, lungime_VALUE)
                || tabel_întreg(Fișier * 72 + 64) < 0 || tabel_întreg(Fișier * 72 + 64) > 16384) return false;
            for (int frontală_VALUE = 0; frontală_VALUE < Fișier; frontală_VALUE++) {
                boolean 같음 = Fișier_tabel[frontală_VALUE * 72 + lungime_VALUE] == 0;
                for (int 칸 = 0; 칸 < lungime_VALUE; 칸++) if (Fișier_tabel[frontală_VALUE * 72 + 칸] != Memorie_sistem_de_fișiere.Nume[칸]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int buta_secțiune = 1 + 보존본 * 259;
        if (dispozitiv_de_stocare_conexiune.Citire(buta_secțiune) < 0 || dispozitiv_de_stocare_conexiune.analiza_întreg(0) != 0x4a4b534e) return -1;
        int 세대 = dispozitiv_de_stocare_conexiune.analiza_întreg(4), sumă_de_verificare = dispozitiv_de_stocare_conexiune.analiza_întreg(8);
        if (세대 < 1 || dispozitiv_de_stocare_conexiune.analiza_întreg(12) != (세대 ^ sumă_de_verificare ^ 0x4a4b534e)) return -1;
        int cod_hash_Fișier = 0x811c9dc5;
        for (int secțiune_VALUE = 0; secțiune_VALUE < 258; secțiune_VALUE++) {
            if (dispozitiv_de_stocare_conexiune.Citire(buta_secțiune + 1 + secțiune_VALUE) < 0) return -1;
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int VALUE = dispozitiv_de_stocare_conexiune.secțiune_date[칸];
                cod_hash_Fișier = 바이트해시(cod_hash_Fișier, VALUE);
                if (secțiune_VALUE < 2) Fișier_tabel[secțiune_VALUE * 512 + 칸] = VALUE;
            }
        }
        return cod_hash_Fișier == sumă_de_verificare && verifica_tabel() ? 세대 : -1;
    }
    static int Încărcare(int 보존본) {
        int buta_secțiune = 1 + 보존본 * 259;
        for (int secțiune_VALUE = 0; secțiune_VALUE < 2; secțiune_VALUE++) {
            if (dispozitiv_de_stocare_conexiune.Citire(buta_secțiune + 1 + secțiune_VALUE) < 0) return -5;
            for (int 칸 = 0; 칸 < 512; 칸++) Fișier_tabel[secțiune_VALUE * 512 + 칸] = dispozitiv_de_stocare_conexiune.secțiune_date[칸];
        }
        for (int Fișier = 0; Fișier < 8; Fișier++) {
            for (int 칸 = 0; 칸 < 64; 칸++) Memorie_sistem_de_fișiere.이름들[Fișier * 64 + 칸] = Fișier_tabel[Fișier * 72 + 칸];
            Memorie_sistem_de_fișiere.dimensiona_Listă[Fișier] = Fișier_tabel[Fișier * 72] == 0 ? 0 : tabel_întreg(Fișier * 72 + 64);
            Memorie_sistem_de_fișiere.허가들[Fișier] = tabel_întreg(Fișier * 72 + 68) & 511;
            for (int secțiune_VALUE = 0; secțiune_VALUE < 32; secțiune_VALUE++) {
                if (dispozitiv_de_stocare_conexiune.Citire(buta_secțiune + 3 + Fișier * 32 + secțiune_VALUE) < 0) return -5;
                int adresa = mobil_VALUE.Fișier_Memorie() + Fișier * 16384 + secțiune_VALUE * 512;
                for (int 칸 = 0; 칸 < 512; 칸++) mobil_VALUE.scriere_Memorie(adresa + 칸, dispozitiv_de_stocare_conexiune.secțiune_date[칸]);
            }
        }
        return 0;
    }
    static void Pregătiți() {
        if (dispozitiv_de_stocare_conexiune.Citire(0) < 0 || dispozitiv_de_stocare_conexiune.analiza_întreg(0) != 0x54534b4a
            || dispozitiv_de_stocare_conexiune.analiza_întreg(4) != 0x3145524f || dispozitiv_de_stocare_conexiune.analiza_întreg(8) != 2048
            || dispozitiv_de_stocare_conexiune.analiza_întreg(12) != 0x3153464a) {
            SMS_Terminal.Scriere("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        dispozitiv_de_stocare_conexiune.sisteme_de_informații_Activ_9e72441a = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Terminal.Scriere("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (Încărcare(현재보존본) < 0) {
            SMS_Terminal.Scriere("STORE read failed; halted to preserve files\n"); mobil_VALUE.정지();
        }
        SMS_Terminal.Scriere("STORE restored generation "); SMS_Terminal.수쓰기(세대번호); SMS_Terminal.문자(10);
    }
    static int sincroniz() {
        if (!dispozitiv_de_stocare_conexiune.sisteme_de_informații_Activ_9e72441a) return -19;
        if (세대번호 == 2147483647) return -75;
        int Următorul_element = 현재보존본 == 0 ? 1 : 0, buta_secțiune = 1 + Următorul_element * 259;
        // 새 본문보다 먼저 Anteriorul_element commit을 무효화하고 mobil_VALUE 캐시를 비운다.
        goli_date();
        if (dispozitiv_de_stocare_conexiune.Scriere(buta_secțiune) < 0 || dispozitiv_de_stocare_conexiune.밀어쓰기() < 0) return -5;
        for (int 칸 = 0; 칸 < 1024; 칸++) Fișier_tabel[칸] = 0;
        for (int Fișier = 0; Fișier < 8; Fișier++) if (Memorie_sistem_de_fișiere.이름들[Fișier * 64] != 0) {
            for (int 칸 = 0; 칸 < 64; 칸++) Fișier_tabel[Fișier * 72 + 칸] = Memorie_sistem_de_fișiere.이름들[Fișier * 64 + 칸];
            scriere_tabel_întreg(Fișier * 72 + 64, Memorie_sistem_de_fișiere.dimensiona_Listă[Fișier]);
            scriere_tabel_întreg(Fișier * 72 + 68, Memorie_sistem_de_fișiere.허가들[Fișier]);
        }
        int cod_hash_Fișier = 0x811c9dc5;
        for (int secțiune_VALUE = 0; secțiune_VALUE < 258; secțiune_VALUE++) {
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int VALUE = 0;
                if (secțiune_VALUE < 2) VALUE = Fișier_tabel[secțiune_VALUE * 512 + 칸];
                else {
                    int Fișier = (secțiune_VALUE - 2) / 32, Poziție = (secțiune_VALUE - 2) % 32 * 512 + 칸;
                    if (Fișier_tabel[Fișier * 72] != 0 && Poziție < Memorie_sistem_de_fișiere.dimensiona_Listă[Fișier])
                        VALUE = mobil_VALUE.기억읽기(mobil_VALUE.Fișier_Memorie() + Fișier * 16384 + Poziție);
                }
                dispozitiv_de_stocare_conexiune.secțiune_date[칸] = VALUE; cod_hash_Fișier = 바이트해시(cod_hash_Fișier, VALUE);
            }
            if (dispozitiv_de_stocare_conexiune.Scriere(buta_secțiune + 1 + secțiune_VALUE) < 0) return -5;
        }
        if (dispozitiv_de_stocare_conexiune.밀어쓰기() < 0) return -5;
        goli_date(); dispozitiv_de_stocare_conexiune.scriere_întreg_VALUE(0, 0x4a4b534e);
        dispozitiv_de_stocare_conexiune.scriere_întreg_VALUE(4, 세대번호 + 1); dispozitiv_de_stocare_conexiune.scriere_întreg_VALUE(8, cod_hash_Fișier);
        dispozitiv_de_stocare_conexiune.scriere_întreg_VALUE(12, (세대번호 + 1) ^ cod_hash_Fișier ^ 0x4a4b534e);
        if (dispozitiv_de_stocare_conexiune.Scriere(buta_secțiune) < 0 || dispozitiv_de_stocare_conexiune.밀어쓰기() < 0) return -5;
        현재보존본 = Următorul_element; 세대번호++;
        return 0;
    }
}
