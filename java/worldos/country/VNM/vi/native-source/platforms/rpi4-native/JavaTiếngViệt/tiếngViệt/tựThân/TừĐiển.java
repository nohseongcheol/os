// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;
import java.util.HashMap;
/** Ánh xạ khóa tra cứu tới giá trị. */
public final class TừĐiển {
    private final HashMap<String, String> giáTrịMục = new HashMap<String, String>();
    public String đặtGiáTrị(String vậtLiệuPhím, String giáTrị) { return giáTrịMục.put(vậtLiệuPhím, giáTrị); }
    public String tìmMục(String vậtLiệuPhím) { return giáTrịMục.get(vậtLiệuPhím); }
    public boolean thựcHiệnĐượcTồnTại(String vậtLiệuPhím) { return giáTrịMục.containsKey(vậtLiệuPhím); }
    public String xóaMục(String vậtLiệuPhím) { return giáTrịMục.remove(vậtLiệuPhím); }
    public int cỡ() { return giáTrịMục.size(); }
    public void xóaSạchCácNộiDung() { giáTrịMục.clear(); }
}
