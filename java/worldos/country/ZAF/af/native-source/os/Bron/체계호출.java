// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 gebruiker wyser/길이는 toegang_inskrywing 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int ARRAY_lengte(int adres) {
        if (!실행관리.snit(adres, 4)) return -14;
        int lengte_VALUE = 실행관리.수(adres);
        if (lengte_VALUE < 0 || lengte_VALUE > (실행관리.gebruiker_beëindig - adres - 4) / 4) return -14;
        return lengte_VALUE;
    }

    public static int Proses_VALUE_inskrywing(int INDEX, int 가, int 나, int 다, int 라, int 마) {
        if (INDEX == 30) return 파일서술자관리.skep_lêer(가, 나, 다);
        if (INDEX == 31) return 파일서술자관리.파일읽기(가, 나, 다);
        if (INDEX == 32) return 파일서술자관리.skryf_lêer(가, 나, 다);
        if (INDEX == 33) return 파일서술자관리.sluit_lêer(가);
        if (INDEX == 34) return 파일서술자관리.soek_lêer(가, 나, 다);
        if (INDEX == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (INDEX == 36) return 파일서술자관리.서술자복제(가, 나, true, 0);
        if (INDEX == 37) return 파일서술자관리.파일상태읽기(가, 나);
        if (INDEX == 38) return 파일서술자관리.verwyder_lêer_inskrywing_naam(가);
        if (INDEX == 39) return 파일서술자관리.stel_lêer_lengte(가, 나);
        if (INDEX == 40) return 파일서술자관리.서술자제어(가, 나, 다);
        if (INDEX == 41) return 파일서술자관리.통신종단점만들기(가, 나, 다);
        if (INDEX == 42) return 파일서술자관리.BIND_adres(가, 나, 다);
        if (INDEX == 43) return 파일서술자관리.자료전문보내기(가, 나, 다, 라, 마);
        if (INDEX == 44) return 파일서술자관리.자료전문받기(가, 나, 다, 라, 마);
        if (INDEX == 45) return 파일서술자관리.통신주소읽기(가, 나, 다);
        if (INDEX == 46) return 파일서술자관리.수신대기정하기(가, 나);
        if (INDEX == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.sinc();
        }
        if (INDEX == 1) {
            int lengte_VALUE = ARRAY_lengte(가);
            if (lengte_VALUE < 0) return lengte_VALUE;
            if (lengte_VALUE > 4096) return -90;
            for (int karakter_VALUE = 0; karakter_VALUE < lengte_VALUE; karakter_VALUE++) SMS_Terminaal.문자(실행관리.수(가 + 4 + karakter_VALUE * 4) & 65535);
            return lengte_VALUE;
        }
        if (INDEX == 2) return 실행관리.argument_COUNT;
        if (INDEX == 3) return 가 >= 0 && 가 < 실행관리.argument_COUNT ? 실행관리.argument_adres[가] : 0;
        if (INDEX == 10) return Netwerk_Stapel.skep(가);
        if (INDEX == 11) {
            int lengte_VALUE = ARRAY_lengte(라);
            if (lengte_VALUE < 0) return lengte_VALUE;
            if (마 < 0 || 마 > lengte_VALUE || 마 > 1024) return -90;
            for (int Posisie = 0; Posisie < 마; Posisie++) 임시자료[Posisie] = 실행관리.수(라 + 4 + Posisie * 4) & 255;
            return Netwerk_Stapel.e_pos(가, 나, 다, 임시자료, 마);
        }
        if (INDEX == 12) {
            int lengte_VALUE = ARRAY_lengte(나);
            if (lengte_VALUE < 0) return lengte_VALUE;
            if (다 < 0 || 다 > 2000) return -22;
            int maatreël = Netwerk_Stapel.받기(가, 임시자료, lengte_VALUE < 1024 ? lengte_VALUE : 1024, 다);
            if (maatreël >= 0) for (int Posisie = 0; Posisie < maatreël; Posisie++) 실행관리.수쓰기(나 + 4 + Posisie * 4, 임시자료[Posisie]);
            return maatreël;
        }
        if (INDEX == 13) return Netwerk_Stapel.Sluit(가);
        if (INDEX == 14) return Netwerk_Stapel.내주소;
        if (INDEX == 15) return Netwerk_Stapel.portuur_adres(가);
        if (INDEX == 16) return Netwerk_Stapel.상대접속번호(가);
        if (INDEX == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Terminaal.문자(가); return 1;
        }
        if (INDEX == 20 || INDEX == 21) {
            int naam_verstel = ARRAY_lengte(가), data_verstel = ARRAY_lengte(나);
            if (naam_verstel < 0 || data_verstel < 0) return -14;
            if (naam_verstel < 1 || naam_verstel > 64) return -22;
            int lengte_VALUE = 0;
            while (lengte_VALUE < naam_verstel && 실행관리.수(가 + 4 + lengte_VALUE * 4) != 0) {
                Geheue_lêerstelsel.Naam[lengte_VALUE] = 실행관리.수(가 + 4 + lengte_VALUE * 4);
                lengte_VALUE++;
            }
            if (!Geheue_lêerstelsel.tjek_naam(Geheue_lêerstelsel.Naam, lengte_VALUE)) return -22;
            if (INDEX == 20) {
                int Lêer = Geheue_lêerstelsel.FIND_inskrywing(Geheue_lêerstelsel.Naam, lengte_VALUE);
                if (Lêer < 0) return Lêer;
                int Grootte = Geheue_lêerstelsel.verstel_Lys[Lêer];
                if (Grootte > data_verstel) return -90;
                int adres = mobiel_VALUE.lêer_Geheue() + Lêer * Geheue_lêerstelsel.최대크기;
                for (int 수 = 0; 수 < Grootte; 수++) 실행관리.수쓰기(나 + 4 + 수 * 4, mobiel_VALUE.기억읽기(adres + 수));
                return Grootte;
            }
            if (다 < 0 || 다 > data_verstel) return -22;
            if (다 > Geheue_lêerstelsel.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) Geheue_lêerstelsel.redigeer_VALUE[수] = 실행관리.수(나 + 4 + 수 * 4) & 255;
            return Geheue_lêerstelsel.bêre_VALUE(Geheue_lêerstelsel.Naam, lengte_VALUE, Geheue_lêerstelsel.redigeer_VALUE, 다);
        }
        return -38;
    }
}
