// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Futtatás() {
        felhasználó.Írás("Hello from a separate Java ELF!\n");
        felhasználó.Írás(felhasználó.végrehajtás_engedély() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEX = 0; INDEX < felhasználó.인수개수(); INDEX++) {
            felhasználó.Írás("arg: "); felhasználó.Írás(felhasználó.Argumentumok(INDEX)); felhasználó.Írás("\n");
        }
        return felhasználó.végrehajtás_engedély() == 3 ? 0 : 1;
    }
}
