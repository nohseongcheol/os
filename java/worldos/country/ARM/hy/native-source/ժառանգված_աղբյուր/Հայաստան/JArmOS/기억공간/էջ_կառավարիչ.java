// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Հայաստան.JArmOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB էջ_արժեք 연결과 Գրել 시 복사를 제공한다. */
public final class էջ_կառավարիչ {
    public static final int էջի_չափ = 4096;

    private static final class էջ_արժեք {
        private byte[] տվյալ = new byte[էջի_չափ];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class հասցե_տեղ {
        private final Map<Integer, էջ_արժեք> էջ_աղյուսակ = new HashMap<Integer, էջ_արժեք>();
    }

    public հասցե_տեղ 새주소공간() {
        return new հասցե_տեղ();
    }

    public void քարտեզանշել_էջ(հասցե_տեղ 공간, int վերիրական_հասցե, boolean 쓰기가능) {
        int դասիչ = 쪽번호(վերիրական_հասցե);
        էջ_արժեք 새쪽 = new էջ_արժեք();
        새쪽.쓰기가능 = 쓰기가능;
        공간.էջ_աղյուսակ.put(Integer.valueOf(դասիչ), 새쪽);
    }

    public հասցե_տեղ 쓰기시복사복제(հասցե_տեղ 원본) {
        հասցե_տեղ 복제본 = new հասցե_տեղ();
        for (Map.Entry<Integer, էջ_արժեք> մուտքագրում_արժեք : 원본.էջ_աղյուսակ.entrySet()) {
            էջ_արժեք 공유쪽 = մուտքագրում_արժեք.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.էջ_աղյուսակ.put(մուտքագրում_արժեք.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(հասցե_տեղ 공간, int վերիրական_հասցե) {
        էջ_արժեք թիրախ = գտնել_էջ(공간, վերիրական_հասցե);
        return թիրախ.տվյալ[Math.floorMod(վերիրական_հասցե, էջի_չափ)];
    }

    public void գրել_բայթ_արժեք(հասցե_տեղ 공간, int վերիրական_հասցե, byte արժեք) {
        int դասիչ = 쪽번호(վերիրական_հասցե);
        էջ_արժեք թիրախ = գտնել_էջ(공간, վերիրական_հասցե);
        if (!թիրախ.쓰기가능) {
            if (!թիրախ.쓰기시복사) {
                throw new IllegalStateException("Ընթերցում 전용 쪽입니다.");
            }
            թիրախ = Կերտի_ր_մասնավոր_էջ(공간, դասիչ, թիրախ);
        }
        թիրախ.տվյալ[Math.floorMod(վերիրական_հասցե, էջի_չափ)] = արժեք;
    }

    public void 범위개인쓰기(հասցե_տեղ 공간, int Մեկնարկ_հասցե, int Չափս) {
        if (Չափս < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int վերջացնել_հասցե = Math.addExact(Մեկնարկ_հասցե, Չափս);
        for (int հասցե = Մեկնարկ_հասցե; հասցե < վերջացնել_հասցե; հասցե = (쪽번호(հասցե) + 1) * էջի_չափ) {
            int դասիչ = 쪽번호(հասցե);
            էջ_արժեք թիրախ = գտնել_էջ(공간, հասցե);
            if (թիրախ.쓰기시복사) {
                Կերտի_ր_մասնավոր_էջ(공간, դասիչ, թիրախ);
            } else {
                թիրախ.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(հասցե_տեղ 공간, int Մեկնարկ_հասցե, byte[] տվյալ) {
        for (int դասիչ = 0; դասիչ < տվյալ.length; դասիչ++) {
            գրել_բայթ_արժեք(공간, Մեկնարկ_հասցե + դասիչ, տվյալ[դասիչ]);
        }
    }

    private էջ_արժեք Կերտի_ր_մասնավոր_էջ(հասցե_տեղ 공간, int դասիչ, էջ_արժեք 공유쪽) {
        էջ_արժեք մասնավոր_էջ = new էջ_արժեք();
        մասնավոր_էջ.տվյալ = Arrays.copyOf(공유쪽.տվյալ, 공유쪽.տվյալ.length);
        մասնավոր_էջ.쓰기가능 = true;
        մասնավոր_էջ.쓰기시복사 = false;
        공유쪽.참조수--;
        공간.էջ_աղյուսակ.put(Integer.valueOf(դասիչ), մասնավոր_էջ);
        return մասնավոր_էջ;
    }

    private էջ_արժեք գտնել_էջ(հասցե_տեղ 공간, int հասցե) {
        էջ_արժեք թիրախ = 공간.էջ_աղյուսակ.get(Integer.valueOf(쪽번호(հասցե)));
        if (թիրախ == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return թիրախ;
    }

    private int 쪽번호(int հասցե) {
        if (հասցե < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return հասցե / էջի_չափ;
    }
}

