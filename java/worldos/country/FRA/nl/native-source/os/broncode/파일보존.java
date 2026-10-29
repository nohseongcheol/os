// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_WAARDE opmaak_WAARDE. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, generatie_nummer = 0;
    static int[] Bestand_tabel = new int[1024];
    static int 바이트해시(int WAARDE, int gegevens) { return (WAARDE ^ gegevens) * 16777619; }
    static void wissen_gegevens() {
        for (int INDEX = 0; INDEX < 512; INDEX++) opslagapparaat_verbinding.sectie_gegevens[INDEX] = 0;
    }
    static int tabel_geheel_getal(int positie) {
        return Bestand_tabel[positie] | Bestand_tabel[positie + 1] << 8 | Bestand_tabel[positie + 2] << 16 | Bestand_tabel[positie + 3] << 24;
    }
    static void schrijven_tabel_geheel_getal(int positie, int WAARDE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) Bestand_tabel[positie + INDEX] = (WAARDE >>> (INDEX * 8)) & 255;
    }
    static boolean cheque_tabel() {
        for (int bestand = 0; bestand < 8; bestand++) {
            int tijdsduur_WAARDE = 0;
            for (int sleuf_invoer = 0; sleuf_invoer < 64; sleuf_invoer++) Geheugen_bestandssysteem.Naam[sleuf_invoer] = Bestand_tabel[bestand * 72 + sleuf_invoer];
            while (tijdsduur_WAARDE < 64 && Geheugen_bestandssysteem.Naam[tijdsduur_WAARDE] != 0) tijdsduur_WAARDE++;
            if (tijdsduur_WAARDE == 0) continue;
            if (!Geheugen_bestandssysteem.cheque_naam(Geheugen_bestandssysteem.Naam, tijdsduur_WAARDE)
                || tabel_geheel_getal(bestand * 72 + 64) < 0 || tabel_geheel_getal(bestand * 72 + 64) > 16384) return false;
            for (int voorkant_WAARDE = 0; voorkant_WAARDE < bestand; voorkant_WAARDE++) {
                boolean 같음 = Bestand_tabel[voorkant_WAARDE * 72 + tijdsduur_WAARDE] == 0;
                for (int sleuf_invoer = 0; sleuf_invoer < tijdsduur_WAARDE; sleuf_invoer++) if (Bestand_tabel[voorkant_WAARDE * 72 + sleuf_invoer] != Geheugen_bestandssysteem.Naam[sleuf_invoer]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int START_sectie = 1 + 보존본 * 259;
        if (opslagapparaat_verbinding.Lezen(START_sectie) < 0 || opslagapparaat_verbinding.parseren_geheel_getal(0) != 0x4a4b534e) return -1;
        int generatie_WAARDE = opslagapparaat_verbinding.parseren_geheel_getal(4), controlesom = opslagapparaat_verbinding.parseren_geheel_getal(8);
        if (generatie_WAARDE < 1 || opslagapparaat_verbinding.parseren_geheel_getal(12) != (generatie_WAARDE ^ controlesom ^ 0x4a4b534e)) return -1;
        int hash_Bestand = 0x811c9dc5;
        for (int sectie_WAARDE = 0; sectie_WAARDE < 258; sectie_WAARDE++) {
            if (opslagapparaat_verbinding.Lezen(START_sectie + 1 + sectie_WAARDE) < 0) return -1;
            for (int sleuf_invoer = 0; sleuf_invoer < 512; sleuf_invoer++) {
                int WAARDE = opslagapparaat_verbinding.sectie_gegevens[sleuf_invoer];
                hash_Bestand = 바이트해시(hash_Bestand, WAARDE);
                if (sectie_WAARDE < 2) Bestand_tabel[sectie_WAARDE * 512 + sleuf_invoer] = WAARDE;
            }
        }
        return hash_Bestand == controlesom && cheque_tabel() ? generatie_WAARDE : -1;
    }
    static int broncodeLaden(int 보존본) {
        int START_sectie = 1 + 보존본 * 259;
        for (int sectie_WAARDE = 0; sectie_WAARDE < 2; sectie_WAARDE++) {
            if (opslagapparaat_verbinding.Lezen(START_sectie + 1 + sectie_WAARDE) < 0) return -5;
            for (int sleuf_invoer = 0; sleuf_invoer < 512; sleuf_invoer++) Bestand_tabel[sectie_WAARDE * 512 + sleuf_invoer] = opslagapparaat_verbinding.sectie_gegevens[sleuf_invoer];
        }
        for (int bestand = 0; bestand < 8; bestand++) {
            for (int sleuf_invoer = 0; sleuf_invoer < 64; sleuf_invoer++) Geheugen_bestandssysteem.이름들[bestand * 64 + sleuf_invoer] = Bestand_tabel[bestand * 72 + sleuf_invoer];
            Geheugen_bestandssysteem.formaat_wijzigen_Lijst[bestand] = Bestand_tabel[bestand * 72] == 0 ? 0 : tabel_geheel_getal(bestand * 72 + 64);
            Geheugen_bestandssysteem.허가들[bestand] = tabel_geheel_getal(bestand * 72 + 68) & 511;
            for (int sectie_WAARDE = 0; sectie_WAARDE < 32; sectie_WAARDE++) {
                if (opslagapparaat_verbinding.Lezen(START_sectie + 3 + bestand * 32 + sectie_WAARDE) < 0) return -5;
                int ADRES = mobiel_WAARDE.Bestand_Geheugen() + bestand * 16384 + sectie_WAARDE * 512;
                for (int sleuf_invoer = 0; sleuf_invoer < 512; sleuf_invoer++) mobiel_WAARDE.schrijven_Geheugen(ADRES + sleuf_invoer, opslagapparaat_verbinding.sectie_gegevens[sleuf_invoer]);
            }
        }
        return 0;
    }
    static void Bereid_voor() {
        if (opslagapparaat_verbinding.Lezen(0) < 0 || opslagapparaat_verbinding.parseren_geheel_getal(0) != 0x54534b4a
            || opslagapparaat_verbinding.parseren_geheel_getal(4) != 0x3145524f || opslagapparaat_verbinding.parseren_geheel_getal(8) != 2048
            || opslagapparaat_verbinding.parseren_geheel_getal(12) != 0x3153464a) {
            sms_Terminal.Schrijven("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        opslagapparaat_verbinding.informatie_Actief_9e72441a = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { sms_Terminal.Schrijven("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; generatie_nummer = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (broncodeLaden(현재보존본) < 0) {
            sms_Terminal.Schrijven("STORE read failed; halted to preserve files\n"); mobiel_WAARDE.정지();
        }
        sms_Terminal.Schrijven("STORE restored generation "); sms_Terminal.schrijven_nummer(generatie_nummer); sms_Terminal.문자(10);
    }
    static int synchroniseren() {
        if (!opslagapparaat_verbinding.informatie_Actief_9e72441a) return -19;
        if (generatie_nummer == 2147483647) return -75;
        int Volgende_item = 현재보존본 == 0 ? 1 : 0, START_sectie = 1 + Volgende_item * 259;
        // 새 본문보다 먼저 Vorige_item commit을 무효화하고 mobiel_WAARDE 캐시를 비운다.
        wissen_gegevens();
        if (opslagapparaat_verbinding.Schrijven(START_sectie) < 0 || opslagapparaat_verbinding.leegmaken_uitvoer() < 0) return -5;
        for (int sleuf_invoer = 0; sleuf_invoer < 1024; sleuf_invoer++) Bestand_tabel[sleuf_invoer] = 0;
        for (int bestand = 0; bestand < 8; bestand++) if (Geheugen_bestandssysteem.이름들[bestand * 64] != 0) {
            for (int sleuf_invoer = 0; sleuf_invoer < 64; sleuf_invoer++) Bestand_tabel[bestand * 72 + sleuf_invoer] = Geheugen_bestandssysteem.이름들[bestand * 64 + sleuf_invoer];
            schrijven_tabel_geheel_getal(bestand * 72 + 64, Geheugen_bestandssysteem.formaat_wijzigen_Lijst[bestand]);
            schrijven_tabel_geheel_getal(bestand * 72 + 68, Geheugen_bestandssysteem.허가들[bestand]);
        }
        int hash_Bestand = 0x811c9dc5;
        for (int sectie_WAARDE = 0; sectie_WAARDE < 258; sectie_WAARDE++) {
            for (int sleuf_invoer = 0; sleuf_invoer < 512; sleuf_invoer++) {
                int WAARDE = 0;
                if (sectie_WAARDE < 2) WAARDE = Bestand_tabel[sectie_WAARDE * 512 + sleuf_invoer];
                else {
                    int bestand = (sectie_WAARDE - 2) / 32, positie = (sectie_WAARDE - 2) % 32 * 512 + sleuf_invoer;
                    if (Bestand_tabel[bestand * 72] != 0 && positie < Geheugen_bestandssysteem.formaat_wijzigen_Lijst[bestand])
                        WAARDE = mobiel_WAARDE.기억읽기(mobiel_WAARDE.Bestand_Geheugen() + bestand * 16384 + positie);
                }
                opslagapparaat_verbinding.sectie_gegevens[sleuf_invoer] = WAARDE; hash_Bestand = 바이트해시(hash_Bestand, WAARDE);
            }
            if (opslagapparaat_verbinding.Schrijven(START_sectie + 1 + sectie_WAARDE) < 0) return -5;
        }
        if (opslagapparaat_verbinding.leegmaken_uitvoer() < 0) return -5;
        wissen_gegevens(); opslagapparaat_verbinding.schrijven_geheel_getal_WAARDE(0, 0x4a4b534e);
        opslagapparaat_verbinding.schrijven_geheel_getal_WAARDE(4, generatie_nummer + 1); opslagapparaat_verbinding.schrijven_geheel_getal_WAARDE(8, hash_Bestand);
        opslagapparaat_verbinding.schrijven_geheel_getal_WAARDE(12, (generatie_nummer + 1) ^ hash_Bestand ^ 0x4a4b534e);
        if (opslagapparaat_verbinding.Schrijven(START_sectie) < 0 || opslagapparaat_verbinding.leegmaken_uitvoer() < 0) return -5;
        현재보존본 = Volgende_item; generatie_nummer++;
        return 0;
    }
}
