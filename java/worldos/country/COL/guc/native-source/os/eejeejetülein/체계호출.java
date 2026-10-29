// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 ka_yataayakalü 포인터/길이는 a_ttaaya_ekeroliaa 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int matüriisü_akaliaa(int ejepüsee) {
        if (!실행관리.külipü_ayaakuaapijana(ejepüsee, 4)) return -14;
        int akaliaa_ajutuu = 실행관리.수(ejepüsee);
        if (akaliaa_ajutuu < 0 || akaliaa_ajutuu > (실행관리.ka_yataayakalü_ajattiraa - ejepüsee - 4) / 4) return -14;
        return akaliaa_ajutuu;
    }

    public static int 처리(int ee_iyatialujuna, int 가, int 나, int 다, int 라, int 마) {
        if (ee_iyatialujuna == 30) return 파일서술자관리.파일열기(가, 나, 다);
        if (ee_iyatialujuna == 31) return 파일서술자관리.파일읽기(가, 나, 다);
        if (ee_iyatialujuna == 32) return 파일서술자관리.ashajaa_anaajaalaa(가, 나, 다);
        if (ee_iyatialujuna == 33) return 파일서술자관리.asürülaa_anaajaalaa(가);
        if (ee_iyatialujuna == 34) return 파일서술자관리.파일위치옮기기(가, 나, 다);
        if (ee_iyatialujuna == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (ee_iyatialujuna == 36) return 파일서술자관리.서술자복제(가, 나, true, 0);
        if (ee_iyatialujuna == 37) return 파일서술자관리.파일상태읽기(가, 나);
        if (ee_iyatialujuna == 38) return 파일서술자관리.파일이름지우기(가);
        if (ee_iyatialujuna == 39) return 파일서술자관리.파일길이정하기(가, 나);
        if (ee_iyatialujuna == 40) return 파일서술자관리.서술자제어(가, 나, 다);
        if (ee_iyatialujuna == 41) return 파일서술자관리.통신종단점만들기(가, 나, 다);
        if (ee_iyatialujuna == 42) return 파일서술자관리.alaasajaa_ejepüsee(가, 나, 다);
        if (ee_iyatialujuna == 43) return 파일서술자관리.자료전문보내기(가, 나, 다, 라, 마);
        if (ee_iyatialujuna == 44) return 파일서술자관리.자료전문받기(가, 나, 다, 라, 마);
        if (ee_iyatialujuna == 45) return 파일서술자관리.통신주소읽기(가, 나, 다);
        if (ee_iyatialujuna == 46) return 파일서술자관리.수신대기정하기(가, 나);
        if (ee_iyatialujuna == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.awanaawajaa();
        }
        if (ee_iyatialujuna == 1) {
            int akaliaa_ajutuu = matüriisü_akaliaa(가);
            if (akaliaa_ajutuu < 0) return akaliaa_ajutuu;
            if (akaliaa_ajutuu > 4096) return -90;
            for (int jeerü_ajutuu = 0; jeerü_ajutuu < akaliaa_ajutuu; jeerü_ajutuu++) 문자단말.문자(실행관리.수(가 + 4 + jeerü_ajutuu * 4) & 65535);
            return akaliaa_ajutuu;
        }
        if (ee_iyatialujuna == 2) return 실행관리.인수수;
        if (ee_iyatialujuna == 3) return 가 >= 0 && 가 < 실행관리.인수수 ? 실행관리.ajutuu_ejepüsee[가] : 0;
        if (ee_iyatialujuna == 10) return 통신망.열기(가);
        if (ee_iyatialujuna == 11) {
            int akaliaa_ajutuu = matüriisü_akaliaa(라);
            if (akaliaa_ajutuu < 0) return akaliaa_ajutuu;
            if (마 < 0 || 마 > akaliaa_ajutuu || 마 > 1024) return -90;
            for (int 위치 = 0; 위치 < 마; 위치++) 임시자료[위치] = 실행관리.수(라 + 4 + 위치 * 4) & 255;
            return 통신망.ajütaa(가, 나, 다, 임시자료, 마);
        }
        if (ee_iyatialujuna == 12) {
            int akaliaa_ajutuu = matüriisü_akaliaa(나);
            if (akaliaa_ajutuu < 0) return akaliaa_ajutuu;
            if (다 < 0 || 다 > 2000) return -22;
            int 결과 = 통신망.받기(가, 임시자료, akaliaa_ajutuu < 1024 ? akaliaa_ajutuu : 1024, 다);
            if (결과 >= 0) for (int 위치 = 0; 위치 < 결과; 위치++) 실행관리.수쓰기(나 + 4 + 위치 * 4, 임시자료[위치]);
            return 결과;
        }
        if (ee_iyatialujuna == 13) return 통신망.asürülaa(가);
        if (ee_iyatialujuna == 14) return 통신망.내주소;
        if (ee_iyatialujuna == 15) return 통신망.wanaawasü_ejepüsee(가);
        if (ee_iyatialujuna == 16) return 통신망.상대접속번호(가);
        if (ee_iyatialujuna == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            문자단말.문자(가); return 1;
        }
        if (ee_iyatialujuna == 20 || ee_iyatialujuna == 21) {
            int 이름크기 = matüriisü_akaliaa(가), 자료크기 = matüriisü_akaliaa(나);
            if (이름크기 < 0 || 자료크기 < 0) return -14;
            if (이름크기 < 1 || 이름크기 > 64) return -22;
            int akaliaa_ajutuu = 0;
            while (akaliaa_ajutuu < 이름크기 && 실행관리.수(가 + 4 + akaliaa_ajutuu * 4) != 0) {
                주기억파일체계.이름[akaliaa_ajutuu] = 실행관리.수(가 + 4 + akaliaa_ajutuu * 4);
                akaliaa_ajutuu++;
            }
            if (!주기억파일체계.이름검사(주기억파일체계.이름, akaliaa_ajutuu)) return -22;
            if (ee_iyatialujuna == 20) {
                int anaajaalaa = 주기억파일체계.찾기(주기억파일체계.이름, akaliaa_ajutuu);
                if (anaajaalaa < 0) return anaajaalaa;
                int 크기 = 주기억파일체계.크기들[anaajaalaa];
                if (크기 > 자료크기) return -90;
                int ejepüsee = serulaalü_ajutuu.파일기억() + anaajaalaa * 주기억파일체계.최대크기;
                for (int 수 = 0; 수 < 크기; 수++) 실행관리.수쓰기(나 + 4 + 수 * 4, serulaalü_ajutuu.기억읽기(ejepüsee + 수));
                return 크기;
            }
            if (다 < 0 || 다 > 자료크기) return -22;
            if (다 > 주기억파일체계.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) 주기억파일체계.anaataa_ajutuu[수] = 실행관리.수(나 + 4 + 수 * 4) & 255;
            return 주기억파일체계.저장(주기억파일체계.이름, akaliaa_ajutuu, 주기억파일체계.anaataa_ajutuu, 다);
        }
        return -38;
    }
}
