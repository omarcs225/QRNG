from flask import Flask, request, jsonify
import qiskit
from qiskit_aer import AerSimulator
from qiskit import transpile, QuantumCircuit

app = Flask(__name__)

def quantum_random_numbers(num_bits, num_random_numbers):
    simulator = AerSimulator()
    random_numbers = []
    for _ in range(num_random_numbers):
        qc = QuantumCircuit(num_bits)
        for qubit in range(num_bits):
            qc.h(qubit)
        qc.measure_all()
        qc = transpile(qc, simulator)
        result = simulator.run(qc, shots=1).result()
        counts = result.get_counts()
        bitstring = list(counts.keys())[0]
        random_number = int(bitstring, 2)
        random_numbers.append(random_number)
    return random_numbers

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    num_bits = data.get("num_bits")
    num_random_numbers = data.get("num_random_numbers")
    random_numbers = quantum_random_numbers(num_bits, num_random_numbers)
    return jsonify(random_numbers=random_numbers)

if __name__ == '__main__':
    app.run(port=5000)
