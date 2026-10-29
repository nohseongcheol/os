// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಕನ್ನಡ.자체;
import java.util.ArrayList;
/** ನಮೂದು_ಪಟ್ಟಿ(目錄): 순서가 있는 항목의 모음. 이 판은 ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ 목록을 제공한다. */
public final class ನಮೂದು_ಪಟ್ಟಿ {
    private final ArrayList<String> ನಮೂದು_ಮೌಲ್ಯ = new ArrayList<String>();
    public void 더하기(String ಮೌಲ್ಯ) { ನಮೂದು_ಮೌಲ್ಯ.add(ಮೌಲ್ಯ); }
    public String ಓದು(int ಕ್ರಮ_ಮೌಲ್ಯ) { return ನಮೂದು_ಮೌಲ್ಯ.get(ಕ್ರಮ_ಮೌಲ್ಯ); }
    public String ಬದಲಾಯಿಸು_ಮೌಲ್ಯ(int ಕ್ರಮ_ಮೌಲ್ಯ, String ಮೌಲ್ಯ) { return ನಮೂದು_ಮೌಲ್ಯ.set(ಕ್ರಮ_ಮೌಲ್ಯ, ಮೌಲ್ಯ); }
    public String ಅಳಿಸು_ನಮೂದು(int ಕ್ರಮ_ಮೌಲ್ಯ) { return ನಮೂದು_ಮೌಲ್ಯ.remove(ಕ್ರಮ_ಮೌಲ್ಯ); }
    public int ಗಾತ್ರ() { return ನಮೂದು_ಮೌಲ್ಯ.size(); }
    public boolean ಮಾಹಿತಿ_ತಂತ್ರಜ್ಞಾನ_ಖಾಲಿ_ಮೌಲ್ಯ() { return ನಮೂದು_ಮೌಲ್ಯ.isEmpty(); }
    public void ತೆರವುಗೊಳಿಸು_ವಿಷಯಗಳು() { ನಮೂದು_ಮೌಲ್ಯ.clear(); }
}
