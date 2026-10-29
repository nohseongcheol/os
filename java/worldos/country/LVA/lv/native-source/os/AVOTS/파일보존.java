// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_VALUE formāts_VALUE. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] Fails_tabula = new int[1024];
    static int 바이트해시(int VALUE, int dati) { return (VALUE ^ dati) * 16777619; }
    static void nodzēst_dati() {
        for (int INDEX = 0; INDEX < 512; INDEX++) atmiņas_ierīce_paziņa.sadaļa_dati[INDEX] = 0;
    }
    static int tabula_vesels_skaitlis(int Novietojums) {
        return Fails_tabula[Novietojums] | Fails_tabula[Novietojums + 1] << 8 | Fails_tabula[Novietojums + 2] << 16 | Fails_tabula[Novietojums + 3] << 24;
    }
    static void rakstīšana_tabula_vesels_skaitlis(int Novietojums, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) Fails_tabula[Novietojums + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
    static boolean čeks_tabula() {
        for (int Fails = 0; Fails < 8; Fails++) {
            int 길이 = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) atmiņa_failu_sistēma.Nosaukums[칸] = Fails_tabula[Fails * 72 + 칸];
            while (길이 < 64 && atmiņa_failu_sistēma.Nosaukums[길이] != 0) 길이++;
            if (길이 == 0) continue;
            if (!atmiņa_failu_sistēma.čeks_nosaukums(atmiņa_failu_sistēma.Nosaukums, 길이)
                || tabula_vesels_skaitlis(Fails * 72 + 64) < 0 || tabula_vesels_skaitlis(Fails * 72 + 64) > 16384) return false;
            for (int priekšējā_VALUE = 0; priekšējā_VALUE < Fails; priekšējā_VALUE++) {
                boolean 같음 = Fails_tabula[priekšējā_VALUE * 72 + 길이] == 0;
                for (int 칸 = 0; 칸 < 길이; 칸++) if (Fails_tabula[priekšējā_VALUE * 72 + 칸] != atmiņa_failu_sistēma.Nosaukums[칸]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int Sākt_sadaļa = 1 + 보존본 * 259;
        if (atmiņas_ierīce_paziņa.Lasīt(Sākt_sadaļa) < 0 || atmiņas_ierīce_paziņa.parsēt_vesels_skaitlis(0) != 0x4a4b534e) return -1;
        int 세대 = atmiņas_ierīce_paziņa.parsēt_vesels_skaitlis(4), kontrolsumma = atmiņas_ierīce_paziņa.parsēt_vesels_skaitlis(8);
        if (세대 < 1 || atmiņas_ierīce_paziņa.parsēt_vesels_skaitlis(12) != (세대 ^ kontrolsumma ^ 0x4a4b534e)) return -1;
        int jaukšana_Fails = 0x811c9dc5;
        for (int sadaļa_VALUE = 0; sadaļa_VALUE < 258; sadaļa_VALUE++) {
            if (atmiņas_ierīce_paziņa.Lasīt(Sākt_sadaļa + 1 + sadaļa_VALUE) < 0) return -1;
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int VALUE = atmiņas_ierīce_paziņa.sadaļa_dati[칸];
                jaukšana_Fails = 바이트해시(jaukšana_Fails, VALUE);
                if (sadaļa_VALUE < 2) Fails_tabula[sadaļa_VALUE * 512 + 칸] = VALUE;
            }
        }
        return jaukšana_Fails == kontrolsumma && čeks_tabula() ? 세대 : -1;
    }
    static int Noslodze(int 보존본) {
        int Sākt_sadaļa = 1 + 보존본 * 259;
        for (int sadaļa_VALUE = 0; sadaļa_VALUE < 2; sadaļa_VALUE++) {
            if (atmiņas_ierīce_paziņa.Lasīt(Sākt_sadaļa + 1 + sadaļa_VALUE) < 0) return -5;
            for (int 칸 = 0; 칸 < 512; 칸++) Fails_tabula[sadaļa_VALUE * 512 + 칸] = atmiņas_ierīce_paziņa.sadaļa_dati[칸];
        }
        for (int Fails = 0; Fails < 8; Fails++) {
            for (int 칸 = 0; 칸 < 64; 칸++) atmiņa_failu_sistēma.이름들[Fails * 64 + 칸] = Fails_tabula[Fails * 72 + 칸];
            atmiņa_failu_sistēma.mainīt_izmērus_Saraksts[Fails] = Fails_tabula[Fails * 72] == 0 ? 0 : tabula_vesels_skaitlis(Fails * 72 + 64);
            atmiņa_failu_sistēma.허가들[Fails] = tabula_vesels_skaitlis(Fails * 72 + 68) & 511;
            for (int sadaļa_VALUE = 0; sadaļa_VALUE < 32; sadaļa_VALUE++) {
                if (atmiņas_ierīce_paziņa.Lasīt(Sākt_sadaļa + 3 + Fails * 32 + sadaļa_VALUE) < 0) return -5;
                int adrese = ierīce_VALUE.Fails_atmiņa() + Fails * 16384 + sadaļa_VALUE * 512;
                for (int 칸 = 0; 칸 < 512; 칸++) ierīce_VALUE.rakstīšana_atmiņa(adrese + 칸, atmiņas_ierīce_paziņa.sadaļa_dati[칸]);
            }
        }
        return 0;
    }
    static void Sagatavot() {
        if (atmiņas_ierīce_paziņa.Lasīt(0) < 0 || atmiņas_ierīce_paziņa.parsēt_vesels_skaitlis(0) != 0x54534b4a
            || atmiņas_ierīce_paziņa.parsēt_vesels_skaitlis(4) != 0x3145524f || atmiņas_ierīce_paziņa.parsēt_vesels_skaitlis(8) != 2048
            || atmiņas_ierīce_paziņa.parsēt_vesels_skaitlis(12) != 0x3153464a) {
            SMS_Terminālis.Rakstīt("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        atmiņas_ierīce_paziņa.informācijas_tehnoloģija_Aktīvs_9e72441a = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Terminālis.Rakstīt("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (Noslodze(현재보존본) < 0) {
            SMS_Terminālis.Rakstīt("STORE read failed; halted to preserve files\n"); ierīce_VALUE.정지();
        }
        SMS_Terminālis.Rakstīt("STORE restored generation "); SMS_Terminālis.rakstīšana_numurs(세대번호); SMS_Terminālis.문자(10);
    }
    static int sinhronizēt() {
        if (!atmiņas_ierīce_paziņa.informācijas_tehnoloģija_Aktīvs_9e72441a) return -19;
        if (세대번호 == 2147483647) return -75;
        int Tālāk_krājums = 현재보존본 == 0 ? 1 : 0, Sākt_sadaļa = 1 + Tālāk_krājums * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 ierīce_VALUE 캐시를 비운다.
        nodzēst_dati();
        if (atmiņas_ierīce_paziņa.Rakstīt(Sākt_sadaļa) < 0 || atmiņas_ierīce_paziņa.밀어쓰기() < 0) return -5;
        for (int 칸 = 0; 칸 < 1024; 칸++) Fails_tabula[칸] = 0;
        for (int Fails = 0; Fails < 8; Fails++) if (atmiņa_failu_sistēma.이름들[Fails * 64] != 0) {
            for (int 칸 = 0; 칸 < 64; 칸++) Fails_tabula[Fails * 72 + 칸] = atmiņa_failu_sistēma.이름들[Fails * 64 + 칸];
            rakstīšana_tabula_vesels_skaitlis(Fails * 72 + 64, atmiņa_failu_sistēma.mainīt_izmērus_Saraksts[Fails]);
            rakstīšana_tabula_vesels_skaitlis(Fails * 72 + 68, atmiņa_failu_sistēma.허가들[Fails]);
        }
        int jaukšana_Fails = 0x811c9dc5;
        for (int sadaļa_VALUE = 0; sadaļa_VALUE < 258; sadaļa_VALUE++) {
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int VALUE = 0;
                if (sadaļa_VALUE < 2) VALUE = Fails_tabula[sadaļa_VALUE * 512 + 칸];
                else {
                    int Fails = (sadaļa_VALUE - 2) / 32, Novietojums = (sadaļa_VALUE - 2) % 32 * 512 + 칸;
                    if (Fails_tabula[Fails * 72] != 0 && Novietojums < atmiņa_failu_sistēma.mainīt_izmērus_Saraksts[Fails])
                        VALUE = ierīce_VALUE.기억읽기(ierīce_VALUE.Fails_atmiņa() + Fails * 16384 + Novietojums);
                }
                atmiņas_ierīce_paziņa.sadaļa_dati[칸] = VALUE; jaukšana_Fails = 바이트해시(jaukšana_Fails, VALUE);
            }
            if (atmiņas_ierīce_paziņa.Rakstīt(Sākt_sadaļa + 1 + sadaļa_VALUE) < 0) return -5;
        }
        if (atmiņas_ierīce_paziņa.밀어쓰기() < 0) return -5;
        nodzēst_dati(); atmiņas_ierīce_paziņa.rakstīšana_vesels_skaitlis_VALUE(0, 0x4a4b534e);
        atmiņas_ierīce_paziņa.rakstīšana_vesels_skaitlis_VALUE(4, 세대번호 + 1); atmiņas_ierīce_paziņa.rakstīšana_vesels_skaitlis_VALUE(8, jaukšana_Fails);
        atmiņas_ierīce_paziņa.rakstīšana_vesels_skaitlis_VALUE(12, (세대번호 + 1) ^ jaukšana_Fails ^ 0x4a4b534e);
        if (atmiņas_ierīce_paziņa.Rakstīt(Sākt_sadaļa) < 0 || atmiņas_ierīce_paziņa.밀어쓰기() < 0) return -5;
        현재보존본 = Tālāk_krājums; 세대번호++;
        return 0;
    }
}
