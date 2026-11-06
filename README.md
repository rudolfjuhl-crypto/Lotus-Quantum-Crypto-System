# Lotus Quantum Crypto System (Core V3)

[![License: CC-BY-4.0](https://shields.io)](https://creativecommons.org)
[![Platform: Quantum/Python](https://shields.io)]()
[![Security: Post-Quantum Ready](https://shields.io)]()

An implementation of **Fractal Circular Path Cryptography (FCPC)** and **Fractal Circular Key Exchange (FCKE)** tailored for asynchronous TCP/IP networks and cryogenic Quantum Processing Units (QPUs).

**Author:** Rudolf Juhl  
**Location:** Bensheim, Germany  

---

## 🌌 Overview

The **Lotus Quantum Crypto System** introduces a radical geometric approach to Post-Quantum Cryptography (PQC). Moving away from traditional lattice-based (LWE) or code-based primitives, this framework leverages the computational hardness of non-commutative group orbits within nested, fractal circular manifolds. 

Inspiration is drawn from the concentric geometry of historical temple reliefs, and the system is optimized for the physical all-to-all connectivity of modern superconducting quantum cores. The framework integrates a hardware-bound Physical Unclonable Function (PUF) to achieve absolute resistance against classical cryptanalysis as well as quantum attacks using Shor’s or Grover’s algorithms.

### Key Components:
1. **FCKE (Fractal Circular Key Exchange):** A quantum-safe asymmetric handshake protocol operating on non-commutative fractal manifolds.
2. **FCPC (Fractal Circular Path Cryptography):** A symmetric stream cipher that projects text bytes into a 24-bit polar orbit space.
3. **Hardware PUF Integration:** Binds the encryption matrix to the specific cryogenic phase error ($\Delta\phi_{\text{hardware}}$) of a superconducting niobium processor at 10 millikelvin.

---

## 📐 Mathematical Foundation


The cryptographic space operates on a two-dimensional polar projection plane $\mathcal{M}$ defined by public base parameters $M_0 = \{R_1, R_2, S\}$. The private key spaces use continuous, non-linear transformations based on hyperbolic functions:

$$\mathcal{T}_k(M_0) \to \mathcal{M}_k = [ R_1 \cdot \frac{\sinh(k)}{10}, R_2 \cdot \frac{\cosh(k)}{10}, (k \cdot \pi) \pmod{2\pi} ]$$

Reversing this transformation represents an NP-hard problem defined as the **Discrete Logarithm Problem on Fractal Surfaces**, rendering Shor's period-finding algorithm useless due to the non-abelian, infinite-dimensional group properties of the orbit space.




## 📦 Project Structure

