// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 utilizator cursor/길이는 acces_intrare 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int ARRAY_lungime(int adresa) {
        if (!실행관리.clip(adresa, 4)) return -14;
        int lungime_VALUE = 실행관리.수(adresa);
        if (lungime_VALUE < 0 || lungime_VALUE > (실행관리.utilizator_termina_un_apel - adresa - 4) / 4) return -14;
        return lungime_VALUE;
    }

    public static int Proces_VALUE_intrare(int INDEX, int 가, int SECOND_operand, int 다, int 라, int 마) {
        if (INDEX == 30) return 파일서술자관리.crea_Fișier(가, SECOND_operand, 다);
        if (INDEX == 31) return 파일서술자관리.파일읽기(가, SECOND_operand, 다);
        if (INDEX == 32) return 파일서술자관리.scriere_Fișier(가, SECOND_operand, 다);
        if (INDEX == 33) return 파일서술자관리.închide_Fișier(가);
        if (INDEX == 34) return 파일서술자관리.căuta_Fișier(가, SECOND_operand, 다);
        if (INDEX == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (INDEX == 36) return 파일서술자관리.서술자복제(가, SECOND_operand, true, 0);
        if (INDEX == 37) return 파일서술자관리.파일상태읽기(가, SECOND_operand);
        if (INDEX == 38) return 파일서술자관리.elimina_Fișier_intrare_nume(가);
        if (INDEX == 39) return 파일서술자관리.set_Fișier_lungime(가, SECOND_operand);
        if (INDEX == 40) return 파일서술자관리.서술자제어(가, SECOND_operand, 다);
        if (INDEX == 41) return 파일서술자관리.crea_participant(가, SECOND_operand, 다);
        if (INDEX == 42) return 파일서술자관리.BIND_adresa(가, SECOND_operand, 다);
        if (INDEX == 43) return 파일서술자관리.trimite_diagramă_informații_date(가, SECOND_operand, 다, 라, 마);
        if (INDEX == 44) return 파일서술자관리.primi_diagramă_informații_date(가, SECOND_operand, 다, 라, 마);
        if (INDEX == 45) return 파일서술자관리.통신주소읽기(가, SECOND_operand, 다);
        if (INDEX == 46) return 파일서술자관리.set_primi_TIMEOUT(가, SECOND_operand);
        if (INDEX == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.sincroniz();
        }
        if (INDEX == 1) {
            int lungime_VALUE = ARRAY_lungime(가);
            if (lungime_VALUE < 0) return lungime_VALUE;
            if (lungime_VALUE > 4096) return -90;
            for (int caracter_VALUE = 0; caracter_VALUE < lungime_VALUE; caracter_VALUE++) SMS_Terminal.문자(실행관리.수(가 + 4 + caracter_VALUE * 4) & 65535);
            return lungime_VALUE;
        }
        if (INDEX == 2) return 실행관리.argument_COUNT;
        if (INDEX == 3) return 가 >= 0 && 가 < 실행관리.argument_COUNT ? 실행관리.argument_adresa[가] : 0;
        if (INDEX == 10) return rețea_Teanc.Deschide(가);
        if (INDEX == 11) {
            int lungime_VALUE = ARRAY_lungime(라);
            if (lungime_VALUE < 0) return lungime_VALUE;
            if (마 < 0 || 마 > lungime_VALUE || 마 > 1024) return -90;
            for (int Poziție = 0; Poziție < 마; Poziție++) 임시자료[Poziție] = 실행관리.수(라 + 4 + Poziție * 4) & 255;
            return rețea_Teanc.trimite(가, SECOND_operand, 다, 임시자료, 마);
        }
        if (INDEX == 12) {
            int lungime_VALUE = ARRAY_lungime(SECOND_operand);
            if (lungime_VALUE < 0) return lungime_VALUE;
            if (다 < 0 || 다 > 2000) return -22;
            int KR = rețea_Teanc.primi(가, 임시자료, lungime_VALUE < 1024 ? lungime_VALUE : 1024, 다);
            if (KR >= 0) for (int Poziție = 0; Poziție < KR; Poziție++) 실행관리.수쓰기(SECOND_operand + 4 + Poziție * 4, 임시자료[Poziție]);
            return KR;
        }
        if (INDEX == 13) return rețea_Teanc.Închide(가);
        if (INDEX == 14) return rețea_Teanc.내주소;
        if (INDEX == 15) return rețea_Teanc.pereche_adresa(가);
        if (INDEX == 16) return rețea_Teanc.pereche_număr_port(가);
        if (INDEX == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Terminal.문자(가); return 1;
        }
        if (INDEX == 20 || INDEX == 21) {
            int nume_dimensiona = ARRAY_lungime(가), date_dimensiona = ARRAY_lungime(SECOND_operand);
            if (nume_dimensiona < 0 || date_dimensiona < 0) return -14;
            if (nume_dimensiona < 1 || nume_dimensiona > 64) return -22;
            int lungime_VALUE = 0;
            while (lungime_VALUE < nume_dimensiona && 실행관리.수(가 + 4 + lungime_VALUE * 4) != 0) {
                Memorie_sistem_de_fișiere.Nume[lungime_VALUE] = 실행관리.수(가 + 4 + lungime_VALUE * 4);
                lungime_VALUE++;
            }
            if (!Memorie_sistem_de_fișiere.verifica_nume(Memorie_sistem_de_fișiere.Nume, lungime_VALUE)) return -22;
            if (INDEX == 20) {
                int Fișier = Memorie_sistem_de_fișiere.FIND_intrare(Memorie_sistem_de_fișiere.Nume, lungime_VALUE);
                if (Fișier < 0) return Fișier;
                int Mărime = Memorie_sistem_de_fișiere.dimensiona_Listă[Fișier];
                if (Mărime > date_dimensiona) return -90;
                int adresa = mobil_VALUE.Fișier_Memorie() + Fișier * Memorie_sistem_de_fișiere.최대크기;
                for (int 수 = 0; 수 < Mărime; 수++) 실행관리.수쓰기(SECOND_operand + 4 + 수 * 4, mobil_VALUE.기억읽기(adresa + 수));
                return Mărime;
            }
            if (다 < 0 || 다 > date_dimensiona) return -22;
            if (다 > Memorie_sistem_de_fișiere.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) Memorie_sistem_de_fișiere.edita_VALUE[수] = 실행관리.수(SECOND_operand + 4 + 수 * 4) & 255;
            return Memorie_sistem_de_fișiere.Store_VALUE(Memorie_sistem_de_fișiere.Nume, lungime_VALUE, Memorie_sistem_de_fișiere.edita_VALUE, 다);
        }
        return -38;
    }
}
