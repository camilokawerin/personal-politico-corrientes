"""
Generador de visualizaciones interactivas de trayectorias políticas.
Este módulo se encarga de generar las visualizaciones interactivas de trayectorias
políticas para su exploración en formato HTML.
"""
import os
import sys
import json
import shutil
from collections import defaultdict
from datetime import datetime

# Add the project root to sys.path
module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
project_root = os.path.dirname(module_path)
sys.path.insert(0, project_root)

from scripts.commons.db_utils import ejecutar_consulta
from scripts.commons.data_retrieval import (
    obtener_detalle_trayectoria_candidatos_peronistas
)
from scripts.commons.html_utils import generar_encabezado_html, generar_pie_html

def generar_datos_trayectorias_json(detalle_trayectorias):
    """
    Genera un archivo JSON con los datos de las trayectorias para visualización interactiva.
    
    Args:
        detalle_trayectorias: Lista de diccionarios con información detallada de trayectorias
        
    Returns:
        str: Ruta al archivo JSON generado
    """
    if not detalle_trayectorias:
        print("No hay datos de trayectorias para generar JSON")
        return None
        
    try:
        # Estructurar datos para la visualización
        candidatos = []
        
        # Identificar grupos partidarios principales
        grupos_partidarios = {
            'Radical Antipersonalista': {'color': '#FFA500'},  # Naranja
            'Radical Personalista': {'color': '#4CAF50'},      # Verde
            'Liberal': {'color': '#2196F3'},                   # Azul
            'Autonomista': {'color': '#F44336'},               # Rojo
            'Otro': {'color': '#9E9E9E'}                       # Gris
        }
        
        # Determinar el nivel correspondiente a cada cargo
        niveles = [
            {"nivel": 1, "nombre": "Elector Provincial"},
            {"nivel": 2, "nombre": "Diputado Provincial"},
            {"nivel": 3, "nombre": "Senador Provincial"},
            {"nivel": 4, "nombre": "Diputado Nacional"}
        ]
        
        # Mapeo de cargos a niveles
        mapeo_cargos = {
            "Elector Provincial": 1,
            "Diputado Provincial": 2,
            "Senador Provincial": 3,
            "Diputado Nacional": 4,
            "Otro Cargo": 0.5
        }
        
        # Determinar el grupo partidario para cada candidato
        for candidato in detalle_trayectorias:
            # Solo incluir candidatos con trayectoria previa
            if candidato['Cantidad_Candidaturas_Previas'] == 0:
                continue
                
            # Identificar el grupo partidario principal según el Partido_Principal
            partido_principal = candidato.get('Partido_Principal', '')
            grupo = 'Otro'
            
            if 'Radical Antipersonalista' in partido_principal:
                grupo = 'Radical Antipersonalista'
            elif 'Radical Personalista' in partido_principal or 'Radical' == partido_principal:
                grupo = 'Radical Personalista'
            elif 'Liberal' in partido_principal:
                grupo = 'Liberal'
            elif 'Autonomista' in partido_principal or 'Demócrata Nacional (Autonomista)' in partido_principal:
                grupo = 'Autonomista'
            
            # Estructurar datos del candidato
            candidato_data = {
                "id": candidato['ID_Persona'],
                "nombre": candidato['Nombre_Completo'],
                "grupo": grupo,
                "electoEnPeronismo": candidato['Electo_Peronista'] == 1,
                "puntos": []
            }
            
            # Obtener todos los puntos (candidaturas previas y la primera peronista)
            # Agregar la candidatura peronista
            candidato_data["puntos"].append({
                "anio": candidato['Anno_Peronista'],
                "nivel": obtener_nivel_cargo(candidato['Cargo_Peronista'], candidato['Ambito_Peronista']),
                "cargo": f"{candidato['Cargo_Peronista']} {candidato['Ambito_Peronista']}",
                "electo": candidato['Electo_Peronista'] == 1,
                "partido": candidato['Partido_Peronista'],
                "es_peronista": True
            })
            
            # Extraer puntos previos de los campos de cargos previos
            if 'Cargos_Previos' in candidato and candidato['Cargos_Previos']:
                partidos_previos = candidato['Partidos_Previos'].split(', ') if candidato['Partidos_Previos'] else []
                
                # Si hay información estructurada sobre candidaturas previas, usarla
                if hasattr(candidato, 'candidaturas_previas') and candidato.candidaturas_previas:
                    for candidatura in candidato.candidaturas_previas:
                        punto = {
                            "anio": candidatura['anno'],
                            "nivel": obtener_nivel_cargo(candidatura['cargo'], candidatura['ambito']),
                            "cargo": f"{candidatura['cargo']} {candidatura['ambito']}",
                            "electo": candidatura['electo'] == 1,
                            "partido": candidatura['partido'],
                            "es_peronista": False
                        }
                        candidato_data["puntos"].append(punto)
                else:
                    # Intentar extraer la información de candidaturas previas desde los strings
                    # Esto es una aproximación y podría no ser 100% precisa
                    # Primero, separar cada cargo previo
                    cargos_previos_texto = candidato['Cargos_Previos'].split(', ')
                    for i, cargo_texto in enumerate(cargos_previos_texto):
                        # Determinar si el cargo fue electo (marcado con (*))
                        electo = False
                        if '(*)' in cargo_texto:
                            electo = True
                            cargo_texto = cargo_texto.replace('(*)', '').strip()
                        
                        # Determinar el cargo y ámbito
                        partes = cargo_texto.split(' ')
                        if len(partes) >= 2:
                            cargo = partes[0]
                            ambito = ' '.join(partes[1:])
                        else:
                            cargo = cargo_texto
                            ambito = "No especificado"
                        
                        # Determinar el partido (usar el primero disponible si hay varios)
                        partido = partidos_previos[0] if partidos_previos else "Desconocido"
                        
                        # Calcular un año aproximado para esta candidatura
                        # Use espaciado regular entre primera candidatura y candidatura peronista
                        anno_primera = candidato['Anno_Primera_Candidatura']
                        anno_peronista = candidato['Anno_Peronista']
                        span = anno_peronista - anno_primera
                        total_cargos = len(cargos_previos_texto)
                        
                        if total_cargos > 1:
                            # Espaciar regularmente las candidaturas
                            anno_estimado = anno_primera + (span * (i / (total_cargos)))
                            anno_estimado = int(anno_estimado)
                        else:
                            anno_estimado = anno_primera
                        
                        punto = {
                            "anio": anno_estimado,
                            "nivel": obtener_nivel_cargo(cargo, ambito),
                            "cargo": f"{cargo} {ambito}",
                            "electo": electo,
                            "partido": partido,
                            "es_peronista": False
                        }
                        candidato_data["puntos"].append(punto)
            
            # Ordenar los puntos por año
            candidato_data["puntos"].sort(key=lambda p: p["anio"])
            
            # Agregar el candidato a la lista
            candidatos.append(candidato_data)
          # Estructura final del JSON
        datos_json = {
            "candidatos": candidatos,
            "niveles": niveles,
            "grupos": [{"nombre": nombre, "color": info["color"]} for nombre, info in grupos_partidarios.items()]
        }
        
        print(f"   ✓ Datos JSON para visualización interactiva generados correctamente")
        return datos_json
        
    except Exception as e:
        print(f"   ✗ Error al generar JSON: {e}")
        return None
        
