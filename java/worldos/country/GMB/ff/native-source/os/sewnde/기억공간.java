// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 waylude_etannde 작업 taƴre_njaru 할당/반환. 일반 물리 hello_njaru 관리자는 아니다. */
public final class 기억공간 {
    static int[] taƴre_njaru = new int[8192];
    static int[] 사용 = new int[8];

    static int 정수읽기(int ñiiɓirde) {
        return kaɓirgal_njaru.기억읽기(ñiiɓirde) | (kaɓirgal_njaru.기억읽기(ñiiɓirde + 1) << 8)
            | (kaɓirgal_njaru.기억읽기(ñiiɓirde + 2) << 16) | (kaɓirgal_njaru.기억읽기(ñiiɓirde + 3) << 24);
    }

    static int 위쪽기억크기() {
        int msinfo32_exe = kaɓirgal_njaru.부팅정보();
        if (kaɓirgal_njaru.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (정수읽기(msinfo32_exe) & 1) == 0) return -1;
        return 정수읽기(msinfo32_exe + 8);
    }

    static int 할당() {
        for (int joopirdu = 0; joopirdu < 사용.length; joopirdu++) {
            if (사용[joopirdu] == 0) {
                사용[joopirdu] = 1;
                for (int 칸 = 0; 칸 < 1024; 칸++) taƴre_njaru[joopirdu * 1024 + 칸] = 0;
                return joopirdu;
            }
        }
        return -1;
    }

    static boolean 반환(int joopirdu) {
        if (joopirdu < 0 || joopirdu >= 사용.length || 사용[joopirdu] == 0) return false;
        사용[joopirdu] = 0;
        return true;
    }

    static int 사용개수() {
        int 개수 = 0;
        for (int joopirdu = 0; joopirdu < 사용.length; joopirdu++) 개수 += 사용[joopirdu];
        return 개수;
    }
}
