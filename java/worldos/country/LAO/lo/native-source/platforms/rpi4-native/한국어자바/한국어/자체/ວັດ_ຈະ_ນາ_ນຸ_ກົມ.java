// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** ວັດ_ຈະ_ນາ_ນຸ_ກົມ(辭典): 찾는 ຄໍາ_ເວົ້າ_ຂໍ້ຄວາມ(열쇠)에 값을 대응시킨다. */
public final class ວັດ_ຈະ_ນາ_ນຸ_ກົມ {
    private final HashMap<String, String> ເຂົ້າໃນ_ຄ່າ = new HashMap<String, String>();
    public String 넣기(String 열쇠, String ຄ່າ) { return ເຂົ້າໃນ_ຄ່າ.put(열쇠, ຄ່າ); }
    public String ຊອກຫາ_ເຂົ້າໃນ(String 열쇠) { return ເຂົ້າໃນ_ຄ່າ.get(열쇠); }
    public boolean 있는가(String 열쇠) { return ເຂົ້າໃນ_ຄ່າ.containsKey(열쇠); }
    public String ລຶບ_ເຂົ້າໃນ(String 열쇠) { return ເຂົ້າໃນ_ຄ່າ.remove(열쇠); }
    public int ຂະ_ຫນາດ() { return ເຂົ້າໃນ_ຄ່າ.size(); }
    public void ລ້າງ_ສາລະບານ() { ເຂົ້າໃນ_ຄ່າ.clear(); }
}
