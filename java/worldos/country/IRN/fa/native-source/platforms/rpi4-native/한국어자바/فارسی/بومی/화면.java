// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package فارسی.بومی;
/** 화면(畫面): 부팅 때 선택한 크기의 بومی هسته_مقدار RGB32 프레임버퍼. */
public final class 화면 {
    private 화면() {}
    public static int 너비() { int مقدار = هسته_مقدار.화면너비(); if (مقدار < 0) throw new وضعیت_استثنا("프레임버퍼 없음"); return مقدار; }
    public static int 높이() { int مقدار = هسته_مقدار.화면높이(); if (مقدار < 0) throw new وضعیت_استثنا("프레임버퍼 없음"); return مقدار; }
    public static void 사각형(int 가로, int عمودی_مرتب_کردن, int 폭, int 높이, int 색) {
        if (가로 < 0 || عمودی_مرتب_کردن < 0 || 폭 < 0 || 높이 < 0 || 가로 > 너비() || عمودی_مرتب_کردن > 높이() || 폭 > 너비() - 가로 || 높이 > 높이() - عمودی_مرتب_کردن) throw new بی_اعتبار_آرگومان_استثنا("화면 کلیپ");
        if (هسته_مقدار.사각형(가로, عمودی_مرتب_کردن, 폭, 높이, 색) < 0) throw new وضعیت_استثنا("프레임버퍼 없음");
    }
    public static void پاک_کردن_ورودی(int 색) { 사각형(0, 0, 너비(), 높이(), 색); }
    public static void 기다리기() { if (هسته_مقدار.그림대기() < 0) throw new وضعیت_استثنا("محاوره_ای 입력 필요"); }
}
