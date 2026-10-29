// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** real_date 부팅 후 호출되는 Java intrare_p. JVM과 gazdă 운영체제에 의존하지 않는다. */
public final class nucleu {
    static int total_VALUE(int 끝) {
        int SUM_VALUE = 0;
        for (int INDEX = 1; INDEX <= 끝; INDEX++) SUM_VALUE += INDEX;
        return SUM_VALUE;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = total_VALUE(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int divizie_KR = -1;
        int INDEX = Memorie_regiune.aloca_Stocare();
        boolean transfera_VALUE = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / divizie_KR == 최소
            && 최소 % divizie_KR == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEX >= 0 && Memorie_regiune.restitui_KR(INDEX) && !Memorie_regiune.restitui_KR(INDEX);
        SMS_Terminal.Scriere(transfera_VALUE ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return transfera_VALUE;
    }

    public static void Pornește() {
        SMS_Terminal.Pregătiți();
        SMS_Terminal.Scriere("JKOROS NATIVE JAVA\n");
        SMS_Terminal.Scriere("자바 기계어 nucleu_VALUE Pornește\n");
        if (mobil_VALUE.부팅표식() != 0x2badb002) {
            SMS_Terminal.Scriere("BAD MULTIBOOT MAGIC\n");
            mobil_VALUE.정지();
        }
        if (!시험()) mobil_VALUE.정지();
        if (Memorie_regiune.UPPER_Memorie_dimensiona() < 15360) {
            SMS_Terminal.Scriere("At least 16 MiB RAM required\n");
            mobil_VALUE.정지();
        }
        mobil_VALUE.Pregătiți_utilizator_program();
        SMS_Terminal.Scriere("USER ELF: ring 3 / paging / int 0x80\n");
        rețea_driver.Pregătiți();
        rețea_Teanc.CLEAN_Proces();
        Memorie_sistem_de_fișiere.Pregătiți();
        파일보존.Pregătiți();
        명령해석기.Pornește();
    }
}
