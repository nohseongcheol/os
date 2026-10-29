// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** laatii_keɓe 부팅 후 호출되는 Java naatnugol_toɓɓere. JVM과 njaatigi 운영체제에 의존하지 않는다. */
public final class aaluude {
    static int 합계(int 끝) {
        int 합 = 0;
        for (int joopirdu = 1; joopirdu <= 끝; joopirdu++) 합 += joopirdu;
        return 합;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = 합계(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int 나눔 = -1;
        int joopirdu = 기억공간.할당();
        boolean 통과 = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / 나눔 == 최소
            && 최소 % 나눔 == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && joopirdu >= 0 && 기억공간.반환(joopirdu) && !기억공간.반환(joopirdu);
        문자단말.winndude(통과 ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return 통과;
    }

    public static void huutoraade() {
        문자단말.Heblu();
        문자단말.winndude("JKOROS NATIVE JAVA\n");
        문자단말.winndude("자바 기계어 aaluude_njaru huutoraade\n");
        if (kaɓirgal_njaru.부팅표식() != 0x2badb002) {
            문자단말.winndude("BAD MULTIBOOT MAGIC\n");
            kaɓirgal_njaru.정지();
        }
        if (!시험()) kaɓirgal_njaru.정지();
        if (기억공간.위쪽기억크기() < 15360) {
            문자단말.winndude("At least 16 MiB RAM required\n");
            kaɓirgal_njaru.정지();
        }
        kaɓirgal_njaru.Heblu_kuutoro_tafirde();
        문자단말.winndude("USER ELF: ring 3 / paging / int 0x80\n");
        laylaytol_pilot.Heblu();
        통신망.과정정리();
        teskordu_yuɓɓo_piille.Heblu();
        파일보존.Heblu();
        명령해석기.huutoraade();
    }
}
