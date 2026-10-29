// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** എന്_ട്രി_ലിസ്റ്റ്(目錄): 순서가 있는 항목의 모음. 이 판은 സ്ട്രിംഗ്_മൂല്യം 목록을 제공한다. */
public final class എന്_ട്രി_ലിസ്റ്റ് {
    private final ArrayList<String> എന്_ട്രി_മൂല്യം = new ArrayList<String>();
    public void 더하기(String മൂല്യം) { എന്_ട്രി_മൂല്യം.add(മൂല്യം); }
    public String വായന(int ക്രമം_മൂല്യം) { return എന്_ട്രി_മൂല്യം.get(ക്രമം_മൂല്യം); }
    public String പകരംവയ്ക്കുക_മൂല്യം(int ക്രമം_മൂല്യം, String മൂല്യം) { return എന്_ട്രി_മൂല്യം.set(ക്രമം_മൂല്യം, മൂല്യം); }
    public String മായ്ക്കുക_എന്_ട്രി(int ക്രമം_മൂല്യം) { return എന്_ട്രി_മൂല്യം.remove(ക്രമം_മൂല്യം); }
    public int വലിപ്പം() { return എന്_ട്രി_മൂല്യം.size(); }
    public boolean വിവര_സാങ്കേതികവിദ്യ_ശൂന്യം_മൂല്യം() { return എന്_ട്രി_മൂല്യം.isEmpty(); }
    public void മായ്ക്കുക_ഉള്ളടക്കങ്ങള്() { എന്_ട്രി_മൂല്യം.clear(); }
}
