// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 kasutaja 과정의 파일서술자와 열린 Fail 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int 읽기쓰기 = 2, avama_kirje = 64, 독점생성 = 128, eemaldama_Sisu = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] avama_pide = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], siht = new int[서술자한도];
    static int[] Fail_ametikoht = new int[서술자한도], avama_Sätted = new int[서술자한도], viide_COUNT = new int[서술자한도];
    static int[] võrk_pide = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] tee_nimetus = new int[64], Edasta_andmed = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return avama_pide[파일서술자] - 1;
    }
    static int 빈서술자(int Käivita_2) {
        for (int INDEX = Käivita_2; INDEX < 서술자한도; INDEX++) if (avama_pide[INDEX] == 0) return INDEX;
        return -24;
    }
    static int 빈기술() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (viide_COUNT[INDEX] == 0) return INDEX;
        return -24;
    }
    static int Ühendu(int 서술자, int 기술, int 파일종류, int Fail_siht, int Seaded) {
        avama_pide[서술자] = 기술 + 1; 서술자설정[서술자] = (Seaded & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; siht[기술] = Fail_siht; viide_COUNT[기술] = 1;
        avama_Sätted[기술] = Seaded & (3 | 이어쓰기 | 기다리지않기); Fail_ametikoht[기술] = 0;
        võrk_pide[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void START_Joonis() {
        CLEAN_Joonis();
        for (int INDEX = 0; INDEX < 3; INDEX++) Ühendu(INDEX, INDEX, 1, INDEX, INDEX == 0 ? 0 : 1);
    }
    static void CLEAN_Joonis() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (avama_pide[INDEX] != 0) Sule_Fail(INDEX);
    }
    static int Sule_Fail(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        avama_pide[서술자] = 0; 서술자설정[서술자] = 0;
        viide_COUNT[기술]--;
        if (viide_COUNT[기술] == 0) {
            if (종류[기술] == 2) Mälu_failisüsteem.avama_COUNT[siht[기술]]--;
            if (종류[기술] == 3 && võrk_pide[기술] != 0) võrk_Virn.Suletud(võrk_pide[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 bait_VALUE 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int ADDRESS) {
        if (!실행관리.klipp(ADDRESS, 1)) return -14;
        int Asukoht = seade_VALUE.기억읽기(ADDRESS) == '/' ? 1 : 0;
        for (int 길이 = 0; 길이 < 64; 길이++) {
            if (!실행관리.klipp(ADDRESS + Asukoht + 길이, 1)) return -14;
            int VALUE = seade_VALUE.기억읽기(ADDRESS + Asukoht + 길이);
            tee_nimetus[길이] = VALUE;
            if (VALUE == 0) return 길이 == 0 ? -2 : (Mälu_failisüsteem.tšekk_nimetus(tee_nimetus, 길이) ? 길이 : -22);
            if (VALUE == '/') return -20;
        }
        return -36;
    }
    static int avama_Fail(int nimetus_ADDRESS, int Seaded, int 허가) {
        int 길이 = 경로읽기(nimetus_ADDRESS);
        if (길이 < 0) return 길이;
        if ((Seaded & ~(3 | avama_kirje | 독점생성 | eemaldama_Sisu | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Seaded & 3) == 3 || ((Seaded & eemaldama_Sisu) != 0 && (Seaded & 3) == 0)) return -22;
        int Fail = Mälu_failisüsteem.FIND_kirje(tee_nimetus, 길이);
        if (Fail >= 0 && (Seaded & (avama_kirje | 독점생성)) == (avama_kirje | 독점생성)) return -17;
        if (Fail == -2 && (Seaded & avama_kirje) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = 빈기술();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Fail == -2) {
            int TULEMUS = Mälu_failisüsteem.salv_VALUE(tee_nimetus, 길이, tee_nimetus, 0);
            if (TULEMUS < 0) return TULEMUS;
            Fail = Mälu_failisüsteem.FIND_kirje(tee_nimetus, 길이);
            Mälu_failisüsteem.허가들[Fail] = 허가 & 511;
        }
        if (Fail < 0) return Fail;
        if ((Seaded & eemaldama_Sisu) != 0) Mälu_failisüsteem.suurust_muutma_Loend[Fail] = 0;
        Mälu_failisüsteem.avama_COUNT[Fail]++;
        return Ühendu(서술자, 기술, 2, Fail, Seaded);
    }
    static int 파일읽기(int 서술자, int andmed_ADDRESS, int 길이) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (avama_Sätted[기술] & 3) == 1) return -9;
        if (길이 < 0) return -22;
        if (길이 == 0) return 0;
        if (!실행관리.klipp(andmed_ADDRESS, 길이)) return -14;
        if (종류[기술] == 3) return saama_datagramm_andmed(서술자, andmed_ADDRESS, 길이, 0, 0);
        if (종류[기술] == 1) {
            int RECEIVED_COUNT = 0;
            while (RECEIVED_COUNT < 길이) {
                int VALUE = SMS_terminal.직렬읽기();
                if (VALUE < 0) VALUE = klaviatuur.Lugemine();
                if (VALUE < 0) {
                    if (RECEIVED_COUNT > 0) return RECEIVED_COUNT;
                    if ((avama_Sätted[기술] & 기다리지않기) != 0) return -11;
                    if (seade_VALUE.사용자남은밀리초() <= 10) return -11;
                    võrk_Virn.kinnitama(); seade_VALUE.잠시양보();
                } else {
                    seade_VALUE.kirjutamine_Mälu(andmed_ADDRESS + RECEIVED_COUNT, VALUE); RECEIVED_COUNT++;
                }
            }
            return RECEIVED_COUNT;
        }
        int Fail = siht[기술], Asukoht = Fail_ametikoht[기술];
        if (Asukoht >= Mälu_failisüsteem.suurust_muutma_Loend[Fail]) return 0;
        if (길이 > Mälu_failisüsteem.suurust_muutma_Loend[Fail] - Asukoht) 길이 = Mälu_failisüsteem.suurust_muutma_Loend[Fail] - Asukoht;
        int 원본주소 = seade_VALUE.Fail_Mälu() + Fail * Mälu_failisüsteem.최대크기 + Asukoht;
        for (int INDEX = 0; INDEX < 길이; INDEX++) seade_VALUE.kirjutamine_Mälu(andmed_ADDRESS + INDEX, seade_VALUE.기억읽기(원본주소 + INDEX));
        Fail_ametikoht[기술] += 길이;
        return 길이;
    }
    static int kirjutamine_Fail(int 서술자, int andmed_ADDRESS, int 길이) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (avama_Sätted[기술] & 3) == 0) return -9;
        if (길이 < 0) return -22;
        if (길이 == 0) return 0;
        if (!실행관리.klipp(andmed_ADDRESS, 길이)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 sihtkoht_VALUE 주소가 필요하다.
        if (종류[기술] == 1) {
            if (길이 > 16384) 길이 = 16384;
            for (int INDEX = 0; INDEX < 길이; INDEX++) {
                int VALUE = seade_VALUE.기억읽기(andmed_ADDRESS + INDEX);
                SMS_terminal.직렬바이트(VALUE); SMS_terminal.화면문자(VALUE);
            }
            return 길이;
        }
        int Fail = siht[기술], Suurus = Mälu_failisüsteem.suurust_muutma_Loend[Fail];
        int Asukoht = (avama_Sätted[기술] & 이어쓰기) != 0 ? Suurus : Fail_ametikoht[기술];
        if (Asukoht >= Mälu_failisüsteem.최대크기) return -27;
        if (길이 > Mälu_failisüsteem.최대크기 - Asukoht) 길이 = Mälu_failisüsteem.최대크기 - Asukoht;
        int sihtkoht_ADDRESS = seade_VALUE.Fail_Mälu() + Fail * Mälu_failisüsteem.최대크기;
        for (int INDEX = Suurus; INDEX < Asukoht; INDEX++) seade_VALUE.kirjutamine_Mälu(sihtkoht_ADDRESS + INDEX, 0);
        for (int INDEX = 0; INDEX < 길이; INDEX++) seade_VALUE.kirjutamine_Mälu(sihtkoht_ADDRESS + Asukoht + INDEX, seade_VALUE.기억읽기(andmed_ADDRESS + INDEX));
        Fail_ametikoht[기술] = Asukoht + 길이;
        if (Asukoht + 길이 > Suurus) Mälu_failisüsteem.suurust_muutma_Loend[Fail] = Asukoht + 길이;
        return 길이;
    }
    static int otsima_Fail(int 서술자, int nihe_VALUE, int Project_juur) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (Project_juur < 0 || Project_juur > 2) return -22;
        int taust_VALUE = Project_juur == 0 ? 0 : (Project_juur == 1 ? Fail_ametikoht[기술] : Mälu_failisüsteem.suurust_muutma_Loend[siht[기술]]);
        if (nihe_VALUE > 0 && taust_VALUE > 2147483647 - nihe_VALUE) return -75;
        if (nihe_VALUE < 0 && nihe_VALUE < -taust_VALUE) return -22;
        Fail_ametikoht[기술] = taust_VALUE + nihe_VALUE;
        return Fail_ametikoht[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean Määra_VALUE, int Seaded) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return Määra_VALUE ? -9 : -22;
        if (Määra_VALUE && 서술자 == 새서술자) return 새서술자;
        if (Määra_VALUE) { if (avama_pide[새서술자] != 0) Sule_Fail(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        avama_pide[새서술자] = 기술 + 1; 서술자설정[새서술자] = Seaded; viide_COUNT[기술]++;
        return 새서술자;
    }
    static int eemaldama_Fail_kirje_nimetus(int nimetus_ADDRESS) {
        int 길이 = 경로읽기(nimetus_ADDRESS);
        if (길이 < 0) return 길이;
        int Fail = Mälu_failisüsteem.FIND_kirje(tee_nimetus, 길이);
        if (Fail < 0) return Fail;
        Mälu_failisüsteem.이름들[Fail * 64] = 0;
        return 0;
    }
    static int 파일길이정하기(int 서술자, int 길이) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (avama_Sätted[기술] & 3) == 0 || 길이 < 0) return -22;
        if (길이 > Mälu_failisüsteem.최대크기) return -27;
        int Fail = siht[기술], ADDRESS = seade_VALUE.Fail_Mälu() + Fail * Mälu_failisüsteem.최대크기;
        for (int INDEX = Mälu_failisüsteem.suurust_muutma_Loend[Fail]; INDEX < 길이; INDEX++) seade_VALUE.kirjutamine_Mälu(ADDRESS + INDEX, 0);
        Mälu_failisüsteem.suurust_muutma_Loend[Fail] = 길이;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int ADDRESS) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.klipp(ADDRESS, 48)) return -14;
        for (int INDEX = 0; INDEX < 12; INDEX++) 실행관리.kirjutamine_number(ADDRESS + INDEX * 4, 0);
        int Fail = siht[기술], Suurus = 종류[기술] == 2 ? Mälu_failisüsteem.suurust_muutma_Loend[Fail] : 0;
        int 허가 = 종류[기술] == 2 ? Mälu_failisüsteem.허가들[Fail] : 438;
        실행관리.kirjutamine_number(ADDRESS, 1);
        실행관리.kirjutamine_number(ADDRESS + 4, 종류[기술] == 2 ? Fail + 1 : 100 + 기술);
        실행관리.kirjutamine_number(ADDRESS + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.kirjutamine_number(ADDRESS + 12, 종류[기술] == 2 && Mälu_failisüsteem.이름들[Fail * 64] == 0 ? 0 : 1);
        실행관리.kirjutamine_number(ADDRESS + 28, Suurus); 실행관리.kirjutamine_number(ADDRESS + 32, 512);
        실행관리.kirjutamine_number(ADDRESS + 36, (Suurus + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int Käsk, int VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Käsk == 0 || Käsk == 1030) return 서술자복제(서술자, VALUE, false, Käsk == 1030 ? 1 : 0);
        if (Käsk == 1) return 서술자설정[서술자];
        if (Käsk == 2) { if ((VALUE & ~1) != 0) return -22; 서술자설정[서술자] = VALUE; return 0; }
        if (Käsk == 3) return avama_Sätted[기술];
        if (Käsk == 4) {
            if ((VALUE & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            avama_Sätted[기술] = (avama_Sätted[기술] & 3) | (VALUE & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int avama_osaleja(int 주소체계, int 통신종류, int kaasus_number) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (kaasus_number != 0 && kaasus_number != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = 빈기술();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Ühendu(서술자, 기술, 3, 0, 읽기쓰기);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int ADDRESS_32(int ADDRESS) {
        return seade_VALUE.기억읽기(ADDRESS) << 24 | seade_VALUE.기억읽기(ADDRESS + 1) << 16
            | seade_VALUE.기억읽기(ADDRESS + 2) << 8 | seade_VALUE.기억읽기(ADDRESS + 3);
    }
    static int tšekk_ADDRESS(int ADDRESS, int 길이) {
        if (길이 < 16) return -22;
        if (!실행관리.klipp(ADDRESS, 16)) return -14;
        return 실행관리.짧은수(ADDRESS) == 2 ? 0 : -97;
    }
    static int BIND_ADDRESS(int 서술자, int ADDRESS, int 길이) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int TULEMUS = tšekk_ADDRESS(ADDRESS, 길이);
        if (TULEMUS < 0) return TULEMUS;
        if (võrk_pide[기술] != 0) return -22;
        int võrgu_ID = ADDRESS_32(ADDRESS + 4);
        if (võrgu_ID != 0 && võrgu_ID != võrk_Virn.내주소) return -99;
        int pordinumber = seade_VALUE.기억읽기(ADDRESS + 2) << 8 | seade_VALUE.기억읽기(ADDRESS + 3);
        TULEMUS = võrk_Virn.Ava(pordinumber);
        if (TULEMUS < 0) return TULEMUS;
        võrk_pide[기술] = TULEMUS; siht[기술] = võrgu_ID;
        return 0;
    }
    static int Automaatne_BIND(int 기술) {
        if (võrk_pide[기술] != 0) return 0;
        int TULEMUS = võrk_Virn.Ava(0);
        if (TULEMUS < 0) return TULEMUS;
        võrk_pide[기술] = TULEMUS;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 päring 구조체로 전달한다.
    static int saatma_datagramm_andmed(int 서술자, int andmed_ADDRESS, int 길이, int Seaded, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Seaded != 0) return -95;
        if (길이 < 0 || 길이 > 1024) return -90;
        if (길이 != 0 && !실행관리.klipp(andmed_ADDRESS, 길이)) return -14;
        if (!실행관리.klipp(요청주소, 8)) return -14;
        int ADDRESS = 실행관리.number(요청주소);
        int TULEMUS = tšekk_ADDRESS(ADDRESS, 실행관리.number(요청주소 + 4));
        if (TULEMUS < 0) return TULEMUS;
        int pordinumber = seade_VALUE.기억읽기(ADDRESS + 2) << 8 | seade_VALUE.기억읽기(ADDRESS + 3);
        if (pordinumber == 0) return -22;
        TULEMUS = Automaatne_BIND(기술);
        if (TULEMUS < 0) return TULEMUS;
        for (int INDEX = 0; INDEX < 길이; INDEX++) Edasta_andmed[INDEX] = seade_VALUE.기억읽기(andmed_ADDRESS + INDEX);
        return võrk_Virn.saatma(võrk_pide[기술], ADDRESS_32(ADDRESS + 4), pordinumber, Edasta_andmed, 길이);
    }
    static void kirjutamine_ADDRESS(int ADDRESS, int 길이, int võrgu_ID, int pordinumber) {
        for (int INDEX = 0; INDEX < 길이 && INDEX < 16; INDEX++) {
            int VALUE = 0;
            if (INDEX == 0) VALUE = 2;
            if (INDEX == 2) VALUE = pordinumber >>> 8;
            if (INDEX == 3) VALUE = pordinumber;
            if (INDEX >= 4 && INDEX < 8) VALUE = võrgu_ID >>> (56 - INDEX * 8);
            seade_VALUE.kirjutamine_Mälu(ADDRESS + INDEX, VALUE & 255);
        }
    }
    static int saama_datagramm_andmed(int 서술자, int andmed_ADDRESS, int 길이, int Seaded, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Seaded & ~64) != 0) return -95;
        if (길이 < 0) return -22;
        if (길이 != 0 && !실행관리.klipp(andmed_ADDRESS, 길이)) return -14;
        int ADDRESS = 0, 주소길이주소 = 0, 주소길이 = 0;
        if (요청주소 != 0) {
            if (!실행관리.klipp(요청주소, 8)) return -14;
            ADDRESS = 실행관리.number(요청주소); 주소길이주소 = 실행관리.number(요청주소 + 4);
            if (ADDRESS != 0) {
                if (!실행관리.klipp(주소길이주소, 4)) return -14;
                주소길이 = 실행관리.number(주소길이주소);
                if (주소길이 < 0) return -22;
                if (!실행관리.klipp(ADDRESS, 주소길이 < 16 ? 주소길이 : 16)) return -14;
            }
        }
        int TULEMUS = Automaatne_BIND(기술);
        if (TULEMUS < 0) return TULEMUS;
        int Käivita_2 = seade_VALUE.밀리초();
        while (true) {
            TULEMUS = võrk_Virn.saama(võrk_pide[기술], Edasta_andmed, 1024, 0);
            if (TULEMUS != -11) break;
            if ((Seaded & 64) != 0 || (avama_Sätted[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && seade_VALUE.밀리초() - Käivita_2 >= 수신대기밀리초[기술]) return -11;
            if (seade_VALUE.사용자남은밀리초() <= 10) return -11;
            seade_VALUE.잠시양보();
        }
        if (TULEMUS < 0) return TULEMUS;
        if (TULEMUS > 길이) TULEMUS = 길이;
        for (int INDEX = 0; INDEX < TULEMUS; INDEX++) seade_VALUE.kirjutamine_Mälu(andmed_ADDRESS + INDEX, Edasta_andmed[INDEX]);
        if (ADDRESS != 0) {
            kirjutamine_ADDRESS(ADDRESS, 주소길이, võrk_Virn.partner_ADDRESS(võrk_pide[기술]), võrk_Virn.partner_pordinumber(võrk_pide[기술]));
            실행관리.kirjutamine_number(주소길이주소, 16);
        }
        return TULEMUS;
    }
    static int 통신주소읽기(int 서술자, int ADDRESS, int 길이주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.klipp(길이주소, 4)) return -14;
        int 길이 = 실행관리.number(길이주소);
        if (길이 < 0) return -22;
        if (!실행관리.klipp(ADDRESS, 길이 < 16 ? 길이 : 16)) return -14;
        int 칸 = võrk_Virn.INDEX(võrk_pide[기술]);
        kirjutamine_ADDRESS(ADDRESS, 길이, siht[기술], 칸 < 0 ? 0 : võrk_Virn.접속번호들[칸]);
        실행관리.kirjutamine_number(길이주소, 16);
        return 0;
    }
    static int hulk_saama_TIMEOUT(int 서술자, int 밀리초) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (밀리초 < 0 || 밀리초 > 2000) return -22;
        수신대기밀리초[기술] = 밀리초;
        return 0;
    }
}
