// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class अभिनन्दन_ae353e94 {
    public static int चलाएँ() {
        उपयोगकर्ता.लिखें("Hello from a separate Java ELF!\n");
        उपयोगकर्ता.लिखें(उपयोगकर्ता.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int इंडेक्स = 0; इंडेक्स < उपयोगकर्ता.인수개수(); इंडेक्स++) {
            उपयोगकर्ता.लिखें("arg: "); उपयोगकर्ता.लिखें(उपयोगकर्ता.तर्क(इंडेक्स)); उपयोगकर्ता.लिखें("\n");
        }
        return उपयोगकर्ता.실행권한() == 3 ? 0 : 1;
    }
}
