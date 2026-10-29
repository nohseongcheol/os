// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 Girma 작업 Sashi_Daraja kasafta_Wurin_adana/반환. 일반 물리 shafi_Daraja 관리자는 아니다. */
public final class 기억공간 {
    static int[] Sashi_Daraja = new int[8192];
    static int[] 사용 = new int[8];

    static int Daddatse_Lamba_mara(int imel) {
        return na_ura_Daraja.기억읽기(imel) | (na_ura_Daraja.기억읽기(imel + 1) << 8)
            | (na_ura_Daraja.기억읽기(imel + 2) << 16) | (na_ura_Daraja.기억읽기(imel + 3) << 24);
    }

    static int 위쪽기억크기() {
        int msinfo32_exe = na_ura_Daraja.부팅정보();
        if (na_ura_Daraja.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (Daddatse_Lamba_mara(msinfo32_exe) & 1) == 0) return -1;
        return Daddatse_Lamba_mara(msinfo32_exe + 8);
    }

    static int kasafta_Wurin_adana() {
        for (int Indes = 0; Indes < 사용.length; Indes++) {
            if (사용[Indes] == 0) {
                사용[Indes] = 1;
                for (int rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < 1024; rami_Mashigar_bayanai++) Sashi_Daraja[Indes * 1024 + rami_Mashigar_bayanai] = 0;
                return Indes;
            }
        }
        return -1;
    }

    static boolean 반환(int Indes) {
        if (Indes < 0 || Indes >= 사용.length || 사용[Indes] == 0) return false;
        사용[Indes] = 0;
        return true;
    }

    static int 사용개수() {
        int 개수 = 0;
        for (int Indes = 0; Indes < 사용.length; Indes++) 개수 += 사용[Indes];
        return 개수;
    }
}
