// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 utilizator 과정의 파일서술자와 열린 Fișier 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int citire_scriere_fanion = 2, crea_intrare = 64, 독점생성 = 128, goli_TOC = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] crea_handle = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], țintă = new int[서술자한도];
    static int[] Fișier_poziție = new int[서술자한도], crea_Setări = new int[서술자한도], referință_COUNT = new int[서술자한도];
    static int[] rețea_handle = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] cale_nume = new int[64], Transfer_date = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return crea_handle[파일서술자] - 1;
    }
    static int 빈서술자(int Pornește) {
        for (int INDEX = Pornește; INDEX < 서술자한도; INDEX++) if (crea_handle[INDEX] == 0) return INDEX;
        return -24;
    }
    static int 빈기술() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (referință_COUNT[INDEX] == 0) return INDEX;
        return -24;
    }
    static int Conectează(int 서술자, int 기술, int 파일종류, int Fișier_țintă, int Setări) {
        crea_handle[서술자] = 기술 + 1; 서술자설정[서술자] = (Setări & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; țintă[기술] = Fișier_țintă; referință_COUNT[기술] = 1;
        crea_Setări[기술] = Setări & (3 | 이어쓰기 | 기다리지않기); Fișier_poziție[기술] = 0;
        rețea_handle[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void buta_Proces() {
        CLEAN_Proces();
        for (int INDEX = 0; INDEX < 3; INDEX++) Conectează(INDEX, INDEX, 1, INDEX, INDEX == 0 ? 0 : 1);
    }
    static void CLEAN_Proces() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (crea_handle[INDEX] != 0) închide_Fișier(INDEX);
    }
    static int închide_Fișier(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        crea_handle[서술자] = 0; 서술자설정[서술자] = 0;
        referință_COUNT[기술]--;
        if (referință_COUNT[기술] == 0) {
            if (종류[기술] == 2) Memorie_sistem_de_fișiere.crea_COUNT[țintă[기술]]--;
            if (종류[기술] == 3 && rețea_handle[기술] != 0) rețea_Teanc.Închide(rețea_handle[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 byte_VALUE 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int adresa) {
        if (!실행관리.clip(adresa, 1)) return -14;
        int Poziție = mobil_VALUE.기억읽기(adresa) == '/' ? 1 : 0;
        for (int lungime_VALUE = 0; lungime_VALUE < 64; lungime_VALUE++) {
            if (!실행관리.clip(adresa + Poziție + lungime_VALUE, 1)) return -14;
            int VALUE = mobil_VALUE.기억읽기(adresa + Poziție + lungime_VALUE);
            cale_nume[lungime_VALUE] = VALUE;
            if (VALUE == 0) return lungime_VALUE == 0 ? -2 : (Memorie_sistem_de_fișiere.verifica_nume(cale_nume, lungime_VALUE) ? lungime_VALUE : -22);
            if (VALUE == '/') return -20;
        }
        return -36;
    }
    static int crea_Fișier(int nume_adresa, int Setări, int 허가) {
        int lungime_VALUE = 경로읽기(nume_adresa);
        if (lungime_VALUE < 0) return lungime_VALUE;
        if ((Setări & ~(3 | crea_intrare | 독점생성 | goli_TOC | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Setări & 3) == 3 || ((Setări & goli_TOC) != 0 && (Setări & 3) == 0)) return -22;
        int Fișier = Memorie_sistem_de_fișiere.FIND_intrare(cale_nume, lungime_VALUE);
        if (Fișier >= 0 && (Setări & (crea_intrare | 독점생성)) == (crea_intrare | 독점생성)) return -17;
        if (Fișier == -2 && (Setări & crea_intrare) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = 빈기술();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Fișier == -2) {
            int KR = Memorie_sistem_de_fișiere.Store_VALUE(cale_nume, lungime_VALUE, cale_nume, 0);
            if (KR < 0) return KR;
            Fișier = Memorie_sistem_de_fișiere.FIND_intrare(cale_nume, lungime_VALUE);
            Memorie_sistem_de_fișiere.허가들[Fișier] = 허가 & 511;
        }
        if (Fișier < 0) return Fișier;
        if ((Setări & goli_TOC) != 0) Memorie_sistem_de_fișiere.dimensiona_Listă[Fișier] = 0;
        Memorie_sistem_de_fișiere.crea_COUNT[Fișier]++;
        return Conectează(서술자, 기술, 2, Fișier, Setări);
    }
    static int 파일읽기(int 서술자, int date_adresa, int lungime_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (crea_Setări[기술] & 3) == 1) return -9;
        if (lungime_VALUE < 0) return -22;
        if (lungime_VALUE == 0) return 0;
        if (!실행관리.clip(date_adresa, lungime_VALUE)) return -14;
        if (종류[기술] == 3) return primi_diagramă_informații_date(서술자, date_adresa, lungime_VALUE, 0, 0);
        if (종류[기술] == 1) {
            int RECEIVED_COUNT = 0;
            while (RECEIVED_COUNT < lungime_VALUE) {
                int VALUE = SMS_Terminal.직렬읽기();
                if (VALUE < 0) VALUE = tastatură.Citire();
                if (VALUE < 0) {
                    if (RECEIVED_COUNT > 0) return RECEIVED_COUNT;
                    if ((crea_Setări[기술] & 기다리지않기) != 0) return -11;
                    if (mobil_VALUE.사용자남은밀리초() <= 10) return -11;
                    rețea_Teanc.verifica(); mobil_VALUE.잠시양보();
                } else {
                    mobil_VALUE.scriere_Memorie(date_adresa + RECEIVED_COUNT, VALUE); RECEIVED_COUNT++;
                }
            }
            return RECEIVED_COUNT;
        }
        int Fișier = țintă[기술], Poziție = Fișier_poziție[기술];
        if (Poziție >= Memorie_sistem_de_fișiere.dimensiona_Listă[Fișier]) return 0;
        if (lungime_VALUE > Memorie_sistem_de_fișiere.dimensiona_Listă[Fișier] - Poziție) lungime_VALUE = Memorie_sistem_de_fișiere.dimensiona_Listă[Fișier] - Poziție;
        int 원본주소 = mobil_VALUE.Fișier_Memorie() + Fișier * Memorie_sistem_de_fișiere.최대크기 + Poziție;
        for (int INDEX = 0; INDEX < lungime_VALUE; INDEX++) mobil_VALUE.scriere_Memorie(date_adresa + INDEX, mobil_VALUE.기억읽기(원본주소 + INDEX));
        Fișier_poziție[기술] += lungime_VALUE;
        return lungime_VALUE;
    }
    static int scriere_Fișier(int 서술자, int date_adresa, int lungime_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (crea_Setări[기술] & 3) == 0) return -9;
        if (lungime_VALUE < 0) return -22;
        if (lungime_VALUE == 0) return 0;
        if (!실행관리.clip(date_adresa, lungime_VALUE)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 destinație_VALUE 주소가 필요하다.
        if (종류[기술] == 1) {
            if (lungime_VALUE > 16384) lungime_VALUE = 16384;
            for (int INDEX = 0; INDEX < lungime_VALUE; INDEX++) {
                int VALUE = mobil_VALUE.기억읽기(date_adresa + INDEX);
                SMS_Terminal.직렬바이트(VALUE); SMS_Terminal.화면문자(VALUE);
            }
            return lungime_VALUE;
        }
        int Fișier = țintă[기술], Mărime = Memorie_sistem_de_fișiere.dimensiona_Listă[Fișier];
        int Poziție = (crea_Setări[기술] & 이어쓰기) != 0 ? Mărime : Fișier_poziție[기술];
        if (Poziție >= Memorie_sistem_de_fișiere.최대크기) return -27;
        if (lungime_VALUE > Memorie_sistem_de_fișiere.최대크기 - Poziție) lungime_VALUE = Memorie_sistem_de_fișiere.최대크기 - Poziție;
        int destinație_adresa = mobil_VALUE.Fișier_Memorie() + Fișier * Memorie_sistem_de_fișiere.최대크기;
        for (int INDEX = Mărime; INDEX < Poziție; INDEX++) mobil_VALUE.scriere_Memorie(destinație_adresa + INDEX, 0);
        for (int INDEX = 0; INDEX < lungime_VALUE; INDEX++) mobil_VALUE.scriere_Memorie(destinație_adresa + Poziție + INDEX, mobil_VALUE.기억읽기(date_adresa + INDEX));
        Fișier_poziție[기술] = Poziție + lungime_VALUE;
        if (Poziție + lungime_VALUE > Mărime) Memorie_sistem_de_fișiere.dimensiona_Listă[Fișier] = Poziție + lungime_VALUE;
        return lungime_VALUE;
    }
    static int căuta_Fișier(int 서술자, int OFFSET_VALUE, int Project_rădăcină) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (Project_rădăcină < 0 || Project_rădăcină > 2) return -22;
        int tapet_VALUE = Project_rădăcină == 0 ? 0 : (Project_rădăcină == 1 ? Fișier_poziție[기술] : Memorie_sistem_de_fișiere.dimensiona_Listă[țintă[기술]]);
        if (OFFSET_VALUE > 0 && tapet_VALUE > 2147483647 - OFFSET_VALUE) return -75;
        if (OFFSET_VALUE < 0 && OFFSET_VALUE < -tapet_VALUE) return -22;
        Fișier_poziție[기술] = tapet_VALUE + OFFSET_VALUE;
        return Fișier_poziție[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean atribui_VALUE, int Setări) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return atribui_VALUE ? -9 : -22;
        if (atribui_VALUE && 서술자 == 새서술자) return 새서술자;
        if (atribui_VALUE) { if (crea_handle[새서술자] != 0) închide_Fișier(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        crea_handle[새서술자] = 기술 + 1; 서술자설정[새서술자] = Setări; referință_COUNT[기술]++;
        return 새서술자;
    }
    static int elimina_Fișier_intrare_nume(int nume_adresa) {
        int lungime_VALUE = 경로읽기(nume_adresa);
        if (lungime_VALUE < 0) return lungime_VALUE;
        int Fișier = Memorie_sistem_de_fișiere.FIND_intrare(cale_nume, lungime_VALUE);
        if (Fișier < 0) return Fișier;
        Memorie_sistem_de_fișiere.이름들[Fișier * 64] = 0;
        return 0;
    }
    static int set_Fișier_lungime(int 서술자, int lungime_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (crea_Setări[기술] & 3) == 0 || lungime_VALUE < 0) return -22;
        if (lungime_VALUE > Memorie_sistem_de_fișiere.최대크기) return -27;
        int Fișier = țintă[기술], adresa = mobil_VALUE.Fișier_Memorie() + Fișier * Memorie_sistem_de_fișiere.최대크기;
        for (int INDEX = Memorie_sistem_de_fișiere.dimensiona_Listă[Fișier]; INDEX < lungime_VALUE; INDEX++) mobil_VALUE.scriere_Memorie(adresa + INDEX, 0);
        Memorie_sistem_de_fișiere.dimensiona_Listă[Fișier] = lungime_VALUE;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int adresa) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.clip(adresa, 48)) return -14;
        for (int INDEX = 0; INDEX < 12; INDEX++) 실행관리.수쓰기(adresa + INDEX * 4, 0);
        int Fișier = țintă[기술], Mărime = 종류[기술] == 2 ? Memorie_sistem_de_fișiere.dimensiona_Listă[Fișier] : 0;
        int 허가 = 종류[기술] == 2 ? Memorie_sistem_de_fișiere.허가들[Fișier] : 438;
        실행관리.수쓰기(adresa, 1);
        실행관리.수쓰기(adresa + 4, 종류[기술] == 2 ? Fișier + 1 : 100 + 기술);
        실행관리.수쓰기(adresa + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(adresa + 12, 종류[기술] == 2 && Memorie_sistem_de_fișiere.이름들[Fișier * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(adresa + 28, Mărime); 실행관리.수쓰기(adresa + 32, 512);
        실행관리.수쓰기(adresa + 36, (Mărime + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int Comandă, int VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Comandă == 0 || Comandă == 1030) return 서술자복제(서술자, VALUE, false, Comandă == 1030 ? 1 : 0);
        if (Comandă == 1) return 서술자설정[서술자];
        if (Comandă == 2) { if ((VALUE & ~1) != 0) return -22; 서술자설정[서술자] = VALUE; return 0; }
        if (Comandă == 3) return crea_Setări[기술];
        if (Comandă == 4) {
            if ((VALUE & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            crea_Setări[기술] = (crea_Setări[기술] & 3) | (VALUE & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int crea_participant(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = 빈기술();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Conectează(서술자, 기술, 3, 0, citire_scriere_fanion);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int adresa_32(int adresa) {
        return mobil_VALUE.기억읽기(adresa) << 24 | mobil_VALUE.기억읽기(adresa + 1) << 16
            | mobil_VALUE.기억읽기(adresa + 2) << 8 | mobil_VALUE.기억읽기(adresa + 3);
    }
    static int verifica_adresa(int adresa, int lungime_VALUE) {
        if (lungime_VALUE < 16) return -22;
        if (!실행관리.clip(adresa, 16)) return -14;
        return 실행관리.짧은수(adresa) == 2 ? 0 : -97;
    }
    static int BIND_adresa(int 서술자, int adresa, int lungime_VALUE) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int KR = verifica_adresa(adresa, lungime_VALUE);
        if (KR < 0) return KR;
        if (rețea_handle[기술] != 0) return -22;
        int ID_rețea = adresa_32(adresa + 4);
        if (ID_rețea != 0 && ID_rețea != rețea_Teanc.내주소) return -99;
        int număr_port = mobil_VALUE.기억읽기(adresa + 2) << 8 | mobil_VALUE.기억읽기(adresa + 3);
        KR = rețea_Teanc.Deschide(număr_port);
        if (KR < 0) return KR;
        rețea_handle[기술] = KR; țintă[기술] = ID_rețea;
        return 0;
    }
    static int Auto_BIND(int 기술) {
        if (rețea_handle[기술] != 0) return 0;
        int KR = rețea_Teanc.Deschide(0);
        if (KR < 0) return KR;
        rețea_handle[기술] = KR;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 cerere 구조체로 전달한다.
    static int trimite_diagramă_informații_date(int 서술자, int date_adresa, int lungime_VALUE, int Setări, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Setări != 0) return -95;
        if (lungime_VALUE < 0 || lungime_VALUE > 1024) return -90;
        if (lungime_VALUE != 0 && !실행관리.clip(date_adresa, lungime_VALUE)) return -14;
        if (!실행관리.clip(요청주소, 8)) return -14;
        int adresa = 실행관리.수(요청주소);
        int KR = verifica_adresa(adresa, 실행관리.수(요청주소 + 4));
        if (KR < 0) return KR;
        int număr_port = mobil_VALUE.기억읽기(adresa + 2) << 8 | mobil_VALUE.기억읽기(adresa + 3);
        if (număr_port == 0) return -22;
        KR = Auto_BIND(기술);
        if (KR < 0) return KR;
        for (int INDEX = 0; INDEX < lungime_VALUE; INDEX++) Transfer_date[INDEX] = mobil_VALUE.기억읽기(date_adresa + INDEX);
        return rețea_Teanc.trimite(rețea_handle[기술], adresa_32(adresa + 4), număr_port, Transfer_date, lungime_VALUE);
    }
    static void scriere_adresa(int adresa, int lungime_VALUE, int ID_rețea, int număr_port) {
        for (int INDEX = 0; INDEX < lungime_VALUE && INDEX < 16; INDEX++) {
            int VALUE = 0;
            if (INDEX == 0) VALUE = 2;
            if (INDEX == 2) VALUE = număr_port >>> 8;
            if (INDEX == 3) VALUE = număr_port;
            if (INDEX >= 4 && INDEX < 8) VALUE = ID_rețea >>> (56 - INDEX * 8);
            mobil_VALUE.scriere_Memorie(adresa + INDEX, VALUE & 255);
        }
    }
    static int primi_diagramă_informații_date(int 서술자, int date_adresa, int lungime_VALUE, int Setări, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Setări & ~64) != 0) return -95;
        if (lungime_VALUE < 0) return -22;
        if (lungime_VALUE != 0 && !실행관리.clip(date_adresa, lungime_VALUE)) return -14;
        int adresa = 0, adresa_lungime_adresa = 0, adresa_lungime = 0;
        if (요청주소 != 0) {
            if (!실행관리.clip(요청주소, 8)) return -14;
            adresa = 실행관리.수(요청주소); adresa_lungime_adresa = 실행관리.수(요청주소 + 4);
            if (adresa != 0) {
                if (!실행관리.clip(adresa_lungime_adresa, 4)) return -14;
                adresa_lungime = 실행관리.수(adresa_lungime_adresa);
                if (adresa_lungime < 0) return -22;
                if (!실행관리.clip(adresa, adresa_lungime < 16 ? adresa_lungime : 16)) return -14;
            }
        }
        int KR = Auto_BIND(기술);
        if (KR < 0) return KR;
        int Pornește = mobil_VALUE.밀리초();
        while (true) {
            KR = rețea_Teanc.primi(rețea_handle[기술], Transfer_date, 1024, 0);
            if (KR != -11) break;
            if ((Setări & 64) != 0 || (crea_Setări[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && mobil_VALUE.밀리초() - Pornește >= 수신대기밀리초[기술]) return -11;
            if (mobil_VALUE.사용자남은밀리초() <= 10) return -11;
            mobil_VALUE.잠시양보();
        }
        if (KR < 0) return KR;
        if (KR > lungime_VALUE) KR = lungime_VALUE;
        for (int INDEX = 0; INDEX < KR; INDEX++) mobil_VALUE.scriere_Memorie(date_adresa + INDEX, Transfer_date[INDEX]);
        if (adresa != 0) {
            scriere_adresa(adresa, adresa_lungime, rețea_Teanc.pereche_adresa(rețea_handle[기술]), rețea_Teanc.pereche_număr_port(rețea_handle[기술]));
            실행관리.수쓰기(adresa_lungime_adresa, 16);
        }
        return KR;
    }
    static int 통신주소읽기(int 서술자, int adresa, int lungime_adresa) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.clip(lungime_adresa, 4)) return -14;
        int lungime_VALUE = 실행관리.수(lungime_adresa);
        if (lungime_VALUE < 0) return -22;
        if (!실행관리.clip(adresa, lungime_VALUE < 16 ? lungime_VALUE : 16)) return -14;
        int 칸 = rețea_Teanc.INDEX(rețea_handle[기술]);
        scriere_adresa(adresa, lungime_VALUE, țintă[기술], 칸 < 0 ? 0 : rețea_Teanc.접속번호들[칸]);
        실행관리.수쓰기(lungime_adresa, 16);
        return 0;
    }
    static int set_primi_TIMEOUT(int 서술자, int 밀리초) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (밀리초 < 0 || 밀리초 > 2000) return -22;
        수신대기밀리초[기술] = 밀리초;
        return 0;
    }
}
