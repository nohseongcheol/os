// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Bido() {
        òjìàrụ.Chekwaa_ozi("Hello from a separate Java ELF!\n");
        òjìàrụ.Chekwaa_ozi(òjìàrụ.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int indèks = 0; indèks < òjìàrụ.인수개수(); indèks++) {
            òjìàrụ.Chekwaa_ozi("arg: "); òjìàrụ.Chekwaa_ozi(òjìàrụ.인수(indèks)); òjìàrụ.Chekwaa_ozi("\n");
        }
        return òjìàrụ.실행권한() == 3 ? 0 : 1;
    }
}
