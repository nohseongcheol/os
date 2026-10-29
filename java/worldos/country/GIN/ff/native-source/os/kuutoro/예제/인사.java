// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int huutoraade() {
        kuutoro.winndude("Hello from a separate Java ELF!\n");
        kuutoro.winndude(kuutoro.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int joopirdu = 0; joopirdu < kuutoro.인수개수(); joopirdu++) {
            kuutoro.winndude("arg: "); kuutoro.winndude(kuutoro.인수(joopirdu)); kuutoro.winndude("\n");
        }
        return kuutoro.실행권한() == 3 ? 0 : 1;
    }
}
