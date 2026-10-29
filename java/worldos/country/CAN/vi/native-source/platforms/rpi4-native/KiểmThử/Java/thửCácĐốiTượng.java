// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface cóThểTính { int giáTrị(); }
class giáTrịNền { static int chuẩnBị = 7; int trịSố; String tên; giáTrịNền(int trịSố) { this.trịSố = trịSố; tên = "giáTrịNền"; } int giáTrị() { return trịSố; } }
class giáTrịNhánh extends giáTrịNền implements cóThểTính { giáTrịNhánh(int trịSố) { super(trịSố); tên = "giáTrịNhánh"; } public int giáTrị() { return trịSố * chuẩnBị; } }
public class thửCácĐốiTượng {
    static int trạngTháiBanĐầu = giáTrịNền.chuẩnBị + 2;
    static int nhánh(int trịSố) { switch (trịSố) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int giáTrịThưa(int trịSố) { switch (trịSố) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] cácĐốiSố) {
        giáTrịNhánh toánHạngThứHai = new giáTrịNhánh(6); giáTrịNền toánHạngThứBa = toánHạngThứHai; cóThểTính toánHạngThứTư = toánHạngThứHai;
        System.out.println(trạngTháiBanĐầu + ":" + toánHạngThứHai.tên + ":" + toánHạngThứBa.giáTrị() + ":" + toánHạngThứTư.giáTrị());
        System.out.println((toánHạngThứBa instanceof giáTrịNhánh) + ":" + (toánHạngThứBa instanceof cóThểTính) + ":" + nhánh(2) + ":" + giáTrịThưa(100));
        Object[] giáTrịMảng = new Object[3]; giáTrịMảng[0] = toánHạngThứHai; giáTrịMảng[1] = "한글😀"; System.gc();
        System.out.println(((giáTrịNhánh)giáTrịMảng[0]).giáTrị()); System.out.println((String)giáTrịMảng[1]);
        int[] danhSáchSốLượng = {1, 2, 3, 4}; System.arraycopy(danhSáchSốLượng, 0, danhSáchSốLượng, 1, 3); System.out.println(danhSáchSốLượng[3]);
        byte[] giáTrịByte = new byte[1]; giáTrịByte[0] = (byte)255; char[] KýTự = {'한'}; short[] làNgắnKiểu = {(short)65535}; boolean[] giáTrịLuậnLý = {true};
        System.out.println(giáTrịByte[0] + ":" + KýTự[0] + ":" + làNgắnKiểu[0] + ":" + giáTrịLuậnLý[0]);
    }
}
