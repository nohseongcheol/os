// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本.JJpnOS.システム呼出;

public final class システム詳細一覧 {
    private final String システム名前;
    private final String 節点名前;
    private final String 言語版値;
    private final String 版値;
    private final String 機械;

    public システム詳細一覧(String システム名前, String 節点名前, String 言語版値, String 版値, String 機械) {
        this.システム名前 = システム名前;
        this.節点名前 = 節点名前;
        this.言語版値 = 言語版値;
        this.版値 = 版値;
        this.機械 = 機械;
    }

    public String システム名前() { return システム名前; }
    public String 節点名前() { return 節点名前; }
    public String 言語版値() { return 言語版値; }
    public String 版値() { return 版値; }
    public String 機械() { return 機械; }
}
