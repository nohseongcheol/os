// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package እስራኤል.JIsrOS.체계호출;

public final class 체계정보 {
    private final String ስርዓት_ስም;
    private final String ዓፅቅ_ስም;
    private final String 배포판;
    private final String ስሪት_እሴት;
    private final String ማሽን;

    public 체계정보(String ስርዓት_ስም, String ዓፅቅ_ስም, String 배포판, String ስሪት_እሴት, String ማሽን) {
        this.ስርዓት_ስም = ስርዓት_ስም;
        this.ዓፅቅ_ስም = ዓፅቅ_ስም;
        this.배포판 = 배포판;
        this.ስሪት_እሴት = ስሪት_እሴት;
        this.ማሽን = ማሽን;
    }

    public String ስርዓት_ስም() { return ስርዓት_ስም; }
    public String ዓፅቅ_ስም() { return ዓፅቅ_ስም; }
    public String 배포판() { return 배포판; }
    public String ስሪት_እሴት() { return ስሪት_እሴት; }
    public String ማሽን() { return ማሽን; }
}
