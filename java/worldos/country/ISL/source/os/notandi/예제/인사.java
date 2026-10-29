// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Keyra_2() {
        notandi.Skrift("Hello from a separate Java ELF!\n");
        notandi.Skrift(notandi.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEX = 0; INDEX < notandi.인수개수(); INDEX++) {
            notandi.Skrift("arg: "); notandi.Skrift(notandi.Viðföng(INDEX)); notandi.Skrift("\n");
        }
        return notandi.실행권한() == 3 ? 0 : 1;
    }
}
