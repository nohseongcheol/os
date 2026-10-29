// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Канада.JCanOS.пристрій_збереження_даних;

import java.util.Arrays;

/** ATA 28비트 команда 계층과 같은 512바이트 논리 розділ_значення_366e0bfa 장치다. */
public final class 고급기술결합장치 {
    public static final int розділ_змінювати_розмір = 512;
    private final byte[] дані;
    private final boolean лише_для_читання_значення;

    public 고급기술결합장치(int 구역수, boolean лише_для_читання_значення) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("розділ_значення_366e0bfa 수가 올바르지 않습니다.");
        }
        дані = new byte[Math.multiplyExact(구역수, розділ_змінювати_розмір)];
        this.лише_для_читання_значення = лише_для_читання_значення;
    }

    public int 구역수() {
        return дані.length / розділ_змінювати_розмір;
    }

    public void Читання(int розділ_індекс, byte[] отримувати_місце) {
        перевіряти_діапазон(розділ_індекс, отримувати_місце);
        System.arraycopy(дані, розділ_індекс * розділ_змінювати_розмір, отримувати_місце, 0, розділ_змінювати_розмір);
    }

    public void Запис(int розділ_індекс, byte[] 쓸자료) {
        if (лише_для_читання_значення) {
            throw new IllegalStateException("Читання 전용 장치입니다.");
        }
        перевіряти_діапазон(розділ_індекс, 쓸자료);
        System.arraycopy(쓸자료, 0, дані, розділ_індекс * розділ_змінювати_розмір, розділ_змінювати_розмір);
    }

    public void видаляти_запис() {
        if (лише_для_читання_значення) {
            throw new IllegalStateException("Читання 전용 장치입니다.");
        }
        Arrays.fill(дані, (byte) 0);
    }

    private void перевіряти_діапазон(int розділ_індекс, byte[] 임시공간) {
        if (розділ_індекс < 0 || розділ_індекс >= 구역수() || 임시공간.length < розділ_змінювати_розмір) {
            throw new IllegalArgumentException("ATA розділ_значення_366e0bfa 범위가 올바르지 않습니다.");
        }
    }
}

