# Elencos legislativos de la provincia de Corrientes

La base de datos contiene 2.883 registros con información sobre las trayectorias políticas de al menos 1.548 personas. Los registros corresponden a candidaturas a diputado nacional, diputado y senador provincial y electores de gobernador y presidente en el período 1909-1955.

## Instalación

* Descargar el archivo [listado_general_1909-1955.sql](https://github.com/camilokawerin/personal-politico-corrientes/blob/master/listado_general_1909-1955.sql) (o clonar el repositorio para obtener futuras actualizaciones)
* Instalar un servidor web local [WampServer](https://www.wampserver.com/en/) (o una alternativa para Mac o Linux)
* Acceder a phpMyAdmin desde un navegador para crear una nueva base de datos e importar el archivo descargado
* Desde la misma interfaz se pueden realizar búsquedas 

## Estructura de la Base de Datos

El sistema está diseñado para trabajar con una base de datos MySQL llamada 'personal-politico-corrientes' que contiene la siguiente tabla principal:

### Tabla `listado`

```sql
CREATE TABLE IF NOT EXISTS `listado` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ID_Persona` int(11) DEFAULT NULL,
  `Control` int(11) DEFAULT NULL,
  `Nombre` varchar(255) DEFAULT NULL,
  `Apellido` varchar(255) DEFAULT NULL,
  `Partido` varchar(255) DEFAULT NULL,
  `Cargo` varchar(255) DEFAULT NULL,
  `Ambito` varchar(255) DEFAULT NULL,
  `Anno` int(11) DEFAULT NULL,
  `Seccion` varchar(255) DEFAULT NULL,
  `Electo` tinyint(1) DEFAULT '0',
  `Suplente` tinyint(1) DEFAULT '0',
  `Inicio_mandato` int(11) DEFAULT NULL,
  `Fin_mandato` int(11) DEFAULT NULL,
  `Sexo` char(1) DEFAULT NULL,
  `Profesion` varchar(255) DEFAULT NULL,
  `Otros_datos` varchar(255) DEFAULT NULL,
  `Nombre_alternativo` varchar(255) DEFAULT NULL,
  `Apellido_alternativo` varchar(255) DEFAULT NULL,
  `Probabilidad_error` varchar(255) DEFAULT NULL,
  `Observaciones` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

## Sistema de Generación de Informes

Este conjunto de scripts permite generar informes estadísticos sobre el personal político de Corrientes entre 1946 y 1955, con énfasis en las trayectorias políticas de los legisladores y candidatos peronistas.

### Estructura del Sistema

El sistema está organizado en módulos independientes pero interconectados:

#### Módulos Comunes (`scripts/commons/`)

- **db_utils.py**: Utilidades para conectar con la base de datos.
- **data_retrieval.py**: Funciones para recuperar datos específicos de la base de datos.
- **visualization.py**: Funciones para generar gráficos y visualizaciones.
- **html_utils.py**: Utilidades comunes para la generación de HTML.

#### Módulos de Informes (`scripts/modules/`)

Cada tipo de informe tiene su propio módulo:

1. **informe_trayectorias_completas.py**: Genera el informe con las trayectorias completas de los legisladores peronistas.
2. **informe_trayectorias_interpartidarias.py**: Genera el informe sobre legisladores con trayectorias en diferentes partidos políticos.
3. **informe_candidatos_peronistas.py**: Genera el informe sobre todos los candidatos peronistas entre 1946 y 1955.
4. **informe_candidatos_1946.py**: Genera el informe específico sobre los candidatos peronistas de 1946.

### Script Principal

- **generar_informes.py**: Script principal que integra todos los módulos y genera todos los informes.

### Cómo Usar

Para generar todos los informes de una vez:

```powershell
python generar_informes.py
```

Para generar un informe específico:

```powershell
# Para generar sólo el informe de trayectorias completas
python -c "from scripts.modules.informe_trayectorias_completas import generar_informe_trayectorias_completas; generar_informe_trayectorias_completas()"

# Para generar sólo el informe de trayectorias interpartidarias
python -c "from scripts.modules.informe_trayectorias_interpartidarias import generar_informe_trayectorias_interpartidarias; generar_informe_trayectorias_interpartidarias()"

# Para generar sólo el informe de todos los candidatos peronistas
python -c "from scripts.modules.informe_candidatos_peronistas import generar_informe_candidatos_peronistas; generar_informe_candidatos_peronistas()"

# Para generar sólo el informe de candidatos de 1946
python -c "from scripts.modules.informe_candidatos_1946 import generar_informe_candidatos_1946; generar_informe_candidatos_1946()"
```

### Requisitos

- Python 3.6 o superior
- Bibliotecas requeridas:
  - mysql-connector-python
  - pandas
  - matplotlib

### Output

Los informes se generan en HTML y se guardan en la carpeta `informes/`, junto con los gráficos generados en formato PNG. Se crea también un archivo `index.html` que sirve como punto de acceso a todos los informes generados.

### Notas

- La configuración de la conexión a la base de datos se encuentra en `commons/db_utils.py` y puede necesitar ajustes según la configuración local.
- Los gráficos generados usan colores y formatos predefinidos que pueden personalizarse en `commons/visualization.py`.

## Próximamente

Para facilitar la investigación, próximamente estará disponible el sistema [Prosopografia](https://github.com/camilokawerin/prosopografia) que permitirá realizar búsquedas, editar los atributos de cada persona y establecer relaciones políticas, de parentesco o derivadas de espacios de sociabilidad.

## Guía para desarrollo de scripts

Al extender o modificar los scripts de análisis de datos, es importante seguir estas reglas para mantener la consistencia y la precisión en los resultados:

### Conteo de personas únicas

- **Regla fundamental**: Al hacer cálculos estadísticos a partir de las candidaturas, siempre se deben contar personas únicas. Si una persona tiene más de una candidatura, se deben concatenar o reducir a uno solo los datos relevantes.
- **Implementación**: Usar `GROUP BY ID_Persona` en consultas SQL o agrupar por este campo en pandas.
- **Ejemplo**: Si una persona fue candidata varias veces por diferentes partidos, debe contarse una sola vez en el total, pero pueden concatenarse sus partidos en un campo separado para análisis de trayectoria.

### Trayectorias interpartidarias

- Identificar primero la fecha de la primera candidatura peronista de cada persona.
- Solo considerar como "experiencia previa" las candidaturas anteriores a esa fecha.
- Usar `MIN(Anno)` agrupando por `ID_Persona` al determinar el inicio de la trayectoria peronista.

### Visualizaciones

- Limitar los gráficos a mostrar las 10 categorías más frecuentes para mejor legibilidad.
- Incluir siempre títulos descriptivos y etiquetas en los ejes.
- Usar esquemas de color consistentes: azul para datos generales, verde para periodos temporales, rojo para cargos.

### Generación de HTML

- Asegurarse de usar codificación UTF-8 en todos los archivos HTML generados.
- Incluir metadatos de fecha y hora de generación en cada informe.
- Proporcionar navegación entre informes mediante enlaces a la página índice.
