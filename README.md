<div align="center">

<img src="indlan_logo.png" alt="IndLan Logo" width="180"/>

# IndLan (v2.1.4)
### A Modern Hindi + English Programming Interface for the Python Ecosystem with VSCode Edition IDE

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Version 2.1.4](https://img.shields.io/badge/version-2.1.4-green.svg)](https://pypi.org/project/indlan/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()

**IndLan** allows you to use real Python libraries (**Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, TensorFlow, PyTorch, Plotly, Joblib, Openpyxl, OpenCV, SQLite3, NLTK**) directly using intuitive **Hindi and English** syntax.

🎯 **NEW v2.1.4**: VSCode Edition IDE with File Explorer, Find/Replace, Enhanced Templates, and Python API Integration

Made by **Bhavya S Solanki**

</div>

---

## 🚀 Key Highlights

- **🖥️ VSCode Edition IDE**: Professional dark-mode IDE with file explorer sidebar, find/replace, font controls, tab navigation, and integrated terminal
- **🌐 Bilingual Interface**: Write code using either Hindi keywords or standard English syntax interchangeably
- **🔗 Real Python Objects**: Objects remain genuine `pandas.DataFrame`, `numpy.ndarray`, `torch.Tensor`, `sklearn` models
- **🎯 Universal & Library-Specific Aliases**:
  - `model.sikhao(X, y)` ➔ `model.fit(X, y)`
  - `model.bhavishyavani(X)` ➔ `model.predict(X)`
  - `np.sarni([1, 2, 3])` ➔ `np.array([1, 2, 3])`
  - `pd.csv_padho("file.csv")` ➔ `pd.read_csv("file.csv")`
  - `plt.rekha(x, y)` ➔ `plt.plot(x, y)`
  - `ganit.vargmool(16)` ➔ `math.sqrt(16)`
- **📝 F-String Interpolation**: Modern string formatting with embedded expressions
- **🔢 Enhanced Built-in Functions**: Math functions, string/list methods, utility functions
- **⚡ Full Keyword Argument Support**: `train_test_split(X, y, test_size=0.25, random_state=42)`
- **📦 Multi-Variable Unpacking**: `maano X_train, X_test, y_train, y_test = train_test_split(...)`
- **🐍 Python API Integration**: `import indlan as ind; ind.run(source_code)`
- **💻 Standalone `.EXE` Executables**: Pre-compiled binaries (`IndLan_IDE.exe` and `IndLan.exe`) for Windows
- **🔧 Enhanced Build Process**: Automatic cleaning, better error handling, improved .exe creation

---

## 🖥️ VSCode Edition IDE (NEW v2.1.4)

IndLan 2.1.4 features a professional VSCode-like Desktop GUI IDE:

```bash
indlan ide        # or simply: indlan
```

### 🎨 IDE Features:
- **📁 File Explorer Sidebar**: Browse directories, navigate folders, double-click to open files
- **🔍 Find & Replace**: Ctrl+F for find, Ctrl+H for find and replace functionality
- **🔤 Font Size Control**: Ctrl++ to increase, Ctrl+- to decrease, Ctrl+0 to reset font size
- **📑 Tab Navigation**: Ctrl+Tab for next tab, Ctrl+Shift+Tab for previous, Ctrl+W to close tab
- **🎨 Real-Time Bilingual Syntax Highlighting**: Color-coded syntax for Hindi keywords, English keywords, ML method aliases, strings, numbers, and comments
- **📏 Synchronized Line Numbers Gutter**: Tracks cursor and scrolling
- **📑 Multi-Tab File Management**: Open, edit, and save multiple `.ind` files
- **💻 Integrated Terminal Console**: View program output and errors with color tags
- **▶️ One-Click Run (F5)** & Output Clearing
- **📝 Preloaded Code Templates**: Instant snippets for Data Science, Machine Learning, F-strings, Math functions, Python API, and more
- **⌨️ Keyboard Shortcuts**: Comprehensive shortcut system for efficient coding

### 🎯 New Templates in v2.1.4:
- F-Strings & String Methods
- Math & Built-in Functions  
- Python API Integration
- Advanced Features (negative indexing, string repetition, compound assignment)

---

## 🆕 What's New in v2.1.4

### 🖥️ VSCode Edition IDE (Major Feature!)
- **File Explorer Sidebar**: Browse directories, navigate folders, double-click to open files
- **Find & Replace**: Ctrl+F for find, Ctrl+H for find and replace functionality  
- **Font Size Control**: Ctrl++ to increase, Ctrl+- to decrease, Ctrl+0 to reset font size
- **Tab Navigation**: Ctrl+Tab for next tab, Ctrl+Shift+Tab for previous, Ctrl+W to close tab
- **Enhanced Toolbar**: Better icons, improved layout, professional VSCode-like interface
- **New Code Templates**: F-strings, Math functions, Python API integration, and advanced features
- **Keyboard Shortcuts**: Comprehensive shortcut system for efficient coding

### 🌟 F-String Interpolation
```indlan
maano naam = "Bhavya"
maano umar = 17
chhap(f"Namaste {naam}!")
chhap(f"Agli baar aap {umar + 1} ke honge.")
chhap(f"2 ka 10 ghaat = {2 ** 10}")
```

### 🔤 String Methods
```indlan
maano text = "  Hello World  "
chhap("Upper: " + text.upper())
chhap("Lower: " + text.lower())
chhap("Strip: " + text.strip())
chhap("Replace: " + text.replace("World", "IndLan"))
chhap("Split: " + str(text.strip().split(" ")))
```

### 📋 List Methods
```indlan
maano numbers = [3, 1, 4, 1, 5]
numbers.sort()
chhap("Sorted: " + str(numbers))
numbers.reverse()
chhap("Reversed: " + str(numbers))
chhap("Contains 5: " + str(numbers.contains(5)))
chhap("Length: " + str(numbers.len()))
```

### 🔢 Math Built-in Functions
```indlan
chhap("abs(-5): " + str(abs(-5)))
chhap("sqrt(16): " + str(sqrt(16)))
chhap("max(10, 20, 5): " + str(max(10, 20, 5)))
chhap("min(10, 20, 5): " + str(min(10, 20, 5)))
chhap("floor(3.7): " + str(floor(3.7)))
chhap("ceil(3.2): " + str(ceil(3.2)))
chhap("round(3.7): " + str(round(3.7)))
```

### 🛠️ Additional Built-in Functions
- `char(v)` - int↔char conversion (ord/chr)
- `has(col, v)` - membership check for collections
- `insert(lst, i, v)` - insert value at index
- `remove(lst, v)` - remove first occurrence

### ⚡ Enhanced Operators
- String repetition: `"ha" * 3` → `"hahaha"`
- Negative indexing: `arr[-1]` (from end of list/string)
- Compound assignment: `**=` for exponentiation

### 🐍 Python API Integration
```python
import indlan as ind

code = '''
maano naam = "Bhavya"
chhap(f"Namaste {naam}!")
'''
ind.run(code)
```

---

##  Installation & Extras

### Core Engine
```bash
pip install indlan
```

### Data Science Extras (Pandas, NumPy, Matplotlib, Seaborn, Openpyxl, Joblib)
```bash
pip install "indlan[data]"
```

### Machine Learning Extras (Scikit-learn, SciPy, Statsmodels)
```bash
pip install "indlan[ml]"
```

### AI & Deep Learning Extras (TensorFlow, PyTorch, Torchvision, Pillow)
```bash
pip install "indlan[ai]"
```

### Full Ecosystem Extras
```bash
pip install "indlan[full]"
```

---

## ⚡ CLI Commands

```bash
indlan                             # Launch VSCode Edition IDE
indlan ide                         # Launch VSCode Edition IDE
indlan repl                        # Start Interactive REPL
indlan program.ind                 # Run an IndLan script
indlan run program.ind             # Run an IndLan script
indlan --debug program.ind         # Run with detailed Python tracebacks
indlan --version                   # Show version (2.1.4)
indlan --help                      # Show help menu
```

---

## 📖 Complete Data Science Example

### 🇮🇳 Hindi Syntax (`program_hindi.ind`)

```indlan
aayat pandas ke_roop_mein pd
aayat numpy ke_roop_mein np
aayat matplotlib.pyplot ke_roop_mein plt

se sklearn.model_selection aayat train_test_split
se sklearn.ensemble aayat RandomForestClassifier
se sklearn.metrics aayat satikta_ank

chhap("=== IndLan Hindi Data Science Pipeline ===")

maano data = pd.csv_padho("students.csv")
chhap("Pehle 5 Rows:\n", data.shuru_ke(5))
chhap("Aakar (Shape):", data.shape)

maano X = np.sarni([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9]])
maano y = np.sarni([0, 0, 0, 0, 1, 1, 1, 1])

maano X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42
)

maano model = RandomForestClassifier(random_state=42)
model.sikhao(X_train, y_train)

maano prediction = model.bhavishyavani(X_test)
chhap("Predictions:", prediction)
chhap("Accuracy Score:", satikta_ank(y_test, prediction))

plt.figure()
plt.rekha(prediction)
plt.sheershak("Prediction Chart")
plt.jaal(true)
plt.dikhao()
```

### 🇬🇧 English Syntax (`program_english.ind`)

```indlan
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

print("=== IndLan English Data Science Pipeline ===")

data = pd.read_csv("students.csv")
print("First 5 Rows:\n", data.head(5))
print("Shape:", data.shape)

X = np.array([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9]])
y = np.array([0, 0, 0, 0, 1, 1, 1, 1])

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42
)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

prediction = model.predict(X_test)
print("Predictions:", prediction)
print("Accuracy Score:", accuracy_score(y_test, prediction))

plt.figure()
plt.plot(prediction)
plt.title("Prediction Chart")
plt.grid(true)
plt.show()
```

---

## 📚 Keyword & Alias Reference

### Keywords
| English | Hindi Alias | Purpose |
|---|---|---|
| `import` | `aayat` | Import Python module |
| `from` | `se` | Import from package |
| `as` | `ke_roop_mein` | Create alias |
| `let` | `maano` | Variable assignment |
| `fun` | `kaam` | Define function |
| `return` | `vapas` | Return value |
| `if` | `agar` | If condition |
| `elif` | `nahito_agar` | Else if condition |
| `else` | `nahito` | Else branch |
| `while` | `jabtak` | While loop |
| `do` | `karo` | Do-while loop |
| `for` | `pratyek` | For-each loop |
| `in` | `mein` | In operator |
| `switch` | `vibhag` | Switch statement |
| `case` | `sthiti` | Switch case |
| `default` | `anyatha` | Default case |
| `class` | `varg` | Define class |
| `new` | `naya` | Instantiate class |
| `this` | `yeh` | Self instance |
| `true` | `sahi` | True boolean |
| `false` | `galat` | False boolean |
| `null` | `khaali` | Null / None |
| `and` | `aur` | Logical AND |
| `or` | `ya` | Logical OR |
| `not` | `nahi` | Logical NOT |
| `break` | `roko` | Break loop |
| `continue` | `jaari` | Continue loop |
| `print` | `chhap` | Print to stdout |

### Universal Method Aliases
| English Method | Hindi Method Alias |
|---|---|
| `fit` | `sikhao` |
| `predict` | `bhavishyavani` |
| `transform` | `badlo` |
| `fit_transform` | `sikhao_aur_badlo` |
| `compile` | `sankalit_karo` |
| `evaluate` | `mulyankan_karo` |
| `train` | `prashikshan_karo` |
| `test` | `parikshan_karo` |
| `save` / `dump` | `bachao` |
| `load` | `bharit_karo` |
| `read` | `padho` |
| `write` | `likho` |
| `append` | `jodo` |
| `drop` / `remove` | `hatao` |
| `filter` | `chhano` |
| `sort` | `kramit_karo` |
| `groupby` | `samuha_banao` |
| `merge` | `milao` |
| `reshape` | `aakar_badlo` |

### Pandas Aliases
| English | Hindi Alias |
|---|---|
| `pd.read_csv()` | `pd.csv_padho()` |
| `pd.DataFrame()` | `pd.dataframe()` |
| `pd.Series()` | `pd.shrankhla()` |
| `pd.read_excel()` | `pd.excel_padho()` |
| `pd.read_json()` | `pd.json_padho()` |
| `df.head()` | `df.shuru_ke()` |
| `df.tail()` | `df.ant_ke()` |
| `df.fillna()` | `df.khali_bharo()` |
| `df.sort_values()` | `df.maan_kramit_karo()` |
| `df.describe()` | `df.vivaran()` |

### NumPy Aliases
| English | Hindi Alias |
|---|---|
| `np.array()` | `np.sarni()` |
| `np.zeros()` | `np.shunya()` |
| `np.ones()` | `np.ek()` |
| `np.arange()` | `np.kram()` |
| `np.linspace()` | `np.samantar_kram()` |
| `np.mean()` | `np.madhya()` |
| `np.median()` | `np.madhyika()` |
| `np.sum()` | `np.yog()` |
| `np.min()` | `np.nyunatam()` |
| `np.max()` | `np.adhiktam()` |
| `np.std()` | `np.manak_vichalan()` |

### Matplotlib & Seaborn Aliases
| English | Hindi Alias |
|---|---|
| `plt.plot()` | `plt.rekha()` |
| `plt.scatter()` | `plt.bindu()` |
| `plt.bar()` | `plt.stambh()` |
| `plt.hist()` | `plt.vitaran()` |
| `plt.pie()` | `plt.vritt()` |
| `plt.title()` | `plt.sheershak()` |
| `plt.xlabel()` | `plt.x_namankit()` |
| `plt.ylabel()` | `plt.y_namankit()` |
| `plt.grid()` | `plt.jaal()` |
| `plt.show()` | `plt.dikhao()` |
| `plt.savefig()` | `plt.chitra_bachao()` |
| `plt.close()` | `plt.band_karo()` |
| `sns.lineplot()` | `sns.rekha_chitra()` |
| `sns.heatmap()` | `sns.tapman_naksha()` |

### Math / Ganit Aliases
| English | Hindi Alias |
|---|---|
| `math.sqrt()` | `ganit.vargmool()` |
| `math.pow()` | `ganit.ghat()` |
| `math.fabs()` | `ganit.nirapeksh()` |
| `math.floor()` | `ganit.neeche_purnank()` |
| `math.ceil()` | `ganit.upar_purnank()` |
| `math.sin()` | `ganit.jya()` |
| `math.cos()` | `ganit.kojya()` |
| `math.tan()` | `ganit.sparshrekha()` |
| `math.exp()` | `ganit.ghatank()` |
| `math.pi` | `ganit.pai` |
| `math.e` | `ganit.aadhar` |

---

## 🛠️ Native File Helpers

IndLan provides out-of-the-box native functions for quick file operations:
- `csv_padho(filepath)`: Reads CSV files into a list of records.
- `csv_likho(filepath, data)`: Writes lists/dicts or DataFrames to CSV.
- `csv_jodo(filepath, row)`: Appends a row to a CSV file.
- `csv_badlo(filepath, callback)`: Transforms CSV rows using a function.
- `csv_chhano(filepath, predicate)`: Filters CSV rows using a condition.
- `json_padho(filepath)`: Reads JSON into native data structures.
- `json_likho(filepath, data)`: Writes data structures to formatted JSON.
- `excel_padho(filepath)`: Reads Excel files (`.xlsx`, `.xlsm`).
- `excel_likho(filepath, data)`: Writes data to Excel files.

---

## 🔢 New Built-in Functions (v2.1.4)

### Math Functions
- `abs(n)`: Absolute value
- `sqrt(n)`: Square root
- `max(a, b, ...)` or `max(lst)`: Maximum value
- `min(a, b, ...)` or `min(lst)`: Minimum value
- `floor(n)`: Round down to nearest integer
- `ceil(n)`: Round up to nearest integer
- `round(n, digits?)`: Round to specified decimal places

### Utility Functions
- `char(v)`: int→char or char→int conversion (ord/chr)
- `has(col, v)`: Check if value exists in collection (list, string, dict)
- `insert(lst, i, v)`: Insert value at index in list
- `remove(lst, v)`: Remove first occurrence of value from list

### String & List Methods
- String: `.upper()`, `.lower()`, `.strip()`, `.lstrip()`, `.rstrip()`, `.replace(old, new)`, `.split(sep?)`, `.startswith(x)`, `.endswith(x)`, `.find(x)`
- List: `.append(v)`, `.pop(i?)`, `.sort()`, `.reverse()`, `.contains(v)`, `.len()`

### Enhanced Operators
- String repetition: `"ha" * 3` → `"hahaha"`
- Negative indexing: `arr[-1]` (access from end)
- Exponentiation: `2 ** 10` → `1024`
- Compound assignment: `**=` for exponentiation

---

## ⌨️ User-Input Functions

IndLan provides intuitive bilingual functions to read user input from the console, terminal, or IDE:

| English Function | IndLan Function | Return Type | Description |
|---|---|---|---|
| `input(prompt?)` | `aalao(prompt?)` | `string` | Reads raw user input as a string |
| `input_int(prompt?)` | `number_dalao(prompt?)` | `integer` | Reads input and converts it to integer |
| `input_float(prompt?)` | `decimal_dalao(prompt?)` | `float` | Reads input and converts it to float |
| `input_bool(prompt?)` | `haan_na(prompt?)` | `bool` (`true` / `false`) | Reads input and converts to boolean (`sahi` / `galat`) |

### Example

```indlan
maano naam = aalao("Apna naam: ")
maano umar = number_dalao("Umar: ")
maano height = decimal_dalao("Height: ")
maano pass = haan_na("Continue? (true/false): ")

chhap("Namaste", naam, "| Umar:", umar, "| Height:", height, "| Pass:", pass)
```

---

## 🚢 Publishing to PyPI

To publish a new version of IndLan to PyPI:

1. **Build Distribution Packages**:
   ```bash
   python -m build
   ```
2. **Validate Packages with Twine**:
   ```bash
   python -m twine check dist/*
   ```
3. **Upload to PyPI**:
   ```bash
   python -m twine upload dist/indlan-2.1.4*
   ```
   *(Enter `__token__` for username and your PyPI API token for password).*

---

## 🔨 Building Standalone .EXE Binaries

To build standalone Windows executables (`IndLan.exe` and `IndLan_IDE.exe`):

```bash
python build_exe.py
```
The enhanced build script automatically cleans previous builds and creates optimized VSCode Edition IDE binaries with custom icons in the `dist/` directory.

---

## 📄 License

This project is licensed under the **MIT License**.

Made with ❤️ by **Bhavya S Solanki**.
