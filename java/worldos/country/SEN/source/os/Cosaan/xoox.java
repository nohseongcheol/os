// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** liteew_mbir 부팅 후 호출되는 Java dugal_xabaar_Tomb. JVM과 dalal 운영체제에 의존하지 않는다. */
public final class xoox {
    static int 합계(int 끝) {
        int 합 = 0;
        for (int àlluwa_tur = 1; àlluwa_tur <= 끝; àlluwa_tur++) 합 += àlluwa_tur;
        return 합;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = 합계(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int 나눔 = -1;
        int àlluwa_tur = 기억공간.jagleel_Dencukaay();
        boolean jox_xëyma = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / 나눔 == 최소
            && 최소 % 나눔 == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && àlluwa_tur >= 0 && 기억공간.반환(àlluwa_tur) && !기억공간.반환(àlluwa_tur);
        문자단말.biir(jox_xëyma ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return jox_xëyma;
    }

    public static void daw() {
        문자단말.jël_matuwaay();
        문자단말.biir("JKOROS NATIVE JAVA\n");
        문자단말.biir("자바 기계어 xoox_xëyma daw\n");
        if (toftal_xëyma.부팅표식() != 0x2badb002) {
            문자단말.biir("BAD MULTIBOOT MAGIC\n");
            toftal_xëyma.정지();
        }
        if (!시험()) toftal_xëyma.정지();
        if (기억공간.위쪽기억크기() < 15360) {
            문자단말.biir("At least 16 MiB RAM required\n");
            toftal_xëyma.정지();
        }
        toftal_xëyma.jël_matuwaay_kiy_jariñoo_internet_jëfekaay();
        문자단말.biir("USER ELF: ring 3 / paging / int 0x80\n");
        mbaal_daraayba.jël_matuwaay();
        mbaal_Tegalo.과정정리();
        fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.jël_matuwaay();
        파일보존.jël_matuwaay();
        명령해석기.daw();
    }
}
