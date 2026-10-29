// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** raun_gögn 부팅 후 호출되는 Java færsla_P. JVM과 hýsa 운영체제에 의존하지 않는다. */
public final class kjarni {
    static int samtala_VALUE(int 끝) {
        int SUM_VALUE = 0;
        for (int INDEX = 1; INDEX <= 끝; INDEX++) SUM_VALUE += INDEX;
        return SUM_VALUE;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = samtala_VALUE(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int deiling_mæld_stærð = -1;
        int INDEX = 기억공간.úthluta_geymsla();
        boolean senda_VALUE = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / deiling_mæld_stærð == 최소
            && 최소 % deiling_mæld_stærð == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEX >= 0 && 기억공간.skila_mæld_stærð(INDEX) && !기억공간.skila_mæld_stærð(INDEX);
        SMS_Endastöð.Skrift(senda_VALUE ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return senda_VALUE;
    }

    public static void Keyra_2() {
        SMS_Endastöð.Undirbúa();
        SMS_Endastöð.Skrift("JKOROS NATIVE JAVA\n");
        SMS_Endastöð.Skrift("자바 기계어 kjarni_VALUE Keyra_2\n");
        if (tæki_VALUE.부팅표식() != 0x2badb002) {
            SMS_Endastöð.Skrift("BAD MULTIBOOT MAGIC\n");
            tæki_VALUE.정지();
        }
        if (!시험()) tæki_VALUE.정지();
        if (기억공간.UPPER_Minni_breyta_stærð() < 15360) {
            SMS_Endastöð.Skrift("At least 16 MiB RAM required\n");
            tæki_VALUE.정지();
        }
        tæki_VALUE.Undirbúa_notandi_forrit();
        SMS_Endastöð.Skrift("USER ELF: ring 3 / paging / int 0x80\n");
        Net_rekill.Undirbúa();
        Net_bunki.CLEAN_Ferli();
        Minni_skrárkerfi.Undirbúa();
        파일보존.Undirbúa();
        명령해석기.Keyra_2();
    }
}
