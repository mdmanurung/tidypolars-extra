"""Generate the code reference pages and navigation."""

from __future__ import annotations

import ast
import importlib.util
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple
import re
import mkdocs_gen_files


@dataclass
class DocumentedMethod:
    name: str
    signature: str

@dataclass
class DocumentedClass:
    name: str
    has_docstring: bool
    signature: str
    init_signature: str | None
    methods: List[DocumentedMethod]

@dataclass
class DocumentedFunction:
    name: str
    signature: str


def _format_annotation(annotation: ast.AST | None) -> str:
    if annotation is None:
        return ""
    return ast.unparse(annotation)


def _format_default(value: ast.AST) -> str:
    return ast.unparse(value)


def _format_arguments(arguments: ast.arguments) -> str:
    parts: List[str] = []

    positional: List[ast.arg] = list(arguments.posonlyargs) + list(arguments.args)
    defaults: List[ast.AST | None] = [None] * (len(positional) - len(arguments.defaults)) + list(arguments.defaults)

    posonly_count = len(arguments.posonlyargs)

    for index, (arg, default) in enumerate(zip(positional, defaults)):
        text = arg.arg
        annotation = _format_annotation(arg.annotation)
        if annotation:
            text += f": {annotation}"
        if default is not None:
            text += f" = {_format_default(default)}"
        parts.append(text)
        if posonly_count and index + 1 == posonly_count:
            parts.append("/")

    if arguments.vararg is not None:
        text = f"*{arguments.vararg.arg}"
        annotation = _format_annotation(arguments.vararg.annotation)
        if annotation:
            text += f": {annotation}"
        parts.append(text)
    elif arguments.kwonlyargs:
        parts.append("*")

    for kwarg, default in zip(arguments.kwonlyargs, arguments.kw_defaults):
        text = kwarg.arg
        annotation = _format_annotation(kwarg.annotation)
        if annotation:
            text += f": {annotation}"
        if default is not None:
            text += f" = {_format_default(default)}"
        parts.append(text)

    if arguments.kwarg is not None:
        text = f"**{arguments.kwarg.arg}"
        annotation = _format_annotation(arguments.kwarg.annotation)
        if annotation:
            text += f": {annotation}"
        parts.append(text)

    return ", ".join(parts)


def _format_function_signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
    arguments = _format_arguments(node.args)
    signature = f"{prefix} {node.name}({arguments})"
    return_annotation = _format_annotation(node.returns)
    if return_annotation:
        signature += f" -> {return_annotation}"
    return signature


def _format_class_signature(node: ast.ClassDef) -> str:
    bases = [ast.unparse(base) for base in node.bases]
    keywords = []
    for keyword in node.keywords:
        value = ast.unparse(keyword.value)
        if keyword.arg is None:
            keywords.append(f"**{value}")
        else:
            keywords.append(f"{keyword.arg}={value}")
    inheritances = bases + keywords
    if inheritances:
        return f"class {node.name}({', '.join(inheritances)})"
    return f"class {node.name}"


def _get_documented_members(tree: ast.AST) -> Tuple[List[DocumentedClass], List[DocumentedFunction]]:
    classes: List[DocumentedClass] = []
    functions: List[DocumentedFunction] = []

    for node in getattr(tree, "body", []):
        if isinstance(node, ast.ClassDef):
            class_doc = ast.get_docstring(node)
            methods: List[DocumentedMethod] = []
            init_signature: str | None = None
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) and ast.get_docstring(child):
                    methods.append(
                        DocumentedMethod(
                            name=child.name,
                            signature=_format_function_signature(child),
                        )
                    )
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) and child.name == "__init__":
                    init_signature = _format_function_signature(child)
            methods.sort(key=lambda m: m.name)
            if class_doc or methods:
                classes.append(
                    DocumentedClass(
                        name=node.name,
                        has_docstring=bool(class_doc),
                        signature=_format_class_signature(node),
                        init_signature=init_signature,
                        methods=methods,
                    )
                )
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if ast.get_docstring(node):
                functions.append(
                    DocumentedFunction(
                        name=node.name,
                        signature=_format_function_signature(node),
                    )
                )

    classes.sort(key=lambda c: c.name)
    functions.sort(key=lambda f: f.name)

    return classes, functions


