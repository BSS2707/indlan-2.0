"""
IndLan Python Bridge
Provides generic dynamic Python module importing, Hindi-English alias resolution,
transparent object wrappers, and missing package detection.
"""

import sys
import os
import importlib
import inspect


class IndLanImportError(Exception):
    """Raised when an imported package or symbol cannot be resolved."""
    def __init__(self, message, line=None):
        loc = f"[Line {line}] " if line is not None else ""
        super().__init__(f"{loc}{message}")
        self.line = line


# Map common packages to their recommended extras and category
PACKAGE_EXTRAS_MAP = {
    "pandas": ("Data Science", "indlan[data]"),
    "numpy": ("Data Science", "indlan[data]"),
    "matplotlib": ("Data Science", "indlan[data]"),
    "seaborn": ("Data Science", "indlan[data]"),
    "openpyxl": ("Data Science", "indlan[data]"),
    "xlsxwriter": ("Data Science", "indlan[data]"),
    "joblib": ("Data Science", "indlan[data]"),
    "scipy": ("Machine Learning", "indlan[ml]"),
    "sklearn": ("Machine Learning", "indlan[ml]"),
    "scikit-learn": ("Machine Learning", "indlan[ml]"),
    "statsmodels": ("Machine Learning", "indlan[ml]"),
    "tensorflow": ("AI", "indlan[ai]"),
    "keras": ("AI", "indlan[ai]"),
    "torch": ("AI", "indlan[ai]"),
    "torchvision": ("AI", "indlan[ai]"),
    "pillow": ("AI", "indlan[ai]"),
    "PIL": ("AI", "indlan[ai]"),
    "plotly": ("Visualization", "indlan[full]"),
    "cv2": ("Computer Vision", "indlan[full]"),
    "opencv-python": ("Computer Vision", "indlan[full]"),
    "nltk": ("NLP", "indlan[full]"),
    "spacy": ("NLP", "indlan[full]"),
    "transformers": ("AI", "indlan[full]"),
}

# Module name aliases (e.g. ganit -> math)
MODULE_ALIASES = {
    "ganit": "math",
}

# Comprehensive Hindi to English method, function, and property aliases
HINDI_METHOD_ALIASES = {
    # Universal Machine Learning & Data Processing
    "sikhao": "fit",
    "bhavishyavani": "predict",
    "badlo": "transform",
    "sikhao_aur_badlo": "fit_transform",
    "sikhao_aur_bhavishyavani": "fit_predict",
    "sankalit_karo": "compile",
    "mulyankan_karo": "evaluate",
    "prashikshan_karo": "train",
    "parikshan_karo": "test",
    "bachao": "save",
    "bharit_karo": "load",
    "padho": "read",
    "likho": "write",
    "jodo": "append",
    "hatao": "drop",
    "chhano": "filter",
    "kramit_karo": "sort",
    "samuha_banao": "groupby",
    "milao": "merge",
    "aakar_badlo": "reshape",

    # Pandas module & DataFrame / Series methods & properties
    "csv_padho": "read_csv",
    "dataframe": "DataFrame",
    "shrankhla": "Series",
    "excel_padho": "read_excel",
    "json_padho": "read_json",
    "csv_likho": "to_csv",
    "excel_likho": "to_excel",
    "json_likho": "to_json",
    "shuru_ke": "head",
    "ant_ke": "tail",
    "khali_bharo": "fillna",
    "maan_kramit_karo": "sort_values",
    "vivaran": "describe",

    # NumPy
    "sarni": "array",
    "shunya": "zeros",
    "ek": "ones",
    "kram": "arange",
    "samantar_kram": "linspace",
    "madhya": "mean",
    "madhyika": "median",
    "yog": "sum",
    "nyunatam": "min",
    "adhiktam": "max",
    "manak_vichalan": "std",

    # Matplotlib (plt)
    "rekha": "plot",
    "bindu": "scatter",
    "stambh": "bar",
    "kshaitij_stambh": "barh",
    "vitaran": "hist",
    "vritt": "pie",
    "dabba_lekha": "boxplot",
    "sheershak": "title",
    "x_namankit": "xlabel",
    "y_namankit": "ylabel",
    "sanket": "legend",
    "jaal": "grid",
    "likhai": "text",
    "tippani": "annotate",
    "chitra": "figure",
    "upchitra": "subplot",
    "upchitra_banao": "subplots",
    "x_seema": "xlim",
    "y_seema": "ylim",
    "dikhao": "show",
    "chitra_bachao": "savefig",
    "band_karo": "close",
    "chitra_saaf": "clf",
    "aksh_saaf": "cla",

    # Seaborn (sns)
    "rekha_chitra": "lineplot",
    "stambh_chitra": "barplot",
    "bindu_chitra": "scatterplot",
    "vitaran_chitra": "histplot",
    "tapman_naksha": "heatmap",
    "violin_chitra": "violinplot",

    # Math (math / ganit)
    "vargmool": "sqrt",
    "ghat": "pow",
    "nirapeksh": "fabs",
    "neeche_purnank": "floor",
    "upar_purnank": "ceil",
    "factorial": "factorial",
    "jya": "sin",
    "kojya": "cos",
    "sparshrekha": "tan",
    "ghatank": "exp",
    "pai": "pi",
    "aadhar": "e",

    # Scikit-learn metrics
    "satikta_ank": "accuracy_score",
    "madhya_varg_truti": "mean_squared_error",
    "vargikaran_vivaran": "classification_report",
    "bhram_matrix": "confusion_matrix",
    "precision_ank": "precision_score",
    "recall_ank": "recall_score",
    "f1_ank": "f1_score",
    "r2_ank": "r2_score",

    # PyTorch
    "mulyankan_sthiti": "eval",
    "pichhe_ganana": "backward",
    "kadam": "step",
    "grad_shunya": "zero_grad",

    # Pillow (PIL) & OpenCV (cv2)
    "chhavi_kholo": "open",
    "chhavi_padho": "imread",
    "chhavi_likho": "imwrite",
    "rang_badlo": "cvtColor",
}

