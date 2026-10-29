// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int ኣኺድ() {
        ተጠቃሚ.ጸሓፍ("Hello from a separate Java ELF!\n");
        ተጠቃሚ.ጸሓፍ(ተጠቃሚ.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int መሐበሪ = 0; መሐበሪ < ተጠቃሚ.인수개수(); መሐበሪ++) {
            ተጠቃሚ.ጸሓፍ("arg: "); ተጠቃሚ.ጸሓፍ(ተጠቃሚ.인수(መሐበሪ)); ተጠቃሚ.ጸሓፍ("\n");
        }
        return ተጠቃሚ.실행권한() == 3 ? 0 : 1;
    }
}
