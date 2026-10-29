// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** skutečný_data spuštění_stroje 후 호출되는 Java vstupní_bod. JVM과 hostit 운영체제에 의존하지 않는다. */
public final class jádro {
    static int celkem_HODNOTA(int 끝) {
        int SUMA_HODNOTA = 0;
        for (int INDEX = 1; INDEX <= 끝; INDEX++) SUMA_HODNOTA += INDEX;
        return SUMA_HODNOTA;
    }

    static boolean zkoušky() {
        int[] 값들 = new int[4];
        값들[2] = celkem_HODNOTA(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int podíl_KV = -1;
        int INDEX = Paměť_oblast.přidělit_Storage();
        boolean předat_HODNOTA = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / podíl_KV == 최소
            && 최소 % podíl_KV == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEX >= 0 && Paměť_oblast.Vratka_KV(INDEX) && !Paměť_oblast.Vratka_KV(INDEX);
        SMS_Terminál.Zápis(předat_HODNOTA ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return předat_HODNOTA;
    }

    public static void Spustit_2() {
        SMS_Terminál.Připravit();
        SMS_Terminál.Zápis("JKOROS NATIVE JAVA\n");
        SMS_Terminál.Zápis("자바 기계어 jádro_HODNOTA Spustit_2\n");
        if (mobilní_HODNOTA.부팅표식() != 0x2badb002) {
            SMS_Terminál.Zápis("BAD MULTIBOOT MAGIC\n");
            mobilní_HODNOTA.정지();
        }
        if (!zkoušky()) mobilní_HODNOTA.정지();
        if (Paměť_oblast.VELKÁ_Paměť_změnit_velikost() < 15360) {
            SMS_Terminál.Zápis("At least 16 MiB RAM required\n");
            mobilní_HODNOTA.정지();
        }
        mobilní_HODNOTA.Připravit_uživatel_program();
        SMS_Terminál.Zápis("USER ELF: ring 3 / paging / int 0x80\n");
        síť_ovladač.Připravit();
        síť_Štos.Čisté_Proces();
        Paměť_systém_souborů.Připravit();
        파일보존.Připravit();
        příkaz_interpret.Spustit_2();
    }
}
