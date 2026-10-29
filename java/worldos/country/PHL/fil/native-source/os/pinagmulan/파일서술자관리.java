// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 gumagamit 과정의 파일서술자와 열린 file 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int nababasa_nasusulatan_i_flag = 2, Create_pagpasok = 64, 독점생성 = 128, i_clear_TOC = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] buksan_hawakán = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], layunin = new int[서술자한도];
    static int[] file_posisyon = new int[서술자한도], buksan_Mga_Setting = new int[서술자한도], Sanggunian_COUNT = new int[서술자한도];
    static int[] Network_hawakán = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] path_pangalan = new int[64], lipat_data = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return buksan_hawakán[파일서술자] - 1;
    }
    static int 빈서술자(int run) {
        for (int INDEX = run; INDEX < 서술자한도; INDEX++) if (buksan_hawakán[INDEX] == 0) return INDEX;
        return -24;
    }
    static int walang_laman_hawakán() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (Sanggunian_COUNT[INDEX] == 0) return INDEX;
        return -24;
    }
    static int CONNECT(int 서술자, int 기술, int 파일종류, int file_layunin, int Mga_Setting) {
        buksan_hawakán[서술자] = 기술 + 1; 서술자설정[서술자] = (Mga_Setting & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; layunin[기술] = file_layunin; Sanggunian_COUNT[기술] = 1;
        buksan_Mga_Setting[기술] = Mga_Setting & (3 | 이어쓰기 | 기다리지않기); file_posisyon[기술] = 0;
        Network_hawakán[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void Start_Proseso() {
        CLEAN_Proseso();
        for (int INDEX = 0; INDEX < 3; INDEX++) CONNECT(INDEX, INDEX, 1, INDEX, INDEX == 0 ? 0 : 1);
    }
    static void CLEAN_Proseso() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (buksan_hawakán[INDEX] != 0) isara_file(INDEX);
    }
    static int isara_file(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        buksan_hawakán[서술자] = 0; 서술자설정[서술자] = 0;
        Sanggunian_COUNT[기술]--;
        if (Sanggunian_COUNT[기술] == 0) {
            if (종류[기술] == 2) Memory_sistema_ng_file.buksan_COUNT[layunin[기술]]--;
            if (종류[기술] == 3 && Network_hawakán[기술] != 0) Network_Stack.isara(Network_hawakán[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 byte_VALUE 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int email) {
        if (!실행관리.clip(email, 1)) return -14;
        int posisyon = device_VALUE.기억읽기(email) == '/' ? 1 : 0;
        for (int haba_VALUE = 0; haba_VALUE < 64; haba_VALUE++) {
            if (!실행관리.clip(email + posisyon + haba_VALUE, 1)) return -14;
            int VALUE = device_VALUE.기억읽기(email + posisyon + haba_VALUE);
            path_pangalan[haba_VALUE] = VALUE;
            if (VALUE == 0) return haba_VALUE == 0 ? -2 : (Memory_sistema_ng_file.tseke_pangalan(path_pangalan, haba_VALUE) ? haba_VALUE : -22);
            if (VALUE == '/') return -20;
        }
        return -36;
    }
    static int buksan_file(int pangalan_email, int Mga_Setting, int 허가) {
        int haba_VALUE = 경로읽기(pangalan_email);
        if (haba_VALUE < 0) return haba_VALUE;
        if ((Mga_Setting & ~(3 | Create_pagpasok | 독점생성 | i_clear_TOC | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Mga_Setting & 3) == 3 || ((Mga_Setting & i_clear_TOC) != 0 && (Mga_Setting & 3) == 0)) return -22;
        int file = Memory_sistema_ng_file.FIND_pagpasok(path_pangalan, haba_VALUE);
        if (file >= 0 && (Mga_Setting & (Create_pagpasok | 독점생성)) == (Create_pagpasok | 독점생성)) return -17;
        if (file == -2 && (Mga_Setting & Create_pagpasok) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = walang_laman_hawakán();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (file == -2) {
            int sukat = Memory_sistema_ng_file.Store_VALUE(path_pangalan, haba_VALUE, path_pangalan, 0);
            if (sukat < 0) return sukat;
            file = Memory_sistema_ng_file.FIND_pagpasok(path_pangalan, haba_VALUE);
            Memory_sistema_ng_file.허가들[file] = 허가 & 511;
        }
        if (file < 0) return file;
        if ((Mga_Setting & i_clear_TOC) != 0) Memory_sistema_ng_file.sukat_list[file] = 0;
        Memory_sistema_ng_file.buksan_COUNT[file]++;
        return CONNECT(서술자, 기술, 2, file, Mga_Setting);
    }
    static int 파일읽기(int 서술자, int data_email, int haba_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (buksan_Mga_Setting[기술] & 3) == 1) return -9;
        if (haba_VALUE < 0) return -22;
        if (haba_VALUE == 0) return 0;
        if (!실행관리.clip(data_email, haba_VALUE)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, data_email, haba_VALUE, 0, 0);
        if (종류[기술] == 1) {
            int RECEIVED_COUNT = 0;
            while (RECEIVED_COUNT < haba_VALUE) {
                int VALUE = SMS_Terminal.직렬읽기();
                if (VALUE < 0) VALUE = keyboard.읽기();
                if (VALUE < 0) {
                    if (RECEIVED_COUNT > 0) return RECEIVED_COUNT;
                    if ((buksan_Mga_Setting[기술] & 기다리지않기) != 0) return -11;
                    if (device_VALUE.사용자남은밀리초() <= 10) return -11;
                    Network_Stack.tiyakin_kumpirmahin(); device_VALUE.잠시양보();
                } else {
                    device_VALUE.sumulat_Memory(data_email + RECEIVED_COUNT, VALUE); RECEIVED_COUNT++;
                }
            }
            return RECEIVED_COUNT;
        }
        int file = layunin[기술], posisyon = file_posisyon[기술];
        if (posisyon >= Memory_sistema_ng_file.sukat_list[file]) return 0;
        if (haba_VALUE > Memory_sistema_ng_file.sukat_list[file] - posisyon) haba_VALUE = Memory_sistema_ng_file.sukat_list[file] - posisyon;
        int 원본주소 = device_VALUE.file_Memory() + file * Memory_sistema_ng_file.최대크기 + posisyon;
        for (int INDEX = 0; INDEX < haba_VALUE; INDEX++) device_VALUE.sumulat_Memory(data_email + INDEX, device_VALUE.기억읽기(원본주소 + INDEX));
        file_posisyon[기술] += haba_VALUE;
        return haba_VALUE;
    }
    static int sumulat_file(int 서술자, int data_email, int haba_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (buksan_Mga_Setting[기술] & 3) == 0) return -9;
        if (haba_VALUE < 0) return -22;
        if (haba_VALUE == 0) return 0;
        if (!실행관리.clip(data_email, haba_VALUE)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 patutunguhan_VALUE 주소가 필요하다.
        if (종류[기술] == 1) {
            if (haba_VALUE > 16384) haba_VALUE = 16384;
            for (int INDEX = 0; INDEX < haba_VALUE; INDEX++) {
                int VALUE = device_VALUE.기억읽기(data_email + INDEX);
                SMS_Terminal.직렬바이트(VALUE); SMS_Terminal.화면문자(VALUE);
            }
            return haba_VALUE;
        }
        int file = layunin[기술], sukat_82232621 = Memory_sistema_ng_file.sukat_list[file];
        int posisyon = (buksan_Mga_Setting[기술] & 이어쓰기) != 0 ? sukat_82232621 : file_posisyon[기술];
        if (posisyon >= Memory_sistema_ng_file.최대크기) return -27;
        if (haba_VALUE > Memory_sistema_ng_file.최대크기 - posisyon) haba_VALUE = Memory_sistema_ng_file.최대크기 - posisyon;
        int patutunguhan_email = device_VALUE.file_Memory() + file * Memory_sistema_ng_file.최대크기;
        for (int INDEX = sukat_82232621; INDEX < posisyon; INDEX++) device_VALUE.sumulat_Memory(patutunguhan_email + INDEX, 0);
        for (int INDEX = 0; INDEX < haba_VALUE; INDEX++) device_VALUE.sumulat_Memory(patutunguhan_email + posisyon + INDEX, device_VALUE.기억읽기(data_email + INDEX));
        file_posisyon[기술] = posisyon + haba_VALUE;
        if (posisyon + haba_VALUE > sukat_82232621) Memory_sistema_ng_file.sukat_list[file] = posisyon + haba_VALUE;
        return haba_VALUE;
    }
    static int i_seek_file(int 서술자, int OFFSET_VALUE, int Project_root) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (Project_root < 0 || Project_root > 2) return -22;
        int wallpaper_VALUE = Project_root == 0 ? 0 : (Project_root == 1 ? file_posisyon[기술] : Memory_sistema_ng_file.sukat_list[layunin[기술]]);
        if (OFFSET_VALUE > 0 && wallpaper_VALUE > 2147483647 - OFFSET_VALUE) return -75;
        if (OFFSET_VALUE < 0 && OFFSET_VALUE < -wallpaper_VALUE) return -22;
        file_posisyon[기술] = wallpaper_VALUE + OFFSET_VALUE;
        return file_posisyon[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean italaga_VALUE, int Mga_Setting) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return italaga_VALUE ? -9 : -22;
        if (italaga_VALUE && 서술자 == 새서술자) return 새서술자;
        if (italaga_VALUE) { if (buksan_hawakán[새서술자] != 0) isara_file(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        buksan_hawakán[새서술자] = 기술 + 1; 서술자설정[새서술자] = Mga_Setting; Sanggunian_COUNT[기술]++;
        return 새서술자;
    }
    static int tanggalin_file_pagpasok_pangalan(int pangalan_email) {
        int haba_VALUE = 경로읽기(pangalan_email);
        if (haba_VALUE < 0) return haba_VALUE;
        int file = Memory_sistema_ng_file.FIND_pagpasok(path_pangalan, haba_VALUE);
        if (file < 0) return file;
        Memory_sistema_ng_file.이름들[file * 64] = 0;
        return 0;
    }
    static int set_file_haba(int 서술자, int haba_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (buksan_Mga_Setting[기술] & 3) == 0 || haba_VALUE < 0) return -22;
        if (haba_VALUE > Memory_sistema_ng_file.최대크기) return -27;
        int file = layunin[기술], email = device_VALUE.file_Memory() + file * Memory_sistema_ng_file.최대크기;
        for (int INDEX = Memory_sistema_ng_file.sukat_list[file]; INDEX < haba_VALUE; INDEX++) device_VALUE.sumulat_Memory(email + INDEX, 0);
        Memory_sistema_ng_file.sukat_list[file] = haba_VALUE;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int email) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.clip(email, 48)) return -14;
        for (int INDEX = 0; INDEX < 12; INDEX++) 실행관리.수쓰기(email + INDEX * 4, 0);
        int file = layunin[기술], sukat_82232621 = 종류[기술] == 2 ? Memory_sistema_ng_file.sukat_list[file] : 0;
        int 허가 = 종류[기술] == 2 ? Memory_sistema_ng_file.허가들[file] : 438;
        실행관리.수쓰기(email, 1);
        실행관리.수쓰기(email + 4, 종류[기술] == 2 ? file + 1 : 100 + 기술);
        실행관리.수쓰기(email + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(email + 12, 종류[기술] == 2 && Memory_sistema_ng_file.이름들[file * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(email + 28, sukat_82232621); 실행관리.수쓰기(email + 32, 512);
        실행관리.수쓰기(email + 36, (sukat_82232621 + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int utos, int VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (utos == 0 || utos == 1030) return 서술자복제(서술자, VALUE, false, utos == 1030 ? 1 : 0);
        if (utos == 1) return 서술자설정[서술자];
        if (utos == 2) { if ((VALUE & ~1) != 0) return -22; 서술자설정[서술자] = VALUE; return 0; }
        if (utos == 3) return buksan_Mga_Setting[기술];
        if (utos == 4) {
            if ((VALUE & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            buksan_Mga_Setting[기술] = (buksan_Mga_Setting[기술] & 3) | (VALUE & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int 통신종단점만들기(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = walang_laman_hawakán();
        if (서술자 < 0 || 기술 < 0) return -24;
        return CONNECT(서술자, 기술, 3, 0, nababasa_nasusulatan_i_flag);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int email_32(int email) {
        return device_VALUE.기억읽기(email) << 24 | device_VALUE.기억읽기(email + 1) << 16
            | device_VALUE.기억읽기(email + 2) << 8 | device_VALUE.기억읽기(email + 3);
    }
    static int tseke_email(int email, int haba_VALUE) {
        if (haba_VALUE < 16) return -22;
        if (!실행관리.clip(email, 16)) return -14;
        return 실행관리.짧은수(email) == 2 ? 0 : -97;
    }
    static int BIND_email(int 서술자, int email, int haba_VALUE) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int sukat = tseke_email(email, haba_VALUE);
        if (sukat < 0) return sukat;
        if (Network_hawakán[기술] != 0) return -22;
        int Network_email_df3458bb = email_32(email + 4);
        if (Network_email_df3458bb != 0 && Network_email_df3458bb != Network_Stack.내주소) return -99;
        int numero_ng_port = device_VALUE.기억읽기(email + 2) << 8 | device_VALUE.기억읽기(email + 3);
        sukat = Network_Stack.buksan(numero_ng_port);
        if (sukat < 0) return sukat;
        Network_hawakán[기술] = sukat; layunin[기술] = Network_email_df3458bb;
        return 0;
    }
    static int Auto_BIND(int 기술) {
        if (Network_hawakán[기술] != 0) return 0;
        int sukat = Network_Stack.buksan(0);
        if (sukat < 0) return sukat;
        Network_hawakán[기술] = sukat;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 요청 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int data_email, int haba_VALUE, int Mga_Setting, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Mga_Setting != 0) return -95;
        if (haba_VALUE < 0 || haba_VALUE > 1024) return -90;
        if (haba_VALUE != 0 && !실행관리.clip(data_email, haba_VALUE)) return -14;
        if (!실행관리.clip(요청주소, 8)) return -14;
        int email = 실행관리.수(요청주소);
        int sukat = tseke_email(email, 실행관리.수(요청주소 + 4));
        if (sukat < 0) return sukat;
        int numero_ng_port = device_VALUE.기억읽기(email + 2) << 8 | device_VALUE.기억읽기(email + 3);
        if (numero_ng_port == 0) return -22;
        sukat = Auto_BIND(기술);
        if (sukat < 0) return sukat;
        for (int INDEX = 0; INDEX < haba_VALUE; INDEX++) lipat_data[INDEX] = device_VALUE.기억읽기(data_email + INDEX);
        return Network_Stack.i_email(Network_hawakán[기술], email_32(email + 4), numero_ng_port, lipat_data, haba_VALUE);
    }
    static void sumulat_email(int email, int haba_VALUE, int Network_email_df3458bb, int numero_ng_port) {
        for (int INDEX = 0; INDEX < haba_VALUE && INDEX < 16; INDEX++) {
            int VALUE = 0;
            if (INDEX == 0) VALUE = 2;
            if (INDEX == 2) VALUE = numero_ng_port >>> 8;
            if (INDEX == 3) VALUE = numero_ng_port;
            if (INDEX >= 4 && INDEX < 8) VALUE = Network_email_df3458bb >>> (56 - INDEX * 8);
            device_VALUE.sumulat_Memory(email + INDEX, VALUE & 255);
        }
    }
    static int 자료전문받기(int 서술자, int data_email, int haba_VALUE, int Mga_Setting, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Mga_Setting & ~64) != 0) return -95;
        if (haba_VALUE < 0) return -22;
        if (haba_VALUE != 0 && !실행관리.clip(data_email, haba_VALUE)) return -14;
        int email = 0, email_haba_email = 0, email_haba = 0;
        if (요청주소 != 0) {
            if (!실행관리.clip(요청주소, 8)) return -14;
            email = 실행관리.수(요청주소); email_haba_email = 실행관리.수(요청주소 + 4);
            if (email != 0) {
                if (!실행관리.clip(email_haba_email, 4)) return -14;
                email_haba = 실행관리.수(email_haba_email);
                if (email_haba < 0) return -22;
                if (!실행관리.clip(email, email_haba < 16 ? email_haba : 16)) return -14;
            }
        }
        int sukat = Auto_BIND(기술);
        if (sukat < 0) return sukat;
        int run = device_VALUE.밀리초();
        while (true) {
            sukat = Network_Stack.받기(Network_hawakán[기술], lipat_data, 1024, 0);
            if (sukat != -11) break;
            if ((Mga_Setting & 64) != 0 || (buksan_Mga_Setting[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && device_VALUE.밀리초() - run >= 수신대기밀리초[기술]) return -11;
            if (device_VALUE.사용자남은밀리초() <= 10) return -11;
            device_VALUE.잠시양보();
        }
        if (sukat < 0) return sukat;
        if (sukat > haba_VALUE) sukat = haba_VALUE;
        for (int INDEX = 0; INDEX < sukat; INDEX++) device_VALUE.sumulat_Memory(data_email + INDEX, lipat_data[INDEX]);
        if (email != 0) {
            sumulat_email(email, email_haba, Network_Stack.peer_email(Network_hawakán[기술]), Network_Stack.peer_numero_ng_port(Network_hawakán[기술]));
            실행관리.수쓰기(email_haba_email, 16);
        }
        return sukat;
    }
    static int 통신주소읽기(int 서술자, int email, int haba_email) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.clip(haba_email, 4)) return -14;
        int haba_VALUE = 실행관리.수(haba_email);
        if (haba_VALUE < 0) return -22;
        if (!실행관리.clip(email, haba_VALUE < 16 ? haba_VALUE : 16)) return -14;
        int espasyo_pagpasok = Network_Stack.INDEX(Network_hawakán[기술]);
        sumulat_email(email, haba_VALUE, layunin[기술], espasyo_pagpasok < 0 ? 0 : Network_Stack.접속번호들[espasyo_pagpasok]);
        실행관리.수쓰기(haba_email, 16);
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
