---
title: Solvent History as a Design Principle for Crosslinked Elastomers
date: 2026-07-25
excerpt: Selective evaporation of solvents to tune entanglements and achieve softening without sacrificing strength.
---

# Solvent History as a Design Principle for Crosslinked Elastomers

## Motivation

Conventionally, stiffness and toughness of a polymer network are coupled: making the network
stiffer often makes it more brittle. Can the *history* of a solvent, rather than its final
composition, decouple these two properties?

## The Solvent-History Strategy

A model network is first swollen to a prescribed degree by a solvent, crosslinked, and then
the solvent is selectively evaporated. The final properties depend on the *path* taken:

$$
\mathcal{P} = \mathcal{F}(c_{\text{max}}, \dot{c}, T)
$$

where $c_{\text{max}}$ is the peak solvent concentration, $\dot{c}$ the evaporation rate,
and $T$ the temperature.

## Decoupling Stiffness and Toughness

The shear modulus $G$ scales with the crosslink density $\nu_x$ and the entanglement density
$\nu_e$:

$$
G \approx k_B T \left( \nu_x + \alpha \, \nu_e \right)
$$

Because solvent evaporation redistributes entanglements without changing the crosslink
density, we can soften the material (reduce $\nu_x$ contribution) while preserving its
toughness (maintained through $\nu_e$). This independent control is captured by the map:

$$
(\nu_x, \nu_e) \xrightarrow{\text{solvent history}} (G, \Gamma)
$$

where $\Gamma$ is the fracture energy.

## Conclusion

Solvent history offers a simple, scalable route to independently tune stiffness and
toughness in crosslinked elastomers — a principle that may extend to other soft materials.
