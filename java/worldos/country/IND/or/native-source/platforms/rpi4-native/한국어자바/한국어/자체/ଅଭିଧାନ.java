// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** ଅଭିଧାନ(辭典): 찾는 말(열쇠)에 값을 대응시킨다. */
public final class ଅଭିଧାନ {
    private final HashMap<String, String> ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ = new HashMap<String, String>();
    public String 넣기(String 열쇠, String ମୂଲ୍ୟ) { return ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.put(열쇠, ମୂଲ୍ୟ); }
    public String ଖୋଜିବା_ଏଣ୍ଟ୍ରି(String 열쇠) { return ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.get(열쇠); }
    public boolean 있는가(String 열쇠) { return ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.remove(열쇠); }
    public int ଆକାର() { return ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.size(); }
    public void ଖାଲି_କରନ୍ତୁ_ସୂଚୀ_ସମୂହ() { ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.clear(); }
}
