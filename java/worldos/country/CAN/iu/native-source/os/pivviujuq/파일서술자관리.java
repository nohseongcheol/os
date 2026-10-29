// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 atuqtuq 과정의 파일서술자와 열린 ini 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int uqalimaarli_titirarli_ujjiqsuut = 2, 만들기 = 64, 독점생성 = 128, piijarli_TOC = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] matuirli_nuuttarut = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], turaagaq = new int[서술자한도];
    static int[] 파일위치 = new int[서술자한도], 열기설정 = new int[서술자한도], 참조수 = new int[서술자한도];
    static int[] Kasuqatigiitsimajut_nuuttarut = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] aqqut_atiq = new int[64], aullaaqtilli_titiqqat = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return matuirli_nuuttarut[파일서술자] - 1;
    }
    static int 빈서술자(int 시작) {
        for (int nalunaiqsimavik = 시작; nalunaiqsimavik < 서술자한도; nalunaiqsimavik++) if (matuirli_nuuttarut[nalunaiqsimavik] == 0) return nalunaiqsimavik;
        return -24;
    }
    static int 빈기술() {
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 서술자한도; nalunaiqsimavik++) if (참조수[nalunaiqsimavik] == 0) return nalunaiqsimavik;
        return -24;
    }
    static int kasurli(int 서술자, int 기술, int 파일종류, int ini_turaagaq, int 설정) {
        matuirli_nuuttarut[서술자] = 기술 + 1; 서술자설정[서술자] = (설정 & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; turaagaq[기술] = ini_turaagaq; 참조수[기술] = 1;
        열기설정[기술] = 설정 & (3 | 이어쓰기 | 기다리지않기); 파일위치[기술] = 0;
        Kasuqatigiitsimajut_nuuttarut[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void pigiarli_Pivallianiq() {
        과정정리();
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 3; nalunaiqsimavik++) kasurli(nalunaiqsimavik, nalunaiqsimavik, 1, nalunaiqsimavik, nalunaiqsimavik == 0 ? 0 : 1);
    }
    static void 과정정리() {
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 서술자한도; nalunaiqsimavik++) if (matuirli_nuuttarut[nalunaiqsimavik] != 0) matuli_ini(nalunaiqsimavik);
    }
    static int matuli_ini(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        matuirli_nuuttarut[서술자] = 0; 서술자설정[서술자] = 0;
        참조수[기술]--;
        if (참조수[기술] == 0) {
            if (종류[기술] == 2) puigujjaikkut_inikkuvik.열림수[turaagaq[기술]]--;
            if (종류[기술] == 3 && Kasuqatigiitsimajut_nuuttarut[기술] != 0) 통신망.matuli(Kasuqatigiitsimajut_nuuttarut[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 byte_atuutilik 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int turaarut) {
        if (!실행관리.Nakatigat(turaarut, 1)) return -14;
        int 위치 = sunakkutaaq_atuutilik.기억읽기(turaarut) == '/' ? 1 : 0;
        for (int takininga_atuutilik = 0; takininga_atuutilik < 64; takininga_atuutilik++) {
            if (!실행관리.Nakatigat(turaarut + 위치 + takininga_atuutilik, 1)) return -14;
            int atuutilik = sunakkutaaq_atuutilik.기억읽기(turaarut + 위치 + takininga_atuutilik);
            aqqut_atiq[takininga_atuutilik] = atuutilik;
            if (atuutilik == 0) return takininga_atuutilik == 0 ? -2 : (puigujjaikkut_inikkuvik.qaujigiarli_atiq(aqqut_atiq, takininga_atuutilik) ? takininga_atuutilik : -22);
            if (atuutilik == '/') return -20;
        }
        return -36;
    }
    static int matuirli_ini(int atiq_turaarut, int 설정, int 허가) {
        int takininga_atuutilik = 경로읽기(atiq_turaarut);
        if (takininga_atuutilik < 0) return takininga_atuutilik;
        if ((설정 & ~(3 | 만들기 | 독점생성 | piijarli_TOC | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((설정 & 3) == 3 || ((설정 & piijarli_TOC) != 0 && (설정 & 3) == 0)) return -22;
        int ini = puigujjaikkut_inikkuvik.nanili_Iliniku(aqqut_atiq, takininga_atuutilik);
        if (ini >= 0 && (설정 & (만들기 | 독점생성)) == (만들기 | 독점생성)) return -17;
        if (ini == -2 && (설정 & 만들기) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = 빈기술();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (ini == -2) {
            int 결과 = puigujjaikkut_inikkuvik.tuqqurli_atuutilik(aqqut_atiq, takininga_atuutilik, aqqut_atiq, 0);
            if (결과 < 0) return 결과;
            ini = puigujjaikkut_inikkuvik.nanili_Iliniku(aqqut_atiq, takininga_atuutilik);
            puigujjaikkut_inikkuvik.허가들[ini] = 허가 & 511;
        }
        if (ini < 0) return ini;
        if ((설정 & piijarli_TOC) != 0) puigujjaikkut_inikkuvik.anininga_Titiqpalliagaq[ini] = 0;
        puigujjaikkut_inikkuvik.열림수[ini]++;
        return kasurli(서술자, 기술, 2, ini, 설정);
    }
    static int 파일읽기(int 서술자, int titiqqat_turaarut, int takininga_atuutilik) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (열기설정[기술] & 3) == 1) return -9;
        if (takininga_atuutilik < 0) return -22;
        if (takininga_atuutilik == 0) return 0;
        if (!실행관리.Nakatigat(titiqqat_turaarut, takininga_atuutilik)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, titiqqat_turaarut, takininga_atuutilik, 0, 0);
        if (종류[기술] == 1) {
            int 받은수 = 0;
            while (받은수 < takininga_atuutilik) {
                int atuutilik = 문자단말.직렬읽기();
                if (atuutilik < 0) atuutilik = naqittaut.읽기();
                if (atuutilik < 0) {
                    if (받은수 > 0) return 받은수;
                    if ((열기설정[기술] & 기다리지않기) != 0) return -11;
                    if (sunakkutaaq_atuutilik.사용자남은밀리초() <= 10) return -11;
                    통신망.nalunairli_1aacb54c(); sunakkutaaq_atuutilik.잠시양보();
                } else {
                    sunakkutaaq_atuutilik.titiraq_puigujjaikkut(titiqqat_turaarut + 받은수, atuutilik); 받은수++;
                }
            }
            return 받은수;
        }
        int ini = turaagaq[기술], 위치 = 파일위치[기술];
        if (위치 >= puigujjaikkut_inikkuvik.anininga_Titiqpalliagaq[ini]) return 0;
        if (takininga_atuutilik > puigujjaikkut_inikkuvik.anininga_Titiqpalliagaq[ini] - 위치) takininga_atuutilik = puigujjaikkut_inikkuvik.anininga_Titiqpalliagaq[ini] - 위치;
        int 원본주소 = sunakkutaaq_atuutilik.ini_puigujjaikkut() + ini * puigujjaikkut_inikkuvik.최대크기 + 위치;
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < takininga_atuutilik; nalunaiqsimavik++) sunakkutaaq_atuutilik.titiraq_puigujjaikkut(titiqqat_turaarut + nalunaiqsimavik, sunakkutaaq_atuutilik.기억읽기(원본주소 + nalunaiqsimavik));
        파일위치[기술] += takininga_atuutilik;
        return takininga_atuutilik;
    }
    static int titiraq_ini(int 서술자, int titiqqat_turaarut, int takininga_atuutilik) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (열기설정[기술] & 3) == 0) return -9;
        if (takininga_atuutilik < 0) return -22;
        if (takininga_atuutilik == 0) return 0;
        if (!실행관리.Nakatigat(titiqqat_turaarut, takininga_atuutilik)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 namunngarvik_atuutilik 주소가 필요하다.
        if (종류[기술] == 1) {
            if (takininga_atuutilik > 16384) takininga_atuutilik = 16384;
            for (int nalunaiqsimavik = 0; nalunaiqsimavik < takininga_atuutilik; nalunaiqsimavik++) {
                int atuutilik = sunakkutaaq_atuutilik.기억읽기(titiqqat_turaarut + nalunaiqsimavik);
                문자단말.직렬바이트(atuutilik); 문자단말.화면문자(atuutilik);
            }
            return takininga_atuutilik;
        }
        int ini = turaagaq[기술], anininga = puigujjaikkut_inikkuvik.anininga_Titiqpalliagaq[ini];
        int 위치 = (열기설정[기술] & 이어쓰기) != 0 ? anininga : 파일위치[기술];
        if (위치 >= puigujjaikkut_inikkuvik.최대크기) return -27;
        if (takininga_atuutilik > puigujjaikkut_inikkuvik.최대크기 - 위치) takininga_atuutilik = puigujjaikkut_inikkuvik.최대크기 - 위치;
        int namunngarvik_turaarut = sunakkutaaq_atuutilik.ini_puigujjaikkut() + ini * puigujjaikkut_inikkuvik.최대크기;
        for (int nalunaiqsimavik = anininga; nalunaiqsimavik < 위치; nalunaiqsimavik++) sunakkutaaq_atuutilik.titiraq_puigujjaikkut(namunngarvik_turaarut + nalunaiqsimavik, 0);
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < takininga_atuutilik; nalunaiqsimavik++) sunakkutaaq_atuutilik.titiraq_puigujjaikkut(namunngarvik_turaarut + 위치 + nalunaiqsimavik, sunakkutaaq_atuutilik.기억읽기(titiqqat_turaarut + nalunaiqsimavik));
        파일위치[기술] = 위치 + takininga_atuutilik;
        if (위치 + takininga_atuutilik > anininga) puigujjaikkut_inikkuvik.anininga_Titiqpalliagaq[ini] = 위치 + takininga_atuutilik;
        return takininga_atuutilik;
    }
    static int qinirli_ini(int 서술자, int 변위, int 기준) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (기준 < 0 || 기준 > 2) return -22;
        int ungataa_atuutilik = 기준 == 0 ? 0 : (기준 == 1 ? 파일위치[기술] : puigujjaikkut_inikkuvik.anininga_Titiqpalliagaq[turaagaq[기술]]);
        if (변위 > 0 && ungataa_atuutilik > 2147483647 - 변위) return -75;
        if (변위 < 0 && 변위 < -ungataa_atuutilik) return -22;
        파일위치[기술] = ungataa_atuutilik + 변위;
        return 파일위치[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean 지정, int 설정) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return 지정 ? -9 : -22;
        if (지정 && 서술자 == 새서술자) return 새서술자;
        if (지정) { if (matuirli_nuuttarut[새서술자] != 0) matuli_ini(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        matuirli_nuuttarut[새서술자] = 기술 + 1; 서술자설정[새서술자] = 설정; 참조수[기술]++;
        return 새서술자;
    }
    static int sanirvalli_ini_Iliniku_atiq(int atiq_turaarut) {
        int takininga_atuutilik = 경로읽기(atiq_turaarut);
        if (takininga_atuutilik < 0) return takininga_atuutilik;
        int ini = puigujjaikkut_inikkuvik.nanili_Iliniku(aqqut_atiq, takininga_atuutilik);
        if (ini < 0) return ini;
        puigujjaikkut_inikkuvik.이름들[ini * 64] = 0;
        return 0;
    }
    static int attiqsimaniit_ini_takininga(int 서술자, int takininga_atuutilik) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (열기설정[기술] & 3) == 0 || takininga_atuutilik < 0) return -22;
        if (takininga_atuutilik > puigujjaikkut_inikkuvik.최대크기) return -27;
        int ini = turaagaq[기술], turaarut = sunakkutaaq_atuutilik.ini_puigujjaikkut() + ini * puigujjaikkut_inikkuvik.최대크기;
        for (int nalunaiqsimavik = puigujjaikkut_inikkuvik.anininga_Titiqpalliagaq[ini]; nalunaiqsimavik < takininga_atuutilik; nalunaiqsimavik++) sunakkutaaq_atuutilik.titiraq_puigujjaikkut(turaarut + nalunaiqsimavik, 0);
        puigujjaikkut_inikkuvik.anininga_Titiqpalliagaq[ini] = takininga_atuutilik;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int turaarut) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.Nakatigat(turaarut, 48)) return -14;
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 12; nalunaiqsimavik++) 실행관리.수쓰기(turaarut + nalunaiqsimavik * 4, 0);
        int ini = turaagaq[기술], anininga = 종류[기술] == 2 ? puigujjaikkut_inikkuvik.anininga_Titiqpalliagaq[ini] : 0;
        int 허가 = 종류[기술] == 2 ? puigujjaikkut_inikkuvik.허가들[ini] : 438;
        실행관리.수쓰기(turaarut, 1);
        실행관리.수쓰기(turaarut + 4, 종류[기술] == 2 ? ini + 1 : 100 + 기술);
        실행관리.수쓰기(turaarut + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(turaarut + 12, 종류[기술] == 2 && puigujjaikkut_inikkuvik.이름들[ini * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(turaarut + 28, anininga); 실행관리.수쓰기(turaarut + 32, 512);
        실행관리.수쓰기(turaarut + 36, (anininga + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int piqujijjut, int atuutilik) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (piqujijjut == 0 || piqujijjut == 1030) return 서술자복제(서술자, atuutilik, false, piqujijjut == 1030 ? 1 : 0);
        if (piqujijjut == 1) return 서술자설정[서술자];
        if (piqujijjut == 2) { if ((atuutilik & ~1) != 0) return -22; 서술자설정[서술자] = atuutilik; return 0; }
        if (piqujijjut == 3) return 열기설정[기술];
        if (piqujijjut == 4) {
            if ((atuutilik & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            열기설정[기술] = (열기설정[기술] & 3) | (atuutilik & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int 통신종단점만들기(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = 빈기술();
        if (서술자 < 0 || 기술 < 0) return -24;
        return kasurli(서술자, 기술, 3, 0, uqalimaarli_titirarli_ujjiqsuut);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int turaarut_32(int turaarut) {
        return sunakkutaaq_atuutilik.기억읽기(turaarut) << 24 | sunakkutaaq_atuutilik.기억읽기(turaarut + 1) << 16
            | sunakkutaaq_atuutilik.기억읽기(turaarut + 2) << 8 | sunakkutaaq_atuutilik.기억읽기(turaarut + 3);
    }
    static int qaujigiarli_turaarut(int turaarut, int takininga_atuutilik) {
        if (takininga_atuutilik < 16) return -22;
        if (!실행관리.Nakatigat(turaarut, 16)) return -14;
        return 실행관리.짧은수(turaarut) == 2 ? 0 : -97;
    }
    static int unittilli_turaarut(int 서술자, int turaarut, int takininga_atuutilik) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int 결과 = qaujigiarli_turaarut(turaarut, takininga_atuutilik);
        if (결과 < 0) return 결과;
        if (Kasuqatigiitsimajut_nuuttarut[기술] != 0) return -22;
        int Kasuqatigiitsimajut_turaarut = turaarut_32(turaarut + 4);
        if (Kasuqatigiitsimajut_turaarut != 0 && Kasuqatigiitsimajut_turaarut != 통신망.내주소) return -99;
        int 접속번호 = sunakkutaaq_atuutilik.기억읽기(turaarut + 2) << 8 | sunakkutaaq_atuutilik.기억읽기(turaarut + 3);
        결과 = 통신망.matuirli(접속번호);
        if (결과 < 0) return 결과;
        Kasuqatigiitsimajut_nuuttarut[기술] = 결과; turaagaq[기술] = Kasuqatigiitsimajut_turaarut;
        return 0;
    }
    static int 자동묶기(int 기술) {
        if (Kasuqatigiitsimajut_nuuttarut[기술] != 0) return 0;
        int 결과 = 통신망.matuirli(0);
        if (결과 < 0) return 결과;
        Kasuqatigiitsimajut_nuuttarut[기술] = 결과;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 요청 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int titiqqat_turaarut, int takininga_atuutilik, int 설정, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (설정 != 0) return -95;
        if (takininga_atuutilik < 0 || takininga_atuutilik > 1024) return -90;
        if (takininga_atuutilik != 0 && !실행관리.Nakatigat(titiqqat_turaarut, takininga_atuutilik)) return -14;
        if (!실행관리.Nakatigat(요청주소, 8)) return -14;
        int turaarut = 실행관리.수(요청주소);
        int 결과 = qaujigiarli_turaarut(turaarut, 실행관리.수(요청주소 + 4));
        if (결과 < 0) return 결과;
        int 접속번호 = sunakkutaaq_atuutilik.기억읽기(turaarut + 2) << 8 | sunakkutaaq_atuutilik.기억읽기(turaarut + 3);
        if (접속번호 == 0) return -22;
        결과 = 자동묶기(기술);
        if (결과 < 0) return 결과;
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < takininga_atuutilik; nalunaiqsimavik++) aullaaqtilli_titiqqat[nalunaiqsimavik] = sunakkutaaq_atuutilik.기억읽기(titiqqat_turaarut + nalunaiqsimavik);
        return 통신망.nassiutili(Kasuqatigiitsimajut_nuuttarut[기술], turaarut_32(turaarut + 4), 접속번호, aullaaqtilli_titiqqat, takininga_atuutilik);
    }
    static void titiraq_turaarut(int turaarut, int takininga_atuutilik, int Kasuqatigiitsimajut_turaarut, int 접속번호) {
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < takininga_atuutilik && nalunaiqsimavik < 16; nalunaiqsimavik++) {
            int atuutilik = 0;
            if (nalunaiqsimavik == 0) atuutilik = 2;
            if (nalunaiqsimavik == 2) atuutilik = 접속번호 >>> 8;
            if (nalunaiqsimavik == 3) atuutilik = 접속번호;
            if (nalunaiqsimavik >= 4 && nalunaiqsimavik < 8) atuutilik = Kasuqatigiitsimajut_turaarut >>> (56 - nalunaiqsimavik * 8);
            sunakkutaaq_atuutilik.titiraq_puigujjaikkut(turaarut + nalunaiqsimavik, atuutilik & 255);
        }
    }
    static int 자료전문받기(int 서술자, int titiqqat_turaarut, int takininga_atuutilik, int 설정, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((설정 & ~64) != 0) return -95;
        if (takininga_atuutilik < 0) return -22;
        if (takininga_atuutilik != 0 && !실행관리.Nakatigat(titiqqat_turaarut, takininga_atuutilik)) return -14;
        int turaarut = 0, turaarut_takininga_turaarut = 0, turaarut_takininga = 0;
        if (요청주소 != 0) {
            if (!실행관리.Nakatigat(요청주소, 8)) return -14;
            turaarut = 실행관리.수(요청주소); turaarut_takininga_turaarut = 실행관리.수(요청주소 + 4);
            if (turaarut != 0) {
                if (!실행관리.Nakatigat(turaarut_takininga_turaarut, 4)) return -14;
                turaarut_takininga = 실행관리.수(turaarut_takininga_turaarut);
                if (turaarut_takininga < 0) return -22;
                if (!실행관리.Nakatigat(turaarut, turaarut_takininga < 16 ? turaarut_takininga : 16)) return -14;
            }
        }
        int 결과 = 자동묶기(기술);
        if (결과 < 0) return 결과;
        int 시작 = sunakkutaaq_atuutilik.밀리초();
        while (true) {
            결과 = 통신망.받기(Kasuqatigiitsimajut_nuuttarut[기술], aullaaqtilli_titiqqat, 1024, 0);
            if (결과 != -11) break;
            if ((설정 & 64) != 0 || (열기설정[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && sunakkutaaq_atuutilik.밀리초() - 시작 >= 수신대기밀리초[기술]) return -11;
            if (sunakkutaaq_atuutilik.사용자남은밀리초() <= 10) return -11;
            sunakkutaaq_atuutilik.잠시양보();
        }
        if (결과 < 0) return 결과;
        if (결과 > takininga_atuutilik) 결과 = takininga_atuutilik;
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 결과; nalunaiqsimavik++) sunakkutaaq_atuutilik.titiraq_puigujjaikkut(titiqqat_turaarut + nalunaiqsimavik, aullaaqtilli_titiqqat[nalunaiqsimavik]);
        if (turaarut != 0) {
            titiraq_turaarut(turaarut, turaarut_takininga, 통신망.ilagijaujuq_turaarut(Kasuqatigiitsimajut_nuuttarut[기술]), 통신망.상대접속번호(Kasuqatigiitsimajut_nuuttarut[기술]));
            실행관리.수쓰기(turaarut_takininga_turaarut, 16);
        }
        return 결과;
    }
    static int 통신주소읽기(int 서술자, int turaarut, int takininga_turaarut) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.Nakatigat(takininga_turaarut, 4)) return -14;
        int takininga_atuutilik = 실행관리.수(takininga_turaarut);
        if (takininga_atuutilik < 0) return -22;
        if (!실행관리.Nakatigat(turaarut, takininga_atuutilik < 16 ? takininga_atuutilik : 16)) return -14;
        int 칸 = 통신망.nalunaiqsimavik(Kasuqatigiitsimajut_nuuttarut[기술]);
        titiraq_turaarut(turaarut, takininga_atuutilik, turaagaq[기술], 칸 < 0 ? 0 : 통신망.접속번호들[칸]);
        실행관리.수쓰기(takininga_turaarut, 16);
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
