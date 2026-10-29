// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int செயல்படுத்துக() {
        பயனர்.எழுது("Hello from a separate Java ELF!\n");
        பயனர்.எழுது(பயனர்.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int அடைவு = 0; அடைவு < பயனர்.인수개수(); அடைவு++) {
            பயனர்.எழுது("arg: "); பயனர்.எழுது(பயனர்.செயலுருபுகள்(அடைவு)); பயனர்.எழுது("\n");
        }
        return பயனர்.실행권한() == 3 ? 0 : 1;
    }
}
