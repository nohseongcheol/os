// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** verklig_data maskinstart 후 호출되는 Java startpunkt. JVM과 värd 운영체제에 의존하지 않는다. */
public final class kärna {
    static int summa_värde(int 끝) {
        int SUM_värde = 0;
        for (int INDEX = 1; INDEX <= 끝; INDEX++) SUM_värde += INDEX;
        return SUM_värde;
    }

    static boolean tester() {
        int[] 값들 = new int[4];
        값들[2] = summa_värde(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int Division_KR = -1;
        int INDEX = Minne_område.allokera_minne();
        boolean skicka_värde = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / Division_KR == 최소
            && 최소 % Division_KR == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEX >= 0 && Minne_område.Retur_KR(INDEX) && !Minne_område.Retur_KR(INDEX);
        SMS_Terminal.Skriv(skicka_värde ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return skicka_värde;
    }

    public static void Kör() {
        SMS_Terminal.Förbereda();
        SMS_Terminal.Skriv("JKOROS NATIVE JAVA\n");
        SMS_Terminal.Skriv("자바 기계어 kärna_värde Kör\n");
        if (enhet_värde.부팅표식() != 0x2badb002) {
            SMS_Terminal.Skriv("BAD MULTIBOOT MAGIC\n");
            enhet_värde.정지();
        }
        if (!tester()) enhet_värde.정지();
        if (Minne_område.VERSALER_Minne_storlek() < 15360) {
            SMS_Terminal.Skriv("At least 16 MiB RAM required\n");
            enhet_värde.정지();
        }
        enhet_värde.Förbereda_användare_app();
        SMS_Terminal.Skriv("USER ELF: ring 3 / paging / int 0x80\n");
        nätverk_drivrutin.Förbereda();
        nätverk_Stack.Rent_Process();
        Minne_filsystem.Förbereda();
        파일보존.Förbereda();
        명령해석기.Kör();
    }
}
