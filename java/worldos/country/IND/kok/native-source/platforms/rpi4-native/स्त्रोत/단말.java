// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int मोल) {
        if (मोल < 0x80) बोर्ड.직렬쓰기(मोल);
        else if (मोल < 0x800) {
            बोर्ड.직렬쓰기(0xc0 | (मोल >> 6)); बोर्ड.직렬쓰기(0x80 | (मोल & 63));
        } else if (मोल < 0x10000) {
            बोर्ड.직렬쓰기(0xe0 | (मोल >> 12)); बोर्ड.직렬쓰기(0x80 | ((मोल >> 6) & 63)); बोर्ड.직렬쓰기(0x80 | (मोल & 63));
        } else {
            बोर्ड.직렬쓰기(0xf0 | (मोल >> 18)); बोर्ड.직렬쓰기(0x80 | ((मोल >> 12) & 63));
            बोर्ड.직렬쓰기(0x80 | ((मोल >> 6) & 63)); बोर्ड.직렬쓰기(0x80 | (मोल & 63));
        }
    }
    static void बरोवचें(String SMS) {
        for (int INDEX = 0; INDEX < SMS.length(); INDEX++) {
            int मोल = SMS.charAt(INDEX);
            if (मोल >= 0xd800 && मोल <= 0xdbff && INDEX + 1 < SMS.length()) {
                int 아래 = SMS.charAt(INDEX + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    मोल = 0x10000 + ((मोल - 0xd800) << 10) + 아래 - 0xdc00; INDEX++;
                }
            }
            if (मोल >= 0xd800 && मोल <= 0xdfff) मोल = 0xfffd;
            문자(मोल);
        }
    }
    static void 수(int मोल) {
        if (मोल < 0) 문자('-'); else मोल = -मोल;
        int स्थिती_INDEX = 1000000000;
        boolean चलोवप = false;
        while (स्थिती_INDEX > 0) {
            int अंक_मोल = -(मोल / स्थिती_INDEX);
            if (अंक_मोल != 0 || चलोवप || स्थिती_INDEX == 1) { 문자('0' + अंक_मोल); चलोवप = true; }
            मोल %= स्थिती_INDEX; स्थिती_INDEX /= 10;
        }
    }
}
