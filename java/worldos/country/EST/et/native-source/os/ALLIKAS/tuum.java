// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** tegelik_andmed 부팅 후 호출되는 Java kirje_p. JVM과 host 운영체제에 의존하지 않는다. */
public final class tuum {
    static int kokku_VALUE(int 끝) {
        int SUM_VALUE = 0;
        for (int INDEX = 1; INDEX <= 끝; INDEX++) SUM_VALUE += INDEX;
        return SUM_VALUE;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = kokku_VALUE(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int allüksus_näitaja = -1;
        int INDEX = Mälu_regioon.lisama_salvesti();
        boolean edastama_VALUE = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / allüksus_näitaja == 최소
            && 최소 % allüksus_näitaja == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEX >= 0 && Mälu_regioon.tagasi_saatma_näitaja(INDEX) && !Mälu_regioon.tagasi_saatma_näitaja(INDEX);
        SMS_terminal.Kirjutamine(edastama_VALUE ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return edastama_VALUE;
    }

    public static void Käivita_2() {
        SMS_terminal.Ettevalmistamine();
        SMS_terminal.Kirjutamine("JKOROS NATIVE JAVA\n");
        SMS_terminal.Kirjutamine("자바 기계어 tuum_VALUE Käivita_2\n");
        if (seade_VALUE.부팅표식() != 0x2badb002) {
            SMS_terminal.Kirjutamine("BAD MULTIBOOT MAGIC\n");
            seade_VALUE.정지();
        }
        if (!시험()) seade_VALUE.정지();
        if (Mälu_regioon.UPPER_Mälu_suurust_muutma() < 15360) {
            SMS_terminal.Kirjutamine("At least 16 MiB RAM required\n");
            seade_VALUE.정지();
        }
        seade_VALUE.Ettevalmistamine_kasutaja_programm();
        SMS_terminal.Kirjutamine("USER ELF: ring 3 / paging / int 0x80\n");
        võrk_draiver.Ettevalmistamine();
        võrk_Virn.CLEAN_Joonis();
        Mälu_failisüsteem.Ettevalmistamine();
        파일보존.Ettevalmistamine();
        명령해석기.Käivita_2();
    }
}
