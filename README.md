# Simulador de Red de Frontera: Megapenteracto 5D (10B Nodos)

Este proyecto implementa un simulador estocástico de **Eventos Discretos por Montecarlo** optimizado para modelar una red en un espacio de 5 dimensiones (*Penteracto*) con un volumen teórico de **10,000,000,000 de nodos lógicos** y **100,000,000,000 de conexiones implícitas**.

## 🚀 Características y Arquitectura HPC
* **Consumo de RAM Sub-Gigabyte:** Paradigma de Vectores Dispersos Implícitos (0 bytes base, <1.8 GB en pico).
* **Alineación de Caché por Strides:** Cálculo de fallos lineal mediante zancadas directas en 64 bits.
* **Auto-Inmunización Topológica:** El modelo demuestra empíricamente cómo el colapso del núcleo actúa como un cortafuegos pasivo que protege el resto del penteracto.
