// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** werklik_data 부팅 후 호출되는 Java inskrywing_p. JVM과 hou 운영체제에 의존하지 않는다. */
public final class kern {
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
        int deling_maatreël = -1;
        int INDEX = 기억공간.toewys_Berging();
        boolean aanstuur_VALUE = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / deling_maatreël == 최소
            && 최소 % deling_maatreël == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEX >= 0 && 기억공간.teruggee_maatreël(INDEX) && !기억공간.teruggee_maatreël(INDEX);
        SMS_Terminaal.Skryf(aanstuur_VALUE ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return aanstuur_VALUE;
    }

    public static void Loop() {
        SMS_Terminaal.Maak_gereed();
        SMS_Terminaal.Skryf("JKOROS NATIVE JAVA\n");
        SMS_Terminaal.Skryf("자바 기계어 kern_VALUE Loop\n");
        if (mobiel_VALUE.부팅표식() != 0x2badb002) {
            SMS_Terminaal.Skryf("BAD MULTIBOOT MAGIC\n");
            mobiel_VALUE.정지();
        }
        if (!시험()) mobiel_VALUE.정지();
        if (기억공간.UPPER_Geheue_verstel() < 15360) {
            SMS_Terminaal.Skryf("At least 16 MiB RAM required\n");
            mobiel_VALUE.정지();
        }
        mobiel_VALUE.Maak_gereed_gebruiker_program();
        SMS_Terminaal.Skryf("USER ELF: ring 3 / paging / int 0x80\n");
        Netwerk_drywer.Maak_gereed();
        Netwerk_Stapel.CLEAN_Proses();
        Geheue_lêerstelsel.Maak_gereed();
        파일보존.Maak_gereed();
        명령해석기.Loop();
    }
}
