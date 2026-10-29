// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 可能判定計算 { int 値(); }
class 背景値 { static int 用意 = 7; int 数; String 名前; 背景値(int 数) { this.数 = 数; 名前 = "背景値"; } int 値() { return 数; } }
class 分岐値 extends 背景値 implements 可能判定計算 { 分岐値(int 数) { super(数); 名前 = "分岐値"; } public int 値() { return 数 * 用意; } }
public class オブジェクト群試験 {
    static int 初期状況 = 背景値.用意 + 2;
    static int 分岐(int 数) { switch (数) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 疎値(int 数) { switch (数) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 引数) {
        分岐値 第二被演算子 = new 分岐値(6); 背景値 第三被演算子 = 第二被演算子; 可能判定計算 第四被演算子 = 第二被演算子;
        System.out.println(初期状況 + ":" + 第二被演算子.名前 + ":" + 第三被演算子.値() + ":" + 第四被演算子.値());
        System.out.println((第三被演算子 instanceof 分岐値) + ":" + (第三被演算子 instanceof 可能判定計算) + ":" + 分岐(2) + ":" + 疎値(100));
        Object[] 配列値 = new Object[3]; 配列値[0] = 第二被演算子; 配列値[1] = "한글😀"; System.gc();
        System.out.println(((分岐値)配列値[0]).値()); System.out.println((String)配列値[1]);
        int[] 個数一覧 = {1, 2, 3, 4}; System.arraycopy(個数一覧, 0, 個数一覧, 1, 3); System.out.println(個数一覧[3]);
        byte[] バイト値 = new byte[1]; バイト値[0] = (byte)255; char[] 文字 = {'한'}; short[] 判定短整数 = {(short)65535}; boolean[] 真偽値値 = {true};
        System.out.println(バイト値[0] + ":" + 文字[0] + ":" + 判定短整数[0] + ":" + 真偽値値[0]);
    }
}
