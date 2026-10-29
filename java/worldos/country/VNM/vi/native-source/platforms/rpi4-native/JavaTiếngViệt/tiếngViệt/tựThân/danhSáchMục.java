// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;
import java.util.ArrayList;
/** Tập hợp các phần tử có thứ tự. Bản này cung cấp danh sách chuỗi. */
public final class danhSáchMục {
    private final ArrayList<String> giáTrịMục = new ArrayList<String>();
    public void thêmCácGiáTrị(String giáTrị) { giáTrịMục.add(giáTrị); }
    public String đọc(int giáTrịThứTự) { return giáTrịMục.get(giáTrịThứTự); }
    public String thayGiáTrị(int giáTrịThứTự, String giáTrị) { return giáTrịMục.set(giáTrịThứTự, giáTrị); }
    public String xóaMục(int giáTrịThứTự) { return giáTrịMục.remove(giáTrịThứTự); }
    public int cỡ() { return giáTrịMục.size(); }
    public boolean làGiáTrịRỗng() { return giáTrịMục.isEmpty(); }
    public void xóaSạchCácNộiDung() { giáTrịMục.clear(); }
}
