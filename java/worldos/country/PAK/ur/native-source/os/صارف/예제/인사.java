// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int چلائیں() {
        صارف.لکھیں("Hello from a separate Java ELF!\n");
        صارف.لکھیں(صارف.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int اشاریہ = 0; اشاریہ < صارف.인수개수(); اشاریہ++) {
            صارف.لکھیں("arg: "); صارف.لکھیں(صارف.دلائل(اشاریہ)); صارف.لکھیں("\n");
        }
        return صارف.실행권한() == 3 ? 0 : 1;
    }
}