# Fallback method resolution candidate chains
METHOD_FALLBACK_CANDIDATES = {
    "bachao": ["save", "dump", "to_csv", "savefig"],
    "bharit_karo": ["load", "load_model", "loads"],
    "padho": ["read", "read_csv", "load"],
    "likho": ["write", "to_csv", "dump"],
    "jodo": ["append", "join", "add"],
    "hatao": ["drop", "remove", "pop"],
    "kramit_karo": ["sort", "sort_values"],
    "nirapeksh": ["fabs", "abs"],
}


def format_missing_package_error(pkg_name, line=None):
    """Format a missing package error message with pip install instructions."""
    base_pkg = pkg_name.split(".")[0]
    category, extra = PACKAGE_EXTRAS_MAP.get(base_pkg, ("Full", "indlan[full]"))
    loc = f"[Line {line}] " if line is not None else ""
    return (
        f"{loc}[IndLan Import Error]\n\n"
        f"Package '{base_pkg}' is not installed.\n\n"
        f"Install it using:\n\n"
        f"pip install {base_pkg}\n\n"
        f"Or install IndLan {category} support:\n\n"
        f'pip install "{extra}"'
    )


def import_module_dynamic(module_path, line=None):
    """
    Dynamically imports a Python module or submodule.
    Translates module aliases (e.g. ganit -> math) if needed.
    """
    actual_path = MODULE_ALIASES.get(module_path, module_path)
    try:
        mod = importlib.import_module(actual_path)
        return mod
    except ModuleNotFoundError as e:
        missing_name = getattr(e, 'name', actual_path) or actual_path
        msg = format_missing_package_error(missing_name, line)
        raise IndLanImportError(msg, line) from e
    except Exception as e:
        loc = f"[Line {line}] " if line is not None else ""
        raise IndLanImportError(f"{loc}[IndLan Import Error] Failed to import '{actual_path}': {e}", line) from e


def resolve_from_import(module_path, item_name, line=None):
    """
    Resolves an imported symbol from a module (e.g. from sklearn.ensemble import RandomForestClassifier).
    Supports Hindi aliases for items (e.g. satikta_ank -> accuracy_score).
    """
    mod = import_module_dynamic(module_path, line)
    
    # Check if item_name is an alias
    target_names = [item_name]
    if item_name in HINDI_METHOD_ALIASES:
        target_names.append(HINDI_METHOD_ALIASES[item_name])
    if item_name in METHOD_FALLBACK_CANDIDATES:
        target_names.extend(METHOD_FALLBACK_CANDIDATES[item_name])

    for name in target_names:
        if hasattr(mod, name):
            return getattr(mod, name)

    # Check if it's a submodule (e.g. from tensorflow import keras)
    try:
        submod_path = f"{module_path}.{item_name}"
        return importlib.import_module(submod_path)
    except Exception:
        pass

    loc = f"[Line {line}] " if line is not None else ""
    raise IndLanImportError(
        f"{loc}[IndLan Import Error]\nCannot import '{item_name}' from module '{module_path}'.",
        line
    )


class PyBridgeCallable:
    """
    Wraps a Python callable (function, method, class constructor) so it can
    be called from IndLan with positional and keyword arguments.
    """
    def __init__(self, target, name=None):
        self.target = target
        self.name = name or getattr(target, "__name__", str(target))

    def __call__(self, *args, **kwargs):
        return self.target(*args, **kwargs)

    def __repr__(self):
        return f"<PyBridgeCallable {self.name}>"


def resolve_attribute(obj, name, line=None):
    """
    Resolves an attribute on any Python object/module/instance.
    Supports Hindi aliases, English names, and property vs method differentiation.
    Returns (found: bool, value: any).
    """
    # 1. Direct attribute match
    if hasattr(obj, name):
        return True, getattr(obj, name)

    # 2. Hindi alias check
    if name in HINDI_METHOD_ALIASES:
        english_name = HINDI_METHOD_ALIASES[name]
        if hasattr(obj, english_name):
            return True, getattr(obj, english_name)

    # 3. Fallback candidates check
    if name in METHOD_FALLBACK_CANDIDATES:
        for cand in METHOD_FALLBACK_CANDIDATES[name]:
            if hasattr(obj, cand):
                return True, getattr(obj, cand)

    # Special handling for standard string methods
    if isinstance(obj, str):
        str_map = {"upper": obj.upper, "lower": obj.lower, "strip": obj.strip, "split": obj.split}
        if name in str_map:
            return True, str_map[name]

    # Special handling for dict methods
    if isinstance(obj, dict):
        dict_map = {"keys": obj.keys, "values": obj.values, "items": obj.items, "get": obj.get}
        if name in dict_map:
            return True, dict_map[name]

    # Special handling for list methods
    if isinstance(obj, list):
        if name in ("append", "jodo"):
            return True, obj.append
        if name in ("pop", "hatao"):
            return True, obj.pop

    return False, None
