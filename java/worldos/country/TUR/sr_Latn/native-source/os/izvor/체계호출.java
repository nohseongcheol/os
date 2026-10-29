// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 korisnik pokazivač/길이는 pristup_stavka 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int 배열길이(int adresa) {
        if (!실행관리.klip(adresa, 4)) return -14;
        int 길이 = 실행관리.수(adresa);
        if (길이 < 0 || 길이 > (실행관리.korisnik_završiti_razgovor - adresa - 4) / 4) return -14;
        return 길이;
    }

    public static int Proces_VALUE_stavka(int INDEX, int 가, int SECOND_operand, int 다, int 라, int 마) {
        if (INDEX == 30) return 파일서술자관리.otvoren_Datoteka(가, SECOND_operand, 다);
        if (INDEX == 31) return 파일서술자관리.파일읽기(가, SECOND_operand, 다);
        if (INDEX == 32) return 파일서술자관리.파일쓰기(가, SECOND_operand, 다);
        if (INDEX == 33) return 파일서술자관리.Zatvori_Datoteka(가);
        if (INDEX == 34) return 파일서술자관리.tražiti_Datoteka(가, SECOND_operand, 다);
        if (INDEX == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (INDEX == 36) return 파일서술자관리.서술자복제(가, SECOND_operand, true, 0);
        if (INDEX == 37) return 파일서술자관리.파일상태읽기(가, SECOND_operand);
        if (INDEX == 38) return 파일서술자관리.ukloniti_Datoteka_stavka_ime(가);
        if (INDEX == 39) return 파일서술자관리.파일길이정하기(가, SECOND_operand);
        if (INDEX == 40) return 파일서술자관리.서술자제어(가, SECOND_operand, 다);
        if (INDEX == 41) return 파일서술자관리.Create_učesnik(가, SECOND_operand, 다);
        if (INDEX == 42) return 파일서술자관리.povezati_adresa(가, SECOND_operand, 다);
        if (INDEX == 43) return 파일서술자관리.poslati_datagram_podaci(가, SECOND_operand, 다, 라, 마);
        if (INDEX == 44) return 파일서술자관리.primiti_datagram_podaci(가, SECOND_operand, 다, 라, 마);
        if (INDEX == 45) return 파일서술자관리.통신주소읽기(가, SECOND_operand, 다);
        if (INDEX == 46) return 파일서술자관리.skup_primiti_TIMEOUT(가, SECOND_operand);
        if (INDEX == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.sinhronizovati();
        }
        if (INDEX == 1) {
            int 길이 = 배열길이(가);
            if (길이 < 0) return 길이;
            if (길이 > 4096) return -90;
            for (int znak_VALUE = 0; znak_VALUE < 길이; znak_VALUE++) SMS_Terminal.문자(실행관리.수(가 + 4 + znak_VALUE * 4) & 65535);
            return 길이;
        }
        if (INDEX == 2) return 실행관리.argument_COUNT;
        if (INDEX == 3) return 가 >= 0 && 가 < 실행관리.argument_COUNT ? 실행관리.argument_adresa[가] : 0;
        if (INDEX == 10) return Mreža_stek.otvoren(가);
        if (INDEX == 11) {
            int 길이 = 배열길이(라);
            if (길이 < 0) return 길이;
            if (마 < 0 || 마 > 길이 || 마 > 1024) return -90;
            for (int pozicija = 0; pozicija < 마; pozicija++) 임시자료[pozicija] = 실행관리.수(라 + 4 + pozicija * 4) & 255;
            return Mreža_stek.poslati(가, SECOND_operand, 다, 임시자료, 마);
        }
        if (INDEX == 12) {
            int 길이 = 배열길이(SECOND_operand);
            if (길이 < 0) return 길이;
            if (다 < 0 || 다 > 2000) return -22;
            int KR = Mreža_stek.primiti(가, 임시자료, 길이 < 1024 ? 길이 : 1024, 다);
            if (KR >= 0) for (int pozicija = 0; pozicija < KR; pozicija++) 실행관리.수쓰기(SECOND_operand + 4 + pozicija * 4, 임시자료[pozicija]);
            return KR;
        }
        if (INDEX == 13) return Mreža_stek.Zatvori(가);
        if (INDEX == 14) return Mreža_stek.내주소;
        if (INDEX == 15) return Mreža_stek.ravnopravni_uređaj_adresa(가);
        if (INDEX == 16) return Mreža_stek.ravnopravni_uređaj_broj_porta(가);
        if (INDEX == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Terminal.문자(가); return 1;
        }
        if (INDEX == 20 || INDEX == 21) {
            int ime_promeniti_veličinu = 배열길이(가), podaci_promeniti_veličinu = 배열길이(SECOND_operand);
            if (ime_promeniti_veličinu < 0 || podaci_promeniti_veličinu < 0) return -14;
            if (ime_promeniti_veličinu < 1 || ime_promeniti_veličinu > 64) return -22;
            int 길이 = 0;
            while (길이 < ime_promeniti_veličinu && 실행관리.수(가 + 4 + 길이 * 4) != 0) {
                Memorija_sistem_datoteka.ime[길이] = 실행관리.수(가 + 4 + 길이 * 4);
                길이++;
            }
            if (!Memorija_sistem_datoteka.proveriti_ime(Memorija_sistem_datoteka.ime, 길이)) return -22;
            if (INDEX == 20) {
                int Datoteka = Memorija_sistem_datoteka.FIND_stavka(Memorija_sistem_datoteka.ime, 길이);
                if (Datoteka < 0) return Datoteka;
                int promeniti_veličinu = Memorija_sistem_datoteka.promeniti_veličinu_Lista[Datoteka];
                if (promeniti_veličinu > podaci_promeniti_veličinu) return -90;
                int adresa = uređaj_VALUE.Datoteka_Memorija() + Datoteka * Memorija_sistem_datoteka.최대크기;
                for (int 수 = 0; 수 < promeniti_veličinu; 수++) 실행관리.수쓰기(SECOND_operand + 4 + 수 * 4, uređaj_VALUE.기억읽기(adresa + 수));
                return promeniti_veličinu;
            }
            if (다 < 0 || 다 > podaci_promeniti_veličinu) return -22;
            if (다 > Memorija_sistem_datoteka.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) Memorija_sistem_datoteka.Uredi_VALUE[수] = 실행관리.수(SECOND_operand + 4 + 수 * 4) & 255;
            return Memorija_sistem_datoteka.Store_VALUE(Memorija_sistem_datoteka.ime, 길이, Memorija_sistem_datoteka.Uredi_VALUE, 다);
        }
        return -38;
    }
}
