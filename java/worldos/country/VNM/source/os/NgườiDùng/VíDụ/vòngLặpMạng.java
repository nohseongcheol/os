// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Kiểm thử vòng đệm nhận RTL8139 thực sự quay vòng với thông điệp dài tối đa và dài lẻ. */
public final class vòngLặpMạng {
    public static int chạy() {
        if (NgườiDùng.sốLượngCácĐốiSố() != 1) { NgườiDùng.ghi("Usage: run stress PORT\n"); return 2; }
        String vănBản = NgườiDùng.cácĐốiSố(0);
        int giáTrịCổng = 0;
        for (int sốHiệu = 0; sốHiệu < vănBản.length(); sốHiệu++) {
            if (vănBản.charAt(sốHiệu) < '0' || vănBản.charAt(sốHiệu) > '9' || giáTrịCổng > 6553) return 2;
            giáTrịCổng = giáTrịCổng * 10 + vănBản.charAt(sốHiệu) - '0';
        }
        if (giáTrịCổng < 1 || giáTrịCổng > 65535) return 2;
        int giáTrịThẻXửLý = NgườiDùng.mởMạng(0);
        if (giáTrịThẻXửLý < 0) return 3;
        int[] DữLiệu = new int[1024];
        for (int thứBậcLầnLặp = 0; thứBậcLầnLặp < 24; thứBậcLầnLặp++) {
            int độDài = 1024 - (thứBậcLầnLặp & 1);
            for (int sốHiệu = 0; sốHiệu < độDài; sốHiệu++) DữLiệu[sốHiệu] = (sốHiệu + thứBậcLầnLặp) & 255;
            if (NgườiDùng.gửiDữLiệu(giáTrịThẻXửLý, 0x0a000202, giáTrịCổng, DữLiệu, độDài) != độDài) return 4;
            if (NgườiDùng.nhậnDữLiệu(giáTrịThẻXửLý, DữLiệu, 300) != độDài) return 5;
            for (int sốHiệu = 0; sốHiệu < độDài; sốHiệu++) if (DữLiệu[sốHiệu] != ((sốHiệu + thứBậcLầnLặp) & 255)) return 6;
        }
        NgườiDùng.đóngMạng(giáTrịThẻXửLý);
        NgườiDùng.ghi("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
