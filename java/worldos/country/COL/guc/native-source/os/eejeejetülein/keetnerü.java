// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 실제 부팅 후 호출되는 Java ekeroliaa_o_uchikanain. JVM과 epiajatü 운영체제에 의존하지 않는다. */
public final class keetnerü {
    static int 합계(int 끝) {
        int 합 = 0;
        for (int ee_iyatialujuna = 1; ee_iyatialujuna <= 끝; ee_iyatialujuna++) 합 += ee_iyatialujuna;
        return 합;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = 합계(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int 나눔 = -1;
        int ee_iyatialujuna = 기억공간.할당();
        boolean 통과 = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / 나눔 == 최소
            && 최소 % 나눔 == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && ee_iyatialujuna >= 0 && 기억공간.반환(ee_iyatialujuna) && !기억공간.반환(ee_iyatialujuna);
        문자단말.ashajaa(통과 ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return 통과;
    }

    public static void 시작() {
        문자단말.준비();
        문자단말.ashajaa("JKOROS NATIVE JAVA\n");
        문자단말.ashajaa("자바 기계어 keetnerü_ajutuu 시작\n");
        if (serulaalü_ajutuu.부팅표식() != 0x2badb002) {
            문자단말.ashajaa("BAD MULTIBOOT MAGIC\n");
            serulaalü_ajutuu.정지();
        }
        if (!시험()) serulaalü_ajutuu.정지();
        if (기억공간.위쪽기억크기() < 15360) {
            문자단말.ashajaa("At least 16 MiB RAM required\n");
            serulaalü_ajutuu.정지();
        }
        serulaalü_ajutuu.사용자준비();
        문자단말.ashajaa("USER ELF: ring 3 / paging / int 0x80\n");
        kusu_aa_inmajülü.준비();
        통신망.과정정리();
        주기억파일체계.준비();
        파일보존.준비();
        명령해석기.시작();
    }
}
