// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 马来西亚.JMysOS.系统调用;

import 马来西亚.JMysOS.内存空间.页管理器;
import 马来西亚.JMysOS.任务.进程值;
import 马来西亚.JMysOS.任务.调度器;
import 马来西亚.JMysOS.文件系统.可执行文件加载器;
import 马来西亚.JMysOS.文件系统.文件系统;
import 马来西亚.JMysOS.文件系统.文件信息;
import 马来西亚.JMysOS.内核.硬件值;
import 马来西亚.JMysOS.输入值.输入管理器;
import 马来西亚.JMysOS.输入值.输入事件;

/** engos 第一阶段 POSIX 调用的 Java 管理层。 */
public final class 系统调用 {
    public static final int 读取仅用标志 = 0;
    public static final int 搜索开始 = 0;
    public static final int 搜索当前 = 1;
    public static final int 查找条目结束 = 2;

    private final 文件系统 文件系统;
    private final 页管理器 页管理工作;
    private final 调度器 调度器;
    private final 可执行文件加载器 加载器 = new 可执行文件加载器();
    private final 硬件值 设备;
    private final 输入管理器 输入管理工作;

    public 系统调用(文件系统 文件系统, 页管理器 页管理工作, 调度器 调度器, 硬件值 设备, 输入管理器 输入管理工作) {
        this.文件系统 = 文件系统;
        this.页管理工作 = 页管理工作;
        this.调度器 = 调度器;
        this.设备 = 设备;
        this.输入管理工作 = 输入管理工作;
    }

    public int 进程标识符(进程值 当前进程) {
        return 当前进程.标识符值();
    }

    public int 父进程标识符(进程值 当前进程) {
        return 当前进程.父标识符();
    }

    public int 打开(进程值 当前进程, String 名称, int 标志值) {
        if (标志值 != 读取仅用标志) {
            return -30;
        }
        return 当前进程.文件描述符().打开(名称);
    }

    public int 读取(进程值 当前进程, int 描述符条目, byte[] 接收目的地址, int 大小) {
        if (描述符条目 == 0) {
            if (大小 <= 0 || 接收目的地址.length == 0) {
                return 0;
            }
            输入事件 事件 = 输入管理工作.下一事件();
            if (事件 == null || 事件.事件种类() != 输入事件.种类值.键向下) {
                return -11;
            }
            接收目的地址[0] = (byte) 事件.首位值();
            return 1;
        }
        return 当前进程.文件描述符().读取(描述符条目, 接收目的地址, 大小);
    }

    public int 写入(进程值 当前进程, int 描述符条目, byte[] 数据, int 大小) {
        if (描述符条目 != 1 && 描述符条目 != 2) {
            return 当前进程.文件描述符().是否打开(描述符条目) ? -30 : -9;
        }
        if (大小 < 0 || 大小 > 数据.length) {
            return -22;
        }
        设备.串行输出(new String(数据, 0, 大小, java.nio.charset.StandardCharsets.UTF_8));
        return 大小;
    }

    public int 关闭(进程值 当前进程, int 描述符条目) {
        return 当前进程.文件描述符().关闭(描述符条目);
    }

    public int 移动位置(进程值 当前进程, int 描述符条目, int 距离值, int 项目根) {
        return 当前进程.文件描述符().移动位置(描述符条目, 距离值, 项目根);
    }

    public int 复制副本描述符(进程值 当前进程, int 描述符条目) {
        return 当前进程.文件描述符().已克隆描述符(描述符条目, 0);
    }

    public int 复制副本描述符位置(进程值 当前进程, int 描述符条目, int 新建描述符) {
        return 当前进程.文件描述符().复制副本位置(描述符条目, 新建描述符);
    }

