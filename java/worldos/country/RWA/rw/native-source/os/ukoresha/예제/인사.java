// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int ihuriro() {
        ukoresha.kwandika("Hello from a separate Java ELF!\n");
        ukoresha.kwandika(ukoresha.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int umugerekashakiro = 0; umugerekashakiro < ukoresha.인수개수(); umugerekashakiro++) {
            ukoresha.kwandika("arg: "); ukoresha.kwandika(ukoresha.인수(umugerekashakiro)); ukoresha.kwandika("\n");
        }
        return ukoresha.실행권한() == 3 ? 0 : 1;
    }
}
