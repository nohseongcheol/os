// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಕನ್ನಡ.자체;
import java.util.HashMap;
/** ನಿಘಂಟು(辭典): 찾는 ಪದ_ಪಠ್ಯ(열쇠)에 값을 대응시킨다. */
public final class ನಿಘಂಟು {
    private final HashMap<String, String> ನಮೂದು_ಮೌಲ್ಯ = new HashMap<String, String>();
    public String 넣기(String 열쇠, String ಮೌಲ್ಯ) { return ನಮೂದು_ಮೌಲ್ಯ.put(열쇠, ಮೌಲ್ಯ); }
    public String ಹುಡುಕಿ_ನಮೂದು(String 열쇠) { return ನಮೂದು_ಮೌಲ್ಯ.get(열쇠); }
    public boolean 있는가(String 열쇠) { return ನಮೂದು_ಮೌಲ್ಯ.containsKey(열쇠); }
    public String ಅಳಿಸು_ನಮೂದು(String 열쇠) { return ನಮೂದು_ಮೌಲ್ಯ.remove(열쇠); }
    public int ಗಾತ್ರ() { return ನಮೂದು_ಮೌಲ್ಯ.size(); }
    public void ತೆರವುಗೊಳಿಸು_ವಿಷಯಗಳು() { ನಮೂದು_ಮೌಲ್ಯ.clear(); }
}
