// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 测试边界列 {
    static int 失败值() { throw new IllegalStateException("任务 중 异常"); }
    public static void main(String[] a) throws Exception {
        Object 明文数组 = new Object[2]; System.out.println(明文数组 instanceof String[]);
        try { String[] 无效结果 = (String[])明文数组; } catch (ClassCastException e) { System.out.println("数组值 转换值 检查项"); }
        Object[] 文本列表 = new String[2];
        try { 文本列表[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("数组值 类型值 检查项"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, 文本列表, 0, 2); } catch (ArrayStoreException e) { System.out.println("复制值 类型值 检查项"); }
        System.out.println((String)文本列表[0]);
        try { "文本".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("字符 裁剪"); }
        Integer 一值 = Integer.valueOf(127), 二值 = Integer.valueOf(127); System.out.println(一值 == 二值);
        Object 锁值 = new Object(); try { synchronized (锁值) { 失败值(); } } catch (IllegalStateException e) { System.out.println("锁值 异常"); }
        synchronized (锁值) { System.out.println("锁值 회수"); }
        byte[] 数据 = {0, (byte)128, (byte)255, 10};
        FileOutputStream 输出 = new FileOutputStream("字节值.bin"); 输出.write(数据); 输出.flush(); 输出.close();
        FileInputStream 输入值 = new FileInputStream("字节值.bin"); byte[] 读取结果 = new byte[8];
        System.out.println(输入值.read(读取结果, 2, 4)); System.out.println(读取结果[3] + ":" + 读取结果[4]);
        System.out.println(输入值.read(读取结果)); System.out.println(输入值.read(读取结果, 0, 0)); 输入值.close();
        try { 输入值.read(); } catch (IOException e) { System.out.println("닫힌 文件"); }
    }
}
