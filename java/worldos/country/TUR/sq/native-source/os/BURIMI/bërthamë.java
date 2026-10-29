// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** aktual_të_dhëna 부팅 후 호출되는 Java futje_p. JVM과 pritës 운영체제에 의존하지 않는다. */
public final class bërthamë {
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
        int pjesëtim_llogaritje = -1;
        int INDEX = 기억공간.caktoj_hapësira_ruajtëse();
        boolean kaloj_VALUE = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / pjesëtim_llogaritje == 최소
            && 최소 % pjesëtim_llogaritje == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEX >= 0 && 기억공간.Kthe_llogaritje(INDEX) && !기억공간.Kthe_llogaritje(INDEX);
        SMS_Terminali.Shkrimi(kaloj_VALUE ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return kaloj_VALUE;
    }

    public static void Ekzekuto() {
        SMS_Terminali.Përgatit();
        SMS_Terminali.Shkrimi("JKOROS NATIVE JAVA\n");
        SMS_Terminali.Shkrimi("자바 기계어 bërthamë_VALUE Ekzekuto\n");
        if (pajisje_VALUE.부팅표식() != 0x2badb002) {
            SMS_Terminali.Shkrimi("BAD MULTIBOOT MAGIC\n");
            pajisje_VALUE.정지();
        }
        if (!시험()) pajisje_VALUE.정지();
        if (기억공간.UPPER_Memorie_ndryshoj_përmasat() < 15360) {
            SMS_Terminali.Shkrimi("At least 16 MiB RAM required\n");
            pajisje_VALUE.정지();
        }
        pajisje_VALUE.Përgatit_përdorues_program();
        SMS_Terminali.Shkrimi("USER ELF: ring 3 / paging / int 0x80\n");
        rrjet_drejtues.Përgatit();
        rrjet_Stivë.CLEAN_Proces();
        Memorie_sistemi_i_skedarëve.Përgatit();
        파일보존.Përgatit();
        명령해석기.Ekzekuto();
    }
}
