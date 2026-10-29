// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Käivita_2() {
        kasutaja.Kirjutamine("Hello from a separate Java ELF!\n");
        kasutaja.Kirjutamine(kasutaja.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEX = 0; INDEX < kasutaja.인수개수(); INDEX++) {
            kasutaja.Kirjutamine("arg: "); kasutaja.Kirjutamine(kasutaja.Argumendid(INDEX)); kasutaja.Kirjutamine("\n");
        }
        return kasutaja.실행권한() == 3 ? 0 : 1;
    }
}
