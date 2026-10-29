// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** taannallarik_titiqqat 부팅 후 호출되는 Java Iliniku_puinti. JVM과 tuttarvik 운영체제에 의존하지 않는다. */
public final class kernel {
    static int 합계(int 끝) {
        int 합 = 0;
        for (int nalunaiqsimavik = 1; nalunaiqsimavik <= 끝; nalunaiqsimavik++) 합 += nalunaiqsimavik;
        return 합;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = 합계(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int 나눔 = -1;
        int nalunaiqsimavik = 기억공간.할당();
        boolean 통과 = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / 나눔 == 최소
            && 최소 % 나눔 == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && nalunaiqsimavik >= 0 && 기억공간.반환(nalunaiqsimavik) && !기억공간.반환(nalunaiqsimavik);
        문자단말.titiraq(통과 ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return 통과;
    }

    public static void 시작() {
        문자단말.Parnalli();
        문자단말.titiraq("JKOROS NATIVE JAVA\n");
        문자단말.titiraq("자바 기계어 kernel_atuutilik 시작\n");
        if (sunakkutaaq_atuutilik.부팅표식() != 0x2badb002) {
            문자단말.titiraq("BAD MULTIBOOT MAGIC\n");
            sunakkutaaq_atuutilik.정지();
        }
        if (!시험()) sunakkutaaq_atuutilik.정지();
        if (기억공간.위쪽기억크기() < 15360) {
            문자단말.titiraq("At least 16 MiB RAM required\n");
            sunakkutaaq_atuutilik.정지();
        }
        sunakkutaaq_atuutilik.Parnalli_atuqtuq_pilirijjut();
        문자단말.titiraq("USER ELF: ring 3 / paging / int 0x80\n");
        Kasuqatigiitsimajut_qarasaujalirijjut.Parnalli();
        통신망.과정정리();
        puigujjaikkut_inikkuvik.Parnalli();
        파일보존.Parnalli();
        명령해석기.시작();
    }
}