def obtener_nivel_cargo(cargo, ambito):
    """
    Determina el nivel de visualización para un cargo
    
    Args:
        cargo: Nombre del cargo
        ambito: Ámbito del cargo (Nacional, Provincial, etc.)
        
    Returns:
        int: Nivel para la visualización (1-4, o 0.5 para otros)
    """
    # Ajustar el cargo si viene con ambito incluido
    cargo_clean = cargo.split(' ')[0] if ' ' in cargo else cargo
    
    if cargo_clean == "Elector" and (ambito == "Provincial" or "Provincial" in ambito):
        return 1
    elif cargo_clean == "Diputado" and (ambito == "Provincial" or "Provincial" in ambito):
        return 2
    elif cargo_clean == "Senador" and (ambito == "Provincial" or "Provincial" in ambito):
        return 3
    elif cargo_clean == "Diputado" and (ambito == "Nacional" or "Nacional" in ambito):
        return 4
    else:
        return 0.5  # Nivel para "Otro Cargo"

# Esta función ya no es necesaria porque ahora trabajamos directamente con datos en memoria
# y la generación del HTML se hace en generar_visualizacion_interactiva

def generar_html_visualizacion_con_datos_embebidos(json_data):
    """
    Genera el contenido HTML con los datos JSON embebidos.
    
    Args:
        json_data: Datos JSON como string que se embeben en el HTML
        
    Returns:
        str: Contenido HTML completo con datos embebidos
    """    # Escapar cualquier carácter especial que pueda causar problemas con JavaScript
    # Eliminamos el uso de escape personalizado y usamos directamente el json
    
    # Creamos la plantilla HTML con los datos JSON embebidos siguiendo el modelo del ejemplo
    html_template = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visualización Interactiva de Trayectorias</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }
        h1, h2, h3 {
            color: #333;
        }
        h1 {
            border-bottom: 2px solid #ccc;
            padding-bottom: 10px;
        }
        .info-box {
            background-color: #e8f4f8;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            border: 1px solid #bde0f3;
        }
        .controls {
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            border: 1px solid #ddd;
        }
        .control-group {
            margin-bottom: 15px;
        }
        .control-group h3 {
            margin-top: 0;
            margin-bottom: 10px;
            font-size: 16px;
        }
        .checkbox-group {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        .checkbox-item {
            display: flex;
            align-items: center;
            padding: 5px 10px;
            background: white;
            border: 1px solid #ddd;
            border-radius: 3px;
        }
        .checkbox-color {
            width: 15px;
            height: 15px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 5px;
        }
        .tooltip {
            position: absolute;
            padding: 10px;
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid #ddd;
            border-radius: 5px;
            pointer-events: none;
            font-size: 14px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            max-width: 250px;
        }
        .visualization {
            width: 100%;
            height: 600px;
            border: 1px solid #ddd;
            background-color: #f9f9f9;
            margin-top: 20px;
            margin-bottom: 30px;
            position: relative;
            z-index: 1;
        }
        .axis text {
            font-size: 12px;
        }
        .axis path, .axis line {
            fill: none;
            stroke: #333;
            shape-rendering: crispEdges;
        }
        .grid line {
            stroke: #eee;
            shape-rendering: crispEdges;
        }
        .candidato-point {
            cursor: pointer;
        }
        #search-container {
            margin-top: 15px;
        }
        #search-input {
            width: 300px;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 3px;
            margin-right: 10px;
        }
        #search-results {
            max-height: 200px;
            overflow-y: auto;
            border: 1px solid #ddd;
            border-radius: 3px;
            margin-top: 5px;
            display: none;
        }
        .search-result-item {
            padding: 8px;
            cursor: pointer;
            border-bottom: 1px solid #eee;
        }
        .search-result-item:hover {
            background-color: #f5f5f5;
        }
        .stats-panel {
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            margin-top: 40px;
            border: 1px solid #ddd;
            clear: both;
        }
        .legend-item {
            display: flex;
            align-items: center;
            margin-bottom: 5px;
        }
        .legend-color {
            width: 15px;
            height: 15px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 5px;
        }
        .btn {
            padding: 8px 15px;
            background-color: #4CAF50;
            border: none;
            color: white;
            border-radius: 3px;
            cursor: pointer;
            margin-right: 5px;
        }
        .btn:hover {
            background-color: #45a049;
        }
        .periodo-peronista {
            fill: rgba(255, 235, 180, 0.3);
            stroke: none;
        }
        .highlight-area {
            opacity: 0.8;
        }
        .candidate-highlight {
            stroke-width: 3;
            opacity: 1;
        }
        .candidate-highlight circle {
            stroke-width: 2;
            r: 6;
        }
        .candidate-fade {
            opacity: 0.2;
        }
        .candidate-highlight .bifurcacion {
            stroke-width: 2;
            opacity: 0.9;
        }
        .candidate-fade .bifurcacion {
            opacity: 0.2;
        }
    </style>    <script id="embedded-json-data" type="application/json">{DATA_PLACEHOLDER}</script>
    <script type="text/javascript">
        // Datos embebidos directamente en el HTML - cargados desde el script JSON
        const datosVisualizacion = JSON.parse(document.getElementById('embedded-json-data').textContent);
    </script>
