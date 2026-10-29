// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** aktuell_Daten 부팅 후 호출되는 Java Agab_Punkt. JVM과 Host 운영체제에 의존하지 않는다. */
public final class Kernel {
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
        int Divisioun_Mooss = -1;
        int INDEX = 기억공간.zouweisen_Späicher();
        boolean iwwermëttelen_VALUE = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / Divisioun_Mooss == 최소
            && 최소 % Divisioun_Mooss == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEX >= 0 && 기억공간.반환(INDEX) && !기억공간.반환(INDEX);
        SMS_Terminal.schreiwen(iwwermëttelen_VALUE ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return iwwermëttelen_VALUE;
    }

    public static void Laf() {
        SMS_Terminal.Préparéieren();
        SMS_Terminal.schreiwen("JKOROS NATIVE JAVA\n");
        SMS_Terminal.schreiwen("자바 기계어 Kernel_VALUE Laf\n");
        if (Mobil_VALUE.부팅표식() != 0x2badb002) {
            SMS_Terminal.schreiwen("BAD MULTIBOOT MAGIC\n");
            Mobil_VALUE.정지();
        }
        if (!시험()) Mobil_VALUE.정지();
        if (기억공간.UPPER_Späicher_d_Gréisst_veränneren() < 15360) {
            SMS_Terminal.schreiwen("At least 16 MiB RAM required\n");
            Mobil_VALUE.정지();
        }
        Mobil_VALUE.Préparéieren_Benotzer_App();
        SMS_Terminal.schreiwen("USER ELF: ring 3 / paging / int 0x80\n");
        Reseau_Driver.Préparéieren();
        Reseau_Stapel.CLEAN_Prozess();
        Späicher_Fichierssystem.Préparéieren();
        파일보존.Préparéieren();
        명령해석기.Laf();
    }
}
