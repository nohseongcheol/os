// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** tūturu_raraunga 부팅 후 호출되는 Java tāurunga_ira. JVM과 taurima 운영체제에 의존하지 않는다. */
public final class kākano {
    static int 합계(int 끝) {
        int SUM_uara = 0;
        for (int INDEX = 1; INDEX <= 끝; INDEX++) SUM_uara += INDEX;
        return SUM_uara;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = 합계(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int whakawehenga_mēhua = -1;
        int INDEX = 기억공간.tiritiri_Rokiroki();
        boolean whakawhiti_uara = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / whakawehenga_mēhua == 최소
            && 최소 % whakawehenga_mēhua == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEX >= 0 && 기억공간.반환(INDEX) && !기억공간.반환(INDEX);
        TEXT_Tauranga.Tuhia(whakawhiti_uara ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return whakawhiti_uara;
    }

    public static void whakahaere() {
        TEXT_Tauranga.Whakarite();
        TEXT_Tauranga.Tuhia("JKOROS NATIVE JAVA\n");
        TEXT_Tauranga.Tuhia("자바 기계어 kākano_uara_0611a8a8 whakahaere\n");
        if (pūkoro_uara.부팅표식() != 0x2badb002) {
            TEXT_Tauranga.Tuhia("BAD MULTIBOOT MAGIC\n");
            pūkoro_uara.정지();
        }
        if (!시험()) pūkoro_uara.정지();
        if (기억공간.UPPER_Pūmahara_rahi() < 15360) {
            TEXT_Tauranga.Tuhia("At least 16 MiB RAM required\n");
            pūkoro_uara.정지();
        }
        pūkoro_uara.Whakarite_kaiwhakamahi_kaupapa();
        TEXT_Tauranga.Tuhia("USER ELF: ring 3 / paging / int 0x80\n");
        whatunga_atekōkiri.Whakarite();
        whatunga_Huinga.CLEAN_Hātepe();
        Pūmahara_pūnaha_kōnae.Whakarite();
        파일보존.Whakarite();
        명령해석기.whakahaere();
    }
}
