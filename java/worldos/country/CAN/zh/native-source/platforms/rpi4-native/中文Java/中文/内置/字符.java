// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.内置;
/** 在 UTF-8 字节与 UTF-16 字符串之间转换；规范化与组合输入另行处理。 */
public final class 字符 {
    public static int 字节个数(byte[] 数据) { return 数据.length; }
    private 字符() {}
    public static int 长度(String 文本) { return 文本.length(); }
    public static boolean 相等文本(String 前端值, String 后端值) { return 前端值 == null ? 后端值 == null : 前端值.equals(后端值); }
    public static String 粘贴文本(String 前端值, String 后端值) { return 前端值.concat(后端值); }
    public static String 剪切值(String 文本, int 运行, int 结尾) { return 文本.substring(运行, 结尾); }
    public static int 解析整数(String 文本) { try { return Integer.parseInt(文本); } catch (NumberFormatException 错误) { throw new 编号格式失败("请检查数字格式和范围。"); } }
    public static String 写入整数值(int 数) { return Integer.toString(数); }
    public static int 代码分个数(String 文本) {
        int 数 = 0;
        for (int 循环索引 = 0; 循环索引 < 文本.length(); 循环索引++, 数++) {
            int 字符代码 = 文本.charAt(循环索引);
            if (字符代码 >= 0xd800 && 字符代码 <= 0xdbff && 循环索引 + 1 < 文本.length() && 文本.charAt(循环索引 + 1) >= 0xdc00 && 文本.charAt(循环索引 + 1) <= 0xdfff) 循环索引++;
        }
        return 数;
    }
    public static byte[] 编码(String 文本) {
        byte[] 临时值 = new byte[文本.length() * 3]; int 已写入 = 0;
        for (int 循环索引 = 0; 循环索引 < 文本.length(); 循环索引++) {
            int 字符代码 = 文本.charAt(循环索引);
            if (字符代码 >= 0xd800 && 字符代码 <= 0xdbff && 循环索引 + 1 < 文本.length() && 文本.charAt(循环索引 + 1) >= 0xdc00 && 文本.charAt(循环索引 + 1) <= 0xdfff) 字符代码 = 0x10000 + ((字符代码 - 0xd800) << 10) + 文本.charAt(++循环索引) - 0xdc00;
            else if (字符代码 >= 0xd800 && 字符代码 <= 0xdfff) 字符代码 = '?';
            if (字符代码 < 128) 临时值[已写入++] = (byte)字符代码;
            else if (字符代码 < 2048) { 临时值[已写入++] = (byte)(192 | 字符代码 >> 6); 临时值[已写入++] = (byte)(128 | 字符代码 & 63); }
            else if (字符代码 < 65536) { 临时值[已写入++] = (byte)(224 | 字符代码 >> 12); 临时值[已写入++] = (byte)(128 | 字符代码 >> 6 & 63); 临时值[已写入++] = (byte)(128 | 字符代码 & 63); }
            else { 临时值[已写入++] = (byte)(240 | 字符代码 >> 18); 临时值[已写入++] = (byte)(128 | 字符代码 >> 12 & 63); 临时值[已写入++] = (byte)(128 | 字符代码 >> 6 & 63); 临时值[已写入++] = (byte)(128 | 字符代码 & 63); }
        }
        byte[] 结果 = new byte[已写入]; System.arraycopy(临时值, 0, 结果, 0, 已写入); return 结果;
    }
    /** 使用 API 的非法参数异常拒绝格式错误的 UTF-8。 */
    public static String 解密数据(byte[] 字节值) {
        StringBuilder 结果 = new StringBuilder();
        for (int 循环索引 = 0; 循环索引 < 字节值.length;) {
            int 字符代码 = 字节值[循环索引++] & 255, 数 = 字符代码 < 128 ? 0 : 字符代码 >= 194 && 字符代码 < 224 ? 1 : 字符代码 >= 224 && 字符代码 < 240 ? 2 : 字符代码 >= 240 && 字符代码 <= 244 ? 3 : -1;
            if (数 < 0 || 字节值.length - 循环索引 < 数) throw new 无效参数异常("无效的 UTF-8");
            int 最小值 = 数 == 1 ? 128 : 数 == 2 ? 2048 : 数 == 3 ? 65536 : 0;
            if (数 > 0) 字符代码 &= (1 << (6 - 数)) - 1;
            for (int 内部侧位置 = 0; 内部侧位置 < 数; 内部侧位置++) { int 后端值 = 字节值[循环索引++] & 255; if ((后端值 & 192) != 128) throw new 无效参数异常("无效的 UTF-8"); 字符代码 = 字符代码 << 6 | 后端值 & 63; }
            if (字符代码 < 最小值 || 字符代码 > 0x10ffff || 字符代码 >= 0xd800 && 字符代码 <= 0xdfff) throw new 无效参数异常("无效的 UTF-8");
            if (字符代码 < 65536) 结果.append((char)字符代码);
            else { 字符代码 -= 65536; 结果.append((char)(0xd800 | 字符代码 >> 10)); 结果.append((char)(0xdc00 | 字符代码 & 1023)); }
        }
        return 结果.toString();
    }
}
