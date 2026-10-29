// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Rọ́ọ̀nù() {
        aṣàmúlò.Kọ("Hello from a separate Java ELF!\n");
        aṣàmúlò.Kọ(aṣàmúlò.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < aṣàmúlò.인수개수(); wá_atọ̀ka_àkóónú++) {
            aṣàmúlò.Kọ("arg: "); aṣàmúlò.Kọ(aṣàmúlò.인수(wá_atọ̀ka_àkóónú)); aṣàmúlò.Kọ("\n");
        }
        return aṣàmúlò.실행권한() == 3 ? 0 : 1;
    }
}