</head>
<body>
    <h1>Visualización Interactiva de Trayectorias Políticas (1905-1955)</h1>
    
    <div class="info-box">
        <p>Esta visualización muestra las trayectorias políticas de los candidatos peronistas que tuvieron experiencia política previa.</p>
        <h3>Cómo interpretar el gráfico:</h3>
        <ul>
            <li>Cada línea representa la carrera política de un candidato a lo largo del tiempo</li>
            <li>Los círculos rellenos indican candidaturas donde el candidato fue electo</li>
            <li>Los círculos vacíos representan candidaturas no exitosas</li>
            <li>Las líneas punteadas verticales indican que el candidato tuvo múltiples candidaturas en un mismo año</li>
        </ul>
        <p>Utilice los controles para filtrar por partido de origen o buscar candidatos específicos.</p>
    </div>
    
    <div class="controls">
        <div class="control-group">
            <h3>Filtrar por Grupos Partidarios</h3>
            <div class="checkbox-group" id="grupos-filter">
                <!-- Los checkboxes se generarán dinámicamente con JavaScript -->
            </div>
        </div>
        
        <div class="control-group">
            <h3>Otras Opciones</h3>
            <div class="checkbox-group">
                <label class="checkbox-item">
                    <input type="checkbox" id="solo-electos" value="electos"> Solo candidatos electos en el peronismo
                </label>
                <label class="checkbox-item">
                    <input type="checkbox" id="resaltar-peronismo" value="peronismo" checked> Resaltar periodo peronista
                </label>
            </div>
        </div>
        
        <div id="search-container">
            <h3>Buscar Candidato</h3>
            <div>
                <input type="text" id="search-input" placeholder="Nombre del candidato...">
                <button id="search-btn" class="btn">Buscar</button>
                <button id="clear-search-btn" class="btn" style="background-color: #f44336;">Limpiar</button>
            </div>
            <div id="search-results"></div>
        </div>
    </div>
    
    <div id="visualization" class="visualization"></div>
    
    <div class="stats-panel">
        <h3>Estadísticas</h3>
        <div id="stats-content">
            <!-- Se llenará con JavaScript -->
        </div>
    </div>
    
    <script>
        // Usar directamente los datos embebidos
        let data = datosVisualizacion;
        let svg, xScale, yScale, tooltip;
        let width, height, innerWidth, innerHeight, margin;
        let searchHighlight = null;
        let candidatosVisibles = new Set();
        
        document.addEventListener('DOMContentLoaded', function() {
            // Referencias a elementos DOM
            const searchBtn = document.getElementById("search-btn");
            const clearSearchBtn = document.getElementById("clear-search-btn");
            const searchInput = document.getElementById("search-input");
            const searchResults = document.getElementById("search-results");
            
            // Inicializar visualización
            initializeVisualization();
            
            function initializeVisualization() {
                console.log("Inicializando visualización...");
                
                // Configurar filtros y actualizar estadísticas
                setupFilters();
                updateStats();
                
                // Configuración de tamaños
                width = document.getElementById("visualization").clientWidth;
                height = 500;
                margin = { top: 50, right: 50, bottom: 50, left: 100 };
                innerWidth = width - margin.left - margin.right;
                innerHeight = height - margin.top - margin.bottom;
                
                // Crear SVG principal
                svg = d3.select("#visualization")
                    .append("svg")
                    .attr("width", width)
                    .attr("height", height)
                    .append("g")
                    .attr("transform", `translate(${margin.left},${margin.top})`);
                
                // Tooltip para información al pasar el mouse
                tooltip = d3.select("#visualization")
                    .append("div")
                    .attr("class", "tooltip")
                    .style("opacity", 0);
                
                // Años mínimos y máximos para escalas
                const minYear = d3.min(data.candidatos, d => d3.min(d.puntos, p => p.anio));
                const maxYear = d3.max(data.candidatos, d => d3.max(d.puntos, p => p.anio));
                
                // Escalas
                xScale = d3.scaleLinear()
                    .domain([minYear - 2, maxYear + 2])
                    .range([0, innerWidth]);
                
                yScale = d3.scaleLinear()
                    .domain([0, 5])
                    .range([innerHeight, 0]);
                
                // Ejes
                const xAxis = d3.axisBottom(xScale)
                    .tickFormat(d3.format("d"))
                    .ticks(10);
                
                const yAxis = d3.axisLeft(yScale)
                    .tickFormat(d => {
                        const nivel = data.niveles.find(n => n.nivel === d);
                        return nivel ? nivel.nombre : "";
                    })
                    .tickValues(data.niveles.map(n => n.nivel));
                
                // Dibujar ejes
                svg.append("g")
                    .attr("class", "x-axis")
                    .attr("transform", `translate(0,${innerHeight})`)
                    .call(xAxis);
                
                svg.append("g")
                    .attr("class", "y-axis")
                    .call(yAxis);
                
                // Líneas de cuadrícula
                svg.append("g")
                    .attr("class", "grid")
                    .selectAll("line")
                    .data(d3.range(minYear, maxYear + 1, 1))
                    .enter()
                    .append("line")
                    .attr("x1", d => xScale(d))
                    .attr("y1", 0)
                    .attr("x2", d => xScale(d))
                    .attr("y2", innerHeight)
                    .attr("stroke", "#eee")
                    .attr("stroke-width", 1);
                
                // Resaltar período peronista (1943-1955)
                const periodoPeronista = svg.append("rect")
                    .attr("class", "periodo-peronista")
                    .attr("x", xScale(1943))
                    .attr("y", 0)
                    .attr("width", xScale(1955) - xScale(1943))
                    .attr("height", innerHeight)
                    .attr("visibility", "visible");
                
                // Actualizar visibilidad del período peronista según checkbox
                document.getElementById("resaltar-peronismo").addEventListener("change", function() {
                    periodoPeronista.attr("visibility", this.checked ? "visible" : "hidden");
                });
                
                // Renderizar trayectorias
                renderTrayectorias();
            }
            
            function renderTrayectorias() {
                // Limpiar visualización anterior
                svg.selectAll(".trayectorias").remove();
                
                // Filtrar candidatos según checkboxes
                const gruposSeleccionados = [];
                document.querySelectorAll('#grupos-filter input:checked').forEach(checkbox => {
                    gruposSeleccionados.push(checkbox.value);
                });
                
                const soloElectos = document.getElementById("solo-electos").checked;
                
                const candidatosFiltrados = data.candidatos.filter(candidato => {
                    // Filtrar por grupo partidario
                    if (gruposSeleccionados.length > 0 && !gruposSeleccionados.includes(candidato.grupo)) {
                        return false;
                    }
                    
                    // Filtrar por candidatos electos en el peronismo si está marcado
                    if (soloElectos && !candidato.electoEnPeronismo) {
                        return false;
                    }
                    
                    return true;
                });
                
                // Actualizar set de candidatos visibles
                candidatosVisibles = new Set(candidatosFiltrados.map(c => c.id));
                
                // Contenedor para las trayectorias
                const trayectoriasGroup = svg.append("g")
                    .attr("class", "trayectorias");
                
                // Dibujar trayectorias para cada candidato
                candidatosFiltrados.forEach(candidato => {
                    // Grupo para cada candidato
                    const candidatoGroup = trayectoriasGroup.append("g")
                        .attr("class", "candidato")
                        .attr("data-id", candidato.id)
                        .classed("candidate-highlight", searchHighlight === candidato.id)
                        .classed("candidate-fade", searchHighlight !== null && searchHighlight !== candidato.id);
                    
                    // Dibujar línea de trayectoria si hay más de un punto
                    if (candidato.puntos.length > 1) {
                        // Ordenar puntos por año
                        const puntosOrdenados = [...candidato.puntos].sort((a, b) => a.anio - b.anio);
                        
                        // Definir línea
                        const line = d3.line()
                            .x(d => xScale(d.anio))
                            .y(d => yScale(d.nivel))
                            .curve(d3.curveMonotoneX);
                        
                        // Dibujar línea
                        candidatoGroup.append("path")
                            .datum(puntosOrdenados)
                            .attr("fill", "none")
                            .attr("stroke", () => {
                                const grupo = data.grupos.find(g => g.nombre === candidato.grupo);
                                return grupo ? grupo.color : "#999";
                            })
                            .attr("stroke-width", 1.5)
                            .attr("opacity", 0.7)
                            .attr("d", line);
                    }
                    
                    // Gestionar bifurcaciones (múltiples cargos en el mismo año)
                    const puntosAgrupados = d3.group(candidato.puntos, d => d.anio);
                    puntosAgrupados.forEach((puntos, anio) => {
                        // Si hay más de un punto en el mismo año, dibujar líneas verticales
                        if (puntos.length > 1) {
                            const niveles = puntos.map(p => p.nivel).sort((a, b) => a - b);
                            
                            candidatoGroup.append("line")
                                .attr("class", "bifurcacion")
                                .attr("x1", xScale(anio))
                                .attr("y1", yScale(niveles[0]))
                                .attr("x2", xScale(anio))
                                .attr("y2", yScale(niveles[niveles.length - 1]))
                                .attr("stroke", () => {
                                    const grupo = data.grupos.find(g => g.nombre === candidato.grupo);
                                    return grupo ? grupo.color : "#999";
                                })
                                .attr("stroke-width", 1.5)
                                .attr("stroke-dasharray", "3,3")
                                .attr("opacity", 0.7);
                        }
                    });
                    
                    // Dibujar puntos para cada candidatura
                    candidatoGroup.selectAll("circle")
                        .data(candidato.puntos)
                        .enter()
                        .append("circle")
                        .attr("class", "candidato-point")
                        .attr("cx", d => xScale(d.anio))
                        .attr("cy", d => yScale(d.nivel))
                        .attr("r", d => d.es_peronista ? 5 : 3)
                        .attr("fill", d => {
                            // Si es electo, se usa el color completo
                            if (d.electo) {
                                return d.es_peronista ? "#E91E63" : 
                                    (() => {
                                        const grupo = data.grupos.find(g => g.nombre === candidato.grupo);
                                        return grupo ? grupo.color : "#999";
                                    })();
                            } else {
                                // Si no es electo, se usa el color de borde y relleno blanco
                                return "white";
                            }
                        })
                        .attr("stroke", d => {
                            return d.es_peronista ? "#E91E63" : 
                                (() => {
                                    const grupo = data.grupos.find(g => g.nombre === candidato.grupo);
                                    return grupo ? grupo.color : "#999";
                                })();
                        })
                        .attr("stroke-width", 1.5)
                        .style("cursor", "pointer")
                        .on("mouseover", function(event, d) {
                            d3.select(this)
                                .attr("r", d.es_peronista ? 7 : 5)
                                .attr("stroke-width", 2);
                                
                            tooltip.transition()
                                .duration(200)
                                .style("opacity", 1);
                                
                            tooltip.html(`
                                <h4>${candidato.nombre}</h4>
                                <p><strong>Año:</strong> ${d.anio}</p>
                                <p><strong>Cargo:</strong> ${d.cargo}</p>
                                <p><strong>Partido:</strong> ${d.partido}</p>
                                <p><strong>Resultado:</strong> ${d.electo ? "Electo" : "No electo"}</p>
                                <p><strong>Grupo:</strong> ${candidato.grupo}</p>
                            `)
                            .style("left", (event.pageX - document.getElementById("visualization").offsetLeft + 10) + "px")
                            .style("top", (event.pageY - document.getElementById("visualization").offsetTop - 80) + "px");
                        })
                        .on("mouseout", function(event, d) {
                            d3.select(this)
                                .attr("r", d.es_peronista ? 5 : 3)
                                .attr("stroke-width", 1.5);
                                
                            tooltip.transition()
                                .duration(500)
                                .style("opacity", 0);
                        })
                        .on("click", function(event, d) {
                            // Al hacer clic en un punto, resaltar el candidato
                            searchHighlight = candidato.id;
                            renderTrayectorias();
                        });
                });
                
                // Actualizar estadísticas
                updateStats(candidatosFiltrados);
            }
            
            function setupFilters() {
                // Configurar checkboxes para grupos partidarios
                const gruposFilter = document.getElementById("grupos-filter");
                gruposFilter.innerHTML = ""; // Limpiar contenido previo
                
                data.grupos.forEach(grupo => {
                    const label = document.createElement("label");
                    label.className = "checkbox-item";
                    
                    const input = document.createElement("input");
                    input.type = "checkbox";
                    input.value = grupo.nombre;
                    input.checked = true;
                    input.addEventListener("change", renderTrayectorias);
                    
                    const colorSpan = document.createElement("span");
                    colorSpan.className = "checkbox-color";
                    colorSpan.style.backgroundColor = grupo.color;
                    
                    label.appendChild(input);
                    label.appendChild(colorSpan);
                    label.appendChild(document.createTextNode(grupo.nombre));
                    
                    gruposFilter.appendChild(label);
                });
                
                // Evento para filtro de solo electos
                document.getElementById("solo-electos").addEventListener("change", renderTrayectorias);
            }
            
            function updateStats(candidatosFiltrados = null) {
                const stats = document.getElementById("stats-content");
                const candidatos = candidatosFiltrados || data.candidatos;
                
                if (!candidatos.length) {
                    stats.innerHTML = "<p>No hay candidatos que cumplan con los filtros seleccionados.</p>";
                    return;
                }
                
                // Contar grupos partidarios
                const gruposCounts = {};
                candidatos.forEach(c => {
                    gruposCounts[c.grupo] = (gruposCounts[c.grupo] || 0) + 1;
                });
                
                // Estadísticas de candidatos electos vs no electos en el peronismo
                const electosPeronismo = candidatos.filter(c => c.electoEnPeronismo).length;
                const totalCandidatos = candidatos.length;
                
                // Generar HTML de estadísticas
                let statsHTML = `
                    <p><strong>Total candidatos:</strong> ${totalCandidatos}</p>
                    <p><strong>Electos en el peronismo:</strong> ${electosPeronismo} (${Math.round(electosPeronismo/totalCandidatos*100)}%)</p>
                    <h4>Distribución por origen partidario:</h4>
                    <div class="grupos-stats">
                `;
                
                // Añadir distribución por grupos
                Object.entries(gruposCounts).forEach(([grupo, cantidad]) => {
                    const grupoInfo = data.grupos.find(g => g.nombre === grupo);
                    const color = grupoInfo ? grupoInfo.color : "#999";
                    const porcentaje = Math.round(cantidad/totalCandidatos*100);
                    
                    statsHTML += `
                        <div class="legend-item">
                            <span class="legend-color" style="background-color: ${color};"></span>
                            <span>${grupo}: ${cantidad} (${porcentaje}%)</span>
                        </div>
                    `;
                });
                
                statsHTML += `</div>`;
                stats.innerHTML = statsHTML;
            }
            
            // Función de búsqueda
            function handleSearch() {
                const searchTerm = searchInput.value.toLowerCase().trim();
                
                if (!searchTerm) {
                    clearSearch();
                    return;
                }
                
                // Buscar candidato por nombre
                const candidatoEncontrado = data.candidatos.find(c => 
                    c.nombre.toLowerCase().includes(searchTerm) && candidatosVisibles.has(c.id));
                    
                if (candidatoEncontrado) {
                    // Resaltar el candidato encontrado
                    searchHighlight = candidatoEncontrado.id;
                    renderTrayectorias();
                    
                    // Ocultar resultados de búsqueda
                    searchResults.style.display = "none";
                } else {
                    alert("No se encontró ningún candidato con ese nombre o no está visible con los filtros actuales.");
                }
            }
            
            function clearSearch() {
                searchInput.value = "";
                searchHighlight = null;
                searchResults.style.display = "none";
                renderTrayectorias();
            }
            
            function showSearchSuggestions() {
                const searchTerm = searchInput.value.toLowerCase().trim();
                
                if (!searchTerm || searchTerm.length < 2) {
                    searchResults.style.display = "none";
                    return;
                }
                
                // Filtrar candidatos que coincidan con la búsqueda y estén visibles
                const candidatosFiltrados = data.candidatos
                    .filter(c => c.nombre.toLowerCase().includes(searchTerm) && candidatosVisibles.has(c.id))
                    .slice(0, 10); // Limitar a 10 resultados
                    
                // Mostrar resultados
                if (candidatosFiltrados.length > 0) {
                    searchResults.innerHTML = "";
                    searchResults.style.display = "block";
                    
                    candidatosFiltrados.forEach(c => {
                        const resultItem = document.createElement("div");
                        resultItem.className = "search-result-item";
                        resultItem.textContent = c.nombre;
                        resultItem.addEventListener("click", function() {
                            searchInput.value = c.nombre;
                            searchHighlight = c.id;
                            searchResults.style.display = "none";
                            renderTrayectorias();
                        });
                        searchResults.appendChild(resultItem);
                    });
                } else {
                    searchResults.style.display = "none";
                }
            }
                
            // Inicializar eventos
            searchBtn.addEventListener("click", handleSearch);
            clearSearchBtn.addEventListener("click", clearSearch);
            searchInput.addEventListener("input", showSearchSuggestions);
        });
    </script>
