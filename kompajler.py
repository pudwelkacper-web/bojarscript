import os
import sys

################################
#  kompajler bojarscript v1.2  #
################################



#eksypyry
def expr_replace(s):
    s = s.replace("Tak", "True")
    s = s.replace("Nie", "False")
    s = s.replace("nic", "None")
    s = s.replace("&&", " and ")
    s = s.replace("||", " or ")
    s = s.replace("!", "not ")
    return s

#stripowanie tekstu
def strip(s):
    return s.strip()

#process statementy
def process_statement(s):
    s = strip(s)
    if not s:
        return None
    if s.startswith("zhakuj "):
        im = s[6:].strip()
        return f"import {im}"
    if s.startswith("ledzio "):
        body = s[6:].strip()
        if "=" in body:
            name, expr = body.split("=", 1)
            return f"{strip(name)} = {strip(expr_replace(expr))}"
        return strip(expr_replace(body))
    if s.startswith("pentium "):
        expr = s[7:].strip()
        return f"print({expr_replace(expr)})"
    if s.startswith("@start_bojar"):
        cond = s[11:].strip()
        tx = "wykonywanie woli profesora, bojarscript v21.37"
        return f"print('{tx}')"
    if s.startswith("grabos "):
        expr = s[7:].strip()
        return f"return {expr_replace(expr)}"
    if s == "fbi":
        return "break"
    if s == "mossad":
        return "continue"
    return expr_replace(s)

#procces headery
def process_header(s):
    s = strip(s)
    if not s:
        return None
    if s.startswith("hybix "):
        rest = s[5:].strip()
        if "(" in rest and ")" in rest:
            idx = rest.find("(")
            name = strip(rest[:idx])
            params = rest[idx+1:rest.rfind(")")]
        else:
            name = strip(rest)
            params = ""
        return f"def {name}({params}):"
    if s.startswith("bojar "):
        cond = s[6:].strip()
        return f"if {expr_replace(cond)}:"
    if s.startswith("cia "):
        cond = s[4:].strip()
        return f"while {expr_replace(cond)}:"
    if s.startswith("ciax "):
        cond = s[5:].strip()
        return f"for {expr_replace(cond)}:"
    if s == "geniusze" or s.startswith("geniusze "):
        return "else:"
    if s.startswith("rozpłucie "):
        name = s[10:].strip()
        return f"class {name}:"
    return expr_replace(s) + ":"

#tłumaczonko kodu
def transpile(text):
    lines = []
    cur = []
    indent = 0
    i = 0
    n = len(text)
    in_string = False
    quote = ""
    while i < n:
        c = text[i]
        if in_string:
            cur.append(c)
            if c == quote:
                in_string = False
                quote = ""
            i += 1
            continue
        if c in ('"', "'"):
            in_string = True
            quote = c
            cur.append(c)
            i += 1
            continue
        if c == ";":
            s = "".join(cur)
            cur = []
            stmt = process_statement(s)
            if stmt is not None:
                lines.append(("    " * indent) + stmt)
            i += 1
            continue
        if c == "{":
            s = "".join(cur)
            cur = []
            header = process_header(s)
            if header is not None:
                lines.append(("    " * indent) + header)
            indent += 1
            i += 1
            continue
        if c == "}":
            s = "".join(cur)
            cur = []
            if strip(s):
                stmt = process_statement(s)
                if stmt is not None:
                    lines.append(("    " * indent) + stmt)
            indent = max(0, indent - 1)
            i += 1
            continue
        if c in ("\r", "\n"):
            i += 1
            continue
        cur.append(c)
        i += 1
    if strip("".join(cur)):
        stmt = process_statement("".join(cur))
        if stmt is not None:
            lines.append(("    " * indent) + stmt)
    return "\n".join(lines)

#główna funkcja compilera
def main():
    filename = input("Podaj plik .boj: ").strip()
    if not filename.endswith(".boj"):
        print("Plik musi mieć rozszerzenie .boj")
        return
    if not os.path.exists(filename):
        print("Nie znaleziono pliku")
        return
    with open(filename, "r", encoding="utf-8") as f:
        src = f.read()
    py_code = transpile(src)
    output_path = os.path.splitext(filename)[0] + ".py"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(py_code)
    print(f"Wygenerowano: {output_path}")
    exec(py_code, {})

if __name__ == "__main__":
    main()
