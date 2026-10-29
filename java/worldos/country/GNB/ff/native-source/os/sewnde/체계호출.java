// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 kuutoro 포인터/길이는 naatde_naatnugol 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int 배열길이(int ñiiɓirde) {
        if (!실행관리.kilip(ñiiɓirde, 4)) return -14;
        int njuuteendi_njaru = 실행관리.수(ñiiɓirde);
        if (njuuteendi_njaru < 0 || njuuteendi_njaru > (실행관리.kuutoro_taƴde - ñiiɓirde - 4) / 4) return -14;
        return njuuteendi_njaru;
    }

    public static int Yuɓɓo_golle_njaru_naatnugol(int joopirdu, int 가, int 나, int 다, int 라, int 마) {
        if (joopirdu == 30) return 파일서술자관리.udditde_fiilde(가, 나, 다);
        if (joopirdu == 31) return 파일서술자관리.파일읽기(가, 나, 다);
        if (joopirdu == 32) return 파일서술자관리.winndude_fiilde(가, 나, 다);
        if (joopirdu == 33) return 파일서술자관리.uddude_fiilde(가);
        if (joopirdu == 34) return 파일서술자관리.파일위치옮기기(가, 나, 다);
        if (joopirdu == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (joopirdu == 36) return 파일서술자관리.서술자복제(가, 나, true, 0);
        if (joopirdu == 37) return 파일서술자관리.파일상태읽기(가, 나);
        if (joopirdu == 38) return 파일서술자관리.ittude_fiilde_naatnugol_innde(가);
        if (joopirdu == 39) return 파일서술자관리.파일길이정하기(가, 나);
        if (joopirdu == 40) return 파일서술자관리.서술자제어(가, 나, 다);
        if (joopirdu == 41) return 파일서술자관리.통신종단점만들기(가, 나, 다);
        if (joopirdu == 42) return 파일서술자관리.seŋondir_ñiiɓirde(가, 나, 다);
        if (joopirdu == 43) return 파일서술자관리.자료전문보내기(가, 나, 다, 라, 마);
        if (joopirdu == 44) return 파일서술자관리.자료전문받기(가, 나, 다, 라, 마);
        if (joopirdu == 45) return 파일서술자관리.통신주소읽기(가, 나, 다);
        if (joopirdu == 46) return 파일서술자관리.수신대기정하기(가, 나);
        if (joopirdu == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.sanngoɗinde();
        }
        if (joopirdu == 1) {
            int njuuteendi_njaru = 배열길이(가);
            if (njuuteendi_njaru < 0) return njuuteendi_njaru;
            if (njuuteendi_njaru > 4096) return -90;
            for (int alkulal_njaru = 0; alkulal_njaru < njuuteendi_njaru; alkulal_njaru++) 문자단말.문자(실행관리.수(가 + 4 + alkulal_njaru * 4) & 65535);
            return njuuteendi_njaru;
        }
        if (joopirdu == 2) return 실행관리.인수수;
        if (joopirdu == 3) return 가 >= 0 && 가 < 실행관리.인수수 ? 실행관리.hujja_ñiiɓirde[가] : 0;
        if (joopirdu == 10) return 통신망.udditde(가);
        if (joopirdu == 11) {
            int njuuteendi_njaru = 배열길이(라);
            if (njuuteendi_njaru < 0) return njuuteendi_njaru;
            if (마 < 0 || 마 > njuuteendi_njaru || 마 > 1024) return -90;
            for (int 위치 = 0; 위치 < 마; 위치++) 임시자료[위치] = 실행관리.수(라 + 4 + 위치 * 4) & 255;
            return 통신망.neldude(가, 나, 다, 임시자료, 마);
        }
        if (joopirdu == 12) {
            int njuuteendi_njaru = 배열길이(나);
            if (njuuteendi_njaru < 0) return njuuteendi_njaru;
            if (다 < 0 || 다 > 2000) return -22;
            int 결과 = 통신망.받기(가, 임시자료, njuuteendi_njaru < 1024 ? njuuteendi_njaru : 1024, 다);
            if (결과 >= 0) for (int 위치 = 0; 위치 < 결과; 위치++) 실행관리.수쓰기(나 + 4 + 위치 * 4, 임시자료[위치]);
            return 결과;
        }
        if (joopirdu == 13) return 통신망.uddude(가);
        if (joopirdu == 14) return 통신망.내주소;
        if (joopirdu == 15) return 통신망.giƴiraaɗo_ñiiɓirde(가);
        if (joopirdu == 16) return 통신망.상대접속번호(가);
        if (joopirdu == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            문자단말.문자(가); return 1;
        }
        if (joopirdu == 20 || joopirdu == 21) {
            int innde_waylude_etannde = 배열길이(가), keɓe_waylude_etannde = 배열길이(나);
            if (innde_waylude_etannde < 0 || keɓe_waylude_etannde < 0) return -14;
            if (innde_waylude_etannde < 1 || innde_waylude_etannde > 64) return -22;
            int njuuteendi_njaru = 0;
            while (njuuteendi_njaru < innde_waylude_etannde && 실행관리.수(가 + 4 + njuuteendi_njaru * 4) != 0) {
                teskordu_yuɓɓo_piille.innde[njuuteendi_njaru] = 실행관리.수(가 + 4 + njuuteendi_njaru * 4);
                njuuteendi_njaru++;
            }
            if (!teskordu_yuɓɓo_piille.sek_innde(teskordu_yuɓɓo_piille.innde, njuuteendi_njaru)) return -22;
            if (joopirdu == 20) {
                int fiilde = teskordu_yuɓɓo_piille.yiylaade_naatnugol(teskordu_yuɓɓo_piille.innde, njuuteendi_njaru);
                if (fiilde < 0) return fiilde;
                int waylude_etannde = teskordu_yuɓɓo_piille.waylude_etannde_Doggol[fiilde];
                if (waylude_etannde > keɓe_waylude_etannde) return -90;
                int ñiiɓirde = kaɓirgal_njaru.fiilde_teskordu() + fiilde * teskordu_yuɓɓo_piille.최대크기;
                for (int 수 = 0; 수 < waylude_etannde; 수++) 실행관리.수쓰기(나 + 4 + 수 * 4, kaɓirgal_njaru.기억읽기(ñiiɓirde + 수));
                return waylude_etannde;
            }
            if (다 < 0 || 다 > keɓe_waylude_etannde) return -22;
            if (다 > teskordu_yuɓɓo_piille.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) teskordu_yuɓɓo_piille.feewnditde_njaru[수] = 실행관리.수(나 + 4 + 수 * 4) & 255;
            return teskordu_yuɓɓo_piille.resde_njaru(teskordu_yuɓɓo_piille.innde, njuuteendi_njaru, teskordu_yuɓɓo_piille.feewnditde_njaru, 다);
        }
        return -38;
    }
}
