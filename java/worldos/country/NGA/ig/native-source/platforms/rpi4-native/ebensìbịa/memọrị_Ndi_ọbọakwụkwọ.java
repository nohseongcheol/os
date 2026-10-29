// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Faịlụ 64개, 파일당 16384바이트, 서술자 16개. 모든 datà/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 mmejọ 번호다.
 */
public final class memọrị_Ndi_ọbọakwụkwọ {
    static final int 파일수 = 64;
    static int[] Aha = new int[파일수 * 64];
    static int[] 이름길이 = new int[파일수];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] ndịnà_valuu = new int[파일수 * 4096];
    static int[] ogologo_valuu = new int[파일수];
    static int[] 참조수 = new int[파일수];
    static int[] 사용 = new int[16];
    static int[] ebenlereanya = new int[16];
    static int[] 위치 = new int[16];
    static int[] usoro_moòdù = new int[16];
    static int[] ụzọ_ozi = new int[64];
    static int ụzọ_ozi_ogologo;

    public static int 파일한도() { return 파일수; }
    static int 자료읽기(int Faịlụ, int 자리) { return (ndịnà_valuu[Faịlụ * 4096 + 자리 / 4] >>> ((자리 & 3) * 8)) & 255; }
    static void dee_datà(int Faịlụ, int 자리, int valuu) {
        int oghere_ndebà = Faịlụ * 4096 + 자리 / 4, gàa_valuu = (자리 & 3) * 8;
        ndịnà_valuu[oghere_ndebà] = (ndịnà_valuu[oghere_ndebà] & ~(255 << gàa_valuu)) | ((valuu & 255) << gàa_valuu);
    }

    public static int ụzọ_ozi_Mbido(int Ụhara) {
        ụzọ_ozi_ogologo = 0;
        if (Ụhara < 1 || Ụhara > 63) return -36;
        ụzọ_ozi_ogologo = Ụhara;
        for (int memmenwè_indèks = 0; memmenwè_indèks < Ụhara; memmenwè_indèks++) ụzọ_ozi[memmenwè_indèks] = 0;
        return 0;
    }
    public static int ụzọ_ozi_baịtị(int indèks, int valuu) {
        if (indèks < 0 || indèks >= ụzọ_ozi_ogologo || valuu < 1 || valuu > 255) return -22;
        ụzọ_ozi[indèks] = valuu; return 0;
    }
    static int chọta_ndebà() {
        for (int ọbọakwụkwọ_indèks = 0; ọbọakwụkwọ_indèks < 파일수; ọbọakwụkwọ_indèks++) if (이름길이[ọbọakwụkwọ_indèks] > 0 && 이름길이[ọbọakwụkwọ_indèks] == 정규길이 && 접두(Aha, ọbọakwụkwọ_indèks * 64, 이름길이[ọbọakwụkwọ_indèks], 정규, 정규길이)) return ọbọakwụkwọ_indèks;
        return -1;
    }
    public static int Mepee(int 플래그) {
        if (ụzọ_ozi_ogologo == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int memmenwè_indèks = 0; memmenwè_indèks < ụzọ_ozi_ogologo; memmenwè_indèks++) if (ụzọ_ozi[memmenwè_indèks] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int 결과 = mèzima_valuu(); if (결과 < 0) return 결과;
        if (chọta_dàịrektrị(정규길이) >= 0) return -21;
        결과 = 부모확인(); if (결과 < 0) return 결과;
        int Faịlụ = chọta_ndebà();
        if (Faịlụ >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Faịlụ < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int memmenwè_indèks = 0; memmenwè_indèks < 16; memmenwè_indèks++) if (사용[memmenwè_indèks] == 0) { 서술자 = memmenwè_indèks; break; }
        if (서술자 < 0) return -24;
        if (Faịlụ < 0) {
            for (int memmenwè_indèks = 0; memmenwè_indèks < 파일수; memmenwè_indèks++) if (이름길이[memmenwè_indèks] == 0 && 참조수[memmenwè_indèks] == 0) { Faịlụ = memmenwè_indèks; break; }
            if (Faịlụ < 0) return -28;
            이름길이[Faịlụ] = 정규길이;
            for (int memmenwè_indèks = 0; memmenwè_indèks < 정규길이; memmenwè_indèks++) Aha[Faịlụ * 64 + memmenwè_indèks] = 정규[memmenwè_indèks];
            ogologo_valuu[Faịlụ] = 0;
        }
        if ((플래그 & 0x200) != 0) ogologo_valuu[Faịlụ] = 0;
        사용[서술자] = 1; ebenlereanya[서술자] = Faịlụ; 위치[서술자] = 0; usoro_moòdù[서술자] = 플래그;
        참조수[Faịlụ]++;
        return 서술자 + 3;
    }
    static int nkwàdo_eziokwū(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Wepụta_ọzi(int 서술자) {
        int oghere_ndebà = nkwàdo_eziokwū(서술자);
        if (oghere_ndebà < 0 || (usoro_moòdù[oghere_ndebà] & 3) == 1) return -9;
        int Faịlụ = ebenlereanya[oghere_ndebà];
        if (위치[oghere_ndebà] >= ogologo_valuu[Faịlụ]) return 256; // EOF와 ǹdịnezie_datà 0x00..0xff 구별
        return 자료읽기(Faịlụ, 위치[oghere_ndebà]++);
    }
    public static int Chekwaa_ozi(int 서술자, int valuu) {
        int oghere_ndebà = nkwàdo_eziokwū(서술자);
        if (oghere_ndebà < 0 || (usoro_moòdù[oghere_ndebà] & 3) == 0) return -9;
        int Faịlụ = ebenlereanya[oghere_ndebà];
        if ((usoro_moòdù[oghere_ndebà] & 0x400) != 0) 위치[oghere_ndebà] = ogologo_valuu[Faịlụ];
        if (위치[oghere_ndebà] >= 16384) return -28;
        while (ogologo_valuu[Faịlụ] < 위치[oghere_ndebà]) dee_datà(Faịlụ, ogologo_valuu[Faịlụ]++, 0);
        dee_datà(Faịlụ, 위치[oghere_ndebà]++, valuu);
        if (ogologo_valuu[Faịlụ] < 위치[oghere_ndebà]) ogologo_valuu[Faịlụ] = 위치[oghere_ndebà];
        return 1;
    }
    public static int 옮기기(int 서술자, int 거리, int 기준) {
        int oghere_ndebà = nkwàdo_eziokwū(서술자);
        if (oghere_ndebà < 0) return -9;
        if (기준 < 0 || 기준 > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (기준 == 0 ? 0 : 기준 == 1 ? 위치[oghere_ndebà] : ogologo_valuu[ebenlereanya[oghere_ndebà]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        위치[oghere_ndebà] = 새위치; return 새위치;
    }
    public static int Mechie(int 서술자) {
        int oghere_ndebà = nkwàdo_eziokwū(서술자);
        if (oghere_ndebà < 0) return -9;
        참조수[ebenlereanya[oghere_ndebà]]--; 사용[oghere_ndebà] = 0; return 0;
    }
    public static int Ụhara(int 서술자) {
        int oghere_ndebà = nkwàdo_eziokwū(서술자); return oghere_ndebà < 0 ? -9 : ogologo_valuu[ebenlereanya[oghere_ndebà]];
    }
    public static int Seti_ogologo(int 서술자, int Ụhara) {
        int oghere_ndebà = nkwàdo_eziokwū(서술자);
        if (oghere_ndebà < 0 || (usoro_moòdù[oghere_ndebà] & 3) == 0) return -9;
        if (Ụhara < 0 || Ụhara > 16384) return -22;
        int Faịlụ = ebenlereanya[oghere_ndebà];
        while (ogologo_valuu[Faịlụ] < Ụhara) dee_datà(Faịlụ, ogologo_valuu[Faịlụ]++, 0);
        ogologo_valuu[Faịlụ] = Ụhara; return 0;
    }
    public static int 지우기() {
        if (ụzọ_ozi_ogologo == 0) return -22;
        int 결과 = mèzima_valuu(); if (결과 < 0) return 결과;
        if (chọta_dàịrektrị(정규길이) >= 0) return -21;
        결과 = 부모확인(); if (결과 < 0) return 결과;
        int Faịlụ = chọta_ndebà();
        if (Faịlụ < 0) return -2;
        이름길이[Faịlụ] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void ndebà_ndepụta() {
        ụzọ_ozi_Mbido(1); ụzọ_ozi_baịtị(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int indèks) {
        if (indèks < 0 || indèks >= 파일수 || 이름길이[indèks] == 0) return 0;
        for (int memmenwè_indèks = 0; memmenwè_indèks < 이름길이[indèks]; memmenwè_indèks++) if (Aha[indèks * 64 + memmenwè_indèks] == '/') return 0;
        return 이름길이[indèks];
    }
    public static int 공개이름바이트(int indèks, int 자리) {
        return indèks >= 0 && indèks < 파일수 && 자리 >= 0 && 자리 < 이름길이[indèks] ? Aha[indèks * 64 + 자리] : -22;
    }
    public static int 공개파일크기(int indèks) { return indèks >= 0 && indèks < 파일수 ? ogologo_valuu[indèks] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], dàịrektrị_akara_ahà = new int[16 * 64], dàịrektrị_ogologo = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int Bido, int ụzọ_ozi_valuu, int[] 앞, int N_ebuụzọ_ụzọ_ozi) {
        if (ụzọ_ozi_valuu < N_ebuụzọ_ụzọ_ozi) return false;
        for (int memmenwè_indèks = 0; memmenwè_indèks < N_ebuụzọ_ụzọ_ozi; memmenwè_indèks++) if (이름들[Bido + memmenwè_indèks] != 앞[memmenwè_indèks]) return false;
        return true;
    }
    static int mèzima_valuu() {
        if (ụzọ_ozi_ogologo == 0) return -22;
        정규길이 = ụzọ_ozi[0] == '/' ? 0 : 현재길이;
        for (int memmenwè_indèks = 0; memmenwè_indèks < 정규길이; memmenwè_indèks++) 정규[memmenwè_indèks] = 현재[memmenwè_indèks];
        int 읽는자리 = 0;
        while (읽는자리 < ụzọ_ozi_ogologo) {
            while (읽는자리 < ụzọ_ozi_ogologo && ụzọ_ozi[읽는자리] == '/') 읽는자리++;
            int 시작자리 = 읽는자리; while (읽는자리 < ụzọ_ozi_ogologo && ụzọ_ozi[읽는자리] != '/') { if (ụzọ_ozi[읽는자리] == 0) return -22; 읽는자리++; }
            int 항목수 = 읽는자리 - 시작자리; if (항목수 == 0 || 항목수 == 1 && ụzọ_ozi[시작자리] == '.') continue;
            if (항목수 == 2 && ụzọ_ozi[시작자리] == '.' && ụzọ_ozi[시작자리 + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + 항목수 + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int memmenwè_indèks = 시작자리; memmenwè_indèks < 읽는자리; memmenwè_indèks++) 정규[정규길이++] = ụzọ_ozi[memmenwè_indèks];
        }
        return 0;
    }
    static int chọta_dàịrektrị(int 항목수) {
        if (항목수 == 0) return 0;
        for (int memmenwè_indèks = 1; memmenwè_indèks < 16; memmenwè_indèks++) if (dàịrektrị_ogologo[memmenwè_indèks] == 항목수 && 접두(dàịrektrị_akara_ahà, memmenwè_indèks * 64, 항목수, 정규, 항목수)) return memmenwè_indèks;
        return -1;
    }
    static int 부모확인() {
        int 항목수 = 정규길이; while (항목수 > 0 && 정규[항목수 - 1] != '/') 항목수--;
        return chọta_dàịrektrị(항목수 == 0 ? 0 : 항목수 - 1) < 0 ? -2 : 0;
    }
    public static int mepụta_dàịrektrị() {
        int 처리값 = mèzima_valuu(); if (처리값 < 0) return 처리값;
        if (chọta_dàịrektrị(정규길이) >= 0 || chọta_ndebà() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int memmenwè_indèks = 1; memmenwè_indèks < 16; memmenwè_indèks++) if (dàịrektrị_ogologo[memmenwè_indèks] == 0) {
            dàịrektrị_ogologo[memmenwè_indèks] = 정규길이; for (int 안쪽자리 = 0; 안쪽자리 < 정규길이; 안쪽자리++) dàịrektrị_akara_ahà[memmenwè_indèks * 64 + 안쪽자리] = 정규[안쪽자리]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = mèzima_valuu(); if (처리값 < 0) return 처리값;
        if (chọta_dàịrektrị(정규길이) >= 0) return 2;
        return chọta_ndebà() >= 0 ? 1 : 0;
    }
    public static int gbanwèe_dàịrektrị() {
        int 처리값 = mèzima_valuu(); if (처리값 < 0) return 처리값;
        if (chọta_dàịrektrị(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int memmenwè_indèks = 0; memmenwè_indèks < 현재길이; memmenwè_indèks++) 현재[memmenwè_indèks] = 정규[memmenwè_indèks]; return 0;
    }
    public static int wepụ_dàịrektrị() {
        int 처리값 = mèzima_valuu(); if (처리값 < 0) return 처리값;
        int 폴더번호 = chọta_dàịrektrị(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int memmenwè_indèks = 0; memmenwè_indèks < 파일수; memmenwè_indèks++) {
            if (이름길이[memmenwè_indèks] > 정규길이 && 접두(Aha, memmenwè_indèks * 64, 이름길이[memmenwè_indèks], 정규, 정규길이) && Aha[memmenwè_indèks * 64 + 정규길이] == '/') return -39;
        }
        for (int memmenwè_indèks = 0; memmenwè_indèks < 16; memmenwè_indèks++) {
            if (dàịrektrị_ogologo[memmenwè_indèks] > 정규길이 && 접두(dàịrektrị_akara_ahà, memmenwè_indèks * 64, dàịrektrị_ogologo[memmenwè_indèks], 정규, 정규길이) && dàịrektrị_akara_ahà[memmenwè_indèks * 64 + 정규길이] == '/') return -39;
        }
        dàịrektrị_ogologo[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= 파일수 || 이름길이[원본번호] == 0) return -2;
        int 처리값 = mèzima_valuu(); if (처리값 < 0) return 처리값;
        if (chọta_dàịrektrị(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = chọta_ndebà(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int memmenwè_indèks = 0; memmenwè_indèks < 정규길이; memmenwè_indèks++) Aha[원본번호 * 64 + memmenwè_indèks] = 정규[memmenwè_indèks]; return 0;
    }
    static int ndebà_Mbido(int[] datà_MKPOKỌTA, int 시작점, int 항목수) {
        if (!접두(datà_MKPOKỌTA, 시작점, 항목수, 정규, 정규길이)) return -1;
        int 시작자리 = 정규길이;
        if (시작자리 > 0) { if (항목수 <= 시작자리 || datà_MKPOKỌTA[시작점 + 시작자리] != '/') return -1; 시작자리++; }
        if (항목수 <= 시작자리) return -1;
        for (int memmenwè_indèks = 시작자리; memmenwè_indèks < 항목수; memmenwè_indèks++) if (datà_MKPOKỌTA[시작점 + memmenwè_indèks] == '/') return -1;
        return 시작자리;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int memmenwè_indèks = 0; memmenwè_indèks < 현재길이; memmenwè_indèks++) 보드.직렬쓰기(현재[memmenwè_indèks]); }
    static int 경로목록() {
        int 처리값 = mèzima_valuu(); if (처리값 < 0) return 처리값;
        int ọbọakwụkwọ_ebenlereanya = chọta_ndebà();
        if (ọbọakwụkwọ_ebenlereanya >= 0) { for (int memmenwè_indèks = 0; memmenwè_indèks < 정규길이; memmenwè_indèks++) 보드.직렬쓰기(정규[memmenwè_indèks]); 단말.Chekwaa_ozi("  "); 단말.수(ogologo_valuu[ọbọakwụkwọ_ebenlereanya]); 단말.Chekwaa_ozi("baịtị_valuu(주기억 Faịlụ)\n"); return 0; }
        if (chọta_dàịrektrị(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (dàịrektrị_ogologo[뒷값] > 0) {
            int 시작자리 = ndebà_Mbido(dàịrektrị_akara_ahà, 뒷값 * 64, dàịrektrị_ogologo[뒷값]); if (시작자리 < 0) continue;
            for (int memmenwè_indèks = 시작자리; memmenwè_indèks < dàịrektrị_ogologo[뒷값]; memmenwè_indèks++) 보드.직렬쓰기(dàịrektrị_akara_ahà[뒷값 * 64 + memmenwè_indèks]); 단말.Chekwaa_ozi("/\n");
        }
        for (int ọbọakwụkwọ_indèks = 0; ọbọakwụkwọ_indèks < 파일수; ọbọakwụkwọ_indèks++) if (이름길이[ọbọakwụkwọ_indèks] > 0) {
            int 시작자리 = ndebà_Mbido(Aha, ọbọakwụkwọ_indèks * 64, 이름길이[ọbọakwụkwọ_indèks]); if (시작자리 < 0) continue;
            for (int memmenwè_indèks = 시작자리; memmenwè_indèks < 이름길이[ọbọakwụkwọ_indèks]; memmenwè_indèks++) 보드.직렬쓰기(Aha[ọbọakwụkwọ_indèks * 64 + memmenwè_indèks]);
            단말.Chekwaa_ozi("  "); 단말.수(ogologo_valuu[ọbọakwụkwọ_indèks]); 단말.Chekwaa_ozi("baịtị_valuu(주기억 Faịlụ)\n");
        }
        return 0;
    }
}
