// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** ଏଣ୍ଟ୍ରି_ତାଲିକା(目錄): 순서가 있는 항목의 모음. 이 판은 ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ 목록을 제공한다. */
public final class ଏଣ୍ଟ୍ରି_ତାଲିକା {
    private final ArrayList<String> ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ = new ArrayList<String>();
    public void 더하기(String ମୂଲ୍ୟ) { ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.add(ମୂଲ୍ୟ); }
    public String ପଢନ୍ତୁ(int କ୍ରମ_ମୂଲ୍ୟ) { return ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.get(କ୍ରମ_ମୂଲ୍ୟ); }
    public String ପ୍ରତିସ୍ଥାପନ_ମୂଲ୍ୟ(int କ୍ରମ_ମୂଲ୍ୟ, String ମୂଲ୍ୟ) { return ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.set(କ୍ରମ_ମୂଲ୍ୟ, ମୂଲ୍ୟ); }
    public String 지우기(int କ୍ରମ_ମୂଲ୍ୟ) { return ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.remove(କ୍ରମ_ମୂଲ୍ୟ); }
    public int ଆକାର() { return ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.size(); }
    public boolean ସୂଚନା_ପ୍ରଯୁକ୍ତିବିଦ୍ୟା_ଖାଲି_ମୂଲ୍ୟ() { return ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.isEmpty(); }
    public void ଖାଲି_କରନ୍ତୁ_ସୂଚୀ_ସମୂହ() { ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.clear(); }
}