</body>
</html>
"""
    
    # Reemplazar el marcador de posición con los datos JSON reales
    html_content = html_template.replace("{DATA_PLACEHOLDER}", json_data)
    return html_content

def generar_html_visualizacion_basico():
    """
    Genera el contenido HTML básico para la visualización interactiva.
    Esta función se mantiene por compatibilidad pero ya no se utiliza.
    
    Returns:
        str: Contenido HTML
    """
    
    # Creamos la plantilla HTML sin usar % para formato
    html_template = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visualización Interactiva de Trayectorias</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }
        h1, h2, h3 {
            color: #333;
        }
        h1 {
            border-bottom: 2px solid #ccc;
            padding-bottom: 10px;
        }
        .controls {
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            border: 1px solid #ddd;
        }
        .control-group {
            margin-bottom: 15px;
        }
        .control-group h3 {
            margin-top: 0;
            margin-bottom: 10px;
            font-size: 16px;
        }
        .checkbox-group {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        .checkbox-item {
            display: flex;
            align-items: center;
            padding: 5px 10px;
            background: white;
            border: 1px solid #ddd;
            border-radius: 3px;
        }
        .checkbox-color {
            width: 15px;
            height: 15px;
            display: inline-block;
            margin-right: 5px;
            border-radius: 2px;
        }
        #visualization {
            width: 100%;
            height: 550px;
            border: 1px solid #ddd;
            background-color: #f9f9f9;
            position: relative;
        }
        .tooltip {
            position: absolute;
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid #ddd;
            border-radius: 3px;
            padding: 10px;
            font-size: 13px;
            pointer-events: none;
            box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
            z-index: 100;
        }
        .tooltip h4 {
            margin: 0 0 5px 0;
        }
        .tooltip p {
            margin: 0;
        }
    </style>
</head>
<body>
    <h1>Visualización Interactiva de Trayectorias Políticas</h1>
    
    <div class="controls">
        <div class="control-group">
            <h3>Filtrar por Grupo Partidario</h3>
            <div class="checkbox-group" id="filtro-grupos">
                <!-- Se llenará con JavaScript -->
            </div>
        </div>
        
        <div class="control-group">
            <h3>Filtrar por Nivel de Cargo</h3>
            <div class="checkbox-group" id="filtro-niveles">
                <!-- Se llenará con JavaScript -->
            </div>
        </div>
        
        <div class="control-group">
            <h3>Filtrar por Resultado Electoral</h3>
            <div class="checkbox-group" id="filtro-resultados">
                <div class="checkbox-item">
                    <input type="checkbox" id="filtro-electos" checked>
                    <label for="filtro-electos">Electos</label>
                </div>
                <div class="checkbox-item">
                    <input type="checkbox" id="filtro-no-electos" checked>
                    <label for="filtro-no-electos">No Electos</label>
                </div>
            </div>
        </div>
    </div>
    
    <div id="visualization"></div>
      <script>        // Usar los datos embebidos directamente
        const data = datosVisualizacion;
        createVisualization(data);
            
        function createVisualization(data) {
            // Configuración
            const width = document.getElementById("visualization").clientWidth;
            const height = 500;
            const margin = {top: 50, right: 50, bottom: 50, left: 100};
            const innerWidth = width - margin.left - margin.right;
            const innerHeight = height - margin.top - margin.bottom;
            
            // Años mínimos y máximos
            const minYear = d3.min(data.candidatos, d => d3.min(d.puntos, p => p.anio));
            const maxYear = d3.max(data.candidatos, d => d3.max(d.puntos, p => p.anio));
            
            // Escalas
            const xScale = d3.scaleLinear()
                .domain([minYear - 2, maxYear + 2])
                .range([0, innerWidth]);
                
            const yScale = d3.scaleLinear()
                .domain([0, 5])
                .range([innerHeight, 0]);
                
            // SVG principal
            const svg = d3.select("#visualization")
                .append("svg")
                    .attr("width", width)
                    .attr("height", height)
                .append("g")
                    .attr("transform", `translate(${margin.left},${margin.top})`);
                    
            // Tooltip
            const tooltip = d3.select("#visualization")
                .append("div")
                .attr("class", "tooltip")
                .style("opacity", 0);
                
            // Ejes
            const xAxis = d3.axisBottom(xScale)
                .tickFormat(d3.format("d"))
                .ticks(10);
                
            const yAxis = d3.axisLeft(yScale)
                .tickFormat(d => {
                    const nivel = data.niveles.find(n => n.nivel === d);
                    return nivel ? nivel.nombre : "";
                })
                .tickValues(data.niveles.map(n => n.nivel));
                
            // Dibujar ejes
            svg.append("g")
                .attr("class", "x-axis")
                .attr("transform", `translate(0,${innerHeight})`)
                .call(xAxis);
                
            svg.append("g")
                .attr("class", "y-axis")
                .call(yAxis);
                
            // Líneas de la cuadrícula
            svg.append("g")
                .attr("class", "grid")
                .selectAll("line")
                .data(d3.range(minYear, maxYear + 1, 1))
                .enter()
                .append("line")
                .attr("x1", d => xScale(d))
                .attr("y1", 0)
                .attr("x2", d => xScale(d))
                .attr("y2", innerHeight)
                .attr("stroke", "#eee")
                .attr("stroke-width", 1);
                
            // Área de visualización principal
            const visualization = svg.append("g")
                .attr("class", "visualization");
                
            // Dibujar trayectorias
            function drawTrajectories(filteredData) {
                // Limpiar visualización anterior
                visualization.selectAll("*").remove();
                
                // Dibujar líneas de trayectoria
                filteredData.forEach(candidato => {
                    if (candidato.puntos.length > 1) {
                        // Definir línea
                        const line = d3.line()
                            .x(d => xScale(d.anio))
                            .y(d => yScale(d.nivel))
                            .curve(d3.curveMonotoneX);
                            
                        // Dibujar línea
                        visualization.append("path")
                            .datum(candidato.puntos)
                            .attr("fill", "none")
                            .attr("stroke", d => {
                                const grupo = data.grupos.find(g => g.nombre === candidato.grupo);
                                return grupo ? grupo.color : "#999";
                            })
                            .attr("stroke-width", 1.5)
                            .attr("opacity", 0.7)
                            .attr("d", line);
                    }
                    
                    // Dibujar puntos
                    visualization.selectAll(null)
                        .data(candidato.puntos)
                        .enter()
                        .append("circle")
                        .attr("cx", d => xScale(d.anio))
                        .attr("cy", d => yScale(d.nivel))
                        .attr("r", d => d.es_peronista ? 5 : 3)
                        .attr("fill", d => d.es_peronista ? "#E91E63" : 
                            (() => {
                                const grupo = data.grupos.find(g => g.nombre === candidato.grupo);
                                return grupo ? grupo.color : "#999";
                            })())
                        .attr("stroke", "#fff")
                        .attr("stroke-width", 1)
                        .attr("opacity", d => d.electo ? 1 : 0.5)
                        .style("cursor", "pointer")
                        .on("mouseover", function(event, d) {
                            d3.select(this)
                                .attr("r", d.es_peronista ? 7 : 5)
                                .attr("stroke-width", 2);
                                
                            tooltip.transition()
                                .duration(200)
                                .style("opacity", 1);
                                
                            tooltip.html(`
                                <h4>${candidato.nombre}</h4>
                                <p><strong>Año:</strong> ${d.anio}</p>
                                <p><strong>Cargo:</strong> ${d.cargo}</p>
                                <p><strong>Partido:</strong> ${d.partido}</p>
                                <p><strong>Resultado:</strong> ${d.electo ? "Electo" : "No electo"}</p>
                                <p><strong>Grupo:</strong> ${candidato.grupo}</p>
                            `)
                            .style("left", (event.pageX - document.getElementById("visualization").offsetLeft + 10) + "px")
                            .style("top", (event.pageY - document.getElementById("visualization").offsetTop - 80) + "px");
                        })
                        .on("mouseout", function(event, d) {
                            d3.select(this)
                                .attr("r", d.es_peronista ? 5 : 3)
                                .attr("stroke-width", 1);
                                
                            tooltip.transition()
                                .duration(500)
                                .style("opacity", 0);
                        });
                });
            }
            
            // Función para aplicar filtros
            function applyFilters() {
                // Obtener valores de los filtros
                const gruposSeleccionados = [];
                document.querySelectorAll('#filtro-grupos input:checked').forEach(checkbox => {
                    gruposSeleccionados.push(checkbox.value);
                });
                
                const nivelesSeleccionados = [];
                document.querySelectorAll('#filtro-niveles input:checked').forEach(checkbox => {
                    nivelesSeleccionados.push(parseFloat(checkbox.value));
                });
                
                const mostrarElectos = document.getElementById('filtro-electos').checked;
                const mostrarNoElectos = document.getElementById('filtro-no-electos').checked;
                
                // Filtrar datos
                const candidatosFiltrados = data.candidatos.filter(candidato => {
                    // Filtrar por grupo
                    if (gruposSeleccionados.length > 0 && !gruposSeleccionados.includes(candidato.grupo)) {
                        return false;
                    }
                    
                    // Filtrar puntos por nivel y resultado electoral
                    candidato.puntosFiltrados = candidato.puntos.filter(punto => {
                        // Filtrar por nivel
                        if (nivelesSeleccionados.length > 0 && !nivelesSeleccionados.includes(punto.nivel)) {
                            return false;
                        }
                        
                        // Filtrar por resultado electoral
                        if (!mostrarElectos && punto.electo) return false;
                        if (!mostrarNoElectos && !punto.electo) return false;
                        
                        return true;
                    });
                    
                    return candidato.puntosFiltrados.length > 0;
                });
                
                // Crear copia de los datos filtrados para la visualización
                const datosFiltrados = candidatosFiltrados.map(c => ({
                    ...c,
                    puntos: c.puntosFiltrados
                }));
                
                // Actualizar visualización
                drawTrajectories(datosFiltrados);
            }
            
            // Inicializar filtros
            function setupFilters() {
                // Filtros de grupos
                const gruposContainer = document.getElementById('filtro-grupos');
                data.grupos.forEach(grupo => {
                    const item = document.createElement('div');
                    item.className = 'checkbox-item';
                    
                    const color = document.createElement('span');
                    color.className = 'checkbox-color';
                    color.style.backgroundColor = grupo.color;
                    
                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.id = `grupo-${grupo.nombre.toLowerCase().replace(/\\s+/g, '-')}`;
                    checkbox.value = grupo.nombre;
                    checkbox.checked = true;
                    checkbox.addEventListener('change', applyFilters);
                    
                    const label = document.createElement('label');
                    label.htmlFor = checkbox.id;
                    label.textContent = grupo.nombre;
                    
                    item.appendChild(checkbox);
                    item.appendChild(color);
                    item.appendChild(label);
                    gruposContainer.appendChild(item);
                });
                
                // Filtros de niveles
                const nivelesContainer = document.getElementById('filtro-niveles');
                data.niveles.forEach(nivel => {
                    const item = document.createElement('div');
                    item.className = 'checkbox-item';
                    
                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.id = `nivel-${nivel.nivel}`;
                    checkbox.value = nivel.nivel;
                    checkbox.checked = true;
                    checkbox.addEventListener('change', applyFilters);
                    
                    const label = document.createElement('label');
                    label.htmlFor = checkbox.id;
                    label.textContent = nivel.nombre;
                    
                    item.appendChild(checkbox);
                    item.appendChild(label);
                    nivelesContainer.appendChild(item);
                });
                
                // Filtros de resultados
                document.getElementById('filtro-electos').addEventListener('change', applyFilters);
                document.getElementById('filtro-no-electos').addEventListener('change', applyFilters);
            }
            
            // Inicializar
            setupFilters();
            applyFilters();
        }    </script>
</html>
"""
    
    return html_template

