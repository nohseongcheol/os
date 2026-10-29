// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;

/** ÉchecArithmétique : exception pouvant être déclarée, levée et interceptée avec l’API française. */
public class ÉchecArithmétique extends java.lang.ArithmeticException {
    public ÉchecArithmétique() { super(); }
    public ÉchecArithmétique(String description) { super(description); }
    public String description() { return getMessage(); }
}
