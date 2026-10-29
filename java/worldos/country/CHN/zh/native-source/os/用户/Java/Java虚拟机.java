// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 在 ring 3 运行的受限 JVM；执行时检查文件、栈、引用和分支边界。 */
public final class Java虚拟机 {
    static int[] 文件 = new int[16384], 文件名称文本 = new int[64];
    static int[] 常量标签 = new int[512], 常量首位值 = new int[512], 常量第二值 = new int[512], 字符串引用 = new int[512];
    static int[] 方法名称文本 = new int[32], 方法类型 = new int[32], 方法存取 = new int[32];
    static int[] 方法开始 = new int[32], 方法结束 = new int[32], 方法栈 = new int[32], 方法局部变量列 = new int[32];
    static int[] 方法参数个数 = new int[32], 方法参数类型 = new int[512], 方法发回 = new int[32];
    static int[] 边界位置值 = new int[16384];
    static int[] 局部值 = new int[4096], 局部类型 = new int[4096], 操作数栈值 = new int[4096], 操作数栈类型 = new int[4096];
    static int[] 帧方法 = new int[32], 帧位置 = new int[32], 帧栈 = new int[32];
    static int[] 堆值 = new int[8192];
    static int 大小, 读取位置, 常量个数, 方法个数, 类名称, 帧索引 = -1, 堆结束位置 = 1, 发回类型;
    static boolean 错误;

