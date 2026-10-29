// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 notandi 과정의 파일서술자와 열린 Skrá 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int les_skrifheimild_flagg = 2, stofna_færsla = 64, 독점생성 = 128, hreinsa_Innihald = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] opið_hald = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], markmið = new int[서술자한도];
    static int[] skrá_staða_2aa21a9a = new int[서술자한도], opið_Stillingar = new int[서술자한도], tilvísun_COUNT = new int[서술자한도];
    static int[] Net_hald = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] slóð_heiti = new int[64], flytja_gögn = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return opið_hald[파일서술자] - 1;
    }
    static int 빈서술자(int Keyra_2) {
        for (int INDEX = Keyra_2; INDEX < 서술자한도; INDEX++) if (opið_hald[INDEX] == 0) return INDEX;
        return -24;
    }
    static int autt_hald() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (tilvísun_COUNT[INDEX] == 0) return INDEX;
        return -24;
    }
    static int Tengjast(int 서술자, int 기술, int 파일종류, int skrá_markmið, int Stillingar) {
        opið_hald[서술자] = 기술 + 1; 서술자설정[서술자] = (Stillingar & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; markmið[기술] = skrá_markmið; tilvísun_COUNT[기술] = 1;
        opið_Stillingar[기술] = Stillingar & (3 | 이어쓰기 | 기다리지않기); skrá_staða_2aa21a9a[기술] = 0;
        Net_hald[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void Opna_Ferli() {
        CLEAN_Ferli();
        for (int INDEX = 0; INDEX < 3; INDEX++) Tengjast(INDEX, INDEX, 1, INDEX, INDEX == 0 ? 0 : 1);
    }
    static void CLEAN_Ferli() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (opið_hald[INDEX] != 0) loka_skrá(INDEX);
    }
    static int loka_skrá(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        opið_hald[서술자] = 0; 서술자설정[서술자] = 0;
        tilvísun_COUNT[기술]--;
        if (tilvísun_COUNT[기술] == 0) {
            if (종류[기술] == 2) Minni_skrárkerfi.opið_COUNT[markmið[기술]]--;
            if (종류[기술] == 3 && Net_hald[기술] != 0) Net_bunki.Loka(Net_hald[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 bæti_VALUE 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int slóð) {
        if (!실행관리.miðlaskrá(slóð, 1)) return -14;
        int Staðsetning = tæki_VALUE.기억읽기(slóð) == '/' ? 1 : 0;
        for (int lengd_VALUE = 0; lengd_VALUE < 64; lengd_VALUE++) {
            if (!실행관리.miðlaskrá(slóð + Staðsetning + lengd_VALUE, 1)) return -14;
            int VALUE = tæki_VALUE.기억읽기(slóð + Staðsetning + lengd_VALUE);
            slóð_heiti[lengd_VALUE] = VALUE;
            if (VALUE == 0) return lengd_VALUE == 0 ? -2 : (Minni_skrárkerfi.athuga_heiti(slóð_heiti, lengd_VALUE) ? lengd_VALUE : -22);
            if (VALUE == '/') return -20;
        }
        return -36;
    }
    static int opið_skrá(int heiti_slóð, int Stillingar, int 허가) {
        int lengd_VALUE = 경로읽기(heiti_slóð);
        if (lengd_VALUE < 0) return lengd_VALUE;
        if ((Stillingar & ~(3 | stofna_færsla | 독점생성 | hreinsa_Innihald | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Stillingar & 3) == 3 || ((Stillingar & hreinsa_Innihald) != 0 && (Stillingar & 3) == 0)) return -22;
        int Skrá = Minni_skrárkerfi.FIND_færsla(slóð_heiti, lengd_VALUE);
        if (Skrá >= 0 && (Stillingar & (stofna_færsla | 독점생성)) == (stofna_færsla | 독점생성)) return -17;
        if (Skrá == -2 && (Stillingar & stofna_færsla) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = autt_hald();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Skrá == -2) {
            int NIÐURSTAÐA = Minni_skrárkerfi.Store_VALUE(slóð_heiti, lengd_VALUE, slóð_heiti, 0);
            if (NIÐURSTAÐA < 0) return NIÐURSTAÐA;
            Skrá = Minni_skrárkerfi.FIND_færsla(slóð_heiti, lengd_VALUE);
            Minni_skrárkerfi.허가들[Skrá] = 허가 & 511;
        }
        if (Skrá < 0) return Skrá;
        if ((Stillingar & hreinsa_Innihald) != 0) Minni_skrárkerfi.breyta_stærð_Listi[Skrá] = 0;
        Minni_skrárkerfi.opið_COUNT[Skrá]++;
        return Tengjast(서술자, 기술, 2, Skrá, Stillingar);
    }
    static int 파일읽기(int 서술자, int gögn_slóð, int lengd_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (opið_Stillingar[기술] & 3) == 1) return -9;
        if (lengd_VALUE < 0) return -22;
        if (lengd_VALUE == 0) return 0;
        if (!실행관리.miðlaskrá(gögn_slóð, lengd_VALUE)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, gögn_slóð, lengd_VALUE, 0, 0);
        if (종류[기술] == 1) {
            int RECEIVED_COUNT = 0;
            while (RECEIVED_COUNT < lengd_VALUE) {
                int VALUE = SMS_Endastöð.직렬읽기();
                if (VALUE < 0) VALUE = lyklaborð.Lestur();
                if (VALUE < 0) {
                    if (RECEIVED_COUNT > 0) return RECEIVED_COUNT;
                    if ((opið_Stillingar[기술] & 기다리지않기) != 0) return -11;
                    if (tæki_VALUE.사용자남은밀리초() <= 10) return -11;
                    Net_bunki.sannprófa(); tæki_VALUE.잠시양보();
                } else {
                    tæki_VALUE.skrifa_Minni(gögn_slóð + RECEIVED_COUNT, VALUE); RECEIVED_COUNT++;
                }
            }
            return RECEIVED_COUNT;
        }
        int Skrá = markmið[기술], Staðsetning = skrá_staða_2aa21a9a[기술];
        if (Staðsetning >= Minni_skrárkerfi.breyta_stærð_Listi[Skrá]) return 0;
        if (lengd_VALUE > Minni_skrárkerfi.breyta_stærð_Listi[Skrá] - Staðsetning) lengd_VALUE = Minni_skrárkerfi.breyta_stærð_Listi[Skrá] - Staðsetning;
        int 원본주소 = tæki_VALUE.skrá_Minni() + Skrá * Minni_skrárkerfi.최대크기 + Staðsetning;
        for (int INDEX = 0; INDEX < lengd_VALUE; INDEX++) tæki_VALUE.skrifa_Minni(gögn_slóð + INDEX, tæki_VALUE.기억읽기(원본주소 + INDEX));
        skrá_staða_2aa21a9a[기술] += lengd_VALUE;
        return lengd_VALUE;
    }
    static int skrifa_skrá(int 서술자, int gögn_slóð, int lengd_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (opið_Stillingar[기술] & 3) == 0) return -9;
        if (lengd_VALUE < 0) return -22;
        if (lengd_VALUE == 0) return 0;
        if (!실행관리.miðlaskrá(gögn_slóð, lengd_VALUE)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 endastaður_VALUE 주소가 필요하다.
        if (종류[기술] == 1) {
            if (lengd_VALUE > 16384) lengd_VALUE = 16384;
            for (int INDEX = 0; INDEX < lengd_VALUE; INDEX++) {
                int VALUE = tæki_VALUE.기억읽기(gögn_slóð + INDEX);
                SMS_Endastöð.직렬바이트(VALUE); SMS_Endastöð.화면문자(VALUE);
            }
            return lengd_VALUE;
        }
        int Skrá = markmið[기술], Stærð = Minni_skrárkerfi.breyta_stærð_Listi[Skrá];
        int Staðsetning = (opið_Stillingar[기술] & 이어쓰기) != 0 ? Stærð : skrá_staða_2aa21a9a[기술];
        if (Staðsetning >= Minni_skrárkerfi.최대크기) return -27;
        if (lengd_VALUE > Minni_skrárkerfi.최대크기 - Staðsetning) lengd_VALUE = Minni_skrárkerfi.최대크기 - Staðsetning;
        int endastaður_slóð_08bbd577 = tæki_VALUE.skrá_Minni() + Skrá * Minni_skrárkerfi.최대크기;
        for (int INDEX = Stærð; INDEX < Staðsetning; INDEX++) tæki_VALUE.skrifa_Minni(endastaður_slóð_08bbd577 + INDEX, 0);
        for (int INDEX = 0; INDEX < lengd_VALUE; INDEX++) tæki_VALUE.skrifa_Minni(endastaður_slóð_08bbd577 + Staðsetning + INDEX, tæki_VALUE.기억읽기(gögn_slóð + INDEX));
        skrá_staða_2aa21a9a[기술] = Staðsetning + lengd_VALUE;
        if (Staðsetning + lengd_VALUE > Stærð) Minni_skrárkerfi.breyta_stærð_Listi[Skrá] = Staðsetning + lengd_VALUE;
        return lengd_VALUE;
    }
    static int leita_skrá(int 서술자, int OFFSET_VALUE, int verk_rót) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (verk_rót < 0 || verk_rót > 2) return -22;
        int veggfóður_VALUE = verk_rót == 0 ? 0 : (verk_rót == 1 ? skrá_staða_2aa21a9a[기술] : Minni_skrárkerfi.breyta_stærð_Listi[markmið[기술]]);
        if (OFFSET_VALUE > 0 && veggfóður_VALUE > 2147483647 - OFFSET_VALUE) return -75;
        if (OFFSET_VALUE < 0 && OFFSET_VALUE < -veggfóður_VALUE) return -22;
        skrá_staða_2aa21a9a[기술] = veggfóður_VALUE + OFFSET_VALUE;
        return skrá_staða_2aa21a9a[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean úthluta_VALUE, int Stillingar) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return úthluta_VALUE ? -9 : -22;
        if (úthluta_VALUE && 서술자 == 새서술자) return 새서술자;
        if (úthluta_VALUE) { if (opið_hald[새서술자] != 0) loka_skrá(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        opið_hald[새서술자] = 기술 + 1; 서술자설정[새서술자] = Stillingar; tilvísun_COUNT[기술]++;
        return 새서술자;
    }
    static int fjarlægja_skrá_færsla_heiti(int heiti_slóð) {
        int lengd_VALUE = 경로읽기(heiti_slóð);
        if (lengd_VALUE < 0) return lengd_VALUE;
        int Skrá = Minni_skrárkerfi.FIND_færsla(slóð_heiti, lengd_VALUE);
        if (Skrá < 0) return Skrá;
        Minni_skrárkerfi.이름들[Skrá * 64] = 0;
        return 0;
    }
    static int sett_skrá_lengd(int 서술자, int lengd_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (opið_Stillingar[기술] & 3) == 0 || lengd_VALUE < 0) return -22;
        if (lengd_VALUE > Minni_skrárkerfi.최대크기) return -27;
        int Skrá = markmið[기술], slóð = tæki_VALUE.skrá_Minni() + Skrá * Minni_skrárkerfi.최대크기;
        for (int INDEX = Minni_skrárkerfi.breyta_stærð_Listi[Skrá]; INDEX < lengd_VALUE; INDEX++) tæki_VALUE.skrifa_Minni(slóð + INDEX, 0);
        Minni_skrárkerfi.breyta_stærð_Listi[Skrá] = lengd_VALUE;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int slóð) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.miðlaskrá(slóð, 48)) return -14;
        for (int INDEX = 0; INDEX < 12; INDEX++) 실행관리.skrifa_númer(slóð + INDEX * 4, 0);
        int Skrá = markmið[기술], Stærð = 종류[기술] == 2 ? Minni_skrárkerfi.breyta_stærð_Listi[Skrá] : 0;
        int 허가 = 종류[기술] == 2 ? Minni_skrárkerfi.허가들[Skrá] : 438;
        실행관리.skrifa_númer(slóð, 1);
        실행관리.skrifa_númer(slóð + 4, 종류[기술] == 2 ? Skrá + 1 : 100 + 기술);
        실행관리.skrifa_númer(slóð + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.skrifa_númer(slóð + 12, 종류[기술] == 2 && Minni_skrárkerfi.이름들[Skrá * 64] == 0 ? 0 : 1);
        실행관리.skrifa_númer(slóð + 28, Stærð); 실행관리.skrifa_númer(slóð + 32, 512);
        실행관리.skrifa_númer(slóð + 36, (Stærð + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int Skipun, int VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Skipun == 0 || Skipun == 1030) return 서술자복제(서술자, VALUE, false, Skipun == 1030 ? 1 : 0);
        if (Skipun == 1) return 서술자설정[서술자];
        if (Skipun == 2) { if ((VALUE & ~1) != 0) return -22; 서술자설정[서술자] = VALUE; return 0; }
        if (Skipun == 3) return opið_Stillingar[기술];
        if (Skipun == 4) {
            if ((VALUE & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            opið_Stillingar[기술] = (opið_Stillingar[기술] & 3) | (VALUE & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int stofna_endastöð(int 주소체계, int 통신종류, int mál_númer) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (mál_númer != 0 && mál_númer != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = autt_hald();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Tengjast(서술자, 기술, 3, 0, les_skrifheimild_flagg);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int slóð_32(int slóð) {
        return tæki_VALUE.기억읽기(slóð) << 24 | tæki_VALUE.기억읽기(slóð + 1) << 16
            | tæki_VALUE.기억읽기(slóð + 2) << 8 | tæki_VALUE.기억읽기(slóð + 3);
    }
    static int athuga_slóð_fc1c397f(int slóð, int lengd_VALUE) {
        if (lengd_VALUE < 16) return -22;
        if (!실행관리.miðlaskrá(slóð, 16)) return -14;
        return 실행관리.짧은수(slóð) == 2 ? 0 : -97;
    }
    static int BIND_slóð(int 서술자, int slóð, int lengd_VALUE) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int NIÐURSTAÐA = athuga_slóð_fc1c397f(slóð, lengd_VALUE);
        if (NIÐURSTAÐA < 0) return NIÐURSTAÐA;
        if (Net_hald[기술] != 0) return -22;
        int Net_slóð = slóð_32(slóð + 4);
        if (Net_slóð != 0 && Net_slóð != Net_bunki.내주소) return -99;
        int tengisnúmer = tæki_VALUE.기억읽기(slóð + 2) << 8 | tæki_VALUE.기억읽기(slóð + 3);
        NIÐURSTAÐA = Net_bunki.Opna(tengisnúmer);
        if (NIÐURSTAÐA < 0) return NIÐURSTAÐA;
        Net_hald[기술] = NIÐURSTAÐA; markmið[기술] = Net_slóð;
        return 0;
    }
    static int sjálfvirk_stilling_BIND(int 기술) {
        if (Net_hald[기술] != 0) return 0;
        int NIÐURSTAÐA = Net_bunki.Opna(0);
        if (NIÐURSTAÐA < 0) return NIÐURSTAÐA;
        Net_hald[기술] = NIÐURSTAÐA;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 요청 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int gögn_slóð, int lengd_VALUE, int Stillingar, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Stillingar != 0) return -95;
        if (lengd_VALUE < 0 || lengd_VALUE > 1024) return -90;
        if (lengd_VALUE != 0 && !실행관리.miðlaskrá(gögn_slóð, lengd_VALUE)) return -14;
        if (!실행관리.miðlaskrá(요청주소, 8)) return -14;
        int slóð = 실행관리.númer(요청주소);
        int NIÐURSTAÐA = athuga_slóð_fc1c397f(slóð, 실행관리.númer(요청주소 + 4));
        if (NIÐURSTAÐA < 0) return NIÐURSTAÐA;
        int tengisnúmer = tæki_VALUE.기억읽기(slóð + 2) << 8 | tæki_VALUE.기억읽기(slóð + 3);
        if (tengisnúmer == 0) return -22;
        NIÐURSTAÐA = sjálfvirk_stilling_BIND(기술);
        if (NIÐURSTAÐA < 0) return NIÐURSTAÐA;
        for (int INDEX = 0; INDEX < lengd_VALUE; INDEX++) flytja_gögn[INDEX] = tæki_VALUE.기억읽기(gögn_slóð + INDEX);
        return Net_bunki.senda(Net_hald[기술], slóð_32(slóð + 4), tengisnúmer, flytja_gögn, lengd_VALUE);
    }
    static void skrifa_slóð(int slóð, int lengd_VALUE, int Net_slóð, int tengisnúmer) {
        for (int INDEX = 0; INDEX < lengd_VALUE && INDEX < 16; INDEX++) {
            int VALUE = 0;
            if (INDEX == 0) VALUE = 2;
            if (INDEX == 2) VALUE = tengisnúmer >>> 8;
            if (INDEX == 3) VALUE = tengisnúmer;
            if (INDEX >= 4 && INDEX < 8) VALUE = Net_slóð >>> (56 - INDEX * 8);
            tæki_VALUE.skrifa_Minni(slóð + INDEX, VALUE & 255);
        }
    }
    static int 자료전문받기(int 서술자, int gögn_slóð, int lengd_VALUE, int Stillingar, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Stillingar & ~64) != 0) return -95;
        if (lengd_VALUE < 0) return -22;
        if (lengd_VALUE != 0 && !실행관리.miðlaskrá(gögn_slóð, lengd_VALUE)) return -14;
        int slóð = 0, slóð_lengd_slóð = 0, slóð_lengd_6e50507f = 0;
        if (요청주소 != 0) {
            if (!실행관리.miðlaskrá(요청주소, 8)) return -14;
            slóð = 실행관리.númer(요청주소); slóð_lengd_slóð = 실행관리.númer(요청주소 + 4);
            if (slóð != 0) {
                if (!실행관리.miðlaskrá(slóð_lengd_slóð, 4)) return -14;
                slóð_lengd_6e50507f = 실행관리.númer(slóð_lengd_slóð);
                if (slóð_lengd_6e50507f < 0) return -22;
                if (!실행관리.miðlaskrá(slóð, slóð_lengd_6e50507f < 16 ? slóð_lengd_6e50507f : 16)) return -14;
            }
        }
        int NIÐURSTAÐA = sjálfvirk_stilling_BIND(기술);
        if (NIÐURSTAÐA < 0) return NIÐURSTAÐA;
        int Keyra_2 = tæki_VALUE.밀리초();
        while (true) {
            NIÐURSTAÐA = Net_bunki.받기(Net_hald[기술], flytja_gögn, 1024, 0);
            if (NIÐURSTAÐA != -11) break;
            if ((Stillingar & 64) != 0 || (opið_Stillingar[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && tæki_VALUE.밀리초() - Keyra_2 >= 수신대기밀리초[기술]) return -11;
            if (tæki_VALUE.사용자남은밀리초() <= 10) return -11;
            tæki_VALUE.잠시양보();
        }
        if (NIÐURSTAÐA < 0) return NIÐURSTAÐA;
        if (NIÐURSTAÐA > lengd_VALUE) NIÐURSTAÐA = lengd_VALUE;
        for (int INDEX = 0; INDEX < NIÐURSTAÐA; INDEX++) tæki_VALUE.skrifa_Minni(gögn_slóð + INDEX, flytja_gögn[INDEX]);
        if (slóð != 0) {
            skrifa_slóð(slóð, slóð_lengd_6e50507f, Net_bunki.jafningi_slóð(Net_hald[기술]), Net_bunki.jafningi_tengisnúmer(Net_hald[기술]));
            실행관리.skrifa_númer(slóð_lengd_slóð, 16);
        }
        return NIÐURSTAÐA;
    }
    static int 통신주소읽기(int 서술자, int slóð, int lengd_slóð) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.miðlaskrá(lengd_slóð, 4)) return -14;
        int lengd_VALUE = 실행관리.númer(lengd_slóð);
        if (lengd_VALUE < 0) return -22;
        if (!실행관리.miðlaskrá(slóð, lengd_VALUE < 16 ? lengd_VALUE : 16)) return -14;
        int rauf_færsla = Net_bunki.INDEX(Net_hald[기술]);
        skrifa_slóð(slóð, lengd_VALUE, markmið[기술], rauf_færsla < 0 ? 0 : Net_bunki.접속번호들[rauf_færsla]);
        실행관리.skrifa_númer(lengd_slóð, 16);
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
