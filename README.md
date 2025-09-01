# USO-DE-ANTLR4
# Calculadora en ANTLR4 en Java y en Python
Este proyecto implementa una calculadora basada en la gramática **`labeldExpr.g4`** spirada en el capítulo 4 del libro The Definitive ANTLR 4 Reference.
La aplicación fue extendida para soportar operaciones más complejas y puede ejecutarse tanto en **Java** como en **Python**.

# Características
La calculadora permite:
* Operaciones simples : `+`, `-`, `*`, `/`, `^`
* Factorial: `n!` 
* Funciones matemáticas:
* 
  * `sin(x)`, `cos(x)`, `tan(x)` (modo grados o radianes)
  * `sqrt(x)` → raíz cuadrada
  * `ln(x)` → logaritmo natural
  * `log(x)` → logaritmo base 10
* Cambio entre grados y radianes:

  * `deg()` → activa modo grados
  * `rad()` → activa modo radianes

# Ejecucion en Java

***Codigo Java Visitor***
```java
// EvalVisitor.java
import java.util.HashMap;
import java.util.Map;

public class EvalVisitor extends labeldExprBaseVisitor<Double> {
    private final Map<String, Double> memory = new HashMap<>();
    // true = trabajar en grados, false = radianes (arranca en radianes)
    private boolean degreesMode = false;

    // --- Utilidad para convertir si se requiere ---
    private double adaptAngle(double x) {
        return degreesMode ? Math.toRadians(x) : x;
    }

    // --- Asignación de valores a variables ---
    @Override
    public Double visitAssign(labeldExprParser.AssignContext ctx) {
        String var = ctx.ID().getText();
        Double val = visit(ctx.expr());
        memory.put(var, val);
        return val;
    }

    // --- Mostrar resultados en pantalla ---
    @Override
    public Double visitPrintExpr(labeldExprParser.PrintExprContext ctx) {
        Double res = visit(ctx.expr());
        System.out.println(res);
        return 0.0;
    }

    // --- Literales numéricos ---
    @Override
    public Double visitInt(labeldExprParser.IntContext ctx) {
        return Double.valueOf(ctx.getText());
    }

    @Override
    public Double visitFloat(labeldExprParser.FloatContext ctx) {
        return Double.valueOf(ctx.getText());
    }

    // --- Variables y constantes ---
    @Override
    public Double visitId(labeldExprParser.IdContext ctx) {
        String id = ctx.ID().getText();
        if (memory.containsKey(id)) return memory.get(id);
        if (id.equalsIgnoreCase("PI")) return Math.PI;
        if (id.equalsIgnoreCase("E")) return Math.E;
        return 0.0;
    }

    // --- Expresiones entre paréntesis ---
    @Override
    public Double visitParens(labeldExprParser.ParensContext ctx) {
        return visit(ctx.expr());
    }

    // --- Negativo unario ---
    @Override
    public Double visitUnaryMinus(labeldExprParser.UnaryMinusContext ctx) {
        return -visit(ctx.expr());
    }

    // --- Suma y resta ---
    @Override
    public Double visitAddSub(labeldExprParser.AddSubContext ctx) {
        Double left = visit(ctx.expr(0));
        Double right = visit(ctx.expr(1));
        return ctx.op.getText().equals("+") ? left + right : left - right;
    }

    // --- Multiplicación y división ---
    @Override
    public Double visitMulDiv(labeldExprParser.MulDivContext ctx) {
        Double left = visit(ctx.expr(0));
        Double right = visit(ctx.expr(1));
        if (ctx.op.getText().equals("*")) {
            return left * right;
        } else {
            if (right == 0.0) {
                throw new ArithmeticException("Error: división entre cero");
            }
            return left / right;
        }
    }

    // --- Potencias ---
    @Override
    public Double visitPowExpr(labeldExprParser.PowExprContext ctx) {
        Double base = visit(ctx.expr(0));
        Double exponent = visit(ctx.expr(1));
        return Math.pow(base, exponent);
    }

    // --- Factorial ---
    @Override
    public Double visitFactorial(labeldExprParser.FactorialContext ctx) {
        Double v = visit(ctx.expr());
        return (double) factorial((int) Math.floor(v));
    }

    private long factorial(int n) {
        if (n < 0) throw new RuntimeException("Factorial de número negativo no permitido");
        long result = 1;
        for (int i = 2; i <= n; i++) result *= i;
        return result;
    }

    // --- Llamadas a funciones ---
    @Override
    public Double visitFunc(labeldExprParser.FuncContext ctx) {
        String fname = ctx.funcCall().ID().getText();
        labeldExprParser.ArgListContext args = ctx.funcCall().argList();
        double a = 0, b = 0;
        if (args != null) {
            java.util.List<labeldExprParser.ExprContext> list = args.expr();
            if (list.size() >= 1) a = visit(list.get(0));
            if (list.size() >= 2) b = visit(list.get(1));
        }

        switch (fname.toLowerCase()) {
            case "sin": return Math.sin(adaptAngle(a));
            case "cos": return Math.cos(adaptAngle(a));
            case "tan": return Math.tan(adaptAngle(a));
            case "sqrt": return Math.sqrt(a);
            case "ln": return Math.log(a);
            case "log": return Math.log10(a);
            case "deg":
                degreesMode = true;
                return 0.0;
            case "rad":
                degreesMode = false;
                return 0.0;
            default:
                throw new RuntimeException("Función no reconocida: " + fname);
        }
    }
}
```
***Codigo Java Calculadora***
```java
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
```
***Codigo Python Calculadora***
```python

```

