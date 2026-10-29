// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** attwali_data 부팅 후 호출되는 Java entrata_punt. JVM과 host 운영체제에 의존하지 않는다. */
public final class kernel {
    static int 합계(int 끝) {
        int SUM_VALUE = 0;
        for (int INDEX = 1; INDEX <= 끝; INDEX++) SUM_VALUE += INDEX;
        return SUM_VALUE;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = 합계(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int diviżjoni_miżura = -1;
        int INDEX = 기억공간.alloka_Ħażna();
        boolean għadda_VALUE = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / diviżjoni_miżura == 최소
            && 최소 % diviżjoni_miżura == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEX >= 0 && 기억공간.반환(INDEX) && !기억공간.반환(INDEX);
        SMS_Terminal.kiteb(għadda_VALUE ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return għadda_VALUE;
    }

    public static void serje() {
        SMS_Terminal.Ħejji();
        SMS_Terminal.kiteb("JKOROS NATIVE JAVA\n");
        SMS_Terminal.kiteb("자바 기계어 kernel_VALUE serje\n");
        if (mowbajl_VALUE.부팅표식() != 0x2badb002) {
            SMS_Terminal.kiteb("BAD MULTIBOOT MAGIC\n");
            mowbajl_VALUE.정지();
        }
        if (!시험()) mowbajl_VALUE.정지();
        if (기억공간.UPPER_Memorja_daqqas() < 15360) {
            SMS_Terminal.kiteb("At least 16 MiB RAM required\n");
            mowbajl_VALUE.정지();
        }
        mowbajl_VALUE.Ħejji_utent_programm();
        SMS_Terminal.kiteb("USER ELF: ring 3 / paging / int 0x80\n");
        netwerk_drajver.Ħejji();
        netwerk_Munzell.CLEAN_Proċess();
        Memorja_sistema_tal_fajls.Ħejji();
        파일보존.Ħejji();
        명령해석기.serje();
    }
}
