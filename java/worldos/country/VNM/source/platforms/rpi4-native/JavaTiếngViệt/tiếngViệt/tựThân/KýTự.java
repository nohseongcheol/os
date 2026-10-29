// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;
/** Chuyển đổi giữa byte UTF-8 và chuỗi UTF-16. Chuẩn hóa và nhập tổ hợp được xử lý riêng. */
public final class KýTự {
    public static int sốLượngByte(byte[] DữLiệu) { return DữLiệu.length; }
    private KýTự() {}
    public static int độDài(String vănBản) { return vănBản.length(); }
    public static boolean vănBảnBằng(String giáTrịPhíaTrước, String giáTrịLùi) { return giáTrịPhíaTrước == null ? giáTrịLùi == null : giáTrịPhíaTrước.equals(giáTrịLùi); }
    public static String vănBảnDán(String giáTrịPhíaTrước, String giáTrịLùi) { return giáTrịPhíaTrước.concat(giáTrịLùi); }
    public static String giáTrịCắt(String vănBản, int chạy, int phầnKết) { return vănBản.substring(chạy, phầnKết); }
    public static int phânTíchCúPhápSốNguyên(String vănBản) { try { return Integer.parseInt(vănBản); } catch (NumberFormatException lỗi) { throw new SựThấtBạiĐịnhDạngSố("Hãy kiểm tra định dạng và phạm vi của số."); } }
    public static String ghiGiáTrịSốNguyên(int trịSố) { return Integer.toString(trịSố); }
    public static int sốLượngĐiểmMã(String vănBản) {
        int trịSố = 0;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < vănBản.length(); chỉSốVòngLặp++, trịSố++) {
            int mãKýTự = vănBản.charAt(chỉSốVòngLặp);
            if (mãKýTự >= 0xd800 && mãKýTự <= 0xdbff && chỉSốVòngLặp + 1 < vănBản.length() && vănBản.charAt(chỉSốVòngLặp + 1) >= 0xdc00 && vănBản.charAt(chỉSốVòngLặp + 1) <= 0xdfff) chỉSốVòngLặp++;
        }
        return trịSố;
    }
    public static byte[] mãHóa(String vănBản) {
        byte[] giáTrịTạm = new byte[vănBản.length() * 3]; int đãGhiXong = 0;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < vănBản.length(); chỉSốVòngLặp++) {
            int mãKýTự = vănBản.charAt(chỉSốVòngLặp);
            if (mãKýTự >= 0xd800 && mãKýTự <= 0xdbff && chỉSốVòngLặp + 1 < vănBản.length() && vănBản.charAt(chỉSốVòngLặp + 1) >= 0xdc00 && vănBản.charAt(chỉSốVòngLặp + 1) <= 0xdfff) mãKýTự = 0x10000 + ((mãKýTự - 0xd800) << 10) + vănBản.charAt(++chỉSốVòngLặp) - 0xdc00;
            else if (mãKýTự >= 0xd800 && mãKýTự <= 0xdfff) mãKýTự = '?';
            if (mãKýTự < 128) giáTrịTạm[đãGhiXong++] = (byte)mãKýTự;
            else if (mãKýTự < 2048) { giáTrịTạm[đãGhiXong++] = (byte)(192 | mãKýTự >> 6); giáTrịTạm[đãGhiXong++] = (byte)(128 | mãKýTự & 63); }
            else if (mãKýTự < 65536) { giáTrịTạm[đãGhiXong++] = (byte)(224 | mãKýTự >> 12); giáTrịTạm[đãGhiXong++] = (byte)(128 | mãKýTự >> 6 & 63); giáTrịTạm[đãGhiXong++] = (byte)(128 | mãKýTự & 63); }
            else { giáTrịTạm[đãGhiXong++] = (byte)(240 | mãKýTự >> 18); giáTrịTạm[đãGhiXong++] = (byte)(128 | mãKýTự >> 12 & 63); giáTrịTạm[đãGhiXong++] = (byte)(128 | mãKýTự >> 6 & 63); giáTrịTạm[đãGhiXong++] = (byte)(128 | mãKýTự & 63); }
        }
        byte[] kếtQuả = new byte[đãGhiXong]; System.arraycopy(giáTrịTạm, 0, kếtQuả, 0, đãGhiXong); return kếtQuả;
    }
    /** Từ chối UTF-8 sai dạng bằng ngoại lệ đối số không hợp lệ của API. */
    public static String giảiMậtMãDữLiệu(byte[] giáTrịByte) {
        StringBuilder kếtQuả = new StringBuilder();
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < giáTrịByte.length;) {
            int mãKýTự = giáTrịByte[chỉSốVòngLặp++] & 255, trịSố = mãKýTự < 128 ? 0 : mãKýTự >= 194 && mãKýTự < 224 ? 1 : mãKýTự >= 224 && mãKýTự < 240 ? 2 : mãKýTự >= 240 && mãKýTự <= 244 ? 3 : -1;
            if (trịSố < 0 || giáTrịByte.length - chỉSốVòngLặp < trịSố) throw new NgoạiLệĐốiSốKhôngHợpLệ("UTF-8 không hợp lệ");
            int giáTrịTốiThiểu = trịSố == 1 ? 128 : trịSố == 2 ? 2048 : trịSố == 3 ? 65536 : 0;
            if (trịSố > 0) mãKýTự &= (1 << (6 - trịSố)) - 1;
            for (int vịTríPhíaTrong = 0; vịTríPhíaTrong < trịSố; vịTríPhíaTrong++) { int giáTrịLùi = giáTrịByte[chỉSốVòngLặp++] & 255; if ((giáTrịLùi & 192) != 128) throw new NgoạiLệĐốiSốKhôngHợpLệ("UTF-8 không hợp lệ"); mãKýTự = mãKýTự << 6 | giáTrịLùi & 63; }
            if (mãKýTự < giáTrịTốiThiểu || mãKýTự > 0x10ffff || mãKýTự >= 0xd800 && mãKýTự <= 0xdfff) throw new NgoạiLệĐốiSốKhôngHợpLệ("UTF-8 không hợp lệ");
            if (mãKýTự < 65536) kếtQuả.append((char)mãKýTự);
            else { mãKýTự -= 65536; kếtQuả.append((char)(0xd800 | mãKýTự >> 10)); kếtQuả.append((char)(0xdc00 | mãKýTự & 1023)); }
        }
        return kếtQuả.toString();
    }
}