    static void 失败值(String 机器字文本) {
        if (!错误) { 用户.写入("JVM error: "); 用户.写入(机器字文本); 用户.写入字符值(10); }
        错误 = true;
    }
    static boolean 裁剪(int 运行, int 长度) { return 运行 >= 0 && 长度 >= 0 && 运行 <= 大小 - 长度; }
    static int 字节值() {
        if (!裁剪(读取位置, 1)) { 失败值("truncated class file"); return 0; }
        return 文件[读取位置++];
    }
    static int 短整数值() { return 字节值() << 8 | 字节值(); }
    static int 整数() { return 短整数值() << 16 | 短整数值(); }
    static void 跳过字节列(int 长度) { if (!裁剪(读取位置, 长度)) 失败值("invalid attribute size"); else 读取位置 += 长度; }
    static boolean 检查常量(int 数, int 种类值) {
        if (数 <= 0 || 数 >= 常量个数 || 常量标签[数] != 种类值) { 失败值("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 文本范围(int 运行, int 长度, String 机器字文本) {
        if (!裁剪(运行, 长度) || 长度 != 机器字文本.length()) return false;
        for (int 数 = 0; 数 < 长度; 数++) if (文件[运行 + 数] != 机器字文本.charAt(数)) return false;
        return true;
    }
    static boolean 机器字文本(int 常量值, String 机器字文本) { return 检查常量(常量值, 1) && 文本范围(常量首位值[常量值], 常量第二值[常量值], 机器字文本); }
    static boolean 匹配中机器字(int 首位操作数, int 第二操作数) {
        if (!检查常量(首位操作数, 1) || !检查常量(第二操作数, 1) || 常量第二值[首位操作数] != 常量第二值[第二操作数]) return false;
        for (int 数 = 0; 数 < 常量第二值[首位操作数]; 数++) if (文件[常量首位值[首位操作数] + 数] != 文件[常量首位值[第二操作数] + 数]) return false;
        return true;
    }
    static int 类名称文本(int 数) { return 检查常量(数, 7) && 检查常量(常量首位值[数], 1) ? 常量首位值[数] : 0; }
    static int 引用名称(int 数) { return 检查常量(数, 12) && 检查常量(常量首位值[数], 1) ? 常量首位值[数] : 0; }
    static int 引用类型(int 数) { return 检查常量(数, 12) && 检查常量(常量第二值[数], 1) ? 常量第二值[数] : 0; }
    static int 描述符类型(int 结尾, boolean 空类型) {
        if (读取位置 >= 结尾) { 失败值("invalid descriptor"); return 0; }
        int 值 = 字节值();
        if (值 == 'V' && 空类型) return 0;
        if (值 == 'I' || 值 == 'B' || 值 == 'C' || 值 == 'S' || 值 == 'Z') return 1;
        if (值 == '[') { 描述符类型(结尾, false); return 2; }
        if (值 == 'L') {
            int 运行 = 读取位置;
            while (读取位置 < 结尾 && 文件[读取位置] != ';') 读取位置++;
            if (读取位置 == 结尾 || 读取位置 == 运行) 失败值("invalid reference descriptor");
            else 读取位置++;
            return 2;
        }
        失败值("unsupported descriptor type"); return 0;
    }
    static void 读取描述符(int 函数) {
        int 上一个项目 = 读取位置, 数 = 方法类型[函数];
        if (!检查常量(数, 1)) return;
        读取位置 = 常量首位值[数]; int 结尾 = 读取位置 + 常量第二值[数];
        if (字节值() != '(') 失败值("invalid method descriptor");
        int 项目个数 = 0;
        while (!错误 && 读取位置 < 结尾 && 文件[读取位置] != ')') {
            if (项目个数 == 16) { 失败值("too many method arguments"); break; }
            方法参数类型[函数 * 16 + 项目个数++] = 描述符类型(结尾, false);
        }
        if (读取位置 >= 结尾 || 字节值() != ')') 失败值("invalid method descriptor");
        方法发回[函数] = 描述符类型(结尾, true); 方法参数个数[函数] = 项目个数;
        if (读取位置 != 结尾) 失败值("invalid method descriptor");
        读取位置 = 上一个项目;
    }
    static void 跳过属性() {
        int 项目个数 = 短整数值();
        for (int 数 = 0; 数 < 项目个数 && !错误; 数++) { 检查常量(短整数值(), 1); 跳过字节列(整数()); }
    }
    static int 命令长度(int 值) {
        if (值 == 16 || 值 == 18 || 值 == 21 || 值 == 25 || 值 == 54 || 值 == 58 || 值 == 188) return 2;
        if (值 == 17 || 值 == 19 || 值 == 132 || 值 >= 153 && 值 <= 167
            || 值 >= 178 && 值 <= 184 || 值 == 187 || 值 == 189 || 值 == 192 || 值 == 198 || 值 == 199) return 3;
        if (值 >= 0 && 值 <= 8 || 值 >= 26 && 值 <= 29 || 值 >= 42 && 值 <= 46 || 值 == 50
            || 值 >= 59 && 值 <= 62 || 值 >= 75 && 值 <= 79 || 值 == 83 || 值 == 87 || 值 == 89 || 值 == 95
            || 值 == 96 || 值 == 100 || 值 == 104 || 值 == 108 || 值 == 112 || 值 == 116
            || 值 == 120 || 值 == 122 || 值 == 124 || 值 == 126 || 值 == 128 || 值 == 130
            || 值 >= 145 && 值 <= 147 || 值 == 172 || 值 == 176 || 值 == 177 || 值 == 190) return 1;
        return 0;
    }
    static void 读取类() {
        if (整数() != 0xcafebabe) 失败值("not a class file");
        int 次版本修订 = 短整数值(), 版本值 = 短整数值();
        if (版本值 < 45 || 版本值 > 52 || 次版本修订 != 0) 失败值("supported class versions: 45..52, minor 0");
        常量个数 = 短整数值();
        if (常量个数 < 1 || 常量个数 > 512) { 失败值("constant pool limit (511)"); return; }
        for (int 数 = 1; 数 < 常量个数 && !错误; 数++) {
            int 种类值 = 字节值(); 常量标签[数] = 种类值;
            if (种类值 == 1) { 常量第二值[数] = 短整数值(); 常量首位值[数] = 读取位置; 跳过字节列(常量第二值[数]); }
            else if (种类值 == 3) 常量首位值[数] = 整数();
            else if (种类值 == 7 || 种类值 == 8) 常量首位值[数] = 短整数值();
            else if (种类值 == 9 || 种类值 == 10 || 种类值 == 12) { 常量首位值[数] = 短整数值(); 常量第二值[数] = 短整数值(); }
            else 失败值("unsupported constant type");
        }
        int 权限值 = 短整数值();
        if ((权限值 & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) 失败值("unsupported class flags");
        类名称 = 类名称文本(短整数值());
        if (!机器字文本(类名称文本(短整数值()), "java/lang/Object")) 失败值("inheritance unsupported");
        if (短整数值() != 0) 失败值("interfaces unsupported");
        if (短整数值() != 0) 失败值("fields unsupported");
        方法个数 = 短整数值();
        if (方法个数 < 1 || 方法个数 > 32) { 失败值("method count limit (32)"); return; }
        for (int 数 = 0; 数 < 方法个数 && !错误; 数++) {
            方法存取[数] = 短整数值(); 方法名称文本[数] = 短整数值(); 方法类型[数] = 短整数值();
            检查常量(方法名称文本[数], 1); 读取描述符(数);
            if ((方法存取[数] & (0x100 | 0x400 | 0x20)) != 0) 失败值("native, abstract and synchronized methods unsupported");
            if ((方法存取[数] & 8) == 0 && !机器字文本(方法名称文本[数], "<init>")) 失败值("instance methods unsupported");
            if (机器字文本(方法名称文本[数], "<clinit>")) 失败值("class initializers unsupported");
            for (int 前端值 = 0; 前端值 < 数; 前端值++) if (匹配中机器字(方法名称文本[前端值], 方法名称文本[数]) && 匹配中机器字(方法类型[前端值], 方法类型[数])) 失败值("duplicate method");
            int 项目个数 = 短整数值();
            for (int 属性值 = 0; 属性值 < 项目个数 && !错误; 属性值++) {
                int 名称 = 短整数值(), 长度 = 整数(), 运行 = 读取位置;
                if (!裁剪(运行, 长度)) { 失败值("truncated method attribute"); break; }
                if (机器字文本(名称, "Code")) {
                    if (方法开始[数] != 0) 失败值("duplicate Code attribute");
                    方法栈[数] = 短整数值(); 方法局部变量列[数] = 短整数值(); int 代码长度 = 整数();
                    if (方法栈[数] > 128 || 方法局部变量列[数] > 128 || 方法局部变量列[数] < 方法参数个数[数]
                        || 代码长度 < 1 || 代码长度 > 8192) 失败值("method memory limits exceeded");
                    方法开始[数] = 读取位置; 跳过字节列(代码长度); 方法结束[数] = 读取位置;
                    if (短整数值() != 0) 失败值("exception handlers unsupported");
                    跳过属性();
                    if (读取位置 != 运行 + 长度) 失败值("Code attribute size mismatch");
                } else 跳过字节列(长度);
            }
            if (方法开始[数] == 0) 失败值("missing Code attribute");
            int 槽条目 = 方法开始[数];
            while (槽条目 < 方法结束[数] && !错误) {
                int 长度 = 命令长度(文件[槽条目]);
                if (长度 == 0 || 长度 > 方法结束[数] - 槽条目) { 失败值("unsupported or truncated bytecode"); break; }
                边界位置值[槽条目] = 数 + 1; 槽条目 += 长度;
            }
            // 即使在不执行的路径上，也拒绝无效的分支目标。
            槽条目 = 方法开始[数];
            while (槽条目 < 方法结束[数] && !错误) {
                int 值 = 文件[槽条目];
                if (值 >= 153 && 值 <= 167 || 值 == 198 || 值 == 199) {
                    int 目的地址值 = 槽条目 + (short)(文件[槽条目 + 1] << 8 | 文件[槽条目 + 2]);
                    if (目的地址值 < 方法开始[数] || 目的地址值 >= 方法结束[数] || 边界位置值[目的地址值] != 数 + 1) 失败值("invalid branch target");
                }
                槽条目 += 命令长度(值);
            }
        }
        if (!错误) 跳过属性();
        if (读取位置 != 大小) 失败值("extra class file data");
    }
    static int 分配存储装置(int 种类值, int 长度) {
        if (长度 < 0 || 长度 > 堆值.length - 堆结束位置 - 2) { 失败值("object heap exhausted or negative array size"); return 0; }
        int 引用 = 堆结束位置; 堆结束位置 += 长度 + 2; 堆值[引用] = 种类值; 堆值[引用 + 1] = 长度;
        return 引用;
    }
    static boolean 对象值(int 引用, int 种类值) {
        if (引用 < 1 || 引用 >= 堆结束位置 - 1 || 堆值[引用] != 种类值) { 失败值("null or invalid object reference"); return false; }
        return true;
    }
    static int 常量文本(int 编号) {
        if (!检查常量(编号, 1)) return 0;
        if (字符串引用[编号] != 0) return 字符串引用[编号];
        int 引用 = 分配存储装置(1, 常量第二值[编号]); if (错误) return 0;
        int 结尾 = 常量首位值[编号] + 常量第二值[编号], 数 = 常量首位值[编号], 长度 = 0;
        while (数 < 结尾 && !错误) {
            int 值 = 文件[数++];
            if (值 == 0) 失败值("invalid modified UTF-8");
            else if (值 >= 192 && 值 <= 223 && 数 < 结尾) {
                int 下一项目 = 文件[数++];
                if ((下一项目 & 192) != 128) 失败值("invalid modified UTF-8");
                值 = (值 & 31) << 6 | 下一项目 & 63;
                if (值 != 0 && 值 < 128) 失败值("overlong modified UTF-8");
            } else if (值 >= 224 && 值 <= 239 && 数 + 1 < 结尾) {
                int 首位操作数 = 文件[数++], 第二操作数 = 文件[数++];
                if ((首位操作数 & 192) != 128 || (第二操作数 & 192) != 128) 失败值("invalid modified UTF-8");
                值 = (值 & 15) << 12 | (首位操作数 & 63) << 6 | 第二操作数 & 63;
                if (值 < 2048) 失败值("overlong modified UTF-8");
            } else if (值 >= 128) 失败值("invalid modified UTF-8");
            堆值[引用 + 2 + 长度++] = 值;
        }
        堆值[引用 + 1] = 长度; 字符串引用[编号] = 引用; return 引用;
    }
    static int 宿主字符(String 值) {
        int 引用 = 分配存储装置(1, 值.length()); if (错误) return 0;
        for (int 数 = 0; 数 < 值.length(); 数++) 堆值[引用 + 2 + 数] = 值.charAt(数);
        return 引用;
    }
    static void 写入文本(int 引用) {
        if (引用 == 0) { 用户.写入("null"); return; }
        if (!对象值(引用, 1)) return;
        for (int 数 = 0; 数 < 堆值[引用 + 1]; 数++) 用户.写入字符值(堆值[引用 + 2 + 数]);
    }
    static int 数字字符(int 值) {
        int 引用 = 分配存储装置(1, 11); if (错误) return 0;
        int 长度 = 0;
        if (值 < 0) 堆值[引用 + 2 + 长度++] = '-'; else 值 = -值;
        int 位置索引 = 1000000000; boolean 运行 = false;
        while (位置索引 != 0) {
            int 数 = -(值 / 位置索引);
            if (数 != 0 || 运行 || 位置索引 == 1) { 堆值[引用 + 2 + 长度++] = '0' + 数; 运行 = true; }
            值 %= 位置索引; 位置索引 /= 10;
        }
        堆值[引用 + 1] = 长度; return 引用;
    }
    static int 解码整数(int 引用) {
        if (!对象值(引用, 1)) return 0;
        int 长度 = 堆值[引用 + 1], 数 = 0, 值 = 0; boolean 负数值 = false;
        if (长度 > 0 && (堆值[引用 + 2] == '-' || 堆值[引用 + 2] == '+')) { 负数值 = 堆值[引用 + 2] == '-'; 数++; }
        if (数 == 长度) 失败值("NumberFormatException");
        for (; 数 < 长度 && !错误; 数++) {
            int 数字值 = 堆值[引用 + 2 + 数] - '0';
            if (数字值 < 0 || 数字值 > 9 || 值 < -214748364 || 值 == -214748364 && 数字值 > (负数值 ? 8 : 7)) 失败值("NumberFormatException");
            值 = 值 * 10 - 数字值;
        }
        return 负数值 ? 值 : -值;
    }
    static void 放入值(int 值, int 类型值) {
        if (错误) return;
        if (帧索引 < 0 || 帧栈[帧索引] >= 方法栈[帧方法[帧索引]]) { 失败值("operand stack overflow"); return; }
        int 槽条目 = 帧索引 * 128 + 帧栈[帧索引]++; 操作数栈值[槽条目] = 值; 操作数栈类型[槽条目] = 类型值;
    }
    static int 减法值列(int 类型值) {
        if (错误) return 0;
        if (帧索引 < 0 || 帧栈[帧索引] < 1) { 失败值("operand stack underflow"); return 0; }
        int 槽条目 = 帧索引 * 128 + --帧栈[帧索引]; 发回类型 = 操作数栈类型[槽条目];
        if (类型值 != 0 && 发回类型 != 类型值) 失败值("operand type mismatch");
        return 操作数栈值[槽条目];
    }
    static void 读取局部(int 编号, int 类型值) {
        if (编号 >= 方法局部变量列[帧方法[帧索引]] || 编号 < 0 || 局部类型[帧索引 * 128 + 编号] != 类型值) { 失败值("invalid or uninitialized local"); return; }
        放入值(局部值[帧索引 * 128 + 编号], 类型值);
    }
    static void 写入局部(int 编号, int 类型值) {
        if (编号 >= 方法局部变量列[帧方法[帧索引]] || 编号 < 0) { 失败值("local index out of range"); return; }
        int 值 = 减法值列(类型值); 局部值[帧索引 * 128 + 编号] = 值; 局部类型[帧索引 * 128 + 编号] = 类型值;
    }
    static int 读取操作码字节() {
        int 位置 = 帧位置[帧索引];
        if (位置 < 方法开始[帧方法[帧索引]] || 位置 >= 方法结束[帧方法[帧索引]]) { 失败值("instruction pointer out of range"); return 0; }
        帧位置[帧索引]++; return 文件[位置];
    }
    static int 读取操作码短整数() { return 读取操作码字节() << 8 | 读取操作码字节(); }
    static void 移动值(int 位置) {
        int 函数 = 帧方法[帧索引];
        if (位置 < 方法开始[函数] || 位置 >= 方法结束[函数] || 边界位置值[位置] != 函数 + 1) 失败值("invalid branch target");
        else 帧位置[帧索引] = 位置;
    }
    static void 调用(int 函数) {
        if (帧索引 == 31) { 失败值("call stack limit (32)"); return; }
        int 下一项目 = 帧索引 + 1;
        for (int 数 = 0; 数 < 128; 数++) 局部类型[下一项目 * 128 + 数] = 0;
        for (int 数 = 方法参数个数[函数] - 1; 数 >= 0; 数--) {
            局部值[下一项目 * 128 + 数] = 减法值列(方法参数类型[函数 * 16 + 数]); 局部类型[下一项目 * 128 + 数] = 方法参数类型[函数 * 16 + 数];
        }
        帧索引 = 下一项目; 帧方法[帧索引] = 函数; 帧位置[帧索引] = 方法开始[函数]; 帧栈[帧索引] = 0;
    }
    static void 发回结果(int 类型值) {
        if (类型值 != 方法发回[帧方法[帧索引]]) { 失败值("return type mismatch"); return; }
        int 值 = 类型值 == 0 ? 0 : 减法值列(类型值);
        帧索引--; if (帧索引 >= 0 && 类型值 != 0) 放入值(值, 类型值);
    }
    static int[] 流文件名称 = new int[64];
    static void 文件流调用(int 所有者值, int 名称, int 格式值, int 命令) {
        boolean 输出 = 机器字文本(所有者值, "java/io/FileOutputStream");
        int 种类值 = 输出 ? 6 : 5;
        if (命令 == 183 && 机器字文本(名称, "<init>")) {
            boolean 继续状态值 = false;
            if (输出 && 机器字文本(格式值, "(Ljava/lang/String;Z)V")) 继续状态值 = 减法值列(1) != 0;
            else if (!机器字文本(格式值, "(Ljava/lang/String;)V")) { 失败值("unsupported file stream constructor"); return; }
            int 文件条目名称 = 减法值列(2), 流值 = 减法值列(2);
            if (!对象值(文件条目名称, 1) || !对象值(流值, 种类值) || 错误) return;
            if (堆值[流值 + 3] != 0) { 失败值("file stream already initialized"); return; }
            int 长度 = 堆值[文件条目名称 + 1];
            if (长度 < 1 || 长度 > 63) { 失败值("invalid file name length"); return; }
            for (int 槽条目 = 0; 槽条目 < 长度; 槽条目++) {
                int 值 = 堆值[文件条目名称 + 2 + 槽条目];
                if (值 < 1 || 值 > 127) { 失败值("file stream paths currently require ASCII"); return; }
                流文件名称[槽条目] = 值;
            }
            流文件名称[长度] = 0;
            int 描述符条目 = 用户.打开文件描述符(流文件名称, 输出 ? (继续状态值 ? 1089 : 577) : 0);
            if (描述符条目 < 0) { 失败值("FileNotFoundException: file open failed"); return; }
            堆值[流值 + 2] = 描述符条目; 堆值[流值 + 3] = 1;
            return;
        }
        if (命令 != 182) { 失败值("invalid file stream invocation"); return; }
        int 动作 = -1, 值 = 0;
        if (机器字文本(名称, "close") && 机器字文本(格式值, "()V")) 动作 = 0;
        if (!输出 && 机器字文本(名称, "read") && 机器字文本(格式值, "()I")) 动作 = 1;
        if (输出 && 机器字文本(名称, "write") && 机器字文本(格式值, "(I)V")) { 动作 = 2; 值 = 减法值列(1); }
        if (动作 < 0) { 失败值("unsupported file stream method"); return; }
        int 流值 = 减法值列(2);
        if (!对象值(流值, 种类值) || 错误) return;
        if (堆值[流值 + 3] == 0) { 失败值("uninitialized file stream"); return; }
        int 描述符条目 = 堆值[流值 + 2];
        if (动作 == 0) {
            if (描述符条目 >= 0 && 用户.关闭文件描述符(描述符条目) < 0) 失败值("IOException: close failed");
            堆值[流值 + 2] = -1; return;
        }
        if (描述符条目 < 0) { 失败值("IOException: stream closed"); return; }
        if (动作 == 1) {
            int 结果 = 用户.读取一文件字节(描述符条目);
            if (结果 < -1) 失败值("IOException: read failed"); else 放入值(结果, 1);
        } else if (用户.写入一文件字节(描述符条目, 值) != 1) 失败值("IOException: write failed");
    }
    static void 调用方法(int 编号, int 命令) {
        if (!检查常量(编号, 10)) return;
        int 所有者值 = 类名称文本(常量首位值[编号]), 名称 = 引用名称(常量第二值[编号]), 格式值 = 引用类型(常量第二值[编号]);
        if (错误) return;
        if (匹配中机器字(所有者值, 类名称)) {
            if (命令 != 184) { 失败值("only static user methods are supported"); return; }
            for (int 数 = 0; 数 < 方法个数; 数++) if (匹配中机器字(名称, 方法名称文本[数]) && 匹配中机器字(格式值, 方法类型[数])) {
                if ((方法存取[数] & 8) == 0) 失败值("method is not static"); else 调用(数);
                return;
            }
            失败值("NoSuchMethodError"); return;
        }
        if (机器字文本(所有者值, "java/io/FileInputStream") || 机器字文本(所有者值, "java/io/FileOutputStream")) {
            文件流调用(所有者值, 名称, 格式值, 命令); return;
        }
        if (命令 == 184 && 机器字文本(所有者值, "java/lang/Integer") && 机器字文本(名称, "parseInt") && 机器字文本(格式值, "(Ljava/lang/String;)I")) {
            放入值(解码整数(减法值列(2)), 1); return;
        }
        if (命令 == 182 && 机器字文本(所有者值, "java/io/PrintStream") && (机器字文本(名称, "println") || 机器字文本(名称, "print"))) {
            int 类型值 = 0, 值 = 0;
            if (机器字文本(格式值, "(I)V")) { 类型值 = 1; 值 = 减法值列(1); }
            else if (机器字文本(格式值, "(Z)V")) { 类型值 = 2; 值 = 减法值列(1); }
            else if (机器字文本(格式值, "(C)V")) { 类型值 = 3; 值 = 减法值列(1); }
            else if (机器字文本(格式值, "(Ljava/lang/String;)V")) { 类型值 = 4; 值 = 减法值列(2); }
            else if (!机器字文本(格式值, "()V") || !机器字文本(名称, "println")) 失败值("unsupported print descriptor");
            if (减法值列(2) != -1) 失败值("invalid PrintStream receiver");
            if (错误) return;
            if (类型值 == 1) Java工具.写入编号(值);
            if (类型值 == 2) 用户.写入(值 == 0 ? "false" : "true");
            if (类型值 == 3) 用户.写入字符值(值 & 65535);
            if (类型值 == 4) 写入文本(值);
            if (机器字文本(名称, "println")) 用户.写入字符值(10);
            return;
        }
        if (命令 == 182 && 机器字文本(所有者值, "java/lang/String")) {
            if (机器字文本(名称, "length") && 机器字文本(格式值, "()I")) {
                int 引用 = 减法值列(2); if (对象值(引用, 1)) 放入值(堆值[引用 + 1], 1); return;
            }
            if (机器字文本(名称, "charAt") && 机器字文本(格式值, "(I)C")) {
                int 下标值 = 减法值列(1), 引用 = 减法值列(2);
                if (对象值(引用, 1)) {
                    if (下标值 < 0 || 下标值 >= 堆值[引用 + 1]) 失败值("StringIndexOutOfBoundsException"); else 放入值(堆值[引用 + 2 + 下标值], 1);
                }
                return;
            }
        }
        if (机器字文本(所有者值, "java/lang/StringBuilder")) {
            if (命令 == 183 && 机器字文本(名称, "<init>") && 机器字文本(格式值, "()V")) { 对象值(减法值列(2), 4); return; }
            if (命令 == 182 && 机器字文本(名称, "toString") && 机器字文本(格式值, "()Ljava/lang/String;")) {
                int 引用 = 减法值列(2); if (对象值(引用, 4)) 放入值(堆值[引用 + 2] == 0 ? 宿主字符("") : 堆值[引用 + 2], 2); return;
            }
            if (命令 == 182 && 机器字文本(名称, "append")) {
                int 文本 = 0;
                if (机器字文本(格式值, "(I)Ljava/lang/StringBuilder;")) 文本 = 数字字符(减法值列(1));
                else if (机器字文本(格式值, "(Z)Ljava/lang/StringBuilder;")) 文本 = 宿主字符(减法值列(1) == 0 ? "false" : "true");
                else if (机器字文本(格式值, "(C)Ljava/lang/StringBuilder;")) {
                    int 值 = 减法值列(1); 文本 = 分配存储装置(1, 1); if (!错误) 堆值[文本 + 2] = 值 & 65535;
                }
                else if (机器字文本(格式值, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { 文本 = 减法值列(2); if (文本 == 0) 文本 = 宿主字符("null"); }
                else { 失败值("unsupported StringBuilder append"); return; }
                int 引用 = 减法值列(2); if (!对象值(引用, 4) || !对象值(文本, 1)) return;
                int 前端值 = 堆值[引用 + 2], 前端值长度 = 前端值 == 0 ? 0 : 堆值[前端值 + 1], 后端值长度 = 堆值[文本 + 1];
                int 新建文本 = 分配存储装置(1, 前端值长度 + 后端值长度); if (错误) return;
                for (int 数 = 0; 数 < 前端值长度; 数++) 堆值[新建文本 + 2 + 数] = 堆值[前端值 + 2 + 数];
                for (int 数 = 0; 数 < 后端值长度; 数++) 堆值[新建文本 + 2 + 前端值长度 + 数] = 堆值[文本 + 2 + 数];
                堆值[引用 + 2] = 新建文本; 放入值(引用, 2); return;
            }
        }
        失败值("unsupported library method");
    }
    static int 数组槽(int 引用, int 下标值, int 类型值) {
        if (!对象值(引用, 类型值)) return 0;
        if (下标值 < 0 || 下标值 >= 堆值[引用 + 1]) { 失败值("ArrayIndexOutOfBoundsException"); return 0; }
        return 引用 + 2 + 下标值;
    }
    static void 执行命令() {
        int 余数数据 = 500000;
        while (帧索引 >= 0 && !错误) {
            if (--余数数据 == 0) { 失败值("instruction limit (500000)"); break; }
            int 运行 = 帧位置[帧索引], 值 = 读取操作码字节();
            if (错误) break;
            if (值 == 0) continue;
            if (值 == 1) { 放入值(0, 2); continue; }
            if (值 >= 2 && 值 <= 8) { 放入值(值 - 3, 1); continue; }
            if (值 == 16) { 放入值((byte)读取操作码字节(), 1); continue; }
            if (值 == 17) { 放入值((short)读取操作码短整数(), 1); continue; }
            if (值 == 18 || 值 == 19) {
                int 数 = 值 == 18 ? 读取操作码字节() : 读取操作码短整数();
                if (数 <= 0 || 数 >= 常量个数) 失败值("invalid ldc constant");
                else if (常量标签[数] == 3) 放入值(常量首位值[数], 1);
                else if (常量标签[数] == 8) 放入值(常量文本(常量首位值[数]), 2);
                else 失败值("unsupported ldc constant");
                continue;
            }
            if (值 == 21 || 值 == 25) { 读取局部(读取操作码字节(), 值 == 21 ? 1 : 2); continue; }
            if (值 >= 26 && 值 <= 29) { 读取局部(值 - 26, 1); continue; }
            if (值 >= 42 && 值 <= 45) { 读取局部(值 - 42, 2); continue; }
            if (值 == 54 || 值 == 58) { 写入局部(读取操作码字节(), 值 == 54 ? 1 : 2); continue; }
            if (值 >= 59 && 值 <= 62) { 写入局部(值 - 59, 1); continue; }
            if (值 >= 75 && 值 <= 78) { 写入局部(值 - 75, 2); continue; }
            if (值 == 46 || 值 == 50) {
                int 下标值 = 减法值列(1), 引用 = 减法值列(2), 槽条目 = 数组槽(引用, 下标值, 值 == 46 ? 2 : 3);
                if (!错误) 放入值(堆值[槽条目], 值 == 46 ? 1 : 2); continue;
            }
            if (值 == 79 || 值 == 83) {
                int 项目元素 = 减法值列(值 == 79 ? 1 : 2), 下标值 = 减法值列(1), 引用 = 减法值列(2), 槽条目 = 数组槽(引用, 下标值, 值 == 79 ? 2 : 3);
                if (值 == 83 && 项目元素 != 0) 对象值(项目元素, 1);
                if (!错误) 堆值[槽条目] = 项目元素; continue;
            }
            if (值 == 87) { 减法值列(0); continue; }
            if (值 == 89) { int 首位操作数 = 减法值列(0), 类型值 = 发回类型; 放入值(首位操作数, 类型值); 放入值(首位操作数, 类型值); continue; }
            if (值 == 95) { int 首位操作数 = 减法值列(0), 首位操作数类型 = 发回类型, 第二操作数 = 减法值列(0), 第二操作数类型 = 发回类型; 放入值(首位操作数, 首位操作数类型); 放入值(第二操作数, 第二操作数类型); continue; }
            if (值 == 96 || 值 == 100 || 值 == 104 || 值 == 108 || 值 == 112 || 值 == 120
                || 值 == 122 || 值 == 124 || 值 == 126 || 值 == 128 || 值 == 130) {
                int 第二操作数 = 减法值列(1), 首位操作数 = 减法值列(1), 结果 = 0;
                if ((值 == 108 || 值 == 112) && 第二操作数 == 0) { 失败值("ArithmeticException: / by zero"); continue; }
                if (值 == 96) 结果 = 首位操作数 + 第二操作数;
                if (值 == 100) 结果 = 首位操作数 - 第二操作数;
                if (值 == 104) 结果 = 首位操作数 * 第二操作数;
                if (值 == 108) 结果 = 首位操作数 / 第二操作数;
                if (值 == 112) 结果 = 首位操作数 % 第二操作数;
                if (值 == 120) 结果 = 首位操作数 << 第二操作数;
                if (值 == 122) 结果 = 首位操作数 >> 第二操作数;
                if (值 == 124) 结果 = 首位操作数 >>> 第二操作数;
                if (值 == 126) 结果 = 首位操作数 & 第二操作数;
                if (值 == 128) 结果 = 首位操作数 | 第二操作数;
                if (值 == 130) 结果 = 首位操作数 ^ 第二操作数;
                放入值(结果, 1); continue;
            }
            if (值 == 116) { 放入值(-减法值列(1), 1); continue; }
            if (值 == 132) {
                int 局部作用域 = 读取操作码字节(), 递增步骤 = (byte)读取操作码字节(); 读取局部(局部作用域, 1); 放入值(减法值列(1) + 递增步骤, 1); 写入局部(局部作用域, 1); continue;
            }
            if (值 >= 145 && 值 <= 147) {
                int 数 = 减法值列(1); 放入值(值 == 145 ? (byte)数 : 值 == 146 ? (char)数 : (short)数, 1); continue;
            }
            if (值 >= 153 && 值 <= 167 || 值 == 198 || 值 == 199) {
                int 目的地址值 = 运行 + (short)读取操作码短整数(); boolean 应当继续执行 = 值 == 167;
                if (值 >= 153 && 值 <= 158) {
                    int 数 = 减法值列(1); 应当继续执行 = 值 == 153 ? 数 == 0 : 值 == 154 ? 数 != 0 : 值 == 155 ? 数 < 0 : 值 == 156 ? 数 >= 0 : 值 == 157 ? 数 > 0 : 数 <= 0;
                } else if (值 >= 159 && 值 <= 166) {
                    int 第二操作数 = 减法值列(值 >= 165 ? 2 : 1), 首位操作数 = 减法值列(值 >= 165 ? 2 : 1);
                    应当继续执行 = 值 == 159 || 值 == 165 ? 首位操作数 == 第二操作数 : 值 == 160 || 值 == 166 ? 首位操作数 != 第二操作数 : 值 == 161 ? 首位操作数 < 第二操作数 : 值 == 162 ? 首位操作数 >= 第二操作数 : 值 == 163 ? 首位操作数 > 第二操作数 : 首位操作数 <= 第二操作数;
                } else if (值 == 198 || 值 == 199) { int 数 = 减法值列(2); 应当继续执行 = 值 == 198 ? 数 == 0 : 数 != 0; }
                if (应当继续执行) 移动值(目的地址值); continue;
            }
            if (值 == 172 || 值 == 176 || 值 == 177) { 发回结果(值 == 172 ? 1 : 值 == 176 ? 2 : 0); continue; }
            if (值 == 178) {
                int 数 = 读取操作码短整数(); if (!检查常量(数, 9)) continue;
                if (!机器字文本(类名称文本(常量首位值[数]), "java/lang/System") || !机器字文本(引用名称(常量第二值[数]), "out")
                    || !机器字文本(引用类型(常量第二值[数]), "Ljava/io/PrintStream;")) 失败值("unsupported static field");
                else 放入值(-1, 2); continue;
            }
            if (值 == 182 || 值 == 183 || 值 == 184) { 调用方法(读取操作码短整数(), 值); continue; }
            if (值 == 187) {
                int 名称 = 类名称文本(读取操作码短整数());
                if (机器字文本(名称, "java/lang/StringBuilder")) 放入值(分配存储装置(4, 1), 2);
                else if (机器字文本(名称, "java/io/FileInputStream") || 机器字文本(名称, "java/io/FileOutputStream")) {
                    int 引用 = 分配存储装置(机器字文本(名称, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!错误) { 堆值[引用 + 2] = -1; 放入值(引用, 2); }
                } else 失败值("unsupported object construction");
                continue;
            }
            if (值 == 188 || 值 == 189) {
                if (值 == 188) { if (读取操作码字节() != 10) 失败值("only int[] newarray is supported"); }
                else if (!机器字文本(类名称文本(读取操作码短整数()), "java/lang/String")) 失败值("only String[] anewarray is supported");
                int 长度 = 减法值列(1); 放入值(分配存储装置(值 == 188 ? 2 : 3, 长度), 2); continue;
            }
            if (值 == 190) {
                int 引用 = 减法值列(2);
                if (引用 < 1 || 引用 >= 堆结束位置 - 1 || (堆值[引用] != 2 && 堆值[引用] != 3)) 失败值("null or invalid array");
                else 放入值(堆值[引用 + 1], 1); continue;
            }
            if (值 == 192) {
                int 名称 = 类名称文本(读取操作码短整数()), 引用 = 减法值列(2);
                if (!机器字文本(名称, "java/lang/String")) 失败值("unsupported checkcast");
                else if (引用 != 0) 对象值(引用, 1);
                放入值(引用, 2); continue;
            }
            失败值("unsupported bytecode");
        }
    }
    public static int 运行() {
        if (用户.参数列个数() == 1 && Java工具.相等文本(用户.实参(0), "-version")) {
            用户.写入("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (用户.参数列个数() < 1) { 用户.写入("Usage: java CLASS [ARGS]\n"); return 2; }
        int 长度 = Java工具.名称(文件名称文本, 用户.实参(0));
        if (长度 < 1 || 长度 > 57) { 用户.写入("java: invalid class name\n"); return 2; }
        文件名称文本[长度] = '.'; 文件名称文本[长度 + 1] = 'c'; 文件名称文本[长度 + 2] = 'l'; 文件名称文本[长度 + 3] = 'a'; 文件名称文本[长度 + 4] = 's'; 文件名称文本[长度 + 5] = 's';
        大小 = 用户.读取文件(文件名称文本, 文件);
        if (大小 < 0) { 用户.写入("java: cannot read class: "); Java工具.写入编号(大小); 用户.写入字符值(10); return 1; }
        读取类(); if (错误) return 1;
        int 字符名称 = 常量文本(类名称);
        if (!错误 && 堆值[字符名称 + 1] != 长度) 失败值("class name does not match file");
        for (int 数 = 0; 数 < 长度 && !错误; 数++) if (堆值[字符名称 + 2 + 数] != 文件名称文本[数]) 失败值("class name does not match file");
        int 条目分值 = -1;
        for (int 数 = 0; 数 < 方法个数; 数++) if (机器字文本(方法名称文本[数], "main") && 机器字文本(方法类型[数], "([Ljava/lang/String;)V") && (方法存取[数] & 9) == 9) 条目分值 = 数;
        if (条目分值 < 0) 失败值("public static void main(String[] args) required");
        if (错误) return 1;
        int 实参 = 分配存储装置(3, 用户.参数列个数() - 1);
        for (int 数 = 1; 数 < 用户.参数列个数() && !错误; 数++) 堆值[实参 + 1 + 数] = 宿主字符(用户.实参(数));
        帧索引 = 0; 帧方法[0] = 条目分值; 帧位置[0] = 方法开始[条目分值]; 局部值[0] = 实参; 局部类型[0] = 2;
        执行命令(); return 错误 ? 1 : 0;
    }
}
