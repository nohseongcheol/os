// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 naudotojas 과정의 파일서술자와 열린 Failas 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int 읽기쓰기 = 2, kurti_įrašas = 64, 독점생성 = 128, apmokėti_Turinys = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] kurti_rodyklė = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], tikslas = new int[서술자한도];
    static int[] Failas_padėtis = new int[서술자한도], kurti_Parametrai = new int[서술자한도], nuoroda_COUNT = new int[서술자한도];
    static int[] tinklas_rodyklė = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] kelias_pavadinimas = new int[64], perduoti_duomenys = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return kurti_rodyklė[파일서술자] - 1;
    }
    static int 빈서술자(int Paleisti) {
        for (int INDEX = Paleisti; INDEX < 서술자한도; INDEX++) if (kurti_rodyklė[INDEX] == 0) return INDEX;
        return -24;
    }
    static int 빈기술() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (nuoroda_COUNT[INDEX] == 0) return INDEX;
        return -24;
    }
    static int Prisijungti(int 서술자, int 기술, int 파일종류, int Failas_tikslas, int Nustatymai) {
        kurti_rodyklė[서술자] = 기술 + 1; 서술자설정[서술자] = (Nustatymai & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; tikslas[기술] = Failas_tikslas; nuoroda_COUNT[기술] = 1;
        kurti_Parametrai[기술] = Nustatymai & (3 | 이어쓰기 | 기다리지않기); Failas_padėtis[기술] = 0;
        tinklas_rodyklė[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void Start_Procesas() {
        CLEAN_Procesas();
        for (int INDEX = 0; INDEX < 3; INDEX++) Prisijungti(INDEX, INDEX, 1, INDEX, INDEX == 0 ? 0 : 1);
    }
    static void CLEAN_Procesas() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (kurti_rodyklė[INDEX] != 0) Uždaryti_Failas(INDEX);
    }
    static int Uždaryti_Failas(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        kurti_rodyklė[서술자] = 0; 서술자설정[서술자] = 0;
        nuoroda_COUNT[기술]--;
        if (nuoroda_COUNT[기술] == 0) {
            if (종류[기술] == 2) atmintis_failų_sistema.kurti_COUNT[tikslas[기술]]--;
            if (종류[기술] == 3 && tinklas_rodyklė[기술] != 0) tinklas_eilė.Užverti(tinklas_rodyklė[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 baitas_VALUE 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int ADDRESS) {
        if (!실행관리.klipas(ADDRESS, 1)) return -14;
        int Pozicija = įrenginys_VALUE.기억읽기(ADDRESS) == '/' ? 1 : 0;
        for (int 길이 = 0; 길이 < 64; 길이++) {
            if (!실행관리.klipas(ADDRESS + Pozicija + 길이, 1)) return -14;
            int VALUE = įrenginys_VALUE.기억읽기(ADDRESS + Pozicija + 길이);
            kelias_pavadinimas[길이] = VALUE;
            if (VALUE == 0) return 길이 == 0 ? -2 : (atmintis_failų_sistema.čekis_pavadinimas(kelias_pavadinimas, 길이) ? 길이 : -22);
            if (VALUE == '/') return -20;
        }
        return -36;
    }
    static int kurti_Failas(int pavadinimas_ADDRESS, int Nustatymai, int 허가) {
        int 길이 = 경로읽기(pavadinimas_ADDRESS);
        if (길이 < 0) return 길이;
        if ((Nustatymai & ~(3 | kurti_įrašas | 독점생성 | apmokėti_Turinys | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Nustatymai & 3) == 3 || ((Nustatymai & apmokėti_Turinys) != 0 && (Nustatymai & 3) == 0)) return -22;
        int Failas = atmintis_failų_sistema.FIND_įrašas(kelias_pavadinimas, 길이);
        if (Failas >= 0 && (Nustatymai & (kurti_įrašas | 독점생성)) == (kurti_įrašas | 독점생성)) return -17;
        if (Failas == -2 && (Nustatymai & kurti_įrašas) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = 빈기술();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Failas == -2) {
            int REZULTATAS = atmintis_failų_sistema.Store_VALUE(kelias_pavadinimas, 길이, kelias_pavadinimas, 0);
            if (REZULTATAS < 0) return REZULTATAS;
            Failas = atmintis_failų_sistema.FIND_įrašas(kelias_pavadinimas, 길이);
            atmintis_failų_sistema.허가들[Failas] = 허가 & 511;
        }
        if (Failas < 0) return Failas;
        if ((Nustatymai & apmokėti_Turinys) != 0) atmintis_failų_sistema.dydis_Sąrašas[Failas] = 0;
        atmintis_failų_sistema.kurti_COUNT[Failas]++;
        return Prisijungti(서술자, 기술, 2, Failas, Nustatymai);
    }
    static int 파일읽기(int 서술자, int duomenys_ADDRESS, int 길이) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (kurti_Parametrai[기술] & 3) == 1) return -9;
        if (길이 < 0) return -22;
        if (길이 == 0) return 0;
        if (!실행관리.klipas(duomenys_ADDRESS, 길이)) return -14;
        if (종류[기술] == 3) return gauti_paketų_kelio_schema_duomenys(서술자, duomenys_ADDRESS, 길이, 0, 0);
        if (종류[기술] == 1) {
            int RECEIVED_COUNT = 0;
            while (RECEIVED_COUNT < 길이) {
                int VALUE = SMS_Terminalas.직렬읽기();
                if (VALUE < 0) VALUE = klaviatūra.Skaitymas();
                if (VALUE < 0) {
                    if (RECEIVED_COUNT > 0) return RECEIVED_COUNT;
                    if ((kurti_Parametrai[기술] & 기다리지않기) != 0) return -11;
                    if (įrenginys_VALUE.사용자남은밀리초() <= 10) return -11;
                    tinklas_eilė.patvirtinti(); įrenginys_VALUE.잠시양보();
                } else {
                    įrenginys_VALUE.rašymas_atmintis(duomenys_ADDRESS + RECEIVED_COUNT, VALUE); RECEIVED_COUNT++;
                }
            }
            return RECEIVED_COUNT;
        }
        int Failas = tikslas[기술], Pozicija = Failas_padėtis[기술];
        if (Pozicija >= atmintis_failų_sistema.dydis_Sąrašas[Failas]) return 0;
        if (길이 > atmintis_failų_sistema.dydis_Sąrašas[Failas] - Pozicija) 길이 = atmintis_failų_sistema.dydis_Sąrašas[Failas] - Pozicija;
        int 원본주소 = įrenginys_VALUE.Failas_atmintis() + Failas * atmintis_failų_sistema.최대크기 + Pozicija;
        for (int INDEX = 0; INDEX < 길이; INDEX++) įrenginys_VALUE.rašymas_atmintis(duomenys_ADDRESS + INDEX, įrenginys_VALUE.기억읽기(원본주소 + INDEX));
        Failas_padėtis[기술] += 길이;
        return 길이;
    }
    static int rašymas_Failas(int 서술자, int duomenys_ADDRESS, int 길이) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (kurti_Parametrai[기술] & 3) == 0) return -9;
        if (길이 < 0) return -22;
        if (길이 == 0) return 0;
        if (!실행관리.klipas(duomenys_ADDRESS, 길이)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 vieta_VALUE 주소가 필요하다.
        if (종류[기술] == 1) {
            if (길이 > 16384) 길이 = 16384;
            for (int INDEX = 0; INDEX < 길이; INDEX++) {
                int VALUE = įrenginys_VALUE.기억읽기(duomenys_ADDRESS + INDEX);
                SMS_Terminalas.직렬바이트(VALUE); SMS_Terminalas.화면문자(VALUE);
            }
            return 길이;
        }
        int Failas = tikslas[기술], Dydis = atmintis_failų_sistema.dydis_Sąrašas[Failas];
        int Pozicija = (kurti_Parametrai[기술] & 이어쓰기) != 0 ? Dydis : Failas_padėtis[기술];
        if (Pozicija >= atmintis_failų_sistema.최대크기) return -27;
        if (길이 > atmintis_failų_sistema.최대크기 - Pozicija) 길이 = atmintis_failų_sistema.최대크기 - Pozicija;
        int vieta_ADDRESS = įrenginys_VALUE.Failas_atmintis() + Failas * atmintis_failų_sistema.최대크기;
        for (int INDEX = Dydis; INDEX < Pozicija; INDEX++) įrenginys_VALUE.rašymas_atmintis(vieta_ADDRESS + INDEX, 0);
        for (int INDEX = 0; INDEX < 길이; INDEX++) įrenginys_VALUE.rašymas_atmintis(vieta_ADDRESS + Pozicija + INDEX, įrenginys_VALUE.기억읽기(duomenys_ADDRESS + INDEX));
        Failas_padėtis[기술] = Pozicija + 길이;
        if (Pozicija + 길이 > Dydis) atmintis_failų_sistema.dydis_Sąrašas[Failas] = Pozicija + 길이;
        return 길이;
    }
    static int ieškoti_Failas(int 서술자, int OFFSET_VALUE, int Project_šaknis) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (Project_šaknis < 0 || Project_šaknis > 2) return -22;
        int Fonas_VALUE = Project_šaknis == 0 ? 0 : (Project_šaknis == 1 ? Failas_padėtis[기술] : atmintis_failų_sistema.dydis_Sąrašas[tikslas[기술]]);
        if (OFFSET_VALUE > 0 && Fonas_VALUE > 2147483647 - OFFSET_VALUE) return -75;
        if (OFFSET_VALUE < 0 && OFFSET_VALUE < -Fonas_VALUE) return -22;
        Failas_padėtis[기술] = Fonas_VALUE + OFFSET_VALUE;
        return Failas_padėtis[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean Priskirti_VALUE, int Nustatymai) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return Priskirti_VALUE ? -9 : -22;
        if (Priskirti_VALUE && 서술자 == 새서술자) return 새서술자;
        if (Priskirti_VALUE) { if (kurti_rodyklė[새서술자] != 0) Uždaryti_Failas(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        kurti_rodyklė[새서술자] = 기술 + 1; 서술자설정[새서술자] = Nustatymai; nuoroda_COUNT[기술]++;
        return 새서술자;
    }
    static int pašalinti_Failas_įrašas_pavadinimas(int pavadinimas_ADDRESS) {
        int 길이 = 경로읽기(pavadinimas_ADDRESS);
        if (길이 < 0) return 길이;
        int Failas = atmintis_failų_sistema.FIND_įrašas(kelias_pavadinimas, 길이);
        if (Failas < 0) return Failas;
        atmintis_failų_sistema.이름들[Failas * 64] = 0;
        return 0;
    }
    static int 파일길이정하기(int 서술자, int 길이) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (kurti_Parametrai[기술] & 3) == 0 || 길이 < 0) return -22;
        if (길이 > atmintis_failų_sistema.최대크기) return -27;
        int Failas = tikslas[기술], ADDRESS = įrenginys_VALUE.Failas_atmintis() + Failas * atmintis_failų_sistema.최대크기;
        for (int INDEX = atmintis_failų_sistema.dydis_Sąrašas[Failas]; INDEX < 길이; INDEX++) įrenginys_VALUE.rašymas_atmintis(ADDRESS + INDEX, 0);
        atmintis_failų_sistema.dydis_Sąrašas[Failas] = 길이;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int ADDRESS) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.klipas(ADDRESS, 48)) return -14;
        for (int INDEX = 0; INDEX < 12; INDEX++) 실행관리.rašymas_numeris(ADDRESS + INDEX * 4, 0);
        int Failas = tikslas[기술], Dydis = 종류[기술] == 2 ? atmintis_failų_sistema.dydis_Sąrašas[Failas] : 0;
        int 허가 = 종류[기술] == 2 ? atmintis_failų_sistema.허가들[Failas] : 438;
        실행관리.rašymas_numeris(ADDRESS, 1);
        실행관리.rašymas_numeris(ADDRESS + 4, 종류[기술] == 2 ? Failas + 1 : 100 + 기술);
        실행관리.rašymas_numeris(ADDRESS + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.rašymas_numeris(ADDRESS + 12, 종류[기술] == 2 && atmintis_failų_sistema.이름들[Failas * 64] == 0 ? 0 : 1);
        실행관리.rašymas_numeris(ADDRESS + 28, Dydis); 실행관리.rašymas_numeris(ADDRESS + 32, 512);
        실행관리.rašymas_numeris(ADDRESS + 36, (Dydis + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int Komanda, int VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Komanda == 0 || Komanda == 1030) return 서술자복제(서술자, VALUE, false, Komanda == 1030 ? 1 : 0);
        if (Komanda == 1) return 서술자설정[서술자];
        if (Komanda == 2) { if ((VALUE & ~1) != 0) return -22; 서술자설정[서술자] = VALUE; return 0; }
        if (Komanda == 3) return kurti_Parametrai[기술];
        if (Komanda == 4) {
            if ((VALUE & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            kurti_Parametrai[기술] = (kurti_Parametrai[기술] & 3) | (VALUE & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int kurti_dalyvis(int 주소체계, int 통신종류, int atvejis_numeris) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (atvejis_numeris != 0 && atvejis_numeris != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = 빈기술();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Prisijungti(서술자, 기술, 3, 0, 읽기쓰기);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int ADDRESS_32(int ADDRESS) {
        return įrenginys_VALUE.기억읽기(ADDRESS) << 24 | įrenginys_VALUE.기억읽기(ADDRESS + 1) << 16
            | įrenginys_VALUE.기억읽기(ADDRESS + 2) << 8 | įrenginys_VALUE.기억읽기(ADDRESS + 3);
    }
    static int čekis_ADDRESS(int ADDRESS, int 길이) {
        if (길이 < 16) return -22;
        if (!실행관리.klipas(ADDRESS, 16)) return -14;
        return 실행관리.짧은수(ADDRESS) == 2 ? 0 : -97;
    }
    static int BIND_ADDRESS(int 서술자, int ADDRESS, int 길이) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int REZULTATAS = čekis_ADDRESS(ADDRESS, 길이);
        if (REZULTATAS < 0) return REZULTATAS;
        if (tinklas_rodyklė[기술] != 0) return -22;
        int tinklo_identifikatorius = ADDRESS_32(ADDRESS + 4);
        if (tinklo_identifikatorius != 0 && tinklo_identifikatorius != tinklas_eilė.내주소) return -99;
        int prievado_numeris = įrenginys_VALUE.기억읽기(ADDRESS + 2) << 8 | įrenginys_VALUE.기억읽기(ADDRESS + 3);
        REZULTATAS = tinklas_eilė.Atverti(prievado_numeris);
        if (REZULTATAS < 0) return REZULTATAS;
        tinklas_rodyklė[기술] = REZULTATAS; tikslas[기술] = tinklo_identifikatorius;
        return 0;
    }
    static int Automatinis_režimas_BIND(int 기술) {
        if (tinklas_rodyklė[기술] != 0) return 0;
        int REZULTATAS = tinklas_eilė.Atverti(0);
        if (REZULTATAS < 0) return REZULTATAS;
        tinklas_rodyklė[기술] = REZULTATAS;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 užklausa 구조체로 전달한다.
    static int siųsti_paketų_kelio_schema_duomenys(int 서술자, int duomenys_ADDRESS, int 길이, int Nustatymai, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Nustatymai != 0) return -95;
        if (길이 < 0 || 길이 > 1024) return -90;
        if (길이 != 0 && !실행관리.klipas(duomenys_ADDRESS, 길이)) return -14;
        if (!실행관리.klipas(요청주소, 8)) return -14;
        int ADDRESS = 실행관리.numeris(요청주소);
        int REZULTATAS = čekis_ADDRESS(ADDRESS, 실행관리.numeris(요청주소 + 4));
        if (REZULTATAS < 0) return REZULTATAS;
        int prievado_numeris = įrenginys_VALUE.기억읽기(ADDRESS + 2) << 8 | įrenginys_VALUE.기억읽기(ADDRESS + 3);
        if (prievado_numeris == 0) return -22;
        REZULTATAS = Automatinis_režimas_BIND(기술);
        if (REZULTATAS < 0) return REZULTATAS;
        for (int INDEX = 0; INDEX < 길이; INDEX++) perduoti_duomenys[INDEX] = įrenginys_VALUE.기억읽기(duomenys_ADDRESS + INDEX);
        return tinklas_eilė.siųsti(tinklas_rodyklė[기술], ADDRESS_32(ADDRESS + 4), prievado_numeris, perduoti_duomenys, 길이);
    }
    static void rašymas_ADDRESS(int ADDRESS, int 길이, int tinklo_identifikatorius, int prievado_numeris) {
        for (int INDEX = 0; INDEX < 길이 && INDEX < 16; INDEX++) {
            int VALUE = 0;
            if (INDEX == 0) VALUE = 2;
            if (INDEX == 2) VALUE = prievado_numeris >>> 8;
            if (INDEX == 3) VALUE = prievado_numeris;
            if (INDEX >= 4 && INDEX < 8) VALUE = tinklo_identifikatorius >>> (56 - INDEX * 8);
            įrenginys_VALUE.rašymas_atmintis(ADDRESS + INDEX, VALUE & 255);
        }
    }
    static int gauti_paketų_kelio_schema_duomenys(int 서술자, int duomenys_ADDRESS, int 길이, int Nustatymai, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Nustatymai & ~64) != 0) return -95;
        if (길이 < 0) return -22;
        if (길이 != 0 && !실행관리.klipas(duomenys_ADDRESS, 길이)) return -14;
        int ADDRESS = 0, 주소길이주소 = 0, 주소길이 = 0;
        if (요청주소 != 0) {
            if (!실행관리.klipas(요청주소, 8)) return -14;
            ADDRESS = 실행관리.numeris(요청주소); 주소길이주소 = 실행관리.numeris(요청주소 + 4);
            if (ADDRESS != 0) {
                if (!실행관리.klipas(주소길이주소, 4)) return -14;
                주소길이 = 실행관리.numeris(주소길이주소);
                if (주소길이 < 0) return -22;
                if (!실행관리.klipas(ADDRESS, 주소길이 < 16 ? 주소길이 : 16)) return -14;
            }
        }
        int REZULTATAS = Automatinis_režimas_BIND(기술);
        if (REZULTATAS < 0) return REZULTATAS;
        int Paleisti = įrenginys_VALUE.밀리초();
        while (true) {
            REZULTATAS = tinklas_eilė.gauti(tinklas_rodyklė[기술], perduoti_duomenys, 1024, 0);
            if (REZULTATAS != -11) break;
            if ((Nustatymai & 64) != 0 || (kurti_Parametrai[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && įrenginys_VALUE.밀리초() - Paleisti >= 수신대기밀리초[기술]) return -11;
            if (įrenginys_VALUE.사용자남은밀리초() <= 10) return -11;
            įrenginys_VALUE.잠시양보();
        }
        if (REZULTATAS < 0) return REZULTATAS;
        if (REZULTATAS > 길이) REZULTATAS = 길이;
        for (int INDEX = 0; INDEX < REZULTATAS; INDEX++) įrenginys_VALUE.rašymas_atmintis(duomenys_ADDRESS + INDEX, perduoti_duomenys[INDEX]);
        if (ADDRESS != 0) {
            rašymas_ADDRESS(ADDRESS, 주소길이, tinklas_eilė.lygiavertis_mazgas_ADDRESS(tinklas_rodyklė[기술]), tinklas_eilė.lygiavertis_mazgas_prievado_numeris(tinklas_rodyklė[기술]));
            실행관리.rašymas_numeris(주소길이주소, 16);
        }
        return REZULTATAS;
    }
    static int 통신주소읽기(int 서술자, int ADDRESS, int 길이주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.klipas(길이주소, 4)) return -14;
        int 길이 = 실행관리.numeris(길이주소);
        if (길이 < 0) return -22;
        if (!실행관리.klipas(ADDRESS, 길이 < 16 ? 길이 : 16)) return -14;
        int 칸 = tinklas_eilė.INDEX(tinklas_rodyklė[기술]);
        rašymas_ADDRESS(ADDRESS, 길이, tikslas[기술], 칸 < 0 ? 0 : tinklas_eilė.접속번호들[칸]);
        실행관리.rašymas_numeris(길이주소, 16);
        return 0;
    }
    static int rinkinys_gauti_SKIRTASIS_LAIKAS(int 서술자, int 밀리초) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (밀리초 < 0 || 밀리초 > 2000) return -22;
        수신대기밀리초[기술] = 밀리초;
        return 0;
    }
}
