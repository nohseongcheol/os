// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** faktisks_dati 부팅 후 호출되는 Java ieejas_punkts. JVM과 viesot 운영체제에 의존하지 않는다. */
public final class kodols {
    static int kopsumma_VALUE(int 끝) {
        int SUM_VALUE = 0;
        for (int INDEX = 1; INDEX <= 끝; INDEX++) SUM_VALUE += INDEX;
        return SUM_VALUE;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = kopsumma_VALUE(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int nodaļa_mērs = -1;
        int INDEX = atmiņa_reģions.piešķirt_Krātuve();
        boolean padot_VALUE = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / nodaļa_mērs == 최소
            && 최소 % nodaļa_mērs == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEX >= 0 && atmiņa_reģions.atdot_mērs(INDEX) && !atmiņa_reģions.atdot_mērs(INDEX);
        SMS_Terminālis.Rakstīt(padot_VALUE ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return padot_VALUE;
    }

    public static void Palaist() {
        SMS_Terminālis.Sagatavot();
        SMS_Terminālis.Rakstīt("JKOROS NATIVE JAVA\n");
        SMS_Terminālis.Rakstīt("자바 기계어 kodols_VALUE Palaist\n");
        if (ierīce_VALUE.부팅표식() != 0x2badb002) {
            SMS_Terminālis.Rakstīt("BAD MULTIBOOT MAGIC\n");
            ierīce_VALUE.정지();
        }
        if (!시험()) ierīce_VALUE.정지();
        if (atmiņa_reģions.UPPER_atmiņa_mainīt_izmērus() < 15360) {
            SMS_Terminālis.Rakstīt("At least 16 MiB RAM required\n");
            ierīce_VALUE.정지();
        }
        ierīce_VALUE.Sagatavot_lietotājs_programma();
        SMS_Terminālis.Rakstīt("USER ELF: ring 3 / paging / int 0x80\n");
        tīkls_draiveris.Sagatavot();
        tīkls_kopa.CLEAN_Process();
        atmiņa_failu_sistēma.Sagatavot();
        파일보존.Sagatavot();
        명령해석기.Palaist();
    }
}
