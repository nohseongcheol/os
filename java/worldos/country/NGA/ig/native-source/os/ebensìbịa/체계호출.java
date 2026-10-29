// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 òjìàrụ nrụaka/길이는 òhèrè_ndebà 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int MKPOKỌTA_ogologo(int àdreèsì) {
        if (!실행관리.ntipanye(àdreèsì, 4)) return -14;
        int ogologo_valuu = 실행관리.수(àdreèsì);
        if (ogologo_valuu < 0 || ogologo_valuu > (실행관리.òjìàrụ_mèdebe - àdreèsì - 4) / 4) return -14;
        return ogologo_valuu;
    }

    public static int ùsòrò_valuu_ndebà(int indèks, int 가, int 나, int 다, int 라, int 마) {
        if (indèks == 30) return 파일서술자관리.mepee_ọbọakwụkwọ(가, 나, 다);
        if (indèks == 31) return 파일서술자관리.파일읽기(가, 나, 다);
        if (indèks == 32) return 파일서술자관리.dee_ọbọakwụkwọ(가, 나, 다);
        if (indèks == 33) return 파일서술자관리.mmechi_ọbọakwụkwọ(가);
        if (indèks == 34) return 파일서술자관리.ọchịchọ_ọbọakwụkwọ(가, 나, 다);
        if (indèks == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (indèks == 36) return 파일서술자관리.서술자복제(가, 나, true, 0);
        if (indèks == 37) return 파일서술자관리.파일상태읽기(가, 나);
        if (indèks == 38) return 파일서술자관리.wepụ_ọbọakwụkwọ_ndebà_akara_ahà(가);
        if (indèks == 39) return 파일서술자관리.Seti_ọbọakwụkwọ_ogologo(가, 나);
        if (indèks == 40) return 파일서술자관리.서술자제어(가, 나, 다);
        if (indèks == 41) return 파일서술자관리.통신종단점만들기(가, 나, 다);
        if (indèks == 42) return 파일서술자관리.JIKỌNYE_àdreèsì(가, 나, 다);
        if (indèks == 43) return 파일서술자관리.자료전문보내기(가, 나, 다, 라, 마);
        if (indèks == 44) return 파일서술자관리.자료전문받기(가, 나, 다, 라, 마);
        if (indèks == 45) return 파일서술자관리.통신주소읽기(가, 나, 다);
        if (indèks == 46) return 파일서술자관리.수신대기정하기(가, 나);
        if (indèks == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.hàkọọ();
        }
        if (indèks == 1) {
            int ogologo_valuu = MKPOKỌTA_ogologo(가);
            if (ogologo_valuu < 0) return ogologo_valuu;
            if (ogologo_valuu > 4096) return -90;
            for (int mkpụrụedemede_valuu = 0; mkpụrụedemede_valuu < ogologo_valuu; mkpụrụedemede_valuu++) 문자단말.문자(실행관리.수(가 + 4 + mkpụrụedemede_valuu * 4) & 65535);
            return ogologo_valuu;
        }
        if (indèks == 2) return 실행관리.인수수;
        if (indèks == 3) return 가 >= 0 && 가 < 실행관리.인수수 ? 실행관리.agụment_àdreèsì[가] : 0;
        if (indèks == 10) return Netwọọkụ_ikpo.Mepee(가);
        if (indèks == 11) {
            int ogologo_valuu = MKPOKỌTA_ogologo(라);
            if (ogologo_valuu < 0) return ogologo_valuu;
            if (마 < 0 || 마 > ogologo_valuu || 마 > 1024) return -90;
            for (int 위치 = 0; 위치 < 마; 위치++) 임시자료[위치] = 실행관리.수(라 + 4 + 위치 * 4) & 255;
            return Netwọọkụ_ikpo.zìga(가, 나, 다, 임시자료, 마);
        }
        if (indèks == 12) {
            int ogologo_valuu = MKPOKỌTA_ogologo(나);
            if (ogologo_valuu < 0) return ogologo_valuu;
            if (다 < 0 || 다 > 2000) return -22;
            int 결과 = Netwọọkụ_ikpo.받기(가, 임시자료, ogologo_valuu < 1024 ? ogologo_valuu : 1024, 다);
            if (결과 >= 0) for (int 위치 = 0; 위치 < 결과; 위치++) 실행관리.수쓰기(나 + 4 + 위치 * 4, 임시자료[위치]);
            return 결과;
        }
        if (indèks == 13) return Netwọọkụ_ikpo.Mechie(가);
        if (indèks == 14) return Netwọọkụ_ikpo.내주소;
        if (indèks == 15) return Netwọọkụ_ikpo.ibè_àdreèsì(가);
        if (indèks == 16) return Netwọọkụ_ikpo.상대접속번호(가);
        if (indèks == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            문자단말.문자(가); return 1;
        }
        if (indèks == 20 || indèks == 21) {
            int akara_ahà_ụha = MKPOKỌTA_ogologo(가), datà_ụha = MKPOKỌTA_ogologo(나);
            if (akara_ahà_ụha < 0 || datà_ụha < 0) return -14;
            if (akara_ahà_ụha < 1 || akara_ahà_ụha > 64) return -22;
            int ogologo_valuu = 0;
            while (ogologo_valuu < akara_ahà_ụha && 실행관리.수(가 + 4 + ogologo_valuu * 4) != 0) {
                memọrị_sistèm_ọbọakwụkwo.Aha[ogologo_valuu] = 실행관리.수(가 + 4 + ogologo_valuu * 4);
                ogologo_valuu++;
            }
            if (!memọrị_sistèm_ọbọakwụkwo.cheèk_akara_ahà(memọrị_sistèm_ọbọakwụkwo.Aha, ogologo_valuu)) return -22;
            if (indèks == 20) {
                int Faịlụ = memọrị_sistèm_ọbọakwụkwo.chọta_ndebà(memọrị_sistèm_ọbọakwụkwo.Aha, ogologo_valuu);
                if (Faịlụ < 0) return Faịlụ;
                int Ụhara = memọrị_sistèm_ọbọakwụkwo.ụha_ndepụta[Faịlụ];
                if (Ụhara > datà_ụha) return -90;
                int àdreèsì = njìarụ_valuu.ọbọakwụkwọ_memọrị() + Faịlụ * memọrị_sistèm_ọbọakwụkwo.최대크기;
                for (int 수 = 0; 수 < Ụhara; 수++) 실행관리.수쓰기(나 + 4 + 수 * 4, njìarụ_valuu.기억읽기(àdreèsì + 수));
                return Ụhara;
            }
            if (다 < 0 || 다 > datà_ụha) return -22;
            if (다 > memọrị_sistèm_ọbọakwụkwo.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) memọrị_sistèm_ọbọakwụkwo.dezìmà_valuu[수] = 실행관리.수(나 + 4 + 수 * 4) & 255;
            return memọrị_sistèm_ọbọakwụkwo.Store_valuu(memọrị_sistèm_ọbọakwụkwo.Aha, ogologo_valuu, memọrị_sistèm_ọbọakwụkwo.dezìmà_valuu, 다);
        }
        return -38;
    }
}
