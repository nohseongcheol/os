// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package កម្ពុជា.JKhmOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 ភាព_តំលៃ ផ្នែក_តំលៃ 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int គំរូដែសថប_តំលៃ;
        private final int 한계;
        private final int ការចូលប្រើ_តំលៃ;

        조각(int គំរូដែសថប_តំលៃ, int 한계, int ការចូលប្រើ_តំលៃ) {
            this.គំរូដែសថប_តំលៃ = គំរូដែសថប_តំលៃ;
            this.한계 = 한계;
            this.ការចូលប្រើ_តំលៃ = ការចូលប្រើ_តំលៃ;
        }

        public int គំរូដែសថប_តំលៃ() { return គំរូដែសថប_តំលៃ; }
        public int 한계() { return 한계; }
        public int ការចូលប្រើ_តំលៃ() { return ការចូលប្រើ_តំលៃ; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int គំរូដែសថប_តំលៃ, int 한계, int ការចូលប្រើ_តំលៃ) {
        조각들.add(new 조각(គំរូដែសថប_តំលៃ, 한계, ការចូលប្រើ_តំលៃ));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void កំណត់_តំលៃស្វ័យប្រវត្តិ() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

