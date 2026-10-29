// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class thửCácRanhGiới {
    static int giáTrịSựThấtBại() { throw new IllegalStateException("TácVụ 중 ngoạiLệ"); }
    public static void main(String[] a) throws Exception {
        Object mảngThuần = new Object[2]; System.out.println(mảngThuần instanceof String[]);
        try { String[] kếtQuảKhôngHợpLệ = (String[])mảngThuần; } catch (ClassCastException e) { System.out.println("giáTrịMảng chuyểnĐổiGiáTrị CácPhépKiểmTra"); }
        Object[] danhSáchVănBản = new String[2];
        try { danhSáchVănBản[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("giáTrịMảng giáTrịKiểu CácPhépKiểmTra"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, danhSáchVănBản, 0, 2); } catch (ArrayStoreException e) { System.out.println("saoChépGiáTrị giáTrịKiểu CácPhépKiểmTra"); }
        System.out.println((String)danhSáchVănBản[0]);
        try { "vănBản".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("KýTự cắtXén"); }
        Integer giáTrịMột = Integer.valueOf(127), giáTrịHai = Integer.valueOf(127); System.out.println(giáTrịMột == giáTrịHai);
        Object giáTrịKhóa = new Object(); try { synchronized (giáTrịKhóa) { giáTrịSựThấtBại(); } } catch (IllegalStateException e) { System.out.println("giáTrịKhóa ngoạiLệ"); }
        synchronized (giáTrịKhóa) { System.out.println("giáTrịKhóa 회수"); }
        byte[] DữLiệu = {0, (byte)128, (byte)255, 10};
        FileOutputStream ĐầuRa = new FileOutputStream("giáTrịByte.bin"); ĐầuRa.write(DữLiệu); ĐầuRa.flush(); ĐầuRa.close();
        FileInputStream giáTrịVào = new FileInputStream("giáTrịByte.bin"); byte[] đọcKếtQuả = new byte[8];
        System.out.println(giáTrịVào.read(đọcKếtQuả, 2, 4)); System.out.println(đọcKếtQuả[3] + ":" + đọcKếtQuả[4]);
        System.out.println(giáTrịVào.read(đọcKếtQuả)); System.out.println(giáTrịVào.read(đọcKếtQuả, 0, 0)); giáTrịVào.close();
        try { giáTrịVào.read(); } catch (IOException e) { System.out.println("닫힌 Tệp"); }
    }
}
