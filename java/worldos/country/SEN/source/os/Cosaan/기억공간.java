// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 tolluwaay 작업 dog_xëyma jagleel_Dencukaay/반환. 일반 물리 xët_xëyma 관리자는 아니다. */
public final class 기억공간 {
    static int[] dog_xëyma = new int[8192];
    static int[] 사용 = new int[8];

    static int Segg_lëmm(int dëkkuwaay) {
        return toftal_xëyma.기억읽기(dëkkuwaay) | (toftal_xëyma.기억읽기(dëkkuwaay + 1) << 8)
            | (toftal_xëyma.기억읽기(dëkkuwaay + 2) << 16) | (toftal_xëyma.기억읽기(dëkkuwaay + 3) << 24);
    }

    static int 위쪽기억크기() {
        int msinfo32_exe = toftal_xëyma.부팅정보();
        if (toftal_xëyma.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (Segg_lëmm(msinfo32_exe) & 1) == 0) return -1;
        return Segg_lëmm(msinfo32_exe + 8);
    }

    static int jagleel_Dencukaay() {
        for (int àlluwa_tur = 0; àlluwa_tur < 사용.length; àlluwa_tur++) {
            if (사용[àlluwa_tur] == 0) {
                사용[àlluwa_tur] = 1;
                for (int xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < 1024; xar_xar_dugal_xabaar++) dog_xëyma[àlluwa_tur * 1024 + xar_xar_dugal_xabaar] = 0;
                return àlluwa_tur;
            }
        }
        return -1;
    }

    static boolean 반환(int àlluwa_tur) {
        if (àlluwa_tur < 0 || àlluwa_tur >= 사용.length || 사용[àlluwa_tur] == 0) return false;
        사용[àlluwa_tur] = 0;
        return true;
    }

    static int 사용개수() {
        int 개수 = 0;
        for (int àlluwa_tur = 0; àlluwa_tur < 사용.length; àlluwa_tur++) 개수 += 사용[àlluwa_tur];
        return 개수;
    }
}
