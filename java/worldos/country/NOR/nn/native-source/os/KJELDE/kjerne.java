// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** faktisk_data 부팅 후 호출되는 Java oppføring_p. JVM과 vert 운영체제에 의존하지 않는다. */
public final class kjerne {
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
        int divisjon_forretningsmål = -1;
        int INDEX = 기억공간.tildele_Lagring();
        boolean sende_VALUE = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / divisjon_forretningsmål == 최소
            && 최소 % divisjon_forretningsmål == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEX >= 0 && 기억공간.levere_tilbake_forretningsmål(INDEX) && !기억공간.levere_tilbake_forretningsmål(INDEX);
        SMS_Terminal.Skriv(sende_VALUE ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return sende_VALUE;
    }

    public static void Køyr_2() {
        SMS_Terminal.Klargjer();
        SMS_Terminal.Skriv("JKOROS NATIVE JAVA\n");
        SMS_Terminal.Skriv("자바 기계어 kjerne_VALUE Køyr_2\n");
        if (mobil_VALUE.부팅표식() != 0x2badb002) {
            SMS_Terminal.Skriv("BAD MULTIBOOT MAGIC\n");
            mobil_VALUE.정지();
        }
        if (!시험()) mobil_VALUE.정지();
        if (기억공간.UPPER_Minne_endre_storleik() < 15360) {
            SMS_Terminal.Skriv("At least 16 MiB RAM required\n");
            mobil_VALUE.정지();
        }
        mobil_VALUE.Klargjer_brukar_app();
        SMS_Terminal.Skriv("USER ELF: ring 3 / paging / int 0x80\n");
        Nettverk_drivar.Klargjer();
        Nettverk_Stabel.CLEAN_Prosess();
        Minne_filsystem.Klargjer();
        파일보존.Klargjer();
        명령해석기.Køyr_2();
    }
}