def generar_visualizacion_interactiva():
    """
    Función principal que genera la visualización interactiva de trayectorias políticas.
    
    Returns:
        bool: True si se genera correctamente, False en caso contrario
    """
    try:
        print("GENERANDO VISUALIZACIÓN INTERACTIVA DE TRAYECTORIAS POLÍTICAS")
        
        # 1. Obtener datos de trayectorias
        print("1. Consultando datos de trayectorias...")
        detalle_trayectorias = obtener_detalle_trayectoria_candidatos_peronistas()
        print(f"   ✓ {len(detalle_trayectorias)} registros de trayectorias recuperados")
        
        # 2. Generar datos JSON para visualización (ahora directamente como objeto Python)
        print("2. Generando datos para visualización interactiva...")
        datos_json = generar_datos_trayectorias_json(detalle_trayectorias)
        if not datos_json:
            print("   ✗ Error al generar datos JSON para visualización")
            return False
            
        # 3. Generar HTML con datos JSON embebidos directamente
        print("3. Generando HTML con datos JSON embebidos...")
        
        # Convertir a string JSON para embeber
        json_str = json.dumps(datos_json, ensure_ascii=False)
        
        # Generar HTML con los datos embebidos de forma segura
        html_content = generar_html_visualizacion_con_datos_embebidos(json_str)
        
        # Ruta de salida para el HTML
        output_dir = os.path.join(project_root, "informes")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "visualizacion_trayectorias.html")
        
        # Guardar el HTML
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print(f"   ✓ HTML con visualización interactiva generado en: {output_path}")
        
        print(f"\n✓ Visualización interactiva generada correctamente")
        print(f"  - HTML: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error al generar visualización interactiva: {e}")
        return False

if __name__ == "__main__":
    generar_visualizacion_interactiva()
