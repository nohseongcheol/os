// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 在客户机运行的受限 Java 源码编译器，生成标准版本 49 类文件。 */
public final class Java编译器 {
    static int[] 源代码 = new int[16384], 输出 = new int[16384], 代码值 = new int[4096];
    static int[] 词元种类 = new int[2048], 词元位置 = new int[2048], 词元长度 = new int[2048];
    static int[] 常量值 = new int[4096], 常量偏移 = new int[512];
    static int[] 字符 = new int[512], 文件名称文本 = new int[64];
    static int[] 已插入代码 = new int[16];
    static int 源代码大小, 词元个数, 位置, 代码大小, 常量大小, 常量个数 = 1, 输出大小, 字符长度;
    static boolean 错误;
    static int 类词元, 类常量, 父常量, 代码常量;
    static int[] 方法条目名称 = new int[32], 方法发回 = new int[32], 方法参数个数 = new int[32];
    static int[] 方法参数名称 = new int[512], 方法参数类型 = new int[512];
    static int[] 方法主体 = new int[32], 方法结束 = new int[32], 方法代码 = new int[32];
    static int[] 方法长度 = new int[32], 方法局部变量列 = new int[32], 方法名称常量 = new int[32], 方法描述符常量 = new int[32];
    static int[] 方法存取 = new int[32];
    static int 方法个数, 当前方法, 局部个数, 深度值, 表达式深度;
    static int[] 局部名称 = new int[128], 局部类型 = new int[128], 局部深度 = new int[128];

