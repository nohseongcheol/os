// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package עברית.עצמי;
/** עברית 화면 구성요소를 만드는 편의 פונקציה_ערך. */
public final class רכיב_גרפי {
    private רכיב_גרפי() {}
    public static void 나중에실행(실행할일 משימה_המלצה) { אירוע_תור.나중에실행(משימה_המלצה); }
    public static תווית תג_ערך(String טקסט, int 가로, int אנכי_עמדה, int 폭, int גובה_ערך) {
        return new תווית(טקסט, 가로, אנכי_עמדה, 폭, גובה_ערך);
    }
    public static לחצן לחצן(String טקסט, int 가로, int אנכי_עמדה, int 폭, int גובה_ערך, 동작받이 받이) {
        return new לחצן(טקסט, 가로, אנכי_עמדה, 폭, גובה_ערך, 받이);
    }
    public static שדה_טקסט שדה_טקסט(String טקסט, int 가로, int אנכי_עמדה, int 폭, int גובה_ערך) {
        return new שדה_טקסט(טקסט, 가로, אנכי_עמדה, 폭, גובה_ערך);
    }
}
