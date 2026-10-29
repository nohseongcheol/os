// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Đọc thăm dò tập mã dịch 1 của PC/AT PS/2; hỗ trợ bố trí bàn phím Mỹ cơ bản, Shift, Backspace và Enter. */
public final class BànPhím {
    static boolean tráiDịch = false;
    static boolean phảiDịch = false;
    static boolean giáTrịPhầnMởRộng = false;
    static String giáTrịMặcĐịnh = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String giáTrịDịch = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int đọc() {
        int giáTrịTrạngThái = ThiếtBị.đọcByteVàoRa(0x64);
        if ((giáTrịTrạngThái & 1) == 0) return -1;
        int giáTrị = ThiếtBị.đọcByteVàoRa(0x60);
        if ((giáTrịTrạngThái & 0x20) != 0) return -1;
        if (giáTrị == 0xe0 || giáTrị == 0xe1) { giáTrịPhầnMởRộng = true; return -1; }
        if (giáTrịPhầnMởRộng) { giáTrịPhầnMởRộng = false; return -1; }
        if (giáTrị == 42 || giáTrị == 170) { tráiDịch = giáTrị == 42; return -1; }
        if (giáTrị == 54 || giáTrị == 182) { phảiDịch = giáTrị == 54; return -1; }
        if (giáTrị >= giáTrịMặcĐịnh.length()) return -1;
        int KýTự = (tráiDịch || phảiDịch) ? giáTrịDịch.charAt(giáTrị) : giáTrịMặcĐịnh.charAt(giáTrị);
        return KýTự == 0 ? -1 : KýTự;
    }
}
