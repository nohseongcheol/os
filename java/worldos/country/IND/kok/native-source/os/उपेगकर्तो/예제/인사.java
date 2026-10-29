// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int चलोवप() {
        उपेगकर्तो.बरोवचें("Hello from a separate Java ELF!\n");
        उपेगकर्तो.बरोवचें(उपेगकर्तो.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEX = 0; INDEX < उपेगकर्तो.인수개수(); INDEX++) {
            उपेगकर्तो.बरोवचें("arg: "); उपेगकर्तो.बरोवचें(उपेगकर्तो.인수(INDEX)); उपेगकर्तो.बरोवचें("\n");
        }
        return उपेगकर्तो.실행권한() == 3 ? 0 : 1;
    }
}
