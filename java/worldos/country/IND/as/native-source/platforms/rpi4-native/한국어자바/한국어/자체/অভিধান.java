// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** অভিধান(辭典): 찾는 말(열쇠)에 값을 대응시킨다. */
public final class অভিধান {
    private final HashMap<String, String> প্রবিষ্ট_মান = new HashMap<String, String>();
    public String 넣기(String 열쇠, String মান) { return প্রবিষ্ট_মান.put(열쇠, মান); }
    public String বিচাৰক_প্রবিষ্ট(String 열쇠) { return প্রবিষ্ট_মান.get(열쇠); }
    public boolean 있는가(String 열쇠) { return প্রবিষ্ট_মান.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return প্রবিষ্ট_মান.remove(열쇠); }
    public int মাপ() { return প্রবিষ্ট_মান.size(); }
    public void পৰিষ্কাৰ_কৰক_সামগ্ৰী() { প্রবিষ্ট_মান.clear(); }
}
