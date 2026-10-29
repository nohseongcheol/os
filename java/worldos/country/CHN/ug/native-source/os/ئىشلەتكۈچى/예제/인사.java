// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int ئىجرا_قىل_2() {
        ئىشلەتكۈچى.ياز("Hello from a separate Java ELF!\n");
        ئىشلەتكۈچى.ياز(ئىشلەتكۈچى.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int ئىندېكس = 0; ئىندېكس < ئىشلەتكۈچى.인수개수(); ئىندېكس++) {
            ئىشلەتكۈچى.ياز("arg: "); ئىشلەتكۈچى.ياز(ئىشلەتكۈچى.ئۆزگەرگۈچىلەر(ئىندېكس)); ئىشلەتكۈچى.ياز("\n");
        }
        return ئىشلەتكۈچى.실행권한() == 3 ? 0 : 1;
    }
}
