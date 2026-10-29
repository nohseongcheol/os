// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;

/** ExceptionConversionTypeType : exception pouvant être déclarée, levée et interceptée avec l’API française. */
public class ExceptionConversionTypeType extends java.lang.ClassCastException {
    public ExceptionConversionTypeType() { super(); }
    public ExceptionConversionTypeType(String description) { super(description); }
    public String description() { return getMessage(); }
}
