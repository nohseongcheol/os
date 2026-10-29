// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 salv_VALUE vorming_VALUE. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] Fail_tabel = new int[1024];
    static int 바이트해시(int VALUE, int andmed) { return (VALUE ^ andmed) * 16777619; }
    static void eemaldama_andmed() {
        for (int INDEX = 0; INDEX < 512; INDEX++) salvesti_ühendus.jaotis_andmed[INDEX] = 0;
    }
    static int tabel_täisarv(int Asukoht) {
        return Fail_tabel[Asukoht] | Fail_tabel[Asukoht + 1] << 8 | Fail_tabel[Asukoht + 2] << 16 | Fail_tabel[Asukoht + 3] << 24;
    }
    static void kirjutamine_tabel_täisarv(int Asukoht, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) Fail_tabel[Asukoht + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
    static boolean tšekk_tabel() {
        for (int Fail = 0; Fail < 8; Fail++) {
            int 길이 = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) Mälu_failisüsteem.Nimi_2[칸] = Fail_tabel[Fail * 72 + 칸];
            while (길이 < 64 && Mälu_failisüsteem.Nimi_2[길이] != 0) 길이++;
            if (길이 == 0) continue;
            if (!Mälu_failisüsteem.tšekk_nimetus(Mälu_failisüsteem.Nimi_2, 길이)
                || tabel_täisarv(Fail * 72 + 64) < 0 || tabel_täisarv(Fail * 72 + 64) > 16384) return false;
            for (int esikaamera_VALUE = 0; esikaamera_VALUE < Fail; esikaamera_VALUE++) {
                boolean 같음 = Fail_tabel[esikaamera_VALUE * 72 + 길이] == 0;
                for (int 칸 = 0; 칸 < 길이; 칸++) if (Fail_tabel[esikaamera_VALUE * 72 + 칸] != Mälu_failisüsteem.Nimi_2[칸]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int START_jaotis = 1 + 보존본 * 259;
        if (salvesti_ühendus.Lugemine(START_jaotis) < 0 || salvesti_ühendus.sõeluma_täisarv(0) != 0x4a4b534e) return -1;
        int 세대 = salvesti_ühendus.sõeluma_täisarv(4), kontrollsumma = salvesti_ühendus.sõeluma_täisarv(8);
        if (세대 < 1 || salvesti_ühendus.sõeluma_täisarv(12) != (세대 ^ kontrollsumma ^ 0x4a4b534e)) return -1;
        int räsikood_Fail = 0x811c9dc5;
        for (int jaotis_VALUE = 0; jaotis_VALUE < 258; jaotis_VALUE++) {
            if (salvesti_ühendus.Lugemine(START_jaotis + 1 + jaotis_VALUE) < 0) return -1;
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int VALUE = salvesti_ühendus.jaotis_andmed[칸];
                räsikood_Fail = 바이트해시(räsikood_Fail, VALUE);
                if (jaotis_VALUE < 2) Fail_tabel[jaotis_VALUE * 512 + 칸] = VALUE;
            }
        }
        return räsikood_Fail == kontrollsumma && tšekk_tabel() ? 세대 : -1;
    }
    static int Koormus(int 보존본) {
        int START_jaotis = 1 + 보존본 * 259;
        for (int jaotis_VALUE = 0; jaotis_VALUE < 2; jaotis_VALUE++) {
            if (salvesti_ühendus.Lugemine(START_jaotis + 1 + jaotis_VALUE) < 0) return -5;
            for (int 칸 = 0; 칸 < 512; 칸++) Fail_tabel[jaotis_VALUE * 512 + 칸] = salvesti_ühendus.jaotis_andmed[칸];
        }
        for (int Fail = 0; Fail < 8; Fail++) {
            for (int 칸 = 0; 칸 < 64; 칸++) Mälu_failisüsteem.이름들[Fail * 64 + 칸] = Fail_tabel[Fail * 72 + 칸];
            Mälu_failisüsteem.suurust_muutma_Loend[Fail] = Fail_tabel[Fail * 72] == 0 ? 0 : tabel_täisarv(Fail * 72 + 64);
            Mälu_failisüsteem.허가들[Fail] = tabel_täisarv(Fail * 72 + 68) & 511;
            for (int jaotis_VALUE = 0; jaotis_VALUE < 32; jaotis_VALUE++) {
                if (salvesti_ühendus.Lugemine(START_jaotis + 3 + Fail * 32 + jaotis_VALUE) < 0) return -5;
                int ADDRESS = seade_VALUE.Fail_Mälu() + Fail * 16384 + jaotis_VALUE * 512;
                for (int 칸 = 0; 칸 < 512; 칸++) seade_VALUE.kirjutamine_Mälu(ADDRESS + 칸, salvesti_ühendus.jaotis_andmed[칸]);
            }
        }
        return 0;
    }
    static void Ettevalmistamine() {
        if (salvesti_ühendus.Lugemine(0) < 0 || salvesti_ühendus.sõeluma_täisarv(0) != 0x54534b4a
            || salvesti_ühendus.sõeluma_täisarv(4) != 0x3145524f || salvesti_ühendus.sõeluma_täisarv(8) != 2048
            || salvesti_ühendus.sõeluma_täisarv(12) != 0x3153464a) {
            SMS_terminal.Kirjutamine("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        salvesti_ühendus.infotehnoloogia_Aktiivne_9e72441a = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_terminal.Kirjutamine("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (Koormus(현재보존본) < 0) {
            SMS_terminal.Kirjutamine("STORE read failed; halted to preserve files\n"); seade_VALUE.정지();
        }
        SMS_terminal.Kirjutamine("STORE restored generation "); SMS_terminal.kirjutamine_number(세대번호); SMS_terminal.문자(10);
    }
    static int sünkroonima() {
        if (!salvesti_ühendus.infotehnoloogia_Aktiivne_9e72441a) return -19;
        if (세대번호 == 2147483647) return -75;
        int Edasi_kaup = 현재보존본 == 0 ? 1 : 0, START_jaotis = 1 + Edasi_kaup * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 seade_VALUE 캐시를 비운다.
        eemaldama_andmed();
        if (salvesti_ühendus.Kirjutamine(START_jaotis) < 0 || salvesti_ühendus.밀어쓰기() < 0) return -5;
        for (int 칸 = 0; 칸 < 1024; 칸++) Fail_tabel[칸] = 0;
        for (int Fail = 0; Fail < 8; Fail++) if (Mälu_failisüsteem.이름들[Fail * 64] != 0) {
            for (int 칸 = 0; 칸 < 64; 칸++) Fail_tabel[Fail * 72 + 칸] = Mälu_failisüsteem.이름들[Fail * 64 + 칸];
            kirjutamine_tabel_täisarv(Fail * 72 + 64, Mälu_failisüsteem.suurust_muutma_Loend[Fail]);
            kirjutamine_tabel_täisarv(Fail * 72 + 68, Mälu_failisüsteem.허가들[Fail]);
        }
        int räsikood_Fail = 0x811c9dc5;
        for (int jaotis_VALUE = 0; jaotis_VALUE < 258; jaotis_VALUE++) {
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int VALUE = 0;
                if (jaotis_VALUE < 2) VALUE = Fail_tabel[jaotis_VALUE * 512 + 칸];
                else {
                    int Fail = (jaotis_VALUE - 2) / 32, Asukoht = (jaotis_VALUE - 2) % 32 * 512 + 칸;
                    if (Fail_tabel[Fail * 72] != 0 && Asukoht < Mälu_failisüsteem.suurust_muutma_Loend[Fail])
                        VALUE = seade_VALUE.기억읽기(seade_VALUE.Fail_Mälu() + Fail * 16384 + Asukoht);
                }
                salvesti_ühendus.jaotis_andmed[칸] = VALUE; räsikood_Fail = 바이트해시(räsikood_Fail, VALUE);
            }
            if (salvesti_ühendus.Kirjutamine(START_jaotis + 1 + jaotis_VALUE) < 0) return -5;
        }
        if (salvesti_ühendus.밀어쓰기() < 0) return -5;
        eemaldama_andmed(); salvesti_ühendus.kirjutamine_täisarv_VALUE(0, 0x4a4b534e);
        salvesti_ühendus.kirjutamine_täisarv_VALUE(4, 세대번호 + 1); salvesti_ühendus.kirjutamine_täisarv_VALUE(8, räsikood_Fail);
        salvesti_ühendus.kirjutamine_täisarv_VALUE(12, (세대번호 + 1) ^ räsikood_Fail ^ 0x4a4b534e);
        if (salvesti_ühendus.Kirjutamine(START_jaotis) < 0 || salvesti_ühendus.밀어쓰기() < 0) return -5;
        현재보존본 = Edasi_kaup; 세대번호++;
        return 0;
    }
}
