// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package العربية.ذاتي;
/** العربية 화면 구성요소를 만드는 편의 دالة_قيمة. */
public final class عنصر_شاشة {
    private عنصر_شاشة() {}
    public static void 나중에실행(실행할일 مهمة_إجراء) { حدث_يدرج.나중에실행(مهمة_إجراء); }
    public static تسمية علامة_قيمة(String نص, int 가로, int عمودي_منصب, int 폭, int ارتفاع_قيمة) {
        return new تسمية(نص, 가로, عمودي_منصب, 폭, ارتفاع_قيمة);
    }
    public static زر زر(String نص, int 가로, int عمودي_منصب, int 폭, int ارتفاع_قيمة, 동작받이 받이) {
        return new زر(نص, 가로, عمودي_منصب, 폭, ارتفاع_قيمة, 받이);
    }
    public static حقل_نصي حقل_نصي(String نص, int 가로, int عمودي_منصب, int 폭, int ارتفاع_قيمة) {
        return new حقل_نصي(نص, 가로, عمودي_منصب, 폭, ارتفاع_قيمة);
    }
}
