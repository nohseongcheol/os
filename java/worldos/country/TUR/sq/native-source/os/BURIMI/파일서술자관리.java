// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 përdorues 과정의 파일서술자와 열린 Kartelë 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int lexoj_shkruaj_flamur = 2, Krijo_futje = 64, 독점생성 = 128, pastroj_TOC = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] hap_dorezë = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], objektiv = new int[서술자한도];
    static int[] skedar_pozicioni = new int[서술자한도], hap_cilësimet = new int[서술자한도], Referencë_COUNT = new int[서술자한도];
    static int[] rrjet_dorezë = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] shteg_emër = new int[64], transferim_të_dhëna = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return hap_dorezë[파일서술자] - 1;
    }
    static int 빈서술자(int Ekzekuto) {
        for (int INDEX = Ekzekuto; INDEX < 서술자한도; INDEX++) if (hap_dorezë[INDEX] == 0) return INDEX;
        return -24;
    }
    static int bosh_dorezë() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (Referencë_COUNT[INDEX] == 0) return INDEX;
        return -24;
    }
    static int Lidhu(int 서술자, int 기술, int 파일종류, int skedar_objektiv, int Rregullime) {
        hap_dorezë[서술자] = 기술 + 1; 서술자설정[서술자] = (Rregullime & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; objektiv[기술] = skedar_objektiv; Referencë_COUNT[기술] = 1;
        hap_cilësimet[기술] = Rregullime & (3 | 이어쓰기 | 기다리지않기); skedar_pozicioni[기술] = 0;
        rrjet_dorezë[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void nis_Proces() {
        CLEAN_Proces();
        for (int INDEX = 0; INDEX < 3; INDEX++) Lidhu(INDEX, INDEX, 1, INDEX, INDEX == 0 ? 0 : 1);
    }
    static void CLEAN_Proces() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (hap_dorezë[INDEX] != 0) mbyll_skedar(INDEX);
    }
    static int mbyll_skedar(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        hap_dorezë[서술자] = 0; 서술자설정[서술자] = 0;
        Referencë_COUNT[기술]--;
        if (Referencë_COUNT[기술] == 0) {
            if (종류[기술] == 2) Memorie_sistemi_i_skedarëve.hap_COUNT[objektiv[기술]]--;
            if (종류[기술] == 3 && rrjet_dorezë[기술] != 0) rrjet_Stivë.Mbyll(rrjet_dorezë[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 bajt_VALUE 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int email) {
        if (!실행관리.fragment(email, 1)) return -14;
        int Pozicioni = pajisje_VALUE.기억읽기(email) == '/' ? 1 : 0;
        for (int gjatësi_VALUE = 0; gjatësi_VALUE < 64; gjatësi_VALUE++) {
            if (!실행관리.fragment(email + Pozicioni + gjatësi_VALUE, 1)) return -14;
            int VALUE = pajisje_VALUE.기억읽기(email + Pozicioni + gjatësi_VALUE);
            shteg_emër[gjatësi_VALUE] = VALUE;
            if (VALUE == 0) return gjatësi_VALUE == 0 ? -2 : (Memorie_sistemi_i_skedarëve.çek_emër(shteg_emër, gjatësi_VALUE) ? gjatësi_VALUE : -22);
            if (VALUE == '/') return -20;
        }
        return -36;
    }
    static int hap_skedar(int emër_email, int Rregullime, int 허가) {
        int gjatësi_VALUE = 경로읽기(emër_email);
        if (gjatësi_VALUE < 0) return gjatësi_VALUE;
        if ((Rregullime & ~(3 | Krijo_futje | 독점생성 | pastroj_TOC | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Rregullime & 3) == 3 || ((Rregullime & pastroj_TOC) != 0 && (Rregullime & 3) == 0)) return -22;
        int Kartelë = Memorie_sistemi_i_skedarëve.FIND_futje(shteg_emër, gjatësi_VALUE);
        if (Kartelë >= 0 && (Rregullime & (Krijo_futje | 독점생성)) == (Krijo_futje | 독점생성)) return -17;
        if (Kartelë == -2 && (Rregullime & Krijo_futje) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = bosh_dorezë();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Kartelë == -2) {
            int llogaritje = Memorie_sistemi_i_skedarëve.Store_VALUE(shteg_emër, gjatësi_VALUE, shteg_emër, 0);
            if (llogaritje < 0) return llogaritje;
            Kartelë = Memorie_sistemi_i_skedarëve.FIND_futje(shteg_emër, gjatësi_VALUE);
            Memorie_sistemi_i_skedarëve.허가들[Kartelë] = 허가 & 511;
        }
        if (Kartelë < 0) return Kartelë;
        if ((Rregullime & pastroj_TOC) != 0) Memorie_sistemi_i_skedarëve.ndryshoj_përmasat_Listë[Kartelë] = 0;
        Memorie_sistemi_i_skedarëve.hap_COUNT[Kartelë]++;
        return Lidhu(서술자, 기술, 2, Kartelë, Rregullime);
    }
    static int 파일읽기(int 서술자, int të_dhëna_email, int gjatësi_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (hap_cilësimet[기술] & 3) == 1) return -9;
        if (gjatësi_VALUE < 0) return -22;
        if (gjatësi_VALUE == 0) return 0;
        if (!실행관리.fragment(të_dhëna_email, gjatësi_VALUE)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, të_dhëna_email, gjatësi_VALUE, 0, 0);
        if (종류[기술] == 1) {
            int RECEIVED_COUNT = 0;
            while (RECEIVED_COUNT < gjatësi_VALUE) {
                int VALUE = SMS_Terminali.직렬읽기();
                if (VALUE < 0) VALUE = tastiera.Leximi();
                if (VALUE < 0) {
                    if (RECEIVED_COUNT > 0) return RECEIVED_COUNT;
                    if ((hap_cilësimet[기술] & 기다리지않기) != 0) return -11;
                    if (pajisje_VALUE.사용자남은밀리초() <= 10) return -11;
                    rrjet_Stivë.verifikoj(); pajisje_VALUE.잠시양보();
                } else {
                    pajisje_VALUE.shkruaj_Memorie(të_dhëna_email + RECEIVED_COUNT, VALUE); RECEIVED_COUNT++;
                }
            }
            return RECEIVED_COUNT;
        }
        int Kartelë = objektiv[기술], Pozicioni = skedar_pozicioni[기술];
        if (Pozicioni >= Memorie_sistemi_i_skedarëve.ndryshoj_përmasat_Listë[Kartelë]) return 0;
        if (gjatësi_VALUE > Memorie_sistemi_i_skedarëve.ndryshoj_përmasat_Listë[Kartelë] - Pozicioni) gjatësi_VALUE = Memorie_sistemi_i_skedarëve.ndryshoj_përmasat_Listë[Kartelë] - Pozicioni;
        int 원본주소 = pajisje_VALUE.skedar_Memorie() + Kartelë * Memorie_sistemi_i_skedarëve.최대크기 + Pozicioni;
        for (int INDEX = 0; INDEX < gjatësi_VALUE; INDEX++) pajisje_VALUE.shkruaj_Memorie(të_dhëna_email + INDEX, pajisje_VALUE.기억읽기(원본주소 + INDEX));
        skedar_pozicioni[기술] += gjatësi_VALUE;
        return gjatësi_VALUE;
    }
    static int shkruaj_skedar(int 서술자, int të_dhëna_email, int gjatësi_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (hap_cilësimet[기술] & 3) == 0) return -9;
        if (gjatësi_VALUE < 0) return -22;
        if (gjatësi_VALUE == 0) return 0;
        if (!실행관리.fragment(të_dhëna_email, gjatësi_VALUE)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 vendmbërritje_VALUE 주소가 필요하다.
        if (종류[기술] == 1) {
            if (gjatësi_VALUE > 16384) gjatësi_VALUE = 16384;
            for (int INDEX = 0; INDEX < gjatësi_VALUE; INDEX++) {
                int VALUE = pajisje_VALUE.기억읽기(të_dhëna_email + INDEX);
                SMS_Terminali.직렬바이트(VALUE); SMS_Terminali.화면문자(VALUE);
            }
            return gjatësi_VALUE;
        }
        int Kartelë = objektiv[기술], Madhësi = Memorie_sistemi_i_skedarëve.ndryshoj_përmasat_Listë[Kartelë];
        int Pozicioni = (hap_cilësimet[기술] & 이어쓰기) != 0 ? Madhësi : skedar_pozicioni[기술];
        if (Pozicioni >= Memorie_sistemi_i_skedarëve.최대크기) return -27;
        if (gjatësi_VALUE > Memorie_sistemi_i_skedarëve.최대크기 - Pozicioni) gjatësi_VALUE = Memorie_sistemi_i_skedarëve.최대크기 - Pozicioni;
        int vendmbërritje_email = pajisje_VALUE.skedar_Memorie() + Kartelë * Memorie_sistemi_i_skedarëve.최대크기;
        for (int INDEX = Madhësi; INDEX < Pozicioni; INDEX++) pajisje_VALUE.shkruaj_Memorie(vendmbërritje_email + INDEX, 0);
        for (int INDEX = 0; INDEX < gjatësi_VALUE; INDEX++) pajisje_VALUE.shkruaj_Memorie(vendmbërritje_email + Pozicioni + INDEX, pajisje_VALUE.기억읽기(të_dhëna_email + INDEX));
        skedar_pozicioni[기술] = Pozicioni + gjatësi_VALUE;
        if (Pozicioni + gjatësi_VALUE > Madhësi) Memorie_sistemi_i_skedarëve.ndryshoj_përmasat_Listë[Kartelë] = Pozicioni + gjatësi_VALUE;
        return gjatësi_VALUE;
    }
    static int kërko_skedar(int 서술자, int OFFSET_VALUE, int Project_rrënjë) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (Project_rrënjë < 0 || Project_rrënjë > 2) return -22;
        int Sfond_VALUE = Project_rrënjë == 0 ? 0 : (Project_rrënjë == 1 ? skedar_pozicioni[기술] : Memorie_sistemi_i_skedarëve.ndryshoj_përmasat_Listë[objektiv[기술]]);
        if (OFFSET_VALUE > 0 && Sfond_VALUE > 2147483647 - OFFSET_VALUE) return -75;
        if (OFFSET_VALUE < 0 && OFFSET_VALUE < -Sfond_VALUE) return -22;
        skedar_pozicioni[기술] = Sfond_VALUE + OFFSET_VALUE;
        return skedar_pozicioni[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean cakto_VALUE, int Rregullime) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return cakto_VALUE ? -9 : -22;
        if (cakto_VALUE && 서술자 == 새서술자) return 새서술자;
        if (cakto_VALUE) { if (hap_dorezë[새서술자] != 0) mbyll_skedar(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        hap_dorezë[새서술자] = 기술 + 1; 서술자설정[새서술자] = Rregullime; Referencë_COUNT[기술]++;
        return 새서술자;
    }
    static int heq_skedar_futje_emër(int emër_email) {
        int gjatësi_VALUE = 경로읽기(emër_email);
        if (gjatësi_VALUE < 0) return gjatësi_VALUE;
        int Kartelë = Memorie_sistemi_i_skedarëve.FIND_futje(shteg_emër, gjatësi_VALUE);
        if (Kartelë < 0) return Kartelë;
        Memorie_sistemi_i_skedarëve.이름들[Kartelë * 64] = 0;
        return 0;
    }
    static int bashkësi_skedar_gjatësi(int 서술자, int gjatësi_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (hap_cilësimet[기술] & 3) == 0 || gjatësi_VALUE < 0) return -22;
        if (gjatësi_VALUE > Memorie_sistemi_i_skedarëve.최대크기) return -27;
        int Kartelë = objektiv[기술], email = pajisje_VALUE.skedar_Memorie() + Kartelë * Memorie_sistemi_i_skedarëve.최대크기;
        for (int INDEX = Memorie_sistemi_i_skedarëve.ndryshoj_përmasat_Listë[Kartelë]; INDEX < gjatësi_VALUE; INDEX++) pajisje_VALUE.shkruaj_Memorie(email + INDEX, 0);
        Memorie_sistemi_i_skedarëve.ndryshoj_përmasat_Listë[Kartelë] = gjatësi_VALUE;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int email) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.fragment(email, 48)) return -14;
        for (int INDEX = 0; INDEX < 12; INDEX++) 실행관리.수쓰기(email + INDEX * 4, 0);
        int Kartelë = objektiv[기술], Madhësi = 종류[기술] == 2 ? Memorie_sistemi_i_skedarëve.ndryshoj_përmasat_Listë[Kartelë] : 0;
        int 허가 = 종류[기술] == 2 ? Memorie_sistemi_i_skedarëve.허가들[Kartelë] : 438;
        실행관리.수쓰기(email, 1);
        실행관리.수쓰기(email + 4, 종류[기술] == 2 ? Kartelë + 1 : 100 + 기술);
        실행관리.수쓰기(email + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(email + 12, 종류[기술] == 2 && Memorie_sistemi_i_skedarëve.이름들[Kartelë * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(email + 28, Madhësi); 실행관리.수쓰기(email + 32, 512);
        실행관리.수쓰기(email + 36, (Madhësi + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int Komanda, int VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Komanda == 0 || Komanda == 1030) return 서술자복제(서술자, VALUE, false, Komanda == 1030 ? 1 : 0);
        if (Komanda == 1) return 서술자설정[서술자];
        if (Komanda == 2) { if ((VALUE & ~1) != 0) return -22; 서술자설정[서술자] = VALUE; return 0; }
        if (Komanda == 3) return hap_cilësimet[기술];
        if (Komanda == 4) {
            if ((VALUE & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            hap_cilësimet[기술] = (hap_cilësimet[기술] & 3) | (VALUE & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int 통신종단점만들기(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = bosh_dorezë();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Lidhu(서술자, 기술, 3, 0, lexoj_shkruaj_flamur);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int email_32(int email) {
        return pajisje_VALUE.기억읽기(email) << 24 | pajisje_VALUE.기억읽기(email + 1) << 16
            | pajisje_VALUE.기억읽기(email + 2) << 8 | pajisje_VALUE.기억읽기(email + 3);
    }
    static int çek_email(int email, int gjatësi_VALUE) {
        if (gjatësi_VALUE < 16) return -22;
        if (!실행관리.fragment(email, 16)) return -14;
        return 실행관리.짧은수(email) == 2 ? 0 : -97;
    }
    static int BIND_email(int 서술자, int email, int gjatësi_VALUE) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int llogaritje = çek_email(email, gjatësi_VALUE);
        if (llogaritje < 0) return llogaritje;
        if (rrjet_dorezë[기술] != 0) return -22;
        int rrjet_email_df3458bb = email_32(email + 4);
        if (rrjet_email_df3458bb != 0 && rrjet_email_df3458bb != rrjet_Stivë.내주소) return -99;
        int numri_i_portës = pajisje_VALUE.기억읽기(email + 2) << 8 | pajisje_VALUE.기억읽기(email + 3);
        llogaritje = rrjet_Stivë.Hap(numri_i_portës);
        if (llogaritje < 0) return llogaritje;
        rrjet_dorezë[기술] = llogaritje; objektiv[기술] = rrjet_email_df3458bb;
        return 0;
    }
    static int Automatik_BIND(int 기술) {
        if (rrjet_dorezë[기술] != 0) return 0;
        int llogaritje = rrjet_Stivë.Hap(0);
        if (llogaritje < 0) return llogaritje;
        rrjet_dorezë[기술] = llogaritje;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 요청 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int të_dhëna_email, int gjatësi_VALUE, int Rregullime, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Rregullime != 0) return -95;
        if (gjatësi_VALUE < 0 || gjatësi_VALUE > 1024) return -90;
        if (gjatësi_VALUE != 0 && !실행관리.fragment(të_dhëna_email, gjatësi_VALUE)) return -14;
        if (!실행관리.fragment(요청주소, 8)) return -14;
        int email = 실행관리.수(요청주소);
        int llogaritje = çek_email(email, 실행관리.수(요청주소 + 4));
        if (llogaritje < 0) return llogaritje;
        int numri_i_portës = pajisje_VALUE.기억읽기(email + 2) << 8 | pajisje_VALUE.기억읽기(email + 3);
        if (numri_i_portës == 0) return -22;
        llogaritje = Automatik_BIND(기술);
        if (llogaritje < 0) return llogaritje;
        for (int INDEX = 0; INDEX < gjatësi_VALUE; INDEX++) transferim_të_dhëna[INDEX] = pajisje_VALUE.기억읽기(të_dhëna_email + INDEX);
        return rrjet_Stivë.dërgoj(rrjet_dorezë[기술], email_32(email + 4), numri_i_portës, transferim_të_dhëna, gjatësi_VALUE);
    }
    static void shkruaj_email(int email, int gjatësi_VALUE, int rrjet_email_df3458bb, int numri_i_portës) {
        for (int INDEX = 0; INDEX < gjatësi_VALUE && INDEX < 16; INDEX++) {
            int VALUE = 0;
            if (INDEX == 0) VALUE = 2;
            if (INDEX == 2) VALUE = numri_i_portës >>> 8;
            if (INDEX == 3) VALUE = numri_i_portës;
            if (INDEX >= 4 && INDEX < 8) VALUE = rrjet_email_df3458bb >>> (56 - INDEX * 8);
            pajisje_VALUE.shkruaj_Memorie(email + INDEX, VALUE & 255);
        }
    }
    static int 자료전문받기(int 서술자, int të_dhëna_email, int gjatësi_VALUE, int Rregullime, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Rregullime & ~64) != 0) return -95;
        if (gjatësi_VALUE < 0) return -22;
        if (gjatësi_VALUE != 0 && !실행관리.fragment(të_dhëna_email, gjatësi_VALUE)) return -14;
        int email = 0, email_gjatësi_email = 0, email_gjatësi = 0;
        if (요청주소 != 0) {
            if (!실행관리.fragment(요청주소, 8)) return -14;
            email = 실행관리.수(요청주소); email_gjatësi_email = 실행관리.수(요청주소 + 4);
            if (email != 0) {
                if (!실행관리.fragment(email_gjatësi_email, 4)) return -14;
                email_gjatësi = 실행관리.수(email_gjatësi_email);
                if (email_gjatësi < 0) return -22;
                if (!실행관리.fragment(email, email_gjatësi < 16 ? email_gjatësi : 16)) return -14;
            }
        }
        int llogaritje = Automatik_BIND(기술);
        if (llogaritje < 0) return llogaritje;
        int Ekzekuto = pajisje_VALUE.밀리초();
        while (true) {
            llogaritje = rrjet_Stivë.받기(rrjet_dorezë[기술], transferim_të_dhëna, 1024, 0);
            if (llogaritje != -11) break;
            if ((Rregullime & 64) != 0 || (hap_cilësimet[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && pajisje_VALUE.밀리초() - Ekzekuto >= 수신대기밀리초[기술]) return -11;
            if (pajisje_VALUE.사용자남은밀리초() <= 10) return -11;
            pajisje_VALUE.잠시양보();
        }
        if (llogaritje < 0) return llogaritje;
        if (llogaritje > gjatësi_VALUE) llogaritje = gjatësi_VALUE;
        for (int INDEX = 0; INDEX < llogaritje; INDEX++) pajisje_VALUE.shkruaj_Memorie(të_dhëna_email + INDEX, transferim_të_dhëna[INDEX]);
        if (email != 0) {
            shkruaj_email(email, email_gjatësi, rrjet_Stivë.homolog_email(rrjet_dorezë[기술]), rrjet_Stivë.homolog_numri_i_portës(rrjet_dorezë[기술]));
            실행관리.수쓰기(email_gjatësi_email, 16);
        }
        return llogaritje;
    }
    static int 통신주소읽기(int 서술자, int email, int gjatësi_email) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.fragment(gjatësi_email, 4)) return -14;
        int gjatësi_VALUE = 실행관리.수(gjatësi_email);
        if (gjatësi_VALUE < 0) return -22;
        if (!실행관리.fragment(email, gjatësi_VALUE < 16 ? gjatësi_VALUE : 16)) return -14;
        int hapësirë_për_tekst_futje = rrjet_Stivë.INDEX(rrjet_dorezë[기술]);
        shkruaj_email(email, gjatësi_VALUE, objektiv[기술], hapësirë_për_tekst_futje < 0 ? 0 : rrjet_Stivë.접속번호들[hapësirë_për_tekst_futje]);
        실행관리.수쓰기(gjatësi_email, 16);
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
