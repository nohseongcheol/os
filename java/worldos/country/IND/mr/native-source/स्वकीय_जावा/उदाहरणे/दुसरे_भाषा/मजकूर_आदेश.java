// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import मराठी.जावा.वर्ण;

/** इतर भाषांना प्रमाणित निर्गतातून परिणाम घेता येणारा लहान Java प्रवेशबिंदू. */
public final class मजकूर_आदेश {
    public static void main(String[] बाबी) {
        if (बाबी.length != 1) {
            System.err.println("사용법: मजकूर_आदेश स्ट्रींग_मूल्य");
            System.exit(2);
        }
        System.out.println(वर्ण.वर्ण_कोड_संख्या(बाबी[0]));
    }
}
