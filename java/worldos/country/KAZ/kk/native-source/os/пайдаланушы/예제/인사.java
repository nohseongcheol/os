// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Орындау_2() {
        пайдаланушы.Жазу("Hello from a separate Java ELF!\n");
        пайдаланушы.Жазу(пайдаланушы.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int индекс = 0; индекс < пайдаланушы.인수개수(); индекс++) {
            пайдаланушы.Жазу("arg: "); пайдаланушы.Жазу(пайдаланушы.Аргументтер(индекс)); пайдаланушы.Жазу("\n");
        }
        return пайдаланушы.실행권한() == 3 ? 0 : 1;
    }
}
