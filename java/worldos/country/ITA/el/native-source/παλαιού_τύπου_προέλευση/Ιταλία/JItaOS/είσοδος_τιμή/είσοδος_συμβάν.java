// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ιταλία.JItaOS.είσοδος_τιμή;

public final class είσοδος_συμβάν {
    public enum 종류 {
        Κλειδί_εκτός_λειτουργίας,
        키놓음,
        쥐이동,
        쥐단추누름,
        쥐단추놓음
    }

    private final 종류 είδος_συμβάντος;
    private final int 첫째값;
    private final int 둘째값;

    public είσοδος_συμβάν(종류 είδος_συμβάντος, int 첫째값, int 둘째값) {
        this.είδος_συμβάντος = είδος_συμβάντος;
        this.첫째값 = 첫째값;
        this.둘째값 = 둘째값;
    }

    public 종류 είδος_συμβάντος() {
        return είδος_συμβάντος;
    }

    public int 첫째값() {
        return 첫째값;
    }

    public int 둘째값() {
        return 둘째값;
    }
}

