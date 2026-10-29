// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** nyakuri_amakurushingiro 부팅 후 호출되는 Java icyinjizwa_inota. JVM과 gucumbikira 운영체제에 의존하지 않는다. */
public final class intima {
    static int 합계(int 끝) {
        int 합 = 0;
        for (int umugerekashakiro = 1; umugerekashakiro <= 끝; umugerekashakiro++) 합 += umugerekashakiro;
        return 합;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = 합계(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int 나눔 = -1;
        int umugerekashakiro = 기억공간.kugenera_Ububiko();
        boolean 통과 = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / 나눔 == 최소
            && 최소 % 나눔 == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && umugerekashakiro >= 0 && 기억공간.반환(umugerekashakiro) && !기억공간.반환(umugerekashakiro);
        문자단말.kwandika(통과 ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return 통과;
    }

    public static void ihuriro() {
        문자단말.Gutegura();
        문자단말.kwandika("JKOROS NATIVE JAVA\n");
        문자단말.kwandika("자바 기계어 intima_agaciro ihuriro\n");
        if (igendanwa_agaciro.부팅표식() != 0x2badb002) {
            문자단말.kwandika("BAD MULTIBOOT MAGIC\n");
            igendanwa_agaciro.정지();
        }
        if (!시험()) igendanwa_agaciro.정지();
        if (기억공간.위쪽기억크기() < 15360) {
            문자단말.kwandika("At least 16 MiB RAM required\n");
            igendanwa_agaciro.정지();
        }
        igendanwa_agaciro.Gutegura_ukoresha_porogaramu();
        문자단말.kwandika("USER ELF: ring 3 / paging / int 0x80\n");
        Urusobemiyoboro_mukoresha.Gutegura();
        Urusobemiyoboro_Ikirundo.과정정리();
        ububiko_sisitemu_ya_dosiye.Gutegura();
        파일보존.Gutegura();
        명령해석기.ihuriro();
    }
}
