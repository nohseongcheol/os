// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 能夠計算 { int 值(); }
class 背景值 { static int 準備 = 7; int 數; String 名稱; 背景值(int 數) { this.數 = 數; 名稱 = "背景值"; } int 值() { return 數; } }
class 分支值 extends 背景值 implements 能夠計算 { 分支值(int 數) { super(數); 名稱 = "分支值"; } public int 值() { return 數 * 準備; } }
public class 測試物件集 {
    static int 初始狀態 = 背景值.準備 + 2;
    static int 分支(int 數) { switch (數) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 稀疏值(int 數) { switch (數) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 實參) {
        分支值 第二操作數 = new 分支值(6); 背景值 第三操作數 = 第二操作數; 能夠計算 第四操作數 = 第二操作數;
        System.out.println(初始狀態 + ":" + 第二操作數.名稱 + ":" + 第三操作數.值() + ":" + 第四操作數.值());
        System.out.println((第三操作數 instanceof 分支值) + ":" + (第三操作數 instanceof 能夠計算) + ":" + 分支(2) + ":" + 稀疏值(100));
        Object[] 陣列值 = new Object[3]; 陣列值[0] = 第二操作數; 陣列值[1] = "한글😀"; System.gc();
        System.out.println(((分支值)陣列值[0]).值()); System.out.println((String)陣列值[1]);
        int[] 個數列表 = {1, 2, 3, 4}; System.arraycopy(個數列表, 0, 個數列表, 1, 3); System.out.println(個數列表[3]);
        byte[] 位元組值 = new byte[1]; 位元組值[0] = (byte)255; char[] 字元 = {'한'}; short[] 是否短整數 = {(short)65535}; boolean[] 布爾值值 = {true};
        System.out.println(位元組值[0] + ":" + 字元[0] + ":" + 是否短整數[0] + ":" + 布爾值值[0]);
    }
}
