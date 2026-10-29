// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int هلائڻ() {
        صارف.لکو("Hello from a separate Java ELF!\n");
        صارف.لکو(صارف.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int ابتدائي = 0; ابتدائي < صارف.인수개수(); ابتدائي++) {
            صارف.لکو("arg: "); صارف.لکو(صارف.인수(ابتدائي)); صارف.لکو("\n");
        }
        return صارف.실행권한() == 3 ? 0 : 1;
    }
}
