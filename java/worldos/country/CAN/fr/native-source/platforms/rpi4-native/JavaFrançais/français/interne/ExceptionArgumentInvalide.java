// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;

/** ExceptionArgumentInvalide : exception pouvant être déclarée, levée et interceptée avec l’API française. */
public class ExceptionArgumentInvalide extends java.lang.IllegalArgumentException {
    public ExceptionArgumentInvalide() { super(); }
    public ExceptionArgumentInvalide(String description) { super(description); }
    public String description() { return getMessage(); }
}
