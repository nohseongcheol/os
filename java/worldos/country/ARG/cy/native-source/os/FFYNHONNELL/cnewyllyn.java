// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** go_iawn_data 부팅 후 호출되는 Java cofnod_p. JVM과 lletya 운영체제에 의존하지 않는다. */
public final class cnewyllyn {
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
        int rhannu_mesur = -1;
        int INDEX = 기억공간.dyrannu_Storio();
        boolean tocyn_VALUE = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / rhannu_mesur == 최소
            && 최소 % rhannu_mesur == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEX >= 0 && 기억공간.return_mesur(INDEX) && !기억공간.return_mesur(INDEX);
        SMS_Terfynell.Ysgrifennu(tocyn_VALUE ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return tocyn_VALUE;
    }

    public static void Gweithredu_2() {
        SMS_Terfynell.Paratoi();
        SMS_Terfynell.Ysgrifennu("JKOROS NATIVE JAVA\n");
        SMS_Terfynell.Ysgrifennu("자바 기계어 cnewyllyn_VALUE Gweithredu_2\n");
        if (dyfais_VALUE.부팅표식() != 0x2badb002) {
            SMS_Terfynell.Ysgrifennu("BAD MULTIBOOT MAGIC\n");
            dyfais_VALUE.정지();
        }
        if (!시험()) dyfais_VALUE.정지();
        if (기억공간.UPPER_Cof_newid_maint() < 15360) {
            SMS_Terfynell.Ysgrifennu("At least 16 MiB RAM required\n");
            dyfais_VALUE.정지();
        }
        dyfais_VALUE.Paratoi_defnyddiwr_Rhaglen();
        SMS_Terfynell.Ysgrifennu("USER ELF: ring 3 / paging / int 0x80\n");
        Rhwydwaith_gyrrwr.Paratoi();
        Rhwydwaith_pentwr.Glân_Proses();
        Cof_system_ffeiliau.Paratoi();
        파일보존.Paratoi();
        명령해석기.Gweithredu_2();
    }
}
