// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** ເຂົ້າໃນ_ລາຍຊື່(目錄): 순서가 있는 항목의 모음. 이 판은 ສະຕຣິງ_ຄ່າ 목록을 제공한다. */
public final class ເຂົ້າໃນ_ລາຍຊື່ {
    private final ArrayList<String> ເຂົ້າໃນ_ຄ່າ = new ArrayList<String>();
    public void 더하기(String ຄ່າ) { ເຂົ້າໃນ_ຄ່າ.add(ຄ່າ); }
    public String 읽기(int ລໍາດັບ_ຄ່າ) { return ເຂົ້າໃນ_ຄ່າ.get(ລໍາດັບ_ຄ່າ); }
    public String 바꾸기(int ລໍາດັບ_ຄ່າ, String ຄ່າ) { return ເຂົ້າໃນ_ຄ່າ.set(ລໍາດັບ_ຄ່າ, ຄ່າ); }
    public String ລຶບ_ເຂົ້າໃນ(int ລໍາດັບ_ຄ່າ) { return ເຂົ້າໃນ_ຄ່າ.remove(ລໍາດັບ_ຄ່າ); }
    public int ຂະ_ຫນາດ() { return ເຂົ້າໃນ_ຄ່າ.size(); }
    public boolean ເທັກໂນໂລຢີຂໍ້ມູນຂ່າວສານ_ຫວ່າງ_ເປົ່າ_ຄ່າ() { return ເຂົ້າໃນ_ຄ່າ.isEmpty(); }
    public void ລ້າງ_ສາລະບານ() { ເຂົ້າໃນ_ຄ່າ.clear(); }
}
