// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 ka_yataayakalü 과정의 파일서술자와 열린 anaajaalaa 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int 읽기쓰기 = 2, 만들기 = 64, 독점생성 = 128, ama_inrüinjiraa_TA = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] 열린기술 = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], 대상 = new int[서술자한도];
    static int[] 파일위치 = new int[서술자한도], 열기설정 = new int[서술자한도], 참조수 = new int[서술자한도];
    static int[] kusu_aapaaya = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] 경로이름 = new int[64], alate_eraa_atijaaya = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return 열린기술[파일서술자] - 1;
    }
    static int 빈서술자(int 시작) {
        for (int ee_iyatialujuna = 시작; ee_iyatialujuna < 서술자한도; ee_iyatialujuna++) if (열린기술[ee_iyatialujuna] == 0) return ee_iyatialujuna;
        return -24;
    }
    static int 빈기술() {
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 서술자한도; ee_iyatialujuna++) if (참조수[ee_iyatialujuna] == 0) return ee_iyatialujuna;
        return -24;
    }
    static int a_ataa(int 서술자, int 기술, int 파일종류, int 파일대상, int 설정) {
        열린기술[서술자] = 기술 + 1; 서술자설정[서술자] = (설정 & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; 대상[기술] = 파일대상; 참조수[기술] = 1;
        열기설정[기술] = 설정 & (3 | 이어쓰기 | 기다리지않기); 파일위치[기술] = 0;
        kusu_aapaaya[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void 과정시작() {
        과정정리();
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 3; ee_iyatialujuna++) a_ataa(ee_iyatialujuna, ee_iyatialujuna, 1, ee_iyatialujuna, ee_iyatialujuna == 0 ? 0 : 1);
    }
    static void 과정정리() {
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 서술자한도; ee_iyatialujuna++) if (열린기술[ee_iyatialujuna] != 0) asürülaa_anaajaalaa(ee_iyatialujuna);
    }
    static int asürülaa_anaajaalaa(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        열린기술[서술자] = 0; 서술자설정[서술자] = 0;
        참조수[기술]--;
        if (참조수[기술] == 0) {
            if (종류[기술] == 2) 주기억파일체계.열림수[대상[기술]]--;
            if (종류[기술] == 3 && kusu_aapaaya[기술] != 0) 통신망.asürülaa(kusu_aapaaya[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 waai_ajutuu 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int ejepüsee) {
        if (!실행관리.külipü_ayaakuaapijana(ejepüsee, 1)) return -14;
        int 위치 = serulaalü_ajutuu.기억읽기(ejepüsee) == '/' ? 1 : 0;
        for (int akaliaa_ajutuu = 0; akaliaa_ajutuu < 64; akaliaa_ajutuu++) {
            if (!실행관리.külipü_ayaakuaapijana(ejepüsee + 위치 + akaliaa_ajutuu, 1)) return -14;
            int ajutuu = serulaalü_ajutuu.기억읽기(ejepüsee + 위치 + akaliaa_ajutuu);
            경로이름[akaliaa_ajutuu] = ajutuu;
            if (ajutuu == 0) return akaliaa_ajutuu == 0 ? -2 : (주기억파일체계.이름검사(경로이름, akaliaa_ajutuu) ? akaliaa_ajutuu : -22);
            if (ajutuu == '/') return -20;
        }
        return -36;
    }
    static int 파일열기(int 이름주소, int 설정, int 허가) {
        int akaliaa_ajutuu = 경로읽기(이름주소);
        if (akaliaa_ajutuu < 0) return akaliaa_ajutuu;
        if ((설정 & ~(3 | 만들기 | 독점생성 | ama_inrüinjiraa_TA | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((설정 & 3) == 3 || ((설정 & ama_inrüinjiraa_TA) != 0 && (설정 & 3) == 0)) return -22;
        int anaajaalaa = 주기억파일체계.찾기(경로이름, akaliaa_ajutuu);
        if (anaajaalaa >= 0 && (설정 & (만들기 | 독점생성)) == (만들기 | 독점생성)) return -17;
        if (anaajaalaa == -2 && (설정 & 만들기) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = 빈기술();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (anaajaalaa == -2) {
            int 결과 = 주기억파일체계.저장(경로이름, akaliaa_ajutuu, 경로이름, 0);
            if (결과 < 0) return 결과;
            anaajaalaa = 주기억파일체계.찾기(경로이름, akaliaa_ajutuu);
            주기억파일체계.허가들[anaajaalaa] = 허가 & 511;
        }
        if (anaajaalaa < 0) return anaajaalaa;
        if ((설정 & ama_inrüinjiraa_TA) != 0) 주기억파일체계.크기들[anaajaalaa] = 0;
        주기억파일체계.열림수[anaajaalaa]++;
        return a_ataa(서술자, 기술, 2, anaajaalaa, 설정);
    }
    static int 파일읽기(int 서술자, int atijaaya_ejepüsee, int akaliaa_ajutuu) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (열기설정[기술] & 3) == 1) return -9;
        if (akaliaa_ajutuu < 0) return -22;
        if (akaliaa_ajutuu == 0) return 0;
        if (!실행관리.külipü_ayaakuaapijana(atijaaya_ejepüsee, akaliaa_ajutuu)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, atijaaya_ejepüsee, akaliaa_ajutuu, 0, 0);
        if (종류[기술] == 1) {
            int 받은수 = 0;
            while (받은수 < akaliaa_ajutuu) {
                int ajutuu = 문자단말.직렬읽기();
                if (ajutuu < 0) ajutuu = ajüttiaapala.읽기();
                if (ajutuu < 0) {
                    if (받은수 > 0) return 받은수;
                    if ((열기설정[기술] & 기다리지않기) != 0) return -11;
                    if (serulaalü_ajutuu.사용자남은밀리초() <= 10) return -11;
                    통신망.확인(); serulaalü_ajutuu.잠시양보();
                } else {
                    serulaalü_ajutuu.기억쓰기(atijaaya_ejepüsee + 받은수, ajutuu); 받은수++;
                }
            }
            return 받은수;
        }
        int anaajaalaa = 대상[기술], 위치 = 파일위치[기술];
        if (위치 >= 주기억파일체계.크기들[anaajaalaa]) return 0;
        if (akaliaa_ajutuu > 주기억파일체계.크기들[anaajaalaa] - 위치) akaliaa_ajutuu = 주기억파일체계.크기들[anaajaalaa] - 위치;
        int 원본주소 = serulaalü_ajutuu.파일기억() + anaajaalaa * 주기억파일체계.최대크기 + 위치;
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < akaliaa_ajutuu; ee_iyatialujuna++) serulaalü_ajutuu.기억쓰기(atijaaya_ejepüsee + ee_iyatialujuna, serulaalü_ajutuu.기억읽기(원본주소 + ee_iyatialujuna));
        파일위치[기술] += akaliaa_ajutuu;
        return akaliaa_ajutuu;
    }
    static int ashajaa_anaajaalaa(int 서술자, int atijaaya_ejepüsee, int akaliaa_ajutuu) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (열기설정[기술] & 3) == 0) return -9;
        if (akaliaa_ajutuu < 0) return -22;
        if (akaliaa_ajutuu == 0) return 0;
        if (!실행관리.külipü_ayaakuaapijana(atijaaya_ejepüsee, akaliaa_ajutuu)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 jalamüinjatü_ajutuu 주소가 필요하다.
        if (종류[기술] == 1) {
            if (akaliaa_ajutuu > 16384) akaliaa_ajutuu = 16384;
            for (int ee_iyatialujuna = 0; ee_iyatialujuna < akaliaa_ajutuu; ee_iyatialujuna++) {
                int ajutuu = serulaalü_ajutuu.기억읽기(atijaaya_ejepüsee + ee_iyatialujuna);
                문자단말.직렬바이트(ajutuu); 문자단말.화면문자(ajutuu);
            }
            return akaliaa_ajutuu;
        }
        int anaajaalaa = 대상[기술], 크기 = 주기억파일체계.크기들[anaajaalaa];
        int 위치 = (열기설정[기술] & 이어쓰기) != 0 ? 크기 : 파일위치[기술];
        if (위치 >= 주기억파일체계.최대크기) return -27;
        if (akaliaa_ajutuu > 주기억파일체계.최대크기 - 위치) akaliaa_ajutuu = 주기억파일체계.최대크기 - 위치;
        int jalamüinjatü_ejepüsee = serulaalü_ajutuu.파일기억() + anaajaalaa * 주기억파일체계.최대크기;
        for (int ee_iyatialujuna = 크기; ee_iyatialujuna < 위치; ee_iyatialujuna++) serulaalü_ajutuu.기억쓰기(jalamüinjatü_ejepüsee + ee_iyatialujuna, 0);
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < akaliaa_ajutuu; ee_iyatialujuna++) serulaalü_ajutuu.기억쓰기(jalamüinjatü_ejepüsee + 위치 + ee_iyatialujuna, serulaalü_ajutuu.기억읽기(atijaaya_ejepüsee + ee_iyatialujuna));
        파일위치[기술] = 위치 + akaliaa_ajutuu;
        if (위치 + akaliaa_ajutuu > 크기) 주기억파일체계.크기들[anaajaalaa] = 위치 + akaliaa_ajutuu;
        return akaliaa_ajutuu;
    }
    static int 파일위치옮기기(int 서술자, int 변위, int 기준) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (기준 < 0 || 기준 > 2) return -22;
        int apa_ajanaa_ajutuu = 기준 == 0 ? 0 : (기준 == 1 ? 파일위치[기술] : 주기억파일체계.크기들[대상[기술]]);
        if (변위 > 0 && apa_ajanaa_ajutuu > 2147483647 - 변위) return -75;
        if (변위 < 0 && 변위 < -apa_ajanaa_ajutuu) return -22;
        파일위치[기술] = apa_ajanaa_ajutuu + 변위;
        return 파일위치[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean 지정, int 설정) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return 지정 ? -9 : -22;
        if (지정 && 서술자 == 새서술자) return 새서술자;
        if (지정) { if (열린기술[새서술자] != 0) asürülaa_anaajaalaa(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        열린기술[새서술자] = 기술 + 1; 서술자설정[새서술자] = 설정; 참조수[기술]++;
        return 새서술자;
    }
    static int 파일이름지우기(int 이름주소) {
        int akaliaa_ajutuu = 경로읽기(이름주소);
        if (akaliaa_ajutuu < 0) return akaliaa_ajutuu;
        int anaajaalaa = 주기억파일체계.찾기(경로이름, akaliaa_ajutuu);
        if (anaajaalaa < 0) return anaajaalaa;
        주기억파일체계.이름들[anaajaalaa * 64] = 0;
        return 0;
    }
    static int 파일길이정하기(int 서술자, int akaliaa_ajutuu) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (열기설정[기술] & 3) == 0 || akaliaa_ajutuu < 0) return -22;
        if (akaliaa_ajutuu > 주기억파일체계.최대크기) return -27;
        int anaajaalaa = 대상[기술], ejepüsee = serulaalü_ajutuu.파일기억() + anaajaalaa * 주기억파일체계.최대크기;
        for (int ee_iyatialujuna = 주기억파일체계.크기들[anaajaalaa]; ee_iyatialujuna < akaliaa_ajutuu; ee_iyatialujuna++) serulaalü_ajutuu.기억쓰기(ejepüsee + ee_iyatialujuna, 0);
        주기억파일체계.크기들[anaajaalaa] = akaliaa_ajutuu;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int ejepüsee) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.külipü_ayaakuaapijana(ejepüsee, 48)) return -14;
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 12; ee_iyatialujuna++) 실행관리.수쓰기(ejepüsee + ee_iyatialujuna * 4, 0);
        int anaajaalaa = 대상[기술], 크기 = 종류[기술] == 2 ? 주기억파일체계.크기들[anaajaalaa] : 0;
        int 허가 = 종류[기술] == 2 ? 주기억파일체계.허가들[anaajaalaa] : 438;
        실행관리.수쓰기(ejepüsee, 1);
        실행관리.수쓰기(ejepüsee + 4, 종류[기술] == 2 ? anaajaalaa + 1 : 100 + 기술);
        실행관리.수쓰기(ejepüsee + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(ejepüsee + 12, 종류[기술] == 2 && 주기억파일체계.이름들[anaajaalaa * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(ejepüsee + 28, 크기); 실행관리.수쓰기(ejepüsee + 32, 512);
        실행관리.수쓰기(ejepüsee + 36, (크기 + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int aluwataaya, int ajutuu) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (aluwataaya == 0 || aluwataaya == 1030) return 서술자복제(서술자, ajutuu, false, aluwataaya == 1030 ? 1 : 0);
        if (aluwataaya == 1) return 서술자설정[서술자];
        if (aluwataaya == 2) { if ((ajutuu & ~1) != 0) return -22; 서술자설정[서술자] = ajutuu; return 0; }
        if (aluwataaya == 3) return 열기설정[기술];
        if (aluwataaya == 4) {
            if ((ajutuu & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            열기설정[기술] = (열기설정[기술] & 3) | (ajutuu & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int 통신종단점만들기(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = 빈기술();
        if (서술자 < 0 || 기술 < 0) return -24;
        return a_ataa(서술자, 기술, 3, 0, 읽기쓰기);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int ejepüsee_32(int ejepüsee) {
        return serulaalü_ajutuu.기억읽기(ejepüsee) << 24 | serulaalü_ajutuu.기억읽기(ejepüsee + 1) << 16
            | serulaalü_ajutuu.기억읽기(ejepüsee + 2) << 8 | serulaalü_ajutuu.기억읽기(ejepüsee + 3);
    }
    static int cheeke_ejepüsee(int ejepüsee, int akaliaa_ajutuu) {
        if (akaliaa_ajutuu < 16) return -22;
        if (!실행관리.külipü_ayaakuaapijana(ejepüsee, 16)) return -14;
        return 실행관리.짧은수(ejepüsee) == 2 ? 0 : -97;
    }
    static int alaasajaa_ejepüsee(int 서술자, int ejepüsee, int akaliaa_ajutuu) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int 결과 = cheeke_ejepüsee(ejepüsee, akaliaa_ajutuu);
        if (결과 < 0) return 결과;
        if (kusu_aapaaya[기술] != 0) return -22;
        int kusu_ejepüsee = ejepüsee_32(ejepüsee + 4);
        if (kusu_ejepüsee != 0 && kusu_ejepüsee != 통신망.내주소) return -99;
        int 접속번호 = serulaalü_ajutuu.기억읽기(ejepüsee + 2) << 8 | serulaalü_ajutuu.기억읽기(ejepüsee + 3);
        결과 = 통신망.열기(접속번호);
        if (결과 < 0) return 결과;
        kusu_aapaaya[기술] = 결과; 대상[기술] = kusu_ejepüsee;
        return 0;
    }
    static int 자동묶기(int 기술) {
        if (kusu_aapaaya[기술] != 0) return 0;
        int 결과 = 통신망.열기(0);
        if (결과 < 0) return 결과;
        kusu_aapaaya[기술] = 결과;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 요청 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int atijaaya_ejepüsee, int akaliaa_ajutuu, int 설정, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (설정 != 0) return -95;
        if (akaliaa_ajutuu < 0 || akaliaa_ajutuu > 1024) return -90;
        if (akaliaa_ajutuu != 0 && !실행관리.külipü_ayaakuaapijana(atijaaya_ejepüsee, akaliaa_ajutuu)) return -14;
        if (!실행관리.külipü_ayaakuaapijana(요청주소, 8)) return -14;
        int ejepüsee = 실행관리.수(요청주소);
        int 결과 = cheeke_ejepüsee(ejepüsee, 실행관리.수(요청주소 + 4));
        if (결과 < 0) return 결과;
        int 접속번호 = serulaalü_ajutuu.기억읽기(ejepüsee + 2) << 8 | serulaalü_ajutuu.기억읽기(ejepüsee + 3);
        if (접속번호 == 0) return -22;
        결과 = 자동묶기(기술);
        if (결과 < 0) return 결과;
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < akaliaa_ajutuu; ee_iyatialujuna++) alate_eraa_atijaaya[ee_iyatialujuna] = serulaalü_ajutuu.기억읽기(atijaaya_ejepüsee + ee_iyatialujuna);
        return 통신망.ajütaa(kusu_aapaaya[기술], ejepüsee_32(ejepüsee + 4), 접속번호, alate_eraa_atijaaya, akaliaa_ajutuu);
    }
    static void ashajaa_ejepüsee(int ejepüsee, int akaliaa_ajutuu, int kusu_ejepüsee, int 접속번호) {
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < akaliaa_ajutuu && ee_iyatialujuna < 16; ee_iyatialujuna++) {
            int ajutuu = 0;
            if (ee_iyatialujuna == 0) ajutuu = 2;
            if (ee_iyatialujuna == 2) ajutuu = 접속번호 >>> 8;
            if (ee_iyatialujuna == 3) ajutuu = 접속번호;
            if (ee_iyatialujuna >= 4 && ee_iyatialujuna < 8) ajutuu = kusu_ejepüsee >>> (56 - ee_iyatialujuna * 8);
            serulaalü_ajutuu.기억쓰기(ejepüsee + ee_iyatialujuna, ajutuu & 255);
        }
    }
    static int 자료전문받기(int 서술자, int atijaaya_ejepüsee, int akaliaa_ajutuu, int 설정, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((설정 & ~64) != 0) return -95;
        if (akaliaa_ajutuu < 0) return -22;
        if (akaliaa_ajutuu != 0 && !실행관리.külipü_ayaakuaapijana(atijaaya_ejepüsee, akaliaa_ajutuu)) return -14;
        int ejepüsee = 0, ejepüsee_akaliaa_ejepüsee = 0, ejepüsee_akaliaa = 0;
        if (요청주소 != 0) {
            if (!실행관리.külipü_ayaakuaapijana(요청주소, 8)) return -14;
            ejepüsee = 실행관리.수(요청주소); ejepüsee_akaliaa_ejepüsee = 실행관리.수(요청주소 + 4);
            if (ejepüsee != 0) {
                if (!실행관리.külipü_ayaakuaapijana(ejepüsee_akaliaa_ejepüsee, 4)) return -14;
                ejepüsee_akaliaa = 실행관리.수(ejepüsee_akaliaa_ejepüsee);
                if (ejepüsee_akaliaa < 0) return -22;
                if (!실행관리.külipü_ayaakuaapijana(ejepüsee, ejepüsee_akaliaa < 16 ? ejepüsee_akaliaa : 16)) return -14;
            }
        }
        int 결과 = 자동묶기(기술);
        if (결과 < 0) return 결과;
        int 시작 = serulaalü_ajutuu.밀리초();
        while (true) {
            결과 = 통신망.받기(kusu_aapaaya[기술], alate_eraa_atijaaya, 1024, 0);
            if (결과 != -11) break;
            if ((설정 & 64) != 0 || (열기설정[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && serulaalü_ajutuu.밀리초() - 시작 >= 수신대기밀리초[기술]) return -11;
            if (serulaalü_ajutuu.사용자남은밀리초() <= 10) return -11;
            serulaalü_ajutuu.잠시양보();
        }
        if (결과 < 0) return 결과;
        if (결과 > akaliaa_ajutuu) 결과 = akaliaa_ajutuu;
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 결과; ee_iyatialujuna++) serulaalü_ajutuu.기억쓰기(atijaaya_ejepüsee + ee_iyatialujuna, alate_eraa_atijaaya[ee_iyatialujuna]);
        if (ejepüsee != 0) {
            ashajaa_ejepüsee(ejepüsee, ejepüsee_akaliaa, 통신망.wanaawasü_ejepüsee(kusu_aapaaya[기술]), 통신망.상대접속번호(kusu_aapaaya[기술]));
            실행관리.수쓰기(ejepüsee_akaliaa_ejepüsee, 16);
        }
        return 결과;
    }
    static int 통신주소읽기(int 서술자, int ejepüsee, int akaliaa_ejepüsee) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.külipü_ayaakuaapijana(akaliaa_ejepüsee, 4)) return -14;
        int akaliaa_ajutuu = 실행관리.수(akaliaa_ejepüsee);
        if (akaliaa_ajutuu < 0) return -22;
        if (!실행관리.külipü_ayaakuaapijana(ejepüsee, akaliaa_ajutuu < 16 ? akaliaa_ajutuu : 16)) return -14;
        int 칸 = 통신망.ee_iyatialujuna(kusu_aapaaya[기술]);
        ashajaa_ejepüsee(ejepüsee, akaliaa_ajutuu, 대상[기술], 칸 < 0 ? 0 : 통신망.접속번호들[칸]);
        실행관리.수쓰기(akaliaa_ejepüsee, 16);
        return 0;
    }
    static int 수신대기정하기(int 서술자, int 밀리초) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (밀리초 < 0 || 밀리초 > 2000) return -22;
        수신대기밀리초[기술] = 밀리초;
        return 0;
    }
}