    public int 是否可访问(String 名称, int 方法模式) {
        文件信息 系统信息 = 文件系统.系统信息(名称);
        if (系统信息 == null) {
            return -2;
        }
        if ((方法模式 & 1) != 0 && (系统信息.形状种类() & 0111) == 0) {
            return -13;
        }
        if ((方法模式 & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int 切换任务列表(String 名称) {
        return "/".equals(名称) ? 0 : -20;
    }

    public String 当前任务列表(int 接收大小) {
        return 接收大小 >= 2 ? "/" : null;
    }

    public int 用户标识符() { return 0; }
    public int 实效用户标识符() { return 0; }
    public int 组标识符() { return 0; }
    public int 实效组标识符() { return 0; }

    public int 同步化文件(进程值 当前进程, int 描述符条目) {
        return 当前进程.文件描述符().系统信息(描述符条目) == null ? -9 : 0;
    }

    public void 同步化全部() {
        // 当前文件系统只读，没有需要刷新的数据。
    }

    public boolean 是否终端(进程值 当前进程, int 描述符条目) {
        文件信息 系统信息 = 当前进程.文件描述符().系统信息(描述符条目);
        return 系统信息 != null && (系统信息.形状种类() & 0170000) == 0020000;
    }

    public int 文件控制(进程值 当前进程, int 描述符条目, int 命令, int 形参参数) {
        if (命令 == 0) {
            return 当前进程.文件描述符().已克隆描述符(描述符条目, 形参参数);
        }
        if (命令 == 1) {
            return 当前进程.文件描述符().关闭启用侧执行操作值(描述符条目);
        }
        if (命令 == 2) {
            return 当前进程.文件描述符().设定关闭启用侧执行操作(描述符条目, (形参参数 & 1) != 0);
        }
        if (命令 == 3) {
            return 当前进程.文件描述符().系统信息(描述符条目) == null ? -9 : 读取仅用标志;
        }
        if (命令 == 4) {
            return 形参参数 == 读取仅用标志 ? 0 : -30;
        }
        return -22;
    }

    public int 创建条目(String 名称, int 权限值) {
        return -30;
    }

    public 文件信息 描述符信息(进程值 当前进程, int 描述符条目) {
        return 当前进程.文件描述符().系统信息(描述符条目);
    }

    public 系统详情列 系统详情列() {
        return new 系统详情列("JMysOS", "JMysOS", "0.1", "Java managed kernel", "i386");
    }

    public 文件信息 文件信息(String 名称) {
        return 文件系统.系统信息(名称);
    }

    public 进程值 克隆进程(进程值 父值) {
        return 调度器.克隆值(父值);
    }

    public int 等待状态用于子(进程值 父值, int 子标识符, boolean 非阻塞) {
        return 调度器.等待状态用于子(父值, 子标识符, 非阻塞);
    }

    public int 程序跳出(进程值 当前进程, int 新建结束) {
        int 上一个结束 = 当前进程.程序跳出();
        if (新建结束 == 0) {
            return 上一个结束;
        }
        if (新建结束 < 0x06000000 || 新建结束 > 0x07000000) {
            return -12;
        }
        int 首位页 = 上一个结束 / 页管理器.页大小;
        int 最后页 = (新建结束 + 页管理器.页大小 - 1) / 页管理器.页大小;
        if (新建结束 > 上一个结束) {
            for (int 编号 = 首位页; 编号 < 最后页; 编号++) {
                int 地址 = 编号 * 页管理器.页大小;
                try {
                    页管理工作.读取字节值(当前进程.地址空间(), 地址);
                } catch (IllegalStateException 错误) {
                    页管理工作.映射表页(当前进程.地址空间(), 地址, true);
                }
            }
        }
        当前进程.设定程序跳出(新建结束);
        return 新建结束;
    }

    public int 增加程序跳出(进程值 当前进程, int 递增总量) {
        int 上一个结束 = 当前进程.程序跳出();
        int 结果 = 程序跳出(当前进程, 上一个结束 + 递增总量);
        return 结果 < 0 ? 结果 : 上一个结束;
    }

    public int 执行命令(进程值 当前进程, byte[] 可执行文件文件) {
        return 执行命令(当前进程, 可执行文件文件, new String[0], new String[0]);
    }

    public int 执行命令(进程值 当前进程, byte[] 可执行文件文件, String[] 形参参数, String[] 环境) {
        可执行文件加载器.映像 映像值;
        try {
            映像值 = 加载器.检查项(可执行文件文件);
        } catch (IllegalArgumentException 错误) {
            return -8;
        }
        if (形参参数 == null || 环境 == null || 形参参数.length > 16 || 环境.length > 16) {
            return -7;
        }
        for (可执行文件加载器.区段值 区段值 : 映像值.区段列列表()) {
            if ((区段值.标志值() & 2) == 0 || 区段值.大小() == 0) {
                continue;
            }
            int 首位页 = 区段值.地址() / 页管理器.页大小;
            int 最后页 = (区段值.地址() + 区段值.大小() + 页管理器.页大小 - 1) / 页管理器.页大小;
            for (int 编号 = 首位页; 编号 < 最后页; 编号++) {
                int 地址 = 编号 * 页管理器.页大小;
                try {
                    页管理工作.读取字节值(当前进程.地址空间(), 地址);
                    页管理工作.私有范围写入(当前进程.地址空间(), 地址, 页管理器.页大小);
                } catch (IllegalStateException 错误) {
                    页管理工作.映射表页(当前进程.地址空间(), 地址, true);
                }
            }
            for (int 编号 = 0; 编号 < 区段值.大小(); 编号++) {
                byte 值 = 区段值.种类值() == 8 ? 0 : 可执行文件文件[区段值.文件位置() + 编号];
                页管理工作.写入字节值(当前进程.地址空间(), 区段值.地址() + 编号, 值);
            }
        }
        当前进程.设定执行状态上下文(映像值.开始地址(), 形参参数, 环境);
        当前进程.文件描述符().关闭启用侧执行操作();
        return 0;
    }

    public void 结束程序(进程值 当前进程, int 状态值) {
        当前进程.退出程序(状态值);
    }
}
