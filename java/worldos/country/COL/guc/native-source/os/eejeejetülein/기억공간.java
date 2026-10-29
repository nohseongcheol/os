// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 정보 조회와 4KiB 고정 크기 작업 alüjalee_ajutuu 할당/반환. 일반 물리 ee_iyalaaya_ajutuu 관리자는 아니다. */
public final class 기억공간 {
    static int[] alüjalee_ajutuu = new int[8192];
    static int[] 사용 = new int[8];

    static int akatajaa_waneepiasü(int ejepüsee) {
        return serulaalü_ajutuu.기억읽기(ejepüsee) | (serulaalü_ajutuu.기억읽기(ejepüsee + 1) << 8)
            | (serulaalü_ajutuu.기억읽기(ejepüsee + 2) << 16) | (serulaalü_ajutuu.기억읽기(ejepüsee + 3) << 24);
    }

    static int 위쪽기억크기() {
        int 정보 = serulaalü_ajutuu.부팅정보();
        if (serulaalü_ajutuu.부팅표식() != 0x2badb002 || 정보 == 0 || (akatajaa_waneepiasü(정보) & 1) == 0) return -1;
        return akatajaa_waneepiasü(정보 + 8);
    }

    static int 할당() {
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 사용.length; ee_iyatialujuna++) {
            if (사용[ee_iyatialujuna] == 0) {
                사용[ee_iyatialujuna] = 1;
                for (int 칸 = 0; 칸 < 1024; 칸++) alüjalee_ajutuu[ee_iyatialujuna * 1024 + 칸] = 0;
                return ee_iyatialujuna;
            }
        }
        return -1;
    }

    static boolean 반환(int ee_iyatialujuna) {
        if (ee_iyatialujuna < 0 || ee_iyatialujuna >= 사용.length || 사용[ee_iyatialujuna] == 0) return false;
        사용[ee_iyatialujuna] = 0;
        return true;
    }

    static int 사용개수() {
        int 개수 = 0;
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 사용.length; ee_iyatialujuna++) 개수 += 사용[ee_iyatialujuna];
        return 개수;
    }
}
