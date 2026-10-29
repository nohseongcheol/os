// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_VALUE formáid_VALUE. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] comhad_tábla = new int[1024];
    static int 바이트해시(int VALUE, int sonraí) { return (VALUE ^ sonraí) * 16777619; }
    static void glan_sonraí() {
        for (int INDEX = 0; INDEX < 512; INDEX++) Stóras_gléas_nasc.rannán_sonraí[INDEX] = 0;
    }
    static int tábla_slánuimhir(int suíomh) {
        return comhad_tábla[suíomh] | comhad_tábla[suíomh + 1] << 8 | comhad_tábla[suíomh + 2] << 16 | comhad_tábla[suíomh + 3] << 24;
    }
    static void scríobh_tábla_slánuimhir(int suíomh, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) comhad_tábla[suíomh + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
    static boolean seic_tábla() {
        for (int Comhad = 0; Comhad < 8; Comhad++) {
            int fad_VALUE = 0;
            for (int spás_iontráil = 0; spás_iontráil < 64; spás_iontráil++) Cuimhne_córas_comhad.Ainm[spás_iontráil] = comhad_tábla[Comhad * 72 + spás_iontráil];
            while (fad_VALUE < 64 && Cuimhne_córas_comhad.Ainm[fad_VALUE] != 0) fad_VALUE++;
            if (fad_VALUE == 0) continue;
            if (!Cuimhne_córas_comhad.seic_ainm(Cuimhne_córas_comhad.Ainm, fad_VALUE)
                || tábla_slánuimhir(Comhad * 72 + 64) < 0 || tábla_slánuimhir(Comhad * 72 + 64) > 16384) return false;
            for (int 앞 = 0; 앞 < Comhad; 앞++) {
                boolean 같음 = comhad_tábla[앞 * 72 + fad_VALUE] == 0;
                for (int spás_iontráil = 0; spás_iontráil < fad_VALUE; spás_iontráil++) if (comhad_tábla[앞 * 72 + spás_iontráil] != Cuimhne_córas_comhad.Ainm[spás_iontráil]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int Start_rannán = 1 + 보존본 * 259;
        if (Stóras_gléas_nasc.Léigh(Start_rannán) < 0 || Stóras_gléas_nasc.parsáil_slánuimhir(0) != 0x4a4b534e) return -1;
        int 세대 = Stóras_gléas_nasc.parsáil_slánuimhir(4), suim_seiceála = Stóras_gléas_nasc.parsáil_slánuimhir(8);
        if (세대 < 1 || Stóras_gléas_nasc.parsáil_slánuimhir(12) != (세대 ^ suim_seiceála ^ 0x4a4b534e)) return -1;
        int hais_comhad = 0x811c9dc5;
        for (int rannán_VALUE = 0; rannán_VALUE < 258; rannán_VALUE++) {
            if (Stóras_gléas_nasc.Léigh(Start_rannán + 1 + rannán_VALUE) < 0) return -1;
            for (int spás_iontráil = 0; spás_iontráil < 512; spás_iontráil++) {
                int VALUE = Stóras_gléas_nasc.rannán_sonraí[spás_iontráil];
                hais_comhad = 바이트해시(hais_comhad, VALUE);
                if (rannán_VALUE < 2) comhad_tábla[rannán_VALUE * 512 + spás_iontráil] = VALUE;
            }
        }
        return hais_comhad == suim_seiceála && seic_tábla() ? 세대 : -1;
    }
    static int Lód(int 보존본) {
        int Start_rannán = 1 + 보존본 * 259;
        for (int rannán_VALUE = 0; rannán_VALUE < 2; rannán_VALUE++) {
            if (Stóras_gléas_nasc.Léigh(Start_rannán + 1 + rannán_VALUE) < 0) return -5;
            for (int spás_iontráil = 0; spás_iontráil < 512; spás_iontráil++) comhad_tábla[rannán_VALUE * 512 + spás_iontráil] = Stóras_gléas_nasc.rannán_sonraí[spás_iontráil];
        }
        for (int Comhad = 0; Comhad < 8; Comhad++) {
            for (int spás_iontráil = 0; spás_iontráil < 64; spás_iontráil++) Cuimhne_córas_comhad.이름들[Comhad * 64 + spás_iontráil] = comhad_tábla[Comhad * 72 + spás_iontráil];
            Cuimhne_córas_comhad.socraigh_méid_Liosta[Comhad] = comhad_tábla[Comhad * 72] == 0 ? 0 : tábla_slánuimhir(Comhad * 72 + 64);
            Cuimhne_córas_comhad.허가들[Comhad] = tábla_slánuimhir(Comhad * 72 + 68) & 511;
            for (int rannán_VALUE = 0; rannán_VALUE < 32; rannán_VALUE++) {
                if (Stóras_gléas_nasc.Léigh(Start_rannán + 3 + Comhad * 32 + rannán_VALUE) < 0) return -5;
                int ADDRESS = gléas_VALUE.comhad_Cuimhne() + Comhad * 16384 + rannán_VALUE * 512;
                for (int spás_iontráil = 0; spás_iontráil < 512; spás_iontráil++) gléas_VALUE.scríobh_Cuimhne(ADDRESS + spás_iontráil, Stóras_gléas_nasc.rannán_sonraí[spás_iontráil]);
            }
        }
        return 0;
    }
    static void Ullmhaigh() {
        if (Stóras_gléas_nasc.Léigh(0) < 0 || Stóras_gléas_nasc.parsáil_slánuimhir(0) != 0x54534b4a
            || Stóras_gléas_nasc.parsáil_slánuimhir(4) != 0x3145524f || Stóras_gléas_nasc.parsáil_slánuimhir(8) != 2048
            || Stóras_gléas_nasc.parsáil_slánuimhir(12) != 0x3153464a) {
            SMS_Teirminéal.Scríobh("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        Stóras_gléas_nasc.teicneolaíocht_faisnéise_ar_fáil = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Teirminéal.Scríobh("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (Lód(현재보존본) < 0) {
            SMS_Teirminéal.Scríobh("STORE read failed; halted to preserve files\n"); gléas_VALUE.정지();
        }
        SMS_Teirminéal.Scríobh("STORE restored generation "); SMS_Teirminéal.수쓰기(세대번호); SMS_Teirminéal.문자(10);
    }
    static int sioncronaigh() {
        if (!Stóras_gléas_nasc.teicneolaíocht_faisnéise_ar_fáil) return -19;
        if (세대번호 == 2147483647) return -75;
        int Ar_aghaidh_mír = 현재보존본 == 0 ? 1 : 0, Start_rannán = 1 + Ar_aghaidh_mír * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 gléas_VALUE 캐시를 비운다.
        glan_sonraí();
        if (Stóras_gléas_nasc.Scríobh(Start_rannán) < 0 || Stóras_gléas_nasc.밀어쓰기() < 0) return -5;
        for (int spás_iontráil = 0; spás_iontráil < 1024; spás_iontráil++) comhad_tábla[spás_iontráil] = 0;
        for (int Comhad = 0; Comhad < 8; Comhad++) if (Cuimhne_córas_comhad.이름들[Comhad * 64] != 0) {
            for (int spás_iontráil = 0; spás_iontráil < 64; spás_iontráil++) comhad_tábla[Comhad * 72 + spás_iontráil] = Cuimhne_córas_comhad.이름들[Comhad * 64 + spás_iontráil];
            scríobh_tábla_slánuimhir(Comhad * 72 + 64, Cuimhne_córas_comhad.socraigh_méid_Liosta[Comhad]);
            scríobh_tábla_slánuimhir(Comhad * 72 + 68, Cuimhne_córas_comhad.허가들[Comhad]);
        }
        int hais_comhad = 0x811c9dc5;
        for (int rannán_VALUE = 0; rannán_VALUE < 258; rannán_VALUE++) {
            for (int spás_iontráil = 0; spás_iontráil < 512; spás_iontráil++) {
                int VALUE = 0;
                if (rannán_VALUE < 2) VALUE = comhad_tábla[rannán_VALUE * 512 + spás_iontráil];
                else {
                    int Comhad = (rannán_VALUE - 2) / 32, suíomh = (rannán_VALUE - 2) % 32 * 512 + spás_iontráil;
                    if (comhad_tábla[Comhad * 72] != 0 && suíomh < Cuimhne_córas_comhad.socraigh_méid_Liosta[Comhad])
                        VALUE = gléas_VALUE.기억읽기(gléas_VALUE.comhad_Cuimhne() + Comhad * 16384 + suíomh);
                }
                Stóras_gléas_nasc.rannán_sonraí[spás_iontráil] = VALUE; hais_comhad = 바이트해시(hais_comhad, VALUE);
            }
            if (Stóras_gléas_nasc.Scríobh(Start_rannán + 1 + rannán_VALUE) < 0) return -5;
        }
        if (Stóras_gléas_nasc.밀어쓰기() < 0) return -5;
        glan_sonraí(); Stóras_gléas_nasc.scríobh_slánuimhir_VALUE(0, 0x4a4b534e);
        Stóras_gléas_nasc.scríobh_slánuimhir_VALUE(4, 세대번호 + 1); Stóras_gléas_nasc.scríobh_slánuimhir_VALUE(8, hais_comhad);
        Stóras_gléas_nasc.scríobh_slánuimhir_VALUE(12, (세대번호 + 1) ^ hais_comhad ^ 0x4a4b534e);
        if (Stóras_gléas_nasc.Scríobh(Start_rannán) < 0 || Stóras_gléas_nasc.밀어쓰기() < 0) return -5;
        현재보존본 = Ar_aghaidh_mír; 세대번호++;
        return 0;
    }
}
