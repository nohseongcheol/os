// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** វចនានុក្រម(辭典): 찾는 ពាក្យ_អត្ថបទ(열쇠)에 값을 대응시킨다. */
public final class វចនានុក្រម {
    private final HashMap<String, String> ការបញ្ចូល_តំលៃ = new HashMap<String, String>();
    public String 넣기(String 열쇠, String តំលៃ) { return ការបញ្ចូល_តំលៃ.put(열쇠, តំលៃ); }
    public String រក_ការបញ្ចូល(String 열쇠) { return ការបញ្ចូល_តំលៃ.get(열쇠); }
    public boolean 있는가(String 열쇠) { return ការបញ្ចូល_តំលៃ.containsKey(열쇠); }
    public String លុប_ការបញ្ចូល(String 열쇠) { return ការបញ្ចូល_តំលៃ.remove(열쇠); }
    public int ដាក់ទំហំ() { return ការបញ្ចូល_តំលៃ.size(); }
    public void លុប_មាតិការ() { ការបញ្ចូល_តំលៃ.clear(); }
}
