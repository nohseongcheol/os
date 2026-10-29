// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 utent 과정의 파일서술자와 열린 fajl 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int qari_kitba_mmarka = 2, ħalaq_entrata = 64, 독점생성 = 128, neħħa_TOC = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] fetaħ_handle = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], mira = new int[서술자한도];
    static int[] fajl_pożizzjoni = new int[서술자한도], fetaħ_Settings = new int[서술자한도], Referenza_COUNT = new int[서술자한도];
    static int[] netwerk_handle = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] mogħdija_isem = new int[64], trasferiment_data = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return fetaħ_handle[파일서술자] - 1;
    }
    static int 빈서술자(int serje) {
        for (int INDEX = serje; INDEX < 서술자한도; INDEX++) if (fetaħ_handle[INDEX] == 0) return INDEX;
        return -24;
    }
    static int vojt_handle() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (Referenza_COUNT[INDEX] == 0) return INDEX;
        return -24;
    }
    static int AQBAD(int 서술자, int 기술, int 파일종류, int fajl_mira, int Settings) {
        fetaħ_handle[서술자] = 기술 + 1; 서술자설정[서술자] = (Settings & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; mira[기술] = fajl_mira; Referenza_COUNT[기술] = 1;
        fetaħ_Settings[기술] = Settings & (3 | 이어쓰기 | 기다리지않기); fajl_pożizzjoni[기술] = 0;
        netwerk_handle[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void Bidu_Proċess() {
        CLEAN_Proċess();
        for (int INDEX = 0; INDEX < 3; INDEX++) AQBAD(INDEX, INDEX, 1, INDEX, INDEX == 0 ? 0 : 1);
    }
    static void CLEAN_Proċess() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (fetaħ_handle[INDEX] != 0) agħlaq_fajl(INDEX);
    }
    static int agħlaq_fajl(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        fetaħ_handle[서술자] = 0; 서술자설정[서술자] = 0;
        Referenza_COUNT[기술]--;
        if (Referenza_COUNT[기술] == 0) {
            if (종류[기술] == 2) Memorja_sistema_tal_fajls.fetaħ_COUNT[mira[기술]]--;
            if (종류[기술] == 3 && netwerk_handle[기술] != 0) netwerk_Munzell.agħlaq(netwerk_handle[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 byte_VALUE 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int ADDRESS) {
        if (!실행관리.klipp(ADDRESS, 1)) return -14;
        int pożizzjoni = mowbajl_VALUE.기억읽기(ADDRESS) == '/' ? 1 : 0;
        for (int tul_VALUE = 0; tul_VALUE < 64; tul_VALUE++) {
            if (!실행관리.klipp(ADDRESS + pożizzjoni + tul_VALUE, 1)) return -14;
            int VALUE = mowbajl_VALUE.기억읽기(ADDRESS + pożizzjoni + tul_VALUE);
            mogħdija_isem[tul_VALUE] = VALUE;
            if (VALUE == 0) return tul_VALUE == 0 ? -2 : (Memorja_sistema_tal_fajls.ċekk_isem(mogħdija_isem, tul_VALUE) ? tul_VALUE : -22);
            if (VALUE == '/') return -20;
        }
        return -36;
    }
    static int fetaħ_fajl(int isem_ADDRESS, int Settings, int 허가) {
        int tul_VALUE = 경로읽기(isem_ADDRESS);
        if (tul_VALUE < 0) return tul_VALUE;
        if ((Settings & ~(3 | ħalaq_entrata | 독점생성 | neħħa_TOC | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Settings & 3) == 3 || ((Settings & neħħa_TOC) != 0 && (Settings & 3) == 0)) return -22;
        int fajl = Memorja_sistema_tal_fajls.sab_entrata(mogħdija_isem, tul_VALUE);
        if (fajl >= 0 && (Settings & (ħalaq_entrata | 독점생성)) == (ħalaq_entrata | 독점생성)) return -17;
        if (fajl == -2 && (Settings & ħalaq_entrata) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = vojt_handle();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (fajl == -2) {
            int miżura = Memorja_sistema_tal_fajls.Store_VALUE(mogħdija_isem, tul_VALUE, mogħdija_isem, 0);
            if (miżura < 0) return miżura;
            fajl = Memorja_sistema_tal_fajls.sab_entrata(mogħdija_isem, tul_VALUE);
            Memorja_sistema_tal_fajls.허가들[fajl] = 허가 & 511;
        }
        if (fajl < 0) return fajl;
        if ((Settings & neħħa_TOC) != 0) Memorja_sistema_tal_fajls.daqqas_Lista[fajl] = 0;
        Memorja_sistema_tal_fajls.fetaħ_COUNT[fajl]++;
        return AQBAD(서술자, 기술, 2, fajl, Settings);
    }
    static int 파일읽기(int 서술자, int data_ADDRESS, int tul_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (fetaħ_Settings[기술] & 3) == 1) return -9;
        if (tul_VALUE < 0) return -22;
        if (tul_VALUE == 0) return 0;
        if (!실행관리.klipp(data_ADDRESS, tul_VALUE)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, data_ADDRESS, tul_VALUE, 0, 0);
        if (종류[기술] == 1) {
            int RECEIVED_COUNT = 0;
            while (RECEIVED_COUNT < tul_VALUE) {
                int VALUE = SMS_Terminal.직렬읽기();
                if (VALUE < 0) VALUE = tastiera.읽기();
                if (VALUE < 0) {
                    if (RECEIVED_COUNT > 0) return RECEIVED_COUNT;
                    if ((fetaħ_Settings[기술] & 기다리지않기) != 0) return -11;
                    if (mowbajl_VALUE.사용자남은밀리초() <= 10) return -11;
                    netwerk_Munzell.vverifika(); mowbajl_VALUE.잠시양보();
                } else {
                    mowbajl_VALUE.kiteb_Memorja(data_ADDRESS + RECEIVED_COUNT, VALUE); RECEIVED_COUNT++;
                }
            }
            return RECEIVED_COUNT;
        }
        int fajl = mira[기술], pożizzjoni = fajl_pożizzjoni[기술];
        if (pożizzjoni >= Memorja_sistema_tal_fajls.daqqas_Lista[fajl]) return 0;
        if (tul_VALUE > Memorja_sistema_tal_fajls.daqqas_Lista[fajl] - pożizzjoni) tul_VALUE = Memorja_sistema_tal_fajls.daqqas_Lista[fajl] - pożizzjoni;
        int 원본주소 = mowbajl_VALUE.fajl_Memorja() + fajl * Memorja_sistema_tal_fajls.최대크기 + pożizzjoni;
        for (int INDEX = 0; INDEX < tul_VALUE; INDEX++) mowbajl_VALUE.kiteb_Memorja(data_ADDRESS + INDEX, mowbajl_VALUE.기억읽기(원본주소 + INDEX));
        fajl_pożizzjoni[기술] += tul_VALUE;
        return tul_VALUE;
    }
    static int kiteb_fajl(int 서술자, int data_ADDRESS, int tul_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (fetaħ_Settings[기술] & 3) == 0) return -9;
        if (tul_VALUE < 0) return -22;
        if (tul_VALUE == 0) return 0;
        if (!실행관리.klipp(data_ADDRESS, tul_VALUE)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 destinazzjoni_VALUE 주소가 필요하다.
        if (종류[기술] == 1) {
            if (tul_VALUE > 16384) tul_VALUE = 16384;
            for (int INDEX = 0; INDEX < tul_VALUE; INDEX++) {
                int VALUE = mowbajl_VALUE.기억읽기(data_ADDRESS + INDEX);
                SMS_Terminal.직렬바이트(VALUE); SMS_Terminal.화면문자(VALUE);
            }
            return tul_VALUE;
        }
        int fajl = mira[기술], daqqas = Memorja_sistema_tal_fajls.daqqas_Lista[fajl];
        int pożizzjoni = (fetaħ_Settings[기술] & 이어쓰기) != 0 ? daqqas : fajl_pożizzjoni[기술];
        if (pożizzjoni >= Memorja_sistema_tal_fajls.최대크기) return -27;
        if (tul_VALUE > Memorja_sistema_tal_fajls.최대크기 - pożizzjoni) tul_VALUE = Memorja_sistema_tal_fajls.최대크기 - pożizzjoni;
        int destinazzjoni_ADDRESS = mowbajl_VALUE.fajl_Memorja() + fajl * Memorja_sistema_tal_fajls.최대크기;
        for (int INDEX = daqqas; INDEX < pożizzjoni; INDEX++) mowbajl_VALUE.kiteb_Memorja(destinazzjoni_ADDRESS + INDEX, 0);
        for (int INDEX = 0; INDEX < tul_VALUE; INDEX++) mowbajl_VALUE.kiteb_Memorja(destinazzjoni_ADDRESS + pożizzjoni + INDEX, mowbajl_VALUE.기억읽기(data_ADDRESS + INDEX));
        fajl_pożizzjoni[기술] = pożizzjoni + tul_VALUE;
        if (pożizzjoni + tul_VALUE > daqqas) Memorja_sistema_tal_fajls.daqqas_Lista[fajl] = pożizzjoni + tul_VALUE;
        return tul_VALUE;
    }
    static int fittex_fajl(int 서술자, int OFFSET_VALUE, int pprojetta_għerq) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (pprojetta_għerq < 0 || pprojetta_għerq > 2) return -22;
        int Sfond_VALUE = pprojetta_għerq == 0 ? 0 : (pprojetta_għerq == 1 ? fajl_pożizzjoni[기술] : Memorja_sistema_tal_fajls.daqqas_Lista[mira[기술]]);
        if (OFFSET_VALUE > 0 && Sfond_VALUE > 2147483647 - OFFSET_VALUE) return -75;
        if (OFFSET_VALUE < 0 && OFFSET_VALUE < -Sfond_VALUE) return -22;
        fajl_pożizzjoni[기술] = Sfond_VALUE + OFFSET_VALUE;
        return fajl_pożizzjoni[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean assenja_VALUE, int Settings) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return assenja_VALUE ? -9 : -22;
        if (assenja_VALUE && 서술자 == 새서술자) return 새서술자;
        if (assenja_VALUE) { if (fetaħ_handle[새서술자] != 0) agħlaq_fajl(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        fetaħ_handle[새서술자] = 기술 + 1; 서술자설정[새서술자] = Settings; Referenza_COUNT[기술]++;
        return 새서술자;
    }
    static int neħħa_fajl_entrata_isem(int isem_ADDRESS) {
        int tul_VALUE = 경로읽기(isem_ADDRESS);
        if (tul_VALUE < 0) return tul_VALUE;
        int fajl = Memorja_sistema_tal_fajls.sab_entrata(mogħdija_isem, tul_VALUE);
        if (fajl < 0) return fajl;
        Memorja_sistema_tal_fajls.이름들[fajl * 64] = 0;
        return 0;
    }
    static int sett_fajl_tul(int 서술자, int tul_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (fetaħ_Settings[기술] & 3) == 0 || tul_VALUE < 0) return -22;
        if (tul_VALUE > Memorja_sistema_tal_fajls.최대크기) return -27;
        int fajl = mira[기술], ADDRESS = mowbajl_VALUE.fajl_Memorja() + fajl * Memorja_sistema_tal_fajls.최대크기;
        for (int INDEX = Memorja_sistema_tal_fajls.daqqas_Lista[fajl]; INDEX < tul_VALUE; INDEX++) mowbajl_VALUE.kiteb_Memorja(ADDRESS + INDEX, 0);
        Memorja_sistema_tal_fajls.daqqas_Lista[fajl] = tul_VALUE;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int ADDRESS) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.klipp(ADDRESS, 48)) return -14;
        for (int INDEX = 0; INDEX < 12; INDEX++) 실행관리.수쓰기(ADDRESS + INDEX * 4, 0);
        int fajl = mira[기술], daqqas = 종류[기술] == 2 ? Memorja_sistema_tal_fajls.daqqas_Lista[fajl] : 0;
        int 허가 = 종류[기술] == 2 ? Memorja_sistema_tal_fajls.허가들[fajl] : 438;
        실행관리.수쓰기(ADDRESS, 1);
        실행관리.수쓰기(ADDRESS + 4, 종류[기술] == 2 ? fajl + 1 : 100 + 기술);
        실행관리.수쓰기(ADDRESS + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(ADDRESS + 12, 종류[기술] == 2 && Memorja_sistema_tal_fajls.이름들[fajl * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(ADDRESS + 28, daqqas); 실행관리.수쓰기(ADDRESS + 32, 512);
        실행관리.수쓰기(ADDRESS + 36, (daqqas + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int kmand, int VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (kmand == 0 || kmand == 1030) return 서술자복제(서술자, VALUE, false, kmand == 1030 ? 1 : 0);
        if (kmand == 1) return 서술자설정[서술자];
        if (kmand == 2) { if ((VALUE & ~1) != 0) return -22; 서술자설정[서술자] = VALUE; return 0; }
        if (kmand == 3) return fetaħ_Settings[기술];
        if (kmand == 4) {
            if ((VALUE & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            fetaħ_Settings[기술] = (fetaħ_Settings[기술] & 3) | (VALUE & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int 통신종단점만들기(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = vojt_handle();
        if (서술자 < 0 || 기술 < 0) return -24;
        return AQBAD(서술자, 기술, 3, 0, qari_kitba_mmarka);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int ADDRESS_32(int ADDRESS) {
        return mowbajl_VALUE.기억읽기(ADDRESS) << 24 | mowbajl_VALUE.기억읽기(ADDRESS + 1) << 16
            | mowbajl_VALUE.기억읽기(ADDRESS + 2) << 8 | mowbajl_VALUE.기억읽기(ADDRESS + 3);
    }
    static int ċekk_ADDRESS(int ADDRESS, int tul_VALUE) {
        if (tul_VALUE < 16) return -22;
        if (!실행관리.klipp(ADDRESS, 16)) return -14;
        return 실행관리.짧은수(ADDRESS) == 2 ? 0 : -97;
    }
    static int BIND_ADDRESS(int 서술자, int ADDRESS, int tul_VALUE) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int miżura = ċekk_ADDRESS(ADDRESS, tul_VALUE);
        if (miżura < 0) return miżura;
        if (netwerk_handle[기술] != 0) return -22;
        int netwerk_ADDRESS = ADDRESS_32(ADDRESS + 4);
        if (netwerk_ADDRESS != 0 && netwerk_ADDRESS != netwerk_Munzell.내주소) return -99;
        int 접속번호 = mowbajl_VALUE.기억읽기(ADDRESS + 2) << 8 | mowbajl_VALUE.기억읽기(ADDRESS + 3);
        miżura = netwerk_Munzell.fetaħ(접속번호);
        if (miżura < 0) return miżura;
        netwerk_handle[기술] = miżura; mira[기술] = netwerk_ADDRESS;
        return 0;
    }
    static int 자동묶기(int 기술) {
        if (netwerk_handle[기술] != 0) return 0;
        int miżura = netwerk_Munzell.fetaħ(0);
        if (miżura < 0) return miżura;
        netwerk_handle[기술] = miżura;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 요청 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int data_ADDRESS, int tul_VALUE, int Settings, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Settings != 0) return -95;
        if (tul_VALUE < 0 || tul_VALUE > 1024) return -90;
        if (tul_VALUE != 0 && !실행관리.klipp(data_ADDRESS, tul_VALUE)) return -14;
        if (!실행관리.klipp(요청주소, 8)) return -14;
        int ADDRESS = 실행관리.수(요청주소);
        int miżura = ċekk_ADDRESS(ADDRESS, 실행관리.수(요청주소 + 4));
        if (miżura < 0) return miżura;
        int 접속번호 = mowbajl_VALUE.기억읽기(ADDRESS + 2) << 8 | mowbajl_VALUE.기억읽기(ADDRESS + 3);
        if (접속번호 == 0) return -22;
        miżura = 자동묶기(기술);
        if (miżura < 0) return miżura;
        for (int INDEX = 0; INDEX < tul_VALUE; INDEX++) trasferiment_data[INDEX] = mowbajl_VALUE.기억읽기(data_ADDRESS + INDEX);
        return netwerk_Munzell.bagħat(netwerk_handle[기술], ADDRESS_32(ADDRESS + 4), 접속번호, trasferiment_data, tul_VALUE);
    }
    static void kiteb_ADDRESS(int ADDRESS, int tul_VALUE, int netwerk_ADDRESS, int 접속번호) {
        for (int INDEX = 0; INDEX < tul_VALUE && INDEX < 16; INDEX++) {
            int VALUE = 0;
            if (INDEX == 0) VALUE = 2;
            if (INDEX == 2) VALUE = 접속번호 >>> 8;
            if (INDEX == 3) VALUE = 접속번호;
            if (INDEX >= 4 && INDEX < 8) VALUE = netwerk_ADDRESS >>> (56 - INDEX * 8);
            mowbajl_VALUE.kiteb_Memorja(ADDRESS + INDEX, VALUE & 255);
        }
    }
    static int 자료전문받기(int 서술자, int data_ADDRESS, int tul_VALUE, int Settings, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Settings & ~64) != 0) return -95;
        if (tul_VALUE < 0) return -22;
        if (tul_VALUE != 0 && !실행관리.klipp(data_ADDRESS, tul_VALUE)) return -14;
        int ADDRESS = 0, ADDRESS_tul_ADDRESS = 0, ADDRESS_tul = 0;
        if (요청주소 != 0) {
            if (!실행관리.klipp(요청주소, 8)) return -14;
            ADDRESS = 실행관리.수(요청주소); ADDRESS_tul_ADDRESS = 실행관리.수(요청주소 + 4);
            if (ADDRESS != 0) {
                if (!실행관리.klipp(ADDRESS_tul_ADDRESS, 4)) return -14;
                ADDRESS_tul = 실행관리.수(ADDRESS_tul_ADDRESS);
                if (ADDRESS_tul < 0) return -22;
                if (!실행관리.klipp(ADDRESS, ADDRESS_tul < 16 ? ADDRESS_tul : 16)) return -14;
            }
        }
        int miżura = 자동묶기(기술);
        if (miżura < 0) return miżura;
        int serje = mowbajl_VALUE.밀리초();
        while (true) {
            miżura = netwerk_Munzell.받기(netwerk_handle[기술], trasferiment_data, 1024, 0);
            if (miżura != -11) break;
            if ((Settings & 64) != 0 || (fetaħ_Settings[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && mowbajl_VALUE.밀리초() - serje >= 수신대기밀리초[기술]) return -11;
            if (mowbajl_VALUE.사용자남은밀리초() <= 10) return -11;
            mowbajl_VALUE.잠시양보();
        }
        if (miżura < 0) return miżura;
        if (miżura > tul_VALUE) miżura = tul_VALUE;
        for (int INDEX = 0; INDEX < miżura; INDEX++) mowbajl_VALUE.kiteb_Memorja(data_ADDRESS + INDEX, trasferiment_data[INDEX]);
        if (ADDRESS != 0) {
            kiteb_ADDRESS(ADDRESS, ADDRESS_tul, netwerk_Munzell.peer_ADDRESS(netwerk_handle[기술]), netwerk_Munzell.상대접속번호(netwerk_handle[기술]));
            실행관리.수쓰기(ADDRESS_tul_ADDRESS, 16);
        }
        return miżura;
    }
    static int 통신주소읽기(int 서술자, int ADDRESS, int tul_ADDRESS) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.klipp(tul_ADDRESS, 4)) return -14;
        int tul_VALUE = 실행관리.수(tul_ADDRESS);
        if (tul_VALUE < 0) return -22;
        if (!실행관리.klipp(ADDRESS, tul_VALUE < 16 ? tul_VALUE : 16)) return -14;
        int slott_entrata = netwerk_Munzell.INDEX(netwerk_handle[기술]);
        kiteb_ADDRESS(ADDRESS, tul_VALUE, mira[기술], slott_entrata < 0 ? 0 : netwerk_Munzell.접속번호들[slott_entrata]);
        실행관리.수쓰기(tul_ADDRESS, 16);
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
