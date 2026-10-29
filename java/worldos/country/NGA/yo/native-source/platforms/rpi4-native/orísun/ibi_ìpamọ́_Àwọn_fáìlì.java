// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Fáìlì 64개, 파일당 16384바이트, 서술자 16개. 모든 détà/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 àṣìṣe 번호다.
 */
public final class ibi_ìpamọ́_Àwọn_fáìlì {
    static final int 파일수 = 64;
    static int[] Orúkọ = new int[파일수 * 64];
    static int[] 이름길이 = new int[파일수];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Àkóónú_iye = new int[파일수 * 4096];
    static int[] gígùn_iye = new int[파일수];
    static int[] 참조수 = new int[파일수];
    static int[] 사용 = new int[16];
    static int[] àfojúsùn = new int[16];
    static int[] 위치 = new int[16];
    static int[] ìlànà_móòdù = new int[16];
    static int[] ọ̀nà = new int[64];
    static int ọ̀nà_gígùn;

    public static int 파일한도() { return 파일수; }
    static int 자료읽기(int Fáìlì, int 자리) { return (Àkóónú_iye[Fáìlì * 4096 + 자리 / 4] >>> ((자리 & 3) * 8)) & 255; }
    static void kọ_détà(int Fáìlì, int 자리, int iye) {
        int ààyè_ìfàyọkàsí_ìgbéwọlé = Fáìlì * 4096 + 자리 / 4, gbé_iye = (자리 & 3) * 8;
        Àkóónú_iye[ààyè_ìfàyọkàsí_ìgbéwọlé] = (Àkóónú_iye[ààyè_ìfàyọkàsí_ìgbéwọlé] & ~(255 << gbé_iye)) | ((iye & 255) << gbé_iye);
    }

