// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Idosiye 64개, 파일당 16384바이트, 서술자 16개. 모든 amakurushingiro/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 IKOSA 번호다.
 */
public final class ububiko_Dosiye {
    static final int 파일수 = 64;
    static int[] Izina = new int[파일수 * 64];
    static int[] 이름길이 = new int[파일수];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Ibirimo_agaciro = new int[파일수 * 4096];
    static int[] uburebure_agaciro = new int[파일수];
    static int[] 참조수 = new int[파일수];
    static int[] 사용 = new int[16];
    static int[] gusimbuza_igishya = new int[16];
    static int[] 위치 = new int[16];
    static int[] uburyo_uburyo = new int[16];
    static int[] Inzira = new int[64];
    static int inzira_uburebure;

    public static int 파일한도() { return 파일수; }
    static int 자료읽기(int Idosiye, int 자리) { return (Ibirimo_agaciro[Idosiye * 4096 + 자리 / 4] >>> ((자리 & 3) * 8)) & 255; }
    static void kwandika_amakurushingiro(int Idosiye, int 자리, int agaciro) {
        int umwanya_icyinjizwa = Idosiye * 4096 + 자리 / 4, kwimura_agaciro = (자리 & 3) * 8;
        Ibirimo_agaciro[umwanya_icyinjizwa] = (Ibirimo_agaciro[umwanya_icyinjizwa] & ~(255 << kwimura_agaciro)) | ((agaciro & 255) << kwimura_agaciro);
    }

