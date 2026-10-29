// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 uporabnik kazalec/길이는 dostop_vnos 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int 배열길이(int naslov) {
        if (!실행관리.izrezek(naslov, 4)) return -14;
        int 길이 = 실행관리.수(naslov);
        if (길이 < 0 || 길이 > (실행관리.uporabnik_končati_klic - naslov - 4) / 4) return -14;
        return 길이;
    }

    public static int Proces_VALUE_vnos(int INDEX, int 가, int SECOND_operand, int 다, int 라, int 마) {
        if (INDEX == 30) return 파일서술자관리.odprto_Datoteka(가, SECOND_operand, 다);
        if (INDEX == 31) return 파일서술자관리.파일읽기(가, SECOND_operand, 다);
        if (INDEX == 32) return 파일서술자관리.pisati_Datoteka(가, SECOND_operand, 다);
        if (INDEX == 33) return 파일서술자관리.Zapri_Datoteka(가);
        if (INDEX == 34) return 파일서술자관리.iskati_Datoteka(가, SECOND_operand, 다);
        if (INDEX == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (INDEX == 36) return 파일서술자관리.서술자복제(가, SECOND_operand, true, 0);
        if (INDEX == 37) return 파일서술자관리.파일상태읽기(가, SECOND_operand);
        if (INDEX == 38) return 파일서술자관리.odstraniti_Datoteka_vnos_ime(가);
        if (INDEX == 39) return 파일서술자관리.파일길이정하기(가, SECOND_operand);
        if (INDEX == 40) return 파일서술자관리.서술자제어(가, SECOND_operand, 다);
        if (INDEX == 41) return 파일서술자관리.Ustvari_končna_točka(가, SECOND_operand, 다);
        if (INDEX == 42) return 파일서술자관리.BIND_naslov(가, SECOND_operand, 다);
        if (INDEX == 43) return 파일서술자관리.poslati_datagram_podatki(가, SECOND_operand, 다, 라, 마);
        if (INDEX == 44) return 파일서술자관리.sprejeti_sprejemati_prejeti_prejemati_datagram_podatki(가, SECOND_operand, 다, 라, 마);
        if (INDEX == 45) return 파일서술자관리.통신주소읽기(가, SECOND_operand, 다);
        if (INDEX == 46) return 파일서술자관리.nabor_sprejeti_sprejemati_prejeti_prejemati_TIMEOUT(가, SECOND_operand);
        if (INDEX == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.sinhronizirati();
        }
        if (INDEX == 1) {
            int 길이 = 배열길이(가);
            if (길이 < 0) return 길이;
            if (길이 > 4096) return -90;
            for (int znak_VALUE = 0; znak_VALUE < 길이; znak_VALUE++) SMS_Terminal.문자(실행관리.수(가 + 4 + znak_VALUE * 4) & 65535);
            return 길이;
        }
        if (INDEX == 2) return 실행관리.argument_COUNT;
        if (INDEX == 3) return 가 >= 0 && 가 < 실행관리.argument_COUNT ? 실행관리.argument_naslov[가] : 0;
        if (INDEX == 10) return mreža_Sklad.Odpri(가);
        if (INDEX == 11) {
            int 길이 = 배열길이(라);
            if (길이 < 0) return 길이;
            if (마 < 0 || 마 > 길이 || 마 > 1024) return -90;
            for (int Položaj = 0; Položaj < 마; Položaj++) 임시자료[Položaj] = 실행관리.수(라 + 4 + Položaj * 4) & 255;
            return mreža_Sklad.poslati(가, SECOND_operand, 다, 임시자료, 마);
        }
        if (INDEX == 12) {
            int 길이 = 배열길이(SECOND_operand);
            if (길이 < 0) return 길이;
            if (다 < 0 || 다 > 2000) return -22;
            int REZULTAT = mreža_Sklad.sprejeti_sprejemati_prejeti_prejemati(가, 임시자료, 길이 < 1024 ? 길이 : 1024, 다);
            if (REZULTAT >= 0) for (int Položaj = 0; Položaj < REZULTAT; Položaj++) 실행관리.수쓰기(SECOND_operand + 4 + Položaj * 4, 임시자료[Položaj]);
            return REZULTAT;
        }
        if (INDEX == 13) return mreža_Sklad.Zapri(가);
        if (INDEX == 14) return mreža_Sklad.내주소;
        if (INDEX == 15) return mreža_Sklad.enakovreden_naslov(가);
        if (INDEX == 16) return mreža_Sklad.enakovreden_številka_vrat(가);
        if (INDEX == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Terminal.문자(가); return 1;
        }
        if (INDEX == 20 || INDEX == 21) {
            int ime_spremeniti_velikost = 배열길이(가), podatki_spremeniti_velikost = 배열길이(SECOND_operand);
            if (ime_spremeniti_velikost < 0 || podatki_spremeniti_velikost < 0) return -14;
            if (ime_spremeniti_velikost < 1 || ime_spremeniti_velikost > 64) return -22;
            int 길이 = 0;
            while (길이 < ime_spremeniti_velikost && 실행관리.수(가 + 4 + 길이 * 4) != 0) {
                pomnilnik_datotečni_sistem.Ime[길이] = 실행관리.수(가 + 4 + 길이 * 4);
                길이++;
            }
            if (!pomnilnik_datotečni_sistem.preveriti_ime(pomnilnik_datotečni_sistem.Ime, 길이)) return -22;
            if (INDEX == 20) {
                int Datoteka = pomnilnik_datotečni_sistem.FIND_vnos(pomnilnik_datotečni_sistem.Ime, 길이);
                if (Datoteka < 0) return Datoteka;
                int Velikost = pomnilnik_datotečni_sistem.spremeniti_velikost_Seznam[Datoteka];
                if (Velikost > podatki_spremeniti_velikost) return -90;
                int naslov = naprava_VALUE.Datoteka_pomnilnik() + Datoteka * pomnilnik_datotečni_sistem.최대크기;
                for (int 수 = 0; 수 < Velikost; 수++) 실행관리.수쓰기(SECOND_operand + 4 + 수 * 4, naprava_VALUE.기억읽기(naslov + 수));
                return Velikost;
            }
            if (다 < 0 || 다 > podatki_spremeniti_velikost) return -22;
            if (다 > pomnilnik_datotečni_sistem.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) pomnilnik_datotečni_sistem.Uredi_VALUE[수] = 실행관리.수(SECOND_operand + 4 + 수 * 4) & 255;
            return pomnilnik_datotečni_sistem.Store_VALUE(pomnilnik_datotečni_sistem.Ime, 길이, pomnilnik_datotečni_sistem.Uredi_VALUE, 다);
        }
        return -38;
    }
}
