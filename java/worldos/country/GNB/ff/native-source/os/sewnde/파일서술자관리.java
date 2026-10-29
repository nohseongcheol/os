// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 kuutoro 과정의 파일서술자와 열린 fiilde 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int tar_winndu_maantaade = 2, 만들기 = 64, 독점생성 = 128, festude_Haatumeere_loowdi = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] udditde_jaggoode = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], faandaare = new int[서술자한도];
    static int[] 파일위치 = new int[서술자한도], 열기설정 = new int[서술자한도], 참조수 = new int[서술자한도];
    static int[] laylaytol_jaggoode = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] laawol_innde = new int[64], egginde_keɓe = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return udditde_jaggoode[파일서술자] - 1;
    }
    static int 빈서술자(int huutoraade) {
        for (int joopirdu = huutoraade; joopirdu < 서술자한도; joopirdu++) if (udditde_jaggoode[joopirdu] == 0) return joopirdu;
        return -24;
    }
    static int 빈기술() {
        for (int joopirdu = 0; joopirdu < 서술자한도; joopirdu++) if (참조수[joopirdu] == 0) return joopirdu;
        return -24;
    }
    static int seŋaade(int 서술자, int 기술, int 파일종류, int fiilde_faandaare, int 설정) {
        udditde_jaggoode[서술자] = 기술 + 1; 서술자설정[서술자] = (설정 & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; faandaare[기술] = fiilde_faandaare; 참조수[기술] = 1;
        열기설정[기술] = 설정 & (3 | 이어쓰기 | 기다리지않기); 파일위치[기술] = 0;
        laylaytol_jaggoode[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void huɓɓude_Yuɓɓo_golle() {
        과정정리();
        for (int joopirdu = 0; joopirdu < 3; joopirdu++) seŋaade(joopirdu, joopirdu, 1, joopirdu, joopirdu == 0 ? 0 : 1);
    }
    static void 과정정리() {
        for (int joopirdu = 0; joopirdu < 서술자한도; joopirdu++) if (udditde_jaggoode[joopirdu] != 0) uddude_fiilde(joopirdu);
    }
    static int uddude_fiilde(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        udditde_jaggoode[서술자] = 0; 서술자설정[서술자] = 0;
        참조수[기술]--;
        if (참조수[기술] == 0) {
            if (종류[기술] == 2) teskordu_yuɓɓo_piille.열림수[faandaare[기술]]--;
            if (종류[기술] == 3 && laylaytol_jaggoode[기술] != 0) 통신망.uddude(laylaytol_jaggoode[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 oktee_njaru 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int ñiiɓirde) {
        if (!실행관리.kilip(ñiiɓirde, 1)) return -14;
        int 위치 = kaɓirgal_njaru.기억읽기(ñiiɓirde) == '/' ? 1 : 0;
        for (int njuuteendi_njaru = 0; njuuteendi_njaru < 64; njuuteendi_njaru++) {
            if (!실행관리.kilip(ñiiɓirde + 위치 + njuuteendi_njaru, 1)) return -14;
            int njaru = kaɓirgal_njaru.기억읽기(ñiiɓirde + 위치 + njuuteendi_njaru);
            laawol_innde[njuuteendi_njaru] = njaru;
            if (njaru == 0) return njuuteendi_njaru == 0 ? -2 : (teskordu_yuɓɓo_piille.sek_innde(laawol_innde, njuuteendi_njaru) ? njuuteendi_njaru : -22);
            if (njaru == '/') return -20;
        }
        return -36;
    }
    static int udditde_fiilde(int innde_ñiiɓirde, int 설정, int 허가) {
        int njuuteendi_njaru = 경로읽기(innde_ñiiɓirde);
        if (njuuteendi_njaru < 0) return njuuteendi_njaru;
        if ((설정 & ~(3 | 만들기 | 독점생성 | festude_Haatumeere_loowdi | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((설정 & 3) == 3 || ((설정 & festude_Haatumeere_loowdi) != 0 && (설정 & 3) == 0)) return -22;
        int fiilde = teskordu_yuɓɓo_piille.yiylaade_naatnugol(laawol_innde, njuuteendi_njaru);
        if (fiilde >= 0 && (설정 & (만들기 | 독점생성)) == (만들기 | 독점생성)) return -17;
        if (fiilde == -2 && (설정 & 만들기) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = 빈기술();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (fiilde == -2) {
            int 결과 = teskordu_yuɓɓo_piille.resde_njaru(laawol_innde, njuuteendi_njaru, laawol_innde, 0);
            if (결과 < 0) return 결과;
            fiilde = teskordu_yuɓɓo_piille.yiylaade_naatnugol(laawol_innde, njuuteendi_njaru);
            teskordu_yuɓɓo_piille.허가들[fiilde] = 허가 & 511;
        }
        if (fiilde < 0) return fiilde;
        if ((설정 & festude_Haatumeere_loowdi) != 0) teskordu_yuɓɓo_piille.waylude_etannde_Doggol[fiilde] = 0;
        teskordu_yuɓɓo_piille.열림수[fiilde]++;
        return seŋaade(서술자, 기술, 2, fiilde, 설정);
    }
    static int 파일읽기(int 서술자, int keɓe_ñiiɓirde, int njuuteendi_njaru) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (열기설정[기술] & 3) == 1) return -9;
        if (njuuteendi_njaru < 0) return -22;
        if (njuuteendi_njaru == 0) return 0;
        if (!실행관리.kilip(keɓe_ñiiɓirde, njuuteendi_njaru)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, keɓe_ñiiɓirde, njuuteendi_njaru, 0, 0);
        if (종류[기술] == 1) {
            int 받은수 = 0;
            while (받은수 < njuuteendi_njaru) {
                int njaru = 문자단말.직렬읽기();
                if (njaru < 0) njaru = tappirde.읽기();
                if (njaru < 0) {
                    if (받은수 > 0) return 받은수;
                    if ((열기설정[기술] & 기다리지않기) != 0) return -11;
                    if (kaɓirgal_njaru.사용자남은밀리초() <= 10) return -11;
                    통신망.ƴeewtaade(); kaɓirgal_njaru.잠시양보();
                } else {
                    kaɓirgal_njaru.winndude_teskordu(keɓe_ñiiɓirde + 받은수, njaru); 받은수++;
                }
            }
            return 받은수;
        }
        int fiilde = faandaare[기술], 위치 = 파일위치[기술];
        if (위치 >= teskordu_yuɓɓo_piille.waylude_etannde_Doggol[fiilde]) return 0;
        if (njuuteendi_njaru > teskordu_yuɓɓo_piille.waylude_etannde_Doggol[fiilde] - 위치) njuuteendi_njaru = teskordu_yuɓɓo_piille.waylude_etannde_Doggol[fiilde] - 위치;
        int 원본주소 = kaɓirgal_njaru.fiilde_teskordu() + fiilde * teskordu_yuɓɓo_piille.최대크기 + 위치;
        for (int joopirdu = 0; joopirdu < njuuteendi_njaru; joopirdu++) kaɓirgal_njaru.winndude_teskordu(keɓe_ñiiɓirde + joopirdu, kaɓirgal_njaru.기억읽기(원본주소 + joopirdu));
        파일위치[기술] += njuuteendi_njaru;
        return njuuteendi_njaru;
    }
    static int winndude_fiilde(int 서술자, int keɓe_ñiiɓirde, int njuuteendi_njaru) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (열기설정[기술] & 3) == 0) return -9;
        if (njuuteendi_njaru < 0) return -22;
        if (njuuteendi_njaru == 0) return 0;
        if (!실행관리.kilip(keɓe_ñiiɓirde, njuuteendi_njaru)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 tiindaare_njaru 주소가 필요하다.
        if (종류[기술] == 1) {
            if (njuuteendi_njaru > 16384) njuuteendi_njaru = 16384;
            for (int joopirdu = 0; joopirdu < njuuteendi_njaru; joopirdu++) {
                int njaru = kaɓirgal_njaru.기억읽기(keɓe_ñiiɓirde + joopirdu);
                문자단말.직렬바이트(njaru); 문자단말.화면문자(njaru);
            }
            return njuuteendi_njaru;
        }
        int fiilde = faandaare[기술], waylude_etannde = teskordu_yuɓɓo_piille.waylude_etannde_Doggol[fiilde];
        int 위치 = (열기설정[기술] & 이어쓰기) != 0 ? waylude_etannde : 파일위치[기술];
        if (위치 >= teskordu_yuɓɓo_piille.최대크기) return -27;
        if (njuuteendi_njaru > teskordu_yuɓɓo_piille.최대크기 - 위치) njuuteendi_njaru = teskordu_yuɓɓo_piille.최대크기 - 위치;
        int tiindaare_ñiiɓirde = kaɓirgal_njaru.fiilde_teskordu() + fiilde * teskordu_yuɓɓo_piille.최대크기;
        for (int joopirdu = waylude_etannde; joopirdu < 위치; joopirdu++) kaɓirgal_njaru.winndude_teskordu(tiindaare_ñiiɓirde + joopirdu, 0);
        for (int joopirdu = 0; joopirdu < njuuteendi_njaru; joopirdu++) kaɓirgal_njaru.winndude_teskordu(tiindaare_ñiiɓirde + 위치 + joopirdu, kaɓirgal_njaru.기억읽기(keɓe_ñiiɓirde + joopirdu));
        파일위치[기술] = 위치 + njuuteendi_njaru;
        if (위치 + njuuteendi_njaru > waylude_etannde) teskordu_yuɓɓo_piille.waylude_etannde_Doggol[fiilde] = 위치 + njuuteendi_njaru;
        return njuuteendi_njaru;
    }
    static int 파일위치옮기기(int 서술자, int 변위, int 기준) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (기준 < 0 || 기준 > 2) return -22;
        int cakkital_njaru = 기준 == 0 ? 0 : (기준 == 1 ? 파일위치[기술] : teskordu_yuɓɓo_piille.waylude_etannde_Doggol[faandaare[기술]]);
        if (변위 > 0 && cakkital_njaru > 2147483647 - 변위) return -75;
        if (변위 < 0 && 변위 < -cakkital_njaru) return -22;
        파일위치[기술] = cakkital_njaru + 변위;
        return 파일위치[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean 지정, int 설정) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return 지정 ? -9 : -22;
        if (지정 && 서술자 == 새서술자) return 새서술자;
        if (지정) { if (udditde_jaggoode[새서술자] != 0) uddude_fiilde(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        udditde_jaggoode[새서술자] = 기술 + 1; 서술자설정[새서술자] = 설정; 참조수[기술]++;
        return 새서술자;
    }
    static int ittude_fiilde_naatnugol_innde(int innde_ñiiɓirde) {
        int njuuteendi_njaru = 경로읽기(innde_ñiiɓirde);
        if (njuuteendi_njaru < 0) return njuuteendi_njaru;
        int fiilde = teskordu_yuɓɓo_piille.yiylaade_naatnugol(laawol_innde, njuuteendi_njaru);
        if (fiilde < 0) return fiilde;
        teskordu_yuɓɓo_piille.이름들[fiilde * 64] = 0;
        return 0;
    }
    static int 파일길이정하기(int 서술자, int njuuteendi_njaru) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (열기설정[기술] & 3) == 0 || njuuteendi_njaru < 0) return -22;
        if (njuuteendi_njaru > teskordu_yuɓɓo_piille.최대크기) return -27;
        int fiilde = faandaare[기술], ñiiɓirde = kaɓirgal_njaru.fiilde_teskordu() + fiilde * teskordu_yuɓɓo_piille.최대크기;
        for (int joopirdu = teskordu_yuɓɓo_piille.waylude_etannde_Doggol[fiilde]; joopirdu < njuuteendi_njaru; joopirdu++) kaɓirgal_njaru.winndude_teskordu(ñiiɓirde + joopirdu, 0);
        teskordu_yuɓɓo_piille.waylude_etannde_Doggol[fiilde] = njuuteendi_njaru;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int ñiiɓirde) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.kilip(ñiiɓirde, 48)) return -14;
        for (int joopirdu = 0; joopirdu < 12; joopirdu++) 실행관리.수쓰기(ñiiɓirde + joopirdu * 4, 0);
        int fiilde = faandaare[기술], waylude_etannde = 종류[기술] == 2 ? teskordu_yuɓɓo_piille.waylude_etannde_Doggol[fiilde] : 0;
        int 허가 = 종류[기술] == 2 ? teskordu_yuɓɓo_piille.허가들[fiilde] : 438;
        실행관리.수쓰기(ñiiɓirde, 1);
        실행관리.수쓰기(ñiiɓirde + 4, 종류[기술] == 2 ? fiilde + 1 : 100 + 기술);
        실행관리.수쓰기(ñiiɓirde + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(ñiiɓirde + 12, 종류[기술] == 2 && teskordu_yuɓɓo_piille.이름들[fiilde * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(ñiiɓirde + 28, waylude_etannde); 실행관리.수쓰기(ñiiɓirde + 32, 512);
        실행관리.수쓰기(ñiiɓirde + 36, (waylude_etannde + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int ginol, int njaru) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (ginol == 0 || ginol == 1030) return 서술자복제(서술자, njaru, false, ginol == 1030 ? 1 : 0);
        if (ginol == 1) return 서술자설정[서술자];
        if (ginol == 2) { if ((njaru & ~1) != 0) return -22; 서술자설정[서술자] = njaru; return 0; }
        if (ginol == 3) return 열기설정[기술];
        if (ginol == 4) {
            if ((njaru & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            열기설정[기술] = (열기설정[기술] & 3) | (njaru & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int 통신종단점만들기(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = 빈기술();
        if (서술자 < 0 || 기술 < 0) return -24;
        return seŋaade(서술자, 기술, 3, 0, tar_winndu_maantaade);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int ñiiɓirde_32(int ñiiɓirde) {
        return kaɓirgal_njaru.기억읽기(ñiiɓirde) << 24 | kaɓirgal_njaru.기억읽기(ñiiɓirde + 1) << 16
            | kaɓirgal_njaru.기억읽기(ñiiɓirde + 2) << 8 | kaɓirgal_njaru.기억읽기(ñiiɓirde + 3);
    }
    static int sek_ñiiɓirde(int ñiiɓirde, int njuuteendi_njaru) {
        if (njuuteendi_njaru < 16) return -22;
        if (!실행관리.kilip(ñiiɓirde, 16)) return -14;
        return 실행관리.짧은수(ñiiɓirde) == 2 ? 0 : -97;
    }
    static int seŋondir_ñiiɓirde(int 서술자, int ñiiɓirde, int njuuteendi_njaru) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int 결과 = sek_ñiiɓirde(ñiiɓirde, njuuteendi_njaru);
        if (결과 < 0) return 결과;
        if (laylaytol_jaggoode[기술] != 0) return -22;
        int laylaytol_ñiiɓirde = ñiiɓirde_32(ñiiɓirde + 4);
        if (laylaytol_ñiiɓirde != 0 && laylaytol_ñiiɓirde != 통신망.내주소) return -99;
        int 접속번호 = kaɓirgal_njaru.기억읽기(ñiiɓirde + 2) << 8 | kaɓirgal_njaru.기억읽기(ñiiɓirde + 3);
        결과 = 통신망.udditde(접속번호);
        if (결과 < 0) return 결과;
        laylaytol_jaggoode[기술] = 결과; faandaare[기술] = laylaytol_ñiiɓirde;
        return 0;
    }
    static int 자동묶기(int 기술) {
        if (laylaytol_jaggoode[기술] != 0) return 0;
        int 결과 = 통신망.udditde(0);
        if (결과 < 0) return 결과;
        laylaytol_jaggoode[기술] = 결과;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 요청 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int keɓe_ñiiɓirde, int njuuteendi_njaru, int 설정, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (설정 != 0) return -95;
        if (njuuteendi_njaru < 0 || njuuteendi_njaru > 1024) return -90;
        if (njuuteendi_njaru != 0 && !실행관리.kilip(keɓe_ñiiɓirde, njuuteendi_njaru)) return -14;
        if (!실행관리.kilip(요청주소, 8)) return -14;
        int ñiiɓirde = 실행관리.수(요청주소);
        int 결과 = sek_ñiiɓirde(ñiiɓirde, 실행관리.수(요청주소 + 4));
        if (결과 < 0) return 결과;
        int 접속번호 = kaɓirgal_njaru.기억읽기(ñiiɓirde + 2) << 8 | kaɓirgal_njaru.기억읽기(ñiiɓirde + 3);
        if (접속번호 == 0) return -22;
        결과 = 자동묶기(기술);
        if (결과 < 0) return 결과;
        for (int joopirdu = 0; joopirdu < njuuteendi_njaru; joopirdu++) egginde_keɓe[joopirdu] = kaɓirgal_njaru.기억읽기(keɓe_ñiiɓirde + joopirdu);
        return 통신망.neldude(laylaytol_jaggoode[기술], ñiiɓirde_32(ñiiɓirde + 4), 접속번호, egginde_keɓe, njuuteendi_njaru);
    }
    static void winndude_ñiiɓirde(int ñiiɓirde, int njuuteendi_njaru, int laylaytol_ñiiɓirde, int 접속번호) {
        for (int joopirdu = 0; joopirdu < njuuteendi_njaru && joopirdu < 16; joopirdu++) {
            int njaru = 0;
            if (joopirdu == 0) njaru = 2;
            if (joopirdu == 2) njaru = 접속번호 >>> 8;
            if (joopirdu == 3) njaru = 접속번호;
            if (joopirdu >= 4 && joopirdu < 8) njaru = laylaytol_ñiiɓirde >>> (56 - joopirdu * 8);
            kaɓirgal_njaru.winndude_teskordu(ñiiɓirde + joopirdu, njaru & 255);
        }
    }
    static int 자료전문받기(int 서술자, int keɓe_ñiiɓirde, int njuuteendi_njaru, int 설정, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((설정 & ~64) != 0) return -95;
        if (njuuteendi_njaru < 0) return -22;
        if (njuuteendi_njaru != 0 && !실행관리.kilip(keɓe_ñiiɓirde, njuuteendi_njaru)) return -14;
        int ñiiɓirde = 0, ñiiɓirde_njuuteendi_ñiiɓirde = 0, ñiiɓirde_njuuteendi = 0;
        if (요청주소 != 0) {
            if (!실행관리.kilip(요청주소, 8)) return -14;
            ñiiɓirde = 실행관리.수(요청주소); ñiiɓirde_njuuteendi_ñiiɓirde = 실행관리.수(요청주소 + 4);
            if (ñiiɓirde != 0) {
                if (!실행관리.kilip(ñiiɓirde_njuuteendi_ñiiɓirde, 4)) return -14;
                ñiiɓirde_njuuteendi = 실행관리.수(ñiiɓirde_njuuteendi_ñiiɓirde);
                if (ñiiɓirde_njuuteendi < 0) return -22;
                if (!실행관리.kilip(ñiiɓirde, ñiiɓirde_njuuteendi < 16 ? ñiiɓirde_njuuteendi : 16)) return -14;
            }
        }
        int 결과 = 자동묶기(기술);
        if (결과 < 0) return 결과;
        int huutoraade = kaɓirgal_njaru.밀리초();
        while (true) {
            결과 = 통신망.받기(laylaytol_jaggoode[기술], egginde_keɓe, 1024, 0);
            if (결과 != -11) break;
            if ((설정 & 64) != 0 || (열기설정[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && kaɓirgal_njaru.밀리초() - huutoraade >= 수신대기밀리초[기술]) return -11;
            if (kaɓirgal_njaru.사용자남은밀리초() <= 10) return -11;
            kaɓirgal_njaru.잠시양보();
        }
        if (결과 < 0) return 결과;
        if (결과 > njuuteendi_njaru) 결과 = njuuteendi_njaru;
        for (int joopirdu = 0; joopirdu < 결과; joopirdu++) kaɓirgal_njaru.winndude_teskordu(keɓe_ñiiɓirde + joopirdu, egginde_keɓe[joopirdu]);
        if (ñiiɓirde != 0) {
            winndude_ñiiɓirde(ñiiɓirde, ñiiɓirde_njuuteendi, 통신망.giƴiraaɗo_ñiiɓirde(laylaytol_jaggoode[기술]), 통신망.상대접속번호(laylaytol_jaggoode[기술]));
            실행관리.수쓰기(ñiiɓirde_njuuteendi_ñiiɓirde, 16);
        }
        return 결과;
    }
    static int 통신주소읽기(int 서술자, int ñiiɓirde, int njuuteendi_ñiiɓirde) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.kilip(njuuteendi_ñiiɓirde, 4)) return -14;
        int njuuteendi_njaru = 실행관리.수(njuuteendi_ñiiɓirde);
        if (njuuteendi_njaru < 0) return -22;
        if (!실행관리.kilip(ñiiɓirde, njuuteendi_njaru < 16 ? njuuteendi_njaru : 16)) return -14;
        int 칸 = 통신망.joopirdu(laylaytol_jaggoode[기술]);
        winndude_ñiiɓirde(ñiiɓirde, njuuteendi_njaru, faandaare[기술], 칸 < 0 ? 0 : 통신망.접속번호들[칸]);
        실행관리.수쓰기(njuuteendi_ñiiɓirde, 16);
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