def _symbol_html(symbol_kind: str) -> str:
    return f"<code class='doc-symbol doc-symbol-toc doc-symbol-{symbol_kind}'></code>"


def _load_api_labels(src_dir: Path) -> dict[str, str]:
    init_path = src_dir / "__init__.py"
    if not init_path.is_file():
        return {}

    spec = importlib.util.spec_from_file_location(MODULE_NAME, init_path)
    if spec is None or spec.loader is None:
        return {}

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    labels = getattr(module, "API_labels", {})
    if not isinstance(labels, dict):
        return {}

    return {str(key): str(value) for key, value in labels.items()}


def _write_doc_page(
    doc_path: Path,
    ident: str,
    symbol_kind: str,
    heading_title: str | None,
    signature: str | None,
    edit_path: Path,
    directive_options: str | None = None,
) -> None:
    with mkdocs_gen_files.open(doc_path, "w") as fd:
        if heading_title:
            if signature:
                fd.write(f"## Signature\n\n")
                fd.write(f"```python\n")
                fd.write(signature)
                fd.write("\n```\n\n")
        fd.write(f"::: {ident}\n")
        if directive_options:
            fd.write(directive_options)
    mkdocs_gen_files.set_edit_path(doc_path, edit_path)


# Configuration
nav = mkdocs_gen_files.Nav()
MODULE_NAME = "tidypolars_extra"
root = Path(__file__).parent.parent.parent
src = root / MODULE_NAME


api_labels = _load_api_labels(src)


for path in sorted(src.rglob("*.py")):
    module_path = path.relative_to(src).with_suffix("")
    module_ident_parts = tuple(module_path.parts)
    module_file_stem = path.stem

    if module_ident_parts[-1] in {"__init__"}:
        continue

    module_doc_parts = module_ident_parts
    if module_doc_parts[-1] == "__main__":
        module_doc_parts = module_doc_parts[:-1] + ("index",)

    module_label = api_labels.get(module_file_stem, module_doc_parts[-1])
    module_nav_parts = module_doc_parts[:-1] + (str(module_label),)

    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    classes, functions = _get_documented_members(tree)

    module_edit_path = path.relative_to(root)

    for documented_class in classes:
        class_name = documented_class.name
        class_doc_parts = module_doc_parts + (class_name,)
        class_ident = ".".join(module_ident_parts + (class_name,))
        class_nav_key = module_nav_parts + (f"{_symbol_html('class')} {class_name}",)
        if documented_class.has_docstring:
            class_doc_path = Path("reference", *class_doc_parts).with_suffix(".md")
            nav[class_nav_key] = Path(*class_doc_parts).with_suffix(".md").as_posix()
            class_signature = documented_class.signature
            if documented_class.init_signature:
                class_signature = f"{class_signature}\n{documented_class.init_signature}"
            _write_doc_page(
                class_doc_path,
                class_ident,
                "class",
                class_name,
                class_signature,
                module_edit_path,
                directive_options="    options:\n      members: []\n",
            )

        for method in documented_class.methods:
            method_name = method.name
            method_doc_parts = class_doc_parts + (method_name,)
            method_ident = ".".join(module_ident_parts + (class_name, method_name))
            method_doc_path = Path("reference", *method_doc_parts).with_suffix(".md")
            method_nav_key = class_nav_key + (f"{_symbol_html('method')} {method_name}",)
            nav[method_nav_key] = Path(*method_doc_parts).with_suffix(".md").as_posix()
            _write_doc_page(
                method_doc_path,
                method_ident,
                "method",
                method_name,
                method.signature,
                module_edit_path,
            )

    for function in functions:
        function_name = function.name
        function_doc_parts = module_doc_parts + (function_name,)
        function_ident = ".".join(module_ident_parts + (function_name,))
        function_doc_path = Path("reference", *function_doc_parts).with_suffix(".md")
        function_nav_key = module_nav_parts + (f"{_symbol_html('function')} {function_name}",)
        nav[function_nav_key] = Path(*function_doc_parts).with_suffix(".md").as_posix()
        _write_doc_page(
            function_doc_path,
            function_ident,
            "function",
            function_name,
            function.signature,
            module_edit_path,
        )

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
