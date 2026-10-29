// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中國香港特別行政區.JHkgOS.中斷;

import java.util.Arrays;

/** 負責 IDT 的 Java 管理側處理器登錄與分派。 */
public final class 中斷管理器 {
    private final 中斷處理程序[] 處理程序列表 = new 中斷處理程序[256];
    private boolean 活躍;

    public void 登記(int 編號, 中斷處理程序 處理程序) {
        驗證編號(編號);
        處理程序列表[編號] = 處理程序;
    }

    public void 釋放存儲裝置(int 編號) {
        驗證編號(編號);
        處理程序列表[編號] = null;
    }

    public int 分派值(int 編號, int 已保存棧地址) {
        驗證編號(編號);
        if (!活躍) {
            return 已保存棧地址;
        }
        中斷處理程序 處理程序 = 處理程序列表[編號];
        return 處理程序 == null ? 已保存棧地址 : 處理程序.程序值條目(已保存棧地址);
    }

    public void 啓用() {
        活躍 = true;
    }

    public void 停用() {
        活躍 = false;
    }

    public boolean 是否活躍() {
        return 活躍;
    }

    public void 釋放全部() {
        Arrays.fill(處理程序列表, null);
    }

    private void 驗證編號(int 編號) {
        if (編號 < 0 || 編號 >= 處理程序列表.length) {
            throw new IllegalArgumentException("中斷 번호가 올바르지 않습니다.");
        }
    }
}

