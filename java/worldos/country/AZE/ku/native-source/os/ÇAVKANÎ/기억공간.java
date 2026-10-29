// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 정보 조회와 4KiB 고정 Mezinahî 작업 구역 할당/반환. 일반 물리 쪽 관리자는 아니다. */
public final class 기억공간 {
    static int[] 구역 = new int[8192];
    static int[] 사용 = new int[8];

    static int 정수읽기(int 주소) {
        return 장치.기억읽기(주소) | (장치.기억읽기(주소 + 1) << 8)
            | (장치.기억읽기(주소 + 2) << 16) | (장치.기억읽기(주소 + 3) << 24);
    }

    static int 위쪽기억크기() {
        int 정보 = 장치.부팅정보();
        if (장치.부팅표식() != 0x2badb002 || 정보 == 0 || (정수읽기(정보) & 1) == 0) return -1;
        return 정수읽기(정보 + 8);
    }

    static int 할당() {
        for (int 번호 = 0; 번호 < 사용.length; 번호++) {
            if (사용[번호] == 0) {
                사용[번호] = 1;
                for (int 칸 = 0; 칸 < 1024; 칸++) 구역[번호 * 1024 + 칸] = 0;
                return 번호;
            }
        }
        return -1;
    }

    static boolean 반환(int 번호) {
        if (번호 < 0 || 번호 >= 사용.length || 사용[번호] == 0) return false;
        사용[번호] = 0;
        return true;
    }

    static int 사용개수() {
        int 개수 = 0;
        for (int 번호 = 0; 번호 < 사용.length; 번호++) 개수 += 사용[번호];
        return 개수;
    }
}
