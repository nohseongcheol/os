// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** todellinen_data koneen_käynnistys 후 호출되는 Java aloituskohta. JVM과 isäntä 운영체제에 의존하지 않는다. */
public final class ydin {
    static int summa_ARVO(int 끝) {
        int SUM_ARVO = 0;
        for (int INDEKSI = 1; INDEKSI <= 끝; INDEKSI++) SUM_ARVO += INDEKSI;
        return SUM_ARVO;
    }

    static boolean testit() {
        int[] 값들 = new int[4];
        값들[2] = summa_ARVO(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int jako_KR = -1;
        int INDEKSI = Muisti_alue.jakaa_Tallennus();
        boolean välittää_ARVO = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / jako_KR == 최소
            && 최소 % jako_KR == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEKSI >= 0 && Muisti_alue.palauttaa_KR(INDEKSI) && !Muisti_alue.palauttaa_KR(INDEKSI);
        SMS_Pääte.Kirjoitus(välittää_ARVO ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return välittää_ARVO;
    }

    public static void Suorita_2() {
        SMS_Pääte.Valmistele();
        SMS_Pääte.Kirjoitus("JKOROS NATIVE JAVA\n");
        SMS_Pääte.Kirjoitus("자바 기계어 ydin_ARVO Suorita_2\n");
        if (laite_ARVO.부팅표식() != 0x2badb002) {
            SMS_Pääte.Kirjoitus("BAD MULTIBOOT MAGIC\n");
            laite_ARVO.정지();
        }
        if (!testit()) laite_ARVO.정지();
        if (Muisti_alue.ISOT_Muisti_muuttaa_kokoa() < 15360) {
            SMS_Pääte.Kirjoitus("At least 16 MiB RAM required\n");
            laite_ARVO.정지();
        }
        laite_ARVO.Valmistele_käyttäjä_ohjelma();
        SMS_Pääte.Kirjoitus("USER ELF: ring 3 / paging / int 0x80\n");
        verkko_ohjain.Valmistele();
        verkko_Pino.SIIVOA_prosessi();
        Muisti_tiedostojärjestelmä.Valmistele();
        파일보존.Valmistele();
        명령해석기.Suorita_2();
    }
}
