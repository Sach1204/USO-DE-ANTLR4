import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;

public class CalcApp {
    public static void main(String[] args) throws Exception {
        // Fuente de entrada: consola (stdin)
        CharStream input = CharStreams.fromStream(System.in);

        // Etapa léxica
        labeldExprLexer lexer = new labeldExprLexer(input);
        CommonTokenStream tokens = new CommonTokenStream(lexer);

        // Etapa de análisis sintáctico
        labeldExprParser parser = new labeldExprParser(tokens);
        ParseTree tree = parser.prog();

        // Visitador para evaluar las expresiones
        EvalVisitor visitor = new EvalVisitor();
        visitor.visit(tree);
    }
}
