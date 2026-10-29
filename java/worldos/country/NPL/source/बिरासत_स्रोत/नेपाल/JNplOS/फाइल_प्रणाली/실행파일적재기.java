// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package नेपाल.JNplOS.फाइल_प्रणाली;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian कार्यान्वयन_गर्नुहोस्_आदेश 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class सेक्सन_मान {
        private final int 종류;
        private final int झन्डा_मान;
        private final int ठेगाना;
        private final int फाइल_राख्नुहोस्;
        private final int आकार;

        सेक्सन_मान(int 종류, int झन्डा_मान, int ठेगाना, int फाइल_राख्नुहोस्, int आकार) {
            this.종류 = 종류;
            this.झन्डा_मान = झन्डा_मान;
            this.ठेगाना = ठेगाना;
            this.फाइल_राख्नुहोस् = फाइल_राख्नुहोस्;
            this.आकार = आकार;
        }

        public int 종류() {
            return 종류;
        }

        public int झन्डा_मान() {
            return झन्डा_मान;
        }

        public int ठेगाना() {
            return ठेगाना;
        }

        public int फाइल_राख्नुहोस्() {
            return फाइल_राख्नुहोस्;
        }

        public int आकार() {
            return आकार;
        }
    }

    public static final class छवि {
        private final int सुरु_ठेगाना;
        private final List<सेक्सन_मान> 구역들;

        छवि(int सुरु_ठेगाना, List<सेक्सन_मान> 구역들) {
            this.सुरु_ठेगाना = सुरु_ठेगाना;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int सुरु_ठेगाना() {
            return सुरु_ठेगाना;
        }

        public List<सेक्सन_मान> 구역들() {
            return 구역들;
        }
    }

    public छवि 검사(byte[] लगत) {
        if (लगत == null || लगत.length < 52
                || लगत[0] != 0x7f || लगत[1] != 'E' || लगत[2] != 'L' || लगत[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (लगत[4] != 1 || लगत[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int सुरु_ठेगाना = पदच्छेद_गर्नुहोस्_पूर्ण_सङ्ख्या(लगत, 24);
        int सेक्सन_तालिका_राख्नुहोस् = पदच्छेद_गर्नुहोस्_पूर्ण_सङ्ख्या(लगत, 32);
        int सेक्सन_प्रविष्टि_साइज = 짧은정수읽기(लगत, 46);
        int 구역수 = 짧은정수읽기(लगत, 48);
        if (सेक्सन_प्रविष्टि_साइज < 40 || सेक्सन_तालिका_राख्नुहोस् < 0
                || (long) सेक्सन_तालिका_राख्नुहोस् + (long) सेक्सन_प्रविष्टि_साइज * 구역수 > लगत.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<सेक्सन_मान> 구역들 = new ArrayList<सेक्सन_मान>();
        for (int अनुक्रमणिका = 0; अनुक्रमणिका < 구역수; अनुक्रमणिका++) {
            int स्थिति = सेक्सन_तालिका_राख्नुहोस् + अनुक्रमणिका * सेक्सन_प्रविष्टि_साइज;
            int 종류 = पदच्छेद_गर्नुहोस्_पूर्ण_सङ्ख्या(लगत, स्थिति + 4);
            int झन्डा_मान = पदच्छेद_गर्नुहोस्_पूर्ण_सङ्ख्या(लगत, स्थिति + 8);
            int ठेगाना = पदच्छेद_गर्नुहोस्_पूर्ण_सङ्ख्या(लगत, स्थिति + 12);
            int फाइल_राख्नुहोस् = पदच्छेद_गर्नुहोस्_पूर्ण_सङ्ख्या(लगत, स्थिति + 16);
            int आकार = पदच्छेद_गर्नुहोस्_पूर्ण_सङ्ख्या(लगत, स्थिति + 20);
            if (आकार < 0 || (종류 != 8 && ((long) फाइल_राख्नुहोस् + आकार > लगत.length || फाइल_राख्नुहोस् < 0))) {
                throw new IllegalArgumentException("ELF सेक्सन_मान लगत 범위가 올바르지 않습니다.");
            }
            구역들.add(new सेक्सन_मान(종류, झन्डा_मान, ठेगाना, फाइल_राख्नुहोस्, आकार));
        }
        return new छवि(सुरु_ठेगाना, 구역들);
    }

    private int पदच्छेद_गर्नुहोस्_पूर्ण_सङ्ख्या(byte[] लगत, int स्थिति) {
        if (स्थिति < 0 || स्थिति > लगत.length - 4) {
            throw new IllegalArgumentException("ELF पूर्ण_सङ्ख्या 범위를 벗어났습니다.");
        }
        return (लगत[स्थिति] & 0xff)
                | ((लगत[स्थिति + 1] & 0xff) << 8)
                | ((लगत[स्थिति + 2] & 0xff) << 16)
                | ((लगत[स्थिति + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] लगत, int स्थिति) {
        if (स्थिति < 0 || स्थिति > लगत.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 पूर्ण_सङ्ख्या 범위를 벗어났습니다.");
        }
        return (लगत[स्थिति] & 0xff) | ((लगत[स्थिति + 1] & 0xff) << 8);
    }
}
