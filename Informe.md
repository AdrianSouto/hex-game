# Resumen de Player.py

## Estructura General
- Implementa un jugador de Hex usando el algoritmo Minimax con poda alfa-beta.
- Contiene dos clases principales: `Player` (clase base) y `PlayerAdrIAn` (implementación concreta).

## Clases Principales

### `Player`
- **Atributos**:
  - `player_id`: Identificador del jugador (1 o 2)
- **Métodos**:
  - `play(board)`: Método abstracto que debe implementarse

### `PlayerAdrIAn` (hereda de `Player`)
- **Métodos**:
  - `play(board)`: 
    - Usa `minimax()` para decidir el mejor movimiento
    - Devuelve la coordenada elegida
  - `minimax()`: Implementación del algoritmo con:
    - Poda alfa-beta
    - Profundidad adaptable
    - Heurística personalizada

## Algoritmo Minimax
- **Parámetros**:
  - `board`: Estado actual del tablero
  - `depth`: Profundidad actual de búsqueda
  - `maximizing_player`: Turno del jugador maximizador
  - `alpha`, `beta`: Valores para poda alfa-beta
  - `heuristic`: Función de evaluación heurística

- **Lógica**:
  1. Calcula movimientos posibles
  2. Ajusta profundidad según densidad de movimientos
  3. Evalúa condiciones terminales (victoria/derrota)
  4. Recorre movimientos posibles con:
     - Simulación de movimiento
     - Llamada recursiva
     - Deshacer movimiento
     - Actualización de alpha/beta
     - Poda cuando sea posible

## Función de Evaluación (`evaluate4`)
- **Objetivo**: Calcular calidad de posición para el jugador
- **Factores considerados**:
  - Distancia a bordes libres (según dirección de victoria)
  - Presencia de "puentes" (patrones estratégicos)
  - Cierres de puente (patrones defensivos/offensivos)
  - Conexión completa (victoria inmediata)

## Funciones Auxiliares
- `bfs_same_player()`: BFS para encontrar piezas conectadas
- `dfs_forest_extremes()`: DFS para calcular extremos de grupos de piezas
  - Devuelve 4 diccionarios con posiciones extremas (derecha, izquierda, arriba, abajo)
- `is_valid()`: Verifica si una posición está dentro del tablero

## Detalles Clave
- Profundidad adaptable según densidad de movimientos
- Heurística considera:
  - Distancia euclidiana a bordes relevantes
  - Patrones especiales (puentes)
  - Conexiones potenciales
- Optimización mediante poda alfa-beta