// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 panga_ukubwa 작업 sehemu_thamani tengea_Hifadhi/반환. 일반 물리 ukurasa_thamani 관리자는 아니다. */
public final class 기억공간 {
    static int[] sehemu_thamani = new int[8192];
    static int[] 사용 = new int[8];

    static int changanua_namba_kamili(int anwani) {
        return kifaa_thamani.기억읽기(anwani) | (kifaa_thamani.기억읽기(anwani + 1) << 8)
            | (kifaa_thamani.기억읽기(anwani + 2) << 16) | (kifaa_thamani.기억읽기(anwani + 3) << 24);
    }

    static int 위쪽기억크기() {
        int msinfo32_exe = kifaa_thamani.부팅정보();
        if (kifaa_thamani.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (changanua_namba_kamili(msinfo32_exe) & 1) == 0) return -1;
        return changanua_namba_kamili(msinfo32_exe + 8);
    }

    static int tengea_Hifadhi() {
        for (int kielezo = 0; kielezo < 사용.length; kielezo++) {
            if (사용[kielezo] == 0) {
                사용[kielezo] = 1;
                for (int Sloti_ingizo = 0; Sloti_ingizo < 1024; Sloti_ingizo++) sehemu_thamani[kielezo * 1024 + Sloti_ingizo] = 0;
                return kielezo;
            }
        }
        return -1;
    }

    static boolean 반환(int kielezo) {
        if (kielezo < 0 || kielezo >= 사용.length || 사용[kielezo] == 0) return false;
        사용[kielezo] = 0;
        return true;
    }

    static int 사용개수() {
        int 개수 = 0;
        for (int kielezo = 0; kielezo < 사용.length; kielezo++) 개수 += 사용[kielezo];
        return 개수;
    }
}
