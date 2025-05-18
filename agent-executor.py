import zmq
import unittest
import io
import sys

# Configurar ZMQ
context = zmq.Context()
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:5556")

sender_dev = context.socket(zmq.PUSH)
sender_dev.bind("tcp://*:5557")

print("Se ha iniciado el agent-executor.")
# Recibir pruebas del tester

# Ejecutar pruebas
def run_tests(test_code):
    # Crear un espacio de nombres para ejecutar el código
    namespace = {}
    
    print(f"Recibí del agent-tester: {test_code}")

    # Ejecutar el código de las pruebas en el espacio de nombres
    exec(test_code, namespace)
    
    # Encontrar todas las clases de prueba en el espacio de nombres
    test_classes = [v for v in namespace.values() if isinstance(v, type) and issubclass(v, unittest.TestCase)]
    
    # Crear una suite de pruebas
    suite = unittest.TestSuite()
    for test_class in test_classes:
        suite.addTest(unittest.makeSuite(test_class))
    
    # Ejecutar las pruebas y capturar la salida
    output = io.StringIO()
    runner = unittest.TextTestRunner(stream=output)
    result = runner.run(suite)
    
    return output.getvalue(), result.wasSuccessful()

while True:
    tests = receiver.recv_string()
    print("Pruebas recibidas del tester.")
    # Ejecutar las pruebas
    output, success = run_tests(tests)

    # Imprimir resultados
    print("Resultados de las pruebas:")
    print(output)

    if success:
        print("Todas las pruebas pasaron exitosamente.")
    else:
        print("Algunas pruebas fallaron.")
        sender_dev.send_string(output)
