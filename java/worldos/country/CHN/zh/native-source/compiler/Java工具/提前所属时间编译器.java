// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** 从 Java 类文件生成独立 ARM64 内核的 C 源码，在宿主 JDK 上运行。 */
public final class 提前所属时间编译器 {
    static final class 翻译错误 extends RuntimeException {
        翻译错误(String 说明) { super(说明); }
    }
    static final class 数据读取器 {
        final byte[] 数据;
        int 位置;
        数据读取器(byte[] 输入数据) { 数据 = 输入数据; }
        byte[] 读取(int 长度) {
            if (长度 < 0 || 长度 > 数据.length - 位置) throw new 翻译错误("已裁剪值 类值 또는 命令 数据");
            byte[] 结果 = Arrays.copyOfRange(数据, 位置, 位置 + 长度); 位置 += 长度; return 结果;
        }
        int 读取字节() { if (位置 >= 数据.length) throw new 翻译错误("已裁剪值 命令 数据"); return 数据[位置++] & 255; }
        int 读取短整数() { return (读取字节() << 8) | 读取字节(); }
        int 读取整数() { return (读取短整数() << 16) | 读取短整数(); }
        int 读取有符号字节() { return (byte) 读取字节(); }
        int 读取有符号短整数() { return (short) 读取短整数(); }
    }
    static final class 成员数据 {
        final int 存取条目;
        final String 名称, 说明值;
        final Map<String, byte[]> 属性值;
        成员数据(int 存取值, String 名称值, String 描述符数据, Map<String, byte[]> 属性数据) {
            存取条目 = 存取值; 名称 = 名称值; 说明值 = 描述符数据; 属性值 = 属性数据;
        }
    }
    static final class 方法引用 implements Comparable<方法引用> {
        final String 所有者值, 名称, 说明值;
        方法引用(String 自有值, String 名称值, String 描述符数据) { 所有者值 = 自有值; 名称 = 名称值; 说明值 = 描述符数据; }
        String[] 部件列() { return new String[]{所有者值, 名称, 说明值}; }
        public int compareTo(方法引用 对端值) {
            int 比较值 = 所有者值.compareTo(对端值.所有者值);
            if (比较值 == 0) 比较值 = 名称.compareTo(对端值.名称);
            return 比较值 == 0 ? 说明值.compareTo(对端值.说明值) : 比较值;
        }
        public boolean equals(Object 对端值) { return 对端值 instanceof 方法引用 && compareTo((方法引用) 对端值) == 0; }
        public int hashCode() { return Objects.hash(所有者值, 名称, 说明值); }
    }
    static final class 类数据 {
        final int[] 常量种类;
        final Object[] 常量数据;
        final String 名称;
        final List<成员数据> 字段值, 函数;
        类数据(Path 路径) throws IOException {
            数据读取器 读取器值 = new 数据读取器(Files.readAllBytes(路径));
            if (读取器值.读取整数() != 0xcafebabe) throw new 翻译错误("Java 类值 표식이 아님");
            读取器值.读取(4);
            int 项目个数 = 读取器值.读取短整数(); 常量种类 = new int[项目个数]; 常量数据 = new Object[项目个数];
            for (int 序数索引 = 1; 序数索引 < 项目个数; 序数索引++) {
                int 种类值 = 读取器值.读取字节(); 常量种类[序数索引] = 种类值;
                switch (种类值) {
                    case 1:
                        int 长度 = 读取器值.读取短整数();
                        byte[] 字符缓冲 = 读取器值.读取(长度), 长度带前缀数据 = new byte[长度 + 2];
                        长度带前缀数据[0] = (byte)(长度 >> 8); 长度带前缀数据[1] = (byte)长度;
                        System.arraycopy(字符缓冲, 0, 长度带前缀数据, 2, 长度);
                        常量数据[序数索引] = new DataInputStream(new ByteArrayInputStream(长度带前缀数据)).readUTF(); break;
                    case 3: 常量数据[序数索引] = 读取器值.读取整数(); break;
                    case 4: 读取器值.读取(4); break;
                    case 5: case 6: 读取器值.读取(8); 序数索引++; break;
                    case 7: case 8: case 16: 常量数据[序数索引] = 读取器值.读取短整数(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        常量数据[序数索引] = new int[]{读取器值.读取短整数(), 读取器值.读取短整数()}; break;
                    case 15: 常量数据[序数索引] = new int[]{读取器值.读取字节(), 读取器值.读取短整数()}; break;
                    default: throw new 翻译错误("지원하지 않는 常量值 种类值: " + 种类值);
                }
            }
            读取器值.读取短整数(); 名称 = 类名称(读取器值.读取短整数());
            if (!类名称(读取器值.读取短整数()).equals("java/lang/Object") || 读取器值.读取短整数() != 0)
                throw new 翻译错误(名称 + ": 상속 및 인터페이스 是否不支持");
            字段值 = 读取成员列(读取器值); 函数 = 读取成员列(读取器值); 读取属性集(读取器值);
            if (读取器值.位置 != 读取器值.数据.length) throw new 翻译错误("类值 뒤에 남은 数据");
        }
        String 字符(int 编号) {
            if (编号 < 1 || 编号 >= 常量种类.length || 常量种类[编号] != 1) throw new 翻译错误("字符 常量值 编号 错误");
            return (String) 常量数据[编号];
        }
        String 类名称(int 编号) {
            if (编号 < 1 || 编号 >= 常量种类.length || 常量种类[编号] != 7) throw new 翻译错误("类值 引用 错误");
            return 字符((Integer)常量数据[编号]);
        }
        方法引用 引用(int 编号) {
            if (编号 < 1 || 编号 >= 常量种类.length || 常量种类[编号] < 9 || 常量种类[编号] > 11) throw new 翻译错误("멤버 引用 错误");
            int[] 一对值 = (int[])常量数据[编号], 名称一对 = (int[])常量数据[一对值[1]];
            return new 方法引用(类名称(一对值[0]), 字符(名称一对[0]), 字符(名称一对[1]));
        }
        Map<String, byte[]> 读取属性集(数据读取器 读取器值) {
            Map<String, byte[]> 结果 = new LinkedHashMap<>();
            int 项目个数 = 读取器值.读取短整数();
            for (int 序数索引 = 0; 序数索引 < 项目个数; 序数索引++) {
                String 属性名称 = 字符(读取器值.读取短整数()); byte[] 值 = 读取器值.读取(读取器值.读取整数());
                if (结果.put(属性名称, 值) != null) throw new 翻译错误("겹친 属性值: " + 属性名称);
            }
            return 结果;
        }
        List<成员数据> 读取成员列(数据读取器 读取器值) {
            List<成员数据> 结果 = new ArrayList<>(); int 项目个数 = 读取器值.读取短整数();
            for (int 序数索引 = 0; 序数索引 < 项目个数; 序数索引++) {
                int 存取条目 = 读取器值.读取短整数(); String 方法条目名称 = 字符(读取器值.读取短整数()), 说明值 = 字符(读取器值.读取短整数());
                结果.add(new 成员数据(存取条目, 方法条目名称, 说明值, 读取属性集(读取器值)));
            }
            return 结果;
        }
    }
    static final class 方法描述符 {
        final List<String> 实参 = new ArrayList<>();
        final String 发回结果;
        方法描述符(String 说明值) {
            if (!说明值.startsWith("(")) throw new 翻译错误("函数 说明值 错误: " + 说明值);
            int 结尾 = 说明值.indexOf(')'); if (结尾 < 0) throw new 翻译错误("函数 说明值 错误: " + 说明值);
            实参.addAll(解析类型列(说明值.substring(1, 结尾)));
            List<String> 已返回值列 = 解析类型列(说明值.substring(结尾 + 1));
            if (实参.contains("V") || 已返回值列.size() != 1) throw new 翻译错误("函数 说明值 错误: " + 说明值);
            发回结果 = 已返回值列.get(0);
        }
    }
    static List<String> 解析类型列(String 说明值) {
        List<String> 结果 = new ArrayList<>();
        String[] 已允许格式 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int 位置 = 0; 位置 < 说明值.length();) {
            String 选中状态值 = null;
            for (String 格式值 : 已允许格式) if (说明值.startsWith(格式值, 位置)) { 选中状态值 = 格式值; break; }
            if (选中状态值 == null) throw new 翻译错误("지원하지 않는 数据类型: " + 说明值);
            结果.add(选中状态值); 位置 += 选中状态值.length();
        }
        return 结果;
    }
    static String 符号(String 种类值, String... 部件列) {
        try {
            byte[] 哈希文件 = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 部件列).getBytes(StandardCharsets.UTF_8));
            StringBuilder 文本 = new StringBuilder("j_" + 种类值 + "_");
            for (int 序数索引 = 0; 序数索引 < 12; 序数索引++) 文本.append(String.format(Locale.ROOT, "%02x", 哈希文件[序数索引] & 255));
            return 文本.toString();
        } catch (Exception 错误) { throw new 翻译错误(错误.toString()); }
    }
    final Map<String, 类数据> 类集列表 = new TreeMap<>();
    final Map<方法引用, 成员数据> 方法列列表 = new TreeMap<>(), 字段列列表 = new TreeMap<>();
    final Map<String, String> 字符串值列 = new LinkedHashMap<>(), 机器函数列表 = new LinkedHashMap<>();
    final String 执行状态目标, 计算机类;
    final int 堆机器字个数;
    final Path 资源路径;
    提前所属时间编译器(List<Path> 路径列表, String 目标值, int 词法用机器字个数, Path 资源值) throws IOException {
        if ((!目标值.equals("kernel") && !目标值.equals("user")) || 词法用机器字个数 < 1024 || 词法用机器字个数 > 1048576) throw new 翻译错误("执行命令 目标值 또는 内存 地址区域 大小 错误");
        执行状态目标 = 目标值; 堆机器字个数 = 词法用机器字个数; 资源路径 = 资源值;
        // 生成各国源码时，此名称也翻译成对应语言。
        计算机类 = 目标值.equals("kernel") ? "板" : "用户";
        for (String 行 : Files.readAllLines(资源值.resolve("计算机功能.tsv"), StandardCharsets.UTF_8)) {
            String[] 部件列 = 行.split("\t", -1);
            if (部件列.length != 4) throw new 翻译错误("计算机 函数 数据 错误");
            if (部件列[0].equals(目标值)) 机器函数列表.put(部件列[1] + 部件列[2], 部件列[3]);
        }
        for (Path 路径 : 路径列表) {
            类数据 数据 = new 类数据(路径);
            if (类集列表.put(数据.名称, 数据) != null) throw new 翻译错误("중복 类值: " + 数据.名称);
            for (成员数据 字段值 : 数据.字段值) {
                if ((字段值.存取条目 & 8) == 0 || 解析类型列(字段值.说明值).equals(Collections.singletonList("V"))) throw new 翻译错误("静态值 필드만 支持值");
                if (字段列列表.put(new 方法引用(数据.名称, 字段值.名称, 字段值.说明值), 字段值) != null) throw new 翻译错误("중복 字段值");
            }
            for (成员数据 函数 : 数据.函数) {
                if (函数.名称.equals("<init>")) continue;
                if ((函数.存取条目 & 8) == 0 || (函数.存取条目 & (0x20 | 0x400)) != 0) throw new 翻译错误("静态值 비동기화 함수만 支持值");
                new 方法描述符(函数.说明值);
                if (方法列列表.put(new 方法引用(数据.名称, 函数.名称, 函数.说明值), 函数) != null) throw new 翻译错误("중복 函数");
            }
        }
    }
    String 字符串符号(String 文本) { return 字符串值列.computeIfAbsent(文本, 值 -> "j_text_" + 字符串值列.size()); }
    String 常量表达式(类数据 数据, int 编号) {
        if (编号 < 1 || 编号 >= 数据.常量种类.length) throw new 翻译错误("常量值 编号 裁剪 错误");
        if (数据.常量种类[编号] == 3) return "(word)(uint32_t)(" + 数据.常量数据[编号] + ")";
        if (数据.常量种类[编号] == 8) return "(word)" + 字符串符号(数据.字符((Integer)数据.常量数据[编号]));
        throw new 翻译错误("정수와 字符串 상수만 支持值");
    }
    String 方法原型(方法引用 引用) {
        List<String> 参数列列表 = new ArrayList<>(); int 项目个数 = new 方法描述符(引用.说明值).实参.size();
        for (int 序数索引 = 0; 序数索引 < 项目个数; 序数索引++) 参数列列表.add("word a" + 序数索引);
        return "static word " + 符号("method", 引用.部件列()) + "(" + (项目个数 == 0 ? "void" : String.join(", ", 参数列列表)) + ")";
    }
    void 检查局部(int 编号, int 局部变量个数) { if (编号 < 0 || 编号 >= 局部变量个数) throw new 翻译错误("局部作用域 变量值 编号 裁剪 错误"); }
    void 发射分支(List<String> 输出, Set<Integer> 分支列表, int 位置, int 移动量总量, String 条件) {
        int 目的地址值 = 位置 + 移动量总量; 分支列表.add(目的地址值);
        输出.add((条件 == null ? "" : "if (" + 条件 + ") ") + "goto b" + 目的地址值 + ";");
    }
    String 方法主体(方法引用 函数, 成员数据 数据) {
        byte[] 主体数据 = 数据.属性值.get("Code"); if (主体数据 == null) throw new 翻译错误("函数 몸체가 缺失方法: " + 函数.名称);
        数据读取器 读取器值 = new 数据读取器(主体数据); int 栈深度 = 读取器值.读取短整数(), 局部变量个数 = 读取器值.读取短整数();
        数据读取器 命令数据 = new 数据读取器(读取器值.读取(读取器值.读取整数()));
        if (读取器值.读取短整数() != 0) throw new 翻译错误("try/catch/finally 是否不支持");
        方法描述符 格式值 = new 方法描述符(函数.说明值); if (局部变量个数 < 格式值.实参.size()) throw new 翻译错误("매개변수보다 적은 局部作用域 变量值");
        类数据 类值 = 类集列表.get(函数.所有者值);
        List<String> 输出 = new ArrayList<>(); 输出.add(方法原型(函数) + " {");
        输出.add("word s[" + Math.max(栈深度, 1) + "], l[" + Math.max(局部变量个数, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 序数索引 = 0; 序数索引 < 格式值.实参.size(); 序数索引++) 输出.add("l[" + 序数索引 + "] = a" + 序数索引 + ";");
        Set<Integer> 边界列列表 = new HashSet<>(), 分支列表 = new HashSet<>();
        String[] 比较列列表 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (命令数据.位置 < 命令数据.数据.length) {
            int 位置 = 命令数据.位置, 命令 = 命令数据.读取字节(); 边界列列表.add(位置); 输出.add("b" + 位置 + ":;");
            if (命令 == 0) continue;
            if (命令 == 1) 输出.add("PUSH(0);");
            else if (命令 >= 2 && 命令 <= 8) 输出.add("PUSH((uint32_t)(" + (命令 - 3) + "));");
            else if (命令 == 16 || 命令 == 17) 输出.add("PUSH((uint32_t)(" + (命令 == 16 ? 命令数据.读取有符号字节() : 命令数据.读取有符号短整数()) + "));");
            else if (命令 == 18 || 命令 == 19) 输出.add("PUSH(" + 常量表达式(类值, 命令 == 18 ? 命令数据.读取字节() : 命令数据.读取短整数()) + ");");
            else if (命令 == 21 || 命令 == 25 || (命令 >= 26 && 命令 <= 29) || (命令 >= 42 && 命令 <= 45)) {
                int 编号 = 命令 == 21 || 命令 == 25 ? 命令数据.读取字节() : 命令 - (命令 <= 29 ? 26 : 42);
                检查局部(编号, 局部变量个数); 输出.add("PUSH(l[" + 编号 + "]);");
            } else if (命令 == 54 || 命令 == 58 || (命令 >= 59 && 命令 <= 62) || (命令 >= 75 && 命令 <= 78)) {
                int 编号 = 命令 == 54 || 命令 == 58 ? 命令数据.读取字节() : 命令 - (命令 <= 62 ? 59 : 75);
                检查局部(编号, 局部变量个数); 输出.add("l[" + 编号 + "] = POP();");
            } else if (命令 == 46) 输出.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (命令 == 79) 输出.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (命令 == 87 || 命令 == 88) 输出.add(命令 == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (命令 >= 89 && 命令 <= 95) {
                int[] 项目个数列 = {1,2,3,2,3,4,2}; String[] 排序列表 = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 序数索引 = 0; 序数索引 < 项目个数列[命令 - 89]; 序数索引++) 输出.add("abcd".charAt(序数索引) + " = POP();");
                for (char 值 : 排序列表[命令 - 89].toCharArray()) 输出.add("PUSH(" + 值 + ");");
            } else if (命令 == 96 || 命令 == 100 || 命令 == 104 || 命令 == 126 || 命令 == 128 || 命令 == 130) {
                String 操作值 = 命令 == 96 ? "+" : 命令 == 100 ? "-" : 命令 == 104 ? "*" : 命令 == 126 ? "&" : 命令 == 128 ? "|" : "^";
                输出.add("b = POP(); a = POP(); PUSH((uint32_t)a " + 操作值 + " (uint32_t)b);");
            } else if (命令 == 108 || 命令 == 112) 输出.add("b = POP(); a = POP(); PUSH(divide(a,b," + (命令 == 112 ? 1 : 0) + "));");
            else if (命令 == 116) 输出.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (命令 == 120 || 命令 == 122 || 命令 == 124) {
                输出.add("b = POP(); a = POP();"); 输出.add("PUSH(" + (命令 == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (命令 == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (命令 == 132) {
                int 编号 = 命令数据.读取字节(), 递增总量 = 命令数据.读取有符号字节(); 检查局部(编号, 局部变量个数);
                输出.add("l[" + 编号 + "] = (uint32_t)l[" + 编号 + "] + (uint32_t)(" + 递增总量 + ");");
            } else if (命令 >= 145 && 命令 <= 147) 输出.add("a = POP(); PUSH((uint32_t)(" + (命令 == 145 ? "int8_t" : 命令 == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (命令 >= 153 && 命令 <= 158) {
                输出.add("a = POP();"); 发射分支(输出, 分支列表, 位置, 命令数据.读取有符号短整数(), "(int32_t)a " + 比较列列表[命令 - 153] + " 0");
            } else if (命令 >= 159 && 命令 <= 166) {
                输出.add("b = POP(); a = POP();"); 发射分支(输出, 分支列表, 位置, 命令数据.读取有符号短整数(), 命令 >= 165 ? "a " + 比较列列表[命令 - 159] + " b" : "(int32_t)a " + 比较列列表[命令 - 159] + " (int32_t)b");
            } else if (命令 == 167 || 命令 == 200) 发射分支(输出, 分支列表, 位置, 命令 == 167 ? 命令数据.读取有符号短整数() : 命令数据.读取整数(), null);
            else if (命令 == 170 || 命令 == 171) {
                while (命令数据.位置 % 4 != 0) 命令数据.读取字节();
                int 默认值 = 命令数据.读取整数(); 输出.add("a = POP();");
                if (命令 == 170) {
                    int 底端值 = 命令数据.读取整数(), 顶端值 = 命令数据.读取整数(); long 项目个数 = (long)顶端值 - 底端值 + 1;
                    if (项目个数 < 1 || 项目个数 > (命令数据.数据.length - 命令数据.位置) / 4) throw new 翻译错误("switch 裁剪 错误");
                    for (long 值 = 底端值; 值 <= 顶端值; 值++) 发射分支(输出, 分支列表, 位置, 命令数据.读取整数(), "(int32_t)a == (" + 值 + ")");
                } else {
                    int 项目个数 = 命令数据.读取整数(), 前端数据 = 0;
                    if (项目个数 < 0 || 项目个数 > (命令数据.数据.length - 命令数据.位置) / 8) throw new 翻译错误("switch 大小 错误");
                    for (int 序数索引 = 0; 序数索引 < 项目个数; 序数索引++) {
                        int 值 = 命令数据.读取整数(); if (序数索引 > 0 && 值 <= 前端数据) throw new 翻译错误("switch 排序值 错误"); 前端数据 = 值;
                        发射分支(输出, 分支列表, 位置, 命令数据.读取整数(), "(int32_t)a == (" + 值 + ")");
                    }
                }
                发射分支(输出, 分支列表, 位置, 默认值, null);
            } else if (命令 == 172 || 命令 == 176 || 命令 == 177) 输出.add("return " + (命令 == 177 ? "0" : "POP()") + ";");
            else if (命令 == 178 || 命令 == 179) {
                方法引用 引用 = 类值.引用(命令数据.读取短整数()); if (!字段列列表.containsKey(引用)) throw new 翻译错误("알 数 없는 字段值");
                输出.add(符号("init", 引用.所有者值) + "();"); String 字段值 = 符号("field", 引用.部件列());
                输出.add(命令 == 178 ? "PUSH(" + 字段值 + ");" : 字段值 + " = POP();");
            } else if (命令 == 184) {
                方法引用 引用 = 类值.引用(命令数据.读取短整数()); if (!方法列列表.containsKey(引用)) throw new 翻译错误("알 数 없는 函数");
                方法描述符 调用状态类型 = new 方法描述符(引用.说明值); int 项目个数 = 调用状态类型.实参.size();
                输出.add(符号("init", 引用.所有者值) + "();"); 输出.add("if(sp < " + 项目个数 + ") kernel_panic(\"call stack underflow\"); sp -= " + 项目个数 + ";");
                List<String> 调用状态参数列 = new ArrayList<>(); for (int 序数索引 = 0; 序数索引 < 项目个数; 序数索引++) 调用状态参数列.add("s[sp + " + 序数索引 + "]");
                输出.add("a = " + 符号("method", 引用.部件列()) + "(" + String.join(",", 调用状态参数列) + ");");
                if (!调用状态类型.发回结果.equals("V")) 输出.add("PUSH(a);");
            } else if (命令 == 182) {
                方法引用 引用 = 类值.引用(命令数据.读取短整数());
                if (引用.equals(new 方法引用("java/lang/String", "length", "()I"))) 输出.add("a = POP(); PUSH(length(a));");
                else if (引用.equals(new 方法引用("java/lang/String", "charAt", "(I)C"))) 输出.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new 翻译错误("가상 函数 调用 是否不支持");
            } else if (命令 == 188) {
                if (命令数据.读取字节() != 10) throw new 翻译错误("new int[]만 支持值"); 输出.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (命令 == 190) 输出.add("a = POP(); PUSH(length(a));");
            else if (命令 == 196) {
                int 扩展名值 = 命令数据.读取字节(), 编号 = 命令数据.读取短整数(); 检查局部(编号, 局部变量个数);
                if (扩展名值 == 21 || 扩展名值 == 25) 输出.add("PUSH(l[" + 编号 + "]);");
                else if (扩展名值 == 54 || 扩展名值 == 58) 输出.add("l[" + 编号 + "] = POP();");
                else if (扩展名值 == 132) 输出.add("l[" + 编号 + "] = (uint32_t)l[" + 编号 + "] + (uint32_t)(" + 命令数据.读取有符号短整数() + ");");
                else throw new 翻译错误("是否不支持 wide 命令");
            } else if (命令 == 198 || 命令 == 199) {
                输出.add("a = POP();"); 发射分支(输出, 分支列表, 位置, 命令数据.读取有符号短整数(), "a " + (命令 == 198 ? "==" : "!=") + " 0");
            } else throw new 翻译错误(函数.所有者值 + "." + 函数.名称 + ", 字节值 " + 位置 + ": 是否不支持 命令 " + 命令);
        }
        if (!边界列列表.containsAll(分支列表)) throw new 翻译错误("命令 경계가 아닌 곳으로 分支");
        输出.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 输出);
    }
    String 导出方法(String 连接符号, String 目标值, boolean 拥有条目分) {
        int 位置索引 = 目标值.lastIndexOf('.'); if (位置索引 < 0 || !连接符号.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new 翻译错误("发射值 赋值值 错误");
        String 所有者值 = 目标值.substring(0, 位置索引).replace('.', '/'), 名称 = 目标值.substring(位置索引 + 1); 方法引用 选中状态值 = null;
        for (方法引用 引用 : 方法列列表.keySet()) if (引用.所有者值.equals(所有者值) && 引用.名称.equals(名称)) {
            if (选中状态值 != null) throw new 翻译错误("겹친 发射值 目标值"); 选中状态值 = 引用;
        }
        if (选中状态值 == null || (方法列列表.get(选中状态值).存取条目 & 0x100) != 0) throw new 翻译错误("내보낼 함수가 缺失方法 또는 native 函数");
        方法描述符 格式值 = new 方法描述符(选中状态值.说明值);
        if ((拥有条目分 && !格式值.实参.isEmpty()) || !Arrays.asList("V", "I").contains(格式值.发回结果)) throw new 翻译错误("条目分值 또는 C 边界位置值 格式值 错误");
        List<String> 参数列列表 = new ArrayList<>(), 调用状态参数列 = new ArrayList<>();
        for (int 序数索引 = 0; 序数索引 < 格式值.实参.size(); 序数索引++) {
            if (!格式值.实参.get(序数索引).equals("I")) throw new 翻译错误("C 경계는 int 인수만 支持值");
            参数列列表.add("int32_t a" + 序数索引); 调用状态参数列.add("(uint32_t)a" + 序数索引);
        }
        return (格式值.发回结果.equals("V") ? "void " : "int32_t ") + 连接符号 + "(" + (参数列列表.isEmpty() ? "void" : String.join(",", 参数列列表)) + ") { " + 符号("init", 选中状态值.所有者值) + "(); " + (格式值.发回结果.equals("V") ? "" : "return (int32_t)") + 符号("method", 选中状态值.部件列()) + "(" + String.join(",", 调用状态参数列) + "); }";
    }
    String 生成(String 条目分, List<String> 导出条目列, boolean 通用表示法) throws IOException {
        List<String> 声明列列表 = new ArrayList<>(), 主体列列表 = new ArrayList<>(), 字段声明列 = new ArrayList<>();
        for (Map.Entry<方法引用, 成员数据> 条目值 : 方法列列表.entrySet()) {
            方法引用 引用 = 条目值.getKey(); 成员数据 数据 = 条目值.getValue(); 声明列列表.add(方法原型(引用) + ";");
            if ((数据.存取条目 & 0x100) != 0) {
                String 连接 = 机器函数列表.get(引用.名称 + 引用.说明值);
                if (!引用.所有者值.equals(计算机类) || 连接 == null) throw new 翻译错误("허용되지 않은 native 函数: " + 引用.名称);
                int 项目个数 = new 方法描述符(引用.说明值).实参.size(); List<String> 参数列列表 = new ArrayList<>();
                for (int 序数索引 = 0; 序数索引 < 项目个数; 序数索引++) 参数列列表.add("a" + 序数索引);
                声明列列表.add("extern word " + 连接 + "(" + (项目个数 == 0 ? "void" : String.join(",", Collections.nCopies(项目个数, "word"))) + ");");
                主体列列表.add(方法原型(引用) + " { return " + 连接 + "(" + String.join(",", 参数列列表) + "); }");
            } else 主体列列表.add(方法主体(引用, 数据));
        }
        for (Map.Entry<方法引用, 成员数据> 条目值 : 字段列列表.entrySet()) {
            方法引用 引用 = 条目值.getKey(); byte[] 常量值 = 条目值.getValue().属性值.get("ConstantValue");
            String 值 = 常量值 == null ? "0" : 常量表达式(类集列表.get(引用.所有者值), new 数据读取器(常量值).读取短整数());
            字段声明列.add("static word " + 符号("field", 引用.部件列()) + " = " + 值 + ";");
        }
        for (String 名称 : 类集列表.keySet()) {
            String 初始化 = 符号("init", 名称), 状态值 = 符号("state", 名称);
            声明列列表.add("static void " + 初始化 + "(void);"); 字段声明列.add("static unsigned " + 状态值 + ";");
            方法引用 引用 = new 方法引用(名称, "<clinit>", "()V");
            主体列列表.add("static void " + 初始化 + "(void) { if(" + 状态值 + ") return; " + 状态值 + " = 1; " + (方法列列表.containsKey(引用) ? 符号("method", 引用.部件列()) + "(); " : "") + 状态值 + " = 2; }");
        }
        主体列列表.add(导出方法("java_entry", 条目分, true)); Set<String> 已导出名称 = new HashSet<>();
        for (String 赋值值 : 导出条目列) {
            int 位置索引 = 赋值值.indexOf('='); if (位置索引 < 1) throw new 翻译错误("发射值 赋值值 错误");
            String 名称 = 赋值值.substring(0, 位置索引); 已导出名称.add(名称); 主体列列表.add(导出方法(名称, 赋值值.substring(位置索引 + 1), false));
        }
        List<String> 字符串声明列 = new ArrayList<>();
        for (Map.Entry<String, String> 条目值 : 字符串值列.entrySet()) {
            String 文本 = 条目值.getKey(); StringBuilder 数组值 = new StringBuilder("static const word " + 条目值.getValue() + "[] = {" + 文本.length());
            for (int 序数索引 = 0; 序数索引 < 文本.length(); 序数索引++) 数组值.append(", ").append((int)文本.charAt(序数索引));
            字符串声明列.add(数组值.append("};").toString());
        }
        String 支持值 = Files.readString(资源路径.resolve("运行时支持.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(堆机器字个数));
        return 本地化已生成源代码(支持值 + String.join("\n", 字符串声明列) + "\n" + String.join("\n", 声明列列表) + "\n" + String.join("\n", 字段声明列) + "\n" + String.join("\n", 主体列列表) + "\n", 已导出名称, 通用表示法);
    }
    String 本地化已生成源代码(String 源代码, Set<String> 已导出名称, boolean 通用表示法) throws IOException {
        Map<String, String> 名称表 = new HashMap<>();
        for (String 行 : Files.readAllLines(资源路径.resolve("已生成名称列.tsv"), StandardCharsets.UTF_8)) {
            String[] 一对值 = 行.split("\t"); 名称表.put(一对值[0], 一对值[1]);
        }
        Pattern 块片表达式 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 查找器值 = 块片表达式.matcher(源代码); StringBuffer 结果 = new StringBuffer();
        while (查找器值.find()) {
            String 名称 = 查找器值.group(), 新建名称 = 名称;
            if (!名称.startsWith("//") && !名称.startsWith("/*") && !名称.startsWith("\"") && !名称.startsWith("'") && !已导出名称.contains(名称)) {
                新建名称 = 名称表.getOrDefault(名称, 名称);
                if (名称.matches("a[0-9]+")) 新建名称 = "实参" + 名称.substring(1);
                if (名称.matches("b[0-9]+")) 新建名称 = "分支" + 名称.substring(1);
                if (通用表示法) {
                    StringBuilder 表示法值 = new StringBuilder();
                    for (char 字符值 : 新建名称.toCharArray()) 表示法值.append(字符值 < 128 ? Character.toString(字符值) : String.format(Locale.ROOT, "\\u%04x", (int)字符值));
                    新建名称 = 表示法值.toString();
                }
            }
            查找器值.appendReplacement(结果, Matcher.quoteReplacement(新建名称));
        }
        查找器值.appendTail(结果); return 结果.toString();
    }
    String x86方法体(方法引用 函数, 成员数据 数据, Map<String,String> 计算机表, String 目标值) {
        String 标记值 = 符号("method", 函数.部件列());
        List<String> 行 = new ArrayList<>();
        if ((数据.存取条目 & 0x100) != 0) {
            String 连接 = 计算机表.get(函数.名称 + 函数.说明值);
            if (!函数.所有者值.equals(目标值.equals("kernel") ? "设备" : "用户") || 连接 == null) throw new 翻译错误("허용되지 않은 native 函数");
            return ".text\n" + 标记值 + ":\njmp " + 连接;
        }
        byte[] 主体文本 = 数据.属性值.get("Code"); if (主体文本 == null) throw new 翻译错误("函数 몸체가 缺失方法");
        数据读取器 读取器值 = new 数据读取器(主体文本); 读取器值.读取短整数(); int 局部个数 = 读取器值.读取短整数();
        数据读取器 命令数据 = new 数据读取器(读取器值.读取(读取器值.读取整数()));
        if (读取器值.读取短整数() != 0) throw new 翻译错误("try/catch/finally 是否不支持");
        方法描述符 格式值 = new 方法描述符(函数.说明值); if (局部个数 < 格式值.实参.size()) throw new 翻译错误("매개변수보다 적은 局部作用域 变量值");
        Collections.addAll(行,".text",".globl " + 标记值,".type " + 标记值 + ", @function",标记值 + ":","pushl %ebp","movl %esp, %ebp","subl $" + 局部个数 * 4 + ", %esp");
        for (int 序数索引 = 0; 序数索引 < 格式值.实参.size(); 序数索引++) Collections.addAll(行,"movl " + (8 + 4 * (格式值.实参.size() - 序数索引 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (序数索引 + 1)) + "(%ebp)");
        类数据 类值 = 类集列表.get(函数.所有者值); Set<Integer> 边界列列表 = new HashSet<>(), 分支列表 = new HashSet<>();
        String[] 比较列列表 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (命令数据.位置 < 命令数据.数据.length) {
            int 位置 = 命令数据.位置, 命令 = 命令数据.读取字节(); String 位置索引 = 标记值 + "_b" + 位置;
            行.add(位置索引 + ":"); 边界列列表.add(位置);
            if (命令 == 0) 行.add("nop");
            else if (命令 == 1) 行.add("pushl $0");
            else if (命令 >= 2 && 命令 <= 8) 行.add("pushl $" + (命令 - 3));
            else if (命令 == 16 || 命令 == 17) 行.add("pushl $" + (命令 == 16 ? 命令数据.读取有符号字节() : 命令数据.读取有符号短整数()));
            else if (命令 == 18 || 命令 == 19) {
                int 编号 = 命令 == 18 ? 命令数据.读取字节() : 命令数据.读取短整数();
                行.add("pushl $" + x86常量(类值,编号));
            } else if (命令 == 21 || 命令 == 25 || (命令 >= 26 && 命令 <= 29) || (命令 >= 42 && 命令 <= 45) || 命令 == 54 || 命令 == 58 || (命令 >= 59 && 命令 <= 62) || (命令 >= 75 && 命令 <= 78)) {
                boolean 读取结果 = 命令 < 54; int 编号 = 命令 == 21 || 命令 == 25 || 命令 == 54 || 命令 == 58 ? 命令数据.读取字节() : 命令 - (命令 <= 29 ? 26 : 命令 <= 45 ? 42 : 命令 <= 62 ? 59 : 75);
                检查局部(编号,局部个数); 行.add((读取结果 ? "pushl " : "popl ") + "-" + (4 * (编号 + 1)) + "(%ebp)");
            } else if (命令 == 46) Collections.addAll(行,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (命令 == 79) Collections.addAll(行,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (命令 == 87 || 命令 == 88) 行.add("addl $" + (命令 == 87 ? 4 : 8) + ", %esp");
            else if (命令 >= 89 && 命令 <= 95) {
                int[] 项目个数列 = {1,2,3,2,3,4,2}; int[][] 排序列表 = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 寄存器值列 = {"%eax","%ecx","%edx","%ebx"};
                for (int 序数索引 = 0; 序数索引 < 项目个数列[命令 - 89]; 序数索引++) 行.add("popl " + 寄存器值列[序数索引]);
                for (int 序数索引 : 排序列表[命令 - 89]) 行.add("pushl " + 寄存器值列[序数索引]);
            } else if (命令 == 96 || 命令 == 100 || 命令 == 104 || 命令 == 126 || 命令 == 128 || 命令 == 130) {
                String 操作值 = 命令 == 96 ? "addl" : 命令 == 100 ? "subl" : 命令 == 104 ? "imull" : 命令 == 126 ? "andl" : 命令 == 128 ? "orl" : "xorl";
                Collections.addAll(行,"popl %ecx","popl %eax",操作值 + " %ecx, %eax","pushl %eax");
            } else if (命令 == 108 || 命令 == 112) Collections.addAll(行,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + 位置索引 + "_divide","cmpl $0x80000000, %eax","jne " + 位置索引 + "_divide","xorl %edx, %edx","jmp " + 位置索引 + "_done",位置索引 + "_divide:","cltd","idivl %ecx",位置索引 + "_done:","pushl " + (命令 == 108 ? "%eax" : "%edx"));
            else if (命令 == 116) 行.add("negl (%esp)");
            else if (命令 == 120 || 命令 == 122 || 命令 == 124) Collections.addAll(行,"popl %ecx","popl %eax",(命令 == 120 ? "sall" : 命令 == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (命令 == 132) {
                int 编号 = 命令数据.读取字节(), 递增值 = 命令数据.读取有符号字节(); 检查局部(编号,局部个数); 行.add("addl $" + 递增值 + ", -" + (4 * (编号 + 1)) + "(%ebp)");
            } else if (命令 >= 145 && 命令 <= 147) Collections.addAll(行,"popl %eax",命令 == 145 ? "movsbl %al, %eax" : 命令 == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (命令 >= 153 && 命令 <= 166) {
                if (命令 <= 158) Collections.addAll(行,"popl %eax","testl %eax, %eax");
                else Collections.addAll(行,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int 目的地址值 = 位置 + 命令数据.读取有符号短整数(); 分支列表.add(目的地址值); 行.add(比较列列表[命令 - (命令 <= 158 ? 153 : 159)] + " " + 标记值 + "_b" + 目的地址值);
            } else if (命令 == 167 || 命令 == 200) {
                int 目的地址值 = 位置 + (命令 == 167 ? 命令数据.读取有符号短整数() : 命令数据.读取整数()); 分支列表.add(目的地址值); 行.add("jmp " + 标记值 + "_b" + 目的地址值);
            } else if (命令 == 170 || 命令 == 171) {
                while (命令数据.位置 % 4 != 0) 命令数据.读取字节();
                int 默认值 = 位置 + 命令数据.读取整数(); 分支列表.add(默认值); 行.add("popl %eax");
                int 项目个数, 底端值 = 0;
                if (命令 == 170) { 底端值 = 命令数据.读取整数(); int 顶端值 = 命令数据.读取整数(); long 长度 = (long)顶端值 - 底端值 + 1; if (长度 < 1 || 长度 > (命令数据.数据.length - 命令数据.位置) / 4) throw new 翻译错误("switch 裁剪 错误"); 项目个数 = (int)长度; }
                else { 项目个数 = 命令数据.读取整数(); if (项目个数 < 0 || 项目个数 > (命令数据.数据.length - 命令数据.位置) / 8) throw new 翻译错误("switch 大小 错误"); }
                for (int 序数索引 = 0; 序数索引 < 项目个数; 序数索引++) {
                    int 值 = 命令 == 170 ? 底端值 + 序数索引 : 命令数据.读取整数(), 目的地址值 = 位置 + 命令数据.读取整数(); 分支列表.add(目的地址值);
                    Collections.addAll(行,"cmpl $" + 值 + ", %eax","je " + 标记值 + "_b" + 目的地址值);
                }
                行.add("jmp " + 标记值 + "_b" + 默认值);
            } else if (命令 == 172 || 命令 == 176 || 命令 == 177) {
                if (命令 != 177) 行.add("popl %eax"); Collections.addAll(行,"leave","ret");
            } else if (命令 == 178 || 命令 == 179) {
                方法引用 引用 = 类值.引用(命令数据.读取短整数()); if (!字段列列表.containsKey(引用)) throw new 翻译错误("알 数 없는 字段值");
                Collections.addAll(行,"call " + 符号("init",引用.所有者值),(命令 == 178 ? "pushl " : "popl ") + 符号("field",引用.部件列()));
            } else if (命令 == 184) {
                方法引用 引用 = 类值.引用(命令数据.读取短整数()); if (!方法列列表.containsKey(引用)) throw new 翻译错误("알 数 없는 函数");
                方法描述符 调用状态类型 = new 方法描述符(引用.说明值); Collections.addAll(行,"call " + 符号("init",引用.所有者值),"call " + 符号("method",引用.部件列()));
                if (!调用状态类型.实参.isEmpty()) 行.add("addl $" + 调用状态类型.实参.size() * 4 + ", %esp");
                if (!调用状态类型.发回结果.equals("V")) 行.add("pushl %eax");
            } else if (命令 == 182) {
                方法引用 引用 = 类值.引用(命令数据.读取短整数());
                if (引用.equals(new 方法引用("java/lang/String","length","()I"))) Collections.addAll(行,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (引用.equals(new 方法引用("java/lang/String","charAt","(I)C"))) Collections.addAll(行,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new 翻译错误("가상 函数 调用 是否不支持");
            } else if (命令 == 188) {
                if (命令数据.读取字节() != 10) throw new 翻译错误("new int[]만 支持值"); Collections.addAll(行,"popl %eax","call rt_new_array","pushl %eax");
            } else if (命令 == 190) Collections.addAll(行,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (命令 == 196) {
                int 扩展名值 = 命令数据.读取字节(), 编号 = 命令数据.读取短整数(); 检查局部(编号,局部个数);
                if (扩展名值 == 21 || 扩展名值 == 25 || 扩展名值 == 54 || 扩展名值 == 58) 行.add((扩展名值 <= 25 ? "pushl " : "popl ") + "-" + 4 * (编号 + 1) + "(%ebp)");
                else if (扩展名值 == 132) 行.add("addl $" + 命令数据.读取有符号短整数() + ", -" + 4 * (编号 + 1) + "(%ebp)");
                else throw new 翻译错误("wide 命令 是否不支持");
            } else if (命令 == 198 || 命令 == 199) {
                int 目的地址值 = 位置 + 命令数据.读取有符号短整数(); 分支列表.add(目的地址值); Collections.addAll(行,"popl %eax","testl %eax, %eax",(命令 == 198 ? "je " : "jne ") + 标记值 + "_b" + 目的地址值);
            } else throw new 翻译错误("是否不支持 命令: " + 命令);
        }
        if (!边界列列表.containsAll(分支列表)) throw new 翻译错误("命令 경계가 아닌 곳으로 分支");
        行.add(".size " + 标记值 + ", .-" + 标记值); return String.join("\n",行);
    }
    String x86常量(类数据 数据, int 编号) {
        if (数据.常量种类[编号] == 3) return 数据.常量数据[编号].toString();
        if (数据.常量种类[编号] == 8) return 字符串符号(数据.字符((Integer)数据.常量数据[编号]));
        throw new 翻译错误("정수와 字符串 상수만 支持值");
    }
    String x86汇编(String 条目分, List<String> 已导出值, String 目标值) throws IOException {
        Map<String,String> 计算机表 = new HashMap<>();
        for (String 行 : Files.readAllLines(资源路径.resolve("x86机器函数.tsv"))) { String[] 一对值 = 行.split("\t"); if (一对值[0].equals(目标值)) 计算机表.put(一对值[1] + 一对值[2],一对值[3]); }
        int 位置索引 = 条目分.lastIndexOf('.'); if (位置索引 < 0) throw new 翻译错误("条目分 赋值值 错误");
        String 所有者值 = 条目分.substring(0,位置索引).replace('.','/'), 方法条目名称 = 条目分.substring(位置索引 + 1); 方法引用 条目分值 = null;
        for (String 说明值 : Arrays.asList("()I","()V")) { 方法引用 引用 = new 方法引用(所有者值,方法条目名称,说明值); if (方法列列表.containsKey(引用)) { if (条目分值 != null) throw new 翻译错误("겹친 条目分"); 条目分值 = 引用; } }
        if (条目分值 == null || (方法列列表.get(条目分值).存取条目 & 0x100) != 0) throw new 翻译错误("条目分值 函数 格式值 错误");
        List<String> 行 = new ArrayList<>(); 行.add(".code32");
        for (类数据 数据 : 类集列表.values()) {
            String 状态值 = 符号("state",数据.名称), 初始化 = 符号("init",数据.名称);
            Collections.addAll(行,".bss",".balign 4",状态值 + ": .long 0",".text",初始化 + ":","cmpl $0, " + 状态值,"jne " + 初始化 + "_done","movl $1, " + 状态值);
            方法引用 初始设定器引用 = new 方法引用(数据.名称,"<clinit>","()V"); if (方法列列表.containsKey(初始设定器引用)) 行.add("call " + 符号("method",初始设定器引用.部件列()));
            Collections.addAll(行,"movl $2, " + 状态值,初始化 + "_done:","ret");
            for (成员数据 字段值 : 数据.字段值) {
                byte[] 常量值 = 字段值.属性值.get("ConstantValue"); String 值 = 常量值 == null ? "0" : x86常量(数据,new 数据读取器(常量值).读取短整数());
                Collections.addAll(行,".data",".balign 4",符号("field",数据.名称,字段值.名称,字段值.说明值) + ": .long " + 值);
            }
            for (成员数据 函数 : 数据.函数) if (!函数.名称.equals("<init>")) 行.add(x86方法体(new 方法引用(数据.名称,函数.名称,函数.说明值),函数,计算机表,目标值));
        }
        Collections.addAll(行,".text",".globl java_entry","java_entry:","call " + 符号("init",条目分值.所有者值),"call " + 符号("method",条目分值.部件列()));
        if (条目分值.说明值.equals("()V")) 行.add("xorl %eax, %eax"); 行.add("ret");
        for (String 赋值值 : 已导出值) {
            int 分隔符值 = 赋值值.indexOf('='); if (分隔符值 < 1) throw new 翻译错误("发射值 赋值值 错误");
            String 外部值 = 赋值值.substring(0,分隔符值), 函数 = 赋值值.substring(分隔符值 + 1); int 除法结果 = 函数.lastIndexOf('.');
            if (除法结果 < 0 || !外部值.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new 翻译错误("发射值 符号 错误");
            String 类值 = 函数.substring(0,除法结果).replace('.','/'), 名称 = 函数.substring(除法结果 + 1); 方法引用 选中状态值 = null;
            for (方法引用 引用 : 方法列列表.keySet()) if (引用.所有者值.equals(类值) && 引用.名称.equals(名称)) { if (选中状态值 != null) throw new 翻译错误("겹친 发射值 目标值"); 选中状态值 = 引用; }
            if (选中状态值 == null) throw new 翻译错误("내보낼 함수가 缺失方法");
            Collections.addAll(行,".text",".globl " + 外部值,外部值 + ":","call " + 符号("init",选中状态值.所有者值),"jmp " + 符号("method",选中状态值.部件列()));
        }
        行.add(".section .rodata");
        for (Map.Entry<String,String> 条目值 : 字符串值列.entrySet()) {
            Collections.addAll(行,".balign 4",条目值.getValue() + ":",".long " + 条目值.getKey().length());
            List<String> 单位列列表 = new ArrayList<>(); for (char 单位值 : 条目值.getKey().toCharArray()) 单位列列表.add(Integer.toString(单位值)); if (!单位列列表.isEmpty()) 行.add(".long " + String.join(",",单位列列表));
        }
        行.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",行) + "\n";
    }
    static void 执行工具(List<String> 命令) throws Exception {
        if (new ProcessBuilder(命令).inheritIO().start().waitFor() != 0) throw new 翻译错误("编译源代码 错误: " + 命令.get(0));
    }
    static String 数据字符串(String 文本) { return "\"" + 文本.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void x86编译结果(List<Path> 输入列表, String 目标值, String 条目分, List<String> 已导出值, Path 输出, Path 资源值) throws Exception {
        Path 临时值 = Files.createTempDirectory("jkoros-java-x86-"), 类路径 = 临时值.resolve("classes"); Files.createDirectory(类路径);
        try {
            List<String> Java命令 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",类路径.toString(),"-sourcepath",类路径.toString(),"-d",类路径.toString()));
            List<Path> 字节码 = new ArrayList<>(); int 源代码个数 = 0;
            for (Path 输入值 : 输入列表) {
                if (输出.toAbsolutePath().normalize().equals(输入值.toAbsolutePath().normalize())) throw new 翻译错误("输出 파일과 입력이 相等文本");
                if (输入值.toString().endsWith(".java")) { Java命令.add(输入值.toString()); 源代码个数++; }
                else if (输入值.toString().endsWith(".class")) 字节码.add(输入值);
                else throw new 翻译错误(".java 또는 .class만 支持值");
            }
            if (源代码个数 > 0) 执行工具(Java命令);
            try (java.util.stream.Stream<Path> 路径列表 = Files.walk(类路径)) { 路径列表.filter(路径 -> 路径.toString().endsWith(".class")).sorted().forEach(字节码::add); }
            提前所属时间编译器 转换值 = new 提前所属时间编译器(字节码,目标值.equals("user") ? "user" : "kernel",262144,资源值);
            String 组装值 = 转换值.x86汇编(条目分,已导出值,目标值); Files.writeString(临时值.resolve("program.s"),组装值,StandardCharsets.UTF_8);
            Path 工具位置 = 资源值.getParent();
            执行工具(Arrays.asList("as","--32","-o",临时值.resolve("program.o").toString(),临时值.resolve("program.s").toString()));
            执行工具(Arrays.asList("as","--32","-o",临时值.resolve("runtime.o").toString(),工具位置.resolve("运行时支持.s").toString()));
            List<String> 连接 = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (目标值.equals("kernel")) 连接.add("-r");
            else {
                执行工具(Arrays.asList("as","--32","-o",临时值.resolve("start.o").toString(),工具位置.resolve(目标值.equals("user") ? "开始用户程序.s" : "Linux启动.s").toString()));
                Collections.addAll(连接,"-e","_start",临时值.resolve("start.o").toString());
                if (目标值.equals("user")) Collections.addAll(连接,"-T",工具位置.resolve("用户连接导航.ld").toString());
            }
            Collections.addAll(连接,"-o",临时值.resolve("result").toString(),临时值.resolve("program.o").toString(),临时值.resolve("runtime.o").toString()); 执行工具(连接);
            输出 = 输出.toAbsolutePath(); Files.createDirectories(输出.getParent()); Path 发布值 = Files.createTempFile(输出.getParent(),".elf-",".tmp");
            try { Files.copy(临时值.resolve("result"),发布值,StandardCopyOption.REPLACE_EXISTING); Files.move(发布值,输出,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(发布值); }
            Files.setPosixFilePermissions(输出,java.nio.file.attribute.PosixFilePermissions.fromString(目标值.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(输出 + ".s"),组装值,StandardCharsets.UTF_8);
            List<String> 符号数据 = new ArrayList<>(), 源代码数据 = new ArrayList<>();
            for (方法引用 引用 : 转换值.方法列列表.keySet()) 符号数据.add(数据字符串(符号("method",引用.部件列())) + ":" + 数据字符串(引用.所有者值 + "." + 引用.名称 + 引用.说明值));
            for (Path 输入值 : 输入列表) {
                byte[] 哈希文件 = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(输入值)); StringBuilder 文本 = new StringBuilder(); for (byte 值 : 哈希文件) 文本.append(String.format(Locale.ROOT,"%02x",值 & 255));
                源代码数据.add(数据字符串(输入值.toAbsolutePath().toString()) + ":" + 数据字符串(文本.toString()));
            }
            Files.writeString(Paths.get(输出 + ".json"),"{\"target\":" + 数据字符串(目标值) + ",\"entry\":" + 数据字符串(条目分) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",符号数据) + "},\"sources\":{" + String.join(",",源代码数据) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> 路径列表 = Files.walk(临时值)) { for (Path 路径 : (Iterable<Path>)路径列表.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(路径); }
        }
    }
    public static void main(String[] 实参) {
        try {
            String 条目分 = null, 目标值 = "kernel", x86目标 = null; Path 输出路径 = null; int 词法用机器字个数 = 262144; boolean 通用表示法 = false;
            List<String> 已导出值 = new ArrayList<>(); List<Path> 路径列表 = new ArrayList<>();
            for (int 序数索引 = 0; 序数索引 < 实参.length; 序数索引++) {
                String 值 = 实参[序数索引];
                switch (值) {
                    case "--target": x86目标 = 实参[++序数索引]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry 类值.函数 -o 输出 [--target linux|kernel|user] [--profile kernel|user] [--export 符号=类值.函数] 클래스파일 또는 Java원문"); return;
                    case "--entry": 条目分 = 实参[++序数索引]; break;
                    case "--profile": 目标值 = 实参[++序数索引]; break;
                    case "--heap-words": 词法用机器字个数 = Integer.parseInt(实参[++序数索引]); break;
                    case "--export": 已导出值.add(实参[++序数索引]); break;
                    case "-o": 输出路径 = Paths.get(实参[++序数索引]); break;
                    case "--ucn": 通用表示法 = true; break;
                    default: if (值.startsWith("-")) throw new 翻译错误("알 数 없는 옵션: " + 值); 路径列表.add(Paths.get(值));
                }
            }
            if (条目分 == null || 输出路径 == null || 路径列表.isEmpty()) throw new 翻译错误("--entry, -o, 类值 파일이 필요합니다");
            Path 资源值 = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (x86目标 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(x86目标)) throw new 翻译错误("알 数 없는 执行命令 目标值");
                x86编译结果(路径列表,x86目标,条目分,已导出值,输出路径,资源值); return;
            }
            String 源代码 = new 提前所属时间编译器(路径列表, 目标值, 词法用机器字个数, 资源值).生成(条目分, 已导出值, 通用表示法);
            输出路径 = 输出路径.toAbsolutePath(); Files.createDirectories(输出路径.getParent());
            Path 临时值 = Files.createTempFile(输出路径.getParent(), ".aot-", ".tmp");
            try { Files.writeString(临时值, 源代码, StandardCharsets.UTF_8); Files.move(临时值, 输出路径, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(临时值); }
        } catch (Exception 错误) { System.err.println("编译源代码 错误: " + 错误.getMessage()); System.exit(1); }
    }
}
