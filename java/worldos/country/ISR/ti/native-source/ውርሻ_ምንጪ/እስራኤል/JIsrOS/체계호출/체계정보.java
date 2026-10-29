// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package እስራኤል.JIsrOS.체계호출;

public final class 체계정보 {
    private final String ስርዓት_ሽም;
    private final String ጨንፈር_ሽም;
    private final String 배포판;
    private final String ሕታም_ዋጋ;
    private final String ማሽን;

    public 체계정보(String ስርዓት_ሽም, String ጨንፈር_ሽም, String 배포판, String ሕታም_ዋጋ, String ማሽን) {
        this.ስርዓት_ሽም = ስርዓት_ሽም;
        this.ጨንፈር_ሽም = ጨንፈር_ሽም;
        this.배포판 = 배포판;
        this.ሕታም_ዋጋ = ሕታም_ዋጋ;
        this.ማሽን = ማሽን;
    }

    public String ስርዓት_ሽም() { return ስርዓት_ሽም; }
    public String ጨንፈር_ሽም() { return ጨንፈር_ሽም; }
    public String 배포판() { return 배포판; }
    public String ሕታም_ዋጋ() { return ሕታም_ዋጋ; }
    public String ማሽን() { return ማሽን; }
}
