// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int ځغلول() {
        کارن.لوستل_2("Hello from a separate Java ELF!\n");
        کارن.لوستل_2(کارن.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int لړیال = 0; لړیال < کارن.인수개수(); لړیال++) {
            کارن.لوستل_2("arg: "); کارن.لوستل_2(کارن.인수(لړیال)); کارن.لوستل_2("\n");
        }
        return کارن.실행권한() == 3 ? 0 : 1;
    }
}
