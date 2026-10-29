// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 한국어 화면 구성요소를 만드는 편의 കാര്യപ്രവര്_ത്തനം_മൂല്യം. */
public final class വിജറ്റ് {
    private വിജറ്റ്() {}
    public static void 나중에실행(실행할일 ചുമതല_ക്രിയ) { ഇവന്റ്_ക്യൂ.나중에실행(ചുമതല_ക്രിയ); }
    public static ലേബല് ടാഗ്_മൂല്യം(String പദാവലി, int 가로, int ലംബം_പദവി, int 폭, int 높이) {
        return new ലേബല്(പദാവലി, 가로, ലംബം_പദവി, 폭, 높이);
    }
    public static ബട്ടണ് ബട്ടണ്(String പദാവലി, int 가로, int ലംബം_പദവി, int 폭, int 높이, 동작받이 받이) {
        return new ബട്ടണ്(പദാവലി, 가로, ലംബം_പദവി, 폭, 높이, 받이);
    }
    public static പാഠ_മണ്ഡലം പാഠ_മണ്ഡലം(String പദാവലി, int 가로, int ലംബം_പദവി, int 폭, int 높이) {
        return new പാഠ_മണ്ഡലം(പദാവലി, 가로, ലംബം_പദവി, 폭, 높이);
    }
}
