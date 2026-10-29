// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 新加坡.JSgpOS.中断;

import java.util.Arrays;

/** 负责 IDT 的 Java 管理侧处理器注册与分派。 */
public final class 中断管理器 {
    private final 中断处理程序[] 处理程序列表 = new 中断处理程序[256];
    private boolean 活跃;

    public void 登记(int 编号, 中断处理程序 处理程序) {
        验证编号(编号);
        处理程序列表[编号] = 处理程序;
    }

    public void 释放存储装置(int 编号) {
        验证编号(编号);
        处理程序列表[编号] = null;
    }

    public int 分派值(int 编号, int 已保存栈地址) {
        验证编号(编号);
        if (!活跃) {
            return 已保存栈地址;
        }
        中断处理程序 处理程序 = 处理程序列表[编号];
        return 处理程序 == null ? 已保存栈地址 : 处理程序.进程值条目(已保存栈地址);
    }

    public void 启用() {
        活跃 = true;
    }

    public void 停用() {
        活跃 = false;
    }

    public boolean 是否活跃() {
        return 活跃;
    }

    public void 释放全部() {
        Arrays.fill(处理程序列表, null);
    }

    private void 验证编号(int 编号) {
        if (编号 < 0 || 编号 >= 处理程序列表.length) {
            throw new IllegalArgumentException("中断 번호가 올바르지 않습니다.");
        }
    }
}

