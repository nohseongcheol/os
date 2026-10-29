// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 kiy_jariñoo_internet 과정의 파일서술자와 열린 bara_denc 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int jàng_bind_tektalukaay = 2, sos_dugal_xabaar = 64, 독점생성 = 128, efaase_TOC = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] sos_yombal = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], luñu_name = new int[서술자한도];
    static int[] 파일위치 = new int[서술자한도], sos_Jekkal_yi = new int[서술자한도], 참조수 = new int[서술자한도];
    static int[] mbaal_yombal = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] Yoonu_jëmale_tur = new int[64], toxal_mbir = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return sos_yombal[파일서술자] - 1;
    }
    static int 빈서술자(int daw) {
        for (int àlluwa_tur = daw; àlluwa_tur < 서술자한도; àlluwa_tur++) if (sos_yombal[àlluwa_tur] == 0) return àlluwa_tur;
        return -24;
    }
    static int neen_yombal() {
        for (int àlluwa_tur = 0; àlluwa_tur < 서술자한도; àlluwa_tur++) if (참조수[àlluwa_tur] == 0) return àlluwa_tur;
        return -24;
    }
    static int JOKKOO(int 서술자, int 기술, int 파일종류, int bara_denc_luñu_name, int Jekkal_yi) {
        sos_yombal[서술자] = 기술 + 1; 서술자설정[서술자] = (Jekkal_yi & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; luñu_name[기술] = bara_denc_luñu_name; 참조수[기술] = 1;
        sos_Jekkal_yi[기술] = Jekkal_yi & (3 | 이어쓰기 | 기다리지않기); 파일위치[기술] = 0;
        mbaal_yombal[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void Door_yokkute() {
        과정정리();
        for (int àlluwa_tur = 0; àlluwa_tur < 3; àlluwa_tur++) JOKKOO(àlluwa_tur, àlluwa_tur, 1, àlluwa_tur, àlluwa_tur == 0 ? 0 : 1);
    }
    static void 과정정리() {
        for (int àlluwa_tur = 0; àlluwa_tur < 서술자한도; àlluwa_tur++) if (sos_yombal[àlluwa_tur] != 0) Tej_bara_denc(àlluwa_tur);
    }
    static int Tej_bara_denc(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        sos_yombal[서술자] = 0; 서술자설정[서술자] = 0;
        참조수[기술]--;
        if (참조수[기술] == 0) {
            if (종류[기술] == 2) fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.열림수[luñu_name[기술]]--;
            if (종류[기술] == 3 && mbaal_yombal[기술] != 0) mbaal_Tegalo.Tej(mbaal_yombal[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 okte_xëyma 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int dëkkuwaay) {
        if (!실행관리.kilip(dëkkuwaay, 1)) return -14;
        int 위치 = toftal_xëyma.기억읽기(dëkkuwaay) == '/' ? 1 : 0;
        for (int diir_xëyma = 0; diir_xëyma < 64; diir_xëyma++) {
            if (!실행관리.kilip(dëkkuwaay + 위치 + diir_xëyma, 1)) return -14;
            int xëyma = toftal_xëyma.기억읽기(dëkkuwaay + 위치 + diir_xëyma);
            Yoonu_jëmale_tur[diir_xëyma] = xëyma;
            if (xëyma == 0) return diir_xëyma == 0 ? -2 : (fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.sek_tur(Yoonu_jëmale_tur, diir_xëyma) ? diir_xëyma : -22);
            if (xëyma == '/') return -20;
        }
        return -36;
    }
    static int sos_bara_denc(int tur_dëkkuwaay, int Jekkal_yi, int 허가) {
        int diir_xëyma = 경로읽기(tur_dëkkuwaay);
        if (diir_xëyma < 0) return diir_xëyma;
        if ((Jekkal_yi & ~(3 | sos_dugal_xabaar | 독점생성 | efaase_TOC | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Jekkal_yi & 3) == 3 || ((Jekkal_yi & efaase_TOC) != 0 && (Jekkal_yi & 3) == 0)) return -22;
        int bara_denc = fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.seet_dugal_xabaar(Yoonu_jëmale_tur, diir_xëyma);
        if (bara_denc >= 0 && (Jekkal_yi & (sos_dugal_xabaar | 독점생성)) == (sos_dugal_xabaar | 독점생성)) return -17;
        if (bara_denc == -2 && (Jekkal_yi & sos_dugal_xabaar) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = neen_yombal();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (bara_denc == -2) {
            int 결과 = fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.Store_xëyma(Yoonu_jëmale_tur, diir_xëyma, Yoonu_jëmale_tur, 0);
            if (결과 < 0) return 결과;
            bara_denc = fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.seet_dugal_xabaar(Yoonu_jëmale_tur, diir_xëyma);
            fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.허가들[bara_denc] = 허가 & 511;
        }
        if (bara_denc < 0) return bara_denc;
        if ((Jekkal_yi & efaase_TOC) != 0) fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.tolluwaay_lim[bara_denc] = 0;
        fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.열림수[bara_denc]++;
        return JOKKOO(서술자, 기술, 2, bara_denc, Jekkal_yi);
    }
    static int 파일읽기(int 서술자, int mbir_dëkkuwaay, int diir_xëyma) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (sos_Jekkal_yi[기술] & 3) == 1) return -9;
        if (diir_xëyma < 0) return -22;
        if (diir_xëyma == 0) return 0;
        if (!실행관리.kilip(mbir_dëkkuwaay, diir_xëyma)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, mbir_dëkkuwaay, diir_xëyma, 0, 0);
        if (종류[기술] == 1) {
            int 받은수 = 0;
            while (받은수 < diir_xëyma) {
                int xëyma = 문자단말.직렬읽기();
                if (xëyma < 0) xëyma = arafukaay.읽기();
                if (xëyma < 0) {
                    if (받은수 > 0) return 받은수;
                    if ((sos_Jekkal_yi[기술] & 기다리지않기) != 0) return -11;
                    if (toftal_xëyma.사용자남은밀리초() <= 10) return -11;
                    mbaal_Tegalo.luñutu(); toftal_xëyma.잠시양보();
                } else {
                    toftal_xëyma.biir_fatlekookaay(mbir_dëkkuwaay + 받은수, xëyma); 받은수++;
                }
            }
            return 받은수;
        }
        int bara_denc = luñu_name[기술], 위치 = 파일위치[기술];
        if (위치 >= fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.tolluwaay_lim[bara_denc]) return 0;
        if (diir_xëyma > fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.tolluwaay_lim[bara_denc] - 위치) diir_xëyma = fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.tolluwaay_lim[bara_denc] - 위치;
        int 원본주소 = toftal_xëyma.bara_denc_fatlekookaay() + bara_denc * fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.최대크기 + 위치;
        for (int àlluwa_tur = 0; àlluwa_tur < diir_xëyma; àlluwa_tur++) toftal_xëyma.biir_fatlekookaay(mbir_dëkkuwaay + àlluwa_tur, toftal_xëyma.기억읽기(원본주소 + àlluwa_tur));
        파일위치[기술] += diir_xëyma;
        return diir_xëyma;
    }
    static int biir_bara_denc(int 서술자, int mbir_dëkkuwaay, int diir_xëyma) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (sos_Jekkal_yi[기술] & 3) == 0) return -9;
        if (diir_xëyma < 0) return -22;
        if (diir_xëyma == 0) return 0;
        if (!실행관리.kilip(mbir_dëkkuwaay, diir_xëyma)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 jëmmukaay_xëyma 주소가 필요하다.
        if (종류[기술] == 1) {
            if (diir_xëyma > 16384) diir_xëyma = 16384;
            for (int àlluwa_tur = 0; àlluwa_tur < diir_xëyma; àlluwa_tur++) {
                int xëyma = toftal_xëyma.기억읽기(mbir_dëkkuwaay + àlluwa_tur);
                문자단말.직렬바이트(xëyma); 문자단말.화면문자(xëyma);
            }
            return diir_xëyma;
        }
        int bara_denc = luñu_name[기술], tolluwaay = fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.tolluwaay_lim[bara_denc];
        int 위치 = (sos_Jekkal_yi[기술] & 이어쓰기) != 0 ? tolluwaay : 파일위치[기술];
        if (위치 >= fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.최대크기) return -27;
        if (diir_xëyma > fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.최대크기 - 위치) diir_xëyma = fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.최대크기 - 위치;
        int jëmmukaay_dëkkuwaay = toftal_xëyma.bara_denc_fatlekookaay() + bara_denc * fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.최대크기;
        for (int àlluwa_tur = tolluwaay; àlluwa_tur < 위치; àlluwa_tur++) toftal_xëyma.biir_fatlekookaay(jëmmukaay_dëkkuwaay + àlluwa_tur, 0);
        for (int àlluwa_tur = 0; àlluwa_tur < diir_xëyma; àlluwa_tur++) toftal_xëyma.biir_fatlekookaay(jëmmukaay_dëkkuwaay + 위치 + àlluwa_tur, toftal_xëyma.기억읽기(mbir_dëkkuwaay + àlluwa_tur));
        파일위치[기술] = 위치 + diir_xëyma;
        if (위치 + diir_xëyma > tolluwaay) fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.tolluwaay_lim[bara_denc] = 위치 + diir_xëyma;
        return diir_xëyma;
    }
    static int seet_bara_denc(int 서술자, int Randal_xëyma, int 기준) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (기준 < 0 || 기준 > 2) return -22;
        int Njiitlay_xëyma = 기준 == 0 ? 0 : (기준 == 1 ? 파일위치[기술] : fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.tolluwaay_lim[luñu_name[기술]]);
        if (Randal_xëyma > 0 && Njiitlay_xëyma > 2147483647 - Randal_xëyma) return -75;
        if (Randal_xëyma < 0 && Randal_xëyma < -Njiitlay_xëyma) return -22;
        파일위치[기술] = Njiitlay_xëyma + Randal_xëyma;
        return 파일위치[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean 지정, int Jekkal_yi) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return 지정 ? -9 : -22;
        if (지정 && 서술자 == 새서술자) return 새서술자;
        if (지정) { if (sos_yombal[새서술자] != 0) Tej_bara_denc(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        sos_yombal[새서술자] = 기술 + 1; 서술자설정[새서술자] = Jekkal_yi; 참조수[기술]++;
        return 새서술자;
    }
    static int dandal_bara_denc_dugal_xabaar_tur(int tur_dëkkuwaay) {
        int diir_xëyma = 경로읽기(tur_dëkkuwaay);
        if (diir_xëyma < 0) return diir_xëyma;
        int bara_denc = fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.seet_dugal_xabaar(Yoonu_jëmale_tur, diir_xëyma);
        if (bara_denc < 0) return bara_denc;
        fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.이름들[bara_denc * 64] = 0;
        return 0;
    }
    static int Boole_gi_bara_denc_diir(int 서술자, int diir_xëyma) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (sos_Jekkal_yi[기술] & 3) == 0 || diir_xëyma < 0) return -22;
        if (diir_xëyma > fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.최대크기) return -27;
        int bara_denc = luñu_name[기술], dëkkuwaay = toftal_xëyma.bara_denc_fatlekookaay() + bara_denc * fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.최대크기;
        for (int àlluwa_tur = fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.tolluwaay_lim[bara_denc]; àlluwa_tur < diir_xëyma; àlluwa_tur++) toftal_xëyma.biir_fatlekookaay(dëkkuwaay + àlluwa_tur, 0);
        fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.tolluwaay_lim[bara_denc] = diir_xëyma;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int dëkkuwaay) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.kilip(dëkkuwaay, 48)) return -14;
        for (int àlluwa_tur = 0; àlluwa_tur < 12; àlluwa_tur++) 실행관리.수쓰기(dëkkuwaay + àlluwa_tur * 4, 0);
        int bara_denc = luñu_name[기술], tolluwaay = 종류[기술] == 2 ? fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.tolluwaay_lim[bara_denc] : 0;
        int 허가 = 종류[기술] == 2 ? fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.허가들[bara_denc] : 438;
        실행관리.수쓰기(dëkkuwaay, 1);
        실행관리.수쓰기(dëkkuwaay + 4, 종류[기술] == 2 ? bara_denc + 1 : 100 + 기술);
        실행관리.수쓰기(dëkkuwaay + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(dëkkuwaay + 12, 종류[기술] == 2 && fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.이름들[bara_denc * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(dëkkuwaay + 28, tolluwaay); 실행관리.수쓰기(dëkkuwaay + 32, 512);
        실행관리.수쓰기(dëkkuwaay + 36, (tolluwaay + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int ndigel, int xëyma) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (ndigel == 0 || ndigel == 1030) return 서술자복제(서술자, xëyma, false, ndigel == 1030 ? 1 : 0);
        if (ndigel == 1) return 서술자설정[서술자];
        if (ndigel == 2) { if ((xëyma & ~1) != 0) return -22; 서술자설정[서술자] = xëyma; return 0; }
        if (ndigel == 3) return sos_Jekkal_yi[기술];
        if (ndigel == 4) {
            if ((xëyma & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            sos_Jekkal_yi[기술] = (sos_Jekkal_yi[기술] & 3) | (xëyma & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int 통신종단점만들기(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = neen_yombal();
        if (서술자 < 0 || 기술 < 0) return -24;
        return JOKKOO(서술자, 기술, 3, 0, jàng_bind_tektalukaay);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int dëkkuwaay_32(int dëkkuwaay) {
        return toftal_xëyma.기억읽기(dëkkuwaay) << 24 | toftal_xëyma.기억읽기(dëkkuwaay + 1) << 16
            | toftal_xëyma.기억읽기(dëkkuwaay + 2) << 8 | toftal_xëyma.기억읽기(dëkkuwaay + 3);
    }
    static int sek_dëkkuwaay(int dëkkuwaay, int diir_xëyma) {
        if (diir_xëyma < 16) return -22;
        if (!실행관리.kilip(dëkkuwaay, 16)) return -14;
        return 실행관리.짧은수(dëkkuwaay) == 2 ? 0 : -97;
    }
    static int BIND_dëkkuwaay(int 서술자, int dëkkuwaay, int diir_xëyma) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int 결과 = sek_dëkkuwaay(dëkkuwaay, diir_xëyma);
        if (결과 < 0) return 결과;
        if (mbaal_yombal[기술] != 0) return -22;
        int mbaal_dëkkuwaay = dëkkuwaay_32(dëkkuwaay + 4);
        if (mbaal_dëkkuwaay != 0 && mbaal_dëkkuwaay != mbaal_Tegalo.내주소) return -99;
        int 접속번호 = toftal_xëyma.기억읽기(dëkkuwaay + 2) << 8 | toftal_xëyma.기억읽기(dëkkuwaay + 3);
        결과 = mbaal_Tegalo.sos(접속번호);
        if (결과 < 0) return 결과;
        mbaal_yombal[기술] = 결과; luñu_name[기술] = mbaal_dëkkuwaay;
        return 0;
    }
    static int 자동묶기(int 기술) {
        if (mbaal_yombal[기술] != 0) return 0;
        int 결과 = mbaal_Tegalo.sos(0);
        if (결과 < 0) return 결과;
        mbaal_yombal[기술] = 결과;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 요청 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int mbir_dëkkuwaay, int diir_xëyma, int Jekkal_yi, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Jekkal_yi != 0) return -95;
        if (diir_xëyma < 0 || diir_xëyma > 1024) return -90;
        if (diir_xëyma != 0 && !실행관리.kilip(mbir_dëkkuwaay, diir_xëyma)) return -14;
        if (!실행관리.kilip(요청주소, 8)) return -14;
        int dëkkuwaay = 실행관리.수(요청주소);
        int 결과 = sek_dëkkuwaay(dëkkuwaay, 실행관리.수(요청주소 + 4));
        if (결과 < 0) return 결과;
        int 접속번호 = toftal_xëyma.기억읽기(dëkkuwaay + 2) << 8 | toftal_xëyma.기억읽기(dëkkuwaay + 3);
        if (접속번호 == 0) return -22;
        결과 = 자동묶기(기술);
        if (결과 < 0) return 결과;
        for (int àlluwa_tur = 0; àlluwa_tur < diir_xëyma; àlluwa_tur++) toxal_mbir[àlluwa_tur] = toftal_xëyma.기억읽기(mbir_dëkkuwaay + àlluwa_tur);
        return mbaal_Tegalo.Yónnee(mbaal_yombal[기술], dëkkuwaay_32(dëkkuwaay + 4), 접속번호, toxal_mbir, diir_xëyma);
    }
    static void biir_dëkkuwaay(int dëkkuwaay, int diir_xëyma, int mbaal_dëkkuwaay, int 접속번호) {
        for (int àlluwa_tur = 0; àlluwa_tur < diir_xëyma && àlluwa_tur < 16; àlluwa_tur++) {
            int xëyma = 0;
            if (àlluwa_tur == 0) xëyma = 2;
            if (àlluwa_tur == 2) xëyma = 접속번호 >>> 8;
            if (àlluwa_tur == 3) xëyma = 접속번호;
            if (àlluwa_tur >= 4 && àlluwa_tur < 8) xëyma = mbaal_dëkkuwaay >>> (56 - àlluwa_tur * 8);
            toftal_xëyma.biir_fatlekookaay(dëkkuwaay + àlluwa_tur, xëyma & 255);
        }
    }
    static int 자료전문받기(int 서술자, int mbir_dëkkuwaay, int diir_xëyma, int Jekkal_yi, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Jekkal_yi & ~64) != 0) return -95;
        if (diir_xëyma < 0) return -22;
        if (diir_xëyma != 0 && !실행관리.kilip(mbir_dëkkuwaay, diir_xëyma)) return -14;
        int dëkkuwaay = 0, dëkkuwaay_diir_dëkkuwaay = 0, dëkkuwaay_diir = 0;
        if (요청주소 != 0) {
            if (!실행관리.kilip(요청주소, 8)) return -14;
            dëkkuwaay = 실행관리.수(요청주소); dëkkuwaay_diir_dëkkuwaay = 실행관리.수(요청주소 + 4);
            if (dëkkuwaay != 0) {
                if (!실행관리.kilip(dëkkuwaay_diir_dëkkuwaay, 4)) return -14;
                dëkkuwaay_diir = 실행관리.수(dëkkuwaay_diir_dëkkuwaay);
                if (dëkkuwaay_diir < 0) return -22;
                if (!실행관리.kilip(dëkkuwaay, dëkkuwaay_diir < 16 ? dëkkuwaay_diir : 16)) return -14;
            }
        }
        int 결과 = 자동묶기(기술);
        if (결과 < 0) return 결과;
        int daw = toftal_xëyma.밀리초();
        while (true) {
            결과 = mbaal_Tegalo.받기(mbaal_yombal[기술], toxal_mbir, 1024, 0);
            if (결과 != -11) break;
            if ((Jekkal_yi & 64) != 0 || (sos_Jekkal_yi[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && toftal_xëyma.밀리초() - daw >= 수신대기밀리초[기술]) return -11;
            if (toftal_xëyma.사용자남은밀리초() <= 10) return -11;
            toftal_xëyma.잠시양보();
        }
        if (결과 < 0) return 결과;
        if (결과 > diir_xëyma) 결과 = diir_xëyma;
        for (int àlluwa_tur = 0; àlluwa_tur < 결과; àlluwa_tur++) toftal_xëyma.biir_fatlekookaay(mbir_dëkkuwaay + àlluwa_tur, toxal_mbir[àlluwa_tur]);
        if (dëkkuwaay != 0) {
            biir_dëkkuwaay(dëkkuwaay, dëkkuwaay_diir, mbaal_Tegalo.Nàttangoo_dëkkuwaay(mbaal_yombal[기술]), mbaal_Tegalo.상대접속번호(mbaal_yombal[기술]));
            실행관리.수쓰기(dëkkuwaay_diir_dëkkuwaay, 16);
        }
        return 결과;
    }
    static int 통신주소읽기(int 서술자, int dëkkuwaay, int diir_dëkkuwaay) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.kilip(diir_dëkkuwaay, 4)) return -14;
        int diir_xëyma = 실행관리.수(diir_dëkkuwaay);
        if (diir_xëyma < 0) return -22;
        if (!실행관리.kilip(dëkkuwaay, diir_xëyma < 16 ? diir_xëyma : 16)) return -14;
        int xar_xar_dugal_xabaar = mbaal_Tegalo.àlluwa_tur(mbaal_yombal[기술]);
        biir_dëkkuwaay(dëkkuwaay, diir_xëyma, luñu_name[기술], xar_xar_dugal_xabaar < 0 ? 0 : mbaal_Tegalo.접속번호들[xar_xar_dugal_xabaar]);
        실행관리.수쓰기(diir_dëkkuwaay, 16);
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
