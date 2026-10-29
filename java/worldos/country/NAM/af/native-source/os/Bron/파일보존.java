// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 bêre_VALUE formaat_VALUE. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] lêer_tabel = new int[1024];
    static int 바이트해시(int VALUE, int data) { return (VALUE ^ data) * 16777619; }
    static void vee_uit_data() {
        for (int INDEX = 0; INDEX < 512; INDEX++) Berging_mobiel_verbinding.seksie_data[INDEX] = 0;
    }
    static int tabel_heelgetal(int Posisie) {
        return lêer_tabel[Posisie] | lêer_tabel[Posisie + 1] << 8 | lêer_tabel[Posisie + 2] << 16 | lêer_tabel[Posisie + 3] << 24;
    }
    static void skryf_tabel_heelgetal(int Posisie, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) lêer_tabel[Posisie + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
    static boolean tjek_tabel() {
        for (int Lêer = 0; Lêer < 8; Lêer++) {
            int lengte_VALUE = 0;
            for (int gleuf_inskrywing = 0; gleuf_inskrywing < 64; gleuf_inskrywing++) Geheue_lêerstelsel.Naam[gleuf_inskrywing] = lêer_tabel[Lêer * 72 + gleuf_inskrywing];
            while (lengte_VALUE < 64 && Geheue_lêerstelsel.Naam[lengte_VALUE] != 0) lengte_VALUE++;
            if (lengte_VALUE == 0) continue;
            if (!Geheue_lêerstelsel.tjek_naam(Geheue_lêerstelsel.Naam, lengte_VALUE)
                || tabel_heelgetal(Lêer * 72 + 64) < 0 || tabel_heelgetal(Lêer * 72 + 64) > 16384) return false;
            for (int voor_VALUE = 0; voor_VALUE < Lêer; voor_VALUE++) {
                boolean 같음 = lêer_tabel[voor_VALUE * 72 + lengte_VALUE] == 0;
                for (int gleuf_inskrywing = 0; gleuf_inskrywing < lengte_VALUE; gleuf_inskrywing++) if (lêer_tabel[voor_VALUE * 72 + gleuf_inskrywing] != Geheue_lêerstelsel.Naam[gleuf_inskrywing]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int BEGIN_seksie = 1 + 보존본 * 259;
        if (Berging_mobiel_verbinding.Lees(BEGIN_seksie) < 0 || Berging_mobiel_verbinding.ontleed_heelgetal(0) != 0x4a4b534e) return -1;
        int 세대 = Berging_mobiel_verbinding.ontleed_heelgetal(4), 검사합 = Berging_mobiel_verbinding.ontleed_heelgetal(8);
        if (세대 < 1 || Berging_mobiel_verbinding.ontleed_heelgetal(12) != (세대 ^ 검사합 ^ 0x4a4b534e)) return -1;
        int huts_lêer = 0x811c9dc5;
        for (int seksie_VALUE = 0; seksie_VALUE < 258; seksie_VALUE++) {
            if (Berging_mobiel_verbinding.Lees(BEGIN_seksie + 1 + seksie_VALUE) < 0) return -1;
            for (int gleuf_inskrywing = 0; gleuf_inskrywing < 512; gleuf_inskrywing++) {
                int VALUE = Berging_mobiel_verbinding.seksie_data[gleuf_inskrywing];
                huts_lêer = 바이트해시(huts_lêer, VALUE);
                if (seksie_VALUE < 2) lêer_tabel[seksie_VALUE * 512 + gleuf_inskrywing] = VALUE;
            }
        }
        return huts_lêer == 검사합 && tjek_tabel() ? 세대 : -1;
    }
    static int Lading(int 보존본) {
        int BEGIN_seksie = 1 + 보존본 * 259;
        for (int seksie_VALUE = 0; seksie_VALUE < 2; seksie_VALUE++) {
            if (Berging_mobiel_verbinding.Lees(BEGIN_seksie + 1 + seksie_VALUE) < 0) return -5;
            for (int gleuf_inskrywing = 0; gleuf_inskrywing < 512; gleuf_inskrywing++) lêer_tabel[seksie_VALUE * 512 + gleuf_inskrywing] = Berging_mobiel_verbinding.seksie_data[gleuf_inskrywing];
        }
        for (int Lêer = 0; Lêer < 8; Lêer++) {
            for (int gleuf_inskrywing = 0; gleuf_inskrywing < 64; gleuf_inskrywing++) Geheue_lêerstelsel.이름들[Lêer * 64 + gleuf_inskrywing] = lêer_tabel[Lêer * 72 + gleuf_inskrywing];
            Geheue_lêerstelsel.verstel_Lys[Lêer] = lêer_tabel[Lêer * 72] == 0 ? 0 : tabel_heelgetal(Lêer * 72 + 64);
            Geheue_lêerstelsel.허가들[Lêer] = tabel_heelgetal(Lêer * 72 + 68) & 511;
            for (int seksie_VALUE = 0; seksie_VALUE < 32; seksie_VALUE++) {
                if (Berging_mobiel_verbinding.Lees(BEGIN_seksie + 3 + Lêer * 32 + seksie_VALUE) < 0) return -5;
                int adres = mobiel_VALUE.lêer_Geheue() + Lêer * 16384 + seksie_VALUE * 512;
                for (int gleuf_inskrywing = 0; gleuf_inskrywing < 512; gleuf_inskrywing++) mobiel_VALUE.skryf_Geheue(adres + gleuf_inskrywing, Berging_mobiel_verbinding.seksie_data[gleuf_inskrywing]);
            }
        }
        return 0;
    }
    static void Maak_gereed() {
        if (Berging_mobiel_verbinding.Lees(0) < 0 || Berging_mobiel_verbinding.ontleed_heelgetal(0) != 0x54534b4a
            || Berging_mobiel_verbinding.ontleed_heelgetal(4) != 0x3145524f || Berging_mobiel_verbinding.ontleed_heelgetal(8) != 2048
            || Berging_mobiel_verbinding.ontleed_heelgetal(12) != 0x3153464a) {
            SMS_Terminaal.Skryf("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        Berging_mobiel_verbinding.사용가능 = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Terminaal.Skryf("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (Lading(현재보존본) < 0) {
            SMS_Terminaal.Skryf("STORE read failed; halted to preserve files\n"); mobiel_VALUE.정지();
        }
        SMS_Terminaal.Skryf("STORE restored generation "); SMS_Terminaal.수쓰기(세대번호); SMS_Terminaal.문자(10);
    }
    static int sinc() {
        if (!Berging_mobiel_verbinding.사용가능) return -19;
        if (세대번호 == 2147483647) return -75;
        int Volgende_item = 현재보존본 == 0 ? 1 : 0, BEGIN_seksie = 1 + Volgende_item * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 mobiel_VALUE 캐시를 비운다.
        vee_uit_data();
        if (Berging_mobiel_verbinding.Skryf(BEGIN_seksie) < 0 || Berging_mobiel_verbinding.밀어쓰기() < 0) return -5;
        for (int gleuf_inskrywing = 0; gleuf_inskrywing < 1024; gleuf_inskrywing++) lêer_tabel[gleuf_inskrywing] = 0;
        for (int Lêer = 0; Lêer < 8; Lêer++) if (Geheue_lêerstelsel.이름들[Lêer * 64] != 0) {
            for (int gleuf_inskrywing = 0; gleuf_inskrywing < 64; gleuf_inskrywing++) lêer_tabel[Lêer * 72 + gleuf_inskrywing] = Geheue_lêerstelsel.이름들[Lêer * 64 + gleuf_inskrywing];
            skryf_tabel_heelgetal(Lêer * 72 + 64, Geheue_lêerstelsel.verstel_Lys[Lêer]);
            skryf_tabel_heelgetal(Lêer * 72 + 68, Geheue_lêerstelsel.허가들[Lêer]);
        }
        int huts_lêer = 0x811c9dc5;
        for (int seksie_VALUE = 0; seksie_VALUE < 258; seksie_VALUE++) {
            for (int gleuf_inskrywing = 0; gleuf_inskrywing < 512; gleuf_inskrywing++) {
                int VALUE = 0;
                if (seksie_VALUE < 2) VALUE = lêer_tabel[seksie_VALUE * 512 + gleuf_inskrywing];
                else {
                    int Lêer = (seksie_VALUE - 2) / 32, Posisie = (seksie_VALUE - 2) % 32 * 512 + gleuf_inskrywing;
                    if (lêer_tabel[Lêer * 72] != 0 && Posisie < Geheue_lêerstelsel.verstel_Lys[Lêer])
                        VALUE = mobiel_VALUE.기억읽기(mobiel_VALUE.lêer_Geheue() + Lêer * 16384 + Posisie);
                }
                Berging_mobiel_verbinding.seksie_data[gleuf_inskrywing] = VALUE; huts_lêer = 바이트해시(huts_lêer, VALUE);
            }
            if (Berging_mobiel_verbinding.Skryf(BEGIN_seksie + 1 + seksie_VALUE) < 0) return -5;
        }
        if (Berging_mobiel_verbinding.밀어쓰기() < 0) return -5;
        vee_uit_data(); Berging_mobiel_verbinding.skryf_heelgetal_VALUE(0, 0x4a4b534e);
        Berging_mobiel_verbinding.skryf_heelgetal_VALUE(4, 세대번호 + 1); Berging_mobiel_verbinding.skryf_heelgetal_VALUE(8, huts_lêer);
        Berging_mobiel_verbinding.skryf_heelgetal_VALUE(12, (세대번호 + 1) ^ huts_lêer ^ 0x4a4b534e);
        if (Berging_mobiel_verbinding.Skryf(BEGIN_seksie) < 0 || Berging_mobiel_verbinding.밀어쓰기() < 0) return -5;
        현재보존본 = Volgende_item; 세대번호++;
        return 0;
    }
}
