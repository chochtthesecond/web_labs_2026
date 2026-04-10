import re
import os
import html

class Template:
    def __init__(self, template_dir='templates'):
        self.template_dir = template_dir

    def render(self, template_name, context=None):
        context = context or {}
        path = os.path.join(self.template_dir, template_name)
        with open(path, 'r', encoding='utf-8') as f:
            template = f.read()

        #наследование
        template = self._handle_extends(template)
        #конвертирование шаблона в код
        code = self._convert_to_python(template)

        #запись переменных
        def write(text):
            output.append(str(text))

        output = []
        exec_globals = {
            '__builtins__': {'__build_class__': None},
            #html.escape экранирует &, <, >, ", '
            'escape': lambda x: html.escape(str(x), quote=True),
            'write': write,
        }
        #вставляем переменные в глобальное пространство имен
        exec_globals.update(context)

        #выполняем код
        compiled = compile(code, '<template>', 'exec')
        exec(compiled, exec_globals)

        return ''.join(output)

    def _handle_extends(self, template):
        ext_match = re.search(r"{%\s*extends\s+['\"](.+?)['\"]\s*%}", template)
        if not ext_match:
            return template
        base_name = ext_match.group(1)
        base_path = os.path.join(self.template_dir, base_name)
        with open(base_path, 'r', encoding='utf-8') as f:
            base = f.read()

        #извлекаем блоки из шаблона потомка
        blocks = {}
        def replace_block(m):
            name = m.group(1)
            content = m.group(2)
            blocks[name] = content
            return ''
        child_no_blocks = re.sub(r"{%\s*block\s+(\w+)\s*%}(.*?){%\s*endblock\s*%}", replace_block, template, flags=re.DOTALL)

        #вставляем блоки в базовый шаблон
        for name, content in blocks.items():
            base = re.sub(r"{%\s*block\s+" + name + r"\s*%}.*?{%\s*endblock\s*%}", content, base, flags=re.DOTALL)

        #убираем extend
        base = re.sub(r"{%\s*extends\s+['\"].+?['\"]\s*%}", '', base)
        return base

    def _convert_to_python(self, template):
        #преобразуем строчный шаблон в код с помощью render()
        lines = []
        lines.append("def _render():")
        indent = 1

        #разделяем на текст и теги шаблона
        tokens = re.split(r"({{.*?}}|{%.*?%})", template, flags=re.DOTALL)

        for token in tokens:
            if not token:
                continue

            if token.startswith('{{') and token.endswith('}}'):
                #применяем полное экранирование для переменных
                expr = token[2:-2].strip()
                lines.append("    " * indent + f"write(escape({expr}))")

            elif token.startswith('{%') and token.endswith('%}'):
                #обрабатываем тег шаблона
                tag = token[2:-2].strip()

                if tag.startswith('for '):
                    parts = tag[4:].split(' in ')
                    var = parts[0].strip()
                    iterable = parts[1].strip()
                    lines.append("    " * indent + f"for {var} in {iterable}:")
                    indent += 1

                elif tag.startswith('if '):
                    condition = tag[3:]
                    lines.append("    " * indent + f"if {condition}:")
                    indent += 1

                elif tag.startswith('elif '):
                    condition = tag[5:]
                    indent -= 1
                    lines.append("    " * indent + f"elif {condition}:")
                    indent += 1

                elif tag == 'else':
                    indent -= 1
                    lines.append("    " * indent + "else:")
                    indent += 1

                elif tag == 'endfor':
                    indent -= 1

                elif tag == 'endif':
                    indent -= 1

            else:
                #экранируем текст
                text = token.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
                lines.append("    " * indent + f'write("{text}")')

        #вызываем _render()
        lines.append("_render()")
        return '\n'.join(lines)