// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** tota_tshedimosetso 부팅 후 호출되는 Java tsenyo_ntlha. JVM과 pinagare 운영체제에 의존하지 않는다. */
public final class Khenele {
    static int 합계(int 끝) {
        int 합 = 0;
        for (int tshupane = 1; tshupane <= 끝; tshupane++) 합 += tshupane;
        return 합;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = 합계(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int 나눔 = -1;
        int tshupane = 기억공간.abela_Polokelo();
        boolean fetisa_Boleng = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / 나눔 == 최소
            && 최소 % 나눔 == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && tshupane >= 0 && 기억공간.반환(tshupane) && !기억공간.반환(tshupane);
        문자단말.kwala(fetisa_Boleng ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return fetisa_Boleng;
    }

    public static void dirisa() {
        문자단말.Baakanya();
        문자단말.kwala("JKOROS NATIVE JAVA\n");
        문자단말.kwala("자바 기계어 Khenele_Boleng dirisa\n");
        if (mobaele_Boleng.부팅표식() != 0x2badb002) {
            문자단말.kwala("BAD MULTIBOOT MAGIC\n");
            mobaele_Boleng.정지();
        }
        if (!시험()) mobaele_Boleng.정지();
        if (기억공간.위쪽기억크기() < 15360) {
            문자단말.kwala("At least 16 MiB RAM required\n");
            mobaele_Boleng.정지();
        }
        mobaele_Boleng.Baakanya_modirisi_Tiriso();
        문자단말.kwala("USER ELF: ring 3 / paging / int 0x80\n");
        Neteweke_selaodi.Baakanya();
        Neteweke_kokoanyodinepe.과정정리();
        memori_setsamaisadifaele.Baakanya();
        파일보존.Baakanya();
        명령해석기.dirisa();
    }
}
