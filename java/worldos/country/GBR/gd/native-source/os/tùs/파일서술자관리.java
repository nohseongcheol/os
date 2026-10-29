// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 cleachdaiche 과정의 파일서술자와 열린 faidhle 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int so_leughte_so_sgrìobhte_bratach = 2, Create_cur_a_steach = 64, 독점생성 = 128, glan_susbaint = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] fosgail_làmhrachan = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], targaid = new int[서술자한도];
    static int[] faidhle_suidhich = new int[서술자한도], fosgail_roghainnean = new int[서술자한도], fiosrachadh_COUNT = new int[서술자한도];
    static int[] lìonra_làmhrachan = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] slighe_ainm = new int[64], tar_chur_dàta = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return fosgail_làmhrachan[파일서술자] - 1;
    }
    static int 빈서술자(int ruith) {
        for (int INDEX = ruith; INDEX < 서술자한도; INDEX++) if (fosgail_làmhrachan[INDEX] == 0) return INDEX;
        return -24;
    }
    static int falamh_làmhrachan() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (fiosrachadh_COUNT[INDEX] == 0) return INDEX;
        return -24;
    }
    static int CONNECT(int 서술자, int 기술, int 파일종류, int faidhle_targaid, int roghainnean) {
        fosgail_làmhrachan[서술자] = 기술 + 1; 서술자설정[서술자] = (roghainnean & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; targaid[기술] = faidhle_targaid; fiosrachadh_COUNT[기술] = 1;
        fosgail_roghainnean[기술] = roghainnean & (3 | 이어쓰기 | 기다리지않기); faidhle_suidhich[기술] = 0;
        lìonra_làmhrachan[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void Start_Pròiseas() {
        CLEAN_Pròiseas();
        for (int INDEX = 0; INDEX < 3; INDEX++) CONNECT(INDEX, INDEX, 1, INDEX, INDEX == 0 ? 0 : 1);
    }
    static void CLEAN_Pròiseas() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (fosgail_làmhrachan[INDEX] != 0) dùin_faidhle(INDEX);
    }
    static int dùin_faidhle(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        fosgail_làmhrachan[서술자] = 0; 서술자설정[서술자] = 0;
        fiosrachadh_COUNT[기술]--;
        if (fiosrachadh_COUNT[기술] == 0) {
            if (종류[기술] == 2) cuimhne_siostam_fhaidhlichean.fosgail_COUNT[targaid[기술]]--;
            if (종류[기술] == 3 && lìonra_làmhrachan[기술] != 0) lìonra_stac.dùin(lìonra_làmhrachan[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 baidht_VALUE 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int ADDRESS) {
        if (!실행관리.cliop(ADDRESS, 1)) return -14;
        int suidhich = uidheam_VALUE.기억읽기(ADDRESS) == '/' ? 1 : 0;
        for (int faid_VALUE = 0; faid_VALUE < 64; faid_VALUE++) {
            if (!실행관리.cliop(ADDRESS + suidhich + faid_VALUE, 1)) return -14;
            int VALUE = uidheam_VALUE.기억읽기(ADDRESS + suidhich + faid_VALUE);
            slighe_ainm[faid_VALUE] = VALUE;
            if (VALUE == 0) return faid_VALUE == 0 ? -2 : (cuimhne_siostam_fhaidhlichean.seic_ainm(slighe_ainm, faid_VALUE) ? faid_VALUE : -22);
            if (VALUE == '/') return -20;
        }
        return -36;
    }
    static int fosgail_faidhle(int ainm_ADDRESS, int roghainnean, int 허가) {
        int faid_VALUE = 경로읽기(ainm_ADDRESS);
        if (faid_VALUE < 0) return faid_VALUE;
        if ((roghainnean & ~(3 | Create_cur_a_steach | 독점생성 | glan_susbaint | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((roghainnean & 3) == 3 || ((roghainnean & glan_susbaint) != 0 && (roghainnean & 3) == 0)) return -22;
        int faidhle = cuimhne_siostam_fhaidhlichean.FIND_cur_a_steach(slighe_ainm, faid_VALUE);
        if (faidhle >= 0 && (roghainnean & (Create_cur_a_steach | 독점생성)) == (Create_cur_a_steach | 독점생성)) return -17;
        if (faidhle == -2 && (roghainnean & Create_cur_a_steach) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = falamh_làmhrachan();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (faidhle == -2) {
            int tomhas = cuimhne_siostam_fhaidhlichean.Store_VALUE(slighe_ainm, faid_VALUE, slighe_ainm, 0);
            if (tomhas < 0) return tomhas;
            faidhle = cuimhne_siostam_fhaidhlichean.FIND_cur_a_steach(slighe_ainm, faid_VALUE);
            cuimhne_siostam_fhaidhlichean.허가들[faidhle] = 허가 & 511;
        }
        if (faidhle < 0) return faidhle;
        if ((roghainnean & glan_susbaint) != 0) cuimhne_siostam_fhaidhlichean.atharraich_am_meud_Liosta[faidhle] = 0;
        cuimhne_siostam_fhaidhlichean.fosgail_COUNT[faidhle]++;
        return CONNECT(서술자, 기술, 2, faidhle, roghainnean);
    }
    static int 파일읽기(int 서술자, int dàta_ADDRESS, int faid_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (fosgail_roghainnean[기술] & 3) == 1) return -9;
        if (faid_VALUE < 0) return -22;
        if (faid_VALUE == 0) return 0;
        if (!실행관리.cliop(dàta_ADDRESS, faid_VALUE)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, dàta_ADDRESS, faid_VALUE, 0, 0);
        if (종류[기술] == 1) {
            int RECEIVED_COUNT = 0;
            while (RECEIVED_COUNT < faid_VALUE) {
                int VALUE = SMS_tèirmineal.직렬읽기();
                if (VALUE < 0) VALUE = meur_chlàr.읽기();
                if (VALUE < 0) {
                    if (RECEIVED_COUNT > 0) return RECEIVED_COUNT;
                    if ((fosgail_roghainnean[기술] & 기다리지않기) != 0) return -11;
                    if (uidheam_VALUE.사용자남은밀리초() <= 10) return -11;
                    lìonra_stac.dearbh(); uidheam_VALUE.잠시양보();
                } else {
                    uidheam_VALUE.sgrìobh_cuimhne(dàta_ADDRESS + RECEIVED_COUNT, VALUE); RECEIVED_COUNT++;
                }
            }
            return RECEIVED_COUNT;
        }
        int faidhle = targaid[기술], suidhich = faidhle_suidhich[기술];
        if (suidhich >= cuimhne_siostam_fhaidhlichean.atharraich_am_meud_Liosta[faidhle]) return 0;
        if (faid_VALUE > cuimhne_siostam_fhaidhlichean.atharraich_am_meud_Liosta[faidhle] - suidhich) faid_VALUE = cuimhne_siostam_fhaidhlichean.atharraich_am_meud_Liosta[faidhle] - suidhich;
        int 원본주소 = uidheam_VALUE.faidhle_cuimhne() + faidhle * cuimhne_siostam_fhaidhlichean.최대크기 + suidhich;
        for (int INDEX = 0; INDEX < faid_VALUE; INDEX++) uidheam_VALUE.sgrìobh_cuimhne(dàta_ADDRESS + INDEX, uidheam_VALUE.기억읽기(원본주소 + INDEX));
        faidhle_suidhich[기술] += faid_VALUE;
        return faid_VALUE;
    }
    static int sgrìobh_faidhle(int 서술자, int dàta_ADDRESS, int faid_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (fosgail_roghainnean[기술] & 3) == 0) return -9;
        if (faid_VALUE < 0) return -22;
        if (faid_VALUE == 0) return 0;
        if (!실행관리.cliop(dàta_ADDRESS, faid_VALUE)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 ceann_uidhe_VALUE 주소가 필요하다.
        if (종류[기술] == 1) {
            if (faid_VALUE > 16384) faid_VALUE = 16384;
            for (int INDEX = 0; INDEX < faid_VALUE; INDEX++) {
                int VALUE = uidheam_VALUE.기억읽기(dàta_ADDRESS + INDEX);
                SMS_tèirmineal.직렬바이트(VALUE); SMS_tèirmineal.화면문자(VALUE);
            }
            return faid_VALUE;
        }
        int faidhle = targaid[기술], atharraich_am_meud = cuimhne_siostam_fhaidhlichean.atharraich_am_meud_Liosta[faidhle];
        int suidhich = (fosgail_roghainnean[기술] & 이어쓰기) != 0 ? atharraich_am_meud : faidhle_suidhich[기술];
        if (suidhich >= cuimhne_siostam_fhaidhlichean.최대크기) return -27;
        if (faid_VALUE > cuimhne_siostam_fhaidhlichean.최대크기 - suidhich) faid_VALUE = cuimhne_siostam_fhaidhlichean.최대크기 - suidhich;
        int ceann_uidhe_ADDRESS = uidheam_VALUE.faidhle_cuimhne() + faidhle * cuimhne_siostam_fhaidhlichean.최대크기;
        for (int INDEX = atharraich_am_meud; INDEX < suidhich; INDEX++) uidheam_VALUE.sgrìobh_cuimhne(ceann_uidhe_ADDRESS + INDEX, 0);
        for (int INDEX = 0; INDEX < faid_VALUE; INDEX++) uidheam_VALUE.sgrìobh_cuimhne(ceann_uidhe_ADDRESS + suidhich + INDEX, uidheam_VALUE.기억읽기(dàta_ADDRESS + INDEX));
        faidhle_suidhich[기술] = suidhich + faid_VALUE;
        if (suidhich + faid_VALUE > atharraich_am_meud) cuimhne_siostam_fhaidhlichean.atharraich_am_meud_Liosta[faidhle] = suidhich + faid_VALUE;
        return faid_VALUE;
    }
    static int sir_faidhle(int 서술자, int OFFSET_VALUE, int tilg_freumh) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (tilg_freumh < 0 || tilg_freumh > 2) return -22;
        int cùlaibh_VALUE = tilg_freumh == 0 ? 0 : (tilg_freumh == 1 ? faidhle_suidhich[기술] : cuimhne_siostam_fhaidhlichean.atharraich_am_meud_Liosta[targaid[기술]]);
        if (OFFSET_VALUE > 0 && cùlaibh_VALUE > 2147483647 - OFFSET_VALUE) return -75;
        if (OFFSET_VALUE < 0 && OFFSET_VALUE < -cùlaibh_VALUE) return -22;
        faidhle_suidhich[기술] = cùlaibh_VALUE + OFFSET_VALUE;
        return faidhle_suidhich[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean 지정, int roghainnean) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return 지정 ? -9 : -22;
        if (지정 && 서술자 == 새서술자) return 새서술자;
        if (지정) { if (fosgail_làmhrachan[새서술자] != 0) dùin_faidhle(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        fosgail_làmhrachan[새서술자] = 기술 + 1; 서술자설정[새서술자] = roghainnean; fiosrachadh_COUNT[기술]++;
        return 새서술자;
    }
    static int thoir_air_falbh_faidhle_cur_a_steach_ainm(int ainm_ADDRESS) {
        int faid_VALUE = 경로읽기(ainm_ADDRESS);
        if (faid_VALUE < 0) return faid_VALUE;
        int faidhle = cuimhne_siostam_fhaidhlichean.FIND_cur_a_steach(slighe_ainm, faid_VALUE);
        if (faidhle < 0) return faidhle;
        cuimhne_siostam_fhaidhlichean.이름들[faidhle * 64] = 0;
        return 0;
    }
    static int seata_faidhle_faid(int 서술자, int faid_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (fosgail_roghainnean[기술] & 3) == 0 || faid_VALUE < 0) return -22;
        if (faid_VALUE > cuimhne_siostam_fhaidhlichean.최대크기) return -27;
        int faidhle = targaid[기술], ADDRESS = uidheam_VALUE.faidhle_cuimhne() + faidhle * cuimhne_siostam_fhaidhlichean.최대크기;
        for (int INDEX = cuimhne_siostam_fhaidhlichean.atharraich_am_meud_Liosta[faidhle]; INDEX < faid_VALUE; INDEX++) uidheam_VALUE.sgrìobh_cuimhne(ADDRESS + INDEX, 0);
        cuimhne_siostam_fhaidhlichean.atharraich_am_meud_Liosta[faidhle] = faid_VALUE;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int ADDRESS) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.cliop(ADDRESS, 48)) return -14;
        for (int INDEX = 0; INDEX < 12; INDEX++) 실행관리.수쓰기(ADDRESS + INDEX * 4, 0);
        int faidhle = targaid[기술], atharraich_am_meud = 종류[기술] == 2 ? cuimhne_siostam_fhaidhlichean.atharraich_am_meud_Liosta[faidhle] : 0;
        int 허가 = 종류[기술] == 2 ? cuimhne_siostam_fhaidhlichean.허가들[faidhle] : 438;
        실행관리.수쓰기(ADDRESS, 1);
        실행관리.수쓰기(ADDRESS + 4, 종류[기술] == 2 ? faidhle + 1 : 100 + 기술);
        실행관리.수쓰기(ADDRESS + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(ADDRESS + 12, 종류[기술] == 2 && cuimhne_siostam_fhaidhlichean.이름들[faidhle * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(ADDRESS + 28, atharraich_am_meud); 실행관리.수쓰기(ADDRESS + 32, 512);
        실행관리.수쓰기(ADDRESS + 36, (atharraich_am_meud + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int àithne, int VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (àithne == 0 || àithne == 1030) return 서술자복제(서술자, VALUE, false, àithne == 1030 ? 1 : 0);
        if (àithne == 1) return 서술자설정[서술자];
        if (àithne == 2) { if ((VALUE & ~1) != 0) return -22; 서술자설정[서술자] = VALUE; return 0; }
        if (àithne == 3) return fosgail_roghainnean[기술];
        if (àithne == 4) {
            if ((VALUE & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            fosgail_roghainnean[기술] = (fosgail_roghainnean[기술] & 3) | (VALUE & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int 통신종단점만들기(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = falamh_làmhrachan();
        if (서술자 < 0 || 기술 < 0) return -24;
        return CONNECT(서술자, 기술, 3, 0, so_leughte_so_sgrìobhte_bratach);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int ADDRESS_32(int ADDRESS) {
        return uidheam_VALUE.기억읽기(ADDRESS) << 24 | uidheam_VALUE.기억읽기(ADDRESS + 1) << 16
            | uidheam_VALUE.기억읽기(ADDRESS + 2) << 8 | uidheam_VALUE.기억읽기(ADDRESS + 3);
    }
    static int seic_ADDRESS(int ADDRESS, int faid_VALUE) {
        if (faid_VALUE < 16) return -22;
        if (!실행관리.cliop(ADDRESS, 16)) return -14;
        return 실행관리.짧은수(ADDRESS) == 2 ? 0 : -97;
    }
    static int BIND_ADDRESS(int 서술자, int ADDRESS, int faid_VALUE) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int tomhas = seic_ADDRESS(ADDRESS, faid_VALUE);
        if (tomhas < 0) return tomhas;
        if (lìonra_làmhrachan[기술] != 0) return -22;
        int lìonra_ADDRESS = ADDRESS_32(ADDRESS + 4);
        if (lìonra_ADDRESS != 0 && lìonra_ADDRESS != lìonra_stac.내주소) return -99;
        int 접속번호 = uidheam_VALUE.기억읽기(ADDRESS + 2) << 8 | uidheam_VALUE.기억읽기(ADDRESS + 3);
        tomhas = lìonra_stac.fosgail(접속번호);
        if (tomhas < 0) return tomhas;
        lìonra_làmhrachan[기술] = tomhas; targaid[기술] = lìonra_ADDRESS;
        return 0;
    }
    static int 자동묶기(int 기술) {
        if (lìonra_làmhrachan[기술] != 0) return 0;
        int tomhas = lìonra_stac.fosgail(0);
        if (tomhas < 0) return tomhas;
        lìonra_làmhrachan[기술] = tomhas;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 요청 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int dàta_ADDRESS, int faid_VALUE, int roghainnean, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (roghainnean != 0) return -95;
        if (faid_VALUE < 0 || faid_VALUE > 1024) return -90;
        if (faid_VALUE != 0 && !실행관리.cliop(dàta_ADDRESS, faid_VALUE)) return -14;
        if (!실행관리.cliop(요청주소, 8)) return -14;
        int ADDRESS = 실행관리.수(요청주소);
        int tomhas = seic_ADDRESS(ADDRESS, 실행관리.수(요청주소 + 4));
        if (tomhas < 0) return tomhas;
        int 접속번호 = uidheam_VALUE.기억읽기(ADDRESS + 2) << 8 | uidheam_VALUE.기억읽기(ADDRESS + 3);
        if (접속번호 == 0) return -22;
        tomhas = 자동묶기(기술);
        if (tomhas < 0) return tomhas;
        for (int INDEX = 0; INDEX < faid_VALUE; INDEX++) tar_chur_dàta[INDEX] = uidheam_VALUE.기억읽기(dàta_ADDRESS + INDEX);
        return lìonra_stac.cuir(lìonra_làmhrachan[기술], ADDRESS_32(ADDRESS + 4), 접속번호, tar_chur_dàta, faid_VALUE);
    }
    static void sgrìobh_ADDRESS(int ADDRESS, int faid_VALUE, int lìonra_ADDRESS, int 접속번호) {
        for (int INDEX = 0; INDEX < faid_VALUE && INDEX < 16; INDEX++) {
            int VALUE = 0;
            if (INDEX == 0) VALUE = 2;
            if (INDEX == 2) VALUE = 접속번호 >>> 8;
            if (INDEX == 3) VALUE = 접속번호;
            if (INDEX >= 4 && INDEX < 8) VALUE = lìonra_ADDRESS >>> (56 - INDEX * 8);
            uidheam_VALUE.sgrìobh_cuimhne(ADDRESS + INDEX, VALUE & 255);
        }
    }
    static int 자료전문받기(int 서술자, int dàta_ADDRESS, int faid_VALUE, int roghainnean, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((roghainnean & ~64) != 0) return -95;
        if (faid_VALUE < 0) return -22;
        if (faid_VALUE != 0 && !실행관리.cliop(dàta_ADDRESS, faid_VALUE)) return -14;
        int ADDRESS = 0, ADDRESS_faid_ADDRESS = 0, ADDRESS_faid = 0;
        if (요청주소 != 0) {
            if (!실행관리.cliop(요청주소, 8)) return -14;
            ADDRESS = 실행관리.수(요청주소); ADDRESS_faid_ADDRESS = 실행관리.수(요청주소 + 4);
            if (ADDRESS != 0) {
                if (!실행관리.cliop(ADDRESS_faid_ADDRESS, 4)) return -14;
                ADDRESS_faid = 실행관리.수(ADDRESS_faid_ADDRESS);
                if (ADDRESS_faid < 0) return -22;
                if (!실행관리.cliop(ADDRESS, ADDRESS_faid < 16 ? ADDRESS_faid : 16)) return -14;
            }
        }
        int tomhas = 자동묶기(기술);
        if (tomhas < 0) return tomhas;
        int ruith = uidheam_VALUE.밀리초();
        while (true) {
            tomhas = lìonra_stac.받기(lìonra_làmhrachan[기술], tar_chur_dàta, 1024, 0);
            if (tomhas != -11) break;
            if ((roghainnean & 64) != 0 || (fosgail_roghainnean[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && uidheam_VALUE.밀리초() - ruith >= 수신대기밀리초[기술]) return -11;
            if (uidheam_VALUE.사용자남은밀리초() <= 10) return -11;
            uidheam_VALUE.잠시양보();
        }
        if (tomhas < 0) return tomhas;
        if (tomhas > faid_VALUE) tomhas = faid_VALUE;
        for (int INDEX = 0; INDEX < tomhas; INDEX++) uidheam_VALUE.sgrìobh_cuimhne(dàta_ADDRESS + INDEX, tar_chur_dàta[INDEX]);
        if (ADDRESS != 0) {
            sgrìobh_ADDRESS(ADDRESS, ADDRESS_faid, lìonra_stac.seise_ADDRESS(lìonra_làmhrachan[기술]), lìonra_stac.상대접속번호(lìonra_làmhrachan[기술]));
            실행관리.수쓰기(ADDRESS_faid_ADDRESS, 16);
        }
        return tomhas;
    }
    static int 통신주소읽기(int 서술자, int ADDRESS, int faid_ADDRESS) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.cliop(faid_ADDRESS, 4)) return -14;
        int faid_VALUE = 실행관리.수(faid_ADDRESS);
        if (faid_VALUE < 0) return -22;
        if (!실행관리.cliop(ADDRESS, faid_VALUE < 16 ? faid_VALUE : 16)) return -14;
        int slot_cur_a_steach = lìonra_stac.INDEX(lìonra_làmhrachan[기술]);
        sgrìobh_ADDRESS(ADDRESS, faid_VALUE, targaid[기술], slot_cur_a_steach < 0 ? 0 : lìonra_stac.접속번호들[slot_cur_a_steach]);
        실행관리.수쓰기(faid_ADDRESS, 16);
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
