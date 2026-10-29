// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int चलाउनुहोस्() {
        प्रयोगकर्ता.लेख्नुहोस्("Hello from a separate Java ELF!\n");
        प्रयोगकर्ता.लेख्नुहोस्(प्रयोगकर्ता.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int अनुक्रमणिका = 0; अनुक्रमणिका < प्रयोगकर्ता.인수개수(); अनुक्रमणिका++) {
            प्रयोगकर्ता.लेख्नुहोस्("arg: "); प्रयोगकर्ता.लेख्नुहोस्(प्रयोगकर्ता.तर्क(अनुक्रमणिका)); प्रयोगकर्ता.लेख्नुहोस्("\n");
        }
        return प्रयोगकर्ता.실행권한() == 3 ? 0 : 1;
    }
}
