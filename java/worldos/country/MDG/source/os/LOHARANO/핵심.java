// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 실제 부팅 후 호출되는 Java 진입점. JVM과 호스트 운영체제에 의존하지 않는다. */
public final class 핵심 {
    static int 합계(int 끝) {
        int 합 = 0;
        for (int 번호 = 1; 번호 <= 끝; 번호++) 합 += 번호;
        return 합;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = 합계(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int 나눔 = -1;
        int 번호 = 기억공간.할당();
        boolean 통과 = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / 나눔 == 최소
            && 최소 % 나눔 == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && 번호 >= 0 && 기억공간.반환(번호) && !기억공간.반환(번호);
        문자단말.Manoratra(통과 ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return 통과;
    }

    public static void Alefaso() {
        문자단말.준비();
        문자단말.Manoratra("JKOROS NATIVE JAVA\n");
        문자단말.Manoratra("자바 기계어 커널 Alefaso\n");
        if (장치.부팅표식() != 0x2badb002) {
            문자단말.Manoratra("BAD MULTIBOOT MAGIC\n");
            장치.정지();
        }
        if (!시험()) 장치.정지();
        if (기억공간.위쪽기억크기() < 15360) {
            문자단말.Manoratra("At least 16 MiB RAM required\n");
            장치.정지();
        }
        장치.사용자준비();
        문자단말.Manoratra("USER ELF: ring 3 / paging / int 0x80\n");
        망장치구동기.준비();
        통신망.과정정리();
        주기억파일체계.준비();
        파일보존.준비();
        명령해석기.Alefaso();
    }
}
