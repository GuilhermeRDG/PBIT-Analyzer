from flask import Flask, render_template, request, redirect, flash
import os
from werkzeug.utils import secure_filename
import zipfile
import json

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
uploads_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
app = Flask(__name__, template_folder=template_dir)
app.secret_key = "1234"
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pbit"}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def read_text_safe(path):
    if not os.path.isfile(path):
        return None
    for enc in ["utf-8", "utf-16", "utf-16-le", "utf-16-be"]:
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, ValueError):
            continue
    return None

def safe_load_json(text):
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return "Arquivo binário ou JSON inválido"

def extract_pbit(pbit_path, extract_folder="pbit_extracted"):
    with zipfile.ZipFile(pbit_path, 'r') as z:
        z.extractall(extract_folder)
    return extract_folder

def parse_data_model_schema(extract_folder):
    print(extract_folder)
    path = os.path.join(extract_folder, "DataModelSchema")
    if not os.path.exists(path):
        return [], [], [], {}

    text = read_text_safe(path)
    if not text:
        return [], [], [], {}

    schema = safe_load_json(text)
    if isinstance(schema, str):
        return [], [], [], {}

    columns_info = []
    measures_info = []
    tables_info = []
    table_sources = {}  

    for table in schema.get("model", {}).get("tables", []):
        table_name = table.get("name")
        if "LocalDateTable_" in table_name or "DateTableTemplate_" in table_name:
            continue
            
        tables_info.append(table_name)


        m_expression = None
        partitions = table.get("partitions", [])
        for partition in partitions:
            if partition.get("name") == table_name:
                source = partition.get("source", {})
                if source.get("type") == "m":
                    expression_lines = source.get("expression", [])
                    if isinstance(expression_lines, list) and len(expression_lines) > 1:

                        for i, line in enumerate(expression_lines):
                            if line.strip() == "let":
                                if i + 1 < len(expression_lines):
                                    m_expression = expression_lines[i + 1].strip()
                                    break
                elif source.get("type") == "calculated":
                    expression_lines = source.get("expression", [])
                    if isinstance(expression_lines, list) and expression_lines:
                        m_expression = " ".join(expression_lines[:3]) + "..." 
        
    
        table_sources[table_name] = m_expression

        for col in table.get("columns", []):
            columns_info.append({
                "table": table_name,
                "name": col.get("name"),
                "type": col.get("type"),
                "dataType": col.get("dataType"),
                "expression": col.get("expression"),
                "columnType": col.get("type")
            })
            
        for measure in table.get("measures", []):
            expr = measure.get("expression")
            if isinstance(expr, list):
                expr = "\n".join(expr)
            measures_info.append({
                "table": table_name,
                "name": measure.get("name"),
                "expression": str(expr) if expr else ""
            })
            
    return columns_info, measures_info, tables_info, table_sources

def parse_security_bindings(extract_folder):
    path = os.path.join(extract_folder, "DataModelSchema")
    if not os.path.exists(path):
        return []

    text = read_text_safe(path)
    if not text:
        return []

    roles = safe_load_json(text)
    if isinstance(roles, str):
        return []

    roles_info = []
    for role in roles.get("model", {}).get("roles", []):
        roles_info.append({
            "name": role.get("name"),
            "permissions": role.get("tablePermissions", [])
        })
    return roles_info

def parse_report(extract_folder):
    path = os.path.join(extract_folder, r"Report\Layout")
    if not os.path.exists(path):
        return []

    text = read_text_safe(path)
    if not text:
        return []

    report = safe_load_json(text)
    if isinstance(report, str):
        return []

    pages_info = []
    for page in report.get("sections", []):
        pages_info.append({"name": page.get("displayName")})
    return pages_info

def process_pbit(file_path):
    extract_folder = extract_pbit(file_path, extract_folder=os.path.join(UPLOAD_FOLDER, "extracted"))
    columns, measures, tables, table_sources = parse_data_model_schema(extract_folder)
    roles = parse_security_bindings(extract_folder)
    pages = parse_report(extract_folder)
    
    column_types = {
        "calculate": 0,
        "calculatedTableColumn": 0,
        "none": 0
    }
    
    calculated_tables = set()
    standard_tables = set()
    
    for col in columns:
        col_type = col.get("type")
        table_name = col.get("table")
        
        if col_type == "calculated":
            column_types["calculate"] += 1
        elif col_type == "calculatedTableColumn":
            column_types["calculatedTableColumn"] += 1
            calculated_tables.add(table_name)  
        else:
            column_types["none"] += 1
            standard_tables.add(table_name) 
    
    for table in tables:
        if table not in calculated_tables and table not in standard_tables:
            standard_tables.add(table)
    
    return {
        "columns": columns,
        "measures": measures,
        "roles": roles,
        "pages": pages,
        "tables": tables,
        "table_sources": table_sources,
        "column_types": column_types,
        "calculated_tables_count": len(calculated_tables),  
        "standard_tables_count": len(standard_tables)      
    }


@app.route("/", methods=["GET", "POST"])
def index():
    data = None
    if request.method == "POST":
        if 'pbit_file' not in request.files:
            flash("Nenhum arquivo selecionado!")
            return redirect(request.url)
        file = request.files['pbit_file']
        if file.filename == "":
            flash("Nenhum arquivo selecionado!")
            return redirect(request.url)
        if file and file.filename.split('.')[-1] in ALLOWED_EXTENSIONS:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            data = process_pbit(file_path)
    return render_template("report_view.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)