// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.फायल_प्रणाली;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian पाळो_दिवचो_आदेश 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class विभाग_मोल {
        private final int 종류;
        private final int कुरवो_मोल;
        private final int नामो;
        private final int फायल_स्थिती_2aa21a9a;
        private final int आवाठ;

        विभाग_मोल(int 종류, int कुरवो_मोल, int नामो, int फायल_स्थिती_2aa21a9a, int आवाठ) {
            this.종류 = 종류;
            this.कुरवो_मोल = कुरवो_मोल;
            this.नामो = नामो;
            this.फायल_स्थिती_2aa21a9a = फायल_स्थिती_2aa21a9a;
            this.आवाठ = आवाठ;
        }

        public int 종류() {
            return 종류;
        }

        public int कुरवो_मोल() {
            return कुरवो_मोल;
        }

        public int नामो() {
            return नामो;
        }

        public int फायल_स्थिती_2aa21a9a() {
            return फायल_स्थिती_2aa21a9a;
        }

        public int आवाठ() {
            return आवाठ;
        }
    }

    public static final class IMAGE {
        private final int Start_नामो;
        private final List<विभाग_मोल> 구역들;

        IMAGE(int Start_नामो, List<विभाग_मोल> 구역들) {
            this.Start_नामो = Start_नामो;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int Start_नामो() {
            return Start_नामो;
        }

        public List<विभाग_मोल> 구역들() {
            return 구역들;
        }
    }

    public IMAGE 검사(byte[] डेटा) {
        if (डेटा == null || डेटा.length < 52
                || डेटा[0] != 0x7f || डेटा[1] != 'E' || डेटा[2] != 'L' || डेटा[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (डेटा[4] != 1 || डेटा[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int Start_नामो = व्याकरणी_फोडणिशी_पुर्णांक(डेटा, 24);
        int विभाग_तकटो_स्थिती = व्याकरणी_फोडणिशी_पुर्णांक(डेटा, 32);
        int विभाग_प्रवेश_आवाठ = 짧은정수읽기(डेटा, 46);
        int विभाग_COUNT = 짧은정수읽기(डेटा, 48);
        if (विभाग_प्रवेश_आवाठ < 40 || विभाग_तकटो_स्थिती < 0
                || (long) विभाग_तकटो_स्थिती + (long) विभाग_प्रवेश_आवाठ * विभाग_COUNT > डेटा.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<विभाग_मोल> 구역들 = new ArrayList<विभाग_मोल>();
        for (int INDEX = 0; INDEX < विभाग_COUNT; INDEX++) {
            int स्थिती = विभाग_तकटो_स्थिती + INDEX * विभाग_प्रवेश_आवाठ;
            int 종류 = व्याकरणी_फोडणिशी_पुर्णांक(डेटा, स्थिती + 4);
            int कुरवो_मोल = व्याकरणी_फोडणिशी_पुर्णांक(डेटा, स्थिती + 8);
            int नामो = व्याकरणी_फोडणिशी_पुर्णांक(डेटा, स्थिती + 12);
            int फायल_स्थिती_2aa21a9a = व्याकरणी_फोडणिशी_पुर्णांक(डेटा, स्थिती + 16);
            int आवाठ = व्याकरणी_फोडणिशी_पुर्णांक(डेटा, स्थिती + 20);
            if (आवाठ < 0 || (종류 != 8 && ((long) फायल_स्थिती_2aa21a9a + आवाठ > डेटा.length || फायल_स्थिती_2aa21a9a < 0))) {
                throw new IllegalArgumentException("ELF विभाग_मोल डेटा 범위가 올바르지 않습니다.");
            }
            구역들.add(new विभाग_मोल(종류, कुरवो_मोल, नामो, फायल_स्थिती_2aa21a9a, आवाठ));
        }
        return new IMAGE(Start_नामो, 구역들);
    }

    private int व्याकरणी_फोडणिशी_पुर्णांक(byte[] डेटा, int स्थिती) {
        if (स्थिती < 0 || स्थिती > डेटा.length - 4) {
            throw new IllegalArgumentException("ELF पुर्णांक 범위를 벗어났습니다.");
        }
        return (डेटा[स्थिती] & 0xff)
                | ((डेटा[स्थिती + 1] & 0xff) << 8)
                | ((डेटा[स्थिती + 2] & 0xff) << 16)
                | ((डेटा[स्थिती + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] डेटा, int स्थिती) {
        if (स्थिती < 0 || स्थिती > डेटा.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 पुर्णांक 범위를 벗어났습니다.");
        }
        return (डेटा[स्थिती] & 0xff) | ((डेटा[स्थिती + 1] & 0xff) << 8);
    }
}
