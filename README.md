# Reporte: Estrategia de Jugadas del Bot Hex

## Introducción

El bot **HexBot** implementado en este código juega en el juego **Hex**, utilizando una combinación de **Minimax con poda alfa-beta** y **heurísticas avanzadas** para tomar decisiones estratégicas. A continuación, se detalla cómo el bot evalúa la situación en el tablero, cómo determina la profundidad de búsqueda, y cómo utiliza diferentes estrategias para elegir las mejores jugadas.

## 1. Determinación de la Profundidad Dinámica de Búsqueda

### Estrategia

La profundidad de búsqueda del algoritmo **Minimax** no es fija, sino que se ajusta dinámicamente según el estado del tablero. Esto se realiza mediante la función `get_dynamic_depth()`, que calcula la profundidad en función de la cantidad de celdas vacías disponibles en el tablero:

- **Si el tablero está mayormente vacío** (más del 80% de las celdas están vacías), se utilizará una profundidad de **3 niveles**.
    
- **Si el tablero está medianamente lleno** (entre el 30% y el 80% de las celdas vacías), se utilizará una profundidad de **5 niveles**.
    
- **Si el tablero está casi lleno** (menos del 30% de las celdas vacías), se utilizará una profundidad de **7 niveles**.

Este enfoque permite ajustar la cantidad de tiempo invertido en el análisis de jugadas, optimizando el tiempo de respuesta del bot.

## 2. Algoritmo Minimax con Poda Alfa-Beta

### Estrategia

El bot utiliza el algoritmo **Minimax con poda alfa-beta** para evaluar los posibles movimientos y elegir la jugada más favorable. El algoritmo se realiza de la siguiente manera:

- **Evaluación del Estado del Juego**: En cada nivel de búsqueda, se evalúan los tableros resultantes de cada movimiento, utilizando la función `evaluate()`.
    
- **Poda Alfa-Beta**: Durante la búsqueda de las jugadas, el algoritmo utiliza dos valores, **alfa** y **beta**, para cortar ramas del árbol de búsqueda que no pueden afectar el resultado final. Esto mejora significativamente la eficiencia del algoritmo, reduciendo el número de jugadas evaluadas.

### Roles de Maximización y Minimización

- **Maximización**: El bot trata de maximizar su puntuación en su turno, eligiendo las jugadas que resulten en una evaluación más alta.
    
- **Minimización**: Durante el turno del oponente, el bot intenta minimizar la puntuación de las jugadas del rival, eligiendo las jugadas que resulten en una evaluación más baja.

## 3. Evaluación de las Jugadas

La evaluación de cada movimiento se realiza mediante la función `evaluate()`, que tiene en cuenta una serie de factores estratégicos. A continuación, se detallan los principales componentes de la evaluación:

### 3.1. Evaluación General del Tablero

Se asigna una puntuación general al tablero según el número de piezas propias y del oponente. Cada pieza del jugador obtiene una **puntuación positiva** y cada pieza del oponente una **puntuación negativa**. Las celdas vacías se analizan más a fondo para determinar su valor estratégico.

### 3.2. Análisis de Caminos con A*

Se utiliza el algoritmo **A* de búsqueda de caminos** para calcular el costo de los caminos que conectan los bordes del tablero. Este análisis es fundamental para determinar la cercanía de ambos jugadores a completar una conexión. Se penaliza al bot si el oponente está cerca de conectar, y se recompensa si el bot tiene un camino relativamente barato hacia la victoria.

### 3.3. Centralidad y Vecinos

El bot también analiza la **centralidad** de las celdas vacías. Cuanto más cerca de la centralidad se encuentre una celda vacía, más valor tiene, ya que proporciona más oportunidades de movimiento en el futuro. Además, se evalúa el número de **vecinos amistosos** (piezas propias) y **enemigos** (piezas del oponente) cercanos a una celda vacía, otorgando una **bonificación** por tener más piezas amigas cercanas y una **penalización** por la presencia de piezas enemigas.

### 3.4. Bloqueos Estratégicos

El bot identifica **posibles bloqueos** al oponente. Si una pieza propia bloquea una posible conexión del oponente, se le asigna un valor positivo. En particular, se favorecen los bloqueos horizontales si el jugador es el **jugador 1** (que juega de izquierda a derecha) y los bloqueos verticales si el jugador es el **jugador 2** (que juega de arriba hacia abajo).

### 3.5. Cadenas Conectadas

El bot evalúa las **cadenas conectadas** de piezas propias y enemigas. Se premian las cadenas largas de piezas propias, ya que indican un avance significativo hacia la victoria. Por el contrario, las cadenas largas del oponente se penalizan para evitar que el rival complete una conexión rápidamente.

## 4. Movimiento de Defensa de Emergencia

Si el algoritmo no puede encontrar un movimiento óptimo durante la búsqueda, o si una jugada de alta calidad no es posible por alguna razón (por ejemplo, debido a la poda alfa-beta), el bot recurre a una **jugada defensiva**. La función `defensive_fallback_move()` evalúa todos los posibles movimientos y elige el que cause más dificultades al oponente, minimizando su evaluación.

Si no se puede encontrar un movimiento defensivo útil, se elige una **jugada aleatoria** para continuar el juego.

## Conclusión

El **HexBot** utiliza un enfoque sofisticado basado en **Minimax con poda alfa-beta**, evaluaciones heurísticas detalladas y estrategias de defensa para determinar sus movimientos en el juego **Hex**. Mediante la evaluación de la posición actual, la centralidad de las piezas, los caminos posibles, y las cadenas conectadas, el bot toma decisiones informadas que maximizan sus posibilidades de ganar mientras minimizan las oportunidades del oponente. Además, la adaptabilidad de la profundidad de búsqueda y el uso de movimientos de emergencia aseguran que el bot se desempeñe de manera eficiente, incluso cuando el tiempo de decisión es limitado.
