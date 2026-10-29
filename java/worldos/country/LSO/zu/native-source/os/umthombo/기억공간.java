// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 I_msinfo32_exe 조회와 4KiB 고정 Ubungako 작업 isigaba_inani abela_Indawo_yokugcina/반환. 일반 물리 ikhasi_inani 관리자는 아니다. */
public final class 기억공간 {
    static int[] isigaba_inani = new int[8192];
    static int[] 사용 = new int[8];

    static int zawula_inamba(int ikheli) {
        return idivayisi_inani.기억읽기(ikheli) | (idivayisi_inani.기억읽기(ikheli + 1) << 8)
            | (idivayisi_inani.기억읽기(ikheli + 2) << 16) | (idivayisi_inani.기억읽기(ikheli + 3) << 24);
    }

    static int 위쪽기억크기() {
        int I_msinfo32_exe = idivayisi_inani.부팅정보();
        if (idivayisi_inani.부팅표식() != 0x2badb002 || I_msinfo32_exe == 0 || (zawula_inamba(I_msinfo32_exe) & 1) == 0) return -1;
        return zawula_inamba(I_msinfo32_exe + 8);
    }

    static int abela_Indawo_yokugcina() {
        for (int thola_inkomba = 0; thola_inkomba < 사용.length; thola_inkomba++) {
            if (사용[thola_inkomba] == 0) {
                사용[thola_inkomba] = 1;
                for (int isikhala_okufakwayo = 0; isikhala_okufakwayo < 1024; isikhala_okufakwayo++) isigaba_inani[thola_inkomba * 1024 + isikhala_okufakwayo] = 0;
                return thola_inkomba;
            }
        }
        return -1;
    }

    static boolean 반환(int thola_inkomba) {
        if (thola_inkomba < 0 || thola_inkomba >= 사용.length || 사용[thola_inkomba] == 0) return false;
        사용[thola_inkomba] = 0;
        return true;
    }

    static int 사용개수() {
        int 개수 = 0;
        for (int thola_inkomba = 0; thola_inkomba < 사용.length; thola_inkomba++) 개수 += 사용[thola_inkomba];
        return 개수;
    }
}
