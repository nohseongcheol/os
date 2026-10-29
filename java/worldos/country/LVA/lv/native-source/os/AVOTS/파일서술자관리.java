// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 lietotājs 과정의 파일서술자와 열린 Fails 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int 읽기쓰기 = 2, atvērt_ievade = 64, 독점생성 = 128, nodzēst_Satura_rādītājs = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] atvērt_turis = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], mērķis = new int[서술자한도];
    static int[] Fails_amats = new int[서술자한도], atvērt_Iestatījumi = new int[서술자한도], Uzziņas_COUNT = new int[서술자한도];
    static int[] tīkls_turis = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] ceļš_nosaukums = new int[64], nodot_dati = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return atvērt_turis[파일서술자] - 1;
    }
    static int 빈서술자(int Palaist) {
        for (int INDEX = Palaist; INDEX < 서술자한도; INDEX++) if (atvērt_turis[INDEX] == 0) return INDEX;
        return -24;
    }
    static int 빈기술() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (Uzziņas_COUNT[INDEX] == 0) return INDEX;
        return -24;
    }
    static int Savienoties(int 서술자, int 기술, int 파일종류, int Fails_mērķis, int Uzstādījumi) {
        atvērt_turis[서술자] = 기술 + 1; 서술자설정[서술자] = (Uzstādījumi & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; mērķis[기술] = Fails_mērķis; Uzziņas_COUNT[기술] = 1;
        atvērt_Iestatījumi[기술] = Uzstādījumi & (3 | 이어쓰기 | 기다리지않기); Fails_amats[기술] = 0;
        tīkls_turis[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void Sākt_Process() {
        CLEAN_Process();
        for (int INDEX = 0; INDEX < 3; INDEX++) Savienoties(INDEX, INDEX, 1, INDEX, INDEX == 0 ? 0 : 1);
    }
    static void CLEAN_Process() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (atvērt_turis[INDEX] != 0) Aizvērt_Fails(INDEX);
    }
    static int Aizvērt_Fails(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        atvērt_turis[서술자] = 0; 서술자설정[서술자] = 0;
        Uzziņas_COUNT[기술]--;
        if (Uzziņas_COUNT[기술] == 0) {
            if (종류[기술] == 2) atmiņa_failu_sistēma.atvērt_COUNT[mērķis[기술]]--;
            if (종류[기술] == 3 && tīkls_turis[기술] != 0) tīkls_kopa.Aizvērt(tīkls_turis[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 byte_VALUE 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int adrese) {
        if (!실행관리.klips(adrese, 1)) return -14;
        int Novietojums = ierīce_VALUE.기억읽기(adrese) == '/' ? 1 : 0;
        for (int 길이 = 0; 길이 < 64; 길이++) {
            if (!실행관리.klips(adrese + Novietojums + 길이, 1)) return -14;
            int VALUE = ierīce_VALUE.기억읽기(adrese + Novietojums + 길이);
            ceļš_nosaukums[길이] = VALUE;
            if (VALUE == 0) return 길이 == 0 ? -2 : (atmiņa_failu_sistēma.čeks_nosaukums(ceļš_nosaukums, 길이) ? 길이 : -22);
            if (VALUE == '/') return -20;
        }
        return -36;
    }
    static int atvērt_Fails(int nosaukums_adrese, int Uzstādījumi, int 허가) {
        int 길이 = 경로읽기(nosaukums_adrese);
        if (길이 < 0) return 길이;
        if ((Uzstādījumi & ~(3 | atvērt_ievade | 독점생성 | nodzēst_Satura_rādītājs | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Uzstādījumi & 3) == 3 || ((Uzstādījumi & nodzēst_Satura_rādītājs) != 0 && (Uzstādījumi & 3) == 0)) return -22;
        int Fails = atmiņa_failu_sistēma.FIND_ievade(ceļš_nosaukums, 길이);
        if (Fails >= 0 && (Uzstādījumi & (atvērt_ievade | 독점생성)) == (atvērt_ievade | 독점생성)) return -17;
        if (Fails == -2 && (Uzstādījumi & atvērt_ievade) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = 빈기술();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Fails == -2) {
            int mērs = atmiņa_failu_sistēma.Store_VALUE(ceļš_nosaukums, 길이, ceļš_nosaukums, 0);
            if (mērs < 0) return mērs;
            Fails = atmiņa_failu_sistēma.FIND_ievade(ceļš_nosaukums, 길이);
            atmiņa_failu_sistēma.허가들[Fails] = 허가 & 511;
        }
        if (Fails < 0) return Fails;
        if ((Uzstādījumi & nodzēst_Satura_rādītājs) != 0) atmiņa_failu_sistēma.mainīt_izmērus_Saraksts[Fails] = 0;
        atmiņa_failu_sistēma.atvērt_COUNT[Fails]++;
        return Savienoties(서술자, 기술, 2, Fails, Uzstādījumi);
    }
    static int 파일읽기(int 서술자, int dati_adrese, int 길이) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (atvērt_Iestatījumi[기술] & 3) == 1) return -9;
        if (길이 < 0) return -22;
        if (길이 == 0) return 0;
        if (!실행관리.klips(dati_adrese, 길이)) return -14;
        if (종류[기술] == 3) return saņemt_datogramma_dati(서술자, dati_adrese, 길이, 0, 0);
        if (종류[기술] == 1) {
            int RECEIVED_COUNT = 0;
            while (RECEIVED_COUNT < 길이) {
                int VALUE = SMS_Terminālis.직렬읽기();
                if (VALUE < 0) VALUE = tastatūra.Lasīt();
                if (VALUE < 0) {
                    if (RECEIVED_COUNT > 0) return RECEIVED_COUNT;
                    if ((atvērt_Iestatījumi[기술] & 기다리지않기) != 0) return -11;
                    if (ierīce_VALUE.사용자남은밀리초() <= 10) return -11;
                    tīkls_kopa.verificēt(); ierīce_VALUE.잠시양보();
                } else {
                    ierīce_VALUE.rakstīšana_atmiņa(dati_adrese + RECEIVED_COUNT, VALUE); RECEIVED_COUNT++;
                }
            }
            return RECEIVED_COUNT;
        }
        int Fails = mērķis[기술], Novietojums = Fails_amats[기술];
        if (Novietojums >= atmiņa_failu_sistēma.mainīt_izmērus_Saraksts[Fails]) return 0;
        if (길이 > atmiņa_failu_sistēma.mainīt_izmērus_Saraksts[Fails] - Novietojums) 길이 = atmiņa_failu_sistēma.mainīt_izmērus_Saraksts[Fails] - Novietojums;
        int 원본주소 = ierīce_VALUE.Fails_atmiņa() + Fails * atmiņa_failu_sistēma.최대크기 + Novietojums;
        for (int INDEX = 0; INDEX < 길이; INDEX++) ierīce_VALUE.rakstīšana_atmiņa(dati_adrese + INDEX, ierīce_VALUE.기억읽기(원본주소 + INDEX));
        Fails_amats[기술] += 길이;
        return 길이;
    }
    static int rakstīšana_Fails(int 서술자, int dati_adrese, int 길이) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (atvērt_Iestatījumi[기술] & 3) == 0) return -9;
        if (길이 < 0) return -22;
        if (길이 == 0) return 0;
        if (!실행관리.klips(dati_adrese, 길이)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 mērķis_VALUE 주소가 필요하다.
        if (종류[기술] == 1) {
            if (길이 > 16384) 길이 = 16384;
            for (int INDEX = 0; INDEX < 길이; INDEX++) {
                int VALUE = ierīce_VALUE.기억읽기(dati_adrese + INDEX);
                SMS_Terminālis.직렬바이트(VALUE); SMS_Terminālis.화면문자(VALUE);
            }
            return 길이;
        }
        int Fails = mērķis[기술], Izmērs = atmiņa_failu_sistēma.mainīt_izmērus_Saraksts[Fails];
        int Novietojums = (atvērt_Iestatījumi[기술] & 이어쓰기) != 0 ? Izmērs : Fails_amats[기술];
        if (Novietojums >= atmiņa_failu_sistēma.최대크기) return -27;
        if (길이 > atmiņa_failu_sistēma.최대크기 - Novietojums) 길이 = atmiņa_failu_sistēma.최대크기 - Novietojums;
        int mērķis_adrese_08bbd577 = ierīce_VALUE.Fails_atmiņa() + Fails * atmiņa_failu_sistēma.최대크기;
        for (int INDEX = Izmērs; INDEX < Novietojums; INDEX++) ierīce_VALUE.rakstīšana_atmiņa(mērķis_adrese_08bbd577 + INDEX, 0);
        for (int INDEX = 0; INDEX < 길이; INDEX++) ierīce_VALUE.rakstīšana_atmiņa(mērķis_adrese_08bbd577 + Novietojums + INDEX, ierīce_VALUE.기억읽기(dati_adrese + INDEX));
        Fails_amats[기술] = Novietojums + 길이;
        if (Novietojums + 길이 > Izmērs) atmiņa_failu_sistēma.mainīt_izmērus_Saraksts[Fails] = Novietojums + 길이;
        return 길이;
    }
    static int meklēt_Fails(int 서술자, int Nobīde_VALUE, int Project_sakne) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (Project_sakne < 0 || Project_sakne > 2) return -22;
        int Fons_VALUE = Project_sakne == 0 ? 0 : (Project_sakne == 1 ? Fails_amats[기술] : atmiņa_failu_sistēma.mainīt_izmērus_Saraksts[mērķis[기술]]);
        if (Nobīde_VALUE > 0 && Fons_VALUE > 2147483647 - Nobīde_VALUE) return -75;
        if (Nobīde_VALUE < 0 && Nobīde_VALUE < -Fons_VALUE) return -22;
        Fails_amats[기술] = Fons_VALUE + Nobīde_VALUE;
        return Fails_amats[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean nodot_VALUE, int Uzstādījumi) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return nodot_VALUE ? -9 : -22;
        if (nodot_VALUE && 서술자 == 새서술자) return 새서술자;
        if (nodot_VALUE) { if (atvērt_turis[새서술자] != 0) Aizvērt_Fails(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        atvērt_turis[새서술자] = 기술 + 1; 서술자설정[새서술자] = Uzstādījumi; Uzziņas_COUNT[기술]++;
        return 새서술자;
    }
    static int noņemt_Fails_ievade_nosaukums(int nosaukums_adrese) {
        int 길이 = 경로읽기(nosaukums_adrese);
        if (길이 < 0) return 길이;
        int Fails = atmiņa_failu_sistēma.FIND_ievade(ceļš_nosaukums, 길이);
        if (Fails < 0) return Fails;
        atmiņa_failu_sistēma.이름들[Fails * 64] = 0;
        return 0;
    }
    static int 파일길이정하기(int 서술자, int 길이) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (atvērt_Iestatījumi[기술] & 3) == 0 || 길이 < 0) return -22;
        if (길이 > atmiņa_failu_sistēma.최대크기) return -27;
        int Fails = mērķis[기술], adrese = ierīce_VALUE.Fails_atmiņa() + Fails * atmiņa_failu_sistēma.최대크기;
        for (int INDEX = atmiņa_failu_sistēma.mainīt_izmērus_Saraksts[Fails]; INDEX < 길이; INDEX++) ierīce_VALUE.rakstīšana_atmiņa(adrese + INDEX, 0);
        atmiņa_failu_sistēma.mainīt_izmērus_Saraksts[Fails] = 길이;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int adrese) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.klips(adrese, 48)) return -14;
        for (int INDEX = 0; INDEX < 12; INDEX++) 실행관리.rakstīšana_numurs(adrese + INDEX * 4, 0);
        int Fails = mērķis[기술], Izmērs = 종류[기술] == 2 ? atmiņa_failu_sistēma.mainīt_izmērus_Saraksts[Fails] : 0;
        int 허가 = 종류[기술] == 2 ? atmiņa_failu_sistēma.허가들[Fails] : 438;
        실행관리.rakstīšana_numurs(adrese, 1);
        실행관리.rakstīšana_numurs(adrese + 4, 종류[기술] == 2 ? Fails + 1 : 100 + 기술);
        실행관리.rakstīšana_numurs(adrese + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.rakstīšana_numurs(adrese + 12, 종류[기술] == 2 && atmiņa_failu_sistēma.이름들[Fails * 64] == 0 ? 0 : 1);
        실행관리.rakstīšana_numurs(adrese + 28, Izmērs); 실행관리.rakstīšana_numurs(adrese + 32, 512);
        실행관리.rakstīšana_numurs(adrese + 36, (Izmērs + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int Komanda, int VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Komanda == 0 || Komanda == 1030) return 서술자복제(서술자, VALUE, false, Komanda == 1030 ? 1 : 0);
        if (Komanda == 1) return 서술자설정[서술자];
        if (Komanda == 2) { if ((VALUE & ~1) != 0) return -22; 서술자설정[서술자] = VALUE; return 0; }
        if (Komanda == 3) return atvērt_Iestatījumi[기술];
        if (Komanda == 4) {
            if ((VALUE & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            atvērt_Iestatījumi[기술] = (atvērt_Iestatījumi[기술] & 3) | (VALUE & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int atvērt_dalībnieks(int 주소체계, int 통신종류, int līgums_numurs) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (līgums_numurs != 0 && līgums_numurs != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = 빈기술();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Savienoties(서술자, 기술, 3, 0, 읽기쓰기);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int adrese_32(int adrese) {
        return ierīce_VALUE.기억읽기(adrese) << 24 | ierīce_VALUE.기억읽기(adrese + 1) << 16
            | ierīce_VALUE.기억읽기(adrese + 2) << 8 | ierīce_VALUE.기억읽기(adrese + 3);
    }
    static int čeks_adrese(int adrese, int 길이) {
        if (길이 < 16) return -22;
        if (!실행관리.klips(adrese, 16)) return -14;
        return 실행관리.짧은수(adrese) == 2 ? 0 : -97;
    }
    static int BIND_adrese(int 서술자, int adrese, int 길이) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int mērs = čeks_adrese(adrese, 길이);
        if (mērs < 0) return mērs;
        if (tīkls_turis[기술] != 0) return -22;
        int tīkla_ID = adrese_32(adrese + 4);
        if (tīkla_ID != 0 && tīkla_ID != tīkls_kopa.내주소) return -99;
        int porta_numurs = ierīce_VALUE.기억읽기(adrese + 2) << 8 | ierīce_VALUE.기억읽기(adrese + 3);
        mērs = tīkls_kopa.Atvērt(porta_numurs);
        if (mērs < 0) return mērs;
        tīkls_turis[기술] = mērs; mērķis[기술] = tīkla_ID;
        return 0;
    }
    static int Automātiskais_BIND(int 기술) {
        if (tīkls_turis[기술] != 0) return 0;
        int mērs = tīkls_kopa.Atvērt(0);
        if (mērs < 0) return mērs;
        tīkls_turis[기술] = mērs;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 pieprasījums 구조체로 전달한다.
    static int sūtīt_datogramma_dati(int 서술자, int dati_adrese, int 길이, int Uzstādījumi, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Uzstādījumi != 0) return -95;
        if (길이 < 0 || 길이 > 1024) return -90;
        if (길이 != 0 && !실행관리.klips(dati_adrese, 길이)) return -14;
        if (!실행관리.klips(요청주소, 8)) return -14;
        int adrese = 실행관리.numurs(요청주소);
        int mērs = čeks_adrese(adrese, 실행관리.numurs(요청주소 + 4));
        if (mērs < 0) return mērs;
        int porta_numurs = ierīce_VALUE.기억읽기(adrese + 2) << 8 | ierīce_VALUE.기억읽기(adrese + 3);
        if (porta_numurs == 0) return -22;
        mērs = Automātiskais_BIND(기술);
        if (mērs < 0) return mērs;
        for (int INDEX = 0; INDEX < 길이; INDEX++) nodot_dati[INDEX] = ierīce_VALUE.기억읽기(dati_adrese + INDEX);
        return tīkls_kopa.sūtīt(tīkls_turis[기술], adrese_32(adrese + 4), porta_numurs, nodot_dati, 길이);
    }
    static void rakstīšana_adrese(int adrese, int 길이, int tīkla_ID, int porta_numurs) {
        for (int INDEX = 0; INDEX < 길이 && INDEX < 16; INDEX++) {
            int VALUE = 0;
            if (INDEX == 0) VALUE = 2;
            if (INDEX == 2) VALUE = porta_numurs >>> 8;
            if (INDEX == 3) VALUE = porta_numurs;
            if (INDEX >= 4 && INDEX < 8) VALUE = tīkla_ID >>> (56 - INDEX * 8);
            ierīce_VALUE.rakstīšana_atmiņa(adrese + INDEX, VALUE & 255);
        }
    }
    static int saņemt_datogramma_dati(int 서술자, int dati_adrese, int 길이, int Uzstādījumi, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Uzstādījumi & ~64) != 0) return -95;
        if (길이 < 0) return -22;
        if (길이 != 0 && !실행관리.klips(dati_adrese, 길이)) return -14;
        int adrese = 0, 주소길이주소 = 0, 주소길이 = 0;
        if (요청주소 != 0) {
            if (!실행관리.klips(요청주소, 8)) return -14;
            adrese = 실행관리.numurs(요청주소); 주소길이주소 = 실행관리.numurs(요청주소 + 4);
            if (adrese != 0) {
                if (!실행관리.klips(주소길이주소, 4)) return -14;
                주소길이 = 실행관리.numurs(주소길이주소);
                if (주소길이 < 0) return -22;
                if (!실행관리.klips(adrese, 주소길이 < 16 ? 주소길이 : 16)) return -14;
            }
        }
        int mērs = Automātiskais_BIND(기술);
        if (mērs < 0) return mērs;
        int Palaist = ierīce_VALUE.밀리초();
        while (true) {
            mērs = tīkls_kopa.saņemt(tīkls_turis[기술], nodot_dati, 1024, 0);
            if (mērs != -11) break;
            if ((Uzstādījumi & 64) != 0 || (atvērt_Iestatījumi[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && ierīce_VALUE.밀리초() - Palaist >= 수신대기밀리초[기술]) return -11;
            if (ierīce_VALUE.사용자남은밀리초() <= 10) return -11;
            ierīce_VALUE.잠시양보();
        }
        if (mērs < 0) return mērs;
        if (mērs > 길이) mērs = 길이;
        for (int INDEX = 0; INDEX < mērs; INDEX++) ierīce_VALUE.rakstīšana_atmiņa(dati_adrese + INDEX, nodot_dati[INDEX]);
        if (adrese != 0) {
            rakstīšana_adrese(adrese, 주소길이, tīkls_kopa.vienranga_adrese(tīkls_turis[기술]), tīkls_kopa.vienranga_porta_numurs(tīkls_turis[기술]));
            실행관리.rakstīšana_numurs(주소길이주소, 16);
        }
        return mērs;
    }
    static int 통신주소읽기(int 서술자, int adrese, int 길이주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.klips(길이주소, 4)) return -14;
        int 길이 = 실행관리.numurs(길이주소);
        if (길이 < 0) return -22;
        if (!실행관리.klips(adrese, 길이 < 16 ? 길이 : 16)) return -14;
        int 칸 = tīkls_kopa.INDEX(tīkls_turis[기술]);
        rakstīšana_adrese(adrese, 길이, mērķis[기술], 칸 < 0 ? 0 : tīkls_kopa.접속번호들[칸]);
        실행관리.rakstīšana_numurs(길이주소, 16);
        return 0;
    }
    static int kopa_saņemt_NOILGUMS(int 서술자, int 밀리초) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (밀리초 < 0 || 밀리초 > 2000) return -22;
        수신대기밀리초[기술] = 밀리초;
        return 0;
    }
}
