// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int ค่า(); }
class พื้นหลัง_ค่า { static int จัดเตรียม = 7; int หมายเลข; String ชื่อ; พื้นหลัง_ค่า(int หมายเลข) { this.หมายเลข = หมายเลข; ชื่อ = "พื้นหลัง_ค่า"; } int ค่า() { return หมายเลข; } }
class สาขา_ค่า extends พื้นหลัง_ค่า implements 계산가능 { สาขา_ค่า(int หมายเลข) { super(หมายเลข); ชื่อ = "สาขา_ค่า"; } public int ค่า() { return หมายเลข * จัดเตรียม; } }
public class 객체시험 {
    static int สภาวะเริ่มต้น = พื้นหลัง_ค่า.จัดเตรียม + 2;
    static int สาขา(int หมายเลข) { switch (หมายเลข) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int หมายเลข) { switch (หมายเลข) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] อาร์กิวเมนต์) {
        สาขา_ค่า 나 = new สาขา_ค่า(6); พื้นหลัง_ค่า 다 = 나; 계산가능 라 = 나;
        System.out.println(สภาวะเริ่มต้น + ":" + 나.ชื่อ + ":" + 다.ค่า() + ":" + 라.ค่า());
        System.out.println((다 instanceof สาขา_ค่า) + ":" + (다 instanceof 계산가능) + ":" + สาขา(2) + ":" + 띄엄(100));
        Object[] อาร์เรย์_ค่า = new Object[3]; อาร์เรย์_ค่า[0] = 나; อาร์เรย์_ค่า[1] = "한글😀"; System.gc();
        System.out.println(((สาขา_ค่า)อาร์เรย์_ค่า[0]).ค่า()); System.out.println((String)อาร์เรย์_ค่า[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] ไบต์_ค่า = new byte[1]; ไบต์_ค่า[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] แบบบูลีน_ค่า = {true};
        System.out.println(ไบต์_ค่า[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + แบบบูลีน_ค่า[0]);
    }
}
