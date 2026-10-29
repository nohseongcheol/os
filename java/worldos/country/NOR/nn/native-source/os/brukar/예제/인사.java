// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Køyr_2() {
        brukar.Skriv("Hello from a separate Java ELF!\n");
        brukar.Skriv(brukar.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEX = 0; INDEX < brukar.인수개수(); INDEX++) {
            brukar.Skriv("arg: "); brukar.Skriv(brukar.Argument(INDEX)); brukar.Skriv("\n");
        }
        return brukar.실행권한() == 3 ? 0 : 1;
    }
}
