// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** faktisk_data 부팅 후 호출되는 Java inngangspunkt. JVM과 vert 운영체제에 의존하지 않는다. */
public final class kjerne {
    static int total_VERDI(int 끝) {
        int SUMMER_VERDI = 0;
        for (int INDEKS = 1; INDEKS <= 끝; INDEKS++) SUMMER_VERDI += INDEKS;
        return SUMMER_VERDI;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = total_VERDI(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int Divisjon_KR = -1;
        int INDEKS = Minne_område.tildele_lager();
        boolean sende_VERDI = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / Divisjon_KR == 최소
            && 최소 % Divisjon_KR == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEKS >= 0 && Minne_område.return_KR(INDEKS) && !Minne_område.return_KR(INDEKS);
        SMS_Terminal.Skriv(sende_VERDI ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return sende_VERDI;
    }

    public static void Kjør_2() {
        SMS_Terminal.Forbered();
        SMS_Terminal.Skriv("JKOROS NATIVE JAVA\n");
        SMS_Terminal.Skriv("자바 기계어 kjerne_VERDI Kjør_2\n");
        if (enhet_VERDI.부팅표식() != 0x2badb002) {
            SMS_Terminal.Skriv("BAD MULTIBOOT MAGIC\n");
            enhet_VERDI.정지();
        }
        if (!시험()) enhet_VERDI.정지();
        if (Minne_område.STORE_Minne_skalere() < 15360) {
            SMS_Terminal.Skriv("At least 16 MiB RAM required\n");
            enhet_VERDI.정지();
        }
        enhet_VERDI.Forbered_bruker_app();
        SMS_Terminal.Skriv("USER ELF: ring 3 / paging / int 0x80\n");
        nettverk_driver.Forbered();
        nettverk_stakk.RENSK_Prosess();
        Minne_filsystem.Forbered();
        파일보존.Forbered();
        명령해석기.Kjør_2();
    }
}
