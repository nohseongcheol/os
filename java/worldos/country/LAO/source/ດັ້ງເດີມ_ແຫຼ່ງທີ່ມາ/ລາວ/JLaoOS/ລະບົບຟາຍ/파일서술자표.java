// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ລາວ.JLaoOS.ລະບົບຟາຍ;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 ຟາຍ 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final ລະບົບຟາຍ.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(ລະບົບຟາຍ.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final ລະບົບຟາຍ ລະບົບຟາຍ;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(ລະບົບຟາຍ ລະບົບຟາຍ) {
        this.ລະບົບຟາຍ = ລະບົບຟາຍ;
    }

    public int ສ້າງ(String ຊື່) {
        ລະບົບຟາຍ.열린파일 열린파일 = ລະບົບຟາຍ.ສ້າງ(ຊື່);
        if (열린파일 == null) {
            return -2;
        }
        int ດັດຊະນີ = ຫວ່າງ_ເປົ່າ_ດັດຊະນີ(3);
        if (ດັດຊະນີ < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(ດັດຊະນີ), new 서술자(열린파일));
        return ດັດຊະນີ;
    }

    public int 읽기(int ດັດຊະນີ, byte[] 받을곳, int ຂະ_ຫນາດ) {
        서술자 ເຂົ້າໃນ_ຄ່າ = 서술자들.get(Integer.valueOf(ດັດຊະນີ));
        if (ເຂົ້າໃນ_ຄ່າ == null) {
            return -9;
        }
        if (ຂະ_ຫນາດ < 0 || ຂະ_ຫນາດ > 받을곳.length) {
            return -22;
        }
        int 남음 = ເຂົ້າໃນ_ຄ່າ.열린파일.ຂໍ້ມູນ.length - ເຂົ້າໃນ_ຄ່າ.열린파일.ຈັດຕໍາແຫນ່ງ;
        int 읽을크기 = Math.min(ຂະ_ຫນາດ, Math.max(남음, 0));
        System.arraycopy(ເຂົ້າໃນ_ຄ່າ.열린파일.ຂໍ້ມູນ, ເຂົ້າໃນ_ຄ່າ.열린파일.ຈັດຕໍາແຫນ່ງ, 받을곳, 0, 읽을크기);
        ເຂົ້າໃນ_ຄ່າ.열린파일.ຈັດຕໍາແຫນ່ງ += 읽을크기;
        return 읽을크기;
    }

    public int 위치옮기기(int ດັດຊະນີ, int 거리, int ໂຄງ_ການ_ເລກຮາກ) {
        서술자 ເຂົ້າໃນ_ຄ່າ = 서술자들.get(Integer.valueOf(ດັດຊະນີ));
        if (ເຂົ້າໃນ_ຄ່າ == null) {
            return -9;
        }
        int ພື້ນຫຼັງ_ຄ່າ;
        if (ໂຄງ_ການ_ເລກຮາກ == 0) {
            ພື້ນຫຼັງ_ຄ່າ = 0;
        } else if (ໂຄງ_ການ_ເລກຮາກ == 1) {
            ພື້ນຫຼັງ_ຄ່າ = ເຂົ້າໃນ_ຄ່າ.열린파일.ຈັດຕໍາແຫນ່ງ;
        } else if (ໂຄງ_ການ_ເລກຮາກ == 2) {
            ພື້ນຫຼັງ_ຄ່າ = ເຂົ້າໃນ_ຄ່າ.열린파일.ຂໍ້ມູນ.length;
        } else {
            return -22;
        }
        int 새위치 = ພື້ນຫຼັງ_ຄ່າ + 거리;
        if (새위치 < 0) {
            return -22;
        }
        ເຂົ້າໃນ_ຄ່າ.열린파일.ຈັດຕໍາແຫນ່ງ = 새위치;
        return 새위치;
    }

    public int ປິດ(int ດັດຊະນີ) {
        서술자 ເຂົ້າໃນ_ຄ່າ = 서술자들.remove(Integer.valueOf(ດັດຊະນີ));
        if (ເຂົ້າໃນ_ຄ່າ == null) {
            return -9;
        }
        ເຂົ້າໃນ_ຄ່າ.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int ດັດຊະນີ, int 최소번호) {
        서술자 ເຂົ້າໃນ_ຄ່າ = 서술자들.get(Integer.valueOf(ດັດຊະນີ));
        if (ເຂົ້າໃນ_ຄ່າ == null) {
            return -9;
        }
        int 새번호 = ຫວ່າງ_ເປົ່າ_ດັດຊະນີ(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        ເຂົ້າໃນ_ຄ່າ.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(ເຂົ້າໃນ_ຄ່າ.열린파일));
        return 새번호;
    }

    public int 지정복제(int ດັດຊະນີ, int 새번호) {
        if (ດັດຊະນີ == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(ດັດຊະນີ)) ? ດັດຊະນີ : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(ດັດຊະນີ));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            ປິດ(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int ດັດຊະນີ, boolean ຄ່າ) {
        서술자 ເຂົ້າໃນ_ຄ່າ = 서술자들.get(Integer.valueOf(ດັດຊະນີ));
        if (ເຂົ້າໃນ_ຄ່າ == null) {
            return -9;
        }
        ເຂົ້າໃນ_ຄ່າ.실행시닫기 = ຄ່າ;
        return 0;
    }

    public int 실행시닫기값(int ດັດຊະນີ) {
        서술자 ເຂົ້າໃນ_ຄ່າ = 서술자들.get(Integer.valueOf(ດັດຊະນີ));
        if (ເຂົ້າໃນ_ຄ່າ == null) {
            return -9;
        }
        return ເຂົ້າໃນ_ຄ່າ.실행시닫기 ? 1 : 0;
    }

    public ຟາຍ_ຂໍ້_ມູນ ລະບົບ_ຂໍ້_ມູນ(int ດັດຊະນີ) {
        if (ດັດຊະນີ >= 0 && ດັດຊະນີ <= 2) {
            return new ຟາຍ_ຂໍ້_ມູນ(0, 0020666);
        }
        서술자 ເຂົ້າໃນ_ຄ່າ = 서술자들.get(Integer.valueOf(ດັດຊະນີ));
        if (ເຂົ້າໃນ_ຄ່າ == null) {
            return null;
        }
        return new ຟາຍ_ຂໍ້_ມູນ(ເຂົ້າໃນ_ຄ່າ.열린파일.ຂໍ້ມູນ.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer ດັດຊະນີ : 번호들) {
            서술자 ເຂົ້າໃນ_ຄ່າ = 서술자들.get(ດັດຊະນີ);
            if (ເຂົ້າໃນ_ຄ່າ != null && ເຂົ້າໃນ_ຄ່າ.실행시닫기) {
                ປິດ(ດັດຊະນີ.intValue());
            }
        }
    }

    public boolean ເທັກໂນໂລຢີຂໍ້ມູນຂ່າວສານ_ສ້າງ(int ດັດຊະນີ) {
        return 서술자들.containsKey(Integer.valueOf(ດັດຊະນີ));
    }

    public 파일서술자표 복제() {
        파일서술자표 ມາດຕະການ = new 파일서술자표(ລະບົບຟາຍ);
        for (Map.Entry<Integer, 서술자> ເຂົ້າໃນ_ຄ່າ : 서술자들.entrySet()) {
            ເຂົ້າໃນ_ຄ່າ.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(ເຂົ້າໃນ_ຄ່າ.getValue().열린파일);
            새서술자.실행시닫기 = ເຂົ້າໃນ_ຄ່າ.getValue().실행시닫기;
            ມາດຕະການ.서술자들.put(ເຂົ້າໃນ_ຄ່າ.getKey(), 새서술자);
        }
        return ມາດຕະການ;
    }

    private int ຫວ່າງ_ເປົ່າ_ດັດຊະນີ(int 최소번호) {
        for (int ດັດຊະນີ = Math.max(0, 최소번호); ດັດຊະນີ < 최대서술자; ດັດຊະນີ++) {
            if (!서술자들.containsKey(Integer.valueOf(ດັດຊະນີ))) {
                return ດັດຊະນີ;
            }
        }
        return -1;
    }
}
