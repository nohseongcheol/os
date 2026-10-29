// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中国澳门特别行政区.JMacOS.文件系统;

import java.util.HashMap;
import java.util.Map;

/** 保留各进程独立的描述符和可共享的打开文件描述。 */
public final class 文件描述符表 {
    private static final int 最大描述符 = 32;

    private static final class 描述符条目 {
        private final 文件系统.已打开文件 已打开文件;
        private boolean 关闭启用侧执行操作;

        描述符条目(文件系统.已打开文件 已打开文件) {
            this.已打开文件 = 已打开文件;
        }
    }

    private final 文件系统 文件系统;
    private final Map<Integer, 描述符条目> 描述符条目列 = new HashMap<Integer, 描述符条目>();

    public 文件描述符表(文件系统 文件系统) {
        this.文件系统 = 文件系统;
    }

    public int 打开(String 名称) {
        文件系统.已打开文件 已打开文件 = 文件系统.打开(名称);
        if (已打开文件 == null) {
            return -2;
        }
        int 编号 = 空索引(3);
        if (编号 < 0) {
            return -24;
        }
        描述符条目列.put(Integer.valueOf(编号), new 描述符条目(已打开文件));
        return 编号;
    }

    public int 读取(int 编号, byte[] 接收目的地址, int 大小) {
        描述符条目 条目值 = 描述符条目列.get(Integer.valueOf(编号));
        if (条目值 == null) {
            return -9;
        }
        if (大小 < 0 || 大小 > 接收目的地址.length) {
            return -22;
        }
        int 余数数据 = 条目值.已打开文件.数据.length - 条目值.已打开文件.位置;
        int 读取大小 = Math.min(大小, Math.max(余数数据, 0));
        System.arraycopy(条目值.已打开文件.数据, 条目值.已打开文件.位置, 接收目的地址, 0, 读取大小);
        条目值.已打开文件.位置 += 读取大小;
        return 读取大小;
    }

    public int 移动位置(int 编号, int 距离值, int 项目根) {
        描述符条目 条目值 = 描述符条目列.get(Integer.valueOf(编号));
        if (条目值 == null) {
            return -9;
        }
        int 背景值;
        if (项目根 == 0) {
            背景值 = 0;
        } else if (项目根 == 1) {
            背景值 = 条目值.已打开文件.位置;
        } else if (项目根 == 2) {
            背景值 = 条目值.已打开文件.数据.length;
        } else {
            return -22;
        }
        int 新建位置 = 背景值 + 距离值;
        if (新建位置 < 0) {
            return -22;
        }
        条目值.已打开文件.位置 = 新建位置;
        return 新建位置;
    }

    public int 关闭(int 编号) {
        描述符条目 条目值 = 描述符条目列.remove(Integer.valueOf(编号));
        if (条目值 == null) {
            return -9;
        }
        条目值.已打开文件.引用个数--;
        return 0;
    }

    public int 已克隆描述符(int 编号, int 最小编号) {
        描述符条目 条目值 = 描述符条目列.get(Integer.valueOf(编号));
        if (条目值 == null) {
            return -9;
        }
        int 新建编号 = 空索引(最小编号);
        if (新建编号 < 0) {
            return -24;
        }
        条目值.已打开文件.引用个数++;
        描述符条目列.put(Integer.valueOf(新建编号), new 描述符条目(条目值.已打开文件));
        return 新建编号;
    }

    public int 复制副本位置(int 编号, int 新建编号) {
        if (编号 == 新建编号) {
            return 描述符条目列.containsKey(Integer.valueOf(编号)) ? 编号 : -9;
        }
        if (新建编号 < 0 || 新建编号 >= 最大描述符) {
            return -9;
        }
        描述符条目 原始 = 描述符条目列.get(Integer.valueOf(编号));
        if (原始 == null) {
            return -9;
        }
        if (描述符条目列.containsKey(Integer.valueOf(新建编号))) {
            关闭(新建编号);
        }
        原始.已打开文件.引用个数++;
        描述符条目列.put(Integer.valueOf(新建编号), new 描述符条目(原始.已打开文件));
        return 新建编号;
    }

    public int 设定关闭启用侧执行操作(int 编号, boolean 值) {
        描述符条目 条目值 = 描述符条目列.get(Integer.valueOf(编号));
        if (条目值 == null) {
            return -9;
        }
        条目值.关闭启用侧执行操作 = 值;
        return 0;
    }

    public int 关闭启用侧执行操作值(int 编号) {
        描述符条目 条目值 = 描述符条目列.get(Integer.valueOf(编号));
        if (条目值 == null) {
            return -9;
        }
        return 条目值.关闭启用侧执行操作 ? 1 : 0;
    }

    public 文件信息 系统信息(int 编号) {
        if (编号 >= 0 && 编号 <= 2) {
            return new 文件信息(0, 0020666);
        }
        描述符条目 条目值 = 描述符条目列.get(Integer.valueOf(编号));
        if (条目值 == null) {
            return null;
        }
        return new 文件信息(条目值.已打开文件.数据.length, 0100444);
    }

    public void 关闭启用侧执行操作() {
        Integer[] 编号列表 = 描述符条目列.keySet().toArray(new Integer[0]);
        for (Integer 编号 : 编号列表) {
            描述符条目 条目值 = 描述符条目列.get(编号);
            if (条目值 != null && 条目值.关闭启用侧执行操作) {
                关闭(编号.intValue());
            }
        }
    }

    public boolean 是否打开(int 编号) {
        return 描述符条目列.containsKey(Integer.valueOf(编号));
    }

    public 文件描述符表 克隆值() {
        文件描述符表 结果 = new 文件描述符表(文件系统);
        for (Map.Entry<Integer, 描述符条目> 条目值 : 描述符条目列.entrySet()) {
            条目值.getValue().已打开文件.引用个数++;
            描述符条目 新建描述符 = new 描述符条目(条目值.getValue().已打开文件);
            新建描述符.关闭启用侧执行操作 = 条目值.getValue().关闭启用侧执行操作;
            结果.描述符条目列.put(条目值.getKey(), 新建描述符);
        }
        return 结果;
    }

    private int 空索引(int 最小编号) {
        for (int 编号 = Math.max(0, 最小编号); 编号 < 最大描述符; 编号++) {
            if (!描述符条目列.containsKey(Integer.valueOf(编号))) {
                return 编号;
            }
        }
        return -1;
    }
}
