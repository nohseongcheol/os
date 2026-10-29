// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 anininga 작업 sukuttia_atuutilik 할당/반환. 일반 물리 mappigaq_atuutilik 관리자는 아니다. */
public final class 기억공간 {
    static int[] sukuttia_atuutilik = new int[8192];
    static int[] 사용 = new int[8];

    static int agguqtuut_naasaut(int turaarut) {
        return sunakkutaaq_atuutilik.기억읽기(turaarut) | (sunakkutaaq_atuutilik.기억읽기(turaarut + 1) << 8)
            | (sunakkutaaq_atuutilik.기억읽기(turaarut + 2) << 16) | (sunakkutaaq_atuutilik.기억읽기(turaarut + 3) << 24);
    }

    static int 위쪽기억크기() {
        int msinfo32_exe = sunakkutaaq_atuutilik.부팅정보();
        if (sunakkutaaq_atuutilik.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (agguqtuut_naasaut(msinfo32_exe) & 1) == 0) return -1;
        return agguqtuut_naasaut(msinfo32_exe + 8);
    }

    static int 할당() {
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 사용.length; nalunaiqsimavik++) {
            if (사용[nalunaiqsimavik] == 0) {
                사용[nalunaiqsimavik] = 1;
                for (int 칸 = 0; 칸 < 1024; 칸++) sukuttia_atuutilik[nalunaiqsimavik * 1024 + 칸] = 0;
                return nalunaiqsimavik;
            }
        }
        return -1;
    }

    static boolean 반환(int nalunaiqsimavik) {
        if (nalunaiqsimavik < 0 || nalunaiqsimavik >= 사용.length || 사용[nalunaiqsimavik] == 0) return false;
        사용[nalunaiqsimavik] = 0;
        return true;
    }

    static int 사용개수() {
        int 개수 = 0;
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 사용.length; nalunaiqsimavik++) 개수 += 사용[nalunaiqsimavik];
        return 개수;
    }
}
