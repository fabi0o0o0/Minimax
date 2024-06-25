#include <iostream>  // Incluye la librería para manejar la entrada y salida estándar
#include <vector>    // Incluye la librería para usar el contenedor vector
#include <queue>     // Incluye la librería para usar el contenedor queue
#include <stack>     // Incluye la librería para usar el contenedor stack
#include <ctime>     // Incluye la librería para manejar el tiempo
#include <cstdlib>   // Incluye la librería para funciones generales como rand() y srand()
#include <algorithm> // Incluye la librería para usar funciones de algoritmos como shuffle
#include <random>    // Incluye la librería para generar números aleatorios

// Definición de las direcciones de movimiento
const int DX[4] = {1, 0, -1, 0}; // Movimiento en el eje x: derecha, sin movimiento, izquierda, sin movimiento
const int DY[4] = {0, 1, 0, -1}; // Movimiento en el eje y: sin movimiento, arriba, sin movimiento, abajo

// Clase para representar el laberinto
class Maze {
public:
    // Constructor que inicializa el laberinto con paredes y el vector de celdas visitadas
    Maze(int width, int height) : width(width), height(height) {
        maze = std::vector<std::vector<char>>(height, std::vector<char>(width, '#')); // Inicializa el laberinto lleno de paredes
        visited = std::vector<std::vector<bool>>(height, std::vector<bool>(width, false)); // Inicializa el vector de celdas visitadas como falso
    }

    // Función para generar el laberinto
    void generate() {
        srand(time(0)); // Inicializa la semilla para la generación de números aleatorios
        carvePassage(1, 1); // Comienza a tallar el laberinto desde la posición (1, 1)
        maze[1][0] = 'E'; // Marca la entrada del laberinto
        maze[height - 2][width - 1] = 'S'; // Marca la salida del laberinto
    }

    // Función para imprimir el laberinto
    void print() const {
        for (const auto& row : maze) { // Itera sobre cada fila del laberinto
            for (char cell : row) { // Itera sobre cada celda de la fila
                std::cout << cell; // Imprime la celda
            }
            std::cout << '\n'; // Salta a la siguiente línea después de imprimir una fila
        }
    }

    // Función para resolver el laberinto
    bool solve() {
        std::queue<std::pair<int, int>> q; // Cola para realizar la búsqueda en anchura (BFS)
        std::vector<std::vector<bool>> visited(height, std::vector<bool>(width, false)); // Vector de celdas visitadas
        std::vector<std::vector<std::pair<int, int>>> parent(height, std::vector<std::pair<int, int>>(width, {-1, -1})); // Vector para rastrear el camino
        q.push({1, 0}); // Empieza la búsqueda desde la entrada
        visited[1][0] = true; // Marca la entrada como visitada

        while (!q.empty()) { // Mientras haya celdas en la cola
            auto [x, y] = q.front(); // Toma la celda al frente de la cola
            q.pop(); // Remueve la celda de la cola

            if (x == height - 2 && y == width - 1) { // Si se ha llegado a la salida
                markPath(parent, x, y); // Marca el camino de la solución en el laberinto
                return true; // Retorna verdadero indicando que se encontró una solución
            }

            for (int i = 0; i < 4; ++i) { // Itera sobre las direcciones de movimiento
                int nx = x + DX[i]; // Calcula la nueva posición en x
                int ny = y + DY[i]; // Calcula la nueva posición en y

                if (isValid(nx, ny) && maze[nx][ny] != '#' && !visited[nx][ny]) { // Si la nueva posición es válida, no es una pared y no ha sido visitada
                    visited[nx][ny] = true; // Marca la nueva posición como visitada
                    parent[nx][ny] = {x, y}; // Guarda el padre de la nueva posición para rastrear el camino
                    q.push({nx, ny}); // Añade la nueva posición a la cola
                }
            }
        }
        return false; // Retorna falso indicando que no se encontró una solución
    }

private:
    int width, height; // Ancho y alto del laberinto
    std::vector<std::vector<char>> maze; // Matriz para representar el laberinto
    std::vector<std::vector<bool>> visited; // Matriz para rastrear las celdas visitadas durante la generación del laberinto

    // Función para verificar si una posición es válida dentro del laberinto
    bool isValid(int x, int y) const {
        return x >= 0 && x < height && y >= 0 && y < width; // La posición es válida si está dentro de los límites del laberinto
    }

    // Función para tallar pasajes en el laberinto
    void carvePassage(int x, int y) {
        visited[x][y] = true; // Marca la posición actual como visitada
        maze[x][y] = ' '; // Crea un pasaje en la posición actual

        std::vector<int> dirs = {0, 1, 2, 3}; // Vector de direcciones de movimiento
        std::random_device rd; // Dispositivo para generación de números aleatorios
        std::mt19937 g(rd()); // Generador de números aleatorios
        std::shuffle(dirs.begin(), dirs.end(), g); // Mezcla aleatoriamente las direcciones de movimiento

        for (int dir : dirs) { // Itera sobre las direcciones de movimiento mezcladas
            int nx = x + DX[dir] * 2; // Calcula la nueva posición en x (movimiento de dos celdas)
            int ny = y + DY[dir] * 2; // Calcula la nueva posición en y (movimiento de dos celdas)

            if (isValid(nx, ny) && !visited[nx][ny]) { // Si la nueva posición es válida y no ha sido visitada
                maze[x + DX[dir]][y + DY[dir]] = ' '; // Crea un pasaje entre la posición actual y la nueva posición
                carvePassage(nx, ny); // Llama recursivamente para tallar pasajes desde la nueva posición
            }
        }
    }

    // Función para marcar el camino de la solución en el laberinto
    void markPath(const std::vector<std::vector<std::pair<int, int>>>& parent, int x, int y) {
        while (x != 1 || y != 0) { // Mientras no se haya regresado a la entrada
            maze[x][y] = '*'; // Marca la posición actual como parte del camino de la solución
            auto [px, py] = parent[x][y]; // Obtiene la posición del padre
            x = px; // Actualiza la posición actual a la posición del padre
            y = py; // Actualiza la posición actual a la posición del padre
        }
    }
};

int main() {
    int width, height; // Ancho y alto del laberinto
    std::cout << "Ingrese el ancho del laberinto: "; // Solicita el ancho del laberinto
    std::cin >> width; // Lee el ancho del laberinto desde la entrada estándar
    std::cout << "Ingrese la altura del laberinto: "; // Solicita la altura del laberinto
    std::cin >> height; // Lee la altura del laberinto desde la entrada estándar

    // Asegurarse de que el tamaño del laberinto sea impar
    if (width % 2 == 0) width += 1; // Si el ancho es par, lo incrementa en 1 para hacerlo impar
    if (height % 2 == 0) height += 1; // Si la altura es par, la incrementa en 1 para hacerla impar

    Maze maze(width, height); // Crea un objeto Maze con el ancho y alto especificados
    maze.generate(); // Genera el laberinto

    std::cout << "Laberinto generado:\n"; // Imprime un mensaje indicando que el laberinto ha sido generado
    maze.print(); // Imprime el laberinto generado

    if (maze.solve()) { // Si se encuentra una solución para el laberinto
        std::cout << "Se encontró una solución para el laberinto:\n"; // Imprime un mensaje indicando que se encontró una solución
        maze.print(); // Imprime el laberinto con la solución marcada
    } else { // Si no se encuentra una solución para el laberinto
        std::cout << "No se encontró una solución para el laberinto.\n"; // Imprime un mensaje indicando que no se encontró una solución
    }

    return 0; // Retorna 0 indicando que el programa terminó correctamente
}