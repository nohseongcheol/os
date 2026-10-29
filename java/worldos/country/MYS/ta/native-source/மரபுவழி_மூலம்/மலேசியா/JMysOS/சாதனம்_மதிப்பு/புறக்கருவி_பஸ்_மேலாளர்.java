// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package மலேசியா.JMysOS.சாதனம்_மதிப்பு;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI சாதனம்_மதிப்பு 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class புறக்கருவி_பஸ்_மேலாளர் {
    public static final class சாதனம்_மதிப்பு {
        private final int 판매자식별자;
        private final int சாதனம்_அடையாளங்காட்டி;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public சாதனம்_மதிப்பு(int 판매자식별자, int சாதனம்_அடையாளங்காட்டி, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.சாதனம்_அடையாளங்காட்டி = சாதனம்_அடையாளங்காட்டி;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int சாதனம்_அடையாளங்காட்டி() { return சாதனம்_அடையாளங்காட்டி; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<சாதனம்_மதிப்பு> சாதனங்கள்_பட்டியல் = new ArrayList<சாதனம்_மதிப்பு>();

    public void 발견(சாதனம்_மதிப்பு சாதனம்_மதிப்பு) {
        சாதனங்கள்_பட்டியல்.add(சாதனம்_மதிப்பு);
    }

    public List<சாதனம்_மதிப்பு> சாதனங்கள்_பட்டியல்() {
        return Collections.unmodifiableList(சாதனங்கள்_பட்டியல்);
    }

    public சாதனம்_மதிப்பு கண்டறி_உள்ளீடு(int 판매자식별자, int சாதனம்_அடையாளங்காட்டி) {
        for (சாதனம்_மதிப்பு 후보 : சாதனங்கள்_பட்டியல்) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.சாதனம்_அடையாளங்காட்டி == சாதனம்_அடையாளங்காட்டி) {
                return 후보;
            }
        }
        return null;
    }
}

