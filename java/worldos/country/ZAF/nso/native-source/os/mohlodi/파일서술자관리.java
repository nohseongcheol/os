// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 mošomiši 과정의 파일서술자와 열린 Faele 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int bala_ngwala_folaga = 2, 만들기 = 64, 독점생성 = 128, tloša_TOC = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] bula_tshwaro = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], nepo = new int[서술자한도];
    static int[] 파일위치 = new int[서술자한도], bula_Dipeakanyo = new int[서술자한도], 참조수 = new int[서술자한도];
    static int[] Netweke_tshwaro = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] tsela_leina = new int[64], fetišetša_data = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return bula_tshwaro[파일서술자] - 1;
    }
    static int 빈서술자(int Diriša) {
        for (int lokela = Diriša; lokela < 서술자한도; lokela++) if (bula_tshwaro[lokela] == 0) return lokela;
        return -24;
    }
    static int hloka_selo_tshwaro() {
        for (int lokela = 0; lokela < 서술자한도; lokela++) if (참조수[lokela] == 0) return lokela;
        return -24;
    }
    static int Ikgokaganye(int 서술자, int 기술, int 파일종류, int faele_nepo, int Dipeakanyo) {
        bula_tshwaro[서술자] = 기술 + 1; 서술자설정[서술자] = (Dipeakanyo & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; nepo[기술] = faele_nepo; 참조수[기술] = 1;
        bula_Dipeakanyo[기술] = Dipeakanyo & (3 | 이어쓰기 | 기다리지않기); 파일위치[기술] = 0;
        Netweke_tshwaro[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void Thomišo_tiragalo() {
        과정정리();
        for (int lokela = 0; lokela < 3; lokela++) Ikgokaganye(lokela, lokela, 1, lokela, lokela == 0 ? 0 : 1);
    }
    static void 과정정리() {
        for (int lokela = 0; lokela < 서술자한도; lokela++) if (bula_tshwaro[lokela] != 0) tswalela_faele(lokela);
    }
    static int tswalela_faele(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        bula_tshwaro[서술자] = 0; 서술자설정[서술자] = 0;
        참조수[기술]--;
        if (참조수[기술] == 0) {
            if (종류[기술] == 2) memori_tshepedišo_ya_difaele.열림수[nepo[기술]]--;
            if (종류[기술] == 3 && Netweke_tshwaro[기술] != 0) Netweke_kgoboko.Tswalela(Netweke_tshwaro[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 paete_boleng 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int atrese) {
        if (!실행관리.setsopolwa(atrese, 1)) return -14;
        int 위치 = sedirišwa_boleng.기억읽기(atrese) == '/' ? 1 : 0;
        for (int botelele_boleng = 0; botelele_boleng < 64; botelele_boleng++) {
            if (!실행관리.setsopolwa(atrese + 위치 + botelele_boleng, 1)) return -14;
            int boleng = sedirišwa_boleng.기억읽기(atrese + 위치 + botelele_boleng);
            tsela_leina[botelele_boleng] = boleng;
            if (boleng == 0) return botelele_boleng == 0 ? -2 : (memori_tshepedišo_ya_difaele.lekola_leina(tsela_leina, botelele_boleng) ? botelele_boleng : -22);
            if (boleng == '/') return -20;
        }
        return -36;
    }
    static int bula_faele(int leina_atrese, int Dipeakanyo, int 허가) {
        int botelele_boleng = 경로읽기(leina_atrese);
        if (botelele_boleng < 0) return botelele_boleng;
        if ((Dipeakanyo & ~(3 | 만들기 | 독점생성 | tloša_TOC | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Dipeakanyo & 3) == 3 || ((Dipeakanyo & tloša_TOC) != 0 && (Dipeakanyo & 3) == 0)) return -22;
        int Faele = memori_tshepedišo_ya_difaele.hwetša_go_tsenya_tshedimošo(tsela_leina, botelele_boleng);
        if (Faele >= 0 && (Dipeakanyo & (만들기 | 독점생성)) == (만들기 | 독점생성)) return -17;
        if (Faele == -2 && (Dipeakanyo & 만들기) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = hloka_selo_tshwaro();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Faele == -2) {
            int 결과 = memori_tshepedišo_ya_difaele.lota_boleng(tsela_leina, botelele_boleng, tsela_leina, 0);
            if (결과 < 0) return 결과;
            Faele = memori_tshepedišo_ya_difaele.hwetša_go_tsenya_tshedimošo(tsela_leina, botelele_boleng);
            memori_tshepedišo_ya_difaele.허가들[Faele] = 허가 & 511;
        }
        if (Faele < 0) return Faele;
        if ((Dipeakanyo & tloša_TOC) != 0) memori_tshepedišo_ya_difaele.bogolo_Lenaneo[Faele] = 0;
        memori_tshepedišo_ya_difaele.열림수[Faele]++;
        return Ikgokaganye(서술자, 기술, 2, Faele, Dipeakanyo);
    }
    static int 파일읽기(int 서술자, int data_atrese, int botelele_boleng) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (bula_Dipeakanyo[기술] & 3) == 1) return -9;
        if (botelele_boleng < 0) return -22;
        if (botelele_boleng == 0) return 0;
        if (!실행관리.setsopolwa(data_atrese, botelele_boleng)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, data_atrese, botelele_boleng, 0, 0);
        if (종류[기술] == 1) {
            int 받은수 = 0;
            while (받은수 < botelele_boleng) {
                int boleng = 문자단말.직렬읽기();
                if (boleng < 0) boleng = khiipote.Bala();
                if (boleng < 0) {
                    if (받은수 > 0) return 받은수;
                    if ((bula_Dipeakanyo[기술] & 기다리지않기) != 0) return -11;
                    if (sedirišwa_boleng.사용자남은밀리초() <= 10) return -11;
                    Netweke_kgoboko.kgonthiša(); sedirišwa_boleng.잠시양보();
                } else {
                    sedirišwa_boleng.ngwala_memori(data_atrese + 받은수, boleng); 받은수++;
                }
            }
            return 받은수;
        }
        int Faele = nepo[기술], 위치 = 파일위치[기술];
        if (위치 >= memori_tshepedišo_ya_difaele.bogolo_Lenaneo[Faele]) return 0;
        if (botelele_boleng > memori_tshepedišo_ya_difaele.bogolo_Lenaneo[Faele] - 위치) botelele_boleng = memori_tshepedišo_ya_difaele.bogolo_Lenaneo[Faele] - 위치;
        int 원본주소 = sedirišwa_boleng.faele_memori() + Faele * memori_tshepedišo_ya_difaele.최대크기 + 위치;
        for (int lokela = 0; lokela < botelele_boleng; lokela++) sedirišwa_boleng.ngwala_memori(data_atrese + lokela, sedirišwa_boleng.기억읽기(원본주소 + lokela));
        파일위치[기술] += botelele_boleng;
        return botelele_boleng;
    }
    static int ngwala_faele(int 서술자, int data_atrese, int botelele_boleng) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (bula_Dipeakanyo[기술] & 3) == 0) return -9;
        if (botelele_boleng < 0) return -22;
        if (botelele_boleng == 0) return 0;
        if (!실행관리.setsopolwa(data_atrese, botelele_boleng)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 boyo_boleng 주소가 필요하다.
        if (종류[기술] == 1) {
            if (botelele_boleng > 16384) botelele_boleng = 16384;
            for (int lokela = 0; lokela < botelele_boleng; lokela++) {
                int boleng = sedirišwa_boleng.기억읽기(data_atrese + lokela);
                문자단말.직렬바이트(boleng); 문자단말.화면문자(boleng);
            }
            return botelele_boleng;
        }
        int Faele = nepo[기술], Bogolo = memori_tshepedišo_ya_difaele.bogolo_Lenaneo[Faele];
        int 위치 = (bula_Dipeakanyo[기술] & 이어쓰기) != 0 ? Bogolo : 파일위치[기술];
        if (위치 >= memori_tshepedišo_ya_difaele.최대크기) return -27;
        if (botelele_boleng > memori_tshepedišo_ya_difaele.최대크기 - 위치) botelele_boleng = memori_tshepedišo_ya_difaele.최대크기 - 위치;
        int boyo_atrese = sedirišwa_boleng.faele_memori() + Faele * memori_tshepedišo_ya_difaele.최대크기;
        for (int lokela = Bogolo; lokela < 위치; lokela++) sedirišwa_boleng.ngwala_memori(boyo_atrese + lokela, 0);
        for (int lokela = 0; lokela < botelele_boleng; lokela++) sedirišwa_boleng.ngwala_memori(boyo_atrese + 위치 + lokela, sedirišwa_boleng.기억읽기(data_atrese + lokela));
        파일위치[기술] = 위치 + botelele_boleng;
        if (위치 + botelele_boleng > Bogolo) memori_tshepedišo_ya_difaele.bogolo_Lenaneo[Faele] = 위치 + botelele_boleng;
        return botelele_boleng;
    }
    static int nyaka_faele(int 서술자, int E_Šetšego_boleng, int 기준) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (기준 < 0 || 기준 > 2) return -22;
        int Bokamorago_boleng = 기준 == 0 ? 0 : (기준 == 1 ? 파일위치[기술] : memori_tshepedišo_ya_difaele.bogolo_Lenaneo[nepo[기술]]);
        if (E_Šetšego_boleng > 0 && Bokamorago_boleng > 2147483647 - E_Šetšego_boleng) return -75;
        if (E_Šetšego_boleng < 0 && E_Šetšego_boleng < -Bokamorago_boleng) return -22;
        파일위치[기술] = Bokamorago_boleng + E_Šetšego_boleng;
        return 파일위치[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean abela_boleng, int Dipeakanyo) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return abela_boleng ? -9 : -22;
        if (abela_boleng && 서술자 == 새서술자) return 새서술자;
        if (abela_boleng) { if (bula_tshwaro[새서술자] != 0) tswalela_faele(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        bula_tshwaro[새서술자] = 기술 + 1; 서술자설정[새서술자] = Dipeakanyo; 참조수[기술]++;
        return 새서술자;
    }
    static int tloša_faele_go_tsenya_tshedimošo_leina(int leina_atrese) {
        int botelele_boleng = 경로읽기(leina_atrese);
        if (botelele_boleng < 0) return botelele_boleng;
        int Faele = memori_tshepedišo_ya_difaele.hwetša_go_tsenya_tshedimošo(tsela_leina, botelele_boleng);
        if (Faele < 0) return Faele;
        memori_tshepedišo_ya_difaele.이름들[Faele * 64] = 0;
        return 0;
    }
    static int sehlopha_faele_botelele(int 서술자, int botelele_boleng) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (bula_Dipeakanyo[기술] & 3) == 0 || botelele_boleng < 0) return -22;
        if (botelele_boleng > memori_tshepedišo_ya_difaele.최대크기) return -27;
        int Faele = nepo[기술], atrese = sedirišwa_boleng.faele_memori() + Faele * memori_tshepedišo_ya_difaele.최대크기;
        for (int lokela = memori_tshepedišo_ya_difaele.bogolo_Lenaneo[Faele]; lokela < botelele_boleng; lokela++) sedirišwa_boleng.ngwala_memori(atrese + lokela, 0);
        memori_tshepedišo_ya_difaele.bogolo_Lenaneo[Faele] = botelele_boleng;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int atrese) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.setsopolwa(atrese, 48)) return -14;
        for (int lokela = 0; lokela < 12; lokela++) 실행관리.수쓰기(atrese + lokela * 4, 0);
        int Faele = nepo[기술], Bogolo = 종류[기술] == 2 ? memori_tshepedišo_ya_difaele.bogolo_Lenaneo[Faele] : 0;
        int 허가 = 종류[기술] == 2 ? memori_tshepedišo_ya_difaele.허가들[Faele] : 438;
        실행관리.수쓰기(atrese, 1);
        실행관리.수쓰기(atrese + 4, 종류[기술] == 2 ? Faele + 1 : 100 + 기술);
        실행관리.수쓰기(atrese + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(atrese + 12, 종류[기술] == 2 && memori_tshepedišo_ya_difaele.이름들[Faele * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(atrese + 28, Bogolo); 실행관리.수쓰기(atrese + 32, 512);
        실행관리.수쓰기(atrese + 36, (Bogolo + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int Taelo, int boleng) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Taelo == 0 || Taelo == 1030) return 서술자복제(서술자, boleng, false, Taelo == 1030 ? 1 : 0);
        if (Taelo == 1) return 서술자설정[서술자];
        if (Taelo == 2) { if ((boleng & ~1) != 0) return -22; 서술자설정[서술자] = boleng; return 0; }
        if (Taelo == 3) return bula_Dipeakanyo[기술];
        if (Taelo == 4) {
            if ((boleng & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            bula_Dipeakanyo[기술] = (bula_Dipeakanyo[기술] & 3) | (boleng & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int 통신종단점만들기(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = hloka_selo_tshwaro();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Ikgokaganye(서술자, 기술, 3, 0, bala_ngwala_folaga);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int atrese_32(int atrese) {
        return sedirišwa_boleng.기억읽기(atrese) << 24 | sedirišwa_boleng.기억읽기(atrese + 1) << 16
            | sedirišwa_boleng.기억읽기(atrese + 2) << 8 | sedirišwa_boleng.기억읽기(atrese + 3);
    }
    static int lekola_atrese(int atrese, int botelele_boleng) {
        if (botelele_boleng < 16) return -22;
        if (!실행관리.setsopolwa(atrese, 16)) return -14;
        return 실행관리.짧은수(atrese) == 2 ? 0 : -97;
    }
    static int tlama_atrese(int 서술자, int atrese, int botelele_boleng) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int 결과 = lekola_atrese(atrese, botelele_boleng);
        if (결과 < 0) return 결과;
        if (Netweke_tshwaro[기술] != 0) return -22;
        int Netweke_atrese = atrese_32(atrese + 4);
        if (Netweke_atrese != 0 && Netweke_atrese != Netweke_kgoboko.내주소) return -99;
        int 접속번호 = sedirišwa_boleng.기억읽기(atrese + 2) << 8 | sedirišwa_boleng.기억읽기(atrese + 3);
        결과 = Netweke_kgoboko.Bula(접속번호);
        if (결과 < 0) return 결과;
        Netweke_tshwaro[기술] = 결과; nepo[기술] = Netweke_atrese;
        return 0;
    }
    static int 자동묶기(int 기술) {
        if (Netweke_tshwaro[기술] != 0) return 0;
        int 결과 = Netweke_kgoboko.Bula(0);
        if (결과 < 0) return 결과;
        Netweke_tshwaro[기술] = 결과;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 요청 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int data_atrese, int botelele_boleng, int Dipeakanyo, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Dipeakanyo != 0) return -95;
        if (botelele_boleng < 0 || botelele_boleng > 1024) return -90;
        if (botelele_boleng != 0 && !실행관리.setsopolwa(data_atrese, botelele_boleng)) return -14;
        if (!실행관리.setsopolwa(요청주소, 8)) return -14;
        int atrese = 실행관리.수(요청주소);
        int 결과 = lekola_atrese(atrese, 실행관리.수(요청주소 + 4));
        if (결과 < 0) return 결과;
        int 접속번호 = sedirišwa_boleng.기억읽기(atrese + 2) << 8 | sedirišwa_boleng.기억읽기(atrese + 3);
        if (접속번호 == 0) return -22;
        결과 = 자동묶기(기술);
        if (결과 < 0) return 결과;
        for (int lokela = 0; lokela < botelele_boleng; lokela++) fetišetša_data[lokela] = sedirišwa_boleng.기억읽기(data_atrese + lokela);
        return Netweke_kgoboko.Romela(Netweke_tshwaro[기술], atrese_32(atrese + 4), 접속번호, fetišetša_data, botelele_boleng);
    }
    static void ngwala_atrese(int atrese, int botelele_boleng, int Netweke_atrese, int 접속번호) {
        for (int lokela = 0; lokela < botelele_boleng && lokela < 16; lokela++) {
            int boleng = 0;
            if (lokela == 0) boleng = 2;
            if (lokela == 2) boleng = 접속번호 >>> 8;
            if (lokela == 3) boleng = 접속번호;
            if (lokela >= 4 && lokela < 8) boleng = Netweke_atrese >>> (56 - lokela * 8);
            sedirišwa_boleng.ngwala_memori(atrese + lokela, boleng & 255);
        }
    }
    static int 자료전문받기(int 서술자, int data_atrese, int botelele_boleng, int Dipeakanyo, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Dipeakanyo & ~64) != 0) return -95;
        if (botelele_boleng < 0) return -22;
        if (botelele_boleng != 0 && !실행관리.setsopolwa(data_atrese, botelele_boleng)) return -14;
        int atrese = 0, atrese_botelele_atrese = 0, atrese_botelele = 0;
        if (요청주소 != 0) {
            if (!실행관리.setsopolwa(요청주소, 8)) return -14;
            atrese = 실행관리.수(요청주소); atrese_botelele_atrese = 실행관리.수(요청주소 + 4);
            if (atrese != 0) {
                if (!실행관리.setsopolwa(atrese_botelele_atrese, 4)) return -14;
                atrese_botelele = 실행관리.수(atrese_botelele_atrese);
                if (atrese_botelele < 0) return -22;
                if (!실행관리.setsopolwa(atrese, atrese_botelele < 16 ? atrese_botelele : 16)) return -14;
            }
        }
        int 결과 = 자동묶기(기술);
        if (결과 < 0) return 결과;
        int Diriša = sedirišwa_boleng.밀리초();
        while (true) {
            결과 = Netweke_kgoboko.받기(Netweke_tshwaro[기술], fetišetša_data, 1024, 0);
            if (결과 != -11) break;
            if ((Dipeakanyo & 64) != 0 || (bula_Dipeakanyo[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && sedirišwa_boleng.밀리초() - Diriša >= 수신대기밀리초[기술]) return -11;
            if (sedirišwa_boleng.사용자남은밀리초() <= 10) return -11;
            sedirišwa_boleng.잠시양보();
        }
        if (결과 < 0) return 결과;
        if (결과 > botelele_boleng) 결과 = botelele_boleng;
        for (int lokela = 0; lokela < 결과; lokela++) sedirišwa_boleng.ngwala_memori(data_atrese + lokela, fetišetša_data[lokela]);
        if (atrese != 0) {
            ngwala_atrese(atrese, atrese_botelele, Netweke_kgoboko.sedirišwa_sa_legoro_le_tee_atrese(Netweke_tshwaro[기술]), Netweke_kgoboko.상대접속번호(Netweke_tshwaro[기술]));
            실행관리.수쓰기(atrese_botelele_atrese, 16);
        }
        return 결과;
    }
    static int 통신주소읽기(int 서술자, int atrese, int botelele_atrese) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.setsopolwa(botelele_atrese, 4)) return -14;
        int botelele_boleng = 실행관리.수(botelele_atrese);
        if (botelele_boleng < 0) return -22;
        if (!실행관리.setsopolwa(atrese, botelele_boleng < 16 ? botelele_boleng : 16)) return -14;
        int sekgobana_go_tsenya_tshedimošo = Netweke_kgoboko.lokela(Netweke_tshwaro[기술]);
        ngwala_atrese(atrese, botelele_boleng, nepo[기술], sekgobana_go_tsenya_tshedimošo < 0 ? 0 : Netweke_kgoboko.접속번호들[sekgobana_go_tsenya_tshedimošo]);
        실행관리.수쓰기(botelele_atrese, 16);
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
