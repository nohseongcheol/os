// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int ማስኬጃ() {
        ተጠቃሚ.መጻፊያ("Hello from a separate Java ELF!\n");
        ተጠቃሚ.መጻፊያ(ተጠቃሚ.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int መረጃ_ጠቆመ = 0; መረጃ_ጠቆመ < ተጠቃሚ.인수개수(); መረጃ_ጠቆመ++) {
            ተጠቃሚ.መጻፊያ("arg: "); ተጠቃሚ.መጻፊያ(ተጠቃሚ.인수(መረጃ_ጠቆመ)); ተጠቃሚ.መጻፊያ("\n");
        }
        return ተጠቃሚ.실행권한() == 3 ? 0 : 1;
    }
}
