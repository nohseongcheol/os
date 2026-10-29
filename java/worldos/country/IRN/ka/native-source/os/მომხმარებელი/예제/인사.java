// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int გაშვება() {
        მომხმარებელი.ჩაწერა("Hello from a separate Java ELF!\n");
        მომხმარებელი.ჩაწერა(მომხმარებელი.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int ინდექსი = 0; ინდექსი < მომხმარებელი.인수개수(); ინდექსი++) {
            მომხმარებელი.ჩაწერა("arg: "); მომხმარებელი.ჩაწერა(მომხმარებელი.인수(ინდექსი)); მომხმარებელი.ჩაწერა("\n");
        }
        return მომხმარებელი.실행권한() == 3 ? 0 : 1;
    }
}
