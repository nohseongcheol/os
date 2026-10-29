// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 òjìàrụ 과정의 파일서술자와 열린 Faịlụ 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int gụọ_dèe_ọkọlọtọ = 2, mepụta_ndebà = 64, 독점생성 = 128, hichaa_TOC = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] mepee_ebenjìaka = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], ebenlereanya = new int[서술자한도];
    static int[] 파일위치 = new int[서술자한도], mepee_Mwube = new int[서술자한도], 참조수 = new int[서술자한도];
    static int[] Netwọọkụ_ebenjìaka = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] ụzọ_ozi_akara_ahà = new int[64], dògharịa_datà = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return mepee_ebenjìaka[파일서술자] - 1;
    }
    static int 빈서술자(int Bido) {
        for (int indèks = Bido; indèks < 서술자한도; indèks++) if (mepee_ebenjìaka[indèks] == 0) return indèks;
        return -24;
    }
    static int oghere_ebenjìaka() {
        for (int indèks = 0; indèks < 서술자한도; indèks++) if (참조수[indèks] == 0) return indèks;
        return -24;
    }
    static int Banye(int 서술자, int 기술, int 파일종류, int ọbọakwụkwọ_ebenlereanya, int Mwube) {
        mepee_ebenjìaka[서술자] = 기술 + 1; 서술자설정[서술자] = (Mwube & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; ebenlereanya[기술] = ọbọakwụkwọ_ebenlereanya; 참조수[기술] = 1;
        mepee_Mwube[기술] = Mwube & (3 | 이어쓰기 | 기다리지않기); 파일위치[기술] = 0;
        Netwọọkụ_ebenjìaka[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void Mbido_ùsòrò() {
        과정정리();
        for (int indèks = 0; indèks < 3; indèks++) Banye(indèks, indèks, 1, indèks, indèks == 0 ? 0 : 1);
    }
    static void 과정정리() {
        for (int indèks = 0; indèks < 서술자한도; indèks++) if (mepee_ebenjìaka[indèks] != 0) mmechi_ọbọakwụkwọ(indèks);
    }
    static int mmechi_ọbọakwụkwọ(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        mepee_ebenjìaka[서술자] = 0; 서술자설정[서술자] = 0;
        참조수[기술]--;
        if (참조수[기술] == 0) {
            if (종류[기술] == 2) memọrị_sistèm_ọbọakwụkwo.열림수[ebenlereanya[기술]]--;
            if (종류[기술] == 3 && Netwọọkụ_ebenjìaka[기술] != 0) Netwọọkụ_ikpo.Mechie(Netwọọkụ_ebenjìaka[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 baịtị_valuu 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int àdreèsì) {
        if (!실행관리.ntipanye(àdreèsì, 1)) return -14;
        int 위치 = njìarụ_valuu.기억읽기(àdreèsì) == '/' ? 1 : 0;
        for (int ogologo_valuu = 0; ogologo_valuu < 64; ogologo_valuu++) {
            if (!실행관리.ntipanye(àdreèsì + 위치 + ogologo_valuu, 1)) return -14;
            int valuu = njìarụ_valuu.기억읽기(àdreèsì + 위치 + ogologo_valuu);
            ụzọ_ozi_akara_ahà[ogologo_valuu] = valuu;
            if (valuu == 0) return ogologo_valuu == 0 ? -2 : (memọrị_sistèm_ọbọakwụkwo.cheèk_akara_ahà(ụzọ_ozi_akara_ahà, ogologo_valuu) ? ogologo_valuu : -22);
            if (valuu == '/') return -20;
        }
        return -36;
    }
    static int mepee_ọbọakwụkwọ(int akara_ahà_àdreèsì, int Mwube, int 허가) {
        int ogologo_valuu = 경로읽기(akara_ahà_àdreèsì);
        if (ogologo_valuu < 0) return ogologo_valuu;
        if ((Mwube & ~(3 | mepụta_ndebà | 독점생성 | hichaa_TOC | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Mwube & 3) == 3 || ((Mwube & hichaa_TOC) != 0 && (Mwube & 3) == 0)) return -22;
        int Faịlụ = memọrị_sistèm_ọbọakwụkwo.chọta_ndebà(ụzọ_ozi_akara_ahà, ogologo_valuu);
        if (Faịlụ >= 0 && (Mwube & (mepụta_ndebà | 독점생성)) == (mepụta_ndebà | 독점생성)) return -17;
        if (Faịlụ == -2 && (Mwube & mepụta_ndebà) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = oghere_ebenjìaka();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Faịlụ == -2) {
            int 결과 = memọrị_sistèm_ọbọakwụkwo.Store_valuu(ụzọ_ozi_akara_ahà, ogologo_valuu, ụzọ_ozi_akara_ahà, 0);
            if (결과 < 0) return 결과;
            Faịlụ = memọrị_sistèm_ọbọakwụkwo.chọta_ndebà(ụzọ_ozi_akara_ahà, ogologo_valuu);
            memọrị_sistèm_ọbọakwụkwo.허가들[Faịlụ] = 허가 & 511;
        }
        if (Faịlụ < 0) return Faịlụ;
        if ((Mwube & hichaa_TOC) != 0) memọrị_sistèm_ọbọakwụkwo.ụha_ndepụta[Faịlụ] = 0;
        memọrị_sistèm_ọbọakwụkwo.열림수[Faịlụ]++;
        return Banye(서술자, 기술, 2, Faịlụ, Mwube);
    }
    static int 파일읽기(int 서술자, int datà_àdreèsì, int ogologo_valuu) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (mepee_Mwube[기술] & 3) == 1) return -9;
        if (ogologo_valuu < 0) return -22;
        if (ogologo_valuu == 0) return 0;
        if (!실행관리.ntipanye(datà_àdreèsì, ogologo_valuu)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, datà_àdreèsì, ogologo_valuu, 0, 0);
        if (종류[기술] == 1) {
            int 받은수 = 0;
            while (받은수 < ogologo_valuu) {
                int valuu = 문자단말.직렬읽기();
                if (valuu < 0) valuu = ụgbọọtụgwo.Wepụta_ọzi();
                if (valuu < 0) {
                    if (받은수 > 0) return 받은수;
                    if ((mepee_Mwube[기술] & 기다리지않기) != 0) return -11;
                    if (njìarụ_valuu.사용자남은밀리초() <= 10) return -11;
                    Netwọọkụ_ikpo.nkwàdo_eziokwū(); njìarụ_valuu.잠시양보();
                } else {
                    njìarụ_valuu.dee_memọrị(datà_àdreèsì + 받은수, valuu); 받은수++;
                }
            }
            return 받은수;
        }
        int Faịlụ = ebenlereanya[기술], 위치 = 파일위치[기술];
        if (위치 >= memọrị_sistèm_ọbọakwụkwo.ụha_ndepụta[Faịlụ]) return 0;
        if (ogologo_valuu > memọrị_sistèm_ọbọakwụkwo.ụha_ndepụta[Faịlụ] - 위치) ogologo_valuu = memọrị_sistèm_ọbọakwụkwo.ụha_ndepụta[Faịlụ] - 위치;
        int 원본주소 = njìarụ_valuu.ọbọakwụkwọ_memọrị() + Faịlụ * memọrị_sistèm_ọbọakwụkwo.최대크기 + 위치;
        for (int indèks = 0; indèks < ogologo_valuu; indèks++) njìarụ_valuu.dee_memọrị(datà_àdreèsì + indèks, njìarụ_valuu.기억읽기(원본주소 + indèks));
        파일위치[기술] += ogologo_valuu;
        return ogologo_valuu;
    }
    static int dee_ọbọakwụkwọ(int 서술자, int datà_àdreèsì, int ogologo_valuu) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (mepee_Mwube[기술] & 3) == 0) return -9;
        if (ogologo_valuu < 0) return -22;
        if (ogologo_valuu == 0) return 0;
        if (!실행관리.ntipanye(datà_àdreèsì, ogologo_valuu)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 ebemwèga_valuu 주소가 필요하다.
        if (종류[기술] == 1) {
            if (ogologo_valuu > 16384) ogologo_valuu = 16384;
            for (int indèks = 0; indèks < ogologo_valuu; indèks++) {
                int valuu = njìarụ_valuu.기억읽기(datà_àdreèsì + indèks);
                문자단말.직렬바이트(valuu); 문자단말.화면문자(valuu);
            }
            return ogologo_valuu;
        }
        int Faịlụ = ebenlereanya[기술], Ụhara = memọrị_sistèm_ọbọakwụkwo.ụha_ndepụta[Faịlụ];
        int 위치 = (mepee_Mwube[기술] & 이어쓰기) != 0 ? Ụhara : 파일위치[기술];
        if (위치 >= memọrị_sistèm_ọbọakwụkwo.최대크기) return -27;
        if (ogologo_valuu > memọrị_sistèm_ọbọakwụkwo.최대크기 - 위치) ogologo_valuu = memọrị_sistèm_ọbọakwụkwo.최대크기 - 위치;
        int ebemwèga_àdreèsì = njìarụ_valuu.ọbọakwụkwọ_memọrị() + Faịlụ * memọrị_sistèm_ọbọakwụkwo.최대크기;
        for (int indèks = Ụhara; indèks < 위치; indèks++) njìarụ_valuu.dee_memọrị(ebemwèga_àdreèsì + indèks, 0);
        for (int indèks = 0; indèks < ogologo_valuu; indèks++) njìarụ_valuu.dee_memọrị(ebemwèga_àdreèsì + 위치 + indèks, njìarụ_valuu.기억읽기(datà_àdreèsì + indèks));
        파일위치[기술] = 위치 + ogologo_valuu;
        if (위치 + ogologo_valuu > Ụhara) memọrị_sistèm_ọbọakwụkwo.ụha_ndepụta[Faịlụ] = 위치 + ogologo_valuu;
        return ogologo_valuu;
    }
    static int ọchịchọ_ọbọakwụkwọ(int 서술자, int Nnokwata_valuu, int 기준) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (기준 < 0 || 기준 > 2) return -22;
        int Bakgraụnd_valuu = 기준 == 0 ? 0 : (기준 == 1 ? 파일위치[기술] : memọrị_sistèm_ọbọakwụkwo.ụha_ndepụta[ebenlereanya[기술]]);
        if (Nnokwata_valuu > 0 && Bakgraụnd_valuu > 2147483647 - Nnokwata_valuu) return -75;
        if (Nnokwata_valuu < 0 && Nnokwata_valuu < -Bakgraụnd_valuu) return -22;
        파일위치[기술] = Bakgraụnd_valuu + Nnokwata_valuu;
        return 파일위치[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean 지정, int Mwube) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return 지정 ? -9 : -22;
        if (지정 && 서술자 == 새서술자) return 새서술자;
        if (지정) { if (mepee_ebenjìaka[새서술자] != 0) mmechi_ọbọakwụkwọ(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        mepee_ebenjìaka[새서술자] = 기술 + 1; 서술자설정[새서술자] = Mwube; 참조수[기술]++;
        return 새서술자;
    }
    static int wepụ_ọbọakwụkwọ_ndebà_akara_ahà(int akara_ahà_àdreèsì) {
        int ogologo_valuu = 경로읽기(akara_ahà_àdreèsì);
        if (ogologo_valuu < 0) return ogologo_valuu;
        int Faịlụ = memọrị_sistèm_ọbọakwụkwo.chọta_ndebà(ụzọ_ozi_akara_ahà, ogologo_valuu);
        if (Faịlụ < 0) return Faịlụ;
        memọrị_sistèm_ọbọakwụkwo.이름들[Faịlụ * 64] = 0;
        return 0;
    }
    static int Seti_ọbọakwụkwọ_ogologo(int 서술자, int ogologo_valuu) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (mepee_Mwube[기술] & 3) == 0 || ogologo_valuu < 0) return -22;
        if (ogologo_valuu > memọrị_sistèm_ọbọakwụkwo.최대크기) return -27;
        int Faịlụ = ebenlereanya[기술], àdreèsì = njìarụ_valuu.ọbọakwụkwọ_memọrị() + Faịlụ * memọrị_sistèm_ọbọakwụkwo.최대크기;
        for (int indèks = memọrị_sistèm_ọbọakwụkwo.ụha_ndepụta[Faịlụ]; indèks < ogologo_valuu; indèks++) njìarụ_valuu.dee_memọrị(àdreèsì + indèks, 0);
        memọrị_sistèm_ọbọakwụkwo.ụha_ndepụta[Faịlụ] = ogologo_valuu;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int àdreèsì) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.ntipanye(àdreèsì, 48)) return -14;
        for (int indèks = 0; indèks < 12; indèks++) 실행관리.수쓰기(àdreèsì + indèks * 4, 0);
        int Faịlụ = ebenlereanya[기술], Ụhara = 종류[기술] == 2 ? memọrị_sistèm_ọbọakwụkwo.ụha_ndepụta[Faịlụ] : 0;
        int 허가 = 종류[기술] == 2 ? memọrị_sistèm_ọbọakwụkwo.허가들[Faịlụ] : 438;
        실행관리.수쓰기(àdreèsì, 1);
        실행관리.수쓰기(àdreèsì + 4, 종류[기술] == 2 ? Faịlụ + 1 : 100 + 기술);
        실행관리.수쓰기(àdreèsì + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(àdreèsì + 12, 종류[기술] == 2 && memọrị_sistèm_ọbọakwụkwo.이름들[Faịlụ * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(àdreèsì + 28, Ụhara); 실행관리.수쓰기(àdreèsì + 32, 512);
        실행관리.수쓰기(àdreèsì + 36, (Ụhara + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int Ntiiwu, int valuu) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Ntiiwu == 0 || Ntiiwu == 1030) return 서술자복제(서술자, valuu, false, Ntiiwu == 1030 ? 1 : 0);
        if (Ntiiwu == 1) return 서술자설정[서술자];
        if (Ntiiwu == 2) { if ((valuu & ~1) != 0) return -22; 서술자설정[서술자] = valuu; return 0; }
        if (Ntiiwu == 3) return mepee_Mwube[기술];
        if (Ntiiwu == 4) {
            if ((valuu & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            mepee_Mwube[기술] = (mepee_Mwube[기술] & 3) | (valuu & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int 통신종단점만들기(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = oghere_ebenjìaka();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Banye(서술자, 기술, 3, 0, gụọ_dèe_ọkọlọtọ);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int àdreèsì_32(int àdreèsì) {
        return njìarụ_valuu.기억읽기(àdreèsì) << 24 | njìarụ_valuu.기억읽기(àdreèsì + 1) << 16
            | njìarụ_valuu.기억읽기(àdreèsì + 2) << 8 | njìarụ_valuu.기억읽기(àdreèsì + 3);
    }
    static int cheèk_àdreèsì(int àdreèsì, int ogologo_valuu) {
        if (ogologo_valuu < 16) return -22;
        if (!실행관리.ntipanye(àdreèsì, 16)) return -14;
        return 실행관리.짧은수(àdreèsì) == 2 ? 0 : -97;
    }
    static int JIKỌNYE_àdreèsì(int 서술자, int àdreèsì, int ogologo_valuu) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int 결과 = cheèk_àdreèsì(àdreèsì, ogologo_valuu);
        if (결과 < 0) return 결과;
        if (Netwọọkụ_ebenjìaka[기술] != 0) return -22;
        int Netwọọkụ_àdreèsì = àdreèsì_32(àdreèsì + 4);
        if (Netwọọkụ_àdreèsì != 0 && Netwọọkụ_àdreèsì != Netwọọkụ_ikpo.내주소) return -99;
        int 접속번호 = njìarụ_valuu.기억읽기(àdreèsì + 2) << 8 | njìarụ_valuu.기억읽기(àdreèsì + 3);
        결과 = Netwọọkụ_ikpo.Mepee(접속번호);
        if (결과 < 0) return 결과;
        Netwọọkụ_ebenjìaka[기술] = 결과; ebenlereanya[기술] = Netwọọkụ_àdreèsì;
        return 0;
    }
    static int 자동묶기(int 기술) {
        if (Netwọọkụ_ebenjìaka[기술] != 0) return 0;
        int 결과 = Netwọọkụ_ikpo.Mepee(0);
        if (결과 < 0) return 결과;
        Netwọọkụ_ebenjìaka[기술] = 결과;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 요청 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int datà_àdreèsì, int ogologo_valuu, int Mwube, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Mwube != 0) return -95;
        if (ogologo_valuu < 0 || ogologo_valuu > 1024) return -90;
        if (ogologo_valuu != 0 && !실행관리.ntipanye(datà_àdreèsì, ogologo_valuu)) return -14;
        if (!실행관리.ntipanye(요청주소, 8)) return -14;
        int àdreèsì = 실행관리.수(요청주소);
        int 결과 = cheèk_àdreèsì(àdreèsì, 실행관리.수(요청주소 + 4));
        if (결과 < 0) return 결과;
        int 접속번호 = njìarụ_valuu.기억읽기(àdreèsì + 2) << 8 | njìarụ_valuu.기억읽기(àdreèsì + 3);
        if (접속번호 == 0) return -22;
        결과 = 자동묶기(기술);
        if (결과 < 0) return 결과;
        for (int indèks = 0; indèks < ogologo_valuu; indèks++) dògharịa_datà[indèks] = njìarụ_valuu.기억읽기(datà_àdreèsì + indèks);
        return Netwọọkụ_ikpo.zìga(Netwọọkụ_ebenjìaka[기술], àdreèsì_32(àdreèsì + 4), 접속번호, dògharịa_datà, ogologo_valuu);
    }
    static void dee_àdreèsì(int àdreèsì, int ogologo_valuu, int Netwọọkụ_àdreèsì, int 접속번호) {
        for (int indèks = 0; indèks < ogologo_valuu && indèks < 16; indèks++) {
            int valuu = 0;
            if (indèks == 0) valuu = 2;
            if (indèks == 2) valuu = 접속번호 >>> 8;
            if (indèks == 3) valuu = 접속번호;
            if (indèks >= 4 && indèks < 8) valuu = Netwọọkụ_àdreèsì >>> (56 - indèks * 8);
            njìarụ_valuu.dee_memọrị(àdreèsì + indèks, valuu & 255);
        }
    }
    static int 자료전문받기(int 서술자, int datà_àdreèsì, int ogologo_valuu, int Mwube, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Mwube & ~64) != 0) return -95;
        if (ogologo_valuu < 0) return -22;
        if (ogologo_valuu != 0 && !실행관리.ntipanye(datà_àdreèsì, ogologo_valuu)) return -14;
        int àdreèsì = 0, àdreèsì_ogologo_àdreèsì = 0, àdreèsì_ogologo = 0;
        if (요청주소 != 0) {
            if (!실행관리.ntipanye(요청주소, 8)) return -14;
            àdreèsì = 실행관리.수(요청주소); àdreèsì_ogologo_àdreèsì = 실행관리.수(요청주소 + 4);
            if (àdreèsì != 0) {
                if (!실행관리.ntipanye(àdreèsì_ogologo_àdreèsì, 4)) return -14;
                àdreèsì_ogologo = 실행관리.수(àdreèsì_ogologo_àdreèsì);
                if (àdreèsì_ogologo < 0) return -22;
                if (!실행관리.ntipanye(àdreèsì, àdreèsì_ogologo < 16 ? àdreèsì_ogologo : 16)) return -14;
            }
        }
        int 결과 = 자동묶기(기술);
        if (결과 < 0) return 결과;
        int Bido = njìarụ_valuu.밀리초();
        while (true) {
            결과 = Netwọọkụ_ikpo.받기(Netwọọkụ_ebenjìaka[기술], dògharịa_datà, 1024, 0);
            if (결과 != -11) break;
            if ((Mwube & 64) != 0 || (mepee_Mwube[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && njìarụ_valuu.밀리초() - Bido >= 수신대기밀리초[기술]) return -11;
            if (njìarụ_valuu.사용자남은밀리초() <= 10) return -11;
            njìarụ_valuu.잠시양보();
        }
        if (결과 < 0) return 결과;
        if (결과 > ogologo_valuu) 결과 = ogologo_valuu;
        for (int indèks = 0; indèks < 결과; indèks++) njìarụ_valuu.dee_memọrị(datà_àdreèsì + indèks, dògharịa_datà[indèks]);
        if (àdreèsì != 0) {
            dee_àdreèsì(àdreèsì, àdreèsì_ogologo, Netwọọkụ_ikpo.ibè_àdreèsì(Netwọọkụ_ebenjìaka[기술]), Netwọọkụ_ikpo.상대접속번호(Netwọọkụ_ebenjìaka[기술]));
            실행관리.수쓰기(àdreèsì_ogologo_àdreèsì, 16);
        }
        return 결과;
    }
    static int 통신주소읽기(int 서술자, int àdreèsì, int ogologo_àdreèsì) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.ntipanye(ogologo_àdreèsì, 4)) return -14;
        int ogologo_valuu = 실행관리.수(ogologo_àdreèsì);
        if (ogologo_valuu < 0) return -22;
        if (!실행관리.ntipanye(àdreèsì, ogologo_valuu < 16 ? ogologo_valuu : 16)) return -14;
        int oghere_ndebà = Netwọọkụ_ikpo.indèks(Netwọọkụ_ebenjìaka[기술]);
        dee_àdreèsì(àdreèsì, ogologo_valuu, ebenlereanya[기술], oghere_ndebà < 0 ? 0 : Netwọọkụ_ikpo.접속번호들[oghere_ndebà]);
        실행관리.수쓰기(ogologo_àdreèsì, 16);
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
