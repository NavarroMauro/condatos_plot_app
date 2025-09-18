# app/debug_utils.py
"""
Funciones de depuración para uso durante el desarrollo.
Estas funciones no son parte de la funcionalidad principal
y sirven principalmente para diagnóstico.
"""

from pathlib import Path
import pandas as pd


def debug_flag_paths(df, flags_config, cat_col="", current_dir=None):
    """
    Muestra información detallada sobre las rutas de las banderas para diagnóstico.
    
    Params:
        df: DataFrame con los datos
        flags_config: Configuración de banderas del gráfico
        cat_col: Columna de categoría (países, etc.)
        current_dir: Directorio actual para rutas relativas
    """
    if not flags_config.get("enabled", False):
        print("⚠️ Las banderas están desactivadas en la configuración.")
        return
    
    print("\n🔍 DIAGNÓSTICO DE RUTAS DE BANDERAS")
    print("====================================")
    
    # Obtener configuración relevante
    flag_col = flags_config.get("column", "flag_url")
    pattern = flags_config.get("pattern", "")
    code_col = flags_config.get("code_column", "code")
    
    # Verificar columnas relevantes
    print(f"Columnas disponibles: {df.columns.tolist()}")
    
    if cat_col and cat_col in df.columns:
        print(f"✅ Columna de categorías '{cat_col}' encontrada")
    else:
        print(f"⚠️ Columna de categorías '{cat_col}' no encontrada")
    
    if flag_col in df.columns:
        print(f"✅ Columna de banderas '{flag_col}' encontrada")
        # Mostrar algunos valores de ejemplo
        print(f"   Ejemplos: {df[flag_col].head(3).tolist()}")
    else:
        print(f"⚠️ Columna de banderas '{flag_col}' no encontrada")
    
    if code_col in df.columns:
        print(f"✅ Columna de códigos '{code_col}' encontrada")
        # Mostrar algunos valores de ejemplo
        print(f"   Ejemplos: {df[code_col].head(3).tolist()}")
    else:
        print(f"⚠️ Columna de códigos '{code_col}' no encontrada")
    
    # Verificar patrón de banderas
    if pattern:
        print(f"✅ Patrón de banderas configurado: '{pattern}'")
    else:
        print("⚠️ Patrón de banderas no configurado")
    
    # Directorio actual
    if current_dir:
        print(f"📂 Directorio actual: {current_dir}")
    
    # Verificar existencia de archivos para los primeros 5 países
    print("\nVerificando rutas de banderas para los primeros 5 elementos:")
    
    for i in range(min(5, len(df))):
        cat_name = df.iloc[i].get(cat_col, f"Elemento {i}") if cat_col in df.columns else f"Elemento {i}"
        print(f"\n- {cat_name}:")
        
        # 1. Verificar flag_url directa
        if flag_col in df.columns:
            flag_path = df.iloc[i].get(flag_col)
            if flag_path:
                if flag_path.startswith('/'):
                    abs_path = str(current_dir / flag_path.lstrip('/')) if current_dir else flag_path
                    exists = Path(abs_path).exists()
                    print(f"  • Ruta directa: {flag_path}")
                    print(f"  • Ruta absoluta: {abs_path}")
                    print(f"  • Existe: {'✅' if exists else '❌'}")
                else:
                    exists = Path(flag_path).exists()
                    print(f"  • Ruta directa: {flag_path}")
                    print(f"  • Existe: {'✅' if exists else '❌'}")
            else:
                print(f"  • No hay ruta directa en columna {flag_col}")
        
        # 2. Verificar construcción por patrón
        if pattern and code_col in df.columns:
            code = str(df.iloc[i].get(code_col, "")).strip()
            if code:
                try:
                    constructed_path = pattern.format(code=code.lower(), CODE=code.upper())
                    exists = Path(constructed_path).exists()
                    print(f"  • Código: {code}")
                    print(f"  • Ruta construida: {constructed_path}")
                    print(f"  • Existe: {'✅' if exists else '❌'}")
                except Exception as e:
                    print(f"  • Error al construir ruta con patrón: {e}")
            else:
                print(f"  • No hay código en columna {code_col}")
    
    # Sugerencias si hay problemas
    print("\n💡 SUGERENCIAS:")
    print("1. Asegúrate que las rutas de las banderas sean correctas y los archivos existan.")
    print("2. Si usas rutas absolutas, verifica que comiencen desde la raíz del proyecto.")
    print("3. Si usas un patrón, verifica que los códigos de país sean correctos.")
    print("4. El patrón debe tener los marcadores {code} o {CODE} para sustitución.")
    print("   Ejemplo: 'assets/flags/{code}.png'")