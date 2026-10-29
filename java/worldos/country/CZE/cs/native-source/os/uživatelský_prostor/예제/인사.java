// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Spustit_2() {
        uživatelský_prostor.Zápis("Hello from a separate Java ELF!\n");
        uživatelský_prostor.Zápis(uživatelský_prostor.spuštění_oprávnění() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEX = 0; INDEX < uživatelský_prostor.인수개수(); INDEX++) {
            uživatelský_prostor.Zápis("arg: "); uživatelský_prostor.Zápis(uživatelský_prostor.argumenty(INDEX)); uživatelský_prostor.Zápis("\n");
        }
        return uživatelský_prostor.spuštění_oprávnění() == 3 ? 0 : 1;
    }
}
