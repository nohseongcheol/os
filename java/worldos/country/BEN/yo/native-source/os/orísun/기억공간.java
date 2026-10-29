// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 Ìwọ̀n 작업 abala_iye pín_Ibi_ìpamọ́/반환. 일반 물리 ojú_ìwé_iye 관리자는 아니다. */
public final class 기억공간 {
    static int[] abala_iye = new int[8192];
    static int[] 사용 = new int[8];

    static int ìpínsíwẹ́wẹ́_nọ́ńbà_odindi(int àdírẹ́ẹ̀sì) {
        return ohun_èlò_iye.기억읽기(àdírẹ́ẹ̀sì) | (ohun_èlò_iye.기억읽기(àdírẹ́ẹ̀sì + 1) << 8)
            | (ohun_èlò_iye.기억읽기(àdírẹ́ẹ̀sì + 2) << 16) | (ohun_èlò_iye.기억읽기(àdírẹ́ẹ̀sì + 3) << 24);
    }

    static int 위쪽기억크기() {
        int msinfo32_exe = ohun_èlò_iye.부팅정보();
        if (ohun_èlò_iye.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (ìpínsíwẹ́wẹ́_nọ́ńbà_odindi(msinfo32_exe) & 1) == 0) return -1;
        return ìpínsíwẹ́wẹ́_nọ́ńbà_odindi(msinfo32_exe + 8);
    }

    static int pín_Ibi_ìpamọ́() {
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 사용.length; wá_atọ̀ka_àkóónú++) {
            if (사용[wá_atọ̀ka_àkóónú] == 0) {
                사용[wá_atọ̀ka_àkóónú] = 1;
                for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < 1024; ààyè_ìfàyọkàsí_ìgbéwọlé++) abala_iye[wá_atọ̀ka_àkóónú * 1024 + ààyè_ìfàyọkàsí_ìgbéwọlé] = 0;
                return wá_atọ̀ka_àkóónú;
            }
        }
        return -1;
    }

    static boolean 반환(int wá_atọ̀ka_àkóónú) {
        if (wá_atọ̀ka_àkóónú < 0 || wá_atọ̀ka_àkóónú >= 사용.length || 사용[wá_atọ̀ka_àkóónú] == 0) return false;
        사용[wá_atọ̀ka_àkóónú] = 0;
        return true;
    }

    static int 사용개수() {
        int 개수 = 0;
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 사용.length; wá_atọ̀ka_àkóónú++) 개수 += 사용[wá_atọ̀ka_àkóónú];
        return 개수;
    }
}
