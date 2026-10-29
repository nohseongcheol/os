// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Trung_Quốc.JChnOS.LờiGọiHệThống;

public final class cácChiTiếtHệThống {
    private final String tênHệThống;
    private final String tênNútCây;
    private final String giáTrịPhiênBảnNgônNgữ;
    private final String giáTrịPhiênBản;
    private final String máy;

    public cácChiTiếtHệThống(String tênHệThống, String tênNútCây, String giáTrịPhiênBảnNgônNgữ, String giáTrịPhiênBản, String máy) {
        this.tênHệThống = tênHệThống;
        this.tênNútCây = tênNútCây;
        this.giáTrịPhiênBảnNgônNgữ = giáTrịPhiênBảnNgônNgữ;
        this.giáTrịPhiênBản = giáTrịPhiênBản;
        this.máy = máy;
    }

    public String tênHệThống() { return tênHệThống; }
    public String tênNútCây() { return tênNútCây; }
    public String giáTrịPhiênBảnNgônNgữ() { return giáTrịPhiênBảnNgônNgữ; }
    public String giáTrịPhiênBản() { return giáTrịPhiênBản; }
    public String máy() { return máy; }
}
