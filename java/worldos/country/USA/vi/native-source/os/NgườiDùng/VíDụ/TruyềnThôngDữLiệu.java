// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class TruyềnThôngDữLiệu {
    static int giáTrịChữSố(String vănBản) {
        if (vănBản == null || vănBản.length() == 0) return -1;
        int kếtQuả = 0;
        for (int sốHiệu = 0; sốHiệu < vănBản.length(); sốHiệu++) {
            int giáTrị = vănBản.charAt(sốHiệu) - '0';
            if (giáTrị < 0 || giáTrị > 9 || kếtQuả > 6553) return -1;
            kếtQuả = kếtQuả * 10 + giáTrị;
            if (kếtQuả > 65535) return -1;
        }
        return kếtQuả;
    }
    static int địaChỉ(String vănBản) {
        if (vănBản == null) return 0;
        int giáTrị = 0, kếtQuả = 0, giáTrịPhầnCon = 0, cácChữSố = 0;
        for (int sốHiệu = 0; sốHiệu <= vănBản.length(); sốHiệu++) {
            int KýTự = sốHiệu == vănBản.length() ? '.' : vănBản.charAt(sốHiệu);
            if (KýTự == '.') {
                if (cácChữSố == 0 || giáTrịPhầnCon == 4) return 0;
                kếtQuả = (kếtQuả << 8) | giáTrị; giáTrịPhầnCon++; giáTrị = 0; cácChữSố = 0;
            } else {
                if (KýTự < '0' || KýTự > '9') return 0;
                giáTrị = giáTrị * 10 + KýTự - '0';
                if (++cácChữSố > 3 || giáTrị > 255) return 0;
            }
        }
        return giáTrịPhầnCon == 4 ? kếtQuả : 0;
    }
    public static int chạy() {
        if (NgườiDùng.sốLượngCácĐốiSố() != 3) { NgườiDùng.ghi("Usage: run udp IP PORT TEXT\n"); return 2; }
        int địaChỉ = địaChỉ(NgườiDùng.cácĐốiSố(0)), giáTrịCổng = giáTrịChữSố(NgườiDùng.cácĐốiSố(1));
        String giáTrịNộiDung = NgườiDùng.cácĐốiSố(2);
        if (địaChỉ == 0 || giáTrịCổng < 1 || giáTrịNộiDung.length() > 1024) { NgườiDùng.ghi("Bad destination\n"); return 2; }
        int giáTrịThẻXửLý = NgườiDùng.mởMạng(0);
        if (giáTrịThẻXửLý < 0) { NgườiDùng.ghi("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] DữLiệu = new int[1024];
        for (int sốHiệu = 0; sốHiệu < giáTrịNộiDung.length(); sốHiệu++) DữLiệu[sốHiệu] = giáTrịNộiDung.charAt(sốHiệu);
        if (NgườiDùng.gửiDữLiệu(giáTrịThẻXửLý, địaChỉ, giáTrịCổng, DữLiệu, giáTrịNộiDung.length()) < 0) {
            NgườiDùng.ghi("UDP SEND FAILED\n"); NgườiDùng.đóngMạng(giáTrịThẻXửLý); return 4;
        }
        NgườiDùng.ghi("UDP SENT\n");
        int độDàiĐãNhận = NgườiDùng.nhậnDữLiệu(giáTrịThẻXửLý, DữLiệu, 1500);
        boolean vănBảnBằng = độDàiĐãNhận == giáTrịNộiDung.length() && NgườiDùng.địaChỉĐãGửi(giáTrịThẻXửLý) == địaChỉ && NgườiDùng.cổngĐãGửi(giáTrịThẻXửLý) == giáTrịCổng;
        if (vănBảnBằng) for (int sốHiệu = 0; sốHiệu < độDàiĐãNhận; sốHiệu++) if (DữLiệu[sốHiệu] != giáTrịNộiDung.charAt(sốHiệu)) vănBảnBằng = false;
        NgườiDùng.đóngMạng(giáTrịThẻXửLý);
        if (độDàiĐãNhận < 0) { NgườiDùng.ghi("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        NgườiDùng.ghi(vănBảnBằng ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return vănBảnBằng ? 0 : 6;
    }
}
