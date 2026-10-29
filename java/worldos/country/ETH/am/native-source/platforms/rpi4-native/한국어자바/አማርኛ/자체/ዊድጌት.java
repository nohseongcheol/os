// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package አማርኛ.자체;
/** አማርኛ 화면 구성요소를 만드는 편의 ተግባር_እሴት. */
public final class ዊድጌት {
    private ዊድጌት() {}
    public static void 나중에실행(실행할일 ተግባር_ምክር) { ፍጻሜ_ሰልፍ.나중에실행(ተግባር_ምክር); }
    public static ምልክት መለያ_እሴት(String ጽሁፍ, int 가로, int ቋሚ_በቦታ_አስቀመጠ, int 폭, int 높이) {
        return new ምልክት(ጽሁፍ, 가로, ቋሚ_በቦታ_አስቀመጠ, 폭, 높이);
    }
    public static አዝራር አዝራር(String ጽሁፍ, int 가로, int ቋሚ_በቦታ_አስቀመጠ, int 폭, int 높이, 동작받이 받이) {
        return new አዝራር(ጽሁፍ, 가로, ቋሚ_በቦታ_አስቀመጠ, 폭, 높이, 받이);
    }
    public static ጽሁፍ_መስክ ጽሁፍ_መስክ(String ጽሁፍ, int 가로, int ቋሚ_በቦታ_አስቀመጠ, int 폭, int 높이) {
        return new ጽሁፍ_መስክ(ጽሁፍ, 가로, ቋሚ_በቦታ_አስቀመጠ, 폭, 높이);
    }
}
