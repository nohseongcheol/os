// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 mtumiaji 과정의 파일서술자와 열린 faili 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int soma_andika_alama = 2, unda_ingizo = 64, 독점생성 = 128, ondoa_YAL = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] unda_kishiko = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], lengo = new int[서술자한도];
    static int[] 파일위치 = new int[서술자한도], unda_Mipangilio = new int[서술자한도], 참조수 = new int[서술자한도];
    static int[] Mtandao_kishiko = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] njia_jina = new int[64], hamisha_data = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return unda_kishiko[파일서술자] - 1;
    }
    static int 빈서술자(int endesha) {
        for (int kielezo = endesha; kielezo < 서술자한도; kielezo++) if (unda_kishiko[kielezo] == 0) return kielezo;
        return -24;
    }
    static int tupu_kishiko() {
        for (int kielezo = 0; kielezo < 서술자한도; kielezo++) if (참조수[kielezo] == 0) return kielezo;
        return -24;
    }
    static int UNGANISHA(int 서술자, int 기술, int 파일종류, int faili_lengo, int Mipangilio) {
        unda_kishiko[서술자] = 기술 + 1; 서술자설정[서술자] = (Mipangilio & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; lengo[기술] = faili_lengo; 참조수[기술] = 1;
        unda_Mipangilio[기술] = Mipangilio & (3 | 이어쓰기 | 기다리지않기); 파일위치[기술] = 0;
        Mtandao_kishiko[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void Anza_Mchakato() {
        Safi_Mchakato();
        for (int kielezo = 0; kielezo < 3; kielezo++) UNGANISHA(kielezo, kielezo, 1, kielezo, kielezo == 0 ? 0 : 1);
    }
    static void Safi_Mchakato() {
        for (int kielezo = 0; kielezo < 서술자한도; kielezo++) if (unda_kishiko[kielezo] != 0) funga_faili(kielezo);
    }
    static int funga_faili(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        unda_kishiko[서술자] = 0; 서술자설정[서술자] = 0;
        참조수[기술]--;
        if (참조수[기술] == 0) {
            if (종류[기술] == 2) kumbukumbu_mfumo_ya_mafaili.열림수[lengo[기술]]--;
            if (종류[기술] == 3 && Mtandao_kishiko[기술] != 0) Mtandao_Mpororo.funga(Mtandao_kishiko[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 baiti_thamani 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int anwani) {
        if (!실행관리.dondoo(anwani, 1)) return -14;
        int 위치 = kifaa_thamani.기억읽기(anwani) == '/' ? 1 : 0;
        for (int urefu_thamani = 0; urefu_thamani < 64; urefu_thamani++) {
            if (!실행관리.dondoo(anwani + 위치 + urefu_thamani, 1)) return -14;
            int thamani = kifaa_thamani.기억읽기(anwani + 위치 + urefu_thamani);
            njia_jina[urefu_thamani] = thamani;
            if (thamani == 0) return urefu_thamani == 0 ? -2 : (kumbukumbu_mfumo_ya_mafaili.hundi_jina(njia_jina, urefu_thamani) ? urefu_thamani : -22);
            if (thamani == '/') return -20;
        }
        return -36;
    }
    static int unda_faili(int jina_anwani, int Mipangilio, int 허가) {
        int urefu_thamani = 경로읽기(jina_anwani);
        if (urefu_thamani < 0) return urefu_thamani;
        if ((Mipangilio & ~(3 | unda_ingizo | 독점생성 | ondoa_YAL | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Mipangilio & 3) == 3 || ((Mipangilio & ondoa_YAL) != 0 && (Mipangilio & 3) == 0)) return -22;
        int faili = kumbukumbu_mfumo_ya_mafaili.gundua_ingizo(njia_jina, urefu_thamani);
        if (faili >= 0 && (Mipangilio & (unda_ingizo | 독점생성)) == (unda_ingizo | 독점생성)) return -17;
        if (faili == -2 && (Mipangilio & unda_ingizo) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = tupu_kishiko();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (faili == -2) {
            int 결과 = kumbukumbu_mfumo_ya_mafaili.Store_thamani(njia_jina, urefu_thamani, njia_jina, 0);
            if (결과 < 0) return 결과;
            faili = kumbukumbu_mfumo_ya_mafaili.gundua_ingizo(njia_jina, urefu_thamani);
            kumbukumbu_mfumo_ya_mafaili.허가들[faili] = 허가 & 511;
        }
        if (faili < 0) return faili;
        if ((Mipangilio & ondoa_YAL) != 0) kumbukumbu_mfumo_ya_mafaili.panga_ukubwa_Orodha[faili] = 0;
        kumbukumbu_mfumo_ya_mafaili.열림수[faili]++;
        return UNGANISHA(서술자, 기술, 2, faili, Mipangilio);
    }
    static int 파일읽기(int 서술자, int data_anwani, int urefu_thamani) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (unda_Mipangilio[기술] & 3) == 1) return -9;
        if (urefu_thamani < 0) return -22;
        if (urefu_thamani == 0) return 0;
        if (!실행관리.dondoo(data_anwani, urefu_thamani)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, data_anwani, urefu_thamani, 0, 0);
        if (종류[기술] == 1) {
            int 받은수 = 0;
            while (받은수 < urefu_thamani) {
                int thamani = 문자단말.직렬읽기();
                if (thamani < 0) thamani = kibodi.읽기();
                if (thamani < 0) {
                    if (받은수 > 0) return 받은수;
                    if ((unda_Mipangilio[기술] & 기다리지않기) != 0) return -11;
                    if (kifaa_thamani.사용자남은밀리초() <= 10) return -11;
                    Mtandao_Mpororo.thibitisha(); kifaa_thamani.잠시양보();
                } else {
                    kifaa_thamani.andika_kumbukumbu(data_anwani + 받은수, thamani); 받은수++;
                }
            }
            return 받은수;
        }
        int faili = lengo[기술], 위치 = 파일위치[기술];
        if (위치 >= kumbukumbu_mfumo_ya_mafaili.panga_ukubwa_Orodha[faili]) return 0;
        if (urefu_thamani > kumbukumbu_mfumo_ya_mafaili.panga_ukubwa_Orodha[faili] - 위치) urefu_thamani = kumbukumbu_mfumo_ya_mafaili.panga_ukubwa_Orodha[faili] - 위치;
        int 원본주소 = kifaa_thamani.faili_kumbukumbu() + faili * kumbukumbu_mfumo_ya_mafaili.최대크기 + 위치;
        for (int kielezo = 0; kielezo < urefu_thamani; kielezo++) kifaa_thamani.andika_kumbukumbu(data_anwani + kielezo, kifaa_thamani.기억읽기(원본주소 + kielezo));
        파일위치[기술] += urefu_thamani;
        return urefu_thamani;
    }
    static int andika_faili(int 서술자, int data_anwani, int urefu_thamani) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (unda_Mipangilio[기술] & 3) == 0) return -9;
        if (urefu_thamani < 0) return -22;
        if (urefu_thamani == 0) return 0;
        if (!실행관리.dondoo(data_anwani, urefu_thamani)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 fikio_thamani 주소가 필요하다.
        if (종류[기술] == 1) {
            if (urefu_thamani > 16384) urefu_thamani = 16384;
            for (int kielezo = 0; kielezo < urefu_thamani; kielezo++) {
                int thamani = kifaa_thamani.기억읽기(data_anwani + kielezo);
                문자단말.직렬바이트(thamani); 문자단말.화면문자(thamani);
            }
            return urefu_thamani;
        }
        int faili = lengo[기술], panga_ukubwa = kumbukumbu_mfumo_ya_mafaili.panga_ukubwa_Orodha[faili];
        int 위치 = (unda_Mipangilio[기술] & 이어쓰기) != 0 ? panga_ukubwa : 파일위치[기술];
        if (위치 >= kumbukumbu_mfumo_ya_mafaili.최대크기) return -27;
        if (urefu_thamani > kumbukumbu_mfumo_ya_mafaili.최대크기 - 위치) urefu_thamani = kumbukumbu_mfumo_ya_mafaili.최대크기 - 위치;
        int fikio_anwani = kifaa_thamani.faili_kumbukumbu() + faili * kumbukumbu_mfumo_ya_mafaili.최대크기;
        for (int kielezo = panga_ukubwa; kielezo < 위치; kielezo++) kifaa_thamani.andika_kumbukumbu(fikio_anwani + kielezo, 0);
        for (int kielezo = 0; kielezo < urefu_thamani; kielezo++) kifaa_thamani.andika_kumbukumbu(fikio_anwani + 위치 + kielezo, kifaa_thamani.기억읽기(data_anwani + kielezo));
        파일위치[기술] = 위치 + urefu_thamani;
        if (위치 + urefu_thamani > panga_ukubwa) kumbukumbu_mfumo_ya_mafaili.panga_ukubwa_Orodha[faili] = 위치 + urefu_thamani;
        return urefu_thamani;
    }
    static int tafuta_faili(int 서술자, int Chipua_thamani, int 기준) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (기준 < 0 || 기준 > 2) return -22;
        int nyuma_thamani = 기준 == 0 ? 0 : (기준 == 1 ? 파일위치[기술] : kumbukumbu_mfumo_ya_mafaili.panga_ukubwa_Orodha[lengo[기술]]);
        if (Chipua_thamani > 0 && nyuma_thamani > 2147483647 - Chipua_thamani) return -75;
        if (Chipua_thamani < 0 && Chipua_thamani < -nyuma_thamani) return -22;
        파일위치[기술] = nyuma_thamani + Chipua_thamani;
        return 파일위치[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean pangia_thamani, int Mipangilio) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return pangia_thamani ? -9 : -22;
        if (pangia_thamani && 서술자 == 새서술자) return 새서술자;
        if (pangia_thamani) { if (unda_kishiko[새서술자] != 0) funga_faili(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        unda_kishiko[새서술자] = 기술 + 1; 서술자설정[새서술자] = Mipangilio; 참조수[기술]++;
        return 새서술자;
    }
    static int ondoa_faili_ingizo_jina(int jina_anwani) {
        int urefu_thamani = 경로읽기(jina_anwani);
        if (urefu_thamani < 0) return urefu_thamani;
        int faili = kumbukumbu_mfumo_ya_mafaili.gundua_ingizo(njia_jina, urefu_thamani);
        if (faili < 0) return faili;
        kumbukumbu_mfumo_ya_mafaili.이름들[faili * 64] = 0;
        return 0;
    }
    static int seti_faili_urefu(int 서술자, int urefu_thamani) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (unda_Mipangilio[기술] & 3) == 0 || urefu_thamani < 0) return -22;
        if (urefu_thamani > kumbukumbu_mfumo_ya_mafaili.최대크기) return -27;
        int faili = lengo[기술], anwani = kifaa_thamani.faili_kumbukumbu() + faili * kumbukumbu_mfumo_ya_mafaili.최대크기;
        for (int kielezo = kumbukumbu_mfumo_ya_mafaili.panga_ukubwa_Orodha[faili]; kielezo < urefu_thamani; kielezo++) kifaa_thamani.andika_kumbukumbu(anwani + kielezo, 0);
        kumbukumbu_mfumo_ya_mafaili.panga_ukubwa_Orodha[faili] = urefu_thamani;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int anwani) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.dondoo(anwani, 48)) return -14;
        for (int kielezo = 0; kielezo < 12; kielezo++) 실행관리.수쓰기(anwani + kielezo * 4, 0);
        int faili = lengo[기술], panga_ukubwa = 종류[기술] == 2 ? kumbukumbu_mfumo_ya_mafaili.panga_ukubwa_Orodha[faili] : 0;
        int 허가 = 종류[기술] == 2 ? kumbukumbu_mfumo_ya_mafaili.허가들[faili] : 438;
        실행관리.수쓰기(anwani, 1);
        실행관리.수쓰기(anwani + 4, 종류[기술] == 2 ? faili + 1 : 100 + 기술);
        실행관리.수쓰기(anwani + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(anwani + 12, 종류[기술] == 2 && kumbukumbu_mfumo_ya_mafaili.이름들[faili * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(anwani + 28, panga_ukubwa); 실행관리.수쓰기(anwani + 32, 512);
        실행관리.수쓰기(anwani + 36, (panga_ukubwa + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int amri, int thamani) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (amri == 0 || amri == 1030) return 서술자복제(서술자, thamani, false, amri == 1030 ? 1 : 0);
        if (amri == 1) return 서술자설정[서술자];
        if (amri == 2) { if ((thamani & ~1) != 0) return -22; 서술자설정[서술자] = thamani; return 0; }
        if (amri == 3) return unda_Mipangilio[기술];
        if (amri == 4) {
            if ((thamani & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            unda_Mipangilio[기술] = (unda_Mipangilio[기술] & 3) | (thamani & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int 통신종단점만들기(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = tupu_kishiko();
        if (서술자 < 0 || 기술 < 0) return -24;
        return UNGANISHA(서술자, 기술, 3, 0, soma_andika_alama);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int anwani_32(int anwani) {
        return kifaa_thamani.기억읽기(anwani) << 24 | kifaa_thamani.기억읽기(anwani + 1) << 16
            | kifaa_thamani.기억읽기(anwani + 2) << 8 | kifaa_thamani.기억읽기(anwani + 3);
    }
    static int hundi_anwani(int anwani, int urefu_thamani) {
        if (urefu_thamani < 16) return -22;
        if (!실행관리.dondoo(anwani, 16)) return -14;
        return 실행관리.짧은수(anwani) == 2 ? 0 : -97;
    }
    static int FUNGA_anwani(int 서술자, int anwani, int urefu_thamani) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int 결과 = hundi_anwani(anwani, urefu_thamani);
        if (결과 < 0) return 결과;
        if (Mtandao_kishiko[기술] != 0) return -22;
        int Mtandao_anwani = anwani_32(anwani + 4);
        if (Mtandao_anwani != 0 && Mtandao_anwani != Mtandao_Mpororo.내주소) return -99;
        int namba_ya_kituo = kifaa_thamani.기억읽기(anwani + 2) << 8 | kifaa_thamani.기억읽기(anwani + 3);
        결과 = Mtandao_Mpororo.unda(namba_ya_kituo);
        if (결과 < 0) return 결과;
        Mtandao_kishiko[기술] = 결과; lengo[기술] = Mtandao_anwani;
        return 0;
    }
    static int Otomatiki_FUNGA(int 기술) {
        if (Mtandao_kishiko[기술] != 0) return 0;
        int 결과 = Mtandao_Mpororo.unda(0);
        if (결과 < 0) return 결과;
        Mtandao_kishiko[기술] = 결과;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 요청 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int data_anwani, int urefu_thamani, int Mipangilio, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Mipangilio != 0) return -95;
        if (urefu_thamani < 0 || urefu_thamani > 1024) return -90;
        if (urefu_thamani != 0 && !실행관리.dondoo(data_anwani, urefu_thamani)) return -14;
        if (!실행관리.dondoo(요청주소, 8)) return -14;
        int anwani = 실행관리.수(요청주소);
        int 결과 = hundi_anwani(anwani, 실행관리.수(요청주소 + 4));
        if (결과 < 0) return 결과;
        int namba_ya_kituo = kifaa_thamani.기억읽기(anwani + 2) << 8 | kifaa_thamani.기억읽기(anwani + 3);
        if (namba_ya_kituo == 0) return -22;
        결과 = Otomatiki_FUNGA(기술);
        if (결과 < 0) return 결과;
        for (int kielezo = 0; kielezo < urefu_thamani; kielezo++) hamisha_data[kielezo] = kifaa_thamani.기억읽기(data_anwani + kielezo);
        return Mtandao_Mpororo.tuma(Mtandao_kishiko[기술], anwani_32(anwani + 4), namba_ya_kituo, hamisha_data, urefu_thamani);
    }
    static void andika_anwani(int anwani, int urefu_thamani, int Mtandao_anwani, int namba_ya_kituo) {
        for (int kielezo = 0; kielezo < urefu_thamani && kielezo < 16; kielezo++) {
            int thamani = 0;
            if (kielezo == 0) thamani = 2;
            if (kielezo == 2) thamani = namba_ya_kituo >>> 8;
            if (kielezo == 3) thamani = namba_ya_kituo;
            if (kielezo >= 4 && kielezo < 8) thamani = Mtandao_anwani >>> (56 - kielezo * 8);
            kifaa_thamani.andika_kumbukumbu(anwani + kielezo, thamani & 255);
        }
    }
    static int 자료전문받기(int 서술자, int data_anwani, int urefu_thamani, int Mipangilio, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Mipangilio & ~64) != 0) return -95;
        if (urefu_thamani < 0) return -22;
        if (urefu_thamani != 0 && !실행관리.dondoo(data_anwani, urefu_thamani)) return -14;
        int anwani = 0, anwani_urefu_anwani = 0, anwani_urefu = 0;
        if (요청주소 != 0) {
            if (!실행관리.dondoo(요청주소, 8)) return -14;
            anwani = 실행관리.수(요청주소); anwani_urefu_anwani = 실행관리.수(요청주소 + 4);
            if (anwani != 0) {
                if (!실행관리.dondoo(anwani_urefu_anwani, 4)) return -14;
                anwani_urefu = 실행관리.수(anwani_urefu_anwani);
                if (anwani_urefu < 0) return -22;
                if (!실행관리.dondoo(anwani, anwani_urefu < 16 ? anwani_urefu : 16)) return -14;
            }
        }
        int 결과 = Otomatiki_FUNGA(기술);
        if (결과 < 0) return 결과;
        int endesha = kifaa_thamani.밀리초();
        while (true) {
            결과 = Mtandao_Mpororo.받기(Mtandao_kishiko[기술], hamisha_data, 1024, 0);
            if (결과 != -11) break;
            if ((Mipangilio & 64) != 0 || (unda_Mipangilio[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && kifaa_thamani.밀리초() - endesha >= 수신대기밀리초[기술]) return -11;
            if (kifaa_thamani.사용자남은밀리초() <= 10) return -11;
            kifaa_thamani.잠시양보();
        }
        if (결과 < 0) return 결과;
        if (결과 > urefu_thamani) 결과 = urefu_thamani;
        for (int kielezo = 0; kielezo < 결과; kielezo++) kifaa_thamani.andika_kumbukumbu(data_anwani + kielezo, hamisha_data[kielezo]);
        if (anwani != 0) {
            andika_anwani(anwani, anwani_urefu, Mtandao_Mpororo.kompyuta_rika_anwani(Mtandao_kishiko[기술]), Mtandao_Mpororo.kompyuta_rika_namba_ya_kituo(Mtandao_kishiko[기술]));
            실행관리.수쓰기(anwani_urefu_anwani, 16);
        }
        return 결과;
    }
    static int 통신주소읽기(int 서술자, int anwani, int urefu_anwani) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.dondoo(urefu_anwani, 4)) return -14;
        int urefu_thamani = 실행관리.수(urefu_anwani);
        if (urefu_thamani < 0) return -22;
        if (!실행관리.dondoo(anwani, urefu_thamani < 16 ? urefu_thamani : 16)) return -14;
        int Sloti_ingizo = Mtandao_Mpororo.kielezo(Mtandao_kishiko[기술]);
        andika_anwani(anwani, urefu_thamani, lengo[기술], Sloti_ingizo < 0 ? 0 : Mtandao_Mpororo.접속번호들[Sloti_ingizo]);
        실행관리.수쓰기(urefu_anwani, 16);
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
