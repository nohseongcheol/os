// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ไทย.เอง;
import java.util.ArrayList;
/** รายการ_รายการ(目錄): 순서가 있는 항목의 모음. 이 판은 สตริง_ค่า 목록을 제공한다. */
public final class รายการ_รายการ {
    private final ArrayList<String> รายการ_ค่า = new ArrayList<String>();
    public void 더하기(String ค่า) { รายการ_ค่า.add(ค่า); }
    public String อ่าน(int ลําดับ_ค่า) { return รายการ_ค่า.get(ลําดับ_ค่า); }
    public String 바꾸기(int ลําดับ_ค่า, String ค่า) { return รายการ_ค่า.set(ลําดับ_ค่า, ค่า); }
    public String ลบ_รายการ(int ลําดับ_ค่า) { return รายการ_ค่า.remove(ลําดับ_ค่า); }
    public int ขนาด() { return รายการ_ค่า.size(); }
    public boolean 비었는가() { return รายการ_ค่า.isEmpty(); }
    public void ล้าง_สารบัญ() { รายการ_ค่า.clear(); }
}
