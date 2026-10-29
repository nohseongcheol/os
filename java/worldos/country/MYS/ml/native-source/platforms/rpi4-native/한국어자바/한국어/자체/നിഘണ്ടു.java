// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** നിഘണ്ടു(辭典): 찾는 വാക്ക്_ലിഖിതം(열쇠)에 값을 대응시킨다. */
public final class നിഘണ്ടു {
    private final HashMap<String, String> എന്_ട്രി_മൂല്യം = new HashMap<String, String>();
    public String 넣기(String 열쇠, String മൂല്യം) { return എന്_ട്രി_മൂല്യം.put(열쇠, മൂല്യം); }
    public String കണ്ടെത്തുക_എന്_ട്രി(String 열쇠) { return എന്_ട്രി_മൂല്യം.get(열쇠); }
    public boolean 있는가(String 열쇠) { return എന്_ട്രി_മൂല്യം.containsKey(열쇠); }
    public String മായ്ക്കുക_എന്_ട്രി(String 열쇠) { return എന്_ട്രി_മൂല്യം.remove(열쇠); }
    public int വലിപ്പം() { return എന്_ട്രി_മൂല്യം.size(); }
    public void മായ്ക്കുക_ഉള്ളടക്കങ്ങള്() { എന്_ട്രി_മൂല്യം.clear(); }
}
