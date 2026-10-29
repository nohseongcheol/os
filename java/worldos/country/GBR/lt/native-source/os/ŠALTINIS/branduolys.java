// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** faktinis_duomenys 부팅 후 호출되는 Java įrašas_p. JVM과 organizuoti 운영체제에 의존하지 않는다. */
public final class branduolys {
    static int bendras_VALUE(int 끝) {
        int SUM_VALUE = 0;
        for (int INDEX = 1; INDEX <= 끝; INDEX++) SUM_VALUE += INDEX;
        return SUM_VALUE;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = bendras_VALUE(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int dalyba_KR = -1;
        int INDEX = atmintis_sritis.priskirti_Saugykla();
        boolean perduoti_VALUE = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / dalyba_KR == 최소
            && 최소 % dalyba_KR == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEX >= 0 && atmintis_sritis.grąžinti_KR(INDEX) && !atmintis_sritis.grąžinti_KR(INDEX);
        SMS_Terminalas.Rašymas(perduoti_VALUE ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return perduoti_VALUE;
    }

    public static void Paleisti() {
        SMS_Terminalas.Parengti();
        SMS_Terminalas.Rašymas("JKOROS NATIVE JAVA\n");
        SMS_Terminalas.Rašymas("자바 기계어 branduolys_VALUE Paleisti\n");
        if (įrenginys_VALUE.부팅표식() != 0x2badb002) {
            SMS_Terminalas.Rašymas("BAD MULTIBOOT MAGIC\n");
            įrenginys_VALUE.정지();
        }
        if (!시험()) įrenginys_VALUE.정지();
        if (atmintis_sritis.UPPER_atmintis_dydis() < 15360) {
            SMS_Terminalas.Rašymas("At least 16 MiB RAM required\n");
            įrenginys_VALUE.정지();
        }
        įrenginys_VALUE.Parengti_naudotojas_programa();
        SMS_Terminalas.Rašymas("USER ELF: ring 3 / paging / int 0x80\n");
        tinklas_tvarkyklė.Parengti();
        tinklas_eilė.CLEAN_Procesas();
        atmintis_failų_sistema.Parengti();
        파일보존.Parengti();
        명령해석기.Paleisti();
    }
}
