// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 korisnik pokazivač/길이는 pristup_unos 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int niz_dužina(int adresa) {
        if (!실행관리.isječak(adresa, 4)) return -14;
        int dužina_VALUE = 실행관리.수(adresa);
        if (dužina_VALUE < 0 || dužina_VALUE > (실행관리.korisnik_završiti - adresa - 4) / 4) return -14;
        return dužina_VALUE;
    }

    public static int proces_VALUE_unos(int INDEX, int 가, int SECOND_operand, int 다, int 라, int 마) {
        if (INDEX == 30) return 파일서술자관리.kreirati_fajl(가, SECOND_operand, 다);
        if (INDEX == 31) return 파일서술자관리.파일읽기(가, SECOND_operand, 다);
        if (INDEX == 32) return 파일서술자관리.pisati_fajl(가, SECOND_operand, 다);
        if (INDEX == 33) return 파일서술자관리.zatvoriti_fajl(가);
        if (INDEX == 34) return 파일서술자관리.tražiti_fajl(가, SECOND_operand, 다);
        if (INDEX == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (INDEX == 36) return 파일서술자관리.서술자복제(가, SECOND_operand, true, 0);
        if (INDEX == 37) return 파일서술자관리.파일상태읽기(가, SECOND_operand);
        if (INDEX == 38) return 파일서술자관리.ukloniti_fajl_unos_naziv(가);
        if (INDEX == 39) return 파일서술자관리.skup_fajl_dužina(가, SECOND_operand);
        if (INDEX == 40) return 파일서술자관리.서술자제어(가, SECOND_operand, 다);
        if (INDEX == 41) return 파일서술자관리.Create_završna_tačka(가, SECOND_operand, 다);
        if (INDEX == 42) return 파일서술자관리.BIND_adresa(가, SECOND_operand, 다);
        if (INDEX == 43) return 파일서술자관리.자료전문보내기(가, SECOND_operand, 다, 라, 마);
        if (INDEX == 44) return 파일서술자관리.자료전문받기(가, SECOND_operand, 다, 라, 마);
        if (INDEX == 45) return 파일서술자관리.통신주소읽기(가, SECOND_operand, 다);
        if (INDEX == 46) return 파일서술자관리.수신대기정하기(가, SECOND_operand);
        if (INDEX == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.sinhronizirati();
        }
        if (INDEX == 1) {
            int dužina_VALUE = niz_dužina(가);
            if (dužina_VALUE < 0) return dužina_VALUE;
            if (dužina_VALUE > 4096) return -90;
            for (int znak_VALUE = 0; znak_VALUE < dužina_VALUE; znak_VALUE++) SMS_Terminal.문자(실행관리.수(가 + 4 + znak_VALUE * 4) & 65535);
            return dužina_VALUE;
        }
        if (INDEX == 2) return 실행관리.argument_COUNT;
        if (INDEX == 3) return 가 >= 0 && 가 < 실행관리.argument_COUNT ? 실행관리.argument_adresa[가] : 0;
        if (INDEX == 10) return Mreža_snop.Otvori(가);
        if (INDEX == 11) {
            int dužina_VALUE = niz_dužina(라);
            if (dužina_VALUE < 0) return dužina_VALUE;
            if (마 < 0 || 마 > dužina_VALUE || 마 > 1024) return -90;
            for (int Pozicija = 0; Pozicija < 마; Pozicija++) 임시자료[Pozicija] = 실행관리.수(라 + 4 + Pozicija * 4) & 255;
            return Mreža_snop.poslati(가, SECOND_operand, 다, 임시자료, 마);
        }
        if (INDEX == 12) {
            int dužina_VALUE = niz_dužina(SECOND_operand);
            if (dužina_VALUE < 0) return dužina_VALUE;
            if (다 < 0 || 다 > 2000) return -22;
            int mjera = Mreža_snop.받기(가, 임시자료, dužina_VALUE < 1024 ? dužina_VALUE : 1024, 다);
            if (mjera >= 0) for (int Pozicija = 0; Pozicija < mjera; Pozicija++) 실행관리.수쓰기(SECOND_operand + 4 + Pozicija * 4, 임시자료[Pozicija]);
            return mjera;
        }
        if (INDEX == 13) return Mreža_snop.Zatvori(가);
        if (INDEX == 14) return Mreža_snop.내주소;
        if (INDEX == 15) return Mreža_snop.peer_adresa(가);
        if (INDEX == 16) return Mreža_snop.peer_broj_priključka(가);
        if (INDEX == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Terminal.문자(가); return 1;
        }
        if (INDEX == 20 || INDEX == 21) {
            int naziv_podesiti_veličinu = niz_dužina(가), podaci_podesiti_veličinu = niz_dužina(SECOND_operand);
            if (naziv_podesiti_veličinu < 0 || podaci_podesiti_veličinu < 0) return -14;
            if (naziv_podesiti_veličinu < 1 || naziv_podesiti_veličinu > 64) return -22;
            int dužina_VALUE = 0;
            while (dužina_VALUE < naziv_podesiti_veličinu && 실행관리.수(가 + 4 + dužina_VALUE * 4) != 0) {
                Memorija_fajl_sistem.Naziv[dužina_VALUE] = 실행관리.수(가 + 4 + dužina_VALUE * 4);
                dužina_VALUE++;
            }
            if (!Memorija_fajl_sistem.ček_naziv(Memorija_fajl_sistem.Naziv, dužina_VALUE)) return -22;
            if (INDEX == 20) {
                int Fajl = Memorija_fajl_sistem.FIND_unos(Memorija_fajl_sistem.Naziv, dužina_VALUE);
                if (Fajl < 0) return Fajl;
                int Veličina = Memorija_fajl_sistem.podesiti_veličinu_spisak[Fajl];
                if (Veličina > podaci_podesiti_veličinu) return -90;
                int adresa = uređaj_VALUE.fajl_Memorija() + Fajl * Memorija_fajl_sistem.최대크기;
                for (int 수 = 0; 수 < Veličina; 수++) 실행관리.수쓰기(SECOND_operand + 4 + 수 * 4, uređaj_VALUE.기억읽기(adresa + 수));
                return Veličina;
            }
            if (다 < 0 || 다 > podaci_podesiti_veličinu) return -22;
            if (다 > Memorija_fajl_sistem.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) Memorija_fajl_sistem.uređivati_VALUE[수] = 실행관리.수(SECOND_operand + 4 + 수 * 4) & 255;
            return Memorija_fajl_sistem.Store_VALUE(Memorija_fajl_sistem.Naziv, dužina_VALUE, Memorija_fajl_sistem.uređivati_VALUE, 다);
        }
        return -38;
    }
}
