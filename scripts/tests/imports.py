"""
Script de prueba para verificar que los módulos se importan correctamente.
"""
import os
import sys
# Add the parent directory to sys.path to enable imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def test_imports():
    """Prueba la importación de todos los módulos"""
    try:
        # Commons modules
        from scripts.commons import db_utils
        print("✓ db_utils importado correctamente")
        
        from scripts.commons import data_retrieval
        print("✓ data_retrieval importado correctamente")
        
        from scripts.commons import visualization
        print("✓ visualization importado correctamente")
        
        from scripts.commons import html_utils
        print("✓ html_utils importado correctamente")
        
        # Report modules
        from scripts.modules import informe_trayectorias_interpartidarias
        print("✓ informe_trayectorias_interpartidarias importado correctamente")
        
        from scripts.modules import informe_trayectorias_completas
        print("✓ informe_trayectorias_completas importado correctamente")
        
        from scripts.modules import informe_candidatos_1946
        print("✓ informe_candidatos_1946 importado correctamente")
        
        from scripts.modules import informe_candidatos_peronistas
        print("✓ informe_candidatos_peronistas importado correctamente")
        
        from scripts import generar_informes
        print("✓ generar_informes importado correctamente")
        
        print("\nTodas las importaciones funcionaron correctamente.")
        return True
        
    except ImportError as e:
        print(f"✗ Error al importar módulo: {e}")
        import traceback
        traceback.print_exc()
        return False
        
if __name__ == "__main__":
    test_imports()
