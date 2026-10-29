// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 istifadəçi 과정의 파일서술자와 열린 FAYL 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int oxunan_yazılan_bayraq = 2, yarat_daxiletmə = 64, 독점생성 = 128, təmizləmək_TOC = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] açmaq_tutacaq = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], hədəf = new int[서술자한도];
    static int[] fayl_yerinə_qoymaq = new int[서술자한도], açmaq_Parametrlər = new int[서술자한도], İstinad_COUNT = new int[서술자한도];
    static int[] Şəbəkə_tutacaq = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] yol_ad = new int[64], ötürmə_verilənlər = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return açmaq_tutacaq[파일서술자] - 1;
    }
    static int 빈서술자(int İcra_Et) {
        for (int INDEX = İcra_Et; INDEX < 서술자한도; INDEX++) if (açmaq_tutacaq[INDEX] == 0) return INDEX;
        return -24;
    }
    static int boş_tutacaq() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (İstinad_COUNT[INDEX] == 0) return INDEX;
        return -24;
    }
    static int Bağlan(int 서술자, int 기술, int 파일종류, int fayl_hədəf, int Sazlama) {
        açmaq_tutacaq[서술자] = 기술 + 1; 서술자설정[서술자] = (Sazlama & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; hədəf[기술] = fayl_hədəf; İstinad_COUNT[기술] = 1;
        açmaq_Parametrlər[기술] = Sazlama & (3 | 이어쓰기 | 기다리지않기); fayl_yerinə_qoymaq[기술] = 0;
        Şəbəkə_tutacaq[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void Başla_Proses() {
        CLEAN_Proses();
        for (int INDEX = 0; INDEX < 3; INDEX++) Bağlan(INDEX, INDEX, 1, INDEX, INDEX == 0 ? 0 : 1);
    }
    static void CLEAN_Proses() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (açmaq_tutacaq[INDEX] != 0) bağlamaq_fayl(INDEX);
    }
    static int bağlamaq_fayl(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        açmaq_tutacaq[서술자] = 0; 서술자설정[서술자] = 0;
        İstinad_COUNT[기술]--;
        if (İstinad_COUNT[기술] == 0) {
            if (종류[기술] == 2) Yaddaş_fayl_sistemi.açmaq_COUNT[hədəf[기술]]--;
            if (종류[기술] == 3 && Şəbəkə_tutacaq[기술] != 0) Şəbəkə_Yığın.Bağla(Şəbəkə_tutacaq[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 bayt_VALUE 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int ünvan) {
        if (!실행관리.klip(ünvan, 1)) return -14;
        int yerinə_qoymaq = cihaz_VALUE.기억읽기(ünvan) == '/' ? 1 : 0;
        for (int uzunluq_VALUE = 0; uzunluq_VALUE < 64; uzunluq_VALUE++) {
            if (!실행관리.klip(ünvan + yerinə_qoymaq + uzunluq_VALUE, 1)) return -14;
            int VALUE = cihaz_VALUE.기억읽기(ünvan + yerinə_qoymaq + uzunluq_VALUE);
            yol_ad[uzunluq_VALUE] = VALUE;
            if (VALUE == 0) return uzunluq_VALUE == 0 ? -2 : (Yaddaş_fayl_sistemi.çek_ad(yol_ad, uzunluq_VALUE) ? uzunluq_VALUE : -22);
            if (VALUE == '/') return -20;
        }
        return -36;
    }
    static int açmaq_fayl(int ad_ünvan, int Sazlama, int 허가) {
        int uzunluq_VALUE = 경로읽기(ad_ünvan);
        if (uzunluq_VALUE < 0) return uzunluq_VALUE;
        if ((Sazlama & ~(3 | yarat_daxiletmə | 독점생성 | təmizləmək_TOC | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Sazlama & 3) == 3 || ((Sazlama & təmizləmək_TOC) != 0 && (Sazlama & 3) == 0)) return -22;
        int FAYL = Yaddaş_fayl_sistemi.FIND_daxiletmə(yol_ad, uzunluq_VALUE);
        if (FAYL >= 0 && (Sazlama & (yarat_daxiletmə | 독점생성)) == (yarat_daxiletmə | 독점생성)) return -17;
        if (FAYL == -2 && (Sazlama & yarat_daxiletmə) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = boş_tutacaq();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (FAYL == -2) {
            int ölçü = Yaddaş_fayl_sistemi.Store_VALUE(yol_ad, uzunluq_VALUE, yol_ad, 0);
            if (ölçü < 0) return ölçü;
            FAYL = Yaddaş_fayl_sistemi.FIND_daxiletmə(yol_ad, uzunluq_VALUE);
            Yaddaş_fayl_sistemi.허가들[FAYL] = 허가 & 511;
        }
        if (FAYL < 0) return FAYL;
        if ((Sazlama & təmizləmək_TOC) != 0) Yaddaş_fayl_sistemi.ölçünü_dəyişmək_Siyahı[FAYL] = 0;
        Yaddaş_fayl_sistemi.açmaq_COUNT[FAYL]++;
        return Bağlan(서술자, 기술, 2, FAYL, Sazlama);
    }
    static int 파일읽기(int 서술자, int verilənlər_ünvan, int uzunluq_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (açmaq_Parametrlər[기술] & 3) == 1) return -9;
        if (uzunluq_VALUE < 0) return -22;
        if (uzunluq_VALUE == 0) return 0;
        if (!실행관리.klip(verilənlər_ünvan, uzunluq_VALUE)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, verilənlər_ünvan, uzunluq_VALUE, 0, 0);
        if (종류[기술] == 1) {
            int RECEIVED_COUNT = 0;
            while (RECEIVED_COUNT < uzunluq_VALUE) {
                int VALUE = SMS_Terminal.직렬읽기();
                if (VALUE < 0) VALUE = klaviatura.Oxuma();
                if (VALUE < 0) {
                    if (RECEIVED_COUNT > 0) return RECEIVED_COUNT;
                    if ((açmaq_Parametrlər[기술] & 기다리지않기) != 0) return -11;
                    if (cihaz_VALUE.사용자남은밀리초() <= 10) return -11;
                    Şəbəkə_Yığın.yoxlamaq(); cihaz_VALUE.잠시양보();
                } else {
                    cihaz_VALUE.yazmaq_Yaddaş(verilənlər_ünvan + RECEIVED_COUNT, VALUE); RECEIVED_COUNT++;
                }
            }
            return RECEIVED_COUNT;
        }
        int FAYL = hədəf[기술], yerinə_qoymaq = fayl_yerinə_qoymaq[기술];
        if (yerinə_qoymaq >= Yaddaş_fayl_sistemi.ölçünü_dəyişmək_Siyahı[FAYL]) return 0;
        if (uzunluq_VALUE > Yaddaş_fayl_sistemi.ölçünü_dəyişmək_Siyahı[FAYL] - yerinə_qoymaq) uzunluq_VALUE = Yaddaş_fayl_sistemi.ölçünü_dəyişmək_Siyahı[FAYL] - yerinə_qoymaq;
        int 원본주소 = cihaz_VALUE.fayl_Yaddaş() + FAYL * Yaddaş_fayl_sistemi.최대크기 + yerinə_qoymaq;
        for (int INDEX = 0; INDEX < uzunluq_VALUE; INDEX++) cihaz_VALUE.yazmaq_Yaddaş(verilənlər_ünvan + INDEX, cihaz_VALUE.기억읽기(원본주소 + INDEX));
        fayl_yerinə_qoymaq[기술] += uzunluq_VALUE;
        return uzunluq_VALUE;
    }
    static int yazmaq_fayl(int 서술자, int verilənlər_ünvan, int uzunluq_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (açmaq_Parametrlər[기술] & 3) == 0) return -9;
        if (uzunluq_VALUE < 0) return -22;
        if (uzunluq_VALUE == 0) return 0;
        if (!실행관리.klip(verilənlər_ünvan, uzunluq_VALUE)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 təyinat_VALUE_a0fbc067 주소가 필요하다.
        if (종류[기술] == 1) {
            if (uzunluq_VALUE > 16384) uzunluq_VALUE = 16384;
            for (int INDEX = 0; INDEX < uzunluq_VALUE; INDEX++) {
                int VALUE = cihaz_VALUE.기억읽기(verilənlər_ünvan + INDEX);
                SMS_Terminal.직렬바이트(VALUE); SMS_Terminal.화면문자(VALUE);
            }
            return uzunluq_VALUE;
        }
        int FAYL = hədəf[기술], Böyüklük = Yaddaş_fayl_sistemi.ölçünü_dəyişmək_Siyahı[FAYL];
        int yerinə_qoymaq = (açmaq_Parametrlər[기술] & 이어쓰기) != 0 ? Böyüklük : fayl_yerinə_qoymaq[기술];
        if (yerinə_qoymaq >= Yaddaş_fayl_sistemi.최대크기) return -27;
        if (uzunluq_VALUE > Yaddaş_fayl_sistemi.최대크기 - yerinə_qoymaq) uzunluq_VALUE = Yaddaş_fayl_sistemi.최대크기 - yerinə_qoymaq;
        int təyinat_ünvan = cihaz_VALUE.fayl_Yaddaş() + FAYL * Yaddaş_fayl_sistemi.최대크기;
        for (int INDEX = Böyüklük; INDEX < yerinə_qoymaq; INDEX++) cihaz_VALUE.yazmaq_Yaddaş(təyinat_ünvan + INDEX, 0);
        for (int INDEX = 0; INDEX < uzunluq_VALUE; INDEX++) cihaz_VALUE.yazmaq_Yaddaş(təyinat_ünvan + yerinə_qoymaq + INDEX, cihaz_VALUE.기억읽기(verilənlər_ünvan + INDEX));
        fayl_yerinə_qoymaq[기술] = yerinə_qoymaq + uzunluq_VALUE;
        if (yerinə_qoymaq + uzunluq_VALUE > Böyüklük) Yaddaş_fayl_sistemi.ölçünü_dəyişmək_Siyahı[FAYL] = yerinə_qoymaq + uzunluq_VALUE;
        return uzunluq_VALUE;
    }
    static int axtarmaq_fayl(int 서술자, int OFFSET_VALUE, int Project_kök) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (Project_kök < 0 || Project_kök > 2) return -22;
        int Fon_VALUE = Project_kök == 0 ? 0 : (Project_kök == 1 ? fayl_yerinə_qoymaq[기술] : Yaddaş_fayl_sistemi.ölçünü_dəyişmək_Siyahı[hədəf[기술]]);
        if (OFFSET_VALUE > 0 && Fon_VALUE > 2147483647 - OFFSET_VALUE) return -75;
        if (OFFSET_VALUE < 0 && OFFSET_VALUE < -Fon_VALUE) return -22;
        fayl_yerinə_qoymaq[기술] = Fon_VALUE + OFFSET_VALUE;
        return fayl_yerinə_qoymaq[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean təyin_et_VALUE, int Sazlama) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return təyin_et_VALUE ? -9 : -22;
        if (təyin_et_VALUE && 서술자 == 새서술자) return 새서술자;
        if (təyin_et_VALUE) { if (açmaq_tutacaq[새서술자] != 0) bağlamaq_fayl(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        açmaq_tutacaq[새서술자] = 기술 + 1; 서술자설정[새서술자] = Sazlama; İstinad_COUNT[기술]++;
        return 새서술자;
    }
    static int silmək_fayl_daxiletmə_ad(int ad_ünvan) {
        int uzunluq_VALUE = 경로읽기(ad_ünvan);
        if (uzunluq_VALUE < 0) return uzunluq_VALUE;
        int FAYL = Yaddaş_fayl_sistemi.FIND_daxiletmə(yol_ad, uzunluq_VALUE);
        if (FAYL < 0) return FAYL;
        Yaddaş_fayl_sistemi.이름들[FAYL * 64] = 0;
        return 0;
    }
    static int Dəst_fayl_uzunluq(int 서술자, int uzunluq_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (açmaq_Parametrlər[기술] & 3) == 0 || uzunluq_VALUE < 0) return -22;
        if (uzunluq_VALUE > Yaddaş_fayl_sistemi.최대크기) return -27;
        int FAYL = hədəf[기술], ünvan = cihaz_VALUE.fayl_Yaddaş() + FAYL * Yaddaş_fayl_sistemi.최대크기;
        for (int INDEX = Yaddaş_fayl_sistemi.ölçünü_dəyişmək_Siyahı[FAYL]; INDEX < uzunluq_VALUE; INDEX++) cihaz_VALUE.yazmaq_Yaddaş(ünvan + INDEX, 0);
        Yaddaş_fayl_sistemi.ölçünü_dəyişmək_Siyahı[FAYL] = uzunluq_VALUE;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int ünvan) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.klip(ünvan, 48)) return -14;
        for (int INDEX = 0; INDEX < 12; INDEX++) 실행관리.수쓰기(ünvan + INDEX * 4, 0);
        int FAYL = hədəf[기술], Böyüklük = 종류[기술] == 2 ? Yaddaş_fayl_sistemi.ölçünü_dəyişmək_Siyahı[FAYL] : 0;
        int 허가 = 종류[기술] == 2 ? Yaddaş_fayl_sistemi.허가들[FAYL] : 438;
        실행관리.수쓰기(ünvan, 1);
        실행관리.수쓰기(ünvan + 4, 종류[기술] == 2 ? FAYL + 1 : 100 + 기술);
        실행관리.수쓰기(ünvan + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(ünvan + 12, 종류[기술] == 2 && Yaddaş_fayl_sistemi.이름들[FAYL * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(ünvan + 28, Böyüklük); 실행관리.수쓰기(ünvan + 32, 512);
        실행관리.수쓰기(ünvan + 36, (Böyüklük + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int Əmr, int VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Əmr == 0 || Əmr == 1030) return 서술자복제(서술자, VALUE, false, Əmr == 1030 ? 1 : 0);
        if (Əmr == 1) return 서술자설정[서술자];
        if (Əmr == 2) { if ((VALUE & ~1) != 0) return -22; 서술자설정[서술자] = VALUE; return 0; }
        if (Əmr == 3) return açmaq_Parametrlər[기술];
        if (Əmr == 4) {
            if ((VALUE & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            açmaq_Parametrlər[기술] = (açmaq_Parametrlər[기술] & 3) | (VALUE & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int 통신종단점만들기(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = boş_tutacaq();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Bağlan(서술자, 기술, 3, 0, oxunan_yazılan_bayraq);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int ünvan_32(int ünvan) {
        return cihaz_VALUE.기억읽기(ünvan) << 24 | cihaz_VALUE.기억읽기(ünvan + 1) << 16
            | cihaz_VALUE.기억읽기(ünvan + 2) << 8 | cihaz_VALUE.기억읽기(ünvan + 3);
    }
    static int çek_ünvan(int ünvan, int uzunluq_VALUE) {
        if (uzunluq_VALUE < 16) return -22;
        if (!실행관리.klip(ünvan, 16)) return -14;
        return 실행관리.짧은수(ünvan) == 2 ? 0 : -97;
    }
    static int BIND_ünvan(int 서술자, int ünvan, int uzunluq_VALUE) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int ölçü = çek_ünvan(ünvan, uzunluq_VALUE);
        if (ölçü < 0) return ölçü;
        if (Şəbəkə_tutacaq[기술] != 0) return -22;
        int Şəbəkə_ünvan = ünvan_32(ünvan + 4);
        if (Şəbəkə_ünvan != 0 && Şəbəkə_ünvan != Şəbəkə_Yığın.내주소) return -99;
        int 접속번호 = cihaz_VALUE.기억읽기(ünvan + 2) << 8 | cihaz_VALUE.기억읽기(ünvan + 3);
        ölçü = Şəbəkə_Yığın.Aç(접속번호);
        if (ölçü < 0) return ölçü;
        Şəbəkə_tutacaq[기술] = ölçü; hədəf[기술] = Şəbəkə_ünvan;
        return 0;
    }
    static int Avtomatik_BIND(int 기술) {
        if (Şəbəkə_tutacaq[기술] != 0) return 0;
        int ölçü = Şəbəkə_Yığın.Aç(0);
        if (ölçü < 0) return ölçü;
        Şəbəkə_tutacaq[기술] = ölçü;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 HTTP_sorğusu 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int verilənlər_ünvan, int uzunluq_VALUE, int Sazlama, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Sazlama != 0) return -95;
        if (uzunluq_VALUE < 0 || uzunluq_VALUE > 1024) return -90;
        if (uzunluq_VALUE != 0 && !실행관리.klip(verilənlər_ünvan, uzunluq_VALUE)) return -14;
        if (!실행관리.klip(요청주소, 8)) return -14;
        int ünvan = 실행관리.수(요청주소);
        int ölçü = çek_ünvan(ünvan, 실행관리.수(요청주소 + 4));
        if (ölçü < 0) return ölçü;
        int 접속번호 = cihaz_VALUE.기억읽기(ünvan + 2) << 8 | cihaz_VALUE.기억읽기(ünvan + 3);
        if (접속번호 == 0) return -22;
        ölçü = Avtomatik_BIND(기술);
        if (ölçü < 0) return ölçü;
        for (int INDEX = 0; INDEX < uzunluq_VALUE; INDEX++) ötürmə_verilənlər[INDEX] = cihaz_VALUE.기억읽기(verilənlər_ünvan + INDEX);
        return Şəbəkə_Yığın.göndərmək(Şəbəkə_tutacaq[기술], ünvan_32(ünvan + 4), 접속번호, ötürmə_verilənlər, uzunluq_VALUE);
    }
    static void yazmaq_ünvan(int ünvan, int uzunluq_VALUE, int Şəbəkə_ünvan, int 접속번호) {
        for (int INDEX = 0; INDEX < uzunluq_VALUE && INDEX < 16; INDEX++) {
            int VALUE = 0;
            if (INDEX == 0) VALUE = 2;
            if (INDEX == 2) VALUE = 접속번호 >>> 8;
            if (INDEX == 3) VALUE = 접속번호;
            if (INDEX >= 4 && INDEX < 8) VALUE = Şəbəkə_ünvan >>> (56 - INDEX * 8);
            cihaz_VALUE.yazmaq_Yaddaş(ünvan + INDEX, VALUE & 255);
        }
    }
    static int 자료전문받기(int 서술자, int verilənlər_ünvan, int uzunluq_VALUE, int Sazlama, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Sazlama & ~64) != 0) return -95;
        if (uzunluq_VALUE < 0) return -22;
        if (uzunluq_VALUE != 0 && !실행관리.klip(verilənlər_ünvan, uzunluq_VALUE)) return -14;
        int ünvan = 0, ünvan_uzunluq_ünvan = 0, ünvan_uzunluq = 0;
        if (요청주소 != 0) {
            if (!실행관리.klip(요청주소, 8)) return -14;
            ünvan = 실행관리.수(요청주소); ünvan_uzunluq_ünvan = 실행관리.수(요청주소 + 4);
            if (ünvan != 0) {
                if (!실행관리.klip(ünvan_uzunluq_ünvan, 4)) return -14;
                ünvan_uzunluq = 실행관리.수(ünvan_uzunluq_ünvan);
                if (ünvan_uzunluq < 0) return -22;
                if (!실행관리.klip(ünvan, ünvan_uzunluq < 16 ? ünvan_uzunluq : 16)) return -14;
            }
        }
        int ölçü = Avtomatik_BIND(기술);
        if (ölçü < 0) return ölçü;
        int İcra_Et = cihaz_VALUE.밀리초();
        while (true) {
            ölçü = Şəbəkə_Yığın.받기(Şəbəkə_tutacaq[기술], ötürmə_verilənlər, 1024, 0);
            if (ölçü != -11) break;
            if ((Sazlama & 64) != 0 || (açmaq_Parametrlər[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && cihaz_VALUE.밀리초() - İcra_Et >= 수신대기밀리초[기술]) return -11;
            if (cihaz_VALUE.사용자남은밀리초() <= 10) return -11;
            cihaz_VALUE.잠시양보();
        }
        if (ölçü < 0) return ölçü;
        if (ölçü > uzunluq_VALUE) ölçü = uzunluq_VALUE;
        for (int INDEX = 0; INDEX < ölçü; INDEX++) cihaz_VALUE.yazmaq_Yaddaş(verilənlər_ünvan + INDEX, ötürmə_verilənlər[INDEX]);
        if (ünvan != 0) {
            yazmaq_ünvan(ünvan, ünvan_uzunluq, Şəbəkə_Yığın.eynisəviyyəli_ünvan(Şəbəkə_tutacaq[기술]), Şəbəkə_Yığın.상대접속번호(Şəbəkə_tutacaq[기술]));
            실행관리.수쓰기(ünvan_uzunluq_ünvan, 16);
        }
        return ölçü;
    }
    static int 통신주소읽기(int 서술자, int ünvan, int uzunluq_ünvan) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.klip(uzunluq_ünvan, 4)) return -14;
        int uzunluq_VALUE = 실행관리.수(uzunluq_ünvan);
        if (uzunluq_VALUE < 0) return -22;
        if (!실행관리.klip(ünvan, uzunluq_VALUE < 16 ? uzunluq_VALUE : 16)) return -14;
        int slot_daxiletmə = Şəbəkə_Yığın.INDEX(Şəbəkə_tutacaq[기술]);
        yazmaq_ünvan(ünvan, uzunluq_VALUE, hədəf[기술], slot_daxiletmə < 0 ? 0 : Şəbəkə_Yığın.접속번호들[slot_daxiletmə]);
        실행관리.수쓰기(uzunluq_ünvan, 16);
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
