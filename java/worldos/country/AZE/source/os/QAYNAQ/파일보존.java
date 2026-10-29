// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_VALUE format_VALUE. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] fayl_cədvəl = new int[1024];
    static int 바이트해시(int VALUE, int verilənlər) { return (VALUE ^ verilənlər) * 16777619; }
    static void təmizləmək_verilənlər() {
        for (int INDEX = 0; INDEX < 512; INDEX++) Yaddaş_cihaz_qoşulma.bölmə_verilənlər[INDEX] = 0;
    }
    static int cədvəl_tam_ədəd(int yerinə_qoymaq) {
        return fayl_cədvəl[yerinə_qoymaq] | fayl_cədvəl[yerinə_qoymaq + 1] << 8 | fayl_cədvəl[yerinə_qoymaq + 2] << 16 | fayl_cədvəl[yerinə_qoymaq + 3] << 24;
    }
    static void yazmaq_cədvəl_tam_ədəd(int yerinə_qoymaq, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) fayl_cədvəl[yerinə_qoymaq + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
    static boolean çek_cədvəl() {
        for (int FAYL = 0; FAYL < 8; FAYL++) {
            int uzunluq_VALUE = 0;
            for (int slot_daxiletmə = 0; slot_daxiletmə < 64; slot_daxiletmə++) Yaddaş_fayl_sistemi.Ad[slot_daxiletmə] = fayl_cədvəl[FAYL * 72 + slot_daxiletmə];
            while (uzunluq_VALUE < 64 && Yaddaş_fayl_sistemi.Ad[uzunluq_VALUE] != 0) uzunluq_VALUE++;
            if (uzunluq_VALUE == 0) continue;
            if (!Yaddaş_fayl_sistemi.çek_ad(Yaddaş_fayl_sistemi.Ad, uzunluq_VALUE)
                || cədvəl_tam_ədəd(FAYL * 72 + 64) < 0 || cədvəl_tam_ədəd(FAYL * 72 + 64) > 16384) return false;
            for (int ön_VALUE = 0; ön_VALUE < FAYL; ön_VALUE++) {
                boolean 같음 = fayl_cədvəl[ön_VALUE * 72 + uzunluq_VALUE] == 0;
                for (int slot_daxiletmə = 0; slot_daxiletmə < uzunluq_VALUE; slot_daxiletmə++) if (fayl_cədvəl[ön_VALUE * 72 + slot_daxiletmə] != Yaddaş_fayl_sistemi.Ad[slot_daxiletmə]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int Başla_bölmə = 1 + 보존본 * 259;
        if (Yaddaş_cihaz_qoşulma.Oxuma(Başla_bölmə) < 0 || Yaddaş_cihaz_qoşulma.parselləmək_tam_ədəd(0) != 0x4a4b534e) return -1;
        int 세대 = Yaddaş_cihaz_qoşulma.parselləmək_tam_ədəd(4), 검사합 = Yaddaş_cihaz_qoşulma.parselləmək_tam_ədəd(8);
        if (세대 < 1 || Yaddaş_cihaz_qoşulma.parselləmək_tam_ədəd(12) != (세대 ^ 검사합 ^ 0x4a4b534e)) return -1;
        int heş_fayl = 0x811c9dc5;
        for (int bölmə_VALUE_366e0bfa = 0; bölmə_VALUE_366e0bfa < 258; bölmə_VALUE_366e0bfa++) {
            if (Yaddaş_cihaz_qoşulma.Oxuma(Başla_bölmə + 1 + bölmə_VALUE_366e0bfa) < 0) return -1;
            for (int slot_daxiletmə = 0; slot_daxiletmə < 512; slot_daxiletmə++) {
                int VALUE = Yaddaş_cihaz_qoşulma.bölmə_verilənlər[slot_daxiletmə];
                heş_fayl = 바이트해시(heş_fayl, VALUE);
                if (bölmə_VALUE_366e0bfa < 2) fayl_cədvəl[bölmə_VALUE_366e0bfa * 512 + slot_daxiletmə] = VALUE;
            }
        }
        return heş_fayl == 검사합 && çek_cədvəl() ? 세대 : -1;
    }
    static int Yük(int 보존본) {
        int Başla_bölmə = 1 + 보존본 * 259;
        for (int bölmə_VALUE_366e0bfa = 0; bölmə_VALUE_366e0bfa < 2; bölmə_VALUE_366e0bfa++) {
            if (Yaddaş_cihaz_qoşulma.Oxuma(Başla_bölmə + 1 + bölmə_VALUE_366e0bfa) < 0) return -5;
            for (int slot_daxiletmə = 0; slot_daxiletmə < 512; slot_daxiletmə++) fayl_cədvəl[bölmə_VALUE_366e0bfa * 512 + slot_daxiletmə] = Yaddaş_cihaz_qoşulma.bölmə_verilənlər[slot_daxiletmə];
        }
        for (int FAYL = 0; FAYL < 8; FAYL++) {
            for (int slot_daxiletmə = 0; slot_daxiletmə < 64; slot_daxiletmə++) Yaddaş_fayl_sistemi.이름들[FAYL * 64 + slot_daxiletmə] = fayl_cədvəl[FAYL * 72 + slot_daxiletmə];
            Yaddaş_fayl_sistemi.ölçünü_dəyişmək_Siyahı[FAYL] = fayl_cədvəl[FAYL * 72] == 0 ? 0 : cədvəl_tam_ədəd(FAYL * 72 + 64);
            Yaddaş_fayl_sistemi.허가들[FAYL] = cədvəl_tam_ədəd(FAYL * 72 + 68) & 511;
            for (int bölmə_VALUE_366e0bfa = 0; bölmə_VALUE_366e0bfa < 32; bölmə_VALUE_366e0bfa++) {
                if (Yaddaş_cihaz_qoşulma.Oxuma(Başla_bölmə + 3 + FAYL * 32 + bölmə_VALUE_366e0bfa) < 0) return -5;
                int ünvan = cihaz_VALUE.fayl_Yaddaş() + FAYL * 16384 + bölmə_VALUE_366e0bfa * 512;
                for (int slot_daxiletmə = 0; slot_daxiletmə < 512; slot_daxiletmə++) cihaz_VALUE.yazmaq_Yaddaş(ünvan + slot_daxiletmə, Yaddaş_cihaz_qoşulma.bölmə_verilənlər[slot_daxiletmə]);
            }
        }
        return 0;
    }
    static void Hazırla() {
        if (Yaddaş_cihaz_qoşulma.Oxuma(0) < 0 || Yaddaş_cihaz_qoşulma.parselləmək_tam_ədəd(0) != 0x54534b4a
            || Yaddaş_cihaz_qoşulma.parselləmək_tam_ədəd(4) != 0x3145524f || Yaddaş_cihaz_qoşulma.parselləmək_tam_ədəd(8) != 2048
            || Yaddaş_cihaz_qoşulma.parselləmək_tam_ədəd(12) != 0x3153464a) {
            SMS_Terminal.Yazma("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        Yaddaş_cihaz_qoşulma.사용가능 = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Terminal.Yazma("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (Yük(현재보존본) < 0) {
            SMS_Terminal.Yazma("STORE read failed; halted to preserve files\n"); cihaz_VALUE.정지();
        }
        SMS_Terminal.Yazma("STORE restored generation "); SMS_Terminal.수쓰기(세대번호); SMS_Terminal.문자(10);
    }
    static int sinxronlaşdırmaq() {
        if (!Yaddaş_cihaz_qoşulma.사용가능) return -19;
        if (세대번호 == 2147483647) return -75;
        int Sonrakı_element = 현재보존본 == 0 ? 1 : 0, Başla_bölmə = 1 + Sonrakı_element * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 cihaz_VALUE 캐시를 비운다.
        təmizləmək_verilənlər();
        if (Yaddaş_cihaz_qoşulma.Yazma(Başla_bölmə) < 0 || Yaddaş_cihaz_qoşulma.밀어쓰기() < 0) return -5;
        for (int slot_daxiletmə = 0; slot_daxiletmə < 1024; slot_daxiletmə++) fayl_cədvəl[slot_daxiletmə] = 0;
        for (int FAYL = 0; FAYL < 8; FAYL++) if (Yaddaş_fayl_sistemi.이름들[FAYL * 64] != 0) {
            for (int slot_daxiletmə = 0; slot_daxiletmə < 64; slot_daxiletmə++) fayl_cədvəl[FAYL * 72 + slot_daxiletmə] = Yaddaş_fayl_sistemi.이름들[FAYL * 64 + slot_daxiletmə];
            yazmaq_cədvəl_tam_ədəd(FAYL * 72 + 64, Yaddaş_fayl_sistemi.ölçünü_dəyişmək_Siyahı[FAYL]);
            yazmaq_cədvəl_tam_ədəd(FAYL * 72 + 68, Yaddaş_fayl_sistemi.허가들[FAYL]);
        }
        int heş_fayl = 0x811c9dc5;
        for (int bölmə_VALUE_366e0bfa = 0; bölmə_VALUE_366e0bfa < 258; bölmə_VALUE_366e0bfa++) {
            for (int slot_daxiletmə = 0; slot_daxiletmə < 512; slot_daxiletmə++) {
                int VALUE = 0;
                if (bölmə_VALUE_366e0bfa < 2) VALUE = fayl_cədvəl[bölmə_VALUE_366e0bfa * 512 + slot_daxiletmə];
                else {
                    int FAYL = (bölmə_VALUE_366e0bfa - 2) / 32, yerinə_qoymaq = (bölmə_VALUE_366e0bfa - 2) % 32 * 512 + slot_daxiletmə;
                    if (fayl_cədvəl[FAYL * 72] != 0 && yerinə_qoymaq < Yaddaş_fayl_sistemi.ölçünü_dəyişmək_Siyahı[FAYL])
                        VALUE = cihaz_VALUE.기억읽기(cihaz_VALUE.fayl_Yaddaş() + FAYL * 16384 + yerinə_qoymaq);
                }
                Yaddaş_cihaz_qoşulma.bölmə_verilənlər[slot_daxiletmə] = VALUE; heş_fayl = 바이트해시(heş_fayl, VALUE);
            }
            if (Yaddaş_cihaz_qoşulma.Yazma(Başla_bölmə + 1 + bölmə_VALUE_366e0bfa) < 0) return -5;
        }
        if (Yaddaş_cihaz_qoşulma.밀어쓰기() < 0) return -5;
        təmizləmək_verilənlər(); Yaddaş_cihaz_qoşulma.yazmaq_tam_ədəd_VALUE(0, 0x4a4b534e);
        Yaddaş_cihaz_qoşulma.yazmaq_tam_ədəd_VALUE(4, 세대번호 + 1); Yaddaş_cihaz_qoşulma.yazmaq_tam_ədəd_VALUE(8, heş_fayl);
        Yaddaş_cihaz_qoşulma.yazmaq_tam_ədəd_VALUE(12, (세대번호 + 1) ^ heş_fayl ^ 0x4a4b534e);
        if (Yaddaş_cihaz_qoşulma.Yazma(Başla_bölmə) < 0 || Yaddaş_cihaz_qoşulma.밀어쓰기() < 0) return -5;
        현재보존본 = Sonrakı_element; 세대번호++;
        return 0;
    }
}
