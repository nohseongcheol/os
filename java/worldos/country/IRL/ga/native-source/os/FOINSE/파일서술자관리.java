// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 úsáideoir 과정의 파일서술자와 열린 Comhad 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int inléite_inscríofa_bratach = 2, Create_iontráil = 64, 독점생성 = 128, glan_TOC = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] oscail_hanla = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], sprioc = new int[서술자한도];
    static int[] comhad_suíomh = new int[서술자한도], oscail_Socruithe = new int[서술자한도], Leabhair_thagartha_COUNT = new int[서술자한도];
    static int[] Líonra_hanla = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] cosán_ainm = new int[64], traschur_sonraí = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return oscail_hanla[파일서술자] - 1;
    }
    static int 빈서술자(int Rith_2) {
        for (int INDEX = Rith_2; INDEX < 서술자한도; INDEX++) if (oscail_hanla[INDEX] == 0) return INDEX;
        return -24;
    }
    static int folamh_hanla() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (Leabhair_thagartha_COUNT[INDEX] == 0) return INDEX;
        return -24;
    }
    static int Nasc(int 서술자, int 기술, int 파일종류, int comhad_sprioc, int Socruithe) {
        oscail_hanla[서술자] = 기술 + 1; 서술자설정[서술자] = (Socruithe & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; sprioc[기술] = comhad_sprioc; Leabhair_thagartha_COUNT[기술] = 1;
        oscail_Socruithe[기술] = Socruithe & (3 | 이어쓰기 | 기다리지않기); comhad_suíomh[기술] = 0;
        Líonra_hanla[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void Start_Próiseas() {
        CLEAN_Próiseas();
        for (int INDEX = 0; INDEX < 3; INDEX++) Nasc(INDEX, INDEX, 1, INDEX, INDEX == 0 ? 0 : 1);
    }
    static void CLEAN_Próiseas() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (oscail_hanla[INDEX] != 0) dún_comhad(INDEX);
    }
    static int dún_comhad(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        oscail_hanla[서술자] = 0; 서술자설정[서술자] = 0;
        Leabhair_thagartha_COUNT[기술]--;
        if (Leabhair_thagartha_COUNT[기술] == 0) {
            if (종류[기술] == 2) Cuimhne_córas_comhad.oscail_COUNT[sprioc[기술]]--;
            if (종류[기술] == 3 && Líonra_hanla[기술] != 0) Líonra_Cruach.Dún(Líonra_hanla[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 beart_VALUE 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int ADDRESS) {
        if (!실행관리.gearrthóg(ADDRESS, 1)) return -14;
        int suíomh = gléas_VALUE.기억읽기(ADDRESS) == '/' ? 1 : 0;
        for (int fad_VALUE = 0; fad_VALUE < 64; fad_VALUE++) {
            if (!실행관리.gearrthóg(ADDRESS + suíomh + fad_VALUE, 1)) return -14;
            int VALUE = gléas_VALUE.기억읽기(ADDRESS + suíomh + fad_VALUE);
            cosán_ainm[fad_VALUE] = VALUE;
            if (VALUE == 0) return fad_VALUE == 0 ? -2 : (Cuimhne_córas_comhad.seic_ainm(cosán_ainm, fad_VALUE) ? fad_VALUE : -22);
            if (VALUE == '/') return -20;
        }
        return -36;
    }
    static int oscail_comhad(int ainm_ADDRESS, int Socruithe, int 허가) {
        int fad_VALUE = 경로읽기(ainm_ADDRESS);
        if (fad_VALUE < 0) return fad_VALUE;
        if ((Socruithe & ~(3 | Create_iontráil | 독점생성 | glan_TOC | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Socruithe & 3) == 3 || ((Socruithe & glan_TOC) != 0 && (Socruithe & 3) == 0)) return -22;
        int Comhad = Cuimhne_córas_comhad.FIND_iontráil(cosán_ainm, fad_VALUE);
        if (Comhad >= 0 && (Socruithe & (Create_iontráil | 독점생성)) == (Create_iontráil | 독점생성)) return -17;
        if (Comhad == -2 && (Socruithe & Create_iontráil) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = folamh_hanla();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Comhad == -2) {
            int tomhas = Cuimhne_córas_comhad.Store_VALUE(cosán_ainm, fad_VALUE, cosán_ainm, 0);
            if (tomhas < 0) return tomhas;
            Comhad = Cuimhne_córas_comhad.FIND_iontráil(cosán_ainm, fad_VALUE);
            Cuimhne_córas_comhad.허가들[Comhad] = 허가 & 511;
        }
        if (Comhad < 0) return Comhad;
        if ((Socruithe & glan_TOC) != 0) Cuimhne_córas_comhad.socraigh_méid_Liosta[Comhad] = 0;
        Cuimhne_córas_comhad.oscail_COUNT[Comhad]++;
        return Nasc(서술자, 기술, 2, Comhad, Socruithe);
    }
    static int 파일읽기(int 서술자, int sonraí_ADDRESS, int fad_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (oscail_Socruithe[기술] & 3) == 1) return -9;
        if (fad_VALUE < 0) return -22;
        if (fad_VALUE == 0) return 0;
        if (!실행관리.gearrthóg(sonraí_ADDRESS, fad_VALUE)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, sonraí_ADDRESS, fad_VALUE, 0, 0);
        if (종류[기술] == 1) {
            int RECEIVED_COUNT = 0;
            while (RECEIVED_COUNT < fad_VALUE) {
                int VALUE = SMS_Teirminéal.직렬읽기();
                if (VALUE < 0) VALUE = méarchlár.Léigh();
                if (VALUE < 0) {
                    if (RECEIVED_COUNT > 0) return RECEIVED_COUNT;
                    if ((oscail_Socruithe[기술] & 기다리지않기) != 0) return -11;
                    if (gléas_VALUE.사용자남은밀리초() <= 10) return -11;
                    Líonra_Cruach.fíoraigh(); gléas_VALUE.잠시양보();
                } else {
                    gléas_VALUE.scríobh_Cuimhne(sonraí_ADDRESS + RECEIVED_COUNT, VALUE); RECEIVED_COUNT++;
                }
            }
            return RECEIVED_COUNT;
        }
        int Comhad = sprioc[기술], suíomh = comhad_suíomh[기술];
        if (suíomh >= Cuimhne_córas_comhad.socraigh_méid_Liosta[Comhad]) return 0;
        if (fad_VALUE > Cuimhne_córas_comhad.socraigh_méid_Liosta[Comhad] - suíomh) fad_VALUE = Cuimhne_córas_comhad.socraigh_méid_Liosta[Comhad] - suíomh;
        int 원본주소 = gléas_VALUE.comhad_Cuimhne() + Comhad * Cuimhne_córas_comhad.최대크기 + suíomh;
        for (int INDEX = 0; INDEX < fad_VALUE; INDEX++) gléas_VALUE.scríobh_Cuimhne(sonraí_ADDRESS + INDEX, gléas_VALUE.기억읽기(원본주소 + INDEX));
        comhad_suíomh[기술] += fad_VALUE;
        return fad_VALUE;
    }
    static int scríobh_comhad(int 서술자, int sonraí_ADDRESS, int fad_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (oscail_Socruithe[기술] & 3) == 0) return -9;
        if (fad_VALUE < 0) return -22;
        if (fad_VALUE == 0) return 0;
        if (!실행관리.gearrthóg(sonraí_ADDRESS, fad_VALUE)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 sprioc_VALUE 주소가 필요하다.
        if (종류[기술] == 1) {
            if (fad_VALUE > 16384) fad_VALUE = 16384;
            for (int INDEX = 0; INDEX < fad_VALUE; INDEX++) {
                int VALUE = gléas_VALUE.기억읽기(sonraí_ADDRESS + INDEX);
                SMS_Teirminéal.직렬바이트(VALUE); SMS_Teirminéal.화면문자(VALUE);
            }
            return fad_VALUE;
        }
        int Comhad = sprioc[기술], Méid = Cuimhne_córas_comhad.socraigh_méid_Liosta[Comhad];
        int suíomh = (oscail_Socruithe[기술] & 이어쓰기) != 0 ? Méid : comhad_suíomh[기술];
        if (suíomh >= Cuimhne_córas_comhad.최대크기) return -27;
        if (fad_VALUE > Cuimhne_córas_comhad.최대크기 - suíomh) fad_VALUE = Cuimhne_córas_comhad.최대크기 - suíomh;
        int sprioc_ADDRESS_08bbd577 = gléas_VALUE.comhad_Cuimhne() + Comhad * Cuimhne_córas_comhad.최대크기;
        for (int INDEX = Méid; INDEX < suíomh; INDEX++) gléas_VALUE.scríobh_Cuimhne(sprioc_ADDRESS_08bbd577 + INDEX, 0);
        for (int INDEX = 0; INDEX < fad_VALUE; INDEX++) gléas_VALUE.scríobh_Cuimhne(sprioc_ADDRESS_08bbd577 + suíomh + INDEX, gléas_VALUE.기억읽기(sonraí_ADDRESS + INDEX));
        comhad_suíomh[기술] = suíomh + fad_VALUE;
        if (suíomh + fad_VALUE > Méid) Cuimhne_córas_comhad.socraigh_méid_Liosta[Comhad] = suíomh + fad_VALUE;
        return fad_VALUE;
    }
    static int lorg_comhad(int 서술자, int OFFSET_VALUE, int teilgean_fréamh) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (teilgean_fréamh < 0 || teilgean_fréamh > 2) return -22;
        int Cúlra_VALUE = teilgean_fréamh == 0 ? 0 : (teilgean_fréamh == 1 ? comhad_suíomh[기술] : Cuimhne_córas_comhad.socraigh_méid_Liosta[sprioc[기술]]);
        if (OFFSET_VALUE > 0 && Cúlra_VALUE > 2147483647 - OFFSET_VALUE) return -75;
        if (OFFSET_VALUE < 0 && OFFSET_VALUE < -Cúlra_VALUE) return -22;
        comhad_suíomh[기술] = Cúlra_VALUE + OFFSET_VALUE;
        return comhad_suíomh[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean 지정, int Socruithe) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return 지정 ? -9 : -22;
        if (지정 && 서술자 == 새서술자) return 새서술자;
        if (지정) { if (oscail_hanla[새서술자] != 0) dún_comhad(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        oscail_hanla[새서술자] = 기술 + 1; 서술자설정[새서술자] = Socruithe; Leabhair_thagartha_COUNT[기술]++;
        return 새서술자;
    }
    static int bain_comhad_iontráil_ainm(int ainm_ADDRESS) {
        int fad_VALUE = 경로읽기(ainm_ADDRESS);
        if (fad_VALUE < 0) return fad_VALUE;
        int Comhad = Cuimhne_córas_comhad.FIND_iontráil(cosán_ainm, fad_VALUE);
        if (Comhad < 0) return Comhad;
        Cuimhne_córas_comhad.이름들[Comhad * 64] = 0;
        return 0;
    }
    static int tacar_comhad_fad(int 서술자, int fad_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (oscail_Socruithe[기술] & 3) == 0 || fad_VALUE < 0) return -22;
        if (fad_VALUE > Cuimhne_córas_comhad.최대크기) return -27;
        int Comhad = sprioc[기술], ADDRESS = gléas_VALUE.comhad_Cuimhne() + Comhad * Cuimhne_córas_comhad.최대크기;
        for (int INDEX = Cuimhne_córas_comhad.socraigh_méid_Liosta[Comhad]; INDEX < fad_VALUE; INDEX++) gléas_VALUE.scríobh_Cuimhne(ADDRESS + INDEX, 0);
        Cuimhne_córas_comhad.socraigh_méid_Liosta[Comhad] = fad_VALUE;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int ADDRESS) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.gearrthóg(ADDRESS, 48)) return -14;
        for (int INDEX = 0; INDEX < 12; INDEX++) 실행관리.수쓰기(ADDRESS + INDEX * 4, 0);
        int Comhad = sprioc[기술], Méid = 종류[기술] == 2 ? Cuimhne_córas_comhad.socraigh_méid_Liosta[Comhad] : 0;
        int 허가 = 종류[기술] == 2 ? Cuimhne_córas_comhad.허가들[Comhad] : 438;
        실행관리.수쓰기(ADDRESS, 1);
        실행관리.수쓰기(ADDRESS + 4, 종류[기술] == 2 ? Comhad + 1 : 100 + 기술);
        실행관리.수쓰기(ADDRESS + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(ADDRESS + 12, 종류[기술] == 2 && Cuimhne_córas_comhad.이름들[Comhad * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(ADDRESS + 28, Méid); 실행관리.수쓰기(ADDRESS + 32, 512);
        실행관리.수쓰기(ADDRESS + 36, (Méid + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int Ordú, int VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Ordú == 0 || Ordú == 1030) return 서술자복제(서술자, VALUE, false, Ordú == 1030 ? 1 : 0);
        if (Ordú == 1) return 서술자설정[서술자];
        if (Ordú == 2) { if ((VALUE & ~1) != 0) return -22; 서술자설정[서술자] = VALUE; return 0; }
        if (Ordú == 3) return oscail_Socruithe[기술];
        if (Ordú == 4) {
            if ((VALUE & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            oscail_Socruithe[기술] = (oscail_Socruithe[기술] & 3) | (VALUE & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int 통신종단점만들기(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = folamh_hanla();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Nasc(서술자, 기술, 3, 0, inléite_inscríofa_bratach);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int ADDRESS_32(int ADDRESS) {
        return gléas_VALUE.기억읽기(ADDRESS) << 24 | gléas_VALUE.기억읽기(ADDRESS + 1) << 16
            | gléas_VALUE.기억읽기(ADDRESS + 2) << 8 | gléas_VALUE.기억읽기(ADDRESS + 3);
    }
    static int seic_ADDRESS(int ADDRESS, int fad_VALUE) {
        if (fad_VALUE < 16) return -22;
        if (!실행관리.gearrthóg(ADDRESS, 16)) return -14;
        return 실행관리.짧은수(ADDRESS) == 2 ? 0 : -97;
    }
    static int BIND_ADDRESS(int 서술자, int ADDRESS, int fad_VALUE) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int tomhas = seic_ADDRESS(ADDRESS, fad_VALUE);
        if (tomhas < 0) return tomhas;
        if (Líonra_hanla[기술] != 0) return -22;
        int Líonra_ADDRESS = ADDRESS_32(ADDRESS + 4);
        if (Líonra_ADDRESS != 0 && Líonra_ADDRESS != Líonra_Cruach.내주소) return -99;
        int uimhir_phoirt = gléas_VALUE.기억읽기(ADDRESS + 2) << 8 | gléas_VALUE.기억읽기(ADDRESS + 3);
        tomhas = Líonra_Cruach.Oscail(uimhir_phoirt);
        if (tomhas < 0) return tomhas;
        Líonra_hanla[기술] = tomhas; sprioc[기술] = Líonra_ADDRESS;
        return 0;
    }
    static int 자동묶기(int 기술) {
        if (Líonra_hanla[기술] != 0) return 0;
        int tomhas = Líonra_Cruach.Oscail(0);
        if (tomhas < 0) return tomhas;
        Líonra_hanla[기술] = tomhas;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 iarratas_HTTP 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int sonraí_ADDRESS, int fad_VALUE, int Socruithe, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Socruithe != 0) return -95;
        if (fad_VALUE < 0 || fad_VALUE > 1024) return -90;
        if (fad_VALUE != 0 && !실행관리.gearrthóg(sonraí_ADDRESS, fad_VALUE)) return -14;
        if (!실행관리.gearrthóg(요청주소, 8)) return -14;
        int ADDRESS = 실행관리.수(요청주소);
        int tomhas = seic_ADDRESS(ADDRESS, 실행관리.수(요청주소 + 4));
        if (tomhas < 0) return tomhas;
        int uimhir_phoirt = gléas_VALUE.기억읽기(ADDRESS + 2) << 8 | gléas_VALUE.기억읽기(ADDRESS + 3);
        if (uimhir_phoirt == 0) return -22;
        tomhas = 자동묶기(기술);
        if (tomhas < 0) return tomhas;
        for (int INDEX = 0; INDEX < fad_VALUE; INDEX++) traschur_sonraí[INDEX] = gléas_VALUE.기억읽기(sonraí_ADDRESS + INDEX);
        return Líonra_Cruach.seol(Líonra_hanla[기술], ADDRESS_32(ADDRESS + 4), uimhir_phoirt, traschur_sonraí, fad_VALUE);
    }
    static void scríobh_ADDRESS(int ADDRESS, int fad_VALUE, int Líonra_ADDRESS, int uimhir_phoirt) {
        for (int INDEX = 0; INDEX < fad_VALUE && INDEX < 16; INDEX++) {
            int VALUE = 0;
            if (INDEX == 0) VALUE = 2;
            if (INDEX == 2) VALUE = uimhir_phoirt >>> 8;
            if (INDEX == 3) VALUE = uimhir_phoirt;
            if (INDEX >= 4 && INDEX < 8) VALUE = Líonra_ADDRESS >>> (56 - INDEX * 8);
            gléas_VALUE.scríobh_Cuimhne(ADDRESS + INDEX, VALUE & 255);
        }
    }
    static int 자료전문받기(int 서술자, int sonraí_ADDRESS, int fad_VALUE, int Socruithe, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Socruithe & ~64) != 0) return -95;
        if (fad_VALUE < 0) return -22;
        if (fad_VALUE != 0 && !실행관리.gearrthóg(sonraí_ADDRESS, fad_VALUE)) return -14;
        int ADDRESS = 0, ADDRESS_fad_ADDRESS = 0, ADDRESS_fad = 0;
        if (요청주소 != 0) {
            if (!실행관리.gearrthóg(요청주소, 8)) return -14;
            ADDRESS = 실행관리.수(요청주소); ADDRESS_fad_ADDRESS = 실행관리.수(요청주소 + 4);
            if (ADDRESS != 0) {
                if (!실행관리.gearrthóg(ADDRESS_fad_ADDRESS, 4)) return -14;
                ADDRESS_fad = 실행관리.수(ADDRESS_fad_ADDRESS);
                if (ADDRESS_fad < 0) return -22;
                if (!실행관리.gearrthóg(ADDRESS, ADDRESS_fad < 16 ? ADDRESS_fad : 16)) return -14;
            }
        }
        int tomhas = 자동묶기(기술);
        if (tomhas < 0) return tomhas;
        int Rith_2 = gléas_VALUE.밀리초();
        while (true) {
            tomhas = Líonra_Cruach.받기(Líonra_hanla[기술], traschur_sonraí, 1024, 0);
            if (tomhas != -11) break;
            if ((Socruithe & 64) != 0 || (oscail_Socruithe[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && gléas_VALUE.밀리초() - Rith_2 >= 수신대기밀리초[기술]) return -11;
            if (gléas_VALUE.사용자남은밀리초() <= 10) return -11;
            gléas_VALUE.잠시양보();
        }
        if (tomhas < 0) return tomhas;
        if (tomhas > fad_VALUE) tomhas = fad_VALUE;
        for (int INDEX = 0; INDEX < tomhas; INDEX++) gléas_VALUE.scríobh_Cuimhne(sonraí_ADDRESS + INDEX, traschur_sonraí[INDEX]);
        if (ADDRESS != 0) {
            scríobh_ADDRESS(ADDRESS, ADDRESS_fad, Líonra_Cruach.piara_ADDRESS(Líonra_hanla[기술]), Líonra_Cruach.piara_uimhir_phoirt(Líonra_hanla[기술]));
            실행관리.수쓰기(ADDRESS_fad_ADDRESS, 16);
        }
        return tomhas;
    }
    static int 통신주소읽기(int 서술자, int ADDRESS, int fad_ADDRESS) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.gearrthóg(fad_ADDRESS, 4)) return -14;
        int fad_VALUE = 실행관리.수(fad_ADDRESS);
        if (fad_VALUE < 0) return -22;
        if (!실행관리.gearrthóg(ADDRESS, fad_VALUE < 16 ? fad_VALUE : 16)) return -14;
        int spás_iontráil = Líonra_Cruach.INDEX(Líonra_hanla[기술]);
        scríobh_ADDRESS(ADDRESS, fad_VALUE, sprioc[기술], spás_iontráil < 0 ? 0 : Líonra_Cruach.접속번호들[spás_iontráil]);
        실행관리.수쓰기(fad_ADDRESS, 16);
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
