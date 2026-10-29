// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 foydalanuvchi 과정의 파일서술자와 열린 Fayl 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int o_qish_yozish_mumkin_bayroq = 2, Yaratish_kiritish = 64, 독점생성 = 128, tozalamoq_TOC = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] ochmoq_deskriptor = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], nishon = new int[서술자한도];
    static int[] fayl_holat_2aa21a9a = new int[서술자한도], ochmoq_Sozlamalar = new int[서술자한도], Ma_lumotnomalar_COUNT = new int[서술자한도];
    static int[] Tarmoq_deskriptor = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] yo_l_nom = new int[64], uzatish_ma_lumotlar = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return ochmoq_deskriptor[파일서술자] - 1;
    }
    static int 빈서술자(int Bajarish) {
        for (int INDEX = Bajarish; INDEX < 서술자한도; INDEX++) if (ochmoq_deskriptor[INDEX] == 0) return INDEX;
        return -24;
    }
    static int bo_sh_deskriptor() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (Ma_lumotnomalar_COUNT[INDEX] == 0) return INDEX;
        return -24;
    }
    static int Ulanish(int 서술자, int 기술, int 파일종류, int fayl_nishon, int Moslamalar) {
        ochmoq_deskriptor[서술자] = 기술 + 1; 서술자설정[서술자] = (Moslamalar & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; nishon[기술] = fayl_nishon; Ma_lumotnomalar_COUNT[기술] = 1;
        ochmoq_Sozlamalar[기술] = Moslamalar & (3 | 이어쓰기 | 기다리지않기); fayl_holat_2aa21a9a[기술] = 0;
        Tarmoq_deskriptor[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void Start_Jarayon() {
        Toza_Jarayon();
        for (int INDEX = 0; INDEX < 3; INDEX++) Ulanish(INDEX, INDEX, 1, INDEX, INDEX == 0 ? 0 : 1);
    }
    static void Toza_Jarayon() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (ochmoq_deskriptor[INDEX] != 0) yopmoq_fayl(INDEX);
    }
    static int yopmoq_fayl(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        ochmoq_deskriptor[서술자] = 0; 서술자설정[서술자] = 0;
        Ma_lumotnomalar_COUNT[기술]--;
        if (Ma_lumotnomalar_COUNT[기술] == 0) {
            if (종류[기술] == 2) Xotira_fayllar_tizimi.ochmoq_COUNT[nishon[기술]]--;
            if (종류[기술] == 3 && Tarmoq_deskriptor[기술] != 0) Tarmoq_Stack.Yopish(Tarmoq_deskriptor[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 bayt_VALUE 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int manzil) {
        if (!실행관리.klip(manzil, 1)) return -14;
        int Holati = qurilma_VALUE.기억읽기(manzil) == '/' ? 1 : 0;
        for (int uzunlik_VALUE = 0; uzunlik_VALUE < 64; uzunlik_VALUE++) {
            if (!실행관리.klip(manzil + Holati + uzunlik_VALUE, 1)) return -14;
            int VALUE = qurilma_VALUE.기억읽기(manzil + Holati + uzunlik_VALUE);
            yo_l_nom[uzunlik_VALUE] = VALUE;
            if (VALUE == 0) return uzunlik_VALUE == 0 ? -2 : (Xotira_fayllar_tizimi.chek_nom(yo_l_nom, uzunlik_VALUE) ? uzunlik_VALUE : -22);
            if (VALUE == '/') return -20;
        }
        return -36;
    }
    static int ochmoq_fayl(int nom_manzil, int Moslamalar, int 허가) {
        int uzunlik_VALUE = 경로읽기(nom_manzil);
        if (uzunlik_VALUE < 0) return uzunlik_VALUE;
        if ((Moslamalar & ~(3 | Yaratish_kiritish | 독점생성 | tozalamoq_TOC | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Moslamalar & 3) == 3 || ((Moslamalar & tozalamoq_TOC) != 0 && (Moslamalar & 3) == 0)) return -22;
        int Fayl = Xotira_fayllar_tizimi.FIND_kiritish(yo_l_nom, uzunlik_VALUE);
        if (Fayl >= 0 && (Moslamalar & (Yaratish_kiritish | 독점생성)) == (Yaratish_kiritish | 독점생성)) return -17;
        if (Fayl == -2 && (Moslamalar & Yaratish_kiritish) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = bo_sh_deskriptor();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Fayl == -2) {
            int o_lchov = Xotira_fayllar_tizimi.Store_VALUE(yo_l_nom, uzunlik_VALUE, yo_l_nom, 0);
            if (o_lchov < 0) return o_lchov;
            Fayl = Xotira_fayllar_tizimi.FIND_kiritish(yo_l_nom, uzunlik_VALUE);
            Xotira_fayllar_tizimi.허가들[Fayl] = 허가 & 511;
        }
        if (Fayl < 0) return Fayl;
        if ((Moslamalar & tozalamoq_TOC) != 0) Xotira_fayllar_tizimi.o_lcham_Ro_yxat[Fayl] = 0;
        Xotira_fayllar_tizimi.ochmoq_COUNT[Fayl]++;
        return Ulanish(서술자, 기술, 2, Fayl, Moslamalar);
    }
    static int 파일읽기(int 서술자, int ma_lumotlar_manzil, int uzunlik_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (ochmoq_Sozlamalar[기술] & 3) == 1) return -9;
        if (uzunlik_VALUE < 0) return -22;
        if (uzunlik_VALUE == 0) return 0;
        if (!실행관리.klip(ma_lumotlar_manzil, uzunlik_VALUE)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, ma_lumotlar_manzil, uzunlik_VALUE, 0, 0);
        if (종류[기술] == 1) {
            int RECEIVED_COUNT = 0;
            while (RECEIVED_COUNT < uzunlik_VALUE) {
                int VALUE = SMS_Terminal.직렬읽기();
                if (VALUE < 0) VALUE = klaviatura.Oʻqish();
                if (VALUE < 0) {
                    if (RECEIVED_COUNT > 0) return RECEIVED_COUNT;
                    if ((ochmoq_Sozlamalar[기술] & 기다리지않기) != 0) return -11;
                    if (qurilma_VALUE.사용자남은밀리초() <= 10) return -11;
                    Tarmoq_Stack.tasdiqlamoq(); qurilma_VALUE.잠시양보();
                } else {
                    qurilma_VALUE.yozmoq_Xotira(ma_lumotlar_manzil + RECEIVED_COUNT, VALUE); RECEIVED_COUNT++;
                }
            }
            return RECEIVED_COUNT;
        }
        int Fayl = nishon[기술], Holati = fayl_holat_2aa21a9a[기술];
        if (Holati >= Xotira_fayllar_tizimi.o_lcham_Ro_yxat[Fayl]) return 0;
        if (uzunlik_VALUE > Xotira_fayllar_tizimi.o_lcham_Ro_yxat[Fayl] - Holati) uzunlik_VALUE = Xotira_fayllar_tizimi.o_lcham_Ro_yxat[Fayl] - Holati;
        int 원본주소 = qurilma_VALUE.fayl_Xotira() + Fayl * Xotira_fayllar_tizimi.최대크기 + Holati;
        for (int INDEX = 0; INDEX < uzunlik_VALUE; INDEX++) qurilma_VALUE.yozmoq_Xotira(ma_lumotlar_manzil + INDEX, qurilma_VALUE.기억읽기(원본주소 + INDEX));
        fayl_holat_2aa21a9a[기술] += uzunlik_VALUE;
        return uzunlik_VALUE;
    }
    static int yozmoq_fayl(int 서술자, int ma_lumotlar_manzil, int uzunlik_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (ochmoq_Sozlamalar[기술] & 3) == 0) return -9;
        if (uzunlik_VALUE < 0) return -22;
        if (uzunlik_VALUE == 0) return 0;
        if (!실행관리.klip(ma_lumotlar_manzil, uzunlik_VALUE)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 ko_chirish_joyi_VALUE 주소가 필요하다.
        if (종류[기술] == 1) {
            if (uzunlik_VALUE > 16384) uzunlik_VALUE = 16384;
            for (int INDEX = 0; INDEX < uzunlik_VALUE; INDEX++) {
                int VALUE = qurilma_VALUE.기억읽기(ma_lumotlar_manzil + INDEX);
                SMS_Terminal.직렬바이트(VALUE); SMS_Terminal.화면문자(VALUE);
            }
            return uzunlik_VALUE;
        }
        int Fayl = nishon[기술], Hajmi = Xotira_fayllar_tizimi.o_lcham_Ro_yxat[Fayl];
        int Holati = (ochmoq_Sozlamalar[기술] & 이어쓰기) != 0 ? Hajmi : fayl_holat_2aa21a9a[기술];
        if (Holati >= Xotira_fayllar_tizimi.최대크기) return -27;
        if (uzunlik_VALUE > Xotira_fayllar_tizimi.최대크기 - Holati) uzunlik_VALUE = Xotira_fayllar_tizimi.최대크기 - Holati;
        int ko_chirish_joyi_manzil = qurilma_VALUE.fayl_Xotira() + Fayl * Xotira_fayllar_tizimi.최대크기;
        for (int INDEX = Hajmi; INDEX < Holati; INDEX++) qurilma_VALUE.yozmoq_Xotira(ko_chirish_joyi_manzil + INDEX, 0);
        for (int INDEX = 0; INDEX < uzunlik_VALUE; INDEX++) qurilma_VALUE.yozmoq_Xotira(ko_chirish_joyi_manzil + Holati + INDEX, qurilma_VALUE.기억읽기(ma_lumotlar_manzil + INDEX));
        fayl_holat_2aa21a9a[기술] = Holati + uzunlik_VALUE;
        if (Holati + uzunlik_VALUE > Hajmi) Xotira_fayllar_tizimi.o_lcham_Ro_yxat[Fayl] = Holati + uzunlik_VALUE;
        return uzunlik_VALUE;
    }
    static int izlamoq_fayl(int 서술자, int OFFSET_VALUE, int Project_ildiz) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (Project_ildiz < 0 || Project_ildiz > 2) return -22;
        int Fon_VALUE = Project_ildiz == 0 ? 0 : (Project_ildiz == 1 ? fayl_holat_2aa21a9a[기술] : Xotira_fayllar_tizimi.o_lcham_Ro_yxat[nishon[기술]]);
        if (OFFSET_VALUE > 0 && Fon_VALUE > 2147483647 - OFFSET_VALUE) return -75;
        if (OFFSET_VALUE < 0 && OFFSET_VALUE < -Fon_VALUE) return -22;
        fayl_holat_2aa21a9a[기술] = Fon_VALUE + OFFSET_VALUE;
        return fayl_holat_2aa21a9a[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean tayinlash_VALUE, int Moslamalar) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return tayinlash_VALUE ? -9 : -22;
        if (tayinlash_VALUE && 서술자 == 새서술자) return 새서술자;
        if (tayinlash_VALUE) { if (ochmoq_deskriptor[새서술자] != 0) yopmoq_fayl(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        ochmoq_deskriptor[새서술자] = 기술 + 1; 서술자설정[새서술자] = Moslamalar; Ma_lumotnomalar_COUNT[기술]++;
        return 새서술자;
    }
    static int olib_tashlamoq_fayl_kiritish_nom(int nom_manzil) {
        int uzunlik_VALUE = 경로읽기(nom_manzil);
        if (uzunlik_VALUE < 0) return uzunlik_VALUE;
        int Fayl = Xotira_fayllar_tizimi.FIND_kiritish(yo_l_nom, uzunlik_VALUE);
        if (Fayl < 0) return Fayl;
        Xotira_fayllar_tizimi.이름들[Fayl * 64] = 0;
        return 0;
    }
    static int to_plam_fayl_uzunlik(int 서술자, int uzunlik_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (ochmoq_Sozlamalar[기술] & 3) == 0 || uzunlik_VALUE < 0) return -22;
        if (uzunlik_VALUE > Xotira_fayllar_tizimi.최대크기) return -27;
        int Fayl = nishon[기술], manzil = qurilma_VALUE.fayl_Xotira() + Fayl * Xotira_fayllar_tizimi.최대크기;
        for (int INDEX = Xotira_fayllar_tizimi.o_lcham_Ro_yxat[Fayl]; INDEX < uzunlik_VALUE; INDEX++) qurilma_VALUE.yozmoq_Xotira(manzil + INDEX, 0);
        Xotira_fayllar_tizimi.o_lcham_Ro_yxat[Fayl] = uzunlik_VALUE;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int manzil) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.klip(manzil, 48)) return -14;
        for (int INDEX = 0; INDEX < 12; INDEX++) 실행관리.수쓰기(manzil + INDEX * 4, 0);
        int Fayl = nishon[기술], Hajmi = 종류[기술] == 2 ? Xotira_fayllar_tizimi.o_lcham_Ro_yxat[Fayl] : 0;
        int 허가 = 종류[기술] == 2 ? Xotira_fayllar_tizimi.허가들[Fayl] : 438;
        실행관리.수쓰기(manzil, 1);
        실행관리.수쓰기(manzil + 4, 종류[기술] == 2 ? Fayl + 1 : 100 + 기술);
        실행관리.수쓰기(manzil + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(manzil + 12, 종류[기술] == 2 && Xotira_fayllar_tizimi.이름들[Fayl * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(manzil + 28, Hajmi); 실행관리.수쓰기(manzil + 32, 512);
        실행관리.수쓰기(manzil + 36, (Hajmi + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int Buyruq, int VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Buyruq == 0 || Buyruq == 1030) return 서술자복제(서술자, VALUE, false, Buyruq == 1030 ? 1 : 0);
        if (Buyruq == 1) return 서술자설정[서술자];
        if (Buyruq == 2) { if ((VALUE & ~1) != 0) return -22; 서술자설정[서술자] = VALUE; return 0; }
        if (Buyruq == 3) return ochmoq_Sozlamalar[기술];
        if (Buyruq == 4) {
            if ((VALUE & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            ochmoq_Sozlamalar[기술] = (ochmoq_Sozlamalar[기술] & 3) | (VALUE & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int 통신종단점만들기(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = bo_sh_deskriptor();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Ulanish(서술자, 기술, 3, 0, o_qish_yozish_mumkin_bayroq);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int manzil_32(int manzil) {
        return qurilma_VALUE.기억읽기(manzil) << 24 | qurilma_VALUE.기억읽기(manzil + 1) << 16
            | qurilma_VALUE.기억읽기(manzil + 2) << 8 | qurilma_VALUE.기억읽기(manzil + 3);
    }
    static int chek_manzil(int manzil, int uzunlik_VALUE) {
        if (uzunlik_VALUE < 16) return -22;
        if (!실행관리.klip(manzil, 16)) return -14;
        return 실행관리.짧은수(manzil) == 2 ? 0 : -97;
    }
    static int BOG_LAMOQ_manzil(int 서술자, int manzil, int uzunlik_VALUE) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int o_lchov = chek_manzil(manzil, uzunlik_VALUE);
        if (o_lchov < 0) return o_lchov;
        if (Tarmoq_deskriptor[기술] != 0) return -22;
        int Tarmoq_manzil = manzil_32(manzil + 4);
        if (Tarmoq_manzil != 0 && Tarmoq_manzil != Tarmoq_Stack.내주소) return -99;
        int 접속번호 = qurilma_VALUE.기억읽기(manzil + 2) << 8 | qurilma_VALUE.기억읽기(manzil + 3);
        o_lchov = Tarmoq_Stack.Ochish(접속번호);
        if (o_lchov < 0) return o_lchov;
        Tarmoq_deskriptor[기술] = o_lchov; nishon[기술] = Tarmoq_manzil;
        return 0;
    }
    static int Avtomatik_BOG_LAMOQ(int 기술) {
        if (Tarmoq_deskriptor[기술] != 0) return 0;
        int o_lchov = Tarmoq_Stack.Ochish(0);
        if (o_lchov < 0) return o_lchov;
        Tarmoq_deskriptor[기술] = o_lchov;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 요청 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int ma_lumotlar_manzil, int uzunlik_VALUE, int Moslamalar, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Moslamalar != 0) return -95;
        if (uzunlik_VALUE < 0 || uzunlik_VALUE > 1024) return -90;
        if (uzunlik_VALUE != 0 && !실행관리.klip(ma_lumotlar_manzil, uzunlik_VALUE)) return -14;
        if (!실행관리.klip(요청주소, 8)) return -14;
        int manzil = 실행관리.수(요청주소);
        int o_lchov = chek_manzil(manzil, 실행관리.수(요청주소 + 4));
        if (o_lchov < 0) return o_lchov;
        int 접속번호 = qurilma_VALUE.기억읽기(manzil + 2) << 8 | qurilma_VALUE.기억읽기(manzil + 3);
        if (접속번호 == 0) return -22;
        o_lchov = Avtomatik_BOG_LAMOQ(기술);
        if (o_lchov < 0) return o_lchov;
        for (int INDEX = 0; INDEX < uzunlik_VALUE; INDEX++) uzatish_ma_lumotlar[INDEX] = qurilma_VALUE.기억읽기(ma_lumotlar_manzil + INDEX);
        return Tarmoq_Stack.yuborish(Tarmoq_deskriptor[기술], manzil_32(manzil + 4), 접속번호, uzatish_ma_lumotlar, uzunlik_VALUE);
    }
    static void yozmoq_manzil(int manzil, int uzunlik_VALUE, int Tarmoq_manzil, int 접속번호) {
        for (int INDEX = 0; INDEX < uzunlik_VALUE && INDEX < 16; INDEX++) {
            int VALUE = 0;
            if (INDEX == 0) VALUE = 2;
            if (INDEX == 2) VALUE = 접속번호 >>> 8;
            if (INDEX == 3) VALUE = 접속번호;
            if (INDEX >= 4 && INDEX < 8) VALUE = Tarmoq_manzil >>> (56 - INDEX * 8);
            qurilma_VALUE.yozmoq_Xotira(manzil + INDEX, VALUE & 255);
        }
    }
    static int 자료전문받기(int 서술자, int ma_lumotlar_manzil, int uzunlik_VALUE, int Moslamalar, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Moslamalar & ~64) != 0) return -95;
        if (uzunlik_VALUE < 0) return -22;
        if (uzunlik_VALUE != 0 && !실행관리.klip(ma_lumotlar_manzil, uzunlik_VALUE)) return -14;
        int manzil = 0, manzil_uzunlik_manzil = 0, manzil_uzunlik = 0;
        if (요청주소 != 0) {
            if (!실행관리.klip(요청주소, 8)) return -14;
            manzil = 실행관리.수(요청주소); manzil_uzunlik_manzil = 실행관리.수(요청주소 + 4);
            if (manzil != 0) {
                if (!실행관리.klip(manzil_uzunlik_manzil, 4)) return -14;
                manzil_uzunlik = 실행관리.수(manzil_uzunlik_manzil);
                if (manzil_uzunlik < 0) return -22;
                if (!실행관리.klip(manzil, manzil_uzunlik < 16 ? manzil_uzunlik : 16)) return -14;
            }
        }
        int o_lchov = Avtomatik_BOG_LAMOQ(기술);
        if (o_lchov < 0) return o_lchov;
        int Bajarish = qurilma_VALUE.밀리초();
        while (true) {
            o_lchov = Tarmoq_Stack.받기(Tarmoq_deskriptor[기술], uzatish_ma_lumotlar, 1024, 0);
            if (o_lchov != -11) break;
            if ((Moslamalar & 64) != 0 || (ochmoq_Sozlamalar[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && qurilma_VALUE.밀리초() - Bajarish >= 수신대기밀리초[기술]) return -11;
            if (qurilma_VALUE.사용자남은밀리초() <= 10) return -11;
            qurilma_VALUE.잠시양보();
        }
        if (o_lchov < 0) return o_lchov;
        if (o_lchov > uzunlik_VALUE) o_lchov = uzunlik_VALUE;
        for (int INDEX = 0; INDEX < o_lchov; INDEX++) qurilma_VALUE.yozmoq_Xotira(ma_lumotlar_manzil + INDEX, uzatish_ma_lumotlar[INDEX]);
        if (manzil != 0) {
            yozmoq_manzil(manzil, manzil_uzunlik, Tarmoq_Stack.bir_rangli_manzil(Tarmoq_deskriptor[기술]), Tarmoq_Stack.상대접속번호(Tarmoq_deskriptor[기술]));
            실행관리.수쓰기(manzil_uzunlik_manzil, 16);
        }
        return o_lchov;
    }
    static int 통신주소읽기(int 서술자, int manzil, int uzunlik_manzil) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.klip(uzunlik_manzil, 4)) return -14;
        int uzunlik_VALUE = 실행관리.수(uzunlik_manzil);
        if (uzunlik_VALUE < 0) return -22;
        if (!실행관리.klip(manzil, uzunlik_VALUE < 16 ? uzunlik_VALUE : 16)) return -14;
        int in_kiritish = Tarmoq_Stack.INDEX(Tarmoq_deskriptor[기술]);
        yozmoq_manzil(manzil, uzunlik_VALUE, nishon[기술], in_kiritish < 0 ? 0 : Tarmoq_Stack.접속번호들[in_kiritish]);
        실행관리.수쓰기(uzunlik_manzil, 16);
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