    public static int inzira_Itangira(int Ingano) {
        inzira_uburebure = 0;
        if (Ingano < 1 || Ingano > 63) return -36;
        inzira_uburebure = Ingano;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < Ingano; gukora_mu_matsinda_umugerekashakiro++) Inzira[gukora_mu_matsinda_umugerekashakiro] = 0;
        return 0;
    }
    public static int inzira_bayiti(int umugerekashakiro, int agaciro) {
        if (umugerekashakiro < 0 || umugerekashakiro >= inzira_uburebure || agaciro < 1 || agaciro > 255) return -22;
        Inzira[umugerekashakiro] = agaciro; return 0;
    }
    static int gushaka_icyinjizwa() {
        for (int dosiye_umugerekashakiro = 0; dosiye_umugerekashakiro < 파일수; dosiye_umugerekashakiro++) if (이름길이[dosiye_umugerekashakiro] > 0 && 이름길이[dosiye_umugerekashakiro] == 정규길이 && 접두(Izina, dosiye_umugerekashakiro * 64, 이름길이[dosiye_umugerekashakiro], 정규, 정규길이)) return dosiye_umugerekashakiro;
        return -1;
    }
    public static int Gufungura(int 플래그) {
        if (inzira_uburebure == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < inzira_uburebure; gukora_mu_matsinda_umugerekashakiro++) if (Inzira[gukora_mu_matsinda_umugerekashakiro] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int 결과 = kuboneza_agaciro(); if (결과 < 0) return 결과;
        if (gushaka_ububiko(정규길이) >= 0) return -21;
        결과 = 부모확인(); if (결과 < 0) return 결과;
        int Idosiye = gushaka_icyinjizwa();
        if (Idosiye >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Idosiye < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 16; gukora_mu_matsinda_umugerekashakiro++) if (사용[gukora_mu_matsinda_umugerekashakiro] == 0) { 서술자 = gukora_mu_matsinda_umugerekashakiro; break; }
        if (서술자 < 0) return -24;
        if (Idosiye < 0) {
            for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 파일수; gukora_mu_matsinda_umugerekashakiro++) if (이름길이[gukora_mu_matsinda_umugerekashakiro] == 0 && 참조수[gukora_mu_matsinda_umugerekashakiro] == 0) { Idosiye = gukora_mu_matsinda_umugerekashakiro; break; }
            if (Idosiye < 0) return -28;
            이름길이[Idosiye] = 정규길이;
            for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 정규길이; gukora_mu_matsinda_umugerekashakiro++) Izina[Idosiye * 64 + gukora_mu_matsinda_umugerekashakiro] = 정규[gukora_mu_matsinda_umugerekashakiro];
            uburebure_agaciro[Idosiye] = 0;
        }
        if ((플래그 & 0x200) != 0) uburebure_agaciro[Idosiye] = 0;
        사용[서술자] = 1; gusimbuza_igishya[서술자] = Idosiye; 위치[서술자] = 0; uburyo_uburyo[서술자] = 플래그;
        참조수[Idosiye]++;
        return 서술자 + 3;
    }
    static int gusuzuma(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int 읽기(int 서술자) {
        int umwanya_icyinjizwa = gusuzuma(서술자);
        if (umwanya_icyinjizwa < 0 || (uburyo_uburyo[umwanya_icyinjizwa] & 3) == 1) return -9;
        int Idosiye = gusimbuza_igishya[umwanya_icyinjizwa];
        if (위치[umwanya_icyinjizwa] >= uburebure_agaciro[Idosiye]) return 256; // EOF와 nyakuri_amakurushingiro 0x00..0xff 구별
        return 자료읽기(Idosiye, 위치[umwanya_icyinjizwa]++);
    }
    public static int kwandika(int 서술자, int agaciro) {
        int umwanya_icyinjizwa = gusuzuma(서술자);
        if (umwanya_icyinjizwa < 0 || (uburyo_uburyo[umwanya_icyinjizwa] & 3) == 0) return -9;
        int Idosiye = gusimbuza_igishya[umwanya_icyinjizwa];
        if ((uburyo_uburyo[umwanya_icyinjizwa] & 0x400) != 0) 위치[umwanya_icyinjizwa] = uburebure_agaciro[Idosiye];
        if (위치[umwanya_icyinjizwa] >= 16384) return -28;
        while (uburebure_agaciro[Idosiye] < 위치[umwanya_icyinjizwa]) kwandika_amakurushingiro(Idosiye, uburebure_agaciro[Idosiye]++, 0);
        kwandika_amakurushingiro(Idosiye, 위치[umwanya_icyinjizwa]++, agaciro);
        if (uburebure_agaciro[Idosiye] < 위치[umwanya_icyinjizwa]) uburebure_agaciro[Idosiye] = 위치[umwanya_icyinjizwa];
        return 1;
    }
    public static int 옮기기(int 서술자, int 거리, int 기준) {
        int umwanya_icyinjizwa = gusuzuma(서술자);
        if (umwanya_icyinjizwa < 0) return -9;
        if (기준 < 0 || 기준 > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (기준 == 0 ? 0 : 기준 == 1 ? 위치[umwanya_icyinjizwa] : uburebure_agaciro[gusimbuza_igishya[umwanya_icyinjizwa]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        위치[umwanya_icyinjizwa] = 새위치; return 새위치;
    }
    public static int Gufunga(int 서술자) {
        int umwanya_icyinjizwa = gusuzuma(서술자);
        if (umwanya_icyinjizwa < 0) return -9;
        참조수[gusimbuza_igishya[umwanya_icyinjizwa]]--; 사용[umwanya_icyinjizwa] = 0; return 0;
    }
    public static int Ingano(int 서술자) {
        int umwanya_icyinjizwa = gusuzuma(서술자); return umwanya_icyinjizwa < 0 ? -9 : uburebure_agaciro[gusimbuza_igishya[umwanya_icyinjizwa]];
    }
    public static int itsinda_uburebure(int 서술자, int Ingano) {
        int umwanya_icyinjizwa = gusuzuma(서술자);
        if (umwanya_icyinjizwa < 0 || (uburyo_uburyo[umwanya_icyinjizwa] & 3) == 0) return -9;
        if (Ingano < 0 || Ingano > 16384) return -22;
        int Idosiye = gusimbuza_igishya[umwanya_icyinjizwa];
        while (uburebure_agaciro[Idosiye] < Ingano) kwandika_amakurushingiro(Idosiye, uburebure_agaciro[Idosiye]++, 0);
        uburebure_agaciro[Idosiye] = Ingano; return 0;
    }
    public static int 지우기() {
        if (inzira_uburebure == 0) return -22;
        int 결과 = kuboneza_agaciro(); if (결과 < 0) return 결과;
        if (gushaka_ububiko(정규길이) >= 0) return -21;
        결과 = 부모확인(); if (결과 < 0) return 결과;
        int Idosiye = gushaka_icyinjizwa();
        if (Idosiye < 0) return -2;
        이름길이[Idosiye] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void icyinjizwa_Urutonde() {
        inzira_Itangira(1); inzira_bayiti(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int umugerekashakiro) {
        if (umugerekashakiro < 0 || umugerekashakiro >= 파일수 || 이름길이[umugerekashakiro] == 0) return 0;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 이름길이[umugerekashakiro]; gukora_mu_matsinda_umugerekashakiro++) if (Izina[umugerekashakiro * 64 + gukora_mu_matsinda_umugerekashakiro] == '/') return 0;
        return 이름길이[umugerekashakiro];
    }
    public static int 공개이름바이트(int umugerekashakiro, int 자리) {
        return umugerekashakiro >= 0 && umugerekashakiro < 파일수 && 자리 >= 0 && 자리 < 이름길이[umugerekashakiro] ? Izina[umugerekashakiro * 64 + 자리] : -22;
    }
    public static int 공개파일크기(int umugerekashakiro) { return umugerekashakiro >= 0 && umugerekashakiro < 파일수 ? uburebure_agaciro[umugerekashakiro] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], ububiko_izina = new int[16 * 64], ububiko_uburebure = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int ihuriro, int inzira_agaciro, int[] 앞, int itandukanyamurongo_inzira) {
        if (inzira_agaciro < itandukanyamurongo_inzira) return false;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < itandukanyamurongo_inzira; gukora_mu_matsinda_umugerekashakiro++) if (이름들[ihuriro + gukora_mu_matsinda_umugerekashakiro] != 앞[gukora_mu_matsinda_umugerekashakiro]) return false;
        return true;
    }
    static int kuboneza_agaciro() {
        if (inzira_uburebure == 0) return -22;
        정규길이 = Inzira[0] == '/' ? 0 : 현재길이;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 정규길이; gukora_mu_matsinda_umugerekashakiro++) 정규[gukora_mu_matsinda_umugerekashakiro] = 현재[gukora_mu_matsinda_umugerekashakiro];
        int 읽는자리 = 0;
        while (읽는자리 < inzira_uburebure) {
            while (읽는자리 < inzira_uburebure && Inzira[읽는자리] == '/') 읽는자리++;
            int 시작자리 = 읽는자리; while (읽는자리 < inzira_uburebure && Inzira[읽는자리] != '/') { if (Inzira[읽는자리] == 0) return -22; 읽는자리++; }
            int 항목수 = 읽는자리 - 시작자리; if (항목수 == 0 || 항목수 == 1 && Inzira[시작자리] == '.') continue;
            if (항목수 == 2 && Inzira[시작자리] == '.' && Inzira[시작자리 + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + 항목수 + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int gukora_mu_matsinda_umugerekashakiro = 시작자리; gukora_mu_matsinda_umugerekashakiro < 읽는자리; gukora_mu_matsinda_umugerekashakiro++) 정규[정규길이++] = Inzira[gukora_mu_matsinda_umugerekashakiro];
        }
        return 0;
    }
    static int gushaka_ububiko(int 항목수) {
        if (항목수 == 0) return 0;
        for (int gukora_mu_matsinda_umugerekashakiro = 1; gukora_mu_matsinda_umugerekashakiro < 16; gukora_mu_matsinda_umugerekashakiro++) if (ububiko_uburebure[gukora_mu_matsinda_umugerekashakiro] == 항목수 && 접두(ububiko_izina, gukora_mu_matsinda_umugerekashakiro * 64, 항목수, 정규, 항목수)) return gukora_mu_matsinda_umugerekashakiro;
        return -1;
    }
    static int 부모확인() {
        int 항목수 = 정규길이; while (항목수 > 0 && 정규[항목수 - 1] != '/') 항목수--;
        return gushaka_ububiko(항목수 == 0 ? 0 : 항목수 - 1) < 0 ? -2 : 0;
    }
    public static int kurema_ububiko() {
        int 처리값 = kuboneza_agaciro(); if (처리값 < 0) return 처리값;
        if (gushaka_ububiko(정규길이) >= 0 || gushaka_icyinjizwa() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int gukora_mu_matsinda_umugerekashakiro = 1; gukora_mu_matsinda_umugerekashakiro < 16; gukora_mu_matsinda_umugerekashakiro++) if (ububiko_uburebure[gukora_mu_matsinda_umugerekashakiro] == 0) {
            ububiko_uburebure[gukora_mu_matsinda_umugerekashakiro] = 정규길이; for (int 안쪽자리 = 0; 안쪽자리 < 정규길이; 안쪽자리++) ububiko_izina[gukora_mu_matsinda_umugerekashakiro * 64 + 안쪽자리] = 정규[안쪽자리]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = kuboneza_agaciro(); if (처리값 < 0) return 처리값;
        if (gushaka_ububiko(정규길이) >= 0) return 2;
        return gushaka_icyinjizwa() >= 0 ? 1 : 0;
    }
    public static int guhindura_ububiko() {
        int 처리값 = kuboneza_agaciro(); if (처리값 < 0) return 처리값;
        if (gushaka_ububiko(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 현재길이; gukora_mu_matsinda_umugerekashakiro++) 현재[gukora_mu_matsinda_umugerekashakiro] = 정규[gukora_mu_matsinda_umugerekashakiro]; return 0;
    }
    public static int gukuramo_ububiko() {
        int 처리값 = kuboneza_agaciro(); if (처리값 < 0) return 처리값;
        int 폴더번호 = gushaka_ububiko(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 파일수; gukora_mu_matsinda_umugerekashakiro++) {
            if (이름길이[gukora_mu_matsinda_umugerekashakiro] > 정규길이 && 접두(Izina, gukora_mu_matsinda_umugerekashakiro * 64, 이름길이[gukora_mu_matsinda_umugerekashakiro], 정규, 정규길이) && Izina[gukora_mu_matsinda_umugerekashakiro * 64 + 정규길이] == '/') return -39;
        }
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 16; gukora_mu_matsinda_umugerekashakiro++) {
            if (ububiko_uburebure[gukora_mu_matsinda_umugerekashakiro] > 정규길이 && 접두(ububiko_izina, gukora_mu_matsinda_umugerekashakiro * 64, ububiko_uburebure[gukora_mu_matsinda_umugerekashakiro], 정규, 정규길이) && ububiko_izina[gukora_mu_matsinda_umugerekashakiro * 64 + 정규길이] == '/') return -39;
        }
        ububiko_uburebure[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= 파일수 || 이름길이[원본번호] == 0) return -2;
        int 처리값 = kuboneza_agaciro(); if (처리값 < 0) return 처리값;
        if (gushaka_ububiko(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = gushaka_icyinjizwa(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 정규길이; gukora_mu_matsinda_umugerekashakiro++) Izina[원본번호 * 64 + gukora_mu_matsinda_umugerekashakiro] = 정규[gukora_mu_matsinda_umugerekashakiro]; return 0;
    }
    static int icyinjizwa_Itangira(int[] amakurushingiro_ARRAY, int 시작점, int 항목수) {
        if (!접두(amakurushingiro_ARRAY, 시작점, 항목수, 정규, 정규길이)) return -1;
        int 시작자리 = 정규길이;
        if (시작자리 > 0) { if (항목수 <= 시작자리 || amakurushingiro_ARRAY[시작점 + 시작자리] != '/') return -1; 시작자리++; }
        if (항목수 <= 시작자리) return -1;
        for (int gukora_mu_matsinda_umugerekashakiro = 시작자리; gukora_mu_matsinda_umugerekashakiro < 항목수; gukora_mu_matsinda_umugerekashakiro++) if (amakurushingiro_ARRAY[시작점 + gukora_mu_matsinda_umugerekashakiro] == '/') return -1;
        return 시작자리;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 현재길이; gukora_mu_matsinda_umugerekashakiro++) 보드.직렬쓰기(현재[gukora_mu_matsinda_umugerekashakiro]); }
    static int 경로목록() {
        int 처리값 = kuboneza_agaciro(); if (처리값 < 0) return 처리값;
        int dosiye_gusimbuza_igishya = gushaka_icyinjizwa();
        if (dosiye_gusimbuza_igishya >= 0) { for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 정규길이; gukora_mu_matsinda_umugerekashakiro++) 보드.직렬쓰기(정규[gukora_mu_matsinda_umugerekashakiro]); 단말.kwandika("  "); 단말.수(uburebure_agaciro[dosiye_gusimbuza_igishya]); 단말.kwandika("bayiti_agaciro(주기억 Idosiye)\n"); return 0; }
        if (gushaka_ububiko(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (ububiko_uburebure[뒷값] > 0) {
            int 시작자리 = icyinjizwa_Itangira(ububiko_izina, 뒷값 * 64, ububiko_uburebure[뒷값]); if (시작자리 < 0) continue;
            for (int gukora_mu_matsinda_umugerekashakiro = 시작자리; gukora_mu_matsinda_umugerekashakiro < ububiko_uburebure[뒷값]; gukora_mu_matsinda_umugerekashakiro++) 보드.직렬쓰기(ububiko_izina[뒷값 * 64 + gukora_mu_matsinda_umugerekashakiro]); 단말.kwandika("/\n");
        }
        for (int dosiye_umugerekashakiro = 0; dosiye_umugerekashakiro < 파일수; dosiye_umugerekashakiro++) if (이름길이[dosiye_umugerekashakiro] > 0) {
            int 시작자리 = icyinjizwa_Itangira(Izina, dosiye_umugerekashakiro * 64, 이름길이[dosiye_umugerekashakiro]); if (시작자리 < 0) continue;
            for (int gukora_mu_matsinda_umugerekashakiro = 시작자리; gukora_mu_matsinda_umugerekashakiro < 이름길이[dosiye_umugerekashakiro]; gukora_mu_matsinda_umugerekashakiro++) 보드.직렬쓰기(Izina[dosiye_umugerekashakiro * 64 + gukora_mu_matsinda_umugerekashakiro]);
            단말.kwandika("  "); 단말.수(uburebure_agaciro[dosiye_umugerekashakiro]); 단말.kwandika("bayiti_agaciro(주기억 Idosiye)\n");
        }
        return 0;
    }
}
