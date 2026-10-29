// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 能够计算 { int 值(); }
class 背景值 { static int 准备 = 7; int 数; String 名称; 背景值(int 数) { this.数 = 数; 名称 = "背景值"; } int 值() { return 数; } }
class 分支值 extends 背景值 implements 能够计算 { 分支值(int 数) { super(数); 名称 = "分支值"; } public int 值() { return 数 * 准备; } }
public class 测试对象集 {
    static int 初始状态 = 背景值.准备 + 2;
    static int 分支(int 数) { switch (数) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 稀疏值(int 数) { switch (数) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 实参) {
        分支值 第二操作数 = new 分支值(6); 背景值 第三操作数 = 第二操作数; 能够计算 第四操作数 = 第二操作数;
        System.out.println(初始状态 + ":" + 第二操作数.名称 + ":" + 第三操作数.值() + ":" + 第四操作数.值());
        System.out.println((第三操作数 instanceof 分支值) + ":" + (第三操作数 instanceof 能够计算) + ":" + 分支(2) + ":" + 稀疏值(100));
        Object[] 数组值 = new Object[3]; 数组值[0] = 第二操作数; 数组值[1] = "한글😀"; System.gc();
        System.out.println(((分支值)数组值[0]).值()); System.out.println((String)数组值[1]);
        int[] 个数列表 = {1, 2, 3, 4}; System.arraycopy(个数列表, 0, 个数列表, 1, 3); System.out.println(个数列表[3]);
        byte[] 字节值 = new byte[1]; 字节值[0] = (byte)255; char[] 字符 = {'한'}; short[] 是否短整数 = {(short)65535}; boolean[] 布尔值值 = {true};
        System.out.println(字节值[0] + ":" + 字符[0] + ":" + 是否短整数[0] + ":" + 布尔值值[0]);
    }
}
