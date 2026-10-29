// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 používateľ ukazovateľ/길이는 prístup_položka 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int pole_dĺžka(int adresa) {
        if (!실행관리.klip(adresa, 4)) return -14;
        int dĺžka_VALUE = 실행관리.수(adresa);
        if (dĺžka_VALUE < 0 || dĺžka_VALUE > (실행관리.používateľ_ukončiť_hovor - adresa - 4) / 4) return -14;
        return dĺžka_VALUE;
    }

    public static int Proces_VALUE_položka(int INDEX, int 가, int SECOND_operand, int 다, int 라, int 마) {
        if (INDEX == 30) return 파일서술자관리.otvoriť_Súbor(가, SECOND_operand, 다);
        if (INDEX == 31) return 파일서술자관리.파일읽기(가, SECOND_operand, 다);
        if (INDEX == 32) return 파일서술자관리.zapísať_Súbor(가, SECOND_operand, 다);
        if (INDEX == 33) return 파일서술자관리.Zavrieť_Súbor(가);
        if (INDEX == 34) return 파일서술자관리.hľadať_Súbor(가, SECOND_operand, 다);
        if (INDEX == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (INDEX == 36) return 파일서술자관리.서술자복제(가, SECOND_operand, true, 0);
        if (INDEX == 37) return 파일서술자관리.파일상태읽기(가, SECOND_operand);
        if (INDEX == 38) return 파일서술자관리.odobrať_Súbor_položka_názov(가);
        if (INDEX == 39) return 파일서술자관리.množina_Súbor_dĺžka(가, SECOND_operand);
        if (INDEX == 40) return 파일서술자관리.서술자제어(가, SECOND_operand, 다);
        if (INDEX == 41) return 파일서술자관리.Create_účastník(가, SECOND_operand, 다);
        if (INDEX == 42) return 파일서술자관리.BIND_adresa(가, SECOND_operand, 다);
        if (INDEX == 43) return 파일서술자관리.odoslať_datagram_údaje(가, SECOND_operand, 다, 라, 마);
        if (INDEX == 44) return 파일서술자관리.dostať_datagram_údaje(가, SECOND_operand, 다, 라, 마);
        if (INDEX == 45) return 파일서술자관리.통신주소읽기(가, SECOND_operand, 다);
        if (INDEX == 46) return 파일서술자관리.množina_dostať_TIMEOUT(가, SECOND_operand);
        if (INDEX == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.synchronizovať();
        }
        if (INDEX == 1) {
            int dĺžka_VALUE = pole_dĺžka(가);
            if (dĺžka_VALUE < 0) return dĺžka_VALUE;
            if (dĺžka_VALUE > 4096) return -90;
            for (int znak_VALUE = 0; znak_VALUE < dĺžka_VALUE; znak_VALUE++) SMS_Terminál.문자(실행관리.수(가 + 4 + znak_VALUE * 4) & 65535);
            return dĺžka_VALUE;
        }
        if (INDEX == 2) return 실행관리.argument_COUNT;
        if (INDEX == 3) return 가 >= 0 && 가 < 실행관리.argument_COUNT ? 실행관리.argument_adresa[가] : 0;
        if (INDEX == 10) return sieť_Vrstvy.Otvoriť(가);
        if (INDEX == 11) {
            int dĺžka_VALUE = pole_dĺžka(라);
            if (dĺžka_VALUE < 0) return dĺžka_VALUE;
            if (마 < 0 || 마 > dĺžka_VALUE || 마 > 1024) return -90;
            for (int Pozícia = 0; Pozícia < 마; Pozícia++) 임시자료[Pozícia] = 실행관리.수(라 + 4 + Pozícia * 4) & 255;
            return sieť_Vrstvy.odoslať(가, SECOND_operand, 다, 임시자료, 마);
        }
        if (INDEX == 12) {
            int dĺžka_VALUE = pole_dĺžka(SECOND_operand);
            if (dĺžka_VALUE < 0) return dĺžka_VALUE;
            if (다 < 0 || 다 > 2000) return -22;
            int KR = sieť_Vrstvy.dostať(가, 임시자료, dĺžka_VALUE < 1024 ? dĺžka_VALUE : 1024, 다);
            if (KR >= 0) for (int Pozícia = 0; Pozícia < KR; Pozícia++) 실행관리.수쓰기(SECOND_operand + 4 + Pozícia * 4, 임시자료[Pozícia]);
            return KR;
        }
        if (INDEX == 13) return sieť_Vrstvy.Zatvoriť(가);
        if (INDEX == 14) return sieť_Vrstvy.내주소;
        if (INDEX == 15) return sieť_Vrstvy.partnerský_uzol_adresa(가);
        if (INDEX == 16) return sieť_Vrstvy.partnerský_uzol_číslo_portu(가);
        if (INDEX == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Terminál.문자(가); return 1;
        }
        if (INDEX == 20 || INDEX == 21) {
            int názov_zmeniť_veľkosť = pole_dĺžka(가), údaje_zmeniť_veľkosť = pole_dĺžka(SECOND_operand);
            if (názov_zmeniť_veľkosť < 0 || údaje_zmeniť_veľkosť < 0) return -14;
            if (názov_zmeniť_veľkosť < 1 || názov_zmeniť_veľkosť > 64) return -22;
            int dĺžka_VALUE = 0;
            while (dĺžka_VALUE < názov_zmeniť_veľkosť && 실행관리.수(가 + 4 + dĺžka_VALUE * 4) != 0) {
                Pamäť_systém_súborov.Názov[dĺžka_VALUE] = 실행관리.수(가 + 4 + dĺžka_VALUE * 4);
                dĺžka_VALUE++;
            }
            if (!Pamäť_systém_súborov.skontrolovať_názov(Pamäť_systém_súborov.Názov, dĺžka_VALUE)) return -22;
            if (INDEX == 20) {
                int Súbor = Pamäť_systém_súborov.FIND_položka(Pamäť_systém_súborov.Názov, dĺžka_VALUE);
                if (Súbor < 0) return Súbor;
                int Veľkosť = Pamäť_systém_súborov.zmeniť_veľkosť_Zoznam[Súbor];
                if (Veľkosť > údaje_zmeniť_veľkosť) return -90;
                int adresa = telefón_VALUE.Súbor_Pamäť() + Súbor * Pamäť_systém_súborov.최대크기;
                for (int 수 = 0; 수 < Veľkosť; 수++) 실행관리.수쓰기(SECOND_operand + 4 + 수 * 4, telefón_VALUE.기억읽기(adresa + 수));
                return Veľkosť;
            }
            if (다 < 0 || 다 > údaje_zmeniť_veľkosť) return -22;
            if (다 > Pamäť_systém_súborov.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) Pamäť_systém_súborov.úprava_VALUE[수] = 실행관리.수(SECOND_operand + 4 + 수 * 4) & 255;
            return Pamäť_systém_súborov.Store_VALUE(Pamäť_systém_súborov.Názov, dĺžka_VALUE, Pamäť_systém_súborov.úprava_VALUE, 다);
        }
        return -38;
    }
}
