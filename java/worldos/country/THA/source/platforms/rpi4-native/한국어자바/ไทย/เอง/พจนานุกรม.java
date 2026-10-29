// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ไทย.เอง;
import java.util.HashMap;
/** พจนานุกรม(辭典): 찾는 คํา_ข้อความ(열쇠)에 값을 대응시킨다. */
public final class พจนานุกรม {
    private final HashMap<String, String> รายการ_ค่า = new HashMap<String, String>();
    public String 넣기(String 열쇠, String ค่า) { return รายการ_ค่า.put(열쇠, ค่า); }
    public String ค้นพบ_รายการ(String 열쇠) { return รายการ_ค่า.get(열쇠); }
    public boolean 있는가(String 열쇠) { return รายการ_ค่า.containsKey(열쇠); }
    public String ลบ_รายการ(String 열쇠) { return รายการ_ค่า.remove(열쇠); }
    public int ขนาด() { return รายการ_ค่า.size(); }
    public void ล้าง_สารบัญ() { รายการ_ค่า.clear(); }
}
