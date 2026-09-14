#!/usr/bin/env python3
import numpy as np
import time

class SimuladorMegapenteractoBlindado:
    def __init__(self, tamano=100, capacidad_critica=10, max_paquetes_por_lote=15000000):
        self.tamano = tamano
        self.total_nodos = int(tamano ** 5)
        self.capacidad_critica = capacidad_critica
        self.max_lote = max_paquetes_por_lote
        self.strides_vecinos = np.array([1, -1, tamano, -tamano, tamano**2, -(tamano**2), tamano**3, -(tamano**3), tamano**4, -(tamano**4)], dtype=np.int64)
        self.nodos_muertos = set()

    def _procesar_bloque_montecarlo(self, sub_paquetes):
        coords_orig = np.random.randint(0, self.tamano, size=(5, sub_paquetes), dtype=np.int64)
        coords_dest = np.random.randint(0, self.tamano, size=(5, sub_paquetes), dtype=np.int64)
        atractores = np.random.rand(sub_paquetes) < 0.85
        num_atractores = np.sum(atractores)
        if num_atractores > 0:
            coords_dest[:, atractores] = np.random.randint(45, 55, size=(5, num_atractores), dtype=np.int64)
        factores = np.array([self.tamano**4, self.tamano**3, self.tamano**2, self.tamano, 1], dtype=np.int64)[:, None]
        return np.concatenate([np.sum(coords_orig * factores, axis=0), np.sum(coords_dest * factores, axis=0)])

    def ejecutar_ciclo_seguro(self, paso, num_paquetes_totales=150000000):
        inicio = time.time()
        lotes_totales = int(np.ceil(num_paquetes_totales / self.max_lote))
        print(f"🔄 [RÁFAGA {paso}] Procesando {num_paquetes_totales:,} paquetes...")
        for i in range(0, num_paquetes_totales, self.max_lote):
            lote_actual = min(self.max_lote, num_paquetes_totales - i)
            flujo_sublote = self._procesar_bloque_montecarlo(lote_actual)
            sub_ids, sub_conteos = np.unique(flujo_sublote, return_counts=True)
            sobrecargados_sublote = sub_ids[sub_conteos >= self.capacidad_critica]
            if len(self.nodos_muertos) > 0:
                sobrecargados_sublote = sobrecargados_sublote[np.isin(sobrecargados_sublote, list(self.nodos_muertos), invert=True)]
            if len(sobrecargados_sublote) > 0:
                self.nodos_muertos.update(sobrecargados_sublote)
                vecinos_cascada = []
                for stride in self.strides_vecinos:
                    vecinos_cascada.extend((sobrecargados_sublote + stride) % self.total_nodos)
                self.nodos_muertos.update(vecinos_cascada)
        tasa_supervivencia = ((self.total_nodos - len(self.nodos_muertos)) / self.total_nodos) * 100
        print(f"✅ Ráfaga {paso} FINALIZADA GLOBALMENTE EN {time.time()-inicio:.2f}s\n")

if __name__ == "__main__":
    simulador = SimuladorMegapenteractoBlindado(tamano=100, capacidad_critica=10)
    for paso in range(1, 4):
        simulador.ejecutar_ciclo_seguro(paso=paso, num_paquetes_totales=150000000)
