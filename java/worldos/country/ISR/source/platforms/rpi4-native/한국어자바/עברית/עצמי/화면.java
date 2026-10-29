// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package עברית.עצמי;
/** 화면(畫面): 부팅 때 선택한 크기의 עצמי ליבה_ערך RGB32 프레임버퍼. */
public final class 화면 {
    private 화면() {}
    public static int 너비() { int ערך = ליבה_ערך.화면너비(); if (ערך < 0) throw new מצב_חריגה("프레임버퍼 없음"); return ערך; }
    public static int גובה_ערך() { int ערך = ליבה_ערך.화면높이(); if (ערך < 0) throw new מצב_חריגה("프레임버퍼 없음"); return ערך; }
    public static void מלבן(int 가로, int אנכי_עמדה, int 폭, int גובה_ערך, int 색) {
        if (가로 < 0 || אנכי_עמדה < 0 || 폭 < 0 || גובה_ערך < 0 || 가로 > 너비() || אנכי_עמדה > גובה_ערך() || 폭 > 너비() - 가로 || גובה_ערך > גובה_ערך() - אנכי_עמדה) throw new לא_חוקי_ארגומנט_חריגה("화면 לגזור");
        if (ליבה_ערך.מלבן(가로, אנכי_עמדה, 폭, גובה_ערך, 색) < 0) throw new מצב_חריגה("프레임버퍼 없음");
    }
    public static void מחק_ערך(int 색) { מלבן(0, 0, 너비(), גובה_ערך(), 색); }
    public static void 기다리기() { if (ליבה_ערך.그림대기() < 0) throw new מצב_חריגה("אינטראקטיבי קלט_ערך 필요"); }
}
