// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 modirisi 과정의 파일서술자와 열린 faele 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int buisa_kwala_folaga = 2, tlhama_tsenyo = 64, 독점생성 = 128, phimola_TOC = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] bula_mokgwakamogelo = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], setotwa = new int[서술자한도];
    static int[] 파일위치 = new int[서술자한도], bula_Diseting = new int[서술자한도], 참조수 = new int[서술자한도];
    static int[] Neteweke_mokgwakamogelo = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] tsela_leina = new int[64], fudusa_tshedimosetso = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return bula_mokgwakamogelo[파일서술자] - 1;
    }
    static int 빈서술자(int dirisa) {
        for (int tshupane = dirisa; tshupane < 서술자한도; tshupane++) if (bula_mokgwakamogelo[tshupane] == 0) return tshupane;
        return -24;
    }
    static int lolea_mokgwakamogelo() {
        for (int tshupane = 0; tshupane < 서술자한도; tshupane++) if (참조수[tshupane] == 0) return tshupane;
        return -24;
    }
    static int Golaganya(int 서술자, int 기술, int 파일종류, int faele_setotwa, int Diseting) {
        bula_mokgwakamogelo[서술자] = 기술 + 1; 서술자설정[서술자] = (Diseting & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; setotwa[기술] = faele_setotwa; 참조수[기술] = 1;
        bula_Diseting[기술] = Diseting & (3 | 이어쓰기 | 기다리지않기); 파일위치[기술] = 0;
        Neteweke_mokgwakamogelo[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void simolola_Thulaganyo() {
        과정정리();
        for (int tshupane = 0; tshupane < 3; tshupane++) Golaganya(tshupane, tshupane, 1, tshupane, tshupane == 0 ? 0 : 1);
    }
    static void 과정정리() {
        for (int tshupane = 0; tshupane < 서술자한도; tshupane++) if (bula_mokgwakamogelo[tshupane] != 0) tswala_faele(tshupane);
    }
    static int tswala_faele(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        bula_mokgwakamogelo[서술자] = 0; 서술자설정[서술자] = 0;
        참조수[기술]--;
        if (참조수[기술] == 0) {
            if (종류[기술] == 2) memori_setsamaisadifaele.열림수[setotwa[기술]]--;
            if (종류[기술] == 3 && Neteweke_mokgwakamogelo[기술] != 0) Neteweke_kokoanyodinepe.tswala(Neteweke_mokgwakamogelo[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 baete_Boleng 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int aterese) {
        if (!실행관리.faelekhutshwe_ya_media(aterese, 1)) return -14;
        int 위치 = mobaele_Boleng.기억읽기(aterese) == '/' ? 1 : 0;
        for (int boleele_Boleng = 0; boleele_Boleng < 64; boleele_Boleng++) {
            if (!실행관리.faelekhutshwe_ya_media(aterese + 위치 + boleele_Boleng, 1)) return -14;
            int Boleng = mobaele_Boleng.기억읽기(aterese + 위치 + boleele_Boleng);
            tsela_leina[boleele_Boleng] = Boleng;
            if (Boleng == 0) return boleele_Boleng == 0 ? -2 : (memori_setsamaisadifaele.tlhola_leina(tsela_leina, boleele_Boleng) ? boleele_Boleng : -22);
            if (Boleng == '/') return -20;
        }
        return -36;
    }
    static int bula_faele(int leina_aterese, int Diseting, int 허가) {
        int boleele_Boleng = 경로읽기(leina_aterese);
        if (boleele_Boleng < 0) return boleele_Boleng;
        if ((Diseting & ~(3 | tlhama_tsenyo | 독점생성 | phimola_TOC | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Diseting & 3) == 3 || ((Diseting & phimola_TOC) != 0 && (Diseting & 3) == 0)) return -22;
        int faele = memori_setsamaisadifaele.batla_tsenyo(tsela_leina, boleele_Boleng);
        if (faele >= 0 && (Diseting & (tlhama_tsenyo | 독점생성)) == (tlhama_tsenyo | 독점생성)) return -17;
        if (faele == -2 && (Diseting & tlhama_tsenyo) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = lolea_mokgwakamogelo();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (faele == -2) {
            int 결과 = memori_setsamaisadifaele.Store_Boleng(tsela_leina, boleele_Boleng, tsela_leina, 0);
            if (결과 < 0) return 결과;
            faele = memori_setsamaisadifaele.batla_tsenyo(tsela_leina, boleele_Boleng);
            memori_setsamaisadifaele.허가들[faele] = 허가 & 511;
        }
        if (faele < 0) return faele;
        if ((Diseting & phimola_TOC) != 0) memori_setsamaisadifaele.lekanya_lenaane[faele] = 0;
        memori_setsamaisadifaele.열림수[faele]++;
        return Golaganya(서술자, 기술, 2, faele, Diseting);
    }
    static int 파일읽기(int 서술자, int tshedimosetso_aterese, int boleele_Boleng) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (bula_Diseting[기술] & 3) == 1) return -9;
        if (boleele_Boleng < 0) return -22;
        if (boleele_Boleng == 0) return 0;
        if (!실행관리.faelekhutshwe_ya_media(tshedimosetso_aterese, boleele_Boleng)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, tshedimosetso_aterese, boleele_Boleng, 0, 0);
        if (종류[기술] == 1) {
            int 받은수 = 0;
            while (받은수 < boleele_Boleng) {
                int Boleng = 문자단말.직렬읽기();
                if (Boleng < 0) Boleng = Khiiboto.읽기();
                if (Boleng < 0) {
                    if (받은수 > 0) return 받은수;
                    if ((bula_Diseting[기술] & 기다리지않기) != 0) return -11;
                    if (mobaele_Boleng.사용자남은밀리초() <= 10) return -11;
                    Neteweke_kokoanyodinepe.netefatsa(); mobaele_Boleng.잠시양보();
                } else {
                    mobaele_Boleng.kwala_memori(tshedimosetso_aterese + 받은수, Boleng); 받은수++;
                }
            }
            return 받은수;
        }
        int faele = setotwa[기술], 위치 = 파일위치[기술];
        if (위치 >= memori_setsamaisadifaele.lekanya_lenaane[faele]) return 0;
        if (boleele_Boleng > memori_setsamaisadifaele.lekanya_lenaane[faele] - 위치) boleele_Boleng = memori_setsamaisadifaele.lekanya_lenaane[faele] - 위치;
        int 원본주소 = mobaele_Boleng.faele_memori() + faele * memori_setsamaisadifaele.최대크기 + 위치;
        for (int tshupane = 0; tshupane < boleele_Boleng; tshupane++) mobaele_Boleng.kwala_memori(tshedimosetso_aterese + tshupane, mobaele_Boleng.기억읽기(원본주소 + tshupane));
        파일위치[기술] += boleele_Boleng;
        return boleele_Boleng;
    }
    static int kwala_faele(int 서술자, int tshedimosetso_aterese, int boleele_Boleng) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (bula_Diseting[기술] & 3) == 0) return -9;
        if (boleele_Boleng < 0) return -22;
        if (boleele_Boleng == 0) return 0;
        if (!실행관리.faelekhutshwe_ya_media(tshedimosetso_aterese, boleele_Boleng)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 bogorogelo_Boleng 주소가 필요하다.
        if (종류[기술] == 1) {
            if (boleele_Boleng > 16384) boleele_Boleng = 16384;
            for (int tshupane = 0; tshupane < boleele_Boleng; tshupane++) {
                int Boleng = mobaele_Boleng.기억읽기(tshedimosetso_aterese + tshupane);
                문자단말.직렬바이트(Boleng); 문자단말.화면문자(Boleng);
            }
            return boleele_Boleng;
        }
        int faele = setotwa[기술], lekanya = memori_setsamaisadifaele.lekanya_lenaane[faele];
        int 위치 = (bula_Diseting[기술] & 이어쓰기) != 0 ? lekanya : 파일위치[기술];
        if (위치 >= memori_setsamaisadifaele.최대크기) return -27;
        if (boleele_Boleng > memori_setsamaisadifaele.최대크기 - 위치) boleele_Boleng = memori_setsamaisadifaele.최대크기 - 위치;
        int bogorogelo_aterese = mobaele_Boleng.faele_memori() + faele * memori_setsamaisadifaele.최대크기;
        for (int tshupane = lekanya; tshupane < 위치; tshupane++) mobaele_Boleng.kwala_memori(bogorogelo_aterese + tshupane, 0);
        for (int tshupane = 0; tshupane < boleele_Boleng; tshupane++) mobaele_Boleng.kwala_memori(bogorogelo_aterese + 위치 + tshupane, mobaele_Boleng.기억읽기(tshedimosetso_aterese + tshupane));
        파일위치[기술] = 위치 + boleele_Boleng;
        if (위치 + boleele_Boleng > lekanya) memori_setsamaisadifaele.lekanya_lenaane[faele] = 위치 + boleele_Boleng;
        return boleele_Boleng;
    }
    static int batla_faele(int 서술자, int Baya_ka_Tekatekanyo_Boleng, int 기준) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (기준 < 0 || 기준 > 2) return -22;
        int Lemorago_Boleng = 기준 == 0 ? 0 : (기준 == 1 ? 파일위치[기술] : memori_setsamaisadifaele.lekanya_lenaane[setotwa[기술]]);
        if (Baya_ka_Tekatekanyo_Boleng > 0 && Lemorago_Boleng > 2147483647 - Baya_ka_Tekatekanyo_Boleng) return -75;
        if (Baya_ka_Tekatekanyo_Boleng < 0 && Baya_ka_Tekatekanyo_Boleng < -Lemorago_Boleng) return -22;
        파일위치[기술] = Lemorago_Boleng + Baya_ka_Tekatekanyo_Boleng;
        return 파일위치[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean abela_Boleng, int Diseting) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return abela_Boleng ? -9 : -22;
        if (abela_Boleng && 서술자 == 새서술자) return 새서술자;
        if (abela_Boleng) { if (bula_mokgwakamogelo[새서술자] != 0) tswala_faele(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        bula_mokgwakamogelo[새서술자] = 기술 + 1; 서술자설정[새서술자] = Diseting; 참조수[기술]++;
        return 새서술자;
    }
    static int tlosa_faele_tsenyo_leina(int leina_aterese) {
        int boleele_Boleng = 경로읽기(leina_aterese);
        if (boleele_Boleng < 0) return boleele_Boleng;
        int faele = memori_setsamaisadifaele.batla_tsenyo(tsela_leina, boleele_Boleng);
        if (faele < 0) return faele;
        memori_setsamaisadifaele.이름들[faele * 64] = 0;
        return 0;
    }
    static int sete_faele_boleele(int 서술자, int boleele_Boleng) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (bula_Diseting[기술] & 3) == 0 || boleele_Boleng < 0) return -22;
        if (boleele_Boleng > memori_setsamaisadifaele.최대크기) return -27;
        int faele = setotwa[기술], aterese = mobaele_Boleng.faele_memori() + faele * memori_setsamaisadifaele.최대크기;
        for (int tshupane = memori_setsamaisadifaele.lekanya_lenaane[faele]; tshupane < boleele_Boleng; tshupane++) mobaele_Boleng.kwala_memori(aterese + tshupane, 0);
        memori_setsamaisadifaele.lekanya_lenaane[faele] = boleele_Boleng;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int aterese) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.faelekhutshwe_ya_media(aterese, 48)) return -14;
        for (int tshupane = 0; tshupane < 12; tshupane++) 실행관리.수쓰기(aterese + tshupane * 4, 0);
        int faele = setotwa[기술], lekanya = 종류[기술] == 2 ? memori_setsamaisadifaele.lekanya_lenaane[faele] : 0;
        int 허가 = 종류[기술] == 2 ? memori_setsamaisadifaele.허가들[faele] : 438;
        실행관리.수쓰기(aterese, 1);
        실행관리.수쓰기(aterese + 4, 종류[기술] == 2 ? faele + 1 : 100 + 기술);
        실행관리.수쓰기(aterese + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(aterese + 12, 종류[기술] == 2 && memori_setsamaisadifaele.이름들[faele * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(aterese + 28, lekanya); 실행관리.수쓰기(aterese + 32, 512);
        실행관리.수쓰기(aterese + 36, (lekanya + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int Taelo, int Boleng) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Taelo == 0 || Taelo == 1030) return 서술자복제(서술자, Boleng, false, Taelo == 1030 ? 1 : 0);
        if (Taelo == 1) return 서술자설정[서술자];
        if (Taelo == 2) { if ((Boleng & ~1) != 0) return -22; 서술자설정[서술자] = Boleng; return 0; }
        if (Taelo == 3) return bula_Diseting[기술];
        if (Taelo == 4) {
            if ((Boleng & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            bula_Diseting[기술] = (bula_Diseting[기술] & 3) | (Boleng & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int 통신종단점만들기(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = lolea_mokgwakamogelo();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Golaganya(서술자, 기술, 3, 0, buisa_kwala_folaga);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int aterese_32(int aterese) {
        return mobaele_Boleng.기억읽기(aterese) << 24 | mobaele_Boleng.기억읽기(aterese + 1) << 16
            | mobaele_Boleng.기억읽기(aterese + 2) << 8 | mobaele_Boleng.기억읽기(aterese + 3);
    }
    static int tlhola_aterese(int aterese, int boleele_Boleng) {
        if (boleele_Boleng < 16) return -22;
        if (!실행관리.faelekhutshwe_ya_media(aterese, 16)) return -14;
        return 실행관리.짧은수(aterese) == 2 ? 0 : -97;
    }
    static int BIND_aterese(int 서술자, int aterese, int boleele_Boleng) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int 결과 = tlhola_aterese(aterese, boleele_Boleng);
        if (결과 < 0) return 결과;
        if (Neteweke_mokgwakamogelo[기술] != 0) return -22;
        int Neteweke_aterese = aterese_32(aterese + 4);
        if (Neteweke_aterese != 0 && Neteweke_aterese != Neteweke_kokoanyodinepe.내주소) return -99;
        int 접속번호 = mobaele_Boleng.기억읽기(aterese + 2) << 8 | mobaele_Boleng.기억읽기(aterese + 3);
        결과 = Neteweke_kokoanyodinepe.bula(접속번호);
        if (결과 < 0) return 결과;
        Neteweke_mokgwakamogelo[기술] = 결과; setotwa[기술] = Neteweke_aterese;
        return 0;
    }
    static int 자동묶기(int 기술) {
        if (Neteweke_mokgwakamogelo[기술] != 0) return 0;
        int 결과 = Neteweke_kokoanyodinepe.bula(0);
        if (결과 < 0) return 결과;
        Neteweke_mokgwakamogelo[기술] = 결과;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 요청 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int tshedimosetso_aterese, int boleele_Boleng, int Diseting, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Diseting != 0) return -95;
        if (boleele_Boleng < 0 || boleele_Boleng > 1024) return -90;
        if (boleele_Boleng != 0 && !실행관리.faelekhutshwe_ya_media(tshedimosetso_aterese, boleele_Boleng)) return -14;
        if (!실행관리.faelekhutshwe_ya_media(요청주소, 8)) return -14;
        int aterese = 실행관리.수(요청주소);
        int 결과 = tlhola_aterese(aterese, 실행관리.수(요청주소 + 4));
        if (결과 < 0) return 결과;
        int 접속번호 = mobaele_Boleng.기억읽기(aterese + 2) << 8 | mobaele_Boleng.기억읽기(aterese + 3);
        if (접속번호 == 0) return -22;
        결과 = 자동묶기(기술);
        if (결과 < 0) return 결과;
        for (int tshupane = 0; tshupane < boleele_Boleng; tshupane++) fudusa_tshedimosetso[tshupane] = mobaele_Boleng.기억읽기(tshedimosetso_aterese + tshupane);
        return Neteweke_kokoanyodinepe.romela(Neteweke_mokgwakamogelo[기술], aterese_32(aterese + 4), 접속번호, fudusa_tshedimosetso, boleele_Boleng);
    }
    static void kwala_aterese(int aterese, int boleele_Boleng, int Neteweke_aterese, int 접속번호) {
        for (int tshupane = 0; tshupane < boleele_Boleng && tshupane < 16; tshupane++) {
            int Boleng = 0;
            if (tshupane == 0) Boleng = 2;
            if (tshupane == 2) Boleng = 접속번호 >>> 8;
            if (tshupane == 3) Boleng = 접속번호;
            if (tshupane >= 4 && tshupane < 8) Boleng = Neteweke_aterese >>> (56 - tshupane * 8);
            mobaele_Boleng.kwala_memori(aterese + tshupane, Boleng & 255);
        }
    }
    static int 자료전문받기(int 서술자, int tshedimosetso_aterese, int boleele_Boleng, int Diseting, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Diseting & ~64) != 0) return -95;
        if (boleele_Boleng < 0) return -22;
        if (boleele_Boleng != 0 && !실행관리.faelekhutshwe_ya_media(tshedimosetso_aterese, boleele_Boleng)) return -14;
        int aterese = 0, aterese_boleele_aterese = 0, aterese_boleele = 0;
        if (요청주소 != 0) {
            if (!실행관리.faelekhutshwe_ya_media(요청주소, 8)) return -14;
            aterese = 실행관리.수(요청주소); aterese_boleele_aterese = 실행관리.수(요청주소 + 4);
            if (aterese != 0) {
                if (!실행관리.faelekhutshwe_ya_media(aterese_boleele_aterese, 4)) return -14;
                aterese_boleele = 실행관리.수(aterese_boleele_aterese);
                if (aterese_boleele < 0) return -22;
                if (!실행관리.faelekhutshwe_ya_media(aterese, aterese_boleele < 16 ? aterese_boleele : 16)) return -14;
            }
        }
        int 결과 = 자동묶기(기술);
        if (결과 < 0) return 결과;
        int dirisa = mobaele_Boleng.밀리초();
        while (true) {
            결과 = Neteweke_kokoanyodinepe.받기(Neteweke_mokgwakamogelo[기술], fudusa_tshedimosetso, 1024, 0);
            if (결과 != -11) break;
            if ((Diseting & 64) != 0 || (bula_Diseting[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && mobaele_Boleng.밀리초() - dirisa >= 수신대기밀리초[기술]) return -11;
            if (mobaele_Boleng.사용자남은밀리초() <= 10) return -11;
            mobaele_Boleng.잠시양보();
        }
        if (결과 < 0) return 결과;
        if (결과 > boleele_Boleng) 결과 = boleele_Boleng;
        for (int tshupane = 0; tshupane < 결과; tshupane++) mobaele_Boleng.kwala_memori(tshedimosetso_aterese + tshupane, fudusa_tshedimosetso[tshupane]);
        if (aterese != 0) {
            kwala_aterese(aterese, aterese_boleele, Neteweke_kokoanyodinepe.semphato_aterese(Neteweke_mokgwakamogelo[기술]), Neteweke_kokoanyodinepe.상대접속번호(Neteweke_mokgwakamogelo[기술]));
            실행관리.수쓰기(aterese_boleele_aterese, 16);
        }
        return 결과;
    }
    static int 통신주소읽기(int 서술자, int aterese, int boleele_aterese) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.faelekhutshwe_ya_media(boleele_aterese, 4)) return -14;
        int boleele_Boleng = 실행관리.수(boleele_aterese);
        if (boleele_Boleng < 0) return -22;
        if (!실행관리.faelekhutshwe_ya_media(aterese, boleele_Boleng < 16 ? boleele_Boleng : 16)) return -14;
        int sebaka_tsenyo = Neteweke_kokoanyodinepe.tshupane(Neteweke_mokgwakamogelo[기술]);
        kwala_aterese(aterese, boleele_Boleng, setotwa[기술], sebaka_tsenyo < 0 ? 0 : Neteweke_kokoanyodinepe.접속번호들[sebaka_tsenyo]);
        실행관리.수쓰기(boleele_aterese, 16);
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