    static void 失败值(String 理由值) {
        if (!错误) {
            用户.写入("javac error: "); 用户.写入(理由值);
            用户.写入(" at line ");
            int 行 = 1, 结尾 = 位置 < 词元个数 ? 词元位置[位置] : 源代码大小;
            for (int 数 = 0; 数 < 结尾; 数++) if (源代码[数] == 10) 行++;
            Java工具.写入编号(行); 用户.写入字符值(10);
        }
        错误 = true;
    }
    static boolean 字符值(int 值) { return 标识符字符规则.首位字符(值); }
    static boolean 数字值(int 值) { return 值 >= '0' && 值 <= '9'; }
    static boolean 名称列相等(int 首位操作数, int 第二操作数) {
        if (首位操作数 < 0 || 第二操作数 < 0 || 首位操作数 >= 词元个数 || 第二操作数 >= 词元个数 || 词元长度[首位操作数] != 词元长度[第二操作数]) return false;
        for (int 数 = 0; 数 < 词元长度[首位操作数]; 数++) if (源代码[词元位置[首位操作数] + 数] != 源代码[词元位置[第二操作数] + 数]) return false;
        return true;
    }
    static boolean 机器字值(int 词元值, String 机器字文本) {
        if (词元值 < 0 || 词元值 >= 词元个数 || 词元长度[词元值] != 机器字文本.length()) return false;
        for (int 数 = 0; 数 < 机器字文本.length(); 数++) if (源代码[词元位置[词元值] + 数] != 机器字文本.charAt(数)) return false;
        return true;
    }
    static int 种类值() { return 位置 < 词元个数 ? 词元种类[位置] : 0; }
    static boolean 接收(int 值) { if (种类值() != 值) return false; 位置++; return true; }
    static void 要求值(int 值) { if (!接收(值)) 失败值("unexpected token"); }
    static boolean 取用机器字(String 机器字文本) { if (!机器字值(位置, 机器字文本)) return false; 位置++; return true; }
    static void 要求机器字(String 机器字文本) { if (!取用机器字(机器字文本)) 失败值(机器字文本); }
    static int 标识符值() {
        int 结果 = 位置;
        if (种类值() != 256) 失败值("identifier required"); else 位置++;
        String 已保留位单词列 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int 运行 = 0;
        for (int 数 = 0; 数 <= 已保留位单词列.length(); 数++) {
            if (数 == 已保留位单词列.length() || 已保留位单词列.charAt(数) == ' ') {
                boolean 相等文本 = 数 - 运行 == 词元长度[结果];
                for (int 槽条目 = 运行; 相等文本 && 槽条目 < 数; 槽条目++) if (已保留位单词列.charAt(槽条目) != 源代码[词元位置[结果] + 槽条目 - 运行]) 相等文本 = false;
                if (相等文本) 失败值("reserved word cannot be an identifier");
                运行 = 数 + 1;
            }
        }
        return 结果;
    }
    static void 剪切值() {
        int 数 = 0;
        while (数 < 源代码大小 && !错误) {
            int 值 = 源代码[数], 运行 = 数, 种类值 = 值;
            if (值 == 32 || 值 == 9 || 值 == 10 || 值 == 13) { 数++; continue; }
            if (值 == '/' && 数 + 1 < 源代码大小 && 源代码[数 + 1] == '/') {
                while (数 < 源代码大小 && 源代码[数] != 10) 数++;
                continue;
            }
            if (值 == '/' && 数 + 1 < 源代码大小 && 源代码[数 + 1] == '*') {
                数 += 2;
                while (数 + 1 < 源代码大小 && !(源代码[数] == '*' && 源代码[数 + 1] == '/')) 数++;
                if (数 + 1 >= 源代码大小) { 失败值("unterminated comment"); break; }
                数 += 2; continue;
            }
            if (字符值(值)) { 种类值 = 256; while (数 < 源代码大小 && 标识符字符规则.继续状态字符(源代码[数])) 数++; }
            else if (数字值(值)) { 种类值 = 257; while (数 < 源代码大小 && 数字值(源代码[数])) 数++; }
            else if (值 == '"' || 值 == '\'') {
                种类值 = 值 == '"' ? 258 : 259; 数++;
                while (数 < 源代码大小 && 源代码[数] != 值 && 源代码[数] != 10 && 源代码[数] != 13) {
                    if (源代码[数] == '\\') 数++;
                    数++;
                }
                if (数 >= 源代码大小 || 源代码[数] != 值) { 失败值("unterminated literal"); break; }
                数++;
            } else {
                数++;
                if (数 < 源代码大小) {
                    int 下一项目 = 源代码[数];
                    if (值 == '=' && 下一项目 == '=') 种类值 = 300;
                    if (值 == '!' && 下一项目 == '=') 种类值 = 301;
                    if (值 == '<' && 下一项目 == '=') 种类值 = 302;
                    if (值 == '>' && 下一项目 == '=') 种类值 = 303;
                    if (值 == '&' && 下一项目 == '&') 种类值 = 304;
                    if (值 == '|' && 下一项目 == '|') 种类值 = 305;
                    if (值 == '+' && 下一项目 == '+') 种类值 = 306;
                    if (值 == '-' && 下一项目 == '-') 种类值 = 307;
                    if (值 == '+' && 下一项目 == '=') 种类值 = 308;
                    if (值 == '-' && 下一项目 == '=') 种类值 = 309;
                    if (值 == '*' && 下一项目 == '=') 种类值 = 310;
                    if (值 == '/' && 下一项目 == '=') 种类值 = 311;
                    if (值 == '%' && 下一项目 == '=') 种类值 = 312;
                    if (种类值 >= 300) 数++;
                }
            }
            if (词元个数 == 词元种类.length - 1) { 失败值("too many tokens (2047 maximum)"); break; }
            词元种类[词元个数] = 种类值; 词元位置[词元个数] = 运行; 词元长度[词元个数++] = 数 - 运行;
        }
    }
    static void 写入常量字节(int 值) {
        if (常量大小 == 常量值.length) { 失败值("constant pool too large"); return; }
        常量值[常量大小++] = 值 & 255;
    }
    static void 写入常量短整数(int 值) { 写入常量字节(值 >> 8); 写入常量字节(值); }
    static int 寄存器常量(int 运行) {
        for (int 数 = 1; 数 < 常量个数; 数++) {
            int 前端值 = 常量偏移[数], 长度 = (数 + 1 < 常量个数 ? 常量偏移[数 + 1] : 运行) - 前端值;
            if (长度 != 常量大小 - 运行) continue;
            boolean 相等文本 = true;
            for (int 槽条目 = 0; 槽条目 < 长度; 槽条目++) if (常量值[前端值 + 槽条目] != 常量值[运行 + 槽条目]) 相等文本 = false;
            if (相等文本) { 常量大小 = 运行; return 数; }
        }
        if (常量个数 == 常量偏移.length) { 失败值("too many constants"); return 0; }
        常量偏移[常量个数] = 运行;
        return 常量个数++;
    }
    static void 追加文本(int 值) {
        if (字符长度 == 字符.length) { 失败值("text too long"); return; }
        字符[字符长度++] = 值;
    }
    static void 追加机器字(String 机器字文本) { for (int 数 = 0; 数 < 机器字文本.length(); 数++) 追加文本(机器字文本.charAt(数)); }
    static int 字符常量() {
        int 运行 = 常量大小; 写入常量字节(1); 写入常量短整数(0);
        for (int 数 = 0; 数 < 字符长度; 数++) {
            int 值 = 字符[数];
            if (值 > 0 && 值 < 128) 写入常量字节(值);
            else if (值 < 2048) { 写入常量字节(192 | 值 >> 6); 写入常量字节(128 | 值 & 63); }
            else { 写入常量字节(224 | 值 >> 12); 写入常量字节(128 | 值 >> 6 & 63); 写入常量字节(128 | 值 & 63); }
        }
        if (错误) return 0;
        int 长度 = 常量大小 - 运行 - 3;
        常量值[运行 + 1] = 长度 >> 8; 常量值[运行 + 2] = 长度 & 255;
        return 寄存器常量(运行);
    }
    static int 机器字常量(String 机器字文本) { 字符长度 = 0; 追加机器字(机器字文本); return 字符常量(); }
    static int 词元常量(int 词元值) {
        字符长度 = 0;
        for (int 数 = 0; 数 < 词元长度[词元值]; 数++) 追加文本(源代码[词元位置[词元值] + 数]);
        return 字符常量();
    }
    static int 引用(int 种类值, int 首位操作数, int 第二操作数) {
        int 运行 = 常量大小; 写入常量字节(种类值); 写入常量短整数(首位操作数);
        if (种类值 == 9 || 种类值 == 10 || 种类值 == 12) 写入常量短整数(第二操作数);
        return 寄存器常量(运行);
    }
    static int 外部引用(int 种类值, String 所有者值, String 名称, String 说明值) {
        int 所有者标识符 = 引用(7, 机器字常量(所有者值), 0);
        int 名称个数 = 机器字常量(名称), 格式个数 = 机器字常量(说明值);
        return 引用(种类值, 所有者标识符, 引用(12, 名称个数, 格式个数));
    }
    static void 发射值(int 值) {
        if (代码大小 == 代码值.length) { 失败值("bytecode too large"); return; }
        代码值[代码大小++] = 值 & 255;
    }
    static void 命令(int 值, int 实参) { 发射值(值); 发射值(实参 >> 8); 发射值(实参); }
    static void 数值常量(int 值) {
        if (值 >= -1 && 值 <= 5) { 发射值(值 + 3); return; }
        int 运行 = 常量大小; 写入常量字节(3); 写入常量短整数(值 >>> 16); 写入常量短整数(值);
        命令(19, 寄存器常量(运行));
    }
    static int 分支(int 命令) { int 结果 = 代码大小; 命令(命令, 0); return 结果; }
    static void 连接值(int 分支, int 目标对象) {
        if (错误) return;
        int 距离值 = 目标对象 - 分支;
        if (距离值 < -32768 || 距离值 > 32767 || 分支 < 0 || 分支 + 2 >= 代码大小) { 失败值("invalid branch"); return; }
        代码值[分支 + 1] = 距离值 >> 8 & 255; 代码值[分支 + 2] = 距离值 & 255;
    }
    static void 比较值(int 命令) {
        int 真值 = 分支(命令); 发射值(3); int 结尾 = 分支(167);
        连接值(真值, 代码大小); 发射值(4); 连接值(结尾, 代码大小);
    }
    static int 格式值() {
        if (取用机器字("void")) return 0;
        if (取用机器字("int")) return 1;
        if (取用机器字("boolean")) return 2;
        if (取用机器字("char")) return 5;
        if (取用机器字("FileInputStream")) return 6;
        if (取用机器字("FileOutputStream")) return 7;
        if (取用机器字("String")) { if (接收('[')) { 要求值(']'); return 4; } return 3; }
        失败值("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void 添加格式(int 类型值) {
        if (类型值 == 0) 追加文本('V');
        if (类型值 == 1) 追加文本('I');
        if (类型值 == 2) 追加文本('Z');
        if (类型值 == 3) 追加机器字("Ljava/lang/String;");
        if (类型值 == 4) 追加机器字("[Ljava/lang/String;");
        if (类型值 == 5) 追加文本('C');
        if (类型值 == 6) 追加机器字("Ljava/io/FileInputStream;");
        if (类型值 == 7) 追加机器字("Ljava/io/FileOutputStream;");
    }
    // 受限编译器支持 throws 声明；异常处理体使用宿主 javac。
    static void 读取异常名称() {
        boolean 韩语捆绑 = 取用机器字("中文");
        if (韩语捆绑) { 要求值('.'); 要求机器字("内置"); 要求值('.'); }
        if (!韩语捆绑 && (取用机器字("Exception") || 取用机器字("IOException"))) return;
        if (取用机器字("异常") || 取用机器字("执行状态异常") || 取用机器字("输入输出异常") || 取用机器字("等待状态超时异常") || 取用机器字("地址查找异常") || 取用机器字("缺失文件异常") || 取用机器字("通信异常") || 取用机器字("无效参数异常") || 取用机器字("编号格式失败") || 取用机器字("边界异常") || 取用机器字("数组边界异常") || 取用机器字("字符串边界异常") || 取用机器字("空引用引用异常") || 取用机器字("算术失败") || 取用机器字("状态异常") || 取用机器字("类型类型转换异常") || 取用机器字("负数数组大小失败") || 取用机器字("数组存储失败") || 取用机器字("线程状态异常") || 取用机器字("等待状态已中断异常")) return;
        失败值("unsupported throws type");
    }
    static void 读取声明() {
        while (取用机器字("import")) {
            if (机器字值(位置, "中文")) 读取异常名称();
            else {
                要求机器字("java"); 要求值('.'); 要求机器字("io"); 要求值('.');
                if (!(取用机器字("FileInputStream") || 取用机器字("FileOutputStream") || 取用机器字("IOException"))) 失败值("unsupported import");
            }
            要求值(';');
        }
        取用机器字("public"); 取用机器字("final"); 要求机器字("class"); 类词元 = 标识符值();
        类常量 = 引用(7, 词元常量(类词元), 0);
        父常量 = 引用(7, 机器字常量("java/lang/Object"), 0); 代码常量 = 机器字常量("Code"); 要求值('{');
        while (!错误 && 种类值() != '}') {
            if (方法个数 == 32) { 失败值("too many methods"); break; }
            int 存取条目 = 取用机器字("public") ? 1 : 取用机器字("private") ? 2 : 0; 要求机器字("static");
            int 函数 = 方法个数++;
            方法存取[函数] = 存取条目 | 8;
            方法发回[函数] = 格式值(); 方法条目名称[函数] = 标识符值(); 要求值('(');
            for (int 前端值 = 0; 前端值 < 函数; 前端值++) if (名称列相等(方法条目名称[前端值], 方法条目名称[函数])) 失败值("duplicate method (overloading unsupported)");
            while (!错误 && 种类值() != ')') {
                int 数 = 方法参数个数[函数];
                if (数 == 16) { 失败值("too many parameters"); break; }
                int 类型值 = 格式值(); if (类型值 == 0) 失败值("void parameter");
                方法参数类型[函数 * 16 + 数] = 类型值; 方法参数名称[函数 * 16 + 数] = 标识符值();
                方法参数个数[函数]++;
                if (!接收(',')) break;
            }
            要求值(')');
            if (取用机器字("throws")) {
                do { 读取异常名称(); } while (!错误 && 接收(','));
            }
            方法主体[函数] = 位置; 要求值('{');
            int 嵌套值 = 1;
            while (位置 < 词元个数 && 嵌套值 > 0) {
                if (种类值() == '{') 嵌套值++;
                if (种类值() == '}') 嵌套值--;
                位置++;
            }
            if (嵌套值 != 0) 失败值("unclosed method body");
            方法结束[函数] = 位置;
            方法名称常量[函数] = 词元常量(方法条目名称[函数]);
            字符长度 = 0; 追加文本('(');
            for (int 数 = 0; 数 < 方法参数个数[函数]; 数++) 添加格式(方法参数类型[函数 * 16 + 数]);
            追加文本(')'); 添加格式(方法发回[函数]); 方法描述符常量[函数] = 字符常量();
        }
        要求值('}'); if (位置 != 词元个数) 失败值("extra input after class");
    }
    static int 查找局部(int 名称) {
        for (int 数 = 局部个数 - 1; 数 >= 0; 数--) if (局部深度[数] >= 0 && 名称列相等(局部名称[数], 名称)) return 数;
        失败值("unknown variable"); return 0;
    }
    static int 添加局部(int 名称, int 类型值) {
        for (int 数 = 0; 数 < 局部个数; 数++) if (局部深度[数] >= 0 && 名称列相等(局部名称[数], 名称)) 失败值("duplicate local variable");
        if (局部个数 == 128) { 失败值("too many locals"); return 0; }
        局部名称[局部个数] = 名称; 局部类型[局部个数] = 类型值; 局部深度[局部个数] = 深度值;
        return 局部个数++;
    }
    static boolean 整数类型(int 类型值) { return 类型值 == 1 || 类型值 == 5; }
    static void 读取局部(int 数) { 发射值(局部类型[数] <= 2 || 局部类型[数] == 5 ? 21 : 25); 发射值(数); }
    static void 写入局部(int 数) { 发射值(局部类型[数] <= 2 || 局部类型[数] == 5 ? 54 : 58); 发射值(数); }
    static void 验证类型(int 实际数据, int 期望状态) { if (实际数据 != 期望状态 && !(实际数据 == 5 && 期望状态 == 1)) 失败值("type mismatch"); }
    static void 读取字符值(int 词元值) {
        字符长度 = 0; int 运行 = 词元位置[词元值] + 1, 结尾 = 词元位置[词元值] + 词元长度[词元值] - 1;
        while (运行 < 结尾 && !错误) {
            int 值 = 源代码[运行++];
            if (值 == '\\') {
                if (运行 == 结尾) { 失败值("invalid escape"); break; }
                值 = 源代码[运行++];
                if (值 == 'n') 值 = 10;
                else if (值 == 'r') 值 = 13;
                else if (值 == 't') 值 = 9;
                else if (值 == 'b') 值 = 8;
                else if (值 == 'f') 值 = 12;
                else if (值 != '\\' && 值 != '"' && 值 != '\'') 失败值("unsupported escape");
            }
            追加文本(值);
        }
    }
    static int 解析整数(int 词元值, boolean 负数值) {
        if (词元长度[词元值] > 1 && 源代码[词元位置[词元值]] == '0') 失败值("octal literals unsupported");
        int 值 = 0;
        for (int 数 = 0; 数 < 词元长度[词元值]; 数++) {
            int 数字项目 = 源代码[词元位置[词元值] + 数] - '0';
            if (值 < -214748364 || 值 == -214748364 && 数字项目 > (负数值 ? 8 : 7)) 失败值("integer literal out of range");
            值 = 值 * 10 - 数字项目;
        }
        return 负数值 ? 值 : -值;
    }
    static int 主要表达式() {
        if (取用机器字("new")) {
            int 类型值 = 格式值();
            if (类型值 != 6 && 类型值 != 7) { 失败值("only file streams supported by new in source"); return 0; }
            String 所有者值 = 类型值 == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            命令(187, 引用(7, 机器字常量(所有者值), 0)); 发射值(89);
            要求值('('); 验证类型(表达式值(), 3); boolean 继续状态值 = false;
            if (接收(',')) { if (类型值 != 7) 失败值("input stream constructor arguments"); 验证类型(表达式值(), 2); 继续状态值 = true; }
            要求值(')');
            命令(183, 外部引用(10, 所有者值, "<init>", 继续状态值 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return 类型值;
        }
        if (接收('(')) { int 类型值 = 表达式值(); 要求值(')'); return 类型值; }
        if (种类值() == 257) { 数值常量(解析整数(位置++, false)); return 1; }
        if (种类值() == 258) { 读取字符值(位置++); 命令(19, 引用(8, 字符常量(), 0)); return 3; }
        if (种类值() == 259) { 读取字符值(位置++); if (字符长度 != 1) 失败值("character literal length"); 数值常量(字符[0]); return 5; }
        if (取用机器字("true")) { 发射值(4); return 2; }
        if (取用机器字("false")) { 发射值(3); return 2; }
        if (取用机器字("中文")) {
            要求值('.'); 要求机器字("内置"); 要求值('.');
            String 所有者值 = "", 方法值 = "", 说明值 = ""; int 首位操作数 = 0, 第二操作数 = 0, 第三操作数 = 0, 第四操作数 = 0, 第五操作数 = 0, 结果 = 0;
            if (取用机器字("输出")) {
                所有者值 = "中文/内置/输出"; 要求值('.');
                if (取用机器字("写入行")) { 方法值 = "写入行"; 说明值 = "(Ljava/lang/String;)V"; 首位操作数 = 3; }
                else if (取用机器字("写入")) { 方法值 = "写入"; 说明值 = "(Ljava/lang/String;)V"; 首位操作数 = 3; }
                else if (取用机器字("写入编号")) { 方法值 = "写入编号"; 说明值 = "(I)V"; 首位操作数 = 1; }
                else 失败值("unknown Korean output method");
            } else if (取用机器字("字符")) {
                所有者值 = "中文/内置/字符"; 要求值('.'); 首位操作数 = 3;
                if (取用机器字("长度")) { 方法值 = "长度"; 说明值 = "(Ljava/lang/String;)I"; 结果 = 1; }
                else if (取用机器字("代码分个数")) { 方法值 = "代码分个数"; 说明值 = "(Ljava/lang/String;)I"; 结果 = 1; }
                else if (取用机器字("解析整数")) { 方法值 = "解析整数"; 说明值 = "(Ljava/lang/String;)I"; 结果 = 1; }
                else if (取用机器字("写入整数值")) { 方法值 = "写入整数值"; 说明值 = "(I)Ljava/lang/String;"; 首位操作数 = 1; 结果 = 3; }
                else if (取用机器字("相等文本")) { 方法值 = "相等文本"; 说明值 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 第二操作数 = 3; 结果 = 2; }
                else if (取用机器字("粘贴文本")) { 方法值 = "粘贴文本"; 说明值 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 第二操作数 = 3; 结果 = 3; }
                else if (取用机器字("剪切值")) { 方法值 = "剪切值"; 说明值 = "(Ljava/lang/String;II)Ljava/lang/String;"; 第二操作数 = 1; 第三操作数 = 1; 结果 = 3; }
                else 失败值("unknown Korean text method");
            } else if (取用机器字("文件")) {
                所有者值 = "中文/内置/文件"; 要求值('.'); 首位操作数 = 3;
                if (取用机器字("读取")) { 方法值 = "读取"; 说明值 = "(Ljava/lang/String;)Ljava/lang/String;"; 结果 = 3; }
                else if (取用机器字("写入")) { 方法值 = "写入"; 说明值 = "(Ljava/lang/String;Ljava/lang/String;)V"; 第二操作数 = 3; }
                else 失败值("unknown Korean file method");
            } else if (取用机器字("屏幕")) {
                所有者值 = "中文/内置/屏幕"; 要求值('.');
                if (取用机器字("宽度值")) { 方法值 = "宽度值"; 说明值 = "()I"; 结果 = 1; }
                else if (取用机器字("高度值")) { 方法值 = "高度值"; 说明值 = "()I"; 结果 = 1; }
                else if (取用机器字("矩形")) { 方法值 = "矩形"; 说明值 = "(IIIII)V"; 首位操作数 = 1; 第二操作数 = 1; 第三操作数 = 1; 第四操作数 = 1; 第五操作数 = 1; }
                else if (取用机器字("擦除条目")) { 方法值 = "擦除条目"; 说明值 = "(I)V"; 首位操作数 = 1; }
                else if (取用机器字("等待")) { 方法值 = "等待"; 说明值 = "()V"; }
                else 失败值("unknown Korean framebuffer method");
            } else 失败值("unsupported Korean library class");
            要求值('('); if (首位操作数 != 0) 验证类型(表达式值(), 首位操作数);
            if (第二操作数 != 0) { 要求值(','); 验证类型(表达式值(), 第二操作数); }
            if (第三操作数 != 0) { 要求值(','); 验证类型(表达式值(), 第三操作数); }
            if (第四操作数 != 0) { 要求值(','); 验证类型(表达式值(), 第四操作数); }
            if (第五操作数 != 0) { 要求值(','); 验证类型(表达式值(), 第五操作数); }
            要求值(')'); 命令(184, 外部引用(10, 所有者值, 方法值, 说明值)); return 结果;
        }
        if (取用机器字("Integer")) {
            要求值('.'); 要求机器字("parseInt"); 要求值('('); 验证类型(表达式值(), 3); 要求值(')');
            命令(184, 外部引用(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int 名称 = 标识符值();
        if (接收('(')) {
            int 函数 = -1;
            for (int 数 = 0; 数 < 方法个数; 数++) if (名称列相等(名称, 方法条目名称[数])) 函数 = 数;
            if (函数 < 0) { 失败值("unknown static method"); return 0; }
            int 数 = 0;
            while (!错误 && 种类值() != ')') {
                if (数 >= 方法参数个数[函数]) { 失败值("too many arguments"); break; }
                验证类型(表达式值(), 方法参数类型[函数 * 16 + 数++]); if (!接收(',')) break;
            }
            要求值(')'); if (数 != 方法参数个数[函数]) 失败值("argument count mismatch");
            命令(184, 引用(10, 类常量, 引用(12, 方法名称常量[函数], 方法描述符常量[函数])));
            return 方法发回[函数];
        }
        int 局部作用域 = 查找局部(名称), 类型值 = 局部类型[局部作用域]; 读取局部(局部作用域);
        while (!错误) {
            if (接收('[')) { 验证类型(类型值, 4); 验证类型(表达式值(), 1); 要求值(']'); 发射值(50); 类型值 = 3; }
            else if (接收('.')) {
                if (类型值 == 6 || 类型值 == 7) {
                    String 所有者值 = 类型值 == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (取用机器字("close")) { 要求值('('); 要求值(')'); 命令(182, 外部引用(10, 所有者值, "close", "()V")); 类型值 = 0; }
                    else if (类型值 == 6 && 取用机器字("read")) { 要求值('('); 要求值(')'); 命令(182, 外部引用(10, 所有者值, "read", "()I")); 类型值 = 1; }
                    else if (类型值 == 7 && 取用机器字("write")) { 要求值('('); 验证类型(表达式值(), 1); 要求值(')'); 命令(182, 外部引用(10, 所有者值, "write", "(I)V")); 类型值 = 0; }
                    else { 失败值("unsupported file stream method"); }
                    continue;
                }
                要求机器字("length");
                if (类型值 == 4) { 发射值(190); 类型值 = 1; }
                else { 验证类型(类型值, 3); 要求值('('); 要求值(')'); 命令(182, 外部引用(10, "java/lang/String", "length", "()I")); 类型值 = 1; }
            } else break;
        }
        return 类型值;
    }
    static int 一元值() {
        if (++表达式深度 > 64) { 失败值("expression nesting too deep"); 表达式深度--; return 0; }
        int 类型值;
        if (接收('!')) { 验证类型(一元值(), 2); 比较值(153); 类型值 = 2; }
        else if (接收('-')) {
            if (种类值() == 257) 数值常量(解析整数(位置++, true));
            else { 验证类型(一元值(), 1); 发射值(116); }
            类型值 = 1;
        } else if (接收('+')) { 验证类型(一元值(), 1); 类型值 = 1; }
        else 类型值 = 主要表达式();
        表达式深度--; return 类型值;
    }
    static int 乘法结果表达式() {
        int 类型值 = 一元值();
        while (!错误 && (种类值() == '*' || 种类值() == '/' || 种类值() == '%')) {
            int 编码状态值 = 种类值(); 位置++; 验证类型(类型值, 1); 验证类型(一元值(), 1);
            发射值(编码状态值 == '*' ? 104 : 编码状态值 == '/' ? 108 : 112); 类型值 = 1;
        }
        return 类型值;
    }
    static int 加法结果表达式() {
        int 类型值 = 乘法结果表达式();
        while (!错误 && (种类值() == '+' || 种类值() == '-')) {
            int 编码状态值 = 种类值(); 位置++; int 边界位置值 = 代码大小, 后端值类型 = 乘法结果表达式();
            if (编码状态值 == '+' && (类型值 == 3 || 后端值类型 == 3)) { 合并值列(边界位置值, 类型值, 后端值类型); 类型值 = 3; }
            else { 验证类型(类型值, 1); 验证类型(后端值类型, 1); 发射值(编码状态值 == '+' ? 96 : 100); 类型值 = 1; }
        }
        return 类型值;
    }
    static int 已附加引用(int 类型值) {
        if (类型值 != 1 && 类型值 != 2 && 类型值 != 3 && 类型值 != 5) 失败值("unsupported concatenation type");
        return 外部引用(10, "java/lang/StringBuilder", "append", 类型值 == 1 ? "(I)Ljava/lang/StringBuilder;"
            : 类型值 == 2 ? "(Z)Ljava/lang/StringBuilder;" : 类型值 == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 合并值列(int 边界位置值, int 前端值类型, int 后端值类型) {
        // 在右操作数代码之前插入生成代码，使已算出的左值先被 append。
        // 右表达式内部的相对分支距离保持不变，因为整个区域一同移动。
        int 结尾 = 代码大小;
        命令(187, 引用(7, 机器字常量("java/lang/StringBuilder"), 0)); 发射值(89);
        命令(183, 外部引用(10, "java/lang/StringBuilder", "<init>", "()V")); 发射值(95); 命令(182, 已附加引用(前端值类型));
        if (错误) return;
        int 长度 = 代码大小 - 结尾;
        for (int 数 = 0; 数 < 长度; 数++) 已插入代码[数] = 代码值[结尾 + 数];
        for (int 数 = 结尾 - 1; 数 >= 边界位置值; 数--) 代码值[数 + 长度] = 代码值[数];
        for (int 数 = 0; 数 < 长度; 数++) 代码值[边界位置值 + 数] = 已插入代码[数];
        命令(182, 已附加引用(后端值类型)); 命令(182, 外部引用(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int 比较表达式() {
        int 类型值 = 加法结果表达式();
        while (!错误 && (种类值() == '<' || 种类值() == '>' || 种类值() == 302 || 种类值() == 303)) {
            int 编码状态值 = 种类值(); 位置++; 验证类型(类型值, 1); 验证类型(加法结果表达式(), 1);
            比较值(编码状态值 == '<' ? 161 : 编码状态值 == '>' ? 163 : 编码状态值 == 302 ? 164 : 162); 类型值 = 2;
        }
        return 类型值;
    }
    static int 等值判断表达式() {
        int 类型值 = 比较表达式();
        while (!错误 && (种类值() == 300 || 种类值() == 301)) {
            int 编码状态值 = 种类值(); 位置++; int 后端值类型 = 比较表达式();
            if (类型值 == 0 || 后端值类型 == 0) 失败值("void expression");
            if (!(整数类型(类型值) && 整数类型(后端值类型))) 验证类型(后端值类型, 类型值);
            比较值((类型值 <= 2 || 类型值 == 5 ? 159 : 165) + (编码状态值 == 301 ? 1 : 0)); 类型值 = 2;
        }
        return 类型值;
    }
    static int 逻辑与() {
        int 类型值 = 等值判断表达式();
        while (!错误 && 接收(304)) {
            验证类型(类型值, 2); int 首位操作数 = 分支(153); 验证类型(等值判断表达式(), 2); int 第二操作数 = 分支(153);
            发射值(4); int 结尾 = 分支(167); 连接值(首位操作数, 代码大小); 连接值(第二操作数, 代码大小); 发射值(3); 连接值(结尾, 代码大小); 类型值 = 2;
        }
        return 类型值;
    }
    static int 表达式值() {
        int 类型值 = 逻辑与();
        while (!错误 && 接收(305)) {
            验证类型(类型值, 2); int 首位操作数 = 分支(154); 验证类型(逻辑与(), 2); int 第二操作数 = 分支(154);
            发射值(3); int 结尾 = 分支(167); 连接值(首位操作数, 代码大小); 连接值(第二操作数, 代码大小); 发射值(4); 连接值(结尾, 代码大小); 类型值 = 2;
        }
        return 类型值;
    }
    static void 赋值状态值(boolean 允许声明) {
        if (机器字值(位置, "int") || 机器字值(位置, "boolean") || 机器字值(位置, "String") || 机器字值(位置, "char")
            || 机器字值(位置, "FileInputStream") || 机器字值(位置, "FileOutputStream")) {
            if (!允许声明) 失败值("declaration not allowed here");
            int 类型值 = 格式值(), 名称 = 标识符值(); 要求值('='); 验证类型(表达式值(), 类型值);
            写入局部(添加局部(名称, 类型值)); return;
        }
        int 名称 = 标识符值(), 局部作用域 = 查找局部(名称);
        if (接收('=')) { 验证类型(表达式值(), 局部类型[局部作用域]); 写入局部(局部作用域); }
        else if (种类值() >= 308 && 种类值() <= 312) {
            int 编码状态值 = 种类值(); 位置++; 读取局部(局部作用域); int 边界位置值 = 代码大小, 后端值类型 = 表达式值();
            if (编码状态值 == 308 && 局部类型[局部作用域] == 3) 合并值列(边界位置值, 3, 后端值类型);
            else {
                验证类型(局部类型[局部作用域], 1); 验证类型(后端值类型, 1);
                发射值(编码状态值 == 308 ? 96 : 编码状态值 == 309 ? 100 : 编码状态值 == 310 ? 104 : 编码状态值 == 311 ? 108 : 112);
                if (局部类型[局部作用域] == 5) 发射值(146);
            }
            写入局部(局部作用域);
        }
        else if (种类值() == 306 || 种类值() == 307) {
            验证类型(局部类型[局部作用域], 1); 发射值(132); 发射值(局部作用域); 发射值(种类值() == 306 ? 1 : 255); 位置++;
            if (局部类型[局部作用域] == 5) { 读取局部(局部作用域); 发射值(146); 写入局部(局部作用域); }
        } else 失败值("assignment or postfix increment required");
    }
    static void 屏幕输出() {
        要求机器字("System"); 要求值('.'); 要求机器字("out"); 要求值('.');
        boolean 换行 = 取用机器字("println"); if (!换行) 要求机器字("print"); 要求值('(');
        命令(178, 外部引用(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean 空参数 = 种类值() == ')';
        int 类型值 = 空参数 ? 0 : 表达式值(); 要求值(')'); 要求值(';');
        String 说明值 = 类型值 == 0 ? "()V" : 类型值 == 1 ? "(I)V" : 类型值 == 2 ? "(Z)V" : 类型值 == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (类型值 == 4 || 类型值 >= 6 || 类型值 == 0 && (!换行 || !空参数)) 失败值("unsupported print argument");
        命令(182, 外部引用(10, "java/io/PrintStream", 换行 ? "println" : "print", 说明值));
    }
    static boolean 语句值() {
        if (错误) return false;
        if (深度值 > 32) { 失败值("statement nesting too deep"); return false; }
        if (接收('{')) {
            深度值++; boolean 发回结果 = false;
            while (!错误 && 种类值() != '}') { if (发回结果) 失败值("unreachable statement"); 发回结果 = 语句值(); }
            要求值('}'); for (int 数 = 0; 数 < 局部个数; 数++) if (局部深度[数] == 深度值) 局部深度[数] = -1;
            深度值--; return 发回结果;
        }
        if (接收(';')) return false;
        if (取用机器字("return")) {
            int 类型值 = 种类值() == ';' ? 0 : 表达式值(); 验证类型(类型值, 方法发回[当前方法]); 要求值(';');
            发射值(类型值 == 0 ? 177 : 类型值 <= 2 || 类型值 == 5 ? 172 : 176); return true;
        }
        if (取用机器字("if")) {
            要求值('('); 验证类型(表达式值(), 2); 要求值(')'); int 假值 = 分支(153);
            深度值++; boolean 首位操作数 = 控制语句(); 深度值--;
            if (取用机器字("else")) { int 结尾 = 分支(167); 连接值(假值, 代码大小); 深度值++; boolean 第二操作数 = 控制语句(); 深度值--; 连接值(结尾, 代码大小); return 首位操作数 && 第二操作数; }
            连接值(假值, 代码大小); return false;
        }
        if (取用机器字("while")) {
            int 运行 = 代码大小; 要求值('('); 验证类型(表达式值(), 2); 要求值(')'); int 结尾 = 分支(153);
            深度值++; 控制语句(); 深度值--; 连接值(分支(167), 运行); 连接值(结尾, 代码大小); return false;
        }
        if (取用机器字("for")) {
            深度值++; 要求值('('); if (种类值() != ';') 赋值状态值(true); 要求值(';');
            int 条件 = 代码大小; if (种类值() == ';') 发射值(4); else 验证类型(表达式值(), 2); 要求值(';');
            int 结尾 = 分支(153), 主体文本 = 分支(167), 刷新 = 代码大小;
            if (种类值() != ')') 赋值状态值(false); 要求值(')'); 连接值(分支(167), 条件); 连接值(主体文本, 代码大小);
            控制语句(); 连接值(分支(167), 刷新); 连接值(结尾, 代码大小);
            for (int 数 = 0; 数 < 局部个数; 数++) if (局部深度[数] == 深度值) 局部深度[数] = -1;
            深度值--; return false;
        }
        if (机器字值(位置, "System")) { 屏幕输出(); return false; }
        if (种类值() == 256 && 位置 + 1 < 词元个数 && (词元种类[位置 + 1] == '(' || 词元种类[位置 + 1] == '.')) {
            int 类型值 = 表达式值(); if (类型值 != 0) 发射值(87); 要求值(';'); return false;
        }
        赋值状态值(true); 要求值(';'); return false;
    }
    static boolean 控制语句() {
        if (机器字值(位置, "int") || 机器字值(位置, "boolean") || 机器字值(位置, "char") || 机器字值(位置, "String")
            || 机器字值(位置, "FileInputStream") || 机器字值(位置, "FileOutputStream")) 失败值("local declaration requires braces");
        return 语句值();
    }
    static void 发射类字节(int 值) { if (输出大小 == 输出.length) 失败值("class file too large"); else 输出[输出大小++] = 值 & 255; }
    static void 发射类短整数(int 值) { 发射类字节(值 >> 8); 发射类字节(值); }
    static void 发射类整数(int 值) { 发射类短整数(值 >>> 16); 发射类短整数(值); }
    static void 写入类() {
        发射类整数(0xcafebabe); 发射类短整数(0); 发射类短整数(49); 发射类短整数(常量个数);
        for (int 数 = 0; 数 < 常量大小; 数++) 发射类字节(常量值[数]);
        发射类短整数(0x21); 发射类短整数(类常量); 发射类短整数(父常量); 发射类短整数(0); 发射类短整数(0); 发射类短整数(方法个数);
        for (int 数 = 0; 数 < 方法个数; 数++) {
            发射类短整数(方法存取[数]); 发射类短整数(方法名称常量[数]); 发射类短整数(方法描述符常量[数]); 发射类短整数(1); 发射类短整数(代码常量);
            发射类整数(12 + 方法长度[数]); 发射类短整数(128); 发射类短整数(方法局部变量列[数]); 发射类整数(方法长度[数]);
            for (int 槽条目 = 0; 槽条目 < 方法长度[数]; 槽条目++) 发射类字节(代码值[方法代码[数] + 槽条目]);
            发射类短整数(0); 发射类短整数(0);
        }
        发射类短整数(0);
    }
    public static int 运行() {
        if (用户.参数列个数() == 1 && Java工具.相等文本(用户.实参(0), "-version")) {
            用户.写入("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (用户.参数列个数() != 1) { 用户.写入("Usage: javac FILE.java\n"); return 2; }
        int 名称大小 = Java工具.名称(文件名称文本, 用户.实参(0));
        if (名称大小 < 6 || 名称大小 > 62 || 文件名称文本[名称大小 - 5] != '.' || 文件名称文本[名称大小 - 4] != 'j'
            || 文件名称文本[名称大小 - 3] != 'a' || 文件名称文本[名称大小 - 2] != 'v' || 文件名称文本[名称大小 - 1] != 'a') {
            用户.写入("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        源代码大小 = 用户.读取文件(文件名称文本, 源代码);
        if (源代码大小 < 0) { 用户.写入("javac: cannot read source: "); Java工具.写入编号(源代码大小); 用户.写入字符值(10); return 1; }
        源代码大小 = Java工具.解码源代码(源代码, 源代码大小);
        if (源代码大小 < 0) { 用户.写入("javac error: invalid UTF-8 source\n"); return 1; }
        剪切值(); if (!错误) 读取声明();
        if (!错误) {
            if (词元长度[类词元] != 名称大小 - 5) 失败值("class name must match file name");
            for (int 数 = 0; 数 < 名称大小 - 5; 数++) if (源代码[词元位置[类词元] + 数] != 文件名称文本[数]) 失败值("class name must match file name");
        }
        for (当前方法 = 0; 当前方法 < 方法个数 && !错误; 当前方法++) {
            位置 = 方法主体[当前方法]; 方法代码[当前方法] = 代码大小; 局部个数 = 0; 深度值 = 0;
            for (int 数 = 0; 数 < 方法参数个数[当前方法]; 数++) 添加局部(方法参数名称[当前方法 * 16 + 数], 方法参数类型[当前方法 * 16 + 数]);
            boolean 发回结果 = 语句值();
            if (!发回结果 && 方法发回[当前方法] != 0) 失败值("missing return");
            // 分支后的汇合点必须是实际指令，这是版本 49 验证器的要求。
            if (方法发回[当前方法] == 0) 发射值(177);
            else { boolean 整数 = 方法发回[当前方法] <= 2 || 方法发回[当前方法] == 5; 发射值(整数 ? 3 : 1); 发射值(整数 ? 172 : 176); }
            if (位置 != 方法结束[当前方法]) 失败值("invalid method body");
            方法局部变量列[当前方法] = 局部个数; 方法长度[当前方法] = 代码大小 - 方法代码[当前方法];
        }
        if (错误) return 1;
        写入类(); if (错误) return 1;
        文件名称文本[名称大小 - 4] = 'c'; 文件名称文本[名称大小 - 3] = 'l'; 文件名称文本[名称大小 - 2] = 'a';
        文件名称文本[名称大小 - 1] = 's'; 文件名称文本[名称大小] = 's'; 文件名称文本[名称大小 + 1] = 0;
        int 结果 = 用户.写入文件(文件名称文本, 输出, 输出大小);
        if (结果 < 0) { 用户.写入("javac: cannot save class: "); Java工具.写入编号(结果); 用户.写入字符值(10); return 1; }
        用户.写入("Compiled: "); for (int 数 = 0; 文件名称文本[数] != 0; 数++) 用户.写入字符值(文件名称文本[数]);
        用户.写入(" (JVM class version 49)\n"); return 0;
    }
}