    public static int ọ̀nà_bẹ̀rẹ̀(int Ìwọ̀n) {
        ọ̀nà_gígùn = 0;
        if (Ìwọ̀n < 1 || Ìwọ̀n > 63) return -36;
        ọ̀nà_gígùn = Ìwọ̀n;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < Ìwọ̀n; ṣetúnṣe_wá_atọ̀ka_àkóónú++) ọ̀nà[ṣetúnṣe_wá_atọ̀ka_àkóónú] = 0;
        return 0;
    }
    public static int ọ̀nà_báìtì(int wá_atọ̀ka_àkóónú, int iye) {
        if (wá_atọ̀ka_àkóónú < 0 || wá_atọ̀ka_àkóónú >= ọ̀nà_gígùn || iye < 1 || iye > 255) return -22;
        ọ̀nà[wá_atọ̀ka_àkóónú] = iye; return 0;
    }
    static int wá_ìgbéwọlé() {
        for (int fáìlì_wá_atọ̀ka_àkóónú = 0; fáìlì_wá_atọ̀ka_àkóónú < 파일수; fáìlì_wá_atọ̀ka_àkóónú++) if (이름길이[fáìlì_wá_atọ̀ka_àkóónú] > 0 && 이름길이[fáìlì_wá_atọ̀ka_àkóónú] == 정규길이 && 접두(Orúkọ, fáìlì_wá_atọ̀ka_àkóónú * 64, 이름길이[fáìlì_wá_atọ̀ka_àkóónú], 정규, 정규길이)) return fáìlì_wá_atọ̀ka_àkóónú;
        return -1;
    }
    public static int Ṣi(int 플래그) {
        if (ọ̀nà_gígùn == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < ọ̀nà_gígùn; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (ọ̀nà[ṣetúnṣe_wá_atọ̀ka_àkóónú] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int 결과 = ṣe_níwọ̀n_iye(); if (결과 < 0) return 결과;
        if (wá_àkójọpọ̀_fáìlì(정규길이) >= 0) return -21;
        결과 = 부모확인(); if (결과 < 0) return 결과;
        int Fáìlì = wá_ìgbéwọlé();
        if (Fáìlì >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Fáìlì < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 16; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (사용[ṣetúnṣe_wá_atọ̀ka_àkóónú] == 0) { 서술자 = ṣetúnṣe_wá_atọ̀ka_àkóónú; break; }
        if (서술자 < 0) return -24;
        if (Fáìlì < 0) {
            for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 파일수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (이름길이[ṣetúnṣe_wá_atọ̀ka_àkóónú] == 0 && 참조수[ṣetúnṣe_wá_atọ̀ka_àkóónú] == 0) { Fáìlì = ṣetúnṣe_wá_atọ̀ka_àkóónú; break; }
            if (Fáìlì < 0) return -28;
            이름길이[Fáìlì] = 정규길이;
            for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 정규길이; ṣetúnṣe_wá_atọ̀ka_àkóónú++) Orúkọ[Fáìlì * 64 + ṣetúnṣe_wá_atọ̀ka_àkóónú] = 정규[ṣetúnṣe_wá_atọ̀ka_àkóónú];
            gígùn_iye[Fáìlì] = 0;
        }
        if ((플래그 & 0x200) != 0) gígùn_iye[Fáìlì] = 0;
        사용[서술자] = 1; àfojúsùn[서술자] = Fáìlì; 위치[서술자] = 0; ìlànà_móòdù[서술자] = 플래그;
        참조수[Fáìlì]++;
        return 서술자 + 3;
    }
    static int ridájú(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Kàá(int 서술자) {
        int ààyè_ìfàyọkàsí_ìgbéwọlé = ridájú(서술자);
        if (ààyè_ìfàyọkàsí_ìgbéwọlé < 0 || (ìlànà_móòdù[ààyè_ìfàyọkàsí_ìgbéwọlé] & 3) == 1) return -9;
        int Fáìlì = àfojúsùn[ààyè_ìfàyọkàsí_ìgbéwọlé];
        if (위치[ààyè_ìfàyọkàsí_ìgbéwọlé] >= gígùn_iye[Fáìlì]) return 256; // EOF와 gangan_détà 0x00..0xff 구별
        return 자료읽기(Fáìlì, 위치[ààyè_ìfàyọkàsí_ìgbéwọlé]++);
    }
    public static int Kọ(int 서술자, int iye) {
        int ààyè_ìfàyọkàsí_ìgbéwọlé = ridájú(서술자);
        if (ààyè_ìfàyọkàsí_ìgbéwọlé < 0 || (ìlànà_móòdù[ààyè_ìfàyọkàsí_ìgbéwọlé] & 3) == 0) return -9;
        int Fáìlì = àfojúsùn[ààyè_ìfàyọkàsí_ìgbéwọlé];
        if ((ìlànà_móòdù[ààyè_ìfàyọkàsí_ìgbéwọlé] & 0x400) != 0) 위치[ààyè_ìfàyọkàsí_ìgbéwọlé] = gígùn_iye[Fáìlì];
        if (위치[ààyè_ìfàyọkàsí_ìgbéwọlé] >= 16384) return -28;
        while (gígùn_iye[Fáìlì] < 위치[ààyè_ìfàyọkàsí_ìgbéwọlé]) kọ_détà(Fáìlì, gígùn_iye[Fáìlì]++, 0);
        kọ_détà(Fáìlì, 위치[ààyè_ìfàyọkàsí_ìgbéwọlé]++, iye);
        if (gígùn_iye[Fáìlì] < 위치[ààyè_ìfàyọkàsí_ìgbéwọlé]) gígùn_iye[Fáìlì] = 위치[ààyè_ìfàyọkàsí_ìgbéwọlé];
        return 1;
    }
    public static int 옮기기(int 서술자, int 거리, int 기준) {
        int ààyè_ìfàyọkàsí_ìgbéwọlé = ridájú(서술자);
        if (ààyè_ìfàyọkàsí_ìgbéwọlé < 0) return -9;
        if (기준 < 0 || 기준 > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (기준 == 0 ? 0 : 기준 == 1 ? 위치[ààyè_ìfàyọkàsí_ìgbéwọlé] : gígùn_iye[àfojúsùn[ààyè_ìfàyọkàsí_ìgbéwọlé]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        위치[ààyè_ìfàyọkàsí_ìgbéwọlé] = 새위치; return 새위치;
    }
    public static int Ti(int 서술자) {
        int ààyè_ìfàyọkàsí_ìgbéwọlé = ridájú(서술자);
        if (ààyè_ìfàyọkàsí_ìgbéwọlé < 0) return -9;
        참조수[àfojúsùn[ààyè_ìfàyọkàsí_ìgbéwọlé]]--; 사용[ààyè_ìfàyọkàsí_ìgbéwọlé] = 0; return 0;
    }
    public static int Ìwọ̀n(int 서술자) {
        int ààyè_ìfàyọkàsí_ìgbéwọlé = ridájú(서술자); return ààyè_ìfàyọkàsí_ìgbéwọlé < 0 ? -9 : gígùn_iye[àfojúsùn[ààyè_ìfàyọkàsí_ìgbéwọlé]];
    }
    public static int ọ̀wọ̀_gígùn(int 서술자, int Ìwọ̀n) {
        int ààyè_ìfàyọkàsí_ìgbéwọlé = ridájú(서술자);
        if (ààyè_ìfàyọkàsí_ìgbéwọlé < 0 || (ìlànà_móòdù[ààyè_ìfàyọkàsí_ìgbéwọlé] & 3) == 0) return -9;
        if (Ìwọ̀n < 0 || Ìwọ̀n > 16384) return -22;
        int Fáìlì = àfojúsùn[ààyè_ìfàyọkàsí_ìgbéwọlé];
        while (gígùn_iye[Fáìlì] < Ìwọ̀n) kọ_détà(Fáìlì, gígùn_iye[Fáìlì]++, 0);
        gígùn_iye[Fáìlì] = Ìwọ̀n; return 0;
    }
    public static int 지우기() {
        if (ọ̀nà_gígùn == 0) return -22;
        int 결과 = ṣe_níwọ̀n_iye(); if (결과 < 0) return 결과;
        if (wá_àkójọpọ̀_fáìlì(정규길이) >= 0) return -21;
        결과 = 부모확인(); if (결과 < 0) return 결과;
        int Fáìlì = wá_ìgbéwọlé();
        if (Fáìlì < 0) return -2;
        이름길이[Fáìlì] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void ìgbéwọlé_Àtòkọ() {
        ọ̀nà_bẹ̀rẹ̀(1); ọ̀nà_báìtì(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int wá_atọ̀ka_àkóónú) {
        if (wá_atọ̀ka_àkóónú < 0 || wá_atọ̀ka_àkóónú >= 파일수 || 이름길이[wá_atọ̀ka_àkóónú] == 0) return 0;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 이름길이[wá_atọ̀ka_àkóónú]; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (Orúkọ[wá_atọ̀ka_àkóónú * 64 + ṣetúnṣe_wá_atọ̀ka_àkóónú] == '/') return 0;
        return 이름길이[wá_atọ̀ka_àkóónú];
    }
    public static int 공개이름바이트(int wá_atọ̀ka_àkóónú, int 자리) {
        return wá_atọ̀ka_àkóónú >= 0 && wá_atọ̀ka_àkóónú < 파일수 && 자리 >= 0 && 자리 < 이름길이[wá_atọ̀ka_àkóónú] ? Orúkọ[wá_atọ̀ka_àkóónú * 64 + 자리] : -22;
    }
    public static int 공개파일크기(int wá_atọ̀ka_àkóónú) { return wá_atọ̀ka_àkóónú >= 0 && wá_atọ̀ka_àkóónú < 파일수 ? gígùn_iye[wá_atọ̀ka_àkóónú] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], àkójọpọ̀_fáìlì_orúkọ = new int[16 * 64], àkójọpọ̀_fáìlì_gígùn = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int Rọ́ọ̀nù, int ọ̀nà_iye, int[] 앞, int ìṣáájú_ọ̀nà) {
        if (ọ̀nà_iye < ìṣáájú_ọ̀nà) return false;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < ìṣáájú_ọ̀nà; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (이름들[Rọ́ọ̀nù + ṣetúnṣe_wá_atọ̀ka_àkóónú] != 앞[ṣetúnṣe_wá_atọ̀ka_àkóónú]) return false;
        return true;
    }
    static int ṣe_níwọ̀n_iye() {
        if (ọ̀nà_gígùn == 0) return -22;
        정규길이 = ọ̀nà[0] == '/' ? 0 : 현재길이;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 정규길이; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 정규[ṣetúnṣe_wá_atọ̀ka_àkóónú] = 현재[ṣetúnṣe_wá_atọ̀ka_àkóónú];
        int 읽는자리 = 0;
        while (읽는자리 < ọ̀nà_gígùn) {
            while (읽는자리 < ọ̀nà_gígùn && ọ̀nà[읽는자리] == '/') 읽는자리++;
            int 시작자리 = 읽는자리; while (읽는자리 < ọ̀nà_gígùn && ọ̀nà[읽는자리] != '/') { if (ọ̀nà[읽는자리] == 0) return -22; 읽는자리++; }
            int 항목수 = 읽는자리 - 시작자리; if (항목수 == 0 || 항목수 == 1 && ọ̀nà[시작자리] == '.') continue;
            if (항목수 == 2 && ọ̀nà[시작자리] == '.' && ọ̀nà[시작자리 + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + 항목수 + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 시작자리; ṣetúnṣe_wá_atọ̀ka_àkóónú < 읽는자리; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 정규[정규길이++] = ọ̀nà[ṣetúnṣe_wá_atọ̀ka_àkóónú];
        }
        return 0;
    }
    static int wá_àkójọpọ̀_fáìlì(int 항목수) {
        if (항목수 == 0) return 0;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 1; ṣetúnṣe_wá_atọ̀ka_àkóónú < 16; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (àkójọpọ̀_fáìlì_gígùn[ṣetúnṣe_wá_atọ̀ka_àkóónú] == 항목수 && 접두(àkójọpọ̀_fáìlì_orúkọ, ṣetúnṣe_wá_atọ̀ka_àkóónú * 64, 항목수, 정규, 항목수)) return ṣetúnṣe_wá_atọ̀ka_àkóónú;
        return -1;
    }
    static int 부모확인() {
        int 항목수 = 정규길이; while (항목수 > 0 && 정규[항목수 - 1] != '/') 항목수--;
        return wá_àkójọpọ̀_fáìlì(항목수 == 0 ? 0 : 항목수 - 1) < 0 ? -2 : 0;
    }
    public static int Ṣẹ̀dá_àkójọpọ̀_fáìlì() {
        int 처리값 = ṣe_níwọ̀n_iye(); if (처리값 < 0) return 처리값;
        if (wá_àkójọpọ̀_fáìlì(정규길이) >= 0 || wá_ìgbéwọlé() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 1; ṣetúnṣe_wá_atọ̀ka_àkóónú < 16; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (àkójọpọ̀_fáìlì_gígùn[ṣetúnṣe_wá_atọ̀ka_àkóónú] == 0) {
            àkójọpọ̀_fáìlì_gígùn[ṣetúnṣe_wá_atọ̀ka_àkóónú] = 정규길이; for (int 안쪽자리 = 0; 안쪽자리 < 정규길이; 안쪽자리++) àkójọpọ̀_fáìlì_orúkọ[ṣetúnṣe_wá_atọ̀ka_àkóónú * 64 + 안쪽자리] = 정규[안쪽자리]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = ṣe_níwọ̀n_iye(); if (처리값 < 0) return 처리값;
        if (wá_àkójọpọ̀_fáìlì(정규길이) >= 0) return 2;
        return wá_ìgbéwọlé() >= 0 ? 1 : 0;
    }
    public static int ṣàyípadà_àkójọpọ̀_fáìlì() {
        int 처리값 = ṣe_níwọ̀n_iye(); if (처리값 < 0) return 처리값;
        if (wá_àkójọpọ̀_fáìlì(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 현재길이; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 현재[ṣetúnṣe_wá_atọ̀ka_àkóónú] = 정규[ṣetúnṣe_wá_atọ̀ka_àkóónú]; return 0;
    }
    public static int ṣèmúkúro_àkójọpọ̀_fáìlì() {
        int 처리값 = ṣe_níwọ̀n_iye(); if (처리값 < 0) return 처리값;
        int 폴더번호 = wá_àkójọpọ̀_fáìlì(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 파일수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) {
            if (이름길이[ṣetúnṣe_wá_atọ̀ka_àkóónú] > 정규길이 && 접두(Orúkọ, ṣetúnṣe_wá_atọ̀ka_àkóónú * 64, 이름길이[ṣetúnṣe_wá_atọ̀ka_àkóónú], 정규, 정규길이) && Orúkọ[ṣetúnṣe_wá_atọ̀ka_àkóónú * 64 + 정규길이] == '/') return -39;
        }
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 16; ṣetúnṣe_wá_atọ̀ka_àkóónú++) {
            if (àkójọpọ̀_fáìlì_gígùn[ṣetúnṣe_wá_atọ̀ka_àkóónú] > 정규길이 && 접두(àkójọpọ̀_fáìlì_orúkọ, ṣetúnṣe_wá_atọ̀ka_àkóónú * 64, àkójọpọ̀_fáìlì_gígùn[ṣetúnṣe_wá_atọ̀ka_àkóónú], 정규, 정규길이) && àkójọpọ̀_fáìlì_orúkọ[ṣetúnṣe_wá_atọ̀ka_àkóónú * 64 + 정규길이] == '/') return -39;
        }
        àkójọpọ̀_fáìlì_gígùn[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= 파일수 || 이름길이[원본번호] == 0) return -2;
        int 처리값 = ṣe_níwọ̀n_iye(); if (처리값 < 0) return 처리값;
        if (wá_àkójọpọ̀_fáìlì(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = wá_ìgbéwọlé(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 정규길이; ṣetúnṣe_wá_atọ̀ka_àkóónú++) Orúkọ[원본번호 * 64 + ṣetúnṣe_wá_atọ̀ka_àkóónú] = 정규[ṣetúnṣe_wá_atọ̀ka_àkóónú]; return 0;
    }
    static int ìgbéwọlé_bẹ̀rẹ̀(int[] détà_ÀRÉÈ, int 시작점, int 항목수) {
        if (!접두(détà_ÀRÉÈ, 시작점, 항목수, 정규, 정규길이)) return -1;
        int 시작자리 = 정규길이;
        if (시작자리 > 0) { if (항목수 <= 시작자리 || détà_ÀRÉÈ[시작점 + 시작자리] != '/') return -1; 시작자리++; }
        if (항목수 <= 시작자리) return -1;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 시작자리; ṣetúnṣe_wá_atọ̀ka_àkóónú < 항목수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (détà_ÀRÉÈ[시작점 + ṣetúnṣe_wá_atọ̀ka_àkóónú] == '/') return -1;
        return 시작자리;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 현재길이; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 보드.직렬쓰기(현재[ṣetúnṣe_wá_atọ̀ka_àkóónú]); }
    static int 경로목록() {
        int 처리값 = ṣe_níwọ̀n_iye(); if (처리값 < 0) return 처리값;
        int fáìlì_àfojúsùn = wá_ìgbéwọlé();
        if (fáìlì_àfojúsùn >= 0) { for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 정규길이; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 보드.직렬쓰기(정규[ṣetúnṣe_wá_atọ̀ka_àkóónú]); 단말.Kọ("  "); 단말.수(gígùn_iye[fáìlì_àfojúsùn]); 단말.Kọ("báìtì_iye(주기억 Fáìlì)\n"); return 0; }
        if (wá_àkójọpọ̀_fáìlì(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (àkójọpọ̀_fáìlì_gígùn[뒷값] > 0) {
            int 시작자리 = ìgbéwọlé_bẹ̀rẹ̀(àkójọpọ̀_fáìlì_orúkọ, 뒷값 * 64, àkójọpọ̀_fáìlì_gígùn[뒷값]); if (시작자리 < 0) continue;
            for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 시작자리; ṣetúnṣe_wá_atọ̀ka_àkóónú < àkójọpọ̀_fáìlì_gígùn[뒷값]; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 보드.직렬쓰기(àkójọpọ̀_fáìlì_orúkọ[뒷값 * 64 + ṣetúnṣe_wá_atọ̀ka_àkóónú]); 단말.Kọ("/\n");
        }
        for (int fáìlì_wá_atọ̀ka_àkóónú = 0; fáìlì_wá_atọ̀ka_àkóónú < 파일수; fáìlì_wá_atọ̀ka_àkóónú++) if (이름길이[fáìlì_wá_atọ̀ka_àkóónú] > 0) {
            int 시작자리 = ìgbéwọlé_bẹ̀rẹ̀(Orúkọ, fáìlì_wá_atọ̀ka_àkóónú * 64, 이름길이[fáìlì_wá_atọ̀ka_àkóónú]); if (시작자리 < 0) continue;
            for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 시작자리; ṣetúnṣe_wá_atọ̀ka_àkóónú < 이름길이[fáìlì_wá_atọ̀ka_àkóónú]; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 보드.직렬쓰기(Orúkọ[fáìlì_wá_atọ̀ka_àkóónú * 64 + ṣetúnṣe_wá_atọ̀ka_àkóónú]);
            단말.Kọ("  "); 단말.수(gígùn_iye[fáìlì_wá_atọ̀ka_àkóónú]); 단말.Kọ("báìtì_iye(주기억 Fáìlì)\n");
        }
        return 0;
    }
}
