// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package فارسی.بومی;
/** فارسی 화면 구성요소를 만드는 편의 عملکرد_مقدار. */
public final class ویجت {
    private ویجت() {}
    public static void 나중에실행(실행할일 کار_عمل) { رویداد_صف.나중에실행(کار_عمل); }
    public static برچسب برچسب_مقدار(String متن, int 가로, int عمودی_مرتب_کردن, int 폭, int 높이) {
        return new برچسب(متن, 가로, عمودی_مرتب_کردن, 폭, 높이);
    }
    public static دکمه دکمه(String متن, int 가로, int عمودی_مرتب_کردن, int 폭, int 높이, 동작받이 받이) {
        return new دکمه(متن, 가로, عمودی_مرتب_کردن, 폭, 높이, 받이);
    }
    public static متن_فیلد متن_فیلد(String متن, int 가로, int عمودی_مرتب_کردن, int 폭, int 높이) {
        return new متن_فیلد(متن, 가로, عمودی_مرتب_کردن, 폭, 높이);
    }
}
