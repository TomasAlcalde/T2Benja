# Tarea 2: DCConejoChico 🐇💨


Un buen ```README.md``` puede marcar una gran diferencia en la facilidad con la que corregimos una tarea, y consecuentemente cómo funciona su programa, por lo en general, entre más ordenado y limpio sea éste, mejor será 

Para nuestra suerte, GitHub soporta el formato [MarkDown](https://es.wikipedia.org/wiki/Markdown), el cual permite utilizar una amplia variedad de estilos de texto, tanto para resaltar cosas importantes como para separar ideas o poner código de manera ordenada ([pueden ver casi todas las funcionalidades que incluye aquí](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet))

Un buen ```README.md``` no tiene por que ser muy extenso tampoco, hay que ser **concisos** (a menos que lo consideren necesario) pero **tampoco pueden** faltar cosas. Lo importante es que sea claro y limpio 

**Dejar claro lo que NO pudieron implementar y lo que no funciona a la perfección. Esto puede sonar innecesario pero permite que el ayudante se enfoque en lo que sí podría subir su puntaje.**

## Consideraciones generales :octocat:

Abre la ventana de inicio, recibe un username y lo corrige para ver si esta malo, ademas de mostrar el salon de la fama actualizado al servidor. Al poner un username con las especificaciones correctas, se abre la ventana de juego, donde se puede ver que se puede mover el conejo con las teclas WASD, se mueven los lobos y las zanahorias (de los canones) a sus velocidades correspondientes, se puede poner pausa con la letra P, se pueden recoger objetos con la letra G, se puede poner los trucos "K + I + L" y "I + N + F". El conejo choca con las paredes por lo que no lo permite moverse mas alla, cuando choca con un lobo o zanahoria, se le resta una vida y vuelve al inicio, al acabarse el tiempo pierde una vida (no logre que volviera al principio) y tira un mensaje de que se le acabo el tiempo. Todo esta hecho en base a señales entre frontend y backend para el manejo de la logica del juego y los elementos graficos del juego, en donde podemos ver que el frontend tiene todo lo requerido, botones de pausa y salir (funcionales), inventario que se actualiza, vidas que se actualizan, tiempo que se actualiza y el tablero que tambien se actualiza. En relacion al uso de objetos, no logre que funcionara ni la bomba de manzana ni la bomba de congelacion, al pasar un nivel se pasa directamente al siguiente guardando el puntaje en el servidor (el cual lamentablemente al no poder eliminar lobos por el mal funcionamiento de la bomba de manzana, siempre da 0.0 (a menos que se este en modo INF)). En caso de salirse a la mitad guarda el ultimo puntaje del ultimo nivel, cuando se pasa el ultimo nivel termina el juego y guarda el puntaje total, mostrando un mensaje de que ganaste. 

Los sonidos estan implementados pero no funcionan bien.

Los archivos cumplen con las reglas de pep8, las lineas son lo suficientemente largas sin pasarse, clases con Mayusculas etc.

### Cosas implementadas y no implementadas :white_check_mark: :x:


#### Entrega Final: 46 pts (75%)
##### ✅ Ventana Inicio: 
Se visualiza correctamente la ventana mostrando lo solicitado en donde el salon de fama se actualiza, las validaciones son cliente servidor notificando en caso de que no se cumpla algo. El boton salir cierra la ventana y termina el programa.
##### ✅ Ventana Juego:
Se cargan correctamente los archivos del laberinto, se visualiza todo correctame lo que piden (exceptuando que al recoger un objeto este se elimina del backend pero no del frontend). Las estadisticas de tiempo, vidas, puntaje, etc se van actualizando a medida que el juego progresa, el boton de salir funciona correctamente.
##### 🟠 ConejoChico:
Cuando colisiona el conejo con un lobo o una zanahoria este pierde una vida y vuelve al principio (hay cierto margen de error en la colision, por lo tanto hay veces que "toca" y no se muere el conejo).
El movimiento de conejo chico es fluido y se detiene al chocar con la pared (tiene un pequeño error que cuando se mantiene apretado la tecla para avanzar, el frontend no alcanza a recibir tan rapido la actualizacion, por lo que descuadra del camino), pero si se hace apretando la direccion para moverse tecla por tecla (con un margen de unos 0.5 segundos por cada click) no deberia descarrilarse y seguiria el camino de manera correcta. Siempre este avanzara a la direccion y un movimiento por cada tecla correspondiente, si el tiempo se agota este pierde una vida, pero no vuelve a su parte inicial.
##### ✅ Lobos:
Funcionan correctamente, tienen direccion y velocidades individuales
##### ✅ Cañón de Zanahorias:
Funcionan correctamente, tienen dirrecion dependiendo de donde apunte y se mueven de manera independiente.
##### 🟠 Bomba Manzana:
No implementado la funcionalidad de hacer click, sin embargo se muestra el objeto en el inventario cuando se apreta g encima de uno de ellos y se acumulan en el inventario en el frontend y el backend. (Falto solo implementar el click y la explocion)
##### 🟠 Bomba Congeladora:
No implementado la funcionalidad de hacer click, sin embargo se muestra el objeto en el inventario cuando se apreta g encima de uno de ellos y se acumulan en el inventario en el frontend y el backend. (Falto solo implementar el click y la explocion)
##### ✅ Fin del nivel:
Implementadas ambas formas de terminar el nivel, unicamente al pasar de nivel se manda la info al servidor y se actualiza en puntaje.txt
##### ✅🟠 Fin del Juego: 
Se notifica con el mensaje y se muestra el puntaje total, aunque este implementado el sonido no suena.
##### 🟠 Recoger (G):
Funciona recoger objetos pero no ponerlos con el click, la imagen no se borra del frontend cuando se recoge, pero si del back por lo que no se puede recoger denuevo (Viendo lo positivo)
##### ✅ Cheatcodes (Pausa, K+I+L, I+N+F):
Funcionan correctamente los 3, sin fallas.
##### ✅ Networking:
Funciona correctamente
##### ✅ Decodificación:
Funciona correctamente
##### ✅ Desencriptación: 
Funciona correctamente
##### ✅ Archivos:
Distribuidos de manera correcta en su arquitectura
##### ✅ Funciones:
Correcto uso de las funciones, cambiandolas a su respectivo funcionamiento con las clases y el manejo de senales entre backend y frontend


## Ejecución :computer:
Para ejecutar cada parte respectivamente de servidor y cliente, se debe abrir ```python main.py``` en servidor y ```python main.py``` en cliente pero dentro de su respectiva carpeta, para que corran las rutas (de sprites, sonidos, laberintos etc) de cada uno correctamente.


## Librerías :books:
### Librerías externas utilizadas
Pyqt6 y todos sus derivados

### Librerías propias


## Supuestos y consideraciones adicionales :thinking:


1. Especial ojo al movimiento del conejo, funciona bien menos cuando se mantiene apretado el boton, por lo que al probar ir apretando una tecla a la vez de movimiento.
2. Como no se implemento las bombas, el puntaje no cambia de 0.0 al no poder eliminar lobos, pero la formula del backend funciona (en caso de querer comprobar, cambiar numero de self.lobos_eliminados a 1 y la formula dara un puntaje "real")
3. ...

PD: <una última consideración (de ser necesaria) o comentario hecho anteriormente que se quiera **recalcar**>


-------



**EXTRA:** si van a explicar qué hace específicamente un método, no lo coloquen en el README mismo. Pueden hacerlo directamente comentando el método en su archivo. Por ejemplo:

```python
class Corrector:

    def __init__(self):
          pass

    # Este método coloca un 6 en las tareas que recibe
    def corregir(self, tarea):
        tarea.nota  = 6
        return tarea
```

Si quieren ser más formales, pueden usar alguna convención de documentación. Google tiene la suya, Python tiene otra y hay muchas más. La de Python es la [PEP287, conocida como reST](https://www.python.org/dev/peps/pep-0287/). Lo más básico es documentar así:

```python
def funcion(argumento):
    """
    Mi función hace X con el argumento
    """
    return argumento_modificado
```
Lo importante es que expliquen qué hace la función y que si saben que alguna parte puede quedar complicada de entender o tienen alguna función mágica usen los comentarios/documentación para que el ayudante entienda sus intenciones.

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \<link de código>: este hace \<lo que hace> y está implementado en el archivo <nombre.py> en las líneas <número de líneas> y hace <explicación breve de que hace>

## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/Syllabus/blob/main/Tareas/Bases%20Generales%20de%20Tareas%20-%20IIC2233.pdf).