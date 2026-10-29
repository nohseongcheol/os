// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 실제 부팅 후 호출되는 Java ننوت_ټکى. JVM과 کوربه 운영체제에 의존하지 않는다. */
public final class نوغی {
    static int 합계(int 끝) {
        int 합 = 0;
        for (int لړیال = 1; لړیال <= 끝; لړیال++) 합 += لړیال;
        return 합;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = 합계(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int 나눔 = -1;
        int لړیال = 기억공간.할당();
        boolean 통과 = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / 나눔 == 최소
            && 최소 % 나눔 == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && لړیال >= 0 && 기억공간.반환(لړیال) && !기억공간.반환(لړیال);
        문자단말.لوستل_2(통과 ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return 통과;
    }

    public static void ځغلول() {
        문자단말.준비();
        문자단말.لوستل_2("JKOROS NATIVE JAVA\n");
        문자단말.لوستل_2("자바 기계어 نوغی_ارزښت ځغلول\n");
        if (وزله_ارزښت.부팅표식() != 0x2badb002) {
            문자단말.لوستل_2("BAD MULTIBOOT MAGIC\n");
            وزله_ارزښت.정지();
        }
        if (!시험()) وزله_ارزښت.정지();
        if (기억공간.위쪽기억크기() < 15360) {
            문자단말.لوستل_2("At least 16 MiB RAM required\n");
            وزله_ارزښت.정지();
        }
        وزله_ارزښت.사용자준비();
        문자단말.لوستل_2("USER ELF: ring 3 / paging / int 0x80\n");
        جال_چلاند.준비();
        통신망.과정정리();
        주기억파일체계.준비();
        파일보존.준비();
        명령해석기.ځغلول();
    }
}
