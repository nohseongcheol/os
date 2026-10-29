// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 defnyddiwr 과정의 파일서술자와 열린 Ffeil 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int darllen_ysgrifennu_fflag = 2, Creu_cofnod = 64, 독점생성 = 128, clirio_Cynnwys = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] agor_dolen = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], targed = new int[서술자한도];
    static int[] ffeil_safle = new int[서술자한도], agor_Gosodiadau = new int[서술자한도], cyfeiriad_COUNT = new int[서술자한도];
    static int[] Rhwydwaith_dolen = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] llwybr_enw = new int[64], trosglwyddo_data = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return agor_dolen[파일서술자] - 1;
    }
    static int 빈서술자(int Gweithredu_2) {
        for (int INDEX = Gweithredu_2; INDEX < 서술자한도; INDEX++) if (agor_dolen[INDEX] == 0) return INDEX;
        return -24;
    }
    static int gwag_dolen() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (cyfeiriad_COUNT[INDEX] == 0) return INDEX;
        return -24;
    }
    static int Cysylltu(int 서술자, int 기술, int 파일종류, int ffeil_targed, int Gosodiadau) {
        agor_dolen[서술자] = 기술 + 1; 서술자설정[서술자] = (Gosodiadau & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; targed[기술] = ffeil_targed; cyfeiriad_COUNT[기술] = 1;
        agor_Gosodiadau[기술] = Gosodiadau & (3 | 이어쓰기 | 기다리지않기); ffeil_safle[기술] = 0;
        Rhwydwaith_dolen[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void START_Proses() {
        Glân_Proses();
        for (int INDEX = 0; INDEX < 3; INDEX++) Cysylltu(INDEX, INDEX, 1, INDEX, INDEX == 0 ? 0 : 1);
    }
    static void Glân_Proses() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (agor_dolen[INDEX] != 0) cau_ffeil(INDEX);
    }
    static int cau_ffeil(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        agor_dolen[서술자] = 0; 서술자설정[서술자] = 0;
        cyfeiriad_COUNT[기술]--;
        if (cyfeiriad_COUNT[기술] == 0) {
            if (종류[기술] == 2) Cof_system_ffeiliau.agor_COUNT[targed[기술]]--;
            if (종류[기술] == 3 && Rhwydwaith_dolen[기술] != 0) Rhwydwaith_pentwr.Cau(Rhwydwaith_dolen[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 beit_VALUE 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int ADDRESS) {
        if (!실행관리.clip(ADDRESS, 1)) return -14;
        int safle = dyfais_VALUE.기억읽기(ADDRESS) == '/' ? 1 : 0;
        for (int hyd_VALUE = 0; hyd_VALUE < 64; hyd_VALUE++) {
            if (!실행관리.clip(ADDRESS + safle + hyd_VALUE, 1)) return -14;
            int VALUE = dyfais_VALUE.기억읽기(ADDRESS + safle + hyd_VALUE);
            llwybr_enw[hyd_VALUE] = VALUE;
            if (VALUE == 0) return hyd_VALUE == 0 ? -2 : (Cof_system_ffeiliau.gwirio_enw(llwybr_enw, hyd_VALUE) ? hyd_VALUE : -22);
            if (VALUE == '/') return -20;
        }
        return -36;
    }
    static int agor_ffeil(int enw_ADDRESS, int Gosodiadau, int 허가) {
        int hyd_VALUE = 경로읽기(enw_ADDRESS);
        if (hyd_VALUE < 0) return hyd_VALUE;
        if ((Gosodiadau & ~(3 | Creu_cofnod | 독점생성 | clirio_Cynnwys | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Gosodiadau & 3) == 3 || ((Gosodiadau & clirio_Cynnwys) != 0 && (Gosodiadau & 3) == 0)) return -22;
        int Ffeil = Cof_system_ffeiliau.FIND_cofnod(llwybr_enw, hyd_VALUE);
        if (Ffeil >= 0 && (Gosodiadau & (Creu_cofnod | 독점생성)) == (Creu_cofnod | 독점생성)) return -17;
        if (Ffeil == -2 && (Gosodiadau & Creu_cofnod) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = gwag_dolen();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Ffeil == -2) {
            int mesur = Cof_system_ffeiliau.Store_VALUE(llwybr_enw, hyd_VALUE, llwybr_enw, 0);
            if (mesur < 0) return mesur;
            Ffeil = Cof_system_ffeiliau.FIND_cofnod(llwybr_enw, hyd_VALUE);
            Cof_system_ffeiliau.허가들[Ffeil] = 허가 & 511;
        }
        if (Ffeil < 0) return Ffeil;
        if ((Gosodiadau & clirio_Cynnwys) != 0) Cof_system_ffeiliau.newid_maint_Rhestr[Ffeil] = 0;
        Cof_system_ffeiliau.agor_COUNT[Ffeil]++;
        return Cysylltu(서술자, 기술, 2, Ffeil, Gosodiadau);
    }
    static int 파일읽기(int 서술자, int data_ADDRESS, int hyd_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (agor_Gosodiadau[기술] & 3) == 1) return -9;
        if (hyd_VALUE < 0) return -22;
        if (hyd_VALUE == 0) return 0;
        if (!실행관리.clip(data_ADDRESS, hyd_VALUE)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, data_ADDRESS, hyd_VALUE, 0, 0);
        if (종류[기술] == 1) {
            int RECEIVED_COUNT = 0;
            while (RECEIVED_COUNT < hyd_VALUE) {
                int VALUE = SMS_Terfynell.직렬읽기();
                if (VALUE < 0) VALUE = allweddell.Darllen();
                if (VALUE < 0) {
                    if (RECEIVED_COUNT > 0) return RECEIVED_COUNT;
                    if ((agor_Gosodiadau[기술] & 기다리지않기) != 0) return -11;
                    if (dyfais_VALUE.사용자남은밀리초() <= 10) return -11;
                    Rhwydwaith_pentwr.dilysu(); dyfais_VALUE.잠시양보();
                } else {
                    dyfais_VALUE.ysgrifennu_Cof(data_ADDRESS + RECEIVED_COUNT, VALUE); RECEIVED_COUNT++;
                }
            }
            return RECEIVED_COUNT;
        }
        int Ffeil = targed[기술], safle = ffeil_safle[기술];
        if (safle >= Cof_system_ffeiliau.newid_maint_Rhestr[Ffeil]) return 0;
        if (hyd_VALUE > Cof_system_ffeiliau.newid_maint_Rhestr[Ffeil] - safle) hyd_VALUE = Cof_system_ffeiliau.newid_maint_Rhestr[Ffeil] - safle;
        int 원본주소 = dyfais_VALUE.ffeil_Cof() + Ffeil * Cof_system_ffeiliau.최대크기 + safle;
        for (int INDEX = 0; INDEX < hyd_VALUE; INDEX++) dyfais_VALUE.ysgrifennu_Cof(data_ADDRESS + INDEX, dyfais_VALUE.기억읽기(원본주소 + INDEX));
        ffeil_safle[기술] += hyd_VALUE;
        return hyd_VALUE;
    }
    static int ysgrifennu_ffeil(int 서술자, int data_ADDRESS, int hyd_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (agor_Gosodiadau[기술] & 3) == 0) return -9;
        if (hyd_VALUE < 0) return -22;
        if (hyd_VALUE == 0) return 0;
        if (!실행관리.clip(data_ADDRESS, hyd_VALUE)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 cyrchfan_VALUE 주소가 필요하다.
        if (종류[기술] == 1) {
            if (hyd_VALUE > 16384) hyd_VALUE = 16384;
            for (int INDEX = 0; INDEX < hyd_VALUE; INDEX++) {
                int VALUE = dyfais_VALUE.기억읽기(data_ADDRESS + INDEX);
                SMS_Terfynell.직렬바이트(VALUE); SMS_Terfynell.화면문자(VALUE);
            }
            return hyd_VALUE;
        }
        int Ffeil = targed[기술], Maint = Cof_system_ffeiliau.newid_maint_Rhestr[Ffeil];
        int safle = (agor_Gosodiadau[기술] & 이어쓰기) != 0 ? Maint : ffeil_safle[기술];
        if (safle >= Cof_system_ffeiliau.최대크기) return -27;
        if (hyd_VALUE > Cof_system_ffeiliau.최대크기 - safle) hyd_VALUE = Cof_system_ffeiliau.최대크기 - safle;
        int cyrchfan_ADDRESS = dyfais_VALUE.ffeil_Cof() + Ffeil * Cof_system_ffeiliau.최대크기;
        for (int INDEX = Maint; INDEX < safle; INDEX++) dyfais_VALUE.ysgrifennu_Cof(cyrchfan_ADDRESS + INDEX, 0);
        for (int INDEX = 0; INDEX < hyd_VALUE; INDEX++) dyfais_VALUE.ysgrifennu_Cof(cyrchfan_ADDRESS + safle + INDEX, dyfais_VALUE.기억읽기(data_ADDRESS + INDEX));
        ffeil_safle[기술] = safle + hyd_VALUE;
        if (safle + hyd_VALUE > Maint) Cof_system_ffeiliau.newid_maint_Rhestr[Ffeil] = safle + hyd_VALUE;
        return hyd_VALUE;
    }
    static int chwilio_ffeil(int 서술자, int OFFSET_VALUE, int prosiect_gwraidd) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (prosiect_gwraidd < 0 || prosiect_gwraidd > 2) return -22;
        int Cefndir_VALUE = prosiect_gwraidd == 0 ? 0 : (prosiect_gwraidd == 1 ? ffeil_safle[기술] : Cof_system_ffeiliau.newid_maint_Rhestr[targed[기술]]);
        if (OFFSET_VALUE > 0 && Cefndir_VALUE > 2147483647 - OFFSET_VALUE) return -75;
        if (OFFSET_VALUE < 0 && OFFSET_VALUE < -Cefndir_VALUE) return -22;
        ffeil_safle[기술] = Cefndir_VALUE + OFFSET_VALUE;
        return ffeil_safle[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean 지정, int Gosodiadau) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return 지정 ? -9 : -22;
        if (지정 && 서술자 == 새서술자) return 새서술자;
        if (지정) { if (agor_dolen[새서술자] != 0) cau_ffeil(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        agor_dolen[새서술자] = 기술 + 1; 서술자설정[새서술자] = Gosodiadau; cyfeiriad_COUNT[기술]++;
        return 새서술자;
    }
    static int tynnu_ffeil_cofnod_enw(int enw_ADDRESS) {
        int hyd_VALUE = 경로읽기(enw_ADDRESS);
        if (hyd_VALUE < 0) return hyd_VALUE;
        int Ffeil = Cof_system_ffeiliau.FIND_cofnod(llwybr_enw, hyd_VALUE);
        if (Ffeil < 0) return Ffeil;
        Cof_system_ffeiliau.이름들[Ffeil * 64] = 0;
        return 0;
    }
    static int set_ffeil_hyd(int 서술자, int hyd_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (agor_Gosodiadau[기술] & 3) == 0 || hyd_VALUE < 0) return -22;
        if (hyd_VALUE > Cof_system_ffeiliau.최대크기) return -27;
        int Ffeil = targed[기술], ADDRESS = dyfais_VALUE.ffeil_Cof() + Ffeil * Cof_system_ffeiliau.최대크기;
        for (int INDEX = Cof_system_ffeiliau.newid_maint_Rhestr[Ffeil]; INDEX < hyd_VALUE; INDEX++) dyfais_VALUE.ysgrifennu_Cof(ADDRESS + INDEX, 0);
        Cof_system_ffeiliau.newid_maint_Rhestr[Ffeil] = hyd_VALUE;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int ADDRESS) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.clip(ADDRESS, 48)) return -14;
        for (int INDEX = 0; INDEX < 12; INDEX++) 실행관리.수쓰기(ADDRESS + INDEX * 4, 0);
        int Ffeil = targed[기술], Maint = 종류[기술] == 2 ? Cof_system_ffeiliau.newid_maint_Rhestr[Ffeil] : 0;
        int 허가 = 종류[기술] == 2 ? Cof_system_ffeiliau.허가들[Ffeil] : 438;
        실행관리.수쓰기(ADDRESS, 1);
        실행관리.수쓰기(ADDRESS + 4, 종류[기술] == 2 ? Ffeil + 1 : 100 + 기술);
        실행관리.수쓰기(ADDRESS + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(ADDRESS + 12, 종류[기술] == 2 && Cof_system_ffeiliau.이름들[Ffeil * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(ADDRESS + 28, Maint); 실행관리.수쓰기(ADDRESS + 32, 512);
        실행관리.수쓰기(ADDRESS + 36, (Maint + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int Gorchymyn, int VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Gorchymyn == 0 || Gorchymyn == 1030) return 서술자복제(서술자, VALUE, false, Gorchymyn == 1030 ? 1 : 0);
        if (Gorchymyn == 1) return 서술자설정[서술자];
        if (Gorchymyn == 2) { if ((VALUE & ~1) != 0) return -22; 서술자설정[서술자] = VALUE; return 0; }
        if (Gorchymyn == 3) return agor_Gosodiadau[기술];
        if (Gorchymyn == 4) {
            if ((VALUE & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            agor_Gosodiadau[기술] = (agor_Gosodiadau[기술] & 3) | (VALUE & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int 통신종단점만들기(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = gwag_dolen();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Cysylltu(서술자, 기술, 3, 0, darllen_ysgrifennu_fflag);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int ADDRESS_32(int ADDRESS) {
        return dyfais_VALUE.기억읽기(ADDRESS) << 24 | dyfais_VALUE.기억읽기(ADDRESS + 1) << 16
            | dyfais_VALUE.기억읽기(ADDRESS + 2) << 8 | dyfais_VALUE.기억읽기(ADDRESS + 3);
    }
    static int gwirio_ADDRESS(int ADDRESS, int hyd_VALUE) {
        if (hyd_VALUE < 16) return -22;
        if (!실행관리.clip(ADDRESS, 16)) return -14;
        return 실행관리.짧은수(ADDRESS) == 2 ? 0 : -97;
    }
    static int BIND_ADDRESS(int 서술자, int ADDRESS, int hyd_VALUE) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int mesur = gwirio_ADDRESS(ADDRESS, hyd_VALUE);
        if (mesur < 0) return mesur;
        if (Rhwydwaith_dolen[기술] != 0) return -22;
        int Rhwydwaith_ADDRESS = ADDRESS_32(ADDRESS + 4);
        if (Rhwydwaith_ADDRESS != 0 && Rhwydwaith_ADDRESS != Rhwydwaith_pentwr.내주소) return -99;
        int rhif_porth = dyfais_VALUE.기억읽기(ADDRESS + 2) << 8 | dyfais_VALUE.기억읽기(ADDRESS + 3);
        mesur = Rhwydwaith_pentwr.Agor(rhif_porth);
        if (mesur < 0) return mesur;
        Rhwydwaith_dolen[기술] = mesur; targed[기술] = Rhwydwaith_ADDRESS;
        return 0;
    }
    static int 자동묶기(int 기술) {
        if (Rhwydwaith_dolen[기술] != 0) return 0;
        int mesur = Rhwydwaith_pentwr.Agor(0);
        if (mesur < 0) return mesur;
        Rhwydwaith_dolen[기술] = mesur;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 cais_HTTP 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int data_ADDRESS, int hyd_VALUE, int Gosodiadau, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Gosodiadau != 0) return -95;
        if (hyd_VALUE < 0 || hyd_VALUE > 1024) return -90;
        if (hyd_VALUE != 0 && !실행관리.clip(data_ADDRESS, hyd_VALUE)) return -14;
        if (!실행관리.clip(요청주소, 8)) return -14;
        int ADDRESS = 실행관리.수(요청주소);
        int mesur = gwirio_ADDRESS(ADDRESS, 실행관리.수(요청주소 + 4));
        if (mesur < 0) return mesur;
        int rhif_porth = dyfais_VALUE.기억읽기(ADDRESS + 2) << 8 | dyfais_VALUE.기억읽기(ADDRESS + 3);
        if (rhif_porth == 0) return -22;
        mesur = 자동묶기(기술);
        if (mesur < 0) return mesur;
        for (int INDEX = 0; INDEX < hyd_VALUE; INDEX++) trosglwyddo_data[INDEX] = dyfais_VALUE.기억읽기(data_ADDRESS + INDEX);
        return Rhwydwaith_pentwr.anfon(Rhwydwaith_dolen[기술], ADDRESS_32(ADDRESS + 4), rhif_porth, trosglwyddo_data, hyd_VALUE);
    }
    static void ysgrifennu_ADDRESS(int ADDRESS, int hyd_VALUE, int Rhwydwaith_ADDRESS, int rhif_porth) {
        for (int INDEX = 0; INDEX < hyd_VALUE && INDEX < 16; INDEX++) {
            int VALUE = 0;
            if (INDEX == 0) VALUE = 2;
            if (INDEX == 2) VALUE = rhif_porth >>> 8;
            if (INDEX == 3) VALUE = rhif_porth;
            if (INDEX >= 4 && INDEX < 8) VALUE = Rhwydwaith_ADDRESS >>> (56 - INDEX * 8);
            dyfais_VALUE.ysgrifennu_Cof(ADDRESS + INDEX, VALUE & 255);
        }
    }
    static int 자료전문받기(int 서술자, int data_ADDRESS, int hyd_VALUE, int Gosodiadau, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Gosodiadau & ~64) != 0) return -95;
        if (hyd_VALUE < 0) return -22;
        if (hyd_VALUE != 0 && !실행관리.clip(data_ADDRESS, hyd_VALUE)) return -14;
        int ADDRESS = 0, ADDRESS_hyd_ADDRESS = 0, ADDRESS_hyd = 0;
        if (요청주소 != 0) {
            if (!실행관리.clip(요청주소, 8)) return -14;
            ADDRESS = 실행관리.수(요청주소); ADDRESS_hyd_ADDRESS = 실행관리.수(요청주소 + 4);
            if (ADDRESS != 0) {
                if (!실행관리.clip(ADDRESS_hyd_ADDRESS, 4)) return -14;
                ADDRESS_hyd = 실행관리.수(ADDRESS_hyd_ADDRESS);
                if (ADDRESS_hyd < 0) return -22;
                if (!실행관리.clip(ADDRESS, ADDRESS_hyd < 16 ? ADDRESS_hyd : 16)) return -14;
            }
        }
        int mesur = 자동묶기(기술);
        if (mesur < 0) return mesur;
        int Gweithredu_2 = dyfais_VALUE.밀리초();
        while (true) {
            mesur = Rhwydwaith_pentwr.받기(Rhwydwaith_dolen[기술], trosglwyddo_data, 1024, 0);
            if (mesur != -11) break;
            if ((Gosodiadau & 64) != 0 || (agor_Gosodiadau[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && dyfais_VALUE.밀리초() - Gweithredu_2 >= 수신대기밀리초[기술]) return -11;
            if (dyfais_VALUE.사용자남은밀리초() <= 10) return -11;
            dyfais_VALUE.잠시양보();
        }
        if (mesur < 0) return mesur;
        if (mesur > hyd_VALUE) mesur = hyd_VALUE;
        for (int INDEX = 0; INDEX < mesur; INDEX++) dyfais_VALUE.ysgrifennu_Cof(data_ADDRESS + INDEX, trosglwyddo_data[INDEX]);
        if (ADDRESS != 0) {
            ysgrifennu_ADDRESS(ADDRESS, ADDRESS_hyd, Rhwydwaith_pentwr.cymar_ADDRESS(Rhwydwaith_dolen[기술]), Rhwydwaith_pentwr.cymar_rhif_porth(Rhwydwaith_dolen[기술]));
            실행관리.수쓰기(ADDRESS_hyd_ADDRESS, 16);
        }
        return mesur;
    }
    static int 통신주소읽기(int 서술자, int ADDRESS, int hyd_ADDRESS) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.clip(hyd_ADDRESS, 4)) return -14;
        int hyd_VALUE = 실행관리.수(hyd_ADDRESS);
        if (hyd_VALUE < 0) return -22;
        if (!실행관리.clip(ADDRESS, hyd_VALUE < 16 ? hyd_VALUE : 16)) return -14;
        int slot_cofnod = Rhwydwaith_pentwr.INDEX(Rhwydwaith_dolen[기술]);
        ysgrifennu_ADDRESS(ADDRESS, hyd_VALUE, targed[기술], slot_cofnod < 0 ? 0 : Rhwydwaith_pentwr.접속번호들[slot_cofnod]);
        실행관리.수쓰기(hyd_ADDRESS, 16);
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
