// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 gebruiker 과정의 파일서술자와 열린 Lêer 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int lees_skryf_vlag = 2, Skep_inskrywing = 64, 독점생성 = 128, vee_uit_inhoud = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] skep_handvatsel = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], teiken = new int[서술자한도];
    static int[] lêer_plaas = new int[서술자한도], skep_Instellings = new int[서술자한도], Naslaan_COUNT = new int[서술자한도];
    static int[] Netwerk_handvatsel = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] pad_naam = new int[64], oordra_data = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return skep_handvatsel[파일서술자] - 1;
    }
    static int 빈서술자(int Loop) {
        for (int INDEX = Loop; INDEX < 서술자한도; INDEX++) if (skep_handvatsel[INDEX] == 0) return INDEX;
        return -24;
    }
    static int leeg_handvatsel() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (Naslaan_COUNT[INDEX] == 0) return INDEX;
        return -24;
    }
    static int Koppel(int 서술자, int 기술, int 파일종류, int lêer_teiken, int Instellings) {
        skep_handvatsel[서술자] = 기술 + 1; 서술자설정[서술자] = (Instellings & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; teiken[기술] = lêer_teiken; Naslaan_COUNT[기술] = 1;
        skep_Instellings[기술] = Instellings & (3 | 이어쓰기 | 기다리지않기); lêer_plaas[기술] = 0;
        Netwerk_handvatsel[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void BEGIN_Proses() {
        CLEAN_Proses();
        for (int INDEX = 0; INDEX < 3; INDEX++) Koppel(INDEX, INDEX, 1, INDEX, INDEX == 0 ? 0 : 1);
    }
    static void CLEAN_Proses() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (skep_handvatsel[INDEX] != 0) sluit_lêer(INDEX);
    }
    static int sluit_lêer(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        skep_handvatsel[서술자] = 0; 서술자설정[서술자] = 0;
        Naslaan_COUNT[기술]--;
        if (Naslaan_COUNT[기술] == 0) {
            if (종류[기술] == 2) Geheue_lêerstelsel.skep_COUNT[teiken[기술]]--;
            if (종류[기술] == 3 && Netwerk_handvatsel[기술] != 0) Netwerk_Stapel.Sluit(Netwerk_handvatsel[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 greep_VALUE 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int adres) {
        if (!실행관리.snit(adres, 1)) return -14;
        int Posisie = mobiel_VALUE.기억읽기(adres) == '/' ? 1 : 0;
        for (int lengte_VALUE = 0; lengte_VALUE < 64; lengte_VALUE++) {
            if (!실행관리.snit(adres + Posisie + lengte_VALUE, 1)) return -14;
            int VALUE = mobiel_VALUE.기억읽기(adres + Posisie + lengte_VALUE);
            pad_naam[lengte_VALUE] = VALUE;
            if (VALUE == 0) return lengte_VALUE == 0 ? -2 : (Geheue_lêerstelsel.tjek_naam(pad_naam, lengte_VALUE) ? lengte_VALUE : -22);
            if (VALUE == '/') return -20;
        }
        return -36;
    }
    static int skep_lêer(int naam_adres, int Instellings, int 허가) {
        int lengte_VALUE = 경로읽기(naam_adres);
        if (lengte_VALUE < 0) return lengte_VALUE;
        if ((Instellings & ~(3 | Skep_inskrywing | 독점생성 | vee_uit_inhoud | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Instellings & 3) == 3 || ((Instellings & vee_uit_inhoud) != 0 && (Instellings & 3) == 0)) return -22;
        int Lêer = Geheue_lêerstelsel.FIND_inskrywing(pad_naam, lengte_VALUE);
        if (Lêer >= 0 && (Instellings & (Skep_inskrywing | 독점생성)) == (Skep_inskrywing | 독점생성)) return -17;
        if (Lêer == -2 && (Instellings & Skep_inskrywing) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = leeg_handvatsel();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Lêer == -2) {
            int maatreël = Geheue_lêerstelsel.bêre_VALUE(pad_naam, lengte_VALUE, pad_naam, 0);
            if (maatreël < 0) return maatreël;
            Lêer = Geheue_lêerstelsel.FIND_inskrywing(pad_naam, lengte_VALUE);
            Geheue_lêerstelsel.허가들[Lêer] = 허가 & 511;
        }
        if (Lêer < 0) return Lêer;
        if ((Instellings & vee_uit_inhoud) != 0) Geheue_lêerstelsel.verstel_Lys[Lêer] = 0;
        Geheue_lêerstelsel.skep_COUNT[Lêer]++;
        return Koppel(서술자, 기술, 2, Lêer, Instellings);
    }
    static int 파일읽기(int 서술자, int data_adres, int lengte_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (skep_Instellings[기술] & 3) == 1) return -9;
        if (lengte_VALUE < 0) return -22;
        if (lengte_VALUE == 0) return 0;
        if (!실행관리.snit(data_adres, lengte_VALUE)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, data_adres, lengte_VALUE, 0, 0);
        if (종류[기술] == 1) {
            int RECEIVED_COUNT = 0;
            while (RECEIVED_COUNT < lengte_VALUE) {
                int VALUE = SMS_Terminaal.직렬읽기();
                if (VALUE < 0) VALUE = sleutelbord.Lees();
                if (VALUE < 0) {
                    if (RECEIVED_COUNT > 0) return RECEIVED_COUNT;
                    if ((skep_Instellings[기술] & 기다리지않기) != 0) return -11;
                    if (mobiel_VALUE.사용자남은밀리초() <= 10) return -11;
                    Netwerk_Stapel.verifieer(); mobiel_VALUE.잠시양보();
                } else {
                    mobiel_VALUE.skryf_Geheue(data_adres + RECEIVED_COUNT, VALUE); RECEIVED_COUNT++;
                }
            }
            return RECEIVED_COUNT;
        }
        int Lêer = teiken[기술], Posisie = lêer_plaas[기술];
        if (Posisie >= Geheue_lêerstelsel.verstel_Lys[Lêer]) return 0;
        if (lengte_VALUE > Geheue_lêerstelsel.verstel_Lys[Lêer] - Posisie) lengte_VALUE = Geheue_lêerstelsel.verstel_Lys[Lêer] - Posisie;
        int 원본주소 = mobiel_VALUE.lêer_Geheue() + Lêer * Geheue_lêerstelsel.최대크기 + Posisie;
        for (int INDEX = 0; INDEX < lengte_VALUE; INDEX++) mobiel_VALUE.skryf_Geheue(data_adres + INDEX, mobiel_VALUE.기억읽기(원본주소 + INDEX));
        lêer_plaas[기술] += lengte_VALUE;
        return lengte_VALUE;
    }
    static int skryf_lêer(int 서술자, int data_adres, int lengte_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (skep_Instellings[기술] & 3) == 0) return -9;
        if (lengte_VALUE < 0) return -22;
        if (lengte_VALUE == 0) return 0;
        if (!실행관리.snit(data_adres, lengte_VALUE)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 bestemming_VALUE 주소가 필요하다.
        if (종류[기술] == 1) {
            if (lengte_VALUE > 16384) lengte_VALUE = 16384;
            for (int INDEX = 0; INDEX < lengte_VALUE; INDEX++) {
                int VALUE = mobiel_VALUE.기억읽기(data_adres + INDEX);
                SMS_Terminaal.직렬바이트(VALUE); SMS_Terminaal.화면문자(VALUE);
            }
            return lengte_VALUE;
        }
        int Lêer = teiken[기술], Grootte = Geheue_lêerstelsel.verstel_Lys[Lêer];
        int Posisie = (skep_Instellings[기술] & 이어쓰기) != 0 ? Grootte : lêer_plaas[기술];
        if (Posisie >= Geheue_lêerstelsel.최대크기) return -27;
        if (lengte_VALUE > Geheue_lêerstelsel.최대크기 - Posisie) lengte_VALUE = Geheue_lêerstelsel.최대크기 - Posisie;
        int bestemming_adres = mobiel_VALUE.lêer_Geheue() + Lêer * Geheue_lêerstelsel.최대크기;
        for (int INDEX = Grootte; INDEX < Posisie; INDEX++) mobiel_VALUE.skryf_Geheue(bestemming_adres + INDEX, 0);
        for (int INDEX = 0; INDEX < lengte_VALUE; INDEX++) mobiel_VALUE.skryf_Geheue(bestemming_adres + Posisie + INDEX, mobiel_VALUE.기억읽기(data_adres + INDEX));
        lêer_plaas[기술] = Posisie + lengte_VALUE;
        if (Posisie + lengte_VALUE > Grootte) Geheue_lêerstelsel.verstel_Lys[Lêer] = Posisie + lengte_VALUE;
        return lengte_VALUE;
    }
    static int soek_lêer(int 서술자, int OFFSET_VALUE, int Project_wortel) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (Project_wortel < 0 || Project_wortel > 2) return -22;
        int muur_VALUE = Project_wortel == 0 ? 0 : (Project_wortel == 1 ? lêer_plaas[기술] : Geheue_lêerstelsel.verstel_Lys[teiken[기술]]);
        if (OFFSET_VALUE > 0 && muur_VALUE > 2147483647 - OFFSET_VALUE) return -75;
        if (OFFSET_VALUE < 0 && OFFSET_VALUE < -muur_VALUE) return -22;
        lêer_plaas[기술] = muur_VALUE + OFFSET_VALUE;
        return lêer_plaas[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean toeken_VALUE, int Instellings) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return toeken_VALUE ? -9 : -22;
        if (toeken_VALUE && 서술자 == 새서술자) return 새서술자;
        if (toeken_VALUE) { if (skep_handvatsel[새서술자] != 0) sluit_lêer(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        skep_handvatsel[새서술자] = 기술 + 1; 서술자설정[새서술자] = Instellings; Naslaan_COUNT[기술]++;
        return 새서술자;
    }
    static int verwyder_lêer_inskrywing_naam(int naam_adres) {
        int lengte_VALUE = 경로읽기(naam_adres);
        if (lengte_VALUE < 0) return lengte_VALUE;
        int Lêer = Geheue_lêerstelsel.FIND_inskrywing(pad_naam, lengte_VALUE);
        if (Lêer < 0) return Lêer;
        Geheue_lêerstelsel.이름들[Lêer * 64] = 0;
        return 0;
    }
    static int stel_lêer_lengte(int 서술자, int lengte_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (skep_Instellings[기술] & 3) == 0 || lengte_VALUE < 0) return -22;
        if (lengte_VALUE > Geheue_lêerstelsel.최대크기) return -27;
        int Lêer = teiken[기술], adres = mobiel_VALUE.lêer_Geheue() + Lêer * Geheue_lêerstelsel.최대크기;
        for (int INDEX = Geheue_lêerstelsel.verstel_Lys[Lêer]; INDEX < lengte_VALUE; INDEX++) mobiel_VALUE.skryf_Geheue(adres + INDEX, 0);
        Geheue_lêerstelsel.verstel_Lys[Lêer] = lengte_VALUE;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int adres) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.snit(adres, 48)) return -14;
        for (int INDEX = 0; INDEX < 12; INDEX++) 실행관리.수쓰기(adres + INDEX * 4, 0);
        int Lêer = teiken[기술], Grootte = 종류[기술] == 2 ? Geheue_lêerstelsel.verstel_Lys[Lêer] : 0;
        int 허가 = 종류[기술] == 2 ? Geheue_lêerstelsel.허가들[Lêer] : 438;
        실행관리.수쓰기(adres, 1);
        실행관리.수쓰기(adres + 4, 종류[기술] == 2 ? Lêer + 1 : 100 + 기술);
        실행관리.수쓰기(adres + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(adres + 12, 종류[기술] == 2 && Geheue_lêerstelsel.이름들[Lêer * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(adres + 28, Grootte); 실행관리.수쓰기(adres + 32, 512);
        실행관리.수쓰기(adres + 36, (Grootte + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int Opdrag, int VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Opdrag == 0 || Opdrag == 1030) return 서술자복제(서술자, VALUE, false, Opdrag == 1030 ? 1 : 0);
        if (Opdrag == 1) return 서술자설정[서술자];
        if (Opdrag == 2) { if ((VALUE & ~1) != 0) return -22; 서술자설정[서술자] = VALUE; return 0; }
        if (Opdrag == 3) return skep_Instellings[기술];
        if (Opdrag == 4) {
            if ((VALUE & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            skep_Instellings[기술] = (skep_Instellings[기술] & 3) | (VALUE & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int 통신종단점만들기(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = leeg_handvatsel();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Koppel(서술자, 기술, 3, 0, lees_skryf_vlag);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int adres_32(int adres) {
        return mobiel_VALUE.기억읽기(adres) << 24 | mobiel_VALUE.기억읽기(adres + 1) << 16
            | mobiel_VALUE.기억읽기(adres + 2) << 8 | mobiel_VALUE.기억읽기(adres + 3);
    }
    static int tjek_adres(int adres, int lengte_VALUE) {
        if (lengte_VALUE < 16) return -22;
        if (!실행관리.snit(adres, 16)) return -14;
        return 실행관리.짧은수(adres) == 2 ? 0 : -97;
    }
    static int BIND_adres(int 서술자, int adres, int lengte_VALUE) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int maatreël = tjek_adres(adres, lengte_VALUE);
        if (maatreël < 0) return maatreël;
        if (Netwerk_handvatsel[기술] != 0) return -22;
        int Netwerk_adres = adres_32(adres + 4);
        if (Netwerk_adres != 0 && Netwerk_adres != Netwerk_Stapel.내주소) return -99;
        int 접속번호 = mobiel_VALUE.기억읽기(adres + 2) << 8 | mobiel_VALUE.기억읽기(adres + 3);
        maatreël = Netwerk_Stapel.skep(접속번호);
        if (maatreël < 0) return maatreël;
        Netwerk_handvatsel[기술] = maatreël; teiken[기술] = Netwerk_adres;
        return 0;
    }
    static int Outo_BIND(int 기술) {
        if (Netwerk_handvatsel[기술] != 0) return 0;
        int maatreël = Netwerk_Stapel.skep(0);
        if (maatreël < 0) return maatreël;
        Netwerk_handvatsel[기술] = maatreël;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 요청 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int data_adres, int lengte_VALUE, int Instellings, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Instellings != 0) return -95;
        if (lengte_VALUE < 0 || lengte_VALUE > 1024) return -90;
        if (lengte_VALUE != 0 && !실행관리.snit(data_adres, lengte_VALUE)) return -14;
        if (!실행관리.snit(요청주소, 8)) return -14;
        int adres = 실행관리.수(요청주소);
        int maatreël = tjek_adres(adres, 실행관리.수(요청주소 + 4));
        if (maatreël < 0) return maatreël;
        int 접속번호 = mobiel_VALUE.기억읽기(adres + 2) << 8 | mobiel_VALUE.기억읽기(adres + 3);
        if (접속번호 == 0) return -22;
        maatreël = Outo_BIND(기술);
        if (maatreël < 0) return maatreël;
        for (int INDEX = 0; INDEX < lengte_VALUE; INDEX++) oordra_data[INDEX] = mobiel_VALUE.기억읽기(data_adres + INDEX);
        return Netwerk_Stapel.e_pos(Netwerk_handvatsel[기술], adres_32(adres + 4), 접속번호, oordra_data, lengte_VALUE);
    }
    static void skryf_adres(int adres, int lengte_VALUE, int Netwerk_adres, int 접속번호) {
        for (int INDEX = 0; INDEX < lengte_VALUE && INDEX < 16; INDEX++) {
            int VALUE = 0;
            if (INDEX == 0) VALUE = 2;
            if (INDEX == 2) VALUE = 접속번호 >>> 8;
            if (INDEX == 3) VALUE = 접속번호;
            if (INDEX >= 4 && INDEX < 8) VALUE = Netwerk_adres >>> (56 - INDEX * 8);
            mobiel_VALUE.skryf_Geheue(adres + INDEX, VALUE & 255);
        }
    }
    static int 자료전문받기(int 서술자, int data_adres, int lengte_VALUE, int Instellings, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Instellings & ~64) != 0) return -95;
        if (lengte_VALUE < 0) return -22;
        if (lengte_VALUE != 0 && !실행관리.snit(data_adres, lengte_VALUE)) return -14;
        int adres = 0, adres_lengte_adres = 0, adres_lengte = 0;
        if (요청주소 != 0) {
            if (!실행관리.snit(요청주소, 8)) return -14;
            adres = 실행관리.수(요청주소); adres_lengte_adres = 실행관리.수(요청주소 + 4);
            if (adres != 0) {
                if (!실행관리.snit(adres_lengte_adres, 4)) return -14;
                adres_lengte = 실행관리.수(adres_lengte_adres);
                if (adres_lengte < 0) return -22;
                if (!실행관리.snit(adres, adres_lengte < 16 ? adres_lengte : 16)) return -14;
            }
        }
        int maatreël = Outo_BIND(기술);
        if (maatreël < 0) return maatreël;
        int Loop = mobiel_VALUE.밀리초();
        while (true) {
            maatreël = Netwerk_Stapel.받기(Netwerk_handvatsel[기술], oordra_data, 1024, 0);
            if (maatreël != -11) break;
            if ((Instellings & 64) != 0 || (skep_Instellings[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && mobiel_VALUE.밀리초() - Loop >= 수신대기밀리초[기술]) return -11;
            if (mobiel_VALUE.사용자남은밀리초() <= 10) return -11;
            mobiel_VALUE.잠시양보();
        }
        if (maatreël < 0) return maatreël;
        if (maatreël > lengte_VALUE) maatreël = lengte_VALUE;
        for (int INDEX = 0; INDEX < maatreël; INDEX++) mobiel_VALUE.skryf_Geheue(data_adres + INDEX, oordra_data[INDEX]);
        if (adres != 0) {
            skryf_adres(adres, adres_lengte, Netwerk_Stapel.portuur_adres(Netwerk_handvatsel[기술]), Netwerk_Stapel.상대접속번호(Netwerk_handvatsel[기술]));
            실행관리.수쓰기(adres_lengte_adres, 16);
        }
        return maatreël;
    }
    static int 통신주소읽기(int 서술자, int adres, int lengte_adres) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.snit(lengte_adres, 4)) return -14;
        int lengte_VALUE = 실행관리.수(lengte_adres);
        if (lengte_VALUE < 0) return -22;
        if (!실행관리.snit(adres, lengte_VALUE < 16 ? lengte_VALUE : 16)) return -14;
        int gleuf_inskrywing = Netwerk_Stapel.INDEX(Netwerk_handvatsel[기술]);
        skryf_adres(adres, lengte_VALUE, teiken[기술], gleuf_inskrywing < 0 ? 0 : Netwerk_Stapel.접속번호들[gleuf_inskrywing]);
        실행관리.수쓰기(lengte_adres, 16);
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
