// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 정보 조회와 4KiB 고정 کچ 작업 برخه_ارزښت 할당/반환. 일반 물리 مخ_ارزښت 관리자는 아니다. */
public final class 기억공간 {
    static int[] برخه_ارزښت = new int[8192];
    static int[] 사용 = new int[8];

    static int تجزیه_صحيح_عدد(int پته) {
        return وزله_ارزښت.기억읽기(پته) | (وزله_ارزښت.기억읽기(پته + 1) << 8)
            | (وزله_ارزښت.기억읽기(پته + 2) << 16) | (وزله_ارزښت.기억읽기(پته + 3) << 24);
    }

    static int 위쪽기억크기() {
        int 정보 = وزله_ارزښت.부팅정보();
        if (وزله_ارزښت.부팅표식() != 0x2badb002 || 정보 == 0 || (تجزیه_صحيح_عدد(정보) & 1) == 0) return -1;
        return تجزیه_صحيح_عدد(정보 + 8);
    }

    static int 할당() {
        for (int لړیال = 0; لړیال < 사용.length; لړیال++) {
            if (사용[لړیال] == 0) {
                사용[لړیال] = 1;
                for (int 칸 = 0; 칸 < 1024; 칸++) برخه_ارزښت[لړیال * 1024 + 칸] = 0;
                return لړیال;
            }
        }
        return -1;
    }

    static boolean 반환(int لړیال) {
        if (لړیال < 0 || لړیال >= 사용.length || 사용[لړیال] == 0) return false;
        사용[لړیال] = 0;
        return true;
    }

    static int 사용개수() {
        int 개수 = 0;
        for (int لړیال = 0; لړیال < 사용.length; لړیال++) 개수 += 사용[لړیال];
        return 개수;
    }
}
