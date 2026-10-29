// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Τουρκία.JTurOS.συσκευή_αποθήκευσης;

import java.util.Arrays;

/** ATA 28비트 Εντολή 계층과 같은 512바이트 논리 ενότητα_τιμή 장치다. */
public final class 고급기술결합장치 {
    public static final int ενότητα_αλλάζω_μέγεθος = 512;
    private final byte[] δεδομένα;
    private final boolean μόνο_για_ανάγνωση_τιμή;

    public 고급기술결합장치(int 구역수, boolean μόνο_για_ανάγνωση_τιμή) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("ενότητα_τιμή 수가 올바르지 않습니다.");
        }
        δεδομένα = new byte[Math.multiplyExact(구역수, ενότητα_αλλάζω_μέγεθος)];
        this.μόνο_για_ανάγνωση_τιμή = μόνο_για_ανάγνωση_τιμή;
    }

    public int 구역수() {
        return δεδομένα.length / ενότητα_αλλάζω_μέγεθος;
    }

    public void Ανάγνωση(int ενότητα_Ευρετήριο, byte[] λαμβάνω_προορισμός) {
        ελέγχω_εύρος(ενότητα_Ευρετήριο, λαμβάνω_προορισμός);
        System.arraycopy(δεδομένα, ενότητα_Ευρετήριο * ενότητα_αλλάζω_μέγεθος, λαμβάνω_προορισμός, 0, ενότητα_αλλάζω_μέγεθος);
    }

    public void Εγγραφή(int ενότητα_Ευρετήριο, byte[] 쓸자료) {
        if (μόνο_για_ανάγνωση_τιμή) {
            throw new IllegalStateException("Ανάγνωση 전용 장치입니다.");
        }
        ελέγχω_εύρος(ενότητα_Ευρετήριο, 쓸자료);
        System.arraycopy(쓸자료, 0, δεδομένα, ενότητα_Ευρετήριο * ενότητα_αλλάζω_μέγεθος, ενότητα_αλλάζω_μέγεθος);
    }

    public void διαγράφω_καταχώρηση() {
        if (μόνο_για_ανάγνωση_τιμή) {
            throw new IllegalStateException("Ανάγνωση 전용 장치입니다.");
        }
        Arrays.fill(δεδομένα, (byte) 0);
    }

    private void ελέγχω_εύρος(int ενότητα_Ευρετήριο, byte[] 임시공간) {
        if (ενότητα_Ευρετήριο < 0 || ενότητα_Ευρετήριο >= 구역수() || 임시공간.length < ενότητα_αλλάζω_μέγεθος) {
            throw new IllegalArgumentException("ATA ενότητα_τιμή 범위가 올바르지 않습니다.");
        }
    }
}

