// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ρουμανία.JRouOS.σύστημα_αρχείων;

public final class Αρχείο_πληροφορία {
    private final int Μέγεθος;
    private final int 형태;

    public Αρχείο_πληροφορία(int Μέγεθος, int 형태) {
        this.Μέγεθος = Μέγεθος;
        this.형태 = 형태;
    }

    public int Μέγεθος() {
        return Μέγεθος;
    }

    public int 형태() {
        return 형태;
    }
}

