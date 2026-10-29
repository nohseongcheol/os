// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 brukar 과정의 파일서술자와 열린 Fil 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int lese_og_skrivetilgang_flagg = 2, Opprett_oppføring = 64, 독점생성 = 128, fjerne_Innhald = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] opne_handtak = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], mål = new int[서술자한도];
    static int[] fil_plassere = new int[서술자한도], opne_Innstillingar = new int[서술자한도], Oppslagsverk_COUNT = new int[서술자한도];
    static int[] Nettverk_handtak = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] bane_namn = new int[64], Overfør_data = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return opne_handtak[파일서술자] - 1;
    }
    static int 빈서술자(int Køyr_2) {
        for (int INDEX = Køyr_2; INDEX < 서술자한도; INDEX++) if (opne_handtak[INDEX] == 0) return INDEX;
        return -24;
    }
    static int tom_handtak() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (Oppslagsverk_COUNT[INDEX] == 0) return INDEX;
        return -24;
    }
    static int Kopla_til(int 서술자, int 기술, int 파일종류, int fil_mål, int Innstillingar) {
        opne_handtak[서술자] = 기술 + 1; 서술자설정[서술자] = (Innstillingar & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; mål[기술] = fil_mål; Oppslagsverk_COUNT[기술] = 1;
        opne_Innstillingar[기술] = Innstillingar & (3 | 이어쓰기 | 기다리지않기); fil_plassere[기술] = 0;
        Nettverk_handtak[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void START_Prosess() {
        CLEAN_Prosess();
        for (int INDEX = 0; INDEX < 3; INDEX++) Kopla_til(INDEX, INDEX, 1, INDEX, INDEX == 0 ? 0 : 1);
    }
    static void CLEAN_Prosess() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (opne_handtak[INDEX] != 0) Lukk_fil(INDEX);
    }
    static int Lukk_fil(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        opne_handtak[서술자] = 0; 서술자설정[서술자] = 0;
        Oppslagsverk_COUNT[기술]--;
        if (Oppslagsverk_COUNT[기술] == 0) {
            if (종류[기술] == 2) Minne_filsystem.opne_COUNT[mål[기술]]--;
            if (종류[기술] == 3 && Nettverk_handtak[기술] != 0) Nettverk_Stabel.Lukk(Nettverk_handtak[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 byte_VALUE 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int ADDRESS) {
        if (!실행관리.klipp(ADDRESS, 1)) return -14;
        int Posisjon = mobil_VALUE.기억읽기(ADDRESS) == '/' ? 1 : 0;
        for (int lengd_VALUE = 0; lengd_VALUE < 64; lengd_VALUE++) {
            if (!실행관리.klipp(ADDRESS + Posisjon + lengd_VALUE, 1)) return -14;
            int VALUE = mobil_VALUE.기억읽기(ADDRESS + Posisjon + lengd_VALUE);
            bane_namn[lengd_VALUE] = VALUE;
            if (VALUE == 0) return lengd_VALUE == 0 ? -2 : (Minne_filsystem.sjekk_namn(bane_namn, lengd_VALUE) ? lengd_VALUE : -22);
            if (VALUE == '/') return -20;
        }
        return -36;
    }
    static int opne_fil(int namn_ADDRESS, int Innstillingar, int 허가) {
        int lengd_VALUE = 경로읽기(namn_ADDRESS);
        if (lengd_VALUE < 0) return lengd_VALUE;
        if ((Innstillingar & ~(3 | Opprett_oppføring | 독점생성 | fjerne_Innhald | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Innstillingar & 3) == 3 || ((Innstillingar & fjerne_Innhald) != 0 && (Innstillingar & 3) == 0)) return -22;
        int Fil = Minne_filsystem.Søk_oppføring(bane_namn, lengd_VALUE);
        if (Fil >= 0 && (Innstillingar & (Opprett_oppføring | 독점생성)) == (Opprett_oppføring | 독점생성)) return -17;
        if (Fil == -2 && (Innstillingar & Opprett_oppføring) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = tom_handtak();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Fil == -2) {
            int forretningsmål = Minne_filsystem.Store_VALUE(bane_namn, lengd_VALUE, bane_namn, 0);
            if (forretningsmål < 0) return forretningsmål;
            Fil = Minne_filsystem.Søk_oppføring(bane_namn, lengd_VALUE);
            Minne_filsystem.허가들[Fil] = 허가 & 511;
        }
        if (Fil < 0) return Fil;
        if ((Innstillingar & fjerne_Innhald) != 0) Minne_filsystem.endre_storleik_Liste[Fil] = 0;
        Minne_filsystem.opne_COUNT[Fil]++;
        return Kopla_til(서술자, 기술, 2, Fil, Innstillingar);
    }
    static int 파일읽기(int 서술자, int data_ADDRESS, int lengd_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (opne_Innstillingar[기술] & 3) == 1) return -9;
        if (lengd_VALUE < 0) return -22;
        if (lengd_VALUE == 0) return 0;
        if (!실행관리.klipp(data_ADDRESS, lengd_VALUE)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, data_ADDRESS, lengd_VALUE, 0, 0);
        if (종류[기술] == 1) {
            int RECEIVED_COUNT = 0;
            while (RECEIVED_COUNT < lengd_VALUE) {
                int VALUE = SMS_Terminal.직렬읽기();
                if (VALUE < 0) VALUE = tastatur.Les();
                if (VALUE < 0) {
                    if (RECEIVED_COUNT > 0) return RECEIVED_COUNT;
                    if ((opne_Innstillingar[기술] & 기다리지않기) != 0) return -11;
                    if (mobil_VALUE.사용자남은밀리초() <= 10) return -11;
                    Nettverk_Stabel.stadfeste(); mobil_VALUE.잠시양보();
                } else {
                    mobil_VALUE.skrive_Minne(data_ADDRESS + RECEIVED_COUNT, VALUE); RECEIVED_COUNT++;
                }
            }
            return RECEIVED_COUNT;
        }
        int Fil = mål[기술], Posisjon = fil_plassere[기술];
        if (Posisjon >= Minne_filsystem.endre_storleik_Liste[Fil]) return 0;
        if (lengd_VALUE > Minne_filsystem.endre_storleik_Liste[Fil] - Posisjon) lengd_VALUE = Minne_filsystem.endre_storleik_Liste[Fil] - Posisjon;
        int 원본주소 = mobil_VALUE.fil_Minne() + Fil * Minne_filsystem.최대크기 + Posisjon;
        for (int INDEX = 0; INDEX < lengd_VALUE; INDEX++) mobil_VALUE.skrive_Minne(data_ADDRESS + INDEX, mobil_VALUE.기억읽기(원본주소 + INDEX));
        fil_plassere[기술] += lengd_VALUE;
        return lengd_VALUE;
    }
    static int skrive_fil(int 서술자, int data_ADDRESS, int lengd_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (opne_Innstillingar[기술] & 3) == 0) return -9;
        if (lengd_VALUE < 0) return -22;
        if (lengd_VALUE == 0) return 0;
        if (!실행관리.klipp(data_ADDRESS, lengd_VALUE)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 mål_VALUE 주소가 필요하다.
        if (종류[기술] == 1) {
            if (lengd_VALUE > 16384) lengd_VALUE = 16384;
            for (int INDEX = 0; INDEX < lengd_VALUE; INDEX++) {
                int VALUE = mobil_VALUE.기억읽기(data_ADDRESS + INDEX);
                SMS_Terminal.직렬바이트(VALUE); SMS_Terminal.화면문자(VALUE);
            }
            return lengd_VALUE;
        }
        int Fil = mål[기술], Storleik = Minne_filsystem.endre_storleik_Liste[Fil];
        int Posisjon = (opne_Innstillingar[기술] & 이어쓰기) != 0 ? Storleik : fil_plassere[기술];
        if (Posisjon >= Minne_filsystem.최대크기) return -27;
        if (lengd_VALUE > Minne_filsystem.최대크기 - Posisjon) lengd_VALUE = Minne_filsystem.최대크기 - Posisjon;
        int mål_ADDRESS_08bbd577 = mobil_VALUE.fil_Minne() + Fil * Minne_filsystem.최대크기;
        for (int INDEX = Storleik; INDEX < Posisjon; INDEX++) mobil_VALUE.skrive_Minne(mål_ADDRESS_08bbd577 + INDEX, 0);
        for (int INDEX = 0; INDEX < lengd_VALUE; INDEX++) mobil_VALUE.skrive_Minne(mål_ADDRESS_08bbd577 + Posisjon + INDEX, mobil_VALUE.기억읽기(data_ADDRESS + INDEX));
        fil_plassere[기술] = Posisjon + lengd_VALUE;
        if (Posisjon + lengd_VALUE > Storleik) Minne_filsystem.endre_storleik_Liste[Fil] = Posisjon + lengd_VALUE;
        return lengd_VALUE;
    }
    static int søk_fil(int 서술자, int OFFSET_VALUE, int spegle_rot) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (spegle_rot < 0 || spegle_rot > 2) return -22;
        int bakgrunn_VALUE = spegle_rot == 0 ? 0 : (spegle_rot == 1 ? fil_plassere[기술] : Minne_filsystem.endre_storleik_Liste[mål[기술]]);
        if (OFFSET_VALUE > 0 && bakgrunn_VALUE > 2147483647 - OFFSET_VALUE) return -75;
        if (OFFSET_VALUE < 0 && OFFSET_VALUE < -bakgrunn_VALUE) return -22;
        fil_plassere[기술] = bakgrunn_VALUE + OFFSET_VALUE;
        return fil_plassere[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean Tilordne_VALUE, int Innstillingar) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return Tilordne_VALUE ? -9 : -22;
        if (Tilordne_VALUE && 서술자 == 새서술자) return 새서술자;
        if (Tilordne_VALUE) { if (opne_handtak[새서술자] != 0) Lukk_fil(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        opne_handtak[새서술자] = 기술 + 1; 서술자설정[새서술자] = Innstillingar; Oppslagsverk_COUNT[기술]++;
        return 새서술자;
    }
    static int fjerne_fil_oppføring_namn(int namn_ADDRESS) {
        int lengd_VALUE = 경로읽기(namn_ADDRESS);
        if (lengd_VALUE < 0) return lengd_VALUE;
        int Fil = Minne_filsystem.Søk_oppføring(bane_namn, lengd_VALUE);
        if (Fil < 0) return Fil;
        Minne_filsystem.이름들[Fil * 64] = 0;
        return 0;
    }
    static int sett_fil_lengd(int 서술자, int lengd_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (opne_Innstillingar[기술] & 3) == 0 || lengd_VALUE < 0) return -22;
        if (lengd_VALUE > Minne_filsystem.최대크기) return -27;
        int Fil = mål[기술], ADDRESS = mobil_VALUE.fil_Minne() + Fil * Minne_filsystem.최대크기;
        for (int INDEX = Minne_filsystem.endre_storleik_Liste[Fil]; INDEX < lengd_VALUE; INDEX++) mobil_VALUE.skrive_Minne(ADDRESS + INDEX, 0);
        Minne_filsystem.endre_storleik_Liste[Fil] = lengd_VALUE;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int ADDRESS) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.klipp(ADDRESS, 48)) return -14;
        for (int INDEX = 0; INDEX < 12; INDEX++) 실행관리.수쓰기(ADDRESS + INDEX * 4, 0);
        int Fil = mål[기술], Storleik = 종류[기술] == 2 ? Minne_filsystem.endre_storleik_Liste[Fil] : 0;
        int 허가 = 종류[기술] == 2 ? Minne_filsystem.허가들[Fil] : 438;
        실행관리.수쓰기(ADDRESS, 1);
        실행관리.수쓰기(ADDRESS + 4, 종류[기술] == 2 ? Fil + 1 : 100 + 기술);
        실행관리.수쓰기(ADDRESS + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(ADDRESS + 12, 종류[기술] == 2 && Minne_filsystem.이름들[Fil * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(ADDRESS + 28, Storleik); 실행관리.수쓰기(ADDRESS + 32, 512);
        실행관리.수쓰기(ADDRESS + 36, (Storleik + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int Kommando, int VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Kommando == 0 || Kommando == 1030) return 서술자복제(서술자, VALUE, false, Kommando == 1030 ? 1 : 0);
        if (Kommando == 1) return 서술자설정[서술자];
        if (Kommando == 2) { if ((VALUE & ~1) != 0) return -22; 서술자설정[서술자] = VALUE; return 0; }
        if (Kommando == 3) return opne_Innstillingar[기술];
        if (Kommando == 4) {
            if ((VALUE & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            opne_Innstillingar[기술] = (opne_Innstillingar[기술] & 3) | (VALUE & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int Opprett_endepunkt(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = tom_handtak();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Kopla_til(서술자, 기술, 3, 0, lese_og_skrivetilgang_flagg);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int ADDRESS_32(int ADDRESS) {
        return mobil_VALUE.기억읽기(ADDRESS) << 24 | mobil_VALUE.기억읽기(ADDRESS + 1) << 16
            | mobil_VALUE.기억읽기(ADDRESS + 2) << 8 | mobil_VALUE.기억읽기(ADDRESS + 3);
    }
    static int sjekk_ADDRESS(int ADDRESS, int lengd_VALUE) {
        if (lengd_VALUE < 16) return -22;
        if (!실행관리.klipp(ADDRESS, 16)) return -14;
        return 실행관리.짧은수(ADDRESS) == 2 ? 0 : -97;
    }
    static int BIND_ADDRESS(int 서술자, int ADDRESS, int lengd_VALUE) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int forretningsmål = sjekk_ADDRESS(ADDRESS, lengd_VALUE);
        if (forretningsmål < 0) return forretningsmål;
        if (Nettverk_handtak[기술] != 0) return -22;
        int Nettverk_ADDRESS = ADDRESS_32(ADDRESS + 4);
        if (Nettverk_ADDRESS != 0 && Nettverk_ADDRESS != Nettverk_Stabel.내주소) return -99;
        int portnummer = mobil_VALUE.기억읽기(ADDRESS + 2) << 8 | mobil_VALUE.기억읽기(ADDRESS + 3);
        forretningsmål = Nettverk_Stabel.Opna(portnummer);
        if (forretningsmål < 0) return forretningsmål;
        Nettverk_handtak[기술] = forretningsmål; mål[기술] = Nettverk_ADDRESS;
        return 0;
    }
    static int 자동묶기(int 기술) {
        if (Nettverk_handtak[기술] != 0) return 0;
        int forretningsmål = Nettverk_Stabel.Opna(0);
        if (forretningsmål < 0) return forretningsmål;
        Nettverk_handtak[기술] = forretningsmål;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 요청 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int data_ADDRESS, int lengd_VALUE, int Innstillingar, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Innstillingar != 0) return -95;
        if (lengd_VALUE < 0 || lengd_VALUE > 1024) return -90;
        if (lengd_VALUE != 0 && !실행관리.klipp(data_ADDRESS, lengd_VALUE)) return -14;
        if (!실행관리.klipp(요청주소, 8)) return -14;
        int ADDRESS = 실행관리.수(요청주소);
        int forretningsmål = sjekk_ADDRESS(ADDRESS, 실행관리.수(요청주소 + 4));
        if (forretningsmål < 0) return forretningsmål;
        int portnummer = mobil_VALUE.기억읽기(ADDRESS + 2) << 8 | mobil_VALUE.기억읽기(ADDRESS + 3);
        if (portnummer == 0) return -22;
        forretningsmål = 자동묶기(기술);
        if (forretningsmål < 0) return forretningsmål;
        for (int INDEX = 0; INDEX < lengd_VALUE; INDEX++) Overfør_data[INDEX] = mobil_VALUE.기억읽기(data_ADDRESS + INDEX);
        return Nettverk_Stabel.sende(Nettverk_handtak[기술], ADDRESS_32(ADDRESS + 4), portnummer, Overfør_data, lengd_VALUE);
    }
    static void skrive_ADDRESS(int ADDRESS, int lengd_VALUE, int Nettverk_ADDRESS, int portnummer) {
        for (int INDEX = 0; INDEX < lengd_VALUE && INDEX < 16; INDEX++) {
            int VALUE = 0;
            if (INDEX == 0) VALUE = 2;
            if (INDEX == 2) VALUE = portnummer >>> 8;
            if (INDEX == 3) VALUE = portnummer;
            if (INDEX >= 4 && INDEX < 8) VALUE = Nettverk_ADDRESS >>> (56 - INDEX * 8);
            mobil_VALUE.skrive_Minne(ADDRESS + INDEX, VALUE & 255);
        }
    }
    static int 자료전문받기(int 서술자, int data_ADDRESS, int lengd_VALUE, int Innstillingar, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Innstillingar & ~64) != 0) return -95;
        if (lengd_VALUE < 0) return -22;
        if (lengd_VALUE != 0 && !실행관리.klipp(data_ADDRESS, lengd_VALUE)) return -14;
        int ADDRESS = 0, ADDRESS_lengd_ADDRESS = 0, ADDRESS_lengd = 0;
        if (요청주소 != 0) {
            if (!실행관리.klipp(요청주소, 8)) return -14;
            ADDRESS = 실행관리.수(요청주소); ADDRESS_lengd_ADDRESS = 실행관리.수(요청주소 + 4);
            if (ADDRESS != 0) {
                if (!실행관리.klipp(ADDRESS_lengd_ADDRESS, 4)) return -14;
                ADDRESS_lengd = 실행관리.수(ADDRESS_lengd_ADDRESS);
                if (ADDRESS_lengd < 0) return -22;
                if (!실행관리.klipp(ADDRESS, ADDRESS_lengd < 16 ? ADDRESS_lengd : 16)) return -14;
            }
        }
        int forretningsmål = 자동묶기(기술);
        if (forretningsmål < 0) return forretningsmål;
        int Køyr_2 = mobil_VALUE.밀리초();
        while (true) {
            forretningsmål = Nettverk_Stabel.받기(Nettverk_handtak[기술], Overfør_data, 1024, 0);
            if (forretningsmål != -11) break;
            if ((Innstillingar & 64) != 0 || (opne_Innstillingar[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && mobil_VALUE.밀리초() - Køyr_2 >= 수신대기밀리초[기술]) return -11;
            if (mobil_VALUE.사용자남은밀리초() <= 10) return -11;
            mobil_VALUE.잠시양보();
        }
        if (forretningsmål < 0) return forretningsmål;
        if (forretningsmål > lengd_VALUE) forretningsmål = lengd_VALUE;
        for (int INDEX = 0; INDEX < forretningsmål; INDEX++) mobil_VALUE.skrive_Minne(data_ADDRESS + INDEX, Overfør_data[INDEX]);
        if (ADDRESS != 0) {
            skrive_ADDRESS(ADDRESS, ADDRESS_lengd, Nettverk_Stabel.node_ADDRESS(Nettverk_handtak[기술]), Nettverk_Stabel.node_portnummer(Nettverk_handtak[기술]));
            실행관리.수쓰기(ADDRESS_lengd_ADDRESS, 16);
        }
        return forretningsmål;
    }
    static int 통신주소읽기(int 서술자, int ADDRESS, int lengd_ADDRESS) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.klipp(lengd_ADDRESS, 4)) return -14;
        int lengd_VALUE = 실행관리.수(lengd_ADDRESS);
        if (lengd_VALUE < 0) return -22;
        if (!실행관리.klipp(ADDRESS, lengd_VALUE < 16 ? lengd_VALUE : 16)) return -14;
        int felt_oppføring = Nettverk_Stabel.INDEX(Nettverk_handtak[기술]);
        skrive_ADDRESS(ADDRESS, lengd_VALUE, mål[기술], felt_oppføring < 0 ? 0 : Nettverk_Stabel.접속번호들[felt_oppføring]);
        실행관리.수쓰기(lengd_ADDRESS, 16);
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
