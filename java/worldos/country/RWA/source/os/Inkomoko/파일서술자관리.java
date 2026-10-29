// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 ukoresha 과정의 파일서술자와 열린 Idosiye 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int gusoma_kwandika_akabendera = 2, kurema_icyinjizwa = 64, 독점생성 = 128, gukuraho_TOC = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] kurema_umukondo = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], gusimbuza_igishya = new int[서술자한도];
    static int[] 파일위치 = new int[서술자한도], kurema_Amagenamiterere = new int[서술자한도], 참조수 = new int[서술자한도];
    static int[] Urusobemiyoboro_umukondo = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] inzira_izina = new int[64], iyimura_amakurushingiro = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return kurema_umukondo[파일서술자] - 1;
    }
    static int 빈서술자(int ihuriro) {
        for (int umugerekashakiro = ihuriro; umugerekashakiro < 서술자한도; umugerekashakiro++) if (kurema_umukondo[umugerekashakiro] == 0) return umugerekashakiro;
        return -24;
    }
    static int irimo_ubusa_umukondo() {
        for (int umugerekashakiro = 0; umugerekashakiro < 서술자한도; umugerekashakiro++) if (참조수[umugerekashakiro] == 0) return umugerekashakiro;
        return -24;
    }
    static int Guhuza(int 서술자, int 기술, int 파일종류, int dosiye_gusimbuza_igishya, int Amagenamiterere) {
        kurema_umukondo[서술자] = 기술 + 1; 서술자설정[서술자] = (Amagenamiterere & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; gusimbuza_igishya[기술] = dosiye_gusimbuza_igishya; 참조수[기술] = 1;
        kurema_Amagenamiterere[기술] = Amagenamiterere & (3 | 이어쓰기 | 기다리지않기); 파일위치[기술] = 0;
        Urusobemiyoboro_umukondo[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void Itangira_Inzira() {
        과정정리();
        for (int umugerekashakiro = 0; umugerekashakiro < 3; umugerekashakiro++) Guhuza(umugerekashakiro, umugerekashakiro, 1, umugerekashakiro, umugerekashakiro == 0 ? 0 : 1);
    }
    static void 과정정리() {
        for (int umugerekashakiro = 0; umugerekashakiro < 서술자한도; umugerekashakiro++) if (kurema_umukondo[umugerekashakiro] != 0) gufunga_dosiye(umugerekashakiro);
    }
    static int gufunga_dosiye(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        kurema_umukondo[서술자] = 0; 서술자설정[서술자] = 0;
        참조수[기술]--;
        if (참조수[기술] == 0) {
            if (종류[기술] == 2) ububiko_sisitemu_ya_dosiye.열림수[gusimbuza_igishya[기술]]--;
            if (종류[기술] == 3 && Urusobemiyoboro_umukondo[기술] != 0) Urusobemiyoboro_Ikirundo.Gufunga(Urusobemiyoboro_umukondo[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 bayiti_agaciro 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int aderesi) {
        if (!실행관리.kiripu(aderesi, 1)) return -14;
        int 위치 = igendanwa_agaciro.기억읽기(aderesi) == '/' ? 1 : 0;
        for (int uburebure_agaciro = 0; uburebure_agaciro < 64; uburebure_agaciro++) {
            if (!실행관리.kiripu(aderesi + 위치 + uburebure_agaciro, 1)) return -14;
            int agaciro = igendanwa_agaciro.기억읽기(aderesi + 위치 + uburebure_agaciro);
            inzira_izina[uburebure_agaciro] = agaciro;
            if (agaciro == 0) return uburebure_agaciro == 0 ? -2 : (ububiko_sisitemu_ya_dosiye.sheki_izina(inzira_izina, uburebure_agaciro) ? uburebure_agaciro : -22);
            if (agaciro == '/') return -20;
        }
        return -36;
    }
    static int kurema_dosiye(int izina_aderesi, int Amagenamiterere, int 허가) {
        int uburebure_agaciro = 경로읽기(izina_aderesi);
        if (uburebure_agaciro < 0) return uburebure_agaciro;
        if ((Amagenamiterere & ~(3 | kurema_icyinjizwa | 독점생성 | gukuraho_TOC | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Amagenamiterere & 3) == 3 || ((Amagenamiterere & gukuraho_TOC) != 0 && (Amagenamiterere & 3) == 0)) return -22;
        int Idosiye = ububiko_sisitemu_ya_dosiye.gushaka_icyinjizwa(inzira_izina, uburebure_agaciro);
        if (Idosiye >= 0 && (Amagenamiterere & (kurema_icyinjizwa | 독점생성)) == (kurema_icyinjizwa | 독점생성)) return -17;
        if (Idosiye == -2 && (Amagenamiterere & kurema_icyinjizwa) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = irimo_ubusa_umukondo();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Idosiye == -2) {
            int 결과 = ububiko_sisitemu_ya_dosiye.Store_agaciro(inzira_izina, uburebure_agaciro, inzira_izina, 0);
            if (결과 < 0) return 결과;
            Idosiye = ububiko_sisitemu_ya_dosiye.gushaka_icyinjizwa(inzira_izina, uburebure_agaciro);
            ububiko_sisitemu_ya_dosiye.허가들[Idosiye] = 허가 & 511;
        }
        if (Idosiye < 0) return Idosiye;
        if ((Amagenamiterere & gukuraho_TOC) != 0) ububiko_sisitemu_ya_dosiye.ingano_Urutonde[Idosiye] = 0;
        ububiko_sisitemu_ya_dosiye.열림수[Idosiye]++;
        return Guhuza(서술자, 기술, 2, Idosiye, Amagenamiterere);
    }
    static int 파일읽기(int 서술자, int amakurushingiro_aderesi, int uburebure_agaciro) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (kurema_Amagenamiterere[기술] & 3) == 1) return -9;
        if (uburebure_agaciro < 0) return -22;
        if (uburebure_agaciro == 0) return 0;
        if (!실행관리.kiripu(amakurushingiro_aderesi, uburebure_agaciro)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, amakurushingiro_aderesi, uburebure_agaciro, 0, 0);
        if (종류[기술] == 1) {
            int 받은수 = 0;
            while (받은수 < uburebure_agaciro) {
                int agaciro = 문자단말.직렬읽기();
                if (agaciro < 0) agaciro = mwandikisho.읽기();
                if (agaciro < 0) {
                    if (받은수 > 0) return 받은수;
                    if ((kurema_Amagenamiterere[기술] & 기다리지않기) != 0) return -11;
                    if (igendanwa_agaciro.사용자남은밀리초() <= 10) return -11;
                    Urusobemiyoboro_Ikirundo.gusuzuma(); igendanwa_agaciro.잠시양보();
                } else {
                    igendanwa_agaciro.kwandika_ububiko(amakurushingiro_aderesi + 받은수, agaciro); 받은수++;
                }
            }
            return 받은수;
        }
        int Idosiye = gusimbuza_igishya[기술], 위치 = 파일위치[기술];
        if (위치 >= ububiko_sisitemu_ya_dosiye.ingano_Urutonde[Idosiye]) return 0;
        if (uburebure_agaciro > ububiko_sisitemu_ya_dosiye.ingano_Urutonde[Idosiye] - 위치) uburebure_agaciro = ububiko_sisitemu_ya_dosiye.ingano_Urutonde[Idosiye] - 위치;
        int 원본주소 = igendanwa_agaciro.dosiye_ububiko() + Idosiye * ububiko_sisitemu_ya_dosiye.최대크기 + 위치;
        for (int umugerekashakiro = 0; umugerekashakiro < uburebure_agaciro; umugerekashakiro++) igendanwa_agaciro.kwandika_ububiko(amakurushingiro_aderesi + umugerekashakiro, igendanwa_agaciro.기억읽기(원본주소 + umugerekashakiro));
        파일위치[기술] += uburebure_agaciro;
        return uburebure_agaciro;
    }
    static int kwandika_dosiye(int 서술자, int amakurushingiro_aderesi, int uburebure_agaciro) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (kurema_Amagenamiterere[기술] & 3) == 0) return -9;
        if (uburebure_agaciro < 0) return -22;
        if (uburebure_agaciro == 0) return 0;
        if (!실행관리.kiripu(amakurushingiro_aderesi, uburebure_agaciro)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 aho_ijya_agaciro 주소가 필요하다.
        if (종류[기술] == 1) {
            if (uburebure_agaciro > 16384) uburebure_agaciro = 16384;
            for (int umugerekashakiro = 0; umugerekashakiro < uburebure_agaciro; umugerekashakiro++) {
                int agaciro = igendanwa_agaciro.기억읽기(amakurushingiro_aderesi + umugerekashakiro);
                문자단말.직렬바이트(agaciro); 문자단말.화면문자(agaciro);
            }
            return uburebure_agaciro;
        }
        int Idosiye = gusimbuza_igishya[기술], Ingano = ububiko_sisitemu_ya_dosiye.ingano_Urutonde[Idosiye];
        int 위치 = (kurema_Amagenamiterere[기술] & 이어쓰기) != 0 ? Ingano : 파일위치[기술];
        if (위치 >= ububiko_sisitemu_ya_dosiye.최대크기) return -27;
        if (uburebure_agaciro > ububiko_sisitemu_ya_dosiye.최대크기 - 위치) uburebure_agaciro = ububiko_sisitemu_ya_dosiye.최대크기 - 위치;
        int aho_ijya_aderesi = igendanwa_agaciro.dosiye_ububiko() + Idosiye * ububiko_sisitemu_ya_dosiye.최대크기;
        for (int umugerekashakiro = Ingano; umugerekashakiro < 위치; umugerekashakiro++) igendanwa_agaciro.kwandika_ububiko(aho_ijya_aderesi + umugerekashakiro, 0);
        for (int umugerekashakiro = 0; umugerekashakiro < uburebure_agaciro; umugerekashakiro++) igendanwa_agaciro.kwandika_ububiko(aho_ijya_aderesi + 위치 + umugerekashakiro, igendanwa_agaciro.기억읽기(amakurushingiro_aderesi + umugerekashakiro));
        파일위치[기술] = 위치 + uburebure_agaciro;
        if (위치 + uburebure_agaciro > Ingano) ububiko_sisitemu_ya_dosiye.ingano_Urutonde[Idosiye] = 위치 + uburebure_agaciro;
        return uburebure_agaciro;
    }
    static int 파일위치옮기기(int 서술자, int Ofuseti_agaciro, int 기준) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (기준 < 0 || 기준 > 2) return -22;
        int Imbuganyuma_agaciro = 기준 == 0 ? 0 : (기준 == 1 ? 파일위치[기술] : ububiko_sisitemu_ya_dosiye.ingano_Urutonde[gusimbuza_igishya[기술]]);
        if (Ofuseti_agaciro > 0 && Imbuganyuma_agaciro > 2147483647 - Ofuseti_agaciro) return -75;
        if (Ofuseti_agaciro < 0 && Ofuseti_agaciro < -Imbuganyuma_agaciro) return -22;
        파일위치[기술] = Imbuganyuma_agaciro + Ofuseti_agaciro;
        return 파일위치[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean 지정, int Amagenamiterere) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return 지정 ? -9 : -22;
        if (지정 && 서술자 == 새서술자) return 새서술자;
        if (지정) { if (kurema_umukondo[새서술자] != 0) gufunga_dosiye(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        kurema_umukondo[새서술자] = 기술 + 1; 서술자설정[새서술자] = Amagenamiterere; 참조수[기술]++;
        return 새서술자;
    }
    static int gukuramo_dosiye_icyinjizwa_izina(int izina_aderesi) {
        int uburebure_agaciro = 경로읽기(izina_aderesi);
        if (uburebure_agaciro < 0) return uburebure_agaciro;
        int Idosiye = ububiko_sisitemu_ya_dosiye.gushaka_icyinjizwa(inzira_izina, uburebure_agaciro);
        if (Idosiye < 0) return Idosiye;
        ububiko_sisitemu_ya_dosiye.이름들[Idosiye * 64] = 0;
        return 0;
    }
    static int itsinda_dosiye_uburebure(int 서술자, int uburebure_agaciro) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (kurema_Amagenamiterere[기술] & 3) == 0 || uburebure_agaciro < 0) return -22;
        if (uburebure_agaciro > ububiko_sisitemu_ya_dosiye.최대크기) return -27;
        int Idosiye = gusimbuza_igishya[기술], aderesi = igendanwa_agaciro.dosiye_ububiko() + Idosiye * ububiko_sisitemu_ya_dosiye.최대크기;
        for (int umugerekashakiro = ububiko_sisitemu_ya_dosiye.ingano_Urutonde[Idosiye]; umugerekashakiro < uburebure_agaciro; umugerekashakiro++) igendanwa_agaciro.kwandika_ububiko(aderesi + umugerekashakiro, 0);
        ububiko_sisitemu_ya_dosiye.ingano_Urutonde[Idosiye] = uburebure_agaciro;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int aderesi) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.kiripu(aderesi, 48)) return -14;
        for (int umugerekashakiro = 0; umugerekashakiro < 12; umugerekashakiro++) 실행관리.수쓰기(aderesi + umugerekashakiro * 4, 0);
        int Idosiye = gusimbuza_igishya[기술], Ingano = 종류[기술] == 2 ? ububiko_sisitemu_ya_dosiye.ingano_Urutonde[Idosiye] : 0;
        int 허가 = 종류[기술] == 2 ? ububiko_sisitemu_ya_dosiye.허가들[Idosiye] : 438;
        실행관리.수쓰기(aderesi, 1);
        실행관리.수쓰기(aderesi + 4, 종류[기술] == 2 ? Idosiye + 1 : 100 + 기술);
        실행관리.수쓰기(aderesi + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(aderesi + 12, 종류[기술] == 2 && ububiko_sisitemu_ya_dosiye.이름들[Idosiye * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(aderesi + 28, Ingano); 실행관리.수쓰기(aderesi + 32, 512);
        실행관리.수쓰기(aderesi + 36, (Ingano + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int Icyo_wifuza, int agaciro) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Icyo_wifuza == 0 || Icyo_wifuza == 1030) return 서술자복제(서술자, agaciro, false, Icyo_wifuza == 1030 ? 1 : 0);
        if (Icyo_wifuza == 1) return 서술자설정[서술자];
        if (Icyo_wifuza == 2) { if ((agaciro & ~1) != 0) return -22; 서술자설정[서술자] = agaciro; return 0; }
        if (Icyo_wifuza == 3) return kurema_Amagenamiterere[기술];
        if (Icyo_wifuza == 4) {
            if ((agaciro & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            kurema_Amagenamiterere[기술] = (kurema_Amagenamiterere[기술] & 3) | (agaciro & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int 통신종단점만들기(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = irimo_ubusa_umukondo();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Guhuza(서술자, 기술, 3, 0, gusoma_kwandika_akabendera);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int aderesi_32(int aderesi) {
        return igendanwa_agaciro.기억읽기(aderesi) << 24 | igendanwa_agaciro.기억읽기(aderesi + 1) << 16
            | igendanwa_agaciro.기억읽기(aderesi + 2) << 8 | igendanwa_agaciro.기억읽기(aderesi + 3);
    }
    static int sheki_aderesi(int aderesi, int uburebure_agaciro) {
        if (uburebure_agaciro < 16) return -22;
        if (!실행관리.kiripu(aderesi, 16)) return -14;
        return 실행관리.짧은수(aderesi) == 2 ? 0 : -97;
    }
    static int BIND_aderesi(int 서술자, int aderesi, int uburebure_agaciro) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int 결과 = sheki_aderesi(aderesi, uburebure_agaciro);
        if (결과 < 0) return 결과;
        if (Urusobemiyoboro_umukondo[기술] != 0) return -22;
        int Urusobemiyoboro_aderesi = aderesi_32(aderesi + 4);
        if (Urusobemiyoboro_aderesi != 0 && Urusobemiyoboro_aderesi != Urusobemiyoboro_Ikirundo.내주소) return -99;
        int 접속번호 = igendanwa_agaciro.기억읽기(aderesi + 2) << 8 | igendanwa_agaciro.기억읽기(aderesi + 3);
        결과 = Urusobemiyoboro_Ikirundo.Gufungura(접속번호);
        if (결과 < 0) return 결과;
        Urusobemiyoboro_umukondo[기술] = 결과; gusimbuza_igishya[기술] = Urusobemiyoboro_aderesi;
        return 0;
    }
    static int 자동묶기(int 기술) {
        if (Urusobemiyoboro_umukondo[기술] != 0) return 0;
        int 결과 = Urusobemiyoboro_Ikirundo.Gufungura(0);
        if (결과 < 0) return 결과;
        Urusobemiyoboro_umukondo[기술] = 결과;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 요청 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int amakurushingiro_aderesi, int uburebure_agaciro, int Amagenamiterere, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Amagenamiterere != 0) return -95;
        if (uburebure_agaciro < 0 || uburebure_agaciro > 1024) return -90;
        if (uburebure_agaciro != 0 && !실행관리.kiripu(amakurushingiro_aderesi, uburebure_agaciro)) return -14;
        if (!실행관리.kiripu(요청주소, 8)) return -14;
        int aderesi = 실행관리.수(요청주소);
        int 결과 = sheki_aderesi(aderesi, 실행관리.수(요청주소 + 4));
        if (결과 < 0) return 결과;
        int 접속번호 = igendanwa_agaciro.기억읽기(aderesi + 2) << 8 | igendanwa_agaciro.기억읽기(aderesi + 3);
        if (접속번호 == 0) return -22;
        결과 = 자동묶기(기술);
        if (결과 < 0) return 결과;
        for (int umugerekashakiro = 0; umugerekashakiro < uburebure_agaciro; umugerekashakiro++) iyimura_amakurushingiro[umugerekashakiro] = igendanwa_agaciro.기억읽기(amakurushingiro_aderesi + umugerekashakiro);
        return Urusobemiyoboro_Ikirundo.kohereza(Urusobemiyoboro_umukondo[기술], aderesi_32(aderesi + 4), 접속번호, iyimura_amakurushingiro, uburebure_agaciro);
    }
    static void kwandika_aderesi(int aderesi, int uburebure_agaciro, int Urusobemiyoboro_aderesi, int 접속번호) {
        for (int umugerekashakiro = 0; umugerekashakiro < uburebure_agaciro && umugerekashakiro < 16; umugerekashakiro++) {
            int agaciro = 0;
            if (umugerekashakiro == 0) agaciro = 2;
            if (umugerekashakiro == 2) agaciro = 접속번호 >>> 8;
            if (umugerekashakiro == 3) agaciro = 접속번호;
            if (umugerekashakiro >= 4 && umugerekashakiro < 8) agaciro = Urusobemiyoboro_aderesi >>> (56 - umugerekashakiro * 8);
            igendanwa_agaciro.kwandika_ububiko(aderesi + umugerekashakiro, agaciro & 255);
        }
    }
    static int 자료전문받기(int 서술자, int amakurushingiro_aderesi, int uburebure_agaciro, int Amagenamiterere, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Amagenamiterere & ~64) != 0) return -95;
        if (uburebure_agaciro < 0) return -22;
        if (uburebure_agaciro != 0 && !실행관리.kiripu(amakurushingiro_aderesi, uburebure_agaciro)) return -14;
        int aderesi = 0, aderesi_uburebure_aderesi = 0, aderesi_uburebure = 0;
        if (요청주소 != 0) {
            if (!실행관리.kiripu(요청주소, 8)) return -14;
            aderesi = 실행관리.수(요청주소); aderesi_uburebure_aderesi = 실행관리.수(요청주소 + 4);
            if (aderesi != 0) {
                if (!실행관리.kiripu(aderesi_uburebure_aderesi, 4)) return -14;
                aderesi_uburebure = 실행관리.수(aderesi_uburebure_aderesi);
                if (aderesi_uburebure < 0) return -22;
                if (!실행관리.kiripu(aderesi, aderesi_uburebure < 16 ? aderesi_uburebure : 16)) return -14;
            }
        }
        int 결과 = 자동묶기(기술);
        if (결과 < 0) return 결과;
        int ihuriro = igendanwa_agaciro.밀리초();
        while (true) {
            결과 = Urusobemiyoboro_Ikirundo.받기(Urusobemiyoboro_umukondo[기술], iyimura_amakurushingiro, 1024, 0);
            if (결과 != -11) break;
            if ((Amagenamiterere & 64) != 0 || (kurema_Amagenamiterere[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && igendanwa_agaciro.밀리초() - ihuriro >= 수신대기밀리초[기술]) return -11;
            if (igendanwa_agaciro.사용자남은밀리초() <= 10) return -11;
            igendanwa_agaciro.잠시양보();
        }
        if (결과 < 0) return 결과;
        if (결과 > uburebure_agaciro) 결과 = uburebure_agaciro;
        for (int umugerekashakiro = 0; umugerekashakiro < 결과; umugerekashakiro++) igendanwa_agaciro.kwandika_ububiko(amakurushingiro_aderesi + umugerekashakiro, iyimura_amakurushingiro[umugerekashakiro]);
        if (aderesi != 0) {
            kwandika_aderesi(aderesi, aderesi_uburebure, Urusobemiyoboro_Ikirundo.Mugenzi_aderesi(Urusobemiyoboro_umukondo[기술]), Urusobemiyoboro_Ikirundo.상대접속번호(Urusobemiyoboro_umukondo[기술]));
            실행관리.수쓰기(aderesi_uburebure_aderesi, 16);
        }
        return 결과;
    }
    static int 통신주소읽기(int 서술자, int aderesi, int uburebure_aderesi) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.kiripu(uburebure_aderesi, 4)) return -14;
        int uburebure_agaciro = 실행관리.수(uburebure_aderesi);
        if (uburebure_agaciro < 0) return -22;
        if (!실행관리.kiripu(aderesi, uburebure_agaciro < 16 ? uburebure_agaciro : 16)) return -14;
        int umwanya_icyinjizwa = Urusobemiyoboro_Ikirundo.umugerekashakiro(Urusobemiyoboro_umukondo[기술]);
        kwandika_aderesi(aderesi, uburebure_agaciro, gusimbuza_igishya[기술], umwanya_icyinjizwa < 0 ? 0 : Urusobemiyoboro_Ikirundo.접속번호들[umwanya_icyinjizwa]);
        실행관리.수쓰기(uburebure_aderesi, 16);
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
